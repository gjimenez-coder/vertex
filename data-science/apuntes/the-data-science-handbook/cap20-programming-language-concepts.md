# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 20 — Programming Language Concepts (Conceptos de lenguajes de programación)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; contenía fragmentos de código de los que se conservan solo los esenciales. Las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo da un paso atrás respecto al scripting rápido del resto del libro y entra en los aspectos más abstractos y teóricos de los lenguajes de programación. Importa por dos razones: estas consideraciones dictan qué herramienta conviene usar en cada caso (para no quedar atrapado en la tecnología equivocada, sobre todo al construir un framework grande), y entender los conceptos núcleo facilita la transición cuando hay que adoptar una herramienta muy distinta a la habitual.

La tesis central es que la mayoría de los lenguajes modernos de alto nivel soportan, en mayor o menor grado, todos los paradigmas, de modo que se pueden mezclar según lo que convenga al problema. Aunque todos los paradigmas son equivalentes (lo que se puede computar con uno se puede computar con los demás), conceptualmente son muy distintos y se prestan a aplicaciones y temperamentos diferentes.

Sales sabiendo los tres grandes paradigmas (imperativo, funcional y orientado a objetos), la diferencia entre compilación e interpretación (hoy un continuo más que una dicotomía) y los dos ejes de los sistemas de tipos: estático frente a dinámico y fuerte frente a débil. Python se usa como hilo conductor porque soporta parcialmente los tres paradigmas.

## Paradigmas de programación

Un "paradigma de programación" es una manera conceptual de pensar la estructura lógica de un programa y plasmarla en código: una secuencia de instrucciones, una especificación matemática de la salida, u otras opciones. Los tres grandes son imperativo, orientado a objetos y funcional.

### Imperativo

En programación imperativa el código es, sobre todo, una secuencia de instrucciones que la computadora sigue: añadir un elemento a una lista, sobrescribir una variable en memoria, escribir un archivo. Cady muestra como ejemplo leer un CSV demográfico y calcular la edad media por estado recorriendo las líneas y acumulando resultados en diccionarios con bucles `for`.

### Funcional

La programación funcional nace del deseo de evitar los "side effects" (efectos secundarios): cualquier modificación de variables existentes (añadir a una lista, incrementar un número) o cualquier interacción con el exterior (imprimir en pantalla). Los efectos son necesarios para que el código haga algo, pero dificultan razonar sobre él: el orden de los pasos importa y cuesta seguirlo. Cady lo ilustra con una anécdota: al reejecutar un script desde cero las cosas se rompían porque versiones previas del código ya habían aplicado side effects que él había olvidado.

En este paradigma el código se divide en funciones "puras", que reciben una entrada (o ninguna) y devuelven una salida sin efectos secundarios. El verdadero nirvana funcional no es solo organizar el código en funciones puras, sino tratar a las funciones como variables: pasarlas como argumentos a otras funciones o generarlas al vuelo.

Un ejemplo típico es una función que devuelve otra función. `get_year_extractor` examina el formato de una fecha de muestra y devuelve un `lambda` que extrae el año de cadenas con ese mismo formato:

```python
def get_year_extractor(example_date):
    if len(example_date) == 8: return lambda d: d[:4]
    elif example_date[4] == '-' and example_date[7] == '-':
        return lambda d: d[:4]
    else: return lambda d: d[-4:]
```

Otro patrón habitual en analítica es pasar una función `f` como argumento a `get_stats`, de modo que se pueda experimentar con muchas funciones personalizadas y ver cómo rinden.

La programación funcional encaja bien con la ciencia de datos, sobre todo en batch processing: hay una secuencia clara de etapas lógicas desde los datos crudos hasta la salida, sin interacciones de usuario difíciles de modelar como funciones puras. En Big Data, Spark es un framework funcional. Una ventaja muy pregonada es el rendimiento, al menos si el código se compila: un programa funcional es más una especificación matemática que un conjunto de instrucciones, y en teoría el compilador puede implementarlo de forma muy eficiente. En la práctica el compilador no suele ser tan listo y lo hace de forma ingenua; en lenguajes interpretados será lento.

La sintaxis funcional puede resultar incómoda en ciertas estructuras de control: hacer 100% funcional obliga a sustituir bucles por recursión, algo ineficiente en Python por el boilerplate de las llamadas anidadas (Python carece de "tail call optimization", que sí tienen lenguajes compilados como Haskell). El abuelo de los lenguajes funcionales es Lisp (1958); hoy destacan Haskell, ML y Scala (que también admite estilo orientado a objetos).

### Orientado a objetos

Un lenguaje orientado a objetos empaqueta datos y la lógica que los maneja en cajas negras amigables llamadas "objetos". Al usar un objeto no te preocupas por cómo se estructuran los datos; solo interactúas con funciones de propósito especial llamadas "métodos". Python es intrínsecamente orientado a objetos: todo (variables, funciones, librerías) es un objeto y toda acción es llamar a un método. Incluso `x + y` es azúcar sintáctico sobre `x.__add__(y)`. Aun así, no estás obligado a escribir en ese estilo; Cady rara vez define clases propias y usa contenedores built-in, con código que lee como mezcla de imperativo y funcional.

El código orientado a objetos brilla cuando interactúa con recursos externos: una GUI, dos procesos que se comunican, un iPhone, una web interactiva o el usuario dentro del bucle se modelan mejor como interacciones entre objetos vía sus métodos (cada pulsación cambia el estado interno del objeto, es decir, un side effect).

La característica clave del paradigma es definir tipos nuevos de objetos, llamados "clases". Una clase especifica la estructura interna y los métodos; puede haber muchos objetos de la misma clase, definida una sola vez:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def talk(self):
        print('My name is %s and I am %s years old' % (self.name, self.age))
```

El argumento `self` desconcierta a muchos: al llamar un método, el propio objeto se pasa silenciosamente como primer argumento, y por convención se llama `self`. Referirse a `self.age` elimina la ambigüedad sobre si `age` es un campo del objeto u otra cosa, a costa de más verbosidad. El método `__init__` construye el objeto al crearse; suele llamarse "constructor", aunque técnicamente no lo es, porque en Python el objeto existe antes de que `__init__` se invoque (solo le faltan los campos).

Donde las clases se vuelven interesantes es con la "herencia" (inheritance): una clase `Parrot(Animal)` hereda la lógica y métodos de `Animal` y añade los suyos. Si `Parrot` define su propio `__init__`, este anula por completo al de `Animal`, y es responsabilidad del programador llamar explícitamente a `Animal.__init__(self, name)` para rescatar lo que necesite. Cady casi no usa herencia, salvo para extender clases de librerías como `HTMLParser`. Otros conceptos a conocer: los datos miembro "estáticos" pertenecen a la clase y no a instancias individuales (p. ej. un contador de instancias), y una clase puede heredar de varias (herencia múltiple), posible pero poco frecuente.

## Compilación e interpretación

Las etiquetas "lenguaje compilado" e "interpretado" tenían significados nítidos, pero los avances recientes las han convertido en un continuo. Tradicionalmente, un compilador traduce código legible a "machine code", que opera sobre bytes y ejecuta directamente el microprocesador; debe conocer el detalle del procesador y toma decisiones de traducción (los compiladores "optimizadores" reorganizan el programa para que corra más eficiente). C es compilado: produce un "executable" que no conserva vestigio del lenguaje original.

Un concepto importante es la diferencia entre "compile time" y "run time": un error de sintaxis aparece al compilar, pero otros problemas solo se descubren al ejecutar el machine code (quizá tras horas de ejecución o tras publicar el producto); por eso mucho del diseño de compiladores busca detectar fallos en compile time.

Un intérprete, en cambio (como el de Python), lee y ejecuta el código línea a línea; es un blob de machine code escrito en algo como C, y el código Python nunca se traduce a machine code. Los lenguajes compilados suelen ser mucho más rápidos (sin el coste de parsear cada línea en run time y con margen para optimizar), pero los interpretados permiten probar y depurar línea a línea sin preocuparse por lo que ocurre bajo el capó.

La zona gris: Python no es puramente interpretado, pues puede traducirse a una representación intermedia llamada "bytecode" (al correr un script entero o importar una librería), aunque ese bytecode está al mismo nivel de abstracción que Python y aporta poca optimización. Java es más gris aún: compila a un bytecode de bajo nivel que ejecuta la "Java virtual machine" (JVM), con muchas optimizaciones que dan casi el rendimiento de un lenguaje compilado; la JVM aporta gestión de memoria y acceso a recursos. El framework .NET de Microsoft es similar, y C# equivale esencialmente a Java. En ambos entornos el bytecode es la lingua franca y el machine code queda en manos de la máquina virtual. Incluso el hardware difumina la frontera: Intel pasó del modelo CISC (x86) a RISC y codificó en el silicio una traducción en tiempo real de x86 a RISC. Así, "compilar" es traducir código de un lenguaje a otro de más bajo nivel, e "interpretar" es enchufar el código en una "máquina" (virtual o física) que lo ejecuta. Finalmente, la compilación "just-in-time" (JIT) recompila partes de un lenguaje interpretado en pleno run time cuando aparecen garantías nuevas (p. ej. que una lista solo contiene enteros), con mucha sobrecarga pero a veces enormes ganancias.

## Sistemas de tipos

Además del paradigma, un lenguaje se caracteriza por su "type system". Toda variable tiene un tipo (entero, diccionario, string, clase propia) y operar sobre un objeto exige saber su tipo. Hay dos ejes principales.

Estático frente a dinámico: un lenguaje es "statically typed" si la computadora determina los tipos en compile time (permite almacenar y procesar de la forma más eficiente); es "dynamically typed" si los tipos no se conocen hasta run time, con boilerplate para rastrearlos. Python es dinámico: cada variable es una estructura C llamada `PyObject` que guarda el tipo, lo que cuesta RAM y obliga a comprobar el tipo antes de cada operación; gran flexibilidad a cambio de rendimiento. En C, estático, el compilador traduce cada operación a manipulaciones de bytes sin referencias explícitas al tipo. Muchos lenguajes interpretados usan "duck typing": una variable es del tipo "correcto" si toda operación llamada sobre ella está definida (si tiene `quack()` y `walk()`, es un pato).

Fuerte frente a débil: noción más difusa sobre cuánto obliga el lenguaje a usar los tipos de forma consistente. Python es fuerte al rechazar `"hello" + 5` (otros lenguajes adivinarían "hello5"), pero débil al aceptar tanto `3/2` como `3.0/2` con resultados distintos; OCaml daría error de compilación. C es fuerte (hay que declarar tipos y no compila si no cuadran), pero permite forzar que un trozo de bytes se trate como un tipo dado; los bytes de memoria no tienen tipo, y los lenguajes de alto nivel ponen capas de seguridad sobre esa flexibilidad.

## Ideas clave

- Los lenguajes modernos soportan varios paradigmas; todos son equivalentes en poder de cómputo pero distintos para pensar y aplicar.
- Imperativo = secuencias de instrucciones y side effects; funcional = funciones puras sin efectos, con funciones tratadas como variables; orientado a objetos = clases que encapsulan datos y métodos.
- Lo funcional encaja con la ciencia de datos y el batch processing (Spark es funcional); lo orientado a objetos brilla al interactuar con recursos externos y usuarios.
- En Python todo es objeto; `self` es el objeto pasado implícitamente, `__init__` inicializa y la herencia (que anula `__init__` por completo) permite reutilizar clases.
- Compilación e interpretación son hoy un continuo: bytecode (Python, JVM, .NET), traducción x86→RISC en silicio y compilación JIT difuminan la frontera.
- Diferenciar compile time de run time es clave: detectar errores pronto es mejor que descubrirlos al ejecutar.
- Tipado estático (eficiente, tipos en compile time) frente a dinámico (flexible pero con sobrecarga, como Python y el duck typing).
- Tipado fuerte frente a débil mide cuán estrictamente se respetan los tipos; los bytes de memoria no están tipados y los lenguajes de alto nivel protegen ese acceso.
