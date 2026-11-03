# Consistency and Consensus (Consistencia y consenso) — Estudio

## Tarjetas de repaso

P: ¿Qué es el consenso y por qué es la abstracción central del capítulo? / R: Lograr que todos los nodos se pongan de acuerdo en algo; alcanzarlo de forma fiable pese a fallos de red y de procesos es sorprendentemente difícil.

P: ¿Qué garantiza la consistencia eventual (convergencia) y por qué es débil? / R: Que si dejas de escribir, con el tiempo todas las réplicas devolverán el mismo valor; es débil porque no dice cuándo convergen y una lectura inmediata tras una escritura puede devolver un valor viejo.

P: ¿Qué es la linealizabilidad? / R: Una garantía de recencia que hace que el sistema parezca tener una única copia de los datos con operaciones atómicas: en cuanto una escritura se completa, toda lectura posterior ve el valor escrito.

P: ¿En qué se diferencian linealizabilidad y serializabilidad? / R: La serializabilidad es una propiedad de aislamiento de transacciones (orden serial de operaciones sobre múltiples objetos); la linealizabilidad es una garantía de recencia sobre lecturas y escrituras de un registro individual.

P: ¿En qué casos se necesita linealizabilidad? / R: Bloqueos y elección de líder (evitar split brain), restricciones de unicidad (nombre/email únicos, saldo no negativo), y dependencias temporales entre canales de comunicación.

P: ¿Qué compensación expresa el teorema CAP? / R: Ante una partición de red hay que elegir entre consistencia (linealizabilidad, réplicas desconectadas no disponibles) o disponibilidad (cada réplica responde pero sin linealizabilidad).

P: ¿Por qué suele abandonarse la linealizabilidad en la práctica? / R: Por rendimiento, no por tolerancia a fallos: Attiya y Welch prueban que el tiempo de respuesta de operaciones linealizables es al menos proporcional a la incertidumbre de los retardos de red; es lenta siempre.

P: ¿Qué expresa la relación "happened-before" y qué tipo de orden define la causalidad? / R: Expresa causalidad (si A ocurrió antes que B, B pudo depender de A); define un orden parcial: algunas operaciones están ordenadas y otras son concurrentes (incomparables).

P: ¿Por qué la consistencia causal es un término medio atractivo? / R: Es el modelo más fuerte que no se ralentiza por los retardos de red y sigue disponible ante fallos (CAP no le aplica); muchos sistemas que parecen necesitar linealizabilidad solo necesitan causalidad.

P: ¿Qué aportan las marcas de tiempo de Lamport y qué les falta? / R: Dan un orden total consistente con la causalidad mediante pares (contador, ID de nodo); pero no revelan si dos operaciones son concurrentes ni bastan para decidir unicidad en el momento (falta saber cuándo el orden queda finalizado).

P: ¿Qué es la difusión de orden total (total order broadcast) y sus dos propiedades de seguridad? / R: Un protocolo para intercambiar mensajes con entrega fiable (si llega a un nodo, llega a todos) y entrega totalmente ordenada (todos reciben los mensajes en el mismo orden), incluso ante fallos.

P: ¿Cómo funciona el two-phase commit (2PC)? / R: Con un coordinador: fase 1 envía `prepare` y cada participante que vota "sí" renuncia a abortar; fase 2, si todos votan "sí" el coordinador escribe su decisión (punto de commit irrevocable) y envía `commit`, si no, `abort`.

P: ¿Por qué 2PC es un protocolo de commit bloqueante? / R: Si el coordinador cae tras recibir votos "sí", los participantes quedan "en duda" y no pueden decidir unilateralmente sin arriesgar inconsistencia; deben esperar a que el coordinador se recupere.

P: ¿Cuáles son las cuatro propiedades de un algoritmo de consenso? / R: Acuerdo uniforme, integridad, validez (seguridad) y terminación (vivacidad, que formaliza la tolerancia a fallos y requiere que menos de la mitad de los nodos fallen).

P: ¿Qué servicios implementan consenso y qué aportan? / R: ZooKeeper y etcd (modelados según Chubby): operaciones atómicas linealizables (locks), ordenación total (fencing tokens vía zxid), detección de fallos (sesiones y nodos efímeros) y notificaciones de cambios (watches).

## Preguntas de autoevaluación

P: ¿Por qué el aislamiento por instantáneas serializable (SSI) no es linealizable? / R: Porque lee de una instantánea consistente que, por diseño, no incluye escrituras más recientes, violando la garantía de recencia. (Sección "Linealizabilidad frente a serializabilidad")

P: ¿Son linealizables los quórum estrictos (w + r > n) en sistemas sin líder? / R: No necesariamente: por retardos variables no garantizan linealizabilidad; "last write wins" con relojes y los sloppy quorums la arruinan, y un compare-and-set linealizable requiere consenso. (Sección "Implementar sistemas linealizables")

P: ¿Por qué CAP tiene hoy poco valor práctico? / R: Su definición formal es de alcance muy estrecho (solo linealizabilidad y particiones de red), su noción de disponibilidad es idiosincrática y confusa, y ha sido superado por resultados más precisos. (Sección "El coste de la linealizabilidad y el teorema CAP")

P: ¿Por qué las marcas de tiempo de Lamport no bastan para una restricción de unicidad en tiempo real? / R: Porque el orden total solo emerge tras recopilar todas las operaciones; un nodo no sabe si otro crea concurrentemente el mismo nombre con una marca menor sin consultar a todos. (Sección "Las marcas de tiempo no bastan")

P: ¿Qué relación hay entre difusión de orden total, cas linealizable y consenso? / R: Son equivalentes y reducibles entre sí: sobre la difusión de orden total se construye almacenamiento linealizable, y con un registro linealizable con increment-and-get atómico se construye difusión de orden total. (Sección "Difusión de orden total")

P: ¿Qué dice el resultado FLP y por qué no impide el consenso en la práctica? / R: Prueba que ningún algoritmo garantiza consenso si un nodo puede caer, pero solo en el modelo asíncrono; con timeouts, detección imperfecta de fallos o números aleatorios el consenso es resoluble. (Sección "La imposibilidad del consenso (FLP)")

P: ¿Cuál es el problema grave de las transacciones en duda con XA? / R: Mientras están en duda mantienen bloqueos que no pueden liberarse, bloqueando otras transacciones durante minutos o indefinidamente, y las huérfanas obligan a resolución manual por un administrador. (Sección "Transacciones distribuidas en la práctica y XA")

P: ¿Cómo resuelven los algoritmos de consenso la paradoja de "para elegir líder hace falta un líder"? / R: Con números de época (ballot/view/term) incrementados y totalmente ordenados; ante conflicto gana la época mayor, y los quórum de elección y de propuesta deben solaparse. (Sección "Consenso tolerante a fallos")

## Checklist

Puntos a dominar:

- Distinguir consistencia eventual (convergencia) de linealizabilidad (recencia, única copia) y de serializabilidad (aislamiento de transacciones).
- Reconocer cuándo se necesita linealizabilidad: locks/elección de líder, restricciones de unicidad y dependencias temporales entre canales.
- Explicar la compensación de CAP y por qué la linealizabilidad es lenta siempre (Attiya y Welch), no solo durante un fallo.
- Diferenciar orden parcial (causalidad) de orden total (linealizabilidad) y ubicar la consistencia causal como término medio sin coste de red.
- Saber qué dan las marcas de tiempo de Lamport y por qué no bastan sin difusión de orden total.
- Justificar la equivalencia entre cas/increment-and-get linealizable, difusión de orden total y consenso.
- Describir las dos fases y los dos puntos de no retorno de 2PC, y por qué es bloqueante ante caída del coordinador.
- Enumerar las limitaciones de XA (punto único de fallo, estado en servidores, mínimo común denominador, amplificación de fallos).
- Recitar las cuatro propiedades del consenso y el requisito de quórum mayoritario, distinguiendo seguridad de terminación.
- Enumerar lo que aportan ZooKeeper/etcd (locks linealizables, fencing tokens, detección de fallos, watches) y por qué conviene usar servicios probados en vez de implementar consenso uno mismo.
