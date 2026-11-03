# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 5 — Stability Patterns (Patrones de estabilidad)

> Nota de extracción: texto extraído de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo es la cara positiva del anterior (los antipatrones): presenta patrones de arquitectura y diseño que reducen, eliminan o mitigan el daño de las grietas que se propagan por un sistema. Ninguno ayuda a pasar QA, pero sí a dormir tranquilo una vez que el software está en producción. La tesis central es que las fallas son inevitables (“todo sistema acaba operando fuera de especificación”), así que hay que cultivar una mentalidad orientada a la recuperación: esperar la falla y aplicar patrones para limitar el daño de cada una.

Nygard advierte explícitamente contra medir la calidad por “cantidad de patrones aplicados”: no es una buena métrica. Los patrones se aplican con juicio, identificando las amenazas y eligiendo la defensa apropiada para cada una. El autor resume esta actitud como “la paranoia es buena ingeniería”: examina los requisitos con cinismo y mira el resto de sistemas de la empresa con desconfianza, porque cualquiera puede apuñalarte por la espalda.

Sales sabiendo doce patrones complementarios: Timeouts, Circuit Breaker, Bulkheads, Steady State, Fail Fast, Let It Crash, Handshaking, Test Harnesses, Decoupling Middleware, Shed Load, Create Back Pressure y Governor. Varios se refuerzan entre sí (timeouts con circuit breakers, fail fast con timeouts, back pressure con shed load).

## Timeouts

Hoy todo sistema es distribuido y las redes son falibles: el código no puede esperar para siempre una respuesta que quizá nunca llegue. “Hope is not a design method” (PDF p. 103). Los timeouts bien ubicados aportan aislamiento de fallas: un problema en otro servicio no tiene por qué volverse tuyo. Las APIs de alto nivel suelen carecer de timeouts explícitos, y las librerías cliente comerciales son notoriamente pobres en esto porque ocultan el socket.

Todo pool de recursos que bloquea hilos debe tener timeout para que los hilos eventualmente se desbloqueen, haya o no recursos. Igual con mutexes y sincronización a nivel de lenguaje: usa siempre la variante con argumento de timeout. Conviene agrupar operaciones largas en primitivas reutilizables (por ejemplo un gateway genérico con un query object) para manejar bien el timeout en un solo lugar; eso también facilita aplicar Circuit Breaker.

Los timeouts suelen acompañarse de reintentos, pero reintentar de inmediato tras una falla casi siempre vuelve a fallar: dentro de un data center el problema del otro extremo suele durar un rato. Mejor devolver una respuesta (éxito, fallo o trabajo encolado) que hacer esperar al cliente. Encolar y reintentar más tarde (store-and-forward, como el correo) hace el sistema más robusto. Para una API web, “suficientemente rápido” está entre 10 y 100 ms. Timeouts protege peticiones salientes; Fail Fast protege las entrantes: dos caras de la misma moneda.

## Circuit Breaker

Inspirado en el disyuntor eléctrico: un componente que falla primero para no destruir el sistema completo, y que puede resetearse al pasar el peligro. Envuelve operaciones peligrosas y evita llamadas cuando el sistema no está sano (a diferencia del reintento, que reejecuta).

Tres estados:
- **Closed** (cerrado): ejecuta normalmente; si falla, cuenta la falla.
- **Open** (abierto): al superar el umbral de fallas, las llamadas fallan de inmediato sin ejecutar la operación real; puede lanzar una excepción distinta a un timeout o aplicar una estrategia de *fallback* (última respuesta buena, valor en caché, respuesta genérica o servicio secundario).
- **Half-Open** (semiabierto): tras un tiempo, deja pasar una llamada de prueba; si tiene éxito vuelve a cerrado, si falla vuelve a abierto.

Importa más la densidad de fallas que el conteo total (cinco fallas en cinco horas no es lo mismo que cinco en treinta segundos); el autor recomienda el patrón **Leaky Bucket**. Los cambios de estado deben registrarse y exponerse para monitoreo, y Operaciones debe poder abrir o resetear manualmente. Un circuit breaker vive en el ámbito de un solo proceso (compartirlo entre procesos añadiría otra comunicación fuera de proceso y un nuevo modo de falla). Conviene usar librerías open source ya existentes para evitar los terrores del multithreading. Involucrar a los stakeholders al definir el fallback es esencial, porque degrada funcionalidad del negocio.

## Bulkheads

Como los mamparos de un barco que lo dividen en compartimentos estancos: particionar el sistema para que una falla en una parte no destruya todo (contención del daño). La forma más común es la redundancia física; las VMs redundantes son menos robustas porque pueden terminar en el mismo host físico. A gran escala, granjas de servidores independientes (por ejemplo, servidores dedicados al check-in separados de las consultas de “estado de vuelo”); en la nube, correr instancias en distintas zonas y regiones. A escala pequeña, *process binding* (atar un proceso a uno o varios cores) evita que un proceso desbocado tumbe toda la máquina, y se pueden particionar los thread pools dentro de un proceso (por ejemplo reservar hilos para administración). En la nube los bulkheads pueden ser dinámicos con balanceadores definidos por software. Elige una granularidad útil; especialmente valioso en arquitecturas de servicios compartidos y microservicios.

## Steady State

Para cada mecanismo que acumula un recurso, debe existir otro que lo recicle. El enemigo es el *fiddling*: cada vez que un humano toca un servidor de producción es una oportunidad de error no forzado (ejemplo del ingeniero que “resilveró” el disco bueno desde el vacío y aniquiló el SO). Hay que mantener a la gente fuera de producción; el sistema debería correr al menos un ciclo de despliegue sin intervención manual. El extremo lógico es la infraestructura inmutable.

Tipos de “lodo” que se acumulan:
- **Purga de datos**: siempre se posterga (“seis meses después del lanzamiento”), pero el crecimiento de datos sube las tasas de I/O y la latencia. La purga debe hacerla la lógica de la aplicación para mantener la integridad referencial (un DBA no siempre sabe cómo se comporta la app sin esos datos).
- **Archivos de log**: sin control llenan el filesystem (en UNIX el 90–95 % ya da errores de I/O) y pueden desatar catástrofes (el “universal exception handler” reentrante que consumió ocho CPUs). Rotarlos (logrotate) y sacarlos pronto a un servidor centralizado como Logstash. Para cumplimiento (p. ej. SOX), conservarlos fuera de producción.
- **Caché en memoria**: pregúntate si el espacio de claves es finito y si los ítems cambian. Si no hay límite de claves, impón límites de tamaño e invalidación (un flush periódico suele bastar; también LRU o working-set). El mal uso de caché es la causa principal de fugas de memoria y reinicios diarios.

## Fail Fast

Si una respuesta lenta es peor que ninguna, lo peor es una respuesta de falla lenta. Si el sistema puede saber de antemano que fallará, mejor fallar rápido para no atar capacidad. No hace falta Deep Learning: hay una gran clase de fallas de “recurso no disponible”. La app puede, al recibir la petición, verificar conexiones a BD, integration points y el estado de los circuit breakers (el *mise en place* del chef) y validar parámetros básicos antes de tocar la BD. Hay que reportar de forma distinta una falla de sistema (recursos no disponibles) y una falla de aplicación (parámetros inválidos), para no hacer que un sistema aguas arriba abra un circuit breaker por datos de usuario erróneos. El caso de la imprenta fotográfica ilustra el patrón (ver abajo).

## Let It Crash

A veces la mejor estabilidad a nivel de sistema se logra abandonando la estabilidad a nivel de componente (filosofía de Erlang). El estado más limpio es justo tras el arranque, así que volver ahí rápido es mejor que una recuperación de errores difícil e inestable. Requiere:
- **Granularidad limitada**: un límite para la “crashiness” (el actor en Erlang/Elixir, o una instancia completa en microservicios); el resto se protege de la falla en cascada.
- **Reemplazo rápido**: volver a estado limpio en microsegundos (actores) o milisegundos (contenedores Go, proceso NodeJS). Si el arranque toma minutos (app JavaEE en VMs), “let it crash” no es la estrategia correcta.
- **Supervisión**: árbol jerárquico de supervisores que decide reiniciar al hijo, a todos los hijos o crashearse a sí mismo; el supervisor no es el consumidor del servicio. En PaaS/autoscaling la plataforma relanza, pero sin la discreción de un supervisor.
- **Reintegración**: tras reiniciar hay que volver a llamar al proveedor restaurado, vía circuit breakers o reincorporación al pool del balanceador cuando pasan los health checks.

No apliques este patrón a monolitos ni a procesos con runtimes pesados o arranques largos.

## Handshaking

Señalización entre dispositivos para regular la comunicación (EIA-232C, los módems, el three-phase handshake de TCP). Es ubicuo en protocolos de bajo nivel pero casi inexistente a nivel de aplicación: HTTP es malo para esto (el “503 Service Unavailable” no siempre se distingue). Sirve para que el servidor se proteja regulando su propia carga y rechazando trabajo. La mejor aproximación con HTTP es la alianza entre balanceador y servidores mediante health checks: el servidor avisa que está ocupado y el balanceador deja de enviarle trabajo. Circuit Breaker es el recurso cuando el servicio llamado no puede hacer handshaking. Construye handshaking en tus propios protocolos de bajo nivel.

## Test Harnesses

Los sistemas distribuidos tienen modos de falla difíciles de provocar en QA. El entorno de integración solo verifica qué hace el sistema cuando sus dependencias funcionan dentro de especificación, y tiende a volverse unitario (un único entorno global con control de cambios estricto) y a imponer version-locking. Un test harness emula el extremo remoto de cada integration point, corre como servidor separado (no obligado a cumplir ninguna interfaz) y debe ser malicioso: provocar errores de red, de protocolo y de aplicación, dejar cicatrices y volver cínico al sistema bajo prueba.

Se diferencia de los *mock objects*: un mock solo produce comportamiento conforme a la interfaz definida; el harness puede provocar fallas de red/protocolo que los mocks no. Puede simular múltiples fallas de socket (conexión rechazada, SYN/ACK sin datos, solo paquetes RESET, respuesta byte a byte cada 30 s, HTML en vez del XML esperado, etc.), cubriendo las cuatro categorías: transporte de red, protocolo de red, protocolo de aplicación y lógica de aplicación. Un truco útil: distintos puertos que provocan distintos malos comportamientos, así un solo harness rompe muchas apps. Suplementa (no reemplaza) otras pruebas y apunta hacia la *chaos engineering*.

## Decoupling Middleware

El middleware integra y desacopla sistemas a la vez. Como los integration points son la causa número uno de inestabilidad, desacoplar es bueno. Toda llamada síncrona (RPC, HTTP, XML-RPC, RMI, CORBA, DCOM… y JSON sobre HTTP) obliga al llamador a esperar y amplifica los shocks, facilitando fallas en cascada. El middleware orientado a mensajes (MQseries, pub/sub, SMTP, SMS, tuple spaces) desacopla en espacio y tiempo, y por eso no puede producir una falla en cascada. La ventaja del síncrono es su simplicidad lógica; el asíncrono es inherentemente más difícil de diseñar (colas de excepción, respuestas tardías, callbacks). A diferencia de otros patrones, elegir el middleware es una decisión de arquitectura casi irreversible que conviene tomar temprano (“decidir en el último momento responsable”).

## Shed Load

Los servicios no controlan su demanda: el mundo siempre puede generar más carga de la que puedes manejar (“you can’t out-scale the world”, PDF p. 131). Modela el enfoque de TCP, que rechaza conexiones con un RST cuando la listen queue se llena. Cuando la carga es demasiado alta, empieza a rechazar trabajo nuevo (relacionado con Fail Fast). Lo ideal es medir el propio rendimiento contra el SLA; si no, usar un semáforo que limite peticiones concurrentes. Una instancia puede responder 503 en su health check para que el balanceador la deje descansar. Dentro de los límites del sistema es más eficiente usar back pressure; shed load es la medida secundaria y la principal en los bordes expuestos a Internet.

## Create Back Pressure

Todo problema de rendimiento empieza con una cola acumulándose. Las colas no acotadas consumen toda la memoria y, por la ley de Little, hacen que el tiempo de respuesta tienda a infinito. Las colas deben ser finitas. Con una cola acotada llena hay pocas opciones, todas desagradables: fingir aceptar y descartar, aceptar y descartar otro ítem, rechazar el ítem, o bloquear al productor. Bloquear al productor es control de flujo: aplica “back pressure” aguas arriba hasta el cliente final (así hace TCP con su ventana). Funciona mejor con llamadas asíncronas (frameworks Rx, actores, channels) y solo dentro de un límite de sistema (el conjunto de consumidores debe ser finito). En los bordes, el back pressure produce hilos bloqueados que frustran al usuario, así que ahí se combina con shed load y llamadas asíncronas (aceptar en un pool, llamar a almacenamiento en otro, y responder 503 o encolar con 202). Cuando se activa, el monitoreo debe enterarse.

## Governor

La automatización no tiene juicio y, cuando se equivoca, lo hace muy rápido (el autoscaler de Reddit que apagó casi todas las instancias durante una migración de ZooKeeper; o el que arranca demasiadas instancias y dispara la factura). Usa automatización para lo repetitivo y las respuestas rápidas, y humanos para percibir la situación global. Inspirado en el regulador de las máquinas de vapor, un *governor* limita la velocidad de las acciones. Es *stateful*, consciente del tiempo y asimétrico: la mayoría de acciones tienen una dirección “segura” y otra “insegura” (apagar instancias, borrar datos, bloquear IPs son inseguras). Las fuerzas (disponibilidad vs. costo) definen una curva en U: una acción es segura dentro de un rango y el governor aplica resistencia creciente fuera de él. El objetivo es frenar lo suficiente para que un humano, avisado por el monitoreo, intervenga.

## El ejemplo que recorre el capítulo

El caso de la empresa de fotografía ilustra Fail Fast: la generación anterior del software de renderizado producía una imagen negra de píxeles en cero cuando faltaban perfiles de color, imágenes, fondos o máscaras alfa; esa imagen entraba a la imprenta, se imprimía y generaba reprocesos costosos. El nuevo renderizado verificaba al llegar el trabajo la presencia de cada fuente, imagen, fondo y máscara, y preasignaba memoria, reportando cualquier falla de inmediato antes de gastar minutos de cómputo; la tasa de reprocesos por software cayó a cero. El único recurso no preasignado fue el espacio en disco para la imagen final, a petición del cliente que confiaba en su “proceso de purga sólido” (en realidad un señor que borraba archivos a mano): menos de un año después los discos se llenaron, y justo el único punto donde rompieron Fail Fast fue donde el renderizado falló tras malgastar esfuerzo. El ejemplo conecta Fail Fast con Steady State.

## Ideas clave

- Las fallas son inevitables; adopta una mentalidad orientada a la recuperación y espera que todo acabe fuera de especificación. “Count of patterns applied” no es métrica de calidad.
- Pon timeouts en llamadas salientes y en todo pool que bloquee hilos; prefiere reintentos diferidos (encolar) a reintentos inmediatos.
- Circuit Breaker es el patrón fundamental ante problemas de integration points: closed/open/half-open, mide densidad de fallas (Leaky Bucket), vive por proceso y expone sus cambios de estado.
- Bulkheads particionan la capacidad (de thread pools a granjas de servidores) para preservar funcionalidad parcial; cruciales en servicios compartidos y microservicios.
- Steady State elimina el *fiddling*: para cada recurso que se acumula (datos, logs, caché) debe haber otro que lo recicle; corre un ciclo de despliegue sin intervención humana.
- Fail Fast reserva recursos y valida pronto para no malgastar trabajo; distingue falla de sistema de falla de aplicación. Let It Crash busca estabilidad de sistema vía reinicio rápido, granularidad acotada, supervisión y reintegración; nunca en monolitos.
- Handshaking y Test Harnesses permiten, respectivamente, controlar la demanda de forma cooperativa (health checks) y emular fallas fuera de especificación que la integración normal no provoca.
- Shed Load, Back Pressure y Governor gestionan carga y automatización: rechaza trabajo en los bordes, frena productores dentro del sistema con colas finitas, y aplica resistencia en la dirección insegura para dar tiempo a la intervención humana. La paranoia es buena ingeniería.
