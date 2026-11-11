# Statistics (Estadística) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre la relación entre data science y estadística?
R: Que buena parte de la data science es un subconjunto de la estadística y que su separación es más un accidente histórico que una diferencia esencial.

P: Si la mayoría de data scientists no necesita estadística profunda, ¿qué es lo verdaderamente crucial que aporta?
R: El pensamiento crítico: ser cuidadoso y riguroso con los datos y con los supuestos que se hacen.

P: ¿Qué restricción hace existir a la estadística y por qué el data scientist suele eludirla?
R: El tamaño de muestra; en Big Data suele sobrar información, mientras que en estadística cada dato puede ser caro (un cultivo, una vida).

P: ¿En qué se diferencian la estadística bayesiana y la frecuentista?
R: Es más filosófico que práctico: la clásica busca el modelo de mejor ajuste a los datos; la bayesiana añade una distribución de confianza sobre qué parámetros podrían ser los correctos.

P: ¿Cuál es la gran idea del contraste de hipótesis clásico?
R: Invertir la pregunta: en lugar de preguntar cuán probable es el patrón, calcula cuán probable es el dato suponiendo verdadera la hipótesis nula.

P: Define null hypothesis, test statistic y p-value.
R: La null hypothesis es que no hay patrón real; el test statistic es un número calculado de los datos con distribución conocida bajo la nula; el p-value es la probabilidad de ver un estadístico tan extremo bajo la nula.

P: ¿Qué significa que un resultado sea statistically significant y qué caveat tiene el umbral de 0.05?
R: Que el p-valor baja de un umbral; el 0.05 es arbitrario y la significancia es gradual, no binaria, y genera falsos positivos (1 de cada 20 con umbral 5 %).

P: ¿Qué problema aparece con el contraste de hipótesis múltiple y cómo se corrige?
R: Que al probar muchas hipótesis es probable que alguna pase por azar; la Bonferroni correction exige que cada prueba pase con α/n para mantener un α global.

P: ¿Por qué la Bonferroni correction es conservadora?
R: Porque supone que todas las pruebas son independientes, lo que a menudo no ocurre (variables correlacionadas como altura y peso).

P: ¿Qué diferencia hay entre consistency y bias en un estimador?
R: Consistency: converge al valor real cuando crecen los datos; bias: un estimador es insesgado si su valor esperado es el valor real.

P: ¿Qué propiedades tienen la media y la varianza muestrales como estimadores?
R: La media es consistente e insesgada; la varianza muestral es consistente pero sesgada a la baja, y se corrige dividiendo por N−1 en lugar de N.

P: ¿Para qué sirve el t-test y qué distribución sigue su estadístico bajo la nula?
R: Para saber si las medias reales de dos distribuciones normales son iguales; el t-statistic sigue una T-distribution (como la normal estándar pero con colas más pesadas).

P: ¿Cómo se interpreta rigurosamente un intervalo de confianza del 95 %?
R: No que haya 95 % de probabilidad de que la media esté en el intervalo, sino que al repetir el muestreo el 95 % de los intervalos calculados contendrán la media real; la aleatoriedad está en los datos.

P: ¿Cuál es el teorema de Bayes y qué requiere para la inferencia bayesiana?
R: P(T|D) = P(T)·P(D|T) / P(D); requiere el prior P(T), la verosimilitud P(D|T) y P(D), la probabilidad de los datos promediada sobre todos los valores.

P: ¿Qué asume naive Bayes y cuál es su principal defecto?
R: Asume que todas las variables son independientes condicionadas a T; su defecto es que si varias variables están muy relacionadas, empujan en exceso la clasificación y la vuelven sobreconfiada.

## Preguntas de autoevaluación

P: ¿Por qué el autor dice que ser "fast-and-loose" puede ser uno de los peores delitos de un data scientist?
R: Porque, aunque el Big Data suele permitir despreocupación, aplicar enfoques rápidos en situaciones que exigen rigor (pocos datos, datos caros) lleva a confundir casualidad con patrón real. (Sección "La estadística en perspectiva")

P: En el ejemplo de la moneda con 9 caras de 10 lanzamientos, ¿cómo se obtiene el p-valor de 0.0215?
R: Con moneda justa hay 2^10 = 1024 secuencias equiprobables; los resultados tan o más sesgados (10 caras, 9 caras, 10 cruces, 9 cruces) suman 22 formas, y 22/1024 = 0.0215. (Sección "Contraste de hipótesis: idea clave y ejemplo")

P: ¿Qué diferencia hay entre el contraste de hipótesis y la estimación de parámetros?
R: El contraste mide si hay un efecto (si el patrón es real); la estimación de parámetros cuantifica su magnitud estimando parámetros como media y desviación de una distribución. (Secciones "Contraste de hipótesis" y "Estimación de parámetros")

P: ¿Por qué la varianza muestral subestima la desviación real?
R: Al minimizar la suma de cuadrados respecto a la media estimada, esta ajusta demasiado bien los datos, por lo que la desviación resultante sale más pequeña que la real. (Sección "Estimación de parámetros")

P: Si un t-test da un p-valor que rechaza la nula, ¿qué dos causas pueden explicarlo?
R: Que las medias reales sean distintas, o que los supuestos sean falsos, ya que el t-test asume normalidad. (Sección "Contraste de hipótesis: t-Test")

P: ¿Cuándo es más útil la estadística bayesiana frente a la clásica?
R: La bayesiana es útil cuando hay conocimiento experto para el prior o faltan muchos datos; la clásica suele ser más fácil de calcular. (Sección "Bayesiana frente a frecuentista")

P: ¿Qué son las redes bayesianas y en qué se diferencian de naive Bayes?
R: Son un grafo donde algunas variables dependen de otras (p. ej., Gender influye en Hair Length), un punto medio que, a diferencia de naive Bayes, no asume independencia total; su topología se construye a mano con conocimiento del dominio y se entrena con datos. (Sección "Naive Bayes, redes bayesianas y priors")

P: ¿Cómo justifica la máxima entropía la elección de un prior ante ignorancia total?
R: La entropía H[T] = −Σ p·ln(p) mide la incertidumbre; maximizarla refleja ignorancia completa, lo que para n estados discretos da pt = 1/n (reparto equitativo). (Sección "Naive Bayes, redes bayesianas y priors")

## Puntos a dominar

- Entender por qué la data science hereda el rigor de la estadística aunque no requiera dominarla, y reconocer cuándo los atajos "rápidos y sucios" fallan.
- Explicar el papel del tamaño de muestra como la restricción central que motiva los métodos estadísticos.
- Aplicar la lógica del contraste de hipótesis: hipótesis nula, test statistic, p-valor y significancia, sin confundirlo con la fuerza del patrón.
- Reconocer el problema del contraste múltiple y aplicar la Bonferroni correction (α/n), sabiendo que es conservadora por suponer independencia.
- Distinguir consistency y bias, y recordar que la media muestral es insesgada mientras la varianza muestral se corrige con N−1.
- Saber cuándo usar el t-test (dos medias de distribuciones normales) y comprobar el supuesto de normalidad (normaltest).
- Interpretar correctamente un intervalo de confianza (µ̂ ± z·SEM) y los coeficientes z (2.58, 1.96, 1.64) bajo el supuesto de normalidad.
- Manejar el teorema de Bayes, el papel del prior y la verosimilitud, y las diferencias entre naive Bayes, redes bayesianas y priors de máxima entropía.
