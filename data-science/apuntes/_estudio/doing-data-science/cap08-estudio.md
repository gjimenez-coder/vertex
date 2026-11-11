# Recommendation Engines: Building a User-Facing Data Product at Scale (Motores de recomendación: construir un producto de datos de cara al usuario a escala) — Estudio

## Tarjetas de repaso

P: ¿Por qué se describe el motor de recomendación como "el producto de datos por excelencia"?
R: Porque casi todos lo han usado (Amazon, Netflix) y convierte el comportamiento del usuario en combustible que se retroalimenta y mejora las recomendaciones.

P: ¿Cómo se representan usuarios e ítems en un motor de recomendación?
R: Como un grafo bipartito: un nodo por usuario y por ítem, con aristas (que pueden tener pesos positivos, negativos o en escala) cuando un usuario expresa una opinión sobre un ítem.

P: ¿En qué consiste el algoritmo de vecinos más próximos para recomendar?
R: Buscas al usuario B más cercano a A que tenga opinión, asumes que A opina igual que B y recomiendas a A algo que B valoró y le gustó pero que A no ha calificado.

P: ¿Qué es la distancia de Jaccard y para qué sirve aquí?
R: Para opiniones binarias, `1 – (cosas que gustan a ambos / cosas que gustan a cualquiera de los dos)`; es una métrica de distancia entre usuarios.

P: ¿Cuáles son los dos mayores problemas de vecinos más próximos?
R: El sobreajuste y la maldición de la dimensionalidad.

P: ¿Qué ventaja aporta la regresión lineal por ítem frente a k-NN?
R: Resuelve la ponderación de atributos, porque los coeficientes de la regresión son directamente los pesos de cada atributo.

P: ¿Qué inconvenientes tiene construir un modelo de regresión lineal por cada ítem?
R: Cada modelo solo sirve para un ítem (necesitas tantos modelos como ítems), no aprovecha la información de otros ítems y persiste el sobreajuste.

P: ¿Cómo se controla el sobreajuste en la regresión lineal por ítem?
R: Con un prior bayesiano que penaliza los coeficientes grandes mediante un término que depende de un parámetro `λ`, previa normalización de las variables.

P: ¿Qué riesgo hay si `λ` se hace enorme?
R: Todos los coeficientes van a cero y te quedas sin modelo.

P: ¿Qué es el SVD y cómo descompone la matriz?
R: Descompone `X` de m×n y rango k como `X = U·S·Vτ`, con `U` m×k, `S` k×k diagonal y `V` k×n, y columnas de `U` y `V` ortogonales por pares.

P: ¿Qué representan los valores de la diagonal de `S` en el SVD?
R: Son los valores singulares y miden la importancia de cada variable latente; el mayor es el más importante.

P: ¿Por qué no se rellenan con 0 las celdas vacías de `X` antes del SVD?
R: Porque el 0 podría significar algo y el SVD no admite valores faltantes; se rellenan con la valoración media de cada ítem.

P: ¿Qué minimiza PCA y qué propiedad clave logra?
R: Minimiza el error cuadrático `argmin Σ(xi,j − ui·vj)²` buscando `U` y `V` con `X ≈ U·Vτ`; produce atributos latentes no correlacionados, eliminando la redundancia de k-NN.

P: ¿En qué consiste el algoritmo de mínimos cuadrados alternados (ALS)?
R: Elige `V` aleatoria, optimiza `U` con `V` fija, optimiza `V` con `U` fija y repite hasta que los coeficientes cambien menos que un `ϵ` (convergencia).

P: ¿Por qué ALS es paralelizable?
R: Porque fijando `V`, actualizar `U` se hace usuario por usuario como un problema de mínimos cuadrados con solución cerrada que depende solo de las preferencias de cada usuario.

## Preguntas de autoevaluación

P: ¿Cómo evolucionó Hunch desde su enfoque inicial hasta el modelo que llevó a su compra por eBay?
R: Empezó haciendo preguntas divertidas (con unas 20 predecía el resto con 80% de acierto) y evolucionó hacia un modelo de API que rastrea la Web en vez de preguntar, usable por terceros para personalizar sitios. (Sección "Lo que necesitas saber")

P: Enumera al menos cuatro problemas del algoritmo de vecinos más próximos.
R: Maldición de la dimensionalidad, sobreajuste, atributos correlacionados, dispersión, errores de medición, complejidad computacional, sensibilidad de las métricas, cambio de preferencias en el tiempo y coste de actualizar el modelo. (Sección "El algoritmo de vecinos más próximos y sus problemas")

P: ¿Por qué los metadatos del usuario se tratan como "ítems" en la regresión lineal por ítem?
R: Porque así el mismo mecanismo que predice gustos sirve para predecir atributos faltantes, como el sexo. (Sección "Más allá de vecinos: regresión lineal por ítem")

P: ¿Cómo se elige el valor del parámetro `λ` y por qué hay que normalizar antes?
R: `λ` se elige experimentalmente (entrenar, evaluar con distintos valores y ajustar); se normaliza porque con escalas distintas la penalización castigaría más a unos coeficientes que a otros. (Sección "Más allá de vecinos: regresión lineal por ítem")

P: ¿Cómo se usa el SVD para generar predicciones y comprimir la información?
R: Se ordenan las columnas por valor singular decreciente y se descartan las menos importantes (eligiendo `d`); al multiplicar `U·S·Vτ` con las celdas vacías rellenadas por la media se obtiene una aproximación-predicción de `X`. (Sección "El problema de la dimensionalidad: SVD")

P: ¿Qué significa que los atributos latentes de PCA queden no correlacionados y por qué importa?
R: Significa que no hay información redundante entre ellos, lo que elimina la redundancia de atributos correlacionados que aquejaba a k-NN. (Sección "Análisis de componentes principales (PCA)")

P: ¿Cuál es la contradicción del prior en ALS respecto a la convergencia?
R: El algoritmo converge si el prior es suficientemente grande, pero un prior enorme lleva todos los coeficientes a cero; cuanto más te importan los coeficientes, menos te importa `X`, cuando en realidad solo te importa `X`. (Sección "Mínimos cuadrados alternados (ALS)")

P: ¿Qué cuestiones plantea el experimento mental de las "burbujas de filtro"?
R: Qué implica usar minimización del error para predecir preferencias, cómo afecta la presentación a la retroalimentación y si se cae en máximos locales con efectos de "el rico se hace más rico" donde ciertos ítems ganan ventaja injusta. (Sección "Experimentos mentales y ejercicio")

## Checklist

Pasos para construir un motor de recomendación escalable según el capítulo:

- [ ] Representar usuarios e ítems como un grafo bipartito y apilar los vectores de atributos en la matriz `U`.
- [ ] Partir de vecinos más próximos como línea base y probar varias métricas de distancia (Jaccard, coseno, euclídea) entendiendo por qué cambian los resultados.
- [ ] Usar k-NN con k>1 (p. ej. k=5) en vez de k=1 para reducir el ruido.
- [ ] Al pasar a regresión lineal por ítem, normalizar las variables antes de entrar al modelo.
- [ ] Añadir un prior bayesiano (`λ`) y elegirlo experimentalmente, evitando valores enormes que anulen los coeficientes.
- [ ] Para muchas dimensiones, rellenar celdas vacías con la valoración media del ítem (no con 0) antes de aplicar SVD.
- [ ] Elegir el número `d` de atributos latentes (típicamente unos 100, según permita el coste de cómputo).
- [ ] Resolver `U` y `V` con ALS iterativo y paralelizar el cálculo por usuario entre varias máquinas.
- [ ] Hacer validación cruzada (dejar fuera una parte y comprobar el resultado) para detectar sobreajuste.
- [ ] Reflexionar sobre efectos de burbujas de filtro y "el rico se hace más rico" al presentar recomendaciones.
