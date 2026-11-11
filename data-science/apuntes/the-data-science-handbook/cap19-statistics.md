# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 19 — Statistics (Estadística)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
El capítulo defiende que buena parte de la data science es, en rigor, un subconjunto de la estadística, y que su separación en disciplinas distintas es más un accidente histórico que una diferencia esencial. Aun así, la mayoría de los data scientists no necesita un conocimiento profundo de estadística la mayor parte del tiempo: lo verdaderamente crucial es el pensamiento crítico que enseña una clase de estadística, es decir, ser cuidadoso y riguroso con los datos y con los supuestos que se hacen.

La tesis central es que la estadística existe para lidiar con restricciones que el data scientist habitualmente no sufre, sobre todo el tamaño de muestra. En Big Data suele sobrar información, de modo que extraer una conclusión puede ser tan simple como mirar un histograma; pero cuando cada dato es caro (un cultivo, una vida humana), hay que recurrir a métodos rigurosos para distinguir un patrón real de una casualidad.

El capítulo recorre los temas clave de la estadística centrándose en las ideas, intuiciones y supuestos, no en las derivaciones. Sales sabiendo cuándo los atajos "rápidos y sucios" fallan, qué son el contraste de hipótesis, el p-valor, la estimación de parámetros, los intervalos de confianza y la estadística bayesiana, además de saber reconocer el momento de aprender la estadística que haga falta sobre la marcha.

## La estadística en perspectiva
Que la mayoría de data scientists no necesite estadística parece absurdo, pero la clave está en las restricciones. La más importante es el tamaño de muestra. La data science nació del Big Data, donde casi por definición hay abundancia de puntos de datos y de features; el reto es parsear bien esa información. En cambio, probar si un fertilizante funciona exige apartar terreno y esperar un ciclo de cultivo por cada dato, y probar un procedimiento médico implica literalmente vidas. La estadística se ocupa de esas situaciones muy restringidas, donde es difícil saber si un patrón es una verdad del mundo o un capricho de los datos, y por eso es apropiadamente quisquillosa con cada detalle.

El data scientist suele tener tanta información que puede permitirse ser despreocupado, pero no siempre; uno de los peores delitos es ser "fast-and-loose" en una situación que exige rigor. Lo más valioso del capítulo es desarrollar sensibilidad para detectar cuándo los enfoques rápidos se rompen.

## Bayesiana frente a frecuentista
El gran cisma entre estadística bayesiana y frecuentista (o clásica) es más filosófico que práctico: en la mayoría de problemas dan respuestas casi iguales. Ambas toman datos y construyen un modelo del mundo (por ejemplo, una normal); la diferencia está en la relación entre datos y modelo. En la estadística clásica el modelo debe ser el "mejor ajuste" a los datos: se asume una forma (como la normal) y se fijan los parámetros para que los datos sean lo más plausibles posible, y con ese modelo de mejor ajuste se predice.

En la bayesiana hay una capa extra: no solo tenemos parámetros de mejor ajuste, sino una distribución de confianza sobre qué parámetros podrían ser los correctos. Esa distribución representa nuestra creencia falible, no un ajuste riguroso. Se parte de un "prior" (distribución de confianza sin datos) y se refina a medida que llegan datos. Para predecir, se promedian las predicciones sobre todos los valores posibles del modelo, ponderados por la confianza. La bayesiana es útil cuando hay conocimiento experto para el prior o faltan muchos datos; la clásica suele ser más fácil de calcular.

## Contraste de hipótesis: idea clave y ejemplo
El hypothesis testing evalúa cuán probable es que un patrón observado sea real frente a una casualidad; no cuantifica la fuerza del patrón y está pensado para datos escasos. Ejemplo: una moneda lanzada 10 veces da 9 caras. No podemos responder "¿cuán probable es que esté cargada?" porque eso exigiría conocimiento a priori. La gran idea clásica es invertir la pregunta: ¿cuán probable es el dato suponiendo que la moneda es justa?

Con moneda justa hay 2^10 = 1024 secuencias equiprobables. Resultados tan o más sesgados que 9 caras: 10 caras (1 forma), 9 caras (10 formas), 10 cruces (1), 9 cruces (10), en total 22. Así, 22/1024 = 0.0215: solo un 2 % de probabilidad de ver algo así con una moneda justa.

Términos: el "null hypothesis" es que no hay patrón real (moneda justa). El "test statistic" es un número calculado de los datos cuya distribución se puede calcular bajo la hipótesis nula (aquí, el número de caras). El "p-value" es la probabilidad de ver un estadístico tan extremo bajo la nula. Un resultado es "statistically significant" si el p-valor baja de un umbral; la convención de 0.05 es arbitraria y se trata de una escala gradual. Caveats: el test dice que un patrón existe, no cuán fuerte es, y produce falsos positivos (con umbral 5 %, 1 de cada 20 pruebas sin patrón real dará significancia).

## Contraste de hipótesis múltiple
A menudo se prueban varias hipótesis a la vez (p. ej., 20 anuncios para ver si alguno mejora la tasa de clics con umbral 0.05). Aunque cada anuncio tiene solo un 5 % de pasar por azar, es muy probable que alguno pase por suerte. Hay que endurecer el p-valor individual para mantener un 0.05 global. La solución estándar, conservadora y simple es la Bonferroni correction: con n pruebas y un p-valor global α deseado, cada prueba individual debe pasar con α/n. Es excesivamente estricta porque supone que todas las pruebas son independientes, lo que a menudo no ocurre (p. ej., altura y peso están correlacionados, así que se testean "1.3 hipótesis" más que dos). Existen ajustes más complejos, pero el data scientist rara vez necesita más que Bonferroni.

## Estimación de parámetros
Mientras el contraste mide si hay efecto, la parameter estimation cuantifica su magnitud estimando los parámetros de una distribución (por ejemplo, media µ y desviación σ de una normal) con la media y la varianza muestrales. Esos estimadores son a su vez estadísticos calculados de los datos: si recogiéramos otra muestra, cambiarían, así que son variables aleatorias con su propia distribución. Dos términos clave:

- Consistency: un estimador es consistente si converge al valor real cuando crece el número de datos.
- Bias: un estimador es insesgado si su valor esperado es el valor real.

La media y la varianza muestrales son ambas consistentes, pero solo la media es insesgada; la varianza muestral subestima en promedio la desviación real. La intuición: al minimizar la suma de cuadrados respecto a la media estimada, se hace que esta ajuste demasiado bien los datos, por lo que la desviación sale más pequeña que la real. El estimador insesgado divide por N−1 en lugar de N, y ambos convergen cuando N tiende a infinito.

## Contraste de hipótesis: t-Test
El t-test es una versión más compleja, útil cuando la medida es un número continuo y se quiere saber si las medias reales de dos distribuciones son iguales (p. ej., colesterol de pacientes con y sin medicación). La intuición es dibujar los histogramas: si las campanas están bien separadas, las distribuciones difieren. Calcular el p-valor con rigor es mucho más complicado que en la moneda, pero en Python es trivial con SciPy:

```python
from scipy.stats import ttest_ind
t_score, p_value = ttest_ind([1,2,3,4], [2,2.2,3,5])
# permitir desviaciones distintas:
t_score, p_value = ttest_ind([1,2,3,4], [2,2.2,3,5], equal_var=False)
```

Hay dos opciones de hipótesis nula: que ambos datasets vienen de la misma normal, o que vienen de normales con la misma media aunque distinta desviación. Ninguna fija una distribución completa. El t-statistic mide cuán separadas están las medias muestrales, penalizando por el tamaño y la varianza de las muestras; bajo la nula sigue una T-distribution (parecida a una normal estándar pero con colas más pesadas). El t-test asume normalidad: un fallo puede deberse a medias distintas o a que los supuestos son falsos. Para comprobar normalidad hay otro test, basado en el z-score, que mira la pesadez de las colas:

```python
from scipy.stats import normaltest
z_score, p_value = normaltest(my_array)
```

## Intervalos de confianza
Al estimar un parámetro conviene dar un intervalo, no solo un único número. El caso más común es la media, y muchos otros cálculos (como la desviación) pueden reformularse como una media. La métrica típica es el "standard error of the mean" (SEM): un valor reportado como 4.1 ± 0.2 tiene 4.1 como media y 0.2 como SEM. En Python:

```python
from scipy.stats import sem
std_err = sem(my_array)
```

Si la distribución es normal, el intervalo µ̂ ± z·SEM contiene la media un porcentaje fijo del tiempo según el coeficiente z: 99 % con 2.58, 95 % con 1.96, 90 % con 1.64. La interpretación rigurosa no es "hay un 95 % de probabilidad de que la media esté en el intervalo" (la media real está o no está), sino que si se repite el muestreo de N puntos, el 95 % de los intervalos calculados contendrán la media real; la aleatoriedad está en los datos, no en el parámetro fijo. Todo depende del supuesto de normalidad; existen fórmulas alternativas, poco usadas en data science. Otro paradigma define el intervalo como el conjunto de valores "plausibles" del parámetro, es decir, los que dan un p-valor alto en un contraste de hipótesis.

## Estadística bayesiana
La bayesiana asume que algo del mundo sigue un modelo con parámetros, pero en lugar de elegir el mejor ajuste (sin aporte humano), parte de una distribución de confianza sobre todos los valores posibles del parámetro y la actualiza con cada dato. Su base es el teorema de Bayes: P(T|D) = P(T)·P(D|T) / P(D). Se vuelve potente cuando T es un parámetro fijo pero desconocido y su "distribución de probabilidad" mide nuestra confianza. Requiere el prior P(T) (confianza previa), la verosimilitud P(D|T) (a menudo conocida o modelable) y P(D) (probabilidad de los datos promediada sobre todos los valores). El lado izquierdo da lo que la estadística clásica no podía: la "probabilidad" de que el parámetro valga algo dado el dato. Resulta más cómodo pensar en odds: para actualizar la razón de probabilidades se multiplica por la verosimilitud relativa (ejemplo del usuario con pelo largo).

## Naive Bayes, redes bayesianas y priors
Lo más difícil suele ser calcular P(D|T), porque D es un vector multidimensional con dependencias complejas. En naive Bayes se asume que todas las variables son independientes entre sí condicionadas a T, de modo que basta describir la relación de cada variable con T por separado. Es una simplificación drástica pero sorprendentemente eficaz; su defecto es que si varias Di están muy relacionadas (pelo largo, coletero, pelo que tarda en secar son casi lo mismo), empujan en exceso la clasificación y la vuelven sobreconfiada.

Un punto medio son las Bayesian networks: un grafo donde algunas Di dependen de otras. Por ejemplo, Gender influye en Hair Length, y esta en el tiempo de champú y en llevar coletero; el género es independiente del tiempo de champú si se condiciona en la longitud del pelo. Son eficientes de entrenar: basta conocer la distribución de género, la de longitud dado el género y las del resto dado la longitud. La topología se construye a mano con conocimiento del dominio y luego se entrena con datos.

Para elegir priors cuando la ignorancia es total, la teoría de la máxima entropía justifica repartir la confianza por igual (50 %/50 %): la entropía H[T] = −Σ p·ln(p) mide la incertidumbre, y maximizarla refleja ignorancia completa, lo que para n estados discretos se logra con pt = 1/n. Hay un análogo continuo que da una densidad constante sobre un intervalo finito.

## Ideas clave
- La data science es en gran medida un subconjunto de la estadística; lo esencial no es dominarla, sino heredar su rigor y detectar cuándo los atajos fallan.
- La estadística atiende restricciones (sobre todo el tamaño de muestra) que el Big Data suele eludir.
- El contraste de hipótesis invierte la pregunta: calcula cuán probable es el dato bajo la hipótesis nula (p-valor), sin medir la fuerza del patrón y generando falsos positivos.
- Con múltiples hipótesis, la Bonferroni correction (α/n) controla el falso positivo global, aunque es conservadora al suponer independencia.
- La media muestral es un estimador consistente e insesgado; la varianza muestral es consistente pero sesgada a la baja (se corrige dividiendo por N−1).
- El t-test compara las medias de dos distribuciones normales; los intervalos de confianza (µ̂ ± z·SEM) acotan la estimación bajo normalidad.
- La diferencia bayesiana/frecuentista es más filosófica que práctica; Bayes parte de un prior y lo actualiza con los datos vía P(T|D) = P(T)·P(D|T)/P(D).
- Naive Bayes asume independencia condicional (simple y eficaz pero sobreconfiado); las redes bayesianas son un punto medio y la máxima entropía justifica priors de ignorancia.
