# The History of Software Security (La historia de la seguridad del software) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre la relación entre hackers e ingenieros? / R: Existe una relación cíclica y continua: cada vez que una capa se vuelve más segura, los atacantes migran a una nueva superficie de ataque.

P: ¿Qué tipo de cifrado usaba la máquina Enigma en términos actuales? / R: Un symmetric key algorithm, un cifrado que usa una sola clave para cifrar y descifrar, familia aún empleada para proteger datos en tránsito.

P: ¿Cómo se llama hoy la interceptación de mensajes que Enigma buscaba evitar? / R: Ataque man-in-the-middle.

P: ¿Cuál era la principal debilidad de la red de máquinas Enigma? / R: La gestión de claves: una sola configuración comprometida inutilizaba toda la red, y los logs de configuración se intercambiaban en persona.

P: ¿Qué era una bombe y qué papel jugó Turing? / R: Un dispositivo electromecánico que intentaba revertir automáticamente la posición de los rotores; Turing la convirtió en una de las primeras herramientas de hacking automatizado.

P: ¿Qué técnica moderna ejemplifica el método de Turing basado en conocer una palabra o frase del mensaje? / R: El known plaintext attack (KPA), que usa pares de entrada/salida previos para un algoritmo más eficiente.

P: ¿Qué es el phreaking y de dónde sugiere el autor que viene el término? / R: La manipulación de sistemas telefónicos reproduciendo frecuencias de audio; el autor sugiere que el término viene de "audio frequency".

P: ¿Qué significaba el tono de 2600 Hz y para qué se abusaba? / R: Era usado internamente por AT&T para señalar fin de llamada; emitirlo mantenía el circuito abierto sin registrar facturación, permitiendo llamadas internacionales gratuitas.

P: ¿Qué lección de diseño deja el phreaking? / R: Los arquitectos solo consideraron al usuario normal (diseño "best-case scenario"); la enseñanza es considerar siempre el peor escenario primero.

P: ¿Qué es DTMF y por qué dificultó el phreaking? / R: El dual-tone multifrequency, que emite dos frecuencias simultáneas por tecla, difíciles de replicar con la voz o un silbato.

P: ¿Quién creó el primer virus informático y qué demostró? / R: Fred Cohen en 1983; demostró que detectar virus dentro de software válido mediante algoritmos era casi imposible.

P: ¿Qué fue el Morris Worm y qué consecuencia legal tuvo? / R: El primer virus desplegado fuera de un laboratorio (1988), que infectó unos 15.000 ordenadores; Robert Morris fue el primer hacker condenado en EE. UU.

P: ¿Qué cambio trajo la Web 2.0 respecto al objetivo de los ataques? / R: Trasladó el objetivo del servidor y la red hacia el usuario y la aplicación, popularizando phishing, DoS y XSS.

P: ¿Qué son XSS en el contexto del capítulo? / R: Vulnerabilidades de Cross-Site Scripting que ejecutan el código del atacante en la sesión del navegador dentro de un sitio legítimo.

P: ¿Cuáles son tres defensas modernas del navegador y los protocolos mencionadas? / R: Same Origin Policy (SOP), Content Security Policy (CSP) y SSL/TLS sobre HTTP.

## Preguntas de autoevaluación

P: ¿Por qué el autor aclara su perspectiva al iniciar el recorrido histórico? / R: Porque no es historiador sino profesional de seguridad, y el recorrido es una referencia de eventos críticos, no una cronología exhaustiva. (Lo que necesitas saber)

P: ¿Por qué la gestión de claves de Enigma era un punto débil y cómo lo resuelve el software actual? / R: Porque una configuración comprometida inutilizaba toda la red y los logs se intercambiaban en persona; en software las claves pueden ser más complejas y regenerarse por sesión, por request o en intervalos programados. (La máquina Enigma, hacia 1930)

P: ¿Cómo aprovechó Turing la rutina del ejército alemán para diseñar su algoritmo? / R: Usó que a diario se enviaba un parte meteorológico cifrado, lo que le daba una palabra o frase conocida y su posición en el mensaje. (Descifrado automatizado de Enigma, hacia 1940)

P: ¿Qué paso tecnológico eliminó casi todo el phreaking y por qué? / R: El paso de entradas analógicas a digitales, además de DTMF, porque los tonos eran mucho más difíciles de replicar y luego la señalización dejó de basarse en audio. (Tecnología anti-phreaking, hacia 1960)

P: ¿Qué dos paralelismos entre los virus de los 80 y los ataques actuales señala el capítulo? / R: La escalabilidad (saltar de un usuario a otro) y el camuflaje (esconder código malicioso en un programa legítimo), aunque hoy el objetivo suele ser el navegador. (Los orígenes del hacking informático, hacia 1980)

P: ¿Por qué el usuario se convirtió en el objetivo perfecto con la llegada de la Web 2.0? / R: Porque la web pasó de plataforma de documentos a plataforma de aplicaciones justo cuando funciones críticas migraban a web applications y existían pocos controles de seguridad. (El auge de la World Wide Web, hacia 2000)

P: ¿Por qué hoy los hackers más exitosos atacan la lógica escrita por los desarrolladores? / R: Porque el navegador es más seguro gracias a SOP, CSP y SSL/TLS, así que la superficie más explotable son los logic bugs de aplicaciones grandes y complejas con muchas dependencias. (Hackers en la era moderna, hacia 2015+)

## Puntos a dominar

- La relación cíclica entre atacantes e ingenieros y cómo cada nueva tecnología trae su propia superficie de ataque.
- Enigma como ejemplo de symmetric key algorithm y por qué su debilidad era la gestión de claves.
- La bombe de Turing como hacking automatizado y su conexión con el known plaintext attack (KPA).
- La lección del phreaking: diseñar para el peor escenario, no el mejor; DTMF como respuesta defensiva.
- La línea Fred Cohen (1983) → Morris Worm (1988) → primera condena por hacking en EE. UU.
- El giro de la Web 2.0: del servidor y la red hacia el usuario y la aplicación (phishing, DoS, XSS).
- Las defensas modernas del navegador y protocolos: Same Origin Policy, Content Security Policy y SSL/TLS.
