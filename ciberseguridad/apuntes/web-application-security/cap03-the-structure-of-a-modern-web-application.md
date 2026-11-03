# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 3 — The Structure of a Modern Web Application (La estructura de una aplicación web moderna)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Antes de poder evaluar una aplicación web con fines de reconocimiento (recon), conviene entender las tecnologías comunes que muchas aplicaciones comparten como dependencias: desde librerías de JavaScript y módulos de CSS, hasta servidores web y sistemas operativos. Conocer su rol y sus implementaciones típicas facilita identificarlas rápidamente y buscar malas configuraciones (misconfigurations).

La tesis central es que la aplicación web moderna ya no es un monolito, sino "una combinación de muchas aplicaciones separadas pero simbióticas trabajando en conjunto" (PDF p. 59). Hace una década se renderizaba HTML/JS/CSS en el servidor y el cliente pedía otra página en cada actualización; con AJAX empezaron las peticiones dentro de la sesión, y hoy predominan aplicaciones que se comunican por protocolos de red, con clientes (UI) que corren en el navegador de forma parecida a una aplicación de escritorio y gestionan su propio ciclo de vida sin recargar la página.

Sales sabiendo qué tecnologías componen el stack moderno y por qué cada capa amplía la superficie de ataque: REST, JSON, JavaScript (con sus peculiaridades), frameworks SPA, sistemas de autenticación y autorización, servidores web, bases de datos del lado servidor y del cliente, GraphQL, control de versiones y CDN/cache. La conclusión del libro es que el experto en seguridad actual necesita también conocimientos de ingeniería de software para analizar la aplicación desde el servidor, el cliente y la red intermedia.

## Tecnologías del stack moderno

La aplicación web media suele usar varias de estas tecnologías (PDF p. 59):

- REST API
- JSON o XML
- JavaScript
- Framework SPA (ReactJS, VueJS, EmberJS, AngularJS)
- Un sistema de autenticación y autorización
- Uno o más servidores web (normalmente sobre Linux)
- Uno o más paquetes de software de servidor web (ExpressJS, Apache, NGINX)
- Una o más bases de datos (MySQL, MongoDB, etc.)
- Un almacén local en el cliente (cookies, web storage, IndexedDB)

Las bases de datos NoSQL y del lado cliente son desarrollos recientes; el full stack JavaScript no fue posible hasta la adopción de Node.js y npm. En el horizonte están la Cache API, WebSockets y web assembly (variante de código ensamblador que permitirá lenguajes distintos de JavaScript en el navegador).

## REST APIs

REST (Representational State Transfer) define una API con rasgos únicos:

- Debe estar separada del cliente: el cliente pide recursos sin acceder a la base de datos ni ejecutar lógica de servidor.
- Debe ser stateless: solo toma entradas y da salidas, no almacena estado de la conexión. Sí puede autenticar/autorizar, pero la autorización debe estar tokenizada y enviarse en cada petición.
- Debe ser fácilmente cacheable: las respuestas se marcan como cacheables o no; los cachés deben gestionarse programáticamente para no filtrar información privilegiada.
- Cada endpoint define un objeto o método específico, típicamente jerárquico (ej. `/moderators/joe/logs/12_21_2018`), aprovechando verbos HTTP (GET, POST, PUT, DELETE), lo que hace el endpoint autodocumentado.

Herramientas como Swagger documentan automáticamente los endpoints REST. REST tiene ventajas sobre SOAP: las peticiones apuntan a datos, no a funciones; caché fácil; alta escalabilidad. SOAP obliga a usar XML; REST acepta cualquier formato, pero normalmente usa JSON (más ligero y legible). Es cada vez más raro encontrar SOAP/XML fuera de apps empresariales con compatibilidad legacy.

## JSON (JavaScript Object Notation)

JSON es un estándar abierto usado como formato de datos en tránsito por la mayoría de las REST API. Requisitos que cumple: muy ligero (reduce ancho de banda), requiere poco parseo (reduce carga de hardware), legible por humanos, jerárquico y muy similar a los objetos de JavaScript. Todos los navegadores principales lo parsean nativamente.

Parseo de un string JSON a objeto en el navegador:

```javascript
// convert the string sent by the server to an object
const jsonObject = JSON.parse(jsonString);
```

Conviene instalar un plugin que formatee JSON en el navegador o editor para localizar claves rápidamente durante el pentesting.

## JavaScript

Un servidor reside en un centro de datos y maneja peticiones; un cliente es cualquier dispositivo del usuario, normalmente el navegador. Los servidores corren casi cualquier lenguaje (Python, Java, JavaScript, C++); el cliente no tiene ese lujo: JavaScript es el único lenguaje de scripting del lado cliente en navegadores. Para dominarlo si vienes de otro lenguaje, hay cinco conceptos clave: scope, context, herencia prototípica, asincronía y el DOM del navegador.

### Variables y scope

En ES6 hay cuatro formas de definir una variable:

```javascript
age = 25;        // global definition
var age = 25;    // function scoped
let age = 25;    // block scoped
const age = 25;  // block scoped, without reassignment
```

Sin palabra clave, la variable se eleva (hoisted) al scope global y queda como puntero en `window`, lo que es mala práctica y causa conflictos de namespacing y posibles vulnerabilidades. `var` se liga a la función más cercana (no al bloque), lo que confunde. `let` y `const` son block scoped; `const` además no admite reasignación (como un `final` en Java), aunque sí permite cambiar propiedades de un objeto. La recomendación es usar siempre `let` y `const`.

### Funciones

En JavaScript las funciones son objetos y pueden asignarse a identificadores con distintos scopes. Destacan la función anónima (no referenciable), la función flecha/shorthand `() => {}` (comparte contexto con su padre) y la IIFE `(function() {})()`, que se ejecuta inmediatamente dentro de su propio namespace para encapsular código.

### Contexto (context)

Cada función tiene su contexto, modificable en runtime y referenciable con `this`. Para compartir contexto entre funciones existen `bind`, `call` y `apply`:

```javascript
const getBoundAge = getAge.bind(ageData)('joe');
const boundAge = getAge.call(ageData, 'joe');
const boundAge = getAge.apply(ageData, ['joe']);
```

La diferencia entre `call` y `apply` es que `call` toma una lista de argumentos y `apply` un array. La función flecha hereda el contexto del padre sin necesidad de bind/call/apply.

### Herencia prototípica

JavaScript no usa herencia basada en clases, sino un sistema prototípico flexible. Todo objeto tiene una propiedad `prototype` con un `constructor` que apunta a la función dueña. Al crear un objeto con `new` se genera también `__proto__`, que apunta al prototipo invocado (permite comparar objetos: `prius.__proto__ === charger.__proto__`). Como los objetos son mutables, modificar `prototype` propaga cambios a los hijos en tiempo de ejecución:

```javascript
Vehicle.prototype.getMaxSpeed = function() {
  return 100; // mph
};
prius.getMaxSpeed();   // 100
charger.getMaxSpeed(); // 100
```

De esta propagación nace un ataque propio de sistemas JavaScript: Prototype Pollution, que modifica un objeto padre y altera sin querer la funcionalidad de los hijos.

### Asincronía

Como el tiempo entre petición y respuesta es variable, la web usa modelos asíncronos: las operaciones pueden no resolverse en el orden en que se leen. Métodos históricos y actuales de manejarla:

- Callbacks: muy rápidos y eficientes, pero difíciles de leer y depurar (anidamiento horizontal).
- Promises: objeto reutilizable con `.then()` y `.catch()`; crece verticalmente y facilita el manejo de errores. Interoperable con callbacks.
- Función `async`: convierte una función en promise; `await` ante una llamada detiene la ejecución dentro de esa función hasta que resuelva, sin bloquear el código externo. Es la forma más legible.

### Browser DOM

El DOM es la representación jerárquica de datos que gestiona el estado del navegador; actúa como librería estándar de JavaScript, bien probada y consistente entre navegadores. Su función principal es ofrecer una interfaz común para definir un árbol de nodos que representa la página. Sus objetos principales son `window` y `document`, definidos en una especificación mantenida por WHATWG. Ejemplos de funciones del DOM (no de JS): `document.querySelector()` y `document.implementation`. No todos los fallos de script vienen de mal JavaScript; algunos nacen de una implementación incorrecta del DOM.

## SPA Frameworks

Los sitios antiguos combinaban scripts ad hoc y plantillas HTML reutilizadas, un modelo no escalable para apps complejas. Los frameworks de single-page application (SPA) cierran la brecha con las apps de escritorio: permiten aplicaciones JavaScript complejas que guardan su propio estado interno y se componen de componentes de UI reutilizables, cada uno con su ciclo de vida (renderizado y ejecución de lógica). Ejemplos open source grandes: ReactJS, EmberJS, VueJS y AngularJS. Construidos sobre JavaScript y el DOM, aportan complejidad extra en funcionalidad y seguridad.

## Sistemas de autenticación y autorización

- Authentication (autenticación): flujo que identifica al usuario; confirma que "joe123" es realmente "joe123" y no "susan1988".
- Authorization (autorización): flujo que determina a qué recursos tiene acceso cada usuario.

HTTP basic authentication adjunta en cada petición una cabecera `Authorization` con `Basic: <base64-encoded username:password>`; tiene fallos graves (fácil de filtrar por WiFi comprometido sobre HTTP o por XSS). Digest authentication usa hashes criptográficos en lugar de base64 y es más popular por sus defensas frente a interceptación y replay. OAuth permite que un sitio grande (Facebook, Google) emita un token que verifica la identidad en un sitio socio: cómodo porque los datos se actualizan en un solo sitio, pero peligroso porque un sitio comprometido puede comprometer varios perfiles. Suelen combinarse con MFA.

Las apps bien diseñadas tienen una clase de autorización centralizada. Las APIs mal escritas reimplementan los chequeos por cada endpoint, lo que suele dejar APIs con controles insuficientes por error humano. Recursos que siempre deben tener chequeos de autorización: actualización de settings/perfil, restablecimiento de contraseña, lectura/escritura de mensajes privados, funcionalidad de pago y funciones de usuario elevado (moderación).

## Servidores web

El software de servidor web corre sobre un sistema operativo (normalmente una distro Linux como Ubuntu, CentOS o Red Hat) y hardware en un centro de datos. Los tres grandes:

- Apache: open source, casi 30 años de desarrollo (desde 1995), sirve cerca de la mitad de los sitios del mundo; muy configurable y extensible.
- NGINX ("Engine X"): ~30% de los servidores y creciendo; de F5 Networks con modelo paid+. Ideal para gran volumen de conexiones únicas por su bajo overhead por conexión.
- Microsoft IIS: en declive por licencias caras y falta de compatibilidad con OSS Unix; adecuado para tecnologías específicas de Microsoft.

Conocer los tres ayuda a detectar vulnerabilidades por configuración incorrecta, no solo por la lógica de aplicación.

## Bases de datos del lado servidor

Los datos deben persistirse en disco de forma fiable, rápida y consultable (la memoria es volátil y cara).

- SQL: la más popular de propósito general; estricta pero rápida y fácil. Grandes: PostgreSQL, Microsoft SQL Server, MySQL, SQLite.
- NoSQL (schema-less): almacenan "documentos" flexibles; MongoDB, DocumentDB, CouchDB. Menos eficientes para consultas o agregaciones.
- Especializadas: motores de búsqueda como Elasticsearch, que se sincroniza con la base principal.

SQL injection es el arquetipo conocido cuando las consultas no se forman bien, pero los ataques de inyección funcionan contra casi cualquier base si el atacante aprende su modelo de consulta. Muchas apps usan varias bases a la vez: una con SQL seguro puede tener consultas o permisos inseguros en MongoDB o Elasticsearch.

## Almacenes del lado cliente

- Local storage: contenedor clave/valor gestionado por el navegador que respeta la SOP (impide que otros dominios accedan a datos ajenos) y persiste aunque se cierre pestaña o navegador.
- Session storage: igual que local storage, pero persiste solo hasta que se cierra la pestaña; útil para datos más críticos en máquinas compartidas.
- IndexedDB: base NoSQL basada en JavaScript, consultable y asíncrona; más potente que local storage, usada en juegos y apps interactivas (editores de imágenes). Comprobación: `if (window.indexedDB) { console.log('true'); }`.

En apps mal arquitecturadas, los almacenes del cliente pueden revelar información sensible como tokens de autenticación u otros secretos (PDF p. 87).

## GraphQL

Método de consulta de endpoints lanzado en septiembre de 2015. Suele implementarse envolviendo endpoints existentes y permitiendo consultarlos con el lenguaje de GraphQL, que agrupa peticiones para ahorrar latencia de red. Funciones extra sobre REST: peticiones de campos específicos, argumentos complejos, alias de campos, fragmentos, operaciones, variables, directivas y mutations.

Ejemplo de consulta:

```graphql
query GetLeadActorFromMovie($movie: Movie)
 actor(movie: $movie) {
   name, age, gender,
   otherMovies {
     name
  }
}
```

Donde REST necesitaría dos consultas (`getLeadActorByMovie/:movieName` y luego `getMoviesByLeadActor/:actorName`), GraphQL las combina en una sola, reduciendo de dos saltos de red a uno.

## Sistemas de control de versiones (VCS)

Casi todas las apps modernas usan un VCS. El más común es Git, creado por Linus Torvalds y la Linux Foundation; ofrece branches, stashes y forks, y permite fusionar copias con distintos algoritmos preservando el historial. Implementaciones alojadas populares: GitHub (de Microsoft) y GitLab.

Flujo típico de Git:

```bash
git init
git remote add origin <github-repository-url>
touch .gitignore
echo "node_modules" > .gitignore
git add -A
git commit -m "initial commit"
git push --set-upstream origin main
```

Las apps modernas usan además CI/CD (integración y entrega continuas). El continuous deployment —correr tests y desplegar al hacer push— es una de las integraciones más comunes, disparada a menudo por un Git hook. Por ello la seguridad ya no depende solo del código y la red de la aplicación, sino también del VCS y del pipeline CI/CD: un compromiso en cualquiera de estas capas puede ser catastrófico.

## CDN/Cache

Las apps modernas descargan contenido estático o poco actualizado a redes de distribución de contenido (CDN) y a cachés en varias capas del stack, incluido el cliente. Una CDN escala con servidores en todo el mundo que replican el contenido estático vía API, mientras el servidor web actúa como fuente única de verdad (single source of truth). Ventaja: escalado mundial muy rápido; riesgo principal: el stale caching (caché obsoleto), que puede provocar escalada de privilegios o divulgación de información.

Las cachés locales y de red se usan con más frecuencia que las CDN. El caché del navegador se configura con cabeceras como `etag` o `cache-control`, y las apps también usan local storage, session storage e IndexedDB. Esta expansión obliga a evaluar la seguridad de los datos en lugares nuevos: las cachés pueden corromperse o desincronizarse.

## Ideas clave

- La app web moderna es un conjunto de aplicaciones simbióticas comunicadas por red, no un monolito; esto amplía mucho la superficie de ataque.
- REST exige separación del cliente, statelessness, cacheabilidad y endpoints jerárquicos con verbos HTTP; JSON es su formato en tránsito habitual por ligero y legible.
- JavaScript tiene cinco conceptos clave para seguridad: scope (usar `let`/`const`, no globales), context (`this`, `bind`/`call`/`apply`), herencia prototípica (origen de Prototype Pollution), asincronía (callbacks, promises, `async`/`await`) y el DOM (fallos pueden venir de su implementación).
- Autenticación identifica al usuario y autorización define su acceso; digest supera a basic; OAuth es cómodo pero propaga compromisos; la autorización debe estar centralizada y cubrir settings, password resets, mensajes privados y funciones de pago o elevadas.
- Los tres grandes servidores web son Apache (~mitad de sitios), NGINX (~30%, alto volumen) y Microsoft IIS (en declive); muchas vulnerabilidades vienen de mala configuración.
- Conviven bases SQL (PostgreSQL, SQL Server, MySQL, SQLite) y NoSQL (MongoDB, CouchDB, Elasticsearch); la inyección afecta a cualquier base y una app puede ser segura en una y vulnerable en otra.
- Los almacenes del cliente (local storage, session storage, IndexedDB) pueden exponer secretos como tokens si la app está mal diseñada.
- GraphQL combina consultas REST en un solo salto de red; el VCS (Git/GitHub/GitLab) y el pipeline CI/CD son hoy parte de la superficie de seguridad, igual que las CDN y cachés, donde el stale caching puede causar escalada de privilegios o fuga de información.
