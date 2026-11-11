# The Data Science Road Map (El mapa de ruta de la ciencia de datos) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son las etapas del Data Science Road Map?
R: Enmarcar el problema, entender los datos (preguntas básicas, data wrangling, análisis exploratorio), extraer features, modelar y analizar, y salir presentando resultados o desplegando código.

P: ¿Qué rasgo distingue la ciencia de datos de la ingeniería de software tradicional según el mapa?
R: El bucle de realimentación estrecho con el mundo real: "Model and Analyze" vuelve a enmarcar el problema una y otra vez, por lo que el proceso es profundamente iterativo.

P: ¿Cuáles son las dos maneras de salir del mapa y de qué dependen?
R: Presentar resultados o desplegar código, según si los clientes son humanos o máquinas; no son mutuamente excluyentes.

P: ¿Qué entregable corresponde a clientes humanos y cuál a clientes máquina?
R: Para humanos, una presentación o informe escrito para la toma de decisiones; para máquinas, un programa que realiza tareas analíticas y debe rendir bien y ser robusto.

P: ¿Dónde está la diferencia entre ciencia de datos excelente y mediocre?
R: En formular las preguntas correctas, no en las matemáticas ni en la ingeniería; ninguna competencia técnica compensa resolver un problema inútil.

P: ¿Qué es la "definition of done"?
R: Los criterios que fijan cuándo un proyecto está completado y, sobre todo, cuándo tiene éxito, aclarados antes de empezar.

P: ¿Qué son un SOW y un PRD?
R: Statements of work (consultoría) y project requirements documents (empresa que crea producto): documentos colaborativos con stakeholders que recogen el trabajo, prioridades y expectativas.

P: ¿Cuál es la pregunta más importante al entender los datos?
R: Si los datos pueden resolver el problema de negocio; si no, hay que buscar fuentes adicionales o modificar el plan.

P: ¿Qué es el data wrangling?
R: Llevar los datos de su formato bruto a uno apto para la analítica convencional mediante una tubería que los extrae, limpia o filtra y los deja en formato regular.

P: ¿Qué es una feature y qué significa extraer features?
R: Una feature es un número o categoría extraído de los datos que describe una entidad; extraer features es destilar los datos brutos en datos tabulares (filas = entidades, columnas = información que las describe).

P: ¿Por qué extraer buenas features es tan decisivo?
R: Es lo más importante para que el análisis funcione —más que clasificadores, estadística o código elegante— y es la parte más creativa y ligada a la pericia de dominio.

P: ¿Qué es la target variable y qué peculiaridad tiene?
R: La variable objetivo que se quiere predecir; a veces no existe como campo y hay que construirla (el autor inventó una forma de medir la "lealtad" de clientes).

P: ¿En qué dos categorías cae el código al desplegar?
R: Analítica por lotes (batch), que repite un análisis sobre datos futuros, y código en tiempo real, un módulo analítico dentro de un paquete mayor en un lenguaje de alto rendimiento.

P: ¿Por qué son imprescindibles las visualizaciones?
R: Porque es muy fácil malinterpretar las salidas de los algoritmos si solo se miran los números; no hay sustituto para el ojo humano al dar sentido intuitivo a los datos.

P: ¿Qué tres recomendaciones da el autor para iterar sin dolor?
R: Obtener resultados preliminares cuanto antes, automatizar todo el análisis en un único script ejecutable con un solo comando, y mantener el código modular y dividido en etapas claras.

## Preguntas de autoevaluación

P: ¿Por qué el código de un proyecto de ciencia de datos debe mantenerse muy flexible?
R: Porque las preguntas se reformulan constantemente dentro del bucle de iteración, a diferencia de la ingeniería de software tradicional donde se suele saber qué construir. (Lo que necesitas saber / Iterating)

P: ¿Qué función de autodefensa cumple un buen SOW?
R: Protege frente a reclamaciones si resulta imposible resolver el problema con los datos, si estos están corruptos o si el cliente pierde interés. (Frame the Problem)

P: Nombra al menos cuatro preguntas básicas que conviene hacerse al acceder a los datos.
R: Tamaño del dataset y si está completo; si es representativo; si hay outliers o ruido extraordinario; si se insertaron datos artificiales; si hay identificadores únicos y si lo son de verdad; qué significan los no-emparejamientos al unir datasets; y de dónde vienen las entradas en blanco. (Understand the Data: Basic Questions)

P: ¿Qué cuatro pasos recomienda el autor para descubrir cómo está roto un dataset?
R: Mirar el texto bruto en un editor; comprobar que la herramienta que debería abrir el dato lo procesa bien; hacer histogramas y scatterplots para ver si los números son realistas; y responder preguntas simples de respuesta conocida y comprobar si coinciden. (Understand the Data: Data Wrangling)

P: ¿Qué dos cosas se obtienen del análisis exploratorio?
R: Una intuición de cómo se ven visualmente los patrones relevantes y una lista de hipótesis concretas, a menudo motivadas por un gráfico revelador. (Understand the Data: Exploratory Analysis)

P: ¿En qué se diferencia el modelado con clientes humanos frente a clientes máquina?
R: Con humanos se suelen usar varios modelos ajustados de formas distintas; con máquinas hay que converger en un único modelo canónico para producción. (Model)

P: ¿Cuáles son los tres entregables típicos al desplegar código?
R: El propio código; documentación de cómo ejecutarlo (a veces un "run book"); y una forma de probarlo: unit tests para tiempo real y, para batch, un dataset de ejemplo con casos límite y su salida esperada. (Deploy Code)

P: ¿Qué error del autor ilustra por qué importan las preguntas básicas sobre los datos?
R: En un proyecto de series temporales de motores descubrió semanas después que a veces la serie terminaba antes del fallo y otras seguía tras la "muerte" del motor; los tiempos de fallo estaban en otra tabla que pudo haber cotejado al inicio. (Understand the Data: Basic Questions)

## Puntos a dominar

- Enumerar las etapas del Data Science Road Map y su orden, incluyendo las dos salidas posibles.
- Explicar el bucle de realimentación y por qué hace iterativa la ciencia de datos.
- Distinguir clientes humanos y máquinas y cómo cambian cada etapa y el entregable final.
- Comprender la importancia de enmarcar el problema (definition of done, SOW, PRD) sobre la destreza técnica.
- Reproducir la batería de preguntas básicas sobre los datos y la receta de cuatro pasos para detectar datos rotos.
- Definir feature, datos tabulares y target variable, y justificar por qué extraer features es lo más decisivo.
- Argumentar por qué las visualizaciones son imprescindibles pese a que la mayoría de algoritmos no sean visuales.
- Recordar las tres recomendaciones para iterar: resultados preliminares tempranos, script único ejecutable y código modular.
