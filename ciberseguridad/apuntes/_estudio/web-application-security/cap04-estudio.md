# Finding Subdomains (Encontrar subdominios) — Estudio

## Tarjetas de repaso

P: ¿Qué objetivo persigue el recon al buscar subdominios? / R: Construir un mapa de la aplicación para priorizar y desplegar payloads más adelante; es un componente inicial de esa búsqueda.

P: ¿Por qué suele ser más interesante atacar subdominios ocultos que el dominio `www`? / R: Los dominios de cara al consumidor reciben más escrutinio y se parchean rápido, mientras que los servidores "entre bastidores" (correo, admin) suelen tener más bugs por su menor uso y exposición.

P: ¿Qué muestra la pestaña XHR dentro de Network en las herramientas del navegador? / R: Las peticiones POST, GET, PUT, DELETE, etc., filtrando fuentes, imágenes, vídeos y dependencias.

P: ¿Qué son los ataques de canal lateral (side-channel) según el capítulo? / R: Ataques que se apoyan en una métrica secundaria distinta de la respuesta (como las métricas de Timing) para deducir qué código corre en el servidor.

P: ¿Qué hace el operador de búsqueda `site:` en Google? / R: Consulta resultados solo dentro de un dominio concreto (p. ej. `site:mega-bank.com`).

P: ¿Para qué sirve `-inurl:<pattern>` y qué riesgo tiene? / R: Descarta URLs que coincidan con un patrón (p. ej. `-inurl:www`); filtra el patrón en toda la cadena de la URL, así que puede producir falsos positivos como descartar `https://admin.mega-bank.com/www`.

P: ¿Cuándo conviene un archivo web como archive.org frente a un buscador? / R: Para datos históricos conviene un archivo web; para datos actuales conviene un buscador.

P: ¿Qué diferencia a las APIs search, streaming y firehose de X para recon? / R: La search API da los datos más relevantes para la mayoría de apps; streaming pierde >99% de los tweets; firehose garantiza el 100% de los tweets que cumplen el criterio.

P: ¿Qué es una transferencia de zona DNS y qué contiene el zone file? / R: Es el mecanismo con que los servidores DNS sincronizan sus registros compartiéndolos en un formato de texto (zone file) que contiene configuración DNS no destinada a ser accesible.

P: ¿Qué comandos usa el capítulo para intentar una transferencia de zona? / R: Primero `host -t mega-bank.com` para hallar los nameservers y luego `host -l mega-bank.com ns1.bankhost.com` para solicitar la transferencia.

P: ¿Cómo responde un servidor DNS bien configurado a una transferencia de zona no autorizada? / R: Solo resuelve transferencias de un servidor secundario autorizado; si no, responde `: Transfer Failed.`.

P: ¿Por qué la fuerza bruta de subdominios debe ser el último recurso? / R: Es muy fácil de detectar y registrar (puede provocar bloqueo de IP) y es lenta por limitaciones de tasa, regex y otros mecanismos.

P: ¿Por qué se usa `dns.resolve` en lugar de `dns.lookup` en Node.js? / R: `dns.lookup` se apoya en `getaddrinfo(3)`/libuv implementado de forma síncrona, mientras que `dns.resolve` es realmente asíncrono.

P: ¿Qué es un ataque de diccionario de subdominios y qué herramienta se cita? / R: Itera sobre una lista de los subdominios más comunes en vez de todas las combinaciones; se cita el escáner open source **dnscan**, con listas basadas en millones de subdominios de más de 86.000 registros de zona DNS.

P: ¿En qué orden conviene aplicar diccionario y fuerza bruta? / R: Empezar por el diccionario (más eficiente) y recurrir a la generación por fuerza bruta solo si el diccionario no da resultados.

## Preguntas de autoevaluación

P: ¿Por qué hoy es raro que un único dominio sirva toda una aplicación web? / R: Lo habitual es separar cliente y servidor en dominios distintos, además de distinguir `https://www` del dominio pelado. (Lo que necesitas saber)

P: En el caso guía de MegaBank, ¿por qué no se centra el ataque en `www.mega-bank.com`? / R: Porque ese dominio ya está ampliamente cubierto por un programa de bug bounty y las vulnerabilidades fáciles ya están corregidas, así que se buscan objetivos más fáciles en otros subdominios. (El ejemplo que recorre el capítulo / Lo que necesitas saber)

P: ¿Cómo se puede identificar a qué dominio se envió una petición usando solo el navegador? / R: Revisando request → headers → general → request URL en la pestaña Network; a menudo basta para encontrar los servidores afiliados. (Las herramientas de análisis de red del navegador)

P: ¿Qué tipo de información dice el autor haber encontrado en registros públicos durante pentests? / R: Repos de GitHub en caché hechos públicos por error, claves SSH, claves de AWS o Stripe expuestas, listados DNS y URLs no públicas, páginas de productos no lanzados, registros financieros y correos/teléfonos/usuarios. (Aprovechar los registros públicos)

P: ¿Por qué los subdominios aparecen en archivos antiguos como archive.org? / R: Suelen aparecer vía hiperenlaces que estaban en el HTML o JS pero ya no se ven en la app en vivo, porque el archivo guarda instantáneas periódicas. (Archivos accidentales)

P: ¿Cómo se fuerza una coincidencia exacta en la búsqueda de la API de X? / R: Por defecto la búsqueda es difusa (fuzzy); para coincidencia exacta se envía la cadena entre comillas dobles escapadas: `"keyword": "\"mega-bank.com\""`. (Instantáneas sociales)

P: ¿Por qué conviene hacer las peticiones asíncronas en la fuerza bruta de subdominios? / R: Porque requiere conectividad de red con latencia típica de 50 a 250 ms por petición, así que se lanzan lo más rápido posible sin esperar la respuesta anterior. (Fuerza bruta de subdominios)

P: ¿Para qué se usa el doble `!!` en el script de resolución DNS? / R: Para descartar los resultados que no tienen IP, dejando solo los subdominios vivos. (Fuerza bruta de subdominios)

## Checklist

- Recorrer la funcionalidad visible de la app con la pestaña Network/XHR del navegador y revisar request URL para hallar servidores afiliados y endpoints de baja dificultad.
- Usar operadores de búsqueda (`site:mega-bank.com`, `-inurl:www`) encadenando negaciones para descartar subdominios ya conocidos, y repetir en otros buscadores como Bing.
- Consultar archive.org abriendo varias instantáneas de fechas distintas, copiar el HTML y buscar esquemas de URL (`http://`, `https://`, `file://`, `ftp://`, `ftps://`).
- Consultar la search API de X con un bearer token para hallar subdominios de campañas de marketing, rastreadores de anuncios y eventos de contratación.
- Buscar los nameservers con `host -t mega-bank.com` e intentar la transferencia de zona con `host -l mega-bank.com ns1.bankhost.com`.
- Reservar la fuerza bruta como último recurso; priorizar el ataque de diccionario (p. ej. listas de dnscan) sobre la generación de todas las combinaciones.
- Mantener las listas grandes separadas del script (formato `.csv`) y leerlas en tiempo de ejecución; usar `dns.resolve` (asíncrono) en vez de `dns.lookup`.
- Combinar varias técnicas, ya que ninguna es completa por sí sola, y volver a buscar subdominios si otros vectores no dan fruto.
