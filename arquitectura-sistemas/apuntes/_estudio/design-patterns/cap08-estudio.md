# Favorece la composición sobre la herencia (Favor composition over inheritance) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo? / R: Favorecer la composición sobre la herencia para evitar jerarquías rígidas y poder sustituir comportamiento en tiempo de ejecución.

P: ¿Qué relación expresa la herencia? / R: La relación "is a" (es un/a); por ejemplo, un auto es un medio de transporte.

P: ¿Qué relación expresa la composición? / R: La relación "tiene un/a" (has a); por ejemplo, un auto tiene un motor.

P: ¿Por qué la herencia es atractiva al principio? / R: Porque es la forma más obvia y sencilla de reutilizar código entre clases, extrayendo el código común a una clase base.

P: ¿Puede una subclase reducir la interfaz de la superclase? / R: No; debe implementar todos los métodos abstractos de la clase padre, aunque no vaya a usarlos.

P: ¿Qué cuidado exige sobrescribir un método heredado? / R: Que el nuevo comportamiento sea compatible con el de base, porque la subclase puede pasarse a cualquier código que espere la superclase sin romperlo.

P: ¿Cómo rompe la herencia la encapsulación? / R: Los detalles internos del padre quedan disponibles para la subclase, e incluso la superclase puede llegar a conocer detalles de las subclases.

P: ¿Qué acoplamiento introduce la herencia? / R: Las subclases quedan fuertemente acopladas a las superclases: un cambio en la superclase puede descomponer la funcionalidad de las subclases.

P: ¿Qué es la explosión combinatoria de subclases? / R: Al heredar en varias dimensiones (carga × motor × navegación), cada parámetro multiplica el número de subclases y duplica código, porque una subclase no puede extender dos clases a la vez.

P: ¿Cómo resuelve la composición la explosión combinatoria? / R: Extrae cada dimensión de funcionalidad a su propia jerarquía de clases y los objetos delegan en ellas, en lugar de implementar todo por su cuenta.

P: ¿Qué ventaja adicional en tiempo de ejecución ofrece la composición? / R: Permite sustituir un comportamiento cambiando el objeto vinculado, por ejemplo asignando otro objeto de motor distinto.

P: ¿A qué patrón se parece la estructura por composición del ejemplo? / R: Al patrón Strategy, explicado más adelante en el libro.

P: ¿Qué es la agregación frente a la composición? / R: Una variante más relajada en la que un objeto referencia a otro pero no gestiona su ciclo vital; p. ej., un auto tiene un conductor que puede usar otro auto o caminar.

P: ¿Qué significa SOLID? / R: Una regla mnemotécnica de cinco principios de diseño para hacer el software más comprensible, flexible y fácil de mantener.

P: ¿Qué advierte el autor sobre SOLID? / R: Que aplicarlos de forma descuidada puede hacer más mal que bien y complicar la arquitectura; conviene ser pragmático y no tomarlos como dogma.

## Preguntas de autoevaluación

P: ¿Por qué la herencia resulta problemática recién cuando el programa ya tiene muchas clases? / R: Porque sus contras no se notan al inicio, sino cuando la jerarquía ha crecido y cambiarlo todo resulta complicado. (Lo que necesitas saber)

P: En el catálogo de automóviles, ¿qué provoca extender la clase en varias dimensiones con herencia? / R: Una explosión combinatoria de subclases y mucho código duplicado, porque una subclase no puede extender dos clases al mismo tiempo. (El ejemplo que recorre el capítulo)

P: ¿Cómo delega el comportamiento un objeto de auto en la solución por composición? / R: En lugar de implementar el comportamiento por su cuenta, lo delega a otros objetos; las dimensiones de funcionalidad se extraen a sus propias jerarquías. (El ejemplo que recorre el capítulo)

P: ¿Qué riesgo implica que una subclase pueda pasarse a código que espera la superclase? / R: Que un comportamiento sobrescrito incompatible rompa ese código; por eso el nuevo comportamiento debe ser compatible con el de base. (Problemas de la herencia)

P: ¿Qué son las jerarquías de herencia paralelas? / R: El resultado de reutilizar código por herencia en dos o más dimensiones, que obliga a crear muchas combinaciones de clases e hincha la jerarquía hasta un tamaño ridículo. (Problemas de la herencia)

P: Con el ejemplo del conductor, ¿por qué es agregación y no composición? / R: Porque el auto solo referencia al conductor sin gestionar su ciclo vital: ese conductor puede usar otro auto o caminar sin el auto. (Composición (y agregación))

P: ¿Quién presentó los principios SOLID y en qué obra? / R: Robert Martin, en *Desarrollo ágil de software: principios, patrones y prácticas* (*Agile Software Development, Principles, Patterns, and Practices*). (Principios SOLID)

P: ¿Por qué el autor duda de aplicar todos los principios SOLID a la vez? / R: Porque su costo puede volver el programa más complicado de lo necesario, y duda de que exista un producto exitoso que los aplique todos simultáneamente. (Principios SOLID)

## Puntos a dominar

- Distinguir la relación "is a" (herencia) de "tiene un/a" (composición) y saber cuándo expresa cada una el diseño correcto.
- Enumerar los cinco problemas de la herencia: no reducir la interfaz, compatibilidad al sobrescribir, ruptura de la encapsulación, acoplamiento fuerte y jerarquías paralelas.
- Explicar la explosión combinatoria de subclases con el ejemplo de carga × motor × navegación.
- Describir cómo la composición extrae cada dimensión a su propia jerarquía y delega el comportamiento.
- Reconocer que la composición permite sustituir comportamiento en tiempo de ejecución y que se parece al patrón Strategy.
- Diferenciar composición de agregación según la gestión del ciclo vital del objeto contenido.
- Recordar qué es SOLID y la advertencia de pragmatismo del autor sobre su aplicación.
