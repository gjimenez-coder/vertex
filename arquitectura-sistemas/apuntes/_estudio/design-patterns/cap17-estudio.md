# Prototype (Prototipo) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Prototype y qué permite?
R: Es un patrón de diseño creacional que permite copiar objetos existentes sin que el código dependa de sus clases.

P: ¿Cuál es la idea central del patrón?
R: Delegar el proceso de clonación a los propios objetos que están siendo clonados, en lugar de copiarlos "desde fuera".

P: ¿Qué es un prototipo?
R: Un objeto que soporta la clonación, es decir, que implementa la interfaz común de clonación (normalmente el método `clonar`).

P: ¿Qué problemas tiene copiar un objeto "desde fuera"?
R: Algunos campos pueden ser privados e invisibles; hay que conocer la clase concreta del objeto; y a veces solo se conoce la interfaz, no la clase concreta.

P: ¿Cómo logra el método `clonar` copiar incluso campos privados?
R: La mayoría de los lenguajes permiten a un objeto acceder a los campos privados de otros objetos de la misma clase.

P: ¿Por qué la clonación es una alternativa a la creación de subclases?
R: Cuando hay muchas configuraciones posibles, se crean prototipos prefabricados y se clonan cuando se necesitan, en lugar de construir subclases para cada configuración.

P: ¿Qué analogía del mundo real ilustra mejor el patrón y por qué?
R: La división mitótica de una célula, porque la célula original actúa como prototipo activo que participa en crear una copia idéntica.

P: ¿Qué tres elementos componen la implementación básica?
R: La interfaz Prototipo (declara `clonar`), el Prototipo Concreto (implementa la clonación) y el Cliente (produce copias de cualquier objeto que siga la interfaz).

P: ¿Qué es el Registro de Prototipos y cómo se implementa de forma sencilla?
R: Un almacén de prototipos de uso frecuente listos para copiar; en su forma más simple es una tabla hash con pares `name → prototype`.

P: ¿Por qué cada subclase debe sobrescribir `clonar` con su propio nombre de clase?
R: Para no producir un objeto de la clase madre y obtener un clon de la clase real.

P: ¿Qué papel juega el polimorfismo al clonar una colección de objetos?
R: Garantiza que invocar `clone()` sobre cada referencia ejecute el método de clonación de la clase real, obteniendo los clones adecuados.

P: ¿Por qué el resultado de la clonación es consistente?
R: El método de clonación crea el nuevo objeto y lo pasa al constructor; hasta que este termina, nadie accede a un clon a medio terminar.

P: ¿Cuáles son los pros del patrón Prototype?
R: Clonas sin acoplar a clases concretas, evitas inicialización repetida, creas objetos complejos con facilidad y obtienes una alternativa a la herencia para preajustes de configuración.

P: ¿Cuál es la principal contra del patrón?
R: Clonar objetos complejos con referencias circulares puede resultar complicado.

## Preguntas de autoevaluación

P: ¿Por qué copiar un objeto directamente acopla el código a su clase?
R: Porque para crear el duplicado hay que crear un nuevo objeto de la misma clase y conocerla; además, a veces solo se conoce la interfaz y no la clase concreta. (Sección "Problema")

P: ¿Cómo resuelve Prototype la imposibilidad de copiar campos privados desde fuera?
R: Delega la clonación al propio objeto; dentro de su método `clonar` puede acceder a los campos privados de otros objetos de su misma clase. (Secciones "Problema" y "Solución")

P: En el pseudocódigo de las formas, ¿qué hace el constructor prototipo de una subclase como `Rectangle`?
R: Invoca al constructor padre con `super(source)` para que la superclase copie sus campos y luego copia sus propios campos (`width`, `height`). (Sección "Pseudocódigo")

P: ¿En qué dos situaciones es aplicable el patrón según el capítulo?
R: Cuando el código no debe depender de las clases concretas de los objetos a copiar, y cuando se quiere reducir subclases que solo se diferencian en cómo inicializan sus objetos. (Sección "Aplicabilidad")

P: ¿Qué pasos sigue la implementación del patrón?
R: Crear la interfaz con `clonar`; definir un constructor alternativo que copie los campos (invocando al padre en subclases); escribir `clonar` como una línea con `new` y el constructor prototípico usando el propio nombre de clase; y opcionalmente crear un registro de prototipos. (Sección "Cómo implementarlo")

P: ¿Cómo se relaciona Prototype con Factory Method en cuanto a herencia e inicialización?
R: Prototype no se basa en la herencia (evita sus inconvenientes) pero requiere una inicialización complicada del clon; Factory Method sí se basa en herencia pero no necesita un paso de inicialización. (Sección "Relaciones con otros patrones")

P: ¿Cuándo puede Prototype ser una alternativa más simple a Memento?
R: Cuando el objeto es sencillo y no tiene enlaces a recursos externos. (Sección "Relaciones con otros patrones")

## Puntos a dominar

- Explicar qué es Prototype y por qué desacopla la copia de las clases concretas.
- Identificar las trampas de copiar "desde fuera" (campos privados, dependencia de clase concreta, solo conocer la interfaz).
- Describir la interfaz común con el método `clonar` y el rol del constructor prototipo.
- Distinguir los tres componentes de la implementación básica: Prototipo, Prototipo Concreto y Cliente.
- Entender el Registro de Prototipos como tabla hash `name → prototype` para prototipos frecuentes.
- Justificar por qué cada subclase sobrescribe `clonar` con su propio nombre de clase y cómo actúa el polimorfismo.
- Enumerar pros y la contra (referencias circulares) y las relaciones con Factory Method, Abstract Factory, Composite, Decorator, Command, Memento y Singleton.
