# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 3 — Introduction to Predictive Modeling: From Correlation to Supervised Segmentation (Introducción al modelado predictivo: de la correlación a la segmentación supervisada)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Este capítulo entra de lleno en uno de los temas centrales de la minería de datos: el modelado predictivo, planteado como *supervised segmentation* (segmentación supervisada). La idea es dividir la población en grupos que difieren entre sí respecto a una cantidad de interés que queremos predecir o estimar (el *target*): quién va a abandonar la compañía (churn), qué cuentas han sido defraudadas, qué clientes dejarán deudas impagadas (write-offs), o en positivo, quién responderá a una oferta.

La tesis central es que predecir bien depende de encontrar atributos informativos: variables conocibles que reducen nuestra incertidumbre sobre el valor del target. Información es, en general, una cantidad que reduce la incertidumbre sobre algo. Tener un target concreto convierte esta búsqueda en una aplicación de la noción de correlación: buscamos atributos que correlacionen con el objetivo.

Sales sabiendo: los conceptos básicos del modelado predictivo; la noción fundamental de seleccionar atributos informativos con una técnica concreta (information gain basada en entropía); la idea de modelos en forma de árbol; y el proceso básico para inducir esos árboles desde los datos (tree induction). Seleccionar atributos informativos también sirve para reducir datasets demasiado grandes y, a menudo, para mejorar la precisión del modelo.

## Models, Induction, and Prediction (Modelos, inducción y predicción)
Un modelo es una representación simplificada de la realidad creada para un propósito; un mapa es un modelo del mundo físico que abstrae lo irrelevante y conserva lo importante. En data science, un modelo predictivo es una fórmula —matemática, lógica (una regla) o híbrida— para estimar el valor desconocido del target. Se distingue entre modelos de clasificación (y de estimación de probabilidad de clase) y modelos de regresión.

Terminología de predicción: en data science, predecir no es solo pronosticar el futuro, sino estimar un valor desconocido, que puede estar en el futuro, el presente o el pasado. Como la minería suele usar datos históricos, los modelos se construyen y prueban con eventos pasados (credit scoring, filtros de spam, detección de fraude).

El modelado predictivo contrasta con el modelado descriptivo, cuyo fin no es estimar un valor sino comprender el fenómeno subyacente (cómo son los clientes que abandonan). Un modelo descriptivo se juzga en parte por su inteligibilidad; un predictivo puede juzgarse solo por su desempeño, aunque la inteligibilidad sigue importando. La frontera no es estricta: muchas técnicas sirven para ambos fines.

Terminología básica (Figura 3-1, problema de clasificación supervisada): el aprendizaje supervisado crea un modelo que relaciona un conjunto de variables seleccionadas (*attributes* o *features*) con una variable predefinida, el *target*. Una *instance* o *example* es un punto de datos (una fila, un *feature vector*) descrito por atributos. Es clasificación cuando el target es una categoría (sí/no) y regresión cuando es un número.

Muchos nombres para lo mismo: los campos de origen (machine learning, estadística, bases de datos) usan términos distintos. La estadística habla de variables independientes o predictores (atributos de entrada) y de variable dependiente (el target). Los autores evitan esa terminología dependiente/independiente porque induce a error. Lo esencial: el target no se usa para predecirse a sí mismo, aunque valores pasados del target sí pueden incluirse como features.

La creación de modelos a partir de datos es la *model induction*: generalizar de casos específicos a reglas generales (estadísticas, que no se cumplen el 100% del tiempo). Al procedimiento se le llama algoritmo de inducción o *learner*. La inducción se contrasta con la deducción, que parte de reglas generales para crear hechos específicos; usar el modelo es una forma de deducción (probabilística). Los datos de entrada del algoritmo son los *training data* (datos etiquetados, porque se conoce el valor del target).

## Supervised Segmentation (Segmentación supervisada)
La idea intuitiva es segmentar la población en subgrupos con valores distintos del target entre grupos y similares dentro de cada grupo. Si la segmentación usa variables conocibles cuando el target no lo es, esos segmentos sirven para predecir y, además, ofrecen patrones comprensibles para humanos: "profesionales de mediana edad que residen en Nueva York tienen en promedio una tasa de churn del 5%". El concepto fundamental: ¿cómo juzgar si una variable contiene información importante sobre el target, y cuánta? Queremos seleccionar automáticamente las variables más informativas e incluso rankearlas.

## Selecting Informative Attributes (Selección de atributos informativos)
Con el ejemplo de doce figuras humanas (Figura 3-2) descritas por atributos head-shape, body-shape y body-color, y target binario write-off (Yes/No), se busca qué atributo segmenta mejor. Técnicamente queremos grupos lo más *puros* posible: homogéneos respecto al target. En datos reales casi nunca se logra pureza total, pero reducir la impureza ya permite construir un modelo predictivo (ofrecer crédito a segmentos con menor tasa de write-off).

Hay varias complicaciones: (1) los atributos rara vez dividen un grupo perfectamente; (2) un split que aísla un solo punto puro puede ser peor que otro que reduce la impureza más ampliamente; (3) no todos los atributos son binarios (¿cómo comparar splits de dos, tres o siete grupos?); (4) hay atributos numéricos (no tiene sentido un segmento por cada valor).

Para clasificación, la solución es una fórmula que evalúe cómo divide cada atributo. El criterio más común es *information gain*, basado en una medida de pureza llamada entropía, ambos de Claude Shannon (Shannon, 1948). La entropía mide el desorden de un conjunto respecto a las propiedades de interés (los valores del target): un segmento muy mezclado tiene entropía alta.

```
entropy = - p1 × log(p1) - p2 × log(p2) - ⋯        (Ecuación 3-1, log base 2)
```

Cada `pi` es la proporción de la propiedad `i`. La entropía va de 0 (desorden mínimo, conjunto puro) a 1 (desorden máximo, clases balanceadas al 50/50 en dos clases). Ejemplo: un conjunto S de 10 personas, 7 non-write-off y 3 write-off, da entropy(S) ≈ 0.88.

La entropía solo mide la impureza de un subconjunto. El *information gain* (IG) mide cuánto mejora (reduce) la entropía toda la segmentación que crea un atributo. Si el atributo tiene k valores, el conjunto original es el *parent* y los resultados son los k *children*:

```
IG(parent, children) = entropy(parent)
    - [ p(c1)×entropy(c1) + p(c2)×entropy(c2) + ⋯ ]   (Ecuación 3-2)
```

Cada hijo se pondera por su proporción de instancias p(ci), lo que resuelve la preocupación de aislar un único ejemplo puro. Ejemplo (Figura 3-4): parent con 16 puntos y 14 estrellas, entropy(parent) ≈ 0.99; al dividir por Balance en 50K, los hijos tienen entropía ≈ 0.39 y ≈ 0.79, con IG ≈ 0.37 (gran reducción). Un split alternativo por Residence (OWN, RENT, OTHER) da IG ≈ 0.13: menos informativo, porque RENT y OTHER no son más puros que el parent.

El information gain atiende todas las complicaciones: no exige pureza absoluta, se aplica a cualquier número de hijos y pondera por el tamaño de los subconjuntos. Los atributos numéricos se *discretizan* eligiendo puntos de corte y tratándolos como categóricos; conceptualmente se prueban todos los cortes razonables y se elige el de mayor IG. Para regresión (target numérico), la medida de impureza natural es la varianza: se busca la mayor reducción ponderada de varianza, lo que equivale a hallar variables más correlacionadas con el target.

## Example: Attribute Selection with Information Gain (Ejemplo: selección de atributos con information gain)
Se usa el dataset de hongos del repositorio de la UC Irvine (del *Audubon Society Field Guide*): 5.644 ejemplos (2.156 venenosos, 3.488 comestibles) descritos por una veintena de atributos discretos (Table 3-1) y target binario edible? (yes/no). La pregunta: ¿qué único atributo distingue mejor comestibles de venenosos? La entropía del dataset completo es 0.96 (ligeramente desbalanceado hacia comestibles).

Los gráficos de entropía (Figuras 3-6 a 3-9) muestran, en el eje x la proporción del dataset y en el y la entropía; el área sombreada representa la entropía total tras dividir por un atributo, y el objetivo es minimizarla. GILL-COLOR reduce algo la entropía; SPORE-PRINT-COLOR tiene valores (chocolate) que especifican perfectamente el target pero cubren poca población (~30%). ODOR tiene el mayor information gain: reduce la entropía total a ~0.1, es decir IG = 0.96 − 0.1 = 0.86. Muchos olores son completamente característicos: si se construyera un modelo de un solo atributo, habría que elegir ODOR.

## Supervised Segmentation with Tree-Structured Models (Segmentación supervisada con modelos de árbol)
La selección de un solo atributo no basta: queremos segmentos que combinen varios atributos. La solución elegante es un árbol (Figura 3-10, con la raíz arriba). Un árbol tiene nodos interiores (cada uno prueba un atributo, con una rama por valor) y nodos terminales u hojas. Cada punto de datos sigue un único camino hasta una hoja; cada hoja es un segmento, y los atributos y valores del camino definen sus características (p. ej. "personas mayores, desempleadas, con saldos altos"). Como cada hoja contiene un valor del target, el árbol es una segmentación supervisada; en clasificación se llama *classification tree* o *decision tree*.

Para clasificar un ejemplo nuevo se desciende desde la raíz eligiendo ramas según los valores del atributo hasta llegar a una hoja, que da la clase. Ejemplo: Claudio (Balance=115K, Employed=No, Age=40) se clasifica como Not Write-off siguiendo Employed=No → Balance>50K → Age<45. Existen también *probability estimation trees* (hojas con probabilidades) y *regression trees* (hojas con valores numéricos); la idea básica es la misma.

Hay muchas técnicas para inducir segmentaciones; una de las más populares es *tree induction*, porque los árboles son fáciles de entender, los procedimientos son elegantes y eficientes, y son robustos a problemas comunes de datos. La mayoría de paquetes de minería los incluyen.

La inducción de árboles usa un enfoque *divide-and-conquer*: parte del dataset completo y aplica selección de variables para crear los subgrupos más puros posibles; luego recursivamente repite sobre cada subgrupo (que es una versión menor del problema original). En el ejemplo de las figuras, se divide primero por body-shape (rectangular vs oval, Figura 3-11), después el grupo oval por head-shape (Figura 3-12) y el rectangular por body-color (Figura 3-13), hasta obtener grupos puros (Figura 3-14). Se detiene cuando los nodos son puros o no quedan variables; a veces conviene parar antes (overfitting, Capítulo 5).

## Visualizing Segmentations (Visualización de segmentaciones)
Visualizar cómo un árbol particiona el *instance space* (el espacio de las features) ayuda a entender los modelos, aunque solo se pueda ver en dos o tres dimensiones. A menudo es más fácil comparar familias de modelos por cómo parten el espacio que por su forma. En la Figura 3-15, el árbol prueba Balance en la raíz (línea vertical en 50K) y luego Age en 45 (línea horizontal solo en el lado Balance≥50K). Cada nodo de decisión es un corte del espacio y cada hoja una región sin dividir; al descender se consideran subregiones cada vez más focalizadas.

Las fronteras que separan regiones son *decision lines* (o superficies/boundaries). Como cada nodo prueba una sola variable contra un valor fijo, la frontera es perpendicular al eje de esa variable (horizontal o vertical en 2D). En n dimensiones, cada nodo impone un *hyperplane* de n−1 dimensiones; el término solo generaliza la idea de línea o plano.

## Trees as Sets of Rules (Árboles como conjuntos de reglas)
Un árbol equivale a un conjunto de reglas lógicas. Recorriendo un camino de la raíz a una hoja y uniendo con AND las pruebas de atributos se obtiene una regla, por ejemplo:

```
IF (Balance < 50K) AND (Age < 50) THEN Class=Write-off
```

Todo árbol de clasificación se expresa así; el árbol agrupa los prefijos comunes de las reglas hacia arriba. Que sea más legible el árbol o el conjunto de reglas es cuestión de preferencia.

## Probability Estimation (Estimación de probabilidad)
A menudo interesa más una probabilidad que una clasificación: en churn, estimar la probabilidad de que un cliente se vaya permite rankear prospectos o asignar un presupuesto limitado de incentivos a los de mayor probabilidad o mayor pérdida esperada. Además, los modelos de clasificación simple fallan cuando una clase es rara: en crédito, casi todo segmento tiene probabilidad de write-off < 0.5, así que todas las hojas se etiquetarían "not write-off"; aun así, las probabilidades por segmento difieren y sirven para reducir el riesgo.

La inducción de árboles produce fácilmente *probability estimation trees*: como las hojas son regiones de baja entropía, se usa el conteo de instancias para una estimación basada en frecuencia: si una hoja tiene n positivos y m negativos, p = n/(n+m). Problema: hojas con pocas instancias dan estimaciones demasiado optimistas (una hoja con un solo caso daría 100%), un ejemplo de *overfitting*. La solución es la corrección de Laplace, que suaviza:

```
p(c) = (n + 1) / (n + m + 2)
```

Así, una hoja con 2 positivos y 0 negativos pasa de p=1 a p=0.75, mientras que una con 20 positivos apenas cambia (p ≈ 0.95); al crecer n, Laplace converge a la estimación por frecuencia.

## Example: Addressing the Churn Problem with Tree Induction (Ejemplo: el problema de churn con tree induction)
Con datos históricos de 20.000 clientes de telefonía (variables de Table 3-2: COLLEGE, INCOME, OVERAGE, LEFTOVER, HOUSE, HANDSET_PRICE, etc., y target LEAVE), primero se mide el information gain individual de cada atributo (Figura 3-17). Los tres mejores son HOUSE (valor de la vivienda), LEFTOVER y LONG_CALLS_PER_MONTH; sorprendentemente, el uso del teléfono y la satisfacción reportada no son muy predictivos. Los IG aquí son mucho menores que en el dataset de hongos.

Al aplicar el algoritmo (Figura 3-18), HOUSE queda en la raíz (siempre se elige primero) y OVERAGE aparece alto, pero el orden del árbol no coincide con el ranking global: salvo la raíz, cada nodo se evalúa solo sobre las instancias que caen por encima de él, no sobre toda la población, así que el IG depende del subconjunto. No se discute aún cuándo parar de crecer el árbol (se difiere al Capítulo 5, overfitting).

El árbol logró 73% de exactitud sobre los datos (entrenado con mitad churners y mitad no). Esto plantea dos preguntas: ¿se confía en ese número (se repetiría con otra muestra)? y, si se confía, ¿73% es suficiente para que el modelo sea útil? Ambas se retoman en los Capítulos 7 y 8 sobre evaluación de modelos.

## Summary (Resumen)
El capítulo introdujo el modelado predictivo —construir un modelo que estime el valor del target para un ejemplo nuevo— y la noción fundamental de encontrar y seleccionar atributos informativos, que ya es un procedimiento útil por sí mismo (identificar variables que correlacionan con el objetivo, como las que informan sobre la probabilidad de churn). Una medida básica de información de atributos es el information gain, basado en la entropía; otra es la reducción de varianza (para regresión).

La selección de atributos informativos es la base de la tree induction, que recursivamente halla atributos informativos para subconjuntos de datos, segmentando el espacio de instancias en regiones similares de forma supervisada. El árbol resultante particiona todas las instancias posibles en segmentos con distintos valores predichos; con target binario (churn/no, write-off/no), cada hoja es un segmento con una probabilidad estimada de pertenencia a la clase. Como ejercicio, los autores proponen pensar qué cambiaría al construir un árbol de regresión en vez de clasificación.

Históricamente la tree induction es muy popular por ser fácil de entender e implementar y barata de computar; la investigación se remonta a los años 1950-60. Sistemas tempranos: CHAID (Kass, 1980) y CART (Breiman, Friedman, Olshen & Stone, 1984), aún muy usados; también C4.5 y C5.0 (Quinlan, 1986, 1993), y J48, reimplementación de C4.5 en Weka (Witten & Frank, 2000; Hall et al., 2001). En la práctica los árboles funcionan muy bien aunque no siempre sean lo más preciso; su valor está en que pueden entenderse y explicarse, lo que ayuda a comunicar resultados a stakeholders no expertos.

## Ideas clave
- El modelado predictivo se entiende como segmentación supervisada: dividir la población en grupos que difieren respecto a un target que se quiere predecir.
- Un atributo es informativo si reduce la incertidumbre sobre el target; tener un target convierte esa búsqueda en encontrar variables correlacionadas con él.
- Entropía (Ecuación 3-1) mide el desorden/impureza de un conjunto; va de 0 (puro) a 1 (clases balanceadas en el caso de dos clases).
- Information gain (Ecuación 3-2) mide cuánto reduce la entropía un atributo al segmentar, ponderando cada hijo por su tamaño; no exige pureza absoluta y admite cualquier número de valores. Para regresión se usa reducción de varianza.
- Un classification tree es una segmentación supervisada multivariada construida por tree induction, un proceso recursivo de divide-and-conquer que elige en cada paso el atributo que da los subgrupos más puros.
- Un árbol equivale a un conjunto de reglas IF...AND...THEN, una por cada camino raíz-hoja.
- Los probability estimation trees estiman p(c)=n/(n+m) por hoja; la corrección de Laplace p(c)=(n+1)/(n+m+2) modera las hojas con pocas instancias y mitiga el overfitting.
- En el árbol, salvo la raíz, cada atributo se evalúa solo sobre las instancias que llegan a su nodo, por lo que su orden puede no coincidir con el ranking global de information gain.
