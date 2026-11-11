# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 4 — Writing Structured Programs (Escribir programas estructurados)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF, por ejemplo (PDF p. N).

## Lo que necesitas saber

Este capítulo deja de organizar el contenido según las necesidades del NLP y vuelve a un enfoque convencional, ligado a la estructura del propio lenguaje Python. Su objetivo es que escribas programas bien estructurados, legibles y reutilizables, que entiendas a fondo los bloques de construcción básicos (asignación, bucles, funciones) y que evites las trampas típicas de Python.

La tesis central es que programar es tanto un arte como una ciencia: la legibilidad y la fiabilidad del código importan tanto como que funcione. Para lograrlo conviene preferir un estilo declarativo sobre uno procedimental, descomponer el código en funciones con propósito claro, documentarlas y adoptar hábitos de programación defensiva.

Sales sabiendo cómo funciona la asignación por referencia de objetos, la diferencia entre `is` y `==`, cómo usar secuencias (cadenas, listas, tuplas) y expresiones generadoras, cómo diseñar y documentar funciones, cómo depurar y estructurar programas en módulos, y nociones de diseño de algoritmos (recursión, programación dinámica, compromisos espacio-tiempo). Cierra con un repaso de bibliotecas Python útiles para datos lingüísticos.

## Volver a lo básico

Asignación. La asignación siempre copia el valor de una expresión, pero el valor de un objeto estructurado (como una lista) es una referencia al objeto, no una copia. Por eso, con cadenas `bar = foo` crea una copia independiente, pero con listas ambas variables apuntan al mismo objeto en memoria, y modificar una afecta a la otra (PDF p. 152). Esto se extiende al paso de parámetros. Para copiar los elementos de una lista usa `bar = foo[:]`; para copiar una estructura sin compartir referencias usa `copy.deepcopy()`.

Un caso ilustrativo son las listas anidadas creadas por multiplicación: `nested = [[]] * 3` produce tres referencias a un mismo objeto, de modo que modificarlo in situ cambia los tres elementos, mientras que reasignar uno solo sustituye su referencia sin tocar los demás. La función `id()` permite verificar la identidad numérica de cada objeto.

Igualdad. Python ofrece dos comprobaciones: `is` prueba la identidad de objeto (si son el mismo objeto) y `==` prueba la equivalencia de valor. Tener dos clases de igualdad refleja la distinción tipo-token (type-token) familiar en el lenguaje natural.

Condicionales. En la condición de un `if`, una cadena o lista no vacía evalúa como verdadera y una vacía como falsa, así que no hace falta escribir `if len(element) > 0`. Un `elif` aporta más información que un `if` suelto: al cumplirse indica que la condición principal no se cumplió. Las funciones `all()` y `any()` comprueban si todos o algunos elementos de una secuencia cumplen una condición.

## Secuencias

Además de cadenas y listas, existe la tupla, que se forma con el operador coma (habitualmente entre paréntesis) y puede tener cualquier número de miembros. Las tres se pueden indexar, segmentar (slicing) y medir con `len()`. Una tupla de un solo elemento necesita coma final (`'snark',`) y la tupla vacía es `()`. Varias expresiones separadas por comas en una línea son, de hecho, tuplas.

Se puede iterar sobre una secuencia `s` de muchas formas: `for item in sorted(s)`, `set(s)`, `reversed(s)`, `set(s).difference(t)`, etc., y combinarlas, como `reversed(sorted(set(s)))`. Se convierte entre tipos con `tuple(s)`, `list(s)` y `':'.join(words)`. Objetos como un `FreqDist` admiten `list()` e iteración.

Las tuplas permiten reordenar elementos de forma idiomática, intercambiando varios valores en una sola línea sin variable temporal:

```python
words[2], words[3], words[4] = words[3], words[4], words[2]
```

Otras funciones modifican la estructura de las secuencias: `zip()` empareja los elementos de dos o más secuencias, y `enumerate(s)` devuelve pares índice-elemento. Para dividir datos (por ejemplo, 90% entrenamiento y 10% prueba) se calcula el punto de corte y se usa slicing: `training_data, test_data = text[:cut], text[cut:]`.

Combinando los tres tipos con listas por comprensión se pueden ordenar palabras por longitud construyendo tuplas `(longitud, palabra)`, ordenándolas y descartando luego la longitud. Esto revela sus roles distintos: las cadenas suelen aparecer en la entrada y la salida; una lista es una secuencia de objetos del mismo tipo y longitud arbitraria (p. ej. palabras); una tupla es una colección de objetos de distinto tipo y longitud fija (un registro). Una buena regla: usa tuplas cuando la interpretación de un elemento depende de su posición, como en `('grail', 'noun')`; usa listas cuando la posición no importa, como en `['venetian', 'blind']` (PDF p. 159).

Hay además una diferencia fundamental: las listas son mutables y las tuplas inmutables. Operaciones como `sort()`, asignación por índice o `del` solo funcionan sobre listas.

Expresiones generadoras. Al pasar una comprensión a otra función, Python permite omitir los corchetes, obteniendo una expresión generadora: `max(w.lower() for w in nltk.word_tokenize(text))`. Esto no es solo conveniencia notacional: en muchos casos es más eficiente, porque los datos se transmiten en flujo a la función que llama en lugar de almacenar antes toda la lista.

## Cuestiones de estilo

Como el código lo leen personas y no solo máquinas, el estilo importa. Python publica una guía de estilo (PEP 8), cuyo valor rector es la consistencia para maximizar la legibilidad. Recomienda cuatro espacios por nivel de sangría (evita tabuladores, que distintos editores interpretan mal), líneas de menos de 80 caracteres, y romper líneas largas dentro de paréntesis/corchetes/llaves o con una barra invertida final.

Estilo procedimental frente a declarativo. El estilo procedimental dicta operaciones paso a paso con variables acumuladoras que son como registros de la CPU (`count`, `total`), con valores intermedios sin significado hasta el final. El estilo declarativo usa funciones integradas y cada línea realiza una tarea completa y comprensible; por ejemplo, `total = sum(len(t) for t in tokens)` en lugar de un bucle manual. Resulta más compacto y legible: `word_list = sorted(set(tokens))` sustituye a un largo bucle anidado. En lugar de contadores manuales conviene usar `enumerate()`, y para hallar el máximo o mínimo, comprensiones como `max(len(word) for word in text)`. Hay que equilibrar la eficiencia del programa con la eficiencia del programador: una solución rápida pero críptica es más difícil de mantener.

Usos legítimos de contadores. A veces sí se necesita una variable de bucle: para extraer n-gramas solapados (`[sent[i:i+n] for i in range(len(sent)-n+1)]`; NLTK ofrece `bigrams()`, `trigrams()` y `ngrams()`), o para construir estructuras multidimensionales con comprensiones anidadas, como una matriz de conjuntos. Ahí no debe usarse multiplicación (`[[set()] * n] * m`) por el problema de copia de referencias ya visto.

## Funciones: el fundamento de la programación estructurada

Las funciones empaquetan y reutilizan código. Reunir varios pasos en una función con nombre significativo (p. ej. `get_text()`) ahorra espacio, aporta interpretación semántica, mejora la legibilidad y la fiabilidad (se reutiliza código ya probado). La primera cadena dentro de una definición es el docstring, que documenta el propósito y es accesible mediante `help()`.

Entradas y salidas. La información se pasa mediante parámetros; una función comunica resultados con `return`, de modo que a la llamada le parece que la llamada se sustituye por el resultado. No es obligatorio tener parámetros ni `return` (algunas funcionan por efecto secundario). Regla: una función debería modificar su argumento o devolver un valor, pero no ambas cosas (`my_sort3()` es peligrosa por hacer ambas).

Paso de parámetros. Python usa paso por valor (call-by-value), pero el valor de un objeto estructurado es una referencia. Así, reasignar un parámetro dentro de la función no afecta a la variable externa, pero modificar in situ el objeto referenciado sí. Entender el paso de parámetros se reduce a entender la asignación.

Ámbito de variables. Las definiciones de función crean un ámbito local; los nombres asignados dentro no son visibles fuera. Al resolver un nombre se aplica la regla LGB: primero local, luego global del módulo, luego integrado (built-in). Se puede crear una global con `global`, pero debe evitarse porque introduce dependencias de contexto y reduce la reutilización.

Comprobación de tipos. Python no obliga a declarar tipos, lo que da flexibilidad, pero conviene programar a la defensiva. Devolver `None` ante un tipo incorrecto es peligroso porque puede propagarse. Mejor usar `assert isinstance(word, basestring), "..."`, que detiene la ejecución con un mensaje claro si falla.

Descomposición funcional. Cuando un bloque supera las 10-20 líneas, conviene dividirlo en funciones con propósito claro, como los párrafos de un buen ensayo. Las funciones son una abstracción que permite escribir el programa principal a mayor nivel (`data = load_corpus(); results = analyze(data); present(results)`) y reimplementar una función sin tocar el resto. El ejemplo de `freq_words` se refactoriza para eliminar efectos secundarios: inicializar el `FreqDist` dentro y dejar la selección y visualización a la llamada.

Documentar funciones. El docstring debe describir qué hace la función, no cómo. Para funciones simples basta una línea; para las no triviales, un resumen de una frase, línea en blanco y descripción detallada. Puede incluir un bloque doctest comprobable automáticamente. NLTK usa el lenguaje de marcado epytext con campos como `@param`, `@type`, `@rtype` y `@raise`.

## Más cosas con funciones

Funciones como argumentos. Python permite pasar una función como argumento, abstrayendo la operación: `extract_property(len)` o `extract_property(last_letter)`. Los paréntesis solo se usan al invocar, no al tratar la función como objeto. Las expresiones lambda definen funciones anónimas en el sitio: `extract_property(lambda w: w[-1])`. También se pueden pasar funciones a `sorted()` para ordenar por un criterio propio.

Funciones acumulativas. Inicializan almacenamiento, iteran sobre la entrada y devuelven el resultado. Una alternativa es un generador, que usa `yield`: se pausa en cada `yield` y reanuda cuando la llamada pide el siguiente valor, siendo más eficiente en memoria. El ejemplo `permutations()` genera todas las permutaciones mediante recursión.

Funciones de orden superior. Python ofrece `filter(función, secuencia)`, que retiene los elementos para los que la función es verdadera, y `map(función, secuencia)`, que la aplica a cada elemento. Ambas tienen equivalentes con comprensiones de lista, que el libro prefiere por ser más legibles.

Argumentos con nombre. Cuando hay muchos parámetros, se pueden referir por nombre (keyword arguments) y darles valor por defecto, permitiendo cualquier orden y omisiones. Los parámetros sin nombre deben preceder a los nombrados. `*args` recoge los posicionales en una tupla y `**kwargs` los nombrados en un diccionario; `zip(*song)` ilustra el desempaquetado. Precaución: no usar un objeto mutable como valor por defecto, porque se comparte entre llamadas.

## Desarrollo de programas

Un módulo Python es simplemente un archivo `.py` que reúne definiciones y funciones relacionadas para facilitar su reutilización y abstracción; sirve como espacio de nombres. Se puede localizar el código de un módulo NLTK con la variable `__file__`. La estructura típica de un módulo es: comentarios de cabecera (título, autores, licencia), docstring de módulo, importaciones, variables globales y definiciones de funciones. Los nombres solo internos deben empezar por guion bajo (`_helper()`) para ocultarse en `from module import *`; `__all__` lista los nombres accesibles externamente. En programas multimódulo se localizan las tareas únicas en el programa principal y se mantienen aparte las comunes (carga, visualización) para reutilizarlas.

Fuentes de error. Los fallos (bugs) pueden venir de los datos de entrada (caracteres inesperados, como el synset `ph.d..n.01` que rompía `split('.')` y se resolvió con `rsplit('.', 2)`), de una función que no se comporta como se espera (un malentendido sobre WordNet, no un bug real) o de un error sobre la semántica de Python (precedencia de operadores, o el clásico valor por defecto mutable que se crea una sola vez al cargar la función, no en cada llamada).

Técnicas de depuración. Como los errores suelen venir de suposiciones incorrectas, lo primero es comprobar tus suposiciones: localiza el problema con `print`, reduce la entrada al mínimo que reproduce el error, recrea la situación en la línea interactiva y explica tu código a otra persona. Python ofrece el depurador `pdb`, con el que se fijan puntos de ruptura (breakpoints) y se recorre el código paso a paso con `step`/`next`, inspeccionando variables (`args`).

Programación defensiva. Construye el programa de abajo arriba a partir de piezas pequeñas ya comprobadas; añade `assert` para verificar propiedades; trata cada corrección como una hipótesis y predice su efecto antes de reejecutar; y mantén un conjunto de casos de prueba (pruebas de regresión), por ejemplo con el módulo `doctest`. La estrategia defensiva más importante es escribir código claro, con nombres significativos e interfaces bien documentadas.

## Diseño de algoritmos

Elegir el algoritmo adecuado depende de cómo escala cada alternativa con el tamaño de los datos. La estrategia más conocida es divide y vencerás: dividir un problema de tamaño n en dos de tamaño n/2, resolverlos y combinar (como Merge Sort o la búsqueda binaria). Otra es transformar el problema en uno ya conocido.

Recursión. Una función se simplifica llamándose a sí misma sobre instancias más fáciles del mismo problema, con un caso base. El factorial admite versión iterativa (`factorial1`) y recursiva (`factorial2`); contar el tamaño de la jerarquía de hipónimos de WordNet se hace recursivamente con `size1()` (más corto y claro) o iterativamente con `size2()` (por capas, más difícil de interpretar). La recursión también construye estructuras anidadas, como un trie de letras para indexar un léxico. Precaución: la recursión tiene coste, pues cada llamada apila estado, por lo que las soluciones iterativas suelen ser más eficientes.

Compromisos espacio-tiempo. Construir una estructura auxiliar (un índice) acelera la ejecución, como el sistema de recuperación de texto del Movie Reviews Corpus o la sustitución de tokens por identificadores enteros. Para comprobar pertenencia conviene almacenar el vocabulario como `set`, no como `list`: con el módulo `timeit`, 1.000 pruebas de pertenencia tardan 2,8 s en una lista frente a 0,0037 s en un conjunto, tres órdenes de magnitud más rápido (PDF p. 187).

Programación dinámica. Se usa cuando un problema tiene subproblemas solapados: en vez de recalcularlos, se guardan en una tabla de consulta. El ejemplo del métrica sánscrita (Pingala/Virahanka) muestra cuatro variantes: iterativa, dinámica ascendente (bottom-up, `virahanka2`), dinámica descendente (top-down, recursiva, `virahanka3`) y con el decorador `memoize` (`virahanka4`). Sin ella, calcular V2 se repetiría millones de veces para n grande.

## Una muestra de bibliotecas de Python

Python tiene cientos de bibliotecas de terceros que amplían su funcionalidad; NLTK es una de ellas. Para datos lingüísticos destacan: Matplotlib, que ofrece funciones de gráficos con interfaz estilo MATLAB y permite mostrar datos numéricos en forma gráfica (p. ej. un diagrama de barras de la frecuencia de verbos modales por género en el Brown Corpus), e incluso generar imágenes al vuelo con el backend `Agg` y `savefig()`. NetworkX define y manipula grafos (nodos y aristas) y, junto a Matplotlib, visualiza redes como la jerarquía de hipónimos de WordNet mediante un recorrido recursivo. La biblioteca `csv` lee y escribe archivos en formato CSV, devolviendo cada fila como lista de cadenas (los campos numéricos hay que convertirlos con `int()` o `float()`). NumPy aporta procesamiento numérico con un objeto array multidimensional y funciones de álgebra lineal, como la descomposición en valores singulares usada en el análisis semántico latente. El índice de paquetes (PyPI) permite buscar muchas otras bibliotecas.

## Ideas clave

- La asignación y el paso de parámetros en Python usan referencias de objeto: si `a` es una lista y `b = a`, cualquier operación in situ sobre `a` modifica `b`, y viceversa.
- `is` comprueba la identidad de objeto; `==` comprueba la equivalencia de valor. La distinción refleja la de tipo-token.
- Cadenas, listas y tuplas son secuencias con operaciones comunes (indexado, slicing, `len()`, `sorted()`, `in`); las listas son mutables y las tuplas inmutables.
- Un estilo declarativo produce código más compacto y legible; evita contadores de bucle manuales y usa `enumerate()` cuando necesites enumerar.
- Las funciones son una abstracción esencial: domina el paso de parámetros, el ámbito de variables (regla LGB) y los docstrings. Una función debe modificar su argumento o devolver un valor, no ambos.
- Las expresiones generadoras (`yield`) procesan datos en flujo y ahorran memoria; `filter()` y `map()` tienen equivalentes legibles con comprensiones.
- Programa a la defensiva: piezas pequeñas comprobadas, `assert`, pruebas de regresión con `doctest`, nombres claros e interfaces documentadas.
- La programación dinámica almacena resultados de cálculos previos para evitar recomputar subproblemas solapados; un `set` indexa sus elementos y acelera las pruebas de pertenencia frente a una `list`.
