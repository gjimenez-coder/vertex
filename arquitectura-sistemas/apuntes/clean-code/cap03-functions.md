# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 3 — Functions (Funciones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber
Las funciones son la primera línea de organización de cualquier programa, y escribirlas bien es el objetivo del capítulo. La tesis central es que una función debe ser pequeña, hacer una sola cosa y a un único nivel de abstracción, de modo que el código se lea como una narrativa descendente. Martin sostiene estas reglas desde la experiencia, no desde investigación formal.

Sales sabiendo cómo encoger funciones mediante extracción de métodos y renombrado, cómo mantener un nivel de abstracción consistente, cómo tratar los argumentos (cuantos menos, mejor), por qué los efectos secundarios y los argumentos de salida son dañinos, y por qué conviene separar comandos de consultas y preferir excepciones a códigos de error. El cierre es una idea mayor: programar es diseñar un lenguaje específico del dominio donde las funciones son los verbos y las clases los sustantivos, y los buenos programadores piensan los sistemas como historias por contar.

## El ejemplo que recorre el capítulo
El hilo conductor es la función `testableHtml` de `HtmlUtil.java` de FitNesse (Listing 3-1): larga, con código duplicado, cadenas raras y `if` doblemente anidados controlados por flags. Mediante extracciones de métodos, renombrados y reestructuración, se convierte en `renderPageWithSetupsAndTeardowns` de nueve líneas (Listing 3-2), y luego en una versión de tres líneas (Listing 3-3). La refactorización completa aparece como `SetupTeardownIncluder.render` (Listing 3-7), donde cada función presenta a la siguiente y se mantiene en un nivel de abstracción consistente.

## Small! (¡Pequeñas!)
La primera regla de las funciones es que deben ser pequeñas; la segunda, que deben ser aún más pequeñas. Las líneas no deberían tener 150 caracteres ni las funciones 100 líneas; rara vez deberían llegar a 20. Martin recuerda el programa Sparkle de Kent Beck, cuyas funciones tenían dos, tres o cuatro líneas, cada una transparente y conducente a la siguiente.

Bloques e indentación: los bloques dentro de `if`, `else`, `while`, etc. deberían ser de una línea, probablemente una llamada a función con nombre descriptivo. Esto implica que una función no debería contener estructuras anidadas: el nivel de indentación no debería superar uno o dos.

## Do One Thing (Hacer una sola cosa)
Regla clásica de más de 30 años: las funciones deben hacer una cosa, hacerla bien, y hacerla solo ellas. El problema es saber qué es "una cosa". Una función hace una sola cosa si sus pasos están todos un nivel de abstracción por debajo de su nombre; de hecho, escribir funciones sirve para descomponer un concepto mayor (el nombre) en pasos del siguiente nivel. Otra señal de que hace más de una cosa es poder extraer de ella otra función con un nombre que no sea una mera reformulación de su implementación.

Secciones dentro de funciones: dividir una función en secciones (declaraciones, inicializaciones, etc.) es síntoma de hacer más de una cosa. Las funciones que hacen una sola cosa no pueden dividirse en secciones.

## One Level of Abstraction per Function (Un nivel de abstracción por función)
Todas las sentencias de una función deben estar al mismo nivel de abstracción. Mezclar niveles (p. ej. `getHtml()` alto, `PathParser.render(pagePath)` intermedio y `.append("\n")` bajo) confunde al lector.

Regla del descenso (Stepdown Rule): el código debe leerse como una narrativa de arriba hacia abajo, donde cada función va seguida por las del siguiente nivel de abstracción, como un conjunto de párrafos "TO" que descienden un nivel a la vez.

## Switch Statements (Sentencias switch)
Es difícil hacer un `switch` pequeño o que haga una sola cosa; por naturaleza hacen N cosas. El ejemplo `calculatePay` (Listing 3-4) es grande, hace más de una cosa, viola el Single Responsibility Principle (SRP) y el Open Closed Principle (OCP). La solución (Listing 3-5) es enterrar el `switch` en un ABSTRACT FACTORY que crea instancias de `Employee`, y despachar funciones como `calculatePay`, `isPayday` y `deliverPay` polimórficamente. Regla general: un `switch` se tolera si aparece una sola vez, crea objetos polimórficos y queda oculto tras una relación de herencia.

## Use Descriptive Names (Usar nombres descriptivos)
Un buen nombre vale mucho. Principio de Ward: "You know you are working on clean code when each routine turns out to be pretty much what you expected" (PDF p. 70). Cuanto más pequeña y enfocada es una función, más fácil es nombrarla. No temer nombres largos: un nombre largo y descriptivo es mejor que uno corto y enigmático, y mejor que un comentario. Probar varios nombres (los IDEs facilitan renombrar) y ser consistente con frases, sustantivos y verbos, de modo que la secuencia cuente una historia.

## Function Arguments (Argumentos de función)
El número ideal de argumentos es cero (niládica), luego uno (monádica) y dos (diádica). Tres (triádica) deben evitarse; más de tres requieren justificación muy especial y aun así no deberían usarse. Los argumentos cuestan carga conceptual y complican las pruebas. Los argumentos de salida son más difíciles de entender que los de entrada.

- Formas monádicas comunes: hacer una pregunta sobre el argumento (`boolean fileExists("MyFile")`), operar y transformarlo devolviéndolo (`InputStream fileOpen("MyFile")`), o interpretarlo como un evento (`void passwordAttemptFailedNtimes(int attempts)`). Evitar monádicas que no sigan estas formas.
- Argumentos flag: pasar un booleano es una práctica terrible; proclama que la función hace más de una cosa. `render(true)` debería dividirse en `renderForSuite()` y `renderForSingleTest()`.
- Diádicas: más difíciles que las monádicas (`writeField(name)` vs `writeField(outputStream, name)`). Son razonables cuando los dos argumentos son componentes ordenados de un solo valor (`new Point(0,0)`). Incluso `assertEquals(expected, actual)` cuesta por el orden.
- Triádicas: más difíciles aún; pensarlo mucho antes de crearlas.
- Objetos argumento: cuando se necesitan muchos argumentos, agrupar varios en una clase (`makeCircle(Point center, double radius)`).
- Listas de argumentos: los argumentos variables tratados igual equivalen a un solo argumento tipo `List`; así `String.format` es en realidad diádica.
- Verbos y keywords: formar pares verbo/sustantivo (`writeField(name)`); la forma keyword codifica los nombres de los argumentos (`assertExpectedEqualsActual`).

## Have No Side Effects (No tener efectos secundarios)
Los efectos secundarios son mentiras: la función promete una cosa pero hace otras ocultas. En `checkPassword` (Listing 3-6), la llamada a `Session.initialize()` es un efecto secundario que crea un acoplamiento temporal (solo puede llamarse cuando es seguro inicializar la sesión). Si el acoplamiento temporal es inevitable, debe quedar claro en el nombre (`checkPasswordAndInitializeSession`), aunque eso viole "hacer una sola cosa".

Argumentos de salida: deben evitarse; en lenguajes OO `this` actúa como argumento de salida, así que `report.appendFooter()` es mejor que `appendFooter(report)`. Si una función debe cambiar un estado, que cambie el de su objeto contenedor.

## Command Query Separation (Separación comando/consulta)
Una función debe hacer algo o responder algo, pero no ambas. `if (set("username", "unclebob"))` es ambiguo (¿comprueba o asigna?). La solución es separar comando de consulta:
```java
if (attributeExists("username")) {
  setAttribute("username", "unclebob");
  ...
}
```

## Prefer Exceptions to Returning Error Codes (Preferir excepciones a códigos de error)
Devolver códigos de error viola sutilmente la separación comando/consulta y obliga al llamador a tratar el error de inmediato, generando estructuras muy anidadas. Usar excepciones permite separar el código de error del camino feliz con un `try/catch`.

- Extraer bloques try/catch: sacar los cuerpos de `try` y `catch` a funciones propias (`delete` que llama a `deletePageAndAllReferences` y `logError`).
- El manejo de errores es una sola cosa: si una función tiene `try`, debe ser la primera palabra y no debe haber nada tras los bloques `catch/finally`.
- El imán de dependencias `Error.java`: una clase/enum de códigos de error es un imán de dependencias; cambiarla obliga a recompilar y redesplegar muchas clases, lo que presiona a reutilizar códigos viejos. Las excepciones, al ser derivadas, se añaden sin forzar recompilación (ejemplo del OCP).

## Don't Repeat Yourself (No te repitas)
En el Listing 3-1 un mismo algoritmo se repite cuatro veces (SetUp, SuiteSetUp, TearDown, SuiteTearDown). La duplicación hincha el código y multiplica el riesgo de error de omisión; se remedia con el método `include`. La duplicación puede ser la raíz de todos los males del software: las formas normales de Codd, la OOP, la programación estructurada, aspectual y por componentes son, en parte, estrategias para eliminarla.

## Structured Programming (Programación estructurada)
Las reglas de Dijkstra (una entrada y una salida; un solo `return`, sin `break`/`continue`/`goto`) aportan poco cuando las funciones son muy pequeñas. En funciones pequeñas, un `return`, `break` o `continue` ocasional no hace daño y puede ser más expresivo; `goto` solo tiene sentido en funciones grandes, así que debe evitarse.

## How Do You Write Functions Like This? (¿Cómo se escriben así?)
Como cualquier escritura: el primer borrador sale largo, anidado y con nombres arbitrarios y duplicación, pero respaldado por una suite de pruebas unitarias. Luego se refina —extraer funciones, renombrar, eliminar duplicación, acortar y reordenar métodos, a veces extraer clases— manteniendo las pruebas en verde. Nadie escribe funciones limpias desde el principio.

## Conclusion (Conclusión)
Todo sistema se construye con un lenguaje específico del dominio diseñado por los programadores: las funciones son los verbos y las clases los sustantivos. El arte de programar es el arte del diseño de lenguaje. Los maestros piensan los sistemas como historias a contar. Este capítulo trató la mecánica de escribir bien las funciones, pero el objetivo real es contar la historia del sistema con un lenguaje claro y preciso.

## Ideas clave
- Las funciones deben ser pequeñas, con indentación de uno o dos niveles y bloques de una línea.
- Deben hacer una sola cosa: solo los pasos un nivel de abstracción por debajo de su nombre.
- Mantener un único nivel de abstracción y leer el código de arriba abajo (Stepdown Rule).
- Menos argumentos es mejor (0 > 1 > 2 > 3); evitar flags y argumentos de salida.
- Sin efectos secundarios: no crear acoplamientos temporales ocultos.
- Separar comando de consulta y preferir excepciones a códigos de error; el manejo de errores es una sola cosa.
- No repetirse: la duplicación es la raíz de muchos males.
- Programar es diseñar un lenguaje; piensa el sistema como una historia por contar.
