# Successive Refinement (Refinamiento sucesivo) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo? / R: Para escribir código limpio primero hay que escribir código sucio y luego limpiarlo; la limpieza es un proceso de refinamiento sucesivo, no una sola pasada de genialidad.

P: ¿Qué módulo sirve de hilo conductor? / R: La clase `Args`, un parser de argumentos de línea de comandos que se construye con un schema y el array de `main` y se consulta con `getBoolean`, `getInt`, `getString`.

P: ¿Qué declara el schema `"l,p#,d*"`? / R: `-l` como booleano, `-p` como entero (`#`) y `-d` como cadena (`*`).

P: ¿Qué se lanza cuando hay un problema de formato o de argumentos? / R: Una `ArgsException` con un `errorMessage` descriptivo.

P: ¿Cuál era el síntoma más visible del borrador inicial? / R: El número abrumador de variables de instancia: tres mapas separados (`booleanArgs`, `stringArgs`, `intArgs`) más `unexpectedArguments`, `argsFound`, `errorArgumentId`, etc.

P: Al añadir String e integer al borrador, ¿cuántos sitios había que tocar por cada tipo nuevo? / R: Tres: parsear su elemento de schema y elegir el mapa, parsearlo en la línea de comandos y convertirlo, y un método `getXXX` para devolverlo.

P: ¿Por qué el autor decidió parar y refactorizar? / R: Tenía al menos dos tipos más por añadir y seguir a la fuerza dejaría un desastre demasiado grande de arreglar; era el momento de hacer la estructura mantenible.

P: ¿Qué concepto nació del patrón "muchos tipos con métodos similares"? / R: `ArgumentMarshaler`, una clase base de la que derivan `BooleanArgumentMarshaler`, `StringArgumentMarshaler`, `IntegerArgumentMarshaler`.

P: ¿En qué disciplina se apoya el incrementalismo? / R: En TDD, cuya doctrina es mantener el sistema funcionando en todo momento, sin permitir cambios que lo rompan.

P: ¿Qué suite de pruebas usó para sostener el refactoring? / R: Pruebas unitarias en Java con JUnit y pruebas de aceptación escritas como páginas wiki en FitNesse.

P: ¿Cómo se eliminó el type-case (`instanceof`) en `setArgument`? / R: Con polimorfismo: bajando la lógica `set` a las derivadas hasta que `setArgument` fuera una única llamada a `m.set(currentArgument)`.

P: ¿Por qué se pasó un `Iterator<String>` a las funciones `set`? / R: Porque `setIntArg` usaba dos variables de instancia (`args` y `currentArg`); convertir `args` en lista y pasar un iterador redujo dos parámetros a uno y permitió bajar la lógica a las derivadas.

P: ¿Qué se hizo para demostrar que la estructura final era fácil de extender? / R: Se añadió el tipo `double` (`##`) con una prueba, detección en `parseSchemaElement`, una `DoubleArgumentMarshaler`, nuevos `ErrorCode` y un `getDouble`: "That was pretty painless".

P: Según el autor, ¿en qué consiste gran parte del buen diseño? / R: En la partición: crear los lugares adecuados para los distintos tipos de código, separando responsabilidades para que sea más simple de entender y mantener.

P: ¿Por qué mantener el código limpio continuamente es preferible a dejarlo pudrir? / R: Porque limpiar código podrido es carísimo (los módulos se entrelazan con dependencias ocultas), mientras que limpiar algo que ensuciaste hace cinco minutos es facilísimo.

## Preguntas de autoevaluación

P: ¿Qué quiere decir Martin con que conformarse con código que "funciona" es un suicidio profesional? / R: Que el código que solo funciona suele estar profundamente roto; los novatos creen que la meta es que funcione y abandonan el código ahí, mientras los veteranos saben que eso es inaceptable. (Secciones "How Did I Do This?" y "Conclusion")

P: ¿Cómo degeneró el código al crecer de forma incremental? / R: Una versión que solo soportaba booleanos era compacta, pero añadir String e integer tuvo impacto masivamente negativo porque cada tipo exigía tocar tres sitios distintos, acumulando mapas, variables y bloques try-catch. (Sección "Args: The Rough Draft")

P: ¿Por qué el incrementalismo exige arreglar de inmediato una prueba rota? / R: Porque la doctrina de TDD es mantener el sistema funcionando en todo momento; cuando cambiar el mapa de booleanos provocó un `NullPointerException`, había que mover la comprobación de null al marshaler antes de cualquier otro cambio. (Sección "On Incrementalism")

P: ¿Qué sorpresa aparecieron al usar `marshalers` en `getBoolean` y cómo se resolvió? / R: Las pruebas de FitNesse comprobaban que `getBoolean` sobre un argumento no booleano devolvía `false`; se añadió el manejo de `ClassCastException` y una prueba unitaria que invocaba todas las pruebas de FitNesse. (Sección "Moviendo la lógica a ArgumentMarshaler y a las derivadas")

P: ¿Por qué el autor compara el refactoring con un cubo de Rubik? / R: Porque avanza con muchísimos pasos diminutos (decenas), a veces metiendo algo para luego sacarlo, donde cada paso habilita el siguiente y las pruebas quedan verdes entre cada uno. (Sección "Eliminando el type-case con un Iterator")

P: ¿Qué compromiso de diseño supone poner `errorMessage` en `ArgsException`? / R: Poner el formateo de mensajes en `Args` violaba el SRP; moverlo a `ArgsException` es un compromiso: quien no quiera los mensajes enlatados deberá escribir los suyos, pero su conveniencia no es insignificante. (Sección "Añadir un nuevo tipo y separar las excepciones")

P: ¿Por qué el mal código degrada un proyecto más que otros factores? / R: Porque plazos, requisitos y dinámicas de equipo se pueden rehacer, pero el mal código se pudre y fermenta, crea dependencias ocultas entre módulos y arrastra al equipo, haciendo la limpieza muy cara. (Sección "Conclusion")

## Puntos a dominar

- Entender el refinamiento sucesivo: escribir código sucio y luego limpiarlo por iteraciones, como los borradores de un escrito.
- Reconocer cuándo parar: cuando añadir una funcionalidad más dejaría un desastre inmanejable, refactorizar antes de seguir.
- Saber que añadir tipos/casos sin revisar la estructura degrada el código (schema + set + get por cada tipo).
- Dominar el papel de TDD y una suite de pruebas (JUnit + FitNesse) para mantener el sistema funcionando en cada paso.
- Aplicar polimorfismo con `ArgumentMarshaler` para eliminar el type-case (`instanceof`) y unificar en `m.set(currentArgument)`.
- Usar un `Iterator<String>` para reducir parámetros y habilitar bajar la lógica a las clases derivadas.
- Valorar la partición (separación de responsabilidades) como núcleo del buen diseño.
- Interiorizar que mantener el código limpio de forma continua es barato y dejar que se pudra es carísimo.
