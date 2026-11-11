# Capítulo 14 — Data Engineering: MapReduce, Pregel, and Hadoop — Estudio

## Tarjetas de repaso

P: ¿Qué es Big Data según David? / R: Datos que no caben en una sola unidad de cómputo; hoy, datos que no caben en un solo ordenador. Es una definición evolutiva (el IRS ya tenía "Big Data" antes de los ordenadores).

P: ¿Por qué no desaparecerá el Big Data? / R: Aunque la capacidad de las máquinas crece exponencialmente, esas mismas máquinas generan datos también de forma exponencial; son dos curvas que no se cruzarán pronto.

P: ¿Qué es MapReduce y de dónde viene? / R: Un algoritmo/plataforma de ingeniería de datos desarrollado en Google por Jeff y Sanjay (paper de 2004 "MapReduce: Simplified Data Processing on Large Clusters"), para volúmenes que no caben en una sola máquina; Hadoop es su versión de código abierto.

P: ¿Qué hace el mapper? / R: Toma cada dato y produce un par ordenado `(clave, valor)`.

P: ¿Qué hace el reducer? / R: Recibe cada montón de valores de una clave fija (tras el shuffle) y emite `(clave, nuevo valor)`, donde el nuevo valor es una agregación de los antiguos.

P: ¿Qué es el shuffle (fan-in) en MapReduce? / R: El paso del framework que ordena las salidas de los mappers y agrupa todas las claves iguales en un mismo montón antes del reduce.

P: ¿Cómo logra MapReduce la tolerancia a fallos? / R: Replicando la entrada (por defecto tres copias) en máquinas distintas, incrustando checksums para auditar errores, monitorizando con un controlador y reiniciando el trabajo automáticamente con la capacidad sobrante.

P: ¿Por qué es inviable programar 1.000 máquinas a mano? / R: Alguna fallará: con probabilidad ϵ = 0,001 de fallo por máquina, que las 1.000 funcionen tiene probabilidad (1−ϵ)¹⁰⁰⁰ ≈ 0,37, menos que una moneda al aire.

P: ¿Dónde fallan casi todos los jobs de MapReduce y por qué? / R: En el paso reduce, por no uniformidad de los datos; si todas las claves son iguales van a una sola máquina en el shuffle (Google lo mitiga con CountSketch usando heaps de hash buckets en los mappers).

P: ¿Qué tipo de algoritmos no encaja bien con MapReduce? / R: Los iterativos que usan la estimación recién calculada como entrada de la siguiente etapa (p. ej. descenso de máxima pendiente/gradiente); Spark resulta más eficiente ahí.

P: ¿Qué es Pregel? / R: Un algoritmo de Google para datos con estructura de grafo o red; los nodos se comunican con sus vecinos y con aggregators, mediante una serie de supersteps. Su versión de código abierto es Giraph.

P: ¿Qué es "mind the gap" (cuidado con la brecha) según Josh? / R: Que lo que optimiza tu modelo no es lo que optimizas para el negocio (p. ej. las recomendaciones de amigos de Facebook optimizan tiempo en la red, no que aceptes amigos).

P: ¿Qué es Hadoop y cuáles son sus dos componentes? / R: La versión de código abierto de GFS y MapReduce de Google (orígenes en Nutch y Yahoo!); sus componentes son HDFS (filesystem distribuido) y MapReduce.

P: ¿Qué es HDFS? / R: El filesystem distribuido de Hadoop, basado en el de Google, con bloques de 64 MB a 256 MB replicados en varios nodos y un nodo maestro que detecta caídas.

P: ¿Qué es "return on byte"? / R: Un indicador que compara el valor extraído por byte frente al coste de almacenarlo; si la razón no supera 1, se descarta el dato.

## Preguntas de autoevaluación

P: ¿Hasta qué escala funciona el enfoque simple de listar y contar palabras, y qué lo limita? / R: Escala hasta ~100 millones de palabras, limitado por memoria (hay que cargar las palabras dos veces). (Sección "MapReduce y el problema de contar palabras")

P: Al escalar el conteo de palabras a muchas máquinas, ¿qué pasa con 10, con 100 y con 1.000 máquinas? / R: Con 10 se cuenta localmente y un controlador suma; con 100 el fan-in rompe el ancho de banda y hace falta un árbol de controladores locales; con 1.000 no funciona porque alguna fallará: "las 10 primeras son fáciles; las 100 difíciles; las 1.000 imposibles". (Sección "MapReduce y el problema de contar palabras", PDF p. 355)

P: ¿Por qué el ejemplo de logs web (usuarios únicos por código postal y sus clics) necesita dos MapReduces? / R: El primero usa `{zip_code, user}` como clave para obtener clics e impresiones por usuario; el segundo usa el código postal como clave y emite `{1, ifelse(clicks>0)}` por usuario. (Sección "Otros ejemplos y límites de MapReduce")

P: ¿Cuál es el atributo clave de un problema apto para MapReduce? / R: Que los datos puedan repartirse entre máquinas y que cada una trabaje por separado, sin saber qué hacen las demás. (Sección "Otros ejemplos y límites de MapReduce")

P: ¿Qué mostró el estudio "Unique in the Crowd" sobre anonimización? / R: Sobre 1,5 millones de usuarios de móvil en Europa, bastaban cuatro puntos de referencia para identificar al 95 % de las personas. (Sección "Experimento mental sobre privacidad médica", PDF p. 352)

P: ¿Qué lección deja el experimento del avión propulsado por humanos de Josh? / R: Que a veces resuelves el problema equivocado: el ganador cambió la pregunta hacia cómo rearmar el avión en cuatro horas tras un choque e iteró prototipos rápido, resolviéndolo en seis meses. (Sección "Josh Wills: ser data scientist y diseñar modelos")

P: Según Josh, ¿en qué consiste la mayor parte del trabajo de un data scientist y qué hace con los datos? / R: El 90 % es limpiar y preparar datos (ingeniería de datos); adopta la abundancia frente a la escasez y lo guarda todo por investigación reproducible, para re-ejecutar cualquier fase sin reiniciar todo ante un error. (Sección "Josh Wills: ser data scientist y diseñar modelos")

P: ¿Qué son Cloudera, Hive y Mahout/Taste en el ecosistema Hadoop? / R: Cloudera es "como Red Hat para Hadoop" (empaqueta Apache, lo distribuye gratis y cobra por soporte); Hive es un data warehouse sobre Hadoop con lenguaje tipo SQL; Mahout es una librería de recomendación con motor de filtrado colaborativo Taste. (Sección "Hadoop, Cloudera y flujo de trabajo")

## Puntos a dominar

- Definir Big Data como datos que no caben en un solo ordenador y explicar por qué el problema persiste (dos curvas exponenciales).
- Explicar por qué los fallos hacen inviable programar miles de máquinas a mano y cómo MapReduce asume la tolerancia a fallos (replicación por tres, checksums, reinicio automático).
- Describir el flujo mapper → shuffle → reducer con el ejemplo de conteo de palabras `("red", 1)` → `("red", 2)`.
- Reconocer la necesidad de distribución uniforme de claves y que la mayoría de fallos ocurren en el reduce (mitigación con CountSketch).
- Identificar qué problemas encajan en MapReduce (datos repartibles, trabajo independiente) y cuáles no (algoritmos iterativos; alternativa: Spark).
- Explicar Pregel (supersteps, nodos vecinos, aggregators) y su versión open source Giraph como contraste para grafos.
- Aplicar las observaciones de Josh: 90 % ingeniería de datos, abundancia frente a escasez, modelos como máquinas de Rube Goldberg y "mind the gap".
- Situar los componentes del ecosistema Hadoop: HDFS (bloques de 64–256 MB replicados), MapReduce, Hive, Cloudera, Mahout/Taste, return on byte y la ley económica del Big Data.
- Recordar el flujo de Josh centrado en el *record*: Hive para construir registros, scripts Python map-only para procesarlos, y actualización al llegar datos nuevos; formatos binarios (Thrift, Avro, protocol buffers) y GitHub sin datos grandes.
