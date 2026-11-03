# Defending Against Injection (Defendiéndose contra la inyección) — Estudio

## Tarjetas de repaso

P: ¿Por qué el SQL injection recibe el mayor foco entre las formas de inyección?
R: Porque es la más común —afecta potencialmente a casi toda aplicación compleja por la prevalencia de bases de datos SQL— y, a la vez, de las más fáciles de defender, ya que ocurre dentro del intérprete SQL y su detección puede ser sencilla.

P: ¿Dónde ocurren las operaciones SQL en aplicaciones modernas y qué implica para la detección?
R: Ocurren pasado el nivel de enrutado del servidor, por lo que el cliente no interesa; la búsqueda de consultas vulnerables se centra en el código del servidor.

P: ¿Qué regla útil indica dónde pueden estar los datos que persisten?
R: Si los datos persisten entre dispositivos y sesiones, están en memoria del servidor, en disco (logs) o en una base de datos.

P: ¿Por qué las búsquedas de consultas deben ser genéricas?
R: Porque muchas aplicaciones usan más de una base de datos (p. ej. SQL Server y MySQL) y algunas usan un DSL con sintaxis distinta a la de una llamada SQL cruda; conviene compilar en un lugar los DSL y tipos de SQL en uso.

P: ¿Qué son las prepared statements y por qué se consideran la "primera línea" de defensa?
R: Son consultas compiladas con placeholders (bind variables) que luego se rellenan con los valores del desarrollador; son fáciles de implementar, bien documentadas y muy efectivas.

P: ¿Por qué una prepared statement impide cambiar la intención de la consulta?
R: Porque la consulta se compila y su intención queda fijada antes de considerar los datos del usuario, así un SELECT no puede convertirse en DELETE ni encadenar una consulta adicional.

P: ¿Cuál es el único gran trade-off de las prepared statements?
R: De rendimiento: en lugar de un viaje a la base de datos se envía la prepared statement y luego las variables tras la compilación; en la mayoría de aplicaciones la pérdida es mínima.

P: ¿Qué hacen las instrucciones PREPARE, EXECUTE y DEALLOCATE en MySQL?
R: PREPARE almacena y compila la consulta bajo un nombre; EXECUTE la ejecuta rellenando el placeholder; DEALLOCATE libera la consulta de memoria.

P: ¿Qué defensas específicas ofrecen los motores además de las prepared statements?
R: Métodos para escapar automáticamente caracteres riesgosos: Oracle con un encoder ESAPI (OracleCodec), y MySQL con QUOTE y mysql_real_escape_string(); SOQL de Salesforce también ofrece métodos propios.

P: ¿Qué diferencia hay entre QUOTE y mysql_real_escape_string() en MySQL?
R: QUOTE escapa backslashes, comillas simples o NULL y devuelve una cadena entrecomillada; mysql_real_escape_string() escapa eso más comillas dobles, \n y \r.

P: ¿Son los sanitizadores específicos de motor una defensa completa?
R: No; son una mitigación que debe usarse siempre que una consulta no pueda parametrizarse, no una defensa integral.

P: ¿Qué establece el principle of least authority (least privilege) en software?
R: Que cada módulo debe tener acceso solo a los datos y la funcionalidad necesarios para operar correctamente, limitando el daño ante una brecha.

P: ¿Cuáles son objetivos de inyección más allá de SQL?
R: Task schedulers, librerías de compresión/optimización, scripts de backup remoto, bases de datos, loggers, cualquier llamada al host OS y cualquier intérprete o compilador; también las dependencias y sus subdependencias.

P: ¿Por qué se usa allowlist y no blocklist para comandos de usuario hacia un CLI?
R: Porque las aplicaciones evolucionan: añadir un comando nuevo con blocklist podría otorgar funcionalidad no deseada; el allowlist solo permite comandos previstos.

P: ¿Qué práctica arquitectónica debe evitarse a toda costa según el capítulo?
R: Permitir que el cliente envíe comandos (o queries) al servidor para ejecutarlos directamente; una arquitectura security-first nunca lo hace.

## Preguntas de autoevaluación

P: ¿Cómo se localizan consultas SQL en un proyecto Node.js y qué lo complica?
R: Si la librería SQL se importa por módulo, basta con buscar el import (p. ej. `require('mysql')`); se complica si las consultas se declaran globalmente o se heredan de una clase padre, o si se usan constructores literales como `q.select()`. (Sección "Detectar SQL injection")

P: ¿Por qué una prepared statement neutraliza una entrada maliciosa como `5; UPDATE users WHERE id = 123 SET balance = 10000`?
R: Porque la consulta adicional no se dispararía: la base de datos no la compila, ya que la intención quedó fijada al compilar la prepared statement con el placeholder. (Sección "Prepared statements")

P: ¿Qué diferencia una consulta parametrizada de la versión insegura equivalente?
R: La insegura concatena directamente la variable en la cadena de la consulta (`... WHERE price <= ' + price + ';'`), mientras que la segura usa un placeholder `?` rellenado tras la compilación. (Sección "Prepared statements")

P: ¿En qué tres bloques organiza el autor las defensas contra la inyección?
R: Defensas contra SQL injection, cuáles de ellas aplican a otras formas de inyección, y métodos genéricos no específicos de ningún subtipo. (Sección "Lo que necesitas saber")

P: ¿Por qué las dependencias son un riesgo de inyección?
R: Porque arrastran subdependencias que suelen caer en las categorías de objetivos de alto riesgo (schedulers, compresores, loggers, llamadas al OS, etc.). (Sección "Objetivos potenciales de inyección")

P: ¿Qué ejemplo ilustra el valor del principle of least authority?
R: Un CLI que respalda fotos de perfil construido con este principio no compromete el resto de la aplicación aunque sea comprometido; en cambio, un CLI corriendo como admin podría exponer todo el servidor ante una inyección. (Sección "Principle of least authority")

P: ¿Qué limitación tiene la mitigación por allowlist mostrada en el ejemplo?
R: No resuelve problemas de orden o frecuencia de los comandos, pero impide invocar comandos no previstos por la librería. (Sección "Allowlisting de comandos")

## Puntos a dominar

- Explicar por qué el SQL injection es a la vez la forma más común y de las más fáciles de defender.
- Saber localizar consultas vulnerables en el servidor, incluyendo casos con múltiples bases de datos y DSL.
- Describir el funcionamiento de las prepared statements (compilación con bind variables, intención inmutable) y su único trade-off de rendimiento.
- Distinguir las defensas específicas de cada motor (ESAPI/OracleCodec, QUOTE, mysql_real_escape_string()) como mitigaciones, no defensas completas.
- Identificar objetivos de inyección más allá de SQL (CLIs, schedulers, loggers, llamadas al OS, dependencias).
- Aplicar el principle of least authority para limitar el daño de una brecha por módulo.
- Justificar el uso de allowlist sobre blocklist para comandos de usuario hacia un CLI y rechazar que el cliente ejecute comandos directamente en el servidor.
