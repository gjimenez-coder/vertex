# Organizing Data (Organización de datos) — Estudio

## Tarjetas de repaso

P: Según el capítulo, ¿cuál es el primer paso al convertir un dato en objeto y dónde está el valor real? / R: Crear el objeto es solo el primer paso; la verdadera ventaja llega al usar Move Method para trasladar comportamiento al nuevo objeto.

P: ¿Qué son las dos escuelas de acceso a campos en Self Encapsulate Field? / R: Acceso directo (más fácil de leer) y acceso indirecto (permite que una subclase sobrescriba la obtención del dato y habilita la inicialización perezosa).

P: ¿Cuándo es más importante aplicar Self Encapsulate Field? / R: Cuando accedes a un campo de una superclase pero quieres sobrescribir ese acceso con un valor calculado en la subclase (ejemplo IntRange/CappedRange).

P: ¿Cuál es la diferencia entre reference objects y value objects? / R: Los reference objects representan un objeto del mundo real y se comparan por identidad; los value objects se definen por sus datos, no importa que haya copias y deben ser inmutables.

P: ¿Qué métodos hay que crear al aplicar Change Reference to Value y cómo se construye uno de ellos? / R: Hay que crear equals y hashCode; el hashCode se construye con XOR bitwise de los campos.

P: ¿Para qué sirven los arrays según Replace Array with Object? / R: Los arrays deben contener solo colecciones de objetos similares en algún orden; convenciones como "el primer elemento es el nombre" son difíciles de recordar y conviene reemplazarlas por un objeto con un campo por elemento.

P: ¿Por qué Duplicate Observed Data es una excepción a la regla de no duplicar datos? / R: Separa interfaz de usuario y lógica de negocio; el comportamiento se mueve fácil pero los datos no, así que hay que duplicarlos y sincronizarlos con un observer, algo que suele ser imposible de evitar.

P: En Duplicate Observed Data, ¿por qué se usa acceso directo al campo en el event handler y en update? / R: Para evitar la recursión infinita que provocaría llamar al setter que notifica a los observers.

P: ¿Cuáles son las reglas para decidir qué clase controla una asociación bidireccional? / R: Si ambos son reference objects uno a muchos, controla el lado "uno"; si uno es componente del otro, controla el compuesto; si ambos son reference objects muchos a muchos, da igual.

P: ¿Qué costes tienen las asociaciones bidireccionales? / R: Complejidad de mantener los dos enlaces, riesgo de "zombies" (objetos que deberían estar muertos pero siguen referenciados) e interdependencia entre clases y paquetes.

P: ¿Qué alternativas conviene buscar antes de aplicar Replace Magic Number with Symbolic Constant? / R: Si el número es un type code, considerar Replace Type Code with Class; si es la longitud de un array, usar anArray.length.

P: ¿Cómo debe comportarse el getter de una colección en Encapsulate Collection? / R: No debe devolver la colección en sí; debe devolver una vista de solo lectura (Collections.unmodifiableSet en Java 2 o una copia con clone en Java 1.1) y no debe haber setter, sino métodos add/remove.

P: ¿Cuándo aplica Replace Type Code with Class y cuándo no? / R: Aplica solo si el type code es dato puro que no afecta al comportamiento; no aplica si provoca comportamiento distinto en un switch.

P: ¿Cuál es la diferencia entre Replace Type Code with Subclasses y with State/Strategy? / R: Subclasses se usa con type codes inmutables que afectan al comportamiento; State/Strategy se usa cuando el type code cambia durante la vida del objeto o la clase ya está subclaseada por otra razón.

P: ¿Cuándo una subclase no justifica su existencia según Replace Subclass with Fields? / R: Cuando varía solo en constant methods que devuelven datos hard-coded; se convierten en campos final de la superclase y se eliminan las subclases.

## Preguntas de autoevaluación

P: ¿Por qué Fowler prefiere el acceso directo a campos como primer recurso? / R: Porque hace el código más fácil de leer, "no necesitas detenerte a decir 'esto es solo un getter'", hasta que ese acceso directo estorba. (Self Encapsulate Field)

P: ¿Qué disparadores indican que conviene aplicar Replace Data Value with Object? / R: Cuando el dato simple empieza a necesitar comportamiento adicional y el código huele a duplicación y feature envy, como un teléfono que pasa de string a objeto con formateo y extracción de prefijo. (Replace Data Value with Object)

P: ¿En qué contextos resultan útiles los value objects al aplicar Change Reference to Value? / R: En sistemas distribuidos y concurrentes, cuando trabajar con el objeto de referencia se vuelve incómodo; el requisito clave es que el objeto sea inmutable. (Change Reference to Value)

P: ¿Cuál es el patrón del modificador al añadir una asociación bidireccional? / R: Primero decir al otro objeto que elimine su puntero, luego fijar tu propio puntero y, por último, decir al nuevo objeto que añada el puntero. (Change Unidirectional Association to Bidirectional)

P: Al eliminar una asociación bidireccional, ¿cuál es la parte difícil y en qué orden se procede? / R: Lo difícil es comprobar que la eliminación es factible (p. ej. pasando el objeto como argumento o con Substitute Algorithm en el getter); el orden es eliminar primero los lectores del campo, luego los escritores y finalmente el campo. (Change Bidirectional Association to Unidirectional)

P: ¿Por qué son problemáticos los type codes numéricos y qué aporta reemplazarlos por una clase? / R: El compilador solo ve el número subyacente, no el nombre simbólico, lo que reduce legibilidad y causa bugs; con una clase el compilador verifica tipos y las factory methods garantizan instancias válidas. (Replace Type Code with Class)

P: ¿Por qué Replace Type Code with Subclasses se describe como un movimiento de andamiaje? / R: Porque principalmente habilita Replace Conditional with Polymorphism, usando self-encapsulate del type code y una subclase por valor que sobrescribe el getter. (Replace Type Code with Subclasses)

P: ¿Cómo se elige entre el patrón state y el patrón strategy en Replace Type Code with State/Strategy? / R: Strategy si simplificas un único algoritmo; state si mueves datos específicos de estado y piensas en el objeto como cambiando de estado. (Replace Type Code with State/Strategy)

## Puntos a dominar

- Reconocer cuándo convertir datos simples en objetos y recordar que el valor llega al mover comportamiento con Move Method.
- Distinguir reference objects (identidad) de value objects (valor, inmutables, con equals y hashCode).
- Elegir entre acceso directo e indirecto a campos y justificar la decisión.
- Aplicar el protocolo de colecciones: vista de solo lectura en el getter y métodos add/remove, sin setter.
- Decidir qué clase controla una asociación y aplicar correctamente el patrón del modificador.
- Seleccionar el reemplazo de type code adecuado: Class (dato puro), Subclasses (afecta al comportamiento e inmutable) o State/Strategy (afecta al comportamiento y mutable o ya subclaseado).
- Identificar subclases que solo tienen constant methods para aplicar Replace Subclass with Fields.
