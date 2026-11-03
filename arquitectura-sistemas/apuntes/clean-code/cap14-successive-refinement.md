# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 14 — Successive Refinement (Refinamiento sucesivo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

Este capítulo es un caso de estudio de refinamiento sucesivo: Martin muestra un módulo (un parser de argumentos de línea de comandos llamado `Args`) que empezó bien pero no escaló, y cómo lo refactorizó y limpió hasta llegar a una versión elegante. La tesis central es que no basta con que el código funcione: para escribir código limpio primero hay que escribir código sucio y luego limpiarlo, igual que un escritor pasa de un borrador a sucesivas revisiones. Conformarse con código que "funciona" y dejarlo en ese estado es, según el autor, un suicidio profesional.

Sales sabiendo que la limpieza del código es un proceso incremental disciplinado, no un acto de genialidad en una sola pasada. El autor insiste en la importancia de parar a tiempo: cuando añadir una funcionalidad más convertiría el código en un montón inmanejable, hay que detenerse y refactorizar antes de seguir. También aprendes a sostener ese refactoring con una suite de pruebas automatizadas que mantiene el sistema funcionando en todo momento.

La enseñanza práctica es doble: por un lado, cómo degenera el código cuando se le añaden tipos/casos de forma incremental sin revisar la estructura; por otro, cómo una buena partición (separación de responsabilidades) y el uso de polimorfismo eliminan los `type-case` (cadenas de `if/else` sobre tipos) y simplifican radicalmente el módulo.

## El ejemplo que recorre el capítulo

El hilo conductor es la clase `Args`. Se construye con una cadena de formato (schema) y el array de argumentos de `main`, y luego se consulta con métodos como `getBoolean`, `getInt`, `getString`. El schema define los argumentos: por ejemplo `"l,p#,d*"` declara `-l` booleano, `-p` entero y `-d` cadena. Si hay un problema de formato o de argumentos, se lanza una `ArgsException` con un `errorMessage` descriptivo.

```java
public static void main(String[] args) {
  try {
    Args arg = new Args("l,p#,d*", args);
    boolean logging = arg.getBoolean('l');
    int port = arg.getInt('p');
    String directory = arg.getString('d');
    executeApplication(logging, port, directory);
  } catch (ArgsException e) {
    System.out.printf("Argument error: %s\n", e.errorMessage());
  }
}
```

Primero se presenta la versión final limpia (basada en el concepto `ArgumentMarshaler`), y luego el capítulo retrocede para mostrar los borradores y reconstruir el camino hacia ella (PDF p. 225).

## How Did I Do This? (¿Cómo lo hice?)

Martin aclara que no escribió el programa limpio de una sola vez. "To write clean code, you must first write dirty code and then clean it" (PDF p. 231). Compara el proceso con los borradores sucesivos de una composición escolar: la escritura limpia es cuestión de refinamiento sucesivo. La mayoría de los programadores novatos creen que la meta es "que funcione" y abandonan el código en ese estado; los programadores veteranos saben que eso es inaceptable.

## Args: The Rough Draft (El borrador)

El primer borrador "funciona" pero es un desastre (PDF p. 232). El síntoma más visible es el número abrumador de variables de instancia: tres mapas separados (`booleanArgs`, `stringArgs`, `intArgs`), más `unexpectedArguments`, `argsFound`, `errorArgumentId`, `errorParameter`, `errorCode`, etc. Aparecen cadenas raras como `"TILT"`, mezcla de `HashSet`/`TreeSet` y bloques `try-catch-catch` que se acumulan en un "festering pile" (montón fermentando).

El autor muestra cómo creció el desastre. Una versión anterior que solo soportaba booleanos (Listing 14-9) era compacta, simple y fácil de entender, pero ya contenía las semillas del problema. Añadir solo dos tipos más de argumento (String e integer) tuvo un impacto masivamente negativo: cada nuevo tipo exigía tocar tres sitios distintos:

- Una forma de parsear su elemento de schema y seleccionar el mapa adecuado.
- Parsearlo en las cadenas de línea de comandos y convertirlo a su tipo real.
- Un método `getXXX` para devolverlo al llamante con su tipo real.

## So I Stopped (Así que paré)

Tenía al menos dos tipos más por añadir y sabía que empeorarían mucho las cosas. Si seguía adelante a la fuerza dejaría un desastre demasiado grande de arreglar. "If the structure of this code was ever going to be maintainable, now was the time to fix it" (PDF p. 243). El patrón repetido —muchos tipos con métodos similares— "suena a una clase": así nació el concepto `ArgumentMarshaler`.

## On Incrementalism (Sobre el incrementalismo)

Una de las mejores formas de arruinar un programa es hacer cambios masivos a su estructura en nombre de la mejora; algunos programas nunca se recuperan de esas "mejoras". Para evitarlo, Martin usa la disciplina de Test-Driven Development (TDD): una de sus doctrinas centrales es mantener el sistema funcionando en todo momento, sin permitir ningún cambio que lo rompa.

Para ello necesitaba una suite de pruebas automatizadas que verificara que el comportamiento no cambiaba. Tenía pruebas unitarias en Java con JUnit y pruebas de aceptación escritas como páginas wiki en FitNesse. Procedió con muchísimos cambios diminutos; cada uno acercaba la estructura al concepto `ArgumentMarshaler` y mantenía el sistema funcionando.

El primer paso fue añadir el esqueleto de `ArgumentMarshaler` al final del montón (no rompía nada) y luego el cambio más simple posible: cambiar el `HashMap` de booleanos para que usara `ArgumentMarshaler`. Esto rompió algunas pruebas (p. ej. `getBoolean('y')` devolvía `null` y provocaba `NullPointerException`); el incrementalismo exigía arreglarlo de inmediato antes de cualquier otro cambio, moviendo la comprobación de null al marshaler. Un detalle de estilo: acortó el nombre de variable largo y redundante a `am`.

## Moviendo la lógica a ArgumentMarshaler y a las derivadas

La estrategia fue: primero concentrar todo el comportamiento de marshalling en la clase base `ArgumentMarshaler`, y luego empujarlo gradualmente hacia las derivadas (`BooleanArgumentMarshaler`, `StringArgumentMarshaler`, `IntegerArgumentMarshaler`), manteniendo las pruebas verdes en cada paso.

- Se crearon métodos abstractos `set` y `get`. El `get` devuelve `Object`, lo que obliga a hacer cast (p. ej. a `Boolean`), algo que el autor reconoce como "feo".
- Al deployar `set`/`get` a cada derivada se eliminaban las funciones viejas y se bajaban las variables a la clase correspondiente.
- El `set` abstracto recibía un `String` aunque la implementación booleana no lo usara, porque String e Integer sí lo necesitarían.

Después se eliminaron los tres mapas separados: se añadió un único `Map` `marshalers` y, uno a uno, se migraron los métodos para usarlo en lugar de los mapas originales. Los métodos `isBooleanArg`, `isStringArg`, `isIntArg` pasaron a usar `instanceof` y luego se incorporaron (inline) en `setArgument`, dejando una cadena `if/else` con `instanceof` (un type-case).

Al introducir el uso de `marshalers` en `getBoolean` apareció una sorpresa: las pruebas de FitNesse comprobaban que llamar `getBoolean` sobre un argumento no booleano devolvía `false`, cosa que las unitarias no verificaban. Por eso se añadió el manejo de `ClassCastException`. Para evitar sorpresas, el autor añadió una prueba unitaria que invocaba todas las pruebas de FitNesse (PDF p. 255).

## Eliminando el type-case con un Iterator

Tras el primer refactoring (Listing 14-12), el resultado seguía siendo decepcionante: muchas variables arriba, un horrible type-case en `setArgument` y funciones `set` feas. El objetivo era que `setArgument` fuera una única llamada a `ArgumentMarshaler.set`, lo que exigía bajar `setIntArg`, `setStringArg` y `setBooleanArg` a las derivadas.

El problema: `setIntArg` usaba dos variables de instancia (`args` y `currentArg`); pasarlas ambas como parámetros era sucio. La solución fue convertir el array `args` en una lista y pasar un `Iterator<String>` a las funciones `set`. Esto se hizo en diez pasos, con las pruebas pasando tras cada uno.

Luego se añadió el método abstracto `set(Iterator<String> currentArgument)`, se implementó en cada derivada, y se fue eliminando `setBooleanArg`, `setStringArg` y `setIntArg` sustituyéndolos por `m.set(currentArgument)`. El autor señala que refactorizar es como resolver un cubo de Rubik: muchos pasitos (a veces metes algo para luego sacarlo) donde cada paso habilita el siguiente. Finalmente:

```java
private boolean setArgument(char argChar) throws ArgsException {
  ArgumentMarshaler m = marshalers.get(argChar);
  if (m == null)
    return false;
  try {
    m.set(currentArgument);
    return true;
  } catch (ArgsException e) {
    valid = false;
    errorArgumentId = argChar;
    throw e;
  }
}
```

El type-case desapareció ("Touché!") y `ArgumentMarshaler` se convirtió en una interfaz.

## Añadir un nuevo tipo y separar las excepciones

Para demostrar lo fácil que es extender la estructura, se añadió el tipo `double` (`##`): una prueba, la detección `##` en `parseSchemaElement`, una clase `DoubleArgumentMarshaler`, nuevos `ErrorCode` (`MISSING_DOUBLE`, `INVALID_DOUBLE`) y un `getDouble`. "That was pretty painless" (PDF p. 269).

Después se fusionaron todas las excepciones en una sola clase `ArgsException` movida a su propio módulo, eliminando la dependencia de `ParseException`. Esto permitió sacar de `Args` todo el código de soporte de errores. El proceso completo fueron unos 30 pasos diminutos manteniendo las pruebas en verde (PDF p. 273). El autor destaca que gran parte del buen diseño es simplemente partición: crear los lugares adecuados para los distintos tipos de código. Esa separación de responsabilidades hace el código más simple de entender y mantener.

Un matiz interesante: poner el formateo de mensajes en `Args` violaba el SRP, pero mover `errorMessage` a `ArgsException` es un compromiso. Quien no quiera esos mensajes "enlatados" deberá escribir los suyos, aunque la conveniencia de tenerlos listos no es insignificante.

## Conclusion (Conclusión)

No basta con que el código funcione; el código que funciona a menudo está profundamente roto y conformarse con eso es comportarse de forma poco profesional. Nada degrada un proyecto a largo plazo tanto como el mal código: los malos plazos, requisitos y dinámicas de equipo se pueden rehacer, pero el mal código se pudre y fermenta, arrastrando al equipo. Limpiar código podrido es muy caro porque los módulos se entrelazan creando dependencias ocultas. En cambio, mantener el código limpio es relativamente fácil: si ensuciaste un módulo por la mañana, es fácil limpiarlo por la tarde; mejor aún, si lo ensuciaste hace cinco minutos, es facilísimo limpiarlo ahora. La solución es mantener el código tan limpio y simple como sea posible de forma continua: nunca dejes que la podredumbre empiece.

## Ideas clave

- Para escribir código limpio hay que escribir primero código sucio y luego limpiarlo; es un proceso de refinamiento sucesivo, no una sola pasada.
- Añadir tipos/casos de forma incremental sin revisar la estructura degrada rápidamente el código: cada tipo tocaba el parseo del schema, el set y el get.
- Saber parar a tiempo es clave: cuando añadir una funcionalidad más dejaría un desastre inmanejable, hay que refactorizar antes de seguir.
- El incrementalismo se apoya en TDD: mantener el sistema funcionando en todo momento con pruebas unitarias (JUnit) y de aceptación (FitNesse).
- El refactoring avanza con pasos diminutos (decenas de ellos), manteniendo las pruebas verdes entre cada uno; es como resolver un cubo de Rubik.
- El concepto `ArgumentMarshaler` con polimorfismo permite eliminar el type-case (`instanceof`) y unificar el set en `m.set(currentArgument)`.
- Pasar un `Iterator<String>` en vez de `args` y `currentArg` reduce dos parámetros a uno y habilita bajar la lógica a las derivadas.
- Gran parte del buen diseño es partición: separar responsabilidades (p. ej. mover `ArgsException` a su módulo) hace el código más simple de entender y mantener.
- Mantener el código limpio continuamente es barato; dejar que se pudra lo vuelve carísimo de arreglar.
