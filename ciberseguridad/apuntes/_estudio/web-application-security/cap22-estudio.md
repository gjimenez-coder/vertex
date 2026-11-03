# Secure Application Configuration (Configuración segura de la aplicación) — Estudio

## Tarjetas de repaso

P: ¿Qué ataques puede prevenir una CSP bien implementada?
R: XSS, data injection, phishing, framing y redirect attacks.

P: ¿Cuáles son los dos métodos para implementar una CSP?
R: Devolver la cabecera `Content-Security-Policy` en cada respuesta (más común) o un meta tag `http-equiv` en el `<HEAD>` de cada página.

P: ¿Cómo se estructura una política CSP?
R: Como directivas separadas por punto y coma (`;`); tras cada directiva va una opción de configuración, y las directivas `-src` reciben una source list.

P: ¿Qué hace la directiva `frame-ancestors` y qué valor es el más seguro?
R: Define qué páginas pueden embeber la actual; ponerla en `'none'` previene clickjacking y suele ser lo más seguro.

P: ¿Qué comportamiento aporta por defecto tener cualquier CSP respecto a inline script y eval?
R: Los bloquea por defecto (vectores comunes de XSS); se pueden reactivar con `'unsafe-inline'` y `'unsafe-eval'`.

P: ¿Cuándo conviene strict CSP con nonce y cuándo con hash?
R: Nonce cuando cada página se renderiza en el servidor (nonce nuevo por carga); hash (SHA-256) para apps cacheadas en CDN, por su bajísima tasa de colisión.

P: ¿Qué diferencia a CORS de CSP en el bloqueo de scripts?
R: CSP elige qué scripts se ejecutan; CORS puede bloquear scripts en una fase anterior, antes de llegar al contexto de ejecución JavaScript.

P: ¿Qué protege la Same Origin Policy respecto a `fetch` y `XMLHTTPRequest`?
R: Que una app solo haga llamadas de red dentro de su propio origen salvo lo definido por CORS, evitando operaciones privilegiadas contra otro sitio autenticado (CSRF).

P: ¿Qué diferencia una petición CORS simple de una preflighted?
R: La simple (POST, HEAD o GET con condiciones y cabeceras CORS-safelisted) basta para peticiones comunes; la preflighted envía un HTTP Options previo para peticiones inusuales o que cambian estado.

P: ¿Qué indica HSTS y por qué es preferible a un redirect 301?
R: Indica que la página solo debe cargarse por HTTPS y que las peticiones HTTP se upgradean; el 301 requiere una petición HTTP inicial vulnerable a man-in-the-middle.

P: ¿Qué ataque mitiga la cabecera Cross-Origin-Resource-Policy (CORP)?
R: Ataques side-channel de temporización tipo Spectre, restringiendo desde dónde puede accederse un recurso.

P: ¿Qué hace el atributo de cookie `HttpOnly`?
R: Impide que JavaScript lea la cookie; aunque un XSS comprometa el sitio, no podrá acceder a cookies de sesión ni hacer llamadas privilegiadas.

P: ¿Por qué se desaconseja el atributo `Domain` en cookies?
R: Cambia el modelo por defecto de `my-domain.com` a `*.my-domain.com`, enviando cookies a todos los subdominios, con riesgo de account takeover (ATO).

P: ¿Qué aporta el atributo `sandbox` en un iframe?
R: Trata el contenido como origen separado y bloquea scripts, envíos de formularios, APIs, plug-ins, acceso al contexto padre, enlaces a otros browsing contexts y autoplay.

P: ¿Qué es Subresource Integrity y cómo funciona?
R: No es aislamiento sino verificación de integridad: se carga el recurso con un hash (SHA-256/384/512 en base64) en el atributo `integrity` y el navegador se niega a cargarlo si no coincide.

## Preguntas de autoevaluación

P: ¿Por qué entregar una app web segura va más allá de escribir código seguro? (sección "Lo que necesitas saber")
R: Porque también implica configurar la app para aprovechar los mecanismos de seguridad del navegador, que es el único medio de entrega de la aplicación, sin importar el backend.

P: Explica por qué el método hash es más adecuado que el nonce para una app cacheada en CDN. (sección "Content Security Policy (CSP)")
R: Porque el contenido se cachea y no cambia por carga; la tasa de colisión de SHA-256 es tan baja (≈1/43.000.000.000) que es casi imposible crear un payload inline que hashee igual que un script legítimo.

P: ¿Cuál es la idea de diseño detrás del preflight de CORS? (sección "Cross-Origin Resource Sharing (CORS)")
R: Más seguridad: no entregar datos u operaciones al servidor antes de confirmar que ambos orígenes pueden comunicarse.

P: Aplica el principle of least privilege a la configuración de CORS. (sección "Cross-Origin Resource Sharing (CORS)")
R: Conceder el mínimo alcance de orígenes mediante una allowlist de los necesarios y no usar comodines (`*`) salvo que sea imprescindible.

P: Nombra tres cabeceras legacy y su equivalente o destino moderno. (sección "Headers (cabeceras de seguridad)")
R: `X-Frame-Options` → CSP `frame-ancestors`; `X-XSS-Protection` → eliminada (CSP bloquea sinks XSS por defecto); `Expect-CT` → eliminada (certificate transparency por defecto desde mayo 2018).

P: ¿Qué combinación de atributos endurece una cookie de sesión y por qué? (sección "Cookies")
R: `Secure` (solo HTTPS, evita MITM), `HttpOnly` (JS no la lee), `SameSite=Strict` (previene CSRF) y `Path` (restringe el envío); juntos reducen robo y uso indebido de la cookie.

P: Compara el aislamiento que ofrecen un iframe de origen separado y un web worker. (sección "Framing y Sandboxing")
R: El iframe crea DOM y contexto JS separados y sandboxed; el web worker aísla menos: no toca el DOM pero sí puede hacer peticiones HTTP in-domain y cross-origin con `XMLHTTPRequest`.

P: ¿Qué ventajas aportan las Shadow Realms frente al aislamiento por iframe? (sección "Framing y Sandboxing")
R: Son fáciles de implementar, no interfieren con la UI, consumen menos memoria y permiten ejecución síncrona, imposible con iframe (cuya comunicación es asíncrona).

## Checklist

- Devolver la cabecera `Content-Security-Policy` en cada respuesta y evitar las deprecadas `X-Content-Security-Policy` y `X-Webkit-CSP`.
- Construir una strict CSP: nonce para páginas renderizadas en servidor o hash SHA-256 para apps cacheadas en CDN.
- Poner `frame-ancestors: 'none'` para prevenir clickjacking.
- Configurar `report-uri` para loggear errores CSP.
- Aplicar CORS con least privilege: allowlist de orígenes concretos, sin comodín `*`, y usar preflight para peticiones que cambian estado.
- Activar HSTS (`max-age`, `includeSubDomains`, y `preload` si procede) en lugar de redirects 301.
- Añadir cabeceras baratas: COOP `same-origin`, CORP `same-origin`, `X-Content-Type-Options: nosniff` y `Content-Type` correcto.
- Desactivar `X-Powered-By` en software legacy para evitar fingerprinting.
- Endurecer cookies con `Secure`, `HttpOnly`, `SameSite=Strict` y `Path`; evitar el atributo `Domain`.
- Probar cookies con proxies de interceptación (Burp Suite, ZAP) o DevTools (Chrome: F12 → Application → Cookies / `document.cookie`).
- Para código de terceros, usar iframe con atributo `sandbox` como primera línea de defensa; valorar web workers para código same-origin.
- Verificar integridad de recursos de terceros con Subresource Integrity (atributo `integrity` + `crossorigin`).
