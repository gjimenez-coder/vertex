# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 12 — Data Encodings and File Formats (Codificaciones de datos y formatos de archivo)

> Nota de extracción: el texto se tomó de la capa de texto del PDF; las citas usan la página del PDF, p. ej. (PDF p. N).

## Lo que necesitas saber

El capítulo recorre los formatos de archivo que un data scientist encuentra a diario y, en su segunda mitad, baja al nivel de los bytes para explicar cómo se representan datos en la memoria del computador. La tesis de Cady es doble: siempre aparecerán formatos nuevos, pero casi todos son variaciones de otros ya conocidos, así que dominar unos pocos fundamentos te deja en buen pie; y entender la física de los bytes te ayuda a resolver patologías de datos y a escribir código rápido.

En la primera parte presenta categorías generales de formatos (texto, arrays numéricos densos, formatos propios de programas, datos comprimidos/archivados) y luego los formatos concretos más comunes: CSV, JSON, XML, HTML, Tar, GZip, Zip y los formatos de imagen. Para cada uno da cuándo es útil y código esencial de parseo en Python.

En la segunda parte explica que al final todo son bytes: cómo se codifican enteros, floats y texto (ASCII y Unicode/UTF-8), con los problemas de precisión de los floats y los líos de conversión entre codificaciones de cadenas. Sales sabiendo elegir el formato adecuado, leerlo con las librerías habituales y anticipar sus costes de almacenamiento y rendimiento.

## Categorías típicas de formatos

Cady agrupa los formatos en cuatro grandes categorías, no exhaustivas ni excluyentes:

- Archivos de texto. Son los más habituales para el data scientist: CSV, JSON, XML, páginas web, volcados de bases de datos y logs. Su ventaja es que los lee un humano y son fáciles de generar o parsear con scripts. Su limitación es que el texto almacena números de forma muy ineficiente: `"938238234232425123"` ocupa 18 bytes, pero como número cabría en 8; además hay que convertirlo antes de operar.
- Arrays numéricos densos. Para grandes arrays de números conviene el formato nativo de la máquina, más eficiente en espacio y rendimiento. Es el caso de imágenes, sonido y muchos datasets científicos; menos frecuente en data science pero aparece.
- Formatos propios de programas. Excel, archivos db y similares requieren una herramienta específica y suelen ser lentos de abrir por los extras del programa. Cady recomienda generar versiones CSV al inicio y usarlas como entrada de los análisis.
- Datos comprimidos o archivados. La compresión reduce ficheros con mucha redundancia (líneas repetidas, arrays con muchos 0s); el archivado condensa muchos ficheros en uno solo para almacenarlos o transferirlos más fácil.

Un algoritmo de compresión "perfecto" reduciría el tamaño en general, no inflaría los datos cuando no puede comprimirlos, descomprimiría rápido (a veces más rápido que leer el crudo del disco), permitiría descomprimir "línea a línea" y recomprimir rápido. La compresión es clave en entornos de Big Data, donde los datasets son grandes y se recargan de disco en cada ejecución.

## CSV

Es el formato de trabajo por excelencia. "CSV" suele significar comma-separated value, pero en la práctica es character-separated value: se usan otros delimitadores (`.tsv` para tabuladores, `.psv` para pipes `|`), aunque todo tiende a llamarse CSV. Conceptualmente es una tabla de filas y columnas, pero hay que vigilar: cabeceras (a veces la primera línea nombra columnas, a veces no), comillas (para incluir el delimitador dentro de un campo), filas no-dato con metadatos al inicio, comentarios (p. ej. `#`), líneas en blanco y filas con número incorrecto de columnas.

En Python se lee con Pandas; los argumentos opcionales que Cady más usa son `sep` y `header`:

```python
import pandas
df = pandas.read_csv("myfile.csv", sep="|", header=False,
                     quotechar='"', compression="gzip", comment='#')
```

## JSON

El formato favorito de Cady por su simplicidad y flexibilidad: serializa estructuras jerárquicas a texto plano. Todo JSON es o un tipo atómico (número, string, booleano), o un JSONObject (mapa de strings a estructuras JSON, parecido a un diccionario de Python pero con claves siempre string), o un array de estructuras JSON (parecido a una lista). Soporta `null`, booleanos en minúscula y anidamiento arbitrario. Nació para serializar objetos de JavaScript, pero no soporta punteros, clases ni funciones.

Parsearlo es trivial: `json.loads` convierte un string JSON en objeto Python y `json.dumps` hace lo contrario.

```python
import json
my_obj = json.loads('{"name": "Field", "height":6.0}')
str_again = json.dumps(my_obj)
```

## XML

Similar a JSON (texto jerárquico legible por humanos y máquinas) pero bastante más complicado, razón por la que JSON lo ha ido desplazando en la web. Todo va entre "tags" `<...>`; cada sección se delimita con un par de tags de apertura y cierre (el de cierre lleva `/`), y el de apertura puede llevar atributos. Las secciones deben anidarse por completo, así que `<a><b></a></b>` es inválido; por eso se piensa el documento como un árbol. Existe azúcar sintáctico: `<foo a="bar"/>` equivale a `<foo a="bar"></foo>`.

Diferencia clave con JSON: en XML el contenido está ordenado (los hijos de cada nodo tienen un orden). Procesarlo es más engorroso: cuesta más localizar un campo con nombre, los atributos se manejan aparte de los hijos, y en la práctica el XML suele ser un documento enorme que hay que recorrer entero. En Python lo más simple es `xml.etree.ElementTree`, que da acceso directo al árbol (`ET.fromstring`, índices de hijos, `.tag`, `.attrib`, `del`, `ET.tostring`). La forma "correcta" y más estandarizada es el Document Object Model (DOM), más complejo de dominar.

## HTML

Es la variante más importante de XML: el lenguaje de las páginas web. En la práctica, HTML "válido" es el que el navegador interpreta como se pretendía; los navegadores han convergido hacia un estándar (HTML5) que, en primera aproximación, es una variante de XML, parseable incluso con una librería XML. HTML es un lenguaje de dominio específico definido por sus tags: `<a>` (hipervínculo), `<img>` (imagen), `<h1>`–`<h6>` (encabezados), `<div>` (división organizativa, a menudo con atributo `class`), `<ul>`/`<li>` (listas).

El problema práctico es que los documentos HTML son muy desordenados (hechos y retocados a mano), sin regularidad entre uno y otro, así que las herramientas tienden a recorrer todo el documento buscando lo que necesitas. La herramienta por defecto en Python es `HTMLParser`: se crea una subclase que define acciones ante cada tag de apertura/cierre o texto, modificando el estado interno del parser; al terminar de recorrer el documento se consulta ese estado. El usuario debe llevar la cuenta de la profundidad de anidamiento.

## Tar, GZip y Zip

- Tar es el formato de archivado más común: combina un directorio entero (con subdirectorios) en un solo fichero, sin comprimir, que ocupa casi lo mismo que el original. Java lo usa: los JAR son class files "tarreados" juntos. Como no comprime, casi siempre se comprime después con GZip; `.tgz` es atajo de `.tar.gz`. Se opera desde la línea de comandos (`tar -xvf`, `tar -zxf`, `tar -cf`).
- GZip es el formato de compresión más común en sistemas tipo Unix (Mac, Linux), a menudo junto a Tar. Comprime muy bien, descomprime rápido y permite hacerlo línea a línea. Usa el algoritmo DEFLATE: el fichero se divide en bloques con una cabecera que indica cómo está codificado el resto (algún tipo de código Huffman); así se lee byte a byte usando mínima RAM. Comandos: `gunzip`, `gzip`.
- Zip es muy parecido a GZip —de hecho usa el mismo DEFLATE— pero puede comprimir un directorio entero en vez de ficheros sueltos. Comandos: `zip`, `unzip`.

## Formatos de imagen

Se dividen en dos categorías. Las imágenes rasterizadas descomponen la imagen en un array de píxeles (brillo o color de cada uno), a veces almacenado directamente y a veces comprimido; casi todo dato generado por máquina es rasterizado. Las vectorizadas son una descripción matemática (círculos, líneas) escalable sin perder resolución, típica de logos y animaciones; el formato vectorial más común es SVG, que por dentro es un XML.

Consideraciones que diferencian los formatos rasterizados: lossy vs lossless (BMP y PNG codifican el array exacto; JPEG degrada resolución para reducir tamaño), escala de grises vs RGB (un número por píxel frente a rojo/verde/azul), y transparencia (canal "alpha" de 0 a 1). Formatos clave: JPEG (el más importante en la web, lossy, RGB, sin transparencia), PNG (lossless, con transparencia) y TIFF (fotografía y ciencia, lossy o lossless).

```python
from scipy.ndimage import imread
img = imread('mypic.jpg')  # array NumPy 3D (ancho, alto, RGB), enteros 0–255
```

Con `mode="F"` se lee en escala de grises (array 2D) y con `mode="RGBA"` se incluye el alpha como cuarto valor.

## Al final todo son bytes: enteros, floats y texto

En el nivel más bajo, un fichero es un array de bits (0 o 1) agrupados en chunks de 8 bits llamados bytes. El byte es a la vez convención lógica (una letra o un número por byte) y físico (el hardware procesa datos byte a byte). La memoria es RAM (random access memory): "random" no alude a probabilidad, sino a que se accede a cualquier parte con la misma latencia. Históricamente cada tipo atómico ocupaba un número fijo de bytes (un entero, 4), porque el layout de bits no indica dónde empieza y acaba una variable; los tamaños fijos son críticos para rastrearlas. Lenguajes modernos como Python admiten tipos de tamaño variable (un string), pero con sobrecarga y coste de rendimiento; las librerías numéricas rápidas se limitan a tipos de tamaño fijo.

Enteros: ocupan un número fijo de bytes (8 en un computador de 64 bits), se codifican en binario y un bit actúa de flag de signo. Hay un máximo: en Python `sys.maxint` es 9223372036854775807 (2^63). Si se supera, Python pasa en silencio a un tipo `long`, mucho menos eficiente, delatado por una "L" al final.

Floats: son propensos a error porque un número puede tener infinitos decimales y solo se guardan finitos. Se almacenan como dos enteros: uno con los dígitos de la representación binaria y otro con la posición del punto decimal; esto permite igual precisión relativa para números muy grandes y muy pequeños. El error de redondeo aflora de forma sutil: `0.1 + 0.2` da `0.30000000000000004`, porque 0.1 y 0.2 tienen infinitos decimales en binario y se guarda una aproximación. Existen sistemas de aritmética exacta (strings de longitud arbitraria o expresiones), muy costosos y útiles sobre todo en matemática teórica.

Texto: al contrario que los números, las cadenas sí requieren atención por sus distintas implementaciones. ASCII es el formato veterano, simple y eficiente: un carácter por byte ("char"), con un mapeo a enteros cortos ("A" es 65, "a" es 97, tab 9, newline 10), pero limitado a lo que se teclea en un teclado americano (números hasta 127). En Python `chr()` y `ord()` convierten entre carácter y número; con `\x` se escribe un byte en hexadecimal (hasta 255). Unicode es una familia de codificaciones que amplían ASCII; la versión principal es UTF-8, de número variable de bytes por carácter: pierde la ventaja del tamaño fijo pero gana flexibilidad, y es backward compatible con ASCII (todo byte sobre 127 señala un carácter no-ASCII). Python soporta Unicode nativamente con el prefijo `u"..."`, y `decode('ascii'/'utf8', 'ignore')` convierte o descarta caracteres no válidos.

## Ideas clave

- Casi todos los formatos nuevos son variaciones de otros; domina los fundamentos y el texto frente al binario (legibilidad vs eficiencia con números).
- CSV es el caballo de batalla: cuidado con delimitadores, cabeceras, comillas, comentarios y filas mal formadas; en Python, Pandas `read_csv` con `sep` y `header`.
- JSON (jerárquico, flexible, sin punteros ni clases) tiende a desplazar a XML, que es más complejo pero mantiene el orden de los hijos.
- HTML es la variante clave de XML; sus documentos son desordenados y se procesan recorriéndolos enteros con `HTMLParser`.
- Tar archiva sin comprimir; GZip y Zip comprimen con el mismo algoritmo DEFLATE (Zip puede comprimir directorios enteros).
- Las imágenes son rasterizadas (array de píxeles: JPEG lossy, PNG lossless con alpha, TIFF) o vectorizadas (SVG, que es XML).
- Al final todo son bytes: enteros de tamaño fijo con bit de signo, floats como par de enteros (propensos a redondeo), strings en ASCII (1 byte) o UTF-8 (variable, compatible con ASCII).
