# The Structure of a Modern Web Application — Estudio

## Tarjetas de repaso

P: Según el capítulo, ¿qué es hoy una aplicación web moderna frente al antiguo monolito?
R: Una combinación de muchas aplicaciones separadas pero simbióticas trabajando en conjunto, comunicadas por protocolos de red, con un cliente (UI) que corre en el navegador como una app de escritorio y gestiona su propio ciclo de vida sin recargar la página.

P: ¿Cuáles son los cuatro rasgos que debe cumplir una REST API?
R: Estar separada del cliente, ser stateless, ser fácilmente cacheable y definir cada endpoint como un objeto o método específico y jerárquico usando verbos HTTP (GET, POST, PUT, DELETE).

P: ¿Por qué JSON se usa como formato en tránsito en la mayoría de las REST API?
R: Porque es muy ligero (reduce ancho de banda), requiere poco parseo (reduce carga de hardware), es legible por humanos, jerárquico, muy similar a los objetos de JavaScript y todos los navegadores principales lo parsean nativamente.

P: ¿Cuáles son los cinco conceptos clave de JavaScript para dominarlo desde la seguridad?
R: Scope, context, herencia prototípica, asincronía y el DOM del navegador.

P: ¿Qué diferencia a las cuatro formas de definir variables en ES6 y cuál es la recomendación?
R: Sin palabra clave la variable se eleva (hoisted) al scope global; `var` es function scoped; `let` es block scoped; `const` es block scoped sin reasignación. La recomendación es usar siempre `let` y `const`.

P: ¿Qué es Prototype Pollution y de dónde nace?
R: Un ataque propio de sistemas JavaScript que modifica un objeto padre y altera sin querer la funcionalidad de los hijos; nace de que al modificar `prototype` los cambios se propagan a los objetos hijos en tiempo de ejecución.

P: ¿Qué diferencia hay entre `call` y `apply`?
R: `call` toma una lista de argumentos y `apply` toma un array; ambos (junto con `bind`) sirven para compartir contexto entre funciones.

P: ¿Cuál es la diferencia entre autenticación y autorización?
R: La autenticación es el flujo que identifica al usuario (confirma que "joe123" es realmente "joe123"); la autorización determina a qué recursos tiene acceso cada usuario.

P: ¿Por qué digest authentication es más popular que HTTP basic authentication?
R: Porque usa hashes criptográficos en lugar de base64, ofreciendo mejores defensas frente a interceptación y replay; basic es fácil de filtrar por WiFi comprometido sobre HTTP o por XSS.

P: ¿Cuáles son los tres grandes servidores web y su cuota aproximada?
R: Apache (open source, sirve cerca de la mitad de los sitios), NGINX (~30% y creciendo, ideal para gran volumen de conexiones) y Microsoft IIS (en declive por licencias caras y falta de compatibilidad con OSS Unix).

P: ¿Qué diferencia a las bases SQL de las NoSQL según el capítulo?
R: SQL es de propósito general, estricta pero rápida y fácil (PostgreSQL, SQL Server, MySQL, SQLite); NoSQL es schema-less y almacena "documentos" flexibles (MongoDB, CouchDB), pero es menos eficiente para consultas o agregaciones.

P: ¿Qué diferencia a local storage, session storage e IndexedDB?
R: Local storage es un contenedor clave/valor que respeta la SOP y persiste tras cerrar el navegador; session storage es igual pero persiste solo hasta cerrar la pestaña; IndexedDB es una base NoSQL en JavaScript, consultable y asíncrona, más potente que local storage.

P: ¿Qué ventaja aporta GraphQL frente a REST?
R: Agrupa peticiones para ahorrar latencia de red, combinando en una sola consulta lo que REST necesitaría en varias (reduciendo, por ejemplo, de dos saltos de red a uno).

P: ¿Por qué el VCS y el pipeline CI/CD forman parte de la superficie de seguridad?
R: Porque el continuous deployment corre tests y despliega al hacer push (a menudo disparado por un Git hook), así que la seguridad ya no depende solo del código y la red, sino también del VCS y el pipeline; un compromiso en cualquiera de estas capas puede ser catastrófico.

P: ¿Cuál es el riesgo principal de las CDN y cachés?
R: El stale caching (caché obsoleto), que puede provocar escalada de privilegios o divulgación de información; las cachés pueden corromperse o desincronizarse.

## Preguntas de autoevaluación

P: ¿Por qué conviene conocer las tecnologías comunes del stack antes de hacer reconocimiento (recon) de una aplicación web?
R: Porque conocer su rol e implementaciones típicas facilita identificarlas rápidamente y buscar malas configuraciones (misconfigurations). (Sección "Lo que necesitas saber")

P: ¿Qué ventajas tiene REST sobre SOAP y por qué REST suele usar JSON?
R: En REST las peticiones apuntan a datos y no a funciones, el caché es fácil y es altamente escalable; SOAP obliga a usar XML, mientras que REST acepta cualquier formato pero normalmente usa JSON por ser más ligero y legible. (Sección "REST APIs")

P: ¿Por qué no todos los fallos de script provienen de mal JavaScript?
R: Porque algunos nacen de una implementación incorrecta del DOM, que es la representación jerárquica que gestiona el estado del navegador y actúa como librería estándar de JavaScript. (Sección "JavaScript" — Browser DOM)

P: ¿Qué problema de seguridad suelen tener las APIs que reimplementan los chequeos de autorización por cada endpoint?
R: Que suelen quedar con controles de autorización insuficientes por error humano; lo recomendable es una clase de autorización centralizada. (Sección "Sistemas de autenticación y autorización")

P: ¿Qué recursos deben tener siempre chequeos de autorización?
R: La actualización de settings/perfil, el restablecimiento de contraseña, la lectura/escritura de mensajes privados, la funcionalidad de pago y las funciones de usuario elevado (moderación). (Sección "Sistemas de autenticación y autorización")

P: Si una aplicación usa varias bases de datos, ¿basta con asegurar la SQL?
R: No; los ataques de inyección funcionan contra casi cualquier base si el atacante aprende su modelo de consulta, y una app con SQL seguro puede tener consultas o permisos inseguros en MongoDB o Elasticsearch. (Sección "Bases de datos del lado servidor")

P: ¿Qué riesgo introducen los almacenes del lado cliente en apps mal arquitecturadas?
R: Pueden revelar información sensible como tokens de autenticación u otros secretos. (Sección "Almacenes del lado cliente", PDF p. 87)

P: ¿Qué conocimientos concluye el libro que necesita el experto en seguridad actual y por qué?
R: Conocimientos de ingeniería de software, para poder analizar la aplicación desde el servidor, el cliente y la red intermedia. (Sección "Lo que necesitas saber")

## Puntos a dominar

- Entender que la app web moderna es un conjunto de aplicaciones simbióticas comunicadas por red y cómo cada capa amplía la superficie de ataque.
- Reconocer los rasgos de una REST API (separación del cliente, statelessness, cacheabilidad, endpoints jerárquicos con verbos HTTP) y por qué JSON es su formato habitual.
- Dominar los cinco conceptos clave de JavaScript: scope (`let`/`const`, no globales), context (`this`, `bind`/`call`/`apply`), herencia prototípica (origen de Prototype Pollution), asincronía (callbacks, promises, `async`/`await`) y el DOM.
- Distinguir autenticación de autorización y saber que digest supera a basic, que OAuth propaga compromisos y que la autorización debe estar centralizada.
- Identificar los tres grandes servidores web (Apache, NGINX, IIS) y saber que muchas vulnerabilidades vienen de mala configuración.
- Diferenciar bases SQL de NoSQL y entender que la inyección afecta a cualquier base y que una app puede ser segura en una y vulnerable en otra.
- Conocer los almacenes del cliente (local storage, session storage, IndexedDB) y su riesgo de exponer secretos.
- Comprender el valor de GraphQL (combinar consultas en un salto de red) y por qué VCS/CI/CD y CDN/cachés forman parte de la superficie de seguridad, con el stale caching como riesgo principal.
