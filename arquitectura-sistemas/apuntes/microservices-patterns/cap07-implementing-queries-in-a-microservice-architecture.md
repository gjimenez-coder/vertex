# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 7 — Implementing queries in a microservice architecture (Implementación de consultas en una arquitectura de microservicios)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

En una aplicación monolítica las consultas son sencillas: al existir una sola base de datos, basta con escribir sentencias `SELECT` que hacen join de varias tablas y definir los índices necesarios. En una arquitectura de microservicios esto se complica, porque las consultas a menudo necesitan recuperar datos dispersos entre las bases de datos que pertenecen a varios servicios. No se puede usar un mecanismo tradicional de consulta distribuida porque, aun siendo técnicamente posible, violaría la encapsulación.

Algunas consultas recuperan datos de un solo servicio (por ejemplo, `findConsumerProfile()` desde Consumer Service), pero otras como `findOrder()` y `findOrderHistory()` devuelven datos que pertenecen a varios servicios. El capítulo presenta dos patrones para implementar consultas: el patrón **API composition** (el más simple, a usar siempre que sea posible) y el patrón **Command query responsibility segregation (CQRS)** (más potente pero más complejo, que mantiene una o varias bases de datos de vista cuyo único fin es dar soporte a las consultas).

Sales sabiendo cuándo y cómo aplicar cada patrón, cómo diseñar vistas CQRS (elección de base de datos, actualizaciones idempotentes, concurrencia, reconstrucción de vistas y lag de replicación) y cómo implementar una vista CQRS concreta con AWS DynamoDB.

## El ejemplo que recorre el capítulo

El hilo conductor es la aplicación **FTGO** (pedidos de comida a domicilio) y su equipo liderado por Mary, migrando de monolito a microservicios. Tres operaciones de consulta vertebran la explicación: `findOrder()` (recupera un pedido por su clave primaria), `findOrderHistory()` (historial de pedidos de un consumidor, con paginación y filtros) y `findAvailableRestaurants()` (búsqueda geoespacial de restaurantes disponibles).

## 7.1 Consultas con el patrón API composition

La operación `findOrder()` recupera un pedido por su clave primaria y devuelve un objeto `OrderDetails`; la invoca un frontend (móvil o web) que implementa la vista Order Status. En el monolito los datos están en una sola base de datos; en microservicios se reparten entre: Order Service (información y estado básicos del pedido), Kitchen Service (estado del pedido desde la perspectiva del restaurante y hora estimada de recogida), Delivery Service (estado y ubicación de la entrega) y Accounting Service (estado del pago).

El patrón API composition implementa la consulta invocando a los servicios que poseen los datos y combinando los resultados. Tiene dos tipos de participantes:

- **API composer**: implementa la operación de consulta consultando a los servicios proveedores.
- **Provider service**: servicio que posee parte de los datos que devuelve la consulta.

`findOrder()` es un buen candidato para este patrón: es un equi-join simple basado en clave primaria. El Find Order Composer expone un endpoint REST `GET /order/{orderId}`, invoca los cuatro servicios y une las respuestas por `orderId` (Order Service recupera por clave primaria; los demás usan el `orderId` como clave foránea).

### ¿Quién hace de API composer?

Tres opciones:

- **Un cliente** de los servicios (por ejemplo, una aplicación web en la misma LAN). Poco práctico para clientes fuera del firewall con red más lenta.
- **Un API gateway**, cuando la operación es parte de la API externa de la aplicación; permite a un cliente externo recuperar datos de varios servicios con una sola llamada.
- **Un servicio independiente**, para consultas usadas internamente por varios servicios o cuya lógica de agregación es demasiado compleja para el API gateway.

### Modelo de programación reactivo

Para minimizar la latencia, el API composer debe llamar a los servicios proveedores **en paralelo** cuando no hay dependencias entre las llamadas; a veces necesita el resultado de un servicio para invocar a otro, y entonces debe hacer algunas llamadas secuencialmente. Para que sea mantenible y escalable, conviene un diseño reactivo basado en `CompletableFuture` de Java, observables de RxJava u otra abstracción equivalente.

### Beneficios e inconvenientes

Es simple e intuitivo, pero tiene inconvenientes:

- **Mayor sobrecarga**: invocar varios servicios y consultar varias bases de datos requiere más recursos de cómputo y red.
- **Riesgo de menor disponibilidad**: la disponibilidad decae con el número de servicios implicados. Con cuatro proveedores más el composer: 99,5%^(4+1) = 97,5%. Estrategias de mejora: devolver datos cacheados (posiblemente obsoletos) cuando un proveedor no está disponible, o devolver datos incompletos (por ejemplo, omitir la parte de Kitchen Service si está caído).
- **Falta de consistencia transaccional**: se ejecutan varias consultas contra varias bases de datos, por lo que la consulta puede devolver datos inconsistentes (un Order en estado `CANCELLED` mientras su Ticket aún no lo está).

## 7.2 El patrón CQRS

Muchas aplicaciones usan un RDBMS como sistema de registro transaccional y una base de datos de búsqueda de texto (Elasticsearch, Solr) para consultas de texto, manteniéndolas sincronizadas. CQRS generaliza esta idea: mantiene una o varias **bases de datos de vista** que implementan una o varias consultas de la aplicación.

### Motivaciones

API composition solo resuelve parcialmente el problema. Hay tres problemas comunes que resuelve CQRS:

- Recuperar datos dispersos en varios servicios con API composition provoca **joins en memoria** caros e ineficientes. Ejemplo: `findOrderHistory()` filtra por palabra clave de ítem de menú, que solo guardan Order Service y Kitchen Service; Delivery y Accounting no pueden filtrar ni ordenar por esos atributos, así que devolverían todos los pedidos del consumidor.
- El servicio que posee los datos los almacena en una forma o base de datos que **no soporta eficientemente la consulta requerida**. Ejemplo: `findAvailableRestaurants()` es una búsqueda geoespacial; se implementa fácil con MongoDB o las extensiones geoespaciales de Postgres/MySQL, pero con otra base de datos hay que mantener una réplica diseñada para la consulta.
- La **separación de responsabilidades** implica que el servicio que posee los datos no debe ser el que implementa la consulta. Restaurant Service posee los datos del restaurante, pero conviene que otro servicio (probablemente del equipo de Order Service) implemente la consulta crítica y de alto volumen `findAvailableRestaurants()`.

### Cómo funciona CQRS

CQRS separa comandos de consultas. Divide el modelo de datos persistente y sus módulos en dos partes:

- **Lado de comando (command side)**: implementa las operaciones de creación, actualización y borrado (CUD; POST, PUT, DELETE). Su modelo de dominio se mapea a su propia base de datos y publica eventos de dominio cada vez que cambian sus datos (con un framework como Eventuate Tram o mediante event sourcing). Puede manejar consultas simples basadas en clave primaria sin join.
- **Lado de consulta (query side)**: implementa las consultas (GET). Es más simple porque no implementa reglas de negocio. Usa el tipo de base de datos que más convenga y mantiene su modelo sincronizado suscribiéndose a los eventos de dominio del lado de comando. Puede haber varios modelos de consulta, uno por tipo de consulta.

**CQRS y servicios de solo consulta**: se puede aplicar dentro de un servicio o para definir servicios de consulta, cuya API consiste solo en operaciones de consulta. Order History Service (implementa `findOrderHistory()`) se suscribe a eventos de Order Service, Delivery Service, etc., y actualiza su base de datos de vista. Es también una buena forma de implementar una vista que replica datos de un solo servicio pero que, por separación de responsabilidades, no forma parte de él (Available Restaurants Service).

### Beneficios

- Implementa eficientemente consultas que recuperan datos de varios servicios (la vista pre-une los datos).
- Permite implementar eficientemente consultas diversas (evita las limitaciones de un único almacén de datos).
- Hace posibles las consultas en una aplicación basada en event sourcing (un event store solo soporta consultas por clave primaria).
- Mejora la separación de responsabilidades.

### Inconvenientes

- **Arquitectura más compleja**: hay que escribir los servicios del lado de consulta y operar almacenes de datos adicionales, posiblemente de distintos tipos.
- **Lag de replicación**: existe retardo entre que el lado de comando publica un evento y el lado de consulta actualiza la vista. Un cliente que actualiza un agregado y consulta de inmediato puede ver la versión anterior. Soluciones: que las APIs proporcionen información de versión (un token con el ID del evento publicado) para que el cliente detecte que la vista está desactualizada y haga polling; o que una UI (app nativa o SPA) actualice su modelo local tras el comando exitoso sin lanzar consulta.

La regla es usar API composition siempre que sea posible y CQRS solo cuando sea necesario.

## 7.3 Diseño de vistas CQRS

Un módulo de vista CQRS tiene una API de operaciones de consulta e implementa esas consultas contra una base de datos que mantiene suscribiéndose a eventos. Consta de una base de datos de vista y tres submódulos: **data access** (lógica de acceso a la base de datos), **event handlers** (se suscriben a eventos y actualizan la base de datos) y **query API** (implementa la API de consulta). Decisiones de diseño principales: elegir base de datos y esquema; garantizar actualizaciones idempotentes y manejar actualizaciones concurrentes; construir o reconstruir la vista eficientemente; y permitir al cliente lidiar con el lag de replicación.

### Elección del almacén de la vista

El fin principal de la base de datos y el modelo de datos es implementar eficientemente las consultas del módulo de vista, pero también debe implementar bien las actualizaciones de los event handlers. Una base de datos **NoSQL** suele ser buena opción para una vista CQRS: aprovecha su modelo de datos más rico y su rendimiento, y no sufre sus limitaciones porque solo usa transacciones simples y un conjunto fijo de consultas. A veces conviene una base de datos **SQL** (rendimiento excelente, familiaridad, extensiones no relacionales como geoespaciales, o soporte a motores de reporting). La tabla 7.1 resume opciones:

| Si necesitas | Usa | Ejemplo |
| --- | --- | --- |
| Búsqueda por PK de objetos JSON | Document store (MongoDB, DynamoDB) o key-value (Redis) | Historial de pedidos con documento MongoDB |
| Búsqueda por consulta de objetos JSON | Document store (MongoDB, DynamoDB) | Vista de cliente con MongoDB o DynamoDB |
| Consultas de texto | Motor de búsqueda de texto (Elasticsearch) | Búsqueda de texto de pedidos |
| Consultas de grafo | Base de datos de grafos (Neo4j) | Detección de fraude |
| Reporting/BI SQL tradicional | RDBMS | Informes y analítica estándar |

Las actualizaciones suelen hacerse por clave primaria, pero a veces por el equivalente de una clave foránea (por ejemplo, un `DeliveryPickedUp` que no trae `orderId` obliga a actualizar por `deliveryId`). RDBMS y MongoDB lo resuelven con índices; DynamoDB solo soporta actualizaciones por PK, así que requiere consultar primero un índice secundario.

### Módulo de acceso a datos

Los event handlers y el módulo de query no acceden al almacén directamente, sino a través de un DAO (data access object).

- **Concurrencia**: si la vista se suscribe a eventos de un solo tipo de agregado no hay problema (se procesan secuencialmente). Si se suscribe a varios tipos, varios handlers pueden actualizar el mismo registro a la vez; el DAO debe evitar que una actualización sobrescriba otra, usando bloqueo pesimista u optimista, o actualizando sin leer primero.
- **Event handlers idempotentes**: un handler es idempotente si procesar eventos duplicados produce el resultado correcto (en el peor caso, la vista queda temporalmente desactualizada). Si no es idempotente (p. ej., incrementar un saldo), debe detectar y descartar duplicados registrando los IDs de eventos procesados de forma atómica con la actualización. Con IDs monótonos crecientes (como en Eventuate) basta con guardar `max(eventId)` por instancia de agregado; los registros que son join de varios agregados guardan un mapa de `[tipo de agregado, id de agregado]` a `max(eventId)`.
- **Vista eventualmente consistente**: una operación del lado de comando devuelve un token con el ID del evento publicado; el cliente lo pasa a la consulta, que devuelve un error si la vista aún no fue actualizada por ese evento.

### Añadir y actualizar vistas CQRS

Conceptualmente es simple (desarrollar el módulo, montar el almacén, desplegar; o cambiar los handlers y reconstruir), pero no es práctico sin más. Problemas y soluciones:

- Los message brokers no almacenan mensajes indefinidamente (RabbitMQ los borra tras consumirlos; Kafka tiene retención configurable). Hay que **construir las vistas desde eventos archivados** (por ejemplo, en AWS S3), con tecnología big data como Apache Spark.
- El tiempo de procesar todos los eventos crece con el tiempo. Solución: un **algoritmo incremental de dos pasos**: primero calcular periódicamente un snapshot de cada instancia de agregado a partir del snapshot previo y los eventos posteriores; luego crear la vista con los snapshots y eventos siguientes.

## 7.4 Implementación de una vista CQRS con AWS DynamoDB

DynamoDB es una base de datos NoSQL escalable y totalmente gestionada en Amazon; su modelo son tablas con ítems (colecciones jerárquicas de pares nombre-valor, como JSON). La vista de `findOrderHistory()` consume eventos de varios servicios, por lo que se implementa como un **Order View Service** independiente con operaciones `findOrderHistory()` y `findOrder()` (esta última sale gratis). Sus módulos: `OrderHistoryEventHandlers`, `OrderHistoryQuery API`, `OrderHistoryDataAccess` (con el `OrderHistoryDAO`) y la tabla `ftgo-order-history`.

**Event handlers** (`OrderHistoryEventHandlers`): métodos de una línea que invocan al DAO con argumentos derivados del evento. Cada uno recibe un `DomainEventEnvelope`. Por ejemplo, `handleOrderCreated()` llama a `orderHistoryDao.addOrder()` y `handleDeliveryPickedUp()` llama a `orderHistoryDao.notePickedUp()`. Un helper `makeSourceEvent()` construye un `SourceEvent` con el tipo e ID del agregado y el ID del evento, usado para la idempotencia.

**Modelado y diseño de consulta**:

- Cada Order se almacena como un único ítem de la tabla `ftgo-order-history`; los campos simples se mapean a atributos de valor único y `lineItems` a una lista de mapas.
- `findOrderHistory()` devuelve los pedidos ordenados por antigüedad creciente, lo que requiere una clave primaria compuesta (**partition key** + **sort key**). Como `(consumerId, orderCreationDate)` no es único, se usa un **índice secundario global** `ftgo-order-history-by-consumer-id-and-creation-time` con esa clave no única, que puede incluir atributos no clave (`orderId`, `status`) para mejorar rendimiento y permitir filtrado.
- El filtro de antigüedad máxima se implementa con la restricción de rango sobre la sort key; los demás criterios con una **filter expression** booleana (p. ej. `orderStatus = :orderStatus`). La búsqueda por palabra clave tokeniza nombre de restaurante e ítems de menú en un atributo `keywords` y usa `contains(keywords, :keyword1) OR contains(keywords, :keyword2)`.
- **Paginación**: la operación `Query` tiene `pageSize`; si hay más ítems devuelve `LastEvaluatedKey`, que se usa como `exclusiveStartKey` para la siguiente página. Como DynamoDB no soporta paginación por posición, el servicio devuelve un token de paginación opaco.
- **Actualizaciones**: se prefiere `UpdateItem()` sobre `PutItem()` porque actualiza atributos individuales (cada handler actualiza atributos distintos del Order), sin tener que leer el ítem primero y evitando pérdidas de actualizaciones.
- **Detección de duplicados**: todos los handlers son idempotentes, pero para evitar que la vista quede temporalmente desactualizada se usa una **conditional update**. Se registra en cada ítem un atributo `«aggregateType»«aggregateId»` con el mayor ID de evento recibido y se usa la condición:

```
attribute_not_exists(«aggregateType»«aggregateId»)
OR «aggregateType»«aggregateId» < :eventId
```

La actualización solo se permite si el atributo no existe o el `eventId` es mayor que el último procesado.

**Clase `OrderHistoryDaoDynamoDb`**: implementa los métodos que leen y escriben en la tabla.

- `addOrder()`: crea un `UpdateItemSpec` con la clave primaria, la expresión de actualización y el mapa de valores, y delega en `idempotentUpdate()`.
- `notePickedUp()`: cambia el `deliveryStatus` del Order a `PICKED_UP` mediante otro `UpdateItemSpec` e `idempotentUpdate()`.
- `idempotentUpdate()`: si hay `sourceEvent`, añade la condition expression de detección de duplicados; captura e ignora la `ConditionalCheckFailedException` que lanza `updateItem()` cuando el evento es duplicado.
- `findOrderHistory()`: crea un `QuerySpec` (con `withScanIndexForward(false)` para ordenar por antigüedad creciente, hash key `consumerId`, condición de rango sobre `creationDate`, filtros y límite de tamaño), consulta el índice secundario y transforma los ítems en un objeto `OrderHistory`. La paginación serializa `getLastEvaluatedKey()` en un token JSON.

La única parte compleja del código es el DAO, porque debe manejar bien la concurrencia y garantizar que las actualizaciones sean idempotentes.

## Ideas clave

- Implementar consultas que recuperan datos de varios servicios es difícil porque los datos de cada servicio son privados y no se puede usar una consulta distribuida tradicional sin romper la encapsulación.
- El patrón API composition hace que un API composer invoque a los servicios proveedores y combine los resultados; es el más simple y debe usarse siempre que sea posible.
- Sus inconvenientes son la sobrecarga, el riesgo de menor disponibilidad (99,5%^(4+1) = 97,5% con cuatro proveedores) y la falta de consistencia transaccional.
- Una limitación clave de API composition es que algunas consultas complejas requieren joins en memoria de grandes conjuntos de datos, ineficientes.
- CQRS separa el lado de comando (CUD, publica eventos) del lado de consulta (vistas de solo lectura mantenidas suscribiéndose a esos eventos); es más potente pero más complejo.
- CQRS resuelve tres problemas: joins en memoria ineficientes, datos en una forma que no soporta la consulta, y la necesidad de separar responsabilidades; además permite consultas sobre aplicaciones con event sourcing.
- Al diseñar una vista hay que elegir base de datos (NoSQL suele encajar), manejar concurrencia y actualizaciones por clave foránea, garantizar handlers idempotentes y detectar/descartar duplicados, y prever la reconstrucción con eventos archivados y snapshots incrementales.
- Los clientes deben manejar la consistencia eventual de las vistas CQRS (lag de replicación), por ejemplo con tokens de versión o actualizando el modelo local de la UI.
- El ejemplo con DynamoDB usa un índice secundario global, `UpdateItem()` en vez de `PutItem()`, condition expressions para idempotencia y tokens opacos para paginación.
