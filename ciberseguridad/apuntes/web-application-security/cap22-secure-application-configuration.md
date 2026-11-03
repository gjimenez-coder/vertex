# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 22 — Secure Application Configuration (Configuración segura de la aplicación)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

Entregar una aplicación web segura no es solo escribir código seguro: también implica configurarla para aprovechar los mecanismos de seguridad incorporados en el navegador. Como el navegador sigue siendo el único medio de entrega de una aplicación web (sin importar el lenguaje o framework del backend), saber activar y configurar estas protecciones es clave para una buena postura de seguridad.

El capítulo recorre las principales tecnologías de seguridad implementadas por el navegador y cómo configurarlas correctamente: Content Security Policy (CSP), Cross-Origin Resource Sharing (CORS), cabeceras de seguridad (HSTS, COOP, CORP y otras), el endurecimiento de cookies, y técnicas de framing y sandboxing para ejecutar código de terceros.

Sales sabiendo cómo construir una CSP estricta (nonce o hash) que bloquea XSS, cómo CORS flexibiliza la Same Origin Policy sin romper la seguridad, qué cabeceras extra aportan seguridad barata, cómo proteger cookies con sus atributos, y qué opciones de aislamiento (iframe, web workers, subresource integrity, Shadow Realms) existen para código de terceros.

## Content Security Policy (CSP)

CSP es uno de los mecanismos principales del navegador contra los ataques más comunes del cliente. Bien implementada, puede prevenir XSS, data injection, phishing, framing y redirect attacks. Es posible correr un sitio sin ninguna CSP, pero entonces el navegador no aplica mitigación alguna.

Implementación: dos métodos. El más común es devolver la cabecera `Content-Security-Policy` en cada respuesta del servidor (las cabeceras `X-Content-Security-Policy` y `X-Webkit-CSP` están deprecadas). Alternativamente, un meta tag en el `<HEAD>` de cada página:

```html
<meta
  http-equiv="Content-Security-Policy"
  content="default-src 'self'; img-src data:" />
```

Estructura: una política CSP se compone de directivas separadas por punto y coma (`;`); tras cada directiva va una opción de configuración. Ejemplo: `script-src scripts.mega-bank.com` permite ejecutar solo scripts de ese origen; el resto lanza un error CSP en la consola. La especificación la mantiene el W3C.

Directivas importantes (seguridad):
- `default-src`: fallback para otras directivas; allow-list de orígenes de imágenes, scripts, CSS y otros recursos. Reduce significativamente el riesgo de XSS.
- `sandbox`: crea un sandbox al cargar la página que impide pop-ups, ejecución de scripts o interacción con plug-ins.
- `frame-ancestors`: define qué páginas pueden embeber la actual. Ponerla en `'none'` suele ser lo más seguro, pues previene clickjacking.
- `eval` e inline script: bloqueados por defecto al tener cualquier CSP (gran victoria, pues son vectores comunes de XSS). Pueden reactivarse con `'unsafe-inline'` y `'unsafe-eval'`.
- `report-uri`: define un endpoint donde se reportan los errores CSP para logging.

Sources y source lists: las directivas que terminan en `-src` reciben una source list (lista de orígenes separados por espacios más valores de configuración CSP):
- `*`: comodín; permite cualquier URL excepto `blob` y `file`.
- `'none'`: no permite cargar ninguna fuente; no puede combinarse con otras fuentes o la política falla.
- `data:`: permite cargar imágenes en base64.
- `https:`: permite cargas siempre que los recursos usen HTTPS.
- `'self'`: el origen actual de la página cargada.

Strict CSP: permite inline script de forma segura sin limitar funcionalidad. Dos métodos:
- Nonce-based: cada script inline lleva un atributo `nonce` generado en runtime; el navegador verifica que coincida antes de ejecutar.

```
Content-Security-Policy:
  script-src 'nonce-{RANDOM}' 'strict-dynamic';
```

```html
<script src="..." nonce="123">alert()</script>
```

- Hash-based: en lugar de nonces aleatorios usa hashes SHA-256 de cada script inline añadidos a la source list; antes de ejecutar, el script se hashea y se compara.

El nonce es ideal cuando cada página se renderiza en el servidor (nonces nuevos en cada carga). El hash es mejor para apps que se cachean (CDN), porque la tasa de colisión de SHA-256 es tan baja (≈1/43.000.000.000) que es extremadamente improbable crear un payload inline que hashee igual que un script no malicioso.

Política CSP segura de ejemplo (secure-by-default) con nonce para scripts, `frame-ancestors` bloqueado, HTTPS en imágenes permitiendo base64, reporting URI y `'self'` como fallback:

```
Content-Security-Policy
default-src: 'self';
script-src: 'self' 'nonce-jgoj23j2o3j2oij26jk2nkn26kjh23' 'strict-dynamic';
frame-ancestors: 'none';
img-src: data: https:;
report-uri: https://reporting.megabank.com
```

## Cross-Origin Resource Sharing (CORS)

A menudo se confunde con CSP. Mientras CSP elige qué scripts pueden ejecutarse, CORS puede bloquear scripts en una fase anterior, antes de que lleguen al contexto de ejecución JavaScript. `fetch` y `XMLHTTPRequest` respetan la Same Origin Policy (SOP): una app solo puede hacer llamadas de red dentro de su propio origen salvo lo definido en una política CORS. Sin SOP, código JS podría hacer operaciones privilegiadas contra otro sitio donde el usuario esté autenticado (ataque CSRF), porque el navegador adjunta cookies automáticamente.

Tipos de petición CORS (según la especificación de WHATWG): el método simple basta para las peticiones comunes; preflight se usa para peticiones inusuales o que cambian estado.

Simple CORS: puede ser POST, HEAD o GET cumpliendo condiciones. Solo cabeceras "CORS-safelisted" (`Accept`, `Accept-Language`, `Content-Language`, `Content-Type`); el `Content-Type` debe ser `application/x-www-form-urlencoded`, `multipart/form-data` o `text/plain`; sin funciones avanzadas (como event listeners en el objeto XMLHTTPRequest). El navegador adjunta `origin: <source-origin>` y el servidor responde 200 con `access-control-allow-origin: <source-origin>`. Si los orígenes no coinciden, la respuesta no vuelve al script y se lanza un error CORS.

Preflighted CORS: toda petición que no cumpla los criterios de simple. El navegador envía un preflight (HTTP Options) con `origin`, `access-control-request-method` y `access-control-request-headers`. Si falla algún check, no se pasa la respuesta al script. La idea de diseño es más seguridad: no entregar datos u operaciones al servidor antes de confirmar que ambos pueden comunicarse.

Implementación: la mayoría de servidores ofrecen middleware CORS; en JS de servidor, el módulo npm `cors`:

```js
const express = require('express');
const app = express();
const cors = require('cors');

const corsOptions = {
  origin: 'https://mega-bank.com'
};

app.get('/users/:id', cors(corsOptions), function (req, res, next) {
  res.sendStatus(200);
});

app.listen(443, function () {
  console.log('listening on port 443')
});
```

Aplica el principle of least privilege: concede el mínimo alcance de orígenes (allowlist solo los necesarios), no uses comodines (`*`) salvo que sea imprescindible.

## Headers (cabeceras de seguridad)

Más allá de CSP y CORS, varias cabeceras aportan seguridad con poco esfuerzo:

- Strict Transport Security (HSTS): indica al navegador que la página solo debe cargarse por HTTPS y que futuras peticiones HTTP se "upgradean". Preferible a los redirects 301, que requieren una petición HTTP inicial vulnerable a man-in-the-middle. Sintaxis: `Strict-Transport-Security: max-age=<expire-time>; includeSubDomains; preload`. Parámetros: `max-age` (segundos a recordar la config), `includeSubDomains` (aplica a subdominios), `preload` (opcional, fuera de la spec; Google mantiene una preload list que Chrome y Firefox consultan).
- Cross-Origin-Opener-Policy (COOP): modifica el reparto del "browsing context" (datos de página, iframes, pestaña). Valores: `unsafe-none` (por defecto), `same-origin-allow-popups`, `same-origin`. Ponerla en `same-origin` impide que nuevas pestañas/ventanas naveguen de vuelta al contexto que las abrió, evitando fugas de información.
- Cross-Origin-Resource-Policy (CORP): mitigación contra ataques side-channel de temporización tipo Spectre (2018, aún afecta CPUs Intel). Restringe desde dónde puede accederse un recurso. Valores: `same-origin` (más seguro), `same-site` (permite subdominios, menos seguro), `cross-origin` (menos seguro). Soportada por Firefox, Edge y Chrome; fuerza el aislamiento de memoria a un nivel más bajo que JavaScript.

Cabeceras con implicaciones de seguridad:
- `X-Content-Type-Options`: en `nosniff` evita que el navegador adivine tipos MIME (mime sniffing) y convierta ficheros no ejecutables en ejecutables.
- `Content-Type`: indica el tipo de contenido (p. ej. `text/html; charset=UTF-8`); su beneficio de seguridad es que el cliente interprete el contenido correctamente.

Cabeceras legacy y sus equivalentes modernos:
- `X-Frame-Options` → CSP `frame-ancestors`.
- `X-XSS-Protection` → eliminada; CSP bloquea los sinks de XSS comunes por defecto.
- `Expect-CT` → eliminada; todos los certificados TLS posteriores a mayo 2018 soportan certificate transparency por defecto.
- `Referrer-Policy` → los navegadores modernos ya no envían todo el referrer; en legacy se puede limitar con `Referrer-Policy: strict-origin-when-cross-origin`.
- `X-Powered-By` → revela servidor/versión (fingerprinting); desactívala en software legacy.
- `X-Download-Options` → solo Internet Explorer (deprecado), ya innecesaria.

## Cookies

La mayoría de apps siguen usando cookies como forma principal de autenticar al usuario por petición, por lo que conviene endurecer cómo las maneja el navegador. Se establecen con la cabecera `Set-Cookie`, con los datos como par `clave=valor` y atributos de configuración:

```
Set-Cookie: auth_token=abc123; Secure;
```

Atributos de seguridad más potentes:
- `Path`: restringe el envío de la cookie a peticiones cuyo path incluya el valor indicado.
- `Secure`: solo envía la cookie sobre HTTPS; para cualquier cookie con datos sensibles, evita man-in-the-middle.
- `Expires`: descarta la cookie tras la fecha indicada (HTTP-date).
- `HttpOnly`: impide que JavaScript lea la cookie; aunque un XSS comprometa el sitio, no podrá acceder a las cookies de sesión ni hacer llamadas privilegiadas.
- `SameSite`: valores `Lax`, `Strict` o `None`; previene CSRF al no enviar cookies en peticiones cross-site. Suele ponerse en `Strict`.

El atributo `Domain` no debería usarse salvo que sea imprescindible: cambia el modelo por defecto de `my-domain.com` a `*.my-domain.com`, enviando cookies a todos los subdominios, con riesgo de account takeover (ATO) si algún subdominio ejecuta scripts de usuario.

Testing de cookies: con HTTP proxies de interceptación (man-in-the-middle sobre dev/staging) como Burp Suite o el open source ZAP; si la app solo habla HTTP necesitarás un certificado TLS de pruebas y la clave de descifrado. También se pueden ver en las DevTools del navegador (en Chrome: F12 → pestaña Application → Cookies) o con `document.cookie` en la consola.

## Framing y Sandboxing

Para ejecutar código de terceros dentro de tu página (p. ej. customización profunda tipo MySpace o partnerships), lo prudente es aislarlo (sandbox). Opciones:

Traditional Iframe: crea un DOM y contexto JavaScript separados, sandboxed contra fugas al frame principal. Los iframe escapes son exploits P0 (Critical Risk) resueltos rápido por Google, Microsoft y Mozilla (la seguridad la financian ellos, no tu empresa). Desventajas: no encajan bien con la UI (DOM propio, duplicación de CSS/código), difíciles de escalar, comunicación con la ventana principal limitada a la API POSTMessage, y posible degradación de rendimiento con varios iframes. Ejemplo básico y versión más segura con `sandbox`:

```html
<iframe src="https://other-website.com"></iframe>
<iframe src="https://other-website.com" sandbox></iframe>
```

El atributo `sandbox` fuerza capas extra de aislamiento: trata el contenido como origen separado, bloquea envíos de formularios, bloquea ejecución de scripts, desactiva APIs, impide que los enlaces accedan a otros browsing contexts, impide plug-ins, impide ver el browsing context padre y desactiva autoplay. El iframe debería ser tu primera línea de defensa al sandboxear.

Web Workers: ofrecen menos aislamiento que un iframe pero más que ejecutar código de terceros en el mismo contexto. Son hilos aislados que ejecutan scripts same-origin sin poder tocar el DOM.

```js
if (window.Worker) {
 // create Web Worker and have it run code from code.js
 const myWorker = new Worker('code.js');
 // destroy Web Worker
 myWorker.terminate()
}
```

No acceden a variables del contexto principal salvo vía `postMessage` o `MessageChannel`. Pero sí pueden hacer peticiones HTTP in-domain y cross-origin con `XMLHTTPRequest`, lo que los hace menos seguros que un iframe de origen separado.

Subresource Integrity: no es aislamiento, sino verificación de que el código de un tercero no fue modificado. Se revisa el JS manualmente, se genera un hash SHA-256/384/512 en base64 y se carga con el atributo `integrity`:

```html
<script src="other-website.com/stuff.js"
        integrity="sha384-NmJhYmViMzNiMmU1NzllMDMyODdl"
        crossorigin="anonymous"></script>
```

Al cargar, el navegador compara el hash del recurso con el del atributo; si no coincide, considera el archivo modificado, lanza error y se niega a cargarlo.

Shadow Realms: característica próxima del lenguaje JavaScript que evita algunos problemas del aislamiento por iframe manteniendo el sandboxing. Crea un nuevo contexto de ejecución con sus propios objetos globales, intrinsics y built-ins. Puede probarse hoy con shims públicos.

```js
const shadowRealm = new ShadowRealm();

// imports code that executes within its own environment.
const doSomething = await shadowRealm.importValue('./file.js', 'redDoSomething');

// This call chains to the shadowRealm's redDoSomething
doSomething();
```

Es fácil de implementar, no interfiere con la UI, consume menos memoria y permite ejecución síncrona (código en el contexto principal que corre justo después del de Shadow Realm; imposible con iframe, cuya comunicación es asíncrona). Es una propuesta TC39 en stage 3/4 que se añadirá al lenguaje al pasar los tests Test262 en todos los navegadores.

## Ideas clave

- La seguridad de una app web es tan buena como su eslabón más débil, que a menudo es el navegador, el stack de red o una integración de terceros.
- CSP bloquea por defecto inline script y `eval`; una strict CSP con nonce (páginas renderizadas en servidor) o hash (apps cacheadas/CDN) permite inline script seguro contra XSS.
- `frame-ancestors: 'none'` previene clickjacking; es el reemplazo moderno de `X-Frame-Options`.
- CORS flexibiliza la Same Origin Policy; configúralo con least privilege (allowlist de orígenes concretos, evita `*`); usa preflight para peticiones que cambian estado.
- Cabeceras baratas y efectivas: HSTS (forzar HTTPS), COOP `same-origin` (evitar fugas de contexto), CORP (mitigar Spectre), `X-Content-Type-Options: nosniff`.
- Endurece cookies con `Secure`, `HttpOnly`, `SameSite=Strict` y `Path`; evita el atributo `Domain` por el riesgo de envío a subdominios y ATO.
- Para código de terceros, el iframe con atributo `sandbox` es la primera línea de defensa; web workers aíslan menos; subresource integrity verifica integridad; Shadow Realms es la opción emergente.
- Varias cabeceras legacy (`X-XSS-Protection`, `Expect-CT`, `X-Download-Options`) fueron eliminadas o integradas en CSP y el comportamiento por defecto del navegador.
