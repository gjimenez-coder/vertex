# Fitting a Model to Data (Ajustar un modelo a los datos) — Estudio

## Tarjetas de repaso

P: ¿Qué es el modelado paramétrico (function fitting o parameter learning)? / R: Un enfoque en el que el analista fija de antemano la estructura del modelo (una función numérica parametrizada de los atributos) y la minería de datos calcula los mejores valores de los parámetros para el conjunto de entrenamiento.

P: ¿En qué se diferencia el modelado paramétrico de la inducción de árboles del capítulo 3? / R: En la inducción de árboles la estructura se descubre a partir de los datos; en el modelado paramétrico la estructura se fija y solo se aprenden los parámetros numéricos.

P: ¿Qué es un discriminante lineal? / R: Un clasificador que decide según el signo de una suma ponderada de los atributos; discrimina entre clases y su frontera es una combinación lineal de los atributos.

P: ¿Cómo se expresa el modelo lineal general? / R: `f(x) = w0 + w1x1 + w2x2 + ⋯`, donde `w0` es el intercepto y los pesos `wi` son los parámetros que ajusta la minería de datos.

P: ¿Cómo se interpreta la magnitud de un peso `wi` tras el aprendizaje? / R: Como la importancia del atributo: cuanto mayor, más importante; si está cerca de cero, el atributo suele poder ignorarse.

P: ¿Qué forma geométrica tiene la frontera de un discriminante lineal según la dimensión? / R: En dos dimensiones es una recta, en tres un plano y en más dimensiones un hiperplano.

P: ¿Qué es una objective function (función objetivo) y por qué es clave? / R: Una función que representa la meta y puede calcularse para un conjunto de pesos y datos; se maximiza o minimiza para elegir los mejores parámetros entre las infinitas rectas posibles.

P: ¿Qué distingue conceptualmente a regresión lineal, regresión logística y SVM? / R: Comparten la misma estructura de modelo lineal; la diferencia esencial es la función objetivo (y la loss function) que cada una optimiza.

P: ¿Qué es el margin en un SVM y cuál es su objetivo? / R: El margen es la distancia entre los bordes de la barra más ancha ajustada entre las clases; el objetivo del SVM es maximizar ese margen.

P: ¿Qué es la hinge loss? / R: La loss function del SVM: no penaliza a un ejemplo que no cruce el lado equivocado del margen, se vuelve positiva al cruzarlo y crece linealmente con la distancia.

P: ¿Qué mide la regresión lineal por mínimos cuadrados (least squares)? / R: Minimiza la suma o media de los cuadrados de los errores entre valores estimados y reales; su gran inconveniente es la sensibilidad a datos erróneos u outliers.

P: ¿Por qué no puede usarse `f(x)` directamente como probabilidad en regresión logística? / R: Porque `f(x)` va de –∞ a ∞ mientras una probabilidad va de 0 a 1; se modela a través de las log-odds, que sí van de –∞ a ∞.

P: ¿Qué función objetivo ajusta la regresión logística? / R: El maximum likelihood: se eligen los pesos que maximizan la suma de verosimilitudes de ver la clase real de cada ejemplo.

P: ¿Por qué el nombre "regresión logística" es un misnomer? / R: Produce una estimación numérica (log-odds) pero sobre un target categórico, por lo que en realidad es un modelo de estimación de probabilidad de clase, no de regresión.

P: ¿Cómo logran los modelos lineales representar funciones no lineales? / R: Incluyendo atributos más complejos (por ejemplo un término al cuadrado, kernels en SVM no lineales o capas en redes neuronales); el coste es un mayor riesgo de overfitting.

## Preguntas de autoevaluación

P1: ¿Por qué el capítulo afirma que hay que elegir una función objetivo y cómo se decide cuál es la "mejor" recta separadora? / R: Porque existen infinitas rectas que separan perfectamente el entrenamiento, cada una un modelo distinto; se define una función objetivo que represente la meta y se maximiza o minimiza, y los pesos solo son los mejores si esa función representa de verdad lo que se quiere lograr. (Sección "Optimizar una función objetivo")

P2: ¿Cómo tratan los SVM los puntos que quedan del lado equivocado cuando los datos no son linealmente separables? / R: La función objetivo penaliza cada punto proporcionalmente a su distancia a la frontera (hinge loss); el mejor ajuste equilibra un margen ancho con una penalización total baja, intentando cometer solo errores pequeños. (Sección "Support Vector Machines, brevemente")

P3: ¿Qué diferencia a la squared error de la hinge y la zero-one loss, y qué limitación tiene en clasificación? / R: La squared error penaliza proporcionalmente al cuadrado de la distancia y se usa sobre todo en predicción numérica; aplicada a clasificación también castiga puntos muy correctos, lo que suele desalinearla del objetivo de negocio. (Sección "Loss functions")

P4: ¿Cómo convierte la regresión logística la salida lineal en una probabilidad? / R: Modela las log-odds del evento con `f(x)` y despeja la función logística `p+(x) = 1 / (1 + e^(-f(x)))`, una curva sigmoide que comprime el valor al rango [0,1]; en la frontera la probabilidad es 0.5. (Sección "Estimación de probabilidad de clase y regresión logística")

P5: ¿En qué dos aspectos difieren la regresión logística y la inducción de árboles aun usando fronteras lineales? / R: (1) El árbol usa fronteras perpendiculares a los ejes porque selecciona un atributo a la vez, mientras el clasificador lineal combina todos los atributos y orienta la frontera libremente; (2) el árbol trocea el espacio recursivamente por tramos, mientras el lineal coloca una única superficie de decisión. (Sección "Ejemplo: regresión logística frente a inducción de árboles")

P6: ¿Para qué sirve la salida `f(x)` de un discriminante lineal más allá del sí/no? / R: Para ordenar instancias por su verosimilitud de pertenecer a la clase: `f(x)` vale cero en la frontera, es pequeño cerca y grande lejos en la dirección +, lo que basta para un marketing dirigido con presupuesto limitado. (Sección "Puntuación y ordenación de instancias")

P7: ¿Qué es una red neuronal según el capítulo y cómo se entrena? / R: Una "pila" de modelos simples donde cada capa aplica un modelo a las salidas de la capa inferior; toda la pila es una gran función numérica parametrizada y, elegida una función objetivo, un procedimiento de optimización halla a la vez los mejores parámetros de todos los modelos. (Sección "Funciones no lineales, SVM y redes neuronales")

P8: ¿Qué resultados obtuvieron regresión logística y árbol J48 sobre el Wisconsin Breast Cancer Dataset y qué advertencia hace el capítulo? / R: La regresión logística tuvo 6 errores sobre 569 casos (~98.9%) y el árbol J48 de 13 hojas un 99.1%; la diferencia es un solo error y ambas cifras se midieron sobre los mismos datos de construcción, por lo que la evaluación fiable se aborda en capítulos posteriores. (Sección "Ejemplo: regresión logística frente a inducción de árboles")

## Puntos a dominar

- Distinguir modelado paramétrico (fijar estructura, aprender parámetros) de la inducción de árboles (descubrir estructura).
- Escribir e interpretar el discriminante lineal `f(x) = w0 + w1x1 + w2x2 + ⋯` y el significado geométrico de su frontera (recta/plano/hiperplano).
- Explicar que regresión lineal, regresión logística y SVM comparten el modelo lineal y se diferencian por su función objetivo y su loss function.
- Relacionar cada loss function con su uso: hinge loss (SVM), squared error (least squares/regresión), zero-one loss.
- Describir el objetivo del SVM: maximizar el margen y penalizar los puntos del lado equivocado por su distancia.
- Reconstruir la cadena de la regresión logística: probabilidad → odds → log-odds → `f(x)` → función logística/sigmoide, ajustada por maximum likelihood.
- Justificar por qué "regresión logística" es un misnomer (estimación de probabilidad de clase sobre target categórico).
- Comparar regresión logística y árboles en cuanto a forma de la frontera y comprensibilidad para los stakeholders.
- Entender cómo los atributos complejos (kernels, capas) permiten modelos no lineales y por qué elevan el riesgo de overfitting.
