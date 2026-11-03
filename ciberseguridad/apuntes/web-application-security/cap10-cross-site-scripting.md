# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 10 — Cross-Site Scripting (Scripting entre sitios)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber

El capítulo explica el cross-site scripting (XSS), una de las vulnerabilidades más comunes de internet, surgida como respuesta al aumento de interacción del usuario en las aplicaciones web. En esencia, un ataque XSS se aprovecha de que las aplicaciones web ejecutan scripts en los navegadores de los usuarios: cualquier script creado dinámicamente que pueda ser contaminado o modificado por un usuario final pone en riesgo a la aplicación.

El texto categoriza XSS en tres grandes tipos reconocidos por comités como OWASP: stored (el código se almacena en una base de datos antes de ejecutarse), reflected (el código no se almacena, sino que el servidor lo refleja) y DOM-based (el código se almacena y ejecuta en el navegador). El autor recorre cada uno con un escenario de banco ficticio, y luego cubre variantes y técnicas avanzadas: mutation-based XSS (mXSS), técnicas de evasión de filtros, y el modelo de sinks y sources.

Sales sabiendo cómo se descubre y explota un XSS, por qué el stored es el más fácil de detectar pero afecta a más usuarios, por qué el reflected y el DOM-based evaden mejor la detección, cómo los payloads pueden burlar filtros, y qué APIs del navegador actúan como fuentes y sumideros de ejecución de script.

## El ejemplo que recorre el capítulo

El hilo conductor es el banco ficticio mega-bank.com. En el portal de soporte (support.mega-bank.com) el usuario escribe una queja y, al intentar poner texto en negrita, añade etiquetas `<strong></strong>` que la aplicación interpreta como DOM en lugar de texto. El fallo arquitectónico es aplicar literalmente el resultado de una petición HTTP al DOM, típicamente con `innerHTML`:

```javascript
const comment = 'my <strong>comment</strong>';
const div = document.createElement('div');
div.innerHTML = comment;
const wrapper = document.querySelector('#commentArea');
wrapper.appendChild(div);
```

Como el texto se añade literalmente al DOM, se interpreta como marcado en lugar de texto. A partir de este mismo banco se ilustran las tres variantes de XSS.

## Descubrimiento y explotación de XSS

El flujo del fallo es: el usuario envía un comentario por formulario → se almacena en base de datos → otros usuarios lo solicitan por HTTP → se inyecta en la página → el comentario inyectado se interpreta como DOM en lugar de texto (PDF p. 160-161).

Sustituyendo la negrita por un `<script>`, el payload puede recorrer el DOM con `document.querySelector()` para robar PII (nombre, email, teléfono) y exfiltrarla a un servidor del atacante vía `XMLHttpRequest`. Cuando una etiqueta script llega al DOM por JavaScript, el intérprete se invoca de inmediato y ejecuta el código sin interacción del usuario. El agente de soporte solo ve el texto literal; las etiquetas `<script>` y su contenido quedan ocultos ejecutándose en segundo plano.

Resumen de lo que pueden hacer los ataques XSS (PDF p. 163-164): ejecutar un script no escrito por el dueño de la app, correr sin visibilidad ni interacción, obtener cualquier dato presente en la app, enviar/recibir datos de un servidor malicioso, robar tokens de sesión (account takeover) y dibujar objetos DOM sobre la UI para phishing perfecto.

## Stored XSS

Es probablemente el tipo más común. Es el más fácil de detectar pero a menudo el más peligroso porque puede afectar a más usuarios: un objeto almacenado puede ser visto por muchos, y un objeto global infectado podría exponer a todos. El ejemplo del autor: un XSS almacenado en el título de un video destacado podría afectar a cada visitante.

Su naturaleza permanente facilita la detección: aunque el script se ejecuta en el cliente, se almacena como texto en el servidor y no se evalúa allí (salvo casos avanzados con servidores Node.js, donde se convierte en RCE). Escanear regularmente las entradas de la base de datos es una mitigación barata, pero no definitiva: los payloads avanzados pueden no estar en texto plano (base64, binario) o almacenarse en varias partes y concatenarse al usarse en el cliente.

El único requisito para que un XSS sea "stored" es que el payload se almacene en la base de datos de la aplicación; no necesita ser JavaScript válido ni que el cliente sea un navegador. Un simple regex para prohibir etiquetas script o una regla CSP que impida el script inline habría detenido el ataque del ejemplo.

## Reflected XSS

Opera igual que el stored pero no se almacena en base de datos: el servidor refleja el payload directamente de vuelta al cliente. En el ejemplo, la búsqueda del portal de soporte correlaciona el query param con el encabezado de resultados; al inyectar `<script>alert(test);</script>` en la URL `support.mega-bank.com/search?query=...` se dispara un modal de alerta.

Es mucho más difícil de detectar porque suele atacar a un usuario directamente y nunca se almacena. El atacante puede distribuir un enlace malicioso por email, anuncios web u otros medios, disfrazándolo como un enlace legítimo (por ejemplo, "Create a New Checking Account"). Regla general: el reflected XSS evade mejor la detección pero generalmente es más difícil de distribuir a muchos usuarios.

## DOM-Based XSS

Puede ser reflected o stored, pero usa sinks y sources del DOM del navegador para ejecutarse. La diferencia clave es que nunca requiere interacción con un servidor; por eso hay un movimiento para clasificarlo como subconjunto de una nueva categoría llamada client-side XSS.

Necesita un source (objeto DOM que almacena texto) y un sink (API DOM capaz de ejecutar un script almacenado como texto). Es casi imposible de detectar con análisis estático o escáneres, y se complica por las diferencias de implementación entre navegadores y versiones: un navegador de 2015 puede ser vulnerable y uno moderno no. JavaScript y el DOM se basan en specs abiertas (TC39 y WHATWG), pero cada navegador implementa distinto.

Ejemplo con el portal de inversiones: `window.location.hash` es la fuente y `document.write()` el sumidero.

```javascript
const hash = document.location.hash;
const funds = [];
const nMatches = findNumberOfMatches(funds, hash);
document.write(nMatches + ' matches found for ' + hash);
```

Con el enlace `investors.mega-bank.com/listing#<script>alert(document.cookie);</script>`, `document.write()` ejecuta el valor del hash como script. Si se pasara una cadena legítima no causaría problemas, por lo que puede pasar desapercibido mucho tiempo.

## Mutation-Based XSS (mXSS)

Clasificación emergente introducida en el paper de Mario Heiderich "mXSS Attacks: Attacking Well-Secured Web-Applications by Using innerHTML Mutations". Es posible contra todos los navegadores principales y se basa en entender cómo el navegador optimiza y renderiza nodos DOM. Ha burlado filtros robustos como DOMPurify, OWASP AntiSamy y Google Caja: funciona con payloads seguros para el filtro que luego mutan en payloads inseguros tras pasar la filtración.

En 2019 Masato Kinugawa encontró un mXSS en la librería Closure de Google (usada en Google Search), que empleaba DOMPurify en el cliente. El payload:

```html
<noscript><p title="</noscript><img src=x onerror=alert(1)>">
```

Técnicamente debería ser DOM-safe, por lo que DOMPurify lo dejó pasar, pero al cargarse en el DOM el navegador hizo optimizaciones que convirtieron el `img onerror` en válido. La causa es que DOMPurify usa un elemento raíz `<template>`, donde el scripting está deshabilitado: ahí `<noscript>` representa sus hijos, pero con scripting habilitado en el navegador real el `<p title="` se ignora y el `img onerror` se activa.

## Bypassing Filters (Evasión de filtros)

Pocos sitios usan sanitizadores de primera clase como DOMPurify de Cure53; el resto no filtra, filtra en casa o usa librerías poco probadas. Técnicas de evasión:

- Self-Closing HTML Tags: el navegador intenta cerrar etiquetas abiertas sin cierre. Muchos filtros evalúan pares de etiquetas, así que un script roto puede pasar y el navegador lo regenera:
  ```html
  <script>alert() // código real
  <script>alert()<script> // código "arreglado" por el navegador
  ```
- Protocol-Relative URLs (PRURLs): mecanismo legado soportado por todos los navegadores que deja al navegador elegir el protocolo. Quitar `http`/`https` y usar `//` burla filtros que ocurren antes de instanciar los nodos DOM:
  ```html
  <a href="https://evil-website.com">click</a> <!-- filtered -->
  <a href="//evil-website.com">click</a> <!-- not filtered -->
  ```
- Malformed Tags: los navegadores corrigen etiquetas mal formadas (comillas mal colocadas). Una etiqueta malformada puede pasar el filtro y ejecutarse tras la corrección del navegador, p. ej. `<IMG """><SCRIPT>alert("XSS")</SCRIPT>"\>`.
- Encoding Escapes: formatos válidos alternativos burlan el análisis estático. Unicode es ideal: en JavaScript se sustituyen caracteres Latin con `\u` + cuatro hex. Así `alert(1)` bloqueado se reescribe como `\u0061lert(1)` o `\u0061\u006c\u0065\u0072\u0074(1)`.
- Polyglot Payloads: payloads capaces de ejecutar script en muchos contextos distintos del navegador, ahorrando trabajo. El polyglot de 0xSobky (2018) ejecuta en más de una docena de contextos (atributos con comillas dobles/simples/sin comillas, comentarios HTML, etiquetas HTML, cadenas JS).

## XSS Sinks and Sources

Una vulnerabilidad XSS explotable tiene dos componentes: el sink (método del navegador capaz de ejecutar script) y el source (lugar que acepta un payload de texto que luego lee y ejecuta el sink). Hay docenas o cientos de sinks/sources poco usados, más probables de ser explotables y menos sujetos a filtración.

Ejemplos de sinks: `eval()`, `<script>`, `javascript://`, `document.write()`, `element.innerHTML`, `element.outerHTML`, `Function()`, `setTimeout()`, `setInterval()`, `document.location`.

Ejemplos de sources: `document.url`, `document.baseURI`, `window.location.search`, `window.location.hash`, `window.location.href`, `window.name`, `localStorage`, `sessionStorage`, `document.referrer`. Para encontrar más, el autor recomienda leer las specs oficiales de ECMAScript (TC39) y DOM (WHATWG).

## Ideas clave

- XSS explota que las apps ejecutan scripts en el navegador; se divide en stored, reflected y DOM-based (categorías de OWASP).
- Stored XSS: payload almacenado en base de datos; fácil de detectar (está server-side) pero puede afectar a muchos usuarios.
- Reflected XSS: el servidor refleja el payload sin almacenarlo; evade mejor la detección pero es más difícil de distribuir masivamente.
- DOM-based XSS no toca el servidor; requiere un source y un sink en el navegador, y depende de la implementación de cada navegador/versión.
- mXSS usa payloads seguros que mutan en inseguros tras la sanitización, burlando filtros como DOMPurify, OWASP AntiSamy y Google Caja.
- Los filtros se evaden con etiquetas autocerradas, PRURLs, etiquetas malformadas, escapes Unicode y polyglot payloads.
- Toda vulnerabilidad XSS explotable se compone de un sink (ejecuta) y un source (acepta el payload).
- El inyectar entrada no saneada en la UI es la causa raíz; mitigaciones citadas: regex contra etiquetas script, reglas CSP y sanitizadores como DOMPurify.
