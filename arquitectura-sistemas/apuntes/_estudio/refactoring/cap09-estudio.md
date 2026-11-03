# Simplifying Conditional Expressions (Simplificación de expresiones condicionales) — Estudio

## Tarjetas de repaso

- P: ¿Qué hace Decompose Conditional? / R: Extrae a métodos propios la condición, la rama *then* y la rama *else*, separando la lógica de conmutación de los detalles y revelando el *por qué* detrás del *qué*.
- P: ¿Por qué merece la pena extraer condiciones cortas a un método? / R: Porque hay una brecha grande entre la intención del código y su cuerpo; un nombre como `notSummer(date)` se lee casi como un comentario y comunica mejor que la expresión original.
- P: ¿Qué hace Consolidate Conditional Expression? / R: Combina una secuencia de comprobaciones distintas que producen el mismo resultado en una sola expresión con `and`/`or` y la extrae, aclarando que en realidad se hace una única comprobación.
- P: ¿Qué requisito imprescindible tiene Consolidate Conditional Expression? / R: Que ningún condicional de la cadena tenga efectos secundarios; si los tiene, no se puede refactorizar.
- P: ¿Cuándo NO se deben consolidar las comprobaciones? / R: Cuando son realmente independientes y no deben pensarse como una sola; el código ya comunica su intención.
- P: ¿Qué hace Consolidate Duplicate Conditional Fragments? / R: Mueve fuera del condicional el fragmento que aparece en todas sus ramas, dejando claro qué varía y qué permanece igual; en excepciones, al bloque `finally`.
- P: ¿Qué reemplaza Remove Control Flag y por qué? / R: Reemplaza una variable que actúa como bandera de control por `break`, `continue` o `return`; estas banderas vienen de la regla de un único punto de salida, que produce condicionales retorcidos.
- P: ¿Qué opción prefiere Fowler al eliminar una bandera de control? / R: Extraer la lógica a un método y reemplazar por `return`, porque señala claramente que no se ejecuta más código.
- P: ¿Qué son las guard clauses y qué comunican? / R: Comprobaciones para casos especiales que devuelven o lanzan excepción; dicen "esto es raro; si pasa, haz algo y sal", destacando el camino normal de ejecución.
- P: ¿En qué dos formas vienen los condicionales según Replace Nested Conditional with Guard Clauses? / R: Una en la que ambos caminos son comportamiento normal (usa `if`/`else`) y otra en la que una respuesta es normal y la otra es una condición inusual (usa guard clause).
- P: ¿Qué hace Replace Conditional with Polymorphism? / R: Mueve cada rama de un condicional que elige según el tipo de un objeto a un método sobrescrito en una subclase, y hace abstracto el método original.
- P: ¿Qué estructura de herencia se necesita antes de Replace Conditional with Polymorphism? / R: La creada con Replace Type Code with Subclasses (la más simple) o con Replace Type Code with State/Strategy (obligatoria si el código de tipo cambia tras crear el objeto o si ya se subclasifica por otro motivo).
- P: ¿Qué resuelve Introduce Null Object? / R: Comprobaciones repetidas de `null`, reemplazando el valor nulo por un objeto nulo que responde con el comportamiento por defecto; al ser constantes e inmutables se implementan con Singleton.
- P: ¿Qué es una aserción (Introduce Assertion)? / R: Una sentencia condicional que se asume siempre verdadera; su fallo indica error del programador, debe producir excepciones no comprobadas y suele eliminarse en producción.
- P: ¿Qué efecto tiene añadir una aserción sobre el comportamiento del programa? / R: Lo preserva; la aserción actúa como ayuda de comunicación y de depuración, pero no debe usarse para comprobar todo lo que crees cierto, solo lo que necesita serlo.

## Preguntas de autoevaluación

- P: ¿Por qué el código condicional suele dificultar la lectura y cómo lo aborda este capítulo? / R: Porque dice *qué* pasa pero oscurece *por qué*; extraer condiciones y ramas a métodos con nombres intencionales hace explícito el motivo de la bifurcación. (Lo que necesitas saber)
- P: ¿Cómo puede simplificarse una rutina que solo prueba una condición consolidada y devuelve un valor? / R: Convirtiéndola en un único `return` con operador ternario, p. ej. `return (onVacation() && lengthOfService() > 10) ? 1 : 0.5;`. (Consolidate Conditional Expression)
- P: Si un fragmento común está en medio de las ramas del condicional, ¿qué se hace? / R: Se comprueba si el código anterior o posterior cambia algo y se desplaza el fragmento hacia un extremo (antes o después del condicional); con más de una sentencia, se extrae a un método. (Consolidate Duplicate Conditional Fragments)
- P: ¿Por qué Fowler rechaza la regla de un único punto de salida pero acepta la de un único punto de entrada? / R: Porque el único punto de entrada lo imponen los lenguajes modernos, pero la regla del único punto de salida produce condicionales retorcidos; a veces salir temprano comunica mejor. (Remove Control Flag / Lo que necesitas saber)
- P: ¿Cuál es la mayor ganancia de Replace Conditional with Polymorphism? / R: Que cuando el mismo conjunto de condiciones se repite en muchos sitios, añadir un tipo solo requiere crear una subclase sin localizar y actualizar todos los condicionales, y los clientes no necesitan conocer las subclases, reduciendo dependencias. (Replace Conditional with Polymorphism)
- P: ¿Cuándo tiene sentido Introduce Null Object y qué opción queda para los clientes que quieren otra respuesta? / R: Solo cuando la mayoría —no todos— de los clientes quieren la misma respuesta; quien quiera otra sigue pudiendo usar `isNull`. (Introduce Null Object)
- P: ¿Qué alternativa existe cuando no se puede modificar la clase fuente para introducir un objeto nulo? / R: La *testing interface*, una interfaz `Null {}` vacía implementada por los objetos nulos y probada con `instanceof`. (Introduce Null Object)
- P: En Java, ¿cómo se consigue que las aserciones sean fácilmente removibles para no afectar al rendimiento? / R: Usando una constante `Assert.ON` para que el compilador elimine el código muerto, o filtrando las líneas de aserción en producción; conviene señalarlas con una clase `Assert`. (Introduce Assertion)

## Checklist

- Ante un `if-then-else` complejo, extrae por separado la condición, el *then* y el *else*, compilando y probando tras cada extracción (Decompose Conditional).
- Antes de descomponer condicionales anidados, valora aplicar Replace Nested Conditional with Guard Clauses.
- Antes de consolidar comprobaciones, verifica que ninguna tenga efectos secundarios; luego sustituye la cadena por un único condicional con operadores lógicos y considera Extract Method.
- Al tener fragmentos duplicados en las ramas, muévelos al inicio o al final del condicional; para excepciones, lleva el código repetido de `try`/`catch` al `finally`.
- Al eliminar una bandera de control, reemplaza por `break`/`continue`/`return`, compilando y probando tras cada reemplazo, y vigila si la bandera transporta información de resultado.
- Introduce una guard clause por cada caso especial (con `return` o excepción), compilando y probando tras cada una; si todas dan el mismo resultado, usa Consolidate Conditional Expressions.
- Antes de Replace Conditional with Polymorphism, asegura la estructura de herencia; luego sube el método a la jerarquía, sobrescribe rama por rama compilando y probando, elimina cada rama del original y finalmente declara abstracto el método de la superclase.
- Para Introduce Null Object, crea la subclase nula y la operación `isNull`, haz que los sitios devuelvan el objeto nulo, reemplaza `== null` por `isNull()` y mueve el comportamiento por defecto caso por caso eliminando el condicional.
- Al añadir aserciones, asegúrate de que el código no funcione correctamente sin ellas; si funciona, quítalas, y evita duplicación con Extract Method.
