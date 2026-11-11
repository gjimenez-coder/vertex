# Forecasting: Principles and Practice — Rob J. Hyndman (material de taller, University of Western Australia, septiembre 2014)
## Capítulo 6 — Making time series stationary (Cómo hacer estacionaria una serie temporal)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (material de taller con laboratorio en R) y las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo explica cómo preparar una serie temporal para el modelado ARIMA, cuyo requisito previo es que la serie sea estacionaria. Para lograrlo se combinan dos herramientas: las transformaciones (estabilizan la varianza) y las diferenciaciones (estabilizan la media). La tesis central es que una serie estacionaria no tiene tendencia ni estacionalidad predecible a largo plazo, y que mediante transformaciones de Box-Cox y diferencias ordinarias o estacionales se puede llevar casi cualquier serie a ese estado.

Sales sabiendo cuándo y cómo aplicar logaritmos o Box-Cox, cómo diferenciar una vez, dos veces o estacionalmente, y cómo decidir el orden de diferenciación con pruebas de raíz unitaria (ADF, KPSS) o con las funciones automáticas de R (`ndiffs`, `nsdiffs`, `BoxCox.lambda`). También aprendes la notación de retardo (backshift) que compacta estas operaciones y prepara el terreno para los modelos ARIMA de los capítulos siguientes.

## 6.1 Transformaciones

Si la serie muestra distinta variación en distintos niveles, conviene transformarla. Denotando las observaciones originales como $y_1,\dots,y_n$ y las transformadas como $w_1,\dots,w_n$, las opciones habituales, de menor a mayor fuerza, son: raíz cuadrada ($w_t=\sqrt{y_t}$), raíz cúbica ($w_t=\sqrt[3]{y_t}$) y logaritmo ($w_t=\log(y_t)$). Los logaritmos son especialmente útiles porque son más interpretables: los cambios en un valor logarítmico son cambios relativos (porcentuales) en la escala original.

Estas transformaciones son casos cercanos de la familia de Box-Cox:

$$w_t = \begin{cases} \log(y_t), & \lambda = 0; \\ (y_t^\lambda - 1)/\lambda, & \lambda \neq 0. \end{cases}$$

Casos particulares: $\lambda=1$ (sin transformación sustantiva), $\lambda=\tfrac12$ (raíz cuadrada más transformación lineal), $\lambda=0$ (logaritmo natural), $\lambda=-1$ (inversa más 1). Para $\lambda$ cercano a cero, $y_t^\lambda$ se comporta como el logaritmo.

Consideraciones prácticas:

- Si algún $y_t=0$, debe cumplirse $\lambda>0$; si algún $y_t<0$, no hay transformación potencia posible salvo que se sume una constante a todos los valores.
- Conviene elegir un valor sencillo de $\lambda$ para facilitar la explicación; los resultados son relativamente insensibles al valor exacto.
- A menudo no hace falta transformación ($\lambda=1$). La transformación suele cambiar poco los pronósticos pero tiene gran efecto sobre los intervalos de predicción (PI).
- $\lambda=0$ es una forma sencilla de forzar que los pronósticos sean positivos.

Hay que invertir la transformación (back-transform) para obtener pronósticos en la escala original:

$$y_t = \begin{cases} \exp(w_t), & \lambda = 0; \\ (\lambda W_t + 1)^{1/\lambda}, & \lambda \neq 0. \end{cases}$$

En R, el valor de $\lambda$ puede estimarse automáticamente con `BoxCox.lambda(elec)`, que intenta equilibrar las fluctuaciones estacionales y la variación aleatoria a lo largo de la serie; conviene comprobar siempre el resultado, ya que un $\lambda$ bajo puede dar intervalos de predicción enormes. Además, una transformación de Box-Cox seguida de un modelo ETS aditivo suele ser mejor que un ETS sin transformación; no tiene sentido combinar Box-Cox con un ETS no aditivo.

## 6.2 Estacionariedad

Definición: si $\{y_t\}$ es una serie estacionaria, entonces para todo $s$ la distribución de $(y_t,\dots,y_{t+s})$ no depende de $t$. En la práctica, una serie estacionaria es aproximadamente horizontal, con varianza constante y sin patrones predecibles a largo plazo.

Las transformaciones ayudan a estabilizar la varianza, pero para el modelado ARIMA también se necesita estabilizar la media. Para identificar series no estacionarias:

- El gráfico temporal (time plot).
- La ACF de datos estacionarios cae a cero con relativa rapidez.
- La ACF de datos no estacionarios decrece lentamente.
- En datos no estacionarios, el valor de $r_1$ suele ser grande y positivo.

El índice Dow-Jones ilustra una serie no estacionaria: su gráfico muestra tendencia y su ACF decae despacio.

## 6.3 Diferenciación ordinaria

La diferenciación ayuda a estabilizar la media. La serie diferenciada es el cambio entre cada observación y la anterior:

$$y'_t = y_t - y_{t-1}.$$

Tendrá solo $T-1$ valores, porque no se puede calcular $y'_1$ para la primera observación.

En el ejemplo del Dow-Jones, las diferencias son los cambios diarios y la serie resultante parece ruido blanco: no hay autocorrelaciones fuera de los límites del 95% y el estadístico $Q^*$ de Ljung-Box tiene un p-valor de 0.153 para $h=10$. Conclusión: el cambio diario del Dow-Jones es esencialmente una cantidad aleatoria no correlacionada con los días previos.

Esto sugiere el modelo de camino aleatorio (random walk):

$$y_t - y_{t-1} = e_t \quad\text{o}\quad y_t = y_{t-1} + e_t.$$

Es un modelo muy usado para datos no estacionarios y está detrás del método ingenuo (naïve). Los caminos aleatorios suelen tener periodos largos de aparente tendencia al alza o a la baja y cambios súbitos e impredecibles de dirección. El random walk con deriva (drift) añade una constante $c$, el cambio medio entre observaciones consecutivas, y está detrás del método de deriva:

$$y_t - y_{t-1} = c + e_t.$$

Ocasionalmente los datos diferenciados aún no parecen estacionarios y hay que diferenciar una segunda vez:

$$y''_t = y'_t - y'_{t-1} = y_t - 2y_{t-1} + y_{t-2}.$$

$y''_t$ tendrá $T-2$ valores. En la práctica casi nunca es necesario ir más allá de las diferencias de segundo orden.

## 6.4 Diferenciación estacional

Una diferencia estacional es la diferencia entre una observación y la correspondiente del año anterior:

$$y'_t = y_t - y_{t-m},$$

donde $m$ es el número de estaciones (por ejemplo, $m=12$ para datos mensuales). En el ejemplo de las ventas de antidiabéticos, la serie diferenciada estacionalmente queda más cerca de ser estacionaria, y la no estacionariedad restante se elimina con una diferencia ordinaria adicional. Si $y'_t = y_t - y_{t-12}$, la serie doblemente diferenciada es:

$$y^*_t = y'_t - y'_{t-1} = y_t - y_{t-1} - y_{t-12} + y_{t-13}.$$

Cuando se aplican diferencia estacional y primera diferencia, no importa cuál se haga primero: el resultado es el mismo. Si la estacionalidad es fuerte, se recomienda diferenciar primero estacionalmente, porque a veces la serie resultante ya es estacionaria y no hace falta la primera diferencia.

Es importante que las diferencias sean interpretables: las primeras diferencias son el cambio de una observación a la siguiente; las estacionales, el cambio de un año al siguiente. Tomar, por ejemplo, diferencias de lag 3 en datos anuales produce un modelo que no puede interpretarse de forma sensata.

## 6.5 Pruebas de raíz unitaria

Son pruebas estadísticas para determinar el orden de diferenciación requerido:

1. Prueba de Dickey-Fuller aumentada (ADF): la hipótesis nula es que los datos son no estacionarios y no estacionales.
2. Prueba KPSS (Kwiatkowski-Phillips-Schmidt-Shin): la hipótesis nula es que los datos son estacionarios y no estacionales.
3. Existen otras pruebas para datos estacionales.

La prueba de Dickey-Fuller estima la regresión:

$$y'_t = \phi y_{t-1} + b_1 y'_{t-1} + b_2 y'_{t-2} + \cdots + b_k y'_{t-k},$$

donde $y'_t = y_t - y_{t-1}$. El número de términos retardados $k$ suele fijarse en torno a 3. Si la serie original necesita diferenciación, $\hat\phi \approx 0$; si ya es estacionaria, $\hat\phi < 0$. En R se usa `adf.test()` (con $k=\lfloor T-1 \rfloor^{1/3}$ por defecto). Para el Dow-Jones, `adf.test(dj)` da un p-valor de 0.5816, por lo que no se rechaza la no estacionariedad.

Para decidir cuántas diferencias tomar, R ofrece `ndiffs(x)` (diferencias ordinarias) y `nsdiffs(x)` (estacionales). El flujo automático aplica primero las estacionales y luego las ordinarias:

```r
ns <- nsdiffs(x)
if(ns > 0) xstar <- diff(x, lag=frequency(x), differences=ns) else xstar <- x
nd <- ndiffs(xstar)
if(nd > 0) xstar <- diff(xstar, differences=nd)
```

## 6.6 Notación de retardo (backshift)

El operador de retardo hacia atrás $B$ desplaza los datos un periodo: $By_t = y_{t-1}$. Dos aplicaciones desplazan dos periodos: $B(By_t) = B^2 y_t = y_{t-2}$. Para datos mensuales, $B^{12} y_t = y_{t-12}$ (el mismo mes del año anterior).

Esta notación describe la diferenciación de forma compacta. Una primera diferencia es:

$$y'_t = y_t - y_{t-1} = (1-B)y_t,$$

es decir, se representa por $(1-B)$. Una diferencia de segundo orden es:

$$y''_t = y_t - 2y_{t-1} + y_{t-2} = (1-B)^2 y_t.$$

Cuidado: la diferencia de segundo orden $(1-B)^2$ no es lo mismo que una "segunda diferencia", que sería $1-B^2$. En general, una diferencia de orden $d$ se escribe $(1-B)^d y_t$. Una diferencia estacional seguida de una primera diferencia es $(1-B)(1-B^m)y_t$. Como los términos se multiplican, el efecto combinado se ve directamente:

$$(1-B)(1-B^m)y_t = y_t - y_{t-1} - y_{t-m} + y_{t-m-1},$$

que para $m=12$ coincide con el resultado obtenido antes.

## 6.7 Laboratorio (Sesión 6)

Tras cargar el paquete con `library(fpp)`, los ejercicios piden: hallar una transformación de Box-Cox y un orden de diferenciación adecuados para varias series (`usnetelec`, `usgdp`, `mcopper`, `enplanements`, `visitors`); razonar por qué Box-Cox no ayuda con los datos `cangas`; y repetir el proceso con una serie de ventas minoristas. Con esos datos se comparan cuatro enfoques —un ETS; un ETS aditivo sobre la serie transformada por Box-Cox; un modelo STL sobre la serie transformada seguido de ETS sobre los datos desestacionalizados; y un método ingenuo estacional sobre la serie transformada— examinando el diagnóstico de residuos y los pronósticos sobre un conjunto de prueba de los dos últimos años, y finalmente mediante validación cruzada de series temporales.

## Ideas clave

- El modelado ARIMA exige series estacionarias: horizontales, con varianza constante y sin patrones predecibles a largo plazo.
- Las transformaciones (raíz, log, Box-Cox) estabilizan la varianza; las diferencias estabilizan la media.
- Box-Cox unifica las transformaciones vía $\lambda$; $\lambda=0$ es el log y fuerza pronósticos positivos. Elegir un $\lambda$ sencillo y comprobarlo.
- Una ACF que decae lentamente y un $r_1$ grande y positivo indican no estacionariedad.
- La primera diferencia $y_t - y_{t-1}$ da el modelo de camino aleatorio; una segunda diferencia casi nunca es superada en la práctica.
- La diferencia estacional $y_t - y_{t-m}$ se aplica preferentemente antes que la ordinaria cuando la estacionalidad es fuerte.
- Las pruebas ADF (nula: no estacionaria) y KPSS (nula: estacionaria), junto con `ndiffs`/`nsdiffs`, determinan el orden de diferenciación.
- El operador backshift $B$ expresa diferencias como $(1-B)^d$ y $(1-B^m)$, cuyo producto da el efecto combinado; $(1-B)^2 \neq 1-B^2$.
