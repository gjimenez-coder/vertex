# Capítulo 2 — Data Models and Query Languages (Modelos de datos y lenguajes de consulta) — Estudio

## Tarjetas de repaso

P: ¿Por qué son tan importantes los modelos de datos según Kleppmann? / R: Porque condicionan tanto cómo se escribe el software como la forma de pensar el problema.

P: ¿Cómo se construyen las aplicaciones en capas respecto al modelo de datos? / R: El mundo real se modela en objetos; estos en un modelo general (JSON, XML, tablas, grafos); el motor lo representa en bytes; y el hardware en corrientes y campos. Cada capa oculta la complejidad de la inferior.

P: ¿Para qué tipo de relaciones encaja mejor cada modelo? / R: Documentos para datos autocontenidos con uno-a-muchos (árbol); relacional para muchos-a-uno y muchos-a-muchos con joins; grafos cuando casi todo puede estar relacionado con todo.

P: ¿Qué es el impedance mismatch (desajuste objeto-relacional)? / R: La capa de traducción incómoda entre los objetos del código y el modelo de tablas, filas y columnas; los ORM (ActiveRecord, Hibernate) lo reducen pero no lo eliminan.

P: ¿Qué es la normalización y qué idea clave encierra? / R: Eliminar duplicación almacenando una sola vez la información con significado para humanos y referenciándola por un ID que nunca necesita cambiar.

P: ¿Qué diferencia hay entre schema-on-read y schema-on-write? / R: Schema-on-read tiene estructura implícita interpretada al leer (análogo a tipado dinámico); schema-on-write tiene esquema explícito verificado al escribir (análogo a tipado estático).

P: ¿Qué es NoSQL y qué lo impulsó? / R: El intento de los años 2010 de destronar al modelo relacional ("Not Only SQL"); impulsado por mayor escalabilidad, preferencia por software libre, consultas especializadas y frustración con la rigidez de esquemas.

P: ¿Qué ventaja aporta la storage locality de un documento? / R: Si la aplicación necesita el documento entero, evita múltiples búsquedas en varias tablas; pero penaliza documentos grandes porque se cargan y reescriben completos.

P: ¿Qué diferencia a un lenguaje declarativo de uno imperativo? / R: El imperativo indica qué operaciones hacer y en qué orden; el declarativo especifica solo el patrón del resultado y deja al query optimizer decidir índices, joins y orden.

P: ¿Qué ventajas tiene lo declarativo frente a lo imperativo? / R: Es más conciso, oculta detalles de implementación (la base mejora sin cambiar consultas) y se presta al paralelismo, importante porque las CPU crecen en núcleos.

P: ¿Qué es MapReduce y de qué naturaleza es? / R: Modelo de programación para procesar grandes volúmenes en bloque sobre muchas máquinas; ni declarativo ni plenamente imperativo, con funciones puras map y reduce.

P: ¿Qué es un property graph? / R: Grafo donde cada vértice tiene id, aristas entrantes/salientes y propiedades, y cada arista tiene id, vértice de cola, de cabeza, una etiqueta y propiedades.

P: ¿Qué es el modelo triple-store? / R: Toda la información son enunciados de tres partes (sujeto, predicado, objeto); el objeto puede ser un valor primitivo (propiedad) u otro vértice (arista).

P: ¿Qué lenguajes de consulta de grafos presenta el capítulo? / R: Cypher (Neo4j), SPARQL (triple-stores RDF) y Datalog (Datomic, Cascalog).

P: ¿Qué debate histórico repite la comparación documentos-vs-relacional? / R: El de los años 70 entre IMS (modelo jerárquico) y CODASYL (network model), resuelto por el modelo relacional al exponer los datos sin caminos de acceso.

## Preguntas de autoevaluación

P: ¿Por qué un perfil tipo currículum encaja bien como documento JSON? / R: Porque es mayormente autocontenido, tiene mejor locality (una sola consulta en lugar de varias o un join multitabla) y hace explícita la estructura de árbol de las relaciones uno-a-muchos. (Sección "Modelo relacional frente a modelo de documentos")

P: ¿Por qué las relaciones muchos-a-uno no encajan bien en el modelo de documentos? / R: Porque normalizar requiere joins, que suelen tener soporte débil (al escribir el libro RethinkDB sí, MongoDB no, CouchDB solo en vistas); si no se soportan hay que emularlos con varias consultas en el código. (Sección "Relaciones muchos-a-uno y muchos-a-muchos")

P: ¿En qué se diferenciaba el network model (CODASYL) del relacional respecto al acceso a datos? / R: En CODASYL el único modo de acceder a un registro era seguir un access path desde la raíz, lo que hacía el código inflexible; el relacional expuso los datos en abierto y el query optimizer decide el access path automáticamente. (Sección "¿Repiten historia las bases de datos de documentos?")

P: ¿Cómo se comporta un cambio de formato en schema-on-read frente a schema-on-write? / R: En documentos basta empezar a escribir con los campos nuevos y manejar los viejos en el código; en relacional se hace una migración (ALTER TABLE ... ADD COLUMN, luego UPDATE). (Sección "Flexibilidad de esquema")

P: ¿Por qué map y reduce deben ser funciones puras? / R: Porque solo usan su entrada, no consultan la base ni tienen efectos secundarios, lo que permite ejecutarlas en cualquier orden y reintentarlas tras un fallo. (Sección "Consultas con MapReduce")

P: ¿Por qué expresar una consulta de grafo en SQL resulta difícil? / R: Porque en un grafo el número de joins no se conoce de antemano; desde SQL:1999 se usan recursive common table expressions (WITH RECURSIVE), pero la sintaxis es muy torpe (4 líneas de Cypher equivalen a 29 de SQL). (Sección "Grafos en SQL, triple-stores y Datalog")

P: ¿Por qué los grafos no son un CODASYL redivivo? / R: Porque no imponen esquema de anidamiento, permiten referir directamente a cualquier vértice por id o índice, no ordenan vértices ni aristas, y ofrecen lenguajes declarativos. (Sección "Grafos en SQL, triple-stores y Datalog")

P: ¿Qué moraleja deja la aggregation pipeline de MongoDB 2.2? / R: Que un sistema NoSQL puede acabar reinventando SQL sin darse cuenta, al añadir un lenguaje declarativo con sintaxis JSON y expresividad similar a un subconjunto de SQL. (Sección "Consultas con MapReduce")

## Puntos a dominar

- Distinguir cuándo conviene cada modelo: documentos (uno-a-muchos autocontenido), relacional (muchos-a-uno/muchos-a-muchos con joins) y grafos (todo interconectado).
- Explicar el impedance mismatch y por qué motiva el modelo de documentos.
- Explicar la normalización como eliminación de duplicación mediante IDs que no cambian.
- Diferenciar schema-on-read de schema-on-write y cuándo conviene cada uno según la heterogeneidad de los datos.
- Razonar la ventaja y el coste de la locality en documentos, y por qué conviene mantenerlos pequeños.
- Distinguir lenguajes declarativos (SQL, Cypher, SPARQL) de imperativos (IMS, CODASYL) y las ventajas en concisión, abstracción y paralelismo.
- Situar MapReduce entre lo declarativo y lo imperativo, y entender el papel de las funciones puras.
- Identificar los componentes de un property graph y de un triple-store, y los lenguajes Cypher, SPARQL y Datalog.
- Relacionar el debate documentos-vs-relacional con la historia de IMS (jerárquico) y CODASYL (network).
