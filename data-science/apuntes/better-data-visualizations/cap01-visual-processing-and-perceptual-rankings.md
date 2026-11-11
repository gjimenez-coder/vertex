# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 1 — Visual Processing and Perceptual Rankings (Procesamiento visual y jerarquías perceptivas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Es un libro muy visual, así que los gráficos se describen con palabras.

## Lo que necesitas saber

Antes de crear gráficos conviene entender cómo el cerebro percibe los estímulos visuales, porque eso guía qué tipo de gráfico es más adecuado para unos datos concretos. La pregunta central es con qué exactitud puede el lector percibir los valores: algunos gráficos permiten distinguir diferencias finas (por ejemplo, entre 2 por ciento y 2,3 por ciento) mejor que otros.

La tesis del capítulo es que la visualización de datos es una mezcla de ciencia y arte. A veces queremos máxima precisión perceptiva (comparaciones exactas); otras veces queremos captar y mantener la atención del lector, aunque eso sacrifique algo de exactitud. Saber dónde situarse en ese espectro depende de los objetivos y de la audiencia.

Sales sabiendo tres cosas: la jerarquía perceptiva que ordena las codificaciones de datos según su exactitud; el valor de visualizar datos, ilustrado con el Cuarteto de Anscombe; y las reglas de percepción (principios Gestalt y procesamiento preatentivo) que puedes usar para codificar y resaltar datos.

## Jerarquía perceptiva de las codificaciones

Una línea de investigación de los últimos treinta años (Cleveland y McGill, 1984; Heer, Bostock y Ogievetsky, 2010; recogida por Alberto Cairo, 2016) ordena las codificaciones de datos —puntos, líneas, barras— según con qué facilidad el lector estima su valor. El diagrama de jerarquía perceptiva coloca arriba lo que se estima con más exactitud y abajo lo que solo permite estimaciones generales.

El orden, de mayor a menor exactitud, es aproximadamente: posición en una escala común; posición en escalas idénticas no alineadas; longitud; dirección/pendiente; ángulo; área; volumen; y, al final, sombreado/saturación y matiz de color. Es más fácil comparar datos en gráficos de líneas, barras y áreas que comparten el mismo eje o línea base. Datos en ejes no alineados (dos barras desplazadas en ejes distintos) son algo más difíciles de leer. Y resulta mucho más fácil leer un valor exacto en un gráfico de barras que en un mapa con países sombreados por color.

Los gráficos estándar (barras, líneas) son tan comunes porque son perceptivamente más exactos, familiares y fáciles de crear. Los gráficos no estándar —con círculos o curvas— pueden no permitir percibir los valores exactos con la misma precisión.

## Precisión perceptiva frente a interés: ciencia y arte

La exactitud perceptiva no siempre es el objetivo, y a veces no lo es en absoluto. Lograr que el lector se enganche con un gráfico puede ser igual de importante, o más. Los gráficos no estándar pueden revelar mejor patrones y tendencias, o simplemente, por ser distintos, atraer la atención.

El autor ilustra esto con la gráfica de Federica Fragapane (para La Lettura, Corriere della Sera) sobre las cincuenta ciudades más violentas del mundo en 2017. El eje vertical mide la población de cada ciudad y el horizontal la tasa de homicidios por 100.000 habitantes. Cada ciudad es un icono: el número de líneas representa el número de homicidios, y colores, formas y marcadores añaden país de origen (símbolo central), región (línea discontinua vertical) y cambio respecto a 2016 (azul para descensos, rojo para aumentos). Podría haber sido un gráfico de barras o de líneas, pero entonces, ¿te acercarías a leerlo con detalle?

A veces hay que hacer los gráficos interesantes y atractivos aun a costa de la exactitud absoluta. El trabajo del creador de contenido es animar a la gente a leer y usar el gráfico, incluso "violando" reglas perceptivas. Pensar en la audiencia no es solo distinguir entre responsables de decisiones, académicos y público general: también significa pensar en distintos niveles de interés y compromiso con el propio gráfico.

No debemos suponer que el lector atenderá a todo, ni siquiera con un tipo de gráfico familiar. Las barras, líneas y tartas se ven constantemente y a menudo resultan aburridas; los gráficos aburridos se olvidan. Leer un gráfico no es la comprensión espontánea de ver una foto, sino un proceso cognitivo más parecido a leer un párrafo. El autor cita a Cecelia Watson —"¿Y si pensáramos menos en reglas y más en comunicación?"— y a Elijah Meeks, quien sostiene que un gráfico, como cualquier comunicación, debe ser convincente, y si tu gráfico de barras óptimo ha quedado reducido a ruido de fondo, es tu responsabilidad hacerlo más atractivo (PDF p. 32).

Introducir un gráfico nuevo o distinto añade un obstáculo para el lector, que puede ser grande (un tipo totalmente nuevo) o pequeño (uno que ocupa un lugar más bajo en la escala de exactitud). Para superarlo quizá haya que explicar cómo leer el gráfico, pero puede merecer la pena si despierta curiosidad.

¿Cuándo usar un gráfico no estándar? Probablemente no en trabajos académicos, donde la exactitud es primordial y queremos comparaciones claras y eficientes. Sí en otros casos —gráficos destacados o autónomos, blogs, informes breves, redes sociales—, donde algo diferente puede atraer a la gente el tiempo suficiente para transmitir el argumento. Como ejemplos, el autor menciona el índice interactivo "Better Life" de la OCDE, que deja explorar distintas métricas de lo que significa vivir mejor, y la pieza del artista y periodista Jaime Serra Palou, que registra su consumo diario de café durante un año usando las manchas de la taza. Una línea mostraría los mismos datos, pero ¿te detendrías a mirarla? A veces se pueden combinar ambas cosas: un gráfico llamativo como pieza principal y gráficos estándar y tablas con el detalle. Hay investigación que muestra que los gráficos novedosos o personalizables animan al lector a procesar activamente el contenido.

## El Cuarteto de Anscombe

El valor de visualizar datos se ilustra con el Cuarteto de Anscombe, publicado en 1973 por el estadístico Francis Anscombe. Son cuatro pares de datos (X e Y) que, pese a parecer distintos en una tabla, comparten los mismos estadísticos resumen: misma media de X y de Y, misma varianza, misma correlación (0,816) y la misma recta de regresión, y = 3 + 0,5x.

Ante la tabla, la mayoría de la gente observa detalles sueltos (que las X son enteras, que hay un 12,7 o un 19 que destacan), pero no comenta la relación entre series, que es lo que de verdad queremos entender. El ejemplo demuestra lo difícil que es extraer patrones y estadísticos básicos de una tabla.

Al representar los mismos datos en cuatro gráficos de dispersión, las relaciones saltan a la vista: la correlación positiva en los cuatro pares, la curvatura del segundo par (invisible en la tabla) y los valores atípicos 12,7 y 19,0 de los dos últimos. Y recordamos mucho mejor cuatro gráficos pequeños que la tabla original. El autor cita al biólogo molecular John Medina (Brain Rules): "Cuanto más visual es la entrada, más probable es que se reconozca y se recuerde" (PDF p. 36).

## Principios Gestalt de la percepción visual

La teoría Gestalt, desarrollada a principios del siglo XX por psicólogos alemanes, describe cómo tendemos a organizar los elementos visuales en grupos. Su desarrollo se interrumpió con el régimen nazi y la Segunda Guerra Mundial, y después se criticó por falta de rigor metodológico, pero sus ideas persisten en teoría de la información, ciencia de la visión y neurociencia cognitiva. Seis principios son especialmente útiles para crear gráficos:

- Proximidad: percibimos como grupo los objetos cercanos entre sí (etiquetas con puntos, barras entre sí, o dos nubes de puntos que se ven como dos clusters, uno arriba a la derecha y otro abajo a la izquierda).
- Similitud: agrupamos los objetos que comparten color, forma o dirección; añadir color a esa dispersión refuerza los dos grupos.
- Cierre perimetral (enclosure): los objetos delimitados se perciben como grupo; podemos encerrar los dos clusters con círculos u otras formas.
- Clausura (closure): el cerebro ignora los huecos y completa estructuras abiertas; vemos un eje horizontal y uno vertical como un único objeto, y en una línea con datos faltantes cerramos mentalmente el hueco con una recta, aunque el patrón real pudiera subir y bajar.
- Continuidad: los objetos alineados o que se prolongan se perciben como grupo y el ojo busca un camino suave; por eso no hace falta la línea del eje horizontal en un gráfico de barras, porque las barras ya marcan un camino consistente.
- Conexión: percibimos como un mismo grupo los objetos conectados; una masa de puntos azules parece una sola serie, pero el color revela dos series y, al conectar los puntos, se ve cómo coinciden al principio y luego divergen.

## Procesamiento preatentivo

El procesamiento preatentivo es un subconjunto de la teoría Gestalt y el proceso que el autor más tiene en cuenta al crear sus gráficos. Como el ojo detecta un conjunto limitado de características visuales, combinamos los rasgos de un objeto y los percibimos inconscientemente como una sola imagen. Los atributos preatentivos atraen la atención hacia una parte concreta del gráfico, pareciendo "saltar" de su entorno.

El autor lo demuestra con una tabla de ventas: buscar los cuatro números más altos entre filas y columnas cuesta trabajo; pero si esos cuatro números se resaltan con color o con intensidad/peso, se identifican sin esfuerzo. También funciona en fotos: en una imagen de frutas donde un grupo de tomates es algo mayor y está separado, el ojo va directo a la esquina superior derecha; en otra imagen equilibrada, nada destaca.

Entre los atributos preatentivos aprovechables están: forma, cierre perimetral, ancho de línea, saturación, color, tamaño, marcas, orientación, posición, 3D, longitud, curvatura, densidad, clausura y nitidez. Se aplican directamente a los gráficos: una línea usa la posición de los puntos para indicar el dato, una barra usa la longitud. Y sirven para dirigir la atención: encerrar con una caja gris la zona de "Forecast" de un gráfico de líneas lleva el ojo a la derecha, y colorear unos pocos puntos de una dispersión (dejando el resto en gris) los destaca.

Con estas reglas básicas de percepción estamos mejor preparados para reconocer e interpretar los rasgos visuales que usamos para codificar y resaltar datos, antes de pasar a las directrices de visualizaciones más efectivas.

## Ideas clave

- La visualización de datos es mezcla de ciencia (exactitud perceptiva, comparaciones precisas) y arte (enganchar y mantener la atención); la audiencia y los objetivos deciden dónde situarse.
- La jerarquía perceptiva ordena las codificaciones por exactitud: posición en escala común arriba; área, volumen y color abajo.
- Los gráficos estándar son más exactos, familiares y fáciles; los no estándar sacrifican exactitud pero pueden atraer, revelar patrones y hacerse memorables.
- Usa gráficos no estándar fuera del ámbito académico (piezas destacadas, blogs, redes); en trabajos académicos prima la exactitud.
- El Cuarteto de Anscombe (1973) muestra cómo cuatro conjuntos con los mismos estadísticos (media, varianza, correlación 0,816, recta y = 3 + 0,5x) revelan sus diferencias solo al graficarlos.
- Lo visual se recuerda mejor: "cuanto más visual es la entrada, más probable es que se reconozca y se recuerde" (Medina).
- Los seis principios Gestalt —proximidad, similitud, cierre perimetral, clausura, continuidad y conexión— explican cómo agrupamos elementos visuales.
- El procesamiento preatentivo (color, peso, posición, longitud, etc.) permite dirigir la atención del lector hacia lo importante sin esfuerzo consciente.
