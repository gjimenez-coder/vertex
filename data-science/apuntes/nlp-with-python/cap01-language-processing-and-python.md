# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 1 — Language Processing and Python (Procesamiento del lenguaje y Python)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El capítulo introduce el procesamiento de lenguaje natural (NLP) combinando dos estilos que se alternan: tareas lingüísticas motivadoras que se resuelven con NLTK sin explicar aún su mecánica, y repasos sistemáticos de los conceptos básicos de Python. La tesis es que con técnicas de programación sencillas aplicadas a grandes cantidades de texto ya se puede extraer información relevante sobre el estilo y el contenido de un texto.

Se trabaja sobre un conjunto de textos predefinidos que vienen con el libro (`text1`…`text9`: Moby Dick, Sense and Sensibility, Genesis, el corpus de discursos inaugurales, el corpus de chat, Monty Python, el Wall Street Journal, el corpus de anuncios personales y The Man Who Was Thursday). Sobre ellos se aprende a buscar palabras en contexto, medir vocabulario, calcular estadísticas simples y programar decisiones y bucles.

Al terminar sales sabiendo: usar el intérprete y NLTK; buscar con `concordance`, `similar`, `common_contexts` y gráficos de dispersión; contar tokens y tipos y medir diversidad léxica; definir funciones; manejar listas y cadenas con indexación y slicing; usar distribuciones de frecuencia, bigramas y colocaciones; escribir comprensiones de listas, condicionales y bucles. La parte final plantea los retos abiertos del NLP (desambiguación, resolución de pronombres, traducción automática, diálogo, inferencia textual) y sus límites actuales.

## Computar con el lenguaje: textos y palabras

El intérprete interactivo de Python funciona de inmediato como calculadora y responde al prompt `>>>`. La división con enteros trunca (`1/3`), y para división flotante estándar se usa `from __future__ import division`. Un error como terminar una instrucción en `+` produce un `SyntaxError`.

Tras instalar NLTK y sus datos (`nltk.download()`, colección *book*), se cargan los textos con `from nltk.book import *`. A partir de ahí se explora el texto más allá de leerlo:

```python
>>> text1.concordance("monstrous")   # cada aparición de la palabra en su contexto
>>> text1.similar("monstrous")       # palabras que aparecen en contextos parecidos
>>> text2.common_contexts(["monstrous", "very"])  # contextos compartidos por dos palabras
```

Un dato relevante: `monstrous` en Austen tiene connotaciones positivas y funciona como intensificador (como *very*), a diferencia de Melville. Esto muestra que el uso de una palabra depende del texto.

Otras herramientas de exploración:

- `text4.dispersion_plot([...])`: gráfico de dispersión léxica que muestra dónde aparece cada palabra a lo largo del texto (requiere NumPy y Matplotlib).
- `text3.generate()`: genera texto aleatorio que imita el estilo y vocabulario de la fuente.

Sobre el conteo de vocabulario, el capítulo fija dos definiciones clave: un *token* es cada aparición de una secuencia de caracteres, y el vocabulario de un texto es el conjunto de tokens distintos, obtenido con `set(text)`. Así, Genesis tiene 44.764 tokens pero solo 2.789 tipos distintos. La diversidad léxica se mide dividiendo tokens entre tipos:

```python
>>> len(text3) / len(set(text3))   # 16.05 -> cada palabra aparece 16 veces de media
```

Para evitar reescribir fórmulas se define una *función* con `def`, asociando un nombre a un bloque de código. Los parámetros son marcadores de los datos reales; la función se *llama* pasándole *argumentos* entre paréntesis:

```python
>>> def lexical_diversity(text):
...     return len(text) / len(set(text))
>>> def percentage(count, total):
...     return 100 * count / total
```

El intérprete cambia el prompt a `...` tras los dos puntos para pedir un bloque indentado (cuatro espacios). La tabla de diversidad léxica del Brown Corpus (Tabla 1-1) ilustra que una misma función se reutiliza por filas con datos distintos.

## Un vistazo a Python: textos como listas de palabras

Un texto se representa como una *lista* de palabras y signos entre corchetes: `sent1 = ['Call', 'me', 'Ishmael', '.']`. Sobre listas se aplican `len()`, `set()`, `sorted()` y la propia `lexical_diversity()`. El operador `+` concatena listas en una sola, y `append()` añade un elemento modificando la lista original.

Indexación y slicing acceden a posiciones por su orden, empezando en cero:

```python
>>> text4[173]            # palabra en el índice 173
>>> text4.index('awaken') # índice de la primera aparición
>>> text5[16715:16735]    # sublista (slice)
```

Puntos importantes sobre índices: `sent[0]` es el primer elemento; un índice demasiado grande da un `IndexError` (error de ejecución, no de sintaxis); en un slice `m:n` se incluyen los elementos `m…n-1`; se puede omitir el primer número (`sent[:3]`) o el último (`text2[141525:]`). También se puede reasignar un elemento o un slice completo, lo que puede cambiar la longitud de la lista.

Las *variables* se crean con `variable = expresión` (asignación: la información va de derecha a izquierda). El nombre debe empezar por letra, admite dígitos y guiones bajos, distingue mayúsculas de minúsculas y no puede ser una palabra reservada (`def`, `if`, `not`, `import`…). Conviene usar nombres significativos y variables intermedias para hacer legible el código.

Las *cadenas* comparten operaciones con las listas: indexación (`name[0]`), slicing (`name[:4]`), multiplicación (`name * 2`) y suma (`name + '!'`). Se pasa de lista a cadena y viceversa con:

```python
>>> ' '.join(['Monty', 'Python'])   # 'Monty Python'
>>> 'Monty Python'.split()          # ['Monty', 'Python']
```

## Computar con el lenguaje: estadísticas simples

Una *distribución de frecuencias* (`FreqDist`) registra cuántas veces aparece cada tipo. Sirve para buscar automáticamente las palabras más informativas:

```python
>>> fdist1 = FreqDist(text1)
>>> fdist1.keys()[:50]   # 50 tipos más frecuentes
>>> fdist1['whale']      # 906
```

Las 50 palabras más frecuentes de Moby Dick cubren casi la mitad del libro, pero casi todas son "fontanería" del inglés; solo `whale` es informativa. Los *hapaxes* (palabras que aparecen una sola vez) tampoco ayudan por ser demasiados y sin contexto. La selección fina combina longitud y frecuencia, inspirándose en la notación de conjuntos `{ w | w ∈ V & P(w)}`:

```python
>>> fdist5 = FreqDist(text5)
>>> sorted([w for w in set(text5) if len(w) > 7 and fdist5[w] > 7])
```

Esto sí identifica palabras largas y frecuentes que cargan contenido.

Una *colocación* es una secuencia de palabras que aparecen juntas con una frecuencia inusual y resisten la sustitución por sinónimos (*red wine*, no *maroon wine*). Se parte de los *bigramas* (pares de palabras) y `collocations()` encuentra los bigramas más frecuentes de lo esperado dadas las frecuencias individuales. Los resultados son muy específicos del género de cada texto.

También se pueden contar otras cosas, como la distribución de longitudes de palabra:

```python
>>> fdist = FreqDist([len(w) for w in text1])
>>> fdist.max()   # 3 -> la longitud más frecuente
```

La Tabla 1-2 resume métodos de `FreqDist`: `inc`, `freq`, `N`, `keys`, `max`, `tabulate`, `plot` y `plot(cumulative=True)`.

## Volver a Python: decisiones y control

El *control* permite que el programa tome decisiones y repita acciones. Los operadores de comparación (`<`, `<=`, `==`, `!=`, `>`, `>=`) se usan dentro de comprensiones de listas con el patrón `[w for w in text if condición]`:

```python
>>> [w for w in sent7 if len(w) == 4]
```

Además hay operadores sobre palabras: `startswith`, `endswith`, `in`, `islower`, `isupper`, `isalpha`, `isalnum`, `isdigit`, `istitle`. Las condiciones se combinan con `not`, `and`, `or`.

La *comprensión de listas* `[f(w) for w in text]` o `[w.f() for w in text]` es un idiom que aplica la misma operación a cada elemento. Aplicada al vocabulario, bajar a minúsculas y filtrar no alfabéticos reduce el conteo de tipos de 19.317 a 16.948 en Moby Dick:

```python
>>> len(set([word.lower() for word in text1 if word.isalpha()]))
```

Las estructuras de control usan dos puntos y un bloque indentado. El `if` ejecuta el bloque solo si la condición es verdadera; el `for` recorre cada elemento de una lista; `elif` y `else` cubren los casos alternativos. Combinando `for` e `if` se filtra e imprime, y una coma final en `print` mantiene la salida en una sola línea:

```python
>>> for token in sent1:
...     if token.islower():
...         print token, 'is a lowercase word'
...     elif token.istitle():
...         print token, 'is a titlecase word'
...     else:
...         print token, 'is punctuation'
```

## Comprensión automática del lenguaje natural

El capítulo cierra pintando el panorama del NLP y sus retos abiertos:

- **Desambiguación de sentido (word sense disambiguation)**: elegir el sentido correcto de palabras ambiguas como *serve* o *dish* a partir del contexto; incluso preposiciones como *by* cambian de sentido (agentivo, locativo, temporal).
- **Resolución de pronombres (pronoun/anaphora resolution)**: averiguar "quién hizo qué a quién" identificando el antecedente de un pronombre y los roles semánticos (agente, paciente, instrumento).
- **Generación de salida**: question answering y traducción automática dependen de entender bien el texto; traducir *they* al francés obliga a elegir género (*ils*/*elles*) según el antecedente correcto.
- **Traducción automática (MT)**: ha sido el "santo grial"; el ejemplo con el *babelizer* de NLTK muestra cómo la ida y vuelta degrada el sentido (p. ej. *Alice Springs* → *Alice jump*). Hoy se abordan sus dificultades con grandes cantidades de textos paralelos y *text alignment*.
- **Sistemas de diálogo hablado**: medidos históricamente por el Turing Test; los comerciales son limitados pero útiles en dominios estrechos, con una arquitectura en *pipeline* (Figura 1-5) de comprensión y generación apoyada en datos lingüísticos.
- **Inferencia textual (RTE, Recognizing Textual Entailment)**: decidir si un texto sustenta una hipótesis; requiere análisis lingüístico y conocimiento del mundo (distinguir autor de editor, quién vence a quién).

Los límites actuales: los sistemas desplegados no razonan con sentido común ni manejan conocimiento del mundo de forma general. El objetivo del NLP ha sido avanzar con técnicas superficiales pero potentes en lugar de esperar a resolver la IA completa.

## Ideas clave

- Un texto en Python es una lista de palabras; `len(text)` cuenta tokens y `len(set(text))` cuenta tipos; `sorted(set(t))` da el vocabulario.
- Token = aparición concreta de una palabra; tipo = forma única; su cociente mide la diversidad léxica.
- `concordance`, `similar`, `common_contexts`, `dispersion_plot` y `generate` permiten explorar un texto más allá de leerlo.
- Las palabras muy frecuentes y los hapaxes informan poco; las palabras largas y frecuentes a la vez caracterizan mejor el texto.
- `FreqDist`, bigramas y `collocations()` resumen el estilo y contenido de un texto.
- La comprensión de listas `[f(x) for x in text]` aplica una operación a cada elemento; `if`/`for` con dos puntos e indentación dan control.
- Las funciones (`def`) encapsulan y reutilizan bloques de código con parámetros y argumentos.
- El NLP tiene retos abiertos (desambiguación, pronombres, traducción, diálogo, inferencia) y límites reales en razonamiento y conocimiento del mundo.
