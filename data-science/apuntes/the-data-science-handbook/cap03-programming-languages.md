# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 3 — Programming Languages (Lenguajes de programación)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Se conservan solo fragmentos de código esenciales.

## Lo que necesitas saber

Lo que distingue a un científico de datos de un analista de negocio tradicional (y, en menor grado, de un estadístico) es que dedica mucho tiempo a escribir código en un lenguaje de programación convencional, como los ingenieros de software. El capítulo defiende por qué es imprescindible saber programar y repasa los lenguajes más populares para ciencia de datos, antes de entrar de lleno en Python, el lenguaje favorito del autor y el más usado en la disciplina.

La tesis central es que ninguna herramienta gráfica (Excel, Tableau, Weka) basta por sí sola: todas asumen que los datos ya están en forma tabular, pero cada dataset exige su propia limpieza idiosincrásica y cada problema requiere creatividad para extraer features. Por eso todo científico de datos necesita dominar al menos un lenguaje de programación.

Sales sabiendo situar los principales lenguajes (Python, R, MATLAB/Octave, SAS, Scala), lo suficiente de Python 2.7 para leer el código del resto del libro (tipos atómicos, strings, listas, tuplas, dicts, sets, funciones, control de flujo, clases y el gotcha de tipos hashables) y los fundamentos de las librerías técnicas, en especial Pandas (DataFrames y Series).

## ¿Por qué usar un lenguaje de programación? (PDF p. 32-33)

El autor nunca ha completado un proyecto de ciencia de datos solo con una herramienta gráfica: siempre surge algo (un formato raro, un dataset que no cabe en memoria, una feature poco convencional) que obliga a escribir código. La ciencia de datos es "Turing complete": muchos trabajan íntegramente en lenguajes de programación apoyados en librerías numéricas; otros hacen el data wrangling y la extracción de features en código y luego cargan los datos en otra herramienta para el análisis exploratorio.

Otras herramientas que conviene integrar en el flujo de trabajo:

- Excel: injustamente menospreciado; para análisis sencillos es probablemente el mejor software jamás hecho.
- Tableau: visualiza datos de bases relacionales; limitado en funcionalidad, pero sus gráficos son bellísimos.
- Weka: aplica algoritmos de machine learning ya empaquetados a datasets bien formateados; es un GUI delgado sobre librerías Java.

Todas comparten una limitación crítica: asumen que los datos ya están en forma tabular. Los datasets tabulares están lo bastante estandarizados como para que existan herramientas reutilizables, pero cada dataset real necesita su propia limpieza y cada problema su propia extracción de features.

## Un recorrido por los lenguajes (PDF p. 33-35)

- Python: el preferido del autor y muy popular entre científicos de datos; equilibra la flexibilidad de un lenguaje de scripting con la potencia numérica de un buen paquete matemático (al combinarse con sus librerías científicas). Creado por Guido van Rossum y lanzado en 1991; sintaxis limpia y consistente, con librerías técnicas de código abierto.
- R: el segundo más popular. Diseñado por y para estadísticos, con gráficos y funciones estadísticas integradas de forma nativa. Basado en S (Bell Labs, 1976). Hoy acusa su edad: sintaxis torpe en zonas, soporte de strings pésimo y sistema de tipos anticuado. Su fuerza es la enorme cantidad de librerías especializadas; sigue siendo la lingua franca en estadística.
- MATLAB y Octave: MATLAB (de MathWorks) es un paquete propietario excelente para cómputo numérico, best-in-class en esa área; sintaxis más consistente que R y más músculo numérico que Python. Octave es la versión open-source, sin toda la funcionalidad ni la infraestructura de soporte.
- SAS: framework estadístico propietario de los años 60, con mucho código heredado; el lenguaje resulta muy ajeno a quien viene de lenguajes modernos. Bueno para estadística de negocio, no recomendado para ciencia de datos general.
- Scala: lenguaje prometedor, aún sin soporte de librerías de analítica y visualización suficiente. Similar a Java por debajo, pero con sintaxis más simple y rasgos funcionales; muchas tecnologías de Big Data están escritas en Scala.

## Curso rápido de Python (PDF p. 35-36)

El tutorial no es exhaustivo; busca que puedas leer el código del libro. Sobre versiones: al escribir el libro, Python 2.7 era el más usado porque todas las librerías numéricas funcionaban con él. Python 3.0 (2008) rompió la compatibilidad hacia atrás. El libro asume 2.7. Diferencias clave en 3.x:

- `print` es una función: `print("hello world")`.
- La división de enteros da decimal (`3/2` == 1.5); para división entera, `//`.
- Desaparece la distinción string/Unicode: todo es Unicode, y existe `ByteArray` para manipular bytes.

El "hello world" puede ejecutarse en el intérprete interactivo (prompt `>>>`) o guardando el código en un archivo. En Windows se suele usar PowerShell y un IDE como Visual Studio; el autor prefiere editores de texto planos salvo en bases de código grandes.

## Tipos atómicos y strings (PDF p. 39-41)

Cinco tipos atómicos principales: `int` (entero), `float` (coma flotante), `bool` (verdadero/falso), `string` (texto) y `NoneType`, cuyo único valor `None` sirve de marcador para datos faltantes o procesos fallidos. Python no declara tipos: una función acepta cualquier argumento y solo falla cuando una operación es inválida; además la indentación debe ser consistente (el "gotcha" más famoso: cuatro espacios, o tabs, pero sin mezclar).

Un string se delimita con comillas simples o dobles (equivalentes); las triples comillas permiten strings multilínea. El carácter `\` escapa caracteres especiales (`\n`, `\t`, `\\`). Se accede a subcadenas con notación de corchetes (slicing), con índices que empiezan en 0:

```python
"ABCD"[0]     # 'A'
"ABCD"[1:3]   # 'BC'
"ABCD"[1:]    # 'BCD'
"ABCD"[:-1]   # 'ABC'  (índice negativo)
```

Comentarios: con `#`, o docstrings (strings sueltas al inicio de archivo o función que documentan y quedan accesibles como `__doc__`).

## Contenedores: listas, tuplas, dicts y sets (PDF p. 42-45)

Los contenedores pueden mezclar tipos. Los tres principales son listas, tuplas y dicts; además está el set.

- Lista: secuencia ordenada y mutable. Admite `append`, slicing e índices negativos. Las list comprehensions crean una lista a partir de otra, con filtrado opcional:

```python
squares = [x*x for x in original_list]
squares_of_evens = [x*x for x in original_list if x%2==0]
```

Métodos clave de strings con listas: `split()` (parte en una lista por espacios o por un separador dado) y `join()` (concatena una lista de strings usando el string como delimitador), p. ej. `",".join(["A","B","C"])` da `'A,B,C'`.

- Tupla: como una lista pero inmutable; más eficiente en casos y necesaria donde las listas no sirven (p. ej. como clave de dict). Permite asignación múltiple: `zeroth, first = my_tuple`.
- Dict: mapea claves (de tipo hashable) a valores (cualquier objeto), con llaves y dos puntos. Buena parte del propio lenguaje está construida con dicts (el namespace de variables es uno). Se crea también con `dict(lista_de_tuplas)` y se extrae con `.items()`.
- Set: como un dict con solo claves; colección de objetos únicos atómicos, con `add` y pertenencia mediante `in`.

## Funciones, control de flujo y clases (PDF p. 45-50)

Una función se define con `def`. Una "pure function" solo toma entrada y devuelve salida; si tiene efectos secundarios (imprimir, escribir ficheros, modificar un argumento) deja de serlo. Sin `return`, devuelve `None`. Admite argumentos opcionales (`def raise(x, n=2)`) y, para funciones de una línea sin efectos, expresiones lambda (`sqr = lambda x: x*x`), útiles como funciones anónimas que se pasan a otras funciones.

Control de flujo: el `for` itera sobre cualquier objeto "iterable" (las listas son el caso típico); con dicts se usa `for key, value in my_dict.items()`. También hay `if/elif/else` y `while`. Funciones integradas que conviene conocer: `int`, `float`, `bool`, `str`, `dict`, `range`, `zip`, `open`, `len` y `enumerate`. El manejo de errores usa `try/except`.

Librerías: se importan con `from lib import f1, f2`, `import lib as ol` o `from lib import *` (los dos primeros dan código más legible). Escribir una librería propia es solo crear un `.py` accesible desde el directorio de ejecución.

Clases: se definen con `class`; `__init__` es el constructor y `self` (equivalente al `this` de C++) debe pasarse explícitamente como primer argumento de cada método para referirse a la instancia.

Gotcha de tipos hashables vs. unhashables (PDF p. 49-50): los hashables (ints, floats, strings, tuplas) son inmutables y de bajo nivel; los unhashables (listas, dicts, clases) son mayores y modificables. Al asignar un hashable (`b = a`) se copia el valor; al asignar un unhashable (`B = A`) ambos nombres apuntan al mismo objeto, por lo que modificar uno afecta al otro. Para copiar de verdad: `B = [x for x in A]` (aunque los elementos unhashables internos seguirían compartidos). Las claves de un dict deben ser hashables.

## Librerías técnicas de Python y Pandas (PDF p. 50-55)

Las principales librerías del ecosistema: Pandas (la central: almacena y opera sobre data frames con una API intuitiva), NumPy (arrays numéricos rápidos y de bajo nivel, base de todo lo demás), Scikit-learn (machine learning sobre arrays NumPy), Matplotlib (visualización, envuelta por Pandas) y SciPy (operaciones numéricas avanzadas sobre NumPy). NumPy es el cimiento, pero la mayoría del trabajo real se hace en Pandas.

El objeto central de Pandas es el DataFrame: una tabla con filas y columnas tipadas, similar a una tabla SQL o un data frame de R. Facilita crear columnas derivadas, calcular agregados, filtrar filas y aplicar funciones:

```python
import pandas as pd
df = pd.DataFrame({"name": ["Bob","Alex","Janice"], "age": [60,25,33]})
df["over_30"] = (df["age"] > 30)
total_age = df["age"].sum()
df_below50 = df[df["age"] < 50]
df["age_squared"] = df["age"].apply(lambda x: x*x)
```

Cada DataFrame tiene un index (por defecto el número de fila, pero se puede fijar con `set_index`). Una Series es una columna del DataFrame: un array de objetos del mismo tipo con un index asociado; sumar dos Series alinea por index. Operaciones avanzadas: `join()` combina dos data frames emparejando filas por index, y `groupby()` agrupa filas por una propiedad y agrega cada grupo (con agregados integrados como `mean()` o funciones personalizadas vía `apply`). El capítulo cierra con recursos (docs de Python 2, Pandas, scikit-learn), lecturas recomendadas y un glosario.

## Ideas clave

- Toda herramienta gráfica asume datos tabulares; por eso el científico de datos necesita dominar al menos un lenguaje de programación.
- Python es la opción más popular por equilibrar flexibilidad de scripting y potencia numérica vía sus librerías; R domina en estadística pese a su edad.
- El libro asume Python 2.7; en 3.x cambian `print`, la división y el manejo de strings/Unicode.
- Los tipos atómicos son int, float, bool, string y NoneType; los contenedores clave son listas, tuplas, dicts y sets, y pueden mezclar tipos.
- La indentación consistente es obligatoria en Python; el 0 es el primer índice y se admite slicing con índices negativos.
- Las funciones pueden ser puras o con efectos secundarios, admiten argumentos opcionales y lambdas anónimas.
- Gotcha clave: asignar un hashable copia el valor; asignar un unhashable comparte el mismo objeto en memoria.
- Pandas es la herramienta central (DataFrame y Series) sobre NumPy, con join y groupby para operaciones tipo SQL.
