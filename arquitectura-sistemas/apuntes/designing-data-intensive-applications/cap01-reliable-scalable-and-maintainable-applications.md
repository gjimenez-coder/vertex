# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 1 — Reliable, Scalable, and Maintainable Applications (Aplicaciones fiables, escalables y mantenibles)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Muchas aplicaciones actuales son data-intensive (intensivas en datos) y no compute-intensive: el límite rara vez es la potencia de CPU, sino la cantidad de datos, su complejidad y la velocidad a la que cambian. Estas aplicaciones se construyen a partir de bloques estándar: bases de datos (almacenar datos), cachés (recordar resultados caros para acelerar lecturas), índices de búsqueda (buscar y filtrar), stream processing (enviar mensajes para procesarlos de forma asíncrona) y batch processing (procesar periódicamente grandes volúmenes acumulados).

El capítulo introduce la idea de "sistema de datos" como término paraguas: las fronteras entre categorías se difuminan (Redis como datastore usado de cola; Apache Kafka como cola con garantías de durabilidad similares a una base de datos) y cada vez más aplicaciones combinan varias herramientas con código de aplicación, convirtiendo al desarrollador también en diseñador de sistemas de datos.

La tesis central es que todo sistema de software debe atender tres preocupaciones: reliability (fiabilidad), scalability (escalabilidad) y maintainability (mantenibilidad). El resto del capítulo aclara qué significan esas palabras y ofrece formas de razonar sobre ellas, sentando la base para los capítulos siguientes.

## El ejemplo que recorre el capítulo

El hilo conductor de la sección de escalabilidad es Twitter, con datos publicados en noviembre de 2012. Dos operaciones principales: publicar un tweet (4,6k solicitudes/seg de media, >12k en pico) y la home timeline (300k solicitudes/seg). El verdadero reto no es el volumen de tweets sino el fan-out: cada usuario sigue a muchos y es seguido por muchos. Hay dos enfoques:

1. Insertar cada tweet en una colección global y, al pedir la timeline, buscar a quién sigue el usuario, recuperar sus tweets y mezclarlos ordenados por tiempo (con un JOIN en un esquema relacional).
2. Mantener una caché por usuario (como un buzón): al publicar, insertar el tweet en la timeline de cada seguidor, de modo que leer la timeline sea barato.

Twitter empezó con el enfoque 1, pero no soportaba la carga de lecturas y pasó al 2, porque la tasa de publicación es casi dos órdenes de magnitud menor que la de lecturas: conviene trabajar más al escribir y menos al leer. El coste: 4,6k tweets/seg se convierten en 345k escrituras/seg a las cachés (media de ~75 seguidores), y algunos usuarios superan los 30 millones de seguidores, lo que puede provocar más de 30 millones de escrituras por un solo tweet (a entregar en ~5 segundos). La distribución de seguidores por usuario es el load parameter clave. La solución final es híbrida: fan-out en la escritura para la mayoría, pero las celebridades se exceptúan y sus tweets se mezclan al leer (enfoque 1).

## Thinking About Data Systems (Pensar en sistemas de datos)

Agrupar bases de datos, colas y cachés bajo "sistemas de datos" tiene sentido porque las categorías tradicionales ya no encajan y porque una sola herramienta no cubre requisitos exigentes. Al combinar herramientas tras una API que oculta la implementación, se crea un sistema de datos de propósito especial a partir de componentes generales, que debe ofrecer ciertas garantías (p. ej., invalidar o actualizar la caché en las escrituras para que los clientes vean resultados consistentes).

## Reliability (Fiabilidad)

Fiabilidad es, a grandes rasgos, "seguir funcionando correctamente incluso cuando las cosas van mal". Lo que puede ir mal son faults (fallos de componente); los sistemas que los anticipan y los soportan son fault-tolerant o resilient. Un fault no es lo mismo que un failure: el fault es una desviación de la especificación de un componente, el failure es cuando el sistema entero deja de dar servicio. No se puede reducir la probabilidad de fault a cero, así que se diseñan mecanismos de tolerancia que eviten que los faults causen failures. Conviene provocar faults deliberadamente para ejercitar esa maquinaria (ejemplo: Netflix Chaos Monkey). En seguridad, en cambio, prevenir es mejor que curar.

- Hardware faults: discos que se estropean, RAM defectuosa, cortes de luz, cables mal conectados. MTTF de discos de ~10 a 50 años; en un clúster de 10.000 discos se espera que muera uno al día. La respuesta tradicional es redundancia (RAID, fuentes duales, generadores). Con más máquinas crece la tasa de faults, y plataformas como AWS pueden dejar instancias indisponibles sin aviso, por lo que se tiende a tolerar la pérdida de máquinas enteras por software (rolling upgrade sin downtime total).
- Software errors: errores sistemáticos, correlacionados entre nodos, difíciles de anticipar (p. ej., el bug del leap second del 30 de junio de 2012 en el kernel de Linux; procesos desbocados; dependencias que se degradan; fallos en cascada). No hay solución rápida: pensar las suposiciones, pruebas exhaustivas, aislamiento de procesos, permitir crash y reinicio, medir/monitorizar y comprobaciones internas con alertas.
- Human errors: en un estudio de grandes servicios de internet, los errores de configuración de los operadores fueron la principal causa de caídas (el hardware intervino solo en el 10–25%). Mitigaciones: diseñar para minimizar oportunidades de error, desacoplar donde se cometen errores de donde causan fallos (sandbox con datos reales), probar a todos los niveles, permitir recuperación rápida (rollback, despliegue gradual, recomputar datos), monitorización detallada (telemetry) y buenas prácticas de gestión y formación.

La fiabilidad importa incluso en aplicaciones "no críticas" (ejemplo: el padre que guarda fotos de sus hijos). A veces se sacrifica (prototipos, márgenes estrechos), pero siempre siendo conscientes de ello.

## Scalability (Escalabilidad)

Escalabilidad es la capacidad de afrontar un aumento de carga; no es una etiqueta unidimensional ("X escala") sino preguntarse cómo crecer y cómo añadir recursos.

- Describir la carga: con load parameters (solicitudes/seg, ratio lecturas/escrituras, usuarios activos, hit rate de caché), según la arquitectura.
- Describir el rendimiento: en batch (como Hadoop) importa el throughput; en sistemas online, el response time. Latency y response time no son lo mismo: el response time es lo que ve el cliente (incluye retrasos de red y de cola); la latency es el tiempo que una solicitud espera a ser atendida.
- El response time es una distribución, no un número. La media no es buen indicador; mejor usar percentiles: la mediana (p50) indica el tiempo típico; p95, p99 y p999 son tail latencies que afectan a la experiencia. Amazon especifica requisitos en el p99.9 porque sus clientes más lentos suelen ser los más valiosos; observó que +100 ms reduce ventas un 1%, y otros que +1 s baja un 16% una métrica de satisfacción. Optimizar el p99.99 resultó demasiado caro para poco beneficio.
- Percentiles y SLO/SLA: definen rendimiento y disponibilidad esperados. Las colas (queueing delays) dominan los percentiles altos (head-of-line blocking), por lo que conviene medir del lado del cliente y, al generar carga de prueba, enviar solicitudes de forma independiente del tiempo de respuesta.
- Varias llamadas a backend amplifican la cola (tail latency amplification): basta una llamada lenta para ralentizar toda la solicitud. Para calcular percentiles de forma eficiente existen algoritmos como forward decay, t-digest o HdrHistogram; promediar percentiles es matemáticamente erróneo (hay que sumar los histogramas).
- Afrontar la carga: scaling up (vertical) frente a scaling out (horizontal, arquitectura shared-nothing); los buenos diseños mezclan ambos. Sistemas elásticos (añaden recursos automáticamente) frente a escalado manual (más simple, menos sorpresas). Distribuir servicios sin estado es sencillo; distribuir sistemas con estado añade complejidad, de ahí la sabiduría tradicional de escalar en vertical hasta que el coste o la alta disponibilidad obliguen a distribuir. No existe una "magic scaling sauce": la arquitectura escalable es muy específica de la aplicación y se construye sobre suposiciones de qué operaciones serán comunes; en una startup suele importar más iterar rápido que escalar a una carga hipotética.

## Maintainability (Mantenibilidad)

La mayor parte del coste del software está en el mantenimiento continuo, no en el desarrollo inicial. Tres principios de diseño:

- Operability (operabilidad): facilitar al equipo de operaciones mantener el sistema en marcha. "Las buenas operaciones pueden sortear las limitaciones de un software malo, pero el buen software no funciona de forma fiable con malas operaciones" (PDF p. 41). Ayuda dar visibilidad del comportamiento en ejecución, soporte para automatización, evitar dependencia de máquinas concretas, buena documentación, buenos defaults con posibilidad de sobrescribirlos, self-healing con control manual y comportamiento predecible.
- Simplicity (simplicidad): gestionar la complejidad. Síntomas: explosión del espacio de estados, acoplamiento fuerte, dependencias enredadas, nombres inconsistentes, hacks de rendimiento. Un proyecto así es un big ball of mud. Conviene eliminar la complejidad accidental (la que no es inherente al problema sino a la implementación, según Moseley y Marks). La mejor herramienta es la abstracción (lenguajes de alto nivel ocultan el código máquina; SQL oculta estructuras en disco y memoria), aunque encontrar buenas abstracciones es difícil, sobre todo en sistemas distribuidos.
- Evolvability (evolucionabilidad): facilitar el cambio ante requisitos cambiantes. En lo organizativo ayudan patrones ágiles (TDD, refactoring), aquí aplicados a nivel de sistema de datos completo. La facilidad de modificar un sistema está ligada a su simplicidad y sus abstracciones; se usa "evolvability" para referirse a la agilidad a nivel de sistema de datos.

## Ideas clave

- Las aplicaciones data-intensive se construyen con bloques estándar (bases de datos, cachés, índices, stream y batch processing) y las fronteras entre categorías se difuminan.
- Combinar herramientas tras una API convierte al desarrollador en diseñador de sistemas de datos, que debe ofrecer garantías propias.
- Fiabilidad = seguir funcionando pese a faults de hardware (aleatorios), software (sistemáticos y correlacionados) y humanos (los operadores causan la mayoría de caídas).
- Un fault es la desviación de un componente; un failure es la caída del sistema. Se diseñan mecanismos para que los faults no se conviertan en failures; provocarlos adrede (Chaos Monkey) ayuda.
- Escalabilidad se razona con load parameters y midiendo el rendimiento; el caso de Twitter ilustra el fan-out y el equilibrio entre trabajo en escritura y en lectura.
- El response time es una distribución: usar percentiles (p50, p95, p99, p999); las tail latencies afectan a los clientes más valiosos y se formalizan en SLO/SLA.
- Escalar admite vertical y horizontal (shared-nothing); no hay arquitectura escalable universal, cada una es específica de la aplicación.
- Mantenibilidad se apoya en operabilidad, simplicidad (reducir complejidad accidental con abstracciones) y evolvability.
