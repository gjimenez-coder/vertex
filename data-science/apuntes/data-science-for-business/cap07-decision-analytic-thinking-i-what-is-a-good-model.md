# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 7 — Decision Analytic Thinking I: What Is a Good Model? (Pensamiento analítico para la decisión I: ¿Qué es un buen modelo?)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
El capítulo aborda una pregunta aparentemente simple pero esquiva: ¿cómo saber si un modelo es bueno? La tesis central es que no existe una métrica universalmente correcta; hay que volver siempre a la pregunta de negocio: ¿qué queremos lograr minando los datos? Con frecuencia los data scientists reportan estadísticos sin entender por qué son los correctos, o miden un sustituto sin pensarlo con cuidado (PDF p. 211).

El error más común es confiar en la exactitud (accuracy). Es fácil de calcular pero suele ser demasiado simplista para problemas reales, porque falla con clases desbalanceadas y porque trata todos los errores como igualmente importantes. El capítulo introduce la matriz de confusión para descomponer los tipos de aciertos y errores, y luego el valor esperado (expected value) como marco general para organizar el pensamiento analítico.

Sales sabiendo descomponer el rendimiento de un clasificador con la matriz de confusión, calcular el beneficio esperado combinando probabilidades (de los datos) con costes y beneficios (del conocimiento del negocio), y elegir líneas base (baselines) sensatas contra las cuales comparar. El marco de valor esperado sirve tanto para decidir sobre un caso individual como para evaluar y comparar modelos en agregado.

## El ejemplo que recorre el capítulo
El hilo conductor es MegaTelCo y la predicción de fuga de clientes (churn), junto con un caso de marketing dirigido (targeted marketing). Se usa el marketing dirigido para ilustrar el valor esperado porque el churn esconde una complejidad que se retoma en el Capítulo 11 (PDF p. 219).

## Evaluar clasificadores: la exactitud y sus problemas
Un clasificador toma una instancia de clase desconocida y predice su clase. Para clasificación binaria las clases se llaman "positiva" y "negativa". Por convención, el positivo es el caso digno de atención o alarma (fraude, enfermedad) y suele ser el raro; el negativo es benigno pero más frecuente (PDF p. 212-213).

La exactitud es la proporción de decisiones correctas: `accuracy = decisiones correctas / total de decisiones`, equivalente a `1 − tasa de error`. Es popular porque reduce el rendimiento a un solo número fácil de medir, pero es simplista.

La matriz de confusión es una tabla de contingencia n × n (columnas = clase real, filas = clase predicha). Para dos clases se usan `p`/`n` para las clases reales y `Y`/`N` para las predichas:

| | p | n |
|---|---|---|
| Y | Verdaderos positivos | Falsos positivos |
| N | Falsos negativos | Verdaderos negativos |

La diagonal principal son los aciertos; fuera de ella están los falsos positivos (negativos clasificados como positivos) y los falsos negativos (positivos clasificados como negativos) (PDF p. 213-214).

## Clases desbalanceadas
Cuando una clase es rara, la evaluación por exactitud se rompe. En un dominio con proporción 999:1, la regla "elegir siempre la clase mayoritaria" da 99,9% de exactitud sin aportar nada. Las asimetrías 1:100 son comunes en detección de fraude, y se han reportado mayores que 1:10⁶ (PDF p. 214).

En el ejemplo de churn, con una tasa base de fuga del 10% mensual (ratio positivo:negativo de 1:9), clasificar a todos como negativos da ya un 90% de exactitud. El capítulo contrasta dos modelos evaluados sobre datos distintos: un analista usó una muestra representativa y otro un conjunto balanceado artificialmente, prácticas ambas comunes. Sobre la población balanceada ambos aciertan el 80%, pero operan muy distinto:

Modelo A (confusión sobre 1.000 clientes): Y→(500 churn, 200 no churn), N→(0, 300). Modelo B: Y→(300, 0), N→(200, 500). A predice muchos falsos positivos; B comete el error opuesto. Al aplicarlos a la población real desbalanceada, la exactitud de A cae al 37% y la de B sube al 93% (PDF p. 215-216). La conclusión: la exactitud es lo que no hay que medir; y además no sabemos cuánto importa cada tipo de error.

## Costes y beneficios desiguales
La exactitud no distingue entre falsos positivos y falsos negativos: al contarlos juntos asume que importan igual, lo cual casi nunca es cierto. En diagnóstico médico, un falso positivo (decir que hay cáncer cuando no lo hay) genera molestias y pruebas extra; un falso negativo (no detectar un cáncer real) puede ser mucho más grave. En churn, dar un incentivo a quien igual se va (falso positivo) cuesta distinto que perder a un cliente al que no se le ofreció nada (falso negativo). Lo ideal es estimar el coste o beneficio de cada decisión; agregados, producen una estimación de beneficio esperado (PDF p. 217).

## Generalizar más allá de la clasificación
El principio es general: al aplicar data science hay que volver a preguntar qué es importante y cuál es el objetivo. Con un modelo de recomendación de películas (regresión que predice estrellas de 1 a 5), reportar el error cuadrático medio exige preguntarse: ¿error cuadrático de qué?, ¿es la métrica apropiada y significativa, o solo la que el analista aprendió en clase? (PDF p. 217-218).

## El marco del valor esperado
El valor esperado es una herramienta conceptual amplia que descompone el pensamiento analítico en: (i) la estructura del problema, (ii) los elementos que salen de los datos y (iii) los que se obtienen de otras fuentes (conocimiento del negocio). Su forma general enumera los posibles resultados y promedia sus valores ponderados por su probabilidad (PDF p. 218):

```
EV = p(o1)·v(o1) + p(o2)·v(o2) + p(o3)·v(o3) ...
```

Las probabilidades suelen estimarse de los datos; los valores de negocio suelen venir de fuera.

Para enmarcar el uso del clasificador (decisión individual), en marketing dirigido el beneficio esperado de contactar a un consumidor x es `p_R(x)·v_R + (1 − p_R(x))·v_NR`. Con producto vendido a $200, coste de producto $100 y coste de envío $1: un true positive vale v_R = $99 y un no-respondedor contactado vale v_NR = −$1. Conviene contactar solo si el valor esperado supera cero, lo que se reduce a la regla de decisión `p_R(x) > 0,01`: basta un 1% de probabilidad de respuesta (PDF p. 219-220). Esto explica por qué un umbral "de sentido común" del 50% haría no contactar a nadie.

## Valor esperado para evaluar modelos
Para comparar modelos pasamos de decisiones individuales a colecciones de decisiones. Cada resultado `oi` corresponde a una celda de la matriz de confusión, y su probabilidad se estima dividiendo el conteo por el total: `p(h,a) = count(h,a) / T`. Con la matriz de ejemplo (Y: 56 p, 7 n; N: 5 p, 42 n), T = 110, y las tasas son p(Y,p)=0,51, p(Y,n)=0,06, p(N,p)=0,05, p(N,n)=0,38 (PDF p. 221-222).

Se necesita además una matriz de costes-beneficios con las mismas dimensiones: beneficios en la diagonal (b(Y,p), b(N,n)) y costes fuera (c(Y,n), c(N,p)). Las probabilidades salen de los datos; los costes y beneficios, del análisis del problema de negocio, y a veces solo como rangos aproximados (PDF p. 222-223). Para el marketing dirigido, expresando todo como beneficios: b(Y,p)=99, b(Y,n)=−1, b(N,p)=0, b(N,n)=0 (PDF p. 223-224).

El beneficio esperado se obtiene multiplicando celda a celda probabilidades por costes-beneficios y sumando. Una formulación alternativa factoriza las probabilidades a priori de clase (class priors) p(p) y p(n), separando el desbalanceo de clases del poder predictivo real del modelo. Con la regla `p(x,y) = p(y)·p(x|y)` se obtiene la ecuación 7-2, donde p(Y|p), p(Y|n), etc. son las tasas de verdaderos/falsos positivos de la matriz (PDF p. 224-225).

Con la matriz de ejemplo (P=61, N=49, p(p)=0,55, p(n)=0,45, tp rate=0,92, fp rate=0,14, fn rate=0,08, tn rate=0,86), el beneficio esperado resulta ≈ $50,04 por consumidor: aplicando el modelo y contactando a quienes clasifica como positivos, se espera un beneficio medio de unos $50 (PDF p. 226). Como los priors se factorizan, se pueden comparar modelos aunque uno se evaluara con distribución representativa y otro con balanceada (balanceada ⇒ p(p)=p(n)=0,5), simplemente sustituyendo los priors.

Dos trampas al formular la matriz de costes-beneficios: (1) mantener consistentes los signos (aquí beneficios positivos, costes negativos); (2) no hacer doble conteo poniendo un beneficio en una celda y un coste negativo por lo mismo en otra. Prueba práctica: la mejora `b(Y,p) − b(N,p)` por cambiar la decisión en una instancia debe coincidir con la intuición; si un caso de fraude cuesta $1.000, poner +$1.000 por atrapar y −$1.000 por omitir da $2.000, señal de doble conteo (uno debe ser cero) (PDF p. 227).

Otras métricas son resúmenes de la matriz de confusión (TP, FP, TN, FN): tasa de verdaderos positivos = TP/(TP+FN); precision = TP/(TP+FP); recall = tasa de verdaderos positivos; F-measure = media armónica de precision y recall; sensitivity y specificity; positive predictive value = precision; accuracy = (TP+TN)/(P+N) (PDF p. 227-228).

## Baselines e inversión en datos
Demostrar que un modelo da beneficio no basta: hay que compararlo con una línea base razonable, tanto para el equipo como para los stakeholders. Comparar con un modelo aleatorio establece que hay información que extraer, pero batirlo suele ser fácil y poco informativo. Mejores baselines: el clasificador mayoritario (majority classifier), que siempre predice la clase mayoritaria —si solo el 6% es positivo, un 94% de exactitud no demuestra nada—; para regresión, predecir el promedio (media o mediana) de la población (PDF p. 228-229).

Nate Silver cita dos baselines meteorológicos simples pero no simplistas: la persistencia (mañana igual que hoy) y la climatología (media histórica del día). Un modelo algo más complejo usa una sola variable: el decision stump (árbol con un único nodo interno), que según Holte (1993) da buen rendimiento base. El principio se extiende a las fuentes de datos: comparar un modelo con y sin cada fuente cuantifica su valor y justifica su coste, tratando los datos como un activo en el que invertir. También sirven baselines de conocimiento del dominio, como marcar cuentas con saltos súbitos de uso en fraude, o priorizar clientes por ingresos previos en ventas (PDF p. 229-231).

## Ideas clave
- No existe una métrica universal: siempre hay que volver a qué se quiere lograr con el minado de datos y elegir una métrica acorde al uso real del modelo.
- La exactitud es simplista: falla con clases desbalanceadas (un clasificador trivial puede parecer excelente) y trata todos los errores por igual.
- La matriz de confusión descompone aciertos y errores (TP, FP, FN, TN) y es la base de casi todas las demás métricas.
- Falsos positivos y falsos negativos tienen costes distintos; hay que contarlos por separado y asignarles costes/beneficios.
- El valor esperado es el marco organizador: probabilidades de los datos × costes-beneficios del negocio, sumados sobre la matriz de confusión.
- Factorizar los priors de clase separa el desbalanceo del poder predictivo y permite comparar modelos evaluados con distribuciones distintas.
- Evaluar sobre la población real (no la balanceada) y vigilar signos consistentes y el doble conteo en la matriz de costes-beneficios.
- Comparar siempre contra baselines simples pero no simplistas (clasificador mayoritario, decision stump, reglas del dominio) y contra modelos con distintas fuentes de datos.
