# Implementing queries in a microservice architecture (Implementación de consultas en una arquitectura de microservicios) — Estudio

## Tarjetas de repaso

P: ¿Por qué es difícil implementar consultas que recuperan datos de varios servicios? / R: Porque los datos de cada servicio son privados y no se puede usar un mecanismo tradicional de consulta distribuida sin violar la encapsulación.

P: ¿Cuáles son los dos patrones del capítulo para implementar consultas? / R: API composition (el más simple) y CQRS (Command query responsibility segregation, más potente pero más complejo).

P: ¿En qué consiste el patrón API composition? / R: Un API composer invoca a los servicios proveedores que poseen los datos y combina los resultados.

P: ¿Qué dos tipos de participantes tiene API composition? / R: El API composer (implementa la consulta) y los provider services (servicios que poseen parte de los datos).

P: ¿Quiénes pueden hacer de API composer? / R: Un cliente de los servicios, un API gateway (cuando la operación es parte de la API externa) o un servicio independiente.

P: ¿Cuáles son los tres inconvenientes de API composition? / R: Mayor sobrecarga de cómputo y red, riesgo de menor disponibilidad (99,5%^(4+1) = 97,5% con cuatro proveedores) y falta de consistencia transaccional.

P: ¿Qué significa CQRS y qué separa? / R: Command query responsibility segregation; separa el lado de comando (CUD, publica eventos) del lado de consulta (vistas de solo lectura mantenidas suscribiéndose a esos eventos).

P: ¿Qué tres problemas resuelve CQRS que API composition no resuelve bien? / R: Joins en memoria ineficientes, datos almacenados en una forma que no soporta la consulta, y la necesidad de separar responsabilidades; además permite consultas en aplicaciones con event sourcing.

P: ¿Qué hace el lado de consulta en CQRS y cómo mantiene sus datos? / R: Implementa las consultas (GET) sin reglas de negocio, usa la base de datos que más convenga y mantiene su modelo sincronizado suscribiéndose a los eventos de dominio del lado de comando.

P: ¿De qué submódulos consta un módulo de vista CQRS? / R: Data access (DAO), event handlers (se suscriben a eventos y actualizan la base de datos) y query API, más la propia base de datos de vista.

P: ¿Qué es el lag de replicación y cómo se maneja? / R: El retardo entre que el lado de comando publica un evento y la vista se actualiza; se maneja con tokens de versión que permiten al cliente detectar la vista desactualizada, o actualizando el modelo local de la UI tras el comando.

P: ¿Cuándo es idempotente un event handler y qué hacer si no lo es? / R: Es idempotente si procesar eventos duplicados produce el resultado correcto; si no lo es, debe detectar y descartar duplicados registrando atómicamente los IDs de eventos procesados.

P: ¿Por qué suele encajar una base de datos NoSQL en una vista CQRS? / R: Aprovecha su modelo de datos rico y su rendimiento sin sufrir sus limitaciones, porque solo usa transacciones simples y un conjunto fijo de consultas.

P: ¿Por qué el ejemplo con DynamoDB prefiere UpdateItem() sobre PutItem()? / R: Porque actualiza atributos individuales (cada handler actualiza atributos distintos del Order) sin leer el ítem primero, evitando pérdidas de actualizaciones.

P: ¿Cuál es la regla práctica para elegir entre los dos patrones? / R: Usar API composition siempre que sea posible y recurrir a CQRS solo cuando sea necesario.

## Preguntas de autoevaluación

P: ¿Por qué `findOrder()` es un buen candidato para API composition y `findOrderHistory()` no? / R: `findOrder()` es un equi-join simple por clave primaria entre los servicios proveedores; `findOrderHistory()` filtra por atributos (palabra clave de ítem de menú) que solo poseen algunos servicios, provocando joins en memoria ineficientes. (Secciones 7.1 y 7.2)

P: ¿Cómo debe invocar el API composer a los servicios proveedores para minimizar la latencia? / R: En paralelo cuando no hay dependencias entre las llamadas, y secuencialmente solo cuando necesita el resultado de un servicio para invocar a otro; conviene un diseño reactivo (CompletableFuture, RxJava). (Sección 7.1, Modelo de programación reactivo)

P: ¿Qué estrategias existen para mejorar la disponibilidad de una consulta con API composition cuando un proveedor está caído? / R: Devolver datos cacheados aunque sean obsoletos, o devolver datos incompletos omitiendo la parte del servicio no disponible. (Sección 7.1, Beneficios e inconvenientes)

P: ¿Por qué `findAvailableRestaurants()` motiva el uso de CQRS? / R: Es una búsqueda geoespacial; si el servicio que posee los datos no soporta ese tipo de consulta eficientemente, se mantiene una réplica/vista diseñada para ella, y además conviene por separación de responsabilidades que otro servicio la implemente. (Sección 7.2, Motivaciones)

P: ¿Cómo se maneja la concurrencia en el módulo de acceso a datos de una vista? / R: Si solo se suscribe a un tipo de agregado no hay problema; si se suscribe a varios, el DAO evita sobrescrituras con bloqueo pesimista u optimista, o actualizando sin leer primero. (Sección 7.3, Módulo de acceso a datos)

P: ¿Por qué no es práctico simplemente procesar todos los eventos para construir o reconstruir una vista, y qué soluciones hay? / R: Los brokers no almacenan mensajes indefinidamente y el tiempo de procesamiento crece con el tiempo; se construyen las vistas desde eventos archivados (p. ej. S3 con Apache Spark) y se usa un algoritmo incremental de snapshots de dos pasos. (Sección 7.3, Añadir y actualizar vistas CQRS)

P: ¿Cómo implementa el ejemplo de DynamoDB la detección de duplicados? / R: Con una conditional update que registra en cada ítem el mayor ID de evento recibido y solo permite la actualización si el atributo no existe o el eventId es mayor que el último procesado. (Sección 7.4)

P: ¿Cómo soporta el Order View Service la paginación en DynamoDB? / R: La operación Query usa pageSize y, si hay más ítems, devuelve LastEvaluatedKey, que se usa como exclusiveStartKey para la siguiente página; como no hay paginación por posición, el servicio devuelve un token de paginación opaco. (Sección 7.4)

## Puntos a dominar

- Distinguir cuándo una consulta recupera datos de un solo servicio frente a varios, y por qué eso descarta la consulta distribuida tradicional.
- Explicar el patrón API composition, sus participantes (API composer y provider services) y las tres opciones de quién hace de composer.
- Razonar los tres inconvenientes de API composition, en especial el cálculo de disponibilidad 99,5%^(4+1) = 97,5%.
- Explicar la separación command side / query side de CQRS y los tres problemas que resuelve.
- Describir los submódulos de una vista CQRS (data access, event handlers, query API) y sus decisiones de diseño.
- Justificar la elección del almacén de la vista según la tabla 7.1 (document store, key-value, motor de texto, grafo, RDBMS).
- Garantizar actualizaciones idempotentes, detectar duplicados y manejar actualizaciones concurrentes y por clave foránea.
- Prever el lag de replicación y las técnicas para que el cliente lo maneje (tokens de versión, actualización del modelo local de la UI).
- Reconocer los elementos clave del ejemplo con DynamoDB: índice secundario global, UpdateItem() vs PutItem(), condition expressions para idempotencia y tokens opacos de paginación.
