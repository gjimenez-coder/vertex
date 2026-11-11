# Spam Filters, Naive Bayes, and Wrangling (Filtros de spam, Naive Bayes y manipulación de datos) — Estudio

## Tarjetas de repaso

P: ¿Por qué linear regression no sirve para filtrar spam?
R: El objetivo es binario (0/1) y la regresión lineal modela salidas continuas; además hay muchas más palabras (features) que correos, lo que hace que la matriz no sea invertible ni almacenable.

P: ¿Por qué k-NN no encaja en el filtrado de spam?
R: Con ~10.000 correos y ~100.000 palabras el espacio tiene demasiadas dimensiones; por la maldición de la dimensionalidad (curse of dimensionality) incluso los vecinos más cercanos están muy lejos.

P: ¿Para qué problema sí funciona bien k-NN según el capítulo?
R: Para reconocer dígitos manuscritos: cada imagen se despliega en 256 dimensiones (rejilla 16×16) con métrica arquimediana y se puede alcanzar 97% de accuracy.

P: ¿Qué es una confusion matrix?
R: Una matriz k×k de etiqueta real frente a predicha cuyo elemento (i, j) cuenta los ítems de clase real i predichos como j; de ella se obtiene la accuracy.

P: ¿Cómo se define la accuracy en el capítulo?
R: La proporción de aciertos, con accuracy = 1 − tasa de misclasificación.

P: ¿Cuál es la ley de Bayes usada para derivar Naive Bayes?
R: p(y|x) = p(x|y)·p(y) / p(x), donde p(x) actúa como constante de normalización.

P: En el ejemplo del test médico (1% infectados, 99% sensibilidad y especificidad), ¿qué probabilidad de enfermedad da un positivo?
R: 50%, porque sobre 10.000 personas 99 enfermos dan positivo pero también 99 sanos.

P: ¿Cómo se entrena un filtro Naive Bayes de una sola palabra?
R: Contando: se calculan p(word|spam), p(word|ham), p(spam) y p(ham)=1−p(spam), y el denominador p(word)=p(word|spam)·p(spam)+p(word|ham)·p(ham).

P: ¿Por qué el método se llama "naive"?
R: Porque modela las palabras como independientes (independent trials) e ignora que ciertas palabras suelen aparecer juntas.

P: ¿Para qué se toman logaritmos en Naive Bayes?
R: Es un truco estándar para evitar problemas numéricos al multiplicar números diminutos; convierte el producto en suma y el modelo acaba pareciéndose a una regresión lineal.

P: ¿Qué es el Laplace Smoothing y qué fórmula usa?
R: Reemplaza θ_j = n_jc/n_c por θ_jc = (n_jc + α)/(n_c + β) para evitar probabilidades de 0 o 1; α y β son pseudocounts/hiperparámetros equivalentes a un prior.

P: ¿Qué relación tienen el suavizado con los estimadores ML y MAP?
R: El estimador de máxima verosimilitud recupera θ_j = n_jc/n_c; al añadir un prior y buscar el máximo a posteriori (MAP) se recupera el resultado suavizado.

P: ¿Qué diferencias clave hay entre Naive Bayes y k-NN?
R: Naive Bayes es un clasificador lineal con dos perillas (α, β), requiere entrenamiento y rinde bien en alta dimensión; k-NN no es lineal, tiene una sola perilla (k) y no requiere entrenamiento. Ambos son aprendizaje supervisado.

P: ¿Qué herramientas de scraping y obtención de datos menciona el capítulo?
R: APIs (con su "key" y términos), YQL de Yahoo!, la extensión Firebug, curl/wget/grep/awk/perl, lynx y lynx --dump, Beautiful Soup y Mechanize.

## Preguntas de autoevaluación

P: ¿Qué dos ideas de código surgieron en el experimento mental y cuál eligió el capítulo?
R: Un modelo probabilístico que agrega reglas de pulgar (buena idea) y usar k-NN o linear regression (no); el capítulo usa Naive Bayes, un punto intermedio. (Sección: Experimento mental: aprender con ejemplos.)

P: Con los datos de Enron, ¿por qué el 100% de "viagra" y el 0% de "enron" evidencian un problema?
R: Evidencian overfitting por datos sesgados: no es seguro que todo correo con "Viagra" sea spam ni que uno con "Enron" nunca lo sea. (Sección: Filtro de spam para una sola palabra.)

P: ¿Cómo se representa un correo en el filtro Naive Bayes que combina palabras?
R: Como un vector binario x con 1/0 según aparezca cada palabra (en la práctica se guardan solo los índices de las presentes). (Sección: Filtro que combina palabras: Naive Bayes.)

P: ¿Por qué un α y β grandes no son razonables en el suavizado?
R: Con α y β grandes la distribución se concentra en el medio, implicando que todas las palabras son igual de probables en spam o no, lo que no es cierto; un compromiso es α y β pequeños pero positivos. (Sección: Suavizado: Laplace Smoothing.)

P: ¿Cómo se representa una imagen para decidir si es paisaje o retrato con k-NN?
R: Con un histograma binado de intensidad RGB: 3 colores × 5 bins = 15 números por imagen, asumiendo igual número de píxeles. (Sección: Experimento mental: reconocimiento de imágenes.)

P: ¿En qué consiste el ejercicio de Jake con la API del New York Times?
R: Bajar los 2.000 artículos más recientes de 5 secciones, entrenar un Bernoulli Naive Bayes multiclase, evaluar con split 50/50, tabla de confusión 5×5, las 10 palabras más informativas por sección y los 10 artículos más difíciles. (Sección: Ejercicio de Jake: Naive Bayes para clasificar artículos.)

P: ¿Qué precaución se da antes de scrapear una API?
R: Revisar siempre los términos y servicios de la API y tener en cuenta límites de acceso o de frecuencia sin pago. (Sección: Scraping de la web: APIs y otras herramientas.)

P: ¿Dónde se enmarca el filtrado de spam dentro del NLP?
R: Es un ejemplo de clasificación de documentos, uno de los problemas del natural language processing, cuya investigación se remonta a los años 50. (Sección: Contexto histórico: procesamiento de lenguaje natural.)

## Checklist

Puntos a dominar:

- Explicar por qué linear regression y k-NN fallan en el filtrado de spam (salida binaria, matriz no invertible, maldición de la dimensionalidad).
- Derivar Naive Bayes desde la ley de Bayes y resolver el ejemplo del test médico (resultado 50%).
- Construir un filtro Naive Bayes de una sola palabra contando apariciones en spam y ham (ejemplo de Enron).
- Entender el filtro que combina palabras: vector binario, supuesto de independencia ("naive") y paso a logaritmos.
- Aplicar Laplace Smoothing y justificar α y β como pseudocounts/prior, relacionándolos con ML y MAP.
- Comparar Naive Bayes y k-NN: linealidad, perillas (α, β vs. k), necesidad de entrenamiento y aprendizaje supervisado.
- Conocer las vías de "wrangling": APIs con key y términos, YQL, Firebug, curl/wget, Beautiful Soup, Mechanize.
