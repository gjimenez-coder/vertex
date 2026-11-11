# Storytelling with Data — Cole Nussbaumer Knaflic (Wiley, 2015)
## Capítulo 9 — Case Studies (Casos de estudio)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Al ser un libro muy visual, los gráficos se describen con palabras cuando es necesario.

## Lo que necesitas saber
Este penúltimo capítulo aplica las lecciones del libro a cinco retos habituales al comunicar con datos, resueltos mediante casos de estudio. En cada uno la autora se centra en el desafío concreto y muestra cómo las mismas herramientas —color, orden, posición, texto y atributos preatentivos— se combinan para dirigir la atención del público.

Los cinco casos son: (1) consideraciones de color sobre un fondo oscuro, (2) uso de la animación en las visualizaciones que presentas, (3) establecer lógica en el orden, (4) estrategias para evitar el "gráfico espagueti" y (5) alternativas a los gráficos de tarta.

La tesis que atraviesa el capítulo es que rara vez hay una única solución correcta: la mejor depende de la situación, de cómo quieres que el público interactúe con la información y del punto que deseas enfatizar. Sales sabiendo que ante un reto de visualización debes pausar, preguntarte qué necesitas que el público sepa o haga y qué historia quieres contar, y probar varias vistas buscando retroalimentación.

## Caso 1: consideraciones de color sobre un fondo oscuro
La autora recomienda por norma el fondo blanco. Un mismo gráfico sencillo mostrado sobre fondo blanco, azul y negro (Figura 9.1) hace que los fondos oscuros se sientan "pesados" y atraigan la vista hacia el fondo, alejándola de los datos. Los elementos claros sobre fondo oscuro crean mayor contraste pero suelen ser más difíciles de leer, por eso evita fondos oscuros y de color.

Aun así, hay consideraciones ajenas al escenario ideal que deben tenerse en cuenta, como la marca del cliente y su plantilla estándar. En un proyecto de consultoría su primer rediseño (Figura 9.2, sobre fondo blanco, con datos de una encuesta a empleados) no encajaba con el estilo audaz del cliente: una plantilla con fondo negro moteado y colores brillantes muy saturados.

Para alinearse con esa marca rehízo su propia mejora sobre fondo oscuro, lo que exigió invertir su proceso mental habitual. Con fondo blanco, cuanto más lejos está un color del blanco, más destaca (el gris destaca poco; el negro, mucho). Con fondo negro ocurre lo mismo, pero el negro pasa a ser la línea base (el gris destaca poco y el blanco destaca mucho). Algunos colores "prohibidos" sobre blanco, como el amarillo, resultan muy llamativos sobre negro.

La versión "más alineada con la marca del cliente" (Figura 9.3) tiene exactamente el mismo contenido que la Figura 9.2, pero se siente muy distinta: buena ilustración de cómo el color afecta al tono general de una visualización.

## Caso 2: aprovechar la animación en lo que presentas
Un problema frecuente es usar una misma vista de los datos tanto para presentar en vivo como para el informe que se circula. En vivo quieres guiar al público por la historia centrándote solo en la parte relevante; la versión circulada —como lectura previa, resumen o para quien no asistió— debe sostenerse sola sin que tú narres. Usar el mismo contenido para ambos fines produce el *slideument* (mitad presentación, mitad documento) que no cubre bien ninguna necesidad.

El ejemplo: una empresa de juegos sociales online quiere contar cómo han crecido los usuarios activos de su juego "Moonville" desde su lanzamiento a finales de 2013. La Figura 9.4 muestra todos los datos de una vez (un gráfico de líneas de usuarios activos en el tiempo). El problema: con tanto dato delante pierdes el control de la atención; el público puede saltar al fuerte aumento de 2015 y dejar de escucharte.

La alternativa es usar animación para acompañar al público mientras cuentas la historia. Se empieza con un gráfico en blanco, lo que obliga a la audiencia a mirar los detalles contigo en vez de interpretar los datos por su cuenta, y genera expectación. Después se muestra o resalta solo el dato relevante para cada punto, forzando la atención justo donde se quiere mientras se habla.

La progresión narrada (Figuras 9.5 a 9.10):
- Primero se montan los ejes: eje Y, usuarios activos (usuarios únicos en los últimos 30 días); eje X, el tiempo desde el lanzamiento.
- Septiembre 2013: lanzamiento con poco más de 5.000 usuarios activos (un punto azul abajo a la izquierda).
- A pesar de una acogida mixta y de casi nula promoción, los activos casi se duplicaron en cuatro meses: unos 11.000 a finales de diciembre.
- Principios de 2014: subida más pronunciada por las promociones *friends and family*.
- Resto de 2014: crecimiento plano al detener el marketing y centrarse en mejorar la calidad.
- 2015 (YTD): el juego renovado se vuelve viral gracias a alianzas con redes sociales; se anticipa superar los 100.000 usuarios activos en junio.

Para la versión que se circula, se usa un único gráfico de líneas que anota directamente los puntos destacados de la historia (Figura 9.11). Esta estrategia exige conocer muy bien tu historia para narrar sin depender de los visuales.

Con software de presentación puedes montar todo en una sola diapositiva: animar que cada imagen aparezca y desaparezca para la versión en vivo, y poner encima la versión anotada final para que sea lo único que se vea en la versión impresa; así usas la misma plataforma para ambos fines. Alternativa: una gráfica por diapositiva que se pasan en secuencia, circulando solo la versión anotada final.

## Caso 3: lógica en el orden
Debe haber una lógica en el orden en que muestras la información. Parece obvio, pero a menudo no se aplica. El ejemplo se centra en aprovechar el orden en datos categóricos dentro de un gráfico de barras horizontales.

Contexto: una empresa con un producto de varias funcionalidades ha encuestado a sus usuarios sobre su uso y satisfacción con cada una. El gráfico inicial (Figura 9.12, con nombres reales sustituidos por Feature A, B, …) ya tiene un orden —descendente según "Very satisfied" + "Completely satisfied"—, pero no se percibe: la vista se va primero al segmento negro "Have not used", y lo más interesante quizá sea la insatisfacción. El problema de fondo es que falta el "so what", la historia.

Con las herramientas de orden, color, posición y texto se pueden contar historias distintas sobre los mismos datos:
- Historia positiva (Figura 9.13): dónde hay más satisfacción, con orden descendente de satisfechos, color destacado, colocándolos como primera serie (la vista los golpea primero al escanear de izquierda a derecha) y un título de acción que dice qué mirar.
- Insatisfacción (Figura 9.14): mismos recursos para destacar dónde están menos satisfechos.
- Funcionalidades no usadas (Figura 9.15): el "Have not used" como comparación primaria; los niveles de satisfacción quedan como comparación de segundo orden por el color.

Si quieres contar las tres historias, reordenar los datos cada vez impone una carga cognitiva innecesaria (impuesto mental, Capítulo 3). Mejor crear un visual base y preservar el mismo orden, familiarizando al público una sola vez y resaltando cada historia con uso estratégico del color:
- Figura 9.16: visual base sin nada resaltado, de "Completely satisfied" a la derecha a "Have not used" a la izquierda (asociación natural: positivo a la derecha, negativo a la izquierda).
- Figura 9.17: satisfacción, con tonos de azul señalando a las Features A y B.
- Figura 9.18: insatisfacción (Features J y N); aquí cuesta más ver el orden relativo que en la Figura 9.14 porque los segmentos no se alinean a una línea base común, pero el tamaño, el color y un recuadro de texto lo compensan.
- Figura 9.19: funcionalidades no usadas; es más fácil ver el orden por la alineación a una línea base común a la izquierda. Como hay que preservar el orden, Feature O queda abajo y se resalta con color y recuadro.

Para un documento que se circula se pueden comprimir todas las vistas en un único visual exhaustivo (Figura 9.20): el color separa las series y guía la vista en "zigzags" entre cada barra resaltada y su recuadro de texto. Es demasiado denso para una presentación en vivo, pero funciona bien en el documento, y dificulta que el público saque otras conclusiones —algo aceptable porque, al comunicar, ya debe haber una historia concreta.

Advertencia: cuando hay orden intrínseco en los datos (categorías ordinales, como rangos de edad 0–9, 10–19, 20–29…), mantén ese orden numérico y dirige la atención con color, posición y recuadros de texto. En resumen: debe haber lógica en el orden de los datos que muestras.

## Caso 4: estrategias para evitar el gráfico espagueti
Un gráfico espagueti es un gráfico de líneas donde estas se solapan tanto que es difícil seguir una serie a la vez (Figura 9.21): parece un puñado de espaguetis crudos tirados al suelo, y resulta igual de informativo, es decir, nada. Los datos del ejemplo muestran tipos de organizaciones sin ánimo de lucro apoyadas por financiadores de una zona. Se presentan tres estrategias.

Enfatizar una línea a la vez. Con atributos preatentivos (color, grosor de línea, marcador y etiqueta de dato) se destaca una sola serie: por ejemplo, el aumento de financiadores que donan a salud (Figura 9.22) o la caída de los que donan a educación (Figura 9.23). Funciona bien en vivo: se explican los detalles del gráfico una vez y luego se recorren las series resaltando qué es interesante y por qué. Hace falta esa narración o texto añadido que aporte la historia.

Separar espacialmente. Se desenredan las líneas tirando de ellas vertical u horizontalmente.
- Vertical (Figura 9.24): cinco gráficos separados organizados como si fueran uno, compartiendo el mismo eje X (año) arriba. No se muestra el eje Y, pero las etiquetas de inicio y fin dan contexto; es clave que el mínimo y el máximo del eje Y sean iguales en cada gráfico para comparar posiciones. Reducidos, se parecen a las *sparklines* de Edward Tufte (*Beautiful Evidence*, 2006). Asume que ver la tendencia de cada categoría importa más que comparar valores entre categorías.
- Horizontal (Figura 9.25): se comparte el mismo eje Y (porcentaje de financiadores) entre las cinco categorías, de modo que la altura relativa permite compararlas con facilidad (en 2015 el mayor porcentaje dona a Salud, menos a Educación, etc.).

Enfoque combinado. Se separa espacialmente y a la vez se enfatiza una línea dejando las demás al fondo para comparar, con separación vertical (Figura 9.26) u horizontal (Figura 9.27). Varios gráficos pequeños juntos se llaman *small multiples*; de nuevo, los ejes X e Y deben tener el mismo mínimo y máximo. Este enfoque, por su densidad, encaja mejor en un informe circulado que en una presentación en vivo.

La meta-lección: no suele haber una única respuesta correcta. Ante un espagueti, no te quedes ahí; piensa qué información quieres transmitir y qué historia contar. A veces la solución es mostrar menos datos: pregúntate si necesitas todas las categorías y todos los años.

## Caso 5: alternativas a los gráficos de tarta
Se retoma el programa piloto de verano sobre ciencia (Capítulo 1), dirigido a mejorar la percepción de la ciencia en niños de 2.º y 3.º de primaria, con una encuesta antes y después usada como evidencia de éxito para pedir financiación futura. El primer intento son dos tartas comparadas (Figura 9.28): antes, el mayor segmento (40%, "OK") se reduce al 14% después; "Bored" y "Not great" suben un punto cada uno, pero el cambio neto es positivo y, tras el programa, casi el 70% expresa algún interés por la ciencia. El problema es que comparar segmentos entre dos tartas obliga al público a esforzarse. Se presentan cuatro alternativas.

Alternativa 1: mostrar los números directamente (Figura 9.29). Si el mensaje principal es la mejora del sentimiento positivo, se puede comunicar solo con uno o dos números directos. A menudo olvidamos la simplicidad y la potencia de esto.

Alternativa 2: gráfico de barras simple (Figura 9.30). Para comparar dos cosas, ponlas lo más cerca posible y alineadas a una línea base común. Alinea las respuestas Antes y Después en la base inferior. La autora prefiere esta vista para el ejemplo porque permite poner recuadros de texto junto a los puntos que describen y limitarse a dos colores (gris y azul), frente a los tres de las siguientes alternativas.

Alternativa 3: barras horizontales apiladas al 100% (Figura 9.31). Cuando importa la relación parte-todo (que no dan las alternativas 1 y 2), estas barras ofrecen línea base a izquierda y derecha, permitiendo comparar los segmentos negativos a la izquierda y los positivos a la derecha entre ambas barras; muy útil para datos de encuestas. Aquí se mantienen las etiquetas del eje X en vez de etiquetar las barras, para poder leer de izquierda a derecha o al revés. Distintas vistas llevan a distintas decisiones de diseño.

Alternativa 4: slopegraph (Figura 9.32). No transmite la idea de todo y partes, y si necesitas un orden de categorías concreto no siempre es ideal (aquí "Bored" y "Not great" quedan intercambiados respecto a una escala ordinal por sus valores). A cambio, la pendiente de cada línea muestra el cambio porcentual de Antes a Después: se ve rápido que "Excited" es la que más sube y "OK" la que más baja, y ordena las categorías de mayor a menor por su posición.

Cualquiera puede ser la mejor opción según la situación, cómo quieras que el público interactúe y qué punto enfatices. La gran lección: hay varias alternativas a las tartas que pueden ser más eficaces.

## En resumen
El capítulo trata consideraciones y soluciones para retos comunes al comunicar visualmente con datos. Inevitablemente aparecerán retos no cubiertos; se aprende tanto del pensamiento crítico que resuelve cada escenario como de la "respuesta" en sí, pues rara vez hay un único camino correcto. Para más casos, la autora remite a su blog storytellingwithdata.com, con ejemplos de antes y después. Ante la duda, su estrategia habitual es pausar y considerar al público: qué necesitas que sepa o haga y qué historia quieres contar; si no surge un camino claro, prueba varias vistas y pide retroalimentación.

## Ideas clave
- El fondo blanco facilita centrarse en los datos; con fondo oscuro se invierte la lógica del contraste (el negro pasa a ser la línea base) y el color define el tono de la visualización.
- La animación permite que una misma diapositiva sirva para presentar en vivo (revelando el dato relevante en cada punto) y para circular (versión anotada), evitando el *slideument*.
- Debe haber lógica en el orden de los datos; con orden, color, posición y texto puedes dirigir la atención a distintas historias.
- Para contar varias historias, conserva un visual base con el mismo orden y resalta cada una con color, en lugar de reordenar y crear carga cognitiva.
- Respeta el orden intrínseco de las categorías ordinales y dirige la atención con otros recursos.
- Ante un gráfico espagueti: enfatiza una línea a la vez, separa espacialmente (vertical u horizontal), combina ambos o muestra menos datos.
- Hay varias alternativas a las tartas —número directo, barras simples, barras apiladas al 100% y slopegraph—, cada una con compromisos según parte-todo, orden y tipo de comparación.
- Rara vez hay una única solución correcta: pausa, piensa en tu público y en la historia, y prueba varias vistas.
