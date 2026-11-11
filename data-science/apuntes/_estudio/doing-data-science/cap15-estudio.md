# The Students Speak (Hablan los estudiantes) — Estudio

## Tarjetas de repaso

P: ¿Quiénes escriben el Capítulo 15 y desde qué perspectiva? / R: Los propios estudiantes de la primera edición del curso de Rachel Schutt en Columbia (Boghosian, Dougherty, Kim, Lee, Obeng y Sakamoto), que reflexionan sobre cómo vivieron el curso y la práctica real de la data science.

P: ¿Cuál es la tesis central del capítulo? / R: La data science es un campo emergente sin cuerpo de conocimiento institucionalizado; por eso hay que aprender el proceso —cómo se decide qué problemas estudiar y cómo abordarlos— y no solo técnicas en orden de dificultad.

P: ¿Qué significa la frase "Every algorithm is editorial"? / R: Que elegir el algoritmo y las variables son juicios editoriales que condicionan los resultados y conllevan responsabilidad ética.

P: ¿Qué analogía con la física abre "Process Thinking"? / R: Una clase de física enseña mecánica, electricidad y magnetismo en orden de dificultad, pero nunca cómo Newton llegó al cálculo (sus herramientas, dudas y "papel de borrador"); ese proceso no se enseña pero es lo que hará el científico incipiente.

P: ¿En qué consistió la definición inicial de científico de datos de Rachel? / R: Alguien cuya aptitud se reparte entre matemáticas, estadística, informática, machine learning, visualización, comunicación y conocimiento del dominio; los alumnos la tomaron como un simple prior que la clase refinó de forma iterativa.

P: ¿Cómo describen los estudiantes la construcción del significado del curso con términos bayesianos? / R: La definición de Rachel era el prior y cada ponente aportaba un nuevo likelihood ratio, convirtiendo la clase en una definición iterativa de la data science.

P: ¿En qué consistió "Jake's Exercise: Naive Bayes for Article Classification"? / R: Descargar 2.000 artículos del New York Times (API limitada a 20 por llamada) y escribir desde cero un clasificador Naive Bayes con regularización ajustable para ordenarlos en cinco secciones; los que insistieron rozaron el 90% de precisión.

P: ¿Qué features usó la solución de Kaggle para calificar ensayos? / R: Número de faltas de ortografía, número de palabras de la lista Dale-Chall, vectores TF-IDF de las 50 palabras más frecuentes y la raíz cuarta del número de palabras, con un modelo de random forest y gradient boosting.

P: ¿Qué demostró Jake Hofman en su charla? / R: Construyó en directo, "como un truco de magia", un clasificador Naive Bayes de spam con utilidades simples de Unix sobre los correos públicos de Enron, descargados en el momento con su "command-line-fu".

P: ¿Qué papel tuvieron Jared Lander y Ben Reddy? / R: En las sesiones de laboratorio enseñaron la mecánica práctica: de la regresión lineal al random forest, y herramientas como regex, LaTeX, SQL, R, la shell, git, Python, APIs y web scraping.

P: ¿Por qué es esencial la comunidad en un campo emergente, según el capítulo? / R: Porque el conocimiento está en continuo cambio y distribuido; la única manera de saber qué deberías saber es mirar lo que saben otros (Stack Overflow, Google Groups, R bloggers, donde responden autores como Wickham, McKinney y Bostock).

P: ¿Qué es el data leakage según el caso de Claudia Perlich? / R: En una competición hospitalaria los IDs de paciente se asignaban secuencialmente por clínica, y como cada clínica trataba gravedades distintas, el ID se volvió un gran predictor: una filtración involuntaria en la competición, aunque quizá útil en el mundo real.

P: ¿Qué quiere decir "no existe un repositorio platónico de conocimiento"? / R: Que no hay conocimiento institucionalizado perfecto que se absorba por ósmosis; hay buenas prácticas de distintas disciplinas con vocabularios diferentes, y por eso importa la estructura de interacciones y quién te influye.

P: ¿Con qué metáfora cierran los estudiantes su identidad profesional? / R: No son ingenieros civiles con planos ni fontaneros de tuberías, sino aventureros con herramientas, mapa y amigos: si la ciencia es una serie de tuberías, son los Mario Brothers.

## Preguntas de autoevaluación

P: ¿Por qué los estudiantes afirman que aprender técnicas en orden de dificultad no basta para la data science? / R: Porque es un campo emergente sin conocimiento institucionalizado; lo esencial es aprender el proceso —cómo decidir qué problemas estudiar y cómo abordarlos—, igual que ellos tuvieron que interpolar una narrativa a partir de clases discretas. (Process Thinking)

P: ¿Cómo refleja la composición de la clase la naturaleza del campo? / R: Los alumnos venían de academia, finanzas, grandes tecnológicas y startups (dropouts de posgrado, ganadores de Kaggle, artistas digitales), y cada uno se evaluaba frente a la definición de Rachel, haciendo de la clase una definición iterativa de la data science. (Process Thinking)

P: ¿Qué enseñó la tarea de Naive Bayes más allá de la precisión del modelo? / R: Enseñó el oficio tal como se vive: obtener datos reales sorteando límites de API, escribir el propio código a partir de pocas ecuaciones y comprender que el Naive Bayes "simple" ni es tan ingenuo, ni tan bayesiano, ni tan simple. (Naive No Longer)

P: ¿Qué dificultad específica afrontaba cada perfil de estudiante? / R: Los informáticos debían aprender selección de features basada en teoría y R; los científicos sociales, la mecánica de bases de datos y variables de ámbito global frente a local; y los de finanzas, ética. (Helping Hands)

P: ¿Por qué Rachel impuso el trabajo en grupo de forma indirecta? / R: Asignó tareas enormes pero divisibles y mostró un diagrama de red en estrella con ella en el centro, para que entendieran que practicar data science es un esfuerzo intrínsecamente colectivo y surgieran amistades, ideas y proyectos. (Helping Hands)

P: ¿Qué muestra el caso de data leakage de Claudia Perlich sobre la predicción? / R: Que una buena predicción puede provenir de un artefacto de los datos (el ID de paciente correlacionado con la clínica y la gravedad) y no del fenómeno real; lo que es filtración en una competición podría ser válido en producción. (Your Mileage May Vary)

P: ¿Qué critican los estudiantes del enfoque académico ilustrado por el ejercicio de Hastie et al.? / R: Que estudiar las piezas por separado impide ver cómo encajan; reaccionan preguntando quién da los datos, quién paga y a quién le importa el rendimiento sobre lo que es su training data, aunque matizan que la filosofía de Hastie coincide: las herramientas sin contexto se vacían de sentido. (Your Mileage May Vary)

P: ¿Qué aportaron los estudiantes como parte de su propio trabajo? / R: Mejoraron el perfil del científico de datos del Capítulo 1 (Figura 15-3, "The Stars of Data Science") y crearon una infografía sobre la popularidad de la data science en universidades (Figura 15-4, "A Constellation is Born"), con datos de finales de 2012. (Some of Our Work)

## Puntos a dominar

- Entender la data science como campo emergente sin conocimiento institucionalizado: prioridad al proceso sobre la mera acumulación de técnicas.
- Explicar y aplicar la idea "Every algorithm is editorial", incluyendo su dimensión ética.
- Reconocer la definición de Rachel (matemáticas, estadística, informática, machine learning, visualización, comunicación, dominio) como un prior refinable, no como una verdad fija.
- Comprender por qué los datos reales y desordenados (tarea de Naive Bayes, competición de Kaggle) enseñan el oficio mejor que los problemas académicos idealizados.
- Identificar el data leakage y por qué una predicción fuerte puede venir de un artefacto de los datos.
- Valorar el aprendizaje colectivo: trabajo en grupo, ponentes invitados y comunidades online como fuentes esenciales de conocimiento distribuido.
- Situar cada herramienta estadística en el contexto de las decisiones y procesos que la rodean, en línea con la crítica al enfoque puramente académico.
