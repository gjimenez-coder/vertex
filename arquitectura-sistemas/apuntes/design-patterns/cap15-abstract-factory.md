# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 15 — Abstract Factory (Fábrica abstracta)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Abstract Factory es un patrón de diseño creacional que permite producir familias de objetos relacionados sin especificar sus clases concretas. En lugar de instanciar productos directamente, el código cliente trabaja contra interfaces abstractas y delega la creación a un objeto de fábrica, de modo que puede cambiarse la variante completa de productos sin tocar el código cliente.

La tesis central es que, cuando una aplicación debe manejar varias familias de productos relacionados y además garantizar que los objetos de una misma familia combinen entre sí, conviene declarar interfaces por producto y una interfaz de fábrica que agrupe los métodos de creación. Cada variante de la familia se materializa en una fábrica concreta que produce solo sus productos compatibles.

Sales sabiendo cómo estructurar productos abstractos, productos concretos, una fábrica abstracta y fábricas concretas; cómo el cliente permanece desacoplado de las clases concretas; y cuándo aplicar el patrón frente a alternativas como Factory Method o Builder.

## El ejemplo que recorre el capítulo

El capítulo usa dos ejemplos. El del problema es un simulador de tienda de muebles con una familia de productos relacionados (Silla + Sofá + Mesilla) y variantes de esa familia (Moderna, Victoriana, Art Decó). Se necesita crear piezas que combinen entre sí dentro de la misma familia, porque "los clientes se enfadan bastante cuando reciben muebles que no combinan" (PDF p. 98), y evitar cambiar el código principal cada vez que los comerciantes actualizan sus catálogos.

El pseudocódigo ilustra elementos de interfaz de usuario (UI) multiplataforma: botones y casillas que deben coincidir con el estilo del sistema operativo. "No queremos que nuestro programa represente controles de macOS al ejecutarse en Windows" (PDF p. 104).

## Problema

El código se compone de clases que representan una familia de productos relacionados y varias variantes de esa familia. Hacen falta dos cosas a la vez: crear objetos individuales que combinen con otros de la misma familia, y no tener que modificar el código existente al añadir nuevos productos o familias.

## Solución

- Declarar de forma explícita interfaces para cada producto distinto de la familia (Silla, Sofá, Mesilla). Todas las variantes de un producto implementan su interfaz; todas las variantes del mismo objeto se mueven a una única jerarquía de clase.
- Declarar la fábrica abstracta: una interfaz con métodos de creación para todos los productos de la familia (crearSilla, crearSofá, crearMesilla). Estos métodos devuelven productos abstractos representados por las interfaces extraídas.
- Para cada variante de la familia se crea una fábrica concreta independiente basada en la interfaz FábricaAbstracta. Cada fábrica devuelve productos de un tipo particular; por ejemplo FábricaDeMueblesModernos solo crea SillaModerna, SofáModerno y MesillaModerna.
- El código cliente trabaja con fábricas y productos a través de sus interfaces abstractas, lo que permite cambiar el tipo de fábrica y, con ella, la variante de producto, sin descomponer el cliente.

El cliente no necesita conocer la clase concreta de la fábrica ni el tipo concreto de silla: trata todas las sillas mediante la interfaz Silla y solo sabe que implementa, por ejemplo, el método `sentarse`. La variante devuelta siempre combina con el sofá o la mesilla producidos por la misma fábrica. Normalmente la aplicación crea el objeto de fábrica concreto en la etapa de inicialización, seleccionando el tipo según la configuración o los ajustes del entorno.

## Estructura

1. Los **Productos Abstractos** declaran interfaces para un grupo de productos distintos pero relacionados que forman una familia.
2. Los **Productos Concretos** son implementaciones agrupadas por variantes. Cada producto abstracto (silla/sofá) se implementa en todas las variantes (victoriano/moderno).
3. La interfaz **Fábrica Abstracta** declara un grupo de métodos para crear cada producto abstracto.
4. Las **Fábricas Concretas** implementan esos métodos de creación; cada una corresponde a una variante específica y crea solo esas variantes.
5. Aunque las fábricas concretas instancian productos concretos, las firmas de sus métodos devuelven los productos abstractos correspondientes. Así el **Cliente** no se acopla a la variante concreta y puede funcionar con cualquier combinación fábrica/producto siempre que se comunique mediante interfaces abstractas.

## Pseudocódigo

El ejemplo crea elementos de UI multiplataforma sin acoplar el cliente a clases concretas. Al lanzarse, la aplicación comprueba el sistema operativo actual y crea el objeto de fábrica de la clase que coincida; el resto del código usa esa fábrica para crear elementos, evitando combinaciones equivocadas.

```
interface GUIFactory is
    method createButton(): Button
    method createCheckbox(): Checkbox

class WinFactory implements GUIFactory is
    method createButton(): Button is
        return new WinButton()
    method createCheckbox(): Checkbox is
        return new WinCheckbox()

class MacFactory implements GUIFactory is
    method createButton(): Button is
        return new MacButton()
    method createCheckbox(): Checkbox is
        return new MacCheckbox()
```

El cliente `Application` recibe una `GUIFactory` por constructor y crea sus elementos mediante `factory.createButton()`, trabajando solo con los tipos abstractos GUIFactory, Button y Checkbox. El `ApplicationConfigurator` lee la configuración y elige la fábrica en tiempo de ejecución:

```
if (config.OS == "Windows") then
    factory = new WinFactory()
else if (config.OS == "Mac") then
    factory = new MacFactory()
else
    throw new Exception("Error! Unknown operating system.")
```

Añadir una nueva variedad de elementos no obliga a modificar el cliente: basta crear una nueva clase de fábrica y ajustar ligeramente el código de inicialización.

## Aplicabilidad

- Úsalo cuando el código deba funcionar con varias familias de productos relacionados y no quieras que dependa de sus clases concretas, porque no las conoces de antemano o quieres permitir futura extensibilidad.
- Considéralo cuando una clase tenga un grupo de métodos de fábrica que nublen su responsabilidad principal; extraer esos métodos a una fábrica única o a una implementación completa del patrón mejora el diseño (cada clase responsable de una sola cosa).

## Cómo implementarlo

1. Mapea una matriz de tipos de productos frente a sus variantes.
2. Declara interfaces abstractas para todos los tipos de producto y haz que las clases concretas las implementen.
3. Declara la interfaz de la fábrica abstracta con métodos de creación para todos los productos abstractos.
4. Implementa una clase concreta de fábrica por cada variante de producto.
5. Crea código de inicialización que instancie una fábrica concreta según la configuración o el entorno, y pasa ese objeto a todas las clases que construyen productos.
6. Busca las llamadas directas a constructores de producto y sustitúyelas por llamadas al método de creación del objeto de fábrica.

## Pros y contras

- Garantiza que los productos obtenidos de una fábrica son compatibles entre sí.
- Evita el acoplamiento fuerte entre productos concretos y el código cliente.
- Principio de responsabilidad única: el código de creación queda en un solo lugar.
- Principio de abierto/cerrado: se introducen nuevas variantes sin descomponer el cliente existente.
- Contra: el código puede complicarse por las muchas interfaces y clases que introduce el patrón.

## Relaciones con otros patrones

- Muchos diseños empiezan con Factory Method y evolucionan hacia Abstract Factory, Prototype o Builder (más flexibles pero más complicados).
- Builder construye objetos complejos paso a paso; Abstract Factory crea familias de objetos relacionados y devuelve el producto de inmediato.
- Las clases de Abstract Factory suelen basarse en métodos de fábrica, pero también pueden usar Prototype.
- Puede servir como alternativa a Facade cuando solo quieres ocultar cómo se crean los objetos del subsistema.
- Se combina con Bridge cuando algunas abstracciones solo funcionan con implementaciones específicas.
- Abstract Factory, Builder y Prototype pueden implementarse como Singletons.

## Ideas clave

- Abstract Factory produce familias de objetos relacionados sin exponer sus clases concretas.
- Separa productos abstractos (interfaces) de productos concretos (implementaciones por variante).
- Una fábrica concreta por variante garantiza que los productos creados combinen entre sí.
- El cliente trabaja solo con interfaces abstractas, por lo que cambiar de variante no lo descompone.
- La fábrica concreta se elige normalmente en la inicialización según configuración o entorno.
- Favorece responsabilidad única y abierto/cerrado, a costa de más interfaces y clases.
- Suele ser el punto de evolución de Factory Method y se relaciona con Builder, Prototype, Bridge y Facade.
