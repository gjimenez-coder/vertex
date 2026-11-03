# Prólogo — Preface (Prefacio) — Estudio

## Tarjetas de repaso

P: ¿Qué es refactoring? / R: El proceso de cambiar un sistema de software de modo que no altere el comportamiento externo del código pero mejore su estructura interna.

P: ¿Por qué se describe el refactoring como "disciplinado"? / R: Porque es una forma de limpiar el código que minimiza las probabilidades de introducir errores.

P: ¿Cuál es la tesis central del prólogo sobre el diseño? / R: Que el diseño no tiene por qué ocurrir todo por adelantado; con refactorización sucede de forma continua durante el desarrollo, manteniendo un buen diseño a medida que el programa crece.

P: ¿Qué idea invierte el refactoring respecto al software? / R: La noción habitual de decaimiento del software: en lugar de que el código "se hunda de la ingeniería al hacking", se reelabora desde un mal diseño o el caos hasta un código bien diseñado.

P: ¿Por qué es contraintuitiva la frase "mejorar el diseño después de escrito"? / R: Porque la concepción habitual es diseñar primero y codificar después, mientras que el refactoring parte de un diseño ya existente para mejorarlo.

P: ¿Cómo logra el refactoring mejoras radicales si cada paso es simple? / R: Por el efecto acumulado de muchos cambios pequeños (mover un campo, extraer un método, subir o bajar código por la jerarquía).

P: ¿Qué papel tuvo Kent Beck en la historia personal de Fowler? / R: Fue traído para reiniciar el proyecto fallido; lo reescribió casi por completo e insistió en la limpieza continua mediante refactorización.

P: ¿Qué aporta el Capítulo 1 del libro? / R: Toma un programa pequeño con defectos de diseño comunes y lo refactoriza a un programa orientado a objetos más aceptable; es el capítulo clave para entender de qué va el refactoring.

P: ¿Qué son los "bad smells" y en qué capítulo se tratan? / R: Los malos olores del código; se detectan y limpian con refactorizaciones en el Capítulo 3, escrito con Kent Beck.

P: ¿Qué contienen los capítulos 5 a 12? / R: El catálogo de refactorizaciones, corazón del libro, que recuerda cómo ejecutar cada refactorización de forma segura y paso a paso (por ejemplo, Replace Conditional with Polymorphism).

P: ¿Por qué todos los ejemplos están en Java? / R: Porque es el lenguaje que Fowler conoce mejor y es cada vez más conocido y comprensible para quien tiene base en C y orientado a objetos, aunque el refactoring aplica a otros lenguajes.

P: ¿Qué temas quedan fuera del alcance de estas refactorizaciones? / R: La programación concurrente y la distribuida; además se evitan áreas complejas de Java como inner classes, reflection y threads.

P: ¿Quiénes son citados como fundadores del campo? / R: Ward Cunningham, Kent Beck, Ralph Johnson, Bill Opdyke, John Brant y Don Roberts.

P: ¿Qué sistema real probó el refactoring en producción? / R: El sistema Chrysler Comprehensive Compensation (C3), cuyo equipo se cita extensamente.

## Preguntas de autoevaluación

P: Define refactoring con tus palabras y explica su característica distintiva respecto al comportamiento del código. / R: Es cambiar la estructura interna del software mejorándola sin alterar su comportamiento externo; lo distintivo es que mejora el diseño preservando la funcionalidad. (Sección "What Is Refactoring?")

P: ¿Qué enseña la anécdota del consultor que visita el proyecto con la jerarquía desordenada? / R: Que la falta de limpieza del código tiene un coste real: pese a limpiarla en uno o dos días eliminando la mitad del código sin perder funcionalidad, la dirección no quedó contenta y seis meses después el proyecto fracasó por exceso de complejidad; Kent Beck lo reinició con refactorización continua. (Sección "El ejemplo que recorre el capítulo")

P: Según el prólogo, ¿qué recorrido de lectura seguir para "hacer refactoring de verdad"? / R: Leer completos los cuatro primeros capítulos, hojear el catálogo para conocer su contenido, leer en detalle cada refactorización cuando se vaya a aplicar y leer los capítulos invitados, especialmente el 15. (Sección "Who Should Read This Book?")

P: ¿A qué público se dirige el libro y por qué deben entenderlo también arquitectos y diseñadores senior? / R: Al programador profesional que vive de escribir software; arquitectos y diseñadores senior deben entender sus principios porque el refactoring impacta fuertemente en el diseño del sistema. (Sección "Who Should Read This Book?")

P: ¿Qué aportaciones concretas hicieron las personas reconocidas en el campo? / R: Cunningham y Beck fueron de los principales proponentes y lo usaron como parte central de su proceso; Johnson lidera un grupo en la Universidad de Illinois notable por sus contribuciones prácticas; Opdyke escribió el primer trabajo detallado en su tesis doctoral; Brant y Roberts escribieron el Refactoring Browser para Smalltalk. (Sección "Building on the Foundations Laid by Others")

P: ¿De dónde surgió la idea de los "code smells" y la semilla del Capítulo 1? / R: De una conversación con Kent Beck sobre un artículo para el Smalltalk Report, que originó la semilla del Capítulo 1 y el hábito de anotar refactorizaciones; Kent aportó la idea de los "code smells". (Sección "Acknowledgments")

P: ¿Por qué el autor evita rasgos complejos de Java en los ejemplos? / R: Para comunicar mejor las ideas y centrarse en las refactorizaciones esenciales, evitando inner classes, reflection, threads y otras características potentes. (Sección "Refactoring in Java")

## Puntos a dominar

- Entender la definición de refactoring: mejora de la estructura interna sin cambiar el comportamiento externo.
- Explicar por qué el refactoring invierte la idea de decaimiento del software y permite que el diseño sea continuo.
- Reconocer que cada refactorización es un paso pequeño cuyo efecto acumulado mejora radicalmente el diseño.
- Conocer la organización del libro: ejemplo inicial (cap. 1), principios (cap. 2), bad smells (cap. 3), pruebas (cap. 4) y catálogo (caps. 5-12).
- Saber elegir el recorrido de lectura según el objetivo (qué es, por qué, dónde, o hacer refactoring de verdad).
- Tener presente el alcance: ejemplos en Java, sin cubrir programación concurrente ni distribuida.
- Identificar a los fundadores del campo y el papel del sistema C3 como prueba en producción.
