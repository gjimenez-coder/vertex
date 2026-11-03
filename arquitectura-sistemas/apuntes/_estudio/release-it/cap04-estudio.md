# Stability Antipatterns (Antipatrones de estabilidad) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la idea central del capítulo sobre los fallos? / R: Los fallos son inevitables; en vez de eliminar todas las fuentes de fallo, hay que diseñar para lo que ocurre *después* de que aparece una grieta.

P: ¿Qué dos condiciones convierten grietas pequeñas en fallos totales en la "technology frontier"? / R: La alta complejidad interactiva (high interactive complexity) y el acoplamiento fuerte (tight coupling).

P: ¿Por qué un Integration Point es "the number-one killer of systems"? / R: Cada conexión entre sistemas puede colgar, caer o generar impulsos en el peor momento, y todo proyecto es en realidad un proyecto de integración.

P: ¿Por qué una respuesta lenta es peor que no recibir respuesta? / R: Porque ata recursos (hilos) tanto en el llamador como en el llamado y se propaga hacia arriba como una cascada gradual.

P: ¿Qué es una Chain Reaction (reacción en cadena)? / R: En un farm escalado horizontalmente todos los nodos comparten el mismo defecto; cuando uno cae, su carga se redistribuye a los demás y acelera el siguiente fallo.

P: ¿Qué es un Cascading Failure y por qué se le llama "the number-one crack accelerator"? / R: Una grieta en una capa dispara una grieta en la capa que la llama, normalmente vía hilos bloqueados por pools de recursos agotados; acelera la propagación del fallo.

P: ¿Qué significa "navel-gazing" en Blocked Threads? / R: El proceso sigue corriendo pero todos los hilos esperan un resultado imposible; para el usuario y el negocio es indistinguible de un sistema caído.

P: ¿Por qué "concurrency does not compose"? / R: Añadir sincronización en una subclase (como en RemoteAvailabilityCache) viola el principio de sustitución de Liskov y rompe suposiciones de concurrencia del código base.

P: ¿Qué es un Self-Denial Attack? / R: El sistema (o el sistema extendido que incluye a las personas) conspira contra sí mismo, p. ej. un email de marketing con oferta que se replica a millones o un deep link que salta el CDN (caso Xbox 360).

P: ¿Por qué la comunicación punto a punto sufre Scaling Effects? / R: El número de conexiones crece con el cuadrado de instancias (O(n^2)); con decenas de servidores conviene usar multicast, publish/subscribe o colas de mensajes.

P: ¿Qué es Unbalanced Capacities y por qué no se corrige igualando capacidad? / R: Ratios desajustados entre capas dejan que un servicio inunde a otro; igualar todo malgastaría capital (infraestructura 99% ociosa), así que se hacen resilientes ambos lados.

P: ¿Qué es un Dogpile? / R: Una concentración de demanda (arranque tras deploy, cron a medianoche, cambio de configuration management o pulsos externos sincronizados) que supera con mucho la carga de estado estable.

P: ¿Qué es el antipatrón Force Multiplier? / R: La automatización del "control plane" amplifica movimientos pequeños; un conflicto entre el estado "creído" por la automatización y el real puede derribar el sistema (caso Reddit, 11 ago 2016).

P: ¿En qué consiste Unbounded Result Sets? / R: Consultar y recorrer un result set sin límite; si la consulta devuelve de repente millones de filas, la app agota memoria (caso "Black Monday", tabla JMS con más de diez millones de filas).

P: Según el capítulo, ¿cuál es la causa próxima de casi todos los fallos? / R: Blocked Threads, que además conduce a Chain Reactions y Cascading Failures.

## Preguntas de autoevaluación

P: ¿Cómo llegan los fallos de red y por qué el caso lento es más peligroso? / R: Llegan de forma rápida (connection refused, pocos ms) o lenta (ACK perdido, hilos bloqueados minutos); el lento es peor porque el hilo bloqueado no procesa otras transacciones y, si se bloquean todos, el servidor cae. (Sección: Integration Points)

P: ¿Cuál fue la causa del "problema de las 5 a.m." y qué lección deja? / R: El firewall descartaba conexiones TCP ociosas más de una hora sin avisar; con el pool LIFO quedaban casi todas ociosas de noche. Se resolvió con el dead connection detection de Oracle. Lección: no todo problema se resuelve en el nivel de abstracción donde se manifiesta. (Sección: Integration Points)

P: ¿Por qué la sesión es el "talón de Aquiles" de una app web respecto a los usuarios? / R: Cada usuario ocupa memoria de sesión incluso en su tiempo muerto, y usuarios no deseados (proxies mal configurados, bots que ignoran cookies) crean una sesión por petición, agotando memoria. (Sección: Users)

P: ¿Qué defensas propone el capítulo frente a Cascading Failures? / R: Circuit Breaker (evita llamar al punto problemático) y Timeouts (permite volver de la llamada), además de vigilar servicios con alto fan-in. (Sección: Cascading Failures)

P: ¿Por qué muchos de estos antipatrones no se detectan en QA? / R: Porque el tamaño del entorno y los datos no replican producción (ratios 1:1 vs 10:1, distribuciones power law vs campana de Gauss); hay que diseñarlos fuera y probar con volúmenes realistas. (Secciones: Scaling Effects, Unbalanced Capacities, Unbounded Result Sets)

P: ¿Qué salvaguardas recomienda para el software de automatización (Force Multiplier)? / R: Sospechar del observador si >80% parece caído, aplicar histéresis (arrancar rápido, apagar lento), pedir confirmación ante grandes discrepancias de estado, detectar intentos de crear infinitas instancias e incluir zonas de desaceleración por el lag de arranque. (Sección: Force Multiplier)

P: ¿Qué recetas da el capítulo para acotar un result set en SQL? / R: SQL no tiene sintaxis estándar, pero: TOP en SQL Server, rownum <= 15 en Oracle y LIMIT 15 en MySQL/PostgreSQL; además paginar en el front end y poner límites en otros protocolos (RMI, DCOM, XML-RPC). (Sección: Unbounded Result Sets)

P: ¿Cómo debería reaccionar un sistema ante respuestas lentas propias? / R: Monitorizar su propia performance y considerar Fail Fast: si la media móvil de las últimas transacciones supera el SLA, rechazar peticiones de forma documentada y esperada por los llamadores. (Sección: Slow Responses)

## Puntos a dominar

- Reconocer los trece antipatrones y entender que interactúan entre sí (p. ej. Blocked Threads + Unbalanced Capacities + falta de timeouts = cascada).
- Identificar los diagramas de contexto "butterfly" (2N conexiones) y "spiderweb" (hasta 2^N) y por qué cada conexión es un riesgo.
- Explicar por qué una respuesta lenta ata recursos en ambos lados y por qué en webs genera más tráfico (usuarios pulsan Reload).
- Distinguir Chain Reactions (mismo defecto en un farm) de Cascading Failures (grieta que salta de una capa a la que la llama).
- Conocer las técnicas de gestión de memoria por usuario: weak/soft references y mover la sesión a Memcached/Redis (trade-off tamaño vs latencia).
- Entender los límites de sockets (puerto de 16 bits, ~64.511 conexiones, TIME_WAIT, IP virtuales) frente a millones de usuarios.
- Saber por qué la comunicación punto a punto escala en O(n^2) y cuándo pasar a multicast, publish/subscribe o colas.
- Explicar el fallo de Reddit como conflicto entre el estado creído por la automatización y el real, y las salvaguardas OSHA para el control plane.
- Relacionar los defensores del capítulo siguiente: Circuit Breaker, Timeouts, Bulkheads, Decoupling Middleware y Handshaking.
- Aplicar "Design with skepticism" y el handshaking: no confiar en productores de datos y acotar result sets.
