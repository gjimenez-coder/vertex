# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 2 — The Data Science Road Map (El mapa de ruta de la ciencia de datos)

> Nota de extracción: el texto proviene de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El capítulo ofrece una visión de alto nivel del proceso de la ciencia de datos mediante un diagrama que el autor llama Data Science Road Map. Sus etapas son: enmarcar el problema (frame the problem), entender los datos, extraer features, modelar y analizar, y finalmente dos salidas posibles —presentar resultados o desplegar código—. La tesis central es que la ciencia de datos no es software lineal: existe un bucle de realimentación estrecho con el mundo real, de modo que "Model and Analyze" vuelve a enmarcar el problema una y otra vez a medida que surgen nuevos hallazgos.

El autor subraya dos rasgos del mapa. Primero, el bucle de iteración, que diferencia la ciencia de datos de la ingeniería de software tradicional: las preguntas se reformulan constantemente, por lo que el código debe mantenerse muy flexible. Segundo, las dos maneras de salir del mapa —no mutuamente excluyentes— según quiénes sean tus clientes: humanos o máquinas. Un amigo del autor, Michael Li (fundador de The Data Incubator), planteó esa metáfora de los dos tipos de clientes.

Si los clientes son humanos, el objetivo es responder un problema de negocio con los datos disponibles y el entregable suele ser una presentación o un informe escrito para la toma de decisiones. Si los clientes son máquinas, el trabajo se mezcla con la ingeniería de software y el entregable es un programa que realiza tareas analíticas y debe funcionar bien en rendimiento y robustez. Sales sabiendo cuáles son las etapas, sus puntos de dolor y por qué el proceso es profundamente iterativo.

## Frame the Problem (Enmarcar el problema)
La diferencia entre ciencia de datos excelente y mediocre no está en las matemáticas ni en la ingeniería, sino en formular las preguntas correctas. Ninguna competencia técnica compensa haber resuelto un problema inútil. Con clientes humanos, los proyectos suelen partir de una pregunta muy abierta; con clientes máquina, el problema de negocio está claro pero hay ambigüedad sobre las restricciones del software (lenguajes, tiempo de ejecución, precisión exigida).

Antes de empezar conviene aclarar qué constituye una solución: una "definition of done" que fije los criterios de proyecto completado y, sobre todo, de éxito. En proyectos grandes esos criterios se recogen en un documento, redactado de forma colaborativa con los stakeholders. En consultoría se llaman statements of work (SOW); en una empresa que crea un producto, project requirements documents (PRD).

El SOW busca que todos coincidan en qué trabajo se hará, cuáles son las prioridades y qué expectativas son realistas; evita invertir esfuerzo en el problema equivocado. También tiene un componente de autodefensa: si resulta imposible resolver el problema con los datos, si estos están corruptos o si el cliente pierde interés, un buen SOW protege frente a reclamaciones. El SOW no fija nada en piedra —hay correcciones de rumbo—, pero orienta todos los esfuerzos hacia la dirección más útil.

## Understand the Data: Basic Questions (Entender los datos: preguntas básicas)
Con acceso a los datos conviene tener una batería de preguntas estándar para arrancar sin caer en la parálisis por análisis y detectar problemas cuanto antes. Algunas preguntas genéricas:

- ¿Qué tamaño tiene el dataset? ¿Es el dataset completo?
- ¿Es suficientemente representativo? (tal vez solo se recogió un subconjunto de usuarios)
- ¿Puede haber outliers graves o ruido extraordinario? (por ejemplo, el 99 % del tráfico de un servidor podría ser un único ataque de denegación de servicio)
- ¿Podría haberse insertado datos artificiales? (frecuente en entornos industriales)
- ¿Hay campos que sean identificadores únicos? ¿Son realmente únicos? ¿Qué significa si no lo son?
- Al unir dos datasets A y B, ¿qué significa que algo de A no case con nada de B?
- Cuando hay entradas en blanco, ¿de dónde vienen? ¿Cómo de comunes son?

Los SOW suelen incluir un apéndice que describe los datos. La pregunta más importante es si los datos pueden resolver el problema de negocio; si no, hay que buscar fuentes adicionales o modificar el plan. El autor confiesa haber descuidado estas preguntas por prisa: en un proyecto con series temporales de motores para hallar indicadores de fallo, descubrió semanas después que a veces la serie terminaba mucho antes del fallo real y otras continuaba tras la "muerte" del motor; los tiempos de fallo estaban en otra tabla que podría haber cotejado al principio.

## Understand the Data: Data Wrangling (Preparación de datos)
El data wrangling consiste en llevar los datos de su formato bruto a uno apto para la analítica convencional, normalmente mediante una tubería de software que los extrae, los limpia o filtra y los deja en un formato regular. Es el área donde el científico de datos necesita habilidades que un estadístico o analista tradicional no tiene: datos en bases especializadas, volúmenes que exigen técnicas de Big Data, trucos de rendimiento y tuberías de preprocesado tan complejas que cuesta mantener el código ordenado.

Los datasets industriales siempre están más enrevesados de lo razonable; la cuestión no es si existen problemas, sino si afectan tu trabajo. La receta del autor para descubrir cómo está roto un dataset:

1) Si el dato bruto es texto, míralo directamente en un editor: formatos de fecha irregulares, capitalizaciones inconsistentes o líneas basura saltarán a la vista.
2) Si hay una herramienta que debería abrir o procesar el dato, comprueba que realmente lo hace (por ejemplo, abrir un CSV en algo que lea data frames: ¿leyó todas las filas?, ¿la columna de fecha se interpretó como datetime?).
3) Haz histogramas y scatterplots: ¿los números son realistas?, ¿hay outliers enormes?
4) Toma preguntas simples cuya respuesta (aproximada) ya conoces, respóndelas con los datos y comprueba si coinciden (por ejemplo, contar clientes por IDs únicos).

## Understand the Data: Exploratory Analysis (Análisis exploratorio)
Con los datos en formato usable, el siguiente paso es el análisis exploratorio: husmear en los datos, visualizarlos de muchas formas, probar transformaciones y ver qué aparece. Es una etapa muy creativa donde conviene dejar correr la curiosidad; se calculan correlaciones y cosas sencillas, pero sin recurrir todavía a clasificadores sofisticados de machine learning. De aquí se obtienen dos cosas: (1) una intuición de cómo se ven visualmente los patrones relevantes, y (2) una lista de hipótesis concretas, a menudo motivadas por un gráfico revelador (una serie temporal con un patrón inconfundible, un scatterplot que relaciona dos variables o un histograma claramente bimodal).

Una idea errónea común y peligrosa es que el científico de datos no necesita visualizaciones. La mayoría de algoritmos no son visuales, pero es muy fácil malinterpretar sus salidas si solo se miran los números: no hay sustituto para el ojo humano a la hora de dar sentido intuitivo a las cosas.

## Extract Features (Extraer features)
Una feature es simplemente un número o categoría extraído de los datos que describe una entidad (por ejemplo, la longitud media de palabra de un documento o la temperatura media de un lugar). Extraer features significa destilar los datasets brutos en una tabla de filas y columnas —"tabular data"—, donde cada fila es una entidad del mundo real y cada columna una pieza de información que la describe. Casi todas las técnicas analíticas, desde el scatterplot hasta las redes neuronales, operan sobre datos tabulares.

Extraer buenas features es lo más importante para que el análisis funcione, más que los clasificadores, las técnicas estadísticas o el código elegante; es especialmente decisivo cuando los datos no traen features listas (páginas web, imágenes). Es también la parte más creativa y la más ligada a la pericia de dominio: una buena feature suele corresponder a un fenómeno real, por lo que conviene trabajar con expertos de dominio. Incluso hay libertad en elegir sobre qué entidades extraer features (¿una fila por persona o por dirección de e-mail?). Además, a veces hay que extraer también la cosa que se quiere predecir, la target variable (variable objetivo), que puede no existir como campo: el autor tuvo que inventar una forma de medir la "lealtad" de clientes a partir de registros de interacciones.

## Model (Modelar)
Tras extraer las features, la mayoría de proyectos usa algún modelo de machine learning: un clasificador, un modelo de regresión o un algoritmo de clustering. A menudo el modelado es simple —probar una batería estándar de modelos y ver cuál funciona mejor—; otras veces se afina con cuidado para exprimir el máximo rendimiento. Analizar los resultados es crucial: ¿a qué corresponden los clústeres?, ¿el clasificador es lo bastante bueno?, ¿hay algo interesante en los casos de fallo? Esta etapa permite correcciones de rumbo. Con clientes humanos se suelen usar varios modelos ajustados de formas distintas; con clientes máquina, hay que converger en un único modelo canónico para producción.

## Present Results (Presentar resultados)
Con clientes humanos, el entregable suele ser un slide deck o un informe escrito que describe el trabajo y los resultados; a menudo hay que hacerlo incluso cuando los clientes principales son máquinas. Comunicar en diapositivas y prosa es una habilidad difícil e importante, especialmente en ciencia de datos, donde el material es muy técnico y la audiencia amplia. El científico de datos debe comunicarse con stakeholders de negocio, expertos de dominio, ingenieros de software y analistas, grupos con bases de conocimiento, focos de atención y estilos de presentación distintos.

## Deploy Code (Desplegar código)
Si los clientes finales son máquinas, el trabajo es producir código que otros ejecutarán con regularidad. Suele caer en dos categorías: (1) código de analítica por lotes (batch), que repite un análisis sobre datos futuros y a veces produce informes o entrena un modelo referenciado por otro código; y (2) código en tiempo real, un módulo analítico dentro de un paquete mayor, en un lenguaje de alto rendimiento y con las mejores prácticas de ingeniería. Hay tres entregables típicos: el propio código; documentación de cómo ejecutarlo (a veces un "run book", a veces embebida en el código); y una forma de probarlo que garantice que opera bien —normalmente unit tests para el tiempo real y, para los procesos batch, un dataset de ejemplo con casos límite junto a la salida esperada—. Al desplegar, el científico de datos asume con frecuencia un rol pleno de ingeniero de software, porque con algoritmos intrincados no suele ser práctico que una persona lo especifique y otra lo reimplemente.

## Iterating (Iterar)
La ciencia de datos es más iterativa que la ingeniería de software: en software se suele saber qué se quiere construir, pero aquí es una pregunta abierta qué features resultarán útiles y qué modelo se entrenará. Por eso el proceso debe diseñarse para poder cambiar las cosas sin dolor. Recomendaciones del autor: obtener resultados preliminares cuanto antes (un scatterplot, un histograma o un modelo crudo que ya revele patrón o la ausencia de señal, para saber pronto si el análisis está condenado al fracaso); automatizar todo el análisis en un único script ejecutable con un solo comando, para mantener la reproducibilidad desde el principio y no perder la cuenta del procesado realizado; y mantener el código modular y dividido en etapas claras para modificar, añadir o quitar pasos con facilidad. Gran parte de esto es cuestión de software, no de analítica: el código debe ser flexible, potente y comprensible, lo que exige lenguajes de programación flexibles y potentes (tema del siguiente capítulo).

## Ideas clave
- El Data Science Road Map encadena: enmarcar el problema, entender los datos (preguntas básicas, data wrangling, análisis exploratorio), extraer features, modelar, y salir presentando resultados o desplegando código.
- El rasgo distintivo frente a la ingeniería de software es el bucle de realimentación: "Model and Analyze" vuelve a enmarcar el problema, y el proceso es profundamente iterativo.
- Hay dos tipos de clientes —humanos (informe o presentación) y máquinas (software en producción)— que modifican cada etapa.
- Enmarcar bien el problema (SOW o PRD, "definition of done") importa más que la destreza técnica; resolver un problema inútil no tiene arreglo.
- Antes de analizar, haz siempre preguntas básicas sobre tamaño, representatividad, outliers, identificadores y blancos; verifica que los datos pueden resolver el problema.
- El data wrangling exige habilidades propias del científico de datos; los datos industriales siempre son más enrevesados de lo esperado.
- Extraer buenas features —destilar los datos a formato tabular— es lo más decisivo del análisis y lo más ligado al dominio; a veces hay que construir la target variable.
- Las visualizaciones son imprescindibles: mirar solo los números lleva a malinterpretar los resultados.
