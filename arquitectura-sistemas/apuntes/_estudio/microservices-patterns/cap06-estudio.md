# Developing business logic with event sourcing — Estudio

## Tarjetas de repaso

P: ¿Qué es event sourcing? / R: Un patrón que persiste cada agregado como una secuencia de eventos de dominio, donde cada evento representa un cambio de estado, en lugar de guardar el estado actual en tablas.

P: ¿Cómo se reconstruye el estado actual de un agregado en event sourcing? / R: Cargando sus eventos, creando una instancia con el constructor por defecto e iterando los eventos llamando a `apply()`; es análogo a una operación fold/reduce.

P: ¿Cuál es la tesis central del capítulo sobre event sourcing? / R: Elimina una fuente de errores al garantizar que se publica un evento cada vez que un agregado se crea o actualiza, en vez de tener la publicación "pegada" (bolted on) a la lógica de negocio.

P: ¿Qué problemas de la persistencia tradicional resuelve event sourcing? / R: El desajuste objeto-relacional, la falta de historia del agregado, el audit logging tedioso y propenso a errores, y la publicación de eventos desincronizada.

P: ¿En qué dos tipos de métodos divide event sourcing un método de comando? / R: `process()`, que valida el comando, no cambia el estado y devuelve una lista de eventos (o lanza excepción), y `apply()`, que toma un evento y actualiza el agregado sin poder fallar.

P: ¿Por qué un evento `OrderCreated` no puede contener solo el `orderId`? / R: Porque el evento debe llevar todos los datos necesarios para la transición de estado (líneas de pedido, pago, entrega) e inicializar el agregado.

P: ¿Cómo se gestiona la concurrencia en event sourcing? / R: Con bloqueo optimista mediante una columna de versión; el event store puede usar el número de eventos como versión o un número de versión explícito.

P: ¿Para qué sirven los snapshots? / R: Para agregados longevos con muchos eventos (p. ej. `Account`): se persiste periódicamente el estado y solo se cargan el snapshot más reciente y los eventos posteriores.

P: ¿Qué es el procesamiento idempotente de un consumidor? / R: La capacidad de invocarlo varias veces con el mismo mensaje sin efectos erróneos; con RDBMS se registra el ID del mensaje en `PROCESSED_MESSAGES` y con NoSQL se guarda el ID en los eventos generados.

P: ¿Qué es el upcasting en la evolución de eventos? / R: Un componente (upcaster) que actualiza cada evento de una versión antigua a una nueva al cargarlo del event store, de modo que la aplicación solo trata el esquema actual.

P: ¿Qué es un event store? / R: Un híbrido de base de datos y message broker: expone una API para insertar y recuperar eventos de un agregado por clave primaria y otra para suscribirse a eventos.

P: ¿Cómo está compuesto Eventuate Local? / R: Una base de datos (p. ej. MySQL) más un broker (Apache Kafka) conectados por un event relay que propaga eventos mediante transaction log tailing.

P: ¿Qué tres tablas tiene el esquema de Eventuate Local? / R: `events` (guarda eventos, con `triggering_event` para detectar duplicados), `entities` (una fila por entidad con `entity_version` para bloqueo optimista) y `snapshots`.

P: ¿Qué hace la clase `ReflectiveMutableCommandProcessingAggregate` del framework Eventuate Client? / R: Es la clase base de agregados y usa reflexión para despachar comandos a `process()` y eventos a `apply()`.

P: ¿Por qué las sagas complejas conviene implementarlas con orquestación en lugar de coreografía? / R: Porque en coreografía los eventos tienen doble propósito (estado + coreografía): un agregado debe emitir un evento aun sin cambio de estado y no hay agregado que emita un evento de error cuando no puede crearse.

## Preguntas de autoevaluación

P: ¿Cuáles son los pasos para cargar un agregado desde el event store? / R: Cargar los eventos del agregado, crear una instancia con su constructor por defecto e iterar los eventos llamando a `apply()`. (Sección 6.1)

P: ¿En qué se diferencia crear un agregado de actualizarlo en event sourcing? / R: Crear: instanciar con el constructor por defecto, llamar a `process()`, aplicar los eventos con `apply()` y guardarlos. Actualizar: cargar los eventos, instanciar, aplicar los eventos cargados, llamar a `process()`, aplicar los nuevos eventos y guardarlos. (Sección 6.1)

P: ¿Por qué el polling simple puede saltarse eventos y cómo se soluciona? / R: Porque las transacciones pueden hacer commit en distinto orden al de generación; se soluciona con una columna `PUBLISHED`. El transaction log tailing (usado por Eventuate Local) es más escalable y garantiza la publicación. (Sección 6.1.4)

P: ¿Cuáles son los principales beneficios de event sourcing? / R: Publica eventos de dominio de forma fiable, preserva la historia del agregado (consultas temporales), evita en gran medida el desajuste O/R y da a los desarrolladores una "máquina del tiempo" para requisitos no anticipados. (Sección 6.1.8)

P: ¿Qué desventajas presenta event sourcing? / R: Modelo de programación distinto con curva de aprendizaje, complejidad de una aplicación basada en mensajería, evolución de eventos complicada, borrado de datos difícil (soft delete, cifrado o pseudonymization para GDPR) y consultas difíciles que suelen exigir CQRS. (Sección 6.1.9)

P: ¿Cómo garantiza el framework Eventuate la idempotencia y el envío atómico de respuestas en un participante basado en event sourcing? / R: Registra el ID del mensaje en los eventos generados (idempotencia) y usa un proceso en dos pasos: guarda un pseudo evento `SagaReplyRequested` junto a los eventos reales, y un handler de ese pseudo evento construye y envía el mensaje de respuesta. (Sección 6.3.3)

P: ¿Cómo se persiste y opera un orquestador basado en event sourcing? / R: Se persiste con eventos `SagaOrchestratorCreated` y `SagaOrchestratorUpdated` (estado serializado); para enviar comandos de forma fiable se persiste un `SagaCommandEvent` por comando y un handler lo publica, descartando duplicados con el ID único del evento. (Sección 6.3.4)

P: ¿Cómo se crea una saga orquestada de forma atómica según el tipo de event store? / R: Con un event store RDBMS (Eventuate Local) el agregado y el orquestador caben en la misma transacción ACID; con un event store NoSQL se usa un event handler que crea el orquestador en respuesta al evento de dominio, derivando el ID de la saga de un atributo único. (Sección 6.3.2)

## Puntos a dominar

- Diferenciar la persistencia tradicional (estado actual en tablas) de event sourcing (secuencia de eventos) y sus respectivos problemas y beneficios.
- Saber refactorizar un método de comando en el par `process()` (valida, devuelve eventos) y `apply()` (actualiza el estado, no falla).
- Explicar la reconstrucción del estado por replay/fold de eventos y los flujos de creación y actualización de agregados.
- Dominar los mecanismos de apoyo: bloqueo optimista por versión, snapshots, publicación por polling o transaction log tailing, procesamiento idempotente y upcasting para la evolución de eventos.
- Describir el event store como híbrido de base de datos y message broker, y la arquitectura de Eventuate Local (MySQL + Kafka + event relay) con sus tablas `events`, `entities` y `snapshots`.
- Identificar las clases del framework Eventuate Client (`ReflectiveMutableCommandProcessingAggregate`, `AggregateRepository`, anotaciones `@EventSubscriber`/`@EventHandlerMethod`).
- Relacionar event sourcing con sagas: por qué es inmediato para coreografía y cómo, mediante pseudo eventos y eventos de comando, se usa en participantes y orquestadores.
- Reconocer que consultar el event store es difícil y suele requerir CQRS (capítulo 7), y cómo se afronta el borrado para cumplir el GDPR.
