# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 9 — Part-to-Whole (Parte respecto al todo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo agrupa los gráficos que muestran cómo las partes de una cantidad se relacionan con el total. El más popular y familiar es el gráfico de tarta (pie chart), que arrastra numerosos problemas perceptivos. Junto a él se presentan alternativas como el treemap, el sunburst, el gráfico de Nightingale y el diagrama de Voronoi, cada una con sus propias ventajas e inconvenientes. Varios de estos gráficos también sirven para visualizar datos jerárquicos, es decir, datos que se agrupan en capas donde existen grupos naturales.

La tesis central es matizada: el pie chart es la opción por defecto por su familiaridad y facilidad de lectura, pero es difícil comparar porciones de tamaño parecido, así que debe usarse con cuidado y de forma estratégica. Hay un doble mensaje recurrente en el libro: equilibrar la precisión perceptiva con lo que capta la atención y permanece en la memoria del lector.

Sales sabiendo cuándo (y cuándo no) usar un pie chart, qué reglas seguir al construirlo, y qué alternativas existen para relaciones parte-todo y jerárquicas, con sus respectivos compromisos perceptivos. Los ejemplos del capítulo siguen la guía de estilo de la publicación digital Texas Tribune, de Austin (Texas).

## El ejemplo que recorre el capítulo

El hilo conductor es la distribución de importaciones de bienes hacia Estados Unidos (valor en dólares de las mercancías que entran), desglosada en siete regiones del mundo según datos del Banco Mundial: East Asia & Pacific, North America, Europe & Central Asia, Latin America & Caribbean, Middle East & North Africa, South Asia y Sub-Saharan Africa. Estos mismos datos se representan a lo largo del capítulo como pie chart, treemap, sunburst y Nightingale para comparar los formatos.

## Pie charts (gráficos de tarta)

El desdén por los pie charts recorre todo el campo de la visualización de datos. La razón más citada: cuesta discernir cantidades exactas cuando se representan como porciones de un círculo. En el ranking perceptivo, el pie chart cae por debajo de la mitad. Aun así, es un tipo muy familiar, y la familiaridad es útil; además, el autor Manuel Lima aporta evidencia de que la afinidad humana por el círculo se remonta a milenios de evolución, y que atraen más las curvas que las formas con puntas afiladas.

Reglas para construirlos:

- Las porciones deben sumar 100 por ciento o algún total. No se pueden omitir segmentos ni incluir segmentos que sumen más de 100 por ciento.
- Ordenar las porciones de mayor a menor empezando en la posición de las 12 en punto. Excepción: si la variable tiene un orden natural (por ejemplo, grupos de edad), es mejor empezar por el grupo más joven a las 12 y seguir por categoría, no por valor.
- Si se usa más de un pie chart (algo recomendable solo en casos muy concretos), ordenar siempre las porciones igual en todos; comparar porciones en posiciones distintas es demasiado difícil.

Se puede etiquetar con porcentajes o con cantidades en dólares; cualquiera funciona, siempre que el etiquetado sea correcto y se indique en el título.

## El caso en contra y a favor de los pie charts

El problema es que el ojo humano no compara bien porciones de tamaño distinto. Con los mismos datos en un pie chart y en un bar chart, es más fácil y rápido rankear valores y ver cuánto difieren en el bar chart; en el pie chart las diferencias pequeñas son imperceptibles. Tampoco está claro cómo percibimos las cantidades: ¿el ángulo en el centro, el área de la porción o la longitud del arco? Un par de artículos de 2016 sugieren que el ángulo del vértice no es la vía principal de lectura, y que el área y la longitud de arco predicen mejor la capacidad de leer valores que el ángulo por sí solo.

Esto tiene implicaciones para el donut chart (un pie chart con el centro vacío): si no leemos por el ángulo central, el donut es una alternativa viable e incluso preferible; si leemos por el ángulo, el donut es peor porque ese ángulo está justo en el hueco que falta. No hay prueba concluyente. Su ventaja principal es que el centro deja espacio para un número o un texto.

Recomendaciones del autor: evitar parejas de pie charts, incluso con pocas porciones, porque el lector debe mirar de un gráfico a otro para detectar cambios; un stacked bar chart o un slope chart hacen esa tarea mejor (aunque el slope chart desplaza el foco hacia el cambio en el tiempo). Evitar sobre todo los pie charts con demasiadas porciones: cinco ya son demasiadas. Evitar también el "breakout" pie chart que extrae una porción y la vuelve a subdividir; mejor un bar chart o un diagrama de Sankey.

El caso a favor: un pie chart funciona mejor cuando el valor de la porción o porciones suma una cifra redonda (25, 50 o 75 por ciento), cuyo ángulo nos resulta familiar porque crea un ángulo recto en el centro. Rotar el gráfico para formar ese ángulo recto hace que el valor sea evidente de un vistazo. Es ideal para enfocar la atención en tres o cuatro porciones como mucho.

Ejemplo práctico: en una presentación sobre la recaudación de una ONG con cien donaciones, donde algo más de la mitad del dinero procede de unos pocos donativos muy grandes (de un millón de dólares o más). El público lee un pie chart casi al instante; como la parte de interés supera la mitad, es fácil trazar mentalmente la línea vertical. Se grafican y etiquetan las siete categorías, pero solo se colorean las dos porciones de interés (que juntas superan el 50 por ciento) y el resto va en gris, al fondo. Otro escenario útil: enfocar un único valor (la verdadera relación parte-todo); en esos casos conviene preguntarse si se necesita un gráfico o basta con dejar la cifra en el texto. Un mal pie chart sigue siendo un mal gráfico: úsese de forma estratégica y reflexiva.

## Treemap

Desarrollado originalmente por Ben Shneiderman en la University of Maryland, el treemap divide un cuadrado o rectángulo en secciones agrupadas para mostrar una jerarquía o una relación parte-todo. En esencia, es un pie chart "cuadrado". Como los rectángulos se comparan con más facilidad que las porciones circulares, puede resultar más legible que un pie chart, aunque al ser menos familiar también puede costar navegarlo.

Shneiderman lo creó para ver de forma compacta el directorio de archivos de su ordenador. Su mayor ventaja es la compacidad: admite muchos grupos y variables, y las jerarquías se visualizan bien porque las subsecciones se etiquetan y se incrustan dentro del grupo padre (por ejemplo, el desglose de las importaciones de EE. UU. de 2016 por región y luego por país). Permite añadir codificaciones extra: en un treemap el color marca las cuotas que aumentaron (azul) y disminuyeron (rojo) entre 1996 y 2016.

## Sunburst diagram

Si se quieren mostrar las proporciones de las partes respecto al todo en varios niveles de una jerarquía, sirve el sunburst. Como el treemap, muestra relaciones parte-todo o jerárquicas. Cada anillo corresponde a un nivel de la jerarquía y las porciones de cada anillo (a veces llamadas nodos) son los subgrupos. El anillo central muestra el nivel superior (la raíz) y los anillos exteriores, cómo los grupos se dividen en subgrupos. El color puede diferenciar anillos, grupos o jerarquías.

Como toda visualización circular, cuesta ver patrones de forma clara y rápida; un sunburst con demasiadas categorías queda recargado. El uso estratégico de color, etiquetas y anotación guía al lector hacia lo importante.

## Nightingale chart

También llamado coxcomb o rose diagram, debe su nombre a Florence Nightingale, que creó el primero y más famoso para visualizar las bajas de soldados durante la Guerra de Crimea. Convencida de que la limpieza era una causa principal de la alta mortalidad en el Barrack Hospital de Scutari (Turquía), llevó registros meticulosos; el gobierno británico creó la Sanitary Commission, que implementó mejoras de saneamiento, ventilación y limpieza.

Su gráfico se dibuja alrededor de un círculo con valores segmentados por periodos de tiempo. Cada porción representa el total de muertes de un mes, de abril de 1854 a marzo de 1856, con la causa dividida en tres categorías: heridas en combate (rosa), "otras causas" (negro) y enfermedades (azul). El área de cada porción representa su valor relativo al todo, y las porciones se ordenan en la dimensión temporal, así que muestra a la vez cambio en el tiempo y relación parte-todo. Transmite dos mensajes: las muertes en combate fueron una porción pequeña frente a las enfermedades (cólera, tifus, disentería), y la Sanitary Commission redujo drásticamente las muertes.

El problema principal es que los segmentos exteriores son necesariamente mayores y quedan enfatizados de forma desproporcionada; la distorsión crece al alejarse del centro. Aun así, R. J. Andrews defiende que la versión en rosas cautivó a los lectores de 1858 y sigue reteniendo la atención hoy, mientras que a nadie le importaron los bar charts que la propia Nightingale también hizo. Alberto Cairo añade que su meta no era solo informar, sino persuadir con una imagen intrigante, inusual y bella. Es el equilibrio entre precisión perceptiva y capacidad de enganchar y permanecer en la memoria. Alternativas más estándar para estos datos: stacked bar chart, stacked area chart o line chart.

## Voronoi diagram

Debe su nombre a Georgy Voronoi, matemático ruso de finales del siglo XIX. El diagrama de Voronoi divide un espacio con cierto número de puntos (llamados sites) en el mismo número de polígonos que se tocan en fronteras que no se solapan. Si se deja caer un punto nuevo, estará más cerca del site de su polígono que de cualquier otro. Su propiedad interesante: la frontera de cada polígono equidista de los dos sites más cercanos, y donde se juntan tres fronteras se forma un vértice equidistante de los tres sites más próximos. Existen varios algoritmos para calcular la forma y posición de los polígonos.

Ejemplo simple: una ciudad con nueve estaciones de bomberos (los puntos generadores); cuando hay un incendio, el polígono en el que cae indica qué estación debe responder, bajo el principio de que acude la más cercana (ignorando calles, puentes u otros obstáculos, que algoritmos más complejos sí pueden incorporar). Así, el Voronoi divide la ciudad en componentes y visualiza una relación parte-todo. Se usa para datos geográficos, pero también en biología (estructuras celulares), ecología (crecimiento forestal) y química (posiciones moleculares). Un ejemplo de parte-todo es el gráfico de Will Chase con la población de los países del mundo por región.

Uno de los mapas más famosos de la historia de la visualización es, en realidad, un Voronoi: a mediados de 1854, el médico inglés John Snow, fundador de la epidemiología moderna, marcó cada muerte de un brote de cólera como un trazo en un mapa del Soho de Londres (más de seiscientos muertos en poco más de un mes). El mapa reveló un agrupamiento de muertes en torno a la bomba de agua de Broad Street. Snow trazó una línea punteada que marca los puntos que, por medición cuidadosa, están a igual distancia por la carretera más próxima entre la bomba de Broad Street y las bombas vecinas. Si se marca cada bomba como un site, se construye el Voronoi: el "Snow Map" es en realidad el "Snow Voronoi".

## Ideas clave

- Los gráficos parte-todo muestran cómo las partes se relacionan con un total; varios también sirven para datos jerárquicos.
- El pie chart es familiar y fácil de leer, pero cuesta comparar porciones y discernir valores exactos; cae por debajo de la mitad del ranking perceptivo.
- Reglas del pie chart: las porciones suman 100 por ciento, se ordenan de mayor a menor desde las 12 (salvo orden natural de categoría) y, si hay varios, se mantiene el mismo orden.
- El pie chart brilla cuando el foco suma una cifra redonda (25, 50, 75 por ciento) o cuando se destaca una sola porción; limita las porciones (cinco ya son demasiadas) y evita parejas y "breakout".
- El treemap es un pie chart "cuadrado": compacto, admite más anotación, jerarquías y codificación por color; los rectángulos se comparan mejor.
- El sunburst muestra varios niveles jerárquicos por anillos, pero se recarga con muchas series.
- El Nightingale chart combina cambio en el tiempo y parte-todo, pero exagera los segmentos exteriores; su valor es el equilibrio entre precisión y memorabilidad.
- El Voronoi divide un espacio en polígonos según el site más cercano; sirve para parte-todo y datos geográficos, como el mapa del cólera de John Snow.
