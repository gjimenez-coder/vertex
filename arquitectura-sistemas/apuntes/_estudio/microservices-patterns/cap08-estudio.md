# External API patterns (Patrones de API externa) — Estudio

## Tarjetas de repaso

P: ¿Por qué no conviene una única API "para todos" (one-size-fits-all)?
R: Porque los clientes (web, JavaScript en navegador, apps móviles, terceros) tienen necesidades de datos distintas y acceden por redes de rendimiento muy diferente, siendo la latencia móvil típicamente 100 veces mayor que una LAN.

P: ¿Qué es el patrón API gateway?
R: Un servicio que es el punto de entrada único a la aplicación de microservicios para los clientes externos; es análogo al patrón Facade porque encapsula la arquitectura interna y ofrece una API a los clientes.

P: ¿Cuáles son las responsabilidades principales de un API gateway?
R: Enrutamiento de peticiones, composición de API, traducción de protocolos, API específica por cliente y funciones de borde (autenticación, autorización, rate limiting, caching, métricas y logging).

P: ¿Qué es la composición de API en la gateway?
R: Implementar operaciones como `getOrderDetails()` invocando varios servicios y agregando los resultados, para que el cliente haga una sola petición.

P: ¿Qué tres problemas surgen si una app móvil llama directamente a los servicios como API composer?
R: Mala experiencia de usuario por múltiples peticiones ("chatty"), falta de encapsulación (los cambios de API rompen clientes) y protocolos poco amigables para el cliente (gRPC, AMQP).

P: ¿Qué es el patrón Backends for frontends (BFF)?
R: Implementar una API gateway separada por cada tipo de cliente; cada módulo de API pasa a ser una gateway autónoma propiedad de un equipo. Fue pionero Phil Calçado y colegas en SoundCloud.

P: ¿Qué beneficios aporta el patrón BFF?
R: Responsabilidades claras, aislamiento (una API que falla no afecta a otras), mejor observabilidad, escalado independiente y menor tiempo de arranque.

P: ¿Qué modelo de propiedad promueve Netflix para la gateway?
R: Que cada equipo cliente posea su módulo de API y un equipo de API gateway mantenga el módulo común y la operación, evitando el cuello de botella de un equipo central; requiere un pipeline de despliegue totalmente automatizado.

P: ¿Qué diferencia hay entre E/S síncrona y asíncrona no bloqueante en la gateway?
R: La síncrona usa un hilo por conexión (simple pero limitada por el coste de los hilos); la asíncrona no bloqueante usa un event loop (más escalable con Netty, Vert.x, Spring Reactor, Undertow o NodeJS, pero de programación más compleja).

P: ¿Para qué sirve la programación reactiva en la gateway?
R: Para invocar los servicios en paralelo (y no en secuencia, cuya respuesta sería la suma de todos) evitando el "callback hell" mediante abstracciones como `CompletableFuture`, `Mono`, Observables de RxJava o promesas.

P: ¿Cómo se afrontan los fallos parciales en una gateway?
R: Replicando la gateway tras un balanceador de carga y usando el patrón Circuit breaker al invocar servicios para no quedar bloqueado por servicios lentos o caídos.

P: ¿Qué limitación común tienen los productos listos para usar como gateway?
R: Que normalmente no soportan composición de API (caso de AWS API Gateway, Kong y Traefik), ofreciendo poco desarrollo a cambio de menor flexibilidad.

P: ¿Qué es Spring Cloud Gateway?
R: Un framework reactivo (sobre Spring Framework 5, Spring Boot 2 y Spring WebFlux/Project Reactor) que permite enrutar por cualquier atributo de la petición e implementar handlers con composición de API y funciones de borde.

P: ¿Qué es GraphQL como alternativa de gateway?
R: Una API con esquema basado en grafo de tipos con campos y relaciones, donde el cliente ejecuta una consulta que especifica exactamente los datos que necesita y los obtiene en un solo round-trip.

P: ¿Qué son los resolvers en GraphQL y cómo logran la composición de API?
R: Funciones (con parámetros objeto, argumentos y contexto) que conectan el esquema con los datos invocando los servicios; GraphQL los ejecuta de forma recursiva, implementando así la composición de API.

## Preguntas de autoevaluación

P: ¿Por qué las aplicaciones web sí pueden acceder a los servicios directamente mientras el JavaScript en navegador y las apps móviles no deberían?
R: Porque las apps web corren dentro del firewall sobre una LAN de alto ancho de banda y en el mismo equipo, mientras que el JavaScript en navegador y el móvil sufren la latencia de internet o red móvil. (Sección 8.1)

P: ¿Cuál es el mayor reto al ofrecer una API a aplicaciones de terceros y cómo se resuelve?
R: Ofrecer una API estable, manteniendo versiones antiguas mucho tiempo; conviene una API pública separada desarrollada por un equipo aparte, implementada por un API gateway. (Sección 8.1)

P: ¿Dónde pueden colocarse las funciones de borde y por qué suele convenir la gateway?
R: En los servicios backend, en un edge service upstream o en la propia gateway; la gateway suele convenir (especialmente para autorización) por tener menos saltos de red, menor latencia y menos piezas que mantener. (Sección 8.2)

P: ¿Cuáles son los beneficios y desventajas del patrón API gateway?
R: Beneficios: encapsula la estructura interna, da API específica por cliente, reduce round-trips y simplifica el código del cliente. Desventajas: es otro componente de alta disponibilidad que mantener y un posible cuello de botella de desarrollo. (Sección 8.2)

P: ¿Qué resultados obtuvo Netflix al reescribir Zuul con NIO (E/S no bloqueante)?
R: Resultados mixtos: +25% de throughput y −25% de CPU en lógica intensiva de E/S, pero sin mejora en lógica intensiva de CPU. (Sección 8.2, Problemas de diseño de la gateway)

P: ¿Por qué Netflix Zuul no soporta la arquitectura de queries CQRS como gateway?
R: Porque está limitado a enrutamiento por path y no distingue el método HTTP (p. ej. `GET /orders` de `POST /orders`). (Sección 8.3)

P: ¿Cómo evita GraphQL hacer demasiados round-trips a los servicios?
R: Mediante batching y caching con el módulo DataLoader, creado por request para no mezclar datos de distintos usuarios. (Sección 8.3)

P: En el ejemplo FTGO, ¿por qué la vista "View Order" ilustra el problema de la API externa?
R: Porque sus datos están repartidos entre Order, Kitchen, Delivery y Accounting Service, de modo que recuperar el detalle del pedido pasa de una sola petición al monolito a muchas llamadas en microservicios. (El ejemplo que recorre el capítulo)

## Puntos a dominar

- Distinguir los cuatro tipos de clientes (web, JavaScript en navegador, apps móviles, terceros) y sus diferencias de red y de API.
- Explicar por qué una API OSFA no sirve y cómo una API específica por cliente reduce round-trips.
- Enumerar las responsabilidades del API gateway: enrutamiento, composición, traducción de protocolos, API por cliente y funciones de borde.
- Describir el patrón Backends for frontends y su modelo de propiedad por equipos.
- Comparar E/S síncrona frente a asíncrona no bloqueante y el papel de la programación reactiva.
- Aplicar replicación tras balanceador y Circuit breaker frente a fallos parciales.
- Comparar las vías de implementación: productos listos (sin composición de API), Spring Cloud Gateway y GraphQL con resolvers.
