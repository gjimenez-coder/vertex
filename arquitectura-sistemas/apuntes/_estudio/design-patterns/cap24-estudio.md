# Flyweight (Peso mosca) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón de diseño es Flyweight y cuál es su propósito? / R: Es un patrón estructural que permite mantener más objetos en la RAM disponible compartiendo las partes comunes del estado entre varios objetos, en lugar de guardar toda la información en cada uno.

P: ¿Qué es el estado intrínseco? / R: La información constante que se repite entre muchos objetos (por ejemplo, color y sprite del mismo tipo de partícula); vive dentro del flyweight y es inmutable.

P: ¿Qué es el estado extrínseco? / R: La información contextual única de cada objeto (coordenadas, vector de movimiento, velocidad) que cambia con el tiempo y se mueve fuera del flyweight.

P: ¿Cómo logra Flyweight reducir el número de objetos? / R: Al dejar en el objeto solo el estado intrínseco, este se reutiliza en distintos contextos; como los objetos solo se diferencian en el intrínseco (con menos variaciones que el extrínseco), se necesitan menos objetos.

P: ¿Dónde se almacena el estado extrínseco? / R: En el objeto contenedor que reúne los objetos, o —más elegante— en una clase de contexto separada que guarda el estado extrínseco junto con la referencia al flyweight.

P: ¿Por qué un flyweight debe ser inmutable? / R: Porque el mismo flyweight se usa en distintos contextos; debe inicializar su estado una sola vez en el constructor y no exponer métodos set ni campos públicos.

P: ¿Qué hace la fábrica flyweight? / R: Gestiona un grupo de flyweights: acepta el estado intrínseco deseado, busca uno que coincida y lo devuelve; si no existe, crea uno nuevo y lo añade al grupo.

P: ¿Qué rol tiene la clase Contexto en la estructura del patrón? / R: Contiene el estado extrínseco único y, emparejada con un flyweight, representa el estado completo del objeto original.

P: ¿Qué rol tiene el Cliente? / R: Calcula o almacena el estado extrínseco y ve el flyweight como un objeto plantilla que configura en tiempo de ejecución pasándole información contextual por parámetros.

P: ¿Cuál es el compromiso central de aplicar Flyweight? / R: Ahorras mucha RAM a cambio de más ciclos de CPU (si hay que recalcular contexto) y de un código más complicado de entender.

P: ¿Cuándo conviene usar Flyweight? / R: Solo cuando la aplicación genera cantidades enormes de objetos similares que agotan la RAM del dispositivo y esos objetos contienen estados duplicados extraíbles y compartibles.

P: ¿En qué se diferencia Flyweight de Singleton? / R: Solo debe haber una instancia Singleton, mientras que una clase Flyweight puede tener varias instancias con distintos estados intrínsecos; además el Singleton puede ser mutable y los flyweights son inmutables.

P: En el pseudocódigo de los árboles, ¿qué guarda la clase flyweight `TreeType`? / R: El estado intrínseco repetido: `name`, `color` y `texture`, y expone `draw(canvas, x, y)`.

P: En ese mismo ejemplo, ¿qué guarda el objeto contextual `Tree`? / R: Solo `x`, `y` y una referencia a su `type`; su `draw(canvas)` delega en `type.draw(canvas, this.x, this.y)`.

## Preguntas de autoevaluación

P: ¿Por qué el videojuego de ejemplo se paraba en la máquina menos potente? / R: Por falta de RAM: cada partícula era un objeto separado con muchos datos, y en el punto culminante las nuevas partículas ya no cabían en la memoria. (Sección «El ejemplo que recorre el capítulo»)

P: ¿Por qué bastan tres objetos flyweight para representar todas las partículas del juego? / R: Porque al extraer el estado extrínseco, los campos pesados `color` y `sprite` son casi idénticos por tipo, así que una bala, un misil y un trozo de metralla cubren todas las partículas. (Sección «El ejemplo que recorre el capítulo»)

P: ¿Qué ventaja tiene usar una clase de contexto frente a mover el estado extrínseco al contenedor? / R: Evita crear varias matrices sincronizadas por índice; la clase contenedora solo necesita una matriz de objetos contextuales pequeños que referencian al flyweight. (Sección «Almacenamiento del estado extrínseco»)

P: ¿Cómo se garantiza la inmutabilidad de un flyweight en la práctica? / R: Inicializando su estado una sola vez mediante parámetros del constructor y no exponiendo ningún método set ni campo público a otros objetos. (Sección «Flyweight e inmutabilidad»)

P: ¿Qué pasos se siguen para implementar Flyweight? / R: Dividir campos en intrínseco y extrínseco; dejar el intrínseco inmutable en el constructor; reemplazar cada campo extrínseco por un parámetro del método; opcionalmente crear una fábrica que busque antes de crear; y almacenar o calcular el extrínseco en el cliente o en una clase contexto. (Sección «Aplicabilidad y cómo implementarlo»)

P: ¿Dónde puede residir el comportamiento en este patrón? / R: Suele quedarse en la clase flyweight, a la que el invocador pasa las partes del estado extrínseco por parámetros; o puede moverse al contexto, que entonces usa el flyweight como mero objeto de datos. (Sección «Estructura»)

P: ¿Qué relación tiene Flyweight con Composite? / R: Los nodos hoja compartidos de un Composite pueden implementarse como Flyweights para ahorrar RAM. (Sección «Relaciones con otros patrones»)

## Puntos a dominar

- Reconocer que Flyweight es ante todo una optimización de memoria y aplicarlo solo ante un problema real de RAM por muchísimos objetos similares no resoluble de otro modo.
- Distinguir con claridad estado intrínseco (constante, compartible, inmutable) de estado extrínseco (contextual, único, pasado por parámetros).
- Explicar por qué el flyweight debe ser inmutable y cómo se logra (constructor único, sin setters ni campos públicos).
- Describir las dos formas de almacenar el estado extrínseco (contenedor con matrices sincronizadas vs. clase contexto única).
- Explicar el funcionamiento de la fábrica flyweight: buscar por estado intrínseco y reutilizar antes de crear.
- Identificar los roles de la estructura: Flyweight, Contexto, Cliente y Fábrica flyweight.
- Articular el compromiso del patrón: menos RAM a cambio de más CPU y mayor complejidad del código.
- Diferenciar Flyweight de Singleton y relacionarlo con Composite y Facade.
