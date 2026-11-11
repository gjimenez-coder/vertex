# Neural network models (Modelos de redes neuronales) — Estudio

## Tarjetas de repaso

P: ¿A qué equivale una red neuronal sin capas ocultas? / R: A una regresión lineal: una capa de entrada conectada directamente a la de salida.

P: ¿Qué son los "weights" en una red neuronal? / R: Los coeficientes asociados a los predictores (las entradas).

P: ¿Cómo se obtiene la previsión en una red sin capa oculta? / R: Como una combinación lineal de las entradas y los pesos.

P: ¿Cómo se eligen los pesos? / R: Con un algoritmo de aprendizaje (learning algorithm) que minimiza una función de coste (cost function).

P: ¿Qué efecto tiene añadir una capa oculta? / R: Convierte el modelo en no lineal, permitiendo capturar relaciones que la regresión lineal no puede.

P: ¿Qué ocurre en cada nodo de una red feed-forward multicapa? / R: Las entradas se combinan linealmente y el resultado se transforma con una función no lineal antes de salir.

P: ¿Qué función no lineal se cita como ejemplo y qué aporta? / R: La sigmoide s(z)=1/(1+e^{-z}); reduce el efecto de valores extremos, haciendo la red robusta frente a outliers.

P: ¿Por qué se entrena la red varias veces y se promedian los resultados? / R: Porque los pesos parten de valores aleatorios, lo que introduce aleatoriedad en las predicciones.

P: ¿Qué debe especificarse de antemano en la red? / R: El número de capas ocultas y de nodos en cada capa.

P: ¿Qué indica la notación NNAR(p,k)? / R: p entradas rezagadas de la serie y k nodos en la única capa oculta.

P: ¿A qué equivale NNAR(p,0)? / R: A un modelo ARIMA(p,0,0), pero sin las restricciones de estacionariedad.

P: ¿Qué entradas usa la versión estacional NNAR(p,P,k)? / R: (y_{t−1},…,y_{t−p}, y_{t−m}, y_{t−2m},…,y_{t−Pm}) con k neuronas en la capa oculta.

P: ¿A qué equivale NNAR(p,P,0)_m? / R: A un ARIMA(p,0,0)(P,0,0)_m, también sin restricciones de estacionariedad.

P: ¿Qué valor de k usa `nnetar()` por defecto? / R: k = (p + P + 1)/2, redondeado al entero más cercano.

P: ¿Cómo se restringen las previsiones a valores positivos con `nnetar()`? / R: Pasando el argumento `lambda=0`.

## Preguntas de autoevaluación

P: ¿Por qué se dice que la red neuronal es una extensión no lineal de la regresión? / R: Porque sin capa oculta coincide con la regresión lineal, y al añadir una capa oculta con función no lineal pasa a capturar relaciones no lineales. (Sección: "De la regresión lineal a la red con capa oculta")

P: ¿Cómo se combinan las entradas en una neurona oculta antes de aplicar la no linealidad? / R: Linealmente, como z_j = b_j + Σ w_{i,j} x_i, y luego se transforma z_j con una función no lineal. (Sección: "De la regresión lineal a la red con capa oculta")

P: ¿Qué diferencia a un NNAR de un ARIMA equivalente? / R: El NNAR no impone las restricciones de estacionariedad (ni de estacionalidad en la versión estacional) que sí tiene el ARIMA. (Sección: "Modelos NNAR")

P: ¿Cómo selecciona `nnetar()` el valor de p cuando no se especifica? / R: En series no estacionales, p es el número óptimo de rezagos según el AIC para un AR(p) lineal; en estacionales, P=1 y p se elige del modelo lineal óptimo sobre datos desestacionalizados. (Sección: "NNAR en R y el caso de las manchas solares")

P: ¿Por qué interesa predecir la actividad de las manchas solares? / R: Afectan a la propagación de las ondas de radio, así que las empresas de telecomunicaciones quieren anticiparse para planificar posibles problemas. (Sección: "NNAR en R y el caso de las manchas solares")

P: ¿Qué modelo se ajusta en el caso de las manchas solares y a cuántos periodos se prevé? / R: Un NNAR(9) mediante `nnetar(sunspotarea)`, con previsión a 20 periodos (h=20). (Sección: "NNAR en R y el caso de las manchas solares")

P: ¿Qué papel juega la función sigmoide frente a datos con valores extremos? / R: Reduce el efecto de las entradas extremas, aportando robustez frente a outliers. (Sección: "De la regresión lineal a la red con capa oculta")

## Puntos a dominar

- Distinguir una red sin capa oculta (equivalente a regresión lineal) de una con capa oculta (modelo no lineal).
- Explicar el flujo en un nodo: combinación lineal de entradas seguida de una función no lineal (p. ej. sigmoide).
- Relacionar pesos, función de coste y algoritmo de aprendizaje, y por qué se promedian varios entrenamientos por la aleatoriedad inicial.
- Interpretar la notación NNAR(p,k) y la estacional NNAR(p,P,k)_m, y sus equivalencias con ARIMA sin restricciones.
- Conocer las reglas por defecto de `nnetar()` para p, P y k.
- Reproducir el ajuste y la previsión del caso de las manchas solares, incluyendo `lambda=0` para forzar valores positivos.
