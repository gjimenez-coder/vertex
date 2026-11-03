# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 33 — Defending Data and Objects (Defendiendo datos y objetos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo cierra el bloque sobre ataques a datos y objetos mostrando que, aunque son un blanco frecuente, en realidad son bastante sencillos de defender. La tesis central es que la mayoría de las mitigaciones son accesibles y de bajo coste siempre que se diseñe la aplicación teniendo en cuenta estos riesgos desde el principio.

El autor parte de una observación técnica: fuera del almacenamiento en base de datos, los objetos con los que interactúa el código viven de forma efímera (en memoria) o persistente (en el sistema de archivos). Como los lenguajes operan principalmente en memoria, los datos persistentes suelen cargarse en memoria durante las operaciones; por eso muchas defensas pensadas para datos efímeros también protegen los datos en disco.

Sales sabiendo cómo mitigar cuatro clases concretas de ataque: mass assignment, IDOR, ataques de serialización, y con ello por qué una buena arquitectura y el uso de librerías sólidas bastan en la mayoría de los casos.

## Defending Against Mass Assignment (defensa contra mass assignment)
Los ataques de mass assignment son relativamente fáciles de prevenir si se piensa en seguridad al programar. El ejemplo del capítulo es un endpoint de API del videojuego "MegaGame" que confía ciegamente en los datos enviados por el cliente:

```javascript
app.post("updatePlayerData", function(req, res, next) {
  // if client sent back player state data, update in the database
  if (!!req.body.data) {
    db.update(session.currentUser, req.body.data);
    return res.sendStatus(200); // success
  } else {
    return res.sendStatus(400); // error
  }
});
```

La vulnerabilidad existe porque el desarrollador actualiza campos de la base de datos a partir de un objeto que un usuario malicioso puede manipular. Hay dos defensas generalmente aceptadas.

### Validation and Allowlisting (validación y allowlist)
El método más sencillo es restringir los campos aceptados del cliente mediante un allowlist, aplicado como validación antes de llamar a `db.update()`. Así se garantiza que no se pueda asignar por error el campo `admin`:

```javascript
const allowlist = ["hp", "location"]; // only allow these two fields to be updated
```

### Data Transfer Objects (objetos de transferencia de datos)
Una mitigación más intensiva es crear un objeto intermediario llamado Data Transfer Object (DTO), usado al pasar datos entre servicios o llamadas de función:

```javascript
const DTO = function(hp, location) {
  this.hp = hp;
  this.location = location;
};
```

Al pasar todos los datos entrantes por el constructor del DTO, cualquier parámetro adicional es rechazado, evitando que datos maliciosos lleguen a `db.update()`.

## Defending Against IDOR (defensa contra IDOR)
La primera defensa es una buena arquitectura: los objetos y archivos nunca deberían referenciarse directamente ni mediante una estructura de API fácil de adivinar. Cuando un usuario necesita acceder a un archivo concreto, la solución recomendada combina enmascarar la llamada de API (para no mostrar el nombre del archivo) con comprobaciones de autorización antes de devolver cada archivo.

Donde eso no sea posible, usar nombres de archivo y referencias generados aleatoriamente puede aportar seguridad, pero solo si existen otros mecanismos (como rate limits) y la entropía es suficiente para que hagan falta millones de intentos para encontrar otro archivo. El propio autor lo califica como una mitigación a corto plazo, no la solución ideal, hasta que sea posible una re-arquitectura a largo plazo.

## Defending Against Serialization Attacks (defensa contra ataques de serialización)
En el núcleo de todo ataque de serialización hay una serialización débil, por lo que la mitigación principal es usar librerías de serialización y deserialización sólidas y bien probadas. Para aplicaciones web conviene elegir una librería open source con millones de usuarios e historial de auditorías de seguridad, un formato popular como JSON o YAML, y evitar formatos con poco o ningún historial.

También hay que considerar el tipo de dato a serializar: los datos que el servidor o el navegador pudieran interpretar como script, o que contengan caracteres de escape comunes, deben sanitizarse antes de serializar o deserializar. Es posible aplicar allowlist a los caracteres de entrada y a los tipos de objeto para reducir el riesgo si el serializador no los maneja.

## Summary (resumen)
Aunque existen ataques contra objetos y datos complejos y parezcan un fallo de los lenguajes de la web, suelen ser fáciles de defender. Diseñar la aplicación con estos ataques en mente y entender los riesgos debería dar tranquilidad, porque las mitigaciones están al alcance.

## Ideas clave
- Fuera de la base de datos, los objetos viven en memoria (efímeros) o en el sistema de archivos (persistentes); muchas defensas sirven para ambos.
- Mass assignment nace de confiar en el objeto enviado por el cliente para actualizar campos de la base de datos.
- Allowlist: restringir los campos aceptados antes de escribir en la base de datos es la mitigación más simple contra mass assignment.
- Un Data Transfer Object (DTO) rechaza parámetros adicionales al pasar los datos por su constructor.
- Contra IDOR: nunca referenciar objetos directamente; enmascarar la API y validar autorización antes de devolver cada archivo.
- Nombres aleatorios con suficiente entropía y rate limits son solo una mitigación a corto plazo frente a IDOR.
- Toda serialización débil es la raíz del ataque; usar librerías open source auditadas y formatos probados como JSON o YAML.
- Sanitizar o aplicar allowlist a caracteres y tipos de objeto que pudieran interpretarse como script antes de serializar o deserializar.
