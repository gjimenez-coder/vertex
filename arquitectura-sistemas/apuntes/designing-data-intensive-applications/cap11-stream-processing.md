# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 11 — Stream Processing (Procesamiento de flujos)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF como (PDF p. N).

## Lo que necesitas saber

El capítulo 10 trataba el procesamiento por lotes (batch) sobre una entrada acotada y finita. Pero gran parte de los datos reales son ilimitados (unbounded): llegan gradualmente y el conjunto nunca está "completo". Los procesos batch dividen artificialmente los datos en bloques de duración fija (un día, una hora), lo que introduce retraso. Reducir ese retraso procesando cada evento conforme ocurre es la idea del procesamiento de flujos (stream processing): la contraparte incremental e ilimitada del batch.

Un stream es cualquier dato puesto a disposición de forma incremental en el tiempo (stdin/stdout de Unix, listas perezosas, conexiones TCP, audio/vídeo). Aquí se estudian los event streams como mecanismo de gestión de datos. El capítulo recorre tres bloques: cómo se transmiten los flujos (mensajería y logs), la relación entre bases de datos y flujos (CDC, event sourcing, inmutabilidad), y cómo procesar los flujos (CEP, analítica, joins, tolerancia a fallos).

Sales sabiendo distinguir los brokers estilo AMQP/JMS de los brokers basados en log (Kafka, Kinesis), entender que una base de datos puede verse como un flujo de cambios, y conocer las dificultades propias del tiempo (event time vs processing time), los tres tipos de join sobre flujos y las técnicas para lograr semántica "exactly-once".

## Transmisión de flujos de eventos

En batch la entrada/salida son ficheros; el equivalente en streaming es el evento: un objeto pequeño, autocontenido e inmutable que describe algo que ocurrió en un instante, normalmente con marca de tiempo. Un evento es generado una vez por un productor (publisher) y procesado por varios consumidores (subscribers). Los eventos relacionados se agrupan en un topic o stream.

Un fichero o base de datos bastaría para conectar productores y consumidores por sondeo (polling), pero el polling se vuelve caro cuando se busca baja latencia: cuanto más a menudo se sondea, menor es el porcentaje de peticiones con eventos nuevos. Es mejor notificar a los consumidores. Los triggers de las bases de datos relacionales son limitados, por lo que se han desarrollado herramientas específicas: los sistemas de mensajería.

### Sistemas de mensajería

Un sistema de mensajería empuja (push) el evento a los consumidores y, a diferencia de una tubería Unix o TCP (uno a uno), permite varios productores y varios consumidores sobre un mismo topic. Para diferenciarlos conviene preguntar dos cosas:

1. ¿Qué pasa si los productores envían más rápido de lo que los consumidores procesan? Tres opciones: descartar mensajes, encolarlos (buffer) o aplicar backpressure (control de flujo, bloqueando al productor; así actúan las tuberías Unix y TCP).
2. ¿Qué pasa si los nodos caen o se desconectan? ¿Se pierden mensajes? La durabilidad requiere escritura en disco y/o replicación, con un coste. Si se puede tolerar pérdida ocasional, se gana rendimiento y latencia.

Que la pérdida sea aceptable depende de la aplicación: para métricas periódicas un dato perdido suele dar igual, pero para contar eventos cada mensaje perdido corrompe el contador.

### Mensajería directa y brokers de mensajes

Algunos sistemas comunican productores y consumidores directamente: UDP multicast (usado en finanzas por su baja latencia), librerías sin broker como ZeroMQ y nanomsg, agregadores de métricas como StatsD y Brubeck (UDP no fiable), o peticiones HTTP/RPC directas, base de los webhooks. Todos exigen que la aplicación asuma posible pérdida de mensajes y suelen suponer que productores y consumidores están siempre en línea.

La alternativa extendida es el message broker (o cola de mensajes): una especie de base de datos optimizada para flujos de mensajes, a la que productores y consumidores se conectan como clientes. Al centralizar los datos, el broker tolera clientes que van y vienen y asume la durabilidad. Los consumidores son generalmente asíncronos: el productor solo espera a que el broker confirme que almacenó el mensaje, no a que se procese.

Diferencias frente a una base de datos: los brokers suelen borrar el mensaje tras entregarlo (no sirven para almacenamiento a largo plazo), asumen colas cortas, permiten suscribirse a subconjuntos de topics, y notifican cuando hay datos nuevos en lugar de responder a consultas arbitrarias. Este es el modelo tradicional, plasmado en estándares como JMS y AMQP, e implementado en RabbitMQ, ActiveMQ, HornetQ, Qpid, TIBCO EMS, IBM MQ, Azure Service Bus y Google Cloud Pub/Sub.

Con múltiples consumidores en un mismo topic hay dos patrones: load balancing (cada mensaje va a uno de los consumidores, para repartir trabajo costoso) y fan-out (cada mensaje va a todos los consumidores). Pueden combinarse.

Para no perder mensajes si un consumidor cae a medio procesar, los brokers usan acknowledgments: el cliente avisa cuando termina y entonces el broker elimina el mensaje; si no llega el ack, lo reentrega a otro consumidor. Combinar load balancing con reentrega provoca reordenación de mensajes (un mensaje no confirmado se reentrega después de otros ya procesados), lo que importa si hay dependencias causales.

## Logs particionados

Los brokers AMQP/JMS tienen mentalidad "transitoria": reciben y borran. Ficheros y bases de datos, en cambio, guardan de forma permanente. ¿Se puede combinar el almacenamiento durable con la notificación de baja latencia? Esa es la idea de los brokers basados en log.

Un log es una secuencia de registros en disco, solo-append. El productor añade mensajes al final; el consumidor los lee secuencialmente y, al llegar al final, espera notificación (como `tail -f`). Para escalar, el log se particiona entre máquinas: un topic es un grupo de particiones. Dentro de cada partición el broker asigna un número de secuencia monótono (offset) y los mensajes quedan totalmente ordenados; no hay garantía de orden entre particiones. Apache Kafka, Amazon Kinesis Streams y Twitter DistributedLog funcionan así, logrando millones de mensajes por segundo mediante particionado y replicación.

Comparado con la mensajería tradicional, el log soporta fan-out trivialmente (leer no borra) y hace load balancing asignando particiones enteras a nodos del grupo de consumidores. Inconvenientes: el número de nodos que comparten un topic está limitado por el número de particiones, y un mensaje lento bloquea los siguientes de su partición (head-of-line blocking). Por eso, para procesamiento costoso mensaje a mensaje y orden poco importante, conviene JMS/AMQP; para alto rendimiento con orden importante, el log.

Consumer offsets: como la partición se lee en orden, basta con que el broker registre periódicamente el offset de cada consumidor, sin seguir cada ack individual (menos sobrecarga, más throughput). Es análogo al log sequence number de la replicación con un solo líder: el broker es el líder y el consumidor el seguidor. Si un consumidor falla, otro retoma desde el último offset registrado, lo que puede reprocesar algunos mensajes.

Uso del disco: para no agotarlo, el log se divide en segmentos y los antiguos se borran o archivan; funciona como un buffer circular de tamaño acotado pero grande (un disco de 6 TB a 150 MB/s guarda ~11 horas al ritmo máximo; en la práctica, días o semanas). El throughput es casi constante, a diferencia de los sistemas que solo escriben a disco cuando la cola crece.

Si un consumidor se retrasa más allá del buffer, pierde mensajes, pero solo él se ve afectado: no perturba a otros consumidores, lo que permite consumir un log de producción para pruebas o depuración. Y como consumir es de solo lectura (solo avanza el offset), se pueden reproducir (replay) mensajes antiguos: arrancar un consumidor con el offset de ayer y reprocesar, cuantas veces se quiera. Esto acerca la mensajería basada en log al batch, separando los datos derivados de los de entrada mediante una transformación repetible.

## Bases de datos y flujos

Una escritura en una base de datos también es un evento que puede capturarse y procesarse. De hecho, un log de replicación es un flujo de eventos de escritura; el principio de replicación de máquina de estados dice que, si cada réplica procesa los mismos eventos en el mismo orden (de forma determinista), todas acaban en el mismo estado.

Mantener sistemas sincronizados: ninguna tecnología cubre todas las necesidades, así que las aplicaciones combinan OLTP, caché, índice full-text y data warehouse, cada uno con su copia de los datos que debe mantenerse en sync. Los dual writes (que la aplicación escriba en cada sistema) tienen problemas graves: condiciones de carrera (dos clientes concurrentes dejan la base de datos y el índice permanentemente inconsistentes sin que salte ningún error) y fallos parciales (una escritura tiene éxito y otra no). Lo ideal sería un único líder del que los demás sistemas fueran seguidores.

### Change Data Capture (CDC)

CDC es observar todos los cambios escritos en una base de datos y extraerlos como un flujo para replicarlos a otros sistemas. Convierte una base de datos en líder y a los demás (índice de búsqueda, data warehouse) en seguidores; un broker basado en log es idóneo para transportar esos cambios porque conserva el orden. Se puede implementar con triggers (frágiles y costosos) o parseando el log de replicación (más robusto, pero hay que manejar cambios de esquema). Ejemplos: Databus (LinkedIn), Wormhole (Facebook), Sherpa (Yahoo!), Bottled Water para PostgreSQL, Maxwell y Debezium para MySQL, Mongoriver, GoldenGate para Oracle. Es asíncrono, con las consecuencias del retraso de replicación.

Para no guardar todos los cambios para siempre: se parte de un snapshot inicial que corresponde a un offset conocido del changelog. Una alternativa es la compactación de log (log compaction): el motor conserva solo la última actualización por clave y descarta los duplicados; un borrado se marca con un tombstone. Así el espacio depende solo del contenido actual, no del número total de escrituras. Con esto, un consumidor nuevo puede leer desde el offset 0 y obtener una copia completa de la base de datos sin otro snapshot (soportado por Kafka). Cada vez más bases de datos ofrecen change streams como interfaz de primera clase (RethinkDB, Firebase, CouchDB, Meteor con el oplog de MongoDB, VoltDB); Kafka Connect integra CDC de muchos sistemas con Kafka.

### Event sourcing e inmutabilidad

El event sourcing, surgido del diseño guiado por el dominio (DDD), también almacena todos los cambios como un log de eventos, pero a un nivel de abstracción distinto al de CDC: la aplicación se construye sobre eventos inmutables que reflejan acciones a nivel de aplicación ("el estudiante canceló su matrícula"), no cambios de bajo nivel en registros. El almacén es solo-append y se desaconsejan updates/deletes. Esto facilita evolucionar la aplicación, depurar y auditar.

El event sourcing distingue comandos de eventos: una petición llega como comando que puede fallar (validación de una condición de integridad); si se acepta, se convierte en un evento durable e inmutable que ya nadie puede rechazar. La validación debe ser síncrona, antes de generar el evento (por ejemplo, con una transacción serializable, o dividiendo la reserva en evento tentativo y confirmación posterior).

Un log de eventos por sí solo no basta: los usuarios quieren el estado actual, no el historial. Las aplicaciones derivan ese estado reproduciendo el log con una transformación determinista, y suelen guardar snapshots como optimización. A diferencia de CDC, un evento de CDC contiene la versión completa del registro (permite compactar), mientras que en event sourcing los eventos posteriores no sobreescriben a los previos, así que se necesita el historial completo.

Estado y log de eventos no se contradicen: son dos caras de la misma moneda. El estado es el resultado de los eventos que lo mutaron; el changelog representa la evolución del estado. Como lo expresa Pat Helland, "The truth is the log. The database is a cache of a subset of the log" (PDF p. 482). La inmutabilidad es una idea antigua (la contabilidad usa libros solo-append durante siglos: un error no se borra, se compensa con otra transacción). Ventajas: auditoría, recuperación frente a código defectuoso que escribió datos erróneos, y captura de más información de la que recoge el estado actual.

Separar el estado mutable del log inmutable permite derivar varias vistas de lectura del mismo log (Druid, Pistachio, Kafka Connect), idea conocida como CQRS (command query responsibility segregation). Así deja de ser necesario escribir los datos en la misma forma en que se consultan, y es razonable desnormalizar en las vistas de lectura. El inconveniente: los consumidores son asíncronos, de modo que un usuario podría no ver de inmediato su propia escritura (problema de "leer tus propias escrituras"). Limitaciones de la inmutabilidad: con mucha rotación (updates/deletes), el historial puede crecer demasiado; y a veces hay que borrar datos de verdad por motivos legales o de privacidad (Datomic lo llama excision; Fossil, shunning), algo sorprendentemente difícil porque quedan copias en muchos sitios.

## Procesamiento de flujos

Con un flujo se puede: (1) escribirlo a una base de datos, caché o índice para consultarlo; (2) enviarlo a personas (alertas, notificaciones, dashboards); o (3) procesar flujos de entrada para producir flujos derivados. El código que hace esto es un operador o job, similar a los procesos Unix y MapReduce. La diferencia crucial es que un flujo nunca termina: no sirve ordenar (ni los sort-merge joins), y la tolerancia a fallos no puede basarse en reiniciar desde el principio un trabajo que lleva años.

Usos: monitorización (detección de fraude, trading, fábricas, inteligencia militar); complex event processing (CEP), que busca patrones de eventos con un lenguaje declarativo tipo SQL invirtiendo la relación consulta/datos (las consultas son permanentes y los eventos pasan ante ellas); stream analytics, orientado a agregaciones y métricas estadísticas sobre ventanas de tiempo, a veces con algoritmos probabilísticos (Bloom filters, HyperLogLog); mantenimiento de vistas materializadas (caché, índices) que requieren una ventana que llega hasta el principio del tiempo; búsqueda sobre flujos (percolator de Elasticsearch), donde las consultas se guardan y los documentos pasan ante ellas; y la frontera con mensajería y RPC (el modelo de actores no se considera stream processing: comunicación efímera uno-a-uno frente a logs durables multisubscriptor).

### Razonar sobre el tiempo

Las ventanas ("la media de los últimos cinco minutos") son engañosas. Hay que distinguir event time (cuándo ocurrió, según el timestamp del evento) de processing time (cuándo se procesa, según el reloj de la máquina). Usar el processing time es simple pero falla con retrasos de procesamiento: tras reiniciar un procesador que acumuló un backlog, parece haber un pico de peticiones cuando el ritmo real fue estable. Los retrasos y la red también desordenan los mensajes (analogía de las películas de Star Wars: el orden de estreno no coincide con el narrativo).

Nunca se sabe con certeza cuándo se han recibido todos los eventos de una ventana: hay que manejar eventos rezagados (stragglers) que llegan tarde, ya sea ignorándolos (midiendo cuántos se descartan) o publicando una corrección. Asignar timestamps es difícil si los eventos se almacenan en el dispositivo (una app móvil offline); una solución es registrar tres timestamps (ocurrido, enviado y recibido) para estimar el desfase del reloj del dispositivo.

Tipos de ventana: tumbling (longitud fija, cada evento en una sola ventana), hopping (longitud fija con solapamiento para suavizar), sliding (todos los eventos dentro de un intervalo entre sí) y session (sin duración fija, agrupa eventos del mismo usuario próximos en el tiempo, termina tras un periodo de inactividad).

### Joins sobre flujos

Hay tres tipos. El stream-stream join (window join) relaciona eventos de dos flujos de actividad dentro de una ventana de tiempo (p. ej., búsqueda y clic con el mismo session ID para calcular el click-through rate); el procesador mantiene estado con los eventos recientes indexados. El stream-table join (enriquecimiento) une un flujo de actividad con una base de datos (añadir el perfil del usuario a cada evento); en vez de consultar una base de datos remota lenta, se carga una copia local que se mantiene al día vía CDC, con una ventana que llega "al principio del tiempo". El table-table join mantiene una vista materializada (la timeline de Twitter): ambos flujos son changelogs y cada cambio se une con el estado actual del otro lado.

Los joins dependen del tiempo: si cambia el estado con el que se une (p. ej., una tarifa de impuestos), hay que decidir qué versión usar; al reprocesar datos históricos suele quererse la tarifa vigente en el momento de la venta. En data warehouses esto es una slowly changing dimension (SCD), que se resuelve con un identificador por versión del registro, aunque entonces no se puede compactar el log.

### Tolerancia a fallos

En batch, un fallo se tolera reiniciando la tarea y descartando su salida, logrando semántica exactly-once (más propiamente, effectively-once). En streaming no se puede esperar a terminar. Soluciones:

- Microbatching (Spark Streaming): trocear el flujo en mini-lotes de ~1 s.
- Checkpointing (Apache Flink): generar puntos de control periódicos del estado en almacenamiento durable, disparados por barriers, y reiniciar desde el último.
- Ambos dan exactly-once dentro del framework, pero no cuando la salida sale de él (escrituras externas, emails). Para eso hace falta commit atómico: todos los efectos ocurren si y solo si el procesamiento tiene éxito (usado en Google Cloud Dataflow y VoltDB).
- Idempotencia: una operación que puede repetirse con el mismo efecto (fijar una clave a un valor es idempotente; incrementar un contador no). Añadiendo metadatos (p. ej., el offset de Kafka) se detecta si una actualización ya se aplicó. Requiere replay determinista en el mismo orden y evitar actualizaciones concurrentes (puede necesitar fencing).

Reconstruir el estado tras un fallo: mantenerlo en un almacén remoto replicado (lento por consulta), o local y replicado periódicamente (Flink hace snapshots a HDFS; Samza y Kafka Streams replican los cambios a un topic de Kafka con compactación); a veces el estado se reconstruye reproduciendo los flujos de entrada. No hay un equilibrio universalmente óptimo: depende de la infraestructura.

## Ideas clave

- El stream processing es el batch aplicado de forma continua a datos ilimitados; brokers y logs de eventos son el equivalente streaming de un sistema de ficheros.
- Dos familias de broker: AMQP/JMS (asigna mensajes individuales, los borra al confirmar; bueno como RPC asíncrono) y basado en log (asigna particiones enteras, mantiene el orden, retiene en disco y permite releer).
- Una escritura en una base de datos puede verse como un evento; el changelog se captura implícitamente con CDC o explícitamente con event sourcing, y la compactación de log permite retener una copia completa.
- Representar bases de datos como flujos permite mantener al día sistemas derivados (índices, cachés, analítica) y construir nuevas vistas reproduciendo el log desde el principio.
- Hay que separar event time de processing time y manejar eventos rezagados; existen ventanas tumbling, hopping, sliding y de sesión.
- Tres joins sobre flujos: stream-stream (dentro de una ventana), stream-table (enriquecimiento con un changelog) y table-table (mantenimiento de una vista materializada).
- La semántica exactly-once (effectively-once) se consigue descartando la salida parcial de tareas fallidas mediante microbatching, checkpointing, commit atómico o escrituras idempotentes.
- Estado mutable y log inmutable de eventos son dos caras de la misma moneda: "la verdad es el log" y la base de datos es una caché del mismo.
