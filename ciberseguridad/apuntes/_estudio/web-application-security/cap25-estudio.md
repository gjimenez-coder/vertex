# Reviewing Code for Security (Revisión de código en busca de seguridad) — Estudio

## Tarjetas de repaso

P: ¿En qué orden debe situarse la revisión de código de seguridad respecto a la revisión de arquitectura? / R: Siempre como segundo paso, después de la revisión de arquitectura ("The code review stage must always occur after the architecture stage").

P: ¿Qué dos beneficios aporta la revisión de seguridad del código? / R: La seguridad en sí y un par de ojos externos al equipo que detectan bugs y fallos de arquitectura que de otro modo pasarían inadvertidos.

P: ¿Cuál es el momento que normalmente tiene más sentido para una revisión de seguridad? / R: El merge request (pull request), porque la funcionalidad ya está desarrollada y los sistemas integrados, permitiendo revisar el alcance completo de una vez.

P: ¿Cuándo conviene entrelazar revisión y desarrollo de forma más granular? / R: En funcionalidades críticas de seguridad, revisando por commit o con pair-programming (una mente en funcionalidad, otra en seguridad).

P: ¿Cuál es el flujo de comandos git para iniciar la revisión? / R: `git checkout main`, `git pull origin main`, `git checkout <username>/feature`, `git diff origin/main...`.

P: ¿Qué devuelve `git diff origin/main...`? / R: La lista de archivos que difieren entre main y la rama actual y la lista de cambios en esos archivos; es el punto de partida común a la revisión funcional y de seguridad.

P: ¿Qué diferencia una vulnerabilidad arquetípica de una de lógica de negocio? / R: La arquetípica es un fallo común (XSS, CSRF, injection); la de lógica de negocio requiere contexto profundo del propósito del código y escapa a los scanners automáticos.

P: En MegaChat, ¿qué ejemplo ilustra una vulnerabilidad de lógica de negocio? / R: Un endpoint mal codificado que permite enviar `isMember: true` para publicar vídeos sin que un moderador haya concedido la membresía.

P: ¿Cuáles son los tres roles de MegaChat y una diferencia de permisos? / R: user (por defecto), member y moderator; members y moderators pueden subir vídeo, juegos e imágenes, y los moderators pueden ascender users a members.

P: ¿Por qué es un buen punto de partida donde el cliente hace peticiones al servidor? / R: Porque revela la superficie de ataque, los datos intercambiados y cómo se interpretan los payloads.

P: ¿Por qué se prefieren las allowlists frente a las blocklists? / R: Una blocklist es incompleta y temporal; solo protege con conocimiento perfecto de todas las entradas presentes y futuras, y un atacante puede comprar otro dominio.

P: ¿Qué principio defiende el anti-patrón boilerplate? / R: Que la seguridad debería venir reforzada "out of the box" y requerir aflojarla, no endurecerla; no lanzar código por defecto a producción sin evaluarlo y configurarlo.

P: ¿Qué riesgo introduce el anti-patrón trust-by-default? / R: Ejecutar logging, escritura en disco y operaciones SQL bajo una única cuenta con todos los permisos hace que una ejecución de código comprometa los tres recursos a la vez.

P: ¿Cómo mitiga una app segura el trust-by-default? / R: Generando permisos independientes por módulo, cada uno bajo su propio usuario con los permisos mínimos necesarios, para que un fallo no se propague.

P: ¿Qué caracteriza el anti-patrón de acoplamiento cliente/servidor y cómo se corrige? / R: Cliente y servidor tan ligados que uno no funciona sin el otro; se corrige desarrollándolos de forma independiente y comunicándolos por red con un formato de datos y protocolo predefinidos.

## Preguntas de autoevaluación

P: ¿Por qué la "move fast and break things" no justifica saltarse la revisión de arquitectura previa a la de código? / R: Porque revisar la arquitectura antes de escribir código evita que esa filosofía sirva de excusa para saltarse los procesos de seguridad; la revisión de código debe ser el segundo paso. (Sección: Lo que necesitas saber)

P: ¿Qué aporta añadir revisión de seguridad a una organización que solo hace revisiones funcionales? / R: Reduce drásticamente los bugs de alto impacto que llegarían a producción, y ayuda tanto a la funcionalidad como a la seguridad. (Sección: Lo que necesitas saber)

P: ¿Por qué se recomienda bajar la rama a una máquina local en lugar de usar solo las herramientas web? / R: Porque las herramientas web de GitHub o GitLab existen pero no son tan completas como las locales. (Sección: How to Start a Code Review)

P: ¿Qué hay que entender antes de poder hallar fallos de lógica de negocio? / R: El objetivo de la funcionalidad: sus usuarios, su funcionalidad y su impacto de negocio. (Sección: Vulnerabilidades arquetípicas vs. de lógica de negocio)

P: ¿Cuál es el camino sugerido para una revisión de seguridad por orden de riesgo? / R: Cliente, luego la capa de API (en especial las APIs vistas en el cliente), trazar dependencias (bases de datos, librerías, logging), buscar APIs públicas expuestas sin querer y por último el resto del código base. (Sección: Where to Start a Security Review)

P: ¿Qué riesgo concreto ilustra el ejemplo de boilerplate con MongoDB? / R: Versiones antiguas eran accesibles por internet por defecto y sin autenticación obligatoria, lo que provocó que decenas de miles de bases de datos fueran secuestradas por scripts que exigían Bitcoin. (Sección: Secure-Coding Anti-Patterns → Boilerplate Code)

P: ¿Por qué el acoplamiento profundo (p. ej. plantillas PHP con lógica de autenticación) facilita la explotación? / R: Porque el servidor debe parsear HTML y evitar ejecución de scripts o manipulación de parámetros; una app separada rechaza el HTML y solo acepta payloads en un formato predefinido. (Sección: Secure-Coding Anti-Patterns → Client/Server Separation)

P: ¿Por qué empezar la revisión por el servidor puede desviar el esfuerzo? / R: Porque puede haber funcionalidad no expuesta al cliente, con lo que el esfuerzo se desviaría hacia código de bajo riesgo. (Sección: Where to Start a Security Review)

## Puntos a dominar

- Situar la revisión de código siempre después de la revisión de arquitectura.
- Elegir el momento de revisión: merge request por defecto; por commit o pair-programming para funciones críticas.
- Ejecutar el flujo de arranque: checkout/pull de main, checkout de la rama de feature y `git diff origin/main...`.
- Distinguir vulnerabilidades arquetípicas (XSS, CSRF, injection) de las de lógica de negocio (ej. `isMember: true`), que requieren contexto y escapan a los scanners.
- Aplicar el marco por orden de riesgo: cliente → API → dependencias → APIs expuestas sin querer → resto del código.
- Reconocer y corregir los cuatro anti-patrones: blocklists (preferir allowlists), boilerplate (evaluar antes de producción), trust-by-default (permisos mínimos por módulo) y acoplamiento cliente/servidor (separar con formato de datos predefinido).
