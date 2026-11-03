# Designing business logic in a microservice architecture — Estudio

## Tarjetas de repaso

- P: ¿Qué dos retos propios de los microservicios aborda el diseño de la lógica de negocio? / R: Que el modelo de dominio es una maraña de clases con referencias de objeto que cruzarían fronteras de servicio, y diseñar la lógica respetando las restricciones de transacciones (ACID dentro de un servicio, saga entre servicios).
- P: ¿Qué es el patrón Transaction script? / R: Un enfoque procedural donde se escribe un método (script) por cada petición de la capa de presentación; separa el comportamiento (clases de servicio y DAOs) de los datos (objetos con poco o ningún comportamiento). Sirve para lógica simple.
- P: ¿Qué es el patrón Domain model? / R: Organizar la lógica como una red de clases pequeñas que corresponden a conceptos del dominio, muchas con estado y comportamiento; el service delega el grueso de la lógica en objetos de dominio persistentes. Adecuado para lógica compleja.
- P: ¿Qué es un aggregate en DDD? / R: Un cúmulo de objetos de dominio dentro de una frontera explícita, tratado como unidad, formado por una entidad raíz y posiblemente otras entidades y value objects.
- P: ¿Cuáles son las tres reglas de los aggregates? / R: 1) Referenciar solo la raíz del aggregate; 2) las referencias entre aggregates usan claves primarias (no referencias de objeto); 3) una transacción crea o actualiza un solo aggregate.
- P: ¿Cómo referencia el Order aggregate a Consumer y Restaurant? / R: Por clave primaria: con `consumerId` y `restaurantId`, no por referencia de objeto.
- P: ¿Por qué conviene hacer los aggregates lo más finos posible? / R: Mejoran la escalabilidad (permiten más actualizaciones simultáneas al serializar por aggregate), reducen conflictos entre usuarios y facilitan la descomposición en servicios; solo se agrandan cuando se necesita mayor atomicidad.
- P: ¿Qué es un domain event? / R: Una clase del modelo de dominio que representa algo que ha ocurrido a un aggregate, normalmente un cambio de estado (p. ej. Order Created, Order Cancelled, Order Shipped), con nombre en participio pasado.
- P: ¿Qué es el event enrichment? / R: Incluir en el evento la información que los consumidores necesitan (líneas, entrega, pago, restaurante) para evitar que consulten al servicio; simplifica a los consumidores pero hace las clases de evento menos estables.
- P: ¿Qué es el event storming? / R: Un taller centrado en eventos para entender un dominio complejo, en tres pasos: brainstorming de eventos, identificar el disparador de cada evento (comando, sistema externo, otro evento o paso del tiempo) e identificar los aggregates.
- P: ¿Cómo se publican los eventos de forma fiable? / R: Con mensajería transaccional: el service los publica en la misma transacción que actualiza el aggregate; Eventuate Tram inserta los eventos en una tabla `OUTBOX` dentro de la transacción ACID y los publica tras el commit.
- P: ¿Cómo se reparte la responsabilidad de publicar eventos entre aggregate y service? / R: El aggregate genera los eventos cuando cambia de estado y los devuelve al service (o los acumula en un campo), y el service, con la API de mensajería inyectada, los publica.
- P: ¿Qué es un pending state en el aggregate Order? / R: Un estado intermedio (p. ej. `APPROVAL_PENDING`) que actúa como contramedida de bloqueo semántico para aislar las sagas mientras colaboran varios servicios.
- P: ¿Por qué `OrderService` es más complejo que `KitchenService`? / R: Porque la mayoría de sus métodos inician sagas que orquestan la creación o actualización del Order, ya que los Orders deben ser consistentes con datos de otros servicios; Kitchen Service solo participa en sagas.

## Preguntas de autoevaluación

- P: ¿Qué patrón de DDD resuelve a la vez el problema de las referencias que cruzan fronteras de servicio y el de las restricciones transaccionales? / R: El patrón Aggregate: las referencias entre aggregates se hacen por clave primaria (ninguna cruza servicios) y una transacción solo crea o actualiza un aggregate, quedando dentro de un servicio. (Lo que necesitas saber; 5.2)
- P: ¿Por qué un modelo de dominio tradicional con fronteras difusas dificulta hacer cumplir las invariantes? / R: Porque no especifica las fronteras de cada objeto de negocio; actualizar directamente parte de un objeto puede violar reglas (ej. Sam y Mary reducen líneas del mismo Order por separado y el total viola el mínimo). (5.2.1)
- P: ¿Qué se hace cuando una operación afecta a varios aggregates, si una transacción solo puede actualizar uno? / R: Se usa una saga, donde cada paso crea o actualiza exactamente un aggregate. (5.2.3)
- P: ¿Qué desventajas tendría agrandar un aggregate, p. ej. haciendo Order parte del aggregate Consumer? / R: Reduce la escalabilidad (se serializan actualizaciones de pedidos distintos del mismo cliente) y dificulta la descomposición (la lógica de Orders y Consumers quedaría en el mismo servicio). (5.2.4)
- P: ¿Para qué escenarios sirve que un aggregate publique domain events? / R: Sagas por coreografía, CQRS (réplicas), notificar a otras aplicaciones vía webhook o broker, actualizar componentes (WebSocket, ElasticSearch), notificaciones a usuarios, monitorización y análisis de comportamiento. (5.3.1)
- P: ¿Qué distingue al aggregate Ticket de Kitchen Service respecto al aggregate Order? / R: Ticket representa la vista del pedido desde la cocina (sin datos de consumidor, entrega ni pago), su ID lo suministra Order Service y referencia al restaurante por `restaurantId`. (5.4.1)
- P: ¿En qué se diferencia la lógica de negocio de un microservicio respecto a la de un monolito? / R: El modelo se organiza como aggregates DDD, las referencias entre aggregates son por clave primaria, una transacción solo crea o actualiza un aggregate y los aggregates publican domain events al cambiar de estado. (5.5.2)
- P: ¿Qué adelanta el capítulo sobre el capítulo 6 respecto a la publicación de eventos? / R: Que aquí el código de publicación de eventos está entrelazado con la lógica de negocio, mientras que el capítulo 6 verá event sourcing, donde la generación de eventos es parte integral de la lógica. (5.5.2)

## Puntos a dominar

- Distinguir cuándo usar Transaction script (lógica simple) y cuándo Domain model (lógica compleja).
- Explicar qué es un aggregate, su entidad raíz y su papel como frontera de consistencia.
- Recitar y justificar las tres reglas de los aggregates (solo la raíz, claves primarias, una transacción por aggregate).
- Argumentar el criterio de granularidad: aggregates lo más finos posible salvo necesidad de atomicidad.
- Identificar los bloques tácticos de DDD: Entity, Value object, Factory, Repository, Service, Aggregate.
- Describir el reparto de responsabilidades aggregate/service para generar y publicar domain events.
- Explicar por qué la publicación fiable exige mensajería transaccional (tabla OUTBOX de Eventuate Tram).
- Reconocer los tres pasos del event storming y los tipos de nota (eventos, comandos, sistemas externos, aggregates).
- Comparar los roles de Kitchen Service (participa en sagas) y Order Service (inicia sagas).
