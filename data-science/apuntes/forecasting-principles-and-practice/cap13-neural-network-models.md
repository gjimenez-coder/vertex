# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 13 — Neural network models (Modelos de redes neuronales)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con sesiones de laboratorio en R); las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo introduce las redes neuronales como extensión no lineal de la regresión para la previsión de series temporales. En su versión más simple, una red sin capas ocultas equivale a una regresión lineal: los coeficientes asociados a los predictores se llaman "weights", las previsiones se obtienen como combinación lineal de las entradas y los pesos se seleccionan con un "learning algorithm" que minimiza una "cost function".

Al añadir una capa oculta se obtiene un modelo no lineal. La idea central es una red feed-forward multicapa en la que cada nodo combina linealmente sus entradas y luego aplica una función no lineal, lo que permite capturar relaciones que la regresión lineal no puede. De ahí el capítulo pasa a los modelos NNAR, que usan valores rezagados de la propia serie como entradas, y cierra con un caso aplicado (manchas solares) y el código en R con `nnetar()`.

Al terminar sabrás distinguir una red lineal de una con capa oculta, entender la notación NNAR(p,k) y su versión estacional, relacionar estos modelos con ARIMA, y ajustar un modelo con `nnetar()` en R, incluyendo cómo restringir las previsiones a valores positivos.

## De la regresión lineal a la red con capa oculta

La versión más simple de una red neuronal es una regresión lineal: una capa de entrada conectada directamente a la capa de salida, sin capas ocultas.

- Los coeficientes de los predictores son los "weights".
- La previsión es una combinación lineal de las entradas.
- Los pesos se eligen con un algoritmo de aprendizaje que minimiza una función de coste.

Al introducir una capa oculta el modelo se vuelve no lineal. Es una red feed-forward multicapa: cada capa de nodos recibe entradas de las capas previas. En cada nodo las entradas se combinan de forma lineal y el resultado se transforma con una función no lineal antes de salir.

Las entradas a la neurona oculta *j* se combinan linealmente:

```
z_j = b_j + Σ_{i=1}^{4} w_{i,j} x_i
```

El valor `z_j` se modifica con una función no lineal como la sigmoide:

```
s(z) = 1 / (1 + e^{-z})
```

Esta función reduce el efecto de valores de entrada extremos, haciendo la red algo robusta frente a outliers.

Aspectos del entrenamiento:

- Los pesos empiezan con valores aleatorios y se actualizan con los datos observados.
- Hay un componente de aleatoriedad en las predicciones, por lo que la red suele entrenarse varias veces con distintos puntos de partida aleatorios y los resultados se promedian.
- El número de capas ocultas y de nodos en cada capa debe especificarse de antemano.

## Modelos NNAR

Los valores rezagados de la serie temporal pueden usarse como entradas de una red neuronal. La notación NNAR(p,k) indica *p* entradas rezagadas y *k* nodos en la única capa oculta.

- NNAR(p,0) equivale a un modelo ARIMA(p,0,0) pero sin las restricciones de estacionariedad.
- Versión estacional NNAR(p,P,k): las entradas son (y_{t−1}, y_{t−2}, …, y_{t−p}, y_{t−m}, y_{t−2m}, …, y_{t−Pm}) con *k* neuronas en la capa oculta.
- NNAR(p,P,0)_m equivale a un ARIMA(p,0,0)(P,0,0)_m, también sin restricciones de estacionariedad.

## NNAR en R y el caso de las manchas solares

La función `nnetar()` ajusta un modelo NNAR(p,P,k)_m. Si no se especifican *p* y *P*, se seleccionan automáticamente:

- Para series no estacionales, *p* por defecto es el número óptimo de rezagos (según el AIC) para un modelo lineal AR(p).
- Para series estacionales, los valores por defecto son P = 1 y *p* se elige del modelo lineal óptimo ajustado a los datos desestacionalizados.
- Por defecto k = (p + P + 1)/2, redondeado al entero más cercano.

Como caso hilo conductor se usan las manchas solares (sunspots): regiones magnéticas de la superficie del Sol que aparecen como puntos oscuros. Afectan a la propagación de las ondas de radio, por lo que las empresas de telecomunicaciones quieren predecir su actividad para planificar posibles problemas. Siguen un ciclo de entre 9 y 14 años.

El ajuste de un NNAR(9) para las manchas solares, con previsión a 20 periodos:

```r
fit <- nnetar(sunspotarea)
plot(forecast(fit, h=20))
```

Para restringir las previsiones a valores positivos:

```r
fit <- nnetar(sunspotarea, lambda=0)
plot(forecast(fit, h=20))
```

## Ideas clave

- Una red neuronal sin capa oculta equivale a una regresión lineal: pesos, combinación lineal de entradas y minimización de una función de coste.
- Añadir una capa oculta y una función no lineal (p. ej. sigmoide) convierte la red en un modelo no lineal, robusto frente a valores extremos.
- El entrenamiento parte de pesos aleatorios; por la aleatoriedad, se entrena varias veces y se promedian los resultados.
- El número de capas y nodos ocultos se fija de antemano.
- NNAR(p,k) usa *p* rezagos como entradas y *k* nodos ocultos; NNAR(p,0) equivale a ARIMA(p,0,0) sin restricciones de estacionariedad.
- La versión estacional NNAR(p,P,k) añade rezagos estacionales; NNAR(p,P,0)_m equivale a ARIMA(p,0,0)(P,0,0)_m sin restricciones.
- `nnetar()` selecciona *p*, *P* y *k* automáticamente si no se indican, usando el AIC y los datos desestacionalizados.
- En el caso de las manchas solares se ajusta un NNAR(9); `lambda=0` restringe las previsiones a valores positivos.
