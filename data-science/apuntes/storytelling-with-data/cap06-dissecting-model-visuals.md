# Storytelling with Data — Cole Nussbaumer Knaflic (Wiley, 2015)
## Capítulo 6 — Dissecting Model Visuals (Diseccionando visuales modelo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo es un intermedio práctico entre las lecciones anteriores y la lección final (contar una historia). En lugar de introducir conceptos nuevos, la autora muestra cinco visuales "modelo" y explica el proceso de pensamiento y las decisiones de diseño que llevaron a cada uno, aplicando todo lo visto antes. La tesis es sencilla: un buen visual no es un accidente, sino el resultado de decisiones deliberadas sobre qué enfatizar y qué atenuar según cómo queremos que la audiencia procese la información.

A lo largo de los ejemplos se repiten las mismas consideraciones —color, tamaño, grosor de línea, elección del tipo de gráfico, orden relativo de los datos, alineación y posición de los elementos, y uso de las palabras—. Esa repetición es intencional: refuerza los conceptos y muestra cómo se combinan en contextos distintos.

Sales sabiendo que no existe una única respuesta "correcta" en visualización de datos: hay "sabores de bueno". Lo esencial es que cada decisión de diseño sea precisamente eso, una decisión intencional, tomada pensando en el contexto, los datos y el uso que la audiencia dará al visual.

## Model visual #1: line graph (gráfico de líneas)

Escenario: la Empresa X realiza una campaña anual de donaciones de un mes; la Figura 6.1 muestra el progreso del año en curso. Es un gráfico de líneas con la cantidad recaudada en el eje vertical ($0 a $60.000) y los días desde el lanzamiento en el horizontal. La línea "Progress to date" (progreso hasta la fecha) termina en $33.967 y se destaca; aparecen además la meta de $50.000 ($51.400 marcado) y la línea del año anterior, ambas atenuadas.

Puntos de diseño:

- Las palabras se usan bien: título del gráfico, título del eje vertical y del horizontal. Las líneas se etiquetan directamente, sin leyenda, para no obligar a ir y venir.
- Aplicando el test "¿hacia dónde van tus ojos?" (Capítulo 4), la vista va al título y luego a la tendencia "Progress to date". El título se pone en gris oscuro para que resalte sin el contraste agresivo del negro puro sobre blanco (el negro se reserva como color destacado cuando no se usa otro).
- Varios atributos preatentivos atraen la atención a la línea principal: color, grosor de línea, presencia de marcador y etiqueta en el punto final, y tamaño del texto correspondiente.
- El contexto (meta y año anterior) se incluye pero se atenúa con líneas finas y grises, y un azul más claro para el año anterior, de modo que no compita por la atención.
- Decisiones sobre los ejes: en el eje Y se conservan los ceros (redondear a miles solo compensaría con cifras en millones). En el eje X no se etiqueta cada día; con datos hasta el día 10 de un mes de 30, se etiqueta cada 5 días (otra opción sería cada 7 días o añadir supercategorías semana 1, semana 2…). No hay una única respuesta correcta: se decide según el contexto.

## Model visual #2: annotated line graph with forecast (gráfico de líneas anotado con pronóstico)

La Figura 6.2 muestra ventas anuales reales y pronosticadas. Error común: trazar pronóstico y datos reales como una única línea indistinta. Aquí se usan señales visuales para diferenciarlos: una línea sólida representa los datos reales (ACTUAL) y una línea punteada más fina —que connota menor certeza— representa el pronóstico (FORECAST). Las etiquetas en mayúsculas bajo el eje X refuerzan la distinción, y la zona de pronóstico se separa con un sombreado de fondo muy tenue.

- Casi todo se envía al fondo (fuente y elementos en gris) salvo el título, las fechas dentro de los cuadros de texto, la línea de datos, marcadores seleccionados y las etiquetas numéricas de 2014 en adelante.
- Jerarquía visual: el ojo va primero al título (arriba a la izquierda, por posición y por el texto grande en gris oscuro), luego a las fechas en azul de los cuadros de texto, donde se lee contexto, y de ahí baja al punto o tendencia correspondiente en los datos.
- Solo se incluyen marcadores en los puntos referenciados por una anotación, para localizar rápido qué parte del dato corresponde a cada texto. Los marcadores son blancos con contorno azul (más visibles); los del pronóstico son más pequeños y azul sólido, porque el contorno blanco quedaba recargado sobre la línea punteada.
- La etiqueta $108 va en negrita: es el último dato real y el ancla del pronóstico. Los puntos históricos no se etiquetan; el eje Y da la noción de magnitud, porque interesan las tendencias relativas más que los valores exactos. Los puntos de pronóstico sí se etiquetan para dar expectativas claras a futuro.
- Todo el texto es del mismo tamaño salvo donde hubo una decisión deliberada: el título es mayor; la nota al pie se atenúa con fuente pequeña y posición de baja prioridad al pie.

## Model visual #3: 100% stacked bars (barras apiladas al 100%)

Ejemplo del mundo de la consultoría (Figura 6.3): cada proyecto tiene metas que se evalúan trimestralmente como "Miss", "Meet" o "Exceed". Las barras apiladas al 100% muestran el porcentaje de proyectos en cada categoría a lo largo del tiempo.

- Alineación: título, leyenda y título del eje Y se alinean arriba a la izquierda, de modo que la audiencia aprende a leer el gráfico antes de llegar a los datos. Título, leyenda, título de eje y nota al pie forman una línea limpia a la izquierda. A la derecha, el texto está justificado a la derecha y alineado con la última barra (que contiene el dato descrito), aprovechando el principio Gestalt de proximidad.
- Atención: el rojo es el único color que atrae la mirada (se usa un tono rojo quemado porque el rojo primario resulta demasiado estridente); el resto es gris. Se añaden etiquetas numéricas —señal extra de importancia, con fuerte contraste blanco sobre rojo— en los puntos clave: el porcentaje creciente de proyectos que no cumplen sus metas. Se usan tonos de gris ligeramente distintos para poder seguir una u otra serie sin distraer del énfasis en el rojo.
- Orden: las categorías van de "Miss" a "Exceed" de abajo hacia arriba. "Miss" queda pegada al eje X, lo que facilita ver su cambio en el tiempo por el alineamiento en la misma base; "Exceed" también se sigue bien por su alineación superior. "Meet" es más difícil de comparar al no tener base constante, pero es una comparación de menor prioridad, así que es aceptable.
- Palabras: hay título de gráfico y de eje Y; el eje X usa supercategorías (los años) para reducir etiquetado redundante. El texto arriba a la derecha refuerza dónde mirar. La nota al pie aporta el número total de proyectos (de 230 a inicios de 2013 a casi 270 en Q3 2015), contexto que las barras al 100% no muestran por sí solas.

## Model visual #4: positive and negative stacked bars (barras apiladas positivas y negativas)

Ejemplo del ámbito de people analytics (Figura 6.4): proyectar la población esperada de directores e identificar brechas. Habrá una necesidad creciente de directores ("Unmet need (gap)") dadas las altas por adquisiciones y promociones y las bajas por rotación (attrition).

- Recorrido visual: la vista va del título a los números negros, grandes y en negrita, los sigue hacia la derecha hasta el texto "Unmet need (gap)", y luego baja leyendo cada serie hasta "Attrition" al pie, alternando entre ambas.
- Color: "Today's directors" en azul medio estándar; "Attrition" en una versión menos saturada del mismo azul para vincularlos. Las adiciones (promociones y adquisiciones) van en verde (connotación positiva). La "Unmet need (gap)" se dibuja solo con contorno, para mostrar espacio vacío y reforzar que es una brecha. Cada etiqueta de texto a la derecha va del color de su serie, salvo "Unmet need (gap)", en el mismo negro grande y grueso que sus etiquetas de datos.

- Orden de series: "Today's directors" es la base, arranca en el eje horizontal; "Attrition" cae por debajo en dirección negativa, reforzando que es una disminución; encima van las adiciones (promociones y adquisiciones); arriba del todo, donde el ojo llega antes, está "Unmet need (gap)".
- El eje Y se conserva (positivo y negativo) para dar magnitud total, pero atenuado en gris. Solo los puntos relevantes —la brecha— llevan etiqueta numérica directa.
- Tamaño de texto uniforme salvo decisiones puntuales: título mayor; el título de eje "# of directors" algo más grande para facilitar la lectura del texto rotado; el texto y los números de "Unmet need (gap)" más grandes y gruesos que nada más; la nota al pie pequeña, gris y en posición de mínima prioridad al pie.

## Model visual #5: horizontal stacked bars (barras apiladas horizontales)

La Figura 6.5 muestra los resultados de una encuesta sobre prioridades de desarrollo en una nación en desarrollo (Top 15). Es mucha información, pero el énfasis y la atenuación estratégicos evitan que resulte abrumadora.

- Las barras apiladas tienen sentido por la naturaleza del dato: primera prioridad (primera posición, tono más oscuro), 2ª prioridad (tono algo más claro del mismo color) y 3ª prioridad (aún más claro). La orientación horizontal permite leer los nombres de categoría a la izquierda en texto horizontal.
- Las categorías se ordenan verticalmente de mayor a menor "Total %", dando un marco claro: las mayores arriba, se ven primero. Las tres prioridades principales (Education 45%, Agriculture & rural development 37%, Poverty reduction 32%) se enfatizan con color —aplicado al nombre, al total % y a las barras— porque la narrativa original se centraba en ellas; ese color consistente une los componentes.
- Decisión sobre valores: aquí se conservan las etiquetas numéricas dentro de las barras pero atenuadas con texto pequeño, orientado a la izquierda (crea una línea limpia al escanear hacia abajo y luce menos recargado que centrado o a la derecha). Se atenúan además con un azul o gris claro que no contrasta tanto como el blanco. El eje X se elimina por completo, asumiendo que los valores son lo bastante importantes como para etiquetarlos.
- Palabras: todo titulado y etiquetado. Los títulos "PRIORITY" y "TOTAL %" en mayúsculas para escaneo fácil. La leyenda de interpretación de las barras aparece justo sobre la primera barra, con "Most", "2nd" y "3rd" en negrita. El detalle adicional (N = 4.392 y la redacción de la pregunta) va en la nota al pie.

## In closing (en cierre)

Se aprende examinando displays visuales efectivos y las decisiones que los crearon. El capítulo reforzó: elección del tipo de gráfico y orden de los datos; hacia dónde van los ojos y en qué orden gracias a enfatizar y atenuar mediante color, grosor y tamaño; alineación y posición de los elementos; y uso apropiado del texto para hacer el visual accesible mediante títulos, etiquetas y anotaciones claras. Se aprende de todo ejemplo, bueno o malo: cuando algo te gusta, detente a pensar por qué.

Con una metáfora culinaria, la autora recuerda que en visualización de datos rara vez hay una única respuesta "correcta"; hay "sabores de bueno", y estos ejemplos son la alta cocina de los gráficos. Distintas personas tomarían decisiones distintas ante el mismo reto, y eso está bien. Lo esencial es que las decisiones de diseño sean intencionales. Con esto, se queda listo para la lección final: contar una historia.

## Ideas clave

- Un buen visual resulta de decisiones deliberadas sobre qué enfatizar y qué atenuar, según cómo quieres que la audiencia procese la información.
- El color (usado con moderación como único foco), el grosor y el tamaño son atributos preatentivos que dirigen la mirada; todo lo demás se empuja al fondo en gris.
- Etiqueta las líneas y series directamente en vez de usar leyendas, y titula siempre gráfico y ejes para hacer el visual accesible.
- Distingue datos reales de pronóstico con señales visuales (línea sólida vs. punteada, sombreado) en lugar de una única línea indistinta.
- Conservar el eje da magnitud general; etiquetar solo los puntos clave enfoca la atención y evita saturar.
- El orden y la alineación de los elementos importan: alinea título, leyenda y ejes a la izquierda y aprovecha supercategorías y el principio de proximidad.
- Usa el color con significado: verde para lo positivo, contorno vacío para una brecha, dirección negativa para una disminución.
- No hay una única respuesta correcta, sino "sabores de bueno"; lo importante es que cada decisión de diseño sea intencional.
