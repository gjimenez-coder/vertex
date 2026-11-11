# Extracting Meaning from Data (Extraer significado de los datos) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central de Will Cukierski sobre variables y algoritmos?
R: "Mejores variables valen más que mejores algoritmos": la extracción y selección de variables son los pasos más importantes y subestimados del machine learning.

P: ¿Qué es una competición de ciencia de datos y qué elementos la componen?
R: Equipos o individuos compiten semanas o meses por diseñar un algoritmo de predicción; se dan un training set, una métrica de evaluación fijada de antemano y unas reglas (frecuencia de envíos, fusión de equipos). Ejemplos: KDD, Netflix Prize, Kaggle.

P: ¿Qué dos modelos de crowdsourcing distingue Will?
R: El distributivo (como Wikipedia, contribuciones simples y a gran escala) y el de problemas puntuales y difíciles (Kaggle, DARPA, InnoCentive), donde compiten especialistas por premio y prestigio.

P: ¿Qué características tiene una buena competición?
R: Pregunta factible e interesante, métrica de evaluación transparente y objetiva, y premios establecidos por adelantado.

P: ¿Cómo funciona Kaggle para un concursante?
R: Se dan un training set y un test set con las *x* visibles y las *y* ocultas; se suben predicciones y el sistema devuelve la puntuación. Un tercer conjunto hold-out decide al ganador al cerrar; se puede enviar hasta cinco veces al día y el leaderboard se actualiza al instante.

P: ¿Qué es el "leapfrogging" y qué riesgo conlleva?
R: El efecto de saltos de rana por el que los concursantes se superan por pequeños márgenes al actualizarse el leaderboard; incentiva mejorar pero empuja al sobreajuste y a modelos cada vez más complejos (como el ganador del Netflix Prize, demasiado complejo para producción).

P: ¿Qué es la selección de variables (feature selection)?
R: Identificar el subconjunto de datos (o de datos transformados) que entra en el modelo; no hay que meterlos todos, pues puede haber redundancias y variables correlacionadas, y a veces conviene crear variables nuevas (logaritmos, binarizar una continua).

P: ¿Cuáles son las tres familias de métodos de selección de variables (Guyon, 2003)?
R: Filtros, wrappers y métodos embebidos.

P: ¿Qué hacen los filtros y cuál es su limitación?
R: Ordenan las variables según una métrica (p. ej. correlación con el objetivo); son útiles en una primera pasada, pero ignoran la redundancia y las interacciones al tratar las variables como independientes.

P: ¿Qué es la regresión por pasos (stepwise) y sus tres métodos?
R: Un conjunto de algoritmos tipo wrapper: selección hacia delante (empezar sin variables y añadir la que más mejora), eliminación hacia atrás (empezar con todas y quitar la que menos aporta) y enfoque combinado (híbrido).

P: ¿Cómo se define la entropía y la ganancia de información en un árbol de decisión?
R: Entropía H(X) = −p(X=1)·log₂p(X=1) − p(X=0)·log₂p(X=0), medida de cuán "mezclado" está algo. Ganancia de información IG(X,a) = H(X) − H(X|a): cuánta entropía se pierde al conocer el atributo a.

P: ¿Por qué los árboles de decisión son selección embebida y cómo se construyen?
R: Se construyen iterativamente desde la raíz eligiendo en cada nodo el atributo que maximiza la ganancia de información; la propia ganancia de información hace la selección por ti. Suelen podarse después para evitar el sobreajuste.

P: ¿Qué son los random forests y con qué hiperparámetros se definen?
R: Generalizan los árboles con bagging (bootstrap aggregating): más precisos y robustos, pero menos interpretables. Se definen con el número de árboles N y el número de variables F seleccionadas al azar por árbol (más un tercero: tamaño de la muestra bootstrap, típicamente 80%).

P: ¿En qué consiste el enfoque híbrido de investigación de Google (Huffaker)?
R: Combinar métodos cualitativos y cuantitativos, y datos pequeños y grandes, con investigadores embebidos en equipos de producto, trabajo iterativo con código casi de producción desde el día 1 y experimentos con grupos pequeños, para pasar de lo descriptivo a lo predictivo.

P: ¿Qué problema de causalidad frente a correlación ilustra Chasing Dragons?
R: Dar muchos puntos sin que el usuario juegue no lo hará volver, porque el factor de confusión es que le gusta el juego; conviene seleccionar con todas las variables pero actuar sobre las que puedes controlar (p. ej. mostrar menos anuncios) y validar con A/B testing.

## Preguntas de autoevaluación

P: ¿Por qué el libro advierte que el ranking en competiciones es un proxy imperfecto del talento de un científico de datos?
R: Porque muchos de los mejores —especialmente mujeres, incluidas las autoras— no compiten, y las competiciones recortan "lo complicado" (buenas preguntas, recogida y limpieza de datos, visualización y comunicación). (Sección: Competiciones de ciencia de datos y crowdsourcing)

P: Según Jeremy Howard, ¿qué separa a los ganadores de las competiciones y qué papel deja al experto de dominio?
R: Lo que separa a los ganadores es la información que alimentan al algoritmo: decidir qué abstraer de los datos siendo curiosos y creativos; deja un papel al experto solo al principio (estrategia, qué problema resolver), defendiendo que los algoritmos ya dicen qué importa. (Sección: Pericia de dominio frente a algoritmos de machine learning)

P: ¿Por qué "más grande no siempre es mejor" en cuanto a datos y variables?
R: Porque más datos a veces son solo más datos sin señal (como registrar tiradas de dados), y si hay más variables que observaciones aparecen problemas de sparsity o solo complejidad computacional sin mejorar la señal. (Sección: Selección de variables)

P: ¿Cómo clasifica el libro la información en "cuatro cubos" al generar variables?
R: Relevante y útil pero imposible de capturar (con posibles proxies); relevante, capturable y lo registraste (la selección confirma si sirve); relevante, capturable pero no lo hiciste (tu imaginación es la restricción, mitigable con estudios de usabilidad); y no relevante ni útil (si lo registraste, la selección debe descubrirlo). (Sección: El ejemplo que recorre el capítulo: Chasing Dragons)

P: ¿Qué criterios de selección menciona el libro para los wrappers y qué advertencia da sobre su elección?
R: R-cuadrado, p-valores, AIC (2k − 2 ln L), BIC (k·ln n − 2 ln L) y entropía; la elección del criterio es algo arbitraria y conviene probar varios para ver la robustez del modelo. (Sección: Filtros, wrappers y criterios de selección)

P: ¿Qué relación tiene la selección de variables con el "data dredging" y cómo se mitiga el riesgo?
R: Si se acepta cualquier correlación con el objetivo se puede caer en señales espurias (p. ej. que la mantequilla de Bangladés "prediga" el S&P); se mitiga curando primero las variables candidatas, pues cuantas más observaciones, menor el riesgo. (Sección: Críticas e interpretabilidad frente a poder predictivo)

P: En el caso de los "círculos" de Google+, ¿qué enfoque usó Google y a qué conclusión llegó sobre el diseño del producto?
R: Un enfoque de métodos mixtos para triangular (muestra aleatoria de 100.000 usuarios, 168 encuestas, 12 entrevistas largas); concluyó que la gente disfruta compartiendo selectivamente según contenido, contexto y audiencia, y el producto debe diseñarse en torno a esos tres ejes. (Sección: El enfoque híbrido de Google)

P: ¿Qué halló Google sobre privacidad y participación, y qué soluciones surgieron?
R: Fuerte correlación entre preocupación por la privacidad y baja participación, ligada a cuánto entiende el usuario qué se comparte y cuánto control tiene; soluciones: transparencia del destino de los datos, un "switchboard" de privacidad, ajustes rápidos y, sobre todo, valores por defecto razonables. (Sección: El enfoque híbrido de Google)

## Checklist

- Al generar variables, no ser selectivo al principio: hacer brainstorming amplio con el equipo (diseño, ingeniería, estadística, marketing) y aceptar redundancias y correlaciones.
- Clasificar la información candidata según si es capturable y si se te ocurrió capturarla (los cuatro cubos); usar proxies cuando el dato directo sea imposible.
- Si dispones de un experto de dominio, aprovecharlo antes de "meterte en la madriguera" del machine learning.
- Empezar con un modelo crudo y simple (p. ej. regresión logística) antes de complicar.
- Usar filtros para una primera criba, recordando que ignoran redundancias e interacciones.
- Probar varios criterios de selección (R-cuadrado, p-valores, AIC, BIC, entropía) para comprobar la robustez del modelo.
- Podar los árboles de decisión para evitar el sobreajuste; en random forests, normalmente no podar.
- Especificar los hiperparámetros de un random forest: número de árboles N, variables F por nodo y tamaño de la muestra bootstrap (~80%).
- Distinguir variables sobre el comportamiento del usuario de las de tu propio comportamiento; hacer la selección con todas pero actuar solo sobre las que puedes controlar.
- Vigilar causalidad frente a correlación (factores de confusión) y validar las decisiones con A/B testing.
- Al trabajar con big data, complementarlo con métodos cualitativos y estudios de usabilidad a pequeña escala.
- En R, apoyarse en librerías como `rpart` para árboles y `randomForest`, glmnet, bagging y boosting para los ejemplos del capítulo.
