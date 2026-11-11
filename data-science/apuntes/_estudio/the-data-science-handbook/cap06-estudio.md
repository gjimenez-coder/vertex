# Machine Learning Overview (Panorama del aprendizaje automático) — Estudio

## Tarjetas de repaso

P: ¿Qué es técnicamente el machine learning según el capítulo? / R: Un subconjunto de la estadística, que por razones históricas evolucionó de forma independiente, a veces reinventando técnicas con otros nombres.

P: ¿De qué disciplina nace el machine learning y de cuál la estadística clásica? / R: El machine learning nace de la informática (con raíces en física e ingeniería); la estadística clásica surgió de las necesidades de los censos de gobierno y de la agricultura.

P: ¿Por qué no se da una definición cerrada de "machine learning"? / R: Porque es un término paraguas que abarca desde clasificación hasta clustering; en su lugar se enumeran rasgos comunes a casi todos los algoritmos.

P: ¿Cuáles son las comunalidades de los algoritmos de machine learning? / R: Se ejecutan en computadoras, toman datos como entrada, tratan esos datos como muestras de una distribución de probabilidad subyacente y trabajan con datos tabulares.

P: ¿Qué estructura tienen los datos tabulares? / R: Una fila por dato y una columna por feature (numérica, binaria o categórica).

P: ¿Por qué lo tabular habilita el análisis matemático? / R: Porque las filas de una tabla de n filas y d columnas se ven como posiciones en un espacio de d dimensiones.

P: ¿Cómo se relaciona el machine learning con el fracaso inicial de la AI? / R: Nació en parte de ese fracaso; el foco pasó de imitar la inteligencia humana a usar computadoras como proxy del juicio humano en tareas concretas y limitadas.

P: ¿Qué diferencia de enfoque hay entre la AI tradicional y el machine learning? / R: La AI tradicional usaba reglas e inferencia lógica; el machine learning es mucho más probabilístico al construir modelos e inferencias.

P: ¿Qué es el aprendizaje supervisado? / R: Aquel en que los datos de entrenamiento son puntos con una etiqueta o valor objetivo asociado, y el algoritmo busca estimar ese valor.

P: ¿Qué es el aprendizaje no supervisado y cuál es su ejemplo prototípico? / R: Solo hay datos crudos, sin nada concreto que predecir; se busca estructura subyacente. El ejemplo prototípico es el clustering.

P: ¿Por qué el supervisado es algo más común en aplicaciones reales? / R: Porque el negocio suele dictar algo específico que predecir, en lugar de un enfoque de "ver qué hay".

P: ¿Qué es el overfitting? / R: El modelo luce excelente sobre los datos de entrenamiento pero no generaliza a datos futuros (caso extremo: memorizar nombres y quién tuvo cáncer).

P: ¿Qué hace la k‐fold cross‐validation? / R: Mide el rendimiento de una familia de clasificadores: divide en k particiones, entrena con todas menos una y prueba en la restante, repite dejando fuera cada una y promedia las k métricas.

P: ¿Qué aporta un conjunto de validación aparte del de prueba? / R: Evita el sesgo de dejar que el test guíe la elección del modelo; el conjunto de validación solo se examina al final, sometiendo el modelo ya entrenado a la prueba real.

P: ¿En qué suele centrar su esfuerzo el científico de datos según Cady? / R: Usa clasificadores estándar y vuelca su esfuerzo en encontrar buenas features para alimentarlos, más que en técnicas punteras como deep learning.

## Preguntas de autoevaluación

P: ¿Cuál es la tesis central del capítulo sobre la relación entre machine learning y estadística? / R: Que el machine learning es técnicamente un subconjunto de la estadística, pero evolucionó aparte desde la informática y con herramientas probabilísticas. (Lo que necesitas saber; Ideas clave)

P: ¿Qué limitación común comparten casi todos los algoritmos respecto al tipo de datos? / R: Que SOLO manejan datos tabulares, aunque manejan casi cualquier dataset tabular. (Qué comparten los algoritmos de machine learning)

P: ¿Por qué dejó de usarse el término "artificial intelligence" en los círculos de informática? / R: Porque la AI fracasó respecto a su propia expectativa de crear máquinas pensantes, y en parte por vergüenza se abandonó el término (aunque está volviendo sin la sobrepromesa). (6.1 Contexto histórico)

P: ¿Cómo se usa el aprendizaje no supervisado junto con el supervisado? / R: Como paso de preprocesamiento para extraer features significativas que luego se emplean en aprendizaje supervisado. (6.2 Supervisado frente a no supervisado)

P: ¿Por qué es crítica la aleatoriedad al dividir datos en entrenamiento y prueba? / R: Para evitar sesgos involuntarios, por ejemplo tomar la primera mitad del archivo, que pudo recogerse antes. (6.3 Datos de entrenamiento, de prueba y el gran coco del overfitting)

P: ¿Qué sesgo sutil evita separar en training, testing y validation? / R: Que, al elegir entre varios modelos por su rendimiento en el test, el test influya en la elección (una forma débil de entrenar sobre los datos de prueba). (6.3)

P: ¿Por qué, al reentrenar periódicamente, conviene probar con la semana N+1 en vez del mismo período? / R: Porque las razones por las que la gente hace clic en anuncios pueden cambiar durante la semana, y probar con datos del mismo período puede inflar artificialmente el rendimiento. (6.3)

## Puntos a dominar

- Entender que el machine learning es un subconjunto de la estadística con origen histórico independiente (informática, enfoque probabilístico).
- Enumerar las comunalidades de los algoritmos: computadoras, datos como muestras de una distribución, datos tabulares.
- Explicar por qué lo tabular (filas como puntos en un espacio d‑dimensional) habilita el análisis matemático.
- Distinguir aprendizaje supervisado (valor objetivo a predecir) de no supervisado (hallar patrones, p. ej. clustering), y su uso combinado.
- Reconocer el overfitting como el mayor riesgo y saber ilustrarlo con el caso de memorizar el dato de entrenamiento.
- Describir las formas de separar datos: división aleatoria, k‐fold cross‐validation, training/testing/validation, y el enfoque por períodos al reentrenar.
- Recordar que el esfuerzo del científico de datos suele ir a encontrar buenas features más que a técnicas punteras.
