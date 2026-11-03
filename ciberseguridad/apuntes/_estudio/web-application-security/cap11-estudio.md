# Cross-Site Request Forgery (Falsificación de petición entre sitios) — Estudio

## Tarjetas de repaso

P: ¿Qué relación de confianza explota un ataque CSRF?
R: La confianza entre navegador, usuario y servidor: el navegador asume que las acciones hechas desde el dispositivo del usuario se realizan en nombre de ese usuario.

P: ¿Cuáles son las dos señas o identificadores principales de un CSRF?
R: La escalada de privilegios y que la cuenta que inicia la petición normalmente no sabe que ocurrió.

P: ¿Qué es el query parameter tampering?
R: La forma más básica de CSRF: manipular los parámetros de una petición GET mediante un hipervínculo malicioso.

P: ¿Por qué los endpoints GET son los más fáciles de atacar con CSRF?
R: Porque GET es la petición por defecto del navegador y muchas etiquetas HTML que aceptan una URL (vía `src`) hacen GET automáticamente al cargarse en el DOM.

P: ¿Qué etiquetas HTML pueden disparar un GET automático sin interacción del usuario?
R: `<img>`, `<video>` (vía `<source>`) e `<iframe>`; en general cualquier etiqueta con atributo `src`.

P: ¿Cómo se atacan endpoints POST con CSRF y qué requiere?
R: Con formularios HTML que usan inputs ocultos; requiere más trabajo e interacción obligatoria del usuario (enviar el formulario).

P: ¿Cómo puede un ataque CSRF por formulario alcanzar un servidor de una red interna?
R: El creador del formulario no tiene acceso a la red, pero un usuario con acceso emitirá la petición al enviar el formulario.

P: ¿Cómo se evaden las defensas que validan headers como `referrer` u `origin`?
R: Eliminando esos headers para que el servidor los lea como null/undefined; añadir `rel=noreferrer` a `<a>` y `<form>` hace que el navegador omita el header referrer.

P: ¿Qué es un ataque de token pool?
R: Aprovechar herramientas legacy que evalúan tokens en "pools" y no caso por caso: se genera un token CSRF legítimo desde la propia cuenta y se adjunta al ataque.

P: ¿Qué hace débil a un token anti-CSRF?
R: Que se genere de forma predecible (fechas, horas, usernames, enteros iterativos); por ejemplo valores como `1691434927` que resultan ser timestamps Unix forjables.

P: ¿Cómo se evade una validación de content type?
R: Enviando un tipo distinto al esperado (p. ej. `application/x-url-encoded` o `form-multipart` cuando se espera `application/json`); en formularios se cambia editando el atributo `enctype`.

P: ¿Cómo se evaden filtros CSRF basados en regex?
R: Con formas alternativas de escribir la URL: punto y coma en vez de `?`, slash hacia adelante o atrás, o símbolos relativos como `/../`.

P: ¿Qué son los Zero Interaction Forms?
R: Payloads (típicamente vía XSS) en los que un script emula la interacción del usuario con el formulario mediante la API del DOM y lo envía sin interacción.

P: Según el autor, ¿por qué no conviene usar headers HTTP como seguridad de primera línea?
R: Porque "HTTP headers are easily forged, bypassed, or altered" (PDF p. 190).

## Preguntas de autoevaluación

P: ¿Por qué el endpoint `/transfer` de MegaBank es vulnerable a CSRF?
R: Verifica autenticación y la presencia de `to_user` y `amount`, pero asume que la petición se hace legítimamente en nombre del usuario; al usar GET basta un hipervínculo fabricado para atacar a un usuario autenticado. (Sección: El ejemplo que recorre el capítulo / Query Parameter Tampering)

P: Describe el flujo típico de un ataque CSRF por manipulación de parámetros.
R: El hacker descubre que el servidor usa params GET para su lógica, fabrica una URL maliciosa apuntando al endpoint, y desarrolla una estrategia de distribución (dirigida o masiva). (Sección: Query Parameter Tampering)

P: ¿Qué diferencia hay entre una estrategia de distribución dirigida y una masiva?
R: La dirigida busca mayor probabilidad de que la víctima esté logueada y con fondos; la masiva busca alcanzar a muchos usuarios antes de ser detectada. (Sección: Query Parameter Tampering)

P: ¿Cómo se puede disfrazar un ataque CSRF contra un endpoint POST?
R: Añadiendo campos legítimos (p. ej. un formulario de login) junto a los inputs ocultos: el usuario ve un login, pero al enviarlo la petición va realmente contra MegaBank aprovechando su sesión activa. (Sección: CSRF Against POST Endpoints)

P: ¿Qué herramientas permiten falsificar peticiones del navegador al evadir defensas CSRF?
R: Burp, Zap o `curl`, que envían peticiones con headers, content type o body falsificados. (Sección: Bypassing CSRF Defenses)

P: ¿En qué casos son posibles los payloads AJAX como CSRF?
R: Cuando hay ejecución de script; es común en sitios que permiten personalización, y fuera de eso es raro sin una vulnerabilidad XSS presente. (Sección: Bypassing CSRF Defenses — AJAX Payloads)

P: ¿Por qué el usuario rara vez detecta un enlace CSRF malicioso?
R: Porque el texto visible del enlace no muestra el destino real; p. ej. `<a href="https://www.my-website.com?id=123">My Website</a>` solo muestra "My Website". (Sección: Query Parameter Tampering)

P: ¿Por qué el autor sugiere que los ataques CSRF seguirán siendo comunes?
R: Porque CSRF deriva del modelo de confianza de los estándares de navegadores (WHATWG), y hasta que estos cambien seguirán siendo fáciles de explotar. (Sección: Ideas clave)

## Checklist

- [ ] Identificar endpoints que ejecutan operaciones con efectos (transferencias, cambios de contraseña) mediante GET y tratarlos como vulnerables.
- [ ] Revisar cualquier etiqueta con atributo `src` (`<img>`, `<video>`, `<iframe>`) como posible disparador de GET automático.
- [ ] No depender de headers HTTP (`referrer`, `origin`) como medida de seguridad de primera línea, ya que se falsifican o eliminan fácilmente.
- [ ] Verificar que los tokens anti-CSRF se evalúen caso por caso y no en pools.
- [ ] Comprobar que los tokens anti-CSRF no sean predecibles (evitar timestamps, usernames o enteros iterativos).
- [ ] Validar estrictamente el content type esperado y no aceptar tipos alternativos.
- [ ] Al validar URLs, probar los bypasses de regex comunes (`;`, `\`, `/../`) para confirmar que el filtro resiste.
- [ ] Considerar el riesgo de que formularios CSRF alcancen servidores de redes internas a través de usuarios con acceso.
