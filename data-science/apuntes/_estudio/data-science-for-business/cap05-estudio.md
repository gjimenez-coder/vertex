# Overfitting and Its Avoidance (El sobreajuste y cómo evitarlo) — Estudio

## Tarjetas de repaso

P: ¿Qué es la generalización?
R: La propiedad de un modelo por la que se aplica a datos que no se usaron para construirlo; es decir, predecir bien sobre instancias no observadas de la población, no solo sobre el conjunto de entrenamiento.

P: ¿Qué es el sobreajuste (overfitting)?
R: La tendencia de los procedimientos de minería de datos a adaptar los modelos a los datos de entrenamiento a expensas de la generalización a datos nuevos.

P: ¿Qué ilustra el "modelo de tabla" de churn de MegaTelCo?
R: El sobreajuste llevado al límite: memoriza a los clientes que abandonaron (100% de acierto en históricos), pero es inútil en producción porque un cliente nuevo no está en la tabla y se le predice "0% de abandono".

P: ¿Qué son los datos de reserva (holdout data)?
R: Una parte de los datos con el valor del objetivo conocido que se aparta y no se usa para construir el modelo; sirven como "test de laboratorio" de la generalización. Suelen llamarse conjunto de prueba (test set).

P: ¿Qué muestra un fitting graph?
R: La precisión del modelo frente a su complejidad, con dos curvas: una sobre datos de entrenamiento y otra sobre datos de reserva. La brecha entre ambas señala sobreajuste.

P: ¿Qué es la tasa base (base rate) y el clasificador de tasa base?
R: La tasa de error de predecir siempre la clase mayoritaria; equivale al porcentaje de la clase minoritaria. En regresión, el modelo que siempre predice la media o la mediana del objetivo.

P: ¿Dónde reside la complejidad de un árbol y qué es el "sweet spot"?
R: En el número de nodos. El sweet spot es el punto (unos 100 nodos en el ejemplo) a partir del cual la precisión de reserva decae porque el árbol capta detalles no propios de la población; no es universal y se halla empíricamente.

P: ¿Cómo se añade complejidad a una función matemática?
R: Añadiendo más atributos (cada uno con su peso wi), incluso versiones no lineales de atributos existentes (p. ej. x4 = x1² o x5 = x2/x3), lo que permite ajustar conjuntos cada vez mayores de puntos arbitrarios.

P: ¿Qué es la validación cruzada (cross-validation)?
R: Dividir el conjunto etiquetado en k folds (típicamente 5 o 10); en cada iteración un fold distinto es prueba y los k–1 restantes entrenamiento. Aporta media y varianza del rendimiento y aprovecha mejor datos limitados.

P: ¿Qué es una learning curve y en qué se diferencia del fitting graph?
R: Representa el rendimiento de generalización frente a la cantidad de datos de entrenamiento (empinada al inicio, luego se aplana). El fitting graph muestra entrenamiento y generalización frente a la complejidad con datos fijos; la learning curve muestra solo generalización frente al tamaño de datos.

P: ¿Qué dos estrategias controlan la complejidad en árboles?
R: (i) Detener el crecimiento antes de que sea demasiado complejo (criterios de parada) y (ii) dejarlo crecer y luego podarlo (prune).

P: ¿Qué es la regularización y qué forma tiene su función objetivo?
R: Optimizar una combinación de ajuste y simpleza, añadiendo una penalización por complejidad ponderada por λ: arg max fit(w, D) − λ · penalty(w).

P: ¿Qué diferencia hay entre ridge regression y lasso?
R: Ridge usa penalización L2 (suma de cuadrados de los pesos); lasso usa L1 (suma de valores absolutos), que pone a cero muchos coeficientes y realiza selección automática de atributos.

P: ¿Qué es el nested holdout testing / nested cross-validation?
R: Dividir de nuevo el entrenamiento en subentrenamiento y validación para elegir la complejidad; con validación cruzada anidada se corre otra CV dentro de cada fold para fijar el parámetro C (con 5-fold en ambos niveles, 30 modelos).

P: ¿Por qué el sobreajuste es, en el fondo, un problema de comparaciones múltiples?
R: Si se prueban muchas alternativas y se eligen solo las que "se ven bien" (como quedarse con el mejor de 1.000 fondos elegidos al azar), la significancia es dudosa; incluso los procedimientos para evitar el sobreajuste realizan estas comparaciones.

## Preguntas de autoevaluación

P: ¿Por qué evaluar un modelo sobre los mismos datos con que se construyó no mide la generalización?
R: Porque mide precisión "in-sample"; un modelo puede memorizar el entrenamiento (como el modelo de tabla) y acertar el 100% ahí sin predecir bien sobre datos nuevos. Hay que usar datos de reserva. (Sección: Examen del sobreajuste: datos de reserva y fitting graphs)

P: En el ejemplo del iris, ¿por qué la SVM mueve menos su frontera que la regresión logística al añadir un punto atípico?
R: Porque la SVM incorpora control de complejidad y es menos sensible a ejemplos individuales, mientras que la regresión logística mueve mucho su frontera para separar perfectamente. (Sección: Sobreajuste en árboles y en funciones matemáticas)

P: ¿Por qué una rama espuria en un árbol puede ser perjudicial aunque mejore la precisión en entrenamiento?
R: Porque recoge una idiosincrasia de la muestra (p. ej. dividir por y, que no tiene poder predictivo real): clasifica mejor el entrenamiento (7 de 8 frente a 6 de 8) pero eleva el error esperado en la población del 25% al 30%. (Sección: Por qué el sobreajuste es perjudicial)

P: ¿Qué ventaja da la validación cruzada frente a un único conjunto de reserva?
R: Un único holdout da una sola estimación que puede ser una elección afortunada o no; la validación cruzada aporta media y varianza del rendimiento (confianza en la estimación) y aprovecha mejor un dataset limitado. (Sección: De la evaluación con reserva a la validación cruzada)

P: ¿Cómo orienta una learning curve la decisión de invertir en más datos o en mejores features?
R: Si la curva ya se ha aplanado, más datos no compensan y conviene mejorar las features; si sigue subiendo, obtener más datos puede ser buena inversión. (Sección: Learning curves)

P: ¿Qué criterio de parada estadístico se usa para limitar el crecimiento de un árbol y con qué umbral habitual?
R: Un test de hipótesis en cada hoja basado en un p-valor (umbral habitual del 5%) para decidir si la ganancia de información observada no se debe al azar. (Sección: Evitar el sobreajuste y controlar la complejidad)

P: En el dataset de churn con validación cruzada de diez folds, ¿qué resultados obtuvieron los árboles y la regresión logística, y cuál se prefirió?
R: Los árboles bajaron del 73% previo a 68,6% de media (había sobreajuste), con desviación 1,1; la regresión logística dio 64,1% de media con desviación 1,3. Se prefirieron los árboles por su mayor estabilidad y rendimiento, aunque no es absoluto. (Sección: De la evaluación con reserva a la validación cruzada)

P: ¿Qué relación tiene la SVM lineal con la regresión logística regularizada?
R: Es casi equivalente a una regresión logística regularizada con L2, salvo que usa hinge loss en vez de verosimilitud. (Sección: Evitar el sobreajuste y controlar la complejidad)

## Puntos a dominar

- Explicar el compromiso fundamental entre complejidad del modelo y posibilidad de sobreajuste, y que todos los tipos de modelo pueden sobreajustar.
- Distinguir generalización de sobreajuste y reconocer el modelo de tabla como memorización pura.
- Usar datos de reserva (holdout) para estimar la generalización y leer un fitting graph (brecha entre curvas, sweet spot, forma de U o U invertida).
- Identificar la tasa base y el clasificador de tasa base en clasificación y su equivalente en regresión.
- Interpretar una learning curve y diferenciarla del fitting graph.
- Aplicar validación cruzada de k folds e interpretar media y varianza del rendimiento.
- Controlar la complejidad en árboles con criterios de parada (mínimo de instancias por hoja, test de hipótesis con p-valor) y poda.
- Aplicar regularización (L2/ridge, L1/lasso) y elegir λ, el tamaño del árbol o el conjunto de features con nested cross-validation (grid search, SFS/eliminación hacia atrás).
- Reconocer el sobreajuste como un problema de comparaciones múltiples y mitigarlo con procedimientos de reserva e inspección cuidadosa de los resultados.
