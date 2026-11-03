# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 14 — Factory Method (Método fábrica)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Factory Method es un patrón de diseño creacional que proporciona una interfaz para crear objetos en una superclase, mientras permite a las subclases alterar el tipo de objetos que se crearán. También se le llama Método fábrica o Constructor virtual.

La tesis central es sencilla: en lugar de instanciar objetos directamente con el operador `new`, el código invoca a un método fábrica especial. Los objetos que ese método devuelve se denominan productos. El valor aparece al sobrescribir el método fábrica en una subclase para cambiar la clase de los productos creados, sin tocar el código que los usa.

Sales sabiendo cuándo aplicar el patrón (cuando no conoces de antemano los tipos exactos de objetos con los que trabajará tu código, cuando quieres ofrecer puntos de extensión en una biblioteca o framework, o cuando quieres reutilizar objetos existentes), cómo implementarlo paso a paso y cómo se relaciona con otros patrones creacionales.

## El ejemplo que recorre el capítulo

El hilo conductor es una aplicación de gestión logística. La primera versión solo maneja transporte en camión, por lo que casi todo el código está acoplado a la clase `Camión`. Al crecer la popularidad llegan peticiones para incorporar logística marítima, pero añadir `Barco` obligaría a cambiar toda la base del código, que quedaría plagada de condicionales según la clase de los objetos de transporte.

La solución propone que tanto `Camión` como `Barco` implementen una interfaz común `Transporte` con un método `entrega`. El método fábrica de `LogísticaTerrestre` devuelve camiones y el de `LogísticaMarítima` devuelve barcos. El código cliente trata a todos como `Transporte`: sabe que tienen `entrega`, pero no necesita conocer cómo funciona exactamente (PDF p. 84).

## Problema

- Al acoplar todo a una clase concreta, añadir un nuevo tipo exige cambios en toda la base del código, y cada tipo adicional repite esos cambios.
- El resultado es código sucio, lleno de condicionales que cambian el comportamiento según la clase del objeto de transporte.

## Solución

- Reemplazar la invocación directa a `new` por una llamada a un método fábrica. Los objetos se siguen creando con `new`, pero dentro del método fábrica.
- Las subclases pueden alterar la clase de los objetos devueltos sobrescribiendo el método fábrica.
- Limitación: las subclases solo pueden devolver productos de distintos tipos si estos comparten una clase base o interfaz común, y el tipo de retorno del método fábrica en la clase base debe declararse como esa interfaz.

## Estructura

1. El **Producto** declara la interfaz común a todos los objetos que puede producir la clase creadora y sus subclases.
2. Los **Productos Concretos** son las distintas implementaciones de la interfaz de producto.
3. La clase **Creadora** declara el método fábrica cuyo tipo de retorno coincide con la interfaz de producto. Puede declararse abstracto para forzar a las subclases a implementarlo, o devolver un producto por defecto. Su responsabilidad principal no es crear productos, sino albergar lógica de negocio relacionada con ellos; el patrón ayuda a desacoplar esa lógica de las clases concretas de producto.
4. Los **Creadores Concretos** sobrescriben el método fábrica base para devolver un tipo diferente de producto. El método fábrica no tiene que crear instancias nuevas siempre: puede devolver objetos de una caché, una agrupación de objetos u otra fuente.

## Pseudocódigo

Ejemplo de diálogo multiplataforma de UI, sin acoplar el código cliente a clases concretas. La clase base `Dialog` declara el método fábrica `createButton(): Button`; su método `render()` lo invoca para obtener un botón y lo usa. Las subclases concretas cambian el producto resultante:

```
class Dialog is
    abstract method createButton(): Button

    method render() is
        Button okButton = createButton()
        okButton.onClick(closeDialog)
        okButton.render()

class WindowsDialog extends Dialog is
    method createButton(): Button is
        return new WindowsButton()

class WebDialog extends Dialog is
    method createButton(): Button is
        return new HTMLButton()

interface Button is
    method render()
    method onClick(f)
```

La clase `Application` elige el creador concreto según la configuración del entorno (`config.OS`) y trabaja con él a través de la interfaz base; mientras lo haga así, puede pasársele cualquier subclase del creador. Para que funcione, el diálogo base debe operar con botones abstractos. Cada nuevo método de fábrica que se añada al diálogo acerca el diseño al patrón Abstract Factory.

## Aplicabilidad

- Cuando no conozcas de antemano las dependencias y los tipos exactos de objetos con los que trabajará tu código. El patrón separa el código de construcción del de uso; para añadir un tipo de producto basta crear una subclase creadora y sobrescribir el método fábrica.
- Cuando quieras ofrecer a los usuarios de tu biblioteca o framework una forma de extender sus componentes internos: reduce toda la construcción de componentes a un único método fábrica que cualquiera pueda sobrescribir.
- Cuando quieras ahorrar recursos reutilizando objetos existentes (conexiones de BD, sistemas de archivos, recursos de red) en lugar de reconstruirlos. Como un constructor siempre devuelve instancias nuevas, necesitas un método regular capaz de crear o reutilizar, que es justo lo que hace un método fábrica.

## Cómo implementarlo

1. Haz que todos los productos sigan la misma interfaz, con métodos que tengan sentido en todos ellos.
2. Añade un método fábrica vacío en la clase creadora, con tipo de retorno igual a la interfaz común.
3. Sustituye las invocaciones a constructores de producto por llamadas al método fábrica, extrayendo el código de creación hacia él. Puede hacer falta un parámetro temporal para controlar el tipo devuelto.
4. Crea subclases creadoras por cada tipo de producto y sobrescribe el método fábrica extrayendo las partes adecuadas del código base.
5. Si hay demasiados tipos y no conviene una subclase por cada uno, reutiliza el parámetro de control en las subclases (ejemplo: `CorreoTerrestre` recibe un argumento para elegir entre `Camión` y `Tren`).
6. Si el método fábrica base queda vacío tras las extracciones, hazlo abstracto; si queda algo, conviértelo en comportamiento por defecto.

## Pros y contras

- Evitas un acoplamiento fuerte entre el creador y los productos concretos.
- Cumple el Principio de responsabilidad única: el código de creación queda en un solo lugar.
- Cumple el Principio de abierto/cerrado: incorporas nuevos tipos de producto sin descomponer el código cliente existente.
- En contra, el código puede complicarse por la multitud de nuevas subclases; lo ideal es introducir el patrón en una jerarquía de creadoras ya existente.

## Relaciones con otros patrones

- Muchos diseños empiezan con Factory Method y evolucionan hacia Abstract Factory, Prototype o Builder (más flexibles pero más complicados).
- Las clases de Abstract Factory suelen basarse en un grupo de métodos de fábrica; también pueden usar Prototype.
- Factory Method puede combinarse con Iterator para que las subclases de la colección devuelvan distintos tipos de iteradores compatibles.
- Prototype no se basa en la herencia (evita sus inconvenientes) pero requiere inicialización complicada del clon; Factory Method se basa en herencia pero no requiere ese paso.
- Factory Method es una especialización de Template Method, y a su vez puede ser un paso de un gran Template Method.

## Ideas clave

- Factory Method sustituye la llamada directa a `new` por un método fábrica sobrescribible en subclases.
- Todos los productos deben compartir una interfaz común, y el método fábrica debe declarar esa interfaz como tipo de retorno.
- La clase creadora existe sobre todo por su lógica de negocio; crear productos no es su responsabilidad principal.
- El método fábrica puede devolver objetos cacheados o agrupados, no solo instancias nuevas.
- Aplícalo cuando desconoces los tipos exactos, cuando ofreces puntos de extensión en un framework o cuando reutilizas objetos costosos.
- Aporta desacoplamiento, responsabilidad única y apertura/cierre, a costa de más subclases.
- Es la base de la que evolucionan Abstract Factory, Prototype y Builder, y una especialización de Template Method.
