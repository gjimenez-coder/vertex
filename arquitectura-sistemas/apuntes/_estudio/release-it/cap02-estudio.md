# Caso de estudio: la excepción que dejó en tierra a una aerolínea — Estudio

## Tarjetas de repaso

P: ¿Qué sistema es el hilo conductor del capítulo y qué hacía?
R: Core Facilities (CF), un servicio de búsqueda de vuelos de primera generación dentro de una migración a SOA; recibía fecha, hora, ciudad, código de aeropuerto o número de vuelo y devolvía detalles de vuelos.

P: ¿Cuál fue la causa raíz del incidente?
R: Un único `SQLException` no capturado en una sola línea de código, que provocó un efecto dominó que tumbó sistemas enteros.

P: ¿Por qué `java.sql.Statement.close()` puede causar problemas?
R: Puede lanzar `SQLException`; el driver de Oracle lo hace al encontrar un `IOException` al cerrar la conexión (por ejemplo tras un failover de base de datos).

P: Si falla el cierre del statement en el bloque `finally`, ¿qué ocurre con la conexión?
R: La conexión no se cierra: se fuga del resource pool. Tras 40 llamadas el pool se agota y toda llamada futura se bloquea en `connectionPool.getConnection()`.

P: ¿Qué pasó con las conexiones TCP tras el failover de base de datos?
R: La IP virtual se movió de host pero el estado de las conexiones TCP existentes no se transfiere; cualquier escritura por el socket termina lanzando `IOException`.

P: ¿Por qué se considera peligroso RMI según el capítulo?
R: Porque sus llamadas no pueden hacer timeout, dejando al llamador vulnerable a problemas del servidor remoto.

P: ¿Qué es un thread dump y qué revela?
R: Un "libro abierto" del proceso: muestra librerías de terceros, pools de hilos, cuántos hilos hay en cada uno, procesamiento en background y protocolos usados.

P: ¿Cómo se obtiene un thread dump en Java?
R: Enviando `SIGQUIT` (signal 3) en UNIX o `Ctrl+Break` en Windows, o con `jcmd <pid> Thread.print`.

P: ¿Por qué el monitoreo no detectó el problema en CF?
R: Porque solo golpeaba una página de estado (por HTTP), que no reflejaba la salud real de los servidores; además los pools de hilos EJB y HTTP estaban separados.

P: ¿Cómo estaban bloqueados los hilos en los kioscos y en CF?
R: En los kioscos, los 40 hilos estaban bloqueados en `SocketInputStream.socketRead0()` dentro de `FlightSearch.lookupByCity()`; en CF, todos los hilos EJB estaban bloqueados intentando sacar una conexión del resource pool.

P: ¿Qué componente controlaba el failover de la base de datos y qué hacía?
R: Veritas Cluster Server: apagaba Oracle en un nodo, desmontaba los filesystems del RAID, los remontaba en el otro, arrancaba Oracle y reasignaba la IP virtual.

P: ¿Cuál es la lección final del capítulo sobre los bugs?
R: Los bugs no se pueden eliminar, se deben sobrevivir; lo crítico es impedir que el fallo de un sistema se propague por la malla de sistemas interconectados.

## Preguntas de autoevaluación

P: ¿Por qué la redundancia de hardware impecable de CF no evitó la caída?
R: Porque el fallo era de software (un `SQLException` no capturado) y ninguna redundancia física podía evitarlo; CF no tenía single points of failure físicos y aun así cayó. (Sección "La arquitectura de alta disponibilidad" / "¿Una onza de prevención?")

P: En el postmortem, ¿por qué el failover era el primer sospechoso?
R: Por el principio "post hoc, ergo propter hoc" — "lo tocaste de último" —, un buen punto de partida en operaciones; además el failover se había hecho tres horas antes de la caída. (Sección "Postmortem y caza de pistas")

P: ¿Cuál es la primera prioridad cuando se produce la caída y cómo se concilia con la investigación?
R: Restaurar el servicio es la primera prioridad, por encima de investigar; tener scripts de recolección automatizada (thread dumps, snapshots) permite obtener evidencia sin improvisar ni alargar la caída. (Sección "La caída (The Outage)")

P: ¿Por qué la coincidencia de kioscos e IVR cayendo casi a la vez apuntaba a CF?
R: Porque ambos compartían una única dependencia común, CF, el único sistema compartido; el failover reciente lo hacía aún más sospechoso. (Sección "La caída (The Outage)")

P: ¿Habría atrapado una revisión de código el fallo?
R: Solo si un revisor conocía las entrañas del driver JDBC de Oracle o dedicaba horas por método; en la práctica era muy difícil de detectar así. (Sección "¿Una onza de prevención?")

P: ¿Por qué el autor tuvo que decompilar los binarios?
R: Porque en producción solo había binarios, sin acceso al código fuente; así encontró el fallo en el EJB `FlightSearch.lookupByCity()`. (Sección "El smoking gun")

P: Según el capítulo, ¿cuál es la pregunta correcta de diseño que se deriva del incidente?
R: No cómo evitar el bug, sino cómo evitar que el bug de un sistema afecte a todo lo demás; el peor problema fue la propagación. (Sección "¿Una onza de prevención?")

## Puntos a dominar

- Entender que un error minúsculo (un `SQLException` no capturado) puede escalar hasta un desastre a escala de toda una aerolínea.
- Saber por qué `java.sql.Statement.close()` puede lanzar `SQLException` y cómo manejarlo para no fugar conexiones del pool.
- Explicar el mecanismo de agotamiento del pool: statements inutilizables tras un failover, cierre fallido, conexión no liberada, bloqueo en `getConnection()`.
- Reconocer el riesgo de RMI por la imposibilidad de hacer timeout en sus llamadas.
- Interpretar thread dumps para localizar hilos bloqueados y saber obtenerlos (`SIGQUIT`, `Ctrl+Break`, `jcmd <pid> Thread.print`).
- Distinguir monitoreo real de salud frente a un simple check de página de estado que da falsa tranquilidad.
- Priorizar la restauración del servicio sobre la investigación, apoyándose en scripts de recolección automatizada.
- Asumir que los bugs se sobreviven, no se eliminan, y que el objetivo de diseño es frenar la propagación de fallos entre sistemas interconectados.
