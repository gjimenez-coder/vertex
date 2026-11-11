# Decision Analytic Thinking I: What Is a Good Model? — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre qué es un buen modelo?
R: No existe una métrica universalmente correcta; siempre hay que volver a la pregunta de negocio: ¿qué queremos lograr minando los datos?

P: ¿Cómo se define la exactitud (accuracy)?
R: Es la proporción de decisiones correctas: `accuracy = decisiones correctas / total de decisiones`, equivalente a `1 − tasa de error`.

P: ¿Por qué la exactitud es una métrica simplista?
R: Porque falla con clases desbalanceadas y porque trata todos los errores como igualmente importantes.

P: ¿Qué es la matriz de confusión?
R: Una tabla de contingencia n × n (columnas = clase real, filas = clase predicha) que descompone aciertos y errores; la diagonal son los aciertos.

P: En clasificación binaria, ¿qué son los falsos positivos y los falsos negativos?
R: Falso positivo = negativo clasificado como positivo; falso negativo = positivo clasificado como negativo.

P: Por convención, ¿qué representa la clase "positiva"?
R: El caso digno de atención o alarma (fraude, enfermedad), que suele ser el raro; el negativo es benigno pero más frecuente.

P: ¿Por qué se rompe la evaluación por exactitud con clases raras?
R: Porque elegir siempre la clase mayoritaria da una exactitud muy alta (p. ej., 99,9% en proporción 999:1) sin aportar nada.

P: ¿Qué es el marco del valor esperado?
R: Una herramienta que enumera los posibles resultados y promedia sus valores ponderados por su probabilidad: `EV = p(o1)·v(o1) + p(o2)·v(o2) + ...`.

P: En el valor esperado, ¿de dónde salen las probabilidades y de dónde los valores?
R: Las probabilidades suelen estimarse de los datos; los valores de negocio (costes y beneficios) suelen venir de fuera (conocimiento del negocio).

P: ¿Cuál es la regla de decisión para contactar en el ejemplo de marketing dirigido?
R: Contactar solo si el valor esperado supera cero, lo que se reduce a `p_R(x) > 0,01`: basta un 1% de probabilidad de respuesta.

P: ¿Para qué sirve factorizar los priors de clase en el beneficio esperado?
R: Separa el desbalanceo de clases del poder predictivo real del modelo y permite comparar modelos evaluados con distribuciones distintas.

P: ¿Cuáles son las dos trampas al formular la matriz de costes-beneficios?
R: (1) Mantener consistentes los signos (beneficios positivos, costes negativos); (2) no hacer doble conteo poniendo beneficio en una celda y coste negativo por lo mismo en otra.

P: ¿Qué es el clasificador mayoritario (majority classifier) como baseline?
R: Un baseline que siempre predice la clase mayoritaria; si solo el 6% es positivo, un 94% de exactitud no demuestra nada.

P: ¿Qué es un decision stump?
R: Un árbol con un único nodo interno (una sola variable) que, según Holte (1993), da buen rendimiento base como baseline simple pero no simplista.

P: ¿Cómo se relacionan precision, recall y F-measure?
R: Precision = TP/(TP+FP); recall = tasa de verdaderos positivos = TP/(TP+FN); F-measure = media armónica de precision y recall.

## Preguntas de autoevaluación

P: ¿Por qué dos modelos con 80% de exactitud sobre datos balanceados pueden comportarse de forma muy distinta en la población real?
R: Porque cometen tipos de error opuestos: el Modelo A genera muchos falsos positivos y el B falsos negativos; aplicados a la población desbalanceada, la exactitud de A cae al 37% y la de B sube al 93%. (Sección: Clases desbalanceadas)

P: ¿Por qué no basta con contar juntos los falsos positivos y falsos negativos?
R: Porque asumir que importan igual casi nunca es cierto; en diagnóstico médico un falso negativo (no detectar un cáncer) suele ser mucho más grave que un falso positivo. Hay que asignarles costes/beneficios distintos. (Sección: Costes y beneficios desiguales)

P: ¿Cómo se calcula la probabilidad de cada celda de la matriz de confusión para el beneficio esperado?
R: Dividiendo el conteo de la celda por el total: `p(h,a) = count(h,a) / T`. (Sección: Valor esperado para evaluar modelos)

P: En el ejemplo de marketing dirigido, ¿cuál es el beneficio esperado por consumidor y qué significa?
R: Es ≈ $50,04 por consumidor: aplicando el modelo y contactando a quienes clasifica como positivos, se espera un beneficio medio de unos $50. (Sección: Valor esperado para evaluar modelos)

P: ¿Cómo detectar un doble conteo en la matriz de costes-beneficios?
R: Si un caso de fraude cuesta $1.000, poner +$1.000 por atraparlo y −$1.000 por omitirlo da $2.000; eso señala doble conteo, y uno de los dos valores debe ser cero. (Sección: Valor esperado para evaluar modelos)

P: ¿Por qué comparar un modelo con uno aleatorio es poco informativo?
R: Porque establece que hay información que extraer, pero batir el modelo aleatorio suele ser fácil; conviene usar baselines mejores como el clasificador mayoritario o el decision stump. (Sección: Baselines e inversión en datos)

P: ¿Cómo se cuantifica el valor de una fuente de datos según el capítulo?
R: Comparando un modelo con y sin cada fuente, lo que justifica su coste y trata los datos como un activo en el que invertir. (Sección: Baselines e inversión en datos)

## Puntos a dominar

- Entender por qué no existe una métrica universal y saber volver siempre a la pregunta de negocio.
- Construir e interpretar la matriz de confusión (TP, FP, FN, TN) y reconocer que es la base de casi todas las demás métricas.
- Explicar los dos problemas de la exactitud: clases desbalanceadas y tratar todos los errores por igual.
- Aplicar el marco de valor esperado tanto a una decisión individual como a la evaluación agregada de modelos.
- Derivar la regla de decisión del marketing dirigido (`p_R(x) > 0,01`) a partir de costes y beneficios.
- Factorizar los priors de clase para comparar modelos evaluados con distribuciones representativa y balanceada.
- Vigilar la consistencia de signos y el doble conteo en la matriz de costes-beneficios.
- Elegir baselines simples pero no simplistas: clasificador mayoritario, predicción del promedio, decision stump y reglas del dominio.
