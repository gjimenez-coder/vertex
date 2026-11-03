# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 5 — Designing business logic in a microservice architecture (Diseño de la lógica de negocio en una arquitectura de microservicios)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

La lógica de negocio es el corazón de una aplicación empresarial. Desarrollarla es difícil, y más aún en una arquitectura de microservicios, donde queda repartida entre varios servicios. El capítulo aborda dos retos propios de ese entorno: un modelo de dominio típico es una maraña de clases interconectadas (problema cuando las clases se reparten entre servicios y aparecen referencias de objeto que cruzarían fronteras de servicio), y el diseño de lógica que respete las restricciones de transacciones del modelo de microservicios (transacciones ACID dentro de un servicio, saga entre servicios).

La tesis central es que el patrón Aggregate de DDD resuelve ambos retos. Un aggregate es un cúmulo de objetos tratado como una unidad; las referencias entre aggregates se hacen por clave primaria (no por referencia de objeto), de modo que ninguna referencia cruza fronteras de servicio, y una transacción solo crea o actualiza un único aggregate, lo que encaja con el modelo transaccional de microservicios y garantiza que cada transacción ACID queda dentro de un servicio.

El capítulo recorre primero las dos formas de organizar la lógica de negocio (Transaction script y Domain model), introduce DDD y el patrón Aggregate con sus reglas, explica el patrón Domain event y por qué conviene que un servicio publique eventos, y termina con dos ejemplos de la aplicación FTGO: Kitchen Service (más simple) y Order Service (más complejo, apoyado fuertemente en sagas).

## El ejemplo que recorre el capítulo

Se usa la aplicación FTGO de reparto de comida. La lógica de negocio del Order Service se presenta con arquitectura hexagonal (PDF p. 178): la lógica en el centro, rodeada de adaptadores inbound (REST API adapter, OrderCommandHandlers) y outbound (Database Adapter, Domain Event Publishing Adapter). La mayor parte de la lógica se implementa como un modelo de dominio orientado a objetos mapeado a la base de datos con JPA.

## Patrones de organización de la lógica de negocio (5.1)

La decisión clave al desarrollar lógica de negocio es si usar un enfoque orientado a objetos o uno procedural. Hay dos patrones principales:

Transaction script (5.1.1): para lógica simple, el enfoque OO puede ser excesivo. Según *Patterns of Enterprise Application Architecture* de Martin Fowler (Addison-Wesley, 2002), se escribe un método (transaction script) por cada petición de la capa de presentación. Las clases con comportamiento están separadas de las que guardan estado: los scripts se ubican en clases de servicio (p. ej. `OrderService`), que acceden a la base de datos mediante DAOs (`OrderDao`), y los objetos de datos (`Order`) son datos puros con poco o ningún comportamiento. Es muy procedural y apenas usa capacidades de OOP; funciona bien para lógica simple, pero no es buena vía para lógica compleja.

Domain model (5.1.2): la simplicidad procedural es seductora, pero si la lógica se vuelve compleja, los transaction scripts crecen y se vuelven inmantenibles. Salvo aplicaciones muy simples, conviene aplicar el patrón Domain model: la lógica es un modelo de objetos, una red de clases pequeñas que corresponden a conceptos del dominio; muchas tienen estado y comportamiento (sello de una clase bien diseñada). El `OrderService` sigue teniendo un método por operación, pero esos métodos suelen ser simples porque delegan en objetos de dominio persistentes que contienen el grueso de la lógica. Ventajas: diseño más fácil de entender y mantener, más fácil de probar (cada clase se prueba por separado) y más fácil de extender con patrones como Strategy y Template method.

Sobre DDD (5.1.3): descrito en *Domain-Driven Design* de Eric Evans (Addison-Wesley, 2003), es un refinamiento de OOD para lógica compleja. Con DDD cada servicio tiene su propio modelo de dominio, evitando un modelo único para toda la aplicación. Subdomain y Bounded Context son dos patrones estratégicos. Entre los patrones tácticos (bloques de construcción) ampliamente adoptados están: Entity (objeto con identidad persistente; en JPA suelen ser `@Entity`), Value object (colección de valores intercambiables si coinciden, p. ej. `Money`), Factory (crea objetos cuando la lógica es demasiado compleja para un constructor), Repository (acceso a entidades persistentes, encapsula la base de datos) y Service (lógica que no pertenece a una entidad ni a un value object). Un bloque generalmente ignorado salvo por los puristas es el aggregate, que resulta muy útil en microservicios.

## Diseño del modelo de dominio con el patrón Aggregate (5.2)

El problema de las fronteras difusas (5.2.1): un modelo de dominio tradicional es una red de clases interconectadas que no especifica las fronteras de cada objeto de negocio. Esto causa problemas al hacer cumplir las invariantes (reglas de negocio que deben respetarse siempre, p. ej. el importe mínimo de un pedido). Ejemplo: Sam y Mary editan a la vez el mismo Order; cada uno reduce una línea y verifica el mínimo por separado, pero el resultado combinado viola el mínimo. Actualizar directamente parte de un objeto de negocio puede violar las reglas de negocio.

Fronteras explícitas (5.2.2): un aggregate es un cúmulo de objetos de dominio dentro de una frontera, tratado como unidad. Consta de una entidad raíz y, posiblemente, otras entidades y value objects. En FTGO, Order, Consumer y Restaurant son aggregates. El Order aggregate incluye la entidad Order, uno o más value objects `OrderLineItem` y value objects como `Address` (entrega) y `PaymentInformation`. Los aggregates descomponen el modelo en trozos más comprensibles y aclaran el alcance de operaciones como load, update y delete, que actúan sobre todo el aggregate. Son fronteras de consistencia: las actualizaciones se invocan sobre la raíz, que hace cumplir las invariantes, y la concurrencia se gestiona bloqueando la raíz (número de versión o bloqueo de base de datos). Lo clave es identificar los aggregates, sus fronteras y sus raíces; la estructura interna es secundaria.

## Reglas de los aggregates (5.2.3)

- Regla 1 — Referenciar solo la raíz del aggregate: la entidad raíz es la única parte que pueden referenciar clases externas al aggregate. Un cliente solo actualiza el aggregate invocando un método en la raíz, lo que garantiza que se hagan cumplir las invariantes.
- Regla 2 — Las referencias entre aggregates usan claves primarias: los aggregates se referencian por identidad (p. ej. clave primaria), no por referencia de objeto. Un Order referencia su Consumer con `consumerId` y su Restaurant con `restaurantId`. Beneficios: aggregates débilmente acoplados, fronteras bien definidas, sin referencias de objeto que crucen servicios, persistencia más simple (fácil en NoSQL como MongoDB), sin lazy loading transparente y sharding más sencillo.
- Regla 3 — Una transacción crea o actualiza un solo aggregate: encaja perfectamente con microservicios y con el modelo transaccional limitado de la mayoría de bases NoSQL, asegurando que la transacción quede dentro de un servicio. Para operaciones que afectan a varios aggregates se usan sagas (capítulo 4): cada paso de la saga crea o actualiza exactamente un aggregate. (Con un RDBMS de modelo transaccional rico se podrían actualizar varios aggregates en una transacción dentro del mismo servicio, pero no con NoSQL simple.)

Granularidad del aggregate (5.2.4): decisión clave sobre su tamaño. Aggregates pequeños mejoran escalabilidad (al serializar las actualizaciones por aggregate, los más finos permiten más peticiones simultáneas) y reducen conflictos entre usuarios. Pero como el aggregate es el alcance de la transacción, a veces se necesita uno mayor para hacer atómica cierta actualización. Si Order fuera parte del aggregate Consumer, se podrían actualizar atómicamente un Consumer y sus Orders, pero se reduciría la escalabilidad (se serializan actualizaciones de pedidos distintos del mismo cliente) y se dificultaría la descomposición (la lógica de Orders y Consumers quedaría colocada en el mismo servicio). Por ello, conviene hacer los aggregates lo más finos posible.

Diseñar lógica con aggregates (5.2.5): en un (micro)servicio típico, el grueso de la lógica son los aggregates; el resto reside en los domain services y las sagas. Las sagas orquestan secuencias de transacciones locales para garantizar la consistencia de datos. Los services son los puntos de entrada a la lógica y son invocados por adaptadores inbound; usan un repository (implementado por un adaptador outbound) para cargar y guardar aggregates. En el Order Service, la lógica consta del aggregate Order, la clase `OrderService`, `OrderRepository` y una o más sagas: para peticiones locales el servicio actualiza el aggregate Order; si la actualización abarca varios servicios, `OrderService` crea además una saga.

## Publicación de domain events (5.3)

En DDD, un domain event es algo que ha ocurrido a un aggregate; se representa con una clase del modelo de dominio y normalmente refleja un cambio de estado (Order Created, Order Cancelled, Order Shipped). Un aggregate publica uno de estos eventos cada vez que sufre una transición de estado, si hay consumidores interesados.

Por qué publicar eventos de cambio (5.3.1): otras partes —usuarios, otras aplicaciones o componentes— suelen interesarse por los cambios de estado. Escenarios: mantener consistencia entre servicios con sagas basadas en coreografía (cap. 4); notificar a un servicio que mantiene una réplica de que el origen cambió (CQRS, cap. 7); notificar a otra aplicación vía webhook o message broker para disparar el siguiente paso de un proceso de negocio; notificar a otro componente (p. ej. enviar un mensaje WebSocket al navegador o actualizar ElasticSearch); enviar notificaciones (SMS o email) a usuarios; monitorizar eventos para verificar el comportamiento correcto; y analizar eventos para modelar el comportamiento del usuario. El disparador en todos los casos es el cambio de estado de un aggregate en la base de datos.

Qué es un domain event (5.3.2): una clase con nombre en participio pasado y propiedades (primitivas o value objects) que transmiten el evento, p. ej. `OrderCreated` con `orderId`. Suele llevar metadatos (ID de evento, timestamp, identidad del usuario para auditoría), que pueden ir en el propio evento (quizá en una superclase) o en un objeto envoltorio. El ID del aggregate emisor puede formar parte del envoltorio.

```java
interface DomainEvent {}
interface OrderDomainEvent extends DomainEvent {}
class OrderCreated implements OrderDomainEvent {}
class DomainEventEnvelope<T extends DomainEvent> {
  private String aggregateType;
  private Object aggregateId;
  private T event;
}
```

Enriquecimiento de eventos (5.3.3): un consumidor puede necesitar los detalles del pedido. En lugar de consultarlos al servicio (con el coste de una petición), el event enrichment incluye en el evento la información que los consumidores necesitan (líneas, datos de entrega y pago, restaurante). Simplifica a los consumidores, pero hace las clases de evento menos estables (pueden cambiar cuando cambian los requisitos de los consumidores), lo que reduce la mantenibilidad; aun así, a menudo es evidente qué propiedades incluir.

Identificar domain events (5.3.4): a menudo los requisitos describen escenarios de notificación con lenguaje del tipo "Cuando ocurre X haz Y" (p. ej. "Cuando se realiza un Order envía un email al consumidor"). Otra técnica cada vez más popular es el event storming, un taller centrado en eventos para entender un dominio complejo, con expertos del dominio y notas adhesivas sobre una superficie grande. Consta de tres pasos: (1) hacer brainstorming de eventos (notas naranjas en una línea temporal); (2) identificar el disparador de cada evento (acción de usuario = comando, nota azul; sistema externo, nota morada; otro domain event; o paso del tiempo); (3) identificar los aggregates que consumen cada comando y emiten el evento (notas amarillas). El resultado es un modelo de dominio centrado en eventos, buen primer paso.

Generar y publicar eventos (5.3.5): comunicarse con domain events es mensajería asíncrona (cap. 3). Conceptualmente los publica el aggregate, pero este no puede usar inyección de dependencias, así que conviene repartir la responsabilidad entre el aggregate y el service. El aggregate genera los eventos cuando cambia su estado y los devuelve al service, que (con la API de mensajería inyectada) los publica. Dos opciones: (a) que el método del aggregate devuelva la lista de eventos (preferida por el autor), o (b) que la raíz acumule eventos en un campo (p. ej. extendiendo `AbstractAggregateRoot` con `registerDomainEvent()`), que el service recupera con `getDomainEvents()`; Spring Data (release Ingalls) hace esto automáticamente, pero obliga a extender una superclase y complica que clases que no sean la raíz registren eventos.

```java
public class Ticket {
  public List<DomainEvent> accept(ZonedDateTime readyBy) {
    this.acceptTime = ZonedDateTime.now();
    this.readyBy = readyBy;
    return singletonList(new TicketAcceptedEvent(readyBy));
  }
}
```

Publicación fiable: un service debe usar mensajería transaccional para publicar los eventos como parte de la misma transacción que actualiza el aggregate. El framework Eventuate Tram (cap. 3) inserta los eventos en una tabla `OUTBOX` dentro de la transacción ACID y, tras el commit, los publica al message broker. Tram ofrece la interfaz `DomainEventPublisher` con métodos `publish()` sobrecargados (tipo e ID del aggregate más la lista de eventos). Para garantizar que un servicio solo publique eventos válidos, conviene implementar una subclase de `AbstractAggregateDomainEventPublisher` (clase genérica con tipo del aggregate y tipo del marcador de eventos), como `TicketDomainEventPublisher`, que solo publica eventos que son subclase de `TicketDomainEvent`.

Consumir eventos (5.3.6): los eventos se publican como mensajes a un broker (p. ej. Apache Kafka). Es más cómodo usar el `DomainEventDispatcher` de Eventuate Tram, que despacha cada evento al método handler adecuado. Por ejemplo, `KitchenServiceEventConsumer` se suscribe a los eventos de Restaurant Service (como `RestaurantMenuRevised`) para mantener actualizada su réplica de datos.

## Lógica de negocio de Kitchen Service (5.4)

Kitchen Service permite a un restaurante gestionar sus pedidos. Sus dos aggregates principales son Restaurant (conoce el menú y el horario, valida pedidos) y Ticket (representa un pedido que el restaurante debe preparar para que lo recoja un courier). Las otras piezas de la lógica son `KitchenService` (punto de entrada, crea y actualiza los aggregates), `TicketRepository` y `RestaurantRepository`. Tiene tres adaptadores inbound (REST API, `KitchenServiceCommandHandler` invocado por sagas, y `KitchenServiceEventConsumer` suscrito a eventos de Restaurant Service) y dos outbound (DB adapter y `DomainEventPublishingAdapter`).

El aggregate Ticket (5.4.1) representa la vista de un pedido desde la cocina (sin datos del consumidor, entrega ni pago); su ID no lo genera Kitchen Service, sino que usa el suministrado por Order Service. Se persiste con JPA (`@Entity`, tabla `tickets`) y referencia al restaurante por `restaurantId` (un `Long`, no referencia de objeto). Define un factory `create()` y métodos que cambian el estado del pedido: `accept()`, `preparing()` (tras lo cual el pedido ya no puede cambiarse ni cancelarse) y `readyForPickup()`. Los métodos validan la transición de estado y, si no procede, lanzan `UnsupportedStateTransitionException`. `KitchenService` carga el aggregate, invoca el método de la raíz y publica los eventos generados. `KitchenServiceCommandHandler` maneja los mensajes de comando enviados por las sagas de Order Service (p. ej. `CreateTicket`, `ConfirmCreateTicket`, `CancelCreateTicket`) y responde con éxito o fallo.

## Lógica de negocio de Order Service (5.5)

Order Service ofrece una API para crear, actualizar y cancelar pedidos, invocada sobre todo por el consumidor. El aggregate central es Order; también hay un aggregate Restaurant, réplica parcial de datos de Restaurant Service, que permite validar y poner precio a las líneas del pedido. La lógica incluye `OrderService` (entrada principal), `OrderRepository`, `RestaurantRepository` y varias sagas (como `CreateOrderSaga`). Tiene adaptadores inbound (REST API, `OrderEventConsumer`, `OrderCommandHandlers`, `SagaReplyAdapter`) y outbound (DB adapter, `DomainEventPublishingAdapter`, `OutboundCommandMessageAdapter`).

El aggregate Order (5.5.1) se persiste con JPA (tabla `orders`), usa un campo `version` para bloqueo optimista y referencia a Consumer y Restaurant por clave primaria. Contiene value objects embebidos (`OrderLineItems`, `DeliveryInformation`, `PaymentInformation`, `Money` como `orderMinimum`). Su comportamiento se describe como una máquina de estados: para crear o actualizar un pedido, Order Service colabora con otros servicios mediante sagas. `OrderService` o el primer paso de la saga invoca un método que verifica la operación y lleva el Order a un estado pending (un pending state es un contramedida de bloqueo semántico que aísla las sagas, cap. 4); luego la saga actualiza el Order según el resultado. Por ejemplo, `createOrder()` crea el Order en `APPROVAL_PENDING` y la CreateOrderSaga invoca después `noteApproved()` (pasa a `APPROVED`) o `noteRejected()` (pasa a `REJECTED`). Igualmente `revise()` lleva a `REVISION_PENDING` (verificando que no se viole el mínimo) y `confirmRevision()` completa la revisión; `cancel()` lleva a `CANCEL_PENDING` y, si no se puede cancelar, revierte a `APPROVED`.

La clase `OrderService` (5.5.2) es más compleja que `KitchenService` porque la mayoría de sus métodos crean una saga que orquesta la creación o actualización del Order. `createOrder()` crea y persiste el aggregate, publica sus domain events y crea una `CreateOrderSaga`; `reviseOrder()` recupera el Order y crea una `ReviseOrderSaga`. En muchos aspectos la lógica de negocio no difiere de la de un monolito (services, entidades JPA, repositories), pero con diferencias clave: el modelo se organiza como aggregates DDD, las referencias entre aggregates son por clave primaria, una transacción solo crea o actualiza un aggregate, y los aggregates publican domain events al cambiar de estado. Kitchen Service solo participa en sagas, mientras que Order Service las inicia porque sus Orders deben ser consistentes con datos de otros servicios. El capítulo cierra señalando que aquí el código de publicación de eventos está entrelazado con la lógica de negocio; el capítulo 6 verá event sourcing, donde la generación de eventos es parte integral de la lógica.

## Ideas clave

- El patrón procedural Transaction script sirve para lógica simple; para lógica compleja conviene el patrón orientado a objetos Domain model.
- Organizar la lógica de un servicio como una colección de aggregates DDD modulariza el modelo, elimina referencias de objeto entre servicios y garantiza que cada transacción ACID quede dentro de un servicio.
- Un aggregate es un cúmulo de objetos con frontera explícita, formado por una entidad raíz y posibles entidades y value objects; solo se actualiza invocando métodos en la raíz, que hace cumplir las invariantes.
- Reglas: referenciar solo la raíz; las referencias entre aggregates usan claves primarias; una transacción crea o actualiza un solo aggregate (varios aggregates requieren una saga).
- Conviene hacer los aggregates lo más finos posible por escalabilidad y para facilitar la descomposición, salvo cuando se necesite atomicidad mayor.
- Un aggregate debería publicar domain events al crearse o actualizarse; sirven para sagas por coreografía, CQRS, webhooks, notificaciones a usuarios y mensajes WebSocket.
- La publicación fiable de eventos exige mensajería transaccional (p. ej. Eventuate Tram con tabla OUTBOX) para publicarlos dentro de la misma transacción que actualiza el aggregate.
- El event storming es una técnica de taller útil para descubrir rápidamente eventos, comandos y aggregates de un dominio complejo.
