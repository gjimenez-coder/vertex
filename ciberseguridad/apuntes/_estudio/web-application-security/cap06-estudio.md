# Identifying Third-Party Dependencies (Identificando dependencias de terceros) — Estudio

## Tarjetas de repaso

P: ¿Por qué las dependencias de terceros son un vector de ataque frecuente? / R: Porque suelen no pasar por una revisión de seguridad tan rigurosa como el código propio, y a menudo basta con copiar un ataque conocido de una base de datos de CVE.

P: ¿Qué son las dependencias propietarias frente a las gratuitas? / R: Las propietarias se integran bajo licencia; las gratuitas suelen provenir de la comunidad OSS.

P: ¿Qué abre la posibilidad de reutilizar ataques conocidos? / R: Fijar la versión de una dependencia, que permite aplicar vulnerabilidades públicas como ReDoS, prototype pollution y XSS, sobre todo en versiones antiguas.

P: ¿Cuáles son los mayores frameworks SPA citados a 2023? / R: EmberJS (LinkedIn, Netflix), Angular (Google), React (Facebook) y VueJS (Adobe, GitLab).

P: ¿Cómo se detecta EmberJS en el cliente? / R: Define el global `Ember`, etiqueta los DOM elements con un `ember-id` (`id=ember1`, `id=ember2`…) y los envuelve en un padre `class="ember-application"`.

P: ¿Cómo se detecta Angular 4.0+ si eliminó su global `angular`? / R: Comprobando si existe el global `ng`; la versión se obtiene del atributo `ng-version` de los root elements con `getAllAngularRootElements()`.

P: ¿Qué señal es inequívoca de React en el HTML? / R: Las script tags con `type="text/jsx"`; además expone el global `React` con la versión en `React.version`.

P: ¿Qué globals usan algunas librerías JS helper conocidas? / R: Underscore y Lodash usan `_`; JQuery usa `$`.

P: ¿Qué técnica conviene más que buscar globals concretos para librerías externas? / R: Enumerar todos los scripts externos con `querySelectorAll('script')` y filtrar por `script.src` (y los `link` con `rel="stylesheet"` para CSS).

P: ¿Qué cabeceras HTTP pueden filtrar el software y versión del servidor? / R: `X-Powered-By`, `Server` y `X-AspNet-Version`, habilitadas por defecto en versiones antiguas de Microsoft IIS.

P: ¿Cómo acota la versión el fingerprinting de la página 404 de Ruby on Rails? / R: Buscando marcas que aparecen o faltan en la 404 (atributos HTML, caracteres, selectores CSS con namespace) y cruzándolas con el historial Git y el calendario de versiones de RubyGems.

P: ¿Qué vulnerabilidad se liga al rango de versiones de Rails del ejemplo? / R: CVE-2016-6316, un XSS en versiones 3.2.x hasta 4.2.7 que permitía inyectar HTML (con script tags) en campos leídos por un Action View Tag helper.

P: ¿Qué es el primary key scanning? / R: Una técnica para identificar el motor de base de datos analizando el método de generación por defecto de la clave primaria en suficientes peticiones.

P: ¿Cómo se identifica MongoDB mediante su clave primaria? / R: Genera un campo `_id` de tipo `ObjectId` con un string hexadecimal de 12 bytes (4 de timestamp Unix, 5 aleatorios y 3 de contador), p. ej. `507f1f77bcf86cd799439011`.

## Preguntas de autoevaluación

P: ¿Cuál es la tesis del capítulo sobre las integraciones de terceros durante el reconocimiento? / R: Que son un vector de ataque frecuente y que muchas veces no hace falta preparar un ataque, basta con copiar uno conocido de una base de datos de CVE; por eso hay que atender tanto a la dependencia como al método de integración. (Lo que necesitas saber)

P: ¿Por qué detectar frameworks de cliente es más fácil que detectar los de servidor? / R: Porque el código del cliente está en memoria y es accesible vía el DOM, mientras que las dependencias de servidor solo dejan marcas en el tráfico HTTP o exponen endpoints. (Detecting Server-Side Frameworks)

P: ¿Cómo se reactiva la inspección de componentes en una app VueJS que ignora las dev tools? / R: Estableciendo `Vue.config.devtools = true`, tras obtener la versión desde `Vue.version`. (Detecting Client-Side Frameworks / VueJS)

P: ¿Qué tres cambios en la página 404 de Rails sirven como marcas de fecha y a qué fechas corresponden? / R: Se eliminó el atributo `type="text/css"` (April 5, 2012), el carácter U+00A0 se reemplazó por whitespace (November 21, 2013) y se añadieron selectores CSS con namespace `.rails-default-error-page` (April 20, 2017). (El ejemplo que recorre el capítulo)

P: ¿A qué rango de versiones se acota la Rails del ejemplo y con qué comandos se obtienen las fechas? / R: Entre la 3.2.16 y la 4.2.8, clonando el repo (`git clone https://github.com/rails/rails`) y filtrando (`git log | grep 404`). (El ejemplo que recorre el capítulo)

P: ¿Qué hacer cuando varias bases de datos comparten el mismo método de generación de clave primaria? / R: Combinar el primary key scanning con otra técnica, como forzar mensajes de error de la DB. (Detecting Server-Side Frameworks / Database Detection)

P: ¿Qué revela típicamente la cabecera `X-Powered-By` y por qué sigue siendo útil? / R: Revela el nombre y versión del servidor; aunque los equipos prudentes la deshabilitan, millones de sitios aún la exponen. (Detecting Server-Side Frameworks / Header Detection)

## Puntos a dominar

- Distinguir código propio (in-house) de dependencias de terceros, y por qué estas se revisan menos y amplían la superficie de ataque.
- Explicar cómo fijar la versión de una dependencia habilita la reutilización de ataques desde bases de CVE (ReDoS, prototype pollution, XSS).
- Reconocer EmberJS, Angular, React y VueJS por sus globals, atributos del DOM y constantes de versión.
- Enumerar librerías JS y CSS externas con `querySelectorAll` sobre `script` y `link`.
- Identificar en servidor las cabeceras reveladoras (`X-Powered-By`, `Server`, `X-AspNet-Version`) y el riesgo de dejarlas habilitadas.
- Aplicar el fingerprinting de open source (página 404 e historial Git) para acotar versiones y ligarlas a CVE conocidos.
- Describir el primary key scanning y el formato `ObjectId` de 12 bytes de MongoDB.
