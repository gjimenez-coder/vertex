# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)
## Capítulo 4 — ¿Qué es un patrón de diseño? (What's a Design Pattern?)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF (con palabras pegadas por la justificación) y las citas usan la página del PDF.

## Lo que necesitas saber

Los patrones de diseño son soluciones habituales a problemas que ocurren con frecuencia en el diseño de software. El capítulo los presenta como planos prefabricados que se pueden personalizar para resolver un problema de diseño recurrente en tu código, en lugar de porciones de código listas para copiar.

La tesis central es que un patrón no es una porción específica de código, sino un concepto general para resolver un problema particular. Puedes seguir los detalles del patrón e implementar una solución que encaje con las realidades de tu propio programa, de modo que el mismo patrón aplicado a dos programas distintos puede resultar en código diferente.

Sales sabiendo qué distingue un patrón de un algoritmo, cómo se describe formalmente un patrón, cómo se clasifican, su origen histórico y por qué conviene aprenderlos.

## Patrón frente a algoritmo

A menudo los patrones se confunden con algoritmos porque ambos describen soluciones típicas a problemas conocidos. La diferencia: un algoritmo siempre define un grupo claro de acciones para lograr un objetivo, mientras que un patrón es una descripción de más alto nivel de una solución.

El capítulo usa una analogía: un algoritmo es como una receta de cocina, con pasos claros para alcanzar una meta; un patrón es más similar a un plano, porque puedes observar cómo son su resultado y sus funciones, pero el orden exacto de la implementación depende de ti.

## ¿En qué consiste el patrón?

La mayoría de los patrones se describe con mucha formalidad para que la gente pueda reproducirlos en muchos contextos. Las secciones que suelen estar presentes en la descripción de un patrón son:

- **El propósito**: explica brevemente el problema y la solución.
- **La motivación**: explica en más detalle el problema y la solución que brinda el patrón.
- **La estructura de las clases**: muestra cada una de las partes del patrón y el modo en que se relacionan.
- **El ejemplo de código** en uno de los lenguajes de programación populares: facilita asimilar la idea que se esconde tras el patrón.

Algunos catálogos de patrones enumeran otros detalles útiles, como la aplicabilidad del patrón, los pasos de implementación y las relaciones con otros patrones.

## Clasificación de los patrones

Los patrones de diseño varían en su complejidad, nivel de detalle y escala de aplicabilidad al sistema completo. El autor usa la analogía de la construcción de carreteras: puedes hacer más segura una intersección instalando semáforos o construyendo un intercambiador completo de varios niveles con pasajes subterráneos para peatones.

Por nivel:

- **Idioms**: los patrones más básicos y de más bajo nivel. Normalmente se aplican a un único lenguaje de programación.
- **Patrones de arquitectura**: los más universales y de más alto nivel. Se pueden implementar prácticamente en cualquier lenguaje y, a diferencia de otros patrones, sirven para diseñar la arquitectura de una aplicación completa.

Además, todos los patrones pueden clasificarse por su propósito. El libro cubre tres grupos generales:

- **Patrones creacionales**: proporcionan mecanismos de creación de objetos que incrementan la flexibilidad y la reutilización de código existente.
- **Patrones estructurales**: explican cómo ensamblar objetos y clases en estructuras más grandes a la vez que se mantiene la flexibilidad y eficiencia de la estructura.
- **Patrones de comportamiento**: se encargan de una comunicación efectiva y la asignación de responsabilidades entre objetos.

## ¿Quién inventó los patrones de diseño?

El autor la llama una buena, aunque imprecisa pregunta. Los patrones no son conceptos opacos y sofisticados: son soluciones habituales a problemas comunes en el diseño orientado a objetos. Cuando una solución se repite una y otra vez en varios proyectos, al final alguien le pone un nombre y la explica en detalle; así se descubre un patrón.

El concepto de los patrones fue descrito por Christopher Alexander en *El lenguaje de patrones*. El libro habla de un "lenguaje" para diseñar el entorno urbano, cuyas unidades son los patrones: pueden describir lo altas que tienen que ser las ventanas, cuántos niveles debe tener un edificio, cuán grandes deben ser las zonas verdes de un barrio, etcétera.

La idea fue recogida por cuatro autores: Erich Gamma, John Vlissides, Ralph Johnson y Richard Helm. En 1995 publicaron *Patrones de diseño*, aplicando el concepto a la programación. El libro presentaba 23 patrones que resolvían varios problemas del diseño orientado a objetos y se convirtió pronto en un éxito de ventas. Por su largo título en inglés, la gente empezó a llamarlo el libro de la "gang of four (banda de los cuatro)", que pronto se abrevió a "el libro GoF".

Desde entonces se han descubierto decenas de nuevos patrones orientados a objetos, y la "metodología del patrón" se hizo muy popular en otros campos de la programación, por lo que hoy existen muchos otros patrones no relacionados con el diseño orientado a objetos.

## ¿Por qué debería aprender sobre patrones?

La realidad es que podrías trabajar durante años como programador sin conocer un solo patrón, e incluso implementarlos sin saberlo. Aun así, el autor da dos razones para dedicar tiempo a aprenderlos:

- Son un juego de herramientas de soluciones comprobadas a problemas habituales en el diseño de software. Aunque nunca te encuentres con esos problemas, conocer los patrones sigue siendo útil, porque te enseña a resolver todo tipo de problemas usando principios del diseño orientado a objetos.
- Definen un lenguaje común que puedes usar con tus compañeros de equipo para comunicaros de forma más eficiente. Podrías decir "Oh, utiliza un singleton para eso" y todos entenderían la idea sin necesidad de explicar qué es un singleton, si conocen el patrón y su nombre.

## Ideas clave

- Un patrón de diseño es un concepto general (como un plano), no una porción de código reutilizable.
- Patrón vs. algoritmo: el algoritmo fija las acciones exactas; el patrón describe la solución a más alto nivel, y su implementación varía.
- Una descripción formal de patrón incluye propósito, motivación, estructura de clases y ejemplo de código.
- Por nivel, los patrones van desde idioms (un lenguaje) hasta patrones de arquitectura (aplicación completa, cualquier lenguaje).
- Por propósito, se agrupan en creacionales, estructurales y de comportamiento.
- El concepto nace con Christopher Alexander (*El lenguaje de patrones*) y llega a la programación con el libro GoF (1995) y sus 23 patrones.
- Aprender patrones aporta soluciones comprobadas y un lenguaje común de equipo.
