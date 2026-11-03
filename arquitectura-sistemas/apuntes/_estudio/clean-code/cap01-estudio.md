# Clean Code (Código limpio) — Estudio

## Tarjetas de repaso

- P: ¿Por qué sostiene Martin que "siempre habrá código"? / R: Porque el código es la expresión precisa de los requisitos; por alto que sea el nivel de abstracción del lenguaje, los detalles deben especificarse con rigor suficiente para que una máquina los ejecute, y eso es programar.
- P: ¿Qué relación hay entre requisitos bien especificados y código? / R: Son tan formales como el código y pueden actuar como pruebas ejecutables de este.
- P: ¿Qué efecto tiene el código malo sobre la productividad de un equipo? / R: La reduce asintóticamente hacia cero, hasta volver inmanejable el sistema.
- P: ¿Qué dice la ley de LeBlanc? / R: *Later equals never* ("después es igual a nunca"): el código malo que se deja "para otro día" no se arregla nunca.
- P: ¿Qué es "The Grand Redesign in the Sky" y por qué suele fallar? / R: Es la exigencia de rehacer todo el sistema; un *tiger team* construye uno nuevo mientras el viejo sigue cambiando, la carrera dura años y al terminar el nuevo sistema ya es, a su vez, un desastre.
- P: Según el apartado "Attitude", ¿de quién es la culpa del deterioro del código? / R: Nuestra, de los programadores; es poco profesional permitirlo, aunque haya presión de plazos o gestores.
- P: ¿Qué ilustra la analogía de Semmelweis (1847)? / R: Que un médico no deja de lavarse las manos porque el paciente lo exija; igual de poco profesional es que el programador ceda ante gestores que no entienden el riesgo del desorden.
- P: ¿Qué es el "code-sense" (sentido del código)? / R: Una habilidad penosamente adquirida que no solo detecta si el código es bueno o malo, sino que muestra la estrategia de transformaciones que preservan el comportamiento para pasar del desorden al orden.
- P: Según Bjarne Stroustrup, ¿qué hace el código limpio? / R: "Clean code does one thing well" (hace una cosa bien); tiene lógica directa, dependencias mínimas, manejo de errores completo y rendimiento casi óptimo.
- P: ¿Qué metáfora usan Dave Thomas y Andy Hunt sobre el deterioro del código? / R: Las *broken windows* (ventanas rotas): una ventana rota inicia la decadencia, igual que el código malo tienta a crecer el desorden.
- P: Según Grady Booch, ¿cómo se lee el código limpio? / R: "Reads like well-written prose" (se lee como prosa bien escrita); es simple, directo, con *crisp abstractions* y nunca oscurece la intención del diseñador.
- P: Para Michael Feathers, ¿cuál es la cualidad que engloba todas las demás? / R: El *care* (cuidado): el código limpio siempre parece escrito por alguien a quien le importa.
- P: ¿Cuáles son las reglas de código simple de Beck según Ron Jeffries, por orden de prioridad? / R: Pasa todas las pruebas; no contiene duplicación; expresa todas las ideas de diseño del sistema; minimiza el número de entidades (clases, métodos, funciones).
- P: ¿Qué significa que "somos autores"? / R: Que escribimos para lectores y somos responsables de comunicar bien; leemos código más de 10 veces por cada vez que escribimos, así que hacerlo fácil de leer lo hace más fácil de escribir.
- P: ¿Qué establece la regla del Boy Scout? / R: "Leave the campground cleaner than you found it": dejar el código un poco más limpio de como se encontró, de modo que no pueda pudrirse.

## Preguntas de autoevaluación

- P: ¿Por qué afirma Martin que el sueño de un futuro sin código es infundado? / R: Porque aunque crezcan los lenguajes de alto nivel y los DSL, sus especificaciones seguirán siendo código riguroso, preciso y formal; especificar los detalles es programar. (Sección "There Will Be Code")
- P: ¿Cuál es, según el capítulo, la única forma de ir rápido? / R: Mantener el código limpio en todo momento; apresurarse ensuciando el código no cumple plazos, los incumple de inmediato. (Secciones "Bad Code" y "The Primal Conundrum")
- P: ¿Qué ocurre cuando la dirección añade más personal a un proyecto con código desordenado? / R: El nuevo equipo no conoce la intención del diseño y, bajo presión, genera más desorden, acelerando la caída de productividad. (Sección "The Total Cost of Owning a Mess")
- P: ¿Qué diferencia hay entre reconocer código limpio y saber escribirlo? / R: Son cosas distintas, como distinguir buena de mala pintura sin ser pintor; escribir código limpio exige la disciplina de aplicar muchas técnicas pequeñas guiadas por el code-sense. (Sección "The Art of Clean Code?")
- P: ¿Por qué dice Dave Thomas que sin pruebas el código no es limpio? / R: Porque el código limpio debe poder ser leído y mejorado por otro desarrollador, y tener pruebas unitarias y de aceptación es parte de esa cualidad. (Sección "What Is Clean Code?")
- P: ¿Qué quiere decir que ninguna escuela de pensamiento es absolutamente correcta? / R: Que las opiniones de la Object Mentor School se presentan como absolutas dentro de esa escuela, pero muchas recomendaciones son controvertibles; son fruto de décadas de experiencia y de prueba y error. (Sección "Schools of Thought")
- P: ¿Por qué conviene optimizar el código para la lectura aunque escribir cueste más? / R: Porque la proporción de tiempo leyendo frente a escribiendo supera con creces 10:1, y hacerlo fácil de leer lo hace, en realidad, más fácil de escribir. (Sección "We Are Authors")
- P: ¿En qué consisten las mejoras mínimas que propone la regla del Boy Scout? / R: Mejorar un nombre, partir una función demasiado larga, eliminar un poco de duplicación o aclarar un `if` compuesto. (Sección "The Boy Scout Rule")

## Puntos a dominar

- Explicar por qué el código es la expresión precisa de los requisitos y por qué nunca desaparecerá.
- Argumentar el coste económico y profesional del código malo: productividad asintótica a cero y la ley *Later equals never*.
- Reconocer por qué el "gran rediseño en el cielo" rara vez resuelve el problema.
- Asumir que la responsabilidad del código es del programador, no de plazos ni gestores, y saber defenderlo con argumentos profesionales (analogía de Semmelweis).
- Enumerar las cualidades del código limpio según Stroustrup, Booch, Thomas, Feathers, Jeffries y Cunningham.
- Recitar las reglas de código simple de Beck en orden de prioridad.
- Interiorizar la mentalidad de "somos autores" y la proporción lectura/escritura superior a 10:1.
- Aplicar la regla del Boy Scout como práctica de mejora continua.
