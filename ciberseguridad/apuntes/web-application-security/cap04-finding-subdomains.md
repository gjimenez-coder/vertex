# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 4 — Finding Subdomains (Encontrar subdominios)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber

Antes de probar los endpoints de una API conviene conocer la estructura de dominios que usa la aplicación. Hoy es raro que un único dominio sirva toda una aplicación web: lo habitual es separar cliente y servidor en dominios distintos, además del clásico `https://www` frente al dominio pelado. Encontrar y registrar de forma iterativa los subdominios que dan vida a una aplicación web es una técnica de reconocimiento (recon) útil como primer paso.

El capítulo plantea un caso guía: mapear las aplicaciones de MegaBank para una prueba de penetración de caja negra patrocinada por el banco. La app principal está en `https://www.mega-bank.com`, cuyo dominio ya está ampliamente cubierto por un programa de bug bounty, así que las vulnerabilidades fáciles ya están corregidas. La estrategia es buscar objetivos más fáciles: los subdominios que alojan servicios de correo, aplicaciones de administración, servidores de archivos y más.

Sales sabiendo varias técnicas, de las más simples a las más avanzadas, para descubrir subdominios: las herramientas de red del navegador, los registros públicos (buscadores, archivos, redes sociales), los ataques de transferencia de zona DNS, y la fuerza bruta y los ataques de diccionario con scripts en JavaScript/Node.js.

## El ejemplo que recorre el capítulo

MegaBank (`mega-bank.com`) es el objetivo hilo conductor. El objetivo es llenar un mapa de la aplicación con los subdominios asociados al dominio principal (Figura 4-1), ya que `www` apunta a la app pública en sí y suele ser menos interesante que los servicios ocultos detrás.

## Las herramientas de análisis de red del navegador

Se puede recolectar información simplemente recorriendo la funcionalidad visible de la app y observando qué peticiones a la API se hacen en segundo plano. Los navegadores modernos (Chrome, Firefox, Edge) incluyen herramientas de desarrollador muy potentes; el libro se apoya solo en el navegador, sin herramientas especializadas de pago.

En Chrome: menú de tres puntos → "More tools" → "Developer tools" → pestaña "Network". Al navegar aparecen nuevas peticiones HTTP.

- La pestaña **XHR** (dentro de Network) muestra las peticiones POST, GET, PUT, DELETE, etc., filtrando fuentes, imágenes, vídeos y dependencias.
- Al seleccionar una petición se ven versiones cruda y formateada, cabeceras y cuerpo; la pestaña **Preview** muestra el resultado formateado y **Response** el payload crudo.
- La pestaña **Timing** da métricas de cola, descarga y espera. Estas métricas pueden usarse en ataques de canal lateral (side-channel), que se apoyan en una métrica secundaria distinta de la respuesta para deducir qué código corre en el servidor.

Al navegar, se puede revisar request → headers → general → request URL para ver a qué dominio se envió una petición. A menudo eso basta para encontrar los servidores afiliados.

## Aprovechar los registros públicos

La cantidad de información pública en la web es tan enorme que una fuga accidental puede pasar desapercibida durante años. Datos que el autor dice haber encontrado en pentests: copias en caché de repos de GitHub que se hicieron públicos por error, claves SSH, claves de servicios como AWS o Stripe expuestas temporalmente, listados DNS y URLs no destinados al público, páginas de productos no lanzados, registros financieros y correos/teléfonos/usuarios.

Fuentes: motores de búsqueda, publicaciones en redes sociales, aplicaciones de archivo como archive.org, y búsquedas de imágenes (incluida la búsqueda inversa). Los subdominios que no se encuentran por diccionario pueden estar indexados en alguno de estos servicios.

### Cachés de motores de búsqueda

Google tiene operadores de búsqueda para ganar especificidad. Con `site:` se consulta solo un dominio:

```
site:mega-bank.com log in
```

El operador menos añade condiciones negativas; `-inurl:<pattern>` descarta URLs que coincidan con un patrón. Para eliminar subdominios ya conocidos como `www`:

```
site:mega-bank.com -inurl:www
```

Ojo: filtra el patrón en toda la cadena de la URL, no solo el subdominio, así que `https://admin.mega-bank.com/www` también se filtraría (falsos positivos). Se pueden encadenar negaciones para quitar subdominios expuestos a propósito que no interesan:

```
site:mega-bank.com -inurl:www -inurl:mobile
```

Probado contra `reddit.com -inurl:www`, el primer resultado es `code.reddit.com`. Conviene repetir hasta no hallar más resultados relevantes y probar también otros buscadores como Bing, que soportan operadores similares.

### Archivos accidentales

Utilidades de archivo como Archive.org guardan instantáneas periódicas de sitios (a veces de hace más de 20 años), lo que las convierte en una mina para hallar información divulgada —a propósito o por error— y luego retirada. Para datos actuales conviene un buscador; para datos históricos, un archivo web. Los subdominios suelen aparecer en archivos antiguos vía hiperenlaces que estaban en el HTML o JS pero ya no se ven en la app en vivo.

Procedimiento manual para automatizar el descubrimiento desde un archivo: abrir 10 instantáneas de 10 fechas distintas, "View source", copiar el HTML a un archivo `legacy-source.html`, repetir con las demás y buscar los esquemas de URL más comunes:

```
http://
https://
file://
ftp://
ftps://
```

### Instantáneas sociales (social snapshots)

Casi todas las grandes redes sociales ganan dinero con la venta de datos de usuario y ofrecen APIs similares. El capítulo usa la API de X (antes Twitter) como ejemplo, pero los conceptos se aplican a cualquier red.

X ofrece varias APIs según alcance y volumen. La capa gratuita de la "search API" permite revisar 30 días de tweets, con límite de 100 tweets por consulta, 30 consultas por minuto y 250 consultas mensuales totales (unos 25.000 tweets). Para consultar se necesita una cuenta de desarrollador registrada, una app registrada y un bearer token.

```
curl --request POST \
  --url https://api.twitter.com/1.1/tweets/search/30day/Prod.json \
  --header 'authorization: Bearer <MY_TOKEN>' \
  --header 'content-type: application/json' \
  --data '{
           "maxResults": "100",
           "keyword": "mega-bank.com"
           }'
```

Por defecto la búsqueda es difusa (fuzzy); para coincidencia exacta hay que enviar la cadena entre comillas dobles escapadas: `"keyword": "\"mega-bank.com\""`. Los subdominios hallados suelen venir de campañas de marketing, rastreadores de anuncios y eventos de contratación. Ejemplo real con Microsoft: `careers.microsoft.com`, `office.microsoft.com`, `powerbi.microsoft.com`, `support.microsoft.com`.

Reglas de uso de X como herramienta de recon: la **search API** da los datos más relevantes para la mayoría de apps; las apps masivas o en tendencia pueden rendir más en las APIs **streaming** (fracción muy pequeña, >99% de tweets perdidos) o **firehose** (garantiza el 100% de los tweets que cumplen el criterio); si vale la información histórica, descargar un volcado histórico y consultarlo localmente.

## Ataques de transferencia de zona (zone transfer)

Un ataque de transferencia de zona funciona contra servidores DNS mal configurados. Más que un "hack" es una técnica de recolección de información: "es solo una técnica de recolección de información que requiere poco esfuerzo" (PDF p. 108). Consiste en una petición con formato especial que simula una petición de transferencia de zona DNS legítima de un servidor DNS válido.

Los servidores DNS traducen nombres de dominio a direcciones IP. Sincronizan sus registros mediante transferencias de zona, que comparten los registros en un formato de texto llamado zone file. Estos ficheros contienen configuración DNS no destinada a ser accesible, por lo que un servidor primario bien configurado solo debería resolver transferencias solicitadas por un servidor secundario autorizado. Si no, queda vulnerable.

Primero se buscan los nameservers del dominio con el utilitario `host` (Linux y macOS recientes):

```
host -t mega-bank.com
```

Salida de ejemplo que revela `ns1.bankhost.com` y `ns2.bankhost.com`. Luego se intenta la transferencia de zona con `-l`:

```
host -l mega-bank.com ns1.bankhost.com
```

Si el servidor está mal asegurado, devuelve direcciones y subdominios (`mail.mega-bank.com`, `admin.mega-bank.com`, `internal.mega-bank.com` con sus IP), ampliando mucho la superficie de ataque. Un servidor bien configurado responde `: Transfer Failed.`. Como el ataque requiere solo unas líneas de Bash, casi siempre vale la pena intentarlo.

## Fuerza bruta de subdominios

Como última medida se puede recurrir a la fuerza bruta: probar cada combinación posible de subdominios hasta hallar coincidencias. Debe ser el último recurso porque es fácil de registrar y lenta por las limitaciones de tasa, regex y otros mecanismos.

> ADVERTENCIA: los ataques de fuerza bruta son muy fáciles de detectar y pueden hacer que registren o bloqueen tus IP (PDF p. 111).

A diferencia de una fuerza bruta local, esta requiere conectividad de red, con latencia típica de 50 a 250 ms por petición. Por eso conviene hacer las peticiones asíncronas y lanzarlas lo más rápido posible sin esperar la respuesta anterior. El bucle es simple: generar un subdominio, pedir a `<guess>.mega-bank.com`; si hay respuesta, es un subdominio vivo.

El libro usa JavaScript. Primero genera la lista de subdominios posibles:

```javascript
const generateSubdomains = function(length) {
    const charset = 'abcdefghijklmnopqrstuvwxyz'.split('');
    let subdomains = charset;
    let subdomain, letter, temp;
    // Time Complexity: o(n*m)  n = longitud, m = nº de caracteres
    for (let i = 1; i < length; i++) {
        temp = [];
        for (let k = 0; k < subdomains.length; k++) {
          subdomain = subdomains[k];
          for (let m = 0; m < charset.length; m++) {
            letter = charset[m];
            temp.push(subdomain + letter);
          }
        }
        subdomains = temp
    }
    return subdomains;
}
const subdomains = generateSubdomains(4);
```

Luego resuelve cada subdominio con la librería DNS de Node.js, usando promesas para la asincronía:

```javascript
const dns = require('dns');
const promises = [];
const subdomains = [];
subdomains.forEach((subdomain) => {
  promises.push(new Promise((resolve, reject) => {
    dns.resolve(`${subdomain}.mega-bank.com`, function (err, ip) {
      return resolve({ subdomain: subdomain, ip: ip });
    });
  }));
});
Promise.all(promises).then(function(results) {
  results.forEach((result) => {
    if (!!result.ip) { console.log(result); }
  });
});
```

Se usa `dns.resolve` en vez de `dns.lookup` porque este último se apoya en `getaddrinfo(3)`/libuv, que se implementa de forma síncrona, mientras que `dns.resolve` es realmente asíncrono. El doble `!!` descarta resultados sin IP. El resultado es una lista de subdominios vivos con sus IP (`mail`, `admin`, `dev`, `test`, `www`, `shop`, `ftp`, `forum`...).

### Ataques de diccionario

En lugar de probar todas las combinaciones, un ataque de diccionario itera sobre una lista de los subdominios más comunes. Es mucho más rápido y suele encontrar algo de interés; solo los subdominios más peculiares escapan. El escáner DNS open source **dnscan** incluye una lista de los subdominios más populares, basada en millones de subdominios de más de 86.000 registros de zona DNS. Sus top 25 incluyen `www`, `mail`, `ftp`, `localhost`, `webmail`, `smtp`, `pop`, `ns1`, `cpanel`, `test`, `blog`, `dev`, `admin`, `forum`, `news`, etc. El repositorio de dnscan en GitHub ofrece los 10.000 subdominios más comunes bajo licencia GNU v3.

Para listas grandes conviene mantener los datos separados del script y leerlos en tiempo de ejecución (normalmente en formato `.csv`):

```javascript
const dns = require('dns');
const csv = require('csv-parser');
const fs = require('fs');
const promises = [];
fs.createReadStream('subdomains-10000.txt')
  .pipe(csv())
  .on('data', (subdomain) => {
    promises.push(new Promise((resolve, reject) => {
      dns.resolve(`${subdomain}.mega-bank.com`, function (err, ip) {
        return resolve({ subdomain: subdomain, ip: ip });
      });
    }));
  })
  .on('end', () => {
   Promise.all(promises).then(function(results) {
     results.forEach((result) => {
       if (!!result.ip) { console.log(result); }
     });
   });
  });
```

Conviene empezar por el diccionario (más eficiente) y recurrir a la generación por fuerza bruta solo si el diccionario no da resultados.

## Ideas clave

- El objetivo del recon es construir un mapa de la aplicación para priorizar y desplegar payloads más adelante; buscar subdominios es un componente inicial de esa búsqueda.
- Los dominios de cara al consumidor reciben más escrutinio y se parchean rápido; los servidores "entre bastidores" (correo, admin) suelen tener más bugs por su menor uso y exposición.
- Las herramientas de red del navegador (pestaña Network/XHR) bastan a menudo para hallar servidores afiliados y endpoints de baja dificultad.
- Los registros públicos —operadores de búsqueda (`site:`, `-inurl:`), archive.org y APIs de redes sociales como la de X— revelan subdominios no descubribles por diccionario.
- La transferencia de zona DNS (`host -t`, luego `host -l`) explota servidores DNS mal configurados y puede revelar subdominios con sus IP con solo unas líneas de Bash.
- La fuerza bruta debe ser el último recurso: es fácil de detectar/registrar y lenta; conviene hacerla asíncrona y usar `dns.resolve` en vez de `dns.lookup`.
- Un ataque de diccionario (p. ej. con las listas de dnscan) es mucho más eficiente que la fuerza bruta pura.
- Ninguna técnica es completa por sí sola: hay que combinar varias y se puede volver a buscar subdominios si otros vectores no dan fruto.
