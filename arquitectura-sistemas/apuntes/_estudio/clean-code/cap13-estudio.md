# Concurrency (Concurrencia) — Estudio

## Tarjetas de repaso

P: ¿Qué es la concurrencia ante todo, según el capítulo?
R: Una estrategia de desacoplamiento que separa *qué* se hace de *cuándo* se hace.

P: ¿Por qué en aplicaciones de un solo hilo el estado suele deducirse del stack backtrace?
R: Porque el *qué* y el *cuándo* están tan acoplados que el estado de toda la aplicación se deduce de la pila de llamadas.

P: ¿Cuándo mejora realmente el rendimiento la concurrencia?
R: Solo cuando hay mucho tiempo de espera que compartir entre varios hilos o procesadores.

P: ¿Es cierto que el diseño no cambia al escribir programas concurrentes?
R: No; es un mito. Desacoplar el *qué* del *cuándo* afecta enormemente a la estructura del algoritmo.

P: En la clase `X` con `getNextId()` devolviendo `++lastIdUsed` y dos hilos (lastIdUsed=42), ¿qué tres resultados son posibles?
R: 43/44 con campo 44; 44/43 con campo 44; o el sorprendente 43/43 con campo 43 cuando los hilos se pisan.

P: ¿Cuántos caminos de ejecución hay para dos hilos en ese método con `int`, y cuántos si pasa a `long`?
R: 12.870 caminos con `int`; 2.704.156 caminos si `lastIdUsed` pasa a `long`.

P: ¿Qué dice el SRP aplicado a la concurrencia?
R: El código de concurrencia tiene su propio ciclo de vida y retos; debe mantenerse separado del resto del código.

P: ¿Qué recomienda el capítulo sobre el acceso a datos compartidos?
R: Llevar la encapsulación al corazón y limitar severamente el acceso a datos compartidos (restringir el número de secciones `synchronized`).

P: ¿Cuáles son los tres modelos de ejecución clásicos?
R: Producer-Consumer, Readers-Writers y Dining Philosophers.

P: ¿Qué clase thread-safe rinde mejor que `HashMap` y permite lecturas/escrituras concurrentes simultáneas?
R: `ConcurrentHashMap`, del paquete `java.util.concurrent`.

P: ¿Qué tres formas de corregir dependencias entre métodos sincronizados menciona el capítulo?
R: Client-based locking, server-based locking y adapted server.

P: ¿Por qué deben mantenerse pequeñas las secciones sincronizadas?
R: Los locks son caros; extender la sincronización más allá del mínimo aumenta la contención y degrada el rendimiento.

P: ¿Qué problema suele causar el apagado con elegancia (graceful shutdown)?
R: Deadlock: hilos que esperan una señal que nunca llega.

P: ¿Qué es "jiggling" en pruebas de código con hilos?
R: Instrumentar el código con `wait()`, `sleep()`, `yield()`, `priority()` para alterar el orden de ejecución y sacar a la luz errores; puede ser hand-coded o automated.

P: ¿Cómo deben tratarse los fallos espurios (one-offs) en código con hilos?
R: Como posibles problemas de hilos; no descartarlos como casos aislados, asumiendo que los one-offs no existen.

## Preguntas de autoevaluación

P: Da dos ejemplos del capítulo en que la concurrencia mejora rendimiento o tiempo de respuesta.
R: El agregador de un solo hilo cuyo proceso diario supera 24 horas y se ataca con un algoritmo multihilo; y el sistema que atiende un usuario a la vez y mejora el tiempo de respuesta atendiendo muchos usuarios concurrentemente. (Sección "Why Concurrency?")

P: ¿Por qué el desacoplamiento que ofrece un contenedor web no exime de entender la concurrencia?
R: Porque ese desacoplamiento es lejos de perfecto; conviene saber qué hace el contenedor y protegerse frente a actualizaciones concurrentes y deadlock. (Secciones "Why Concurrency?" y "Myths and Misconceptions")

P: ¿Qué estrategias de defensa propone el capítulo para que los hilos sean independientes?
R: Que cada hilo viva en su mundo con datos en variables locales sin compartir nada, y particionar los datos en subconjuntos independientes operables por hilos independientes. (Sección "Concurrency Defense Principles")

P: ¿Qué ventaja tiene usar copias de datos frente a compartirlos?
R: Evita el lock intrínseco; el ahorro suele compensar la creación y la recolección de basura extra, copiando objetos de solo lectura o fundiendo resultados en un solo hilo. (Sección "Concurrency Defense Principles")

P: ¿Cuál es el reto central del problema Readers-Writers?
R: Equilibrar throughput evitando starvation e información obsoleta, sin que los escritores bloqueen a los lectores demasiado tiempo. (Sección "Know Your Execution Models")

P: ¿Qué recomienda el capítulo respecto al orden de desarrollo entre código concurrente y no concurrente?
R: Hacer funcionar primero el código no concurrente, aislando POJOs ajenos a los hilos y probándolos fuera del entorno concurrente, para no perseguir bugs de hilos y no-hilos a la vez. (Sección "Testing Threaded Code")

P: ¿Por qué se recomienda ejecutar con más hilos que procesadores y en distintas plataformas?
R: Más hilos que procesadores fomenta el intercambio de tareas y expone secciones críticas faltantes o deadlocks; distintas plataformas tienen distintas políticas de hilos (OS X frente a Windows XP en VM). (Sección "Testing Threaded Code")

## Puntos a dominar

- Entender la concurrencia como desacoplamiento de *qué* y *cuándo*, y por qué el código concurrente limpio es difícil.
- Desmontar los tres mitos: rendimiento, diseño inmutable y la supuesta irrelevancia de entender concurrencia con contenedor.
- Explicar cómo una línea como `++lastIdUsed` genera miles de caminos de ejecución y resultados incorrectos.
- Aplicar los principios de defensa: SRP, limitar datos compartidos, copias de datos e hilos independientes.
- Conocer `java.util.concurrent`, `java.util.concurrent.atomic` y `java.util.concurrent.locks`, y definiciones como `ReentrantLock`, `Semaphore`, `CountDownLatch`, deadlock, livelock, starvation.
- Reconocer los tres modelos de ejecución: Producer-Consumer, Readers-Writers y Dining Philosophers.
- Evitar dependencias entre métodos sincronizados y, si es inevitable, aplicar client-based, server-based o adapted server locking.
- Mantener secciones sincronizadas mínimas y planear pronto el apagado con elegancia.
- Diseñar código enchufable y ajustable, probarlo con muchas configuraciones y plataformas, e instrumentarlo con jiggling.
