# The Future of Data Systems (El futuro de los sistemas de datos) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre las aplicaciones de datos?
R: No existe una única herramienta para todos los casos de uso; las aplicaciones componen varias piezas de software y el reto principal es la integración de datos.

P: ¿Qué es un sistema de registro (system of record) en el enfoque de dataflow?
R: El sistema donde se escribe primero y que decide un orden total de escrituras; el resto de representaciones se derivan de él mediante transformaciones asíncronas y débilmente acopladas sobre un log de eventos ordenado.

P: ¿Qué es change data capture (CDC)?
R: Escribir primero en la base de datos de registro y capturar sus cambios para aplicarlos en el mismo orden a otros sistemas derivados (por ejemplo, un índice).

P: ¿Qué diferencia clave hay entre transacciones distribuidas y datos derivados basados en log?
R: Las transacciones ordenan con bloqueos (2PL) y commit atómico y suelen ofrecer linealizabilidad; CDC y event sourcing ordenan con un log y se basan en reintento determinista e idempotencia, actualizándose de forma asíncrona.

P: ¿Por qué decidir un orden total de escrituras es difícil de escalar?
R: Formalmente equivale a total order broadcast (consenso); al particionar por throughput, usar varios datacenters, microservicios sin estado compartido o clientes offline, el orden entre esas unidades queda indefinido o ambiguo.

P: ¿Cuál es la diferencia fundamental entre stream y batch processing?
R: El stream opera sobre datasets ilimitados y el batch sobre entradas de tamaño finito conocido, aunque la distinción se difumina (microbatches en Spark, batch sobre motor de streaming en Flink).

P: ¿Qué propone la arquitectura lambda y qué problemas prácticos tiene?
R: Derivar vistas en paralelo con un sistema batch (versión exacta) y uno stream (aproximación rápida) sobre eventos inmutables; problemas: mantener lógica duplicada en dos frameworks, fusionar salidas y el coste de reprocesar todo.

P: ¿Qué distingue una base de datos federada (polystore) de una desagregada (unbundled)?
R: La federada unifica lecturas con una interfaz de consulta común (tradición relacional); la desagregada unifica escrituras sincronizando cambios entre sistemas dispares con CDC y logs de eventos (tradición Unix).

P: ¿Qué significa diseñar aplicaciones "database inside-out" o en torno al dataflow?
R: Un patrón de diseño en el que el código responde a cambios de estado en un lugar provocando cambios en otro, de modo que índices, caches y agregaciones se actualicen automáticamente con tolerancia a fallos, escala y durabilidad.

P: ¿Qué son el write path y el read path, y dónde se encuentran?
R: El write path precomputa de forma eager al escribir; el read path construye la respuesta de forma lazy al leer. Se encuentran en el dataset derivado, que es un compromiso entre trabajo en escritura y en lectura.

P: ¿En qué consiste el argumento end-to-end aplicado a la corrección?
R: Ciertas funciones (como la supresión de duplicados exactamente-una-vez) solo se implementan completamente con el conocimiento de los extremos; p. ej. un identificador de operación generado por el cliente y una restricción de unicidad sobre request_id.

P: ¿Cómo se logra la ejecución exactamente-una-vez para evitar corrupción?
R: Haciendo la operación idempotente, lo que exige metadatos (IDs de operación) y fencing al hacer failover; TCP, las transacciones o los stream processors por sí solos no bastan.

P: ¿Qué diferencia hay entre puntualidad (timeliness) e integridad?
R: La puntualidad asegura ver el estado actualizado y su violación (consistencia eventual) es temporal y resoluble esperando; la integridad es ausencia de corrupción y su violación es "inconsistencia perpetua" que requiere comprobación y reparación explícitas.

P: ¿Qué son los sistemas que evitan coordinación (coordination-avoiding)?
R: Sistemas que mantienen integridad sin commit atómico ni coordinación síncrona, pudiendo operar multi-datacenter en multi-leader; introducen coordinación síncrona solo donde es imprescindible.

P: ¿Qué significa "trust, but verify" en sistemas de datos?
R: Asumir que la corrupción es inevitable a la larga (bit-flips, rowhammer, bugs) y auditar continuamente la integridad comparando réplicas, restaurando backups y rederivando datos para verificar.

## Preguntas de autoevaluación

P: ¿Por qué considera Kleppmann que los datos derivados basados en log son más prometedores que las transacciones distribuidas para integrar sistemas?
R: Porque XA tiene mala tolerancia a fallos y rendimiento, y no existe un buen protocolo de transacciones distribuidas ampliamente soportado; el log con consumidores idempotentes es más simple y robusto. (Integración de datos)

P: ¿Cómo ilustra el ejemplo del cambio de ancho de vía ferroviario la evolución de una aplicación?
R: Muestra una migración gradual mediante un tercer raíl (vía mixta) donde conviven ambos anchos; análogamente, las vistas derivadas permiten mantener esquema antiguo y nuevo en paralelo, migrar usuarios poco a poco y revertir si algo falla. (Procesamiento batch y de streams)

P: ¿Qué diferencia el enfoque de dataflow del de microservicios en el ejemplo de conversión de divisa?
R: En microservicios el código consulta de forma síncrona un servicio de tipos de cambio; en dataflow se suscribe de antemano a un stream de actualizaciones y guarda el tipo en una base local, consultándolo localmente (un stream-table join dependiente del tiempo), más rápido y robusto. (Diseñar aplicaciones en torno al dataflow)

P: ¿Por qué un índice full-text ilustra que caches, índices y vistas materializadas solo desplazan una frontera?
R: Sin índice, leer implica escanear como grep (poco trabajo al escribir, mucho al leer) y precomputar todas las consultas es imposible; una cache de las consultas comunes desplaza la frontera entre read path y write path sin eliminar el compromiso. (Observar estado derivado)

P: ¿Por qué no basta con transacciones serializables para garantizar que no haya pérdida ni corrupción de datos?
R: Porque un bug de la aplicación puede escribir o borrar datos mal, y la supresión de duplicados de TCP solo vale dentro de una conexión; si el cliente reintenta tras un timeout la operación puede ejecutarse dos veces. La solución es end-to-end. (Buscar la corrección)

P: ¿Por qué en la mayoría de aplicaciones la integridad importa más que la puntualidad?
R: Porque un retraso temporal (como un extracto bancario) es tolerable y resoluble esperando, mientras que la corrupción (saldos que no cuadran) es "inconsistencia perpetua" catastrófica que exige reparación explícita. (Buscar la corrección)

P: ¿Cómo logra corrección una transferencia que toca tres particiones sin usar commit atómico?
R: Registrando la petición como un único mensaje atómico del que se derivan instrucciones de débito y crédito, deduplicando por request ID; aunque el procesador reintente tras un fallo, al ser determinista produce las mismas instrucciones. (Buscar la corrección)

P: ¿Qué riesgos éticos plantea Kleppmann sobre la analítica predictiva y el rastreo?
R: La "prisión algorítmica" sin apelación, el sesgo que el sistema aprende y amplifica del pasado discriminatorio, los bucles de retroalimentación (cámaras de eco) y la deriva del rastreo conductual hacia la vigilancia, con consentimiento no significativo y datos como "activo tóxico". (Hacer lo correcto)

## Puntos a dominar

- Explicar por qué no hay una herramienta universal y por qué la integración de datos es el reto central.
- Distinguir CDC y event sourcing de las transacciones distribuidas, incluyendo qué garantizan y a qué renuncian (linealizabilidad vs. actualización asíncrona).
- Entender que decidir un orden total es total order broadcast equivalente a consenso, y por qué escalarlo es un problema abierto.
- Relacionar batch y stream con funciones deterministas, idempotencia y reprocesamiento para la evolución de esquemas.
- Diferenciar bases de datos federadas (unifican lecturas) de desagregadas (unifican escrituras con logs).
- Razonar sobre write path y read path y cómo caches, índices y vistas materializadas desplazan la frontera entre ambos, incluso hasta el cliente (offline-first, publish/subscribe).
- Aplicar el argumento end-to-end: identificadores de operación idempotentes y restricción de unicidad sobre request_id para lograr exactamente-una-vez.
- Separar puntualidad de integridad y justificar los sistemas que evitan coordinación y las restricciones laxas con compensaciones.
- Fundamentar "trust, but verify": auditar, comparar réplicas, restaurar backups y diseñar para auditabilidad.
- Reconocer las responsabilidades éticas: sesgo y discriminación, rendición de cuentas, bucles de retroalimentación, privacidad, vigilancia y los datos como activo tóxico.
