# Advanced Classifiers (Clasificadores avanzados) — Estudio

## Tarjetas de repaso

P: ¿Qué diferencia a los clasificadores avanzados de los básicos del capítulo anterior?
R: No pueden usarse como cajas negras: tienen mucha estructura interna que el usuario debe diseñar, muchos parámetros que ajustar y ninguna receta prefabricada; a cambio, son los más potentes que existen hoy.

P: ¿Qué dos familias de clasificadores avanzados trata el capítulo?
R: El deep learning (una clase amplia de redes neuronales de nueva generación) y las redes bayesianas.

P: ¿Qué librerías usa el libro para deep learning y para redes bayesianas?
R: Para deep learning, Keras como envoltorio amigable sobre Theano y TensorFlow; para redes bayesianas, PyMC.

P: ¿Qué es un perceptrón y qué es una red profunda?
R: El perceptrón es la red neuronal más simple, con una sola capa oculta; una red profunda es una red con varias capas ocultas.

P: ¿Qué es una capa "oculta"?
R: Todas las capas de neuronas anteriores a la última; sus nodos no son variables de entrada ni de salida etiquetadas.

P: ¿Qué es un tensor?
R: Coloquialmente, un array multidimensional de números sobre el que se hacen operaciones lineales; cada capa toma un tensor como entrada y produce un tensor como salida.

P: ¿Qué parte del cómputo de una capa es no lineal?
R: Casi todo son operaciones lineales (combinación lineal ponderada = multiplicar una matriz de pesos por el vector de entrada); la única parte no lineal es aplicar la activación, por ejemplo la sigmoid, a cada elemento.

P: ¿Qué hace una capa convolucional y qué es un kernel?
R: Tiene varios filtros que buscan patrones; cada filtro tiene un kernel (una pequeña matriz), que se desliza por la imagen tomando el producto escalar con los píxeles solapados; ese deslizamiento con paso fijo es la convolución.

P: ¿Para qué sirve una capa de aplanamiento (flattening)?
R: Convierte un tensor d-por-n en un tensor 1-D de longitud d*n con los mismos valores; es lineal y se necesita porque la entrada convolucional es 2-D pero la salida final suele ser 1-D.

P: ¿Qué hace la capa dropout y para qué sirve?
R: Reduce el overfitting: recibe un parámetro p y, en cada iteración de entrenamiento, pone a 0 una fracción aleatoria p de los valores antes de pasarlos a la siguiente capa.

P: ¿Qué aportan las redes recurrentes (RNN) frente a las redes vistas antes?
R: Una memoria primitiva: las capas recurrentes toman dos entradas, la salida de la capa anterior y la salida de la propia capa recurrente en el punto anterior, lo que las hace ideales para series temporales.

P: ¿Qué diferencia a una LSTM de una RNN básica?
R: Las LSTM recuerdan con claridad eventos seleccionados de un pasado lejano; en las RNN básicas la memoria decae con el tiempo.

P: ¿Qué representa una red bayesiana y quién define su topología?
R: Representa las dependencias entre variables como un grafo dirigido; el usuario elige la topología y el modelo probabilístico de cada dependencia, y los datos ajustan los parámetros.

P: En la regla de Bayes P(Y|D)=P(D|Y)·P(Y)/P(D), ¿qué papel tiene cada término?
R: P(Y) es el prior (confianza inicial, filosóficamente controvertido); P(D|Y) es donde está la "magia" y suele ser más fácil de modelar; P(D) es solo normalización que casi nunca hace falta calcular.

P: ¿Qué es MCMC y cuál es su problema principal?
R: Markov chain Monte Carlo es una secuencia de estimaciones θ_i que a lo largo del tiempo se muestrea de la distribución entrenada; su problema principal es la autocorrelación entre muestras sucesivas.

P: ¿Qué es el burn-in en MCMC?
R: Las primeras N muestras que se descartan, porque empezar en un punto improbable sesga las estadísticas.

## Preguntas de autoevaluación

P: ¿Por qué el autor advierte sobre las librerías usadas en este capítulo? (sección "Una nota sobre librerías")
R: Porque, a diferencia del resto del libro, no hay librerías estandarizadas: hay varias en competencia, son inmaduras, con mala documentación, bugs y APIs que cambiarán.

P: En el ejemplo con el dataset Iris, ¿qué efecto tuvo cambiar el número de neuronas de la capa oculta? (sección "Deep learning básico")
R: Con 10 neuronas el rendimiento oscilaba al azar entre corr. ~0,6 y valores cercanos a 0 o negativos; con 50 neuronas se estabilizaba en torno a 0,6, mostrando lo quisquillosas que son las redes.

P: ¿Por qué las redes convolucionales se consideran inspiradas en la neurología humana? (sección "Redes neuronales convolucionales")
R: Porque en las primeras etapas del procesamiento visual hay neuronas que detectan patrones primitivos en zonas concretas, y capas posteriores los combinan para detectar patrones cada vez más complejos.

P: ¿Por qué Keras espera un array de cuatro dimensiones para redes convolucionales 2-D en MNIST? (sección "Ejemplo: el dataset MNIST")
R: Por las dimensiones: qué punto de datos, el canal (uno en escala de grises, tres en color), y las filas y columnas de la imagen.

P: ¿En qué sentido las redes bayesianas son casi lo opuesto a las redes neuronales? (sección "Redes bayesianas")
R: La topología de la red bayesiana es un punto donde insertar conocimiento experto o intuición y puede diseccionarse para obtener insights; las redes neuronales son casi imposibles de interpretar.

P: ¿Por qué predecir con una red bayesiana requiere aproximaciones numéricas? (sección "Entrenamiento y predicción")
R: Porque los propios parámetros tienen una distribución de confianza, y clasificar implica promediar las predicciones sobre todas las configuraciones posibles ponderadas por la confianza, una integral muy complicada o imposible.

P: ¿Qué entrega PyMC en lugar de la función de confianza, y cómo se usa? (sección "Markov chain Monte Carlo")
R: Entrega muestras aleatorias de la distribución entrenada Θ, y la integral se estima sumando sobre esas muestras.

P: En el ejemplo con el dataset de viviendas de Boston, ¿qué relación causal modela el autor? (sección "Ejemplo con PyMC")
R: Que una mala educación (ratio alumno/profesor) eleva la criminalidad, que a su vez reduce el precio de la vivienda; descarta 30.000 simulaciones de burn-in y usa las siguientes 40.000.

## Puntos a dominar

- Entender por qué el deep learning y las redes bayesianas requieren diseñar estructura y ajustar parámetros a mano, sin recetas prefabricadas.
- Reconocer el papel de Keras (sobre Theano/TensorFlow) y PyMC como herramientas inmaduras elegidas por el autor.
- Distinguir perceptrón, red profunda, red convolucional y red recurrente (RNN/LSTM), y saber cuándo conviene cada una.
- Explicar qué es un tensor y por qué la mayor parte del cómputo de una red son operaciones lineales (matrices de pesos) con una activación no lineal.
- Describir la convolución con kernels y para qué sirven las capas de aplanamiento, dropout y pooling en el ejemplo de MNIST.
- Manejar la regla de Bayes y el papel del prior, de P(D|Y) y del término de normalización P(D).
- Comprender cómo una red bayesiana codifica dependencias como grafo dirigido y permite insertar intuición experta.
- Saber qué es MCMC, por qué la autocorrelación es su mayor problema y por qué se aplica burn-in.
