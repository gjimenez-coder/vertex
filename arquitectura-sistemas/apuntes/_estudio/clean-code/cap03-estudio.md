# Functions (Funciones) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la primera y la segunda regla de las funciones?
R: La primera es que deben ser pequeñas; la segunda, que deben ser aún más pequeñas (rara vez más de 20 líneas).

P: ¿Qué nivel de indentación debería tener una función y cómo deberían ser sus bloques?
R: El nivel de indentación no debería superar uno o dos; los bloques dentro de `if`, `else`, `while`, etc. deberían ser de una línea, probablemente una llamada a función con nombre descriptivo.

P: ¿Cuándo hace una función "una sola cosa"?
R: Cuando todos sus pasos están un nivel de abstracción por debajo de su nombre; si se puede extraer otra función cuyo nombre no sea una mera reformulación de su implementación, hace más de una cosa.

P: ¿Qué dice la regla de un nivel de abstracción por función?
R: Todas las sentencias de una función deben estar al mismo nivel de abstracción; mezclar niveles alto, intermedio y bajo confunde al lector.

P: ¿Qué es la Stepdown Rule (regla del descenso)?
R: El código debe leerse como una narrativa de arriba hacia abajo, donde cada función va seguida por las del siguiente nivel de abstracción, descendiendo un nivel a la vez.

P: ¿Por qué los `switch` son problemáticos y cuándo se toleran?
R: Por naturaleza hacen N cosas y violan SRP y OCP; se toleran si aparecen una sola vez, crean objetos polimórficos y quedan ocultos tras una relación de herencia (p. ej. en un ABSTRACT FACTORY).

P: ¿Cuál es el número ideal de argumentos de una función y su orden de preferencia?
R: Cero (niládica) es lo ideal, luego uno (monádica) y dos (diádica); tres deben evitarse y más de tres requieren justificación muy especial.

P: ¿Por qué es mala práctica pasar un argumento flag (booleano)?
R: Proclama que la función hace más de una cosa; `render(true)` debería dividirse en `renderForSuite()` y `renderForSingleTest()`.

P: ¿Qué es un efecto secundario y por qué es dañino?
R: Es una acción oculta que la función hace además de lo que promete; por ejemplo `Session.initialize()` en `checkPassword` crea un acoplamiento temporal. Martin dice que los efectos secundarios son mentiras.

P: ¿En qué consiste la separación comando/consulta?
R: Una función debe hacer algo o responder algo, pero no ambas; `if (set("username", "unclebob"))` es ambiguo y debe separarse en `attributeExists` y `setAttribute`.

P: ¿Por qué se prefieren excepciones a códigos de error?
R: Los códigos de error violan la separación comando/consulta y obligan al llamador a tratar el error de inmediato, generando estructuras muy anidadas; las excepciones separan el error del camino feliz con un `try/catch`.

P: ¿Por qué una clase/enum de códigos de error (`Error.java`) es un imán de dependencias?
R: Cambiarla obliga a recompilar y redesplegar muchas clases, lo que presiona a reutilizar códigos viejos; las excepciones derivadas se añaden sin forzar recompilación (ejemplo del OCP).

P: Según el principio de Ward, ¿cuándo sabes que trabajas con código limpio?
R: "You know you are working on clean code when each routine turns out to be pretty much what you expected" (PDF p. 70).

P: ¿Qué aportan las reglas de programación estructurada de Dijkstra en funciones pequeñas?
R: Poco; en funciones pequeñas un `return`, `break` o `continue` ocasional no hace daño y puede ser más expresivo, aunque `goto` debe evitarse.

P: ¿Cuál es la idea mayor del cierre del capítulo sobre programar?
R: Programar es diseñar un lenguaje específico del dominio donde las funciones son los verbos y las clases los sustantivos; los maestros piensan los sistemas como historias por contar.

## Preguntas de autoevaluación

P: ¿Cómo se transforma la función `testableHtml` a lo largo del capítulo?
R: Mediante extracciones de métodos, renombrados y reestructuración pasa de una función larga y anidada a `renderPageWithSetupsAndTeardowns` de nueve líneas, luego a una de tres líneas, y a la refactorización completa `SetupTeardownIncluder.render`. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué señales indican que una función hace más de una cosa?
R: Que se pueda extraer de ella otra función con un nombre que no sea una mera reformulación de su implementación, y que se pueda dividir en secciones (declaraciones, inicializaciones, etc.). (Sección: Do One Thing)

P: ¿Por qué el ejemplo `calculatePay` (Listing 3-4) es problemático y cómo se resuelve?
R: Es grande, hace más de una cosa y viola SRP y OCP; se resuelve enterrando el `switch` en un ABSTRACT FACTORY que crea instancias de `Employee` y despachando funciones polimórficamente. (Sección: Switch Statements)

P: ¿Cuándo es razonable una función diádica y qué coste tiene?
R: Es razonable cuando los dos argumentos son componentes ordenados de un solo valor (p. ej. `new Point(0,0)`); aun así cuesta por el orden, como en `assertEquals(expected, actual)`. (Sección: Function Arguments)

P: ¿Cómo deben tratarse los argumentos de salida en lenguajes orientados a objetos?
R: Deben evitarse; `this` actúa como argumento de salida, así que `report.appendFooter()` es mejor que `appendFooter(report)`: si una función debe cambiar un estado, que cambie el de su objeto contenedor. (Sección: Have No Side Effects)

P: ¿Qué reglas aplican al manejo de errores dentro de una función?
R: El manejo de errores es una sola cosa: si una función tiene `try`, debe ser la primera palabra y no debe haber nada tras los bloques `catch/finally`; conviene extraer los cuerpos de `try` y `catch` a funciones propias. (Sección: Prefer Exceptions to Returning Error Codes)

P: ¿Qué papel juega la duplicación según el capítulo?
R: Puede ser la raíz de todos los males del software; en el Listing 3-1 un mismo algoritmo se repite cuatro veces y se remedia con el método `include`. Formas normales de Codd, OOP y la programación estructurada, aspectual y por componentes son en parte estrategias para eliminarla. (Sección: Don't Repeat Yourself)

P: Según el capítulo, ¿cómo se llega a escribir funciones limpias?
R: Como cualquier escritura: el primer borrador sale largo, anidado y con duplicación pero respaldado por pruebas unitarias; luego se refina extrayendo funciones, renombrando y eliminando duplicación con las pruebas en verde. Nadie las escribe limpias desde el principio. (Sección: How Do You Write Functions Like This?)

## Checklist

- [ ] Mantener las funciones pequeñas (rara vez más de 20 líneas) con indentación de uno o dos niveles.
- [ ] Asegurar que cada función haga una sola cosa: solo pasos un nivel de abstracción por debajo de su nombre.
- [ ] Verificar que todas las sentencias estén en el mismo nivel de abstracción y que el código se lea de arriba abajo (Stepdown Rule).
- [ ] Reducir el número de argumentos (0 > 1 > 2 > 3); eliminar argumentos flag dividiendo la función.
- [ ] Agrupar argumentos múltiples en un objeto cuando sean varios.
- [ ] Eliminar efectos secundarios y acoplamientos temporales ocultos; si son inevitables, reflejarlos en el nombre.
- [ ] Separar comando de consulta: una función hace algo o responde algo, no ambas.
- [ ] Preferir excepciones a códigos de error y extraer los bloques `try/catch` a funciones propias.
- [ ] Eliminar la duplicación de código.
- [ ] Renombrar con nombres descriptivos y consistentes hasta que cada rutina sea lo que se esperaba.
