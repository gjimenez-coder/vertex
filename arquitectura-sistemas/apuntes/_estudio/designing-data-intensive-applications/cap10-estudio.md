# Batch Processing (Procesamiento por lotes) — Estudio

## Tarjetas de repaso

P: ¿Qué tres tipos de sistemas distingue el capítulo y cuál es la métrica clave de cada uno?
R: Servicios online (tiempo de respuesta), procesamiento por lotes offline (throughput) y procesamiento de flujos near-real-time (intermedio entre ambos).

P: ¿Cuál es la tesis central del capítulo sobre la filosofía Unix?
R: Que sus principios (entradas inmutables, la salida de un programa como entrada de otro, componer herramientas que hacen una cosa bien) se trasladan a sistemas distribuidos de gran escala como MapReduce y los motores de dataflow.

P: ¿Qué es HDFS y en qué principio se basa?
R: Es el sistema de ficheros distribuido de Hadoop, reimplementación de código abierto del Google File System; se basa en el principio shared-nothing, frente al shared-disk de NAS y SAN.

P: ¿Cómo tolera fallos HDFS?
R: Replicando los bloques en varias máquinas, bien por copias múltiples, bien mediante erasure coding (p. ej. códigos Reed–Solomon); un NameNode central registra qué bloques están en qué máquina.

P: ¿En qué cuatro pasos consiste la ejecución de un trabajo MapReduce?
R: Leer y dividir los ficheros en registros; llamar al mapper para extraer clave-valor de cada registro; ordenar los pares por clave; llamar al reducer para iterar sobre los pares ordenados.

P: ¿Qué es el shuffle en MapReduce?
R: El proceso de particionar, ordenar y copiar la salida de los mappers hacia los reducers; la ordenación es implícita, pues la salida del mapper siempre se ordena antes de entregarse al reducer.

P: ¿Qué hace el mapper y qué hace el reducer?
R: El mapper se llama una vez por registro, extrae clave y valor sin guardar estado; el reducer recibe todos los valores de una misma clave mediante un iterador y produce registros de salida.

P: ¿Qué es un sort-merge join?
R: Un join del lado del reducer donde los mappers extraen el ID como clave de ambas entradas; al particionar y ordenar, los registros del mismo ID quedan adyacentes y el reducer los une sin peticiones por red.

P: ¿En qué consiste el broadcast hash join?
R: En un map-side join donde un dataset grande se une con uno pequeño que cabe en memoria: cada mapper carga el pequeño en una tabla hash y escanea su bloque del grande.

P: ¿Qué es el partitioned hash join?
R: Un map-side join aplicable cuando ambas entradas están particionadas igual (misma clave, función hash y número de particiones), aplicando la tabla hash por partición de forma independiente.

P: ¿Qué es el skew (hot keys o linchpin objects) y por qué es un problema?
R: Una clave con muchísimos datos (p. ej. una celebridad) que satura un solo reducer y retrasa el trabajo al romper el patrón de reunir datos relacionados en el mismo sitio.

P: ¿Qué tipos de salida suelen producir los flujos de trabajo por lotes?
R: No un informe, sino estructuras como índices de búsqueda y almacenes clave-valor de solo lectura construidos como ficheros y cargados en bloque (Voldemort, Terrapin, ElephantDB, bulk loading de HBase).

P: ¿Qué significa schema-on-read / data lake en la comparación de Hadoop con las MPP?
R: Que en un sistema de ficheros distribuido los datos son secuencias de bytes en cualquier formato; se vuelcan sin discriminación y se decide después cómo procesarlos ("raw data is better").

P: ¿Qué problema de los trabajos MapReduce encadenados resuelven los motores de dataflow?
R: La materialización completa del estado intermedio: tratan el workflow como un solo trabajo, mantienen el estado intermedio en memoria o disco local y recomputan ante fallos en vez de escribirlo todo en HDFS.

P: ¿Qué es el modelo Pregel / BSP y para qué sirve?
R: El modelo bulk synchronous parallel para procesamiento iterativo de grafos: un vértice "envía un mensaje" a otro por las aristas, se llama una función por vértice en cada iteración y el vértice recuerda su estado entre iteraciones.

## Preguntas de autoevaluación

P: ¿Por qué el enfoque de ordenación puede ser mejor que una tabla hash en memoria para contar URLs en un log grande?
R: Porque si el working set es mayor que la memoria disponible, ordenar aprovecha mejor el disco (como SSTables y LSM-Trees): ordena por trozos en memoria, vuelca segmentos a disco y los fusiona; el `sort` de GNU vuelca a disco y paraleliza. (Sección: Procesamiento por lotes con herramientas Unix)

P: ¿Cuáles son los dos problemas centrales del batch processing distribuido?
R: La partición (reunir los datos relacionados en el mismo sitio) y la tolerancia a fallos (reintentar tareas con seguridad gracias a entradas inmutables y al descarte de salidas parciales). (Sección: Ideas clave / Joins y agrupamiento del lado del reducer)

P: ¿Por qué no se consulta la base de datos remota de perfiles por cada evento en un join con MapReduce?
R: Porque tendría muy mal rendimiento y haría el trabajo no determinista; es mejor copiar la base de usuarios al mismo sistema de ficheros distribuido vía ETL y unir con MapReduce. (Sección: Joins y agrupamiento del lado del reducer)

P: ¿Por qué es mala idea que un trabajo por lotes escriba directamente, registro a registro, en la base de datos de producción?
R: Porque es lento, satura la base de datos y rompe la garantía todo-o-nada; es mejor construir una base de solo lectura como ficheros y cargarla en bloque, cambiando atómicamente al terminar. (Sección: La salida de los flujos de trabajo por lotes)

P: ¿Por qué MapReduce se diseñó para tolerar terminaciones frecuentes de tareas?
R: No por hardware poco fiable, sino para mejorar la utilización del clúster en datacenters de uso mixto donde tareas de baja prioridad se expulsan (preempt); una tarea de una hora tiene ~5% de riesgo de terminación. (Sección: Comparación de Hadoop con bases de datos distribuidas)

P: ¿Qué desventajas tiene materializar por completo el estado intermedio frente a las tuberías Unix?
R: Un trabajo no empieza hasta que terminan todas las tareas del anterior (los stragglers ralentizan todo), los mappers suelen releer lo que escribió un reducer y el estado intermedio se replica, algo excesivo para datos temporales. (Sección: Materialización del estado intermedio y motores de dataflow)

P: ¿Por qué importa que los operadores de un motor de dataflow sean deterministas?
R: Porque, al no escribir el estado intermedio en HDFS, lo recomputan si una máquina falla; para recomputar correctamente hay que evitar orden no garantizado de hash tables, números aleatorios sin semilla fija o uso del reloj. (Sección: Materialización del estado intermedio y motores de dataflow)

P: ¿Por qué MapReduce no expresa bien algoritmos iterativos de grafos como PageRank?
R: Porque hace una sola pasada; implementarlo iterativamente con un planificador externo es ineficiente al releer todo el dataset en cada iteración, lo que optimiza el modelo Pregel/BSP. (Sección: Grafos y procesamiento iterativo)

## Puntos a dominar

- Distinguir servicios online, procesamiento por lotes y procesamiento de flujos, y la métrica clave de cada uno.
- Explicar la cadena de comandos Unix del análisis de logs y qué hace cada herramienta (awk, sort, uniq -c, sort -r -n, head).
- Enunciar los principios de la filosofía Unix y cómo se trasladan a MapReduce.
- Describir el modelo shared-nothing de HDFS y sus mecanismos de tolerancia a fallos.
- Reproducir los cuatro pasos de un trabajo MapReduce y el papel de mapper, shuffle y reducer.
- Comparar los joins distribuidos: sort-merge, broadcast hash, partitioned hash y map-side merge, y cuándo aplica cada uno.
- Reconocer el skew (hot keys) y las técnicas para compensarlo (skewed join de Pig, sharded join de Crunch, skewed join de Hive).
- Identificar las salidas típicas del batch (índices de búsqueda, almacenes clave-valor de solo lectura) y por qué se cargan en bloque.
- Contrastar Hadoop con las bases de datos MPP en almacenamiento, modelos de procesamiento y diseño para fallos.
- Explicar qué mejoran los motores de dataflow (Spark, Tez, Flink) y el modelo Pregel/BSP para grafos.
