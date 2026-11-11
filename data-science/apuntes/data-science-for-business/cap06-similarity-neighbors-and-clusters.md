# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 6 — Similarity, Neighbors, and Clusters (Similitud, vecinos y clústeres)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

La similitud es un concepto que atraviesa gran parte de la ciencia de datos: si dos cosas (personas, empresas, productos) se parecen en algunos aspectos, suelen compartir otras características. El capítulo aborda la similitud de forma directa y muestra cómo se aplica a tareas muy distintas: recuperar entidades parecidas, clasificar y hacer regresión, y agrupar objetos en clústeres. Varias tareas de negocio razonan a partir de ejemplos similares: IBM busca empresas parecidas a sus mejores clientes para orientar a su fuerza de ventas, los anunciantes buscan consumidores similares a sus buenos clientes, y los minoristas como Amazon y Netflix usan similitud para recomendar.

La tesis central es que, una vez que un objeto se representa como un vector de características, podemos medir la distancia entre objetos: cuanto más cerca estén en el espacio definido por las características, más similares son. A partir de esa idea de distancia se construyen los métodos de vecinos más cercanos (nearest neighbors) para predicción y los métodos de clustering para segmentación no supervisada.

Al terminar el capítulo sabrás calcular distancias (Euclídea y alternativas), usar k-NN para clasificación, regresión y estimación de probabilidad, entender k como parámetro de complejidad y controlar el overfitting, y aplicar clustering jerárquico y k-means. También distinguirás entre resolver un problema de negocio bien definido (supervisado) y la exploración de datos (no supervisado), donde el esfuerzo se desplaza hacia la fase de evaluación del proceso CRISP.

## El ejemplo que recorre el capítulo

El hilo conductor es *Whiskey Analytics*: Foster quiere encontrar single malts similares a uno que le gustó (Bunnahabhain). Siguiendo a Lapointe y Legendre (1994), los whiskies se describen con cinco atributos generales (Color, Nose, Body, Palate, Finish), cada uno con muchos valores posibles. Como los valores pueden coocurrir, cada valor se codifica como una característica binaria independiente, resultando en 68 características binarias por whisky. Con la distancia Euclídea se recuperan los cinco más parecidos a Bunnahabhain (Glenglassaugh, Tullibardine, Ardberg, Bruichladdich, Glenmorangie), ordenados por distancia creciente. El mismo ejemplo reaparece en clustering, donde un dueño de tienda podría elegir un whisky de cada grupo de sabor para tener una colección amplia y ecléctica.

## Similitud y distancia

Una vez representado un objeto como vector de características, cuanto más cerca están dos objetos en ese espacio, más similares son. Modelos vistos antes (árboles de clasificación, clasificadores lineales) ya usan similitud implícita: establecen fronteras entre regiones, bajo la idea de que instancias en una misma región deben ser parecidas; lo que cambia entre métodos es cómo se representan y descubren esas regiones.

La medida básica es la distancia Euclídea, derivada del teorema de Pitágoras. Para dos puntos en 2D la distancia es la hipotenuse del triángulo cuyos catetos son las diferencias en cada eje. Se generaliza a *n* dimensiones (Ecuación 6-1):

```
d(A,B) = sqrt( (d1,A - d1,B)^2 + (d2,A - d2,B)^2 + ... + (dn,A - dn,B)^2 )
```

Para las personas A y B del ejemplo de crédito (edad, años en el domicilio, estatus residencial), la distancia Euclídea es ≈ 18,8. Ese número no tiene unidades ni interpretación por sí mismo: solo sirve para comparar la similitud de un par de instancias frente a otro par.

## Razonamiento por vecinos más cercanos (nearest-neighbor)

Con una medida de distancia podemos encontrar los ejemplos más similares (los *nearest neighbors*) y actuar según el contexto de negocio: IBM orienta su fuerza de ventas, los anunciantes online eligen a quién mostrar anuncios. El ejemplo del whisky es una aplicación directa de la similitud; el trabajo del científico de datos está en definir los datos para que la similitud se calcule sobre características útiles.

Para modelado predictivo, el procedimiento es simple: dada una instancia nueva, se recuperan los ejemplos de entrenamiento más similares y se predice el valor objetivo combinando los valores conocidos de esos vecinos mediante una función de combinación (voto, promedio).

- **Clasificación**: se recuperan los k vecinos (p. ej. 3) y se consulta su clase; con voto mayoritario se predice la clase dominante. En el ejemplo de la oferta de tarjeta de crédito, los tres vecinos más cercanos a David (Rachael, John, Norah) tienen clases No, Sí, Sí, así que por voto mayoritario se predice Sí.
- **Estimación de probabilidad**: en vez de una decisión Sí/No se asigna un score. Con Sí=1 y No=0, el promedio de los tres vecinos de David da 2/3. En la práctica conviene usar más vecinos para estimar probabilidades.
- **Regresión**: se combinan los valores numéricos de los vecinos. Para predecir el ingreso de David a partir de los ingresos de sus tres vecinos (50, 35, 40 mil) se usa la media (≈42) o la mediana (40). Importante: en la recuperación de vecinos no se usa la variable objetivo, porque es justo lo que queremos predecir.

### Cuántos vecinos y cuánta influencia

No hay respuesta simple a cuántos vecinos usar. Los números impares ayudan a romper empates en el voto mayoritario de dos clases. Los algoritmos se abrevian como k-NN (p. ej. 3-NN). Cuanto mayor es k, más se suavizan las estimaciones entre vecinos; si k = n (todo el conjunto), se predice siempre el promedio global: la clase mayoritaria en clasificación, la media en regresión, la tasa base (base rate) en probabilidad.

Como no todos los vecinos están igual de cerca, los métodos suelen usar voto ponderado o moderado por similitud: cada vecino contribuye en proporción a su similitud, usando como peso el recíproco del cuadrado de la distancia. Al reponderar a los cinco clientes de David, Rachael, John y Norah dominan la predicción (0,65 Sí frente a 0,35 No) mientras Jefferson y Ruth, lejanos, apenas contribuyen. El scoring ponderado reduce la importancia de elegir k con exactitud, porque la influencia cae con la distancia.

### Muchos nombres y geometría

El razonamiento por vecinos recibe varios nombres por desarrollos independientes: *instance-based learning*, *memory-based learning* y, por aplazar casi todo el esfuerzo al momento de la consulta sin construir modelo, *lazy learning*. Relacionado está el Case-Based Reasoning (CBR) de la IA, usado por médicos y abogados; a diferencia de k-NN, los casos del CBR no son simples vectores sino resúmenes detallados de un episodio (síntomas, historia, diagnóstico, tratamiento, resultado) que requieren adaptación compleja al nuevo caso.

Geométricamente, k-NN crea regiones implícitas por vecindad, sin fronteras explícitas. Un clasificador 1-NN produce fronteras erráticas que siguen los límites entre instancias de clases distintas, e incluso crea "islas" alrededor de outliers. El 1-NN memoriza los datos de entrenamiento (clasifica perfecto en entrenamiento, pues cada punto es su propio vecino) y por tanto sobreajusta fuertemente. Así, **k es un parámetro de complejidad**: k=1 da un modelo muy complejo; k=n, muy simple (predice el promedio). Se elige k mediante validación cruzada u otro holdout anidado sobre el entrenamiento, y las herramientas suelen automatizarlo. Con 30-NN las fronteras son mucho menos dentadas que con 1-NN, aunque nunca son curvas suaves como en modelos lineales o árboles.

### Problemas de los métodos de vecinos

- **Inteligibilidad**: es fácil justificar una decisión concreta mostrando los vecinos que participan y sus contribuciones (Netflix y Amazon lo hacen: "La película X se recomendó por tu interés en…"). Pero una justificación tipo "le negamos la hipoteca porque se parece a los Smith y los Mitchell, que incumplieron" no es aceptable, y algunas regulaciones de crédito exigen modelos con explicaciones simples por variable. Explicar qué "conocimiento" se extrajo de los datos es difícil, porque no hay modelo explícito: el "modelo" es el conjunto de casos, la función de distancia y la función de combinación. Si la inteligibilidad es crítica, conviene evitar estos métodos.
- **Dimensionalidad y conocimiento del dominio**: como todos los atributos entran en la distancia, muchos atributos irrelevantes confunden la similitud —la *maldición de la dimensionalidad* (curse of dimensionality)—. Se mitiga con selección de características (manual, inyectando conocimiento del dominio, o automática) y ajustando la función de distancia con pesos por atributo (p. ej. dar más peso a "Número de tarjetas" o a "peatiness" en whiskies).
- **Eficiencia computacional**: el entrenamiento es rápido (solo se almacenan instancias), pero la predicción es costosa porque hay que consultar la base para hallar vecinos. En usos que exigen respuestas en decenas de milisegundos (publicidad online) puede ser impráctico. Existen estructuras como kd-trees y métodos de hashing para acelerar, aunque muchas herramientas pequeñas usan búsqueda por fuerza bruta.

## Detalles técnicos: atributos heterogéneos y otras distancias

Con atributos numéricos directamente comparables, la distancia Euclídea es sencilla. Con atributos heterogéneos surgen complicaciones: los categóricos (p. ej. Sexo) deben codificarse numéricamente (binario M=0, F=1 basta para dos valores, no para más); y variables numéricas con escalas muy distintas (Edad 18–100 frente a Ingreso 10–10.000.000) deben escalarse, o diez dólares pesarían igual que diez años. Por eso los sistemas de vecinos suelen escalar las variables o repartirlas en bins. El principio: la medida de similitud debe ser significativa para la aplicación.

La Euclídea es la más usada (norma L2, ‖·‖₂), general, intuitiva y rápida, pero hay muchas otras. El *Dictionary of Distances* lista cientos; una docena se usa con frecuencia:

- **Distancia Manhattan** (norma L1): suma de las diferencias absolutas por dimensión, sin elevar al cuadrado. Es la distancia "taxi" en una cuadrícula.
- **Distancia de Jaccard**: trata los objetos como conjuntos de características; es la proporción de características (que posee alguno) no compartidas: `dJaccard(X,Y) = 1 - |X∩Y|/|X∪Y|`. Apropiada cuando importa la presencia común de una característica pero no la ausencia común (p. ej. dos whiskies peaty sí importa; que ambos no sean salados, no). La usaron Lapointe y Legendre en el ejemplo del whisky.
- **Distancia del coseno**: mide la similitud de dos documentos; ignora la magnitud (escala) de los vectores. Útil en clasificación de texto donde cada palabra es una dimensión y el valor es el número de ocurrencias. Para A=<7,3,2> y B=<2,3,0> la distancia del coseno ≈ 0,19; y entre A y C=<70,30,20> es cero porque C es A por 10. La literatura de recuperación de información habla de *cosine similarity* (= 1 − distancia del coseno).
- **Distancia de edición (Levenshtein)**: cuenta el número mínimo de operaciones (insertar, borrar, reemplazar un carácter) para convertir una cadena en otra. Entre "1113 Bleaker St." y "113 Bleecker St." la distancia de edición es tres. Común para decidir si dos registros corresponden a la misma persona (con erratas) y en biología, donde el orden de las secuencias importa.

## Funciones de combinación

Son las fórmulas para calcular la predicción a partir de los vecinos. El voto mayoritario (Ecuaciones 6-6 y 6-7) elige la clase que maximiza el conteo de vecinos de esa clase. El voto moderado por similitud (Ecuación 6-8) añade un peso w basado en la similitud, típicamente `w(x,y) = 1/dist(x,y)²`. Escalando el score por la suma de pesos se obtiene una estimación de probabilidad entre 0 y 1 (Ecuación 6-9), y sustituyendo la parte de clase por valores numéricos se generaliza a regresión como promedio ponderado por distancia de los valores objetivo de los vecinos (Ecuación 6-10).

## Clustering (segmentación no supervisada)

Mientras la segmentación supervisada busca grupos que difieren respecto a una variable objetivo, el clustering busca agrupaciones naturales sin objetivo prefijado: objetos dentro de un grupo similares entre sí y distintos de los de otros grupos. Es útil para entender mejor el negocio (¿nuestros clientes forman grupos naturales?) y suele ser análisis exploratorio de datos. En el whisky, agrupar por sabor permitiría a una tienda elegir de cada grupo un miembro popular y otro menos conocido, o uno caro y uno económico.

### Clustering jerárquico

Agrupa los puntos por similitud creando una jerarquía anidada de agrupaciones: el único solapamiento entre clústeres es cuando uno contiene a otro. Se representa con un **dendrograma**, cuyo eje y es la distancia entre clústeres. "Cortando" el dendrograma con una línea horizontal se obtiene cualquier número de clústeres deseado; esa es su ventaja: ver el "paisaje" de similitud antes de decidir cuántos clústeres extraer. Una vez unidos dos clústeres, permanecen unidos en los niveles superiores.

Se forma empezando con cada instancia como su propio clúster y fusionando iterativamente hasta quedar uno solo, según una **función de enlace** (linkage) que define la distancia entre clústeres (p. ej. la distancia Euclídea entre los puntos más cercanos de cada clúster). En el dendrograma, un salto grande de distancia entre niveles sugiere una buena división, y un punto que se une muy arriba (como Aultmore en los whiskies, o F en el ejemplo de seis puntos) indica un posible outlier. Un uso célebre es el "Árbol de la Vida", una clasificación jerárquica de secuencias de ARN. El clustering de whiskies por sabor no coincide exactamente con las regiones de Escocia, aunque hay correlación.

### Clustering en torno a centroides: k-means

En lugar de enfocarse en las instancias, k-means se centra en los clústeres representados por su **centroide**: la media de los valores de cada característica de las instancias del clúster (no necesariamente una instancia real). El analista fija k (número de clústeres). El algoritmo: (1) crea k centros iniciales, normalmente al azar; (2) asigna cada punto al centro más cercano; (3) recalcula cada centroide como la media de sus puntos; y repite 2–3 hasta que no haya cambios. Por eso también se llama nearest-neighbor clustering.

Un solo run encuentra un óptimo local dependiente de los centros iniciales, así que k-means se ejecuta muchas veces con centros aleatorios distintos; se compara por la **distorsión** (suma de diferencias al cuadrado entre cada punto y su centroide) y se elige la de menor distorsión. Es eficiente (solo calcula distancias punto-centro en cada iteración), más rápido que el jerárquico, que necesita distancias entre todos los pares. Para elegir k se experimenta y se examinan los clústeres, o se grafican métricas (índices) de calidad al aumentar k y se toma el k donde empiezan a estabilizarse.

### Ejemplo: clustering de noticias de negocio

Para identificar agrupaciones de noticias sobre una empresa, se usó el corpus Reuters TRC2 (1.800.370 noticias) y se extrajeron las 312 historias cuyo titular mencionaba a Apple (AAPL). Tras preprocesamiento de texto (quitar HTML/URLs, normalizar mayúsculas, eliminar palabras muy raras o muy comunes), cada documento se representó con un vector de puntuaciones **TFIDF** (frecuencia del término penalizada por su frecuencia en el corpus). Con k=9 se obtuvieron grupos como: cambios de rating y precio objetivo de analistas; movimientos de la acción; la salud de Steve Jobs; anuncios de Apple; acuerdos del iPhone en otros países; cotizaciones *Before/After the Bell*; iTunes y música digital; y *News Briefs* (agrupados por su forma muy similar). Algunos clústeres son temáticamente coherentes y otros no: *la similitud sintáctica no es similitud semántica*. Aun así, el clustering revela estructura imprevista y sugiere oportunidades de minería.

### Entender los resultados del clustering

El resultado es un dendrograma o un conjunto de centroides con sus puntos. Formas de interpretarlo: listar los miembros del clúster (útil solo si los nombres son significativos, como los whiskies o empresas conocidas, no los nombres de clientes minoristas); mostrar un **ejemplar** del clúster (el "mejor de su clase", el más conocido o el de más ventas; para noticias, los titulares); y mostrar las **características promedio**, es decir, el centroide.

### Describir clústeres con aprendizaje supervisado (avanzado)

Se pueden generar descripciones automáticas mezclando no supervisado (el clustering) con supervisado. La estrategia: usar la asignación de clúster como etiqueta de clase, entrenar un clasificador inteligible (p. ej. un árbol con reglas) y leer su descripción. El resultado es una **descripción diferencial**: qué distingue a un clúster de los demás. Para el clúster J de whiskies (68 características binarias), un árbol de decisión produjo reglas como "cuerpo redondo y nariz a jerez ⇒ J". Esto contrasta con la **descripción característica** de Lapointe y Legendre, que describe lo típico del grupo sin atender a lo que comparte con otros. Las características se centran en comunalidades intergrupo; las diferenciales, en diferencias intragrupo. Ninguna es mejor: depende del uso.

## Resolver un problema de negocio frente a explorar datos

Los ejemplos de modelado predictivo y de similitud directa resuelven un problema de negocio muy concreto: definimos con precisión la variable objetivo o qué significa "similar", gastando esfuerzo en la fase de entendimiento del negocio/datos del proceso CRISP; así la evaluación es clara (¿resuelve el problema definido?). El clustering, en cambio, suele ser exploratorio, con una noción vaga del problema. El compromiso: lo que no se precisó al inicio hay que trabajarlo después, en la fase de **evaluación**, donde a menudo es difícil entender qué revela el clustering y cómo usarlo para mejores decisiones; se requiere creatividad y conocimiento del negocio. Haimowitz y Schwartz (1997) agruparon clientes de GE Capital en cinco perfiles de comportamiento crediticio, pero como esos datos no están disponibles al fijar la línea de crédito inicial, usaron ese conocimiento para definir un problema predictivo —predecir la probabilidad de que un cliente caiga en cada clúster con datos disponibles al aprobar el crédito— cerrando el ciclo del proceso.

## Ideas clave

- La similitud, aproximada por la distancia en el espacio de características, subyace a buscar entidades parecidas, al modelado predictivo y al clustering.
- La distancia Euclídea (norma L2) es la más común; existen alternativas (Manhattan/L1, Jaccard, coseno, edición/Levenshtein) y la elección debe ser significativa para el problema.
- Los métodos de vecinos (k-NN) son *lazy learning*: no construyen modelo; predicen clasificación, regresión o probabilidad combinando los vecinos, con voto o ponderación por similitud (recíproco del cuadrado de la distancia).
- En k-NN, k es un parámetro de complejidad: k=1 sobreajusta, k=n suaviza al máximo; se elige por validación cruzada.
- Limitaciones de k-NN: baja inteligibilidad del modelo global, maldición de la dimensionalidad (mitigada con selección de características y pesos), y coste en la predicción.
- El clustering jerárquico produce un dendrograma recortable para elegir el número de clústeres; k-means usa centroides, requiere fijar k, se repite por caer en óptimos locales y se evalúa con la distorsión.
- Entender clústeres: miembros, ejemplares y centroides; las descripciones supervisadas dan diferencias entre clústeres (diferenciales) frente a lo típico (características).
- En problemas supervisados el esfuerzo está al inicio (definir el objetivo); en el clustering exploratorio se desplaza a la evaluación e iteración del proceso CRISP.
