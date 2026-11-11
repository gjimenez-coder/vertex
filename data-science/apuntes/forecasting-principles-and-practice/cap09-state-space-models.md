# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 9 — State space models (Modelos de espacio de estados)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con sesiones de laboratorio en R) y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo presenta los modelos de espacio de estados: una forma general de escribir modelos de series temporales mediante una ecuación de observación (lo que medimos) y una ecuación de estado (variables latentes que evolucionan en el tiempo). Partiendo de los modelos estructurales simples, llega a la formulación lineal gaussiana genérica y al filtro de Kalman, el algoritmo que calcula predicciones, verosimilitud y estados filtrados para cualquier modelo escrito en ese formato.

La tesis central es que el formato de espacio de estados unifica una gran variedad de modelos (estructurales, ARIMA, regresiones con parámetros variables) bajo un mismo conjunto de recursiones. Una vez que un modelo está en ese formato, el filtro de Kalman da predicciones óptimas en MSE, maneja datos faltantes con facilidad y permite calcular la verosimilitud para estimar parámetros.

Sales sabiendo escribir los modelos de nivel local, tendencia lineal local, estructural básico (BSM) y trigonométrico; relacionarlos con sus equivalentes aditivos ETS; traducir modelos ARIMA al espacio de estados; aplicar el filtro de Kalman, el suavizado (smoothing) y modelos con parámetros variables en el tiempo, con el código esencial de R (`StructTS`, `tsSmooth`).

## Modelos estructurales simples

Son análogos a los modelos ETS aditivos, con dos diferencias: `yt` depende del estado `xt`, y un proceso de error distinto afecta a `xt|xt−1` y a `yt|xt`.

Modelo de nivel local (local level):

```
yt = 𝓁t + εt
𝓁t = 𝓁t−1 + ξt
```

`εt` y `ξt` son ruidos blancos gaussianos independientes. Equivale a ETS(A,N,N) donde `ξt = αεt−1`. Se estiman `σ²ε` y `σ²ξ`. Si `σ²ξ = 0`, entonces `yt ∼ NID(𝓁0, σ²ε)`.

Modelo de tendencia lineal local (local linear trend):

```
yt = 𝓁t + εt
𝓁t = 𝓁t−1 + bt−1 + ξt
bt = bt−1 + ζt
```

Compárese con ETS(A,A,N) donde `ξt = (α+β)εt−1` y `ζt = βεt−1`. Se estiman `σ²ε`, `σ²ξ` y `σ²ζ`. Si `σ²ζ = σ²ξ = 0`, el modelo se reduce a `yt = 𝓁0 + t·b0 + εt`, es decir, una regresión lineal con coeficientes variables en el tiempo.

Modelo estructural básico (BSM): añade estacionalidad con `s1,t = −Σ sj,t−1 + ηt`. Equivale a ETS(A,A,A); se estiman `σ²ε, σ²ξ, σ²ζ, σ²η`. Si `σ²η = 0` la estacionalidad es determinista.

Modelos trigonométricos: representan la estacionalidad mediante pares de componentes `sj,t`, `s*j,t` con frecuencias `λj = 2πj/m`. Son equivalentes al BSM cuando `σ²ω,j = σ²ω` y `J = m/2`; se elige `J < m/2` para usar menos grados de libertad.

ETS frente a modelos estructurales: los ETS son más generales porque admiten componentes no lineales (multiplicativos) y permiten pronóstico automático por su mayor espacio de modelos. Los ETS aditivos son casi equivalentes a los modelos estructurales correspondientes. Los estructurales tienen parámetros siempre no negativos (varianzas), son más fáciles de generalizar (p. ej. añadir covariables) y manejan mejor los valores faltantes.

En R, con `StructTS`:

```r
fit <- StructTS(austourists, type = "BSM")
decomp <- cbind(austourists, fitted(fit))
colnames(decomp) <- c("data","level","slope","seasonal")
plot(decomp)
```

Los tipos disponibles son `"level"`, `"trend"` y `"BSM"`.

## Modelos lineales gaussianos de espacio de estados

Forma general:

```
Ecuación de observación:  yt = f′·xt + εt
Ecuación de estado:       xt = G·xt−1 + wt
```

con `xt` vector de estado de longitud `p`, `G` matriz `p×p`, `f` vector de longitud `p`, `εt ∼ NID(0, σ²)` y `wt ∼ NID(0, W)`.

Casos particulares: el nivel local es `f = G = 1`, `xt = 𝓁t`. La tendencia lineal local usa `f′ = [1 0]`, `G = [[1,1],[0,1]]` y `W` diagonal con `σ²ξ, σ²ζ`. El BSM añade al vector de estado los componentes estacionales, con `f′ = [1 0 1 0 ... 0]` y `W = diag(σ²ξ, σ²ζ, σ²η, 0, ..., 0)`.

## Filtro de Kalman

Notación: `x̂t|t` y `P̂t|t` son la media y varianza del estado dado `y1,...,yt`; `x̂t|t−1`, `P̂t|t−1` lo mismo condicionando hasta `t−1`. Las recursiones, iteradas para `t = 1,...,T` partiendo de un `x1|0` y `P1|0` conocidos, son tres pasos:

```
Pronóstico:       ŷt|t−1 = f′·x̂t|t−1
                  v̂t|t−1 = f′·P̂t|t−1·f + σ²
Filtrado estado:  x̂t|t = x̂t|t−1 + P̂t|t−1·f·v̂⁻¹t|t−1·(yt − ŷt|t−1)
                  P̂t|t = P̂t|t−1 − P̂t|t−1·f·v̂⁻¹t|t−1·f′·P̂t|t−1
Predicción estado: x̂t+1|t = G·x̂t|t ;  P̂t+1|t = G·P̂t|t·G′ + W
```

Son solo esperanzas condicionales, así que dan estimaciones de MSE mínimo. Para inicializar se necesitan `x1|0` y `P1|0`; un enfoque común en modelos estructurales es fijar `x1|0 = 0` y `P1|0 = kI` con `k` muy grande. El enfoque ETS estimaba `x1|0` y evitaba `P1|0` asumiendo procesos de error idénticos; usar un `x1|0` aleatorio da intervalos de pronóstico más realistas.

Valores faltantes: se aplican solo los pasos de predicción (se saltan los de filtrado) cuando falta `yt`. El pronóstico a varios pasos trata los valores futuros como faltantes, iterando para `t = T+1,...,T+h` desde `xT|T`, `PT|T`.

Lo especial del filtro de Kalman: ecuaciones muy generales para cualquier modelo en formato de espacio de estados, pronósticos óptimos en MSE, manejo fácil de faltantes y cálculo sencillo de la verosimilitud.

Verosimilitud: con `θ` todos los parámetros desconocidos y `et = yt − ŷt|t−1`,

```
logL = −(T/2)·log(2π) − ½·Σ log v̂t|t−1 − ½·Σ e²t / v̂t|t−1
```

Todos los términos salen de las ecuaciones del filtro de Kalman.

## Modelos ARIMA en espacio de estados

Cualquier ARIMA puede escribirse en formato de espacio de estados y entonces el filtro de Kalman calcula verosimilitud y pronósticos. Para un AR(2), `yt = φ1·yt−1 + φ2·yt−2 + et`, se toma `xt = [yt, yt−1]′`, `wt = [et, 0]′`, con `yt = [1 0]·xt` y `G = [[φ1, φ2],[1, 0]]`. Existen formulaciones alternativas equivalentes. Se generaliza a AR(p), ARMA(1,1) y ARMA(p,q) con `r = max(p, q+1)`. La función `arima` de R se implementa con esta formulación.

## Suavizado de Kalman (Kalman smoothing)

Busca `x̂t|T` para `t < T`, es decir, estimar el estado usando todos los datos y no solo los anteriores:

```
x̂t|T = x̂t|t + At·(x̂t+1|T − x̂t+1|t)
P̂t|T = P̂t|t + At·(P̂t+1|T − P̂t+1|t)·A′t,   con At = P̂t|t·G′·(P̂t+1|t)⁻¹
```

Es útil para estimar valores faltantes (`ŷt|T = f′·x̂t|T`) y para el ajuste estacional cuando uno de los estados es la componente estacional. En R:

```r
fit <- StructTS(austourists, type = "BSM")
sm <- tsSmooth(fit)
aus.sa <- austourists - sm[,3]   # datos desestacionalizados
```

Con valores faltantes, se puede recuperar la estimación como `sm[,1] + sm[,3]`.

## Modelos de parámetros variables en el tiempo

El modelo lineal gaussiano admite matrices y varianzas dependientes de `t`: `yt = f′t·xt + εt`, `xt = Gt·xt−1 + wt`, con las mismas recursiones de Kalman pero con `ft`, `Gt`, `Wt`, `σ²t`. Casos:

- Nivel local con covariable: incorpora `β·zt` con `f′t = [1 zt]`, `xt = [𝓁t, β]′`, `Wt = diag(σ²ξ, 0)`. Supone `zt` fijo y conocido; `β` se estima con `x̂T|T`. Equivale a regresión lineal simple con intercepto variable.
- Regresión con parámetros variables: `βt` sigue un paseo aleatorio (`βt = βt−1 + ζt`), permitiendo coeficientes que cambian lentamente; estimados con `x̂t|t` o `x̂t|T`.
- Regresión con actualización recursiva: fijando `Wt = 0`, los parámetros se actualizan al llegar nuevos datos; los residuos recursivos son `yt − ŷt|t−1`.

## Sesión de laboratorio 9

Tras cargar `library(fpp)`, los ejercicios proponen: (1) usar `StructTS` para pronosticar las series de la sesión 4 y comparar pronósticos puntuales e intervalos, revisando que los residuos parezcan ruido blanco; (2) programar un filtro de Kalman propio para actualizar coeficientes de regresión del consumo personal (`y`) frente a la renta disponible (`z`) con el modelo `yt = at + bt·zt + εt`, `Wt = 0`, comprobando que `x̂T|T` coincide con los estimadores OLS de `lm` y graficando la evolución de los parámetros.

## Ideas clave

- El formato de espacio de estados separa observación y estado latente, y unifica modelos estructurales, ARIMA y regresiones con parámetros variables.
- Los modelos estructurales (nivel local, tendencia lineal local, BSM, trigonométrico) son casi equivalentes a los ETS aditivos, pero con parámetros no negativos y más fáciles de generalizar.
- El filtro de Kalman da, en tres pasos (pronóstico, filtrado, predicción), estimaciones óptimas en MSE para cualquier modelo en este formato.
- Maneja valores faltantes saltando el paso de filtrado, y el pronóstico multistep trata el futuro como faltante.
- La verosimilitud se obtiene directamente de las cantidades del filtro de Kalman, lo que permite estimar parámetros.
- Cualquier ARIMA se escribe en espacio de estados; la función `arima` de R lo usa internamente.
- El suavizado (`tsSmooth`) usa todos los datos para estimar estados pasados, útil en imputación y ajuste estacional.
- Con `ft`, `Gt`, `Wt` dependientes del tiempo se obtienen regresiones con parámetros fijos (OLS), variables (paseo aleatorio) o actualizados recursivamente.
