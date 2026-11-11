# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 14 — Databases (Bases de datos)

> Nota de extracción: el texto se tomó de la capa de texto del PDF; las citas usan la página del PDF (PDF p. N).

## Lo que necesitas saber

Una base de datos es, en esencia, un marco para almacenar datos y acceder a ellos de forma eficiente. El autor confiesa que, viniendo de un perfil ajeno a la programación, al principio no entendía por qué usar una base de datos en lugar de archivos sueltos en un directorio. La ventaja principal frente a archivos crudos es el rendimiento, sobre todo en servicios sensibles al tiempo (como una página web), además de gestionar la sincronización de copias y el traslado de datos entre medios de almacenamiento.

Conviene distinguir entre "database" (los datos y su organización) y "database management system" (DBMS, el software que da acceso a esos datos), aunque en la práctica se usan indistintamente y el libro es informal al respecto. Las bases de datos pueden ir desde una pequeña instancia bajo el capó de un programa de un solo equipo hasta sistemas repartidos en cientos de servidores; en ese caso, la idea de "una sola base de datos" es una abstracción que oculta con qué servidor físico hablas realmente.

El capítulo es un recorrido por los grandes paradigmas de bases de datos desde la línea de comandos. La familia más importante es la SQL, que da soporte al modelo relacional (RDB): extremadamente rápida y con gran capacidad de procesamiento, pero muy rígida en cuanto a tipos y formatos de datos. Frente a ella, las bases NoSQL (clave-valor, columnas anchas, documentos) son más flexibles con los tipos de datos, pero no ofrecen la misma potencia computacional.

Sales sabiendo escribir consultas básicas de MySQL (SELECT, WHERE, GROUP BY, JOIN, subconsultas), gestionar el servidor y cargar datos, y conociendo cuándo conviene un almacén clave-valor, de columnas anchas o de documentos (MongoDB).

## Bases de datos relacionales y MySQL (14.1)

En una RDB un conjunto de datos se representa como una tabla con filas (a menudo sin orden) y columnas. Cada columna tiene un tipo de dato asociado: entero, timestamp o cadena de longitud máxima conocida (los VARCHAR en jerga SQL). Una RDB lleva asociado un lenguaje de consulta que permite especificar qué datos seleccionar y qué preprocesamiento o agregación aplicar antes de devolverlos; la base está estructurada para responder esas consultas con gran eficiencia.

La familia SQL agrupa muchas RDB con interfaces casi idénticas. MySQL es la versión open-source más popular y la que más probablemente encontrarás en data science. Casi todo lo que se explica se traslada al resto de la familia SQL, y la sintaxis SQL es tan ubicua que muchos lenguajes de procesamiento la toman prestada.

Los datos en un servidor MySQL son una colección de tablas con columnas de tipos conocidos, organizadas en "databases" que actúan como espacios de nombres. Una consulta básica ilustra la sintaxis central:

```sql
USE my_database;
SELECT name, age
FROM people
WHERE state='WA';
```

`SELECT *` es atajo para seleccionar todas las columnas. También se puede omitir el `USE` y cualificar la tabla: `FROM my_database.people`. Esta selección de filas y columnas es la funcionalidad más básica.

Además de seleccionar columnas, MySQL permite aplicarles operaciones mediante una amplia gama de funciones integradas, usables tanto en `SELECT` como en `WHERE`. El libro muestra cómo extraer el nombre de pila con `SUBSTRING(name,0,LOCATE(name,' '))`: una sintaxis algo tortuosa. En Python sería más natural dividir la cadena por espacios y tomar la primera parte, pero eso crea una lista, una estructura arbitrariamente compleja que es anatema en un MySQL orientado al rendimiento: sus funciones evitan tipos complejos y se limitan a operaciones que pueden hacerse rapidísimas a gran escala.

El libro tabula funciones útiles, entre ellas: ABS, COALESCE (primer valor no nulo, muy útil tras joins), CONCAT, CONVERT_TZ, DATE, DAYOFMONTH, DAYOFWEEK, FLOOR, HOUR, LENGTH, LOWER, LOCATE, LPAD, NOW, POW, REGEXP, REPLACE, SQRT, TRIM y UPPER.

Para agregar muchas filas en un único valor se usa `GROUP BY`:

```sql
SELECT state, COUNT(name)
FROM people
GROUP BY state
WHERE first_name='Helen';
```

`COUNT()` es un agregador entre varios: MAX, MIN, AVG, STDDEV, VARIANCE y SUM. Se puede agrupar por varios campos (`GROUP BY state, city`) y renombrar columnas con `AS` (p. ej. `COUNT(name) AS num_people`). El renombrado no cambia nada si solo extraes datos, pero es muy útil al escribir el resultado en otra tabla o al trabajar con varias tablas en la misma consulta.

### Joins (14.1.2)

Un join combina varias tablas en una, emparejando filas según un criterio (normalmente campos comunes):

```sql
SELECT p.state, e.job_title, COUNT(p.name)
FROM people p JOIN employees e
ON p.name=e.name
GROUP BY p.state, e.job_title;
```

La cláusula `ON` da el criterio de coincidencia y los alias (`people p`, `employees e`) eliminan ambigüedad entre columnas homónimas. Cada fila de una tabla se empareja con cada fila coincidente de la otra: si hay 5 filas "Helen" en una y 10 en otra, el resultado tendrá 50 filas para Helen. Esa explosión de tamaño es una razón por la que los joins pueden ser muy costosos.

El ejemplo anterior es un inner join: las filas sin coincidencia se descartan en ambas tablas. Un left outer join conserva las filas huérfanas de la tabla izquierda, rellenando con NULL las columnas de la derecha (y el right outer join, al revés). Los outer joins son muy comunes cuando hay una tabla "primaria": por ejemplo, para predecir si alguien hará clic en un anuncio, un left outer join entre la tabla de anuncios y la de empresas añade columnas-features sin perder anuncios aunque falten datos de la empresa.

### Subconsultas y gestión de la base (14.1.3-14.1.4)

Las operaciones clave son SELECT, WHERE, GROUP BY y JOIN; cada consulta suele usar cada una como mucho una vez, pero se pueden anidar. El libro muestra una subconsulta que cuenta empleados por ciudad y la vuelve a unir a la tabla original para saber cuántos compañeros locales tiene cada empleado. Puntos a notar: la subconsulta va entre paréntesis, se le da un alias después del paréntesis (muchas variantes de SQL lo exigen) y se nombran sus columnas con `AS` para mayor legibilidad.

Para la operativa, lo más fácil es la línea de comandos. Se abre una sesión indicando host, usuario, contraseña y base:

```sql
mysql --host=10.0.0.4 --user=myname --password=mypass mydb
```

Dentro del shell, cada comando termina en punto y coma (puede abarcar varias líneas): `SHOW TABLES;`, `USE otra_db;`, `DROP TABLE tabla;`, `CREATE DATABASE nueva;`. Crear una tabla es algo más complejo, dando nombres y tipos de columna (`VARCHAR(30)` = cadena de hasta 30 caracteres):

```sql
CREATE TABLE MyGuests (
  id INT,
  firstname VARCHAR(30),
  lastname VARCHAR(30),
  arrival_date TIMESTAMP
);
```

Se rellena con `INSERT INTO ... VALUES (...)` para pocas entradas, o cargando un CSV con `LOAD DATA INFILE '/tmp/test.txt' INTO TABLE test FIELDS DELIMITED BY ','`. Para extraer resultados a un CSV local desde bash se usa la opción `-e` del cliente y redirección: `mysql --host localhost -e 'SELECT * FROM foo.MyGuests' > foo.csv`.

## Almacenes clave-valor (14.2)

El siguiente paradigma es el almacén clave-valor, conceptualmente como un diccionario de Python a escala masiva: mapea claves (normalmente cadenas) a objetos de datos arbitrarios. Es excelente para datos no estructurados como páginas web y ha ganado protagonismo en el movimiento Big Data. Su desventaja: solo dan acceso a los datos, sin el preprocesamiento optimizado de una RDB.

También es una forma más eficiente de guardar datos relacionales muy dispersos (muchas columnas potenciales, casi todas NULL): se usa la tupla persona/columna como clave y el dato como valor, asumiendo NULL si no hay entrada. Ejemplos: Oracle NoSQL Database, redis y dbm.

## Almacenes de columnas anchas (14.3)

Un wide column store es como una RDB pero con un número enorme de columnas y mayormente disperso. A diferencia de las RDB, se pueden añadir o borrar columnas a voluntad y una columna puede existir solo para unas pocas filas relacionadas; se parece más a un clave-valor cuyo clave combina id de fila y nombre de columna. Operaciones como GROUP BY y JOIN a menudo no están soportadas.

El original suele considerarse Bigtable, herramienta interna de Google descrita en su artículo *Bigtable: A Distributed Storage System for Structured Data*. Bigtable añade timestamps a cada celda y guarda registros de entradas previas; sus columnas se agrupan en "column families" accedidas juntas. Opciones open-source: Cassandra, HBase y Accumulo.

## Almacenes de documentos y MongoDB (14.4)

Los document stores son parecidos a los clave-valor, pero los valores son documentos de formato flexible (XML o JSON). Además de leer y escribir, ofrecen funcionalidad para buscar y extraer documentos (o partes) que cumplan ciertos criterios. Son un punto intermedio feliz entre RDB y clave-valor: flexibles para datos no tabulares, pero estructurados para poder procesarlos. El más popular es MongoDB, open-source y gratuito.

En Mongo los datos se dividen en bases que contienen "Collections" (análogas a las tablas), y cada colección agrupa documentos en un formato tipo JSON llamado BSON. Un documento es muy flexible: mezcla campos, tipos, anidamiento, etc. Lo único obligatorio es un identificador único `_id` que actúa como clave primaria; si se repite, da error. Si no se indica, Mongo asigna un ObjectID que codifica el instante de creación (en segundos), un código de la máquina (útil en clústeres), el id del proceso y un contador de orden, de modo que ObjectIDs del mismo proceso en el mismo segundo siguen siendo distintos.

El núcleo del acceso es la consulta, que es en sí misma un objeto tipo JSON que mapea campos a los requisitos sobre ellos:

```javascript
use some_db
db.posts.insert({"name":"Bob","age":31})
db.posts.find()              // sin query = todos los documentos
db.posts.find({"name":"Bob"})
```

Los operadores que empiezan por `$` son "query operators" y forman la lógica de la consulta: `{"age":{$gt:10}}`, `{$gt:10,$lt:20}`, `{$exists:true}`. De hecho `{"name":"Bob"}` es azúcar sintáctico de `{"name":{$eq:"Bob"}}`. La función `find` admite un segundo argumento, la projection, que indica qué campos devolver (hay que excluir `_id` explícitamente con `_id:0`) y cuántos elementos de un array (`$slice`, `$elemMatch`).

Para modificar se usa `update()`, con tres argumentos: una consulta que indica los documentos a modificar, una sentencia de actualización con operadores (`$set`, `$inc`) y, opcionalmente, opciones; la más importante es `multi`, que indica si se modifican varios documentos y cuyo valor por defecto (false) resulta contraintuitivo.

## Ideas clave

- Una base de datos almacena y accede a datos eficientemente; su ventaja sobre archivos crudos es el rendimiento, además de sincronizar copias y mover datos entre medios.
- "Database" son los datos y su organización; "DBMS" es el software que los sirve, aunque en la práctica se usen indistintamente.
- La familia SQL (modelo relacional) es rapidísima y potente pero rígida en tipos; las NoSQL son más flexibles pero con menos potencia de procesamiento.
- En MySQL las operaciones clave son SELECT, WHERE, GROUP BY y JOIN, con agregadores (COUNT, AVG, SUM...) y posibilidad de anidar consultas.
- Un inner join descarta filas sin coincidencia; los outer joins conservan filas huérfanas rellenando con NULL, útiles cuando hay una tabla primaria.
- Los joins pueden explotar en tamaño (producto de coincidencias), por lo que son operaciones costosas.
- Clave-valor (redis, dbm): como un diccionario masivo, ideal para datos no estructurados o relacionales muy dispersos, sin preprocesamiento.
- Columnas anchas (Bigtable, Cassandra, HBase): tablas enormes y dispersas con columnas dinámicas, normalmente sin JOIN ni GROUP BY.
- Document stores (MongoDB): almacenan documentos JSON/BSON flexibles con `_id` obligatorio y consultas con query operators `$`, término medio entre RDB y clave-valor.
