# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 10 — Making Method Calls Simpler (Simplificar las llamadas a métodos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El capítulo trata sobre cómo mejorar las interfaces de los objetos para que sean fáciles de entender y usar, algo que Fowler considera una habilidad clave del buen software orientado a objetos. La tesis central es que buena parte de la claridad de un programa vive en los nombres de los métodos, en el diseño de sus listas de parámetros y en la separación nítida entre métodos que consultan estado y los que lo modifican.

Sales sabiendo un catálogo de refactorizaciones para: renombrar métodos, añadir y quitar parámetros, acortar listas de parámetros (pasando el objeto entero, introduciendo un objeto parámetro o sustituyendo un parámetro por un método), separar consultas de modificadores, parametrizar o desparametrizar métodos, ocultar métodos y setters, reemplazar constructores por factory methods, encapsular downcasts y manejar errores con excepciones en lugar de códigos de error (y cuándo volver a un test en vez de una excepción).

Fowler insiste en que el código se escribe primero para un humano y después para la máquina, y recoge dos advertencias de Doug Lea: la programación concurrente suele usar listas de parámetros largas (parámetros inmutables), por lo que hay que ser cauto al reducirlas; y que separar consulta de modificador es compatible con la concurrencia si se conserva un tercer método sincronizado que combine ambos.

## Rename Method (Renombrar método)

Si el nombre no revela el propósito, cámbialo. Un buen truco: pensar qué comentario llevaría el método y convertir ese comentario en su nombre. La mecánica segura declara el método nuevo copiando el cuerpo, hace que el método viejo delegue en él, compila y testea, migra los llamadores uno a uno y por último elimina el viejo (o lo marca como `deprecated` si es parte de una interfaz que no puedes quitar). Si hay pocos llamadores, puedes saltarte el paso de delegación.

## Add Parameter / Remove Parameter (Añadir / quitar parámetro)

`Add Parameter` se usa cuando el método necesita información que antes no recibía. Fowler dedica casi toda la motivación a desaconsejarlo: las listas largas huelen mal (data clumps, difíciles de recordar). Antes de añadir, pregunta si puedes obtener el dato de un parámetro existente o considerar `Introduce Parameter Object`. `Remove Parameter` elimina un parámetro que el cuerpo ya no usa; los programadores lo evitan por si acaso, pero un parámetro espurio obliga a trabajar al llamador. Cuidado con métodos polimórficos: si otra implementación sí usa el parámetro, no lo quites. La mecánica de ambos replica la de `Rename Method` (al suministrar un valor provisional, usa `null` para objetos y un valor claramente raro para tipos primitivos).

## Separate Query from Modifier (Separar consulta de modificador)

Un método que devuelve un valor no debería tener efectos secundarios observables; así puedes llamarlo tantas veces y donde quieras. Se crea una consulta que devuelve el mismo valor y un modificador con retorno `void`. En el ejemplo, `foundMiscreant` devuelve el nombre y además envía una alerta; se extrae `foundPerson` (solo consulta) y se deja el modificador para el efecto. El término clave es *observable*: cachear el resultado en un campo cambia el estado pero no es un efecto observable.

```java
String foundPerson(String[] people){
    for (int i = 0; i < people.length; i++) {
        if (people[i].equals("Don"))  return "Don";
        if (people[i].equals("John")) return "John";
    }
    return "";
}
```

Problema de concurrencia: en sistemas multihilo las operaciones test-and-set deben ser atómicas; se conserva un tercer método sincronizado que llama a la consulta y al modificador (que pueden ser `package`/`private`).

## Parameterize Method (Parametrizar método)

Varios métodos hacen lo mismo variando solo unos valores; se crean como un único método con un parámetro. Elimina duplicación y gana flexibilidad.

```java
void raise(double factor) { salary *= (1 + factor); }   // reemplaza tenPercentRaise / fivePercentRaise
```

Si no puedes parametrizar el método completo, extrae primero el fragmento repetitivo y parametrízalo (ejemplo `usageInRange(start, end)`).

## Replace Parameter with Explicit Methods (Reemplazar parámetro por métodos explícitos)

Inversa de `Parameterize Method`. Cuando un método ejecuta código distinto según los valores de un parámetro enumerado, crea un método por valor. Ventajas: evitas el condicional, ganas comprobación en tiempo de compilación y la interfaz es más clara (`Switch.beOn()` frente a `Switch.setState(true)`). No lo uses si los valores del parámetro cambian mucho; para comportamiento condicional, usa `Replace Conditional with Polymorphism`.

## Preserve Whole Object (Preservar el objeto completo)

Si extraes varios valores de un objeto para pasarlos sueltos como parámetros, pasa el objeto entero. Hace la lista de parámetros más robusta a cambios futuros y más legible, y a menudo revela comportamiento que conviene mover al objeto (p. ej. `TempRange.includes(...)`). Contrapartida: introduce una dependencia entre el objeto requerido y el llamado; si eso estropea tu estructura de dependencias, no lo uses. Un objeto o un valor cuestan lo mismo al pasarlos; la fuerza motriz es la dependencia. Si no existe el objeto, usa `Introduce Parameter Object`; si el método usa muchos valores de otro objeto, considera `Move Method`.

## Replace Parameter with Method (Reemplazar parámetro por método)

Si el receptor puede calcular por sí mismo un valor que recibe como parámetro, quítalo y que lo invoque. Aplica cuando el objeto se llama a sí mismo (o el receptor tiene referencia al emisor) y el cálculo no depende de los parámetros del método llamante. En el ejemplo se extrae `getDiscountLevel()`, se sustituyen las referencias y se aplica `Remove Parameter`, hasta poder incluso hacer `Inline Method` de `discountedPrice`.

## Introduce Parameter Object (Introducir objeto parámetro)

Un grupo de parámetros que viajan juntos es un *data clump*; reúnelos en un objeto. El ejemplo convierte `(Date start, Date end)` en una clase `DateRange` **inmutable** (campos `final`, fijados en el constructor, sin setters), lo que imita el paso por valor de Java y evita bugs de aliasing. El beneficio profundo llega después: puedes mover comportamiento al nuevo objeto (`DateRange.includes(...)`) y eliminar duplicación.

## Remove Setting Method (Eliminar método set)

Si un campo debe fijarse en la creación y no cambiar nunca, no proporciones setter y haz el campo `final`; así la intención es clara. El problema surge al usar acceso indirecto a variables ciegamente, incluso en el constructor. Si hay cálculo sobre el argumento, hazlo en el constructor o, si es complejo, en un método con nombre claro de intención (`initializeId`, no un setter). Para subclases que inicializan campos privados del padre, usa un constructor de superclase (`super(id)`). Para colecciones, reemplaza el setter por operaciones add/remove (ver `Encapsulate Collection`).

## Hide Method (Ocultar método)

Si un método no lo usa ninguna otra clase, hazlo `private`. Es fácil ver cuándo relajar la visibilidad; cuesta más detectar métodos demasiado visibles, así que revisa con regularidad (idealmente con una herramienta tipo lint). Caso común: ocultar getters y setters a medida que la clase gana comportamiento más rico.

## Replace Constructor with Factory Method (Reemplazar constructor por factory method)

Cuando necesitas hacer más que una construcción simple, sustituye el constructor por un factory method, y hazlo `private`. Motivación principal: reemplazar un type code por subclases, ya que un constructor solo devuelve instancias de su propia clase. Se muestran tres variantes de creación de subclases: con `switch` sobre el type code, con `Class.forName` (flexible pero sin comprobación en tiempo de compilación y expone nombres de subclase a los clientes), y con métodos explícitos por subclase (`createMale`/`createFemale`, útil con pocas subclases estables). Es un trade-off entre flexibilidad y seguridad de tipos; se puede revertir con `Parameterize Method` o `Replace Parameter with Explicit Methods`.

## Encapsulate Downcast (Encapsular downcast)

Si un método devuelve un objeto que sus llamadores deben downcastear, mueve el downcast dentro del método y devuelve el tipo más específico posible. Frecuente con métodos que devuelven iteradores o colecciones (ver `Encapsulate Collection`). Devolver una subclase cambia la firma pero no rompe el código existente, siempre que la subclase no viole el contrato del padre.

```java
Reading lastReading() { return (Reading) readings.lastElement(); }
```

## Replace Error Code with Exception (Reemplazar código de error por excepción)

En lugar de devolver un código especial de error, lanza una excepción: separa con claridad el procesamiento normal del de error. La parte que detecta el error no siempre es la que sabe resolverlo. Decide si la excepción es *checked* o *unchecked*: si es responsabilidad del llamador comprobar la condición antes de llamar, es un error de programación y usa *unchecked* (incluso una aserción); si es responsabilidad del método, declara una *checked*. Si hay muchos llamadores, usa un método intermedio temporal (`newWithdraw`) para migrar gradualmente y luego renómbralo.

## Replace Exception with Test (Reemplazar excepción por comprobación)

Las excepciones son para comportamiento excepcional, no un sustituto de tests condicionales. Si el llamador puede comprobar razonablemente la condición antes de llamar, provee un test. En el ejemplo del `ResourcePool`, quedarse sin recursos no es excepcional: se antepone un `if (_available.isEmpty())`, se añade una aserción temporal en el `catch`, y al confirmar que nunca se alcanza, se elimina el bloque `try` y se limpia el condicional con `Consolidate Duplicate Conditional Fragments`.

## Ideas clave

- El código se escribe primero para un humano y después para la máquina; un buen nombre vale el esfuerzo de renombrar.
- Las listas de parámetros largas huelen mal; prefiere pasar el objeto entero, introducir un objeto parámetro o dejar que el receptor calcule el valor.
- Separa siempre consultas (sin efectos observables) de modificadores; mejora el razonamiento sobre el código.
- Oculta todo lo que puedas: datos, setters innecesarios y métodos no usados por otras clases.
- Usa factory methods cuando la creación necesita más que un constructor, especialmente para devolver subclases según un type code.
- Encapsula el downcast dentro del método y devuelve el tipo más específico posible.
- Usa excepciones para errores excepcionales, no como sustituto de un test condicional que el llamador podría hacer.
- Advertencias de Doug Lea: cuidado al reducir listas de parámetros en código concurrente; `Separate Query from Modifier` es compatible con hilos si conservas un tercer método sincronizado.
