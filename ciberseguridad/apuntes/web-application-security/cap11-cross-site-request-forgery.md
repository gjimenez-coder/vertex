# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 11 — Cross-Site Request Forgery (Falsificación de petición entre sitios)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo trata sobre CSRF, un ataque que explota la relación de confianza entre el navegador, el usuario y el servidor. La idea central: a veces conocemos un endpoint que realiza una operación que deseamos, pero no tenemos acceso porque requiere privilegios (p. ej., una cuenta de admin). Con CSRF logramos que sea el usuario privilegiado quien ejecute la operación en nuestro nombre, sin usar un snippet de JavaScript propio.

CSRF se apoya en que el navegador confía demasiado en que las acciones hechas desde el dispositivo del usuario son en nombre de ese usuario. Al encontrar llamadas a API que dependen de esa confianza para garantizar seguridad, podemos crear enlaces y formularios que hacen que el usuario emita peticiones por su cuenta sin saberlo. Es uno de los ataques más sigilosos: las peticiones ocurren en segundo plano y la víctima no se entera.

Los dos identificadores principales de un CSRF son la escalada de privilegios y que la cuenta que inicia la petición normalmente no sabe que ocurrió. Sales sabiendo cómo construir payloads CSRF sobre endpoints GET y POST, cómo se distribuyen y cómo evadir defensas anti-CSRF débiles.

## El ejemplo que recorre el capítulo
El hilo conductor es el banco ficticio MegaBank. Se parte de un endpoint simple `/account` (ExpressJS) que refleja los query params, y luego se presenta un endpoint vulnerable `/transfer` que transfiere fondos. Ese endpoint verifica autenticación y la presencia de `to_user` y `amount`, pero asume que la petición se hace legítimamente en nombre del usuario. Al usar HTTP GET, basta con fabricar un hipervínculo apuntando a esa ruta para atacar a un usuario autenticado.

## Query Parameter Tampering (manipulación de parámetros)
La forma más básica de CSRF: manipular parámetros vía hipervínculo. La mayoría de enlaces web corresponden a peticiones HTTP GET. Anatomía de un GET:

```
GET /resource-url?key=value HTTP/1.1
Host: www.mega-bank.com
```

El inicio de los query params se marca con `?` y continúa hasta encontrar un espacio. El servidor enruta la petición al handler, que recibe los parámetros junto con información del usuario, tipo de navegador y formato esperado.

Ruta vulnerable de MegaBank que transfiere fondos mediante GET:

```javascript
app.get('/transfer', function(req, res) {
  if (!session.isAuthenticated) { return res.sendStatus(401); }
  if (!req.query.to_user) { return res.sendStatus(400); }
  if (!req.query.amount) { return res.sendStatus(400); }

  transferFunds(session.currentUser, req.query.to_user, req.query.amount, ...);
});
```

Como la lógica depende de params GET, un hipervínculo malicioso basta. El flujo típico del ataque:
1. El hacker descubre que el servidor usa params GET para su lógica (monto y destino de la transferencia).
2. Fabrica la URL: `<a href="https://www.mega-bank.com/transfer?to_user=<cuenta del hacker>&amount=10000">click me</a>`.
3. Desarrolla una estrategia de distribución: dirigida (mayor probabilidad de estar logueado y con fondos) o masiva (alcanzar a muchos antes de ser detectado).

Suelen distribuirse por email o redes sociales; incluso se han comprado campañas publicitarias para sembrar los enlaces. El usuario rara vez evalúa el destino del enlace: `<a href="https://www.my-website.com?id=123">My Website</a>` solo muestra "My Website".

## Alternate GET Payloads (payloads GET alternativos)
Como el GET es la petición por defecto del navegador, muchas etiquetas HTML que aceptan una URL hacen GET automáticamente al cargarse en el DOM. Esto hace que los GET sean los más fáciles de atacar.

Una imagen invisible fuerza el GET sin interacción del usuario:

```html
<img src="https://www.mega-bank.com/transfer?to_user=<hacker's account>&amount=10000" width="0" height="0" border="0">
```

La etiqueta `<video>` funciona igual:

```html
<video width="1280" height="720" controls>
  <source src="https://www.mega-bank.com/transfer?to_user=<hacker's account>&amount=10000" type="video/mp4">
</video>
```

Hay que vigilar cualquier etiqueta que solicite datos mediante un atributo `src`.

## CSRF Against POST Endpoints (CSRF contra endpoints POST)
Es posible atacar POST, PUT o DELETE, aunque requiere más trabajo e interacción obligatoria del usuario. Suele hacerse con formularios, uno de los pocos objetos HTML que inician un POST sin script, usando inputs ocultos:

```html
<form action="https://www.mega-bank.com/transfer" method="POST">
  <input type="hidden" name="to_user" value="hacker">
  <input type="hidden" name="amount" value="10000">
  <input type="submit" value="Submit">
</form>
```

Se puede disfrazar añadiendo campos legítimos (p. ej., un formulario de login) junto a los ocultos: el usuario ve un login, pero al enviarlo la petición va realmente contra MegaBank, aprovechando su sesión activa. Esta técnica también sirve para alcanzar servidores de una red interna: el creador del formulario no puede, pero un usuario con acceso a esa red sí emitirá la petición al enviarlo.

## Bypassing CSRF Defenses (evasión de defensas CSRF)
Según la aplicación, las defensas anti-CSRF pueden evadirse con poco esfuerzo. Cualquier petición del navegador puede falsificarse: herramientas como Burp, Zap o `curl` envían peticiones con headers, content type o body falsificados. No todos los validadores se evaden igual, así que conviene probar varias opciones y documentar el proceso.

Header Validation: las defensas que validan headers como `referrer` u `origin` pueden evadirse eliminando esos headers (el servidor lee null/undefined). Agregar `rel=noreferrer` a `<a>` y `<form>` hace que el navegador omita el header referrer.

```html
<a href="https://example.com/update_password?password=123" rel="noreferrer">click me to update password</a>
```

El autor advierte que no recomienda usar headers como medida de seguridad de primera línea: "HTTP headers are easily forged, bypassed, or altered" (PDF p. 190).

Token Pools: algunas herramientas legacy evalúan tokens en "pools" y no caso por caso. Es posible generar un token CSRF legítimo desde tu propia cuenta y adjuntarlo al ataque. Los tokens pueden extraerse de las herramientas de desarrollo y reenviarse, p. ej. con curl:

```
curl https://website.com/auth
  -H "anti-csrf-token": "12345abc"
```

Weak Tokens: tokens generados de forma predecible (fechas, horas, usernames, enteros iterativos) pueden forjarse. El ejemplo del libro: `1691434927`, `1691434928` resultan ser timestamps Unix (ms desde 00:00:00 UTC del 1 de enero de 1970); entendido el mecanismo, se forjan tokens aceptados por el validador.

Content Types: si el servidor espera `application/json`, enviar `application/x-url-encoded` o `form-multipart` puede saltarse la validación. En casos raros, otros tipos la evaden (p. ej. `application/zip`, `application/xml`, `application/pdf`, `text/csv`, `application/gzip`). El content type se declara como header, y en formularios como atributo `enctype`; editar `enctype` en las dev tools cambia el content type enviado.

Regex Filter Bypasses: si la validación usa regex, formas alternativas de escribir la URL la evaden: punto y coma en vez de `?` (`https://example.com;test=123`), slash hacia adelante o atrás (`https://example.com\test`), o símbolos relativos (`https://example.com/../test`). Muchos desarrolladores no diseñan su propia regex, así que conviene probar primero los regex comunes de los buscadores.

Iframe Payloads: el atributo `src` de un iframe carga automáticamente sin interacción. Solo funciona con endpoints HTTP GET.

```html
<iframe src="https://example.com/change_password?password=123"></iframe>
```

AJAX Payloads: si hay ejecución de script, se pueden hacer peticiones AJAX (XMLHttpRequest) como payload CSRF. Común en sitios que permiten personalización; fuera de eso es raro sin una vulnerabilidad XSS presente.

Zero Interaction Forms: con ejecución de script, un payload JavaScript (típicamente vía XSS) emula la interacción del usuario con el formulario mediante la API del DOM y lo envía sin interacción. Casi todas las interacciones del DOM se pueden invocar vía JavaScript donde la ejecución de script es posible.

## Ideas clave
- CSRF explota la confianza entre navegador, usuario y servidor: el navegador asume que las acciones del dispositivo son en nombre del usuario.
- Sus dos señas son la escalada de privilegios y que la víctima no sabe que la petición ocurrió.
- Los endpoints GET son los más fáciles de atacar: enlaces, `<img>`, `<video>` e `<iframe>` disparan GET automáticamente al cargarse en el DOM.
- Los endpoints POST se atacan con formularios e inputs ocultos, a veces disfrazados de formularios legítimos; también permiten alcanzar redes internas vía un usuario con acceso.
- Las defensas débiles se evaden: eliminación de headers, token pools, tokens predecibles (timestamps Unix), content types alternativos y bypasses de regex.
- Los headers HTTP no son buena medida de seguridad de primera línea porque se falsifican fácilmente.
- Con ejecución de script (típicamente XSS) se logran payloads AJAX y formularios de cero interacción.
- CSRF deriva del modelo de confianza de los estándares de navegadores (WHATWG); hasta que cambien, estos ataques seguirán siendo comunes y fáciles de explotar.
