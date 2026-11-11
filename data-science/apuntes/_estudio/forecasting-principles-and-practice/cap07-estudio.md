# Non-seasonal ARIMA models (Modelos ARIMA no estacionales) — Estudio

## Tarjetas de repaso

P: ¿Qué representa cada orden en un modelo ARIMA(p, d, q)? / R: `p` es el orden de la parte autorregresiva, `d` el grado de primeras diferencias y `q` el orden de la parte de medias móviles.

P: ¿Qué es un modelo autorregresivo (AR)? / R: Expresa el valor actual como combinación lineal de valores pasados de la propia serie: `yt = c + φ1·yt−1 + ··· + φp·yt−p + et`; es una regresión múltiple con valores rezagados como predictores.

P: En un AR(1) `yt = c + φ1·yt−1 + et`, ¿qué significa `φ1 = 1` y `c = 0`? / R: Equivale a un random walk (RW). Si además `c ≠ 0`, es un random walk con deriva; si `φ1 = 0`, es ruido blanco; si `φ1 < 0`, la serie tiende a oscilar entre valores positivos y negativos.

P: ¿Qué es un modelo de medias móviles (MA)? / R: Usa errores pasados como predictores: `yt = c + et + θ1·et−1 + ··· + θq·et−q`. No debe confundirse con el suavizado por medias móviles.

P: ¿Qué es la invertibilidad de un modelo MA? / R: Un MA(q) es invertible si, imponiendo restricciones a los parámetros, puede escribirse como un AR(∞); equivale a la pronosticabilidad de un modelo ETS.

P: ¿Cuál es la condición general de estacionariedad (AR) e invertibilidad (MA)? / R: Que las raíces complejas de los polinomios correspondientes (`1 − φ1z − ···` para AR y `1 + θ1z + ···` para MA) queden fuera del círculo unitario en el plano complejo; el software de estimación las garantiza.

P: ¿Cómo se escribe un ARIMA(1,1,1) en notación de retardo (backshift)? / R: `(1−φ1B)(1−B)·yt = c + (1+θ1B)·et`, que combina un AR(1), una primera diferencia y un MA(1).

P: ¿Qué casos especiales de ARIMA conviene memorizar? / R: Ruido blanco = ARIMA(0,0,0); random walk = ARIMA(0,1,0) sin constante; random walk con deriva = ARIMA(0,1,0) con constante; AR(p) = ARIMA(p,0,0); MA(q) = ARIMA(0,0,q).

P: ¿Qué mide la autocorrelación parcial (PACF) `αk`? / R: La relación entre `yt` e `yt−k` eliminando el efecto de los retardos intermedios; equivale al coeficiente `bk` de la regresión `yt = c + φ1·yt−1 + ··· + φk·yt−k`, con `α1 = ρ1`.

P: ¿Cómo se identifica un ARIMA(p,d,0) con ACF/PACF? / R: La ACF decae exponencialmente o es sinusoidal y hay un pico significativo en el retardo `p` de la PACF, sin nada más allá.

P: ¿Cómo se identifica un ARIMA(0,d,q) con ACF/PACF? / R: La PACF decae exponencialmente o es sinusoidal y hay un pico significativo en el retardo `q` de la ACF, sin nada más allá.

P: ¿Qué criterio de información se prefiere y cómo se usa? / R: Se eligen buenos modelos minimizando el criterio; se prefiere el AICc (con AIC y BIC como alternativas), donde `k = 1` si `c ≠ 0` y `k = 0` si `c = 0`.

P: ¿Qué hace el algoritmo `auto.arima()`? / R: Selecciona `d` con tests de raíz unitaria, elige `p, q` minimizando el AICc y recorre el espacio de modelos con búsqueda stepwise a partir de cuatro modelos iniciales (ARIMA(2,d,2), (0,d,0), (1,d,0), (0,d,1)).

P: ¿Cómo se calculan los pronósticos puntuales de un ARIMA? / R: Se reordena la ecuación con `yt` a la izquierda, se reemplaza `t` por `T+h`, se sustituyen observaciones futuras por pronósticos, errores futuros por cero y errores pasados por residuos; se hace recursivamente desde `h = 1`.

P: ¿Por qué los intervalos de pronóstico ARIMA tienden a ser demasiado estrechos? / R: Porque no incorporan la incertidumbre de los parámetros, suponen que los patrones históricos no cambian y que los errores futuros no están correlacionados.

## Preguntas de autoevaluación

P: ¿Qué condición de estacionariedad aplica a un AR de orden 2? / R: `−1 < φ2 < 1`, `φ2 + φ1 < 1` y `φ2 − φ1 < 1`. (Sección «Modelos autorregresivos (AR)»)

P: ¿Cómo influyen `c` y `d` en el comportamiento de los pronósticos a largo plazo? / R: Con `c = 0`: `d = 0` tienden a cero, `d = 1` a una constante no nula, `d = 2` siguen una recta. Con `c ≠ 0`: `d = 0` a la media, `d = 1` siguen una recta, `d = 2` tendencia cuadrática; además, cuanto mayor `d`, más rápido crecen los intervalos. (Sección «Modelos ARIMA»)

P: ¿Qué relación existe entre MLE y la minimización de errores al estimar un ARIMA? / R: La estimación por máxima verosimilitud (MLE) es similar a minimizar `∑et²`; `Arima()` permite CLS o MLE y ambos usan optimización no lineal, por lo que distintos softwares pueden dar estimaciones distintas. (Sección «Estimación y criterios de información»)

P: ¿Qué pasos del procedimiento de modelado cubre el algoritmo automático y cuáles no? / R: `auto.arima()` solo cubre los pasos 3–5 (diferenciar, examinar ACF/PACF y comparar modelos por AICc); graficar datos, transformar, diagnosticar residuos y pronosticar corren por cuenta del analista. (Sección «Modelado ARIMA en R»)

P: ¿Qué se revisa en los residuos antes de pronosticar y con qué herramienta? / R: Se examina la ACF de los residuos y se aplica el test portmanteau de Ljung-Box; si no parecen ruido blanco, se modifica el modelo. (Sección «Modelado ARIMA en R»)

P: ¿Qué se necesita para que un ARIMA muestre comportamiento cíclico en los pronósticos? / R: Se requiere `p > 2` (o `p = 2` con `φ1² + 4φ2 < 0`). (Sección «Modelos ARIMA»)

P: ¿Cómo se construye un intervalo de pronóstico al 95 % y cuánto vale la varianza a un paso? / R: `ŷT+h|T ± 1.96·√vT+h|T`; para todo ARIMA, `vT+1|T = σ̂²`, y en ARIMA(0,0,q), `vT+h|T = σ̂²·(1 + ∑θi²)`. (Sección «Pronósticos»)

P: ¿Qué modelo eligió `auto.arima` para el consumo personal de EE. UU. y cuál fue su ecuación? / R: Un ARIMA(0,0,3) con media no nula: `yt = 0.756 + et + 0.254·et−1 + 0.226·et−2 + 0.269·et−3`. (Sección «Modelos ARIMA», PDF p. 74)

## Checklist

- [ ] Graficar los datos e identificar observaciones inusuales.
- [ ] Si hace falta, aplicar una transformación Box-Cox para estabilizar la varianza.
- [ ] Diferenciar hasta lograr estacionariedad, usando tests de raíz unitaria si hay dudas.
- [ ] Examinar ACF/PACF de los datos diferenciados para decidir entre AR(p) o MA(q).
- [ ] Probar modelos candidatos y buscar el mejor minimizando el AICc.
- [ ] Revisar los residuos con la ACF y el test de Ljung-Box (`Box.test(..., type="Ljung")`).
- [ ] Modificar el modelo si los residuos no parecen ruido blanco; repetir el diagnóstico.
- [ ] Cuando los residuos parezcan ruido blanco, calcular los pronósticos con `forecast()`.
- [ ] Cargar el paquete con `library(fpp)` antes de empezar las sesiones de laboratorio.
- [ ] Comparar el modelo ARIMA elegido con `ets()` sin transformación y valorar si los pronósticos son razonables.
