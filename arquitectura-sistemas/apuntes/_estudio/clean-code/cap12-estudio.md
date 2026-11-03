# Emergence (Emergencia) — Estudio

## Tarjetas de repaso

P: ¿Qué propone la idea de diseño emergente en este capítulo? / R: Que existen reglas simples que, seguidas mientras programas, ayudan a que surja un buen diseño por sí solo.

P: ¿Cuáles son las cuatro reglas del Diseño Simple de Kent Beck, en orden de importancia? / R: Ejecuta todas las pruebas, no contiene duplicación, expresa la intención del programador y minimiza el número de clases y métodos.

P: ¿Qué principios refuerza seguir el Diseño Simple? / R: Empuja al programador a respetar principios como SRP y DIP.

P: ¿Por qué la testeabilidad empuja hacia clases pequeñas? / R: Porque es más fácil probar clases que respetan el SRP, así que escribir más pruebas tiende hacia lo simple de probar.

P: ¿Cómo lleva escribir más pruebas a reducir el acoplamiento? / R: El acoplamiento fuerte dificulta las pruebas, así que escribir más pruebas nos lleva a usar DIP, inyección de dependencias, interfaces y abstracción.

P: Según el capítulo, ¿qué no debería desplegarse nunca? / R: Un sistema que no se puede verificar ("a system that cannot be verified should never be deployed").

P: ¿Qué elimina el tener pruebas al refactorizar? / R: El miedo a que limpiar el código lo rompa.

P: ¿Por qué la duplicación es el enemigo principal del buen diseño? / R: Porque representa trabajo, riesgo y complejidad innecesaria.

P: ¿Qué revela eliminar la duplicación incluso en pocas líneas? / R: Violaciones de SRP, lo que lleva a mover métodos a otras clases y eleva su visibilidad.

P: ¿Qué es la "reutilización en lo pequeño" y para qué sirve? / R: Extraer lo común a nivel mínimo; reduce drásticamente la complejidad y es esencial para la reutilización en lo grande.

P: ¿Para qué sirve el patrón TEMPLATE METHOD según el capítulo? / R: Para eliminar duplicación de nivel más alto, dejando que las subclases rellenen solo el "hueco" que varía.

P: ¿Por qué es importante que el código sea expresivo? / R: Porque la mayor parte del costo está en el mantenimiento a largo plazo y quien mantiene no tendrá nuestra comprensión profunda.

P: ¿Cuáles son las formas de expresarse que menciona el capítulo? / R: Buenos nombres, funciones y clases pequeñas, nomenclatura estándar (nombres de patrones) y pruebas unitarias bien hechas.

P: ¿Cuál es la forma más importante de ser expresivo? / R: Intentarlo: tener orgullo del oficio y dedicar un poco de tiempo a cada función y clase.

P: ¿Por qué la regla de clases y métodos mínimos es la de menor prioridad? / R: Porque importa más tener pruebas, eliminar duplicación y expresarse; los conteos altos suelen venir de dogmatismo sin sentido.

## Preguntas de autoevaluación

P: ¿Cómo mejora una regla tan obvia como "ejecutar todas las pruebas" las metas OO del sistema? / R: Hacer el sistema testeable lo empuja hacia clases pequeñas de un solo propósito y a minimizar el acoplamiento, mejorando bajo acoplamiento y alta cohesión. (Sección: Simple Design Rule 1: Runs All the Tests)

P: ¿En qué consiste el ciclo de refactorización incremental que describe el capítulo? / R: Tras añadir unas pocas líneas se hace una pausa para reflexionar si se degradó el diseño; si fue así se limpia y se ejecutan las pruebas para demostrar que nada se rompió. (Sección: Simple Design Rules 2–4: Refactoring)

P: ¿Qué conocimiento de diseño se aplica durante el paso de refactorización? / R: Aumentar cohesión, reducir acoplamiento, separar responsabilidades, modularizar, encoger funciones y clases, y elegir mejores nombres, junto con las tres últimas reglas. (Sección: Simple Design Rules 2–4: Refactoring)

P: En el ejemplo de VacationPolicy, ¿cómo se aplica TEMPLATE METHOD? / R: Se crea una clase abstracta con accrueVacation() que llama a calculateBaseVacationHours(), alterForLegalMinimums() (abstracto) y applyToPayroll(); las subclases US y EU rellenan solo lo que varía. (Sección: No Duplication)

P: ¿Por qué el código debe expresar la intención de su autor? / R: Porque el costo mayoritario es el mantenimiento y quien mantiene no tendrá la comprensión profunda del problema; más claridad reduce el tiempo de entendimiento, los defectos y el costo. (Sección: Expressive)

P: ¿De dónde suelen venir los conteos altos de clases y métodos, y cómo evitarlos? / R: Del dogmatismo sin sentido (p. ej. exigir una interfaz por clase o separar siempre datos y comportamiento); se evitan resistiendo el dogma y adoptando un enfoque pragmático. (Sección: Minimal Classes and Methods)

P: ¿Pueden las prácticas simples reemplazar la experiencia, según la conclusión? / R: No, pero son una forma cristalizada de décadas de experiencia que permite adherir a buenos principios y patrones que de otro modo tardarían años en aprenderse. (Sección: Conclusión)

## Puntos a dominar

- Recordar las cuatro reglas del Diseño Simple de Kent Beck en su orden de prioridad.
- Explicar por qué la testeabilidad conduce a SRP y a bajo acoplamiento (DIP, inyección de dependencias).
- Describir el ciclo escribir–pausar–refactorizar–probar y el papel de las pruebas para eliminar el miedo a romper el código.
- Reconocer las formas de duplicación y cómo la "reutilización en lo pequeño" habilita la reutilización en lo grande.
- Aplicar TEMPLATE METHOD para eliminar duplicación de alto nivel dejando variar solo lo necesario.
- Enumerar las vías de expresividad y recordar que la principal es intentarlo con orgullo del oficio.
- Mantener un enfoque pragmático que evite el dogmatismo que multiplica clases y métodos.
