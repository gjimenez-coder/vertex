# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 14 — Data Engineering: MapReduce, Pregel, and Hadoop (Ingeniería de datos: MapReduce, Pregel y Hadoop)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo explica qué es MapReduce, de dónde viene y para qué sirve, con dos ingenieros invitados de Google como ponentes: David Crawshaw y Josh Wills (este último, después, director de data science en Cloudera). Rachel trabajó con ambos en el equipo de data science de Google+. Las autoras señalan que MapReduce se ha convertido en una palabra de moda —muchas ofertas de empleo exigen "saber Hadoop"— y que a menudo se pide sin entender para qué sirve, cuando no todos los problemas de data science lo necesitan.

La tesis central es que MapReduce (desarrollado en Google por Jeff y Sanjay, y luego replicado en código abierto como Hadoop) es la tercera categoría de algoritmos del libro: los de ingeniería e infraestructura para grandes volúmenes de datos, junto a los de machine learning y los de optimización. Como contraste, se describe Pregel, un algoritmo de Google para computación de grafos a gran escala.

Sales sabiendo qué es Big Data según David (datos que no caben en una sola máquina), por qué la tolerancia a fallos hace imposible programar miles de máquinas a mano, cómo MapReduce resuelve eso con dos funciones (mapper y reducer), qué cosas no encaja bien, y cómo encajan Hadoop, HDFS, Hive y el ecosistema de Cloudera en el flujo de trabajo de un data scientist.

## Experimento mental sobre privacidad médica (David)

Antes de MapReduce, David plantea el acceso a historiales médicos. Hay tensión: la privacidad protege (ser ateo se castiga con la muerte en algunos lugares), pero también cuesta vidas. Por falta de flujo de información entre urgencias y una clínica de salud mental cercana, se estima que morían uno o dos pacientes por semana en cierto pueblo. Preguntas que surgen: ¿cuánta privacidad es la adecuada en salud?, ¿quién debe acceder y en qué circunstancias?, ¿hasta qué punto podemos decidir por otros?

Para la persona concreta suele ser un problema de seguridad: no importa que alguien tenga tus datos, sino que puedan usarse contra ti o vincularse a ti. Anonimizar de verdad es dificilísimo: un estudio en *Nature*, "Unique in the Crowd" de Yves-Alexandre de Montjoye et al., sobre 1,5 millones de usuarios de móvil en Europa, mostró que bastaban cuatro puntos de referencia para identificar al 95 % de las personas (PDF p. 352). El capítulo menciona la filtración de Edward Snowden y el debate sobre la NSA, y sugiere trasladar esa conversación a empresas privadas como el broker de datos Acxiom.

## MapReduce y el problema de contar palabras (David)

David define Big Data como datos que no caben en una unidad de cómputo; es una definición evolutiva (el IRS ya tenía "Big Data" antes de los ordenadores). Hoy significa datos que no caben en un solo ordenador. No desaparecerá: aunque la capacidad de las máquinas crece exponencialmente, esas mismas máquinas generan datos, también de forma exponencial; son dos curvas que no se cruzarán pronto.

El ejemplo hilo conductor es hallar las palabras más frecuentes en una lista. Por inspección es trivial; con 10.000 o 10⁹ palabras no. El enfoque simple —listar y contar— escala hasta ~100 millones de palabras, limitado por memoria (hay que cargar las palabras dos veces). Se puede streamear desde disco con un *channel* (leer 100, procesar, leer otras 100), pero si todas las palabras son únicas el programa revienta igual. Con máquinas multinúcleo el cuello pasa a ser el ancho de banda, y ayuda comprimir y usar un *heap* de valores hasheados (un conjunto parcialmente ordenado de tamaño acotado donde se descartan los elementos minúsculos). Así se llega al orden de 10 billones de palabras en una máquina.

Con 10 máquinas (cada una con 1/10 de la entrada) se cuenta localmente y se envía a un "controlador" que suma; con 100, el "fan-in" rompe el ancho de banda y hace falta un árbol de controladores locales. Pero con 1.000 máquinas no funciona: alguna fallará. Si cada máquina tiene probabilidad ϵ de estar rota, con ϵ = 0,001 la probabilidad de que las 1.000 funcionen es (1−ϵ)¹⁰⁰⁰ ≈ 0,37, menos que una moneda al aire.

La respuesta es la tolerancia a fallos para trabajo distribuido: replicar la entrada (por defecto tres copias) en máquinas distintas, incrustar *checksums* para auditar errores, monitorizar con un controlador y reiniciar trabajo automáticamente, usando la capacidad sobrante para re-ejecutar. Como resume el texto: "las 10 primeras máquinas son fáciles; las 100 primeras, difíciles; las 1.000 primeras, imposibles" (PDF p. 355). Eso era así hasta hace unos ocho años; hoy David usa 10.000 máquinas con regularidad.

## Cómo funciona MapReduce (David)

En 2004 Jeff y Sanjay publicaron "MapReduce: Simplified Data Processing on Large Clusters". MapReduce es una plataforma que hace la tolerancia a fallos por ti: programar 1.000 máquinas pasa a ser más fácil que programar 100. Se escriben dos funciones:

- **Mapper**: toma cada dato y produce un par ordenado `(clave, valor)`.
- **Shuffle** (fan-in): el framework ordena las salidas y agrupa todas las claves iguales en un montón.
- **Reducer**: recibe cada montón y emite `(clave, nuevo valor)`, donde el nuevo valor es una agregación de los antiguos. La clave está en que un reducer maneja todos los valores de una clave fija.

Para contar palabras, cada palabra se emite como `("red", 1)`; tras el shuffle se juntan los `("red", 1, 1)` y el reducer suma, dando `("red", 2)`. Si hay más datos, se añaden más workers de map y reduce. MapReduce aplana la complejidad de trabajar con muchas máquinas, pero se abusa de él. Convertir un algoritmo en pasos de MapReduce suele ser poco intuitivo, y la distribución debe ser uniforme: si todas las palabras son iguales van a una sola máquina en el shuffle (Google lo resuelve con *CountSketch*, usando heaps de hash buckets en los mappers). Casi todo falla en el paso reduce por no uniformidad de los datos. Conviene hacerlo todo en una iteración; la optimización se hace casi toda en C++, afinando nanosegundos sobre petabytes.

## Otros ejemplos y límites de MapReduce (David)

El atributo clave de un problema apto para MapReduce es que los datos puedan repartirse entre máquinas y que cada una trabaje por separado, sin saber qué hacen las demás. Ejemplo de logs web con `{user_id, IP_address, zip_code, ad_they_saw, did_they_click}`: contar usuarios únicos que vieron anuncios por código postal y cuántos hicieron clic requiere **dos** MapReduces. El primero usa `{zip_code, user}` como clave para obtener clics e impresiones por usuario; el segundo usa el código postal como clave y emite `{1, ifelse(clicks>0)}` por usuario. Un paper de 2006 muestra que algoritmos de machine learning que calculan estadísticos suficientes o gradientes (expresables como suma sobre puntos) también encajan.

Qué no hace bien: algoritmos iterativos que usan la estimación recién calculada como entrada de la siguiente etapa (como los métodos de descenso de máxima pendiente). Es posible, pero exige arrancar muchas etapas del motor; enfoques más nuevos como **Spark** son más eficientes.

## Pregel (David)

Como contraste, Pregel es un algoritmo de Google para datos con estructura de grafo o red. Los nodos se comunican con los nodos a los que están conectados, y hay *aggregators* (nodos con acceso a la información de todos, que pueden sumar o promediar). La base son una serie de *supersteps* que alternan entre nodos que envían información a sus vecinos y nodos que la envían a los aggregators. Existe una versión de código abierto llamada **Giraph**.

## Josh Wills: ser data scientist y diseñar modelos

Josh (director de data science en Cloudera, antes en Google) abre con un experimento mental: construir un avión propulsado por humanos. El premio X de 1950 ($50.000) tardó 10 años en ganarse; los primeros equipos planificaban años y se estrellaban en segundos. El ganador cambió la pregunta: ¿cómo construir un avión que puedas rearmar en cuatro horas tras un choque? Iterando prototipos rápido, lo resolvió en seis meses. Lección: a veces resuelves el problema equivocado.

Observaciones de Josh sobre el oficio: un data scientist dedica el 90 % del trabajo a limpiar y preparar datos (ingeniería de datos); resuelve problemas más que buscar *insights*; empieza con un problema y algo que optimizar; paraleliza todo; y, más que ser listo, conviene aprender rápido corriendo experimentos. Sobre **abundancia frente a escasez**: la mayoría piensa en escasez y tira cosas; Josh lo guarda todo por investigación reproducible —puede re-ejecutar cualquier fase y, ante un error, no reinicia todo; además integra nuevas fuentes donde corresponda.

Los modelos acaban siendo máquinas de Rube Goldberg, mezclas de modelos con *hacks* acumulados; no es malo si funcionan. **Cuidado con la brecha** (*mind the gap*): lo que optimiza tu modelo no es lo que optimizas para el negocio. Las recomendaciones de amigos de Facebook no optimizan que aceptes amigos sino que pases más tiempo en la red (de ahí tantas personas atractivas del sexo opuesto). Igual en medicina: se estudia la eficacia del fármaco o el éxito de la cirugía, no el bienestar del paciente.

## Hadoop, Cloudera y flujo de trabajo (Josh)

En 2001 había dos opciones de almacenamiento, bases de datos y *filers*, comparadas en esquema, procesamiento, fiabilidad y coste (Tabla 14-1): las bases de datos tienen esquema estructurado y procesamiento intensivo donde residen los datos; los filers no tienen esquema ni procesamiento pero son fiables; ambos, caros a escala. Surge el indicador *return on byte* (valor extraído por byte frente a coste de almacenarlo; si la razón no supera 1, se descarta) y la ley económica del Big Data: ningún registro individual vale mucho, pero tenerlos todos es valiosísimo (índice web, recomendación, sensores, publicidad).

**Hadoop** es la versión de código abierto de GFS y MapReduce de Google (con orígenes en el proyecto Nutch y Yahoo!). Tiene dos componentes: **HDFS**, el filesystem distribuido basado en el de Google, con bloques de 64 MB a 256 MB replicados en varios nodos y un nodo maestro que detecta caídas; y MapReduce. Hadoop está en Java (Google usa C++) y su API no es agradable, pero con *Hadoop streaming* se puede escribir en Python, R u otros lenguajes. **Cloudera** —cofundada por Doug Cutting (creador de Hadoop) y Jeff Hammerbacher— es "como Red Hat para Hadoop": empaqueta el proyecto Apache, lo distribuye gratis y cobra por soporte. **Apache Hive** es un data warehouse sobre Hadoop con lenguaje tipo SQL.

Flujo de Josh, cuya unidad de análisis es el *record*: (1) usar Hive para construir registros con todo lo conocido de una entidad (MapReduce intensivo); (2) scripts de Python para procesarlos repetidamente, típicamente jobs map-only fáciles de paralelizar; (3) actualizar los registros al llegar datos nuevos. Prefiere formatos binarios compactos (Thrift, Avro, protocol buffers) sobre texto, y GitHub para código y metadatos, sin guardar archivos de datos grandes en Git. Para empezar: probablemente Hive analizando logs de usuarios, o construir un motor de recomendación con **Apache Mahout** y su motor de filtrado colaborativo **Taste** (los mismos algoritmos que Netflix y Amazon).

## Ideas clave

- MapReduce (Google, 2004; Hadoop es su versión open source) es un algoritmo de ingeniería de datos para volúmenes que no caben en una sola máquina; no todo problema lo necesita.
- Programar miles de máquinas a mano es inviable por fallos; MapReduce asume la tolerancia a fallos (replicación por tres, checksums, reinicio automático).
- Se escriben dos funciones: mapper, que emite `(clave, valor)`; y reducer, que agrega todos los valores de una clave fija, con un shuffle en medio.
- La distribución de claves debe ser uniforme; la mayoría de fallos ocurren en el reduce por datos no uniformes (Google lo mitiga con CountSketch).
- MapReduce no encaja bien con algoritmos iterativos (p. ej. descenso de gradiente); Spark resulta más eficiente ahí.
- Pregel (open source: Giraph) procesa grafos a gran escala mediante supersteps entre nodos vecinos y aggregators.
- Según Josh, el 90 % del trabajo es ingeniería de datos; guarda todo por reproducibilidad y vigila la brecha entre lo que optimiza el modelo y lo que importa al negocio.
- El ecosistema Hadoop incluye HDFS (bloques de 64–256 MB replicados), Hive (SQL sobre Hadoop), Mahout/Taste (recomendación) y Cloudera como empresa de soporte.
