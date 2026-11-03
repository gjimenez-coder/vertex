# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 2 — Data Models and Query Languages (Modelos de datos y lenguajes de consulta)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página como (PDF p. N).

## Lo que necesitas saber

Los modelos de datos son, según Kleppmann, una de las partes más importantes del desarrollo de software, porque condicionan tanto cómo se escribe el software como la forma de pensar el problema. Las aplicaciones se construyen por capas: el mundo real se modela en objetos y estructuras; estas se expresan en un modelo general (JSON, XML, tablas relacionales, grafos); el motor de base de datos las representa en bytes; y por debajo el hardware las convierte en corrientes y campos. Cada capa oculta la complejidad de la inferior ofreciendo un modelo limpio.

El capítulo compara tres modelos de propósito general para almacenar y consultar datos —relacional, de documentos y de grafos— junto con sus lenguajes de consulta. La tesis central es que no existe un modelo único óptimo: cada uno encaja mejor con un tipo de relaciones entre los datos. El modelo de documentos sirve para datos autocontenidos con relaciones uno-a-muchos (estructura de árbol); el relacional soporta bien joins y relaciones muchos-a-uno y muchos-a-muchos; y el de grafos es el más natural cuando casi todo puede estar relacionado con todo.

Sales sabiendo distinguir schema-on-read frente a schema-on-write, el concepto de impedance mismatch, las razones del auge de NoSQL, la diferencia entre lenguajes de consulta declarativos e imperativos, y cómo se consultan datos de grafos con Cypher, SPARQL y Datalog. También entiendes por qué los sistemas relacionales y de documentos están convergiendo.

## El ejemplo que recorre el capítulo

El hilo conductor es un currículum/perfil de LinkedIn (el de Bill Gates). Un perfil tiene campos únicos (first_name, last_name) y colecciones uno-a-muchos (positions, education, contact_info). Sirve para contrastar la representación relacional normalizada en varias tablas frente a un documento JSON autocontenido, y para mostrar cómo, al añadir features (organizaciones y escuelas como entidades, recomendaciones), aparecen relaciones muchos-a-muchos. En la parte de grafos el ejemplo cambia a Lucy (de Idaho) y Alain (de Beaune), casados y viviendo en Londres.

## Modelo relacional frente a modelo de documentos

El modelo relacional de SQL, propuesto por Edgar Codd en 1970, organiza los datos en relaciones (tablas), colecciones no ordenadas de tuplas (filas). Nació en el procesamiento de datos de negocio en mainframes de los años 60-70 (transaction processing y batch processing) y su objetivo era ocultar el detalle de representación tras una interfaz limpia. Dominó durante 25-30 años, superando a los modelos network y hierarchical, a las bases de datos de objetos y a las de XML. Resultó generalizar muy bien más allá de su ámbito original.

NoSQL es el intento de los años 2010 de destronar al modelo relacional. El nombre surgió como hashtag para un meetup de 2009 sobre bases de datos distribuidas, open source y no relacionales, y se reinterpretó como "Not Only SQL". Sus motores de adopción: necesidad de mayor escalabilidad (datasets enormes o alto throughput de escritura), preferencia por software libre, operaciones de consulta especializadas no bien soportadas por el modelo relacional, y frustración con la rigidez de los esquemas relacionales. El resultado previsible es la *polyglot persistence*: lo relacional convive con diversos datastores no relacionales.

El desajuste objeto-relacional (*impedance mismatch*) es la capa de traducción incómoda entre los objetos del código y el modelo de tablas, filas y columnas. Los ORM (ActiveRecord, Hibernate) reducen el boilerplate pero no eliminan la diferencia. Un perfil tipo currículum, mayormente autocontenido, encaja bien como JSON: tiene mejor *locality* (toda la información en un sitio, una sola consulta frente a múltiples consultas o un join multitabla) y hace explícita la estructura de árbol de las relaciones uno-a-muchos.

### Relaciones muchos-a-uno y muchos-a-muchos

En el ejemplo, region_id e industry_id se guardan como IDs, no como texto. Usar un ID en lugar del texto evita duplicación: la información con significado para humanos se almacena una sola vez, da consistencia de estilo, evita ambigüedad, facilita la actualización, permite localización e mejora la búsqueda. Como el ID no significa nada para los humanos, nunca necesita cambiar. Eliminar esa duplicación es la idea clave de la *normalización*.

El problema es que normalizar requiere relaciones muchos-a-uno, que no encajan bien en el modelo de documentos: los joins suelen tener soporte débil (al escribir el libro, RethinkDB los soportaba, MongoDB no, y CouchDB solo en vistas predeclaradas). Si la base de datos no los soporta, hay que emularlos con varias consultas en el código. Además los datos tienden a interconectarse más con el tiempo: convertir organizaciones y escuelas en entidades, o añadir recomendaciones, introduce relaciones muchos-a-muchos que exigen referencias y joins.

### ¿Repiten historia las bases de datos de documentos?

El debate sobre cómo representar estas relaciones es anterior a NoSQL. En los 70, la base de datos más popular para negocio era IMS de IBM (de 1968, desarrollada para el programa Apollo), basada en el *hierarchical model*: datos como un árbol de registros anidados, muy similar a JSON. Como los documentos, IMS funcionaba bien con uno-a-muchos pero hacía difícil muchos-a-muchos y no soportaba joins; había que duplicar (desnormalizar) o resolver referencias a mano.

Surgieron dos soluciones. El *network model* (CODASYL), generalización del jerárquico en que un registro puede tener varios padres, modelaba muchos-a-uno y muchos-a-muchos mediante enlaces tipo punteros. El único modo de acceder a un registro era seguir un *access path* desde la raíz, lo que hacía el código complicado e inflexible: cambiar los caminos obligaba a reescribir las consultas. El *relational model* hizo lo contrario: expuso los datos en abierto, sin estructuras anidadas ni caminos de acceso. El *query optimizer* decide automáticamente el "access path" (qué índices usar y en qué orden). La idea clave: basta construir el optimizador una vez y todas las aplicaciones se benefician.

Respecto a muchos-a-uno y muchos-a-muchos, relacional y documentos no difieren de fondo: el ítem relacionado se referencia por un identificador único (*foreign key* en relacional, *document reference* en documentos) resuelto en lectura con un join o consultas sucesivas. Las de documentos no han seguido el camino de CODASYL.

### Relacional frente a documentos hoy

A favor del modelo de documentos: flexibilidad de esquema, mejor rendimiento por locality y mayor cercanía a las estructuras de la aplicación. A favor del relacional: mejor soporte de joins y de relaciones muchos-a-uno y muchos-a-muchos. Si los datos tienen forma de documento (árbol uno-a-muchos cargado de una vez), el modelo de documentos simplifica; el *shredding* relacional (partir el documento en muchas tablas) da esquemas engorrosos. Pero si hay muchos-a-muchos, el modelo de documentos se complica: desnormalizar obliga a mantener la consistencia en el código. Para datos muy interconectados, el modelo de documentos es incómodo, el relacional aceptable y los grafos lo más natural.

### Flexibilidad de esquema

Las bases de documentos no imponen esquema. Son mal llamadas *schemaless*: hay un esquema implícito que el código de lectura asume pero la base no refuerza. Es más preciso hablar de *schema-on-read* (estructura implícita, interpretada al leer) frente a *schema-on-write* (esquema explícito, verificado al escribir), análogos al tipado dinámico y estático. La diferencia se nota al cambiar el formato: en documentos basta empezar a escribir con los campos nuevos y manejar los viejos en el código; en relacional se hace una migración (`ALTER TABLE ... ADD COLUMN`, luego `UPDATE`). El `ALTER TABLE` suele tardar milisegundos (MySQL es la excepción: copia la tabla entera). Schema-on-read conviene con datos heterogéneos; schema-on-write documenta y refuerza una estructura común.

### Locality y convergencia

Un documento se guarda como una cadena continua (JSON, XML o variantes binarias como BSON de MongoDB). Si la aplicación necesita el documento entero, hay ventaja de *storage locality* frente a múltiples búsquedas en varias tablas. Pero la base carga el documento completo aunque uses poco, y al actualizar suele reescribirlo entero; por eso se recomienda mantener documentos pequeños. La idea de agrupar datos relacionados no es exclusiva de documentos: Spanner (interleaving), Oracle (multi-table index cluster tables) y las column-families de Bigtable (Cassandra, HBase) persiguen lo mismo.

Relacional y documentos convergen: la mayoría de sistemas relacionales soportan XML desde mediados de los 2000 y JSON (PostgreSQL 9.3, MySQL 5.7, DB2 10.5); del otro lado, RethinkDB ofrece joins y algunos drivers de MongoDB resuelven referencias (join del lado cliente). Un híbrido relacional-documento parece el buen camino a futuro.

## Lenguajes de consulta para datos

SQL introdujo una forma nueva de consultar: es un lenguaje *declarativo*, mientras que IMS y CODASYL usaban código *imperativo*. Un lenguaje imperativo indica qué operaciones hacer y en qué orden (un bucle que recorre `animals` y filtra los "Sharks"). Uno declarativo, como SQL o el álgebra relacional (`σ family="Sharks"`), especifica solo el patrón del resultado —qué condiciones debe cumplir y cómo transformarlo— y deja al query optimizer decidir índices, métodos de join y orden de ejecución.

Lo declarativo es más conciso, oculta detalles de implementación (la base puede mejorar el rendimiento sin cambiar las consultas, p. ej. reordenar registros en disco porque SQL no garantiza un orden) y se presta a la ejecución en paralelo, importante porque las CPU crecen en núcleos, no en frecuencia. El código imperativo es difícil de paralelizar porque fija el orden de las instrucciones.

La ventaja declarativa no se limita a bases de datos. En un navegador, CSS (`li.selected > p { background-color: blue; }`) y XSL/XPath declaran el patrón de elementos a estilar; hacer lo mismo imperativamente con la DOM API en JavaScript resulta largo, frágil (no quita el estilo al cambiar la clase) y atado a APIs concretas.

### Consultas con MapReduce

MapReduce es un modelo de programación para procesar grandes volúmenes en bloque sobre muchas máquinas, popularizado por Google; MongoDB y CouchDB soportan una forma limitada para consultas de solo lectura. No es ni declarativo ni plenamente imperativo: la lógica se expresa con fragmentos de código basados en las funciones `map` y `reduce` del paradigma funcional. En el ejemplo (contar tiburones avistados por mes), `map` emite un par clave-valor (`"1995-12"`, numAnimals) por cada documento que coincide con el filtro, y `reduce` suma los valores de cada clave.

`map` y `reduce` deben ser funciones puras: solo usan su entrada, no consultan la base ni tienen efectos secundarios, lo que permite ejecutarlas en cualquier orden y reintentarlas tras un fallo. El inconveniente de usabilidad es tener que escribir dos funciones JavaScript coordinadas, más difícil que una sola consulta, y además un lenguaje declarativo da más margen al optimizador. Por eso MongoDB 2.2 añadió la *aggregation pipeline*, declarativa con sintaxis JSON y expresividad similar a un subconjunto de SQL. Moraleja: un sistema NoSQL puede acabar reinventando SQL sin darse cuenta.

## Modelos de datos tipo grafo

Cuando las relaciones muchos-a-muchos son muy frecuentes, lo natural es modelar como grafo. Un grafo tiene *vertices* (nodos/entidades) y *edges* (aristas/relaciones). Ejemplos: grafos sociales, el grafo de la web, redes de carreteras. No se limitan a datos homogéneos: permiten almacenar tipos de objetos muy distintos de forma consistente (Facebook mantiene un único grafo con personas, lugares, eventos, checkins y comentarios). El capítulo usa a Lucy (Idaho) y Alain (Beaune), casados en Londres, que permite expresar estructuras regionales distintas por país y granularidades variables. Se presentan dos modelos (property graph y triple-store) y tres lenguajes declarativos: Cypher, SPARQL y Datalog.

### Property graphs y Cypher

En el *property graph*, cada vértice tiene id único, aristas entrantes y salientes y propiedades (clave-valor); cada arista tiene id, vértice de cola, vértice de cabeza, una etiqueta (*label*) que describe la relación y propiedades. Puede representarse con dos tablas relacionales (vertices y edges, con índices sobre tail_vertex y head_vertex). Rasgos clave: cualquier vértice puede conectarse con cualquier otro (sin esquema que lo restrinja), se recorre eficientemente hacia delante y hacia atrás, y distintas etiquetas permiten mezclar tipos de información. Son buenos para la evolvabilidad.

Cypher es el lenguaje declarativo de Neo4j. Usa notación de flechas (`(Idaho)-[:WITHIN]->(USA)`) para crear aristas y cláusulas `MATCH` para buscar patrones; `:WITHIN*0..` significa "seguir una arista WITHIN cero o más veces", como el `*` de una expresión regular. No hace falta especificar el plan: el optimizador elige la estrategia.

### Grafos en SQL, triple-stores y Datalog

La misma consulta puede escribirse en SQL, pero con dificultad: en un grafo el número de joins no se conoce de antemano. Desde SQL:1999 esto se expresa con *recursive common table expressions* (`WITH RECURSIVE`), pero la sintaxis es muy torpe: lo que en Cypher son 4 líneas, en SQL son 29. Distintos modelos sirven a distintos casos de uso.

El modelo *triple-store* es casi equivalente al property graph: toda la información son enunciados de tres partes (sujeto, predicado, objeto); p. ej. (Jim, likes, bananas). El objeto es un valor primitivo (equivale a una propiedad) u otro vértice (el predicado es una arista). Formatos como Turtle (subconjunto de N3) escriben estos triples. El modelo es independiente del *semantic web*, idea razonable pero sobrevendida en los 2000: publicar datos legibles por máquina mediante RDF para combinarlos en una "web de datos". SPARQL es el lenguaje de consulta para triple-stores RDF; precede a Cypher (que tomó de él su pattern matching) y resulta aún más conciso.

Los grafos no son CODASYL redivivo: no imponen esquema de anidamiento, permiten referir directamente a cualquier vértice por id o índice, no ordenan vértices ni aristas, y ofrecen lenguajes declarativos. Datalog es más antiguo (estudiado en los 80) y es la base sobre la que se apoyan los demás; se usa en Datomic y Cascalog (Hadoop). Escribe los triples como `predicado(sujeto, objeto)` y define *reglas* (con `:-`) que derivan nuevos predicados y pueden combinarse y reutilizarse; es menos cómodo para consultas puntuales pero más potente con datos complejos.

## Ideas clave

- El modelo de datos condiciona tanto cómo se escribe el software como cómo se piensa el problema; se construye por capas que ocultan complejidad.
- No hay modelo único: documentos para datos autocontenidos con uno-a-muchos, relacional para muchos-a-uno/muchos-a-muchos con joins, grafos cuando todo puede estar relacionado con todo.
- El impedance mismatch motiva el modelo de documentos; la normalización (evitar duplicación con IDs) favorece el relacional.
- Documentos y grafos suelen no reforzar esquema (schema-on-read); el relacional lo hace al escribir (schema-on-write); ambos enfoques tienen ventajas según la heterogeneidad de los datos.
- La locality beneficia a los documentos cuando se usa el documento entero, pero penaliza documentos grandes; relacional y documentos convergen (soporte de JSON/XML y joins).
- Los lenguajes declarativos (SQL, Cypher, SPARQL) son más concisos, ocultan la implementación y permiten optimización y paralelismo, frente a las APIs imperativas de IMS/CODASYL.
- MapReduce queda entre ambos (funciones puras map/reduce); MongoDB terminó añadiendo la aggregation pipeline declarativa, "reinventando SQL".
- El debate documentos-vs-relacional repite el de IMS (jerárquico) y CODASYL (network) de los 70; los grafos, pese al parecido, difieren de CODASYL y se consultan con Cypher, SPARQL o Datalog.
