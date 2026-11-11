# Data Science for Business — Foster Provost & Tom Fawcett (O'Reilly, 2013)
## Capítulo 1 — Introduction: Data-Analytic Thinking (Introducción: el pensamiento analítico de datos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Los últimos quince años de inversión en infraestructura han hecho que casi toda actividad de negocio quede instrumentada para recolectar datos (operaciones, manufactura, cadena de suministro, comportamiento del cliente, marketing). Esa abundancia, unida a computadoras más potentes, redes ubicuas y algoritmos nuevos, dio origen a la aplicación generalizada de los principios de la data science y de las técnicas de data mining.

La tesis central es que bajo las numerosas técnicas de minería de datos existe un conjunto mucho menor de conceptos fundamentales —la data science—, y que aprender a aplicarlos a problemas de negocio es "pensar analíticamente con datos" (data-analytic thinking). Data science es el conjunto de principios que guían la extracción de conocimiento a partir de datos; data mining es esa extracción mediante tecnologías que encarnan tales principios. Los autores priorizan los principios sobre las técnicas concretas.

Sales sabiendo por qué conviene entender data science aunque no la practiques: para evaluar sistemáticamente propuestas de proyectos de minería de datos, detectar fallos evidentes, supuestos irreales y piezas que faltan, y reconocer oportunidades o amenazas competitivas basadas en datos. El objetivo del libro es dar estructura y principios que, con intuición, creatividad, sentido común y conocimiento del dominio, permitan abordar estos problemas de forma sistemática.

## El ejemplo que recorre el capítulo

El hilo conductor del libro es el problema de churn (fuga de clientes). Asumes un puesto analítico en MegaTelCo, una de las mayores telcos de EE. UU. En la región del Atlántico medio, el 20% de los clientes de móvil se va al expirar su contrato, y captar nuevos es cada vez más caro en un mercado saturado. El churn es costoso para todos: una empresa gasta en incentivos para atraer a un cliente mientras la otra pierde ingresos cuando se marcha.

Como retener sale mucho más barato que captar, marketing ya diseñó una oferta especial de retención. Tu tarea es idear un plan preciso, paso a paso, de cómo el equipo de data science debe usar los vastos datos de MegaTelCo para decidir qué clientes deben recibir la oferta antes de que expire su contrato, de modo que se reduzca al máximo el churn con un presupuesto de incentivos dado. El libro vuelve una y otra vez a este caso, añadiendo sofisticación a medida que se desarrollan los conceptos.

## Dos casos de extracción de patrones predictivos

El caso del huracán Frances (New York Times, 2004) ilustra el valor de descubrir patrones no obvios. Ante la llegada del huracán a Florida, Wal-Mart analizó datos de situaciones previas similares (el huracán Charley) para anticipar demanda inusual y abastecer las tiendas. No bastaba con lo obvio (más agua embotellada): la minería reveló que las Pop-Tarts de fresa se vendían hasta siete veces más antes de un huracán y que el artículo más vendido era la cerveza. Conocer esos patrones permite enviar stock a las tiendas antes de que el huracán toque tierra.

## Data science, ingeniería y toma de decisiones basada en datos

La data science involucra principios, procesos y técnicas para entender fenómenos mediante el análisis (automatizado) de datos, con la meta última de mejorar la toma de decisiones. La toma de decisiones basada en datos (data-driven decision-making, DDD) consiste en basar las decisiones en el análisis de datos y no solo en la intuición; no es todo o nada, y las empresas la practican en distinto grado.

Sus beneficios están demostrados: el estudio de Brynjolfsson, Hitt y Kim (2011) muestra que, a mayor orientación a datos, más productividad, incluso controlando factores de confusión; una desviación estándar más alta en la escala DDD se asocia con un 4%–6% más de productividad, y con mayor rentabilidad y valor de mercado, en una relación que parece causal.

Las decisiones de interés son de dos tipos: (1) aquellas en las que hay que hacer "descubrimientos" dentro de los datos (Wal-Mart con Frances; Target prediciendo embarazos para adelantarse a la competencia), y (2) decisiones repetitivas a gran escala, donde pequeñas mejoras de precisión rinden grandes beneficios (el churn de MegaTelCo, con cientos de millones de clientes). Un modelo predictivo abstrae la complejidad del mundo y se centra en un conjunto de indicadores que correlacionan con la magnitud de interés (quién se irá, quién comprará, quién está embarazada). Cada vez más, estas decisiones las toman automáticamente los sistemas; finanzas y telecomunicaciones fueron pioneras (crédito al consumo, control de fraude en los años 90), y hoy destacan los ejemplos de Harrah's, Amazon y Netflix y la revolución de la publicidad online.

## Procesamiento de datos y "big data"

No todo el procesamiento de datos es data science. La ingeniería y el procesamiento de datos son críticos para sostenerla, pero son más generales y sirven para tareas que no implican extraer conocimiento (procesamiento transaccional eficiente, sistemas web, gestión de campañas). Las tecnologías de "big data" (Hadoop, HBase, MongoDB) procesan conjuntos de datos demasiado grandes para los sistemas tradicionales; a veces implementan técnicas de minería, pero mucho más a menudo dan soporte de procesamiento a las actividades de data science. El estudio de Tambe (2012) halla que una desviación estándar más alta en el uso de big data se asocia con un 1%–3% más de productividad frente a la empresa media.

### De Big Data 1.0 a Big Data 2.0

Por analogía con la adopción de Internet: en Web 1.0 las empresas montaron las tecnologías básicas para tener presencia web y mejorar la eficiencia; estamos en la era de Big Data 1.0, construyendo capacidades para procesar grandes datos en apoyo de las operaciones actuales. Igual que Web 2.0 aprovechó la interactividad y la "voz" del consumidor, un Big Data 2.0 preguntará qué se puede hacer ahora que antes no se podía: será la era dorada de la data science. Amazon (recomendaciones a partir de datos masivos) y la publicidad online (miles de millones de impresiones diarias, pujas en tiempo real en decenas de milisegundos) ya se adelantan.

## Los datos y la capacidad analítica como activo estratégico

Un principio fundamental: los datos y la capacidad de extraer conocimiento de ellos deben tratarse como activos estratégicos clave. Verlos así obliga a pensar cuánto invertir, y revela que son complementarios: el mejor equipo de data science aporta poco sin los datos adecuados, y los datos no mejoran decisiones sin talento analítico que los explote.

El caso de Signet Bank (años 90) lo ejemplifica. Fairbanks y Morris vieron que la TI permitía un modelado predictivo lo bastante sofisticado como para ofrecer términos diferenciados (precios, límites de crédito, cash back, puntos). Signet quería modelar la rentabilidad —no solo la probabilidad de impago—, sabiendo que una pequeña proporción de clientes aporta más del 100% del beneficio de las tarjetas. El problema: no tenía los datos adecuados, porque solo disponía de información sobre los términos ya ofrecidos y los clientes ya aprobados. Aplicaron otra estrategia fundamental: adquirir los datos a un costo, ofreciendo términos al azar a distintos clientes. Las cuentas malas se dispararon (del 2,9% al casi 6% de charge-offs), pero la empresa trató esas pérdidas como inversión en datos y persistió. La operación acabó escindiéndose como Capital One, que en 2000 realizaba 45.000 "tests científicos".

La idea no se limita a la banca. Amazon generó datos tempranos que crean costos de cambio; Harrah's pasó de actor pequeño a la mayor empresa de casinos; y la valoración de Facebook se atribuye a sus activos de datos únicos, incluida la estructura de la red social, útil para predecir quién comprará ciertos productos (Hill, Provost & Volinsky, 2006). El estudio de Martens y Provost (2011) muestra que los datos detallados de transacciones individuales mejoran los modelos muy por encima de los sociodemográficos, y el rendimiento sigue creciendo con más datos: quien tiene mayores activos de datos gana ventaja estratégica.

## El pensamiento analítico de datos

Analizar casos como el churn mejora la capacidad de afrontar problemas "analíticamente con datos". Ante un problema de negocio, hay que evaluar si los datos pueden mejorar el desempeño y cómo, usando conceptos y marcos que estructuren el análisis de forma sistemática. Entender estos fundamentos no solo permite interactuar con competencia con los equipos de datos, sino vislumbrar oportunidades y detectar amenazas competitivas: evaluar la propuesta de un consultor, reconocer una alianza de datos de un rival o juzgar la valoración de una startup basada en sus datos. McKinsey (Manyika, 2011) estimó que para 2018 EE. UU. podría enfrentar un déficit de 140.000 a 190.000 personas con habilidades analíticas profundas y de 1,5 millones de gestores y analistas capaces de usar el análisis de big data para decidir eficazmente.

## Conceptos fundamentales y la ciencia frente al trabajo del data scientist

El libro ilustra cada principio con al menos una técnica que lo encarna. Cuatro conceptos fundamentales introducidos aquí:

- Extraer conocimiento útil puede tratarse sistemáticamente siguiendo un proceso con etapas bien definidas; CRISP-DM (Cross Industry Standard Process for Data Mining) es una codificación de ese proceso.
- A partir de grandes masas de datos, la TI puede hallar atributos descriptivos informativos de las entidades de interés (p. ej., qué atributos de un cliente correlacionan con el churn), incluso descubriéndolos de forma automática.
- Si miras demasiado un conjunto de datos encontrarás algo que quizá no generalice: es el overfitting, cuya detección y evitación es uno de los conceptos más importantes.
- Formular soluciones y evaluar resultados exige pensar en el contexto de uso: qué es "útil" depende de la aplicación (¿debe pesar el valor del cliente además de la probabilidad de fuga?, ¿mejora la decisión frente a una alternativa razonable o frente al azar?).

"La química no trata de tubos de ensayo": conviene separar la data science del trabajo del data scientist. La data science es un campo joven cuyos principios apenas emergen, comparable a la química de mediados del siglo XIX, aún experimental. Igual que todo buen químico debía ser competente en el laboratorio, cuesta imaginar un data scientist que no domine ciertas herramientas de software. Aun así, el libro se centra en la ciencia (los principios perdurables) y no en la tecnología (Hadoop, MapReduce), que cambiará en diez años mientras los principios apenas varían en décadas.

## Ideas clave

- Bajo la gran cantidad de técnicas de data mining subyace un conjunto menor de conceptos fundamentales: la data science.
- Data science = principios que guían la extracción de conocimiento; data mining = esa extracción mediante tecnologías que los encarnan.
- Pensar analíticamente con datos permite evaluar propuestas, detectar fallos y supuestos irreales aunque no se practique la minería.
- La toma de decisiones basada en datos (DDD) mejora de forma demostrable y a veces causal la productividad y el valor de la empresa.
- Las decisiones son de tipo descubrimiento (Wal-Mart, Target) o repetitivas a gran escala (churn de MegaTelCo), donde pequeñas mejoras de precisión rinden mucho.
- Big data da soporte a la data science, pero sus tecnologías no son data science en sí; se vislumbra un salto de Big Data 1.0 a 2.0.
- Los datos y el talento analítico son activos estratégicos complementarios; a veces conviene adquirir datos a un costo (Signet Bank → Capital One).
- Conceptos clave transversales: proceso CRISP-DM, atributos informativos, overfitting y evaluación en el contexto de uso.
