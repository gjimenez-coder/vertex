# API Analysis (Análisis de APIs) — Estudio

## Tarjetas de repaso

P: ¿Cuál es el siguiente paso de recon tras el descubrimiento de subdominios?
R: El análisis de endpoints de API, porque cada dominio (x.domain, y.domain, z.domain) puede exponer sus propias APIs.

P: ¿Qué señales indican que una API es REST?
R: Peticiones orientadas a recursos (no a funciones), estructura jerárquica/anidada (p. ej. `/users/1234/payments`) y un token enviado en cada petición, porque las REST APIs son stateless.

P: ¿Por qué un token en cada petición es señal de REST?
R: Porque las REST APIs deben ser stateless: el servidor no rastrea a quien hace la petición, así que la autenticación viaja en cada una.

P: ¿Qué verbos HTTP soporta la arquitectura REST y para qué?
R: POST (create), GET (read), PUT (update/replace), PATCH (update/modify) y DELETE (delete).

P: ¿Qué hace el método OPTIONS y cuál es su limitación en recon?
R: Informa de los verbos permitidos por una API (p. ej. `Allow: HEAD, GET, PUT, DELETE, OPTIONS`); debería ser el primer intento, pero casi solo está disponible en APIs de uso público, no en aplicaciones empresariales.

P: Si OPTIONS no está disponible, ¿cómo se enumeran los verbos de un endpoint?
R: Partiendo de un endpoint que ya acepta al menos un verbo (p. ej. `GET /users/1234`) y probando los demás (POST, PUT, PATCH, DELETE) con un script, siempre con permiso del dueño.

P: ¿Qué hace el script discoverHTTPVerbs(url)?
R: Prueba cada verbo con XMLHttpRequest y promesas, registra el status devuelto; si no hay respuesta en 1 segundo (1.000 ms, ajustable) devuelve -1, porque solo importa que exista un código de estado.

P: ¿Qué caracteriza a HTTP Basic Auth?
R: Envía usuario y contraseña en cada petición con soporte nativo en todos los navegadores; la sesión no expira y es fácil de interceptar, por lo que solo se usa con cifrado SSL/TLS.

P: ¿Qué caracteriza a HTTP Digest Authentication?
R: Envía `username:realm:password` hasheado en cada petición; es más difícil de interceptar, el servidor puede rechazar tokens expirados y su fuerza depende del algoritmo de hashing.

P: ¿Qué caracteriza a OAuth y qué riesgos tiene?
R: Autenticación basada en token "Bearer" que permite sign in con otros sitios (p. ej. Amazon → Twitch) compartiendo permisos tokenizados; riesgos: phishing y que comprometer el sitio central comprometa todas las apps conectadas.

P: ¿Qué significa la cabecera `Authorization: Basic am9lOjEyMzQ=` y cómo se decodifica?
R: Indica HTTP Basic Auth; la cadena es un `username:password` en base64 (aquí `joe:1234`), decodificable en la consola del navegador con `atob(base64)` y codificable con `btoa(str)`.

P: ¿Qué diferencia a los "common shapes" de los "application-specific shapes"?
R: Los comunes siguen specs públicos ampliamente implementados (p. ej. OAuth 2.0) y se deducen con documentación pública; los específicos de la aplicación requieren prueba y error, pistas en errores HTTP y fuerza bruta guiada.

P: ¿Qué parámetros espera un endpoint de autorización OAuth 2.0?
R: `response_type`, `client_id`, `scope`, `state` y `redirect_uri`, todos parte del spec oficial (como muestran las documentaciones de Discord y Facebook).

P: ¿Qué es el "solutions space" y cuál es el objetivo al analizar un shape?
R: Es el conjunto de combinaciones posibles de un campo; el objetivo es reducirlo al espacio de búsqueda viable más pequeño, y buscar soluciones inválidas también ayuda a reducirlo e incluso a descubrir bugs.

## Preguntas de autoevaluación

P: ¿Por qué es crucial encontrar los endpoints de API antes de buscar fallos?
R: Porque sin ese mapa se puede perder tiempo buscando fallos en endpoints bien protegidos cuando existen otros menos seguros con funcionalidad o datos similares. (Sección: Summary)

P: ¿Cómo se identifica si una API es REST a partir del tráfico del navegador?
R: Analizando las peticiones de red en las developer tools: peticiones a recursos, recursos anidados jerárquicos y un token en cada petición apuntan a REST stateless. (Sección: Endpoint Discovery)

P: ¿Por qué hace falta permiso explícito antes de forzar verbos HTTP contra una API?
R: Porque forzar verbos como POST, PUT o DELETE puede borrar o alterar datos de la aplicación. (Sección: Endpoint Discovery, WARNING)

P: ¿Por qué conviene empezar el análisis de payloads por endpoints de sign in, sign up o password reset?
R: Porque son comunes a casi toda aplicación y suelen tener payloads similares al basarse en esquemas estandarizados, lo que facilita adivinar su shape. (Sección: Authentication Mechanisms)

P: ¿Qué se debe probar si un endpoint no devuelve nada interesante con un payload vacío?
R: Adjuntar una cabecera de autorización y observar si el comportamiento cambia como usuario autenticado. (Sección: Authentication Mechanisms)

P: ¿Cómo revelan las aplicaciones inseguras el shape específico de un endpoint?
R: Mediante mensajes de error HTTP que exponen parámetros faltantes o valores aceptados (p. ej. `auth_token not supplied` o `publicProfile only accepts "auth" and "noAuth" as params`); las aplicaciones seguras solo lanzan errores genéricos. (Sección: Endpoint Shapes — Application-Specific Shapes)

P: ¿Cómo ayuda una cuenta privilegiada a deducir un shape específico de la aplicación?
R: Permite ejecutar la misma petición contra tu propia cuenta desde la UI y observar el shape saliente en Developer tools → Network o con Burp antes de intentarla contra otra cuenta. (Sección: Endpoint Shapes — Application-Specific Shapes)

P: ¿Por qué el shape de OAuth 2.0 se puede deducir con suposiciones informadas?
R: Porque OAuth 2.0 es una especificación pública ampliamente implementada; aunque convenciones y scopes varían algo, el shape general no cambia y hay documentación pública. (Sección: Endpoint Shapes — Common Shapes)

## Puntos a dominar

- Situar el análisis de APIs como el paso de recon posterior al descubrimiento de subdominios y entender que cada dominio puede exponer APIs propias.
- Reconocer una API REST por sus peticiones a recursos, jerarquía anidada, naturaleza stateless y token por petición.
- Recordar los cinco verbos REST y su propósito: POST (create), GET (read), PUT (update/replace), PATCH (update/modify), DELETE (delete).
- Saber que OPTIONS es el primer intento pero casi solo funciona en APIs públicas; en caso contrario, enumerar verbos sobre un endpoint conocido, siempre con permiso por el riesgo de alterar datos.
- Distinguir HTTP Basic Auth, HTTP Digest Authentication y OAuth, sus mecanismos y sus riesgos.
- Decodificar `Authorization: Basic ...` como base64 de `username:password` con `atob()` y codificar con `btoa()`.
- Diferenciar common shapes (deducibles con specs públicos como OAuth 2.0) de application-specific shapes (prueba y error, pistas en errores HTTP, fuerza bruta guiada).
- Comprender el concepto de "solutions space" y la estrategia de reducirlo al mínimo viable, incluyendo la búsqueda de soluciones inválidas.
