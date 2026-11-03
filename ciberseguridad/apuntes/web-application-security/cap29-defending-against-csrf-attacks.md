# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 29 — Defending Against CSRF Attacks (Defensa contra ataques CSRF)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo cierra el ciclo abierto en la Parte II, donde se construyeron ataques de Cross-Site Request Forgery (CSRF) que aprovechaban la sesión autenticada de un usuario para hacer peticiones en su nombre: mediante enlaces `<a></a>`, etiquetas `<img></img>` e incluso HTTP POST a través de formularios web. Estos ataques son peligrosos porque operan con privilegios elevados y suelen ser indetectables para el usuario autenticado.

La tesis es que no existe una única bala de plata: la defensa eficaz contra CSRF es por capas. Se combinan la verificación de cabeceras (referer y origin), los tokens anti-CSRF y buenas prácticas de diseño de código. El autor insiste en que cada técnica solo funciona bien si se aplica a toda la aplicación, porque "el eslabón más débil rompe la cadena".

Al terminar sales sabiendo cómo validar el origen de las peticiones, cómo funciona un token CSRF (incluida su variante stateless para APIs REST), por qué las peticiones HTTP GET nunca deben modificar estado del servidor, y cómo centralizar todas estas protecciones mediante middleware de petición.

## Verificación de cabeceras (Header Verification)
Como muchas peticiones CSRF se originan fuera de tu aplicación, puedes mitigar el riesgo comprobando el origen de la petición. Hay dos cabeceras HTTP relevantes, importantes porque no pueden modificarse programáticamente con JavaScript en los navegadores principales, lo que les da baja probabilidad de ser falsificadas:

- **Origin header**: se envía solo en peticiones HTTP POST. Indica dónde se originó la petición. Ejemplo: `Origin: https://www.mega-bank.com:80`.
- **Referer header**: se envía en todas las peticiones (HTTP o HTTPS) e indica también el origen. La única vez que no está presente es cuando el enlace de referencia tiene el atributo `rel=noreferer`. Ejemplo: `Referer: https://www.mega-bank.com:80`.

Ante un POST a tu servidor puedes verificar que estas cabeceras coinciden con tus orígenes de confianza:

```javascript
const validLocations = [
  'https://www.mega-bank.com',
  'https://api.mega-bank.com',
  'https://portal.mega-bank.com'
];

const validateHeadersAgainstCSRF = function(headers) {
  const origin = headers.origin;
  const referer = headers.referer;
  if (!origin || referer) { return false; }
  if (!validLocations.includes(origin) ||
      !validLocations.includes(referer)) {
        return false;
      }
  return true;
};
```

Siempre que sea posible, comprueba ambas cabeceras; si ninguna está presente, es seguro asumir que la petición no es estándar y debe rechazarse. Sin embargo hay un caso donde fallan: si un atacante consigue un XSS en uno de tus orígenes permitidos, puede lanzar el ataque desde tu propio origen y parecer legítimo. Esto es aún más preocupante si el sitio permite contenido generado por usuarios. Por eso la verificación de cabeceras es un punto de partida, no una solución completa.

## Tokens CSRF
La forma más potente de defensa es el token anti-CSRF (o simplemente token CSRF). La mayoría de los sitios grandes lo usan como defensa principal. Funciona así:

1. El servidor envía al cliente un token especial, generado criptográficamente con un algoritmo de muy baja colisión. Puede regenerarse por petición, pero normalmente se genera por sesión.
2. Cada petición reenvía el token (en formularios y en peticiones AJAX). El servidor verifica que esté vivo (no expirado), sea auténtico y no haya sido manipulado. Si falla, la petición se registra y también falla.
3. Como el token es único por sesión y por usuario, el atacante necesitaría un token vivo y actualizado y además tendría que apuntar a un usuario específico en lugar de a muchos. Con la expiración, el token puede estar muerto cuando el usuario hace clic en el enlace malicioso.

Antiguamente, antes del auge de REST, los servidores guardaban registro de los clientes conectados y gestionaban los tokens de forma stateful. En aplicaciones modernas la ausencia de estado (statelessness) suele ser un requisito de diseño de API y no conviene volver stateful solo por añadir tokens. Un token CSRF stateless debe componerse de:

- Un identificador único del usuario al que pertenece el token.
- Un timestamp (que sirve para la expiración).
- Un nonce criptográfico cuya clave solo existe en el servidor.

Esto da un token práctico que además consume menos recursos que la alternativa stateful, porque gestionar sesiones no escala bien.

## Buenas prácticas de código anti-CSRF
Varios métodos efectivos empiezan en la fase de código o diseño:

- Refactorizar hacia peticiones GET stateless.
- Implementar defensas CSRF a nivel de toda la aplicación.
- Introducir middleware de verificación de peticiones.

### Peticiones GET stateless
Como los ataques CSRF más comunes y fáciles de distribuir llegan vía HTTP GET, las peticiones GET no deben almacenar ni modificar ningún estado del servidor. Comparación:

```javascript
// GET — vulnerable: modifica estado en un GET
const user = function(req, res) {
  getUserById(req.query.id).then((user) => {
    if (req.query.updates) { user.update(req.updates); }
    return res.json(user);
  });
};
// GET — solo lectura
const getUser = function(req, res) {
  getUserById(req.query.id).then((user) => {
    return res.json(user);
  });
};
// POST — la actualización va por POST
const updateUser = function(req, res) { /* ... user.update ... */ };
```

La primera API puede explotarse con cualquier GET (enlace o imagen: `https://<url>/user?user=123&updates=email:hacker`). La segunda, al separar lectura (GET) de actualización (POST), no puede explotarse con enlaces, imágenes u otros CSRF basados en GET. La regla clave: las peticiones HTTP GET están en riesgo por defecto; evítalas para operaciones con estado.

## Mitigación CSRF a nivel de aplicación
Las técnicas solo son útiles aplicadas a toda la aplicación. El middleware —scripts que corren en cada petición antes de la lógica de cada ruta— permite implementarlas en todas las rutas del servidor:

```javascript
const validateHeaders = function(headers, method) {
  const origin = headers.origin;
  const referer = headers.referer;
  let isValid = false;
  if (method === 'POST') {
    isValid = validLocations.includes(referer) && validLocations.includes(origin);
  } else {
    isValid = validLocations.includes(referer);
  }
  return isValid;
};

const validateCSRFToken = function(token, user) {
  const text_token = crypto.decrypt(token);
  const user_id = text_token.split(':')[0];
  const date = text_token.split(':')[1];
  const nonce = text_token.split(':')[2];
  let validUser = false, validDate = false, validNonce = false;
  if (user_id === user.id) { validUser = true; }
  if (dateTime.lessThan(1, 'week', date)) { validDate = true; }
  if (crypto.validateNonce(user_id, date, nonce)) { validNonce = true; }
  return validUser && validDate && validNonce;
};
```

El middleware `CSRFShield` valida las cabeceras y luego el token CSRF; si cualquiera falla, registra la petición y devuelve un 401 antes de ejecutar más lógica, de lo contrario llama a `next()`. Como depende de que el cliente envíe el token en cada petición, conviene automatizarlo también en el cliente: por ejemplo, con el patrón proxy sobreescribiendo el comportamiento por defecto de `XMLHTTPRequest` para incluir siempre el token, o con una librería que envuelva `XMLHTTPRequest` e inyecte el token según el verbo HTTP.

## Ideas clave
- CSRF explota la sesión autenticada del usuario para hacer peticiones en su nombre; es peligroso por operar con privilegios elevados y ser indetectable.
- No hay solución única: defiende por capas (cabeceras + tokens + diseño de código) y aplícalas a toda la aplicación.
- Verifica `origin` (solo en POST) y `referer` (en todas las peticiones); no pueden falsificarse con JavaScript, pero fallan si hay un XSS en un origen permitido.
- El token anti-CSRF es la defensa más potente: único por sesión y usuario, criptográfico y con expiración.
- En APIs stateless, el token debe llevar identificador de usuario, timestamp y un nonce cuya clave solo existe en el servidor; escala mejor que la alternativa stateful.
- Las peticiones HTTP GET nunca deben modificar estado del servidor; separa lectura (GET) de modificación (POST).
- Centraliza las defensas con middleware que valide cabeceras y token antes de cualquier lógica de ruta, y automatiza el envío del token en el cliente.
