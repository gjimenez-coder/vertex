# Abstract Factory (Fábrica abstracta) — Estudio

## Tarjetas de repaso

P: ¿Qué tipo de patrón es Abstract Factory y qué permite?
R: Es un patrón creacional que permite producir familias de objetos relacionados sin especificar sus clases concretas.

P: ¿Contra qué trabaja el código cliente en lugar de instanciar productos directamente?
R: Trabaja contra interfaces abstractas y delega la creación a un objeto de fábrica.

P: ¿Qué son los Productos Abstractos?
R: Interfaces que declaran un grupo de productos distintos pero relacionados que forman una familia (Silla, Sofá, Mesilla).

P: ¿Qué son los Productos Concretos?
R: Implementaciones agrupadas por variantes; cada producto abstracto se implementa en todas las variantes (p. ej. victoriano/moderno).

P: ¿Qué declara la interfaz Fábrica Abstracta?
R: Un grupo de métodos para crear cada producto abstracto (crearSilla, crearSofá, crearMesilla).

P: ¿Qué hace cada Fábrica Concreta?
R: Implementa los métodos de creación de una variante específica y crea solo esas variantes (p. ej. FábricaDeMueblesModernos crea SillaModerna, SofáModerno y MesillaModerna).

P: ¿Por qué el cliente no se acopla a la variante concreta?
R: Porque las firmas de los métodos de las fábricas concretas devuelven productos abstractos, así el cliente se comunica solo mediante interfaces.

P: ¿Qué garantiza usar una fábrica concreta por variante?
R: Que los productos obtenidos de una misma fábrica combinen entre sí.

P: ¿Cuándo y según qué se elige normalmente la fábrica concreta?
R: En la etapa de inicialización, seleccionando el tipo según la configuración o los ajustes del entorno.

P: ¿Cuál es el principal contra del patrón?
R: El código puede complicarse por las muchas interfaces y clases que introduce el patrón.

P: ¿Qué diferencia a Builder de Abstract Factory?
R: Builder construye objetos complejos paso a paso; Abstract Factory crea familias de objetos relacionados y devuelve el producto de inmediato.

P: ¿Qué dos principios de diseño favorece Abstract Factory?
R: Responsabilidad única (el código de creación queda en un solo lugar) y abierto/cerrado (nuevas variantes sin descomponer el cliente).

## Preguntas de autoevaluación

P: ¿Qué dos necesidades simultáneas plantea el problema que resuelve el patrón?
R: Crear objetos individuales que combinen con otros de la misma familia y no tener que modificar el código existente al añadir nuevos productos o familias. (Sección "Problema")

P: En el ejemplo de los muebles, ¿qué familia de productos y qué variantes se manejan?
R: La familia Silla + Sofá + Mesilla, con variantes Moderna, Victoriana y Art Decó. (Sección "El ejemplo que recorre el capítulo")

P: En el pseudocódigo de UI, ¿cómo se decide qué fábrica concreta se instancia?
R: El ApplicationConfigurator lee la configuración y, según config.OS, crea WinFactory o MacFactory en tiempo de ejecución; si es desconocido lanza una excepción. (Sección "Pseudocódigo")

P: ¿Qué hay que hacer para añadir una nueva variedad de elementos sin modificar el cliente?
R: Basta crear una nueva clase de fábrica y ajustar ligeramente el código de inicialización. (Sección "Pseudocódigo")

P: ¿En qué dos situaciones recomienda el capítulo aplicar el patrón?
R: Cuando el código deba funcionar con varias familias de productos relacionados sin depender de sus clases concretas, y cuando una clase tenga métodos de fábrica que nublen su responsabilidad principal. (Sección "Aplicabilidad")

P: ¿Con qué patrón suelen empezar muchos diseños antes de evolucionar hacia Abstract Factory?
R: Con Factory Method, evolucionando luego hacia Abstract Factory, Prototype o Builder. (Sección "Relaciones con otros patrones")

P: ¿Cómo sabe el cliente usar una silla sin conocer su clase concreta?
R: La trata mediante la interfaz Silla y solo sabe que implementa, por ejemplo, el método sentarse. (Sección "Solución")

## Checklist

Pasos para implementar el patrón (de "Cómo implementarlo"):

- [ ] Mapear una matriz de tipos de productos frente a sus variantes.
- [ ] Declarar interfaces abstractas para todos los tipos de producto y hacer que las clases concretas las implementen.
- [ ] Declarar la interfaz de la fábrica abstracta con métodos de creación para todos los productos abstractos.
- [ ] Implementar una clase concreta de fábrica por cada variante de producto.
- [ ] Crear código de inicialización que instancie una fábrica concreta según la configuración o el entorno y pasarla a las clases que construyen productos.
- [ ] Buscar las llamadas directas a constructores de producto y sustituirlas por llamadas al método de creación del objeto de fábrica.
