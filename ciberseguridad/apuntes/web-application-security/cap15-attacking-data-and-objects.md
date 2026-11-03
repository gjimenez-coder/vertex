# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 15 — Attacking Data and Objects (Atacando datos y objetos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber

Los lenguajes de programación modernos separan dos capacidades: los datos, representados normalmente como objetos, y las acciones, representadas como funciones. Casi todos definen los objetos (datos) como *first-class citizen* (ciudadanos de primera clase), es decir, entidades que pueden asignarse, reasignarse, modificarse, pasarse como argumento y devolverse desde una función. No todos los lenguajes tratan las funciones (acciones) como ciudadanos de primera clase, por lo que la mayoría divide en dos features distintas el almacenamiento de datos y la operación sobre ellos.

El capítulo trata los métodos para explotar datos mientras se almacenan como objetos y se operan mediante funciones. Estas técnicas funcionan contra múltiples lenguajes modernos y abusan de los potentes efectos secundarios de almacenar datos como ciudadanos de primera clase. Sales sabiendo reconocer y explotar tres clases de ataque: mass assignment, IDOR, y los ataques de serialización (serialization attacks).

La tesis central es que, pese a la evolución de la web, los lenguajes siguen usando patrones de diseño antiguos; al entender los sistemas subyacentes de una aplicación compleja se vuelve evidente cómo explotarlos a nivel fundamental.

## Mass Assignment

El método más común de atacar objetos de primera clase. También se conoció históricamente como *autobinding attack* (en frameworks Spring MVC y ASP.NET) y como *object injection attack* (en vulnerabilidades legacy de PHP); todos los términos refieren al mismo sistema de explotación.

La vulnerabilidad permite al atacante cambiar campos que no estaban destinados a cambiarse, pasando campos adicionales dentro de un objeto a una llamada de función que no valida las claves (keys). Aparecen típicamente en sistemas que mueven mucho estado en forma de objetos de una función a otra: por ejemplo un videojuego que pasa el estado del usuario constantemente, o una aplicación web con *dynamic forms* cuyo título o tipo de dato puede cambiar el usuario final.

Ejemplo: un endpoint `updatePlayerData` recibe un objeto de estado del cliente y lo guarda con un helper de base de datos:

```javascript
app.post("updatePlayerData", function(req, res, next) {
 if (!!req.body.data) {
   db.update(session.currentUser, req.body.data);
   return res.sendStatus(200); // success
 } else {
   return res.sendStatus(400); // error
 }
});
```

La función `update()` hace upsert de los datos del cliente sin validar las claves del objeto:

```javascript
const update = function(data) {
 for (const [key, value] of Object.entries(data)) {
   database.upsert({ `${key}`: `${value}` })
 }
}
```

El desarrollador asume un payload con `playerId`, `playerPosition` y `playerHP`. Como no hay validación, el atacante añade una clave extra:

```javascript
const data = {
 playerId: 123,
 playerPosition: { "x": 125, "y": 346 },
 playerHP: 90,
 isAdmin: true // this is the "attack" portion of the payload
};
```

Al incluir `isAdmin`, la función escribe/modifica esa entrada en la fila del usuario y este eleva su rol a admin. Si `update()` hubiera validado las claves y saneado `isAdmin`, no se habría producido la actualización de rol. Es una de las vulnerabilidades de objeto más comunes y fáciles de explotar.

## Insecure Direct Object Reference (IDOR)

IDOR es una vulnerabilidad web común que se destacó en 2007 al añadirse a la lista OWASP top 10. Desde entonces es menos frecuente, pero por su naturaleza simple aún aparece y requiere muy poca habilidad para explotarse.

Ocurre cuando los objetos de un servidor son directamente accesibles mediante parámetros proporcionados por el usuario: parámetros de query de la URL, cuerpo de un HTTP POST o campos `:id` de la URL. Confiar en que el usuario suministre los parámetros correctos hace muy probable que otros objetos queden accesibles, llevando a privilege escalation.

```javascript
app.get('/files/:id', function(req, res, next) => {
  return res.sendFile(`/filesystem/files/${req.params.id}`);
});
```

Este endpoint devuelve cualquier archivo bajo `/filesystem/files` según el nombre en `:id`. El desarrollador espera que el usuario descargue, por ejemplo, `my-report-card.txt`:

```
HTTP GET https://mywebsite.com/files/my-report-card.txt
```

El ataque es simple: interceptar la petición en el navegador y cambiar el nombre de archivo, o usar un HTTP proxy como Burp Suite o ZAP. Si se cambia a `other-report-card.txt`, el servidor lo envía aunque el usuario no debería acceder a él. Por eso IDOR es una forma de privilege escalation además de un ataque contra objetos vía referencias de objeto.

## Serialization Attacks

Cuando los datos viajan entre clientes de navegador, servidores y servicios, enviarlos en formato crudo suele ser impráctico, caro y difícil. Por eso muchas aplicaciones serializan los datos crudos antes de enviarlos por la red.

### Web Serialization Explained

El concepto clave es que el formato serializado debe ser fácil de deserializar (revertir a datos crudos) y de almacenar en disco. Un ejemplo es tomar un objeto en memoria del contexto de ejecución JavaScript del navegador y convertirlo a JSON:

```json
{
  "name": "Joe Carrot",
  "age": 62,
  "location": "Montana, USA",
  "crops": {
    "wheat": {
      "measurement": "acres",
      "amount": 100
    }
  }
}
```

Este "blob" JSON del granjero "Joe Carrot" puede guardarse en disco o transferirse por red, y cuando se requiere se deserializa y carga en memoria, creando nuevas direcciones y punteros. Otros formatos populares de serialización son XML, YAML y base64 (formato para serializar texto en binario).

### Attacking Weak Serialization

El primer paso es encontrar una función que realice serialización en la aplicación; el siguiente, usarla con datos de prueba para comparar entrada y salida de un conjunto de funciones de serialización.

Ejemplo real: la librería npm `serialize-javascript` (más de 30 millones de descargas semanales). Las versiones 3.0.9 e inferiores eran vulnerables a code injection usando su función `serialization()` como mecanismo de entrega de un payload.

El payload `{"foo": /1"/, "bar": "a\"@__R-<UID>-0__@"}` producía el JSON serializado `{"foo": /1"/, "bar": "a\/1"/}`. La estructura resultante escapa comillas (parte esperada de un JSON válido) y crea ejecución de código si pasa alguna vez por `eval()`.

```javascript
eval('('+ serialize({"foo": /1" + console .log(1) /i, "bar": '"@__R-<UID>-0__@'}) + ')');
```

Todos los ataques de serialización siguen los mismos pasos:

1. Encontrar una función que realice serialización.
2. Leer la función con cuidado o probarla con payloads comunes.
3. Tras hallar un fallo al serializar, crear un payload capaz de ejecutar script.
4. Llamar a la función con ese payload.
5. Obtener remote code execution (servidor) o XSS (cliente).

Como la mayoría de sitios no implementan sus propios serializadores, se pueden encontrar serializadores open source vulnerables y escanear aplicaciones y métodos vulnerables. Es una técnica avanzada, pero una de las mejores formas de hallar y explotar vulnerabilidades de serialización en el mundo real.

## Ideas clave

- Los objetos son *first-class citizens* en casi todos los lenguajes modernos; atacar datos y objetos abusa de ese diseño fundamental.
- Mass assignment: pasar claves extra (p. ej. `isAdmin: true`) a funciones que no validan las claves del objeto; se mitiga validando y saneando las keys.
- IDOR: objetos accesibles directamente vía parámetros del usuario (query, POST body, `:id`); lleva a privilege escalation. Entró en el OWASP top 10 en 2007.
- Herramientas de interceptación como Burp Suite o ZAP facilitan explotar IDOR cambiando parámetros antes de que lleguen al servidor.
- La serialización convierte datos crudos a formatos transferibles/almacenables (JSON, XML, YAML, base64) y debe poder deserializarse fácilmente.
- Un serializador débil que no escapa correctamente las comillas puede derivar en code injection vía `eval()`, con RCE en servidor o XSS en cliente.
- Los ataques de serialización siguen cinco pasos: localizar la función, analizarla/probarla, crear el payload, invocarlo y obtener ejecución de código.
- Los lenguajes web siguen usando patrones de diseño antiguos, por lo que los sistemas subyacentes siguen siendo blancos viables pese a décadas de mejoras.
