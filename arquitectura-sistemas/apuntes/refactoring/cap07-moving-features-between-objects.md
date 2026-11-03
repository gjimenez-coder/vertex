# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 7 — Moving Features Between Objects (Mover características entre objetos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

La decisión más fundamental del diseño orientado a objetos es decidir dónde poner las responsabilidades, y Fowler reconoce que, tras más de una década trabajando con objetos, nunca acierta a la primera. La tesis del capítulo es tranquilizadora: no hace falta acertar la primera vez, porque el refactoring permite cambiar de opinión y mover el comportamiento cuando una decisión que era razonable deja de serlo.

El capítulo presenta un conjunto de refactorizaciones para reubicar características entre clases. Las dos básicas son Move Method y Move Field; si hay que usar ambas, Fowler prefiere mover primero el campo y luego el método. Cuando una clase se sobrecarga de responsabilidades se usa Extract Class para separarlas, y cuando una clase deja de aportar valor se usa Inline Class para fundirla en otra. Para gestionar el acoplamiento con clases delegadas están Hide Delegate y su inverso, Remove Middle Man.

Las dos últimas refactorizaciones, Introduce Foreign Method e Introduce Local Extension, son casos especiales reservados a cuando no se puede acceder al código fuente de una clase pero se le quiere añadir responsabilidad: para uno o dos métodos se usa el método foráneo; para más, la extensión local. Sales sabiendo cuándo y cómo trasladar estado y comportamiento entre clases con pasos seguros (compilar y probar en cada paso).

## El ejemplo que recorre el capítulo

Gran parte del capítulo gira en torno a una clase `Account` con un `AccountType`, y a una pareja `Person`/`Department`/`TelephoneNumber`. El cálculo del cargo por descubierto (`overdraftCharge`) sirve para ilustrar Move Method, el `_interestRate` para Move Field, y el número de teléfono para Extract Class e Inline Class. La relación persona–departamento ilustra Hide Delegate y Remove Middle Man, y la clase `Date` de Java ilustra los métodos foráneos y la extensión local.

## Move Method

Síntoma: un método usa o es usado por más características de otra clase que de aquella en la que está definido. Se mueve cuando las clases tienen demasiado comportamiento o están demasiado acopladas. Mecánica resumida: examinar las características usadas por el método y considerar moverlas también; revisar sub/superclases por otras declaraciones (si hay polimorfismo puede no poderse mover); declarar el método en la clase destino (quizá con otro nombre); copiar y adaptar el cuerpo; compilar; determinar cómo referenciar el objeto destino desde el origen; convertir el método origen en delegación; compilar y probar; decidir si eliminar el método origen o dejarlo como delegación.

En el ejemplo, `overdraftCharge` se mueve de `Account` a `AccountType`. El campo `_daysOverdrawn` debe quedarse en la cuenta porque varía con cada cuenta, así que se pasa como parámetro. Cuando el método necesita una característica de la clase origen hay cuatro opciones: moverla también al destino, crear/usar una referencia del destino al origen, pasar el objeto origen como parámetro, o (si es una variable) pasarla como parámetro.

## Move Field

Síntoma: un campo lo usa otra clase más que la clase en la que está definido (uso que puede ser indirecto vía getters/setters). Si los métodos tienen sentido donde están, se mueve el campo. Los campos van primero al hacer Extract Class. Mecánica: si el campo es público, usar Encapsulate Field (o Self Encapsulate Field si muchos métodos lo acceden); crear el campo con accesores en el destino; determinar cómo referenciar el objeto destino; eliminar el campo origen y redirigir todas las referencias a los accesores del destino; compilar y probar.

Ejemplo: se mueve `_interestRate` de `Account` a `AccountType`. Fowler insiste en eliminar el campo en origen para que el compilador detecte métodos no redirigidos. Con autoencapsulación solo hay que redirigir los accesores, lo que permite dar un paso más pequeño y facilita un posterior Move Method.

## Extract Class

Síntoma: una clase hace el trabajo de dos. Las clases crecen hasta quedar tan "crujientes como un pato al microondas". Buena señal: un subconjunto de datos y métodos que van juntos o cambian juntos. Mecánica: decidir cómo dividir responsabilidades; crear la nueva clase (renombrar la vieja si ya no encaja su nombre); enlazar de la vieja a la nueva (enlace bidireccional solo si hace falta); aplicar Move Field a cada campo y Move Method a cada método (empezando por los de bajo nivel), compilando y probando tras cada paso; reducir las interfaces; decidir si exponer la nueva clase como objeto de referencia o como objeto de valor inmutable.

Ejemplo: se separa el comportamiento del teléfono en `TelephoneNumber`. Al exponer la clase hay que considerar el aliasing; opciones: aceptarla como objeto de referencia (Change Value to Reference), hacerla inmutable o dar una interfaz inmutable, o clonarla al pasarla (con riesgo de confusión). Extract Class también mejora la "liveness" de programas concurrentes al permitir bloqueos separados.

## Inline Class

Es el inverso de Extract Class: se usa cuando una clase ya no aporta valor, a menudo tras moverle responsabilidades fuera. Mecánica: declarar el protocolo público de la clase origen en la clase absorbente delegando los métodos; redirigir todas las referencias a la absorbente (hacer la origen privada y renombrarla para que el compilador detecte referencias colgantes); compilar y probar; mover características con Move Method y Move Field hasta vaciar la origen; "celebrar un funeral breve". Ejemplo: `TelephoneNumber` se reintegra en `Person`.

## Hide Delegate

La clave de los objetos es la encapsulación. Si un cliente llama a un método definido en un campo del servidor (el delegado), el cliente depende del delegado y debe cambiar si este cambia. Se coloca un método delegante simple en el servidor para ocultar el delegado, de modo que los cambios se limiten al servidor. Mecánica: crear un método delegante en el servidor por cada método del delegado; ajustar el cliente para llamar al servidor; compilar y probar; si ningún cliente necesita ya el delegado, eliminar el accesor. Ejemplo: `john.getDepartment().getManager()` pasa a `john.getManager()`.

## Remove Middle Man

Inverso de Hide Delegate. El precio de ocultar el delegado es que cada nueva característica exige un nuevo método delegante en el servidor; con el tiempo se vuelve doloroso y el servidor es solo un intermediario. Es difícil saber cuánto ocultar, pero no importa demasiado porque se puede ajustar con el tiempo: "Refactoring means you never have to say you're sorry" (PDF p. 130). Mecánica: crear un accesor para el delegado; para cada uso de un método delegado, eliminarlo del servidor y hacer que el cliente llame directamente al delegado; compilar y probar. Se pueden conservar algunas delegaciones por conveniencia.

## Introduce Foreign Method

Síntoma: una clase servidor que usas necesita un método adicional, pero no puedes modificarla. Se crea el método en la clase cliente con una instancia del servidor como primer argumento. Si solo se usa una vez no merece la pena; si se repite, hay que factorizarlo ("la repetición es la raíz de todo mal del software"). Mecánica: crear el método en el cliente (sin acceder a características del cliente; pasar valores como parámetros); poner la instancia del servidor como primer parámetro; comentar el método como "foreign method; should be in server" para poder buscarlo luego. Ejemplo: `nextDay(previousEnd)` como método foráneo de `Date`.

## Introduce Local Extension

Síntoma: necesitas varios métodos adicionales en una clase servidor que no puedes modificar. Más allá de uno o dos métodos foráneos, conviene agruparlos en una extensión local: una subclase o un wrapper de la original, que es un subtipo y soporta todo lo original más lo extra. Fowler prefiere la subclase por ser menos trabajo; su obstáculo es que debe aplicarse en el momento de la creación del objeto. Si el original puede cambiar y la extensión se aplica más tarde, hay que usar wrapper para que los cambios afecten a ambos. Mecánica: crear la clase extensión (subclase o wrapper); añadir constructores de conversión que tomen el original como argumento; añadir las nuevas características; sustituir el original por la extensión donde haga falta; mover los métodos foráneos a la extensión.

Ejemplo con la clase `Date` de Java (`MfDate`). Con wrapper surge un problema con métodos que toman un original como argumento (p. ej. `after`) y con métodos del sistema como `equals`, que Java asume simétrico; sobrescribir `equals(Date)` es peligroso, así que se expone el wrapping con un nuevo nombre, `equalsDate`, con versiones para `Date` y para `MfDateWrap`. Con subclase el problema no aparece si no se sobrescriben operaciones; Fowler normalmente solo añade métodos, no sobrescribe.

## Ideas clave

- Dónde poner las responsabilidades no se acierta a la primera; el refactoring permite reubicarlas con seguridad.
- Move Method y Move Field son el pan de cada día; si usas ambos, mueve primero el campo.
- Elimina el campo o método en origen para que el compilador detecte referencias no redirigidas.
- Extract Class divide clases sobrecargadas; Inline Class funde clases que ya no aportan; son inversos.
- Al exponer una clase extraída, cuida el aliasing: referencia, inmutabilidad o clonación.
- Hide Delegate reduce acoplamiento ocultando el delegado; Remove Middle Man revierte el exceso de delegación.
- Para clases que no puedes modificar: Introduce Foreign Method (1–2 métodos) o Introduce Local Extension (más).
- Entre subclase y wrapper, prefiere la subclase salvo que la extensión deba aplicarse tras la creación de un objeto mutable.
