# Conexiones entre libros

Este documento enlaza temas que aparecen en dos o más libros de la carpeta `arquitectura-sistemas/apuntes`, con base exclusiva en los `README.md` y `_glosario.md` de cada libro. Por cada tema se indica qué dice cada libro (con enlace relativo al capítulo correspondiente) y una frase sobre qué los conecta o en qué se diferencian. Solo se incluyen conexiones con respaldo explícito en los apuntes. Al final se recoge una lista de temas exclusivos de cada libro.

Libros considerados: Designing Data-Intensive Applications (DDIA), Microservices Patterns, Release It!, Clean Code, Refactoring, Dive Into Design Patterns, Acquiring Card Payments, Development of Microservices Using NestJS y Code Simplicity.

## Refactorización

- **Refactoring**: define refactoring como cambiar la estructura interna del código sin alterar su comportamiento observable, en pasos pequeños verificados con pruebas ([refactoring/cap02-principles-in-refactoring.md](refactoring/cap02-principles-in-refactoring.md)).
- **Clean Code**: presenta el refactoring como proceso iterativo de ensayo y error con pasos diminutos y pruebas verdes entre cada uno, no como reescritura ([clean-code/cap14-successive-refinement.md](clean-code/cap14-successive-refinement.md)).
- **Code Simplicity**: propone el rediseño en pasos pequeños como forma de manejar la complejidad sin introducir más, alternando rediseño y funciones ([simplicity-the-fundamentals-of-software/cap08-complexity.md](simplicity-the-fundamentals-of-software/cap08-complexity.md)).
- **Microservices Patterns**: aplica la refactorización a gran escala migrando incrementalmente un monolito con una strangler application en lugar de reescribirlo ([microservices-patterns/cap13-refactoring-to-microservices.md](microservices-patterns/cap13-refactoring-to-microservices.md)).

Los cuatro coinciden en mejorar código existente mediante cambios pequeños y seguros y en rechazar la reescritura total; difieren en la escala, desde el método (Refactoring, Clean Code) hasta el rediseño del sistema (Code Simplicity) y la migración de arquitectura completa (Microservices Patterns).

## Pruebas automatizadas como red de seguridad

- **Refactoring**: el código autocomprobable y JUnit son precondición para refactorizar con seguridad y reducir la depuración ([refactoring/cap04-building-tests.md](refactoring/cap04-building-tests.md)).
- **Clean Code**: el código de prueba es tan importante como el de producción, con TDD y las propiedades F.I.R.S.T. ([clean-code/cap09-unit-tests.md](clean-code/cap09-unit-tests.md)).
- **Code Simplicity**: la Ley de las Pruebas afirma que conoces el comportamiento de tu software solo en la medida en que lo has probado con precisión ([simplicity-the-fundamentals-of-software/cap09-testing.md](simplicity-the-fundamentals-of-software/cap09-testing.md)).
- **Microservices Patterns**: la pirámide de pruebas y el consumer-driven contract testing sostienen la entrega rápida en microservicios ([microservices-patterns/cap09-testing-microservices-part-1.md](microservices-patterns/cap09-testing-microservices-part-1.md)).

Todos tratan las pruebas automatizadas como base para cambiar el software con confianza; Refactoring y Clean Code las enfocan a la unidad, Code Simplicity las eleva a ley fundamental y Microservices Patterns las adapta a la frontera entre servicios con contratos.

## Principios SOLID

- **Dive Into Design Patterns**: dedica un capítulo a cada principio SOLID (SRP, OCP, LSP, ISP, DIP) como base del catálogo de patrones ([design-patterns/cap09-s-principio-de-responsabilidad-unica.md](design-patterns/cap09-s-principio-de-responsabilidad-unica.md)).
- **Clean Code**: las clases deben ser pequeñas y respetar SRP, OCP y DIP, con nombres comodín (`Manager`, `Processor`) que delatan la violación de SRP ([clean-code/cap10-classes.md](clean-code/cap10-classes.md)).
- **Microservices Patterns**: usa SRP y CCP en la descomposición para evitar el distributed monolith ([microservices-patterns/cap02-decomposition-strategies.md](microservices-patterns/cap02-decomposition-strategies.md)).

Los tres aplican los mismos principios de responsabilidad y acoplamiento, pero a escalas distintas: la clase (Design Patterns, Clean Code) frente al servicio (Microservices Patterns), que extiende SRP a la frontera de un microservicio.

## Simplicidad frente a complejidad

- **Code Simplicity**: la Ley de la Simplicidad liga la facilidad de mantenimiento a la simplicidad de las piezas individuales, y sostiene que la complejidad se acumula sobre sí misma ([simplicity-the-fundamentals-of-software/cap07-simplicity.md](simplicity-the-fundamentals-of-software/cap07-simplicity.md)).
- **Clean Code**: entre las cuatro reglas del Diseño Simple de Kent Beck figuran eliminar duplicación y minimizar clases y métodos ([clean-code/cap12-emergence.md](clean-code/cap12-emergence.md)).
- **DDIA**: la mantenibilidad se apoya en operabilidad, simplicidad y evolvability como cualidades del sistema de datos ([designing-data-intensive-applications/cap01-reliable-scalable-and-maintainable-applications.md](designing-data-intensive-applications/cap01-reliable-scalable-and-maintainable-applications.md)).

Los tres sitúan la simplicidad como clave de la mantenibilidad; Code Simplicity y Clean Code la buscan en el código y el diseño, mientras DDIA la enmarca como atributo de un sistema de datos distribuido.

## Transacciones distribuidas y 2PC/XA

- **DDIA**: describe el two-phase commit (2PC) como protocolo de commit atómico distribuido y el estándar XA, que amplifica fallos y causa problemas operativos ([designing-data-intensive-applications/cap09-consistency-and-consensus.md](designing-data-intensive-applications/cap09-consistency-and-consensus.md)).
- **Microservices Patterns**: rechaza XA/2PC porque reduce la disponibilidad y choca con el teorema CAP, y propone sagas como alternativa ([microservices-patterns/cap04-managing-transactions-with-sagas.md](microservices-patterns/cap04-managing-transactions-with-sagas.md)).

Ambos coinciden en que el 2PC/XA es bloqueante y problemático; DDIA lo analiza como mecanismo de consenso en sistemas de datos, mientras Microservices Patterns lo descarta en favor de sagas con transacciones locales y compensaciones.

## Event sourcing y change data capture

- **DDIA**: contrasta el event sourcing (captura explícita del changelog como secuencia de eventos) con el CDC (captura implícita del changelog de una base de datos) para mantener sistemas derivados ([designing-data-intensive-applications/cap11-stream-processing.md](designing-data-intensive-applications/cap11-stream-processing.md)).
- **Microservices Patterns**: persiste cada agregado como una secuencia de eventos de dominio y reconstruye el estado reproduciéndolos (fold/replay), con un event store ([microservices-patterns/cap06-developing-business-logic-with-event-sourcing.md](microservices-patterns/cap06-developing-business-logic-with-event-sourcing.md)).

Los dos tratan el event sourcing como persistencia basada en un log de eventos; DDIA lo sitúa en el procesamiento de flujos y la integración de datos, y Microservices Patterns en la lógica de negocio de un servicio.

## CQRS y datos derivados

- **DDIA**: plantea el write path / read path y las vistas materializadas como frontera desplazable que caches e índices mueven, extensible hasta el cliente ([designing-data-intensive-applications/cap12-the-future-of-data-systems.md](designing-data-intensive-applications/cap12-the-future-of-data-systems.md)).
- **Microservices Patterns**: CQRS separa el lado de comando (publica eventos) del lado de consulta (vistas de solo lectura mantenidas suscribiéndose a esos eventos) ([microservices-patterns/cap07-implementing-queries-in-a-microservice-architecture.md](microservices-patterns/cap07-implementing-queries-in-a-microservice-architecture.md)).

Ambos construyen vistas de lectura derivadas de un flujo de eventos; DDIA lo generaliza como dataflow y vistas materializadas, y Microservices Patterns lo concreta en el patrón CQRS para consultas sobre datos repartidos entre servicios.

## Teorema CAP

- **DDIA**: considera el CAP de valor histórico: ante una partición hay que elegir entre consistencia (linealizabilidad) o disponibilidad ([designing-data-intensive-applications/cap09-consistency-and-consensus.md](designing-data-intensive-applications/cap09-consistency-and-consensus.md)).
- **Microservices Patterns**: invoca el teorema CAP para justificar que XA/2PC reduce la disponibilidad y no encaja en microservicios ([microservices-patterns/cap04-managing-transactions-with-sagas.md](microservices-patterns/cap04-managing-transactions-with-sagas.md)).
- **Release It!**: señala que ZooKeeper (CP) y Consul (AP) están sujetos al teorema CAP al elegir una herramienta de service discovery ([release-it/cap09-interconnect.md](release-it/cap09-interconnect.md)).

Los tres usan el CAP como marco de decisión entre consistencia y disponibilidad ante particiones; DDIA lo analiza a fondo, mientras Microservices Patterns y Release It! lo aplican para justificar decisiones concretas de arquitectura.

## Reemplazar condicionales por polimorfismo (State/Strategy)

- **Refactoring**: Replace Conditional with Polymorphism elimina `switch`/`if` sobre tipos, y usa el patrón State/Strategy cuando el tipo afecta al comportamiento ([refactoring/cap09-simplifying-conditional-expressions.md](refactoring/cap09-simplifying-conditional-expressions.md)).
- **Dive Into Design Patterns**: State permite a un objeto alterar su comportamiento al cambiar su estado interno, y Strategy define una familia de algoritmos intercambiables en clases separadas ([design-patterns/cap32-state.md](design-patterns/cap32-state.md)).
- **Clean Code**: menciona el patrón TEMPLATE METHOD para eliminar duplicación de alto nivel dejando que las subclases rellenen lo que varía ([clean-code/cap12-emergence.md](clean-code/cap12-emergence.md)).

Refactoring y Design Patterns coinciden en sustituir lógica condicional por polimorfismo con State/Strategy; Refactoring lo plantea como transformación de código y Design Patterns como solución estructural, mientras Clean Code recurre a un patrón de comportamiento afín para eliminar duplicación.

## Patrón Observer y separación de dominio y presentación

- **Dive Into Design Patterns**: Observer define un mecanismo de suscripción para notificar a varios objetos de los eventos de otro ([design-patterns/cap31-observer.md](design-patterns/cap31-observer.md)).
- **Refactoring**: Duplicate Observed Data separa la lógica de negocio de la GUI duplicando datos mediante el patrón observer ([refactoring/cap08-organizing-data.md](refactoring/cap08-organizing-data.md)).

Ambos usan el patrón observer para desacoplar emisor y observadores; Design Patterns lo expone como patrón general y Refactoring lo aplica a la separación concreta entre modelo y presentación.

## Composición frente a herencia

- **Dive Into Design Patterns**: favorece la composición ("tiene un") sobre la herencia ("es un") para evitar acoplamiento y explosión de clases ([design-patterns/cap08-favorece-la-composicion-sobre-la-herencia.md](design-patterns/cap08-favorece-la-composicion-sobre-la-herencia.md)).
- **Refactoring**: Replace Inheritance with Delegation cambia herencia por delegación cuando la herencia modela mal ([refactoring/cap11-dealing-with-generalization.md](refactoring/cap11-dealing-with-generalization.md)).

Los dos prefieren la delegación/composición cuando la herencia es rígida o inapropiada; Design Patterns lo formula como principio de diseño y Refactoring como refactorización mecánica para deshacer una herencia mal elegida.

## Ocultamiento de datos y encapsulación

- **Clean Code**: distingue objetos que ocultan datos tras abstracciones de estructuras de datos que los exponen, y critica getters/setters que rompen la abstracción ([clean-code/cap06-objects-and-data-structures.md](clean-code/cap06-objects-and-data-structures.md)).
- **Dive Into Design Patterns**: la encapsulación es un pilar de la POO que oculta estado y comportamiento internos, exponiendo solo una interfaz limitada ([design-patterns/cap02-los-pilares-de-la-poo.md](design-patterns/cap02-los-pilares-de-la-poo.md)).
- **Refactoring**: Encapsulate Field oculta un campo tras accesores para reducir el acoplamiento, y Self Encapsulate Field accede al campo propio vía accesores ([refactoring/cap08-organizing-data.md](refactoring/cap08-organizing-data.md)).

Los tres defienden ocultar el estado interno tras una interfaz; Design Patterns lo trata como pilar conceptual, Clean Code como criterio de diseño de objetos y Refactoring como transformación concreta de campos.

## Arquitectura de microservicios y descomposición

- **Microservices Patterns**: descompone funcionalmente la aplicación en servicios desplegables de forma independiente, cada uno con su propia base de datos, organizados en torno a business capabilities ([microservices-patterns/cap02-decomposition-strategies.md](microservices-patterns/cap02-decomposition-strategies.md)).
- **Development of Microservices Using NestJS**: refactoriza aplicaciones monolíticas en servicios independientes y autónomos, no atados a una tecnología concreta ([microservices-using-nestjs/cap00-development-of-microservices-using-nestjs.md](microservices-using-nestjs/cap00-development-of-microservices-using-nestjs.md)).

Ambos parten del monolito y proponen servicios autónomos y desplegables por separado; Microservices Patterns ofrece un lenguaje de patrones exhaustivo, mientras NestJS lo presenta de forma compacta ligado a un framework concreto.

## Despliegue sin downtime y rolling upgrades

- **Release It!**: trata el despliegue como una feature del software con zero downtime como objetivo, mediante Blue/Green Deploy y Canary Deployment ([release-it/cap13-design-for-deployment.md](release-it/cap13-design-for-deployment.md)).
- **Microservices Patterns**: Kubernetes mantiene el número deseado de instancias sanas y permite rolling upgrades y rollbacks sin downtime con readinessProbe y livenessProbe ([microservices-patterns/cap12-deploying-microservices.md](microservices-patterns/cap12-deploying-microservices.md)).
- **DDIA**: el rolling upgrade actualiza por nodos y obliga a la coexistencia de versiones viejas y nuevas, exigiendo compatibilidad backward/forward ([designing-data-intensive-applications/cap04-encoding-and-evolution.md](designing-data-intensive-applications/cap04-encoding-and-evolution.md)).

Los tres buscan actualizar sin interrumpir el servicio; Release It! y Microservices Patterns se centran en estrategias de despliegue (blue/green, canary, orquestación), y DDIA en la compatibilidad de datos que exige la coexistencia de versiones.

## Compatibilidad de versiones y evolución de API

- **DDIA**: la compatibilidad backward/forward permite que versiones viejas y nuevas coexistan durante los rolling upgrades, con field tags que no deben cambiarse en Thrift/Protocol Buffers ([designing-data-intensive-applications/cap04-encoding-and-evolution.md](designing-data-intensive-applications/cap04-encoding-and-evolution.md)).
- **Release It!**: versiona APIs según el principio de robustez de Postel y las pruebas de contrato, entendiendo una API como pila de acuerdos cuya ruptura unilateral es un cambio rompedor ([release-it/cap14-handling-versions.md](release-it/cap14-handling-versions.md)).
- **Microservices Patterns**: usa Semantic Versioning para gestionar la evolución de la API entre servicios ([microservices-patterns/cap03-interprocess-communication-in-a-microservice-architecture.md](microservices-patterns/cap03-interprocess-communication-in-a-microservice-architecture.md)).

Los tres abordan cómo evolucionar una interfaz sin romper a los consumidores; DDIA desde la codificación de datos, Release It! desde los acuerdos y pruebas de contrato y Microservices Patterns desde el versionado semántico de la API.

## Circuit Breaker y estabilidad ante fallos en cascada

- **Release It!**: el Circuit Breaker, con estados closed/open/half-open, es el patrón fundamental ante problemas de integration points para evitar cascadas de fallos ([release-it/cap05-stability-patterns.md](release-it/cap05-stability-patterns.md)).
- **Microservices Patterns**: el Circuit Breaker evita cascadas de fallos en clientes síncronos y se aplica en el API gateway ante servicios lentos o caídos ([microservices-patterns/cap03-interprocess-communication-in-a-microservice-architecture.md](microservices-patterns/cap03-interprocess-communication-in-a-microservice-architecture.md)).

Ambos adoptan el mismo patrón para impedir que el fallo de una dependencia se propague; Release It! lo define en profundidad como patrón de estabilidad y Microservices Patterns lo aplica a la comunicación entre servicios y al API gateway.

## Inyección de dependencias e inversión de la dependencia

- **Clean Code**: la Dependency Injection aplica IoC a las dependencias dejando a la clase pasiva mientras el contenedor instancia y cablea, siendo Spring el contenedor DI más conocido en Java ([clean-code/cap11-systems.md](clean-code/cap11-systems.md)).
- **Dive Into Design Patterns**: el principio de inversión de la dependencia hace que alto y bajo nivel dependan de abstracciones, no de detalles ([design-patterns/cap13-d-principio-de-inversion-de-la-dependencia.md](design-patterns/cap13-d-principio-de-inversion-de-la-dependencia.md)).
- **Development of Microservices Using NestJS**: la inyección de dependencias usa un contenedor integrado que gestiona automáticamente las dependencias de las clases, promoviendo modularidad y testabilidad ([microservices-using-nestjs/cap00-development-of-microservices-using-nestjs.md](microservices-using-nestjs/cap00-development-of-microservices-using-nestjs.md)).

Los tres separan la construcción del uso delegando el cableado de dependencias; Design Patterns enuncia el principio (DIP), mientras Clean Code y NestJS describen el mecanismo de DI con un contenedor concreto (Spring, NestJS).

## Descubrimiento de servicios

- **Release It!**: el service discovery es otro servicio que puede fallar; conviene cachear resultados y saber si la herramienta es CP (ZooKeeper) o AP (Consul) ([release-it/cap09-interconnect.md](release-it/cap09-interconnect.md)).
- **Microservices Patterns**: combina mecanismos de service discovery a nivel de aplicación (Client-side discovery con Self registration) o de plataforma (Server-side discovery con 3rd party registration) ([microservices-patterns/cap03-interprocess-communication-in-a-microservice-architecture.md](microservices-patterns/cap03-interprocess-communication-in-a-microservice-architecture.md)).

Ambos tratan cómo localizar instancias de servicio en un entorno dinámico; Release It! advierte de su fragilidad y del compromiso CAP de la herramienta, y Microservices Patterns cataloga los patrones de registro y descubrimiento.

## Chaos engineering y tolerancia a fallos

- **Release It!**: el chaos engineering experimenta sobre un sistema distribuido en producción para construir confianza en su resistencia, con herramientas como Chaos Monkey que matan instancias ([release-it/cap17-chaos-engineering.md](release-it/cap17-chaos-engineering.md)).
- **DDIA**: cita Chaos Monkey como práctica de provocar faults adrede para comprobar que no se conviertan en failures ([designing-data-intensive-applications/cap01-reliable-scalable-and-maintainable-applications.md](designing-data-intensive-applications/cap01-reliable-scalable-and-maintainable-applications.md)).

Ambos defienden inducir fallos deliberadamente para validar la resiliencia; Release It! lo desarrolla como disciplina completa y DDIA lo menciona como técnica dentro de la fiabilidad del sistema.

## Seguridad: inyección, XSS y gestión de secretos

- **Release It!**: integra la seguridad desde el diseño cubriendo inyección (SQL/XXE), XSS, mínimo privilegio y gestión de secretos, abandonando la defensa perimetral tipo "pie crust" ([release-it/cap11-security.md](release-it/cap11-security.md)).
- **Microservices Patterns**: aplica seguridad con OAuth 2.0 y JWT en el API gateway y guarda los secretos de configuración en un Vault ([microservices-patterns/cap11-developing-production-ready-services.md](microservices-patterns/cap11-developing-production-ready-services.md)).

Ambos tratan la seguridad como preocupación de primera clase en producción; Release It! enfatiza vulnerabilidades de código y principios defensivos, y Microservices Patterns la autenticación centralizada y el almacenamiento de secretos en una arquitectura distribuida.

## Criptografía y protección de claves

- **Acquiring Card Payments**: detalla cifrados simétricos (DES, 3-DES, AES), MAC/CBC-MAC y la protección de todas las claves en un HSM bajo la LMK ([acquiring-card-payment/cap12-cryptography-101.md](acquiring-card-payment/cap12-cryptography-101.md)).
- **Release It!**: exige cifrar en tránsito incluso dentro de la organización y gestionar secretos sin confiar en la IP de origen ([release-it/cap11-security.md](release-it/cap11-security.md)).

Ambos usan la criptografía para proteger datos sensibles; Acquiring Card Payments entra en los algoritmos y la gestión de claves hardware del dominio de pagos, mientras Release It! la plantea como práctica de seguridad general en producción.

## Temas exclusivos de cada libro

- **Designing Data-Intensive Applications**: replicación (single-leader, multi-leader, leaderless), particionamiento/sharding, niveles de aislamiento y serializabilidad, consenso (Raft, difusión de orden total), relojes y linealizabilidad, procesamiento por lotes (MapReduce) y de flujos, almacenamiento (LSM-trees, B-trees, columnar).
- **Microservices Patterns**: sagas (coreografía/orquestación) y contramedidas, API composition, API gateway y Backends for frontends, consumer-driven contract testing, microservice chassis, patrones de despliegue (serverless, contenedores), aggregates DDD y event storming.
- **Release It!**: antipatrones de estabilidad (Integration Points, Cascading Failures, Blocked Threads, Dogpile), patrones Bulkhead/Steady State/Fail Fast/Handshaking, Recovery-Oriented Computing, control plane, OODA/PDCA, Real-User Monitoring, sesiones frente a usuarios concurrentes.
- **Clean Code**: nombres significativos, funciones pequeñas a un único nivel de abstracción, comentarios como mal necesario, formato, límites (boundaries) y learning tests, catálogo de code smells y heurísticas, casos de estudio (Args, JUnit, SerialDate).
- **Refactoring**: catálogo de refactorizaciones con mecánica (Extract Method, Move Method, Extract/Inline Class, etc.), malos olores del código, grandes refactorizaciones, los dos sombreros y la regla de tres, herramientas de refactorización automatizada.
- **Dive Into Design Patterns**: catálogo completo de patrones GoF (creacionales, estructurales y de comportamiento), pilares de la POO, relaciones entre objetos (dependencia, asociación, agregación, composición), Double Dispatch en Visitor.
- **Acquiring Card Payments**: ecosistema de pagos (modelos three-party/four-party), flujo de transacción e ISO 8583, EMV de contacto y contactless (APDU, criptogramas, Kernels), entorno CNP (3D Secure, AVS, tokenización), disputas y liability shifts, estándares PCI (DSS/PA DSS/PTS), algoritmos de validación (Luhn, LRC, KCV), tablas de códigos y formatos de bloque de PIN.
- **Development of Microservices Using NestJS**: NestJS y sus elementos (módulos, controladores, servicios), decoradores de TypeScript, @MessagePattern/@EventPattern, Docker, Docker Compose y Docker Hub para el despliegue en contenedores.
- **Code Simplicity**: el software como ciencia con leyes fundamentales, Propósito del Software (ayudar a las personas), Ecuación del Diseño de Software, Ley del Cambio, Ley de la Probabilidad de Defectos, deseabilidad de un cambio (valor/esfuerzo), optimización prematura y YAGNI.
