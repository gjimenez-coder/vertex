# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 5 — Formatting (Formato)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo sostiene que el formato del código es demasiado importante para ignorarlo, pero también para tratarlo como un dogma. El formato es, ante todo, comunicación, y la comunicación es la primera prioridad del desarrollador profesional (PDF p. 107). La tesis central es que la funcionalidad de hoy cambiará, pero la legibilidad del código afecta a todos los cambios futuros: el estilo y la disciplina sobreviven aunque el código original desaparezca.

Sales sabiendo cómo dar forma vertical y horizontal a un archivo fuente: cuán largos deben ser los archivos, cómo separar y agrupar conceptos con líneas en blanco y densidad, cómo ordenar funciones y variables, cuán anchas deben ser las líneas, cuándo usar (y no usar) espacios y alineación, y por qué la indentación es imprescindible. Cierra con una idea organizativa clave: en un equipo, las reglas de formato las decide el equipo, no el individuo.

## Vertical Formatting (Formato vertical)

Sobre el tamaño de archivo: analizando siete proyectos (Junit, FitNesse, testNG, Time and Money, JDepend, Ant, Tomcat), se observa que es posible construir sistemas grandes (FitNesse ronda las 50.000 líneas) con archivos típicamente de 200 líneas y un límite superior de 500 (PDF p. 108). No es regla rígida, pero sí deseable: los archivos pequeños suelen ser más fáciles de entender.

- **La metáfora del periódico**: un archivo fuente debe leerse como un artículo de prensa. El nombre, simple y explicativo, actúa como titular; las partes superiores dan los conceptos y algoritmos de alto nivel, y el detalle aumenta a medida que se desciende, hasta encontrar al final las funciones de más bajo nivel (PDF p. 108-109).
- **Apertura vertical entre conceptos**: cada grupo de líneas es un pensamiento completo y debe separarse de los demás con líneas en blanco. La comparación entre `BoldWidget.java` con y sin líneas en blanco (Listing 5-1 y 5-2) muestra el efecto: sin ellas, el código se vuelve un amasijo (PDF p. 109-110).
- **Densidad vertical**: si la apertura separa conceptos, la densidad implica asociación estrecha. Las líneas muy relacionadas deben aparecer juntas. Los comentarios inútiles del `ReporterConfig` (Listing 5-3) rompen la asociación entre dos variables de instancia; la versión densa (Listing 5-4) entra "de un vistazo" (PDF p. 110-111).

## Vertical Distance (Distancia vertical)

Los conceptos muy relacionados deben estar cerca verticalmente [G10], para que el lector no tenga que saltar por el archivo (PDF p. 111). Esta es una de las razones para evitar variables `protected`.

- **Declaración de variables**: las variables se declaran lo más cerca posible de su uso. Como las funciones son cortas, las locales van al inicio de cada función. Las variables de control de bucles se declaran dentro de la sentencia del bucle (PDF p. 111-112).
- **Variables de instancia**: van al inicio de la clase. En C++ se usaba la "scissors rule" (al final); la convención Java es ponerlas arriba. Lo importante es que estén en un lugar conocido. El caso de `TestSuite` de JUnit 4.3.1 ilustra el error de esconderlas a mitad de la clase (PDF p. 112-113).
- **Funciones dependientes**: si una función llama a otra, deben estar cerca y la que llama debe estar por encima de la llamada, dando un flujo natural (Listing 5-5, `WikiPageResponder.java`). El ejemplo también muestra mantener las constantes en el nivel apropiado [G35]: `"FrontPage"` se pasa desde donde tiene sentido conocerla hasta donde se usa (PDF p. 113-114).
- **Afinidad conceptual**: ciertos fragmentos quieren estar cerca por afinidad. En la clase `Assert` de Junit 4.3.1, las variantes de `assertTrue`/`assertFalse` comparten esquema de nombres y realizan la misma tarea básica; aunque no se llamaran entre sí, querrían estar juntas (PDF p. 115).

## Vertical Ordering (Orden vertical)

Las dependencias de llamada deben apuntar hacia abajo: la función llamada debe quedar por debajo de la que llama. Como en los periódicos, los conceptos más importantes van primero y con el mínimo de detalle contaminante; los detalles de bajo nivel, al final. Esto permite hojear el archivo y captar la idea sin sumergirse en el detalle (PDF p. 115-116). Es lo opuesto a Pascal, C y C++, que exigen definir o declarar antes de usar.

## Horizontal Formatting (Formato horizontal)

Analizando los mismos siete proyectos, los programadores prefieren líneas cortas (PDF p. 116). El antiguo límite Hollerith de 80 es algo arbitrario; el autor no se opone a 100 o 120, pero más allá es descuido. Fija su límite personal en 120.

- **Apertura y densidad horizontal**: el espacio en blanco asocia lo fuertemente relacionado y disocia lo débilmente relacionado. En `measureLine`, se rodean los operadores de asignación con espacios para destacar lado izquierdo y derecho; no se separa el nombre de función del paréntesis de apertura porque función y argumentos están estrechamente ligados. También sirve para acentuar la precedencia de operadores (`Quadratic`): los factores sin espacio por alta precedencia, los términos separados por ser suma/resta. Los reformateadores suelen ser ciegos a la precedencia y pierden estos matices (PDF p. 117).
- **Alineación horizontal**: el autor solía alinear nombres de variables y rvalues (ejemplo `FitNesseExpediter`), pero concluyó que no es útil: enfatiza lo incorrecto y las herramientas lo eliminan. Prefiere declaraciones y asignaciones sin alinear, porque una lista demasiado larga señala un problema real (la longitud sugiere dividir la clase), no la falta de alineación (PDF p. 118).

## Indentation (Indentación)

Un archivo fuente es una jerarquía como un esquema: información del archivo, de las clases, de los métodos, de los bloques y, recursivamente, de los bloques dentro de bloques. Para hacer visible esa jerarquía de ámbitos, se indenta en proporción a la posición en la jerarquía. La comparación de `FitNesseServer` sin indentar y correctamente indentado muestra que sin indentación los programas son prácticamente ilegibles (PDF p. 119-120).

- **Romper la indentación**: a veces se tienta colapsar `if`, `while` o funciones cortas en una línea (`CommentWidget`). El autor casi siempre acaba restaurando la indentación; prefiere expandir e indentar los ámbitos (PDF p. 120).
- **Ámbitos tontos (dummy scopes)**: cuerpos vacíos de `while`/`for` deben evitarse; cuando no se puede, hay que indentar el punto y coma en su propia línea y hacerlo visible para no ser engañado por él (PDF p. 121).

## Team Rules / Uncle Bob's Formatting Rules (Reglas del equipo / Reglas de Tío Bob)

Cada programador tiene sus reglas favoritas, pero en un equipo mandan las reglas del equipo. Todos deben adoptar un único estilo para que el software no parezca escrito por individuos en desacuerdo (PDF p. 121). En FitNesse (2002), el equipo acordó en unos 10 minutos dónde poner las llaves, el tamaño de indentación y cómo nombrar clases, variables y métodos, y codificó esas reglas en el formateador del IDE. El autor ilustra sus reglas personales con `CodeAnalyzer.java` (Listing 5-6), con la idea de que el mejor documento de estándar de codificación es el propio código (PDF p. 121-122).

## Ideas clave

- El formato es comunicación; la legibilidad sobrevive al código original y afecta a todos los cambios futuros.
- Archivos pequeños (≈200 líneas, tope 500) son más fáciles de entender; un archivo debe leerse como un artículo de periódico, de lo general a lo detallado.
- Líneas en blanco separan conceptos; la densidad vertical agrupa lo que está estrechamente relacionado.
- Mantén lo relacionado cerca: variables cerca de su uso, variables de instancia arriba, la función que llama por encima de la llamada, y agrupa por afinidad conceptual.
- Las dependencias de llamada apuntan hacia abajo, del alto nivel al bajo nivel.
- Prefiere líneas cortas (límite personal 120); usa el espacio horizontal para asociar/disociar y para acentuar la precedencia de operadores.
- Evita alinear declaraciones y asignaciones: una lista larga señala que hay que dividir la clase.
- La indentación hace visible la jerarquía de ámbitos; no la rompas ni siquiera en construcciones cortas.
- En equipo, el estilo lo decide el equipo y se automatiza en el IDE; el código es el mejor documento de estándar.
