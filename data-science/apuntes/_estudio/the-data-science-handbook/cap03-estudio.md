# Programming Languages (Lenguajes de programación) — Estudio

## Tarjetas de repaso

P: ¿Qué distingue a un científico de datos de un analista de negocio tradicional? / R: Dedica mucho tiempo a escribir código en un lenguaje de programación convencional, como los ingenieros de software.

P: ¿Por qué ninguna herramienta gráfica (Excel, Tableau, Weka) basta por sí sola? / R: Todas asumen que los datos ya están en forma tabular, pero cada dataset exige su propia limpieza y cada problema su propia extracción de features.

P: ¿Cuál es el lenguaje favorito del autor y por qué? / R: Python, porque equilibra la flexibilidad de un lenguaje de scripting con la potencia numérica de un buen paquete matemático al combinarse con sus librerías científicas.

P: ¿Qué caracteriza a R como lenguaje para ciencia de datos? / R: Es el segundo más popular, diseñado por y para estadísticos con gráficos y funciones estadísticas nativas; acusa su edad pero sigue siendo la lingua franca en estadística por su cantidad de librerías.

P: ¿Qué versión de Python asume el libro y qué tres cosas cambian en 3.x? / R: Asume Python 2.7; en 3.x `print` es función, la división de enteros da decimal (`3/2`==1.5, y `//` para entera) y todo string es Unicode (con `ByteArray` para bytes).

P: ¿Cuáles son los cinco tipos atómicos principales de Python? / R: int, float, bool, string y NoneType (cuyo único valor `None` marca datos faltantes o procesos fallidos).

P: ¿Qué diferencia una lista de una tupla? / R: La lista es una secuencia ordenada y mutable; la tupla es como una lista pero inmutable, más eficiente y necesaria donde las listas no sirven (p. ej. como clave de dict).

P: ¿Qué es una list comprehension? / R: Una expresión que crea una lista a partir de otra, con filtrado opcional, p. ej. `[x*x for x in original_list if x%2==0]`.

P: ¿Qué es una "pure function"? / R: Una función que solo toma entrada y devuelve salida; si tiene efectos secundarios (imprimir, escribir ficheros, modificar un argumento) deja de serlo.

P: ¿Cuál es el gotcha de tipos hashables vs. unhashables al asignar? / R: Asignar un hashable (`b = a`) copia el valor; asignar un unhashable (`B = A`) hace que ambos nombres apunten al mismo objeto, por lo que modificar uno afecta al otro.

P: ¿Cuáles son las principales librerías técnicas de Python del ecosistema? / R: Pandas (central), NumPy (cimiento, arrays numéricos), Scikit-learn (machine learning), Matplotlib (visualización) y SciPy (operaciones numéricas avanzadas).

P: ¿Qué es un DataFrame de Pandas? / R: Una tabla con filas y columnas tipadas, similar a una tabla SQL o un data frame de R, con un index asociado (por defecto el número de fila).

P: ¿Qué es una Series en Pandas? / R: Una columna del DataFrame: un array de objetos del mismo tipo con un index asociado; sumar dos Series alinea por index.

P: ¿Para qué sirven `join()` y `groupby()` en Pandas? / R: `join()` combina dos data frames emparejando filas por index; `groupby()` agrupa filas por una propiedad y agrega cada grupo con agregados integrados (`mean()`) o funciones personalizadas vía `apply`.

## Preguntas de autoevaluación

P: ¿Por qué afirma el autor que todo científico de datos necesita dominar al menos un lenguaje de programación? / R: Porque nunca ha completado un proyecto solo con herramientas gráficas: siempre surge algo (un formato raro, datos que no caben en memoria, una feature poco convencional) que obliga a escribir código, y todas las herramientas gráficas asumen datos ya tabulares. (Sección: ¿Por qué usar un lenguaje de programación?)

P: ¿Qué significa que la ciencia de datos sea "Turing complete" en el flujo de trabajo descrito? / R: Que muchos trabajan íntegramente en lenguajes de programación apoyados en librerías numéricas, mientras otros hacen el data wrangling y la extracción de features en código y luego cargan los datos en otra herramienta para el análisis. (Sección: ¿Por qué usar un lenguaje de programación?)

P: ¿Qué limitación comparten MATLAB/Octave, SAS y Scala según el recorrido de lenguajes? / R: MATLAB es propietario (Octave es su versión open-source sin toda la funcionalidad), SAS es propietario de los años 60 muy ajeno y no recomendado para ciencia de datos general, y Scala aún carece de soporte suficiente de librerías de analítica y visualización. (Sección: Un recorrido por los lenguajes)

P: ¿Qué reglas gobiernan la indentación y el slicing de strings en Python? / R: La indentación debe ser consistente (cuatro espacios o tabs, sin mezclar); el slicing usa corchetes con índices que empiezan en 0 y admite índices negativos, p. ej. `"ABCD"[1:3]` da `'BC'` y `"ABCD"[:-1]` da `'ABC'`. (Secciones: Tipos atómicos y strings)

P: ¿Cómo se copia de verdad una lista para evitar el gotcha de los unhashables? / R: Con una list comprehension como `B = [x for x in A]`, aunque los elementos unhashables internos seguirían compartidos; las claves de un dict deben ser hashables. (Sección: Funciones, control de flujo y clases)

P: ¿Qué papel cumplen `__init__` y `self` en una clase de Python? / R: `__init__` es el constructor y `self` (equivalente al `this` de C++) debe pasarse explícitamente como primer argumento de cada método para referirse a la instancia. (Sección: Funciones, control de flujo y clases)

P: ¿Por qué se dice que NumPy es el cimiento pero el trabajo real se hace en Pandas? / R: NumPy provee arrays numéricos rápidos y de bajo nivel que son la base de todo lo demás, pero la mayoría del trabajo real se hace en Pandas por su API intuitiva sobre data frames. (Sección: Librerías técnicas de Python y Pandas)

## Puntos a dominar

- Argumentar por qué un lenguaje de programación es imprescindible frente a herramientas gráficas que asumen datos tabulares.
- Situar los principales lenguajes (Python, R, MATLAB/Octave, SAS, Scala) y sus fortalezas y limitaciones.
- Reconocer las diferencias clave entre Python 2.7 (asumido por el libro) y 3.x: `print`, división y strings/Unicode.
- Identificar los cinco tipos atómicos (int, float, bool, string, NoneType) y los contenedores clave (listas, tuplas, dicts, sets).
- Aplicar slicing con índices desde 0 e índices negativos, y respetar la indentación consistente.
- Distinguir funciones puras de las que tienen efectos secundarios, y usar argumentos opcionales y lambdas.
- Explicar el gotcha de hashables (copia por valor) vs. unhashables (referencia compartida) y cómo copiar de verdad.
- Operar con Pandas: DataFrame, Series, columnas derivadas, filtrado, `apply`, `join()` y `groupby()`.
