# Software Engineering Best Practices (Buenas prácticas de ingeniería de software) — Estudio

## Tarjetas de repaso

P: Según Cady, ¿cuál es la habilidad que más falta a los data scientists? / R: Escribir código decente: mantener unos cientos de líneas claras y manejables durante un proyecto, no rutinas numéricas optimizadas ni librerías sofisticadas.

P: ¿De qué trata realmente el estilo de código? / R: No de escribir rápido ni de que el código sea correcto, sino de hacerlo fácil de leer y entender para otros y para tu yo futuro.

P: ¿Qué principios básicos de buen estilo enumera el capítulo? / R: Nombres descriptivos, modularidad, evitar indentación excesiva, usar comentarios con mesura, refactorizar bloques duplicados y separar el boilerplate de la lógica central.

P: ¿Cuál es la diferencia entre código de análisis y código de producción? / R: El objetivo de la calidad general es que alguien pueda leerlo y entenderlo; el del código de producción es hacer innecesaria esa comprensión mediante APIs intuitivas, documentadas y flexibles.

P: ¿Qué es un sistema de control de versiones y qué ventajas da? / R: Un marco que rastrea cambios en una base de código y los sincroniza con una copia maestra en un servidor; respalda el código, sincroniza equipos y permite volver a una versión que funcionaba.

P: ¿Para qué sirven las ramas (branches)? / R: Para trabajar sin contaminar la rama master y fusionar al final, y para versiones puntuales con fines especiales (p. ej., una versión personalizada para un cliente).

P: ¿Qué hace el comando `git clone`? / R: Clona la rama master de un repositorio, descargando la base de código como un directorio en tu máquina.

P: ¿Qué cubren las pruebas unitarias? / R: Piezas pequeñas y autocontenidas de lógica, incluyendo todos los casos límite conocidos más varios casos generales, probando cada módulo de forma aislada.

P: ¿Qué es un mock y cuándo se usa? / R: Un objeto que imita la API de un recurso externo de forma predefinida; se usa en pruebas unitarias para evitar acceder a recursos externos reales (Internet, MySQL remoto, otros procesos).

P: ¿Qué son las pruebas de integración? / R: Pruebas donde los módulos se enlazan entre sí y se usan recursos externos reales ejecutando el sistema de forma realista, para detectar errores que solo surgen a escala.

P: ¿En qué consiste el test-driven development (TDD)? / R: Escribir las pruebas unitarias del módulo antes del código fuente y programar con el único objetivo de hacerlas pasar una a una sin romper las anteriores.

P: ¿Por qué TDD no siempre encaja en data science? / R: Porque solo es apropiado si sabes qué debe hacer el software, y a menudo no se sabe qué extracciones de features y preprocesamiento funcionarán hasta jugar con los datos.

P: ¿Qué es la metodología AGILE y de dónde viene? / R: Es cómo se organizan los equipos de desarrolladores; el término se acuñó en 2001 en "The Manifesto for Agile Software Development" por programadores hartos de planes de arriba abajo que fracasaban.

P: ¿Qué es un stand-up o scrum diario? / R: Una reunión matinal donde cada miembro dice qué logró ayer, qué planea hacer hoy y qué obstáculos tiene.

P: ¿Qué es el technical debt en AGILE? / R: La desorganización e inestabilidades que se acumulan por el foco en iterar features rápido y que vuelven a morderte después.

## Preguntas de autoevaluación

P: ¿Por qué muchos genios de física o matemáticas nunca desarrollaron la destreza de escribir buen código? / R: Porque jamás escribieron más de unas docenas de líneas ni tuvieron que volver a su código a actualizarlo; es una destreza aprendida. (Sección "Lo que necesitas saber")

P: Menciona tres "pecados" de estilo que critica Cady en su ejemplo. / R: Nombres de variables sin significado, hard-codear la URL en vez de exponerla como parámetro, usar un `try–except` para comprobar si una variable ya existe, o tres `if` mutuamente excluyentes que deberían ser `elif` (también indentación irregular y un nombre de clase poco útil como `Parser`). (Sección "Estilo de código")

P: ¿Por qué el capítulo advierte de no abusar de los comentarios? / R: Porque distraen, pueden quedar desactualizados o ser erróneos; si el código habla por sí mismo, conviene omitirlos. (Sección "Estilo de código")

P: Además de comprobar que el código es correcto, ¿qué otra ventaja menos obvia tienen las pruebas? / R: El código de prueba suele ser la mejor documentación: muestra cómo llamar al código, qué entra y qué sale, y ejecutarlo verifica que esa documentación está al día. (Sección "Probar el código")

P: ¿Cómo ayudan las pruebas unitarias en el trabajo en equipo con Git? / R: Tras un `git pull` de los cambios ajenos, recompilas y relanzas las pruebas; si pasan, haces push con confianza. (Sección "Pruebas unitarias")

P: ¿Cuáles son las dos grandes ventajas de TDD? / R: (1) Te obliga a pensar de antemano la funcionalidad y a decidir una API preliminar probando si resulta torpe de usar; (2) te permite concentrarte en una sola prueba en vez de sostener todo el sistema en la cabeza. (Sección "Desarrollo guiado por pruebas")

P: ¿Cuál es la idea clave de AGILE y qué tres principios destaca el capítulo? / R: Hacer los proyectos más flexibles acortando el ciclo de desarrollo y estrechando los bucles de feedback; destaca la colaboración y decisiones frecuentes del equipo, la comunicación frecuente con clientes/stakeholders y asegurar siempre un producto funcional de extremo a extremo. (Sección "Metodología AGILE")

P: ¿Qué relación simbiótica describe Cady entre el código fuente y el de prueba? / R: Los ve como dos mitades "en sync" cuando todas las pruebas pasan, ya que es minúsculamente improbable que ambas tengan un bug que se cancele. (Sección "Pruebas unitarias")

## Puntos a dominar

- Entender que la claridad del código es responsabilidad de todo el que lo escribe y que el buen estilo es una mentalidad, no un conjunto de reglas.
- Distinguir código de análisis de código de producción, y qué significa que el código de producción haga innecesaria la comprensión de su interior.
- Reconocer los principios de buen estilo: nombres descriptivos, modularidad, poca indentación, comentarios justos, refactorizar duplicados, separar boilerplate de la lógica.
- Manejar el flujo básico de Git (clone, status, add, commit, push, pull, diff, branch, checkout, merge) y el papel de las ramas y de Github.
- Diferenciar pruebas unitarias (piezas aisladas, casos límite, mocks) de pruebas de integración (módulos y recursos reales enlazados).
- Comprender TDD: escribir pruebas antes del código y cuándo es apropiado (implementar producción) frente a la exploración inicial de datos.
- Conocer los principios de AGILE, el stand-up diario y el riesgo de technical debt.
