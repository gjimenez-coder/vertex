# Command (Comando) — Estudio

## Tarjetas de repaso

P: ¿Qué es el patrón Command? / R: Un patrón de comportamiento que convierte una solicitud en un objeto independiente que contiene toda la información sobre ella, permitiendo parametrizar métodos, encolar o diferir su ejecución y soportar operaciones reversibles.

P: ¿Cuál es la tesis central del patrón? / R: Desacoplar el objeto que invoca una operación (emisor) del que la realiza (receptor), colocando entre ambos un objeto comando con una interfaz común.

P: ¿Qué información se extrae a la clase comando? / R: Todos los detalles de la solicitud: el objeto invocado, el nombre del método y la lista de argumentos.

P: ¿Cómo suele ser la interfaz Comando? / R: Normalmente declara un único método de ejecución sin parámetros, por lo que el comando debe estar preconfigurado con la información o ser capaz de conseguirla por su cuenta.

P: ¿Qué responsabilidad tiene la clase Emisora (invocadora)? / R: Inicia las solicitudes activando el comando al que referencia, en lugar de enviar la solicitud directamente al receptor; no es responsable de crear el comando.

P: ¿Qué hacen los Comandos Concretos? / R: Implementan distintos tipos de solicitudes, pero no hacen el trabajo por su cuenta: pasan la llamada a un objeto de la lógica de negocio (el receptor); sus parámetros se guardan como campos.

P: ¿Qué papel cumple la clase Receptora? / R: Contiene la lógica de negocio y hace el trabajo real; casi cualquier objeto puede ser receptor, porque el comando solo gestiona cómo se le pasa la solicitud.

P: ¿Qué tareas realiza el Cliente en este patrón? / R: Crea y configura los comandos concretos pasando todos los parámetros (incluido el receptor) por el constructor, y luego asocia cada comando a uno o varios emisores.

P: ¿Cómo evita Command la duplicación de código en GUI? / R: Vinculando los elementos de una misma operación (botón, menú, atajo) al mismo comando, de modo que no se duplica la implementación en muchas clases.

P: ¿Cómo se implementa deshacer/rehacer con Command? / R: Con un historial (pila de comandos) y copias del estado: los comandos que cambian el estado hacen una copia de seguridad antes de ejecutarse y se apilan; para deshacer se toma el comando más reciente y se restaura su copia.

P: ¿Por qué el ejemplo del editor devuelve `false` en CopyCommand? / R: Porque copiar no cambia el estado del editor, así que el comando devuelve `false` y no entra al historial; cortar y pegar devuelven `true` tras hacer saveBackup().

P: ¿Qué permite serializar un comando? / R: Guardarlo como cadena en archivo o base de datos y restaurarlo luego, lo que habilita diferir, encolar, registrar o enviar comandos por la red.

P: ¿Cuál es la principal desventaja del patrón? / R: El código puede complicarse por la nueva capa intermedia que se introduce entre emisores y receptores.

P: ¿Qué principios SOLID respeta Command? / R: El principio de responsabilidad única (separa invocación de ejecución) y el principio de abierto/cerrado (se añaden comandos sin descomponer el código cliente).

## Preguntas de autoevaluación

P: ¿Qué problema concreto motiva el patrón en el ejemplo del editor de texto? / R: Crear una subclase de Botón por cada gestor de clic genera una cantidad enorme de subclases y riesgo de romper el código al modificar la clase base; además, operaciones como copiar/pegar deben invocarse desde varios lugares, obligando a duplicar la implementación. (Secciones "El ejemplo que recorre el capítulo" y "Problema")

P: ¿Por qué el emisor no queda acoplado a clases concretas de comando? / R: Porque todos los comandos implementan la misma interfaz con un método de ejecución común, lo que permite usar varios comandos con el mismo emisor e incluso cambiar el comando vinculado en tiempo de ejecución. (Sección "Solución")

P: ¿Qué papel juega el pedido en papel en la analogía del restaurante? / R: Hace de comando: permanece en cola hasta que el chef está listo y contiene toda la información necesaria para que el cocinero empiece sin aclarar detalles con el cliente. (Sección "Analogía en el mundo real")

P: En el pseudocódigo, ¿qué clases actúan como emisor y como receptor? / R: `Application` actúa como emisor (crea comandos y los asocia a botones y atajos, y los ejecuta) y `Editor` actúa como receptor (getSelection, deleteSelection, replaceSelection). (Sección "Pseudocódigo")

P: ¿En qué tres casos conviene aplicar Command según la aplicabilidad? / R: Para parametrizar objetos con operaciones, para poner operaciones en cola/programarlas/ejecutarlas de forma remota, y para implementar operaciones reversibles (deshacer/rehacer). (Sección "Aplicabilidad")

P: ¿Qué dificultades tiene guardar el estado para deshacer y cómo se mitigan? / R: Es difícil si parte del estado es privado (se mitiga con Memento) y las copias consumen mucha RAM; como alternativa el comando puede realizar la operación inversa, aunque también puede ser difícil o imposible. (Sección "Aplicabilidad")

P: ¿Cuál es el orden de inicialización que sigue el cliente al implementar el patrón? / R: Crear receptores, crear comandos y asociarlos a los receptores, y por último crear emisores y asociarlos a los comandos. (Sección "Cómo implementarlo")

P: ¿En qué se parecen y se diferencian Command y Strategy? / R: Ambos parametrizan con una acción; pero Command convierte cualquier operación en objeto (para aplazar, encolar, historial o servicios remotos), mientras Strategy describe distintas formas intercambiables de hacer lo mismo en una clase contexto. (Sección "Relaciones con otros patrones")

## Puntos a dominar

- Distinguir los cinco participantes del patrón: Emisor, interfaz Comando, Comandos Concretos, Receptor y Cliente, y quién crea y asocia cada pieza.
- Explicar cómo la interfaz de ejecución común desacopla emisor y receptor y evita subclases por cada acción.
- Justificar por qué un mismo comando puede vincularse a botón, menú y atajo sin duplicar código.
- Describir el mecanismo de historial (pila de comandos + copias de estado) para deshacer/rehacer y su alternativa por operación inversa.
- Reconocer los tres casos de aplicabilidad: parametrizar, encolar/diferir/remoto y operaciones reversibles.
- Relacionar Command con Chain of Responsibility, Mediator, Observer, Memento, Strategy, Prototype y Visitor según cómo conectan emisores y receptores.
- Identificar pros (responsabilidad única, abierto/cerrado, deshacer/rehacer, composición de comandos) y la contra de la capa intermedia adicional.
