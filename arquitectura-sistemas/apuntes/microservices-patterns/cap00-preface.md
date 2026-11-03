# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Prólogo — preface (prefacio)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El prefacio narra, en primera persona, cómo el autor descubrió la arquitectura de microservicios y por qué escribió este libro. Richardson arranca con una cita de William Gibson —"el futuro ya está aquí, solo que no está repartido de forma uniforme" (PDF p. 19)— para ilustrar que las ideas y tecnologías tardan en difundirse y adoptarse ampliamente en una comunidad. Su propio camino hacia los microservicios es un ejemplo de esa difusión lenta.

La tesis que anticipa el libro es que la arquitectura de microservicios reemplaza el monolito por una colección de servicios poco acoplados, desarrollados y desplegados por equipos pequeños, para acelerar y hacer más fiable la entrega de software. El prefacio también deja claro el enfoque de la obra: no es un "manifiesto" de microservicios, sino un libro organizado en torno a patrones, soluciones reutilizables que describen tanto beneficios como inconvenientes.

Al terminar este prefacio sabes de dónde viene el término, qué problema resuelve el enfoque frente al monolito tradicional y qué promete abordar el libro: entender la arquitectura, sus ventajas y desventajas, cuándo usarla, cómo resolver los retos de diseño (incluida la gestión de datos distribuidos) y cómo refactorizar un monolito.

## El origen de los microservicios según el autor

Richardson relata una cronología personal que sirve de hilo conductor:

- 2006: inspirado por una charla de un evangelista de AWS, crea el Cloud Foundry original (sin relación con el actual salvo el nombre), un Platform-as-a-Service (PaaS) para automatizar el despliegue de aplicaciones Java en EC2.
- Ese Cloud Foundry tenía arquitectura monolítica: un único archivo Java WAR (Web Application Archive).
- Reconoce los problemas del monolito: no se podía cambiar la UI sin probar y redesplegar toda la aplicación, y como el componente de monitorización y gestión dependía de un motor de Complex Event Processing (CEP) con estado en memoria, no podían ejecutar varias instancias de la aplicación.
- 2002 (contexto externo que cita): Amazon ya había empezado a migrar fuera del monolito hacia servicios poco acoplados, propiedad de "two-pizza teams" (equipos tan pequeños que se alimentan con dos pizzas). Según cita el autor, Amazon llega a desplegar cambios en producción cada 11,6 segundos.
- Inicios de 2010: lee *The Art of Scalability* (Addison-Wesley Professional, 2009), de Michael T. Fisher y Martin L. Abbott. De ahí toma el "scale cube", un modelo tridimensional de escalado cuya escala en el eje Y descompone funcionalmente una aplicación en servicios. Fue su momento "a-ha": podía haber resuelto los retos de Cloud Foundry años antes.
- Abril de 2012: da su primera charla sobre el enfoque, "Decomposing Applications for Deployability and Scalability". Aún no existía un término aceptado; a veces lo llamaba arquitectura modular y políglota, porque los servicios podían escribirse en distintos lenguajes.
- El término "microservice" se había usado en un taller de arquitectura de software en 2011. Richardson lo encuentra por primera vez en una charla de Fred George en Oredev 2013, y le gustó.
- Enero de 2014: crea el sitio https://microservices.io para documentar patrones de arquitectura y diseño.
- Marzo de 2014: James Lewis y Martin Fowler publican su entrada de blog sobre microservicios, que populariza el término y hace que la comunidad se consolide en torno al concepto.

## La realidad actual frente a la visión

El autor contrasta la visión de equipos pequeños y poco acoplados entregando microservicios con la realidad diaria del lector: hoy las aplicaciones empresariales críticas suelen ser grandes monolitos desarrollados por equipos grandes, con lanzamientos infrecuentes y dolorosos, y un área de IT que lucha por seguir el ritmo del negocio. De ahí la pregunta que motiva el libro: cómo adoptar la arquitectura de microservicios.

## El objetivo del libro

El libro busca responder a esa pregunta. Promete:

- Dar una buena comprensión de la arquitectura de microservicios, sus beneficios, inconvenientes y cuándo usarla.
- Describir cómo resolver los numerosos retos de diseño, incluida la gestión de datos distribuidos.
- Cubrir cómo refactorizar una aplicación monolítica hacia una arquitectura de microservicios.

En lugar de ser un manifiesto, se organiza en torno a patrones. Un patrón es "una solución reutilizable a un problema que ocurre en un contexto particular" (PDF p. 21); su valor está en describir también los inconvenientes y los asuntos que hay que resolver para implementar la solución con éxito. Para el autor, esa objetividad al pensar las soluciones conduce a mejores decisiones.

## Ideas clave

- La cita de Gibson enmarca el prefacio: las buenas ideas, como los microservicios, se difunden lentamente por la comunidad.
- El monolito (un único WAR en el caso de Cloud Foundry) genera problemas de desarrollo y operación: no se puede cambiar una parte sin redesplegar todo, y el estado en memoria impide escalar con varias instancias.
- La alternativa es descomponer la aplicación en servicios poco acoplados, propiedad de equipos pequeños ("two-pizza teams"), como hicieron Amazon y eBay.
- El "scale cube" de *The Art of Scalability* y su escala en el eje Y (descomposición funcional en servicios) fue la clave conceptual para el autor.
- El término "microservices" se consolidó tras el blog de James Lewis y Martin Fowler (2014); el autor documenta patrones en microservices.io desde enero de 2014.
- El libro no es un manifiesto: se estructura en patrones, soluciones reutilizables que exponen beneficios y también inconvenientes.
- Objetivo del libro: entender la arquitectura, decidir cuándo aplicarla, resolver retos de diseño (datos distribuidos incluidos) y refactorizar monolitos.
