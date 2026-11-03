# Secure User Experience (Experiencia de usuario segura) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre la UI y la seguridad? / R: La UI es un componente de seguridad a menudo olvidado; muchos fallos nacen de decisiones de UX bienintencionadas, y una buena experiencia puede tanto introducir riesgos como mitigarlos.

P: ¿A qué conjunto de tecnologías está limitada la UI web por el modelo de cómputo del navegador? / R: Típicamente HTML, CSS y JavaScript, y a veces plug-ins o applets (p. ej. Java), pese a sus limitaciones de seguridad y rendimiento.

P: ¿Cuál es la tensión central al decidir cuánta información dar en una UI? / R: El propósito de la UI es dar información (más suele ser mejor para el usuario), pero más información puede implicar más riesgo de seguridad; hay que evaluar el trade-off.

P: ¿Cuál es técnicamente la opción más segura ante un error de formulario y por qué no suele ser la correcta? / R: No dar ni mensaje ni código de error; no suele ser correcta por su coste en usabilidad.

P: ¿Cómo se debe filtrar el estado del servidor antes de mostrarlo? / R: Creando un allowlist de fallos comunes en tono genérico y devolviendo la coincidencia más cercana, en vez de reflejar el error crudo de la base de datos o el middleware.

P: ¿Por qué es importante mantener un allowlist robusto de mensajes de error? / R: Porque los mensajes del servidor cambian al actualizar bases de datos y middleware; sin un allowlist robusto, una divulgación puede no ocurrir ahora pero sí más adelante.

P: ¿Qué código HTTP genérico se suele elegir para dificultar el recon y por qué se menciona el "418 - I'm a teapot"? / R: Se suele elegir "400 - bad request" por dar menos datos; el "418 - I'm a teapot" (broma del April Fools' de 1998) no tiene uso oficial, así que es poco probable que interfiera con herramientas de terceros.

P: ¿Qué es la enumeration? / R: Ocurre cuando múltiples consultas de estructura similar producen una divulgación, o cuando la suma o combinación de consultas permite deducir información a la que el cliente no debería acceder.

P: ¿Por qué la enumeration facilita un ataque frente a la fuerza bruta directa? / R: Porque reduce drásticamente la complejidad: ya no se busca la combinación username:password, sino solo una contraseña válida para un username conocido, permitiendo métodos dirigidos (spear phishing) menos detectables.

P: ¿Qué tres criterios de diseño ayudan a evitar la enumeration? / R: Entregar errores de forma genérica, evitar patrones o secuencias fáciles de adivinar en datos o módulos accesibles por el usuario, y aplicar rate limits en todo endpoint en riesgo.

P: ¿Qué mensaje recomienda OWASP para los fallos de autenticación? / R: El mensaje genérico "authentication failed", en vez de indicar si falló el username, el password o la combinación.

P: ¿Cómo se fija un rate limit adecuado contra la enumeration? / R: Mirando el número medio de peticiones de un usuario legítimo y situando el límite en el límite superior del uso legítimo.

P: ¿Qué es un dark pattern y qué es un light pattern? / R: Un dark pattern es un diseño de UI que engaña al usuario para invocar una función no pretendida, degradando su seguridad o privacidad; un light pattern (término del autor) guía suavemente al usuario a mejorar su seguridad y privacidad.

P: ¿Por qué un enlace a documentación junto a un ajuste no es un light pattern? / R: Porque es documentación, y solo un subconjunto de usuarios la lee entera; los light patterns se reparten por la aplicación cada vez que se invoca una función con riesgo.

P: ¿Cuál es el patrón superior al light pattern y cuándo se usa este último? / R: El "secure by default" sigue siendo superior; los light patterns se usan cuando el secure by default no es viable.

## Preguntas de autoevaluación

P: Ordena de menos a más seguras las opciones para mostrar un error de formulario y explica el trade-off. / R: De menos a más seguras: reflejar mensaje y código del servidor; reflejarlos solo si están en un allowlist; mensaje genérico del cliente más código del servidor; solo el código del servidor; ni mensaje ni código. El trade-off es que mayor seguridad suele degradar la usabilidad. (Sección: Information Disclosures)

P: ¿Qué diferencia hay entre revelar información del código fuente y revelar estado del servidor? / R: Nunca se debe revelar información del código fuente que permita fingerprinting, pero la información sobre el estado del servidor puede ser valiosa si se filtra y formatea para minimizar el riesgo. (Sección: Information Disclosures)

P: En el ejemplo del banco (MegaBank), ¿cuál es exactamente el paso de enumeración? / R: Probar los usernames obtenidos de brechas en la API admin y armar una hoja de cálculo con aquellos que devuelven "wrong password" (frente a "user does not exist"), confirmando así usernames válidos. (Sección: Enumeration)

P: Da dos ejemplos de malas prácticas que facilitan la enumeration por patrones predecibles. / R: Nombrar endpoints como 1/2/3/4/5 y crear user IDs según la fecha de alta; también exponer `:id` como entero iterable que revela el total de usuarios. (Sección: Enumeration)

P: ¿Dónde debe colocarse un light pattern y por qué ahí y no en la página de ajustes? / R: En toda la funcionalidad donde se invoca el riesgo (p. ej. cada transacción saliente), no en la página de ajustes, para crear una conexión entre acción y consecuencia y elevar la tasa de activación de los mecanismos de seguridad. (Sección: Secure User Experience Best Practices)

P: En el ejemplo de la cartera de criptomonedas, ¿cómo reduce el riesgo un límite de salida diario y qué enfoque de aviso convierte mejor? / R: Limitar a $1,000 diarios en una cartera de $100,000 haría que un atacante tardara cien días en vaciarla, dando tiempo a reaccionar; convierte mejor avisar del caso límite de pérdida por error propio (teclear un monto erróneo) que del escenario del atacante, cuya probabilidad el usuario no sabe medir. (Sección: Secure User Experience Best Practices)

P: ¿Por qué un mensaje genérico pero informativo (p. ej. "address mismatch") es preferible a reflejar el error crudo o a "an error occurred"? / R: Porque da más información útil que un simple "an error occurred" sin el riesgo de divulgar datos como la dirección o detalles del código fuente que permitirían fingerprinting. (Sección: Information Disclosures)

## Puntos a dominar

- Explicar el trade-off entre cantidad de información en la UI y riesgo de seguridad, y las cinco opciones ordenadas para mostrar errores.
- Distinguir entre divulgar información del código fuente (nunca) y estado del servidor (filtrado mediante allowlist genérico).
- Justificar el uso de códigos HTTP genéricos ("400 - bad request", "418 - I'm a teapot") para dificultar el recon y cuándo afinar por endpoint.
- Definir la enumeration como divulgación repetida de datos pequeños y reconstruir el caso MegaBank identificando el paso de enumeración.
- Aplicar los tres criterios anti-enumeration: errores genéricos, ausencia de patrones predecibles y rate limits en el límite superior del uso legítimo.
- Recordar la recomendación de OWASP del mensaje "authentication failed" para todo fallo de autenticación.
- Diferenciar dark pattern y light pattern, ubicar el light pattern donde se invoca el riesgo y recordar que el secure by default sigue siendo superior.
