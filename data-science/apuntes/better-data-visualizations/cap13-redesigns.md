# Better Data Visualizations — Jonathan Schwabish (Columbia University Press, 2021)
## Capítulo 13 — Redesigns (Rediseños)

> Nota de extracción: texto extraído de la capa de texto del PDF; las citas referencian la página del PDF. Es un capítulo muy visual, así que los gráficos se describen con palabras.

## Lo que necesitas saber
El capítulo reúne una serie de rediseños de gráficos reales para mostrar cómo aplicar en la práctica todas las lecciones del libro. Schwabish aclara que no busca criticar a quienes crearon los gráficos originales: muchos no son malos, simplemente admiten formas más eficaces de representar los datos. La tesis es que no hay un enfoque "correcto" o "incorrecto", solo distintas maneras de mejorar, y que con la práctica cada quien desarrolla su propia estética visual.

Cada rediseño sigue las pautas tratadas a lo largo del libro: mostrar los datos, reducir el desorden (clutter), integrar texto y gráfico, usar más de un gráfico cuando haga falta y empezar con gris. El hilo conductor es un método: identificar el objetivo central del gráfico y los retos de los datos para elegir el tipo de representación adecuado.

Al terminar, sales sabiendo cómo diagnosticar por qué un gráfico falla (demasiada tinta, líneas base distintas, datos cortados, estructura que no coincide con el texto) y qué alternativas aplicar: pasar de barras a líneas, separar barras apiladas en small multiples, limpiar gráficos recargados, convertir mapas en diagramas de dispersión o usar heatmaps.

## Gráfico de barras pareadas: superficie de cultivos (USDA)
Un gráfico del Departamento de Agricultura de EE. UU. muestra las hectáreas cosechadas de cinco cultivos en seis años. Lo primero que se ve es que la superficie creció en todos; lo segundo, que el algodón cayó el último año. Pero esa caída no resalta porque hay demasiada tinta y color.

Si el objetivo es mostrar tendencias relativas, el gráfico de barras es mala elección: las barras pareadas son buenas para valores exactos, pero las tendencias relativas no se ven con claridad. El rediseño como gráfico de líneas simple hace evidente la caída del algodón y los tamaños relativos de los cinco cultivos (por ejemplo, que el arroz queda justo en medio). En vez de leyenda, Schwabish etiqueta el final de cada línea y usa color para vincular etiqueta y línea.

Una segunda opción es un cycle chart: en esencia un small multiples de líneas donde cada cultivo tiene su propio panel. Da más espacio y resulta más atractivo por ser distinto, pero los patrones relativos se perciben algo menos claros que en el gráfico de líneas único.

## Gráfico de barras apiladas: prestación de servicios
El ejemplo retoma el diagrama de rankings perceptuales del capítulo 1. Arriba están los gráficos que comparten una escala común (barra o línea con un único eje); un escalón por debajo, los que no comparten escala y son más difíciles de evaluar. La barra apilada mezcla ambos casos: la serie que descansa sobre la línea base común (Functional assignment) se compara bien, pero las demás no, porque no comparten base. Prueba: ¿el valor de Political Institutions es mayor para "All Countries" o para Zambia? Cuesta decirlo.

La solución es dividir el gráfico en cinco gráficos separados, uno por serie, de modo que cada serie tenga su propia línea base vertical y las comparaciones entre países dentro de cada serie sean más fáciles. Lo crucial es que el espacio horizontal de cada serie sea idéntico: si se encogiera el de "Fiscal Institutions", sus valores parecerían mayores. Este enfoque no dice mucho sobre los totales entre países; se puede añadir una serie de Total con el mismo espaciado horizontal (misma separación entre líneas de cuadrícula). Funciona aún mejor cuando los valores suman lo mismo o 100 %, porque entonces la longitud total es igual para todas las barras y el segmento Total resulta innecesario.

## Gráfico de líneas: los Trustees de la Seguridad Social
Cada año, la Junta de Trustees informa sobre el estado actual y proyectado del programa de Seguridad Social de EE. UU. El Technical Panel, un panel experto independiente, revisa su trabajo. El panel de 2019 enfocó la comunicación: cree que la confianza en las instituciones públicas se refuerza con mayor comprensión, y pide lenguaje claro, foco en el mensaje central y mejores visualizaciones.

### Una limpieza
El primer caso es más limpieza que rediseño. El gráfico de líneas —presente en casi todos los informes— muestra ingresos del sistema (impuestos) frente a costos (prestaciones) en un período histórico corto (2000–2018) y en la proyección larga (2018–2092). Se muestran dos costos: las prestaciones programadas (línea discontinua) y las realmente pagables (línea sólida gruesa). El gráfico tiene anotaciones útiles, pero gasta mucha tinta en detalles superfluos: cuadrículas horizontales y verticales y marcas de cada punto porcentual y cada año.

El rediseño elimina las cuadrículas verticales y todas las marcas, borra la tablita inferior y etiqueta directamente los años referenciados. Añade algo de color (consistente con impresión en blanco y negro) y un recuadro gris sobre el período de proyección (tras 2018) para destacar el desequilibrio.

### Un mejor diagrama de puntos
El segundo gráfico, del informe del Technical Panel de 2011, muestra la sensibilidad de distintos supuestos del modelo. Casi todos los informes presentan esto como tablas, pero en 2011 se usó algo parecido a un dot plot o un box-and-whisker simplificado: una estimación "intermedia" en el centro y opciones de "bajo costo" y "alto costo" a cada lado. El original tiene formas variadas, cuadrículas vertical y horizontal y etiquetas de eje rotadas. Aplicando las pautas del capítulo 2, el rediseño rota toda la visualización para no tener que ladear la cabeza y lleva lo que estaba en el eje vertical al horizontal. En vez de puntos, usa cajas: un extremo codifica el valor bajo, el otro el alto y un marcador central el intermedio, reduciendo líneas y puntos extra. Las etiquetas de cada métrica van junto al primer grupo de cajas.

## Mapa coroplético: esclavitud en Alabama y elecciones al Senado
En 2017 hubo una segunda vuelta por un escaño del Senado en Alabama. La periodista Sarah Slobin (entonces en Quartz) escribió sobre la relación entre el voto y la distribución de personas esclavizadas en 1860. Advirtió que correlación no es causalidad, pero que hay un paralelismo visual sorprendente. Los datos de voto muestran una banda horizontal azul oscuro (más voto demócrata); un mapa de 1860 del Census Bureau muestra una franja de colores oscuros en los condados con mayor proporción de población esclavizada: el "black belt" que cruza ambos mapas.

Aunque es visualmente impactante, el emparejamiento obliga al lector a saltar entre dos mapas. El voto demócrata en los 67 condados fue de 16,1 % a 88,1 %, y se superpone aproximadamente con 51 condados identificables en el mapa censal (de 3,1 % a 78,3 %). Representar ambas variables en un diagrama de dispersión deja ver mejor la relación positiva: los doce condados del corredor este-oeste aparecen como círculos (más oscuros) arriba a la derecha. Para una noticia, los mapas quizá sean lo mejor; para una revista académica revisada por pares, Schwabish prefiere el scatterplot porque muestra la asociación con claridad. También cabe publicar ambos: los mapas atraen, el scatterplot da el detalle.

## Diagrama de puntos: Programa Nacional de Almuerzo Escolar
Un gráfico del NAEP/NCES muestra diferencias de puntajes entre estudiantes negros y blancos, ordenadas por el puntaje de los estudiantes negros. En las barras de la izquierda hay tres números —28 %, 32 % y 60 %—: los recuadros verdes marcan los puntajes de blancos (60 %) y negros (28 %), y el número central la brecha (32 %). Pero los recuadros verdes hacen parecer que el 28 % es un rango (p. ej. de 22 % a 28 %): al usar rectángulos en vez de puntos, se parece a un gráfico apilado y no al dot plot que se pretendía. El rediseño lo convierte en un dot plot vertical real: círculos verdes conectados por una línea gris vertical, que se perciben como puntos concretos. Además se elimina la leyenda y se etiquetan las tres series directamente en el gráfico izquierdo; no se repite en el derecho porque hay menos espacio y el lector ya no necesita recordar cada definición.

## Diagrama de puntos: crecimiento del PIB en EE. UU.
Cada trimestre, la Bureau of Economic Analysis (BEA) publica cambios del PIB. El gráfico del tercer trimestre de 2014 muestra el "Real Value Added" (contribución de cada industria al PIB) por industrias. Se podrían etiquetar las barras directamente, rotar la leyenda del eje vertical y aclarar las cuadrículas. Pero lo más importante es que la estructura del gráfico no coincide con el texto: las seis viñetas que lo rodean describen cómo cambió el RVA entre el primer y el último período para cada industria, mientras que el gráfico compara industrias dentro de cada período.

Un mejor enfoque muestra el inverso: el cambio dentro de cada industria entre períodos. Dos opciones eficaces: un gráfico de barras pareadas (ordenado por el período más reciente, 2014:Q3, para guiar hacia las industrias con mejor desempeño) y un dot plot (ordenado por el cambio entre los dos períodos, con los mayores aumentos arriba y las caídas abajo). Moraleja: las visualizaciones no están para romper bloques de texto ni dar un "respiro visual", sino para apoyar el argumento e integrarse con la escritura.

## Gráfico de líneas: endeudamiento neto del Gobierno
Schwabish es fan de los gráficos de líneas, pero critica uno de un Economic Policy Paper de 2012 del Federal Reserve Bank of Minneapolis. Problemas: el título partido en tres ("Figure 2", "Net government borrowing", "percent GDP"), cuadrículas de peso uniforme aunque el cero no esté abajo, mezcla de colores pastel y vivos, y sobre todo la línea de Irlanda que se sale por arriba del gráfico. Hay que tener muy buena razón para no mostrar todos los datos, y poner el valor en una nota al pie no cuenta.

El creador enfrentaba un problema real: el pico de deuda de Irlanda en 2011 superaba con mucho a los demás países, y mostrarlo todo aplastaría el detalle. La mejor solución son dos gráficos: uno que incluya Irlanda con eje de −10 % a 35 %, y otro de −4 % a 18 % con el detalle de los demás, en un esquema zoom-out/zoom-in. El subtítulo explica cuál incluye Irlanda y cuál no. No hay que temer usar más de un gráfico: somos una sociedad digital y el espacio extra solo cuesta memoria, no papel.

## Tabla: participación de las empresas
Como en el capítulo 11, las tablas pueden hacerse más visuales con color, iconos o barras. Una tabla de Chappell y Jaffe (2018) usa formas y tonos de gris distintos para la proporción de empresas que realizan actividades como diseño o investigación de mercado, lo que obliga al lector a descifrar qué forma corresponde a qué porcentaje; además, los triángulos no significan "más" que los círculos, así que el orden de los valores es difícil de interpretar. La alternativa es un heatmap con una rampa monocromática (azul claro para valores bajos, azul oscuro para altos): así se ve enseguida que hay mucho tiempo dedicado a Employee training. Ordenar los datos enfoca aún más la atención; las etiquetas largas requieren rotarlas o rotar todo el gráfico y ajustar el tamaño de celda.

## Conclusión del capítulo
Con más gráficos en la caja de herramientas, el lector está listo para mejorar los suyos; buscar y rediseñar incluso el gráfico más simple —la literatura académica revisada por pares es buen punto de partida— afina la destreza y la estética propia. Dos advertencias: primero, si se critica un gráfico en público, recordar que alguien lo hizo bajo presiones de tiempo, limitaciones de software o exigencias organizativas; contactar al autor puede valer la pena. Segundo, identificar el objetivo central del gráfico y los retos de la serie de datos, lo que conduce al mejor tipo de gráfico para la tarea.

## Ideas clave
- No hay gráficos "correctos" o "incorrectos": el rediseño aplica pautas (mostrar datos, reducir clutter, integrar texto y gráfico, usar más gráficos, empezar con gris) para ganar claridad.
- Las barras pareadas sirven para valores exactos; para tendencias relativas conviene un gráfico de líneas o un cycle chart (small multiples).
- Las barras apiladas dificultan comparar series que no comparten línea base; separarlas en small multiples con igual espacio horizontal lo resuelve.
- Limpiar un gráfico (quitar cuadrículas y marcas, etiquetar directamente, usar color con moderación) puede bastar sin rediseñarlo por completo.
- Rotar el gráfico y convertir puntos en cajas facilita la lectura de etiquetas y codifica bajo/intermedio/alto sin líneas extra.
- Un scatterplot puede sustituir a dos mapas coropléticos para mostrar una asociación de forma más rigurosa, aunque exija más explicación.
- Usar rectángulos en lugar de puntos convierte un dot plot en algo que parece apilado; los círculos restauran la lectura de valores puntuales.
- La estructura del gráfico debe coincidir con el mensaje del texto; nunca cortes datos (como la línea de Irlanda): usa dos gráficos si hace falta.
