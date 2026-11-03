# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 2 — Decomposition strategies (Estrategias de descomposición)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo responde la pregunta central de la arquitectura de microservicios: cómo descomponer funcionalmente una aplicación en servicios. La tesis es que los servicios deben organizarse en torno a conceptos de negocio, no a conceptos técnicos. Richardson primero sitúa la arquitectura de microservicios dentro de los conceptos generales de arquitectura de software y luego describe un proceso de tres pasos para definirla a partir de los requisitos.

Sales sabiendo definir una arquitectura de microservicios aplicando dos patrones de descomposición —Decompose by business capability y Decompose by subdomain— apoyados en dos principios de diseño orientado a objetos (SRP y CCP). También aprendes a usar ideas de domain-driven design (DDD), en especial subdomains y bounded contexts, para eliminar las god classes, clases infladas que se usan en toda la aplicación y crean dependencias enredadas que impiden la descomposición.

Finalmente se exponen los obstáculos a la descomposición (latencia de red, disponibilidad reducida por comunicación síncrona, consistencia de datos, vistas consistentes y god classes) y cómo abordarlos, muchos remitiendo a capítulos posteriores (IPC en el 3, sagas en el 4, CQRS en el 7, API gateway en el 8).

## El ejemplo que recorre el capítulo

El hilo conductor es FTGO, la aplicación de entrega de comida. Se usa para ilustrar una posible arquitectura de microservicios (Order Service, Restaurant Service, Kitchen Service, Delivery Service, Consumer Service, Accounting Service, Notification Service, Courier Service) y, sobre todo, cómo la clase `Order` sería una god class si hubiera un único modelo de dominio, y cómo DDD resuelve el problema dándole a cada servicio su propia versión de `Order`.

## ¿Qué es exactamente la arquitectura de microservicios?

La arquitectura de software es la estructura de alto nivel de una aplicación: sus partes y las dependencias entre ellas. Richardson cita la definición de Len Bass y colegas del Software Engineering Institute: "the set of structures needed to reason about the system" (PDF p. 65), compuesta por elementos de software, relaciones entre ellos y propiedades de ambos. La descomposición importa porque facilita la división del trabajo y del conocimiento, y define cómo interactúan los elementos. Importa además porque determina las *-ilities* o atributos de calidad: tradicionalmente escalabilidad, fiabilidad y seguridad, y hoy también la entrega rápida y segura de software.

El modelo de vistas 4+1 de Krutchen describe una arquitectura desde cuatro perspectivas:

- **Logical view**: lo que crean los desarrolladores (clases y paquetes).
- **Implementation view**: la salida del sistema de build (módulos como JAR, componentes como WAR o JAR ejecutables).
- **Process view**: los componentes en ejecución (procesos y su comunicación entre procesos).
- **Deployment view**: cómo se mapean los procesos a máquinas (físicas o virtuales) y el networking entre ellas.

El +1 son los *scenarios*, que animan las vistas mostrando cómo colaboran los elementos para atender una petición. La arquitectura importa porque, aunque los requisitos funcionales se pueden implementar con casi cualquier arquitectura (incluso un big ball of mud), son los requisitos de calidad de servicio (*quality attributes*) los que dependen de la arquitectura elegida.

### Estilos arquitectónicos

Un estilo arquitectónico define una familia de sistemas mediante un patrón de organización estructural, con un vocabulario limitado de componentes y conectores y restricciones sobre cómo combinarlos (Garlan y Shaw).

- **Layered**: organiza los elementos en capas con dependencias restringidas. El clásico three-tier (presentation, business logic, persistence) aplica este estilo a la logical view. Sus inconvenientes: una única capa de presentación, una única capa de persistencia, y que define la lógica de negocio como dependiente de la persistencia (cuando en realidad las dependencias deberían invertirse: la lógica define interfaces de repositorio que la persistencia implementa mediante DAOs).
- **Hexagonal**: coloca la lógica de negocio en el centro, con *inbound adapters* que gestionan peticiones externas invocando un *inbound port*, y *outbound adapters* que implementan un *outbound port* para invocar sistemas externos. Beneficio clave: la lógica de negocio no depende de los adapters; son los adapters los que dependen de ella, lo que desacopla la lógica de la presentación y el acceso a datos y facilita probarla aislada.

### Microservicios como estilo arquitectónico

Tanto el monolito como los microservicios son estilos que organizan la *implementation view*:

- **Pattern: Monolithic architecture** — estructurar la aplicación como un único componente ejecutable/desplegable.
- **Pattern: Microservice architecture** — estructurar la aplicación como una colección de servicios débilmente acoplados y desplegables de forma independiente.

Cada servicio suele tener internamente una arquitectura hexagonal. Un **servicio** es un componente autónomo, desplegable de forma independiente, con una API que encapsula su implementación. La API consta de *commands* (como `createOrder()`, que actualizan datos), *queries* (como `findOrderById()`, que recuperan datos) y *events* (como `OrderCreated`) a los que los clientes se suscriben. A diferencia del monolito, nadie puede eludir la API, lo que fuerza la modularidad.

El **loose coupling** implica que toda interacción ocurre vía la API y prohíbe que los servicios se comuniquen a través de una base de datos compartida: los datos persistentes deben tratarse como campos privados de una clase. Ello permite cambiar el esquema sin coordinarse con otros equipos y mejora el aislamiento en runtime (p. ej., evita bloqueos de base de datos entre servicios); el inconveniente es que mantener la consistencia y consultar entre servicios se vuelve más complejo.

Sobre las **bibliotecas compartidas**: úsalas solo para funcionalidad que es poco probable que cambie (p. ej. una clase `Money`). Empaquetar funcionalidad que cambia (como la gestión de `Order`) en una librería compartida introduce acoplamiento, porque obligaría a reconstruir y redesplegar varios servicios a la vez. Por último, el **tamaño del servicio es irrelevante**: la meta es un servicio que pueda desarrollar un equipo pequeño con mínimo tiempo de entrega y mínima colaboración con otros equipos; si cambia constantemente por cambios en otros servicios, podrías tener un *distributed monolith*.

## Definir la arquitectura de microservicios de una aplicación

Proceso de tres pasos (más arte que ciencia, iterativo y creativo):

1. **Identificar las operaciones del sistema**: destilar los requisitos en *system operations* abstractas (no en tecnologías IPC concretas), que son *commands* o *queries*.
2. **Determinar la descomposición en servicios**: con Decompose by business capability o Decompose by subdomain.
3. **Definir las APIs de los servicios y sus colaboraciones**: asignar cada operación a un servicio y determinar las operaciones adicionales que se necesitan para colaborar.

### Identificar las operaciones del sistema

Se usa un proceso de dos pasos inspirado en Craig Larman (*Applying UML and Patterns*): primero crear un *high-level domain model* (derivado sobre todo de los sustantivos de las user stories) y luego definir las operaciones del sistema (derivadas de los verbos). El modelo de dominio de FTGO incluye clases como `Consumer`, `Order`, `OrderLineItem`, `DeliveryInfo`, `Restaurant`, `MenuItem`, `Courier`, `Address` y `Location`.

Cada command se especifica con parámetros, valor de retorno, precondiciones y postcondiciones. Por ejemplo `createOrder()` tiene como precondición que el consumidor existe y puede pedir, y como postcondición que se autorizó la tarjeta y se creó un pedido en estado `PENDING_ACCEPTANCE`. También hay queries relevantes como `findAvailableRestaurants(deliveryAddress, deliveryTime)` —arquitectónicamente significativa por implicar geosearch y rendimiento crítico— y `findRestaurantMenu(id)`.

### Decompose by business capability

Una *business capability* es algo que el negocio hace para generar valor; captura *qué* hace la organización y es estable, a diferencia del *cómo*, que cambia (ejemplo del depósito de cheques: teller → ATM → smartphone). Se identifican analizando el propósito, la estructura y los procesos de negocio, y pueden descomponerse en sub-capacidades. En FTGO: Supplier management (Courier / Restaurant information management), Consumer management, Order taking and fulfillment (Order management, Restaurant order management, Logistics con Courier availability y Delivery management), Accounting (Consumer / Restaurant / Courier). Luego se define un servicio por capacidad o grupo de capacidades relacionadas; el nivel de la jerarquía a mapear es subjetivo. Ventaja: como las capacidades son estables, la arquitectura resultante también lo es.

### Decompose by subdomain

DDD (Eric Evans) se centra en un modelo de dominio orientado a objetos y define el *Ubiquitous Language*. Frente al modelado empresarial tradicional de un único modelo, DDD define múltiples modelos, cada uno con un alcance explícito. Un *subdomain* es una parte del dominio (el espacio del problema); se identifican como las capacidades de negocio, por áreas de experiencia (en FTGO: Order taking, Order management, Kitchen management, Delivery, Financials). El alcance de un modelo de dominio es un *bounded context*, que en microservicios corresponde a un servicio (o varios). DDD y microservicios se alinean casi perfectamente, incluida la idea de equipos autónomos que poseen cada modelo.

### Guías de descomposición (SRP y CCP)

Dos principios de Robert C. Martin:

- **Single Responsibility Principle (SRP)**: "A class should have only one reason to change" (PDF p. 86). Aplicado a microservicios, crea servicios pequeños, cohesivos, con una sola responsabilidad.
- **Common Closure Principle (CCP)**: las clases que cambian por la misma razón deben estar juntas. Aplicado a microservicios, empaqueta en el mismo servicio los componentes que cambian por la misma razón, minimizando el número de servicios a cambiar y desplegar. CCP es el antídoto contra el distributed monolith.

### Obstáculos a la descomposición

- **Network latency**: demasiados round-trips; mitigable con APIs batch o combinando servicios.
- **Comunicación síncrona reduce disponibilidad**: invocar servicios vía REST síncrono hace que uno no pueda operar si otro cae; a menudo es mejor la mensajería asíncrona (cap. 3).
- **Consistencia de datos entre servicios**: evitar el commit en dos fases; usar *sagas* (secuencias de transacciones locales coordinadas por mensajería, eventualmente consistentes; cap. 4).
- **Obtener una vista consistente de los datos**: no se puede una vista globalmente consistente entre bases; si se necesita, los datos deben residir en un solo servicio (raramente un problema en la práctica).
- **God classes**: clases infladas con lógica de muchos aspectos. `Order` sería una god class en FTGO. Empaquetarla en una librería con base de datos central genera acoplamiento; encapsularla en un Order Service la vuelve anémica. La solución es aplicar DDD y dar a cada servicio su propio modelo de `Order`: en Delivery Service la vista es mínima (y se llama `Delivery`), en Kitchen Service se llama `Ticket`, y Order Service tiene la vista más compleja pero aún más simple que la original.

### Definir las APIs de los servicios

Una operación de API existe o bien porque corresponde a una operación del sistema (invocada por clientes externos u otros servicios) o bien para soportar colaboración entre servicios. Se asigna cada operación a un servicio (a veces al que necesita la información, como `noteUpdatedLocation()` que interesa a Delivery Service) y se determinan las APIs adicionales de colaboración. Por ejemplo, `createOrder()` en Order Service invoca a Consumer Service (`verifyConsumerDetails()`), Restaurant Service (`verifyOrderDetails()`), Kitchen Service (`createTicket()`) y Accounting Service (`authorizeCard()`); `acceptOrder()` en Kitchen Service invoca a Delivery Service (`scheduleDelivery()`). La arquitectura resultante es abstracta: aún no se elige IPC. Capítulos posteriores profundizan: IPC (3), sagas (4), CQRS y API composition (7), API gateway (8).

## Ideas clave

- La arquitectura determina las *-ilities* (mantenibilidad, testabilidad, desplegabilidad), que impactan directamente en la velocidad de desarrollo.
- Los microservicios son un estilo arquitectónico que organiza la implementation view como servicios débilmente acoplados y desplegables de forma independiente; cada servicio suele ser hexagonal internamente.
- Los servicios se organizan en torno a conceptos de negocio (business capabilities o subdomains), no técnicos.
- El loose coupling exige comunicación solo vía API y prohíbe compartir base de datos entre servicios.
- El tamaño del servicio es poco importante; lo que importa es que lo pueda desarrollar un equipo pequeño con mínima colaboración externa.
- SRP y CCP, de Robert C. Martin, guían la descomposición y evitan el distributed monolith.
- Los obstáculos (latencia, disponibilidad, consistencia, vistas consistentes, god classes) se abordan con APIs batch, mensajería asíncrona, sagas y DDD.
- Aplicar DDD para dar a cada servicio su propio modelo de dominio elimina las god classes como la `Order` de FTGO.
