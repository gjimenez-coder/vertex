# Extracting Information from Text — Estudio

## Tarjetas de repaso

P: ¿Qué es la Information Extraction (extracción de información)? / R: Convertir texto no estructurado en datos estructurados —tuplas `(entidad, relación, entidad)`— que puedan consultarse como una base de datos, limitándose a relaciones concretas entre entidades.

P: ¿Por qué es viable la extracción de información si una representación general del significado no lo es? / R: Porque se limita el objetivo a relaciones concretas entre entidades (p. ej. qué organización opera en qué localización) en lugar de interpretar el significado de texto arbitrario.

P: ¿Cuál es la arquitectura típica de un sistema de extracción? / R: Segmentación de oraciones, tokenización, etiquetado POS, reconocimiento de entidades nombradas y, por último, reconocimiento de relaciones.

P: ¿Qué hace la función `ie_preprocess`? / R: Encadena las tres primeras tareas: segmenta en oraciones (`sent_tokenize`), tokeniza cada oración (`word_tokenize`) y las etiqueta morfosintácticamente (`pos_tag`).

P: ¿Qué es el chunking y qué caracteriza a un NP-chunk? / R: Segmentar y etiquetar secuencias de varios tokens como fragmentos no solapados, subconjunto de los tokens; un NP-chunk no contiene otro NP-chunk, por lo que quedan fuera cláusulas subordinadas y sintagmas preposicionales modificadores.

P: ¿Qué es un tag pattern y qué expresa `<DT>?<JJ>*<NN>`? / R: Una secuencia de etiquetas POS entre ángulos que define una regla de fragmento; expresa determinante opcional, cero o más adjetivos y un sustantivo.

P: ¿Cómo resuelve el `RegexpParser` los solapamientos entre reglas? / R: Parte de una estructura plana, aplica las reglas en orden y, ante solapamientos, gana la coincidencia más a la izquierda.

P: ¿Qué es el chinking? / R: Definir lo que se excluye de un chunk; un chink es una secuencia de tokens que no se incluye en el fragmento, y según dónde caiga el chunk desaparece, se parte en dos o se reduce.

P: ¿Qué significan las etiquetas IOB? / R: `B` (begin, inicio de un chunk), `I` (inside, dentro) y `O` (outside, fuera); `B` e `I` se sufijan con el tipo de chunk (`B-NP`, `I-NP`).

P: ¿Qué es el CoNLL-2000 Chunking Corpus? / R: 270.000 palabras del Wall Street Journal en formato IOB, divididas en train y test, con tres tipos de chunk: NP, VP y PP.

P: ¿Por qué un chunker basado en clasificador supera a los de reglas y n-gramas? / R: Porque aprovecha también el contenido de las palabras además de las etiquetas POS, que a veces no bastan para fragmentar correctamente secuencias con idénticas etiquetas.

P: ¿Qué es un cascaded chunker? / R: Una gramática multietapa con reglas recursivas que produce estructuras anidadas de profundidad limitada por el número de etapas; se repiten pasadas con el argumento `loop`.

P: ¿Qué son las named entities (NEs) y cuáles son sus tipos comunes? / R: Sintagmas nominales definidos que refieren a tipos concretos de individuos: ORGANIZATION, PERSON, LOCATION, DATE, TIME, MONEY, PERCENT, FACILITY y GPE.

P: ¿Por qué buscar en un gazetteer es propenso a errores para NER? / R: Por cobertura pobre de personas y organizaciones nuevas, y por ambigüedad (May/North como DATE/LOCATION o parte de PERSON, Christian Dior, Yankee) y nombres multipalabra o anidados.

P: ¿Cómo se extraen relaciones entre entidades? / R: Buscando tripletes `(X, α, Y)` con X e Y de los tipos requeridos y α la cadena intermedia, filtrando con expresiones regulares (reglas) o con aprendizaje automático.

## Preguntas de autoevaluación

P: ¿Cuál es la estrategia del capítulo para responder "¿Qué organizaciones operan en Atlanta?" a partir de texto libre? / R: No interpretar el texto para responder directamente, sino convertir primero las oraciones en datos estructurados y luego aprovechar herramientas de consulta potentes como SQL. (Sección: Information Extraction / El ejemplo que recorre el capítulo)

P: ¿Qué diferencia hay entre chunking y chinking? / R: El chunking segmenta y etiqueta lo que se incluye en un fragmento; el chinking define lo que se excluye, eliminando una secuencia de tokens de un chunk (marcada con llaves invertidas). (Sección: Chunking / Chinking)

P: ¿Cómo evolucionan las métricas F-measure al mejorar el chunker en CoNLL-2000? / R: Chunker ingenuo con regex ~69,2%; unigram chunker 83,2%; bigram 84,5%; y clasificador con rasgos ricos hasta 89,5%. (Sección: Desarrollo y evaluación de chunkers)

P: ¿Qué rasgos hacen crecer el rendimiento del chunker basado en clasificador? / R: Solo `pos` 83,2%; añadir `prevpos` 84,4%; añadir `word` 85,9%; y añadir lookahead (`nextpos`), rasgos emparejados y `tags-since-dt` llega a 89,5%. (Sección: Chunkers basados en clasificadores)

P: ¿Cuáles son las dos subtareas del NER y por qué es útil en Question Answering? / R: Identificar los límites de la entidad e identificar su tipo; en Question Answering conocer el tipo esperado de la respuesta ayuda a descartar menciones del tipo equivocado. (Sección: Named Entity Recognition)

P: ¿Cuál es la limitación de una cascada de chunkers y qué alternativa propone el libro? / R: Solo genera árboles de profundidad fija, insuficiente para el análisis sintáctico completo, y es difícil de crear y depurar; pasado cierto punto conviene hacer parsing completo (Capítulo 8). (Sección: Recursión en la estructura lingüística)

P: ¿Cómo se usa `nltk.sem.extract_rels` y qué hace el patrón `IN`? / R: Busca relaciones entre entidades de tipos dados (p. ej. ORG y LOC) en un corpus; el patrón `IN` casa la palabra *in* con un lookahead negativo que descarta gerundios (`-ing`). (Sección: Relation Extraction)

## Puntos a dominar

- Distinguir la arquitectura completa de extracción: segmentación de oraciones → tokenización → etiquetado POS → NER → reconocimiento de relaciones.
- Entender que la extracción de información produce tuplas `(entidad, relación, entidad)` consultables, viable al limitarse a relaciones concretas.
- Leer y escribir tag patterns (`<DT>?<JJ>*<NN>`, `<DT>?<JJ.*>*<NN.*>+`, `{<NNP>+}`) y saber escapar `$` como `PP\$`.
- Diferenciar chunking de chinking y saber cuándo un chink hace desaparecer, partir o reducir un chunk.
- Dominar el esquema IOB (B/I/O) y su intercambiabilidad con árboles en NLTK.
- Conocer las métricas de evaluación (IOB accuracy, precision, recall, F-measure) y el orden de rendimiento de los enfoques (reglas < n-gramas < clasificador con rasgos ricos).
- Identificar los tipos de entidad del NER y por qué los gazetteers fallan por cobertura y ambigüedad.
- Comprender las dos vías de relation extraction: patrones basados en reglas (regex sobre α) y aprendizaje automático.
