# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 2 — Principles in Refactoring (Principios de la refactorización)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Tras el ejemplo del capítulo 1, Fowler da un paso atrás para fijar los principios de la refactorización: qué es, por qué y cuándo hacerla, sus límites y su relación con el diseño y el rendimiento. La tesis central es que un buen diseño es esencial para desarrollar software con rapidez, y que la refactorización es la herramienta que impide que el diseño se degrade con el tiempo e incluso lo mejora.

El término tiene dos acepciones. Como sustantivo, un *refactoring* es un cambio en la estructura interna del software para hacerlo más fácil de entender y más barato de modificar, sin alterar su comportamiento observable. Como verbo, *refactorizar* es reestructurar el software aplicando una serie de refactorings sin cambiar ese comportamiento. Un refactoring suele ser un cambio pequeño, aunque puede implicar otros (por ejemplo, Extract Class suele involucrar Move Method y Move Field).

Sales sabiendo que refactorizar no es simplemente "limpiar código": es una técnica para hacerlo de forma más eficiente y controlada, minimizando errores y probando en cada oportunidad. Dos matices importantes: el propósito es facilitar la comprensión y modificación (a diferencia de la optimización de rendimiento, que suele hacer el código más difícil de entender), y nunca cambia el comportamiento observable para ningún usuario.

## Los dos sombreros

Kent Beck propone la metáfora de los dos sombreros. Al desarrollar con refactorización repartes el tiempo entre dos actividades distintas: añadir función y refactorizar. Cuando añades función, no cambias el código existente, solo agregas capacidades, y mides el progreso con tests nuevos que pasan. Cuando refactorizas, no añades función ni tests (salvo que descubras un caso que te faltaba), solo reestructuras; cambias los tests únicamente si un cambio de interfaz lo exige. Durante el desarrollo cambias de sombrero con frecuencia, pero siempre debes saber cuál llevas puesto.

## Por qué deberías refactorizar

No es una bala de plata, pero sí una herramienta valiosa para varios fines:

- **Mejora el diseño del software.** Sin refactorización el diseño se degrada: los cambios para metas a corto plazo o sin comprensión plena van borrando la estructura. Un aspecto clave es eliminar código duplicado para que el código diga todo "una vez y solo una vez", esencia del buen diseño. Reducir código no acelera la ejecución, pero facilita mucho la modificación correcta.
- **Hace el software más fácil de entender.** Programar es en parte una conversación: hay un segundo lector (el programador futuro, a menudo tú mismo) que es el usuario más importante. Ralph Johnson describe las primeras refactorizaciones como limpiar la suciedad de una ventana para poder ver más allá.
- **Ayuda a encontrar bugs.** Al clarificar la estructura se clarifican las suposiciones, y los errores se vuelven visibles.
- **Ayuda a programar más rápido.** Aunque parezca contraintuitivo, un buen diseño es esencial para el desarrollo rápido; la refactorización mantiene la velocidad al impedir que el diseño decaiga.

## Cuándo deberías refactorizar

Fowler se opone a reservar tiempo específico para refactorizar: se hace todo el tiempo, en pequeñas ráfagas, porque quieres hacer otra cosa y refactorizar te ayuda a hacerla.

- **La regla de tres** (guía de Don Roberts): la primera vez lo haces; la segunda, haces la duplicación aunque te moleste; la tercera vez que haces algo similar, refactorizas. *"Three strikes and you refactor"* (PDF p. 49).
- **Al añadir función:** para entender el código que vas a tocar y porque un diseño que no encaja con la nueva característica se arregla antes de añadirla; suele ser lo más rápido.
- **Al corregir un bug:** si llega un informe de error, es señal de que el código no era lo bastante claro para verlo.
- **Al hacer revisiones de código:** la refactorización hace la revisión más concreta (las sugerencias se implementan en el momento). Recomienda grupos pequeños: un revisor con el autor para código, y grupos mayores con diagramas UML y tarjetas CRC para diseño. El límite de esta idea es el *pair programming* de Extreme Programming: revisión continua plegada en el desarrollo.

## Por qué funciona la refactorización (Kent Beck)

Los programas tienen dos valores: lo que hacen hoy y lo que podrán hacer mañana. Cuatro cosas vuelven un programa difícil de modificar: que sea difícil de leer, que tenga lógica duplicada, que exija cambiar código en ejecución para añadir comportamiento, y que tenga lógica condicional compleja. Refactorizar es tomar un programa que funciona y añadirle valor dándole esas cualidades, sin cambiar su comportamiento.

## Qué le digo a mi jefe

Con un gerente orientado a la calidad, enfatiza la calidad y usa la refactorización dentro del proceso de revisión. Con uno orientado al calendario, el consejo más polémico: no se lo digas. El trabajo del profesional es construir software eficaz lo más rápido posible, y refactorizar es la vía más rápida; cómo lo hace es asunto suyo.

## Indirección y refactorización (Kent Beck)

La mayoría de las refactorizaciones introducen más indirección (parten objetos y métodos grandes en varios pequeños). La indirección es un arma de doble filo, pero se paga sola cuando sirve para compartir lógica, explicar intención e implementación por separado, aislar el cambio o codificar lógica condicional (mensajes polimórficos en vez de condicionales explícitos). El juego de la refactorización: manteniendo el comportamiento actual, ¿cómo hacer el sistema más valioso aumentando su calidad o reduciendo su costo? Hay una variante inversa: quitar la indirección parasitaria que ya no se paga sola. Esto contrasta con el diseño especulativo por adelantado, donde es fácil equivocarse.

## Problemas con la refactorización

Sección breve y tentativa: se conocen los beneficios, no todos los límites.

- **Bases de datos:** las aplicaciones suelen estar acopladas al esquema y la migración de datos es costosa. Con bases no orientadas a objetos, interponer una capa separada entre modelo de objetos y modelo de datos; puedes crearla cuando notes partes volátiles. Las bases orientadas a objetos ayudan y estorban; usa accesores para dar la ilusión de que el dato se movió.
- **Cambiar interfaces:** mientras controles a todos los que llaman, puedes cambiar la interfaz. El problema es la *interfaz publicada* (un paso más allá de pública). Si una refactorización cambia una interfaz publicada, conserva la vieja y la nueva (que la vieja llame a la nueva, sin copiar el cuerpo), y marca con *deprecated* en Java. Caso en Java: añadir una excepción al `throws` no es cambio de firma y no se cubre con delegación. *"Don't publish interfaces prematurely"* (PDF p. 55).
- **Cambios de diseño difíciles de refactorizar:** su enfoque es imaginar la refactorización; si parece fácil, elige el diseño más simple; si no, invierte más esfuerzo en el diseño.

## Cuándo no deberías refactorizar

Cuando conviene reescribir desde cero: código tan desordenado que empezar de nuevo sería más fácil, o código que directamente no funciona (hay que recordar que debe funcionar en su mayoría antes de refactorizar). Vía intermedia: refactorizar en componentes con fuerte encapsulación y decidir refactor-vs-reconstruir componente a componente. También cuando estás cerca de una fecha límite: Ward Cunningham lo describe como deuda, con sus intereses (mantenimiento más costoso por código complejo), que conviene gestionar. Fuera de un plazo inminente, no tener tiempo suele ser señal de que necesitas refactorizar.

## Refactorización y diseño

La refactorización complementa el diseño y cambia su papel. Sin ella, hay mucha presión por acertar el diseño por adelantado porque los cambios posteriores son caros; con ella, el diseño inicial solo busca una solución razonable. El resultado es un movimiento hacia la simplicidad: en vez de implementar soluciones flexibles (que cuestan complejidad y mantenimiento), preguntas "¿qué tan difícil será refactorizar la solución simple hacia la flexible?"; si es fácil, construyes lo más simple que funcione.

## Refactorización y rendimiento

Refactorizar suele hacer el programa más lento a corto plazo, pero lo hace más susceptible de afinarse. Tres enfoques para software rápido: presupuesto de tiempo (sistemas de tiempo real duro, como marcapasos), atención constante (común pero poco eficaz: dispersa optimizaciones y dificulta el desarrollo) y optimización tardía con perfilador. El dato clave: los programas gastan la mayor parte del tiempo en una fracción pequeña del código; optimizarlo todo por igual desperdicia el 90 por ciento del esfuerzo. El enfoque recomendado es construir bien factorizado, perfilar para hallar los *hot spots* y optimizarlos en pasos pequeños (compilar, probar, reperfilar, y deshacer si no mejora). Un programa bien factorizado da más tiempo para afinar y granularidad más fina.

Dos historias lo ilustran. En "It Takes Awhile to Create Nothing" (Ron Jeffries), el equipo especuló sobre la lentitud del proceso de nómina de Chrysler, pero al medir con el perfilador de Kent descubrió que el sistema pasaba la mitad del tiempo creando fechas, casi todas rangos vacíos; una constante de rango vacío duplicó la velocidad en cinco minutos. Lección: mide el rendimiento, no especules. En "Optimizing a Payroll System" (Rich Garzaniti), al migrar a GemStone el mayor culpable era la creación repetida de cadenas de 12.000 bytes; cachear y luego escribir directo a un file stream, junto con hilos múltiples (posibles en tres días por estar bien factorizado), bajó la nómina de más de 1.000 horas estimadas a un par de horas.

## De dónde vino la refactorización

Fowler no fija el origen exacto del término. Ward Cunningham y Kent Beck, trabajando con Smalltalk desde los años 80, reconocieron pronto su importancia (Kent lo llama hoy Extreme Programming). Ralph Johnson (uno de la Gang of Four) la exploró para frameworks; su doctorando Bill Opdyke investigó refactorizaciones que preservan la semántica en C++ y escribió la tesis más sustancial hasta la fecha (aporta el capítulo 13). John Brant y Don Roberts llevaron las ideas de herramientas más lejos con el Refactoring Browser para Smalltalk (capítulo 14). Fowler escribió el libro porque, pese a convencerse de su importancia al trabajar con Kent, no existía uno para dárselo a un programador en activo.

## Ideas clave

- Refactoring (sustantivo): cambio en la estructura interna para entender y modificar más barato, sin alterar el comportamiento observable; refactorizar (verbo): aplicar una serie de ellos.
- Los dos sombreros: añadir función y refactorizar son actividades separadas; sé consciente de cuál llevas puesto.
- Refactorizar mejora el diseño, la comprensión, ayuda a encontrar bugs y, en conjunto, acelera el desarrollo al frenar la degradación del diseño.
- No se agenda: se hace en pequeñas ráfagas; regla de tres, al añadir función, al corregir bugs y en revisiones de código.
- La indirección se paga sola si comparte lógica, separa intención de implementación, aísla el cambio o codifica condicionales como mensajes.
- Límites: bases de datos, interfaces publicadas (conserva la vieja llamando a la nueva) y ciertos cambios de diseño; a veces conviene reescribir o no refactorizar ante un plazo (deuda técnica).
- La refactorización empuja hacia diseños simples: implementa lo simple si refactorizar hacia lo flexible será fácil.
- Para el rendimiento: construye bien factorizado y afina tarde con perfilador; mide, no especules.
