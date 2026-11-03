# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 9 — Testing microservices: Part 1 (Pruebas de microservicios: Parte 1)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo es la primera de dos partes dedicadas a las pruebas. Parte de un diagnóstico cultural: muchas organizaciones, como la ficticia FTGO, siguen el enfoque tradicional de probar *después* de desarrollar, con pruebas manuales y a cargo del equipo de QA. Esto es ineficaz por dos motivos: las pruebas manuales son lentas y no escalan, y se ejecutan demasiado tarde en el proceso de entrega. La tesis es que las pruebas automatizadas son indispensables para una entrega rápida y segura, porque acortan el *lead time* y, sobre todo, obligan a construir una aplicación testeable.

La arquitectura de microservicios mejora la testabilidad, pero su complejidad exige pruebas automatizadas y traslada el reto de probar los servicios individuales a verificar las *interacciones* entre ellos, minimizando las pruebas end-to-end (lentas, complejas y poco fiables).

Sales sabiendo: los conceptos de prueba automatizada (fases, dobles de prueba), los cuatro tipos de pruebas, el cuadrante y la pirámide de pruebas como guía de dónde concentrar el esfuerzo, la estrategia de *consumer-driven contract testing* para verificar interacciones sin end-to-end, el *deployment pipeline*, y cómo escribir pruebas unitarias para las distintas clases de un servicio.

## El ejemplo que recorre el capítulo

El hilo conductor es la aplicación FTGO y, en particular, su Order Service junto con las clases y servicios que lo rodean: Order (entidad), Money (value object), CreateOrderSaga, OrderService, OrderController y OrderEventConsumer, además de las relaciones consumidor-proveedor con API Gateway, Order History Service, Consumer Service y Kitchen Service.

## 9.1 Testing strategies for microservice architectures

El flujo de desarrollo ideal es: editar código, ejecutar pruebas (idealmente con una sola pulsación), repetir. Las pruebas rápidas confirman en segundos si el cambio funciona.

Conceptos de prueba:
- Un *test case* verifica el comportamiento del *System Under Test* (SUT), que puede ser tan pequeño como una clase o tan grande como la aplicación entera. Un conjunto de pruebas relacionadas forma un *test suite*.
- Una prueba automatizada tiene cuatro fases: *setup* (inicializa el *fixture*), *exercise* (invoca el SUT), *verify* (hace aserciones sobre el resultado y el estado) y *teardown* (limpia el fixture; a menudo se omite).

Dobles de prueba (test doubles): sustituyen las dependencias del SUT para probarlo en aislamiento, haciendo la prueba más simple y rápida. Hay dos tipos: un *stub* devuelve valores al SUT; un *mock* se usa para verificar que el SUT invoca correctamente una dependencia (y suele ser también un stub). En los ejemplos se usa Mockito.

Los cuatro tipos de pruebas, que difieren principalmente en alcance:
- **Unit tests**: prueban una parte pequeña de un servicio, como una clase.
- **Integration tests**: verifican que un servicio interactúa con infraestructura (bases de datos, otros servicios).
- **Component tests**: pruebas de aceptación de un servicio individual.
- **End-to-end tests**: pruebas de aceptación de toda la aplicación.

**Cuadrante de pruebas** (Brian Marick): categoriza según dos dimensiones —*business facing* vs *technology facing*, y *support programming* vs *critique the application*—. Q1 (unit e integration), Q2 (component y end-to-end), Q3 (usabilidad y exploratorias), Q4 (no funcionales, como rendimiento).

**Pirámide de pruebas** (Martin Fowler): el tiempo de ejecución, la complejidad y la fragilidad crecen con el alcance. En la base están las pruebas unitarias (rápidas, fáciles, fiables) y en la cima las end-to-end (lentas, frágiles, costosas). La idea clave: al subir por la pirámide, escribir cada vez menos pruebas. Muchas unitarias, muy pocas end-to-end.

### 9.1.2 El reto de probar microservicios

La comunicación interproceso (IPC) es central en los microservicios: la aplicación es un sistema distribuido donde los equipos evolucionan constantemente sus APIs. Cada interacción entre dos servicios es un contrato (estructura de eventos y canal, endpoints REST, formato de mensajes de comando y respuesta). Cada desarrollador necesita confiar en que las APIs que consume son estables y en no romper la API de su propio servicio.

**Consumer-driven contract testing**: en vez de probar interacciones con costosos end-to-end, se usan pruebas de contrato. En una relación consumidor-proveedor (p. ej., API Gateway consumidor, Order Service proveedor), una *consumer contract test* es una prueba de integración del proveedor que verifica que la "forma" de su API cumple las expectativas del consumidor. Para un endpoint REST verifica método HTTP y ruta, cabeceras aceptadas, cuerpo de petición y respuesta esperada (código de estado, cabeceras, cuerpo). No prueba la lógica de negocio del proveedor (eso es trabajo de las unitarias).

- Patrón: *Consumer-driven contract test* — verifica que un servicio cumple las expectativas de sus clientes.
- Patrón: *Consumer-side contract test* — verifica que el cliente de un servicio puede comunicarse con él.

El equipo consumidor escribe un *contract test suite* (p. ej., vía pull request) y lo añade a la suite del proveedor; el *deployment pipeline* del proveedor lo ejecuta. Si falla, indica al equipo proveedor que ha introducido un cambio incompatible.

**Spring Cloud Contract**: los dos frameworks populares son Spring Cloud Contract (para Spring) y la familia Pact (multilenguaje). Spring Cloud Contract ofrece un DSL en Groovy para escribir contratos; genera pruebas de contrato para el proveedor y configura mocks (p. ej., servidor HTTP mock) para las pruebas de integración del consumidor. Flujo: el equipo de API Gateway escribe los contratos, el equipo de Order Service los usa para probar su servicio y los publica en un repositorio Maven como JAR, y el equipo consumidor usa los contratos publicados para probar API Gateway. Ejemplo de contrato:

```groovy
org.springframework.cloud.contract.spec.Contract.make {
  request {
    method 'GET'
    url '/orders/1223232'
  }
  response {
    status 200
    headers {
      header('Content-Type': 'application/json;charset=UTF-8')
    }
    body("{ ... }")
  }
}
```

Para APIs de mensajería también hay soporte: un contrato de publicación de eventos de dominio consiste en un evento de ejemplo; uno de request/response asíncrono consiste en un mensaje de petición y uno de respuesta.

### 9.1.3 El deployment pipeline

Según *Continuous Delivery* (Jez Humble), es el proceso automatizado que lleva el código del escritorio del desarrollador a producción. Consiste en una serie de etapas con suites de pruebas cada vez más exhaustivas y entornos más parecidos a producción; a mayor etapa, mayor tiempo de ejecución. Suele implementarse con un servidor CI como Jenkins. Etapas del ejemplo:
- *Pre-commit tests*: ejecuta las pruebas unitarias (lo hace el desarrollador antes de hacer commit).
- *Commit tests*: compila, corre unitarias y análisis estático.
- *Integration tests*.
- *Component tests*.
- *Deploy*: despliega a producción.

## 9.2 Writing unit tests for a service

Las pruebas unitarias están en la base de la pirámide: *technology-facing* y de soporte al desarrollo. Verifican que una unidad (normalmente una clase) funciona. Hay dos tipos:
- **Solitary unit test**: prueba una clase en aislamiento, con mocks para sus dependencias.
- **Sociable unit test**: prueba una clase junto con sus dependencias.

La responsabilidad de la clase (arquitectura hexagonal) determina el tipo:
- Entidades (Order), value objects (Money) y sagas (CreateOrderSaga): pruebas sociables.
- Domain services (OrderService), controllers (OrderController) y gateways de mensajería entrantes/salientes: pruebas solitarias.

**9.2.1 Entidades**: `OrderTest` usa un `@Before setUp()` que crea una Order; `shouldCalculateTotal()` verifica `getOrderTotal()`. Son pruebas sociables (Order depende de Money) y lo bastante rápidas para usarse en tiempo de compilación.

**9.2.2 Value objects**: son inmutables, fáciles de probar. `MoneyTest` verifica `add()` y `multiply()`. Son solitarias porque Money no depende de otras clases de la aplicación.

**9.2.3 Sagas**: `CreateOrderSagaTest` verifica que la saga envía la secuencia correcta de mensajes de comando y gestiona las respuestas (camino feliz y escenarios de rollback). Es sociable, escrita con el framework de pruebas Eventuate Tram Saga, que ofrece un DSL `given/expect` y configura mocks para la base de datos y la mensajería. Ejemplo: ante una `successReply()` envía `CreateTicket` a Kitchen Service; ante un fallo de verificación del consumidor envía `RejectOrderCommand` a Order Service.

**9.2.4 Domain services**: `OrderServiceTest` usa pruebas mayormente solitarias con mocks de Mockito para repositorios y clases de mensajería. `shouldCreateOrder()` configura los mocks, invoca `createOrder()` y verifica que se guarda la Order, se publica un `OrderCreatedEvent` y se crea una `CreateOrderSaga`.

**9.2.5 Controllers**: mejor usar un framework de mock MVC (Spring Mock Mvc o Rest Assured Mock MVC) que prueba enrutamiento de peticiones y conversión JSON sin llamadas de red reales. `OrderControllerTest` inyecta mocks de OrderService y OrderRepository; `shouldFindOrder()` hace un `get("/orders/1")` y verifica el código 200 y el cuerpo JSON. El libro reconoce el debate sobre si estas son realmente "unit tests" (Spring las llama *out-of-servlet-container integration tests*), pero concluye que lo importante es escribirlas.

**9.2.6 Event/message handlers**: `OrderEventConsumerTest` usa Eventuate Tram Mock Messaging (DSL `given-when-then`, infraestructura de mensajería *stubbed*, sin broker). `shouldCreateMenu()` publica un evento `RestaurantCreated` y verifica que `OrderEventConsumer` invocó `OrderService.createMenu()`.

Las pruebas unitarias corren en pocos segundos, pero no verifican que un servicio interactúe correctamente con otros (persistencia en MySQL, formato de mensajes de la saga, estructura de eventos entre servicios). Para eso hacen falta integration tests, component tests y end-to-end tests, tema del capítulo 10.

## Ideas clave

- Las pruebas automatizadas son el fundamento de una entrega rápida y segura, y son imprescindibles para aprovechar la arquitectura de microservicios por su complejidad inherente.
- El objetivo de una prueba es verificar el comportamiento del SUT; las pruebas tienen cuatro fases (setup, exercise, verify, teardown).
- Los dobles de prueba simplifican y aceleran: un *stub* devuelve valores; un *mock* verifica que el SUT invoca correctamente una dependencia.
- La pirámide de pruebas guía el esfuerzo: muchas unitarias (rápidas, fiables), muy pocas end-to-end (lentas, frágiles, costosas).
- En microservicios el reto se desplaza a verificar las *interacciones*; el *consumer-driven contract testing* (Spring Cloud Contract, Pact) sustituye costosos end-to-end.
- Un *consumer contract test* verifica la forma de la API del proveedor; no prueba su lógica de negocio.
- El *deployment pipeline* ejecuta suites cada vez más exhaustivas (pre-commit, commit, integration, component, deploy), dando feedback cuanto antes.
- El tipo de prueba unitaria depende de la clase: solitarias para domain services, controllers y gateways de mensajería; sociables para entidades, value objects y sagas.
