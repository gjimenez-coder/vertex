# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 10 — Testing microservices: Part 2 (Probar microservicios: Parte 2)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo continúa el ascenso por la pirámide de pruebas iniciada en el capítulo anterior. Tras los tests unitarios (la base), aquí se cubren los tres niveles superiores: tests de integración, tests de componente y tests end-to-end. La tesis central es que probar la comunicación entre servicios arrancando todos ellos (end-to-end) es lento, frágil y costoso, por lo que debe reducirse al mínimo; en su lugar se emplean estrategias más baratas que verifican lo mismo con menos piezas en marcha.

Sales sabiendo cómo escribir tests de integración que verifican que un servicio interactúa correctamente con infraestructura (bases de datos) y con otros servicios, usando el testing de contratos dirigido por el consumidor (consumer-driven contract testing). También aprendes a escribir tests de componente, que son los tests de aceptación de un servicio probado en aislamiento con stubs para sus dependencias, y a decidir cuándo y cómo hacer tests end-to-end de la aplicación completa.

El hilo conductor es la aplicación FTGO, en particular Order Service y sus interacciones con API Gateway, Order History Service y Kitchen Service a través de REST, publish/subscribe y request/response asíncrono.

## El ejemplo que recorre el capítulo

Order Service es la clase/servicio bajo prueba. Su API REST la consume API Gateway; sus eventos de dominio los consume Order History Service; persiste Orders en MySQL con JPA; y envía comandos y consume respuestas de otros servicios como Kitchen Service (PDF p. 349). La estrategia no es probar servicios enteros, sino las clases adaptador individuales que implementan cada forma de comunicación.

## Writing integration tests (Escribir tests de integración)

Los tests de integración son la capa por encima de los unitarios y verifican que un servicio se comunica con sus dependencias, pero sin arrancar los servicios (PDF p. 350). Se apoyan en dos estrategias: probar cada adaptador del servicio por separado (en lugar del servicio completo) y usar contratos para las interacciones entre servicios de aplicación. Un contrato es un ejemplo concreto de interacción entre un par de servicios; su estructura depende del estilo de interacción:

| Estilo de interacción | Consumidor | Proveedor | Contrato |
| --- | --- | --- | --- |
| REST, request/response | API Gateway | Order Service | petición y respuesta HTTP |
| Publish/subscribe | Order History Service | Order Service | evento de dominio |
| Request/response asíncrono | Order Service | Kitchen Service | mensaje de comando y mensaje de respuesta |

Un contrato consta de un mensaje (publish/subscribe) o dos (request/response). Se usa para probar ambos lados: los tests del consumidor usan el contrato para configurar stubs que simulan al proveedor; los del proveedor lo usan para probar sus adaptadores con mocks de sus dependencias (PDF p. 351).

### Persistence integration tests

Verifican que la lógica de acceso a base de datos funciona. En Order Service significa probar los repositorios JPA como `OrderRepository`. Cada fase: setup (crear el esquema e inicializar un estado conocido, quizá abrir transacción), execute (operación de BD), verify (aserciones sobre el estado y los objetos) y un teardown opcional. El test `shouldSaveAndLoadOrder()` ejecuta dos transacciones: la primera guarda un Order nuevo y la segunda lo carga y verifica sus campos (PDF p. 352). Una solución efectiva para aprovisionar la base de datos en estos tests es ejecutar una instancia con Docker.

### REST-based request/response

El cliente y el servicio REST deben acordar los endpoints y la estructura de peticiones/respuestas. Se usa Spring Cloud Contract: en el lado consumidor, los contratos configuran un servidor stub HTTP (WireMock) que simula a Order Service; en el lado proveedor, Spring Cloud Contract genera tests que prueban los controladores con Rest Assured Mock MVC (PDF p. 353). Un contrato REST especifica método, URL y cabeceras de la petición, y código de estado, cabeceras y cuerpo de la respuesta (PDF p. 354). La clase base `HttpBase` crea los controladores con mocks y configura esos mocks para devolver los valores que producen la respuesta esperada. En el consumidor, `OrderServiceProxyIntegrationTest` se anota con `@AutoConfigureStubRunner` para arrancar WireMock en un puerto aleatorio y verifica que `OrderServiceProxy` devuelve los valores del contrato o lanza la excepción esperada (`shouldVerifyExistingCustomer`, `shouldFailToFindMissingOrder`).

### Publish/subscribe

Verifica que el publicador y los consumidores acuerdan el canal y la estructura de los eventos de dominio. Cada contrato especifica un evento de dominio, con `label` (usado por el test del consumidor para disparar la publicación) y `triggeredBy` (método de la superclase que el test generado invoca para disparar la publicación) (PDF p. 358). En el proveedor, los tests extienden `MessagingBase`, que configura `OrderDomainEventPublisher` con stubs de mensajería en memoria y define métodos como `orderCreated()`. En el consumidor, `OrderHistoryEventHandlersTest` crea `OrderHistoryEventHandlers` con un `OrderHistoryDao` mockeado; `shouldHandleOrderCreatedEvent()` publica el evento con Spring Cloud Contract y verifica que se invocó `orderHistoryDao.addOrder()`.

### Asynchronous request/response

Las dos partes son el requestor (envía el comando) y el replier (procesa y responde); deben acordar el canal del comando y la estructura del comando y la respuesta. El contrato especifica un mensaje de entrada y uno de salida, con la nomenclatura desde la perspectiva del proveedor: `messageFrom` indica el canal de lectura y `sentTo` el canal de respuesta (PDF p. 361). Ejemplo: un comando `CreateTicket` al canal `kitchenService` y una respuesta de éxito al canal de respuesta de `CreateOrderSaga`. En el consumidor, `KitchenServiceProxyIntegrationTest` envía el comando con `KitchenServiceProxy` usando `SagaMessagingTestHelper` y verifica la respuesta, con mensajería en memoria. En el proveedor, los tests prueban `KitchenServiceCommandHandler` con un `KitchenService` mockeado configurado para devolver valores que coincidan con el mensaje de salida del contrato (PDF p. 364).

## Developing component tests (Desarrollar tests de componente)

Los tests de componente son los tests de aceptación de un servicio: lo tratan como caja negra y verifican su comportamiento a través de su API, probándolo en aislamiento con stubs para sus dependencias (patrón *Service component test*). Están entre los de integración y los end-to-end, y son más fáciles de escribir y rápidos de ejecutar (PDF p. 365).

### Defining y writing acceptance tests

Los tests de aceptación describen el comportamiento externo visible desde la perspectiva de los clientes, derivados de historias de usuario. La historia "Place Order" se expande en escenarios con estructura given-when-then, donde los *given* son el setup, el *when* la ejecución y el *then*/*and* la verificación. En lugar de traducir a Java manualmente, se escriben con Gherkin (DSL de especificaciones ejecutables) y se ejecutan con Cucumber (PDF p. 367). La especificación consta de *features* (ej. Place Order, Cancel Order, Revise Order), cada una con nombre, *specification brief* (la historia de usuario) y escenarios. En Java se escribe una clase *step definition* cuyos métodos se anotan con `@Given`, `@When`, `@Then` o `@And`, cada anotación con una expresión regular que Cucumber compara con los pasos.

### Designing component tests

Hay un compromiso entre realismo, velocidad y simplicidad:

- In-process: ejecuta el servicio con stubs y mocks en memoria en la misma JVM que el test (con `@SpringBootTest`), usando una BD JDBC en memoria (H2, HSQLDB, Derby) y stubs de Eventuate Tram. Más simple y rápido, pero no prueba el servicio desplegable.
- Out-of-process: empaqueta el servicio en formato listo para producción (p. ej. imagen Docker) y lo ejecuta como proceso aparte, usando infraestructura real (MySQL, Apache Kafka) y stubs solo para los servicios de aplicación. Mejora la cobertura porque se acerca a lo desplegado, pero es más complejo, lento y potencialmente más frágil (PDF p. 369).

Para hacer stub de servicios en tests out-of-process se puede usar Spring Cloud Contract, aunque su enfoque es algo pesado (los JAR de contratos deben desplegarse en un repositorio Maven). Una opción más simple es configurar los stubs dentro del propio test, por ejemplo con el DSL de stubbing de WireMock para HTTP o stubs de mensajería para Eventuate Tram (PDF p. 370).

### Writing component tests for the FTGO Order Service

Se usa la estrategia out-of-process con el servicio corriendo como contenedor Docker. `OrderServiceComponentTest` se anota con `@RunWith(Cucumber.class)` y `@CucumberOptions` (ubicación de los features); no tiene métodos de test, sino que lee los features y usa `OrderServiceComponentTestStepDefinitions` para hacerlos ejecutables. Esta clase de step definitions se anota con `@ContextConfiguration` y define cada paso: `useCreditCard()` usa `SagaParticipantStubManager` para configurar el stub de Accounting Service con respuesta de éxito o fallo según la tarjeta; `placeOrder()` invoca `POST /orders` y guarda la respuesta; `theOrderShouldBe()` verifica el estado invocando `GET /orders/{orderId}` dentro de `eventually()`; `verifyEventPublished()` usa `MessageTracker` para comprobar que el evento de dominio esperado se publicó (PDF p. 371-373). Las pruebas se colocan en `src/component-test/java` y se ejecutan con `./gradlew componentTest`; el plugin Gradle Docker Compose arranca Order Service y su infraestructura antes de los tests y los detiene al terminar. El ciclo completo (construir, arrancar, probar, detener) tarda un par de minutos.

## Writing end-to-end tests (Escribir tests end-to-end)

Los tests end-to-end están en la cima de la pirámide y prueban la aplicación completa; son lentos, frágiles y costosos de desarrollar porque hay que desplegar múltiples servicios y su infraestructura, y es probable que alguno falle al desplegarse (PDF p. 375). Por ello deben minimizarse. La mejor estrategia son los *user journey tests*: un test que recorre el viaje de un usuario por el sistema (por ejemplo crear, revisar y cancelar un pedido en un solo test), lo que reduce el número de tests y acorta el tiempo de ejecución. Se escriben en un DSL de alto nivel comprensible por el negocio (Gherkin) y se ejecutan con Cucumber; a diferencia de los de aceptación, tienen varias acciones (múltiples pasos) en lugar de un solo *Then* (PDF p. 376). El módulo `ftgo-end-to-end-test` los implementa; el plugin Gradle Docker Compose arranca todos los servicios de la aplicación, y arrancar los contenedores y correr los tests tarda unos cuatro o cinco minutos, lo que refuerza que conviene centrarse en tests más abajo en la pirámide.

## Ideas clave

- Usa contratos (mensajes de ejemplo) para dirigir las pruebas de interacción entre servicios: en vez de arrancar ambos servicios y sus dependencias transitivas, verifica que los adaptadores de ambos lados cumplen el contrato.
- Los tests de integración prueban adaptadores individuales y no arrancan los servicios; cubren persistencia (repositorios JPA), REST, publish/subscribe y request/response asíncrono.
- Spring Cloud Contract genera los tests del lado proveedor y configura stubs (WireMock para HTTP, mensajería en memoria) en el lado consumidor a partir de los mismos contratos.
- Los tests de componente son tests de aceptación que prueban un servicio en aislamiento vía su API, usando stubs para sus dependencias; son más simples y rápidos que los end-to-end.
- Escribe escenarios en Gherkin (estructura given-when-then) y ejecútalos con Cucumber para tener especificaciones ejecutables sin traducción manual.
- Elige entre tests de componente in-process (rápidos, no prueban el desplegable) y out-of-process (más realistas con Docker, MySQL y Kafka, pero más lentos y frágiles).
- Minimiza los tests end-to-end y escribe *user journey tests* que recorran un viaje completo del usuario para reducir número de tests y sobrecarga por test.
- El principio transversal: slow, brittle, and time consuming — cuanto más arriba en la pirámide, menos tests debes escribir.
