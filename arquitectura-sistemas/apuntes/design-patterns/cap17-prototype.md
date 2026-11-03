# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 17 — Prototype (Prototipo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Prototype es un patrón de diseño creacional que permite copiar objetos existentes sin que el código dependa de sus clases (PDF p. 133). La idea central es delegar el proceso de clonación a los propios objetos que están siendo clonados, en lugar de copiarlos "desde fuera".

El patrón declara una interfaz común para todos los objetos que soportan la clonación, normalmente con un único método `clonar`. Gracias a esta interfaz, el código cliente puede duplicar un objeto sin acoplarse a su clase concreta. Un objeto que soporta la clonación se denomina prototipo (PDF p. 135).

Sales sabiendo cuándo conviene clonar en lugar de instanciar: cuando no debes depender de clases concretas, cuando quieres reducir subclases que solo se diferencian en cómo inicializan sus objetos, y cuando copiar un objeto complejo preconfigurado es más barato que reconstruirlo. También aprendes la variante del registro de prototipos para gestionar prototipos de uso frecuente.

## Problema

Para copiar un objeto de forma directa habría que crear un nuevo objeto de la misma clase y recorrer todos los campos del original copiando sus valores (PDF p. 134). Este enfoque tiene varias trampas:

- Algunos campos pueden ser privados e invisibles desde fuera del objeto, por lo que no siempre se puede copiar "desde fuera".
- Para crear el duplicado hay que conocer la clase del objeto, lo que vuelve el código dependiente de esa clase.
- A veces solo se conoce la interfaz que sigue el objeto, no su clase concreta; por ejemplo, cuando un parámetro de un método acepta cualquier objeto que siga cierta interfaz (PDF p. 135).

## Solución

El patrón delega la clonación a los objetos clonados mediante una interfaz común con el método `clonar`. La implementación de ese método es muy parecida en todas las clases: crea un objeto de la clase actual y copia los valores de campo del viejo objeto al nuevo. Incluso se pueden copiar campos privados, porque la mayoría de los lenguajes permiten a un objeto acceder a campos privados de otros objetos de la misma clase (PDF p. 135).

Cuando los objetos tienen decenas de campos y miles de configuraciones posibles, la clonación sirve como alternativa a la creación de subclases: se crea un grupo de objetos configurados de maneras diferentes (prototipos prefabricados) y, cuando se necesita uno así, se clona en lugar de construirlo desde cero (PDF p. 136).

## Analogía del mundo real

En la industria, los prototipos se usan para hacer pruebas antes de la producción en masa, pero ahí juegan un papel pasivo y no se copian a sí mismos. Una analogía más precisa es la división mitótica de una célula: tras la división se forma un par de células idénticas, donde la célula original actúa como prototipo y asume un papel activo en la creación de la copia (PDF p. 137).

## Estructura

Implementación básica (PDF p. 138-139):

1. La interfaz **Prototipo** declara los métodos de clonación, normalmente un único método `clonar`.
2. El **Prototipo Concreto** implementa el método de clonación. Además de copiar la información del original al clon, puede gestionar casos extremos como clonar objetos vinculados o deshacer dependencias recursivas.
3. El **Cliente** puede producir una copia de cualquier objeto que siga la interfaz del prototipo.

Implementación del registro de prototipos (PDF p. 139):

1. El **Registro de Prototipos** ofrece acceso sencillo a prototipos de uso frecuente, almacenando un grupo de objetos prefabricados listos para copiar. El registro más sencillo es una tabla hash con pares `name → prototype`; si se necesita un criterio de búsqueda más preciso que un nombre, se puede crear una versión más robusta.

## Pseudocódigo

El ejemplo clona objetos geométricos sin acoplar el código a sus clases. Todas las clases de forma siguen la misma interfaz con un método de clonación, y una subclase puede invocar el método de clonación padre antes de copiar sus propios campos (PDF p. 140).

```
abstract class Shape is
    field X: int
    field Y: int
    field color: string

    constructor Shape() is
        // ...

    // El constructor prototipo inicializa un nuevo objeto
    // con valores del objeto existente.
    constructor Shape(source: Shape) is
        this()
        this.X = source.X
        this.Y = source.Y
        this.color = source.color

    abstract method clone(): Shape

class Rectangle extends Shape is
    field width: int
    field height: int

    constructor Rectangle(source: Rectangle) is
        super(source)
        this.width = source.width
        this.height = source.height

    method clone(): Shape is
        return new Rectangle(this)

class Circle extends Shape is
    field radius: int

    constructor Circle(source: Circle) is
        super(source)
        this.radius = source.radius

    method clone(): Shape is
        return new Circle(this)
```

El método de clonación crea un nuevo objeto y lo pasa al constructor; hasta que el constructor termina, nadie tiene acceso a un clon a medio terminar, lo que garantiza la consistencia del resultado (PDF p. 140). En el cliente, al recorrer una matriz de formas e invocar `clone()` sobre cada una, el polimorfismo asegura que se ejecuta el método de clonación de la clase real, obteniendo los clones adecuados en lugar de simples objetos `Shape` (PDF p. 142-143).

## Aplicabilidad

- Usa Prototype cuando tu código no deba depender de las clases concretas de los objetos que necesitas copiar. Esto ocurre a menudo con objetos pasados por código de terceros a través de una interfaz, cuyas clases concretas desconoces (PDF p. 144).
- Úsalo para reducir la cantidad de subclases que solo se diferencian en cómo inicializan sus objetos: en lugar de instanciar una subclase que coincida con una configuración, el cliente busca el prototipo adecuado y lo clona (PDF p. 144).

## Cómo implementarlo

1. Crea la interfaz del prototipo con el método `clonar`, o añade el método a todas las clases de una jerarquía existente (PDF p. 145).
2. Define un constructor alternativo que acepte un objeto de la clase y copie los valores de todos sus campos; para subclases, invoca al constructor padre para que la superclase clone sus campos privados. Si el lenguaje no soporta la sobrecarga de métodos, define un método especial de copia (PDF p. 145).
3. El método de clonación suele ser una sola línea con el operador `new` y la versión prototípica del constructor; cada clase debe sobrescribirlo usando su propio nombre de clase para no producir un objeto de una clase madre (PDF p. 145).
4. Opcionalmente, crea un registro de prototipos centralizado, como clase de fábrica o con un método estático en la clase base, que busque y clone el prototipo según un criterio; luego sustituye las llamadas directas a constructores por llamadas a su método de fábrica (PDF p. 146).

## Pros y contras

Pros (PDF p. 146):
- Clonas objetos sin acoplarlos a sus clases concretas.
- Evitas código de inicialización repetido clonando prototipos prefabricados.
- Creas objetos complejos con más facilidad.
- Obtienes una alternativa a la herencia al tratar con preajustes de configuración para objetos complejos.

Contra (PDF p. 146):
- Clonar objetos complejos con referencias circulares puede resultar complicado.

## Relaciones con otros patrones

- Muchos diseños empiezan con Factory Method y evolucionan hacia Abstract Factory, Prototype o Builder (PDF p. 147).
- Las clases de Abstract Factory pueden usar Prototype para escribir sus métodos.
- Prototype ayuda a guardar copias de Comandos en un historial.
- Composite y Decorator se benefician de Prototype para clonar estructuras complejas en lugar de reconstruirlas.
- Prototype no se basa en la herencia (evita sus inconvenientes) pero requiere una inicialización complicada del clon; Factory Method sí se basa en herencia pero no necesita un paso de inicialización.
- Prototype puede ser una alternativa más simple a Memento si el objeto es sencillo y sin enlaces a recursos externos (PDF p. 147-148).
- Abstract Factory, Builder y Prototype pueden implementarse como Singletons (PDF p. 148).

## Ideas clave

- Prototype delega la clonación al propio objeto mediante una interfaz común con un método `clonar`, evitando el acoplamiento a clases concretas.
- Un objeto que soporta la clonación es un prototipo; el constructor prototipo copia campos desde un objeto fuente, incluidos los privados de la misma clase.
- La clonación es una alternativa a la herencia cuando hay muchas configuraciones posibles: se clonan prototipos prefabricados en lugar de crear subclases.
- El polimorfismo hace que invocar `clonar` sobre una referencia genérica ejecute el método correcto de la clase real.
- Cada subclase debe sobrescribir `clonar` usando su propio nombre de clase para no clonar como la clase madre.
- El registro de prototipos centraliza prototipos de uso frecuente, típicamente en una tabla hash `name → prototype`.
- La principal dificultad es clonar objetos complejos con referencias circulares.
