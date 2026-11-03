# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 3 — Interprocess communication in a microservice architecture (Comunicación entre procesos en una arquitectura de microservicios)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

En un monolito los módulos se invocan mediante llamadas a métodos del lenguaje, pero en una arquitectura de microservicios los servicios son procesos separados que colaboran para atender una petición, por lo que la comunicación entre procesos (IPC) adquiere un papel mucho más importante. El capítulo recorre las opciones de IPC y sus compromisos, sin "balas de plata".

La tesis del autor es favorecer servicios poco acoplados que se comunican mediante mensajería asíncrona, reservando protocolos síncronos como REST sobre todo para comunicarse con otras aplicaciones. La elección de IPC es una decisión arquitectónica que afecta a la disponibilidad e incluso se cruza con la gestión de transacciones.

Sales sabiendo definir y versionar APIs, comparar REST, gRPC y mensajería, manejar fallos parciales con el patrón Circuit breaker, aplicar service discovery, escalar consumidores preservando el orden, descartar mensajes duplicados, publicar mensajes de forma fiable dentro de una transacción (Transactional outbox) y diseñar servicios que mejoran la disponibilidad evitando la comunicación síncrona.

## El ejemplo que recorre el capítulo

La aplicación FTGO (reparto de comida) es el hilo conductor. El `Order Service` aparece una y otra vez: expone una API REST para crear pedidos, invoca `Consumer Service` y `Restaurant Service` para validarlos, y sirve para ilustrar el Circuit breaker, la composición de APIs vía API gateway, la mensajería de dominio y el diseño autocontenido que mejora la disponibilidad.

## Visión general de la IPC

Las interacciones cliente-servicio se clasifican en dos dimensiones: uno-a-uno vs uno-a-muchos, y síncrono vs asíncrono.

- Uno-a-uno síncrono: Request/response (el cliente espera respuesta y suele bloquearse; acopla fuertemente).
- Uno-a-uno asíncrono: Asynchronous request/response y One-way notifications.
- Uno-a-muchos asíncrono: Publish/subscribe y Publish/async responses.

El estilo request/response es ortogonal a la tecnología: incluso con un message broker el cliente puede bloquearse esperando respuesta, por lo que usar mensajería no implica por sí solo acoplamiento débil.

### Definir y evolucionar APIs

La API de un servicio es un contrato de operaciones (invocables) y eventos (publicados). Como servicio y clientes no se compilan juntos, una API incompatible no da error de compilación sino fallos en tiempo de ejecución. Conviene definir la API con un IDL y aplicar diseño API-first: primero se escribe la definición, se revisa con los clientes y solo después se implementa.

Las APIs evolucionan. El autor recomienda Semantic Versioning (MAJOR.MINOR.PATCH): MAJOR para cambios incompatibles, MINOR para mejoras retrocompatibles y PATCH para correcciones retrocompatibles. Los cambios aditivos (atributos opcionales en la petición, atributos nuevos en la respuesta, nuevas operaciones) son retrocompatibles si se respeta el principio de robustez: "Be conservative in what you do, be liberal in what you accept from others" (PDF p. 100). Para cambios mayores el servicio debe soportar a la vez versiones antigua y nueva (p. ej. prefijos `/v1/…` y `/v2/…` en la URL, o versión en el MIME type vía content negotiation).

### Formatos de mensaje

Deben ser multilenguaje (no usar serialización de Java). Dos categorías:

- Texto (JSON, XML): legibles y autodescriptivos, facilitan la evolución retrocompatible; esquemas con XML Schema o JSON Schema. Inconveniente: mensajes verbosos y coste de parseo.
- Binario (Protocol Buffers, Avro): compactos, con IDL tipado que obliga a API-first. Protocol Buffers usa campos etiquetados (tagged), lo que facilita la evolución frente a Avro, que exige conocer el esquema.

## Comunicación con el patrón síncrono Remote procedure invocation (RPI)

> Patrón: Remote procedure invocation — el cliente invoca a un servicio con un protocolo síncrono de invocación remota, como REST.

La lógica de negocio del cliente invoca una interfaz proxy implementada por un RPI proxy, que hace la petición a un RPI server adapter en el servicio.

### REST

REST (casi siempre sobre HTTP) gira en torno al recurso, referenciado por URL y manipulado con verbos HTTP (GET para recuperar, POST para crear, PUT para actualizar). Modelo de madurez de Richardson:

- Nivel 0: POST a un único endpoint.
- Nivel 1: idea de recursos.
- Nivel 2: verbos HTTP (habilita caching en GET).
- Nivel 3: HATEOAS, la representación incluye enlaces para acciones.

El IDL más popular es la OpenAPI Specification (nacida de Swagger). Problemas típicos: recuperar varios recursos relacionados en una sola petición (soluciones como `?expand=consumer`, o alternativas como GraphQL y Netflix Falcor) y mapear operaciones a verbos HTTP (p. ej. `POST /orders/{orderId}/cancel`).

Beneficios: simple y familiar, testeable con Postman o curl, soporta request/response, amigable con firewalls y sin broker intermedio. Inconvenientes: solo request/response, menor disponibilidad (cliente y servicio deben estar activos a la vez), el cliente debe conocer la ubicación de las instancias (necesita service discovery) y la dificultad de obtener varios recursos o mapear verbos.

### gRPC

Framework multilenguaje, binario sobre HTTP/2, con IDL basado en Protocol Buffers que genera stubs de cliente y skeletons de servidor. Una API gRPC son servicios con métodos fuertemente tipados; soporta streaming. Al ser formato etiquetado, permite evolucionar APIs manteniendo retrocompatibilidad.

```protobuf
service OrderService {
  rpc createOrder(CreateOrderRequest) returns (CreateOrderReply) {}
  rpc cancelOrder(CancelOrderRequest) returns (CancelOrderReply) {}
  rpc reviseOrder(ReviseOrderRequest) returns (ReviseOrderReply) {}
}
```

Beneficios: fácil diseñar muchas operaciones de actualización, mecanismo compacto y eficiente, streaming bidireccional e interoperabilidad entre lenguajes. Inconvenientes: más trabajo para clientes JavaScript y firewalls antiguos sin HTTP/2. Como REST, es síncrono y sufre fallos parciales.

### Fallo parcial con el patrón Circuit breaker

> Patrón: Circuit breaker — un RPI proxy que rechaza inmediatamente las invocaciones durante un periodo cuando el número de fallos consecutivos supera un umbral.

Un servicio no disponible o lento puede provocar un fallo en cascada que agote recursos del llamante (p. ej. hilos en el API gateway). La solución combina:

- Network timeouts: nunca bloquear indefinidamente.
- Limitar el número de peticiones pendientes de un cliente a un servicio.
- Circuit breaker: tras superar un umbral de errores, los intentos fallan de inmediato; tras un tiempo se reintenta y, si hay éxito, se cierra.

Netflix Hystrix implementa estos patrones en la JVM; en .NET existe Polly. Hay que decidir caso por caso cómo recuperarse: devolver un error, un valor por defecto o una respuesta cacheada. En la composición de APIs del API gateway, datos esenciales (Order Service) justifican error o caché, mientras que datos menos críticos (Delivery Service) pueden omitirse.

### Service discovery

Las instancias tienen ubicaciones de red asignadas dinámicamente y cambiantes (autoescalado, fallos, upgrades), por lo que el cliente necesita un mecanismo de descubrimiento basado en un service registry (base de datos de ubicaciones). Dos enfoques:

- A nivel de aplicación: combina Self registration (la instancia se registra, con health check URL) y Client-side discovery (el cliente consulta el registro y balancea). Popularizado por Netflix (Eureka, Ribbon) y Pivotal (Spring Cloud). Ventaja: funciona entre plataformas de despliegue; inconveniente: una librería por lenguaje y gestionar el registro.
- Provisto por la plataforma: combina 3rd party registration (un registrar registra el servicio) y Server-side discovery (el cliente llama a un DNS/VIP y un router balancea). En Docker/Kubernetes el descubrimiento es transparente para cualquier lenguaje; inconveniente: solo descubre servicios desplegados en la plataforma. El autor recomienda este enfoque siempre que sea posible.

## Comunicación con el patrón Asynchronous messaging

> Patrón: Messaging — el cliente invoca un servicio mediante mensajería asíncrona.

Basado en el modelo de *Enterprise Integration Patterns* (Hohpe y Woolf): los mensajes se intercambian por canales. Un mensaje tiene cabecera (pares nombre-valor, id único, return address) y cuerpo. Tipos: Document, Command (equivale a una petición RPC) y Event (algo notable ocurrió; suele ser un evento de dominio). Canales: point-to-point (un solo consumidor, para uno-a-uno) y publish-subscribe (todos los consumidores, para uno-a-muchos).

### Implementar los estilos de interacción

La mensajería soporta todos los estilos. Request/response asíncrono: el cliente envía un command message con cabecera `reply channel` y message id; el servicio responde con un `correlation id` igual al id del mensaje para emparejar respuesta y petición. One-way notification: se envía y no hay respuesta. Publish/subscribe: eventos de dominio a canales cuyo nombre deriva de la clase de dominio (p. ej. `Order Service` publica eventos Order en un canal Order). Publish/async responses combina publish/subscribe y request/response.

La especificación de una API asíncrona debe indicar nombres de canales, tipos y formatos de mensaje; no hay estándar ampliamente adoptado (documento informal).

### Message broker

Casi todas las apps usan un broker intermediario; la alternativa brokerless (p. ej. ZeroMQ) ofrece menor latencia y sin punto único de fallo, pero exige service discovery, reduce disponibilidad y dificulta la entrega garantizada. Brokers populares: ActiveMQ, RabbitMQ, Apache Kafka; servicios cloud como AWS Kinesis y AWS SQS. Criterios de selección: lenguajes soportados, estándares (AMQP, STOMP), orden de mensajes, garantías de entrega, persistencia, durabilidad, escalabilidad, latencia y competing consumers. Cada broker implementa los canales de forma distinta (JMS: colas/topics; AMQP: exchanges+colas; Kafka: topics; Kinesis: streams; SQS: colas, solo point-to-point).

Beneficios del broker: acoplamiento débil, buffering de mensajes, comunicación flexible y IPC explícita. Inconvenientes: posible cuello de botella, posible punto único de fallo y complejidad operativa añadida.

### Consumidores en competencia y orden de mensajes

Para escalar consumidores sin perder el orden se usan canales particionados (sharded): el emisor incluye un shard key; el broker asigna el mensaje a una partición y asigna cada shard a un único receptor de un grupo (p. ej. *consumer group* en Kafka). Usando `orderId` como shard key, todos los eventos de un pedido van al mismo shard y se procesan en orden.

### Mensajes duplicados

Los brokers suelen garantizar entrega *at-least-once*, por lo que puede haber duplicados. Dos soluciones: escribir manejadores idempotentes (seguros al ejecutarse varias veces, si el broker preserva el orden en la reentrega) o rastrear y descartar duplicados registrando el message id (p. ej. insertándolo en una tabla `PROCESSED_MESSAGES`; el `INSERT` falla si es duplicado).

### Mensajería transaccional

Un servicio necesita publicar mensajes como parte de la transacción que actualiza la base de datos para evitar estados inconsistentes. Las transacciones distribuidas no son buena opción (y brokers como Kafka no las soportan).

> Patrón: Transactional outbox — publicar un evento o mensaje como parte de una transacción guardándolo en una OUTBOX de la base de datos.

El servicio inserta el mensaje en una tabla `OUTBOX` dentro de la transacción local ACID, y un Message Relay lee la tabla y publica al broker. Dos formas de mover los mensajes:

> Patrón: Polling publisher — publicar mensajes sondeando la outbox en la base de datos.

El relay consulta periódicamente (`SELECT * FROM OUTBOX ...`), publica y borra. Simple pero el sondeo frecuente es costoso.

> Patrón: Transaction log tailing — publicar los cambios de la base de datos leyendo el log de transacciones.

Un transaction log miner lee el commit log y publica cada cambio. Ejemplos: Debezium, LinkedIn Databus, DynamoDB streams y Eventuate Tram (del propio autor, con MySQL binlog, Postgres WAL o polling).

### Librerías y frameworks

Usar la librería del broker directamente acopla la lógica de negocio y requiere mucho boilerplate. El autor usa su framework Eventuate Tram, que oculta detalles y añade mensajería transaccional y detección de duplicados. Expone `MessageProducer`/`MessageConsumer`, publicación/consumo de eventos de dominio (`DomainEventPublisher`, `DomainEventDispatcher`) y mensajería command/reply (`CommandProducer`, `CommandDispatcher`).

## Usar mensajería asíncrona para mejorar la disponibilidad

La comunicación síncrona reduce la disponibilidad: la de una operación es el producto de la de los servicios invocados. Si `Order Service` y los dos servicios que invoca están al 99,5%, el conjunto baja a 99,5%³ = 98,5% (PDF p. 134). El problema no es exclusivo de REST: también ocurre si se usa request/response sobre mensajería y se espera la respuesta.

Formas de eliminar la interacción síncrona:

- Definir servicios con APIs solo asíncronas (no siempre posible, pues las APIs públicas suelen ser REST).
- Replicar datos: el servicio mantiene una réplica de los datos que necesita, actualizada suscribiéndose a eventos de los servicios dueños. Inconvenientes: puede replicar grandes volúmenes y no resuelve cómo actualizar datos de otros servicios.
- Terminar el procesamiento tras responder: validar con datos locales, actualizar la BD (incluida la tabla OUTBOX), responder al cliente y luego intercambiar mensajes de forma asíncrona (a menudo con una saga). `Order Service` crea el pedido en estado `PENDING`, responde con el id y valida después con `Consumer Service` y `Restaurant Service`, pasando a `VALIDATED`. Así sigue creando pedidos aunque un servicio esté caído; el inconveniente es que complica al cliente (debe sondear o recibir una notificación).

## Ideas clave

- La IPC es central en microservicios; elige con cuidado entre invocación remota síncrona (RPI) y el patrón de mensajería asíncrona, sin "balas de plata".
- Gestiona la evolución de la API: los cambios retrocompatibles son los más sencillos; usa Semantic Versioning y soporta versiones antigua y nueva ante cambios incompatibles.
- REST es simple y de facto estándar, pero síncrono, con problemas de obtener varios recursos y mapear verbos; gRPC es binario, eficiente y con muchas operaciones de actualización.
- Los clientes síncronos deben manejar fallos parciales con timeouts, límite de peticiones pendientes y Circuit breaker para evitar cascadas.
- Las arquitecturas síncronas necesitan service discovery: a nivel de aplicación (Self registration + Client-side discovery) o provisto por la plataforma (3rd party registration + Server-side discovery), este último preferido.
- Diseña la mensajería con el modelo de mensajes y canales y mapéalo a un broker; valora orden, entrega, persistencia y escalabilidad.
- Preserva el orden con canales particionados (shard key) y descarta duplicados con manejadores idempotentes o registrando message ids.
- Publica mensajes de forma atómica con Transactional outbox, leyéndola mediante Polling publisher o Transaction log tailing; la mensajería asíncrona aumenta la disponibilidad.
