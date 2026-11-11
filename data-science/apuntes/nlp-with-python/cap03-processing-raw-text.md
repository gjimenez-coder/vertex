# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 3 — Processing Raw Text (Procesamiento de texto en bruto)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Se omiten la mayoría de las sesiones interactivas y se conservan solo las esenciales.

## Lo que necesitas saber

El capítulo enseña a trabajar con texto propio en lugar de depender de corpus preparados. Responde a tres preguntas: cómo acceder a texto desde archivos locales y la Web, cómo partir documentos en palabras y signos de puntuación (tokenización) para analizarlos como un corpus, y cómo producir salida formateada y guardarla en un archivo. En el recorrido se consolidan conceptos de Python (cadenas, archivos, expresiones regulares) y de NLP (tokenización, stemming, lematización).

La tesis central es que el "texto plano" es una ficción: todo texto real llega con ruido (encabezados, marcado HTML, codificaciones diversas) y hay que procesarlo por capas. El flujo típico (pipeline) es: abrir una URL o archivo, eliminar marcado, recortar la porción útil, tokenizar, opcionalmente convertir a objeto `nltk.Text`, normalizar a minúsculas y extraer el vocabulario.

A partir de este capítulo los ejemplos asumen que la sesión empieza con `from __future__ import division` e `import nltk, re, pprint`. Al terminar sabrás manejar cadenas y codificaciones Unicode, escribir expresiones regulares para detectar patrones y tokenizar, normalizar texto con stemmers y lematizadores, abordar la segmentación de oraciones y palabras, y formatear resultados para pantalla o archivo.

## 3.1 Acceso a texto desde la Web y el disco

La Web es la fuente de textos más importante. Project Gutenberg ofrece 25.000 libros libres; se puede obtener la URL de un archivo ASCII y leerlo con `urllib`:

```python
from urllib import urlopen
url = "http://www.gutenberg.org/files/2554/2554.txt"
raw = urlopen(url).read()
```

`raw` es una cadena (`str`) con todo el contenido crudo, incluyendo espacios, saltos de línea y caracteres `\r\n`. Para analizarlo se tokeniza con `nltk.word_tokenize(raw)`, que devuelve una lista de palabras y puntuación, y se puede crear un `nltk.Text` para aplicar operaciones lingüísticas (`collocations`, `concordance`) y de listas (slicing). NLTK solo hace falta para la tokenización, no para abrir y leer la URL.

Los textos de Gutenberg traen cabecera y pie (nombre, autor, licencia), por eso "Project Gutenberg" aparece como colocación. No hay forma fiable de detectar dónde empieza y termina el contenido, así que se inspecciona manualmente y se recorta con `find()` y `rfind()` (índice de la primera y última aparición de una cadena) para quedarnos solo con el texto útil. Primera lección: el texto de la Web contiene material no deseado y a veces hay que quitarlo a mano.

Para HTML, `nltk.clean_html(html)` devuelve texto sin marcado, que luego se tokeniza; aun así queda material de navegación que se recorta por índices. Para procesamiento más sofisticado se sugiere Beautiful Soup. Los buscadores web actúan como un corpus enorme no anotado: su ventaja es el tamaño y la facilidad de uso para comprobar hipótesis rápidamente (ej. Tabla 3-1 con hits de Google para colocaciones). Sus límites: patrones de búsqueda muy restringidos, resultados inconsistentes según momento o región, y marcado que cambia impredeciblemente.

Los feeds RSS (blogosfera) se procesan con la librería Universal Feed Parser (`feedparser`): se parsea el feed, se accede a las entradas y su contenido, y se limpia con `clean_html`. Las cadenas resultantes llevan prefijo `u` por ser Unicode. Para leer un archivo local se usa `open()` seguido de `read()`; conviene abrir con el modo `'rU'` ('r' lectura, 'U' "Universal") para ignorar las distintas convenciones de salto de línea entre sistemas operativos. También se puede iterar línea a línea con un `for`, usando `strip()` para quitar el `\n` final. Los archivos de corpus de NLTK se localizan con `nltk.data.find()` y se abren igual.

Formatos binarios como PDF o MSWord requieren librerías de terceros (pypdf, pywin32); para pocos documentos es más simple abrirlos con la aplicación adecuada y guardarlos como texto. Para capturar lo que teclea el usuario se usa `raw_input()`. La Figura 3-1 resume el pipeline de procesamiento. Es clave entender el tipo de cada variable: al leer una URL o archivo obtenemos `str`; al tokenizar obtenemos `list`; normalizar y ordenar listas produce otras listas. El tipo determina las operaciones válidas: a una lista se le puede hacer `append`, a una cadena no; se pueden concatenar cadenas con cadenas y listas con listas, pero no mezclarlas.

## 3.2 Cadenas: procesamiento de texto en el nivel más bajo

Una cadena (string) es el tipo de dato fundamental que representa palabras y contenidos de archivos. Se especifican con comillas simples o dobles; si la cadena contiene una comilla simple hay que escaparla con barra invertida o usar comillas dobles. Para cadenas en varias líneas se usa barra invertida, paréntesis o triple comilla (esta última sí conserva el salto de línea).

Operaciones básicas: concatenación con `+` (no inserta espacios) y repetición con `*`. No se admiten resta ni división sobre cadenas (producen `TypeError`, otro aviso de tipos mezclados). El `print` muestra la forma más legible (sin comillas); escribir el nombre de la variable muestra la representación de Python (con comillas).

Las cadenas se indexan desde cero; un carácter es una cadena de longitud 1. Los índices negativos cuentan desde el final (`-1` es el último). Acceder fuera de rango da `IndexError`. Se puede iterar con un `for` sobre los caracteres y contar frecuencias de letras con `nltk.FreqDist` (útil para identificar el idioma de un texto por sus frecuencias relativas). Las subcadenas se obtienen con slice `[m:n]`, que incluye desde `m` hasta `n-1`; si se omite el primer valor empieza al inicio, si se omite el segundo llega al final. El operador `in` comprueba si una subcadena está presente y `find()` da su posición.

Tabla 3-2 (métodos útiles de cadenas, todos producen una nueva cadena o lista):

| Método | Función |
|---|---|
| `s.find(t)` / `s.rfind(t)` | Índice de la primera / última aparición de `t` en `s` (−1 si no está) |
| `s.index(t)` / `s.rindex(t)` | Como `find`/`rfind` pero lanzan `ValueError` si no está |
| `s.join(text)` | Une las palabras de `text` usando `s` como pegamento |
| `s.split(t)` | Divide `s` donde aparece `t` (espacios por defecto) |
| `s.splitlines()` | Divide en una lista de cadenas, una por línea |
| `s.lower()` / `s.upper()` / `s.titlecase()` | Versiones en minúsculas / mayúsculas / título |
| `s.strip()` | Copia sin espacios al principio ni al final |
| `s.replace(t, u)` | Reemplaza `t` por `u` dentro de `s` |

Diferencia entre listas y cadenas: ambas son secuencias (se indexan, cortan y concatenan), pero no se pueden unir entre sí. Al abrir un archivo obtenemos una cadena y al iterarla solo podemos extraer caracteres; una lista, en cambio, puede tener elementos de cualquier tamaño (párrafos, oraciones, palabras). Por eso lo primero en código NLP suele ser tokenizar una cadena en lista, y al escribir resultados formatearlos como cadena. Además las listas son mutables (se pueden cambiar elementos, `del`) mientras que las cadenas son inmutables: `query[0] = 'F'` da `TypeError`.

## 3.3 Procesamiento de texto con Unicode

El "texto plano" es una ficción: distintos idiomas usan distintos juegos de caracteres (ASCII, latín extendido, etc.). Unicode admite más de un millón de caracteres; cada uno tiene asignado un número llamado code point, escrito como `\uXXXX` (hexadecimal de cuatro dígitos). Dentro del programa se manipulan cadenas Unicode como cadenas normales, pero para guardarlas en archivos o mostrarlas en pantalla deben codificarse como flujo de bytes. Algunas codificaciones usan un byte por code point (ASCII, Latin-2); otras usan varios (UTF-8) y cubren todo el rango. Traducir de bytes a Unicode es decodificar (decoding); traducir de Unicode a bytes es codificar (encoding). Un carácter es una entidad abstracta que se realiza como uno o más glifos; una fuente es el mapeo de caracteres a glifos.

El módulo `codecs` lee datos codificados a Unicode y los escribe: `codecs.open(path, encoding='latin2')` abre un archivo indicando su codificación. Para ver Unicode en el terminal hay que codificarlo con una codificación adecuada; `unicode_escape` convierte los no-ASCII en su forma `\uXXXX`. Un literal Unicode se escribe anteponiendo `u` a la cadena (`u'hello'`) y se usan secuencias `\uXXXX` para caracteres arbitrarios. `ord()` da el ordinal entero de un carácter. El módulo `unicodedata` permite inspeccionar propiedades (nombre, code point con prefijo `U+`). Los métodos de cadena, el módulo `re` y los tokenizadores de NLTK aceptan y devuelven cadenas Unicode. Para usar la codificación local en un archivo fuente se incluye `# -*- coding: <coding> -*-` como primera o segunda línea.

## 3.4 Expresiones regulares para detectar patrones de palabras

Las expresiones regulares ("regexp") dan un método potente y flexible para describir patrones de caracteres, más allá de pruebas como `endswith('ed')`. Se usa `import re` y `re.search(p, s)` para comprobar si el patrón `p` aparece en la cadena `s`. En el libro los patrones se marcan con chevrones «patt». Ejemplo con la lista de palabras (sin nombres propios):

```python
wordlist = [w for w in nltk.corpus.words.words('en') if w.islower()]
[w for w in wordlist if re.search('ed$', w)]   # palabras que terminan en ed
```

Metacaracteres básicos: `.` cualquier carácter; `^` inicio; `$` fin; `?` carácter previo opcional (`^e-?mail$` casa email y e-mail). Rangos y clausuras: `[ghi]` uno del conjunto; `[g-o]` un rango; `+` una o más repeticiones del elemento previo; `*` cero o más (clausuras de Kleene); `^` dentro de corchetes niega el conjunto (`[^aeiou]` = no vocal). Otros símbolos: `\` quita el poder especial al carácter siguiente (`\.` casa un punto literal); `{n}`, `{n,}`, `{,n}`, `{m,n}` especifican número de repeticiones; `|` indica disyunción (elección); los paréntesis delimitan el alcance de un operador, combinables con `|` como en «w(i|e|ai|oo)t».

Tabla 3-3 (metacaracteres básicos): `.` comodín; `^abc`/`abc$` patrón al inicio/final; `[abc]` uno de un conjunto; `[A-Z0-9]` uno de un rango; `ed|ing|s` disyunción; `*` cero o más (clausura de Kleene); `+` uno o más; `?` cero o uno (opcional); `{n}`/`{n,}`/`{,n}`/`{m,n}` repeticiones; `a(b|c)+` paréntesis para el alcance.

Para el intérprete de Python una regexp es una cadena más, y secuencias como `\b` tienen significado propio; por eso conviene prefijar las regexp con `r` (cadena "raw") para que Python las pase literalmente a `re`. Así `r'\band\b'` casa fronteras de palabra en vez de retrocesos.

## 3.5 Aplicaciones útiles de las expresiones regulares

Además de comprobar coincidencias, las regexp sirven para extraer o modificar material. `re.findall()` encuentra todas las coincidencias no solapadas: por ejemplo todas las vocales de una palabra, o todas las secuencias de dos o más vocales en un texto para medir su frecuencia con `nltk.FreqDist`. Con los trozos extraídos se pueden hacer cosas interesantes, como comprimir palabras quitando vocales internas (conservando secuencias vocálicas iniciales o finales) y volver a unirlas con `''.join()`. Combinando regexp con distribuciones de frecuencia condicionales se pueden tabular secuencias consonante-vocal de un idioma (ej. Rotokas) y detectar distribución complementaria entre letras.

Para hallar raíces (stems) de palabras, un enfoque simple quita sufijos de una lista. Con regexp se construye una disyunción de sufijos; hay sutilezas importantes: los paréntesis seleccionan la subcadena extraída (para solo delimitar el alcance se usa `(?:...)`), y el operador `*` es "codicioso" (consume lo máximo posible), por lo que conviene la versión no codiciosa `*?` para separar bien raíz y sufijo. El patrón `r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'` divide palabra en raíz y sufijo, aunque sigue produciendo no-palabras como `distribut` o `deriv`, aceptables en algunas aplicaciones.

NLTK también permite buscar sobre texto tokenizado con una regexp especial donde los corchetes angulares marcan límites de token: `moby.findall(r"<a> (<.*>) <man>")` encuentra lo que va entre "a" y "man"; `<.*>` casa cualquier token. Patrones como «x and other ys» permiten descubrir hiperónimos automáticamente, aunque con falsos positivos (casos a excluir) y falsos negativos (casos omitidos): es arriesgado concluir que un fenómeno no existe solo porque no se encontró con un patrón.

## 3.6 Normalización de texto

Antes de procesar solemos convertir el texto a minúsculas (`w.lower()`) para ignorar la distinción entre "The" y "the". Ir más allá y quitar afijos es stemming; asegurar además que la forma resultante es una palabra de diccionario es lematización (lemmatization).

Stemmers: NLTK incluye varios listos para usar, preferibles a crear uno propio con regexp porque manejan muchos casos irregulares. El Porter y el Lancaster siguen sus propias reglas; el Porter trata bien "lying" (lo mapea a "lie"), el Lancaster no. Se elige el stemmer que mejor se adapte a la aplicación; el Porter es buena opción para indexar textos y permitir búsquedas con formas alternativas (Ejemplo 3-1, clase `IndexedText`). Lematización: `nltk.WordNetLemmatizer()` solo quita afijos si el resultado está en su diccionario, lo que lo hace más lento; no trata "lying" pero sí convierte "women" en "woman". Es la mejor opción para compilar un vocabulario de lemas válidos. Otra tarea de normalización es identificar palabras no estándar (números, abreviaturas, fechas) y mapearlas a un vocabulario especial (p. ej. todo decimal a `0.0`), lo que reduce el vocabulario y mejora el modelado del lenguaje.

## 3.7 Expresiones regulares para tokenizar texto

La tokenización corta una cadena en unidades lingüísticas identificables. El método más simple es dividir por espacios (`raw.split()`), pero con regexp tenemos más control. `re.split(r' ', raw)` deja tokens con `\n`; mejor `re.split(r'[ \t\n]+', raw)` o su abreviatura `\s+` (cualquier espacio en blanco). Dividir por espacios da tokens como `'(not'` o `'herself,'`. Usando la clase `\w` (caracteres de palabra, `[a-zA-Z0-9_]`) y su complemento `\W`, `re.findall(r'\w+', raw)` extrae palabras sin cadenas vacías. Patrones más ricos agrupan la puntuación con las letras siguientes y separan secuencias de dos o más signos, y pueden permitir guiones y apóstrofos internos («\w+([-']\w+)*»).

Tabla 3-4 (símbolos de clase): `\b` frontera de palabra; `\d`/`\D` dígito / no dígito; `\s`/`\S` espacio / no espacio; `\w`/`\W` alfanumérico / no alfanumérico; `\t` tabulador; `\n` salto de línea.

`nltk.regexp_tokenize()` es similar a `re.findall()` pero más eficiente para tokenizar y evita el tratamiento especial de paréntesis. La bandera verbose `(?x)` permite escribir la regexp en varias líneas con comentarios (entonces hay que usar `\s` en vez de un espacio literal). Con `gaps=True` la regexp especifica los huecos entre tokens. La tokenización es más difícil de lo que parece: no hay solución universal, se evalúa comparando con texto tokenizado a mano ("gold-standard"), y hay casos como las contracciones (didn't → did + n't) que conviene normalizar con una tabla de consulta.

## 3.8 Segmentación

La tokenización es un caso de un problema más general: la segmentación. Segmentación de oraciones: manipular palabras suele requerir dividir el texto en oraciones. NLTK incluye el segmentador Punkt (Kiss & Strunk, 2006): `nltk.data.load('tokenizers/punkt/english.pickle')`. Es difícil porque el punto marca abreviaturas y a veces abreviatura y fin de oración a la vez (ej. U.S.A.). Segmentación de palabras: en sistemas de escritura sin espacios (chino) o en el habla continua no hay límites visibles de palabra. Se representa el problema anotando cada carácter con un booleano (hay o no frontera después). La tarea se vuelve un problema de búsqueda: hallar la cadena de ceros y unos que segmenta correctamente. Siguiendo a Brent & Cartwright (1995) se define una función objetivo que puntúa una segmentación según el tamaño del léxico y la información para reconstruir el texto (valores menores = mejor), y se busca el óptimo con recocido simulado (simulated annealing). Con suficientes datos se puede segmentar en palabras con precisión razonable.

## 3.9 Formateo: de listas a cadenas

Para mostrar o guardar listas de palabras hay que convertirlas en cadenas con `join()`, indicando el pegamento: `' '.join(silly)`. `join()` es un método de la cadena que hace de pegamento y solo funciona sobre listas de cadenas. Hay dos formas de mostrar un objeto: `print` da la forma más legible (sin comillas), y nombrar la variable muestra una representación recreable; ambas son solo cadenas para el usuario. La salida formateada combina variables y cadenas fijas mediante expresiones de formato: los especificadores de conversión `%s` (cadena) y `%d` (entero decimal) son marcadores que se combinan con el operador `%` y una tupla de valores. Se puede fijar el ancho (`%6s` rellena a 6, justificado a la derecha; `%-6s` a la izquierda; `%*s` toma el ancho de una variable), usar `%2.4f` para flotantes y `%%` para un porcentaje literal. Esto es clave para tabular datos con control de cabeceras y anchos (Ejemplo 3-5, frecuencia de modales en el Brown). Para escribir en archivo se abre con `open('output.txt', 'w')` y se usa `write()`, convirtiendo antes los datos no textuales a cadena con `str()` o formato; conviene evitar nombres con espacios o que solo difieran en mayúsculas. El módulo `textwrap` (`fill`) ajusta la salida tipo texto que desborda la línea.

## Ideas clave

- Un texto se ve como lista de palabras; un "texto en bruto" es una cadena larga con palabras y espacios, que casi siempre llega con ruido (cabeceras, pies, marcado) que hay que eliminar antes de procesar.
- El pipeline típico: abrir URL/archivo → quitar marcado → recortar porción útil → tokenizar → `nltk.Text` → minúsculas → vocabulario; conviene tener claro el tipo (`str`, `list`) de cada variable.
- Las cadenas son inmutables y se indexan/cortan desde cero (índices negativos desde el final); las listas son mutables y de granularidad flexible; no se pueden concatenar entre sí.
- El "texto plano" es una ficción: se usa Unicode (code points `\uXXXX`), con decoding (bytes→Unicode) y encoding (Unicode→bytes), y el módulo `codecs` para leer/escribir con una codificación concreta.
- Las expresiones regulares (prefijadas con `r'...'`) detectan patrones con metacaracteres (`.`, `^`, `$`, `?`, `*`, `+`, `[]`, `{}`, `()`, `|`); `re.search`, `re.findall` y `re.split` cubren comprobar, extraer y dividir.
- La tokenización segmenta el texto en tokens; dividir solo por espacios es insuficiente, por eso se usan regexp o `nltk.word_tokenize()` / `nltk.regexp_tokenize()`.
- La normalización incluye pasar a minúsculas, stemming (Porter, Lancaster) y lematización (WordNet, solo si la forma está en el diccionario).
- La segmentación de oraciones (Punkt) y de palabras (búsqueda con función objetivo y recocido simulado) son casos del problema general de segmentación; el formateo con `%s`/`%d`, anchos y `join()` convierte resultados en cadenas para pantalla o archivo.
