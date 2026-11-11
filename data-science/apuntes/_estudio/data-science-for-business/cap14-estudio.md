# Conclusion (Conclusión) — Estudio

## Tarjetas de repaso

P: ¿Qué dos facetas combina la ciencia de datos según el capítulo?
R: La ingeniería analítica y la exploración y descubrimiento; omitir cualquiera reduce la probabilidad de éxito.

P: ¿Qué ocurre si se omite la ingeniería analítica y qué si se omite la exploración?
R: Sin ingeniería es improbable que los resultados resuelvan el problema; sin exploración no se ponen la gestión, los incentivos y las inversiones adecuadas para el éxito.

P: ¿Cuáles son los tres tipos de conceptos fundamentales?
R: Conceptos generales de cómo encaja la ciencia de datos en la organización/competencia, formas de pensar analíticamente con los datos, y conceptos para extraer conocimiento de los datos.

P: ¿Qué es el marco de expected value y para qué sirve?
R: Un marco para estructurar problemas y ver los subproblemas junto con costes, beneficios y restricciones del negocio; descompone problemas en tareas tratables.

P: ¿Qué distingue la generalización del overfitting?
R: Si se miran demasiado los datos siempre se hallan patrones; se busca que los patrones generalicen a datos no vistos, controlando la complejidad para equilibrar ambos.

P: ¿Qué es el lift y dónde reaparece?
R: Cuánto más probable es un patrón que lo esperable por azar; aparece al evaluar targeting de anuncios, pesar evidencia y juzgar si una co-ocurrencia es interesante o mero efecto de la popularidad.

P: ¿Cómo se representa un dispositivo en el problema de datos móviles?
R: Como un "bag of locations" (análogo a la bolsa de palabras del text mining, ignorando la secuencia), una estrategia de lo-más-simple-primero.

P: ¿Cómo se aplica TFIDF a las ubicaciones de dispositivos?
R: Ubicaciones muy populares (un Starbucks) reciben IDF bajo por poco informativas; un WiFi de apartamento con pocos dispositivos es muy discriminativo; la "D" es de "Device", no "Document".

P: ¿Por qué cambia la noción del problema durante el proceso en el caso móvil?
R: Se pasa de buscar el mismo usuario en varios dispositivos a hallar usuarios muy similares por ubicación; la identificación se vuelve probabilística.

P: ¿Qué hacen mejor los humanos y qué las computadoras?
R: Los humanos identifican qué aspectos del mundo son relevantes para reunir datos; las computadoras criban grandes volúmenes y cuantifican la relevancia de variables para predecir un objetivo.

P: ¿Qué enseña el caso del "cellsite número cero"?
R: Fue una fuga (leak): al resolver fraudes, las llamadas se movían a otra base sin el campo cellsite, rellenado con ceros; "qué son los datos" es una interpretación maleable durante el proceso.

P: ¿Por qué los datos no son verdad objetiva?
R: Incorporan creencias, propósitos, sesgos y pragmáticas de quienes diseñaron la recolección; hay que recordar los proxies elegidos como fuentes de riesgo al desplegar.

P: ¿Qué tensión central plantean privacidad y minería de datos sobre individuos?
R: Parece haber relación directa entre más datos personales y más efectividad en las decisiones, lo que choca con la protección de la privacidad.

P: ¿Cómo cambia el cloud labor la economía de invertir en datos?
R: Sistemas como Amazon Mechanical Turk y oDesk permiten micro-outsourcing de tareas pequeñas; por ejemplo, etiquetar webs pasó de 250 a 2.500 webs/hora al mismo coste total, a cambio de vigilar la calidad.

## Preguntas de autoevaluación

P: ¿Por qué el capítulo sostiene que abrazar los conceptos fundamentales mejora el éxito de los proyectos?
R: Porque esos conceptos son transversales y reaparecen bajo estrategias, tareas, algoritmos y procesos distintos, ya que muchos métodos son instancias de uno o más principios fundamentales, lo que vuelve ambas facetas (ingeniería y exploración) más sistemáticas. (Sección: Los conceptos fundamentales de la ciencia de datos)

P: ¿De qué maneras concretas se usa la similitud en distintos métodos?
R: Directamente (hallar clientes parecidos a los mejores), en clasificación y regresión vía vecinos más cercanos, como base del clustering, para hallar documentos relevantes a una consulta y para recomendar situando clientes y películas en un mismo espacio de gustos. (Sección: Los conceptos fundamentales de la ciencia de datos)

P: Si una empresa dice personalizar noticias con support vector machines, ¿qué preguntas conviene hacer?
R: No quedarse en "Ah, vale", sino preguntar qué es exactamente, qué datos de entrenamiento usarán y si habrá etiquetas fiables, para distinguir algo creíble del uso de "data science" como cortina de humo. (Sección: Los conceptos fundamentales de la ciencia de datos)

P: ¿Por qué la identificación probabilística de dispositivos puede ser aceptable para muchas ofertas?
R: Según el marco coste/beneficio, los falsos positivos son baratos frente al beneficio de acertar, e incluso los "fallos" (pareja, amigos, colegas con gustos parecidos) pueden ser buenos aciertos. (Sección: Cambiar cómo pensamos la solución al problema de negocio)

P: ¿Por qué importa notar y comunicar que la noción del problema ha cambiado?
R: Porque no todos los stakeholders participan en la formulación, y si se olvida el cambio puede surgir resistencia por puro malentendido, percibida como terquedad. (Sección: Cambiar cómo pensamos la solución al problema de negocio)

P: ¿Qué papel es crítico del humano en la fase de evaluación?
R: Solo las personas pueden decir cuál es el mejor criterio objetivo a optimizar; como el criterio verdadero suele no poder medirse, hay que elegir el mejor proxy y recordar esas decisiones como fuentes de riesgo. (Sección: Lo que los datos no pueden hacer)

P: ¿Qué evidencia da el capítulo sobre la tensión entre privacidad y efectividad?
R: Tras endurecerse la protección de privacidad en Europa, la intención de compra declarada cayó un 65% entre expuestos y no expuestos a anuncios, sin cambio fuera de Europa (Goldfarb & Tucker, 2011). (Sección: Privacidad, ética y minería de datos sobre individuos)

P: ¿Cuál es el mensaje final del libro para el stakeholder de negocio y para el científico de datos?
R: Al stakeholder: que no se deje deslumbrar por la jerga, pues estos conceptos más su conocimiento del negocio permiten entender el 80% o más de la ciencia de datos. Al científico de datos: que piense a fondo por qué su trabajo es relevante para el negocio y sepa presentarlo como tal. (Sección: Palabras finales)

## Puntos a dominar

- Explicar cómo la ciencia de datos integra ingeniería analítica y exploración, y qué se pierde al omitir cada una.
- Clasificar los conceptos fundamentales en los tres tipos y dar ejemplos de principios de cada uno (datos como activo, expected value, generalización/overfitting, atributos informativos, similitud).
- Reconocer cómo similitud y lift instancian múltiples métodos (vecinos, clustering, búsqueda, recomendación, evaluación).
- Aplicar el kit conceptual a un problema nuevo: datos móviles como "bag of locations" con TFIDF para enlazar dispositivos de un mismo usuario.
- Identificar cuándo y por qué la noción del problema cambia durante el proceso y la necesidad de comunicarlo.
- Argumentar el papel del humano en el bucle: selección de datos, objetivos, proxies y validación de dominio; y reconocer fugas como el caso del cellsite cero.
- Discutir la complejidad e ineludibilidad de la privacidad y la ética al minar datos sobre individuos.
- Valorar cómo el cloud labor (Mechanical Turk) altera la economía de invertir en datos etiquetados y el reto de la calidad.
