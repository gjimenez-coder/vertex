# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 16 — Builder (Constructor)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Builder es un patrón de diseño creacional que permite construir objetos complejos paso a paso. El patrón permite producir distintos tipos y representaciones de un objeto empleando el mismo código de construcción.

Su valor aparece cuando la inicialización de un objeto es laboriosa: muchos campos y objetos anidados que normalmente quedan sepultados en un constructor monstruoso con muchos parámetros, o dispersos por el código cliente. La idea central es sacar el código de construcción de la clase del producto y colocarlo en objetos independientes llamados constructores (builders), invocando solo los pasos que cada configuración necesita.

Sales sabiendo cuándo conviene el patrón (evitar el “constructor telescópico”, crear distintas representaciones con pasos similares, construir árboles recursivos como en Composite), cómo se estructura (interfaz constructora, constructores concretos, productos, directora y cliente) y qué compromisos implica (más clases a cambio de aislar y reutilizar el código de construcción).

## El ejemplo que recorre el capítulo

El hilo conductor es construir una casa y, en el pseudocódigo, construir automóviles con sus manuales. Para una casa sencilla hay que levantar cuatro paredes y un piso, instalar una puerta, colocar un par de ventanas y poner un tejado; pero una casa mayor puede exigir jardín, calefacción, fontanería o cableado, e incluso una piscina que solo tiene una de cada diez casas.

En el pseudocódigo, en lugar de saturar la clase `Automóvil` con un constructor enorme, el código de ensamblaje se extrae a un constructor de automóviles. Como todo automóvil necesita un manual cuyos detalles varían por modelo, se reutiliza el mismo proceso de construcción con un constructor especializado en elaborar manuales: implementa los mismos métodos, pero en lugar de fabricar piezas, las describe.

## Problema

- Crear una subclase de `Casa` por cada combinación de parámetros hace crecer sin control la jerarquía: cada parámetro nuevo (p. ej. el estilo del porche) la amplía más.
- Un único constructor gigante con todos los parámetros posibles elimina las subclases, pero no todos los parámetros son necesarios siempre, así que gran parte queda sin usar y las llamadas resultan feas.

## Solución

Builder saca el código de construcción a objetos constructores independientes y organiza la construcción en pasos (`construirParedes`, `construirPuerta`, etc.). No es necesario invocar todos los pasos: solo los que exija una configuración particular. Cuando se necesitan distintas representaciones, se crean varios constructores que implementan los mismos pasos de forma diferente (paredes de madera para una cabaña, de piedra para un castillo) y un cliente que interactúe con ellos mediante una interfaz común. El constructor no permite a otros objetos acceder al producto mientras se construye.

## Clase directora

Se pueden extraer las llamadas a los pasos de construcción a una clase independiente llamada directora. La directora define el orden en que se ejecutan los pasos, mientras que el constructor proporciona su implementación. No es estrictamente necesaria —el cliente puede invocar los pasos directamente—, pero es un buen lugar para colocar rutinas de construcción reutilizables y oculta por completo los detalles de la construcción al cliente, que solo asocia un constructor con la directora, inicia la construcción y recoge el resultado del constructor.

## Estructura

1. La interfaz Constructora declara los pasos de construcción comunes a todos los tipos de constructores.
2. Los Constructores Concretos ofrecen distintas implementaciones de esos pasos y pueden crear productos que no siguen una interfaz común.
3. Los Productos son los objetos resultantes; no tienen que pertenecer a la misma jerarquía de clases o interfaz.
4. La Directora define el orden de invocación de los pasos, permitiendo crear y reutilizar configuraciones específicas.
5. El Cliente asocia un constructor con la directora, normalmente una vez mediante el constructor de la directora; existe una alternativa en la que el cliente pasa el constructor al método de producción y así puede usar uno distinto cada vez.

## Pseudocódigo

La interfaz `Builder` declara pasos como `reset()`, `setSeats(...)`, `setEngine(...)`, `setTripComputer(...)` y `setGPS(...)`. `CarBuilder` y `CarManualBuilder` los implementan para productos diferentes (`Car` y `Manual`) que no comparten interfaz. Cada constructor concreto aporta su propio método de extracción (`getProduct`), porque el tipo de retorno varía y no puede declararse en la interfaz en lenguajes de tipado estático. Es práctica común invocar `reset` al final de `getProduct` para dejar el constructor listo para otro producto. El `Director` ejecuta secuencias como `constructSportsCar` (reset, 2 asientos, `SportEngine`, trip computer y GPS en `true`); el resultado final se extrae del constructor, no del director, porque este no conoce ni depende de constructores y productos concretos.

## Aplicabilidad

- Para evitar un “constructor telescópico”: en vez de sobrecargar un constructor con muchos parámetros opcionales (posible solo en lenguajes con sobrecarga como C# o Java), se construye paso a paso usando solo los pasos necesarios.
- Cuando se quieran crear distintas representaciones de un producto (p. ej. casas de piedra y de madera) cuya construcción use pasos similares que varían solo en los detalles: la interfaz base define los pasos, los concretos los implementan y la directora guía el orden.
- Para construir árboles con Composite u otros objetos complejos: se pueden aplazar pasos o invocarlos de forma recursiva sin descomponer el producto final, y el constructor no expone el producto incompleto.

## Cómo implementarlo

1. Define claramente los pasos de construcción comunes a todas las representaciones; si no se puede, no procede el patrón.
2. Declara esos pasos en la interfaz constructora base.
3. Crea un constructor concreto por representación e implementa sus pasos, incluyendo un método de extracción (que no va en la interfaz si los productos no comparten jerarquía).
4. Considera crear una clase directora que encapsule varias formas de construir usando el mismo constructor.
5. El cliente crea constructor y director, y pasa el constructor al director antes de construir.
6. El resultado solo se obtiene del director si todos los productos siguen la misma interfaz; si no, se extrae del constructor.

## Pros y contras

- A favor: construir objetos paso a paso, aplazar pasos o ejecutarlos de forma recursiva; reutilizar el mismo código para varias representaciones; principio de responsabilidad única, aislando la construcción compleja de la lógica de negocio.
- En contra: aumenta la complejidad general del código, pues exige crear varias clases nuevas.

## Relaciones con otros patrones

- Muchos diseños empiezan con Factory Method y evolucionan hacia Abstract Factory, Prototype o Builder (más flexibles pero más complicados).
- Builder construye objetos complejos paso a paso; Abstract Factory crea familias de objetos relacionados y devuelve el producto de inmediato, mientras Builder permite pasos adicionales antes de extraerlo.
- Builder sirve para crear árboles Composite complejos de forma recursiva.
- Se combina con Bridge: la directora hace de abstracción y las constructoras de implementaciones.
- Abstract Factory, Builder y Prototype pueden implementarse como Singletons.

## Ideas clave

- Builder construye objetos complejos paso a paso y produce distintas representaciones con el mismo código de construcción.
- Resuelve el constructor telescópico y la explosión de subclases por combinaciones de parámetros.
- Los pasos se declaran en una interfaz común; los constructores concretos los implementan de forma distinta.
- No hace falta invocar todos los pasos: solo los que necesita cada configuración.
- La clase directora es opcional pero encapsula y reutiliza el orden de construcción, ocultando los detalles al cliente.
- El método de extracción vive en el constructor concreto cuando los productos no comparten interfaz; un `reset` deja el constructor listo para el siguiente.
- El producto incompleto nunca se expone al cliente durante la construcción.
- Cuesta más clases, pero aísla la construcción (responsabilidad única) y la hace reutilizable.
