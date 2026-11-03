# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 3 — Bad Smells in Code (Malos olores en el código)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo, escrito conjuntamente por Kent Beck y Martin Fowler, aborda el *cuándo* refactorizar, no el *cómo*. Saber ejecutar una refactorización no dice en qué momento conviene empezar o parar, y esa decisión es tan importante como la mecánica. En lugar de apelar a una noción vaga de estética de programación, Beck propuso describir el "cuándo" en términos de *smells* (olores): estructuras en el código que sugieren —o a veces gritan— la posibilidad de refactorizar.

Los autores advierten que no ofrecen criterios precisos: según su experiencia, ningún conjunto de métricas rivaliza con la intuición humana informada. Lo que dan son indicios de que hay un problema resoluble con una refactorización. El lector debe desarrollar su propio sentido de cuántas variables de instancia o cuántas líneas en un método son demasiadas.

El capítulo funciona como catálogo: ante la duda, se identifica el olor y se acude a las refactorizaciones sugeridas (y a la tabla de la contraportada del libro). No siempre se encontrará el olor exacto, pero debería apuntar en la dirección correcta. Sales sabiendo reconocer una colección de síntomas recurrentes y qué refactorizaciones aplicar a cada uno.

## Duplicated Code (Código duplicado)

El número uno del desfile de hedores. Misma estructura en más de un sitio: unificar siempre mejora el programa.

- Misma expresión en dos métodos de la misma clase: *Extract Method* e invocar desde ambos.
- Misma expresión en dos subclases hermanas: *Extract Method* en ambas y luego *Pull Up Field*. Si es parecido pero no igual, *Extract Method* para separar lo similar de lo distinto, y quizá *Form Template Method*. Si hacen lo mismo con algoritmo distinto, elegir el más claro con *Substitute Algorithm*.
- En dos clases no relacionadas: *Extract Class* en una y usar el nuevo componente en la otra; o decidir en qué clase (o en una tercera) debe vivir el método.

## Long Method (Método largo)

Los programas que viven mejor y más tiempo tienen métodos cortos. La indirección paga en explicación, compartición y elección. El coste de las llamadas en OO moderno es mínimo; el coste real para el lector se mitiga con buenos nombres: con un buen nombre no hace falta mirar el cuerpo.

Heurística: cuando sientes la necesidad de comentar algo, escribe un método en su lugar, nombrado por la intención y no por el cómo. La clave no es la longitud sino la distancia semántica entre qué hace el método y cómo lo hace. El 99% de las veces basta *Extract Method*. Con muchos parámetros y temporales: *Replace Temp with Query*, *Introduce Parameter Object*, *Preserve Whole Object*, y como artillería pesada *Replace Method with Method Object*. Para condicionales y bucles: *Decompose Conditional* y extraer el bucle a su propio método.

## Large Class (Clase grande)

Demasiadas variables de instancia suelen indicar que la clase hace demasiado, y ahí el código duplicado no anda lejos. *Extract Class* para agrupar variables (p. ej. `depositAmount` y `depositCurrency` van juntas); prefijos o sufijos comunes señalan componentes; si encaja como subclase, *Extract Subclass*. *Extract Interface* según cómo la usen los clientes ayuda a trocearla. Si es una clase GUI, mover datos y comportamiento a un objeto de dominio con *Duplicate Observed Data*.

## Long Parameter List (Lista larga de parámetros)

Con objetos no se pasa todo lo que el método necesita, sino lo suficiente para que lo obtenga. Las listas largas son difíciles de entender y cambian constantemente. *Replace Parameter with Method* cuando el dato se obtiene de un objeto ya conocido; *Preserve Whole Object* para sustituir datos sacados de un objeto por el objeto mismo; *Introduce Parameter Object* para datos sin objeto lógico. Excepción: cuando no se quiere crear dependencia del objeto llamado hacia el mayor.

## Divergent Change (Cambio divergente)

Una clase que cambia de formas distintas por razones distintas ("estos métodos cambian por cada base de datos nueva; estos otros por cada instrumento financiero"). Lo ideal: que cualquier variación afecte a una sola clase. Reunir todo lo que cambia por una misma causa con *Extract Class*.

## Shotgun Surgery (Cirugía con escopeta)

Lo opuesto al anterior: un cambio obliga a muchos pequeños cambios en muchas clases. *Move Method* y *Move Field* para concentrar los cambios en una clase; crearla si no existe; *Inline Class* para reunir comportamiento. Idealmente, relación uno a uno entre cambios comunes y clases.

## Feature Envy (Envidia de atributos)

Un método que parece más interesado en otra clase que en la suya (típicamente invoca muchos *getters* ajenos). *Move Method* para llevarlo; *Extract Method* sobre la parte envidiosa y luego *Move Method*. Regla: poner el método donde están la mayoría de los datos. Patrones como Strategy, Visitor (Gang of Four) y Self Delegation (Beck) rompen la regla a propósito para aislar comportamiento que cambia.

## Data Clumps (Grumos de datos)

Los mismos tres o cuatro datos que aparecen juntos en muchos sitios deben formar su propio objeto. *Extract Class* sobre los campos; *Introduce Parameter Object* o *Preserve Whole Object* en las firmas. Buena prueba: si borraras un valor, ¿tendrían sentido los demás? Si no, hay un objeto esperando nacer.

## Primitive Obsession (Obsesión por los primitivos)

Reticencia a usar objetos pequeños para tareas pequeñas (dinero con número y moneda, rangos, teléfonos, códigos postales). *Replace Data Value with Object*; para códigos de tipo, *Replace Type Code with Class* (si no afecta al comportamiento), o *Replace Type Code with Subclasses* / *Replace Type Code with State/Strategy* si hay condicionales que dependen del código. También *Extract Class*, *Introduce Parameter Object* y *Replace Array with Object*.

## Switch Statements (Sentencias switch)

Su problema es la duplicación: el mismo switch disperso que hay que cambiar en todas partes al añadir un caso. La polimorfia es la respuesta elegante. *Extract Method* y *Move Method* para llevar el switch a la clase adecuada, luego *Replace Type Code with Subclasses* o *State/Strategy* y *Replace Conditional with Polymorphism*. Si son pocos casos estables, la polimorfia es excesiva: *Replace Parameter with Explicit Methods*; para un caso nulo, *Introduce Null Object*.

## Parallel Inheritance Hierarchies (Jerarquías de herencia paralelas)

Caso especial de shotgun surgery: cada subclase de una jerarquía obliga a crear otra en la paralela (se reconocen por prefijos de nombre iguales). Hacer que las instancias de una jerarquía referencien a las de la otra; con *Move Method* y *Move Field* desaparece una de las jerarquías.

## Lazy Class (Clase holgazana)

Toda clase cuesta mantener y entender; la que no se gana su sustento se elimina. *Collapse Hierarchy* para subclases insuficientes; *Inline Class* para componentes casi inútiles.

## Speculative Generality (Generalidad especulativa)

Mecanismos y casos especiales para cosas que "quizá algún día" se necesiten, pero que no se requieren. *Collapse Hierarchy*, *Inline Class*, *Remove Parameter*, *Rename Method*. Si el único usuario de un método o clase son casos de prueba, bórralos junto con la prueba.

## Temporary Field (Campo temporal)

Variable de instancia asignada solo en ciertas circunstancias, confusa porque se espera que un objeto necesite todas sus variables. *Extract Class* para darles hogar; *Introduce Null Object* para eliminar código condicional. Caso común: variables de un algoritmo complejo puestas como campos; extraerlas con los métodos que las usan crea un *method object*.

## Message Chains (Cadenas de mensajes)

El cliente pide un objeto a otro, y a ese otro, y así (largas secuencias de `getThis`). Acopla al cliente con la estructura de navegación. *Hide Delegate*; mejor aún, *Extract Method* + *Move Method* para empujar el uso cadena abajo. Moderación: no todo encadenamiento es terrible.

## Middle Man (Intermediario)

La encapsulación trae delegación, pero puede excederse: media interfaz de una clase delega en otra. *Remove Middle Man* para hablar con quien realmente sabe; *Inline Method* si son pocos; *Replace Delegation with Inheritance* si hay comportamiento adicional.

## Inappropriate Intimacy (Intimidad inapropiada)

Clases demasiado íntimas que hurgan en las partes privadas de la otra. *Move Method*, *Move Field*, *Change Bidirectional Association to Unidirectional*, *Extract Class* para lo común, o *Hide Delegate*. La herencia favorece la intimidad excesiva; si toca, *Replace Delegation with Inheritance*.

## Alternative Classes with Different Interfaces (Clases alternativas con interfaces distintas)

Métodos que hacen lo mismo con firmas distintas: *Rename Method*. Si no basta, *Move Method* hasta igualar protocolos y *Extract Superclass* para redimir duplicación.

## Incomplete Library Class (Clase de biblioteca incompleta)

No se puede (ni suele convenir) modificar una clase de biblioteca, así que *Move Method* es inútil. Si faltan un par de métodos, *Introduce Foreign Method*; si falta mucho comportamiento, *Introduce Local Extension*.

## Data Class (Clase de datos)

Clases con campos, *getters*/*setters* y nada más: meros contenedores manipulados en exceso por otras clases. *Encapsulate Field*, *Encapsulate Collection*, *Remove Setting Method*. Mover comportamiento hacia ellas con *Move Method* (o *Extract Method* previo) y luego *Hide Method* en los accesores. Son como niños: punto de partida aceptable, pero deben asumir responsabilidad.

## Refused Bequest (Herencia rechazada)

Subclases que heredan métodos y datos que no quieren. El consejo tradicional: crear una clase hermana con *Push Down Method* y *Push Down Field*. Los autores lo relativizan: subclasear para reutilizar comportamiento es legítimo; nueve de cada diez veces el olor es demasiado tenue para limpiarlo. Es fuerte cuando la subclase reutiliza comportamiento pero rechaza la *interfaz* del padre: ahí, *Replace Inheritance with Delegation*.

## Comments (Comentarios)

Los comentarios no son mal olor —son dulces—, pero a menudo actúan como desodorante que tapa código malo. Primero refactorizar; con frecuencia el comentario queda superfluo. *Extract Method* si un comentario explica un bloque; *Rename Method* si ya está extraído; *Introduce Assertion* para reglas sobre el estado requerido. Buen uso del comentario: cuando no sabes qué hacer, o para explicar *por qué* hiciste algo.

> "When you feel the need to write a comment, first try to refactor the code so that any comment becomes superfluous." (PDF p. 71)

## Ideas clave

- Los *smells* describen el *cuándo* refactorizar; la intuición humana informada supera a cualquier métrica fija.
- El código duplicado es el peor olor y casi todo lo demás lo alimenta (clases grandes, métodos largos).
- Regla rectora: poner juntas las cosas que cambian juntas; datos y el comportamiento que los usa suelen cambiar a la vez.
- Divergent change (una clase, muchos tipos de cambio) y shotgun surgery (un cambio, muchas clases) son caras opuestas; el ideal es una relación uno a uno entre cambios y clases.
- *Extract Method* y *Move Method* son las refactorizaciones recurrentes en casi todos los olores.
- Muchos olores se curan creando objetos pequeños a partir de primitivos y grumos de datos.
- Los switch suelen pedir polimorfia, salvo pocos casos estables.
- Los comentarios suelen señalar código que debería refactorizarse hasta volverlos innecesarios; los autores predican moderación frente a los consejos "tradicionales".
