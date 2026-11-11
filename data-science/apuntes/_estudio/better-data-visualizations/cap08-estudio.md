# Relationship (Relación) — Estudio

## Tarjetas de repaso

P: ¿Qué codifican los gráficos de relación? / R: Asociaciones y correlaciones entre dos o más variables u observaciones; incluyen scatterplot, bubble plot, parallel coordinates, radar, chord, arc, correlation matrix, network y tree.

P: ¿Cuál es la visualización más común para ilustrar correlación entre dos variables? / R: El scatterplot, con una variable en el eje horizontal y otra en el vertical y las observaciones en el espacio así creado.

P: ¿Los ejes de un scatterplot deben empezar en cero? / R: No necesariamente, a diferencia del gráfico de barras, sobre todo si cero no es un valor posible.

P: ¿Qué significan correlación positiva y negativa? / R: Positiva, cuando ambas variables se mueven en la misma dirección; negativa, cuando van en sentidos opuestos; si no hay patrón, no están correlacionadas.

P: ¿Qué mide el coeficiente de correlación de Pearson (ρ) y en qué rango? / R: La fuerza de la asociación lineal entre dos variables cuantitativas; va de −1 (negativa perfecta) a 1 (positiva perfecta), con 0 = ausencia de correlación lineal.

P: ¿Qué ilustran el "Datasaurus" y el cuarteto de Anscombe? / R: Que no hay que fiarse solo de las estadísticas resumen; conjuntos con idénticas medias y correlación pueden dibujar figuras muy distintas al visualizarse.

P: ¿Cómo se convierte un scatterplot en bubble plot y cómo deben escalarse los círculos? / R: Variando el tamaño de los círculos según una tercera variable; deben escalarse por área, no por radio, para no distorsionar la percepción.

P: ¿Qué aporta aplicar el logaritmo a los datos? / R: Muestra valores relativos en vez de absolutos y "desinfla" distribuciones muy sesgadas; cada línea de cuadrícula representa un aumento de diez veces, convirtiendo una curva exponencial en recta.

P: ¿Qué muestra un parallel coordinates plot y qué representa cada línea? / R: Más de dos variables en varios ejes verticales conectados por líneas; cada línea es una observación (p. ej. un país).

P: ¿Qué es un radar chart y para qué es bueno? / R: Un parallel coordinates envuelto en un círculo con ejes que irradian desde el centro; es compacto y bueno para destacar outliers.

P: ¿Qué representa un chord diagram? / R: Asociaciones entre observaciones dispuestas en un círculo y conectadas por arcos internos, cuyo grosor representa el grado de conexión.

P: ¿Qué es un arc chart y qué consideración clave comparte con otros gráficos del capítulo? / R: Un chord diagram estirado sobre un eje horizontal con nodos alineados y arcos; el orden de los datos cambia por completo la percepción.

P: ¿Qué es una correlation matrix? / R: Una tabla con las variables en ambos ejes y, en cada celda, la fuerza de la relación (a menudo el Pearson); su versión gráfica usa formas como círculos y color.

P: ¿Cómo se clasifican las network diagrams? / R: Por ser dirigidas o no dirigidas y ponderadas o no ponderadas; sus puntos son nodos (vértices) y sus líneas edges (aristas).

P: ¿Qué es un tree diagram y qué son el root y los leaf nodes? / R: Un gráfico que muestra niveles de una jerarquía; el root es el nodo inicial (padre de todos) y los leaf nodes son los nodos sin hijos.

## Preguntas de autoevaluación

P: ¿Por qué el autor insiste en "Correlation does not imply causation"? / R: Porque hay que distinguir entre asociación coincidente y relación causal; la visualización muestra asociación, no necesariamente causa. (Sección "Lo que necesitas saber")

P: ¿Cómo afecta un solo outlier a la medida de correlación y qué conclusión se extrae? / R: Mover un único punto a la esquina superior izquierda puede reducir la correlación de 1.0 a 0.8; por eso hay que mirar los datos visualmente y no solo las estadísticas resumen. (Sección "Correlación: definición y advertencias")

P: En parallel coordinates, ¿por qué importa el orden y la escala de los ejes? / R: El orden determina qué correlaciones se ven y reordenarlos revela relaciones ocultas; poner todas las métricas en el mismo rango suprime la varianza de algunas, mientras dejar que cada eje fluctúe da mejor vista pero exige más etiquetado. (Sección "Parallel coordinates plot")

P: ¿En qué se diferencia un parallel coordinates de dos ejes de un slope chart? / R: El slope chart muestra cambios en el tiempo, mientras el parallel coordinates compara variables distintas (p. ej. educación frente a empleo). (Sección "Parallel coordinates plot")

P: ¿Cuál es el principal problema de los gráficos densos del capítulo y qué estrategia lo resuelve? / R: El desorder con muchas líneas y ejes dificulta hallar correlaciones; la estrategia "Start with Gray" pinta todo en gris y resalta solo un subconjunto. (Secciones "Parallel coordinates plot" y "Chord diagram")

P: ¿Por qué suelen omitirse los valores de la diagonal en una correlation matrix? / R: Porque valen por definición uno (la relación de una región consigo misma) y dominarían la vista. (Sección "Correlation matrix")

P: ¿Por qué Schwabish usa el término "diagram" en los network diagrams? / R: Porque parte del diseño responde a lo que luce mejor y no solo a los datos. (Sección "Network diagrams")

P: ¿Qué transmiten los 32 small multiples de Clio Andris et al. sobre el Congreso de EE. UU.? / R: La polarización del voto en la Cámara de Representantes de 1949 a 2011, dejando claro que en 2011 los partidos votaban juntos mucho menos; un line chart lo informa igual pero no impacta como los small multiples. (Sección "Network diagrams")

## Checklist

- [ ] Elegir el gráfico de relación según el número de variables y el tipo de asociación (scatterplot para dos, bubble para tres, parallel/radar para más, chord/arc/network para conexiones entre observaciones).
- [ ] En un scatterplot, no forzar los ejes a empezar en cero si cero no es posible y añadir una línea de mejor ajuste (regression line) para clarificar la relación.
- [ ] Usar opacidad en puntos solapados y color para distinguir grupos o regiones.
- [ ] Escalar las burbujas por área y no por radio.
- [ ] Evaluar si conviene normalizar, calcular cambio porcentual o aplicar logaritmo según si la pregunta busca valores relativos o absolutos.
- [ ] Visualizar siempre los datos durante el análisis, no fiarse solo de las estadísticas resumen.
- [ ] Experimentar con el orden y la escala de los ejes en parallel coordinates, radar y arc charts, pues cambian lo percibido.
- [ ] Aplicar "Start with Gray" en gráficos densos: pintar en gris y resaltar solo el subconjunto relevante.
- [ ] Evitar etiquetar todos los puntos; si se necesitan valores exactos, publicar el archivo de datos o una versión interactiva (Tableau, Power BI).
- [ ] Guiar al lector de gráficos poco habituales con etiquetas de ejes, dirección del cambio, anotaciones y títulos activos.
