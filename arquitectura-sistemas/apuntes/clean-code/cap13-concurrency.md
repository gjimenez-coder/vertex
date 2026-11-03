# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 13 — Concurrency (Concurrencia)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo, escrito por Brett L. Schuchert, trata de por qué necesitamos la concurrencia, de lo difícil que es hacerla bien y de cómo escribir código concurrente limpio. La tesis central es que escribir programas concurrentes limpios es muy difícil: es fácil escribir código multihilo que parece correcto en la superficie pero está roto a un nivel más profundo y solo falla bajo estrés. Se presenta como un panorama general, con un tutorial más detallado en "Concurrency II" para quien necesite profundizar.

La concurrencia es ante todo una estrategia de desacoplamiento: separa *qué* se hace de *cuándo* se hace. En aplicaciones de un solo hilo, el *qué* y el *cuándo* están tan acoplados que el estado de toda la aplicación suele deducirse del stack backtrace. Desacoplarlos puede mejorar el rendimiento y la estructura, haciendo que la aplicación parezca muchos pequeños ordenadores colaborando en lugar de un gran bucle principal.

Sales sabiendo los motivos para adoptar concurrencia, los mitos que la rodean, un conjunto de principios de defensa (SRP, limitar datos compartidos, copias de datos, hilos independientes, conocer la librería y los modelos de ejecución), y una serie de recomendaciones para probar código con hilos.

## Why Concurrency?

Además de los beneficios estructurales (por ejemplo, el modelo de Servlets de aplicaciones web, donde cada ejecución vive en su propio mundo bajo un contenedor web/EJB), hay motivos de rendimiento y tiempo de respuesta:

- Un agregador de información de un solo hilo que visita muchos sitios web en secuencia; al crecer los sitios, el proceso diario supera las 24 horas. Un algoritmo multihilo puede atacar varios sitios a la vez, aprovechando la espera en los sockets de I/O.
- Un sistema que atiende un usuario a la vez (un segundo por usuario) se vuelve lento al crecer la cola; atender muchos usuarios concurrentemente mejora el tiempo de respuesta.
- Un sistema que procesa grandes conjuntos de datos puede procesar cada conjunto en un ordenador distinto, en paralelo.

El desacoplamiento que ofrecen los contenedores web es lejos de perfecto: el programador debe estar muy atento para que sus programas concurrentes sean correctos.

## Myths and Misconceptions

Mitos comunes que el capítulo desmonta:

- "La concurrencia siempre mejora el rendimiento." Solo lo mejora cuando hay mucho tiempo de espera que compartir entre varios hilos o procesadores, y ninguna de esas situaciones es trivial.
- "El diseño no cambia al escribir programas concurrentes." En realidad el diseño de un algoritmo concurrente puede ser muy distinto; desacoplar el *qué* del *cuándo* afecta enormemente a la estructura.
- "No importa entender la concurrencia si usas un contenedor." Más vale saber qué hace tu contenedor y cómo protegerte frente a actualizaciones concurrentes y deadlock.

Afirmaciones equilibradas: la concurrencia implica sobrecarga (rendimiento y código extra); la concurrencia correcta es compleja incluso para problemas simples; sus bugs no suelen ser reproducibles y se ignoran como casos aislados; y a menudo requiere un cambio fundamental en la estrategia de diseño.

## Challenges

Con la clase trivial `X` que tiene `getNextId()` devolviendo `++lastIdUsed`, si dos hilos comparten una instancia (con `lastIdUsed = 42`) hay tres resultados posibles: 43/44 (y campo 44), 44/43 (y campo 44), o el sorprendente 43/43 (y campo 43), que ocurre cuando los hilos se pisan. Hay muchos caminos posibles a través de esa línea de Java. Trabajando solo con el byte-code generado hay 12.870 caminos de ejecución posibles para dos hilos en ese método; si `lastIdUsed` pasa de `int` a `long`, suben a 2.704.156. La mayoría dan resultados válidos, pero algunos no.

## Concurrency Defense Principles

- **Single Responsibility Principle (SRP):** el código relacionado con concurrencia tiene su propio ciclo de vida y sus propios retos; merece separarse del resto. *Recomendación: mantén tu código de concurrencia separado del resto.*
- **Limitar el alcance de los datos:** usa `synchronized` para proteger secciones críticas, pero restringe su número; cuantos más sitios actualizan datos compartidos, más fácil es olvidar proteger alguno, duplicar esfuerzo (violar DRY) y dificultar el diagnóstico. *Recomendación: lleva al corazón la encapsulación; limita severamente el acceso a datos compartidos.*
- **Usar copias de datos:** evita compartir; copia objetos como solo lectura, o recoge resultados en copias por hilo y fúndelos en un solo hilo. El ahorro de evitar el lock intrínseco suele compensar la creación y recolección de basura extra.
- **Los hilos deben ser lo más independientes posible:** que cada hilo viva en su mundo, con sus datos en variables locales y sin compartir nada (como los subtipos de `HttpServlet` que reciben todo por `doGet`/`doPost`). *Recomendación: particiona los datos en subconjuntos independientes operables por hilos independientes.*

## Know Your Library

Java 5 aporta mejoras: usa las colecciones thread-safe, el executor framework para tareas no relacionadas, soluciones no bloqueantes cuando se pueda, y recuerda que varias clases de librería no son thread-safe. Doug Lea escribió *Concurrent Programming in Java* y sus colecciones pasaron al paquete `java.util.concurrent`. `ConcurrentHashMap` rinde mejor que `HashMap` en casi todas las situaciones y permite lecturas/escrituras concurrentes simultáneas. *Recomendación: familiarízate con `java.util.concurrent`, `java.util.concurrent.atomic` y `java.util.concurrent.locks`.*

Definiciones de apoyo: `ReentrantLock` (lock adquirido en un método y liberado en otro), `Semaphore` (lock con cuenta), `CountDownLatch` (lock que espera varios eventos), recursos acotados (bound resources), exclusión mutua, starvation (inanición), deadlock, livelock.

## Know Your Execution Models

Tres problemas clásicos de los que suelen ser variantes la mayoría de problemas concurrentes:

- **Producer-Consumer:** productores ponen trabajo en una cola acotada y consumidores lo retiran; se señalan mutuamente (cola no vacía / no llena) y pueden esperar a ser notificados.
- **Readers-Writers:** un recurso compartido que sirve sobre todo a lectores y ocasionalmente lo actualizan escritores; el reto es equilibrar throughput y evitar starvation e información obsoleta, sin que los escritores bloqueen a los lectores demasiado tiempo.
- **Dining Philosophers:** filósofos en torno a una mesa que necesitan dos tenedores para comer; sustituye filósofos por hilos y tenedores por recursos y aparecen deadlock, livelock y degradación de throughput y eficiencia.

*Recomendación: aprende estos algoritmos básicos y entiende sus soluciones.*

## Beware Dependencies Between Synchronized Methods

Las dependencias entre métodos sincronizados causan bugs sutiles: `synchronized` protege un método individual, pero con más de un método sincronizado sobre la misma clase compartida el sistema puede ser incorrecto. *Recomendación: evita usar más de un método sobre un objeto compartido.* Si debes hacerlo, hay tres formas de corregirlo: **client-based locking** (el cliente bloquea el servidor abarcando desde el primer al último método), **server-based locking** (un método en el servidor que bloquea, llama a todos los métodos y desbloquea) y **adapted server** (un intermediario que hace el bloqueo cuando no se puede cambiar el servidor original).

## Keep Synchronized Sections Small

`synchronized` introduce un lock; todas las secciones guardadas por el mismo lock garantizan un único hilo a la vez. Los locks son caros (retrasos y sobrecarga), así que no conviene llenar el código de ellos, pero las secciones críticas deben protegerse. Hacer secciones críticas muy grandes es un error ingenuo: extender la sincronización más allá del mínimo aumenta la contención y degrada el rendimiento. *Recomendación: mantén tus secciones sincronizadas lo más pequeñas posible.*

## Writing Correct Shut-Down Code Is Hard

Apagar con elegancia (graceful shutdown) es difícil y suele dar deadlock: hilos esperando una señal que nunca llega. Ejemplos: un padre que espera a hijos que nunca terminan por estar bloqueados; o un par productor/consumidor donde el productor se apaga rápido y el consumidor queda bloqueado esperando un mensaje, sin poder recibir la señal de apagado. *Recomendación: piensa pronto en el apagado y hazlo funcionar pronto; te llevará más de lo que crees.*

## Testing Threaded Code

Probar no garantiza corrección, pero una buena prueba minimiza el riesgo. *Recomendación: escribe pruebas con potencial de exponer problemas y ejecútalas con frecuencia, con distintas configuraciones de programa, sistema y carga; si fallan, rastrea el fallo y no lo ignores.* Recomendaciones de grano fino:

- **Trata los fallos espurios como posibles problemas de hilos:** no los descartes como casos aislados ("one-offs"); mejor asumir que los one-offs no existen.
- **Haz funcionar primero el código no concurrente:** aísla POJOs ajenos a los hilos y pruébalos fuera del entorno concurrente; no persigas bugs de hilos y no-hilos a la vez.
- **Haz tu código enchufable (pluggable):** ejecutable con uno o varios hilos, con objetos reales o dobles de prueba (rápidos, lentos, variables) y por un número de iteraciones.
- **Haz tu código ajustable (tunable):** permite afinar el número de hilos, incluso en ejecución, y considera el autoajuste según throughput y utilización.
- **Ejecuta con más hilos que procesadores:** fomenta el intercambio de tareas y expone secciones críticas faltantes o deadlocks.
- **Ejecuta en distintas plataformas:** los sistemas operativos tienen distintas políticas de hilos (la experiencia de OS X frente a Windows XP en VM lo demostró); prueba en todos los entornos de despliegue.
- **Instrumenta tu código para forzar fallos:** inserta llamadas a `Object.wait()`, `sleep()`, `yield()`, `priority()` para alterar el orden de ejecución. Puede ser **hand-coded** (a mano, con sus inconvenientes: hay que encontrar los sitios, ralentiza producción y es un enfoque de escopetazo) o **automated** (con AOP, CGLIB o ASM; por ejemplo una clase `ThreadJigglePoint` con `jiggle()` que elige al azar entre no hacer nada, dormir o ceder). La herramienta **ConTest** de IBM hace algo similar con más sofisticación. *Recomendación: usa estrategias de "jiggling" para sacar a la luz errores.*

## Ideas clave

- La concurrencia es una estrategia de desacoplamiento (*qué* vs. *cuándo*); escribir código concurrente limpio es muy difícil.
- Desconfía de los mitos: no siempre mejora el rendimiento, el diseño sí cambia y entender la concurrencia importa aunque uses un contenedor.
- Una sola línea como `++lastIdUsed` compartida entre dos hilos genera miles de caminos de ejecución, algunos incorrectos.
- Aplica el SRP: separa el código consciente de hilos del ignorante de hilos (POJOs); limita y encapsula los datos compartidos, usa copias y hilos independientes.
- Conoce tu librería (`java.util.concurrent`) y los algoritmos fundamentales: Producer-Consumer, Readers-Writers y Dining Philosophers.
- Evita depender de varios métodos sincronizados sobre el mismo objeto; si es inevitable, usa client-based, server-based o adapted server locking.
- Mantén las secciones sincronizadas mínimas; el apagado con elegancia es más difícil de lo que parece.
- Prueba con muchas configuraciones y plataformas, repetidamente, e instrumenta ("jiggle") el código para forzar fallos antes de producción.
