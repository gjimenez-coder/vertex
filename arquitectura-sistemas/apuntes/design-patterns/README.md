# Dive Into Design Patterns — Alexander Shvets (Refactoring.Guru, 2021)

Apuntes del libro de Alexander Shvets. La obra parte del vocabulario y los pilares de la programación orientada a objetos y las relaciones entre objetos, explica qué caracteriza a un buen diseño y presenta los principios de diseño del libro, incluidos los cinco principios SOLID. Sobre esa base desarrolla un catálogo de patrones de diseño agrupados por propósito: creacionales, estructurales y de comportamiento. Cada patrón se expone con su intención, estructura, cuándo aplicarlo, cómo implementarlo y sus relaciones con otros patrones.

## Capítulos

- [Capítulo 1 — Conceptos básicos de POO](cap01-conceptos-basicos-de-poo.md): vocabulario mínimo de la POO: objetos, clases, campos, métodos, estado, comportamiento y jerarquías de herencia.
- [Capítulo 2 — Los pilares de la POO](cap02-los-pilares-de-la-poo.md): los cuatro pilares de la POO: abstracción, encapsulación, herencia y polimorfismo.
- [Capítulo 3 — Relaciones entre objetos](cap03-relaciones-entre-objetos.md): dependencia, asociación, agregación, composición, implementación y herencia ordenadas por acoplamiento.
- [Capítulo 4 — ¿Qué es un patrón de diseño?](cap04-que-es-un-patron-de-diseno.md): el patrón como concepto general, su diferencia con un algoritmo, su clasificación y su origen histórico.
- [Capítulo 5 — Características del buen diseño](cap05-caracteristicas-del-buen-diseno.md): reutilización y extensibilidad como ejes del buen diseño frente al cambio inevitable.
- [Capítulo 6 — Encapsula lo que varía](cap06-encapsula-lo-que-varia.md): aislar los aspectos que varían para minimizar el efecto de los cambios, a nivel de método y de clase.
- [Capítulo 7 — Programa a una interfaz, no a una implementación](cap07-programa-a-una-interfaz-no-a-una-implementacion.md): depender de abstracciones en vez de clases concretas para lograr flexibilidad.
- [Capítulo 8 — Favorece la composición sobre la herencia](cap08-favorece-la-composicion-sobre-la-herencia.md): la composición ("tiene un") frente a la herencia ("es un") para evitar acoplamiento y explosión de clases.
- [Capítulo 9 — S: Principio de responsabilidad única](cap09-s-principio-de-responsabilidad-unica.md): una clase debe tener una sola razón para cambiar, reduciendo la complejidad.
- [Capítulo 10 — O: Principio de abierto/cerrado](cap10-o-principio-de-abierto-cerrado.md): clases abiertas a la extensión y cerradas a la modificación.
- [Capítulo 11 — L: Principio de sustitución de Liskov](cap11-l-principio-de-sustitucion-de-liskov.md): las subclases deben poder sustituir a la superclase sin romper el código cliente, con requisitos formales.
- [Capítulo 12 — I: Principio de segregación de la interfaz](cap12-principio-de-segregacion-de-la-interfaz.md): no forzar a los clientes a depender de métodos que no utilizan.
- [Capítulo 13 — D: Principio de inversión de la dependencia](cap13-d-principio-de-inversion-de-la-dependencia.md): alto y bajo nivel dependen de abstracciones, invirtiendo la dirección de la dependencia.
- [Capítulo 14 — Factory Method](cap14-factory-method.md): interfaz para crear objetos en una superclase, dejando a las subclases alterar el tipo de producto.
- [Capítulo 15 — Abstract Factory](cap15-abstract-factory.md): producir familias de objetos relacionados sin especificar sus clases concretas.
- [Capítulo 16 — Builder](cap16-builder.md): construir objetos complejos paso a paso y producir distintas representaciones con el mismo código.
- [Capítulo 17 — Prototype](cap17-prototype.md): copiar objetos existentes delegando la clonación al propio objeto, sin acoplarse a sus clases.
- [Capítulo 18 — Singleton](cap18-singleton.md): asegurar una única instancia de una clase con un punto de acceso global.
- [Capítulo 19 — Adapter](cap19-adapter.md): hacer colaborar objetos con interfaces incompatibles mediante un traductor intermedio.
- [Capítulo 20 — Bridge](cap20-bridge.md): separar abstracción e implementación en dos jerarquías independientes.
- [Capítulo 21 — Composite](cap21-composite.md): componer objetos en árboles y tratarlos como objetos individuales mediante una interfaz común.
- [Capítulo 22 — Decorator](cap22-decorator.md): añadir funcionalidades envolviendo un objeto en wrappers que comparten su interfaz.
- [Capítulo 23 — Facade](cap23-facade.md): interfaz simplificada a un subsistema complejo, reduciendo el acoplamiento.
- [Capítulo 24 — Flyweight](cap24-flyweight.md): compartir estado común entre muchos objetos para ahorrar memoria.
- [Capítulo 25 — Proxy](cap25-proxy.md): sustituto con la misma interfaz que un servicio para controlar su acceso.
- [Capítulo 26 — Chain of Responsibility](cap26-chain-of-responsibility.md): pasar una solicitud por una cadena de manejadores que deciden procesarla o reenviarla.
- [Capítulo 27 — Command](cap27-command.md): convertir una solicitud en un objeto independiente que desacopla emisor y receptor.
- [Capítulo 28 — Iterator](cap28-iterator.md): recorrer los elementos de una colección sin exponer su representación subyacente.
- [Capítulo 29 — Mediator](cap29-mediator.md): reducir dependencias caóticas forzando la comunicación a través de un mediador.
- [Capítulo 30 — Memento](cap30-memento.md): guardar y restaurar el estado previo de un objeto sin revelar su implementación.
- [Capítulo 31 — Observer](cap31-observer.md): mecanismo de suscripción para notificar a varios objetos de los eventos de otro.
- [Capítulo 32 — State](cap32-state.md): permitir que un objeto altere su comportamiento al cambiar su estado interno.
- [Capítulo 33 — Strategy](cap33-strategy.md): definir una familia de algoritmos intercambiables, cada uno en su propia clase.
- [Capítulo 34 — Template Method](cap34-template-method.md): definir el esqueleto de un algoritmo en la superclase y dejar que las subclases rellenen pasos.
- [Capítulo 35 — Visitor](cap35-visitor.md): separar algoritmos de los objetos sobre los que operan mediante Double Dispatch.
