# Memento (Recuerdo) — Estudio

## Tarjetas de repaso

P: ¿Qué es el patrón Memento?
R: Un patrón de diseño de comportamiento que permite guardar y restaurar el estado previo de un objeto sin revelar los detalles de su implementación.

P: ¿Cuáles son los casos de uso principales de Memento?
R: La función "deshacer" y el manejo de transacciones reversibles, por ejemplo cuando hay que revertir un error durante una operación.

P: ¿A quién se delega la creación de la instantánea y por qué?
R: Al propio objeto originador, propietario del estado, para preservar la encapsulación y evitar que otros objetos invadan su espacio privado.

P: ¿Cuáles son los tres actores del patrón?
R: Originadora (produce y restaura instantáneas), Memento (objeto de valor/instantánea, normalmente inmutable) y Cuidadora (sabe cuándo capturar y restaurar, y gestiona el historial).

P: ¿Qué contiene como mínimo una instantánea del editor del ejemplo?
R: El texto, las coordenadas del cursor y la posición actual de desplazamiento.

P: ¿Por qué el memento debe ser inmutable?
R: Para que acepte datos solo una vez por el constructor, sin modificadores, de modo que nadie pueda alterar sus contenidos.

P: ¿Cómo acceden los cuidadores al memento?
R: A través de una interfaz limitada que permite extraer metadatos (tiempo de creación, nombre de la operación), pero no el estado original.

P: ¿Cuál es el problema de copiar el estado desde fuera del objeto?
R: Que la mayoría de objetos esconden datos en campos privados; exponerlos genera clases frágiles acopladas a cada cambio, y restringirlos impide producir instantáneas.

P: ¿En qué consiste la implementación basada en clases anidadas?
R: Se anida el memento dentro de la originadora (C++, C#, Java), dándole acceso a los campos y métodos privados del memento; la cuidadora solo puede almacenarlo, no alterarlo.

P: ¿En qué consiste la implementación basada en interfaz intermedia y su inconveniente?
R: En lenguajes sin clases anidadas (PHP), las cuidadoras usan una interfaz que solo declara métodos de metadatos; el inconveniente es que todos los miembros del memento deben ser públicos.

P: ¿Qué aporta la implementación con encapsulación más estricta?
R: Permite varios tipos de originadoras y mementos sin exponer estado; la cuidadora queda independiente porque el método de restauración se define en el memento, vinculado a su originadora.

P: ¿Cómo se combinan Command y Memento?
R: Los objetos de comando actúan como cuidadores: obtienen un memento justo antes de ejecutar la operación para poder deshacerla restaurando el estado.

P: ¿Cuáles son los principales contras de Memento?
R: Puede consumir mucha RAM si se crean mementos a menudo; las cuidadoras deben rastrear el ciclo de vida de la originadora; y en lenguajes dinámicos no se garantiza que el estado se mantenga intacto.

P: ¿Qué papel cumple la clase de historial en el editor?
R: Actúa como cuidadora con una pila de mementos que crece antes de cada operación; al deshacer, toma el memento más reciente y lo pasa al editor para restaurar su estado.

## Preguntas de autoevaluación

P: ¿Por qué Memento preserva la encapsulación mejor que copiar campos desde el exterior?
R: Porque delega la creación de la instantánea al originador, que tiene pleno acceso a su propio estado, y guarda la copia en un memento cuyos contenidos no son accesibles para ningún otro objeto. (Sección "Solución")

P: ¿A qué "callejón sin salida" se llega si no se usa Memento?
R: O se exponen los detalles internos (campos públicos y clases frágiles acopladas a cada cambio) o se restringe el acceso, lo que hace imposible producir instantáneas. (Sección "Problema")

P: ¿Qué responsabilidad tiene la cuidadora y qué no puede hacer?
R: Sabe cuándo y por qué capturar el estado y cuándo restaurarlo, y puede almacenar una pila de mementos; al trabajar solo con la interfaz limitada, no puede manipular el estado. (Secciones "Solución" y "Estructura")

P: En el pseudocódigo, ¿por qué la clase Snapshot no declara campos, getters ni setters públicos?
R: Para que nadie pueda alterar sus contenidos; los mementos se vinculan al editor que los creó, lo que además permite varias ventanas independientes con una pila centralizada de deshacer. (Sección "Pseudocódigo")

P: ¿Qué diferencia hay entre la variante de clases anidadas y la de interfaz intermedia?
R: La de clases anidadas mantiene privados los miembros del memento gracias al anidamiento; la de interfaz intermedia, usada en lenguajes sin clases anidadas, obliga a declarar públicos todos los miembros del memento. (Sección "Variantes de implementación")

P: ¿Cuándo puede Prototype ser una alternativa a Memento?
R: Cuando el objeto es sencillo y no tiene enlaces a recursos externos, Prototype puede resultar una alternativa más simple. (Sección "Relaciones con otros patrones")

P: ¿Por qué las cuidadoras deben rastrear el ciclo de vida de la originadora?
R: Para destruir los mementos obsoletos y evitar un consumo excesivo de memoria, uno de los contras del patrón. (Sección "Pros y contras")

## Puntos a dominar

- Definir Memento y explicar cómo guarda y restaura el estado sin revelar la implementación.
- Identificar los tres actores (originadora, memento, cuidadora) y su reparto de responsabilidades.
- Explicar por qué la creación de la instantánea se delega al originador para preservar la encapsulación.
- Distinguir las tres variantes de implementación (clases anidadas, interfaz intermedia, encapsulación estricta) y cuándo aplica cada una.
- Comprender la interfaz limitada de metadatos y por qué el memento conviene que sea inmutable.
- Reconocer los contras: consumo de RAM, gestión del ciclo de vida y lenguajes dinámicos.
- Relacionar Memento con Command, Iterator y Prototype.
