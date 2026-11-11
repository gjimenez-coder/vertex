# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 5 — Logistic Regression (Regresión logística)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página del PDF. El capítulo recoge una charla del ponente invitado Brian Dalessandro; las ideas se atribuyen a quien las expone.

## Lo que necesitas saber

El capítulo lo aporta Brian Dalessandro, VP de data science en Media 6 Degrees (M6D), startup de publicidad online en Nueva York. Vino a hablar de regresión logística y de evaluación de modelos, y arrancó con dos experimentos mentales sobre qué es la ciencia en la ciencia de datos.

La tesis central es doble. Primero, elegir un clasificador no es solo cuestión de precisión: hay que navegar restricciones reales (tiempo de ejecución, interpretabilidad, escalabilidad, tu propia comprensión del algoritmo). Segundo, la regresión logística es una elección sólida para clasificación binaria a gran escala porque es rápida, escalable y devuelve probabilidades directamente interpretables.

Sales sabiendo: cómo plantear un problema de clasificación y sus cinco decisiones (clasificador, optimización, función de pérdida, features, métrica); la matemática de la regresión logística (función inverse-logit, estimación por máxima verosimilitud, Newton y Stochastic Gradient Descent); y cómo evaluar según el contexto (ranking con AUC/lift, clasificación con precisión/recall/F-score, estimación de densidad con MSE).

## Los dos experimentos mentales

Brian plantea: ¿en qué cambiaría la ciencia de datos si existiera una "teoría unificada del todo" que explicara el mundo de forma simbólica? Sugiere pensar las ciencias como un continuo: la física a la derecha (predecir dónde aterriza el Mars Rover) y, al desplazarse a la izquierda, más caos y aleatoriedad (economía, marketing, finanzas). El consenso es que el mundo real no está tan bien entendido ni se espera que lo esté.

Segundo: ¿en qué sentido la ciencia de datos merece el nombre de "ciencia"? El data scientist traduce la visión humana a un modelo matemático dentro de restricciones operativas: definir bien el problema, argumentar una métrica y optimizarla. Hay arte en traducir problemas humanos al contexto matemático y de vuelta. La ciencia está en que cada decisión de diseño se formula como una hipótesis que se valida o refuta con experimentación rigurosa: conservar el mejor modelo actual, montar un experimento donde el nuevo compite contra él, y repetir sin overfitting.

## Clasificadores

La clasificación mapea puntos de datos a un conjunto finito de etiquetas o a la probabilidad de una etiqueta. Ya se vieron Naive Bayes y k-NN; a partir de aquí el foco es clasificación binaria (0 o 1). Otros algoritmos existen (árboles de decisión y random forests en el Capítulo 7; SVM y redes neuronales no se cubren).

Dados los datos, un problema real y restricciones, hay que decidir cinco cosas: (1) qué clasificador usar, (2) qué método de optimización, (3) qué función de pérdida minimizar, (4) qué features extraer, (5) qué métrica de evaluación. Se podrían probar todos los clasificadores y quedarse con el mejor, pero normalmente las restricciones pesan.

Restricciones comunes a casi todos los algoritmos:

- Runtime (tiempo de ejecución): en M6D actualizan unos 500 modelos al día y los modelos son decisiones de puja, así que importa cuánto tarda actualizar un modelo y, sobre todo, cuánto tarda en decidir con él ya entrenado. k-NN es lento en runtime (hay que tener todos los datos en memoria y buscar los k vecinos más cercanos). Los modelos lineales son muy rápidos: basta guardar el vector de coeficientes y hacer un producto escalar con el vector de features del usuario.
- Tú mismo: una restricción infravalorada es si de verdad entiendes el algoritmo. No hace falta dominar todos; un error común de quien no conoce bien un algoritmo es hacer overfitting creyendo que lo está ajustando.
- Interpretabilidad: a veces hay que poder explicar el modelo al negocio. Los árboles de decisión son fáciles de interpretar; los random forests no, aunque sean casi lo mismo. Por ley, las compañías de tarjetas de crédito deben explicar sus denegaciones, así que un árbol tiene más sentido que un random forest.
- Escalabilidad: tiempo de aprendizaje (entrenar), tiempo de scoring (puntuar un usuario nuevo en producción) y almacenamiento del modelo.

Se cita el paper *An Empirical Comparison of Supervised Learning Algorithms*: los modelos más simples son más interpretables pero peores en rendimiento; qué algoritmo funciona mejor depende del problema y de las restricciones.

## Caso M6D: modelos de clics

M6D tiene tres problemas núcleo: ingeniería de features, predicción de conversión a nivel de usuario (cuándo alguien hará clic) y puja (cuánto vale mostrar un anuncio a un usuario). El caso se centra en el segundo, y usan regresión logística por ser escalable y buena para salidas binarias como el clic.

M6D registra los sitios visitados sin mirar el contenido: hashean la URL a una cadena aleatoria y acumulan un vector por usuario. Con todos los usuarios forman una matriz dispersa (filas = usuarios, columnas = sitios; 1 si visitó el sitio). Para convertirlo en clasificación añaden una columna de etiquetas: 1 si hizo clic en el anuncio de zapatos, 0 si no.

Esto reduce el problema a uno ya resuelto: es idéntico a la clasificación de spam (salida binaria con matriz dispersa grande de predictores). La salida de la regresión logística es una probabilidad de clic; se puede usar directa o con un umbral (p. ej. 0.75) para decidir si mostrar el anuncio. A diferencia de la regresión lineal, no busca predecir el valor real (0 o 1) sino emitir una probabilidad; además la lineal daría predicciones por debajo de 0 y por encima de 1, no interpretables como probabilidades.

## La matemática subyacente

La belleza de la regresión logística es que su salida está acotada en [0,1], por lo que se interpreta como probabilidad. Se usa la función inverse-logit:

```
P(t) = logit⁻¹(t) = 1 / (1 + e⁻ᵗ) = eᵗ / (1 + eᵗ)
```

Cuando t es grande, e⁻ᵗ es diminuto y el valor tiende a 1; cuando t es pequeño, tiende a 0. La función logit hace lo inverso: `logit(p) = log(p / (1 − p))`, llevando valores de [0,1] a toda la recta real.

El modelo expresa el logit de la probabilidad de clic como función lineal de las features (las URLs que visitó el usuario i):

```
logit( P(cᵢ=1 | xᵢ) ) = α + βᵀxᵢ
```

El parámetro α es la base rate: la probabilidad incondicional de clic sin saber nada del usuario, que corresponde al click-through rate (del orden del 1%). El vector β es la pendiente, tan largo como el número de features, y marca cuánto cada feature aumenta o disminuye la probabilidad de clic.

## Estimación de α y β

El objetivo es hallar los mejores α y β con el entrenamiento mediante estimación por máxima verosimilitud (MLE), usando optimización convexa porque la función de verosimilitud es convexa. No hay solución cerrada como en la regresión lineal. Se asume independencia entre usuarios (el clic de uno no afecta al de otro), lo que permite escribir la verosimilitud como producto de densidades. Como maximizar la verosimilitud equivale a maximizar su logaritmo, se minimiza la log-verosimilitud negativa.

Bajo condiciones razonables (variables no linealmente dependientes, Hessiana definida positiva), los dos métodos convergen a un máximo global:

- Método de Newton: aproxima la función con los primeros términos de su serie de Taylor; usa gradiente local (primera derivada) y la matriz Hessiana (segunda derivada): `Θₙ₊₁ = Θₙ − γ H⁻¹ ∇Θ`. Invertir la Hessiana k×k es malo con muchísimas features (10.000). En la práctica nunca se invierte, se resuelve `Ax = y`, más estable.
- Stochastic Gradient Descent (SGD): aproxima el gradiente con una observación a la vez y actualiza los parámetros con cada dato nuevo. No hay inversión de matrices y funciona bien con datos enormes y features dispersas (clave en Mahout y Vowpal Wabbit). Lo malo: no es gran optimizador y depende mucho del tamaño de paso.

En la práctica no hay que programar esto: R lo implementa. Con una matriz `train`, la orden es:

```r
fit <- glm(click ~ url_1 + url_2 + url_3 + url_4 + url_5,
           data = train, family = binomial(logit))
```

## Evaluación

La métrica depende del contexto, incluso dentro de la propia regresión logística.

Como modelo de ranking (ordenar anuncios por probabilidad de clic, sin importar el valor absoluto):
- AUC (área bajo la curva ROC): la curva ROC traza la tasa de verdaderos positivos frente a la de falsos positivos al variar el umbral. El área bajo ella mide el éxito de un clasificador o compara dos. Se cita el paper de Tom Fawcett, "Introduction to ROC Analysis".
- Área bajo la curva de lift acumulado: habitual en marketing directo; capta cuántas veces es mejor usar el modelo que no usarlo (elegir al azar).

Aviso de feedback loop: si pones el anuncio de gomina encima del de desodorante y recibe más clics, ¿es por la posición o por el producto? Solución: registrar siempre la posición/rank mostrado y usarla como predictor, estimando un "normalizador de posición". Google tiene una división entera, Ads Quality, dedicada a esto.

Como modelo de clasificación (etiquetar 1 si la probabilidad predicha > 0.5, para minimizar la tasa de error):
- Lift: cuánta más gente compra o hace clic gracias al modelo en producción.
- Accuracy: con qué frecuencia se predice el resultado correcto.
- Precision: verdaderos positivos / (verdaderos positivos + falsos positivos).
- Recall: verdaderos positivos / (verdaderos positivos + falsos negativos).
- F-score: media armónica de precision y recall: `(2 × P × R)/(P + R)`.

Para estimación de densidad (cuando se necesita la probabilidad real, no un score relativo): mean squared error, root squared error y mean absolute error. El AUC es "base rate invariant" y compara mejor que las curvas de lift. Importante: un modelo puede dar buen ranking pero malas estimaciones de probabilidad (p. ej. estimar .7, .5, .3 cuando lo real es .03, .02, .01). En publicidad, si cada impresión cuesta $c y cada conversión da $q, se apunta a conversiones con `P(conversión|X)·$q > $c`, lo que exige un MSE pequeño en la estimación.

Usando A/B testing: la optimización ajusta parámetros contra una métrica (accuracy, MSE), pero el objetivo real puede ser otro (ingresos). Se desvía un grupo de usuarios a una versión del algoritmo y otro a otra, y se compara la métrica que de verdad importa. Se amplía en el Capítulo 11.

## Ejercicio Media 6 Degrees

M6D proporciona un dataset (en el repo oreillymedia/doing_data_science) para explorar y evaluar modelos logísticos en R. El código de Brian Dalessandro: separa train/test (split .65), define funciones para un gráfico GAM suavizado (`plotrel`), para el cálculo y gráfico del MAE ponderado (`getmae`, con la librería `plyr`), y para el AUC (`get_auc`, con `ROCR`). `getxval` obtiene métricas por validación cruzada. El bloque principal ajusta un `glm` con todas las variables, evalúa cada feature individualmente, hace selección hacia delante (greedy forward selection) y dibuja curvas ROC para `LAST_SV`, `LAST_BUY` y `num_checkins`.

## Ideas clave

- Elegir clasificador no es solo precisión: runtime, tu comprensión del algoritmo, interpretabilidad y escalabilidad son restricciones decisivas.
- Un problema de clasificación exige cinco decisiones: clasificador, optimización, función de pérdida, features y métrica.
- La regresión logística usa la función inverse-logit para acotar la salida en [0,1] y devolver probabilidades, no valores 0/1.
- El modelo expresa `logit(P) = α + βᵀx`; α es la base rate (≈1% de click-through) y β la pendiente por feature.
- Se ajusta por máxima verosimilitud minimizando la log-verosimilitud negativa, con Newton o Stochastic Gradient Descent; SGD escala mejor con datos enormes y dispersos.
- La métrica de evaluación depende del uso: AUC y lift para ranking; accuracy, precision, recall y F-score para clasificación; MSE para estimación de densidad.
- Cuidado con el feedback loop del ranking en producción: registra la posición mostrada y úsala como predictor.
- El A/B testing conecta la métrica optimizada por el modelo con el objetivo real del negocio (p. ej. ingresos).
