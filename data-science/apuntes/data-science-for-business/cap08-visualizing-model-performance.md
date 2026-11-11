# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 8 — Visualizing Model Performance (Visualización del rendimiento de modelos)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber
El capítulo anterior desarrolló el marco de valor esperado (expected value) con cálculos que producen un único número de beneficio esperado para un conjunto de condiciones. Este capítulo da un giro: en lugar de confiar en cálculos aislados que dependen de supuestos muy estrictos (conocimiento preciso de costes, beneficios y probabilidades), propone visualizaciones que comunican mejor el rendimiento a los stakeholders y que exponen el comportamiento del modelo bajo incertidumbre.

La tesis central es que un clasificador que asigna scores puede usarse para rankear casos y actuar sobre los mejor clasificados, y que al barrer un umbral (threshold) a lo largo de ese ranking se genera una familia de matrices de confusión. Graficar las consecuencias de ese barrido produce curvas de rendimiento. Según qué supuestos sean estables (priors de clase, costes y beneficios), conviene una visualización u otra.

Sales sabiendo cuatro técnicas y cuándo usarlas: las profit curves (cuando priors, costes y beneficios se conocen y son estables), las ROC curves y su AUC (cuando esas condiciones son inciertas o cambian), y las cumulative response y lift curves (cuando los costes son inciertos pero la proporción de clases no cambia). El cierre es un caso de churn que compara varios modelos con todas estas herramientas.

## El ejemplo que recorre el capítulo
El hilo conductor final es el churn de telefonía móvil, usando el dataset anonimizado de la KDD Cup 2009 (datos de Orange, France Telecom). Son unas 47.000 instancias con un sesgo de clase del 7% de churn (positivos) frente al 93% de no churn (negativos). Se entrenan y comparan cuatro modelos tratados como "cajas negras": classification tree, logistic regression, k-Nearest Neighbor y Naive Bayes. El objetivo no es resolver bien el problema ni tunear modelos, sino usar el dominio como banco de pruebas para ilustrar las técnicas de evaluación.

## Rankear en lugar de clasificar
En vez de decidir cada caso por separado con su valor esperado, otra estrategia es rankear los casos por score y actuar sobre los `n` primeros (o los que superen un umbral). Esto es práctico por varias razones: el score puede ordenar bien sin ser una probabilidad verdadera (como la distancia a la frontera separadora); a veces no se pueden obtener probabilidades fiables (por ejemplo, sin una muestra de entrenamiento representativa en marketing dirigido); y es habitual tener un presupuesto fijo, por lo que basta con apuntar a los candidatos más prometedores.

Cuando los costes y beneficios son constantes por clase, rankear por verosimilitud de la clase objetivo es suficiente; el único cuidado es que el presupuesto no lleve a territorio de valor esperado negativo. En cambio, si cada caso tiene costes y beneficios distintos, el simple ranking por verosimilitud no basta.

Un clasificador con scores puede ser conservador (umbral alto: exige mucha certeza antes de actuar) o permisivo (umbral bajo). Aquí entra la extensión clave del marco: un clasificador de ranking más un umbral produce una única matriz de confusión; al cambiar el umbral, cambian los true positives y false positives y, por tanto, la matriz. Al bajar el umbral, las instancias suben de la fila N a la fila Y: si eran positivas se vuelven true positives (Y,p) y si eran negativas, false positives (Y,n). Cada umbral es, técnicamente, un clasificador distinto. Quedan dos preguntas: cómo comparar rankings y cómo elegir un umbral adecuado.

## Profit curves
Combinando el cálculo de beneficio esperado con el ranking, se barre el umbral por puntos sucesivos de la lista ordenada por score decreciente, registrando en cada corte el porcentaje de la lista predicho como positivo y el beneficio esperado correspondiente. Graficar esos valores da una profit curve.

El ejemplo usa un test de 1.000 consumidores con margen pequeño: cada oferta cuesta $5 y cada oferta aceptada genera $9, con beneficio neto de $4. La matriz de costes es:

```
      p      n
Y    $4    -$5
N    $0     $0
```

Todas las curvas empiezan y terminan en el mismo punto: a la izquierda no se apunta a nadie (cero gasto, cero beneficio) y a la derecha se apunta a todos (todos los clasificadores rinden igual). El clasificador aleatorio es el peor. El beneficio puede volverse negativo cuando el margen es fino y hay pocos respondedores, porque se "entra en números rojos" al bajar demasiado en la lista y ofertar a quienes no responderán.

Con recursos ilimitados y objetivo de maximizar beneficio, el Classifier 2 logra el máximo de $200 apuntando al 50% mejor rankeado. Pero con una restricción presupuestaria la cosa cambia: con 100.000 clientes y $40.000 de presupuesto, a $5 por oferta solo se pueden hacer 40.000/5 = 8.000 ofertas, es decir, el 8% de la base. Mirando las curvas en x=8%, el mejor es el Classifier 1. La lección: añadir un presupuesto cambia no solo el punto de operación (8% en vez de 50%) sino también qué clasificador conviene usar para rankear. El mismo razonamiento aplica a restricciones de personal (por ejemplo, una plantilla fija de analistas de fraude).

## ROC graphs y curvas
Las profit curves exigen conocer con certeza dos condiciones críticas: los class priors (la proporción de positivos y negativos, o base rate) y los costes y beneficios. Si ambos son conocidos y estables, las profit curves sirven. Pero en muchos dominios (detección de fraude, gestión de churn) esas condiciones son inciertas o inestables.

El gráfico ROC (Receiver Operating Characteristics) acomoda la incertidumbre mostrando todo el espacio de posibilidades de rendimiento. Es un plano 2D con la false positive rate en el eje x y la true positive rate en el eje y; representa el trade-off entre beneficios (true positives) y costes (false positives). De las cuatro cifras de la matriz de confusión solo se necesitan dos tasas (una de cada par), y por convención se usan tp rate (informalmente, hit rate: qué porcentaje de los positivos reales acierta) y fp rate (false alarm rate: qué porcentaje de los negativos reales clasifica mal).

Puntos clave del espacio ROC: (0,0) nunca clasifica positivo (sin false positives ni true positives); (1,1) siempre clasifica positivo; (0,1) es clasificación perfecta; la diagonal de (0,0) a (1,1) es adivinar al azar. Para separarse de la diagonal hacia el triángulo superior, el clasificador debe explotar información de los datos. Ningún clasificador debería caer en el triángulo inferior derecho (peor que el azar). Un punto es superior a otro si está al noroeste (mayor tp rate con fp rate no peor, o menor fp rate con tp rate no peor). Los clasificadores a la izquierda son "conservadores" (pocas falsas alarmas pero baja tp rate) y los de arriba a la derecha, "permisivos". En dominios con muchos negativos, la zona de la izquierda es la más interesante, porque incluso una tasa moderada de falsas alarmas puede ser inmanejable.

Un modelo de ranking produce una curva: imaginando las instancias ordenadas por score y variando el umbral de −∞ a +∞, se sube un paso al pasar un positivo (más true positives) y se avanza a la derecha al pasar un negativo (más false positives). Es realmente una función escalonada que con muchas instancias parece suave. La gran ventaja del ROC es que desacopla el rendimiento del clasificador de las condiciones de uso: es independiente de las proporciones de clase y de los costes y beneficios, así que las posiciones relativas de los clasificadores no cambian aunque sí la región de interés.

## El área bajo la curva ROC (AUC)
El AUC es el área bajo la curva expresada como fracción del cuadrado unidad; va de cero a uno. Aporta menos información que la curva entera, pero es útil cuando se necesita un solo número que resuma el rendimiento o cuando no se conocen las condiciones de operación. Técnicamente equivale a la medida Mann-Whitney-Wilcoxon y, con una transformación algebraica menor, al coeficiente de Gini; ambas equivalen a la probabilidad de que un positivo elegido al azar quede rankeado por delante de un negativo elegido al azar.

## Cumulative response y lift curves
Las ROC son potentes pero poco intuitivas para muchos stakeholders de negocio, y comunicar bien es parte esencial del trabajo. La cumulative response curve es una alternativa más intuitiva: grafica el hit rate (tp rate, eje y) frente al porcentaje de la población que se apunta (eje x). La diagonal x=y es el azar: si apuntas al 20% al azar, alcanzas el 20% de los positivos. Cualquier clasificador por encima de la diagonal aporta ventaja.

A estas curvas a veces se las llama lift curves porque se ve cuánto se "eleva" la línea del modelo sobre la diagonal del azar. El lift es la ventaja sobre adivinar al azar: en una lista de 100 clientes, mitad churn, si paras a la mitad (0,5 apuntado) con orden aleatorio ves la mitad de los positivos (lift 0,5/0,5 = 1); con un buen clasificador verías más de la mitad (lift > 1); con uno perfecto verías todos (1,0/0,5 = 2). La lift curve propiamente dicha grafica ese lift numérico (valor de la cumulative response dividido por la diagonal y=x) frente al porcentaje de población apuntado; la diagonal se convierte en una horizontal en y=1. Un "2X lift" significa que, en el umbral elegido, el modelo apunta el doble de bien que el azar.

Ambas curvas deben usarse con cuidado: a diferencia de las ROC, asumen que el test tiene exactamente los mismos priors que la población real. En publicidad online, donde el base rate puede ser 1:10⁷, se suele hacer down-sampling de los negativos; esto no afecta a las ROC (sus ejes son proporciones de una sola clase), pero sí distorsiona las relaciones de ejes en las lift y cumulative response curves.

## Ejemplo: analítica de rendimiento para modelos de churn
Con el dataset KDD Cup 2009, una evaluación ingenua (entrenar y testear sobre el mismo set, midiendo accuracy) da resultados engañosos: árbol 95%, logistic 93%, k-NN 100%, Naive Bayes 76%. Como el base rate es 93%, cualquier clasificador debería alcanzar ese mínimo, lo que hace sospechoso el 76% de Naive Bayes y, sobre todo, el 100% del k-NN (regla práctica: desconfiar de cualquier rendimiento perfecto en un problema real). Esos números reflejan memorización (overfitting) más que otra cosa.

Rehaciéndolo con ten-fold cross-validation se obtienen accuracy y AUC: Classification Tree 91,8% / AUC 0,614; Logistic Regression 93,0% / 0,574; k-NN 93,0% / 0,537; Naive Bayes 76,5% / 0,632. La desviación estándar pequeña actúa como "sanity check". El AUC va de 0 (0,5 = azar) a 1; la accuracy engaña con datasets sesgados. Las fitting curves del árbol confirman overfitting: el rendimiento en training sigue subiendo mientras el de holdout alcanza su "sweet spot" hacia los 100 nodos y luego cae.

Dos observaciones sobre el AUC: todos son modestos (normal en problemas reales con poca señal, y aun así pueden dar buen resultado de negocio) y, curiosamente, Naive Bayes tiene la accuracy más baja pero el AUC más alto. Comparando matrices de confusión se entiende: el k-NN casi nunca predice churn (actúa como clasificador de base rate, ~93% de accuracy), mientras Naive Bayes comete más errores pero identifica a muchos más churners. En las ROC, las curvas de NB y Tree están más "arqueadas", señal de su superioridad predictiva.

Las lift curves (sin comprometer costes) muestran que Tree y NB rinden bien: Tree es superior hasta ~25% de las instancias y a partir de ahí domina NB; k-NN y LR rinden mal. Nota sobre combinar clasificadores: no se puede tomar el top 25% de Tree y seguir con NB esperando lo óptimo, porque los órdenes son distintos; combinarlos bien requiere métodos principiados (ensembles, tratados en el capítulo sobre bias, variance y métodos de ensemble).

Las profit curves incorporan supuestos de costes. Escenario 1: coste $3 por oferta y beneficio bruto $30 (true positive neto $27, false positive −$3), ratio 9 a 1; Tree domina en los umbrales más altos y NB en el resto, con máximo hacia el 20% de la población. Escenario 2: mismo coste $3 pero beneficio bruto $39 (neto $36), ratio 12 a 1; beneficio máximo mayor y dos máximos (Tree ~20%, NB ~35%), ilustrando la sensibilidad de las profit curves a los supuestos de costes y beneficios. Se insiste en que es solo ilustrativo: no se afinaron los modelos ni cabe sacar conclusiones generales sobre su idoneidad para churn.

## Resumen del capítulo
Evaluar bien y comunicar los resultados a los stakeholders es parte crítica del trabajo del data scientist, y la visualización es clave. Aunque la muestra de entrenamiento se ajuste, la evaluación debe usar una muestra que refleje la población real. Si los costes y beneficios se pueden especificar, basta calcular el coste esperado por instancia y elegir el mejor modelo, y una profit curve ayuda a comparar con un "bottom line" comprensible; su desventaja es exigir condiciones de operación exactas. Cuando esas condiciones son imprecisas o cambian, conviene otra visualización: si los costes son inciertos pero la mezcla de clases no cambia, una cumulative response o lift curve; y las ROC curves, aunque cuestan de leer, separan el rendimiento de las condiciones de operación y muestran los trade-offs fundamentales de cada modelo.

## Ideas clave
- Rankear por score y actuar sobre los primeros `n` (o sobre un umbral) es una alternativa a decidir caso por caso; un clasificador de ranking + umbral = una matriz de confusión.
- Profit curves: útiles cuando priors, costes y beneficios se conocen y son estables; una restricción de presupuesto cambia el punto de operación y hasta el clasificador elegido.
- ROC graphs: fp rate (x) vs tp rate (y); desacoplan el rendimiento de priors y costes; mejor rendimiento hacia el noroeste, nunca por debajo de la diagonal del azar.
- AUC resume la curva ROC en un número (0 a 1; 0,5 = azar) y equivale a la probabilidad de rankear un positivo por delante de un negativo.
- Cumulative response y lift curves son más intuitivas para negocio, pero asumen que el test conserva los priors reales (sensibles al down-sampling).
- La accuracy engaña en datasets sesgados: en el churn, k-NN alcanzaba el 93% comportándose como clasificador de base rate, mientras Naive Bayes, con menor accuracy, tenía mayor AUC por detectar más churners.
- Validar con cross-validation y fitting curves evita confiar en resultados de entrenamiento inflados por overfitting.
- Combinar segmentos de distintos clasificadores no da lo óptimo; para eso existen los ensembles.
