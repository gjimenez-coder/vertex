# Data Visualization and Fraud Detection (Visualización de datos y detección de fraude) — Estudio

## Tarjetas de repaso

P: ¿Qué proponen Tarde y Latour, según Hansen, sobre los datos sociales? / R: Seguir al individuo y no solo al agregado; el todo es una "visualización provisional" reversible volviendo a los componentes individuales.

P: ¿Qué significa la cita de Latour "Change the instruments and you will change the entire social theory that goes with them"? / R: Que al cambiar los métodos de recolección cambia la teoría; teniendo todos los datos ya no hay que limitarse a estadísticas agregadas heredadas de restricciones pasadas.

P: ¿Qué es una ciencia de datos "expansionist" para Hansen? / R: La que integra prácticas de otras disciplinas (ciencias sociales, diseño, periodismo, humanidades digitales) en lugar de limitarse a las matemáticas; todo puede ser dato.

P: ¿Para qué usuarios está diseñado el lenguaje Processing y qué lo caracteriza? / R: Para artistas y diseñadores; permite especificar formas, renderizar, bocetar en 3D, animar, interactuar y, sobre todo, publicar (basado en Java, con botón de "publish").

P: ¿Qué es el "distant reading" de Franco Moretti? / R: Captar de qué trata un texto sin leerlo línea a línea; un pensamiento tipo PCA, una reducción de dimensión de novelas.

P: Según Ian Wong, ¿por qué "hacer machine learning no es escribir scripts de R"? / R: Porque el ML se funda en matemáticas, se expresa en código y se ensambla en software; hay que escribir código legible y reutilizable para el lector, no para el escritor.

P: ¿Por qué la detección de fraude en Square es un problema semi-supervisado? / R: Porque las etiquetas cambian (un cargo puede rechazarse y luego aceptarse, o aceptarse y luego ser malo); el "label churn" solo se estabiliza a los pocos meses con los chargebacks.

P: ¿Por qué la Accuracy engaña con pocas transacciones fraudulentas? / R: Porque con clases muy desbalanceadas un modelo que dice "nada es fraudulento" tiene buena exactitud pero es inútil.

P: ¿Cómo se definen Precision y Recall en el contexto de fraude? / R: Precision = TP/(TP+FP), probabilidad de que lo marcado como fraude lo sea; Recall = TP/(TP+FN), probabilidad de cazar un fraude real.

P: ¿Qué quiere decir que las etiquetas son "la mitad olvidada" de los datos? / R: Que definirlas y capturarlas de forma fiable (granularidad de evento o entidad, sistemas a integrar) es de lo más difícil, y el ruido afecta mucho con clases desbalanceadas.

P: ¿Qué retos añade el desbalance de clases al modelado de features? / R: Riesgo de overfitting (el tamaño de muestra necesario es proporcional a la clase "fraude"), binning de categóricas con muchos niveles, cold start con vendedores nuevos y comportamiento adversario.

P: ¿Cómo organiza Square su código y dónde escriben scripts? / R: En carpetas reutilizables Model, Signal, Error, Experiment y Test; solo escriben scripts en Experiment, revisitados para generar conocimiento.

P: ¿Qué es el pair programming tal como lo practican en Square? / R: Dos personas sobre un problema común: un "driver" escribe y un "observer" revisa y planifica, turnándose; cuando no se puede emparejar, se revisan pull requests como peer review.

P: ¿Qué es la "ambient analytics" y qué métricas vigila Ian? / R: Ingerir datos de forma pasiva y constante para desarrollar un instinto sobre ellos; vigila "clear rates" y "freeze rates" diarios y cuántos eventos se revisaron.

P: Según Wong, ¿qué hace difícil "productionizar" un modelo? / R: Calcular las features en tiempo real (milisegundos) sobre datos que crecen y minimizar la discrepancia entre rendimiento offline y online ("lo que ves es lo que obtienes").

## Preguntas de autoevaluación

P: ¿Por qué Hansen objeta la idea de Tukey de "jugar en el patio de todos"? / R: Porque traza una línea entre los campos de datos tradicionales y "todo lo demás" y sugiere que somos superhumanos uber-nerds, una visión egocéntrica y arrogante; la tecnología nace de las necesidades de cada disciplina (GIS de los geógrafos, minería de texto de las humanidades digitales). (Sección "Qué es la ciencia de datos, revisitado")

P: ¿Qué moraleja deja el proyecto Million Dollar Blocks? / R: Que puedas ponerlo en un mapa no significa que debas; a veces hay que cavar más hondo y darle la vuelta a los datos para encontrar la historia. (Sección "Una muestra de proyectos de visualización")

P: ¿Cuál es el dilema de costes del riesgo en Square con el ejemplo de John, el food truck? / R: Si deja pasar un cargo malo acaba pagándolo porque el defraudador suele ser insolvente; si bloquea uno legítimo pierde la confianza del cliente: los falsos positivos erosionan la confianza y los falsos negativos cuestan dinero. (Sección "El reto del riesgo")

P: ¿Por qué Wong recomienda subir la estimación del rendimiento al principio del proceso? / R: Porque la receta escolar (datos, features, entrenar, estimar, publicar) no basta; hay que pensar primero en el objetivo y en cómo se medirá el error. (Sección "El reto del riesgo" / "El problema de la estimación del rendimiento")

P: ¿Qué ejemplo ilustra que a veces no hay ground truth para las etiquetas? / R: Itamar Rosenn, primer data scientist de Facebook, con la dificultad de definir "usuario comprometido": no hay verdad de base y se definen y predicen las etiquetas a la vez. (Sección "El problema de la estimación del rendimiento")

P: ¿Cómo ilustra Wong el comportamiento adversario y qué respuesta exige? / R: Si un atacante descubre que se detecta fraude por coincidencia exacta de direcciones, abre 10 cuentas con la misma dirección mal escrita; como los modelos se degradan al burlarlos, hay que vigilar el rendimiento y reentrenar. (Sección "El problema de la estimación del rendimiento")

P: ¿Por qué importa más el código que el modelo o el paquete concreto? / R: Porque empezar preguntando "¿qué modelo o paquete usas?" pierde el bosque; lo que importa es poder usar y reemplazar modelos con facilidad, con legibilidad, reutilización, corrección, estructura e higiene y tests. (Sección "Consejos para construir modelos")

P: ¿Cómo integra Square la visualización en la gestión de riesgo? / R: Con una herramienta de flujo de trabajo (tipo mission control) e "information radiators" que, junto al ML, forman un exoesqueleto para que el equipo de operaciones detecte patrones sospechosos y mida la salud del negocio ("What gets measured gets managed"). (Sección "Visualización de datos en Square")

## Checklist

Puntos a dominar:
- Explicar la postura "expansionist" de Hansen y la idea de que todo es dato, con el argumento de Tarde y Latour sobre seguir al individuo.
- Reconocer la detección de fraude como problema semi-supervisado y el concepto de "label churn".
- Calcular e interpretar la matriz de confusión, Accuracy, Precision y Recall, y saber cuándo la exactitud engaña con clases desbalanceadas.
- Justificar por qué las etiquetas son "la mitad olvidada" y los efectos del ruido con alto desbalance.
- Enumerar los retos del desbalance de clases: overfitting, binning de categóricas, cold start y comportamiento adversario.
- Describir la organización de código de Square (Model, Signal, Error, Experiment, Test) y el papel del pair programming y los tests.
- Explicar los retos de puesta en producción: cálculo de features en tiempo real y coherencia offline/online.
- Distinguir los usos de la visualización en Square: revisiones eficientes, patrones por cliente/segmento, salud del negocio y "ambient analytics".
