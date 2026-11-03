# Development of Microservices Using NestJS — Estudio

## Tarjetas de repaso

P: ¿Sobre qué tecnologías se basa NestJS? / R: Sobre Node.js y TypeScript; usa JavaScript progresivo y se apoya en Express.

P: ¿Qué patrón hereda NestJS al apoyarse en Express? / R: Las técnicas de implementación del patrón MVC (Model-View-Controller) aplicables a Express.

P: ¿Cuáles son los tres elementos fundamentales de una aplicación NestJS? / R: Módulos, controladores y servicios.

P: ¿Qué función cumple cada uno de esos tres elementos? / R: Los módulos organizan la lógica en código reutilizable; los controladores manejan operaciones REST (métodos HTTP); los servicios gestionan la lógica, invocada desde el controlador.

P: ¿Qué es el sistema de inyección de dependencias (DI) de NestJS? / R: Un contenedor integrado que gestiona automáticamente las dependencias de las clases, promoviendo modularidad, testabilidad y reutilización de código.

P: ¿Qué son los decoradores en NestJS? / R: Una característica de TypeScript que adjunta metadatos a clases, métodos y propiedades; simplifican enrutamiento, integración de middleware y validación, reduciendo código repetitivo.

P: ¿Para qué sirve el soporte de middleware? / R: Para añadir lógica al ciclo petición/respuesta con control granular del flujo de datos, integrando autenticación, logging y manejo de errores.

P: ¿Qué protocolos de transporte admite NestJS? / R: HTTP, WebSockets y TCP.

P: ¿Qué problemas presenta el desarrollo monolítico según el artículo? / R: Reejecutar todo el sistema al actualizar código, inaccesibilidad del servidor entero ante errores difíciles de localizar y necesidad de refactorización significativa al ampliar funcionalidad.

P: ¿Qué son los microservicios según el texto? / R: Un conjunto de enfoques arquitectónicos donde cada servicio opera de forma autónoma, no atado a una tecnología concreta.

P: ¿Cuáles son las dos características principales de los microservicios? / R: Independencia funcional de los módulos y capacidad de desplegar cada módulo de forma independiente.

P: ¿Qué protocolo y decoradores usa NestJS para la comunicación entre microservicios? / R: TCP como protocolo por defecto, con los decoradores `@MessagePattern` y `@EventPattern`, en modos request-response y event-driven.

P: ¿Cuáles son las ventajas principales de la arquitectura de microservicios? / R: Escalabilidad independiente, soporte y mantenimiento más fáciles, y flexibilidad tecnológica.

P: ¿Qué es Docker y qué beneficios aporta al despliegue? / R: Plataforma de código abierto para construir, empaquetar y distribuir aplicaciones en contenedores ligeros y portátiles; aporta escalabilidad, aislamiento y seguridad.

P: ¿Qué son Docker Compose y Docker Hub? / R: Docker Compose define aplicaciones multicontenedor con un archivo YAML declarativo; Docker Hub es el registro oficial de imágenes preconfiguradas.

## Preguntas de autoevaluación

P: ¿Por qué se considera a NestJS especialmente adecuado para microservicios? / R: Por su sistema avanzado de inyección de dependencias y el soporte de distintos patrones de programación, que favorecen aplicaciones modulares y testeables. (Sección: Lo que necesitas saber)

P: ¿Cómo responde la arquitectura de microservicios a los problemas del monolito? / R: Refactorizando la aplicación masiva en servicios independientes con independencia funcional y despliegue independiente, acelerando el despliegue y facilitando la detección de errores. (Sección: De monolito a microservicios)

P: ¿En qué escenarios conviene aplicar microservicios y por qué hay que sopesarlo? / R: En proyectos grandes o aplicaciones extensas, porque hay que equilibrar beneficios (gestión simplificada, escalabilidad) frente al posible aumento de complejidad y coste. (Sección: De monolito a microservicios)

P: ¿Cómo se organiza un proyecto de microservicios basado en Nest con TCP? / R: El proyecto principal y los microservicios residen en directorios distintos con arranque separado (p. ej. `main-service`, `auth-service`, `data-service`, `notification-service`), y cada uno define sus módulos, servicios y controladores en `app.module.ts`. (Sección: De monolito a microservicios)

P: ¿Qué contrapartidas implica implementar microservicios y cómo las aborda NestJS? / R: Gestionar las interacciones entre servicios y asegurar la consistencia de datos; NestJS lo simplifica con inyección de dependencias, decoradores y soporte de middleware. (Sección: Impacto de la arquitectura de microservicios)

P: ¿Cómo mejora la escalabilidad en microservicios respecto al monolito? / R: El monolito escala toda la aplicación, mientras que los microservicios permiten escalar componentes de forma independiente, con asignación de recursos más eficiente, mejor rendimiento y menor coste. (Sección: Impacto de la arquitectura de microservicios)

P: ¿Qué beneficios de aislamiento y seguridad aporta Docker? / R: Cada contenedor opera en un entorno aislado que minimiza que un fallo afecte a otros, reduce fallos en cascada y aísla del sistema operativo anfitrión, disminuyendo accesos no autorizados y fugas de datos. (Sección: Docker para desplegar microservicios)

## Puntos a dominar

- Identificar los tres elementos de NestJS (módulos, controladores, servicios) y la función de cada uno.
- Explicar el papel de la inyección de dependencias y de los decoradores en la modularidad y testabilidad.
- Contrastar los problemas del monolito con las características de la arquitectura de microservicios.
- Reconocer los protocolos de transporte de NestJS (HTTP, WebSockets, TCP) y los decoradores `@MessagePattern` y `@EventPattern`.
- Enumerar las ventajas de los microservicios (escalabilidad independiente, mantenimiento, flexibilidad tecnológica) y sus contrapartidas.
- Describir el papel de Docker, Docker Compose y Docker Hub en el despliegue de microservicios.
