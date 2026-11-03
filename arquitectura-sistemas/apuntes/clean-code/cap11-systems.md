# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 11 — Systems (Sistemas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo (escrito por Kevin Dean Wampler) sube el foco de la limpieza del código desde los niveles bajos de abstracción al nivel del sistema. La tesis central es que un sistema limpio mantiene la misma separación de concerns, abstracción y modularidad que hace funcionar a una ciudad: nadie puede gestionar todos los detalles, así que se delega en componentes que trabajan sin entender el panorama completo.

La idea rectora es separar la construcción de un sistema de su uso. El arranque —cuando se instancian los objetos y se "cablean" sus dependencias— es un concern distinto de la lógica de ejecución que toma el control después. Mezclar ambos rompe la modularidad, dispersa la estrategia de setup por toda la aplicación y viola el Single Responsibility Principle.

Sales sabiendo cómo separar el arranque (mediante `main`, factorías o inyección de dependencias), cómo las arquitecturas pueden crecer de forma incremental si se separan bien los concerns, cómo tratar los cross-cutting concerns con enfoques tipo aspecto, y por qué conviene escribir la lógica de dominio como POJOs, usar estándares solo cuando aportan valor demostrable y apoyarse en lenguajes específicos de dominio (DSL).

## El ejemplo que recorre el capítulo

El hilo conductor es un objeto de dominio `Bank` (con dirección y una colección de `Account`), que se reescribe a lo largo del capítulo: primero como Entity Bean de EJB2, luego envuelto con un proxy JDK para persistencia, después configurado con Spring como "muñeca rusa" de decoradores, y finalmente como un EJB3 casi POJO con anotaciones. La evolución ilustra el paso de una arquitectura invasiva y fuertemente acoplada a una limpia y testeable.

## Separar la construcción del sistema de su uso

La construcción es un proceso distinto del uso (como un hotel en obras frente a uno terminado). El sistema debe separar el arranque de la lógica de runtime. El idiom de LAZY INITIALIZATION/EVALUATION ilustra el problema:

```java
public Service getService() {
  if (service == null)
    service = new MyServiceImpl(...);  // ¿default razonable para la mayoría?
  return service;
}
```

Tiene méritos (no se paga el coste de construir hasta usar el objeto, nunca se devuelve null), pero crea una dependencia fija de `MyServiceImpl`, complica el testing (hay que probar todas las rutas y colocar un TEST DOUBLE o MOCK OBJECT), mezcla construcción con runtime y asume que ese objeto es el correcto en todo contexto. Una ocurrencia aislada no es grave, pero suele haber muchas, dispersando la estrategia global de setup con duplicación. Hay que modularizar el proceso de construcción y cableado aparte y tener una estrategia global y consistente para resolver las dependencias principales.

## Separación de main

Una forma es mover toda la construcción a `main` (o a módulos llamados por `main`) y diseñar el resto del sistema asumiendo que todos los objetos ya están construidos y cableados. `main` construye los objetos y los pasa a la aplicación, que solo los usa. Todas las flechas de dependencia cruzan la barrera en una sola dirección, apuntando lejos de `main`: la aplicación no conoce `main` ni el proceso de construcción.

## Factorías

A veces la aplicación necesita controlar cuándo se crea un objeto (p. ej., crear `LineItem` para añadir a un `Order`). El patrón ABSTRACT FACTORY le da a la aplicación control sobre el momento de la construcción, pero mantiene los detalles de cómo construir en la `LineItemFactoryImplementation`, que vive del lado de `main`. Las dependencias siguen apuntando desde `main` hacia la aplicación.

## Inyección de dependencias

La Dependency Injection (DI) es la aplicación de Inversion of Control (IoC) a la gestión de dependencias: un objeto no debe instanciar sus propias dependencias, sino delegar esa responsabilidad en un mecanismo "autoritativo" (normalmente `main` o un contenedor especializado), apoyando el SRP. Las búsquedas JNDI son una implementación "parcial": el objeto invocador sigue resolviendo activamente la dependencia. La DI verdadera va más allá: la clase es completamente pasiva y ofrece setters o argumentos de constructor por los que se inyectan las dependencias; el contenedor DI las instancia (normalmente bajo demanda) y las cablea según un archivo de configuración o un módulo de construcción. Spring es el contenedor DI más conocido en Java. LAZY-INITIALIZATION sigue siendo útil: la mayoría de contenedores no construyen un objeto hasta necesitarlo y ofrecen factorías o proxies para optimizaciones.

## Escalar hacia arriba

Las ciudades crecen desde asentamientos; igual los sistemas. Es un mito que un sistema se pueda hacer "bien a la primera": hay que implementar solo las historias de hoy y luego refactorizar y expandir. A diferencia de los sistemas físicos, las arquitecturas de software pueden crecer de forma incremental si se mantiene la separación de concerns. Las arquitecturas EJB1 y EJB2 son el contraejemplo: el Entity Bean de un `Bank` obligaba a definir interfaces local/remota, descriptores de despliegue XML y numerosos métodos de ciclo de vida. La lógica de negocio quedaba fuertemente acoplada al contenedor pesado, el unit testing aislado era difícil, el reuso prácticamente imposible, y hasta la POO quedaba minada (los beans no heredan entre sí, proliferan los DTO tipo "struct" y el boilerplate).

## Cross-cutting concerns

EJB2 se acercaba a la separación de concerns al declarar transacciones, seguridad y parte de la persistencia en descriptores de despliegue. Concerns como la persistencia atraviesan las fronteras naturales de los objetos del dominio: en la práctica hay que esparcir el mismo código por muchos objetos. A esa intersección fina de dominios se la llama cross-cutting concerns. La forma en que EJB manejaba persistencia, seguridad y transacciones "anticipó" la programación orientada a aspectos (AOP), un enfoque general para restaurar la modularidad. En AOP, construcciones modulares llamadas aspects especifican, de forma declarativa o programática, qué puntos del sistema deben modificar su comportamiento de forma consistente y no invasiva.

## Java Proxies

Los proxies de Java sirven para casos simples (envolver llamadas a métodos). Los dynamic proxies del JDK solo funcionan con interfaces; para proxiar clases hay que usar librerías de manipulación de bytecode (CGLIB, ASM, Javassist). El ejemplo envuelve `Bank` (interfaz) con un `BankProxyHandler` (un `InvocationHandler`) que usa reflexión para mapear invocaciones genéricas a los métodos del POJO `BankImpl`. El volumen y la complejidad del código son dos inconvenientes de los proxies, y además no ofrecen un mecanismo para especificar "puntos" de ejecución a nivel de sistema, necesario para una solución AOP real.

## Frameworks AOP en Java puro

Herramientas como Spring AOP y JBoss AOP automatizan el boilerplate de los proxies para implementar aspectos en Java puro. Escribes la lógica de negocio como POJOs, centrados solo en su dominio y sin dependencias de frameworks empresariales, lo que los hace más simples y fáciles de testear. La infraestructura (persistencia, transacciones, seguridad, caching, failover) se incorpora con configuración declarativa (XML o APIs) que alimenta el contenedor DI. En Spring, cada "bean" es como una muñeca rusa de DECORATOR anidados: el cliente cree llamar a `getAccounts()` sobre un `Bank`, pero habla con el decorador más externo. Con muy pocas líneas de código específico de Spring, la aplicación queda casi del todo desacoplada del framework, eliminando el acoplamiento de sistemas como EJB2. Este modelo motivó el rediseño de EJB3, que soporta cross-cutting concerns de forma declarativa con XML y/o anotaciones de Java 5, produciendo un `Bank` mucho más limpio y casi POJO.

## AspectJ Aspects

AspectJ es la herramienta más completa para separar concerns mediante aspectos: una extensión de Java con soporte de "primera clase" para aspectos como construcciones de modularidad. Spring AOP y JBoss AOP (Java puro) bastan para el 80–90 % de los casos; AspectJ ofrece un conjunto más rico y potente, a costa de adoptar nuevas herramientas y aprender nuevos constructos e idioms. Su "forma anotada" (anotaciones de Java 5) y el soporte de Spring mitigan esa adopción.

## Probar (test drive) la arquitectura del sistema

Si escribes la lógica de dominio como POJOs, desacoplada de los concerns de arquitectura a nivel de código, puedes "test drive" tu arquitectura y evolucionarla de simple a sofisticada adoptando tecnologías bajo demanda. No hace falta Big Design Up Front (BDUF); de hecho el BDUF es dañino porque inhibe la adaptación al cambio. Los arquitectos de edificios deben hacer BDUF porque no es viable cambiar radicalmente una estructura física empezada; en software sí es económicamente factible el cambio radical si la estructura separa bien sus concerns. Esto no significa ir "sin rumbo": hay expectativas de alcance, metas y planificación, pero manteniendo la capacidad de cambiar de rumbo. Un buen API debería desaparecer de la vista la mayor parte del tiempo. En resumen: *"Una arquitectura óptima consiste en dominios de concern modularizados, cada uno implementado con POJOs"* (PDF p. 198), integrados mediante aspectos mínimamente invasivos, y puede ser test-driven como el código.

## Optimizar la toma de decisiones

La modularidad y la separación de concerns hacen posible la gestión y decisión descentralizadas: en un sistema suficientemente grande, nadie puede tomar todas las decisiones. Conviene dar responsabilidades a las personas más cualificadas y posponer las decisiones hasta el último momento posible, para decidir con la mejor información. Una decisión prematura se toma con conocimiento subóptimo. La agilidad de un sistema POJO con concerns modularizados permite decisiones óptimas y just-in-time.

## Usar estándares con sabiduría, cuando aporten valor demostrable

Los estándares facilitan reutilizar ideas y componentes, reclutar gente con experiencia y cablear componentes. Pero muchos equipos usaron EJB2 solo por ser estándar, cuando diseños más ligeros bastaban, y perdieron el foco en el valor para el cliente. El proceso de crear estándares puede ser demasiado lento y algunos pierden contacto con las necesidades reales de sus adoptantes.

## Los sistemas necesitan lenguajes específicos de dominio

Hay interés renovado en los Domain-Specific Languages (DSL): lenguajes de scripting pequeños o APIs en lenguajes estándar que permiten escribir código que se lee como prosa estructurada que escribiría un experto de dominio. Un buen DSL minimiza la brecha de comunicación entre el concepto de dominio y el código que lo implementa, reduciendo el riesgo de traducir mal el dominio. Los DSL elevan el nivel de abstracción por encima de los idioms de código y los patrones de diseño, y permiten expresar todos los niveles de abstracción y dominios como POJOs.

## Ideas clave

- Mantén limpio también el nivel del sistema: separa concerns, abstracción y modularidad igual que hace funcionar a una ciudad.
- Separa la construcción (arranque, instanciación y cableado de dependencias) de la lógica de uso en runtime; mezclarlas rompe la modularidad y el SRP.
- Lleva la construcción a `main` o a módulos llamados por `main`, con dependencias apuntando siempre lejos de la aplicación; usa ABSTRACT FACTORY cuando la app deba controlar cuándo se crean objetos.
- La Dependency Injection (IoC aplicada a dependencias) deja a la clase pasiva: el contenedor instancia y cablea; Spring es el contenedor DI más conocido en Java.
- Las arquitecturas de software pueden crecer de forma incremental si separan bien sus concerns; el BDUF es dañino porque inhibe la adaptación al cambio.
- Trata los cross-cutting concerns (persistencia, seguridad, transacciones) con AOP o mecanismos tipo aspecto, de forma no invasiva; EJB2 era invasivo y acoplado, EJB3 y Spring lo corrigen.
- Escribe la lógica de dominio como POJOs testeables; integra la infraestructura con aspectos mínimamente invasivos, y así podrás test-drive la arquitectura.
- Usa estándares solo cuando añadan valor demostrable, pospón decisiones hasta el último momento razonable y apóyate en DSLs para cerrar la brecha entre dominio y código. Usa siempre lo más simple que pueda funcionar.
