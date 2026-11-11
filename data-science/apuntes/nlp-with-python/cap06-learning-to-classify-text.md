# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 6 — Learning to Classify Text (Aprender a clasificar texto)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

El capítulo trata la clasificación supervisada de texto: cómo elegir la etiqueta correcta para una entrada a partir de rasgos (features) observables del lenguaje. Responde a tres preguntas: cómo identificar rasgos relevantes, cómo construir modelos que ejecuten tareas de procesamiento de lenguaje automáticamente, y qué nos enseñan esos modelos sobre el lenguaje mismo.

La tesis central es que patrones observables —estructura y frecuencia de las palabras— se correlacionan con aspectos del significado (tiempo verbal, tema), y que un clasificador entrenado sobre corpus etiquetados puede aprender esas correlaciones. El esquema común es: un extractor de rasgos convierte cada entrada en un feature set; pares (feature set, etiqueta) alimentan un algoritmo de aprendizaje que produce un modelo; el mismo extractor convierte entradas nuevas que el modelo etiqueta.

Sales sabiendo construir y evaluar clasificadores con NLTK (identificación de género de nombres, clasificación de documentos, etiquetado gramatical, segmentación de oraciones, actos de diálogo, implicación textual), y entendiendo tres métodos de aprendizaje —árboles de decisión, naive Bayes y máxima entropía— además de las técnicas de evaluación (conjunto de prueba, exactitud, precisión y exhaustividad, matriz de confusión, validación cruzada).

## El ejemplo que recorre el capítulo

El hilo conductor es la identificación de género de nombres propios: nombres acabados en a, e, i tienden a ser femeninos; en k, o, r, s, t, masculinos. Partiendo de un único rasgo (la última letra) se construye, refina y evalúa un clasificador que reaparece al explicar árboles de decisión, entropía y naive Bayes.

## Clasificación supervisada

Clasificar es elegir la etiqueta correcta para una entrada de un conjunto de etiquetas definido de antemano; en la tarea básica cada entrada se considera aislada. Variantes: clasificación multiclase (varias etiquetas por instancia), de clase abierta (etiquetas no definidas de antemano) y de secuencia (varias entradas se clasifican conjuntamente). Un clasificador es supervisado si se construye a partir de corpus de entrenamiento que contienen la etiqueta correcta de cada entrada.

El primer paso es decidir qué rasgos de la entrada son relevantes y cómo codificarlos. El extractor devuelve un feature set, un diccionario que mapea nombres de rasgos a valores de tipos simples (booleanos, números, cadenas):

```python
def gender_features(word):
    return {'last_letter': word[-1]}
```

Con los nombres del corpus `names`, se construye una lista de ejemplos etiquetados, se dividen en train/test y se entrena un clasificador naive Bayes; `nltk.classify.accuracy` mide la exactitud (0.758) y `show_most_informative_features` revela los rasgos más informativos y sus razones de verosimilitud (likelihood ratios), p. ej. terminar en a es 38 veces más femenino que masculino. Para corpus grandes conviene `nltk.classify.apply_features`, que evita almacenar todos los feature sets en memoria.

Elegir y codificar bien los rasgos tiene un impacto enorme en la calidad del modelo. Los extractores se construyen por ensayo y error; es común empezar con un enfoque "de fregadero" (todo lo que se nos ocurra) y luego comprobar qué ayuda. Pero demasiados rasgos provocan overfitting: el algoritmo se apoya en idiosincrasias del entrenamiento que no generalizan, problema agravado con conjuntos pequeños. Un extractor con un rasgo por letra y recuentos resulta ~1% menos exacto que el de la última letra.

Para refinar rasgos se usa el análisis de errores. El corpus se divide en tres partes: conjunto de entrenamiento (construir el modelo), dev-test (análisis de errores) y conjunto de prueba (evaluación final). Es clave que el dev-test sea distinto del test: tras usar el dev-test para desarrollar el modelo ya no refleja fielmente el rendimiento sobre datos nuevos. Examinando los errores sobre el dev-test se observa, por ejemplo, que nombres acabados en *yn* son femeninos pese a que en *n* tienden a masculinos, y en *ch* masculinos pese a que en *h* tienden a femeninos. Añadir sufijos de dos letras sube la exactitud del dev-test de 76,5% a 78,2%. El procedimiento se repite cambiando la partición dev-test/train en cada vuelta.

Clasificación de documentos: con el Movie Reviews Corpus (reseñas positivas/negativas) se define un rasgo por cada una de las 2.000 palabras más frecuentes, indicando si el documento la contiene. El clasificador alcanza ~0,81 de exactitud; rasgos como `contains(outstanding)` indican reseña positiva y `contains(seagal)` negativa.

Etiquetado gramatical (POS): en lugar de un etiquetador de expresiones regulares hecho a mano, se entrena un clasificador que detecta qué sufijos son más informativos. Un árbol de decisión sobre sufijos del corpus Brown logra ~0,627 y puede imprimirse como pseudocódigo legible.

## Explotar el contexto y clasificación de secuencias

Mientras el extractor solo mire la palabra objetivo no puede usar el contexto, pero este aporta pistas potentes (saber que *fly* va tras *a* indica que es sustantivo). Para ello se pasa la oración completa sin etiquetar y el índice de la palabra, añadiendo rasgos como la palabra anterior. Con el contexto, el etiquetador POS mejora (~0,789). Aun así, no aprende generalizaciones como "tras un adjetivo probablemente hay un sustantivo", porque no accede a la etiqueta de la palabra previa: los clasificadores simples tratan cada entrada como independiente.

Para capturar dependencias entre tareas relacionadas se usan modelos de clasificador conjunto. La clasificación consecutiva (o voraz, greedy) halla la etiqueta más probable de la primera entrada y la usa para la siguiente, repitiendo hasta el final; así actuaba el bigram tagger. El extractor recibe un argumento `history` con las etiquetas ya predichas (solo las de palabras a la izquierda). Un `ConsecutivePosTagger` entrenado así alcanza ~0,798.

Limitación: cada decisión es definitiva y no puede corregirse después. Alternativas: la estrategia transformacional, que asigna etiquetas iniciales y las refina iterativamente reparando inconsistencias (el Brill tagger); y asignar puntuaciones a todas las secuencias posibles y elegir la de mayor puntuación, enfoque de los Hidden Markov Models. Como el número de secuencias es enorme (con 30 etiquetas, ~600 billones para 10 palabras), los HMM solo miran la(s) etiqueta(s) más reciente(s) y usan programación dinámica. Modelos más avanzados son los Maximum Entropy Markov Models y los Linear-Chain Conditional Random Fields.

## Más ejemplos de clasificación supervisada

Segmentación de oraciones: tarea de clasificación sobre la puntuación: ante un símbolo que podría cerrar oración (punto, interrogación), decidir si la termina. Con datos ya segmentados se arma una lista de tokens y un conjunto de índices frontera; los rasgos incluyen si la palabra siguiente va en mayúscula, la palabra previa y si esta tiene un solo carácter. El clasificador alcanza ~0,974.

Actos de diálogo: el NPS Chat Corpus (más de 10.000 posts etiquetados con 15 tipos como "Statement", "Emotion", "ynQuestion", "Continuer") permite clasificar el tipo de acto de nuevos mensajes usando como rasgos las palabras del post; exactitud ~0,66.

Reconocimiento de implicación textual (RTE): determinar si un texto T implica una hipótesis H (no implicación lógica, sino si un humano concluiría que T da evidencia razonable para H). Tratado como clasificación True/False, muchos enfoques tempranos lograron resultados razonables con análisis superficial basado en solapamiento de palabras. El extractor `RTEFeatureExtractor` arma bolsas de palabras de T y H quitando stopwords y calcula el solapamiento y las palabras de H ausentes de T (`hyp_extra`), distinguiendo palabras de entidades nombradas (nes), más significativas. El módulo `nltk.classify.rte_classify` supera por poco el 58% sobre los datos combinados de RTE.

Escalado a grandes conjuntos: Python es excelente para procesar texto y extraer rasgos, pero lento para los cálculos numéricos del aprendizaje automático frente a lenguajes como C. Con muchos datos o rasgos conviene usar las interfaces de NLTK hacia paquetes externos de machine learning.

## Evaluación

La evaluación compara las etiquetas que el modelo genera sobre un conjunto de prueba con las correctas; el test debe ser distinto del entrenamiento o un modelo que solo memoriza obtendría puntuaciones engañosamente altas. Hay un compromiso entre datos para probar y para entrenar: bastan ~100 instancias si las etiquetas son pocas y equilibradas, pero con muchas etiquetas o etiquetas raras conviene que la menos frecuente aparezca al menos 50 veces; es común reservar el 10%. Importa también la similitud entre test y desarrollo: cuanto más se parezcan, menos confianza en que los resultados generalicen. Barajar oraciones del mismo género (o del mismo documento) produce un test muy parecido al train; mejor extraer train y test de documentos distintos, o de géneros distintos (p. ej. entrenar en `news` y probar en `fiction`) para una evaluación más estricta.

La exactitud mide el porcentaje de entradas bien etiquetadas, pero hay que considerar la frecuencia de cada etiqueta: un 95% no impresiona si una clase domina el 95% de los casos. En tareas de búsqueda se usan cuatro categorías —verdaderos positivos, verdaderos negativos, falsos positivos (error de tipo I) y falsos negativos (error de tipo II)— y de ellas se definen: precisión = TP/(TP+FP); exhaustividad (recall) = TP/(TP+FN); F-Measure = media armónica (2·P·R)/(P+R).

Con tres o más etiquetas, la matriz de confusión es una tabla donde la celda [i,j] indica cuántas veces se predijo j siendo la correcta i; la diagonal son aciertos y lo demás errores. La validación cruzada divide el corpus en N pliegues (folds): para cada uno se entrena con el resto y se prueba sobre el pliegue, combinando las puntuaciones. Aporta una evaluación fiable sobre muchos datos y, además, muestra cuánto varía el rendimiento entre conjuntos de entrenamiento.

## Árboles de decisión

Un árbol de decisión es un diagrama de flujo que asigna etiquetas: nodos de decisión que comprueban un rasgo y nodos hoja que asignan etiquetas, empezando en el nodo raíz. Un decision stump es un árbol de un solo nodo basado en un único rasgo, con una hoja por valor posible. Para construirlo se elige un rasgo (por ejemplo el que da mayor exactitud) y se etiqueta cada hoja con la etiqueta más frecuente de sus ejemplos. Para crecer el árbol se toma el mejor stump global y se reemplazan las hojas poco exactas por nuevos stumps entrenados sobre el subconjunto que llega a esa hoja.

Para elegir el rasgo más informativo se usa la ganancia de información (information gain): mide cuánto se "organizan" los valores al dividirlos con un rasgo. Se parte de la entropía de las etiquetas —alta si hay etiquetas muy variadas, baja si predomina una—, definida como H = Σ P(l)·log2 P(l). Tras aplicar el stump se calcula la entropía media (ponderada) de las hojas; la ganancia es la entropía original menos esa entropía reducida. Se eligen los stumps de mayor ganancia.

Ventajas: son simples de entender e interpretar, sobre todo cerca de la raíz, y van bien con distinciones categóricas jerárquicas. Desventajas: cada rama divide los datos, de modo que los nodos inferiores disponen de poco entrenamiento y tienden al overfitting (se mitiga deteniendo la división o podando); fuerzan a comprobar rasgos en un orden fijo aunque actúen de forma independiente, obligando a repetir rasgos muy indicativos en muchas ramas; y aprovechan mal los rasgos que son predictores débiles, pues quedan muy abajo donde ya escasean los datos. Naive Bayes supera esta limitación dejando que todos los rasgos actúen "en paralelo".

## Clasificadores naive Bayes

Cada rasgo contribuye a decidir la etiqueta. El clasificador calcula primero la probabilidad previa (prior) de cada etiqueta según su frecuencia en el entrenamiento, y luego combina la contribución de cada rasgo para obtener una estimación de verosimilitud por etiqueta; se asigna la de mayor verosimilitud. Cada rasgo "vota en contra" de las etiquetas con las que rara vez aparece: la puntuación se multiplica por P(f|label).

El modelo asume que cada entrada se genera eligiendo primero una etiqueta y luego cada rasgo de forma independiente de los demás (suposición de independencia o naive Bayes), lo que simplifica combinar contribuciones. Como P(features) es igual para toda etiqueta, basta maximizar la verosimilitud de la etiqueta P(features, label) = P(label) · ⊓ P(f|label).

Conteos cero y suavizado: estimar P(f|label) como count(f,label)/count(label) falla si un rasgo nunca aparece con una etiqueta, anulando su verosimilitud. Que no se haya visto una combinación no la hace imposible; por eso se aplican técnicas de suavizado (smoothing): la Expected Likelihood Estimation suma 0,5 a cada conteo y la Heldout Estimation usa un corpus reservado (módulo `nltk.probability`). Rasgos no binarios: los de valor categórico se convierten en binarios ("color-is-red"); los numéricos mediante binning o modelando su distribución (p. ej. gaussiana).

El nombre "naive" viene de la irreal suposición de independencia. Si los rasgos están correlacionados, el clasificador los "cuenta por partida doble" y se desplaza hacia una etiqueta más de lo justificado (p. ej. `ends-with(a)` y `ends-with(vowel)`). El origen es que las contribuciones se calculan por separado en el entrenamiento pero se combinan al clasificar.

## Clasificadores de máxima entropía

Usan un modelo similar a naive Bayes, pero en vez de fijar los parámetros con probabilidades buscan, mediante técnicas de optimización iterativa, el conjunto de parámetros que maximiza la verosimilitud total del corpus. No hay fórmula directa por las interacciones entre rasgos; la optimización inicia con valores aleatorios y los refina acercándose al óptimo, lo que puede tardar mucho. El libro recomienda evitar GIS e IIS por lentos y preferir Conjugate Gradient (CG) y BFGS.

El modelo generaliza al de naive Bayes, pero deja al usuario decidir qué combinaciones de rasgos y etiquetas reciben parámetro propio (joint-features), pudiendo asociar un rasgo a varias etiquetas o varios rasgos a una. El principio de máxima entropía dice: entre las distribuciones consistentes con lo que sabemos, elegir la de mayor entropía (la que menos suposiciones no justificadas hace), reproduciendo a la vez la frecuencia empírica de cada joint-feature.

Generativos vs. condicionales: naive Bayes es generativo (modela P(input, label)) y puede responder preguntas como cuál es la entrada más probable; máxima entropía es condicional (modela P(label|input)) y solo responde cuál es la etiqueta más probable y su probabilidad. Los generativos son más potentes pero tienen más parámetros libres que entrenar con datos fijos, así que un condicional puede ser mejor en sus dos preguntas propias.

## Modelando patrones lingüísticos

Los clasificadores crean modelos explícitos que capturan patrones del lenguaje y hacen predicciones sobre datos nuevos. Algunos modelos son transparentes (árboles de decisión), otros opacos (redes neuronales multicapa). Distinción clave: los modelos descriptivos capturan patrones de los datos pero no explican por qué (p. ej. *absolutely adore* sí, *definitely adore* no); los explicativos postulan propiedades y relaciones causales (concepto de "adjetivo polar"). La mayoría de modelos construidos automáticamente de un corpus son descriptivos: dicen qué rasgos son relevantes, no las relaciones causales.

## Ideas clave

- Clasificar es elegir la etiqueta correcta de una entrada; el esquema supervisado encadena extractor de rasgos → algoritmo de aprendizaje → modelo.
- La elección y codificación de rasgos es determinante; demasiados provocan overfitting, sobre todo con corpus pequeños.
- Divide el corpus en tres: entrenamiento (construir), dev-test (análisis de errores y ajuste de rasgos) y prueba (evaluación final, con datos nunca usados antes).
- Evalúa con exactitud teniendo en cuenta la frecuencia de etiquetas; en búsqueda usa precisión, exhaustividad y F-Measure; la matriz de confusión y la validación cruzada aportan fiabilidad.
- Los árboles de decisión son interpretables pero manejan mal la interacción de rasgos y los predictores débiles; la ganancia de información (basada en la entropía) guía su construcción.
- En naive Bayes cada rasgo contribuye independientemente combinando prior y P(f|label); requiere suavizado para conteos cero y sufre doble conteo con rasgos correlacionados.
- La máxima entropía usa optimización iterativa para hallar pesos que maximizan la verosimilitud, eligiendo la distribución de mayor entropía consistente con lo conocido.
- Naive Bayes es generativo (P(input, label)) y máxima entropía condicional (P(label|input)); la mayoría de modelos de corpus son descriptivos, no explicativos.
