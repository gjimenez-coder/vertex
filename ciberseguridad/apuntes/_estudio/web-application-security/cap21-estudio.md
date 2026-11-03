# Secure Application Architecture (Arquitectura de aplicaciones segura) — Estudio

## Tarjetas de repaso

P: ¿Por qué la fase de arquitectura es el primer paso para asegurar una aplicación web?
R: Porque re-arquitecturar o refactorizar es caro una vez construida la aplicación; según la NIST, corregir una vulnerabilidad en diseño cuesta entre 30 y 60 veces menos que en producción.

P: ¿Qué áreas de riesgo revela el análisis de alto nivel de los requisitos de MegaMerch?
R: Se almacenan credenciales, se almacena PII, los usuarios tienen privilegios elevados frente a invitados, hay búsqueda y se almacenan datos financieros.

P: ¿Qué tres riesgos obliga a considerar tener sistemas de autenticación y autorización?
R: Cómo manejar los datos en tránsito, cómo almacenar las credenciales y cómo manejar los distintos niveles de autorización de los usuarios.

P: ¿Cuál es la diferencia entre SSL y TLS según el capítulo?
R: SSL lo diseñó Netscape a mediados de los 90 y tiene más adopción pero múltiples vulnerabilidades; TLS se definió en el RFC 2246 (1999), corrige problemas de SSL, ofrece la seguridad más rígida y no interopera con SSL antiguo.

P: ¿Qué es la entropía en el contexto de contraseñas?
R: La cantidad de aleatoriedad e incertidumbre; lo que hace segura una contraseña es la ausencia de patrones observables, más que su longitud o caracteres especiales.

P: ¿Qué tres propiedades distinguen al hashing del cifrado?
R: No es reversible, es muy eficiente (representa cadenas grandes en 128 a 264 bits) y tiene colisión casi nula en la práctica.

P: ¿Por qué un buen algoritmo de hashing debe ser lento en hardware moderno?
R: Porque reduce los intentos por segundo del atacante; algoritmos muy lentos como BCrypt pueden tardar años en romper una sola contraseña.

P: ¿De dónde viene el nombre BCrypt y qué lo hace resistente al futuro?
R: De Blowfish Cipher (Bruce Schneier, 1993) y de Crypt (hashing por defecto de Unix); itera sobre ambos y se vuelve más lento en hardware más rápido, escalando al futuro.

P: ¿Qué es PBKDF2 y cuándo conviene usarlo?
R: Una alternativa basada en key stretching; genera el hash rápido en el primer intento pero cada intento adicional es más lento. Sirve cuando no hay algoritmos tipo BCrypt y debe fijarse su mínimo de iteraciones al máximo que soporte el hardware.

P: ¿Qué aporta la MFA según el libro?
R: "MFA eliminates remote logins to your web application that were not initiated by the owner of the account" (PDF p. 301); la única forma de comprometer la cuenta es obtener contraseña y dispositivo físico.

P: ¿Por qué un motor de búsqueda propio complica la arquitectura de seguridad?
R: Suele requerir una base separada de la primaria que exige sincronización: cambios de permisos deben reflejarse, bugs pueden desincronizar datos y metadatos pueden seguir siendo buscables tras eliminar un objeto.

P: ¿Qué es la Zero Trust Architecture y de dónde proviene el término?
R: Es la aplicación de la filosofía zero trust a la arquitectura de software; el término apareció en la tesis doctoral de 1994 de Stephen Paul Marsh y lo revitalizó el whitepaper de la NIST SP-800-207 (2020).

P: ¿Cuál es la diferencia entre confianza implícita y confianza explícita?
R: La implícita se concede por proximidad o roles (p. ej. estar tras un firewall), modelo que la NIST considera obsoleto; la explícita ("trust but verify") verifica cada vez que se invoca una funcionalidad privilegiada.

P: ¿Qué ilustra el ejemplo de "Joe Admin"?
R: Que conceder confianza implícita a cualquier token no expirado es peligroso: tras ser despedido, Joe pudo seguir usando el software porque no se verificaba su estado laboral; la autorización continua lo habría bloqueado.

## Preguntas de autoevaluación

P: ¿Qué argumento económico sostiene la tesis del capítulo sobre resolver vulnerabilidades en diseño?
R: Que corregir una vulnerabilidad en la fase de diseño cuesta entre 30 y 60 veces menos que en producción, por lo que la planificación temprana evita rehacer código a gran costo. (Sección "Lo que necesitas saber")

P: Partiendo de los requisitos de negocio de MegaMerch, ¿cómo se derivan las áreas de riesgo iniciales?
R: Recopilando todos los requisitos y evaluándolos antes de integrarlos; de ellos se deducen autenticación/autorización, datos personales (leyes aplicables) y motor de búsqueda (fuente única de verdad o base cacheada aparte). (Secciones "El ejemplo que recorre el capítulo" y "Analizar los requisitos de la funcionalidad")

P: ¿Por qué la decisión sobre datos en tránsito se toma al inicio de la arquitectura?
R: Porque afecta el flujo de todos los datos; todo dato enviado por la red debe ir cifrado para reducir el riesgo de un ataque man-in-the-middle que podría robar credenciales y comprar en nombre del usuario. (Sección "SSL y TLS")

P: ¿Qué diferencia hay entre los casos #2 (MD5) y #3 (BCrypt) si roban la base de datos de MegaMerch?
R: Con MD5 el atacante puede romper algunas contraseñas con rainbow tables por ser un algoritmo débil; con BCrypt es improbable que rompa alguna. (Sección "Hashing de credenciales")

P: ¿Qué requisitos impone MegaMerch a las contraseñas y por qué?
R: Rechaza contraseñas de la lista de las mil más comunes e impide usar nombre, apellido, fecha de nacimiento o partes de la dirección, porque la seguridad está en la falta de patrones (entropía) y porque esos datos se piden en el registro. (Sección "Credenciales seguras")

P: ¿Qué consideraciones legales y de arquitectura aplican a la PII y a los datos financieros?
R: Asegurar que almacenarlos sea legal en los países donde se opera, cumplir las leyes aplicables y evitar que queden expuestos en formato abusable ante una brecha; una empresa pequeña puede externalizarlos a un proveedor conforme. (Sección "PII y datos financieros")

P: ¿Cómo habría prevenido la Zero Trust Authorization el caso de "Joe Admin"?
R: Aplicando verificación explícita y continua en cada paso de autorización, de modo que tener un token no expirado no bastara; se habría comprobado que su estado de empleado siguiera vigente. (Sección "Autenticación y autorización (zero trust)")

P: ¿Qué relación tiene el zero trust con el principio de least privilege?
R: Solapa mucho con él: asegura que un actor (script o usuario) solo acceda a los recursos previstos y que existir en una zona de confianza implícita no conceda acceso adicional. (Sección "Autenticación y autorización (zero trust)")

## Checklist

- [ ] Recopilar y analizar los requisitos de negocio en busca de riesgo antes de integrarlos, con stakeholders de ingeniería y de producto.
- [ ] Cifrar todo dato en tránsito con TLS/SSL (preferir TLS) y servir la aplicación por HTTPS.
- [ ] Rechazar contraseñas de la lista de las mil más comunes y bloquear nombre, apellido, fecha de nacimiento y partes de la dirección dentro de la contraseña.
- [ ] Nunca almacenar credenciales en texto plano: hashear con un algoritmo lento como BCrypt (o PBKDF2 con iteraciones al máximo del hardware) y comparar solo hashes.
- [ ] Evitar algoritmos débiles como MD5, susceptibles a rainbow tables.
- [ ] Ofrecer MFA (app móvil, SMS o token de hardware) para eliminar inicios de sesión remotos no iniciados por el dueño.
- [ ] Verificar la legalidad de almacenar PII y datos financieros y valorar externalizarlos a un proveedor conforme.
- [ ] Si se usa un motor de búsqueda propio (p. ej. Elasticsearch), planificar la sincronización de permisos y datos entre la base primaria y la de búsqueda desde el inicio.
- [ ] Aplicar Zero Trust Architecture (NIST SP-800-207): sustituir la confianza implícita por verificación explícita y continua en cada acción privilegiada.
