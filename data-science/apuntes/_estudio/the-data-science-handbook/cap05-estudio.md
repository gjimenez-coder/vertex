# Visualizations and Simple Metrics (Visualizaciones y métricas simples) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre el papel de las visualizaciones? / R: "Si no hay una imagen, lo estás haciendo mal": un proyecto empieza con visualizaciones exploratorias para formular hipótesis y termina con figuras que hacen obvios los resultados; el objetivo es transmitir la información como la entiende el cerebro humano.

P: ¿Por qué a veces sigue haciendo falta un número y no solo una imagen? / R: Porque los ojos nos engañan y conviene una estadística fría, y porque los ordenadores necesitan cifras para automatizar decisiones (aunque solo sea elegir qué imágenes merecen atención).

P: ¿Qué es el dataset Iris que recorre el capítulo? / R: 150 especímenes de flor, 50 de cada una de tres especies, con longitud y anchura de pétalos y sépalos; viene en scikit-learn y se carga en un DataFrame con una columna `species`.

P: ¿Qué papel juega matplotlib en la pila de Python según Cady? / R: Es la herramienta principal y estándar, potente y bien integrada, pero el eslabón más débil: gráficos caricaturescos, sintaxis poco intuitiva y mala interactividad, casi todo arreglable ajustando los malos valores por defecto.

P: ¿Por qué defiende Cady el pie chart pese a ser "simple"? / R: Porque interpretar una lista de números exige esfuerzo cognitivo, mientras que los circuitos neuronales de bajo nivel entienden un pie chart al instante; ilustra el principio de que importa cómo se transmite la información.

P: ¿Por qué es el histograma la visualización favorita del autor? / R: Porque casi siempre contiene algo interesante (bultos que pueden ser clases reales, outliers, variación de la población) y funciona con un solo campo numérico, a diferencia del scatterplot.

P: ¿Cuáles son los dos grandes problemas de los histogramas? / R: El número y tamaño de los bins (grandes ocultan patrones, pequeños dejan cubos vacíos) y que los datos pueden estropear la imagen cuando un cubo con muchísimos puntos aplasta a los demás.

P: ¿Qué diferencia hay entre resumir con media/desviación y con mediana/cuantiles? / R: Media y desviación son históricamente populares y fáciles de calcular pero frágiles ante outliers; mediana y percentiles 25/75 son robustos pero más costosos porque exigen ordenar. Ambas opciones asumen una distribución acampanada.

P: ¿Cuándo usa Cady la mediana y cuándo la media? / R: La mediana para lo "típico" (la mitad de valores por encima y la mitad por debajo) y la media cuando lo que importa de negocio es el comportamiento promedio.

P: ¿Qué ventaja tiene el boxplot frente al histograma con outliers? / R: Muestra mediana, cuantiles y min/máx, y los outliers grandes se ven de inmediato: donde el cuantil superior queda mucho más lejos de la mediana, un histograma solo mostraría un leve engrosamiento de las colas.

P: ¿Para qué sirven los ejes logarítmicos en un scatterplot y qué limitación tienen? / R: Rescatan datos positivos que varían en órdenes de magnitud y se aplastarían a un lado (`logx=True`/`logy=True`); solo funcionan con valores mayores que 0 (con 0 se suele sumar 1, con negativos no sirven).

P: ¿Qué diferencia a la correlación de Pearson de las ordinales (Spearman y Kendall)? / R: Pearson mide cuán buena aproximación es Y = mX + b (asume linealidad); Spearman y Kendall solo asumen relación monótona. Si debe elegir, Cady usa Spearman; Kendall es más robusta pero muy sensible a pequeños cambios de orden.

P: ¿Qué regla práctica propone Cady sobre correlación y causalidad? / R: "Si A y B están correlacionadas, ninguna causa a la otra; hay un factor C que causa ambas" (PDF p. 89); es un buen generador de hipótesis, aunque a veces sí hay causalidad e inferirla exige conocimiento del dominio.

P: ¿Qué demuestra el cuarteto de Anscombe? / R: Que las métricas resumen pueden enmascarar rasgos importantes: sus cuatro conjuntos tienen idénticos media, desviación, correlación y recta de ajuste, pero relaciones muy distintas.

P: ¿Por qué la visualización es insustituible en series temporales? / R: Porque no existe una "suposición por defecto" que funcione como la campana, así que siempre hay que mirar los datos para saber qué es normal.

## Preguntas de autoevaluación

P: ¿Cómo se reparte un proyecto analítico típico entre visualización y procesamiento numérico, según el capítulo? / R: Empieza con visualizaciones exploratorias y termina con figuras cuidadas; el verdadero procesamiento numérico queda escondido en medio, a veces casi como un detalle secundario, y en varios proyectos nunca hubo machine learning. (Sección: Lo que necesitas saber)

P: ¿Cómo se relacionan las visualizaciones de Pandas con matplotlib? / R: Son un envoltorio sobre matplotlib: normalmente se genera la imagen con el método `plot()` del objeto Pandas y luego se usa `pyplot` para título, mostrar o guardar el archivo. (Sección: Herramientas de visualización en Python)

P: En el dataset Iris, ¿qué revela el histograma de `petal length` y cómo se confirma? / R: Muestra una distribución bimodal; al dibujar cada especie por separado (con `alpha` y `label`) se confirma que el pico de la izquierda corresponde solo a la especie setosa. (Sección: Histogramas)

P: ¿Cómo se añaden dimensiones extra a un scatterplot y con qué argumentos? / R: Con color coding (`c`), tamaño en píxeles (`s`), tipo de marcador (`marker`) y opacidad (`alpha`, útil cuando los puntos se solapan). (Sección: Scatterplots)

P: ¿Qué soluciones ofrece el capítulo para el amontonamiento de puntos y para visualizar más de tres dimensiones? / R: La scatter matrix (un scatterplot por cada par de variables, con histogramas en la diagonal) para las dimensiones, y reducir tamaño, usar `alpha` o un heatmap de densidad (`kind='hexbin'`) cuando importa la densidad y no los puntos concretos. (Sección: Scatter matrices y heatmaps)

P: ¿Qué umbrales de correlación usa Cady como referencia de "fuerte"? / R: Le empieza a importar por encima de 0.4; hacia 0.7 se puede estimar de forma defendible una variable con la otra; por encima de 0.95 una variable es casi sinónimo de la otra y probablemente hay algo raro en la data. (Sección: Correlaciones)

P: ¿Qué recomendaciones da el autor para trabajar con series temporales? / R: Poder hacer zoom, usar escala logarítmica cuando importan los cambios proporcionales, graficar muchas series juntas (normalizadas) o mostrar mediana y cuantiles, y considerar transformaciones al dominio de la frecuencia (Fourier) si se espera periodicidad; la visualización suele servir para extraer features. (Sección: Series temporales)

P: ¿Por qué filtrar outliers antes de calcular la media puede ser un error? / R: Porque vale si los outliers son patológicos (fallo de un sensor), pero no si son datos clave (importes de transacciones), donde descartarlos elimina señal significativa. (Sección: Medias, desviaciones estándar, medianas y cuantiles)

## Puntos a dominar

- Elegir la visualización según la pregunta: pie/bar para proporciones y resultados binarios; histograma para una variable (bimodalidad, outliers); scatterplot para relaciones entre dos variables.
- Reconocer cuándo la media y la desviación estándar son engañosas por outliers y cuándo preferir mediana y cuantiles.
- Saber que los boxplots delatan outliers que un histograma disimularía, mostrando mediana, cuantiles y extremos.
- Aplicar ejes logarítmicos solo a datos positivos que varían en órdenes de magnitud.
- Distinguir Pearson (linealidad) de Spearman/Kendall (monotonicidad) y recordar que ninguna correlación capta relaciones no monótonas.
- Interiorizar "correlación no es causalidad" y buscar el factor C común como generador de hipótesis.
- Recordar el cuarteto de Anscombe como prueba de que los números resumen pueden engañar.
- Tratar las series temporales graficando siempre, al no haber una suposición por defecto como la campana.
