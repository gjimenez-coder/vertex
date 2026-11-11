# Similarity, Neighbors, and Clusters (Similitud, vecinos y clústeres) — Estudio

## Tarjetas de repaso

P: ¿Qué idea central conecta la búsqueda de entidades parecidas, el modelado predictivo y el clustering?
R: La similitud, aproximada por la distancia en el espacio de características: cuanto más cerca están dos objetos representados como vectores, más similares son.

P: ¿Qué es la distancia Euclídea y de qué se deriva?
R: La medida básica de distancia, derivada del teorema de Pitágoras; generaliza a n dimensiones como la raíz de la suma de las diferencias al cuadrado por cada característica (norma L2, ‖·‖₂).

P: ¿Por qué la distancia Euclídea entre dos instancias (≈18,8 en el ejemplo de crédito) no tiene interpretación por sí misma?
R: No tiene unidades ni significado aislado; solo sirve para comparar la similitud de un par de instancias frente a otro par.

P: ¿Cómo predice un clasificador k-NN?
R: Recupera los k vecinos más similares a la instancia nueva y combina sus clases por voto mayoritario, prediciendo la clase dominante.

P: En k-NN, ¿por qué k es un parámetro de complejidad?
R: Con k=1 el modelo memoriza y sobreajusta (fronteras erráticas, islas en outliers); con k=n se predice siempre el promedio global (muy simple). Se elige por validación cruzada.

P: ¿Qué significa que k-NN sea "lazy learning"?
R: Que no construye un modelo explícito; aplaza casi todo el esfuerzo al momento de la consulta (también llamado instance-based o memory-based learning).

P: ¿Cómo funciona el voto ponderado por similitud y qué peso usa?
R: Cada vecino contribuye en proporción a su similitud, usando como peso el recíproco del cuadrado de la distancia: w(x,y) = 1/dist(x,y)²; reduce la importancia de elegir k con exactitud.

P: ¿Cuáles son las tres limitaciones principales de los métodos de vecinos?
R: Baja inteligibilidad del modelo global, la maldición de la dimensionalidad (atributos irrelevantes confunden la similitud) y el coste computacional en la predicción.

P: ¿Qué distancias alternativas a la Euclídea menciona el capítulo?
R: Manhattan (L1), Jaccard (conjuntos de características), coseno (ignora magnitud, para texto) y edición/Levenshtein (operaciones mínimas para transformar una cadena en otra).

P: ¿Qué calcula la distancia de Jaccard y cuándo es apropiada?
R: dJaccard(X,Y) = 1 − |X∩Y|/|X∪Y|; trata objetos como conjuntos y es apropiada cuando importa la presencia común de una característica pero no su ausencia común.

P: ¿Qué diferencia al clustering de la segmentación supervisada?
R: El clustering busca agrupaciones naturales sin variable objetivo prefijada (objetos similares dentro del grupo y distintos entre grupos); suele ser análisis exploratorio de datos.

P: ¿Qué es un dendrograma y qué ventaja aporta?
R: La representación del clustering jerárquico con la distancia entre clústeres en el eje y; cortándolo con una línea horizontal se obtiene cualquier número de clústeres, mostrando el "paisaje" de similitud antes de decidir cuántos extraer.

P: Describe el algoritmo k-means.
R: Fijado k: (1) crea k centros iniciales al azar; (2) asigna cada punto al centro más cercano; (3) recalcula cada centroide como la media de sus puntos; repite 2–3 hasta que no haya cambios.

P: ¿Por qué se ejecuta k-means muchas veces y cómo se compara?
R: Un solo run halla un óptimo local dependiente de los centros iniciales; se repite con centros aleatorios distintos y se elige el de menor distorsión (suma de diferencias al cuadrado entre cada punto y su centroide).

P: ¿Qué es una descripción diferencial de un clúster frente a una descripción característica?
R: La diferencial (vía un clasificador supervisado sobre la etiqueta de clúster) indica qué distingue a un clúster de los demás; la característica describe lo típico del grupo sin atender a lo que comparte con otros.

## Preguntas de autoevaluación

P: ¿Por qué el ejemplo de los whiskies codifica cada valor de atributo como una característica binaria independiente, y cuántas resultan?
R: Porque los valores de los cinco atributos (Color, Nose, Body, Palate, Finish) pueden coocurrir, así que cada valor se codifica aparte, resultando en 68 características binarias por whisky. (Sección "El ejemplo que recorre el capítulo")

P: ¿Cómo se usa k-NN para estimación de probabilidad y qué resultado da en el ejemplo de David?
R: En vez de una decisión Sí/No se asigna un score promediando los vecinos con Sí=1 y No=0; con los tres vecinos de David da 2/3, y en la práctica conviene usar más vecinos. (Sección "Razonamiento por vecinos más cercanos")

P: ¿Por qué no se usa la variable objetivo al recuperar los vecinos en una regresión?
R: Porque la variable objetivo es justo lo que queremos predecir; en el ejemplo se combinan los ingresos de los vecinos (50, 35, 40 mil) con media (≈42) o mediana (40). (Sección "Razonamiento por vecinos más cercanos")

P: ¿Por qué una justificación tipo "le negamos la hipoteca porque se parece a los Smith y los Mitchell" es problemática con k-NN?
R: Porque no hay un modelo explícito y esa explicación no es aceptable; algunas regulaciones de crédito exigen modelos con explicaciones simples por variable, por lo que si la inteligibilidad es crítica conviene evitar estos métodos. (Sección "Problemas de los métodos de vecinos")

P: En el ejemplo de clustering de noticias de Apple, ¿qué demuestra que algunos clústeres sean coherentes y otros no?
R: Que la similitud sintáctica (vectores TFIDF) no es similitud semántica; aun así el clustering revela estructura imprevista y sugiere oportunidades de minería. (Sección "Ejemplo: clustering de noticias de negocio")

P: ¿Qué compromiso existe entre resolver un problema de negocio supervisado y hacer clustering exploratorio?
R: En el supervisado el esfuerzo se concentra al inicio (definir el objetivo) y la evaluación es clara; en el clustering, con noción vaga del problema, el esfuerzo se desplaza a la fase de evaluación del proceso CRISP, donde cuesta entender qué revela y cómo usarlo. (Sección "Resolver un problema de negocio frente a explorar datos")

P: ¿Cómo cerró el ciclo el caso de Haimowitz y Schwartz con GE Capital?
R: Agruparon clientes en cinco perfiles crediticios, pero como esos datos no están disponibles al fijar la línea de crédito, usaron el conocimiento para definir un problema predictivo: estimar la probabilidad de que un cliente caiga en cada clúster con datos disponibles al aprobar el crédito. (Sección "Resolver un problema de negocio frente a explorar datos")

## Puntos a dominar

- Calcular la distancia Euclídea entre dos instancias representadas como vectores de características y entender que el valor solo sirve para comparar pares.
- Aplicar k-NN a clasificación (voto mayoritario), estimación de probabilidad (promedio con Sí=1/No=0) y regresión (media o mediana de los vecinos).
- Reconocer k como parámetro de complejidad y saber que se elige por validación cruzada; entender el efecto del voto ponderado por 1/dist².
- Identificar cuándo usar distancias alternativas (Manhattan, Jaccard, coseno, edición) según si lo significativo es la escala, la presencia de características, el texto o las cadenas.
- Escalar o binnear atributos numéricos de escalas dispares y codificar categóricos antes de medir distancias.
- Distinguir clustering jerárquico (dendrograma recortable, función de enlace) de k-means (centroides, fijar k, repetir runs, distorsión).
- Interpretar clústeres mediante miembros, ejemplares y centroides, y diferenciar descripción diferencial de descripción característica.
- Situar el esfuerzo del proceso CRISP: al inicio en problemas supervisados, en la evaluación cuando el clustering es exploratorio.
