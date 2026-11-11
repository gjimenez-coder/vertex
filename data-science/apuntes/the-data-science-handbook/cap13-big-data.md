# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 13 — Big Data (Big Data / Grandes volúmenes de datos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Big Data y data science se solapan pero no son lo mismo. Big Data designa varias tendencias en almacenamiento y procesamiento de datos que plantearon nuevos retos, oportunidades y soluciones, y que exigían un nivel de ingeniería de software que los estadísticos y analistas tradicionales no solían manejar. Esa demanda convirtió a "data scientist" en un título propio, pero el científico de datos moderno solo usa tecnologías de Big Data cuando son la herramienta adecuada.

Es un terreno donde las preocupaciones de ingeniería de bajo nivel pasan a primer plano: es fácil añadir horas al tiempo de ejecución o fallar por un error de memoria si no se vigila lo que ocurre dentro del computador. El capítulo repasa dos piezas clave —el sistema de ficheros Hadoop (HDFS) y el framework de cómputo en clúster Spark— y luego los conceptos de fondo del cómputo distribuido, en especial el paradigma MapReduce (MR).

Sales sabiendo qué es Big Data y cuándo (no) usarlo, cómo trabajar con HDFS, cómo escribir y configurar un script PySpark con RDDs, cómo funciona Spark por dentro (evaluación perezosa, caché, shuffle) y en qué consiste MapReduce con sus optimizaciones y consideraciones de rendimiento.

## ¿Qué es Big Data?

El término es algo engañoso: siempre ha habido datasets enormes (por ejemplo, los de aceleradores de partículas, procesados con hardware a medida) sin que se les diera un nombre especial. Big Data alude a tendencias en los datos y en las tecnologías para procesarlos. Los datasets suelen tener dos propiedades:

1) Son grandes. No hay un umbral fijo: ocurre cuando ya no es práctico almacenar o procesar todo en un solo computador y se recurre a un clúster (desde unos pocos hasta miles de nodos). El foco está en que el procesamiento sea escalable y distribuible en paralelo, con comunicación entre nodos reducida al mínimo.
2) Suelen ser "no estructurados". No significa sin estructura, sino que no encajan limpiamente en una base de datos relacional (SQL). Ejemplos: imágenes, PDFs, HTML, Excel desordenados, logs generados por máquinas. Las bases tradicionales exigen una estructura rígida a cambio de rendimiento optimizado; Big Data aporta flexibilidad para datos en cualquier formato, pero se paga caro en tiempo de ejecución porque hay pocas optimizaciones prefabricadas.

Advertencias del autor: desconfía de usar herramientas de Big Data por moda; casi siempre son más lentas, más difíciles de configurar y más caprichosas que sus equivalentes tradicionales. Si tus datasets caben en una sola máquina o solo necesitas operaciones de SQL, usa eso. Y aunque uses Big Data, conviene combinarlo con tecnologías tradicionales: el autor rara vez hace machine learning o visualización con Big Data; lo usa para extraer features, que ocupan mucho menos, y luego analiza en una máquina normal con algo como Pandas.

## Hadoop: el sistema de ficheros y el procesador

El campo moderno de Big Data arrancó cuando Google publicó su artículo sobre MapReduce. Doug Cutting escribió una implementación libre y de código abierto en Java (Google la hizo en C++) y la llamó Hadoop, por el elefante de peluche de su hija. Hadoop se volvió casi sinónimo de Big Data.

Tiene dos partes:

- HDFS (Hadoop Distributed File System): almacena datos en un clúster sin que te preocupes de qué dato está en qué nodo; te refieres a ubicaciones como en un sistema de directorios normal. Por debajo gestiona la distribución y mantiene copias por si falla algún nodo.
- El framework MR propiamente dicho, que lee de HDFS, procesa en paralelo y escribe en HDFS.

El autor apenas trata el MR de Hadoop porque hoy es "un dinosaurio": tiene mucha sobrecarga (lee de disco y escribe a disco, y el IO de disco es muy lento frente a RAM) e integra mal con lenguajes convencionales. La comunidad se ha movido hacia otras herramientas sobre HDFS, sobre todo Spark.

## Usar HDFS

Se accede por una interfaz de línea de comandos basada en bash. Comandos principales: `hadoop fs -ls`, `-copyFromLocal`, `-copyToLocal`, `-cat`, `-mv`, `-rm`, `-rmr` (borrado recursivo) y `-appendToFile`. Son austeros pero suficientes.

Muchos ficheros se llaman `part-m-00000`: convención casi universal. El directorio es la salida de un único job distribuido en varios nodos, y cada fichero es la salida de una parte paralela, almacenada en el nodo que la generó.

A veces conviene usar HDFS directamente en lugar de las herramientas de análisis, porque sus comandos son muy rápidos y evitan la sobrecarga. Por ejemplo, para extraer filas que contienen "boston" en un dataset pequeño:

```bash
hadoop fs -cat /my/dataset/* | grep boston > rows_containing_boston.csv
```

La pega: todo se trae al nodo maestro y se procesa allí (no es paralelo), pero si el dataset es pequeño puede ser mucho más rápido.

## Script de PySpark de ejemplo

PySpark es la forma más popular de que los usuarios de Python trabajen con Big Data: funciona como un shell de Python y, mediante la librería PySpark, conecta con Spark para paralelizar el cómputo. El script central del capítulo cuenta cuántas veces aparece cada palabra en un documento. Lo esencial:

```python
from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf=conf)

lines_rdd = sc.parallelize(open("myfile.txt"))
words_rdd = lines_rdd.map(clean_line).flatMap(lambda l: l.split())
counts = words_rdd.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
```

Se ejecuta en el clúster con `bin/spark-submit --master yarn-client myfile.py`, o en una sola máquina con `--master local`.

## Visión general de Spark

Spark es la tecnología de procesamiento líder en el ecosistema Hadoop y ha reemplazado al MR tradicional: es más eficiente (sobre todo encadenando operaciones) y mucho más fácil. Es una librería que importas desde Python o Scala; está escrito en Scala (va más rápido desde ahí), pero la API es casi idéntica en ambos. La interfaz Python se llama PySpark.

La abstracción central es el RDD (resilient distributed dataset): una colección de objetos Python distribuidos por el clúster. Es inmutable, pero sus métodos devuelven nuevos RDDs (p. ej. `X.map(f)`). Hay dos tipos: sin clave (operan elemento a elemento, como `map()`) y con clave. Un RDD con clave es uno de tuplas de dos elementos donde el primero es la clave y el segundo el valor; permite agrupar o unir, operaciones que requieren coordinación entre elementos. No son clases distintas: métodos como `reduceByKey` simplemente asumen pares clave–valor y fallan en tiempo de ejecución si no lo son.

La otra abstracción clave es `SparkContext` (por convención `sc`), punto de entrada al clúster. Las operaciones son de dos tipos: métodos de `sc` que crean RDDs (p. ej. `parallelize()`), y métodos de RDD que devuelven otros RDDs o producen salida.

La mayoría de operaciones son "perezosas" (lazy): al definir un RDD no se computa nada; Spark acumula una estructura de dependencias y solo cuando pides una salida (guardar en HDFS, traer a Python) se crean todos los RDDs en cascada. Por defecto un RDD es efímero. Para reutilizarlo, Spark puede cachearlo en la RAM de los nodos con `cache()` —gran diferencia frente al MR tradicional—. La evaluación perezosa también retrasa los errores: una función que falla solo lo revela cuando el RDD se fuerza; una táctica de depuración es llamar a `count()` tras declarar cada RDD (fuerza su creación y saca errores a la luz, aunque es caro y no debe quedar en código de producción).

## Operaciones de Spark

Métodos de `SparkContext`: `parallelize(lista)`, `textFile(ruta_hdfs)`, `pickleFile(ruta_hdfs)` (deserializa objetos picklados), `addFile(fichero)` y `addPyFile(libreria)` (copian ficheros/librerías a cada nodo).

Métodos de RDD más usados: `map(func)`, `filter(func)`, `flatMap(func)` (un elemento puede generar varios o ninguno), `take(5)` y `collect()` (este último solo si cabe en memoria de una máquina), `saveAsTextFile`, `saveAsPickleFile`, `distinct()`, `union(rdd2)`, `cache()`, `keyBy(func)`, `join(rdd2)` (sobre RDDs con clave), `reduceByKey(func)` y `groupByKey(func)`.

## Dos formas de ejecutar PySpark y configuración

Se puede lanzar un script autónomo (`bin/spark-submit --master yarn-client myfile.py`) o abrir un intérprete (`bin/pyspark --master yarn-client`). La diferencia clave: en el script creas explícitamente el `SparkContext`; el intérprete ya trae uno como `sc`. Los scripts suelen fijar muchos parámetros de configuración para que otros los ejecuten de forma fiable.

Los clústeres son delicados: hay que vigilar el nivel de paralelismo (demasiado puede ralentizar) y no acaparar recursos de un clúster compartido. Configuraciones desde línea de comandos: `--name` (nombre legible para monitorización), `--master` (`yarn-client` para paralelo, `local` por defecto), `--py-files` (librerías Python separadas por comas), `--files` (ficheros adicionales), `--num-executors` (por defecto 2) y `--executor-cores` (por defecto 1). Las mismas opciones pueden fijarse en el script sobre el objeto `SparkConf`.

## Por dentro, trucos y escollos

Puntos clave del funcionamiento interno: el comando `pyspark` ejecuta en realidad `python` enlazado a las librerías de Spark, así que tus librerías Python del nodo principal están disponibles. En modo clúster, Spark no ejecuta Python directamente: arranca un subproceso Python en cada nodo; si falta una librería o fichero en un nodo, ese proceso falla (de ahí la importancia de enviar los ficheros). Siempre que es posible, cada segmento de datos se confina a un proceso Python (operaciones como `map` o `flatMap` evitan tráfico de red). Mover datos entre nodos es muy costoso porque hay que serializar los objetos y rehidratarlos al otro lado; ese paso, en operaciones como `groupByKey()`, se llama "shuffle" y lo gestiona el framework Spark, no los procesos Python.

Trucos del autor: usar RDDs de diccionarios hace código y datos más comprensibles (convierte el CSV a diccionarios como primer paso); guardar en pickle en vez de texto si vas a reutilizar; usar `take()` para ver el formato de los datos al depurar; `count()` para forzar la creación y aflorar errores; depurar en modo local (más rápido y con menos fallos de configuración); si funciona en local pero falla en distribuido, revisa qué ficheros se envían; y separar las listas de `--files` por comas, no por dos puntos.

## El paradigma MapReduce

MapReduce es el paradigma más popular para Big Data: obliga a escribir el código de forma fácilmente paralelizable en un clúster de tamaño arbitrario. Subyace a muchas herramientas, incluido Spark. Un job MR toma un dataset (p. ej. un RDD) y tiene dos etapas:

- Mapping: cada elemento se mapea, mediante una función, a una colección de pares clave–valor (en PySpark, `flatMap`).
- Reducing: por cada clave única se lanza un proceso "reduce" que recibe sus valores asociados de uno en uno, en orden arbitrario, y produce salidas (en PySpark, `reduceByKey`).

El programador solo escribe el mapper y el reducer; no se preocupa del tamaño del clúster ni de dónde están los datos. Por debajo: los datos arrancan distribuidos; cada nodo aplica el mapper en paralelo; para cada clave se elige un nodo que hospeda el reduce; cada nodo reenvía sus pares a su reductor (ese movimiento de datos suele ser la etapa más lenta, incluso más que el procesamiento); y los reduce corren en paralelo. La optimización de que cada nodo condense localmente sus pares antes de enviarlos se llama "combiner", válida solo si la operación es conmutativa/asociativa (como la suma); reduce enormemente la presión sobre el ancho de banda.

## Consideraciones de rendimiento

Pautas para cualquier framework MR: filtra lo antes posible (reduce el ancho de banda); el job solo acaba cuando termina el último reduce, así que evita que un reductor acumule la mayoría de pares; más reductores significa menos pares por cada uno. En MR, lo importante no es el número de pasos del código, sino el tráfico de datos entre nodos y cuántos pasos da el peor nodo.

Optimización específica de Spark: `reduceByKey` es ineficiente cuando los valores agregados son estructuras grandes y mutables (p. ej. listas), porque crea listas nuevas en memoria una y otra vez y puede matar el job. La alternativa es `aggregateByKey`, que mantiene una lista y va añadiendo (`append`) sin recrearla: algo más compleja de usar pero mucho más eficiente.

## Ideas clave

- Big Data = datasets grandes y "no estructurados" más tecnologías de clúster; no uses sus herramientas por moda si una máquina y SQL te bastan.
- Suele combinarse con herramientas tradicionales: extrae features con Big Data y analiza en local con Pandas.
- Hadoop aporta HDFS (almacenamiento distribuido) y un MR ya anticuado; Spark lo ha reemplazado por eficiencia y facilidad.
- El RDD es la abstracción central de Spark: inmutable, distribuido, con variantes con y sin clave; `sc` es el punto de entrada.
- Spark evalúa de forma perezosa; `cache()` permite reutilizar RDDs en RAM y `count()` fuerza la creación para depurar.
- En modo clúster cada nodo corre un subproceso Python; hay que enviar librerías y ficheros, y el "shuffle" (serializar y mover datos) es costoso.
- MapReduce = mapear a pares clave–valor y reducir por clave; el programador solo escribe mapper y reducer.
- En rendimiento MR manda el tráfico de red y el peor nodo: filtra pronto, usa combiners y, para agregados mutables grandes, `aggregateByKey` en vez de `reduceByKey`.
