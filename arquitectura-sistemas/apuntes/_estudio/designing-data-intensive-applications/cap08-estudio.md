# The Trouble with Distributed Systems (Los problemas de los sistemas distribuidos) — Estudio

## Tarjetas de repaso

P: ¿Qué es un fallo parcial y por qué es tan difícil de tratar?
R: Es cuando unas partes del sistema distribuido fallan de forma impredecible mientras otras funcionan. Su dificultad es que es no determinista: una operación a veces funciona y a veces falla sin aviso, y puedes ni saber si tuvo éxito.

P: ¿Por qué en un solo computador se prefiere un fallo total a un resultado incorrecto?
R: Es una decisión de diseño: se prefiere que el computador se caiga del todo (kernel panic, pantalla azul) antes que devolver datos erróneos, que son difíciles de tratar; así se oculta la realidad física y se presenta un modelo idealizado.

P: ¿En qué se diferencian la filosofía HPC y la del cloud computing ante los fallos?
R: HPC hace checkpoint y reinicia todo el cluster desde el último punto (deja que el fallo parcial escale a total); el cloud usa hardware commodity, es online, no puede detenerse y debe tolerar nodos caídos (rolling upgrade).

P: ¿Qué es una red de paquetes asíncrona?
R: Una red (Ethernet/IP) donde un nodo puede enviar un paquete pero no hay garantía de cuándo llegará ni de si llegará; las formas de fallo (petición perdida, nodo caído, respuesta perdida o retrasada) son indistinguibles entre sí.

P: ¿Por qué elegir mal un timeout es peligroso?
R: Uno largo tarda en detectar el fallo; uno corto puede declarar muerto un nodo solo lento, causando ejecución doble de acciones y transferencia de carga que provoca fallos en cascada.

P: ¿Cuál es la principal causa de la variabilidad del retraso en la red?
R: La formación de colas (queueing): congestión en switches, CPUs ocupadas, VMs pausadas y el control de flujo (backpressure) de TCP, más las retransmisiones de TCP.

P: ¿Qué diferencia hay entre el reloj time-of-day y el reloj monótono?
R: El time-of-day da fecha/hora de calendario, se sincroniza con NTP y puede saltar hacia atrás (no sirve para medir duraciones); el monótono solo avanza y sirve para medir intervalos, pero su valor absoluto no tiene significado ni debe compararse entre máquinas.

P: ¿Por qué es peligroso usar last write wins (LWW) con relojes físicos?
R: Por el skew entre relojes, una escritura causalmente posterior puede llevar marca anterior y descartarse, perdiendo datos silenciosamente; además LWW no distingue escrituras secuenciales de concurrentes.

P: ¿Qué aporta la API TrueTime de Spanner?
R: Devuelve un intervalo [earliest, latest] que contiene con certeza el tiempo real; si dos intervalos no se solapan, un evento ocurrió con certeza después del otro, lo que permite snapshots globales.

P: ¿Qué causas pueden provocar una pausa de proceso prolongada?
R: Pausas stop-the-world del GC, suspensión/migración de VMs, cierre de la tapa de un portátil, cambios de contexto (steal time), acceso síncrono a disco, swapping/thrashing o una señal SIGSTOP accidental.

P: ¿Por qué un nodo no puede fiarse de su propio juicio?
R: Puede sufrir un fallo asimétrico o una pausa larga y "resucitar" sin notar que fue degradado; por eso las decisiones importantes se toman por quórum, normalmente una mayoría absoluta.

P: ¿Qué es un fencing token y cómo protege los datos?
R: Es un número que crece monótonamente que el servidor de locks entrega; el cliente lo incluye en cada escritura y el recurso rechaza tokens menores al ya procesado, impidiendo que un nodo con creencias obsoletas corrompa datos.

P: ¿Qué es un fallo bizantino?
R: Cuando un nodo puede enviar respuestas arbitrarias o corruptas, incluso mentir deliberadamente (p. ej. un token falso); alcanzar consenso así es el Problema de los Generales Bizantinos.

P: ¿Cuáles son los tres modelos de sistema según las suposiciones de temporización?
R: Síncrono (retrasos y error de reloj acotados; poco realista), parcialmente síncrono (síncrono la mayor parte del tiempo pero a veces excede límites; el más realista) y asíncrono (sin suposiciones de temporización).

P: ¿Qué distingue una propiedad de safety de una de liveness?
R: Safety significa "no pasa nada malo" (si se viola, el daño es irreversible y puede señalarse el instante); liveness significa "algo bueno acaba ocurriendo" (suele incluir "eventualmente"). Safety debe cumplirse siempre; liveness admite salvedades.

## Preguntas de autoevaluación

P: ¿Por qué se dice que hay que construir un sistema fiable a partir de componentes no fiables, y qué ejemplos previos cita el libro?
R: Porque en un sistema con miles de nodos es razonable asumir que algo siempre está roto. Ejemplos antiguos: los códigos correctores de errores y TCP sobre IP, aunque TCP no puede eliminar los retrasos de red. (Sección "Fallos y fallos parciales")

P: ¿Qué fórmula de timeout serviría en una red con garantías y por qué no se aplica en redes reales?
R: Con retraso máximo d y tiempo de respuesta r, un timeout razonable sería 2d + r. No se aplica porque las redes asíncronas tienen retrasos no acotados y los servidores no garantizan un tiempo máximo de respuesta. (Sección "Timeouts y retrasos no acotados")

P: ¿Por qué la red telefónica fija puede garantizar un retraso acotado y Ethernet/IP no?
R: La telefonía establece un circuito con ancho de banda fijo reservado, sin colas, así que la latencia máxima es fija; Ethernet/IP son protocolos de paquetes optimizados para tráfico a ráfagas, con colas variables que resultan de un compromiso coste/beneficio. (Sección "Redes síncronas frente a asíncronas")

P: ¿Por qué los relojes incorrectos son más peligrosos que un fallo de CPU o red?
R: Un fallo de CPU o red se nota enseguida, pero un reloj que se desvía gradualmente produce pérdida de datos silenciosa y sutil en lugar de un crash; por eso hay que monitorizar los offsets y declarar muerto el nodo que se desvíe demasiado. (Sección "Relojes poco fiables")

P: Describe el escenario de pausa del hilo que rompe la seguridad de un lease.
R: Un líder comprueba el tiempo restante del lease y luego procesa la petición; si el hilo se pausa 15 s en medio, el lease puede expirar, otro nodo tomar el relevo, y el hilo pausado seguir procesando sin enterarse. (Sección "Pausas de proceso")

P: ¿Por qué se usa una mayoría absoluta como quórum y no otro criterio?
R: Porque solo puede existir una mayoría absoluta (más de la mitad) a la vez, de modo que no caben dos decisiones mayoritarias contradictorias simultáneamente. (Sección "Conocimiento, verdad y mentiras")

P: ¿Por qué debe ser el recurso de almacenamiento quien comprueba el fencing token, y no el cliente?
R: Porque es imprudente asumir que los clientes se comportarán bien; si solo el cliente verifica su propio estado, un cliente rezagado podría igualmente corromper datos. (Sección "El líder y el lock")

P: ¿En qué casos sí importa la tolerancia a fallos bizantinos y por qué el libro los descarta en general?
R: Importa en aeroespacial (corrupción por radiación) y entre organizaciones que no se fían entre sí (Bitcoin, blockchains). El libro los descarta en sistemas de datos del lado servidor porque los nodos son propios, la corrupción es rara y los protocolos bizantinos son complicados y caros. (Sección "Fallos bizantinos")

## Puntos a dominar

- Explicar el fallo parcial no determinista como característica definitoria de los sistemas distribuidos.
- Distinguir las tres fuentes de incertidumbre: redes poco fiables, relojes poco fiables y pausas de proceso.
- Justificar por qué la detección de fallos depende de timeouts imperfectos y cómo mitigarlo (medición experimental, Phi Accrual).
- Diferenciar reloj time-of-day y monótono, y explicar los riesgos de LWW frente a relojes lógicos e intervalos de confianza.
- Argumentar por qué un nodo no puede fiarse de su propio juicio y cómo el quórum (mayoría absoluta) y los fencing tokens lo resuelven.
- Clasificar los modelos de sistema (síncrono, parcialmente síncrono, asíncrono) y de fallo (crash-stop, crash-recovery, bizantino), identificando el par más útil (parcialmente síncrono + crash-recovery).
- Distinguir propiedades de safety y de liveness al razonar sobre la corrección de un algoritmo.
