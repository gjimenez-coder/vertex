# Card-Not-Present Environment (Entorno de tarjeta no presente) — Estudio

## Tarjetas de repaso

P: ¿Qué es el entorno card-not-present (CNP)? / R: Aquel en el que ni la tarjeta ni el dispositivo están físicamente en el punto de venta: pagos por teléfono, correo, Internet, móvil o navegador, además de los que reutilizan datos de una transacción previa (card-on-file o facturación recurrente).

P: ¿Cuál es la tesis sobre la seguridad en CNP? / R: Se construye por capas complementarias: cifrado del canal (SSL/TLS), autenticación del titular (3D Secure/EMV 3DS 2.0), verificación de datos adicionales (AVS) y sustitución del PAN por tokens (tokenización).

P: ¿Qué tres rasgos de seguridad aporta SSL/TLS? / R: Validación criptográfica del certificado firmado del servidor por el cliente (con generación y reparto de una clave simétrica aleatoria), cifrado de las comunicaciones con esa clave de un solo uso, y una firma digital en cada mensaje del túnel.

P: ¿Qué significa la "D" de 3D Secure y cuáles son los tres dominios? / R: Significa "domain"; el modelo de tres dominios es adquirente, emisor e interoperabilidad.

P: ¿Cuáles son los módulos principales de 3D Secure? / R: MPI (Merchant Plug-In) en la tienda, Directory Server, ACS (Access Control Server) del lado emisor y Attempts/Stand-In Service.

P: ¿Qué son UCAF/CAVV y el ECI en 3D Secure? / R: UCAF (Universal Cardholder Authentication Field) o CAVV (Cardholder Authentication Verification Value) es la evidencia criptográfica; el ECI (E-Commerce Indicator) es un código de dos o tres dígitos: full authentication 05, attempted 06, no authentication 07.

P: ¿Por qué fracasó 3D Secure 1.0? / R: Por fricción y abandono: las tasas de abandono del carrito llegaron a cifras de dos dígitos, hasta un 40%, porque muchos titulares no recordaban o no renovaban su contraseña; la autenticación basada en riesgo lo alivió.

P: ¿Qué cambios introduce EMV 3DS 2.0 respecto a 1.0? / R: Usa JSON y JWE en vez de XML, es royalty-free, soporta flujo frictionless, mantiene redirección por navegador añadiendo plantillas de UI nativa y HTML, admite autenticaciones decoupled/out-of-band, cierra el bucle de usuarios desaparecidos, añade autenticación no de pago y peticiones iniciadas por el comercio (3RI), e incluye un SDK móvil.

P: ¿Cómo cambia la terminología en EMV 3DS 2.0? / R: El MPI pasa a ser 3DS Server, la tienda es 3DS Requestor y la app en el dispositivo es 3DS Client; Directory Server y ACS conservan su nombre.

P: ¿Qué secuencia de mensajes usa EMV 3DS 2.0? / R: PReq/PRes (enrutamiento previo), AReq/ARes (inicio de autenticación), CReq/CRes (challenge) y RReq/RRes (resultado y acuse).

P: ¿Cómo valida AVS la dirección en formato condensado? / R: Extrae los símbolos numéricos de la calle por orden de aparición y los compara con los almacenados; así "1600 Pennsylvania Ave NW" se condensa como "1600" y pasa aunque el cliente escriba variantes de la calle.

P: ¿Qué es un token y por qué reduce el fraude? / R: Un valor sustituto usado en vez del PAN real; al ser muy específico de la aplicación y ligarse a menudo a un único comercio, un token obtenido de un comercio no sirve en otros.

P: En la tokenización de procesador, ¿cómo se protege el dato? / R: Se combina PAN y caducidad en un vector V; el HSM descifra el DEK con la LMK, cifra V con el DEK y devuelve VDEK, que se guarda en base de datos con un token T asignado; V no se almacena.

P: ¿Qué es un servicio "account updater"? / R: Un servicio basado en ficheros que recibe una lista de PAN y caducidades, consulta a los emisores y devuelve el estado de cada cuenta (válida con nueva caducidad, o nuevo PAN y caducidad), evitando declinaciones "Do not honor" y "Revoke authorization".

P: ¿Qué es la tokenización de red de pago y qué habilita? / R: El token cumple el formato PAN estándar (IIN "2") pero la red lo traduce al PAN real; sigue la EMV Payment Tokenization Specification y habilita pagos móviles como Apple Pay y Samsung Pay con dCVV sobre Track 2.

## Preguntas de autoevaluación

P: ¿Por qué el cifrado del canal (SSL/TLS) no fue suficiente para el entorno CNP? / R: Resolvió el eavesdropping y los ataques man-in-the-middle, pero no permitía autenticar al titular ni la tarjeta más allá del CVV2, lo que motivó mecanismos adicionales como 3D Secure. (Sección: 3D Secure)

P: ¿Cómo funciona el proceso de 3D Secure 1.0 en sus dos pasos? / R: En la comprobación de participación el MPI consulta al Directory Server, que autentica al comercio y determina el ACS según el PAN o deriva al servicio Attempts; en la autenticación del pagador el MPI redirige el navegador (normalmente en un IFRAME) al ACS, que confirma la identidad con OTP por SMS, push de la app o contraseña estática. (Sección: 3D Secure)

P: ¿Qué problema de seguridad tenía la función Activation During Shopping (ADS)? / R: Al estar basada en IFRAME facilitaba el spoofing de la web del emisor, difícil de detectar incluso por titulares expertos. (Sección: 3D Secure)

P: En EMV 3DS 2.0, ¿qué tres resultados puede dar el ACS en el ARes? / R: Aprobar la transacción (frictionless), rechazarla de inmediato, o indicar que se requiere un challenge incluyendo una URL de ACS. (Sección: 3D Secure 2.0 (EMV 3D Secure))

P: ¿Qué es el flujo 3RI (3DS Requestor-Initiated) y qué resultados admite? / R: Un flujo sin UI de titular con tres resultados posibles: la transacción se autentica (p. ej. confirma una suscripción recurrente), se rechaza (la autorización permanente ya no es válida) o se lanza una autenticación decoupled por canal separado. (Sección: 3D Secure 2.0 (EMV 3D Secure))

P: ¿Por qué en una suscripción con facturación recurrente no se guardan CVV2, AVS ni la evidencia de 3D Secure? / R: El CVV2 una vez usado no valida mejor las siguientes transacciones y aumenta el riesgo de robo, la dirección puede cambiar, y la evidencia de 3D Secure no es reutilizable. (Sección: Tokenización)

P: ¿En qué se diferencia la facturación recurrente del card-on-file? / R: La recurrente automática se transmite solo con PAN y caducidad emparejada con la primera transacción de la serie (flag propietario); el card-on-file reutiliza los valores de forma interactiva en una compra posterior, pudiendo pedir reintroducir el CVV o un challenge de 3D Secure. (Sección: Tokenización)

P: ¿Cómo viaja un token en una compra de tarjeta presente con pago móvil? / R: Por contactless magstripe data entry mode: el número, único del dispositivo, se transmite por NFC junto a evidencia criptográfica (dynamic CVV) en la parte DD del Track 2, empaquetado en campos ISO 8583 existentes. (Sección: Tokenización)

## Puntos a dominar

- Explicar las cuatro capas de seguridad del entorno CNP y qué problema resuelve cada una.
- Describir los tres rasgos de seguridad de SSL/TLS y por qué no bastan para autenticar al titular.
- Reconstruir el modelo de tres dominios de 3D Secure y la función de MPI, Directory Server, ACS y Attempts/Stand-In.
- Interpretar los valores de UCAF/CAVV y los códigos ECI (05, 06, 07).
- Enumerar las causas del fracaso de 3D Secure 1.0 y el papel de la autenticación basada en riesgo.
- Diferenciar los flujos de EMV 3DS 2.0: frictionless, challenge (navegador y app), decoupled/out-of-band y 3RI.
- Ordenar la secuencia de mensajes PReq/PRes, AReq/ARes, CReq/CRes y RReq/RRes y los tres identificadores de transacción.
- Explicar la validación AVS en formato condensado y los estados de resultado posibles.
- Describir el flujo de tokenización de procesador con V, DEK, LMK, DEKLMK, VDEK, HSM y token T.
- Distinguir facturación recurrente, card-on-file, servicios de revocación de autorización y account updater.
- Contrastar la tokenización de procesador con la tokenización de red de pago (EMV Tokenization, IIN "2") y su uso en Apple Pay y Samsung Pay.
