# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 12 — Developing a Data Visualization Style Guide (Desarrollar una guía de estilo de visualización de datos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Una guía de estilo de visualización de datos hace por los gráficos lo que el *Chicago Manual of Style* hace por la gramática inglesa: define las partes de un gráfico y su uso correcto y consistente. Elementos como la fuente, el color, el grosor de las líneas, las gridlines o los tick marks determinan si un gráfico es claro, atractivo y consistente. A diferencia de la gramática, muchas de estas decisiones son subjetivas: no existe un grosor de línea objetivamente correcto, aunque sí principios a considerar. En gran medida, los estilos elegidos reflejan las preferencias tuyas y de tu organización.

En una organización, la guía cumple tres propósitos: da a los miembros del equipo estilos y expectativas detalladas sobre qué incluir y qué no; guía a quienes no conocen (o no les importan) las reglas de marca, automatizando decisiones al integrarlas en las herramientas; y fija el tono de que la visualización de datos es tan importante como el resto de materiales de marca. Incluso para alguien que trabaja solo, una guía propia hace el trabajo más consistente y eficiente y construye una marca personal.

Sales sabiendo qué secciones debe cubrir una guía y cómo abordarlas: anatomía del gráfico, paletas de color, fuentes, guías por tipo de gráfico, exportación de imágenes y accesibilidad. La guía debe tratarse como un documento vivo que evoluciona con la estética, los tipos de publicación y las herramientas. Conviene probar sus componentes: colores que lucen en un logo pueden no funcionar en un gráfico de líneas o de barras.

## El ejemplo que recorre el capítulo
El hilo conductor es la guía de estilo del Urban Institute (institución de investigación sin ánimo de lucro de Washington, DC), usada como plantilla para definir cada parte de un gráfico. El capítulo se apoya además en guías publicadas por otras organizaciones (Economist, Financial Times, London Datastore, Sunlight Foundation, National Cancer Institute, CFPB, BBC, USDA) como ejemplos de cómo definir estilos.

## Los elementos de una guía
Las secciones básicas que toda guía debería cubrir son seis: (1) **Graph Anatomy** (dónde se colocan etiquetas, títulos y elementos, y el tamaño del gráfico según el tipo de salida); (2) **Color Palette** (qué colores usar según el tipo de gráfico o dato, y si varían entre impreso y digital); (3) **Font** (qué fuente usar y cómo varían tamaño, grosor y posición; quizá una para el título y otra para el cuerpo); (4) **Graph Types** (consideraciones especiales, p. ej. si se prohíben los pie charts o cuántas series admite un gráfico de líneas); (5) **Exporting Images** (formato de imagen y cómo generarlo); y (6) **Accessibility, Diversity, and Inclusion** (hacer los gráficos accesibles y presentar los resultados de distintos grupos con cuidado). Los Marimekko del Economist y el Financial Times ilustran cómo una marca distintiva vuelve un gráfico reconocible al instante.

## La anatomía de un gráfico
Para fijar estilos primero hay que definir cada parte del gráfico. Con la plantilla del Urban Institute, Schwabish enumera catorce elementos:

1. **Overall Dimensions**: tamaño total, que varía por tipo de producto (online en píxeles, impreso en pulgadas/centímetros). Urban fija 6,5 pulgadas de ancho para encajar en página de 8,5 × 11.
2. **Figure Number**: numerar, usar letras o nada; puede ir sobre el título o en línea ("Figure 1. Chart Title."). Urban lo pone encima, en mayúsculas, fuente Lato Regular 9 pt, color azul (RGB 22 150 210).
3. **Title**: alineado a la izquierda (crea una rejilla vertical más ordenada) o centrado; descriptivo o activo; sentence case o title case. Urban usa title case, corto y máximo dos líneas.
4. **Subtitle**: lugar para una afirmación activa o para las unidades; buen sitio para el título del eje vertical al quedar cerca del eje. Urban lo escribe en sentence case, menor tamaño y color negro.
5. **Axis Titles**: mejor que el título del eje vertical vaya horizontal y sobre el eje (puede ser el subtítulo); el del eje horizontal a veces se omite (meses, años). Urban pone unidades entre paréntesis y la etiqueta del eje horizontal en Lato Italic 8,5 pt, centrada.
6. **Axis Labels**: formato (negrita, cursiva, tamaño); las verticales suelen ir a la izquierda; decidir formato de unidades (p. ej. años escritos completos o abreviados).
7. **Axis Lines and Tick Marks**: color y grosor; tick marks dentro o fuera. A veces se omite la línea del eje vertical pero se conserva la horizontal como ancla. El autor prefiere oscurecer la línea del cero, sobre todo con valores negativos. Urban: sin línea vertical, línea horizontal negra de 1 pt con tick marks mayores hacia fuera.
8. **Gridlines**: sólidas, discontinuas o punteadas; grosor, color e incrementos. Pocas incluyen gridlines verticales (salvo algún scatterplot).
9. **Sources and Notes**: documentar fuentes y notas de modelado; caja abajo, alineada a la izquierda. El *Chicago Manual of Style* (sección 3.20) sugiere la fuente sobre la nota; Urban pone "Source" y "Notes" en negrita y en ese orden.
10. **Logo**: dónde y de qué tamaño (alta resolución); habitual en la esquina inferior derecha, lejos de título y notas.
11. **Legend**: si se usa, dónde, tamaño y marcadores.
12. **Data Markers**: círculos o cuadrados, rellenos o huecos; cuándo etiquetar valores.
13. **Data Labels**: cuándo etiquetar puntos y cómo colocarlos y formatearlos.
14. **Data Series**: varía por tipo de gráfico (grosor de líneas, espacio entre barras, colores de cada elemento).

Como otros ejemplos de definición de partes, cita las guías del London Datastore (ciudad de Londres, datos abiertos) y de la Sunlight Foundation (gobierno abierto).

## Paletas de color
El color tiene un poder innegable: suele ser lo primero que se nota, evoca emociones y atrae la atención. Una paleta que sirve para el membrete o la web puede no funcionar en un gráfico de líneas con cinco series. Hay herramientas gratuitas para crear paletas (Adobe Color, Color Brewer, Colour Lovers, Design Seeds) y conviene definir tintes y sombras de cada color. Cuanto más fácil sea aplicar la marca, más tiempo tiene el analista para trabajar los datos.

Existen cinco esquemas de color principales: **Binary** (dos categorías nominales: urbano-rural, demócrata-republicano); **Sequential** (valores de bajo a alto, claros a oscuros; mapas coropléticos de pobreza o población); **Diverging** (progresan hacia fuera desde un punto medio más claro, combinando dos esquemas secuenciales; desviaciones respecto a cero); **Categorical** (colores separados para diferencias nominales, como grupos de raza o género); y **Highlighting** (caso especial del categórico que resalta un valor o grupo, p. ej. unos puntos en un scatterplot). Añade la **Transparency**, más que un esquema una técnica: usar colores transparentes deja ver el objeto que hay detrás y hace visibles los solapamientos.

Como ejemplos de definición cita las guías del National Cancer Institute (paletas primaria y secundaria con tintes y sombras) y del CFPB. Hay que tener presente a quienes padecen deficiencia de visión del color (CVD): unos 300 millones de personas en el mundo, en su mayoría hombres, con dificultad sobre todo entre rojos y verdes; herramientas como Vischeck.com o WebAIM permiten comprobar colores.

**Avoid the rainbow**: el arcoíris es mala elección por tres razones. No es lógico decir que "morado" es más que "naranja"; no se corresponde con nuestro sistema numérico (la franja verde es ancha y la azul clara estrecha, de modo que un mismo cambio de unidad se percibe distinto según la zona); y no es consistente para personas con CVD ni al imprimir en blanco y negro.

**Colors and culture**: el color puede reforzar estereotipos o significar cosas distintas según la cultura. El par rosa-azul arrastra un bagaje de género (rosa=debilidad, azul=fuerza), aunque antes de mediados del siglo XX era al revés; St. Clair recuerda en *The Secret Lives of Color* que el rosa era "solo rojo desvaído", el color más masculino. Mejor usar morados y verdes (Telegraph) o azules y naranjas (Guardian). Además, el rojo evoca pasión en Occidente, felicidad y celebración en Oriente, pureza en India y vida/ira/peligro en Japón.

## Definir las fuentes
La guía debe definir tipografías para cada parte del gráfico. Rara vez hacen falta más de dos fuentes, y a menudo basta una; se puede variar su aspecto cambiando grosor (fina, negrita), ángulo (cursiva) y color. Cuidado con las fuentes personalizadas: diferencian el estilo pero deben estar instaladas en toda máquina que muestre el gráfico, lo que da problemas al compartir archivos o presentar desde otro portátil. Fuentes por defecto como Century Gothic, Tahoma, Trebuchet MS y Verdana son eficaces, están en casi todos los sistemas y, al usarse poco, resultan novedosas. La guía de la BBC para Tableau usa su fuente Reith Sans (no estándar, debe instalarse); la del USDA incluye fuentes como Arial y Times New Roman, normalmente por defecto.

## Guías por tipo de gráfico
Conviene incluir ejemplos o instrucciones para tipos concretos, empezando por los más usados en la organización, e incorporar tipos menos comunes para ampliar el repertorio. Se pueden fijar reglas como no usar gráficos de líneas de doble eje, limitar las series de un pie chart, dónde colocar las etiquetas en una barra apilada, si los puntos de una línea van sobre o entre los tick marks, o que al mostrar data labels se omitan gridlines y tick marks. También cómo gestionar el orden de la paleta según el número de series o el tipo (barras pareadas frente a apiladas). El Urban Institute encabeza su guía con cinco consejos: mantener alta la densidad de datos (sus gráficos son de 685px de ancho), referenciar siempre la figura en el texto, mantener el título corto y simple, reservar la información técnica para Source and Notes, y extender las leyendas por la parte superior o a la derecha en orden lógico.

## Exportar imágenes
Una exportación incorrecta puede comprimir la resolución y pixelar la imagen, arruinando el trabajo. La diferencia clave entre formatos es **bitmap** (o raster), almacenado como píxeles que pierden nitidez al ampliar, frente a **vector**, que guarda la forma y es "resolution-independent" (se amplía sin perder calidad, a costa de archivos grandes). El formato adecuado depende de la herramienta, el sistema operativo y el destino (PDF, imagen web, tuit). El libro adapta de Claus O. Wilke una tabla: vectoriales **pdf** (uso general), **eps** (uso general), **svg** (online); de bitmap **png** (dibujos de líneas), **jpeg** (fotografías), **tiff** (impresión, mejor color) y **gif** (animaciones). La mejor estrategia es probar varios enfoques y revisar siempre el resultado final.

## Accesibilidad, diversidad e inclusión
Muchas personas con discapacidad visual usan lectores de pantalla: si un gráfico se llama "Image1.png", eso es lo que oirán. La accesibilidad abarca también a quienes tienen discapacidades cognitivas o conexiones lentas. Se puede seguir la Sección 508 de la Rehabilitation Act de 1973, que obliga a las agencias federales de EE. UU. a que su tecnología (ICT) sea accesible. Un estándar aplicable por todos es el **alt text**: una descripción concisa que, en un gráfico, comunique su conclusión o mensaje en una sola frase. Las WCAG definen cuatro áreas: **Perceivable** (información perceptible, contraste suficiente, alt tags), **Operable** (toda la funcionalidad accesible desde el teclado), **Understandable** (contenido legible y páginas predecibles) y **Robust** (compatible con tecnologías asistivas actuales y futuras). No hay reglas concretas para una web plenamente accesible —es un blanco móvil—, pero considerar distintas capacidades mejora la usabilidad para todos. También importa cómo se nombra a los grupos ("Black", "African American", "Hispanic"): usar el lenguaje aceptado por cada comunidad y preferir el "people-first" ("personas con discapacidad"). Lo mismo aplica al orden de barras o líneas (alfabético, por tamaño de muestra, etc.): los datos reflejan vidas de personas reales.

## Juntarlo todo
Muchas decisiones (grosor de gridlines de 1 o 2 pt, un gris u otro) no tienen respuesta correcta: son estilísticas pero también funcionales, y el objetivo es enfatizar los datos sobre gridlines, tick marks y marcadores. Una guía completa se desarrolla mejor a nivel organizativo, reuniendo a los equipos de diseño y de datos; quien trabaje solo puede acudir a expertos o a guías publicadas. Y conviene tratarla como documento vivo: revisarla según cambian tecnologías y tendencias, y ser flexible ante las necesidades, herramientas y habilidades de la organización.

## Ideas clave
- Una guía de estilo define y estandariza las partes de un gráfico; muchas decisiones son subjetivas pero se guían por principios, y debe ser un documento vivo.
- Sus seis secciones básicas: anatomía del gráfico, paleta de color, fuente, tipos de gráfico, exportación de imágenes y accesibilidad/diversidad/inclusión.
- La plantilla del Urban Institute descompone el gráfico en 14 elementos, desde dimensiones y título hasta data series.
- Cinco esquemas de color (binary, sequential, diverging, categorical, highlighting) más la transparencia; evitar el arcoíris por no mapear al sistema numérico ni funcionar con CVD o en blanco y negro.
- Basta una o dos fuentes; cuidado con las personalizadas, que deben estar instaladas en toda máquina que muestre el gráfico.
- Define reglas por tipo de gráfico y exporta con suficiente resolución, eligiendo entre formatos bitmap y vector.
- La accesibilidad (alt text, Sección 508, las cuatro áreas WCAG) y un lenguaje respetuoso y "people-first" mejoran la comunicación para todos.
