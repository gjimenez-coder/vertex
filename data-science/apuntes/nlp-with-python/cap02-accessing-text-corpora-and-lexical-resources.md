# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 2 — Accessing Text Corpora and Lexical Resources (Acceso a corpus de texto y recursos léxicos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El trabajo práctico en procesamiento del lenguaje natural usa grandes cuerpos de datos lingüísticos, o *corpora*. Este capítulo responde tres preguntas: qué corpus y recursos léxicos útiles existen y cómo acceder a ellos con Python; qué construcciones de Python ayudan más en este trabajo; y cómo evitar repetir código. Se presentan los conceptos mediante ejemplos, dejando el estudio sistemático de cada construcción para capítulos posteriores.

Sales sabiendo acceder a los corpus incluidos en NLTK (Gutenberg, web/chat, Brown, Reuters, discursos inaugurales, corpus en otras lenguas) mediante un conjunto común de métodos (`fileids()`, `words()`, `sents()`, `raw()`, `categories()`), y cargar tus propios textos con `PlaintextCorpusReader`. Aprendes a usar distribuciones de frecuencia condicionales para comparar categorías de texto, a reutilizar código con editores de texto, funciones y módulos, y a explorar recursos léxicos: listas de palabras, el diccionario de pronunciación CMU, listas comparativas Swadesh, léxicos Toolbox y, sobre todo, WordNet.

La tesis central es que los corpus y los recursos léxicos, combinados con unas pocas construcciones de Python bien elegidas, permiten investigar sistemáticamente diferencias entre géneros, autores y lenguas, y relaciones de significado entre palabras.

## Acceso a corpus de texto

Un corpus de texto es un cuerpo grande de texto; muchos se diseñan con un equilibrio cuidado de material en uno o más géneros.

NLTK incluye una selección del archivo Project Gutenberg (unas 25.000 obras libres). Se accede a los identificadores de archivo y luego a cada texto:

```python
>>> import nltk
>>> nltk.corpus.gutenberg.fileids()
['austen-emma.txt', 'austen-persuasion.txt', ...]
>>> emma = nltk.corpus.gutenberg.words('austen-emma.txt')
>>> len(emma)
192427
```

Para concordancias sobre un corpus hay que envolver las palabras en `nltk.Text`: `emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))`. Con `from nltk.corpus import gutenberg` se evitan nombres largos. Un bucle sobre `gutenberg.fileids()` calcula para cada texto longitud media de palabra, longitud media de frase y diversidad léxica; la longitud media de palabra resulta ser una propiedad general del inglés (valor recurrente de 4, en realidad 3 descontando el espacio), mientras que longitud de frase y diversidad léxica caracterizan a autores concretos.

Además de `words()`, están `raw()` (contenido sin procesar, incluidos espacios) y `sents()` (lista de frases, cada una lista de palabras). Muchos lectores de corpus ofrecen más métodos de acceso (etiquetas morfosintácticas, árboles sintácticos, etc.) que se verán más adelante.

El corpus **web y chat** recoge lenguaje menos formal: un foro de Firefox, conversaciones oídas en Nueva York, el guion de *Pirates of the Caribbean*, anuncios personales y reseñas de vino (`webtext`). El corpus `nps_chat` contiene más de 10.000 mensajes de mensajería instantánea, anonimizados (usuarios como "UserNNN"), organizados en 15 archivos por fecha y sala de chat según edad.

El **Brown Corpus** fue el primer corpus electrónico de un millón de palabras de inglés (1961, Brown University). Contiene texto de 500 fuentes categorizadas por género (news, editorial, reviews, religion, hobbies, etc.). Se accede por categorías o por archivos:

```python
>>> from nltk.corpus import brown
>>> brown.categories()
['adventure', 'belles_lettres', ...]
>>> brown.words(categories='news')
['The', 'Fulton', 'County', ...]
```

Es un recurso conveniente para la *estilística* (diferencias sistemáticas entre géneros). Comparando el uso de verbos modales con una `ConditionalFreqDist` tabulada por género se observa que el modal más frecuente en *news* es *will*, mientras que en *romance* es *could*.

El **Reuters Corpus** tiene 10.788 documentos de noticias (1,3 millones de palabras), clasificados en 90 temas y divididos en conjuntos "training" y "test" para entrenar y probar algoritmos de detección de tema. A diferencia de Brown, sus categorías se solapan, porque una noticia puede cubrir varios temas. Los métodos aceptan un `fileid` o una lista; las primeras palabras de cada texto son el título, en mayúsculas por convención.

El **Inaugural Address Corpus** es en realidad una colección de 55 textos, uno por discurso presidencial, con dimensión temporal: el año aparece en el nombre de archivo (`fileid[:4]`). Una `ConditionalFreqDist` permite ver cómo evoluciona el uso de palabras como *america* y *citizen* a lo largo del tiempo.

NLTK distribuye muchos corpus anotados (etiquetas morfosintácticas, entidades nombradas, estructuras sintácticas, roles semánticos): Brown, Penn Treebank, CoNLL, Movie Reviews, Names Corpus, NPS Chat, Reuters, WordNet 3.0, entre otros (ver la tabla del capítulo). También hay corpus en **otras lenguas** (`cess_esp`, `floresta`, `indian`, `udhr`), que a veces requieren manejar codificaciones de caracteres. El corpus `udhr` contiene la Declaración Universal de los Derechos Humanos en más de 300 lenguas, con la codificación indicada en el `fileid`.

Las **estructuras de corpus** van de lo más simple (una colección de textos sin organización) a textos agrupados en categorías (que pueden solaparse, como los temas) o con estructura temporal (colecciones de noticias). Los lectores de corpus de NLTK comparten una funcionalidad básica: `fileids()`, `categories()`, `raw()`, `words()`, `sents()`, además de `abspath()`, `encoding()`, `open()`, `root()` y `readme()`.

Para **cargar tu propio corpus** se usa `PlaintextCorpusReader(corpus_root, patrón)`, donde el patrón puede ser una lista de `fileids` o una expresión regular que los empareje. Para corpus analizados como Penn Treebank se usa `BracketParseCorpusReader`.

## Distribuciones de frecuencia condicionales

Cuando los textos de un corpus se dividen en categorías (género, tema, autor), se puede mantener una distribución de frecuencia separada por categoría. Una *conditional frequency distribution* es una colección de distribuciones de frecuencia, una por cada "condición". Mientras `FreqDist()` toma una lista simple, `ConditionalFreqDist()` toma una lista de pares `(condición, evento)`:

```python
>>> cfd = nltk.ConditionalFreqDist(
...           (genre, word)
...           for genre in brown.categories()
...           for word in brown.words(categories=genre))
>>> cfd.conditions()
```

Procesando Brown por género habría 15 condiciones y 1.161.192 eventos. Se accede a cada condición con `cfd['news']`, que es a su vez una `FreqDist`, y a una frecuencia concreta con `cfd['romance']['could']`.

Para visualizar hay `plot()` y `tabulate()`, ambos con parámetros opcionales `conditions=` y `samples=` que controlan qué mostrar y en qué orden. Esto permite cargar muchos datos y explorarlos tabulando o graficando subconjuntos; con `cumulative=True` se obtienen frecuencias acumuladas.

Las expresiones multilínea usadas aquí son como listas por comprensión sin corchetes: al pasar una comprensión como argumento de una función se pueden omitir los corchetes (expresiones generadoras).

Una `ConditionalFreqDist` también sirve para **generar texto con bigramas**. La función `nltk.bigrams()` produce pares de palabras consecutivas. Tratando cada palabra como condición, se registra qué palabras siguen a cada una; una función `generate_model()` parte de una palabra semilla y en cada paso elige la palabra más probable con `max()`. Este enfoque tiende a quedarse atrapado en bucles (una alternativa sería elegir la siguiente palabra al azar).

## Más Python: reutilizar código

Reescribir código en el intérprete es propenso a errores. Hay dos formas importantes de reutilizarlo.

Con un **editor de texto** se compone un programa de varias líneas y se ejecuta de una vez (en IDLE, File → New, luego Run → Run Module). Conviene probar ideas en el intérprete y luego pegar el código (sin los `>>>` y `...`) en un archivo `.py` con nombre descriptivo en minúsculas y guiones bajos.

Una **función** es un bloque de código con nombre que realiza una tarea bien definida. Se define con `def`, nombre, parámetros entre paréntesis y un cuerpo indentado; `return` indica el valor de salida. Las variables creadas en el cuerpo son locales. Una función no hace nada hasta que se la "llama" (invoca).

```python
>>> def lexical_diversity(text):
...     return len(text) / len(set(text))
```

El ejemplo `plural()` intenta formar el plural de un nombre inglés según patrones (si termina en `y`, se cambia por `ies`, etc.), aunque no siempre acierta. Las funciones asociadas a un objeto, como `word.endswith()`, se llaman *métodos*.

Un **módulo** es una colección de definiciones de variables y funciones en un archivo; guardando funciones en `textproc.py` se accede a ellas con `from textproc import plural`, de modo que hay una sola versión de cada función. Una colección de módulos relacionados es un *paquete*; NLTK es un conjunto de paquetes (una biblioteca). Cuidado: no llames `nltk.py` a tus archivos, porque podría importarse en lugar del paquete real (Python busca primero en el directorio actual).

## Recursos léxicos

Un *léxico* o recurso léxico es una colección de palabras o frases con información asociada (categoría gramatical, definiciones de sentido). Son secundarios a los textos y suelen crearse con su ayuda: `sorted(set(my_text))` da el vocabulario y `FreqDist(my_text)` cuenta frecuencias; ambos son léxicos simples. Una *entrada léxica* consta de un lema (headword) más información adicional; dos palabras distintas con la misma grafía son *homónimos*.

NLTK incluye **corpus de listas de palabras**. El Words Corpus (archivo `/usr/dict/words` de Unix) sirve para encontrar palabras inusuales o mal escritas: se computa el vocabulario de un texto y se le resta el de la lista (`unusual_words`). El corpus de *stopwords* reúne palabras muy frecuentes (como *the*, *to*, *also*) que a veces se filtran antes de procesar; una función `content_fraction` muestra que filtran alrededor de un tercio de las palabras de Reuters. Las listas de palabras también sirven para resolver puzzles (comparando `nltk.FreqDist(w) <= puzzle_letters`). El Names Corpus contiene 8.000 nombres categorizados por género en archivos separados; una `ConditionalFreqDist` por última letra muestra que los nombres terminados en *a*, *e* o *i* suelen ser femeninos.

El **CMU Pronouncing Dictionary** (inglés de EE. UU., diseñado para síntesis de voz) asocia a cada palabra una lista de *phones* (códigos fonéticos del Arpabet); por ejemplo *fire* tiene dos pronunciaciones. Las entradas se recorren desempaquetando con `for word, pron in entries`. Los dígitos en los phones marcan acento primario (1), secundario (2) o átono (0); con una función `stress()` se buscan palabras con un patrón de acentuación dado. También se puede acceder por búsqueda directa convirtiéndolo en diccionario Python con `nltk.corpus.cmudict.dict()`; indexar una clave inexistente produce `KeyError`.

Las **listas comparativas Swadesh** reúnen unas 200 palabras comunes en varias lenguas, identificadas por código ISO 639 de dos letras. Con `swadesh.entries(['fr', 'en'])` se obtienen pares de cognados que, pasados por `dict()`, forman un traductor simple; `update()` añade más lenguas de origen.

Los léxicos **Shoebox y Toolbox** son la herramienta más popular entre lingüistas para gestionar datos de campo. Un archivo Toolbox es una colección de entradas formadas por campos, la mayoría opcionales o repetibles, por lo que no puede tratarse como una tabla. El ejemplo del rotokas muestra pares atributo-valor como `('ps', 'V')` (categoría) o `('ge', 'gag')` (glosa al inglés). Su estructura laxa se procesa mejor con XML (capítulo 11).

## WordNet

WordNet es un diccionario de inglés orientado semánticamente, similar a un tesauro pero con estructura más rica; el WordNet inglés de NLTK tiene 155.287 palabras y 117.659 conjuntos de sinónimos.

Si en una frase se sustituye *motorcar* por *automobile* sin cambiar el significado, ambas son sinónimas. `wn.synsets('motorcar')` devuelve un único *synset*, `car.n.01` (primer sentido nominal de *car*). Un synset es un conjunto de sinónimos cuyos miembros (lemas) se obtienen con `.lemma_names`; también trae `.definition` y `.examples`. El emparejamiento de un synset con una palabra concreta (p. ej. `car.n.01.automobile`) es un *lemma*. La palabra *car* es ambigua: tiene cinco synsets.

Los synsets corresponden a conceptos abstractos ligados en una **jerarquía**. Los conceptos muy generales (Entity, State, Event) son raíces o *unique beginners*. Desde un concepto se navega hacia lo más específico con `hyponyms()` y hacia lo más general con `hypernyms()`; `hypernym_paths()` da los caminos hasta la raíz (motorcar tiene dos, porque `wheeled_vehicle` se clasifica como vehículo y como contenedor) y `root_hypernyms()` da el más general.

Hiperónimos e hipónimos son *relaciones léxicas* en la jerarquía "es-un". Otras relaciones: *meronyms* (partes o sustancia de algo) y *holonyms* (aquello en lo que algo está contenido), con variantes `part_`, `substance_` y `member_`. Entre verbos existe la implicación (`entailments()`: caminar implica dar pasos). Entre lemas hay antonimia (`antonyms()`).

Para la **similitud semántica**, dos synsets que comparten un hiperónimo muy específico están muy relacionados. `lowest_common_hypernyms()` encuentra el hiperónimo común más bajo, y `min_depth()` cuantifica la generalidad (profundidad en la jerarquía). `path_similarity()` asigna una puntuación de 0 a 1 según el camino más corto entre conceptos (devuelve -1 si no hay camino, 1 al compararse consigo mismo); las puntuaciones decrecen al alejarse del espacio semántico de las criaturas marinas hacia objetos inanimados. Hay otras medidas de similitud; NLTK también incluye VerbNet, un léxico jerárquico de verbos enlazado a WordNet.

## Ideas clave

- Un corpus de texto es una colección grande y estructurada de textos; NLTK trae muchos (Brown, Gutenberg, Reuters, inaugural, chat, otras lenguas).
- Los lectores de corpus comparten métodos comunes (`fileids()`, `words()`, `sents()`, `raw()`, `categories()`); se pueden cargar corpus propios con `PlaintextCorpusReader`.
- Algunos corpus se categorizan por género o tema, y las categorías pueden solaparse (como los temas de Reuters) o tener estructura temporal (discursos inaugurales).
- Una distribución de frecuencia condicional (`ConditionalFreqDist`) es una colección de distribuciones de frecuencia, una por condición, útil para comparar géneros y para generar texto con bigramas.
- El código se reutiliza con editores de texto, funciones (`def` ... `return`, con variables locales y métodos) y módulos importables; evita nombrar un archivo `nltk.py`.
- Los recursos léxicos van de listas simples de palabras y stopwords al diccionario de pronunciación CMU, las listas Swadesh y los léxicos Toolbox de estructura laxa.
- WordNet organiza synsets (conjuntos de sinónimos) en una red de relaciones: hiperónimos/hipónimos, merónimos/holónimos, implicaciones y antónimos.
- La similitud semántica se estima con el hiperónimo común más bajo, la profundidad de los synsets y medidas como `path_similarity`.
