# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 14 — Forecasting complex seasonality (Pronóstico de estacionalidad compleja)

> Nota de extracción: texto obtenido de la capa de texto del PDF (material de taller con laboratorios en R); las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo breve cierra el curso abordando series temporales con estacionalidad compleja: patrones estacionales múltiples, no enteros y de periodo largo que los modelos clásicos no manejan bien. Los ejemplos motivadores son productos de gasolina terminada en EE. UU. (datos semanales), el número de llamadas a un gran banco americano en intervalos de 5 minutos (de 7am a 9pm) y la demanda eléctrica turca diaria.

La propuesta central es el modelo TBATS, pensado precisamente para captar varias estacionalidades a la vez, incluso con periodos no enteros. Combina términos trigonométricos para la estacionalidad, transformaciones de Box-Cox para la heterogeneidad, errores ARMA para la dinámica de corto plazo, y una tendencia (posiblemente amortiguada).

Sales sabiendo qué componentes integra TBATS, cómo ajustarlo y pronosticar con la función `tbats` del paquete `fpp`/`forecast` en R, y qué comparaciones hacer (validación cruzada, uso de términos de Fourier en lugar de diferenciación estacional) para evaluarlo frente a los otros métodos del curso.

## 14.1 El modelo TBATS

TBATS está diseñado para estacionalidad compleja y reúne cuatro ideas (PDF p. 134):

- Términos trigonométricos para la estacionalidad.
- Transformaciones de Box-Cox para la heterogeneidad (varianza no constante).
- Errores ARMA para la dinámica de corto plazo.
- Tendencia, posiblemente amortiguada.
- Componente estacional que admite periodos múltiples y no enteros.

La transformación de Box-Cox sobre la observación `y_t` es:

```
y_t^(ω) = (y_t^ω − 1)/ω   si ω ≠ 0
y_t^(ω) = log y_t         si ω = 0
```

La serie transformada se descompone en nivel, tendencia, los componentes estacionales y el término de error:

```
y_t^(ω) = ℓ_{t-1} + φ b_{t-1} + Σ_{i=1}^{M} s^{(i)}_{t-m_i} + d_t
```

donde el nivel y la tendencia se actualizan como:

```
ℓ_t = ℓ_{t-1} + φ b_{t-1} + α d_t
b_t = (1−φ) b + φ b_{t-1} + β d_t
```

El término `d_t` sigue un proceso ARMA(p, q):

```
d_t = Σ_{i=1}^{p} φ_i d_{t-i} + Σ_{j=1}^{q} θ_j ε_{t-j} + ε_t
```

Cada estacionalidad `i` se representa mediante una suma de `k_i` armónicos trigonométricos, lo que permite periodos no enteros y reduce el número de parámetros frente a la diferenciación estacional:

```
s^{(i)}_t = Σ_{j=1}^{k_i} s^{(i)}_{j,t}

s^{(i)}_{j,t}  =  s^{(i)}_{j,t-1} cos λ^{(i)}_j + s*^{(i)}_{j,t-1} sin λ^{(i)}_j + γ^{(i)}_1 d_t
s*^{(i)}_{j,t} = −s^{(i)}_{j,t-1} sin λ^{(i)}_j + s*^{(i)}_{j,t-1} cos λ^{(i)}_j + γ^{(i)}_2 d_t
```

## Ejemplos y uso en R

Los tres conjuntos de datos ilustran el ajuste automático de TBATS. La notación del título de cada gráfico resume los parámetros estimados: la potencia de Box-Cox `ω`, el orden ARMA `{p,q}`, el parámetro de amortiguamiento `φ` de la tendencia y, entre llaves angulares, cada periodo estacional con su número de armónicos `<periodo, k>`.

Para la gasolina (datos semanales, periodo estacional anual no entero de 52.18 semanas), el modelo elegido fue TBATS(0.999, {2,2}, 1, {<52.1785714285714,8>}) (PDF p. 135):

```r
fit <- tbats(gasoline)
fcast <- forecast(fit)
plot(fcast)
```

Para las llamadas al centro de atención (intervalos de 5 minutos), con dos estacionalidades —diaria y semanal—, el modelo fue TBATS(1, {3,1}, 0.987, {<169,5>, <845,3>}) (PDF p. 136):

```r
fit <- tbats(callcentre)
fcast <- forecast(fit)
plot(fcast)
```

Para la demanda eléctrica turca (datos diarios) se identificaron tres estacionalidades —semanal, anual aproximada y anual de 365.25 días—, dando TBATS(0, {5,3}, 0.997, {<7,3>, <354.37,12>, <365.25,4>}) (PDF p. 136):

```r
fit <- tbats(turk)
fcast <- forecast(fit)
plot(fcast)
```

En todos los casos el flujo es el mismo: ajustar con `tbats`, generar pronósticos con `forecast` y representarlos con `plot`.

## 14.2 Lab Session 12

Antes de cualquier ejercicio en R, cargar el paquete fpp con `library(fpp)` (PDF p. 137). Los ejercicios proponen:

1. Modelar la serie `visitors` con `tbats`: revisar los residuos y producir pronósticos; valorar si este enfoque totalmente automático funciona para esos datos; y comprobar si se han ahorrado grados de libertad usando términos de Fourier en lugar de diferenciación estacional.
2. Leer datos semanales de gasolina terminada de EE. UU. (miles de barriles/día) y ajustarles un modelo TBATS, revisar residuos y pronosticar, y reflexionar sobre si esos datos podrían modelarse con alguno de los otros métodos del curso:

```r
gas <- read.csv("http://robjhyndman.com/data/gasoline.csv")[,1]
gas <- ts(gas, start=1991+31/365.25, frequency = 365.25/7)
```

3. Experimentar con `nnetar()` (redes neuronales) sobre datos de sesiones de laboratorio previas.
4. Como ejercicio final, usar validación cruzada para comparar objetivamente todos los modelos desarrollados para los datos de comercio minorista (`retail`), calculando los valores de MAE validados por cruzamiento para cada modelo. La ejecución es lenta: conviene dejarla corriendo durante la noche.

El capítulo cierra felicitando por terminar el curso de pronósticos y remite a recursos adicionales en robjhyndman.com/hyndsight/forecasting/ y OTexts.org/fpp (PDF p. 138).

## Ideas clave

- La estacionalidad compleja incluye patrones estacionales múltiples, no enteros y de periodo largo que los métodos clásicos no capturan bien.
- TBATS integra términos Trigonométricos, transformación Box-Cox, errores ARMA, Tendencia (posiblemente amortiguada) y estacionalidad múltiple/no entera.
- La transformación Box-Cox controla la heterogeneidad; con ω = 0 equivale al logaritmo.
- Los términos trigonométricos (armónicos de Fourier) permiten periodos no enteros y ahorran grados de libertad frente a la diferenciación estacional.
- La notación TBATS(ω, {p,q}, φ, {<periodo, k>,...}) resume Box-Cox, orden ARMA, amortiguamiento y cada estacionalidad con su número de armónicos.
- El flujo en R es `tbats()` para ajustar, `forecast()` para pronosticar y `plot()` para visualizar; `fpp` debe cargarse antes.
- La validación cruzada (MAE) permite comparar objetivamente TBATS frente a los otros modelos del curso; `nnetar()` ofrece una alternativa con redes neuronales.
