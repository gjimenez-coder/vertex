# Conexiones entre libros

Enlaces temáticos entre los siete libros de ciencia de datos de esta carpeta: *Better Data Visualizations* (Schwabish), *Doing Data Science* (O'Neil & Schutt), *The Data Science Handbook* (Cady), *Data Science for Business* (Provost & Fawcett), *Forecasting: Principles and Practice* (Hyndman), *Storytelling with Data* (Knaflic) y *Natural Language Processing with Python* (Bird, Klein & Loper).

Cada tema recoge qué dice cada libro con respaldo explícito en sus apuntes (README y glosario), con un enlace relativo al capítulo correspondiente, y una frase final de qué los conecta o en qué difieren. Solo se incluyen temas tratados por dos o más libros. Al final hay una lista de temas exclusivos de cada libro.

## Naive Bayes

- *Doing Data Science*: clasificador lineal derivado de la ley de Bayes que combina palabras asumiéndolas independientes, barato e incremental, aplicado a filtros de spam ([cap04](doing-data-science/cap04-spam-filters-naive-bayes-and-wrangling.md)).
- *Data Science for Business*: método generativo que aplica la Regla de Bayes con independencia condicional; eficiente y baseline habitual ([cap09](data-science-for-business/cap09-evidence-and-probabilities.md)).
- *The Data Science Handbook*: clasificador que asume independencia entre características y aun así suele ser potente ([cap08](the-data-science-handbook/cap08-machine-learning-classification.md)).
- *NLP with Python*: clasificador generativo P(input, label) donde cada rasgo contribuye de forma independiente combinando prior y P(f|label); requiere suavizado ([cap06](nlp-with-python/cap06-learning-to-classify-text.md)).

Los cuatro coinciden en la suposición "ingenua" de independencia condicional y en su bajo coste; *Doing Data Science* y *NLP with Python* lo anclan en texto (spam, clasificación), mientras *Data Science for Business* lo presenta como baseline generativo y el *Handbook* subraya su robustez pese a la suposición.

## Overfitting y su control

- *Doing Data Science*: ajuste excesivo que hay que vigilar; los árboles sin podar sobreajustan, y se detecta con cross-validation ([cap02](doing-data-science/cap02-statistical-inference-exploratory-data-analysis-and-the-data-science-process.md), [cap13](doing-data-science/cap13-lessons-learned-from-data-competitions-data-leakage-and-model-evaluation.md)).
- *Data Science for Business*: ajustar a los datos de entrenamiento a costa de la generalización; en el fondo un problema de comparaciones múltiples, controlado con holdout, poda y regularización ([cap05](data-science-for-business/cap05-overfitting-and-its-avoidance.md)).
- *The Data Science Handbook*: el mayor riesgo del ML, memorizar el dato de entrenamiento sin generalizar ([cap06](the-data-science-handbook/cap06-machine-learning-overview.md)).

Los tres lo tratan como el riesgo central del modelado; *Data Science for Business* es el más teórico (comparaciones múltiples, fitting graph) y *Doing Data Science* lo liga a casos concretos de competiciones y árboles.

## Validación cruzada

- *Doing Data Science*: validación cruzada usada para detectar overfitting y que siempre conviene aplicar ([cap03](doing-data-science/cap03-algorithms.md)).
- *Data Science for Business*: divide el dataset en k folds y produce media y varianza del rendimiento, aprovechando mejor datos limitados ([cap05](data-science-for-business/cap05-overfitting-and-its-avoidance.md)).
- *Forecasting*: evaluación honesta que respeta el orden temporal con un rolling forecasting origin, entrenando con el pasado y evaluando sobre el futuro ([cap05](forecasting-principles-and-practice/cap05-time-series-cross-validation.md)).
- *NLP with Python*: técnica de evaluación que aporta fiabilidad a las métricas de un clasificador ([cap06](nlp-with-python/cap06-learning-to-classify-text.md)).

Todos la usan para una evaluación fiable; la diferencia clave es que *Forecasting* no puede barajar los datos y debe desplazar el origen en el tiempo, mientras los demás dividen en folds libremente.

## Árboles de decisión, entropía e information gain

- *Doing Data Science*: método que elige el atributo que maximiza la ganancia de información (basada en entropía); interpretable y suele podarse para evitar el sobreajuste ([cap07](doing-data-science/cap07-extracting-meaning-from-data.md)).
- *Data Science for Business*: segmentación supervisada construida por tree induction; la entropía mide la impureza y el information gain, cuánto la reduce un atributo ([cap03](data-science-for-business/cap03-introduction-to-predictive-modeling-from-correlation-to-supervised-segmentation.md)).
- *The Data Science Handbook*: desmitifica los clasificadores y recorre árboles y random forests dentro del ML ([cap08](the-data-science-handbook/cap08-machine-learning-classification.md)).
- *NLP with Python*: clasificador interpretable que maneja mal la interacción de rasgos, construido guiado por la ganancia de información ([cap06](nlp-with-python/cap06-learning-to-classify-text.md)).

Coinciden en la entropía/ganancia de información como criterio de división; *Data Science for Business* y *Doing Data Science* lo desarrollan formalmente, mientras *NLP with Python* advierte de sus límites con rasgos interdependientes.

## Random forests y ensembles

- *Doing Data Science*: generalización de los árboles con bagging; más preciso y robusto pero poco interpretable ([cap07](doing-data-science/cap07-extracting-meaning-from-data.md)).
- *Data Science for Business*: los ensembles reducen error combinando modelos con errores distintos, útil con métodos de alta varianza como los árboles ([cap12](data-science-for-business/cap12-other-data-science-tasks-and-techniques.md)).
- *The Data Science Handbook*: ensemble muy preciso y robusto por la ley de los grandes números, casi imposible de interpretar ([cap08](the-data-science-handbook/cap08-machine-learning-classification.md)).

Los tres destacan el mismo trade-off: ganancia de precisión y robustez a costa de interpretabilidad; *Data Science for Business* lo enmarca en la descomposición sesgo-varianza.

## k-means y clustering

- *Doing Data Science*: clustering no supervisado que itera asignación y recálculo de centroides; elegir k es arte y la interpretabilidad es el mayor problema ([cap03](doing-data-science/cap03-algorithms.md)).
- *Data Science for Business*: clustering en torno a centroides que requiere fijar k, se repite por caer en óptimos locales y se evalúa con la distorsión ([cap06](data-science-for-business/cap06-similarity-neighbors-and-clusters.md)).
- *The Data Science Handbook*: algoritmo que particiona en clusters compactos y no solapados, simple pero sin garantía de optimalidad ([cap10](the-data-science-handbook/cap10-unsupervised-learning-clustering-and-dimensionality-reduction.md)).

Coinciden en el procedimiento iterativo y en la necesidad de fijar k; *The Data Science Handbook* añade el GMM como alternativa "suave" y *Data Science for Business* lo integra con la similitud por distancia.

## k-Nearest Neighbors

- *Doing Data Science*: clasificación no paramétrica por voto mayoritario de los vecinos; dependen la métrica de distancia, el escalado y la elección de k ([cap03](doing-data-science/cap03-algorithms.md)).
- *Data Science for Business*: método de lazy learning que predice clasificación, regresión o probabilidad combinando los vecinos; k es su parámetro de complejidad ([cap06](data-science-for-business/cap06-similarity-neighbors-and-clusters.md)).

Ambos lo presentan como método basado en distancia sensible a la elección de k; *Data Science for Business* lo integra con la similitud y la maldición de la dimensionalidad, y *Doing Data Science* señala por qué falla en spam.

## Regresión logística

- *Doing Data Science*: modelo de clasificación que usa la inverse-logit para devolver probabilidades y se ajusta por máxima verosimilitud ([cap05](doing-data-science/cap05-logistic-regression.md)).
- *Data Science for Business*: modela las log-odds y las convierte en probabilidad vía la función logística; pese a su nombre, estima probabilidad de clase ([cap04](data-science-for-business/cap04-fitting-a-model-to-data.md)).
- *The Data Science Handbook*: clasificador que equilibra precisión e interpretabilidad vía la sigmoide ([cap08](the-data-science-handbook/cap08-machine-learning-classification.md)).

Los tres aclaran que, pese al nombre, es un clasificador probabilístico; *Doing Data Science* y *Data Science for Business* detallan su ajuste por máxima verosimilitud sobre un modelo lineal.

## Regresión lineal y mínimos cuadrados

- *Doing Data Science*: modelo que asume linealidad y ruido, se ajusta por mínimos cuadrados y se evalúa con R², p-values y cross-validation ([cap03](doing-data-science/cap03-algorithms.md)).
- *Data Science for Business*: discriminante lineal y modelado paramétrico; regresión lineal, logística y SVM comparten el modelo lineal y difieren en su función objetivo ([cap04](data-science-for-business/cap04-fitting-a-model-to-data.md)).
- *The Data Science Handbook*: predicción de una salida real por least squares, muy sensible a outliers, con R² y LASSO ([cap11](the-data-science-handbook/cap11-regression.md)).

Coinciden en el ajuste por mínimos cuadrados y en R² como medida; *Data Science for Business* la unifica con logística y SVM bajo el modelo lineal, y el *Handbook* insiste en la sensibilidad a outliers y la regularización LASSO.

## Regularización y LASSO

- *Data Science for Business*: optimiza ajuste más simpleza con una penalización ponderada por λ; L2 da ridge y L1 da lasso ([cap05](data-science-for-business/cap05-overfitting-and-its-avoidance.md)).
- *The Data Science Handbook*: LASSO penaliza pesos no nulos (parámetro alpha), combate el sobreajuste y lleva coeficientes a 0 ([cap11](the-data-science-handbook/cap11-regression.md)).

Ambos presentan la regularización como control del sobreajuste; coinciden en que L1 (LASSO) tiende a anular coeficientes, con *Data Science for Business* distinguiendo también ridge (L2).

## PCA y reducción de dimensionalidad

- *Doing Data Science*: busca U y V minimizando el error cuadrático y produce atributos latentes no correlacionados, dentro del motor de recomendación ([cap08](doing-data-science/cap08-recommendation-engines-building-a-user-facing-data-product-at-scale.md)).
- *The Data Science Handbook*: expresa cada punto como combinación lineal de componentes principales ordenadas por varianza ([cap10](the-data-science-handbook/cap10-unsupervised-learning-clustering-and-dimensionality-reduction.md)).

Ambos describen PCA como extracción de atributos latentes; *Doing Data Science* lo liga a SVD y recomendación, mientras el *Handbook* lo encuadra en el aprendizaje no supervisado junto al clustering.

## Maldición de la dimensionalidad

- *Doing Data Science*: fenómeno por el que incluso los vecinos más cercanos están lejos, lo que impide usar k-NN en spam ([cap04](doing-data-science/cap04-spam-filters-naive-bayes-and-wrangling.md)).
- *Data Science for Business*: limitación de k-NN mitigada con selección de características y pesos ([cap06](data-science-for-business/cap06-similarity-neighbors-and-clusters.md)).
- *The Data Science Handbook*: en dimensiones altas los puntos quedan casi equidistantes ([cap10](the-data-science-handbook/cap10-unsupervised-learning-clustering-and-dimensionality-reduction.md)).

Los tres la vinculan a los métodos basados en distancia; *Doing Data Science* y *Data Science for Business* la conectan directamente con las limitaciones de k-NN.

## Máxima verosimilitud

- *Doing Data Science*: método de estimación de parámetros que minimiza la log-verosimilitud negativa, p. ej. con Newton o SGD ([cap02](doing-data-science/cap02-statistical-inference-exploratory-data-analysis-and-the-data-science-process.md), [cap05](doing-data-science/cap05-logistic-regression.md)).
- *Data Science for Business*: criterio de ajuste de la regresión logística y base del profiling como ajuste de una gaussiana ([cap04](data-science-for-business/cap04-fitting-a-model-to-data.md)).
- *The Data Science Handbook*: estimación que busca el θ que maximiza P(X|θ), pilar del libro junto a la optimización ([cap23](the-data-science-handbook/cap23-maximum-likelihood-estimation-and-optimization.md)).
- *Forecasting*: estimación por máxima verosimilitud de parámetros y estados iniciales de los modelos de suavizado exponencial, minimizando L* ([cap03](forecasting-principles-and-practice/cap03-exponential-smoothing.md)).

Los cuatro la usan como criterio de ajuste de parámetros; *The Data Science Handbook* la trata como fundamento matemático, mientras los demás la aplican a un modelo concreto (logística, ETS).

## Descenso de gradiente y SGD

- *Doing Data Science*: el SGD escala mejor con datos enormes y dispersos, usado para ajustar regresión lineal y logística ([cap03](doing-data-science/cap03-algorithms.md), [cap05](doing-data-science/cap05-logistic-regression.md)).
- *The Data Science Handbook*: el descenso de gradiente se mueve en dirección −∇f y el SGD aproxima el gradiente con pocos puntos, viable con datasets grandes ([cap23](the-data-science-handbook/cap23-maximum-likelihood-estimation-and-optimization.md)).

Ambos presentan el SGD como la variante escalable del descenso de gradiente para datos masivos; el *Handbook* lo enmarca en la optimización numérica general y *Doing Data Science* en el ajuste de modelos lineales.

## Big Data: MapReduce, Hadoop y Spark

- *Doing Data Science*: MapReduce (Google, 2004) para volúmenes que no caben en una máquina, con su ecosistema Hadoop (HDFS, Hive) y Spark para algoritmos iterativos ([cap14](doing-data-science/cap14-data-engineering-mapreduce-pregel-and-hadoop.md)).
- *The Data Science Handbook*: delimita qué es Big Data y cuándo usarlo, con Hadoop/HDFS, Spark/RDD y un MapReduce ya anticuado ([cap13](the-data-science-handbook/cap13-big-data.md)).
- *Data Science for Business*: tecnologías que dan soporte a la data science, pero que no son data science en sí ([cap01](data-science-for-business/cap01-introduction-data-analytic-thinking.md)).

Coinciden en el stack MapReduce/Hadoop/Spark; el *Handbook* y *Doing Data Science* lo detallan técnicamente, mientras *Data Science for Business* lo relativiza como soporte, no como fin.

## Data leakage (fuga de datos)

- *Doing Data Science*: información no disponible en el momento real de la predicción, a menudo causa y efecto invertidos o artefactos de preparación, con AUC sospechosamente alto ([cap13](doing-data-science/cap13-lessons-learned-from-data-competitions-data-leakage-and-model-evaluation.md)).
- *Data Science for Business*: variable usada en la preparación de datos que no estará disponible en el momento de decidir ([cap02](data-science-for-business/cap02-business-problems-and-data-science-solutions.md)).

Ambos la definen igual —información del futuro que se cuela en el entrenamiento— y advierten de resultados "demasiado buenos"; *Doing Data Science* lo ilustra con competiciones y *Data Science for Business* lo integra en el proceso CRISP-DM.

## Evaluación con clases desbalanceadas: ROC, AUC, precision/recall

- *Doing Data Science*: con clases desbalanceadas, precision y recall sustituyen a la exactitud engañosa; el AUC cercano a 1 delata fuga de datos ([cap09](doing-data-science/cap09-data-visualization-and-fraud-detection.md)).
- *Data Science for Business*: la exactitud falla con clases desbalanceadas; la matriz de confusión, la curva ROC y el AUC desacoplan el rendimiento de priors y costes ([cap07](data-science-for-business/cap07-decision-analytic-thinking-i-what-is-a-good-model.md), [cap08](data-science-for-business/cap08-visualizing-model-performance.md)).
- *The Data Science Handbook*: la F1 resume el rendimiento de un clasificador binario ([cap08](the-data-science-handbook/cap08-machine-learning-classification.md)).

Los tres rechazan la exactitud como métrica única; *Data Science for Business* es el más completo (ROC, AUC, lift, profit curves) y *Doing Data Science* conecta el AUC con la fuga de datos.

## Minería de texto: bag-of-words y TF-IDF

- *Data Science for Business*: el bag of words trata cada palabra como característica independiente, y el TFIDF pondera por frecuencia en el documento y rareza en el corpus ([cap10](data-science-for-business/cap10-representing-and-mining-text.md)).
- *The Data Science Handbook*: el bag-of-words convierte texto en vectores numéricos y el TF-IDF da más importancia a las palabras raras; la cosine similarity compara documentos ([cap16](the-data-science-handbook/cap16-natural-language-processing.md)).

Ambos presentan la misma tubería bag-of-words → TF-IDF → similitud coseno como base del NLP práctico; coinciden incluso en el papel de la rareza del término.

## NLP y reconocimiento de entidades

- *The Data Science Handbook*: introduce el NLP estadístico con bag-of-words, cosine similarity y TF-IDF, y problemas típicos de texto ([cap16](the-data-science-handbook/cap16-natural-language-processing.md)).
- *NLP with Python*: NER identifica límites y tipo de entidades (ORGANIZATION, PERSON...) y la relation extraction las enlaza para poblar bases de datos ([cap07](nlp-with-python/cap07-extracting-information-from-text.md)).
- *Data Science for Business*: entre las técnicas avanzadas de texto cita n-gramas, entidades nombradas y topic models ([cap10](data-science-for-business/cap10-representing-and-mining-text.md)).

Los tres abordan el procesamiento de lenguaje; *The Data Science Handbook* y *Data Science for Business* lo tratan como representación para ML, mientras *NLP with Python* profundiza en la extracción de información estructurada.

## Series temporales y ARIMA

- *Forecasting*: dedica el libro a las series temporales, con ARIMA(p,d,q), suavizado exponencial, descomposición y estacionariedad ([cap07](forecasting-principles-and-practice/cap07-non-seasonal-arima-models.md)).
- *The Data Science Handbook*: reformula las series temporales como problemas de ML (remuestreo, suavizado, Fourier) y el modelado estocástico incluye ARIMA ([cap17](the-data-science-handbook/cap17-time-series-analysis.md), [cap25](the-data-science-handbook/cap25-stochastic-modeling.md)).
- *Doing Data Science*: datos con marca de tiempo cuyo orden permite ver causa, tendencia y estacionalidad, aplicados al modelado financiero ([cap06](doing-data-science/cap06-time-stamps-and-financial-modeling.md)).

Los tres tratan datos ordenados en el tiempo; *Forecasting* es el especialista (ARIMA, ETS, estacionalidad), el *Handbook* los reencuadra como ML y *Doing Data Science* se centra en el caso financiero y la causalidad temporal.

## Principios Gestalt y procesamiento preatentivo

- *Better Data Visualizations*: los principios Gestalt (proximidad, similitud, cierre, continuidad, conexión) y el procesamiento preatentivo (color, peso, posición) explican cómo agrupamos y a dónde miramos ([cap01](better-data-visualizations/cap01-visual-processing-and-perceptual-rankings.md)).
- *Storytelling with Data*: los principios Gestalt distinguen señal de ruido y los atributos preatentivos (tamaño, color, posición) dirigen la mirada casi al instante ([cap03](storytelling-with-data/cap03-clutter-is-your-enemy.md), [cap04](storytelling-with-data/cap04-focus-your-audience-s-attention.md)).

Ambos parten de la misma psicología de la percepción para justificar sus decisiones de diseño; coinciden en Gestalt y en los atributos/procesamiento preatentivo como herramientas para guiar la atención.

## Reducir el desorden (clutter / data-ink)

- *Better Data Visualizations*: el clutter son elementos que distraen o distorsionan (cuadrículas pesadas, 3D); la segunda pauta es reducirlo y empezar con gris ([cap02](better-data-visualizations/cap02-five-guidelines-for-better-data-visualizations.md)).
- *Storytelling with Data*: el desorden es el enemigo; el data-ink ratio de Tufte y el decluttering iterativo reducen la carga cognitiva ([cap03](storytelling-with-data/cap03-clutter-is-your-enemy.md)).

Ambos defienden eliminar todo elemento que no aporta; comparten la idea del data-ink ratio y el uso del gris/énfasis selectivo, con *Storytelling* enfatizando la carga cognitiva.

## Elegir el gráfico adecuado

- *Better Data Visualizations*: organiza las familias de gráficos por objetivo (comparar categorías, tiempo, distribución, relación, parte-todo) guiado por la jerarquía perceptiva ([cap03](better-data-visualizations/cap03-form-and-function.md), [cap04](better-data-visualizations/cap04-comparing-categories.md)).
- *Storytelling with Data*: unos pocos tipos de visuales —texto, tabla, heatmap, scatterplot, línea, slopegraph, barras, área— cubren casi todo ([cap02](storytelling-with-data/cap02-choosing-an-effective-visual.md)).
- *The Data Science Handbook*: sin imagen lo estás haciendo mal; repasa gráficos y el boxplot delata outliers que un histograma disimularía ([cap05](the-data-science-handbook/cap05-visualizations-and-simple-metrics.md)).

Los tres insisten en elegir el visual según la pregunta; *Better Data Visualizations* es el catálogo exhaustivo, *Storytelling* reduce a un repertorio mínimo y el *Handbook* lo integra en el flujo analítico.

## Anscombe's quartet (visualizar antes de resumir)

- *Better Data Visualizations*: cuatro conjuntos (1973) con los mismos estadísticos que solo revelan sus diferencias al graficarlos, junto al Datasaurus ([cap01](better-data-visualizations/cap01-visual-processing-and-perceptual-rankings.md), [cap08](better-data-visualizations/cap08-relationship.md)).
- *The Data Science Handbook*: ejemplo que prueba que los números resumen engañan y que no hay sustituto para graficar los datos ([cap05](the-data-science-handbook/cap05-visualizations-and-simple-metrics.md)).

Ambos usan el mismo ejemplo clásico para la misma moraleja: las estadísticas resumen pueden ocultar la estructura real de los datos.

## Correlación de Pearson

- *Better Data Visualizations*: el coeficiente de Pearson (ρ) indica dirección y magnitud de la asociación lineal, de −1 a 1, y no implica causalidad ([cap08](better-data-visualizations/cap08-relationship.md)).
- *The Data Science Handbook*: coeficiente de correlación que asume linealidad, frente a Spearman y Kendall que solo exigen monotonicidad ([cap05](the-data-science-handbook/cap05-visualizations-and-simple-metrics.md)).

Ambos definen Pearson como medida de asociación lineal; el *Handbook* añade las alternativas de rango (Spearman, Kendall) y *Better Data Visualizations* subraya que correlación no es causalidad.

## Temas exclusivos de cada libro

- **Better Data Visualizations**: catálogo de gráficos geoespaciales (choropleth, cartograma, flow map), proyecciones y binning; parte-todo y jerárquicos (treemap, sunburst, Nightingale, Voronoi); tablas como visualización; guía de estilo con paletas, fuentes y accesibilidad (WCAG, Sección 508); rediseños.
- **Doing Data Science**: datificación y perfil del científico de datos; motores de recomendación a escala (SVD, ALS, grafo bipartito); análisis de redes sociales y centralidad (ERGM, cierre triádico); causalidad (modelo de Rubin, paradoja de Simpson, puntaje de propensión); epidemiología y OMOP; ingeniería de datos (Pregel, Giraph); ética y soberbia algorítmica.
- **The Data Science Handbook**: formatos de archivo y encodings (CSV, JSON, XML, DEFLATE); bases de datos SQL/NoSQL (joins, DBMS); buenas prácticas de software (TDD, AGILE, control de versiones); conceptos de lenguajes de programación (compilación, tipos, duck typing); memoria y estructuras de datos (Big-O, arrays, hash tables, punteros); probabilidad y estadística formal (entropía, contraste de hipótesis, Bonferroni); deep learning (CNN, RNN, LSTM, dropout) y redes bayesianas; modelado estocástico (Markov, HMM/Viterbi, Poisson).
- **Data Science for Business**: data-analytic thinking y DDD; proceso CRISP-DM; marco de valor esperado y pensamiento decisión-analítico; ingeniería analítica; asociaciones (support, lift, leverage); profiling y predicción de enlaces; ventaja competitiva y estrategia de negocio; guías de evaluación de propuestas.
- **Forecasting: Principles and Practice**: métodos benchmark (naïve, drift); suavizado exponencial y modelos ETS (Holt, Holt-Winters); descomposición STL; estacionariedad, transformación Box-Cox y diferenciación; modelos ARIMA estacionales; espacio de estados y filtro de Kalman; regresión dinámica con errores ARIMA; pronóstico jerárquico y reconciliación; VAR; redes NNAR; estacionalidad compleja (TBATS).
- **Storytelling with Data**: contexto de la comunicación (who/what/how, Gran Idea); storyboarding y el relato con conflicto y tensión (tres actos de Aristóteles, sound bites); pensar como diseñador (affordances, aceptación, resistencia al cambio); enfoque del optometrista; instalar la competencia en un equipo.
- **Natural Language Processing with Python**: pipeline NLP con NLTK y repasos de Python; acceso a corpus y WordNet (synsets, hiperónimos, merónimos); POS tagging y taggers (backoff, Brill); chunking, chinking e IOB; gramáticas formales y parsing (CFG, PCFG, chart parsing, shift-reduce); gramáticas basadas en rasgos (unificación, subsunción, reentrancia); semántica (lógica de primer orden, cálculo λ, DRT); gestión de datos lingüísticos (OLAC, standoff, kappa, round-tripping).
