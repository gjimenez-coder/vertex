# Natural Language Processing with Python — Steven Bird, Ewan Klein & Edward Loper (O'Reilly, 2009)
## Capítulo 9 — Building Feature-Based Grammars (Construcción de gramáticas basadas en rasgos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`. Se han conservado solo las sesiones interactivas esenciales y resumido el resto.

## Lo que necesitas saber
Las gramáticas libres de contexto (CFG) tratan categorías como S, NP o V como símbolos atómicos, lo que las hace rígidas frente a la riqueza de las construcciones gramaticales del lenguaje natural. Este capítulo sustituye esas etiquetas atómicas por estructuras de rasgos (feature structures): diccionarios donde cada rasgo puede tomar un rango de valores. Así se gana control fino sobre categorías y producciones sin multiplicar el número de reglas.

La tesis central es que, al añadir rasgos con variables y restricciones de unificación, podemos capturar fenómenos como la concordancia (agreement), la subcategorización, la inversión y las dependencias no acotadas de forma elegante y económica. El capítulo responde a tres preguntas: cómo extender las CFG con rasgos, qué propiedades formales tienen las estructuras de rasgos y cómo usarlas computacionalmente, y qué patrones lingüísticos permiten describir.

Sales sabiendo declarar rasgos en gramáticas `.fcfg` de NLTK, usar variables como `?n` para expresar co-variación entre nodos, manipular estructuras de rasgos con `nltk.FeatStruct()`, entender subsunción y unificación (incluido el reparto de estructura o reentrancia), y aplicar todo ello a casos de inglés y alemán.

## Rasgos gramaticales
En lugar de extraer rasgos automáticamente (como en los clasificadores del capítulo 6), aquí se declaran los rasgos de palabras y frases. Un ejemplo simple usa diccionarios: `kim = {'CAT': 'NP', 'ORTH': 'Kim', 'REF': 'k'}` y `chase = {'CAT': 'V', 'ORTH': 'chased', 'REL': 'chase'}`. CAT es la categoría gramatical y ORTH la ortografía; REF da el referente y REL la relación. A un verbo se le pueden añadir roles semánticos (AGT agente, PAT paciente) que se ligan al sujeto y al objeto cuando el verbo se combina con sus argumentos. Estos pares rasgo-valor se llaman feature structures, pero manipularlos a mano es muy ad hoc; el objetivo es integrarlos en el marco de la CFG y el parsing.

El fenómeno motivador es la concordancia sintáctica. En inglés, `this dog`/`these dogs` son correctos, pero `*these dog`/`*this dogs` no: el demostrativo y el nombre deben coincidir en número. Lo mismo ocurre entre sujeto y verbo (`the dog runs` vs. `*the dog run`). El verbo en presente tiene dos formas: tercera persona del singular (`runs`) y el resto (`run`).

Si codificamos la concordancia duplicando no-terminales (`NP_SG`, `NP_PL`, `VP_SG`, `VP_PL`...), cada producción pasa a tener dos versiones; extendido a primera, segunda y tercera persona en singular y plural, la gramática se multiplicaría por seis. Es inasumible.

La solución elegante es usar atributos y restricciones. Se anota la categoría con un rasgo y su valor, por ejemplo `N[NUM=pl]`, y se introducen variables sobre los valores. Con `?n` como variable del rasgo NUM, las producciones expresan co-variación:

```
S -> NP[NUM=?n] VP[NUM=?n]
NP[NUM=?n] -> Det[NUM=?n] N[NUM=?n]
VP[NUM=?n] -> V[NUM=?n]
```

`?n` se instancia a `sg` o `pl` dentro de cada producción: sea cual sea el NUM del NP, el VP debe tomar el mismo valor. Al construir el árbol, los valores NUM de Det y N deben coincidir para formar un NP; si difieren, la combinación falla. Así, el valor NUM del nombre del sujeto se propaga hasta el verbo cabeza del VP. Para determinantes que no exigen número (como `the`, `some`, `several`) basta con no especificar NUM; solo se pone una variable cuando restringe otro valor en la misma producción.

La gramática `feat0.fcfg` de NLTK reúne estas ideas, incluyendo rasgos múltiples como `V[TENSE=pres, NUM=pl]` y la directiva `% start S`, que fija S como símbolo inicial. Las gramáticas basadas en rasgos se parsean en NLTK con un Earley chart parser:

```python
>>> tokens = 'Kim likes children'.split()
>>> from nltk import load_parser
>>> cp = load_parser('grammars/book_grammars/feat0.fcfg', trace=2)
>>> trees = cp.nbest_parse(tokens)
```

El parser trabaja directamente con las producciones subespecificadas en vez de compilar una CFG gigante totalmente especificada. Los valores "fluyen hacia arriba" desde las entradas léxicas y las variables se asocian mediante bindings (diccionarios como `{?n: 'sg', ?t: 'pres'}`); con ellos se instancian los nodos del árbol.

## Terminología
Los valores vistos (`sg`, `pl`) son atómicos: no se descomponen. Un caso especial son los valores booleanos, que indican si una propiedad es verdadera o falsa, por convención `+aux`/`-aux` (equivalentes a `aux=+`/`aux=-`); el parser los trata como cualquier otro valor atómico. La categoría completa (no-terminal más anotación) puede verse como un paquete de rasgos: `N[NUM=sg]` equivale a `[POS=N, NUM=sg]`.

Además de valores atómicos, un rasgo puede tener como valor otra estructura de rasgos (valor complejo). Por ejemplo, los rasgos de concordancia (persona, número, género) se agrupan bajo AGR, y se muestran en una matriz atributo-valor (AVM). El orden de los rasgos no es significativo. Con AGR se puede refactorizar la gramática para empaquetar los rasgos de concordancia juntos.

## Procesamiento de estructuras de rasgos
Las estructuras de rasgos son estructuras de datos de propósito general para representar conocimiento, no solo objetos lingüísticos (por ejemplo, datos de una persona). En NLTK se construyen con `FeatStruct()`, con valores atómicos (cadenas o enteros) o complejos:

```python
>>> fs1 = nltk.FeatStruct(PER=3, NUM='pl', GND='fem')
>>> fs2 = nltk.FeatStruct(POS='N', AGR=fs1)
```

Como son diccionarios, se accede por índice (`fs2['AGR']['PER']`). También se pueden definir con una cadena entre corchetes: `nltk.FeatStruct("[POS='N', AGR=[PER=3, NUM='pl', GND='fem']]")`.

Es útil verlas como grafos acíclicos dirigidos (DAG): los rasgos son etiquetas de los arcos y los valores son nodos. Un feature path (camino de rasgos) es una secuencia de arcos desde la raíz, representada como tupla, p. ej. `('ADDRESS', 'STREET')`. Cuando dos caminos comparten el mismo valor (misma subestructura), hay reparto de estructura (structure sharing) o reentrancia (reentrancy), y se dice que los caminos son equivalentes. En la notación de matriz, la primera aparición se marca con un entero entre paréntesis `(1)` (tag o coíndice) y las referencias posteriores con `->(1)`:

```python
>>> nltk.FeatStruct("[A='a', B=(1)[C='c'], D->(1), E->(1)]")
```

### Subsunción y unificación
Las estructuras de rasgos aportan información parcial y se ordenan por generalidad. Si FS0 subsume a FS1 (`FS0 ⊑ FS1`), FS0 es más general: FS1 tiene todos los caminos y equivalencias de FS0 y puede tener más. Es un orden parcial: hay estructuras incomparables.

Combinar la información de dos estructuras es la unificación (`unify()`), operación binaria y simétrica:

```python
>>> fs1 = nltk.FeatStruct(NUMBER=74, STREET='rue Pascal')
>>> fs2 = nltk.FeatStruct(CITY='Paris')
>>> print fs1.unify(fs2)
[ CITY   = 'Paris'      ]
[ NUMBER = 74           ]
[ STREET = 'rue Pascal' ]
```

Si una estructura subsume a la otra, el resultado es la más específica. La unificación falla (devuelve `None`) si ambas comparten un camino con valores atómicos distintos. Lo más interesante es su interacción con el reparto de estructura: si la unificación especializa el valor de un camino π, especializa simultáneamente el de cualquier camino equivalente a π. El reparto también se expresa con variables como `?x` (`[ADDRESS1=?x, ADDRESS2=?x]`).

## Extensión de una gramática basada en rasgos
Subcategorización. En vez de etiquetas atómicas separadas para verbos intransitivos (IV) y transitivos (TV), se usa un rasgo SUBCAT en las categorías léxicas que indica la clase de subcategorización. Con valores mnemónicos `intrans`, `trans`, `clause` (enfoque de Generalized Phrase Structure Grammar, GPSG):

```
VP[TENSE=?t, NUM=?n] -> V[SUBCAT=intrans, TENSE=?t, NUM=?n]
VP[TENSE=?t, NUM=?n] -> V[SUBCAT=trans, TENSE=?t, NUM=?n] NP
VP[TENSE=?t, NUM=?n] -> V[SUBCAT=clause, TENSE=?t, NUM=?n] SBar
```

Así, `walk` y `like` son ambos categoría V, pero solo aparecen en VP expandidos por la producción con el SUBCAT correcto. SBar etiqueta cláusulas subordinadas (`SBar -> Comp S`, `Comp -> 'that'`). Un enfoque alternativo (gramática categorial, PATR, HPSG) usa SUBCAT para codificar directamente la valencia como lista de argumentos, p. ej. `V[SUBCAT=<NP, NP, PP>]` para `put`; una oración tiene SUBCAT con lista vacía.

Cabezas y sintaxis X-barra. Los V son cabezas de VP, los N de NP, etc. La sintaxis X-barra abstrae el nivel sintagmático en tres niveles: N (nivel léxico), N' (nivel intermedio, Nom) y N'' (sintagmático, NP). Se codifica con un rasgo BAR; los complementos subcategorizados son hermanos de la cabeza y los adjuntos hermanos del nivel intermedio X'.

Auxiliares e inversión. En interrogativas y tras adverbios negativos el orden sujeto-verbo se invierte, pero solo con verbos auxiliares (`do`, `can`, `have`, `be`, `will`, `shall`). Se captura con `S[+INV] -> V[+AUX] NP VP`.

Dependencias no acotadas. Complementos obligatorios pueden omitirse si hay un filler apropiado (palabra interrogativa, tópico antepuesto), dejando un gap (hueco). El filler y el gap se co-exigen mutuamente ("dependencia"). No hay cota superior en la distancia entre filler y gap (recursión de complementos oracionales), de ahí el nombre unbounded dependency construction. Se tratan con categorías con barra (slash categories) de GPSG: `Y/XP` es una Y a la que le falta un XP. Se integran como rasgo: `S/NP` equivale a `S[SLASH=NP]`. La información del gap se "filtra" (percola) por el árbol añadiendo barras con variables (`VP/?x -> V[...] NP/?x`) hasta descargarse con `NP/NP ->` (cadena vacía). La gramática `feat1.fcfg` parsea `who do you claim that you like`, oraciones sin gap y oraciones invertidas sin wh.

Caso y género en alemán. El alemán tiene morfología de concordancia más rica: el artículo definido varía en caso, género y número. Los sujetos van en nominativo y la mayoría de verbos rigen acusativo en el objeto, pero hay excepciones como `helfen`, que rige dativo. La gramática `german.fcfg` usa el rasgo `OBJCASE` para especificar el caso que un verbo rige sobre su objeto, combinando AGR (persona, número, género) con CASE. Ante un fallo de parsing, el parámetro `trace` del parser muestra dónde falla la unificación (p. ej. el AGR de `Katze` no unifica con ninguno de los AGR de `den`).

## Ideas clave
- Las categorías atómicas de la CFG se sustituyen por estructuras de rasgos para captar distinciones finas sin multiplicar las categorías ni las producciones.
- Las variables sobre valores de rasgos (`?n`, `?t`) expresan restricciones que hacen interdependientes las realizaciones de los rasgos entre nodos.
- Los valores se fijan en el nivel léxico y en los sintagmas se obligan a unificar con los de sus hijos; los valores pueden ser atómicos o complejos, con el caso booleano `[+/- feat]`.
- Dos rasgos pueden compartir un valor (reentrancia), marcado con índices numéricos en las AVM; un camino es una tupla de rasgos desde la raíz y dos caminos son equivalentes si comparten valor.
- Las estructuras de rasgos están parcialmente ordenadas por subsunción: FS0 subsume a FS1 cuando es más general; la unificación combina la información de ambas si tienen éxito.
- Si la unificación especializa un camino π, especializa también todo camino equivalente a π.
- Con rasgos se modelan de forma concisa la subcategorización verbal, la inversión, las dependencias no acotadas (slash categories) y el régimen de caso.
- NLTK parsea gramáticas `.fcfg` con un Earley chart parser que trabaja con producciones subespecificadas y usa bindings de variables para instanciar los nodos.
