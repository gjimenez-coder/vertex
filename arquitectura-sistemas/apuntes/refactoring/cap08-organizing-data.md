# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 8 — Organizing Data (Organización de datos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo reúne una serie de refactorizaciones centradas en cómo se organizan los datos dentro de un programa orientado a objetos. La idea de fondo es que los datos simples (strings, enteros, arrays, campos públicos) tienden, con el tiempo, a necesitar comportamiento y estructura adicionales; estas refactorizaciones permiten convertir "datos tontos" en objetos elocuentes sin romper el código existente.

La tesis central es que el objeto creado a partir de un dato es solo el primer paso: la verdadera ventaja llega cuando se usa Move Method para trasladar comportamiento al nuevo objeto. El capítulo cubre encapsulación (campos, colecciones, registros), la distinción entre objetos de referencia y de valor, la eliminación de números mágicos, la gestión de asociaciones uni/bidireccionales, la separación entre lógica de negocio y GUI, y tres estrategias para tratar los type codes según si afectan o no al comportamiento.

Sales sabiendo cuándo y cómo aplicar cada refactorización, con sus mecánicas paso a paso, y entendiendo los criterios de decisión: acceso directo vs. indirecto a campos, referencia vs. valor, y qué reemplazo de type code corresponde en cada caso.

## Self Encapsulate Field

Accedes a un campo directamente pero el acoplamiento al campo se vuelve incómodo; crea métodos getter y setter y accede al campo solo a través de ellos. Hay dos escuelas: acceso directo (código más fácil de leer, "no necesitas detenerte a decir 'esto es solo un getter'") y acceso indirecto (permite que una subclase sobrescriba la obtención del dato y habilita flexibilidad como la inicialización perezosa). Fowler prefiere el acceso directo como primer recurso hasta que estorba. El momento más importante para aplicarlo es cuando accedes a un campo de una superclase pero quieres sobrescribir ese acceso con un valor calculado en la subclase (ejemplo `IntRange`/`CappedRange`). Cuidado con usar el setter en el constructor: conviene usar acceso directo o un método `initialize` separado.

## Replace Data Value with Object

Tienes un dato que necesita datos o comportamiento adicionales; conviértelo en un objeto. En etapas tempranas representas hechos simples como datos simples (un teléfono como string), pero luego necesitan comportamiento (formateo, extraer prefijo). Cuando el código empieza a oler a duplicación y feature envy, conviertes el valor en objeto. Ejemplo: el campo `_customer` de `Order` pasa de `String` a clase `Customer`. Como regla, los value objects deben ser inmutables para evitar bugs de aliasing.

## Change Value to Reference

Tienes una clase con muchas instancias iguales que quieres sustituir por un único objeto. Los reference objects (cliente, cuenta) representan un objeto del mundo real y se comparan por identidad; los value objects (fecha, dinero) se definen por sus datos y no importa que existan copias. Mecánica: usar Replace Constructor with Factory Method, decidir qué objeto da acceso (un diccionario estático o un registry), decidir si los objetos se crean por adelantado o al vuelo. Ejemplo: `Customer` pasa a tener un `Dictionary` estático de instancias y un método `getNamed`.

## Change Reference to Value

Tienes un objeto de referencia pequeño, inmutable e incómodo de manejar; conviértelo en value object. El disparador es que trabajar con el objeto de referencia se vuelve incómodo (hay que pedirlo al controlador, los enlaces de memoria estorban); los value objects son útiles en sistemas distribuidos y concurrentes. Requisito clave: el objeto debe ser inmutable. Hay que crear `equals` y `hashCode` (con XOR bitwise de los campos). Ejemplo `Currency`: tras definir ambos métodos, `new Currency("USD").equals(new Currency("USD"))` pasa de devolver `false` a `true`, y se puede hacer público el constructor.

## Replace Array with Object

Tienes un array en el que ciertos elementos significan cosas distintas; reemplázalo por un objeto con un campo por elemento. Los arrays deben contener solo colecciones de objetos similares en algún orden; convenciones como "el primer elemento es el nombre" son difíciles de recordar. Ejemplo: `String[] row` con nombre, victorias y derrotas de un equipo pasa a una clase `Performance` con `getName()`/`setWins()`, encapsulando además la conversión de tipos.

## Duplicate Observed Data

Tienes datos de dominio disponibles solo en un control de GUI y los métodos de dominio necesitan acceder; copia los datos a un objeto de dominio y configura un observer para sincronizar ambas copias. Un sistema bien estratificado separa interfaz de usuario de lógica de negocio. El comportamiento se separa fácil, pero los datos no: hay que duplicarlos y sincronizarlos. Fowler normalmente no duplica datos, pero "esto es una excepción que suele ser imposible de evitar". Ejemplo `IntervalWindow` (campos start/end/length): se crea una clase de dominio `Interval extends Observable`, la ventana implementa `Observer`, se aplica Self Encapsulate Field a los campos de la GUI y se usa acceso directo (no el getter) en el event handler y en `update` para evitar recursión infinita. También aplica con event listeners en lugar de observer/observable.

## Change Unidirectional Association to Bidirectional

Dos clases necesitan usar características mutuas pero solo hay un enlace unidireccional; añade back pointers y modifica los setters para actualizar ambos conjuntos. Conviene que una sola clase controle la asociación. Reglas de decisión del controlador: (1) si ambos son reference objects y la asociación es uno a muchos, controla el que tiene la referencia "uno"; (2) si uno es componente del otro, controla el compuesto; (3) si ambos son reference objects y es muchos a muchos, da igual. Patrón del modificador: primero decir al otro objeto que elimine su puntero, luego fijar tu puntero, luego decir al nuevo objeto que añada el puntero. Es un caso raro en que la refactorización añade un test.

## Change Bidirectional Association to Unidirectional

Tienes una asociación de dos vías pero una clase ya no necesita características de la otra; elimina el extremo innecesario. Las asociaciones bidireccionales tienen un precio: complejidad de mantener los dos enlaces, riesgo de "zombies" (objetos que deberían estar muertos pero siguen referenciados) e interdependencia entre clases y paquetes. La parte difícil es comprobar que la eliminación es factible; a menudo se resuelve pasando el objeto como argumento a los métodos que lo usan, o usando Substitute Algorithm en el getter para obtener el objeto sin el puntero. Primero se eliminan los lectores del campo, luego los escritores, luego el campo.

## Replace Magic Number with Symbolic Constant

Tienes un número literal con un significado particular; crea una constante nombrada según el significado y reemplaza el número. Ejemplo: `9.81` pasa a `GRAVITATIONAL_CONSTANT`. Los números mágicos son especialmente nocivos cuando el mismo número lógico aparece en varios sitios. No hay coste de rendimiento al declarar una constante y mejora mucho la legibilidad. Antes de aplicarlo, busca alternativas: si es un type code, considera Replace Type Code with Class; si es la longitud de un array, usa `anArray.length`.

## Encapsulate Field

Hay un campo público; hazlo privado y provee accessors. Uno de los principios de la orientación a objetos es la encapsulación: nunca hagas públicos tus datos, porque otros objetos podrían cambiarlos sin que el objeto propietario se entere, separando datos de comportamiento. Es solo el primer paso: una clase con solo accessors es "tonta"; después conviene buscar métodos que puedan mudarse al objeto con Move Method.

## Encapsulate Collection

Un método devuelve una colección; haz que devuelva una vista de solo lectura y provee métodos add/remove. Las colecciones usan un protocolo distinto: el getter no debe devolver la colección en sí (permitiría manipularla sin que el propietario se entere y revela la estructura interna), y no debe haber setter sino operaciones add/remove. En Java 2 el getter devuelve `Collections.unmodifiableSet`; en Java 1.1 devuelve una copia (`clone`) porque los vectores no tienen versión inmodificable. Tras encapsular, mover comportamiento a la clase anfitriona con Extract Method y Move Method (ej. `numberOfAdvancedCourses`, `numberOfCourses`). También se tratan arrays, que Fowler suele convertir en listas durante la encapsulación.

## Replace Record with Data Class

Necesitas interactuar con una estructura de registro en un entorno de programación tradicional; crea un objeto de datos tonto para el registro. Útil al copiar un programa legacy, comunicar con una API tradicional o un registro de base de datos. Se crea una clase con un campo privado y getter/setter por cada ítem de dato; el comportamiento llega después con más refactorizaciones.

## Replace Type Code with Class

Una clase tiene un type code numérico que no afecta a su comportamiento; reemplaza el número por una nueva clase. Los type codes numéricos (enumeraciones) son comunes en lenguajes basados en C, pero el compilador solo ve el número subyacente, no el nombre simbólico, lo que reduce legibilidad y causa bugs. Al usar una clase, el compilador puede verificar tipos y las factory methods garantizan que solo se creen instancias válidas. Solo aplica si el type code es dato puro (no provoca comportamiento distinto en un switch). Ejemplo `BloodGroup` (O, A, B, AB) con instancias estáticas, campo `_code` y método estático `code(int)`.

## Replace Type Code with Subclasses

Tienes un type code inmutable que afecta al comportamiento de una clase; reemplázalo por subclases. Se indica por la presencia de condicionales tipo case (switch o if-then-else) que prueban el valor del type code. Es principalmente un movimiento de andamiaje que habilita Replace Conditional with Polymorphism. No aplica si el valor del type code cambia tras crear el objeto o si la clase ya está subclaseada por otra razón; en esos casos se usa Replace Type Code with State/Strategy. Mecánica: self-encapsulate del type code (reemplazando el constructor por factory method), una subclase por valor que sobrescribe el getter, luego eliminar el campo y declararlo abstracto. Después, Push Down Method y Push Down Field.

## Replace Type Code with State/Strategy

Tienes un type code que afecta al comportamiento pero no puedes usar subclassing; reemplázalo por un objeto de estado. Similar al anterior, pero aplicable cuando el type code cambia durante la vida del objeto. Usa el patrón state o strategy: strategy si simplificas un único algoritmo, state si mueves datos específicos de estado y piensas en el objeto como cambiando de estado. Ejemplo `Employee` (ENGINEER, SALESMAN, MANAGER) con promoción de managers a engineers (type code mutable): se crea `EmployeeType` abstracta con subclases, el setter asigna la instancia adecuada, y queda un único switch ejecutado solo al cambiar el tipo, listo para Replace Conditional with Polymorphism en `payAmount`.

## Replace Subclass with Fields

Tienes subclases que varían solo en métodos que devuelven datos constantes; convierte los métodos en campos de la superclase y elimina las subclases. Una subclase formada solo por constant methods (que devuelven un valor hard-coded) no hace lo suficiente para justificar su existencia. Ejemplo `Person` con subclases `Male`/`Female` que solo difieren en `isMale()` y `getCode()`: se usan factory methods, se declaran campos `final` en la superclase inicializados por un constructor protegido, y se eliminan las subclases una a una con Inline Method.

## Ideas clave

- Convertir datos simples en objetos es solo el primer paso; el valor real llega al mover comportamiento al nuevo objeto con Move Method.
- Reference objects se comparan por identidad; value objects por valor y deben ser inmutables (con `equals` y `hashCode`).
- La refactorización da libertad para cambiar de opinión entre acceso directo e indirecto a campos, y entre asociaciones uni y bidireccionales.
- Encapsular campos y colecciones reduce el acoplamiento; las colecciones usan un protocolo con vista de solo lectura y métodos add/remove.
- Duplicate Observed Data separa lógica de negocio de la GUI aunque obligue a duplicar datos, usando el patrón observer y acceso directo para evitar recursión.
- Las asociaciones bidireccionales tienen un coste (complejidad, zombies, interdependencia); elimina el extremo que no aporta.
- Para type codes hay tres caminos: Replace Type Code with Class (dato puro), with Subclasses (afecta al comportamiento, inmutable) y with State/Strategy (afecta al comportamiento, mutable o ya subclaseado).
