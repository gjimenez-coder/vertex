# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 6 — Machine Learning Overview (Panorama del aprendizaje automático)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo breve sitúa el machine learning dentro del trabajo del científico de datos antes de entrar en técnicas concretas en los capítulos siguientes. La tesis de Cady es que el machine learning es, técnicamente, un subconjunto de la estadística, pero que por razones históricas evolucionó de forma independiente, a veces reinventando técnicas con otros nombres. Nace de la informática (con raíces en física e ingeniería), mientras que la estadística clásica surgió de las necesidades de los censos de gobierno y de la agricultura.

No se ofrece una definición cerrada de "machine learning" porque es un término paraguas que abarca desde clasificación hasta clustering. En su lugar se dan rasgos comunes a casi todos los algoritmos: se ejecutan en computadoras, toman datos como entrada, tratan esos datos como muestras de una distribución de probabilidad "del mundo real" y trabajan con datos tabulares (una fila por dato, una columna por feature, numérica, binaria o categórica).

Sales sabiendo de dónde viene el campo, la distinción entre aprendizaje supervisado y no supervisado, y el mayor quebradero de cabeza del machine learning: el overfitting, junto con las formas de separar datos de entrenamiento y de prueba para detectarlo.

## Qué comparten los algoritmos de machine learning

Cady evita una definición precisa y enumera las comunalidades (PDF p. 96):

- Todo se hace con computadoras, para cálculos intratables a mano.
- Toma datos como entrada; simular un sistema a partir de un modelo idealizado no es machine learning.
- Los datos se consideran muestras de una distribución de probabilidad subyacente.
- Los datos son tabulares: una fila por dato, una columna por feature.

La última propiedad es la clave: la mayoría de los algoritmos manejan casi cualquier dataset tabular, pero SOLO manejan datos tabulares. Lo tabular se presta al análisis matemático porque las filas de una tabla de n filas y d columnas se ven como posiciones en un espacio de d dimensiones; por eso el machine learning es lo más sofisticado matemáticamente que suele hacer un científico de datos. La meta habitual es hallar patrones en las muestras que digan algo sobre la distribución completa o que permitan procesar otras muestras de ella.

## 6.1 Contexto histórico

El machine learning nació en parte del fracaso inicial del movimiento de la inteligencia artificial (AI). Durante mucho tiempo se esperaba que las máquinas pensantes estaban a pocos años de distancia; se cuenta la anécdota de que Marvin Minsky asignó a un estudiante resolver la visión por computadora en un verano. Se concebía el cerebro humano como un gran motor lógico y el foco estaba en imitar el procesamiento lógico humano.

La AI fracasó respecto a su propia expectativa, y en parte por vergüenza el término "artificial intelligence" dejó de usarse en los círculos de informática (aunque está volviendo, sin la sobrepromesa). Seguimos tan lejos de imitar la inteligencia humana como siempre, porque el cerebro es muchísimo más complejo que un motor lógico.

El foco se desplazó de crear inteligencia verdadera a usar computadoras para tareas que históricamente hacía una persona: reconocer si hay un pájaro en una foto, decidir si un correo es spam, o detectar un "evento interesante" en una serie temporal. El machine learning se construyó usando computadoras como proxy del juicio humano en situaciones concretas y limitadas; luego esas técnicas se aplicaron a muchas áreas y maduró como herramienta estándar.

También cambiaron las herramientas: la AI tradicional usaba un enfoque basado en reglas e inferencia lógica; el machine learning es mucho más probabilístico al construir modelos e inferencias. Cady anticipa una crítica por no profundizar en áreas punteras como deep learning: en su experiencia, los científicos de datos rara vez llegan tan lejos; usan clasificadores estándar y vuelcan su esfuerzo en encontrar buenas features para alimentarlos.

## 6.2 Supervisado frente a no supervisado

Hay dos tipos principales de machine learning. En el aprendizaje supervisado los datos de entrenamiento son puntos con una etiqueta o valor objetivo asociado, y el algoritmo busca estimar ese valor. Ejemplo: datos de pacientes con el contenido de una gota de sangre y si luego desarrollaron cáncer; predecir el riesgo de futuros pacientes a partir de su sangre es un problema supervisado.

En el aprendizaje no supervisado solo hay datos crudos, sin nada concreto que predecir; se usa para hallar patrones y desentrañar la estructura subyacente. Los algoritmos de clustering, que dividen un dataset en agrupaciones "naturales", son el ejemplo prototípico.

El supervisado es algo más común en aplicaciones reales, porque el negocio suele dictar algo específico que predecir en lugar de un enfoque de "ver qué hay". Aun así, los algoritmos no supervisados se emplean como paso de preprocesamiento para extraer features significativas, que luego se usan en aprendizaje supervisado.

## 6.3 Datos de entrenamiento, de prueba y el gran coco del overfitting

El mayor dolor de cabeza del machine learning es el overfitting: los resultados lucen excelentes sobre los datos con que se entrenó, pero no generalizan a datos futuros. Caso extremo: si el dataset de pacientes incluyera sus nombres y el clasificador memorizara quién tuvo cáncer, acertaría al 100% con los conocidos y sería inútil con cualquier otro.

La solución es entrenar con parte de los datos y evaluar con otra parte. Formas de hacerlo:

- Dividir aleatoriamente los puntos entre entrenamiento y prueba. La aleatoriedad es crítica para evitar sesgos involuntarios (por ejemplo, tomar la primera mitad del archivo, que pudo recogerse antes). Este enfoque crudo suele bastar en la práctica.
- k‐fold cross‐validation (específico de supervisado): mide el rendimiento de una familia de clasificadores, no de uno concreto. Se divide el dato en k particiones; se entrena con todas menos una y se prueba en la que quedó fuera; se repite dejando fuera cada partición, obteniendo k clasificadores y k métricas; se promedian las métricas como mejor estimación del rendimiento "verdadero" de esa familia sobre ese tipo de dato.
- Con mayor rigor estadístico, dividir en training set, testing set y validation set. El conjunto de validación solo se examina al final. Evita un sesgo sutil: con solo training/testing y varios modelos a elegir, se escogería el que mejor rinde en el test, lo que es una forma débil de entrenar sobre los datos de prueba porque el test influye en la elección del modelo; la validación somete el modelo ya entrenado a la prueba real.
- Un enfoque sin nombre, útil cuando un modelo se reentrena periódicamente (por ejemplo, cada semana con los datos nuevos): entrenar con todos los datos de la semana N y anteriores, y probar con los de la semana N + 1. Las razones por las que la gente hace clic en anuncios pueden cambiar durante la semana, así que probar con datos del mismo período puede inflar artificialmente el rendimiento.

El glosario del capítulo (PDF p. 100) define, entre otros: inteligencia artificial, machine learning, overfitting, aprendizaje supervisado y no supervisado, datos tabulares, y datos de entrenamiento y de prueba.

## Ideas clave

- El machine learning es, en el fondo, un subconjunto de la estadística, pero evolucionó aparte desde la informática y con herramientas probabilísticas, no basadas en reglas.
- Casi todos los algoritmos comparten lo mismo: usan computadoras, toman datos como muestras de una distribución y SOLO trabajan con datos tabulares.
- Lo tabular convierte cada fila en un punto en un espacio d‑dimensional, lo que habilita el análisis matemático del machine learning.
- Supervisado = hay un valor objetivo que predecir; no supervisado = solo se buscan patrones (p. ej., clustering); a menudo el no supervisado preprocesa features para el supervisado.
- El overfitting es el mayor riesgo: el modelo memoriza el dato de entrenamiento y no generaliza.
- Separar entrenamiento y prueba (con aleatoriedad) lo detecta; k‑fold cross‐validation estima el rendimiento de una familia de clasificadores.
- Un conjunto de validación aparte evita el sesgo de dejar que el test guíe la elección del modelo.
- El científico de datos suele usar clasificadores estándar y centrar su esfuerzo en encontrar buenas features, más que en técnicas punteras.
