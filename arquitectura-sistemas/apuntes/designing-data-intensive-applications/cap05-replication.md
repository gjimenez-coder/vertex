# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 5 — Replication (Replicación)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

La replicación consiste en mantener copias de los mismos datos en varias máquinas conectadas por red. Se hace por tres motivos: acercar los datos geográficamente a los usuarios (reducir latencia), mantener el sistema funcionando aunque fallen partes (disponibilidad) y escalar el número de máquinas que atienden lecturas (throughput de lectura). El capítulo asume que el dataset cabe entero en cada máquina; la partición se trata en el capítulo 6.

Si los datos no cambian, replicar es trivial: se copian una vez. Toda la dificultad está en gestionar los cambios. El capítulo examina los tres algoritmos que usan casi todas las bases de datos distribuidas: replicación con un líder (single-leader), con varios líderes (multi-leader) y sin líder (leaderless), con sus ventajas y desventajas.

Sales sabiendo cómo funciona cada esquema, el papel de la replicación síncrona frente a la asíncrona, cómo se gestionan los fallos de nodos y el failover, los problemas que causa el retraso de replicación (replication lag) y las garantías de consistencia que mitigan sus anomalías (read-after-write, monotonic reads, consistent prefix reads), además de cómo detectar y resolver escrituras concurrentes.

## Líderes y seguidores

Cada nodo que guarda una copia se llama réplica. La solución más común es la replicación basada en líder (leader-based, también active/passive o master–slave):

1. Una réplica es el líder (master o primary). Los clientes envían sus escrituras al líder, que primero las graba en su almacenamiento local.
2. Las demás réplicas son seguidores (followers, read replicas, slaves o hot standbys). El líder envía cada cambio a los seguidores mediante un log de replicación o flujo de cambios; cada seguidor aplica las escrituras en el mismo orden que el líder.
3. Las lecturas pueden ir al líder o a cualquier seguidor, pero las escrituras solo las acepta el líder.

Este modo está integrado en muchas bases relacionales (PostgreSQL desde 9.0, MySQL, Oracle Data Guard, SQL Server AlwaysOn) y no relacionales (MongoDB, RethinkDB, Espresso). También lo usan brokers de mensajes como Kafka y RabbitMQ.

### Replicación síncrona frente a asíncrona

Un detalle clave es si la replicación es síncrona o asíncrona. Con replicación síncrona el líder espera la confirmación del seguidor antes de reportar éxito: garantiza que el seguidor tiene una copia actualizada, pero si el seguidor no responde, el líder debe bloquear todas las escrituras hasta que vuelva. Por eso es impráctico que todos los seguidores sean síncronos. En la práctica se activa en un solo seguidor (configuración semi-síncrona): si el síncrono falla, se promueve otro asíncrono. Así siempre hay copia actualizada en al menos dos nodos.

A menudo se configura todo asíncrono: el líder sigue procesando aunque los seguidores se retrasen, pero si el líder falla sin recuperación, se pierden las escrituras no replicadas (la durabilidad no está garantizada aun habiéndose confirmado al cliente). Pese a ello, la replicación asíncrona es muy usada, sobre todo con muchos seguidores o geográficamente distribuidos. Como línea de investigación, la replicación en cadena (chain replication) es una variante síncrona usada, por ejemplo, en Microsoft Azure Storage.

### Configurar nuevos seguidores y gestionar fallos de nodos

Para añadir o reemplazar seguidores no basta copiar archivos, porque los datos cambian constantemente. El proceso, normalmente sin downtime, es: tomar un snapshot consistente del líder (asociado a una posición exacta del log: log sequence number en PostgreSQL, binlog coordinates en MySQL), copiarlo al nuevo seguidor, y que este pida al líder todos los cambios posteriores hasta ponerse al día (caught up).

Cualquier nodo puede caer por fallo o mantenimiento planificado. El objetivo es mantener el sistema funcionando con el menor impacto posible.

- Fallo de un seguidor (catch-up recovery): cada seguidor guarda en disco su log de cambios; al reiniciar, sabe cuál fue la última transacción procesada, se reconecta al líder y pide los cambios que se perdió.
- Fallo del líder (failover): hay que promover un seguidor a líder, reconfigurar a los clientes y hacer que los demás seguidores consuman del nuevo líder. El failover puede ser manual o automático. El automático suele seguir tres pasos: detectar que el líder ha fallado (normalmente por timeout, p. ej. 30 segundos sin respuesta), elegir un nuevo líder (por elección o por un nodo controlador; el mejor candidato es el de datos más actualizados, un problema de consenso) y reconfigurar el sistema para usarlo.

El failover tiene muchos riesgos:

- Con replicación asíncrona, el nuevo líder puede no tener todas las escrituras del antiguo. Lo habitual es descartar las no replicadas, violando expectativas de durabilidad. Es peligroso si hay sistemas externos coordinados: en un incidente de GitHub, un seguidor MySQL desactualizado fue promovido y reutilizó claves primarias que ya estaban en un store Redis, lo que expuso datos privados a usuarios equivocados.
- Dos nodos pueden creerse líder a la vez: situación llamada split brain, peligrosa si ambos aceptan escrituras sin resolución de conflictos. Algunos sistemas apagan un nodo si detectan dos líderes (fencing, o STONITH), pero si se diseña mal pueden acabar apagados los dos.
- Elegir el timeout correcto es difícil: muy largo retrasa la recuperación; muy corto provoca failovers innecesarios que pueden empeorar la situación.

No hay soluciones fáciles; por eso algunos equipos prefieren failover manual.

### Implementación de los logs de replicación

- Statement-based: el líder reenvía cada sentencia (INSERT, UPDATE, DELETE) y cada seguidor la ejecuta. Falla con funciones no deterministas (NOW(), RAND()), columnas autoincrementales, dependencias del estado existente y efectos secundarios (triggers). MySQL la usaba antes de 5.1.
- Write-ahead log (WAL) shipping: el líder envía el mismo log de bajo nivel (qué bytes cambiaron en qué bloques) que usa el motor de almacenamiento. La usan PostgreSQL y Oracle. El inconveniente es que queda acoplada al motor: si cambia el formato de almacenamiento, no suele poderse ejecutar versiones distintas en líder y seguidores, lo que impide upgrades sin downtime.
- Logical (row-based) log: usa un formato distinto para la replicación, desacoplado del motor, a nivel de fila (binlog de MySQL en modo row-based). Permite versiones o motores distintos en líder y seguidores y es más fácil de parsear por sistemas externos (base de la técnica de change data capture, capítulo 11).
- Trigger-based: mueve la replicación a la capa de aplicación mediante triggers y procedimientos almacenados (Databus para Oracle, Bucardo para Postgres). Más flexible, pero con mayor overhead y más propensa a errores.

## Problemas con el retraso de replicación

En cargas con muchas lecturas y pocas escrituras (habitual en web), se crean muchos seguidores y se reparten las lecturas (arquitectura read-scaling). Esto solo funciona con replicación asíncrona: si un seguidor va retrasado, el cliente puede leer datos obsoletos. La inconsistencia es temporal: si se deja de escribir, los seguidores se ponen al día. Este efecto es la consistencia eventual (eventual consistency). El término "eventual" es deliberadamente vago: el retraso (replication lag) suele ser de fracciones de segundo, pero puede llegar a segundos o minutos si el sistema está al límite o hay problemas de red. El capítulo describe tres anomalías y sus garantías.

### Read-after-write (lee tus propias escrituras)

Si un usuario escribe (al líder) y lee justo después de un seguidor retrasado, puede parecer que su dato se perdió. La garantía read-after-write (o read-your-writes) asegura que cada usuario ve siempre sus propias actualizaciones, sin prometer nada sobre las de otros. Técnicas: leer del líder lo que el usuario pueda haber modificado (p. ej. su propio perfil); leer del líder durante un minuto tras la última actualización; o que el cliente recuerde el timestamp de su última escritura y se sirva solo desde réplicas al día. Con varios datacenters o varios dispositivos del mismo usuario (cross-device read-after-write) aumenta la complejidad: los metadatos deben centralizarse y conviene enrutar las peticiones al mismo datacenter.

### Monotonic reads y consistent prefix reads

Monotonic reads evita que un usuario vea el tiempo ir hacia atrás: si lee de un seguidor poco retrasado y luego de uno muy retrasado, un dato que ya había visto podría desaparecer. La garantía asegura que, en lecturas sucesivas de un mismo usuario, no se lea algo más antiguo tras haber leído algo más nuevo. Se logra haciendo que cada usuario lea siempre de la misma réplica (p. ej. elegida por hash del ID de usuario).

Consistent prefix reads evita violaciones de causalidad: si una secuencia de escrituras ocurre en cierto orden, quien las lea debe verlas en ese mismo orden (como en el diálogo donde la respuesta aparece antes que la pregunta). Es un problema típico de bases particionadas, donde las particiones operan independientemente sin orden global. Una solución es escribir las operaciones causalmente relacionadas en la misma partición, o rastrear explícitamente las dependencias causales.

Como tratar estas anomalías en el código de aplicación es complejo y propenso a errores, es mejor que la base ofrezca garantías más fuertes. Para eso existen las transacciones: permiten simplificar la aplicación. Muchos sistemas distribuidos las abandonaron por coste, aceptando consistencia eventual; el libro matizará esa visión en capítulos posteriores (7 y 9).

## Replicación con varios líderes (multi-leader)

El esquema de un solo líder tiene una gran desventaja: si no puedes conectar con el líder, no puedes escribir. La extensión natural es permitir que más de un nodo acepte escrituras (multi-leader, master–master o active/active); cada líder actúa a la vez como seguidor de los demás.

Casos de uso:

- Operación multi-datacenter: un líder por datacenter. Frente al esquema de un solo líder, mejora el rendimiento (cada escritura se procesa en el datacenter local y se replica asíncronamente), tolera mejor la caída de un datacenter entero y aguanta mejor los problemas de la red entre datacenters. Se implementa a menudo con herramientas externas (Tungsten Replicator para MySQL, BDR para PostgreSQL, GoldenGate para Oracle). Su gran inconveniente es que la misma dato puede modificarse en dos datacenters y hay que resolver conflictos; por eso se considera terreno peligroso.
- Clientes con operación offline: apps (p. ej. calendario) que deben funcionar sin conexión. Cada dispositivo es un líder con base local y sincroniza asíncronamente; equivale a multi-leader entre datacenters con red muy poco fiable. CouchDB está diseñado para esto.
- Edición colaborativa en tiempo real (Etherpad, Google Docs): cambios aplicados al instante en la réplica local y replicados asíncronamente. Con bloqueo equivale a single-leader; sin bloqueo y con cambios pequeños trae los retos del multi-leader.

### Gestión de conflictos de escritura

El mayor problema del multi-leader es el conflicto: dos usuarios cambian el mismo registro a la vez y el conflicto solo se detecta asíncronamente, cuando ya es tarde para pedir ayuda al usuario. Hacer la detección síncrona eliminaría la ventaja del multi-leader (daría igual usar un solo líder).

- Evitar conflictos: enrutar siempre todas las escrituras de un registro al mismo líder (cada usuario con su datacenter "de casa"). Es lo más recomendado, aunque se rompe si hay que cambiar de líder.
- Converger a un estado consistente: toda réplica debe acabar con el mismo valor. Opciones: last write wins (LWW) por ID/timestamp más alto (popular pero propenso a perder datos), dar precedencia por ID de réplica (también pierde datos), fusionar valores (p. ej. concatenar "B/C") o registrar el conflicto en una estructura explícita para resolverlo después.
- Lógica de resolución personalizada, ejecutada on write (controlador en segundo plano, p. ej. Bucardo con Perl) o on read (se guardan todas las versiones y se devuelven al leer, como CouchDB). La resolución suele aplicarse por fila o documento, no por transacción.

La resolución automática incluye CRDTs (datatypes libres de conflicto, en Riak 2.0), estructuras persistentes fusionables (merge de tres vías, estilo Git) y la transformación operacional (operational transformation), algoritmo tras Etherpad y Google Docs. Algunos conflictos son sutiles, como reservas solapadas de una sala creadas en líderes distintos.

### Topologías multi-líder

Una topología describe los caminos por los que se propagan las escrituras. Con más de dos líderes hay varias: all-to-all (cada líder envía a todos los demás), circular (MySQL por defecto: cada nodo recibe de uno y reenvía a otro) y en estrella (un nodo raíz reenvía al resto, generalizable a árbol). En circular y estrella una escritura pasa por varios nodos; para evitar bucles infinitos, cada escritura se etiqueta con los identificadores de los nodos por los que ha pasado. El fallo de un nodo en circular o estrella interrumpe la replicación; all-to-all es más tolerante, pero sus mensajes pueden adelantarse unos a otros y llegar en orden incorrecto (problema de causalidad, p. ej. una actualización antes que su insert). Los timestamps no bastan por la falta de sincronía de relojes; se usan version vectors. La detección de conflictos está mal implementada en muchos sistemas multi-líder.

## Replicación sin líder (leaderless)

Algunos sistemas abandonan el concepto de líder y permiten que cualquier réplica acepte escrituras del cliente. Lo popularizó el sistema Dynamo de Amazon; Riak, Cassandra y Voldemort son datastores de código abierto de estilo Dynamo. El cliente envía la escritura a varias réplicas (o lo hace un nodo coordinador que no impone orden).

### Quórums, read repair y escrituras concurrentes

Si una réplica está caída, el cliente escribe en paralelo a todas y basta con que w respondan; al leer, consulta varias en paralelo y usa números de versión para saber cuál es más nueva. Para que una réplica caída se ponga al día se usan dos mecanismos: read repair (el cliente detecta valores obsoletos al leer y reescribe el valor más nuevo) y anti-entropy (un proceso en segundo plano copia datos faltantes entre réplicas, sin orden fijo). Voldemort no tiene anti-entropy, por lo que los valores poco leídos pueden tener durabilidad reducida.

Con n réplicas, una escritura necesita w confirmaciones y una lectura consulta r nodos. Si `w + r > n` se espera leer siempre un valor actualizado, porque los conjuntos de nodos escritos y leídos se solapan. Opción común: n impar (3 o 5) y w = r = (n+1)/2. Con n=3, w=2, r=2 se tolera un nodo caído. Aun con `w + r > n` pueden devolverse valores obsoletos en casos límite: sloppy quorums, escrituras concurrentes, lecturas concurrentes con escrituras, escrituras parcialmente fallidas no revertidas o restauración desde una réplica antigua. Los quórums no garantizan en la práctica las garantías de read-after-write, monotonic reads ni consistent prefix reads; para eso hacen falta transacciones o consenso. Conviene monitorizar la obsolescencia (staleness), más difícil sin orden fijo de escrituras.

Un sloppy quorum acepta w/r respuestas en nodos que no son los "de casa" del valor cuando una interrupción de red impide alcanzar el quórum; cuando se arregla, el hinted handoff reenvía esas escrituras a los nodos correctos. Aumenta la disponibilidad de escritura, pero no garantiza leer el último valor. Leaderless también sirve para operación multi-datacenter (Cassandra, Voldemort, Riak).

Como varios clientes escriben a la vez, hay conflictos aunque se usen quórums estrictos. LWW (único método en Cassandra, opcional en Riak) logra convergencia pero pierde datos; solo es seguro si cada clave se escribe una vez y es inmutable (p. ej. clave UUID). Para decidir si dos operaciones son concurrentes se usa la relación happens-before: A ocurre antes que B si B conoce, depende o se construye sobre A; son concurrentes si ninguna conoce a la otra (no importa el tiempo físico). El servidor mantiene un número de versión por clave: al leer devuelve todos los valores no sobrescritos y la versión; al escribir, el cliente incluye la versión de su lectura previa y fusiona los valores recibidos. Así ningún dato se descarta en silencio, pero los clientes deben fusionar los valores concurrentes (siblings en Riak). Una fusión por unión puede hacer reaparecer ítems borrados; para evitarlo se usa un marcador de borrado (tombstone). Con varias réplicas se usa un número de versión por réplica y por clave; el conjunto de todos ellos es el version vector (la variante dotted version vector se usa en Riak 2.0), que distingue sobrescrituras de escrituras concurrentes.

## Ideas clave

- La replicación sirve para alta disponibilidad, operación desconectada, menor latencia y escalabilidad de lecturas; la dificultad está en gestionar los cambios.
- Hay tres enfoques: single-leader (fácil, sin conflictos), multi-leader y leaderless (más robustos ante fallos y latencia, pero con garantías de consistencia débiles y conflictos que resolver).
- La replicación asíncrona es rápida pero puede perder escrituras confirmadas si el líder falla; la síncrona garantiza copias al día a costa de bloquear ante fallos.
- El failover es delicado: riesgo de perder escrituras, split brain y timeouts mal ajustados.
- Los logs de replicación pueden ser statement-based, WAL shipping, logical (row-based) o trigger-based; el logical desacopla la replicación del motor.
- El retraso de replicación causa anomalías que se mitigan con read-after-write, monotonic reads y consistent prefix reads.
- En leaderless, los quórums `w + r > n` buscan solapamiento entre lecturas y escrituras, con read repair y anti-entropy para converger; sloppy quorums priorizan disponibilidad.
- La concurrencia se define por la relación happens-before; los version vectors detectan escrituras concurrentes y evitan perder datos si los siblings se fusionan bien.
