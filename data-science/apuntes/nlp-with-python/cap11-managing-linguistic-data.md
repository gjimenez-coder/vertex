# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 11 — Managing Linguistic Data (Gestión de datos lingüísticos)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Las colecciones estructuradas de datos lingüísticos anotados son esenciales en casi toda área del PLN, pero su uso plantea muchos obstáculos. El capítulo responde a tres preguntas: cómo diseñar un recurso lingüístico cuya cobertura, equilibrio y documentación sirvan a usos variados; cómo convertir datos que llegan en un formato inadecuado; y cómo documentar la existencia de un recurso para que otros lo encuentren.

La tesis central es que, bajo su aparente diversidad e idiosincrasia, todo corpus se reduce a dos tipos de datos fundamentales: textos (con organización temporal) y léxicos (con estructura de registro). A partir de ahí se estudia el ciclo de vida de un corpus (recolección, anotación, control de calidad, publicación y evolución posterior), la adquisición y conversión de datos desde la Web, procesadores de texto, hojas de cálculo y bases de datos, y el trabajo con XML y Toolbox.

Sales sabiendo reconocer las características de un buen diseño de corpus (ejemplificadas con TIMIT), medir la concordancia entre anotadores (coeficiente Kappa, windowdiff), elegir capas de anotación (inline frente a standoff), manipular datos XML con ElementTree, validar léxicos Toolbox con gramáticas, y describir recursos con metadatos OLAC sobre Dublin Core.

## El ejemplo que recorre el capítulo
El corpus **TIMIT** es el hilo conductor del diseño de corpus. Fue la primera base de datos de habla anotada ampliamente distribuida, desarrollada por un consorcio que incluía Texas Instruments y el MIT (de ahí su nombre). Se diseñó para adquirir conocimiento acústico-fonético y para apoyar el desarrollo y evaluación de sistemas de reconocimiento automático del habla.

## Estructura de un corpus: estudio de caso (TIMIT)
Como el Brown Corpus equilibra géneros y fuentes, TIMIT equilibra dialectos, hablantes y materiales. Para cada una de las ocho regiones dialectales, 50 hablantes de ambos sexos, con rango de edades y formación, leyeron 10 frases cuidadosamente elegidas. Dos frases, leídas por todos, se diseñaron para resaltar la variación dialectal; el resto se eligió para ser fonéticamente rico, cubriendo todos los fonos y una amplia gama de difonos (bigramas de fonos). El diseño equilibra que varios hablantes digan la misma frase (comparabilidad) con cubrir un amplio rango de frases (cobertura): cinco frases de cada hablante las leen también otros seis, y tres son únicas de ese hablante.

NLTK incluye una muestra de TIMIT. Cada ítem tiene transcripción fonética accesible con `phones()` y los tokens de palabra con alineación temporal; ambos métodos admiten `offset=True`.

```python
>>> nltk.corpus.timit.phones('dr1-fvmh0/sa1')
['h#', 'sh', 'iy', 'hv', 'ae', ...]
>>> nltk.corpus.timit.word_times('dr1-fvmh0/sa1')
[('she', 7812, 10610), ('had', 10610, 14496), ...]
```

Además del texto, TIMIT incluye un léxico con la pronunciación canónica de cada palabra (`transcription_dict()`) y datos demográficos de los hablantes (`spkrinfo()`), que permiten estudios finos de rasgos vocales, sociales y de género.

TIMIT ilustra rasgos clave del diseño de corpus: (1) dos capas de anotación, fonética y ortográfica —en general un corpus puede anotarse en niveles morfológico, sintáctico o de discurso, con esquemas o versiones múltiples—; (2) equilibrio en varias dimensiones de variación, con datos demográficos que aportan variables independientes para usos no previstos (p. ej. sociolingüística); (3) separación nítida entre el evento lingüístico original (la grabación, artefacto inmutable) y sus anotaciones, por lo que conviene conservar la fuente lo más fiel posible; (4) estructura jerárquica en árbol (4 ficheros por frase, 10 frases por cada 500 hablantes = 20.000 ficheros), con división superior entre conjuntos de entrenamiento y prueba. Aunque es un corpus de habla, sus transcripciones y datos son solo texto y se procesan como cualquier otro corpus.

## Tipos de datos fundamentales
Pese a su complejidad, TIMIT contiene solo dos tipos fundamentales: **léxicos** y **textos**. Un recurso léxico se representa con una estructura de registro (una clave más uno o más campos): diccionario, lista comparativa de palabras, léxico de frases, tesauro (acceso por campos no clave que corresponden a temas) o paradigmas que ilustran contrastes. La tabla de hablantes de TIMIT es también un léxico. Un **texto** es la representación de un evento de habla real o ficticio, cuyo transcurso temporal se traslada al propio texto; puede venir con anotaciones (POS, análisis morfológico, estructura del discurso) y los constituyentes de nivel superior pueden representarse con etiquetas por palabra (técnica IOB del Capítulo 7). Los corpus suelen estar sesgados hacia uno u otro tipo: el Brown tiene 500 ficheros de texto pero usa una tabla para 15 géneros; WordNet tiene 117.659 registros de synset con mini-textos de ejemplo.

## El ciclo de vida de un corpus
Los corpus requieren preparación prolongada: recolectar, limpiar, documentar y almacenar los datos crudos en una estructura sistemática, aplicar capas de anotación (a veces con conocimiento especializado) y disponer de un flujo de trabajo eficiente con herramientas y conversores. Los corpus grandes pueden tardar años y decenas o cientos de personas-año.

Hay tres escenarios de creación. En la **lingüística de campo**, el diseño emerge durante la exploración: el material de sesiones de elicitación se analiza según se recoge (ejemplo: el programa Shoebox, reeditado como Toolbox). En la **investigación experimental**, se recoge material cuidadosamente diseñado de varios sujetos para evaluar una hipótesis o desarrollar una tecnología; estos corpus sostienen el método de "tarea común" habitual en programas de investigación financiados. Por último, los **corpus de referencia** de una lengua (ANC, BNC) buscan un registro exhaustivo, con fuerte dependencia de anotación automática más post-edición.

El **control de calidad** depende tanto de buenas herramientas como de documentación, formación y flujo de trabajo. Las guías de anotación definen la tarea y las convenciones de marcado, se actualizan para casos difíciles, y los anotadores se forman en ellas. Con varios anotadores surge el problema de la consistencia: se mide haciendo que dos personas anoten de forma independiente una parte del material (buena práctica: reportar la concordancia inter-anotadores, p. ej. doble-anotando el 10%), lo que da una cota superior del rendimiento esperable de un sistema automático. El **coeficiente Kappa (κ)** mide la concordancia entre dos codificadores corrigiendo el acuerdo esperado por azar: con cuatro opciones equiprobables, el 25% de acuerdo da κ = 0 y el 50% da κ = 0,333. Cuidado al interpretarlo: 90% de acuerdo sería pésimo para etiquetado POS pero excepcional para etiquetado de roles semánticos. Para comparar segmentaciones (tokenización, segmentación de frases, NER) se usa **windowdiff**, que desliza una ventana y da crédito parcial a los casi aciertos:

```python
>>> s1 = "00000010000000001000000"
>>> s2 = "00000001000000010000000"
>>> nltk.windowdiff(s1, s2, 3)
4
```

### Curación frente a evolución
Tras publicarse, los corpus se reutilizan para fines distintos del original (p. ej. Switchboard, creado para identificación de hablantes, se usó luego en reconocimiento, pronunciación, disfluencias, sintaxis, entonación y discurso). Cada grupo reformatea, renombra, re-tokeniza o enriquece de forma independiente, lo que vuelve muy costoso integrar versiones después. Una opción es la **curación central** por comités que revisan y publican nuevas versiones (diccionarios impresos, corpus nacionales), pero suele ser impracticable. El camino intermedio es la **anotación standoff**: asignar identificadores únicos a cada sub-parte (frase, árbol, entrada) con desplazamientos relativos, de modo que las anotaciones referencien la fuente sin modificarla y puedan distribuirse, compararse y actualizarse por separado. Si un corpus se revisa y no hay correspondencia uno a uno entre identificadores viejos y nuevos, es mejor que las anotaciones standoff "se rompan" a que apunten silenciosamente a lugares incorrectos.

## Adquisición de datos
La **Web** es una fuente rica: lo más simple es usar un corpus web publicado (SIGWAC los lista), documentado y estable para experimentos reproducibles. Para capturar un sitio se usan utilidades como GNU Wget, o rastreadores (crawlers) como Heritrix para mayor control. Escribir un crawler propio tiene decenas de trampas (tipos MIME, URLs relativas a absolutas, ciclos de enlaces, latencias, sobrecargar o ser baneado del sitio).

Los **procesadores de texto** se usan en proyectos con poca infraestructura; no garantizan la estructura de los datos. Si el documento puede guardarse en formato no propietario (texto, HTML, XML), se pueden escribir programas que validen el contenido —por ejemplo, extraer con expresiones regulares todas las partes de la oración marcadas con cierto estilo y compararlas con un conjunto legal para detectar las ilegales— y luego convertirlo (p. ej. HTML de MSWord a CSV con `nltk.clean_html()`).

Las **hojas de cálculo** sirven para listas de palabras o paradigmas y exportan a CSV, leíble con el módulo `csv`. Las **bases de datos relacionales** normalizadas garantizan validez (p. ej. POS como clave foránea), pero exigen declarar el esquema de antemano, lo que choca con el enfoque exploratorio dominante en datos lingüísticos, donde los campos supuestamente obligatorios y únicos resultan opcionales y repetibles. Para extraer contenido basta volcar las tablas a CSV y consultarlas desde Python con consultas lingüísticamente motivadas difíciles de expresar en SQL.

### Conversión de formatos
En el caso más simple, entrada y salida son isomorfas (p. ej. transliterar entradas Toolbox a XML con un bucle `for`). Otras veces la salida es una forma digerida (un índice invertido): se construye la estructura en memoria y luego se escribe. En los casos más espinosos, los formatos origen y destino cubren el dominio de forma distinta y se pierde información inevitablemente (el problema del "round-tripping"); una solución parcial es asociar identificadores explícitos a cada objeto lingüístico y propagarlos.

### Capas de anotación
Van desde un mínimo (secuencia de símbolos sonoros u ortográficos) hasta mucha información sintáctica, morfológica, prosódica, semántica, de discurso o actos de diálogo. Capas habituales: tokenización de palabras, segmentación de frases, segmentación de párrafos, POS, estructura sintáctica, semántica superficial (entidades nombradas, correferencia, roles semánticos) y diálogo/discurso. Hay dos clases de representación: la **anotación inline** modifica el documento original insertando símbolos (p. ej. `"fly"` → `"fly/NN"`); la **anotación standoff** no toca el original y crea un fichero nuevo con punteros (p. ej. `<token id=8 pos='NN'/>`).

### Estándares y herramientas
No existen estándares ampliamente aceptados para expresar estructura y contenido de corpus, y sin ellos no hay herramientas de propósito general (ni al revés). Una respuesta es un formato genérico muy expresivo; el reto es escribir programas que manejen su generalidad (p. ej. validar propiedades de árbol si el formato admite grafos arbitrarios). La propuesta de NLTK es un **interfaz común** (como `nltk.corpus`) en vez de un formato común: un árbol de estructura de frases puede almacenarse de muchas formas, pero su estructura lógica es casi la misma, así que conviene un interfaz con métodos como `children()`, `leaves()`, `depth()`. Esto sigue prácticas aceptadas en informática (tipos abstractos de datos, diseño orientado a objetos, arquitectura de tres capas) y aísla las aplicaciones de los formatos de fichero.

### Lenguas en peligro
De las ~7.000 lenguas humanas, la mayoría afronta la extinción. El PLN aporta aquí sobre todo mejores herramientas para recoger y curar datos (textos y léxicos), no tanto etiquetadores o analizadores. La transcripción es un problema práctico porque muchas lenguas carecen de ortografía estándar; conviene crear el léxico en paralelo al corpus. Ayuda etiquetar los ítems con dominios semánticos y permitir la búsqueda por glosa o por **similitud de pronunciación**: se mapean secuencias de letras confundibles a versiones simples, se calcula una "firma" (signature) de cada palabra y se rankean candidatos por distancia de edición (`edit_dist`).

```python
>>> fuzzy_spell('ebsekwieous')
['obsequious']
```

## Trabajar con XML
XML permite inventar etiquetas propias y crear datos sin especificar antes su estructura, con elementos opcionales y repetibles. Es natural para estructuras lingüísticas (p. ej. una entrada léxica con `<entry>`, `<headword>`, `<pos>`, `<gloss>`, `<sense>`, `<synset>`), y la estructura puede restringirse con un **schema**. Pero la flexibilidad tiene coste: cada complicación da más trabajo a los programas, dificulta validar y consultar, y no resuelve por arte de magia el modelado de datos (sigue habiendo que normalizar, evitar duplicados y modelar dependencias existenciales y relaciones muchos-a-muchos).

El módulo **ElementTree** (estándar desde Python 2.5) accede a datos XML. Con una obra de Shakespeare en XML, se parsea el fichero, se navega por índices (`merchant[0].text`) o se buscan subelementos por nombre con `findall('ACT/SCENE/SPEECH/SPEAKER')`, pudiendo combinar con `FreqDist` o `ConditionalFreqDist` para analizar diálogos. ElementTree también accede a datos **Toolbox** (`toolbox.xml('rotokas.dic')`) por índices o por rutas (`record/lx`), y permite escribir el resultado como XML o generar tablas HTML.

## Trabajar con datos Toolbox
Toolbox es un formato muy popular entre lingüistas. Muchas técnicas previas (conteos, distribuciones de frecuencia, co-ocurrencias) se aplican a sus entradas (p. ej. el número medio de campos por entrada). Dos tareas útiles no soportadas por el propio Toolbox: **añadir un campo** derivado automáticamente —por ejemplo un campo `cv` que mapea cada lexema a su secuencia de consonantes y vocales con `SubElement`, recomendando crear ficheros enriquecidos en vez de reemplazar los ficheros fuente curados a mano—; y **validar un léxico**, ya que muchos léxicos Toolbox no siguen un esquema. Con una `FreqDist` de las secuencias de etiquetas de campo se identifican secuencias frecuentes frente a excepcionales; luego se puede devisar una gramática libre de contexto (`RecursiveDescentParser`) que modele la estructura anidada y marque cada entrada con `+` o `-` según su conformidad, filtrando algunas etiquetas. Un parser de chunks es aún más eficaz para identificar y reportar estructuras parciales.

## Describir recursos con metadatos OLAC
Los metadatos son "datos estructurados sobre datos": información descriptiva de un recurso. La **Dublin Core Metadata Initiative** (desde 1995) define 15 elementos opcionales y repetibles (Title, Creator, Subject, Description, Publisher, Contributor, Date, Type, Format, Identifier, Source, Language, Relation, Coverage, Rights). La **Open Archives Initiative (OAI)** da un marco común para repositorios, cada ítem con identificador único y registro Dublin Core, y define un protocolo para "cosechar" (harvest) los metadatos. La **Open Language Archives Community (OLAC)** es una alianza internacional que crea una biblioteca virtual de recursos lingüísticos: desarrolla consenso sobre buenas prácticas de archivado digital y una red de repositorios interoperables. OLAC Metadata extiende Dublin Core con descriptores propios de recursos lingüísticos (lengua del tema, tipo lingüístico), limitando ciertos valores a vocabularios controlados. Los archivos publican sus catálogos en XML, cosechados vía OAI. Los identificadores OAI tienen la forma `oai:archive:local_id` (p. ej. `oai:www.ldc.upenn.edu:LDC97L18`), y el registro XML completo se recupera con una URL del tipo `http://www.language-archives.org/static-records/oai:archive:local_id`.

## Ideas clave
- Todo corpus se reduce a dos tipos de datos fundamentales: **textos** (estructura temporal) y **léxicos** (estructura de registro); incluso los datos de hablantes de TIMIT son un léxico.
- Un buen diseño de corpus equilibra varias dimensiones de variación, separa el evento original (inmutable) de sus anotaciones, y organiza los datos jerárquicamente; TIMIT es el caso modelo.
- El ciclo de vida abarca recolección, anotación, control de calidad y publicación, y continúa evolucionando con la reutilización por distintos grupos.
- La concordancia inter-anotadores se mide con el coeficiente **Kappa** (corrige el azar) y las segmentaciones con **windowdiff**; conviene reportarla como cota superior del rendimiento automático.
- Los datos se adquieren de la Web, procesadores de texto, hojas de cálculo y bases de datos, y suele hacer falta convertir formatos, a veces con pérdida ("round-tripping").
- La anotación puede ser **inline** (modifica el original) o **standoff** (ficheros aparte con punteros e identificadores), siendo esta última clave para la curación distribuida.
- NLTK promueve un **interfaz común** (no un formato común) para aislar las aplicaciones de la idiosincrasia de los formatos.
- **XML** aporta un formato flexible pero no resuelve el modelado de datos; **ElementTree** permite acceder a XML y Toolbox, y **OLAC** (sobre Dublin Core y OAI) permite documentar y descubrir recursos lingüísticos.
