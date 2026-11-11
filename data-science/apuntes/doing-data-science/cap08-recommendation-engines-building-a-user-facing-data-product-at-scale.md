# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 8 — Recommendation Engines: Building a User-Facing Data Product at Scale (Motores de recomendación: construir un producto de datos de cara al usuario a escala)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Este capítulo, narrado a partir de la charla invitada de Matt Gattis (CTO cofundador de Hunch.com, ex-MIT y ex-SiteAdvisor), presenta los motores de recomendación como el "producto de datos por excelencia": algo que casi todos han usado en Amazon o Netflix y que convierte el comportamiento del usuario en combustible que retroalimenta y mejora las recomendaciones. Construir uno de punta a punta exige álgebra lineal y saber programar, y revela los retos que impone el Big Data cuando un problema intuitivo se complica al implementarlo a escala.

Hunch empezó haciendo preguntas divertidas a los usuarios y descubrió que con unas 20 preguntas podía predecir el resto con un 80% de acierto (preguntas al estilo MBTI: competitivo frente a no competitivo, introvertido frente a extrovertido, etc.). Luego evolucionó hacia un modelo de API que rastrea la Web en vez de preguntar, y que terceros podían usar para personalizar sitios, propuesta que llevó a que eBay comprara Hunch.

Sales sabiendo cómo pasar de un enfoque ingenuo (vecinos más próximos) a uno escalable: primero regresión lineal por ítem con regularización bayesiana para el sobreajuste, luego reducción de dimensiones con SVD y PCA para manejar decenas de miles de ítems, y finalmente mínimos cuadrados alternados (ALS) como método iterativo y paralelizable para hallar las matrices de factores latentes. Una frase de Matt resume el espíritu del equipo: "Formar un equipo de datos es como planear un atraco" (PDF p. 228), porque hacen falta personas con habilidades muy distintas.

## Un motor de recomendación en el mundo real
El planteamiento: tienes un conjunto de usuarios `U` y un conjunto de ítems a recomendar `V`. Como contó Kyle Teague en el capítulo 6, esto se representa como un grafo bipartito (Figura 8-1): un nodo por usuario y por ítem, con aristas cuando un usuario ha expresado una opinión sobre un ítem. Las aristas pueden tener pesos: positivos, negativos, en escala continua o con muchos valores (sistema de estrellas). Aquí se tratan como valoraciones numéricas.

Dispones de datos de entrenamiento con algunas preferencias de algunos usuarios sobre algunos ítems, y a partir de ellos quieres predecir las demás preferencias: esa es la salida del motor. Puede haber metadatos de usuarios (sexo, edad) y de ítems (color del producto). Cada usuario se representa como un vector de atributos: solo metadatos, solo preferencias (vector disperso, porque no se conocen todas sus opiniones) o ambos. Apilando los vectores se obtiene una gran matriz de usuarios, que por abuso de notación también se llama `U`.

## El algoritmo de vecinos más próximos y sus problemas
Repaso del vecino más próximo (capítulo 3): para predecir si al usuario A le gusta algo, buscas al usuario B más cercano a A que tenga opinión y asumes que A opina igual que B; luego recomiendas a A algo que B valoró y le gustó pero que A no ha calificado. Necesitas una métrica de distancia: para opiniones binarias, la distancia de Jaccard, es decir `1 – (cosas que gustan a ambos / cosas que gustan a cualquiera de los dos)`; también sirven la similitud del coseno o la distancia euclídea. El resultado cambia según la métrica, y eso es bueno: conviene probar varias funciones de distancia y entender por qué cambian los resultados.

Vecinos más próximos tiene problemas serios:

- Maldición de la dimensionalidad: con demasiadas dimensiones, los vecinos más próximos quedan en realidad muy lejos.
- Sobreajuste: el más cercano puede ser puro ruido; usar k-NN con, por ejemplo, k=5 en vez de k=1 reduce ese ruido.
- Atributos correlacionados: muchos atributos están muy correlacionados (edad y conservadurismo), lo que duplica el peso de información redundante; mejor proyectar a un espacio de menor dimensión.
- Importancia relativa de los atributos: unos informan más que otros, conviene ponderarlos (por ejemplo con covarianzas).
- Dispersión: si el vector o la matriz es demasiado disperso, Jaccard no significa nada por falta de solapamiento.
- Errores de medición (o de reporte): la gente miente.
- Complejidad computacional: tiene coste de cálculo.
- Sensibilidad de las métricas: la distancia euclídea tiene un problema de escala; las distancias en edad eclipsan a las demás, y la relación puede no ser lineal (¿convendría agrupar por franjas de edad?).
- Las preferencias cambian con el tiempo, lo que queda fuera del modelo (en eBay, comprar una impresora solo genera deseo de tinta un tiempo).
- Coste de actualizar el modelo al añadir más datos.

Los dos mayores problemas son el sobreajuste y la maldición de la dimensionalidad.

## Más allá de vecinos: regresión lineal por ítem
Una simplificación del algoritmo real: construir un modelo de regresión lineal independiente por cada ítem. Cada modelo predice, dados los atributos de un usuario, si le gustaría ese ítem (uno para Mad Men, otro para Bob Dylan). Un punto sutil: los metadatos se tratan también como "ítems", así que el mismo mecanismo que predice gustos sirve para predecir atributos faltantes (por ejemplo, el sexo). Con tres atributos numéricos por usuario, la preferencia estimada es `pi = β1·f1,i + β2·f2,i + β3·f3,i + ϵ`, cuyos coeficientes se estiman por regresión lineal.

Ventaja: esto resuelve el problema de la ponderación de atributos, porque los coeficientes de la regresión son los pesos. Inconvenientes: cada modelo solo sirve para un ítem (necesitas tantos modelos como ítems) y no aprovecha la información de otros ítems. Además persiste el sobreajuste, que aquí aparece como coeficientes enormes cuando faltan datos (si dos variables son casi iguales, una puede llevar coeficiente 100.000 y la otra –100.000 sin aportar nada).

La solución es un prior bayesiano que impide que los pesos se disparen, añadiendo un término de penalización por coeficientes grandes; esto equivale a sumar una matriz prior a la de covarianzas y depende de un único parámetro `λ`. ¿Cómo elegir `λ`? Experimentalmente: entrenar, evaluar con distintos valores y ajustar. Hay que normalizar las variables antes de entrar al modelo, porque si están en escalas distintas la penalización castigaría más a unos coeficientes que a otros; la forma de normalizar es, de nuevo, equivalente a imponer un prior. Cuidado: si `λ` se hace enorme, todos los coeficientes van a cero y te quedas sin modelo.

## El problema de la dimensionalidad: SVD
Para manejar decenas de miles de ítems se usan la descomposición en valores singulares (SVD) y el análisis de componentes principales (PCA). La idea de los "atributos latentes" se parece a cómo las personas inventan conceptos como la "coolness": no se mide directamente, sino que resume y pondera muchos rasgos observados. Aquí la máquina decide qué atributos latentes importan: los que explican la varianza de las respuestas. El objetivo es un modelo en un subespacio de baja dimensión que recoja la "información de gusto". Como las preguntas suelen ser binarias (sí/no), Hunch creó una variable por pregunta y vio que las preguntas de comparación revelan mejor las preferencias.

Conviene repasar álgebra lineal (rango —que nada tiene que ver con los algoritmos de ranking—, ortogonalidad, transpuesta, base, span, descomposición de matrices). El SVD descompone una matriz `X` de m×n y rango k como `X = U·S·Vτ`, donde `U` es m×k, `S` es k×k diagonal y `V` es k×n, con columnas de `U` y `V` ortogonales por pares. `X` es el conjunto original con las valoraciones: m usuarios, n ítems; cada fila de `U` es un usuario y cada fila de `V` un ítem. Los valores de la diagonal de `S` son los valores singulares y miden la importancia de cada variable latente (el mayor, el más importante).

Como las columnas son ortogonales, puedes ordenarlas por valor singular decreciente y quedarte con una aproximación de menor rango descartando parte de `S` (y las partes correspondientes de `U` y `V`): así eliges el número `d` de variables latentes y "comprimes" `X`. A menudo la variable latente más importante resulta ser algo como si alguien es hombre o mujer. Para recomendar: rellenas las celdas vacías de `X` con la valoración media de cada ítem (no con 0, porque podría significar algo y el SVD no admite valores faltantes), calculas el SVD y, al multiplicar `U·S·Vτ`, obtienes una aproximación-predicción de `X`. Pero el SVD no arregla los datos faltantes ni la complejidad: es muy caro computacionalmente.

## Análisis de componentes principales (PCA)
Otro enfoque: buscar `U` y `V` sin necesidad de `S`, de modo que `X ≈ U·Vτ`. Se minimiza el error cuadrático entre `X` real y la aproximación: `argmin Σ(xi,j − ui·vj)²`, donde `ui` es la fila de `U` del usuario `i` y `vj` la de `V` del ítem `j` (los ítems incluyen metadatos). El producto escalar `ui·vj` es la preferencia predicha, que debe acercarse a la real `xi,j`. Es el mismo error cuadrático medio de la regresión lineal: si el modelo acierta en lo conocido, acertará en lo desconocido. Eliges `d`, el número de atributos latentes, típicamente unos 100 (más de las 20 preguntas que ya bastaban para conocer a alguien, y tanto como permita el coste de cómputo).

Teorema: los atributos latentes resultantes quedan no correlacionados, lo que elimina la redundancia que aquejaba a k-NN. Esbozo de la prueba: fijado el producto `U·V = X` que minimiza el error, se minimiza además la suma de cuadrados de las entradas de `U` y `V`; se puede modificar con `U·G·G⁻¹·V = X`. Con transformaciones que preservan el volumen (determinante 1), minimizar las entradas de `U` equivale a minimizar la superficie de un paralelepípedo de volumen fijo, lo que se logra haciendo sus lados ortogonales entre sí: atributos latentes no correlacionados. Las filas de `V` también quedan ortogonales. Esta forma `U·V` se parece tanto al SVD que algunos la llaman "algoritmo SVD" aunque no lo sea del todo.

## Mínimos cuadrados alternados (ALS)
El problema de optimización no tiene fórmula cerrada única como los mínimos cuadrados ordinarios; se resuelve iterativamente (como el descenso de gradiente). Si el problema es convexo, converge a un óptimo global, y la regularización ayuda a forzar la convexidad. El algoritmo:

- Elige una `V` aleatoria.
- Optimiza `U` manteniendo `V` fija.
- Optimiza `V` manteniendo `U` fija.
- Repite hasta que los coeficientes cambien menos que un `ϵ` elegido (convergencia).

Teorema (sin prueba): el algoritmo converge si el prior es suficientemente grande, pero un prior enorme lleva todos los coeficientes a cero; optimizar el prior ajustándolo a conveniencia es contradictorio, y cuanto más te importan los coeficientes, menos te importa `X`, cuando en realidad solo te importa `X`.

La clave es que, fijando `V`, actualizar `U` se hace usuario por usuario y es un problema de mínimos cuadrados lineal con solución cerrada: `ui = (V*,iτ·V*,i)⁻¹·V*,iτ·P*i`, donde `V*,i` es el subconjunto de `V` con preferencias del usuario `i`. Invertir es fácil porque la matriz es d×d (pequeña) y hay pocas preferencias por usuario. Fijar `U` y optimizar `V` es análogo. Como cada usuario depende solo de sus propias preferencias, el cálculo se puede paralelizar en muchas máquinas.

Observaciones finales: hay muchas variantes; puedes añadir usuarios o datos y seguir optimizando `U` y `V`, actualizando solo a quienes lo necesiten para ahorrar cómputo. Como en todo modelo de ML, hay que hacer validación cruzada (dejar fuera una parte y comprobar el resultado) para detectar sobreajuste.

## Experimentos mentales y ejercicio
El capítulo plantea el experimento mental de las "burbujas de filtro" (filter bubbles): ¿qué implica usar minimización del error para predecir preferencias, y cómo afecta la presentación de las recomendaciones a la retroalimentación? ¿Se puede caer en máximos locales con efectos de "el rico se hace más rico", donde mostrar ciertos ítems al principio les da ventaja injusta y se vuelven populares por suerte? ¿Cómo corregirlo? Como ejercicio, propone construir un sistema de recomendación con el conjunto de datos de GetGlue del capítulo 6, adaptando el código Python de Matt (que implementa ALS con numpy sobre un conjunto pequeño).

## Ideas clave
- Un motor de recomendación es el producto de datos por excelencia: usa el comportamiento del usuario como combustible que se retroalimenta.
- Usuarios e ítems forman un grafo bipartito; el objetivo es predecir preferencias desconocidas a partir de las conocidas.
- Vecinos más próximos es intuitivo pero sufre maldición de la dimensionalidad, sobreajuste, atributos correlacionados, dispersión y coste de cómputo.
- La regresión lineal por ítem resuelve la ponderación de atributos (los coeficientes son pesos), pero necesita un prior/penalización (`λ`) y normalización para controlar el sobreajuste.
- SVD (`X = U·S·Vτ`) descubre atributos latentes ordenados por importancia y permite comprimir eligiendo `d`, pero es caro y no maneja datos faltantes.
- PCA busca `U` y `V` minimizando el error cuadrático y produce atributos latentes no correlacionados.
- ALS resuelve `U` y `V` iterativamente, con solución cerrada d×d por usuario/ítem y fácilmente paralelizable.
- Siempre hay que validar de forma cruzada, y conviene reflexionar sobre efectos como las burbujas de filtro y el "rico se hace más rico".
