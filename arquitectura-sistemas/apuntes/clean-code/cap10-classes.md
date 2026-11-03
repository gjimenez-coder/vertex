# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 10 — Classes (Clases)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Tras dedicar los capítulos previos a escribir buenas líneas, funciones y bloques, este capítulo (escrito con Jeff Langr) sube al siguiente nivel de organización: la clase. La tesis central es que el código no está limpio hasta que atendemos a este nivel superior de estructura, y la regla primaria para diseñar clases —igual que con las funciones— es que sean pequeñas.

A diferencia de las funciones, el tamaño de una clase no se mide contando líneas físicas sino contando responsabilidades. De ahí que el capítulo gire en torno al Single Responsibility Principle (SRP), la cohesión y a cómo organizar el sistema para resistir el cambio.

Sales sabiendo cómo organizar una clase según la convención estándar de Java, por qué preferimos muchas clases pequeñas a pocas grandes, cómo detectar violaciones del SRP, qué significa alta cohesión y cómo aplicar el Open-Closed Principle (OCP) y el Dependency Inversion Principle (DIP) para aislar el sistema del cambio.

## Organización de la clase (Class Organization)

Siguiendo la convención estándar de Java, una clase empieza con la lista de variables: primero las constantes públicas estáticas, luego las variables privadas estáticas y finalmente las variables de instancia privadas. Rara vez hay una buena razón para tener una variable pública.

Las funciones públicas van tras la lista de variables. Las utilidades privadas que llama una función pública se colocan justo después de esa función, siguiendo la stepdown rule para que el programa se lea como un artículo de periódico.

### Encapsulamiento (Encapsulation)

Se prefiere mantener variables y utilidades privadas, pero sin fanatismo. A veces hay que hacer una variable o función `protected` o de ámbito de paquete para que un test la alcance: "para nosotros, mandan los tests". Aun así, primero se busca mantener la privacidad; relajar el encapsulamiento es siempre el último recurso.

## Las clases deben ser pequeñas (Classes Should Be Small!)

La primera regla de las clases es que sean pequeñas; la segunda, que sean aún más pequeñas. El tamaño se mide por responsabilidades. La clase `SuperDashboard`, con unos 70 métodos públicos, es un ejemplo de "God class" con demasiadas responsabilidades. Pero incluso una versión reducida a cinco métodos (Listing 10-2) sigue teniendo demasiadas responsabilidades: pocos métodos no garantizan una clase pequeña.

El nombre de la clase ayuda a determinar su tamaño: si no podemos derivar un nombre conciso, probablemente es demasiado grande. Nombres ambiguos con palabras comodín como `Processor`, `Manager` o `Super` delatan una agregación desafortunada de responsabilidades. Otra prueba: describir la clase en unas 25 palabras sin usar "if", "and", "or" o "but". El primer "and" que aparezca es señal de exceso de responsabilidades.

### El Single Responsibility Principle (SRP)

El SRP establece que una clase o módulo debe tener una, y solo una, razón para cambiar. Esto da a la vez una definición de responsabilidad y una guía de tamaño. `SuperDashboard` (Listing 10-2) tiene dos razones para cambiar: gestiona información de versión y gestiona componentes Swing. Identificar esas responsabilidades permite extraer una clase `Version` reutilizable (Listing 10-3).

El SRP es uno de los conceptos más importantes del diseño OO y uno de los más sencillos de entender, pero también de los más abusados. La causa: hacer que el software funcione y hacerlo limpio son actividades distintas, y muchos creemos haber terminado cuando el programa funciona, sin volver a descomponer las clases sobrecargadas en unidades desacopladas con una sola responsabilidad.

Frente al temor de que muchas clases pequeñas dificulten ver el panorama general, el autor responde que un sistema con muchas clases pequeñas no tiene más piezas móviles que uno con pocas clases grandes. La analogía es la caja de herramientas: cajones pequeños bien etiquetados frente a unos pocos cajones donde se tira todo. Queremos sistemas compuestos de muchas clases pequeñas, cada una con una responsabilidad única, una razón para cambiar y que colabore con unas pocas más.

### Cohesión (Cohesion)

Las clases deben tener pocas variables de instancia, y cada método debería manipular una o más de ellas. Cuantas más variables manipula un método, más cohesivo es respecto a su clase. Una clase donde cada variable es usada por cada método es máximamente cohesiva; eso no suele ser posible ni aconsejable, pero buscamos cohesión alta: que métodos y variables sean codependientes y formen un todo lógico. El `Stack` del Listing 10-4 es muy cohesivo (solo `size()` no usa ambas variables).

Mantener funciones pequeñas y listas de parámetros cortas puede provocar una proliferación de variables de instancia usadas solo por un subconjunto de métodos; eso casi siempre significa que hay otra clase intentando salir. En ese caso hay que separar variables y métodos en clases más cohesivas.

### Mantener la cohesión produce muchas clases pequeñas

Al partir una función grande en funciones pequeñas, el código extraído puede usar variables locales. Promoverlas a variables de instancia evita pasarlas como argumentos, pero hace que la clase pierda cohesión. Si unas pocas funciones comparten ciertas variables, forman una clase por derecho propio: cuando una clase pierde cohesión, hay que dividirla.

El ejemplo del `PrintPrimes` de Knuth (Listing 10-5) muestra una única función enredada, con anidamiento profundo y variables extrañas. Refactorizada (Listings 10-6 a 10-8) se divide en tres responsabilidades: `PrimePrinter` (maneja el entorno de ejecución), `RowColumnPagePrinter` (formatea números en páginas con filas y columnas) y `PrimeGenerator` (genera los primos). El programa resulta más largo por nombres descriptivos, por usar declaraciones de clase y función como comentario, y por el uso de espacio en blanco. No fue una reescritura: se escribió un test que verificaba el comportamiento del primer programa y se aplicaron muchísimos cambios diminutos, ejecutando tras cada uno para confirmar que el comportamiento no cambiaba.

## Organizar para el cambio (Organizing for Change)

En la mayoría de sistemas el cambio es continuo, y cada cambio arriesga romper el resto. La clase `Sql` (Listing 10-9) genera cadenas SQL; debe cambiar al añadir un nuevo tipo de sentencia y también al alterar el detalle de una sentencia existente (por ejemplo, soportar subselects), dos razones que violan el SRP. Un método privado que aplica solo a un subconjunto de la clase (como `selectWithCriteria`) es una heurística útil para detectar mejoras, pero el detonante principal para actuar debe ser el cambio real: si la clase está lógicamente completa, se deja en paz; en cuanto nos vemos "abriendo" la clase, conviene arreglar el diseño.

La solución (Listing 10-10) convierte `Sql` en una clase abstracta y refactoriza cada método de interfaz a su propia derivada (`CreateSql`, `SelectSql`, `InsertSql`, etc.), moviendo los métodos privados a donde se necesitan y aislando el comportamiento común en clases de utilidad (`Where`, `ColumnList`). Cada clase queda simplísima, el tiempo de comprensión cae casi a cero y el riesgo de que una función rompa otra se vuelve ínfimo. Al añadir sentencias `update`, ninguna clase existente cambia: se añade una nueva subclase `UpdateSql`. Esto cumple el SRP y también el Open-Closed Principle (OCP): las clases deben estar abiertas a la extensión pero cerradas a la modificación.

### Aislarse del cambio (Isolating from Change)

Una clase cliente que depende de detalles concretos corre riesgo cuando esos detalles cambian. Interfaces y clases abstractas ayudan a aislar ese impacto. Si `Portfolio` dependiera directamente de la API `TokyoStockExchange`, sería difícil de testear por la volatilidad de la cotización. En su lugar se crea una interfaz `StockExchange` con un método `currentPrice(String symbol)`; `TokyoStockExchange` la implementa y el constructor de `Portfolio` recibe una referencia a `StockExchange`. Así el test usa una implementación de prueba (`FixedStockExchangeStub`) que fija valores conocidos.

Un sistema desacoplado de esta forma es más flexible y reutilizable, y queda mejor aislado del cambio. Al minimizar el acoplamiento, las clases cumplen el Dependency Inversion Principle (DIP): deben depender de abstracciones, no de detalles concretos. `Portfolio` pasa a depender de la abstracción `StockExchange`, que representa el concepto de pedir el precio actual de un símbolo, aislando de dónde se obtiene.

## Ideas clave

- El tamaño de una clase se mide en responsabilidades, no en líneas; y más pequeña es mejor.
- Convención de organización: constantes públicas, variables privadas estáticas, variables de instancia privadas, funciones públicas y sus utilidades privadas debajo (stepdown rule).
- El SRP exige una única razón para cambiar; nombres comodín (`Manager`, `Processor`, `Super`) y el test de "describir en 25 palabras sin and/or/if/but" delatan su violación.
- Preferir muchas clases pequeñas y cohesivas a pocas grandes: no hay más piezas, solo mejor organizadas.
- Alta cohesión significa que métodos y variables se sostienen como un todo lógico; cuando se pierde, hay que dividir la clase.
- Refactorizar no es reescribir: con un test que fija el comportamiento, se avanza con cambios diminutos verificados uno a uno.
- El OCP busca sistemas que se amplían por extensión (subclases) sin modificar código existente.
- El DIP aísla del cambio haciendo que las clases dependan de abstracciones (interfaces) y no de detalles concretos, lo que además facilita el testeo.
