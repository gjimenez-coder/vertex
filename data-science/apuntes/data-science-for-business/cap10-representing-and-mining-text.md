# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 10 — Representing and Mining Text (Representación y minería de texto)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

Este capítulo aborda una etapa del proceso de minería de datos que hasta ahora se había pasado por alto: la preparación de los datos. El mundo rara vez entrega la información en el formato de vector de características que esperan los algoritmos, así que el científico de datos debe o bien adaptar la representación de los datos a las herramientas, o bien construir herramientas nuevas. Lo más simple suele ser lo primero, porque las herramientas existentes están bien entendidas y son numerosas.

El tipo de dato elegido para ilustrar esto es el texto, hoy omnipresente en Internet (páginas, Twitter, email, reseñas, blogs) y en sistemas heredados (registros médicos, quejas de clientes, reparaciones). El texto es importante porque gran parte de la comunicación humana y del feedback de los clientes vive en forma textual, pero es difícil: se le llama dato "no estructurado" porque su estructura es lingüística —pensada para humanos, no para máquinas—. Es además sucio (faltas de ortografía, abreviaturas, puntuación errática) y depende fuertemente del contexto (una misma palabra como *incredible* puede ser positiva o negativa).

La tesis central es que, con un buen preprocesamiento, el texto se puede convertir en vectores de características aptos para minería. Sales sabiendo cómo transformar una colección de documentos en datos mediante bag of words, cómo ponderar términos con TFIDF, y qué técnicas superan a bag of words cuando hace falta más sofisticación (n-grams, extracción de entidades nombradas, topic models). El capítulo cierra con un caso completo: predecir movimientos de precio de acciones a partir de noticias financieras.

## El ejemplo que recorre el capítulo

El capítulo usa dos ejemplos ilustrativos. Primero, un corpus pequeño de 15 biografías de músicos de jazz de Wikipedia, con el que se muestra paso a paso cómo se representa y recupera texto. Después, un caso extenso de minería de noticias financieras de 1999 para predecir cambios en el precio de las acciones, que reúne muchos elementos reales de procesamiento de texto y formulación del problema.

## Por qué el texto importa y por qué es difícil

El texto está en todas partes. Muchas aplicaciones heredadas aún producen texto como medio de comunicación entre personas (registros médicos, logs de quejas, consultas de producto, registros de reparación). Internet, pese a ser el hogar de los "nuevos medios", contiene grandes cantidades de texto (páginas personales, feeds de Twitter, email, descripciones de producto, comentarios, blogs); detrás de buscadores como Google y Bing hay data science orientada a texto. En negocio, entender el feedback del cliente suele exigir leer lo que escribe: reseñas, formularios de opinión, correos. Aunque algunas actitudes se capturan explícitamente (valoraciones de cinco estrellas, click-through, conversiones, encuestas), "escuchar al cliente" a menudo significa leer texto.

El texto se llama "no estructurado" porque carece de la estructura habitual de los datos (tablas de registros con campos de significado fijo). En realidad tiene mucha estructura, pero es lingüística. Las palabras tienen longitudes variables, los campos tienen números variables de palabras, y a veces el orden importa y a veces no. Como dato, el texto es relativamente sucio: la gente escribe de forma agramatical, comete faltas, pega palabras, abrevia de forma impredecible y puntúa al azar. Incluso cuando es impecable, puede contener sinónimos (varias palabras con el mismo significado) y homógrafos (una grafía compartida por varias palabras con significados distintos). La terminología de un dominio puede ser inútil o conflictiva en otro. Por todo esto, el texto necesita bastante preprocesamiento antes de servir de entrada a un algoritmo.

## Representación: bag of words y frecuencia de términos

La estrategia general en minería de texto es usar la técnica más simple (y barata) que funcione. La terminología proviene de la recuperación de información (IR): un *documento* es cualquier pieza de texto (una frase o un informe de 100 páginas); se compone de *tokens* o *términos* (por ahora, palabras); y una colección de documentos es un *corpus*.

El enfoque básico es *bag of words*: tratar cada documento como una simple colección de palabras, ignorando gramática, orden, estructura de la frase y (normalmente) puntuación. Cada palabra es una posible característica. La representación es directa, barata de generar y funciona bien en muchas tareas. En su forma más básica, cada documento se representa con un 1 (el token está) o un 0 (no está) para cada término.

El siguiente paso es usar la cuenta de ocurrencias (*term frequency*) en lugar de solo 0/1, cuando la importancia de un término crece con cuántas veces aparece. Con tres documentos de ejemplo (p. ej. *d1: "jazz music has a swing rhythm"*) se construye una tabla de cuentas de términos.

Antes de contar se aplica procesamiento básico a las palabras:

- Normalización de mayúsculas/minúsculas: todo a minúscula, para que *Skype* y *SKYPE* cuenten igual (variaciones como iPhone/iphone/IPHONE son muy comunes).
- *Stemming*: eliminar sufijos, de modo que *announces*, *announced* y *announcing* se reducen al término *announc*, y *directors* a *director*.
- Eliminación de *stopwords*: palabras muy comunes del idioma (*the*, *and*, *of*, *on*) que se suelen quitar.

Cuidado: la eliminación de stopwords no siempre conviene. En títulos las palabras comunes pueden ser muy significativas (*The Road* frente a *On the Road*). Los números (p. ej. "$8.5") suelen descartarse como detalles sin importancia, pero el propósito de la representación debe decidirlo; términos como "4TB" o "1Q13" pueden ser irrelevantes o modificadores críticos según el caso. Además, algunos sistemas normalizan las frecuencias respecto a la longitud del documento (p. ej. dividiendo por el total de palabras), porque un documento largo no es necesariamente más relevante que uno corto solo por tener más palabras.

## Esparcidad y TFIDF

La frecuencia de término mide cuán prevalente es un término en un documento; también interesa cuán común es en todo el corpus. Hay dos consideraciones opuestas. Un término no debería ser demasiado raro: una palabra que aparece en un solo documento puede importar para recuperación (el usuario podría buscarla), pero es inútil para clustering. Por eso los sistemas suelen imponer un límite inferior al número de documentos en que un término debe aparecer. En sentido contrario, un término no debería ser demasiado común: uno que aparece en todos los documentos no distingue nada, así que se suele eliminar con un límite superior.

Muchos sistemas además ponderan según la distribución del término en el corpus: cuantos menos documentos lo contengan, más significativo es en los que aparece. Esta esparcidad se mide con la *inverse document frequency* (IDF):

```
IDF(t) = 1 + log( Nº total de documentos / Nº de documentos que contienen t )
```

La IDF es el "empuje" que recibe un término por ser raro: es alta cuando el término es muy raro y decae rápido hasta estabilizarse en 1.0 para los términos muy frecuentes (las stopwords tienen IDF cercana a 1).

La representación más popular combina ambas: TFIDF es el producto de la frecuencia de término por la IDF:

```
TFIDF(t, d) = TF(t, d) × IDF(t)
```

El valor TFIDF es específico de un documento *d*, mientras que la IDF depende de todo el corpus. Tras stemming y eliminación de stopwords, las cuentas dentro de los documentos dan los TF y las cuentas entre documentos dan los IDF. Cada documento se convierte así en un vector de características y el corpus en un conjunto de vectores, apto para clasificación, clustering o recuperación. Como hay muchísimos términos posibles, suele aplicarse selección de características (umbrales mínimos/máximos de cuenta, o medidas como information gain para rankear términos). Bag of words con TFIDF es muy común pero no necesariamente óptimo; los valores pueden ser binarios, TF o TFIDF, con o sin normalización, y los científicos de datos experimentan con varias representaciones.

## Ejemplo: músicos de jazz

Con un corpus de 15 biografías de músicos de jazz de Wikipedia (casi 2.000 características tras stemming y stopwords), se procesa la frase de ejemplo "Famous jazz saxophonist born in Kansas who played bebop and latin" como si fuera una consulta a un buscador. Se aplica stemming (imperfecto: produce *kansa* y *famou*, lo cual no importa si es consistente), se quitan stopwords (*in*, *and*) y se normaliza. Al multiplicar por la IDF, *jazz* y *play* —muy frecuentes en este corpus— no reciben empuje (son casi stopwords aquí), mientras que *latin*, *famous* y *kansas* —las más raras— obtienen los pesos más altos.

Con ese vector TFIDF se construye un buscador simple por vecino más cercano, midiendo la similitud de la consulta con cada biografía mediante la *cosine similarity* (muy usada en clasificación de texto). El documento más cercano resulta ser Charlie Parker (similitud 0.135), que efectivamente fue saxofonista nacido en Kansas, tocó bebop y a veces combinó otros géneros como el latin.

## Relación entre IDF y entropía

En una sección opcional, el texto muestra que IDF y entropía, aunque no idénticas, están relacionadas: ambas miden cuán "mezclado" está un conjunto respecto a una propiedad. Descartando la constante, IDF(t) equivale a log(1/p) = −log(p), donde *p* es la probabilidad de que un término aparezca en un documento. Definiendo un término espejo *not_t*, la entropía de un conjunto partido por *t* puede expresarse como el valor esperado de IDF(t) e IDF(not_t) según su probabilidad de ocurrencia en el corpus.

## Más allá de bag of words

Bag of words es simple, no requiere parsing sofisticado y rinde sorprendentemente bien, por lo que suele ser la primera opción. Pero a veces hace falta más:

- **N-gramas**: incluir secuencias de palabras adyacentes como términos para conservar algo del orden. Los pares se llaman *bi-gramas*; "bag of n-grams up to three" significa usar palabras individuales, pares y tríos. Son útiles cuando las frases importan aunque sus palabras sueltas no (p. ej. *exceed_analyst_expectation* es más significativo que esas palabras por separado). Ventaja: fáciles de generar, sin conocimiento lingüístico. Desventaja: inflan enormemente el conjunto de características, lo que casi siempre exige selección de características o atención al almacenamiento.
- **Extracción de entidades nombradas**: reconocer nombres propios significativos (*Silicon Valley*, *New York Mets*, *Game of Thrones*) que bag of words o n-gramas no capturan bien. Muchos toolkits incluyen un extractor que anota frases como *persona* u *organización* y normaliza variantes ("HP", "H-P", "Hewlett-Packard"). A diferencia de bag of words y n-gramas, estos extractores son intensivos en conocimiento: deben entrenarse con un gran corpus o codificarse a mano, y su calidad varía por dominio.
- **Topic models**: insertar una capa de temas entre el documento y el modelo. Cada documento es una secuencia de palabras que se mapean a uno o más *temas* aprendidos de los datos (normalmente por minería no supervisada); el clasificador final se define sobre temas, no sobre palabras. Ventaja: una consulta puede usar términos que no coinciden exactamente con los de un documento pero mapean al mismo tema. Métodos: factorización de matrices (Latent Semantic Indexing) y modelos probabilísticos (Latent Dirichlet Allocation). El topic layer puede verse como un clustering de palabras; los temas emergen de regularidades estadísticas y no siempre son inteligibles. Son un tipo de *información latente*, una capa intermedia no observada entre entradas y salidas.

## Ejemplo: minería de noticias para predecir el precio de acciones

La tarea: predecir cambios en el precio de acciones a partir de noticias financieras. Como es difícil predecir el precio con precisión y por adelantado, se simplifica el problema (es tanto un ejercicio de formulación como de minería de texto): se predice el efecto el mismo día; solo la *dirección* del movimiento, reducida a *change*/*no change*; solo cambios *grandes*; y se asume que solo las noticias que mencionan una acción afectan a esa acción (acotando el "radio causal"). Se fija un umbral del 5%: subida ≥5% es *surge*, bajada ≥5% es *plunge*; entre −2.5% y 2.5% es *stable*; las zonas grises intermedias se dejan sin etiquetar para separar mejor las clases. El propósito real no es operar en bolsa sino **recomendar noticias** (*information triage*): señalar las que probablemente provocarán un cambio significativo.

Los datos son dos series temporales enlazadas: un flujo de noticias (cerca de 36.000 historias de 1999, NYSE y NASDAQ, de un estudio previo de Fawcett & Provost, 1999) y los precios diarios. Las noticias son muy ruidosas ("The News Is Messy"): formatos variados, varias noticias no relacionadas en un mismo documento, y etiquetado de acciones imperfecto y demasiado permisivo. El preprocesamiento: medir el precio de apertura a las 10:00 (no a las 9:30, por la volatilidad) y comparar con el cierre de las 16:00; descartar historias sin timestamp; rechazar las que mencionan más de dos acciones; case-normalizar, stemming, quitar stopwords y crear n-gramas hasta dos. Resultan unas 16.000 historias etiquetadas, con reparto de ~75% no change, 13% surge y 12% plunge; al fusionar surge y plunge, 25% son *change*.

Como el propósito quedó abierto, no se hacen cálculos de valor esperado ni gráficos de beneficio; se mira la predecibilidad. Las curvas ROC (validación cruzada de diez pliegues) de Logistic Regression, Naive Bayes y un árbol de clasificación se alejan de la diagonal con AUC claramente por encima de 0.5, así que hay señal predictiva en las noticias. Logistic Regression y Naive Bayes rinden parecido; el árbol es bastante peor. Las curvas de lift muestran que tomando el top 20% de historias rankeadas por el modelo se obtiene lift ≈2.0 (el doble de precisión que en la población), es decir, la mitad de ese grupo son positivas. Entre los términos de alta information gain (de Macskassy et al., 2001) aparecen palabras sugestivas de buenas o malas noticias (*merg*, *gain*, *award*, *bond*, *outperform*) y vestigios del "Dotcom Boom" (*econtent*, *edesign*, *eoperate*).

El enfoque, aunque es de los más complejos del libro, sigue siendo simple: bag of words es primitivo para esta tarea; la extracción de entidades nombradas y, mejor aún, el *event parsing* darían más fuerza, ya que las noticias narran eventos y modificadores como *not*, *despite* o *expect* pueden no estar adyacentes a lo que modifican. También convendrían timestamps y precios más finos ("tick level") para poder operar.

## Ideas clave

- Los datos rara vez llegan como vectores de características; preparar la representación (representation engineering) es una etapa clave, y suele ser más simple adaptar los datos a las herramientas que al revés.
- El texto es abundante e importante en negocio, pero "no estructurado", sucio y muy dependiente del contexto, por lo que exige preprocesamiento dedicado.
- Bag of words trata cada palabra como una característica independiente, ignorando orden y gramática; es simple, barato y sorprendentemente eficaz.
- El preprocesamiento típico incluye normalización de mayúsculas, stemming y eliminación de stopwords (con cuidado: en títulos las stopwords pueden importar).
- TFIDF = TF × IDF pondera cada término por su frecuencia en el documento y por su rareza en el corpus; es la representación de valores más común para texto.
- La similitud entre documentos (p. ej. cosine similarity sobre vectores TFIDF) permite recuperación por vecino más cercano, como en el ejemplo de los músicos de jazz.
- Cuando bag of words no basta: n-gramas (preservan orden pero inflan características), extracción de entidades nombradas (intensiva en conocimiento) y topic models (capa latente de temas entre palabras y modelo).
- El caso de noticias financieras muestra que gran parte del trabajo es formulación del problema (qué predecir, qué umbral, qué radio causal) y que hay señal predictiva real aun con representaciones primitivas.
