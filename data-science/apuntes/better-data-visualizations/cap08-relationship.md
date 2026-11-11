# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 8 — Relationship (Relación)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Al ser un capítulo muy visual, los gráficos se describen con palabras cuando es necesario.

## Lo que necesitas saber
Este capítulo reúne los gráficos que muestran relaciones y correlaciones entre dos o más variables. El más familiar es el scatterplot (gráfico de dispersión), pero hay muchos más: bubble plot, parallel coordinates plot, radar chart, chord diagram, arc chart, correlation matrix, network diagram y tree diagram. Cada uno usa formas distintas —puntos, líneas, arcos, círculos— para codificar cómo se asocian las variables u observaciones.

La tesis central es doble. Primero, que la visualización no solo comunica resultados sino que también es una herramienta de exploración: revela patrones y relaciones que las estadísticas resumen no muestran. Segundo, un recordatorio constante: "Correlation does not imply causation" (la correlación no implica causalidad); hay que distinguir entre asociación coincidente y relación causal.

Sales sabiendo cuándo conviene cada tipo de gráfico de relación, cómo leerlos, y qué compensaciones (claridad, orden, compacidad) implica cada uno. Como muchos son poco habituales, el autor insiste en preparar al lector con etiquetas, anotaciones, títulos activos y la estrategia de "empezar en gris" para reducir el desorden.

Para la paleta de colores y la tipografía (Bariol) el capítulo se inspira en el famoso bubble chart de Hans Rosling y su fundación Gapminder.

## Scatterplot
El scatterplot es la visualización más común para ilustrar correlaciones (o su ausencia) entre dos variables: una en el eje horizontal y otra en el vertical, con las observaciones en el espacio así creado. A diferencia del gráfico de barras, los ejes no necesitan empezar en cero, sobre todo si cero no es un valor posible.

Uno de los ejemplos más famosos es el conjunto de scatterplots animados de Rosling y Gapminder, mostrados en su charla TED de 2014, que relacionaban la tasa de fertilidad con la esperanza de vida al nacer de los países entre 1962 y 2003. Incluso gráficos lúdicos como el "Approval Matrix" semanal de New York Magazine son, en el fondo, scatterplots (con ejes "Highbrow-Lowbrow" y "Despicable-Brilliant").

Los ejemplos de datos del capítulo cruzan la inmigración neta (eje horizontal) con el PIB per cápita (eje vertical). Si ambas variables se mueven en la misma dirección, están **positivamente correlacionadas**; si van en sentidos opuestos, **negativamente correlacionadas**; si no hay patrón, no están correlacionadas. En el ejemplo, la inmigración neta es mayor donde el PIB per cápita es más alto (Europa Occidental y del Norte, Australia/Nueva Zelanda, Norteamérica).

Para hacer la correlación más clara se añade una **línea de mejor ajuste** (regression line o trendline), que muestra la dirección y magnitud de la relación. Aun así, el scatterplot no es trivial: una encuesta del Pew Research Center de 2016 mostró que solo un 60 % de las personas identificaban correctamente lo que veían en uno. Para marcar transparencia en puntos solapados se usa opacidad, y el color puede distinguir regiones del mundo.

## Correlación: definición y advertencias
La **correlación** mide la fuerza de la asociación lineal entre dos variables cuantitativas. La medida más común es el **coeficiente de correlación de Pearson**, denotado con la letra griega rho (ρ). Su valor va de −1 a 1: −1 es correlación perfectamente negativa, 1 perfectamente positiva y 0 ausencia de correlación lineal. El signo indica la dirección; el valor, la magnitud.

Existe también la **asociación no lineal**: patrones que se curvan o rompen la línea recta. Un ejemplo lineal es distancia = velocidad × tiempo (a velocidad constante); uno no lineal es el beneficio de un producto nuevo que sube, se estabiliza y cae con la competencia, reiniciando el ciclo.

Un punto atípico (outlier) basta para distorsionar la medida: mover un solo punto a la esquina superior izquierda puede reducir la correlación de 1.0 a 0.8. Por eso hay que mirar los datos visualmente durante el análisis. En 2016 el profesor Alberto Cairo creó el "Datasaurus": un conjunto de 142 puntos que dibujan un dinosaurio pero cuyas estadísticas resumen (media x de 54.26, media y de 47.83, Pearson de −0.06) parecen inocuas. En 2017 Justin Matejka y George Fitzmaurice generaron doce alternativas con idénticas estadísticas resumen. La lección —como la del cuarteto de Anscombe del Capítulo 1— es nunca fiarse solo de las estadísticas resumen, sino también de los visuales.

## Bubble plot
El scatterplot se convierte en **bubble plot** (o bubble scatterplot) al variar el tamaño de los círculos según una tercera variable. Los puntos no tienen que ser círculos, pero si lo son deben escalarse por **área, no por radio** (véase pág. 123), para no distorsionar la percepción. El color agrupa, destaca o dirige la atención.

En el ejemplo, los círculos se escalan por la población de cada región: se mantiene la relación positiva y además se ve el tamaño relativo de cada zona. Como es un gráfico poco común, conviene etiquetar los ejes y la dirección del cambio (p. ej. "Higher/Lower Net Immigration"), añadir una línea de 45 grados donde los valores son iguales, y resaltar puntos con color, contornos o texto.

Dos advertencias finales. Primera: evitar etiquetar todos los puntos, porque genera un desorden ilegible; si alguien quiere los valores exactos, se publica el archivo de datos o una versión interactiva (Tableau, Power BI). Segunda: a veces conviene normalizar, calcular el cambio porcentual o tomar el **logaritmo**. El log muestra valores relativos en vez de absolutos y "desinfla" distribuciones muy sesgadas: en escala log cada línea de cuadrícula representa un aumento de diez veces (1, 10, 100, 1000), convirtiendo una curva exponencial en una recta. El contrapeso es que los logs no son intuitivos (el PIB per cápita de Luxemburgo, 107 865 dólares, en log es 11.59). En un ejemplo con turistas de Nueva Zelanda (1921-2018) de Lisa Charlotte Rost, la escala log revela la caída durante la Segunda Guerra Mundial que la escala absoluta oculta. Transformar o no depende de la pregunta: ¿valores relativos o absolutos?

## Parallel coordinates plot
Cuando hay más de dos variables, el **parallel coordinates plot** las plotea en varios ejes verticales conectados por líneas; cada línea es una observación (p. ej. un país). Los ejes pueden tener unidades distintas o normalizarse (como porcentajes). Permite visualizar múltiples correlaciones en una sola vista. Simplificado a dos ejes se parece a un slope chart, pero mientras el slope chart muestra cambios en el tiempo (Capítulo 5), el parallel coordinates compara variables distintas: si los países altos en el eje izquierdo (educación) están altos en el derecho (empleo), las variables están correlacionadas positivamente.

El orden de los ejes determina qué correlaciones se ven: reordenarlos revela relaciones que antes estaban ocultas (p. ej. participación electoral y esperanza de vida). Poner todas las métricas en el mismo rango vertical suprime la varianza de algunas (la esperanza de vida varía poco, de 74.6 a 83.9 años; la migración neta mucho, de 8.6 % a 93.9 %). Dejar que cada eje fluctúe según su mínimo y máximo exige más etiquetado pero da mejor vista de los datos. El principal problema es el desorden: con muchas líneas y ejes cuesta hallar correlaciones. La solución es la estrategia "Start with Gray": pintar las líneas en gris y resaltar solo un subconjunto.

## Radar charts
Los **radar charts** (también spider o star charts) son como un parallel coordinates envuelto en un círculo: los ejes irradian desde el centro y las líneas o áreas los conectan. Son compactos y buenos para destacar outliers: la forma de Turquía se distingue de inmediato, algo más difícil en un gráfico de barras pareadas. Como el parallel coordinates, se complica al añadir líneas y requiere normalizar métricas de distinta escala. Una alternativa son los **small multiples**: un radar por país o grupo, que ocupa más espacio pero facilita comparar cada uno con el promedio general.

## Chord diagram
El **chord diagram** muestra asociaciones entre observaciones dispuestas en un círculo, ideal cuando comparten características. Las observaciones (nodos) se colocan en la circunferencia y se conectan con arcos internos; el grosor del arco (y a veces su color o transparencia) representa el grado de conexión. El ejemplo usa los flujos migratorios entre regiones del mundo en 2017, con más de 110 valores en un solo gráfico: más visual y compacto que una tabla enorme. Se ven los grandes flujos dentro de Asia y entre Centro y Norteamérica. Para evitar el desorden se resalta un grupo (p. ej. Asia en rojo, el resto en gris).

## Arc chart
Estira un chord diagram a lo largo de un eje horizontal y obtienes un **arc chart**: los nodos se alinean y se conectan con arcos cuya altura, grosor y color indican la fuerza de la relación. Una consideración clave —común a varios gráficos del capítulo— es que el **orden de los datos** cambia la percepción: mover Norteamérica al extremo derecho transforma por completo la vista. Conviene experimentar con color y posición de los nodos.

Una variante es el **arc-time** o **arc-connection chart**, donde los nodos denotan tiempo (alternativa a un timeline o flow chart). El de Adam McCann muestra la permanencia de todos los jueces de la Corte Suprema de EE. UU. desde 1804: el origen marca el inicio del mandato, el arco llega a la edad de retiro, la altura refleja la edad al nombramiento y el color el partido y el año. Otro arc chart del Guardian muestra, por distancia, a qué ciudades envía Nueva York a su población sin hogar.

## Correlation matrix
Una **correlation matrix** es una tabla con las variables en ambos ejes y, en cada celda, la fuerza de la relación (a menudo el coeficiente de Pearson). La versión gráfica sustituye los números por formas —normalmente círculos— y a veces color o sombras; es prima del heatmap y una forma de añadir un elemento visual a una tabla estándar (Capítulo 11).

El ejemplo relaciona inmigrantes y emigrantes por región en 2017. La tabla con números da todo el detalle pero cuesta navegarla y los valores importantes no destacan; el heatmap pierde detalle pero resalta las correlaciones positivas fuertes (sobre todo dentro de Asia). Se pueden combinar números y color, a riesgo de saturar. Con círculos, el tamaño cuesta de comparar porque percibimos mal las áreas. Un detalle: los valores de la diagonal valen por definición uno (migración de una región consigo misma), así que suelen omitirse para no dominar la vista.

## Network diagrams
Schwabish usa el término **diagram** (no graph o chart) porque parte del diseño responde a lo que luce mejor y no solo a los datos. Los **network diagrams** muestran jerarquías y conexiones dentro y entre grupos. Los puntos son **nodos** (o vértices) y las líneas **edges** (aristas); su posición, longitud y grosor indican la fuerza de la relación. Un árbol genealógico es un caso donde las líneas no se escalan por un valor.

Se distinguen cuatro tipos:
- **No dirigido y no ponderado**: amistades (conectados o no).
- **No dirigido y ponderado**: investigadores que coescriben; el grosor es el número de artículos juntos.
- **Dirigido y no ponderado**: seguidores en Twitter (con dirección, sin peso).
- **Dirigido y ponderado**: migración entre países; el grosor es el número de personas y la dirección, el destino.

Existen varios algoritmos de disposición (Fruchterman–Reingold, Sphere, Circle, Random) que buscan minimizar cruces de aristas y solapamientos y repartir los nodos uniformemente. A veces el objetivo es mostrar la aglomeración densa: los 32 small multiples de Clio Andris et al. (2015) dibujan la polarización del voto en la Cámara de Representantes de EE. UU. de 1949 a 2011 (rojos republicanos, azules demócratas; líneas = votos coincidentes), dejando claro que en 2011 los partidos votaban juntos mucho menos. Un simple line chart lo informa igual, pero no impacta como los small multiples. Para redes muy densas ("hairballs") existe el **hive plot** de Martin Krzywinski, que organiza los nodos en ejes radiales según la estructura de la red, no la estética.

## Tree diagrams
Los **tree diagrams** muestran niveles de una jerarquía, como un organigrama. Los nodos se ramifican desde un nodo inicial (el **root**, padre de todos) mediante líneas llamadas links o ramas; los nodos sin hijos son **leaf nodes**. El diseño importa porque a menudo hay pocos o ningún dato: un organigrama solo con nombres sirve para una reunión formal, mientras que uno con iconos encaja en marketing. Los árboles pueden ramificar hacia abajo, arriba u horizontalmente.

Un tipo especial es el **word tree** (Martin Wattenberg y Fernanda Viégas, 2007), representación visual del texto de un libro o pasaje (Capítulo 10): una palabra a izquierda o derecha se ramifica en los contextos donde aparece, con los nodos dimensionados por frecuencia. Los árboles pueden mostrar datos complejos (el genoma humano) o simples (regiones divididas en países); la elección depende del propósito y la audiencia.

## Ideas clave
- Los gráficos de relación codifican asociaciones entre dos o más variables: scatterplot, bubble plot, parallel coordinates, radar, chord, arc, correlation matrix, network y tree.
- Correlación no implica causalidad; el coeficiente de Pearson (ρ) va de −1 a 1 e indica dirección y magnitud de la asociación lineal.
- Hay que visualizar los datos, no fiarse solo de las estadísticas resumen: el "Datasaurus" y el cuarteto de Anscombe lo demuestran.
- El bubble plot añade una tercera variable escalando círculos por área (no radio); el log ayuda con datos sesgados o muy agrupados.
- En parallel coordinates, radar y arc charts el orden y la escala de los ejes cambian lo que se percibe.
- La estrategia "Start with Gray" reduce el desorden en gráficos densos resaltando solo un subconjunto.
- Las network diagrams se clasifican por ser dirigidas/no dirigidas y ponderadas/no ponderadas, y a veces buscan mostrar la aglomeración (polarización del Congreso de EE. UU.).
- Como muchos son gráficos poco habituales, hay que guiar al lector con etiquetas, anotaciones y títulos activos en lugar de simplificar los datos.
