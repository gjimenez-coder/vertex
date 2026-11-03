# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 8 — External API patterns (Patrones de API externa)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo aborda el reto de diseñar la API externa de una aplicación de microservicios cuando los clientes son diversos: aplicaciones web, JavaScript en el navegador, apps móviles y aplicaciones de terceros. La tesis central es que raramente conviene una única API "para todos" (one-size-fits-all), porque los clientes tienen necesidades de datos distintas y acceden por redes de rendimiento muy diferente (LAN interna frente a internet o red móvil, cuya latencia es "típicamente 100 veces mayor que una LAN").

Que los clientes invoquen los servicios directamente es poco práctico en microservicios: las APIs de grano fino obligan a múltiples peticiones, la falta de encapsulación acopla el cliente a la descomposición de servicios, y algunos servicios usan protocolos (gRPC, AMQP) poco amigables fuera del firewall. La solución es un API gateway: punto de entrada único responsable de enrutamiento de peticiones, composición de API, traducción de protocolos y funciones de borde como autenticación.

Sales sabiendo cuándo usar un API gateway, la variante Backends for frontends (una gateway por tipo de cliente), los problemas de diseño (rendimiento, programación reactiva, fallos parciales) y tres caminos de implementación: productos listos para usar, Spring Cloud Gateway y GraphQL.

## El ejemplo que recorre el capítulo

La aplicación FTGO (reparto de comida). El hilo conductor es la vista "View Order" de la app móvil del consumidor, cuyos datos están repartidos entre varios servicios: Order Service (información y estado básico del pedido), Kitchen Service (estado desde el restaurante), Delivery Service (estado, ubicación y tiempo estimado de entrega) y Accounting Service (estado de pago). Recuperar el detalle del pedido pasa de una sola petición al monolito a muchas llamadas en microservicios.

## 8.1 Problemas de diseño de la API externa

Cuatro tipos de clientes consumen las APIs: aplicaciones web (Consumer, Restaurant, Admin), JavaScript en el navegador, apps móviles (consumidor y repartidor) y aplicaciones de terceros. Las web corren dentro del firewall sobre una LAN de alto ancho de banda; los demás acceden por internet o red móvil, de menor rendimiento.

Si la app móvil llama a los servicios directamente actúa como *API composer* y surgen tres problemas:

- **Mala experiencia de usuario** por múltiples peticiones: la interacción "chatty" sobre redes lentas vuelve la app poco responsiva, exige código de composición complejo y agota la batería.
- **Falta de encapsulación**: los cambios de API de los servicios rompen clientes; desplegar una nueva versión de una app móvil tarda horas o días y depende de que Apple/Google la aprueben y el usuario la descargue.
- **Protocolos poco amigables para el cliente**: gRPC o AMQP funcionan bien internamente pero no siempre son consumibles ni compatibles con firewall.

Las apps web sí pueden acceder a los servicios directamente (están dentro del firewall, mismo equipo). El JavaScript en navegador sufre la misma latencia que el móvil. Para los terceros el mayor reto es ofrecer una **API estable**: hay que mantener versiones antiguas mucho tiempo, por lo que conviene una API pública separada desarrollada por un equipo aparte, implementada por un API gateway.

## 8.2 El patrón API gateway

**Patrón: API gateway** — implementa un servicio que es el punto de entrada a la aplicación de microservicios para los clientes externos de la API.

Es análogo al patrón Facade: encapsula la arquitectura interna y ofrece una API a los clientes. Sus responsabilidades:

- **Enrutamiento de peticiones (request routing)**: consulta un mapa de rutas (p. ej. método y path HTTP → URL del servicio); equivale al reverse proxy de servidores como NGINX.
- **Composición de API (API composition)**: implementa operaciones como `getOrderDetails()` invocando varios servicios y agregando resultados, para que el cliente haga una sola petición.
- **Traducción de protocolos**: expone, por ejemplo, REST hacia fuera aunque los servicios usen REST y gRPC internamente.
- **API específica por cliente**: mejor que una API OSFA; incluso APIs distintas para Android e iPhone, más una API pública para terceros.
- **Funciones de borde (edge functions)**: autenticación, autorización, rate limiting, caching, recolección de métricas y logging de peticiones.

Las funciones de borde pueden colocarse en los servicios backend, en un *edge service* upstream (separa responsabilidades y centraliza la autenticación, pero añade un salto de red y complejidad) o en la propia gateway (menos saltos, menor latencia, menos piezas; suele ser la opción conveniente, especialmente para autorización).

**Arquitectura**: capas API y común. La capa API tiene módulos independientes (Mobile API, Browser API, Public API); la capa común implementa funcionalidad compartida como la autenticación.

**Modelo de propiedad**: en lugar de un equipo central (que recrea el cuello de botella del ESB en SOA), el enfoque promovido por Netflix es que cada equipo cliente posea su módulo de API; un equipo de API gateway mantiene el módulo común y la operación. Requiere un pipeline de despliegue totalmente automatizado.

**Patrón: Backends for frontends (BFF)** — implementa una API gateway separada por cada tipo de cliente. Pionero: Phil Calçado y colegas en SoundCloud. Cada módulo de API pasa a ser una gateway autónoma, propiedad de un equipo. Beneficios: responsabilidades claras, aislamiento (una API que falla no afecta a otras), mejor observabilidad, escalado independiente y menor tiempo de arranque.

**Beneficios y desventajas**: encapsula la estructura interna, da API específica por cliente, reduce round-trips y simplifica el código del cliente. En contra: es otro componente de alta disponibilidad que mantener y un posible cuello de botella de desarrollo si actualizar la gateway no es ligero.

**Netflix** es el ejemplo de referencia: pasó de una API OSFA a una API por dispositivo; su gateway maneja miles de millones de peticiones al día y cada llamada se abre en seis o siete servicios backend. Está migrando hacia una arquitectura tipo BFF con módulos en NodeJS que invocan una segunda gateway basada en Netflix Falcor.

### Problemas de diseño de la gateway

- **Rendimiento y escalabilidad**: E/S síncrona (un hilo por conexión, simple pero limitada por el coste de los hilos) frente a E/S asíncrona no bloqueante (un event loop; más escalable con Netty, Vert.x, Spring Reactor, Undertow o NodeJS, pero de programación más compleja). Netflix tuvo resultados mixtos al reescribir Zuul con NIO: +25% throughput y −25% CPU en lógica intensiva de E/S, sin mejora en lógica intensiva de CPU.
- **Programación reactiva**: llamar a los servicios en secuencia hace que el tiempo de respuesta sea la suma de todos; conviene invocarlos en paralelo. Los callbacks tradicionales llevan a "callback hell"; mejor un estilo declarativo con abstracciones reactivas: Java 8 `CompletableFuture`, `Mono` de Project Reactor, Observables de RxJava (creado por Netflix para esto), Scala Futures, o promesas/RxJS en NodeJS.
- **Fallos parciales**: replicar la gateway tras un balanceador de carga y usar el patrón **Circuit breaker** al invocar servicios para no quedar bloqueado por servicios lentos o caídos.
- **Ser buen ciudadano**: adoptar los patrones de descubrimiento de servicios y de observabilidad elegidos para la arquitectura.

## 8.3 Implementación de un API gateway

Dos vías: usar un producto/servicio listo (poco desarrollo, menos flexible; normalmente **no** soporta composición de API) o desarrollar la propia con un framework (más flexible).

**Productos y servicios listos**:
- **AWS API Gateway**: conjunto de recursos REST que enruta cada (método, recurso) a un backend (Lambda, servicio HTTP o servicio AWS); autentica y escala solo. No soporta composición de API, solo HTTP(S) con énfasis en JSON y solo el patrón de descubrimiento del lado servidor.
- **AWS Application Load Balancer**: enrutamiento básico HTTP/HTTPS/WebSocket/HTTP2, pero sin enrutamiento por método HTTP, composición ni autenticación; no cumple los requisitos de una gateway.
- **Kong** (basado en NGINX) y **Traefik** (en GoLang): enrutamiento flexible y plugins de funciones de borde, pero hay que operarlos y no hacen composición de API.

**Desarrollar la propia** con Spring Cloud Gateway (sobre Spring Framework 5, Spring Boot 2 y Spring WebFlux/Project Reactor). Permite enrutar, implementar handlers con composición de API y funciones de borde. Paquetes: `ApiGatewayMain`, uno o más paquetes de API y un paquete `Proxy`. El enrutamiento se define con un DSL (p. ej. `orderProxyRouting` mapea `/orders` al Order Service; `orderHandlerRouting` mapea `GET /orders/{orderId}` a `OrderHandlers::getOrderDetails`). El handler usa `Mono` (un `CompletableFuture` enriquecido) para invocar los cuatro servicios en paralelo, tratando como opcionales todos menos Order Service con `onErrorReturn()`, combinando con `Mono.when()` en un `Tuple4` y devolviendo un `ServerResponse`. Los proxies usan `WebClient`, el cliente HTTP reactivo de WebFlux. Alternativa citada: **Netflix Zuul** (y Spring Cloud Zuul), basado en filtros, pero limitado a enrutamiento por path (no distingue `GET /orders` de `POST /orders`), por lo que no soporta la arquitectura de queries CQRS.

**GraphQL** (con Apollo GraphQL sobre NodeJS/Express) es otra opción: la API es un **esquema basado en grafo** de tipos (nodos) con campos y relaciones; el cliente ejecuta una consulta que especifica exactamente los datos que necesita y los obtiene en un solo round-trip. Da control al cliente y reduce el esfuerzo de desarrollo. El esquema se conecta a los datos mediante **resolvers** (funciones con parámetros objeto, argumentos y contexto) que invocan los servicios; GraphQL ejecuta los resolvers de forma recursiva e implementa así la composición de API. Para evitar demasiados round-trips se usan **batching y caching** con el módulo DataLoader (creado por request para no mezclar datos de usuarios). El servidor Apollo se integra con Express vía `graphqlExpress` enrutando `GET`/`POST /graphql`; los clientes pueden usar la librería ApolloClient. Otra tecnología basada en grafo mencionada es Netflix Falcor (una implementación que modela los datos como un grafo JSON virtual; GraphQL, en cambio, es un estándar).

## Ideas clave

- Los clientes externos acceden a los servicios a través de un API gateway, no directamente; este es el punto de entrada único.
- El API gateway se encarga de enrutamiento, composición de API, traducción de protocolos y funciones de borde como la autenticación.
- Una sola API OSFA no sirve para clientes diversos; dar a cada cliente una API específica reduce round-trips y simplifica su código.
- El patrón Backends for frontends define una gateway por tipo de cliente y da autonomía a los equipos para desarrollar, desplegar y operar la suya.
- El rendimiento depende del modelo de E/S (síncrona frente a asíncrona no bloqueante); la reactividad (`Mono`, Observables, promesas) evita el "callback hell".
- Para la fiabilidad, replicar la gateway tras un balanceador y aplicar el Circuit breaker ante servicios lentos o caídos.
- Spring Cloud Gateway (reactivo, basado en Spring 5 y Project Reactor) enruta por cualquier atributo de la petición y permite handlers con composición de API.
- GraphQL ofrece un esquema basado en grafo con resolvers y consultas flexibles; es una alternativa atractiva a una gateway REST tradicional para soportar clientes diversos.
