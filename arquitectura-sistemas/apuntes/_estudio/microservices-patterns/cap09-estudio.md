# Testing microservices: Part 1 (Pruebas de microservicios: Parte 1) — Estudio

## Tarjetas de repaso

P: ¿Por qué el enfoque tradicional de probar después de desarrollar (manual y a cargo de QA) es ineficaz?
R: Porque las pruebas manuales son lentas y no escalan, y se ejecutan demasiado tarde en el proceso de entrega.

P: ¿Cuál es la tesis del capítulo sobre las pruebas automatizadas?
R: Son indispensables para una entrega rápida y segura porque acortan el *lead time* y obligan a construir una aplicación testeable.

P: ¿Qué es el System Under Test (SUT) y qué forma un *test suite*?
R: El SUT es lo que verifica un *test case* (desde una clase hasta la aplicación entera); un conjunto de pruebas relacionadas forma un *test suite*.

P: ¿Cuáles son las cuatro fases de una prueba automatizada?
R: Setup (inicializa el *fixture*), exercise (invoca el SUT), verify (hace aserciones sobre resultado y estado) y teardown (limpia el fixture; a menudo se omite).

P: ¿Qué diferencia a un *stub* de un *mock*?
R: Un *stub* devuelve valores al SUT; un *mock* se usa para verificar que el SUT invoca correctamente una dependencia (y suele ser también un stub).

P: ¿Cuáles son los cuatro tipos de pruebas y en qué difieren principalmente?
R: Unit, integration, component y end-to-end; difieren principalmente en alcance (desde una clase hasta toda la aplicación).

P: ¿Qué dimensiones usa el cuadrante de pruebas de Brian Marick?
R: *Business facing* vs *technology facing*, y *support programming* vs *critique the application* (Q1 unit/integration, Q2 component/end-to-end, Q3 usabilidad/exploratorias, Q4 no funcionales).

P: ¿Cuál es la idea clave de la pirámide de pruebas de Martin Fowler?
R: Al subir por la pirámide (crece tiempo, complejidad y fragilidad) escribir cada vez menos pruebas: muchas unitarias, muy pocas end-to-end.

P: ¿En qué se desplaza el reto de probar en una arquitectura de microservicios?
R: De probar los servicios individuales a verificar las *interacciones* entre ellos, minimizando las pruebas end-to-end.

P: ¿Qué verifica un *consumer contract test* y qué no verifica?
R: Verifica que la "forma" de la API del proveedor cumple las expectativas del consumidor (método, ruta, cabeceras, cuerpos); no prueba la lógica de negocio.

P: ¿Qué es el *deployment pipeline* según *Continuous Delivery*?
R: El proceso automatizado que lleva el código del escritorio del desarrollador a producción, con etapas de pruebas cada vez más exhaustivas y entornos más parecidos a producción.

P: ¿Cuáles son las etapas del *deployment pipeline* del ejemplo?
R: Pre-commit tests, commit tests (compila, unitarias y análisis estático), integration tests, component tests y deploy.

P: ¿Qué diferencia una *solitary unit test* de una *sociable unit test*?
R: La solitaria prueba una clase en aislamiento con mocks para sus dependencias; la sociable prueba la clase junto con sus dependencias.

P: Según la responsabilidad de la clase (arquitectura hexagonal), ¿qué clases usan pruebas sociables y cuáles solitarias?
R: Sociables: entidades (Order), value objects (Money) y sagas (CreateOrderSaga). Solitarias: domain services, controllers y gateways de mensajería entrantes/salientes.

P: ¿Cuáles son los dos frameworks populares de contract testing mencionados?
R: Spring Cloud Contract (para Spring, con DSL en Groovy) y la familia Pact (multilenguaje).

## Preguntas de autoevaluación

P: ¿Cuál es el flujo de desarrollo ideal al trabajar con pruebas rápidas?
R: Editar código, ejecutar pruebas (idealmente con una sola pulsación) y repetir; las pruebas rápidas confirman en segundos si el cambio funciona. (Sección 9.1)

P: ¿Para qué sirven los dobles de prueba y por qué mejoran la prueba?
R: Sustituyen las dependencias del SUT para probarlo en aislamiento, haciendo la prueba más simple y rápida. (Sección 9.1)

P: ¿Qué es un contrato entre dos servicios y por qué importa en microservicios?
R: Cada interacción es un contrato (estructura de eventos y canal, endpoints REST, formato de mensajes de comando y respuesta); importa porque cada desarrollador necesita confiar en que las APIs que consume son estables y en no romper la API de su propio servicio. (Sección 9.1.2)

P: ¿Cómo funciona el flujo de consumer-driven contract testing entre equipos?
R: El equipo consumidor escribe un *contract test suite* y lo añade a la suite del proveedor; el *deployment pipeline* del proveedor lo ejecuta, y si falla indica un cambio incompatible. (Sección 9.1.2)

P: ¿Por qué las entidades como Order se prueban con pruebas sociables y los value objects como Money con solitarias?
R: Order depende de Money (sociable), mientras que Money es inmutable y no depende de otras clases de la aplicación (solitaria). (Secciones 9.2.1 y 9.2.2)

P: ¿Qué verifica `shouldCreateOrder()` en `OrderServiceTest`?
R: Configura los mocks, invoca `createOrder()` y verifica que se guarda la Order, se publica un `OrderCreatedEvent` y se crea una `CreateOrderSaga`. (Sección 9.2.4)

P: ¿Por qué se recomienda un framework de mock MVC para probar controllers?
R: Porque prueba el enrutamiento de peticiones y la conversión JSON sin llamadas de red reales. (Sección 9.2.5)

P: ¿Qué limitación tienen las pruebas unitarias y qué las complementa?
R: Corren en pocos segundos pero no verifican que un servicio interactúe correctamente con otros (persistencia, formato de mensajes, estructura de eventos); las complementan integration, component y end-to-end tests (capítulo 10). (Sección 9.2.6)

## Puntos a dominar

- Explicar por qué las pruebas automatizadas son el fundamento de una entrega rápida y segura en microservicios.
- Identificar el SUT, el *test suite* y las cuatro fases de una prueba (setup, exercise, verify, teardown).
- Distinguir *stub* de *mock* y reconocer su uso con Mockito.
- Clasificar los cuatro tipos de pruebas por alcance y situarlos en el cuadrante de Marick y la pirámide de Fowler.
- Justificar por qué concentrar el esfuerzo en pruebas unitarias y minimizar las end-to-end.
- Describir el consumer-driven contract testing y la diferencia entre *consumer-driven contract test* y *consumer-side contract test*.
- Enumerar las etapas del *deployment pipeline* y qué prueba cada una.
- Elegir entre prueba solitaria y sociable según la responsabilidad de la clase (arquitectura hexagonal).
- Reconocer los frameworks usados en los ejemplos: Mockito, Eventuate Tram Saga, Spring/Rest Assured Mock MVC, Eventuate Tram Mock Messaging y Spring Cloud Contract/Pact.
