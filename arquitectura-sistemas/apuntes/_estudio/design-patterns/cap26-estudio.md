# Chain of Responsibility (Cadena de responsabilidad) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Chain of Responsibility y qué permite hacer?
R: Es un patrón de diseño de comportamiento que permite pasar solicitudes a lo largo de una cadena de manejadores; cada manejador decide si la procesa o la pasa al siguiente.

P: ¿Qué otros nombres recibe el patrón?
R: Cadena de responsabilidad, CoR o Chain of Command.

P: ¿Cuál es la tesis central del patrón?
R: Transformar comportamientos particulares en objetos autónomos llamados manejadores, cada uno con una clase propia y un único método de procesamiento, vinculados en una cadena donde cada uno referencia al siguiente.

P: ¿Qué puede hacer un manejador además de procesar y reenviar la solicitud?
R: Puede decidir no pasar la solicitud más allá y detener así el procesamiento.

P: ¿En qué consiste la variante más estandarizada del patrón?
R: Al recibir la solicitud, el manejador decide si puede procesarla; si puede, no la pasa más allá, de modo que un único manejador la procesa o no la procesa ninguno (típica en eventos GUI).

P: ¿Cuáles son los cuatro elementos de la estructura del patrón?
R: La clase Manejadora (interfaz común), la ManejadoraBase (opcional, con boilerplate), los Manejadores Concretos (procesan solicitudes) y el Cliente (compone la cadena).

P: ¿Qué papel cumple la clase ManejadoraBase?
R: Es opcional y aloja el código boilerplate común: suele definir el campo de referencia al siguiente manejador y puede implementar el reenvío por defecto tras comprobar su existencia.

P: ¿Cómo son habitualmente los Manejadores Concretos?
R: Autónomos e inmutables, y reciben toda la información necesaria por el constructor.

P: ¿Desde qué manejador puede el cliente enviar la solicitud?
R: Desde cualquier manejador de la cadena; no tiene por qué ser el primero.

P: ¿Qué requisito es fundamental para todas las clases manejadoras?
R: Que implementen la misma interfaz.

P: ¿Cuáles son los pros del patrón?
R: Controlas el orden de control de solicitudes, cumples el principio de responsabilidad única (desacoplas invocadores de ejecutores) y el de abierto/cerrado (añades manejadores sin tocar el cliente).

P: ¿Cuál es la principal contra del patrón?
R: Algunas solicitudes pueden acabar sin ser gestionadas.

P: ¿Cómo se relacionan CoR y Composite?
R: Un componente hoja puede pasar la solicitud por la cadena de componentes padre hasta la raíz del árbol; siempre se puede extraer una cadena de un árbol de objetos.

P: ¿En qué se diferencian CoR y Decorator pese a su estructura similar?
R: Ambos usan composición recursiva, pero los manejadores de CoR ejecutan operaciones arbitrarias e independientes y pueden dejar de pasar la solicitud; los decoradores extienden el comportamiento manteniendo la interfaz base y no pueden romper el flujo.

## Preguntas de autoevaluación

P: ¿Por qué el sistema de pedidos online termina necesitando refactorizarse con CoR?
R: Porque al crecer el código, un cambio en una comprobación afecta a las demás y reutilizarlas obliga a duplicar código, ya que cada componente necesita parte de las comprobaciones pero no todas, volviéndolo difícil de mantener. (Sección «El ejemplo que recorre el capítulo»)

P: ¿Qué comprobaciones se añaden con el tiempo al ejemplo de pedidos?
R: Un paso de validación para sanear datos, un filtro contra fuerza bruta que bloquea solicitudes fallidas repetidas desde la misma IP, y una caché que deja pasar la solicitud solo si no hay respuesta adecuada en caché. (Sección «El ejemplo que recorre el capítulo»)

P: ¿En qué casos conviene aplicar el patrón?
R: Cuando los tipos de solicitudes y su secuencia no se conocen de antemano, cuando es fundamental ejecutar varios manejadores en un orden específico, y cuando el grupo de manejadores y su orden deben cambiar en tiempo de ejecución. (Sección «Aplicabilidad»)

P: En el pseudocódigo, ¿qué hace un componente simple cuando no tiene texto de ayuda asignado?
R: Reenvía la llamada a su contenedor (`container.showHelp()`), y la solicitud emerge por los contenedores hasta el elemento capaz de mostrar la ayuda. (Sección «Pseudocódigo»)

P: ¿Qué debe prever el cliente por la naturaleza dinámica de la cadena?
R: Cadenas de un único vínculo, solicitudes que no llegan al final y solicitudes que llegan al final sin ser gestionadas. (Sección «Cómo implementarlo»)

P: ¿Cómo ilustra la analogía del soporte técnico el funcionamiento del patrón?
R: La llamada pasa por un contestador automático, luego un operador humano y finalmente un ingeniero; cada eslabón procesa la solicitud o la pasa al siguiente. (Sección «Analogía en el mundo real»)

P: ¿Cómo distingue el capítulo a CoR de Command, Mediator y Observer?
R: CoR pasa la solicitud secuencialmente por una cadena dinámica hasta que uno la gestiona; Command establece conexiones unidireccionales; Mediator comunica indirectamente mediante un mediador; Observer permite suscribirse o darse de baja dinámicamente. (Sección «Relaciones con otros patrones»)

## Puntos a dominar

- Reconocer CoR como patrón de comportamiento que encadena manejadores con una interfaz común.
- Explicar que cada manejador decide si procesa la solicitud y si la reenvía, pudiendo detener la cadena.
- Diferenciar la variante donde todos los manejadores participan de la variante donde un único manejador procesa o ninguno (eventos GUI).
- Identificar los cuatro elementos de la estructura: Manejadora, ManejadoraBase opcional, Manejadores Concretos y Cliente.
- Enumerar los pasos de implementación: interfaz, clase base abstracta, subclases concretas, ensamblaje por el cliente y envío desde cualquier eslabón.
- Justificar los pros (orden de control, responsabilidad única, abierto/cerrado) y la contra (solicitudes sin gestionar).
- Relacionar CoR con Composite y distinguirlo de Decorator por su capacidad de romper el flujo de la solicitud.
