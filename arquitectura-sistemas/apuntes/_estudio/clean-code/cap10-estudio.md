# Classes (Clases) — Estudio

## Tarjetas de repaso

P: ¿Cómo se mide el tamaño de una clase según el capítulo? / R: No contando líneas físicas, sino contando responsabilidades; la primera regla es que las clases sean pequeñas y la segunda, aún más pequeñas.

P: ¿Cuál es la convención estándar de Java para organizar una clase? / R: Primero las constantes públicas estáticas, luego las variables privadas estáticas, después las variables de instancia privadas y por último las funciones públicas.

P: ¿Dónde se colocan las utilidades privadas que llama una función pública? / R: Justo después de esa función, siguiendo la stepdown rule para que el programa se lea como un artículo de periódico.

P: ¿Qué establece el Single Responsibility Principle (SRP)? / R: Que una clase o módulo debe tener una, y solo una, razón para cambiar.

P: ¿Qué es una "God class" y qué ejemplo usa el capítulo? / R: Una clase con demasiadas responsabilidades; el ejemplo es `SuperDashboard`, con unos 70 métodos públicos.

P: ¿Qué señales delatan una violación del SRP? / R: Nombres comodín como `Processor`, `Manager` o `Super`, y no poder describir la clase en unas 25 palabras sin usar "if", "and", "or" o "but".

P: ¿Qué significa que una clase tenga alta cohesión? / R: Que tiene pocas variables de instancia y cada método manipula una o más de ellas, de modo que métodos y variables son codependientes y forman un todo lógico.

P: ¿Qué ocurre cuando una clase pierde cohesión? / R: Casi siempre significa que hay otra clase intentando salir, por lo que hay que dividir variables y métodos en clases más cohesivas.

P: ¿Qué diferencia hay entre refactorizar y reescribir según el ejemplo de PrintPrimes? / R: No fue una reescritura: se escribió un test que fijaba el comportamiento original y se aplicaron muchísimos cambios diminutos, ejecutando tras cada uno para confirmar que el comportamiento no cambiaba.

P: ¿En qué tres responsabilidades se dividió el PrintPrimes de Knuth? / R: `PrimePrinter` (maneja el entorno de ejecución), `RowColumnPagePrinter` (formatea números en páginas con filas y columnas) y `PrimeGenerator` (genera los primos).

P: ¿Qué establece el Open-Closed Principle (OCP)? / R: Que las clases deben estar abiertas a la extensión pero cerradas a la modificación; se amplía el sistema con nuevas subclases sin modificar las clases existentes.

P: ¿Qué establece el Dependency Inversion Principle (DIP)? / R: Que las clases deben depender de abstracciones, no de detalles concretos, lo que aísla del cambio y facilita el testeo.

P: ¿Por qué se introduce la interfaz `StockExchange` en el ejemplo de `Portfolio`? / R: Para que `Portfolio` dependa de una abstracción en vez de la API concreta `TokyoStockExchange`, permitiendo testear con un stub (`FixedStockExchangeStub`) que fija valores conocidos.

P: ¿Cuál es la postura del capítulo sobre el encapsulamiento? / R: Se prefiere mantener variables y utilidades privadas, pero sin fanatismo; relajar el encapsulamiento (p. ej. hacer algo `protected`) para que un test alcance la variable es siempre el último recurso, porque "mandan los tests".

## Preguntas de autoevaluación

P: ¿Garantiza un número bajo de métodos públicos que una clase sea pequeña? / R: No; la versión reducida de `SuperDashboard` a cinco métodos sigue teniendo demasiadas responsabilidades, porque el tamaño se mide por responsabilidades. (Sección: Las clases deben ser pequeñas)

P: ¿Por qué el SRP, siendo sencillo de entender, es de los más abusados? / R: Porque hacer que el software funcione y hacerlo limpio son actividades distintas, y muchos creemos haber terminado cuando el programa funciona, sin descomponer las clases sobrecargadas. (Sección: El Single Responsibility Principle)

P: ¿Cómo responde el autor al temor de que muchas clases pequeñas dificulten ver el panorama general? / R: Un sistema con muchas clases pequeñas no tiene más piezas móviles que uno con pocas grandes; la analogía es la caja de herramientas con cajones pequeños bien etiquetados. (Sección: El Single Responsibility Principle)

P: ¿Qué heurística ayuda a detectar mejoras de diseño en la clase `Sql`, y cuál debe ser el detonante real para actuar? / R: Un método privado que aplica solo a un subconjunto de la clase (como `selectWithCriteria`) es una heurística útil, pero el detonante principal debe ser el cambio real: si la clase está lógicamente completa se deja en paz. (Sección: Organizar para el cambio)

P: Al refactorizar la clase `Sql`, ¿qué pasa cuando se añade la sentencia `update`? / R: Ninguna clase existente cambia: se añade una nueva subclase `UpdateSql`, cumpliendo el OCP. (Sección: Organizar para el cambio)

P: ¿Cómo se relaciona mantener funciones pequeñas con la aparición de nuevas clases? / R: Al partir funciones grandes, las variables locales pueden promoverse a variables de instancia; si unas pocas funciones comparten ciertas variables, forman una clase por derecho propio y hay que dividir. (Sección: Mantener la cohesión produce muchas clases pequeñas)

P: ¿Por qué el programa refactorizado de PrintPrimes resulta más largo que el original? / R: Por los nombres descriptivos, por usar declaraciones de clase y función como comentario y por el uso de espacio en blanco. (Sección: Mantener la cohesión produce muchas clases pequeñas)

P: ¿Qué dos razones para cambiar violan el SRP en la clase `Sql` original? / R: Debe cambiar al añadir un nuevo tipo de sentencia y también al alterar el detalle de una sentencia existente (por ejemplo, soportar subselects). (Sección: Organizar para el cambio)

## Puntos a dominar

- El tamaño de una clase se mide en responsabilidades, no en líneas; más pequeña es mejor.
- Convención de organización: constantes públicas, variables privadas estáticas, variables de instancia privadas, funciones públicas y utilidades privadas debajo (stepdown rule).
- Aplicar el SRP: una única razón para cambiar; desconfiar de nombres comodín (`Manager`, `Processor`, `Super`) y usar el test de describir en 25 palabras sin and/or/if/but.
- Reconocer la alta cohesión y dividir la clase cuando se pierde.
- Refactorizar con respaldo de tests y cambios diminutos verificados, sin reescribir.
- Aplicar OCP (extensión sin modificación) y DIP (depender de abstracciones, no de detalles concretos) para aislar del cambio y facilitar el testeo.
