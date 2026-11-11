# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 2 — Business Problems and Data Science Solutions (Problemas de negocio y soluciones de ciencia de datos)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF como (PDF p. N).

## Lo que necesitas saber

El capítulo defiende una idea central: la minería de datos es un proceso con etapas bien definidas, no una hazaña heroica dependiente del azar o del talento individual. Parte de ese proceso aplica tecnología (descubrimiento automático de patrones), pero otra parte exige creatividad, conocimiento del negocio y sentido común del analista. Entender el proceso completo permite estructurar los proyectos como análisis sistemáticos.

Para hablar del proceso con concreción, primero se presenta un catálogo de tareas canónicas de minería de datos. Una habilidad crítica del científico de datos es descomponer un problema de negocio en subtareas, de modo que cada pieza encaje en una tarea conocida con herramientas disponibles, evitando reinventar la rueda y reservando el esfuerzo humano para lo que no se ha automatizado.

Sales sabiendo (i) los nueve tipos de tareas canónicas, (ii) la distinción entre minería supervisada y no supervisada y entre clasificación y regresión, (iii) las seis fases del proceso CRISP-DM, (iv) por qué gestionar estos proyectos como desarrollo de software es un error, y (v) cómo se relaciona la minería de datos con estadística, consultas a bases de datos, data warehousing, análisis de regresión y machine learning.

## El ejemplo que recorre el capítulo

El hilo conductor es el problema de *churn* (abandono) de MegaTelCo: estimar, a partir de datos históricos, la probabilidad de que un cliente cancele su contrato poco después de que expire, para actuar en consecuencia. El caso sirve para ilustrar casi todos los conceptos, junto con ejemplos de detección de fraude y de clientes rentables.

## De los problemas de negocio a las tareas de minería de datos

Cada problema de decisión basado en datos es único, pero bajo él subyacen tareas comunes. El científico de datos, junto con los *stakeholders*, descompone el problema en subtareas; algunas son idiosincrásicas y otras son tareas estándar de minería de datos. Pese a la abundancia de algoritmos, solo existe un puñado de tipos de tarea fundamentalmente distintos. El texto define nueve ("un individuo" es cualquier entidad sobre la que hay datos: un cliente, un consumidor o incluso un negocio):

1. **Clasificación y estimación de probabilidad de clase**: predice a cuál de un conjunto pequeño de clases (normalmente mutuamente excluyentes) pertenece cada individuo. Ej.: ¿qué clientes responderán a una oferta (will respond / will not respond)? El *scoring* es una tarea cercana: en vez de la clase, produce un puntaje o probabilidad de pertenencia. Un modelo que hace una tarea suele poder adaptarse a la otra.
2. **Regresión (estimación de valor)**: estima el valor numérico de una variable para cada individuo. Ej.: ¿cuánto usará el servicio este cliente? Informalmente, la clasificación predice *si* algo ocurrirá y la regresión *cuánto* ocurrirá.
3. **Similarity matching**: identifica individuos similares según sus datos. Ej.: IBM busca empresas parecidas a sus mejores clientes usando datos "firmographic". Es base de recomendaciones de producto y de otras tareas.
4. **Clustering**: agrupa individuos por similitud, sin un propósito específico. Ej.: ¿forman los clientes grupos naturales? Útil en exploración preliminar del dominio.
5. **Co-occurrence grouping** (frequent itemset mining, association rules, market-basket analysis): halla asociaciones entre entidades según transacciones. Ej.: ¿qué productos se compran juntos? Su resultado describe ítems que co-ocurren, con estadísticas de frecuencia y de cuán sorprendente es la asociación. A diferencia del clustering, mira la similitud por aparecer juntos en transacciones.
6. **Profiling (behavior description)**: caracteriza el comportamiento típico de un individuo, grupo o población. Ej.: ¿cuál es el uso típico de móvil de este segmento? Sirve para fijar normas de comportamiento en detección de anomalías (fraude, intrusiones): el grado de desajuste con el perfil se usa como puntaje de sospecha.
7. **Link prediction**: predice conexiones entre elementos (y a veces su fuerza). Ej.: en redes sociales, sugerir amistades por amigos en común; en recomendación de películas, predecir enlaces fuertes inexistentes entre clientes y películas.
8. **Data reduction**: reemplaza un conjunto grande de datos por otro menor que conserva la información importante. Suele implicar pérdida de información; lo que importa es el intercambio por mayor claridad (ej.: reducir datos de visionado a preferencias de género latentes).
9. **Causal modeling**: ayuda a entender qué eventos o acciones influyen realmente sobre otros. Incluye experimentos controlados aleatorizados (los "A/B tests") y métodos para inferir causalidad de datos observacionales; ambos son análisis "contrafactual". Un científico de datos cuidadoso debe explicitar siempre los supuestos necesarios para que la conclusión causal se sostenga (el "efecto placebo" ilustra un supuesto pasado por alto).

El libro ilustra sus principios sobre todo con clasificación, regresión, similarity matching y clustering. El problema de churn suele formularse como segmentar clientes más o menos propensos a irse, lo que suena a clasificación, clustering o regresión; para decidir falta una distinción clave.

## Supervisado frente a no supervisado

"¿Caen los clientes en grupos naturales?" no fija un objetivo: es un problema **no supervisado**. "¿Podemos hallar grupos con alta probabilidad de cancelar al expirar su contrato?" fija un objetivo (¿se irá el cliente?): es **supervisado**. Los términos vienen del machine learning: un profesor "supervisa" al aprendiz aportando la información del objetivo junto con los ejemplos.

Para la minería supervisada debe cumplirse otra condición: tiene que existir *dato* sobre el objetivo, no basta con que exista en principio. Adquirir ese dato suele ser una inversión clave; el valor del objetivo para un individuo se llama su *label*, y etiquetar los datos puede costar dinero.

Clasificación, regresión y causal modeling se resuelven con métodos supervisados. Similarity matching, link prediction y data reduction pueden ser cualquiera de los dos. Clustering, co-occurrence grouping y profiling suelen ser no supervisados. Las dos subclases supervisadas se distinguen por el tipo de objetivo: **regresión** (objetivo numérico) y **clasificación** (objetivo categórico, a menudo binario). Predecir la *probabilidad* de continuar suscrito sigue siendo clasificación (objetivo categórico), lo que se llama "class probability estimation". En etapas tempranas hay que decidir si el ataque será supervisado o no y, si lo es, definir con precisión la variable objetivo.

## Minería de datos y sus resultados

Hay que distinguir entre (1) minar datos para hallar patrones y construir modelos, y (2) usar los resultados de la minería. En el churn, la minería produce un modelo de estimación de probabilidad M a partir de datos históricos (que incluyen el valor del objetivo); el *uso* aplica M a clientes nuevos, cuya clase se desconoce, para generar un puntaje de abandono. Ambos procesos deben mantenerse distintos, aunque el uso debe informar a la minería.

## El proceso de minería de datos (CRISP-DM)

La minería de datos es un oficio (*craft*): mezcla ciencia, tecnología y arte. Una codificación útil del proceso es CRISP-DM (Cross Industry Standard Process for Data Mining; Shearer, 2000). El diagrama hace explícito que la **iteración es la regla, no la excepción**: pasar una vez sin resolver el problema no es un fracaso, sino exploración que informa la siguiente iteración. Sus fases:

- **Business Understanding**: entender el problema a resolver. Los proyectos rara vez vienen empaquetados como problemas claros de minería; recastear el problema es iterativo. Aquí la creatividad del analista es clave: formular el problema de negocio como uno o varios problemas de ciencia de datos. Conviene pensar desde el inicio en el *use scenario* (¿qué queremos hacer y cómo?); enmarcar el problema en términos de *expected value* ayuda a descomponerlo en tareas.
- **Data Understanding**: los datos son la materia prima. Hay que entender sus fortalezas y límites, pues rara vez encajan exactamente con el problema. Los datos históricos suelen haberse recogido con otros fines; sus costes varían (gratis, con esfuerzo, comprados o inexistentes). Hay que estimar costes y beneficios de cada fuente. Ejemplo ilustrativo: el fraude con tarjeta tiene *labels* fiables (cliente y defraudador son personas distintas con metas opuestas), así que es supervisado; el fraude de Medicare no tiene objetivo fiable (los defraudadores son un subconjunto de usuarios legítimos) y exige enfoques no supervisados (profiling, clustering, detección de anomalías). Su similitud superficial es engañosa.
- **Data Preparation**: las tecnologías analíticas imponen requisitos de formato. Tareas típicas: convertir a formato tabular, tratar valores ausentes, convertir tipos, normalizar o escalar valores numéricos. Aquí los analistas invierten mucho tiempo definiendo y construyendo variables: otro punto donde entran creatividad, sentido común y conocimiento del negocio. Advertencia clave: cuidado con las **fugas (leaks)**, variables del histórico que dan información sobre el objetivo pero que no estarían disponibles en el momento de decidir (ej.: "total de páginas visitadas en la sesión", conocido solo al terminar la sesión).
- **Modeling**: fase principal donde se aplican las técnicas de minería; su salida es un modelo o patrón que captura regularidades. Es donde más ciencia y tecnología se aplican.
- **Evaluation**: valorar los resultados con rigor para ganar confianza en que son válidos y fiables *antes* de desplegar. Si se busca lo suficiente, siempre se hallan patrones, pero pueden no resistir escrutinio. Es más barato y seguro probar en laboratorio. Debe asegurar también que el modelo cumple los objetivos de negocio: un modelo con >99% de precisión puede generar demasiadas falsas alarmas y ser inviable. La evaluación es cuantitativa y cualitativa; los *stakeholders* suelen tener que dar el visto bueno, por lo que importa la comprensibilidad del modelo.
- **Deployment**: poner los resultados —y cada vez más las propias técnicas— en uso real para obtener retorno. Ej.: integrar el modelo de churn enviando ofertas a los clientes en riesgo. El despliegue puede ser poco técnico (reglas pegadas al costado de una impresora) o requerir recodificar el modelo para producción. Riesgo de transferencias "over the wall": conviene involucrar pronto al equipo de desarrollo ("tu modelo no es lo que diseñan los científicos de datos, es lo que construyen los ingenieros"). Tras el despliegue (o si Evaluation no es suficiente) el proceso suele volver a Business Understanding; debería haber atajos de retorno desde cada fase.

## Implicaciones para gestionar el equipo de ciencia de datos

Es tentador —pero suele ser un error— ver la minería de datos como un ciclo de desarrollo de software. Es más una empresa exploratoria, cercana a I+D que a la ingeniería: los resultados son inciertos y un paso puede cambiar la comprensión del problema. Comprometerse a ingenierizar una solución para despliegue de forma prematura es caro. Mejor invertir en información para reducir incertidumbre (estudios piloto, prototipos desechables, revisar la literatura, testbeds experimentales). Las habilidades buscadas difieren de las del software: formular bien los problemas, prototipar rápido, hacer supuestos razonables ante problemas mal estructurados, diseñar experimentos que sean buenas inversiones y analizar resultados.

## Otras técnicas y tecnologías analíticas

La diferencia principal es que la minería de datos se centra en la **búsqueda automática** de conocimiento o patrones. Seis grupos relacionados:

- **Statistics**: dos usos. Como "summary statistics" (sumas, promedios, tasas, a veces condicionadas a subpoblaciones), elegidas según el problema y la distribución (el ejemplo del ingreso: media >$60.000 frente a mediana $44.389 en EE. UU., 2004). Como campo de estudio (Statistics), que aporta pruebas de hipótesis e intervalos de confianza. La minería genera hipótesis; la estadística las contrasta (idealmente con datos distintos). El término "correlation" —punto de partida del resto del libro— tiene sentido general y técnico.
- **Database Querying**: una consulta (SQL, QBE/GUI) pide un subconjunto o estadísticas de datos; no descubre patrones. Apropiada cuando el analista ya sospecha una subpoblación interesante (`SELECT * FROM CUSTOMERS WHERE AGE > 45 and SEX='M' and DOMICILE = 'NE'`). La minería, en cambio, podría *descubrir* esa consulta como patrón. OLAP ofrece exploración manual/visual en tiempo real sobre dimensiones preprogramadas, sin modelar ni hallar patrones automáticamente; complementa a la minería.
- **Data Warehousing**: integra y coalesce datos de toda la empresa desde múltiples sistemas transaccionales. Es una tecnología facilitadora: no siempre necesaria, pero quien invierte en ella puede aplicar minería más amplia y profundamente.
- **Regression Analysis**: comparte métodos, pero el libro se interesa menos en *explicar* un conjunto histórico que en extraer patrones que *generalicen* a datos nuevos para mejorar un proceso de negocio (predecir, probar patrones en datos nuevos, reducir el sobreajuste). El debate modelado explicativo vs. predictivo excede su foco.
- **Machine Learning y Data Mining**: los métodos para extraer modelos predictivos (machine learning) surgieron a la vez en Machine Learning, Applied Statistics y Pattern Recognition. Data Mining (o KDD) nació como derivación de Machine Learning; siguen muy ligados y comparten técnicas, pero KDD está más orientado a aplicaciones, negocio y al proceso completo de análisis.

**Responder preguntas de negocio**: (1) ¿quiénes son los clientes más rentables? → consulta a BD; (2) ¿hay diferencia real con el cliente medio? → prueba de hipótesis estadística; (3) ¿cómo caracterizarlos? → minería de datos para hallar patrones; (4) ¿será rentable un cliente nuevo y cuánto generará? → minería predictiva (clasificación para el sí/no, regresión para el valor).

## Ideas clave

- La minería de datos es un oficio con un proceso bien definido (CRISP-DM) cuyas seis fases iteran; la iteración es la norma, no un fracaso.
- Existe un puñado de tareas canónicas: clasificación/probabilidad de clase, regresión, similarity matching, clustering, co-occurrence grouping, profiling, link prediction, data reduction y causal modeling.
- La habilidad crítica es descomponer un problema de negocio en subtareas que encajen en tareas conocidas, resolverlas y recomponer las soluciones.
- Supervisado requiere un objetivo definido y datos (*labels*) sobre él; no supervisado no fija objetivo. Clasificación = objetivo categórico; regresión = objetivo numérico.
- Hay que distinguir minar datos (construir el modelo) de usar sus resultados (aplicar el modelo a casos nuevos).
- Cuidado con las fugas (leaks) en la preparación de datos: variables que no estarán disponibles en el momento de decidir.
- Evaluar antes de desplegar, con criterios cuantitativos y cualitativos y pensando en el contexto de negocio (p. ej., coste de falsas alarmas).
- La minería de datos complementa, sin sustituir, a estadística, consultas a BD, data warehousing, análisis de regresión y machine learning; gestionar el proyecto como I+D exploratorio, no como desarrollo de software.
