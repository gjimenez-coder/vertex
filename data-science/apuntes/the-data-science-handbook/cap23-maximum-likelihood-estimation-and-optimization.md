# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 23 — Maximum Likelihood Estimation and Optimization (Estimación por máxima verosimilitud y optimización)

> Nota de extracción: el texto proviene de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber
El capítulo presenta dos pilares matemáticos y computacionales que sostienen buena parte del libro: la estimación por máxima verosimilitud (MLE) y la optimización numérica. El objetivo es dar un marco para plantear problemas nuevos de forma que tengan sentido teórico y que un ordenador pueda resolver de manera realista.

La MLE es una manera muy general de formular una gran clase de problemas: tienes una familia de distribuciones de probabilidad descrita por parámetros θ, supones que un proceso del mundo real sigue alguna distribución de esa familia, dispones de un conjunto de datos X extraído de ese proceso y buscas el θ que maximiza P(X|θ). Muchos modelos de clasificación y regresión caen bajo este paraguas: "entrenar el modelo" se reduce, en esencia, a calcular θ.

La otra mitad del capítulo trata la optimización numérica, el mecanismo con el que se resuelven en la práctica la mayoría de problemas MLE cuando no hay solución cerrada. Sales sabiendo cómo funciona el descenso de gradiente, qué es la optimización convexa (y por qué garantiza convergencia al óptimo global) y qué es el descenso de gradiente estocástico (SGD).

## Máxima verosimilitud (MLE)
En MLE casi siempre se asume que los puntos de datos de X son independientes entre sí, de modo que la probabilidad del conjunto es el producto de las probabilidades de cada punto:

```
P(X|θ) = ∏ P(Xi|θ)
```

En la práctica suele ser más fácil maximizar el logaritmo de la probabilidad que la probabilidad misma, porque el log convierte el producto en una suma:

```
log P(X|θ) = Σ log P(Xi|θ)
```

La MLE tiene dos problemas significativos. El primero es el **overfitting**: sobre todo con conjuntos pequeños, se corre el riesgo real de obtener parámetros que predicen muy bien tus datos concretos pero generalizan pésimamente. La alternativa más popular es el enfoque bayesiano, que en general es más difícil de entender, más complicado de implementar y más lento, y que arrastra la espinosa cuestión de cómo se elige el prior.

El segundo problema es logístico: calcular realmente el θ óptimo. En algunos casos hay una solución cerrada y ordenada —suelen ser los casos históricamente importantes, porque la gente podía resolverlos con papel y lápiz—, pero en general no existe solución cerrada y hay que recurrir a algoritmos numéricos que dan buenas aproximaciones. Eso es precisamente la optimización numérica.

## Un ejemplo simple: ajustar una recta
Para ilustrar la MLE se reproduce el ajuste de mínimos cuadrados, que aquí sí tiene solución cerrada. Se asume que y es una función lineal de x más ruido, y que el ruido sigue una distribución normal. Al escribir la expresión de verosimilitud (negativa) a minimizar y exigir que las derivadas respecto a la pendiente m y la ordenada b sean 0, se obtienen, tras algo de álgebra, las fórmulas cerradas clásicas de mínimos cuadrados para m y b.

Lo valioso es el cambio de perspectiva: los mínimos cuadrados dejan de ser una técnica de caja negra y pasan a ser *la* técnica correcta si se cumplen ciertas suposiciones sobre el mundo (y lineal en x más ruido normal). Pero no siempre es la suposición adecuada. Si x es el ingreso de una persona e y el precio de su vivienda, convendría un modelo donde la desviación típica del ruido sea proporcional a x (β·x), porque una diferencia de 20.000 $ pesa mucho si ganas 50.000 $ al año y poco si ganas 500.000 $. Esa variante probablemente no tiene solución cerrada, pero sí una aproximación numérica.

Otra variación sería usar una distribución distinta de la normal, que admita más outliers (gente que compra casas muy por encima o por debajo de sus medios). La idea de fondo: en lugar de confiar a ciegas en técnicas estándar, la MLE permite traducir el conocimiento del mundo real en modelos probabilísticos e incorporarlo directamente al modelo.

## Otro ejemplo: regresión logística
En la regresión logística x es un vector e y vale 0 o 1. La puntuación que da es:

```
p(x) = σ(w·x + b) = 1 / (1 + exp(w·x + b))
```

donde p(x) es la probabilidad de que un punto real en x sea un 1 (y 1 − p(x) la de que sea 0). Dada la muestra de entrenamiento, la verosimilitud de las etiquetas observadas es el producto de p(x) sobre los puntos con y=1 por el producto de (1 − p(x)) sobre los puntos con y=0. La fase de entrenamiento busca el w y el b que maximizan esa expresión.

## Optimización
La optimización resuelve este problema: dada una función f(θ), con θ un vector de d dimensiones, y posiblemente varias restricciones gi(θ) ≤ 0, encontrar el θ que minimiza f(θ) cumpliendo todas las restricciones. Es el modo en que muchos problemas MLE se resuelven en la práctica, aunque sirve en muchos otros dominios.

La optimización también permite mitigar el overfitting de la MLE añadiendo términos de penalización. En regresión logística, restar λ·Σ|wi| (λ positivo elegido por ti) ya no es una MLE válida, pero sí un problema de optimización: es la **regresión LASSO**, que penaliza moderadamente pesos grandes y pequeños. Si además se añade un término que penaliza el cuadrado de los pesos para castigar con dureza los pesos grandes, se obtiene la **regularización elastic net**.

Cualquier buen paquete de cálculo numérico trae rutinas de optimización que puedes tratar como caja negra: le das un handle a la función a minimizar y, opcionalmente, una conjetura inicial; el optimizador genera una secuencia de conjeturas que, con suerte, converge al óptimo. Hay dos formas típicas de fallo: que la secuencia se dispare al infinito en alguna dirección (reinicia con otra conjetura inicial) o que converja a un **óptimo local** —mejor que todo lo cercano pero peor que algún punto lejano—. Lo más sencillo ante lo segundo es probar varias conjeturas iniciales y ver si las mejores convergen al mismo sitio; aun así, no puedes estar seguro.

## Descenso de gradiente y optimización convexa
La imagen mental útil es caminar con los ojos vendados por un terreno de colinas: la altura es el valor de la función objetivo y tus coordenadas son las componentes del vector de conjetura. En cada paso hay que responder dos preguntas: ¿en qué dirección moverse (cuesta abajo) y cuánto avanzar?

Formas de elegir la dirección:

- **Descenso de gradiente**: si puedes derivar el gradiente ∇f(x) con cálculo, multiplicarlo por −1 da la dirección más empinada cuesta abajo.
- Si no tienes el gradiente, una implementación ingenua incrementa cada dimensión un poco, recalcula f y se mueve en la dirección que más la reduce.
- Con el **Hessiano** (matriz de segundas derivadas) puedes aproximar f localmente como un paraboloide y moverte hacia su centro.
- También se pueden mantener estimaciones del gradiente y del Hessiano actualizadas con pocas evaluaciones. Muchos algoritmos empiezan con descenso de gradiente y pasan al Hessiano cerca del óptimo, porque converge más rápido.

Para la distancia (tamaño de paso), una técnica común es usar el gradiente como paso inicial y, si f baja, multiplicar el paso por un α > 1 mientras siga bajando; si no bajó, dividir el paso por α hasta que empiece a bajar. Hay que evitar dos problemas: reducir el paso tan rápido que se tarde mucho (o se converja antes del mínimo) y sobrepasar el mínimo repetidamente (ineficiente, y si se sobrepasa mucho ¡f puede aumentar!). Aun con buenas decisiones, el algoritmo converge a un óptimo local: si x0 cae cerca de un óptimo local, probablemente caiga en ese pozo.

## Optimización convexa
Un problema es convexo si cumple restricciones matemáticas que garantizan que cualquier algoritmo razonable converge a x* (si existe). Intuitivamente: la función objetivo tiene forma de "cuenco" y, al trazar una línea recta entre dos puntos cualesquiera de la región factible, esa línea queda entera dentro de la región.

La primera condición implica que la función no tiene mínimos locales salvo el único mínimo global en el fondo del cuenco: no puedes caer en una trampa. La segunda implica que hay una recta desde xn hasta x* dentro de la región factible; si no, el descenso de gradiente podría chocar contra la frontera de la región y detenerse ahí. Formalmente, f es convexa si para cualesquiera x, y y cualquier α entre 0 y 1: f(αx + (1−α)y) ≤ αf(x) + (1−α)f(y).

La convexidad es una condición muy restrictiva: una función al azar rara vez es convexa, y mucha gente dedica tiempo a reformular problemas no convexos en equivalentes convexos o a demostrar que ciertas clases lo son. Casi no hay término medio: si es convexo, cualquier algoritmo decente converge a la respuesta correcta; si no, no hay garantías. Aun así, gran parte del machine learning trabaja con problemas no convexos (o no demostrados convexos) con excelentes resultados, apoyándose en reglas empíricas en lugar de teoremas.

## Descenso de gradiente estocástico (SGD)
En muchos problemas la función objetivo es una suma de muchas funciones más simples. En MLE se optimiza `log P(X|θ) = Σ log P(Xi|θ)`, donde N (el número de puntos de entrenamiento) suele ser enorme y calcular el gradiente completo es computacionalmente prohibitivo.

La idea del SGD es aproximar el gradiente eligiendo un único índice i y calculando el gradiente de `log P(Xi|θ)`; cada paso toma un nuevo i, al azar o recorriendo todo el conjunto. Una variante es el **mini batch SGD**, que calcula el gradiente sobre una selección de varios puntos: suficientes para estimar mejor el gradiente real pero pocos para que el cálculo siga siendo viable. Tiende a converger más rápido que el SGD puro.

## Ideas clave
- La MLE busca el θ que maximiza P(X|θ) asumiendo puntos independientes; en la práctica se maximiza el log-verosimilitud (suma en vez de producto).
- Sus dos problemas son el overfitting (alternativa: enfoque bayesiano, más costoso) y el cálculo del óptimo (rara vez cerrado, suele requerir optimización numérica).
- Los mínimos cuadrados son la MLE correcta si y es lineal en x con ruido normal; cambiar esas suposiciones permite modelar mejor la realidad.
- La optimización minimiza f(θ) sujeta a restricciones gi(θ) ≤ 0; penalizar pesos convierte la MLE en LASSO (|w|) o elastic net (|w| y w²).
- Los optimizadores generan una secuencia de conjeturas; pueden diverger o quedar atrapados en un óptimo local.
- El descenso de gradiente se mueve en dirección −∇f; variantes usan el Hessiano o estimaciones running del gradiente/Hessiano, ajustando el tamaño de paso con un factor α.
- En problemas convexos (función en forma de cuenco y región factible convexa) cualquier algoritmo decente converge al óptimo global; fuera de ahí no hay garantías.
- El SGD y su variante mini batch aproximan el gradiente con uno o pocos puntos, haciendo viable la optimización con datasets grandes.
