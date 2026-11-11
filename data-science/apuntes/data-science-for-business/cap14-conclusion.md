# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 14 — Conclusion (Conclusión)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El capítulo cierra el libro insistiendo en que la ciencia de datos es una combinación de *ingeniería analítica* y *exploración y descubrimiento*. El negocio plantea un problema que rara vez coincide con una tarea básica de minería de datos; hay que descomponerlo en subtareas resolubles, probar con las herramientas existentes, minar los datos y evaluar. Omitir la ingeniería hace improbable que los resultados resuelvan el problema; omitir la exploración impide poner la gestión, los incentivos y las inversiones adecuadas para que el proyecto tenga éxito.

La tesis central es que entender y abrazar los conceptos fundamentales de la ciencia de datos vuelve ambas facetas más sistemáticas y más propensas a tener éxito. Esos conceptos son transversales: aparecen una y otra vez bajo estrategias, tareas, algoritmos y procesos distintos, porque muchos métodos son instancias particulares de uno o más principios fundamentales.

Sales sabiendo cómo agrupar los conceptos del libro en tres tipos, cómo aplicarlos a un problema nuevo (datos de dispositivos móviles), por qué la noción del problema cambia durante el proceso, qué cosas los datos no pueden hacer (el humano en el bucle), y las implicaciones de privacidad y ética al minar datos sobre individuos. Termina con un ejemplo de inversión en datos vía cloud labor y un mensaje final para científicos de datos y para stakeholders de negocio.

## Los conceptos fundamentales de la ciencia de datos

Los conceptos abarcan desde imaginar cómo la ciencia de datos mejora decisiones de negocio, hasta aplicar técnicas, hasta desplegar resultados para mejorar la toma de decisiones. Se agrupan a grandes rasgos en tres tipos:

1. Conceptos generales sobre cómo encaja la ciencia de datos en la organización y el panorama competitivo: cómo atraer, estructurar y nutrir equipos; cómo la ciencia de datos da ventaja competitiva y cómo esa ventaja se sostiene; y principios tácticos para hacer buenos proyectos.
2. Formas generales de pensar de manera analítica con los datos, que ayudan a reunir los datos y considerar los métodos apropiados. Incluye el proceso de minería de datos, el conjunto de tareas de alto nivel y principios como:
   - Tratar los datos como un activo y pensar qué inversiones hacer para sacarle el mayor provecho.
   - El marco de *expected value* para estructurar problemas y ver los subproblemas junto con costes, beneficios y restricciones del entorno de negocio.
   - Generalización y overfitting: si miramos demasiado los datos, encontraremos patrones; queremos patrones que generalicen a datos no vistos.
   - Un problema bien estructurado versus la minería exploratoria exigen distintos niveles de esfuerzo en distintas etapas del proceso.
3. Conceptos generales para extraer conocimiento de los datos, que sustentan el enorme abanico de técnicas:
   - Identificar atributos informativos, los que correlacionan o dan información sobre una cantidad desconocida de interés.
   - Ajustar un modelo de función numérica eligiendo un objetivo y hallando parámetros según ese objetivo.
   - Controlar la complejidad para hallar el equilibrio entre generalización y overfitting.
   - Calcular la similitud entre objetos descritos por datos.

Vistos así, los mismos conceptos subyacen a muchas estrategias y algoritmos. El marco de *expected value* descompone problemas en tareas tratables. La *similitud* se usa directamente (hallar clientes parecidos a los mejores), en clasificación y regresión vía vecinos más cercanos, como base del clustering, para hallar documentos relevantes a una consulta y para recomendar (situar clientes y películas en un mismo "espacio de gustos"). El *lift* —cuánto más probable es un patrón que lo esperable por azar— aparece al evaluar targeting de anuncios, al pesar evidencia a favor o en contra de una conclusión y al juzgar si una co-ocurrencia es interesante o mero efecto de la popularidad.

Entender los fundamentos también facilita la comunicación entre stakeholders de negocio y científicos de datos, no solo por el vocabulario compartido sino porque ambos lados comprenden mejor y pueden hacer preguntas que revelen aspectos críticos. Si una empresa dice personalizar noticias con *support vector machines*, conviene no quedarse en "Ah, vale" sino preguntar "¿qué es eso exactamente?" y, sobre todo, "¿qué datos de entrenamiento van a usar?" y si habrá etiquetas fiables; así se distingue algo creíble del uso de "data science" como cortina de humo.

## Aplicar los fundamentos a un problema nuevo: datos de dispositivos móviles

Pensar la ciencia de datos como una colección de conceptos y métodos generales permite abordar problemas nuevos. Con el giro del consumo online hacia dispositivos móviles, aparece un dato con poco aprovechamiento todavía: la *ubicación*. Según los ajustes de privacidad, un dispositivo puede difundir su GPS exacto, o al menos la IP de la red, que suele revelar ubicación. La Figura 14-1 muestra un scatterplot de ubicaciones GPS captadas de dispositivos móviles; curiosamente, sin mapa, dibuja la densidad de población mundial.

El problema de negocio elegido: en el mundo móvil la conducta de un consumidor se fragmenta entre varios dispositivos. Si se identifica un buen prospecto en uno, ¿cómo alcanzarlo en los demás? Una posibilidad es usar la ubicación para acotar qué otros dispositivos podrían ser suyos, apoyándose en la similitud entre objetos (Capítulo 6).

En la fase de comprensión de los datos hay que decidir cómo representar dispositivos y ubicaciones. Aquí encaja la idea de la formulación del problema para *text mining* (Capítulo 10), aunque no haya texto: igual que se trata un documento como una bolsa de palabras ignorando su secuencia, aquí se trata cada dispositivo como un "*bag of locations*" (una estrategia de lo-más-simple-primero).

También se aplica TFIDF: las ubicaciones WiFi muy populares (el Starbucks de la esquina) son poco informativas y reciben un IDF bajo (aquí la "D" es de "Device", no "Document"); una red WiFi de un apartamento, con pocos dispositivos, es muy discriminativa y TFIDF magnifica su importancia; una red de oficina queda en un IDF intermedio. Con un perfil TFIDF de ubicaciones se buscan los dispositivos más similares al identificado como prospecto. Si mi portátil es el prospecto, observado en el WiFi de mi casa y de mi trabajo, mi teléfono y mi tablet resultarán muy similares y quedarán marcados como buenos prospectos para el mismo anuncio. No es una solución definitiva: ilustra cómo un kit conceptual ayuda a pensar un problema nuevo, que luego los científicos de datos desarrollan y evalúan.

## Cambiar cómo pensamos la solución al problema de negocio

Es muy común que, en el subciclo de comprensión del negocio y de los datos, nuestra noción de cuál es el problema cambie para ajustarse a lo que de verdad se puede hacer con los datos. El cambio suele ser sutil, pero importa notarlo: no todos los stakeholders participan en la formulación, y si olvidamos que cambiamos el problema podemos chocar con resistencia por puro malentendido, percibida como terquedad. En el ejemplo móvil, empezamos buscando el *mismo* usuario en distintos dispositivos y acabamos hallando usuarios *muy similares* por su ubicación: la identificación pasó a ser probabilística. Según el marco coste/beneficio (Capítulo 7), para muchas ofertas eso es aceptable, porque los falsos positivos son baratos frente al beneficio de acertar, e incluso los "fallos" (pareja, amigos, colegas con gustos parecidos) pueden ser buenos aciertos.

## Lo que los datos no pueden hacer: el humano en el bucle, revisitado

Hay cosas que hacen bien las máquinas y cosas que hacen bien las personas, y no son las mismas. Los humanos son mucho mejores identificando qué pequeños aspectos del mundo son relevantes para reunir datos de cara a una tarea; las computadoras son mucho mejores cribando grandes volúmenes de datos y cuantificando la relevancia de las variables para predecir un objetivo. La ciencia de datos es la integración juiciosa del conocimiento humano con técnicas computacionales para lograr lo que ninguno conseguiría solo (y hay que desconfiar de cualquier vendedor de herramientas que sugiera lo contrario). El proceso de minería (Capítulo 2) dirige esa combinación: la interacción humana temprana asegura centrar los métodos en las tareas correctas, y la selección de los datos a minar —a menudo ignorada— es clave.

El humano también es crítico en la evaluación: solo las personas pueden decir cuál es el mejor criterio objetivo a optimizar. Como el criterio verdadero suele no poder medirse, hay que elegir el mejor *proxy* y recordar esas decisiones como fuentes de riesgo al desplegar. Y no debemos creer que los datos son verdad objetiva: incorporan creencias, propósitos, sesgos y pragmáticas de quienes diseñaron la recolección.

El mini-caso del fraude telefónico lo ilustra: un componente del modelo indicaba que "llamar desde el cellsite número cero aumenta mucho el riesgo de fraude", validado por holdout. Pero no existía el cellsite cero. Al resolver un fraude, las llamadas fraudulentas se retiraban de la facturación y se guardaban en otra base de datos que no conservaba el campo cellsite, rellenado con ceros. Era una *fuga* (leak) del Capítulo 2, difícil de detectar por el volumen, por estar las llamadas intercaladas por cliente y porque el scrubbing del target hacía que cellsite cero no fuera un predictor perfecto (lo que habría sido una señal de alarma). La moraleja: "qué son los datos" es una interpretación que cambia durante el proceso, y hay que abrazar esa maleabilidad, incluyendo cómo se muestrearon los datos. Finalmente, hay que discernir en qué problemas la ciencia de datos aporta valor: para decisiones estratégicas de altísimo nivel, únicas, el decisor debe apoyarse en su experiencia, conocimiento e intuición (como ilustra la cita de Steve Jobs sobre diseñar por focus groups).

## Privacidad, ética y minería de datos sobre individuos

Minar datos, sobre todo sobre individuos, plantea cuestiones éticas que no deben ignorarse. Las grandes empresas de cara al consumidor recopilan o compran datos detallados y los usan para decidir crédito, límites, ofertas, contenido, recomendaciones, fuga o fraude. La tensión entre privacidad y mejores decisiones es intensa porque parece haber relación directa entre más datos personales y más efectividad: tras endurecerse la protección de privacidad en Europa, la intención de compra declarada cayó un 65% entre expuestos y no expuestos a anuncios, sin cambio fuera de Europa (Goldfarb & Tucker, 2011). Lo mismo con datos de red social para detección de fraude y marketing. El libro no resuelve el problema; incluso definir qué es la privacidad es difícil: Solove la llama "un concepto en desorden" y dedica más de 80 páginas a una taxonomía, y Nissenbaum más de 300 en *Privacy in Context*. Quien sea científico de datos o stakeholder debe preocuparse por la privacidad e invertir tiempo serio en pensarla; hay un apéndice online con conceptos y lecturas.

## ¿Hay más en la ciencia de datos?

El libro escoge los conceptos fundamentales más relevantes, sin cubrirlos todos. Para profundizar, conviene revisar programas de congresos punteros como ACM SIGKDD o IEEE ICDM, con buenos *Industry Tracks*.

## Ejemplo final: del crowd-sourcing al cloud-sourcing

Internet cambió la economía del trabajo: sistemas como Amazon Mechanical Turk y oDesk permiten *cloud labor* y *micro-outsourcing* de muchas tareas pequeñas y bien definidas, relevante porque cambia la economía de invertir en datos. Ejemplo: el modelado supervisado necesita un target preciso y etiquetas; a veces el target está claro pero faltan datos etiquetados. Los anunciantes quieren mantener sus anuncios fuera de páginas objetables (hate speech), pero con miles de millones de páginas es inviable revisarlas a mano. Es candidato a clasificación de texto (Capítulo 10), pero no hay muestra representativa de hate speech. Si el problema es importante (se reportó como un problema de 2.000 millones de dólares), conviene invertir en datos etiquetados. Un becario etiquetaba 250 webs/hora a 15 $/hora; en Mechanical Turk el ritmo subió a 2.500 webs/hora al mismo coste total (Ipeirotis et al., 2010). El problema: lo barato a veces es de baja calidad, y hay mucha investigación sobre mantener la calidad con cloud labor. Hay otras opciones, como pedir a los trabajadores que *busquen* ejemplos positivos o que reten al modelo a equivocarse ("beat the machine").

## Palabras finales

Tras más de dos décadas aplicando ciencia de datos, los autores destacan lo útil que sigue siendo tener a mano los conceptos fundamentales: ante un impasse, volver a "¿cuál es exactamente el problema que intentamos resolver?" aclara el camino, ya sea por el marco de expected value, por cómo se reúnen los datos, por costes y beneficios, por invertir en datos o por si el target está bien definido. Conocer los tipos de tarea evita tratar todo problema como un clavo para el martillo que uno domina. Al stakeholder de negocio: no te dejes deslumbrar por la jerga; estos conceptos más tu conocimiento del negocio y los datos permiten entender el 80% o más de la ciencia de datos, y si no entiendes a un supuesto científico de datos, desconfía. Al científico de datos, el desafío: piensa a fondo por qué tu trabajo es relevante para el negocio y sé capaz de presentarlo como tal.

## Ideas clave

- La ciencia de datos combina ingeniería analítica y exploración; omitir cualquiera reduce la probabilidad de éxito.
- Los conceptos fundamentales se agrupan en tres tipos (organización/competencia, pensar analíticamente, extraer conocimiento) y reaparecen bajo muchas técnicas.
- Similitud y lift son ejemplos de conceptos que instancian múltiples métodos (vecinos, clustering, búsqueda, recomendación, evaluación).
- Un kit conceptual permite abordar problemas nuevos: datos móviles tratados como "bag of locations" con TFIDF para enlazar dispositivos de un mismo usuario.
- La noción del problema cambia durante el proceso (p. ej., de "mismo usuario" a "muy similar"); hay que notarlo y comunicarlo a los stakeholders.
- Humano en el bucle: las personas eligen datos, objetivos y proxies, y validan con conocimiento de dominio; los datos no son verdad objetiva (caso del cellsite cero / leak).
- Privacidad y ética son complejas e ineludibles: más datos personales suelen dar mejores decisiones, lo que crea tensión real.
- El cloud labor (Mechanical Turk) cambia la economía de invertir en datos etiquetados, al coste de vigilar la calidad.
