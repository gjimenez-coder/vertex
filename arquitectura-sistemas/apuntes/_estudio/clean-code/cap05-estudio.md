# Capítulo 5 — Formatting (Formato) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre el formato del código?
R: El formato es ante todo comunicación, la primera prioridad del desarrollador profesional; la legibilidad sobrevive al código original y afecta a todos los cambios futuros.

P: ¿Qué tamaño de archivo resulta deseable según el análisis de los siete proyectos?
R: Archivos típicamente de ~200 líneas con un tope de 500; es posible construir sistemas grandes (FitNesse ronda 50.000 líneas) con archivos pequeños.

P: ¿Qué dice la metáfora del periódico?
R: Un archivo fuente debe leerse como un artículo de prensa: el nombre es el titular, arriba van los conceptos de alto nivel y el detalle aumenta a medida que se desciende, con las funciones de más bajo nivel al final.

P: ¿Para qué sirve la apertura vertical entre conceptos?
R: Cada grupo de líneas es un pensamiento completo y las líneas en blanco lo separan de los demás; sin ellas el código se vuelve un amasijo.

P: ¿Qué significa la densidad vertical?
R: Que las líneas muy relacionadas aparezcan juntas para mostrar asociación estrecha; comentarios inútiles que separan variables de instancia rompen esa asociación.

P: ¿Dónde deben declararse las variables locales y las de control de bucles?
R: Las locales lo más cerca posible de su uso, al inicio de cada función corta; las de control de bucles dentro de la sentencia del bucle.

P: ¿Dónde se colocan las variables de instancia en Java y por qué?
R: Al inicio de la clase; lo importante es que estén en un lugar conocido y no escondidas a mitad de la clase (error ilustrado por TestSuite de JUnit 4.3.1).

P: ¿Cómo deben ordenarse las funciones dependientes?
R: Cerca unas de otras, con la función que llama por encima de la llamada, dando un flujo natural de lectura de arriba hacia abajo.

P: ¿Qué es la afinidad conceptual?
R: La tendencia de ciertos fragmentos a estar cerca por compartir esquema de nombres o tarea básica, como las variantes de assertTrue/assertFalse en la clase Assert, aunque no se llamen entre sí.

P: ¿Hacia dónde deben apuntar las dependencias de llamada en el orden vertical?
R: Hacia abajo: la función llamada queda por debajo de la que llama, con los conceptos importantes primero y los detalles de bajo nivel al final.

P: ¿Cuál es el límite de ancho de línea que fija el autor?
R: Prefiere líneas cortas; su límite personal es 120, no se opone a 100 o 120, pero más allá lo considera descuido (el límite Hollerith de 80 es arbitrario).

P: ¿Cómo se usa el espacio en blanco horizontal?
R: Para asociar lo fuertemente relacionado y disociar lo débilmente relacionado; se rodean operadores de asignación con espacios, no se separa el nombre de función del paréntesis, y se acentúa la precedencia de operadores.

P: ¿Por qué el autor rechaza alinear declaraciones y asignaciones?
R: Porque enfatiza lo incorrecto y las herramientas lo eliminan; una lista demasiado larga señala un problema real (dividir la clase), no la falta de alineación.

P: ¿Para qué sirve la indentación?
R: Hace visible la jerarquía de ámbitos (archivo, clases, métodos, bloques); sin ella los programas son prácticamente ilegibles.

P: En un equipo, ¿quién decide las reglas de formato?
R: El equipo, no el individuo; todos adoptan un único estilo codificado en el formateador del IDE, y el mejor documento de estándar es el propio código.

## Preguntas de autoevaluación

P: ¿Por qué el formato importa más que la funcionalidad presente? (Lo que necesitas saber)
R: Porque la funcionalidad de hoy cambiará, pero la legibilidad afecta a todos los cambios futuros; el estilo y la disciplina sobreviven aunque el código original desaparezca.

P: Explica la diferencia entre apertura vertical y densidad vertical. (Vertical Formatting)
R: La apertura separa conceptos distintos con líneas en blanco, mientras que la densidad acerca líneas estrechamente relacionadas para mostrar su asociación.

P: ¿Qué problema concreto evita mantener los conceptos relacionados cerca verticalmente? (Vertical Distance)
R: Evita que el lector tenga que saltar por el archivo; es además una de las razones para evitar variables protected.

P: En el orden vertical, ¿qué analogía con el periódico se aplica y qué permite? (Vertical Ordering)
R: Los conceptos más importantes van primero con el mínimo de detalle y los de bajo nivel al final, lo que permite hojear el archivo y captar la idea sin sumergirse en el detalle.

P: ¿Cómo se usa el espacio horizontal para reflejar la precedencia de operadores? (Horizontal Formatting)
R: En Quadratic, los factores de alta precedencia van sin espacio y los términos de suma/resta se separan con espacios; los reformateadores suelen ser ciegos a estos matices.

P: ¿Qué hacer con los ámbitos tontos (dummy scopes) y por qué? (Indentation)
R: Evitar cuerpos vacíos de while/for; cuando no se puede, indentar el punto y coma en su propia línea y hacerlo visible para no ser engañado por él.

P: ¿Cómo acordó el equipo de FitNesse sus reglas de formato? (Team Rules)
R: En unos 10 minutos acordaron dónde poner las llaves, el tamaño de indentación y cómo nombrar clases, variables y métodos, y codificaron esas reglas en el formateador del IDE.

## Checklist

- Mantén los archivos pequeños (objetivo ~200 líneas, tope 500).
- Ordena el archivo de lo general a lo detallado, como un artículo de periódico.
- Separa conceptos distintos con líneas en blanco y agrupa lo relacionado con densidad vertical.
- Declara las variables locales cerca de su uso y las de instancia al inicio de la clase.
- Coloca la función que llama por encima de la llamada y agrupa funciones por afinidad conceptual.
- Haz que las dependencias de llamada apunten hacia abajo, del alto nivel al bajo nivel.
- Mantén las líneas cortas (límite 120) y usa el espacio horizontal para asociar/disociar y marcar precedencia.
- No alinees declaraciones ni asignaciones; si la lista es larga, divide la clase.
- Indenta siempre para mostrar la jerarquía de ámbitos, sin romperla en construcciones cortas.
- Adopta un único estilo de equipo y automatízalo en el formateador del IDE.
