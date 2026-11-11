# Learning to Classify Text (Aprender a clasificar texto) — Estudio

## Tarjetas de repaso

P: ¿Qué es clasificar en el contexto del capítulo?
R: Elegir la etiqueta correcta para una entrada a partir de un conjunto de etiquetas definido de antemano; en la tarea básica cada entrada se considera aislada.

P: ¿Qué cadena de componentes define el esquema de clasificación supervisada?
R: Un extractor de rasgos convierte cada entrada en un feature set; pares (feature set, etiqueta) alimentan un algoritmo de aprendizaje que produce un modelo que etiqueta entradas nuevas.

P: ¿Qué es un feature set?
R: Un diccionario que mapea nombres de rasgos a valores de tipos simples (booleanos, números, cadenas), devuelto por el extractor de rasgos.

P: ¿Qué es el overfitting y cuándo se agrava?
R: Cuando el algoritmo se apoya en idiosincrasias del entrenamiento que no generalizan; se agrava con demasiados rasgos y con conjuntos de datos pequeños.

P: ¿En qué tres partes se divide el corpus para refinar rasgos y por qué?
R: Entrenamiento (construir el modelo), dev-test (análisis de errores y ajuste de rasgos) y prueba (evaluación final); el dev-test debe ser distinto del test porque tras usarlo ya no refleja fielmente el rendimiento sobre datos nuevos.

P: ¿Qué es la ganancia de información (information gain)?
R: Mide cuánto se organizan las etiquetas al dividirlas con un rasgo; es la entropía original menos la entropía media ponderada de las hojas tras aplicar el stump. Se eligen los stumps de mayor ganancia.

P: ¿Cómo se define la entropía de las etiquetas?
R: H = Σ P(l)·log2 P(l); es alta si hay etiquetas muy variadas y baja si predomina una.

P: ¿Qué es un decision stump?
R: Un árbol de decisión de un solo nodo basado en un único rasgo, con una hoja por valor posible, etiquetada con la etiqueta más frecuente de sus ejemplos.

P: ¿En qué consiste la suposición "naive" de naive Bayes?
R: Que cada entrada se genera eligiendo primero una etiqueta y luego cada rasgo de forma independiente de los demás, lo que simplifica combinar contribuciones.

P: ¿Por qué naive Bayes necesita suavizado (smoothing)?
R: Porque estimar P(f|label) como count(f,label)/count(label) anula la verosimilitud si un rasgo nunca aparece con una etiqueta; el suavizado evita los conteos cero (p. ej. Expected Likelihood Estimation suma 0,5 a cada conteo).

P: ¿Qué problema causa el doble conteo en naive Bayes?
R: Si los rasgos están correlacionados, el clasificador los cuenta por partida doble y se desplaza hacia una etiqueta más de lo justificado (p. ej. ends-with(a) y ends-with(vowel)).

P: ¿Cómo encuentra sus parámetros un clasificador de máxima entropía?
R: Mediante técnicas de optimización iterativa que buscan el conjunto de parámetros que maximiza la verosimilitud total del corpus; el libro recomienda Conjugate Gradient (CG) y BFGS en lugar de GIS e IIS.

P: ¿Qué dice el principio de máxima entropía?
R: Entre las distribuciones consistentes con lo que sabemos, elegir la de mayor entropía (la que menos suposiciones no justificadas hace), reproduciendo la frecuencia empírica de cada joint-feature.

P: ¿Qué diferencia a un modelo generativo de uno condicional?
R: Naive Bayes es generativo (modela P(input, label)) y puede responder cuál es la entrada más probable; máxima entropía es condicional (modela P(label|input)) y solo responde cuál es la etiqueta más probable y su probabilidad.

P: ¿Qué distingue un modelo descriptivo de uno explicativo?
R: El descriptivo captura patrones de los datos pero no explica por qué; el explicativo postula propiedades y relaciones causales. La mayoría de modelos construidos de un corpus son descriptivos.

## Preguntas de autoevaluación

P: ¿Por qué la elección y codificación de rasgos es determinante, y qué riesgo trae añadir demasiados?
R: Tiene un impacto enorme en la calidad del modelo; demasiados rasgos provocan overfitting, apoyándose en idiosincrasias del entrenamiento que no generalizan, problema agravado con conjuntos pequeños. (Sección "Clasificación supervisada")

P: ¿Por qué el conjunto de prueba debe ser distinto del de entrenamiento?
R: Porque si no, un modelo que solo memoriza obtendría puntuaciones engañosamente altas; la evaluación debe compararse contra datos no usados para entrenar. (Sección "Evaluación")

P: ¿Por qué la exactitud por sí sola puede ser engañosa?
R: Porque depende de la frecuencia de cada etiqueta: un 95% no impresiona si una clase domina el 95% de los casos; por eso se usan precisión, exhaustividad y F-Measure. (Sección "Evaluación")

P: ¿Cuál es la limitación de la clasificación consecutiva (greedy) y qué alternativas existen?
R: Cada decisión es definitiva y no puede corregirse después; alternativas son la estrategia transformacional (Brill tagger) y puntuar todas las secuencias posibles eligiendo la mejor (Hidden Markov Models). (Sección "Explotar el contexto y clasificación de secuencias")

P: ¿Qué desventajas tienen los árboles de decisión frente a naive Bayes?
R: Cada rama divide los datos (poco entrenamiento abajo y overfitting), fuerzan a comprobar rasgos en un orden fijo repitiendo rasgos indicativos, y aprovechan mal los predictores débiles; naive Bayes deja que todos los rasgos actúen en paralelo. (Sección "Árboles de decisión")

P: ¿Cómo mejora el etiquetado POS al explotar el contexto y qué sigue sin poder aprender?
R: Pasando la oración completa y el índice de la palabra, añadiendo rasgos como la palabra anterior, la exactitud sube (~0,789); aun así no aprende generalizaciones como "tras un adjetivo probablemente hay un sustantivo" porque no accede a la etiqueta de la palabra previa. (Sección "Explotar el contexto y clasificación de secuencias")

P: En reconocimiento de implicación textual (RTE), ¿qué significa que T implique H y cómo se aborda?
R: No es implicación lógica, sino si un humano concluiría que T da evidencia razonable para H; se trata como clasificación True/False con análisis superficial basado en solapamiento de palabras (bolsas de palabras de T y H sin stopwords, hyp_extra y entidades nombradas). (Sección "Más ejemplos de clasificación supervisada")

P: ¿Por qué un clasificador condicional puede superar a uno generativo en sus propias preguntas?
R: Porque el generativo es más potente pero tiene más parámetros libres que entrenar con datos fijos, de modo que un condicional puede ser mejor en sus dos preguntas propias. (Sección "Clasificadores de máxima entropía")

## Puntos a dominar

- Explicar el esquema supervisado completo: extractor de rasgos → pares (feature set, etiqueta) → algoritmo de aprendizaje → modelo que etiqueta entradas nuevas.
- Distinguir las variantes de clasificación: multiclase, de clase abierta y de secuencia.
- Justificar la división en tres conjuntos (entrenamiento, dev-test, prueba) y el papel del análisis de errores sobre el dev-test.
- Reconocer y mitigar el overfitting (reducir rasgos; en árboles, detener la división o podar).
- Calcular e interpretar exactitud, precisión, exhaustividad (recall) y F-Measure, más la matriz de confusión y la validación cruzada.
- Diferenciar verdaderos/falsos positivos y negativos (error de tipo I y tipo II).
- Describir cómo se construye un árbol de decisión y el uso de la entropía y la ganancia de información para elegir rasgos.
- Explicar cómo naive Bayes combina prior y P(f|label), por qué necesita suavizado y cuándo sufre doble conteo.
- Contrastar naive Bayes (generativo) con máxima entropía (condicional) y el principio de máxima entropía.
- Separar modelos descriptivos de explicativos y reconocer que los modelos de corpus suelen ser descriptivos.
