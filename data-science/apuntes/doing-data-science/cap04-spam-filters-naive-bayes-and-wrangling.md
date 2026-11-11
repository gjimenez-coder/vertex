# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 4 — Spam Filters, Naive Bayes, and Wrangling (Filtros de spam, Naive Bayes y manipulación de datos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El ponente invitado es Jake Hofman (Microsoft Research, antes Yahoo! Research; doctor en física por Columbia), que aportó a la clase de Rachel Schutt el perfil de "data wrangling" (manipulación de datos). El capítulo usa el problema de filtrar spam en el correo para introducir la clasificación con Naive Bayes y, de paso, las tareas prácticas de obtener y limpiar datos reales.

La tesis central es que, aunque linear regression y k-nearest neighbors (k-NN) son herramientas ya conocidas, ninguna encaja bien en el filtrado de spam; Naive Bayes, mucho más simple, funciona sorprendentemente bien. El capítulo deriva Naive Bayes desde la ley de Bayes, muestra cómo entrenarlo contando palabras y lo complementa con Laplace Smoothing para evitar probabilidades de 0 o 1.

Sales sabiendo por qué fallan regresión lineal y k-NN en este caso, cómo construir un filtro Naive Bayes contando palabras (con un ejemplo real sobre los correos de Enron), qué es el suavizado de Laplace y sus hiperparámetros, y cómo conseguir datos de la web con APIs y herramientas de scraping (parte "wrangling").

## El ejemplo que recorre el capítulo

El hilo conductor es construir un filtro de spam. Se parte de un experimento mental —mirar asuntos de correos y reconocer a ojo cuáles parecen spam— y se avanza hasta implementar Naive Bayes sobre el corpus público de correos de Enron, usando su propia definición de spam para entrenar.

## Experimento mental: aprender con ejemplos

Al ver asuntos y primeras líneas de correos, el lector detecta spam de forma intuitiva. La clase de Rachel propuso señales: la presencia de "Viagra" (regla fácil que los spammers burlan cambiando la ortografía), la longitud del asunto o el uso excesivo de signos de exclamación —aunque palabras legítimas como "Yahoo!" complican reglas demasiado simples—.

Sobre qué código escribir, surgieron dos ideas: un modelo probabilístico que agregue muchas reglas de pulgar para dar la probabilidad de que un correo sea spam (buena idea), y usar k-NN o linear regression (la respuesta es "no"). El capítulo usará Naive Bayes, que queda en un punto intermedio.

## Por qué linear regression no sirve para filtrar spam

Imagina una matriz donde cada fila es un correo (keyed por `email_id`) y cada columna es una palabra: 1 si la palabra aparece, 0 si no (o el número de apariciones). Para regresión lineal necesitaríamos un conjunto de entrenamiento ya etiquetado como spam/no spam, etiquetado por humanos o reutilizando los labels de un filtro existente (p. ej. Gmail).

Los problemas: el objetivo es binario (0/1) y la regresión lineal modela salidas continuas, así que no es el modelo adecuado. Además, hay demasiadas variables frente a observaciones —del orden de 10.000 correos y 100.000 palabras—, lo que hace que la matriz de la ecuación no sea invertible, ni siquiera cercana, y quizá ni se pueda almacenar. Limitar a las 10.000 o incluso 100 palabras principales (con feature selection y conocimiento del dominio) resuelve la invertibilidad, pero sigue sin ser el modelo apropiado para una salida binaria.

Aparte (estado del arte): en los últimos cinco años se empezaron a usar métodos de gradiente estocástico para evitar el sobreajuste de la matriz no invertible; pasar a logistic regression con gradiente estocástico ayuda mucho y capta correlaciones entre palabras. Aun así, Naive Bayes es impresionantemente bueno para lo simple que es.

## ¿Y k-nearest neighbors?

Con k-NN también elegiríamos features por palabra (0/1 según presencia) y definiríamos cuándo dos correos están "cerca" según las palabras que comparten. Con 10.000 correos y 100.000 palabras surge otro problema: el espacio tiene demasiadas dimensiones. Calcular distancias en 100.000 dimensiones es costoso, pero el problema real es más básico: incluso los vecinos más cercanos están muy lejos. Esto es la "maldición de la dimensionalidad" (curse of dimensionality) y hace a k-NN una mala opción aquí.

Aparte (reconocimiento de dígitos): k-NN sí funciona bien para reconocer dígitos manuscritos. Se toma cada imagen píxel a píxel (rejilla 16×16), se mide el brillo, se despliega en un espacio de 256 dimensiones con métrica arquimediana (distancia = raíz de la suma de cuadrados de las diferencias) y se aplica k-NN. Variando el número de vecinos cambia la frontera y se ajusta k para evitar overfitting; con bastantes datos se puede alcanzar 97% de accuracy. El resultado se resume en una confusion matrix, matriz k×k de etiqueta real frente a predicha cuyo elemento (i, j) cuenta los ítems de clase real i predichos como j. De ahí se obtiene la accuracy (proporción de aciertos), con accuracy = 1 − tasa de misclasificación.

## Naive Bayes

Naive Bayes es otro método de clasificación que escala bien y resulta intuitivo. Para captar la idea, un ejemplo con una enfermedad rara: 1% de la población infectada, test con 99% de sensibilidad (99% de los enfermos dan positivo) y 99% de especificidad (99% de los sanos dan negativo). Sobre 10.000 personas representativas, 100 enfermas y 9.900 sanas: 99 enfermos dan positivo, pero también 99 sanos. Así que dar positivo deja al paciente igual de probable sano o enfermo: la respuesta es 50%.

En notación, a partir de probabilidades conjuntas y condicionales se obtiene la ley de Bayes: `p(y|x) = p(x|y)·p(y) / p(x)`, donde el denominador `p(x)` actúa como constante de normalización. Con y = "estar enfermo" y x = "test positivo":

```
p(sick|+) = 0.99·0.01 / (0.99·0.01 + 0.01·0.99) = 0.50 = 50%
```

### Filtro de spam para una sola palabra

Para una palabra genérica: `p(spam|word) = p(word|spam)·p(spam) / p(word)`. Llamando "ham" al no-spam, basta calcular `p(word|spam)`, `p(word|ham)`, `p(spam)` y `p(ham) = 1 − p(spam)`; el denominador sale de `p(word) = p(word|spam)·p(spam) + p(word|ham)·p(ham)`. Todo se reduce a un ejercicio de contar.

Con los correos públicos de Enron (usando su definición de spam, de 2001), un script en bash descarga y separa spam y ham en carpetas. Para un empleado: 1.500 spam y 3.672 ham. Contando la palabra "meeting":

```
grep -il meeting enron1/spam/*.txt | wc -l   # 16 (y 153 en ham)

p(spam)=1500/(1500+3672)=.29   p(ham)=.71
p(meeting|spam)=16/1500=.0106  p(meeting|ham)=153/3672=.0416
p(spam|meeting)= .0106·.29 / (.0106·.29 + .0416·.71) = 0.09 = 9%
```

Otras palabras dan "money" 80%, "viagra" 100%, "enron" 0%. Esto evidencia overfitting por datos sesgados: no es seguro que todo correo con "Viagra" sea spam, ni que uno con "Enron" nunca lo sea.

### Filtro que combina palabras: Naive Bayes

Cada correo se representa como un vector binario x con entrada 1/0 según aparezca cada palabra (en la práctica se guardan solo los índices de las palabras presentes). El modelo da la probabilidad de ver ese vector dado que es spam (o ham): `p(x|c) = ∏_j θ_jc^{x_j} (1−θ_jc)^{1−x_j}`, donde θ es la probabilidad de que una palabra aparezca en spam, calculada contando. Se llama "naive" porque modela las palabras como independientes (independent trials) e ignora que ciertas palabras suelen aparecer juntas.

Tomando logaritmos (truco estándar para evitar problemas numéricos al multiplicar números diminutos), se llega a `log p(x|c) = ∑_j x_j·w_j + w0`, con `w_j = log(θ_j/(1−θ_j))` y `w0 = ∑_j log(1−θ_j)` precomputados por palabra. Luego, con la ley de Bayes, se estima `p(c|x)`. Si solo importa decidir spam vs. ham, basta computar el término variable. El resultado se parece a una regresión lineal, pero los pesos `w_j` vienen de Naive Bayes en vez de invertir una matriz enorme. Es barato de entrenar (básicamente contar) e incremental con más datos. En producción hay un modelo global que se personaliza por usuario, con reglas rápidas hardcodeadas antes del modelo fino y lento.

## Suavizado: Laplace Smoothing

θ_j es un cociente de conteos `θ_j = n_jc / n_c`. El suavizado de Laplace lo reemplaza por `θ_jc = (n_jc + α) / (n_c + β)`, fijando por ejemplo α = 1 y β = 10 para evitar probabilidades de 0 o 1 (como el 100% de "viagra"). No es ad hoc: equivale a usar un prior y hacer estimación por máxima verosimilitud. El estimador de máxima verosimilitud (ML), bajo independencia, recupera `θ_j = n_jc / n_c`. Al añadir un prior y buscar el máximo a posteriori (MAP), si se asume que θ se distribuye como θ^α (1−θ)^β, se recupera el resultado suavizado.

¿Es razonable? Con α > 0 y β > 0 la distribución se anula en 0 y 1 (pocas palabras nunca o siempre en spam), lo cual es razonable; pero con α y β grandes se concentra en el medio (todas las palabras igual de probables en spam o no), lo que tampoco es cierto. Un compromiso es α y β pequeños pero positivos, como 1/5, relajables cuando hay más y mejores datos (los priors fuertes solo hacen falta con pocos datos).

## Comparación de Naive Bayes y k-NN

A α y β se les llama "pseudocounts" o hiperparámetros: dos perillas que ajusta el data scientist, frente a la única perilla de k-NN (el número de vecinos k). Naive Bayes es un clasificador lineal; k-NN no. La maldición de la dimensionalidad y los grandes conjuntos de features perjudican a k-NN, mientras Naive Bayes rinde bien. k-NN no requiere entrenamiento (solo cargar los datos); Naive Bayes sí. Ambos son aprendizaje supervisado (datos etiquetados). El capítulo incluye código bash de ejemplo (`enron_naive_bayes.sh`) que entrena un filtro de una palabra con los datos de Enron.

## Scraping de la web: APIs y otras herramientas

El data scientist a menudo debe conseguir los datos por su cuenta (parte "wrangling"). Una vía son las APIs (application programming interface), que los sitios ofrecen para descargar datos en formato estándar; suele hacer falta registrarse y obtener una "key" (p. ej. la API del New York Times). Advertencia: revisa siempre los términos y servicios de la API antes de scrapear, y ten en cuenta límites de acceso o de frecuencia sin pago.

Los formatos devueltos varían (a veces JSON), sin una estandarización real. El YQL de Yahoo! permite escribir consultas tipo SQL contra muchas APIs (`select * from flickr.photos.search where text="Cat" ...`) y parsear un formato estándar una sola vez en Python. Si no hay API, la extensión Firebug de Firefox permite "inspeccionar el elemento" y ver el HTML como un mapa de la página. Localizado lo que se quiere, se usan curl, wget, grep, awk, perl, etc. para un script rápido, o Python/R para algo más sistemático. Otras herramientas de parsing mencionadas: lynx y `lynx --dump`, Beautiful Soup (robusto pero lento), Mechanize (no parsea JavaScript) y PostScript (clasificación de imágenes).

## Experimento mental: reconocimiento de imágenes

¿Cómo saber si una imagen es un paisaje o un retrato? Primero reunir datos: etiquetar a mano (mucho trabajo) o tomar fotos ya etiquetadas de flickr. Cada imagen se representa con un histograma binado de intensidad RGB: para cada píxel y cada color (rojo, verde, azul) se mide la intensidad (0 a 255). Con un histograma binado (p. ej. conteos de píxeles de intensidad 0–51, etc.) resultan 15 números por imagen (3 colores × 5 bins), asumiendo que todas tienen igual número de píxeles. Finalmente se usa k-NN para decidir cuánto "azul" hace un paisaje frente a un retrato, ajustando los hiperparámetros (número de bins y k).

## Ejercicio de Jake: Naive Bayes para clasificar artículos

Aplicación multiclase: usar la Article Search API del New York Times Developer para bajar los 2.000 artículos más recientes de las secciones Arts, Business, Obituaries, Sports y World (facet `nytd_section_facet`), guardándolos en formato tab-delimited (URL, título, cuerpo). Luego entrenar un Bernoulli Naive Bayes: documentos de C categorías, etiqueta `y_i ∈ {0,1,...,C}` (Arts = 0, Business = 1, etc.) y matriz binaria dispersa X. Se estiman `θ_jc = (n_jc + α − 1)/(n_c + α + β − 2)` y `θ_c = n_c/n`, y se calculan log-odds por clase respecto a la base c = 0 sumando pesos `w_jc` y sesgo `w0c`. El código debe tokenizar, quitar puntuación y stop words. Se evalúa con un split aleatorio 50/50 (accuracy y runtime), una tabla de confusión 5×5, las 10 palabras más informativas por sección y los 10 artículos "más difíciles de clasificar", comentando el efecto de α y β y la generalización a otras fuentes o periodos. Se incluye código R de Jared Lander para llamar a la API del NYT (paquetes rjson, plyr, RTextTools) y construir la document-term matrix.

## Contexto histórico: procesamiento de lenguaje natural

El caso de datos en texto es la punta del iceberg del natural language processing (NLP), campo cuyos problemas incluyen traducción automática, análisis semántico, etiquetado de partes del habla y clasificación de documentos (el spam es un ejemplo). La investigación en estas áreas se remonta a los años 50.

## Ideas clave

- Linear regression no sirve para spam: salida binaria frente a continua y matriz no invertible por tener muchas más palabras (features) que correos.
- k-NN tampoco encaja: la maldición de la dimensionalidad hace que incluso los vecinos más cercanos estén lejos (aunque sí funciona para dígitos manuscritos).
- Naive Bayes deriva de la ley de Bayes `p(y|x) = p(x|y)·p(y)/p(x)` y el ejemplo del test médico ilustra por qué un positivo puede dar solo 50% de probabilidad de enfermedad.
- El filtro se entrena contando palabras en spam y ham (ejemplo real con los correos de Enron) y combina palabras asumiéndolas independientes, de ahí "naive".
- Tomar logaritmos convierte el producto en suma y evita problemas numéricos; el modelo acaba pareciéndose a una regresión lineal pero con pesos obtenidos por conteo.
- Laplace Smoothing `θ_jc = (n_jc + α)/(n_c + β)` evita probabilidades de 0 o 1; α y β son pseudocounts/hiperparámetros equivalentes a un prior.
- Naive Bayes es un clasificador lineal con dos perillas (α, β), barato e incremental; k-NN no requiere entrenamiento pero tiene una sola perilla (k). Ambos son aprendizaje supervisado.
- El "wrangling" incluye obtener datos con APIs (con cuidado de sus términos) y herramientas de scraping como YQL, Firebug, curl/wget, Beautiful Soup o Mechanize.
