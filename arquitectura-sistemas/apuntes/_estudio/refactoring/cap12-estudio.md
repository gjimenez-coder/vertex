# Big Refactorings (Grandes refactorizaciones) — Estudio

## Tarjetas de repaso

P: ¿Qué son las grandes refactorizaciones según el capítulo? / R: Cambios de diseño a gran escala que no se describen con mecánicas tan precisas como las pequeñas, porque cada situación cambia demasiado; fijan la dirección de muchísimos cambios.

P: ¿Por qué las grandes refactorizaciones carecen de mecánicas exactas? / R: Porque cada enredo es distinto y los autores no saben qué verás cuando las realices.

P: ¿Cómo se avanza en una gran refactorización en un sistema en producción? / R: "Mordisqueando los bordes" como Hansel y Gretel: un poco hoy, un poco más mañana, guiado por la necesidad de añadir funcionalidad o corregir errores, sin terminar de una vez.

P: ¿Qué condición de equipo exigen las grandes refactorizaciones? / R: Cierto grado de acuerdo en todo el equipo, que debe reconocer que una gran refactorización está "en juego" y actuar en consecuencia.

P: ¿Por qué importan las grandes refactorizaciones? / R: Porque la acumulación de decisiones de diseño a medio entender ahoga el programa como la maleza ahoga un canal; refactorizando, la comprensión plena del diseño queda reflejada en el programa.

P: ¿Qué problema resuelve Tease Apart Inheritance? / R: Una jerarquía de herencia que hace dos trabajos a la vez; se crean dos jerarquías y se usa delegación para invocar una desde la otra.

P: ¿Cómo se detecta una jerarquía que hace dos trabajos? / R: Si cada clase en un nivel tiene subclases que empiezan con el mismo adjetivo, probablemente haces dos trabajos con una sola jerarquía.

P: ¿En qué consiste Convert Procedural Design to Objects? / R: Convertir los registros de datos en objetos (datos tontos con accesores), descomponer el comportamiento con Extract Method y moverlo a los objetos con Move Method.

P: ¿Qué principio sustenta Separate Domain from Presentation? / R: El núcleo de model-view-controller (MVC): separar el código de interfaz (vista/presentación) de la lógica de dominio (modelo).

P: ¿Qué refactorización se usa para campos de ventana usados por presentación y dominio a la vez? / R: Duplicate Observed Data, para mantenerlos sincronizados.

P: ¿Qué problema resuelve Extract Hierarchy? / R: Una clase que hace demasiado por muchas sentencias condicionales (clase "navaja suiza"); se crea una jerarquía donde cada subclase representa un caso especial.

P: ¿De qué depende que Extract Hierarchy funcione? / R: De que la lógica condicional permanezca estática durante la vida del objeto; si no, puede hacer falta Extract Class antes.

P: ¿Qué refactorizaciones usa Extract Hierarchy para eliminar condicionales? / R: Replace Constructor with Factory Method, Replace Type Code with Subclasses (o with State/Strategy) y Replace Conditional with Polymorphism.

P: ¿Qué son los objetos strategy en el contexto de diseño procedural? / R: Pequeños objetos con comportamiento y pocos datos que varían comportamiento; son legítimos pero suelen ser pequeños y usados por necesidad de flexibilidad.

## Preguntas de autoevaluación

P: ¿Por qué cuesta convencer a los gerentes de emprender una gran refactorización y cómo se aborda? / R: Porque cuesta detener el progreso un par de meses solo para ordenar; se aborda avanzando poco a poco, "mordisqueando los bordes". (Sección: La naturaleza del juego)

P: En Tease Apart Inheritance, ¿qué trabajo se queda en la jerarquía actual y qué ocurre con las subclases vacías? / R: Se queda el trabajo más importante; el subsidiario se mueve a otra jerarquía con Extract Class y Move Method, y cuando una subclase queda vacía se elimina. (Sección: Tease Apart Inheritance)

P: En el ejemplo de `Deal`, ¿por qué se conserva esa jerarquía y se extrae el estilo de presentación? / R: Porque la "dealidad" del objeto importa más que el estilo de presentación; al final las diferencias de presentación se capturan con un par de variables sin subclases. (Sección: Tease Apart Inheritance)

P: ¿Cuál es la situación típica que motiva Convert Procedural Design to Objects? / R: Métodos largos y procedurales sobre una clase con pocos datos, y objetos de datos tontos con solo accesores; usar Java no basta para usar objetos. (Sección: Convert Procedural Design to Objects)

P: ¿Qué ventajas aporta separar presentación de dominio? / R: Separa dos partes complicadas, facilita modificarlas y permite múltiples presentaciones de la misma lógica. (Sección: Separate Domain from Presentation)

P: En el ejemplo de `Order Window`, ¿por qué se trabaja desde la ventana y qué da sensación de cierre? / R: Porque el mayor riesgo es mezclar presentación y dominio; mover todas las llamadas SQL al dominio y retirar el `import` de `java.sql` de la ventana da sensación de cierre. (Sección: Separate Domain from Presentation)

P: ¿Cuáles son las dos mecánicas de Extract Hierarchy y cuándo se usa cada una? / R: Cuando no tienes claras las variaciones, aíslas una a la vez con subclases y factory method; cuando las variaciones son claras desde el inicio, creas una subclase por variación y aplicas Replace Conditional with Polymorphism. (Sección: Extract Hierarchy)

P: En el ejemplo de la factura eléctrica, ¿cómo se empieza y qué pasa con las variaciones siguientes? / R: Se elige una variación recurrente (discapacidad), se aplica Replace Constructor with Factory Method y se copia `createBill` a la subclase para simplificarla; al estabilizarse el patrón, las variaciones siguientes (como lifeline) se vuelven más fáciles. (Sección: Extract Hierarchy)

## Puntos a dominar

- Entender que las grandes refactorizaciones toman meses o años y carecen de gratificación instantánea, pero marcan la dirección de muchos cambios.
- Reconocer cuándo una jerarquía hace dos trabajos (subclases con el mismo adjetivo) y aplicar Tease Apart Inheritance con delegación.
- Saber transformar diseño procedural en objetos: datos tontos con accesores, luego Extract Method y Move Method, hasta vaciar y borrar la clase original.
- Aplicar MVC para separar vista y modelo, mover el SQL al dominio y usar Duplicate Observed Data en campos compartidos.
- Convertir una clase "navaja suiza" en una jerarquía por caso especial con factory methods y Replace Conditional with Polymorphism, verificando que la condición sea estática durante la vida del objeto.
- Interiorizar la filosofía de avanzar "mordisqueando los bordes" y de atender primero al mayor riesgo.
