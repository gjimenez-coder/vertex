# The forecaster's toolbox (La caja de herramientas del analista de pronósticos) — Estudio

## Tarjetas de repaso

P: ¿Qué muestra un gráfico estacional (`seasonplot`)? / R: Traza los datos contra las estaciones individuales en que se observaron, superponiendo cada año, para ver con claridad el patrón estacional y sus desviaciones.

P: ¿Qué aporta un gráfico de subseries estacionales (`monthplot`)? / R: Agrupa los datos de cada estación como series separadas, mostrando el patrón estacional y sus cambios a lo largo del tiempo.

P: ¿Qué es una tendencia (trend)? / R: Un aumento o descenso a largo plazo en los datos.

P: ¿Qué diferencia a un patrón estacional de uno cíclico? / R: El estacional tiene longitud constante y picos/valles predecibles; el cíclico tiene longitud variable, media mayor, magnitud más variable y es impredecible a largo plazo (periodo de al menos 2 años).

P: ¿Qué miden la autocovarianza y la autocorrelación? / R: La relación lineal entre valores rezagados (lagged) de una misma serie, por ejemplo entre y_t y y_{t−1}, y_t y y_{t−2}, etc.

P: ¿Cómo se definen c_k y r_k? / R: c_k = (1/T) Σ (y_t − ȳ)(y_{t−k} − ȳ) es la autocovarianza muestral en el lag k; r_k = c_k / c_0 es la autocorrelación muestral.

P: ¿Qué son la ACF y el correlograma? / R: La ACF (función de autocorrelación) es el conjunto de autocorrelaciones a los lags 1, 2, …; su gráfico es el correlograma.

P: ¿Cómo se reconoce la estacionalidad en la ACF? / R: El valor de la ACF en el lag estacional es grande y positivo: lag 12 (y 24, 36) en datos mensuales, lag 4 (y 8, 12) en trimestrales.

P: ¿Qué es un residuo de pronóstico a un paso? / R: La diferencia entre el valor observado y su pronóstico basado en todas las observaciones previas: e_t = y_t − ŷ_{t|t−1}.

P: ¿Qué dos supuestos deben cumplir los residuos y qué pasa si fallan? / R: Deben estar no correlacionados (si no, queda información aprovechable) y tener media cero (si no, los pronósticos están sesgados).

P: ¿Qué es el ruido blanco (white noise)? / R: Una serie no correlacionada en el tiempo, con media cero y varianza constante (idealmente independiente), sin patrones predecibles.

P: ¿Cuál es la distribución muestral de r_k para ruido blanco y su límite crítico? / R: r_k ~ N(0, 1/T) asintóticamente; el 95% de los r_k debe caer dentro de ±1.96/√T.

P: ¿Para qué sirven los tests de portmanteau Box-Pierce y Ljung-Box? / R: Comprueban en bloque si todo un conjunto de valores r_k difiere significativamente de ceros, es decir, si los residuos son ruido blanco; Ljung-Box rinde mejor en muestras pequeñas.

P: ¿Qué medidas de error dependen de la escala y cuál es independiente pero requiere valores positivos? / R: MAE, MSE y RMSE dependen de la escala; MAPE es independiente de la escala pero solo tiene sentido si y_t ≫ 0 y la serie tiene un cero natural.

P: ¿Qué es el MASE y qué ventaja tiene? / R: El Error Escalado Absoluto Medio escala el error por una medida estable Q de la escala de la serie, lo que lo hace comparable entre series; equivale al MAE relativo a un método ingenuo.

## Preguntas de autoevaluación

P: ¿Por qué el momento de los picos y valles es predecible en datos estacionales pero no en datos cíclicos? / R: Porque el patrón estacional tiene longitud constante, mientras que el ciclo tiene longitud variable y magnitud más variable, haciéndolo impredecible a largo plazo. (Sección: ¿Estacional o cíclico?)

P: En los datos trimestrales de cerveza, ¿por qué r_4 es más alto y r_2 más negativo? / R: Porque el patrón estacional hace que los picos estén a 4 trimestres de distancia (r_4 alto) y los valles vayan 2 trimestres por detrás de los picos (r_2 negativo). (Sección: Autocorrelación)

P: ¿Qué propiedades adicionales de los residuos se desean y para qué sirven? / R: Varianza constante y distribución normal; son útiles para construir intervalos de pronóstico. (Sección: Residuos de pronóstico)

P: Con T = 50, ¿cuál es el límite crítico para las autocorrelaciones de ruido blanco? / R: ±1.96/√50 = ±0.28. (Sección: Ruido blanco)

P: ¿Qué grados de libertad tiene Q* en el test de Ljung-Box y qué lag máximo recomienda el autor? / R: χ² con (h − K) grados de libertad, siendo K el número de parámetros (K = 0 sobre datos crudos); h = 10 para datos no estacionales y h = 2m para estacionales. (Sección: Ruido blanco)

P: ¿Por qué no debe usarse el conjunto de prueba durante el desarrollo del modelo? / R: Porque la precisión se evalúa solo sobre ese conjunto independiente; usarlo invalidaría la medida de precisión fuera de muestra. (Sección: Evaluación de la precisión del pronóstico)

P: ¿Qué es el sobreajuste (over-fitting) y cómo se evita? / R: Es ajustar tan bien los datos de entrenamiento que el modelo no pronostica bien; siempre se logra un ajuste perfecto con suficientes parámetros. Se evita midiendo la precisión fuera de muestra sobre el conjunto de prueba. (Sección: Evaluación de la precisión del pronóstico)

P: En la cerveza trimestral, ¿qué método de referencia gana y con qué MASE? / R: El método ingenuo estacional, con MASE 0.7673, frente a 2.2990 del método de la media y 4.3498 del ingenuo. (Sección: Evaluación de la precisión del pronóstico)

## Checklist

- Visualiza la serie con el gráfico temporal, el estacional (`seasonplot`) y el de subseries estacionales (`monthplot`) para detectar tendencia, estacionalidad y ciclo.
- Usa `tsdisplay` para ver juntos el gráfico temporal, la ACF y la dispersión rezagada.
- Interpreta el correlograma: decaimiento lento indica tendencia; picos en los lags estacionales indican estacionalidad.
- Calcula residuos de pronóstico y comprueba que no estén correlacionados y tengan media cero (inspecciona `plot`, `hist` y `Acf` de los residuos).
- Verifica si los residuos son ruido blanco revisando que el 95% de las autocorrelaciones caiga dentro de ±1.96/√T.
- Aplica un test de portmanteau (`Box.test` con `type="Lj"` para Ljung-Box) usando h = 10 (no estacional) o h = 2m (estacional).
- Divide los datos en entrenamiento (~80%) y prueba (~20%) sin usar el conjunto de prueba en el desarrollo del modelo.
- Compara los métodos de referencia con `accuracy` sobre el conjunto de prueba y elige la medida de error adecuada (RMSE/MAE, MAPE o MASE) según la escala y el signo de los datos.
- Evita el sobreajuste evaluando la precisión fuera de muestra, no por el ajuste a los datos de entrenamiento.
