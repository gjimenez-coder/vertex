# Designing Data-Intensive Applications — Martin Kleppmann (O'Reilly Media, 2017)
## Capítulo 6 — Partitioning (Particionamiento)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Cuando un conjunto de datos o una carga de consultas es demasiado grande para la replicación (capítulo 5), hace falta dividir los datos en particiones, también llamadas *sharding*. Cada registro pertenece normalmente a exactamente una partición, que funciona como una pequeña base de datos propia. La razón principal para particionar es la escalabilidad: colocar particiones en distintos nodos de un clúster *shared-nothing* permite repartir datos y carga de consultas entre muchos discos y procesadores.

El capítulo recorre cómo decidir qué registros van a qué nodos (por rango de clave o por hash), cómo interactúan las particiones con los índices secundarios, cómo se rebalancean las particiones al añadir o quitar nodos, y cómo se enrutan las peticiones al nodo correcto. El objetivo es siempre repartir la carga de forma pareja y evitar el *skew* (reparto desigual) y los *hot spots* (particiones con carga desproporcionada).

Terminología: lo que el libro llama *partition* se llama *shard* en MongoDB, Elasticsearch y SolrCloud; *region* en HBase, *tablet* en Bigtable, *vnode* en Cassandra y Riak, y *vBucket* en Couchbase. El libro usa *partitioning* por ser el término más establecido. El particionamiento suele combinarse con replicación, pero ambas elecciones son en gran medida independientes, así que el capítulo ignora la replicación.

## Particionamiento de datos clave-valor

La meta es repartir datos y carga de forma pareja. Asignar registros a nodos al azar los distribuiría bien, pero obligaría a consultar todos los nodos para leer un ítem, así que se busca algo mejor suponiendo acceso por clave primaria.

- **Por rango de clave (key range):** cada partición posee un rango continuo de claves (como los volúmenes de una enciclopedia). Los límites no tienen por qué estar espaciados de forma uniforme, porque los datos pueden no estarlo; se eligen manualmente o automáticamente. Lo usan Bigtable, HBase, RethinkDB y MongoDB antes de la 2.4. Ventaja: dentro de cada partición las claves van ordenadas, lo que permite *range scans* eficientes (por ejemplo, todas las lecturas de sensores de un mes). Desventaja: ciertos patrones de acceso crean hot spots; si la clave es un *timestamp*, todas las escrituras recientes caen en la misma partición. Solución: anteponer, por ejemplo, el nombre del sensor al timestamp.
- **Por hash de la clave:** una buena función de hash convierte datos sesgados en una distribución uniforme. No necesita ser criptográficamente fuerte: Cassandra y MongoDB usan MD5, Voldemort usa Fowler–Noll–Vo. Las funciones de hash integradas del lenguaje pueden no servir (en Java `Object.hashCode()` y en Ruby `Object#hash` dan valores distintos entre procesos). Se asigna a cada partición un rango de hashes. Desventaja: se pierde el orden, por lo que las *range queries* se vuelven ineficientes (en MongoDB con sharding por hash van a todas las particiones; Riak, Couchbase y Voldemort no soportan range queries sobre la clave primaria).

El libro desaconseja el término *consistent hashing* (definido por Karger et al. para distribuir carga en CDNs): no funciona bien para bases de datos y confunde porque no tiene relación con la consistencia de réplicas ni la de ACID; mejor llamarlo *hash partitioning*.

Cassandra ofrece un compromiso con una clave primaria compuesta: solo la primera parte se hashea para elegir la partición y las demás columnas sirven de índice concatenado para ordenar. Esto habilita modelos uno-a-muchos, como `(user_id, update_timestamp)` para recuperar eficientemente las publicaciones de un usuario en un intervalo.

### Cargas sesgadas y alivio de hot spots

El hash reduce hot spots pero no los elimina: si todas las lecturas y escrituras van a la misma clave (por ejemplo, una celebridad en una red social), todo se enruta a la misma partición. Hoy la mayoría de sistemas no compensan esto automáticamente, así que la aplicación añade, por ejemplo, un número aleatorio de dos dígitos a la clave caliente para repartir las escrituras en 100 claves. El coste: las lecturas deben combinar las 100 claves y hace falta llevar registro de qué claves están divididas.

## Particionamiento e índices secundarios

Un índice secundario no identifica un registro de forma única, sino que busca ocurrencias de un valor (todos los coches rojos, todos los artículos con cierta palabra). No encajan bien con las particiones. Hay dos enfoques:

- **Índice particionado por documento (índice local):** cada partición mantiene su propio índice secundario cubriendo solo sus documentos. Las escrituras tocan una sola partición, pero las lecturas requieren *scatter/gather* sobre todas las particiones y combinar resultados, lo que es propenso a la amplificación de latencia de cola. Lo usan MongoDB, Riak, Cassandra, Elasticsearch, SolrCloud y VoltDB.
- **Índice particionado por término (índice global):** se construye un índice global que cubre todas las particiones, pero también se particiona (por el término mismo, útil para range scans, o por hash del término, mejor reparto). Las lecturas son más eficientes (una sola partición), pero las escrituras son más lentas y complejas porque un documento puede afectar varias particiones del índice; por eso las actualizaciones suelen ser asíncronas (DynamoDB actualiza sus índices secundarios globales en una fracción de segundo normalmente).

## Rebalanceo de particiones

Con el tiempo cambian el throughput, el tamaño del dataset o fallan máquinas, lo que exige mover carga entre nodos: eso es el *rebalancing*. Requisitos mínimos: reparto justo tras rebalancear, seguir aceptando lecturas y escrituras durante el proceso, y mover no más datos de los necesarios.

- **Cómo NO hacerlo — hash mod N:** si N (número de nodos) cambia, casi todas las claves deben moverse, lo que lo hace excesivamente caro.
- **Número fijo de particiones:** crear muchas más particiones que nodos (p. ej. 1.000 particiones en 10 nodos) y asignar varias a cada nodo. Al añadir un nodo, este "roba" unas pocas particiones de cada nodo existente; solo se mueven particiones enteras. El número fijado al inicio es el máximo de nodos posibles, así que hay que elegirlo con holgura pero sin excederse por el overhead. Lo usan Riak, Elasticsearch, Couchbase y Voldemort. Es difícil acertar el número si el tamaño del dataset varía mucho.
- **Particionamiento dinámico:** para rangos de clave (HBase, RethinkDB), las particiones se dividen cuando superan un tamaño (en HBase por defecto 10 GB) y se fusionan si encogen, como en un árbol B. El número de particiones se adapta al volumen. Caveat: una base vacía empieza con una sola partición (un solo nodo activo) hasta la primera división; HBase y MongoDB permiten *pre-splitting*. También sirve para datos por hash (MongoDB desde 2.4).
- **Proporcional al número de nodos:** usado por Cassandra y Ketama, un número fijo de particiones por nodo (256 por defecto en Cassandra). Al unirse un nodo, divide particiones existentes al azar; Cassandra 3.0 introdujo un algoritmo que evita divisiones injustas. Requiere particionamiento por hash y corresponde a la definición original de consistent hashing.

### Rebalanceo automático o manual

Hay un gradiente entre automático total y manual total. El automático es cómodo pero impredecible y peligroso junto a la detección automática de fallos: un nodo sobrecargado puede ser dado por muerto, desencadenando un rebalanceo que empeora la carga y causa un fallo en cascada. Por eso conviene mantener a un humano en el bucle.

## Enrutamiento de peticiones

Al hacer una petición, el cliente debe saber a qué nodo conectarse; esto es un caso de *service discovery*. Hay tres enfoques:

1. El cliente contacta cualquier nodo (p. ej. round-robin); si no posee la partición, reenvía la petición.
2. Todas las peticiones van primero a un *routing tier* que actúa como balanceador consciente de las particiones.
3. El cliente conoce la asignación de particiones a nodos y se conecta directamente.

El problema clave es que el componente que decide el enrutamiento aprenda los cambios de asignación, lo que exige acuerdo entre participantes. Muchos sistemas usan un servicio de coordinación como ZooKeeper (Espresso de LinkedIn vía Helix, HBase, SolrCloud, Kafka; MongoDB usa su propio config server y *mongos*). Cassandra y Riak usan en cambio un protocolo *gossip* entre nodos, evitando la dependencia externa. Couchbase usa el routing tier *moxi*. Para las IPs suele bastar con DNS.

## Ejecución de consultas en paralelo

Lo visto cubre consultas simples sobre una clave (más scatter/gather). Las bases relacionales MPP (procesamiento masivamente paralelo), usadas para analítica, soportan consultas con *joins*, filtrados, agrupaciones y agregaciones: el optimizador las divide en etapas y particiones ejecutables en paralelo en varios nodos. Es un tema especializado que el libro retoma en el capítulo 10.

## Ideas clave

- Particionar reparte datos y carga para escalar más allá de una sola máquina; el enemigo es el *skew* que produce *hot spots*.
- El particionamiento por rango de clave permite range scans eficientes pero arriesga hot spots con claves cercanas; el particionamiento por hash reparte mejor pero destruye el orden.
- Las claves compuestas permiten enfoques híbridos: una parte elige la partición y otra da el orden.
- Los índices secundarios se particionan por documento (local: escritura barata, lectura con scatter/gather) o por término (global: lectura barata, escritura cara y a menudo asíncrona).
- Para rebalancear, `hash mod N` es un antipatrón; mejor un número fijo de particiones, particionamiento dinámico o proporcional a los nodos.
- El rebalanceo automático combinado con detección de fallos puede causar fallos en cascada; conviene supervisión humana.
- El enrutamiento de peticiones se resuelve con nodos que reenvían, un routing tier o clientes conscientes, apoyados en coordinación (ZooKeeper) o gossip.
- Las operaciones que escriben en varias particiones son difíciles de razonar (¿qué pasa si una escritura tiene éxito y otra falla?), tema de capítulos siguientes.
