# Analyzing the Meaning of Sentences (Analizando el significado de las oraciones) — Estudio

## Tarjetas de repaso

P: ¿Qué tres preguntas aborda el capítulo? / R: Cómo representar el significado del lenguaje natural para un ordenador, cómo asociar representaciones de significado a un conjunto ilimitado de oraciones, y cómo conectar esas representaciones con bases de conocimiento.

P: ¿Cuál es la tesis central sobre la semántica computacional? / R: Que la lógica —en particular la lógica de primer orden (first-order logic)— es una buena elección porque es lo bastante expresiva y existen demostradores de teoremas eficientes para razonar con ella.

P: ¿Por qué se prefiere traducir el inglés a lógica en vez de a SQL? / R: Porque la lógica es más abstracta y genérica; las representaciones SQL cablean detalles de la base de datos (tabla, campos) y los constituyentes no tienen significado bien definido por separado. Desde la lógica se puede convertir a otros lenguajes especializados.

P: ¿Qué es un modelo para un conjunto W de oraciones? / R: Una representación formal de una situación donde todas las oraciones de W son verdaderas, expresada con teoría de conjuntos: un dominio D de individuos y relaciones tratadas como conjuntos construidos a partir de D.

P: ¿Qué captura la lógica proposicional y cuál es su limitación? / R: Captura solo las partes correspondientes a conectores oracionales (operadores booleanos); su limitación es que no puede "mirar dentro" de las proposiciones atómicas para hablar de relaciones entre individuos.

P: ¿Cuándo es falsa la implicación `(P -> Q)`? / R: Solo cuando P es verdadera y Q falsa; si P es falsa, la implicación es verdadera.

P: ¿En qué se diferencian las constantes lógicas de las no lógicas? / R: Las constantes no lógicas (símbolos de predicado) no tienen significado intrínseco y su valor depende de la valuación; las constantes lógicas (operadores booleanos, la igualdad `=`) reciben la misma interpretación en todo modelo.

P: ¿Qué expresan los cuantificadores `exists x` y `all x`? / R: `exists x` significa "para algún x" (existencial) y `all x` significa "para todo x" (universal); p. ej. `exists x.(dog(x) & disappear(x))` y `all x.(dog(x) -> disappear(x))`.

P: ¿Qué es un modelo M en la lógica de primer orden? / R: Un par ⟨D, Val⟩ donde D es el dominio no vacío y Val la función de valuación que asigna a cada constante individual un elemento de D y a cada predicado de aridad n una función de Dⁿ a {True, False}, representada como conjunto de tuplas.

P: ¿Qué es el model checking? / R: El proceso de determinar la verdad o falsedad de una fórmula en un modelo; usa asignaciones de variables y la satisfacción de variables para las fórmulas cuantificadas.

P: ¿Qué es el Principio de Composicionalidad (o de Frege)? / R: El significado del todo es función de los significados de las partes y del modo en que se combinan sintácticamente; en la semántica composicional se usa aplicación de función en lugar de concatenar cadenas.

P: ¿Qué es la β-reducción y para qué sirve la α-conversión? / R: La β-reducción aplica un λ-abstracto a un argumento sustituyendo la variable ligada (lo hace `simplify()`); la α-conversión relabela variables ligadas para evitar su captura (fórmulas que solo difieren en ese nombre son α-equivalentes).

P: ¿Para qué sirve el Cooper storage? / R: Para generar todos los alcances posibles de los cuantificadores separando la representación en un par CORE más una lista STORE de operadores de ligado; la S-Retrieval los aplica en todas las permutaciones, produciendo ambas lecturas.

P: ¿Qué es una DRS en la Discourse Representation Theory (DRT)? / R: Una discourse representation structure que representa el significado mediante una lista de referentes del discurso y una lista de condiciones (fórmulas atómicas abiertas); se traduce a lógica de primer orden con `fol()`.

P: ¿Qué papel juegan Prover9 y Mace4? / R: Prover9 es un demostrador de teoremas que verifica si una meta se deriva de las asunciones; Mace4 es un constructor de modelos que crea un modelo para un conjunto de oraciones (si lo logra, es consistente) y puede hallar contraejemplos.

## Preguntas de autoevaluación

P: ¿Qué dos críticas recibe la solución de traducir oraciones a SQL? / R: Primero, las representaciones de los constituyentes no tienen un significado bien definido por separado; segundo, se cablea demasiado detalle de la base de datos (nombre de tabla y campos), de modo que otro formato obligaría a traducir a otro lenguaje de consulta. (Sección: Natural Language Understanding)

P: ¿Por qué `all x.(dog(x) -> disappear(x))` es verdadera si no hay perros? / R: Porque la traducción universal usa `->` y la implicación es verdadera cuando su antecedente es falso; sin perros, `dog(x)` nunca se cumple, por lo que la implicación se satisface para todo x. (Sección: First-Order Logic)

P: ¿Qué diferencia una variable libre de una ligada y qué es una fórmula cerrada? / R: Una ocurrencia es libre si no cae bajo el alcance de un cuantificador y ligada si cae bajo él; una fórmula sin variables libres es cerrada. El método `free()` devuelve las variables libres. (Sección: First-Order Logic)

P: ¿Cuáles son las dos lecturas de *Everybody admires someone* y cuál es más fuerte? / R: `all x.(person(x) -> exists y.(person(y) & admire(x,y)))` (∀ amplio) y `exists y.(person(y) & all x.(person(x) -> admire(x,y)))` (∃ amplio); la segunda es lógicamente más fuerte porque afirma que existe una persona única admirada por todos. (Sección: Ambigüedad de alcance de cuantificadores)

P: ¿En qué se diferencia la construcción de modelos (model building) del model checking? / R: El model checking determina la verdad de una fórmula en un modelo dado, mientras que la construcción de modelos crea un nuevo modelo a partir de un conjunto de oraciones; si lo logra, el conjunto es consistente, y puede hallar contraejemplos construyendo un modelo para A junto con -g. (Sección: Model Building)

P: ¿Cómo se representan los NPs cuantificados y los nombres propios en la semántica composicional? / R: Mediante type-raising como expresiones de función de tipo `⟨⟨e, t⟩, t⟩`: p. ej. *a dog* es `\P.exists x.(dog(x) & P(x))` y *Angus* es `\P.P(angus)`. (Sección: NPs cuantificados y verbos transitivos)

P: ¿Por qué el método syntax-driven no genera ambas lecturas de *Every girl chases a dog*? / R: Porque el alcance de los cuantificadores refleja el de los NPs en el árbol sintáctico, de modo que solo se obtiene la lectura con ∀ amplio; el Cooper storage se usa para producir todos los alcances. (Sección: Ambigüedad de alcance revisitada)

P: ¿Cómo maneja la DRT los pronombres anafóricos entre oraciones? / R: Procesa la segunda oración en el contexto de la primera; el pronombre añade un referente del discurso nuevo y la resolución anafórica lo liga a un referente existente mediante una condición de igualdad (p. ej. `u = y`), usando `resolve_anaphora()`. (Sección: Discourse Semantics)

## Puntos a dominar

- Explicar por qué la lógica es una representación más abstracta y genérica que SQL y qué limitaciones de la traducción a SQL la motivan.
- Distinguir qué captura la lógica proposicional frente a la de primer orden (predicados, argumentos, variables, cuantificadores).
- Reconocer las condiciones de verdad de los operadores booleanos, en especial la implicación.
- Describir un modelo ⟨D, Val⟩ y cómo se representan predicados y relaciones como conjuntos de tuplas en NLTK.
- Interpretar fórmulas cuantificadas mediante asignaciones de variables y satisfacción (model checking).
- Identificar la ambigüedad de alcance de cuantificadores y las dos técnicas asociadas (syntax-driven y Cooper storage).
- Aplicar el cálculo λ y la β-reducción para composición semántica, cuidando la captura de variables con α-conversión.
- Explicar cómo la DRT extiende la semántica al discurso con referentes y condiciones, resolución anafórica y comprobaciones de consistencia e informatividad.
- Relacionar Prover9 (demostración) y Mace4 (construcción de modelos) con las tareas de inferencia y consistencia.
