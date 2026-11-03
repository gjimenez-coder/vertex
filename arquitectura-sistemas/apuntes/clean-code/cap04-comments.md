# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 4 — Comments (Comentarios)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo defiende una tesis incómoda: los comentarios son, en el mejor de los casos, un mal necesario. Su uso adecuado es compensar nuestra incapacidad de expresarnos en el código. El autor insiste en la palabra "fracaso": cada vez que escribes un comentario deberías sentir el fracaso de tu capacidad de expresión, porque si el lenguaje fuera suficientemente expresivo —o tuviéramos el talento para usarlo— casi no necesitaríamos comentarios.

La razón de fondo para desconﬁar de los comentarios es que mienten. No siempre ni intencionadamente, pero sí con demasiada frecuencia. El código cambia y evoluciona, los fragmentos se mueven, pero los comentarios no siempre pueden seguirlos y quedan huérfanos, con una exactitud cada vez menor. Los programadores no pueden mantenerlos de forma realista. Un comentario inexacto es mucho peor que ningún comentario: engaña y desinforma. La única verdad está en el código, única fuente de información realmente precisa.

Sales sabiendo distinguir los pocos comentarios buenos (legales, informativos, de intención, aclaración, advertencia de consecuencias, TODO, amplificación, Javadoc en APIs públicas) de la mayoría, que son malos (balbuceos, redundantes, engañosos, obligatorios, de diario, de ruido, código comentado, etc.). La consigna general: antes de escribir un comentario, intenta expresar la intención en el código; el único comentario verdaderamente bueno es el que encontraste la manera de no escribir.

## El ejemplo que recorre el capítulo

El hilo conductor final es `GeneratePrimes.java` (Listing 4-7), un módulo que el autor escribió para la primera XP Immersion como ejemplo de mal estilo de comentarios, y que Kent Beck refactorizó en vivo a `PrimeGenerator.java` (Listing 4-8). La versión original estaba, en su día, considerada "bien documentada"; hoy se ve como un pequeño desastre. La refactorización reduce todo a solo dos comentarios explicativos: el primero introduce el algoritmo de la Criba de Eratóstenes (posiblemente redundante, pero facilita la lectura) y el segundo justifica por qué el límite de iteración es la raíz cuadrada del tamaño del arreglo —algo que no pudo expresar con un nombre de variable ni otra estructura—. El autor incluso duda de si esa optimización merece el esfuerzo de comprensión que exige a los demás.

## Comentarios buenos

Son necesarios o beneficiosos, pero siempre recordando que el mejor es el que no se escribe.

- **Legales**: encabezados de copyright y autoría al inicio del archivo. No deben ser contratos; cuando se pueda, referir a una licencia estándar externa.
- **Informativos**: aportan información básica (p. ej., el formato que casa una expresión regular). Mejor si se puede trasladar la información al nombre de la función o a una clase especializada.
- **Explicación de intención**: documentan la razón detrás de una decisión; aunque no estés de acuerdo con la solución, al menos entiendes qué pretendía el autor (ej. `return 1; // we are greater because we are the right type.`).
- **Aclaración**: traducen un argumento o valor de retorno oscuro a algo legible, útil sobre todo en código de librería estándar que no puedes alterar. Riesgo alto de que la aclaración sea incorrecta: cuida que sea exacta.
- **Advertencia de consecuencias**: avisan a otros programadores (ej. un test lento, o que `SimpleDateFormat` no es thread-safe, por lo que hay que crear cada instancia aparte).
- **TODO**: notas de trabajo pendiente con su justificación. No son excusa para dejar código malo. Los buenos IDE los localizan; aun así, revísalos y elimínalos periódicamente.
- **Amplificación**: resaltan la importancia de algo que podría parecer intrascendente (ej. por qué un `trim` es realmente importante).
- **Javadocs en APIs públicas**: muy útiles al describir una API pública, pero sujetos a todo el resto de advertencias del capítulo.

## Comentarios malos

La mayoría de los comentarios caen aquí: muletas o excusas para código pobre.

- **Balbuceo (Mumbling)**: comentarios puestos por obligación o prisa que no comunican; si obligan a mirar otro módulo para entenderlos, han fallado.
- **Redundantes**: dicen lo mismo que el código y tardan más en leerse (ej. el `waitForClose` o los Javadocs de `ContainerBase.java` de Tomcat).
- **Engañosos (Misleading)**: imprecisos de forma sutil; el `waitForClose` no retorna cuando `this.closed` se vuelve `true`, sino que espera un timeout ciego y lanza excepción.
- **Obligatorios (Mandated)**: la regla de que toda función o variable lleve comentario solo genera ruido y mentiras (ej. Javadoc de `addCD`).
- **De diario (Journal)**: registros de cambios al inicio del módulo; hoy el control de versiones lo hace por nosotros, deben eliminarse.
- **De ruido (Noise)**: reafirman lo obvio ("Default constructor.", "The day of the month."); se aprenden a ignorar y acaban mintiendo.
- **Ruido alarmante (Scary Noise)**: Javadocs redundantes que hasta arrastran errores de copiar-pegar.
- **Usar función o variable en vez de comentario**: a menudo se reescribe el código con variables explicativas y el comentario sobra.
- **Marcadores de posición**: banderas tipo `// Actions /////`; úsalas muy rara vez o se vuelven ruido de fondo.
- **Comentarios en llaves de cierre**: señal de que la función es demasiado larga; mejor acortarla.
- **Atribuciones y firmas** (`/* Added by Rick */`): el control de versiones lo hace mejor.
- **Código comentado**: no lo hagas; nadie se atreve a borrarlo y se acumula como posos. Bórralo, el control de versiones lo recuerda.
- **Comentarios HTML**: una abominación en el código fuente; si una herramienta los extrae, que sea esa herramienta la que ponga el HTML.
- **Información no local**: un comentario debe describir el código cercano, no partes lejanas del sistema (ej. el puerto por defecto que la función no controla).
- **Demasiada información**: nada de disquisiciones históricas o detalles irrelevantes (ej. el texto largo del RFC 2045 sobre base64).
- **Conexión no obvia (Inobvious Connection)**: la relación entre comentario y código debe ser evidente; es una lástima cuando el comentario necesita su propia explicación.
- **Encabezados de función**: las funciones cortas con buen nombre no los necesitan.
- **Javadocs en código no público**: son anatema; la formalidad extra solo distrae.

## Ideas clave

- Los comentarios son un mal necesario; su uso compensa el fracaso de expresarse en el código. (PDF p. 85)
- Los comentarios mienten porque los programadores no pueden mantenerlos al ritmo del código; la verdad solo está en el código.
- Un comentario inexacto es peor que ninguno: engaña y crea expectativas que no se cumplen.
- No comentes código malo: límpialo. Expresa la intención en código (ej. `employee.isEligibleForFullBenefits()`).
- Comentarios buenos legítimos: legales, informativos, de intención, aclaración, advertencia, TODO, amplificación y Javadoc de APIs públicas.
- La mayoría de los comentarios son ruido, redundancia o excusas; el código comentado y los diarios deben borrarse (para eso está el control de versiones).
- Antes de escribir un comentario, busca una función o variable que lo haga innecesario; el mejor comentario es el que no escribiste.
- En la refactorización de `PrimeGenerator`, de un módulo saturado se pasa a solo dos comentarios explicativos.
