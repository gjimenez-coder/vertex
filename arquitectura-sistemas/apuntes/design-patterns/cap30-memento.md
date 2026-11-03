# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 30 — Memento (Recuerdo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Memento es un patrón de diseño de comportamiento que permite guardar y restaurar el estado previo de un objeto sin revelar los detalles de su implementación. Su caso de uso más conocido es la función "deshacer", pero también resulta indispensable al tratar con transacciones, por ejemplo cuando hay que revertir un error durante una operación.

La tesis central es que la creación de la instantánea debe delegarse al propio objeto propietario del estado (el originador), en lugar de que otros objetos invadan su espacio privado para copiarlo desde el exterior. Así se preserva la encapsulación: nadie más puede leer el estado almacenado, lo que mantiene seguros los datos del objeto original.

Sales sabiendo cómo repartir las responsabilidades entre tres actores —originador, memento y cuidador—, cómo implementar el patrón con clases anidadas o con una interfaz intermedia, y por qué cada variante existe según las capacidades del lenguaje.

## El ejemplo que recorre el capítulo

Un editor de texto al que se le quiere añadir la función de deshacer cualquier operación. La solución directa guarda, antes de cada operación, el estado de todos los objetos en un almacenamiento; al revertir, extrae la última instantánea del historial y restaura el estado. Una instantánea del editor contiene, como mínimo, el texto, las coordenadas del cursor y la posición actual de desplazamiento.

## Problema

Para producir una instantánea habría que recorrer todos los campos de un objeto y copiar sus valores. Esto solo funciona si el objeto tiene acceso laxo a sus contenidos, pero la mayoría de objetos reales esconden los datos significativos en campos privados.

Si se asume que los objetos "se comportan como hippies" y mantienen su estado público, aparecen inconvenientes serios: al refactorizar las clases editoras o añadir/eliminar campos, hay que cambiar también las clases responsables de copiar el estado. Además, los objetos contenedores de instantáneas necesitarían campos públicos, exponiendo todo el estado del editor y haciendo que otras clases dependan de cada pequeño cambio. Se llega a un callejón sin salida: o se exponen los detalles internos (clases frágiles) o se restringe el acceso (imposible producir instantáneas).

## Solución

El problema nace de una encapsulación fragmentada: algunos objetos invaden el espacio privado de otros. Memento delega la creación de instantáneas al objeto originador, que tiene pleno acceso a su propio estado. La copia se guarda en un objeto especial llamado memento, cuyos contenidos no son accesibles para ningún otro objeto excepto el que lo produjo.

Los demás objetos se comunican con el memento a través de una interfaz limitada que permite extraer metadatos (tiempo de creación, nombre de la operación), pero no el estado original. Esto permite almacenar mementos dentro de otros objetos llamados cuidadores. El cuidador, al trabajar solo con la interfaz limitada, no puede manipular el estado; el originador sí tiene acceso total y puede restaurar su estado previo a voluntad.

En el editor, una clase de historial actúa como cuidadora con una pila de mementos que crece antes de cada operación. Al activar Deshacer, el historial toma el memento más reciente y lo pasa de vuelta al editor para que restaure su estado.

## Estructura

Participantes:

1. Originadora: produce instantáneas de su propio estado y lo restaura a partir de ellas.
2. Memento: objeto de valor que actúa como instantánea. Es práctica común hacerlo inmutable y pasarle los datos una sola vez, por el constructor.
3. Cuidadora: sabe cuándo y por qué capturar el estado, y cuándo restaurarlo. Puede rastrear el historial almacenando una pila de mementos.

## Variantes de implementación

Implementación basada en clases anidadas (C++, C#, Java): la clase memento se anida dentro de la originadora, lo que da a esta acceso a los campos y métodos del memento aunque sean privados; la cuidadora tiene acceso muy limitado, suficiente para almacenar mementos pero no para alterarlos.

Implementación basada en una interfaz intermedia (lenguajes sin clases anidadas, como PHP): las cuidadoras trabajan con el memento solo a través de una interfaz intermediaria que declara únicamente métodos de metadatos. Las originadoras acceden directamente a los campos y métodos del memento. El inconveniente es que todos los miembros de la clase memento deben declararse públicos.

Implementación con encapsulación más estricta: permite varios tipos de originadoras y mementos, cada originadora con su memento correspondiente, sin exponer estado a nadie. La cuidadora queda independiente de la originadora porque el método de restauración se define en la clase memento. Cada memento se vincula a la originadora que lo produce (pasándola al constructor) y puede restaurarla siempre que esta defina los modificadores (setters) adecuados.

## Pseudocódigo

El ejemplo combina Memento con Command para guardar instantáneas del estado complejo del editor. Los objetos de comando actúan como cuidadores: obtienen un memento justo antes de ejecutar la operación. La clase memento (`Snapshot`) no declara ningún campo, getter o setter público, por lo que nadie puede alterar sus contenidos. Los mementos se vinculan al editor que los creó, lo que permite soportar varias ventanas de editor independientes con una pila centralizada para deshacer.

```
class Editor is
    private field text, curX, curY, selectionWidth
    method createSnapshot(): Snapshot is
        return new Snapshot(this, text, curX, curY, selectionWidth)

class Snapshot is
    private field editor: Editor
    private field text, curX, curY, selectionWidth
    method restore() is
        editor.setText(text)
        editor.setCursor(curX, curY)
        editor.setSelectionWidth(selectionWidth)

class Command is
    private field backup: Snapshot
    method makeBackup() is
        backup = editor.createSnapshot()
    method undo() is
        if (backup != null)
            backup.restore()
```

## Cómo implementarlo

1. Determina qué clase será la originadora y si el programa usa un objeto central o varios pequeños.
2. Crea la clase memento con campos que reflejen los de la originadora.
3. Hazla inmutable: acepta datos solo por el constructor, sin modificadores.
4. Si el lenguaje soporta clases anidadas, anida el memento en la originadora; si no, extrae una interfaz en blanco con solo operaciones de metadatos.
5. Añade a la originadora un método productor de mementos que pase su estado al constructor del memento.
6. Añade a la originadora un método de restauración que acepte un memento como argumento.
7. La cuidadora debe saber cuándo pedir mementos, cómo almacenarlos y cuándo restaurar.
8. Opcionalmente, mueve a la clase memento el vínculo con la originadora y el método de restauración.

## Pros y contras

Pros: produce instantáneas sin violar la encapsulación; simplifica el código de la originadora al dejar que la cuidadora mantenga el historial.

Contras: puede consumir mucha RAM si se crean mementos muy a menudo; las cuidadoras deben rastrear el ciclo de vida de la originadora para destruir mementos obsoletos; en lenguajes dinámicos (PHP, Python, JavaScript) no se garantiza que el estado del memento se mantenga intacto.

## Relaciones con otros patrones

- Command y Memento juntos para implementar deshacer: los comandos ejecutan operaciones y los mementos guardan el estado del objeto justo antes.
- Memento con Iterator para capturar el estado de la iteración actual y reanudarla.
- Prototype puede ser una alternativa más simple si el objeto es sencillo y no tiene enlaces a recursos externos.

## Ideas clave

- Memento guarda y restaura el estado previo de un objeto sin revelar su implementación.
- La creación de la instantánea se delega al originador, propietario del estado.
- El memento se expone a los cuidadores solo mediante una interfaz limitada de metadatos.
- Tres actores: originadora, memento (inmutable) y cuidadora (gestiona el historial).
- Hay tres variantes: clases anidadas, interfaz intermedia y encapsulación estricta.
- El patrón sirve para deshacer y también para transacciones reversibles.
- Preserva la encapsulación a costa de posible consumo de memoria.
