# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 7 — Interlude: Feature Extraction Ideas (Interludio: ideas para extracción de características)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF (PDF p. N). Se conservan solo los fragmentos de código esenciales.

## Lo que necesitas saber
Antes de entrar en técnicas concretas de machine learning, el autor retoma la extracción de características (feature extraction). La tesis es directa: un análisis de machine learning solo será tan bueno como las características que le introduzcas. Las mejores características reflejan con cuidado aquello que estudias, así que necesitarás aportar mucha experiencia de dominio (domain expertise) a tus problemas.

Este interludio no pretende ser exhaustivo, sino repasar los "usual suspects": formas clásicas de extraer características que sirven en una amplia variedad de contextos y que, como mínimo, conviene considerar. Sales sabiendo un catálogo de características estándar, cómo agregar datos cuando hay varias filas por entidad, un adelanto de métodos más sofisticados y, sobre todo, la idea de que a veces la característica más importante que extraes es la que intentas predecir.

## Standard Features (características estándar)
El capítulo enumera tipos clásicos de extracción de características junto con sus consideraciones prácticas:

- **Is_null**: una de las más simples y sorprendentemente efectivas. Consiste en registrar si la entrada original falta. Muchas veces el valor es nulo por una razón importante: quizá no se recogieron datos de ciertos widgets de una fábrica concreta, o con humanos faltan datos demográficos porque algunos grupos los reportan menos.

- **Dummy variables**: una variable categórica toma un número finito de valores (una columna de estado de EE. UU. tiene 50 valores posibles). Una dummy variable es binaria e indica si la columna categórica tiene un valor concreto. También se llama one-hot encoding, porque cada fila tendrá un 1 en exactamente una de las dummy variables. Dos problemas grandes:
  a) Puede haber muchísimas categorías, algunas muy raras. Lo típico es fijar un umbral, crear dummies solo para los valores más comunes y una dummy adicional que valga 1 para todo lo demás.
  b) A menudo solo conoces los valores posibles mirando los datos de entrenamiento, y luego deberás extraer las mismas dummies de otros datos (quizá de prueba). Necesitas un protocolo para entradas no presentes en el entrenamiento.

- **Ranks**: forma contundente de corregir outliers en una columna: ordenar los valores y usar sus rangos ordinales. Dos problemas grandes:
  a) Es un cálculo costoso, pues hay que ordenar toda la lista, y no puede hacerse en paralelo si los datos están distribuidos en un clúster.
  b) Los rangos dan problemas con datos de prueba/entrenamiento. Si clasificas todos los puntos antes de dividir, la información del conjunto de prueba queda implícita en el de entrenamiento: un error grave. Un apaño es dar a cada punto de prueba el rango que habría tenido en el entrenamiento, pero es computacionalmente caro.

- **Binning**: ambos problemas de los rangos se abordan eligiendo varios bins de histograma de tamaño parecido donde colocar los datos. Por ejemplo, un bin para lo que esté por debajo del percentil 25, otro para el 25 al 50, etc. En vez de un rango percentil, solo dices en qué bin cae cada punto. El inconveniente es que pierdes la resolución fina de los rangos percentiles.

- **Logarithms**: es común tomar el logaritmo de un número bruto y usarlo como característica. Amortigua los grandes outliers y realza los valores pequeños. Si los datos contienen ceros, lo habitual es sumar 1 antes de tomar el logaritmo.

## Features That Involve Grouping (características con agrupación)
A menudo un dataset incluye varias filas para una sola entidad que describimos. Por ejemplo, una fila por transacción con una columna que indica el cliente, pero queremos extraer características sobre los clientes. En estos casos hay que agregar de algún modo las filas de cada cliente. Varias métricas agregadas de fuerza bruta:

- El número de filas.
- La media, mínimo, máximo, mean, mediana, etc., de una columna concreta.
- Si una columna no es numérica, el número de entradas distintas que contiene.
- Si una columna no es numérica, el número de entradas idénticas a la entrada más común.
- La correlación entre dos columnas diferentes.

## Preview of More Sophisticated Features (adelanto de características más sofisticadas)
Muchos capítulos avanzados del libro tratan métodos más elaborados. Una lista rápida de los más interesantes:

- Si tu punto de datos es una imagen, puedes extraer alguna medida de cuánto se parece a otra imagen. La forma clásica es el Principal Component Analysis (PCA). También funciona para arrays numéricos de datos de series temporales o mediciones de sensores.
- Puedes hacer clustering de tus datos y usar el cluster de cada punto como característica categórica.
- Si los datos son texto, puedes extraer la frecuencia de cada palabra. El problema es que suele dar demasiadas características, por lo que puede hacer falta un método adicional para condensarlas.

## Defining the Feature You Want to Predict (definir la característica a predecir)
A veces extraes la característica más importante de todas: la que usas machine learning para predecir. El autor da ejemplos de su propia carrera:

- Tuvo que predecir el tráfico humano a un conjunto de sitios web, pero los logs estaban contaminados por bots. Filtrar ese tráfico y estimar su correspondencia con humanos reales se convirtió en un problema aparte. Lo resolvieron comparando su estimación con la de Google en unos pocos sitios: a veces por encima, a veces por debajo, pero concluyeron que coincidía lo suficiente para seguir.
- Ha estudiado el customer "churn" (cuando los clientes se van a la competencia). La "ground truth" intuitiva es un sentimiento de lealtad en la mente del cliente, y hay que estimarlo a partir de su comportamiento de compra. Es difícil distinguir el churn del cliente que simplemente no necesita tus servicios durante un tiempo.
- Al predecir eventos a partir de series temporales, a menudo hay que predecir si un evento es inminente en cierto momento. Esto exige decidir cuán lejos en el futuro puede estar antes de considerarse "imminent". Alternativamente, puedes usar un valor continuo del tiempo hasta el próximo evento, topándolo en un máximo para evitar outliers (o tomar su logaritmo, que también los amortigua).

## Ideas clave
- Un análisis de machine learning solo es tan bueno como las características que le das; la experiencia de dominio es decisiva.
- `Is_null` captura por qué falta un dato y suele ser sorprendentemente útil.
- Las dummy variables (one-hot encoding) exigen gestionar categorías raras y valores no vistos en el entrenamiento.
- Ranks corrigen outliers pero son costosos y arriesgan filtrar información de prueba al entrenamiento; el binning es una alternativa más barata a costa de resolución.
- El logaritmo amortigua outliers; suma 1 antes si hay ceros.
- Cuando hay varias filas por entidad, se agregan con métricas como conteo, media, mínimo, máximo, mediana, entradas distintas o correlaciones.
- Métodos avanzados: PCA para imágenes/series, clustering como feature categórica, frecuencia de palabras para texto.
- A veces la característica más difícil de extraer es la variable objetivo que quieres predecir.
