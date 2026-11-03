# Developing production-ready services — Estudio

## Tarjetas de repaso

P: ¿Qué tres atributos de calidad críticos debe satisfacer un servicio para estar listo para producción? / R: Seguridad, configurabilidad y observabilidad.

P: ¿Cuáles son los cuatro aspectos de seguridad de los que es responsable el desarrollador? / R: Authentication, authorization, auditing y secure interprocess communication (idealmente sobre TLS).

P: ¿Qué combina la autorización en los servicios? / R: Role-based security (roles como CONSUMER, RESTAURANT, COURIER, ADMIN) y ACLs sobre objetos de negocio o aggregates concretos.

P: ¿Qué dos elementos del monolito son inviables en microservicios para la seguridad? / R: El in-memory security context (los servicios no comparten memoria) y la centralized session (una sesión en BD compartida violaría el bajo acoplamiento).

P: ¿En qué consiste el patrón Access token? / R: El API gateway pasa un token con información del usuario (identidad y roles) a los servicios que invoca.

P: ¿Qué diferencia a los opaque tokens de los transparent tokens? / R: Los opaque (UUID) obligan a una llamada RPC síncrona al servicio de seguridad para validar, reduciendo rendimiento y disponibilidad; los transparent (JWT) son autocontenidos con payload JSON firmado.

P: ¿Por qué un JWT es irrevocable y cómo se mitiga? / R: Porque es autocontenido; se mitiga emitiéndolo con expiración corta, lo que obliga a reemitirlo (con refresh tokens) para mantener la sesión.

P: ¿Cuáles son los conceptos clave de OAuth 2.0? / R: Authorization Server (emite access y refresh token), Access Token, Refresh Token (revocable, larga vida), Resource Server (los servicios) y Client (el API gateway).

P: ¿Qué establece el patrón Externalized configuration? / R: Suministrar al servicio los valores de configuración en tiempo de ejecución, sin cablearlos en el código.

P: ¿Qué diferencia al push model del pull model de configuración? / R: En push, la infraestructura de despliegue pasa las propiedades al crear la instancia (variables de entorno o archivo); en pull, la instancia lee su configuración de un configuration server al arrancar.

P: ¿Qué es un trace en distributed tracing y de qué se compone? / R: Un trace representa una petición externa y se compone de spans (operación con nombre y timestamps de inicio y fin), que pueden tener spans hijos.

P: ¿Cuáles son los seis patrones de observabilidad? / R: Health check API, log aggregation, distributed tracing, application metrics, exception tracking y audit logging.

P: ¿Qué compone una muestra de application metrics? / R: Name, Value y Timestamp, y opcionalmente dimensions (pares nombre-valor).

P: ¿Qué establece el patrón Microservice chassis? / R: Construir los servicios sobre un framework que maneja los cross-cutting concerns (configuración externalizada, health checks, métricas, service discovery, circuit breakers, trazado distribuido, logging y seguimiento de excepciones).

P: ¿Qué es un service mesh y qué permite separar? / R: Una capa de infraestructura de red por la que pasa todo el tráfico del servicio; permite separar el deployment del release.

## Preguntas de autoevaluación

P: ¿Por qué conviene centralizar la autenticación en el API gateway en lugar de dejar que cada servicio autentique? / R: Porque dejar que cada servicio autentique arriesga permitir peticiones no autenticadas en la red interna y obliga a manejar múltiples mecanismos; el gateway autentica y reenvía un token en cada petición. (Sección 11.1, Developing secure services)

P: ¿Qué inconvenientes tiene realizar la autorización en el API gateway? / R: Acopla el gateway a los servicios y no es práctico implementar ACLs por objeto de dominio; por eso los servicios hacen role-based para URLs/métodos más ACLs sobre aggregates. (Sección 11.1)

P: ¿Por qué no deben guardarse los datos sensibles de configuración en el código fuente? / R: Porque crea vulnerabilidades y obliga a reconstruir el servicio por cada entorno; los secretos deben ir en un secrets storage como Hashicorp Vault o AWS Parameter Store. (Sección 11.2, Designing configurable services)

P: ¿Qué beneficios aporta el pull model frente a sus inconvenientes? / R: Beneficios: configuración centralizada, descifrado transparente de datos sensibles y reconfiguración dinámica; inconveniente: es otra pieza de infraestructura que mantener. (Sección 11.2)

P: ¿Cómo valida el health check API la salud de un servicio y quién lo invoca? / R: El handler prueba conexiones a servicios externos (p. ej. una query de prueba a la BD) o ejecuta una synthetic transaction; lo invoca periódicamente la infraestructura de despliegue o un service registry como Netflix Eureka. (Sección 11.3, Designing observable services)

P: ¿Por qué el exception tracking es mejor que buscar excepciones en los logs? / R: Porque los logs son de una línea y las excepciones multilínea, no hay seguimiento de resolución ni deduplicación; un servicio de exception tracking deduplica, alerta y gestiona la resolución. (Sección 11.3)

P: ¿Cuáles son las tres formas de implementar audit logging y qué limita a cada una? / R: Código en la lógica de negocio (intertwines código y reduce mantenibilidad), AOP (más fiable, pero el advice solo ve nombre y argumentos del método) y event sourcing (audit log automático de create/update, pero no registra queries). (Sección 11.3)

P: ¿Cómo evoluciona el chassis al adoptar un service mesh? / R: El chassis se simplifica a solo configuración externalizada y health checks (propagando las cabeceras B3), ya que el mesh asume circuit breakers, distributed tracing, service discovery, load balancing, enrutamiento y TLS. (Sección 11.4, Microservice chassis)

## Puntos a dominar

- Distinguir los tres atributos de producción (seguridad, configurabilidad, observabilidad) y sus patrones asociados.
- Explicar cómo se pasa la identidad entre gateway y servicios con el patrón Access token y tokens transparentes (JWT).
- Describir el flujo OAuth 2.0: Authorization Server, access/refresh token, Resource Server y Client, con Password Grant y Refresh Grant.
- Comparar push y pull model de Externalized configuration y ubicar los secretos en Vault o Parameter Store.
- Enumerar los seis patrones de observabilidad y su reparto entre desarrollador y operaciones.
- Explicar la relación trace–span y el uso del traceId en los logs para correlacionar una misma petición.
- Justificar el Microservice chassis frente a reimplementar concerns y reconocer su límite (uno por lenguaje/plataforma).
- Explicar qué mueve el service mesh fuera del servicio y por qué separa deployment de release.
