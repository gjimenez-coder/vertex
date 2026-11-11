# Capítulo 9 — Building Feature-Based Grammars (Construcción de gramáticas basadas en rasgos) — Estudio

## Tarjetas de repaso

P: ¿Qué limitación de las CFG motiva el uso de estructuras de rasgos?
R: Las CFG tratan categorías como S, NP o V como símbolos atómicos, lo que las hace rígidas frente a la riqueza de construcciones del lenguaje natural.

P: ¿Qué es una feature structure (estructura de rasgos)?
R: Un diccionario de pares rasgo-valor donde cada rasgo puede tomar un rango de valores; sustituye a las etiquetas atómicas y permite control fino sin multiplicar reglas.

P: ¿Qué significan los rasgos CAT, ORTH, REF y REL en los ejemplos del capítulo?
R: CAT es la categoría gramatical, ORTH la ortografía, REF el referente y REL la relación; a los verbos se les añaden roles semánticos como AGT (agente) y PAT (paciente).

P: ¿Qué es la concordancia sintáctica (agreement) y qué ejemplos la ilustran?
R: La exigencia de coincidir en número; `this dog`/`these dogs` son correctos pero `*these dog`/`*this dogs` no, igual que `the dog runs` vs. `*the dog run`.

P: ¿Por qué no se codifica la concordancia duplicando no-terminales como NP_SG y NP_PL?
R: Porque cada producción pasaría a tener dos versiones, y extendida a primera, segunda y tercera persona en singular y plural la gramática se multiplicaría por seis, lo que es inasumible.

P: ¿Para qué sirve una variable como `?n` en una producción?
R: Expresa co-variación: `?n` se instancia a `sg` o `pl` dentro de la producción y obliga a que los nodos relacionados tomen el mismo valor de NUM.

P: ¿Qué es un valor booleano y cómo se escribe por convención?
R: Un valor atómico que indica si una propiedad es verdadera o falsa; se escribe `+aux`/`-aux` (equivalente a `aux=+`/`aux=-`) y el parser lo trata como cualquier valor atómico.

P: ¿Qué diferencia hay entre un valor atómico y un valor complejo?
R: Un valor atómico no se descompone (p. ej. `sg`, `pl`); un valor complejo es otra estructura de rasgos, como agrupar persona, número y género bajo AGR.

P: ¿Cómo se construye una estructura de rasgos en NLTK?
R: Con `nltk.FeatStruct()`, pasando valores atómicos o complejos, p. ej. `nltk.FeatStruct(PER=3, NUM='pl', GND='fem')`, o mediante una cadena entre corchetes.

P: ¿Qué es un feature path y cuándo dos caminos son equivalentes?
R: Es una secuencia de arcos desde la raíz representada como tupla (p. ej. `('ADDRESS', 'STREET')`); dos caminos son equivalentes cuando comparten el mismo valor (reparto de estructura o reentrancia).

P: ¿Qué es la subsunción entre estructuras de rasgos?
R: Un orden parcial por generalidad: si FS0 subsume a FS1 (`FS0 ⊑ FS1`), FS0 es más general y FS1 tiene todos sus caminos y equivalencias, y puede tener más.

P: ¿Qué hace la unificación (`unify()`) y cuándo falla?
R: Combina la información de dos estructuras; es binaria y simétrica. Falla (devuelve `None`) si ambas comparten un camino con valores atómicos distintos.

P: ¿Cómo interactúa la unificación con el reparto de estructura?
R: Si la unificación especializa el valor de un camino π, especializa simultáneamente el de cualquier camino equivalente a π.

P: ¿Qué es el rasgo SUBCAT y para qué se usa?
R: Un rasgo en las categorías léxicas que indica la clase de subcategorización (p. ej. `intrans`, `trans`, `clause`), evitando etiquetas atómicas separadas como IV y TV.

P: ¿Qué son las slash categories y qué construcción modelan?
R: Categorías con barra de GPSG donde `Y/XP` es una Y a la que le falta un XP (`S/NP` = `S[SLASH=NP]`); modelan las dependencias no acotadas entre filler y gap.

## Preguntas de autoevaluación

P: ¿Cuáles son las tres preguntas que responde el capítulo?
R: Cómo extender las CFG con rasgos, qué propiedades formales tienen las estructuras de rasgos y cómo usarlas computacionalmente, y qué patrones lingüísticos permiten describir. (Lo que necesitas saber)

P: En las producciones `S -> NP[NUM=?n] VP[NUM=?n]` y `NP[NUM=?n] -> Det[NUM=?n] N[NUM=?n]`, ¿cómo se propaga el número hasta el verbo?
R: Los valores NUM de Det y N deben coincidir para formar el NP; sea cual sea ese NUM, el VP toma el mismo valor, de modo que el número del nombre del sujeto llega al verbo cabeza del VP. (Rasgos gramaticales)

P: ¿Por qué a determinantes como `the`, `some` o `several` no se les especifica NUM?
R: Porque no exigen número; solo se pone una variable cuando restringe otro valor en la misma producción. (Rasgos gramaticales)

P: ¿Cómo parsea NLTK las gramáticas `.fcfg` y qué ventaja tiene su enfoque?
R: Con un Earley chart parser que trabaja directamente con producciones subespecificadas en vez de compilar una CFG gigante totalmente especificada; usa bindings de variables (p. ej. `{?n: 'sg', ?t: 'pres'}`) para instanciar los nodos. (Rasgos gramaticales)

P: ¿Qué aporta agrupar los rasgos de concordancia bajo AGR?
R: Permite usar valores complejos (persona, número, género en una AVM) y refactorizar la gramática empaquetando juntos los rasgos de concordancia; el orden de los rasgos no es significativo. (Terminología / Procesamiento de estructuras de rasgos)

P: ¿Cómo se captura la inversión sujeto-verbo y con qué restricción?
R: Con `S[+INV] -> V[+AUX] NP VP`; la inversión solo ocurre con verbos auxiliares (`do`, `can`, `have`, `be`, `will`, `shall`) en interrogativas y tras adverbios negativos. (Extensión de una gramática basada en rasgos)

P: ¿Qué es una dependencia no acotada y cómo se filtra la información del gap por el árbol?
R: Un complemento obligatorio omitido que deja un gap co-exigido por un filler, sin cota en la distancia entre ambos; la información se percola añadiendo barras con variables (`VP/?x -> V[...] NP/?x`) hasta descargarse con `NP/NP ->` (cadena vacía). (Extensión de una gramática basada en rasgos)

P: ¿Qué papel juega el rasgo OBJCASE en la gramática `german.fcfg`?
R: Especifica el caso que un verbo rige sobre su objeto (los sujetos van en nominativo y la mayoría de verbos rigen acusativo, pero `helfen` rige dativo), combinando AGR con CASE. (Extensión de una gramática basada en rasgos)

## Puntos a dominar

- Entender por qué las categorías atómicas de la CFG se sustituyen por estructuras de rasgos y qué se gana en economía de reglas.
- Saber escribir producciones con variables (`?n`, `?t`) que expresen co-variación y restricciones entre nodos.
- Distinguir valores atómicos, booleanos (`+/- feat`) y complejos, y agrupar rasgos bajo AGR.
- Manejar `nltk.FeatStruct()`, el acceso por índice y la notación de cadena entre corchetes.
- Interpretar estructuras de rasgos como DAG, identificar feature paths y la reentrancia con índices numéricos en las AVM.
- Explicar subsunción y unificación, incluido su fallo por valores atómicos distintos y su interacción con el reparto de estructura.
- Modelar con rasgos la subcategorización (SUBCAT), la sintaxis X-barra (BAR), la inversión (`+INV`/`+AUX`), las dependencias no acotadas (slash categories) y el régimen de caso (OBJCASE).
- Reconocer que NLTK parsea `.fcfg` con un Earley chart parser sobre producciones subespecificadas y bindings de variables.
