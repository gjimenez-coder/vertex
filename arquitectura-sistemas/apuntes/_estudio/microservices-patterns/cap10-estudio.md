# Testing microservices: Part 2 (Probar microservicios: Parte 2) — Estudio

## Tarjetas de repaso

P: ¿Qué tres niveles de la pirámide de pruebas cubre este capítulo? / R: Tests de integración, tests de componente y tests end-to-end (los tres niveles superiores, por encima de los unitarios).

P: ¿Por qué deben minimizarse los tests end-to-end? / R: Porque probar la comunicación entre servicios arrancándolos todos es lento, frágil y costoso; hay que desplegar múltiples servicios e infraestructura y es probable que alguno falle al desplegarse.

P: ¿Qué verifican los tests de integración y qué los diferencia de arrancar los servicios? / R: Verifican que un servicio se comunica con sus dependencias, pero sin arrancar los servicios; prueban cada adaptador por separado y usan contratos para las interacciones.

P: ¿Qué es un contrato en el testing de contratos dirigido por el consumidor? / R: Un ejemplo concreto de interacción entre un par de servicios; consta de un mensaje (publish/subscribe) o dos (request/response) y su estructura depende del estilo de interacción.

P: ¿Cómo se usa un contrato en ambos lados de la interacción? / R: Los tests del consumidor lo usan para configurar stubs que simulan al proveedor; los del proveedor lo usan para probar sus adaptadores con mocks de sus dependencias.

P: En FTGO, ¿qué consumidor, proveedor y contrato corresponden a cada estilo de interacción? / R: REST: API Gateway consume de Order Service (petición/respuesta HTTP); Publish/subscribe: Order History Service consume de Order Service (evento de dominio); Request/response asíncrono: Order Service consume de Kitchen Service (mensaje de comando y de respuesta).

P: ¿Qué cuatro fases tiene un test de integración de persistencia? / R: Setup (crear esquema e inicializar estado conocido), execute (operación de BD), verify (aserciones sobre estado y objetos) y un teardown opcional.

P: ¿Qué herramientas usa Spring Cloud Contract en cada lado para REST? / R: En el consumidor configura un servidor stub HTTP (WireMock); en el proveedor genera tests que prueban los controladores con Rest Assured Mock MVC.

P: ¿Qué especifican `label` y `triggeredBy` en un contrato de publish/subscribe? / R: `label` lo usa el test del consumidor para disparar la publicación; `triggeredBy` es el método de la superclase que el test generado invoca para disparar la publicación.

P: En request/response asíncrono, ¿qué indican `messageFrom` y `sentTo`? / R: Desde la perspectiva del proveedor, `messageFrom` indica el canal de lectura (comando) y `sentTo` el canal de respuesta.

P: ¿Qué es un test de componente? / R: El test de aceptación de un servicio: lo trata como caja negra y verifica su comportamiento a través de su API, probándolo en aislamiento con stubs para sus dependencias (patrón Service component test).

P: ¿Cuál es la diferencia entre tests de componente in-process y out-of-process? / R: In-process ejecuta el servicio con stubs/mocks en memoria en la misma JVM (BD en memoria), más simple y rápido pero no prueba el desplegable; out-of-process empaqueta el servicio (p. ej. imagen Docker) con infraestructura real (MySQL, Kafka), más realista pero más lento y frágil.

P: ¿Qué son Gherkin y Cucumber y para qué se usan aquí? / R: Gherkin es un DSL de especificaciones ejecutables con estructura given-when-then; Cucumber ejecuta esos escenarios, permitiendo especificaciones ejecutables sin traducción manual a Java.

P: ¿Qué es un user journey test y qué ventaja aporta? / R: Un test que recorre el viaje completo de un usuario por el sistema (p. ej. crear, revisar y cancelar un pedido en un solo test), reduciendo el número de tests y el tiempo de ejecución en los end-to-end.

P: ¿Qué diferencia a un user journey test de un test de aceptación? / R: El user journey test tiene varias acciones (múltiples pasos) en lugar de un solo Then.

## Preguntas de autoevaluación

P: ¿Cuál es la tesis central del capítulo sobre probar la comunicación entre servicios? / R: Que arrancar todos los servicios para probar su comunicación (end-to-end) es lento, frágil y costoso, por lo que debe reducirse al mínimo y sustituirse por estrategias más baratas que verifican lo mismo con menos piezas en marcha. (Lo que necesitas saber)

P: ¿Por qué los tests de contratos permiten evitar arrancar ambos servicios y sus dependencias transitivas? / R: Porque el contrato es un mensaje de ejemplo que sirve para verificar que los adaptadores de ambos lados lo cumplen: el consumidor prueba contra stubs y el proveedor contra mocks, sin desplegar el otro servicio. (Writing integration tests / Ideas clave)

P: En el test de persistencia `shouldSaveAndLoadOrder()`, ¿qué hace cada una de sus dos transacciones? / R: La primera guarda un Order nuevo y la segunda lo carga y verifica sus campos. (Persistence integration tests)

P: ¿Cómo se prueba el lado consumidor de una interacción REST con Spring Cloud Contract? / R: `OrderServiceProxyIntegrationTest` se anota con `@AutoConfigureStubRunner` para arrancar WireMock en un puerto aleatorio y verifica que `OrderServiceProxy` devuelve los valores del contrato o lanza la excepción esperada. (REST-based request/response)

P: ¿Qué compromiso guía el diseño de los tests de componente? / R: Un compromiso entre realismo, velocidad y simplicidad, que lleva a elegir entre el enfoque in-process (más simple y rápido) y el out-of-process (más realista pero más complejo, lento y frágil). (Designing component tests)

P: ¿Cómo se estructura una especificación de aceptación a partir de una historia de usuario? / R: La historia (p. ej. "Place Order") se expande en escenarios given-when-then, organizados en features con nombre, specification brief y escenarios; en Java se implementan con step definitions anotadas con `@Given`, `@When`, `@Then` o `@And`. (Defining y writing acceptance tests)

P: ¿Cómo se ejecutan los tests de componente del FTGO Order Service y cuánto tardan? / R: Se colocan en `src/component-test/java` y se ejecutan con `./gradlew componentTest`; el plugin Gradle Docker Compose arranca Order Service y su infraestructura antes y los detiene al terminar, con un ciclo completo de un par de minutos. (Writing component tests for the FTGO Order Service)

P: ¿Cuál es la mejor estrategia para los tests end-to-end y por qué? / R: Los user journey tests, porque recorren un viaje completo del usuario en un solo test, reduciendo el número de tests y la sobrecarga por test; aun así arrancar todos los servicios tarda unos cuatro o cinco minutos. (Writing end-to-end tests)

## Puntos a dominar

- Ubicar correctamente cada tipo de test en la pirámide: integración, componente y end-to-end por encima de los unitarios, con menos tests cuanto más arriba.
- Explicar qué es un contrato y cómo se deriva según el estilo de interacción (REST, publish/subscribe, request/response asíncrono).
- Describir las cuatro fases de un test de integración de persistencia y el papel de los repositorios JPA.
- Diferenciar el rol de Spring Cloud Contract en el lado consumidor (stubs: WireMock, mensajería en memoria) y en el proveedor (tests generados con Rest Assured Mock MVC).
- Reconocer la nomenclatura de los contratos de publish/subscribe (`label`, `triggeredBy`) y de request/response asíncrono (`messageFrom`, `sentTo`).
- Caracterizar el patrón Service component test y justificar la elección entre in-process y out-of-process según realismo, velocidad y simplicidad.
- Redactar escenarios en Gherkin (given-when-then) y mapearlos a step definitions con Cucumber.
- Argumentar por qué minimizar los tests end-to-end y cómo los user journey tests reducen su coste.
