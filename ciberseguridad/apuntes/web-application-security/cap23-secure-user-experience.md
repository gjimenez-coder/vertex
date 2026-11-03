# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 23 — Secure User Experience (Experiencia de usuario segura)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber
La interfaz de usuario (UI) es un componente de la seguridad web que a menudo se olvida. Es la forma estándar en que un usuario interactúa con una aplicación web; aunque existen alternativas (CLI, REST API, archivos XML o JSON), la mayoría de usuarios prefiere la UI. En la web, las UIs están limitadas a un conjunto reducido de tecnologías por el modelo de cómputo del navegador: típicamente HTML, CSS y JavaScript, a veces plug-ins o applets (p. ej. Java) pese a sus limitaciones de seguridad y rendimiento.

El capítulo no se centra en esas tecnologías, sino en el diseño, la experiencia y la usabilidad de la salida que producen y con la que interactúa el usuario final. La tesis: muchos fallos de seguridad nacen de decisiones de diseño de UX bienintencionadas, y una buena experiencia de usuario puede tanto introducir riesgos como mitigarlos.

Sales sabiendo cómo evitar information disclosures y enumeration mediante decisiones de diseño de UX, cómo equilibrar la información que se entrega al usuario frente al riesgo de seguridad, y cómo usar "light patterns" para guiar al usuario hacia un uso más seguro de la aplicación.

## Information Disclosures (divulgación de información)
Lo primero a decidir al diseñar una UI es cuánta información dar al usuario. La tensión central: el propósito principal de una UI es dar información —para el usuario, más información suele ser mejor— pero más información puede implicar más riesgo de seguridad. Hay trade-offs donde se degrada la experiencia a cambio de mejor seguridad.

Ejemplo: diseñadores de UX quieren mostrar mensajes de error detallados cuando falla el envío de un formulario. Opciones posibles, de menos a más seguras:

- Reflejar el mensaje y código de error del servidor directamente al usuario.
- Reflejar el mensaje y código del servidor, solo si está en un allowlist predefinido.
- Dar un mensaje genérico determinado en el código cliente, junto al código de error del servidor.
- Dar solo el código de error del servidor.
- No dar ni mensaje ni código de error.

Técnicamente la opción más segura es no dar ni mensaje ni código, pero probablemente no es la correcta por el coste en usabilidad. Aquí importa evaluar el trade-off: nunca se debe revelar información del código fuente que permita fingerprinting, pero la información sobre el estado del servidor puede ser valiosa.

Al divulgar estado del servidor, hay que filtrarlo y formatearlo para minimizar el riesgo. En lugar de reflejar el error crudo de la base de datos o el middleware, se crea un allowlist de fallos comunes en tono genérico y se devuelve la coincidencia más cercana. Ejemplo del libro:

```
"the user Jonathan Smith could not be queried because the address
905 N. Main St. provided does not match the current file."
```

Puede sustituirse por un mensaje genérico que no filtre la dirección:

```
"The user could not be queried due to an address mismatch."
```

Esto da más información que un simple "an error occurred" sin el riesgo de divulgación. Importante: los mensajes del servidor cambian con el tiempo al actualizar bases de datos y middleware; sin un allowlist robusto, una divulgación puede no ocurrir ahora pero sí más adelante.

Sobre códigos HTTP, la buena práctica suele ser usar un código genérico para dificultar el recon; se elige a menudo "400 - bad request" porque da menos datos que códigos más específicos. Con sentido del humor puede usarse "418 - I’m a teapot", un código sin uso real (broma del April Fools' de 1998, aún soportado), que al no tener uso oficial es poco probable que interfiera con herramientas de terceros. En APIs consumidas por varios clientes que esperan estado detallado, pueden ser preferibles códigos no genéricos, pero evaluando cada endpoint caso por caso para no filtrar estado explotable.

## Enumeration (enumeración)
Ocurre cuando múltiples consultas de estructura similar producen una divulgación, o cuando la suma o combinación de consultas permite deducir información a la que el cliente no debería acceder.

Ejemplo simple: si `GET /user/:id` permite buscar un usuario y `:id` es un entero iterable (1, 2, 3…), repitiendo peticiones con números sucesivos un atacante deduce el total de usuarios del sistema. Riesgo bajo, pero información no prevista para divulgar.

Ejemplo más severo (MegaBank):

1. Un atacante encuentra una interfaz de administración no destinada a estar expuesta a internet.
2. No puede romper la autenticación, así que busca un `username:password` válido.
3. Nota que algunos intentos devuelven "wrong password" y otros "user does not exist".
4. Recopila brechas de datos de otros sitios (foros de hobby, pequeños ecommerce) con usernames y emails.
5. Encuentra correos `@megabank.com` y prueba los usernames asociados en la API admin, armando una hoja de cálculo de los que devuelven "wrong password" (este es el paso de enumeración).
6. Con los usernames válidos confirmados, usa otras técnicas (brechas, ingeniería social, fuerza bruta, diccionarios) para hallar la contraseña.

¿Por qué importa si podría haber hecho fuerza bruta desde el inicio? Porque la fuerza bruta y los diccionarios carecen de precisión, son fácilmente detectables y a veces no son matemáticamente factibles. Explotando la enumeración, la complejidad baja drásticamente: ya no se busca la combinación `username:password`, sino solo una contraseña válida para un username conocido. Además, con riesgo de detección o rate limits, el atacante puede usar métodos dirigidos (spear phishing) que pasarían inadvertidos.

Mecanismo común para evitar enumeración: diseñar cumpliendo tres criterios:

- Entregar los errores de forma genérica para que múltiples llamadas no acumulen datos útiles. OWASP sugiere que todos los fallos de autenticación usen el mensaje genérico "authentication failed" en vez de indicar si falló el username, el password o la combinación.
- Evitar en cualquier estructura de datos o módulo accesible por el usuario patrones o secuencias fáciles de adivinar. Nombrar endpoints 1/2/3/4/5 es mala práctica; crear user IDs según la fecha de alta también.
- Aplicar rate limits en todo endpoint en riesgo de enumeración. El límite se fija mirando el número medio de peticiones de un usuario legítimo y situándolo en el límite superior del uso legítimo.

En conclusión, la enumeración se mitiga como la information disclosure: si se la ve como una forma de divulgación que ocurre al filtrar repetidamente bits de datos relativamente inofensivos, mitigarla resulta sencillo.

## Secure User Experience Best Practices (buenas prácticas de UX segura)
La capa de experiencia de usuario es un lugar ideal para educar y guiar a los usuarios hacia un uso seguro de la aplicación.

Un dark pattern (Wikipedia) es un patrón de diseño de UI que engaña al usuario para que invoque una funcionalidad que no pretendía, degradando a menudo su seguridad o privacidad. Su contracara, que el autor llama light pattern, es un patrón que guía suavemente al usuario a mejorar su seguridad y privacidad. Son útiles porque los usuarios suelen no entender lo suficiente la aplicación como para tomar las mejores decisiones de seguridad. La librería React usa light patterns en sus convenciones de nombres para alejar a los desarrolladores de funciones con riesgo de seguridad (Figura 23-1).

Un enlace a documentación junto a una configuración de seguridad no es un light pattern: es documentación, y solo un subconjunto de usuarios la lee entera. Los light patterns se reparten por la aplicación cada vez que se invoca una función con riesgo de seguridad o privacidad.

Ejemplo: una cartera de criptomonedas web que permite transferencias. Por defecto permite salidas de cualquier monto, pero muchas ofrecen configuraciones opt-in que limitan el blast radius de una cuenta comprometida. Permitir solo $1,000 de salida al día en una cartera con $100,000 implica que, incluso comprometida, el atacante tardaría cien días en vaciarla, dando tiempo al usuario a reaccionar.

¿Dónde colocar el light pattern? No en la página de ajustes donde se activa el control, sino en toda la funcionalidad donde se invoca el riesgo. En cada transacción saliente se avisa al usuario de que el ajuste no está activado y de que teclear un monto erróneo podría causar daños financieros irreversibles. Así no se le carga con pensar en un atacante, sino con un caso límite de pérdida por error propio —algo con lo que tiene familiaridad directa porque está enviando dinero. Esto convierte mejor que el escenario del atacante, cuya probabilidad el usuario no sabe medir.

Guiar suavemente al usuario cada vez que ejecuta una acción arriesgada crea una conexión entre acción y consecuencia, y eleva mucho la tasa de activación de mecanismos de seguridad frente a la documentación sola. Aun así, el "secure by default" sigue siendo un patrón superior; los light patterns se usan cuando el secure by default no es viable.

## Ideas clave
- El primer dilema de la UI es cuánta información entregar: más usabilidad puede significar más riesgo, y hay que evaluar el trade-off.
- Nunca reveles información del código fuente que permita fingerprinting; filtra el estado del servidor mediante un allowlist de mensajes genéricos.
- Usa códigos HTTP genéricos (p. ej. "400 - bad request") para dificultar el recon; afina por endpoint solo cuando el cliente necesite detalle.
- La enumeration es divulgación repetida de datos pequeños; evita IDs y endpoints predecibles y no reveles si falló el username o el password.
- OWASP recomienda el mensaje genérico "authentication failed" para todo fallo de autenticación.
- Aplica rate limits fijados en el límite superior del uso legítimo en endpoints enumerables.
- Los dark patterns engañan al usuario; los light patterns lo guían hacia mejores decisiones de seguridad y privacidad.
- Coloca los light patterns donde se invoca el riesgo (cada transacción), no en la página de ajustes; secure by default sigue siendo superior cuando es viable.
