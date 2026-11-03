# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 10 — Batch Processing (Procesamiento por lotes)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

El capítulo distingue tres tipos de sistemas: los servicios (sistemas online), que esperan una petición y responden lo más rápido posible, donde la métrica clave es el tiempo de respuesta; los sistemas de procesamiento por lotes (offline), que toman un gran volumen de datos de entrada, ejecutan un trabajo y producen una salida, cuya métrica clave es el throughput; y el procesamiento de flujos (near-real-time), situado entre ambos y tratado en el Capítulo 11. El batch processing es un bloque fundamental para construir aplicaciones fiables, escalables y mantenibles.

La tesis central es que los principios de diseño de las herramientas Unix (entradas inmutables, salidas destinadas a ser entrada de otro programa, componer herramientas pequeñas que "hacen una cosa bien") se trasladan a sistemas distribuidos de gran escala como MapReduce y los motores de dataflow más recientes. MapReduce, publicado en 2004, es un modelo de bajo nivel pero fue un gran avance en la escala alcanzable sobre hardware común; aunque su importancia declina, sigue siendo útil para entender por qué y cómo funciona el procesamiento por lotes.

Sales sabiendo cómo se procesan datos con herramientas Unix, cómo ejecuta un trabajo MapReduce sobre un sistema de ficheros distribuido (HDFS), los principales algoritmos de join distribuido (sort-merge, broadcast hash, partitioned hash), qué salidas producen los flujos de trabajo por lotes, cómo se compara Hadoop con las bases de datos distribuidas (MPP), y qué mejoras aportan los motores de dataflow como Spark, Flink y Tez, además del modelo Pregel para grafos.

## Procesamiento por lotes con herramientas Unix

El ejemplo hilo conductor es un log de acceso de nginx: cada petición añade una línea con IP del cliente, usuario, fecha, petición, estado y bytes. Para hallar las cinco páginas más populares se encadena en el shell:

```
cat /var/log/nginx/access.log |
  awk '{print $7}' |
  sort             |
  uniq -c          |
  sort -r -n       |
  head -n 5
```

`awk` extrae el campo 7 (la URL), `sort` ordena alfabéticamente para dejar iguales adyacentes, `uniq -c` cuenta ocurrencias, el segundo `sort -r -n` ordena por número descendente y `head` deja las cinco primeras. Procesa gigabytes en segundos y se modifica con facilidad.

Una alternativa es un programa propio (ejemplo en Ruby) que mantiene una tabla hash en memoria con un contador por URL. La diferencia de fondo entre ambos enfoques es cómo se agrega: la tabla hash en memoria frente a ordenar la lista. ¿Cuál es mejor? Depende del número de URLs distintas: si el working set cabe en memoria (p. ej. 1 GB), la tabla hash funciona bien incluso en un portátil; si es mayor que la memoria disponible, el enfoque de ordenación aprovecha mejor el disco, con el mismo principio de las SSTables y LSM-Trees: ordenar por trozos en memoria, escribir segmentos en disco y fusionarlos. El `sort` de GNU Coreutils vuelca a disco automáticamente y paraleliza entre CPUs, por lo que la cadena de comandos escala a grandes datasets; el cuello de botella suele ser la velocidad de lectura del fichero.

## La filosofía Unix

Doug McIlroy describió las tuberías en 1964 como "conectar programas como [una] manguera de jardín" (PDF p. 416). La filosofía Unix (1978) reúne cuatro principios: que cada programa haga una cosa bien; esperar que la salida de un programa sea entrada de otro, evitando formatos binarios o rígidos y sin exigir entrada interactiva; diseñar software para probarlo pronto, descartando lo torpe; y usar herramientas aun si hay que detenerse a construirlas. Esto recuerda a los movimientos Agile y DevOps actuales.

¿Qué permite esa componibilidad?

- Una interfaz uniforme: en Unix esa interfaz es el fichero (un descriptor de fichero), una secuencia ordenada de bytes que representa tanto un fichero real como un socket, un dispositivo o una conexión TCP. Por convención muchos programas tratan esos bytes como texto ASCII separado por `\n`. No es perfecto (`{print $7}` no es muy legible), pero sigue siendo notable; su ausencia lleva a la "balcanización" de los datos.
- Separación de lógica y cableado: el uso de stdin y stdout, combinado con tuberías, permite al usuario conectar entradas y salidas sin que el programa sepa de dónde vienen ni a dónde van (un tipo de acoplamiento débil, late binding o inversión de control). Hay límites: no es fácil manejar múltiples entradas/salidas ni dirigir la salida a una conexión de red sin herramientas aparte.
- Transparencia y experimentación: las entradas se tratan como inmutables, se puede detener la tubería en cualquier punto y canalizarla a `less` para inspeccionar, y escribir la salida de una etapa a un fichero para reiniciar etapas posteriores sin rehacer todo.

La mayor limitación de las herramientas Unix es que corren en una sola máquina; ahí entra Hadoop.

## MapReduce y sistemas de ficheros distribuidos

MapReduce es como las herramientas Unix pero distribuido entre miles de máquinas: un trabajo toma una o más entradas y produce una o más salidas, normalmente sin modificar la entrada ni tener efectos secundarios. Mientras Unix usa stdin/stdout, los trabajos MapReduce leen y escriben ficheros en un sistema de ficheros distribuido; en Hadoop ese sistema es HDFS, una reimplementación de código abierto del Google File System (GFS).

HDFS se basa en el principio shared-nothing, frente al shared-disk de NAS y SAN; no requiere hardware especial, solo máquinas conectadas por una red de datacenter convencional. Un demonio corre en cada máquina exponiendo sus discos, y un servidor central (NameNode) registra qué bloques están en qué máquina. Para tolerar fallos, los bloques se replican en varias máquinas, bien por copias múltiples, bien mediante erasure coding (p. ej. códigos Reed–Solomon). Los mayores despliegues de HDFS corren en decenas de miles de máquinas con cientos de petabytes, viable por el bajo coste del hardware común.

### Ejecución de un trabajo MapReduce

El patrón es idéntico al del análisis de logs y consta de cuatro pasos: leer los ficheros de entrada y dividirlos en registros; llamar a la función mapper para extraer una clave y un valor de cada registro; ordenar todos los pares clave-valor por clave; y llamar a la función reducer para iterar sobre los pares ordenados. El paso de ordenación (shuffle) es implícito: la salida del mapper siempre se ordena antes de entregarse al reducer. El programador solo implementa dos callbacks:

- Mapper: se llama una vez por registro de entrada, extrae clave y valor, puede generar cualquier número de pares (incluido ninguno) y no guarda estado entre registros.
- Reducer: el framework reúne todos los valores de una misma clave y llama al reducer con un iterador sobre esa colección, que puede producir registros de salida.

La paralelización se basa en la partición: cada fichero o bloque de la entrada es una partición procesada por una tarea map separada. El planificador intenta ejecutar cada mapper en una máquina que almacene una réplica del fichero de entrada (poner la computación cerca de los datos) para ahorrar tráfico de red. El número de tareas map depende de los bloques de entrada; el de tareas reduce lo configura el autor. Para que todos los pares con la misma clave lleguen al mismo reducer se usa un hash de la clave. Cada mapper particiona y ordena su salida localmente, y los reducers descargan de cada mapper los ficheros de su partición y los fusionan preservando el orden: ese proceso de particionar, ordenar y copiar es el shuffle.

### Flujos de trabajo MapReduce

El rango de problemas resolubles con un solo trabajo es limitado (por ejemplo, contar vistas por URL sí, pero no las URLs más populares, que requieren una segunda ordenación). Por eso es común encadenar trabajos en workflows, donde la salida de uno es la entrada del siguiente. Hadoop no ofrece soporte explícito para workflows: el encadenamiento se hace implícitamente por el nombre del directorio. La salida de un trabajo solo es válida tras completarse con éxito (MapReduce descarta la salida parcial de trabajos fallidos), por lo que han surgido planificadores como Oozie, Azkaban, Luigi, Airflow y Pinball. Herramientas de más alto nivel como Pig, Hive, Cascading, Crunch y FlumeJava también configuran workflows de varias etapas.

### Joins y agrupamiento del lado del reducer

Un join resuelve todas las ocurrencias de una asociación en un dataset (foreign key, referencia de documento o arista de un grafo). MapReduce no tiene índices: lee todo el contenido (full table scan), algo razonable en consultas analíticas que agregan sobre muchos registros. El ejemplo típico: correlacionar eventos de actividad de usuarios (fact table) con una base de datos de perfiles (dimensión). Consultar la base de datos remota por cada evento tendría muy mal rendimiento y haría el trabajo no determinista; mejor copiar la base de datos de usuarios al mismo sistema de ficheros distribuido (vía ETL) y unir con MapReduce.

En el sort-merge join, un conjunto de mappers extrae el user ID como clave de los eventos y otro conjunto lo extrae de la base de usuarios; al particionar y ordenar, todos los registros del mismo user ID quedan adyacentes en la entrada del reducer. Mediante un secondary sort, el reducer puede ver primero el registro de perfil y luego los eventos. Así solo necesita mantener un registro en memoria y nunca hace peticiones por red. Una forma de verlo: los mappers "envían mensajes" a los reducers, donde la clave actúa como dirección de destino; MapReduce separa la comunicación física por red de la lógica de aplicación y reintenta tareas fallidas de forma transparente.

El patrón de "llevar los datos relacionados al mismo lugar" también sirve para GROUP BY: contar registros por grupo, sumar un campo o elegir los top k; además de la sessionización (agrupar eventos de una sesión de usuario). Este patrón se rompe con el skew (hot keys o linchpin objects): una clave con muchísimos datos (p. ej. una celebridad) satura un reducer y retrasa el trabajo. Para compensar existen el skewed join de Pig (que muestrea para detectar claves calientes y las reparte al azar entre varios reducers, replicando la otra entrada), el sharded join de Crunch (claves calientes explícitas) y el skewed join de Hive (claves en metadatos y map-side join para ellas); al agrupar se puede hacer en dos etapas.

### Map-side joins

Si se asumen ciertas propiedades de la entrada, el join se acelera con un map-side join: un trabajo recortado sin reducers ni ordenación.

- Broadcast hash join: aplica cuando un dataset grande se une con uno pequeño que cabe en memoria. Cada mapper carga el dataset pequeño en una tabla hash y escanea su bloque del grande buscando cada registro. Soportado por Pig ("replicated join"), Hive ("MapJoin"), Cascading, Crunch e Impala.
- Partitioned hash join: si ambas entradas están particionadas igual (misma clave, misma función hash, mismo número de particiones), la tabla hash se aplica por partición de forma independiente, cargando menos datos por mapper. En Hive son "bucketed map joins".
- Map-side merge join: si además están ordenadas por la misma clave, el mapper fusiona ambas entradas de forma incremental, sin que tengan que caber en memoria.

La elección afecta a la estructura de la salida: un reduce-side join produce salida particionada y ordenada por la clave del join, mientras que un map-side join la produce particionada y ordenada como la entrada grande. Los metadatos sobre partición suelen mantenerse en HCatalog y el Hive metastore.

### La salida de los flujos de trabajo por lotes

El batch processing no es ni OLTP ni analítica pura; se acerca a la analítica pero su salida no suele ser un informe, sino otra estructura:

- Índices de búsqueda: el uso original de MapReduce en Google (workflow de 5 a 10 trabajos). Para una colección fija de documentos, los mappers particionan los documentos, cada reducer construye el índice de su partición y los ficheros, inmutables, se escriben en el sistema distribuido. Si los documentos cambian se puede reconstruir todo el índice periódicamente o construirlo de forma incremental (como hace Lucene con sus segmentos).
- Almacenes clave-valor como salida: para sistemas de ML (clasificadores, recomendación). Escribir desde el trabajo directamente a la base de datos de producción, registro a registro, es mala idea (lento, satura la base, rompe la garantía todo-o-nada). Mejor construir una base de datos de solo lectura como ficheros en el directorio de salida y cargarla en bloque; lo soportan Voldemort, Terrapin, ElephantDB y el bulk loading de HBase. Voldemort sigue sirviendo los ficheros antiguos mientras copia los nuevos y cambia atómicamente al terminar.

La filosofía de las salidas sigue la de Unix: tratar las entradas como inmutables y evitar efectos secundarios facilita el mantenimiento. Si un bug corrompe la salida, basta revertir el código y reejecutar (human fault tolerance); el framework reintenta tareas fallidas con seguridad precisamente porque las entradas son inmutables; los mismos ficheros pueden alimentar varios trabajos, incluidos los de monitorización. A diferencia de Unix, en Hadoop se evitan conversiones sintácticas usando formatos estructurados como Avro y Parquet.

### Comparación de Hadoop con bases de datos distribuidas

Hadoop es como una versión distribuida de Unix. Los algoritmos de MapReduce ya existían en las bases de datos MPP (Gamma, Teradata, Tandem NonStop SQL) una década antes. La mayor diferencia: las MPP se centran en ejecutar consultas SQL analíticas en paralelo, mientras que MapReduce más un sistema de ficheros distribuido ofrece algo más parecido a un sistema operativo de propósito general que ejecuta programas arbitrarios.

- Diversidad de almacenamiento: las bases de datos exigen modelar los datos según un modelo; en un sistema de ficheros distribuido los datos son secuencias de bytes en cualquier formato. Hadoop permite volcar datos sin discriminación y decidir después cómo procesarlos (schema-on-read, "data lake", principio del sushi: "raw data is better"). Se usa mucho para ETL.
- Diversidad de modelos de procesamiento: las MPP son monolíticas e integradas, pero no todo se expresa bien en SQL (ML, búsqueda, análisis de imágenes). Sobre Hadoop se pueden construir muchos modelos (incluido un motor SQL, como hizo Hive) y correrlos sobre el mismo clúster compartido sin mover los datos. El ecosistema incluye tanto HBase (OLTP de acceso aleatorio) como Impala (analítico estilo MPP).
- Diseño para fallos frecuentes: los procesos por lotes son menos sensibles a fallos. Las MPP abortan y reejecutan la consulta entera y prefieren mantener datos en memoria; MapReduce tolera el fallo de una tarea reintentándola individualmente y escribe con avidez en disco. Esto encaja con el entorno de Google: datacenters de uso mixto donde tareas de baja prioridad se expulsan (preempt) para liberar recursos. Una tarea de una hora tiene ~5% de riesgo de terminación; MapReduce se diseñó para tolerar terminaciones frecuentes no por hardware poco fiable, sino para mejorar la utilización del clúster. La expulsión es menos usada en planificadores de código abierto (YARN, Mesos, Kubernetes).

## Más allá de MapReduce

MapReduce es un buen recurso didáctico (una abstracción clara sobre un sistema de ficheros distribuido), pero implementar trabajos complejos con sus APIs crudas es laborioso (hay que programar los joins desde cero). Por eso surgieron APIs de más alto nivel (Pig, Hive, Cascading, Crunch). Además, el modelo de ejecución tiene problemas propios de rendimiento para ciertos trabajos.

### Materialización del estado intermedio y motores de dataflow

Cada trabajo MapReduce es independiente y se comunica con el resto solo por sus directorios de entrada y salida. Cuando la salida de un trabajo solo sirve de entrada a otro del mismo equipo, esos ficheros son simplemente estado intermedio; escribirlos se llama materialización. Materializar por completo tiene desventajas frente a las tuberías Unix: un trabajo no empieza hasta que terminan todas las tareas del anterior (los stragglers ralentizan todo), los mappers suelen ser redundantes (releen lo que escribió un reducer) y el estado intermedio se replica, algo excesivo para datos temporales.

Para resolverlo surgieron motores de dataflow como Spark, Tez y Flink, que tratan todo el workflow como un solo trabajo. Modelan explícitamente el flujo de datos entre etapas; sus funciones, llamadas operadores, no se limitan a map y reduce y se conectan de formas flexibles (reparticionar y ordenar por clave, particionar sin ordenar, o difundir a todas las particiones). Ventajas frente a MapReduce: ordenar solo donde hace falta, evitar tareas map innecesarias, optimizaciones de localidad por parte del planificador, mantener el estado intermedio en memoria o disco local (menos I/O que HDFS), empezar operadores en cuanto su entrada esté lista, y reutilizar procesos JVM.

La tolerancia a fallos es distinta: al no escribir el estado intermedio en HDFS, lo recomputan si una máquina falla. Spark usa la abstracción RDD (resilient distributed dataset) para rastrear la ascendencia de los datos; Flink hace checkpoints del estado de los operadores. Para recomputar es importante que los operadores sean deterministas (evitando orden no garantizado de hash tables, números aleatorios sin semilla fija, o uso del reloj). A veces es más barato materializar que recomputar. Al final, las entradas y la salida final de un trabajo siguen estando normalmente en HDFS.

### Grafos y procesamiento iterativo

En contexto de batch, el objetivo es analizar un grafo entero (p. ej. PageRank). Muchos algoritmos recorren una arista cada vez y repiten hasta converger, algo que MapReduce no expresa bien porque hace una sola pasada; implementarlo de forma iterativa con un planificador externo es ineficiente, pues relee todo el dataset cada iteración. La optimización es el modelo bulk synchronous parallel (BSP) o Pregel (popularizado por Google), implementado por Apache Giraph, GraphX de Spark y Gelly de Flink. En Pregel, un vértice "envía un mensaje" a otro a lo largo de las aristas; en cada iteración se llama a una función por vértice con los mensajes recibidos, y el vértice recuerda su estado en memoria entre iteraciones. Se parece al modelo de actores, pero con estado y mensajes duraderos y tolerantes a fallos (mediante checkpointing periódico) y comunicación en rondas fijas. El framework particiona el grafo por ID de vértice, lo que genera mucha comunicación entre máquinas; si el grafo cabe en una sola máquina, un algoritmo mono-máquina suele superar al distribuido.

### APIs y lenguajes de alto nivel

Las APIs de dataflow (Hive, Pig, Cascading, Crunch, y las propias de Spark y Flink, inspiradas en FlumeJava) usan bloques de estilo relacional: joins, agrupamientos, filtros y agregaciones. Requieren menos código, permiten uso interactivo y mejoran la eficiencia. Especificar joins de forma declarativa deja que un optimizador basado en costes elija el mejor algoritmo e incluso reordene joins (Hive, Spark, Flink). A diferencia del modelo totalmente declarativo de SQL, MapReduce se basa en callbacks que pueden ejecutar código arbitrario, aprovechando ecosistemas de librerías. Los motores de dataflow incorporan rasgos declarativos (almacenamiento columnar, ejecución vectorizada, generación de bytecode/código nativo) acercándose a las MPP sin perder flexibilidad. También emergen implementaciones reutilizables por dominio: Mahout y MADlib para ML, algoritmos espaciales como k-nearest neighbors y análisis de genomas.

## Ideas clave

- Existen tres estilos de sistemas: servicios online (métrica: tiempo de respuesta), procesamiento por lotes offline (métrica: throughput) y procesamiento de flujos near-real-time; el batch processing opera sobre una entrada acotada y termina cuando la ha leído entera.
- Los principios de la filosofía Unix (entradas inmutables, salida de un programa como entrada de otro, componer herramientas que hacen una cosa bien, separar lógica de cableado) se trasladan a MapReduce, donde la interfaz uniforme pasa del fichero/pipe al sistema de ficheros distribuido (HDFS).
- Un trabajo MapReduce consta de mapper (extrae clave-valor por registro), ordenación implícita (shuffle) y reducer (procesa los valores de cada clave); paraleliza por partición y acerca la computación a los datos.
- Los dos problemas centrales del batch distribuido son la partición (reunir los datos relacionados en el mismo sitio) y la tolerancia a fallos (reintentar tareas con seguridad gracias a entradas inmutables y descarte de salidas parciales).
- Principales joins distribuidos: sort-merge join (del lado del reducer), broadcast hash join (una entrada pequeña cargada en memoria) y partitioned hash join (ambas entradas particionadas igual); el skew con hot keys exige técnicas específicas.
- La salida de un flujo por lotes no suele ser un informe, sino estructuras como índices de búsqueda o almacenes clave-valor de solo lectura cargados en bloque, evitando escribir directamente en bases de datos de producción.
- Hadoop se parece a un SO de propósito general frente a las bases MPP: admite almacenamiento y modelos de procesamiento diversos (schema-on-read, data lake) y está diseñado para tolerar fallos y expulsiones frecuentes.
- Los motores de dataflow (Spark, Tez, Flink) tratan el workflow como un solo trabajo, evitan materializar el estado intermedio en HDFS y recomputan ante fallos; el modelo Pregel/BSP adapta el enfoque a grafos, y las APIs declarativas de alto nivel acercan estos sistemas a las MPP.
