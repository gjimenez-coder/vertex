# Other Data Science Tasks and Techniques (Otras tareas y técnicas de ciencia de datos) — Estudio

## Tarjetas de repaso

P: ¿Qué es la ingeniería analítica según el capítulo? / R: Un enfoque donde el problema de negocio aporta el objetivo y las restricciones, los datos y el conocimiento del dominio son la materia prima, y la ciencia de datos ofrece marcos para descomponer el problema y herramientas para resolverlo; conviene reformular un problema nuevo como una tarea conocida en lugar de construir soluciones a medida.

P: ¿Qué busca la agrupación por co-ocurrencia o descubrimiento de asociaciones? / R: Relaciones entre entidades a partir de las transacciones que las involucran, formuladas como regla "si ocurre A, es probable que ocurra B también"; aplicaciones típicas son la venta cruzada y la optimización de operaciones.

P: ¿Qué miden support, confidence (strength), lift y leverage en una asociación? / R: Support es el porcentaje mínimo de transacciones a las que aplica la regla (control de complejidad contra el azar); confidence/strength es p(B|A); lift es el cociente p(A,B)/(p(A)·p(B)) frente a la independencia; leverage es la diferencia p(B,A)−p(A)·p(B).

P: En el ejemplo de cerveza y lotería (p(cerveza)=0,3, p(lotería)=0,4, p(cerveza y lotería)=0,2), ¿cuánto valen lift y leverage? / R: Lift ≈ 1,67 (0,2/0,12) y leverage = 0,08; hay algo de relación, pero buena parte de la co-ocurrencia se debe a que ambos ítems son muy populares.

P: ¿Qué son los "virtual items" en el análisis de asociaciones de Likes de Facebook? / R: Ítems virtuales añadidos a la cesta de Likes, como la ubicación del usuario o datos psicométricos (extroversión, afabilidad, IQ), para hallar asociaciones con esas características.

P: ¿Qué es el profiling y qué concepto fundamental lo sostiene? / R: Caracterizar el comportamiento típico de un individuo, grupo o población; es una instancia del concepto del Capítulo 4: definir una función numérica con parámetros, un objetivo, y encontrar los parámetros que mejor lo cumplen (p. ej. media y desviación como máxima verosimilitud bajo una gaussiana).

P: ¿Por qué hay que desconfiar de reportar media y desviación en datos sesgados? / R: Una cola larga sesga la media al alza y deja de representar el valor típico; conviene visualizar la distribución y, por ejemplo, reportar la mediana o tomar el logaritmo (distribución log-normal) para recuperar una campana.

P: ¿Qué es un Gaussian Mixture Model (GMM) y en qué se diferencia del clustering del Capítulo 6? / R: Ajusta varias gaussianas para identificar subgrupos; produce un clustering "suave" o probabilístico, donde cada punto tiene un grado o probabilidad de pertenencia a cada cluster en lugar de pertenecer estrictamente a uno.

P: ¿De qué dos formas se puede encuadrar la predicción de enlaces con los fundamentos? / R: Como similitud (los enlaces se dan entre individuos similares, usando medidas como amigos compartidos) o como modelado predictivo supervisado, donde la instancia es un par de personas y la variable objetivo es si la relación existe o se formaría.

P: ¿Qué significa "latente" y cómo se aplica a la recomendación de películas de Netflix? / R: Significa "relevante pero no observado explícitamente en los datos"; películas y usuarios se representan como vectores sobre dimensiones latentes de preferencia (serio vs. escapista, comedia vs. drama…) y se recomienda por similitud usuario–película.

P: ¿Qué es matrix factorization en el contexto del recomendador de películas? / R: El ajuste de la similitud usuario–película expresada como fórmula con d dimensiones desconocidas (pesos sobre películas y clientes), optimizando una función objetivo con regularización; determina a la vez cuán "rara" es una película y cuánto le gustan al usuario las películas raras.

P: ¿Qué es un ensemble model y por qué funciona? / R: Un "supermodelo" que combina muchos modelos (votando o promediando) tratados como expertos; funciona cuando los expertos cometen errores distintos e idealmente independientes, que al promediar tienden a cancelarse.

P: ¿En qué tres factores se descompone el error de un modelo? / R: Aleatoriedad inherente (cuyo límite teórico es la tasa de Bayes), sesgo (bias) y varianza (variance); existe un trade-off entre sesgo y varianza que el control de complejidad intenta equilibrar.

P: ¿Por qué los ensembles se usan especialmente con árboles? / R: Los árboles tienen alta varianza, y promediar métodos de alta varianza reduce la varianza de las predicciones; de ahí random forests, bagging y boosting.

P: ¿Por qué el marketing viral exige explicación causal y no solo correlación? / R: Porque por homofilia social la gente se agrupa con personas similares, así que los vecinos de un comprador comprarían aun sin influencia causal; un análisis cuidadoso mostró que los métodos tradicionales sobreestimaban la influencia en al menos un 700%.

## Preguntas de autoevaluación

P: ¿Por qué los autores insisten en entender la ciencia de datos desde los principios y no desde algoritmos sueltos? / R: Porque las técnicas adicionales del capítulo son instancias o combinaciones de los fundamentos ya vistos (control de complejidad, similitud, ajuste de funciones, supervisado vs. no supervisado, lift), y ante un problema nuevo conviene reformularlo como una tarea conocida en lugar de crear una solución a medida. (Sección: Lo que necesitas saber)

P: ¿Cómo decide el capítulo cuándo usar búsqueda de asociaciones y cuándo modelado supervisado? / R: Si se quiere entender qué correlaciona con una variable concreta (afabilidad, gustar de nuestra marca), se formula como problema supervisado; si se explora sin un objetivo específico, la búsqueda de asociaciones es más apropiada. (Sección: Asociaciones entre "Likes" de Facebook)

P: ¿Por qué el ejemplo de cerveza y lotería muestra que una co-ocurrencia alta no siempre es "interesante"? / R: Porque aunque el support (20%) y el strength (67%) son notables, el lift de solo ~1,67 revela que buena parte de la co-ocurrencia proviene de que ambos ítems son muy populares, no de una relación fuerte. (Sección: Ejemplo: cerveza y billetes de lotería)

P: ¿Qué relación tiene el profiling con el concepto del Capítulo 4 y con el clustering? / R: Es un ajuste de modelo (definir función con parámetros, un objetivo y optimizar), como reportar media y desviación bajo una gaussiana; y puede implicar clustering si hay subgrupos, llegando con el GMM a un clustering suave probabilístico. (Sección: Profiling: encontrar el comportamiento típico)

P: ¿Qué dos ideas combinó el equipo ganador del Netflix Challenge? / R: Ensembles de modelos y reducción de datos; el problema se planteó como predicción de la fuerza del enlace usuario–película usando dimensiones latentes y matrix factorization. (Secciones: Reducción de datos, información latente y recomendación de películas; Sesgo, varianza y métodos de ensemble)

P: ¿Cómo gestiona el control de complejidad el trade-off sesgo-varianza? / R: Buscando el "punto dulce" donde la suma de ambos errores es mínima; por ejemplo, con selección de variables, ya que predecir solo la tasa media es bajo en varianza pero alto en sesgo, y usar miles de variables aumenta la varianza (overfitting). (Sección: Sesgo, varianza y métodos de ensemble)

P: ¿Qué supuesto crítico sostiene el marketing viral y por qué un análisis ingenuo lo sobreestima? / R: El supuesto de que los consumidores realmente se influyen entre sí; un análisis ingenuo lo sobreestima porque la homofilia social agrupa a personas similares, de modo que los conocidos de un comprador comprarían igual sin influencia causal. (Sección: Explicación causal a partir de datos y el ejemplo del marketing viral)

## Puntos a dominar

- Encuadrar un problema nuevo como una tarea conocida de ciencia de datos (ingeniería analítica), reconociendo qué principio fundamental lo sostiene.
- Calcular e interpretar support, confidence/strength, lift y leverage, distinguiendo co-ocurrencia debida a popularidad de una asociación realmente fuerte.
- Reconocer cuándo el profiling debe reportar media/desviación y cuándo conviene mediana o transformación logarítmica según la forma de la distribución.
- Distinguir el clustering estricto (Capítulo 6) del clustering suave probabilístico del GMM.
- Plantear la predicción de enlaces de las dos maneras (similitud y modelado predictivo supervisado) e identificar atributos del par.
- Explicar qué son las dimensiones latentes y la matrix factorization en la recomendación de películas, y por qué su interpretación es a posteriori y subjetiva.
- Descomponer el error en aleatoriedad inherente (tasa de Bayes), sesgo y varianza, y justificar por qué los ensembles ayudan sobre todo con métodos de alta varianza.
- Diferenciar correlación de causación y detectar el sesgo que la homofilia social introduce en la estimación de influencia.
