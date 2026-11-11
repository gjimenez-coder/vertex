# Machine Learning Classification (Clasificación con aprendizaje automático) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son las dos etapas de un clasificador?
R: Se entrena con datos etiquetados para aprender un patrón y luego actúa como función que recibe puntos nuevos y predice su clasificación (etiqueta o número continuo como puntuación de confianza).

P: ¿Cuáles son los dos usos principales de un clasificador según Cady?
R: Clasificar cosas en producción (de forma autónoma o marcando casos para revisión humana) y obtener insights sobre los datos subyacentes; este segundo ha sido el más común en su carrera.

P: ¿Qué dilema crea el uso de clasificadores para extraer insights?
R: A veces los clasificadores más precisos son los más difíciles de interpretar, y al negocio le interesan los patrones que explican el fenómeno, no solo la predicción.

P: ¿Cómo se maneja un problema multiclase con k etiquetas usando un clasificador binario?
R: Se entrenan k clasificadores, uno por etiqueta (X o no-X); el capítulo asume que todos los clasificadores son binarios.

P: ¿Por qué los árboles de decisión son propensos al overfitting?
R: Si la profundidad es excesiva, cada hoja contiene pocos puntos y da puntuaciones muy seguras que son accidentes de números pequeños; hay que ajustarlos porque los valores por defecto suelen sobreajustar.

P: ¿Por qué un random forest es preciso y robusto?
R: Es un conjunto de árboles entrenados sobre subconjuntos aleatorios de filas y características; sus sobreajustes individuales, aleatorios y distintos, tienden a cancelarse (ley de los grandes números), y se promedian sus puntuaciones.

P: ¿Qué es la feature importance en un random forest?
R: Lo único extraíble para interpretación: se baraja aleatoriamente la k-ésima característica entre puntos y se mide cuánto empeora el rendimiento.

P: ¿Qué asume una SVM y qué maximiza al entrenar?
R: Asume separabilidad lineal; busca el hiperplano que separa las clases maximizando el margin (distancia mínima a los puntos de cada clase). Clasifica según el signo de f(x) = w·x + b.

P: ¿Qué es el kernel trick?
R: Mapear los puntos a otro espacio donde la frontera sea lineal sin calcular el mapeo ϕ directamente, usando solo la función kernel k(x,y) = ϕ(x)·ϕ(y), normalmente simple y no lineal.

P: ¿Qué equilibrio ofrece la regresión logística y cómo puntúa?
R: Buen equilibrio entre precisión e interpretabilidad; puntúa con probabilidades según la distancia al hiperplano mediante la sigmoide σ(z) = 1/(1 + exp[−z]), con σ(0)=0.5.

P: ¿Qué aporta lasso regression frente a la logística?
R: Penaliza los pesos modestos y tiende a llevar la mayoría a 0, dejando solo las pocas características más significativas; mejora interpretación y reduce una forma solapada de overfitting.

P: ¿Cuál es el gran defecto de naive Bayes y por qué aun así funciona?
R: Trata cada característica como independiente de las demás (una variable duplicada se cuenta dos veces); aun así suele ser potente porque la sobreconfianza rara vez cambia la clasificación correcta.

P: ¿Qué relación tiene una red neuronal con la regresión logística?
R: Cada neurona calcula su salida con una activation function (típicamente sigmoide sobre una combinación ponderada), por lo que es una pequeña regresión logística; una red sin capas ocultas es un conjunto de regresores logísticos.

P: ¿Qué significan TPR y FPR?
R: TPR (true positive rate): de todo lo que debía marcarse, la fracción que se marca (ideal 1.0). FPR (false positive rate): de todo lo que NO debía marcarse, la fracción que se marca igualmente (ideal 0.0).

P: ¿Qué significa el AUC y por qué es útil?
R: Resume la curva ROC en un número; cercano a 1.0 es bueno y a 0.5 es pobre. No depende del corte elegido y equivale a la probabilidad de que un hit aleatorio tenga mayor predicción que un no-hit aleatorio.

## Preguntas de autoevaluación

P1: ¿Por qué dice Cady que entrenar un clasificador "no es ciencia de cohetes" y dónde está el trabajo real?
R: Porque el clasificador no es una caja negra mágica; el trabajo está en preparar los datos, apuntar el clasificador a la pregunta correcta, extraer características con señal y dar sentido a los resultados. (Lo que necesitas saber; 8.1–8.3)

P2: ¿Qué problemas plantea obtener datos etiquetados en detección de fraude?
R: Sueles tener pocos casos etiquetados a mano y una enorme masa sin etiquetar que presumes no fraudulenta, así que una fracción desconocida del entrenamiento está mal etiquetada; además definir qué es "fraude" (el ground truth) es un problema en sí mismo. (8.2)

P3: ¿Qué truco usó Cady con el cliente que estudiaba la "lealtad" y qué resultado tuvo?
R: Definió criterios de "claramente leal" y "claramente no leal" y descartó la zona gris (un tercio de los clientes); el clasificador funcionó sorprendentemente bien. (8.2)

P4: ¿Por qué prefiere Cady un random forest pero advierte de su limitación?
R: Es consistentemente de los más precisos y robustos, pero es imposible de interpretar en términos de negocio; su potencia es justamente ser demasiado complejo, y solo puede extraerse la feature importance. (8.5)

P5: ¿Qué problemas atribuye Cady a las SVM?
R: Si hay tantas características como puntos siempre existe un hiperplano separador y el sobreajuste es casi seguro; son fundamentalmente binarias sin puntuaciones continuas de confianza; y la separabilidad lineal falla (p. ej. una clase cerca del origen y otra lejos), lo que obliga a usar kernels. (8.5)

P6: En el ejemplo del dataset iris, ¿qué clasificador obtuvo el mejor AUC y cuáles fueron los valores?
R: La regresión logística con 0.989, seguida de random forest 0.901, naive Bayes 0.897 y árbol de decisión 0.830. (8.4, PDF p. 109)

P7: ¿Cómo se lee una curva ROC y qué indica la "rodilla"?
R: Se grafica FPR en el eje x y TPR en el eje y; la esquina superior izquierda (0.0, 1.0) es el clasificador perfecto y por debajo de y = x es peor que inútil. Un buen clasificador sube abruptamente, y la "rodilla" apuntando a la esquina superior izquierda es la firma de un clasificador fuerte. (8.6.2)

P8: ¿Qué es el F1 score y por qué no se usa la media aritmética?
R: Es la media armónica de precision y recall (1.0 perfecto, 0.0 el peor); la aritmética sería mala porque marcarlo todo o nada daría una puntuación mejor que 0. (8.7.1)

## Puntos a dominar

- Explicar las dos etapas de un clasificador y sus dos usos (producción vs. insights), reconociendo el dilema precisión/interpretabilidad.
- Identificar los problemas de datos: etiquetas insuficientes o erróneas, definición del ground truth y extracción de características con señal.
- Saber convertir un problema multiclase en k clasificadores binarios.
- Describir la idea de fondo, fortalezas y debilidades de cada algoritmo: árboles de decisión, random forests/ensembles, SVM (y kernel trick), regresión logística, lasso, naive Bayes y redes neuronales.
- Distinguir cuándo prima la interpretabilidad (logística, árbol) y cuándo la precisión (random forest).
- Calcular e interpretar TPR, FPR, precision y recall a partir de una matriz de confusión 2×2.
- Leer curvas ROC, interpretar el AUC y elegir un umbral cerca de la "rodilla" (corte con y = 1−x o punto de pendiente paralela a y = x).
- Usar F1 score y curvas lift–reach como métricas resumen equivalentes a la ROC.
