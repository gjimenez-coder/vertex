# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 8 — Favorece la composición sobre la herencia (Favor composition over inheritance)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con muchas palabras pegadas por la justificación de párrafos); las citas usan la página del PDF.

## Lo que necesitas saber

La herencia es la forma más obvia y sencilla de reutilizar código entre clases: se extrae el código común a una clase base. Pero tiene contras que no se notan hasta que el programa tiene demasiadas clases y cambiarlo todo resulta complicado. El capítulo enumera esos problemas y propone la composición como alternativa.

La tesis central es que conviene favorecer la composición sobre la herencia. La herencia expresa la relación "is a" (es un/a) —un auto es un medio de transporte—, mientras que la composición expresa la relación "tiene un/a" (has a) —un auto tiene un motor—. Delegar comportamiento a otros objetos evita jerarquías rígidas y permite sustituir ese comportamiento en tiempo de ejecución.

Sales sabiendo por qué la herencia acopla fuertemente subclases y superclases y provoca explosión combinatoria de clases cuando hay varias dimensiones de variación, y cómo la composición resuelve ese problema extrayendo cada dimensión a su propia jerarquía. El capítulo cierra introduciendo los principios SOLID.

## El ejemplo que recorre el capítulo

Una aplicación de catálogo para un fabricante de automóviles. La empresa fabrica autos y camiones; pueden ser eléctricos o de gasolina; y todos los modelos pueden tener controles manuales o piloto automático.

Con herencia, extender la clase en varias dimensiones (tipo de carga × tipo de motor × tipo de navegación) provoca una explosión combinatoria de subclases: cada parámetro adicional multiplica el número de subclases y aparece mucho código duplicado, porque una subclase no puede extender dos clases al mismo tiempo.

Con composición, en lugar de que los objetos de auto implementen el comportamiento por su cuenta, lo delegan a otros objetos. Las distintas "dimensiones" de funcionalidad se extraen a sus propias jerarquías de clases. Como ventaja adicional, se puede sustituir un comportamiento durante el tiempo de ejecución: por ejemplo, cambiar el objeto de motor vinculado a un auto asignándole simplemente otro objeto de motor distinto. Esta estructura se parece al patrón Strategy, que se explica más adelante en el libro.

## Problemas de la herencia

El texto lista los inconvenientes que aparecen cuando la jerarquía crece:

- Una subclase no puede reducir la interfaz de la superclase: tiene que implementar todos los métodos abstractos de la clase padre, aunque no vaya a usarlos.
- Al sobrescribir métodos debes asegurarte de que el nuevo comportamiento sea compatible con el de base, porque los objetos de la subclase pueden pasarse a cualquier código que espere objetos de la superclase y no quieres que ese código se rompa.
- La herencia rompe la encapsulación de la superclase, porque los detalles internos de la clase padre quedan disponibles para la subclase. También puede darse la situación opuesta: que un programador haga que una superclase conozca algunos detalles de las subclases para facilitar futuras extensiones.
- Las subclases están fuertemente acopladas a las superclases: cualquier cambio en una superclase puede descomponer la funcionalidad de las subclases.
- Reutilizar código mediante herencia puede conducir a jerarquías de herencia paralelas. La herencia suele suceder en una única dimensión, pero con dos o más dimensiones hay que crear muchas combinaciones de clases, hinchando la jerarquía hasta un tamaño ridículo.

## Composición (y agregación)

La composición es la alternativa a la herencia. Frente al "is a" de la herencia, la composición se basa en la relación "tiene un/a".

El principio también se aplica a la agregación, una variante más relajada de la composición en la que un objeto puede contener una referencia a otro pero no gestiona su ciclo vital. Ejemplo del texto: un auto tiene un conductor, pero ese conductor puede utilizar otro auto o caminar sin el auto.

## Principios SOLID

Una vez conocidos los principios básicos de diseño, el capítulo presenta los cinco que se conocen popularmente como principios SOLID. Robert Martin los presentó en el libro *Desarrollo ágil de software: principios, patrones y prácticas* (*Agile Software Development, Principles, Patterns, and Practices*).

SOLID es una regla mnemotécnica para cinco principios de diseño ideados para hacer que los diseños de software sean más comprensibles, flexibles y fáciles de mantener.

Advertencia del autor: aplicar estos principios de forma descuidada puede hacer más mal que bien. El costo de aplicarlos en la arquitectura de un programa es que puede volverlo más complicado de lo que debería. El autor duda de que exista un producto de software exitoso en el que se apliquen todos estos principios al mismo tiempo. Aspirar a ellos es bueno, pero conviene ser siempre pragmático y no tomar todo lo escrito como un dogma.

## Ideas clave

- La herencia es la forma más obvia de reutilizar código, pero introduce acoplamiento fuerte y rigidez a medida que crece la jerarquía.
- Una subclase no puede reducir la interfaz de la superclase y debe implementar todos sus métodos abstractos, aunque no los use.
- La herencia rompe la encapsulación: los detalles internos del padre quedan expuestos a la subclase.
- La herencia en varias dimensiones provoca explosión combinatoria de subclases y código duplicado.
- La herencia expresa "is a"; la composición expresa "tiene un/a" (has a).
- La composición delega el comportamiento a otros objetos y permite sustituirlo en tiempo de ejecución.
- La agregación es una composición relajada: un objeto referencia a otro sin gestionar su ciclo vital (auto y conductor).
- SOLID son cinco principios para diseños más comprensibles, flexibles y mantenibles; aplicarlos sin pragmatismo puede perjudicar.
