# Reliable, Scalable, and Maintainable Applications — Estudio

## Tarjetas de repaso

P: ¿Qué distingue a una aplicación data-intensive de una compute-intensive?
R: En la data-intensive el límite no es la potencia de CPU, sino la cantidad de datos, su complejidad y la velocidad a la que cambian.

P: ¿Cuáles son los bloques estándar con los que se construyen las aplicaciones data-intensive?
R: Bases de datos, cachés, índices de búsqueda, stream processing y batch processing.

P: ¿Cuáles son las tres preocupaciones que todo sistema de software debe atender según el capítulo?
R: Reliability (fiabilidad), scalability (escalabilidad) y maintainability (mantenibilidad).

P: ¿Qué diferencia hay entre un fault y un failure?
R: Un fault es la desviación de un componente respecto a su especificación; un failure es cuando el sistema entero deja de dar servicio.

P: ¿Qué es un sistema fault-tolerant o resilient?
R: Un sistema que anticipa los faults y los soporta, evitando que se conviertan en failures.

P: ¿Cuáles son los tres tipos de faults que afectan a la fiabilidad?
R: Hardware faults (aleatorios), software errors (sistemáticos y correlacionados entre nodos) y human errors.

P: Según el estudio citado, ¿cuál fue la principal causa de caídas en grandes servicios de internet?
R: Los errores de configuración de los operadores; el hardware intervino solo en el 10–25% de los casos.

P: ¿Qué son los load parameters?
R: Las magnitudes que describen la carga de un sistema (solicitudes/seg, ratio lecturas/escrituras, usuarios activos, hit rate de caché), según la arquitectura.

P: ¿En qué se diferencian latency y response time?
R: El response time es lo que ve el cliente (incluye retrasos de red y de cola); la latency es el tiempo que una solicitud espera a ser atendida.

P: ¿Por qué se usan percentiles en lugar de la media para el response time?
R: Porque el response time es una distribución; la media no es buen indicador y los percentiles (p50, p95, p99, p999) reflejan el tiempo típico y las tail latencies.

P: ¿Por qué Amazon especifica requisitos en el p99.9?
R: Porque sus clientes más lentos suelen ser los más valiosos (los que más datos/compras tienen).

P: ¿Qué diferencia hay entre scaling up y scaling out?
R: Scaling up es escalado vertical (máquina más potente); scaling out es escalado horizontal con arquitectura shared-nothing. Los buenos diseños mezclan ambos.

P: ¿Cuáles son los tres principios de diseño de la mantenibilidad?
R: Operability (operabilidad), simplicity (simplicidad) y evolvability (evolucionabilidad).

P: ¿Qué es la complejidad accidental según Moseley y Marks?
R: La complejidad que no es inherente al problema sino a su implementación; conviene eliminarla, y la mejor herramienta es la abstracción.

P: ¿Qué es el tail latency amplification?
R: El efecto por el cual, al hacer varias llamadas a backend, basta una llamada lenta para ralentizar toda la solicitud del usuario.

## Preguntas de autoevaluación

P: ¿Por qué tiene sentido agrupar bases de datos, colas y cachés bajo el término "sistemas de datos"? (sección "Thinking About Data Systems")
R: Porque las categorías tradicionales ya no encajan (p. ej., Redis usado de cola, Kafka con durabilidad de base de datos) y una sola herramienta no cubre requisitos exigentes, así que se combinan tras una API creando un sistema de propósito especial.

P: En el caso de Twitter, ¿por qué se pasó del enfoque de mezclar tweets al leer al de fan-out en la escritura? (sección "El ejemplo que recorre el capítulo")
R: Porque la tasa de publicación es casi dos órdenes de magnitud menor que la de lecturas, por lo que conviene trabajar más al escribir y menos al leer; el enfoque de lectura no soportaba la carga de 300k timelines/seg.

P: ¿Cuál es el load parameter clave en el ejemplo de Twitter y cómo influyó en la solución final? (sección "El ejemplo que recorre el capítulo")
R: La distribución de seguidores por usuario; como las celebridades generan hasta más de 30 millones de escrituras por tweet, la solución final es híbrida: fan-out en la escritura para la mayoría y mezcla al leer para los usuarios con muchos seguidores.

P: ¿Por qué provocar faults deliberadamente mejora la fiabilidad y por qué esto no aplica igual en seguridad? (sección "Reliability")
R: Provocar faults (p. ej., Chaos Monkey) ejercita los mecanismos de tolerancia y da confianza en que funcionan; en seguridad, en cambio, prevenir es mejor que curar.

P: ¿Qué medidas propone el capítulo para reducir los human errors? (sección "Reliability")
R: Diseñar para minimizar oportunidades de error, desacoplar donde se cometen errores de donde causan fallos (sandbox con datos reales), probar a todos los niveles, permitir recuperación rápida (rollback, despliegue gradual), monitorización detallada y buenas prácticas de gestión y formación.

P: ¿Por qué es erróneo promediar percentiles de varias instancias? (sección "Scalability")
R: Porque matemáticamente no tiene sentido; para combinar la distribución hay que sumar los histogramas, usando algoritmos como forward decay, t-digest o HdrHistogram.

P: ¿Por qué el capítulo afirma que no existe una "magic scaling sauce"? (sección "Scalability")
R: Porque la arquitectura escalable es muy específica de la aplicación, se construye sobre suposiciones de qué operaciones serán comunes, y en una startup suele importar más iterar rápido que escalar a una carga hipotética.

P: ¿Qué quiere decir la cita "las buenas operaciones pueden sortear las limitaciones de un software malo, pero el buen software no funciona de forma fiable con malas operaciones"? (sección "Maintainability")
R: Que la operabilidad es decisiva: aunque el software sea bueno, necesita buenas operaciones para funcionar con fiabilidad; por eso se diseña para facilitar el trabajo del equipo de operaciones.

## Puntos a dominar

- Explicar qué significa data-intensive y nombrar los cinco bloques estándar (bases de datos, cachés, índices, stream, batch).
- Distinguir con precisión fault vs failure y los tres tipos de faults (hardware, software, humanos) con su naturaleza (aleatoria, sistemática, operativa).
- Razonar la escalabilidad con load parameters y describir el rendimiento con throughput (batch) y response time (online).
- Diferenciar latency y response time, y saber interpretar p50, p95, p99, p999 como distribución y no como número único.
- Reproducir el equilibrio escritura/lectura del caso Twitter y por qué la solución final es híbrida.
- Enumerar los tres principios de mantenibilidad (operability, simplicity, evolvability) y asociar cada uno a su idea central (visibilidad/automatización, complejidad accidental/abstracción, agilidad ante el cambio).
