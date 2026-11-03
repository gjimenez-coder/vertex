# Code Simplicity: The Fundamentals of Software — Max Kanat-Alexander (O'Reilly Media, 2012)
## Capítulo 3 — The Driving Forces of Software Design (Las fuerzas que impulsan el diseño de software)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo busca una orientación común para toda la ciencia del diseño de software: saber por qué escribimos software y cuál es su meta final. La tesis central es que existe un único propósito para todo el software, y que ese propósito debe guiar las decisiones de diseño.

Ese propósito es "ayudar a las personas" (to help people). Max Kanat-Alexander lo sitúa por encima de una ley: lo llama "el Propósito del Software". De este propósito el autor deriva luego los objetivos concretos del diseño de software, cerrando con una justificación de por qué la facilidad de mantenimiento es inseparable de ser útil.

Sales sabiendo cómo usar la pregunta "¿cuánto ayuda esto a los usuarios?" para priorizar y evaluar cualquier cambio, y entendiendo los tres objetivos del diseño de software que el autor plantea.

## El propósito del software

Todo el software existe para ayudar a las personas. El propósito general puede concretarse por pieza de software: un procesador de texto ayuda a escribir, un navegador web ayuda a navegar por la Web, y el software de contabilidad ayuda a los contadores.

Puntos clave sobre el propósito:

- El software nunca existe para ayudar a objetos inanimados ni a la computadora; siempre ayuda a personas. Incluso al escribir bibliotecas, se ayuda a programadores, que son personas.
- El software que ayuda a animales o plantas en realidad ayuda a personas a ayudar a animales o plantas.
- "Ayudar", según el diccionario que cita el autor (Webster's New World Dictionary of the American Language), es "hacer más fácil para (una persona) hacer algo; ayudar, asistir... hacer parte del trabajo de; aliviar o compartir la labor".
- *Con qué* se ayuda queda a elección de cada quien (organizar una agenda, escribir un libro, planear una dieta); lo invariable es que el propósito sea ayudar.

El propósito del software no es "ganar dinero" ni "demostrar lo inteligente que soy". Diseñar solo con esos fines viola el propósito del software y probablemente lleve a software de menor calidad. Ganar dinero puede ser un fin personal o de la organización —no está mal—, pero no debe ser el propósito del software; además, el ingreso suele estar ligado a cuánto ayuda el software. El autor observa que quien no concibe ayudar a otra persona escribirá mal software, y plantea como hipótesis que la capacidad de escribir buen software está limitada por la capacidad de concebir cómo ayudar a otro.

Como principio rector, al decidir sobre el software la pregunta base es cómo podemos ayudar. Hay grados de ayuda (mucho o poco, a muchos o a pocos), y eso permite priorizar funcionalidades: la que más ayude a las personas recibe la mayor prioridad.

## Aplicación en el mundo real (Real-World Application)

El ejemplo hilo conductor es escribir un editor de texto para programadores. Lo primero es definir el propósito; conviene mantenerlo simple, por ejemplo "ayudar a los programadores a editar texto". Se puede ser más específico, pero si el grupo no se pone de acuerdo, basta con uno simple.

Con el propósito definido, para cada solicitud de funcionalidad se pregunta: "¿Cómo ayudaría esta función a que los programadores editen texto?". Si la respuesta es "no ayudaría", se descarta de inmediato. Para las demás, se escribe la respuesta en una frase corta. Ejemplo: ante la petición de atajos de teclado para acciones comunes, la respuesta sería que ayuda a los programadores porque les permite interactuar con el programa más rápido sin dejar de escribir. No hace falta escribirlo literalmente; basta con tener clara la respuesta.

Otras razones útiles para hacerse esta pregunta:

- Resuelve dudas sobre la descripción o la implementación de la función. En el ejemplo, la respuesta indica que la implementación debe ser rápida, porque ahí está el valor para el usuario.
- Ayuda al equipo a acordar el valor de una función. Quien no simpatice con los atajos de teclado puede, aun así, aceptar la razón de su valor; e incluso alguien puede idear una mejor forma de cubrir la necesidad real (interactuar más rápido) sin atajos. La respuesta dice lo que de verdad se necesita, no solo lo que el usuario creyó querer.
- Hace evidente que unas funciones son más importantes que otras, lo que ayuda a los líderes del proyecto a priorizar.
- En el peor caso, si el editor se ha vuelto inflado con demasiadas funciones, la respuesta ayuda a decidir cuáles eliminar.

También puede hacerse una lista de errores (bugs) y plantear la pregunta inversa: "¿Cómo estorba este error la edición de texto de los programadores?". A veces la respuesta es obvia y no necesita escribirse (si el programa se cuelga al guardar un archivo, no hace falta explicar por qué eso es malo).

## Los objetivos del diseño de software (The Goals of Software Design)

Del propósito del software el autor deriva tres objetivos para la ciencia del diseño:

1. Permitirnos escribir software que sea lo más útil posible.
2. Permitir que nuestro software siga siendo lo más útil posible (normalmente queremos que la gente siga recibiendo ayuda con el tiempo).
3. Diseñar sistemas que puedan crearse y mantenerse tan fácilmente como sea posible por sus programadores, de modo que puedan ser —y seguir siendo— lo más útiles posible.

Sobre estos objetivos:

- El tercero es el que tradicionalmente se piensa como "el objetivo" del diseño, aunque no se enuncie explícitamente. Pero el primero y el segundo son necesarios para recordar que ser útil ahora y en el futuro es la motivación del tercero.
- La frase "tan fácilmente como sea posible" importa: la idea es hacer los programas fáciles de crear y mantener, no difíciles ni complejos. No todo será fácil de inmediato (aprender una tecnología o diseñar bien lleva tiempo), pero a largo plazo las decisiones deben facilitar la creación y el mantenimiento.
- El mayor obstáculo actual para escribir y mantener software útil es la dificultad real del diseño y la programación. Cuando el software es difícil de crear o modificar, los programadores gastan su tiempo en hacer que "simplemente funcione" y menos en ayudar al usuario; cuando es fácil de trabajar y mantener, pueden centrarse en la utilidad.
- A veces el primer objetivo (ser útil) y el tercero (facilidad de mantenimiento) entran en conflicto: hacer el software más útil puede complicar su mantenimiento. Sin embargo, históricamente han estado más en conflicto de lo necesario: es totalmente posible crear un sistema mantenible y a la vez muy útil. Si no se hace mantenible, será muy difícil cumplir el segundo objetivo (seguir siendo útil). Por eso el tercer objetivo es importante: sin él no se logran los dos primeros.

## Ideas clave

- El propósito de todo el software es ayudar a las personas; nunca ayudar a objetos ni a la computadora.
- "Ayudar" es hacer más fácil que alguien haga algo; con qué se ayuda es libre, el propósito de ayudar no.
- Ganar dinero o lucirse no deben ser el propósito del software; diseñar así suele dar peor calidad.
- Pregunta rectora para priorizar funciones y evaluar cambios: "¿cuánto ayuda esto a los usuarios?".
- En la práctica, define un propósito simple y evalúa cada funcionalidad por cómo cumple ese propósito; descarta lo que no ayuda.
- La misma pregunta resuelve dudas de implementación, alinea al equipo, prioriza y permite recortar funciones innecesarias.
- Tres objetivos del diseño: ser lo más útil posible, seguir siéndolo, y ser fácil de crear y mantener.
- La facilidad de mantenimiento no es opcional: es la condición para que el software siga siendo útil en el tiempo.
