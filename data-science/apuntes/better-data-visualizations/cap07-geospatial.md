# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 7 — Geospatial (Datos geoespaciales)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; es un capítulo muy visual, por lo que algunos gráficos se describen con palabras. Las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Los mapas tienen una ventaja evidente: la gente puede encontrarse a sí misma en los datos, una conexión que otras visualizaciones no logran. Añadir datos a un mapa puede significar colorear áreas geográficas (estados, países) o superponer círculos, cuadrados, líneas u otras formas. Los mapas basados en datos no son nuevos: Schwabish recuerda la visualización "Maps and Sales Visualization" de E. P. Hermann (1922), que ya mostraba treinta y seis formas de colocar datos sobre un mapa.

La tesis central del capítulo es de cautela: muchos mapas se hacen solo porque el creador tiene datos geográficos, no porque el mapa sea el mejor medio. Antes de mapear hay que preguntarse si el mapa muestra de verdad las relaciones que queremos explorar o si solo enseña dónde vive la gente. El gran problema es que el tamaño de un área geográfica puede no corresponder a la importancia del valor de los datos (Rusia y Alaska ocupan mucho; Luxemburgo o Massachusetts, muy poco pese a cifras altas).

Qué sales sabiendo: los retos perceptivos de los mapas; qué es un choropleth y cómo elegir proyección, bins (intervalos) y etiquetas; alternativas que corrigen la distorsión geográfica (cartogramas de varios tipos, tile grid maps); y otros tipos como proportional symbol, dot density y flow maps. La decisión de qué mapa usar depende de dos preguntas: ¿qué importancia tienen los patrones geográficos? y ¿qué importancia tiene que el lector vea un mapa familiar?

## Los retos de los mapas

El ejemplo de apertura es *Flight Patterns* de Aaron Koblin, que traza todas las rutas aéreas sobre Estados Unidos en veinticuatro horas; no clasifica aeropuertos ni evita retrasos, pero muestra de un vistazo los patrones de tráfico del cielo.

El reto mayor es que el tamaño geográfico no se corresponde con el valor del dato. Rusia (más de 6,6 millones de millas cuadradas) ocupa muchísimo espacio; Texas (270.000) es menos de la mitad de Alaska (665.000), que además suele dibujarse distorsionada y arbitrariamente colocada al sur de California. El mapa puede, así, distorsionar nuestra percepción de los valores importantes.

Schwabish recomienda acercarse al deseo de hacer un mapa con más escepticismo y pensamiento crítico. No se trata de no hacer mapas nunca —a menudo los necesitamos para entender los datos—, sino de dar un paso atrás y considerar si es la elección correcta. El mensaje es simple: hay muchas maneras de presentar datos geográficos y muchos objetos, formas y colores que añadir.

## Choropleth map (mapa coroplético)

El mapa de datos más familiar tiene quizá el nombre más desconocido: el *choropleth*. Usa colores, tonos o patrones sobre unidades geográficas para mostrar cantidades y magnitudes proporcionales. El ejemplo es un mapa de PIB per cápita mundial en 2017: forma reconocible, fácil de leer, con una paleta en la que los valores pequeños van en colores claros y los grandes en oscuros (un "color ramp").

Un error frecuente es usar una paleta divergente (colores que progresan hacia afuera desde un punto medio) cuando no comparamos por encima y por debajo de un punto medio como el promedio; en ese caso la paleta divergente es mala elección. La distorsión geográfica persiste: Luxemburgo tuvo el PIB per cápita más alto en 2017 (más de 104.000 dólares; EE. UU., 59.500) pero es casi invisible por su tamaño. Hay alternativas que corrigen esa distorsión (cartogramas, tile grid maps, heat maps), con el coste de que el mapa deja de ser familiar. Como señaló Kenneth Field (*Cartography*), ninguno de estos mapas es correcto o incorrecto: "They are all just a different representation of the truth" (PDF p. 236).

## Elegir la proyección

El mundo es un globo y los mapas son planos, así que el cartógrafo debe elegir una proyección que transforme la esfera en un plano; toda proyección distorsiona en algún grado. La más familiar es la Mercator (Gerardus Mercator, 1569), estándar náutico y opción por defecto en herramientas como Tableau y PowerBI. Permite trazar una línea recta (rhumb line) entre dos puntos para hallar el rumbo, pero distorsiona el tamaño a medida que aumenta la latitud: Groenlandia parece del tamaño de Sudamérica cuando es un octavo. La Robinson, en cambio, acerca las áreas a su tamaño real.

Tres categorías principales de proyecciones:

- **Cónica**: como un cono colocado sobre la Tierra y desenrollado; buena para geografías largas este-oeste (EE. UU., Rusia) porque la distorsión es constante a lo largo de los paralelos comunes. Ejemplos: Albers Equal Area Conic y Lambert Conformal Conic.
- **Cilíndrica**: como la cónica pero con cilindros; igual que Mercator, infla las áreas lejanas del centro.
- **Planar (azimutal)**: el planeta se proyecta sobre una superficie plana; todos los puntos quedan a la misma distancia proporcional del centro, pero la distorsión crece al alejarse de él.

No hay una proyección correcta o incorrecta, pero cada una tiene tradeoffs. Muchos en el campo evitan Mercator por sus inconvenientes, aunque funciona bien en áreas pequeñas. En EE. UU., con Mercator el borde superior izquierdo es una línea recta; con Albers, el borde norte muestra una ligera curvatura.

## Elegir los bins (intervalos)

Agrupar datos en categorías discretas es, en esencia, un problema de agregación: al combinar varios estados o países en un mismo bin perdemos las diferencias internas. Con el ejemplo del ingreso familiar mediano por estado de EE. UU. en 2018 (Massachusetts 86.345 y Maryland 86.223 arriba; Nuevo México 48.283 y Misisipi 42.781 abajo), Schwabish describe cuatro métodos de binning:

- **Sin bins**: paleta continua (ramp); cada valor recibe su propio tono. Fácil, pero el gradiente puede enmascarar patrones por cambios sutiles de color (cuesta distinguir Iowa 68.718, Nebraska 67.515 y Wyoming 62.539).
- **Intervalos iguales**: se divide el rango en grupos iguales (p. ej. tramos de 10.000). Distingue mejor las unidades que la opción continua, pero con distribuciones sesgadas reparte los estados de forma desigual.
- **Distribución de datos**: bins con igual número de observaciones (cuartiles, quintiles, deciles) o según varianza/desviación estándar. Muestra bien las diferencias, pero los cortes pueden no ser significativos: Connecticut (72.812) queda en el grupo superior y Minnesota (71.817) en el siguiente, pese a cifras casi iguales.
- **Bins arbitrarios**: cortes elegidos por números redondos o rupturas naturales; evita cortes raros como el de Connecticut-Minnesota, pero puede inducir a error.

Ninguno es correcto o incorrecto; la clave es la decisión de binning. Siguiendo a Mark Monmonier (*How to Lie with Maps*, 2018), conviene considerar y mostrar la distribución real: añadir un gráfico de columnas junto al mapa hace visibles los cortes y las diferencias.

## Etiquetar los bins

Cómo etiquetamos los bins también importa. Si el bin superior es ">86.000" pero el máximo del siguiente grupo es 81.346 (New Hampshire), la etiqueta superior podría ser igualmente ">85.000" o ">81.346". La leyenda admite varias definiciones: con números redondos (que siguen siendo arbitrarios y dejan dudas sobre a qué grupo va 86.000); con los valores reales de datos (muestra con claridad las brechas, p. ej. entre 49.973 y 50.573, pero resulta demasiado detallada); o incluyendo "bins de hueco" que conectan los tramos (precisa pero recargada, oscurece los cinco bins originales). No hay solución única: hay que sopesar la precisión necesaria (decimales), el número de bins y la suavidad de los datos. Incluir en la leyenda el número de observaciones por bin —por ejemplo convirtiéndola en un pequeño gráfico de barras— ayuda a revelar la distribución.

## ¿Debería ser un mapa?

Antes de explorar otros tipos, conviene preguntarse si un mapa logra el objetivo. El ejemplo es una historia del *Washington Post* (2016) sobre la relación entre tasas de suicidio y posesión de armas en EE. UU. Recreadas como dos choropleths, cuesta ver la relación positiva: el lector salta de un mapa a otro intentando identificar estados. En cambio, un bubble plot con la tasa de suicidio en el eje vertical, la de posesión de armas en el horizontal y el tamaño de los círculos escalado a la población deja claro que los estados del cuadrante superior derecho tienden a ser del oeste y el sur. Los bubble plots son menos familiares, pero con buen título y anotación comunican mejor. (El texto incluye recursos de prevención del suicidio, como la National Suicide Prevention Lifeline en EE. UU.)

## Cartogram (cartograma)

El cartograma reescala las áreas geográficas según sus valores, corrigiendo la distorsión del choropleth; el tradeoff es que deja de parecerse al mapa conocido. Kenneth Field resume su propósito: casi siempre la geografía es inapropiada para comparar, así que en vez de cambiar los datos y mantener la geografía, se conservan los valores y se modifica la geografía. El ejemplo recurrente es el colegio electoral de EE. UU., donde los votos se asignan por población, no por tamaño: Idaho, Montana y Wyoming (325.412 millas² juntas) suman solo diez votos electorales, mientras Massachusetts (7.838 millas², menos del 2,5 % de aquellas) tiene once. Cuatro tipos principales:

- **Contiguo**: ajusta el tamaño de cada unidad al dato (votos electorales o población) manteniéndolas unidas; variantes usan cuadrados por estado o escalan condados por voto, generando un tono más púrpura. Distorsiona la forma del país.
- **No contiguo**: escala las unidades según el dato pero las separa, conservando su forma individual y dejando espacio para etiquetas y anotación. Inventado a mediados de los 1970 por Judy Olson, quien destacó que el área vacía entre unidades es significativa: con la unidad de mayor densidad como ancla, el vacío refleja la discrepancia de densidades.
- **Gráfico**: no mantiene la forma original; usa otras formas escaladas al dato. El más conocido es el mapa Dorling (Danny Dorling), con círculos dimensionados por área; su variante DeMers (o tilegram) usa cuadrados, minimizando el espacio entre unidades a costa de reconocibilidad.
- **En cuadrícula (gridded)**: formas escaladas al dato pero dispuestas para mantener la forma general de la geografía; suelen usarse cuadrados o hexágonos. El hexagon grid map ofrece flexibilidad para acercarse a la geografía real. El **tile grid map** usa un único cuadrado por unidad: ventaja, todos los estados del mismo tamaño (abstrae la distorsión) y se puede construir en Excel; desventaja, las unidades quedan fuera de su sitio (Carolina del Sur al este de Carolina del Norte, California sin tocar Arizona). Permite añadir sparklines, barras o incluso emojis a cada celda.

Hay además un **cartograma no basado en área** (o de distancia): distorsiona la geografía física para mostrar tiempo o distancia relativos. El ejemplo es el mapa del metro de Washington, DC (de Jacob Berman), con distancias casi constantes entre paradas aunque las reales varíen mucho; el objetivo es una vista compacta para planear el viaje. Sobre ese mapa familiar se puede añadir datos: convertir cada estación en un gráfico de pastel que muestre la cuota de entradas (azul) y salidas (naranja) en la hora punta matinal revela el movimiento desde las afueras hacia el centro. Siempre hay que recordar a la audiencia: estos mapas sirven a usuarios del metro de DC, no a un urbanista en Atlanta, Dallas o Berlín.

## Proportional symbol y dot density maps

El color y el tamaño no son las únicas codificaciones. Se pueden colocar sobre el mapa líneas, flechas, puntos, círculos, iconos e incluso pequeñas barras o pasteles: son los **proportional symbol maps**, con símbolos dimensionados según el dato. El ejemplo muestra el PIB per cápita en Europa (2017) con círculos y cuadrados en lugar de color. Importa usar color transparente para ver formas superpuestas; en racimos densos (Bélgica, Países Bajos) cuesta aislar unidades individuales, y de por sí es difícil leer cantidades exactas a partir de formas.

El **dot density map** (o dot distribution) usa puntos para mostrar la presencia de un valor, en relación uno-a-uno o uno-a-muchos. Son intensivos en datos pero revelan densidades y clusters difíciles de ver en un choropleth. Como requieren ubicaciones exactas (direcciones o pares latitud-longitud) rara vez disponibles, los símbolos se colocan de forma aleatoria o arbitraria dentro del área. El ejemplo usa el censo decenal de 2010: un punto por cada uno de los 308 millones de residentes en su bloque censal, con colores por grupo racial/étnico (azul blancos; verde negros; rojo asiáticos; naranja hispanos o latinos; marrón nativos y otros/mixtos). Sin fronteras ni etiquetas, se reconoce la forma del país porque la gente se agrupa en ciudades, fronteras y costas (principio Gestalt de "similitud").

## Flow map (mapa de flujos)

Los flow maps muestran movimiento entre lugares: flechas y líneas indican la dirección y el ancho puede codificar el valor. También pueden codificar datos cualitativos (sin escalar el ancho). Los **radiales** (origen-destino) muestran flujos de una fuente a muchos destinos; los **distributivos** son similares pero el flujo se bifurca en muchas líneas. El ejemplo distributivo es el mapa de la revista de Delta Airlines: parece caótico, pero cumple su objetivo de demostrar la "unrivaled coverage".

El flow map más famoso es el de Charles-Joseph Minard (1869) sobre la campaña de Napoleón en Rusia (1812-1813), junto al de la marcha de Aníbal en 218 a. C. El mapa de Napoleón muestra las pérdidas progresivas de hombres: 420.000 invaden Rusia en junio de 1812; solo 100.000 llegan a Moscú cuatro meses después; tras la retirada bajo frío extremo (hasta −30 °C), quedan 10.000 al salir de Rusia. Integra seis valores en una sola vista: número de tropas (grosor de línea), distancia (escala abajo a la derecha), temperatura (gráfico de líneas inferior), tiempo (también en ese gráfico), dirección (color: marrón hacia el este, negro en retirada) y geografía (ciudades, ríos, batallas). Sandra Rendgen (*The Minard System*) destaca que Minard enfocó todo en una sola variable —el número de personas en el flujo—, cuyo declive agudo y constante transmite el mensaje sobre el cataclismo de la guerra.

## Conclusión

El capítulo repasa promesas y peligros de visualizar datos geográficos. A veces el tamaño variable de las unidades distorsiona los datos; otras, escalar la geografía al dato vuelve extraña una geografía familiar. Ante datos geográficos, el instinto es hacer un mapa, pero conviene preguntarse si es la mejor forma, si el lector necesita ver diferencias exactas (donde el problema de agregación estorba) y si hay patrones geográficos claros. Si el mapa es lo adecuado, hay que elegir con cuidado la proyección y plantearse si el choropleth estándar es lo mejor o si un cartograma —con todos sus defectos— encaja mejor. A menudo lo óptimo es combinar tipos: un mapa con una tabla o un gráfico de barras, para dar al lector una vista familiar donde ubicarse y, a la vez, un detalle más preciso de los datos.

## Ideas clave

- La gran ventaja del mapa es que el lector se encuentra a sí mismo; el gran riesgo es que el tamaño geográfico no se corresponde con la importancia del dato.
- Antes de mapear, pregúntate si el mapa comunica tu argumento o solo muestra dónde vive la gente; a veces un scatter o bubble plot funciona mejor.
- El choropleth es el mapa más familiar; usa paletas secuenciales (claro a oscuro), no divergentes salvo que compares respecto a un punto medio.
- Toda proyección distorsiona: Mercator infla las latitudes altas; conic, cylindrical y planar (azimutal) ofrecen tradeoffs distintos.
- El binning (sin bins, intervalos iguales, distribución de datos, arbitrario) y el etiquetado condicionan la percepción; mostrar la distribución real ayuda.
- Los cartogramas (contiguo, no contiguo, gráfico, en cuadrícula) corrigen la distorsión escalando la geografía al dato, a costa de familiaridad; el tile grid map iguala tamaños y admite mini-gráficos.
- Proportional symbol y dot density maps codifican con formas y puntos; los dot density revelan clusters mediante el principio de similitud.
- Los flow maps muestran movimiento; el mapa de Napoleón de Minard integra seis variables y concentra el mensaje en el declive del número de tropas.
