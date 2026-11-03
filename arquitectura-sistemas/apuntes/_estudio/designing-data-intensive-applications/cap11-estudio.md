# Stream Processing (Procesamiento de flujos) — Estudio

## Tarjetas de repaso

P: ¿Qué es el stream processing frente al batch processing?
R: Es la contraparte incremental e ilimitada del batch: en lugar de operar sobre una entrada acotada y finita, procesa cada evento conforme ocurre sobre datos ilimitados (unbounded), reduciendo el retraso que introduce dividir los datos en bloques de duración fija.

P: ¿Qué es un evento en el contexto del streaming?
R: Un objeto pequeño, autocontenido e inmutable que describe algo que ocurrió en un instante, normalmente con marca de tiempo. Es generado una vez por un productor (publisher) y procesado por varios consumidores (subscribers); los eventos relacionados se agrupan en un topic o stream.

P: ¿Por qué el polling es ineficiente para notificar eventos con baja latencia?
R: Cuanto más a menudo se sondea, menor es el porcentaje de peticiones que devuelven eventos nuevos, lo que lo vuelve caro; es mejor notificar (push) a los consumidores con sistemas de mensajería.

P: ¿Qué tres opciones tiene un sistema de mensajería si los productores envían más rápido de lo que los consumidores procesan?
R: Descartar mensajes, encolarlos (buffer) o aplicar backpressure (control de flujo que bloquea al productor, como las tuberías Unix y TCP).

P: ¿Qué diferencia a un broker AMQP/JMS de uno basado en log?
R: El AMQP/JMS asigna mensajes individuales y los borra al confirmarlos (mentalidad transitoria, bueno como RPC asíncrono); el basado en log (Kafka, Kinesis, DistributedLog) asigna particiones enteras, mantiene el orden por offset, retiene los mensajes en disco y permite releerlos.

P: ¿Qué son los acknowledgments y qué efecto tiene combinarlos con load balancing?
R: El cliente avisa cuando termina de procesar y el broker elimina el mensaje; si no llega el ack, lo reentrega a otro consumidor. Combinarlo con load balancing provoca reordenación de mensajes, lo que importa si hay dependencias causales.

P: ¿Qué es el head-of-line blocking en un log particionado?
R: Un mensaje lento bloquea el procesamiento de los mensajes siguientes de su misma partición; por eso para procesamiento costoso mensaje a mensaje con orden poco importante conviene JMS/AMQP.

P: ¿Qué es Change Data Capture (CDC)?
R: Observar todos los cambios escritos en una base de datos y extraerlos como un flujo para replicarlos a otros sistemas; convierte la base de datos en líder y a índices o data warehouses en seguidores. Se implementa con triggers (frágiles) o parseando el log de replicación (más robusto).

P: ¿Qué es la compactación de log (log compaction)?
R: El motor conserva solo la última actualización por clave y descarta duplicados; un borrado se marca con un tombstone. Así el espacio depende del contenido actual, no del número total de escrituras, y un consumidor nuevo puede leer desde el offset 0 y obtener una copia completa.

P: ¿En qué se diferencia el event sourcing del CDC?
R: El event sourcing almacena eventos inmutables a nivel de aplicación ("el estudiante canceló su matrícula") y los eventos posteriores no sobreescriben a los previos, por lo que requiere el historial completo; un evento de CDC contiene la versión completa del registro y permite compactar.

P: ¿Qué diferencia hay entre un comando y un evento en event sourcing?
R: Una petición llega como comando, que puede fallar al validar una condición de integridad (validación síncrona); si se acepta, se convierte en un evento durable e inmutable que ya nadie puede rechazar.

P: ¿Qué es CQRS?
R: Command Query Responsibility Segregation: separar el estado mutable del log inmutable para derivar varias vistas de lectura del mismo log, permitiendo desnormalizar y dejar de escribir los datos en la misma forma en que se consultan.

P: ¿Cuál es la diferencia entre event time y processing time?
R: Event time es cuándo ocurrió el evento (según su timestamp); processing time es cuándo se procesa (según el reloj de la máquina). Usar processing time falla con retrasos: tras reiniciar un procesador con backlog aparece un falso pico de peticiones.

P: ¿Cuáles son los tres tipos de join sobre flujos?
R: Stream-stream (window join, relaciona eventos de dos flujos dentro de una ventana), stream-table (enriquecimiento con un changelog local mantenido vía CDC) y table-table (mantiene una vista materializada uniendo dos changelogs).

P: ¿Cómo se logra semántica exactly-once en streaming?
R: Descartando la salida parcial de tareas fallidas mediante microbatching (Spark Streaming), checkpointing con barriers (Flink), commit atómico para efectos externos o escrituras idempotentes (detectando duplicados con metadatos como el offset de Kafka).

## Preguntas de autoevaluación

P: ¿Qué dos preguntas conviene hacerse para diferenciar sistemas de mensajería, y por qué importan?
R: (1) Qué pasa si los productores envían más rápido de lo que los consumidores procesan (descartar, encolar o backpressure) y (2) qué pasa si los nodos caen o se desconectan (si se pierden mensajes). La durabilidad requiere disco o replicación con coste; que la pérdida sea aceptable depende de la aplicación (ver "Sistemas de mensajería").

P: ¿Por qué un log basado en broker permite reproducir (replay) mensajes antiguos y qué lo acerca al batch?
R: Consumir es de solo lectura (solo avanza el offset), así que se puede arrancar un consumidor con el offset de ayer y reprocesar cuantas veces se quiera, separando los datos derivados de los de entrada mediante una transformación repetible, como en batch (ver "Logs particionados").

P: ¿Qué problemas tienen los dual writes y qué solución ideal propone el capítulo?
R: Condiciones de carrera (dos clientes concurrentes dejan base de datos e índice permanentemente inconsistentes sin error) y fallos parciales (una escritura tiene éxito y otra no). Lo ideal sería un único líder del que los demás sistemas fueran seguidores, lo que logra el CDC (ver "Bases de datos y flujos" y "Change Data Capture").

P: Según Pat Helland, ¿qué relación hay entre el estado y el log de eventos?
R: Son dos caras de la misma moneda: el estado es el resultado de los eventos que lo mutaron y el changelog representa su evolución. "The truth is the log. The database is a cache of a subset of the log" (PDF p. 482) (ver "Event sourcing e inmutabilidad").

P: ¿Por qué nunca se sabe con certeza cuándo se han recibido todos los eventos de una ventana y cómo se manejan los rezagados?
R: Porque los retrasos y la red desordenan los mensajes, así que siempre pueden llegar eventos rezagados (stragglers) tarde. Se manejan ignorándolos (midiendo cuántos se descartan) o publicando una corrección (ver "Razonar sobre el tiempo").

P: ¿Qué es una slowly changing dimension (SCD) y cómo se resuelve?
R: Es el problema de que el estado con el que se une un join cambie con el tiempo (p. ej., una tarifa de impuestos); al reprocesar datos históricos suele quererse la versión vigente en el momento de la venta. Se resuelve con un identificador por versión del registro, aunque entonces no se puede compactar el log (ver "Joins sobre flujos").

P: ¿Por qué la tolerancia a fallos en streaming no puede funcionar como en batch, y qué técnicas la sustituyen?
R: En batch se reinicia la tarea y se descarta su salida, pero en streaming el flujo nunca termina y no se puede esperar a acabar un trabajo que lleva años. Se usan microbatching, checkpointing, commit atómico para efectos externos e idempotencia (ver "Tolerancia a fallos").

P: ¿Qué es complex event processing (CEP) y cómo invierte la relación habitual entre consulta y datos?
R: Busca patrones de eventos con un lenguaje declarativo tipo SQL; invierte la relación porque las consultas son permanentes y los eventos pasan ante ellas, al contrario que en una base de datos tradicional (ver "Procesamiento de flujos").

## Puntos a dominar

- Distinguir datos acotados (batch) de ilimitados (unbounded) y por qué el streaming reduce el retraso procesando cada evento al ocurrir.
- Comparar mensajería directa (UDP multicast, ZeroMQ, StatsD, webhooks) con message brokers, y los patrones load balancing frente a fan-out.
- Diferenciar brokers AMQP/JMS de brokers basados en log: borrado tras entrega frente a retención en disco, acks individuales frente a consumer offsets, head-of-line blocking y replay.
- Entender el log particionado: solo-append, offset monótono por partición, orden total dentro de la partición pero no entre particiones, segmentos y buffer circular acotado.
- Relacionar bases de datos y flujos: el log de replicación como flujo de eventos, replicación de máquina de estados y los peligros de los dual writes.
- Diferenciar CDC (cambios de bajo nivel, compactable) de event sourcing (eventos de dominio inmutables que requieren el historial), más comandos frente a eventos y CQRS.
- Separar event time de processing time, manejar stragglers y clasificar ventanas tumbling, hopping, sliding y de sesión.
- Clasificar los tres joins sobre flujos (stream-stream, stream-table, table-table) y entender su dependencia del tiempo (SCD).
- Conocer las técnicas de tolerancia a fallos y semántica exactly-once (effectively-once): microbatching, checkpointing con barriers, commit atómico, idempotencia y reconstrucción de estado.
