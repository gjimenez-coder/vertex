# Big Data (Big Data / Grandes volúmenes de datos) — Estudio

## Tarjetas de repaso

P: ¿Qué designa el término Big Data? / R: Varias tendencias en los datos y en las tecnologías para procesarlos; no es solo datasets enormes, sino los retos, oportunidades y soluciones de almacenamiento y procesamiento que surgieron con ellos.

P: ¿Qué dos propiedades suelen tener los datasets de Big Data? / R: Que son grandes (no caben ni se procesan prácticamente en un solo computador y requieren un clúster) y que suelen ser "no estructurados" (no encajan limpiamente en una base de datos relacional).

P: ¿Qué significa "no estructurado" en este contexto? / R: No que carezca de estructura, sino que no encaja bien en una base relacional (SQL); ejemplos: imágenes, PDFs, HTML, Excel desordenados y logs de máquinas.

P: ¿Qué compensación (trade-off) ofrece Big Data frente a las bases tradicionales? / R: Aporta flexibilidad para datos en cualquier formato, pero se paga en tiempo de ejecución porque hay pocas optimizaciones prefabricadas; las bases tradicionales exigen estructura rígida a cambio de rendimiento optimizado.

P: ¿Cómo combina el autor Big Data con herramientas tradicionales? / R: Usa Big Data para extraer features (que ocupan mucho menos) y luego analiza en una máquina normal con algo como Pandas; rara vez hace machine learning o visualización con Big Data.

P: ¿Qué es Hadoop y cuáles son sus dos partes? / R: Una implementación libre y de código abierto de MapReduce en Java (creada por Doug Cutting); consta de HDFS (almacenamiento distribuido) y el framework MR que lee de HDFS, procesa en paralelo y escribe en HDFS.

P: ¿Por qué el autor considera "un dinosaurio" al MR de Hadoop? / R: Tiene mucha sobrecarga porque lee y escribe a disco (IO de disco muy lento frente a RAM) e integra mal con lenguajes convencionales; la comunidad se ha movido hacia Spark.

P: ¿Qué es un RDD y qué propiedades tiene? / R: Resilient Distributed Dataset: una colección de objetos Python distribuidos por el clúster, inmutable; sus métodos devuelven nuevos RDDs. Hay variantes sin clave y con clave (tuplas clave–valor).

P: ¿Qué es la evaluación perezosa (lazy) en Spark? / R: Al definir un RDD no se computa nada; Spark acumula una estructura de dependencias y solo crea los RDDs en cascada cuando se pide una salida (guardar en HDFS o traer a Python).

P: ¿Para qué sirve `cache()` en Spark? / R: Por defecto un RDD es efímero; `cache()` lo guarda en la RAM de los nodos para reutilizarlo, una gran diferencia frente al MR tradicional.

P: ¿Qué es el "shuffle"? / R: El paso de mover datos entre nodos serializando los objetos y rehidratándolos al otro lado (p. ej. en `groupByKey()`); es muy costoso y lo gestiona el framework Spark, no los procesos Python.

P: ¿En qué consisten las dos etapas de MapReduce? / R: Mapping: cada elemento se mapea a una colección de pares clave–valor (`flatMap`). Reducing: por cada clave única un proceso reduce recibe sus valores de uno en uno y produce salidas (`reduceByKey`).

P: ¿Qué es un "combiner" y cuándo es válido? / R: La optimización de que cada nodo condense localmente sus pares antes de enviarlos; solo es válida si la operación es conmutativa/asociativa (como la suma) y reduce mucho la presión sobre el ancho de banda.

P: ¿Cuándo conviene usar `aggregateByKey` en lugar de `reduceByKey`? / R: Cuando los valores agregados son estructuras grandes y mutables (p. ej. listas); `reduceByKey` recrea listas en memoria una y otra vez, mientras `aggregateByKey` mantiene una y va añadiendo (`append`).

## Preguntas de autoevaluación

P: ¿Cuándo NO deberías usar herramientas de Big Data? / R: Si tus datasets caben en una sola máquina o solo necesitas operaciones de SQL; las herramientas de Big Data suelen ser más lentas, más difíciles de configurar y más caprichosas. (Sección "¿Qué es Big Data?")

P: ¿Por qué aparece tan a menudo el nombre de fichero `part-m-00000` en HDFS? / R: Es una convención casi universal: el directorio es la salida de un único job distribuido y cada fichero es la salida de una parte paralela, almacenada en el nodo que la generó. (Sección "Usar HDFS")

P: ¿Qué ventaja y qué pega tiene usar HDFS directamente con un comando como `hadoop fs -cat ... | grep`? / R: Ventaja: sus comandos son muy rápidos y evitan la sobrecarga de las herramientas de análisis. Pega: todo se trae al nodo maestro y se procesa allí, no en paralelo; solo compensa con datasets pequeños. (Sección "Usar HDFS")

P: ¿Cuál es la diferencia entre lanzar un script con `spark-submit` y abrir el intérprete `pyspark`? / R: En el script creas explícitamente el `SparkContext`; el intérprete ya trae uno como `sc`. (Sección "Dos formas de ejecutar PySpark y configuración")

P: ¿Por qué puede fallar un job en modo clúster pero no en local? / R: En clúster Spark arranca un subproceso Python en cada nodo; si falta una librería o fichero en un nodo, ese proceso falla, de ahí la importancia de enviar los ficheros con `--py-files`/`--files`. (Secciones "Por dentro, trucos y escollos" y configuración)

P: En rendimiento de MapReduce, ¿qué importa más que el número de pasos del código? / R: El tráfico de datos entre nodos y cuántos pasos da el peor nodo; el job solo acaba cuando termina el último reduce. (Sección "Consideraciones de rendimiento")

P: ¿Qué es `SparkContext` y qué dos tipos de operaciones existen en Spark? / R: Es el punto de entrada al clúster (por convención `sc`). Las operaciones son métodos de `sc` que crean RDDs (p. ej. `parallelize()`) y métodos de RDD que devuelven otros RDDs o producen salida. (Sección "Visión general de Spark")

## Checklist

Puntos a dominar:

- Decidir cuándo usar o no Big Data: si cabe en una máquina o basta SQL, usa eso; combina Big Data con herramientas tradicionales (features con Big Data, análisis en local con Pandas).
- Manejar HDFS con sus comandos (`-ls`, `-copyFromLocal`, `-copyToLocal`, `-cat`, `-mv`, `-rm`, `-rmr`, `-appendToFile`) y reconocer la convención `part-m-00000`.
- Escribir un script PySpark con RDDs (`parallelize`, `map`, `flatMap`, `reduceByKey`) y lanzarlo con `spark-submit --master yarn-client` o `local`.
- Configurar la ejecución: `--name`, `--master`, `--py-files`, `--files`, `--num-executors` (por defecto 2), `--executor-cores` (por defecto 1), o fijarlo en `SparkConf`.
- Entender el interior de Spark: evaluación perezosa, `cache()` para reutilizar en RAM, `count()` para forzar creación y aflorar errores, y el coste del shuffle.
- Aplicar tácticas de depuración: depurar en local, usar `take()` para ver el formato, RDDs de diccionarios, guardar en pickle para reutilizar y separar las listas de `--files` por comas.
- Razonar en MapReduce: escribir mapper y reducer, filtrar lo antes posible, usar combiners cuando la operación sea conmutativa/asociativa y equilibrar la carga entre reductores.
- Usar `aggregateByKey` en lugar de `reduceByKey` cuando los agregados sean estructuras grandes y mutables.
