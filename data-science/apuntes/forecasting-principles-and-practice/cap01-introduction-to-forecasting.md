# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 1 — Introduction to forecasting (Introducción a la predicción)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con sesiones de laboratorio en R); las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo abre un taller práctico de predicción de series temporales basado en el libro de referencia Hyndman & Athanasopoulos (2013), *Forecasting: principles and practice* (OTexts.org/fpp), gratuito y en línea, con datos y código en el paquete de R `fpp`. El enfoque no es teórico ni una introducción a R o a la estadística: se asume comodidad previa con R y con conceptos como media, desviación estándar, cuantiles, regresión y distribución normal. El objetivo es enseñar herramientas de predicción, cuándo usarlas y cómo aplicarlas con eficacia (PDF p. 7).

El capítulo motiva la materia con tres casos reales, define qué es una serie temporal y qué significa predecir, muestra cómo representar datos temporales en R con la clase `ts`, y presenta cuatro métodos de referencia (benchmark) simples: media, naïve, naïve estacional y drift. Estos métodos sirven como punto de comparación para evaluar cualquier modelo más sofisticado.

Al terminar sales sabiendo qué es predecir una serie temporal, cómo cargar y graficar datos con el paquete `fpp`, y cómo producir predicciones base con cuatro métodos cuyo acierto depende de la naturaleza de la serie (estacionaria, con tendencia o estacional).

## Contexto del taller y herramientas

El material proviene de un taller impartido por Hyndman, director de la Business & Economic Forecasting Unit de Monash University y editor jefe del *International Journal of Forecasting*. Su metodología se aplica en ámbitos como el Pharmaceutical Benefits Scheme, incidencia y mortalidad de cáncer, demanda eléctrica, envejecimiento poblacional y venta de fertilizantes (PDF p. 5).

La referencia clave y fuente de datos y código es Hyndman & Athanasopoulos (2013). El paquete principal del curso se instala y carga así:

```r
install.packages("fpp", dependencies=TRUE)
library(fpp)
```

Cargar `fpp` trae datos de ejemplo y los paquetes `forecast` (funciones de predicción), `tseries`, `fma` y `expsmooth` (datos de series temporales) y `lmtest` (funciones de regresión) (PDF p. 10). Para obtener ayuda en R el capítulo recuerda `help.search("forecasting")`, `help(forecast)`, `example("forecast.ar")`, `apropos("forecast")` y `help(package="fpp")` (PDF p. 6).

## Casos de estudio

El capítulo ilustra la diversidad de problemas de predicción con tres casos (PDF p. 7-8):

- Caso 1 — Empresa de papel. Necesitan predecir cientos de productos cuyas series pueden ser estacionarias, con tendencia o estacionales. Tienen un programa interno en COBOL que no produce predicciones sensatas, con cálculo numérico limitado y sin posibilidad de optimización; no emplean estadísticos y quieren predicciones automáticas. Los métodos que usaban eran ad hoc: media de 12 o 6 meses, regresión lineal sobre los últimos 12 o 6 meses, y la pendiente media entre el valor del año pasado y el actual (equivalente a diferenciar en el lag 12 y tomar la media).

- Caso 2 — PBS. El Pharmaceutical Benefits Scheme es el esquema australiano de subsidio de medicamentos; su coste roza el 1% del PIB y se presupuesta a partir de predicciones de uso de fármacos. En 2001 hubo un presupuesto de 4.500 millones infraestimado en 800 millones. Son miles de productos con demanda estacional, afectados por marketing encubierto y gasto incontrolable; pese a disponer de 10 años de datos mensuales, se agregaban a valores anuales usando solo los tres primeros años, y todas las predicciones se hacían con la función FORECAST de MS-Excel.

- Caso 3 — Aerolínea. Buscan predecir el tráfico de pasajeros (primera, business y economy) en rutas principales como Melbourne–Sídney. Disponen de mucho dato histórico y de un equipo capaz, pero el tráfico se ve afectado por vacaciones escolares, eventos especiales (como el Gran Premio), campañas publicitarias y la competencia.

## Datos de series temporales

Una serie temporal es una secuencia de observaciones recogidas a lo largo del tiempo, que se asume igualmente espaciadas (precios diarios de acciones de IBM, lluvia mensual, beneficios anuales de Google, producción trimestral de cerveza australiana). Predecir es estimar cómo continuará esa secuencia en el futuro (PDF p. 8).

En R las series se representan con la clase `ts`, que incorpora métodos de impresión y de gráfico. El ejemplo del PIB australiano se construye indicando frecuencia (trimestral) e inicio:

```r
ausgdp <- ts(scan("gdp.dat"), frequency=4, start=1971+2/4)
plot(ausgdp)
```

Al imprimir un objeto `ts` se muestran los datos ordenados por periodo (p. ej. por trimestre), y para series anuales como `elecsales` (ventas eléctricas residenciales) aparecen inicio, fin y frecuencia (PDF p. 9-10).

## Métodos simples de predicción (benchmark)

El capítulo presenta cuatro métodos de referencia. Sirven como mínimos a batir: cualquier modelo elaborado debería mejorarlos. La notación $\hat y_{T+h|T}$ es la predicción a horizonte $h$ dadas las $T$ observaciones (PDF p. 12).

- Método de la media. Todas las predicciones futuras son iguales a la media de los datos históricos:
  $$\hat y_{T+h|T} = \bar y = (y_1 + \cdots + y_T)/T.$$

- Método naïve (solo para series temporales). Las predicciones son iguales al último valor observado, $\hat y_{T+h|T} = y_T$. Es consecuencia de la hipótesis del mercado eficiente.

- Método naïve estacional. Las predicciones son iguales al último valor de la misma estación: $\hat y_{T+h|T} = y_{T+h-km}$, donde $m$ es el periodo estacional y $k = \lfloor (h-1)/m \rfloor + 1$.

- Método drift. Las predicciones son el último valor más el cambio medio observado:
  $$\hat y_{T+h|T} = y_T + \frac{h}{T-1}\sum_{t=2}^{T}(y_t - y_{t-1}) = y_T + \frac{h}{T-1}(y_T - y_1).$$
  Equivale a extrapolar la recta que une la primera y la última observación.

Funciones correspondientes en R (PDF p. 12):

```r
meanf(x, h=20)              # media
naive(x, h=20)             # naïve (o rwf(x, h=20))
snaive(x, h=20)            # naïve estacional
rwf(x, drift=TRUE, h=20)   # drift
```

## Sesión de laboratorio 1

La sesión práctica pide, tras cargar el paquete con `library(fpp)` (PDF p. 13): usar el índice Dow Jones (`dowjones`) para graficar la serie, predecir con el método drift y mostrar que las predicciones coinciden con prolongar la recta entre la primera y la última observación, probando también los otros métodos benchmark para decidir cuál es mejor y por qué. Después, para una serie de ejemplos (producción de carbón bituminoso `bicoal`, precio del pollo `chicken`, personas en subsidio de desempleo en Australia `dole`, muertes accidentales en EE. UU. `usdeaths`, producción de ladrillos `bricksq` y capturas de lince canadiense `lynx`), se debe graficar cada una con el método benchmark más apropiado —media, naïve, naïve estacional o drift— y valorar si las predicciones son razonables y cómo mejorarlas.

## Ideas clave

- El taller enseña herramientas de predicción y su uso práctico; no deriva teoría ni introduce R o estadística desde cero, apoyándose en el libro `fpp` y su paquete de R.
- Una serie temporal es una secuencia de observaciones igualmente espaciadas; predecir es estimar su continuación futura.
- Los casos (empresa de papel, PBS, aerolínea) muestran series estacionarias, con tendencia y estacionales, con herramientas inadecuadas (COBOL, Excel) y errores costosos como la infraestimación de 800 millones del PBS en 2001.
- En R los datos se manejan con la clase `ts`, indicando frecuencia e inicio, y se cargan y grafican fácilmente con el paquete `fpp`.
- Cuatro métodos simples sirven de referencia: media (promedio histórico), naïve (último valor), naïve estacional (último valor de la misma estación) y drift (último valor más el cambio medio).
- El método drift equivale a extrapolar la recta que une la primera y la última observación.
- La elección del método benchmark depende de la naturaleza de la serie; estos métodos son el mínimo a superar por cualquier modelo más avanzado.
