# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 5 — Time series cross-validation (Validación cruzada de series temporales)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con sesiones de laboratorio en R); las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo explica cómo evaluar modelos de pronóstico de forma honesta cuando los datos son una serie temporal. La partición tradicional en un único conjunto de entrenamiento y uno de prueba, y la validación cruzada estándar (que mezcla observaciones al azar), no respetan el orden temporal. La idea central es la *time series cross-validation*: entrenar con el pasado y evaluar siempre sobre observaciones futuras, avanzando el origen del pronóstico paso a paso.

El procedimiento se conoce también como *rolling forecasting origin* (origen de pronóstico deslizante), porque el punto desde el que se pronostica se desplaza hacia adelante en el tiempo. Fija un tamaño mínimo de entrenamiento `k`, ajusta el modelo con lo observado hasta ese punto, mide el error del pronóstico futuro y repite ampliando (o desplazando) la ventana.

Sales sabiendo cómo montar en R un bucle de validación cruzada temporal, cómo comparar modelos (LM, ARIMA, ETS) por horizonte usando el MAE, qué variantes existen (ventana fija y pronósticos a un paso), y la conexión teórica entre minimizar el AIC y la validación cruzada a un paso.

## Cross-validation

La evaluación tradicional divide la serie en un bloque de entrenamiento y un bloque de prueba al final. La validación cruzada estándar, en cambio, reparte las observaciones en varios grupos sin tener en cuenta el orden, algo inadecuado para series temporales.

En la validación cruzada de series temporales, sea `k` el número mínimo de observaciones para un conjunto de entrenamiento:

- Se selecciona la observación `k + i` para el conjunto de prueba y se usan las observaciones en los tiempos `1, 2, ..., k + i − 1` para estimar el modelo. Se calcula el error del pronóstico para el tiempo `k + i`.
- Se repite para `i = 0, 1, ..., T − k`, donde `T` es el número total de observaciones.
- Se calcula una medida de precisión sobre todos los errores.

Por eso se llama *rolling forecasting origin*: el origen `(k + i − 1)` en que se basa el pronóstico rueda hacia adelante en el tiempo.

Existe además una relación teórica entre selección de modelos y validación cruzada. En datos transversales (*cross-sectional*), minimizar el AIC es asintóticamente equivalente a minimizar el MSE mediante *leave-one-out cross-validation* (Stone, 1977). En series temporales, minimizar el AIC es asintóticamente equivalente a minimizar el MSE mediante validación cruzada a un paso (Akaike, 1969, 1973).

## Ejemplo: ventas farmacéuticas

El ejemplo hilo conductor son las ventas de fármacos antidiabéticos (serie `a10`), observadas entre 1995 y 2005 y analizadas también en escala logarítmica. La pregunta es cuál de tres modelos pronostica mejor:

1. Modelo lineal con tendencia y variables ficticias estacionales, aplicado a los datos en logaritmo.
2. Modelo ARIMA aplicado a los datos en logaritmo.
3. Modelo ETS aplicado a los datos originales.

El diseño de la validación cruzada fija `k = 48` como conjunto de entrenamiento mínimo, pronostica 12 pasos hacia adelante a partir de los datos hasta el tiempo `k + i − 1` para `i = 1, 2, ..., 156`, y compara el MAE en cada horizonte de pronóstico. El código esencial:

```r
k <- 48
n <- length(a10)
mae1 <- mae2 <- mae3 <- matrix(NA, n-k-12, 12)
for(i in 1:(n-k-12))
{
  xshort <- window(a10, end=1995+(5+i)/12)
  xnext  <- window(a10, start=1995+(6+i)/12, end=1996+(5+i)/12)
  fit1 <- tslm(xshort ~ trend + season, lambda=0)
  fcast1 <- forecast(fit1, h=12)
  fit2 <- auto.arima(xshort, D=1, lambda=0)
  fcast2 <- forecast(fit2, h=12)
  fit3 <- ets(xshort)
  fcast3 <- forecast(fit3, h=12)
  mae1[i,] <- abs(fcast1[['mean']]-xnext)
  mae2[i,] <- abs(fcast2[['mean']]-xnext)
  mae3[i,] <- abs(fcast3[['mean']]-xnext)
}
plot(1:12, colMeans(mae1), type="l", col=2, xlab="horizon", ylab="MAE")
lines(1:12, colMeans(mae2), type="l", col=3)
lines(1:12, colMeans(mae3), type="l", col=4)
legend("topleft", legend=c("LM","ARIMA","ETS"), col=2:4, lty=1)
```

Cada fila del bucle amplía la ventana de entrenamiento (`xshort`) y toma los 12 meses siguientes (`xnext`) como prueba. Al promediar los errores absolutos por columna con `colMeans`, se obtiene el MAE por horizonte para cada modelo, que se grafica en función del horizonte (1 a 12 meses).

## Variantes de la validación cruzada de series temporales

El esquema básico admite modificaciones. La primera es mantener la ventana de entrenamiento de longitud fija, en vez de ampliarla, deslizando también su inicio:

```r
xshort <- window(a10, start=i+1/12, end=1995+(5+i)/12)
```

La segunda variante calcula pronósticos a un paso en el período fuera de muestra. En lugar de reajustar el modelo en cada iteración, se estima el modelo con la ventana corta (`xshort`) y luego se aplica el mismo modelo a la ventana larga (`xlong`) para obtener los residuos, que son los errores a un paso:

```r
for(i in 1:(n-k))
{
  xshort <- window(a10, end=1995+(5+i)/12)
  xlong  <- window(a10, start=1995+(6+i)/12)
  fit2  <- auto.arima(xshort, D=1, lambda=0)
  fit2a <- Arima(xlong, model=fit2)
  fit3  <- ets(xshort)
  fit3a <- ets(xlong, model=fit3)
  mae2a[i,] <- abs(residuals(fit3a))
  mae3a[i,] <- abs(residuals(fit2a))
}
```

Con los pronósticos a un paso, el MAE se compara igualmente por horizonte entre LM, ARIMA y ETS.

## Lab Session 5b

La sesión de laboratorio aplica la validación cruzada temporal a datos reales. Antes de los ejercicios se carga el paquete con `library(fpp)`.

El ejercicio principal usa los datos mensuales de visitantes extranjeros de corta estancia a Australia, de mayo de 1985 a abril de 2005 (conjunto `visitors` del paquete `expsmooth`):

- (a) Con `ets` se busca el mejor modelo y se registra el RMSE del conjunto de entrenamiento; el mejor resulta ser ETS(M,A,M).
- (b) Se comprueba cuánto mayor es el RMSE a un paso fuera de muestra mediante validación cruzada temporal, empezando con cuatro años de datos en el entrenamiento:

```r
k <- 48              # tamaño mínimo del entrenamiento
n <- length(visitors)
e <- visitors * NA   # vector de errores de pronóstico a un paso
for(i in 48:(n-1))
{
  train <- ts(visitors[1:i], freq=12)
  fit <- ets(train, "MAM", damped=FALSE)
  fc  <- forecast(fit, h=1)$mean
  e[i] <- visitors[i+1] - fc
}
sqrt(mean(e^2, na.rm=TRUE))
```

El resto del ejercicio pide entender y reflexionar sobre el código: qué pasaría si `train <- visitors[1:i]` (sin `ts`); graficar `e` y observar las varianzas de los errores y por qué ocurre; cómo sesga ese problema la comparación de los RMSE de (a) y (b) por los valores faltantes en `e`; y rehacer el análisis dejando que `ets` seleccione un modelo distinto en cada iteración —más realista, porque en la práctica no se sabe de antemano que el mejor modelo sobre todos los datos es ETS(M,A,M)— para comparar ese RMSE con el de (b) y ver si la reselección del modelo en cada paso cambia mucho el resultado.

El segundo ejercicio propone aplicar un enfoque de validación cruzada similar a otra de las series ya consideradas, comprobando si la selección de modelo de `ets()` mediante AICc da el mismo modelo que la validación cruzada, y decidiendo qué modelo se usaría en la práctica.

## Ideas clave

- La validación cruzada de series temporales respeta el orden temporal: se entrena con el pasado y se evalúa sobre el futuro.
- Es un *rolling forecasting origin*: el origen del pronóstico `(k + i − 1)` se desplaza hacia adelante y se promedian los errores.
- `k` es el tamaño mínimo del conjunto de entrenamiento; se repite para `i = 0, 1, ..., T − k`.
- Minimizar el AIC equivale asintóticamente a la validación cruzada *leave-one-out* (transversal) o a un paso (series temporales).
- En las ventas de antidiabéticos se comparan LM, ARIMA y ETS por horizonte usando el MAE con `k = 48` y 12 pasos adelante.
- Variantes: ventana de entrenamiento de longitud fija y pronósticos a un paso obtenidos aplicando el modelo ajustado a la ventana larga.
- El RMSE a un paso fuera de muestra suele ser mayor que el del entrenamiento; los valores faltantes en el vector de errores pueden sesgar la comparación.
- Permitir que `ets` reseleccione el modelo en cada paso es más realista que fijar ETS(M,A,M) de antemano.
