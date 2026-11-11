# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 4 — Data Munging: String Manipulation, Regular Expressions, and Data Cleaning (Limpieza de datos: manipulación de cadenas, expresiones regulares y saneamiento)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber
El capítulo trata las patologías que aparecen en datos del mundo real: de dónde vienen y cómo abordarlas. El autor las divide en dos grandes tipos: problemas de formato (capitalización inconsistente, espacios sobrantes, etc.), normalmente fáciles de resolver con preprocesado; y problemas de contenido (entradas duplicadas, valores atípicos grandes, NULLs), que exigen trabajo detectivesco para entender qué significan en cada situación.

La tesis central es que la manipulación de cadenas de texto, aunque parezca aburrida, es una de las herramientas más potentes del data scientist, a la par de la propia machine learning. Sirve para resolver cualquier problema de formato y, a menudo, es la única solución viable; también es clave para escribir scripts rápidos que extraen la información concreta que necesitas. Muchas veces el camino "rápido y sucio" de un script hecho a mano es más expeditivo que aprender un paradigma y herramientas complicadas.

Sales sabiendo reconocer y diagnosticar rápido los problemas típicos de los datos, y manejar las herramientas para resolverlos: métodos de cadenas de Python, un script de formateo de ejemplo y, como "artillería pesada", las expresiones regulares (regular expressions).

## El peor dataset del mundo y cómo detectar patologías
El autor relata que su peor dataset industrial fue el primero: logs de servidores donde un mismo servidor tenía varios nombres, campos codificados en hexadecimal extraño, líneas sin filas ni columnas y la mayoría del contenido inútil. La lección: todos los datasets son así. Donde hay una organización grande, un proceso de recolección complejo o varios datasets fusionados, los problemas se acumulan y rara vez están documentados.

Uno de los peores escándalos en data science es tener que retractar resultados por haber procesado mal los datos, así que conviene cierta paranoia. Para identificar problemas pronto, el autor da cuatro consejos:

- Si los datos son texto, mira directamente el archivo crudo, no solo lo que lee tu script.
- Lee la documentación de apoyo si existe; códigos y convenciones raras suelen estar explicados en PDFs adjuntos.
- Ten una batería de preguntas diagnósticas estándar: ¿esta columna tiene NULLs? ¿Están todos los identificadores de la tabla A en la B y viceversa?
- Haz comprobaciones de sensatez (sanity checks): deriva de los datos algo que ya conozcas. Si cuentas los clientes y no coincide con los que sabes que tiene la empresa, probablemente no los estás identificando bien.

## Problemas de contenido de los datos
- Entradas duplicadas: comprueba siempre si existen. A veces son reales y conviene condensarlas en una sola, añadiendo una columna con el número de entradas únicas; otras veces la duplicación es solo un artefacto de cómo se generaron los datos (seleccionar unas columnas de un dataset mayor).
- Múltiples entradas para una misma entidad: lo habitual es que algunas filas estén desactualizadas y solo una sea correcta. Pero a veces debe haber varias: p. ej. un generador con varios motores idénticos, cada uno reportando su estado con el mismo número de serie; si no hay campo que los distinga, suelen venir en orden fijo. También ocurre si la misma entidad se procesa dos veces (componentes que se reparan y pasan de nuevo por la línea de montaje).
- Entradas faltantes: cuando faltan entidades suele haber una característica común que las excluyó. Si agrupas transacciones por cliente, quien no tuvo transacciones queda fuera; se arregla uniendo contra un conjunto conocido de todos los clientes. Otras veces el dato nunca se recogió para ciertas entidades.
- NULLs: normalmente significan que no se conoce un dato. Muchos algoritmos no los procesan, así que a menudo hay que sustituirlos por un valor razonable (estimado de otros campos o la media de los valores no nulos). Si el NULL surge porque ese dato nunca se recogió, el hecho de ser NULL puede ser por sí mismo una feature muy potente (p. ej. la fábrica de origen).
- Valores atípicos enormes (outliers): a veces reflejan un evento real, a veces deben filtrarse (un pico de tráfico web suele ser un ataque de bots, no humanos), y otras veces indican datos faltantes codificados con un valor arbitrario predeterminado (muchas entradas idénticas y aparentemente arbitrarias).
- Datos desactualizados: en muchas bases de datos cada fila lleva timestamp y, al actualizar, se añade una fila nueva en vez de reemplazar; quedan entradas ya no vigentes, útiles solo para reconstruir la historia.
- Entradas artificiales: datos insertados deliberadamente, normalmente para probar los sistemas de software que los procesan.
- Espaciados irregulares: muchos algoritmos asumen puntos equiespaciados. Con sensores suele usarse interpolación para generar valores equiespaciados. Un caso especial: dos entradas con timestamp idéntico por precisión finita del reloj.

## Problemas de formato
- Formato irregular entre tablas/columnas: frecuente por cómo se almacenaron; especialmente grave cuando las claves para unir o agrupar están formateadas de forma distinta.
- Espacios sobrantes: resultan insidiosos porque no se ven al imprimir; arruinan uniones ("ABC" vs " ABC "). En Python, `strip()` quita espacios de ambos extremos, y `lstrip()`/`rstrip()` solo del inicio/final; si se pasa un carácter como argumento, solo se elimina ese.

```python
>>> "ABC\t".strip()
'ABC'
>>> "ABC".strip("C")
'AB'
```

- Capitalización irregular: `lower()` y `upper()` devuelven una copia en minúsculas o mayúsculas.
- Delimitadores inconsistentes: lo normal es un único delimitador, pero distintas tablas pueden usar otros. Los más comunes: comas, tabuladores y pipes (`|`).
- Formato de NULL irregular: en CSV los faltantes se codifican de muchas formas y todas deben leerse como NULL: cadena vacía `""`, `NA`, `NULL`, y a veces `unavailable` o `unknown`.
- Caracteres inválidos: algunos archivos tienen bytes no válidos. `decode()` toma el formato de texto y qué hacer si la conversión falla; con `"ignore"` los caracteres inválidos se descartan.

```python
>>> s = "abc\xFF"
>>> s.decode("ascii", "ignore")
u'abc'
```

- Fechas/horas raras o incompatibles: de los campos más maltratados (`August 1, 2013`, `AUG 1, '13`, `2013-08-13`). A diferencia de otros formatos, aquí el contenido informativo puede variar (¿hay hora?, ¿minuto, segundo, zona horaria?). Conviene pasar cuanto antes al tipo datetime nativo. En Python, el paquete `dateutil` parsea bien y redondea hacia abajo.

```python
>>> import dateutil.parser as p
>>> p.parse("2013-8-13 4:15am")
datetime.datetime(2013, 8, 13, 4, 15)
```

- Incompatibilidades de sistema operativo: sobre todo saltos de línea, `\n` en Mac/Linux y `\r\n` en Windows.
- Versiones de software equivocadas: un archivo generado con una versión y abierto con otra lanza errores crípticos (típico en formatos de compresión).

## Script de formateo de ejemplo
El autor muestra cómo limpiar datos "asquerosos" con formateo de cadenas improvisado y cargarlos en un DataFrame de Pandas. Partiendo de un archivo con delimitador `|` donde nombres llevan títulos (`Ms.`, `Dr.`), edades vienen como `74 Years` o `66yo` y fechas en formatos dispares, define funciones que normalizan cada campo: `get_first_last_name` quita títulos y capitaliza, `format_age` extrae solo los dígitos, y `format_date` normaliza a `AAAA-MM-DD` con un mapa de meses. Luego aplica cada función con `df["col"].apply(...)`. El código no es elegante ni eficiente, pero es claro, hace el trabajo y es fácil de modificar.

## Expresiones regulares (regular expressions)
Son la "artillería pesada" del procesamiento de datos: generalizan operaciones como split o indexado para que actúen sobre un patrón, no sobre cadenas concretas. Por ejemplo, extraer todos los teléfonos con formato `(XXX)XXX-XXXX` de un documento sería penoso con cadenas normales y trivial con regex. El autor advierte dos inconvenientes: son notoriamente delicadas de usar y depurar (expresar un patrón complejo es mucho más difícil que "entenderlo"), por lo que conviene mantenerlas cortas; y son costosas computacionalmente, incluso compilarlas lleva tiempo.

Sintaxis básica, con `ab*` como ejemplo: una `a` seguida de cualquier número (incluido 0) de `b`. El `*` repite el carácter anterior. Ante matches solapados, la estrategia por defecto es greedy (voraz): desde la izquierda, busca el match más largo, lo recorta y sigue. Es eficiente porque hace una sola pasada. Los Match objects devuelven la cadena y sus índices de inicio/fin, aunque el autor suele usar enfoques simples que devuelven una lista de cadenas.

Elementos frecuentes de sintaxis:
- `a*` cero o más; `a+` una o más; `a?` como mucho una.
- `a{5}` exactamente 5; `a{2,4}` entre 2 y 4 (rango inclusivo); `(a*b){3}` repite un patrón.
- `[ab]c` elige un carácter del grupo; `[A-H][a-z]*` rangos; `[^AB]` cualquiera MENOS los indicados (el `^` solo tiene ese sentido como primer carácter).
- `Dr|Mr|Ms|Mrs` elección entre expresiones; `([A-Z]|[a-z]|[0-9])*` anida (en Python `\w` abrevia alfanumérico).
- `^ab` inicio de línea; `ab$` fin de línea; `\[` escapa un carácter especial; `.` cualquier carácter salvo newline; `\s` cualquier espacio en blanco.
- Evaluación no voraz (nongreedy) con `?`: busca el camino más corto. Para extraer campos de `<name>Jane</name><name>Bob</name>`, `<name>.*</name>` captura todo; `<name>.*?</name>` devuelve los dos matches.

La implementación de Python es la librería ligera `re`. El autor muestra un ejemplo que busca direcciones compilando un patrón y usando `re.findall`. Tres observaciones: es muy potente (pocas líneas, tarea compleja); es limitado (no maneja números de apartamento, calles de varias palabras ni "32nd street", y parchearlo puede volverlo inmanejable); y usa raw strings, poniendo una `r` antes de la comilla. Las raw strings evitan el dolor del carácter de escape `\`: `"\n"` es un salto de línea, pero `re.compile` espera la barra y la `n`; sin raw string habría que escribir `"\\n"`, y una sola barra sería `"\\\\"`.

## Vida en las trincheras
Es un capítulo corto porque la limpieza de datos generaliza mal: es la parte aburrida, el precio de dejar los datos en un formato donde hacer las preguntas reales. Aun así es un reto intelectual y de resolución de problemas, a veces mayor que el propio análisis: suele requerir mucho trabajo detectivesco y código solo para dejar los datos en forma tabular limpia. Es donde data science se mezcla con código de producción: hay creatividad al extraer features, pero normalmente solo hay una forma "correcta" de limpiar, y ese código se escribe una vez y se reutiliza entre iteraciones. Después toca entender el mundo descrito: visualizaciones y análisis exploratorio.

## Ideas clave
- Las patologías de datos se dividen en problemas de formato (normalmente preprocesables) y de contenido (requieren interpretación).
- Detecta problemas pronto: mira el archivo crudo, lee la documentación, ten preguntas diagnósticas y haz sanity checks.
- Duplicados, múltiples entradas por entidad, faltantes, NULLs, outliers, datos obsoletos, entradas artificiales y espaciados irregulares son las patologías de contenido típicas.
- Un NULL por dato nunca recogido puede ser, en sí mismo, una feature informativa.
- Los métodos de cadenas de Python (`strip`, `lower`/`upper`, `decode`) resuelven espacios, capitalización y bytes inválidos; `dateutil` normaliza fechas.
- Un script de formateo improvisado pero claro basta para limpiar datos sucios y cargarlos en Pandas.
- Las expresiones regulares son potentes pero finicky y costosas; mantenlas cortas, entiende greedy vs nongreedy y usa raw strings (`r"..."`) en Python.
- La limpieza de datos es tediosa pero intelectualmente exigente; suele haber una única forma correcta y se reutiliza entre análisis.
