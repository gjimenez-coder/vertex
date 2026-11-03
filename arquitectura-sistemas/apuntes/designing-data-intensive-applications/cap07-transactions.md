# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 7 — Transactions (Transacciones)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

En los sistemas de datos muchas cosas pueden fallar: el software o el hardware caen a mitad de una escritura, la aplicación se cae, la red se interrumpe, varios clientes escriben a la vez y se pisan, o un cliente lee datos actualizados solo parcialmente. Una transacción agrupa varias lecturas y escrituras en una unidad lógica que se ejecuta como una sola operación: o toda tiene éxito (commit) o falla (abort/rollback) y puede reintentarse con seguridad. Su propósito no es natural, sino simplificar el modelo de programación: la aplicación delega en la base ciertos escenarios de error y concurrencia (las llamadas "garantías de seguridad").

La tesis del capítulo es que las transacciones no son ni enemigas de la escalabilidad ni un requisito absoluto para "aplicaciones serias": tienen ventajas y límites como cualquier otra decisión de diseño. Para decidir si las necesitas, hay que entender exactamente qué garantizan y a qué coste. El capítulo examina con profundidad el control de concurrencia: los tipos de race conditions que aparecen y cómo las bases implementan niveles de aislamiento como read committed, snapshot isolation y serializability.

Sales sabiendo qué significa realmente ACID (y por qué es casi un término de marketing), distinguir operaciones de uno o varios objetos, reconocer anomalías concretas (dirty reads/writes, read skew, lost updates, write skew, phantoms) y los tres caminos para lograr serializabilidad: ejecución serial real, two-phase locking (2PL) y serializable snapshot isolation (SSI). Todo aplica tanto a bases de un solo nodo como distribuidas; los retos propios de lo distribuido se dejan para capítulos posteriores.

## El concepto resbaladizo de transacción y el significado de ACID

Casi todas las bases relacionales y algunas no relacionales soportan transacciones siguiendo el estilo introducido en 1975 por IBM System R, la primera base SQL; la idea apenas ha cambiado en 40 años. Con la popularidad de NoSQL a finales de los 2000, las transacciones fueron la principal víctima: muchas bases las abandonaron o redefinieron la palabra para describir garantías mucho más débiles.

Las garantías se describen con el acrónimo ACID (Atomicity, Consistency, Isolation, Durability), acuñado en 1983 por Theo Härder y Andreas Reuter. En la práctica, la implementación de ACID de una base no equivale a la de otra —hay mucha ambigüedad, sobre todo alrededor del aislamiento—, así que ACID se ha convertido casi en un término de marketing. Los sistemas que no cumplen ACID se llaman a veces BASE (Basically Available, Soft state, Eventual consistency), definición aún más vaga: en el fondo solo significa "no ACID".

- Atomicity: no trata de concurrencia (eso es la I). Describe qué pasa si un cliente hace varias escrituras pero ocurre un fallo a mitad; si la transacción no puede confirmarse, se aborta y la base descarta o deshace lo escrito. Su rasgo definitorio es la capacidad de abortar y descartarlo todo; quizá "abortabilidad" habría sido mejor nombre.
- Consistency: término muy sobrecargado (consistencia de réplica, consistent hashing, linealizabilidad en CAP). En ACID se refiere a una noción de "buen estado" definida por la aplicación mediante invariantes (p. ej., que créditos y débitos cuadren). Es responsabilidad de la aplicación: la base no puede impedir que escribas datos que violen tus invariantes. La C "no pertenece realmente a ACID".
- Isolation: las transacciones concurrentes no deben pisarse. La formalización clásica es la serializabilidad: cada transacción puede fingir que es la única en toda la base, y el resultado tras los commits es el mismo que si se hubieran ejecutado en serie. En la práctica rara vez se usa por su coste (Oracle 11g llama "serializable" a lo que en realidad es snapshot isolation).
- Durability: una vez confirmada una transacción, sus datos no se pierden ni ante fallos. En un nodo suele significar escritura a almacenamiento no volátil con write-ahead log; en bases replicadas, copia a varios nodos. La durabilidad perfecta no existe: ninguna técnica (disco, replicación, backups) da garantías absolutas por sí sola, conviene combinarlas.

## Operaciones de uno y varios objetos

Atomicity e isolation describen qué hace la base cuando un cliente escribe varios objetos en la misma transacción: todo-o-nada (atomicidad) y que otra transacción vea todas o ninguna de esas escrituras, no un subconjunto (aislamiento). Las transacciones multiobjeto son necesarias cuando varios datos deben mantenerse sincronizados. El ejemplo del capítulo es una app de correo que guarda un contador desnormalizado de mensajes no leídos: sin aislamiento, el usuario puede ver el correo nuevo pero un contador en cero (dirty read); sin atomicidad, si la actualización del contador falla, buzón y contador quedan desincronizados.

Las bases relacionales agrupan operaciones por la conexión TCP: todo entre `BEGIN TRANSACTION` y `COMMIT` pertenece a la misma transacción. Muchas no relacionales carecen de este agrupamiento; incluso una API multiobjeto (p. ej. un multi-put) puede tener éxito en unas claves y fallar en otras, dejando un estado parcial.

La atomicidad y el aislamiento también aplican a un solo objeto: los motores de almacenamiento casi siempre los garantizan a nivel de un objeto en un nodo (atomicidad con log de recuperación, aislamiento con un lock por objeto). Algunas bases ofrecen operaciones atómicas más complejas como increment o compare-and-set, útiles para evitar lost updates. Pero esas operaciones de un solo objeto no son transacciones en el sentido habitual; llamarlas "transacciones ligeras" o "ACID" es marketing engañoso.

¿Hacen falta las transacciones multiobjeto? En muchos casos sí: claves foráneas que deben seguir siendo válidas, datos desnormalizados en varios documentos que deben actualizarse juntos, o índices secundarios que son objetos distintos desde el punto de vista transaccional (sin aislamiento, un registro podría aparecer en un índice y no en otro). Se puede vivir sin transacciones, pero el manejo de errores se complica y la falta de aislamiento causa problemas de concurrencia.

### Manejo de errores y aborts

Un rasgo clave de la transacción es poder abortarse y reintentarse con seguridad. Las bases ACID prefieren abandonar una transacción entera antes que dejarla a medias. No todos los sistemas siguen esa filosofía: los de replicación leaderless funcionan a "mejor esfuerzo" y dejan la recuperación a la aplicación. Reintentar es simple pero imperfecto:

- Si la transacción sí tuvo éxito y solo falló el acuse de red, reintentar la ejecuta dos veces (salvo que haya deduplicación a nivel de aplicación).
- Si el error es por sobrecarga, reintentar empeora el problema; conviene limitar reintentos y usar exponential backoff.
- Solo vale reintentar tras errores transitorios (deadlock, violación de aislamiento, cortes de red); tras un error permanente (violación de restricción) es inútil.
- Si la transacción tiene efectos externos (enviar un email), estos pueden ocurrir aunque se aborte; two-phase commit puede ayudar a coordinar varios sistemas.
- Si el proceso cliente muere durante el reintento, se pierde lo que intentaba escribir.

## Niveles de aislamiento débiles

La serializabilidad tiene un coste de rendimiento que muchas bases no quieren pagar, así que es común usar niveles más débiles que protegen de algunas race conditions pero no de todas. Estos bugs son difíciles de encontrar por pruebas (dependen del azar del timing) y han causado pérdidas de dinero reales. La recomendación del libro es entender qué problemas existen y cómo prevenirlos en vez de confiar ciegamente en las herramientas.

### Read committed

Es el nivel más básico y da dos garantías: al leer, solo ves datos confirmados (sin dirty reads); al escribir, solo sobrescribes datos confirmados (sin dirty writes).

- Sin dirty reads: las escrituras de una transacción solo se hacen visibles al resto cuando confirma, y todas a la vez. Evita ver estados parcialmente actualizados y leer datos que luego se deshacen.
- Sin dirty writes: si dos transacciones escriben el mismo objeto, la segunda escritura se retrasa hasta que la primera confirme o aborte. Evita que escrituras conflictivas se mezclen (ejemplo del coche usado: la venta se adjudica a Bob pero la factura va a Alice). No previene, en cambio, el lost update de dos incrementos de contador.

Es el nivel por defecto en Oracle 11g, PostgreSQL, SQL Server 2012 y otros. Los dirty writes se evitan con row-level locks que la transacción retiene hasta confirmar o abortar. Los dirty reads no se evitan con locks de lectura (una escritura larga bloquearía muchas lecturas); en su lugar, la base recuerda el valor antiguo confirmado y entrega ese a los lectores hasta que el nuevo valor se confirma.

### Snapshot isolation y repeatable read

Read committed no evita el read skew (lectura no repetible): si Alice mira sus dos cuentas justo mientras se transfiere dinero entre ellas, puede ver $100 que parecen desaparecer. Es aceptable bajo read committed, pero situaciones como backups o consultas analíticas no toleran esa inconsistencia temporal.

La solución habitual es snapshot isolation: cada transacción lee de un snapshot consistente de la base, es decir, ve todos los datos confirmados al inicio de la transacción, aunque luego cambien. Su principio de rendimiento es "los lectores nunca bloquean a los escritores y los escritores nunca bloquean a los lectores". Se implementa con multi-version concurrency control (MVCC): la base mantiene varias versiones confirmadas de cada objeto. En PostgreSQL cada transacción recibe un `txid` creciente; cada fila lleva `created_by` y `deleted_by`, y un update se traduce internamente en delete + create.

Las reglas de visibilidad construyen el snapshot: se ignoran las escrituras de transacciones en curso al inicio, las de transacciones abortadas y las de transacciones con `txid` posterior; el resto es visible. Un objeto es visible si la transacción que lo creó ya estaba confirmada al empezar el lector y no está marcado para borrado por una transacción confirmada antes de ese momento. Por un desafortunado accidente del estándar SQL, Oracle llama a esto "serializable" y PostgreSQL y MySQL lo llaman "repeatable read"; en la práctica "nadie sabe realmente qué significa repeatable read".

### Evitar lost updates

El lost update ocurre cuando dos transacciones leen-modifican-escriben el mismo valor concurrentemente y una sobrescribe a la otra (incrementar un contador, editar un documento JSON, dos usuarios guardando una wiki). Soluciones:

- Operaciones atómicas de escritura: `UPDATE counters SET value = value + 1 WHERE key = 'foo';` es seguro en la mayoría de bases relacionales; es la mejor opción cuando aplica. Suelen implementarse con un lock exclusivo al leer (cursor stability).
- Bloqueo explícito: la aplicación bloquea las filas a actualizar con `SELECT ... FOR UPDATE`. Funciona, pero es fácil olvidar un lock e introducir una race condition.
- Detección automática de lost updates: permitir ejecución en paralelo y abortar/reintentar si el gestor detecta el problema. Lo hacen PostgreSQL (repeatable read), Oracle (serializable) y SQL Server (snapshot), pero no MySQL/InnoDB. Es menos propenso a errores porque no exige código especial.
- Compare-and-set: actualizar solo si el valor no cambió desde la última lectura; hay que comprobar que la base no lea el `WHERE` de un snapshot antiguo.

En bases replicadas (multi-leader o leaderless) no hay una única copia actualizada, así que locks y compare-and-set no aplican. Lo habitual es permitir versiones conflictivas (siblings) y resolverlas después; las operaciones atómicas conmutativas (incrementos, añadir a un conjunto) funcionan bien, como en los datatypes de Riak 2.0. El método last write wins (LWW), por defecto en muchas bases, es propenso a perder actualizaciones.

### Write skew y phantoms

El write skew es más sutil: dos transacciones leen los mismos objetos y actualizan objetos distintos. Ejemplo: dos médicos de guardia (Alice y Bob) piden baja a la vez; cada transacción comprueba que hay dos o más de guardia (bajo snapshot isolation ambas ven 2), ambas confirman y se quedan sin nadie de guardia. Es una generalización del lost update. Las opciones son más limitadas: las operaciones atómicas de un objeto no sirven, la detección de lost updates tampoco, y las restricciones multiobjeto rara vez existen. Si no se puede usar aislamiento serializable, la segunda mejor opción es bloquear explícitamente las filas de las que depende la transacción con `SELECT ... FOR UPDATE`.

Más ejemplos: reserva de salas (doble reserva), movimientos en un juego multijugador, reclamar un nombre de usuario (aquí sí basta una restricción de unicidad) y evitar gastar de más (double-spending). Todos siguen el patrón: un `SELECT` comprueba una condición, la aplicación decide según el resultado y escribe algo que cambia la premisa de esa decisión. Cuando la escritura añade una fila que coincide con una condición que antes no devolvía filas, no hay objeto al que fijar el lock: ese efecto se llama phantom. Snapshot isolation evita phantoms en lecturas, pero en transacciones de lectura-escritura provocan casos difíciles de write skew. Una técnica de último recurso es materializar conflictos (crear filas-lock artificiales, p. ej. una tabla de slots de salas), pero es fea y propensa a errores; es preferible un nivel serializable.

## Serializabilidad

Es el nivel más fuerte: garantiza que, aunque las transacciones corran en paralelo, el resultado sea el mismo que si se ejecutaran una a una. Si cada transacción es correcta por separado, lo sigue siendo en concurrencia. Como los niveles débiles son difíciles de razonar y no hay buenas herramientas para detectar race conditions, la respuesta de los investigadores desde los 70 ha sido: usa aislamiento serializable. Hay tres técnicas para implementarlo.

### Ejecución serial real

Eliminar la concurrencia ejecutando una transacción a la vez en un solo hilo. Se volvió viable hacia 2007 por dos cambios: la RAM barata permite tener el dataset activo en memoria, y las transacciones OLTP suelen ser cortas (las analíticas, largas y de solo lectura, corren aparte sobre un snapshot). Lo usan VoltDB/H-Store, Redis y Datomic. Para aprovechar el único hilo, las transacciones no pueden ser interactivas (esperar al usuario o ir sentencia a sentencia por red sería lentísimo): se envían de golpe como stored procedures. Los procedimientos almacenados tenían mala fama (lenguajes propietarios y arcaicos, difíciles de depurar y versionar, sensibles al rendimiento), pero las implementaciones modernas usan lenguajes de propósito general (VoltDB con Java/Groovy, Datomic con Java/Clojure, Redis con Lua). VoltDB también los usa para replicación, exigiendo que sean deterministas.

Para escalar más allá de un núcleo se puede particionar: si cada transacción toca una sola partición, cada partición tiene su propio hilo y el throughput escala linealmente con los núcleos. Las transacciones que cruzan particiones necesitan coordinación y son mucho más lentas (VoltDB reporta ~1.000 escrituras cross-partition por segundo). En resumen, la ejecución serial sirve si cada transacción es pequeña y rápida, el dataset activo cabe en memoria, y la escritura la maneja un núcleo o se particiona sin coordinación cruzada.

### Two-Phase Locking (2PL)

Durante unos 30 años fue el único algoritmo serializable usado ampliamente (no confundir con two-phase commit). Refuerza los locks: varias transacciones pueden leer un objeto a la vez, pero en cuanto alguien quiere escribirlo necesita acceso exclusivo. Los escritores bloquean a lectores y viceversa. Se implementa con un lock por objeto en modo compartido (lectura) o exclusivo (escritura); la transacción retiene los locks hasta el final (de ahí "dos fases": adquirir y luego liberar). Al usar tantos locks aparecen deadlocks, que la base detecta y resuelve abortando una transacción, que la aplicación debe reintentar.

Su gran inconveniente es el rendimiento: menor concurrencia, latencias inestables y colas cuando hay contención; una sola transacción lenta puede frenar el sistema. Para evitar phantoms necesita predicate locks (locks sobre todos los objetos que cumplen una condición, incluso los que aún no existen). Como no rinden bien, la mayoría de bases usan index-range locks (next-key locking), una aproximación que bloquea un rango de un índice; si no hay índice adecuado, se cae al lock de toda la tabla.

### Serializable Snapshot Isolation (SSI)

Algoritmo relativamente nuevo (descrito en 2008) que da serializabilidad completa con poco coste sobre snapshot isolation. Lo usa PostgreSQL (desde 9.1) y, de forma similar, FoundationDB. A diferencia del control pesimista de 2PL y la ejecución serial, SSI es optimista: deja que las transacciones avancen sin bloquear y, al confirmar, comprueba si se violó el aislamiento; si es así, aborta y reintenta. Rinde mal con alta contención, pero mejor que los pesimistas si hay capacidad de sobra.

SSI parte de snapshot isolation y añade la detección de una "premisa desactualizada": una transacción decide según lo que leyó, pero el dato puede haber cambiado al confirmar. La base detecta dos casos: lecturas de una versión MVCC obsoleta (una escritura ignorada se confirmó después) y escrituras que afectan lecturas previas (usando algo parecido a index-range locks, pero que no bloquean, solo actúan como "tripwire" para avisar que lo leído quedó desactualizado). La comprobación se hace al confirmar, evitando abortos innecesarios y preservando las lecturas largas sobre snapshots. Frente a 2PL, no hay que esperar locks y la latencia es más predecible; frente a la ejecución serial, no se limita a un núcleo (FoundationDB distribuye la detección). SSI requiere que las transacciones de lectura-escritura sean cortas, pero tolera mejor las lentas que 2PL o la ejecución serial.

## Ideas clave

- Una transacción agrupa lecturas y escrituras en una unidad con garantía todo-o-nada; reduce una gran clase de errores a "aborta y reintenta" y simplifica el modelo de programación.
- ACID (Atomicity, Consistency, Isolation, Durability) es impreciso en la práctica: la C es responsabilidad de la aplicación y el término se ha vuelto casi marketing; BASE solo significa "no ACID".
- Las operaciones de un solo objeto (increment, compare-and-set) no son transacciones reales; las transacciones multiobjeto importan para claves foráneas, datos desnormalizados e índices secundarios.
- Anomalías por orden de fuerza: dirty reads y dirty writes (los evita read committed), read skew (lo evita snapshot isolation con MVCC), lost updates (algunas implementaciones de snapshot los detectan), write skew y phantoms (solo los evita la serializabilidad).
- Snapshot isolation lee de un snapshot consistente vía MVCC con el lema "lectores no bloquean a escritores y viceversa"; se llama confusamente "serializable" (Oracle) o "repeatable read" (PostgreSQL, MySQL).
- El write skew surge cuando dos transacciones leen lo mismo y escriben objetos distintos invalidando una premisa; los phantoms son escrituras que cambian el resultado de una búsqueda de otra transacción.
- Solo el aislamiento serializable previene todas las race conditions; se implementa con ejecución serial real, two-phase locking (2PL) o serializable snapshot isolation (SSI).
- 2PL es pesimista (bloquea, con riesgo de deadlocks y mal rendimiento); la ejecución serial exige transacciones cortas y datos en memoria; SSI es optimista y promete serializabilidad con bajo coste, apto para cargas de lectura intensiva.
