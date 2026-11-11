# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 3 — Form and Function (Forma y función)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo propone un marco para elegir el tipo de visualización según las necesidades de la audiencia. Su tesis es un lema: "Deja que las necesidades de tu audiencia guíen tus decisiones de visualización de datos" (PDF p. 68). Antes de pensar en color, disposición o tipografía, conviene preguntarse qué gráfico —estático o interactivo— sirve mejor al público, porque algunas audiencias quieren un informe largo, otras un resumen breve y otras solo los datos.

Para ordenar esa decisión, Schwabish presenta un esquema de dos ejes perpendiculares. El eje vertical es la FORM (forma) y va de estático a interactivo; el eje horizontal es la FUNCTION (función) y va de explicativo (explanatory) a exploratorio (exploratory). Toda visualización cae en algún punto de estos espectros, y su cruce genera cuatro cuadrantes.

Sales sabiendo clasificar visualizaciones en ese espacio forma-función, reconocer que los ejes son espectros (no cajas rígidas) y que no hay cuadrante "correcto": la elección depende de la reacción que buscas, de dónde publicas y de qué herramientas necesita tu audiencia. Además, el capítulo advierte que el crecimiento del móvil ha cambiado cómo interactuamos con los datos.

## Los dos ejes: forma y función

El libro se centra sobre todo en visualizaciones estáticas, pero reconoce que las interactivas y animadas son cada vez más comunes, con herramientas más fáciles, baratas y potentes año tras año. Las interactivas añaden decisiones de diseño propias: dónde va el botón, cómo se guía al usuario, si hay que hacer scroll y en qué dirección, o cómo cambia la interactividad entre un ordenador de escritorio y una tableta o teléfono.

En el eje de la FORM:
- Estáticas: dan toda la información a la vez y no se mueven (gráficos básicos de línea, barras, tarta).
- Interactivas: permiten transferir información entre el usuario y la interfaz; el usuario hace clic, desliza o pasa el cursor y algo ocurre o aparece información adicional.
- Animadas: se sitúan entre ambas (GIF animados, películas, presentaciones online); no siempre dejan manipular datos para crear resultados alternativos, pero sí controlar el ritmo o las transiciones.

En el eje de la FUNCTION:
- Explicativas: ponen los resultados en primer plano; transmiten la hipótesis o el argumento del autor al lector.
- Exploratorias: animan al usuario a explorar los datos o el tema para descubrir hallazgos por sí mismo.

## Los cuatro cuadrantes

Estático y explicativo. Gráficos que no son interactivos ni se mueven, usados para ilustrar un punto o reforzar un argumento del texto o la presentación (una línea o un gráfico de barras). Son también los que hacemos para explorar nuestros datos dentro de la organización. El libro se ocupa sobre todo de estos y los desarrolla en los capítulos 4 a 11.

Estático y exploratorio. Permiten que el lector interprete los datos y encuentre sus propios resultados en una presentación estática. El ejemplo es una infografía de la diseñadora Krisztina Szűcs: en cada gráfico, el eje vertical izquierdo muestra la puntuación de una película en Rotten Tomatoes y el derecho su rentabilidad (la diferencia entre ingresos brutos y presupuesto). No defiende un argumento concreto, sino que invita a explorar y sacar conclusiones propias.

Interactivo y explicativo. El caso más sencillo es un gráfico estático con una capa interactiva de hover o rollover encima. Muy popular hace unos años, parece perder favor a medida que los lectores migran a los smartphones y hacer clic o pasar el cursor pierde importancia. La interactividad puede atraer al lector para que viva una historia o entienda un proceso; ejemplo: el gráfico "Paths to the White House" del New York Times, que deja elegir los caminos por los que cada candidato presidencial podría ganar las elecciones.

Interactivo y exploratorio. Presentan gráficamente un conjunto completo de datos y piden al usuario que encuentre patrones o historias interesantes. Ejemplo: el proyecto Flight Patterns de Aaron Koblin, que muestra todos los vuelos en el espacio aéreo de EE. UU. en veinticuatro horas; vídeos e instantáneas (incluida su charla TED de 2011) permiten hacer zoom, pausar, rebobinar y explorar. A veces el fin es simplemente dar los datos para que la gente juegue o los use en su propio trabajo.

## Los ejes como espectros y la combinación de cuadrantes

Como los ejes son espectros, una visualización puede situarse en medio del espacio o combinar aspectos de varios cuadrantes. Medios como el Guardian, el New York Times o el Washington Post mezclan visualizaciones interactivas y estáticas con texto, clips de audio de entrevistas e imágenes, cosiéndolo todo en una experiencia visual que da más profundidad que el texto solo. Un ejemplo es "Bussed Out" del Guardian (2018), que con texto, entrevistas en vídeo y visualizaciones estáticas y animadas cuenta cómo los gobiernos de ciudades de EE. UU. trasladan en autobús a personas sin hogar fuera de sus ciudades.

Las animaciones son otra forma de mezclar cuadrantes. Citando el libro de Tamara Munzner, *Visualization Analysis and Design*, Schwabish distingue tres tipos de animación: narración de historias (películas), transiciones de un estado a otro, y reproducción de vídeo, donde el usuario controla la secuencia reproduciendo, pausando y rebobinando. Munzner señala que la animación es muy potente en las transiciones entre dos configuraciones de datos porque ayuda al usuario a mantener el contexto, de modo que el lector ve cómo uno o varios puntos de datos se mueven de una posición a otra.

Una manera sencilla de pensar las animaciones es el GIF animado: varias imágenes o fotogramas en un solo archivo. Funcionan como dibujos animados: un gráfico con una línea, luego el mismo con otra y otra, hasta construir un gráfico de cuatro líneas. Son especialmente eficaces en redes sociales porque rompen el flujo continuo de contenido. Durante los Juegos Olímpicos de verano de 2016, una serie de tuits del New York Times mostró (acelerados) eventos de natación para que los usuarios "vieran" una versión ilustrada —por ejemplo, cómo Katie Ledecky superó a sus rivales por amplio margen—, captando la atención en una plataforma tan rápida como Twitter. No hay cuadrante "correcto" o "incorrecto": depende de la reacción buscada, del lugar de publicación y de lo que la audiencia necesita para entender los datos.

## Cómo ha cambiado nuestra interacción con los datos

En 1997, Ben Shneiderman (profesor de ciencias de la computación en la Universidad de Maryland) formuló lo que sería un mantra de las visualizaciones interactivas en línea: "Overview first, zoom and filter, then details-on-demand" (PDF p. 76), es decir, primero una visión general, luego permitir zoom y filtrado, y después revelar los detalles bajo demanda (tooltips, descargas).

Con el auge del móvil, ese mantra es menos aplicable. Una década después, Archie Tse, subdirector de gráficos del New York Times, sostuvo que con el aumento de las plataformas móviles la gente solo quiere hacer scroll; si el lector tiene que hacer clic o algo más, "algo espectacular tiene que ocurrir". Schwabish lo comparte: al desplazarse por el móvil en el trayecto al trabajo, no quiere ordenar ni filtrar datos, quiere que el autor le muestre lo más importante, y más aún en trabajos técnicos o científicos.

Un proyecto de 2018 de Microsoft Research (Brehmer, Lee, Isenberg y Choe) probó con cien personas la rapidez y precisión al leer gráficos en el móvil usando datos de una app del tiempo y otra de sueño, con disposición de barras lineal frente a radial (tipo columnas circulares). Resultado: la gente era más lenta comprendiendo las disposiciones radiales, pero no menos precisa en sus inferencias. El uso del móvil solo crece: según Pew Research Center, en octubre de 2017 cerca de seis de cada diez adultos (58 %) obtenían sus noticias desde el móvil, frente al 39 % desde el ordenador personal. Tecnología, comportamiento y hábitos de noticias cambian constantemente.

## Empecemos

El resto del libro explora familias de gráficos según su función principal, y cada capítulo usa una guía de estilo distinta prestada de medios, organizaciones sin ánimo de lucro y otras entidades para mostrar la variedad de decisiones de diseño subjetivas; el capítulo 12 enseña a montar la propia guía de estilo. Schwabish insiste en preguntarse por la audiencia e incluso hablar con ella para saber qué quiere y necesita. Algunos quieren un informe PDF de treinta y cinco páginas, otros un resumen de dos páginas, otros un blog de ochocientas palabras, otros una experiencia narrativa inmersiva, y algunos solo los datos. Investigador, gestor, profesional, responsable político y periodista pueden necesitar cosas muy distintas, y conviene equilibrar la precisión del gráfico con su capacidad de atraer, desde la empatía con la audiencia; cita a Alan Alda: desarrollar empatía y reconocer lo que piensa el otro son esenciales para comunicar bien.

## Ideas clave

- El marco central son dos ejes: FORM (estático ↔ interactivo) y FUNCTION (explicativo ↔ exploratorio), cuyo cruce da cuatro cuadrantes.
- Explicativo transmite el argumento del autor; exploratorio invita al usuario a hallar sus propias conclusiones.
- El libro se centra en el cuadrante estático-explicativo (capítulos 4 a 11).
- Los ejes son espectros: las visualizaciones pueden situarse en medio o combinar cuadrantes (p. ej. "Bussed Out").
- La animación (narración, transiciones, reproducción) ayuda a mantener el contexto; los GIF animados funcionan como dibujos y brillan en redes sociales.
- El mantra de Shneiderman ("overview first, zoom and filter, then details-on-demand") pierde vigencia frente al móvil, donde domina el scroll.
- Microsoft Research halló que las disposiciones radiales se comprenden más despacio, pero sin pérdida de precisión.
- No hay cuadrante correcto: la elección depende de la audiencia, del medio de publicación y de lo que el público necesita.
