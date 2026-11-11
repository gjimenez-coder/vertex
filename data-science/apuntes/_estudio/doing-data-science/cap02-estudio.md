# Statistical Inference, Exploratory Data Analysis, and the Data Science Process (Inferencia estadística, análisis exploratorio de datos y el proceso de la ciencia de datos) — Estudio

## Tarjetas de repaso

P: ¿Qué son los datos según el capítulo y qué implica cómo los recogemos? / R: Son las huellas de procesos del mundo real; qué huellas se recogen lo decide el método de muestreo, que es un proceso subjetivo, no objetivo.

P: ¿Qué es la inferencia estadística? / R: La disciplina que desarrolla procedimientos, métodos y teoremas para extraer significado e información de datos generados por procesos estocásticos (aleatorios).

P: ¿Cuáles son las dos fuentes de aleatoriedad e incertidumbre al convertir el mundo en datos? / R: La del propio proceso del mundo real y la asociada al método de recolección (muestreo).

P: ¿Qué distinción hace la estadística clásica entre N y n? / R: N es el número total de observaciones de la población y n el tamaño de la muestra, el subconjunto examinado para inferir sobre la población.

P: ¿Por qué importa el mecanismo de muestreo? / R: Porque puede introducir sesgos y distorsionar los datos, de modo que la muestra no sea una "versión en miniatura" de la población.

P: ¿Qué sostiene el eslogan "N=ALL" y cómo lo rebaten las autoras? / R: Propone usar todos los datos, aceptar el desorden y renunciar a las causas; las autoras replican que casi nunca se tiene todo y que lo que falta suele ser lo más importante.

P: ¿Qué es un modelo? / R: Un intento de entender y representar la realidad a través de una lente; una construcción artificial de la que se ha abstraído todo detalle superfluo.

P: ¿Qué consejo dan las autoras para empezar a construir un modelo? / R: Hacer primero "lo más tonto que se te ocurra", trazar histogramas y diagramas de dispersión, escribir supuestos aunque estén mal y aumentar la complejidad poco a poco.

P: ¿Qué significa ajustar un modelo? / R: Estimar sus parámetros con los datos observados, a menudo mediante optimización como la estimación por máxima verosimilitud (maximum likelihood estimation).

P: ¿Qué es el overfitting? / R: Cuando el modelo ajusta bien los datos muestreados pero captura mal la realidad fuera de ellos; se detecta al predecir sobre datos nuevos con una métrica como la exactitud.

P: Según Tukey, ¿qué es el EDA? / R: "Una actitud, un estado de flexibilidad": no hay hipótesis ni modelo y la comprensión del problema cambia sobre la marcha.

P: ¿En qué se diferencia el EDA de la visualización de datos? / R: El EDA se hace al inicio y solo para ti (ganar intuición); la visualización se hace al final, para comunicar hallazgos.

P: ¿Cuáles son las etapas del proceso de la ciencia de datos? / R: Del mundo real a datos crudos, procesado/data munging hasta un conjunto limpio, EDA, diseño del modelo con un algoritmo y finalmente interpretación, visualización, informe o producto de datos.

P: ¿Qué distingue a un producto de datos y qué efecto provoca? / R: Se reincorpora al mundo real y los usuarios generan más datos, creando un bucle de realimentación; el modelo influye en el fenómeno que observa, no solo lo predice.

P: ¿Qué son las 4 V del Big Data? / R: Volumen, variedad, velocidad y valor.

## Preguntas de autoevaluación

P: ¿Por qué dicen las autoras que convertir el mundo en datos es subjetivo y no objetivo? / R: Porque las huellas que se recogen dependen del método de muestreo elegido, lo que introduce decisiones y sesgos; los datos no "hablan por sí solos". (Sección "El pensamiento estadístico en la era del Big Data")

P: En el ejemplo de BigCorp, ¿por qué dos muestras del mismo tamaño pueden dar estimaciones muy distintas? / R: Porque muestrear 1/10 de los empleados o 1/10 de los correos diarios tiene el mismo n pero el mecanismo de muestreo distinto puede producir estimaciones muy diferentes del número de correos por persona. (Sección "Poblaciones y muestras")

P: ¿Qué enseña el ejemplo de Kate Crawford con los tuits del huracán Sandy? / R: Que aunque se tenga todo el corpus, las inferencias no deben extenderse fuera de ese conjunto de usuarios: los tuits eran de neoyorquinos usuarios intensivos de Twitter, no de los costeros de Nueva Jersey, y sin contexto ni se interpretaría bien. (Sección "Poblaciones y muestras")

P: ¿Por qué ignorar la causalidad es un defecto y no una virtud, según el ejemplo del algoritmo de contratación? / R: Porque un algoritmo podría aprender a preferir a hombres sobre mujeres igualmente cualificadas por datos históricos, en lugar de preguntarse si la empresa las trata mal; renunciar a las causas perpetúa el sesgo. (Sección "'Big Data' y las grandes suposiciones")

P: ¿Qué papel juegan las distribuciones de probabilidad en el modelado? / R: Son los cimientos de los modelos estadísticos; ciertas formas reaparecen al medir fenómenos reales (normal, Poisson, Weibull, exponencial) y una función de densidad p(x) integra 1, lo que permite interpretarla como probabilidad. (Sección "Modelado")

P: ¿Para qué sirve el EDA más allá de hacer gráficos? / R: Para ganar intuición, comparar distribuciones, hacer comprobaciones de cordura (sanity checking), localizar datos ausentes y outliers, resumir y depurar el proceso de logging antes de modelar. (Sección "Análisis exploratorio de datos (EDA)")

P: ¿Por qué un recomendador se diferencia de predecir el tiempo? / R: Porque el recomendador influye en el fenómeno que observa (los modelos no solo predicen el futuro, también lo causan), mientras que tu modelo del tiempo no causa la lluvia; hay que ajustar los sesgos que el propio modelo provoca. (Sección "El proceso de la ciencia de datos")

P: ¿Qué dos problemas ataca RealDirect con datos inmobiliarios? / R: Los corredores que acaparan datos y la mala calidad/antigüedad de los datos públicos (hasta tres meses de retraso entre una venta y su publicación). (Sección "Experimento mental y caso de estudio")

## Puntos a dominar

- Explicar por qué los datos son huellas subjetivas de procesos del mundo real y nombrar las dos fuentes de incertidumbre (proceso y recolección).
- Distinguir población y muestra, y el significado de N y n, reconociendo que el muestreo puede introducir sesgos.
- Argumentar por qué "N=ALL" casi nunca es cierto y por qué los datos no son objetivos ni hablan por sí solos.
- Definir qué es un modelo, aplicar el consejo de empezar simple y explicar el compromiso entre simplicidad y precisión.
- Relacionar distribuciones de probabilidad, ajuste de parámetros (máxima verosimilitud) y el riesgo de overfitting.
- Describir el EDA como actitud y conjunto de herramientas, y diferenciarlo de la visualización de datos.
- Enumerar las etapas del proceso de la ciencia de datos y explicar el bucle de realimentación de un producto de datos.
- Reconocer el papel del científico de datos en todas las etapas y el hábito de preguntar para aclarar el vocabulario del dominio.
