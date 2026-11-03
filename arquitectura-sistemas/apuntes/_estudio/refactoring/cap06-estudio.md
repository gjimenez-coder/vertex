# Composing Methods (Componer métodos) — Estudio

## Tarjetas de repaso

- P: ¿Cuál es la fuente habitual de problemas que resuelve este capítulo? / R: Los métodos demasiado largos, que acumulan información sepultada por lógica compleja; el remedio es componer métodos cortos y bien nombrados.
- P: ¿Qué hace Extract Method y cómo se nombra el método resultante? / R: Convierte un fragmento agrupable en un método propio, nombrándolo por lo que hace y no por cómo lo hace.
- P: ¿Cuál es el criterio de Fowler para decidir si extraer un método? / R: La distancia semántica entre el nombre y el cuerpo; si extraer mejora la claridad, se hace aunque el nombre sea más largo que el código extraído.
- P: ¿Cuál es el mayor obstáculo de Extract Method? / R: Las variables locales, y en especial los temporales (temps).
- P: ¿Qué se hace con un temp asignado que se usa después del código extraído? / R: El método extraído debe devolver el valor cambiado; Fowler prefiere métodos que devuelvan un único valor.
- P: ¿Qué es Inline Method y cuándo se aplica? / R: Meter el cuerpo de un método en sus llamadores y eliminarlo, cuando el cuerpo es tan claro como su nombre o para reagrupar métodos mal factorizados antes de re-extraer.
- P: ¿Qué relación tiene Replace Temp with Query con Extract Method? / R: Suele ser un paso previo imprescindible, porque las variables locales dificultan la extracción; sustituye el temp por una llamada a un método que calcula la expresión.
- P: ¿Qué condición debe cumplir el método extraído en Replace Temp with Query? / R: Debe estar libre de efectos secundarios; si no, se aplica antes Separate Query from Modifier.
- P: ¿Cuándo se usa Introduce Explaining Variable y por qué Fowler suele preferir otra opción? / R: Para explicar partes de una expresión complicada con temps bien nombrados; Fowler prefiere Extract Method porque un método es reutilizable por todo el objeto, salvo cuando extraer cuesta más (muchas variables locales).
- P: ¿Qué temporales NO se dividen en Split Temporary Variable? / R: Las variables de bucle (loop variables) y las de acumulación (collecting temporary variables), con forma `i = i + expresión`.
- P: ¿Qué significa exactamente "asignar a un parámetro" en Remove Assignments to Parameters? / R: Cambiar la referencia del parámetro (p. ej. `foo = anotherObject`), no modificar el objeto recibido (`foo.modifyInSomeWay()`), que es correcto.
- P: ¿Por qué el paso por valor de Java motiva Remove Assignments to Parameters? / R: Porque reasignar el parámetro no afecta al llamador, pero sí se puede modificar el objeto; eso confunde entre modificar el objeto y reasignar la referencia.
- P: ¿Qué resuelve Replace Method with Method Object y a qué costo? / R: Un método largo con variables locales que impiden Extract Method; convierte los locales en campos de una clase nueva para descomponerlo sin pasar parámetros, a costa de introducir esa clase.
- P: ¿Qué paso es imprescindible antes de aplicar Substitute Algorithm? / R: Descomponer el método tanto como sea posible, porque sustituir un algoritmo grande y complejo solo se vuelve tratable simplificándolo primero.

## Preguntas de autoevaluación

- P: ¿Cuáles son los cuatro casos de variables locales al aplicar Extract Method y cómo se tratan? / R: Variables solo leídas → se pasan como parámetros; objeto local al que se invoca un método modificador → también como parámetro (salvo reasignación); temp asignado usado solo dentro del código extraído → se mueve al método; temp asignado usado después → el método devuelve el valor cambiado. (Sección: Extract Method)
- P: ¿Por qué Inline Method ayuda a reagrupar métodos mal factorizados? / R: Porque se hace inline de todos en un método grande y luego se vuelve a extraer; Kent Beck suele hacerlo antes de Replace Method with Method Object. (Sección: Inline Method)
- P: Según el capítulo, ¿cómo debe tratarse la preocupación por el rendimiento al eliminar temps? / R: Dejarla pasar de momento: nueve de cada diez veces no importará, y el código mejor factorizado habilita optimizaciones más potentes. (Sección: Replace Temp with Query)
- P: ¿Qué pasos sigue la mecánica de Split Temporary Variable? / R: Renombrar el temp en su declaración y primera asignación, declararlo `final`, cambiar las referencias hasta la segunda asignación, y repetir por etapas. (Sección: Split Temporary Variable)
- P: En el ejemplo del "haggis", ¿en qué se divide la variable `acc` y por qué? / R: En `primaryAcc` y `secondaryAcc`, porque `acc` tenía más de una responsabilidad: primero la aceleración inicial y luego la aceleración con ambas fuerzas. (Sección: Split Temporary Variable)
- P: ¿Qué elementos componen la clase creada en Replace Method with Method Object? / R: Un campo `final` para el source object, un campo por cada temporal y parámetro, un constructor que recibe el source object y los parámetros, y un método `compute` con el cuerpo original. (Sección: Replace Method with Method Object)
- P: ¿Cómo valida Substitute Algorithm que el nuevo algoritmo es correcto? / R: Preparándolo hasta que compile, ejecutándolo contra los tests, y si los resultados difieren, usando el algoritmo antiguo como comparación en las pruebas, ejecutando cada caso con ambos. (Sección: Substitute Algorithm)

## Puntos a dominar

- Reconocer que los métodos largos son el problema central y que componer métodos cortos y bien nombrados es el remedio.
- Distinguir Extract Method e Inline Method como refactorizaciones opuestas y saber cuándo aplicar cada una.
- Identificar cómo las variables locales (sobre todo los temps) obstaculizan la extracción y resolverlas con Replace Temp with Query, Split Temporary Variable o Inline Temp.
- Diferenciar Introduce Explaining Variable de Extract Method y saber cuándo prefiere Fowler cada una.
- No dividir variables de bucle ni de acumulación al aplicar Split Temporary Variable.
- Entender por qué no se asigna a parámetros en Java y cómo el paso por valor influye en esa regla.
- Saber cuándo recurrir a Replace Method with Method Object y qué estructura tiene la clase resultante.
- Recordar que Substitute Algorithm exige descomponer primero el método y validar el nuevo algoritmo contra el antiguo.
