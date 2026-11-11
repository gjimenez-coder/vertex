# Natural Language Processing (Procesamiento de lenguaje natural) — Estudio

## Tarjetas de repaso

P: ¿Qué es el NLP según el capítulo? / R: El conjunto de técnicas para trabajar con lenguaje humano (filtrar spam, medir sentimiento, agrupar documentos por tema), aplicables también a logs o bioinformática.

P: ¿Cuál es la tesis central del capítulo sobre el alcance práctico del NLP? / R: La mayoría del trabajo real de NLP cabe dentro del paradigma de la bag-of-words y sus extensiones; ir más allá lo vuelve enormemente complejo y conviene dejarlo a especialistas.

P: ¿Qué diferencia al NLP lingüístico del estadístico? / R: El lingüístico busca entender el lenguaje como lenguaje (verbos, estructura de la frase), muy difícil; el estadístico usa corpus enormes para hallar patrones y domina en la era de los datos grandes.

P: ¿Qué es la bag-of-words? / R: Una distribución de frecuencias que convierte texto libre en un vector numérico con una dimensión por palabra, donde cada componente cuenta las veces que aparece esa palabra.

P: ¿Qué es la cosine similarity y por qué se usa? / R: El producto escalar de dos vectores normalizados (el coseno del ángulo entre ellos); compara documentos y sustenta la búsqueda, dando 1.0 si son idénticos y 0.0 si no comparten palabras.

P: ¿Qué es TF-IDF y cuál es su intuición? / R: Term Frequency–Inverse Document Frequency; pondera dividiendo cada conteo por la frecuencia de la palabra en el corpus, amortiguando las comunes y amplificando las raras, porque las palabras más raras son más importantes.

P: ¿Qué es un n-grama? / R: Una secuencia de n palabras consecutivas; un texto de M palabras produce M − n + 1 n-gramas y puede tratarse con bag-of-words, TF-IDF o una cadena de Markov.

P: ¿Qué son las stop words? / R: Palabras no informativas en sí mismas ("the", "it", "and") que se descartan en bag-of-words; se vuelven problemáticas con n-gramas porque una frase como "to be or not to be" podría desaparecer entera.

P: ¿Qué diferencia hay entre lemmatización y stemming? / R: La lemmatización reduce cada palabra a su lemma (forma base) y es precisa pero costosa; el stemming aplica reglas rápidas para quedarse con el stem (parte invariable), más rápido y menos preciso.

P: ¿Qué es un synset y qué base léxica lo usa? / R: Un conjunto de palabras de significado aproximadamente equivalente; es el concepto central de WordNet y permite comparar frases que dicen lo mismo con términos distintos y desambiguar polisemias.

P: ¿Qué hace el POS tagging? / R: Identifica la parte de la oración de cada palabra (sustantivo, verbo, adjetivo, etc.); en nltk se obtiene con nltk.pos_tag.

P: ¿Qué es la tokenización y por qué se complica? / R: Partir el texto en sus partes constituyentes (normalmente palabras); se complica por la puntuación y las contracciones (¿"that's" es una o dos palabras?).

P: ¿En qué consiste el named entity recognition y en qué se apoya? / R: Extrae entidades concretas (como personas) y se apoya mucho en POS tagging, porque suelen ser sustantivos propios.

P: ¿Qué es el topic modeling y qué herramienta se usa? / R: Busca temas amplios asumiendo que un documento combina varios temas y que las palabras que aparecen juntas pertenecen al mismo; la herramienta habitual es LSA, basada en SVD.

P: ¿Qué son las bases de conocimiento y las ontologías? / R: Las bases de conocimiento almacenan hechos en un formato consultable; las ontologías son las colecciones de categorías y reglas lógicas del dominio que las bases de conocimiento modernas añaden.

## Preguntas de autoevaluación

P: ¿Por qué el capítulo recomienda preguntarse primero si realmente se necesita NLP? / R: Porque el NLP es difícil de implementar, propenso a errores extraños y requiere muchos datos de entrenamiento; si los datos tienen estructura regular, las expresiones regulares pueden bastar y funcionar mejor. (Sección "¿Necesito siquiera NLP?")

P: ¿Por qué el NLP estadístico lleva ventaja en la era de los datos masivos? / R: Porque con corpus enormes se hallan patrones y se entrenan sistemas como los traductores de Google (principalmente estadísticos) que dan mejores resultados, aunque esquiven cómo procesa el lenguaje el cerebro. (Sección "La gran división: lenguaje frente a estadística")

P: ¿Cómo convierte la bag-of-words un documento en algo apto para machine learning y cómo se almacena en la práctica? / R: Lo representa como un vector en un espacio de altísima dimensión con una dimensión por palabra; en la práctica se guarda como un mapa de palabra a número (un FreqDist), disperso, conservando solo entradas no nulas. (Sección "Concepto central: bag-of-words")

P: ¿Cómo implementa la búsqueda el enfoque de bag-of-words? / R: Vectorizando consulta y documentos, normalizando cada vector a suma de cuadrados 1.0 y tomando el producto escalar de la consulta con cada vector del corpus (cosine similarity). (Sección "Problemas comunes")

P: ¿Por qué suele fijarse un umbral de frecuencia mínima en TF-IDF y en los n-gramas? / R: Para evitar dar importancia infinita a palabras nuevas o ruido de erratas en TF-IDF, y porque hay demasiados n-gramas posibles y la mayoría aparece una sola vez. (Secciones "Ponderación de palabras: TF-IDF" y "n-Gramas")

P: ¿Cuál es el gran escollo al sustituir palabras por synsets? / R: Que una palabra puede pertenecer a varios synsets (varios significados), por lo que traducir del idioma original a "synset-ese" no siempre es factible. (Sección "Sinónimos")

P: ¿Por qué se prefiere SVD a PCA en el modelado de temas con LSA? / R: Porque SVD fuerza componentes ortogonales, evitando que un tema se exprese como combinación de otros. (Sección "Problemas comunes")

P: ¿Por qué la lemmatización es costosa frente al stemming? / R: Porque extraer el lemma requiere conocer la parte de la oración, lo que a su vez exige analizar la frase; el stemming evita eso aplicando reglas rápidas de pulgar o tablas de búsqueda. (Sección "Lemmatización y stemming")

## Puntos a dominar

- Decidir si un problema necesita NLP o si basta con estructura regular y expresiones regulares.
- Distinguir el NLP lingüístico del estadístico y saber por qué este último domina con datos masivos.
- Explicar la bag-of-words como vectorización de texto y su almacenamiento disperso (FreqDist).
- Calcular e interpretar la cosine similarity entre consulta y documentos para búsqueda.
- Aplicar TF-IDF entendiendo que las palabras raras pesan más, con umbral de frecuencia mínima.
- Construir y usar n-gramas, y reconocer el riesgo de eliminar stop words sobre ellos.
- Canonicalizar texto: tokenizar, quitar stop words, lemmatizar o stemming y mapear a synsets (WordNet).
- Identificar los problemas típicos: búsqueda, análisis de sentimiento, named entity recognition (con POS tagging) y topic modeling (LSA/SVD).
- Reconocer cuándo se supera la bag-of-words y entran bases de conocimiento y ontologías.
