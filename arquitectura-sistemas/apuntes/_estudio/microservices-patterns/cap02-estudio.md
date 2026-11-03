# Decomposition strategies (Estrategias de descomposición) — Estudio

## Tarjetas de repaso

P: ¿Qué es la arquitectura de software según la definición citada de Len Bass y colegas? / R: "The set of structures needed to reason about the system": elementos de software, relaciones entre ellos y propiedades de ambos.

P: ¿Por qué importa la descomposición arquitectónica? / R: Facilita la división del trabajo y del conocimiento, define cómo interactúan los elementos y determina los atributos de calidad (*-ilities*).

P: ¿Cuáles son las cuatro vistas del modelo 4+1 de Krutchen? / R: Logical view (clases y paquetes), Implementation view (salida del build), Process view (componentes en ejecución) y Deployment view (mapeo de procesos a máquinas). El +1 son los *scenarios*.

P: ¿Qué define un estilo arquitectónico? / R: Una familia de sistemas con un patrón de organización estructural, un vocabulario limitado de componentes y conectores, y restricciones sobre cómo combinarlos (Garlan y Shaw).

P: ¿Qué caracteriza al estilo hexagonal? / R: Coloca la lógica de negocio en el centro; los inbound adapters invocan inbound ports y los outbound adapters implementan outbound ports. La lógica no depende de los adapters, sino al revés.

P: ¿Cómo define Richardson el patrón Microservice architecture? / R: Estructurar la aplicación como una colección de servicios débilmente acoplados y desplegables de forma independiente.

P: ¿De qué consta la API de un servicio? / R: De commands (p. ej. `createOrder()`, actualizan datos), queries (p. ej. `findOrderById()`, recuperan datos) y events (p. ej. `OrderCreated`) a los que los clientes se suscriben.

P: ¿Qué implica el loose coupling entre servicios? / R: Que toda interacción ocurre vía la API y que se prohíbe comunicarse a través de una base de datos compartida; los datos persistentes son campos privados del servicio.

P: ¿Cuándo conviene usar bibliotecas compartidas? / R: Solo para funcionalidad que es poco probable que cambie (p. ej. una clase `Money`); empaquetar funcionalidad que cambia introduce acoplamiento.

P: ¿Cuáles son los tres pasos para definir la arquitectura de microservicios? / R: Identificar las operaciones del sistema, determinar la descomposición en servicios y definir las APIs de los servicios y sus colaboraciones.

P: ¿Qué es una business capability y por qué sirve para descomponer? / R: Algo que el negocio hace para generar valor; captura el *qué* (estable) frente al *cómo* (cambiante), por lo que produce una arquitectura estable.

P: ¿Qué es un bounded context en DDD y cómo se relaciona con microservicios? / R: El alcance explícito de un modelo de dominio; en microservicios corresponde a un servicio (o varios).

P: ¿Qué enuncian el SRP y el CCP de Robert C. Martin? / R: SRP: "A class should have only one reason to change". CCP: las clases que cambian por la misma razón deben estar juntas; aplicado a servicios, es el antídoto contra el distributed monolith.

P: ¿Qué es una god class y cómo la resuelve DDD? / R: Una clase inflada con lógica de muchos aspectos (como `Order` en FTGO). DDD la resuelve dando a cada servicio su propio modelo: `Delivery` en Delivery Service, `Ticket` en Kitchen Service y una vista más simple en Order Service.

P: ¿Qué es un distributed monolith? / R: El resultado de una mala descomposición: un servicio que cambia constantemente por cambios en otros servicios, sin la independencia de despliegue esperada.

## Preguntas de autoevaluación

P: ¿Por qué la arquitectura elegida importa más para los requisitos de calidad que para los funcionales? / R: Porque los requisitos funcionales se pueden implementar con casi cualquier arquitectura (incluso un big ball of mud), mientras que los atributos de calidad de servicio dependen de la arquitectura elegida. (Sección "¿Qué es exactamente la arquitectura de microservicios?")

P: ¿Cuáles son los inconvenientes del estilo layered three-tier que señala el capítulo? / R: Una única capa de presentación, una única capa de persistencia, y que define la lógica de negocio como dependiente de la persistencia cuando las dependencias deberían invertirse. (Sección "Estilos arquitectónicos")

P: ¿Por qué el tamaño del servicio es irrelevante según el capítulo? / R: Porque la meta es un servicio que pueda desarrollar un equipo pequeño con mínimo tiempo de entrega y mínima colaboración con otros equipos, no un tamaño concreto. (Sección "Microservicios como estilo arquitectónico")

P: ¿En qué se diferencia DDD del modelado empresarial tradicional? / R: El modelado tradicional usa un único modelo de dominio; DDD define múltiples modelos, cada uno con un alcance explícito (bounded context) y su Ubiquitous Language. (Sección "Decompose by subdomain")

P: ¿Cómo se identifican las operaciones del sistema? / R: Con un proceso de dos pasos inspirado en Craig Larman: primero un high-level domain model (sustantivos de las user stories) y luego las operaciones del sistema (verbos), que son commands o queries. (Sección "Identificar las operaciones del sistema")

P: ¿Por qué la comunicación síncrona puede reducir la disponibilidad? / R: Porque invocar servicios vía REST síncrono hace que un servicio no pueda operar si otro del que depende está caído; suele ser mejor la mensajería asíncrona. (Sección "Obstáculos a la descomposición")

P: ¿Cómo se mantiene la consistencia de datos entre servicios sin commit en dos fases? / R: Con sagas: secuencias de transacciones locales coordinadas por mensajería, eventualmente consistentes. (Sección "Obstáculos a la descomposición")

P: ¿Por qué existe una operación de API de un servicio? / R: O bien porque corresponde a una operación del sistema invocada por clientes externos u otros servicios, o bien para soportar la colaboración entre servicios. (Sección "Definir las APIs de los servicios")

## Puntos a dominar

- Distinguir las cuatro vistas del modelo 4+1 y qué organiza cada estilo (layered y hexagonal la logical view; monolito y microservicios la implementation view).
- Explicar el patrón Microservice architecture y por qué cada servicio suele ser hexagonal internamente.
- Describir la API de un servicio en términos de commands, queries y events, y por qué nadie puede eludirla.
- Justificar el loose coupling: interacción solo vía API y prohibición de base de datos compartida.
- Reproducir los tres pasos para definir la arquitectura de microservicios.
- Contrastar Decompose by business capability y Decompose by subdomain y su alineación con DDD.
- Aplicar SRP y CCP como guías de descomposición y reconocer cómo CCP evita el distributed monolith.
- Enumerar los cinco obstáculos a la descomposición (latencia, disponibilidad por comunicación síncrona, consistencia de datos, vistas consistentes y god classes) y su mitigación.
- Explicar cómo DDD elimina la god class `Order` de FTGO dando a cada servicio su propio modelo.
