# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 15 — Appendix A. Proposal Review Guide (Apéndice A. Guía de revisión de propuestas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El apéndice A es una guía práctica de preguntas para evaluar de forma sistemática proyectos de data mining. La tesis es que el pensamiento analítico que enseña el libro permite valorar propuestas y detectar sus posibles fallos, tanto en autoevaluación de las propias como al revisar las de equipos internos de data science o de consultores externos.

Las preguntas se organizan según el proceso de data mining expuesto en el capítulo 2, que sirve como marco conceptual de todo el libro. La lista no pretende ser exhaustiva, sino reunir una selección de las preguntas más importantes que conviene tener presentes al considerar un proyecto.

El libro se centra en proyectos cuyo objetivo es extraer regularidades, patrones o modelos de los datos, y la guía lo refleja. Hay proyectos de data science donde esas regularidades no están definidas con tanta claridad —por ejemplo, muchos proyectos de visualización de datos no tienen al inicio objetivos de modelado bien definidos—, pero el proceso de data mining igual ayuda a estructurar el pensamiento: simplemente se parecen más al data mining no supervisado que al supervisado.

## Business and Data Understanding (Comprensión del negocio y de los datos)

- ¿Cuál es exactamente el problema de negocio a resolver?
- ¿La solución de data science está formulada de forma apropiada para resolverlo? A veces hay que hacer aproximaciones juiciosas.
- ¿A qué entidad de negocio corresponde una instancia/ejemplo?
- ¿El problema es supervisado o no supervisado?
  - Si es supervisado: ¿hay una variable objetivo (target) definida? ¿Está definida con precisión? Piensa en los valores que puede tomar.
- ¿Los atributos están definidos con precisión? Piensa en sus posibles valores.
- En problemas supervisados: ¿modelar esa variable objetivo mejorará el problema de negocio planteado, o un subproblema importante? Si es un subproblema, ¿se aborda el resto del problema de negocio?
- ¿Formular el problema en términos de expected value (valor esperado) ayuda a estructurar las subtareas a resolver?
- Si es no supervisado, ¿está bien definido un camino de "análisis exploratorio de datos"? Es decir, ¿hacia dónde va el análisis?

## Data Preparation (Preparación de datos)

- ¿Será práctico obtener valores para los atributos, crear vectores de características y volcarlos en una única tabla?
- Si no, ¿se define con claridad un formato de datos alternativo? ¿Se tiene en cuenta en las etapas posteriores? (Muchas técnicas posteriores asumen formato de vector de características.)
- Si el modelado será supervisado, ¿está bien definida la variable objetivo? ¿Está claro cómo obtener sus valores para entrenamiento y prueba y ponerlos en la tabla?
- ¿Cómo se adquirirán exactamente los valores de la variable objetivo? ¿Hay costes asociados? Si los hay, ¿se contemplan en la propuesta?
- ¿Los datos proceden de una población similar a aquella donde se aplicará el modelo? Si hay discrepancias, ¿se señalan con claridad los sesgos de selección? ¿Hay un plan para compensarlos?

## Modeling (Modelado)

- ¿La elección del modelo es apropiada para la variable objetivo elegida (clasificación, estimación de probabilidad de clase, ranking, regresión, clustering, etc.)?
- ¿El modelo o la técnica cumple el resto de requisitos de la tarea: rendimiento de generalización, comprensibilidad, velocidad de aprendizaje y de aplicación, cantidad de datos requerida, tipo de datos, valores perdidos?
  - ¿La técnica es compatible con el conocimiento previo del problema (p. ej., no proponer un modelo lineal para un problema claramente no lineal)?
- ¿Deberían probarse y compararse varios modelos en la evaluación?
- Para clustering, ¿hay una métrica de similitud definida? ¿Tiene sentido para el problema de negocio?

## Evaluation and Deployment (Evaluación y despliegue)

- ¿Hay un plan de validación con conocimiento del dominio? ¿Los expertos o stakeholders querrán revisar el modelo antes del despliegue? Si es así, ¿estará en una forma que puedan entender?
- ¿El montaje de la evaluación y la métrica son apropiados para la tarea de negocio? Recuerda la formulación original.
  - ¿Se tienen en cuenta costes y beneficios de negocio?
  - En clasificación, ¿cómo se elige el umbral? ¿Se usan directamente las estimaciones de probabilidad? ¿Es más apropiado el ranking (p. ej., con presupuesto fijo)?
  - En regresión, ¿cómo se evaluará la calidad de las predicciones numéricas y por qué es la forma correcta en el contexto del problema?
- ¿La evaluación usa datos de holdout? La validación cruzada (cross-validation) es una técnica.
- ¿Contra qué baselines se compararán los resultados? ¿Por qué tienen sentido en el contexto del problema real? ¿Hay un plan para evaluarlos objetivamente también?
- Para clustering, ¿cómo se entenderá el agrupamiento obtenido?
- ¿El despliegue tal como se planea abordará realmente (de la mejor manera) el problema de negocio?
- Si el gasto del proyecto debe justificarse ante los stakeholders, ¿cuál es el plan para medir el impacto de negocio final del modelo desplegado?

## Ideas clave

- La guía ofrece preguntas sistemáticas para evaluar propuestas de data mining, propias o ajenas, y detectar sus fallos.
- Se estructura según las fases del proceso de data mining del capítulo 2: comprensión del negocio y de los datos, preparación, modelado, y evaluación y despliegue.
- Empezar siempre por el problema de negocio: definirlo con precisión y comprobar que la solución de data science lo resuelve, aun con aproximaciones juiciosas.
- Distinguir problema supervisado vs. no supervisado condiciona si hay variable objetivo precisa o un camino exploratorio bien definido.
- En la preparación importa la viabilidad de los vectores de características, el coste de obtener el target y los sesgos de selección entre poblaciones.
- La elección del modelo debe encajar con el target y con requisitos como comprensibilidad, velocidad, datos disponibles y conocimiento previo.
- La evaluación debe reflejar costes y beneficios de negocio, usar datos de holdout y compararse con baselines con sentido en el problema real.
- No es una lista exhaustiva, sino una selección de las preguntas más importantes a tener en mente.
