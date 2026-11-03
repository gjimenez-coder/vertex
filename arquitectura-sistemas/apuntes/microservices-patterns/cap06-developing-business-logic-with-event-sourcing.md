# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 6 — Developing business logic with event sourcing (Desarrollo de la lógica de negocio con event sourcing)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo presenta el patrón *event sourcing* como una forma distinta de estructurar la lógica de negocio y persistir los agregados DDD. En lugar de guardar el estado actual de un agregado en tablas, se persiste como una secuencia de eventos de dominio, donde cada evento representa un cambio de estado. La aplicación reconstruye el estado actual de un agregado reproduciendo (fold/replay) sus eventos.

La tesis central es que event sourcing elimina una fuente de errores de programación: garantiza que se publica un evento cada vez que un agregado se crea o actualiza, en lugar de tener la lógica de publicación "pegada" (bolted on) a la lógica de negocio, donde un desarrollador podría olvidar emitir el evento. Esto lo hace una base sólida para una arquitectura de microservicios basada en eventos (sagas coreografiadas, vistas CQRS).

Sales sabiendo cómo funciona event sourcing, cómo refactorizar métodos de comando en pares `process()`/`apply()`, cómo implementar un event store (con el ejemplo de Eventuate Local y el framework Eventuate Client), sus beneficios y desventajas, y cómo integrar event sourcing con sagas coreografiadas y orquestadas.

## El ejemplo que recorre el capítulo

Mary, de la aplicación FTGO, considera usar event sourcing para implementar los eventos de dominio de forma fiable. El agregado `Order` (y también `Customer`/`Account` del ejemplo de tienda online) sirve de hilo conductor: se muestra su versión JPA tradicional frente a su versión event sourcing, y cómo participa en la `CreateOrderSaga` junto con `Kitchen Service`, `Consumer Service` y `Accounting Service`.

## 6.1 Desarrollo de la lógica de negocio usando event sourcing

Problemas de la persistencia tradicional (que mapea clases a tablas, campos a columnas e instancias a filas):

- Desajuste objeto-relacional (*Object-Relational impedance mismatch*): conflicto conceptual entre el esquema relacional tabular y el grafo del modelo de dominio. Richardson cita a Ted Neward: "Object-Relational mapping is the Vietnam of Computer Science" (PDF p. 215).
- Falta de historia del agregado: solo se guarda el estado actual; el estado previo se pierde.
- El *audit logging* es tedioso y propenso a errores: el código de auditoría y el de negocio pueden divergir.
- La publicación de eventos está "pegada" a la lógica de negocio y puede desincronizarse.

Visión general: event sourcing persiste cada agregado como una secuencia de eventos en un *event store*. Por ejemplo, en vez de una tabla `ORDER`, los pedidos se guardan como filas en una tabla `EVENTS` (`OrderCreated`, `OrderApproved`, `OrderShipped`, etc.). Cargar un agregado consiste en:

1. Cargar los eventos del agregado.
2. Crear una instancia con su constructor por defecto.
3. Iterar los eventos llamando a `apply()`.

Es análogo a una operación *fold* o *reduce*.

Los eventos representan cambios de estado y no son opcionales: todo cambio de estado, incluida la creación, se representa con un evento, y el evento debe contener los datos necesarios para la transición. Un `OrderCreated` debe llevar todos los datos para inicializar el `Order` (líneas de pedido, pago, entrega), no basta con el `orderId`.

Los métodos del agregado giran en torno a eventos. Event sourcing divide un método de comando en dos tipos de métodos:

- `process()`: toma un objeto *command*, valida los argumentos, no cambia el estado y devuelve una lista de eventos (o lanza una excepción).
- `apply()`: toma un evento concreto y actualiza el agregado; no puede fallar, porque el evento representa un cambio que ya ocurrió.

```java
public class Order {
  public List<Event> process(CreateOrderCommand command) {
    // ... validar comando ...
    return events(new OrderCreatedEvent(command.getOrderDetails()));
  }
  public void apply(OrderCreatedEvent event) {
    OrderDetails orderDetails = event.getOrderDetails();
    this.orderLineItems = new OrderLineItems(orderDetails.getLineItems());
    this.orderMinimum = orderDetails.getOrderMinimum();
    this.state = APPROVAL_PENDING;
  }
}
```

Crear un agregado: instanciar con el constructor por defecto, llamar a `process()`, aplicar los eventos con `apply()` y guardarlos en el event store. Actualizar: cargar los eventos, instanciar, aplicar los eventos cargados, llamar a `process()`, aplicar los nuevos eventos y guardarlos.

Concurrencia (6.1.3): se usa bloqueo optimista con una columna de versión. El event store puede usar el número de eventos como versión o mantener un número de versión explícito.

Publicación de eventos (6.1.4): event sourcing también sirve como mecanismo fiable de publicación. Se publican los eventos de la tabla `EVENTS` mediante *polling* o *transaction log tailing* (ambos de capítulo 3). El polling simple puede saltarse eventos si las transacciones hacen commit en distinto orden al de generación; se soluciona con una columna `PUBLISHED`. El transaction log tailing (usado por Eventuate Local) es más escalable y garantiza la publicación.

Snapshots (6.1.5): para agregados longevos con muchos eventos (p. ej. `Account`), se persiste periódicamente un *snapshot* del estado y solo se cargan el snapshot más reciente y los eventos posteriores. Agregados simples pueden serializarse a JSON; los complejos usan el patrón *Memento*.

Procesamiento idempotente (6.1.6): un consumidor es idempotente si puede invocarse varias veces con el mismo mensaje sin efectos erróneos. Con RDBMS se registra el ID del mensaje en una tabla `PROCESSED_MESSAGES` dentro de la transacción. Con NoSQL, el consumidor guarda el ID del mensaje en los eventos generados y detecta duplicados buscándolo. Si procesar un mensaje no genera eventos, se guarda un *pseudo evento* para registrar el ID.

Evolución de eventos (6.1.7): como los eventos se guardan para siempre, su esquema cambia en tres niveles (esquema de agregados, eventos por agregado, estructura del evento). Algunos cambios son retrocompatibles (añadir campo); otros no (renombrar evento o campo). La solución recomendada es el *upcasting*: un componente llamado *upcaster* actualiza cada evento de una versión antigua a una nueva al cargarlo del event store, de modo que el código de la aplicación solo trata el esquema actual.

Beneficios (6.1.8): publica eventos de dominio de forma fiable; preserva la historia del agregado (consultas temporales); evita en gran medida el desajuste O/R; ofrece a los desarrolladores una "máquina del tiempo" para implementar requisitos no anticipados sobre datos históricos.

Desventajas (6.1.9): modelo de programación distinto con curva de aprendizaje; complejidad de una aplicación basada en mensajería; evolución de eventos complicada; borrado de datos difícil (se usa *soft delete*; para cumplir el GDPR y el derecho al olvido se recurre a cifrado por usuario o a *pseudonymization* con tokens UUID); consultar el event store es difícil y a menudo exige el patrón CQRS (capítulo 7).

## 6.2 Implementación de un event store

Un event store es un híbrido de base de datos y *message broker*: expone una API para insertar y recuperar eventos de un agregado por clave primaria, y otra para suscribirse a eventos. Opciones de event stores especializados: Event Store (de Greg Young), Lagom (Lightbend), Axon y Eventuate (del autor, con versiones Eventuate SaaS y Eventuate Local).

Eventuate Local (6.2.1) es open source y usa una base de datos (p. ej. MySQL) más un broker (Apache Kafka), conectados por un *event relay* que propaga eventos mediante transaction log tailing. Su esquema tiene tres tablas:

- `events`: guarda los eventos; la columna `triggering_event` almacena el ID del mensaje/evento que generó este evento (para detectar duplicados).
- `entities`: una fila por entidad con `entity_version`, para el bloqueo optimista.
- `snapshots`: guarda los snapshots por entidad y versión.

Operaciones: `find()` (lee snapshot y eventos posteriores, más la versión actual), `create()` (inserta en `entities` y `events`) y `update()` (inserta eventos y verifica/actualiza `entity_version` con un `UPDATE` condicional dentro de una transacción). Los consumidores se suscriben a un *topic* de Kafka por tipo de agregado; el `entity_id` es la clave de partición, lo que preserva el orden de los eventos de un agregado. El event relay lee el binlog de MySQL (como si fuera un esclavo) y publica las inserciones en `EVENTS` al topic de Kafka correspondiente, guardando su posición en el binlog para reiniciarse.

Framework Eventuate Client para Java (6.2.2): provee clases base para agregados, comandos y eventos, una clase `AggregateRepository` con CRUD, y una API para suscribirse a eventos.

- `ReflectiveMutableCommandProcessingAggregate`: clase base de agregados; usa reflexión para despachar comandos a `process()` y eventos a `apply()`.
- Comandos extienden una interfaz base del agregado que extiende `Command`; eventos extienden la interfaz marcadora `Event`.
- `AggregateRepository` ofrece `save()` (crear), `find()` (buscar) y `update()` (actualizar), encapsulando el boilerplate de instanciar, procesar, aplicar y guardar eventos.
- Suscripción con `@EventSubscriber` (ID de la suscripción durable) y `@EventHandlerMethod`; el handler recibe un `EventHandlerContext`.

## 6.3 Uso conjunto de sagas y event sourcing

Event sourcing facilita las *sagas coreografiadas* (6.3.1): los participantes intercambian los eventos de dominio de sus agregados y el framework hace cada handler idempotente automáticamente. El inconveniente específico es que los eventos pasan a tener doble propósito (estado + coreografía): un agregado debe emitir un evento incluso cuando no hay cambio de estado (p. ej. para reportar un error de regla de negocio), y no hay agregado que emita un evento de error cuando no puede crearse. Por eso las sagas complejas conviene implementarlas con orquestación.

Crear una saga orquestada (6.3.2): el servicio debe crear/actualizar un agregado y crear el orquestador de forma atómica. Con un event store RDBMS (Eventuate Local), ambas acciones caben en la misma transacción ACID junto con el framework Eventuate Tram. Con un event store NoSQL no es posible la atomicidad: se usa un *event handler* que crea el orquestador en respuesta al evento de dominio (p. ej. `OrderCreated`). Para evitar crear varias sagas ante eventos duplicados, se deriva el ID de la saga de un atributo único (ID del agregado o ID del evento).

Participante basado en event sourcing (6.3.3): debe resolver (1) manejo idempotente de comandos —registrando el ID del mensaje en los eventos generados— y (2) envío atómico de la respuesta. Para lo segundo, en lugar de que el orquestador se suscriba a los eventos del agregado, el participante usa un proceso en dos pasos: al crear/actualizar el agregado guarda un pseudo evento `SagaReplyRequested` junto a los eventos reales, y un handler de ese pseudo evento construye y envía el mensaje de respuesta al canal de respuesta del orquestador. El ejemplo es `Accounting Service` manejando `AuthorizeAccount` con la clase `AccountingServiceCommandHandler` y `AggregateRepository.update()`.

Orquestadores basados en event sourcing (6.3.4): hay que resolver cómo persistir el orquestador, cómo cambiar su estado y enviar comandos de forma atómica, y cómo procesar respuestas exactamente una vez. El orquestador se persiste con eventos `SagaOrchestratorCreated` y `SagaOrchestratorUpdated` (que contienen el estado serializado, p. ej. `CreateOrderSagaState`). Para enviar comandos de forma fiable se persiste un `SagaCommandEvent` por cada comando, y un handler se suscribe a esos eventos y envía el mensaje al canal destino (entrega *at-least-once*). Los duplicados se descartan usando el ID único del `SagaCommandEvent` como ID del mensaje de comando. Las respuestas se procesan una sola vez guardando el ID de la respuesta en los eventos que emite el orquestador.

## Ideas clave

- Event sourcing persiste cada agregado como una secuencia de eventos de dominio; el estado actual se reconstruye reproduciéndolos (fold/replay).
- Resuelve limitaciones de la persistencia tradicional: historia del agregado, auditoría fiable y publicación de eventos garantizada al cambiar el estado.
- Los métodos del agregado se dividen en `process()` (valida y devuelve eventos) y `apply()` (actualiza el estado y no puede fallar).
- Se usan snapshots para no recargar todos los eventos de agregados longevos, y bloqueo optimista por versión para la concurrencia.
- El event store es un híbrido de base de datos y message broker; Eventuate Local combina MySQL y Apache Kafka con un event relay basado en transaction log tailing.
- La evolución del esquema de eventos se gestiona con *upcasting*; el borrado se hace con soft delete, cifrado o pseudonymization para cumplir el GDPR.
- Consultar el event store es difícil y suele requerir CQRS (capítulo 7).
- Event sourcing es una buena base para sagas: inmediato para coreografía y, con pseudo eventos y eventos de comando, también para orquestadores y participantes.
