# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 2 — The forecaster's toolbox (La caja de herramientas del analista de pronósticos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con sesiones de laboratorio en R); las citas usan la página del PDF y se conserva solo el código esencial.

## Lo que necesitas saber

Este capítulo reúne las herramientas básicas que se usan antes y después de ajustar cualquier modelo de pronóstico: visualización de series temporales, autocorrelación, análisis de residuos, ruido blanco y medidas de precisión. La tesis central es que un buen pronóstico empieza por entender los patrones de los datos (tendencia, estacionalidad, ciclo) y termina validando que el método no dejó información útil sin explotar.

Sales sabiendo distinguir estacionalidad de ciclo, interpretar un correlograma (ACF), comprobar si los residuos se comportan como ruido blanco mediante inspección visual y tests de portmanteau (Box-Pierce y Ljung-Box), y elegir entre métodos de referencia usando medidas de error (MAE, MSE, RMSE, MAPE, MASE) evaluadas sobre un conjunto de prueba independiente.

El hilo conductor son varias series australianas (ventas de antidiabéticos, producción de cerveza, electricidad, cerdos sacrificados) y el índice Dow-Jones, que ilustran cada concepto con gráficos y código en R.

## Gráficos de series temporales

Más allá del gráfico temporal habitual (`plot`), el capítulo presenta dos vistas para destacar la estacionalidad:

- Gráfico estacional (`seasonplot`): los datos se trazan contra las "estaciones" individuales en que se observaron (por ejemplo, el mes), superponiendo los datos de cada año. Permite ver con claridad el patrón estacional subyacente e identificar desviaciones sustanciales de ese patrón.
- Gráfico de subseries estacionales (`monthplot`): los datos de cada estación se agrupan como series temporales separadas. Permite ver el patrón estacional y los cambios de estacionalidad a lo largo del tiempo.

```r
beer <- window(ausbeer, start=1992)
plot(beer)
seasonplot(beer, year.labels=TRUE)
monthplot(beer)
```

## ¿Estacional o cíclico?

El capítulo define tres patrones (PDF p. 17):

- Tendencia (trend): existe cuando hay un aumento o descenso a largo plazo en los datos.
- Patrón estacional (seasonal): existe cuando la serie está influida por factores estacionales (el trimestre, el mes o el día de la semana).
- Patrón cíclico (cyclic): existe cuando los datos muestran subidas y bajadas que no son de periodo fijo (duración normalmente de al menos 2 años).

Diferencias entre patrones estacionales y cíclicos:

- El patrón estacional tiene longitud constante; el cíclico tiene longitud variable.
- La longitud media de un ciclo es mayor que la del patrón estacional.
- La magnitud del ciclo es más variable que la del patrón estacional.

El momento de picos y valles es predecible con datos estacionales, pero impredecible a largo plazo con datos cíclicos.

## Autocorrelación

Así como la covarianza y la correlación miden la relación lineal entre dos variables, la autocovarianza y la autocorrelación miden la relación lineal entre valores rezagados (lagged) de una misma serie: entre y_t y y_{t-1}, y_t y y_{t-2}, etc. Un gráfico de dispersión rezagado (`lag.plot`) muestra y_t frente a y_{t-k} para distintos k; las autocorrelaciones son las correlaciones asociadas a esos diagramas.

Se denota la autocovarianza muestral en el lag k como c_k y la autocorrelación muestral como r_k, con:

```
c_k = (1/T) Σ_{t=k+1}^{T} (y_t − ȳ)(y_{t−k} − ȳ)      r_k = c_k / c_0
```

- r_1 indica cómo se relacionan valores sucesivos de y.
- r_2 indica cómo se relacionan valores separados dos periodos.
- r_k es casi igual a la correlación muestral entre y_t y y_{t−k}.

El conjunto de autocorrelaciones a lags 1, 2, ... forma la función de autocorrelación o ACF, y su gráfico se llama correlograma. En los datos trimestrales de cerveza, r_4 es más alto que el resto por el patrón estacional (los picos tienden a estar a 4 trimestres de distancia), y r_2 es más negativo porque los valles suelen ir 2 trimestres por detrás de los picos.

Reconocer estacionalidad: si hay estacionalidad, la ACF en el lag estacional será grande y positiva. Para datos mensuales estacionales, se verá un valor de ACF grande en el lag 12 y posiblemente en 24, 36, ...; para datos trimestrales, en el lag 4 y posiblemente en 8, 12, ... En la electricidad mensual australiana, una ACF que decae lentamente indica tendencia, y los picos en los lags 12, 24, 36 indican estacionalidad de longitud 12.

## Residuos de pronóstico

Los residuos en pronóstico son la diferencia entre el valor observado y su pronóstico basado en todas las observaciones previas: e_t = y_t − ŷ_{t|t−1}. Se llaman residuos de pronóstico a un paso (one-step).

Supuestos:

1. Los {e_t} no están correlacionados. Si lo están, queda información en los residuos que debería usarse al pronosticar.
2. Los {e_t} tienen media cero. Si no, los pronósticos están sesgados.

Propiedades útiles (para intervalos de pronóstico):

3. Los {e_t} tienen varianza constante.
4. Los {e_t} se distribuyen normalmente.

El ejemplo usa el índice Dow-Jones con el pronóstico ingenuo (naïve): ŷ_{t|t−1} = y_{t−1}, de modo que e_t = y_t − y_{t−1}.

```r
fc  <- rwf(dj)
res <- residuals(fc)
plot(res)
hist(res, breaks="FD")
Acf(res, main="")
```

## Ruido blanco

El ruido blanco (white noise) es una serie no correlacionada en el tiempo, con media cero y varianza constante (técnicamente también se requiere independencia). Es completamente "poco interesante": no tiene patrones predecibles. Para datos no correlacionados, cada autocorrelación debería estar cerca de cero.

Distribución muestral de las autocorrelaciones: para ruido blanco, r_k se distribuye asintóticamente como N(0, 1/T). Por tanto, el 95% de los r_k debe caer dentro de ±1.96/√T; si no, la serie probablemente no es ruido blanco. Es habitual dibujar líneas en ±1.96/√T en la ACF como valores críticos. Ejemplo: con T = 50, los límites son ±1.96/√50 = ±0.28.

En el ejemplo de cerdos sacrificados en Victoria (1990-1995), es difícil detectar un patrón en el gráfico temporal, pero la ACF muestra autocorrelación significativa en los lags 1, 2 y 3, y un r_12 relativamente grande (aunque no significativo) que podría indicar leve estacionalidad: la serie no es ruido blanco.

ACF de los residuos: suponemos que los residuos son ruido blanco; si no lo son, queda información aprovechable. Por eso un diagnóstico estándar es revisar la ACF de los residuos y esperar que parezcan ruido blanco.

Tests de portmanteau: consideran todo un conjunto de valores r_k y comprueban si difiere significativamente de un conjunto de ceros.

```
Box-Pierce:  Q  = T Σ_{k=1}^{h} r_k^2
Ljung-Box:   Q* = T(T+2) Σ_{k=1}^{h} (T−k)^{-1} r_k^2
```

donde h es el lag máximo y T el número de observaciones. Preferencias del autor: h = 10 para datos no estacionales, h = 2m para estacionales. Si los datos son ruido blanco, Q* tiene distribución χ² con (h − K) grados de libertad, siendo K el número de parámetros del modelo (K = 0 al aplicarlo a datos crudos). Ljung-Box tiene mejor rendimiento, especialmente en muestras pequeñas.

```r
res <- residuals(naive(dj))
Box.test(res, lag=10, fitdf=0)              # Box-Pierce
Box.test(res, lag=10, fitdf=0, type="Lj")   # Ljung-Box
```

## Evaluación de la precisión del pronóstico

Con y_t la observación t y ŷ_{t|t−1} su pronóstico a partir de los datos previos, las medidas de error más útiles son:

```
MAE  = T^{-1} Σ |y_t − ŷ_{t|t−1}|
MSE  = T^{-1} Σ (y_t − ŷ_{t|t−1})^2        RMSE = √MSE
MAPE = 100·T^{-1} Σ |y_t − ŷ_{t|t−1}| / |y_t|
```

MAE, MSE y RMSE dependen de la escala. MAPE es independiente de la escala, pero solo tiene sentido si y_t ≫ 0 para todo t y la serie tiene un cero natural.

El Error Escalado Absoluto Medio (MASE), propuesto por Hyndman y Koehler (IJF, 2006), escala el error por una medida estable Q de la escala de la serie:

```
MASE = T^{-1} Σ |y_t − ŷ_{t|t−1}| / Q
```

Para series no estacionales, Q = (T−1)^{-1} Σ_{t=2}^{T} |y_t − y_{t−1}| y MASE equivale al MAE relativo a un método ingenuo. Para series estacionales, Q = (T−m)^{-1} Σ_{t=m+1}^{T} |y_t − y_{t−m}| y MASE equivale al MAE relativo a un método ingenuo estacional. En la cerveza trimestral, el método ingenuo estacional gana claramente (MASE 0.7673 frente a 2.2990 del método de la media y 4.3498 del ingenuo).

Conjuntos de entrenamiento y prueba: los datos disponibles se dividen en entrenamiento (p. ej., 80%) y prueba (p. ej., 20%). El conjunto de prueba no debe usarse en ningún aspecto del desarrollo del modelo ni del cálculo de pronósticos; la precisión se evalúa solo sobre él.

```r
beer3 <- window(ausbeer, start=1992, end=2005.99)
beer4 <- window(ausbeer, start=2006)
fit1 <- meanf(beer3, h=20)
fit2 <- rwf(beer3, h=20)
accuracy(fit1, beer4)
accuracy(fit2, beer4)
```

Cuidado con el sobreajuste (over-fitting): un modelo que ajusta bien los datos no necesariamente pronostica bien. Siempre puede lograrse un ajuste perfecto con suficientes parámetros (comparar con R²). Sobreajustar es tan malo como no identificar el patrón sistemático. La solución es medir la precisión fuera de muestra (out-of-sample) sobre el conjunto de prueba.

## Lab Session 2

El taller propone cargar el paquete `fpp` (`library(fpp)`) y practicar con `tsdisplay` (gráfico temporal, ACF y dispersión rezagada juntos) sobre series como `bricksq`, `hsales`, `ibmclose` para detectar estacionalidad, ciclicidad y tendencia. Los ejercicios piden aplicar métodos ingenuos, revisar la ACF de los residuos y hacer un test de Ljung-Box, dividir los datos en entrenamiento y prueba, comparar los cuatro métodos de referencia con `accuracy`, y diagnosticar los residuos del mejor método.

## Ideas clave

- Antes de modelar, visualiza: el gráfico temporal, el estacional y el de subseries estacionales revelan tendencia, estacionalidad y ciclo.
- Estacional ≠ cíclico: la estacionalidad tiene periodo fijo y picos predecibles; el ciclo tiene longitud variable y es impredecible a largo plazo.
- La ACF (correlograma) resume las autocorrelaciones; decaimiento lento indica tendencia y picos en los lags estacionales indican estacionalidad.
- Los residuos de pronóstico deben estar no correlacionados y tener media cero; idealmente, varianza constante y normalidad para construir intervalos.
- El ruido blanco no tiene patrones; el 95% de sus autocorrelaciones cae dentro de ±1.96/√T.
- Los tests de portmanteau (Box-Pierce y Ljung-Box) comprueban en bloque si los residuos son ruido blanco; Ljung-Box es preferible en muestras pequeñas.
- Elige medidas de error según el caso: RMSE/MAE (dependen de escala), MAPE (requiere valores positivos) y MASE (comparable entre series).
- Evalúa la precisión solo sobre un conjunto de prueba independiente para evitar el sobreajuste.
