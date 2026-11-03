# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 7 — Error Handling (Manejo de errores)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo, escrito por Michael Feathers, defiende que el manejo de errores es necesario pero no debe dominar el código. Muchas bases de código resultan ilegibles porque el manejo de errores disperso oscurece lo que el código realmente hace. La tesis es clara: el manejo de errores es importante, pero si oscurece la lógica, está mal (PDF p. 134).

La propuesta es tratar el manejo de errores como una preocupación separada, viewable e independiente de la lógica principal. Si se consigue esa separación, se puede razonar sobre ambas por separado y mejorar enormemente la mantenibilidad. Sales sabiendo cuándo usar excepciones en lugar de códigos de retorno, cómo estructurar bloques try-catch-finally, por qué evitar las excepciones comprobadas (checked), cómo diseñar clases de excepción según las necesidades de quien las captura, y por qué no se debe devolver ni pasar `null`.

El mensaje de cierre: código limpio es legible, pero también debe ser robusto, y esas metas no están en conflicto (PDF p. 143).

## Usar excepciones en lugar de códigos de retorno

Antiguamente, sin excepciones, se señalaba un error con un flag o un código de retorno que quien llamaba debía comprobar. El problema es que esto satura al llamador: hay que comprobar el error justo después de la llamada y es fácil olvidarlo. Lanzar una excepción deja el código del llamador más limpio y su lógica no queda oscurecida por el manejo de errores (PDF p. 135).

En el ejemplo de `DeviceController.sendShutDown()`, al pasar de condicionales anidados a un `try { tryToShutDown(); } catch (DeviceShutDownError e) { ... }`, se separan dos preocupaciones que estaban entrelazadas: el algoritmo de apagado del dispositivo y el manejo de errores. Cada una se entiende de forma independiente (PDF p. 136).

## Escribir primero el try-catch-finally

Las excepciones definen un ámbito (scope) dentro del programa: en el bloque `try` declaras que la ejecución puede abortar en cualquier punto y reanudarse en el `catch`. Los bloques `try` son como transacciones; el `catch` debe dejar el programa en un estado consistente pase lo que pase. Por eso conviene empezar por el try-catch-finally al escribir código que pueda lanzar excepciones: así defines qué debe esperar el usuario de ese código (PDF p. 136).

El ejemplo de `retrieveSection` lo construye con TDD: primero un test que espera `StorageException` al abrir un archivo inexistente, luego el stub, luego una implementación que lanza la excepción, y finalmente se refina el `catch` para capturar `FileNotFoundException`. Una vez definido el ámbito con la estructura try-catch, se añade el resto de la lógica entre la creación del `FileInputStream` y el `close` (PDF p. 137).

## Usar excepciones no comprobadas (unchecked)

«El debate ha terminado» (PDF p. 137). Las excepciones comprobadas parecían buena idea al introducirse en Java, pero no son necesarias para producir software robusto: C#, C++, Python y Ruby no las tienen y en todos ellos se escribe software robusto.

El precio de las checked exceptions es una violación del Open/Closed Principle: si lanzas una excepción comprobada tres niveles por debajo del `catch`, debes declararla en la firma de cada método intermedio. Un cambio en un nivel bajo fuerza cambios de firma en muchos niveles superiores, provocando una cascada de modificaciones de abajo arriba y rompiendo la encapsulación, pues todas las funciones del camino deben conocer la excepción de bajo nivel. Pueden ser útiles en una librería crítica, pero en desarrollo de aplicaciones general el coste de dependencias supera los beneficios (PDF p. 138).

## Dar contexto con las excepciones

Cada excepción debe aportar suficiente contexto para determinar el origen y la ubicación del error. En Java se obtiene un stack trace, pero este no revela la intención de la operación que falló. Hay que crear mensajes de error informativos: mencionar la operación fallida y el tipo de fallo, y pasar la información necesaria para registrarlo en el `catch` (PDF p. 138).

## Definir clases de excepción según las necesidades del llamador

Los errores pueden clasificarse por origen o por tipo, pero al definir clases de excepción en una aplicación lo más importante es cómo se capturan. El ejemplo del `ACMEPort` muestra un try-catch con mucha duplicación: tres `catch` (`DeviceResponseException`, `ATM1212UnlockedException`, `GMXError`) que hacen prácticamente lo mismo (PDF p. 139).

La solución es envolver (wrap) la API llamada para que devuelva un tipo de excepción común. La clase `LocalPort` envuelve `ACMEPort` y traduce sus excepciones a un único `PortDeviceFailure`, dejando el try-catch del cliente mucho más limpio. Envolver APIs de terceros es una buena práctica: minimiza dependencias (puedes cambiar de librería con poco coste), facilita el mock en pruebas y te libera de las decisiones de diseño del proveedor. A menudo basta una sola clase de excepción por área de código; usa clases distintas solo cuando quieras capturar una y dejar pasar otra (PDF p. 139-140).

## Definir el flujo normal

Siguiendo los consejos anteriores, el manejo de errores queda empujado a los bordes del programa y la lógica de negocio parece un algoritmo limpio. Pero a veces no quieres abortar. El ejemplo del cálculo de gastos usa un `catch(MealExpensesNotFound e)` para aplicar el per diem, lo que satura la lógica. La solución es el **SPECIAL CASE PATTERN** [Fowler]: cambiar el `ExpenseReportDAO` para que siempre devuelva un `MealExpenses`; cuando no hay gastos, devuelve un objeto `PerDiemMealExpenses` cuyo `getTotal()` retorna el per diem. El cliente deja de tratar el caso excepcional porque ese comportamiento queda encapsulado (PDF p. 140-141).

## No devolver null

Devolver `null` es lo primero que invita a errores: bases de código con un chequeo de `null` cada pocas líneas. Al devolver `null` creamos trabajo para nosotros y trasladamos problemas al llamador; basta un chequeo olvidado para descontrolar la aplicación. El ejemplo de `registerItem` esconde que `persistentStore` podría ser `null` y lanzar un `NullPointerException`. El problema no es que falte un chequeo, sino que hay demasiados. En lugar de devolver `null`, lanza una excepción o devuelve un objeto SPECIAL CASE; si una API de terceros devuelve `null`, envuélvela. Para colecciones, devolver una lista vacía (`Collections.emptyList()`) en vez de `null` limpia el código y reduce los `NullPointerException` (PDF p. 141-142).

## No pasar null

Pasar `null` a un método es peor que devolverlo. En `MetricsCalculator.xProjection`, pasar `null` produce un `NullPointerException`. Lanzar un `InvalidArgumentException` es algo mejor, pero exige definir un handler sin buen curso de acción; las aserciones (`assert p1 != null`) documentan pero no resuelven el error en tiempo de ejecución. En la mayoría de lenguajes no hay buena forma de tratar un `null` pasado accidentalmente, así que el enfoque racional es prohibir pasar `null` por defecto; entonces un `null` en la lista de argumentos indica un problema y hay menos errores por descuido (PDF p. 142-143).

## Ideas clave

- El manejo de errores es necesario, pero si oscurece la lógica, está mal; trátalo como preocupación separada.
- Lanza excepciones en lugar de usar flags o códigos de retorno: deja al llamador más limpio.
- Las excepciones definen un ámbito tipo transacción; escribe primero el try-catch-finally y construye la lógica con TDD.
- Evita las checked exceptions: violan el Open/Closed Principle y rompen la encapsulación con cascadas de cambios.
- Aporta contexto en cada excepción: operación fallida y tipo de fallo, más información para el log.
- Define las clases de excepción según cómo se capturan; envolver APIs de terceros para devolver un tipo común reduce la duplicación y las dependencias.
- Usa el Special Case Pattern para evitar tratar casos excepcionales en el cliente.
- No devuelvas ni pases `null`: usa excepciones, objetos special case o colecciones vacías.
