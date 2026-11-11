# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 16 — Natural Language Processing (Procesamiento de lenguaje natural)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página como (PDF p. N). Del código fuente solo se conservan los fragmentos esenciales.

## Lo que necesitas saber
El capítulo presenta el procesamiento de lenguaje natural (NLP) como el conjunto de técnicas para trabajar con lenguaje humano: filtrar spam, medir sentimiento en Twitter o agrupar documentos por tema. Cady advierte que muchos científicos de datos nunca lo necesitan, pero es lo bastante distinto del resto de temas como para merecer un capítulo. También recuerda que estas técnicas no se limitan al lenguaje: sirven para analizar logs de ordenador o bioinformática.

La tesis central es que la mayoría del trabajo real de NLP cabe dentro del paradigma de la *bag-of-words* (bolsa de palabras) y sus extensiones. Ir más allá convierte el NLP en una tarea enormemente compleja que conviene dejar a especialistas. El capítulo avanza de lo simple y rápido (bag-of-words, TF-IDF, n-gramas, stop words, lemmatización) hacia lo más complicado (POS tagging, bases de conocimiento, ontologías).

Sales sabiendo cuándo conviene (y cuándo no) usar NLP, la diferencia entre la escuela estadística y la lingüística, cómo convertir texto en vectores numéricos y los problemas clásicos a los que se aplica: búsqueda, análisis de sentimiento, reconocimiento de entidades y modelado de temas.

## ¿Necesito siquiera NLP?
La primera pregunta al abordar un problema es si de verdad hace falta NLP. Suele haber presión de clientes y jefes para usarlo como si fuera una bala de plata mágica, pero es difícil de implementar y propenso a errores extraños que a un humano le resultan obviamente equivocados. Cady relata casos de gente que se estrella contra un problema con NLP y acaba resolviéndolo mejor con expresiones regulares.

Puntos a tener en cuenta antes de intentarlo:

- Si los datos tienen estructura regular, probablemente puedas extraer lo que necesitas sin NLP.
- El NLP es muy eficaz en tareas como determinar si dos documentos tienen contenido similar, porque algo tan simple como la frecuencia de palabras es muy informativo.
- Extraer hechos de documentos es casi imposible salvo que el lenguaje esté estandarizado (Wikipedia, contratos legales); no se consigue con algo como Twitter.
- Suele ser difícil entender por qué un algoritmo de NLP actuó como lo hizo.
- El NLP normalmente requiere mucha cantidad de datos de entrenamiento.

## La gran división: lenguaje frente a estadística
Existen dos escuelas que usan técnicas muy distintas y a veces enfrentadas. El NLP *lingüístico* busca entender el lenguaje como lenguaje (identificar verbos, analizar la estructura de la frase); suena bien pero es asombrosamente difícil por las mil formas en que los humanos rompen las reglas de su idioma. El NLP *estadístico* usa corpus enormes para hallar patrones: notar que "dog" y "bark" aparecen juntos, o que "Nigerian prince" es más frecuente en correos de lo que el azar dictaría.

En la era de los conjuntos de datos masivos (como la web) esta división se acentúa y el NLP estadístico lleva ventaja: los mejores traductores automáticos (Google) son principalmente estadísticos, entrenados con miles de ejemplos de traducción humana. Los lingüistas protestan porque esto esquiva el problema científico de cómo procesa el cerebro el lenguaje, pero los resultados suelen ser mejores. La contrapartida es que entrenar algo así requiere un corpus y algoritmos a medida fuera del alcance de casi todos.

## Ejemplo: análisis de sentimiento sobre artículos bursátiles
El capítulo muestra un script con `nltk` (*natural language toolkit*): se fija el *ticker* de una acción, se descargan artículos recientes, se clasifican como positivos o negativos y se cuenta cuántos caen en cada categoría. El flujo esencial encadena cuatro funciones: obtener URLs, extraer el contenido del HTML, convertir el texto en una bolsa de palabras y contar palabras "buenas" frente a "malas" usando los synsets de WordNet para "good"/"up" y "bad"/"down". La pieza clave del preprocesado:

```python
def text_to_bag(txt):
    # texto -> bolsa de lemas, sin stop words
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.tokenize.word_tokenize(txt.lower())
    words = [t for t in tokens if t.isalpha()]
    lemmas = [lemmatizer.lemmatize(w) for w in words]
    stop = set(stopwords.words('english'))
    nostops = [l for l in lemmas if l not in stop]
    return nltk.FreqDist(nostops)
```

## Software y datasets
El NLP es computacionalmente ineficiente: incluso saber si una palabra es un sustantivo exige consultar el léxico completo del idioma, y analizar el significado de una frase crece exponencialmente con las ambigüedades (que casi siempre existen), sin contar erratas, jerga y reglas rotas. Existen datasets lingüísticos de dominio público que catalogan definiciones, sinónimos y reglas gramaticales. Destaca **WordNet**, base léxica del inglés cuyo concepto central es el *synset*: un conjunto de palabras con significado aproximadamente equivalente. Pasar cada palabra a su synset permite comparar si dos frases hablan de lo mismo con términos distintos y desambiguar palabras polisémicas como "run".

## Tokenización
Toda tarea de NLP empieza partiendo el texto en sus partes constituyentes (normalmente palabras): la *tokenización*. Se complica por la puntuación y las contracciones: ¿"that's" es una palabra o dos?, y si son dos, ¿la segunda es "is" o "'s"? Se complica aún más si los tokens son frases en lugar de palabras.

## Concepto central: bag-of-words
El concepto más básico del NLP es la *bag-of-words* o distribución de frecuencias: una forma de convertir texto libre (un tweet, un documento) en un vector numérico apto para machine learning. Hay una dimensión por cada palabra del idioma, y la puntuación del documento en la dimensión n es el número de veces que aparece la palabra n. El texto se vuelve un vector en un espacio de altísima dimensión.

En Google, Cady aprendió que así funcionaba parte del algoritmo de búsqueda: se condensa cada web en una bag-of-words normalizada; al llegar una consulta se vectoriza también y se toma su producto escalar con los vectores de las páginas. Esto es la *cosine similarity*, porque el producto escalar de dos vectores normalizados es el coseno del ángulo entre ellos.

Extensiones habituales del vector de palabras:

- Hay un número enorme de palabras e infinitas cadenas posibles: hay que acotarlas.
- Unas palabras son más informativas que otras: hay que ponderarlas.
- Algunas no importan ("I", "is"): son *stop words* que conviene descartar al inicio.
- Una misma palabra tiene muchas formas: unificarlas ("ran", "runs", "running" → "run") es *lemmatización*.
- Varias palabras pueden tener significado similar: usar *synsets* en vez de palabras.
- A veces importan frases más que palabras sueltas: un grupo de n palabras en orden es un *n-grama*.

En la práctica, los vectores se almacenan como un mapa de nombres de palabra a números (un `FreqDist` en Python), no como listas ordenadas con índices. Suelen ser dispersos, así que es más eficiente guardar solo las entradas no nulas. Las operaciones vectoriales (productos escalares) son centrales, y los pipelines convierten los mapas a vectores y matrices dispersas para operaciones de álgebra lineal más complejas.

## Ponderación de palabras: TF-IDF
La primera corrección es que unas palabras importan más que otras. La forma más común es *Term Frequency–Inverse Document Frequency* (TF-IDF). La intuición: las palabras más raras son más importantes. Se calcula el vector contando frecuencias como siempre, pero dividiendo cada conteo por la frecuencia de esa palabra en el corpus de entrenamiento. Eso amortigua las palabras comunes y amplifica las raras que aparecen comparativamente mucho en un documento. Normalmente solo se consideran palabras con una frecuencia mínima en el corpus (cinco apariciones es un umbral común; incluso dos elimina mucho ruido de erratas), para no dar importancia infinita a palabras nuevas ni excesiva a las que aparecen una sola vez.

## n-Gramas
A menudo interesan frases, no palabras sueltas. Un *n-grama* es una secuencia de n palabras consecutivas; un texto de M palabras produce M − n + 1 n-gramas. Se puede hacer bag-of-words de n-gramas, aplicarles TF-IDF o modelarlos con una cadena de Markov, igual que con palabras normales. El problema es que hay demasiados posibles y la mayoría aparece una sola vez (más aún cuanto mayor es n), por lo que se suelen mirar solo los que superan cierta frecuencia en el corpus.

## Stop words
La versión más simple de canonicalización es eliminar las *stop words*: palabras como "the", "it" y "and", no informativas en sí mismas. Son críticas para analizar la estructura de una frase, pero para bag-of-words son ruido. No hay definición absoluta: suelen hallarse tomando las palabras más comunes del corpus y revisándolas a mano, o venir prehechas en la librería. Se vuelven problemáticas con n-gramas: una frase informativa como "to be or not to be" podría desaparecer entera.

## Lemmatización y stemming
La *lemmatización* convierte cada palabra en su *lemma*, la forma base de la que deriva ("running", "ran", "runs" → "run"). Es muy importante en inglés y crítica en idiomas que modifican más sus palabras (el español asigna género a los sustantivos y ajusta los adjetivos; otros idiomas usan "caso"). Su pega es que es muy costosa, porque extraer el lemma requiere conocer la parte de la oración, que a su vez exige analizar la frase. Una alternativa más rápida y menos precisa es el *stemming*: el *stem* es la parte de la palabra que no cambia entre formas ("produce", "producer", "production"… → "produc-"). Los stemmers aplican reglas de pulgar (quitar "ing" o "ation" al final, salvo que queden muy pocas letras) o usan tablas de búsqueda.

## Sinónimos
Lo importante es el significado más que las palabras, así que interesa colapsar términos relacionados ("big", "large") en un único identificador: un *synset* (conjunto de sinónimos). Sustituir cada palabra por su synset es una lemmatización mejorada, porque además mezcla "sprinting". El gran escollo: una palabra puede pertenecer a varios synsets (varios significados), por lo que traducir del idioma original a "synset-ese" no siempre es factible.

## Etiquetado gramatical (POS tagging)
Acercándonos a técnicas más lingüísticas, el *POS tagging* identifica si las palabras son sustantivos, verbos, adjetivos, etc. En `nltk`:

```python
>>> nltk.pos_tag(["I", "drink", "milk"])
[('I', 'PRP'), ('drink', 'VBP'), ('milk', 'NN')]
```

## Problemas comunes
- **Búsqueda**: se distingue entre navegacional (localizar un documento concreto) y de investigación (el usuario no sabe qué documentos son relevantes). Se implementa vectorizando consulta y documentos y comparando con *cosine similarity*: (1) normalizar cada vector a suma de cuadrados 1.0, (2) producto escalar de la consulta con cada vector del corpus. Da 1.0 si son idénticos y 0.0 si no comparten palabras; en bag-of-words nunca es negativa porque no hay conteos negativos.
- **Análisis de sentimiento**: medir el tono (positivo, negativo, neutro). Lo simple usa listas de palabras clave hechas a mano; algo más sofisticado mete bag-of-words en pipelines de ML entrenados con ejemplos etiquetados, lo que identifica palabras y pesos por sí solo y, con n-gramas, frases como "nose dive". Lo más avanzado parsea la frase para saber qué entidad se describe, aunque se puede sortear analizando fragmentos pequeños (una frase suele tener un sentimiento predominante).
- **Reconocimiento de entidades y modelado de temas**: el *named entity recognition* extrae entidades concretas (personas) y se apoya mucho en POS tagging, porque suelen ser los sustantivos propios. El *topic modeling* busca temas amplios: un documento es combinación de varios temas y las palabras que aparecen juntas suelen pertenecer al mismo tema. La herramienta habitual es *latent semantic analysis* (LSA), basada en *singular value decomposition* (SVD); se prefiere SVD a PCA porque fuerza componentes ortogonales, evitando que un tema se exprese como combinación de otros.

## NLP avanzado: árboles sintácticos, conocimiento y comprensión
Responder preguntas concretas ("¿con quién sale John?") exige ir más allá de bag-of-words. Para ello se crean *bases de conocimiento* que almacenan hechos en un formato consultable. La teoría de las bases de datos relacionales ya funcionaba esencialmente como una base de conocimiento con consultas lógicas: una tabla `IsParentOf` con columnas padre/hijo permite preguntas tipo SQL. Rellenar esas tablas a partir de texto obliga a saber de antemano qué relaciones interesan y cómo parsearlas, y hay reglas lógicas que una RDB no captura (cada hijo tiene como mucho dos padres). Las bases de conocimiento modernas añaden reglas lógicas sobre las categorías y relaciones del dominio: esas colecciones de categorías y reglas se llaman *ontologías*.

## Ideas clave
- Antes de usar NLP, pregúntate si lo necesitas: si los datos tienen estructura regular, las expresiones regulares pueden bastar y funcionar mejor.
- Hay dos escuelas: la lingüística (entender el lenguaje, muy difícil) y la estadística (patrones en corpus masivos), que domina en la era de los datos grandes.
- La *bag-of-words* convierte texto en vectores numéricos y es la base del NLP práctico; casi todo cabe en ese paradigma.
- La *cosine similarity* (producto escalar de vectores normalizados) compara documentos y sustenta la búsqueda.
- TF-IDF pondera palabras dando más importancia a las raras; los n-gramas capturan frases.
- Canonicalizar el texto incluye quitar *stop words*, lemmatizar/stemming y mapear a *synsets* (WordNet) para reducir ambigüedad.
- Problemas típicos: búsqueda, análisis de sentimiento, reconocimiento de entidades (apoyado en POS tagging) y modelado de temas con LSA/SVD.
- Ir más allá de bag-of-words lleva a bases de conocimiento y ontologías, terreno complejo reservado a especialistas.
