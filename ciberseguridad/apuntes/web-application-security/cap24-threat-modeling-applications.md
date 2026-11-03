# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 24 — Threat Modeling Applications (Modelado de amenazas de aplicaciones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El threat modeling es un método valioso para mejorar la postura de seguridad de una aplicación, pero solo si se implementa correctamente. Una implementación apresurada no hace más que "marcar casillas" y malgastar tiempo. Bien hecho, permite que ingenieros de software y de seguridad trabajen de forma cohesionada, compartiendo un flujo de trabajo que identifica amenazas (vulnerabilidades potenciales), threat actors (atacantes potenciales), mitigaciones existentes (controles de seguridad) y el delta entre amenazas y mitigaciones.

Además de esos beneficios, un buen threat model funciona como documento vivo que traspasa conocimiento de seguridad de un ingeniero a otro, aportando robustez al conocimiento de seguridad de la organización de una forma difícil de lograr con otros métodos.

El capítulo enseña a diseñar un threat model efectivo recorriendo un ejemplo completo (MegaBank). Sales sabiendo las cinco metas de un buen modelo, cómo recopilar diseño lógico y técnico, cómo listar threat actors, cómo derivar attack vectors con severidad, cómo documentar mitigaciones existentes y, finalmente, cómo hacer la identificación del delta para no lanzar hasta cubrir cada vector sin mitigar.

## El ejemplo que recorre el capítulo
Una corporación ficticia, MegaBank, implementa una función "user review" con la que usuarios autenticados reseñan features existentes. Es una función pública (y por tanto susceptible de abuso), así que el equipo de seguridad —representado por Holly Hacker, miembro senior— colabora con los desarrolladores para construir un threat model siguiendo cada fase del proceso.

## Diseñar un threat model efectivo
Un buen modelo debe cumplir una serie de metas; si falta alguna, su impacto es limitado:
- Documentar conocimiento
- Identificar threat actors
- Identificar riesgos (attack vectors)
- Identificar mitigaciones
- Identificar el delta (entre riesgos y mitigaciones)

Cada meta se apoya en las anteriores. Un modelo que solo identifica riesgos sin documentar mitigaciones es poco útil, porque "risks are not actionable until existing mitigations are known" (PDF p. 335). Implementar una mitigación para un riesgo ya mitigado introduce más bugs, deuda técnica e incluso nuevas vulnerabilidades.

## Diseño lógico (Logic Design)
El primer dato que recopila Holly es una descripción de la feature desde la perspectiva de la lógica: qué hace, a un nivel más alto que un documento de arquitectura pero más bajo que una descripción de marketing (el nivel que usaría un diseñador UX).

En MegaBank, la función es pública: un usuario autenticado rellena un formulario web y publica una reseña de cualquier feature existente. El formulario incluye una puntuación entre 0 y 5 y un cuerpo de texto. Al enviarse, el servidor almacena contenido y puntuación en una base de datos, consultable al pulsar "show reviews" en páginas tipo "activate cryptocurrency wallet" o "activate bank loans".

El diseño lógico suele desdeñarse pero es clave para detectar logic vulnerabilities: vulnerabilidades derivadas de que la aplicación no siga la lógica para la que está pensada. Son únicas a cada aplicación y sus requisitos de negocio. Ejemplo: un usuario que publique una puntuación mayor de 5 saltándose el formulario con una petición HTTP personalizada. Guardar un entero no es por sí mismo una vulnerabilidad, pero aquí sí lo es porque sesgaría la agregación/promedio y dañaría la confianza y la reputación de marca de MegaBank.

## Diseño técnico (Technical Design)
Más común que la recopilación de diseño lógico, pero por sí solo no explica los objetivos de negocio; de ahí que ambos sean necesarios. Su meta es permitir identificar amenazas generadas por la arquitectura. Debe ser lo bastante completo para identificar:
- Qué herramientas y tecnologías se usan: lenguajes, bases de datos, build tools, package managers, frameworks.
- Qué servicios de terceros: in-network (p. ej. subrecursos AWS como S3) y out-of-network (p. ej. Datadog, CircleCI).
- Cómo fluyen los datos entre módulos (los data flow diagrams [DFD] ayudan): formatos en tránsito, cifrado en tránsito, protocolos de red.
- Cómo están configuradas las redes (interna/VPN, externa): firewalls, VPNs, redes físicas.
- Qué controles de autenticación y autorización se usan: ¿varios tipos de token?, ¿todos los endpoints hacen las mismas comprobaciones de authorization?
- Cuál es el esquema de base de datos (¿datos regulados?). En NoSQL schemaless, listar todas las formas de datos posibles.

Diseño técnico de MegaBank (resumido): UI React con dos componentes nuevos, `getReviews` y `createReview`, cada uno con entrada en BD y endpoints REST. `getReviews` lanza un HTTP GET contra un servidor REST en AWS EC2 que consulta PostgreSQL por `featureID`; si no hay reseñas devuelve "no reviews found for chosen feature". `createReview` lanza un HTTP POST que primero verifica la sesión contra el servicio de gestión de sesiones y, si pasa, valida que `score` es integer y `review` es texto antes de guardar. Lenguaje JavaScript en cliente y servidor; servidor con ExpressJS usando `body-parser` y `cookie-parser` vía npm, todo en última versión estable, sobre una instancia AWS EC2. Datos cifrados con TLS 1.3 y certificado de Let's Encrypt. Todas las APIs también consultables opcionalmente vía GraphQL.

Con este detalle ya se intuyen vulnerabilidades: no se indica cómo se renderiza el texto (posible vector XSS), ni cómo se genera la consulta SQL (peligroso al almacenar un string del usuario, posible SQL injection), y el mensaje de error de "no reviews" podría provocar information disclosure de features aún no públicas. Conviene anotarlas, aunque lo ideal es esperar a tener todos los datos antes de hacer brainstorming de vulnerabilidades.

## Identificación de amenazas: threat actors
Los threat actors son atacantes arquetípicos, cada uno con rutas únicas de ataque. Hay que considerar niveles de permiso, incluyendo permisos de insiders. Para la feature se identifican (Tabla 24-1):
- User admin: usa la UI de admin para leer/actualizar la BD; podría robar PII o modificar ratings; su uso no se registra bien, sin accountability.
- Customer support user: puede leer datos de la BD pero no actualizar; podría robar PII.
- Review aggregator script: corre periódicamente para promediar puntuaciones; tiene acceso directo como database admin; si se compromete, puede ejecutar cualquier query (potencial de daño significativo).
- Authenticated user: publica reseñas/puntuaciones y lee reseñas públicas; podría enviar payloads maliciosos (SQL injection, desbordar reseñas) saltándose el formulario.
- Unauthenticated (guest) user: solo lee puntuaciones; amenaza baja salvo DoS o consultas de grafo circulares.

Conclusión importante: la lista debe ser exhaustiva e incluir no solo humanos sino usuarios máquina. Es un error común considerar solo ataques humanos directos, y peor aún solo humanos externos. Incluye usuarios internos, externos y máquina, divididos en conjuntos de permisos autenticados y no autenticados. Cada threat actor tiene una attack surface area distinta, útil para rankear riesgos y resolver primero los ataques más graves de los actores más peligrosos.

## Identificación de amenazas: attack vectors
Con los threat actors documentados, se consideran los attack vectors: aún no son vulnerabilidades (el sistema no está desarrollado), sino vías potenciales futuras de ataque. Se obtienen por cross-analysis de tres componentes: logic design, technical design y threat actors. El diseño lógico expone lógica de negocio relevante para evaluar el técnico; los threat actors determinan quién puede o no aprovechar cada vector (algunos requieren acceso privilegiado como VPN interna o credenciales de admin). La tabla incorpora una columna de severidad (Severity) para priorizar. Vectores (Tabla 24-2):
- Improper validation—score — P1 — todos menos guest: falta de validaciones permite POST con score fuera de 0–5, sesgando ratings.
- Information disclosure—FeatureID — P3 — todos: los errores de `getReviews` permiten escanear features no lanzadas o gated.
- SQL injection — P0 — todos menos guest: mala implementación del payload POST puede derivar en SQL injection contra `postReview`.
- GraphQL circular and large queries — P1 — todos: consultas circulares/grandes no posibles en REST, no frenadas por rate limits; requieren tiempos máximos de query.
- GraphQL introspection and errors — P1 — todos: el motor de introspection debe desactivarse o filtrará configuración; los errores internos también filtran info si no se suprimen.
- High privilege user attacks — P0 — admin y review aggregator script: tokens privilegiados leen/actualizan la BD sin monitorización ni accountability; un token comprometido comprometería todo.

Nota: "P" es prioridad; P0–P4 son anotaciones comunes de severidad en la industria, siendo P0 la más alta y P4 la más baja (PDF p. 343). Muchos vectores vienen de actores internos: usuarios internos pueden ser hackeados, volverse rogue o (máquinas) malfuncionar. Hay que modelar el peor caso, no el mejor. No todos los vectores tienen el mismo riesgo, lo que permite priorizar.

## Identificación de mitigaciones
Fase sencilla de recolección de datos: documentar las mitigaciones existentes por cada attack vector (Tabla 24-3):
- Validation logic → Improper validation—score: el motor de validación rechaza scores no enteros o fuera de 0–5, evitando errores de agregación.
- SQL Injection Mitigations → SQL Injection: todas las llamadas SQL usan un DSL propio que fuerza prepared statements.

El resto de ataques anotados no tienen mitigaciones conocidas.

## Identificación del delta
Se cruzan los attack vectors con la lista de mitigaciones y se eliminan los vectores ya suficientemente mitigados. Quedan sin mitigar (Tabla 24-4): Information disclosure—FeatureID (P3), GraphQL circular and large queries (P1), GraphQL introspection and errors (P1) y High privilege user attacks (P0). Para cada uno hay que idear una mitigación suficiente; sin ella, "the feature should not be permitted to launch" (PDF p. 345). Mitigaciones propuestas (Tabla 24-5):
- Better error messages → information disclosure: mensajes genéricos que no revelen info de la aplicación ni de los datos.
- GraphQL compute limits → consultas circulares/grandes: además de rate limits, tiempo máximo de cómputo por query; al agotarse, la petición falla.
- GraphQL configuration → introspection y errores: no exponer errores propios y desactivar las consultas de introspection.
- Privileged permissions rework → high privilege user attacks: tokens privilegiados acotados solo a su funcionalidad; cada llamada API registrada off-platform de forma que el usuario privilegiado no pueda revocar/borrar logs; el review aggregator script solo con permiso de escritura en una columna (aggregate score) y lectura en otra (score).

Una vez implementadas y marcadas las mitigaciones, el propósito inmediato del modelo queda completo y la feature puede avanzar. Si en el futuro aumenta el alcance de la feature, se vuelve al modelo para actualizar el conocimiento documentado, los threat actors y vectores, y reevaluar mitigaciones y delta.

## Resumen
Un threat model bien implementado documenta en un repositorio centralizado tanto el conocimiento técnico como el de seguridad, volviéndose una fuente de información duradera y efectiva. El propio ejercicio identifica threat actors y attack vectors antes incluso de desarrollar la aplicación, y al listarlos junto a las mitigaciones existentes permite refinar la postura de seguridad temprano, cuando los problemas son más baratos de corregir. Se dice que 10 horas de arreglos en la fase de arquitectura equivalen a 100 postlanzamiento, lo que hace del threat model una de las herramientas de seguridad más coste-efectivas.

## Ideas clave
- Un buen threat model cumple cinco metas: documentar conocimiento, identificar threat actors, riesgos (attack vectors), mitigaciones y el delta.
- Un riesgo no es accionable hasta conocer sus mitigaciones existentes; implementar mitigaciones redundantes añade bugs y deuda técnica.
- El logic design (descripción funcional) revela logic vulnerabilities; el technical design revela vulnerabilidades de arquitectura. Ambos son necesarios.
- La lista de threat actors debe incluir usuarios internos, externos y máquina, divididos por permisos autenticados y no autenticados; cada uno tiene su propia attack surface.
- Los attack vectors salen del cross-analysis de logic design, technical design y threat actors, y se priorizan por severidad (P0–P4).
- Modela siempre el peor caso: usuarios internos y scripts automáticos también son threat actors (p. ej. SQL injection, abuso de GraphQL, tokens privilegiados sin accountability).
- La delta identification cruza vectores con mitigaciones; sin mitigación suficiente para cada vector sin cubrir, la feature no debe lanzarse.
- El modelo es un documento vivo: ante cambios de alcance se reevalúan conocimiento, actores, vectores, mitigaciones y delta; arreglar en arquitectura es ~10x más barato que postlanzamiento.
