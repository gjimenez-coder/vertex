# Business Problems and Data Science Solutions (Problemas de negocio y soluciones de ciencia de datos) — Estudio

## Tarjetas de repaso

P: ¿Qué idea central defiende el capítulo sobre la minería de datos?
R: Que es un proceso con etapas bien definidas, no una hazaña heroica dependiente del azar o del talento individual; combina tecnología (descubrimiento automático de patrones) con creatividad, conocimiento del negocio y sentido común.

P: ¿Cuáles son las nueve tareas canónicas de minería de datos?
R: Clasificación/estimación de probabilidad de clase, regresión, similarity matching, clustering, co-occurrence grouping, profiling, link prediction, data reduction y causal modeling.

P: ¿Cuál es la diferencia informal entre clasificación y regresión?
R: La clasificación predice *si* algo ocurrirá (objetivo categórico, a menudo binario) y la regresión *cuánto* ocurrirá (objetivo numérico).

P: ¿Qué distingue a un problema supervisado de uno no supervisado?
R: El supervisado fija un objetivo definido y requiere datos (*labels*) sobre él; el no supervisado no fija objetivo. El término viene del machine learning, donde un "profesor" supervisa aportando el objetivo con los ejemplos.

P: ¿Qué condición extra, además de definir el objetivo, exige la minería supervisada?
R: Que exista dato real sobre el objetivo (no basta con que exista en principio); adquirir y etiquetar ese dato (su *label*) suele ser una inversión clave que puede costar dinero.

P: ¿Qué diferencia hay entre clustering y co-occurrence grouping?
R: El clustering agrupa individuos por similitud sin propósito específico; el co-occurrence grouping (market-basket analysis, association rules) halla asociaciones entre entidades por aparecer juntas en transacciones.

P: ¿Para qué sirve el profiling y cómo se aplica a la detección de anomalías?
R: Caracteriza el comportamiento típico de un individuo, grupo o población; fija normas de comportamiento y el grado de desajuste con el perfil se usa como puntaje de sospecha (fraude, intrusiones).

P: ¿Qué es el causal modeling y qué métodos incluye?
R: Ayuda a entender qué eventos o acciones influyen realmente sobre otros; incluye experimentos controlados aleatorizados (A/B tests) y métodos sobre datos observacionales, ambos análisis contrafactual, y exige explicitar los supuestos de causalidad.

P: ¿Cuáles son las seis fases del proceso CRISP-DM?
R: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation y Deployment.

P: ¿Qué significa que en CRISP-DM "la iteración es la regla, no la excepción"?
R: Que pasar una vez por el proceso sin resolver el problema no es un fracaso, sino exploración que informa la siguiente iteración; hay atajos de retorno desde cada fase.

P: ¿Qué es una fuga (leak) en la preparación de datos?
R: Una variable del histórico que da información sobre el objetivo pero que no estaría disponible en el momento de decidir (ej.: "total de páginas visitadas en la sesión", conocido solo al terminar).

P: ¿Por qué es un error gestionar un proyecto de minería de datos como desarrollo de software?
R: Porque es una empresa exploratoria, más cercana a I+D que a la ingeniería; los resultados son inciertos y conviene invertir en reducir incertidumbre (pilotos, prototipos desechables) antes de ingenierizar prematuramente.

P: ¿En qué se diferencia el análisis de regresión estadístico del interés de la minería de datos?
R: La minería se interesa menos en explicar un conjunto histórico y más en extraer patrones que generalicen a datos nuevos para mejorar un proceso de negocio, reduciendo el sobreajuste.

P: ¿Cómo se relacionan Machine Learning y Data Mining (KDD)?
R: Data Mining (o KDD) nació como derivación de Machine Learning; siguen muy ligados y comparten técnicas, pero KDD está más orientado a aplicaciones, negocio y al proceso completo de análisis.

## Preguntas de autoevaluación

P: ¿Cuál es la "habilidad crítica" del científico de datos según el capítulo?
R: Descomponer un problema de negocio en subtareas que encajen en tareas conocidas con herramientas disponibles, resolverlas y recomponer las soluciones, evitando reinventar la rueda. (Sección "De los problemas de negocio a las tareas de minería de datos")

P: El problema de churn de MegaTelCo "¿podemos hallar grupos con alta probabilidad de cancelar al expirar su contrato?" ¿es supervisado o no supervisado, y por qué?
R: Supervisado, porque fija un objetivo (¿se irá el cliente?); además, predecir la probabilidad de continuar sigue siendo clasificación por tener objetivo categórico (class probability estimation). (Sección "Supervisado frente a no supervisado")

P: ¿Por qué hay que distinguir entre minar datos y usar los resultados de la minería?
R: Porque minar construye el modelo M a partir de datos históricos que incluyen el objetivo, mientras que el uso aplica M a clientes nuevos cuya clase se desconoce para generar un puntaje; son procesos distintos aunque el uso debe informar a la minería. (Sección "Minería de datos y sus resultados")

P: ¿Por qué el fraude con tarjeta se aborda de forma supervisada y el fraude de Medicare no?
R: El fraude con tarjeta tiene labels fiables (cliente y defraudador son personas distintas con metas opuestas); el de Medicare no tiene objetivo fiable porque los defraudadores son un subconjunto de usuarios legítimos, lo que exige enfoques no supervisados. (Sección "El proceso de minería de datos (CRISP-DM)", Data Understanding)

P: ¿Por qué un modelo con más del 99% de precisión puede ser inviable en la fase de Evaluation?
R: Porque puede generar demasiadas falsas alarmas y no cumplir los objetivos de negocio; la evaluación debe ser cuantitativa y cualitativa y considerar el contexto, incluida la comprensibilidad del modelo para los stakeholders. (Sección "El proceso de minería de datos (CRISP-DM)", Evaluation)

P: ¿Qué riesgo se asocia al Deployment y cómo mitigarlo?
R: El riesgo de transferencias "over the wall"; conviene involucrar pronto al equipo de desarrollo, recordando que el modelo desplegado no es lo que diseñan los científicos de datos, sino lo que construyen los ingenieros. (Sección "El proceso de minería de datos (CRISP-DM)", Deployment)

P: ¿Cuándo es apropiada una consulta a base de datos frente a la minería de datos?
R: La consulta es apropiada cuando el analista ya sospecha una subpoblación interesante y pide un subconjunto o estadísticas; la minería, en cambio, podría descubrir automáticamente esa consulta como patrón. (Sección "Otras técnicas y tecnologías analíticas", Database Querying)

P: ¿Cómo se responderían con distintas técnicas las preguntas sobre clientes rentables?
R: ¿Quiénes son los más rentables? → consulta a BD; ¿difieren del cliente medio? → prueba de hipótesis estadística; ¿cómo caracterizarlos? → minería de datos; ¿será rentable un cliente nuevo y cuánto? → minería predictiva (clasificación y regresión). (Sección "Otras técnicas y tecnologías analíticas")

## Puntos a dominar

- Reconocer las nueve tareas canónicas y saber a cuál corresponde un problema de negocio concreto.
- Clasificar un problema como supervisado o no supervisado y, si es supervisado, distinguir clasificación (objetivo categórico) de regresión (objetivo numérico).
- Verificar que exista dato real sobre el objetivo (labels) antes de plantear minería supervisada.
- Recorrer mentalmente las seis fases de CRISP-DM y asumir que la iteración es la norma.
- Detectar fugas (leaks) al definir y construir variables en Data Preparation.
- Evaluar los modelos con criterios cuantitativos, cualitativos y de negocio antes de desplegar.
- Gestionar el proyecto como I+D exploratorio, no como desarrollo de software.
- Situar la minería de datos frente a estadística, consultas a BD, data warehousing, análisis de regresión y machine learning, entendiendo que las complementa y no las sustituye.
