# Systems (Sistemas) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la idea rectora del capítulo sobre sistemas limpios? / R: Separar la construcción de un sistema (arranque, instanciación y cableado de dependencias) de su uso en runtime; mezclarlas rompe la modularidad, dispersa la estrategia de setup y viola el Single Responsibility Principle.

P: ¿Qué analogía usa el capítulo para explicar la separación de concerns a nivel de sistema? / R: La de una ciudad: nadie gestiona todos los detalles, así que se delega en componentes que trabajan sin entender el panorama completo.

P: ¿Qué problema introduce el idiom de LAZY INITIALIZATION/EVALUATION? / R: Crea una dependencia fija de la implementación concreta, complica el testing, mezcla construcción con runtime y asume que ese objeto es el correcto en todo contexto; al repetirse mucho dispersa la estrategia de setup con duplicación.

P: ¿En qué consiste la separación mediante `main`? / R: Mover toda la construcción a `main` o a módulos llamados por `main`; `main` construye y cablea los objetos y los pasa a la aplicación, que solo los usa. Todas las dependencias apuntan lejos de `main`.

P: ¿Para qué sirve el patrón ABSTRACT FACTORY en este contexto? / R: Da a la aplicación control sobre el momento en que se crean los objetos, manteniendo los detalles de cómo construirlos del lado de `main`; las dependencias siguen apuntando desde `main` hacia la aplicación.

P: ¿Qué es la Dependency Injection (DI)? / R: La aplicación de Inversion of Control (IoC) a la gestión de dependencias: un objeto no instancia sus propias dependencias, sino que delega esa responsabilidad en un mecanismo autoritativo (normalmente `main` o un contenedor), apoyando el SRP.

P: ¿Por qué las búsquedas JNDI son una implementación "parcial" de DI? / R: Porque el objeto invocador sigue resolviendo activamente la dependencia; en la DI verdadera la clase es completamente pasiva y ofrece setters o argumentos de constructor por los que se inyectan las dependencias.

P: ¿Pueden las arquitecturas de software crecer de forma incremental? / R: Sí; a diferencia de los sistemas físicos, pueden crecer incrementalmente si se mantiene la separación de concerns. Es un mito hacer el sistema "bien a la primera".

P: ¿Qué son los cross-cutting concerns? / R: Concerns como persistencia, seguridad o transacciones que atraviesan las fronteras naturales de los objetos del dominio, obligando a esparcir el mismo código por muchos objetos.

P: ¿Qué es AOP y qué son los aspects? / R: La programación orientada a aspectos es un enfoque general para restaurar la modularidad; los aspects son construcciones modulares que especifican, de forma declarativa o programática, qué puntos del sistema deben cambiar su comportamiento de forma consistente y no invasiva.

P: ¿Qué limitaciones tienen los dynamic proxies del JDK? / R: Solo funcionan con interfaces (para proxiar clases se usan CGLIB, ASM o Javassist), su código es voluminoso y complejo, y no ofrecen un mecanismo para especificar puntos de ejecución a nivel de sistema.

P: ¿Cómo ve Spring un "bean" respecto a los decoradores? / R: Como una muñeca rusa de DECORATOR anidados: el cliente cree llamar a un método sobre un `Bank`, pero habla con el decorador más externo; con pocas líneas de Spring la aplicación queda casi desacoplada del framework.

P: ¿Qué cobertura dan Spring AOP/JBoss AOP frente a AspectJ? / R: Spring AOP y JBoss AOP (Java puro) bastan para el 80–90 % de los casos; AspectJ es la herramienta más completa, con soporte de "primera clase" para aspectos, a costa de nuevas herramientas e idioms.

P: ¿Por qué el capítulo rechaza el Big Design Up Front (BDUF)? / R: Porque es dañino: inhibe la adaptación al cambio. En software el cambio radical es económicamente factible si la estructura separa bien sus concerns, a diferencia de un edificio físico ya empezado.

P: ¿Qué aporta un buen Domain-Specific Language (DSL)? / R: Minimiza la brecha de comunicación entre el concepto de dominio y el código, reduciendo el riesgo de traducir mal el dominio, y eleva el nivel de abstracción por encima de los idioms y patrones, expresando todo como POJOs.

## Preguntas de autoevaluación

P: ¿Por qué mezclar la construcción de objetos con su uso viola el Single Responsibility Principle? / R: Porque el arranque (instanciar y cablear dependencias) es un concern distinto de la lógica de ejecución; combinarlos hace que un mismo módulo cargue con dos responsabilidades y dispersa la estrategia de setup por toda la aplicación. (Sección "Separar la construcción del sistema de su uso")

P: En la separación por `main`, ¿en qué dirección apuntan las dependencias y por qué importa? / R: Todas las flechas de dependencia cruzan la barrera en una sola dirección, apuntando lejos de `main`; así la aplicación no conoce `main` ni el proceso de construcción y asume que los objetos ya están construidos y cableados. (Sección "Separación de main")

P: ¿Qué hace invasivas y difíciles de testear a las arquitecturas EJB1/EJB2? / R: El Entity Bean obligaba a definir interfaces local/remota, descriptores XML y numerosos métodos de ciclo de vida; la lógica de negocio quedaba fuertemente acoplada al contenedor pesado, dificultando el unit testing aislado, impidiendo el reuso y minando la POO. (Secciones "Escalar hacia arriba" y "Cross-cutting concerns")

P: ¿Cómo logran los frameworks AOP en Java puro desacoplar la lógica de dominio de la infraestructura? / R: Escribiendo la lógica de negocio como POJOs centrados en su dominio, sin dependencias de frameworks empresariales, e incorporando la infraestructura (persistencia, transacciones, seguridad, caching, failover) mediante configuración declarativa que alimenta el contenedor DI. (Sección "Frameworks AOP en Java puro")

P: ¿Qué significa "test drive" la arquitectura del sistema y qué lo hace posible? / R: Significa evolucionar la arquitectura de simple a sofisticada adoptando tecnologías bajo demanda, sin BDUF; lo hace posible escribir la lógica de dominio como POJOs desacoplados de los concerns de arquitectura a nivel de código. (Sección "Probar (test drive) la arquitectura del sistema")

P: ¿Por qué conviene posponer las decisiones hasta el último momento posible? / R: Porque una decisión prematura se toma con conocimiento subóptimo; posponerla permite decidir con la mejor información disponible, y la agilidad de un sistema POJO con concerns modularizados habilita decisiones óptimas y just-in-time. (Sección "Optimizar la toma de decisiones")

P: ¿Qué riesgo señala el capítulo al adoptar un estándar como EJB2? / R: Que muchos equipos lo usaron solo por ser estándar, cuando diseños más ligeros bastaban, perdiendo el foco en el valor para el cliente; además el proceso de crear estándares puede ser lento y perder contacto con las necesidades reales de los adoptantes. (Sección "Usar estándares con sabiduría...")

## Puntos a dominar

- Explicar por qué separar construcción y uso preserva modularidad y SRP, y reconocer el problema del idiom LAZY INITIALIZATION.
- Distinguir las tres estrategias de arranque: construcción en `main`, ABSTRACT FACTORY y Dependency Injection (DI como IoC aplicada a dependencias).
- Diferenciar una implementación parcial de DI (JNDI, objeto activo) de la DI verdadera (clase pasiva con setters/constructor y contenedor que cablea).
- Argumentar que las arquitecturas de software crecen de forma incremental con buena separación de concerns y por qué el BDUF es dañino.
- Identificar los cross-cutting concerns y los enfoques tipo aspecto (AOP) para tratarlos de forma no invasiva.
- Comparar proxies JDK, Spring AOP/JBoss AOP y AspectJ en cobertura, complejidad y coste de adopción.
- Justificar escribir la lógica de dominio como POJOs testeables, usar estándares solo con valor demostrable, posponer decisiones y apoyarse en DSLs. Usa siempre lo más simple que pueda funcionar.
