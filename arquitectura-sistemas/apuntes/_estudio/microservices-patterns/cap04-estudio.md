# Managing transactions with sagas (Gestión de transacciones con sagas) — Estudio

## Tarjetas de repaso

P: ¿Por qué las transacciones distribuidas XA/2PC no encajan en microservicios? / R: Muchas tecnologías actuales no las soportan (NoSQL como MongoDB y Cassandra; brokers como RabbitMQ y Kafka), son IPC síncrona que reduce la disponibilidad (producto de la de cada participante) y chocan con el teorema CAP.

P: ¿Qué es una saga? / R: Una secuencia de transacciones locales coordinadas por mensajería asíncrona, donde cada transacción local actualiza los datos de un único servicio con las herramientas ACID habituales.

P: ¿Por qué se dice que una saga es ACD y no ACID? / R: Porque tiene Atomicity, Consistency y Durability, pero carece de la propiedad de aislamiento (Isolation): los cambios confirmados de cada transacción local son visibles de inmediato para otras sagas.

P: ¿Cómo revierte una saga sus cambios si no puede hacerlo automáticamente? / R: Mediante transacciones de compensación; si falla la transacción (n+1), se deshacen las n anteriores ejecutando cada compensación en orden inverso (T₁…Tₙ, Cₙ…C₁).

P: ¿Todos los pasos de una saga necesitan compensación? / R: No; los pasos de solo lectura (como verifyConsumerDetails()) y los seguidos por pasos que siempre tienen éxito (como authorizeCreditCard()) no necesitan compensación.

P: ¿Qué caracteriza a una saga basada en coreografía? / R: No hay coordinador central; los participantes se suscriben a los eventos de los demás y reaccionan publicando sus propios eventos. Es simple y poco acoplada, pero difícil de entender y con riesgo de dependencias cíclicas.

P: ¿Qué caracteriza a una saga basada en orquestación? / R: Una clase orquestadora dice a los participantes qué hacer mediante comando/respuesta asíncrona y decide el siguiente paso; se modela bien como máquina de estados y evita dependencias cíclicas.

P: ¿Qué recomienda el libro sobre cuándo usar coreografía u orquestación? / R: Coreografía para sagas simples; orquestación para todas las sagas salvo las más simples.

P: ¿Qué dos cuestiones de comunicación hay que resolver en la coreografía? / R: Comunicación fiable basada en eventos (actualizar BD y publicar evento de forma atómica con transactional messaging) y correlación (mapear el evento recibido a los propios datos mediante un correlation id, p. ej. el orderId).

P: ¿Cuáles son las tres anomalías por falta de aislamiento? / R: Lost updates (una saga sobrescribe la actualización de otra sin leerla), dirty reads (leer datos que otra saga actualiza a medias) y fuzzy/nonrepeatable reads (dos lecturas del mismo dato dan resultados distintos).

P: ¿Cómo se estructura una saga según el modelo de Frank y Zahle (1998)? / R: En transacciones compensables (reversibles con compensación), una transacción pivote (punto go/no-go que decide si la saga llega al final) y transacciones reintetables (siguen al pivote y están garantizadas para completarse).

P: ¿Qué es un semantic lock y qué inconveniente tiene? / R: Un bloqueo a nivel de aplicación: una transacción compensable marca un flag (como los estados *_PENDING del Order) que una transacción reintetable o de compensación limpia. Recrea el aislamiento de ACID pero obliga a gestionar bloqueos y detectar deadlocks.

P: ¿Qué contramedidas describe el paper para la falta de aislamiento? / R: Semantic lock, commutative updates, pessimistic view, reread value, version file y by value.

P: ¿Qué framework implementa la Create Order Saga y qué ofrece? / R: Eventuate Tram Saga, que aporta un DSL para definir la máquina de estados, la ejecuta e intercambia mensajes usando Eventuate Tram.

P: ¿Qué rol(es) cumple Order Service respecto a las sagas? / R: Es a la vez orquestador (p. ej. CreateOrderSaga) y participante de sagas, y atiende los comandos que las sagas le envían mediante OrderCommandHandlers.

## Preguntas de autoevaluación

P: ¿Por qué la operación createOrder() del ejemplo FTGO necesita un mecanismo de consistencia entre bases de datos? / R: Porque lee datos de Consumer Service y actualiza Order Service, Kitchen Service y Accounting Service, cada uno con su propia base de datos, de modo que la transacción abarca varios servicios. (Sección: Lo que necesitas saber)

P: Enumera los seis pasos de la Create Order Saga. / R: 1) Order Service crea un Order en APPROVAL_PENDING; 2) Consumer Service verifica al consumidor; 3) Kitchen Service valida y crea un Ticket en CREATE_PENDING; 4) Accounting Service autoriza la tarjeta; 5) Kitchen Service pasa el Ticket a AWAITING_ACCEPTANCE; 6) Order Service pasa el Order a APPROVED. (Sección: El ejemplo que recorre el capítulo)

P: ¿Por qué la orquestación evita las dependencias cíclicas que aparecen en la coreografía? / R: Porque las dependencias son unidireccionales: el orquestador depende de los participantes, pero los participantes no dependen del orquestador, lo que simplifica las dependencias y reduce el acoplamiento. (Sección: 4.2 Coordinación de sagas — Sagas basadas en orquestación)

P: ¿Cuál es el riesgo de la orquestación y cómo se evita? / R: Centralizar demasiada lógica de negocio en el orquestador; se evita manteniéndolo responsable solo de la secuenciación. (Sección: 4.2 Coordinación de sagas — Sagas basadas en orquestación)

P: ¿Por qué la falta de aislamiento es a menudo aceptable en la práctica? / R: Porque es común aceptar menor aislamiento a cambio de rendimiento; de hecho, los RDBMS suelen usar por defecto un nivel más débil que serializable. (Sección: 4.3 Cómo manejar la falta de aislamiento)

P: ¿Cómo previene la contramedida "reread value" un lost update? / R: Relee el registro antes de actualizarlo y verifica que no cambió; si cambió, aborta o reinicia la saga. Es una forma del patrón Optimistic Offline Lock. (Sección: 4.3 Cómo manejar la falta de aislamiento — Contramedidas)

P: ¿Qué hace la contramedida "by value" y cuándo recurre a transacciones distribuidas? / R: Elige dinámicamente el mecanismo de concurrencia según el riesgo de negocio: sagas para peticiones de bajo riesgo y transacciones distribuidas para las de alto riesgo (p. ej. grandes importes). (Sección: 4.3 Cómo manejar la falta de aislamiento — Contramedidas)

P: ¿Cuál es la responsabilidad principal de CreateOrderSagaState y para qué sirven las clases proxy de participante? / R: CreateOrderSagaState mantiene el estado persistente de la instancia y su responsabilidad principal es crear los mensajes de comando enviados a los participantes; las proxy (p. ej. KitchenServiceProxy) definen la API de mensajería de cada participante y aportan endpoints tipados estáticamente. (Sección: 4.4 Diseño de Order Service y la Create Order Saga)

## Puntos a dominar

- Distinguir por qué XA/2PC no es viable en microservicios (soporte tecnológico, disponibilidad, teorema CAP) y qué resuelve la saga en su lugar.
- Explicar la saga como secuencia de transacciones locales coordinadas por mensajería y el porqué de la propiedad ACD (sin Isolation).
- Reconstruir la secuencia de compensación en orden inverso (T₁…Tₙ, Cₙ…C₁) e identificar qué pasos no necesitan compensación y por qué.
- Comparar coreografía y orquestación: beneficios, inconvenientes y la recomendación del libro sobre cuándo usar cada una.
- Identificar las tres anomalías (lost updates, dirty reads, fuzzy/nonrepeatable reads) y relacionarlas con ejemplos del capítulo.
- Clasificar las transacciones de una saga en compensables, pivote y reintetables, situando la transacción pivote como punto go/no-go.
- Asociar cada contramedida (semantic lock, commutative updates, pessimistic view, reread value, version file, by value) con la anomalía que previene o mitiga.
- Describir los componentes de la implementación con Eventuate Tram Saga: OrderService, CreateOrderSaga, CreateOrderSagaState, proxies, SagaManager, OrderCommandHandlers y OrderServiceConfiguration.
