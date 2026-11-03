# Attacking Data and Objects (Atacando datos y objetos) — Estudio

## Tarjetas de repaso

P: ¿Qué es un *first-class citizen* en un lenguaje de programación? / R: Una entidad (normalmente un objeto/dato) que puede asignarse, reasignarse, modificarse, pasarse como argumento y devolverse desde una función.

P: ¿Por qué la mayoría de lenguajes separa datos y acciones en dos features distintas? / R: Porque casi todos tratan los objetos (datos) como ciudadanos de primera clase, pero no todos tratan las funciones (acciones) de igual modo, así que dividen el almacenamiento de datos y la operación sobre ellos.

P: ¿Qué tres clases de ataque enseña el capítulo? / R: Mass assignment, IDOR (Insecure Direct Object Reference) y los ataques de serialización (serialization attacks).

P: ¿Qué es un ataque de mass assignment? / R: Pasar campos/claves adicionales dentro de un objeto a una función que no valida las claves, logrando cambiar campos que no estaban destinados a cambiarse.

P: ¿Con qué otros nombres se ha conocido históricamente el mass assignment? / R: Autobinding attack (en Spring MVC y ASP.NET) y object injection attack (en vulnerabilidades legacy de PHP).

P: ¿Cómo se explota el ejemplo `updatePlayerData`? / R: El atacante añade una clave extra como `isAdmin: true` al objeto de estado; como `update()` no valida las claves, se escribe esa entrada y el usuario eleva su rol a admin.

P: ¿Cómo se mitiga el mass assignment? / R: Validando y saneando las claves (keys) del objeto antes de operar sobre ellas.

P: ¿Qué es IDOR? / R: Una vulnerabilidad donde los objetos del servidor son directamente accesibles mediante parámetros proporcionados por el usuario (query de la URL, cuerpo POST o campos `:id`).

P: ¿Cuándo destacó IDOR y qué consecuencia principal tiene? / R: Se destacó en 2007 al añadirse al OWASP top 10; conduce a privilege escalation.

P: ¿Cómo se explota un IDOR en la práctica? / R: Interceptando la petición en el navegador o con un HTTP proxy como Burp Suite o ZAP, y cambiando el parámetro (p. ej. el nombre de archivo en `:id`).

P: ¿Qué es la serialización y qué propiedad debe cumplir el formato serializado? / R: Convertir datos crudos a un formato transferible/almacenable; debe ser fácil de deserializar (revertir a datos crudos) y de almacenar en disco.

P: ¿Qué formatos de serialización menciona el capítulo? / R: JSON, XML, YAML y base64 (formato para serializar texto en binario).

P: ¿Cómo puede un serializador débil derivar en ejecución de código? / R: Si no escapa correctamente las comillas, puede crear ejecución de código cuando el resultado pasa por `eval()`, logrando RCE en servidor o XSS en cliente.

P: ¿Qué librería real se cita como vulnerable y en qué versiones? / R: La librería npm `serialize-javascript` en versiones 3.0.9 e inferiores, vulnerable a code injection a través de su función de serialización.

P: ¿Cuáles son los cinco pasos de un ataque de serialización? / R: 1) Encontrar la función que serializa; 2) leerla/probarla con payloads comunes; 3) crear un payload que ejecute script; 4) invocar la función con ese payload; 5) obtener RCE (servidor) o XSS (cliente).

## Preguntas de autoevaluación

P: ¿Por qué atacar datos y objetos abusa de un diseño fundamental de los lenguajes modernos? / R: Porque los objetos son ciudadanos de primera clase, lo que les da potentes efectos secundarios (asignación, modificación, paso como argumento) que se pueden explotar a nivel fundamental. (Sección "Lo que necesitas saber")

P: En el ejemplo del videojuego, ¿qué fallo concreto del código permite el mass assignment? / R: La función `update()` hace upsert de todas las claves del objeto cliente sin validar ni sanear las keys, por lo que acepta `isAdmin`. (Sección "Mass Assignment")

P: ¿Por qué IDOR se considera una forma de privilege escalation? / R: Porque confiar en los parámetros del usuario permite acceder a objetos que no le corresponden (p. ej. el archivo de otro usuario), obteniendo acceso por encima de sus privilegios. (Sección "Insecure Direct Object Reference (IDOR)")

P: ¿Qué papel juega una herramienta como Burp Suite o ZAP en la explotación de IDOR? / R: Permite interceptar y modificar la petición antes de que llegue al servidor para cambiar el parámetro directo al objeto. (Secciones "IDOR" e "Ideas clave")

P: ¿Para qué se serializan los datos antes de enviarlos por la red? / R: Porque enviar los datos crudos suele ser impráctico, caro y difícil; serializarlos facilita su transferencia y almacenamiento, y luego se deserializan en memoria. (Sección "Serialization Attacks" / "Web Serialization Explained")

P: ¿Qué hace exactamente el payload vulnerable de `serialize-javascript`? / R: Escapa comillas (parte esperada de un JSON válido) de forma que, si el resultado pasa por `eval()`, se produce ejecución de código. (Sección "Attacking Weak Serialization")

P: ¿Por qué los ataques de serialización suelen apuntar a serializadores open source? / R: Porque la mayoría de sitios no implementan sus propios serializadores, así que se buscan serializadores open source vulnerables y se escanean aplicaciones y métodos que los usen. (Sección "Attacking Weak Serialization")

P: ¿Cuál es la tesis central del capítulo sobre los patrones de diseño web? / R: Que los lenguajes web siguen usando patrones de diseño antiguos, por lo que los sistemas subyacentes siguen siendo blancos viables pese a décadas de mejoras. (Secciones "Lo que necesitas saber" e "Ideas clave")

## Puntos a dominar

- Distinguir las tres clases de ataque del capítulo: mass assignment, IDOR y ataques de serialización, y qué las diferencia.
- Explicar qué es un first-class citizen y por qué habilita estos ataques.
- Reconocer un endpoint vulnerable a mass assignment y saber que la defensa es validar y sanear las claves del objeto.
- Identificar referencias directas a objetos vía parámetros de usuario (query, POST body, `:id`) como posibles IDOR y asociarlo a privilege escalation y al OWASP top 10 (2007).
- Describir qué es serializar/deserializar y nombrar los formatos citados (JSON, XML, YAML, base64).
- Comprender cómo un escape incorrecto de comillas más `eval()` deriva en RCE o XSS.
- Recitar los cinco pasos de un ataque de serialización y relacionarlos con el caso de `serialize-javascript` (≤ 3.0.9).
