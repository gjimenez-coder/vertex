# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 21 — Secure Application Architecture (Arquitectura de aplicaciones segura)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
El capítulo defiende que el primer paso para asegurar cualquier aplicación web es la fase de arquitectura. Igual que un arquitecto de edificios, el arquitecto de software diseña módulos a alto nivel, decide cómo se comunican, cómo se almacenan los datos, qué dependencias de terceros usar y qué paradigma de programación predomina. Es un proceso delicado y de alto riesgo, porque re-arquitecturar o refactorizar es caro una vez construida la aplicación.

La tesis central es económica además de técnica: según la NIST, "The cost of removing an application security vulnerability during the design phase ranges from 30–60 times less than if removed during production" (PDF p. 292). Muchas vulnerabilidades se evitan fácilmente con planificación cuidadosa en la fase de diseño; con poca planificación, el código debe rehacerse a gran costo.

Sales sabiendo cómo pasar de requisitos de negocio a un análisis de riesgos, y cómo abordar decisiones de arquitectura segura en autenticación/autorización, datos en tránsito (SSL/TLS), credenciales seguras (hashing, MFA), PII y datos financieros, motores de búsqueda y, finalmente, el patrón Zero Trust Architecture.

## El ejemplo que recorre el capítulo
MegaBank, tras limpiar agujeros de seguridad, decide lanzar su marca de merchandising MegaMerch (camisetas, pantalones, trajes de baño). Quiere una aplicación de ecommerce con estos requisitos: los usuarios crean cuentas e inician sesión; las cuentas guardan nombre completo, dirección y fecha de nacimiento; hay portada con artículos; búsqueda de artículos; y guardar tarjetas de crédito y cuentas bancarias.

Un análisis de alto nivel de esos requisitos revela: se almacenan credenciales, se almacena PII, los usuarios tienen privilegios elevados frente a invitados, hay búsqueda, y se almacenan datos financieros. De ahí se derivan áreas de riesgo iniciales: autenticación y autorización, datos personales (¿leyes aplicables?) y motor de búsqueda (¿fuente única de verdad o base cacheada aparte?).

## Analizar los requisitos de la funcionalidad
El primer paso es recopilar todos los requisitos de negocio que el producto debe implementar; pueden evaluarse en busca de riesgo antes incluso de integrarlos. Las organizaciones con equipos separados de seguridad y R&D deben construir rutas de comunicación dentro del proceso de desarrollo: las features no se analizan en silos y el análisis debe incluir stakeholders de ingeniería y de producto.

## Autenticación y autorización
Como se almacenan credenciales y se ofrece experiencia distinta a invitados y usuarios registrados, existen sistemas tanto de autenticación como de autorización. Esto obliga a considerar tres riesgos: cómo manejar los datos en tránsito, cómo almacenar las credenciales y cómo manejar los distintos niveles de autorización de los usuarios.

### SSL y TLS
La decisión arquitectónica inicial es cómo manejar los datos en tránsito, porque afecta el flujo de todos los datos. El requisito base: todo dato enviado por la red debe ir cifrado en ruta, reduciendo el riesgo de un ataque man-in-the-middle que podría robar credenciales y hacer compras en nombre del usuario. SSL y TLS son los dos protocolos criptográficos principales hoy. SSL fue diseñado por Netscape a mediados de los 90; TLS se definió en el RFC 2246 (1999) corrigiendo problemas de SSL. TLS no interopera con versiones viejas de SSL por sus diferencias arquitectónicas; TLS ofrece la seguridad más rígida, mientras SSL tiene más adopción pero múltiples vulnerabilidades. Let's Encrypt es una de las pocas autoridades de seguridad sin ánimo de lucro que emiten certificados para cifrado TLS. Los navegadores muestran un candado cuando la comunicación está asegurada; HTTPS es el esquema URI que exige TLS/SSL antes de enviar datos. Para MegaMerch se busca que todo dato sea cifrado y compatible con TLS antes de salir por la red.

### Credenciales seguras
Lo que hace segura una contraseña no es tanto su longitud o caracteres especiales, sino la ausencia de patrones observables. En criptografía esto es la entropía —la cantidad de aleatoriedad e incertidumbre—; se buscan contraseñas con mucha entropía. La mayoría de contraseñas no son únicas; un atacante usa listas de las más comunes para un dictionary attack (y ataques avanzados combinan contraseñas y estructuras comunes), y en última instancia el brute force clásico itera todas las combinaciones. Como es difícil transmitir esto a los usuarios, se imponen requisitos: rechazar contraseñas de una lista de las mil más comunes e impedir fechas de nacimiento, nombre, apellido o partes de la dirección. MegaMerch exige nombre, apellido y fecha de nacimiento en el registro y los bloquea dentro de la contraseña.

### Hashing de credenciales
Nunca almacenar credenciales en texto plano: se hashea la contraseña la primera vez antes de guardarla. Los algoritmos de hashing difieren del cifrado: no son reversibles (ni el propio personal puede robar contraseñas), son muy eficientes (representan cadenas de megabytes en 128 a 264 bits, permitiendo rehashear en login y comparar a gran velocidad) y tienen colisión casi nula en la práctica (0 o estadísticamente cercana a 0, 1/1.000.000.000+). Si roban la base de datos, el atacante solo obtiene el hash.

Tres casos con acceso a las bases de MegaMerch:

- Caso #1: contraseñas en texto plano → todas comprometidas.
- Caso #2: hasheadas con MD5 → el atacante puede romper algunas con rainbow tables (tabla precalculada hash → contraseña; algoritmos débiles son susceptibles).
- Caso #3: hasheadas con BCrypt → improbable que se rompa alguna.

El algoritmo debe elegirse por su integridad matemática y su escalabilidad frente al hardware moderno: debe ser LENTO en hardware moderno al hashear, reduciendo los intentos por segundo del atacante. Algoritmos muy lentos como BCrypt pueden tardar años en romper una sola contraseña.

- BCrypt: su nombre viene de Blowfish Cipher (cifrado de bloque de clave simétrica de Bruce Schneier, 1993) y de Crypt (función de hashing por defecto de Unix). Crypt se diseñó para hardware Unix antiguo (menos de 10 contraseñas/segundo), pero hoy hashea decenas de miles por segundo. BCrypt itera sobre ambos y se vuelve más lento en hardware más rápido: a mayor potencia, más operaciones, escalando al futuro.
- PBKDF2: alternativa basada en key stretching; genera el hash rápido en el primer intento pero cada intento adicional es más lento, haciendo el brute force costoso. No se diseñó originalmente para contraseñas, pero sirve cuando no hay algoritmos tipo BCrypt. Tiene una opción de iteraciones mínimas que debe fijarse al máximo que soporte tu hardware.

Para MegaMerch se decide hashear con BCrypt y comparar solo hashes.

### MFA
Además de contraseñas seguras, hasheadas y cifradas en tránsito, conviene ofrecer multifactor authentication (MFA). Google Authenticator es una de las apps MFA más comunes en Android e iOS, con API abierta. La mayoría de sistemas MFA exigen contraseña en el navegador más una contraseña generada por app móvil o SMS; los protocolos más avanzados usan un token de hardware físico (típicamente un USB que genera un token de un solo uso), más aplicable a empleados que a usuarios de un ecommerce. "MFA eliminates remote logins to your web application that were not initiated by the owner of the account" (PDF p. 301). La única forma de comprometer una cuenta con MFA es obtener la contraseña y el dispositivo físico. Se recomienda ofrecer MFA a los usuarios de MegaMerch.

## PII y datos financieros
Al almacenar PII hay que asegurar que sea legal en los países donde se opera y cumplir las leyes aplicables. Además, ante una brecha o compromiso del servidor, la PII no debe quedar expuesta en un formato fácilmente abusable. Reglas similares aplican a datos financieros como números de tarjeta (incluidos en leyes de PII en algunos países). Una empresa pequeña puede encontrar más efectivo externalizar el almacenamiento de estos datos a un negocio conforme (compliant) especializado.

## Motores de búsqueda
Un motor de búsqueda propio requiere almacenar datos de forma que ciertas consultas sean muy eficientes, algo distinto de una base de datos de propósito general. Por eso suele necesitarse una base separada de la que el motor extrae datos, lo que genera complicaciones que exigen arquitectura de seguridad desde el inicio. Sincronizar dos bases es grande: si cambia el modelo de permisos en la base primaria, hay que reflejarlo en la del buscador. Además, bugs pueden borrar modelos en la base primaria pero no en la de búsqueda, o metadatos de un objeto pueden seguir siendo buscables tras eliminar el objeto. Elasticsearch es el motor de búsqueda distribuido open source más grande y usado; es configurable, bien documentado, gratuito y se basa en el proyecto Solr de Apache.

## Zero Trust Architecture
Es la aplicación de la filosofía zero trust a la arquitectura de software (los términos se usan de forma intercambiable). Se conoce por varios nombres: Zero Trust, Zero Trust Network Access (ZTNA), Zero Trust Design, Zero Trust Pattern y Zero Trust Design Pattern.

### Historia del zero trust
El término apareció primero en la tesis doctoral de 1994 del científico Stephen Paul Marsh en la University of Stirling (Escocia), que argumentaba que la confianza podía descomponerse en un conjunto finito de criterios computables. Luego el término desapareció hasta 2018. En 2020 la NIST publicó el whitepaper Zero Trust Architecture (SP-800-207), que revitalizó el término; hoy zero trust suele referirse a esas guías.

### Confianza implícita vs. explícita
Zero Trust distingue dos tipos de confianza. La confianza implícita (según el whitepaper de la NIST) se concede por proximidad o roles. Ejemplo: un castillo con un foso; se asume que quien ya pasó el foso es de confianza, sin verificación adicional (modelo implícito que ignora al visitante que cruza el foso nadando). El equivalente relevante: una red protegida por firewall sin verificación tras el firewall. La NIST considera ese modelo obsoleto y productor de aplicaciones vulnerables. El mejor modelo es trust but verify o confianza explícita: la verificación ocurre cada vez que se invoca una funcionalidad privilegiada, de modo que existir en la zona de confianza implícita (cuenta AWS, pasar el firewall, autenticación previa) no basta. Toda acción que pueda llevar a un compromiso debe tener un paso de verificación delante.

### Autenticación y autorización (zero trust)
Zero Trust solapa mucho con el principio de least privilege: asegura que un actor (script, usuario) solo acceda a los recursos previstos. Ejemplo "Joe Admin": empleado con permisos de administrador sobre finanzas y cuentas bancarias; el software interno usa tokens con ventana de expiración de 48 horas y solo busca un token válido, sin verificar que el estado de Joe como empleado siga vigente. Al ser despedido, Joe puede seguir usando el software y modificar los libros por venganza. La Zero Trust Authorization habría prevenido el caso: el ataque ocurrió porque se concedió confianza implícita a cualquier usuario con token no expirado, sin considerar el cambio de estado laboral. Implementar el zero trust de la NIST en cada paso de autorización habría dado autorización continua, bloqueando el ataque.

## Ideas clave
- La fase de arquitectura es donde más barato se corrige una vulnerabilidad: la NIST estima entre 30 y 60 veces menos que en producción (PDF p. 292).
- Partir de los requisitos de negocio permite derivar riesgos tempranos (credenciales, PII, privilegios, búsqueda, datos financieros).
- Todo dato en tránsito debe cifrarse con TLS/SSL (TLS es más seguro); HTTPS exige TLS/SSL antes de enviar datos.
- La seguridad de una contraseña está en su entropía (falta de patrones), no tanto en su longitud; bloquear contraseñas comunes y datos personales.
- Nunca almacenar credenciales en texto plano: hashear con algoritmos lentos como BCrypt (o PBKDF2 con iteraciones al máximo del hardware); MD5 es vulnerable a rainbow tables.
- MFA elimina los inicios de sesión remotos no iniciados por el dueño de la cuenta; se recomienda ofrecerlo.
- La PII y los datos financieros deben cumplir la ley y poder externalizarse a un proveedor conforme; un motor de búsqueda propio (p. ej. Elasticsearch) añade una base separada que exige sincronización y cuidado.
- Zero Trust Architecture (NIST SP-800-207) sustituye la confianza implícita por verificación explícita y continua en cada acción privilegiada, evitando casos como el de "Joe Admin".
