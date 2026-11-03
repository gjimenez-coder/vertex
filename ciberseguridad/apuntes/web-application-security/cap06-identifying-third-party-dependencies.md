# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 6 — Identifying Third-Party Dependencies (Identificando dependencias de terceros)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF (PDF p. N).

## Lo que necesitas saber
La mayoría de las aplicaciones web actuales combinan código propio (in-house) con código externo integrado por diversas técnicas. Esas dependencias de terceros pueden ser propietarias (bajo licencia) o gratuitas, a menudo provenientes de la comunidad OSS. Su uso no está libre de riesgo: con frecuencia no pasan por una revisión de seguridad tan rigurosa como el código propio.

La tesis del capítulo es que, durante el reconocimiento, las integraciones de terceros son un vector de ataque frecuente, y muchas veces no hace falta preparar un ataque: basta con copiar uno conocido de una base de datos de CVE (Common Vulnerabilities and Exposures). Por eso debes prestar atención tanto a la dependencia como al método de integración.

Sales sabiendo cómo detectar frameworks de cliente (SPA, librerías JS, librerías CSS), cómo inferir frameworks de servidor (cabeceras, mensajes de error y páginas 404 por defecto, fingerprinting), y cómo identificar la base de datos subyacente mediante el escaneo de claves primarias. Si consigues fijar la versión, a menudo encontrarás vulnerabilidades aplicables de ReDoS, prototype pollution y XSS, sobre todo en versiones antiguas sin actualizar.

## El ejemplo que recorre el capítulo
Ruby on Rails sirve de caso práctico de fingerprinting en servidor. Al ser open source con historial Git en GitHub, se pueden rastrear cambios en su página 404 por defecto (que contiene un cuadro con el texto "The page you were looking for doesn't exist", PDF p. 137) para acotar la versión:

- April 5, 2012 — se eliminó el atributo HTML5 `type="text/css"`.
- November 21, 2013 — el carácter U+00A0 se reemplazó por whitespace.
- April 20, 2017 — se añadieron selectores CSS con namespace (`.rails-default-error-page`).

Clonando el repo (`git clone https://github.com/rails/rails`) y filtrando (`git log | grep 404`) se obtienen esas fechas. Buscando qué marcas existen o faltan en la 404 bajo prueba y cruzando con el calendario de versiones de RubyGems, se concluye que la versión está entre la 3.2.16 y la 4.2.8. Justamente las versiones 3.2.x hasta 4.2.7 eran vulnerables a un XSS documentado como CVE-2016-6316, que permitía inyectar HTML (con script tags) en cualquier campo de base de datos leído por un Action View Tag helper.

## Detecting Client-Side Frameworks (detección en cliente)
Los desarrolladores suelen reutilizar frameworks de UI bien mantenidos: librerías SPA para manejar estado complejo, frameworks JS para parchear la funcionalidad de JavaScript entre navegadores (Lodash, JQuery) y frameworks CSS para la apariencia (Bootstrap, Bulma). Los tres tipos suelen ser fáciles de detectar, y fijar la versión abre la puerta a vulnerabilidades públicas.

### Frameworks SPA
Los mayores frameworks SPA a 2023 (sin orden particular): EmberJS (LinkedIn, Netflix), Angular (Google), React (Facebook) y VueJS (Adobe, GitLab). Cada uno tiene sintaxis y forma de gestionar el DOM propias. Cuando la versión esté disponible, anótala siempre.

- EmberJS: al arrancar define el global `Ember` y etiqueta los DOM elements con un `ember-id` (`id=ember1`, `id=ember2`…), envueltos en un padre `class="ember-application"` (normalmente el body).
```javascript
// 3.1.0
console.log(Ember.VERSION);
```
- Angular: versiones antiguas exponían el global `angular` (versión en `angular.version`). Angular 4.0+ eliminó ese global; puedes detectarlo comprobando si existe el global `ng`. Para la versión:
```javascript
// returns array of root elements
const elements = getAllAngularRootElements();
const version = elements[0].attributes['ng-version'];
// ng-version="6.1.2"
console.log(version);
```
- React: global `React`; versión por constante. Las script tags con `type="text/jsx"` son una señal inequívoca de React.
```javascript
const version = React.version;
// 0.13.3
console.log(version);
```
- VueJS: global `Vue` con constante de versión. Si no puedes inspeccionar elementos, probablemente la app ignora las dev tools; se puede reactivar:
```javascript
const version = Vue.version;
// 2.6.10
// Vue components can now be inspected
Vue.config.devtools = true;
```

### Librerías JavaScript
Hay demasiadas librerías helper para contarlas; algunas exponen globals (Underscore y Lodash usan `_`; JQuery usa `$`) y otras operan bajo el radar. Mejor que buscar globals concretos, conviene listar todos los scripts externos de la página:
```javascript
const getScripts = function() {
  const scripts = document.querySelectorAll('script');
  scripts.forEach((script) => {
    if (script.src) {
      console.log(`i: ${script.src}`);
    }
  });
};
```
La salida muestra fuentes como `https://code.jquery.com/jquery-3.4.1.min.js` o `https://js.stripe.com/v3/`.

### Librerías CSS
Con una variante del algoritmo anterior, filtrando elementos `<link>` con `rel="stylesheet"`:
```javascript
const getStyles = function() {
  const scripts = document.querySelectorAll('link');
  scripts.forEach((link) => {
    if (link.rel === 'stylesheet') {
      console.log(`i: ${link.getAttribute('href')}`);
    }
  });
};
```

## Detecting Server-Side Frameworks (detección en servidor)
Detectar lo que corre en el cliente es fácil (el código está en memoria vía el DOM); detectar lo del servidor es más difícil pero a menudo posible, ya que las dependencias dejan marcas en el tráfico HTTP o exponen endpoints. Conviene memorizar cómo detectar los paquetes más usados.

### Header Detection
Paquetes mal configurados exponen demasiados datos en cabeceras por defecto. El caso típico es `X-Powered-By`, que revela nombre y versión del servidor (habilitado por defecto en versiones antiguas de Microsoft IIS):
```
X-Powered-By: ASP.NET
Server: Microsoft-IIS/4.5
X-AspNet-Version: 4.0.25
```
Administradores y equipos de desarrollo prudentes deshabilitan estas cabeceras, pero millones de sitios aún las exponen.

### Default Error Messages y páginas 404
Los mensajes de error y páginas 404 por defecto siguen presentes hasta que el dueño los reemplaza, y pueden revelar el software del servidor y su versión (o rango). El caso de Ruby on Rails (ver sección del ejemplo) muestra cómo el fingerprinting por historial Git acota la versión y la conecta con un CVE. La técnica aplica a cualquier dependencia de terceros cuya versión se pueda determinar.

### Database Detection
La mayoría de apps usan una base de datos de servidor (MySQL, MongoDB). Si los mensajes de error de la DB llegan al cliente, se puede inferir el motor; si no, se usa primary key scanning. Casi todas las bases soportan una clave primaria generada automáticamente; si conoces el método de generación por defecto de las bases principales, puedes identificar el motor analizando suficientes peticiones.

Ejemplo con MongoDB (NoSQL): genera un campo `_id` con un string hexadecimal de longitud 12. Según su documentación, la clase es `ObjectId` y cada id tiene exactamente 12 bytes: 4 bytes de timestamp Unix, 5 bytes aleatorios y 3 bytes de contador con valor inicial aleatorio. Ejemplo: `507f1f77bcf86cd799439011`. Buscando strings de 12 bytes de aspecto similar en el tráfico HTTP:
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "username": "joe123",
  "email": "joe123@my-email.com",
  "role": "moderator",
  "biography": "..."
}
```
Si varias bases comparten el mismo método de generación (p. ej. enteros secuenciales), puede hacer falta combinarlo con otra técnica como forzar mensajes de error.

## Ideas clave
- Las apps modernas mezclan código propio y de terceros; estas dependencias suelen revisarse menos y son vector de ataque frecuente.
- Fijar la versión de una dependencia permite reutilizar ataques conocidos desde bases de CVE (ReDoS, prototype pollution, XSS).
- Los frameworks SPA (EmberJS, Angular, React, VueJS) se detectan por globals, atributos del DOM y constantes de versión.
- `querySelectorAll` sobre `script` y `link` permite enumerar rápidamente librerías JS y CSS externas.
- En servidor, cabeceras como `X-Powered-By`, `Server` y `X-AspNet-Version` filtran software y versión si no se deshabilitan.
- El fingerprinting de open source (Ruby on Rails vía su página 404 e historial Git) acota la versión y la liga a CVE conocidos (p. ej. CVE-2016-6316).
- El primary key scanning identifica la base de datos; MongoDB usa `ObjectId` de 12 bytes (4 timestamp + 5 aleatorios + 3 contador).
- Entender las integraciones de terceros es hoy una habilidad imprescindible tanto para atacar como para mitigar riesgo en el propio código.
