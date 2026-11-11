# Analyzing Sentence Structure (Análisis de la estructura de las oraciones) — Estudio

## Tarjetas de repaso

P: ¿Qué dos problemas del lenguaje natural motivan el paso del nivel de palabra al de oración?
R: La ambigüedad del lenguaje natural y que el número de oraciones posibles es ilimitado mientras que los programas son finitos.

P: ¿Qué es una gramática en el marco de la gramática generativa?
R: La notación capaz de generar el conjunto (potencialmente infinito) de todas las oraciones gramaticales mediante producciones recursivas, como `S -> S and S`.

P: ¿Por qué la oración de Groucho "I shot an elephant in my pajamas" es ambigua?
R: El sintagma preposicional *in my pajamas* puede describir al elefante o al acto de disparar, produciendo dos árboles distintos sin que ninguna palabra sea ambigua (ambigüedad de attachment).

P: ¿En qué criterio se basa la identificación de constituyentes?
R: En la sustituibilidad: una secuencia que forma unidad puede reemplazarse por una más corta sin volver mal formada la oración (p. ej. *The little bear* por *He*).

P: ¿Qué es el símbolo inicial de una CFG?
R: Por convención, el lado izquierdo de la primera producción (normalmente S), raíz de todo árbol bien formado.

P: ¿Qué dos restricciones impone NLTK al escribir CFG?
R: No mezclar categorías gramaticales con ítems léxicos en el mismo lado derecho (prohibido `PP -> 'of' NP`) y no usar ítems léxicos multipalabra (usar `NP -> 'New_York'`).

P: ¿Cuándo es recursiva una gramática?
R: Cuando una categoría del lado izquierdo reaparece en el derecho: recursión directa (`Nom -> Adj Nom`) o indirecta (S vía `S -> NP VP` y `VP -> V S`).

P: ¿Qué diferencia una gramática de un parser?
R: La gramática es una especificación declarativa de buena formación (una cadena); el parser es su interpretación procedimental que busca un árbol licenciado cuya frontera sea la oración.

P: ¿Cuáles son los tres defectos del parser de descenso recursivo (top-down)?
R: Las producciones recursivas por la izquierda lo meten en bucle infinito; pierde tiempo con estructuras que no corresponden a la entrada; y el backtracking descarta constituyentes ya construidos que luego rehace.

P: ¿Qué hacen las operaciones shift y reduce en el parser shift-reduce (bottom-up)?
R: *Shift* empuja la siguiente palabra a la pila; *reduce* sustituye los n ítems de la cima que coinciden con el lado derecho de una producción por su lado izquierdo.

P: ¿Qué es el left-corner parser?
R: Un híbrido top-down con filtrado bottom-up que no cae en producciones recursivas por la izquierda, usando una tabla de "esquinas izquierdas" (preterminales) por no terminal.

P: ¿Qué técnica usa la tabla de subcadenas bien formadas (WFST) y cuál es su limitación principal?
R: Programación dinámica para construir cada constituyente una sola vez y reutilizarlo; su limitación es que solo reconoce (no es un árbol), exige producciones binarias y no representa la ambigüedad estructural.

P: ¿Qué es una relación de dependencia?
R: Una relación binaria asimétrica entre un núcleo (head) y sus dependientes; el núcleo de la oración suele ser el verbo conjugado y toda palabra depende de él directa o indirectamente.

P: ¿Qué es la valencia de un verbo y cómo se controla en una CFG?
R: Los complementos que admite (p. ej. *saw* con NP, *thought* con S, *put* con NP PP); se controla subcategorizando los verbos como TV, IV, DatV, SV.

P: ¿Cómo asigna probabilidades una PCFG y cómo se calcula la de un análisis?
R: Asocia una probabilidad a cada producción (las de un mismo lado izquierdo suman 1); la probabilidad del análisis es el producto de las de sus producciones, y `nltk.ViterbiParser` halla el más probable.

## Preguntas de autoevaluación

P: ¿Por qué un corpus con todo el inglés dicho o escrito en 50 años no equivaldría a "el inglés moderno"?
R: Porque los hablantes rechazan secuencias agramaticales como *the of* y a la vez aceptan oraciones nuevas jamás pronunciadas; la lengua es un conjunto generado, no un inventario cerrado. (Sección "Algunos dilemas gramaticales")

P: ¿Por qué los chunk parsers de profundidad acotada del capítulo 7 no sirven para analizar estructura de oraciones?
R: Porque las oraciones tienen longitud arbitraria, por lo que sus árboles de estructura sintagmática tienen profundidad arbitraria. (Sección "Para qué sirve la sintaxis")

P: ¿Por qué *the worst part and clumsy looking* es agramatical?
R: Por la regla de estructura coordinada: *v1 and v2* solo es de categoría X si v1 y v2 son de la misma categoría X, y aquí se coordina un NP con un AP. (Sección "Para qué sirve la sintaxis")

P: ¿Qué ventaja tiene el shift-reduce frente al descenso recursivo y qué sacrifica?
R: Solo construye estructura que corresponde a las palabras de la entrada y cada subestructura una sola vez; pero al no tener backtracking puede no hallar un análisis existente y encuentra a lo sumo uno. (Sección "Parsing con CFG")

P: ¿Qué significa que un grafo de dependencias sea proyectivo?
R: Que, con las palabras en orden lineal, los arcos no se cruzan; en lenguas de orden más libre abundan las dependencias no proyectivas. (Sección "Dependencias y gramática de dependencias")

P: ¿En qué se diferencian complementos y modificadores?
R: Los complementos son seleccionados por el núcleo según su valencia; los modificadores (adjuntos: PP, adjetivos, adverbios) son opcionales, iterables y no seleccionados por el núcleo. (Sección "Dependencias y gramática de dependencias")

P: ¿Por qué la ambigüedad crece con la cobertura de una gramática y por qué no se resuelve por enumeración?
R: Porque el número de análisis crece según los números de Catalan (1, 2, 5, 14, 42...): una oración de longitud 23 ya tiene miles y una de 50 superaría 10^12; además la ambigüedad léxica es inevitable. (Sección "Desarrollo de gramáticas")

P: ¿Cuál es la solución que propone el capítulo frente a la explosión de análisis ambiguos?
R: El parsing probabilístico: rankear los análisis con evidencia de corpus mediante gramáticas ponderadas (PCFG), de modo que no importa cuántos análisis posibles haya. (Sección "Desarrollo de gramáticas")

## Puntos a dominar

- Entender la gramática generativa: la lengua como conjunto infinito de oraciones gramaticales generado por producciones recursivas.
- Identificar constituyentes por sustituibilidad y reconocer la ambigüedad de attachment del PP sin ambigüedad léxica.
- Escribir y cargar CFG en NLTK (`nltk.parse_cfg`, `nltk.data.load`) respetando sus dos restricciones (no mezclar léxico con categorías, no multipalabra).
- Distinguir recursión directa e indirecta y por qué el descenso recursivo no admite recursión por la izquierda.
- Comparar los cuatro algoritmos de parsing: descenso recursivo, shift-reduce, left-corner y chart parsing con WFST, con sus ventajas y limitaciones.
- Diferenciar estructura sintagmática y gramática de dependencias (núcleo/dependiente, proyectividad, funciones gramaticales).
- Distinguir complementos de modificadores usando la valencia y la subcategorización verbal (TV, IV, DatV, SV).
- Explicar por qué la ambigüedad crece con la cobertura (números de Catalan) y cómo las PCFG con `nltk.ViterbiParser` seleccionan el análisis más probable.
