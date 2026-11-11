# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 10 — Dynamic regression models (Modelos de regresión dinámica)

> Nota de extracción: texto extraído de la capa de texto del PDF (material de taller con sesiones de laboratorio en R); las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo extiende la regresión clásica para permitir que los errores estén autocorrelacionados en lugar de ser ruido blanco. La idea central es combinar una parte de regresión (variables explicativas) con una parte ARIMA que modela la estructura temporal de los errores. Así se obtienen coeficientes y pruebas estadísticas válidas, evitando la "regresión espuria".

Sales sabiendo cómo plantear una regresión con errores ARIMA, por qué hay que trabajar con variables estacionarias, cómo elegir la estructura de error mediante un procedimiento iterativo y cómo pronosticar con estos modelos. También se cubren tendencias deterministas frente a estocásticas, estacionalidad periódica con términos de Fourier, y modelos de regresión dinámica con variables explicativas rezagadas (funciones de transferencia).

La distinción clave que recorre todo el capítulo es entre `nt` (el error del modelo de regresión, que puede estar autocorrelacionado) y `et` (el ruido blanco del modelo ARIMA de esos errores). Solo `et` se asume ruido blanco.

## El ejemplo que recorre el capítulo

No hay un único hilo conductor, sino varios casos ilustrativos: consumo e ingreso personal en EE. UU., visitantes internacionales a Australia, muertes accidentales en EE. UU. y presupuestos de seguros frente a publicidad en TV.

## 10.1 Regresión con errores ARIMA

El modelo base es `yt = β0 + β1x1,t + ··· + βkxk,t + nt`, donde antes se asumía `et` ruido blanco pero ahora se permite que el error `nt` esté autocorrelacionado. Por ejemplo, con errores ARIMA(1,1,1):

```
yt = β0 + β1x1,t + ··· + βkxk,t + nt
(1 − φ1B)(1 − B)nt = (1 + θ1B)et
```

donde `et` es ruido blanco. Hay que distinguir `nt` de `et`: en la regresión ordinaria `nt` se asume ruido blanco y por tanto `nt = et`.

Estimación. Minimizar ∑nt² (regresión ordinaria) tiene problemas: los coeficientes estimados dejan de ser óptimos porque se ignora información, las pruebas estadísticas (p. ej. t-tests) son incorrectas, los p-values suelen quedar demasiado pequeños ("spurious regression") y el AIC es engañoso. Minimizar ∑et² evita estos problemas, y maximizar la verosimilitud es similar a minimizar ∑et². Para ello, todas las variables del modelo deben ser estacionarias; si alguna no lo es, los coeficientes pueden salir incorrectos, así que se diferencian las variables hasta que todas sean estacionarias, aplicando la misma diferenciación a todas cuando corresponda.

Cualquier regresión con error ARIMA puede reescribirse como regresión con error ARMA diferenciando todas las variables con el mismo operador de diferenciación que el del modelo ARIMA. Si `φ(B)(1−B)d Nt = θ(B)et`, tras diferenciar queda `y′t = β1x′1,t + ··· + βkx′k,t + n′t` con `φ(B)Nt = θ(B)et` y `y′t = (1−B)d yt`.

Selección del modelo. Para determinar la estructura ARIMA de los errores se necesita `nt`, pero no se puede obtener `nt` sin conocer los `β`, y para estimar los `β` hace falta especificar la estructura ARIMA. La solución es empezar con un modelo "proxy" para los errores. El procedimiento:

1. Comprobar que todas las variables son estacionarias; si no, diferenciar (usando la misma diferenciación en todas donde corresponda, para preservar la interpretabilidad).
2. Ajustar la regresión con errores AR(2) para datos no estacionales o ARIMA(2,0,0)(1,0,0)m para estacionales.
3. Calcular los errores `nt` del modelo ajustado e identificar un modelo ARMA para ellos.
4. Reajustar el modelo completo con el nuevo ARMA para los errores.
5. Verificar que la serie `et` parece ruido blanco.

Selección de predictores. Se calcula el AIC del modelo final, se repite el procedimiento para todos los subconjuntos de predictores considerados y se elige el de menor AIC.

## 10.2 Ejemplo: consumo e ingreso personal en EE. UU.

Con cambios trimestrales de consumo e ingreso no se necesitan transformaciones ni más diferenciación. Un aumento del ingreso no se traduce necesariamente en un aumento instantáneo del consumo (por ejemplo, tras perder el empleo, los gastos tardan meses en ajustarse), pero esto se ignora de momento. Se prueba una regresión simple con AR(2) como modelo proxy de errores:

```r
fit <- Arima(usconsumption[,1], xreg=usconsumption[,2], order=c(2,0,0))
tsdisplay(arima.errors(fit), main="ARIMA errors")
```

Los candidatos incluyen MA(3) y AR(2), pero ARIMA(1,0,2) tiene el menor AICc, así que se reajusta con esos errores. El mismo resultado se obtiene de forma automática con `auto.arima(usconsumption[,1], xreg=usconsumption[,2])`, que da ARIMA(1,0,2) (AIC=300.54, AICc=301.08). El test de Ljung-Box sobre los residuos arroja p-value=0.4673, compatible con ruido blanco. El pronóstico se produce con `forecast(fit2, xreg=..., h=8)`, fijando los regresores futuros.

## 10.3 Pronóstico

Para pronosticar una regresión con errores ARIMA hay que pronosticar por separado la parte de regresión y la parte ARIMA, y combinarlas. Los pronósticos de variables macroeconómicas pueden obtenerse de fuentes como la ABS; otras variables explicativas pueden requerir sus propios modelos. Algunas variables se conocen hacia el futuro (p. ej. el tiempo, variables dummy).

## 10.4 Tendencias estocásticas y deterministas

Tendencia determinista: `yt = β0 + β1t + nt` con `nt` proceso ARMA. Tendencia estocástica: la misma forma pero con `nt` proceso ARIMA con `d ≥ 1`; al diferenciar ambos lados queda `y′t = β1 + n′t` con `n′t` ARMA.

Con los visitantes internacionales a Australia, el enfoque determinista (`auto.arima(austa, d=0, xreg=1:length(austa))`) da ARIMA(2,0,0) con `yt = 0.4173 + 0.1715t + nt`, mientras que el estocástico (`auto.arima(austa, d=1)`) da ARIMA(0,1,0) con drift: `yt − yt−1 = 0.1538 + et`. Los pronósticos puntuales son casi idénticos, pero los intervalos difieren: las tendencias estocásticas tienen intervalos mucho más anchos porque los errores son no estacionarios. Hay que ser cauto al pronosticar con tendencias deterministas demasiado lejos.

## 10.5 Estacionalidad periódica

La estacionalidad periódica se maneja con pares de términos de Fourier: `sk(t) = sin(2πkt/m)` y `ck(t) = cos(2πkt/m)`, de modo que `yt = ∑ᴷ [αk sk(t) + βk ck(t)] + nt`, donde `nt` es un ARIMA no estacional. Toda función periódica puede aproximarse con sumas de senos y cosenos para un K suficientemente grande; se elige K minimizando el AICc. Ejemplo con muertes accidentales en EE. UU.:

```r
fit <- auto.arima(USAccDeaths, xreg=fourier(USAccDeaths, 5), seasonal=FALSE)
fc <- forecast(fit, xreg=fourierf(USAccDeaths, 5, 24))
```

## 10.6 Modelos de regresión dinámica

A veces un cambio en `xt` no afecta a `yt` de forma instantánea (ventas/publicidad, caudal/lluvia, tamaño del rebaño/reproductores). Son sistemas dinámicos con entrada `xt` (a menudo un indicador adelantado) y salida `yt`. El modelo incluye valores presentes y pasados del predictor:

```
yt = a + ν0xt + ν1xt−1 + ··· + νkxt−k + nt
   = a + ν(B)xt + nt
```

donde `ν(B)` es la función de transferencia: describe cómo el cambio en `xt` se transfiere a `yt`. `x` puede influir en `y`, pero `y` no puede influir en `x`. En el ejemplo de seguros y anuncios de TV, se construyen rezagos (`AdLag0`, `AdLag1`) y `auto.arima` da ARIMA(3,0,0) con `yt = 2.04 + 1.26xt + 0.16xt−1 + nt`.

## 10.7 Funciones de transferencia racionales

Partiendo de `yt = a + ν(B)xt + nt` con `nt` ARMA, se tiene `nt = θ(B)/φ(B) et = ψ(B)et`, de modo que `yt = a + ν(B)xt + ψ(B)et`. Los modelos ARMA son aproximaciones racionales a funciones de transferencia generales de `et`, y también se puede sustituir `ν(B)` por una aproximación racional. No hay un paquete de R para pronosticar con el enfoque general de funciones de transferencia.

## 10.8 Lab Session 10

Tras cargar `library(fpp)`, los ejercicios piden: (1) desarrollar una regresión dinámica con términos de Fourier para la estacionalidad en la serie de retail elegida, seleccionando el número de términos por AIC, revisar residuos y comparar pronósticos; (2) con el conjunto `motel`, calcular el costo medio por noche, graficarlo contra el CPI, justificar la toma de logaritmos, ajustar una regresión con errores ARIMA y pronosticar el precio medio por habitación a doce meses (requiere pronosticar antes el CPI).

## Ideas clave

- La regresión con errores ARIMA permite errores autocorrelacionados; distinguir `nt` (error de regresión) de `et` (ruido blanco).
- Minimizar ∑et² (verosimilitud) evita la regresión espuria que surge al minimizar ∑nt².
- Todas las variables deben ser estacionarias; diferenciar con el mismo operador preserva la interpretabilidad.
- La estructura de error se identifica iterando desde un modelo proxy AR(2) o ARIMA(2,0,0)(1,0,0)m; se compara con AIC.
- Se pronostica por separado la parte de regresión y la ARIMA, y luego se combinan.
- Tendencias estocásticas producen intervalos de pronóstico más anchos que las deterministas.
- Los términos de Fourier capturan estacionalidad periódica; K se elige minimizando el AICc.
- La función de transferencia `ν(B)` modela efectos rezagados de `x` sobre `y`, sin retroalimentación de `y` hacia `x`.
