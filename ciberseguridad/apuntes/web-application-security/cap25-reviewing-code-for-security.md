# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 25 — Reviewing Code for Security (Revisión de código en busca de seguridad)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
Este capítulo explica cómo y cuándo revisar el código en busca de fallos de seguridad dentro de un proceso de desarrollo. La tesis central es que la revisión de código debe ser el *segundo* paso, siempre después de la revisión de arquitectura: "The code review stage must always occur after the architecture stage" (PDF p. 348). Revisar la arquitectura antes de escribir código evita que una filosofía de "move fast and break things" sirva de excusa para saltarse los procesos de seguridad.

La revisión de seguridad del código aporta dos beneficios: la seguridad en sí y un par de ojos externos al equipo que detectan bugs y fallos de arquitectura que de otro modo pasarían inadvertidos. Es útil tanto para la funcionalidad como para la seguridad de la aplicación, y añadirla a organizaciones que solo hacen revisiones funcionales reduce drásticamente los bugs de alto impacto que llegarían a producción.

Sales sabiendo cuándo hacer la revisión (normalmente en los merge requests / pull requests), cómo arrancarla con comandos de git, la diferencia entre vulnerabilidades arquetípicas y de lógica de negocio, un marco para decidir por dónde empezar, y un catálogo de anti-patrones de codificación segura (blocklists, código boilerplate, confianza por defecto y acoplamiento cliente/servidor).

## El ejemplo que recorre el capítulo
El capítulo usa **MegaChat**, un portal social que se integraría en MegaBank, para ilustrar las vulnerabilidades de lógica de negocio. Los usuarios registrados solicitan membresía, que los moderadores aprueban revisando su actividad. Hay tres roles: user (por defecto), member y moderator, cada uno con permisos distintos.

Del contexto se extraen tres ejes:
- **Usuarios y roles:** son clientes de MegaBank divididos en user, member y moderator, con permisos y funcionalidad diferentes.
- **Funcionalidad:** users, members y moderators pueden publicar texto; members y moderators pueden subir vídeo, juegos e imágenes; los moderators pueden ascender users a members.
- **Impacto de negocio:** alojar vídeo, juegos e imágenes es caro; la membresía protege del *freeloading* (coste de almacenamiento/ancho de banda) y de bots.

Con ese contexto se distinguen los dos tipos de fallo: una vulnerabilidad arquetípica sería un XSS en un post de usuario; una de lógica de negocio sería un endpoint mal codificado que permite enviar `isMember: true` para publicar vídeos sin que un moderador haya concedido la membresía.

## Cuándo revisar el código
Las revisiones de seguridad tienen más sentido al hacer merge requests (pull requests), porque el conjunto de la funcionalidad ya está desarrollado y todos los sistemas integrados, lo que permite revisar el alcance completo de una sola vez. Para funcionalidades críticas de seguridad puede valer la pena entrelazar la revisión con el desarrollo de forma más granular (por commit o con *pair-programming*): una mente centrada en la funcionalidad y otra en la seguridad. El momento concreto depende de los procesos de cada organización.

## How to Start a Code Review (Cómo iniciar la revisión)
La revisión de seguridad funciona de forma muy similar a la revisión funcional, que ya es estándar, así que la curva de aprendizaje es corta. El primer paso es bajar la rama a una máquina local; las herramientas web de GitHub o GitLab existen pero no son tan completas como las locales. Flujo típico desde la terminal:

```
1. git checkout main
2. git pull origin main
3. git checkout <username>/feature
4. git diff origin/main...
```

El `git diff` devuelve la lista de archivos que difieren entre `main` y la rama actual, y la lista de cambios en esos archivos. Es el punto de partida común a la revisión funcional y a la de seguridad; a partir de ahí divergen.

## Vulnerabilidades arquetípicas vs. de lógica de negocio
Una revisión funcional comprueba que el código cumple la especificación y no tiene bugs de usabilidad. Una revisión de seguridad busca vulnerabilidades comunes (XSS, CSRF, injection, etc.) pero, sobre todo, vulnerabilidades a nivel de lógica que requieren contexto profundo del propósito del código y que las herramientas automáticas o scanners no detectan fácilmente.

Para hallar fallos de lógica hay que entender primero el objetivo de la funcionalidad: sus usuarios, su funcionalidad y su impacto de negocio. Muchas vulnerabilidades del libro son arquetipos conocidos, pero una aplicación con un caso de uso muy específico puede tener fallos que no caben en un libro de educación general.

## Where to Start a Security Review (Por dónde empezar)
Lo ideal es empezar por los componentes de mayor riesgo, pero no siempre se conocen (frecuente en consultoría o productos ya existentes). El autor propone un marco: imagina una app web básica con un cliente en el navegador y un servidor. Empezar por el servidor es válido, pero puede haber funcionalidad no expuesta al cliente, con lo que el esfuerzo se desviaría hacia código de bajo riesgo. Un buen punto de partida es donde el cliente (navegador) hace peticiones al servidor, porque revela la superficie de ataque, los datos intercambiados y cómo se interpretan los payloads.

Camino sugerido:
1. Evaluar el código del cliente para entender la lógica de negocio y qué podrán hacer los usuarios.
2. Evaluar la capa de API, en particular las APIs encontradas en la revisión del cliente, y descubrir sus dependencias.
3. Trazar las dependencias de la API: bases de datos, librerías auxiliares, funciones de logging, etc. Con esto se cubre casi toda la funcionalidad orientada al usuario.
4. Buscar APIs públicas expuestas sin querer o pensadas para futuras versiones, y revisarlas al encontrarlas.
5. Continuar por el resto del código base, ya con familiaridad adquirida de forma orgánica.

No es el único método; aplicaciones con requisitos de seguridad nicho pueden necesitar otra ruta. La ventaja es ganar familiaridad a ritmo orgánico y priorizar la funcionalidad orientada al usuario, dejando lo de bajo riesgo para el final.

## Secure-Coding Anti-Patterns (Anti-patrones de codificación segura)
La revisión de código comparte similitudes con la de arquitectura, pero es el momento ideal para *encontrar* vulnerabilidades reales (en arquitectura solo son hipotéticas). Un anti-patrón suele ser una solución apresurada o implementada sin el conocimiento previo adecuado; saber detectarlos agiliza la revisión.

### Blocklists (Listas de bloqueo)
Las mitigaciones temporales deben evitarse salvo que exista un plan previo para la solución definitiva. Una blocklist es incompleta y temporal: solo protege si se tiene conocimiento perfecto de todas las entradas presentes y futuras, algo improbable. Un atacante puede simplemente comprar otro dominio.

```javascript
const blocklist = ['http://www.evil.com', 'http://www.badguys.net'];

const isDomainAccepted = function(domain) {
  return !blocklist.includes(domain);
};
```

Las allowlists siempre son preferibles en seguridad; basta invertir la lógica:

```javascript
const allowlist = ['https://happy-site.com', 'https://www.my-friends.com'];

const isDomainAccepted = function(domain) {
  return allowlist.includes(domain);
};
```

El coste de mantenimiento de una allowlist se reduce combinando esfuerzo manual y automatizado (por ejemplo, exigir a los socios integrantes su web y licencia de negocio antes de añadirlos).

### Boilerplate Code (Código de plantilla por defecto)
Usar código por defecto de frameworks es peligroso: la seguridad debería venir reforzada "out of the box" y requerir aflojarla, no endurecerla. Ejemplo clásico: versiones antiguas de MongoDB eran accesibles por internet por defecto y sin autenticación obligatoria, lo que provocó que decenas de miles de bases de datos fueran secuestradas por scripts que exigían Bitcoin. Otros casos: una página 404 boilerplate de Ruby on Rails delata la versión usada, y EmberJS tiene una landing por defecto que debe quitarse en producción. No lanzar código boilerplate a producción sin evaluarlo y configurarlo.

### Trust-by-Default (Confianza por defecto)
Si una app genera logs, escribe en disco y actualiza una base de datos SQL bajo una única cuenta de usuario con todos esos permisos, una vulnerabilidad de ejecución de código comprometería los tres recursos. Una app segura genera permisos independientes para cada módulo (logging, escritura en disco, operaciones de base de datos), cada uno bajo su propio usuario con los permisos mínimos necesarios, de modo que un fallo en un módulo no se propague a los demás.

### Client/Server Separation (Separación cliente/servidor)
El anti-patrón de acoplamiento cliente/servidor ocurre cuando el código del cliente y del servidor están tan ligados que uno no funciona sin el otro (típico en apps antiguas o monolíticas). Una app segura desarrolla cliente y servidor de forma independiente, comunicándose por red con un formato de datos y protocolo predefinidos. El acoplamiento profundo (por ejemplo, plantillas PHP con lógica de autenticación) facilita la explotación, porque el servidor debe parsear HTML y evitar ejecución de scripts o manipulación de parámetros. En una app bien separada, el servidor rechaza cualquier HTML y solo acepta payloads en un formato predefinido. La separación de concerns reduce los mecanismos de seguridad que cada módulo debe gestionar.

## Ideas clave
- La revisión de código de seguridad debe ser el segundo paso, siempre después de la revisión de arquitectura.
- El mejor momento suele ser el merge request (pull request); para funciones críticas, conviene revisar por commit o con pair-programming.
- Flujo de arranque: checkout/pull de `main`, checkout de la rama de feature y `git diff origin/main...`.
- Lo distintivo de la revisión de seguridad es cazar vulnerabilidades de lógica de negocio (ej. `isMember: true`), que requieren contexto y escapan a los scanners.
- Marco recomendado: empezar por el cliente, seguir las llamadas a la API, trazar dependencias, buscar APIs expuestas sin querer y luego el resto, por orden de riesgo.
- Anti-patrón blocklist: prefiere siempre allowlists; las blocklists son incompletas y temporales.
- Anti-patrón boilerplate: el código por defecto de frameworks (MongoDB, Rails, EmberJS) puede filtrar información o exponer servicios; evalúalo antes de producción.
- Anti-patrones trust-by-default y acoplamiento cliente/servidor: aplica permisos mínimos por módulo y separa cliente y servidor con un formato de datos predefinido.
