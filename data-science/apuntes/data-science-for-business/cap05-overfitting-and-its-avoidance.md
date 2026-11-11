# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 5 — Overfitting and Its Avoidance (El sobreajuste y cómo evitarlo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo trata uno de los conceptos fundamentales de la ciencia de datos: el sobreajuste (overfitting) y su contraparte, la generalización. Si damos a una búsqueda de patrones suficiente flexibilidad, siempre encontraremos patrones en un conjunto de datos; pero esos "patrones" pueden ser meras casualidades que no se repiten en datos nuevos. Generalizar es predecir bien sobre instancias no observadas; sobreajustar es ajustar el modelo a los datos de entrenamiento a costa de esa generalización.

La tesis central es que existe un compromiso fundamental entre la complejidad del modelo y la posibilidad de sobreajuste. Todos los procedimientos de minería de datos sobreajustan en algún grado, y no hay una fórmula mágica que lo elimine. Por eso la mejor estrategia no es evitar los modelos complejos, sino reconocer el sobreajuste y gestionar la complejidad de forma principiada.

Sales sabiendo cómo detectar el sobreajuste (datos de reserva, fitting graphs, learning curves), cómo estimar la generalización con validación cruzada, y cómo controlar la complejidad en árboles (poda, criterios de parada) y en funciones matemáticas (selección de atributos, regularización). También aprendes que el sobreajuste es, en el fondo, un problema de comparaciones múltiples.

## El ejemplo que recorre el capítulo

El hilo conductor es la predicción de abandono (churn) de clientes de MegaTelCo. El capítulo arranca con un "modelo de tabla" extremo que memoriza a los clientes que abandonaron: acierta el 100% sobre los datos históricos, pero sería inútil en producción porque cualquier cliente nuevo no estará en la tabla y se le predeciría "0% de abandono". Este caso ilustra el sobreajuste llevado al límite: memorización pura sin ninguna generalización.

## Generalización y sobreajuste

La generalización es la propiedad de un modelo (o de un proceso de modelado) por la cual el modelo se aplica a datos que no se usaron para construirlo. Todo conjunto de datos es una muestra finita de una población; queremos modelos que sirvan para la población general, no solo para el conjunto de entrenamiento exacto. En el modelo de tabla los datos eran representativos, pero el modelado no produjo generalización alguna.

El sobreajuste es la tendencia de los procedimientos de minería de datos a adaptar los modelos a los datos de entrenamiento a expensas de la generalización a datos nuevos. Como resume la cita atribuida a Ronald Coase: "If you torture the data long enough, it will confess" (PDF p. 137). El problema es insidioso: no basta con usar un procedimiento que no sobreajuste (todos lo hacen) ni con elegir siempre modelos menos complejos, porque a veces se necesita más complejidad para capturar la complejidad real de la aplicación. No existe una sola elección que elimine el sobreajuste.

## Examen del sobreajuste: datos de reserva y fitting graphs

Para reconocer el sobreajuste se introduce un concepto esencial: los datos de reserva (holdout data). El error del modelo de tabla fue evaluarlo con los mismos datos con los que se construyó. Evaluar sobre datos de entrenamiento no mide la generalización. En su lugar se "aparta" una parte de los datos con el valor del objetivo conocido pero que no se usa para construir el modelo: es como un "test de laboratorio" de la generalización. A estos datos de reserva se les suele llamar conjunto de prueba (test set), y la precisión sobre entrenamiento ("in-sample") difiere de la precisión de generalización estimada sobre ellos.

El fitting graph muestra la precisión del modelo en función de su complejidad, con dos curvas: una sobre datos de entrenamiento y otra sobre datos de reserva. Cuando el modelo no es lo bastante complejo, es poco preciso; a medida que crece en complejidad, parece muy preciso en entrenamiento pero empieza a sobreajustar, y la precisión de entrenamiento se separa de la de generalización. Para el modelo de tabla de churn, al aumentar las filas permitidas el error de entrenamiento baja hasta cero (cuando la tabla contiene todo el conjunto, marcado como N), pero el error de prueba arranca en un valor *b* y nunca baja. Esa brecha es señal clara de memorización.

La tasa base (base rate): como el modelo de tabla predice "sin abandono" para todo caso nuevo, acierta todos los casos de no-abandono y falla todos los de abandono; su tasa de error es el porcentaje de casos de abandono en la población. Un clasificador que siempre elige la clase mayoritaria es un clasificador de tasa base. El equivalente en regresión es un modelo que siempre predice la media o la mediana del objetivo.

## Sobreajuste en árboles y en funciones matemáticas

En la inducción de árboles, si seguimos dividiendo los datos hasta que las hojas son puras, construimos en esencia una tabla de consulta: precisión perfecta en entrenamiento, pero con riesgo de sobreajuste. Los árboles pueden representar cualquier función de los atributos si se les deja crecer sin límite, y su complejidad reside en el número de nodos. El fitting graph típico muestra que, al principio, precisión de entrenamiento y de reserva mejoran juntas; a partir de cierto punto (el "sweet spot", en torno a 100 nodos en el ejemplo) el árbol capta detalles del entrenamiento que no son propios de la población y la precisión de reserva decae. Ese valor no es universal: depende del dataset y del algoritmo, y no hay forma teórica de hallarlo, por lo que se recurre a técnicas empíricas.

En las funciones matemáticas, una forma de ganar complejidad es añadir más variables (atributos), cada una con su peso aprendido wi; incluso se pueden añadir versiones no lineales de atributos existentes (por ejemplo x4 = x1² o x5 = x2/x3). Con más dimensiones se puede ajustar perfectamente conjuntos cada vez mayores de puntos arbitrarios. De ahí que los modeladores poden cuidadosamente los atributos; la selección manual es sensata cuando hay pocos atributos y esfuerzo humano disponible, pero en aplicaciones modernas (miles de modelos semanales, millones de posibles features, como en la publicidad display dirigida) solo cabe la selección automática de atributos.

El ejemplo del iris lo ilustra: con dos atributos (ancho de pétalo y de sépalo), regresión logística y máquinas de vectores de soporte (SVM) trazan fronteras casi idénticas. Al añadir un único punto atípico, la regresión logística mueve mucho su frontera para separar perfectamente, mientras que la SVM apenas se mueve: la SVM incorpora control de complejidad y es menos sensible a ejemplos individuales. Al añadir el cuadrado del ancho de sépalo, ambas pueden crear fronteras curvas (parábolas): más libertad para ajustar, pero también más oportunidad de sobreajustar.

## Por qué el sobreajuste es perjudicial

Al crecer en complejidad, el modelo puede recoger correlaciones espurias: idiosincrasias del conjunto de entrenamiento concreto que no representan a la población. En el ejemplo de dos clases con atributos x e y, solo x tiene poder predictivo (acierto máximo del 75%), pero en una muestra pequeña y parece predecir por azar. Un árbol divide también por y y clasifica mejor el entrenamiento (7 de 8 frente a 6 de 8), pero esa rama espuria es dañina: en la población general eleva el error esperado del 25% al 30%. El fenómeno no es exclusivo de los árboles (todos los modelos lo sufren), no se debe a datos sesgados (toda muestra finita tiene variación) y no hay forma analítica de saber de antemano si un modelo ha sobreajustado: en la práctica hace falta un conjunto de reserva para detectarlo.

## De la evaluación con reserva a la validación cruzada

Un único conjunto de reserva da una sola estimación de la generalización, que puede ser una elección afortunada o desafortunada de datos. La validación cruzada (cross-validation) es un procedimiento más sofisticado que, además de la estimación, aporta estadísticas como la media y la varianza del rendimiento, clave para confiar en la estimación, y aprovecha mejor un dataset limitado. Se divide el conjunto etiquetado en k particiones (folds), típicamente cinco o diez; en cada iteración un fold distinto hace de prueba y los k–1 restantes de entrenamiento. Así cada ejemplo se usa una vez para prueba y k–1 para entrenamiento, y al final se promedian las k estimaciones y se calcula su desviación.

Un recuadro advierte que el laboratorio de modelado no captura toda la complejidad del mundo real: si los datos de entrenamiento y reserva no coinciden con los datos de despliegue, el rendimiento cae. Ocurre con la publicidad dirigida y con el credit scoring, donde los datos provienen solo de clientes previamente seleccionados. Conviene recordar la idea de tratar los datos como un activo en el que invertir.

Al revisar el dataset de churn con validación cruzada de diez folds, los árboles de clasificación bajan del 73% previo a un 68,6% de media (había sobreajuste), con desviación de 1,1; la regresión logística da 64,1% de media con desviación de 1,3. En este dataset los árboles son preferibles por su mayor estabilidad y rendimiento, aunque esto no es absoluto.

## Learning curves

Una learning curve representa el rendimiento de generalización (solo sobre datos de prueba) frente a la cantidad de datos de entrenamiento. Suele ser empinada al inicio y luego aplanarse, pues el beneficio marginal de más datos decrece. Se diferencia del fitting graph: el fitting graph muestra rendimiento de entrenamiento y de generalización frente a la complejidad (con datos fijos); la learning curve muestra solo generalización frente al tamaño de datos. En el churn, con datos pequeños la regresión logística generaliza mejor (menos flexible, sobreajusta menos), pero al crecer los datos las curvas se cruzan y el árbol, más flexible, capta relaciones no lineales y acaba siendo más preciso. La curva también orienta la inversión: si se ha aplanado, más datos no compensan y conviene mejorar las features; si sigue subiendo, obtener más datos puede ser buena inversión.

## Evitar el sobreajuste y controlar la complejidad

Para evitar el sobreajuste se controla la complejidad del modelo. En árboles se usan dos estrategias: (i) detener el crecimiento antes de que sea demasiado complejo y (ii) dejarlo crecer y luego podarlo (prune). El método más simple para limitar el tamaño es exigir un número mínimo de instancias por hoja, lo que hace que el árbol crezca donde hay muchos datos y se recorte donde hay pocos. ¿Qué umbral usar? No hay número fijo; una alternativa estadística es aplicar un test de hipótesis en cada hoja, basado en un p-valor (umbral habitual del 5%), para decidir si la ganancia de información observada no se debe al azar. La poda consiste en sustituir hojas y ramas por hojas cuando hacerlo no reduce la precisión, iterando sobre subárboles.

El método general: construir modelos de distintas complejidades y elegir el de mejor generalización estimada. Como el conjunto de prueba debe permanecer independiente, se vuelve a dividir el entrenamiento en un subconjunto de subentrenamiento y un conjunto de validación (nested holdout testing). Se elige la complejidad con la validación y, una vez elegida, se reconstruye el modelo con todo el conjunto de entrenamiento. A menudo se usa nested cross-validation: dentro de cada fold se corre otra validación cruzada para fijar el parámetro de complejidad C. Con 5-fold en ambos niveles se llegan a construir 30 modelos; esta práctica solo se generalizó en la última década por su coste computacional. La misma idea sirve para elegir el conjunto de features, por ejemplo con sequential forward selection (SFS), que añade features de una en una hasta que dejan de mejorar la validación (y su inversa, sequential backward elimination).

Para funciones numéricas, el control de complejidad elegante es la regularización: en vez de optimizar solo el ajuste a los datos, se optimiza una combinación de ajuste y simpleza, añadiendo a la función objetivo una penalización por complejidad ponderada por λ:

```
arg max  fit(w, D) − λ · penalty(w)
   w
```

La penalización más común es la suma de los cuadrados de los pesos (norma L2), que castiga pesos de gran valor absoluto. Con L2 en mínimos cuadrados se obtiene la ridge regression; con la suma de valores absolutos (norma L1, L1-regularization) se obtiene el lasso, que pone a cero muchos coeficientes y realiza así selección automática de atributos. La SVM lineal es casi equivalente a una regresión logística regularizada con L2, salvo que usa hinge loss en vez de verosimilitud. El parámetro λ se elige, como el tamaño del árbol o el conjunto de features, mediante nested cross-validation sobre el entrenamiento; este barrido de valores se conoce como grid search.

Un recuadro advierte sobre las comparaciones múltiples: si se prueban muchas alternativas y se eligen solo las que "se ven bien" (como quedarse con el mejor de 1.000 fondos de inversión escogidos al azar), la significancia es dudosa. En el fondo, el sobreajuste es un problema de comparaciones múltiples; incluso los procedimientos para evitarlo las realizan. No hay bala de plata, pero los procedimientos de reserva y una inspección cuidadosa de los resultados (por ejemplo, confirmar que el fitting graph tiene forma de U invertida) reducen el riesgo.

## Ideas clave

- La minería de datos implica un compromiso fundamental entre complejidad del modelo y posibilidad de sobreajuste; todos los tipos de modelo pueden sobreajustar.
- No hay técnica única que elimine el sobreajuste: la mejor estrategia es reconocerlo probando con un conjunto de reserva (holdout).
- El fitting graph compara precisión de entrenamiento y de reserva frente a la complejidad; la curva de reserva suele tener forma de U (o U invertida) con un "sweet spot".
- La learning curve muestra el rendimiento de generalización frente a la cantidad de datos; orienta si conviene invertir en más datos o en mejores features.
- La validación cruzada divide el dataset en k folds y produce media y varianza del rendimiento, dando confianza y aprovechando mejor datos limitados.
- El control de complejidad en árboles se logra con criterios de parada (mínimo de instancias por hoja, test de hipótesis con p-valor) y con poda.
- La regularización optimiza ajuste más simpleza mediante una penalización ponderada por λ; L2 da ridge regression, L1 da lasso (con selección de atributos), y la SVM lineal equivale a logística regularizada con hinge loss.
- El sobreajuste es, en esencia, un problema de comparaciones múltiples: cuidado al probar muchas opciones y quedarse solo con las que lucen bien.
