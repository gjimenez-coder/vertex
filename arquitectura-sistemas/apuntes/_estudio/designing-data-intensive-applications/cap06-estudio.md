# Partitioning (Particionamiento) — Estudio

## Tarjetas de repaso

P: ¿Qué es el particionamiento (partitioning o sharding) y para qué sirve?
R: Dividir los datos en particiones cuando el dataset o la carga son demasiado grandes para la replicación; cada registro pertenece normalmente a una sola partición. Su razón principal es la escalabilidad: repartir datos y carga de consultas entre varios nodos de un clúster shared-nothing.

P: ¿Qué nombres recibe una "partition" en distintos sistemas?
R: shard (MongoDB, Elasticsearch, SolrCloud), region (HBase), tablet (Bigtable), vnode (Cassandra, Riak) y vBucket (Couchbase).

P: ¿Qué son el skew y los hot spots?
R: El skew es un reparto desigual de la carga; un hot spot es una partición con carga desproporcionada. Son los problemas que el particionamiento busca evitar.

P: ¿Cómo funciona el particionamiento por rango de clave (key range) y cuál es su ventaja y desventaja?
R: Cada partición posee un rango continuo de claves con límites no necesariamente uniformes. Ventaja: las claves van ordenadas, permitiendo range scans eficientes. Desventaja: ciertos patrones (p. ej. clave timestamp) concentran escrituras recientes en una partición, creando hot spots.

P: ¿Cómo funciona el particionamiento por hash de la clave y qué pierde?
R: Una buena función de hash convierte datos sesgados en una distribución uniforme y se asigna a cada partición un rango de hashes. No necesita ser criptográficamente fuerte (Cassandra y MongoDB usan MD5; Voldemort usa Fowler–Noll–Vo). Desventaja: se pierde el orden, por lo que las range queries se vuelven ineficientes.

P: ¿Por qué el libro desaconseja el término "consistent hashing"?
R: Fue definido por Karger et al. para distribuir carga en CDNs, no funciona bien para bases de datos y confunde porque no tiene relación con la consistencia de réplicas ni la de ACID; mejor llamarlo hash partitioning.

P: ¿Qué permite la clave primaria compuesta de Cassandra?
R: Solo la primera parte se hashea para elegir la partición y las demás columnas sirven de índice concatenado para ordenar, habilitando modelos uno-a-muchos como (user_id, update_timestamp).

P: ¿Cómo se alivian los hot spots sobre una clave caliente concreta?
R: La aplicación añade, por ejemplo, un número aleatorio de dos dígitos a la clave caliente para repartir las escrituras en 100 claves; el coste es que las lecturas deben combinar las 100 claves y hay que registrar qué claves están divididas.

P: ¿Qué es un índice particionado por documento (índice local) y su compromiso?
R: Cada partición mantiene su propio índice secundario sobre solo sus documentos. Las escrituras tocan una sola partición, pero las lecturas requieren scatter/gather sobre todas las particiones, propenso a amplificación de latencia de cola.

P: ¿Qué es un índice particionado por término (índice global) y su compromiso?
R: Un índice global que cubre todas las particiones pero también se particiona (por el término o por su hash). Lecturas más eficientes (una sola partición), pero escrituras más lentas y complejas, a menudo asíncronas (DynamoDB).

P: ¿Por qué "hash mod N" es un antipatrón para rebalancear?
R: Si N (número de nodos) cambia, casi todas las claves deben moverse, lo que lo hace excesivamente caro.

P: ¿En qué consiste la estrategia de número fijo de particiones?
R: Crear muchas más particiones que nodos (p. ej. 1.000 en 10 nodos) y asignar varias a cada nodo; al añadir un nodo este roba particiones enteras de los existentes. El número inicial es el máximo de nodos posibles. Lo usan Riak, Elasticsearch, Couchbase y Voldemort.

P: ¿Qué es el particionamiento dinámico?
R: Las particiones se dividen al superar un tamaño (10 GB por defecto en HBase) y se fusionan si encogen, como en un árbol B, adaptando su número al volumen. Caveat: una base vacía empieza con una sola partición hasta la primera división, mitigable con pre-splitting.

P: ¿Cuáles son los tres enfoques de enrutamiento de peticiones (service discovery)?
R: 1) el cliente contacta cualquier nodo que reenvía si no posee la partición; 2) todas las peticiones van a un routing tier consciente de las particiones; 3) el cliente conoce la asignación y se conecta directamente.

P: ¿Qué son las bases relacionales MPP?
R: Bases de procesamiento masivamente paralelo usadas para analítica; el optimizador divide consultas con joins, filtrados, agrupaciones y agregaciones en etapas y particiones ejecutables en paralelo en varios nodos.

## Preguntas de autoevaluación

P: ¿Por qué no se asignan los registros a nodos al azar aunque reparta bien los datos?
R: Porque obligaría a consultar todos los nodos para leer un ítem; se busca algo mejor suponiendo acceso por clave primaria. (Sección "Particionamiento de datos clave-valor")

P: Si eliges una clave timestamp para particionar por rango, ¿qué problema surge y cómo se resuelve?
R: Todas las escrituras recientes caen en la misma partición, creando un hot spot. Se resuelve anteponiendo, por ejemplo, el nombre del sensor al timestamp. (Sección "Particionamiento de datos clave-valor")

P: ¿Elimina el particionamiento por hash todos los hot spots?
R: No; si todas las lecturas y escrituras van a la misma clave (p. ej. una celebridad), todo se enruta a la misma partición, y la mayoría de sistemas no lo compensan automáticamente. (Sección "Cargas sesgadas y alivio de hot spots")

P: ¿Qué enfoque de índice secundario elegirías si las escrituras son frecuentes y debes minimizar su coste?
R: El índice particionado por documento (local), porque las escrituras tocan una sola partición; el coste se traslada a las lecturas con scatter/gather. (Sección "Particionamiento e índices secundarios")

P: ¿Por qué el rebalanceo automático puede ser peligroso junto a la detección automática de fallos?
R: Un nodo sobrecargado puede ser dado por muerto, desencadenando un rebalanceo que aumenta la carga sobre los demás nodos y causa un fallo en cascada; por eso conviene mantener a un humano en el bucle. (Sección "Rebalanceo automático o manual")

P: ¿Cuál es el problema central del enrutamiento de peticiones y cómo lo abordan los sistemas?
R: Que el componente que decide el enrutamiento aprenda los cambios de asignación, lo que exige acuerdo entre participantes; se usa coordinación como ZooKeeper (HBase, SolrCloud, Kafka) o un protocolo gossip entre nodos (Cassandra, Riak). (Sección "Enrutamiento de peticiones")

P: ¿Por qué las funciones de hash integradas del lenguaje pueden no servir para particionar?
R: Porque pueden dar valores distintos entre procesos; en Java Object.hashCode() y en Ruby Object#hash no son consistentes entre procesos. (Sección "Particionamiento de datos clave-valor")

## Puntos a dominar

- Distinguir cuándo y por qué particionar: escalar más allá de una máquina evitando skew y hot spots.
- Comparar particionamiento por rango de clave (range scans eficientes, riesgo de hot spots) frente a por hash (mejor reparto, sin orden).
- Entender el papel de las claves compuestas como enfoque híbrido (una parte elige partición, otra ordena).
- Diferenciar índice secundario local (por documento) frente a global (por término) y sus compromisos de lectura/escritura.
- Reconocer las estrategias de rebalanceo: evitar hash mod N; usar número fijo de particiones, dinámico o proporcional a los nodos.
- Conocer los tres enfoques de enrutamiento y el rol de ZooKeeper o gossip en la coordinación.
- Recordar que las escrituras en varias particiones son difíciles de razonar (éxito parcial), tema de capítulos siguientes.
