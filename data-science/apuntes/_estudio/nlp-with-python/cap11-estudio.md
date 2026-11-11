# Capítulo 11 — Managing Linguistic Data (Gestión de datos lingüísticos) — Estudio

## Tarjetas de repaso

P: ¿A qué dos tipos de datos fundamentales se reduce todo corpus? / R: A textos (con organización temporal) y léxicos (con estructura de registro).

P: ¿Qué es el corpus TIMIT y para qué se diseñó? / R: La primera base de datos de habla anotada ampliamente distribuida, hecha por un consorcio con Texas Instruments y el MIT, para adquirir conocimiento acústico-fonético y apoyar el desarrollo y evaluación de sistemas de reconocimiento automático del habla.

P: ¿Qué equilibra el diseño de TIMIT? / R: Dialectos, hablantes y materiales: ocho regiones dialectales, 50 hablantes de ambos sexos por región, con frases que resaltan variación dialectal y frases fonéticamente ricas que cubren todos los fonos y una amplia gama de difonos.

P: ¿Cómo se representa un recurso léxico? / R: Con una estructura de registro: una clave más uno o más campos (diccionarios, listas comparativas, tesauros, paradigmas); la tabla de hablantes de TIMIT es también un léxico.

P: ¿Qué es un texto en este marco? / R: La representación de un evento de habla real o ficticio cuyo transcurso temporal se traslada al propio texto, que puede venir con anotaciones (POS, morfología, estructura del discurso).

P: ¿Cuáles son las fases del ciclo de vida de un corpus? / R: Recolección, anotación, control de calidad y publicación, con evolución posterior por la reutilización de distintos grupos.

P: ¿Qué mide el coeficiente Kappa (κ)? / R: La concordancia entre dos codificadores corrigiendo el acuerdo esperado por azar; con cuatro opciones equiprobables, 25% de acuerdo da κ = 0 y 50% da κ = 0,333.

P: ¿Para qué sirve windowdiff? / R: Para comparar segmentaciones (tokenización, segmentación de frases, NER) deslizando una ventana y dando crédito parcial a los casi aciertos.

P: ¿Qué diferencia hay entre anotación inline y standoff? / R: La inline modifica el documento original insertando símbolos (p. ej. "fly" → "fly/NN"); la standoff no toca el original y crea un fichero nuevo con punteros e identificadores (p. ej. <token id=8 pos='NN'/>).

P: ¿Por qué es clave la anotación standoff para la curación distribuida? / R: Porque usa identificadores únicos y desplazamientos para referenciar la fuente sin modificarla, permitiendo distribuir, comparar y actualizar anotaciones por separado; si no hay correspondencia, es mejor que se "rompan" a que apunten en silencio a lugares incorrectos.

P: ¿Qué es el problema del "round-tripping" en la conversión de formatos? / R: Cuando los formatos origen y destino cubren el dominio de forma distinta y se pierde información inevitablemente; una solución parcial es asociar identificadores explícitos a cada objeto lingüístico y propagarlos.

P: ¿Qué propone NLTK en lugar de un formato común? / R: Un interfaz común (como nltk.corpus) con métodos como children(), leaves() y depth(), para aislar las aplicaciones de la idiosincrasia de los formatos de fichero.

P: ¿Qué aporta XML y qué no resuelve? / R: Aporta un formato flexible con etiquetas propias y elementos opcionales/repetibles, pero no resuelve el modelado de datos (sigue habiendo que normalizar, evitar duplicados y modelar dependencias y relaciones muchos-a-muchos).

P: ¿Qué es Dublin Core y qué define? / R: La Dublin Core Metadata Initiative (desde 1995), que define 15 elementos de metadatos opcionales y repetibles (Title, Creator, Subject, Description, etc.).

P: ¿Qué es OLAC? / R: La Open Language Archives Community, una alianza internacional que crea una biblioteca virtual de recursos lingüísticos y extiende Dublin Core con descriptores propios, con catálogos en XML cosechados vía OAI.

## Preguntas de autoevaluación

P: ¿Qué rasgos clave del diseño de corpus ilustra TIMIT? / R: Dos capas de anotación (fonética y ortográfica), equilibrio en varias dimensiones de variación con datos demográficos como variables independientes, separación nítida entre el evento original inmutable y sus anotaciones, y estructura jerárquica en árbol con división entre entrenamiento y prueba. (Sección "Estructura de un corpus: estudio de caso (TIMIT)")

P: ¿Cómo se controla la calidad cuando hay varios anotadores? / R: Con guías de anotación, formación y flujo de trabajo, y midiendo la consistencia: dos personas anotan de forma independiente parte del material (buena práctica: doble-anotar el 10%), lo que da una cota superior del rendimiento esperable de un sistema automático. (Sección "El ciclo de vida de un corpus")

P: ¿Por qué un 90% de acuerdo no se interpreta igual en todas las tareas? / R: Porque el significado de κ depende de la tarea: 90% de acuerdo sería pésimo para etiquetado POS pero excepcional para etiquetado de roles semánticos. (Sección "El ciclo de vida de un corpus")

P: ¿Cuáles son los tres escenarios de creación de corpus? / R: La lingüística de campo (el diseño emerge durante la exploración, p. ej. Toolbox), la investigación experimental (material diseñado de varios sujetos para evaluar una hipótesis o desarrollar tecnología) y los corpus de referencia de una lengua (ANC, BNC), que buscan un registro exhaustivo con anotación automática más post-edición. (Sección "El ciclo de vida de un corpus")

P: ¿Qué problema plantean las bases de datos relacionales para datos lingüísticos? / R: Que exigen declarar el esquema de antemano, lo que choca con el enfoque exploratorio dominante, donde campos supuestamente obligatorios y únicos resultan opcionales y repetibles. (Sección "Adquisición de datos")

P: ¿Qué dos tareas útiles sobre léxicos Toolbox no soporta el propio Toolbox y cómo se abordan? / R: Añadir un campo derivado automáticamente (p. ej. un campo cv con SubElement, creando ficheros enriquecidos en vez de reemplazar los fuente) y validar un léxico usando una FreqDist de secuencias de etiquetas y una gramática libre de contexto (RecursiveDescentParser) o un parser de chunks que marque cada entrada según su conformidad. (Sección "Trabajar con datos Toolbox")

P: ¿Qué forma tienen los identificadores OAI y cómo se recupera el registro completo? / R: Tienen la forma oai:archive:local_id (p. ej. oai:www.ldc.upenn.edu:LDC97L18), y el registro XML completo se recupera con una URL del tipo http://www.language-archives.org/static-records/oai:archive:local_id. (Sección "Describir recursos con metadatos OLAC")

P: ¿Qué papel juega el PLN frente a las lenguas en peligro? / R: Aporta sobre todo mejores herramientas para recoger y curar datos (textos y léxicos), más que etiquetadores o analizadores; conviene crear el léxico en paralelo al corpus y permitir la búsqueda por glosa o por similitud de pronunciación. (Sección "Lenguas en peligro")

## Puntos a dominar

- Reconocer que todo corpus se reduce a textos (estructura temporal) y léxicos (estructura de registro), incluso la tabla de hablantes de TIMIT.
- Explicar los rasgos de un buen diseño de corpus usando TIMIT: equilibrio de variación, separación evento/anotaciones y estructura jerárquica.
- Describir el ciclo de vida de un corpus y los tres escenarios de creación (campo, experimental, referencia).
- Interpretar correctamente el coeficiente Kappa (corrige el azar) y saber cuándo usar windowdiff para segmentaciones.
- Distinguir anotación inline frente a standoff y justificar por qué standoff favorece la curación distribuida.
- Identificar las fuentes de adquisición de datos (Web, procesadores de texto, hojas de cálculo, bases de datos) y el problema de conversión con pérdida ("round-tripping").
- Entender la propuesta de interfaz común de NLTK frente a un formato común.
- Describir el papel de XML y ElementTree para acceder a datos XML y Toolbox, y sus límites en el modelado de datos.
- Situar OLAC sobre Dublin Core y OAI como medio para documentar y descubrir recursos lingüísticos.
