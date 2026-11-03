# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 8 — Complexity (Complejidad)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo identifica la complejidad como la raíz de las historias de terror habituales en el desarrollo: proyectos que tras años de trabajo quedan obsoletos, equipos que no logran sacar una primera versión o productos que la competencia escribe mejor y más rápido. La tesis central es que la complejidad no crece de forma lineal, sino que se acumula sobre sí misma: cada función nueva debe coordinarse con todas las existentes, así que el coste de añadir funciones aumenta con el tamaño del sistema.

El autor enumera las formas en que se introduce complejidad, propone tres factores objetivos para detectar "tecnologías malas" antes de adoptarlas, y defiende que la complejidad irresoluble casi siempre delata un error de diseño en un nivel más profundo. Sales sabiendo cómo evitar añadir complejidad, cómo elegir tecnología, y cómo reducir la complejidad existente mediante rediseño en pasos pequeños en lugar de reescrituras.

La conclusión práctica es que un sistema bien diseñado y mantenido no tiene por qué reescribirse nunca; reescribir es, casi siempre, una admisión de fracaso de diseño.

## Cómo se añade complejidad

Empezar con requisitos tan complejos que nunca sale una primera versión es un error común; la solución es recortar funciones y mejorar con el tiempo. Más allá de añadir funciones, las vías más habituales de introducir complejidad son:

- **Expandir el propósito del software**: en general, nunca hacerlo. El software solo tiene que hacer bien lo que hace.
- **Añadir programadores**: sumar gente añade complejidad, no la quita (referencia a *The Mythical Man-Month* de Fred Brooks). Es más probable tener éxito con un grupo pequeño de expertos que con uno grande de inexpertos.
- **Cambiar cosas que no necesitan cambiarse**: todo cambio introduce posibilidad de bugs y costes de decisión, implementación, validación, seguimiento y pruebas. Hay que decidir de forma informada, no por capricho.
- **Quedar atado a tecnologías malas**: una tecnología es "mala" si te encierra, no será flexible para el futuro o no tiene la calidad necesaria.
- **Malentendido**: quien no entiende del todo su trabajo tiende a crear sistemas complejos, en un círculo vicioso. Entender bien los sistemas y herramientas permite diseños más simples.
- **Diseño pobre o ausencia de diseño**: en el fondo, "no planificar para el cambio". Con mal diseño, cada función multiplica la complejidad en vez de sumar un poco.
- **Reinventar la rueda**: inventar un protocolo cuando ya existe uno bueno malgasta tiempo. Solo es aceptable cuando: (a) necesitas algo que aún no existe, (b) todas las ruedas existentes son tecnologías que te encierran, (c) son incapaces de cubrir tus necesidades, o (d) no se mantienen y no puedes tomar su mantenimiento.

Todos estos factores dañan de forma gradual y a largo plazo, por eso parecen inofensivos al proponerlos; acumulados, conducen al "producto que nunca se entrega".

## Complejidad y propósito

El propósito básico de un sistema debería ser simple, lo que ayuda a mantenerlo simple en conjunto. Añadir funciones de otro propósito dispara la complejidad: un procesador de texto que además leyera el correo sería ridículamente complicado. También importa el propósito del usuario: idealmente el propósito del programa debe coincidir casi con las mismas palabras que usaría el usuario para describir el suyo. Enfureces al usuario interfiriendo en su propósito (ventanas emergentes, exceso de funciones, iconos extraños).

A veces marketing o gestión persiguen metas ajenas al propósito básico ("ser lindo", "usar la última tecnología"); esas personas no deben decidir qué hace el programa. El diseñador o gestor técnico es responsable de que no se viole el propósito. Productos muy exitosos lo son por ceñirse a un solo propósito: el jabón limpia, la sal sala, la bombilla ilumina.

## Tecnologías malas

Para saber si una tecnología es mala antes de usarla, se examinan tres factores:

- **Potencial de supervivencia (survival potential)**: probabilidad de que siga manteniéndose. Se evalúa por el historial reciente de versiones, la respuesta a reportes de bugs, la actividad de la comunidad y si hay un solo proveedor o adopción amplia. Sobre la **popularidad**: conviene, pero hay que distinguir lo válidamente popular (ejemplo: C, con múltiples estándares e implementaciones) de lo popular por monopolio o por obligación (caso de un solo proveedor).
- **Interoperabilidad**: facilidad para abandonar la tecnología. Si interactúas por una vía estándar (ejemplo: los estándares para hablar con una base de datos), cambiar a otro sistema que siga el mismo estándar requiere cambios menores; si no, quedas encerrado y tendrás que reescribir.
- **Atención a la calidad**: medida subjetiva; ver si el producto mejora en sus versiones recientes, si refactorizan y limpian el código y si han tenido muchas vulnerabilidades graves por mala programación.

Otros factores: la simplicidad, la idoneidad para tu propósito y la opinión personal cuando todo lo demás es igual.

## Complejidad y la solución equivocada

Cuando algo se vuelve muy complejo, suele haber un error de diseño en un nivel muy por debajo de donde aparece la complejidad. La analogía: es difícil hacer correr rápido un coche con ruedas cuadradas; afinar el motor no sirve, hay que rediseñar para que las ruedas sean redondas. Ante una "complejidad irresoluble", hay que retroceder y mirar qué subyace. Si el problema es que el código está desordenado, hay que limpiarlo primero.

**¿Qué problema intentas resolver?** Ante peticiones confusas ("¿cómo hago volar este poni a la luna?"), la pregunta correcta es "¿qué problema intentas resolver?". Al entenderlo del todo, la solución simple aparece. Hay que descartar suposiciones y preguntarse cómo debería resolverse ese tipo de problema en un mundo perfecto, no cómo resolverlo con el código actual.

## Problemas complejos

Algunos problemas son inherentemente complejos (corrector ortográfico, ajedrez por computadora). Eso no obliga a una solución compleja, pero exige más esfuerzo para simplificar. Ante la dificultad, conviene escribirlo en lenguaje llano o dibujarlo: la mayoría de los problemas de diseño difíciles se resuelven dibujándolos o escribiéndolos en papel; meterlos en el computador es un detalle menor.

## Manejar la complejidad

Para arreglar una parte demasiado compleja, se rediseñan las piezas individuales en pasos pequeños. Cada arreglo debe ser lo más pequeño posible sin introducir más complejidad: desde renombrar una variable o añadir comentarios, hasta dividir una pieza compleja en varias simples. El mayor peligro es que el propio arreglo añada complejidad; por eso fracasan tantas reescrituras. El método es concebir un sistema algo más simple que el actual y avanzar paso a paso hacia él, repitiendo el proceso; no existe el sistema "perfecto".

No se puede dejar de escribir funciones para dedicarse solo a rediseñar: la Ley del Cambio (Law of Change) obliga a adaptar la funcionalidad, so pena de perder usuarios. La mejor forma de equilibrar es rediseñar con el objetivo de facilitar una función concreta y luego implementarla, alternando rediseño y funciones; vale también para bugs.

**Rediseñar para una función (ejemplo Bugzilla)**: Bugzilla guardaba datos en un único sistema de base de datos (OldDB) y nuevos clientes querían usar otro (NewDB). En lugar de llenar el código de `if` (lo que duplicaría la complejidad para un equipo de pocos programadores a tiempo parcial), rediseñaron para soportar varias bases de datos: (1) usar comandos estándar donde fuera posible, un archivo a la vez; (2) crear funciones que devuelvan el comando correcto para los comandos no estándar; (3) dejar de usar funciones específicas de OldDB en favor de estándar; (4) rediseñar el instalador para cualquier base de datos. Cada paso es un proyecto subdividido, probado tras cada cambio. No dio un sistema perfecto, pero sí mejor y más mantenible; Bugzilla acabó soportando cuatro bases de datos.

**Hacer simple una pieza**: aquí entra todo el conocimiento de diseño (patrones, código heredado, herramientas de ingeniería); conocer varios lenguajes y librerías aporta formas distintas de pensar. Nunca aplicar una herramienta de forma robótica por autoridad; hacer lo correcto para el código y la situación. Si no conoces herramientas, la pregunta clave es: "¿cómo podría ser esto más fácil de manejar o más comprensible?".

**Complejidad irreparable**: parte de la complejidad es difícil de evitar (ejemplo: el hardware subyacente). El objetivo es ocultarla con un envoltorio simple de usar y entender.

## Reescribir

Reescribir un sistema desde cero es esencialmente una admisión de fracaso como diseñador. No es cierto que todo sistema deba reescribirse: es posible diseñar un sistema que nunca haya que tirar, igual que un rascacielos bien construido y mantenido no tiene por qué caerse. Reescribir solo es aceptable si se cumplen **todas** estas condiciones:

1. Una estimación precisa (con experimentos reales de rediseño, no conjeturas) muestra que reescribir es más eficiente que rediseñar.
2. Dispones de muchísimo tiempo para crear el nuevo sistema.
3. Eres mejor diseñador que el original, o tus habilidades mejoraron drásticamente.
4. Diseñarás el nuevo sistema en pasos simples, con usuarios que den feedback en cada paso.
5. Tienes recursos para mantener el sistema existente y diseñar el nuevo a la vez; nunca dejar de mantener un sistema en uso para reescribirlo, y contar tu propia atención como recurso.

Si no se cumplen todas, lo correcto es manejar la complejidad del sistema existente sin reescribir, mejorando el diseño en pasos simples.

## Ideas clave

- La complejidad se acumula sobre sí misma: cada función debe coordinarse con todas las existentes, por lo que el coste de añadir crece con el tamaño.
- Las vías para introducir complejidad incluyen expandir el propósito, añadir programadores, cambiar lo que no hace falta, tecnologías malas, malentendido, mal diseño y reinventar la rueda.
- El software debe ceñirse a su propósito básico y acercarlo al propósito del usuario; productos simples y enfocados tienen éxito.
- Una tecnología mala se detecta por bajo potencial de supervivencia, mala interoperabilidad (encierro) y poca atención a la calidad.
- La complejidad irresoluble delata un error de diseño en un nivel más profundo; primero pregunta qué problema se intenta resolver y descarta suposiciones.
- Se maneja la complejidad rediseñando en pasos pequeños, sin introducir más complejidad, alternando rediseño y funciones para no violar la Ley del Cambio.
- La complejidad inevitable (hardware) se oculta tras un envoltorio simple.
- Reescribir desde cero es una admisión de fracaso; solo es aceptable si se cumplen las cinco condiciones a la vez.
