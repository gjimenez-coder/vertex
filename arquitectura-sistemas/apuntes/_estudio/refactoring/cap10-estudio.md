# Making Method Calls Simpler (Simplificar las llamadas a métodos) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre las interfaces de los objetos? / R: Mejorar las interfaces para que sean fáciles de entender y usar; la claridad vive en los nombres de los métodos, el diseño de las listas de parámetros y la separación entre consultas y modificadores.

P: ¿Qué truco propone Fowler para encontrar un buen nombre al aplicar Rename Method? / R: Pensar qué comentario llevaría el método y convertir ese comentario en su nombre.

P: En Rename Method, ¿cómo se hace la migración de forma segura? / R: Se declara el método nuevo copiando el cuerpo, el viejo delega en él, se compila y testea, se migran los llamadores uno a uno y se elimina el viejo (o se marca como `deprecated` si es parte de una interfaz que no puedes quitar).

P: ¿Por qué Fowler desaconseja Add Parameter y qué considerar antes? / R: Las listas largas huelen mal (data clumps, difíciles de recordar); antes de añadir, pregunta si puedes obtener el dato de un parámetro existente o considera Introduce Parameter Object.

P: Al quitar un parámetro en un método polimórfico, ¿qué precaución hay? / R: Si otra implementación sí usa el parámetro, no lo quites.

P: ¿Qué significa que una consulta no tenga efectos secundarios "observables"? / R: Puede llamarse tantas veces y donde se quiera; cachear el resultado en un campo cambia el estado pero no es un efecto observable.

P: ¿En qué consiste Parameterize Method? / R: Varios métodos que hacen lo mismo variando solo unos valores se unifican en un único método con un parámetro, eliminando duplicación y ganando flexibilidad.

P: ¿Cuándo usar Replace Parameter with Explicit Methods y qué ventajas aporta? / R: Cuando un método ejecuta código distinto según los valores de un parámetro enumerado; evita el condicional, gana comprobación en tiempo de compilación e interfaz más clara (p. ej. `Switch.beOn()`).

P: ¿Cuál es la fuerza motriz de Preserve Whole Object y su contrapartida? / R: Pasar el objeto entero hace la lista más robusta y legible y revela comportamiento que mover al objeto; la contrapartida es introducir una dependencia entre el objeto requerido y el llamado.

P: ¿Qué es un data clump y qué refactorización lo resuelve? / R: Un grupo de parámetros que viajan juntos; se resuelve con Introduce Parameter Object, reuniéndolos en un objeto (en el ejemplo, una clase `DateRange` inmutable).

P: ¿Por qué el objeto parámetro del ejemplo (DateRange) se hace inmutable? / R: Campos `final` fijados en el constructor y sin setters, para imitar el paso por valor de Java y evitar bugs de aliasing.

P: ¿Cuándo se aplica Remove Setting Method? / R: Cuando un campo debe fijarse en la creación y no cambiar nunca: no se da setter y el campo se hace `final`, dejando clara la intención.

P: ¿Cuál es la motivación principal de Replace Constructor with Factory Method? / R: Reemplazar un type code por subclases, ya que un constructor solo devuelve instancias de su propia clase; el factory se hace `private`.

P: ¿Qué criterio decide entre excepción checked y unchecked en Replace Error Code with Exception? / R: Si es responsabilidad del llamador comprobar la condición antes de llamar, es un error de programación y se usa unchecked (incluso una aserción); si es responsabilidad del método, se declara checked.

P: ¿Para qué deben usarse las excepciones según Replace Exception with Test? / R: Para comportamiento excepcional, no como sustituto de un test condicional que el llamador podría hacer razonablemente antes de llamar.

## Preguntas de autoevaluación

P: ¿Por qué Fowler afirma que un buen nombre vale el esfuerzo de renombrar? / R: Porque el código se escribe primero para un humano y después para la máquina. (Ideas clave / Rename Method)

P: En el ejemplo de Separate Query from Modifier, ¿qué se extrae de `foundMiscreant` y qué queda? / R: Se extrae `foundPerson` como consulta pura que devuelve el nombre, y se deja el modificador con el efecto de enviar la alerta. (Separate Query from Modifier)

P: ¿Cómo se reconcilia Separate Query from Modifier con la programación concurrente? / R: Las operaciones test-and-set deben ser atómicas, así que se conserva un tercer método sincronizado que llama a la consulta y al modificador (que pueden ser package/private). (Separate Query from Modifier / advertencias de Doug Lea)

P: Si no puedes parametrizar el método completo, ¿qué haces? / R: Extraes primero el fragmento repetitivo y lo parametrizas (ejemplo `usageInRange(start, end)`). (Parameterize Method)

P: ¿Cuándo aplica Replace Parameter with Method? / R: Cuando el receptor puede calcular por sí mismo el valor que recibe como parámetro, el objeto se llama a sí mismo (o tiene referencia al emisor) y el cálculo no depende de los parámetros del método llamante. (Replace Parameter with Method)

P: ¿Qué tres variantes de creación de subclases muestra Replace Constructor with Factory Method? / R: Con `switch` sobre el type code, con `Class.forName` (flexible pero sin comprobación en tiempo de compilación y expone nombres de subclase), y con métodos explícitos por subclase como `createMale`/`createFemale`. (Replace Constructor with Factory Method)

P: ¿Por qué devolver una subclase al encapsular un downcast no rompe el código existente? / R: Porque cambia la firma pero la subclase no viola el contrato del padre, de modo que los llamadores siguen funcionando. (Encapsulate Downcast)

P: En el ejemplo del `ResourcePool`, ¿qué pasos convierten una excepción en un test? / R: Se antepone `if (_available.isEmpty())`, se añade una aserción temporal en el `catch`, y al confirmar que nunca se alcanza se elimina el bloque `try` y se limpia con Consolidate Duplicate Conditional Fragments. (Replace Exception with Test)

## Puntos a dominar

- Reconocer cuándo un nombre no revela el propósito y aplicar Rename Method con delegación segura (o directo si hay pocos llamadores).
- Preferir acortar listas de parámetros: Preserve Whole Object, Introduce Parameter Object o Replace Parameter with Method frente a Add Parameter.
- Mantener las consultas libres de efectos observables y separadas de los modificadores.
- Ocultar lo que se pueda: datos, setters innecesarios y métodos no usados por otras clases (Hide Method).
- Usar factory methods cuando la creación necesita más que un constructor, sobre todo para devolver subclases según un type code.
- Encapsular el downcast dentro del método y devolver el tipo más específico posible.
- Usar excepciones solo para lo excepcional; distinguir checked vs. unchecked y volver a un test cuando el llamador puede comprobar la condición.
- Tener presentes las advertencias de Doug Lea sobre listas de parámetros en código concurrente.
