# Injection (Inyección) — Estudio

## Tarjetas de repaso

P: ¿Qué dos componentes requiere todo ataque de inyección? / R: Un payload enviado por el usuario y un intérprete que lo ejecuta por falta de saneamiento del input.

P: ¿Cuáles son los tres niveles de gravedad creciente de la inyección según el capítulo? / R: SQL injection → code injection (intérprete/CLI) → command injection (OS anfitrión).

P: ¿Qué es SQL injection? / R: La forma clásica: una cadena SQL se escapa dentro de un payload HTTP y se ejecutan queries personalizadas en nombre del usuario.

P: ¿Cuál es la causa raíz de SQL injection? / R: Concatenar parámetros del usuario en la query sin sanearlos, en lugar de parametrizar.

P: ¿Por qué abundó la inyección en paquetes OSS de PHP + MySQL? / R: Por la laxitud de PHP al mezclar vista, lógica y datos (SQL, HTML y PHP en un mismo archivo); incluso WordPress cayó víctima.

P: ¿Qué diferencia a code injection de SQL injection? / R: En code injection el script corre bajo un intérprete o CLI (no solo una BD SQL), y suele ser específico de la aplicación, menos común y peor documentado.

P: ¿Qué convierte un code injection en command injection? / R: Que el CLI/comandos se ejecuten contra el OS anfitrión en lugar de en su propio entorno aislado.

P: ¿Por qué command injection es de los ataques más peligrosos? / R: Porque ejecuta comandos (normalmente Bash) contra el OS; con acceso de superusuario en Unix se puede hacer lo que se quiera con ese sistema.

P: ¿Qué archivos críticos del OS quedan expuestos tras un command injection? / R: /etc/passwd, /etc/shadow, ~/.ssh, /etc/apache2/httpd.conf y /etc/nginx/nginx.conf.

P: ¿Qué es la exfiltración in-band? / R: El caso más fácil y común: el resultado del payload se ve directamente en el navegador o en la respuesta HTTP, usando el mismo canal.

P: ¿Qué es la exfiltración out-of-band (OOB)? / R: Cuando el resultado no se refleja; se usan utilidades HTTP del motor SQL (util_http) para enviar los datos a un servidor del atacante.

P: ¿Qué es la inyección inferencial o blind? / R: Cuando ni in-band ni OOB sirven; no se obtienen respuestas pero se fuerza al servidor a comportarse de forma errática, p. ej. con WAITFOR DELAY y lógica condicional.

P: ¿Por qué las blocklists son una defensa pobre? / R: Se evaden fácilmente porque a menudo se puede expresar la misma lógica de otra forma que el intérprete entiende igual (p. ej. codificando el payload en base64).

P: ¿Qué defensas son superiores a las blocklists frente a la inyección? / R: Allowlists, prepared statements y stored procedures.

## Preguntas de autoevaluación

P: ¿Por qué la inyección puede ocurrir contra bases de datos, CLI y el propio OS? / R: Porque el patrón común es el mismo —un payload del usuario que llega sin sanear a un intérprete—, y ese intérprete puede ser SQL, un CLI como FFMPEG/imagemin o el shell del OS. (Lo que necesitas saber)

P: Según el capítulo, ¿cómo evolucionó la frecuencia de las vulnerabilidades de inyección y por qué? / R: Bajaron de casi el 5% de todas las vulnerabilidades en 2010 a menos del 1% hoy, en parte por el declive del uso de PHP (índice TIOBE) y por estándares de codificación más estrictos. (SQL Injection)

P: En el ejemplo del convertidor de vídeo, ¿cómo se pasa de code injection a command injection? / R: Escapando comillas para salir del CLI y ejecutar comandos Bash contra el OS; p. ej. `' && rm -rf /videos`, que se concatena tras la opción legítima. (Command Injection)

P: ¿Qué función cumplen las técnicas de exfiltración cuando el atacante no recibe respuestas del servidor? / R: Permiten conocer el estado del ataque; según el caso se usa in-band, out-of-band (util_http hacia el servidor atacante) o inferencial/blind. (Injection Data Exfiltration Techniques)

P: ¿Cómo infiere información un atacante con WAITFOR DELAY? / R: Fuerza un retardo condicional: si la respuesta tarda más de lo normal (p. ej. 30 s, atípico en el 99.99% de queries) el payload tuvo éxito; con delay si verdadero y no delay si falso se infiere dato a dato. (Injection Data Exfiltration Techniques)

P: ¿Cómo se evade una blocklist que bloquea el comando `mail`? / R: Codificando el payload en base64 para que pase el filtro de texto plano; la utilidad `base64` de la terminal lo decodifica y lo canaliza (pipe) hacia Bash. (Bypassing Common Defenses)

P: ¿Qué mitigación parcial ofrece Unix frente a command injection y por qué suele fallar? / R: Su sistema de permisos sobre archivos, directorios, usuarios y comandos puede forzar a la API a correr como usuario no privilegiado; pero la mayoría de apps vulnerables no configuran estos perfiles. (Command Injection)

P: ¿En qué se diferencia la causa de la inyección respecto a la de XXE? / R: La inyección no depende de una especificación débil (como XXE), sino de confiar demasiado en las entradas del usuario. (Ideas clave)

## Puntos a dominar

- Identificar los dos factores presentes en todo ataque de inyección: payload del usuario + intérprete sin saneamiento.
- Distinguir los tres niveles: SQL injection, code injection (intérprete/CLI) y command injection (OS).
- Reconocer la concatenación de input en queries o comandos como causa raíz, frente a la parametrización.
- Explicar por qué command injection encabeza las escalas de riesgo y qué recursos del OS expone.
- Diferenciar las tres técnicas de exfiltración: in-band, out-of-band y inferencial/blind.
- Argumentar por qué las allowlists, prepared statements y stored procedures superan a las blocklists.
- Entender por qué los parsers y CLI poco comunes tienen defensas más débiles y peor documentación que las BD conocidas.
