# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 10 — Analyzing the Meaning of Sentences (Analizando el significado de las oraciones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo aborda tres preguntas: cómo representar el significado del lenguaje natural para que un ordenador lo procese, cómo asociar representaciones de significado a un conjunto ilimitado de oraciones, y cómo conectar esas representaciones con bases de conocimiento. La tesis central es que la lógica —en particular la lógica de primer orden (first-order logic)— es una buena elección para la semántica computacional: es lo bastante expresiva y existen demostradores de teoremas eficientes para razonar con ella.

El recorrido parte de una tarea concreta (consultar una base de datos en inglés traduciendo a SQL) para mostrar sus limitaciones y motivar una representación más abstracta y genérica: la lógica. De ahí avanza por la lógica proposicional, la lógica de primer orden, la noción de verdad en un modelo, el cálculo λ como herramienta para construir significado composicionalmente, y finalmente la semántica del discurso con DRT.

Sales sabiendo traducir oraciones del inglés a fórmulas lógicas, evaluar su verdad en modelos set-teóricos definidos en NLTK, usar los demostradores Prover9 y Mace4 para inferencia y construcción de modelos, aplicar el cálculo λ y la β-reducción para composición semántica, y entender la ambigüedad de alcance de cuantificadores y el procesamiento de discurso.

## El ejemplo que recorre el capítulo

Un pequeño mundo de individuos —Angus, Cyril (el perro), Bertie, Olive, Evi, Stefan, Klaus— con predicados como `boy`, `girl`, `dog`, `walk`, `see`, `chase` y `bark`. Oraciones como *Cyril barks*, *A dog barks*, *Angus chases a dog* y *Every girl chases a dog* sirven para ilustrar cada técnica, desde la valuación de un modelo hasta la composición con λ-abstractos.

## Natural Language Understanding (consultar una base de datos)

El punto de partida es una tabla `city_table` (ciudades, países, poblaciones) tomada del sistema Chat-80 (Warren & Pereira, 1982), con datos de los años 80. La vía obvia para recuperar respuestas es una consulta SQL:

```sql
SELECT Country FROM city_table WHERE City = 'athens'
```

Con una gramática basada en rasgos (`sql0.fcfg`) del Capítulo 9, cada regla añade una receta para el rasgo `SEM`, ensamblada por concatenación de cadenas (`+`), de modo que al parsear *What cities are located in China* se construye la consulta SQL correspondiente y se ejecuta sobre `city.db`.

Esta solución tiene dos críticas. Primero, las representaciones de los constituyentes (p. ej. `SELECT` para el determinante, `City FROM city_table` para el nombre) no tienen un significado bien definido por separado. Segundo, hemos cableado demasiado detalle de la base de datos (nombre de tabla y campos); con otro formato (XML) habría que traducir a otro lenguaje de consulta. Esto sugiere traducir el inglés a algo más abstracto y genérico: la lógica. La conjunción *and* en *What cities are in China and have populations above 1,000,000?* se interpreta como el `AND` clásico: `Cond1 AND Cond2` es verdad en una situación `s` sii ambas condiciones lo son, con independencia del lenguaje de consulta.

## Lenguaje natural, semántica y lógica

En lugar de traducir una oración de un lenguaje a otro, se busca decir de qué trata relacionándola con una situación del mundo. Dos nociones fundamentales: las oraciones declarativas son verdaderas o falsas en ciertas situaciones, y las frases nominales definidas y los nombres propios refieren a cosas del mundo. Con la noción de verdad en una situación podemos preguntar si un conjunto de oraciones puede ser verdadero conjuntamente (consistencia) o no (inconsistencia). Los enfoques lógicos se centran en los aspectos que guían nuestros juicios de consistencia, reduciendo tareas como determinar la consistencia a manipulación simbólica.

Un modelo para un conjunto W de oraciones es una representación formal de una situación donde todas las oraciones de W son verdaderas, expresada con teoría de conjuntos: un dominio D de individuos y relaciones tratadas como conjuntos construidos a partir de D. El capítulo enlaza con el Test de Turing (Turing, 1950): juzgar la comprensión del lenguaje por el comportamiento observable y no por los estados internos.

## Propositional Logic (lógica proposicional)

La lógica proposicional representa solo las partes que corresponden a conectores oracionales (operadores booleanos). Los símbolos proposicionales (P, Q, R) y los operadores generan un conjunto infinito de fórmulas bien formadas. Las versiones ASCII en NLTK:

```
negation       -
conjunction    &
disjunction    |
implication    ->
equivalence    <->
```

Si φ es fórmula, `-φ` lo es; y si φ y ψ lo son, también `(φ & ψ)`, `(φ | ψ)`, `(φ -> ψ)` y `(φ <-> ψ)`. Las condiciones de verdad siguen la tabla clásica; la implicación es sorprendente: `(P -> Q)` solo es falsa cuando P es verdadera y Q falsa (si P es falsa, la implicación es verdadera).

La lógica permite inferencia: pasar de una o varias asunciones a una conclusión. Un argumento es válido si no hay situación donde las premisas sean todas verdaderas y la conclusión no. La notación `[A1, ..., An] / C` representa que C se sigue de las asunciones. La limitación de la lógica proposicional es que no puede "mirar dentro" de las proposiciones atómicas para hablar de relaciones entre individuos (p. ej. la asimetría de *to the north of*). Con `LogicParser` y `Prover9` se puede verificar la validez:

```python
>>> prover = nltk.Prover9()
>>> prover.prove(NotFnS, [SnF, R])   # R: SnF -> -FnS
True
```

Un modelo proposicional asigna True/False a cada fórmula. Una `Valuation` mapea símbolos a valores; un `Model` ofrece `evaluate()` para calcular el valor semántico de fórmulas complejas aplicando las condiciones de los operadores.

## First-Order Logic (lógica de primer orden)

La lógica de primer orden analiza las proposiciones en predicados y argumentos, acercándose a la estructura del lenguaje natural: *Angus walks* se formaliza como `walk(angus)` y *Angus sees Bertie* como `see(angus, bertie)` (predicado unario y binario). Los símbolos de predicado no tienen significado intrínseco: `love(margrietje, brunoke)` y `houden_van(margrietje, brunoke)` no difieren lógicamente. Son constantes no lógicas, cuyo valor depende de la valuación; en cambio, las constantes lógicas (operadores booleanos, la igualdad `=`) reciben la misma interpretación en todo modelo.

Siguiendo la gramática de Montague se usan dos tipos básicos: `e` (entidades) y `t` (fórmulas con valor de verdad). Los tipos complejos `⟨σ, τ⟩` son funciones; un predicado unario es `⟨e, t⟩` y uno binario `⟨e, ⟨e, t⟩⟩`. `LogicParser(type_check=True)` comprueba tipos y admite una `signature` que asocia tipos a constantes no lógicas.

Las variables individuales (x, y, z) son como pronombres: su denotación depende del contexto. Pueden ligarse con cuantificadores. El cuantificador existencial `exists x` ("para algún x") y el universal `all x` ("para todo x"):

```
exists x.(dog(x) & disappear(x))     # Un perro desapareció
all x.(dog(x) -> disappear(x))        # Todo perro desapareció
```

La traducción universal con `->` tiene condiciones de verdad peculiares: si no hay perros, `all x.(dog(x) -> disappear(x))` sigue siendo verdadera. Una ocurrencia de x es libre si no cae bajo el alcance de un cuantificador; en caso contrario está ligada. Una fórmula sin variables libres es cerrada. El método `free()` devuelve las variables libres de una expresión.

### Demostración de teoremas y resumen sintáctico

La lógica de primer orden sí captura reglas sobre predicados binarios, como la asimetría de *to the north of*:

```
all x. all y. (north_of(x, y) -> -north_of(y, x))
```

Con Prover9 se demuestra `A ⊢ g` (que la meta g se deriva de las asunciones A). Las reglas de formación resumen la sintaxis: predicados de tipo `⟨eⁿ, t⟩` con n argumentos (n es la aridad), igualdad/desigualdad `=` y `!=`, negación, los conectores binarios y los cuantificadores `exists`/`all`.

## Truth in Model (verdad en un modelo)

Dado un lenguaje L, un modelo M es un par ⟨D, Val⟩: D es el dominio no vacío y Val la función de valuación. Val asigna a cada constante individual un elemento de D, y a cada predicado de aridad n una función de Dⁿ a {True, False}; en NLTK se representa convenientemente como un conjunto de tuplas. Las relaciones se representan como conjuntos de tuplas; los predicados unarios como conjuntos de tuplas singleton, para un tratamiento uniforme de cualquier aridad.

```python
>>> v = """
... bertie => b
... boy => {b}
... see => {(b, o), (c, b), (o, c)}
... """
>>> val = nltk.parse_valuation(v)
```

### Asignaciones de variables y cuantificación

El contraparte del contexto de uso es una asignación de variables (`Assignment`), un mapeo parcial de variables individuales a entidades del dominio. Al evaluar una fórmula con variable, el intérprete pregunta a la asignación por su valor. Si la variable no está ligada, la evaluación devuelve `'Undefined'`. El proceso de determinar verdad o falsedad en un modelo se llama *model checking*.

La satisfacción de variables interpreta las fórmulas cuantificadas: `exists x.(girl(x) & walk(x))` es verdadera si hay algún `u` en el dominio tal que `g[u/x]` satisface la fórmula abierta. El método `satisfiers()` devuelve el conjunto de individuos que satisfacen una fórmula abierta. Un universal `∀x.φ` es verdadero respecto de `g` sii para todo `u`, φ es verdadera respecto de `g[u/x]`.

### Ambigüedad de alcance de cuantificadores

*Everybody admires someone* tiene (al menos) dos representaciones con significados distintos:

```
all x.(person(x) -> exists y.(person(y) & admire(x,y)))   # alcance amplio de ∀
exists y.(person(y) & all x.(person(x) -> admire(x,y)))   # alcance amplio de ∃
```

La segunda es lógicamente más fuerte: afirma que existe una persona única admirada por todos. Se distinguen por el alcance de los cuantificadores; la oración es ambigua respecto a ese alcance y `satisfiers()` permite explorar qué lecturas se cumplen en un modelo dado.

### Model Building (construcción de modelos)

A diferencia del *model checking*, la construcción de modelos crea un nuevo modelo dado un conjunto de oraciones; si lo logra, el conjunto es consistente. Se usa el constructor Mace4 vía `Mace()` y `build_model()`. Puede usarse como complemento del demostrador: para probar `A ⊢ g`, Mace4 intenta hallar un contraejemplo construyendo un modelo para `A` junto con `-g`. Al encontrar un modelo introduce constantes de Skolem (p. ej. `C1`) como representantes del cuantificador existencial. El ejercicio con *There is a woman that every man loves* muestra cómo el constructor revela el conocimiento implícito que aportamos: hay que añadir asunciones (p. ej. que hombres y mujeres son conjuntos disjuntos) para obtener contramodelos acordes con nuestra intuición.

## The Semantics of English Sentences (semántica composicional)

El Principio de Composicionalidad (o Principio de Frege): el significado del todo es función de los significados de las partes y del modo en que se combinan sintácticamente. En lugar de concatenar cadenas (como en `sql0.fcfg`), ahora se usa aplicación de función. La regla clave:

```
S[SEM=<?vp(?np)>] -> NP[SEM=?subj] VP[SEM=?vp]
```

El `SEM` de la S se construye aplicando el `SEM` del VP (función) al del NP (argumento).

### El cálculo λ

El operador λ introduce abstracción sobre variables, análogo a la notación de conjuntos `{w | P(w)}`. `λx.(walk(x) & chew_gum(x))` (en NLTK `\x.(...)`) es la propiedad de ser un x que camina y mastica chicle (λ-abstracción). No forma parte de la lógica de primer orden; ambos pueden usarse independientemente. Aplicar un λ-abstracto a un argumento y sustituir la variable ligada es la β-reducción, que `simplify()` realiza:

```python
>>> lp.parse(r'\x.(walk(x) & chew_gum(x))(gerald)').simplify()
(walk(gerald) & chew_gum(gerald))
```

Se puede abstraer sobre variables de tipo superior (p. ej. `P`, `Q` de tipo `⟨e, t⟩`), lo que permite el *type-raising*. Hay que evitar la captura de variables: al β-reducir se relabelan variables ligadas mediante α-conversión (fórmulas que solo difieren en el nombre de la variable ligada son α-equivalentes). Esto es automático en el módulo `logic`.

### NPs cuantificados y verbos transitivos

Para que *A dog barks* produzca `exists x.(dog(x) & bark(x))`, el NP sujeto actúa como expresión de función (type-raising) de tipo `⟨⟨e, t⟩, t⟩`:

```
\P.exists x.(dog(x) & P(x))     # a dog
\P.all x.(dog(x) -> P(x))        # every dog
\Q P.exists x.(Q(x) & P(x))      # determinante "a"
```

Los nombres propios se reinterpretan también como expresiones de función: *Angus* es `\P.P(angus)`. Para los verbos transitivos, con las restricciones de que el NP tenga la misma representación sea sujeto u objeto y que los VP sean siempre de tipo `⟨e, t⟩`, el verbo *chases* se representa como `\X y.X(\x.chase(y, x))`. La gramática `simple-sem.fcfg` reúne estas reglas; `batch_interpret()` deriva las representaciones y `batch_evaluate()` comprueba además el valor de verdad en un modelo.

### Ambigüedad de alcance revisitada (Cooper storage)

El método anterior es *syntax-driven*: el alcance de los cuantificadores refleja el de los NPs en el árbol, de modo que *Every girl chases a dog* solo recibe la lectura con ∀ amplio. El *Cooper storage* separa la representación en un par CORE (núcleo) más una lista de operadores de ligado (STORE). La S-Retrieval va tomando operadores de la lista y aplicándolos al núcleo; probando todas las permutaciones se generan todos los alcances posibles. El módulo `nltk.sem.cooper_storage` convierte estas representaciones en formas lógicas estándar, produciendo ambas lecturas.

## Discourse Semantics (semántica del discurso)

Un discurso es una secuencia de oraciones; a menudo la interpretación de una oración depende de las anteriores, como ocurre con los pronombres anafóricos (*he*, *she*, *it*). La cuantificación estándar de primer orden se limita a oraciones individuales, pero el alcance de un cuantificador puede extenderse a varias: en *Angus owns a dog. It bit Irene*, el NP *a dog* liga el *it* de la segunda oración.

La Discourse Representation Theory (DRT) maneja estos fenómenos. Una discourse representation structure (DRS) representa el significado mediante una lista de referentes del discurso (los individuos en cuestión, análogos a las variables individuales) y una lista de condiciones (fórmulas atómicas abiertas). Al procesar la segunda oración se interpreta en el contexto de la primera: el pronombre añade un referente nuevo y la resolución anafórica lo liga a un referente existente (condición `u = y`).

```python
>>> dp = nltk.DrtParser()
>>> drs1 = dp.parse('([x, y], [angus(x), dog(y), own(x, y)])')
>>> print drs1.fol()
exists x y.((angus(x) & dog(y)) & own(x,y))
```

Toda DRS se traduce a lógica de primer orden con `fol()`. El operador de concatenación `+` fusiona referentes y condiciones (con α-conversión automática). Se pueden anidar DRS para la cuantificación universal mediante implicación. El módulo `nltk.sem.drt_resolve_anaphora` y `resolve_anaphora()` reemplazan una condición `PRO(x)` por `x = [...lista de antecedentes...]`, dejando la elección del antecedente a procedimientos intercambiables. La DRT es compatible con el cálculo λ, permitiendo representaciones composicionales basadas en DRT (gramática `drt.fcfg`).

### Procesamiento de discurso

El módulo `nltk.inference.discourse` incorpora inferencia y procesa secuencias de oraciones. Un *discourse thread* es una secuencia de lecturas, una por oración; el módulo las procesa incrementalmente rastreando todos los hilos cuando hay ambigüedad. Con `consistchk=True` se comprueba consistencia (invocando el model checker) y con `informchk=True` si una nueva oración es informativa (es informativa si el demostrador no puede probarla a partir de las anteriores). Combinando DRT y Glue Semantics, las lecturas inadmisibles —por ejemplo, aquellas en que un pronombre no puede resolverse— se filtran con `filter=True`.

## Ideas clave

- La lógica de primer orden es un buen lenguaje para representar el significado del lenguaje natural: es expresiva y cuenta con demostradores de teoremas eficientes (Prover9) y constructores de modelos (Mace4).
- Traducir a lógica es más abstracto y genérico que traducir a SQL; una vez en lógica se puede convertir a otros lenguajes especializados.
- Las oraciones declarativas son verdaderas o falsas en situaciones; los nombres propios y NPs definidos refieren a entidades. Un modelo ⟨D, Val⟩ formaliza una situación con conjuntos.
- La lógica proposicional solo captura conectores oracionales; la de primer orden añade predicados, argumentos, variables y cuantificadores (`exists`, `all`).
- El cálculo λ se añade a la lógica para construir significado composicionalmente; la β-reducción corresponde a aplicar una función a un argumento, con α-conversión para evitar la captura de variables.
- Los cuantificadores se interpretan vía satisfacción de variables; las oraciones con cuantificadores anidados suelen ser ambiguas respecto al alcance (wide scope), resoluble con Cooper storage.
- `batch_interpret()` deriva representaciones semánticas y `batch_evaluate()` comprueba su verdad en un modelo a partir de una gramática con el rasgo `SEM`.
- La DRT extiende la semántica más allá de la oración, con referentes del discurso y condiciones, resolución anafórica y comprobaciones de consistencia e informatividad.
