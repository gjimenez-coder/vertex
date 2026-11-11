# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 4 — Time series decomposition (Descomposición de series temporales)

> Nota de extracción: texto extraído de la capa de texto del PDF (material de taller con láminas y sesiones de laboratorio en R); las citas usan la página del PDF.

## Lo que necesitas saber
El capítulo plantea que una serie temporal puede entenderse como la combinación de varias componentes: una estacional, una de tendencia-ciclo y un resto irregular. Formalmente, `Yt = f(St, Tt, Et)`, donde `St` es la componente estacional, `Tt` la tendencia y `Et` el resto (o componente irregular/error) en el periodo `t`. La descomposición aditiva corresponde al caso `Yt = St + Tt + Et`.

Descomponer una serie sirve para dos cosas: comprender mejor los datos antes de modelar y producir pronósticos tratando por separado cada componente. El capítulo presenta el método STL como herramienta flexible y robusta de descomposición, y muestra cómo combinar la descomposición con un método de pronóstico sencillo para obtener predicciones de la serie original.

Al terminar sabrás qué es la descomposición aditiva, cómo obtener datos desestacionalizados, qué ofrece STL y cómo encadenar descomposición y pronóstico en R.

## 4.1 Ejemplo: equipamiento eléctrico en la zona euro
El capítulo usa como hilo conductor el índice de nuevos pedidos de fabricación de equipamiento eléctrico en la zona euro (dataset `elecequip`). Al descomponer la serie se obtienen cuatro paneles: los datos originales, la componente estacional, la tendencia y el resto. Este ejemplo recorre todo el capítulo para ilustrar la estacionalidad, la tendencia-ciclo y la desestacionalización.

## 4.2 Ajuste estacional (seasonal adjustment)
Un subproducto útil de la descomposición es el cálculo sencillo de datos desestacionalizados (seasonally adjusted). En la descomposición aditiva, los datos desestacionalizados se obtienen restando la componente estacional:

```
Yt − St = Tt + Et
```

Es decir, eliminada la estacionalidad queda la combinación de tendencia y resto. Esto facilita ver el movimiento de fondo de la serie sin el patrón estacional.

## 4.3 Descomposición STL
STL significa "Seasonal and Trend decomposition using Loess". Sus características, según el texto:

- Muy versátil y robusto.
- Permite que la componente estacional cambie con el tiempo, y el usuario controla la velocidad de ese cambio.
- El usuario también controla la suavidad de la tendencia-ciclo.
- Robusto frente a valores atípicos (outliers).
- Solo aditivo; para otras descomposiciones se usan transformaciones Box-Cox.

En R la descomposición se obtiene con `stl`:

```r
fit <- stl(elecequip, t.window=15, s.window="periodic", robust=TRUE)
plot(fit)
```

Dos parámetros son clave: `t.window` controla la flexibilidad ("wiggliness") de la componente de tendencia, y `s.window` controla la variación de la componente estacional.

## 4.4 Pronóstico y descomposición
La descomposición se integra con el pronóstico siguiendo estos pasos:

- Pronosticar la componente estacional repitiendo el último año.
- Pronosticar los datos desestacionalizados con un método de serie no estacional (por ejemplo, un modelo ETS).
- Combinar el pronóstico de la componente estacional con el de los datos desestacionalizados para obtener el pronóstico de la serie original.
- A veces la descomposición es útil solo para entender los datos antes de construir un modelo de pronóstico aparte.

En R, el flujo con STL y un paseo aleatorio (random walk / naive) es:

```r
fit <- stl(elecequip, t.window=15, s.window="periodic", robust=TRUE)
eeadj <- seasadj(fit)
plot(naive(eeadj), xlab="New orders index")
fcast <- forecast(fit, method="naive")
plot(fcast, ylab="New orders index")
```

Sobre los intervalos de pronóstico: es habitual tomar los intervalos de los pronósticos desestacionalizados y modificarlos con la componente estacional. El texto advierte que esto ignora tanto la incertidumbre en la estimación de la componente estacional como la incertidumbre en el patrón estacional futuro.

## 4.5 Sesión de laboratorio 5a
Antes de los ejercicios en R se carga el paquete fpp con `library(fpp)`. El ejercicio usa las ventas mensuales del producto A de un fabricante de plásticos (dataset `plastics`, años 1 a 5) y pide: graficar la serie e identificar estacionalidad y/o tendencia; aplicar una descomposición STL para obtener tendencia-ciclo e índices estacionales (probando estacionalidad fija o cambiante); comprobar si los resultados respaldan la interpretación gráfica; calcular y graficar los datos desestacionalizados; usar un paseo aleatorio para pronosticar esos datos; reestacionalizar para dar pronósticos en la escala original (con la función `stlf` y `method="naive"`); y razonar por qué los pronósticos resultan demasiado bajos.

## Ideas clave
- Una serie se descompone en componentes estacional (`St`), de tendencia-ciclo (`Tt`) y resto (`Et`): `Yt = f(St, Tt, Et)`.
- La descomposición aditiva es `Yt = St + Tt + Et`.
- Los datos desestacionalizados se obtienen con `Yt − St = Tt + Et`.
- STL ("Seasonal and Trend decomposition using Loess") es versátil, robusto a outliers y permite estacionalidad cambiante; solo es aditivo (Box-Cox para otras formas).
- En `stl`, `t.window` controla la tendencia y `s.window` la estacionalidad.
- Para pronosticar: predecir la estacionalidad repitiendo el último año, los datos desestacionalizados con un método no estacional (p. ej. ETS), y combinar ambos.
- Modificar los intervalos desestacionalizados con la componente estacional ignora la incertidumbre estacional (presente y futura).
