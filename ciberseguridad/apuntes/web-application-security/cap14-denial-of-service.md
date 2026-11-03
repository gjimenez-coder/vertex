# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 14 — Denial of Service (Denegación de servicio)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

El capítulo cubre los ataques de denegación de servicio (DoS), cuya forma más conocida y publicitada es el DDoS (distributed denial of service), donde una gran red de dispositivos inunda un servidor con peticiones hasta ralentizarlo o volverlo inutilizable para los usuarios legítimos. Pero el DoS abarca mucho más: desde la versión distribuida con miles de dispositivos coordinados, hasta DoS a nivel de código que afecta a un solo usuario por una implementación defectuosa de regex.

La tesis es que cualquier esfuerzo automatizado que degrade o impida la usabilidad de una aplicación web puede considerarse DoS, sin importar su origen. Los ataques varían en gravedad: desde reducir un servidor activo, pasar por una factura eléctrica inútil, hasta hacer que una página cargue algo más lento o pausar un vídeo a mitad de buffer. Esta amplitud hace que probar DoS sea difícil, y por eso la mayoría de programas de bug bounty prohíben directamente los envíos de DoS para evitar interferencias con el uso normal.

Sales sabiendo reconocer y construir una variedad amplia de ataques DoS comunes (regex, lógico, DDoS) y varias formas avanzadas (YoYo, compresión, basados en proxy), además de los conceptos compartidos detrás de todos ellos. Con pocas excepciones, el DoS no suele causar daño permanente, pero interfiere con la usabilidad; a veces es muy difícil encontrar el DoS sink que degrada la experiencia.

> Advertencia: conviene probar vulnerabilidades DoS en un entorno de desarrollo local donde los usuarios reales no sufran interrupciones del servicio.

## Regex DoS

Las vulnerabilidades basadas en regex DoS son de las formas más comunes de DoS en aplicaciones web actuales, con riesgo que va de muy menor a medio según dónde esté el parser de regex. Las expresiones regulares se usan para validar campos de formulario y asegurar que el usuario introduce el texto esperado.

En JavaScript, las regex se definen de dos formas, y cualquier cosa entre dos barras es un literal:

```javascript
const myregex = /username/; // literal definition
const myregex = new regexp('username'); // constructor
```

Las regex normalmente se parsean muy rápido, pero pueden construirse para correr lentamente: son las *malicious regexes* (o *evil regexes*). Son un riesgo grande cuando se permite que los usuarios aporten sus propias expresiones, y también pueden introducirse por accidente. La mayoría se forman con el operador `+`, que convierte la operación en "greedy" (busca una o más coincidencias en lugar de parar en la primera).

Una regex maliciosa provoca *backtracking* al encontrar un caso de fallo. Ejemplo: `/^((ab)*)+$/`. Con la entrada `abab` corre rápido; con `ababababababab` también. Pero al añadir una `a` extra (`abababababababa`) evalúa lento, porque la regex es válida hasta el final y el motor retrocede probando combinaciones:

```
(abababababababa) is not valid.
(ababababababa)(ba) is not valid.
(abababababa)(baba) is not valid.
```

El motor intenta exhaustivamente todas las combinaciones válidas de `(ab)`, completando un número de combinaciones igual a la longitud de la cadena antes de determinar que no es válida. En la Tabla 14-1, con `/^((ab)*)+$/`, el tiempo se duplica cada dos caracteres añadidos (8 ms a 23 chars, 15 ms a 25, 31 ms a 27, 61 ms a 29). Esto acaba causando reducción significativa de rendimiento en el servidor (si se computa en servidor) o crashea totalmente el navegador (si se computa en cliente).

La regex no es vulnerable a todas las entradas (Tabla 14-2): cadenas de longitud par de `ababab...` de hasta 26 caracteres tardan <1 ms (con 28 caracteres ya tardan >1 ms). Esto significa que una regex maliciosa puede permanecer latente durante años hasta que un hacker encuentra la entrada que provoca backtracking significativo, apareciendo "de la nada". El OSS suele ser más vulnerable, ya que pocos desarrolladores detectan regex maliciosas.

## Logical DoS Vulnerabilities (vulnerabilidades de DoS lógico)

En el DoS lógico, los recursos del servidor son drenados por un usuario ilegítimo, causando degradación o pérdida de servicio para los legítimos. Son de las más difíciles de encontrar y explotar, pero aparecen más de lo esperado; requieren cierta pericia.

Primero hay que pensar qué hace funcionar un DoS: consumir recursos de hardware (servidor o cliente) dejándolos no disponibles. Por eso se buscan operaciones intensivas en recursos. Lista no exhaustiva:

- Cualquier operación que confirmes que opera de forma síncrona
- Escrituras en base de datos
- Escrituras en disco
- SQL joins
- Backups de archivos
- Operaciones lógicas en bucle

Las llamadas API complejas suelen contener varias de estas. Ejemplo: una app de fotos con una ruta de subida puede hacer escritura en base de datos (metadatos), escritura en disco (log de subida), SQL join (datos de usuario y álbumes) y file backup.

No se puede cronometrar fácilmente estas operaciones en un servidor sin acceso, pero se combina timing y estimación. Se cronometra la petición de principio a fin con las developer tools del navegador. Se prueba si una operación es síncrona haciendo la misma petición varias veces a la vez y viendo si las respuestas llegan escalonadas; conviene promediar unas cien llamadas API para que las métricas no se vean alteradas por diferencias aleatorias (picos de tráfico, cron jobs).

También se aproxima la estructura del backend analizando payloads de red y la UI. Si la app soporta objetos User, Album (user HAS album), Photo (album HAS photos) y Metadata (photos HAVE metadata), cada hijo se referencia por un ID. Pidiendo todos los metadatos asociados a un usuario sabemos que corre un join complejo o consulta iterativa en el backend, por ejemplo en `GET /metadata/:userid`.

La escala varía según el uso (Tabla 14-3): cuenta nueva (1 álbum, 1 foto) 120 ms; cuenta media (6 álbumes, 60 fotos) 470 ms; power user (28 álbumes, 490 fotos) 1.870 ms. Deducimos que se puede crear un perfil que consuma tiempo de recursos: con un script cliente que resuba imágenes similares se puede tener una cuenta de 600 álbumes y 3.500 fotos, y luego lanzar peticiones repetidas contra el endpoint para reducir el rendimiento de otros. Aunque el servidor dé timeout, la base de datos probablemente seguiría coordinando recursos. Estos ataques difieren según la lógica de cada aplicación, de ahí el nombre "DoS lógico".

## Distributed DoS

Con DDoS, los recursos del servidor son drenados por un gran número de usuarios ilegítimos que piden en masa, pudiendo incluso realizar peticiones estándar; a escala ahogan los recursos para los legítimos. Queda algo fuera del alcance del libro, pero conviene conocerlo conceptualmente. A diferencia del DoS de un solo hacker, el ataque distribuido involucra múltiples atacantes: otros hackers o bots en red (botnets).

En teoría los bots podrían explotar cualquier DoS a mayor escala (p. ej. varios clientes enviando payloads de regex maliciosos al mismo endpoint). En la práctica, la mayoría de DDoS no usan DoS lógico ni de regex, sino que atacan a un nivel más bajo (nivel de red, no de aplicación), haciendo peticiones directas contra la IP del servidor. Suelen ser tráfico User Datagram Protocol (UDP) para ahogar el ancho de banda disponible.

Las botnets no suelen ser dispositivos de un solo hacker, sino equipos de personas reales tomados vía malware distribuido en internet, controlables remotamente. Esto dificulta detectar a los clientes ilegítimos (¿son usuarios reales?). Si se obtiene o simula una botnet para pruebas, conviene probar ataques a nivel de red y de aplicación. Cualquier DoS que corra contra un servidor es vulnerable a DDoS; generalmente el DDoS no es efectivo contra un solo cliente.

## Advanced DoS (DoS avanzado)

Existen muchas formas oscuras y menos comunes. Cualquier esfuerzo automatizado que degrade o impida la usabilidad de una app web es DoS, sea cual sea su origen.

### YoYo Attacks (ataques YoYo)

Método más moderno que aprovecha las funciones de autoescalado de grandes proveedores cloud como AWS o GCP. El autoscaler usa recursos limitados (poco CPU/RAM) cuando hay poco tráfico, ahorrando coste, y aumenta recursos automáticamente cuando sube la carga (con su correspondiente factura). El atacante inunda la app con muchas peticiones en poco tiempo para invocar el escalado; luego el tráfico se detiene de golpe, el proveedor empieza a reducir recursos, y al volver a la línea base el atacante lanza otra oleada. Se repite una y otra vez. Esto degrada la experiencia del usuario durante las reasignaciones de hardware y provoca un aumento de costes de hosting, que pueden ser significativos en periodos largos.

### Compression Attacks (ataques de compresión)

Las apps que permiten subir archivos suelen ser vulnerables a DoS de capa de aplicación con archivos malformados. Ejemplo: un sitio tipo YouTube acepta vídeos y los pasa por un compresor/optimizador (p. ej. FFMPEG) antes de servirlos. Durante la compresión hay que parsear el archivo crudo, y un vídeo cuidadosamente construido puede consumir muchos recursos del servidor, degradando la experiencia de todos.

Cada vez más común al depender de datos enviados por usuarios. Por ejemplo, CVE-2021-38094 describe un ataque contra el FFMPEG open source (versión 4.1): un vídeo con datos fuera de los límites esperados dispara un integer overflow en la función `filter_sobel()` del archivo `libavfilter/vf_convolution.c`, lo que lleva a muy alto consumo de CPU y memoria y posible crash del proceso FFMPEG. Son difíciles de encontrar porque muchas apps dependen de software de terceros como FFMPEG e ImageMagick, que simplifican el manejo de archivos complejos pero exponen una superficie amplia para payloads malformados.

### Proxy-Based DoS (DoS basado en proxy)

El DoS suele requerir recursos de cómputo significativos (y coste) del atacante. Algunos atacantes buscan robar recursos de cómputo de aplicaciones legítimas y redirigir sus peticiones al objetivo, reduciendo coste y dificultando identificar al causante.

Ejemplo: motores de búsqueda como Google, Bing o Yahoo! tienen enormes recursos dedicados a rastrear y cachear datos de sitios nuevos. Los desarrolladores suelen permitir (allowlist) a los crawlers en su `robots.txt` para ser indexados. Como estos crawlers tienen muchos recursos de salida, a veces se puede "engañar" al crawler para que empuje demasiadas peticiones de rastreo hacia un objetivo. Usando dominios y subdominios nuevos que hacen de proxy hacia la app objetivo, un hacker engaña a los crawlers para indexar el mismo contenido una y otra vez; escalado a miles o millones de subdominios, degrada el rendimiento sin pagar los recursos uno mismo. El autor denomina a esto *proxy-based DoS*, porque usa un servicio intermediario (como un buscador) para enviar tráfico al objetivo.

## Summary (resumen)

Los DDoS clásicos son con diferencia la forma más común, pero son solo uno de muchos ataques que buscan consumir recursos del servidor. El DoS puede ocurrir en muchas capas del stack: cliente, servidor y a veces la capa de red. Puede afectar a un usuario o a muchos, y el daño va de rendimiento reducido al bloqueo total de la aplicación. Al buscar DoS, conviene investigar qué recursos del servidor son más valiosos y luego buscar APIs que los usen; el valor varía entre aplicaciones (RAM/CPU, o funcionalidad en cola). Aunque suelen causar molestia o interrupción, algunos DoS pueden filtrar datos: hay que vigilar logs y errores que aparezcan a raíz de los intentos.

## Ideas clave

- DoS es cualquier esfuerzo automatizado que degrada o impide la usabilidad de una app web; abarca desde un solo usuario hasta el bloqueo total, en cliente, servidor o red.
- Regex DoS: las *malicious/evil regexes* (a menudo con el operador greedy `+`) provocan backtracking exponencial; `/^((ab)*)+$/` duplica su tiempo cada dos caracteres añadidos.
- Una regex maliciosa puede quedar latente años hasta que aparece la entrada que dispara el backtracking; el OSS es especialmente vulnerable.
- DoS lógico: se identifican operaciones intensivas (escrituras en BD/disco, SQL joins, backups, bucles) y se escalan perfiles de usuario para drenar recursos, p. ej. `GET /metadata/:userid`.
- DDoS usa múltiples atacantes o botnets (equipos reales infectados por malware); en la práctica ataca a nivel de red (tráfico UDP contra la IP) más que a nivel de aplicación.
- YoYo attacks explotan el autoescalado de la nube (AWS, GCP) con oleadas intermitentes que degradan el servicio e inflan los costes de hosting.
- Ataques de compresión abusan de parsers de archivos de terceros como FFMPEG o ImageMagick (ver CVE-2021-38094, integer overflow en `filter_sobel()`).
- Proxy-based DoS "engaña" a crawlers de buscadores vía subdominios que hacen proxy para que indexen el mismo contenido repetidamente y degraden el objetivo sin coste propio.
