# Storytelling with Data — Cole Nussbaumer Knaflic (Wiley, 2015)
## Capítulo 3 — Clutter Is Your Enemy! (¡El desorden es tu enemigo!)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (libro muy visual, los gráficos se describen con palabras); las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Cada elemento que añadimos a una página o pantalla consume carga cognitiva de la audiencia: energía mental para procesarlo. La tesis del capítulo es que debemos revisar con criterio los elementos visuales y eliminar todo lo que no aporte valor informativo suficiente para justificar su presencia. A ese ruido visual la autora lo llama *clutter* (desorden), y lo presenta como un enemigo a batir.

El desorden importa porque hace que nuestros visuales parezcan más complicados de lo necesario. Cuando algo se siente complicado, la audiencia decide que no vale la pena el esfuerzo de entenderlo y pasa de largo —el momento "ugh"—, y perdemos la capacidad de comunicar. Lo que más cuenta es la carga cognitiva *percibida*: cuánto cree la audiencia que va a tener que trabajar, una decisión casi inconsciente que puede marcar la diferencia entre transmitir el mensaje o no.

Sales del capítulo sabiendo reconocer y eliminar el desorden mediante tres herramientas: los principios Gestalt de percepción visual (para distinguir señal de ruido), la atención al orden visual (alineación y espacio en blanco) y el uso estratégico del contraste. El capítulo cierra con un decluttering paso a paso sobre un caso real.

## Carga cognitiva, data-ink y señal-ruido

La carga cognitiva es el esfuerzo mental necesario para asimilar información nueva; al pedirle trabajo a la audiencia usamos su capacidad de procesamiento, que es finita. Hay que evitar la carga cognitiva *extraña*: la que consume recursos mentales pero no ayuda a entender la información (la diapositiva recargada o el gráfico que se abandona a mitad).

Para guiar esta reducción, la autora recupera dos conceptos. Edward Tufte, en *The Visual Display of Quantitative Information*, habla de maximizar el **data-ink ratio**: "cuanto mayor sea la proporción de tinta de un gráfico dedicada a los datos, mejor" (PDF p. 88). El mismo principio se expresa como maximizar la **razón señal-ruido** (Nancy Duarte, *Resonate*), donde la señal es la información que queremos comunicar y el ruido son los elementos que no suman o incluso restan al mensaje.

El objetivo general es minimizar la carga cognitiva percibida, hasta donde sea razonable sin perder la capacidad de transmitir la información.

## Principios Gestalt de percepción visual

La escuela Gestalt de psicología estudió a principios del siglo XX cómo las personas perciben orden en el mundo. Sus principios siguen vigentes y ayudan a identificar qué elementos son señal y cuáles ruido. El capítulo trata seis, cada uno con aplicación a tablas o gráficos:

- **Proximidad**: percibimos como grupo los objetos físicamente cercanos. En una tabla, variando solo el espaciado entre elementos, la vista se dirige hacia abajo por las columnas o a lo ancho por las filas, sin necesidad de bordes.
- **Similitud**: objetos de igual color, forma, tamaño u orientación se perciben relacionados. En una tabla, usar el mismo color en una fila invita a leer a lo ancho (y no por columnas), eliminando la necesidad de bordes.
- **Encierro (enclosure)**: objetos encerrados juntos se ven como grupo; basta un sombreado de fondo ligero. Sirve, por ejemplo, para separar visualmente datos de pronóstico (forecast) de datos reales (actual) dentro de un mismo gráfico.
- **Cierre (closure)**: tendemos a percibir elementos individuales como una forma reconocible única y rellenamos los huecos. Esto nos dice que bordes de gráfico y sombreados de fondo (defaults de Excel) son innecesarios: al quitarlos, el gráfico sigue viéndose como un todo y los datos destacan más.
- **Continuidad**: la vista busca el camino más suave y crea continuidad aunque no exista explícitamente. Permite, por ejemplo, eliminar la línea del eje vertical: el espacio en blanco consistente entre las etiquetas y los datos basta para que las barras se perciban alineadas.
- **Conexión**: percibimos como grupo los objetos conectados físicamente. La conexión suele tener mayor valor asociativo que el color, el tamaño o la forma similares (aunque no suele superar al encierro). Es el principio que aprovechan los gráficos de líneas al unir los puntos para mostrar orden en los datos.

En conjunto, los principios Gestalt explican cómo ve la gente, lo que nos permite detectar elementos innecesarios y facilitar el procesamiento de nuestras comunicaciones visuales.

## Falta de orden visual

Cuando el diseño es cuidado, se desvanece en el fondo y la audiencia ni lo nota; cuando no, siente la carga. El capítulo compara una ficha de resultados de encuesta (atributos que valoran los clientes al elegir proveedor de servicios) antes y después: el contenido es idéntico, solo cambian la ubicación y el formato de los elementos, y la segunda versión "se siente más fácil" gracias al orden. Las dos palancas son la alineación y el espacio en blanco.

### Alineación

El cambio de mayor impacto fue pasar de texto centrado a texto justificado a la izquierda. El centrado no crea líneas limpias ni a izquierda ni a derecha y hace que incluso un buen diseño parezca descuidado. El objetivo es crear líneas limpias (horizontales y verticales) de elementos y espacio en blanco. Como la audiencia suele empezar arriba a la izquierda y recorrer la página en "z", conviene justificar títulos, títulos de ejes y leyenda arriba a la izquierda, para que encuentren primero las claves de lectura y luego los datos. Un truco práctico: activar reglas o cuadrículas del software, o usar una tabla provisional como guía y luego ocultar sus bordes.

Deben evitarse los elementos diagonales (líneas y texto): se ven desordenados y el texto girado es más difícil de leer. Un estudio (Wigdor & Balakrishnan, 2005) halló que leer texto rotado 45 grados es en promedio un 52% más lento, y rotado 90 grados un 205% más lento.

### Espacio en blanco

Mucha gente teme el espacio en blanco en la página y cae en "queda hueco, pongamos algo" o, peor, "añadamos más datos". Nunca se añaden datos por añadir: solo con un propósito claro. El espacio en blanco es a la comunicación visual lo que las pausas al hablar en público; su ausencia resulta incómoda, igual que un discurso atropellado sin pausas. Bien usado, dirige la atención hacia lo que no es espacio en blanco: una pausa dramática de 15 segundos tras una afirmación potente capta la atención. Pautas mínimas: mantener los márgenes libres de texto y visuales, y no estirar los gráficos para rellenar el espacio disponible, sino dimensionarlos según su contenido. Si algo es muy importante, puede ser lo único en la página —una sola frase o incluso un solo número.

## Uso no estratégico del contraste

El contraste claro es una señal que indica a la audiencia dónde mirar; su falta es otra forma de desorden visual. La autora cita una analogía de Colin Ware (*Information Visualization: Perception for Design*, 2004): es fácil ver un halcón en un cielo lleno de palomas, pero según aumenta la variedad de aves, el halcón se vuelve más difícil de distinguir. Cuantas más cosas hacemos diferentes, menos destaca cada una; si hay algo realmente importante (el halcón), debe ser lo único muy distinto del resto.

El ejemplo es un índice de desempeño ponderado (weighted performance index) de una tienda frente a cinco competidores, en cinco categorías: Selection, Convenience, Service, Relationship y Price. El gráfico original —un scatterplot con un color y forma por competidor— resulta ocupado, confuso y agotador: exige mucho ir y venir entre la leyenda y los datos, y "Our Business" (el diamante azul) queda a veces tapado por otros puntos, impidiendo la comparación más importante.

La versión rediseñada usa el contraste estratégicamente: un gráfico de barras horizontales, con las categorías en el eje vertical y "Our business" en azul frente a los competidores en gris. Se reescalaron los valores a positivos y se omitió deliberadamente la escala del eje x para forzar el foco en las diferencias relativas, no en los números exactos. Así se ven rápido dos cosas: cómo le va a "Our business" entre categorías (alto en Price y Convenience, bajo en Service y Selection) y cómo se compara con los competidores dentro de cada categoría. Las categorías se ordenaron por índice decreciente y se añadió un rango relativo (relative rank). Los competidores se distinguen por su orden de aparición: esto no permite identificar rápido a cada uno, pero funciona si esa es una comparación de segundo o tercer orden.

Cuando los detalles redundantes no son desorden: hay elementos que siempre deben conservarse junto a los números —signos de dólar, de porcentaje y comas en cifras grandes—. Un gráfico titulado "Monthly Sales ($USD Millions)" con etiquetas 10, 20, 30... es confuso; incluir el "$" en cada número facilita la interpretación.

## Decluttering paso a paso

Escenario: diriges un equipo de IT que recibe tickets (incidencias) de los empleados; en el último año se marcharon un par de personas sin reemplazo y hay quejas por tener que "cubrir el hueco". Para fundamentar una petición de contratación, graficas la tendencia mensual de tickets recibidos frente a procesados. A partir del gráfico rápido inicial, la autora identifica seis cambios para reducir el desorden:

1. **Quitar el borde del gráfico**: suele ser innecesario (principio de cierre); usa espacio en blanco para separar el visual de otros elementos.
2. **Quitar las líneas de cuadrícula (gridlines)**: si ayudan a trazar hasta el eje, déjalas finas y en gris claro para que no compitan con los datos; cuando puedas, elimínalas para dar más contraste.
3. **Quitar los marcadores de datos**: añaden carga cognitiva para procesar datos que las líneas ya muestran. Úsalos a propósito y con un fin, no por defecto de la aplicación.
4. **Limpiar las etiquetas de los ejes**: eliminar los ceros a la derecha (300.00 → 300), que no aportan valor y complican la lectura, y abreviar los meses para que quepan horizontales, eliminando el texto diagonal.
5. **Etiquetar los datos directamente**: en lugar de obligar a ir y volver a la leyenda, coloca las etiquetas junto a los datos que describen (principio de proximidad).
6. **Usar color consistente**: dar a cada etiqueta el mismo color que su serie (principio de similitud) refuerza visualmente que ambas informaciones están relacionadas.

El antes-y-después muestra cuánto se reduce la carga cognitiva y mejora la accesibilidad, aunque la autora aclara que el visual aún no está completo: identificar y eliminar el desorden es solo un gran avance.

## En resumen

Siempre que pones información delante de tu audiencia creas carga cognitiva. El desorden visual genera carga cognitiva excesiva que estorba la transmisión del mensaje. Los principios Gestalt ayudan a entender cómo ve la audiencia y a quitar lo innecesario; la alineación y el espacio en blanco hacen la interpretación más cómoda; y el contraste debe usarse de forma estratégica. El desorden es tu enemigo: destiérralo de tus visuales.

## Ideas clave

- Cada elemento visual consume carga cognitiva; elimina todo lo que no aporte valor informativo suficiente para justificar su presencia.
- Lo decisivo es la carga cognitiva *percibida*: si algo parece complicado, la audiencia abandona antes de intentar entenderlo.
- Maximiza el data-ink ratio (Tufte) o la razón señal-ruido (Duarte): más tinta para los datos, menos para el ruido.
- Los seis principios Gestalt (proximidad, similitud, encierro, cierre, continuidad, conexión) sirven para distinguir señal de ruido y suprimir bordes, cuadrículas y adornos por defecto.
- Alinea los elementos (texto justificado a la izquierda, sin diagonales) y respeta el espacio en blanco; nunca añadas datos solo para rellenar.
- Usa el contraste de forma estratégica: cuantas más cosas diferencies, menos destaca cada una; haz muy distinto solo lo importante.
- Conserva siempre signos de dólar, de porcentaje y comas en cifras grandes; no son desorden.
- El decluttering es un proceso iterativo (borde, cuadrícula, marcadores, etiquetas de ejes, etiquetado directo, color consistente) que reduce carga cognitiva y mejora la accesibilidad.
