# Appendix A. Proposal Review Guide — Estudio

## Tarjetas de repaso

P: ¿Cuál es el propósito del Apéndice A? / R: Ofrecer una guía práctica de preguntas para evaluar de forma sistemática proyectos de data mining, tanto propios como de equipos internos o consultores externos.

P: ¿Cómo se organizan las preguntas de la guía? / R: Según las fases del proceso de data mining del capítulo 2: comprensión del negocio y de los datos, preparación de datos, modelado, y evaluación y despliegue.

P: ¿Pretende ser una lista exhaustiva? / R: No; reúne una selección de las preguntas más importantes a tener presentes al considerar un proyecto.

P: ¿Por dónde conviene empezar al evaluar una propuesta? / R: Por el problema de negocio: definirlo con exactitud y comprobar que la solución de data science está formulada apropiadamente para resolverlo, aun con aproximaciones juiciosas.

P: ¿Qué distingue a un problema supervisado de uno no supervisado en la guía? / R: El supervisado requiere una variable objetivo (target) definida con precisión; el no supervisado requiere un camino de análisis exploratorio bien definido.

P: ¿Para qué ayuda formular el problema en términos de expected value? / R: Para estructurar las subtareas que hay que resolver.

P: ¿Qué cuestiones clave plantea la preparación de datos? / R: La viabilidad de crear vectores de características en una tabla única, el coste de obtener los valores del target y los sesgos de selección entre poblaciones.

P: ¿Por qué importa que los datos procedan de una población similar a la de aplicación? / R: Porque las discrepancias generan sesgos de selección que deben señalarse y, si es posible, compensarse con un plan.

P: ¿Qué requisitos, además del tipo de target, debe cumplir el modelo elegido? / R: Rendimiento de generalización, comprensibilidad, velocidad de aprendizaje y aplicación, cantidad de datos requerida, tipo de datos y manejo de valores perdidos.

P: ¿Qué ejemplo de incompatibilidad con el conocimiento previo menciona el modelado? / R: Proponer un modelo lineal para un problema claramente no lineal.

P: ¿Qué debe tener en cuenta la evaluación respecto al negocio? / R: Los costes y beneficios de negocio, recordando la formulación original del problema.

P: En clasificación, ¿qué preguntas plantea la elección del umbral? / R: Cómo se elige el umbral, si se usan directamente las estimaciones de probabilidad y si es más apropiado el ranking (p. ej., con presupuesto fijo).

P: ¿Qué papel juegan los baselines en la evaluación? / R: Sirven de comparación; deben tener sentido en el contexto del problema real y contar con un plan para evaluarlos objetivamente.

P: ¿Qué técnica se cita para la evaluación con datos de holdout? / R: La validación cruzada (cross-validation).

P: Para clustering, ¿qué dos cuestiones se destacan? / R: Que exista una métrica de similitud con sentido para el negocio y que se defina cómo se entenderá el agrupamiento obtenido.

## Preguntas de autoevaluación

P: ¿Por qué el pensamiento analítico del libro sirve para revisar propuestas? / R: Porque permite valorar sistemáticamente los proyectos y detectar posibles fallos, en autoevaluación de las propias y al revisar las de equipos internos o consultores externos. (Lo que necesitas saber)

P: ¿Cómo encajan en la guía los proyectos sin objetivos de modelado claros, como la visualización de datos? / R: El proceso de data mining igual ayuda a estructurar el pensamiento; se parecen más al data mining no supervisado que al supervisado. (Lo que necesitas saber)

P: Si un problema supervisado solo resuelve un subproblema, ¿qué hay que verificar? / R: Que modelar esa variable objetivo mejore el problema de negocio o un subproblema importante y que se aborde el resto del problema de negocio. (Business and Data Understanding)

P: ¿Qué hay que preguntar sobre la adquisición del valor de la variable objetivo? / R: Cómo se adquirirán exactamente sus valores, si hay costes asociados y si esos costes se contemplan en la propuesta. (Data Preparation)

P: ¿Por qué importa el formato de vector de características en la preparación? / R: Porque muchas técnicas posteriores lo asumen; si no es práctico, hay que definir con claridad un formato alternativo y tenerlo en cuenta en etapas posteriores. (Data Preparation)

P: ¿Qué debe revisarse sobre la participación de expertos antes del despliegue? / R: Si hay un plan de validación con conocimiento del dominio y si los expertos o stakeholders querrán revisar el modelo en una forma que puedan entender. (Evaluation and Deployment)

P: ¿Cómo evaluar un problema de regresión según la guía? / R: Definiendo cómo se evaluará la calidad de las predicciones numéricas y por qué esa forma es la correcta en el contexto del problema. (Evaluation and Deployment)

P: ¿Qué se debe planear si el gasto del proyecto debe justificarse ante los stakeholders? / R: Un plan para medir el impacto de negocio final del modelo desplegado. (Evaluation and Deployment)

## Puntos a dominar

- Empezar por el problema de negocio: definirlo con precisión y comprobar que la solución de data science lo resuelve.
- Identificar la entidad de negocio que corresponde a cada instancia/ejemplo.
- Distinguir si el problema es supervisado o no supervisado y sus implicaciones (target preciso vs. camino exploratorio definido).
- Verificar que atributos y variable objetivo estén definidos con precisión, pensando en sus posibles valores.
- Evaluar la viabilidad de obtener atributos y vectores de características en una tabla única, o definir un formato alternativo.
- Considerar los costes de obtener el target y los sesgos de selección entre la población de entrenamiento y la de aplicación.
- Comprobar que la elección del modelo encaja con el target y con requisitos de generalización, comprensibilidad, velocidad, datos y valores perdidos.
- Planear la comparación de varios modelos y, en clustering, definir una métrica de similitud con sentido.
- Asegurar que la evaluación refleje costes y beneficios de negocio, use datos de holdout y se compare con baselines pertinentes.
- Confirmar que el despliegue planeado abordará realmente el problema de negocio y que existe un plan para medir su impacto final.
