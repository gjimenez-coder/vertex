# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 21 — Performance and Computer Memory (Rendimiento y memoria del computador)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo trata de cómo hacer que tu código corra más rápido, y se divide en dos temas distintos. El primero es la teoría de cuán rápido es un algoritmo en abstracto, independiente del computador o de la implementación: basta con entender lo suficiente para evitar unos pocos errores potencialmente catastróficos. El segundo son optimizaciones concretas, que en su mayoría consisten en hacer buen uso de la memoria y la caché del computador.

La tesis central es doble. La notación Big-O te dice cómo crece el número de pasos de un algoritmo en función del tamaño de la entrada, no cuánto tarda cada paso; sirve para asegurar que tu código escala y evitar decisiones de diseño desastrosas (sobre todo un O(n²) sobre todo el dataset). Una vez elegido un buen algoritmo, las mejoras de rendimiento reales vienen de dos principios: reducir overhead y gestionar bien la memoria (RAM, caché y la jerarquía de memoria).

Sales sabiendo analizar la complejidad de algoritmos clásicos (búsqueda lineal, búsqueda binaria, ordenamiento), distinguir el peor caso del rendimiento amortizado y promedio, y aplicar consejos prácticos de rendimiento en Python: usar librerías numéricas, borrar estructuras grandes, usar funciones integradas, evitar llamadas superfluas y evitar crear objetos grandes nuevos.

## El ejemplo que recorre el capítulo

El hilo conductor es contar cuántas entradas de una lista están duplicadas, resuelto de dos formas. La primera recorre cada elemento `x` y cuenta sus ocurrencias con `lst.count(x)`, lo que obliga a recorrer toda la lista para cada elemento: n² comparaciones, es decir O(n²). La segunda mantiene un diccionario que mapea elementos a su número de ocurrencias y lo actualiza en un solo recorrido; como consultar y actualizar un diccionario es O(1), el total es O(n).

```python
def duplicates_On2(lst):
    ct = 0
    for x in lst:
        if lst.count(x) > 1: ct += 1
    return ct

def duplicates_On(lst):
    cts = {}
    for x in lst:
        if cts.has_key(x): cts[x] += 1
        else: cts[x] = 1
    return sum([ct for x, ct in cts.items() if ct > 1])
```

Al cronometrar ambos sobre listas de distinta longitud, con listas cortas son comparables (a veces O(n²) es mejor por una implementación ineficiente del O(n)), pero al crecer la lista se abre una brecha y O(n²) se vuelve mucho más lento. Esto no depende del computador ni de Python: es un algoritmo fundamentalmente mejor.

## Rendimiento de algoritmos y notación Big-O

Big-O es la forma estándar de hablar del rendimiento teórico de un algoritmo en abstracto. Que un algoritmo sea O(n²) significa que, en el límite de entradas grandes, su tiempo de ejecución es aproximadamente una constante por n²; O(n) significa una constante por n. Dos ideas clave: (1) cuánto tarda el código realmente depende de muchos otros factores (la máquina, la eficiencia de cada paso), y (2) en el límite de entradas grandes, las diferencias de Big-O dominan el tiempo de ejecución. Big-O no dice nada de cuánto tarda un paso, pero sí cómo crece el número de pasos con el tamaño de la entrada.

Al rendimiento Big-O se le llama a menudo "complejidad", un término desafortunado: el número de pasos no tiene que ver con lo complicados que sean esos pasos (de hecho, los algoritmos menos "complejos" suelen ser los más complicados de entender). Regla práctica: tu código de ciencia de datos nunca debería tener un algoritmo O(n²) operando sobre todo el dataset, salvo que lo quieras deliberadamente. Las operaciones básicas de las librerías mostradas tienen buen rendimiento asintótico, así que es raro caer en un O(n²) por accidente, pero cuando ocurre es desastroso.

## Problemas clásicos: ordenar una lista y búsqueda binaria

Buscar un elemento `x` en una lista de longitud n recorriéndola entera es O(n). Si la lista está ordenada, la búsqueda binaria es mucho más eficiente: en cada iteración la distancia entre los índices `i` y `j` se divide entre 2. Si T(n) es el tiempo, cada expansión añade un O(1) hasta que el tamaño es O(1), lo que ocurre tras log₂(n) pasos; por tanto la búsqueda binaria es O(log(n)), muchísimo más rápida que O(n) para n grande.

Para ordenar, el método obvio (extraer repetidamente el mínimo) recorre una lista de tamaño n, luego n−1, etc., sumando n(n+1)/2 operaciones: tiempo cuadrático O(n²), señal de que hay algo mejor. MergeSort divide la lista en dos mitades, las ordena recursivamente y luego las fusiona. La fusión (Merge) es O(n); la recurrencia T(n) = O(n) + 2·T(n/2) se expande hasta que n/2^k ≈ 1, es decir k ≈ log₂(n), dando un total O(n·log(n)).

## Rendimiento amortizado y rendimiento promedio

Una limitación de Big-O es que es rendimiento del peor caso. A veces la complejidad Big-O es mala pero el tiempo observado escala bien. El caso más simple son algoritmos aleatorizados deliberadamente: QuickSort elige un elemento al azar como pivote, parte la lista en menores y mayores y ordena recursivamente. Es O(n²) en el peor caso (si siempre eligiera el mayor), pero O(n·log(n)) en promedio, y suele ser aún mejor que MergeSort.

El otro matiz es el análisis amortizado, relevante cuando se hacen muchas operaciones que modifican una estructura de datos. No siempre se logra que todas sean O(1), pero sí que en promedio salgan lineales. Ejemplo: los diccionarios de Python. Añadir un elemento suele ser O(1), pero al llenarse la estructura interna (un hash map) hay que reorganizar los datos, lo que es O(n). Esas reorganizaciones se vuelven más costosas pero también más raras, de modo que el promedio sobre muchos cambios es O(1).

## Dos principios: reducir overhead y gestionar la memoria

Más allá de Big-O, el computador y las herramientas que usas pueden determinar si tu código corre lo bastante rápido para ser útil. Los consejos del capítulo caen en dos categorías: (1) reducir overhead, esas pequeñas penalizaciones que incurre cada operación y que se acumulan dentro de un bucle; y (2) hacer mejor uso de la memoria y la caché. Según el autor, los problemas de memoria suelen pesar más en ciencia de datos que el overhead.

La memoria (RAM, "random access memory") se llama así porque el computador accede a cualquier región igual de rápido (del orden de 100 nanosegundos por byte), no por nada aleatorio. La RAM es finita: si fuerzas más datos de los que caben, el programa falla o el sistema operativo recurre al "paging" (mover datos entre RAM y disco), una operación lentísima. Primer principio: no ocupar demasiada memoria.

Dentro de la RAM no todo es igual. El computador guarda una copia de parte de la RAM en la caché, memoria con lectura/escritura mucho más rápida (alrededor de un orden de magnitud). Al leer un byte, busca primero en la caché; si no está, ocurre un "cache miss" y recurre a la RAM. Suele haber varios niveles de caché, cada uno más pequeño y rápido. RAM, disco y niveles de caché forman la "jerarquía de memoria": cada capa es más rápida pero más pequeña que la de abajo. Cuánto se encuentra el dato en los niveles altos suele ser el factor individual más importante del rendimiento.

## Consejos de rendimiento

Usar librerías numéricas cuando aplique: operar sobre arrays de NumPy (directamente o vía Pandas) es mucho más eficiente que sobre objetos Python. Dos factores: Python no sabe hasta runtime que un número es entero y debe comprobar el tipo en cada operación (overhead constante); y la estructura de Python ocupa mucho más espacio porque carga metadatos de tipo, llenando antes los niveles altos de caché, por lo que empeora en listas largas.

Borrar estructuras grandes que no necesitas: todos los objetos creados compiten por espacio en la caché. Liberar los que ya no sirven ("garbage collection") deja subir en la jerarquía a los que sí necesitarás. Python recolecta algo automáticamente, pero es conservador; puedes liberar mucho con `del my_object`.

Usar funciones integradas cuando sea posible: las built-in de Python están escritas en C eficiente y solo incurren el coste único de llamar a una función. Sumar con `sum(l)` en lugar de un bucle es, en el ejemplo del autor, unas 14 veces más rápido.

Evitar llamadas de función superfluas: cada llamada tiene overhead. Recorrer una lista llamando a una función para sumar tarda unas 2 veces más que sumar en línea dentro del bucle.

Evitar crear objetos grandes nuevos: `myList = myList + [1, 2, 3]` crea una lista nueva, copia todo y borra la vieja (O(n)); `myList.extend([1,2,3])` logra lo mismo en O(1) amortizado.

## Ideas clave

- Big-O describe cómo crece el número de pasos con el tamaño de la entrada, no cuánto tarda cada paso; en el límite de entradas grandes domina el tiempo de ejecución.
- Evita algoritmos O(n²) sobre todo el dataset salvo que lo quieras deliberadamente: son desastrosos a gran escala.
- Búsqueda lineal O(n); búsqueda binaria sobre lista ordenada O(log(n)); ordenamiento ingenuo O(n²); MergeSort O(n·log(n)).
- QuickSort es O(n²) en el peor caso pero O(n·log(n)) en promedio; el análisis amortizado explica por qué añadir a un diccionario es O(1) de media pese a reorganizaciones O(n).
- Dos principios de rendimiento práctico: reducir overhead y gestionar la memoria (RAM, caché y jerarquía de memoria); encontrar el dato en niveles altos de caché es clave.
- En Python: usa NumPy/Pandas, borra con `del` lo que no necesites, prefiere funciones integradas en C, evita llamadas superfluas y usa `extend` en vez de crear listas nuevas.
