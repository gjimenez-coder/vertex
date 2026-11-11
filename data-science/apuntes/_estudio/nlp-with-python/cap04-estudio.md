# Writing Structured Programs (Escribir programas estructurados) — Estudio

## Tarjetas de repaso

P: ¿Qué copia la asignación cuando el valor es un objeto estructurado como una lista? / R: Copia una referencia al objeto, no el objeto en sí; por eso `b = a` sobre listas hace que ambas apunten al mismo objeto y modificar una afecte a la otra.

P: ¿Cómo se copian los elementos de una lista sin compartir referencia? / R: Con `bar = foo[:]`; para estructuras anidadas sin referencias compartidas, con `copy.deepcopy()`.

P: ¿Qué problema tiene `nested = [[]] * 3`? / R: Crea tres referencias a un mismo objeto, así que modificarlo in situ cambia los tres elementos; reasignar uno solo sustituye su referencia sin tocar los demás.

P: ¿Qué diferencia hay entre `is` y `==`? / R: `is` prueba la identidad de objeto (si son el mismo objeto); `==` prueba la equivalencia de valor. La distinción refleja la de tipo-token (type-token).

P: ¿Cómo evalúa un `if` una cadena o lista vacía frente a una no vacía? / R: Una secuencia no vacía evalúa como verdadera y una vacía como falsa, así que no hace falta escribir `if len(element) > 0`.

P: ¿Cuándo usar una tupla y cuándo una lista? / R: Tupla cuando la interpretación de un elemento depende de su posición (p. ej. `('grail', 'noun')`, registro de tipos distintos y longitud fija); lista cuando la posición no importa (secuencia de objetos del mismo tipo y longitud arbitraria). Las listas son mutables y las tuplas inmutables.

P: ¿Qué es una expresión generadora y por qué puede ser más eficiente? / R: Es una comprensión sin corchetes pasada a otra función (p. ej. `max(w.lower() for w in nltk.word_tokenize(text))`); transmite los datos en flujo a la función en lugar de almacenar antes toda la lista.

P: ¿Qué diferencia el estilo procedimental del declarativo? / R: El procedimental usa variables acumuladoras paso a paso (`count`, `total`) sin significado hasta el final; el declarativo usa funciones integradas y cada línea realiza una tarea completa, p. ej. `total = sum(len(t) for t in tokens)`, resultando más compacto y legible.

P: ¿Cuál es la regla LGB para resolver nombres? / R: Al resolver un nombre se busca primero en el ámbito local, luego en el global del módulo y luego en el integrado (built-in).

P: ¿Qué regla de diseño debe cumplir una función respecto a su argumento y su valor de retorno? / R: Debe modificar su argumento o devolver un valor, pero no ambas cosas (como hace la peligrosa `my_sort3()`).

P: ¿Cómo programar a la defensiva ante un tipo incorrecto en lugar de devolver `None`? / R: Usar `assert isinstance(word, basestring), "..."`, que detiene la ejecución con un mensaje claro si falla; devolver `None` es peligroso porque puede propagarse.

P: ¿Qué hace `yield` en una función generadora? / R: Pausa la función en cada `yield` y la reanuda cuando la llamada pide el siguiente valor, siendo más eficiente en memoria que una función acumulativa.

P: ¿En qué consiste la programación dinámica? / R: Se usa cuando un problema tiene subproblemas solapados: en vez de recalcularlos, se guardan en una tabla de consulta (p. ej. las variantes `virahanka2/3/4` de la métrica sánscrita).

P: ¿Por qué usar un `set` en vez de una `list` para pruebas de pertenencia? / R: Un `set` indexa sus elementos; con `timeit`, 1.000 pruebas tardan 2,8 s en una lista frente a 0,0037 s en un conjunto (tres órdenes de magnitud más rápido).

P: ¿Qué recomienda PEP 8 sobre la sangría y la longitud de línea? / R: Cuatro espacios por nivel de sangría (evitar tabuladores), líneas de menos de 80 caracteres y romper líneas largas dentro de paréntesis/corchetes/llaves o con barra invertida final; su valor rector es la consistencia.

## Preguntas de autoevaluación

P: Si `foo` es una lista y haces `bar = foo`, ¿qué ocurre al modificar `bar` in situ, y cómo lo evitarías? / R: `foo` también cambia porque ambas variables apuntan al mismo objeto; se evita copiando con `foo[:]` o `copy.deepcopy()`. (Sección "Volver a lo básico")

P: ¿Por qué `is` y `==` pueden dar resultados distintos y qué distinción lingüística reflejan? / R: `is` compara identidad de objeto y `==` compara valor, así que dos objetos iguales en valor pueden no ser el mismo objeto; reflejan la distinción tipo-token. (Sección "Volver a lo básico")

P: ¿Qué ventajas aporta reescribir un bucle procedimental en estilo declarativo? / R: Cada línea realiza una tarea completa y comprensible, el código es más compacto y legible (p. ej. `word_list = sorted(set(tokens))`), equilibrando eficiencia del programa y del programador. (Sección "Cuestiones de estilo")

P: ¿Cuándo está justificado usar una variable de bucle con contador manual? / R: Para extraer n-gramas solapados (`[sent[i:i+n] for i in range(len(sent)-n+1)]`) o construir estructuras multidimensionales con comprensiones anidadas; ahí no debe usarse multiplicación por el problema de copia de referencias. (Sección "Cuestiones de estilo")

P: ¿Qué beneficios aporta empaquetar varios pasos en una función con nombre significativo? / R: Ahorra espacio, aporta interpretación semántica, mejora la legibilidad y la fiabilidad al reutilizar código ya probado; el docstring documenta su propósito y es accesible con `help()`. (Sección "Funciones: el fundamento de la programación estructurada")

P: ¿Por qué debe evitarse un objeto mutable como valor por defecto de un parámetro? / R: Porque se crea una sola vez al cargar la función y se comparte entre llamadas, generando un bug sobre la semántica de Python. (Secciones "Más cosas con funciones" y "Desarrollo de programas")

P: ¿Qué pasos sigue la depuración cuando un error nace de suposiciones incorrectas? / R: Comprobar las suposiciones: localizar el problema con `print`, reducir la entrada al mínimo que reproduce el error, recrearlo en la línea interactiva y explicar el código a otra persona; también existe `pdb` con breakpoints y `step`/`next`. (Sección "Desarrollo de programas")

P: ¿Qué compromiso representa construir un índice auxiliar como un `set` o identificadores enteros? / R: Un compromiso espacio-tiempo: se usa más memoria en una estructura auxiliar para acelerar la ejecución, como el sistema de recuperación del Movie Reviews Corpus o las pruebas de pertenencia en un `set`. (Sección "Diseño de algoritmos")

## Puntos a dominar

- Entender que la asignación y el paso de parámetros usan referencias de objeto, y saber copiar con `foo[:]` o `copy.deepcopy()` cuando no quieras compartir estado.
- Distinguir `is` (identidad) de `==` (valor) y reconocer la distinción tipo-token.
- Elegir entre cadena, lista y tupla según mutabilidad y según si la posición del elemento determina su interpretación.
- Preferir el estilo declarativo: `sorted(set(...))`, `sum(... for ...)`, `enumerate()`, comprensiones y expresiones generadoras frente a contadores manuales.
- Diseñar funciones con propósito claro, docstring, paso de parámetros entendido, regla LGB para el ámbito, y la regla de modificar el argumento o devolver un valor, no ambos.
- Aplicar programación defensiva: piezas pequeñas comprobadas, `assert isinstance(...)`, pruebas de regresión con `doctest` e interfaces documentadas.
- Conocer las técnicas de diseño de algoritmos: divide y vencerás, recursión con caso base, compromisos espacio-tiempo y programación dinámica (bottom-up, top-down y `memoize`).
- Reconocer las fuentes de error (datos de entrada, función que no se comporta como se espera, semántica de Python) y las bibliotecas útiles: Matplotlib, NetworkX, `csv` y NumPy.
