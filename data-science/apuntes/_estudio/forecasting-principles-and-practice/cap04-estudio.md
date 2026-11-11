# Time series decomposition (Descomposición de series temporales) — Estudio

## Tarjetas de repaso

P: ¿En qué componentes se descompone una serie temporal según el capítulo? / R: En una componente estacional (`St`), una de tendencia-ciclo (`Tt`) y un resto o componente irregular (`Et`), con la forma general `Yt = f(St, Tt, Et)`.

P: ¿Cuál es la fórmula de la descomposición aditiva? / R: `Yt = St + Tt + Et`.

P: ¿Para qué sirve descomponer una serie? / R: Para comprender mejor los datos antes de modelar y para producir pronósticos tratando por separado cada componente.

P: ¿Cómo se obtienen los datos desestacionalizados (seasonally adjusted) en la descomposición aditiva? / R: Restando la componente estacional: `Yt − St = Tt + Et`, lo que deja la combinación de tendencia y resto.

P: ¿Qué significa el acrónimo STL? / R: "Seasonal and Trend decomposition using Loess".

P: ¿Cuáles son las características de STL según el texto? / R: Es versátil y robusto, permite que la componente estacional cambie con el tiempo (a velocidad controlada por el usuario), permite controlar la suavidad de la tendencia-ciclo, es robusto frente a outliers y solo es aditivo.

P: ¿Qué se hace en STL cuando se necesita una descomposición no aditiva? / R: Se usan transformaciones Box-Cox, ya que STL solo es aditivo.

P: ¿Qué controlan los parámetros `t.window` y `s.window` en la función `stl`? / R: `t.window` controla la flexibilidad ("wiggliness") de la componente de tendencia y `s.window` controla la variación de la componente estacional.

P: ¿Qué pasos sigue el pronóstico basado en descomposición? / R: Pronosticar la componente estacional repitiendo el último año, pronosticar los datos desestacionalizados con un método no estacional (p. ej. un modelo ETS) y combinar ambos para obtener el pronóstico de la serie original.

P: ¿Qué dataset se usa como hilo conductor del capítulo? / R: `elecequip`, el índice de nuevos pedidos de fabricación de equipamiento eléctrico en la zona euro.

P: ¿Qué cuatro paneles se obtienen al descomponer la serie `elecequip`? / R: Los datos originales, la componente estacional, la tendencia y el resto.

P: ¿Qué advierte el texto sobre los intervalos de pronóstico al reestacionalizar? / R: Que tomar los intervalos de los pronósticos desestacionalizados y modificarlos con la componente estacional ignora tanto la incertidumbre en la estimación de la componente estacional como la del patrón estacional futuro.

P: ¿Qué función y método se usan para reestacionalizar y dar pronósticos en la escala original en el laboratorio? / R: La función `stlf` con `method="naive"`.

## Preguntas de autoevaluación

P: Escribe la relación general y la forma aditiva de la descomposición y explica qué representa cada término. / R: General: `Yt = f(St, Tt, Et)`; aditiva: `Yt = St + Tt + Et`, donde `St` es la componente estacional, `Tt` la tendencia-ciclo y `Et` el resto o componente irregular en el periodo `t`. (Sección "Lo que necesitas saber")

P: ¿Cómo calcularías los datos desestacionalizados de una serie descompuesta de forma aditiva y qué queda tras quitar la estacionalidad? / R: Restando la componente estacional (`Yt − St`), con lo que queda la combinación de tendencia y resto (`Tt + Et`), permitiendo ver el movimiento de fondo sin el patrón estacional. (Sección 4.2 Ajuste estacional)

P: ¿Por qué se considera STL un método flexible y robusto? / R: Porque permite que la estacionalidad cambie con el tiempo a velocidad controlada por el usuario, permite controlar la suavidad de la tendencia-ciclo y es robusto frente a outliers. (Sección 4.3 Descomposición STL)

P: Describe el flujo de pronóstico con STL y un paseo aleatorio tal como se presenta. / R: Se ajusta con `stl`, se obtienen los datos desestacionalizados con `seasadj`, se pronostican con un método naive y se combina con la estacionalidad usando `forecast(fit, method="naive")` para predecir la serie original. (Sección 4.4 Pronóstico y descomposición)

P: ¿Qué limitación tiene STL respecto al tipo de descomposición y cómo se soluciona? / R: STL solo es aditivo; para otras descomposiciones se usan transformaciones Box-Cox. (Sección 4.3 Descomposición STL)

P: En el laboratorio con el dataset `plastics`, ¿qué tareas se piden al estudiante? / R: Graficar la serie e identificar estacionalidad/tendencia, aplicar STL para obtener tendencia-ciclo e índices estacionales (fija o cambiante), comprobar la interpretación gráfica, calcular y graficar los datos desestacionalizados, pronosticar con paseo aleatorio, reestacionalizar con `stlf`/`method="naive"` y razonar por qué los pronósticos resultan demasiado bajos. (Sección 4.5 Sesión de laboratorio 5a)

P: ¿Por qué hay que ser cauto al construir intervalos de pronóstico a partir de datos desestacionalizados? / R: Porque modificar esos intervalos con la componente estacional ignora la incertidumbre en la estimación de la componente estacional y en el patrón estacional futuro. (Sección 4.4 Pronóstico y descomposición)

## Checklist

- Graficar la serie original e identificar visualmente estacionalidad y/o tendencia.
- Cargar el paquete necesario antes de los ejercicios en R (`library(fpp)`).
- Ajustar una descomposición STL con `stl`, eligiendo `t.window` (tendencia) y `s.window` (estacionalidad fija `"periodic"` o cambiante) y `robust=TRUE`.
- Comprobar que los resultados de la descomposición respaldan la interpretación gráfica.
- Calcular y graficar los datos desestacionalizados con `seasadj`.
- Pronosticar los datos desestacionalizados con un método no estacional (paseo aleatorio / naive).
- Reestacionalizar para dar pronósticos en la escala original (`stlf` con `method="naive"`, o `forecast(fit, method="naive")`).
- Al construir intervalos de pronóstico, tener presente que se ignora la incertidumbre estacional (presente y futura).
