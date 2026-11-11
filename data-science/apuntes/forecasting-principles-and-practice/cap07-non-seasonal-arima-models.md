# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 7 — Non-seasonal ARIMA models (Modelos ARIMA no estacionales)

> Nota de extracción: texto obtenido de la capa de texto del PDF (material de taller con sesiones de laboratorio en R); las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo presenta la familia ARIMA para series no estacionales, una alternativa a los modelos ETS. La tesis es que combinando componentes autorregresivos (AR), diferenciación (I) y de medias móviles (MA) se puede describir una amplia variedad de series temporales y generar pronósticos fiables. Sales sabiendo qué representan los órdenes `(p, d, q)`, cómo se imponen las condiciones de estacionariedad e invertibilidad, cómo se seleccionan los modelos con criterios de información (AICc) y cómo opera el algoritmo automático `auto.arima()`.

El capítulo es muy práctico: alterna la teoría con sesiones de laboratorio en R (paquete `fpp`). Define primero los bloques AR y MA por separado, los une en ARMA/ARIMA con notación de retardo (backshift), y termina con el procedimiento de modelado paso a paso y el cálculo de pronósticos puntuales e intervalos.

## Modelos autorregresivos (AR)

Un modelo autorregresivo expresa el valor actual como combinación lineal de valores pasados de la propia serie:

```
yt = c + φ1·yt−1 + φ2·yt−2 + ··· + φp·yt−p + et
```

donde `et` es ruido blanco. Es una regresión múltiple con valores rezagados de `yt` como predictores.

Casos del AR(1) `yt = c + φ1·yt−1 + et`:
- Si `φ1 = 0`, `yt` equivale a ruido blanco (WN).
- Si `φ1 = 1` y `c = 0`, equivale a un random walk (RW).
- Si `φ1 = 1` y `c ≠ 0`, equivale a un random walk con deriva (drift).
- Si `φ1 < 0`, `yt` tiende a oscilar entre valores positivos y negativos.

Condiciones de estacionariedad: normalmente se restringen los modelos AR a datos estacionarios, lo que impone límites a los parámetros. La condición general es que las raíces complejas de `1 − φ1z − φ2z² − ··· − φpzᵖ` queden fuera del círculo unitario en el plano complejo. En casos sencillos:
- `p = 1`: `−1 < φ1 < 1`.
- `p = 2`: `−1 < φ2 < 1`, `φ2 + φ1 < 1`, `φ2 − φ1 < 1`.
- Para `p ≥ 3` las condiciones son más complejas, pero el software de estimación se encarga de ellas.

## Modelos de medias móviles (MA)

Un modelo MA usa errores pasados como predictores (no confundir con el suavizado por medias móviles):

```
yt = c + et + θ1·et−1 + θ2·et−2 + ··· + θq·et−q
```

Invertibilidad: todo proceso MA(q) puede escribirse como un AR(∞) si se imponen restricciones a los parámetros; entonces el modelo es "invertible". Los modelos invertibles tienen propiedades matemáticas que facilitan su uso práctico. La invertibilidad de un modelo ARIMA equivale a la pronosticabilidad de un modelo ETS. La condición general es que las raíces complejas de `1 + θ1z + ··· + θqzᵠ` queden fuera del círculo unitario:
- `q = 1`: `−1 < θ1 < 1`.
- `q = 2`: `−1 < θ2 < 1`, `θ2 + θ1 > −1`, `θ1 − θ2 < 1`.
- Para `q ≥ 3` el software gestiona las condiciones.

## Modelos ARIMA

Un modelo ARMA combina predictores AR y MA: `yt = c + φ1·yt−1 + ··· + θ1·et−1 + ··· + et`. Las condiciones sobre los coeficientes aseguran estacionariedad e invertibilidad. Un ARIMA combina ARMA con diferenciación: `(1−B)ᵈ·yt` sigue un modelo ARMA.

El modelo ARIMA(p, d, q):
- `p` = orden de la parte autorregresiva.
- `d` = grado de primeras diferencias.
- `q` = orden de la parte de medias móviles.

Casos especiales:
- Ruido blanco: ARIMA(0,0,0).
- Random walk: ARIMA(0,1,0) sin constante.
- Random walk con deriva: ARIMA(0,1,0) con constante.
- AR(p): ARIMA(p,0,0); MA(q): ARIMA(0,0,q).

Notación de retardo (backshift): el ARMA se escribe `(1 − φ1B − ··· − φpBᵖ)·yt = c + (1 + θ1B + ··· + θqBᵠ)·et`. Un ARIMA(1,1,1) es `(1−φ1B)(1−B)·yt = c + (1+θ1B)·et`, que combina un AR(1), una primera diferencia y un MA(1).

Ejemplo del consumo personal de EE. UU. (cambio porcentual trimestral): `auto.arima` ajusta un ARIMA(0,0,3) con media no nula, `yt = 0.756 + et + 0.254·et−1 + 0.226·et−2 + 0.269·et−3` (PDF p. 74).

Comportamiento de los pronósticos a largo plazo según `c` y `d`:
- `c = 0, d = 0`: tienden a cero. `c = 0, d = 1`: a una constante no nula. `c = 0, d = 2`: siguen una recta.
- `c ≠ 0, d = 0`: a la media de los datos. `c ≠ 0, d = 1`: siguen una recta. `c ≠ 0, d = 2`: tendencia cuadrática.
- Cuanto mayor es `d`, más rápido crecen los intervalos de pronóstico. Para comportamiento cíclico se requiere `p > 2` (o `p = 2` con `φ1² + 4φ2 < 0`).

## Autocorrelaciones parciales (PACF) y selección de órdenes

La autocorrelación parcial `αk` mide la relación entre `yt` e `yt−k` eliminando el efecto de los retardos intermedios (1, 2, …, k−1); equivale al coeficiente `bk` de la regresión `yt = c + φ1·yt−1 + ··· + φk·yt−k`. Cumple `α1 = ρ1` y usa los mismos valores críticos `±1.96/√T` que la ACF.

Interpretación de ACF/PACF sobre datos diferenciados:
- ARIMA(p,d,0): la ACF decae exponencialmente o es sinusoidal, y hay un pico significativo en el retardo `p` de la PACF, sin nada más allá.
- ARIMA(0,d,q): la PACF decae exponencialmente o es sinusoidal, y hay un pico significativo en el retardo `q` de la ACF, sin nada más allá.

## Estimación y criterios de información

Tras identificar el orden hay que estimar `c, φ1…φp, θ1…θq`. La estimación por máxima verosimilitud (MLE) es similar a minimizar `∑et²`; el comando `Arima()` permite CLS o MLE, y en ambos casos se usa optimización no lineal (distintos softwares dan estimaciones distintas).

Criterios de información (se eligen buenos modelos minimizándolos, con preferencia por el AICc):

```
AIC  = −2·log(L) + 2(p + q + k + 1)
AICc = AIC + 2(p + q + k + 1)(p + q + k + 2) / (T − p − q − k − 2)
BIC  = AIC + log(T)(p + q + k − 1)
```

donde `k = 1` si `c ≠ 0` y `k = 0` si `c = 0`.

## Modelado ARIMA en R

El algoritmo de `auto.arima()` (Hyndman y Khandakar, JSS 2008): selecciona `d` (y `D`) mediante tests de raíz unitaria, elige `p, q` minimizando el AICc y recorre el espacio de modelos con una búsqueda por pasos (stepwise). Parte de cuatro modelos iniciales (ARIMA(2,d,2), (0,d,0), (1,d,0), (0,d,1)), toma el de menor AIC, y en cada paso considera variaciones de `p, q` en ±1 e incluir/excluir `c`, hasta que no se encuentre un AIC menor.

Procedimiento de modelado completo:
1. Graficar los datos e identificar observaciones inusuales.
2. Si hace falta, transformar (Box-Cox) para estabilizar la varianza.
3. Diferenciar hasta lograr estacionariedad (tests de raíz unitaria si hay dudas).
4. Examinar ACF/PACF para decidir si conviene AR(p) o MA(q).
5. Probar modelos candidatos y buscar uno mejor con el AICc.
6. Revisar los residuos (ACF y test portmanteau de Ljung-Box); si no parecen ruido blanco, modificar el modelo.
7. Cuando los residuos parezcan ruido blanco, calcular los pronósticos.

El algoritmo automático solo cubre los pasos 3–5; el resto corre por cuenta del analista. Código esencial del laboratorio:

```r
fit <- Arima(internet, order=c(3,1,0))
fit2 <- auto.arima(internet)
Box.test(residuals(fit), fitdf=3, lag=10, type="Ljung")
forecast(fit)
```

Ejemplo del equipamiento eléctrico ajustado estacionalmente: tras diferenciar una vez, la PACF sugiere AR(3) (candidato ARIMA(3,1,0)); al comparar variaciones, ARIMA(3,1,1) tiene el menor AICc y sus residuos parecen ruido blanco (PDF p. 80-81).

## Pronósticos

Para obtener pronósticos puntuales:
1. Reordenar la ecuación ARIMA dejando `yt` a la izquierda.
2. Reemplazar `t` por `T + h`.
3. En la derecha, sustituir observaciones futuras por sus pronósticos, errores futuros por cero y errores pasados por los residuos correspondientes.

Se empieza con `h = 1` y se repite para `h = 2, 3, …` de forma recursiva (cada pronóstico alimenta al siguiente).

Intervalos de pronóstico (95 %): `ŷT+h|T ± 1.96·√vT+h|T`, con `vT+h|T` la varianza estimada. Para todo ARIMA, `vT+1|T = σ̂²`. En ARIMA(0,0,q), `vT+h|T = σ̂²·(1 + ∑θi²)`. Consideraciones:
- Los intervalos crecen con el horizonte y son difíciles de calcular a mano.
- Los cálculos asumen residuos no correlacionados y normalmente distribuidos.
- Los intervalos tienden a ser demasiado estrechos porque no incorporan la incertidumbre de los parámetros, suponen que los patrones históricos no cambian y que los errores futuros no están correlacionados.

## Lab Session 7

Cargar el paquete con `library(fpp)` antes de empezar. Para cada serie (`wmurders`, `usgdp`, `mcopper`) se repite el mismo flujo: (a) buscar una transformación Box-Cox si procede; (b) ajustar un ARIMA con `auto.arima()`; (c) probar otros órdenes plausibles; (d) elegir el mejor modelo y revisar los diagnósticos de residuos; (e) producir pronósticos y valorar si son razonables; (f) comparar con `ets()` sin transformación.

## Ideas clave

- ARIMA(p,d,q) combina componentes autorregresivos (`p`), diferenciación (`d`) y de medias móviles (`q`) para modelar series no estacionales.
- La estacionariedad (AR) y la invertibilidad (MA) imponen que las raíces de los polinomios queden fuera del círculo unitario; el software las garantiza.
- Casos límite útiles: ARIMA(0,0,0) es ruido blanco y ARIMA(0,1,0) es un random walk (con o sin deriva).
- La ACF y la PACF de los datos diferenciados orientan hacia modelos AR(p) o MA(q).
- La selección de órdenes se guía por criterios de información, con preferencia por el AICc.
- `auto.arima()` automatiza la elección de `d`, `p` y `q` mediante tests de raíz unitaria y búsqueda stepwise, pero no sustituye la revisión de datos, transformaciones ni diagnóstico de residuos.
- Los pronósticos puntuales se calculan recursivamente; los intervalos crecen con el horizonte y tienden a ser demasiado estrechos.
