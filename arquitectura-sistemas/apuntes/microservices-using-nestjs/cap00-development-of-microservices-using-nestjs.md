# Development of Microservices Using NestJS: Architecture and Practical Examples — V. Dolzhenko (Universum: Technical Sciences, 2024)
## Prólogo — Development of Microservices Using NestJS (Desarrollo de microservicios usando NestJS)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Este trabajo es un artículo compacto que presenta el framework NestJS como herramienta para desarrollar microservicios. NestJS se basa en Node.js y TypeScript, usa JavaScript progresivo y, al apoyarse en Express, hereda las técnicas de implementación del patrón MVC (Model-View-Controller) aplicables a Express. Su tesis central es que NestJS ofrece herramientas eficaces para crear aplicaciones de servidor escalables mediante técnicas modernas de programación.

El texto sostiene que dos rasgos de NestJS lo hacen especialmente adecuado para microservicios: un sistema avanzado de inyección de dependencias (Dependency Injection, DI) y el soporte de distintos patrones de programación, que favorecen aplicaciones modulares y testeables. A lo largo del artículo se analizan los aspectos clave de la arquitectura de microservicios —despliegue independiente, escalabilidad y mantenimiento ligero— y cómo NestJS mejora la gestión de la complejidad y aumenta la flexibilidad en sistemas complejos.

Al terminar sales sabiendo qué elementos básicos componen una aplicación NestJS (módulos, controladores y servicios), cómo la arquitectura de microservicios responde a los problemas de las aplicaciones monolíticas, qué protocolos de comunicación admite NestJS y qué papel juega Docker en el despliegue. El artículo combina explicación conceptual con referencias a ejemplos de código (presentados como figuras en el PDF).

## Elementos de NestJS

Los conceptos principales con los que trabaja un desarrollador en NestJS son módulos, controladores y servicios, clave para entender y usar la plataforma con eficacia:

- Módulos: organizan la lógica en piezas de código reutilizables (componentes).
- Controladores: manejan operaciones REST (métodos HTTP).
- Servicios: gestionan la lógica y la funcionalidad; sus métodos se invocan desde el controlador.

Otras características destacadas:

- Sistema de inyección de dependencias (DI) con un contenedor integrado que gestiona automáticamente las dependencias de las clases, promoviendo modularidad, testabilidad y reutilización de código.
- Uso intensivo de decoradores, una característica de TypeScript que permite adjuntar metadatos a clases, métodos y propiedades; simplifican el enrutamiento, la integración de middleware y la validación de entradas, reduciendo código repetitivo.
- Soporte de middleware para añadir lógica al ciclo petición/respuesta, con control granular del flujo de datos y facilidad para integrar autenticación, logging y manejo de errores.
- Arquitectura modular que favorece la separación y organización del código, encapsulando funcionalidad relacionada en módulos reutilizables entre microservicios.
- Soporte de varios protocolos de transporte: HTTP, WebSockets y TCP, para elegir el mecanismo de comunicación óptimo.

## De monolito a microservicios

El artículo describe las dificultades típicas del desarrollo monolítico: al actualizar código hay que volver a ejecutar todo el sistema en pruebas y despliegue, lo que ralentiza el proceso; ante errores, el servidor entero puede quedar inaccesible por la dificultad de localizar problemas; y ampliar la funcionalidad puede exigir una refactorización significativa.

Frente a esto, la arquitectura de microservicios propone refactorizar aplicaciones monolíticas masivas en servicios independientes. Los microservicios no están atados a una tecnología concreta: son un conjunto de enfoques arquitectónicos donde cada servicio opera de forma autónoma. Sus características principales:

- Independencia funcional de los módulos, eliminando interdependencias de código entre servicios y mejorando la extensibilidad.
- Capacidad de desplegar cada módulo de forma independiente, acelerando el despliegue y facilitando la detección de errores.

El texto advierte que hay que sopesar beneficios (gestión simplificada, mayor escalabilidad) frente al posible aumento de complejidad y coste, aplicando microservicios solo cuando esté justificado. Los escenarios adecuados son proyectos grandes o aplicaciones extensas.

En NestJS, la arquitectura de microservicios admite protocolos como TCP y modos de comunicación request-response y event-driven. Para empezar, se recomienda un framework simple: una plataforma de microservicios basada en Nest que use TCP como protocolo por defecto. El proyecto principal y los microservicios residen en directorios distintos y requieren arranque separado (por ejemplo, `main-service`, `auth-service`, `data-service`, `notification-service`). Cada microservicio incluye un archivo `app.module.ts` que define sus módulos, servicios y controladores. La interacción se realiza vía TCP usando los decoradores `@MessagePattern` y `@EventPattern` para procesar peticiones y eventos de forma asíncrona.

## Impacto de la arquitectura de microservicios

La arquitectura de microservicios ha influido notablemente en el diseño y los enfoques modernos de desarrollo. Es un método escalable y adaptable: el sistema se descompone en muchos servicios pequeños e independientes que sirven como bloques de construcción de ecosistemas digitales de gran escala, cada uno especializado en una función de negocio. El artículo resalta sus ventajas:

- Escalabilidad: a diferencia del monolito, que escala toda la aplicación, los microservicios permiten escalar componentes de forma independiente, con asignación de recursos más eficiente, mejor rendimiento y menor coste.
- Soporte y mantenimiento más fáciles: al estar aislados y tener su propio código, los servicios son más fáciles de probar y modificar, reduciendo el riesgo de errores y efectos secundarios.
- Flexibilidad tecnológica: cada equipo puede elegir la tecnología más adecuada para su servicio y actualizarlo sin arriesgar el sistema completo.

Como contrapartida, implementar microservicios implica complejidades como gestionar las interacciones entre servicios y asegurar la consistencia de datos. NestJS aporta herramientas robustas —inyección de dependencias, decoradores y soporte de middleware— que simplifican esa gestión.

## Docker para desplegar microservicios

Gestionar y desplegar múltiples servicios requiere las herramientas adecuadas, y aquí destaca Docker, plataforma de código abierto que permite construir, empaquetar y distribuir aplicaciones en contenedores ligeros y portátiles. Beneficios señalados:

- Escalabilidad: los servicios se contenerizan y escalan de forma independiente, con asignación eficiente de recursos y estabilidad ante cargas crecientes.
- Aislamiento y seguridad: cada contenedor opera en un entorno aislado, lo que minimiza el riesgo de que un fallo afecte a otros, reduce los fallos en cascada y aísla del sistema operativo anfitrión, disminuyendo accesos no autorizados y fugas de datos.
- Docker Compose: define y organiza aplicaciones multicontenedor con un simple archivo YAML, estableciendo de forma declarativa parámetros, dependencias y red, y desplegando con un solo comando.
- Ecosistema de imágenes preconfiguradas en Docker Hub, el registro oficial, que sirven de base para construir microservicios y facilitan la colaboración entre equipos.

## Ideas clave

- NestJS se basa en Node.js y TypeScript y, al usar Express, hereda las técnicas del patrón MVC.
- Los tres elementos fundamentales son módulos (código reutilizable), controladores (operaciones REST/HTTP) y servicios (lógica invocada desde el controlador).
- El sistema de inyección de dependencias y los decoradores de TypeScript favorecen modularidad, testabilidad y menos código repetitivo.
- Los microservicios responden a los problemas del monolito mediante independencia funcional y despliegue independiente, pero conviene usarlos solo cuando están justificados.
- En NestJS la comunicación entre servicios usa TCP con los decoradores `@MessagePattern` y `@EventPattern`, en modos request-response y event-driven.
- Las ventajas principales de los microservicios son escalabilidad independiente, mantenimiento más sencillo y flexibilidad tecnológica.
- Docker, con contenedores, Docker Compose y Docker Hub, simplifica el despliegue aportando escalabilidad, aislamiento y seguridad.
