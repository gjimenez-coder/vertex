# Time series cross-validation (Validación cruzada de series temporales) — Estudio

## Tarjetas de repaso

P: ¿Qué problema tienen la partición tradicional (un solo train/test) y la validación cruzada estándar en series temporales? / R: No respetan el orden temporal; la validación cruzada estándar mezcla observaciones al azar, lo que es inadecuado para series temporales.

P: ¿Cuál es la idea central de la validación cruzada de series temporales? / R: Entrenar con el pasado y evaluar siempre sobre observaciones futuras, avanzando el origen del pronóstico paso a paso.

P: ¿Por qué se llama *rolling forecasting origin*? / R: Porque el origen `(k + i − 1)` en que se basa el pronóstico se desplaza (rueda) hacia adelante en el tiempo.

P: ¿Qué representa `k` en el procedimiento? / R: El número mínimo de observaciones para un conjunto de entrenamiento.

P: ¿Cómo se construye cada iteración de la validación cruzada temporal? / R: Se usan las observaciones `1, 2, ..., k + i − 1` para estimar el modelo, se selecciona `k + i` como prueba y se calcula el error del pronóstico para ese tiempo.

P: ¿Sobre qué rango se repite el procedimiento y qué es `T`? / R: Para `i = 0, 1, ..., T − k`, donde `T` es el número total de observaciones; al final se calcula una medida de precisión sobre todos los errores.

P: ¿A qué equivale asintóticamente minimizar el AIC en datos transversales (*cross-sectional*)? / R: A minimizar el MSE mediante *leave-one-out cross-validation* (Stone, 1977).

P: ¿A qué equivale asintóticamente minimizar el AIC en series temporales? / R: A minimizar el MSE mediante validación cruzada a un paso (Akaike, 1969, 1973).

P: ¿Qué tres modelos se comparan en el ejemplo de ventas farmacéuticas? / R: Un modelo lineal (LM) con tendencia y variables ficticias estacionales sobre logaritmos, un ARIMA sobre logaritmos, y un ETS sobre los datos originales.

P: ¿Qué diseño de validación cruzada usa el ejemplo de la serie `a10`? / R: Fija `k = 48`, pronostica 12 pasos adelante a partir de los datos hasta `k + i − 1` para `i = 1, ..., 156`, y compara el MAE en cada horizonte.

P: ¿En qué consiste la variante de ventana de longitud fija? / R: Mantener el tamaño de la ventana de entrenamiento constante en vez de ampliarla, deslizando también su inicio.

P: ¿Cómo se obtienen pronósticos a un paso sin reajustar el modelo en cada iteración? / R: Se estima el modelo con la ventana corta (`xshort`) y se aplica ese mismo modelo a la ventana larga (`xlong`) para obtener los residuos, que son los errores a un paso.

P: ¿Qué modelo resulta el mejor según el RMSE de entrenamiento en la Lab Session 5b (datos `visitors`)? / R: ETS(M,A,M).

P: ¿Qué relación suele haber entre el RMSE a un paso fuera de muestra y el del entrenamiento? / R: El RMSE a un paso fuera de muestra suele ser mayor que el del entrenamiento.

## Preguntas de autoevaluación

P: ¿Por qué la validación cruzada estándar no sirve para series temporales y qué la reemplaza? / R: Porque reparte las observaciones en grupos sin tener en cuenta el orden temporal; se reemplaza por la validación cruzada de series temporales, que entrena con el pasado y evalúa sobre el futuro (sección "Cross-validation").

P: Describe paso a paso una iteración del *rolling forecasting origin*. / R: Con un mínimo `k`, se estima el modelo con las observaciones `1, ..., k + i − 1`, se pronostica y mide el error en `k + i`, y se repite para `i = 0, ..., T − k`, promediando después los errores (sección "Cross-validation").

P: ¿Qué conexión teórica existe entre AIC y validación cruzada, y en qué se diferencia según el tipo de datos? / R: Minimizar el AIC equivale asintóticamente a minimizar el MSE; en datos transversales vía *leave-one-out* (Stone, 1977) y en series temporales vía validación cruzada a un paso (Akaike, 1969, 1973) (sección "Cross-validation").

P: En el ejemplo de antidiabéticos, ¿qué hacen `xshort` y `xnext` en cada paso del bucle y cómo se obtiene el MAE por horizonte? / R: `xshort` amplía la ventana de entrenamiento y `xnext` toma los 12 meses siguientes como prueba; se promedian los errores absolutos por columna con `colMeans` para obtener el MAE por horizonte (sección "Ejemplo: ventas farmacéuticas").

P: ¿Cuáles son las dos variantes de la validación cruzada temporal descritas y en qué se diferencian del esquema básico? / R: La ventana de entrenamiento de longitud fija (deslizando también su inicio) y los pronósticos a un paso (aplicando el modelo ajustado a la ventana larga para obtener residuos), en lugar de ampliar la ventana y reajustar en cada iteración (sección "Variantes de la validación cruzada de series temporales").

P: En la Lab Session 5b, ¿cuál es el propósito de comparar el RMSE de (a) con el de (b)? / R: Comprobar cuánto mayor es el RMSE a un paso fuera de muestra, obtenido por validación cruzada temporal empezando con cuatro años de entrenamiento, frente al RMSE de entrenamiento del mejor modelo ETS(M,A,M) (sección "Lab Session 5b").

P: ¿Por qué es más realista permitir que `ets` reseleccione el modelo en cada iteración? / R: Porque en la práctica no se sabe de antemano que el mejor modelo sobre todos los datos es ETS(M,A,M); reseleccionar en cada paso refleja esa incertidumbre y permite ver si cambia mucho el resultado (sección "Lab Session 5b").

P: ¿Cómo pueden sesgar la comparación de RMSE los valores faltantes en el vector de errores `e`? / R: Los valores faltantes (NA) en `e` afectan la comparación entre los RMSE de (a) y (b), por lo que se pide reflexionar sobre ese efecto al graficar `e` y observar las varianzas de los errores (sección "Lab Session 5b").

## Checklist

- Fijar un tamaño mínimo de entrenamiento `k` y estimar el modelo solo con observaciones hasta `k + i − 1`, evaluando sobre el futuro.
- Repetir el ajuste y la medición del error para `i = 0, 1, ..., T − k` y promediar los errores.
- Para comparar modelos (LM, ARIMA, ETS) por horizonte, calcular el MAE por columna con `colMeans` y graficarlo frente al horizonte (1 a 12 meses).
- Al replicar el ejemplo de `a10`, usar `k = 48`, pronosticar 12 pasos adelante y recorrer `i = 1, ..., 156`.
- Si se usa ventana de longitud fija, deslizar también el inicio con `window(a10, start=i+1/12, end=1995+(5+i)/12)`.
- Para pronósticos a un paso, ajustar con `xshort` y aplicar el mismo modelo a `xlong` (p. ej. `Arima(xlong, model=fit2)` o `ets(xlong, model=fit3)`) y tomar los residuos como errores.
- En la Lab Session 5b, cargar el paquete con `library(fpp)` antes de los ejercicios.
- Construir `train <- ts(visitors[1:i], freq=12)` (con `ts`) y comprobar qué pasaría sin `ts`; graficar `e` para observar las varianzas de los errores.
- Rehacer el análisis dejando que `ets` seleccione el modelo en cada iteración y comparar ese RMSE con el de (b).
- Verificar si la selección de `ets()` por AICc coincide con el modelo elegido por validación cruzada y decidir qué modelo se usaría en la práctica.
