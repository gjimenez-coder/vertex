# Clean Code: A Handbook of Agile Software Craftsmanship

**Autor:** Robert C. Martin (Prentice Hall, 2008). Con capítulos de colaboradores: Tim Ottinger, Michael Feathers, James Grenning, Jeff Langr, Kevin Dean Wampler y Brett L. Schuchert.

## Descripción general

El libro defiende que el código limpio importa y seguirá importando, y que la forma de quedar del lado correcto cuando el software se complica es la artesanía (*craftsmanship*): conocimiento y práctica inseparables. Se organiza en tres partes: principios y prácticas de código limpio (nombres, funciones, comentarios, formato, objetos y estructuras de datos, manejo de errores, límites, pruebas, clases, sistemas, emergencia y concurrencia), casos de estudio de refactorización real (`Args`, JUnit y `SerialDate`), y una lista de heurísticas y *code smells*. La tesis central es que no basta con que el código funcione: hay que escribir código sucio y luego limpiarlo, aplicando la Regla del Boy Scout de dejar el código más limpio de como se encontró.

## Capítulos

- [Capítulo 0 — Prólogo: Introduction (Introducción)](cap00-introduction.md): plantea la artesanía como respuesta a cómo mantener el código limpio cuando el trabajo se complica.
- [Capítulo 1 — Clean Code (Código limpio)](cap01-clean-code.md): siempre habrá código y la única forma de ir rápido es mantenerlo limpio en todo momento.
- [Capítulo 2 — Meaningful Names (Nombres significativos)](cap02-meaningful-names.md): reglas simples para que los nombres revelen su intención y mejoren la legibilidad.
- [Capítulo 3 — Functions (Funciones)](cap03-functions.md): las funciones deben ser pequeñas, hacer una sola cosa y a un único nivel de abstracción.
- [Capítulo 4 — Comments (Comentarios)](cap04-comments.md): los comentarios son un mal necesario que compensa el fracaso de expresarse en el código.
- [Capítulo 5 — Formatting (Formato)](cap05-formatting.md): el formato es comunicación y la legibilidad sobrevive al código original.
- [Capítulo 6 — Objects and Data Structures (Objetos y estructuras de datos)](cap06-objects-and-data-structures.md): objetos que ocultan datos frente a estructuras de datos que los exponen, dos opuestos complementarios.
- [Capítulo 7 — Error Handling (Manejo de errores)](cap07-error-handling.md): el manejo de errores es necesario pero no debe oscurecer la lógica del código.
- [Capítulo 8 — Boundaries (Límites)](cap08-boundaries.md): cómo integrar limpiamente el software de terceros que no controlamos.
- [Capítulo 9 — Unit Tests (Pruebas unitarias)](cap09-unit-tests.md): el código de prueba es tan importante como el de producción y debe mantenerse igual de limpio.
- [Capítulo 10 — Classes (Clases)](cap10-classes.md): las clases deben ser pequeñas, medirse por responsabilidades y respetar SRP, OCP y DIP.
- [Capítulo 11 — Systems (Sistemas)](cap11-systems.md): separar la construcción del uso y mantener la limpieza al nivel del sistema.
- [Capítulo 12 — Emergence (Emergencia)](cap12-emergence.md): las cuatro reglas del Diseño Simple de Kent Beck que hacen emerger un buen diseño.
- [Capítulo 13 — Concurrency (Concurrencia)](cap13-concurrency.md): por qué la concurrencia es difícil y cómo escribir código concurrente limpio.
- [Capítulo 14 — Successive Refinement (Refinamiento sucesivo)](cap14-successive-refinement.md): caso de estudio de refactorización del parser `Args` por pasos diminutos.
- [Capítulo 15 — JUnit Internals (Interioridades de JUnit)](cap15-junit-internals.md): crítica y refactoring incremental de un fragmento real de JUnit.
- [Capítulo 16 — Refactoring SerialDate (Refactorizando SerialDate)](cap16-refactoring-serialdate.md): revisión profesional y refactorización pública de la clase `SerialDate`.
- [Capítulo 17 — Smells and Heuristics (Olores y heurísticas)](cap17-smells-and-heuristics.md): catálogo de referencia de code smells y heurísticas agrupadas por categorías.
- [Capítulo 18 — Appendix A: Concurrency II (Apéndice A: Concurrencia II)](cap18-appendix-a-concurrency-ii.md): ampliación del capítulo de concurrencia con disciplinas concretas para mantenerla limpia.
- [Capítulo 19 — Epilogue (Epílogo)](cap19-epilogue.md): cierre personal con la anécdota de la pulsera "Test Obsessed" como símbolo de ética profesional.
