# Logistic Regression (Regresión logística) — Estudio

## Tarjetas de repaso

P: ¿Qué cinco decisiones exige plantear un problema de clasificación?
R: Qué clasificador usar, qué método de optimización, qué función de pérdida minimizar, qué features extraer y qué métrica de evaluación.

P: ¿Por qué elegir un clasificador no es solo cuestión de precisión?
R: Porque hay que navegar restricciones reales: runtime, tu propia comprensión del algoritmo, interpretabilidad y escalabilidad.

P: ¿Por qué la regresión logística es una buena elección para clasificación binaria a gran escala?
R: Porque es rápida, escalable y devuelve probabilidades directamente interpretables.

P: ¿Qué es la función inverse-logit y qué rango acota?
R: `P(t) = 1 / (1 + e⁻ᵗ)`; acota la salida en [0,1], por lo que se interpreta como probabilidad.

P: ¿Cómo expresa el modelo el logit de la probabilidad de clic?
R: Como función lineal de las features: `logit(P(cᵢ=1 | xᵢ)) = α + βᵀxᵢ`.

P: ¿Qué representan α y β en el modelo logístico?
R: α es la base rate (probabilidad incondicional de clic, el click-through rate, del orden del 1%); β es la pendiente, tan largo como el número de features, e indica cuánto cada feature sube o baja la probabilidad.

P: ¿Cómo se estiman α y β?
R: Por máxima verosimilitud (MLE) mediante optimización convexa, minimizando la log-verosimilitud negativa; no hay solución cerrada como en la regresión lineal.

P: ¿En qué se diferencian el método de Newton y el Stochastic Gradient Descent?
R: Newton usa gradiente y matriz Hessiana (`Θₙ₊₁ = Θₙ − γ H⁻¹ ∇Θ`) y sufre al invertir la Hessiana con muchas features; SGD aproxima el gradiente con una observación a la vez, no invierte matrices y escala mejor con datos enormes y dispersos.

P: ¿Qué métricas se usan para evaluar la regresión logística como modelo de ranking?
R: AUC (área bajo la curva ROC) y el área bajo la curva de lift acumulado.

P: ¿Qué métricas se usan para evaluarla como modelo de clasificación?
R: Lift, accuracy, precision, recall y F-score (media armónica de precision y recall: `(2 × P × R)/(P + R)`).

P: ¿Cómo se definen precision y recall?
R: Precision = verdaderos positivos / (verdaderos positivos + falsos positivos); recall = verdaderos positivos / (verdaderos positivos + falsos negativos).

P: ¿Qué métricas aplican a la estimación de densidad y por qué?
R: Mean squared error, root squared error y mean absolute error; se usan cuando se necesita la probabilidad real, no un score relativo.

P: ¿Qué es el feedback loop del ranking y cómo se mitiga?
R: El riesgo de confundir el efecto de la posición mostrada con el del producto; se mitiga registrando siempre la posición/rank y usándola como predictor para estimar un normalizador de posición.

P: ¿Para qué sirve el A/B testing en este contexto?
R: Para conectar la métrica que optimiza el modelo (accuracy, MSE) con el objetivo real del negocio (p. ej. ingresos), desviando grupos de usuarios a distintas versiones del algoritmo.

## Preguntas de autoevaluación

P: ¿Por qué no se usa la regresión lineal para predecir el clic en el caso M6D?
R: Porque la lineal intentaría predecir el valor real (0 o 1) y daría predicciones por debajo de 0 y por encima de 1, no interpretables como probabilidades; la logística emite una probabilidad acotada en [0,1]. (Sección: Caso M6D / La matemática subyacente)

P: ¿Por qué el runtime es una restricción crítica para M6D y cómo se comportan k-NN y los modelos lineales?
R: Porque actualizan unos 500 modelos al día y los modelos deciden pujas, así que importa el tiempo de entrenar y de decidir; k-NN es lento (necesita todos los datos en memoria y buscar los k vecinos), mientras los modelos lineales solo guardan el vector de coeficientes y hacen un producto escalar. (Sección: Clasificadores)

P: ¿Por qué una compañía de tarjetas de crédito preferiría un árbol de decisión a un random forest?
R: Porque por ley deben explicar sus denegaciones y los árboles son fáciles de interpretar, mientras que los random forests no lo son aunque sean casi lo mismo. (Sección: Clasificadores)

P: ¿Cómo convierte M6D los datos de navegación en un problema de clasificación?
R: Hashean las URLs visitadas a cadenas aleatorias, forman una matriz dispersa (filas = usuarios, columnas = sitios) y añaden una columna de etiquetas: 1 si hizo clic en el anuncio, 0 si no; esto lo reduce al problema ya resuelto de la clasificación de spam. (Sección: Caso M6D: modelos de clics)

P: ¿Por qué se puede escribir la verosimilitud como producto de densidades?
R: Porque se asume independencia entre usuarios (el clic de uno no afecta al de otro); como maximizar la verosimilitud equivale a maximizar su logaritmo, se minimiza la log-verosimilitud negativa. (Sección: Estimación de α y β)

P: ¿Por qué un buen modelo de ranking puede ser un mal estimador de probabilidad y cuándo importa?
R: Un modelo puede ordenar bien (p. ej. .7, .5, .3) pero estar lejos de lo real (.03, .02, .01); importa en publicidad, donde se busca `P(conversión|X)·$q > $c`, lo que exige un MSE pequeño. (Sección: Evaluación)

P: Según los dos experimentos mentales de Brian, ¿en qué sentido la ciencia de datos es "ciencia"?
R: En que cada decisión de diseño se formula como hipótesis que se valida o refuta con experimentación rigurosa: conservar el mejor modelo actual, enfrentarlo a un nuevo modelo y repetir sin overfitting. (Sección: Los dos experimentos mentales)

## Checklist

- Definir las cinco decisiones del problema: clasificador, optimización, función de pérdida, features y métrica.
- Evaluar las restricciones del problema: runtime, tu comprensión del algoritmo, interpretabilidad y escalabilidad.
- Comprobar que entiendes el algoritmo elegido para evitar hacer overfitting sin darte cuenta.
- Representar los datos como matriz dispersa (usuarios × sitios) y añadir la columna de etiqueta 0/1 para clasificación.
- Ajustar el modelo en R con `glm(click ~ ..., data = train, family = binomial(logit))`.
- Decidir si usar la probabilidad directa o aplicar un umbral (p. ej. 0.75) para mostrar el anuncio.
- Elegir la métrica según el uso: AUC/lift para ranking, accuracy/precision/recall/F-score para clasificación, MSE para estimación de densidad.
- Registrar la posición/rank mostrado y usarla como predictor para controlar el feedback loop.
- Validar la elección del modelo con A/B testing contra la métrica de negocio que de verdad importa.
