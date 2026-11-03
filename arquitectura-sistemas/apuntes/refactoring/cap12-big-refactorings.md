# Refactoring: Improving the Design of Existing Code — Martin Fowler (con Kent Beck, John Brant, William Opdyke y Don Roberts) (Addison-Wesley, 1999)
## Capítulo 12 — Big Refactorings (Grandes refactorizaciones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Los capítulos anteriores muestran los "movimientos" individuales de refactorización; aquí falta la sensación del "juego" completo. Este capítulo, escrito por Kent Beck y Martin Fowler, trata de las grandes refactorizaciones: cambios de diseño a gran escala que no se describen con mecánicas tan precisas como las pequeñas, porque cada situación cambia demasiado. No pueden decirte exactamente qué hacer porque no saben qué verás cuando lo hagas.

La tesis central es que estas refactorizaciones toman tiempo (meses o años sobre sistemas en producción), carecen de la gratificación instantánea de las pequeñas y exigen cierto grado de acuerdo en todo el equipo de programación, que debe reconocer que una gran refactorización está "en juego" y actuar en consecuencia. No se completan de una vez: se avanza poco a poco, guiado por la necesidad de añadir funcionalidad o corregir errores, haciendo solo lo necesario para la tarea real.

Son importantes porque sin ellas corres el riesgo de invertir esfuerzo en refactorizar sin obtener el beneficio. La acumulación de decisiones de diseño a medio entender acaba ahogando un programa como la maleza ahoga un canal; refactorizando aseguras que tu comprensión plena del diseño siempre quede reflejada en el programa. Sales sabiendo cuatro ejemplos de gran refactorización y la filosofía para abordarlas a lo largo del tiempo.

## La naturaleza del juego

Refactorizas con un propósito, no solo para evitar progresar. Las grandes refactorizaciones fijan la dirección de muchísimos cambios. Cuesta convencer a los gerentes de detener el progreso un par de meses para ordenar, así que hay que "mordisquear los bordes" como Hansel y Gretel: un poco hoy, un poco más mañana. Siempre puedes volver mañana. Como ejemplo, Fowler intentó mostrar cada refactorización completa y habría requerido cien páginas por cada una, así que los ejemplos se comprimieron en diagramas esquemáticos.

## Tease Apart Inheritance (Separar la herencia)

Tienes una jerarquía de herencia que hace dos trabajos a la vez. Solución: crear dos jerarquías y usar delegación para invocar una desde la otra.

La herencia mal usada se cuela poco a poco: un día añades una subclase, al mes nadas en espagueti. La herencia enredada causa duplicación de código, dificulta los cambios y vuelve el código difícil de entender. Se detecta fácilmente: si cada clase en un nivel tiene subclases que empiezan con el mismo adjetivo, probablemente haces dos trabajos con una jerarquía.

Mecánica resumida:
- Identifica los distintos trabajos y dibújalos en una cuadrícula con un eje por trabajo.
- Decide qué trabajo es más importante (se queda en la jerarquía actual) y cuál se mueve a otra.
- Usa Extract Class en la superclase común para crear un objeto del trabajo subsidiario y añade una variable de instancia.
- Crea subclases del objeto extraído por cada subclase original e inicialízalas.
- Usa Move Method para mover el comportamiento de cada subclase al objeto extraído; cuando la subclase queda vacía, elimínala.
- Continúa y busca más refactorizaciones (Pull Up Method, Pull Up Field).

Ejemplo: la jerarquía `Deal` nació para mostrar un solo trato; luego se añadieron subclases para tablas (`Active Deal`, `Passive Deal`, `Tabular Deal`). Como la "dealidad" del objeto importa más que el estilo de presentación, se deja `Deal` y se extrae el estilo de presentación a su propia jerarquía. Tras mover métodos y campos, las subclases tabulares quedan vacías y se eliminan. Al final, las diferencias de presentación pueden capturarse con un par de variables, sin necesidad de subclases. A veces hay que dar un paso atrás (más clases) para luego dar dos adelante.

## Convert Procedural Design to Objects (Convertir diseño procedural a objetos)

Tienes código escrito en estilo procedural. Solución: convierte los registros de datos en objetos, descompón el comportamiento y muévelo a los objetos.

Usar objetos bien lleva tiempo; usar Java no basta (un cliente exigió usar Java pero no usar objetos). La situación típica: métodos largos y procedurales sobre una clase con pocos datos, y objetos de datos tontos con solo accesores. No se niega que a veces convenga tener objetos con comportamiento y pocos datos (pequeños objetos *strategy* para variar comportamiento), pero suelen ser pequeños y usados por necesidad de flexibilidad.

Mecánica resumida:
- Convierte cada tipo de registro en un objeto de datos tonto con accesores (cada tabla de una base relacional, un objeto de datos tonto).
- Pon todo el código procedural en una sola clase (singleton para reinicializar, o métodos estáticos).
- Aplica Extract Method a cada procedimiento largo y Move Method para llevar cada pieza a la clase de datos apropiada.
- Continúa hasta vaciar la clase original; si era puramente procedural, es muy gratificante borrarla.

Ejemplo: el del Capítulo 1, especialmente la primera fase, donde el método `statement` se descompone y distribuye.

## Separate Domain from Presentation (Separar dominio de presentación)

Tienes clases de GUI que contienen lógica de dominio. Solución: separa la lógica de dominio en clases de dominio aparte.

El núcleo de model-view-controller (MVC), que sustentó la relación entre GUI y objetos de dominio en Smalltalk-80, es separar el código de interfaz (la vista o presentación) de la lógica de dominio (el modelo). Las clases de presentación contienen solo lógica de interfaz; los objetos de dominio no contienen código visual pero sí toda la lógica de negocio. Esto separa dos partes complicadas, facilita modificarlas y permite múltiples presentaciones de la misma lógica. La mayoría de entornos cliente-servidor con GUI usan un diseño de dos capas: datos en la base y lógica en las clases de presentación.

Mecánica resumida:
- Crea una clase de dominio por ventana; si hay una rejilla, crea una clase para las filas y una colección en la clase de dominio de la ventana.
- Examina los datos de la ventana: si solo son de interfaz, déjalos; si son de dominio pero no se muestran, muévelos con Move Method; si los usan ambos, usa Duplicate Observed Data para mantenerlos sincronizados.
- Examina la lógica de la clase de presentación: usa Extract Method para separar lógica de presentación de la de dominio y Move Method para moverla al objeto de dominio.
- Al terminar tendrás clases de presentación que manejan la GUI y objetos de dominio con toda la lógica de negocio (aún no bien factorizados).

Ejemplo: un programa de entrada y tarificación de pedidos con todo en una sola clase `Order Window`. Se trabaja desde la ventana, no desde la base de datos, porque el mayor riesgo es mezclar presentación y dominio. Un buen motor es mover todas las llamadas SQL a la clase de dominio; retirar el `import` de `java.sql` de la ventana da sensación de cierre. Hay que atender primero al mayor riesgo.

## Extract Hierarchy (Extraer jerarquía)

Tienes una clase que hace demasiado, en parte por muchas sentencias condicionales. Solución: crea una jerarquía de clases donde cada subclase represente un caso especial.

En diseño evolutivo es común que una clase acabe implementando varias ideas: un flag aquí, unas pruebas allá, y un año después hay banderas y condicionales por todas partes (una clase "navaja suiza"). La estrategia funciona solo si la lógica condicional permanece estática durante la vida del objeto; si no, puede hacer falta Extract Class antes. No te desanimes: puede tomar semanas o meses; haz los pasos fáciles y obvios y toma un descanso.

Dos mecánicas:
- Cuando no tienes claras las variaciones (un paso a la vez): identifica una variación; crea una subclase para ese caso y usa Replace Constructor with Factory Method; copia los métodos con lógica condicional a la subclase y simplifícalos; continúa aislando casos hasta poder declarar la superclase abstracta.
- Cuando las variaciones son claras desde el inicio: crea una subclase por variación; usa Replace Constructor with Factory Method; si hay un type code, usa Replace Type Code with Subclasses (o with State/Strategy si cambia durante la vida); aplica Replace Conditional with Polymorphism.

Ejemplo: un programa que calcula una factura eléctrica. La clase `Billing Scheme` tiene mucha lógica condicional (verano/invierno; planes residencial, pequeño negocio, lifeline por Seguridad Social, y discapacidad). Se elige una variación recurrente (discapacidad), se aplica Replace Constructor with Factory Method, se devuelve un esquema de discapacidad cuando corresponde y se copia `createBill` a la subclase. Allí se simplifica: `if (disabilityScheme()) doSomething` se reduce a `doSomething`. Con Extract Method y Decompose Conditional se separa lo que varía de lo que no. Al abordar la segunda variación (lifeline), se alinean las firmas de métodos con igual intención; con más variaciones el patrón se estabiliza y las siguientes se vuelven más fáciles.

## Ideas clave

- Las grandes refactorizaciones carecen de mecánicas precisas porque cada enredo es distinto; toman tiempo y requieren fe en un progreso diario.
- Se avanza "mordisqueando los bordes", guiado por la necesidad de añadir funciones o corregir bugs, sin obligación de terminar de una vez.
- Exigen acuerdo de todo el equipo: una gran refactorización "en juego" marca la dirección de muchos cambios.
- Importan porque la acumulación de decisiones de diseño a medio entender ahoga el programa como la maleza un canal.
- Tease Apart Inheritance: separa una jerarquía que hace dos trabajos en dos jerarquías con delegación; a menudo la extraída se simplifica luego hasta eliminar subclases.
- Convert Procedural Design to Objects: datos tontos con accesores, luego Extract Method y Move Method para distribuir el comportamiento.
- Separate Domain from Presentation: aplica MVC separando vista y modelo; usa Duplicate Observed Data para campos usados por ambos y mueve el SQL al dominio.
- Extract Hierarchy: convierte una clase "navaja suiza" llena de condicionales en subclases por caso especial, usando factory methods y Replace Conditional with Polymorphism.
