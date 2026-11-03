# Denial of Service (Denegación de servicio) — Estudio

## Tarjetas de repaso

P: ¿Qué se considera un ataque de denegación de servicio (DoS) según el capítulo?
R: Cualquier esfuerzo automatizado que degrade o impida la usabilidad de una aplicación web, sin importar su origen; abarca desde un solo usuario hasta el bloqueo total, en cliente, servidor o red.

P: ¿Qué es una *malicious regex* (o *evil regex*) y qué operador suele formarla?
R: Una expresión regular construida para correr lentamente; la mayoría se forman con el operador `+`, que convierte la operación en "greedy" (busca una o más coincidencias en lugar de parar en la primera).

P: ¿Qué fenómeno provoca una regex maliciosa al encontrar un caso de fallo?
R: Backtracking: el motor retrocede probando exhaustivamente todas las combinaciones válidas antes de determinar que la entrada no es válida.

P: ¿Cómo escala el tiempo de la regex `/^((ab)*)+$/` según la Tabla 14-1?
R: El tiempo se duplica cada dos caracteres añadidos (8 ms a 23 chars, 15 ms a 25, 31 ms a 27, 61 ms a 29).

P: ¿Por qué una regex maliciosa puede permanecer latente durante años?
R: Porque no es vulnerable a todas las entradas; solo ciertas cadenas disparan el backtracking significativo, apareciendo "de la nada" cuando un hacker encuentra esa entrada. El OSS es especialmente vulnerable.

P: ¿En qué consiste un DoS lógico?
R: Un usuario ilegítimo drena los recursos del servidor, causando degradación o pérdida de servicio para los legítimos; es difícil de encontrar y requiere pericia.

P: ¿Qué operaciones intensivas en recursos se buscan en un DoS lógico?
R: Operaciones síncronas confirmadas, escrituras en base de datos, escrituras en disco, SQL joins, backups de archivos y operaciones lógicas en bucle.

P: ¿Cómo se comprueba si una operación es síncrona sin acceso al servidor?
R: Lanzando la misma petición varias veces a la vez y viendo si las respuestas llegan escalonadas; conviene promediar unas cien llamadas API para que picos de tráfico o cron jobs no alteren las métricas.

P: ¿Qué diferencia a un DDoS de un DoS de un solo hacker?
R: El DDoS involucra múltiples atacantes (otros hackers o botnets); drena recursos con peticiones en masa, incluso peticiones estándar, hasta ahogar los recursos de los usuarios legítimos.

P: En la práctica, ¿a qué nivel y con qué tráfico suelen operar los DDoS?
R: A nivel de red (no de aplicación), haciendo peticiones directas contra la IP del servidor, normalmente con tráfico UDP para ahogar el ancho de banda disponible.

P: ¿Qué son las botnets y por qué dificultan la detección?
R: Equipos de personas reales tomados vía malware distribuido y controlados remotamente; como son usuarios reales, cuesta distinguir a los clientes ilegítimos de los legítimos.

P: ¿En qué consiste un ataque YoYo?
R: Aprovecha el autoescalado de proveedores cloud (AWS, GCP) con oleadas intermitentes de peticiones: se invoca el escalado, se corta el tráfico de golpe, y al bajar la carga se lanza otra oleada; degrada la experiencia e infla los costes de hosting.

P: ¿Cómo funcionan los ataques de compresión y qué ejemplo da el capítulo?
R: Un archivo malformado subido por el usuario consume muchos recursos al parsearse durante la compresión; p. ej. CVE-2021-38094 en FFMPEG 4.1, un vídeo que dispara un integer overflow en `filter_sobel()` (`libavfilter/vf_convolution.c`).

P: ¿Qué es un proxy-based DoS?
R: Robar recursos de cómputo de servicios legítimos (p. ej. crawlers de buscadores) redirigiendo sus peticiones al objetivo mediante subdominios proxy, para degradarlo sin pagar los recursos uno mismo y ocultar al causante.

## Preguntas de autoevaluación

P: ¿Por qué la mayoría de programas de bug bounty prohíben los envíos de DoS?
R: Porque probar DoS es difícil y podría interferir con el uso normal de la aplicación por usuarios reales. (Sección "Lo que necesitas saber")

P: Dada la regex `/^((ab)*)+$/`, ¿por qué la entrada `abababababababa` (con una `a` extra) se evalúa lento mientras una cadena par corre rápido?
R: La cadena es válida hasta el final y, al fallar por el carácter extra, el motor retrocede probando exhaustivamente todas las combinaciones de `(ab)`, una por cada carácter de longitud, antes de concluir que no es válida. (Sección "Regex DoS")

P: Al analizar una app de fotos con objetos User, Album, Photo y Metadata, ¿cómo deduces que el endpoint `GET /metadata/:userid` es candidato a DoS lógico?
R: Porque pedir todos los metadatos asociados a un usuario implica que el backend corre un join complejo o una consulta iterativa sobre objetos relacionados por ID, una operación intensiva en recursos. (Sección "Logical DoS Vulnerabilities")

P: Según la Tabla 14-3, ¿cómo cambia el tiempo de respuesta entre una cuenta nueva y un power user, y qué permite deducir?
R: Pasa de 120 ms (1 álbum, 1 foto) a 1.870 ms (28 álbumes, 490 fotos); permite deducir que creando un perfil muy grande (p. ej. 600 álbumes y 3.500 fotos) y lanzando peticiones repetidas se reduce el rendimiento para otros usuarios. (Sección "Logical DoS Vulnerabilities")

P: ¿Por qué en la práctica los DDoS rara vez usan DoS lógico o de regex?
R: Porque atacan a un nivel más bajo, el de red, haciendo peticiones directas contra la IP del servidor (normalmente tráfico UDP) para ahogar el ancho de banda, en lugar de explotar la lógica de la aplicación. (Sección "Distributed DoS")

P: ¿Por qué los ataques de compresión son difíciles de encontrar?
R: Porque muchas apps dependen de software de terceros como FFMPEG e ImageMagick, que simplifican el manejo de archivos complejos pero exponen una superficie amplia para payloads malformados. (Sección "Compression Attacks")

P: Más allá de la interrupción del servicio, ¿qué riesgo adicional menciona el resumen sobre los ataques DoS?
R: Que algunos DoS pueden filtrar datos, por lo que hay que vigilar logs y errores que aparezcan a raíz de los intentos. (Sección "Summary")

## Checklist

- Probar las vulnerabilidades DoS en un entorno de desarrollo local, para que los usuarios reales no sufran interrupciones del servicio.
- Revisar los parsers de regex del proyecto buscando operadores greedy (`+`) y patrones propensos a backtracking como `/^((ab)*)+$/`, especialmente donde los usuarios aporten sus propias expresiones.
- Prestar atención especial a regex en dependencias OSS, donde las regex maliciosas suelen pasar desapercibidas.
- Inventariar operaciones intensivas en recursos: operaciones síncronas, escrituras en BD/disco, SQL joins, backups de archivos y bucles lógicos.
- Cronometrar las peticiones de principio a fin con las developer tools del navegador y comprobar si una operación es síncrona lanzando varias peticiones a la vez para ver si las respuestas llegan escalonadas.
- Promediar alrededor de cien llamadas API al medir, para que picos de tráfico o cron jobs no alteren las métricas.
- Mapear la estructura del backend analizando payloads de red y la UI (relaciones User → Album → Photo → Metadata referenciadas por ID).
- Comprobar y restringir las rutas de subida de archivos que delegan en terceros (FFMPEG, ImageMagick) frente a archivos malformados (p. ej. CVE-2021-38094).
- Revisar el `robots.txt` y las allowlist de crawlers para evitar que subdominios proxy abusen de los buscadores contra la propia app.
- Vigilar logs y errores generados por intentos de DoS, por si filtran datos.
