# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 6 — Distribution (Distribución)

> Nota de extracción: texto extraído de la capa de texto del PDF (libro muy visual; los gráficos se describen con palabras); las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo recorre las formas de visualizar distribuciones de datos e incertidumbre estadística. Son gráficos que, para muchos lectores, resultan difíciles porque exigen cierta alfabetización estadística y porque algunos (fan chart, box-and-whisker, violin plot) tienen aspectos poco familiares. La tesis de Schwabish no es que sean malos gráficos, sino que, con buen etiquetado y diseño, incluso el más esotérico puede ser claro y útil: la clave está siempre en conocer a tu audiencia.

El hilo de datos del capítulo son los ingresos de trabajadores por industria y por estado (U.S. Census Bureau, American Community Survey 2016; más de un millón de personas). Sobre esos datos se construyen todos los gráficos, lo que permite comparar directamente qué muestra y qué oculta cada tipo. Los gráficos siguen las guías de estilo del Dallas Morning News (2005) y usan la tipografía Montserrat (similar a Gotham).

Sales sabiendo cuándo mostrar la distribución completa frente a solo puntos concretos (percentiles), cómo representar la incertidumbre (de aleatoriedad y de desconocimiento), y un catálogo de gráficos: histograma, Pareto, pyramid chart, error bars, intervalo de confianza, gradient/fan chart, box-and-whisker, candlestick, violin, ridgeline, strip, beeswarm, Wilkinson/wheat, raincloud y stem-and-leaf.

## Histograma

El histograma es el gráfico más básico para una distribución: es un tipo de gráfico de barras que muestra la frecuencia tabulada de los datos en intervalos distintos llamados *bins*, que suman la distribución total. La altura de cada barra indica el número de observaciones en ese intervalo. Permite ver dónde se concentran los valores, dónde están los extremos y si hay huecos o valores inusuales.

Se pueden superponer histogramas para comparar distribuciones (por ejemplo, ingresos de hombres y mujeres en EE. UU. en 2016). Dos vías: usar dos gráficos de columnas con colores transparentes para que ambos sean visibles, o combinar columnas y una línea (evita los colores transparentes, pero desequilibra la presentación de los dos grupos; además la línea cruza el centro de cada bin en vez de abarcarlo entero).

Una decisión clave es el ancho de los *bins*: demasiado anchos ocultan patrones, demasiado estrechos difuminan la forma global. No hay un número "correcto", pero existen pruebas estadísticas (raíces cuadradas, logaritmos, raíces cúbicas) que ayudan a elegirlo. La misma distribución se ve muy distinta al pasar de 5 a 30, 50 o 120 bins.

El histograma ayuda a entender el sesgo y la forma: *right-skewed* (más datos a la izquierda), *left-skewed* (más a la derecha), *bimodal* (dos picos), *multimodal* (varios picos), simétrica (reparto equilibrado en torno a un valor central) y uniforme (reparto aproximadamente igual). Dos distribuciones muy distintas pueden compartir media y mediana; por eso visualizar los datos es inestimable antes de aplicar pruebas estadísticas.

Una variante es el gráfico de Pareto (por Vilfredo Pareto): barras con los valores individuales de cada grupo más una línea con el total acumulado. Es quizá la excepción a la regla contra los ejes duales, porque ambas series son la misma métrica (distribución marginal y distribución acumulada). En el ejemplo, muestra los ingresos totales de trece grandes industrias de EE. UU.

## Entender los percentiles

Imagina 100 personas en un escenario ordenadas de izquierda a derecha según sus ingresos. La de menores ingresos (a tu izquierda) está en el percentil 1: el 99 % gana más que ella. La del extremo derecho está en el percentil 99 (top 1 %). El punto que divide a todos en dos mitades iguales es el percentil 50 o mediana. La matemática no cambia aunque haya 100, 1.000 o 150 millones de personas; como los percentiles son independientes del tamaño de la población, se pueden comparar entre grupos (países, industrias).

Otras medidas globales: la media (suma de todos los valores dividida entre el número de observaciones) puede distorsionarse con valores grandes —si una persona pasara a ganar 100 millones, la media cambiaría drásticamente pero la mediana no, porque esa persona seguiría en el extremo derecho—. La varianza mide cuánto se alejan las observaciones de la media: una varianza grande indica datos dispersos; una pequeña, lo contrario. La descomposición completa queda fuera del alcance del libro, pero conviene estudiarla para entender la forma y el alcance de los datos.

## Pyramid chart

Se usa sobre todo para métricas de población (natalidad, mortalidad, edad, niveles de población). Coloca dos grupos a cada lado de un eje vertical central. Es una subcategoría del diverging bar chart, reservada para comparar distribuciones (normalmente edades). Riesgo: el lector puede asumir que las barras hacia la izquierda son valores negativos y las de la derecha positivos.

Su ventaja es que, al apoyarse ambos grupos en la misma línea base vertical, se aprecia la forma global de la distribución. Los ejemplos de EE. UU. y Japón en 2016 (mujeres a la izquierda, hombres a la derecha, cada fila un grupo de edad) muestran de un vistazo que Japón tiene más población mayor y EE. UU. más joven. Como las barras no están contiguas, cuesta comparar el total de hombres y mujeres; si ese es el objetivo, conviene un paired bar chart o un dot plot. Alternativas a la pirámide básica: dot plot o lollipop chart (puntos sobre el eje horizontal unidos por una línea). Para comparar los dos países, superponer los gráficos facilita la lectura, pero usar codificaciones distintas (barras y líneas) puede sobreenfatizar una serie.

## Visualizar la incertidumbre estadística

Contabilizar la incertidumbre —y dejar claro que lo has hecho— genera confianza en el lector. Hay dos tipos. La *uncertainty from randomness* afecta a la confianza estadística de modelos y resultados (por ejemplo, el margen de error de una encuesta: "54 % de aprobación, ±4 puntos"). La *uncertainty from unknowns* ocurre cuando los datos son inexactos, poco fiables, imprecisos o desconocidos (p. ej., edades de bebés en meses en vez de semanas). La primera se puede modelar y visualizar; la segunda no siempre se resuelve con más datos.

Con los datos del Census, muchas personas pueden declarar mal sus ingresos (mienten, redondean, omiten trabajos secundarios, estiman los del cónyuge), y la encuesta solo cubre a una parte de la población. Las líneas y las barras sugieren certeza con sus bordes nítidos, pero esa certeza rara vez es real. Alberto Cairo (*How Charts Lie*) recuerda que la ciencia y la estadística solo ofrecen estimaciones imperfectas, sujetas a cambios.

La investigadora Jessica Hullman encontró cuatro razones por las que los autores omiten la incertidumbre: no querer confundir al lector, no tener acceso a esa información, no saber calcularla, y no querer que los datos parezcan cuestionables. Según ella, omitirla hace que los datos se interpreten como más creíbles de lo que son. Esta sección presenta señales visuales de incertidumbre: error bars, intervalos de confianza, gradient charts y fan charts.

## Error bars, intervalo de confianza, gradient y fan chart

Las *error bars* son la forma más simple y común de mostrar incertidumbre: marcadores que señalan el margen de error o el intervalo de confianza. No son un gráfico por sí mismas, sino un añadido a barras o líneas. Sus extremos pueden representar percentiles, el error estándar, el intervalo de confianza del 95 % o un número fijo; por eso hay que etiquetarlos claramente para evitar confusiones. En barras aparece el sesgo "within-the-bar" (tendemos a juzgar los puntos dentro de la barra como más probables que los de fuera). La investigación sugiere que juzgamos mejor la incertidumbre con violin plots, stripe plots o gradient plots.

El *confidence interval chart* usa líneas o áreas sombreadas para mostrar rangos de incertidumbre, a menudo a lo largo del tiempo. En su forma básica es un gráfico de líneas con tres líneas: estimación central, valor superior y valor inferior (intervalos de confianza, errores estándar o un número fijo). La línea central debe destacarse más gruesa u oscura.

El *gradient chart* (o stripe plot) muestra distribuciones o incertidumbre añadiendo un degradado de color a uno o ambos lados del valor principal; se llama así por el uso del degradado, no por su forma. Con los mismos datos que las error bars, la media se codifica con una línea horizontal oscura y los percentiles 25-75 con el degradado; el color puede representar múltiplos del error estándar (más incertidumbre cuanto más lejos del centro). Un ejemplo célebre son las *stripe charts* de temperatura de Ed Hawkins (1850-2018), de azules fríos a rojos cálidos, sin ejes ni etiquetas, pensadas para públicos no acostumbrados a los gráficos.

El *fan chart* es como un gradient plot para gráficos de líneas: el área entre los intervalos cambia de color o saturación según el valor. Los valores más próximos a la estimación central son los más oscuros y se aclaran hacia fuera, señalando el paso de mayor a menor confianza estadística. El ejemplo muestra la mediana de ingresos del hogar en EE. UU. en 50 años, con el error estándar dividido en ocho bandas.

Una última estrategia no es visual sino de diseño: los efectos "sketchy", "gooey" o "painty" (dibujado a mano) añaden bordes irregulares que transmiten imprecisión. La investigación sugiere que generan más interacción y permiten "atar lo esbozado a la incertidumbre". Ejemplos: Mona Chalabi (*The Guardian*) y Jo Wood (University of London).

## Box-and-whisker plot y candlestick

El box-and-whisker plot (o boxplot), llamado originalmente *schematic plot* por su inventor John W. Tukey, usa una caja y líneas para mostrar percentiles concretos. Es un resumen compacto, con menos detalle que un histograma o un violin. Tiene cinco componentes principales: (1) la mediana (línea dentro de la caja); (2) dos *hinges* (bordes de la caja), normalmente percentiles 25 y 75, cuya diferencia es el rango intercuartílico o IQR; (3) los extremos superior e inferior, a 1,5 veces el IQR; (4) dos *whiskers* (líneas) que conectan los hinges con una observación o percentil; (5) *outliers*, puntos más alejados que los extremos de los whiskers. Cada componente puede variar: algunos sustituyen outliers por mínimo/máximo o percentiles 1 y 99, otros usan el rango semi-intercuartílico, otros añaden media o error estándar.

En el ejemplo de las trece industrias, la línea central es la mediana, los bordes de la caja los percentiles 25 y 75, y los whiskers los percentiles 10 y 90. Schwabish prefiere ordenar por valor (no alfabéticamente), salvo que el lector necesite localizar categorías concretas (p. ej., los cincuenta estados). Al dibujar solo percentiles, decidimos explícitamente no mostrar toda la distribución; conviene explorar bien los datos para no ocultar patrones.

El *candlestick* (gráfico de velas) se parece al boxplot pero visualiza otra cosa: cambios de precio de acciones, bonos y materias primas en el tiempo. La caja central ("real body") muestra la diferencia entre precio de apertura y cierre, y las líneas ("wick") los valores mínimo y máximo del día. En el ejemplo (acciones de Alphabet, ene-feb 2018) el color distingue subidas de bajadas y, debajo, otro gráfico muestra el volumen, apilado en vez de usar eje dual.

## Violin chart y ridgeline plot

El *violin chart* muestra la forma de toda la distribución (no percentiles sueltos ni intervalos agrupados). Las zonas más anchas tienen más valores; las estrechas, menos; se puede añadir un punto para la media de cada grupo. Requiere estimar la *kernel density*: una forma de estimar la distribución de una variable, como un histograma pero suavizado para parecer continuo mediante algoritmos. En el violin, esas densidades se dibujan reflejadas en torno a una línea central invisible. Es más rico que el boxplot, pero más difícil de crear y de entender (en Excel el boxplot es gráfico por defecto; el violin exige calcular las densidades a mano).

El *ridgeline plot* es una serie de histogramas o density plots para distintos grupos, alineados sobre el mismo eje horizontal y con ligero solapamiento vertical; es como un histograma de small multiples o un horizon chart. El solapamiento puede ser un problema, pero se compensa con la rapidez con que se ven alinearse las distribuciones. El ridgeline más famoso es la portada del álbum *Unknown Pleasures* (Joy Division, 1979): Jen Christiansen rastreó su origen hasta la tesis doctoral de 1970 de Harold D. Craft, Jr. (pulsos de radio de un púlsar). Funciona bien cuando las distribuciones difieren de una fila a otra. Ejemplo del *Guardian* (2018): brecha salarial entre hombres y mujeres en más de diez mil empresas británicas, con colores a cada lado de la línea del 0 % y ordenado de mayor a menor brecha.

## Visualizar la incertidumbre mostrando los datos

Otra vía es simplemente *mostrar* los datos. El *strip plot* dibuja los puntos sobre un único eje (horizontal o vertical). En el ejemplo se muestran los ingresos medios de cada estado por industria (no de 1,3 millones de trabajadores, que serían una línea maciza). Con colores transparentes que se oscurecen al solaparse se ve dónde se concentran los datos. No hay regla sobre cuántos puntos son demasiados. El ejemplo de NPR dibuja un punto por distrito escolar: naranja para gasto por alumno bajo la media, verde para gasto por encima.

El *beeswarm plot* usa *jittering*: altera ligeramente los valores para que los puntos no se solapen y cada uno sea visible. La clave es manipularlos lo justo para hacerlos visibles sin cambiar la forma de la distribución; con demasiados puntos, el jittering los desplaza tanto que modifica los datos. Conviene anotar algunos outliers para mostrar al lector que se han considerado. El ejemplo de Axios (ocho beeswarm) muestra el gasto en propiedades de The Trump Organization antes y después de las elecciones de 2016, combinando color, tamaño y densidad.

El *Wilkinson Dot Plot* (o dot histogram; Wilkinson los llamó *histodot plots*) es como un histograma, pero en vez de una barra apila puntos dentro de cada bin: cada punto es una observación del bin, no su valor exacto. El *wheat plot*, de Stephen Few, lo mejora mostrando los valores reales sobre el eje horizontal, aún agrupados por bins y apilados verticalmente; la alineación curva de los puntos refleja la distribución dentro de cada intervalo. El límite es que muchos valores se solapan. Hay un trade-off: el wheat plot ofrece más detalle y resulta más atractivo, pero el histograma es más inmediato. Ejemplo del *Guardian* con un punto por empresa.

El *raincloud plot* (nombrado por Micah Allan) muestra a la vez la densidad (como un violin) y los puntos reales debajo, como una nube que llueve datos: permite ver resumen, outliers y patrones, a costa de más esfuerzo de lectura. Ejemplo de Len Kiefer (Freddie Mac): tipos hipotecarios semanales de 2010 a 2019.

El *stem-and-leaf plot* es una tabla que muestra los valores posicionales: el "stem" (primeros dígitos) en una columna y las "leaves" (últimos dígitos) a la derecha. Es útil como herramienta de referencia (horarios de transporte, como el del tren de Tokorozawa, Saitama) o para distribuciones básicas con pocos datos; al ser tabla, pierde ventajas de una visualización tradicional.

## Ideas clave

- El histograma es la base: agrupa en *bins* y su ancho determina cuánto patrón o forma se revela; ayuda a ver sesgo (right/left-skewed, bimodal, simétrica, uniforme).
- Percentiles y mediana son independientes del tamaño de la población y comparables entre grupos; la media se distorsiona con valores extremos, la mediana no.
- Hay dos incertidumbres: la de aleatoriedad (modelable y visualizable) y la de desconocimiento (no siempre resoluble con más datos); mostrarla genera confianza.
- Para incertidumbre: error bars (simples pero con sesgo "within-the-bar"), confidence interval chart, gradient/stripe chart y fan chart (color = pérdida de confianza).
- Mostrar percentiles concretos (box-and-whisker) frente a toda la distribución (violin, ridgeline, basados en kernel density) implica decidir qué se oculta.
- Mostrar los datos uno a uno: strip plot, beeswarm (jittering), Wilkinson/wheat plot y raincloud; todos tienen un límite de puntos antes de solaparse.
- No confundir candlestick (precios financieros en el tiempo) con box-and-whisker (distribución/incertidumbre), aunque se parezcan.
- Regla transversal: recuerda a tu audiencia; en entornos técnicos no hace falta explicar la mediana o el IC del 95 %, pero ante público general hay que definir y anotar.
