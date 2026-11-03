# Capítulo 7 — Transactions (Transacciones) — Estudio

## Tarjetas de repaso

P: ¿Qué es una transacción y para qué sirve?
R: Agrupa varias lecturas y escrituras en una unidad lógica que se ejecuta como una sola operación: o toda tiene éxito (commit) o falla (abort/rollback) y puede reintentarse. Su propósito es simplificar el modelo de programación delegando en la base ciertos escenarios de error y concurrencia.

P: ¿Qué significa el acrónimo ACID y por qué se dice que es casi marketing?
R: Atomicity, Consistency, Isolation y Durability, acuñado en 1983 por Härder y Reuter. Es marketing porque la implementación de ACID de una base no equivale a la de otra; hay mucha ambigüedad, sobre todo en el aislamiento.

P: ¿Qué describe realmente la Atomicity en ACID?
R: No trata de concurrencia, sino de qué pasa si hay un fallo a mitad de varias escrituras: la transacción se aborta y se descarta/deshace lo escrito. Su rasgo definitorio es la abortabilidad.

P: ¿Por qué se dice que la Consistency "no pertenece realmente a ACID"?
R: Porque se refiere a invariantes de "buen estado" definidos por la aplicación (p. ej. que créditos y débitos cuadren) y es responsabilidad de la aplicación; la base no puede impedir que escribas datos que violen tus invariantes.

P: ¿Qué es la serializabilidad como formalización del aislamiento?
R: Cada transacción puede fingir que es la única en la base, y el resultado tras los commits es el mismo que si se hubieran ejecutado en serie. Rara vez se usa por su coste de rendimiento.

P: ¿Por qué las operaciones de un solo objeto (increment, compare-and-set) no son transacciones reales?
R: Porque, aunque los motores garantizan atomicidad y aislamiento a nivel de un objeto en un nodo, llamarlas "transacciones ligeras" o "ACID" es marketing engañoso; las transacciones multiobjeto son las que mantienen sincronizados varios datos.

P: ¿Qué garantías da el nivel read committed?
R: Dos: al leer, solo ves datos confirmados (sin dirty reads); al escribir, solo sobrescribes datos confirmados (sin dirty writes).

P: ¿Cómo evita read committed los dirty reads sin usar locks de lectura?
R: La base recuerda el valor antiguo confirmado y lo entrega a los lectores hasta que el nuevo valor se confirma, evitando que una escritura larga bloquee muchas lecturas.

P: ¿Qué es snapshot isolation y cómo se implementa?
R: Cada transacción lee de un snapshot consistente: ve todos los datos confirmados al inicio, aunque luego cambien. Se implementa con MVCC manteniendo varias versiones confirmadas de cada objeto. Lema: los lectores nunca bloquean a los escritores y viceversa.

P: ¿Qué es un lost update y cuáles son sus soluciones?
R: Dos transacciones leen-modifican-escriben el mismo valor y una sobrescribe a la otra. Soluciones: operaciones atómicas de escritura, bloqueo explícito (SELECT ... FOR UPDATE), detección automática y abort/retry, y compare-and-set.

P: ¿Qué es el write skew y en qué se diferencia del lost update?
R: Dos transacciones leen los mismos objetos pero actualizan objetos distintos, invalidando una premisa (ej. dos médicos que piden baja a la vez). Es una generalización del lost update, con opciones de prevención más limitadas.

P: ¿Qué es un phantom?
R: El efecto en que una escritura añade una fila que coincide con una condición que antes no devolvía filas, de modo que no hay objeto al que fijar un lock. Provoca casos difíciles de write skew en transacciones de lectura-escritura.

P: ¿Cuáles son las tres técnicas para lograr serializabilidad?
R: Ejecución serial real (un solo hilo), two-phase locking (2PL) y serializable snapshot isolation (SSI).

P: ¿Qué caracteriza a 2PL frente a SSI?
R: 2PL es pesimista: bloquea (lectores y escritores se bloquean mutuamente), retiene locks hasta el final, sufre deadlocks y mal rendimiento. SSI es optimista: deja avanzar las transacciones y al confirmar comprueba si se violó el aislamiento, abortando si es necesario.

P: ¿Qué dos casos detecta SSI para abortar una transacción?
R: Lecturas de una versión MVCC obsoleta (una escritura ignorada se confirmó después) y escrituras que afectan lecturas previas (usando algo similar a index-range locks que actúan como "tripwire"); la comprobación se hace al confirmar.

## Preguntas de autoevaluación

P: ¿Por qué las transacciones no son ni enemigas de la escalabilidad ni un requisito absoluto para aplicaciones serias?
R: Porque, como cualquier decisión de diseño, tienen ventajas y límites; para decidir si las necesitas hay que entender exactamente qué garantizan y a qué coste. (Lo que necesitas saber)

P: En el ejemplo de la app de correo con contador desnormalizado, ¿qué problema causa la falta de aislamiento y cuál la falta de atomicidad?
R: Sin aislamiento el usuario puede ver el correo nuevo pero el contador en cero (dirty read); sin atomicidad, si la actualización del contador falla, buzón y contador quedan desincronizados. (Operaciones de uno y varios objetos)

P: ¿Cuándo tiene sentido reintentar una transacción abortada y cuándo no?
R: Solo tras errores transitorios (deadlock, violación de aislamiento, cortes de red); tras un error permanente como violación de restricción es inútil. Además hay que limitar reintentos y usar exponential backoff para no empeorar una sobrecarga. (Manejo de errores y aborts)

P: ¿Por qué read committed no evita el read skew y qué lo soluciona?
R: Porque permite ver un estado temporalmente inconsistente (ej. $100 que parecen desaparecer entre dos cuentas durante una transferencia). Lo soluciona snapshot isolation, útil para backups y consultas analíticas. (Snapshot isolation y repeatable read)

P: ¿Por qué locks y compare-and-set no aplican en bases replicadas multi-leader o leaderless?
R: Porque no hay una única copia actualizada. Lo habitual es permitir versiones conflictivas (siblings) y resolverlas después; las operaciones atómicas conmutativas funcionan bien, mientras que LWW es propenso a perder actualizaciones. (Evitar lost updates)

P: ¿Qué patrón común siguen los ejemplos de write skew (reserva de salas, double-spending, etc.)?
R: Un SELECT comprueba una condición, la aplicación decide según el resultado y escribe algo que cambia la premisa de esa decisión. (Write skew y phantoms)

P: ¿Qué condiciones hacen viable la ejecución serial real y por qué se volvió posible hacia 2007?
R: Es viable si cada transacción es pequeña y rápida, el dataset activo cabe en memoria y la escritura la maneja un núcleo o se particiona sin coordinación cruzada. Se volvió posible por la RAM barata y porque las transacciones OLTP suelen ser cortas. (Ejecución serial real)

P: ¿Por qué la ejecución serial exige stored procedures y no transacciones interactivas?
R: Porque esperar al usuario o ir sentencia a sentencia por red sería lentísimo en un único hilo; se envían de golpe como stored procedures (en implementaciones modernas con lenguajes de propósito general). (Ejecución serial real)

## Puntos a dominar

- Distinguir qué describe cada letra de ACID, en especial que Atomicity trata de abortabilidad (no de concurrencia) y que Consistency es responsabilidad de la aplicación.
- Diferenciar operaciones de un solo objeto (no son transacciones reales) de las transacciones multiobjeto (claves foráneas, datos desnormalizados, índices secundarios).
- Reconocer las anomalías por orden de fuerza: dirty reads/writes (read committed), read skew (snapshot isolation con MVCC), lost updates (detección en algunas implementaciones), write skew y phantoms (solo serializabilidad).
- Explicar cómo read committed evita dirty reads (valor antiguo confirmado) y dirty writes (row-level locks hasta commit).
- Entender MVCC y las reglas de visibilidad que construyen el snapshot (txid, created_by/deleted_by).
- Enumerar las cuatro soluciones al lost update y saber cuándo aplica cada una.
- Comparar las tres técnicas de serializabilidad: ejecución serial real, 2PL (pesimista, deadlocks, predicate/index-range locks) y SSI (optimista, detección de premisa desactualizada al confirmar).
