# Data Encodings and File Formats — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis doble del capítulo sobre formatos y bytes? / R: Siempre aparecerán formatos nuevos, pero casi todos son variaciones de otros ya conocidos, así que dominar unos pocos fundamentos basta; y entender la física de los bytes ayuda a resolver patologías de datos y a escribir código rápido.

P: ¿Cuáles son las cuatro categorías típicas de formatos según Cady? / R: Archivos de texto, arrays numéricos densos, formatos propios de programas, y datos comprimidos o archivados.

P: ¿Cuál es la limitación de los archivos de texto para almacenar números? / R: Son muy ineficientes: `"938238234232425123"` ocupa 18 bytes cuando como número cabría en 8, y además hay que convertirlo antes de operar.

P: ¿Qué significa realmente "CSV" en la práctica y qué variantes de delimitador existen? / R: Suele significar comma-separated value, pero en la práctica es character-separated value; usa otros delimitadores como `.tsv` (tabuladores) y `.psv` (pipes `|`), aunque todo tiende a llamarse CSV.

P: ¿Qué tres tipos de estructura compone todo JSON? / R: Un tipo atómico (número, string, booleano), un JSONObject (mapa de strings a estructuras JSON) o un array de estructuras JSON.

P: ¿Qué no soporta JSON pese a nacer de JavaScript? / R: No soporta punteros, clases ni funciones.

P: ¿Cuál es la diferencia clave entre XML y JSON? / R: En XML el contenido está ordenado (los hijos de cada nodo tienen un orden); además XML es más engorroso de procesar y JSON lo ha ido desplazando en la web.

P: ¿Por qué `<a><b></a></b>` es inválido en XML? / R: Porque las secciones deben anidarse por completo; por eso el documento se piensa como un árbol.

P: ¿Qué relación tiene HTML con XML? / R: HTML es la variante más importante de XML; HTML5, en primera aproximación, es una variante de XML parseable incluso con una librería XML.

P: ¿En qué se diferencian Tar, GZip y Zip? / R: Tar archiva un directorio en un solo fichero sin comprimir; GZip comprime ficheros (usa DEFLATE) y suele combinarse con Tar; Zip usa el mismo DEFLATE pero puede comprimir un directorio entero.

P: ¿Cuáles son las dos categorías de formatos de imagen? / R: Rasterizadas (array de píxeles, p. ej. JPEG, PNG, TIFF) y vectorizadas (descripción matemática escalable, p. ej. SVG, que por dentro es XML).

P: ¿Qué distingue a JPEG, PNG y TIFF? / R: JPEG es lossy, RGB y sin transparencia (el más importante en la web); PNG es lossless y con transparencia; TIFF se usa en fotografía y ciencia y puede ser lossy o lossless.

P: ¿Cómo se almacena un float y por qué es propenso a error? / R: Se guarda como dos enteros (dígitos de la representación binaria y posición del punto decimal); un número puede tener infinitos decimales y solo se guardan finitos, por eso `0.1 + 0.2` da `0.30000000000000004`.

P: ¿Qué es ASCII y cuál es su límite? / R: Es el formato veterano, un carácter por byte con mapeo a enteros cortos ("A" es 65, "a" es 97), limitado a lo tecleable en un teclado americano (hasta 127).

P: ¿Qué es UTF-8 y qué ventaja/desventaja tiene frente a ASCII? / R: Es la versión principal de Unicode, de número variable de bytes por carácter: pierde el tamaño fijo pero gana flexibilidad y es backward compatible con ASCII (todo byte sobre 127 señala un carácter no-ASCII).

## Preguntas de autoevaluación

P: ¿Qué características tendría un algoritmo de compresión "perfecto" según el capítulo? / R: Reduciría el tamaño en general, no inflaría los datos cuando no puede comprimirlos, descomprimiría rápido (a veces más que leer el crudo del disco) y permitiría descomprimir línea a línea y recomprimir rápido. (Sección "Categorías típicas de formatos")

P: ¿Qué recomienda Cady al trabajar con formatos propios de programas como Excel o archivos db? / R: Generar versiones CSV al inicio y usarlas como entrada de los análisis, ya que esos formatos requieren una herramienta específica y suelen ser lentos de abrir. (Sección "Categorías típicas de formatos")

P: Al leer un CSV, ¿qué aspectos hay que vigilar? / R: Cabeceras (puede o no haber una primera línea con nombres), comillas para incluir el delimitador en un campo, filas no-dato con metadatos, comentarios (p. ej. `#`), líneas en blanco y filas con número incorrecto de columnas. (Sección "CSV")

P: ¿Por qué procesar XML resulta más engorroso que JSON? / R: Porque cuesta más localizar un campo con nombre, los atributos se manejan aparte de los hijos y en la práctica el XML suele ser un documento enorme que hay que recorrer entero. (Sección "XML")

P: ¿Cómo funciona `HTMLParser` en Python y qué debe gestionar el usuario? / R: Se crea una subclase que define acciones ante cada tag de apertura/cierre o texto modificando el estado interno; al terminar de recorrer el documento se consulta ese estado, y el usuario debe llevar la cuenta de la profundidad de anidamiento. (Sección "HTML")

P: ¿Qué significa "random" en RAM y por qué importaban los tamaños fijos de los tipos? / R: "Random" alude a que se accede a cualquier parte con la misma latencia, no a probabilidad; los tamaños fijos eran críticos porque el layout de bits no indica dónde empieza y acaba una variable. (Sección "Al final todo son bytes")

P: ¿Qué ocurre en Python cuando un entero supera `sys.maxint`? / R: Python pasa en silencio a un tipo `long`, mucho menos eficiente, delatado por una "L" al final. (Sección "Al final todo son bytes")

P: ¿Por qué la compresión es clave en entornos de Big Data? / R: Porque los datasets son grandes y se recargan de disco en cada ejecución, de modo que la compresión reduce ficheros con mucha redundancia como líneas repetidas o arrays con muchos 0s. (Sección "Categorías típicas de formatos")

## Puntos a dominar

- Reconocer las cuatro categorías de formatos (texto, arrays numéricos densos, formatos propios de programas, comprimidos/archivados) y el compromiso legibilidad vs eficiencia con números.
- Leer un CSV con Pandas `read_csv` controlando `sep` y `header`, y anticipar cabeceras, comillas, comentarios y filas mal formadas.
- Parsear y serializar JSON con `json.loads` / `json.dumps` y distinguir tipo atómico, JSONObject y array.
- Entender el modelo de árbol de XML/HTML y cuándo usar `xml.etree.ElementTree`, el DOM o `HTMLParser`.
- Diferenciar archivado (Tar) de compresión (GZip, Zip con DEFLATE) y saber que Zip puede comprimir directorios enteros.
- Clasificar imágenes en rasterizadas (JPEG lossy, PNG lossless con alpha, TIFF) y vectorizadas (SVG = XML), y leer imágenes con `scipy.ndimage.imread` y sus modos `F` y `RGBA`.
- Explicar la representación de enteros (tamaño fijo con bit de signo), floats (par de enteros, error de redondeo) y texto (ASCII de 1 byte vs UTF-8 variable y compatible con ASCII).
