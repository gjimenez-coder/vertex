# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 5 — API Analysis (Análisis de APIs)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El análisis de endpoints de API es la siguiente habilidad lógica en el toolkit de reconocimiento tras el descubrimiento de subdominios. Una aplicación puede usar varios dominios (x.domain, y.domain, z.domain) y cada uno puede exponer sus propios endpoints de API. El capítulo enseña a descubrir esos endpoints, identificar qué verbos HTTP aceptan, reconocer su mecanismo de autenticación y deducir la "forma" (shape) del payload que esperan.

La tesis central es que encontrar APIs es el segundo paso para entender la estructura de una aplicación web (después de los subdominios). Entender por qué una API está expuesta en la red permite ver cómo encaja en la aplicación y cuál es su propósito de negocio. Las técnicas son similares a las del descubrimiento de subdominios: fuerza bruta, ataques de diccionario, pero también análisis manual y lógico.

Sales sabiendo cómo identificar si una API es REST o SOAP, cómo enumerar verbos HTTP sobre un endpoint conocido (incluyendo un script en JavaScript), cómo reconocer esquemas de autenticación (HTTP Basic, Digest, OAuth) y cómo determinar la forma del payload, ya sea mediante archetipos comunes como OAuth 2.0 o mediante prueba y error en shapes específicos de la aplicación.

## El ejemplo que recorre el capítulo
El hilo conductor es `mega-bank.com` (y su subdominio `api.mega-bank.com`). Sobre él se ilustran peticiones REST a `/users/1234` y `/users/1234/payments`, la enumeración de verbos HTTP, el login con HTTP Basic Auth y los intentos de deducir el shape de endpoints como `/users/config`.

## Endpoint Discovery (Descubrimiento de endpoints)
Las APIs empresariales suelen seguir un esquema REST o SOAP; REST es cada vez más popular y se considera la estructura ideal para APIs web modernas. Usando las developer tools del navegador y analizando las peticiones de red, si se ven peticiones como estas puede asumirse que es una API REST:

```
GET api.mega-bank.com/users/1234
GET api.mega-bank.com/users/1234/payments
POST api.mega-bank.com/users/1234/payments
```

Cada endpoint apunta a un recurso y no a una función; el recurso anidado `payments` pertenece al usuario 1234, lo que indica una API jerárquica, otra señal de diseño RESTful. En las cabeceras, un token enviado en cada petición también es señal de REST, porque "REST APIs are supposed to be stateless" (PDF p. 121): el servidor no debe rastrear a quien hace la petición.

La arquitectura REST soporta estos verbos HTTP (Tabla 5-1):

| Verbo HTTP REST | Uso |
|---|---|
| POST | Create |
| GET | Read |
| PUT | Update/replace |
| PATCH | Update/modify |
| DELETE | Delete |

La especificación HTTP define el método `OPTIONS`, que da información sobre los verbos de una API y debería ser el primer intento en recon:

```
curl -i -X OPTIONS https://api.mega-bank.com/users/1234
```

Una respuesta exitosa muestra algo como `200 OK` con `Allow: HEAD, GET, PUT, DELETE, OPTIONS`. Sin embargo, OPTIONS normalmente solo está disponible en APIs de uso público; muy pocas aplicaciones empresariales lo exponen, así que hace falta una solución más robusta.

El método más probable: partir de un endpoint que ya acepta al menos un verbo (p. ej. `GET api.mega-bank.com/users/1234`) y probar los demás verbos (POST, PUT, PATCH, DELETE) con un script.

> WARNING: forzar verbos HTTP puede borrar o alterar datos; hay que tener permiso explícito del dueño de la aplicación antes de hacer fuerza bruta contra una API.

El script `discoverHTTPVerbs(url)` prueba cada verbo con `XMLHttpRequest` y promesas; registra el `status` devuelto. No importa qué código de estado sea, solo que haya uno. Como la mayoría de servidores no responden a peticiones que no mapean a un endpoint válido, se devuelve `-1` si no hay respuesta en 1 segundo (1.000 ms, ajustable). Al resolverse todas las promesas, el log indica qué verbos tienen endpoint asociado.

## Authentication Mechanisms (Mecanismos de autenticación)
Adivinar el shape del payload es más difícil que afirmar que un endpoint existe. Lo más fácil es analizar la estructura de peticiones conocidas enviadas por el navegador; más allá de eso hay que hacer suposiciones informadas y probarlas manualmente. Conviene empezar por endpoints comunes a casi toda aplicación: sign in, sign up, password reset, que suelen tener payloads similares por basarse en esquemas estandarizados.

Reconocer el esquema de autenticación es clave porque muchas apps envían tokens en cada petición; si se entiende cómo se adjunta el token, es más fácil analizar otros endpoints que dependen de un usuario autenticado. Esquemas principales (Tabla 5-2):

- HTTP Basic Auth: usuario y contraseña en cada petición. Soporte nativo en todos los navegadores; pero la sesión no expira y es fácil de interceptar.
- HTTP Digest Authentication: `username:realm:password` hasheado en cada petición. Más difícil de interceptar y el servidor puede rechazar tokens expirados; la fuerza depende del algoritmo de hashing.
- OAuth: autenticación basada en token "Bearer", permite sign in con otros sitios (p. ej. Amazon → Twitch). Los permisos tokenizados se comparten entre apps; riesgos: phishing y que comprometer el sitio central comprometa todas las apps conectadas.

Ejemplo de login en `mega-bank.com`: la cabecera `Authorization: Basic am9lOjEyMzQ=` indica HTTP Basic Auth. La cadena es un `username:password` en base64. En la consola del navegador se usan `btoa(str)` y `atob(base64)` para codificar/decodificar:

```
/*
 * Decodes a string that was previously encoded with base64.
 * Result = joe:1234
 */
atob('am9lOjEyMzQ=');
```

Por su inseguridad, basic authentication solo se usa en aplicaciones que fuerzan cifrado SSL/TLS, para que las credenciales no se intercepten en el aire. Lección práctica: si un endpoint no devuelve nada interesante con payload vacío, lo primero es adjuntar una cabecera de autorización y ver si cambia el comportamiento como usuario autenticado.

## Endpoint Shapes (Formas de los endpoints)
Tras localizar subdominios y sus APIs, hay que determinar los verbos HTTP por recurso y añadirlo al mapa de la aplicación. Luego surge la pregunta de qué payload espera cada API.

### Common Shapes (Formas comunes)
Muchas APIs esperan shapes comunes en la industria. Un endpoint de autorización OAuth 2.0 puede esperar:

```
{
  "response_type": code,
  "client_id": id,
  "scope": [scopes],
  "state": state,
  "redirect_uri": uri
}
```

Como OAuth 2.0 es una especificación pública ampliamente implementada, se puede deducir con suposiciones informadas más la documentación pública. Las convenciones y los scopes varían algo entre implementaciones, pero el shape general no. La documentación de Discord y la de Facebook muestran endpoints OAuth 2.0 con parámetros `response_type`, `client_id`, `scope`, `state` y `redirect_uri`, todos parte del spec oficial. Aviso: aunque muchas APIs implementan specs comunes como OAuth, suelen no usar un spec común para sus APIs internas que ejecutan la lógica de negocio.

### Application-Specific Shapes (Formas específicas de la aplicación)
Son mucho más difíciles de determinar; requieren varias técnicas de recon y aprendizaje por prueba y error. Las aplicaciones inseguras dan pistas en mensajes de error HTTP. Por ejemplo, un `POST /users/config` puede devolver `401 not authorized` o `400 internal error`; un mensaje como `auth_token not supplied` revela un parámetro faltante, y con el `auth_token` correcto podría aparecer `publicProfile only accepts "auth" and "noAuth" as params`. Las aplicaciones más seguras solo lanzan errores genéricos.

Con una cuenta privilegiada, se puede ejecutar la misma petición contra tu propia cuenta usando la UI antes de intentarla contra otra, observando el shape saliente en Developer tools → Network o con una herramienta como Burp. Si se conoce el nombre de una variable pero no su valor, se puede intentar fuerza bruta con un script. Cuantas más reglas se conozcan del valor esperado (longitud fija de 12 caracteres, formato hexadecimal, etc.), mejor.

El conjunto de combinaciones posibles de un campo es el "solutions space"; el objetivo es reducirlo al espacio de búsqueda viable más pequeño. Buscar soluciones inválidas también puede ayudar a reducir el espacio e incluso descubrir bugs en el código.

## Summary (Resumen)
Tras un modelo mental (idealmente documentado) de los subdominios, el siguiente paso es encontrar los endpoints de API alojados en ellos para determinar su propósito. Es crucial porque, sin él, se puede perder tiempo buscando fallos en endpoints bien protegidos cuando existen otros menos seguros con funcionalidad o datos similares. Después, determinar el shape de los payloads mediante suposiciones informadas, automatización y análisis de archetipos comunes revela los datos que los endpoints esperan y devuelven, lo que da entendimiento de la función de la aplicación: primer gran paso para romperla o asegurarla.

## Ideas clave
- Tras descubrir subdominios, el análisis de endpoints de API es el siguiente paso de recon; cada dominio puede exponer APIs propias.
- Peticiones orientadas a recursos y jerárquicas, con token en cada petición, indican una API REST (stateless).
- REST soporta POST (create), GET (read), PUT (update/replace), PATCH (update/modify) y DELETE (delete).
- `OPTIONS` revela verbos permitidos pero casi solo en APIs públicas; lo normal es enumerar verbos sobre un endpoint ya conocido, siempre con permiso por el riesgo de alterar datos.
- Esquemas de autenticación principales: HTTP Basic Auth, HTTP Digest Authentication y OAuth; `Authorization: Basic ...` es base64 de `username:password`, decodificable con `atob()`.
- Si un endpoint no responde con payload vacío, probar adjuntando la cabecera de autorización.
- Shapes comunes (OAuth 2.0) se deducen con documentación pública; shapes específicos requieren prueba y error, pistas en errores HTTP y fuerza bruta guiada.
- Reducir el "solutions space" al mínimo viable y buscar también soluciones inválidas acelera el descubrimiento del shape.
