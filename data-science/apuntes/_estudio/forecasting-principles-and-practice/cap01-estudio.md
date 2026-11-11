# Introduction to forecasting (Introducción a la predicción) — Estudio

## Tarjetas de repaso

P: ¿Qué es una serie temporal? / R: Una secuencia de observaciones recogidas a lo largo del tiempo, que se asume igualmente espaciadas (p. ej. precios diarios de acciones, lluvia mensual).

P: ¿Qué significa predecir una serie temporal? / R: Estimar cómo continuará esa secuencia en el futuro.

P: ¿Cuál es el objetivo del taller y qué NO pretende? / R: Enseñar herramientas de predicción, cuándo usarlas y cómo aplicarlas con eficacia; no deriva teoría ni introduce R o la estadística desde cero.

P: ¿Qué conocimientos previos se asumen? / R: Comodidad con R y con conceptos como media, desviación estándar, cuantiles, regresión y distribución normal.

P: ¿Qué clase de R se usa para representar series temporales? / R: La clase `ts`, que incorpora métodos de impresión y de gráfico, indicando frecuencia e inicio.

P: ¿Qué trae cargar el paquete `fpp`? / R: Datos de ejemplo y los paquetes `forecast`, `tseries`, `fma`, `expsmooth` y `lmtest`.

P: ¿Qué es el método de la media? / R: Todas las predicciones futuras son iguales a la media de los datos históricos: $\hat y_{T+h|T} = \bar y$.

P: ¿Qué es el método naïve? / R: Las predicciones son iguales al último valor observado, $\hat y_{T+h|T} = y_T$; es consecuencia de la hipótesis del mercado eficiente.

P: ¿Qué es el método naïve estacional? / R: Las predicciones son iguales al último valor de la misma estación, $\hat y_{T+h|T} = y_{T+h-km}$, con $m$ el periodo estacional.

P: ¿Qué es el método drift? / R: El último valor más el cambio medio observado; equivale a extrapolar la recta que une la primera y la última observación.

P: ¿Para qué sirven los cuatro métodos simples (benchmark)? / R: Como punto de comparación y mínimo a batir: cualquier modelo más sofisticado debería mejorarlos.

P: ¿Qué representa la notación $\hat y_{T+h|T}$? / R: La predicción a horizonte $h$ dadas las $T$ observaciones.

P: ¿Qué función de R corresponde al método drift? / R: `rwf(x, drift=TRUE, h=20)`.

P: ¿De qué depende la elección del método benchmark? / R: De la naturaleza de la serie: estacionaria, con tendencia o estacional.

## Preguntas de autoevaluación

P: ¿Cuál es el enfoque del taller y en qué libro y paquete se apoya? / R: Enseñar el uso práctico de herramientas de predicción, apoyándose en Hyndman & Athanasopoulos (2013), *Forecasting: principles and practice* (OTexts.org/fpp), y el paquete de R `fpp`. (Sección: Lo que necesitas saber / Contexto del taller y herramientas)

P: ¿Qué tres casos de estudio motivan el capítulo y qué tipo de problema ilustran? / R: Empresa de papel (cientos de productos estacionarios, con tendencia o estacionales con un programa en COBOL inadecuado), PBS (miles de fármacos con demanda estacional pronosticados con Excel) y una aerolínea (tráfico de pasajeros afectado por vacaciones, eventos y competencia). (Sección: Casos de estudio)

P: ¿Qué error costoso ocurrió en el caso del PBS? / R: En 2001 un presupuesto de 4.500 millones fue infraestimado en 800 millones; además agregaban 10 años de datos mensuales a valores anuales usando solo los tres primeros años. (Sección: Casos de estudio)

P: ¿Cómo se construye un objeto `ts` en R y qué información hay que indicar? / R: Con `ts(...)` indicando frecuencia (p. ej. 4 para trimestral) e inicio; ejemplo: `ausgdp <- ts(scan("gdp.dat"), frequency=4, start=1971+2/4)`. (Sección: Datos de series temporales)

P: ¿Qué diferencia al método naïve del naïve estacional? / R: El naïve usa el último valor observado ($y_T$), mientras el naïve estacional usa el último valor de la misma estación ($y_{T+h-km}$). (Sección: Métodos simples de predicción (benchmark))

P: ¿Por qué se dice que el método drift extrapola una recta? / R: Porque la predicción es $y_T + \frac{h}{T-1}(y_T - y_1)$, lo que equivale a prolongar la recta que une la primera y la última observación. (Sección: Métodos simples de predicción (benchmark))

P: ¿Qué pide la sesión de laboratorio 1 con el índice Dow Jones? / R: Graficar la serie `dowjones`, predecir con el método drift y mostrar que las predicciones coinciden con prolongar la recta entre la primera y la última observación, probando también los otros métodos benchmark para decidir cuál es mejor y por qué. (Sección: Sesión de laboratorio 1)

## Checklist

- [ ] Instalar y cargar el paquete: `install.packages("fpp", dependencies=TRUE)` y `library(fpp)`.
- [ ] Usar la ayuda de R cuando se necesite: `help.search("forecasting")`, `help(forecast)`, `example("forecast.ar")`, `apropos("forecast")`, `help(package="fpp")`.
- [ ] Representar datos con la clase `ts`, indicando frecuencia e inicio, y graficarlos con `plot`.
- [ ] Graficar `dowjones`, aplicar `rwf(x, drift=TRUE, h=20)` y comprobar que coincide con la recta entre la primera y la última observación.
- [ ] Probar los cuatro métodos benchmark con `meanf`, `naive`/`rwf`, `snaive` y `rwf(drift=TRUE)` para decidir el más adecuado.
- [ ] Graficar `bicoal`, `chicken`, `dole`, `usdeaths`, `bricksq` y `lynx` con el método benchmark más apropiado y valorar si las predicciones son razonables y cómo mejorarlas.
