# Accessing Text Corpora and Lexical Resources (Acceso a corpus de texto y recursos léxicos) — Estudio

## Tarjetas de repaso

P: ¿Qué es un corpus de texto? / R: Un cuerpo grande de texto; muchos se diseñan con un equilibrio cuidado de material en uno o más géneros.

P: ¿Qué métodos de acceso comparten los lectores de corpus de NLTK? / R: `fileids()`, `categories()`, `raw()`, `words()`, `sents()`, además de `abspath()`, `encoding()`, `open()`, `root()` y `readme()`.

P: ¿Para qué sirven `words()`, `raw()` y `sents()`? / R: `words()` da la lista de palabras, `raw()` el contenido sin procesar (incluidos espacios) y `sents()` una lista de frases, cada una lista de palabras.

P: ¿Qué es el Brown Corpus y para qué es conveniente? / R: El primer corpus electrónico de un millón de palabras de inglés (1961, Brown University), con 500 fuentes categorizadas por género; conveniente para la estilística.

P: ¿En qué se diferencian las categorías de Reuters frente a las de Brown? / R: En Reuters las categorías (90 temas) se solapan, porque una noticia puede cubrir varios temas; además se divide en conjuntos "training" y "test".

P: ¿Qué es una conditional frequency distribution? / R: Una colección de distribuciones de frecuencia, una por cada "condición"; `ConditionalFreqDist()` toma una lista de pares `(condición, evento)`.

P: ¿Cómo se accede a una condición y a una frecuencia concreta en una `ConditionalFreqDist`? / R: Con `cfd['news']` se obtiene la `FreqDist` de esa condición y con `cfd['romance']['could']` una frecuencia concreta.

P: ¿Cómo se carga un corpus propio en NLTK? / R: Con `PlaintextCorpusReader(corpus_root, patrón)`, donde el patrón es una lista de `fileids` o una expresión regular; para corpus analizados como Penn Treebank, `BracketParseCorpusReader`.

P: ¿Qué es una función en Python y cómo se define? / R: Un bloque de código con nombre que realiza una tarea bien definida; se define con `def`, nombre, parámetros entre paréntesis y cuerpo indentado, y `return` indica el valor de salida.

P: ¿Qué es un módulo y qué precaución hay al nombrar archivos? / R: Una colección de definiciones de variables y funciones en un archivo; no debe llamarse `nltk.py` porque podría importarse en lugar del paquete real (Python busca primero en el directorio actual).

P: ¿Qué es un recurso léxico y qué es una entrada léxica? / R: Un léxico es una colección de palabras o frases con información asociada; una entrada léxica consta de un lema (headword) más información adicional.

P: ¿Qué es el CMU Pronouncing Dictionary y qué marcan los dígitos de sus phones? / R: Un diccionario de pronunciación del inglés de EE. UU. (Arpabet); los dígitos marcan acento primario (1), secundario (2) o átono (0).

P: ¿Qué es un synset en WordNet? / R: Un conjunto de sinónimos cuyos miembros (lemas) se obtienen con `.lemma_names`; incluye `.definition` y `.examples`.

P: ¿Qué relaciones léxicas organiza WordNet? / R: Hiperónimos/hipónimos (jerarquía "es-un"), merónimos/holónimos (partes/contenedor), implicaciones entre verbos (`entailments()`) y antonimia entre lemas (`antonyms()`).

P: ¿Cómo se estima la similitud semántica en WordNet? / R: Con el hiperónimo común más bajo (`lowest_common_hypernyms()`), la profundidad (`min_depth()`) y `path_similarity()`, que da de 0 a 1 según el camino más corto.

## Preguntas de autoevaluación

P: ¿Qué propiedad resulta general del inglés al recorrer los textos de Gutenberg y cuáles caracterizan a autores concretos? / R: La longitud media de palabra es una propiedad general (valor recurrente de 4, 3 descontando el espacio), mientras que longitud de frase y diversidad léxica caracterizan a autores concretos. (Sección: Acceso a corpus de texto)

P: ¿Qué revela comparar verbos modales por género en Brown con una `ConditionalFreqDist`? / R: Que el modal más frecuente en *news* es *will*, mientras que en *romance* es *could*. (Sección: Acceso a corpus de texto)

P: ¿Qué dimensión especial tiene el Inaugural Address Corpus y cómo se aprovecha? / R: Una dimensión temporal: el año está en el nombre de archivo (`fileid[:4]`), lo que permite ver con una `ConditionalFreqDist` la evolución de palabras como *america* y *citizen*. (Sección: Acceso a corpus de texto)

P: ¿Cómo sirve una `ConditionalFreqDist` para generar texto con bigramas y qué limitación tiene? / R: Tratando cada palabra como condición se registra qué palabras la siguen, y `generate_model()` elige en cada paso la más probable con `max()`; tiende a quedarse atrapada en bucles. (Sección: Distribuciones de frecuencia condicionales)

P: ¿Para qué sirven el Words Corpus y el corpus de stopwords? / R: El Words Corpus permite encontrar palabras inusuales o mal escritas restando su lista del vocabulario del texto; las stopwords son palabras muy frecuentes que a veces se filtran (filtran alrededor de un tercio de las palabras de Reuters). (Sección: Recursos léxicos)

P: ¿Por qué un archivo Toolbox no puede tratarse como una tabla? / R: Porque es una colección de entradas formadas por campos, la mayoría opcionales o repetibles; su estructura laxa se procesa mejor con XML. (Sección: Recursos léxicos)

P: ¿Por qué *motorcar* tiene dos `hypernym_paths()` hasta la raíz? / R: Porque `wheeled_vehicle` se clasifica como vehículo y como contenedor, dando dos caminos distintos hacia la raíz. (Sección: WordNet)

## Puntos a dominar

- Acceder a los corpus de NLTK (Gutenberg, web/chat, Brown, Reuters, inaugural, otras lenguas) con los métodos comunes `fileids()`, `words()`, `sents()`, `raw()`, `categories()`.
- Cargar corpus propios con `PlaintextCorpusReader` (y `BracketParseCorpusReader` para corpus analizados).
- Distinguir estructuras de corpus: colección simple, categorías por género/tema (que pueden solaparse) y estructura temporal.
- Construir y explorar una `ConditionalFreqDist` con pares `(condición, evento)`, visualizándola con `plot()` y `tabulate()` (parámetros `conditions=`, `samples=`, `cumulative=True`).
- Reutilizar código mediante editores de texto, funciones (`def`/`return`, variables locales, métodos) y módulos importables, evitando nombrar un archivo `nltk.py`.
- Usar recursos léxicos: listas de palabras, stopwords, Names Corpus, CMU Pronouncing Dictionary, listas Swadesh y léxicos Toolbox.
- Navegar WordNet: synsets, lemas, jerarquía con `hyponyms()`/`hypernyms()`, relaciones (merónimos/holónimos, implicaciones, antónimos) y similitud con `path_similarity()`.
