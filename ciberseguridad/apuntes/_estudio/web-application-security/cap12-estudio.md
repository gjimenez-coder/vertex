# XML External Entity (Entidad externa XML) — Estudio

## Tarjetas de repaso

P: ¿Qué es un ataque XXE y de qué depende? / R: Es el ataque XML External Entity, a menudo simple de ejecutar pero devastador; depende de un parser XML mal configurado dentro del código de una aplicación.

P: ¿Dónde aparecen casi todas las vulnerabilidades XXE? / R: En un endpoint de API que acepta un payload XML o similar a XML.

P: ¿Qué formatos tipo XML pueden aceptar los parsers como entrada? / R: SVG, HTML/DOM, PDF (XFDF) y RTF, porque comparten características con la especificación XML.

P: ¿Qué son las XML entities? / R: Conjuntos de caracteres que referencian otro dato dentro del archivo XML o de la especificación.

P: ¿Qué diferencia hay entre predefined entities y custom entities? / R: Las predefined siempre referencian el mismo carácter ASCII (como `&amp;` o `&lt;`); las custom las define el programador y pueden referenciar datos fuera del documento XML actual.

P: ¿Qué es una external entity reference y por qué es el núcleo de XXE? / R: Es una referencia a una entidad externa dentro del DTD que permite incorporar archivos externos antes del parseo; es la forma más peligrosa.

P: ¿Cómo se escribe una entidad que referencia /etc/passwd? / R: `<!DOCTYPE foo [ <!ENTITY ext SYSTEM "file:///etc/passwd"> ]>`.

P: ¿En qué consiste el XXE directo? / R: Se envía al servidor un objeto XML con un flag de entidad externa; se parsea y se devuelve un resultado que incluye la entidad externa.

P: ¿En qué consiste el XXE indirecto? / R: El servidor genera un objeto XML que incluye parámetros del usuario (p. ej. para sincronizar con un CRM/SOAP legacy que espera XML), de modo que puede terminar incluyendo una etiqueta de entidad externa aunque la API pública no acepte XML.

P: ¿Cuándo se recurre a la exfiltración out-of-band y cómo se hace? / R: Cuando la vulnerabilidad XXE no devuelve datos; se exfiltra durante el parseo, más fácilmente vía FTP (también Gopher en legacy, o HTTP/LDAP), usando un DTD alojado en el servidor del atacante.

P: ¿Qué indica el campo 2 de /etc/passwd? / R: La ubicación de almacenamiento de la contraseña; una `x` indica que el hash está en /etc/shadow.

P: ¿Qué algoritmo revela cada prefijo `$id` en /etc/shadow? / R: `$1$` MD5, `$2a$` y `$2y$` Blowfish, `$5$` SHA-256, `$6$` SHA-512, `$y$` yescrypt.

P: ¿Qué herramientas se usan para crackear hashes y por qué hace falta unshadow? / R: John the Ripper y Hashcat; como no aceptan /etc/shadow y /etc/passwd sin formato, se combinan con `unshadow`.

P: ¿Cuál es la defensa típica contra XXE? / R: A menudo basta una sola línea de configuración que deshabilite las entidades externas; debe probarse siempre en aplicaciones nuevas.

## Preguntas de autoevaluación

P: ¿Por qué un endpoint que no parece aceptar XML puede seguir siendo vulnerable a XXE? / R: Porque formatos como SVG, HTML/DOM, XFDF o RTF comparten características con XML y muchos parsers los aceptan; además, el servidor puede convertir datos del usuario a XML para sistemas legacy. (Secciones "Lo que necesitas saber" e "Indirect XXE")

P: En el ejemplo de MegaBank, ¿por qué el atacante puede inyectar su propio XML? / R: Porque el DOM que envía el cliente es modificable o se puede forjar la petición de red directamente, y el XML debe pasar por un parser XML para convertirse en JPG. (Sección "El ejemplo que recorre el capítulo")

P: ¿Qué condición del parser hace que el contenido de /etc/passwd aparezca en la captura devuelta en XXE directo? / R: Que el parser no deshabilite explícitamente las entidades externas. (Sección "Direct XXE")

P: ¿Cómo se puede detectar un posible XXE indirecto sin información interna? / R: Investigando los acuerdos de licencia de software empresarial (a veces públicos), revisando si datos se presentan vía sistemas o URLs ajenas, y conociendo los formatos que esperan los paquetes heredados (CRM, contabilidad, RRHH). (Sección "Indirect XXE")

P: ¿Cómo logra el payload out-of-band extraer /etc/passwd? / R: El payload referencia un DTD alojado en el servidor del atacante; con FTP habilitado, el servidor objetivo solicita ese DTD, que transmite el contenido de /etc/passwd línea por línea vía FTP a los logs del atacante. (Sección "Out-of-Band Data Exfiltration")

P: ¿Cuáles son los pasos del flujo de account takeover en Linux? / R: Obtener /etc/passwd, luego los hashes de /etc/shadow, identificar el algoritmo por el `$id`, crackear el hash con John the Ripper/Hashcat (usando unshadow) y finalmente iniciar sesión vía SSH con el usuario comprometido. (Sección "Account Takeover Workflow")

P: ¿Qué diferencia hay entre John the Ripper y Hashcat respecto al hardware? / R: John the Ripper usa GPU o CPU, pero no ambas a la vez; Hashcat puede usar ambas. (Sección "Account Takeover Workflow")

## Checklist

- Verificar en cada endpoint de API si acepta XML o formatos tipo XML (SVG, HTML/DOM, XFDF, RTF).
- Deshabilitar explícitamente las entidades externas en la configuración del parser XML.
- Probar siempre esta configuración en aplicaciones nuevas, dado lo simple que es la corrección.
- Revisar integraciones con sistemas legacy (CRM, SOAP) donde el servidor convierte datos del usuario a XML.
- Considerar vectores out-of-band (FTP, Gopher, HTTP, LDAP) al evaluar exposición aunque la respuesta no devuelva datos.
- Proteger archivos core de autenticación/autorización (/etc/passwd, /etc/shadow) frente a lecturas por el parser.
