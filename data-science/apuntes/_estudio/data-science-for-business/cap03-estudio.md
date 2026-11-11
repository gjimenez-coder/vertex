# Introduction to Predictive Modeling: From Correlation to Supervised Segmentation — Estudio

## Tarjetas de repaso

P: ¿Qué es la segmentación supervisada (supervised segmentation)?
R: Dividir la población en subgrupos con valores del target distintos entre grupos y similares dentro de cada grupo, usando variables conocibles para predecir el target.

P: ¿Qué hace que un atributo sea informativo?
R: Que reduzca la incertidumbre sobre el valor del target; tener un target convierte esa búsqueda en encontrar variables que correlacionan con él.

P: ¿Qué es un modelo en data science y qué tipos predictivos se distinguen?
R: Una representación simplificada de la realidad creada para un propósito; se distinguen modelos de clasificación (y estimación de probabilidad de clase) y de regresión.

P: ¿En qué se diferencian el modelado predictivo y el descriptivo?
R: El predictivo estima el valor desconocido del target; el descriptivo busca comprender el fenómeno subyacente y se juzga en parte por su inteligibilidad.

P: ¿Qué significa "predecir" en data science?
R: Estimar un valor desconocido, que puede estar en el futuro, el presente o el pasado, no solo pronosticar el futuro.

P: ¿Qué es la model induction y cómo se llama su procedimiento?
R: Crear modelos generalizando de casos específicos a reglas generales (estadísticas); el procedimiento es el algoritmo de inducción o learner, que usa training data etiquetados.

P: ¿Qué mide la entropía (Ecuación 3-1)?
R: El desorden o impureza de un conjunto respecto a los valores del target; va de 0 (conjunto puro) a 1 (clases balanceadas 50/50 con dos clases).

P: ¿Qué mide el information gain (Ecuación 3-2)?
R: Cuánto reduce la entropía toda la segmentación que crea un atributo; pondera cada hijo por su proporción de instancias p(ci) respecto al parent.

P: ¿Cómo atiende el information gain las complicaciones de los splits?
R: No exige pureza absoluta, se aplica a cualquier número de hijos y pondera por el tamaño de los subconjuntos, evitando premiar el aislar un único ejemplo puro.

P: ¿Qué medida de impureza se usa para regresión (target numérico)?
R: La varianza; se busca la mayor reducción ponderada de varianza, lo que equivale a hallar variables más correlacionadas con el target.

P: ¿Qué es un classification tree o decision tree?
R: Una segmentación supervisada en forma de árbol donde cada hoja es un segmento con un valor del target, construida combinando varios atributos.

P: ¿Cómo funciona la tree induction?
R: Con un enfoque divide-and-conquer: elige el atributo que crea los subgrupos más puros y repite recursivamente sobre cada subgrupo hasta nodos puros o sin variables.

P: ¿Cómo se relaciona un árbol con un conjunto de reglas?
R: Cada camino de la raíz a una hoja, uniendo con AND las pruebas de atributos, produce una regla IF...AND...THEN; el árbol agrupa los prefijos comunes.

P: ¿Cómo estima probabilidades un probability estimation tree y qué problema tiene?
R: Por frecuencia en cada hoja, p = n/(n+m); las hojas con pocas instancias dan estimaciones demasiado optimistas, un caso de overfitting.

P: ¿Qué es la corrección de Laplace y para qué sirve?
R: Un suavizado p(c)=(n+1)/(n+m+2) que modera las hojas con pocas instancias; al crecer n converge a la estimación por frecuencia.

## Preguntas de autoevaluación

P: ¿Por qué los autores evitan la terminología estadística de variable "dependiente" e "independiente"?
R: Porque induce a error; lo esencial es que el target no se usa para predecirse a sí mismo, aunque sus valores pasados sí puedan incluirse como features. (Sección: Models, Induction, and Prediction)

P: En el ejemplo del dataset de hongos, ¿qué atributo tiene el mayor information gain y por qué?
R: ODOR, que reduce la entropía total a ~0.1 (IG = 0.96 − 0.1 = 0.86) porque muchos olores son completamente característicos del target. (Sección: Example: Attribute Selection with Information Gain)

P: ¿Por qué el orden de los atributos en el árbol puede no coincidir con el ranking global de information gain?
R: Porque, salvo la raíz, cada nodo se evalúa solo sobre las instancias que caen por encima de él, no sobre toda la población, así que el IG depende del subconjunto. (Sección: Example: Addressing the Churn Problem with Tree Induction)

P: ¿Por qué una simple clasificación puede fallar cuando una clase es rara, y qué se usa en su lugar?
R: Porque todos los segmentos pueden tener probabilidad < 0.5 y etiquetarse igual; se usan probabilidades por segmento, que difieren y sirven para rankear y reducir el riesgo. (Sección: Probability Estimation)

P: ¿Qué forma tienen las fronteras de decisión de un árbol en el instance space y por qué?
R: Son perpendiculares al eje de la variable probada (horizontales o verticales en 2D) porque cada nodo prueba una sola variable contra un valor fijo; en n dimensiones imponen un hyperplane de n−1 dimensiones. (Sección: Visualizing Segmentations)

P: ¿Qué exactitud logró el árbol en el problema de churn y qué dos preguntas plantea ese resultado?
R: 73% de exactitud; plantea si se confía en ese número (se repetiría con otra muestra) y si 73% basta para que el modelo sea útil, retomadas en los Capítulos 7 y 8. (Sección: Example: Addressing the Churn Problem with Tree Induction)

P: ¿Por qué la tree induction es tan popular en la práctica a pesar de no ser siempre la más precisa?
R: Porque los árboles son fáciles de entender e implementar y baratos de computar, y su valor está en que pueden explicarse a stakeholders no expertos. (Sección: Summary)

## Puntos a dominar

- Distinguir modelado predictivo (estimar el target) de descriptivo (comprender el fenómeno) y clasificación de regresión.
- Entender la inducción como generalización de datos a reglas, y el uso del modelo como deducción probabilística.
- Calcular e interpretar la entropía (Ecuación 3-1) y el information gain (Ecuación 3-2), incluyendo la ponderación por tamaño de los hijos.
- Saber que la medida de impureza para regresión es la reducción de varianza.
- Reconstruir mentalmente la tree induction como proceso recursivo divide-and-conquer que elige el atributo más informativo en cada subgrupo.
- Traducir un árbol a su conjunto equivalente de reglas IF...AND...THEN.
- Aplicar la estimación de probabilidad por hoja p=n/(n+m) y la corrección de Laplace p=(n+1)/(n+m+2), entendiendo su relación con el overfitting.
- Recordar que, salvo la raíz, cada atributo se evalúa solo sobre las instancias que llegan a su nodo.
