# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 24 — Flyweight (Peso mosca)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación de párrafos) y las citas usan la página del PDF.

## Lo que necesitas saber

Flyweight es un patrón de diseño estructural que te permite mantener más objetos dentro de la cantidad disponible de RAM compartiendo las partes comunes del estado entre varios objetos, en lugar de mantener toda la información en cada objeto (PDF p. 238). Es, ante todo, una optimización de memoria: solo tiene sentido cuando un programa debe soportar una enorme cantidad de objetos similares que apenas caben en la RAM disponible.

La idea central es distinguir dos clases de estado dentro de un objeto. El estado intrínseco es la información constante que se repite entre muchos objetos (por ejemplo, el color y el sprite de todas las balas del mismo tipo); vive dentro del flyweight y es inmutable. El estado extrínseco es la información contextual única de cada objeto (coordenadas, vector de movimiento, velocidad), que cambia a lo largo del tiempo y se mueve fuera del flyweight.

Sales sabiendo cómo separar ambos estados, cómo almacenar el extrínseco en una clase contexto o en el objeto contenedor, por qué el flyweight debe ser inmutable, y cómo una fábrica flyweight reutiliza objetos existentes para no duplicarlos. También entiendes el principal compromiso: ahorras RAM a cambio de más ciclos de CPU y de un código más complicado.

## El ejemplo que recorre el capítulo

Decides crear un sencillo videojuego en el que los jugadores se mueven por un mapa disparándose entre sí, con un sistema de partículas realista: balas, misiles y metralla de las explosiones vuelan por todo el mapa (PDF p. 239). El juego funciona en tu máquina, pero en la computadora menos potente de un amigo se para a los pocos minutos: tras revisar los registros de depuración descubres que falla por falta de RAM.

El problema está en el sistema de partículas: cada partícula es un objeto separado con gran cantidad de datos, y al llegar la masacre a su punto culminante las nuevas partículas ya no caben en la RAM, provocando que el programa falle (PDF p. 240). Observando la clase `Partícula`, los campos `color` y `sprite` consumen mucha más memoria que el resto y almacenan información casi idéntica en todas las partículas del mismo tipo. Extraído el estado extrínseco, bastan tres objetos flyweight (una bala, un misil y un trozo de metralla) para representar todas las partículas del juego.

## Solución

El patrón sugiere dejar de almacenar el estado extrínseco dentro del objeto y pasarlo a los métodos específicos que dependen de él. Solo el estado intrínseco se mantiene dentro del objeto, lo que permite reutilizarlo en distintos contextos; así necesitas menos objetos, porque solo se diferencian en el estado intrínseco, que tiene muchas menos variaciones que el extrínseco (PDF p. 242). El objeto que solo almacena el estado intrínseco se denomina Flyweight.

### Almacenamiento del estado extrínseco

El estado extrínseco debe ir a alguna parte. En la mayoría de los casos se mueve al objeto contenedor que reúne los objetos antes de aplicar el patrón (en el ejemplo, el objeto principal `Juego` con su campo `partículas`). Esto obligaría a crear varias matrices sincronizadas por índice para coordenadas, vectores, velocidades y referencias a cada flyweight. Una solución más elegante es crear una clase de contexto separada que almacene el estado extrínseco junto con la referencia al flyweight, de modo que la clase contenedora solo necesite una matriz (PDF p. 243). Estos objetos contextuales son muchos pero muy pequeños, porque los campos pesados se han movido a unos pocos flyweights reutilizables.

### Flyweight e inmutabilidad

Como el mismo flyweight se usa en distintos contextos, su estado no debe poder modificarse. Un flyweight debe inicializar su estado una sola vez a través de parámetros del constructor y no exponer ningún método `set` ni campo público a otros objetos (PDF p. 244).

### Fábrica flyweight

Para un acceso cómodo puedes crear un método fábrica que gestione un grupo de flyweights existentes. Acepta el estado intrínseco del flyweight deseado, busca uno que coincida y lo devuelve; si no existe, crea uno nuevo y lo añade al grupo. Puede colocarse en un contenedor flyweight o en una nueva clase fábrica con método estático dentro de la clase flyweight real (PDF p. 244).

## Estructura

1. El patrón es simplemente una optimización; antes de aplicarlo, asegúrate de que hay un problema de consumo de RAM por muchos objetos similares y que no se puede resolver de otra forma sensata.
2. La clase **Flyweight** contiene la parte del estado compartible; lo almacenado dentro es intrínseco, lo que se pasa a sus métodos es extrínseco.
3. La clase **Contexto** contiene el estado extrínseco único; emparejada con un flyweight, representa el estado completo del objeto original.
4. El comportamiento suele quedarse en la clase flyweight (y quien lo invoca pasa las partes adecuadas del estado extrínseco por parámetros), o puede moverse al contexto, que usa el flyweight como mero objeto de datos.
5. El **Cliente** calcula o almacena el estado extrínseco; ve el flyweight como un objeto plantilla configurable en tiempo de ejecución pasando información contextual por parámetros.
6. La **Fábrica flyweight** gestiona el grupo: los clientes no crean flyweights directamente, sino que invocan a la fábrica pasándole el estado intrínseco deseado (PDF p. 245-246).

## Pseudocódigo

El ejemplo reduce el uso de memoria al representar millones de árboles en un lienzo. Se extrae el estado intrínseco repetido de la clase `Árbol` a la clase flyweight `TipodeÁrbol` (`TreeType`), que guarda `name`, `color` y `texture` y expone `draw(canvas, x, y)` (PDF p. 248). La fábrica `TreeFactory` mantiene una colección estática y en `getTreeType` busca un tipo existente; si es `null`, crea uno nuevo y lo añade. El objeto contextual `Tree` guarda solo `x`, `y` y una referencia a su `type`, y su `draw(canvas)` delega en `type.draw(canvas, this.x, this.y)`. La clase `Forest` es cliente: en `plantTree` pide el tipo a la fábrica, crea el `Tree` y lo almacena (PDF p. 248-249).

## Aplicabilidad y cómo implementarlo

Usa Flyweight solo cuando el programa deba soportar una enorme cantidad de objetos que apenas quepan en la RAM. Es más útil cuando la aplicación genera cantidades enormes de objetos similares, eso agota la RAM del dispositivo objetivo, y los objetos contienen estados duplicados extraíbles y compartibles (PDF p. 250).

Para implementarlo: (1) divide los campos en estado intrínseco (información invariable duplicada) y extrínseco (información contextual única); (2) deja el estado intrínseco en la clase pero hazlo inmutable, inicializado solo en el constructor; (3) por cada campo extrínseco usado en un método, introduce un parámetro que lo reemplace; (4) opcionalmente crea una fábrica que busque antes de crear; (5) el cliente almacena o calcula el estado extrínseco, que por comodidad puede moverse a una clase contexto con la referencia al flyweight (PDF p. 250-251).

## Pros y contras

- Puedes ahorrar mucha RAM, siempre que tu programa tenga toneladas de objetos similares.
- Puede que estés cambiando RAM por ciclos de CPU cuando deba recalcularse parte del contexto cada vez que se invoque un método flyweight.
- El código se complica: los nuevos miembros del equipo se preguntarán por qué el estado de una entidad se separó de tal manera (PDF p. 250-251).

## Relaciones con otros patrones

- Puedes implementar los nodos hoja compartidos de un **Composite** como Flyweights para ahorrar RAM.
- Flyweight muestra cómo crear muchos objetos pequeños, mientras que **Facade** muestra cómo crear un único objeto que represente un subsistema completo.
- Flyweight se asemeja a **Singleton** si pudieras reducir todos los estados compartidos a un único flyweight, pero: (1) solo debe haber una instancia Singleton, mientras que una clase Flyweight puede tener varias instancias con distintos estados intrínsecos; (2) el Singleton puede ser mutable, los flyweights son inmutables (PDF p. 252).

## Ideas clave

- Flyweight es una optimización de memoria: compartir el estado común entre muchos objetos para que quepan en la RAM.
- Estado intrínseco: constante, inmutable, vive en el flyweight; estado extrínseco: contextual, único, se pasa por parámetros.
- Un flyweight debe ser inmutable: estado inicializado solo en el constructor, sin setters ni campos públicos.
- El estado extrínseco suele moverse al contenedor o, mejor, a una clase contexto que referencia al flyweight.
- La fábrica flyweight reutiliza objetos existentes buscándolos por su estado intrínseco antes de crear uno nuevo.
- Aplícalo solo ante un problema real de RAM por muchísimos objetos similares que no se resuelve de otro modo.
- Compromiso central: ahorras memoria a costa de más CPU y de un código más complejo.
- Se relaciona con Composite (hojas compartidas), Facade (contraste de intención) y Singleton (una instancia mutable vs. varios flyweights inmutables).
