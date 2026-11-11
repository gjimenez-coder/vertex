# Representing and Mining Text (Representación y minería de texto) — Estudio

## Tarjetas de repaso

P: ¿Por qué suele ser más simple adaptar la representación de los datos a las herramientas que construir herramientas nuevas?
R: Porque las herramientas existentes están bien entendidas y son numerosas; el mundo rara vez entrega los datos en el formato de vector de características que esperan los algoritmos.

P: ¿Por qué se llama al texto dato "no estructurado" si en realidad tiene estructura?
R: Porque carece de la estructura habitual de tablas con campos de significado fijo; su estructura es lingüística, pensada para humanos y no para máquinas.

P: ¿Qué hace que el texto sea un dato "sucio" y dependiente del contexto?
R: La gente escribe de forma agramatical, con faltas, abreviaturas impredecibles y puntuación errática; además hay sinónimos, homógrafos y palabras como *incredible* que pueden ser positivas o negativas según el contexto.

P: ¿En qué consiste la representación bag of words?
R: Tratar cada documento como una colección de palabras, ignorando gramática, orden, estructura de la frase y normalmente puntuación; cada palabra es una posible característica.

P: ¿Qué tres pasos de procesamiento básico se aplican a las palabras antes de contarlas?
R: Normalización de mayúsculas/minúsculas (todo a minúscula), stemming (eliminar sufijos, p. ej. *announces/announced/announcing* → *announc*) y eliminación de stopwords (*the, and, of, on*).

P: ¿Por qué la eliminación de stopwords no siempre conviene?
R: Porque en ciertos casos, como los títulos, las palabras comunes pueden ser muy significativas: *The Road* frente a *On the Road*.

P: ¿Qué mide la inverse document frequency (IDF) y cómo se comporta?
R: Mide la rareza de un término en el corpus; es alta cuando el término es muy raro y decae hasta estabilizarse en 1.0 para términos muy frecuentes (las stopwords tienen IDF cercana a 1). IDF(t) = 1 + log(Nº total de documentos / Nº de documentos que contienen t).

P: ¿Cómo se calcula TFIDF y qué pondera?
R: TFIDF(t, d) = TF(t, d) × IDF(t); pondera cada término por su frecuencia en el documento y por su rareza en el corpus. El valor es específico del documento, mientras que la IDF depende de todo el corpus.

P: ¿Qué dos consideraciones opuestas se tienen con la esparcidad de un término?
R: Un término no debe ser demasiado raro (inútil para clustering, de ahí un límite inferior de documentos) ni demasiado común (no distingue nada, de ahí un límite superior).

P: ¿Qué técnica de similitud se usa para construir un buscador por vecino más cercano sobre vectores TFIDF?
R: La cosine similarity, muy usada en clasificación de texto; en el ejemplo, el documento más cercano a la consulta fue Charlie Parker (similitud 0.135).

P: ¿Qué son los n-gramas y cuál es su principal ventaja y desventaja?
R: Secuencias de palabras adyacentes tomadas como términos (bi-gramas los pares) para conservar algo del orden. Ventaja: fáciles de generar, sin conocimiento lingüístico. Desventaja: inflan enormemente el conjunto de características.

P: ¿Qué distingue a la extracción de entidades nombradas de bag of words y n-gramas?
R: Reconoce nombres propios significativos (*Silicon Valley*, *New York Mets*) y normaliza variantes; es intensiva en conocimiento: debe entrenarse con un gran corpus o codificarse a mano, y su calidad varía por dominio.

P: ¿Qué son los topic models y qué ventaja aportan?
R: Insertan una capa de temas entre el documento y el modelo (el clasificador se define sobre temas, no palabras); permiten que una consulta use términos que no coinciden exactamente pero mapean al mismo tema. Métodos: Latent Semantic Indexing y Latent Dirichlet Allocation.

P: En el caso de noticias financieras, ¿cuál era el propósito real y qué umbral se fijó?
R: El propósito no era operar en bolsa sino recomendar noticias (information triage). Umbral del 5%: subida ≥5% es *surge*, bajada ≥5% es *plunge*, entre −2.5% y 2.5% es *stable*; las zonas grises se dejan sin etiquetar.

## Preguntas de autoevaluación

P: ¿Por qué es importante el texto para el negocio y dónde se encuentra?
R: Porque gran parte de la comunicación humana y del feedback del cliente vive en forma textual (reseñas, formularios, correos, quejas, registros médicos, feeds de Twitter, blogs). "Escuchar al cliente" a menudo significa leer texto, aunque algunas actitudes se capturen explícitamente (valoraciones, click-through, encuestas). (Sección: Por qué el texto importa y por qué es difícil)

P: ¿Qué diferencia hay entre usar la presencia binaria (0/1) y la frecuencia de término (term frequency)?
R: La forma más básica de bag of words marca 1 si el token está y 0 si no; se pasa a la cuenta de ocurrencias cuando la importancia de un término crece con cuántas veces aparece en el documento. (Sección: Representación: bag of words y frecuencia de términos)

P: ¿Por qué algunos sistemas normalizan las frecuencias respecto a la longitud del documento?
R: Porque un documento largo no es necesariamente más relevante que uno corto solo por tener más palabras; se divide, por ejemplo, por el total de palabras. (Sección: Representación: bag of words y frecuencia de términos)

P: En el ejemplo de los músicos de jazz, ¿qué términos recibieron más peso y por qué?
R: *latin*, *famous* y *kansas*, por ser los más raros en el corpus, obtuvieron los pesos más altos; *jazz* y *play*, muy frecuentes, no recibieron empuje (casi stopwords en ese corpus). (Sección: Ejemplo: músicos de jazz)

P: ¿Qué relación plantea el texto entre IDF y entropía?
R: No son idénticas pero están relacionadas: ambas miden cuán "mezclado" está un conjunto respecto a una propiedad. Descartando la constante, IDF(t) equivale a −log(p), y la entropía de un conjunto partido por t puede expresarse como el valor esperado de IDF(t) e IDF(not_t). (Sección: Relación entre IDF y entropía)

P: ¿Qué simplificaciones de formulación se aplicaron para predecir el precio de las acciones a partir de noticias?
R: Predecir el efecto el mismo día, solo la dirección reducida a change/no change, solo cambios grandes, y asumir que solo las noticias que mencionan una acción la afectan (acotando el radio causal). (Sección: Ejemplo: minería de noticias para predecir el precio de acciones)

P: ¿Qué resultados mostraron las curvas ROC y de lift en el caso de noticias financieras?
R: Las ROC de Logistic Regression, Naive Bayes y un árbol se alejaron de la diagonal con AUC claramente por encima de 0.5 (hay señal predictiva); Logistic Regression y Naive Bayes rindieron parecido y el árbol peor. En el top 20% de historias el lift fue ≈2.0 (el doble de precisión que en la población). (Sección: Ejemplo: minería de noticias para predecir el precio de acciones)

P: Según el capítulo, ¿qué técnicas darían más fuerza que bag of words en la tarea de noticias y por qué?
R: La extracción de entidades nombradas y, mejor aún, el event parsing, porque las noticias narran eventos y modificadores como *not*, *despite* o *expect* pueden no estar adyacentes a lo que modifican. (Sección: Ejemplo: minería de noticias para predecir el precio de acciones)

## Puntos a dominar

- Entender la representation engineering como etapa clave: el mundo no entrega vectores de características y suele ser más simple adaptar los datos a las herramientas.
- Explicar por qué el texto es "no estructurado", sucio y dependiente del contexto, y qué implica eso para el preprocesamiento.
- Describir bag of words y aplicar el preprocesamiento típico: normalización de mayúsculas, stemming y eliminación de stopwords (sabiendo cuándo las stopwords sí importan).
- Calcular e interpretar TF, IDF y TFIDF, y relacionar los umbrales mínimo/máximo de documentos con la esparcidad.
- Usar cosine similarity sobre vectores TFIDF para recuperación por vecino más cercano.
- Distinguir cuándo recurrir a n-gramas, extracción de entidades nombradas o topic models, con sus ventajas y costes.
- Reconocer que gran parte del trabajo del caso de noticias es formulación del problema (qué predecir, qué umbral, qué radio causal) y que hay señal predictiva real aun con representaciones primitivas.
