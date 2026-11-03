# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 1 — Escaping monolithic hell (Escapando del infierno monolítico)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo plantea el problema que recorre todo el libro: las aplicaciones monolíticas exitosas acaban superando su propia arquitectura y caen en lo que el autor llama "monolithic hell" (infierno monolítico), un estado donde el desarrollo se vuelve lento, penoso y poco fiable. La tesis central es que la cura para una aplicación grande y compleja es migrar a la arquitectura de microservicios, entendida como la descomposición funcional de la aplicación en un conjunto de servicios con límites bien definidos.

Richardson define los microservicios apoyándose en el *scale cube* (cubo de escalabilidad) y presenta sus características esenciales: servicios poco acoplados que se comunican solo vía APIs y donde cada servicio tiene su propia base de datos. También expone de forma equilibrada los beneficios y los inconvenientes, insistiendo en que los microservicios no son una "bala de plata" (silver bullet).

Al terminar el capítulo sabes reconocer los síntomas del infierno monolítico, entiendes qué es (y qué no es) la arquitectura de microservicios, conoces sus ventajas y desventajas, y tienes una visión general del *Microservice architecture pattern language* (lenguaje de patrones de arquitectura de microservicios) que estructura el resto del libro. Además queda claro que la arquitectura por sí sola no basta: hace falta combinarla con DevOps y equipos pequeños y autónomos.

## El ejemplo que recorre el capítulo

El hilo conductor es FTGO (Food to Go, Inc.), una empresa líder de reparto de comida a domicilio en EE. UU. lanzada a finales de 2005. Su CTO, Mary, vuelve de una conferencia convencida de que FTGO sufre de infierno monolítico y de que la solución son los microservicios, pero no sabe cómo combatir los incendios del día a día mientras mejora la forma de desarrollar software.

La aplicación FTGO es una aplicación Java empresarial típica, empaquetada como un único archivo WAR, con una arquitectura hexagonal: lógica de negocio en el centro rodeada de adaptadores de entrada (REST API, Web UI) y de salida (base de datos MySQL, servicios cloud como Stripe para pagos, Twilio para mensajería y Amazon SES para email). Pese a ser lógicamente modular, se ha convertido en un ejemplo del patrón *Big Ball of Mud* (gran bola de barro).

## El lento avance hacia el infierno monolítico

Al principio la arquitectura monolítica tuvo muchos beneficios: simple de desarrollar, fácil de hacer cambios radicales, sencilla de probar (tests de extremo a extremo con Selenium), sencilla de desplegar (copiar el WAR a un Tomcat) y fácil de escalar (varias instancias tras un balanceador de carga).

Con el tiempo FTGO superó su arquitectura y entró en el infierno monolítico, con estos síntomas:

- La complejidad intimida a los desarrolladores: la aplicación es demasiado grande para que alguien la entienda del todo, lo que forma una espiral descendente.
- El desarrollo es lento: el IDE va sobrecargado, la compilación y el arranque tardan, y el ciclo editar-compilar-ejecutar-probar se alarga.
- El camino del commit al despliegue es largo y arduo: se despliega una vez al mes, con ramas de funcionalidades que provocan *merges* dolorosos y pruebas que tardan días (incluso manuales). Se cita que Amazon.com en 2011 desplegaba un cambio cada 11,6 segundos.
- Escalar es difícil: módulos con requisitos de recursos en conflicto (p. ej., datos de restaurantes en memoria vs. procesamiento de imágenes intensivo en CPU) obligan a compromisos en la configuración del servidor.
- Entregar un monolito fiable es un reto: sin aislamiento de fallos, un fallo en un módulo (como una fuga de memoria) tumba todas las instancias.
- Bloqueo en una pila tecnológica cada vez más obsoleta: no pueden actualizar frameworks ni experimentar con lenguajes no-JVM como GoLang o NodeJS.

## La arquitectura de microservicios al rescate

La arquitectura importa por los atributos de calidad (requisitos no funcionales o *ilities*), sobre todo mantenibilidad, extensibilidad y testabilidad, que condicionan la velocidad de entrega.

El **scale cube** de *The Art of Scalability* define tres formas de escalar:

- **Eje X** (duplicación horizontal): clonar; varias instancias idénticas tras un balanceador.
- **Eje Z** (partición de datos): varias instancias idénticas, pero cada una responsable de un subconjunto de datos, enrutando por un atributo de la petición (p. ej., `userId`).
- **Eje Y** (descomposición funcional): dividir la aplicación en servicios según función.

La definición de alto nivel: la arquitectura de microservicios es un estilo arquitectónico que descompone funcionalmente (eje Y) la aplicación en un conjunto de servicios; la definición no habla de tamaño, sino de responsabilidades cohesivas y enfocadas. Un servicio puede a su vez escalarse en los ejes X y Z.

Puntos clave:

- **Microservicios como forma de modularidad**: un servicio tiene una API que es una frontera impermeable, difícil de violar, lo que preserva la modularidad mejor que los paquetes Java.
- **Cada servicio tiene su propia base de datos**: logra el acoplamiento débil; se puede cambiar el esquema sin coordinar con otros y en ejecución los servicios están aislados. Tener BD por servicio no obliga a un servidor de BD por servicio.
- **FTGO con microservicios**: servicios frontend (API Gateway, Restaurant Web UI) y backend con API REST y datastore privado: Order Service, Delivery Service, Restaurant Service, Kitchen Service, Accounting Service.

### Microservicios frente a SOA

Aunque ambos estructuran el sistema como un conjunto de servicios, difieren:

| | SOA | Microservicios |
|---|---|---|
| Comunicación | Tuberías inteligentes (ESB), protocolos pesados (SOAP, WS*) | Tuberías tontas (message broker o comunicación directa), protocolos ligeros (REST, gRPC) |
| Datos | Modelo de datos global y bases de datos compartidas | Modelo de datos y base de datos por servicio |
| Servicio típico | Aplicación monolítica grande | Servicio más pequeño |

## Beneficios e inconvenientes

**Beneficios:**

- Permite la entrega y despliegue continuos de aplicaciones grandes y complejas (por testabilidad, desplegabilidad y equipos autónomos, p. ej., equipos "two-pizza").
- Cada servicio es pequeño y fácil de mantener.
- Servicios desplegables de forma independiente.
- Servicios escalables de forma independiente, cada uno en el hardware más adecuado.
- Permite que los equipos sean autónomos.
- Facilita experimentar y adoptar nuevas tecnologías sin compromiso a largo plazo.
- Mejor aislamiento de fallos.

**Inconvenientes:**

- Encontrar el conjunto correcto de servicios es difícil; descomponer mal produce un *distributed monolith* (monolito distribuido) con las desventajas de ambos mundos.
- Los sistemas distribuidos son complejos: IPC, fallos parciales, transacciones y consultas entre servicios (sagas, API composition, CQRS), herramientas y tests más difíciles, y mayor complejidad operativa (requiere automatización: Spinnaker, PaaS como Pivotal Cloud Foundry u OpenShift, orquestadores como Docker Swarm o Kubernetes).
- Desplegar funcionalidades que abarcan varios servicios exige coordinación cuidadosa.
- Decidir cuándo adoptarlos es difícil: una startup debería empezar casi siempre con un monolito y descomponer más tarde, cuando el problema sea la complejidad.

## El lenguaje de patrones de arquitectura de microservicios

No hay una bala de plata (Fred Brooks, *The Mythical Man-Month*); las discusiones sobre tecnología caen en la dicotomía "suck/rock" (Neal Ford) y en el *hype cycle* de Gartner. El formato de patrón es útil porque es objetivo y obliga a describir los inconvenientes.

Un **patrón** es una solución reutilizable a un problema en un contexto dado (concepto de Christopher Alexander); un **pattern language** es una colección de patrones relacionados. Una estructura de patrón valiosa incluye:

- **Forces** (fuerzas): los problemas que hay que resolver; pueden estar en conflicto y hay que priorizar.
- **Resulting context** (contexto resultante): beneficios, inconvenientes (*drawbacks*) e *issues* nuevos introducidos.
- **Related patterns** (patrones relacionados): cinco relaciones: predecesor, sucesor, alternativa, generalización y especialización.

El *Microservice architecture pattern language* primero ayuda a decidir entre arquitectura monolítica y de microservicios, y luego a aplicarla. Se organiza en tres capas (infraestructura, infraestructura de aplicación y aplicación) y en grupos por área de problema: descomposición (por capacidad de negocio o por subdominio DDD), comunicación (estilo, descubrimiento, fiabilidad, mensajería transaccional, API externa), consistencia de datos (Saga, Database per service, Event sourcing, Domain event, Aggregate), consultas (API composition, CQRS), despliegue (Single service per host, service-per-container, service-per-VM, serverless), observabilidad (Health check API, Log aggregation, Distributed tracing, Exception tracking, Application metrics, Audit logging), pruebas (contract tests, Service component test), preocupaciones transversales (Externalized Configuration, Microservice Chassis) y seguridad (Access token, p. ej., JWT).

## Más allá de los microservicios: proceso y organización

La arquitectura sola no basta. La entrega rápida, frecuente y fiable requiere combinar microservicios con una organización adecuada y procesos de desarrollo.

- **Organización**: refactorizar un gran equipo único en un "team of teams" (equipo de equipos), cada uno pequeño (8-12 personas), transfuncional y con una misión orientada al negocio. Hay que aplicar la ley de Conway en reverso (*reverse Conway maneuver*): diseñar la organización para que su estructura refleje la arquitectura de microservicios.
- **Proceso**: adoptar desarrollo ágil (Scrum, Kanban) y, mejor aún, entrega/despliegue continuos como parte de DevOps. Métricas útiles: frecuencia de despliegue, *lead time*, tiempo medio de recuperación y tasa de fallo de cambios.
- **Lado humano**: adoptar microservicios cambia el entorno de trabajo de personas que son emocionales. El modelo de transición de *Managing Transitions* (Bridges) tiene tres etapas: Ending/Losing/Letting Go, The Neutral Zone y The New Beginning.

## Ideas clave

- El patrón Monolithic architecture estructura la aplicación como una única unidad desplegable; el patrón Microservice architecture la descompone en servicios desplegables de forma independiente, cada uno con su propia base de datos.
- El monolito es buena opción para aplicaciones simples; los microservicios suelen serlo para aplicaciones grandes y complejas.
- La arquitectura importa por los atributos de calidad (mantenibilidad, extensibilidad, testabilidad), no por los requisitos funcionales.
- Los microservicios son el eje Y del scale cube: descomposición funcional; el tamaño no es lo que los define, sino las responsabilidades cohesivas.
- Los microservicios aceleran la velocidad al permitir equipos pequeños y autónomos en paralelo, pero no son una bala de plata: añaden complejidad distribuida y operativa.
- El pattern language ayuda a decidir si usar microservicios y, si se eligen, a aplicarlos eficazmente mediante patrones por área de problema.
- Se necesita más que arquitectura: también DevOps, equipos pequeños y autónomos, y atención al lado humano (modelo de transición) de la adopción.
