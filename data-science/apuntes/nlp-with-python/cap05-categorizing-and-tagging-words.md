# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 5 — Categorizing and Tagging Words (Categorizar y etiquetar palabras)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`. Se han conservado solo las sesiones interactivas esenciales y resumido el resto.

## Lo que necesitas saber
El capítulo trata del etiquetado gramatical (part-of-speech tagging o POS tagging): clasificar cada palabra de un texto según su clase léxica (nombre, verbo, adjetivo, adverbio, etc.) y asignarle una etiqueta corta como `NN` o `VB`. Es el segundo paso del pipeline típico de NLP, tras la tokenización. El conjunto de etiquetas usado en una tarea se llama tagset.

La tesis central es que las clases léxicas no son una invención ociosa de los gramáticos: emergen del análisis de la distribución de las palabras en el texto y son útiles en muchas tareas (predecir el comportamiento de palabras nuevas, analizar el uso de palabras en corpus, sistemas de texto a voz). El capítulo presenta además técnicas fundamentales de NLP que trascienden el etiquetado: sequence labeling, modelos de n-gramas, backoff y evaluación.

Sales sabiendo usar el tagger de NLTK, representar y leer corpus etiquetados, modelar mapeos palabra→propiedad con diccionarios de Python (incluido `defaultdict`), y construir y evaluar una batería de taggers automáticos: default, por expresiones regulares, lookup, unigrama, n-grama (con backoff) y transformación (Brill). También aprendes a razonar sobre precisión, datos dispersos y los límites de rendimiento.

## 5.1 Usar un tagger
Un POS tagger procesa una secuencia de palabras y asigna una etiqueta a cada una. En NLTK:

```python
>>> text = nltk.word_tokenize("And now for something completely different")
>>> nltk.pos_tag(text)
[('And','CC'),('now','RB'),('for','IN'),('something','NN'),
 ('completely','RB'),('different','JJ')]
```

Aquí `and` es conjunción coordinante (`CC`), `now`/`completely` adverbios (`RB`), `for` preposición (`IN`), `something` nombre (`NN`) y `different` adjetivo (`JJ`). La documentación de cada etiqueta se consulta con `nltk.help.upenn_tagset('RB')`.

Con homónimos, el tagger distingue según el contexto: en "They refuse to permit us to obtain the refuse permit", `refuse` y `permit` aparecen como verbo (`VBP`/`VB`) y como nombre (`NN`). Por eso los sistemas de texto a voz suelen hacer POS tagging: refUSE (verbo, "negar") y REFuse (nombre, "basura") se pronuncian distinto.

La justificación de estas categorías es distribucional. El método `text.similar(w)` busca contextos w1·w·w2 y devuelve palabras que aparecen en el mismo contexto: buscar `woman` encuentra nombres; `bought`, verbos; `over`, preposiciones; `the`, determinantes. Un tagger también modela nuestro conocimiento de palabras desconocidas: puede adivinar que *scrobbling* es probablemente un verbo por el contexto "he was scrobbling".

## 5.2 Corpus etiquetados
Por convención, en NLTK un token etiquetado es una tupla `(token, tag)`. `nltk.tag.str2tuple('fly/NN')` produce `('fly', 'NN')`, y una cadena con pares `palabra/etiqueta` puede convertirse en lista de tuplas.

Varios corpus de NLTK vienen etiquetados y ofrecen una interfaz uniforme que oculta las diferencias de formato: todo corpus etiquetado tiene `tagged_words()` (y `tagged_sents()` si está segmentado en frases, útil para entrenar taggers). Las etiquetas se convirtieron a mayúsculas, práctica estándar desde el Brown Corpus:

```python
>>> nltk.corpus.brown.tagged_words()
[('The','AT'),('Fulton','NP-TL'),('County','NN-TL'), ...]
>>> nltk.corpus.brown.tagged_words(simplify_tags=True)
[('The','DET'),('Fulton','NP'),('County','N'), ...]
```

No todos los corpus usan el mismo tagset. Para empezar sin complicaciones se usa un mapeo a un tagset simplificado (`simplify_tags=True`). Hay corpus etiquetados en otros idiomas (chino, hindi, portugués, español, neerlandés, catalán), que suelen contener texto no ASCII mostrado en hexadecimal.

El tagset simplificado (Tabla 5-1) incluye, entre otros: `ADJ` adjetivo, `ADV` adverbio, `CNJ` conjunción, `DET` determinante, `MOD` verbo modal, `N` nombre, `NP` nombre propio, `NUM` número, `PRO` pronombre, `P` preposición, `TO` la palabra *to*, `V` verbo, `VD` pasado, `VG` gerundio/participio presente, `VN` participio pasado, `WH` determinante wh.

Explorando el Brown (categoría news), las etiquetas más frecuentes son `N`, `P`, `DET`, `NP`, `V`, `ADJ`. Los nombres (`N` comunes, `NP` propios) aparecen tras determinantes y adjetivos (incluidos numerales `NUM`). Los verbos describen eventos y relaciones entre sintagmas nominales; con una `ConditionalFreqDist` se puede ver, dada una palabra, sus etiquetas (p. ej. `cut` puede ser `V`, `VD`, `N`, `VN`), o dada una etiqueta, sus palabras típicas. La distinción entre `VD` (pasado) y `VN` (participio) se aprecia en el contexto: el participio suele ir precedido de una forma del auxiliar *have*.

Las etiquetas sin simplificar del Brown añaden sufijos: `$` posesivo, `S` plural, `P` propio, y modificadores `-NC` (citas), `-HL` (titulares), `-TL` (títulos). El programa `findtags()` lista los nombres más frecuentes de cada variante de `NN`. Con bigramas/trigramas de pares palabra-etiqueta se pueden buscar patrones como "<Verbo> to <Verbo>" (combined to achieve, wanted to wait...) o detectar palabras muy ambiguas (`best`: ADJ ADV NP V; `cut`: V N VN VD).

## 5.3 Mapear palabras a propiedades con diccionarios de Python
El etiquetado puede verse como un mapeo de palabras a etiquetas, y la estructura natural para mapeos en Python es el diccionario (también llamado array asociativo o hash). A diferencia de una lista, donde se indexa con un entero y se obtiene una palabra, un diccionario se indexa con una clave (una palabra) y devuelve un valor. La Tabla 5-4 muestra objetos lingüísticos como mapeos: índice de documento (palabra→páginas), tesauro (sentido→sinónimos), diccionario (lema→entrada), analizador morfológico (forma→morfemas).

Operaciones básicas: `pos = {}`, asignación `pos['colorless'] = 'ADJ'`, consulta `pos['ideas']`; acceder a una clave inexistente lanza `KeyError`. Las claves no están ordenadas (un diccionario es un mapeo, no una secuencia); `list(pos)`, `sorted(pos)` o un bucle `for` dan las claves. Métodos `keys()`, `values()`, `items()` devuelven claves, valores y pares. Solo hay un valor por clave (una reasignación sobrescribe); para múltiples valores se usa una lista como valor, p. ej. `pos['sleep'] = ['N','V']`. Las claves deben ser inmutables (cadenas, tuplas; una lista da `TypeError`).

Diccionarios por defecto: `nltk.defaultdict(tipo)` crea automáticamente un valor por defecto (`int`→0, `list`→[]) al acceder a una clave nueva, o cualquier valor vía una función sin argumentos (`lambda: 'N'`). Son útiles para tareas de lenguaje: para tratar los hapaxes y fijar un vocabulario, se reemplazan las palabras poco frecuentes por un token especial `UNK` mapeando las *n* más frecuentes a sí mismas y el resto a `UNK`.

Idioma habitual: inicializar un `defaultdict(int)` y recorrer el texto incrementando conteos (`counts[tag] += 1`), luego ordenar por valor con `sorted(..., key=itemgetter(1), reverse=True)`. El mismo patrón sirve para indexar palabras por sus dos últimas letras o crear un diccionario de anagramas (clave = letras ordenadas). NLTK ofrece atajos: `nltk.Index` es un `defaultdict(list)` con soporte de inicialización, y `nltk.FreqDist` es en esencia un `defaultdict(int)` con métodos de ordenación y gráficos.

Se pueden usar claves y valores complejos: un `defaultdict(lambda: defaultdict(int))` indexado por `(etiqueta_previa, palabra)` permite estudiar las etiquetas posibles de una palabra según la etiqueta anterior, información que un tagger puede usar (p. ej. `right` tras un determinante debe ser `ADJ`). Para búsqueda inversa (hallar clave dado un valor) conviene invertir el diccionario: si no hay valores repetidos, basta `dict((v,k) for (k,v) in pos.items())`; si los hay, se acumulan con `append()` o con `nltk.Index`.

## 5.4 Etiquetado automático
El tag de una palabra depende de la palabra y de su contexto en la frase, por lo que se trabaja con frases etiquetadas, no con palabras sueltas (`brown.tagged_sents(...)`).

- Default tagger: asigna la misma etiqueta a todo. Como el tag más frecuente del Brown news es `NN`, `nltk.DefaultTagger('NN')` etiqueta todo como nombre y acierta ~1/8 (0.13). Pese a su torpeza, aporta robustez porque la mayoría de palabras nuevas son nombres.
- Regexp tagger: asigna etiquetas según patrones de escritura (`.*ing$`→`VBG`, `.*ed$`→`VBD`, `.*\'s$`→`NN$`, `.*s$`→`NNS`, números cardinales, y un comodín `.*`→`NN`). Se procesan en orden y gana el primero que coincide; acierta ~1/5 (0.20).
- Lookup tagger (un `UnigramTagger` con `model`): almacena el tag más probable de las *n* palabras más frecuentes. Con solo las 100 más frecuentes acierta casi la mitad (0.46). Las palabras fuera del modelo quedan como `None`; combinándolo con un default tagger mediante `backoff` se cubren esos casos. El rendimiento crece rápido al aumentar el tamaño del modelo y luego se estanca (Figura 5-4).

Evaluación: se mide la precisión frente a un gold standard, un corpus anotado manualmente aceptado como referencia. El tagger acierta si su etiqueta coincide con la del gold standard. Aunque los anotadores humanos cometen errores y el tagset depende de una posición teórica, el gold standard es "correcto" por definición a efectos de evaluación. Crear un corpus anotado es una empresa mayor (datos, herramientas, documentación y prácticas de calidad). La evaluación es central porque los errores de un módulo se multiplican aguas abajo en el pipeline.

## 5.5 Etiquetado por n-gramas
Un unigram tagger asigna a cada token su tag más probable; se configura entrenándolo con frases etiquetadas (`nltk.UnigramTagger(train_sents)`). Entrenado y evaluado sobre los mismos datos da 0.93, pero eso es engañoso: hay que separar datos (p. ej. 90% entrenamiento, 10% prueba), tras lo cual baja a ~0.81, una medida honesta de su utilidad con texto nuevo.

Un n-gram tagger generaliza el unigrama: el contexto es la palabra actual más las etiquetas de los *n*-1 tokens previos (1-gram = unigrama; 2-gram = bigrama; 3-gram = trigrama) y elige el tag más probable en ese contexto. El `BigramTagger` etiqueta bien frases vistas en entrenamiento, pero ante una palabra nueva (p. ej. `13.5`) devuelve `None` y, al perder el contexto, falla el resto de la frase; su precisión global cae a ~0.10. Al crecer *n* aumenta la especificidad del contexto y la probabilidad de encontrar contextos no vistos: es el problema de los datos dispersos (sparse data), con un compromiso entre precisión y cobertura. Los n-gram taggers no deben cruzar fronteras de frase; al inicio, las etiquetas previas son `None`.

Combinar taggers (backoff): usar el algoritmo más preciso cuando se puede y recurrir a otro de mayor cobertura cuando no. Se encadenan pasando un tagger como `backoff` de otro:

```python
>>> t0 = nltk.DefaultTagger('NN')
>>> t1 = nltk.UnigramTagger(train_sents, backoff=t0)
>>> t2 = nltk.BigramTagger(train_sents, backoff=t1)
>>> t2.evaluate(test_sents)   # ~0.845
```

Especificar el backoff en el entrenamiento mantiene el modelo pequeño (se descarta un contexto si daría el mismo tag que su backoff); `cutoff` descarta contextos vistos pocas veces. Para palabras desconocidas, se limita el vocabulario a las *n* más frecuentes y se sustituye el resto por `UNK`: así los n-gram taggers pueden aprender que `UNK` tras `to` (`TO`) suele ser verbo. Un tagger entrenado puede guardarse con pickle para reutilizarlo.

Límites de rendimiento: empíricamente, ~1 de cada 20 trigramas del Brown es ambiguo (5%), lo que fija una cota inferior para un trigram tagger. La matriz de confusión (`nltk.ConfusionMatrix`) contrasta las etiquetas esperadas (gold) con las generadas y ayuda a decidir qué distinciones simplificar. Otra cota viene del desacuerdo entre anotadores humanos. El etiquetado colapsa distinciones (todos los pronombres personales → `PRP`) y a la vez resuelve ambigüedades, rasgo que facilita clasificación y predicción. En los años 90, la sorprendente precisión de los taggers estadísticos demostró que se podía resolver la desambiguación gramatical sin recurrir a conocimiento lingüístico profundo.

## 5.6 Etiquetado por transformación (Brill)
Los n-gram taggers tienen dos problemas: el tamaño de sus tablas (arrays dispersos de millones de entradas) y que solo usan tags del contexto, no las palabras. El Brill tagging, una forma de transformation-based learning, rinde muy bien con modelos minúsculos. La idea: adivinar el tag de cada palabra y luego corregir los errores, transformando un mal etiquetado en uno mejor. Como los n-gramas es aprendizaje supervisado, pero no cuenta observaciones sino que compila una lista de reglas de corrección.

La analogía es pintar: cubrir todo el lienzo de azul y luego sobrepintar el árbol con pinceles cada vez más finos. Ejemplo con dos reglas: (a) cambiar `NN` por `VB` cuando la palabra previa es `TO`; (b) cambiar `TO` por `IN` cuando el tag siguiente es `NNS`. Todas las reglas salen de una plantilla "reemplazar T1 por T2 en el contexto C"; en el entrenamiento el tagger genera miles de reglas candidatas y las puntúa por beneficio neto (etiquetas incorrectas que corrige menos etiquetas correctas que estropea). Ventaja añadida: las reglas son interpretables lingüísticamente, al contrario que una tabla de n-gramas.

## 5.7 Cómo determinar la categoría de una palabra
Los lingüistas usan tres tipos de pistas:

- Morfológicas: la estructura interna da pistas. El sufijo `-ness` forma nombres a partir de adjetivos (happy→happiness); `-ment` forma nombres a partir de verbos (govern→government); `-ing` marca el participio presente/gerundio.
- Sintácticas: los contextos típicos. Un criterio para adjetivo en inglés es que puede ir inmediatamente antes de un nombre o tras *be*/*very* (the near window; the end is very near).
- Semánticas: el significado (un nombre es "el nombre de una persona, lugar o cosa"). Se tratan con recelo por difíciles de formalizar, pero sustentan muchas intuiciones y permiten adivinar categorías en lenguas desconocidas (con cautela: el neerlandés *jarig* se traduce por *birthday* pero es adjetivo).

Clases abiertas y cerradas: los nombres son clase abierta (los idiomas incorporan términos nuevos constantemente: muggle, SARS...); las preposiciones son clase cerrada, con un conjunto limitado que cambia muy lentamente.

Morfología en los tagsets: los tagsets comunes capturan información morfosintáctica. Las formas de *go* se distinguen en el Brown: `go`/VB (base), `goes`/VBZ (3.ª sing.), `gone`/VBN (participio), `going`/VBG (gerundio), `went`/VBD (pasado). El verbo *to be* tiene tags especiales (be/BE, is/BEZ, are/BER, was/BEDZ...). Así, un tagger que use este tagset hace en efecto un análisis morfológico limitado. Los tagsets comparten categorías básicas pero difieren en cuán fino dividen y cómo definen las categorías: no hay una forma "correcta" de etiquetar, solo formas más o menos útiles según el objetivo.

Otros tipos de etiquetado existen por encima del POS: directivas para síntesis de voz (SSML), números de sentido (SemCor con sentidos de WordNet), rasgos morfológicos y actos de diálogo (NPS Chat Corpus: Statement, ynQuestion, Bye, System...).

## Ideas clave
- Las palabras se agrupan en clases léxicas (parts-of-speech); asignarlas automáticamente es el POS tagging, segundo paso del pipeline de NLP tras la tokenización.
- En NLTK un token etiquetado es una tupla `(palabra, tag)`; los corpus etiquetados ofrecen `tagged_words()`/`tagged_sents()` con interfaz uniforme y un tagset simplificado opcional.
- Los diccionarios de Python (y `defaultdict`, `nltk.Index`, `nltk.FreqDist`) son la estructura natural para mapear palabras a propiedades como su etiqueta.
- Hay una gama de taggers: default, por expresiones regulares, lookup, unigrama y n-grama; se combinan con backoff para equilibrar precisión y cobertura.
- Hay que separar datos de entrenamiento y prueba y evaluar contra un gold standard; al crecer *n* aparece el problema de datos dispersos y el compromiso precisión/cobertura.
- El Brill tagging (transformation-based learning) corrige un etiquetado inicial con reglas interpretables y usa modelos mucho más pequeños que los n-gramas.
- La categoría de una palabra se determina con pistas morfológicas, sintácticas y semánticas; los nombres son clase abierta y las preposiciones clase cerrada.
- El etiquetado colapsa algunas distinciones e introduce otras, y un tagset fino implica un análisis morfológico implícito; no existe un único tagset "correcto".
