# Refactoring: Improving the Design of Existing Code

Autores: Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) — Addison-Wesley, 1999.

Según los apuntes, el libro presenta la refactorización (refactoring) como el cambio de la estructura interna del código sin alterar su comportamiento externo, una forma disciplinada de limpiar código que minimiza el riesgo de introducir errores. Su tesis es que un buen diseño es esencial para desarrollar con rapidez y que la refactorización impide que el diseño se degrade con el tiempo e incluso lo mejora. La obra combina un ejemplo inicial, los principios, los malos olores del código, la construcción de pruebas y un extenso catálogo de refactorizaciones de referencia, con ejemplos en Java y pasos pequeños verificados con pruebas tras cada cambio.

## Capítulos

- [Capítulo 0 — Preface (Prefacio)](cap00-preface.md): presenta la refactorización como hilo conductor del libro y la motivación de Fowler, a partir de una anécdota de un proyecto rescatado por Kent Beck con limpieza continua.
- [Capítulo 1 — Refactoring, a First Example (Refactorización, un primer ejemplo)](cap01-refactoring-a-first-example.md): un ejemplo que refactoriza un programa partiendo de pruebas sólidas, con pasos pequeños hasta reemplazar la lógica condicional del precio por polimorfismo (patrón State).
- [Capítulo 2 — Principles in Refactoring (Principios de la refactorización)](cap02-principles-in-refactoring.md): define qué es refactorizar, por qué, cuándo y cuándo no, los dos sombreros y su relación con diseño y rendimiento.
- [Capítulo 3 — Bad Smells in Code (Malos olores en el código)](cap03-bad-smells-in-code.md): catálogo de *smells* que indican *cuándo* refactorizar, siendo el código duplicado el peor de todos.
- [Capítulo 4 — Building Tests (Construir pruebas)](cap04-building-tests.md): el código autocomprobable y JUnit como precondición para refactorizar con seguridad y reducir la depuración.
- [Capítulo 5 — Toward a Catalog of Refactorings (Hacia un catálogo de refactorizaciones)](cap05-toward-a-catalog-of-refactorings.md): explica el formato del catálogo (nombre, resumen, motivación, mecánica, ejemplos) y cómo encontrar referencias.
- [Capítulo 6 — Composing Methods (Componer métodos)](cap06-composing-methods.md): refactorizaciones para trocear métodos largos en métodos cortos y bien nombrados, como Extract Method y Replace Temp with Query.
- [Capítulo 7 — Moving Features Between Objects (Mover características entre objetos)](cap07-moving-features-between-objects.md): reubica responsabilidades con Move Method, Move Field, Extract Class y gestión del acoplamiento entre objetos.
- [Capítulo 8 — Organizing Data (Organización de datos)](cap08-organizing-data.md): convierte datos simples en objetos elocuentes, distingue reference y value objects y trata los type codes.
- [Capítulo 9 — Simplifying Conditional Expressions (Simplificación de expresiones condicionales)](cap09-simplifying-conditional-expressions.md): simplifica lógica condicional con Decompose Conditional, guard clauses, polimorfismo y Null Object.
- [Capítulo 10 — Making Method Calls Simpler (Simplificar las llamadas a métodos)](cap10-making-method-calls-simpler.md): mejora las interfaces de los objetos con buenos nombres, listas de parámetros cuidadas y separación consulta/modificador.
- [Capítulo 11 — Dealing with Generalization (Tratar con la generalización)](cap11-dealing-with-generalization.md): trabaja las jerarquías de herencia subiendo y bajando miembros, extrayendo super/subclases e interfaces y alternando herencia y delegación.
- [Capítulo 12 — Big Refactorings (Grandes refactorizaciones)](cap12-big-refactorings.md): cambios de diseño a gran escala sin mecánicas precisas, que se avanzan "mordisqueando los bordes" con acuerdo del equipo.
- [Capítulo 13 — Refactoring, Reuse, and Reality (Refactorización, reutilización y realidad)](cap13-refactoring-reuse-and-reality.md): capítulo de William Opdyke que atiende las preocupaciones prácticas que hacen la refactorización "real", su seguridad y su relación con la reutilización.
- [Capítulo 14 — Refactoring Tools (Herramientas de refactorización)](cap14-refactoring-tools.md): capítulo de Don Roberts y John Brant sobre el soporte de herramientas, con criterios técnicos y prácticos para refactorizar de forma automatizada.
- [Capítulo 15 — Putting It All Together (Juntándolo todo)](cap15-putting-it-all-together.md): capítulo de Kent Beck que cierra el libro enseñando el *ritmo* del refactoring: pasos pequeños, saber parar y los dos sombreros.
