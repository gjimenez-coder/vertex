# Web Application Security (2nd Edition) — Andrew Hoffman (O'Reilly Media, 2024)
## Capítulo 31 — Defending Against Injection (Defendiéndose contra la inyección)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF (PDF p. N).

## Lo que necesitas saber

Este capítulo cierra la parte defensiva frente a los ataques de injection presentados en el Capítulo 13. La tesis central es que la inyección sigue siendo común y abarca una superficie amplia —cualquier CLI o intérprete aislado en el servidor es un objetivo potencial—, pero también es de las vulnerabilidades más fáciles de mitigar si se aplican controles adecuados. El autor organiza las defensas en tres bloques: defensas contra SQL injection, cuáles de ellas aplican a otras formas de inyección, y métodos genéricos no específicos de ningún subtipo.

El SQL injection recibe el mayor foco por ser la forma más común y, a la vez, de las más fáciles de defender: afecta potencialmente a casi toda aplicación compleja por la prevalencia de bases de datos SQL, y por ocurrir dentro del intérprete SQL su detección puede ser sencilla. Con detección y mitigación correctas, la exposición es muy baja.

Sales sabiendo cómo localizar consultas vulnerables en el código, cómo funcionan y por qué protegen las prepared statements, qué defensas específicas ofrece cada motor, y cómo aplicar principios genéricos —principle of least authority y allowlisting de comandos— para limitar el daño cuando la inyección no es solo contra SQL.

## Mitigar SQL injection

### Detectar SQL injection

El primer paso es familiarizarse con la forma del SQL injection y con las zonas más vulnerables del código. En aplicaciones modernas, las operaciones SQL ocurren pasado el nivel de enrutado del servidor, así que el cliente no interesa. Sobre una estructura típica (`/api`, `/analytics`, `/client`), se puede omitir el cliente, pero conviene revisar rutas como analytics porque suelen usar alguna base de datos. Regla útil: si los datos persisten entre dispositivos y sesiones, están en memoria del servidor, en disco (logs) o en una base de datos.

Muchas aplicaciones usan más de una base de datos (p. ej. SQL Server y MySQL), por lo que las búsquedas deben ser genéricas para encontrar consultas en varias implementaciones. Además, algún software usa un DSL que puede hacer llamadas SQL por nosotros con una sintaxis distinta a la de una llamada SQL cruda. Conviene compilar en un solo lugar la lista de DSL y tipos de SQL en uso.

En Node.js, si la librería SQL se importa por módulo, encontrar consultas es tan simple como buscar el import:

```js
const sql = require('mssql')
// OR
const mysql = require('mysql');
```

Si en cambio se declaran globalmente o se heredan de una clase padre, localizarlas se complica. Los adaptadores `mssql` y `mysql` terminan con una llamada `.query(x)`, pero otros usan una sintaxis más literal con constructores (`q.select()`, `q.from()`, `q.where()`).

### Prepared statements

Consideradas la "primera línea" de defensa contra la inyección: fáciles de implementar, bien documentadas y muy efectivas.

> "Prepared statements are often considered the 'first line' of defense against injection." (PDF p. 407)

Funcionan compilando primero la consulta con placeholders (bind variables o placeholder variables) y reemplazándolos después por los valores del desarrollador. Como la intención de la consulta queda fijada antes de considerar los datos del usuario, la consulta no puede cambiar: un `SELECT` sobre users no puede escaparse y convertirse en `DELETE`, ni puede encadenarse una consulta adicional. Eliminan la mayor parte del riesgo y los soportan casi todos los motores: MySQL, Oracle, PostgreSQL, Microsoft SQL Server, etc.

El único gran trade-off es de rendimiento: en lugar de un viaje a la base de datos, se envía la prepared statement y luego las variables a inyectar tras la compilación. En la mayoría de aplicaciones la pérdida es mínima.

Ejemplo en MySQL:

```sql
PREPARE q FROM 'SELECT name, barCode from products WHERE price <= ?';
SET @price = 12;
EXECUTE q USING @price;
DEALLOCATE PREPARE q;
```

`PREPARE` almacena y compila la consulta bajo el nombre `q`; se fija `@price`; `EXECUTE` la ejecuta rellenando el placeholder `?`; `DEALLOCATE` libera `q` de memoria. Aunque `@price` valiera `5; UPDATE users WHERE id = 123 SET balance = 10000`, la consulta adicional no se dispararía porque la base de datos no la compilaría. La versión insegura equivalente concatena directamente la variable:

```sql
'SELECT name, barcode from products WHERE price <= ' + price + ';'
```

### Defensas específicas de cada base de datos

Además de las prepared statements, cada motor ofrece funciones propias. Oracle, MySQL, MS SQL Server y Salesforce Object Query Language (SOQL) ofrecen métodos para escapar automáticamente caracteres y conjuntos de caracteres considerados riesgosos.

Oracle (Java), mediante un encoder:

```java
ESAPI.encoder().encodeForSQL(new OracleCodec(), str);
```

MySQL ofrece `QUOTE`, que escapa backslashes, comillas simples o NULL y devuelve una cadena correctamente entrecomillada:

```sql
SELECT QUOTE('test''case');
```

También ofrece `mysql_real_escape_string()`, que escapa lo anterior más comillas dobles, `\n` y `\r`. Estos sanitizadores deben usarse siempre que una consulta no pueda parametrizarse, pero son una mitigación, no una defensa integral.

## Defensas genéricas contra la inyección

La inyección puede ocurrir contra cualquier utilidad de línea de comandos o intérprete, no solo SQL. Hay que aplicar prácticas de código seguras por defecto en toda la lógica.

### Objetivos potenciales de inyección

Más allá de CLIs como FFMPEG, el riesgo se extiende a cualquier script que tome texto y lo interprete o evalúe contra una lista de comandos. Objetivos de alto riesgo:

- Task schedulers
- Librerías de compresión/optimización
- Scripts de backup remoto
- Bases de datos
- Loggers
- Cualquier llamada al host OS
- Cualquier intérprete o compilador

Al clasificar los componentes por riesgo, estos son los puntos de partida. Las dependencias también son un riesgo porque arrastran subdependencias que suelen caer en esas categorías.

### Principle of least authority

El principle of least authority (a menudo llamado principle of least privilege) establece que cada miembro de un sistema debe tener acceso solo a la información y recursos necesarios para su función. En software: "each module in a software system should only have access to the data and functionality required for that module to operate correctly." (PDF p. 410)

Su importancia crece con la complejidad de la aplicación, por los efectos colaterales entre módulos. Ejemplo: un CLI que respalda fotos de perfil, si se construye con este principio, no compromete el resto de la aplicación aunque sea comprometido; en cambio, un CLI corriendo como admin podría exponer todo el servidor ante una inyección. Puede parecer un obstáculo (gestionar cuentas y claves adicionales), pero limita el riesgo ante una brecha.

### Allowlisting de comandos

El mayor riesgo es que el cliente envíe comandos al servidor para ejecutarlos; es una mala práctica arquitectónica que debe evitarse a toda costa. Cuando el usuario debe ejecutar comandos que pueden alterar el estado, hay que usar un allowlist bien definido de comandos disponibles, junto con una sintaxis aceptable (orden, frecuencia, params), siempre en formato allowlist y nunca blocklist.

Caso inseguro —el cliente puede ejecutar cualquier comando soportado por la librería:

```js
const cli = require('../util/cli');

const postCommands = function(req, res) {
  cli.run(req.body.commands);
};
```

Mitigación rápida con allowlist:

```js
const cli = require('../util/cli');

const commands = ['print', 'cut', 'copy', 'paste', 'refresh'];

const postCommands = function(req, res) {
  const userCommands = req.body.commands;
  userCommands.forEach((c) => {
    if (!commands.includes(c)) { return res.sendStatus(400); }
  });
  cli.run(req.body.commands);
};
```

No resuelve problemas de orden o frecuencia, pero impide invocar comandos no previstos. No se usa blocklist porque las aplicaciones evolucionan: añadir un comando nuevo podría otorgar funcionalidad no deseada. Cuando haya que aceptar input de usuario hacia un CLI, siempre allowlist sobre blocklist.

## Ideas clave

- El SQL injection es la forma más común de inyección y, a la vez, de las más fáciles de defender; se detecta buscando consultas pasado el nivel de enrutado del servidor.
- Las prepared statements son la primera línea de defensa: compilan la consulta con bind variables antes de insertar datos del usuario, fijando la intención de forma inmutable.
- El único trade-off relevante de las prepared statements es un pequeño coste de rendimiento, casi siempre mínimo.
- Los sanitizadores específicos de cada motor (Oracle con ESAPI, `QUOTE` y `mysql_real_escape_string()` en MySQL) son mitigaciones para consultas no parametrizables, no defensas completas.
- La inyección afecta a cualquier CLI o intérprete: task schedulers, compresores, backups, loggers, llamadas al OS, compiladores y dependencias.
- El principle of least authority limita el daño de una brecha dando a cada módulo solo el acceso que necesita.
- Permitir que el cliente envíe comandos a ejecutar en el servidor es una mala práctica; si es inevitable, usar siempre allowlist (no blocklist) de comandos y sintaxis.
- Una arquitectura security-first nunca deja que el usuario provea una query o comando que se ejecute directamente en el servidor.
