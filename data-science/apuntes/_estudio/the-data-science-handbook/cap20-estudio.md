# Programming Language Concepts (Conceptos de lenguajes de programación) — Estudio

## Tarjetas de repaso

P: ¿Qué es un "paradigma de programación"? / R: Una manera conceptual de pensar la estructura lógica de un programa y plasmarla en código (una secuencia de instrucciones, una especificación matemática de la salida, u otras opciones).

P: ¿Cuáles son los tres grandes paradigmas? / R: Imperativo, funcional y orientado a objetos.

P: ¿En qué consiste la programación imperativa? / R: El código es sobre todo una secuencia de instrucciones que la computadora sigue (añadir a una lista, sobrescribir una variable, escribir un archivo).

P: ¿Qué son los "side effects" y por qué evitarlos en lo funcional? / R: Cualquier modificación de variables existentes o interacción con el exterior (imprimir); dificultan razonar sobre el código porque el orden de los pasos importa y cuesta seguirlo.

P: ¿Qué es una función "pura"? / R: Una función que recibe una entrada (o ninguna) y devuelve una salida sin efectos secundarios.

P: ¿Cuál es el "verdadero nirvana funcional"? / R: No solo organizar el código en funciones puras, sino tratar a las funciones como variables: pasarlas como argumentos o generarlas al vuelo.

P: ¿Por qué lo funcional encaja con la ciencia de datos? / R: Por el batch processing: hay una secuencia clara de etapas desde los datos crudos hasta la salida, sin interacciones de usuario difíciles de modelar como funciones puras (Spark es un framework funcional).

P: ¿Qué es un objeto en el paradigma orientado a objetos? / R: Una caja negra que empaqueta datos y la lógica que los maneja; se interactúa con él solo mediante funciones de propósito especial llamadas "métodos".

P: ¿Qué representa el argumento `self` en Python? / R: El propio objeto, que se pasa silenciosamente como primer argumento al llamar un método; por convención se llama `self`.

P: ¿Qué hace `__init__` y por qué no es técnicamente un constructor? / R: Construye/inicializa el objeto al crearse, pero en Python el objeto ya existe antes de invocarlo (solo le faltan los campos).

P: ¿Qué es la herencia (inheritance) y qué pasa con `__init__` al heredar? / R: Una clase hija hereda lógica y métodos de la clase padre; si define su propio `__init__`, este anula por completo al del padre y el programador debe llamarlo explícitamente para rescatar lo que necesite.

P: ¿Cuál es la diferencia entre "compile time" y "run time"? / R: Un error de sintaxis aparece al compilar; otros problemas solo se descubren al ejecutar el machine code, por lo que el diseño de compiladores busca detectar fallos en compile time.

P: ¿Qué diferencia a un lenguaje compilado de uno interpretado? / R: El compilado traduce el código a machine code que ejecuta el microprocesador; el interpretado lee y ejecuta el código línea a línea sin traducirlo a machine code.

P: ¿Qué distingue tipado estático de dinámico? / R: Estático determina los tipos en compile time (almacenamiento eficiente); dinámico no los conoce hasta run time, con boilerplate para rastrearlos (Python usa `PyObject`).

P: ¿Qué es el "duck typing"? / R: Una variable es del tipo "correcto" si toda operación llamada sobre ella está definida (si tiene `quack()` y `walk()`, es un pato).

## Preguntas de autoevaluación

P: ¿Por qué importa entender los conceptos núcleo de los lenguajes según el capítulo? / R: Porque dictan qué herramienta conviene en cada caso (para no quedar atrapado en la tecnología equivocada al construir frameworks grandes) y facilitan la transición al adoptar una herramienta muy distinta. (Sección: Lo que necesitas saber)

P: ¿Son los paradigmas equivalentes? Explica el matiz. / R: Sí, todos son equivalentes en poder de cómputo (lo que se computa con uno se computa con los demás), pero conceptualmente son muy distintos y se prestan a aplicaciones y temperamentos diferentes. (Sección: Lo que necesitas saber / Paradigmas de programación)

P: ¿Qué ventaja de rendimiento se le atribuye a lo funcional y qué matiz añade Cady? / R: Un programa funcional es más una especificación matemática que instrucciones, así que en teoría el compilador puede implementarlo muy eficientemente; en la práctica el compilador no suele ser tan listo y lo hace de forma ingenua, y en lenguajes interpretados será lento. (Sección: Funcional)

P: ¿Por qué hacer código 100% funcional resulta incómodo en Python? / R: Obliga a sustituir bucles por recursión, ineficiente en Python por el boilerplate de las llamadas anidadas, ya que Python carece de "tail call optimization" (que sí tienen lenguajes como Haskell). (Sección: Funcional)

P: ¿Cuándo brilla el código orientado a objetos? / R: Al interactuar con recursos externos: una GUI, dos procesos que se comunican, un iPhone, una web interactiva o el usuario en el bucle, modelados como interacciones entre objetos vía sus métodos. (Sección: Orientado a objetos)

P: ¿Por qué se dice que compilación e interpretación son hoy un continuo? / R: El bytecode (Python, la JVM de Java, .NET), la traducción x86→RISC codificada en el silicio de Intel y la compilación just-in-time (JIT) difuminan la frontera entre ambas. (Sección: Compilación e interpretación)

P: ¿Cómo gestiona Python los tipos y qué coste tiene? / R: Es dinámico: cada variable es una estructura C `PyObject` que guarda el tipo, lo que cuesta RAM y obliga a comprobar el tipo antes de cada operación; gran flexibilidad a cambio de rendimiento. (Sección: Sistemas de tipos)

P: ¿En qué sentido Python es de tipado fuerte y en cuál débil? / R: Fuerte al rechazar `"hello" + 5`; débil al aceptar tanto `3/2` como `3.0/2` con resultados distintos (OCaml daría error de compilación). (Sección: Sistemas de tipos)

## Puntos a dominar

- Distinguir los tres paradigmas (imperativo, funcional, orientado a objetos) y reconocer que son equivalentes en cómputo pero conceptualmente distintos.
- Identificar qué es un side effect y cómo lo evita el paradigma funcional mediante funciones puras y funciones tratadas como variables.
- Saber cuándo encaja cada paradigma: funcional con batch processing/ciencia de datos (Spark), orientado a objetos con recursos externos y usuarios.
- Entender en Python el rol de `self`, `__init__` y la herencia (incluido que `__init__` del hijo anula al del padre).
- Diferenciar compile time de run time y por qué conviene detectar errores pronto.
- Ubicar los lenguajes en el continuo compilación–interpretación (machine code, bytecode, JVM/.NET, JIT, x86→RISC).
- Diferenciar los dos ejes de los sistemas de tipos: estático vs. dinámico y fuerte vs. débil, con Python y C como referencias, y reconocer el duck typing.
