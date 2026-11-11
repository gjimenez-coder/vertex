# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 4 — Fitting a Model to Data (Ajustar un modelo a los datos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo presenta una segunda forma de modelado predictivo, complementaria a la inducción de árboles del capítulo 3: el ajuste de funciones o modelado paramétrico. En lugar de descubrir la estructura del modelo a partir de los datos, aquí el analista fija de antemano la estructura (normalmente una función matemática parametrizada de los atributos numéricos) y deja sin especificar los parámetros numéricos; la minería de datos calcula los mejores valores de esos parámetros para un conjunto de entrenamiento concreto. Este enfoque se llama parameter learning o parametric modeling (PDF p. 105).

La tesis central es que linear regression, logistic regression y support-vector machines son variantes del mismo procedimiento fundamental —ajustar un modelo lineal a los datos— y que la diferencia esencial entre ellas es la función objetivo que optimizan. El concepto clave del capítulo es, por tanto, qué significa exactamente que un modelo "ajusta bien" los datos: eso se define mediante una objective function que se maximiza o minimiza, y mediante loss functions que penalizan los errores (PDF p. 105, 111).

Al terminar el capítulo sales sabiendo qué es un discriminante lineal y cómo se expresa como suma ponderada de atributos; por qué hay infinitas rectas que separan los datos y cómo la elección de la función objetivo decide cuál es la "mejor"; cómo funcionan a grandes rasgos SVM, regresión lineal por mínimos cuadrados y regresión logística; y por qué aumentar la flexibilidad del modelo (SVM no lineales, redes neuronales) arrastra el riesgo de overfitting, tema del capítulo siguiente (PDF p. 132).

El capítulo advierte de que es más matemático que el resto y hace tres supuestos simplificadores: solo considera clases binarias, asume que todos los atributos son numéricos e ignora la necesidad de normalizar las medidas a una escala común (PDF p. 106).

## Clasificación mediante funciones matemáticas

Recuperando la vista del espacio de instancias del capítulo 3, un árbol parte el espacio con fronteras de decisión horizontales y verticales (paralelas a los ejes). Pero si se permite una frontera que siga siendo una recta sin ser perpendicular a los ejes, a menudo se separan las clases casi perfectamente. Eso es un clasificador lineal: esencialmente una suma ponderada de los valores de los atributos (PDF p. 107-108).

La frontera se representa matemáticamente. Partiendo de la recta `Age = (-1.5) × Balance + 60`, se reordena a una función de discriminante lineal que clasifica una instancia según el signo del resultado:

```
class(x) = + si 1.0 × Age - 1.5 × Balance + 60 > 0
           • si 1.0 × Age - 1.5 × Balance + 60 ≤ 0
```

Se llama discriminante lineal porque discrimina entre clases y la frontera es una combinación lineal —una suma ponderada— de los atributos. En dos dimensiones es una recta, en tres un plano y en más un hiperplano. El modelo lineal general se escribe (PDF p. 109-110):

```
f(x) = w0 + w1x1 + w2x2 + ⋯
```

donde `w0` es el intercepto. Los pesos `wi` son los parámetros que la minería de datos debe ajustar. Tras el aprendizaje, la magnitud de un peso se interpreta libremente como la importancia del atributo: cuanto mayor, más importante; si está cerca de cero, el atributo suele poder ignorarse (PDF p. 110).

## Optimizar una función objetivo

El problema es que hay infinitas rectas que separan perfectamente un conjunto de entrenamiento, con pendientes e interceptos distintos: cada una es un modelo diferente. ¿Cuál elegir? Esto lleva a una de las ideas fundamentales de la minería de datos, a menudo pasada por alto: ¿cuál debe ser el objetivo al elegir los parámetros? El procedimiento general es definir una objective function que represente la meta y pueda calcularse para un conjunto de pesos y de datos; luego se buscan los pesos óptimos maximizándola o minimizándola. Los pesos solo son "los mejores" si creemos que la función objetivo representa de verdad lo que queremos lograr, o es el mejor sustituto disponible (PDF p. 111).

Crear una función objetivo que coincida con la meta real suele ser imposible, así que los analistas eligen por fe y experiencia. Varias opciones resultan muy eficaces. Regresión lineal, regresión logística y SVM son instancias muy parecidas de la misma técnica fundamental; la diferencia clave es que cada una usa una función objetivo distinta (PDF p. 112).

Como ilustración se usa una adaptación del dataset Iris (UCI), limitado a dos especies, Iris Setosa e Iris Versicolor, descritas por dos medidas: Petal width y Sepal width. En la figura se muestran dos separadores: uno generado por regresión logística y otro por un SVM. La regresión logística separa las dos clases por completo; el SVM queda casi a mitad de camino entre los grupos y clasifica mal un punto en (3, 1). Producen fronteras distintas porque optimizan funciones distintas (PDF p. 112-113).

### Puntuación y ordenación de instancias

A menudo no queremos una respuesta sí/no, sino saber qué ejemplos son más o menos propensos a pertenecer a la clase (qué consumidores responderán a una oferta, qué clientes se irán). Los discriminantes lineales ofrecen esa ordenación gratis: `f(x)` vale cero sobre la frontera, es pequeño cerca de ella y grande y positivo lejos, en la dirección +. Así, la propia salida `f(x)` ordena las instancias por su verosimilitud estimada de pertenecer a la clase de interés, lo que basta para, por ejemplo, un marketing dirigido con presupuesto limitado (PDF p. 114).

## Support Vector Machines, brevemente

En esencia, los support vector machines son discriminantes lineales: clasifican según una función lineal de los atributos. Su función objetivo parte de dos ideas. La primera: en vez de pensar en separar con una recta, se ajusta la barra más ancha posible entre las clases; la frontera es la línea central de esa barra y la distancia entre sus bordes es el margin. El objetivo es maximizar el margen (PDF p. 115). Esto es intuitivo porque el conjunto de entrenamiento es solo una muestra: instancias nuevas pueden caer dentro del margen, y la frontera de margen máximo da el mayor margen de maniobra para clasificarlas bien (PDF p. 116).

La segunda idea es cómo tratar los puntos del lado equivocado cuando no hay recta que separe perfectamente (lo habitual en datos reales): la función objetivo penaliza cada punto por estar en el lado incorrecto. Si los datos son linealmente separables no hay penalización y solo se maximiza el margen; si no, el mejor ajuste equilibra un margen ancho con una penalización total baja. La penalización es proporcional a la distancia a la frontera, por lo que el SVM intenta cometer solo errores "pequeños". Esa función de error es la hinge loss (PDF p. 116-117).

Los SVM no lineales, simplificando, usan atributos que son funciones de los originales, de modo que un discriminante lineal en el nuevo espacio es no lineal en el original (PDF p. 115).

### Loss functions

"Loss" es el término general para la penalización del error; una loss function determina cuánta penalización asignar a una instancia según el error de la predicción (aquí, según su distancia a la frontera de separación) (PDF p. 118):

- Hinge loss (SVM): no penaliza un ejemplo que no esté del lado equivocado del margen; se vuelve positiva cuando el ejemplo cruza la frontera y supera el margen, y crece linealmente con la distancia.
- Zero-one loss: pérdida de cero para una decisión correcta y de uno para una incorrecta.
- Squared error: pérdida proporcional al cuadrado de la distancia; se usa sobre todo para predicción de valores numéricos (regresión). Penaliza con fuerza los errores groseros, pero aplicada a clasificación también castiga puntos muy correctos, lo que suele desalinearla del objetivo de negocio (PDF p. 118).

## Regresión mediante funciones matemáticas

La regresión lineal usa exactamente la misma estructura de modelo que el discriminante lineal (`f(x) = w0 + w1x1 + w2x2 + ⋯`). Falta decidir la función objetivo. Como el target es numérico y los datos tienen su valor real, una noción intuitiva de ajuste es cuán lejos están los valores estimados de los reales; se busca minimizar ese error sumado sobre los puntos de entrenamiento (PDF p. 119).

Hay varias formas de medir el error. La más natural es el valor absoluto de la diferencia (absolute error), pero la regresión lineal estándar minimiza en cambio la suma o media de los cuadrados de esos errores, de ahí el nombre least squares. Su popularidad se debe sobre todo a la conveniencia: es lo que se enseña en estadística básica, está en todos los paquetes de software, tiene fundamentos teóricos ligados a la distribución normal y resulta cómoda matemáticamente (Gauss) (PDF p. 119-120). Toda función objetivo tiene ventajas e inconvenientes: un inconveniente serio de least squares es su gran sensibilidad a datos erróneos o outliers, que pueden distorsionar mucho la función; para sistemas automáticos puede convenir un procedimiento más robusto (p. ej. absolute error) (PDF p. 120).

## Estimación de probabilidad de clase y regresión logística

Para muchas aplicaciones queremos estimar la probabilidad de que una instancia pertenezca a la clase, para usarla en decisiones con costes y beneficios (p. ej. en fraude, centrarse en las cuentas con mayor pérdida esperada, no solo en las más probables). Cambiando la función objetivo dentro del mismo marco de modelos lineales obtenemos estimaciones precisas de probabilidad: ese procedimiento es la logistic regression (PDF p. 120). Idealmente las estimaciones deben ser bien calibradas (de 100 casos estimados en 0.2, unos 20 pertenecen a la clase) y discriminativas (dar probabilidades distintas a ejemplos distintos, no la base rate a todos) (PDF p. 121).

El problema de usar directamente `f(x)` como probabilidad es que `f(x)` va de –∞ a ∞, mientras una probabilidad va de 0 a 1. La solución pasa por las odds (razón entre probabilidad de que ocurra y de que no: 80% → 4:1), que van de 0 a ∞, y luego por el logaritmo de las odds (log-odds), que sí va de –∞ a ∞. Así, la regresión logística modela las log-odds del evento con la función lineal `f(x)` (PDF p. 121-122):

```
log( p+(x) / (1 - p+(x)) ) = f(x) = w0 + w1x1 + w2x2 + ⋯
```

Despejando se obtiene la función logística, cuya gráfica es la curva sigmoide (en S) que comprime la probabilidad al rango [0,1]:

```
p+(x) = 1 / (1 + e^(-f(x)))
```

En la frontera (distancia 0) la probabilidad es 0.5; varía casi linealmente cerca y se acerca a la certeza lejos. Los puntos esenciales: la regresión logística usa el mismo modelo lineal que los discriminantes y la regresión lineal; su salida se interpreta como las log-odds de pertenencia a la clase; y esas log-odds se traducen directamente en probabilidad, por lo que suele verse como un modelo de probabilidad de clase (PDF p. 122-124).

El nombre es un misnomer: produce una estimación numérica (log-odds), pero sobre un target categórico, así que es un modelo de estimación de probabilidad de clase, no de regresión (PDF p. 123). La función objetivo que ajusta el modelo es el maximum likelihood: para cada ejemplo etiquetado se calcula la verosimilitud `g(x,w)` de ver su clase real (`p+(x)` si es +, `1 - p+(x)` si es •) y se eligen los pesos que maximizan la suma, dando en promedio las probabilidades más altas a los positivos y las más bajas a los negativos. Conviene ver los datos de entrenamiento como "extracciones" estadísticas de las probabilidades subyacentes, no como las probabilidades mismas (PDF p. 125-126).

## Ejemplo: regresión logística frente a inducción de árboles

Aunque ambos usan fronteras lineales, difieren en dos aspectos: (1) el árbol usa fronteras perpendiculares a los ejes porque selecciona un atributo cada vez, mientras el clasificador lineal usa una combinación ponderada de todos y puede orientar la frontera libremente; (2) el árbol es un clasificador por tramos que trocea el espacio recursivamente tan fino como haga falta, mientras el lineal coloca una única superficie de decisión en todo el espacio (PDF p. 126). No es fácil saber de antemano cuál encaja mejor. Práctica­mente, difieren en comprensibilidad para los stakeholders: la regresión logística es clara para quien tiene base estadística y difícil para quien no; un árbol no demasiado grande suele entenderse mejor sin esa base, lo que importa porque gestores de distintas áreas deben "firmar" el uso de un modelo (PDF p. 126-127).

Sobre el Wisconsin Breast Cancer Dataset (10 características por imagen de núcleos celulares, ampliadas a 30 atributos con _mean, _SE y _worst; 357 benignos y 212 malignos), la regresión logística aprende una ecuación lineal con solo 6 errores sobre 569 casos, una exactitud de ~98.9%; un árbol J48 de 13 hojas alcanza 99.1% (PDF p. 127-129). Pero esa diferencia es un único error adicional y ambas cifras se midieron sobre los mismos datos de construcción: la evaluación fiable se trata en los capítulos 5, 7 y 8 (PDF p. 129).

## Funciones no lineales, SVM y redes neuronales

Las funciones lineales pueden representar modelos no lineales si se incluyen atributos más complejos. En el ejemplo Iris, añadir un término Sepal width² produce una frontera curva (una parábola) en el espacio original. El concepto fundamental del capítulo es más general que ajustar funciones lineales: se pueden especificar funciones numéricas arbitrariamente complejas y ajustar sus parámetros (PDF p. 129-130).

Las dos familias más comunes basadas en funciones complejas son los SVM no lineales y las redes neuronales. Un SVM no lineal es una forma sistemática de añadir términos complejos: su kernel function mapea los atributos originales a otro espacio de atributos donde se ajusta un modelo lineal (por ejemplo, un polynomial kernel considera combinaciones de orden superior) (PDF p. 130-131).

Una red neuronal es una "pila" de modelos: en la base están los atributos originales; de ellos se aprenden modelos simples (p. ej. regresiones logísticas) y cada capa aplica otro modelo simple a las salidas de la capa inferior, como crear "expertos" en facetas del problema y luego aprender a ponderar sus opiniones. Las etiquetas de entrenamiento suelen darse solo en la capa final; las capas inferiores se entrenan porque toda la pila se representa como una gran función numérica parametrizada cuyos parámetros son los coeficientes de todos los modelos: elegida una función objetivo, un procedimiento de optimización halla los mejores parámetros de todos los modelos a la vez (PDF p. 131). El inconveniente: cuanta más flexibilidad para ajustar los datos, mayor el riesgo de ajustarlos demasiado (overfitting), tema del capítulo 5 (PDF p. 132).

## Resumen del capítulo

Este capítulo introdujo el function fitting o modelado paramétrico: el modelo es una ecuación parcialmente especificada (función numérica de los atributos con parámetros sin fijar) y la minería de datos "ajusta" el modelo hallando el mejor conjunto de parámetros. La mayoría de las técnicas comparten la estructura de modelo lineal —suma ponderada de atributos— y la diferencia conceptual clave es su respuesta a qué significa ajustar mejor los datos, descrita por la función objetivo. Vistas ya dos formas de modelado (árboles y ajuste de funciones) y dos criterios de evaluación (rendimiento predictivo e inteligibilidad), queda el problema central: si se busca lo suficiente se encuentra estructura en los datos aunque sea por azar; esa tendencia es el overfitting (PDF p. 132).

## Ideas clave

- El modelado paramétrico fija la estructura del modelo y deja que los datos determinen los parámetros; parameter learning es la alternativa a la inducción de árboles.
- Un discriminante lineal clasifica según el signo de `f(x) = w0 + w1x1 + w2x2 + ⋯`, una suma ponderada de los atributos; en 2D es una recta, en 3D un plano y en más un hiperplano.
- Hay infinitas rectas que separan los datos; elegir la "mejor" equivale a elegir una función objetivo que se maximiza o minimiza, y debe alinearse con la meta de negocio.
- Regresión lineal, regresión logística y SVM comparten el modelo lineal y se distinguen por su función objetivo y su loss function (squared error, hinge loss, zero-one loss).
- El SVM maximiza el margen (la barra más ancha entre clases) y penaliza con hinge loss los puntos del lado equivocado proporcionalmente a su distancia.
- La regresión logística modela las log-odds con `f(x)` y las convierte en probabilidad vía la función logística (curva sigmoide); se ajusta por maximum likelihood y es, pese a su nombre, un estimador de probabilidad de clase.
- La salida `f(x)` de un discriminante lineal sirve para ordenar instancias por verosimilitud de pertenencia a la clase, sin necesitar la probabilidad exacta.
- Añadir atributos complejos (kernels en SVM no lineales, capas en redes neuronales) permite modelos no lineales dentro del mismo marco, a costa de un mayor riesgo de overfitting.
