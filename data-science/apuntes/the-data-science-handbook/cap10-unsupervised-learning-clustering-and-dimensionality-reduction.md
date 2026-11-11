# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 10 — Unsupervised Learning: Clustering and Dimensionality Reduction (Aprendizaje no supervisado: clustering y reducción de dimensionalidad)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Se conservan solo los fragmentos de código esenciales.

## Lo que necesitas saber

Este capítulo trata técnicas para estudiar la estructura latente de los datos cuando no sabemos de antemano qué forma debería tener. Se llaman de aprendizaje "no supervisado" porque, a diferencia de la clasificación y la regresión, no se conocen las "respuestas correctas" de partida. Hay dos vías principales para estudiar la estructura de un conjunto de datos: el clustering y la reducción de dimensionalidad.

El clustering intenta agrupar los puntos en "clusters" distintos, con la esperanza de que cada grupo corresponda a un fenómeno subyacente distinto (el ejemplo clásico: altura y peso de personas forman dos manchas, hombres y mujeres). La reducción de dimensionalidad no busca categorías: parte de la idea de que los campos son en gran medida redundantes y quiere extraer la variabilidad real de los datos. Los datos son d-dimensionales, pero los puntos viven realmente en un subconjunto k-dimensional (con k < d) más algo de ruido.

Una diferencia práctica clave: el clustering suele hacerse para revelar la estructura de los datos, mientras que la reducción de dimensionalidad está motivada sobre todo por preocupaciones computacionales. Con sonido, imagen o vídeo, d puede llegar a decenas de miles, y aparece la "curse of dimensionality". Al terminar sabrás qué es PCA y cómo usarlo, los principales algoritmos de clustering (k-means, GMM, aglomerativo) y cómo evaluar la calidad de los clusters.

## El ejemplo que recorre el capítulo

El hilo conductor es un conjunto de imágenes de caras de 64×64 píxeles (10 fotos de cada una de 40 personas), lo que da d = 64·64 = 4096 dimensiones. El script carga las imágenes, las agrupa con k-means y mide: la "bondad" de los clusters con el silhouette score y su correspondencia con las personas reales con el adjusted Rand index. Luego aplica PCA para reducir de 4096 a 25 dimensiones y repite el análisis, encontrando que los clusters casan algo mejor con las personas (de 0.148 a 0.230 en silhouette, de 0.454 a 0.467 en Rand ajustado). Visualizando las primeras componentes principales se obtienen las "eigenfaces", pseudo-caras fantasmales que muestran cómo varían las caras del conjunto.

```python
pca = PCA(25)          # número de componentes a extraer
pca.fit(X)
X_reduced = pca.transform(X)
```

## La maldición de la dimensionalidad

La geometría en espacios de muchas dimensiones es extraña, y eso importa porque un algoritmo con d features opera sobre vectores que viven en un espacio d-dimensional. Si las features son, por ejemplo, todos los píxeles de una imagen, d es enorme y el rendimiento de los algoritmos empieza a degradarse. El problema de fondo: en dimensiones altas todos los puntos quedan muy lejos unos de otros. En el experimento del libro, con mil puntos aleatorios en el cubo unidad, para d = 500 dos puntos están casi siempre a la misma distancia entre sí; en una esfera de dimensión alta, casi toda la masa está en la corteza. La conclusión práctica: para que los algoritmos funcionen bien, casi siempre hace falta comprimir los datos a un espacio de menor dimensión.

## Análisis de componentes principales (PCA) y factor analysis

PCA es el algoritmo por excelencia de reducción de dimensionalidad. Geométricamente asume que los datos tienen forma "de balón de fútbol americano": una mancha elipsoidal estirada en unos ejes y estrecha en otros, sin grandes outliers. Si los datos están "realmente" sobre la recta x = y con algo de ruido, basta la feature x + y para aproximarlos bien: es más significativa que las features crudas y más eficiente de procesar (un número en vez de dos).

Técnicamente, PCA toma vectores d-dimensionales y encuentra d vectores "componentes principales" de longitud 1 (p1, p2, …, pd), de modo que cada punto x se expresa como combinación lineal: x = a1·p1 + a2·p2 + … + ad·pd. Las componentes se eligen de forma que a1 es mucho mayor que el resto, a2 mayor que a3 en adelante, etc. Así, las primeras pocas componentes capturan la mayor parte de la variación. El caso ideal es cuando grandes grupos de features están muy correlacionadas, como en una fotografía donde píxeles adyacentes tienen brillo similar. Al pasar el número de componentes como parámetro a PCA solo se extraen las primeras, lo que es mucho más eficiente.

## Skree plots y entender la dimensionalidad

Rara vez queda claro cuántas dimensiones "reales" tiene un dataset. Lo habitual es que las primeras componentes sean las más importantes y luego haya un descenso suave hacia la inutilidad. Se suele representar la importancia de cada componente (la fracción de la varianza del dataset que explica) en un "skree plot". A ojo, el autor estima que el dataset de caras tiene más o menos 15 dimensiones: todavía muchas, pero muchas menos que las 4096 originales.

## Factor analysis

PCA está emparentado con la técnica estadística del factor analysis: matemáticamente son lo mismo (un cambio de coordenadas donde la mayor varianza queda en la primera coordenada, la segunda en la segunda, etc.). La diferencia es de uso. En PCA el objetivo es reducir dimensionalidad. El factor analysis busca identificar "factores" causales que dan lugar a los datos observados; el ejemplo histórico es el estudio de la inteligencia, donde un único "g-factor" explica cerca de la mitad de la varianza entre distintos tests. El libro adopta la perspectiva de PCA, pero ambos puntos de vista son útiles.

## Limitaciones de PCA

Hay tres grandes trampas:

- Las dimensiones deben escalarse a desviaciones estándar comparables. Si se multiplica una feature por mil (p. ej. medir en milímetros en vez de metros), PCA la considerará mucho más importante. En imágenes no suele ser problema (todos los píxeles van en la misma escala), pero en datos demográficos ingresos y altura deben ir a una escala común. PCA también es muy sensible a los outliers.
- PCA asume que los datos son lineales. Si la forma "real" es un arco en el espacio, se difumina en varias componentes; seguirá sirviendo para reducir, pero las componentes no serán muy significativas.
- En imágenes de caras, las partes clave deben estar alineadas entre sí. PCA no sirve si, por ejemplo, los ojos caen en píxeles distintos; la alineación automática queda fuera del alcance de la mayoría de los data scientists.

## Clustering

El clustering es más resbaladizo que PCA: está claro qué debe hacer PCA, pero rara vez sabemos qué queremos del clustering. No hay definición analítica de "buenos" clusters; la única métrica real es si reflejan una segmentación natural subyacente, difícil de evaluar. Preguntas a tener presentes: ¿y si los puntos forman un continuo?, ¿deben poder solaparse los clusters?, ¿los quiero compactos como bolitas o permito formas tipo donut?

Evaluación en el mundo real: cuando no hay ground truth, el autor recomienda una batería de comprobaciones de sentido común: calcular estadísticas de cada cluster con features NO usadas para agrupar; examinar a mano muestras aleatorias de distintos clusters; proyectar con PCA a dos dimensiones y hacer un scatterplot; o elegir dos features relevantes y graficarlas; probar otro algoritmo de clustering; y reagrupar sobre un subconjunto aleatorio para ver si salen clusters similares. También importa si en el futuro habrá que asignar puntos nuevos: algunos algoritmos tienen criterios claros para ello y otros exigirían reagrupar todo el dataset.

### k-means

Es uno de los métodos más simples. Parte de vectores en espacio d-dimensional y los particiona en clusters compactos y no solapados. El algoritmo clásico:

1. Empezar con k centros de cluster iniciales.
2. Asignar cada punto al centro más cercano.
3. Recalcular el centro de cada cluster como la media de sus puntos.
4. Repetir 2 y 3 hasta cumplir un criterio de parada.

```python
from sklearn.cluster import KMeans
model = KMeans(n_clusters=k)
model.fit(my_data)
labels = model.labels_
cluster_centers = model.cluster_centers_
```

Si k es mayor que el número "real" de clusters, k-means divide un cluster real en varios: pasa a ser más una forma de particionar el dataset en regiones "naturales". No garantiza clusters óptimos, por lo que se reinicia varias veces con centros aleatorios (scikit-learn lo hace por defecto). Asignar puntos nuevos es trivial: al centro más cercano.

### Gaussian mixture models (GMM)

Los GMM son como una versión de k-means que captura la "zona gris" y da niveles de confianza al asignar un punto. Cada cluster se modela como una Gaussiana multivariante, y el modelo se especifica con: el número de clusters, la fracción de puntos en cada uno, y la media y la matriz de covarianza d×d de cada cluster. Durante el entrenamiento nunca se decide definitivamente a qué cluster pertenece un punto: cada punto influye en la media y la varianza de un cluster en proporción a su probabilidad de pertenecer a él. Comparten virtudes y defectos de k-means (simples, ligeros, salida clara y reutilizable; pero asumen clusters más o menos convexos y pueden caer en mínimos locales). Todos los mixture models se entrenan con el algoritmo EM, agnóstico a la distribución modelada.

```python
from sklearn import mixture
model = mixture.GMM(n_components=5)
model.fit(my_data)
labels = model.predict_proba(my_data)
```

### Clustering aglomerativo

El clustering jerárquico empieza con muchos clusters pequeños (cada punto el suyo) y va fusionándolos hasta un único cluster gigante; la salida es una jerarquía de agrupaciones posibles. Ventaja sobre k-means: los clusters pueden tener cualquier tamaño o forma. Desventaja: no hay forma natural de asignar un punto nuevo. La linkage "ward" fusiona los dos clusters con menor varianza entre ellos.

```python
from sklearn.cluster import AgglomerativeClustering
clst = AgglomerativeClustering(n_clusters=5, linkage='ward')
cluster_labels = clst.fit_predict(my_data)
```

## Evaluar la calidad de los clusters

Los métodos algorítmicos son de dos tipos: supervisados (hay ground truth y se mide cuánto se ajustan los clusters hallados) y no supervisados (se mira lo geométricamente distintos que son los clusters).

Silhouette score: el método no supervisado más común, ideal para k-means. Parte de que los clusters deben ser densos y bien separados, así que funciona mejor con clusters compactos y de tamaño comparable (no con un donut con otra mancha en el centro). Para cada punto se define a = distancia media a los puntos de su propio cluster y b = distancia media a los del cluster más cercano; el coeficiente es s = (b − a) / max(a, b), entre −1 y 1. Cerca de 1, el punto está mucho más cerca de su cluster; cerca de 0, equidistante (solapamiento); negativo, mal asignado. El score del cluster es el promedio de sus coeficientes. No es perfecto: un punto correcto en un cluster muy grande y cercano a otro puede recibir mala puntuación.

Rand index: supervisado. Un par (x, y) está "correctamente agrupado" si lo ponemos juntos y el ground truth también, o si lo ponemos separados y el ground truth también. Con n puntos hay n(n−1)/2 pares; el índice es la fracción de pares correctos (de 0 a 1). Problema: incluso agrupando al azar se aciertan pares por casualidad. El adjusted Rand index corrige esto escalando el índice para que valga 0 de media con asignaciones aleatorias y 1 con coincidencia perfecta.

Mutual information: métrica supervisada tomada de la teoría de la información, parecida a la correlación pero para variables categóricas. Mide cuánto se puede acertar sobre el cluster real de un punto conociendo solo el cluster asignado (y viceversa). Si las distribuciones son independientes vale 0; si una se infiere perfectamente de la otra, da la entropía de la distribución.

```python
from sklearn import metrics
metrics.adjusted_rand_score(labels_true, labels_pred)
metrics.mutual_info_score(labels_true, labels_pred)
```

## Ideas clave

- El aprendizaje no supervisado estudia la estructura latente sin "respuestas correctas"; sus dos vías son clustering (revelar grupos) y reducción de dimensionalidad (extraer la variabilidad real, a menudo por motivos computacionales).
- La curse of dimensionality hace que en dimensiones altas los puntos queden casi equidistantes; comprimir a menos dimensiones suele ser prerequisito para cualquier análisis.
- PCA expresa cada punto como combinación lineal de componentes principales ordenadas por varianza; las primeras pocas capturan la mayor parte de la estructura. El skree plot ayuda a elegir cuántas conservar.
- PCA y factor analysis son matemáticamente lo mismo, pero PCA reduce dimensiones y el factor analysis busca factores causales.
- Limitaciones de PCA: exige escalas comparables, asume linealidad, es sensible a outliers y requiere imágenes alineadas.
- k-means particiona en clusters compactos y no solapados, es simple y permite asignar puntos nuevos al centro más cercano, pero no garantiza optimalidad.
- Los GMM añaden una "zona gris" con niveles de confianza modelando cada cluster como una Gaussiana; el clustering aglomerativo construye una jerarquía y admite formas variadas pero no asigna fácilmente puntos nuevos.
- La calidad se evalúa con métodos no supervisados (silhouette) o supervisados (Rand index, adjusted Rand index, mutual information), siempre apoyados en comprobaciones de sentido común.
