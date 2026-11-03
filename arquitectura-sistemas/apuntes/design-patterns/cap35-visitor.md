# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 35 — Visitor (Visitante)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Visitor es un patrón de diseño de comportamiento que te permite separar algoritmos de los objetos sobre los que operan. En lugar de meter un nuevo comportamiento dentro de clases existentes, lo colocas en una clase aparte llamada visitante, y el objeto original se pasa a uno de los métodos del visitante como argumento.

La tesis central es que puedes añadir operaciones nuevas a una jerarquía de clases sin modificarlas, respetando el principio de abierto/cerrado. El truco técnico que lo hace posible es el Double Dispatch: delegar en los propios objetos la elección del método visitante adecuado, porque son ellos los que conocen su clase exacta.

Sales sabiendo cuándo conviene aplicarlo (estructuras de objetos complejas con muchos tipos), cómo se estructura (interfaz visitante, visitantes concretos, interfaz elemento con método `accept`, elementos concretos), y cuáles son sus compromisos, especialmente el coste de mantener todos los visitantes cada vez que cambia la jerarquía de elementos.

## El ejemplo que recorre el capítulo

Un equipo desarrolla una aplicación que trabaja con información geográfica estructurada como un enorme grafo. Cada nodo representa una entidad (una ciudad, una industria, un área turística) y cada tipo de nodo tiene su propia clase. Surge la tarea de exportar el grafo a formato XML.

La idea inicial —añadir un método de exportación a cada clase de nodo y recorrer el grafo por recursión— choca con dos problemas. Primero, el arquitecto no permite alterar las clases de nodo existentes porque el código ya está en producción y un error podría descomponer la aplicación. Segundo, la lógica de exportación XML no pertenece conceptualmente a unas clases cuyo trabajo principal es manejar geodatos; y si se añade un formato, pedirían luego otros, forzando a tocar de nuevo esas clases frágiles.

## Problema

Meter el comportamiento de exportación dentro de las clases de nodo supone riesgo (cambiar código en producción) y mala cohesión (mezclar geodatos con exportación). Además, anticipa cambios futuros: nuevos formatos de exportación obligarían a modificar otra vez las mismas clases.

## Solución

El patrón sugiere poner el nuevo comportamiento en una clase visitante separada. Como el comportamiento varía según la clase del objeto, el visitante define un grupo de métodos (uno por tipo), cada uno con un argumento de tipo distinto:

```
class ExportVisitor implements Visitor is
    method doForCity(City c) { ... }
    method doForIndustry(Industry f) { ... }
    method doForSightSeeing(SightSeeing ss) { ... }
```

El problema es elegir el método correcto. Estos métodos tienen firmas distintas, así que no sirve el polimorfismo directo, y revisar la clase con `instanceof` sería "una pesadilla". La sobrecarga de métodos tampoco ayuda: como la clase exacta del nodo es desconocida de antemano, el mecanismo recurre por defecto al método que toma la clase base `Nodo`.

La salida es el Double Dispatch: se delega la elección en el objeto pasado como argumento. Cada nodo "acepta" un visitante y le dice qué método ejecutar:

```
// Código cliente
foreach (Node node in graph)
    node.accept(exportVisitor)

class City is
    method accept(Visitor v) is
        v.doForCity(this)

class Industry is
    method accept(Visitor v) is
        v.doForIndustry(this)
```

El autor lo admite: hubo que cambiar las clases de nodo, pero el cambio es trivial y permite añadir más comportamientos sin volver a tocarlas. Al extraer una interfaz común para los visitantes, todos los nodos existentes funcionan con cualquier visitante nuevo que se introduzca.

## Analogía en el mundo real

Un agente de seguros experimentado visita todos los edificios de un barrio y ofrece pólizas distintas según el tipo de organización que ocupe cada edificio: seguros médicos a un edificio residencial, seguros contra robos a un banco, y seguros contra incendios e inundaciones a una cafetería.

## Estructura

1. La interfaz Visitante declara un grupo de métodos visitantes que toman elementos concretos como argumentos. Pueden compartir nombre si el lenguaje soporta sobrecarga, pero los tipos de sus parámetros deben ser diferentes.
2. Cada Visitante Concreto implementa varias versiones de los mismos comportamientos, personalizadas para las distintas clases de elemento concreto.
3. La interfaz Elemento declara un método para "aceptar" visitantes, con un parámetro del tipo de la interfaz visitante.
4. Cada Elemento Concreto implementa el método de aceptación, cuyo propósito es redirigir la llamada al método adecuado del visitante. Aunque la clase base lo implemente, cada subclase debe sobrescribirlo e invocar el método apropiado.
5. El Cliente suele ser una colección u otro objeto complejo (por ejemplo, un árbol Composite) y trabaja con los elementos a través de una interfaz abstracta, sin conocer todas sus clases concretas.

## Pseudocódigo

El ejemplo añade exportación XML a una jerarquía de formas geométricas. La interfaz `Shape` declara `accept(v: Visitor)`, y cada forma concreta (`Dot`, `Circle`, `Rectangle`, `CompoundShape`) lo implementa invocando el método visitante que coincide con su clase:

```
class Dot implements Shape is
    method accept(v: Visitor) is
        v.visitDot(this)

class Circle implements Shape is
    method accept(v: Visitor) is
        v.visitCircle(this)
```

La interfaz `Visitor` declara `visitDot`, `visitCircle`, `visitRectangle` y `visitCompoundShape`. El `XMLExportVisitor` implementa cada uno (exportar ID y coordenadas del punto, radio del círculo, anchura y altura del rectángulo, lista de IDs de los hijos de la forma compuesta). El cliente `Application` recorre `allShapes` y llama a `shape.accept(exportVisitor)` sin conocer las clases concretas. El autor remite a su artículo "Visitor y Double Dispatch" para justificar por qué se necesita el método aceptar.

## Aplicabilidad

- Cuando necesites realizar una operación sobre todos los elementos de una estructura de objetos compleja (por ejemplo, un árbol).
- Para limpiar la lógica de negocio de comportamientos auxiliares, manteniendo las clases primarias centradas en su trabajo principal.
- Cuando un comportamiento solo tenga sentido en algunas clases de una jerarquía y no en otras: se extrae a un visitante que implementa solo los métodos de las clases relevantes y deja el resto vacíos.

## Cómo implementarlo

1. Declara la interfaz visitante con un método "visitante" por cada clase de elemento concreto existente.
2. Declara la interfaz de elemento; si ya existe la jerarquía, añade el método abstracto de "aceptación" a la clase base, que acepta un objeto visitante.
3. Implementa los métodos de aceptación en todas las clases de elemento concreto, redirigiendo la llamada al método visitante que coincida con la clase actual.
4. Las clases de elemento solo trabajan con visitantes a través de la interfaz visitante; los visitantes, en cambio, deben conocer todas las clases de elemento concreto.
5. Por cada comportamiento que no pueda ir en la jerarquía de elementos, crea una nueva clase visitante concreta. Si el visitante necesita miembros privados del elemento, puedes hacerlos públicos (violando la encapsulación) o anidar la clase visitante en la clase elemento (si el lenguaje lo soporta).
6. El cliente crea los objetos visitantes y los pasa a los elementos mediante los métodos de aceptación.

## Pros y contras

- Principio de abierto/cerrado: introduces un nuevo comportamiento sobre objetos de clases diferentes sin cambiar esas clases.
- Principio de responsabilidad única: agrupas varias versiones del mismo comportamiento en una sola clase.
- Un visitante puede acumular información útil mientras recorre una estructura compleja como un árbol de objetos.
- Contra: debes actualizar todos los visitantes cada vez que se añade o elimina una clase de la jerarquía de elementos.
- Contra: los visitantes pueden carecer del acceso necesario a los campos y métodos privados de los elementos.

## Relaciones con otros patrones

- Visitor puede verse como una versión potente de Command: sus objetos ejecutan operaciones sobre varios objetos de distintas clases.
- Sirve para ejecutar una operación sobre un árbol Composite entero.
- Se combina con Iterator para recorrer una estructura de datos compleja y ejecutar una operación sobre sus elementos, aunque todos tengan clases distintas.

## Ideas clave

- Visitor separa algoritmos de los objetos sobre los que operan, colocándolos en una clase visitante aparte.
- Resuelve el problema de añadir operaciones a una jerarquía sin modificar sus clases (abierto/cerrado).
- Usa Double Dispatch: el objeto que "acepta" elige el método visitante adecuado porque conoce su propia clase.
- Ni el polimorfismo simple ni la sobrecarga resuelven la selección del método, porque la clase exacta es desconocida de antemano.
- Estructura: interfaz Visitante, visitantes concretos, interfaz Elemento con `accept`, elementos concretos que redirigen la llamada.
- Ideal para estructuras complejas (árboles, Composite) donde el visitante puede acumular estado al recorrerlas.
- Su mayor desventaja es el mantenimiento: cada cambio en la jerarquía de elementos obliga a actualizar todos los visitantes.
