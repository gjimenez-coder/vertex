# Error Handling (Manejo de errores) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre el manejo de errores? / R: El manejo de errores es necesario e importante, pero si oscurece la lógica del código, está mal; debe tratarse como una preocupación separada.

P: ¿Por qué conviene lanzar excepciones en lugar de usar códigos de retorno o flags? / R: Porque los códigos de retorno saturan al llamador, que debe comprobar el error justo después de la llamada y es fácil olvidarlo; la excepción deja el código del llamador más limpio y no oscurece su lógica.

P: ¿Qué dos preocupaciones separa el ejemplo de `DeviceController.sendShutDown()` al usar try-catch? / R: El algoritmo de apagado del dispositivo y el manejo de errores, que antes estaban entrelazados en condicionales anidados.

P: ¿Por qué conviene escribir primero el bloque try-catch-finally? / R: Porque las excepciones definen un ámbito tipo transacción; empezar por el try-catch define qué debe esperar el usuario del código y en qué estado consistente debe quedar pase lo que pase.

P: ¿Cómo se construye el ejemplo de `retrieveSection`? / R: Con TDD: primero un test que espera `StorageException` al abrir un archivo inexistente, luego el stub, luego la implementación que lanza la excepción, y finalmente se refina el `catch` para capturar `FileNotFoundException`.

P: ¿Qué postura adopta el capítulo sobre las excepciones comprobadas (checked)? / R: «El debate ha terminado»: no son necesarias para producir software robusto, como demuestran C#, C++, Python y Ruby, que no las tienen.

P: ¿Qué principio violan las checked exceptions y por qué? / R: El Open/Closed Principle: una excepción lanzada niveles por debajo del catch debe declararse en la firma de cada método intermedio, provocando una cascada de cambios de abajo arriba y rompiendo la encapsulación.

P: ¿Qué contexto debe aportar cada excepción? / R: Suficiente para determinar el origen y la ubicación del error: mencionar la operación fallida y el tipo de fallo, y pasar la información necesaria para registrarlo en el catch, ya que el stack trace no revela la intención.

P: ¿Según qué criterio deben definirse las clases de excepción en una aplicación? / R: Según cómo se capturan (las necesidades del llamador), más que por su origen o tipo.

P: ¿Qué hace la clase `LocalPort` en el ejemplo del `ACMEPort`? / R: Envuelve (wrap) `ACMEPort` y traduce sus distintas excepciones a un único `PortDeviceFailure`, eliminando la duplicación de múltiples catch en el cliente.

P: ¿Qué ventajas tiene envolver APIs de terceros? / R: Minimiza dependencias (permite cambiar de librería con poco coste), facilita el mock en pruebas y libera de las decisiones de diseño del proveedor.

P: ¿En qué consiste el Special Case Pattern? / R: En encapsular el comportamiento excepcional en un objeto; por ejemplo, que `ExpenseReportDAO` devuelva siempre un `MealExpenses`, retornando un `PerDiemMealExpenses` cuando no hay gastos, para que el cliente no trate el caso excepcional.

P: ¿Por qué no se debe devolver `null`? / R: Porque invita a errores: genera chequeos de null por todas partes y basta un chequeo olvidado para descontrolar la aplicación; en su lugar se lanza una excepción, se devuelve un objeto special case o una colección vacía.

P: ¿Qué hacer en lugar de devolver `null` en colecciones? / R: Devolver una lista vacía (`Collections.emptyList()`), lo que limpia el código y reduce los NullPointerException.

P: ¿Por qué pasar `null` es peor que devolverlo? / R: Porque en la mayoría de lenguajes no hay buena forma de tratar un null pasado accidentalmente; lo racional es prohibir pasarlo por defecto, de modo que un null en los argumentos indique un problema.

## Preguntas de autoevaluación

P: ¿Cómo mejora la legibilidad separar el manejo de errores de la lógica principal? / R: Permite razonar sobre ambas preocupaciones por separado y mejora la mantenibilidad; la lógica de negocio parece un algoritmo limpio y el manejo de errores queda empujado a los bordes del programa. (Sección: Lo que necesitas saber / Definir el flujo normal)

P: ¿Por qué se comparan los bloques try con transacciones? / R: Porque el catch debe dejar el programa en un estado consistente pase lo que pase, igual que una transacción garantiza consistencia. (Sección: Escribir primero el try-catch-finally)

P: ¿Qué problema concreto provoca lanzar una checked exception tres niveles por debajo del catch? / R: Obliga a declararla en la firma de cada método intermedio, forzando una cascada de modificaciones y haciendo que todas las funciones del camino conozcan la excepción de bajo nivel. (Sección: Usar excepciones no comprobadas)

P: ¿Cuándo pueden ser aceptables las excepciones comprobadas? / R: En una librería crítica, pero en el desarrollo de aplicaciones general el coste de dependencias supera los beneficios. (Sección: Usar excepciones no comprobadas)

P: ¿Por qué el problema del ejemplo `registerItem` no es que falte un chequeo de null? / R: Porque el problema real es que hay demasiados chequeos de null; la solución es no devolver null, no añadir otro chequeo. (Sección: No devolver null)

P: ¿Qué limitaciones tienen las alternativas a prohibir pasar null (InvalidArgumentException y aserciones)? / R: Lanzar `InvalidArgumentException` exige definir un handler sin buen curso de acción, y las aserciones (`assert p1 != null`) documentan pero no resuelven el error en tiempo de ejecución. (Sección: No pasar null)

P: ¿Cuándo conviene usar clases de excepción distintas en vez de una sola por área de código? / R: Solo cuando quieras capturar una excepción y dejar pasar otra. (Sección: Definir clases de excepción según las necesidades del llamador)

P: ¿Están en conflicto la legibilidad y la robustez según el mensaje de cierre? / R: No; el código limpio debe ser legible y robusto, y esas metas no están en conflicto. (Sección: Lo que necesitas saber)

## Checklist

- Lanza una excepción en lugar de devolver flags o códigos de retorno.
- Escribe primero el bloque try-catch-finally y construye el resto de la lógica después, apoyándote en TDD.
- Usa excepciones no comprobadas (unchecked) por defecto en el desarrollo de aplicaciones.
- Incluye en cada excepción la operación fallida, el tipo de fallo y la información necesaria para el log.
- Define las clases de excepción según cómo se capturan; envuelve las APIs de terceros para devolver un tipo de excepción común.
- Aplica el Special Case Pattern para encapsular casos excepcionales y evitar tratarlos en el cliente.
- No devuelvas `null`: usa una excepción, un objeto special case o una colección vacía (`Collections.emptyList()`).
- No pases `null` como argumento; prohíbelo por defecto.
