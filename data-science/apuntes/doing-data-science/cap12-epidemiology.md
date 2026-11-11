# Doing Data Science — Cathy O'Neil & Rachel Schutt (O'Reilly, 2013)
## Capítulo 12 — Epidemiology (Epidemiología)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo lo expone David Madigan, catedrático y director de estadística en Columbia, con más de 100 publicaciones en estadística bayesiana, text mining, métodos de Monte Carlo, farmacovigilancia y modelos gráficos probabilísticos. El hilo conductor es una pregunta incómoda: ¿funcionan de verdad los estudios observacionales de los que depende gran parte de la práctica médica? Madigan cuenta su trayectoria (matemáticas en Trinity College Dublin, seis años en la industria, doctorado, cátedra en la Universidad de Washington, AT&T Labs, una startup y, desde entonces, grandes datos médicos) para situar cómo pasó de la estadística académica clásica al trabajo real con datos.

La tesis central es que los métodos habituales de la epidemiología —sobre todo la estratificación y los ajustes por posibles confusores— no son fiables: según cómo se elijan la base de datos, los confusores o la ventana temporal, un mismo par fármaco-efecto puede salir estadísticamente significativo en direcciones opuestas. Dicho de otro modo, "puedes obtener lo que quieras".

Sales sabiendo por qué la estratificación no resuelve por sí sola el problema de los confusores, cómo Madigan y sus coautores midieron empíricamente el rendimiento de la epidemiología (proyecto OMOP), y qué significa la llamada "curva ROC de 25 millones de dólares": aplicar un único método a todo apenas supera a adivinar al azar (AUC 0,64), aunque especializando el análisis por base de datos y resultado se mejora bastante (AUC 0,92).

## El experimento mental de partida

Madigan plantea: hoy tenemos datos médicos longitudinales y detallados de decenas de millones de pacientes. La mayor base de datos cubre 80 millones de personas, con cada receta, diagnóstico, visita, resultado de laboratorio y procedimiento, todo con marca de tiempo. Pese a ello, la mayoría del diagnóstico y el tratamiento sigue ocurriendo "en el cerebro del médico". ¿Podemos aprovechar estos datos para dar mejor atención, por ejemplo evitando hospitalizaciones? Lo ilustra con un premio de Kaggle, "Improve Healthcare, Win $3,000,000", que retaba a predecir quién iría al hospital el año siguiente (con datos previamente degradados por privacidad).

Madigan subraya que el dataset de 80 millones de personas trae problemas éticos serios: en lugar de ayudar a la gente a estar sana, los modelos podrían usarse para cobrar primas abusivas a los enfermos o directamente excluirlos del seguro. Y remata: esto no es una cuestión de modelado, sino de qué queremos hacer como sociedad con nuestros modelos.

## Estadística académica moderna

Hace 20 años, según Madigan, el estadístico académico demostraba teoremas sin datos a la vista o inventaba un test nuevo y luego buscaba un dataset al que aplicárselo; en ningún caso hacía falta experiencia de dominio. Hoy las mejores revistas de estadística son más profundas en áreas de aplicación, con colaboraciones estrechas con ciencias sociales y aplicadas, y él mismo da ejemplo implicándose con la comunidad médica.

Su crítica apunta al machine learning actual: un campo académico joven que, a su juicio, se parece a la estadística de hace 20 años (inventar un método y probarlo en datasets), un paso atrás en cuanto a implicación con el dominio. Tampoco salva a la estadística: muy pocos estadísticos académicos tienen verdaderas habilidades de hacking —su colega Mark Hansen es una excepción— y opina que no deberían dejar salir de la universidad a un estadístico sin esas destrezas.

## Literatura médica y estudios observacionales

Las revistas médicas están llenas de estudios observacionales cuyos resultados influyen profundamente en lo que recetan los médicos y en lo que deciden los reguladores. Madigan cita el artículo de Jane Green et al. sobre bifosfonatos orales y riesgo de cáncer de esófago, estómago y colon: concluía que el riesgo aumentaba con 10 o más recetas. Salió en portada del New York Times, lo firmaba un grupo sin aparente conflicto de interés y los fármacos los toman millones de personas, pero el resultado bien podría estar equivocado —y de hecho estudios posteriores lo contradijeron. Hay miles de ejemplos así; se gastan miles de millones en estudios médicos de los que dependen vidas, y deberíamos saber de verdad si funcionan.

## La estratificación no resuelve el problema del confusor

La epidemiología intenta ajustar por posibles confusores, apoyándose mucho en la estratificación: partir los casos en subcasos y mirarlos por separado (por ejemplo, ajustar por género mediante una media ponderada). El problema es que estratificar puede empeorar las estimaciones del efecto causal, sobre todo con números pequeños o poblaciones que no son realmente comparables.

El ejemplo del libro (Tabla 12-1) muestra 100 personas en tratamiento y 100 en control con un efecto causal agregado de 0,3 − 0,2 = 0,1 (10%). Al dividir por género (Tablas 12-2 y 12-3), con cifras pequeñas, el efecto estimado pasa a 0,05 en hombres y 0,1125 en mujeres: un titular podría proclamar que el fármaco tiene efectos secundarios "dos veces más fuertes" en mujeres. La moraleja: estratificar no garantiza mejores estimaciones, y conviene tener buena evidencia de que ayuda antes de hacerlo.

## Qué hace la gente con los confusores en la práctica

Pese a estas objeciones, los expertos siguen usando la estratificación como método principal, junto con ajustes basados en modelos como el propensity score matching. Madigan cita un estudio sobre el riesgo de tromboembolismo venoso con ciertos anticonceptivos orales: tras ajustar por duración de uso, concluyó que el riesgo de coágulos era al menos el doble frente a otros anticonceptivos, y tuvo gran repercusión (salió en ABC). Pero ¿por qué esos confusores y no otros, como la aspirina o el comportamiento distinto de los médicos al recetar según el riesgo del paciente? Otro estudio sobre la misma pregunta, ajustando por antecedentes de coágulos, llegó a una conclusión diferente. En los bifosfonatos orales ajustaron por tabaco, alcohol e IMC: ¿cómo se eligen esas variables? Hay cientos de casos donde dos equipos tomaron decisiones radicalmente distintas en estudios paralelos. Madigan y sus coautores pidieron a varios epidemiólogos que diseñaran cinco estudios: hubo poca consistencia, y además las figuras del campo afirman conocer la forma "correcta" de elegir los confusores.

## ¿Hay una forma mejor?

Madigan y sus coautores examinaron 50 estudios, cada uno un par fármaco-resultado (p. ej., antibióticos y sangrado gastrointestinal). Corrieron unos 5.000 análisis por par —cada epistudio imaginable— sobre nueve bases de datos distintas (desde 4 millones hasta 80 millones de pacientes). Para inhibidores de la ECA e inflamación del corazón, una base de datos triplicaba el riesgo y otra lo sextuplicaba; ese es de los mejores casos, porque al menos siempre es mala noticia (consistente en dirección). En 20 de los 50 pares se podía pasar de significativo en una dirección a la contraria según la base de datos elegida: puedes obtener lo que quieras. Y la elección de base de datos casi nunca se discute en los papers publicados.

En una prueba aún más extensa, ante cada decisión la tomaron de las dos formas posibles: qué base de datos, qué confusores y qué ventana temporal (por ejemplo, si cuenta un infarto una semana o un mes después de dejar el tratamiento). Resultado: casi todos los estudios podían salir en cualquier dirección según las elecciones. Con los bifosfonatos orales, un estudio concluyó que causan cáncer de esófago y dos semanas después JAMA publicó lo contrario —usando la misma base de datos.

## Experimento de investigación: OMOP

Para sacar a la luz estas limitaciones, Madigan trabajó como investigador principal en el programa OMOP (Observational Medical Outcomes Partnership). En 2007, ante el auge de las historias clínicas electrónicas (EHR), el Congreso encargó a la FDA un programa de vigilancia de fármacos más agresivo (de ahí el programa Sentinel). La Foundation for the NIH, junto con PhRMA y la FDA, lanzó OMOP, una colaboración público-privada para identificar los métodos más fiables de analizar grandes volúmenes de datos de fuentes heterogéneas.

Madigan y colegas tomaron 10 grandes bases de datos (reclamaciones de aseguradoras y EHR), con registros de 200 millones de personas ("Big Data, salvo que hables con un astrónomo"). Mapearon todo a un modelo de datos común e implementaron todos los métodos usados en estudios observacionales: 14 diseños epidemiológicos adaptados a datos longitudinales, con unas 5.000 "configuraciones". La idea era ver cómo de bien predicen los métodos cosas que ya sabemos. Tomaron 10 clases de fármacos antiguas (inhibidores de la ECA, betabloqueantes, warfarina…) y 10 resultados (fallo renal, hospitalización, sangrado…). Había 9 efectos nocivos conocidos (la warfarina es anticoagulante y claramente causa sangrado) y 44 casos "negativos" conocidos sin daño. El experimento: correr 5.000 análisis en las 10 bases y ver si discriminan entre casos "rojos" y "azules", como un test de filtro de spam. Cada modelo daba un riesgo relativo (RR) y un error. Era una evaluación empírica de cómo funciona la epidemiología, la versión cuantitativa del trabajo de John Ioannidis.

### Por qué no se había hecho antes

Hay conflicto de interés (¿por qué querrían demostrar que sus métodos no funcionan?) y es caro: costó 25 millones de dólares, aunque poco frente al dinero volcado en estos estudios. Compraron los datos, automatizaron los métodos y calcularon en la nube de Amazon; el código es open source.

## La curva ROC de 25 millones de dólares

En la segunda versión se centraron en cuatro resultados y construyeron la "curva ROC de 25.000.000 $". Con un umbral (p. ej., RR > 2 = "efecto malo"), al variarlo de muy bajo a muy alto se barre una curva de sensibilidad frente a tasa de falsos positivos. Existe un umbral (≈1,8) con 30% de falsos positivos y 50% de sensibilidad, inaceptable para la FDA. La bondad se mide con el área bajo la curva (AUC): 1 es ideal, 0,5 equivale a adivinar al azar y menos de 0,5 es un modelo "perverso". El AUC obtenido fue 0,64, y era el mejor de los 5.000 análisis si se usa un único método para todo: apenas mejor que adivinar.

Ningún epidemiólogo haría eso, así que especializaron el análisis por base de datos y resultado, logrando mejores cifras: en la base de datos de Medicare y para lesión renal aguda, el modelo óptimo da un AUC de 0,92 (80% de sensibilidad con 10% de falsos positivos), mediante validación cruzada. Un método ganador, "OS", compara dentro del historial de un mismo paciente (periodos con y sin fármaco), hoy poco usado. En general, los epidemiólogos no creen los resultados del estudio. En http://elmo.omop.org puede consultarse el AUC por base de datos y método (datos de mediados de 2010).

## Experimento mental de cierre

Se corrieron 5.000 análisis distintos: ¿hay una buena forma de combinarlos para hacerlo mejor, con medias ponderadas o métodos de votación entre estrategias? El código es público y podría dar para una buena tesis doctoral.

## Ideas clave

- El ponente es David Madigan; el capítulo cuestiona empíricamente la fiabilidad de los estudios observacionales en epidemiología.
- Hay datos médicos longitudinales de decenas de millones de pacientes, con enorme potencial clínico pero también serios riesgos éticos (primas abusivas, exclusión de enfermos).
- Madigan critica que el machine learning actual recuerda a la estadística de hace 20 años: inventar un método y probarlo en datasets, con poca implicación de dominio.
- La estratificación no resuelve el problema del confusor; con cifras pequeñas puede empeorar las estimaciones del efecto causal (ejemplo agregado 10% que se distorsiona por género).
- Según cómo se elijan base de datos, confusores y ventana temporal, un mismo par fármaco-efecto puede salir significativo en direcciones opuestas: "puedes obtener lo que quieras".
- OMOP evaluó 14 diseños y ~5.000 configuraciones sobre 10 bases (200 millones de personas) para ver si detectan efectos ya conocidos.
- La "curva ROC de 25 millones" da AUC 0,64 con un método único (apenas mejor que el azar), pero 0,92 al especializar por base de datos y resultado.
