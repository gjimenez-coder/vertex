# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 7 — Extracting Information from Text (Extracción de información a partir de texto)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El capítulo aborda cómo convertir texto no estructurado en datos estructurados que puedan consultarse como una base de datos. La tesis central es que, aunque construir una representación general del significado de un texto arbitrario sigue siendo inviable, sí es posible progresar mucho si limitamos el objetivo a "relaciones entre entidades" concretas (por ejemplo, qué organización opera en qué localización). A ese enfoque se le llama Information Extraction (extracción de información).

Sales sabiendo cuál es la arquitectura típica de un sistema de extracción (segmentación de oraciones, tokenización, etiquetado morfosintáctico, reconocimiento de entidades y, por último, reconocimiento de relaciones) y las técnicas concretas que la sostienen: chunking (segmentación en fragmentos), reconocimiento de entidades nombradas (NER) y extracción de relaciones.

Para el chunking aprendes a definir gramáticas de fragmentos con expresiones regulares sobre etiquetas POS, a usar chinking (lo contrario: definir lo que se excluye), a representar los fragmentos con etiquetas IOB o con árboles, y a entrenar y evaluar chunkers con el corpus CoNLL-2000, comparando enfoques basados en reglas, en n-gramas y en clasificadores.

## El ejemplo que recorre el capítulo

El hilo conductor es la relación entre organizaciones y localizaciones. La meta ilustrativa es responder "¿Qué organizaciones operan en Atlanta?" a partir de texto libre. Si los datos estuvieran en forma tabular (Tabla 7-1, con pares OrgName/LocationName como Omnicom–New York o Georgia-Pacific–Atlanta), la consulta sería trivial; el reto es obtener esa estructura desde un fragmento de prensa (de `nltk.corpus.ieer`) que menciona a Georgia-Pacific y BBDO South en Atlanta sin ningún vínculo explícito entre nombres y lugares.

## Information Extraction

La información útil suele venir como structured data: una organización regular y predecible de entidades y relaciones. Si los datos están en una lista de tuplas `(entidad, relación, entidad)`, una consulta se traduce directamente a código. La estrategia del capítulo no es interpretar el texto para responder la pregunta, sino convertir primero las oraciones en datos estructurados y luego aprovechar herramientas de consulta potentes como SQL. Aplicaciones mencionadas: business intelligence, recolección de currículos, análisis de medios, detección de sentimiento, búsqueda de patentes, escaneo de correo y, como área de investigación destacada, la extracción desde literatura científica de biología y medicina.

La arquitectura (Figura 7-1) toma el texto crudo y produce una lista de tuplas `(entidad, relación, entidad)`, por ejemplo `([ORG: 'Georgia-Pacific'] 'in' [LOC: 'Atlanta'])`. Las tres primeras tareas se encadenan en una función:

```python
def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
```

Después, el named entity recognition segmenta y etiqueta las entidades candidatas (sintagmas nominales definidos o nombres propios), y la relation extraction busca patrones entre pares de entidades cercanas para construir las tuplas de relación.

## Chunking

El chunking es la técnica básica para reconocer entidades: segmenta y etiqueta secuencias de varios tokens como fragmentos (chunks) que no se solapan y que normalmente son un subconjunto de los tokens. El caso central es el NP-chunking (fragmentos de sintagma nominal), que captura piezas más pequeñas que un sintagma nominal completo: por definición, un NP-chunk no contiene otro NP-chunk, de modo que cláusulas subordinadas y sintagmas preposicionales modificadores quedan fuera.

Las etiquetas POS son la fuente de información más útil. Se define una gramática de fragmentos con reglas basadas en patrones de etiquetas (tag patterns), secuencias de etiquetas entre ángulos como `<DT>?<JJ>*<NN>` (determinante opcional, cero o más adjetivos, un sustantivo):

```python
grammar = "NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar)
result = cp.parse(sentence)   # devuelve un árbol; result.draw() lo muestra
```

Un patrón más amplio como `<DT>?<JJ.*>*<NN.*>+` cubre más casos, aunque siempre aparecen ejemplos difíciles. El `RegexpParser` parte de una estructura plana y aplica las reglas en orden; en solapamientos, gana la coincidencia más a la izquierda (si una regla casa dos sustantivos y hay tres seguidos, solo se agrupan los dos primeros). El símbolo `$` de etiquetas como `PP$` debe escaparse (`PP\$`). Una gramática puede tener varias reglas, por ejemplo una para determinante/posesivo + adjetivos + sustantivo y otra `{<NNP>+}` para secuencias de nombres propios.

### Chinking

A veces es más fácil definir lo que se excluye. Un chink es una secuencia de tokens que no se incluye en un fragmento, y el chinking es el proceso de eliminarla de un chunk. Según dónde caiga la secuencia excluida (todo el chunk, su interior o un extremo), el resultado es que el chunk desaparece, se parte en dos o se reduce. Se marca con llaves invertidas, por ejemplo `}<VBD|IN>+{`, tras una regla `{<.*>+}` que mete toda la oración en un solo chunk.

### Representación: etiquetas frente a árboles

Las estructuras de chunks pueden representarse con etiquetas IOB o con árboles. En el esquema IOB cada token lleva una de tres etiquetas: `B` (begin, inicio de un chunk), `I` (inside, dentro) u `O` (outside, fuera). `B` e `I` se sufijan con el tipo de chunk (`B-NP`, `I-NP`); los tokens fuera llevan solo `O`. IOB es el formato estándar en ficheros (un token por línea con su etiqueta POS y su etiqueta de chunk) y permite varios tipos de chunk si no se solapan. NLTK usa árboles internamente, pero ofrece métodos para convertir entre árboles y el formato IOB.

## Desarrollo y evaluación de chunkers

Para evaluar hace falta un corpus anotado. El CoNLL-2000 Chunking Corpus contiene 270.000 palabras de Wall Street Journal en formato IOB, divididas en "train" y "test", con tres tipos de chunk: NP, VP y PP. Se accede con `nltk.corpus.conll2000`, y `chunk_types=['NP']` permite quedarse solo con los NP. La función `chunk.conllstr2tree()` convierte una cadena IOB en árbol.

Partiendo de líneas base, un chunker trivial que no crea chunks da 43,4% de precisión IOB pero precision/recall/F-measure de 0%. Un chunker ingenuo con expresión regular `r"NP: {<[CDJNP].*>+}"` ya alcanza F-measure de 69,2%.

Se mejora con un enfoque guiado por datos: un chunker basado en un unigram tagger que, en vez de predecir la etiqueta POS, predice la etiqueta de chunk (I/O/B) más probable para cada etiqueta POS. La clase `UnigramChunker` convierte entre árboles y tripletas `(palabra, etiqueta, chunk)` con `tree2conlltags` y `conlltags2tree`:

```python
class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data)
    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [c for (pos, c) in tagged_pos_tags]
        conlltags = [(w, p, c) for ((w,p),c) in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)
```

El unigram chunker logra F-measure de 83,2%; al inspeccionarlo se ve que casi toda la puntuación queda fuera de los NP (salvo `#` y `$` como marcas de moneda), que determinantes y posesivos abren los NP y que los sustantivos van dentro. Cambiar a un `BigramTagger` sube ligeramente (F-measure 84,5%).

### Chunkers basados en clasificadores

Las etiquetas POS a veces no bastan: `Joey/NN sold/VBD the/DT farmer/NN rice/NN` y `Nick/NN broke/VBD my/DT computer/NN monitor/NN` tienen las mismas etiquetas pero se fragmentan distinto. Para usar también el contenido de las palabras se emplea un tagger basado en clasificador (`ConsecutiveNPChunkTagger` con `MaxentClassifier`, envuelto por `ConsecutiveNPChunker`), con un extractor de rasgos `npchunk_features`. La performance crece al enriquecer los rasgos:

- Solo `pos`: F-measure 83,2% (similar al unigrama).
- Añadir `prevpos`: 84,4% (parecido al bigrama).
- Añadir `word`: 85,9% (mejora ~1,5 puntos, ~10% menos de error).
- Añadir lookahead (`nextpos`), rasgos emparejados (`prevpos+pos`, `pos+nextpos`) y el rasgo contextual `tags-since-dt` (etiquetas vistas desde el último determinante): F-measure 89,5%.

## Recursión en la estructura lingüística

Los chunks son planos, pero se pueden anidar con un cascaded chunker: una gramática multietapa con reglas recursivas (por ejemplo cuatro etapas para NP, PP, VP y S) produce estructuras de profundidad limitada por el número de etapas. Una sola pasada deja fuera algunos chunks (como el VP encabezado por el verbo); la solución es repetir las pasadas con el argumento `loop`:

```python
cp = nltk.RegexpParser(grammar, loop=2)
```

El libro advierte que crear y depurar una cascada es difícil y que, pasado cierto punto, conviene hacer parsing completo (Capítulo 8); además, la cascada solo genera árboles de profundidad fija, insuficiente para el análisis sintáctico completo.

Un árbol es un conjunto de nodos etiquetados conectados, cada uno alcanzable por un único camino desde la raíz; se usa la metáfora familiar (padre, hijo, hermanos). En NLTK se construye con etiqueta de nodo y lista de hijos (`nltk.Tree('NP', ['Alice'])`), se anidan en árboles mayores y se recorren con una función recursiva, detectando que un nodo es árbol por duck typing (que `t.node` esté definido).

## Named Entity Recognition

Las entidades nombradas (NEs) son sintagmas nominales definidos que refieren a tipos concretos de individuos. Los tipos comunes (Tabla 7-3) son ORGANIZATION, PERSON, LOCATION, DATE, TIME, MONEY, PERCENT, FACILITY (artefactos de arquitectura e ingeniería civil) y GPE (entidades geopolíticas: ciudad, estado/provincia, país). El NER tiene dos subtareas: identificar los límites de la entidad e identificar su tipo. Es útil, por ejemplo, en Question Answering, donde conocer el tipo esperado de la respuesta ayuda a descartar menciones del tipo equivocado.

Buscar cada palabra en una lista (un gazetteer o diccionario geográfico, como el Alexandria o el Getty) es propenso a errores: cobertura pobre para personas y organizaciones nuevas, y ambigüedad (May y North pueden ser DATE/LOCATION o parte de un PERSON; Christian Dior parece PERSON pero suele ser ORGANIZATION; Yankee cambia según contexto), además de nombres multipalabra o anidados. Por eso el NER encaja bien con el enfoque basado en clasificador del NP-chunking, etiquetando en formato IOB con el tipo de entidad. NLTK ofrece un clasificador ya entrenado:

```python
nltk.ne_chunk(sent, binary=True)  # solo marca NE
nltk.ne_chunk(sent)               # añade categorías: PERSON, ORGANIZATION, GPE...
```

## Relation Extraction

Identificadas las entidades, se extraen las relaciones entre tipos concretos. Una vía es buscar todos los tripletes `(X, α, Y)`, donde X e Y son entidades de los tipos requeridos y α es la cadena de palabras intermedia, y luego filtrar con expresiones regulares los α que expresan la relación buscada. Buscando la palabra *in* con un lookahead negativo que descarta gerundios:

```python
IN = re.compile(r'.*\bin\b(?!\b.+ing)')
nltk.sem.extract_rels('ORG', 'LOC', doc, corpus='ieer', pattern=IN)
# [ORG: 'Georgia-Pacific'] 'in' [LOC: 'Atlanta'] ...
```

Funciona razonablemente, aunque produce falsos positivos. Si el corpus trae etiquetas POS (sección neerlandesa del CoNLL 2002), se pueden diseñar patrones sensibles a ellas; `show_clause()` imprime la relación en forma clausal con el símbolo dado en `relsym`, p. ej. `VAN('annie_lennox', 'eurythmics')`.

## Ideas clave

- La extracción de información convierte texto no estructurado en tuplas `(entidad, relación, entidad)` que pueblan bases de datos consultables; es viable al limitarse a relaciones concretas.
- La arquitectura típica encadena segmentación de oraciones, tokenización, etiquetado POS, reconocimiento de entidades y, por último, reconocimiento de relaciones.
- El chunking segmenta y etiqueta secuencias de varios tokens no solapadas; las etiquetas POS son el rasgo más importante y se expresan en tag patterns como `<DT>?<JJ>*<NN>`.
- El chinking define lo que se excluye de un chunk; las estructuras se representan con etiquetas IOB (B/I/O) o con árboles, intercambiables en NLTK.
- Se evalúan chunkers con el CoNLL-2000 (métricas IOB accuracy, precision, recall, F-measure): de reglas simples (~69%) al unigrama/bigrama (83-84,5%) y al clasificador con rasgos ricos (89,5%).
- Los chunkers basados en clasificador aprovechan el contenido de las palabras además de las etiquetas POS, lo que supera a los enfoques de reglas y n-gramas.
- Los chunkers son planos, pero se pueden cascar para construir estructuras anidadas de profundidad fija.
- El NER identifica límites y tipo de entidades (ORGANIZATION, PERSON, LOCATION, DATE, TIME, MONEY, GPE...); la búsqueda en gazetteers falla por cobertura y ambigüedad, y la relation extraction se hace con patrones (reglas) o aprendizaje automático.
