# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)

Autor: Martin Kleppmann.

Estudio de los internals de sistemas de datos reales en producción para ir más allá de las buzzwords (NoSQL, Big Data, teorema CAP, MapReduce, tiempo real) hacia los principios perdurables que permiten elegir y usar bien cada herramienta y tomar buenas decisiones de arquitectura. El libro se estructura en tres partes: fundamentos de los sistemas de datos (fiabilidad, escalabilidad y mantenibilidad, modelos de datos, almacenamiento y codificación), datos distribuidos (replicación, particionamiento, transacciones, problemas de los sistemas distribuidos, consistencia y consenso) y datos derivados (procesamiento por lotes y de flujos, y el futuro de los sistemas de datos).

## Capítulos

- [Prólogo — Preface (Prólogo)](cap00-preface.md): sitúa el libro frente a las buzzwords y defiende los principios perdurables que permiten elegir y usar bien cada tecnología de datos.
- [Capítulo 1 — Reliable, Scalable, and Maintainable Applications (Aplicaciones fiables, escalables y mantenibles)](cap01-reliable-scalable-and-maintainable-applications.md): las aplicaciones data-intensive se construyen con bloques estándar y deben ser fiables, escalables y mantenibles.
- [Capítulo 2 — Data Models and Query Languages (Modelos de datos y lenguajes de consulta)](cap02-data-models-and-query-languages.md): compara modelos relacional, de documentos y de grafos, y los lenguajes declarativos de consulta.
- [Capítulo 3 — Storage and Retrieval (Almacenamiento y recuperación)](cap03-storage-and-retrieval.md): cómo guardan y recuperan datos los motores de almacenamiento, de LSM-trees y B-trees al almacenamiento columnar para OLAP.
- [Capítulo 4 — Encoding and Evolution (Codificación y evolución)](cap04-encoding-and-evolution.md): formatos de codificación y compatibilidad backward/forward para que versiones viejas y nuevas coexistan durante los rolling upgrades.
- [Capítulo 5 — Replication (Replicación)](cap05-replication.md): mantener copias de los datos con enfoques single-leader, multi-leader y leaderless, y gestionar el retraso de replicación.
- [Capítulo 6 — Partitioning (Particionamiento)](cap06-partitioning.md): dividir los datos en particiones (sharding) para escalar, evitando skew y hot spots, con rebalanceo y enrutamiento.
- [Capítulo 7 — Transactions (Transacciones)](cap07-transactions.md): las transacciones como unidad todo-o-nada, las anomalías de aislamiento y los niveles hasta la serializabilidad.
- [Capítulo 8 — The Trouble with Distributed Systems (Los problemas de los sistemas distribuidos)](cap08-the-trouble-with-distributed-systems.md): recorrido pesimista por los fallos parciales, redes poco fiables, relojes imprecisos y pausas de procesos.
- [Capítulo 9 — Consistency and Consensus (Consistencia y consenso)](cap09-consistency-and-consensus.md): linealizabilidad, causalidad, CAP y el consenso tolerante a fallos como abstracción central.
- [Capítulo 10 — Batch Processing (Procesamiento por lotes)](cap10-batch-processing.md): procesamiento offline sobre entradas acotadas con MapReduce, joins distribuidos y motores de dataflow.
- [Capítulo 11 — Stream Processing (Procesamiento de flujos)](cap11-stream-processing.md): procesar datos ilimitados conforme ocurren, con brokers, logs de eventos, ventanas y joins sobre flujos.
- [Capítulo 12 — The Future of Data Systems (El futuro de los sistemas de datos)](cap12-the-future-of-data-systems.md): cómo diseñar aplicaciones de datos integrando sistemas en torno al dataflow, con corrección end-to-end y responsabilidad ética.
