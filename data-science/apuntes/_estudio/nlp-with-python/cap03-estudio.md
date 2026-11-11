# Processing Raw Text (Procesamiento de texto en bruto) — Estudio

## Tarjetas de repaso

P: ¿Qué tres preguntas responde el capítulo sobre el trabajo con texto propio?
R: Cómo acceder a texto desde archivos locales y la Web, cómo partir documentos en palabras y signos de puntuación (tokenización), y cómo producir salida formateada y guardarla en un archivo.

P: ¿Cuál es la tesis central del capítulo sobre el "texto plano"?
R: Que el "texto plano" es una ficción: todo texto real llega con ruido (encabezados, marcado HTML, codificaciones diversas) y hay que procesarlo por capas.

P: ¿Cuál es el pipeline típico de procesamiento de texto?
R: Abrir una URL o archivo → eliminar marcado → recortar la porción útil → tokenizar → convertir opcionalmente a `nltk.Text` → normalizar a minúsculas → extraer el vocabulario.

P: ¿Qué diferencia hay entre decoding y encoding en Unicode?
R: Decoding es traducir de bytes a Unicode; encoding es traducir de Unicode a bytes (flujo de bytes para guardar o mostrar).

P: ¿Qué es un code point y cómo se escribe?
R: Es el número asignado a cada carácter en Unicode, escrito como `\uXXXX` (hexadecimal de cuatro dígitos).

P: ¿Cuál es la diferencia fundamental entre cadenas y listas?
R: Ambas son secuencias (se indexan, cortan y concatenan), pero las cadenas son inmutables y de granularidad de caracteres, mientras que las listas son mutables y pueden tener elementos de cualquier tamaño; no se pueden concatenar entre sí.

P: ¿Para qué sirven `re.search`, `re.findall` y `re.split`?
R: `re.search` comprueba si un patrón aparece en una cadena; `re.findall` encuentra todas las coincidencias no solapadas (extraer); `re.split` divide la cadena donde casa el patrón.

P: ¿Por qué conviene prefijar las expresiones regulares con `r'...'`?
R: Porque para Python una regexp es una cadena y secuencias como `\b` tienen significado propio; la cadena "raw" (`r`) hace que Python la pase literalmente a `re`.

P: ¿Qué diferencia hay entre stemming y lematización?
R: Stemming quita afijos para hallar la raíz; la lematización, además, asegura que la forma resultante es una palabra de diccionario.

P: ¿En qué se diferencian el stemmer Porter y el Lancaster con "lying"?
R: El Porter trata bien "lying" (lo mapea a "lie"); el Lancaster no.

P: ¿Qué hace el `WordNetLemmatizer` de NLTK?
R: Solo quita afijos si el resultado está en su diccionario (más lento); no trata "lying" pero sí convierte "women" en "woman".

P: ¿Por qué dividir solo por espacios es insuficiente para tokenizar?
R: Deja tokens con ruido como `'(not'` o `'herself,'`; por eso se usan regexp (`\w+`, patrones más ricos) o `nltk.word_tokenize()` / `nltk.regexp_tokenize()`.

P: ¿Qué es la segmentación y qué casos cubre?
R: Es el problema general de dividir texto; incluye la segmentación de oraciones (segmentador Punkt) y la de palabras (en escrituras sin espacios o habla continua).

P: ¿Cómo se aborda la segmentación de palabras según Brent & Cartwright (1995)?
R: Se anota cada carácter con un booleano de frontera y se busca la segmentación óptima con una función objetivo (tamaño del léxico e información para reconstruir el texto) mediante recocido simulado.

P: ¿Qué especificadores de conversión se usan en la salida formateada y para qué?
R: `%s` para cadena y `%d` para entero decimal, combinados con el operador `%` y una tupla de valores; se pueden fijar anchos (`%6s`, `%-6s`, `%*s`) y usar `%2.4f` para flotantes.

## Preguntas de autoevaluación

P: ¿Por qué hay que recortar manualmente los textos de Project Gutenberg y cómo se hace? (sección 3.1)
R: Traen cabecera y pie (nombre, autor, licencia) y no hay forma fiable de detectar dónde empieza y termina el contenido; se inspecciona manualmente y se recorta con `find()` y `rfind()`.

P: ¿Qué ventajas y límites tienen los buscadores web como corpus? (sección 3.1)
R: Ventaja: su enorme tamaño y la facilidad para comprobar hipótesis rápidamente. Límites: patrones de búsqueda muy restringidos, resultados inconsistentes según momento o región, y marcado que cambia impredeciblemente.

P: ¿Por qué suele ser lo primero tokenizar una cadena en lista en código NLP? (sección 3.2)
R: Porque al abrir un archivo se obtiene una cadena de la que solo se extraen caracteres, mientras que una lista puede tener elementos de cualquier tamaño (párrafos, oraciones, palabras); al escribir resultados se formatea de nuevo como cadena.

P: ¿Para qué sirve el módulo `codecs` y cómo se indica la codificación de un archivo? (sección 3.3)
R: Lee datos codificados a Unicode y los escribe; `codecs.open(path, encoding='latin2')` abre un archivo indicando su codificación.

P: ¿Qué problema resuelven los paréntesis no capturantes `(?:...)` y el operador no codicioso `*?` al hallar raíces? (sección 3.5)
R: `(?:...)` delimita el alcance sin seleccionar la subcadena extraída, y `*?` evita que `*` (codicioso) consuma lo máximo posible, separando bien raíz y sufijo.

P: ¿Por qué es arriesgado concluir que un fenómeno no existe al buscar con un patrón? (sección 3.5)
R: Porque los patrones producen falsos positivos (casos a excluir) y falsos negativos (casos omitidos), de modo que no encontrarlo no prueba su ausencia.

P: ¿Cómo se evalúa la calidad de una tokenización y por qué es difícil? (sección 3.7)
R: No hay solución universal; se evalúa comparando con texto tokenizado a mano ("gold-standard"), y hay casos complejos como las contracciones (didn't → did + n't) que conviene normalizar con una tabla de consulta.

P: ¿Por qué es difícil la segmentación de oraciones? (sección 3.8)
R: Porque el punto marca abreviaturas y a veces abreviatura y fin de oración a la vez (ej. U.S.A.); NLTK usa el segmentador Punkt para abordarlo.

## Puntos a dominar

- Reconocer el tipo de cada variable del pipeline (`str` al leer URL/archivo, `list` al tokenizar) y qué operaciones admite cada uno.
- Recordar que las cadenas son inmutables y se indexan/cortan desde cero (índices negativos desde el final) y que las listas son mutables; no se concatenan entre sí.
- Entender Unicode: code points `\uXXXX`, decoding (bytes→Unicode), encoding (Unicode→bytes) y el uso de `codecs` y `# -*- coding: <coding> -*-`.
- Dominar los metacaracteres de regexp (`.`, `^`, `$`, `?`, `*`, `+`, `[]`, `{}`, `()`, `|`) y las clases (`\w`, `\W`, `\s`, `\d`, `\b`), siempre prefijando con `r'...'`.
- Distinguir las tres aplicaciones de regexp: comprobar (`re.search`), extraer (`re.findall`) y dividir (`re.split`), más `nltk.regexp_tokenize()` con `(?x)` y `gaps=True`.
- Elegir la técnica de normalización adecuada: minúsculas, stemming (Porter para indexar, Lancaster) o lematización (WordNet) para un vocabulario de lemas válidos.
- Diferenciar segmentación de oraciones (Punkt) y de palabras (función objetivo + recocido simulado) como casos del problema general de segmentación.
- Formatear salida con `join()`, especificadores `%s`/`%d`, anchos y `%2.4f`, y escribir en archivo con `open(..., 'w')` y `write()` convirtiendo con `str()`; usar `textwrap.fill` para ajustar líneas.
