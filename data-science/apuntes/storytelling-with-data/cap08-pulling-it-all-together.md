# Storytelling with Data — Cole Nussbaumer Knaflic (Wiley, 2015)
## Capítulo 8 — Pulling It All Together (Juntándolo todo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. El libro es muy visual, por lo que los gráficos se describen con palabras cuando es necesario.

## Lo que necesitas saber
Este capítulo no introduce ideas nuevas: aplica de principio a fin las seis lecciones de los capítulos anteriores sobre un único ejemplo. Esas lecciones son: entender el contexto (cap. 1), elegir un display apropiado (cap. 2), eliminar el desorden (cap. 3), dirigir la atención donde se quiere (cap. 4), pensar como diseñador (cap. 5) y contar una historia (cap. 7).

El caso parte de una visual original (Figura 8.1): un gráfico de barras que muestra el precio medio de venta al público a lo largo del tiempo (2008–2014) de cinco productos de consumo de la competencia (A, B, C, D y E). A partir de ahí se recorre iteración por iteración cómo transformar ese gráfico mediocre en una historia persuasiva que termina en una recomendación de precio.

La tesis es que el proceso completo —no cada lección por separado— es lo que lleva de "simplemente mostrar datos" a "contar una historia con datos". Sales sabiendo cómo encadenar las seis lecciones en un flujo de trabajo real: desde definir audiencia e idea central hasta secuenciar una presentación en vivo que construye tensión y cierra con una llamada a la acción.

## El ejemplo que recorre el capítulo
Trabajamos para una startup que ha creado un producto de consumo y está decidiendo cómo fijarle precio. La pregunta concreta es cómo han cambiado los precios de la competencia a lo largo del tiempo. Los datos son el precio medio anual de A, B, C, D y E entre 2008 y 2014. El objetivo final es recomendar un rango de precio competitivo, y todo el capítulo transforma la Figura 8.1 hasta llegar a esa recomendación.

## Lección 1: entender el contexto
Lo primero ante un reto de visualización es comprender bien el contexto y qué hay que comunicar: identificar una audiencia concreta, qué necesita saber o hacer, y qué datos lo ilustran. El libro define el who, what y how:

- Who: el VP de Producto, el decisor principal del precio.
- What: entender cómo ha cambiado el precio de la competencia y recomendar un rango de precio.
- How: mostrar el precio medio de venta a lo largo del tiempo para los productos A, B, C, D y E.

Con esto se formula la Gran Idea (Big Idea): "Con base en el análisis de precios del mercado a lo largo del tiempo, para ser competitivos recomendamos introducir nuestro producto en un rango de $ABC–$XYZ" (PDF p. 204).

## Lección 2: elegir un display apropiado
Lo que más interesa es la tendencia del precio en el tiempo para cada producto. En la Figura 8.1 la variación de colores entre las barras distrae de esa tendencia. El capítulo avanza mediante iteraciones:

- Figura 8.2: se elimina la variación de color de las barras, dejando todas iguales.
- Figura 8.3: se resalta el periodo de interés, de 2010 en adelante (desde el lanzamiento del Producto C). Se observa un descenso claro del precio medio en A y B, pero no en los productos lanzados más tarde. Esto obligará a cambiar el titular original.
- Figura 8.4: se pasa de barras a un gráfico de líneas, más adecuado para mostrar tendencia en el tiempo, lo que además elimina el efecto de escalones artificial de las barras. Con una línea por producto se ve bien la evolución de cada uno, pero cuesta comparar productos en un mismo instante.
- Figura 8.5: se grafican todas las líneas contra el mismo eje x, lo que permite comparar productos entre sí y reduce la redundancia de etiquetas de año. Excel reintrodujo colores distintos por serie, atados a una leyenda inferior.

Esta vista (Figura 8.5) ya cumple el propósito de ver cómo han cambiado los precios de la competencia; el siguiente paso es facilitar aún más la lectura.

## Lección 3: eliminar el desorden
La Figura 8.5 refleja los ajustes por defecto de Excel. Las mejoras aplicadas son:

- Restar énfasis al título del gráfico: debe estar, pero sin la atención que acapara en negro y negrita.
- Quitar el borde del gráfico y las líneas de cuadrícula, que ocupan espacio sin aportar valor.
- Enviar al fondo los ejes x e y y sus etiquetas poniéndolos en gris, para que no compitan con los datos; alinear las marcas del eje x con los puntos de datos.
- Eliminar la variación de colores entre líneas, para usar el color de forma más estratégica después.
- Etiquetar las líneas directamente (A, B, C, D, E), evitando el ir y venir entre leyenda y datos.

El resultado es la Figura 8.6, un gráfico de líneas limpio y gris con las series rotuladas directamente.

## Lección 4: dirigir la atención donde quieres que mire tu audiencia
Sobre la vista limpia (Figura 8.6) se usan atributos preatentivos, sobre todo el color, para enfocar distintos aspectos del mismo dato:

- Figura 8.7: se revisa el titular inicial ("Price has declined for all products on the market since the launch of Product C in 2010") por uno más preciso: "After the launch of Product C in 2010, the average retail price of existing products declined." El color resalta los segmentos de A y B que caen tras 2010 y un marcador de datos señala la introducción del Producto C en 2010, enlazando visualmente causa y efecto.
- Figura 8.8: con el mismo gráfico se reenfoca a otra observación: al lanzar un producto nuevo en este espacio es típico ver un aumento inicial del precio medio seguido de un descenso.
- Figura 8.9: se destaca que, en 2014, los precios han convergido, con un precio medio de $223, de un mínimo de $180 (Producto C) a un máximo de $260 (Producto A).

Cada vista, con distintos atributos preatentivos, permite ver con claridad cosas distintas y contar fragmentos diferentes de una historia matizada.

El libro incluye un recuadro, "Changing components of a graph in Excel", explicando cómo formatear puntos individuales: normalmente se formatea toda una serie a la vez, pero para destacar puntos concretos (como en las Figuras 8.7–8.9) se hace clic una vez en la serie para seleccionarla, otra vez sobre el punto de interés, botón derecho y "Format Data Point" para cambiar su color o añadir un marcador. Repetir para cada punto. Lleva tiempo, pero facilita la comprensión: es tiempo bien invertido (PDF p. 212).

## Lección 5: pensar como diseñador
De hecho ya se ha estado pensando como diseñador: la forma sigue a la función, pues se eligió un display (forma) que permite a la audiencia hacer lo que necesita (función) con facilidad. Se refinan accesibilidad y estética:

- Hacer la visual accesible con texto: título más simple con solo la primera palabra en mayúscula, y añadir títulos a ambos ejes (vertical y horizontal).
- Alinear elementos para mejorar la estética: el título centrado queda colgando; se alinea arriba a la izquierda. El título del eje y se alinea verticalmente con la etiqueta superior y el del eje x horizontalmente con la etiqueta más a la izquierda, creando líneas más limpias.

El resultado es la Figura 8.10: gráfico "Retail price over time", con eje "Average price" y eje "Year", líneas A–E rotuladas, listo para servir de base a la narrativa.

## Lección 6: contar una historia
Usando la Figura 8.10 como base, se imagina una presentación en vivo de cinco minutos bajo el tema "Competitive Landscape—Pricing". La secuencia de Figuras 8.11–8.19 muestra un camino para contar la historia:

- 8.11: se anuncia la estructura y el objetivo —entender cómo han cambiado los precios para informar el precio del producto propio— prometiendo cerrar con una recomendación concreta.
- 8.12: los Productos A y B se lanzaron en 2008 a precios de $360+.
- 8.13: A y B se han fijado precios similares, con B consistentemente algo por debajo de A.
- 8.14: en 2014, A y B estaban a $260 y $250 respectivamente.
- 8.15: C, D y E se introdujeron más tarde a precios mucho más bajos...
- 8.16: ...pero todos han subido de precio desde sus respectivos lanzamientos.
- 8.17: de hecho, al lanzar un producto nuevo tendemos a ver un aumento inicial de precio seguido de un descenso.
- 8.18: en 2014 los precios han convergido, con media de $223 (mínimo $180 en C, máximo $260 en A).
- 8.19: la recomendación —introducir el producto por debajo de la media de $223, en el rango $150–$200— resaltada como "Recommended range".

La progresión primero expone la estructura, luego construye el recorrido cronológico de precios, introduce tensión cuando C, D y E socavan los precios existentes al lanzarse, restaura el equilibrio cuando los precios convergen, y cierra con una llamada a la acción clara. Mostrando solo los puntos relevantes o empujando el resto al fondo, y combinándolo con una narrativa reflexiva, se guía a la audiencia por la historia.

Este ejemplo cuenta una historia con una sola visual, pero el mismo proceso sirve cuando hay varias visuales en una presentación más amplia: se piensa en la historia global que lo une todo, y las historias de cada visual se tratan como subtramas dentro de la trama mayor.

## In closing (Para cerrar)
El capítulo recorre el proceso completo de principio a fin: construir un entendimiento robusto del contexto, elegir un display apropiado, identificar y eliminar el desorden, usar atributos preatentivos para dirigir la atención, ponerse el sombrero de diseñador añadiendo texto para la accesibilidad y alineando para la estética, y por último elaborar una narrativa y contar una historia. La Figura 8.20 muestra el antes y el después: de la barra genérica con titular "Price has declined for all products..." al gráfico de líneas limpio con la recomendación de rango de precio. Las lecciones nos llevan de simplemente mostrar datos a contar historias con datos.

## Ideas clave
- El capítulo aplica las seis lecciones del libro (contexto, display, desorden, atención, diseño, historia) sobre un único ejemplo de principio a fin.
- Empezar por el contexto: definir who (VP de Producto), what (recomendar rango de precio) y how (precio medio en el tiempo de A–E), y formular la Gran Idea.
- Iterar la elección del display: de barras multicolor a líneas sobre un mismo eje x para ver tendencia y comparar entre productos.
- Eliminar el desorden: quitar bordes y cuadrícula, enviar ejes al fondo en gris, rotular las líneas directamente y restar énfasis al título.
- El color es estratégico: con la misma visual, resaltar segmentos y marcadores distintos permite contar fragmentos diferentes de la historia.
- Pensar como diseñador significa que la forma sigue a la función: texto accesible, títulos de eje y alineación arriba a la izquierda.
- Contar la historia secuenciando láminas (Figuras 8.11–8.19) que construyen tensión y cierran con la recomendación: introducir por debajo de $223, en $150–$200.
- Con varias visuales, hay una historia global que las une; cada visual individual es una subtrama.
