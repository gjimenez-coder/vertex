# Factory Method (Método fábrica) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Factory Method y qué proporciona? / R: Es un patrón creacional que da una interfaz para crear objetos en una superclase, dejando que las subclases alteren el tipo de objetos creados.

P: ¿Qué otros nombres recibe Factory Method? / R: Método fábrica y Constructor virtual.

P: ¿Cómo se llaman los objetos devueltos por el método fábrica? / R: Productos.

P: ¿Cuál es la idea central del patrón? / R: Sustituir la instanciación directa con `new` por la llamada a un método fábrica especial, que las subclases pueden sobrescribir para cambiar la clase de los productos.

P: ¿Qué condición deben cumplir los productos para que las subclases puedan devolver tipos distintos? / R: Deben compartir una clase base o interfaz común, y el método fábrica de la clase base debe declarar esa interfaz como tipo de retorno.

P: ¿Cuáles son los cuatro elementos de la estructura del patrón? / R: Producto (interfaz común), Productos Concretos (implementaciones), Creadora (declara el método fábrica) y Creadores Concretos (lo sobrescriben).

P: ¿Cuál es la responsabilidad principal de la clase Creadora? / R: Albergar lógica de negocio relacionada con los productos; crear productos no es su responsabilidad principal.

P: ¿El método fábrica siempre crea instancias nuevas? / R: No; puede devolver objetos de una caché, de una agrupación de objetos u otra fuente.

P: En el ejemplo de logística, ¿qué interfaz comparten Camión y Barco y qué método tiene? / R: La interfaz `Transporte` con el método `entrega`.

P: ¿Qué método de `Dialog` invoca al método fábrica en el pseudocódigo y para qué? / R: El método `render()`, que llama a `createButton()` para obtener un botón, le asigna el manejador de clic y lo renderiza.

P: ¿Qué dos principios SOLID cumple el patrón? / R: Responsabilidad única (código de creación en un solo lugar) y Abierto/Cerrado (nuevos productos sin romper el código cliente).

P: ¿Cuál es la principal desventaja del patrón? / R: El código puede complicarse por la multitud de nuevas subclases.

P: ¿Qué relación tiene Factory Method con Abstract Factory, Prototype y Builder? / R: Muchos diseños empiezan con Factory Method y evolucionan hacia esos patrones, más flexibles pero más complicados.

P: ¿De qué patrón es una especialización Factory Method? / R: De Template Method, y a su vez puede ser un paso de un gran Template Method.

## Preguntas de autoevaluación

P: ¿Qué problema aparece cuando una aplicación acopla todo su código a una sola clase concreta de transporte? / R: Añadir un nuevo tipo exige cambios en toda la base del código y lo llena de condicionales según la clase del objeto; cada tipo adicional repite esos cambios. (Sección: Problema)

P: ¿Cómo desacopla Factory Method la creación del uso de los objetos? / R: Reemplaza la llamada directa a `new` por un método fábrica; los objetos se siguen creando con `new`, pero dentro del método, y las subclases pueden alterar la clase devuelta sobrescribiéndolo. (Sección: Solución)

P: ¿Por qué el diálogo base debe operar con botones abstractos en el pseudocódigo? / R: Para que `Application` pueda pasarle cualquier subclase del creador y el código cliente no quede acoplado a clases concretas como `WindowsButton` o `HTMLButton`. (Sección: Pseudocódigo)

P: ¿En qué tres situaciones conviene aplicar el patrón? / R: Cuando no conoces los tipos exactos de objetos con los que trabajará el código, cuando quieres ofrecer puntos de extensión en una biblioteca o framework, y cuando quieres reutilizar objetos costosos existentes. (Sección: Aplicabilidad)

P: ¿Por qué un constructor no sirve para reutilizar objetos existentes y sí un método fábrica? / R: Porque un constructor siempre devuelve instancias nuevas; se necesita un método regular capaz de crear o reutilizar, que es justo lo que hace el método fábrica. (Sección: Aplicabilidad)

P: ¿Qué se hace cuando hay demasiados tipos de producto y no conviene una subclase por cada uno? / R: Se reutiliza un parámetro de control en las subclases, como `CorreoTerrestre` recibiendo un argumento para elegir entre `Camión` y `Tren`. (Sección: Cómo implementarlo)

P: Tras extraer el código de creación, ¿qué se hace con el método fábrica base? / R: Si queda vacío, se hace abstracto para forzar a las subclases a implementarlo; si queda algo, se convierte en comportamiento por defecto. (Sección: Cómo implementarlo)

P: ¿Qué diferencia a Prototype de Factory Method en cuanto a herencia? / R: Prototype no se basa en la herencia (evita sus inconvenientes) pero requiere inicialización complicada del clon; Factory Method se basa en herencia pero no requiere ese paso. (Sección: Relaciones con otros patrones)

## Checklist

Pasos para implementar Factory Method (derivados de la sección "Cómo implementarlo"):

- [ ] Haz que todos los productos sigan la misma interfaz, con métodos que tengan sentido en todos ellos.
- [ ] Añade un método fábrica vacío en la clase creadora, con tipo de retorno igual a la interfaz común.
- [ ] Sustituye las invocaciones a constructores de producto por llamadas al método fábrica, extrayendo el código de creación hacia él (usa un parámetro temporal para controlar el tipo si hace falta).
- [ ] Crea subclases creadoras por cada tipo de producto y sobrescribe el método fábrica extrayendo las partes adecuadas del código base.
- [ ] Si hay demasiados tipos, reutiliza el parámetro de control en las subclases en lugar de crear una subclase por cada uno.
- [ ] Si el método fábrica base queda vacío, hazlo abstracto; si queda algo, conviértelo en comportamiento por defecto.
- [ ] Verifica que el patrón se introduce preferentemente en una jerarquía de creadoras ya existente para no complicar el código con subclases innecesarias.
