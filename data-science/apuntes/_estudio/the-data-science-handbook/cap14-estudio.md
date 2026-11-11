# Databases (Bases de datos) — Estudio

## Tarjetas de repaso

P: ¿Qué es una base de datos y cuál es su principal ventaja frente a archivos crudos? / R: Un marco para almacenar datos y acceder a ellos eficientemente; su ventaja principal es el rendimiento (sobre todo en servicios sensibles al tiempo), además de sincronizar copias y mover datos entre medios de almacenamiento.

P: ¿Qué diferencia hay entre "database" y "DBMS"? / R: "Database" son los datos y su organización; "DBMS" (database management system) es el software que da acceso a esos datos, aunque en la práctica se usen indistintamente.

P: ¿Cómo se contrastan las bases SQL y NoSQL en potencia y flexibilidad? / R: La familia SQL (modelo relacional) es rapidísima y de gran capacidad de procesamiento pero rígida en tipos y formatos; las NoSQL (clave-valor, columnas anchas, documentos) son más flexibles con los tipos pero no ofrecen la misma potencia computacional.

P: ¿Cómo se representa un conjunto de datos en una RDB? / R: Como una tabla con filas (a menudo sin orden) y columnas, donde cada columna tiene un tipo de dato asociado: entero, timestamp o cadena de longitud máxima conocida (VARCHAR).

P: ¿Cuáles son las cuatro operaciones clave de una consulta MySQL? / R: SELECT, WHERE, GROUP BY y JOIN; cada consulta suele usar cada una como mucho una vez, pero se pueden anidar.

P: ¿Por qué las funciones integradas de MySQL evitan tipos complejos como listas? / R: Porque una lista es una estructura arbitrariamente compleja, anatema en un MySQL orientado al rendimiento; sus funciones se limitan a operaciones que pueden hacerse rapidísimas a gran escala.

P: ¿Para qué sirve COALESCE y cuándo es especialmente útil? / R: Devuelve el primer valor no nulo; es muy útil tras joins.

P: ¿Qué hace GROUP BY y qué agregadores se pueden usar? / R: Agrega muchas filas en un único valor; agregadores: COUNT, MAX, MIN, AVG, STDDEV, VARIANCE y SUM.

P: ¿Qué es un join y por qué puede ser costoso? / R: Combina varias tablas emparejando filas según un criterio; cada fila se empareja con cada fila coincidente de la otra (5 × 10 = 50 filas), y esa explosión de tamaño encarece la operación.

P: ¿Qué diferencia un inner join de un left outer join? / R: El inner join descarta las filas sin coincidencia en ambas tablas; el left outer join conserva las filas huérfanas de la tabla izquierda, rellenando con NULL las columnas de la derecha.

P: ¿Qué es un almacén clave-valor y para qué es excelente? / R: Es como un diccionario de Python a escala masiva que mapea claves (normalmente cadenas) a objetos de datos arbitrarios; excelente para datos no estructurados como páginas web y para datos relacionales muy dispersos. Ejemplos: Oracle NoSQL Database, redis y dbm.

P: ¿Qué caracteriza a un wide column store frente a una RDB? / R: Es como una RDB pero con un número enorme de columnas y mayormente disperso; se pueden añadir o borrar columnas a voluntad y a menudo no soporta GROUP BY ni JOIN. Original: Bigtable; open-source: Cassandra, HBase, Accumulo.

P: ¿Qué es un document store y cuál es el más popular? / R: Es parecido a un clave-valor pero los valores son documentos de formato flexible (XML o JSON), con funcionalidad para buscar y extraer; el más popular es MongoDB. Es un punto intermedio entre RDB y clave-valor.

P: ¿Qué es obligatorio en un documento de MongoDB y qué pasa si no se indica? / R: Un identificador único `_id` que actúa como clave primaria (da error si se repite); si no se indica, Mongo asigna un ObjectID que codifica instante de creación, código de máquina, id de proceso y un contador de orden.

P: ¿Qué son los query operators en MongoDB y cómo se reconocen? / R: Son operadores que empiezan por `$` y forman la lógica de la consulta, como `$gt`, `$lt`, `$exists`, `$eq`; de hecho `{"name":"Bob"}` es azúcar sintáctico de `{"name":{$eq:"Bob"}}`.

## Preguntas de autoevaluación

P: ¿Por qué el autor inicialmente no veía la ventaja de una base de datos frente a archivos sueltos, y qué la justifica? / R: Viniendo de un perfil ajeno a la programación no lo entendía; la justifica el rendimiento, sobre todo en servicios sensibles al tiempo como una página web, además de la sincronización de copias y el traslado entre medios. (Lo que necesitas saber)

P: ¿Por qué MySQL es la variante SQL más relevante en data science y por qué importa aprenderla? / R: Es la versión open-source más popular y la que más probablemente encontrarás; casi todo se traslada al resto de la familia SQL y su sintaxis es tan ubicua que muchos lenguajes la toman prestada. (14.1)

P: En un join, ¿qué papel cumplen la cláusula ON y los alias de tabla? / R: La cláusula ON da el criterio de coincidencia entre filas y los alias (p. ej. `people p`, `employees e`) eliminan la ambigüedad entre columnas homónimas. (14.1.2 Joins)

P: ¿Cuándo conviene un left outer join y con qué ejemplo lo ilustra el libro? / R: Cuando hay una tabla "primaria" que no se quiere perder; ejemplo: para predecir si alguien hará clic en un anuncio, un left outer join entre la tabla de anuncios y la de empresas añade columnas-features sin perder anuncios aunque falten datos de la empresa. (14.1.2 Joins)

P: ¿Qué puntos hay que cuidar al escribir una subconsulta en SQL? / R: La subconsulta va entre paréntesis, se le da un alias después del paréntesis (muchas variantes de SQL lo exigen) y se nombran sus columnas con AS para mayor legibilidad. (14.1.3-14.1.4)

P: ¿Por qué un almacén clave-valor puede ser más eficiente que una RDB para datos relacionales muy dispersos? / R: Porque con muchas columnas potenciales casi todas NULL, se usa la tupla persona/columna como clave y el dato como valor, asumiendo NULL si no hay entrada, evitando almacenar los huecos. (14.2)

P: ¿Qué aporta Bigtable respecto a un wide column store básico? / R: Añade timestamps a cada celda y guarda registros de entradas previas, y agrupa sus columnas en "column families" que se acceden juntas. (14.3)

P: En MongoDB, ¿qué tres argumentos recibe update() y qué opción resulta contraintuitiva? / R: Una consulta con los documentos a modificar, una sentencia de actualización con operadores (`$set`, `$inc`) y opcionalmente opciones; la más importante es `multi`, cuyo valor por defecto (false) es contraintuitivo. (14.4)

## Puntos a dominar

- Explicar la ventaja de una base de datos frente a archivos crudos y distinguir "database" de "DBMS".
- Situar SQL (relacional) frente a NoSQL en el eje potencia de procesamiento vs. flexibilidad de tipos.
- Escribir consultas MySQL básicas combinando SELECT, WHERE, GROUP BY y JOIN, con agregadores y alias (AS).
- Diferenciar inner join de left/right outer join y razonar su coste por explosión de filas.
- Anidar subconsultas correctamente (paréntesis, alias, columnas con AS).
- Reconocer cuándo elegir clave-valor, columnas anchas o document store según la estructura y dispersión de los datos.
- Manejar los fundamentos de MongoDB: colecciones, BSON, `_id`/ObjectID, consultas con query operators `$`, projection y update() con `multi`.
