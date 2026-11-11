# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 3 — Exponential smoothing (Suavizado exponencial)

> Nota de extracción: texto extraído de la capa de texto del PDF (material de taller con laboratorios en R); las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo presenta el suavizado exponencial como una familia de métodos de pronóstico que ponderan las observaciones pasadas con pesos que decaen geométricamente: lo más reciente pesa más. Se construye de lo simple a lo complejo, desde el suavizado exponencial simple (SES, sin tendencia ni estacionalidad) hasta los métodos de Holt (tendencia) y Holt-Winters (tendencia y estacionalidad), con variantes aditivas, multiplicativas y amortiguadas (damped).

La tesis central es que toda esta "confusa" colección de métodos puede organizarse en una taxonomía única y, sobre todo, dotarse de un fundamento estadístico mediante los modelos de espacio de estados con innovaciones (ETS). Cada método tiene una ecuación de observación y ecuaciones de transición para los estados (nivel, tendencia, estacionalidad), y admite dos versiones de error —aditivo y multiplicativo— que producen los mismos pronósticos puntuales pero distintos intervalos de pronóstico.

Sales sabiendo cómo formular SES, Holt y Holt-Winters en forma de componentes y de espacio de estados; cómo estimar los parámetros de suavizado y los estados iniciales por optimización numérica (MLE); cómo seleccionar automáticamente un modelo con criterios de información (AIC, AICc, BIC); y cómo usar la función `ets()` del paquete `fpp`/`forecast` en R para ajustar, diagnosticar y pronosticar.

## La perspectiva de espacio de estados

El marco distingue datos observados (y₁,…,y_T) de un estado no observado (x₁,…,x_T). El pronóstico es la esperanza condicional ŷ_{T+h|T} = E(y_{T+h}|x_T), la "varianza del pronóstico" es Var(y_{T+h}|x_T) y el intervalo de pronóstico es un rango de valores de y_{T+h} con alta probabilidad.

## Suavizado exponencial simple (SES)

En forma de componentes, el pronóstico es plano y el nivel se actualiza como media ponderada:

```
Pronóstico:  ŷ_{t+h|t} = ℓ_t
Suavizado:   ℓ_t = α y_t + (1−α) ℓ_{t−1}
```

Desarrollando la recursión, el pronóstico es una suma ponderada de todas las observaciones con pesos α(1−α)^{t−j} más un término del nivel inicial ℓ₀, con 0 ≤ α ≤ 1. Cuanto mayor es α, más peso recibe lo reciente (p. ej. con α=0.8, y_t pesa 0.8; con α=0.2, pesa 0.2 y el decaimiento es más lento). Casos límite: α→1 y α→0.

En forma de espacio de estados:

```
Observación: y_t = ℓ_{t−1} + e_t
Estado:      ℓ_t = ℓ_{t−1} + α e_t
```

donde e_t = y_t − ℓ_{t−1} = y_t − ŷ_{t|t−1} es el error de pronóstico a un paso dentro de la muestra. Hay que estimar α y ℓ₀. A diferencia de la regresión no existe solución cerrada: se eligen α y ℓ₀ minimizando el MSE = (1/T)Σe²_t mediante optimización numérica. Los pronósticos a varios pasos son constantes (función "plana") porque sin tendencia ni estacionalidad el pronóstico es una media constante.

```r
library(fpp)
fit <- ses(oil, h=3)
```

## Métodos con tendencia

Holt (1957) extendió SES para datos con tendencia añadiendo una segunda ecuación y un segundo parámetro β* (ambos entre 0 y 1):

```
Pronóstico: ŷ_{t+h|t} = ℓ_t + h b_t
Nivel:      ℓ_t = α y_t + (1−α)(ℓ_{t−1} + b_{t−1})
Tendencia:  b_t = β*(ℓ_t − ℓ_{t−1}) + (1−β*) b_{t−1}
```

Aquí ℓ_t estima el nivel y b_t la pendiente. En espacio de estados, con β = αβ* y e_t = y_t − (ℓ_{t−1}+b_{t−1}), hay que estimar α, β, ℓ₀, b₀. Holt casi siempre tendrá mejor RMSE dentro de muestra porque se optimiza con un parámetro más, pero eso no garantiza que sea mejor: la comparación útil es el RMSE fuera de muestra con un conjunto de prueba.

```r
fit2 <- holt(ausair, h=5)
accuracy(fit2)
```

El método de tendencia exponencial sustituye la tendencia aditiva por una relativa (b_t es la tasa de crecimiento), con ŷ_{t+h|t} = ℓ_t b_t^h, y se activa con `holt(x, exponential=TRUE)`.

Gardner y McKenzie (1985) propusieron amortiguar la tendencia (damped) para ser más conservadores en horizontes largos, con un parámetro 0 < φ < 1:

```
Pronóstico: ŷ_{t+h|t} = ℓ_t + (φ + φ² + ··· + φ^h) b_t
```

Si φ=1 coincide con Holt lineal; cuando h→∞, ŷ_{T+h|T} → ℓ_T + φb_T/(1−φ), de modo que los pronósticos de corto plazo tienen tendencia y los de largo plazo son constantes. Taylor (2003) introdujo además el amortiguamiento multiplicativo (φ=1 da el método exponencial).

```r
fit4 <- holt(air, h=5, damped=TRUE)
```

El ejemplo de ovejas en Asia (livestock, millones, 1970–2010) ilustra en una sola gráfica las alternativas: SES, Holt, exponencial, amortiguada aditiva y amortiguada multiplicativa.

## Métodos estacionales (Holt-Winters)

Holt y Winters añadieron una tercera ecuación de suavizado para la estacionalidad, con parámetros 0 ≤ α ≤ 1, 0 ≤ β* ≤ 1, 0 ≤ γ ≤ 1−α y m = periodo estacional. En la versión aditiva:

```
ŷ_{t+h|t} = ℓ_t + h b_t + s_{t−m+h⁺m}
ℓ_t = ℓ_{t−1} + b_{t−1} + α e_t
b_t = b_{t−1} + β e_t
s_t = s_{t−m} + γ e_t
```

con h⁺_m = ⌊(h−1) mod m⌋ + 1. Existe también la versión multiplicativa (la estacionalidad multiplica al nivel+tendencia) y la variante amortiguada, que a menudo es el método más preciso para datos estacionales. Se optimizan α, β*, γ y todos los estados iniciales ℓ₀, b₀, s₀, …, s_{1−m}.

```r
aus1 <- hw(austourists)
aus2 <- hw(austourists, seasonal="mult")
aus3 <- hw(austourists, seasonal="mult", damped=TRUE)
```

Ante tanta variedad de métodos, la pregunta práctica es cómo elegir entre ellos; el marco ETS da una respuesta automática. Fue desarrollado para pronosticar automáticamente ventas farmacéuticas de miles de productos.

## Taxonomía y modelos ETS

Los métodos se organizan por componente de tendencia (N, A, Ad, M, Md) y componente estacional (N, A, M), dando 15 métodos de suavizado exponencial distintos. Los modelos de espacio de estados con innovaciones generan los mismos pronósticos puntuales que los métodos, pero además producen intervalos de pronóstico y permiten una selección "propia" de modelo, al ser procesos generadores de datos estocásticos que describen toda la distribución de pronóstico.

Cada modelo se denota ETS(Error, Trend, Seasonal):

- Error = {A, M}
- Trend = {N, A, Ad, M, Md}
- Seasonal = {N, A, M}

Como cada método tiene una versión con error aditivo y otra con error multiplicativo, hay 30 modelos en total. Ambas versiones dan los mismos pronósticos puntuales pero distintos intervalos. Ejemplos de formulación:

```
ETS(A,N,N):  y_t = ℓ_{t−1} + ε_t;  ℓ_t = ℓ_{t−1} + α ε_t
ETS(M,N,N):  y_t = ℓ_{t−1}(1+ε_t); ℓ_t = ℓ_{t−1}(1+α ε_t)
ETS(A,A,A):  y_t = ℓ_{t−1} + b_{t−1} + s_{t−m} + ε_t
```

En ETS(A,N,N) el error e_t coincide con la innovación ε_t ~ NID(0,σ²); se llama modelo de "innovaciones" o de "fuente única de error" porque el mismo proceso ε_t alimenta observación y estados. En los modelos multiplicativos ε_t es un error relativo (y_t − μ_t)/μ_t.

Forma general de espacio de estados con x_t = (ℓ_t, b_t, s_t, …, s_{t−m+1}):

```
y_t = h(x_{t−1}) + k(x_{t−1}) ε_t   [μ_t y e_t]
x_t = f(x_{t−1}) + g(x_{t−1}) ε_t
```

Error aditivo: k(x)=1, y_t = μ_t + ε_t. Error multiplicativo: k(x_{t−1})=μ_t, y_t = μ_t(1+ε_t). La única diferencia entre ambos está en la ecuación de observación.

Algunas combinaciones causan dificultades numéricas (las que dividen por un estado), p. ej. ETS(M,M,A), ETS(A,N,M), ETS(A,A,M), ETS(A,M,M), etc. Los modelos con error multiplicativo sirven para datos estrictamente positivos, pero son inestables con ceros o negativos; en ese caso solo se aplican los seis modelos totalmente aditivos.

## Estimación y selección de modelo

Los parámetros θ = (α, β, γ, φ) y los estados iniciales x₀ se estiman minimizando la función de verosimilitud L* (equivalente a −2 log(verosimilitud) + constante). Restricciones de parámetros:

- Región usual (interpretación de medias ponderadas): 0 < α < 1, 0 < β < α, 0 < γ < 1−α; y 0.8 < φ < 0.98 para evitar problemas numéricos.
- Región admisible: evita que el pasado lejano siga influyendo; suele ser menos restrictiva (p. ej. ETS(A,N,N) admite 0 < α < 2).

La selección usa criterios de información: AIC = −2 log(Likelihood) + 2p (p = número de parámetros), su corrección AICc para muestras pequeñas, y BIC. Minimizar el AIC da el mejor modelo para predicción. El AIC solo tiene sentido comparado con otro modelo sobre los mismos datos; diferencias de 2 o menos no son sustanciales y puede preferirse el modelo más simple. El AIC puede ser negativo.

El pronóstico automático (Hyndman et al., IJF 2002) ajusta cada modelo apropiado por MLE, elige el mejor por AICc y produce pronósticos e intervalos a partir del modelo de espacio de estados. El método funcionó muy bien en la competencia M3.

## ETS y pronóstico en R

La función `ets()` elige automáticamente un modelo por AIC/AICc/BIC, maneja cualquier combinación de tendencia, estacionalidad y amortiguamiento, asegura parámetros admisibles (equivalentes a invertibles) y produce intervalos de pronóstico para todo modelo, devolviendo un objeto de clase `"ets"` con métodos como `plot()`, `summary()`, `residuals()`, `fitted()`, `simulate()` y `forecast()`.

```r
fit  <- ets(ausbeer)                         # selección automática
fit2 <- ets(ausbeer, model="AAA", damped=FALSE)
fcast1 <- forecast(fit, h=20)
```

En la notación `model="ZZZ"`, cada letra es "N", "A", "M" o "Z" (selección automática); el default `ZZZ` elige todos los componentes por criterio de información. `damped=NULL` deja que el criterio decida entre tendencia amortiguada o no. Con `alpha/beta/gamma/phi=NULL` los parámetros se estiman. `additive.only=TRUE` restringe a componentes aditivos; `lambda` aplica transformación Box-Cox (y fuerza `additive.only`). Otros argumentos: `opt.crit` (por defecto `lik`), `bounds` (`usual`, `admissible` o `both`), `ic` (`aic` por defecto) y `restrict=TRUE` para descartar modelos con problemas numéricos.

Sobre `ausbeer`, la selección automática eligió ETS(M,Md,M) (α=0.1776, β=0.0454, γ=0.1947, φ=0.9549) frente al ETS(A,A,A) forzado; `plot(fit)` descompone la serie en nivel, pendiente y estacionalidad. La bondad de ajuste se evalúa con `accuracy()` (ME, RMSE, MAE, MPE, MAPE, MASE). La función también permite reajustar un modelo ya estimado a datos nuevos (`ets(serie, model=ajuste_previo)`) para evaluar fuera de muestra.

Pronóstico con ETS: los pronósticos puntuales se obtienen iterando las ecuaciones para t = T+1,…,T+h fijando ε_t = 0 para t > T. No equivalen a E(y_{t+h}|x_t) salvo cuando tendencia y estacionalidad son ambas aditivas. ETS(A,x,y) y ETS(M,x,y) dan pronósticos puntuales idénticos si comparten parámetros (p. ej. ETS(A,A,N) coincide con Holt lineal), pero los intervalos difieren. Existen fórmulas exactas de intervalos para muchos modelos; en el resto se simulan trayectorias futuras condicionadas al último estado y se toman los percentiles, todo disponible vía `forecast()` del paquete `forecast`.

## Ideas clave

- El suavizado exponencial pondera el pasado con pesos que decaen geométricamente; α controla la velocidad de decaimiento.
- SES da pronósticos planos; Holt añade tendencia; Holt-Winters añade estacionalidad; existen variantes aditivas, multiplicativas y amortiguadas (damped).
- La tendencia amortiguada (0 < φ < 1) hace que el corto plazo tenga tendencia y el largo plazo sea constante, más conservador.
- Los 15 métodos se clasifican por (Trend, Seasonal) y se formalizan como modelos de espacio de estados ETS(Error, Trend, Seasonal), con 30 modelos al distinguir error aditivo y multiplicativo.
- Error aditivo y multiplicativo dan iguales pronósticos puntuales pero distintos intervalos de pronóstico; la única diferencia está en la ecuación de observación.
- Los parámetros y estados iniciales se estiman por MLE (minimizando L*); la elección de modelo usa AIC, AICc o BIC.
- Los modelos con error multiplicativo exigen datos estrictamente positivos; con ceros o negativos solo valen los seis modelos totalmente aditivos.
- En R, `ets()` selecciona y ajusta el modelo automáticamente y `forecast()` genera pronósticos e intervalos (exactos o por simulación).
