# Performance and Computer Memory (Rendimiento y memoria del computador) — Estudio

## Tarjetas de repaso

P: ¿Qué describe la notación Big-O?
R: Cómo crece el número de pasos de un algoritmo en función del tamaño de la entrada, no cuánto tarda cada paso.

P: ¿Qué significa que un algoritmo sea O(n²) frente a O(n)?
R: O(n²) significa que, en el límite de entradas grandes, su tiempo es aproximadamente una constante por n²; O(n) es una constante por n.

P: ¿Por qué "complejidad" es un término desafortunado para el rendimiento Big-O?
R: Porque el número de pasos no tiene que ver con lo complicados que sean esos pasos; los algoritmos menos "complejos" suelen ser los más complicados de entender.

P: ¿Cuál es la regla práctica sobre O(n²) en ciencia de datos?
R: Tu código nunca debería tener un algoritmo O(n²) operando sobre todo el dataset, salvo que lo quieras deliberadamente.

P: ¿Cuál es la complejidad de la búsqueda lineal y de la búsqueda binaria?
R: Búsqueda lineal O(n); búsqueda binaria sobre una lista ordenada O(log(n)), porque cada iteración divide entre 2 la distancia entre índices.

P: ¿Por qué el ordenamiento ingenuo (extraer repetidamente el mínimo) es O(n²)?
R: Recorre una lista de tamaño n, luego n−1, etc., sumando n(n+1)/2 operaciones, lo que da tiempo cuadrático.

P: ¿Cómo funciona MergeSort y cuál es su complejidad?
R: Divide la lista en dos mitades, las ordena recursivamente y las fusiona (Merge es O(n)); la recurrencia da un total O(n·log(n)).

P: ¿Cuál es la complejidad de QuickSort en el peor caso y en promedio?
R: O(n²) en el peor caso (si siempre eligiera el mayor como pivote) pero O(n·log(n)) en promedio.

P: ¿Qué es el análisis amortizado y qué ejemplo lo ilustra?
R: Que operaciones individuales pueden ser costosas pero en promedio salen lineales; añadir a un diccionario de Python es O(1) de media pese a reorganizaciones O(n) cada vez más raras.

P: ¿Cuáles son los dos principios del rendimiento práctico más allá de Big-O?
R: Reducir overhead (pequeñas penalizaciones que se acumulan en bucles) y gestionar bien la memoria (RAM, caché y jerarquía de memoria).

P: ¿Por qué se llama RAM a la memoria y qué pasa si se llena?
R: Porque el computador accede a cualquier región igual de rápido (unos 100 nanosegundos por byte); si se fuerzan más datos de los que caben, el programa falla o el SO recurre al paging (lentísimo).

P: ¿Qué es un cache miss y qué es la jerarquía de memoria?
R: Un cache miss ocurre cuando el dato no está en la caché y hay que ir a la RAM; la jerarquía de memoria (RAM, disco, niveles de caché) tiene capas más rápidas pero más pequeñas conforme se sube.

P: ¿Por qué operar con NumPy/Pandas es más eficiente que con objetos Python?
R: Python comprueba el tipo en cada operación (overhead) y sus objetos ocupan más espacio por los metadatos, llenando antes los niveles altos de caché.

P: ¿Qué ventaja tiene `myList.extend([1,2,3])` frente a `myList = myList + [1,2,3]`?
R: extend logra lo mismo en O(1) amortizado, mientras que la suma crea una lista nueva, copia todo y borra la vieja (O(n)).

## Preguntas de autoevaluación

P: Según el ejemplo del capítulo, ¿por qué contar duplicados con `lst.count(x)` dentro de un bucle es O(n²) y cómo se mejora a O(n)?
R: Porque `count` recorre toda la lista para cada elemento (n² comparaciones); se mejora usando un diccionario que mapea elementos a su número de ocurrencias en un solo recorrido, ya que consultar y actualizar un diccionario es O(1). (Sección: El ejemplo que recorre el capítulo)

P: Con listas cortas, ¿por qué a veces la versión O(n²) resulta más rápida que la O(n)?
R: Porque con entradas pequeñas ambas son comparables y la implementación del O(n) puede ser ineficiente; la brecha solo se abre al crecer la lista. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué dos ideas clave resume el autor sobre lo que Big-O sí dice y lo que no?
R: (1) Lo que tarda el código realmente depende de otros factores (máquina, eficiencia de cada paso); (2) en el límite de entradas grandes, las diferencias de Big-O dominan el tiempo de ejecución. (Sección: Rendimiento de algoritmos y notación Big-O)

P: ¿Por qué la búsqueda binaria es O(log(n))?
R: Porque en cada iteración la distancia entre los índices se divide entre 2, y hacen falta log₂(n) pasos hasta que el tamaño es O(1). (Sección: Problemas clásicos: ordenar una lista y búsqueda binaria)

P: ¿Qué limitación de Big-O motiva el rendimiento amortizado y el promedio?
R: Que Big-O es rendimiento del peor caso; a veces la complejidad es mala pero el tiempo observado escala bien, como en QuickSort o en las inserciones en diccionarios. (Sección: Rendimiento amortizado y rendimiento promedio)

P: ¿Cuál es, según el autor, el factor individual más importante del rendimiento una vez elegido el algoritmo?
R: Cuánto se encuentra el dato en los niveles altos de la jerarquía de memoria (la caché). (Sección: Dos principios: reducir overhead y gestionar la memoria)

P: ¿Por qué conviene borrar estructuras grandes con `del` y usar funciones integradas?
R: Porque todos los objetos compiten por la caché y liberar los inútiles deja subir a los necesarios; las built-in están en C eficiente y solo cuestan la llamada única (p. ej. `sum(l)` es ~14 veces más rápido que un bucle). (Sección: Consejos de rendimiento)

## Checklist

- Evitar cualquier algoritmo O(n²) que opere sobre todo el dataset salvo que sea deliberado.
- Usar diccionarios/estructuras O(1) para contar u ordenar accesos en lugar de recorrer la lista por cada elemento.
- Preferir búsqueda binaria sobre listas ordenadas y algoritmos O(n·log(n)) (MergeSort, QuickSort) frente a ordenamientos ingenuos O(n²).
- No ocupar demasiada memoria para evitar fallos o paging entre RAM y disco.
- Operar sobre arrays de NumPy (directamente o vía Pandas) en vez de objetos Python en datasets grandes.
- Liberar estructuras grandes que ya no se necesitan con `del my_object`.
- Usar funciones integradas de Python (p. ej. `sum`) en lugar de bucles manuales.
- Evitar llamadas de función superfluas dentro de bucles.
- Usar `myList.extend([...])` en vez de `myList = myList + [...]` para no crear objetos grandes nuevos.
