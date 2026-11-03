# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 4 — Managing transactions with sagas (Gestión de transacciones con sagas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Casi toda petición de una aplicación empresarial se ejecuta dentro de una transacción de base de datos. En un monolito con una sola base de datos esto es sencillo (por ejemplo, con la anotación `@Transactional` de Spring), pero en una arquitectura de microservicios las transacciones abarcan varios servicios, cada uno con su propia base de datos. La operación `createOrder()` del ejemplo FTGO lee datos de Consumer Service y actualiza Order Service, Kitchen Service y Accounting Service, de modo que se necesita un mecanismo que mantenga la consistencia entre bases de datos.

El enfoque tradicional —transacciones distribuidas basadas en el estándar X/Open DTP (XA) con two-phase commit (2PC)— no es viable para aplicaciones modernas. Muchas tecnologías actuales no lo soportan (NoSQL como MongoDB y Cassandra; brokers como RabbitMQ y Apache Kafka), es una forma de IPC síncrona que reduce la disponibilidad (la disponibilidad global es el producto de la de cada participante) y choca con el teorema CAP: hoy los arquitectos prefieren sistemas disponibles frente a consistentes.

La alternativa es la saga: una secuencia de transacciones locales, coordinadas por mensajería asíncrona, donde cada transacción local actualiza los datos de un único servicio con las herramientas ACID habituales. La tesis central es que una saga es ACD (Atomicity, Consistency, Durability): le falta la propiedad de aislamiento (Isolation) de ACID. Sales sabiendo cómo se coordina una saga (coreografía y orquestación), cómo se revierte mediante transacciones de compensación, y cómo lidiar con la falta de aislamiento usando contramedidas.

## El ejemplo que recorre el capítulo

El hilo conductor es la **Create Order Saga**, con la que Order Service implementa `createOrder()`. Consta de seis transacciones locales:

1. Order Service — crear un `Order` en estado `APPROVAL_PENDING`.
2. Consumer Service — verificar que el consumidor puede hacer el pedido.
3. Kitchen Service — validar el pedido y crear un `Ticket` en estado `CREATE_PENDING`.
4. Accounting Service — autorizar la tarjeta de crédito del consumidor.
5. Kitchen Service — cambiar el `Ticket` a `AWAITING_ACCEPTANCE`.
6. Order Service — cambiar el `Order` a `APPROVED`.

La operación externa inicia el primer paso; cada transacción local, al completarse, dispara la siguiente mediante mensajería asíncrona. La mensajería garantiza que la saga se complete aunque un participante esté temporalmente no disponible, porque el broker almacena el mensaje hasta poder entregarlo.

## 4.1 Gestión de transacciones en microservicios

El patrón Saga mantiene la consistencia de datos sin transacciones distribuidas. Se define una saga por cada comando del sistema que actualice datos en varios servicios.

Como cada paso confirma sus cambios en su base de datos local, una saga no puede revertirse automáticamente: debe usar **transacciones de compensación**. Si falla la transacción (n+1), hay que deshacer los efectos de las n anteriores ejecutando cada compensación Cᵢ en orden inverso: la secuencia es T₁ … Tₙ, Cₙ … C₁.

No todos los pasos necesitan compensación. En la Create Order Saga:

| Paso | Servicio | Transacción | Compensación |
|------|----------|-------------|--------------|
| 1 | Order Service | createOrder() | rejectOrder() |
| 2 | Consumer Service | verifyConsumerDetails() | — |
| 3 | Kitchen Service | createTicket() | rejectTicket() |
| 4 | Accounting Service | authorizeCreditCard() | — |
| 5 | Kitchen Service | approveTicket() | — |
| 6 | Order Service | approveOrder() | — |

Los pasos de solo lectura (como `verifyConsumerDetails()`) y los seguidos por pasos que siempre tienen éxito (como `authorizeCreditCard()`) no necesitan compensación.

## 4.2 Coordinación de sagas

Hay dos formas de estructurar la lógica de coordinación.

### Sagas basadas en coreografía

No hay coordinador central: los participantes se suscriben a los eventos de los demás y reaccionan. En la Create Order Saga, cada participante actualiza su base de datos y publica un evento (`OrderCreated`, `ConsumerVerified`, `TicketCreated`, `CreditCardAuthorized`…) que dispara al siguiente. La saga también maneja el camino de fallo: si Accounting Service no autoriza la tarjeta, publica un evento de fallo que lleva a Kitchen Service a rechazar el `Ticket` y a Order Service a rechazar el `Order`.

Dos cuestiones de comunicación a resolver:

- **Comunicación fiable basada en eventos**: cada paso debe actualizar la base de datos y publicar el evento de forma atómica, usando *transactional messaging* (capítulo 3).
- **Correlación**: cada participante debe poder mapear el evento recibido a sus propios datos mediante un *correlation id* (por ejemplo, el `orderId` que se propaga entre participantes).

Beneficios: simplicidad y bajo acoplamiento. Inconvenientes: más difícil de entender (la saga queda dispersa, sin un único lugar en el código), dependencias cíclicas entre servicios (considerado un *design smell*) y riesgo de acoplamiento fuerte. La coreografía sirve para sagas simples.

### Sagas basadas en orquestación

Se define una clase orquestadora cuya única responsabilidad es decir a los participantes qué hacer, mediante interacción comando/respuesta asíncrona. El orquestador envía un mensaje de comando, el participante responde y el orquestador decide el siguiente paso. La Create Order Saga la orquesta la clase `CreateOrderSaga`.

Un buen modelo para un orquestador es una **máquina de estados**: un conjunto de estados y transiciones disparadas por eventos; cada transición puede tener una acción (invocar a un participante). Estados de la Create Order Saga: `Verifying Consumer` (inicial), `Creating Ticket`, `Authorizing Card`, `Order Approved` (final) y `Order Rejected` (final). Modelarla así facilita diseñar, implementar y probar la saga. También aquí cada paso debe usar transactional messaging.

Beneficios: dependencias más simples (sin ciclos: el orquestador depende de los participantes, no al revés), menor acoplamiento y mejor separación de responsabilidades (los objetos de dominio ignoran las sagas; el `Order` pasa directamente de `APPROVAL_PENDING` a `APPROVED`). Inconveniente: el riesgo de centralizar demasiada lógica de negocio en el orquestador; se evita manteniéndolo responsable solo de la secuenciación. Recomendación del libro: usar orquestación para todas las sagas salvo las más simples.

## 4.3 Cómo manejar la falta de aislamiento

La propiedad de aislamiento de ACID garantiza que ejecutar transacciones concurrentes dé el mismo resultado que algún orden serial. Las sagas carecen de esa propiedad: los cambios de cada transacción local son visibles para otras sagas en cuanto se confirman. Esto permite que otras sagas modifiquen datos en uso o lean datos inconsistentes. Por eso la saga es ACD (Atomicity, Consistency, Durability). La falta de aislamiento puede causar *anomalies*. En la práctica es común aceptar menor aislamiento a cambio de rendimiento (los RDBMS suelen usar por defecto un nivel más débil que *serializable*).

**Anomalías** (tres posibles; las dos primeras son las más frecuentes y difíciles):

- **Lost updates**: una saga sobrescribe la actualización de otra sin leerla. Ejemplo: la Create Order Saga aprueba un `Order` que la Cancel Order Saga ya había cancelado.
- **Dirty reads**: una saga lee datos que otra está actualizando a medias. Ejemplo con límite de crédito: el crédito disponible se lee en un punto intermedio y se permite un pedido que excede el límite.
- **Fuzzy/nonrepeatable reads**: dos pasos de una saga leen el mismo dato y obtienen resultados distintos porque otra saga lo modificó.

**Estructura de una saga** (modelo del paper de Lars Frank y Torben U. Zahle, 1998):

- **Transacciones compensables**: pueden revertirse con una compensación (en el ejemplo, pasos 1 a 3).
- **Transacción pivote**: el punto go/no-go; si se confirma, la saga llega hasta el final (el paso 4, `authorizeCreditCard()`).
- **Transacciones reintetables (retriable)**: siguen al pivote y están garantizadas para completarse (pasos 5 y 6).

**Contramedidas** descritas en ese paper:

- **Semantic lock**: bloqueo a nivel de aplicación. Una transacción compensable marca un flag en el registro (como los estados `*_PENDING` del `Order`), que una transacción reintetable o de compensación limpia. Hay que decidir caso a caso cómo reaccionar ante un registro bloqueado (fallar y pedir reintento, o bloquear hasta liberar). Recrea el aislamiento de ACID pero obliga a gestionar bloqueos y detectar interbloqueos (*deadlocks*).
- **Commutative updates**: diseñar las operaciones para ejecutarse en cualquier orden (p. ej. `debit()`/`credit()`); elimina los lost updates.
- **Pessimistic view**: reordenar los pasos de la saga para minimizar el riesgo de negocio ante un dirty read (p. ej. aumentar el crédito disponible en una transacción reintetable al final).
- **Reread value**: releer el registro antes de actualizarlo y verificar que no cambió; si cambió, aborta/reinicia. Es una forma del patrón Optimistic Offline Lock; previene lost updates.
- **Version file**: registrar las operaciones sobre un registro para reordenarlas; convierte operaciones no conmutativas en conmutativas.
- **By value**: elegir dinámicamente el mecanismo de concurrencia según el riesgo de negocio: sagas para peticiones de bajo riesgo, transacciones distribuidas para las de alto riesgo (p. ej. grandes importes).

## 4.4 Diseño de Order Service y la Create Order Saga

Order Service es a la vez orquestador y participante de sagas. Su lógica de negocio tradicional la forman `OrderService`, la entidad `Order` y `OrderRepository`; a ello se suman los orquestadores (como `CreateOrderSaga`) y el adaptador `OrderCommandHandlers` que atiende los comandos que la propia saga envía a Order Service. Todo se implementa con el framework **Eventuate Tram Saga**, que ofrece un DSL para definir la máquina de estados, la ejecuta e intercambia mensajes usando Eventuate Tram.

- **`OrderService`**: su método `createOrder()` crea el `Order` con `Order.createOrder()`, lo persiste con `OrderRepository`, publica eventos de dominio y crea la saga con `SagaManager.create()`, pasando un `CreateOrderSagaState` con el `orderId` y los `OrderDetails`.
- **`CreateOrderSaga`**: clase singleton que implementa `SimpleSaga` y define la máquina de estados mediante el DSL (`step()`, `invokeParticipant()`, `onReply()`, `withCompensation()`). Por ejemplo, el tercer paso invoca a Kitchen Service para crear el `Ticket` y define como compensación la cancelación de ese `Ticket`.
- **`CreateOrderSagaState`**: estado persistente de la instancia de saga; su responsabilidad principal es crear los mensajes de comando enviados a los participantes.
- **Clases proxy de participante** (p. ej. `KitchenServiceProxy`): definen la API de mensajería de cada participante (tipo de comando, canal destino y tipos de respuesta). No son estrictamente necesarias, pero aportan endpoints tipados estáticamente y una API clara que facilita entender y probar el código.
- **`SagaManager`** (de Eventuate Tram Saga): crea y gestiona instancias de saga, las persiste, envía los mensajes de comando, se suscribe a las respuestas e invoca la saga para procesarlas. Si un participante falla, ejecuta las compensaciones en orden inverso.
- **`OrderCommandHandlers`**: enruta (vía `SagaCommandDispatcher`) los comandos que las sagas envían a Order Service (`approveOrder`, `rejectOrder`), invoca a `OrderService` y devuelve el mensaje de respuesta.
- **`OrderServiceConfiguration`**: clase `@Configuration` de Spring que instancia y cablea los `@Bean` (`orderService`, `createOrderSagaManager`, `createOrderSaga`, `orderCommandHandlers`, los proxies, etc.).

`CreateOrderSaga` es solo una de las muchas sagas de Order Service (también `cancelOrder()` usa una Cancel Order Saga y `reviseOrder()` una Revise Order Saga), por lo que gran parte de la comunicación entre servicios es mensajería asíncrona aunque la API externa sea síncrona (REST o gRPC).

## Ideas clave

- Las transacciones distribuidas XA/2PC no encajan en microservicios: muchas tecnologías no las soportan, reducen la disponibilidad y chocan con el teorema CAP.
- Una saga es una secuencia de transacciones locales coordinadas por mensajería; cada una actualiza un solo servicio y confirma sus cambios.
- Al no poder revertirse automáticamente, una saga deshace sus cambios con transacciones de compensación ejecutadas en orden inverso (Cₙ … C₁); no todos los pasos las necesitan.
- Coreografía: sin coordinador, los participantes intercambian eventos; simple y poco acoplada, pero difícil de entender y con dependencias cíclicas. Buena para sagas simples.
- Orquestación: un orquestador central (modelado como máquina de estados) envía comandos; evita ciclos y mejora la separación de responsabilidades. Recomendada para todo salvo lo más simple.
- Las sagas son ACD: carecen de aislamiento, lo que provoca anomalías como lost updates, dirty reads y fuzzy/nonrepeatable reads.
- Una saga se estructura en transacciones compensables, una transacción pivote (go/no-go) y transacciones reintetables garantizadas.
- Las contramedidas (semantic lock, commutative updates, pessimistic view, reread value, version file, by value) previenen o reducen el impacto de la falta de aislamiento.
- En el ejemplo, Order Service es orquestador y participante, y se implementa con el framework Eventuate Tram Saga y un DSL de máquina de estados.
