# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 11 — Developing production-ready services (Desarrollo de servicios listos para producción)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Un servicio no está listo para producción solo porque cumple sus requisitos funcionales. Debe además satisfacer tres atributos de calidad críticos: seguridad, configurabilidad y observabilidad. El capítulo muestra cómo implementar cada uno en una arquitectura de microservicios, donde muchos problemas se resuelven igual que en un monolito, pero otros exigen enfoques distintos por tratarse de un sistema distribuido.

La tesis central es que estos "concerns" transversales (seguridad, configuración externalizada, chequeos de salud, agregación de logs, trazado distribuido, seguimiento de excepciones, métricas y audit logging) deben diseñarse desde el inicio y, en gran medida, delegarse a un framework reutilizable. El capítulo cierra presentando el patrón Microservice chassis y su evolución hacia el service mesh.

Sales sabiendo cómo pasar la identidad del usuario entre servicios con tokens transparentes (JWT) y OAuth 2.0, cómo externalizar la configuración con modelos push y pull, qué patrones de observabilidad implementar y cómo repartir responsabilidad entre desarrolladores y operaciones, y cómo acelerar el desarrollo apoyándote en un chassis o en un service mesh.

## El ejemplo que recorre el capítulo

Se usa la aplicación FTGO (delivery de comida). Tiene usuarios humanos (consumers, couriers, restaurant staff) y clientes API. El monolito FTGO está escrito en Java con Spring Security. Servicios como Order Service, Kitchen Service, Accounting Service, User Service y Order History Service ilustran la seguridad, la configuración (Order History Service usa Apache Kafka y AWS DynamoDB) y la observabilidad.

## Developing secure services (11.1)

El desarrollador es responsable de cuatro aspectos de seguridad:

- Authentication: verificar la identidad del principal (usuario o aplicación) mediante credenciales como user ID y password, o API key y secret.
- Authorization: verificar que el principal puede realizar la operación. Se combinan role-based security (roles como CONSUMER, RESTAURANT, COURIER, ADMIN) y ACLs (acceso a un objeto de negocio o aggregate concreto).
- Auditing: rastrear las operaciones del principal para detectar problemas, dar soporte y cumplir normativa.
- Secure interprocess communication: idealmente toda comunicación sobre TLS.

Recomienda usar un framework probado: Spring Security o Apache Shiro (Java), Passport (NodeJS).

En el monolito, la sesión (HttpSession en memoria) guarda ID y roles del principal, identificada por un session token (cookie `JSESSIONID`). El security context se almacena en una variable thread-local estática. Dos elementos del monolito son inviables en microservicios: el in-memory security context (los servicios no comparten memoria) y la centralized session (una sesión en base de datos compartida violaría el bajo acoplamiento).

Autenticación en el API gateway: en lugar de dejar que cada servicio autentique (riesgo de permitir peticiones no autenticadas en la red interna y de manejar múltiples mecanismos), conviene centralizar la autenticación en el API gateway. Este reenvía un token en cada petición a los servicios para que identifiquen al principal y verifiquen la autenticación.

> Patrón Access token: el API gateway pasa un token con información del usuario (identidad y roles) a los servicios que invoca.

Autorización: puede hacerse en el API gateway (acceso role-based a rutas URL; inconveniente: acopla el gateway a los servicios y no es práctico implementar ACLs por objeto de dominio) o en los servicios (role-based para URLs y métodos, más ACLs sobre aggregates).

Tipos de token para pasar identidad:

- Opaque tokens (típicamente UUID): reducen rendimiento y disponibilidad porque obligan a una llamada RPC síncrona al servicio de seguridad para validar.
- Transparent tokens, como el JSON Web Token (JWT): payload JSON con identidad, roles y metadatos (p. ej. expiración), firmado con un secreto. Problema: al ser autocontenido, un JWT es irrevocable; la solución es emitirlos con expiración corta, lo que obliga a reemitirlos para mantener la sesión.

OAuth 2.0: protocolo de autorización reutilizable para no reinventar la infraestructura de seguridad. Conceptos clave: Authorization Server (autentica y emite access token y refresh token; p. ej. Spring OAuth), Access Token (acceso al Resource Server, puede ser un JWT), Refresh Token (token revocable de larga vida para obtener nuevos access tokens), Resource Server (los servicios) y Client (el API gateway). El API gateway autentica usando un Password Grant request y, al expirar el access token, lo renueva con un Refresh Grant request.

Ideas centrales de seguridad: el API gateway autentica a los clientes; gateway y servicios usan un token transparente (JWT) para pasar información del principal; el servicio usa el token para obtener identidad y roles.

## Designing configurable services (11.2)

Las propiedades de configuración (ubicación de red y credenciales de Kafka, DynamoDB, etc.) dependen del entorno. No deben cablearse en el servicio ni en el código fuente (crea vulnerabilidades y obliga a reconstruir por entorno). Los datos sensibles deben guardarse en un secrets storage como Hashicorp Vault o AWS Parameter Store.

> Patrón Externalized configuration: suministrar al servicio los valores de configuración en tiempo de ejecución.

Dos enfoques:

- Push model: la infraestructura de despliegue pasa las propiedades al crear la instancia (variables de entorno o archivo de configuración). Spring Boot lee propiedades de varias fuentes con precedencia definida (argumentos de línea de comandos, `SPRING_APPLICATION_JSON`, propiedades del sistema JVM, variables de entorno del SO, archivo de configuración) y las inyecta con `@Value`. Limitaciones: reconfigurar un servicio en ejecución puede ser imposible y las propiedades quedan dispersas entre muchos servicios.
- Pull model: la instancia lee su configuración de un configuration server al arrancar (la configuración para acceder al server se le pasa vía push). Implementaciones: sistemas de control de versiones como Git, bases SQL/NoSQL, o servidores especializados (Spring Cloud Config Server, Hashicorp Vault, AWS Parameter Store). Beneficios: configuración centralizada, descifrado transparente de datos sensibles y reconfiguración dinámica. Inconveniente: es otra pieza de infraestructura que mantener.

## Designing observable services (11.3)

La mayoría de patrones tienen un componente de desarrollador y otro de operaciones. Patrones:

- Health check API: el servicio expone un endpoint que devuelve su salud. Spring Boot Actuator implementa `GET /actuator/health` (200 si está sano, 503 si no); HealthChecks .NET usa `GET /hc`. El handler suele probar las conexiones a servicios externos (p. ej. una query de prueba a la base de datos) o ejecutar una synthetic transaction. En Spring Boot se personaliza implementando la interfaz `HealthIndicator` con su método `health()`. La infraestructura de despliegue (o un service registry como Netflix Eureka) invoca periódicamente el endpoint.
- Log aggregation: enviar los logs de todas las instancias a un servidor de logging centralizado que permita búsqueda y alertas. Librerías Java: Logback, log4j, JUL y la fachada SLF4J; Log4JS en NodeJS. Con tecnologías modernas (contenedores, serverless como AWS Lambda) el servicio debe loguear a stdout. Infraestructura popular: el stack ELK (Elasticsearch, Logstash, Kibana); otros pipelines: Fluentd, Apache Flume; servidores: AWS CloudWatch Logs.
- Distributed tracing: asigna un ID único a cada petición externa y registra el árbol de llamadas entre servicios; es análogo a un performance profiler del monolito. Un trace representa una petición externa y se compone de spans (operación con nombre, timestamp de inicio y fin), que pueden tener spans hijos. El traceId se incluye en los logs (vía el Mapped Diagnostic Context de SLF4J). Dos partes: una instrumentation library en cada servicio (gestiona traces y spans, propaga estado con cabeceras del estándar B3 como `X-B3-TraceId` y `X-B3-ParentSpanId`) y un distributed tracing server. Spring Cloud Sleuth usa AOP para integrar el trazado automáticamente. Servidores: OpenZipkin (creado por Twitter) y AWS X-Ray.
- Application metrics: los servicios reportan métricas a un servidor central que agrega, visualiza y alerta. Una muestra tiene Name, Value y Timestamp, y opcionalmente dimensions (pares nombre-valor). En Spring Boot se usa la librería Micrometer; `OrderService` incrementa counters como `placed_orders`, `approved_orders` y `rejected_orders` mediante `MeterRegistry`. Entrega push (AWS CloudWatch) o pull (Prometheus, que sondea `GET /actuator/prometheus`). Visualización con Grafana.
- Exception tracking: reportar excepciones a un servicio que las deduplica, alerta y gestiona su resolución. Mejor que buscarlas en logs (los logs son de una línea, las excepciones multilínea, no hay seguimiento de resolución ni deduplicación). Servicios: Honeybadger (cloud), Sentry.io (tiene versión open source). Se integra con una client library (p. ej. un Servlet Filter).
- Audit logging: registrar las acciones de cada usuario (identidad, acción y objetos de negocio) para soporte, cumplimiento y detección de comportamiento sospechoso. Tres formas: añadir código de auditoría en la lógica de negocio (intertwines código y reduce mantenibilidad), usar AOP (más fiable, pero el advice solo ve nombre y argumentos del método) o usar event sourcing (provee audit log automático de create/update, pero no registra queries).

## Developing services using the Microservice chassis pattern (11.4)

Implementar desde cero todos estos concerns retrasaría el desarrollo días o semanas.

> Patrón Microservice chassis: construir los servicios sobre un framework que maneja los cross-cutting concerns (configuración externalizada, health checks, métricas, service discovery, circuit breakers, trazado distribuido, logging, seguimiento de excepciones).

FTGO usa Spring Boot (configuración externalizada) y Spring Cloud (circuit breakers, client-side service discovery) como chassis. Para GoLang existen Go Kit y Micro. Inconveniente: se necesita un chassis por cada combinación lenguaje/plataforma.

De chassis a service mesh: un service mesh es una capa de infraestructura de red por la que pasa todo el tráfico del servicio. Implementa circuit breakers, distributed tracing, service discovery, load balancing, rule-based traffic routing y comunicación segura con TLS-based IPC. Con él, el chassis se simplifica (solo configuración externalizada y health checks, propagando las cabeceras B3). Separa el deployment del release. Implementaciones: Istio, Linkerd (la más madura al momento de escribir) y Conduit.

## Ideas clave

- La seguridad a nivel de aplicación en microservicios cambia en cómo se pasa la identidad entre gateway y servicios y en quién autentica y autoriza; el resto es igual que en un monolito.
- El API gateway centraliza la autenticación y pasa un token transparente (JWT) a los servicios; OAuth 2.0 es una buena base.
- Un JWT es irrevocable por autocontenido: se mitiga con expiraciones cortas y refresh tokens.
- La configuración se externaliza con modelo push (variables de entorno o archivo) o pull (configuration server como Spring Cloud Config); los secretos van en Vault o Parameter Store.
- Los seis patrones de observabilidad (health check API, log aggregation, distributed tracing, exception tracking, application metrics, audit logging) reparten responsabilidad entre desarrolladores y operaciones.
- Un trace se compone de spans; el traceId en los logs permite correlacionar entradas de una misma petición.
- El Microservice chassis evita reimplementar concerns transversales en cada servicio, pero exige uno por lenguaje/plataforma.
- El service mesh mueve las funciones de red fuera del servicio y permite separar deployment de release.
