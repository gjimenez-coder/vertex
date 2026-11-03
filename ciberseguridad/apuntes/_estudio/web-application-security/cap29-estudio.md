# Defending Against CSRF Attacks (Defensa contra ataques CSRF) — Estudio

## Tarjetas de repaso

P: ¿Qué explota un ataque CSRF y por qué es peligroso?
R: Explota la sesión autenticada del usuario para hacer peticiones en su nombre; es peligroso porque opera con privilegios elevados y suele ser indetectable para el usuario.

P: ¿Cuál es la tesis central del capítulo sobre la defensa contra CSRF?
R: No hay una única bala de plata: la defensa eficaz es por capas, combinando verificación de cabeceras, tokens anti-CSRF y buenas prácticas de diseño de código, aplicadas a toda la aplicación.

P: ¿Por qué las cabeceras origin y referer son útiles contra CSRF?
R: Porque no pueden modificarse programáticamente con JavaScript en los navegadores principales, lo que les da baja probabilidad de ser falsificadas.

P: ¿En qué se diferencian las cabeceras Origin y Referer según su envío?
R: Origin se envía solo en peticiones HTTP POST; Referer se envía en todas las peticiones (HTTP o HTTPS), salvo cuando el enlace tiene el atributo rel=noreferer.

P: ¿En qué caso falla la verificación de cabeceras?
R: Si un atacante logra un XSS en uno de los orígenes permitidos, puede lanzar el ataque desde tu propio origen y parecer legítimo; es más preocupante si el sitio permite contenido generado por usuarios.

P: ¿Qué es un token anti-CSRF y cómo se genera habitualmente?
R: Es la defensa más potente: un token generado criptográficamente con un algoritmo de muy baja colisión, único por usuario; puede regenerarse por petición, pero normalmente se genera por sesión.

P: ¿Qué verifica el servidor al recibir un token CSRF en cada petición?
R: Que esté vivo (no expirado), que sea auténtico y que no haya sido manipulado; si falla, la petición se registra y también falla.

P: ¿Por qué el token único por sesión y usuario dificulta el ataque?
R: El atacante necesitaría un token vivo y actualizado y apuntar a un usuario específico en lugar de a muchos; además la expiración puede dejar el token muerto cuando el usuario hace clic en el enlace malicioso.

P: ¿De qué debe componerse un token CSRF stateless?
R: De un identificador único del usuario, un timestamp (para la expiración) y un nonce criptográfico cuya clave solo existe en el servidor.

P: ¿Por qué se prefiere un token stateless en aplicaciones modernas?
R: Porque la ausencia de estado suele ser requisito de diseño de API, consume menos recursos y escala mejor, ya que gestionar sesiones stateful no escala bien.

P: ¿Qué regla se aplica a las peticiones HTTP GET para prevenir CSRF?
R: Las peticiones GET nunca deben almacenar ni modificar estado del servidor; están en riesgo por defecto, así que se evitan para operaciones con estado.

P: ¿Qué es el middleware de verificación de peticiones en este contexto?
R: Scripts que corren en cada petición antes de la lógica de cada ruta, permitiendo aplicar las defensas CSRF en todas las rutas del servidor.

P: ¿Qué hace el middleware CSRFShield ante una validación fallida?
R: Valida cabeceras y luego el token CSRF; si cualquiera falla, registra la petición y devuelve un 401 antes de ejecutar más lógica; si todo es válido, llama a next().

P: ¿Cómo se automatiza el envío del token CSRF en el cliente?
R: Con el patrón proxy sobreescribiendo el comportamiento por defecto de XMLHTTPRequest para incluir siempre el token, o con una librería que lo envuelva e inyecte el token según el verbo HTTP.

## Preguntas de autoevaluación

P: ¿Por qué el autor afirma que cada técnica solo funciona si se aplica a toda la aplicación?
R: Porque "el eslabón más débil rompe la cadena": una ruta sin protección deja expuesta a toda la aplicación. (Sección: Lo que necesitas saber)

P: Si una petición POST llega sin cabecera origin ni referer, ¿qué conviene hacer y por qué?
R: Rechazarla, porque si ninguna de las dos está presente es seguro asumir que la petición no es estándar. (Sección: Verificación de cabeceras)

P: ¿Por qué la verificación de cabeceras es un punto de partida y no una solución completa?
R: Porque falla cuando hay un XSS en un origen permitido, ya que el ataque parece provenir de un origen legítimo. (Sección: Verificación de cabeceras)

P: ¿Qué ventaja da la expiración del token frente a un enlace malicioso?
R: El token puede estar muerto cuando el usuario hace clic en el enlace, invalidando la petición. (Sección: Tokens CSRF)

P: ¿Por qué en APIs modernas no conviene volver stateful solo para añadir tokens?
R: Porque la ausencia de estado suele ser requisito de diseño de API y gestionar sesiones stateful no escala bien; el token stateless cumple la función consumiendo menos recursos. (Sección: Tokens CSRF)

P: ¿Cómo puede explotarse una API GET que modifica estado y cómo se corrige?
R: Puede explotarse con cualquier GET (un enlace o una imagen, como /user?user=123&updates=email:hacker); se corrige separando la lectura (GET) de la actualización (POST). (Sección: Peticiones GET stateless)

P: ¿Qué tres comprobaciones realiza validateCSRFToken sobre el token?
R: Que el user_id coincida con el usuario, que la fecha no exceda una semana (expiración) y que el nonce sea válido; devuelve verdadero solo si las tres pasan. (Sección: Mitigación CSRF a nivel de aplicación)

## Puntos a dominar

- Entender que la defensa contra CSRF es por capas (cabeceras + tokens + diseño de código) y debe cubrir toda la aplicación.
- Distinguir cuándo se envía cada cabecera: Origin solo en POST, Referer en todas las peticiones salvo con rel=noreferer.
- Reconocer la limitación de la verificación de cabeceras frente a un XSS en un origen permitido.
- Explicar cómo funciona un token anti-CSRF: único por sesión y usuario, criptográfico, con verificación de vigencia, autenticidad e integridad.
- Componer un token CSRF stateless: identificador de usuario, timestamp y nonce con clave solo en el servidor.
- Aplicar la regla de que las peticiones GET nunca deben modificar estado del servidor, separando lectura (GET) de modificación (POST).
- Centralizar las defensas con middleware que valide cabeceras y token antes de la lógica de ruta, y automatizar el envío del token en el cliente.
