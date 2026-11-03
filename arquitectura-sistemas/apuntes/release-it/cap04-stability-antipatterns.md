# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 4 — Stability Antipatterns (Antipatrones de estabilidad)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Este capítulo cataloga los antipatrones comunes que crean, aceleran o multiplican las "grietas" que terminan derribando un sistema. Nygard parte de una idea central: los fallos son inevitables ("Everything breaks. Faults are unavoidable"), así que no sirve de nada pretender eliminar todas las fuentes de fallo; hay que diseñar para lo que ocurre *después* de que una grieta aparece. Los sistemas grandes y muy conectados viven en lo que James R. Chiles llama la "technology frontier", donde la alta complejidad interactiva (high interactive complexity) y el acoplamiento fuerte (tight coupling) convierten grietas pequeñas en fallos totales.

La alta complejidad interactiva aparece cuando el sistema tiene tantas piezas y dependencias ocultas que el modelo mental del operador es incompleto o erróneo, de modo que sus acciones instintivas resultan ineficaces o dañinas. El acoplamiento fuerte permite que una grieta en una parte se propague a través de capas y límites de sistema: cuando un componente falla, su carga se redistribuye a sus pares y añade estrés a quienes lo llaman, haciendo más probable el siguiente fallo.

Sales sabiendo reconocer trece antipatrones y entendiendo que no basta con evitarlos: casi todos interactúan entre sí. Los dos "number-one killers" son los Integration Points (fuente número uno de grietas) y las Cascading Failures (acelerador número uno). Los patrones defensivos (Circuit Breaker, Timeouts, Bulkheads, Decoupling Middleware, Handshaking) se detallan en el capítulo siguiente.

## El ejemplo que recorre el capítulo

No hay un único caso hilo conductor, sino varias "war stories" del autor que ilustran cada antipatrón: el problema de las 5 a.m. (firewall que cierra conexiones ociosas de un pool JDBC), los motores de búsqueda que se caían en cadena a mediodía, el ataque de autonegación del preorden de la Xbox 360, el fallo de Reddit del 11 de agosto de 2016 y el "Black Monday" de la tabla de mensajes con diez millones de filas.

## Integration Points (Puntos de integración)

Todo proyecto es un proyecto de integración; sus diagramas de contexto siguen el patrón "butterfly" (un sistema central con muchas entradas y salidas, con `2N` conexiones) o "spiderweb" (muchas cajas, hasta `2^N` conexiones). Cada conexión es un punto de integración que puede colgar, caer o generar impulsos en el peor momento. Son "the number-one killer of systems" (PDF p. 47).

Protocolos sobre sockets: una "connection" es una abstracción (sobre paquetes, que a su vez abstraen electrones). TCP abre conexión con el "three-way handshake" (SYN, SYN/ACK, ACK). Los fallos de red llegan de dos formas: rápidos (connection refused, pocos milisegundos) o lentos (ACK perdido, hilos bloqueados minutos). "Clearly, a slow response is a lot worse than no response" (PDF p. 50): el hilo bloqueado no procesa otras transacciones y, si se bloquean todos, el servidor está caído.

El problema de las 5 a.m.: treinta instancias se colgaban al amanecer. La causa estaba dos capas de abstracción más abajo: el firewall olvidaba conexiones TCP ociosas más de una hora (su tabla es finita), sin avisar a los extremos (dropeaba los paquetes sin ICMP reset). El pool de conexiones usaba una estrategia LIFO, así que de noche 39 de 40 conexiones quedaban ociosas y el firewall las descartaba; al subir el tráfico, se bloqueaban de inmediato. La solución fue el *dead connection detection* de Oracle, cuyo ping mantenía viva la conexión en el firewall. Lección: "not every problem can be solved at the level of abstraction where it manifests" (PDF p. 55).

Protocolos HTTP: REST con JSON sobre HTTP es la lingua franca y hereda todos los problemas de sockets, más los suyos: el proveedor puede no responder, no leer la petición, devolver un status desconocido, un content-type inesperado o decir que envía JSON y mandar otra cosa. Recomendaciones: usar una librería cliente con control fino de timeouts (de conexión y de lectura) y tratar la respuesta como datos hasta confirmar que cumple lo esperado, evitando librerías que mapeen directo a objetos de dominio.

Vendor API Libraries: las librerías cliente de los proveedores rara vez están endurecidas; son código normal con toda su variabilidad de calidad. Tienes poco control sobre ellas y su principal riesgo es el bloqueo (pools internos, lecturas de socket, HTTP, serialización). El ejemplo del callback `messageReceived()` muestra que no se puede saber en qué hilo se ejecuta ni qué locks sostiene: un campo minado de deadlocks.

Para contrarrestarlos: escribir software "cínico" que maneje violaciones de forma y función, construir un test harness por cada integración que devuelva respuestas prefabricadas y simule fallos de red/sistema, y probarlo bajo carga considerable. Patrones: Circuit Breaker, Timeouts, Decoupling Middleware, Handshaking.

## Chain Reactions (Reacciones en cadena)

Ocurren en capas escaladas horizontalmente (farms) donde todos los servidores corren la misma aplicación y comparten el mismo defecto (fuga de recursos o crash por carga). Cuando un nodo cae, los demás asumen su carga: en un farm de ocho, pasar de 12,5% a 14,3% sube la carga de cada superviviente un ~15%, aumentando su probabilidad de caer. Solo se elimina arreglando el defecto de fondo; los Bulkheads pueden partir una reacción en cadena en dos más lentas. El ejemplo de los motores de búsqueda con fuga de memoria muestra crashes que se aceleran (5-6 min, luego 3-4, luego segundos). Defensas: buscar fugas de memoria y bugs de timing, usar autoscaling con health checks y Bulkheads.

## Cascading Failures (Fallos en cascada)

Un fallo en cascada ocurre cuando una grieta en una capa dispara una grieta en la capa que la llama; es "the number-one crack accelerator" (PDF p. 62). Necesita un mecanismo que "salte el hueco", normalmente hilos bloqueados por pools de recursos que se agotan al no retornar ninguna llamada (integration points sin timeout son garantía de cascada). También puede saltar por un hilo demasiado agresivo que reintenta sin distinguir errores transitorios de graves, o por speculative retries que inundan a un proveedor ya lento. Defensas clave: Circuit Breaker (evita llamar al punto problemático) y Timeouts (permite volver de la llamada); vigilar servicios con alto fan-in.

## Users (Usuarios)

Los usuarios "hacen exactamente lo peor en el peor momento". Al crecer el tráfico, superará la capacidad; la pregunta es cómo reacciona el sistema al exceso de demanda.

- **Heap Memory**: cada usuario tiene una sesión que ocupa memoria incluso en su "dead time". Mantén lo mínimo en sesión; usa weak/soft references (`SoftReference` en Java, `WeakReference` en C#, `weakref` en Python) para que el GC pueda reclamar el payload cuando falte memoria; el código debe manejar un `null`.
- **Off-Heap / Off-Host Memory**: mueve la memoria por usuario a otro proceso con Memcached o Redis; es un trade-off entre tamaño direccionable y latencia (jerarquía de memoria).
- **Sockets**: un puerto son 16 bits (máx. 65535); con rango 1024-65535 hay ~64.511 conexiones. Para millones de conexiones se usan IP virtuales. Los sockets cerrados en estado TIME_WAIT (defensa contra "bogons", paquetes errantes) también limitan; dentro del datacenter se puede bajar ese intervalo.
- **Expensive to Serve**: los usuarios que compran disparan integration points (autorización de tarjeta, impuestos, inventario, envío). No hay defensa efectiva salvo probar agresivamente, duplicando o triplicando la proporción de las transacciones más caras.
- **Unwanted Users**: proxies mal configurados y bots que no respetan cookies de sesión crean una sesión por petición. La sesión es el "talón de Aquiles" de las apps web. Las *competitive intelligence companies* raspan datos como "un batallón con portapapeles"; `robots.txt` es solo una convención social. Solo funcionan bloquear por IP/subred (una forma de Circuit Breaker) y la vía legal (términos de uso).
- **Malicious Users**: la mayoría son "script kiddies"; el riesgo principal de estabilidad es el DDoS (vía botnets) que satura tu ancho de banda de salida. Un Circuit Breaker especializado limita el daño por host. Los *advanced persistent threats* son raros pero casi garantizan la brecha.

Lecciones: los usuarios consumen memoria, hacen cosas raras (prueba con fuzzing, property-based o simulation testing en vez de scripts predecibles) y se juntan en multitudes que disparan hangs, deadlocks y race conditions.

## Blocked Threads (Hilos bloqueados)

En lenguajes gestionados (C#, Java, Ruby) el intérprete casi nunca crashea de verdad; el modo de fallo más común es "navel-gazing": el proceso corre pero todos los hilos esperan un resultado imposible. Desde la perspectiva del usuario (y del negocio: "¿genera ingresos?"), un sistema colgado es indistinguible de uno caído, por eso conviene complementar la monitorización interna con monitorización externa (transacciones sintéticas) y métricas.

El problema tiene cuatro partes: demasiadas permutaciones de error para probarlas todas, interacciones inesperadas, timing crucial y que los desarrolladores nunca golpean su app con 10.000 peticiones concurrentes. No se puede "testear fuera del sistema"; hay que escribir el código con cuidado usando primitivas probadas. Nygard desaconseja escribir tu propio connection pool. Sincronizar métodos de objetos de dominio es señal de mal diseño: rompe en más de un servidor y escala peor; mejor objetos de dominio inmutables y CQRS (Command Query Responsibility Separation).

El ejemplo de `RemoteAvailabilityCache` (subclase de `GlobalObjectCache` que sobrescribe `get()` con una llamada remota) muestra cómo interactúan los antipatrones: cuando el sistema de inventario se cayó, un hilo quedó dentro de `create()` esperando para siempre y todos los demás se bloquearon ("waiting endlessly for Godot"). Blocked Threads + Unbalanced Capacities + falta de timeouts = cascada que tiró todo el sitio. "No one designed this failure mode into the combined system, but no one designed it out either" (PDF p. 78). Añadir synchronization en una subclase viola el principio de sustitución de Liskov: "concurrency does not compose".

Lecciones: Blocked Threads es la causa próxima de casi todos los fallos y lleva a Chain Reactions y Cascading Failures; escruta los pools de recursos; usa primitivas probadas; defiéndete con Timeouts (no puedes probar que no hay deadlocks, pero sí que ninguno dure para siempre); desconfía del código que no puedes ver.

## Self-Denial Attacks (Ataques de autonegación)

El sistema (o el sistema extendido que incluye a las personas) conspira contra sí mismo. El ejemplo clásico es el email de marketing con una oferta para un "grupo selecto" que se replica a millones (coupon codes reutilizables). El caso de la Xbox 360: un email con la fecha/hora exacta del preorden y un deep link que saltaba Akamai hizo que el sitio desapareciera "gone in sixty seconds". "Good marketing can kill you at any time" (Paul Lord). También un único servidor rogue puede dañar a todos vía un recurso compartido (lock manager). Defensas: arquitectura shared-nothing, decoupling middleware, recursos compartidos redundantes, modos de fallback (p. ej. de locking pesimista a optimista), "pre-autoscaling" antes del evento y, sobre todo, comunicación interna.

## Scaling Effects (Efectos de escala)

Analogía de la ley del cuadrado-cubo (por qué no hay arañas gigantes). Aparecen en relaciones "many-to-one" o "many-to-few". La **comunicación punto a punto** escala mal: el número de conexiones crece con el cuadrado de instancias (`O(n^2)`); con decenas de servidores conviene reemplazarla por UDP broadcasts, TCP/UDP multicast, publish/subscribe o colas de mensajes (aplica "do the simplest thing that will work"). Los **recursos compartidos** (cluster/lock manager) se vuelven cuello de botella; lo más escalable es shared-nothing (capacidad lineal con los servidores), aunque complica el failover (p. ej. de sesión). Estos defectos no se testean fuera: deben diseñarse fuera, ya que rara vez se puede replicar el tamaño de producción en QA.

## Unbalanced Capacities (Capacidades desbalanceadas)

Ratios desajustados entre capas permiten que un servicio inunde a otro (ej.: front-end de 3.000 hilos contra back-end de 450). Igualar la capacidad de todo sería malgastar capital (infraestructura 99% ociosa). La solución es hacer resilientes a ambos lados: Circuit Breaker en el llamador, Handshaking y Backpressure en el proveedor, Bulkheads para reservar capacidad a llamadores prioritarios. Es un caso especial de Scaling Effects. En QA suele ser 1:1 y en producción 10:1; virtualiza y escala QA, y estresa ambos lados de la interfaz.

## Dogpile

Un dogpile concentra la demanda: la carga de arranque o periódica puede ser mucho mayor que la de estado estable (caches frías golpeando la base de datos al mismo tiempo). Ocurre al arrancar varios servidores tras un deploy, cuando un cron dispara a medianoche o cuando configuration management empuja un cambio; también por "pulsos" externos sincronizados (analogía de los semáforos peatonales). La anécdota del "Colo Workaround" (breaker que salta al arrancar todo a la vez) lo ilustra. Defensas: random clock slew (no todos los cron a medianoche) y backoff creciente para evitar pulsos; en load tests, añadir delta aleatorio a cada pausa.

## Force Multiplier (Multiplicador de fuerza)

La automatización es una palanca que amplifica movimientos pequeños. El fallo de Reddit (11 ago 2016): apagaron el autoscaler para actualizar ZooKeeper, el package management lo reinició, leyó datos parciales de ZooKeeper (reflejando un entorno más pequeño) y apagó muchos servidores; al restaurarlos manualmente, las caches vacías provocaron un dogpile en la base de datos. El fallo emergió del conflicto entre la "creencia" del sistema de automatización y la del administrador ("stuck between two conflicting sets of instructions", como HAL 9000).

Los sistemas de service discovery pueden amplificar fallos: un nodo particionado que no distingue "el universo desapareció" de "tengo una venda" propaga por gossip que cero servicios están disponibles. Este patrón afecta sobre todo al software de "control plane" (logging, monitoring, schedulers, scalers, load balancers, configuration management), que compara estado actual con estado deseado y actúa como robótica industrial. Siguiendo la guía de OSHA para robots, implementa salvaguardas: si >80% del sistema parece caído, sospecha del observador; aplica histéresis (arrancar rápido, apagar lento); pide confirmación cuando la brecha entre estado esperado y observado es grande; detecta intentos de "spin up infinity instances"; incluye zonas de desaceleración por el lag de arranque.

## Slow Responses (Respuestas lentas)

Una respuesta lenta es peor que un error o un rechazo de conexión, porque ata recursos en el llamador y en el llamado. Suelen venir de demanda excesiva o de problemas subyacentes: fugas de memoria (alto CPU por garbage collection), congestión de red (sobre todo en WAN con protocolos muy "chatty") o TCP stalls por buffers mal drenados en protocolos de socket hechos a mano. Se propagan hacia arriba como una cascada gradual. El sistema debería monitorizar su propia performance y considerar Fail Fast: si la media móvil de las últimas transacciones supera el SLA, rechazar peticiones (a nivel aplicación o conexión), siempre documentado y esperado por los llamadores. En sitios web, las respuestas lentas generan *más* tráfico porque los usuarios pulsan Reload.

## Unbounded Result Sets (Conjuntos de resultados sin límite)

"Design with skepticism, and you will achieve resilience": no confíes ciegamente en tu base de datos. El patrón peligroso es consultar y recorrer el result set sin límite; si la consulta devuelve de repente cinco millones de filas, la app agota memoria. El "Black Monday": una tabla de mensajes JMS que debía tener <1.000 filas acumuló más de diez millones; cada instancia hacía `select for update` de todas, agotaba memoria y crasheaba (driver JDBC tipo 2 con código nativo), liberando el lock para que la siguiente instancia cayera igual. Faltaba una cláusula LIMIT.

Es un fallo de handshaking: el llamador deja que el otro sistema dicte términos. TCP limita con el campo "window"; las APIs de búsqueda piden count y offset; SQL no tiene sintaxis estándar pero sí recetas (`TOP` en SQL Server, `rownum <= 15` en Oracle, `LIMIT 15` en MySQL/PostgreSQL). Cuidado con relaciones que acumulan hijos ilimitados (orders→order lines, perfiles→visitas, auditorías) y con distribuciones que cambian de QA a producción (las conexiones por usuario siguen una power law, no una campana de Gauss). Lecciones: usa volúmenes de datos realistas, pagina en el front end (first item + count), no confíes en los productores de datos y pon límites en otros protocolos de aplicación (RMI, DCOM, XML-RPC).

## Ideas clave

- Los fallos son inevitables; diseña para lo que pasa *después* de la grieta, no para eliminar todos los fallos.
- Alta complejidad interactiva + acoplamiento fuerte convierten grietas pequeñas en fallos totales (la "technology frontier").
- Integration Points son la fuente número uno de grietas; Cascading Failures, el acelerador número uno; Blocked Threads, la causa próxima de casi todos los fallos.
- Una respuesta lenta es peor que no responder: ata recursos en ambos lados y propaga cascadas.
- Los antipatrones interactúan: Blocked Threads + Unbalanced Capacities + falta de timeouts producen cascadas que nadie diseñó ni descartó.
- Muchos problemas (Scaling Effects, Unbalanced Capacities, Dogpile, Unbounded Result Sets) no se ven en QA porque el tamaño y los datos no replican producción: hay que diseñarlos fuera y probar con volúmenes realistas.
- La automatización (control plane) es un multiplicador de fuerza que necesita salvaguardas, histéresis y confirmación ante grandes discrepancias de estado.
- Defiéndete con los patrones del capítulo siguiente: Circuit Breaker, Timeouts, Bulkheads, Decoupling Middleware y Handshaking.
