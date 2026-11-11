# Unsupervised Learning: Clustering and Dimensionality Reduction — Estudio

## Tarjetas de repaso

P: ¿Por qué se llama "no supervisado" el aprendizaje de este capítulo? / R: Porque, a diferencia de la clasificación y la regresión, no se conocen de antemano las "respuestas correctas".

P: ¿Cuáles son las dos vías principales para estudiar la estructura de un conjunto de datos? / R: El clustering (agrupar los puntos en clusters distintos) y la reducción de dimensionalidad (extraer la variabilidad real).

P: ¿Qué diferencia de motivación hay entre clustering y reducción de dimensionalidad? / R: El clustering suele hacerse para revelar la estructura de los datos; la reducción de dimensionalidad está motivada sobre todo por preocupaciones computacionales.

P: ¿Qué es la curse of dimensionality? / R: En espacios de muchas dimensiones todos los puntos quedan muy lejos y casi equidistantes entre sí, lo que degrada el rendimiento de los algoritmos.

P: ¿Qué hace PCA técnicamente con un vector d-dimensional? / R: Encuentra d componentes principales de longitud 1 y expresa cada punto como combinación lineal x = a1·p1 + … + ad·pd, ordenando las componentes por varianza decreciente.

P: ¿Qué forma geométrica asume PCA que tienen los datos? / R: Forma "de balón de fútbol americano": una mancha elipsoidal estirada en unos ejes y estrecha en otros, sin grandes outliers.

P: ¿Qué es un skree plot? / R: Una representación de la importancia de cada componente (la fracción de varianza del dataset que explica) para decidir cuántas dimensiones conservar.

P: ¿En qué se diferencian PCA y factor analysis? / R: Matemáticamente son lo mismo; PCA busca reducir dimensionalidad y el factor analysis busca identificar factores causales que generan los datos observados.

P: ¿Cuáles son las tres limitaciones principales de PCA? / R: Exige escalas (desviaciones estándar) comparables y es sensible a outliers; asume que los datos son lineales; y en caras requiere que las partes clave estén alineadas.

P: ¿Cuáles son los pasos del algoritmo clásico de k-means? / R: Empezar con k centros iniciales, asignar cada punto al centro más cercano, recalcular cada centro como la media de sus puntos y repetir hasta un criterio de parada.

P: ¿Qué aportan los GMM frente a k-means? / R: Capturan la "zona gris" y dan niveles de confianza; modelan cada cluster como una Gaussiana multivariante y no deciden definitivamente la pertenencia de cada punto.

P: ¿Cómo funciona el clustering aglomerativo y qué linkage menciona el capítulo? / R: Empieza con cada punto como su propio cluster y los fusiona hasta uno solo, dando una jerarquía; la linkage "ward" fusiona los dos clusters con menor varianza entre ellos.

P: ¿Cómo se calcula el silhouette score de un punto? / R: Con a = distancia media a su propio cluster y b = distancia media al cluster más cercano, el coeficiente es s = (b − a) / max(a, b), entre −1 y 1.

P: ¿Qué corrige el adjusted Rand index respecto al Rand index? / R: Que incluso agrupando al azar se aciertan pares por casualidad; lo escala para valer 0 de media con asignaciones aleatorias y 1 con coincidencia perfecta.

P: ¿Qué mide la mutual information en clustering? / R: Cuánto se puede acertar sobre el cluster real de un punto conociendo solo el cluster asignado (y viceversa); 0 si son independientes, la entropía si una se infiere perfectamente de la otra.

## Preguntas de autoevaluación

P: ¿Qué supone la reducción de dimensionalidad sobre la estructura "real" de los datos? / R: Que los campos son en gran medida redundantes y que los puntos, siendo d-dimensionales, viven realmente en un subconjunto k-dimensional (k < d) más algo de ruido. (Sección: Lo que necesitas saber)

P: En el ejemplo de las caras, ¿qué dimensionalidad tienen las imágenes y cómo mejoró PCA los resultados? / R: Son imágenes de 64×64 = 4096 dimensiones; reducir a 25 componentes hizo que los clusters casaran algo mejor con las personas (silhouette de 0.148 a 0.230 y Rand ajustado de 0.454 a 0.467). (Sección: El ejemplo que recorre el capítulo)

P: ¿Por qué es más difícil evaluar un clustering que PCA? / R: Porque no hay definición analítica de "buenos" clusters; la única métrica real es si reflejan una segmentación natural subyacente, difícil de evaluar. (Sección: Clustering)

P: ¿Qué comprobaciones de sentido común recomienda el autor cuando no hay ground truth? / R: Calcular estadísticas con features no usadas para agrupar, examinar a mano muestras de distintos clusters, proyectar con PCA a 2D en un scatterplot, graficar dos features relevantes, probar otro algoritmo y reagrupar sobre un subconjunto aleatorio. (Sección: Clustering)

P: ¿Qué ocurre en k-means si k es mayor que el número "real" de clusters? / R: k-means divide un cluster real en varios, convirtiéndose más en una forma de particionar el dataset en regiones "naturales". (Sección: k-means)

P: ¿Para qué tipo de clusters funciona mejor el silhouette score y cuándo falla? / R: Funciona mejor con clusters compactos, densos, bien separados y de tamaño comparable; falla, por ejemplo, con un donut con otra mancha en el centro, y puede penalizar a un punto correcto en un cluster muy grande y cercano a otro. (Sección: Evaluar la calidad de los clusters)

P: ¿Qué diferencia hay entre métodos de evaluación supervisados y no supervisados? / R: Los supervisados tienen ground truth y miden cuánto se ajustan los clusters hallados; los no supervisados miran lo geométricamente distintos que son los clusters. (Sección: Evaluar la calidad de los clusters)

P: ¿Qué algoritmo entrena a los mixture models y qué propiedad tiene? / R: El algoritmo EM, que es agnóstico a la distribución que se está modelando. (Sección: Gaussian mixture models)

## Puntos a dominar

- Distinguir aprendizaje no supervisado de clasificación/regresión y las dos vías: clustering y reducción de dimensionalidad, con sus motivaciones (estructura vs. cómputo).
- Explicar la curse of dimensionality y por qué comprimir a menos dimensiones suele ser prerequisito del análisis.
- Describir qué hace PCA (componentes principales ordenadas por varianza, combinación lineal) y cómo el skree plot ayuda a elegir el número de componentes.
- Diferenciar PCA de factor analysis (misma matemática, distinto objetivo) y recordar las tres limitaciones de PCA: escalas comparables/outliers, linealidad y alineación en imágenes.
- Conocer k-means, GMM y clustering aglomerativo: cómo funcionan, sus ventajas/defectos y cómo asignan (o no) puntos nuevos.
- Manejar las métricas de calidad: silhouette (no supervisada), Rand index y adjusted Rand index, y mutual information (supervisadas), y cuándo apoyarse en comprobaciones de sentido común.
