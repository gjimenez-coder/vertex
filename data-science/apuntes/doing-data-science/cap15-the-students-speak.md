# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 15 — The Students Speak (Hablan los estudiantes)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

Este capítulo lo escriben los propios estudiantes de la primera edición del curso Introduction to Data Science de Rachel Schutt en Columbia. Los autores son Alexandra Boghosian, Jed Dougherty, Eurry Kim, Albert Lee, Adam Obeng y Kaz Sakamoto. En lugar de exponer teoría, reflexionan sobre cómo vivieron el curso y qué aprendieron sobre la práctica real de la data science.

La tesis central es que la data science es un campo emergente y aún en construcción, sin cuerpo de conocimiento institucionalizado. Por eso no basta con aprender técnicas en orden de dificultad: hay que aprender el proceso, la forma en que los científicos de datos deciden qué problemas estudiar y cómo abordarlos. La frase que recorre el capítulo, atribuida a Emily Bell, resume su postura: "Every algorithm is editorial" (PDF p. 365).

Sales sabiendo que la data science es un oficio colectivo y editorial: las decisiones sobre qué algoritmo y qué variables usar son juicios que condicionan los resultados; el aprendizaje ocurre en comunidad (compañeros, ponentes invitados, foros online); y la intuición sobre datos reales y desordenados solo se gana con la experiencia, no con problemas académicos idealizados.

## Process Thinking (Pensar en procesos)

Los estudiantes abren con una analogía: una clase introductoria de física cubre mecánica, electricidad y magnetismo en orden de dificultad creciente, pero nunca enseña cómo Newton llegó realmente al cálculo diferencial —sus herramientas, lecturas, dudas o su "papel de borrador" (PDF p. 365-366). Ese proceso no se enseña, pero es justo lo que un científico incipiente tendrá que hacer.

Rachel empezó el curso con una advertencia de peso: la data science aún se está definiendo, tanto en la industria como en la academia. Cada ponente llegaba con su estilo, trasfondo y enfoque, y casi todos decían algo como "no sé qué habéis cubierto hasta ahora, pero…". Las clases eran discretas y tocaba a los alumnos interpolar una narrativa continua, construyendo su propio significado igual que los científicos de datos siguen construyendo su campo.

El primer día Rachel propuso una definición de trabajo: un científico de datos es alguien cuya aptitud se reparte entre matemáticas, estadística, informática, machine learning, visualización, comunicación y conocimiento del dominio. Los estudiantes la describen como un simple prior en su entendimiento bayesiano en construcción: cada alumno y cada ponente se evaluaba frente a esa definición, y cada ponente aportaba un nuevo likelihood ratio. Venían de la academia, las finanzas, grandes tecnológicas y startups; había dropouts de posgrado, ganadores de Kaggle y artistas digitales. La propia clase se volvió una definición iterativa de la data science.

Además de escuchar, hacían tareas difíciles con datos reales y desordenados, muchas veces sobre problemas de la industria, entregadas como informes claros presentables a un profesional. Lo más importante: tenían que salir de su zona de confort y apoyarse unos en otros. Rachel subrayaba el carácter social del campo, y solía llevarlos al bar de enfrente junto con el ponente de la noche.

## Naive No Longer (Ya no tan ingenuos)

El punto de inflexión llegó con el tercer apartado de la segunda tarea, "Jake's Exercise: Naive Bayes for Article Classification". Había que descargar 2.000 artículos del New York Times —cuya API solo permitía 20 por llamada— y entrenar un clasificador Naive Bayes para ordenarlos por sección. Conseguir los artículos era solo la mitad del reto: debían escribir su propio código a partir de unas pocas ecuaciones, con hiperparámetros de regularización ajustables y clasificando en cinco categorías en lugar de dos. Como les dijeron, el Naive Bayes simple ni es tan ingenuo, ni tan bayesiano, ni tan simple. Quienes aguantaron 40 horas "puliendo" 300 líneas de código R hacky vieron cómo sus modelos rozaban el 90% de precisión y quedaron enganchados (PDF p. 367-368).

La otra mitad del proyecto final era una competición de Kaggle entre los alumnos para crear un algoritmo que calificara ensayos. La solución de uno de los autores incluía como features el número de faltas de ortografía, el número de palabras de la lista Dale-Chall (las que un niño de cuarto grado debería entender), vectores TF-IDF de las 50 palabras más frecuentes y la raíz cuarta del número de palabras del ensayo. El modelo combinaba random forest y gradient boosting, con optimización estocástica de hiperparámetros, entrenando cincuenta mil modelos durante miles de horas en instancias de Amazon EC2. "It worked OK" (PDF p. 368).

## Helping Hands (Manos que ayudan)

En una de las primeras clases conocieron al ponente invitado Jake Hofman, cuya charla describen como un truco de magia: con utilidades simples de Unix y datos básicos, construyó en directo un clasificador Naive Bayes de spam, parseando los correos públicos de Enron que descargó en el momento con su "command-line-fu" (PDF p. 368-369).

Mientras los ponentes semanales ofrecían actuaciones de ovación, fueron Jared Lander y Ben Reddy quienes, en las sesiones de laboratorio de apoyo, les enseñaron la mecánica: desde la regresión lineal hasta el funcionamiento del random forest, y herramientas nuevas como expresiones regulares, LaTeX, SQL, R, la shell, git y Python, además del acceso a datos mediante APIs y web scraping.

Cada perfil cargaba con su propia dificultad: los informáticos tenían que aprender selección de features basada en teoría y R; los científicos sociales, la mecánica de una base de datos y la diferencia entre variables de ámbito global y local; y los de finanzas, ética. A medida que mejoraban, dejaban de ver el código para ver solo las ideas detrás.

Rachel impuso el trabajo en grupo de forma indirecta, asignando tareas enormes pero divisibles, para que entendieran que practicar data science es intrínsecamente un esfuerzo colectivo. Al inicio mostró un diagrama de red en estrella (hub-and-spoke) con ella en el centro, con la esperanza de que surgieran amistades, ideas y proyectos. En un campo emergente, formar parte de una comunidad no solo ayuda a la carrera: es esencial para la práctica, porque el conocimiento está en continuo cambio y distribuido —la única manera de saber qué deberías saber es mirar lo que saben otros. Lo ilustra el hecho de que, en un meetup sobre MapReduce en abril, Cathy pudo remitir una pregunta a Nick Avteniev, presente entre el público. Los alumnos también recurrieron a Stack Overflow, Google Groups y R bloggers, donde a menudo respondían los propios creadores de las herramientas, como Hadley Wickham, Wes McKinney y Mike Bostock (PDF p. 369-370).

## Your Mileage May Vary (Los resultados pueden variar)

No existe un repositorio platónico de conocimiento perfecto que se absorba por ósmosis. Hay buenas prácticas de distintas disciplinas, con vocabularios e interpretaciones diferentes para un mismo método (¿el parámetro de regularización es un prior o solo un suavizado?). Como no hay instituciones, no hay conocimiento institucionalizado, y por eso importa la estructura de las interacciones: puedes crear tus propias instituciones y eliges quién te influye. Los autores citan a Gabriel Tarde (vía Bruno Latour, vía Mark Hansen) sobre el joven granjero que, al dudar entre su maestro y sus sentidos ante el atardecer, queda atado a Galileo por un "rayo imitativo" (PDF p. 370-371).

Comparando soluciones vieron que los resultados variaban enormemente según unas pocas decisiones: el número de combinaciones posibles en el proceso es enorme, y "algorithms are editorial". Claudia Perlich (Media 6 Degrees), ganadora del KDD Cup en varios años, les contó un caso de data leakage: en una competición de resultados hospitalarios, los identificadores de paciente se habían asignado secuencialmente por clínica, y como cada clínica trataba gravedades distintas, el ID resultó un gran predictor. En la competición era una filtración involuntaria, pero en el mundo real quizá debería usarse (PDF p. 371-372).

David Madigan subrayó los retos éticos de las decisiones editoriales mostrando cómo los estudios observacionales en farmacia dan resultados muy dispares (ejemplo del gráfico de la aspirina), e insistió en no alejarse de los datos reales. La academia sufre un problema análogo: al estudiar las piezas por separado es casi imposible ver cómo encajan. Como contraste, citan el ejercicio 3.2 de "Linear Methods for Regression" de The Elements of Statistical Learning (Hastie y coautores), sobre bandas de confianza al 95% en una regresión polinómica cúbica. Ante ese problema, los estudiantes ya reaccionan con escepticismo: ¿en qué punto del proceso aparecería algo así?, ¿quién nos da los datos?, ¿quién les paga?, ¿y a quién le importa el rendimiento sobre lo que es, en esencia, nuestro training data? Matizan que no es del todo justo con Hastie: su filosofía es que entender las herramientas estadísticas sin el contexto de las decisiones y procesos que las rodean las vacía de sentido, y que lo desordenado de los datos reales solo se entiende viviéndolo.

## Bridging Tunnels (Tendiendo túneles)

Con respeto hacia Michael Driscoll, los estudiantes se definen no como ingenieros civiles con planos, sino como aventureros: saben qué buscan, llevan herramientas en la mochila, quizá un mapa y unos amigos. Si la ciencia es una serie de tuberías, no son fontaneros: son los Mario Brothers (PDF p. 373).

## Some of Our Work (Parte de nuestro trabajo)

Los estudiantes mejoraron el perfil del científico de datos del Capítulo 1 (Figura 15-3, "The Stars of Data Science", obra colaborativa de varios alumnos) y crearon una infografía sobre la creciente popularidad de la data science en las universidades (Figura 15-4, "A Constellation is Born"), basada en información disponible a finales de 2012 (PDF p. 373-374).

## Ideas clave

- La data science es un campo emergente sin conocimiento institucionalizado: hay que aprender el proceso, no solo las técnicas en orden de dificultad.
- La definición inicial de Rachel (matemáticas, estadística, informática, machine learning, visualización, comunicación, dominio) fue solo un prior que la clase refinó de forma iterativa.
- "Every algorithm is editorial": elegir algoritmo y variables son decisiones que condicionan los resultados y conllevan responsabilidad ética.
- El aprendizaje es colectivo: trabajo en grupo, ponentes invitados y comunidades online (Stack Overflow, R bloggers) donde responden los propios autores de las herramientas.
- La tarea de Naive Bayes y la competición de Kaggle enseñaron, con datos reales y desordenados, el oficio tal como se vive en la industria.
- El data leakage del ID de paciente (Claudia Perlich) muestra que una buena predicción puede venir de un artefacto de los datos, no del fenómeno.
- Frente al enfoque académico (ejercicio de Hastie et al.), la intuición sobre datos reales solo se gana con la experiencia.
