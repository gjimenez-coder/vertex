# Prólogo — preface (prefacio) — Estudio

## Tarjetas de repaso

P: ¿Qué cita de William Gibson enmarca el prefacio y qué ilustra? / R: "El futuro ya está aquí, solo que no está repartido de forma uniforme"; ilustra que las ideas y tecnologías tardan en difundirse y adoptarse ampliamente en una comunidad.

P: ¿Qué reemplaza la arquitectura de microservicios según la tesis del libro? / R: Reemplaza el monolito por una colección de servicios poco acoplados, desarrollados y desplegados por equipos pequeños, para acelerar y hacer más fiable la entrega de software.

P: ¿Qué es el Cloud Foundry original que creó Richardson en 2006? / R: Un Platform-as-a-Service (PaaS) para automatizar el despliegue de aplicaciones Java en EC2, sin relación con el actual salvo el nombre.

P: ¿Qué arquitectura tenía ese Cloud Foundry original? / R: Monolítica: un único archivo Java WAR (Web Application Archive).

P: ¿Qué dos problemas del monolito reconoce el autor en Cloud Foundry? / R: No se podía cambiar la UI sin probar y redesplegar toda la aplicación; y el estado en memoria de un motor CEP impedía ejecutar varias instancias.

P: ¿Qué son los "two-pizza teams" y de dónde viene el ejemplo? / R: Equipos tan pequeños que se alimentan con dos pizzas, dueños de servicios poco acoplados; viene de Amazon, que desde 2002 migraba fuera del monolito.

P: ¿Cada cuánto llega a desplegar Amazon cambios en producción según cita el autor? / R: Cada 11,6 segundos.

P: ¿Qué es el "scale cube" y de qué libro lo toma el autor? / R: Un modelo tridimensional de escalado de *The Art of Scalability* (Fisher y Abbott); su escala en el eje Y descompone funcionalmente una aplicación en servicios.

P: ¿Cuándo dio Richardson su primera charla sobre el enfoque y cómo se titulaba? / R: En abril de 2012, "Decomposing Applications for Deployability and Scalability".

P: ¿Dónde encontró el autor por primera vez el término "microservice"? / R: En una charla de Fred George en Oredev 2013 (el término ya se había usado en un taller de arquitectura de software en 2011).

P: ¿Qué publicación popularizó el término "microservices" y cuándo? / R: La entrada de blog de James Lewis y Martin Fowler en marzo de 2014.

P: ¿Qué sitio creó el autor en enero de 2014 y para qué? / R: https://microservices.io, para documentar patrones de arquitectura y diseño.

P: ¿Cómo define el libro un patrón? / R: "Una solución reutilizable a un problema que ocurre en un contexto particular", cuyo valor incluye describir inconvenientes y asuntos a resolver.

P: ¿Cuáles son los tres objetivos que promete el libro? / R: Comprender la arquitectura (beneficios, inconvenientes y cuándo usarla); resolver retos de diseño incluida la gestión de datos distribuidos; y refactorizar un monolito hacia microservicios.

## Preguntas de autoevaluación

1. ¿Por qué Richardson insiste en que este libro no es un "manifiesto" de microservicios? / R: Porque se organiza en torno a patrones, soluciones reutilizables que describen tanto beneficios como inconvenientes, buscando objetividad para tomar mejores decisiones. (Sección: El objetivo del libro / Lo que necesitas saber)

2. ¿Qué momento "a-ha" tuvo el autor y qué le reveló? / R: Leer *The Art of Scalability* a inicios de 2010 y descubrir el "scale cube"; comprendió que la escala del eje Y (descomposición funcional en servicios) podía haber resuelto los retos de Cloud Foundry años antes. (Sección: El origen de los microservicios según el autor)

3. ¿Cómo contrasta el autor la visión de los microservicios con la realidad actual del lector? / R: La visión es de equipos pequeños y poco acoplados entregando microservicios; la realidad son grandes monolitos de equipos grandes, con lanzamientos infrecuentes y dolorosos y un IT que no sigue el ritmo del negocio. (Sección: La realidad actual frente a la visión)

4. ¿Por qué el estado en memoria fue un problema concreto en Cloud Foundry? / R: El componente de monitorización y gestión dependía de un motor de Complex Event Processing (CEP) con estado en memoria, lo que impedía ejecutar varias instancias de la aplicación. (Sección: El origen de los microservicios según el autor)

5. ¿Qué pregunta motiva el libro a partir del contraste visión/realidad? / R: Cómo adoptar la arquitectura de microservicios. (Sección: La realidad actual frente a la visión / El objetivo del libro)

6. ¿Cómo llamaba el autor al enfoque antes de que existiera un término aceptado y por qué? / R: Arquitectura modular y políglota, porque los servicios podían escribirse en distintos lenguajes. (Sección: El origen de los microservicios según el autor)

7. ¿Qué sales sabiendo tras leer el prefacio? / R: De dónde viene el término, qué problema resuelve el enfoque frente al monolito tradicional y qué promete abordar el libro (entender la arquitectura, cuándo usarla, resolver retos de diseño incluida la gestión de datos distribuidos y refactorizar un monolito). (Sección: Lo que necesitas saber)

## Puntos a dominar

- La cita de Gibson como marco: las buenas ideas (microservicios) se difunden lentamente.
- Los problemas del monolito ilustrados con Cloud Foundry: redespliegue total y estado en memoria que impide escalar.
- La alternativa: servicios poco acoplados en manos de "two-pizza teams" (Amazon, eBay).
- El "scale cube" y la descomposición funcional del eje Y como clave conceptual.
- La cronología del término: taller 2011, Fred George (Oredev 2013), microservices.io (enero 2014), blog de Lewis y Fowler (marzo 2014).
- La definición de patrón y por qué el libro se estructura en patrones en vez de ser un manifiesto.
- Los tres objetivos del libro: comprender, resolver retos de diseño y refactorizar.
