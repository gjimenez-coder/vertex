# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 11 — Dealing with Generalization (Tratar con la generalización)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo agrupa las refactorizaciones que trabajan sobre la generalización, es decir, sobre las jerarquías de herencia. La mayoría consisten en mover métodos y campos arriba y abajo de una jerarquía, pero también en crear jerarquías nuevas (extrayendo superclases, subclases o interfaces) y en cambiar entre herencia y delegación cuando la elección inicial resultó equivocada.

La idea central es que la duplicación entre clases relacionadas es un criadero de errores: si lo mismo se dice en varios sitios, cualquier cambio obliga a tocar más puntos de los necesarios. La herencia ofrece un mecanismo integrado para eliminar esa duplicación, pero a menudo las comunalidades no se notan hasta tener ya varias clases, por lo que la estructura de herencia hay que crearla después. Cuando la herencia no es la forma correcta de modelar una situación, el capítulo enseña a sustituirla por delegación, y viceversa.

Al terminar sabrás promover y degradar miembros (`Pull Up`/`Push Down`), tratar el caso especial de los constructores, separar lo común de lo variable con un método plantilla, formar nuevos tipos (subclase, superclase, interfaz), colapsar jerarquías redundantes y conmutar entre herencia y delegación según convenga.

## Pull Up Field / Pull Up Method (Subir campo / Subir método)

Cuando dos subclases comparten el mismo campo (aunque tengan nombres distintos), se mueve a la superclase. Primero se inspecciona que el uso sea el mismo, se renombran los campos para unificar el nombre, se crea el campo en la superclase (protegido si eran privados) y se borran los de las subclases. Reduce duplicación eliminando la declaración repetida y permitiendo subir también el comportamiento que usa el campo.

Subir un método se aplica cuando subclases tienen métodos con resultados idénticos. El caso más fácil es el copy-paste con cuerpo idéntico, pero Fowler recomienda buscar las diferencias porque suelen revelar comportamiento que no se probó. El elemento más complicado es que el cuerpo del método referencie features presentes en la subclase y no en la superclase: entonces se generaliza ese otro método o se declara abstracto en la superclase.

Ejemplo: un `Customer` con subclases `regular` y `preferred` cuyo `createBill` es idéntico. No se puede subir directamente porque `chargeFor` difiere en cada subclase, así que primero se declara abstracto en `Customer`:

```java
class Customer...
  abstract double chargeFor(date start, date end)
```

Luego se copia `createBill` a la superclase y se borra de cada subclase, compilando y probando en cada paso.

## Pull Up Constructor Body (Subir el cuerpo del constructor)

Los constructores son delicados: no son métodos normales y no se heredan, de modo que no sirve subir el método. Cuando varias subclases tienen constructores con cuerpos casi idénticos, se crea un constructor en la superclase (a menudo `protected` para señalar que lo deben llamar las subclases) y se invoca con `super` como primer paso del constructor de la subclase.

```java
class Employee
  protected Employee (String name, String id) {
    _name = name;
    _id = id;
  }
```

Si hay código común posterior que debe ejecutarse después de asignar campos de la subclase (como `if (isPriviliged()) assignCar();`), se extrae a un método (`initialize()`) con Extract Method y se sube con Pull Up Method. Si la refactorización se complica, conviene considerar Replace Constructor with Factory Method.

## Push Down Method / Push Down Field (Bajar método / Bajar campo)

Son los inversos de los anteriores. Se usan cuando un comportamiento o un campo de la superclase solo tiene sentido para algunas subclases. Se declara el método o campo en las subclases que lo necesitan, se copia el cuerpo y se elimina de la superclase. Es frecuente tras aplicar Extract Subclass.

## Extract Subclass (Extraer subclase)

El disparador es darse cuenta de que una clase tiene comportamiento que solo usan algunas instancias. A veces lo señala un type code (y entonces caben Replace Type Code with Subclasses o con State/Strategy). La alternativa principal es Extract Class: es la elección entre herencia y delegación. Extract Subclass suele ser más simple, pero tiene límites: no puedes cambiar el comportamiento basado en clase una vez creado el objeto, y solo sirve para representar un conjunto de variaciones.

Ejemplo del taller: de `JobItem` se extrae `LaborItem`. Se crea la subclase, se le da constructor, se cambian las llamadas `new JobItem(...)` por `new LaborItem(...)` donde corresponde, se limpian las listas de parámetros con Rename Method, y se van bajando métodos y campos (`getEmployee`, `_employee`). El campo `_isLabor`, que ahora es inherente a la jerarquía, se elimina sustituyendo su getter por métodos constantes polimórficos:

```java
class JobItem...
  protected boolean isLabor() { return false; }
class LaborItem...
  protected boolean isLabor() { return true; }
```

Después, los usos condicionales de `isLabor()` se refactorizan con Replace Conditional with Polymorphism (por ejemplo `getUnitPrice`). Con los métodos bajados, se baja el dato con Push Down Field.

## Extract Superclass (Extraer superclase)

Cuando dos clases tienen features similares, se crea una superclase abstracta y se suben los elementos comunes. Suele ser más fácil mover primero los campos. Si hay métodos con el mismo propósito pero distinta firma, se usa Rename Method y luego Pull Up Method; si tienen la misma firma pero cuerpos distintos, se declara el método abstracto en la superclase.

Ejemplo: `Employee` y `Department` comparten `name` y un coste anual calculado de forma distinta. Se crea `abstract class Party`, se sube `_name` y `getName`, se sube el cuerpo del constructor y se unifica el nombre `getAnnualCost` declarándolo abstracto en `Party`. Esto abre la posibilidad de tratar departamento y empleado como un composite (Gang of Four), aunque eso ya sería nueva funcionalidad, no estrictamente refactoring.

## Extract Interface (Extraer interfaz)

Cuando varios clientes usan el mismo subconjunto de la interfaz de una clase, o dos clases comparten parte de su interfaz, se extrae ese subconjunto a una interfaz. Java tiene herencia simple pero permite expresar estos requisitos con interfaces. A diferencia de Extract Superclass, Extract Interface solo saca interfaces comunes, no código común, y puede generar duplicación.

Ejemplo: un `Timesheet` solo necesita de `Employee` la tarifa y si tiene una habilidad especial, así que se define:

```java
interface Billable {
  public int getRate();
  public boolean hasSpecialSkill();
}
class Employee implements Billable ...
```

El cargo pasa a declararse `charge(Billable emp, int days)`. La gran ganancia aparece cuando se quiere facturar también a computadoras: basta con que implementen `Billable`.

## Collapse Hierarchy (Colapsar jerarquía)

Cuando una superclase y su subclase ya no se diferencian lo suficiente, se fusionan. Se elige cuál eliminar, se mueve todo su comportamiento y datos a la clase con la que se fusiona (con Pull Up/Push Down), se ajustan las referencias y se borra la clase vacía.

## Form Template Method (Formar método plantilla)

Cuando dos métodos de subclases realizan pasos similares en el mismo orden pero los pasos difieren, se mueve la secuencia a la superclase y se deja que el polimorfismo diferencie los pasos: esto es un template method (Gang of Four). Se descomponen los métodos con Extract Method hasta que los trozos extraídos sean idénticos o completamente distintos; los distintos se renombran para compartir firma, y se sube uno de los métodos originales, declarando abstractos los pasos variables.

Ejemplo continuación del capítulo 1: `statement()` (ASCII) y `htmlStatement()` (HTML). Primero se usa un method object para crear una jerarquía de estrategia (`Statement`, `TextStatement`, `HtmlStatement`) y se mueven los métodos con Move Method, renombrándolos a `value`. Luego se extraen `headerString`, `eachRentalString` y `footerString` con la misma firma en ambas subclases, hasta que los dos `value` quedan idénticos y se sube uno:

```java
class Statement...
  abstract String headerString(Customer aCustomer);
  abstract String eachRentalString (Rental aRental);
  abstract String footerString (Customer aCustomer);
```

Añadir un nuevo tipo de statement se reduce a crear una subclase que redefina los tres métodos abstractos.

## Replace Inheritance with Delegation (Reemplazar herencia por delegación)

Cuando una subclase usa solo parte de la interfaz de la superclase o no quiere heredar sus datos, la herencia dice una cosa mientras la intención es otra. Se crea un campo que refiera a una instancia de la (ex) superclase, se cambian los métodos para delegar, se rompe la subclasificación y se añaden métodos delegadores simples para los métodos de superclase usados por clientes.

Ejemplo clásico: `MyStack extends Vector`. Los clientes solo usan push, pop, size e isEmpty. Se crea `private Vector _vector = this;`, se reescriben `push` y `pop` para delegar, se rompe la herencia (`_vector = new Vector()`) y se añaden delegadores `size` e `isEmpty`.

## Replace Delegation with Inheritance (Reemplazar delegación por herencia)

El inverso: si escribes muchos delegadores simples para toda la interfaz del delegado, conviertes la clase delegante en subclase del delegado. Se hace subclase, se compila (resolviendo choques de métodos con Rename Method), se apunta el campo delegado al propio objeto, se eliminan los delegadores simples y luego el campo. Advertencias: no aplicarlo si no usas todos los métodos del delegado (una subclase debe seguir la interfaz de su superclase) ni si el delegado es mutable y compartido por varios objetos, porque perderías el compartido de datos.

## Ideas clave

- La duplicación entre clases relacionadas es el enemigo; la herencia es el mecanismo integrado para eliminarla.
- `Pull Up`/`Push Down` de campos y métodos mueven miembros por la jerarquía; sube lo común, baja lo específico.
- Los constructores no se heredan: usa Pull Up Constructor Body y, si se complica, Replace Constructor with Factory Method.
- Extract Subclass vs Extract Class, y Extract Superclass vs Extract Class, son siempre la elección entre herencia y delegación.
- Extract Interface saca interfaces comunes (no código) y marca subconjuntos de responsabilidad para el sistema de tipos.
- Form Template Method separa los pasos variables de los invariables y los resuelve con polimorfismo.
- Si una jerarquía no aporta valor, colápsala; si la herencia modela mal, cámbiala por delegación (y al revés cuando delegas interfaces completas).
- Compila y prueba después de cada movimiento: estas refactorizaciones avanzan en pasos pequeños y verificables.
