# Dynamic regression models (Modelos de regresión dinámica) — Estudio

## Tarjetas de repaso

P: ¿Qué extiende la regresión con errores ARIMA respecto a la regresión clásica? / R: Permite que los errores estén autocorrelacionados en lugar de ser ruido blanco, combinando una parte de regresión (variables explicativas) con una parte ARIMA que modela la estructura temporal de los errores.

P: ¿Cuál es la distinción clave entre `nt` y `et`? / R: `nt` es el error del modelo de regresión, que puede estar autocorrelacionado; `et` es el ruido blanco del modelo ARIMA de esos errores. Solo `et` se asume ruido blanco.

P: ¿Qué relación tienen `nt` y `et` en la regresión ordinaria? / R: En la regresión ordinaria `nt` se asume ruido blanco y por tanto `nt = et`.

P: ¿Qué problemas trae minimizar ∑nt² (regresión ordinaria)? / R: Los coeficientes dejan de ser óptimos, las pruebas estadísticas son incorrectas, los p-values quedan demasiado pequeños ("spurious regression") y el AIC es engañoso.

P: ¿Por qué se minimiza ∑et² en su lugar? / R: Evita esos problemas; además, maximizar la verosimilitud es similar a minimizar ∑et².

P: ¿Qué condición deben cumplir todas las variables del modelo y cómo se logra? / R: Deben ser estacionarias; si alguna no lo es, se diferencian las variables hasta que todas lo sean, aplicando la misma diferenciación a todas cuando corresponda para preservar la interpretabilidad.

P: ¿Cuál es el problema circular en la selección de la estructura de error? / R: Para identificar el ARIMA de los errores se necesita `nt`, pero `nt` requiere conocer los `β`, y estimar los `β` requiere especificar la estructura ARIMA; se rompe empezando con un modelo proxy de los errores.

P: ¿Qué modelo proxy de errores se usa al iniciar el procedimiento? / R: Errores AR(2) para datos no estacionales o ARIMA(2,0,0)(1,0,0)m para estacionales.

P: ¿Cómo se seleccionan los predictores del modelo final? / R: Se calcula el AIC del modelo final, se repite el procedimiento para todos los subconjuntos de predictores considerados y se elige el de menor AIC.

P: ¿Cómo se pronostica una regresión con errores ARIMA? / R: Se pronostica por separado la parte de regresión y la parte ARIMA, y luego se combinan.

P: ¿En qué se diferencian la tendencia determinista y la estocástica? / R: La determinista tiene `nt` ARMA; la estocástica tiene `nt` ARIMA con `d ≥ 1`. Los pronósticos puntuales son casi idénticos, pero la estocástica da intervalos mucho más anchos porque los errores son no estacionarios.

P: ¿Cómo se maneja la estacionalidad periódica? / R: Con pares de términos de Fourier `sk(t) = sin(2πkt/m)` y `ck(t) = cos(2πkt/m)`, siendo `nt` un ARIMA no estacional; el número K se elige minimizando el AICc.

P: ¿Qué es la función de transferencia `ν(B)`? / R: Describe cómo el cambio en `xt` se transfiere a `yt` mediante valores presentes y pasados del predictor; `x` puede influir en `y`, pero `y` no puede influir en `x`.

P: ¿Qué son las funciones de transferencia racionales? / R: A partir de `yt = a + ν(B)xt + nt` con `nt` ARMA, se tiene `nt = ψ(B)et`; los ARMA son aproximaciones racionales y `ν(B)` también puede sustituirse por una aproximación racional. No hay paquete de R para el enfoque general.

## Preguntas de autoevaluación

P: ¿Por qué es incorrecto aplicar t-tests estándar a una regresión cuyos errores están autocorrelacionados? / R: Porque al minimizar ∑nt² se ignora información, las pruebas estadísticas son incorrectas y los p-values suelen quedar demasiado pequeños, dando lugar a regresión espuria. (Sección 10.1)

P: ¿Cuáles son los pasos del procedimiento iterativo para ajustar una regresión con errores ARIMA? / R: (1) Comprobar estacionariedad y diferenciar si hace falta; (2) ajustar la regresión con errores AR(2) o ARIMA(2,0,0)(1,0,0)m; (3) calcular `nt` e identificar un ARMA para ellos; (4) reajustar el modelo completo con ese ARMA; (5) verificar que `et` parece ruido blanco. (Sección 10.1)

P: En el ejemplo de consumo e ingreso en EE. UU., ¿qué estructura de error resultó óptima y cómo se validó? / R: ARIMA(1,0,2), por tener el menor AICc (coincide con `auto.arima`, AIC=300.54, AICc=301.08); se validó con el test de Ljung-Box (p-value=0.4673, compatible con ruido blanco). (Sección 10.2)

P: ¿Por qué hay que ser cauto al pronosticar con tendencias deterministas demasiado lejos? / R: Porque los pronósticos puntuales con tendencia determinista y estocástica son casi idénticos, pero una tendencia determinista impone una forma fija que puede no sostenerse en horizontes largos; los intervalos de la estocástica reflejan mejor la incertidumbre al ser mucho más anchos. (Sección 10.4)

P: ¿Cómo se elige el número de términos de Fourier K? / R: Toda función periódica puede aproximarse con sumas de senos y cosenos para K suficientemente grande; K se elige minimizando el AICc. (Sección 10.5)

P: ¿Qué motiva usar un modelo de regresión dinámica con predictores rezagados? / R: Que un cambio en `xt` no siempre afecta a `yt` de forma instantánea (p. ej. ventas/publicidad, caudal/lluvia), por lo que el modelo incluye valores presentes y pasados del predictor mediante la función de transferencia. (Sección 10.6)

P: ¿Cómo se reescribe una regresión con error ARIMA como regresión con error ARMA? / R: Diferenciando todas las variables con el mismo operador de diferenciación del modelo ARIMA; así `φ(B)(1−B)d Nt = θ(B)et` pasa a `y′t = β1x′1,t + ··· + βkx′k,t + n′t` con `φ(B)Nt = θ(B)et` y `y′t = (1−B)d yt`. (Sección 10.1)

## Puntos a dominar

- Distinguir siempre `nt` (error de regresión, posiblemente autocorrelacionado) de `et` (ruido blanco del ARIMA).
- Saber por qué minimizar ∑et² (verosimilitud) es preferible a minimizar ∑nt² (evita la regresión espuria).
- Comprobar estacionariedad de todas las variables y diferenciar con el mismo operador para preservar interpretabilidad.
- Aplicar el procedimiento iterativo partiendo del proxy AR(2) o ARIMA(2,0,0)(1,0,0)m y comparar con AIC.
- Pronosticar por separado la parte de regresión y la ARIMA, combinándolas, y tener los regresores futuros.
- Diferenciar tendencia determinista frente a estocástica y su efecto sobre la anchura de los intervalos.
- Modelar estacionalidad periódica con términos de Fourier eligiendo K por AICc.
- Entender la función de transferencia `ν(B)` y la unidireccionalidad `x → y` sin retroalimentación.
