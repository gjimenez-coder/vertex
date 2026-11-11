# Algorithms (Algoritmos) — Estudio

## Tarjetas de repaso

P: ¿Qué es un algoritmo según el capítulo? / R: Un procedimiento o conjunto de pasos o reglas para realizar una tarea; es un bloque fundamental de la informática (ordenar, buscar, resolver grafos).

P: ¿Cuáles son las tres clases de algoritmos relevantes en ciencia de datos? / R: De procesamiento de datos (sorting, MapReduce, Pregel), de optimización para estimar parámetros (SGD, método de Newton, mínimos cuadrados) y de machine learning (predecir, clasificar, agrupar).

P: ¿Cómo describe el capítulo al científico de datos respecto a las dos culturas? / R: Como un híbrido entre estadístico e ingeniero de software; debe valorar la incertidumbre/interpretación estadística y la mentalidad ingenieril de construir y predecir.

P: ¿Por qué "modelo" y "algoritmo" se usan de forma intercambiable? / R: Un algoritmo es un conjunto de pasos y un modelo intenta describir el mundo, pero la regresión puede verse como ambas cosas, así que la frontera es borrosa.

P: ¿Qué advertencia da el capítulo sobre elegir técnicas? / R: No ser el del martillo buscando clavos: lo difícil no es implementar, sino saber qué algoritmo encaja con los atributos del problema.

P: ¿Qué asume y cómo se ajusta la regresión lineal? / R: Asume relación lineal entre la respuesta y los predictores; se ajusta por mínimos cuadrados minimizando la suma residual de cuadrados, con β̂ = (xᵀx)⁻¹xᵀy.

P: ¿Para qué sirven R², p-values y cross-validation en regresión? / R: R² es la proporción de varianza explicada; los p-values indican si un coeficiente es significativo frente a la hipótesis nula de β=0; cross-validation compara el error en train/test para detectar overfitting.

P: ¿Qué es el mean squared error y su relación con la función de pérdida? / R: Es el error cuadrático medio (se estima con ∑ei²/(n−2)); es un ejemplo de función de pérdida estándar en regresión lineal, compatible con máxima verosimilitud bajo ruido normal.

P: ¿Cuáles son los supuestos de la regresión lineal? / R: Linealidad; errores normales con media 0; errores independientes; varianza constante del error; y que los predictores usados son los correctos.

P: ¿En qué consiste k-NN y qué dos decisiones exige? / R: Clasifica un ítem sin etiqueta por voto mayoritario de sus vecinos más similares; hay que decidir cómo medir la cercanía (métrica de distancia) y cuántos vecinos votan (el valor k).

P: ¿Qué métricas de distancia menciona el capítulo para k-NN? / R: Euclídea, similitud coseno, Jaccard, Mahalanobis, Hamming y Manhattan; el escalado de variables es "modeling danger" y actúa como prior.

P: ¿Qué supuestos tiene k-NN como método no paramétrico? / R: No asume distribuciones ni estima parámetros, pero sí asume un espacio de features con noción de distancia, datos de entrenamiento etiquetados, una k elegida y asociación entre features y etiquetas.

P: ¿Qué es k-means y cómo funciona su iteración? / R: Es clustering no supervisado; elige k centroides al azar, asigna cada punto al centroide más cercano, mueve los centroides al promedio de sus puntos y repite hasta que las asignaciones no cambien o cambien poco.

P: ¿Cuáles son los problemas conocidos de k-means? / R: Elegir k es más arte que ciencia (1 ≤ k ≤ n), hay problemas de convergencia (solución no siempre única) y la interpretabilidad puede fallar, a menudo el mayor problema.

P: ¿Qué exige escalar modelos a Big Data? / R: Versiones paralelizadas o aproximaciones de los métodos de optimización, métodos simples, cuidadosos con la memoria y escalables, porque el coste de una sola iteración clásica es excesivo.

## Preguntas de autoevaluación

P: ¿Qué diferencias culturales distinguen a estadísticos de ingenieros según el capítulo? / R: Los estadísticos buscan sentido en los parámetros, aportan intervalos de confianza y hacen supuestos explícitos sobre el proceso generador de datos; los ingenieros tratan el modelo como caja negra, ajustan para optimizar la predicción y muchos algoritmos de ML (k-means, k-NN) no tienen noción de incertidumbre. (Sección "Tres clases de algoritmos y las dos culturas")

P: ¿Por qué se divide por n−2 al estimar la varianza del error en regresión lineal? / R: Porque se resta el número de parámetros del modelo (2) para obtener un estimador insesgado de la varianza del error. (Sección "Regresión lineal")

P: ¿De qué tres formas se extiende el modelo de regresión lineal simple? / R: Añadiendo supuestos sobre los errores, añadiendo más predictores (regresión lineal múltiple, con interacciones) y transformando predictores (por ejemplo z = x², logaritmos o umbrales). (Sección "Regresión lineal")

P: ¿Por qué el escalado de variables es crítico en k-NN? / R: Porque cambia qué variable domina la distancia; medir el salario en dólares hace que domine, y en miles de dólares las variables pesan parecido. Es "modeling danger" y equivale a fijar un prior. (Sección "k-Nearest Neighbors")

P: ¿Qué trade-off aparece al evaluar un clasificador y por qué importa el coste de cada error? / R: El trade-off entre sensibilidad (recall/true positive rate) y especificidad (true negative rate); a veces hay que penalizar más ciertos errores, como los falsos negativos en diagnóstico de cáncer, definiendo la métrica junto a un experto del dominio. (Sección "k-Nearest Neighbors")

P: ¿Qué diferencia a k-means de la regresión lineal y k-NN en cuanto al tipo de aprendizaje? / R: k-means es aprendizaje no supervisado (no se conocen las etiquetas y descubre los clusters), mientras que regresión lineal y k-NN son aprendizaje supervisado (se observan x e y). (Secciones "k-means" y "k-Nearest Neighbors")

P: ¿Qué aporta la versión k-means++ frente al algoritmo estándar? / R: Optimiza las semillas (centroides iniciales) para evitar los problemas de convergencia; fue propuesta en 2007 por David Arthur y Sergei Vassilvitskii. (Sección "k-means")

## Puntos a dominar

- Distinguir las tres clases de algoritmos (procesamiento, optimización, machine learning) y para qué sirve cada una.
- Explicar la tensión entre la cultura estadística y la ingenieril y por qué "modelo" y "algoritmo" se solapan.
- Reconstruir el ajuste de la regresión lineal por mínimos cuadrados y justificar sus supuestos.
- Interpretar R², p-values y cross-validation para juzgar un modelo y detectar overfitting.
- Ejecutar mentalmente k-NN: elegir métrica de distancia, escalar variables, elegir k impar en clases binarias y seleccionar k por la tasa de error.
- Elegir la métrica de evaluación adecuada (misclassification rate, sensibilidad/especificidad, precision, accuracy) según el coste de cada error.
- Describir el ciclo asignación-recálculo de k-means y sus limitaciones (elección de k, convergencia, interpretabilidad).
- Entender por qué escalar a Big Data exige optimización paralelizada y aproximada.
