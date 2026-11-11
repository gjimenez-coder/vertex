# Capítulo 1 — Language Processing and Python (Procesamiento del lenguaje y Python) — Estudio

## Tarjetas de repaso

P: ¿Qué es un *token* según el capítulo? / R: Cada aparición concreta de una secuencia de caracteres (una palabra o signo) en el texto.

P: ¿Qué es el vocabulario de un texto y cómo se obtiene? / R: El conjunto de tokens distintos (tipos), obtenido con `set(text)`.

P: ¿Cómo se mide la diversidad léxica? / R: Dividiendo el número de tokens entre el número de tipos: `len(text) / len(set(text))`.

P: ¿Qué hace `text.concordance("palabra")`? / R: Muestra cada aparición de la palabra en su contexto.

P: ¿Qué diferencia hay entre `similar` y `common_contexts`? / R: `similar` da palabras que aparecen en contextos parecidos; `common_contexts` da los contextos que comparten dos palabras.

P: ¿Para qué sirve `dispersion_plot`? / R: Dibuja un gráfico de dispersión léxica que muestra dónde aparece cada palabra a lo largo del texto (requiere NumPy y Matplotlib).

P: ¿Qué es una distribución de frecuencias (`FreqDist`)? / R: Un registro de cuántas veces aparece cada tipo en el texto, útil para hallar las palabras más informativas.

P: ¿Qué son los *hapaxes* y por qué informan poco? / R: Palabras que aparecen una sola vez; son demasiados y sin contexto, así que no caracterizan el texto.

P: ¿Qué es una colocación? / R: Una secuencia de palabras que aparecen juntas con frecuencia inusual y resisten la sustitución por sinónimos (*red wine*, no *maroon wine*).

P: ¿Qué son los bigramas y cómo se relacionan con `collocations()`? / R: Los bigramas son pares de palabras; `collocations()` halla los bigramas más frecuentes de lo esperado dadas las frecuencias individuales.

P: ¿Qué hace una comprensión de listas `[f(w) for w in text]`? / R: Aplica la misma operación a cada elemento del texto.

P: ¿Qué es una función en Python y cómo se define? / R: Un bloque de código con nombre reutilizable, definido con `def`, que recibe parámetros y se llama con argumentos.

P: ¿Cómo se concatena y cómo se añade a una lista? / R: El operador `+` concatena dos listas en una nueva; `append()` añade un elemento modificando la lista original.

P: En un slice `m:n`, ¿qué elementos se incluyen? / R: Los elementos desde `m` hasta `n-1`.

P: ¿Qué reto del NLP consiste en elegir el sentido correcto de palabras ambiguas según el contexto? / R: La desambiguación de sentido (word sense disambiguation).

## Preguntas de autoevaluación

P: ¿Por qué `monstrous` ilustra que el uso de una palabra depende del texto? / R: En Austen tiene connotaciones positivas y funciona como intensificador (como *very*), a diferencia de Melville. (Sección: Computar con el lenguaje: textos y palabras)

P: ¿Por qué las 50 palabras más frecuentes de Moby Dick no son muy informativas, y cómo se seleccionan palabras más útiles? / R: Casi todas son "fontanería" del inglés (solo `whale` informa); se combinan longitud y frecuencia, p. ej. palabras con `len(w) > 7` y frecuencia mayor que un umbral. (Sección: Computar con el lenguaje: estadísticas simples)

P: ¿Qué diferencia hay entre un `SyntaxError` y un `IndexError`? / R: El `SyntaxError` ocurre por instrucciones mal formadas (p. ej. terminar en `+`); el `IndexError` es un error de ejecución por usar un índice demasiado grande. (Secciones: Computar con el lenguaje: textos y palabras / Un vistazo a Python: textos como listas de palabras)

P: ¿Cómo se convierte entre lista de palabras y cadena? / R: Con `' '.join([...])` se pasa de lista a cadena y con `'...'.split()` de cadena a lista. (Sección: Un vistazo a Python: textos como listas de palabras)

P: ¿Cómo reduce la comprensión de listas el conteo de tipos en Moby Dick y por qué? / R: Bajando a minúsculas y filtrando no alfabéticos (`word.lower()` con `word.isalpha()`), el conteo baja de 19.317 a 16.948 tipos. (Sección: Volver a Python: decisiones y control)

P: ¿Qué estructuras de control se presentan y qué formato comparten? / R: `if`, `elif`, `else` y `for`; todas usan dos puntos y un bloque indentado. (Sección: Volver a Python: decisiones y control)

P: ¿Qué muestra el ejemplo del *babelizer* sobre la traducción automática? / R: Que la traducción de ida y vuelta degrada el sentido (p. ej. *Alice Springs* → *Alice jump*); hoy se aborda con textos paralelos y *text alignment*. (Sección: Comprensión automática del lenguaje natural)

P: ¿Cuáles son los límites actuales del NLP según el capítulo? / R: Los sistemas desplegados no razonan con sentido común ni manejan conocimiento del mundo general; se avanza con técnicas superficiales pero potentes. (Sección: Comprensión automática del lenguaje natural)

## Puntos a dominar

- Instalar NLTK y sus datos (`nltk.download()`, colección *book*) y cargar los textos con `from nltk.book import *`.
- Explorar un texto con `concordance`, `similar`, `common_contexts`, `dispersion_plot` y `generate`.
- Contar tokens (`len(text)`) y tipos (`len(set(text))`) y calcular la diversidad léxica.
- Definir funciones con `def` (p. ej. `lexical_diversity`, `percentage`) y reutilizarlas con distintos argumentos.
- Manejar listas y cadenas: indexación, slicing (`m:n`, omisión de extremos), `+`, `append()`, `join`, `split`.
- Usar `FreqDist` y sus métodos (`keys`, `max`, `freq`, `N`, `tabulate`, `plot`) y hallar colocaciones con `collocations()`.
- Escribir comprensiones de listas con filtros (`isalpha`, `islower`, `len`, etc.) y estructuras de control `if`/`elif`/`else` y `for` con indentación.
- Reconocer los retos abiertos del NLP: desambiguación de sentido, resolución de pronombres, traducción automática, diálogo e inferencia textual (RTE).
