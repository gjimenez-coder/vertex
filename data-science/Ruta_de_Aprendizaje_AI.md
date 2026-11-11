# Plan de Estudios de IA / Data Analytics

> Plan de estudios enfocado en el aprendizaje: **qué estudiar**, **por qué estudiarlo** y **cómo aplicarlo**. Organizado como una ruta progresiva, de los fundamentos a la especialización e integración.

## Ruta de aprendizaje (orden recomendado)

```
1. Programación y manejo de datos   →  base técnica
2. Estadística y probabilidad        →  base matemática
3. Análisis exploratorio de datos    →  entender los datos
4. Aprendizaje de máquina            →  modelar y predecir
5. Aprendizaje profundo              →  problemas complejos
6. Series temporales                 →  especialización
7. Visualización y comunicación      →  transmitir valor
8. Big Data e infraestructura        →  escalar
9. Gestión y aplicación de proyectos →  integración (capstone)
```

Cada etapa construye sobre la anterior. Puedes avanzar de forma lineal o volver a reforzar una base cuando una etapa posterior lo exija.

---

## 1. Programación y Manejo de Datos

**Objetivo de la etapa:** adquirir la base técnica para manipular datos de forma programática.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Fundamentos de Python (variables, tipos, expresiones, control de flujo, funciones) | Es el lenguaje base de todo el ecosistema de ciencia de datos | Escribir scripts que automaticen cálculos y transformaciones sencillas |
| Estructuras de datos (listas, tuplas, diccionarios, conjuntos) | Permiten organizar y acceder a datos eficientemente | Modelar datos en memoria antes de pasarlos a librerías especializadas |
| Cómputo numérico y vectorial (NumPy) | El cálculo vectorizado es la base del rendimiento en análisis de datos | Operar vectores y matrices para cálculos estadísticos y de ML |
| Datos tabulares (pandas: DataFrame, Series, índices) | La mayoría de los datos reales son tablas | Cargar, filtrar, agrupar y transformar datasets |
| Gestión de entornos y paquetes (Conda) | Garantiza reproducibilidad y evita conflictos de dependencias | Crear entornos aislados por proyecto |
| Control de versiones (Git, GitHub, SSH) | Permite trabajar en equipo y rastrear cambios | Versionar código y colaborar en repositorios remotos |

## 2. Estadística y Probabilidad

**Objetivo de la etapa:** construir la base matemática para describir datos y razonar bajo incertidumbre.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Estadística descriptiva (tendencia central, dispersión, posición, forma) | Resume y caracteriza cualquier conjunto de datos | Describir un dataset antes de modelarlo |
| Asociación entre variables (covarianza, correlación, tablas de contingencia) | Revela relaciones que guían el modelado | Detectar qué variables se relacionan entre sí |
| Probabilidad y teorema de Bayes | Fundamenta el razonamiento bajo incertidumbre | Calcular probabilidades condicionales en problemas reales |
| Distribuciones de probabilidad (Binomial, Poisson, Normal, Exponencial, etc.) | Modelan el comportamiento de fenómenos aleatorios | Elegir el modelo adecuado para una variable |
| Inferencia estadística (TLC, intervalos de confianza, Bootstrap) | Permite generalizar de la muestra a la población | Estimar parámetros con una medida de confianza |
| Pruebas de hipótesis (una/dos poblaciones, errores, ANOVA) | Fundamentan la toma de decisiones basada en datos | Validar si una diferencia observada es significativa |
| Causalidad vs. correlación (modelos causales, d-separación) | Evita conclusiones erróneas y decisiones mal informadas | Distinguir relaciones causales de simples asociaciones |

## 3. Análisis Exploratorio y Preprocesamiento de Datos

**Objetivo de la etapa:** entender, limpiar y preparar los datos antes de modelar.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Tipos de datos y calidad de datos | La calidad determina la confiabilidad de todo el análisis | Diagnosticar problemas en un dataset nuevo |
| Valores faltantes e imputación | Los datos incompletos sesgan los resultados | Rellenar o descartar datos ausentes de forma justificada |
| Valores atípicos (outliers) | Pueden distorsionar modelos y métricas | Detectarlos y decidir cómo tratarlos |
| Análisis de asociaciones (algoritmo A-priori, Market Basket) | Descubre reglas y patrones de co-ocurrencia | Recomendar productos o detectar combinaciones frecuentes |
| Procesamiento de texto (Bag-of-words, tf-idf, embeddings) | Gran parte de la información es texto no estructurado | Preparar texto para clasificación o búsqueda |
| Análisis de grafos | Modela relaciones y redes complejas | Analizar redes sociales, rutas o dependencias |
| Datos geoespaciales (operaciones espaciales) | Muchos problemas tienen componente geográfico | Analizar ubicaciones, distancias y zonas de influencia |

## 4. Aprendizaje de Máquina

**Objetivo de la etapa:** construir modelos que aprenden patrones para predecir y decidir.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Aprendizaje supervisado vs. no supervisado | Define el enfoque según se tengan o no etiquetas | Elegir la estrategia correcta para cada problema |
| Regresión lineal (simple/múltiple, función de costo, gradiente descendente) | Es la base del modelado predictivo continuo | Predecir valores numéricos (precios, demanda) |
| Clasificación (regresión logística, regularización) | Resuelve problemas de categorización | Clasificar correos, clientes o diagnósticos |
| Evaluación y selección de modelos (validación cruzada, matriz de confusión, métricas) | Garantiza que el modelo generalice y no solo memorice | Comparar modelos y evitar sobreajuste |
| Reducción de dimensionalidad (selección de variables, PCA) | Mejora el desempeño y reduce ruido | Simplificar datasets con muchas variables |
| Árboles de decisión (ID3, CART, poda) | Modelos interpretables y potentes | Crear reglas de decisión explicables |
| Máquinas de vectores de soporte (SVM, kernels) | Eficaces en problemas complejos y no lineales | Clasificar datos difíciles de separar |
| Métodos de ensamble (bagging, random forest, votación) | Combinan modelos para mayor precisión y robustez | Mejorar resultados en problemas reales |
| Clustering (K-means, jerárquico, DBSCAN, RFM) | Descubre grupos sin etiquetas previas | Segmentar clientes o agrupar observaciones |

## 5. Aprendizaje Profundo

**Objetivo de la etapa:** aplicar redes neuronales a problemas complejos de datos no estructurados.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Redes neuronales (forward pass, retropropagación, funciones de activación) | Son la base del Deep Learning moderno | Entrenar modelos para regresión y clasificación |
| Perceptrón multicapa (MLP) | Arquitectura fundamental de las redes profundas | Resolver problemas no lineales generales |
| Redes convolucionales (CNN: convolución, filtros, pooling) | Especializadas en imágenes y datos espaciales | Clasificar imágenes y reconocer patrones visuales |
| Transferencia de aprendizaje | Reutiliza modelos preentrenados y ahorra recursos | Adaptar modelos existentes a nuevas tareas con pocos datos |
| Redes recurrentes (RNN, LSTM, GRU, Encoder-Decoder) | Modelan datos secuenciales y dependencias temporales | Procesar texto, secuencias y series temporales |

## 6. Series Temporales

**Objetivo de la etapa:** analizar y pronosticar datos que evolucionan en el tiempo.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Preprocesamiento temporal (remuestreo, interpolación, suavizado, windowing) | Las series requieren tratamiento específico | Preparar datos temporales para modelar |
| Análisis descriptivo (tendencia, estacionalidad, estacionariedad, autocorrelación) | Revela la estructura subyacente de la serie | Diagnosticar qué modelo es apropiado |
| Modelos estadísticos (AR, MA, ARMA, ARIMA, SARIMA, VAR, VARMA) | Son la base clásica del pronóstico | Predecir ventas, demanda o indicadores |
| Pronóstico con ML (feature engineering temporal, pipeline) | Supera limitaciones de los modelos estadísticos | Construir modelos predictivos más flexibles |
| Pronóstico con redes neuronales (MLP, CNN 1D, RNN, LSTM, GRU) | Capturan patrones complejos y no lineales | Pronosticar series difíciles con Deep Learning |

## 7. Visualización y Comunicación

**Objetivo de la etapa:** transmitir hallazgos de forma clara y accionable.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Gráficos según tipo de dato (líneas, barras, histogramas, heatmaps) | Cada dato requiere una representación adecuada | Elegir el gráfico correcto para cada mensaje |
| Percepción visual y principios de Gestalt | Mejora la comprensión y evita gráficos engañosos | Diseñar visualizaciones claras y honestas |
| Data storytelling | Convierte datos en narrativas que persuaden | Presentar resultados a tomadores de decisión |
| Teoría y psicología del color | El color comunica y guía la atención | Crear visualizaciones de alto impacto |
| Visualización espacial y temporal | Representa dinámicas geográficas y de tiempo | Mostrar evolución y distribución geográfica |
| Dashboards e indicadores (KPIs) | Centralizan la información clave del negocio | Construir tableros interactivos para seguimiento |

## 8. Big Data e Infraestructura

**Objetivo de la etapa:** escalar el análisis a grandes volúmenes de datos.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Fundamentos y arquitectura de Big Data (Data Lake) | Define cómo almacenar y organizar datos masivos | Diseñar la arquitectura de un proyecto de datos |
| Procesamiento distribuido (Hadoop, HDFS) | Permite procesar datos que no caben en una máquina | Ejecutar tareas sobre clústeres |
| Consultas sobre almacenamiento distribuido (Hive/HQL) | Facilita el acceso a datos masivos con lenguaje tipo SQL | Consultar grandes datasets de forma declarativa |
| Procesamiento en memoria (PySpark) | Acelera el análisis en tiempo casi real | Procesar grandes flujos de datos eficientemente |
| Bases de datos no estructuradas y cloud computing | Soportan datos diversos y escalan bajo demanda | Almacenar y escalar servicios en la nube |
| Ética y gobernanza de datos | Asegura un uso responsable, seguro y legal de los datos | Definir políticas de manejo y privacidad |

## 9. Gestión y Aplicación de Proyectos de Datos

**Objetivo de la etapa:** integrar todo lo aprendido en un proyecto que genere valor real.

| Qué estudiar | Por qué estudiarlo | Cómo aplicarlo |
|--------------|--------------------|----------------|
| Metodología CRISP-DM | Estructura el ciclo de vida de un proyecto de datos | Guiar un proyecto desde el problema hasta el despliegue |
| Gestión ágil y trabajo en equipo (sprints, roles) | Mejora la organización y entrega de valor | Coordinar un proyecto por iteraciones |
| Feature engineering aplicado | Las buenas variables determinan el éxito del modelo | Refinar el dataset para maximizar desempeño |
| Selección y validación de modelos (viabilidad, fiabilidad, re-entrenamiento) | Garantiza modelos útiles y sostenibles en producción | Decidir qué modelo desplegar y cuándo re-entrenarlo |
| Valor de negocio y evaluación de riesgos | Alinea la técnica con los objetivos de la organización | Justificar el impacto del proyecto |
| Prototipado interactivo y presentación de resultados | Hace tangible el valor para el usuario final | Entregar una solución usable y comprensible |

---

## Herramientas de aplicación

Tecnologías que soportan la práctica a lo largo del plan. Son medios para aplicar lo aprendido, no un fin en sí mismas.

| Área | Herramientas |
|------|--------------|
| Lenguaje y entornos | Python 3, R, Jupyter Notebook, Conda |
| Manipulación de datos | NumPy, pandas |
| Visualización | Matplotlib, Seaborn, Plotly, GeoPandas, Power BI, Streamlit |
| Machine / Deep Learning | Scikit-Learn, TensorFlow, Keras |
| Big Data | Hadoop, HDFS, Hive (HQL), PySpark, MongoDB |
| Colaboración y despliegue | Git, GitHub, SSH, cloud computing |

---

# Diccionario de Términos

Glosario de los conceptos clave del plan, con definiciones concisas.

## Fundamentos y procesos

- **Inteligencia Artificial (IA):** Campo que busca que las máquinas realicen tareas que requieren inteligencia humana, como aprender, razonar y reconocer patrones.
- **Ciencia de Datos:** Disciplina que combina estadística, programación y conocimiento de dominio para extraer conocimiento y valor a partir de datos.
- **Aprendizaje de Máquina (ML):** Conjunto de técnicas que permiten a los sistemas aprender patrones desde los datos sin ser programados explícitamente para cada tarea.
- **Minería de Datos:** Proceso de descubrir patrones, relaciones y conocimiento útil en grandes conjuntos de datos.
- **Análisis Exploratorio de Datos (EDA):** Fase inicial donde se resumen, visualizan y describen los datos para entender su estructura antes de modelar.
- **CRISP-DM:** Metodología estándar para el ciclo de vida de un proyecto de datos (comprensión del negocio, de los datos, preparación, modelado, evaluación y despliegue).
- **Ciclo de vida de un proyecto de ML:** Secuencia de etapas desde la definición del problema hasta el despliegue y re-entrenamiento del modelo.

## Datos y preprocesamiento

- **Calidad de datos:** Grado en que los datos son precisos, completos, consistentes y adecuados para su uso.
- **Valores faltantes (missing values):** Datos ausentes que deben tratarse, usualmente mediante imputación.
- **Imputación:** Técnica para reemplazar valores faltantes con estimaciones (media, mediana, modelos, etc.).
- **Valores atípicos (outliers):** Observaciones que se desvían notablemente del resto y pueden distorsionar el análisis.
- **Feature Engineering:** Proceso de crear, transformar y seleccionar variables para mejorar el desempeño de los modelos.
- **Reducción de dimensionalidad:** Técnicas para disminuir el número de variables conservando la información relevante.
- **PCA (Análisis de Componentes Principales):** Método que proyecta los datos en nuevas variables (componentes) que capturan la mayor varianza.
- **Maldición de la dimensionalidad:** Problemas que surgen cuando el número de variables es muy alto respecto al número de observaciones.
- **Normalización tf-idf:** Ponderación que mide la importancia de una palabra en un documento respecto a una colección.
- **Bag-of-words:** Representación de texto que cuenta la frecuencia de palabras ignorando el orden.
- **Word embeddings:** Representaciones vectoriales densas que capturan el significado semántico de las palabras.

## Estadística y probabilidad

- **Estadística descriptiva:** Métodos para resumir y describir las características de un conjunto de datos.
- **Medidas de tendencia central:** Valores que representan el centro de los datos (media, mediana, moda).
- **Medidas de dispersión:** Indican la variabilidad de los datos (varianza, desviación estándar, rango).
- **Covarianza / Correlación:** Medidas del grado y dirección de la relación entre dos variables.
- **Probabilidad condicional:** Probabilidad de un evento dado que otro ya ocurrió.
- **Teorema de Bayes:** Fórmula que actualiza la probabilidad de una hipótesis en función de nueva evidencia.
- **Distribución de probabilidad:** Función que describe cómo se reparten los valores de una variable aleatoria (Binomial, Normal, Poisson, etc.).
- **Teorema del Límite Central (TLC):** Establece que la distribución de las medias muestrales tiende a ser normal al aumentar el tamaño de muestra.
- **Intervalo de confianza:** Rango de valores plausibles para un parámetro poblacional con cierto nivel de confianza.
- **Bootstrap:** Técnica de remuestreo con reemplazo para estimar la distribución de un estadístico.
- **Prueba de hipótesis:** Procedimiento para decidir si rechazar o no una afirmación sobre un parámetro poblacional.
- **Error tipo I / tipo II:** Rechazar una hipótesis verdadera (I) o no rechazar una falsa (II).
- **ANOVA (Análisis de Varianza):** Técnica para comparar las medias de tres o más grupos.
- **Causalidad vs. Correlación:** La correlación mide asociación; la causalidad implica que una variable produce un efecto en otra.
- **d-separación:** Criterio en modelos causales para determinar independencia condicional entre variables en un grafo.

## Aprendizaje supervisado y no supervisado

- **Aprendizaje supervisado:** Entrenamiento con datos etiquetados para predecir una salida conocida.
- **Aprendizaje no supervisado:** Descubrimiento de estructura en datos sin etiquetas (p. ej. clustering).
- **Regresión:** Predicción de una variable continua a partir de otras variables.
- **Clasificación:** Asignación de observaciones a categorías o clases.
- **Regresión logística:** Modelo de clasificación que estima la probabilidad de pertenecer a una clase.
- **Función de costo:** Mide el error del modelo; se minimiza durante el entrenamiento.
- **Gradiente descendente:** Algoritmo de optimización que ajusta los parámetros siguiendo la dirección que reduce el costo.
- **Sobreajuste (overfitting):** El modelo memoriza el ruido del entrenamiento y generaliza mal.
- **Subajuste (underfitting):** El modelo es demasiado simple para capturar el patrón de los datos.
- **Regularización:** Técnica que penaliza la complejidad del modelo para reducir el sobreajuste.
- **Validación cruzada:** Método que divide los datos en varios pliegues para evaluar el modelo de forma robusta.
- **Matriz de confusión:** Tabla que resume aciertos y errores de un clasificador por clase.
- **Hiperparámetros:** Parámetros de configuración del modelo que no se aprenden del dato y se optimizan por búsqueda.
- **Árbol de decisión:** Modelo que divide los datos mediante reglas jerárquicas (ID3, CART).
- **SVM (Máquinas de Vectores de Soporte):** Clasificador que busca el hiperplano de margen máximo entre clases.
- **Kernel:** Función que permite a SVM separar datos no lineales proyectándolos a dimensiones superiores.
- **Métodos de ensamble:** Combinan varios modelos para mejorar el desempeño (bagging, random forest, votación).
- **Bagging:** Entrenamiento de múltiples modelos sobre muestras bootstrap y combinación de sus predicciones.
- **Random Forest:** Ensamble de árboles de decisión con aleatoriedad en datos y variables.
- **Clustering:** Agrupamiento de observaciones similares (K-means, jerárquico, DBSCAN).
- **K-means:** Algoritmo que agrupa datos en k clústeres minimizando la distancia al centroide.
- **DBSCAN:** Algoritmo de clustering basado en densidad, capaz de detectar ruido.
- **RFM:** Segmentación de clientes por Recencia, Frecuencia y Monto (Monetary).
- **One vs. All / Softmax:** Estrategias para extender la clasificación binaria a múltiples clases.

## Aprendizaje profundo (Deep Learning)

- **Red neuronal artificial:** Modelo inspirado en el cerebro, compuesto por capas de neuronas interconectadas.
- **Perceptrón / MLP (Multilayer Perceptron):** Red neuronal con una o varias capas ocultas totalmente conectadas.
- **Función de activación:** Función no lineal que determina la salida de una neurona (ReLU, sigmoide, etc.).
- **Propagación hacia adelante (forward pass):** Cálculo de la salida de la red a partir de la entrada.
- **Retropropagación (backpropagation):** Algoritmo que ajusta los pesos propagando el error hacia atrás.
- **CNN (Red Neuronal Convolucional):** Red especializada en datos con estructura espacial como imágenes.
- **Convolución / Filtros / Padding / Pooling:** Operaciones base de las CNN para extraer y resumir características.
- **Transferencia de aprendizaje:** Reutilización de un modelo preentrenado para una nueva tarea.
- **RNN (Red Neuronal Recurrente):** Red para datos secuenciales que mantiene estado entre pasos.
- **LSTM (Long Short-Term Memory):** RNN capaz de aprender dependencias de largo plazo.
- **GRU (Gated Recurrent Unit):** Variante simplificada de LSTM con menos parámetros.
- **Encoder-Decoder:** Arquitectura que codifica una secuencia de entrada y genera una secuencia de salida.

## Series temporales

- **Serie temporal:** Secuencia de observaciones ordenadas en el tiempo.
- **Tendencia:** Dirección general de largo plazo de una serie.
- **Estacionalidad:** Patrones que se repiten en intervalos regulares.
- **Estacionariedad:** Propiedad de una serie cuyas características estadísticas no cambian con el tiempo.
- **Autocorrelación:** Correlación de una serie con sus propios valores pasados.
- **Ruido blanco:** Serie de valores aleatorios sin patrón ni autocorrelación.
- **Random walk:** Serie donde cada valor depende del anterior más un cambio aleatorio.
- **AR / MA / ARMA / ARIMA / SARIMA:** Familia de modelos estadísticos de pronóstico (auto-regresivos, de media móvil y sus combinaciones con estacionalidad).
- **VAR / VARMA:** Modelos para pronóstico de múltiples series temporales relacionadas.
- **Forecasting:** Pronóstico de valores futuros de una serie.
- **Windowing / Shifting:** Técnicas para generar ventanas y desplazamientos usados como variables en forecasting.

## Visualización y Big Data

- **Visualización de datos:** Representación gráfica de datos para facilitar su comprensión.
- **Data Storytelling:** Técnica de comunicar hallazgos combinando datos, visuales y narrativa.
- **Principios de Gestalt:** Reglas de percepción visual que guían el diseño de gráficos efectivos.
- **Dashboard:** Tablero que agrupa visualizaciones e indicadores clave (KPIs).
- **KPI (Indicador Clave de Desempeño):** Métrica que mide el éxito respecto a un objetivo.
- **Big Data:** Conjuntos de datos tan grandes o complejos que requieren tecnologías especiales.
- **Data Lake:** Repositorio que almacena datos en bruto en su formato original.
- **Hadoop / HDFS:** Framework y sistema de archivos para procesamiento distribuido de Big Data.
- **Hive / HQL:** Herramienta y lenguaje tipo SQL para consultar datos en Hadoop.
- **PySpark:** API de Python para Apache Spark, procesamiento distribuido en memoria.
- **Gobernanza de datos:** Políticas y procesos para gestionar la disponibilidad, integridad y seguridad de los datos.

---

# Bibliografía por Fase de la Ruta

Libros citados en los sílabos, mapeados a la fase donde más te sirven. Marco con **(base)** los más fundamentales de cada fase y con **(profundización)** los opcionales para ir más lejos.

## Fase 1 — Programación y Manejo de Datos

- **(base)** Guttag, J. V. (2016). *Introduction to Computation and Programming Using Python*. MIT Press. — Fundamentos de programación orientados a datos.
- **(base)** McKinney, W. (2012). *Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython*. O'Reilly. — Referencia directa de pandas y NumPy (su autor creó pandas).
- Stephenson, B. (2016). *The Python Workbook*. Springer. — Práctica guiada de Python.
- Ascher, D. et al. (2001). *Numerical Python*. — Cómputo numérico con NumPy.
- Fonseca, P. (2026). *Python para Ciencia de Datos* (Draft). — Material introductorio en español.

## Fase 2 — Estadística y Probabilidad

- **(base)** Diez, D., Çetinkaya-Rundel, M. & Barr, C. (2019). *OpenIntro Statistics* (4th ed.). — Introducción clara a estadística e inferencia (gratuito).
- **(base)** Anderson, D. R. et al. (2017). *Statistics for Business & Economics*. Cengage. — Estadística aplicada a decisiones.
- Devore, J. L. & Berk, K. N. (2012). *Modern Mathematical Statistics with Applications*. Springer. — Base matemática más formal.
- Buglear, J. (2001). *Stats Means Business*. Elsevier. — Estadística orientada a negocio.
- Ekstrom, C. T. (2016). *The R Primer* (2nd ed.). — Si decides practicar estadística en R.
- **(profundización)** Fenton, N. & Neil, M. (2019). *Risk Assessment and Decision Analysis with Bayesian Networks*. CRC Press. — Para la parte de causalidad y riesgo.
- **(profundización)** Pearl, J. (2018). *The Book of Why*. Basic Books. — Causalidad vs. correlación (Judea Pearl).

## Fase 3 — Análisis Exploratorio y Preprocesamiento

- **(base)** Irizarry, R. A. (2020). *Introduction to Data Science*. — EDA de principio a fin (gratuito en línea).
- Skiena, S. S. (2017). *The Data Science Design Manual*. Springer. — Panorama de todo el proceso de análisis.
- Downey, A. B. (2014). *Think Stats: Exploratory Data Analysis in Python*. Green Tea Press. — EDA práctico en Python (también útil en Fase 2).

## Fase 4 — Aprendizaje de Máquina

- **(base)** Géron, A. (2019). *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow*. O'Reilly. — El libro práctico de referencia; cubre fases 4 y 5.
- **(base)** VanderPlas, J. (2016). *Python Data Science Handbook*. O'Reilly. — Puente entre pandas, visualización y Scikit-Learn.
- Kelleher, J. D. et al. (2015). *Fundamentals of Machine Learning for Predictive Data Analytics*. MIT Press. — ML con casos trabajados.
- **(profundización)** Bishop, C. (2006). *Pattern Recognition and Machine Learning*. Springer. — Teoría rigurosa.
- **(profundización)** Murphy, K. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press. — Enfoque probabilístico avanzado.
- **(profundización)** Hastie, T., Tibshirani, R. & Friedman, J. (2001). *The Elements of Statistical Learning*. Springer. — Clásico que une estadística y ML.
- Duda, R., Hart, P. & Stork, D. (2001). *Pattern Classification*. Wiley. — Clasificación de patrones.
- Witten, I. H. & Frank, E. (2005). *Data Mining: Practical Machine Learning Tools and Techniques*. Morgan Kaufmann. — ML aplicado a minería de datos.

## Fase 5 — Aprendizaje Profundo

- **(base)** Géron, A. (2019). *Hands-On Machine Learning...* (parte de Deep Learning con Keras/TensorFlow). — Continúa desde la Fase 4.
- Torres, J. (2020). *Python Deep Learning: Introducción práctica con Keras y TensorFlow 2*. Marcombo. — En español, muy práctico.
- Véliz, C. (2020). *Aprendizaje automático: Introducción al aprendizaje profundo*. Fondo Editorial PUCP. — Introducción en español.

## Fase 6 — Series Temporales

- **(base)** Nielsen, A. (2020). *Practical Time Series Analysis: Prediction with Statistics and Machine Learning*. — Cubre modelos estadísticos y de ML.
- Pal, A. & Prakash, PKS (2017). *Practical Time-Series Analysis* (Python). Packt. — Procesamiento, visualización y modelado en Python.
- Mather, B. (2020). *Time Series with Python*. — Implementación práctica de forecasting.

## Fase 7 — Visualización y Comunicación

- **(base)** Nussbaumer, C. (2015). *Storytelling with Data*. Wiley. — Referencia de data storytelling.
- **(base)** Few, S. (2006). *Information Dashboard Design*. O'Reilly. — Diseño de dashboards efectivos.
- Wexler, S., Shaffer, J. & Cotgreave, A. (2017). *The Big Book of Dashboards*. Wiley. — Catálogo de dashboards reales.
- Mazza, R. (2004). *Introduction to Information Visualization*. — Fundamentos del área.
- Fry, B. (2008). *Visualizing Data*. O'Reilly. — Visualización programática.
- Dale, K. (2016). *Data Visualization with Python and JavaScript*. O'Reilly. — Visualización con código.
- Chen, C., Härdle, W. & Unwin, A. (2008). *Handbook of Data Visualization*. Springer. — Referencia amplia.
- Sosulski, K. (2019). *Data Visualization Made Simple*. Taylor & Francis. — Introducción accesible.

## Fase 8 — Big Data e Infraestructura

- **(base)** Dasgupta, N. (2018). *Practical Big Data*. Packt. — Fundamentos y arquitectura de Big Data.
- Miller, J. D. (2017). *Big Data Visualization*. Packt. — Visualización a escala (enlaza con Fase 7).
- **(profundización)** O'Neil, C. (2018). *Armas de destrucción matemática*. Capitán Swing. — Ética y riesgos del Big Data.

## Fase 9 — Gestión y Aplicación de Proyectos

- **(base)** Fishman, N. *Smarter Data Science: Succeeding with Enterprise-Grade Data and AI Projects*. Wiley. — Gestión de proyectos de datos con enfoque de valor.
- Bull, P. et al. (2017). *Prescriptive Analytics for Business Leaders*. — Analítica orientada a decisiones de negocio.
- Boyd, S. & Vandenberghe, L. (2018). *Introduction to Applied Linear Algebra*. Cambridge. — Álgebra lineal aplicada (base transversal útil desde la Fase 1).

---

**Sugerencia de uso:** empieza cada fase por los libros marcados **(base)** y reserva los de **(profundización)** para cuando quieras consolidar la teoría o especializarte. Géron (*Hands-On ML*) y VanderPlas (*Python Data Science Handbook*) son los que más fases cruzan, así que son buenas inversiones tempranas.

---

# Recursos Online por Fase

Cursos, documentación oficial, libros gratuitos y plataformas de práctica. Marco con **(gratis)** los de acceso libre.

## Transversales (útiles en toda la ruta)

- **(gratis)** [Kaggle](https://www.kaggle.com/) — Datasets, notebooks y competencias para practicar en cualquier fase.
- **(gratis)** [Kaggle Learn](https://www.kaggle.com/learn) — Micro-cursos cortos y prácticos (Python, Pandas, ML, visualización, etc.).
- **(gratis)** [Google Colab](https://colab.research.google.com/) — Entorno de notebooks gratuito con GPU.
- **(gratis)** [freeCodeCamp](https://www.freecodecamp.org/learn/) — Rutas gratuitas de programación y análisis de datos.

## Fase 1 — Programación y Manejo de Datos

- **(gratis)** [Documentación oficial de Python](https://docs.python.org/3/) y [tutorial oficial](https://docs.python.org/3/tutorial/).
- **(gratis)** [Documentación de pandas](https://pandas.pydata.org/docs/) y [guía "10 minutes to pandas"](https://pandas.pydata.org/docs/user_guide/10min.html).
- **(gratis)** [Documentación de NumPy](https://numpy.org/doc/stable/) y su [tutorial para principiantes](https://numpy.org/doc/stable/user/absolute_beginners.html).
- **(gratis)** [Pro Git (libro oficial)](https://git-scm.com/book/es/v2) — Control de versiones, disponible en español.
- [Python for Everybody (Coursera / Dr. Chuck)](https://www.coursera.org/specializations/python) — Introducción muy accesible (auditable gratis).

## Fase 2 — Estadística y Probabilidad

- **(gratis)** [OpenIntro Statistics](https://www.openintro.org/book/os/) — El libro de la bibliografía, con PDF gratuito, labs y videos.
- **(gratis)** [Introduction to Modern Statistics (OpenIntro)](https://openintro-ims.netlify.app/) — Versión más moderna y computacional.
- **(gratis)** [Seeing Theory (Brown University)](https://seeing-theory.brown.edu/) — Probabilidad y estadística visual e interactiva.
- **(gratis)** [StatQuest con Josh Starmer (YouTube)](https://www.youtube.com/@statquest) — Explicaciones visuales de estadística y ML, muy recomendadas.
- **(gratis)** [Khan Academy — Estadística y probabilidad](https://es.khanacademy.org/math/statistics-probability) — En español.

## Fase 3 — Análisis Exploratorio y Preprocesamiento

- **(gratis)** [Introduction to Data Science (Rafael Irizarry)](https://rafalab.dfci.harvard.edu/dsbook/) — El libro de la bibliografía, en línea.
- **(gratis)** [Think Stats (Allen Downey)](https://greenteapress.com/wp/think-stats-2e/) — EDA en Python, gratuito.
- **(gratis)** [Kaggle — Data Cleaning](https://www.kaggle.com/learn/data-cleaning) y [Pandas](https://www.kaggle.com/learn/pandas).
- **(gratis)** [NLTK Book](https://www.nltk.org/book/) — Procesamiento de texto en Python.

## Fase 4 — Aprendizaje de Máquina

- **(gratis)** [Machine Learning Specialization (Andrew Ng, DeepLearning.AI + Stanford)](https://www.coursera.org/specializations/machine-learning-introduction) — El curso introductorio de referencia (auditable gratis).
- **(gratis)** [Documentación y tutoriales de Scikit-Learn](https://scikit-learn.org/stable/user_guide.html) — Guía de usuario y ejemplos.
- **(gratis)** [Notebooks del libro de Géron (Hands-On ML)](https://github.com/ageron/handson-ml3) — Código del libro de la bibliografía.
- **(gratis)** [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — Con ejercicios interactivos.
- [fast.ai — Practical Deep Learning](https://course.fast.ai/) — Enfoque práctico (también aplica a Fase 5).

## Fase 5 — Aprendizaje Profundo

- **(gratis)** [Deep Learning Specialization (Andrew Ng)](https://www.coursera.org/specializations/deep-learning) — Redes neuronales, CNN, RNN (auditable gratis).
- **(gratis)** [Tutoriales oficiales de TensorFlow/Keras](https://www.tensorflow.org/tutorials) y [Keras](https://keras.io/examples/).
- **(gratis)** [Dive into Deep Learning (d2l.ai)](https://d2l.ai/) — Libro interactivo con código.
- **(gratis)** [3Blue1Brown — Neural Networks (YouTube)](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) — Intuición visual del Deep Learning.

## Fase 6 — Series Temporales

- **(gratis)** [Forecasting: Principles and Practice (Hyndman & Athanasopoulos)](https://otexts.com/fpp3/) — Referencia abierta del área (en R).
- **(gratis)** [Documentación de statsmodels — Time Series](https://www.statsmodels.org/stable/tsa.html) — ARIMA, SARIMA, VAR en Python.
- **(gratis)** [Kaggle — Time Series](https://www.kaggle.com/learn/time-series) — Micro-curso práctico.
- **(gratis)** [Documentación de Prophet (Meta)](https://facebook.github.io/prophet/) — Herramienta de forecasting popular.

## Fase 7 — Visualización y Comunicación

- **(gratis)** [Documentación de Matplotlib](https://matplotlib.org/stable/tutorials/index.html), [Seaborn](https://seaborn.pydata.org/tutorial.html) y [Plotly](https://plotly.com/python/).
- **(gratis)** [From Data to Viz](https://www.data-to-viz.com/) — Ayuda a elegir el gráfico correcto según los datos.
- **(gratis)** [The Python Graph Gallery](https://python-graph-gallery.com/) — Catálogo de gráficos con código.
- **(gratis)** [Microsoft Learn — Power BI](https://learn.microsoft.com/training/powerbi/) — Formación oficial de Power BI.
- **(gratis)** [Documentación de Streamlit](https://docs.streamlit.io/) — Para construir apps de datos.

## Fase 8 — Big Data e Infraestructura

- **(gratis)** [Documentación de Apache Spark / PySpark](https://spark.apache.org/docs/latest/api/python/) — Guía oficial.
- **(gratis)** [Documentación de Apache Hadoop](https://hadoop.apache.org/docs/stable/) y [Apache Hive](https://cwiki.apache.org/confluence/display/Hive/Home).
- **(gratis)** [MongoDB University](https://learn.mongodb.com/) — Cursos gratuitos oficiales de MongoDB.
- **(gratis)** [AWS Skill Builder](https://skillbuilder.aws/) / [Google Cloud Skills Boost](https://www.cloudskillsboost.google/) — Formación en cloud computing.

## Fase 9 — Gestión y Aplicación de Proyectos

- **(gratis)** [Guía oficial de CRISP-DM (IBM)](https://www.ibm.com/docs/en/spss-modeler/saas?topic=dm-crisp-help-overview) — Metodología paso a paso.
- **(gratis)** [Documentación de conda](https://docs.conda.io/projects/conda/en/stable/user-guide/) — Gestión de entornos y paquetes.
- **(gratis)** [Jupyter — documentación oficial](https://docs.jupyter.org/) — Notebooks y despliegue local.
- **(gratis)** [DrivenData — competencias con impacto social](https://www.drivendata.org/) — Proyectos reales para tu portafolio.
- **(gratis)** [Papers with Code](https://paperswithcode.com/) — Estado del arte con implementaciones para inspirar proyectos.

---

*Nota: los enlaces apuntan a sitios oficiales y recursos abiertos ampliamente usados. Algunos cursos de Coursera pueden auditarse gratis (sin certificado). Verifica disponibilidad y versión actual al acceder.*
