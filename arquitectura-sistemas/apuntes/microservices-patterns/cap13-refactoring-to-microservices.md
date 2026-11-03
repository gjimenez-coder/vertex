# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 13 — Refactoring to microservices (Refactorización hacia microservicios)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber
El capítulo explica cómo migrar una aplicación monolítica grande y compleja a una arquitectura de microservicios sin reescribirla desde cero. La tesis central es que debe hacerse de forma incremental, construyendo una *strangler application* (aplicación estranguladora): una nueva aplicación de microservicios que crece alrededor del monolito, implementando nuevas funcionalidades como servicios y extrayendo capacidades existentes, hasta que el monolito se reduce y acaba desapareciendo o convirtiéndose en un microservicio más.

Antes de migrar, hay que asegurarse de que los problemas de entrega (lentitud, releases con errores, falta de escalabilidad) se deben a haber superado la arquitectura y no a un mal proceso de desarrollo; a veces basta con introducir pruebas automatizadas. La migración solo tiene sentido si resuelve un problema de negocio significativo, porque desvía recursos del desarrollo de funcionalidades.

Sales sabiendo las tres estrategias para estrangular el monolito (implementar nuevas funciones como servicios, separar presentación del backend y extraer capacidades de negocio), cómo diseñar el *integration glue* que conecta servicio y monolito, cómo mantener la consistencia de datos con sagas, cómo manejar la seguridad durante la transición, y dos ejemplos concretos: Delayed Order Service (nueva funcionalidad) y Delivery Service (extraído del monolito).

## El ejemplo que recorre el capítulo
El hilo conductor es la aplicación FTGO (reparto de comida) y el equipo de Mary, atrapados en el "infierno monolítico". El capítulo usa dos servicios como casos: Delayed Delivery/Order Service, que notifica entregas con retraso o no realizables, y Delivery Service, que extrae la gestión de entregas enredada dentro de la gestión de pedidos del monolito.

## Visión general de la refactorización a microservicios
El monolito FTGO sufre un caso clásico de infierno monolítico. Los beneficios de los microservicios (mantenibilidad, testabilidad, desplegabilidad, escalabilidad, aislamiento de fallos, evolución del stack) justifican la migración solo si resuelve un problema de negocio real como entrega lenta, releases con errores o mala escalabilidad.

La lección más importante acumulada en décadas de modernización de aplicaciones es no hacer un *big bang rewrite*. Reescribir desde cero es muy arriesgado: duplicas funcionalidad durante meses o años, el monolito sigue siendo un objetivo en movimiento y puedes reimplementar funciones ya innecesarias. Como se atribuye a Martin Fowler, "the only thing a Big Bang rewrite guarantees is a Big Bang!" (PDF p. 461).

En su lugar, se refactoriza de forma incremental construyendo la strangler application, estrategia que Fowler llama patrón *Strangler application* (PDF p. 462). El nombre viene de la higuera estranguladora de las selvas. El proceso tarda meses o años (a Amazon le llevó un par de años) y en sistemas muy grandes puede no completarse nunca: si el monolito deja de ser un obstáculo, se puede dejar como está.

Principios clave de la sección:
- **Demostrar valor pronto y a menudo**: el retorno es inmediato, a diferencia del big bang. Se migran primero las áreas de alto valor (p. ej. el algoritmo de programación de entregas) y se mantiene así el apoyo del negocio.
- **Minimizar los cambios al monolito**: los cambios amplios son costosos, lentos y arriesgados. Se reducen replicando datos del servicio extraído de vuelta a la BD del monolito y secuenciando con cuidado las extracciones.
- **No necesitas aún toda la infraestructura de despliegue**: lo único imprescindible es un pipeline con pruebas automatizadas. Con pocos servicios basta incluso un archivo de configuración fijo para el descubrimiento. Las decisiones costosas de infraestructura se difieren hasta tener experiencia real.

## Estrategias para refactorizar el monolito
Hay tres estrategias principales para estrangular el monolito:
1. Implementar nuevas funciones como servicios.
2. Separar la capa de presentación del backend.
3. Romper el monolito extrayendo funcionalidad en servicios.

La primera frena el crecimiento del monolito y demuestra valor rápido; la tercera es la que realmente migra funcionalidad y siempre se acaba usando.

**Implementar nuevas funciones como servicios.** Aplica la Ley de los Agujeros: "if you find yourself in a hole, stop digging" (PDF p. 463). No añadas código nuevo al monolito; implementa las funciones nuevas como servicios. La integración con el monolito requiere dos elementos: un *API gateway* que enruta las peticiones nuevas al servicio y las antiguas al monolito, y el *integration glue code* (adaptadores en monolito y servicio que usan IPC como REST o eventos de dominio). No toda función puede ser servicio: si es demasiado pequeña o está muy acoplada al monolito (problemas de rendimiento por IPC excesiva o de consistencia), conviene implementarla en el monolito y extraerla después junto a funciones relacionadas.

**Separar presentación del backend.** Una app empresarial típica tiene tres capas: lógica de presentación, lógica de negocio y lógica de acceso a datos. La frontera limpia entre presentación y negocio (una API de fachada de grano grueso) permite partir el monolito en dos aplicaciones desplegables de forma independiente. Beneficios: desarrollar, desplegar y escalar ambas por separado, iterar rápido en la UI y hacer A/B testing, y exponer una API remota reutilizable por servicios futuros. Es solo una solución parcial: al menos una de las dos partes seguirá siendo un monolito inmanejable.

**Extraer capacidades de negocio en servicios.** La funcionalidad a extraer es un corte vertical del monolito: adaptadores de entrada (endpoints de API), lógica de dominio, adaptadores de salida (acceso a datos) y el esquema de BD. El API gateway enruta las peticiones de esa capacidad al servicio. Extraer es difícil y lento (el código del monolito suele estar desordenado), por lo que hay que priorizar las partes de mayor valor. Dos desafíos: dividir el modelo de dominio y refactorizar la base de datos.

**Dividir el modelo de dominio.** Hay que eliminar las referencias entre objetos que cruzarían fronteras de servicio (una instancia de servicio es un proceso). La solución es pensar en términos de agregados DDD, que se referencian por clave primaria: p. ej., la referencia de `Order` a `Restaurant` se sustituye por un campo `restaurantId`. El reto mayor es extraer funcionalidad embebida en *god classes* (como `Order`, que mezcla gestión de pedidos y de entregas); extraer la gestión de entregas implica sacar una entidad `Delivery` de `Order`.

**Refactorizar la base de datos.** Al dividir una entidad se divide su tabla y se mueve al servicio (p. ej., partir `ORDERS` y crear `DELIVERY`). El libro *Refactoring Databases* (Ambler y Sadalage, Addison-Wesley, 2011) describe el refactor *Split Table* y la idea de replicar datos para migrar clientes de forma incremental.

**Replicar datos para evitar cambios amplios.** En vez de cambiar todos los sitios que referencian campos movidos, se preserva la estructura original durante una transición: los campos relacionados con la entrega en `Order` quedan de solo lectura y se mantienen al día replicando datos desde Delivery Service hacia el monolito. Así solo hay que cambiar los puntos que *actualizan* esos campos.

**Qué servicios extraer y cuándo.** Conviene empezar con un esfuerzo acotado en el tiempo (un par de semanas) para definir la arquitectura destino, sabiendo que no es inmutable. Dos estrategias de secuenciación: congelar el desarrollo del monolito y extraer servicios bajo demanda (fuerza la ruptura, pero guiada por el corto plazo), o un enfoque planificado que clasifica los módulos por el beneficio esperado. Un servicio es valioso de extraer si acelera el desarrollo, resuelve un problema de rendimiento/escalabilidad/fiabilidad, o habilita la extracción de otros servicios.

## Diseñar la colaboración entre el servicio y el monolito
Un servicio rara vez es autónomo: suele necesitar datos u operaciones del monolito y viceversa. Dos preocupaciones: mantener la consistencia de datos (al extraer un servicio partes transacciones ACID, a veces hay que usar sagas) y el diseño del *integration glue*, formado por adaptadores en servicio y monolito que se comunican por algún IPC. Delayed Delivery Service, por ejemplo, usa REST para recuperar la información de contacto del cliente y eventos de dominio para seguir el estado de los pedidos.

**Diseño del integration glue.** Primero se decide qué API ofrece a la lógica de dominio, encapsulando el IPC tras una interfaz. Si se consultan datos, se usa un repositorio (p. ej. `CustomerContactInfoRepository`); si se invocan operaciones, una interfaz de servicio (p. ej. `DeliveryService` con `scheduleDelivery`, `rescheduleDelivery`, `cancelDelivery`). Para consultar datos del otro lado hay dos opciones: invocar su API de consulta (simple, pero potencialmente ineficiente y con menor disponibilidad por ser IPC síncrona) o mantener una réplica tipo vista CQRS que se actualiza suscribiéndose a eventos de dominio (consultas eficientes, pero más compleja). Para actualizaciones que deben mantener consistencia se usa mensajería transaccional (p. ej. Eventuate Tram); en casos complejos, una saga.

**Anti-corruption layer (ACL).** Como el servicio nuevo modela conceptos de forma distinta y más limpia que el monolito, se implementa una ACL: una capa que traduce entre los dos modelos de dominio para evitar que el modelo heredado contamine al del servicio. La usan tanto el servicio como el monolito, en adaptadores REST y en manejadores de eventos (que traducen los eventos del publicador al modelo del suscriptor).

**Cómo el monolito publica y consume eventos.** Para publicar, dos vías: insertar llamadas a la API de publicación en cada punto que cambia una entidad (difícil y propenso a errores; los stored procedures lo complican), o publicar a nivel de BD con *transaction log tailing* o *polling* (no cambia el monolito, pero publica eventos de cambios de tablas, no de entidades de negocio). Consumir suele ser más fácil con un framework como Eventuate Tram; si el monolito está en un lenguaje sin cliente de broker, se escribe una pequeña app "helper".

**Mantener la consistencia de datos con sagas.** Al extraer un servicio quizá haya que convertir comandos del monolito (p. ej. `createOrder()`) en sagas. El problema es que las sagas requieren transacciones compensatorias, y añadirlas al monolito (p. ej. un estado `APPROVAL_PENDING` como *semantic lock* en `Order`) puede exigir cambios amplios, costosos y arriesgados. Términos clave de sagas (cap. 4): compensating transaction, countermeasure, semantic lock, compensatable transaction, pivot transaction y retriable transaction.

Sin embargo, el monolito solo necesita transacciones compensatorias si las transacciones posteriores pueden fallar. Si cada transacción del monolito es *pivot* o *retriable*, nunca compensa. Extraer Kitchen Service obliga a compensar en el monolito, pero extraer Order Service no: su transacción del monolito queda como pivot. Secuenciando con cuidado (p. ej. extraer primero Order Service, luego Consumer Service y después Kitchen Service y Accounting Service) se consigue que la transacción del monolito sea siempre pivot o retriable, evitando compensaciones complejas en él.

**Autenticación y autorización.** Durante la transición hay que soportar a la vez el mecanismo del monolito (sesión en memoria, identidad vía thread local) y el basado en tokens JWT de los servicios. La solución requiere un solo cambio pequeño en el login handler: devolver además una cookie `USERINFO` (un JWT con ID y roles). El navegador la envía en cada petición; el API gateway valida la cookie y la pasa en el header `Authorization` al invocar servicios. Así cada servicio accede a la identidad del usuario sin extraer todavía la gestión de usuarios.

## Ejemplo 1: nueva función como servicio — Delayed Order Service
FTGO gestiona mal las entregas fallidas: el cliente recibe la mala noticia tarde. La función nueva debe notificar al cliente cuando su pedido no llegará a tiempo o no podrá recogerse antes de que cierre el restaurante, avisar a atención al cliente para compensar proactivamente y registrar estadísticas de entrega. En vez de ampliar el monolito ("stop digging"), se implementa como servicio: Delayed Order Service.

El servicio expone una única consulta `getDelayedOrders()`; el API gateway le enruta esa petición y manda el resto al monolito. Su modelo de dominio incluye `DelayedOrderNotification`, `Order` y `Restaurant`, pero no posee `Order` ni `Restaurant`: esos datos se replican del monolito, y la información de contacto del cliente se consulta en él. El `DelayedOrderService` se invoca periódicamente por un temporizador para detectar pedidos que no llegarán a tiempo.

Integration glue: la información de contacto se obtiene vía `CustomerContactInfoRepository` (implementado por un proxy que llama al endpoint REST `getCustomerContactInfo()` del monolito), porque es poco frecuente y de poco volumen. En cambio, consultar todos los pedidos y horarios abiertos sería ineficiente, así que el servicio mantiene réplicas de `Order` y `Restaurant` suscribiéndose a eventos del monolito (publicados como eventos de alto nivel o por transaction log tailing). La réplica solo guarda un subconjunto de columnas de `ORDERS` y `RESTAURANT`.

## Ejemplo 2: romper el monolito — extraer Delivery Service
La gestión de entregas es de lo más antiguo de FTGO y está enredada con la gestión de pedidos: gran parte del código vive en `OrderService` y no hay entidad `Delivery` explícita (sus datos están en `Order`, con campos como `scheduledPickupTime` y `scheduledDeliveryTime`). Para acelerar un nuevo algoritmo de rutas se extrae un Delivery Service. La primera iteración no expone API pública: solo la invoca el monolito.

Hay que decidir qué comportamiento y datos se mueven, y qué APIs se exponen en cada sentido. Tras identificar las entidades y campos de la gestión de entregas (muchos compartidos con el monolito), el servicio se queda con los planes del *Courier* y los campos `scheduledPickupTime`/`scheduledDeliveryTime` del `Order`; `Courier.location` y `Courier.availability` se dejan en el monolito para minimizar el cambio. Su modelo de dominio tiene clases como `Delivery` y `Courier`, con `DeliveryServiceImpl` como punto de entrada (implementa `DeliveryService` y `CourierService`); gran parte es código copiado del monolito. Un lenguaje de tipado estático ayuda a romper dependencias.

Integration glue: en lugar de reaccionar a eventos `Order`, Delivery Service ofrece una API de notificaciones con tres mensajes (`ScheduleDelivery`, `ReviseDelivery`, `CancelDelivery`), de modo que no necesita conocer el ciclo de vida del pedido. El monolito le replica los datos de `Courier` (location/availability) publicando eventos `CourierLocationUpdated` y `CourierAvailabilityUpdated`. A la inversa, el servicio replica de vuelta al monolito publicando `CourierPlanUpdated` y `DeliveryScheduleUpdate`, evitando cambiar el esquema del monolito.

Cambiar el monolito en tres pasos: (1) encapsular la gestión de entregas tras una interfaz `DeliveryService` de grano grueso (`schedule`, `reschedule`, `cancel`); (2) cambiar todos los puntos que invocan la gestión de entregas para usar esa interfaz (lo más laborioso); (3) implementar la interfaz con un proxy que envía mensajes al servicio, usando un *feature toggle* (`FeatureToggleBasedDeliveryServiceImpl`) para alternar dinámicamente entre la implementación antigua y Delivery Service, lo que reduce el riesgo del despliegue. Después pueden extraerse Order History Service, Order Service, Consumer Service, Kitchen Service, etc.

## Ideas clave
- Antes de migrar, confirma que los problemas de entrega vienen de haber superado la arquitectura monolítica y no de un mal proceso de desarrollo.
- Migra de forma incremental con una *strangler application*; evita el *big bang rewrite* y demuestra valor pronto y a menudo para conservar el apoyo del negocio.
- Tres estrategias: implementar nuevas funciones como servicios, separar presentación del backend y extraer capacidades de negocio (esta última es la clave de la migración).
- Extraer un servicio implica dividir el modelo de dominio (referencias por clave primaria al estilo agregados DDD) y refactorizar la base de datos.
- Replicar los datos movidos de vuelta al monolito minimiza los cambios necesarios en su código y esquema.
- El *integration glue* conecta servicio y monolito mediante adaptadores e IPC, y debe usar una *anti-corruption layer* para no contaminar el modelo del servicio.
- Las sagas con el monolito son costosas si exigen transacciones compensatorias; secuencia las extracciones para que las transacciones del monolito sean pivot o retriable.
- Durante la transición, un cambio mínimo en el login handler (cookie `USERINFO` con JWT) permite soportar a la vez la seguridad por sesión del monolito y la basada en tokens de los servicios.
