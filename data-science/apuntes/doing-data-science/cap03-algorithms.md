# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 3 — Algorithms (Algoritmos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber
El capítulo presenta los algoritmos como piezas básicas de la ciencia de datos y distingue tres clases que conviene conocer: algoritmos de preparación y procesamiento de datos (sorting, MapReduce, Pregel), algoritmos de optimización para estimar parámetros (Stochastic Gradient Descent, método de Newton, mínimos cuadrados) y algoritmos de machine learning. Estos últimos sirven sobre todo para predecir, clasificar o agrupar (cluster).

La tesis central es que un científico de datos es un híbrido entre estadístico e ingeniero de software, y debe valorar ambas culturas. Las autoras marcan que el modelado estadístico surgió de los departamentos de estadística y los algoritmos de machine learning de ciencias de la computación, de modo que la frontera entre "modelo" y "algoritmo" es borrosa y los términos se usan de forma intercambiable. Rachel observa estas diferencias culturales en Google y en conferencias del sector.

El verdadero reto no es implementar las técnicas, sino saber cuándo usar cada una según el contexto y las propiedades del problema. Las autoras advierten contra el patrón de "tener un martillo y buscar clavos": no intentes resolver todo con regresión lineal solo porque la conoces.

Sales sabiendo tres algoritmos fundamentales —regresión lineal, k-nearest neighbors (k-NN) y k-means—, con qué supuestos trabajan, cómo se evalúan y cómo pensar qué atributos de un problema los hacen adecuados, además de una primera noción de qué pasa al escalar a Big Data.

## Tres clases de algoritmos y las dos culturas
Un algoritmo es un procedimiento o conjunto de pasos o reglas para realizar una tarea; es un bloque fundamental de la informática. Tareas típicas son ordenar, buscar y resolver problemas de grafos; aunque varias opciones resuelvan la misma tarea, existe una noción de "mejor" medida por eficiencia y tiempo de cómputo, crucial con grandes volúmenes de datos.

Las autoras señalan generalizaciones amplias que distinguen a estadísticos de ingenieros:

- Interpretación de parámetros: los estadísticos buscan sentido real en los parámetros; los ingenieros tratan el modelo como caja negra (black box) y, si los ajustan a mano, es para optimizar la capacidad predictiva.
- Intervalos de confianza: los estadísticos aportan intervalos de confianza y distribuciones posteriores para capturar la incertidumbre; muchos algoritmos de ML, como k-means o k-NN, no tienen esa noción.
- Supuestos explícitos: los modelos estadísticos hacen supuestos explícitos sobre el proceso generador de datos; las soluciones no paramétricas no asumen distribuciones de probabilidad, o lo hacen de forma implícita.

Lo resumen, con respeto, diciendo que los estadísticos investigan la incertidumbre y nunca están 100% seguros, mientras que los ingenieros quieren construir y lo arreglan si algo se rompe (filosofía de empresas como Facebook o Google: construir e iterar). Citan al ponente invitado Josh Wills (capítulo 13): "Data scientist (noun): Person who is better at statistics than any software engineer and better at software engineering than any statistician" (PDF p. 82).

## Regresión lineal
La regresión lineal expresa la relación matemática entre una variable de resultado (respuesta, dependiente o etiqueta) y uno o más predictores (variables independientes, explicativas o features), asumiendo que esa relación es lineal. Es el supuesto más simple y, por tanto, un buen punto de partida; a veces solo se justifica localmente, como en cálculo, donde todo se aproxima por segmentos de recta si las funciones son continuas.

Las autoras aclaran la confusión entre "modelo" y "algoritmo": en sentido puro, un algoritmo es un conjunto de pasos y un modelo es un intento de describir el mundo, pero la regresión puede verse como modelo estadístico y como algoritmo de ML, así que no vale la pena discutirlo con precisión (PDF p. 84).

Partiendo de una recta determinista `y = β0 + β1·x`, se pasa a una función estocástica. Con datos a nivel de usuario (por ejemplo, `total_new_friends` frente a `time_spent`), se observa una relación aproximadamente lineal pero no determinista. El modelo quiere capturar dos cosas: la tendencia (trend) y la variación.

Se asume la forma funcional `y = β0 + β1x`, en notación matricial `y = x·β`. Ajustar el modelo significa hallar la recta que minimiza la distancia entre los puntos y la recta. Se usa estimación por mínimos cuadrados (least squares): se define la suma residual de cuadrados `RSS(β) = ∑i (yi − βxi)²`, se deriva respecto a β y se iguala a cero, obteniendo `β̂ = (xᵀx)⁻¹xᵀy`. El "sombrero" indica que es el estimador de β a partir de los datos observados. En R basta una línea: `model <- lm(y ~ x)`, que en el ejemplo da `y = −32.08 + 45.92x`.

Para capturar la variación, el modelo se extiende a `y = β0 + β1x + ϵ`, donde ϵ es el ruido o término de error. Es habitual suponer ruido normal `ϵ ∼ N(0, σ²)`, aunque no siempre es razonable: con distribuciones de colas pesadas (fat-tailed), típicas en finanzas, los errores también lo son; se puede usar regresión sin ese supuesto. Sea cual sea la distribución de los ϵ, los estimadores de mínimos cuadrados son óptimos por ser insesgados y de mínima varianza.

La varianza del error se estima con `∑i ei² / (n−2)`; se divide por n−2 (número de parámetros del modelo) para obtener un estimador insesgado. Esta cantidad es el error cuadrático medio (mean squared error), útil en cualquier problema de predicción.

Para medir la confianza en el modelo, la salida de R (`summary(model)`) ofrece: R-squared `R² = 1 − ∑(yi−ŷi)² / ∑(yi−ȳ)²`, interpretable como la proporción de varianza explicada; p-values, que bajo la hipótesis nula de que los β son cero indican que un valor bajo hace muy improbable ese estadístico y, por tanto, el coeficiente es significativo; y cross-validation, dividir los datos en entrenamiento (80%) y prueba (20%), comparar el error cuadrático medio en ambos y, si son parecidos, concluir que el modelo generaliza bien y no hay overfitting (enfoque muy recomendado).

El mean squared error es un ejemplo de función de pérdida (loss function), estándar en regresión lineal y compatible con el principio de máxima verosimilitud bajo ruido normal; existen otras (valor absoluto) y pérdidas personalizadas.

El modelo simple se extiende de tres formas: añadir supuestos sobre los errores, añadir más predictores (regresión lineal múltiple `y = β0 + β1x1 + β2x2 + β3x3 + ϵ`, en R `lm(y ~ x_1 + x_2 + x_3)`, con interacciones vía `x_2*x_3`) y transformar predictores (por ejemplo `z = x²` para capturar relaciones polinómicas que siguen siendo "lineales" en las nuevas variables; también logaritmos o umbrales). El mayor reto del modelador es que nunca conoce la verdad: puede asumir linealidad cuando el verdadero modelo es cuadrático o viceversa.

Los supuestos del modelo son: linealidad; errores normales con media 0; errores independientes; varianza constante del error en todo x; y que los predictores usados son los correctos. Se hace regresión para predecir una variable conociendo otras o para explicar/entender la relación. El ejercicio propuesto consiste en simular datos falsos en R ("jugar a ser Dios") para ver si el modelo recupera los β verdaderos.

## k-Nearest Neighbors (k-NN)
k-NN sirve cuando hay objetos ya clasificados o etiquetados y otros similares sin etiquetar que se quieren etiquetar automáticamente (por ejemplo, pacientes de "alto" o "bajo" riesgo de cáncer). La regresión lineal da salida continua, no categórica; puede adaptarse con umbrales (thresholds) que creen bins, pero no todo está en escala continua (etiquetas como "likely Democrat/Republican/independent").

La intuición: mirar los ítems más similares según sus atributos, observar sus etiquetas y dar al ítem no asignado el voto mayoritario; en caso de empate, se elige al azar. Hay que tomar dos decisiones: cómo definir similitud o cercanía y cuántos vecinos votan (el valor k, elegido por el científico de datos).

El proceso general: elegir la métrica de distancia; dividir en entrenamiento y prueba; elegir una métrica de evaluación (la tasa de error de clasificación, misclassification rate, es buena); ejecutar k-NN varias veces cambiando k; optimizar k por la mejor evaluación; y aplicar k al nuevo caso a predecir.

La definición de cercanía depende del contexto. Métricas citadas: distancia euclídea (si las variables están en la misma escala), similitud coseno (entre −1 y 1), distancia/similitud de Jaccard (entre conjuntos), distancia de Mahalanobis (tiene en cuenta la correlación y es invariante a escala), distancia de Hamming (entre cadenas de igual longitud) y distancia Manhattan (como un taxi por una cuadrícula). El escalado es "modeling danger": si se mide el salario en dólares, domina la distancia; en miles de dólares, las variables pesan parecido. En estadística esto se llama tu "prior". Con atributos mixtos se puede definir una métrica propia (por ejemplo, sumar 10 si el género de película difiere), que actúa como segundo parámetro de ajuste o como prior.

La fase de entrenamiento en k-NN es simplemente leer los datos etiquetados; en la prueba se finge no conocer la etiqueta. Sobre evaluación: a veces hay que penalizar más ciertos errores (los falsos negativos pueden ser peores que los falsos positivos, como en diagnóstico de cáncer), definiéndola junto a un experto del dominio. Hay un trade-off entre sensibilidad (sensitivity, también true positive rate o recall) y especificidad (specificity, true negative rate). Otras medidas: precision (no es lo mismo que specificity), accuracy (proporción de etiquetas correctas) y misclassification rate (1 − accuracy).

En R todo se reduce a `knn(train, test, cl, k=3)`. Con clases binarias conviene un k impar para evitar empates. Recorriendo k de 1 a 20 y mirando la tasa de error, en el ejemplo se elige k = 5 (menor error), y el individuo de 57 años con 37.000 $ se clasifica como "low". k-NN es un enfoque no paramétrico: no asume distribuciones ni estima parámetros, pero sí asume que existe un espacio de features con noción de distancia, que los datos de entrenamiento están etiquetados, que se elige k y que features y etiquetas están asociadas; siempre hay riesgo de overfitting. Tanto la regresión lineal como k-NN son aprendizaje supervisado (supervised learning): se observan x e y.

## k-means
k-means es la primera técnica de aprendizaje no supervisado (unsupervised learning): no se conocen las etiquetas y el algoritmo descubre los clusters. El objetivo es segmentar usuarios (estratificar, agrupar, clusterizar) para darles experiencias distintas, aplicar modelos específicos por grupo o separar efectos (como el modelado jerárquico). Construir bins a mano genera una explosión combinatoria (ejemplo: 10×2×50×10×3 = 30.000 celdas en un espacio de cinco dimensiones), de ahí la utilidad de un algoritmo donde k es el número de bins elegido de antemano.

El algoritmo (versión por defecto Hartigan-Wong): 1) elegir al azar k centroides en el espacio d-dimensional, cercanos a los datos pero distintos entre sí; 2) asignar cada punto al centroide más cercano; 3) mover los centroides al promedio de sus puntos asignados; 4) repetir hasta que las asignaciones no cambien o cambien poco. El científico de datos interpreta si hay una forma natural de describir los grupos y puede ajustar k. Problemas conocidos: elegir k es más arte que ciencia (con cota `1 ≤ k ≤ n`); hay problemas de convergencia (la solución puede no ser única); y la interpretabilidad puede fallar, a menudo el mayor problema. Aun así es rápido y de amplia aplicación (marketing, visión por computador, punto de partida de otros modelos). En R: `kmeans(x, centers, ...)`.

Perspectiva histórica: el algoritmo estándar se atribuye a Hugo Steinhaus y Stuart Lloyd (1957); James MacQueen acuñó el término "k-means" en 1967; se publicó fuera de Bell Labs en 1982. Versiones más recientes: Hartigan-Wong, Lloyd y Forgy, y k-means++ (2007, David Arthur y Sergei Vassilvitskii), que optimiza las semillas iniciales para evitar problemas de convergencia.

## Modelado y algoritmos a escala
Con datos pequeños basta muestrear o ejecutar el mismo modelo sobre datos sharded (repartidos entre máquinas) y mirar la distribución empírica de los estimadores: son soluciones estadísticas a retos de ingeniería. Para ajustar a gran escala, el reto se traduce en crear versiones paralelizadas o aproximaciones de los métodos de optimización (la regresión lineal depende de inversiones de matrices o sus aproximaciones). El ponente Peter Richtárik (Universidad de Edimburgo, 2013) señala que en Big Data los métodos clásicos con múltiples iteraciones no son aplicables porque el coste de una sola iteración es excesivo; se necesitan métodos simples, cuidadosos con memoria y escalables, que aprovechen arquitecturas paralelas (multicore, GPU, clústeres) (PDF p. 118).

## Ideas clave
- Hay tres clases de algoritmos en ciencia de datos: procesamiento de datos, optimización y machine learning (predecir, clasificar, agrupar).
- El científico de datos combina las culturas estadística (incertidumbre, interpretación) e ingenieril (construir y predecir); "modelo" y "algoritmo" se usan de forma intercambiable.
- Lo difícil no es implementar, sino saber qué algoritmo encaja con los atributos del problema; evita ser el del martillo buscando clavos.
- Regresión lineal: asume linealidad y ruido (a menudo normal); se ajusta por mínimos cuadrados y se evalúa con R², p-values y cross-validation para detectar overfitting.
- k-NN: clasificación no paramétrica por voto mayoritario de los vecinos; dependen críticamente la métrica de distancia, el escalado de variables y la elección de k.
- Evaluar implica elegir métrica (misclassification rate, sensibilidad/especificidad, precision, accuracy) según el coste de cada error, a veces con un experto de dominio.
- k-means: clustering no supervisado que itera asignación-recálculo de centroides; elegir k es arte, y la interpretabilidad suele ser el mayor problema.
- Escalar a Big Data exige optimización paralelizada y aproximada; el científico de datos debe conocer estos retos aunque queden fuera del alcance del libro.
