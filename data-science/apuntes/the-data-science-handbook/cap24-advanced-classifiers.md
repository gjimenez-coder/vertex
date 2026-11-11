# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 24 — Advanced Classifiers (Clasificadores avanzados)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página del PDF. Se conservan solo los fragmentos de código esenciales.

## Lo que necesitas saber

El capítulo profundiza en algoritmos de machine learning de vanguardia que, a diferencia de los clasificadores del capítulo anterior, no pueden usarse como cajas negras. Tienen mucha estructura interna que el usuario debe diseñar, numerosos parámetros que ajustar y ninguna receta prefabricada para tomar esas decisiones. A cambio del trabajo extra, se obtiene el tipo de clasificadores más potente que existe hoy, el que opera en el corazón de Google y Microsoft para tareas como reconocer personas en fotos, interpretar comandos de voz o decidir si una imagen es segura.

Se tratan dos familias: el deep learning (una clase amplia de redes neuronales de nueva generación, posibles gracias a avances en las técnicas numéricas de entrenamiento) y las redes bayesianas. El autor advierte que son temas profundos que los data scientists rara vez necesitan, por lo que la cobertura es relativamente somera y se apoya sobre todo en código de ejemplo que ilustra las ideas clave. También aclara que no es experto en estas técnicas, pero sí conoce lo suficiente para dar las ideas fundamentales, mostrar aplicaciones simples y orientar hacia dónde seguir aprendiendo.

Sales sabiendo qué distingue a redes profundas, convolucionales y recurrentes, qué es un tensor, cómo se estructura una red bayesiana y cómo se ajusta con simulación de Markov chain Monte Carlo (MCMC).

## Una nota sobre librerías

A diferencia del resto del libro, aquí no hay librerías estandarizadas: existen varias en competencia y aún no está claro cuál prevalecerá. El código mostrado usa las que el propio autor emplea, pero son librerías inmaduras, con mala documentación, bugs y APIs que cambiarán (PDF p. 359).

- Para deep learning, las punteras son **Theano** y **TensorFlow**, pero son de muy bajo nivel. El autor usa **Keras**, un envoltorio más amigable sobre ellas que permite centrarse en cómo estructurar la red en vez de en los detalles numéricos del entrenamiento.
- Para redes bayesianas usa **PyMC**, librería creada originalmente para aplicar MCMC y que hoy se usa casi sin conciencia de los algoritmos que corren por debajo.

## Deep learning básico

La red neuronal más simple es el perceptrón: una red de "neuronas" donde cada una toma varias entradas y produce una salida. Los nodos etiquetados son variables de entrada o de salida; el resto son neuronas organizadas en capas, y cada capa alimenta a la siguiente. Todas las capas de neuronas antes de la última se llaman capas "ocultas". Un perceptrón tiene una sola capa oculta; el tipo más simple de deep learning son las "redes profundas": redes con varias capas ocultas.

En Keras, el modelo más simple es el `Sequential`: capas apiladas donde cada una alimenta a la siguiente. Una capa `Dense` conecta cada nodo de la capa previa con cada nodo de la actual; `input_dim` indica el número de nodos de la capa anterior (solo hace falta en la primera capa). El parámetro `activation` define cómo cada nodo condensa sus entradas en una salida (por ejemplo, la función `sigmoid`). Compilar el modelo lo traduce a una implementación de bajo nivel en Theano o TensorFlow: no es entrenarlo, sino configurar la maquinaria; `loss` indica la función objetivo a minimizar y `optimizer` el algoritmo de entrenamiento.

```python
model = Sequential([
    Dense(50, input_dim=4, activation='sigmoid'),
    Dense(3, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adadelta')
model.fit(X_train, Y_train, nb_epoch=5)
```

Las redes neuronales son quisquillosas: en el ejemplo con el dataset Iris, usar 10 neuronas en la capa oculta daba un rendimiento que oscilaba al azar entre corr. ~0,6 y valores cercanos a 0 o negativos; con 50 neuronas el rendimiento se estabilizaba en torno a 0,6.

## Redes neuronales convolucionales

Una extensión clave, sobre todo para clasificar imágenes o sonidos, es la red convolucional. Está inspirada en la neurología humana: en las primeras etapas del procesamiento visual hay neuronas que detectan patrones primitivos en zonas concretas del campo visual (una línea inclinada en una región), y capas posteriores combinan esas respuestas para detectar patrones cada vez más complejos, hasta llegar a neuronas que responden a algo tan específico como una imagen concreta.

Una capa convolucional tiene varios "filtros", cada uno busca un patrón. Cada filtro tiene un "kernel": una pequeña matriz de números que, vista como imagen, se parece al patrón que detecta. Para localizar el patrón en toda la imagen, se desliza el kernel por ella y se toma el producto escalar entre el kernel y los píxeles que solapa; ese deslizamiento con paso fijo es la "convolución". El valor resultante en cada punto indica cuánto se parece esa zona al kernel. Se pueden encadenar varias capas convolucionales, cada una con varios filtros.

Las imágenes en color tienen varios valores por píxel (rojo, verde, azul), por lo que los kernels serán arrays tridimensionales. La convolución también funciona para señales unidimensionales como series temporales, lo que hace útiles estas redes en áreas como el reconocimiento del habla.

## Tipos de capas: ¿qué es un tensor?

El nombre TensorFlow alude a los cimientos matemáticos. Coloquialmente, un "tensor" es un array multidimensional de números sobre el que se hacen operaciones lineales. La entrada de una red básica es un array 1-D y su salida también; la entrada de una red convolucional 2-D es un array 2-D y su salida es 1-D. En general, cada capa toma un tensor como entrada y produce un tensor como salida.

Casi todo lo que ocurre en una red son operaciones lineales sobre tensores. Una capa con activación sigmoid toma las entradas, cada nodo calcula una combinación lineal ponderada de ellas (multiplicar una matriz n-por-d por el vector de entrada) y luego aplica la sigmoid a cada elemento: esta es la única parte no lineal. La capa queda completamente caracterizada por su matriz de pesos.

Una capa convolucional es enteramente lineal. Como la entrada es 2-D pero la salida final suele ser 1-D, hace falta una capa de **aplanamiento** (flattening), también lineal, que convierte un tensor d-por-n en un tensor 1-D de longitud d*n con los mismos valores.

## Ejemplo: el dataset MNIST

MNIST es el dataset estándar para aprender redes convolucionales: 70.000 imágenes de dígitos manuscritos de 28×28 píxeles. En Keras, las redes convolucionales 2-D esperan un array de **cuatro dimensiones**: (1) qué punto de datos, (2) el "canal" (uno en escala de grises, tres en color para rojo/verde/azul), y (3-4) filas y columnas de la imagen.

El ejemplo usa además una capa **dropout**, una forma contundente de reducir el overfitting: recibe un parámetro `p` y, en cada iteración de entrenamiento, pone a 0 una fracción aleatoria `p` de los valores antes de pasarlos a la siguiente capa.

```python
model = Sequential()
model.add(Convolution2D(nb_filter=N_FILTERS, input_shape=(1,28,28),
    nb_row=KERNEL_HEIGHT, nb_col=KERNEL_WIDTH, subsample=(STRIDE, STRIDE)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(5,5)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(nb_classes))
model.add(Activation('softmax'))
```

## Redes neuronales recurrentes

Hasta aquí, las redes clasifican cada punto de forma independiente: no tienen memoria tras procesar un punto. Las redes recurrentes (RNN) introducen una memoria primitiva mediante capas "recurrentes", que toman dos entradas: la salida de la capa anterior y la salida de la propia capa recurrente en el punto anterior. Esa realimentación las hace ideales para series temporales. Interpretar su salida es difícil, pero puede codificar una predicción del siguiente punto o una memoria a largo plazo de algo visto hace tiempo. Los tipos más comunes:

- **RNN básicas**: recuerdan solo la última salida de la capa y la realimentan en la siguiente clasificación.
- **LSTM** ("long short-term memory"): muy buenas recordando con claridad eventos seleccionados de un pasado lejano, frente a las RNN básicas, donde la memoria decae con el tiempo.

## Redes bayesianas

Recordatorio de estadística bayesiana: con datos D y una variable Y que queremos inferir, buscamos P(Y|D) mediante P(Y|D) = P(D|Y)·P(Y) / P(D). El **prior** P(Y) es la confianza inicial (la parte filosóficamente controvertida); P(D|Y) es donde está la "magia" y suele ser mucho más fácil de modelar que P(Y|D); P(D) es solo un término de normalización que casi nunca hace falta calcular, porque normalmente interesan las probabilidades relativas entre valores de Y.

El término P(D|Y) es complicado porque las D_i pueden tener dependencias entre sí. La suposición naive Bayes es que todas las D_i son condicionalmente independientes dado Y, lo que en general es falso. Una **red bayesiana** representa esas dependencias como un grafo dirigido (ejemplo del libro: género → longitud del pelo → lleva coletero). El grafo muestra, por ejemplo, que entre quienes tienen el pelo largo no hay relación entre género y coletero.

El usuario elige la topología de la red y un modelo probabilístico de cómo cada variable depende de las que la influyen; los datos de entrenamiento ajustan los parámetros. La topología es un punto donde insertar conocimiento experto o intuición: en ese sentido, las redes bayesianas son casi lo opuesto a las redes neuronales, que son casi imposibles de interpretar. Se pueden usar para predecir o para diseccionar el modelo entrenado y obtener insights.

## Entrenamiento y predicción

En naive Bayes los parámetros de P(D|Y) se conocen con precisión (típicamente por máxima verosimilitud, lo que abre la puerta al overfitting). En las redes bayesianas, en cambio, los propios parámetros tienen una distribución de confianza: partimos de priors y los refinamos con los datos. Para clasificar hay que promediar las predicciones sobre todas las configuraciones posibles del modelo, ponderadas por la confianza, lo que da una integral muy complicada (a veces imposible), por lo que se recurre a aproximaciones numéricas.

## Markov chain Monte Carlo

PyMC ajusta redes bayesianas a datos reales, pero no es un clasificador al uso: si quieres predecir, debes hacerlo por tu cuenta; PyMC se encarga del trabajo pesado de ajustar el modelo. En lugar de darnos la función Confidence(θ), computacionalmente intratable, PyMC entrega **muestras aleatorias** de la distribución entrenada Θ, y la integral se estima sumando sobre las muestras. La técnica es Markov chain Monte Carlo (MCMC): una secuencia de estimaciones θ_i que, a lo largo del tiempo, se muestrea de Θ.

El problema principal es que las muestras sucesivas no son independientes: cada θ_i está correlacionada con las vecinas (autocorrelación). Si las correlaciones decaen rápido, las muestras son casi independientes; si no, hacen falta muchísimas para aproximar bien Θ. Imaginando Θ como un paisaje, MCMC es un paseo aleatorio que, en el límite infinito, pasa en cada zona un tiempo proporcional a su probabilidad, pero puede tardar arbitrariamente en alcanzar una región de alta probabilidad. Como empezar en un punto improbable sesga las estadísticas, se descartan las primeras N muestras: el **burn-in**.

## Ejemplo con PyMC

Usando el dataset de viviendas de Boston de scikit-learn, el autor ajusta una red bayesiana con la idea de que una mala educación (ratio alumno/profesor) eleva la criminalidad, que a su vez reduce el precio de la vivienda. Las suposiciones: el ratio alumno/profesor sigue una distribución exponencial de media conocida; la criminalidad es exponencial con media A·ratio; el número medio de habitaciones es normal; el precio mediano es normal con media B·habitaciones·(C−criminalidad). A, B y C son parámetros desconocidos con priors exponenciales de media 1.

En PyMC el modelo se declara entero en un fichero; cada variable especifica su familia y sus parámetros (fijos o definidos por otras variables), y con `observed=True` se pasan los valores observados. El entrenamiento descarta las primeras 30.000 simulaciones (burn-in) y calcula estadísticas con las siguientes 40.000:

```python
S = pymc.MCMC(mymodel)
S.sample(iter=40000, burn=30000)
```

Los gráficos de PyMC muestran la evolución de un parámetro (B) y su histograma, centrado en torno a 0,0605; la simulación parece haberse equilibrado. Técnicamente queda el riesgo de que exista una región de Θ aún no explorada que cambiaría la dinámica, pero a la vista de los gráficos parece improbable.

## Ideas clave

- A diferencia de los clasificadores básicos, el deep learning y las redes bayesianas requieren diseñar estructura y ajustar muchos parámetros a mano; son potentes pero difíciles de dominar.
- No hay librerías estándar maduras: el libro usa Keras (sobre Theano/TensorFlow) para deep learning y PyMC para redes bayesianas.
- Una red profunda tiene varias capas ocultas; cada capa toma un tensor (array multidimensional) y la mayor parte del cómputo son operaciones lineales (matrices de pesos) más una activación no lineal.
- Las redes convolucionales deslizan kernels que detectan patrones locales; son clave para imágenes y señales 1-D como el sonido.
- Las redes recurrentes añaden memoria realimentando la salida de una capa; las LSTM recuerdan eventos lejanos mejor que las RNN básicas. El dropout reduce el overfitting poniendo valores a 0 al azar.
- Una red bayesiana representa dependencias entre variables como un grafo dirigido que el usuario diseña; admite insertar intuición experta, al contrario que las redes neuronales.
- En las redes bayesianas los parámetros tienen distribuciones de confianza; predecir implica una integral intratable que se aproxima numéricamente.
- MCMC (vía PyMC) genera muestras correlacionadas de la distribución entrenada; su mayor problema es la autocorrelación, y se descartan las primeras muestras (burn-in) para evitar el sesgo del arranque.
