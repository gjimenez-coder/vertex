# Storage and Retrieval (Almacenamiento y recuperación) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son las dos cosas fundamentales que hace una base de datos? / R: Cuando le das datos los guarda, y cuando se los pides luego te los devuelve.

P: ¿Qué es un log en el sentido general que usan muchas bases de datos? / R: Una secuencia de registros solo-de-adición (append-only), no necesariamente legible por humanos.

P: ¿Qué es un índice y qué compromiso impone? / R: Son metadatos que se mantienen aparte y guían la localización de los datos; aceleran las lecturas pero ralentizan las escrituras porque también hay que actualizarlos.

P: ¿Cómo funciona un índice hash y qué motor lo ejemplifica? / R: Mantiene en memoria un mapa hash que asocia cada clave a un offset de bytes en el fichero de datos; lo usa Bitcask (motor por defecto de Riak), con el requisito de que todas las claves quepan en RAM.

P: ¿Qué es una SSTable y qué ventajas aporta frente a un índice hash? / R: Una Sorted String Table guarda los pares ordenados por clave con cada clave una sola vez por segmento; permite fusión eficiente estilo mergesort, índice disperso (no toda clave en memoria) y compresión de bloques.

P: ¿Qué es un memtable y cómo se integra en un LSM-tree? / R: Un árbol balanceado en memoria (p. ej. rojo-negro) que recibe las escrituras; al superar un umbral se vuelca a disco como SSTable (segmento más reciente) mientras un log en disco protege las escrituras recientes ante una caída.

P: ¿Para qué sirve un filtro de Bloom en un LSM-tree? / R: Para descartar rápidamente claves inexistentes y evitar lecturas de disco inútiles.

P: ¿Cómo organiza los datos un B-tree? / R: Divide la base de datos en páginas de tamaño fijo (tradicionalmente 4 KB), lee o escribe una página a la vez y las referencia entre sí formando un árbol balanceado de profundidad O(log n).

P: ¿Qué es el write-ahead log (WAL / redo log) y por qué lo usan los B-trees? / R: Un fichero append-only donde toda modificación se escribe antes de aplicarse a las páginas, para dar resiliencia ante caídas a medias que podrían corromper el índice.

P: Como regla general, ¿en qué destacan respectivamente LSM-trees y B-trees? / R: Los LSM-trees suelen ser más rápidos en escritura (menor amplificación, escrituras secuenciales) y los B-trees en lectura, con cada clave en un único lugar útil para transacciones.

P: ¿Qué diferencia a un heap file, un índice agrupado y un covering index? / R: El heap file guarda la fila real referenciada desde los índices; el índice agrupado (clustered) guarda la fila dentro del índice; el covering index guarda algunas columnas para responder consultas solo con el índice.

P: ¿Por qué las bases de datos en memoria son rápidas? / R: No tanto por evitar el disco (el SO ya cachea bloques), sino por evitar el coste de codificar las estructuras en un formato apto para disco.

P: ¿Qué distingue a OLTP de OLAP? / R: OLTP maneja muchas peticiones que tocan pocos registros por clave (cuello de botella: tiempo de búsqueda en disco); OLAP escanea muchísimos registros, lee pocas columnas y calcula agregados (cuello de botella: ancho de banda de disco).

P: ¿En qué consiste el esquema en estrella? / R: Una tabla de hechos central (cada fila un evento) con atributos y claves foráneas a tablas de dimensiones (quién, qué, dónde, cuándo, cómo y por qué del evento).

P: ¿Qué idea central tiene el almacenamiento orientado a columnas? / R: Guardar juntos todos los valores de cada columna (cada columna en su fichero, en el mismo orden de filas) para que la consulta solo lea las columnas necesarias.

## Preguntas de autoevaluación

P: ¿Por qué `db_get` de la base de datos más simple tiene mal rendimiento mientras `db_set` es eficiente? / R: `db_set` solo añade al final (append), lo que es muy eficiente; `db_get` tiene coste O(n) porque debe escanear todo el fichero en cada búsqueda. (Sección: Estructuras de datos que impulsan tu base de datos)

P: ¿Qué problema resuelven la compactación y la fusión de segmentos en un índice hash y por qué pueden correr en segundo plano? / R: Evitan quedarse sin disco descartando claves duplicadas (quedándose con el valor más reciente) y fusionando segmentos; como los segmentos son inmutables, corren en un hilo en segundo plano sin dejar de servir. (Sección: Índices hash)

P: ¿Cuáles son las dos limitaciones principales del índice hash? / R: Debe caber entero en memoria y las consultas por rango no son eficientes. (Sección: Índices hash)

P: ¿Qué ventajas de escritura tienen los LSM-trees frente a los B-trees y qué inconveniente puede surgir? / R: Menor amplificación de escritura y mayor throughput por usar escrituras secuenciales; el inconveniente es que la compactación puede interferir con lecturas/escrituras elevando la latencia en percentiles altos y, mal configurada, no alcanzar el ritmo de escritura. (Sección: Comparación entre B-trees y LSM-trees)

P: ¿Por qué se separa la analítica del OLTP en un data warehouse y cómo se carga? / R: Porque los internos y el patrón de acceso difieren y las consultas analíticas son muy exigentes; el warehouse es una copia de solo lectura de los sistemas OLTP, cargada mediante ETL (Extract–Transform–Load) y optimizada para accesos analíticos. (Sección: ¿Procesamiento de transacciones o analítica?)

P: ¿Cómo funciona la codificación por mapas de bits (bitmap encoding) y para qué sirve? / R: Una columna con n valores distintos se convierte en n mapas de bits (uno por valor, un bit por fila); si son dispersos se añade run-length encoding, y consultas con `IN` o `AND` se resuelven con operaciones OR/AND bit a bit muy eficientes. (Sección: Almacenamiento orientado a columnas)

P: ¿Por qué ayuda a la compresión imponer un orden a las filas en almacenamiento columnar? / R: Porque la primera clave de orden queda muy repetida y comprime muy bien con run-length encoding; además permite consultas por rango. (Sección: Almacenamiento orientado a columnas)

P: ¿Qué es un data cube (cubo OLAP) y qué compromiso implica? / R: Es un caso especial de vista materializada: una rejilla de agregados por dimensiones que acelera ciertas consultas a costa de flexibilidad. (Sección: Almacenamiento orientado a columnas)

## Puntos a dominar

- Distinguir las dos familias de motores OLTP: log-structured (Bitcask, SSTables, LSM-trees; LevelDB, RocksDB, Cassandra, HBase, Lucene) y update-in-place (B-trees).
- Explicar el flujo de un LSM-tree: memtable en memoria, volcado a SSTable, log de recuperación, fusión y compactación en segundo plano, filtros de Bloom y estrategias size-tiered vs leveled.
- Describir la estructura de un B-tree: páginas de 4 KB, factor de ramificación, partición de páginas, balanceo O(log n), WAL y latches para concurrencia.
- Comparar amplificación de escritura, throughput y semántica transaccional entre LSM-trees y B-trees, recordando probar con la propia carga.
- Identificar los tipos de índices: secundario, agrupado (clustered), de cobertura (covering), concatenado, multidimensional (R-trees) y difuso (distancia de edición en Lucene).
- Justificar por qué las bases de datos en memoria son rápidas y conocer ejemplos (Memcached, VoltDB, MemSQL, Oracle TimesTen, RAMCloud, Redis, Couchbase) y el enfoque anti-caching.
- Contrastar OLTP y OLAP, y el papel del data warehouse con ETL y esquemas en estrella/copo de nieve.
- Explicar el almacenamiento columnar: compresión por mapas de bits, run-length encoding, ordenación de filas, procesamiento vectorizado (SIMD), escritura vía LSM-trees y agregados materializados.
