# Making time series stationary (Cómo hacer estacionaria una serie temporal) — Estudio

## Tarjetas de repaso

P: ¿Qué requisito previo impone el modelado ARIMA sobre la serie temporal?
R: Que la serie sea estacionaria.

P: ¿Qué dos herramientas se combinan para hacer estacionaria una serie y qué estabiliza cada una?
R: Las transformaciones (estabilizan la varianza) y las diferenciaciones (estabilizan la media).

P: ¿Qué caracteriza en la práctica a una serie estacionaria?
R: Es aproximadamente horizontal, con varianza constante y sin patrones predecibles a largo plazo (sin tendencia ni estacionalidad predecible).

P: ¿Cuáles son las transformaciones habituales de menor a mayor fuerza?
R: Raíz cuadrada ($w_t=\sqrt{y_t}$), raíz cúbica ($w_t=\sqrt[3]{y_t}$) y logaritmo ($w_t=\log(y_t)$).

P: ¿Por qué son especialmente útiles los logaritmos?
R: Son más interpretables: los cambios en el valor logarítmico son cambios relativos (porcentuales) en la escala original.

P: ¿Cómo se define la transformación de Box-Cox según $\lambda$?
R: $w_t=\log(y_t)$ si $\lambda=0$, y $w_t=(y_t^\lambda-1)/\lambda$ si $\lambda\neq 0$.

P: ¿Qué representan los casos $\lambda=1$, $\lambda=\tfrac12$, $\lambda=0$ y $\lambda=-1$ de Box-Cox?
R: $\lambda=1$ sin transformación sustantiva; $\lambda=\tfrac12$ raíz cuadrada más transformación lineal; $\lambda=0$ logaritmo natural; $\lambda=-1$ inversa más 1.

P: ¿Qué señales en la ACF indican no estacionariedad?
R: Una ACF que decrece lentamente y un valor de $r_1$ grande y positivo.

P: ¿Cómo se define la primera diferencia ordinaria y cuántos valores tiene?
R: $y'_t=y_t-y_{t-1}$; tiene solo $T-1$ valores porque no se puede calcular $y'_1$.

P: ¿Qué modelo sugiere que la serie diferenciada parezca ruido blanco, y cuál es su fórmula?
R: El modelo de camino aleatorio (random walk): $y_t-y_{t-1}=e_t$, o bien $y_t=y_{t-1}+e_t$.

P: ¿Qué añade el random walk con deriva (drift) y qué representa esa constante?
R: Añade una constante $c$, el cambio medio entre observaciones consecutivas: $y_t-y_{t-1}=c+e_t$.

P: ¿Cómo se define una diferencia estacional?
R: $y'_t=y_t-y_{t-m}$, la diferencia entre una observación y la correspondiente $m$ estaciones antes (por ejemplo $m=12$ para datos mensuales).

P: ¿Cuáles son las hipótesis nulas de las pruebas ADF y KPSS?
R: ADF: los datos son no estacionarios y no estacionales. KPSS: los datos son estacionarios y no estacionales.

P: ¿Qué hacen las funciones `ndiffs(x)` y `nsdiffs(x)` de R y en qué orden se aplican?
R: `ndiffs` da el número de diferencias ordinarias y `nsdiffs` el de estacionales; el flujo automático aplica primero las estacionales y luego las ordinarias.

P: ¿Qué expresa el operador de retardo $B$ y cómo se escribe una diferencia de orden $d$?
R: $By_t=y_{t-1}$ (desplaza un periodo); una diferencia de orden $d$ se escribe $(1-B)^d y_t$.

## Preguntas de autoevaluación

P: ¿Por qué la elección exacta de $\lambda$ en Box-Cox no suele ser crítica y qué conviene hacer en la práctica?
R: Los resultados son relativamente insensibles al valor exacto, por lo que conviene elegir un valor sencillo de $\lambda$ para facilitar la explicación. La transformación cambia poco los pronósticos pero tiene gran efecto sobre los intervalos de predicción. (Sección 6.1 Transformaciones)

P: Si una serie tiene valores iguales a 0 o negativos, ¿qué restricciones hay para la transformación potencia?
R: Si algún $y_t=0$, debe cumplirse $\lambda>0$; si algún $y_t<0$, no hay transformación potencia posible salvo que se sume una constante a todos los valores. (Sección 6.1 Transformaciones)

P: En el ejemplo del Dow-Jones, ¿qué conclusión se extrae tras diferenciar una vez?
R: La serie diferenciada parece ruido blanco (sin autocorrelaciones fuera de los límites del 95% y Ljung-Box $Q^*$ con p-valor 0.153 para $h=10$); el cambio diario es una cantidad aleatoria no correlacionada con los días previos. (Sección 6.3 Diferenciación ordinaria)

P: ¿Cuándo hay que diferenciar una segunda vez y hasta qué orden suele llegarse en la práctica?
R: Cuando los datos diferenciados aún no parecen estacionarios se diferencia otra vez ($y''_t=y_t-2y_{t-1}+y_{t-2}$, con $T-2$ valores); en la práctica casi nunca es necesario pasar de segundo orden. (Sección 6.3 Diferenciación ordinaria)

P: Cuando la estacionalidad es fuerte, ¿conviene diferenciar primero de forma estacional u ordinaria, y por qué?
R: Primero estacionalmente, porque a veces la serie resultante ya es estacionaria y no hace falta la primera diferencia; además el orden de aplicación no cambia el resultado combinado. (Sección 6.4 Diferenciación estacional)

P: ¿Qué estima la regresión de Dickey-Fuller y cómo se interpreta $\hat\phi$?
R: Estima $y'_t=\phi y_{t-1}+b_1 y'_{t-1}+\cdots+b_k y'_{t-k}$; si la serie necesita diferenciación $\hat\phi\approx 0$, y si ya es estacionaria $\hat\phi<0$. Para el Dow-Jones el p-valor de 0.5816 no rechaza la no estacionariedad. (Sección 6.5 Pruebas de raíz unitaria)

P: ¿Por qué $(1-B)^2$ no equivale a $1-B^2$?
R: $(1-B)^2 y_t$ es una diferencia de segundo orden ($y_t-2y_{t-1}+y_{t-2}$), mientras que $1-B^2$ sería una "segunda diferencia" distinta; son operaciones diferentes. (Sección 6.6 Notación de retardo)

P: ¿Por qué importa que las diferencias sean interpretables, con un ejemplo de mala práctica?
R: Las primeras diferencias son el cambio de una observación a la siguiente y las estacionales el cambio de un año al siguiente; tomar, por ejemplo, diferencias de lag 3 en datos anuales produce un modelo que no puede interpretarse de forma sensata. (Sección 6.4 Diferenciación estacional)

## Puntos a dominar

- Reconocer cuándo una serie necesita transformación (variación distinta en distintos niveles) y elegir entre raíz, log o Box-Cox, prefiriendo un $\lambda$ sencillo.
- Recordar que $\lambda=0$ (log) fuerza pronósticos positivos y que hay que invertir la transformación (back-transform) para volver a la escala original.
- Identificar no estacionariedad con el gráfico temporal y la ACF (decaimiento lento, $r_1$ grande y positivo).
- Distinguir diferencia ordinaria ($y_t-y_{t-1}$) de diferencia estacional ($y_t-y_{t-m}$) y saber combinarlas.
- Asociar la primera diferencia con el modelo de camino aleatorio y su variante con deriva.
- Aplicar las pruebas ADF y KPSS recordando sus hipótesis nulas opuestas, y apoyarse en `ndiffs`/`nsdiffs` y `BoxCox.lambda`.
- Escribir diferencias con el operador backshift: $(1-B)^d$, $(1-B^m)$ y su producto $(1-B)(1-B^m)y_t=y_t-y_{t-1}-y_{t-m}+y_{t-m-1}$.
- Comprobar siempre el resultado automático de $\lambda$, ya que un valor bajo puede dar intervalos de predicción enormes.
