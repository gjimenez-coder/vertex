# Interprocess communication in a microservice architecture — Estudio

## Tarjetas de repaso

P: ¿Por qué la IPC es más importante en microservicios que en un monolito? / R: En un monolito los módulos se invocan con llamadas a métodos del lenguaje, pero en microservicios los servicios son procesos separados que colaboran para atender una petición, así que la comunicación entre procesos adquiere un papel central.

P: ¿Cuáles son las dos dimensiones para clasificar las interacciones cliente-servicio? / R: Uno-a-uno vs uno-a-muchos, y síncrono vs asíncrono.

P: ¿Qué estilos de interacción corresponden a uno-a-uno asíncrono y a uno-a-muchos asíncrono? / R: Uno-a-uno asíncrono: asynchronous request/response y one-way notifications; uno-a-muchos asíncrono: publish/subscribe y publish/async responses.

P: ¿Por qué usar un message broker no implica por sí solo acoplamiento débil? / R: Porque el estilo request/response es ortogonal a la tecnología: incluso con un broker el cliente puede bloquearse esperando la respuesta.

P: ¿Qué es el diseño API-first y con qué se define la API? / R: Primero se escribe la definición de la API con un IDL, se revisa con los clientes y solo después se implementa el servicio.

P: ¿Qué significan MAJOR, MINOR y PATCH en Semantic Versioning? / R: MAJOR para cambios incompatibles, MINOR para mejoras retrocompatibles y PATCH para correcciones retrocompatibles.

P: ¿En qué consiste el patrón Remote procedure invocation (RPI)? / R: El cliente invoca a un servicio mediante un protocolo síncrono de invocación remota, como REST; la lógica del cliente usa una interfaz proxy implementada por un RPI proxy que llama a un RPI server adapter en el servicio.

P: ¿Cuáles son los niveles del modelo de madurez de Richardson para REST? / R: Nivel 0 (POST a un único endpoint), Nivel 1 (idea de recursos), Nivel 2 (verbos HTTP, habilita caching en GET) y Nivel 3 (HATEOAS, la representación incluye enlaces para acciones).

P: ¿Qué es gRPC y sobre qué se apoya? / R: Un framework multilenguaje, binario sobre HTTP/2, con IDL basado en Protocol Buffers que genera stubs de cliente y skeletons de servidor; sus APIs son servicios con métodos fuertemente tipados y soporta streaming.

P: ¿Qué hace el patrón Circuit breaker? / R: Es un RPI proxy que rechaza inmediatamente las invocaciones durante un periodo cuando el número de fallos consecutivos supera un umbral, evitando fallos en cascada.

P: ¿Qué dos enfoques de service discovery existen y cuál recomienda el autor? / R: A nivel de aplicación (self registration + client-side discovery) y provisto por la plataforma (3rd party registration + server-side discovery); el autor recomienda el provisto por la plataforma siempre que sea posible.

P: ¿Qué tres tipos de mensaje define el modelo de mensajería? / R: Document, Command (equivale a una petición RPC) y Event (algo notable ocurrió, suele ser un evento de dominio).

P: ¿Cómo se preserva el orden al escalar consumidores en competencia? / R: Con canales particionados (sharded): el emisor incluye un shard key, el broker asigna el mensaje a una partición y cada shard a un único receptor de un grupo; con orderId como shard key los eventos de un pedido van al mismo shard.

P: ¿Qué es el patrón Transactional outbox? / R: Publicar un evento o mensaje como parte de una transacción guardándolo en una tabla OUTBOX de la base de datos, que luego un Message Relay lee y publica al broker.

P: ¿Cómo afecta la comunicación síncrona a la disponibilidad? / R: La disponibilidad de una operación es el producto de la de los servicios invocados; con tres servicios al 99,5% el conjunto baja a 99,5%³ = 98,5%.

## Preguntas de autoevaluación

P: ¿Qué riesgo tiene que servicio y clientes no se compilen juntos y cómo se mitiga? / R: Una API incompatible no da error de compilación sino fallos en tiempo de ejecución; se mitiga definiendo la API con un IDL, aplicando diseño API-first y usando Semantic Versioning. (Sección: Visión general de la IPC — Definir y evolucionar APIs)

P: ¿Cuándo un cambio de API es retrocompatible y qué principio lo respalda? / R: Los cambios aditivos (atributos opcionales en la petición, atributos nuevos en la respuesta, nuevas operaciones) son retrocompatibles si se respeta el principio de robustez: "Be conservative in what you do, be liberal in what you accept from others". (Sección: Definir y evolucionar APIs)

P: ¿Por qué se prefieren formatos de mensaje multilenguaje y qué ventaja tiene Protocol Buffers frente a Avro? / R: Para no acoplarse a un lenguaje (no usar serialización de Java); Protocol Buffers usa campos etiquetados (tagged), lo que facilita la evolución, mientras Avro exige conocer el esquema. (Sección: Formatos de mensaje)

P: ¿Cómo evita el Circuit breaker un fallo en cascada y qué lo acompaña? / R: Un servicio no disponible o lento puede agotar recursos del llamante (p. ej. hilos en el API gateway); el Circuit breaker, combinado con network timeouts y el límite de peticiones pendientes, hace que los intentos fallen de inmediato tras superar un umbral. (Sección: Fallo parcial con el patrón Circuit breaker)

P: ¿Cómo se emparejan petición y respuesta en el request/response asíncrono sobre mensajería? / R: El cliente envía un command message con cabecera reply channel y message id; el servicio responde con un correlation id igual al id del mensaje para emparejar respuesta y petición. (Sección: Asynchronous messaging — Implementar los estilos de interacción)

P: ¿Qué problema resuelve el Transactional outbox y por qué no se usan transacciones distribuidas? / R: Permite publicar mensajes como parte de la transacción que actualiza la base de datos para evitar estados inconsistentes; las transacciones distribuidas no son buena opción y brokers como Kafka no las soportan. (Sección: Mensajería transaccional)

P: ¿Cuáles son las dos formas de que el Message Relay mueva los mensajes de la outbox? / R: Polling publisher (sondear periódicamente la outbox, publicar y borrar) y Transaction log tailing (un miner lee el commit log y publica cada cambio, con herramientas como Debezium o Eventuate Tram). (Sección: Mensajería transaccional)

P: ¿Qué técnica permite seguir creando pedidos aunque un servicio dependiente esté caído? / R: Terminar el procesamiento tras responder: Order Service crea el pedido en estado PENDING, responde con el id y valida después con Consumer Service y Restaurant Service pasando a VALIDATED; el inconveniente es que complica al cliente. (Sección: Usar mensajería asíncrona para mejorar la disponibilidad)

## Puntos a dominar

- Distinguir los estilos de IPC según las dos dimensiones (uno-a-uno/uno-a-muchos, síncrono/asíncrono) y saber que no hay "balas de plata".
- Explicar el diseño API-first, el versionado semántico y cómo soportar a la vez versiones antigua y nueva ante cambios incompatibles.
- Comparar REST (simple, de facto, síncrono) y gRPC (binario, eficiente, muchas operaciones de actualización) con sus beneficios e inconvenientes.
- Describir el manejo de fallos parciales: network timeouts, límite de peticiones pendientes y Circuit breaker (Hystrix en JVM, Polly en .NET).
- Diferenciar los dos enfoques de service discovery y justificar la preferencia por el provisto por la plataforma.
- Modelar la mensajería con mensajes y canales (point-to-point y publish-subscribe) y mapearla a un broker según orden, entrega, persistencia y escalabilidad.
- Preservar el orden con canales particionados (shard key) y descartar duplicados con manejadores idempotentes o registrando message ids.
- Aplicar Transactional outbox con Polling publisher o Transaction log tailing, y usar mensajería asíncrona para mejorar la disponibilidad.
