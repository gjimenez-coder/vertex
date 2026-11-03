# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 9 — Consistency and Consensus (Consistencia y consenso)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber
Los sistemas distribuidos sufren todas las fallas del capítulo 8: pérdida y reordenación de paquetes, relojes imprecisos, pausas y caídas de nodos. En lugar de dejar que el servicio falle, buscamos abstracciones de propósito general con garantías útiles (como hicieron las transacciones con la atomicidad, aislamiento y durabilidad). La abstracción central de este capítulo es el consenso: lograr que todos los nodos se pongan de acuerdo en algo. Alcanzar consenso de forma fiable pese a fallos de red y de procesos es sorprendentemente difícil.

El capítulo recorre tres bloques profundamente enlazados: la linealizabilidad (uno de los modelos de consistencia más fuertes), las garantías de ordenación (causalidad y orden total) y, finalmente, el commit atómico distribuido y el consenso. La tesis es que ordenación, linealizabilidad y consenso son problemas íntimamente relacionados y, en buena medida, reducibles entre sí.

Sales sabiendo qué puede y qué no puede hacerse: cuándo conviene pagar el coste de la linealizabilidad, por qué la consistencia causal es una alternativa más barata, por qué las marcas de tiempo no bastan para imponer unicidad, y cómo los algoritmos de consenso tolerantes a fallos (y servicios como ZooKeeper/etcd) resuelven elección de líder, locks, unicidad y commit atómico. También aprendes por qué el teorema CAP tiene hoy poco valor práctico.

## Garantías de consistencia
La mayoría de las bases replicadas ofrecen al menos consistencia eventual (mejor llamada convergencia): si dejas de escribir, con el tiempo todas las réplicas devolverán el mismo valor. Es una garantía muy débil: no dice cuándo convergen, y una lectura inmediata tras una escritura puede devolver un valor viejo. Esto es difícil para los desarrolladores porque difiere del comportamiento de una variable en un programa de un solo hilo, y los bugs solo aparecen ante fallos de red o alta concurrencia.

Existen modelos más fuertes, pero no son gratis: mayor garantía suele implicar peor rendimiento o menor tolerancia a fallos. La consistencia distribuida (coordinar réplicas ante retardos y fallos) es independiente del aislamiento de transacciones (evitar condiciones de carrera entre transacciones concurrentes), aunque hay cierto solapamiento.

## Linealizabilidad
La linealizabilidad (también consistencia atómica, fuerte, inmediata o externa) hace que el sistema parezca tener una única copia de los datos, con todas las operaciones atómicas. Es una garantía de recencia: en cuanto una escritura se completa, toda lectura posterior debe ver el valor escrito, nunca una caché o réplica obsoleta. El ejemplo de Alice y Bob viendo la final del Mundial 2014 ilustra la violación: Bob recarga tras oír a Alice el resultado y su réplica rezagada aún muestra el partido en juego (PDF p. 347).

Formalizar la idea exige cuidado. Con operaciones `read(x)⇒v`, `write(x,v)⇒r` y `cas(x, vold, vnew)⇒r` sobre un registro, una lectura que se solapa con una escritura puede devolver el valor viejo o el nuevo. Pero se añade una restricción: una vez que una lectura devuelve el valor nuevo, todas las lecturas posteriores (en cualquier cliente) deben devolver el nuevo. Se imagina que existe un punto en el tiempo donde el valor "salta" atómicamente, y las marcas que unen las operaciones solo pueden avanzar en el tiempo, nunca retroceder.

### Linealizabilidad frente a serializabilidad
Son garantías distintas. La serializabilidad es una propiedad de aislamiento de transacciones (que leen y escriben múltiples objetos): garantiza que se comporten como si se hubieran ejecutado en algún orden serial, no necesariamente el real. La linealizabilidad es una garantía de recencia sobre lecturas y escrituras de un registro individual; no agrupa operaciones en transacciones, por lo que no evita por sí sola problemas como el write skew. Una base puede ofrecer ambas (serializabilidad estricta o strong-1SR). El 2PL y la ejecución serial real suelen ser linealizables; el aislamiento de instantáneas serializable (SSI) no lo es, porque lee de una instantánea consistente que, por diseño, no incluye escrituras más recientes.

### Cuándo se necesita linealizabilidad
- Bloqueos y elección de líder: un sistema con replicación de un solo líder debe garantizar un único líder (evitar split brain). El lock debe ser linealizable. ZooKeeper y etcd implementan locks y elección de líder mediante algoritmos de consenso.
- Restricciones de unicidad: un nombre de usuario o email único requiere linealizabilidad, análogo a un compare-and-set. Lo mismo para que un saldo no sea negativo o no se venda el mismo asiento dos veces. Las claves foráneas u otras restricciones pueden implementarse sin linealizabilidad.
- Dependencias temporales entre canales: en el ejemplo de Alice y Bob había un canal adicional (la voz). En un redimensionador de imágenes que recibe la orden por una cola mientras lee la imagen del almacenamiento, si este no es linealizable surge una condición de carrera y las imágenes quedan permanentemente inconsistentes.

### Implementar sistemas linealizables
Una única copia no tolera fallos, así que se usa replicación. Comparando métodos del capítulo 5:
- Un solo líder (potencialmente linealizable): leer del líder o de seguidores síncronos puede serlo, pero no siempre lo es (p. ej. por snapshot isolation, bugs, o un líder "iluso" que ya no lo es). Con replicación asíncrona el failover puede perder escrituras.
- Algoritmos de consenso (linealizable): se parecen a un solo líder pero previenen split brain y réplicas obsoletas; así funcionan ZooKeeper y etcd.
- Multi-líder (no linealizable): procesan escrituras concurrentes en varios nodos con conflictos.
- Sin líder (probablemente no linealizable): los quórum estrictos (w + r > n) no garantizan linealizabilidad por retardos variables; "last write wins" con relojes y los sloppy quorums la arruinan. Se puede forzar con read repair síncrono y lecturas de quórum previas al escribir, pero con coste. Un compare-and-set linealizable no puede lograrse así: requiere consenso.

### El coste de la linealizabilidad y el teorema CAP
Ante una interrupción de red entre centros de datos, una base multi-líder sigue operando (las escrituras se encolan y se intercambian al restaurarse la conexión). Con un solo líder, los clientes conectados a centros seguidores no pueden escribir ni hacer lecturas linealizables: quedan no disponibles hasta reparar el enlace. Esta es la compensación del teorema CAP: si exiges linealizabilidad, las réplicas desconectadas deben esperar o devolver error (no disponibles); si no la exiges, cada réplica puede procesar peticiones de forma independiente (disponible pero no linealizable).

CAP (Brewer, 2000) impulsó un cambio de cultura hacia sistemas shared-nothing (NoSQL), pero hoy tiene poco valor práctico: su definición formal es de alcance muy estrecho (solo linealizabilidad y particiones de red), su noción de disponibilidad es idiosincrática y confusa, y ha sido superado por resultados más precisos. Mejor expresarlo como "Consistent or Available when Partitioned".

Sorprendentemente, pocos sistemas son linealizables en la práctica: ni siquiera la RAM de una CPU multinúcleo lo es (cachés y store buffers asíncronos). El motivo de abandonar la linealizabilidad suele ser el rendimiento, no la tolerancia a fallos: Attiya y Welch prueban que el tiempo de respuesta de lecturas/escrituras linealizables es al menos proporcional a la incertidumbre de los retardos de red. La linealizabilidad es lenta siempre, no solo durante un fallo.

## Garantías de ordenación
La ordenación es un tema recurrente (orden de escrituras en el log del líder, serializabilidad, relojes) y hay conexiones profundas entre ordenación, linealizabilidad y consenso.

### Ordenación y causalidad
La ordenación ayuda a preservar la causalidad: la causa precede al efecto, la pregunta precede a la respuesta, un mensaje se envía antes de recibirse. La relación "happened-before" expresa causalidad: si A ocurrió antes que B, B pudo depender de A; si son concurrentes, ninguno supo del otro. Un sistema que respeta ese orden es causalmente consistente (p. ej. el snapshot isolation).

La causalidad define un orden parcial, no total: algunas operaciones están ordenadas y otras son incomparables (concurrentes), como los conjuntos matemáticos o el historial de Git con ramas y fusiones. La linealizabilidad, en cambio, impone un orden total: no hay operaciones concurrentes. Por eso la linealizabilidad es más fuerte: implica causalidad y la preserva automáticamente incluso entre varios canales de comunicación.

El punto clave: existe un término medio. La consistencia causal es el modelo más fuerte que no se ralentiza por los retardos de red y sigue disponible ante fallos (CAP no aplica). Muchos sistemas que parecen necesitar linealizabilidad en realidad solo necesitan causalidad, que puede implementarse de forma más eficiente. Para capturar dependencias causales se generalizan los version vectors, y la base debe saber qué versión leyó la aplicación.

### Ordenación por números de secuencia
Rastrear todas las dependencias causales es impráctico; mejor usar números de secuencia o marcas de tiempo de un reloj lógico (un contador). Son compactos y dan orden total. Con un solo líder, el log de replicación define un orden total consistente con la causalidad. Sin líder, los generadores habituales (nodos con números pares/impares, marcas de reloj físico, bloques preasignados) escalan mejor pero no son consistentes con la causalidad.

Las marcas de tiempo de Lamport (1978) sí lo son: cada marca es un par (contador, ID de nodo), único y totalmente ordenado. La clave es que cada nodo y cliente lleva el máximo contador visto y lo incluye en cada petición; al recibir un valor mayor, aumenta su contador a ese máximo. Así toda dependencia causal incrementa la marca. A diferencia de los version vectors (que distinguen concurrencia de dependencia), las marcas de Lamport solo imponen orden total y no revelan si dos operaciones son concurrentes, pero son más compactas.

### Las marcas de tiempo no bastan
Para una restricción de unicidad de nombre de usuario, un orden total como Lamport sirve para decidir el ganador después de recopilar todas las operaciones, pero no cuando un nodo debe decidir ahora mismo si acepta un registro: no sabe si otro nodo está creando concurrentemente el mismo nombre con una marca menor, y tendría que consultar a todos los demás (frágil ante fallos). El problema es que el orden total solo emerge tras recopilar todas las operaciones; hace falta saber cuándo ese orden queda finalizado. Eso lo captura la difusión de orden total.

### Difusión de orden total (total order broadcast)
También llamada atomic broadcast, es un protocolo para intercambiar mensajes entre nodos con dos propiedades de seguridad: entrega fiable (si un mensaje llega a un nodo, llega a todos) y entrega totalmente ordenada (todos reciben los mensajes en el mismo orden), incluso ante fallos (reintentando tras reparar la red). ZooKeeper y etcd la implementan, señal de su fuerte conexión con el consenso.

Es justo lo que necesita la replicación de bases de datos: si cada mensaje es una escritura y todas las réplicas las aplican en el mismo orden, quedan consistentes (replicación de máquina de estados). Sirve también para transacciones serializables, y para un servicio de locks con fencing tokens (en ZooKeeper, el zxid monótono). Su rasgo esencial: el orden se fija al entregar los mensajes, no puede insertarse uno retroactivamente; esto la hace más fuerte que la ordenación por marcas de tiempo. Es equivalente a crear un log de solo-adición.

Se puede construir almacenamiento linealizable sobre la difusión de orden total (p. ej. reclamar un nombre de usuario con un cas: añadir un mensaje al log, esperar a recibirlo de vuelta y ganar si el primer mensaje para ese nombre es el tuyo). Esto da escrituras linealizables, pero las lecturas pueden quedar obsoletas (consistencia secuencial); para hacerlas linealizables se secuencian por el log o se usa `sync()`. A la inversa, con un registro linealizable con increment-and-get atómico se construye difusión de orden total (los números no tienen huecos). Se demuestra que un cas/increment-and-get linealizable y la difusión de orden total son ambos equivalentes al consenso.

## Transacciones distribuidas y consenso
El consenso formaliza como: uno o más nodos proponen valores y el algoritmo decide uno. Dos situaciones donde importa: elección de líder (todos deben acordar quién es el líder para evitar split brain y pérdida de datos) y commit atómico (en una transacción que abarca varios nodos, todos deben acordar commit o abort).

### La imposibilidad del consenso (FLP)
El resultado FLP (Fischer, Lynch, Paterson) prueba que ningún algoritmo garantiza consenso si un nodo puede caer, pero solo en el modelo asíncrono (sin relojes ni timeouts). Si se permiten timeouts, detección de fallos aunque sea imperfecta, o números aleatorios, el consenso es resoluble. Así que en la práctica los sistemas distribuidos sí alcanzan consenso.

### Commit atómico y 2PC
En un solo nodo, el commit depende del orden en que se escribe a disco (primero los datos, luego el registro de commit); un único dispositivo lo hace atómico. Con varios nodos no basta enviar commit a cada uno: unos podrían confirmar y otros abortar, violando la atomicidad. Un commit debe ser irrevocable, porque otros ya pueden depender de los datos confirmados.

El two-phase commit (2PC) logra commit atómico entre varios nodos con un coordinador (gestor de transacciones). Fase 1: el coordinador envía un `prepare` a cada participante. Al recibirlo, el participante se asegura de poder confirmar bajo cualquier circunstancia (escribe todo a disco, comprueba conflictos) y, al votar "sí", renuncia al derecho de abortar. Fase 2: si todos votan "sí", el coordinador escribe su decisión a disco (el punto de commit, irrevocable) y envía `commit`; si alguno vota "no", envía `abort`. Hay dos "puntos de no retorno": el voto "sí" del participante y la decisión del coordinador. Es como la ceremonia de matrimonio: tras el "sí quiero" no se puede retractar (PDF p. 379). No confundir 2PC (commit atómico) con 2PL (aislamiento serializable).

Fallo del coordinador: si cae tras recibir votos "sí", los participantes quedan "en duda" (in doubt) y no pueden decidir unilateralmente sin arriesgar inconsistencia; deben esperar a que el coordinador se recupere y lea su log. Por eso 2PC es un protocolo de commit bloqueante. El three-phase commit (3PC) pretende ser no bloqueante pero asume retardos y tiempos de respuesta acotados; el commit atómico no bloqueante requiere un detector de fallos perfecto, inviable con retardos no acotados, así que se sigue usando 2PC.

### Transacciones distribuidas en la práctica y XA
Las transacciones distribuidas tienen mala reputación: problemas operativos y penalización de rendimiento (en MySQL, más de 10 veces más lentas que las de un solo nodo, por el fsync extra y las rondas de red). Hay dos tipos: internas de la base (todos los nodos ejecutan el mismo software; funcionan bastante bien) y heterogéneas (tecnologías distintas, p. ej. una base y un broker de mensajes). Las heterogéneas permiten, por ejemplo, procesamiento exactamente-una-vez: confirmar atómicamente el acuse del mensaje y las escrituras de la base, de modo que un mensaje se reprocese con seguridad tras un fallo.

X/Open XA es el estándar para 2PC entre tecnologías heterogéneas: no es un protocolo de red sino una API en C (con bindings como JTA en Java). El coordinador suele ser una librería cargada en el proceso de la aplicación, con su log en disco local. Si la aplicación cae, las transacciones preparadas quedan en duda. El problema grave es que, mientras una transacción está en duda, mantiene bloqueos (exclusivos sobre filas modificadas y, con 2PL, compartidos sobre filas leídas) que no pueden liberarse, bloqueando otras transacciones durante minutos o indefinidamente. Las transacciones en duda huérfanas obligan a resolución manual por un administrador, y las "decisiones heurísticas" de XA son un eufemismo de "probablemente romper la atomicidad".

Limitaciones de XA: el coordinador es un punto único de fallo si no se replica; convierte servidores sin estado en servidores con estado; es un mínimo común denominador (no detecta deadlocks entre sistemas ni funciona con SSI); y, al requerir respuesta de todos los participantes, amplifica fallos, en contra del objetivo de tolerancia a fallos.

### Consenso tolerante a fallos
Un algoritmo de consenso debe cumplir cuatro propiedades: acuerdo uniforme (dos nodos no deciden distinto), integridad (ningún nodo decide dos veces), validez (si se decide v, v fue propuesto por algún nodo) y terminación (todo nodo que no cae decide algún valor). Las tres primeras son de seguridad; la terminación es de vivacidad y formaliza la tolerancia a fallos. Un "dictador" cumple las tres primeras pero no la terminación si cae (como el coordinador en 2PC). La terminación requiere que menos de la mitad de los nodos fallen (quórum mayoritario); las propiedades de seguridad se mantienen incluso con mayoría caída. Se asume que no hay fallos bizantinos (salvo algoritmos específicos que toleran menos de un tercio de nodos bizantinos).

Los mejores algoritmos tolerantes a fallos son Viewstamped Replication (VSR), Paxos, Raft y Zab. En lugar de decidir un único valor, deciden una secuencia de valores, lo que los convierte en algoritmos de difusión de orden total: esta equivale a rondas repetidas de consenso.

Sobre líder y consenso: un solo líder elegido manualmente es "consenso dictatorial" que no cumple terminación. La elección automática de líder acerca a resolver consenso, pero surge una paradoja: para elegir líder parece hacer falta un líder. Se resuelve con números de época (ballot en Paxos, view en VSR, term en Raft): cada elección recibe una época incrementada y totalmente ordenada; ante conflicto gana la época mayor. Antes de decidir, el líder recoge votos de un quórum, y los quórum de la elección y de la propuesta deben solaparse. Se diferencia de 2PC en que el coordinador no se elige y solo se requiere mayoría (no todos).

Limitaciones del consenso: el voto sobre propuestas es replicación síncrona (coste de rendimiento); requiere mayoría estricta (mínimo 3 nodos para tolerar 1 fallo); la mayoría asume un conjunto fijo de nodos (la membresía dinámica es menos comprendida); y depende de timeouts, por lo que en redes con retardos variables pueden dispararse elecciones frecuentes que degradan el rendimiento (Raft tiene casos límite con enlaces poco fiables).

### Servicios de membresía y coordinación
ZooKeeper y etcd son almacenes clave-valor que mantienen poco dato (cabe en memoria) replicado con difusión de orden total tolerante a fallos. Modelados según Chubby de Google, aportan: operaciones atómicas linealizables (locks vía compare-and-set, como lease con expiración), ordenación total de operaciones (fencing tokens vía zxid), detección de fallos (sesiones con heartbeats y nodos efímeros que se liberan al expirar) y notificaciones de cambios (watches). Solo las operaciones atómicas requieren consenso, pero es la combinación lo que los hace útiles.

Sirven para asignar trabajo a nodos (elegir primario, rebalancear particiones) de forma automática sin intervención humana, y para descubrimiento de servicios (aunque este no requiere consenso; algunos sistemas ofrecen réplicas de solo lectura en caché). ZooKeeper corre en un número fijo de nodos (3 o 5) y "externaliza" la coordinación de muchos clientes. Es parte de la larga historia de los servicios de membresía, que deciden qué nodos están vivos acoplando detección de fallos con consenso.

## Ideas clave
- La linealizabilidad hace que los datos replicados parezcan una única copia con operaciones atómicas (garantía de recencia); es fácil de usar pero lenta, sobre todo con retardos de red grandes.
- La causalidad impone un orden parcial (ramas y fusiones); la consistencia causal es el modelo más fuerte que no se ralentiza por la red ni sacrifica disponibilidad, y CAP no le aplica.
- CAP tiene hoy valor histórico: ante una partición hay que elegir entre consistencia (linealizabilidad) o disponibilidad total; mejor leído como "Consistent or Available when Partitioned".
- Las marcas de tiempo de Lamport dan orden total consistente con causalidad, pero no bastan para una restricción de unicidad: hace falta saber cuándo el orden queda finalizado (difusión de orden total).
- Un compare-and-set linealizable, la difusión de orden total y el consenso son problemas equivalentes y reducibles entre sí.
- El 2PC logra commit atómico distribuido con un coordinador, pero es bloqueante: si el coordinador cae, los participantes quedan en duda reteniendo bloqueos; XA amplifica fallos y causa problemas operativos.
- El consenso tolerante a fallos (Paxos, Raft, Zab, VSR) exige acuerdo, integridad, validez y terminación, requiere mayoría de nodos y usa épocas con quórum para elegir líder y decidir.
- Muchos problemas (cas linealizable, commit atómico, difusión de orden total, locks/leases, membresía, unicidad) se reducen al consenso; conviene usar servicios probados como ZooKeeper en vez de implementarlo uno mismo.
