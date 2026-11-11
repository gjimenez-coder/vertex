# Categorizing and Tagging Words (Categorizar y etiquetar palabras) — Estudio

## Tarjetas de repaso

P: ¿Qué es el POS tagging?
R: El etiquetado gramatical: clasificar cada palabra de un texto según su clase léxica (nombre, verbo, adjetivo, etc.) y asignarle una etiqueta corta como `NN` o `VB`. Es el segundo paso del pipeline de NLP, tras la tokenización.

P: ¿Qué es un tagset?
R: El conjunto de etiquetas usado en una tarea de etiquetado. No todos los corpus usan el mismo; NLTK ofrece un mapeo a un tagset simplificado con `simplify_tags=True`.

P: ¿Por qué las clases léxicas no son una invención ociosa de los gramáticos?
R: Emergen del análisis de la distribución de las palabras en el texto y son útiles para predecir el comportamiento de palabras nuevas, analizar corpus y en sistemas de texto a voz.

P: ¿Cómo se representa un token etiquetado en NLTK?
R: Como una tupla `(token, tag)`. `nltk.tag.str2tuple('fly/NN')` produce `('fly', 'NN')`.

P: ¿Qué métodos uniformes ofrecen los corpus etiquetados de NLTK?
R: `tagged_words()` para todos, y `tagged_sents()` si están segmentados en frases (útil para entrenar taggers), ocultando las diferencias de formato.

P: ¿Por qué un diccionario de Python es la estructura natural para el etiquetado?
R: Porque el etiquetado es un mapeo de palabras a etiquetas; un diccionario se indexa con una clave (la palabra) y devuelve un valor (la etiqueta), a diferencia de una lista indexada por enteros.

P: ¿Qué es un `defaultdict` y para qué sirve en tareas de lenguaje?
R: Un diccionario que crea automáticamente un valor por defecto al acceder a una clave nueva (`int`→0, `list`→[], o vía función). Sirve para contar, indexar y para mapear palabras poco frecuentes a un token `UNK`.

P: ¿Cuál es la precisión aproximada del default tagger, el regexp tagger y el lookup tagger (100 palabras) sobre Brown news?
R: Default (`NN` para todo) ~0.13; regexp (patrones de escritura) ~0.20; lookup con las 100 palabras más frecuentes ~0.46.

P: ¿Qué es el backoff al combinar taggers?
R: Usar el tagger más preciso cuando puede etiquetar y recurrir a otro de mayor cobertura cuando no, encadenándolos con el parámetro `backoff`.

P: ¿Qué es un n-gram tagger?
R: Un tagger cuyo contexto es la palabra actual más las etiquetas de los *n*-1 tokens previos (1-gram unigrama, 2-gram bigrama, 3-gram trigrama); elige el tag más probable en ese contexto.

P: ¿Qué es el problema de los datos dispersos (sparse data) en el etiquetado por n-gramas?
R: Al crecer *n* aumenta la especificidad del contexto y la probabilidad de encontrar contextos no vistos, generando un compromiso entre precisión y cobertura.

P: ¿Qué es un gold standard y por qué importa la evaluación?
R: Un corpus anotado manualmente aceptado como referencia; el tagger acierta si su etiqueta coincide con la del gold standard. Importa porque los errores de un módulo se multiplican aguas abajo en el pipeline.

P: ¿En qué consiste el Brill tagging?
R: Una forma de transformation-based learning: adivinar un tag inicial para cada palabra y luego corregir errores aplicando reglas de la plantilla "reemplazar T1 por T2 en el contexto C", puntuadas por beneficio neto. Rinde bien con modelos minúsculos y reglas interpretables.

P: ¿Qué tres tipos de pistas usan los lingüistas para determinar la categoría de una palabra?
R: Morfológicas (sufijos como `-ness`, `-ment`, `-ing`), sintácticas (contextos típicos, p. ej. un adjetivo antes de un nombre o tras *be*/*very*) y semánticas (el significado, tratadas con recelo).

P: ¿Qué diferencia una clase abierta de una cerrada?
R: Los nombres son clase abierta (los idiomas incorporan términos nuevos constantemente: muggle, SARS); las preposiciones son clase cerrada, con un conjunto limitado que cambia muy lentamente.

## Preguntas de autoevaluación

P: ¿Por qué los sistemas de texto a voz suelen hacer POS tagging? (sección 5.1)
R: Porque los homónimos se pronuncian distinto según su categoría: en "They refuse to permit us...", refUSE (verbo, "negar") y REFuse (nombre, "basura") requieren pronunciación distinta, que depende de su etiqueta.

P: ¿Qué hace el método `text.similar(w)` y qué justifica sobre las categorías? (sección 5.1)
R: Busca contextos w1·w·w2 y devuelve palabras que aparecen en el mismo contexto (p. ej. `woman` encuentra nombres, `bought` verbos). Justifica que las categorías léxicas tienen base distribucional.

P: Al acceder a una clave inexistente en un diccionario normal, ¿qué ocurre, y cómo lo evita un `defaultdict`? (sección 5.3)
R: Un diccionario normal lanza `KeyError`; un `defaultdict` crea automáticamente un valor por defecto para la clave nueva, evitando el error.

P: ¿Por qué entrenar y evaluar un unigram tagger sobre los mismos datos da un resultado engañoso? (sección 5.5)
R: Da ~0.93, pero mide memorización, no utilidad real. Separando datos (p. ej. 90% entrenamiento, 10% prueba) baja a ~0.81, una medida honesta de su rendimiento con texto nuevo.

P: ¿Por qué la precisión global de un BigramTagger puede caer a ~0.10 ante palabras nuevas? (sección 5.5)
R: Ante una palabra nueva devuelve `None` y, al perder el contexto (las etiquetas previas), falla el resto de la frase, arrastrando el error.

P: ¿Qué cota inferior de rendimiento tiene un trigram tagger sobre el Brown y de dónde sale? (sección 5.5)
R: Empíricamente, ~1 de cada 20 trigramas del Brown es ambiguo (5%), lo que fija una cota inferior; otra cota viene del desacuerdo entre anotadores humanos.

P: ¿Qué dos problemas de los n-gram taggers resuelve el Brill tagging? (sección 5.6)
R: El tamaño de sus tablas (arrays dispersos de millones de entradas) y que solo usan tags del contexto, no las palabras. El Brill rinde bien con modelos minúsculos y reglas interpretables.

P: ¿Por qué se dice que no existe una forma "correcta" de etiquetar? (sección 5.7)
R: Los tagsets comparten categorías básicas pero difieren en cuán fino dividen y cómo definen las categorías; solo hay formas más o menos útiles según el objetivo. Un tagset fino implica además un análisis morfológico implícito.

## Checklist

Puntos a dominar:

- Explicar qué es el POS tagging y su lugar en el pipeline de NLP.
- Distinguir tagset completo del Brown frente al tagset simplificado (ADJ, ADV, CNJ, DET, MOD, N, NP, NUM, PRO, P, TO, V, VD, VG, VN, WH).
- Representar y leer corpus etiquetados con `tagged_words()` y `tagged_sents()`.
- Usar diccionarios, `defaultdict`, `nltk.Index` y `nltk.FreqDist` para mapear palabras a propiedades.
- Construir y comparar la batería de taggers: default, regexp, lookup, unigrama y n-grama.
- Encadenar taggers con `backoff` para equilibrar precisión y cobertura.
- Separar datos de entrenamiento y prueba y evaluar contra un gold standard.
- Reconocer el problema de los datos dispersos y el compromiso precisión/cobertura al crecer *n*.
- Entender el Brill tagging (transformation-based learning) y la ventaja de sus reglas interpretables.
- Determinar la categoría de una palabra con pistas morfológicas, sintácticas y semánticas, y distinguir clases abiertas de cerradas.
