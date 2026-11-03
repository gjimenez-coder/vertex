# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 27 — Command (Comando)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Command es un patrón de diseño de comportamiento que convierte una solicitud en un objeto independiente que contiene toda la información sobre ella. Esta transformación permite parametrizar métodos con distintas solicitudes, retrasar o poner en cola su ejecución y soportar operaciones reversibles.

La tesis central es desacoplar el objeto que invoca una operación (emisor) del objeto que la realiza (receptor), colocando entre ambos un objeto comando con una interfaz común. Al terminar sabes cómo extraer una solicitud (objeto invocado, método y argumentos) a una clase comando, cómo conectar comandos con botones, menús y atajos sin duplicar código, y cómo apoyarte en el historial de comandos para implementar deshacer/rehacer.

## El ejemplo que recorre el capítulo

Un editor de texto con una barra de herramientas de botones. La solución ingenua crea cientos de subclases de `Botón`, una por cada lugar de uso, lo que acopla torpemente el código GUI al volátil código de la lógica de negocio. Peor aún, operaciones como copiar/pegar deben invocarse desde varios lugares (botón de la barra, menú contextual, Ctrl+C), obligando a duplicar la implementación en muchas clases.

## Problema

Todos los botones provienen de la misma clase pero deben hacer cosas diferentes. Crear una subclase por cada gestor de clic genera una cantidad enorme de subclases y riesgo de descomponer el código cada vez que se modifica la clase base `Botón`. Al añadir menús contextuales y atajos, hay que duplicar el código de cada operación o, peor, hacer los menús dependientes de los botones.

## Solución

El buen diseño se apoya en la separación de responsabilidades, que suele dividir la aplicación en capas: una capa GUI y una capa de lógica de negocio. La GUI delega el trabajo importante a la capa subyacente; este proceso se describe como un objeto que envía a otro una solicitud.

Command sugiere que los objetos GUI no envíen las solicitudes directamente. En su lugar, se extraen todos los detalles de la solicitud (objeto invocado, nombre del método y lista de argumentos) a una clase comando separada con un único método que activa esa solicitud. El objeto comando sirve de vínculo entre la GUI y la lógica de negocio: el objeto GUI ya no necesita saber qué objeto recibirá la solicitud ni cómo la procesará, solo activa el comando.

Los comandos implementan la misma interfaz, normalmente con un único método de ejecución sin parámetros. Esto permite usar varios comandos con el mismo emisor sin acoplarlo a clases concretas, e incluso cambiar el comando vinculado durante el tiempo de ejecución. Como el método de ejecución no tiene parámetros, el comando debe estar preconfigurado con esa información o ser capaz de conseguirla por su cuenta.

En el editor ya no hacen falta subclases de botón: basta un campo en la clase base `Botón` que almacene una referencia al comando y lo ejecute al hacer clic. Menús, atajos y diálogos se implementan igual, vinculando los elementos de una misma operación al mismo comando y evitando duplicación. Los comandos se vuelven una capa intermedia que reduce el acoplamiento entre GUI y lógica de negocio.

## Analogía en el mundo real

Un pedido en un restaurante. El camarero anota el pedido en un papel, lo lleva a la cocina y lo pega a la pared; el chef lo lee y prepara la comida. El pedido en papel hace de comando: permanece en cola hasta que el chef está listo y contiene toda la información necesaria, de modo que el cocinero empieza de inmediato sin aclarar detalles directamente con el cliente.

## Estructura

1. La clase **Emisora** (o invocadora) inicia las solicitudes. Tiene un campo con referencia a un comando y lo activa en lugar de enviar la solicitud directamente al receptor. No es responsable de crear el comando: normalmente lo recibe precreado del cliente por el constructor.
2. La interfaz **Comando** declara un único método para ejecutar el comando.
3. Los **Comandos Concretos** implementan distintos tipos de solicitudes. No hacen el trabajo por su cuenta, sino que pasan la llamada a un objeto de la lógica de negocio; aunque por simplicidad pueden fusionarse. Los parámetros para ejecutar el método del receptor se declaran como campos; los comandos pueden hacerse inmutables inicializándolos solo por el constructor.
4. La clase **Receptora** contiene la lógica de negocio. Casi cualquier objeto puede ser receptor; el comando solo gestiona cómo se le pasa la solicitud, mientras el receptor hace el trabajo real.
5. El **Cliente** crea y configura los comandos concretos, pasando todos los parámetros (incluida una instancia del receptor) por el constructor, y luego asocia el comando a uno o varios emisores.

## Pseudocódigo

El ejemplo rastrea el historial de operaciones y permite revertir una operación. Los comandos que cambian el estado del editor (cortar, pegar) realizan una copia de seguridad antes de ejecutarse; al ejecutarse se colocan en una pila (historial) junto a la copia del estado. Para deshacer, la aplicación toma el comando más reciente, lee la copia asociada y la restaura.

La clase base `Command` define `saveBackup()`, `undo()` y un `execute()` abstracto que devuelve verdadero o falso según cambie o no el estado. `CopyCommand.execute()` copia la selección al portapapeles y devuelve `false` (no entra al historial). `CutCommand` y `PasteCommand` hacen `saveBackup()`, operan sobre el editor y devuelven `true`. `UndoCommand` llama a `app.undo()`. `CommandHistory` es una pila con `push`/`pop`. `Editor` actúa como receptor (`getSelection`, `deleteSelection`, `replaceSelection`), y `Application` actúa como emisor: en `createUI()` crea comandos y los asocia a botones y atajos (Ctrl+C, Ctrl+X, Ctrl+V, Ctrl+Z); `executeCommand` ejecuta y, si procede, apila el comando. El código cliente no se acopla a clases concretas porque trabaja a través de la interfaz, lo que permite añadir nuevos comandos sin descomponer el existente.

## Aplicabilidad

- Cuando quieras **parametrizar objetos con operaciones**: Command convierte una llamada a un método en un objeto autónomo que puedes pasar como argumento, almacenar o cambiar en tiempo de ejecución (por ejemplo, opciones configurables de un menú contextual).
- Cuando quieras **poner operaciones en cola, programarlas o ejecutarlas de forma remota**: un comando puede serializarse a una cadena, guardarse en archivo o base de datos y restaurarse luego, lo que permite diferir, encolar, registrar o enviar comandos por la red.
- Cuando quieras **implementar operaciones reversibles**: Command es quizá la forma más popular de hacer deshacer/rehacer, mediante un historial que guarda los comandos ejecutados y copias del estado. Desventajas: guardar el estado es difícil si parte es privado (se mitiga con **Memento**) y las copias consumen mucha RAM; como alternativa el comando puede realizar la operación inversa, aunque eso también puede ser difícil o imposible.

## Cómo implementarlo

1. Declara la interfaz de comando con un único método de ejecución.
2. Extrae las solicitudes a clases concretas de comando con campos para los argumentos y referencias al receptor, inicializados por el constructor.
3. Identifica las clases emisoras, añádeles un campo para el comando y haz que se comuniquen solo a través de la interfaz; normalmente reciben los comandos del cliente.
4. Cambia las emisoras para que ejecuten el comando en lugar de enviar la solicitud al receptor.
5. El cliente inicializa en orden: crear receptores, crear comandos y asociarlos a receptores, crear emisores y asociarlos a comandos.

## Pros y contras

- Principio de responsabilidad única: desacoplas las clases que invocan operaciones de las que las realizan.
- Principio de abierto/cerrado: introduces nuevos comandos sin descomponer el código cliente existente.
- Puedes implementar deshacer/rehacer y la ejecución diferida de operaciones.
- Puedes ensamblar comandos simples en uno complejo.
- Contra: el código puede complicarse por la nueva capa entre emisores y receptores.

## Relaciones con otros patrones

- **Chain of Responsibility, Command, Mediator y Observer** conectan emisores y receptores de distinta forma: la cadena pasa la solicitud secuencialmente hasta que alguien la gestiona; Command establece conexiones unidireccionales; Mediator fuerza la comunicación indirecta vía un mediador; Observer permite suscripción/baja dinámica.
- Los manejadores de **Chain of Responsibility** pueden implementarse como Comandos, o bien la propia solicitud ser un Comando que se ejecuta en varios contextos de la cadena.
- **Command + Memento** implementan "deshacer": el comando ejecuta operaciones sobre un objeto destino y el memento guarda su estado previo.
- **Command y Strategy** se parecen porque ambos parametrizan con una acción, pero difieren: Command convierte cualquier operación en objeto (para aplazar, encolar, historial, servicios remotos), mientras Strategy describe distintas formas de hacer lo mismo e intercambiables en una clase contexto.
- **Prototype** ayuda a guardar copias de comandos en un historial.
- **Visitor** puede verse como una versión potente de Command, cuyos objetos ejecutan operaciones sobre objetos de distintas clases.

## Ideas clave

- Command encapsula una solicitud como objeto con una interfaz de ejecución común, desacoplando emisor y receptor.
- El emisor solo activa el comando; no crea el comando ni conoce al receptor (eso lo hace el cliente).
- Un mismo comando puede vincularse a varios disparadores (botón, menú, atajo) evitando duplicar código.
- Los comandos concretos delegan el trabajo real en el receptor; sus parámetros se guardan como campos, idealmente inmutables.
- El historial (pila de comandos) más copias de estado habilita deshacer/rehacer; alternativa: operación inversa.
- Serializar comandos permite encolarlos, programarlos, registrarlos o enviarlos por la red.
- Respeta los principios de responsabilidad única y abierto/cerrado, a costa de una capa intermedia adicional.
