# Security (Seguridad) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre seguridad? / R: La seguridad debe integrarse desde el diseño, no añadirse al final; y dos componentes seguros no forman necesariamente un sistema seguro, por lo que hay que pensarla a nivel de componente y de sistema completo.

P: ¿Qué es la inyección (injection) y cómo se defiende la inyección SQL? / R: Es un ataque a un parser o intérprete que confía en entrada del usuario; la inyección SQL se defiende usando placeholders (consultas parametrizadas con `PreparedStatement`) en lugar de concatenar cadenas.

P: ¿Qué es la inyección de entidad externa (XXE)? / R: Un vector de inyección por XML donde el DTD define una entidad externa que el parser expande leyendo una URL (por ejemplo `file:///etc/passwd`); la mayoría de parsers XML son vulnerables por defecto y hay que configurarlos de forma segura.

P: ¿Qué riesgos tienen los IDs de sesión en la URL? / R: Son visibles para switches, routers, proxies y personas, y habilitan el session hijacking; deben intercambiarse por cookies y no aceptarse por otros mecanismos.

P: ¿Qué diferencia hay entre session fixation y session prediction? / R: En session fixation el atacante entrega al usuario un ID de sesión que él controla; en session prediction los IDs son predecibles o secuenciales.

P: ¿Cuál es la regla básica para prevenir el XSS? / R: Nunca confiar en la entrada: sanearla al entrar y escaparla al salir, usando herramientas como el OWASP Java Encoder Project y una librería de HTML que escape por defecto.

P: ¿Qué es el "direct object access" y cómo se mitiga? / R: Usar IDs secuenciales de base de datos en la URL que el atacante itera; se mitiga disuadiendo el sondeo (IDs no secuenciales, URLs sensibles a sesión como `/users/me`) y verificando la autorización sobre los objetos en cada petición.

P: ¿Por qué responder con 404 y 403 según el caso puede filtrar información? / R: Responder 404 cuando el recurso no existe y 403 cuando existe pero no está autorizado revela qué recursos existen; la regla es que, si el llamante no está autorizado, debe ser como si el recurso no existiera.

P: ¿Cuál es la forma segura de manejar las cargas de archivos (uploads)? / R: Tratar el nombre del cliente como una cadena arbitraria almacenada en la base de datos y generar una clave aleatoria única como nombre real de archivo, evitando el directory traversal (`../`, `..\`).

P: ¿Qué es la "security misconfiguration" más típica? / R: Habilitar por omisión funciones innecesarias y dejar consolas de administración con contraseñas por defecto (admin/admin); nunca debe permitirse una contraseña por defecto en producción.

P: ¿De dónde suele venir la "sensitive data exposure"? / R: No de romper la criptografía, sino de grietas: un portátil robado con datos en una hoja de cálculo, o TLS en el borde pero HTTP plano internamente.

P: ¿Cómo se defiende el CSRF? / R: Evitar ser vehículo escapando bien el XSS, usar anti-CSRF tokens en peticiones con efectos secundarios y usar el atributo de cookie SameSite (`SameSite=strict`).

P: ¿Qué incidente ilustra el uso de componentes con vulnerabilidades conocidas? / R: La brecha de Equifax, causada por Struts 2 (CVE-2017-5638); conviene revisar el informe de artefactos del build contra CVEs y usar herramientas como OWASP Dependency Check.

P: ¿Qué implica el principio de mínimo privilegio? / R: Un proceso debe tener el nivel mínimo de privilegio necesario, que nunca incluye correr como root o administrador; cada aplicación importante debe tener su propio usuario.

P: ¿Por qué es peligroso un archivo de contraseñas configuradas y cómo se protege? / R: En cuanto una contraseña está en un archivo de texto es vulnerable; se protege separándola del resto de config, fuera del directorio de instalación, con permisos legibles solo por el usuario propietario, vaulting y detección de intrusiones como Tripwire.

## Preguntas de autoevaluación

P: ¿Por qué el autor dice que "viene de un usuario" no significa solo la petición HTTP actual? / R: Porque los datos almacenados en una base de datos pueden haberse originado en un usuario, de modo que una consulta que usa esos datos también puede sufrir inyección. (Sección: Injection)

P: ¿Qué recomienda OWASP para generar IDs de sesión seguros? / R: Usar un ID largo y con mucha entropía, generarlo con un PRNG de buenas propiedades criptográficas (no `rand()`), protegerlo frente a XSS, generar uno nuevo al autenticar, usar las funciones de la plataforma parcheadas e intercambiarlos por cookies. (Sección: Broken Authentication and Session Management)

P: ¿Qué significa abandonar la defensa "pie crust"? / R: Dejar de confiar solo en un perímetro externo: hay que autenticar en todas partes, cifrar en tránsito incluso dentro de la organización y no confiar en la IP de origen. (Sección: Broken Authentication and Session Management / Ideas clave)

P: ¿Qué defensas propone el capítulo frente a la "insufficient attack protection"? / R: Asumir que los atacantes tienen acceso ilimitado detrás del firewall, registrar las peticiones malas por principal de origen, usar blacklists (revocación de certificados o por principal), API Gateways con límite de tasa y firewalls de capa 7. (Sección: Insufficient Attack Protection)

P: ¿Cómo deben protegerse las APIs subprotegidas (underprotected APIs)? / R: Aplicar bulkheading para que una credencial robada no dé acceso a datos de otros clientes, usar el medio más seguro de comunicación (TLS sin downgrades, CA al día, certificados bidireccionales en B2B) y endurecer el parser con fuzz-testing. (Sección: Underprotected APIs)

P: ¿Qué riesgos introducen los contenedores respecto al mínimo privilegio y cómo se gestionan? / R: Las imágenes que incluyen casi un SO completo o un init tienen una gran attack surface y las herramientas de parcheo no saben tratarlas; se tratan como bienes perecederos con builds automatizados y programados desde la CI. (Sección: The Principle of Least Privilege)

P: ¿Por qué conviene deshabilitar los core dumps en producción al manejar contraseñas? / R: Porque los volcados de memoria (core dumps en UNIX, "blue screen of death" en Windows) pueden contener la clave de cifrado, por lo que hay que borrarla de memoria lo antes posible. (Sección: Configured Passwords)

P: ¿Por qué la seguridad es un proceso continuo y no una revisión única? / R: Porque ni los frameworks ni una revisión única de AppSec protegen frente al Top 10; surgen ataques nuevos constantemente, sobre todo con tecnología no probada en batalla, y hace falta descubrir, remediar y redesplegar rápido. (Sección: Security as an Ongoing Process)

## Checklist

- [ ] Usar placeholders/consultas parametrizadas en todo acceso SQL; nunca concatenar entrada de usuario.
- [ ] Configurar los parsers XML de forma segura frente a XXE siguiendo la cheat sheet de OWASP.
- [ ] Transportar los IDs de sesión en cookies, con entropía alta vía PRNG criptográfico, y regenerarlos al autenticar.
- [ ] Hashear las contraseñas con salt fuerte; no guardarlas en claro ni enviarlas por email; planear rehashear; limitar (con cuidado) los intentos de autenticación.
- [ ] Sanear la entrada al entrar y escaparla al salir (OWASP Java Encoder y librería de HTML que escape por defecto) para prevenir XSS.
- [ ] Verificar la autorización en cada petición; usar identificadores no secuenciales y responder como si el recurso no existiera cuando no se está autorizado.
- [ ] Generar nombres de archivo aleatorios en uploads y guardar el nombre del cliente como dato arbitrario; evitar directory traversal.
- [ ] Eliminar funciones y aplicaciones de ejemplo innecesarias; cambiar todas las contraseñas por defecto (p. ej. Redis, Mongo, Postgres, ZooKeeper); separar el tráfico interno en su propia NIC; cuentas administrativas personales con logging.
- [ ] No almacenar datos sensibles innecesarios; usar HSTS, dejar SHA-1, cifrar en reposo y descifrar según la autorización del usuario; gestionar secretos con AWS KMS o HashiCorp Vault.
- [ ] Registrar peticiones malas por principal; mantener blacklists y usar API Gateways / firewalls de capa 7.
- [ ] Usar anti-CSRF tokens en peticiones con efectos secundarios y el atributo de cookie SameSite.
- [ ] Extraer el informe de artefactos del build (incluidos plugins) y revisarlo contra CVEs semanalmente; usar OWASP Dependency Check o similar y seguir issue trackers de los proyectos.
- [ ] Ejecutar cada aplicación con su propio usuario y mínimo privilegio, nunca como root; tratar las imágenes de contenedor como perecederas con builds automatizados.
- [ ] Mantener las contraseñas configuradas separadas de la config, fuera del directorio de instalación, legibles solo por el usuario propietario; usar vaulting, Tripwire y deshabilitar core dumps en producción.
