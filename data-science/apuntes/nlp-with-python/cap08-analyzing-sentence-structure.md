# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 8 — Analyzing Sentence Structure (Análisis de la estructura de las oraciones)

> Nota de extracción: el texto procede de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber
El capítulo pasa del nivel de las palabras y los n-gramas al de la oración, donde aparecen dos problemas que los métodos anteriores no resuelven: la ambigüedad del lenguaje natural y el hecho de que el número de oraciones posibles es ilimitado mientras que los programas son finitos. La tesis es que una gramática formal —una notación capaz de generar el conjunto de las oraciones gramaticales— permite describir esa infinitud y que los árboles sintácticos permiten representar su estructura.

Se adopta el marco de la gramática generativa: una "lengua" se entiende como el enorme conjunto de todas las oraciones gramaticales, y la gramática es la notación que genera sus miembros mediante producciones recursivas del tipo `S → S and S`. Sobre esa base se introducen las gramáticas de estructura sintagmática libres de contexto (CFG), las gramáticas de dependencias, y varios algoritmos de análisis (parsing).

Sales sabiendo: distinguir constituyentes por sustituibilidad; escribir y cargar CFG en NLTK; reconocer la ambigüedad de attachment de sintagmas preposicionales; usar cuatro estrategias de parsing (descenso recursivo, shift-reduce, left-corner y chart parsing con WFST); diferenciar complementos de modificadores vía valencia; y entender por qué la ambigüedad crece con la cobertura, lo que motiva las gramáticas ponderadas (PCFG).

## El ejemplo que recorre el capítulo
La oración ambigua de Groucho Marx, "I shot an elephant in my pajamas" (PDF p. 315), es el hilo conductor. El sintagma preposicional *in my pajamas* puede describir al elefante o al acto de disparar, lo que produce dos árboles distintos sin que ninguna palabra sea ambigua. El mismo caso reaparece con la gramática `groucho_grammar`, con la gramática de dependencias y con la tabla WFST, mostrando cómo cada formalismo captura la misma ambigüedad de attachment.

## Algunos dilemas gramaticales
Si imaginamos un corpus con todo lo dicho o escrito en inglés en 50 años, no equivaldría a "el inglés moderno": los hablantes rechazan secuencias como *the of* por agramaticales, y a la vez aceptan oraciones nuevas jamás pronunciadas. Las oraciones pueden incrustarse unas en otras (plantillas como *Andre said S*, *S but S*, *S when S*), lo que permite construir oraciones arbitrariamente largas —como el extenso pasaje de Winnie the Pooh citado—, con estructura simple del tipo `S but S when S`. Esta propiedad recursiva es la que una gramática generativa busca modelar.

La ambigüedad es ubicua. En la oración de Groucho se define una CFG simple y se analiza con `nltk.ChartParser`, que devuelve dos estructuras: en una el PP cuelga del NP (el elefante estaba en el pijama) y en otra del VP (el disparo ocurrió en el pijama). El capítulo presenta gramáticas y parsers como los métodos formales y computacionales para investigar estos fenómenos, con la comprensión del lenguaje natural como motivación central.

## Para qué sirve la sintaxis
Los n-gramas generan texto aceptable en tramos cortos pero degeneran en "ensalada de palabras". La gramática aporta vocabulario para explicar por qué. La estructura coordinada ilustra una regla: si v1 y v2 son sintagmas de la misma categoría X, *v1 and v2* también es de categoría X; por eso *the worst part and clumsy looking* (NP + AP) es agramatical.

La estructura de constituyentes se basa en la sustituibilidad: una secuencia que forma unidad puede reemplazarse por una más corta sin volver la oración mal formada (se puede sustituir *The little bear* por *He*, pero no *little bear saw*). Añadiendo etiquetas de categoría (NP, VP, PP, Nom) y un nodo S se obtiene un árbol de estructura sintagmática estándar; cada nodo es un constituyente. Como las oraciones tienen longitud arbitraria, los árboles tienen profundidad arbitraria, por lo que los chunk parsers de profundidad acotada del capítulo 7 no sirven aquí.

## Gramática libre de contexto (CFG)
Por convención, el lado izquierdo de la primera producción es el símbolo inicial (normalmente S), raíz de todo árbol bien formado. En NLTK las CFG se definen en `nltk.grammar`:

```python
grammar1 = nltk.parse_cfg("""
  S -> NP VP
  VP -> V NP | V NP PP
  PP -> P NP
  V -> "saw" | "ate" | "walked"
  NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
  Det -> "a" | "an" | "the" | "my"
  N -> "man" | "dog" | "cat" | "telescope" | "park"
  P -> "in" | "on" | "by" | "with"
  """)
```

Las categorías sintácticas son S (oración), NP (sintagma nominal), VP (verbal), PP (preposicional), Det (determinante), N (nombre), V (verbo) y P (preposición). La barra `|` es una disyunción abreviada. Al analizar *The dog saw a man in the park* se obtienen dos árboles: el sentido es estructuralmente ambiguo por el attachment del PP, que puede colgar del VP o del NP.

Se pueden escribir CFG en un fichero `.cfg` y cargarlas con `nltk.data.load('file:mygrammar.cfg')`. Dos restricciones en NLTK: no se mezclan categorías gramaticales con ítems léxicos en el mismo lado derecho (prohibido `PP -> 'of' NP`), ni se ponen ítems léxicos multipalabra (usar `NP -> 'New_York'`).

Una gramática es recursiva si una categoría del lado izquierdo reaparece en el derecho: recursión directa en `Nom -> Adj Nom`, o indirecta en S vía `S -> NP VP` y `VP -> V S`. No hay límite de profundidad, aunque el parser de descenso recursivo no admite producciones recursivas por la izquierda (`X -> X Y`).

## Parsing con CFG
Una gramática es una especificación declarativa de buena formación (es solo una cadena); un parser es su interpretación procedimental, que busca en el espacio de árboles licenciados uno cuya frontera sea la oración. Sirve para evaluar gramáticas, modelar el procesamiento psicolingüístico y como paso inicial en aplicaciones como los sistemas de preguntas y respuestas. Se ven cuatro algoritmos.

El descenso recursivo (top-down) interpreta la gramática como la descomposición de un objetivo (hallar una S) en subobjetivos (hallar NP, luego VP), hasta llegar a palabras que se comparan con la entrada; si no coinciden, retrocede (backtracking). Construye el árbol de arriba abajo (`nltk.RecursiveDescentParser`). Tiene tres defectos: las producciones recursivas por la izquierda lo meten en bucle infinito; pierde tiempo considerando estructuras que no corresponden a la entrada; y el backtracking descarta constituyentes ya construidos que luego debe rehacer.

El shift-reduce (bottom-up) usa una pila: la operación *shift* empuja la siguiente palabra; la operación *reduce* sustituye los n ítems de la cima que coinciden con el lado derecho de una producción por su lado izquierdo. Termina cuando toda la entrada se ha consumido y queda un único S en la pila (`nltk.ShiftReduceParser`). No implementa backtracking, por lo que puede no hallar un análisis existente y encuentra a lo sumo uno. Debe resolver conflictos shift-reduce y reduce-reduce. Su ventaja: solo construye estructura que corresponde a las palabras de la entrada, y cada subestructura una sola vez.

El left-corner parser es un híbrido: un parser top-down con filtrado bottom-up que no cae en las producciones recursivas por la izquierda. Preprocesa la gramática en una tabla que asocia a cada no terminal sus posibles "esquinas izquierdas" (preterminales), y comprueba que la palabra siguiente sea compatible con alguna antes de aplicar una producción.

Las tablas de subcadenas bien formadas (WFST) aplican programación dinámica: se construye una vez cada constituyente (p. ej. el PP *in my pajamas*) y se guarda en una tabla para reutilizarlo. En una matriz triangular, el eje vertical marca la posición inicial y el horizontal la final; se añade A en la celda (i, j) si existe una producción `A → B C` con B en (i, k) y C en (k, j). Construir un S en la celda (0, 7) indica que hay análisis para toda la entrada. `init_wfst()` inicializa la matriz con las categorías léxicas y `complete_wfst()` la completa. Limitaciones: la WFST no es un árbol (solo reconoce), exige producciones binarias, puede proponer constituyentes no licenciados y no representa la ambigüedad estructural (una entrada sobrescribe la otra). Los chart parsers resuelven esto con una estructura más rica.

## Dependencias y gramática de dependencias
A diferencia de la estructura sintagmática, la gramática de dependencias describe cómo se relacionan las palabras entre sí. La dependencia es una relación binaria asimétrica entre un núcleo (head) y sus dependientes; el núcleo de la oración suele ser el verbo conjugado, y toda palabra depende de él directa o indirectamente. Se representa como un grafo dirigido etiquetado, donde los arcos van del núcleo al dependiente y la etiqueta indica la función gramatical (p. ej. *I* es SBJ de *shot*, *in* es NMOD de *elephant*). En NLTK se define con `nltk.parse_dependency_grammar` y se analiza con `nltk.ProjectiveDependencyParser`, que para la oración de Groucho vuelve a producir las dos lecturas. Un grafo es proyectivo si, con las palabras en orden lineal, los arcos no se cruzan; en lenguas de orden más libre abundan las dependencias no proyectivas. El capítulo lista criterios para decidir núcleo y dependiente (el núcleo determina la distribución y el tipo semántico de la construcción, es obligatorio, selecciona al dependiente, etc.) y señala que las CFG ya incorporan implícitamente dependencias (un PP tiene como núcleo la preposición).

Los verbos se distinguen por su valencia: los complementos que admiten. Según la gramática, *was* va con Adj, *saw* con NP, *thought* con S y *put* con NP PP; otras combinaciones son agramaticales. En una CFG esto se controla subcategorizando los verbos: TV (transitivo), IV (intransitivo), DatV (dativo), SV (sentencial). Los complementos se oponen a los modificadores (o adjuntos: PP, adjetivos, adverbios), que son opcionales, iterables y no seleccionados por el núcleo.

## Desarrollo de gramáticas
Escribir a mano gramáticas de amplia cobertura es muy difícil: cuesta modularizarlas y, al crecer la cobertura, crece la ambigüedad. Existen proyectos a gran escala como LFG Pargram, HPSG LinGO Matrix y el XTAG Project. NLTK da acceso a treebanks (una muestra del 10% del Penn Treebank vía `nltk.corpus.treebank`), que permiten descubrir, p. ej., qué verbos toman complementos oracionales o cómo el verbo determina el attachment del PP (`nltk.corpus.ppattach`).

La ambigüedad es perniciosa: con oraciones *fish fish fish...* el número de análisis crece según los números de Catalan (1, 2, 5, 14, 42...); una oración de longitud 23 (media del WSJ) ya tiene miles, y una de 50 superaría los 10^12. A esto se suma la ambigüedad léxica inevitable en gramáticas amplias (casi cualquier nombre puede ser verbo; hasta *the a are of I* es un NP gramatical). La solución es el parsing probabilístico: rankear los análisis con evidencia de corpus. Una gramática ponderada, y en concreto una PCFG (`nltk.parse_pcfg`), asocia una probabilidad a cada producción; la probabilidad de un análisis es el producto de las de sus producciones, y las producciones con un mismo lado izquierdo deben sumar 1. El `nltk.ViterbiParser` halla el análisis más probable, de modo que ya no importa cuántos análisis posibles haya.

## Ideas clave
- Una gramática es una caracterización compacta de un conjunto potencialmente infinito de oraciones; la recursión, los núcleos, los complementos y los modificadores son rasgos clave de la estructura de constituyentes.
- Las CFG analizan un sintagma de categoría A en una secuencia de partes menores mediante producciones; el símbolo inicial suele ser S.
- Los constituyentes se identifican por sustituibilidad; la ambigüedad de attachment del PP produce múltiples árboles sin ambigüedad léxica.
- Descenso recursivo (top-down): no admite recursión por la izquierda y repite trabajo; shift-reduce (bottom-up): no garantiza hallar el análisis ni lo hace globalmente consistente.
- El left-corner combina top-down con filtrado bottom-up; el chart parsing con WFST usa programación dinámica para reutilizar constituyentes.
- La gramática de dependencias expresa funciones gramaticales entre núcleo y dependientes; la valencia determina qué complementos admite cada verbo.
- La ambigüedad crece con la cobertura (números de Catalan) y es insoluble por enumeración.
- Las gramáticas ponderadas y las PCFG asignan probabilidades a los análisis, permitiendo elegir el más probable.
