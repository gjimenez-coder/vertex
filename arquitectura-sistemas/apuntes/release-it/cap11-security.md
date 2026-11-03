# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 11 — Security (Seguridad)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

La seguridad debe estar integrada desde el diseño, no añadirse al final como un condimento. Aunque exista un equipo de seguridad dedicado, cada desarrollador sigue siendo responsable de proteger a sus clientes y a su empresa. Una brecha puede traer fraude, extorsión, multas, pérdida de reputación y despidos; el capítulo recuerda casos como el ransomware WannaCry (2017, más de 70 países), el robo de identidades de 145,5 millones de consumidores en Equifax y los 3.000 millones de cuentas de Yahoo!. Las brechas no siempre buscan extraer datos: a veces implantan información, como identidades falsas o documentos de embarque.

El núcleo del capítulo es un recorrido por el OWASP Top 10 (basado en el "Release Candidate 1" de la lista de 2017), más dos temas transversales: el principio de mínimo privilegio y el manejo de contraseñas configuradas. Sales sabiendo cómo se producen las vulnerabilidades más críticas de aplicaciones web y qué defensas concretas aplicar en cada caso.

La tesis es que dos componentes seguros no forman necesariamente un sistema seguro. Hay que pensar la seguridad a nivel de componente y de sistema completo, y entenderla como un proceso continuo frente a amenazas que surgen constantemente.

## El OWASP Top 10

Desde 2001 la OWASP Foundation cataloga incidentes y vulnerabilidades de aplicaciones con datos de ataques reales aportados por sus organizaciones miembro.

### Injection (inyección)

Ataque a un parser o intérprete que confía en entrada del usuario. El ejemplo clásico es la inyección SQL ("Little Bobby Tables"): si la aplicación concatena cadenas para construir la consulta, la entrada puede terminar la consulta original e introducir sentencias destructivas como `DROP TABLE`. No hay excusa hoy: toda librería SQL permite placeholders.

```java
// Vulnerable a inyección
String query = "SELECT * FROM STUDENT WHERE NAME = '" + name + "';"

// Mejor
String query = "SELECT * FROM STUDENT WHERE NAME = ?;"
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, name);
ResultSet results = stmt.executeQuery();
```

"Viene de un usuario" no significa solo la petición HTTP actual: los datos de una base de datos pueden haberse originado en un usuario. Otro vector es XML, con la inyección de entidad externa (XXE), donde el DTD define una entidad externa que el parser expande leyendo una URL (por ejemplo `file:///etc/passwd`). La mayoría de los parsers XML son vulnerables a XXE por defecto; hay que configurarlos de forma segura siguiendo la cheat sheet de OWASP. La inyección ocupa el primer puesto del Top 10 desde 2010.

### Broken Authentication and Session Management

Cubre desde poner el ID de sesión en la URL hasta almacenar contraseñas sin salt. Los IDs de sesión en parámetros de URL son visibles para switches, routers, proxies y personas, y habilitan el "session hijacking". El capítulo relata el caso de un minorista electrónico cuyo email de oferta incluía un deep link con el ID de sesión del marketer, y miles de usuarios compartieron la misma sesión, causando una caída. Variantes: "session fixation" (el atacante entrega al usuario un ID de sesión que él controla) y "session prediction" (IDs predecibles o secuenciales).

Guías de OWASP para IDs de sesión:
- ID largo y con mucha entropía.
- Generarlo con un PRNG de buenas propiedades criptográficas (no el `rand()` del lenguaje).
- Proteger contra XSS para evitar la revelación del ID.
- Generar un ID nuevo al autenticar (frena session fixation).
- Usar las funciones de gestión de sesión de la plataforma y mantenerlas parcheadas.
- Intercambiar los IDs por cookies y no aceptarlos por otros mecanismos.

El problema más común con las credenciales sigue siendo el más simple: enviarlas en claro, por la dificultad histórica de los certificados TLS y de configurar un trust store. Let's Encrypt y los proveedores cloud facilitan esto. "Autenticación" es verificar la identidad del llamante, que puede ser de primera parte (nosotros guardamos las credenciales) o de tercera parte (el principal presenta una "prueba" emitida por otra autoridad: Kerberos, NTLM, OAuth). Abandonar la defensa "pie crust": hay que pensar la autenticación en todas partes y no confiar en la IP de origen.

Do's y don'ts: no guardar contraseñas en la base de datos ni enviarlas por email en el "forgotten password"; aplicar un hash fuerte con salt; permitir contraseñas largas y pegarlas en la GUI; planear rehashear en el futuro; y no permitir intentos de autenticación ilimitados (pero cuidado con bloquear a tres intentos, ya que los dispositivos reintentan automáticamente).

### Cross-Site Scripting (XSS)

Ocurre cuando un servicio renderiza la entrada del usuario directamente en HTML sin escaparla. Un parámetro `search` echo de vuelta sin escape permite inyectar un `<script>` que envía `document.cookie` a un sitio del atacante y secuestra la sesión. No es solo un problema de renderizado en servidor: muchos front-ends vuelcan contenido en el DOM sin escapar. Hay ataques dirigidos a GUIs de administración o visores de logs, donde el script se ejecuta con privilegios del admin. Regla: nunca confíes en la entrada; sanéala al entrar y escápala al salir. Usar el OWASP Java Encoder Project y una librería de generación de HTML que escape por defecto.

### Broken Access Control

Permite acceder a datos indebidos. Una forma común es el "direct object access": IDs secuenciales de base de datos en la URL que el atacante itera. Dos partes de solución: reducir el valor de sondear URLs y verificar la autorización sobre los objetos.

- Disuadir el sondeo: no usar IDs de base de datos en URLs; usar identificadores no secuenciales, URLs genéricas sensibles a sesión (`/users/me`), o un mapeo por sesión de IDs aleatorios a reales.
- Autorizar acceso: el servicio confunde "poseer una URL" con "tener permiso". Debe comprobar la autorización en cada petición; las URLs son solo texto que cualquiera puede crear.

Fuga de información sutil: responder 404 cuando el recurso no existe y 403 cuando existe pero no está autorizado revela qué recursos existen. Regla general: si el llamante no está autorizado a ver el recurso, debe ser como si no existiera.

Otra variante es el directory traversal (`../` en Unix, `..\` en Windows) para construir nombres de archivo y salir del directorio esperado, llegando incluso a sobrescribir archivos en cargas. La única forma segura de manejar uploads es tratar el nombre del cliente como una cadena arbitraria almacenada en la base de datos y generar una clave aleatoria única como nombre real de archivo (ver CWE-22).

### Security Misconfiguration

Suele ser por omisión: funciones innecesarias habilitadas por defecto, consolas de administración con contraseñas por defecto ("admin/admin"). Nunca permitir una contraseña por defecto en producción; vigilar imágenes de contenedores que incluyen servidores (Redis, Mongo, Postgres, ZooKeeper) con sus credenciales por defecto. En 2017 más de 20.000 instalaciones de MongoDB con credenciales por defecto expuestas a Internet fueron secuestradas por rescate en bitcoin. Reducir la "attack surface" separando el tráfico interno en su propia NIC; no poner nunca aplicaciones de ejemplo en producción; y que cada administrador use una cuenta personal, con logging en las llamadas administrativas.

### Sensitive Data Exposure

"La grande." Tarjetas de crédito, historiales médicos, seguros, emails. La exposición no suele venir de romper la criptografía, sino de grietas: un portátil robado con un extracto en una hoja de cálculo, o TLS en el borde pero HTTP plano internamente. Guías: no almacenar datos sensibles innecesarios (usar un tokenizador de tarjetas del proveedor de pagos); usar HTTP Strict Transport Security; dejar de usar SHA-1; nunca almacenar contraseñas en claro (Password Storage Cheat Sheet); cifrar datos sensibles en la base de datos; y descifrar según la autorización del usuario, no del servidor. En AWS considerar KMS (claves maestras y claves de cifrado de datos cifradas con una "key encryption key"); on-premises, HashiCorp Vault.

### Insufficient Attack Protection

Hay que asumir que los atacantes tienen acceso ilimitado a máquinas detrás del firewall. Los servicios no suelen rastrear peticiones ilegítimas por origen ni bloquear a quien emite demasiadas peticiones malas. El servicio debe registrar las peticiones malas por principal de origen para que las herramientas de logs detecten patrones. No es factible una whitelist de consumidores, pero sí una blacklist (lista de revocación de certificados o por nombre de principal). Los "API Gateways" bloquean por API key y limitan la tasa de peticiones; los firewalls de capa 7 detectan llamadas sospechosas.

### Cross-Site Request Forgery (CSRF)

Hoy la mayoría de frameworks lo defienden automáticamente, pero quedan apps viejas. El ataque empieza en otro sitio cuyo contenido enlaza al tuyo; el navegador de la víctima envía las cookies de sesión y tu sistema cree que es una petición válida. Defensas: evitar ser vehículo (escapar bien el XSS); usar anti-CSRF tokens en peticiones con efectos secundarios (cambios de contraseña, dirección, compras); y usar el atributo de cookie "SameSite" (`Set-Cookie: SID=...; SameSite=strict`), que a junio de 2017 soportaban la familia Chrome y Opera, pero no Firefox, Internet Explorer ni Edge. El RFC recomienda un par de cookies: una de "lectura" (no same-site, para GET) y una de "escritura" (same-site strict, para peticiones que cambian estado).

### Using Components with Known Vulnerabilities

Fue lo que afectó a Equifax (Struts 2, CVE-2017-5638). Pocos desarrolladores conocen todo su árbol de dependencias. La mayoría de ataques son mundanos: herramientas que sondean cientos de vulnerabilidades, algunas antiguas. Hay que mantener las aplicaciones al día: extraer un informe de artefactos del build (incluidos plugins), revisarlo semanalmente contra los CVEs, o usar un plugin que rompa el build ante un CVE (OWASP Dependency Check), o un servicio como VersionEye. Muchas vulnerabilidades nunca reciben CVE, así que conviene seguir listas y issue trackers de los proyectos.

### Underprotected APIs

Nueva entrada del Top 10. Los escáneres de seguridad tardan en abordar APIs por falta de metadatos estándar, y un atacante con las credenciales correctas es indistinguible de un usuario legítimo. Claves de defensa: aplicar bulkheading para que una credencial robada no dé acceso a datos de otros clientes (la API no puede usar hyperlinks como medida de seguridad: debe autorizar el enlace al salir y reautorizar la petición al volver); usar el medio más seguro de comunicación (TLS, rechazando downgrades de protocolo, CA raíz al día, y certificados bidireccionales en B2B); y endurecer el parser de datos contra entrada maliciosa con fuzz-testing mediante una librería de pruebas generativas.

## The Principle of Least Privilege

Un proceso debe tener el nivel mínimo de privilegio necesario, lo que nunca incluye correr como root o administrador. El software que corre como root es automáticamente un objetivo, y cualquier vulnerabilidad se vuelve crítica. Cada aplicación importante debe tener su propio usuario (el usuario "Apache" no debe acceder al de "Postgres"). Lo único que puede requerir root en UNIX es abrir un puerto por debajo de 1024, pero un servidor web tras un balanceador puede usar cualquier puerto.

Los contenedores dan aislamiento, pero cuidado: imágenes que incluyen casi un SO completo o un sistema init tienen una gran attack surface, y las herramientas de parcheo aún no saben tratarlos. La solución es tratar las imágenes como bienes perecederos, con un build automatizado (idealmente desde la CI) que cree imágenes nuevas desde una base upstream, con builds programados.

## Configured Passwords

Las contraseñas no pueden teclearse interactivamente al arrancar, así que las credenciales deben configurarse en archivos persistentes, y en cuanto están en un archivo de texto son vulnerables. Mínimo: mantener las contraseñas de producción separadas del resto de la configuración y fuera del directorio de instalación; que los archivos sean legibles solo por el usuario propietario (el usuario de la aplicación); y, si el lenguaje permite separación de privilegios, leer las contraseñas antes de bajar privilegios (archivos propiedad de root). El password vaulting cifra los archivos, reduciendo el problema a proteger la clave de cifrado, pero no es solución completa; conviene software de detección de intrusiones como Tripwire para vigilar permisos. AWS KMS evita que datos cifrados y claves de descifrado estén en el mismo almacenamiento; Vault guarda las credenciales directamente. Hay que borrar la clave de memoria lo antes posible, porque los volcados de memoria (core dumps en UNIX, "blue screen of death" en Windows) pueden contenerla; conviene deshabilitar los core dumps en producción.

## Security as an Ongoing Process

Ni los frameworks ni una revisión única del equipo de AppSec protegen frente al Top 10. La seguridad es una actividad continua y parte de la arquitectura: comunicación cifrada, cifrado en reposo, autenticación y autorización son preocupaciones transversales. Surgen ataques nuevos todo el tiempo, sobre todo al adoptar tecnología no probada en batalla, así que hace falta un proceso para descubrir y remediar rápido, y poder redesplegar los servidores en cualquier momento.

## Ideas clave

- La seguridad se integra desde el diseño; dos componentes seguros no forman necesariamente un sistema seguro.
- La inyección (SQL, XXE) nace de concatenar cadenas con entrada de usuario; usar placeholders y configurar los parsers de forma segura.
- Gestiona sesiones con IDs largos y aleatorios, transportados en cookies, renovados al autenticar, y protegidos frente a hijacking, fixation y prediction.
- Nunca confíes en la entrada: sanéala al entrar y escápala al salir (XSS); y verifica autorización en cada petición, no por posesión de una URL.
- Abandona el "pie crust": autentica en todas partes, cifra en tránsito incluso dentro de la organización y no confíes en la IP de origen.
- No almacenes datos sensibles que no necesites, usa HSTS y hashing con salt, y gestiona secretos con herramientas como AWS KMS o Vault.
- Mantén el árbol de dependencias al día frente a CVEs y protege las APIs con bulkheading, TLS sin downgrades y parsers endurecidos con fuzz-testing.
- Aplica el mínimo privilegio (nunca root), trata las imágenes de contenedor como perecederas y protege las contraseñas configuradas con permisos estrictos, vaulting y detección de intrusiones.
