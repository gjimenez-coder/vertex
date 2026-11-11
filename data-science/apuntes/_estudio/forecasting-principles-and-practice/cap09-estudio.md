# State space models (Modelos de espacio de estados) — Estudio

## Tarjetas de repaso

P: ¿Qué dos ecuaciones componen un modelo de espacio de estados? / R: La ecuación de observación (lo que medimos, `yt`) y la ecuación de estado (variables latentes `xt` que evolucionan en el tiempo).

P: ¿Cómo se escribe el modelo de nivel local (local level)? / R: `yt = 𝓁t + εt` y `𝓁t = 𝓁t−1 + ξt`, con `εt` y `ξt` ruidos blancos gaussianos independientes.

P: ¿A qué modelo ETS equivale el nivel local y bajo qué relación? / R: A ETS(A,N,N), donde `ξt = αεt−1`.

P: ¿Qué ocurre en el nivel local si `σ²ξ = 0`? / R: Que `yt ∼ NID(𝓁0, σ²ε)`.

P: ¿Qué añade el modelo de tendencia lineal local respecto al nivel local? / R: Una pendiente: `𝓁t = 𝓁t−1 + bt−1 + ξt` y `bt = bt−1 + ζt`; equivale a ETS(A,A,N).

P: ¿Qué es el modelo estructural básico (BSM) y a qué ETS equivale? / R: Un modelo que añade estacionalidad con `s1,t = −Σ sj,t−1 + ηt`; equivale a ETS(A,A,A), estimando `σ²ε, σ²ξ, σ²ζ, σ²η`.

P: ¿Por qué los ETS se consideran más generales que los modelos estructurales? / R: Porque admiten componentes no lineales (multiplicativos) y permiten pronóstico automático por su mayor espacio de modelos.

P: ¿Qué ventajas tienen los modelos estructurales frente a los ETS? / R: Parámetros siempre no negativos (varianzas), más fáciles de generalizar (p. ej. añadir covariables) y mejor manejo de valores faltantes.

P: ¿Cuál es la forma general del modelo lineal gaussiano de espacio de estados? / R: Observación `yt = f′·xt + εt` y estado `xt = G·xt−1 + wt`, con `εt ∼ NID(0, σ²)` y `wt ∼ NID(0, W)`.

P: ¿Cuáles son los tres pasos del filtro de Kalman? / R: Pronóstico (`ŷt|t−1`, `v̂t|t−1`), filtrado del estado (`x̂t|t`, `P̂t|t`) y predicción del estado (`x̂t+1|t`, `P̂t+1|t`).

P: ¿Por qué las estimaciones del filtro de Kalman son óptimas en MSE? / R: Porque son esperanzas condicionales, lo que da estimaciones de MSE mínimo.

P: ¿Cómo maneja el filtro de Kalman los valores faltantes? / R: Aplica solo los pasos de predicción y salta los de filtrado cuando falta `yt`.

P: ¿Para qué sirve el suavizado de Kalman (Kalman smoothing)? / R: Para estimar `x̂t|T` usando todos los datos (no solo los anteriores); útil en imputación de faltantes y ajuste estacional.

P: ¿Cómo se escribe un AR(2) en espacio de estados? / R: Con `xt = [yt, yt−1]′`, `wt = [et, 0]′`, `yt = [1 0]·xt` y `G = [[φ1, φ2],[1, 0]]`.

P: ¿Qué se obtiene al hacer `ft`, `Gt`, `Wt` dependientes del tiempo? / R: Regresiones con parámetros fijos (OLS), variables (paseo aleatorio) o actualizados recursivamente.

## Preguntas de autoevaluación

P: ¿En qué se diferencian los modelos estructurales simples de los modelos ETS aditivos? / R: En que `yt` depende del estado `xt` y en que un proceso de error distinto afecta a `xt|xt−1` y a `yt|xt`. (Sección "Modelos estructurales simples")

P: Si en la tendencia lineal local se cumple `σ²ζ = σ²ξ = 0`, ¿a qué se reduce el modelo? / R: A `yt = 𝓁0 + t·b0 + εt`, es decir, una regresión lineal con coeficientes variables en el tiempo. (Sección "Modelos estructurales simples")

P: ¿Cómo se obtiene la verosimilitud de un modelo en espacio de estados? / R: Directamente de las cantidades del filtro de Kalman: `logL = −(T/2)·log(2π) − ½·Σ log v̂t|t−1 − ½·Σ e²t / v̂t|t−1`, con `et = yt − ŷt|t−1`. (Sección "Filtro de Kalman")

P: ¿Cómo se realiza el pronóstico a varios pasos con el filtro de Kalman? / R: Tratando los valores futuros como faltantes e iterando para `t = T+1,...,T+h` desde `xT|T`, `PT|T`. (Sección "Filtro de Kalman")

P: ¿Por qué es útil escribir un modelo ARIMA en formato de espacio de estados? / R: Porque entonces el filtro de Kalman calcula su verosimilitud y sus pronósticos; la función `arima` de R se implementa así. (Sección "Modelos ARIMA en espacio de estados")

P: ¿Qué diferencia hay entre una regresión con parámetros variables y una con actualización recursiva? / R: En la variable, `βt` sigue un paseo aleatorio (`βt = βt−1 + ζt`); en la recursiva se fija `Wt = 0` y los parámetros se actualizan al llegar nuevos datos. (Sección "Modelos de parámetros variables en el tiempo")

P: ¿Cómo se inicializa el filtro de Kalman en modelos estructurales y qué ventaja aporta un `x1|0` aleatorio? / R: Un enfoque común fija `x1|0 = 0` y `P1|0 = kI` con `k` muy grande; usar un `x1|0` aleatorio da intervalos de pronóstico más realistas. (Sección "Filtro de Kalman")

## Puntos a dominar

- Escribir los modelos de nivel local, tendencia lineal local, BSM y trigonométrico, y relacionarlos con sus equivalentes aditivos ETS.
- Reconocer la forma general del modelo lineal gaussiano: ecuación de observación `yt = f′·xt + εt` y ecuación de estado `xt = G·xt−1 + wt`.
- Identificar los casos particulares de `f`, `G` y `W` para el nivel local, la tendencia lineal local y el BSM.
- Aplicar las tres recursiones del filtro de Kalman (pronóstico, filtrado, predicción) e interpretarlas como esperanzas condicionales con MSE mínimo.
- Explicar el manejo de valores faltantes (saltar el paso de filtrado) y el pronóstico multistep (tratar el futuro como faltante).
- Derivar la verosimilitud a partir de las cantidades del filtro de Kalman para estimar parámetros.
- Traducir modelos ARIMA (AR(2), AR(p), ARMA(1,1), ARMA(p,q) con `r = max(p, q+1)`) al espacio de estados.
- Distinguir filtrado (`x̂t|t`) de suavizado (`x̂t|T`) y usar `StructTS` y `tsSmooth` en R para descomponer y desestacionalizar.
- Diferenciar las variantes de parámetros variables en el tiempo: covariable con intercepto variable, paseo aleatorio y actualización recursiva.
