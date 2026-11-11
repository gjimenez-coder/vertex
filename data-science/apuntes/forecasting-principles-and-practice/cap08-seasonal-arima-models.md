# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 8 — Seasonal ARIMA models (Modelos ARIMA estacionales)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con sesiones de laboratorio en R, del que se conserva solo el código esencial); las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo extiende los modelos ARIMA no estacionales para capturar patrones estacionales. La notación completa es ARIMA(p,d,q)(P,D,Q)ₘ, donde la primera terna es la parte no estacional, la segunda la parte estacional y m el número de periodos por estación (p. ej. 4 trimestral, 12 mensual). Los términos estacionales operan sobre rezagos múltiplos de m usando el operador de retardo elevado a potencias de m.

La tesis central es que el modelo estacional se construye multiplicando los factores AR, de diferenciación y MA de ambas partes, lo que genera un polinomio con rezagos en 1, 4, 5, 6, etc. (para m=4). La identificación se apoya en la ACF y la PACF: los términos estacionales se manifiestan en los rezagos estacionales (m, 2m, 3m…).

Sales sabiendo elegir órdenes de diferenciación (d y D), leer rezagos estacionales en ACF/PACF, comparar modelos candidatos con AICc y RMSE sobre conjunto de prueba, y validar residuos con la prueba de Ljung-Box. El capítulo también aclara la relación entre ARIMA y el suavizado exponencial (ETS).

## El modelo estacional y su notación
La forma general multiplica los factores de ambas partes. Para un ARIMA(1,1,1)(1,1,1)₄ sin constante (PDF p. 84):

```
(1−φ₁B)(1−Φ₁B⁴)(1−B)(1−B⁴)yₜ = (1+θ₁B)(1+Θ₁B⁴)eₜ
```

donde cada factor representa, en orden: AR(1) no estacional, AR(1) estacional, diferencia no estacional, diferencia estacional, MA(1) no estacional y MA(1) estacional. Al multiplicar los factores, el modelo se escribe con rezagos no solo contiguos sino también alrededor de los múltiplos de m: aparecen términos en yₜ₋₁, yₜ₋₂, yₜ₋₄, yₜ₋₅, yₜ₋₆, yₜ₋₈, yₜ₋₉, yₜ₋₁₀ y en los errores eₜ₋₁, eₜ₋₄, eₜ₋₅ (PDF p. 84).

## 8.1 Modelos ARIMA comunes
La Oficina del Censo de EE. UU. emplea con más frecuencia estos modelos (PDF p. 85):

- ARIMA(0,1,1)(0,1,1)ₘ con transformación logarítmica
- ARIMA(0,1,2)(0,1,1)ₘ con transformación logarítmica
- ARIMA(2,1,0)(0,1,1)ₘ con transformación logarítmica
- ARIMA(0,2,2)(0,1,1)ₘ con transformación logarítmica
- ARIMA(2,1,2)(0,1,1)ₘ sin transformación

## 8.2 ACF y PACF de modelos ARIMA estacionales
La parte estacional de un modelo AR o MA se ve en los rezagos estacionales de la PACF y la ACF (PDF p. 85):

- ARIMA(0,0,0)(0,0,1)₁₂ muestra un pico en el rezago 12 de la ACF (sin otros picos significativos) y decaimiento exponencial en los rezagos estacionales de la PACF (12, 24, 36…).
- ARIMA(0,0,0)(1,0,0)₁₂ muestra decaimiento exponencial en los rezagos estacionales de la ACF y un único pico significativo en el rezago 12 de la PACF.

Es el reflejo estacional de la regla no estacional: un término MA estacional deja picos en la ACF estacional, y un término AR estacional deja picos en la PACF estacional.

## 8.3 Ejemplo: comercio minorista trimestral europeo
Partiendo de la serie `euretail` y de la inspección gráfica (`tsdisplay`) tras diferenciar, se concluye (PDF p. 86):

- d = 1 y D = 1 parecen necesarios.
- Un pico significativo en el rezago 1 de la ACF sugiere componente MA(1) no estacional.
- Un pico significativo en el rezago 4 de la ACF sugiere componente MA(1) estacional.
- Modelo candidato inicial: ARIMA(0,1,1)(0,1,1)₄ (también podría partirse de ARIMA(1,1,0)(1,1,0)₄).

```r
fit <- Arima(euretail, order=c(0,1,1), seasonal=c(0,1,1))
tsdisplay(residuals(fit))
```

Los residuos muestran picos significativos en el rezago 2 (y quizá el 3), lo que indica que el modelo aún no es adecuado. Comparando por AICc: ARIMA(0,1,2)(0,1,1)₄ da 74.36 y ARIMA(0,1,3)(0,1,1)₄ da 68.53, mejorando el ajuste (PDF p. 87).

```r
fit3 <- Arima(euretail, order=c(0,1,3), seasonal=c(0,1,1))
Box.test(res, lag=16, fitdf=4, type="Ljung")
plot(forecast(fit3, h=12))
```

Con selección automática, `auto.arima(euretail)` elige ARIMA(1,1,1)(0,1,1)₄ (AICc 69.11), mientras que una búsqueda más exhaustiva `auto.arima(euretail, stepwise=FALSE, approximation=FALSE)` encuentra ARIMA(0,1,3)(0,1,1)₄ (AICc 68.53), coherente con la identificación manual (PDF p. 88).

## 8.4 Ejemplo: ventas del fármaco corticosteroide (H02)
Para la serie mensual `h02` (ventas H02 en millones de recetas), se trabaja con transformación logarítmica y diferenciación estacional. La identificación sobre la serie diferenciada estacionalmente arroja (PDF p. 89):

- Elegir D = 1 y d = 0.
- Picos en la PACF en los rezagos 12 y 24 sugieren término AR(2) estacional.
- Picos en la PACF sugieren posible término AR(3) no estacional.
- Modelo candidato inicial: ARIMA(3,0,0)(2,1,0)₁₂.

Se comparan varios candidatos por AICc (PDF p. 90). Entre ellos, el ARIMA(3,0,1)(0,1,2)₁₂ obtiene uno de los mejores valores (AICc −485.48):

```r
fit <- Arima(h02, order=c(3,0,1), seasonal=c(0,1,2), lambda=0)
tsdisplay(residuals(fit))
Box.test(residuals(fit), lag=36, fitdf=6, type="Ljung")
auto.arima(h02, lambda=0)
```

(La comparación de AICc exige el mismo orden de diferenciación en todos los modelos.)

Para comparar sobre conjunto de prueba se usa un entrenamiento jul 91 – jun 06 y prueba jul 06 – jun 08, con una función auxiliar que calcula el RMSE fuera de muestra (PDF p. 91):

```r
getrmse <- function(x,h,...) {
  train <- window(x, end=time(x)[length(x)-h])
  test  <- window(x, start=time(x)[length(x)-h+1])
  fit <- Arima(train,...)
  fc  <- forecast(fit, h=h)
  return(accuracy(fc,test)[2,"RMSE"])
}
```

Conclusiones de la comparación (PDF p. 91):

- Los modelos con menor AICc tienden a dar resultados ligeramente mejores.
- Las comparaciones de AICc exigen el mismo orden de diferenciación; las de RMSE en prueba pueden involucrar cualquier modelo.
- Ningún modelo pasa todas las pruebas de residuos: se usa el mejor disponible aunque no las supere todas.
- El ARIMA(3,0,1)(0,1,2)₁₂ tiene el menor RMSE (0.0622) y el mejor AICc entre modelos con menos de 6 parámetros, por lo que se usa para pronosticar (PDF p. 92).

## 8.5 ARIMA frente a ETS
El capítulo desmonta el mito de que ARIMA sea más general que el suavizado exponencial (PDF p. 92):

- Los modelos de suavizado exponencial lineales son todos casos especiales de ARIMA.
- Los modelos de suavizado exponencial no lineales no tienen contraparte ARIMA.
- Muchos modelos ARIMA no tienen contraparte en suavizado exponencial.
- Los modelos ETS son todos no estacionarios: los que tienen estacionalidad o tendencia no amortiguada (o ambas) tienen dos raíces unitarias; el resto, una.

Equivalencias: suavizado exponencial simple ≡ ARIMA(0,1,1); método de Holt ≡ ARIMA(0,2,2); Holt amortiguado ≡ ARIMA(1,1,2); Holt-Winters aditivo ≡ ARIMA(0,1,m+1)(0,1,0)ₘ (con restricciones de parámetros). Holt-Winters multiplicativo no tiene equivalencia ARIMA.

## 8.6 Sesión de laboratorio 8
Cargando el paquete con `library(fpp)`, los ejercicios pistean el flujo completo (PDF p. 93): elegir una serie estacional (condmilk, hsales, uselec), decidir transformación y diferenciación para lograr estacionariedad, identificar un par de modelos ARIMA y elegir por AIC, estimar parámetros y diagnosticar residuos (¿ruido blanco?), pronosticar 24 meses y comparar con `ets()`. Un segundo ejercicio desarrolla un ARIMA estacional sobre datos de comercio minorista y contrasta con datos reales posteriores.

## Ideas clave
- La notación ARIMA(p,d,q)(P,D,Q)ₘ separa la parte no estacional de la estacional; m es el número de periodos por estación.
- El modelo se obtiene multiplicando los factores AR, de diferenciación y MA de ambas partes, generando rezagos alrededor de los múltiplos de m.
- Los términos estacionales se identifican en los rezagos estacionales (m, 2m…) de la ACF y la PACF; MA estacional deja picos en la ACF, AR estacional en la PACF.
- La diferenciación estacional (D) y no estacional (d) se eligen para lograr estacionariedad antes de identificar p, q, P, Q.
- Se comparan candidatos por AICc (con igual diferenciación) y por RMSE fuera de muestra, validando residuos con Ljung-Box.
- `auto.arima` apoya la selección; búsquedas exhaustivas (stepwise=FALSE, approximation=FALSE) pueden hallar mejores modelos.
- Se usa el mejor modelo disponible aunque no pase todas las pruebas de residuos.
- Los modelos de suavizado exponencial lineales son casos especiales de ARIMA, pero ARIMA no engloba a todo ETS ni viceversa.
