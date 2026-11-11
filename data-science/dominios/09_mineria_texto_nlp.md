# 09 · Minería de Texto y NLP

Cómo convertir texto no estructurado (reseñas, correos, tickets, noticias, redes) en algo que los modelos puedan usar, y qué técnicas aplicar después. El reto central es que **el texto no viene como un vector de atributos**: es secuencial, sucio y de altísima dimensionalidad. La estrategia base es *ingeniar la representación* para que encaje en las herramientas que ya conocemos.

> **Idea rectora (Provost & Fawcett):** *"Si queremos aplicar las herramientas de minería que tenemos, debemos o ingeniar la representación de los datos para que encaje con las herramientas, o construir herramientas nuevas."* Casi siempre conviene lo primero. Empieza simple (bolsa de palabras) y añade complejidad solo si mejora el resultado.

> Fuentes: *Data Science for Business* cap. 10 (fundamentos de representación) y *Natural Language Processing with Python* / NLTK (stack práctico).

---

## 1. Por qué el texto es importante y difícil

- **Ubicuo y valioso:** web, correo, reseñas, soporte, noticias, documentos legales.
- **"Sucio":** no estructurado, con sinonimia, errores, variaciones de caso, puntuación, altísima dimensionalidad (una columna potencial por cada palabra del vocabulario).
- Por eso el texto ilustra toda la complejidad de la **preparación de datos**: la representación es una decisión de diseño creativa y experimentable, no un paso fijo.

---

## 2. Preprocesamiento (normalización)

Antes de representar numéricamente, limpia y unifica el texto:

| Paso | Qué hace | Nota |
| --- | --- | --- |
| **Tokenización** | Partir el texto en unidades (palabras, símbolos) | Base de todo lo demás |
| **Minúsculas** | `SKYPE` → `skype` | Unifica variantes de caso |
| **Quitar puntuación / números** | Según el propósito | **Con criterio**: a veces importan (`4TB`, `1Q13`) |
| **Stopwords** | Quitar palabras muy comunes (`the`, `de`, `y`) | **No siempre conviene** (el título *The Road* pierde sentido sin ellas) |
| **Stemming** | Recortar sufijos: `announces/announced/announcing` → `announc` | Rápido, agresivo, produce raíces no-palabras |
| **Lematización** | Reducir a la forma de diccionario: `mejores` → `bueno` | Más preciso que stemming, requiere análisis morfológico |

> **Regla:** quitar stopwords, números o puntuación **a ciegas** puede destruir señal. El propósito decide. (El encoding de texto como paso de pipeline está en `05_preparacion_de_datos.md`.)

---

## 3. Bolsa de palabras y TF-IDF (representación base)

### Bolsa de palabras (bag of words)
Trata **cada palabra como un atributo independiente**: se tira la gramática y el orden. Cada documento → un vector de frecuencias; el corpus → un conjunto de vectores, listo para clasificación, clustering o recuperación.

### TF, IDF y TF-IDF
| Medida | Qué mide |
| --- | --- |
| **TF** (term frequency) | Cuántas veces aparece el término en *este* documento |
| **IDF** (inverse document frequency) | Cuán **raro** es el término en el corpus (penaliza los omnipresentes) |
| **TF-IDF** = TF × IDF | Premia términos frecuentes en este documento **pero raros** en el corpus → los verdaderamente distintivos |

Es la representación de valor más común para texto (aunque no siempre la óptima; conviene experimentar: binaria, TF, TF-IDF, con/sin normalización).

> **Conexión:** IDF está emparentada con la **entropía** (ver ganancia de información en `06`): ambas miden cuán "mezclado/informativo" es algo.

### Pipeline bolsa de palabras + TF-IDF
1. Normalizar (minúsculas, tokenizar).
2. Stemming / lematización.
3. Quitar stopwords (con criterio según el propósito).
4. Contar términos por documento → TF.
5. Calcular IDF por término en el corpus.
6. Combinar → TF-IDF; cada documento = un vector.
7. (Opcional) **selección de atributos:** umbrales mín/máx de frecuencia o ranking por ganancia de información para descartar términos poco informativos.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
X = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1,1)).fit_transform(docs)
```

---

## 4. Recuperación y similitud

Con los documentos como vectores TF-IDF, la **similitud coseno** mide cuán parecidos son dos textos (ángulo entre sus vectores). Base de buscadores, recomendación de documentos y clasificación por vecinos.

> *Ej. (DSB):* 15 biografías de músicos de jazz en Wikipedia (~2.000 features); la consulta *"Famous jazz saxophonist born in Kansas who played bebop"* se vectoriza en TF-IDF y se compara por coseno con cada biografía → el más cercano es **Charlie Parker**.

> **Conexión:** similitud, vecinos y clustering (incluido el coseno) se desarrollan en `06_modelado_y_evaluacion.md` §3c.

---

## 5. Más allá de la bolsa de palabras

Cuando el **orden, las entidades o los temas** importan:

- **N-gramas:** secuencias de `n` palabras adyacentes (bi-gramas, tri-gramas); capturan algo del orden y las frases hechas, a costa de disparar la dimensionalidad.
- **POS tagging (etiquetado gramatical):** marcar cada palabra con su categoría (sustantivo, verbo…); útil como feature o para extracción.
- **Named Entity Recognition (NER):** reconocer nombres propios (personas, empresas, lugares). Algunos extractores tienen áreas de especialidad.
- **Topic models:** una capa intermedia de **temas latentes** entre palabras y documentos (palabras → temas → documento). Métodos: **LSI** (Latent Semantic Indexing), **LDA** (Latent Dirichlet Allocation). Un tema es como "un clustering de palabras"; permite que una consulta coincida con un documento aunque no compartan las palabras exactas (mapean al mismo tema).

> **Regla:** añade complejidad (n-gramas, temas) solo si mejora el desempeño medido.

---

## 6. Representaciones densas (embeddings) y modelos de lenguaje

La bolsa de palabras es **dispersa** (sparse) y no captura significado ni orden. Las representaciones modernas lo superan:

- **Word embeddings** (word2vec, GloVe, fastText): cada palabra → un vector **denso** donde la cercanía refleja similitud semántica (`rey − hombre + mujer ≈ reina`).
- **Embeddings contextuales / Transformers** (BERT y sucesores): el vector de una palabra depende de su contexto; estado del arte para clasificación, NER, QA, resumen.
- **Embeddings de frase/documento** + **búsqueda semántica** (bases vectoriales): recuperación por significado, no por coincidencia léxica.
- **LLMs:** generación, clasificación zero/few-shot, extracción y resumen con poco o ningún entrenamiento específico.

> Elección pragmática: TF-IDF + modelo lineal/Naive Bayes sigue siendo una **línea base** fuerte, rápida e interpretable; sube a embeddings/Transformers solo si el problema lo justifica.

---

## 7. Tareas típicas de NLP

| Tarea | Descripción | Enfoque base |
| --- | --- | --- |
| **Clasificación de texto** | Spam, sentimiento, categoría de ticket | TF-IDF + Naive Bayes / logística → embeddings |
| **Recuperación / búsqueda** | Documentos relevantes a una consulta | TF-IDF + coseno → búsqueda semántica |
| **Clustering de documentos** | Agrupar textos sin etiqueta | TF-IDF + k-means / jerárquico |
| **Topic modeling** | Descubrir temas latentes | LDA / LSI |
| **NER** | Extraer entidades | spaCy / Transformers |
| **Sentimiento** | Polaridad/emoción | Léxicos → clasificador → Transformers |
| **Resumen / generación / QA** | Condensar, generar, responder | Transformers / LLMs |

---

## 8. Flujo de trabajo de un proyecto de texto

```
Texto crudo
   ↓
Normalización (tokenizar, minúsculas, stemming/lematización, stopwords con criterio)
   ↓
Representación:  bolsa de palabras / TF-IDF  →  n-gramas  →  embeddings
   ↓
Tarea:  clasificación · recuperación/coseno · clustering · topic models · NER
   ↓
Evaluación (según la tarea; ver métricas de clasificación en 06)
   ↓
Decisión / producto (buscador, moderación, enrutamiento de tickets…)
```

### Librerías principales

| Librería | Uso |
| --- | --- |
| **NLTK** | Tokenización, stemming, POS, corpora didácticos |
| **spaCy** | Pipeline industrial: tokenización, lematización, POS, NER |
| **scikit-learn** | `TfidfVectorizer`, `CountVectorizer`, clasificadores, clustering |
| **gensim** | Topic models (LDA/LSI), word2vec |
| **Hugging Face Transformers** | Embeddings contextuales, BERT, LLMs |

---

## Conexión con el resto del flujo

- **Texto libre como tipo de variable** → `01_fundamentos_ciencia_datos.md` §5.
- **Encoding/vectorización de texto en el pipeline** → `05_preparacion_de_datos.md` §6 (ColumnTransformer).
- **Naive Bayes** (clasificador base para texto), **similitud coseno, k-NN y clustering**, y **ganancia de información** (emparentada con IDF) → `06_modelado_y_evaluacion.md` §3b, §3c, §9/interpretabilidad.
- **Visualizar texto cualitativo** (citas, word trees, coloreo de frases) → `08_visualizacion_y_comunicacion.md` §2.

> La representación del texto es una decisión de diseño: empieza con bolsa de palabras + TF-IDF como línea base y añade complejidad (n-gramas, embeddings, Transformers) solo cuando mejore el resultado medido.
