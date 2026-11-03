# Appendix A: Concurrency II (Apéndice A: Concurrencia II) — Estudio

## Tarjetas de repaso

P: ¿Cómo se mantiene limpio el código concurrente según el apéndice?
R: Aislando la gestión de hilos en pocos lugares bien controlados, entendiendo el modelo de memoria, previniendo el deadlock y diseñando pruebas que expongan fallos de concurrencia.

P: ¿Qué tipos de sistema mejoran con hilos y cuáles no?
R: La concurrencia aumenta la eficiencia en sistemas I/O-bound (mientras una parte espera por I/O, otra procesa); en problemas processor-bound no ayuda porque los ciclos de CPU son finitos.

P: ¿Qué problema de diseño introduce añadir threading directamente al método `process` del servidor?
R: El método acumula demasiadas responsabilidades (conexión del socket, procesamiento, política de threading y política de apagado), violando el Single Responsibility Principle; además no limita el número de hilos.

P: ¿Cuál es la regla sobre el código que gestiona hilos?
R: La gestión de hilos debe concentrarse en pocos lugares bien controlados y ese código no debe hacer nada más que eso, para no mezclar problemas de concurrencia con otros asuntos.

P: ¿Es atómico el operador de preincremento `++`?
R: No. Según el modelo de memoria de Java la asignación de 32 bits es atómica, pero la de 64 bits requiere dos asignaciones y `++` no es atómico; es un mito que lo sea.

P: ¿Cuál es la fórmula del número de trayectorias de ejecución y cómo la reduce `synchronized`?
R: Para N instrucciones en secuencia y T hilos es `(N*T)! / (N!**T)`; para 8 instrucciones y 2 hilos son 12.870, y con `synchronized` baja a dos (y a `N!` en el caso general).

P: ¿Qué es una operación atómica y qué tres conceptos ayudan a leer el byte-code?
R: Una operación ininterrumpible. Los conceptos son: frame (dirección de retorno, parámetros y variables locales), variable local (toda variable del ámbito del método, con al menos `this`) y operand stack (pila LIFO de parámetros de instrucciones).

P: ¿Qué es el Executor framework y qué aporta?
R: Framework de Java 5 (`java.util.concurrent`) que ejecuta con pools de hilos; agrupa y redimensiona hilos, los recrea, soporta futures y funciona con `Runnable` y `Callable` (este último puede devolver un resultado).

P: ¿Qué es Compare and Swap (CAS) y con qué se analoga?
R: Mecanismo de actualización no bloqueante usado por clases como `AtomicInteger`; es análogo al bloqueo optimista en bases de datos (el `synchronized` equivale al bloqueo pesimista): detecta el conflicto y reintenta hasta tener éxito.

P: ¿Por qué combinar `hasNext()` y `next()` puede romper el código aunque ambos sean `synchronized`?
R: Un hilo puede comprobar `hasNext()` como true, ser interrumpido, y otro consumir el último elemento; al reanudarse, `next()` sobrepasa el final y lanza excepción. El fallo solo aparece en la última iteración.

P: ¿Por qué se prefiere server-based locking sobre client-based locking?
R: Reduce código repetido, permite mejor rendimiento, reduce la posibilidad de error, impone una única política en un solo lugar y reduce el alcance de las variables compartidas; el client-based viola DRY y obliga a cada programador a recordar bloquear.

P: ¿Cuáles son las cuatro condiciones necesarias para el deadlock?
R: Exclusión mutua, lock & wait, no preemption (sin expropiación) y circular wait (espera circular); romper cualquiera de ellas impide el deadlock.

P: ¿Cuál es la forma más común de romper la espera circular?
R: Imponer un orden global de adquisición de recursos acordado por todos; sus limitaciones son que el orden puede no coincidir con el de uso y que a veces no se puede ordenar.

P: ¿Por qué es tan difícil probar código multihilo?
R: El fallo ocurre tan raramente que hay que iterar más de un millón de veces y aun así puede no aparecer; habría que llegar a cientos de millones y reajustar en cada máquina, SO o versión de JVM.

P: ¿Qué es ConTest y qué efecto tiene?
R: Herramienta de IBM que instrumenta clases para que el código no thread-safe falle con más probabilidad; subió el ratio de fallo de ~1 en diez millones de iteraciones a ~1 en treinta.

## Preguntas de autoevaluación

P: Si un test de rendimiento del servidor falla, ¿cómo decides si añadir hilos ayudará?
R: Identificando dónde se consume el tiempo: si es I/O-bound (sockets, base de datos, swapping) la concurrencia ayuda; si es processor-bound (cálculos, regex, GC) no acelera. (Sección "Ejemplo cliente/servidor")

P: ¿Cómo se refactoriza el servidor para aislar la política de threading?
R: Concentrando todo lo relacionado con hilos en `clientScheduler` (interfaz `ClientScheduler` con `schedule(...)`); cambiar de `ThreadPerRequestScheduler` a `ExecutorClientScheduler` solo requiere una clase nueva y enchufarla. (Sección "Ejemplo cliente/servidor")

P: Partiendo de `lastIdUsed = 93`, ¿por qué dos hilos pueden producir un valor final de 94?
R: Porque `++` no es atómico: un hilo lee 93 (GETFIELD), es interrumpido, otro completa y obtiene 94, y al reanudarse el primero suma sobre el valor leído y vuelve a almacenar 94, perdiendo un incremento. (Sección "Posibles trayectorias de ejecución")

P: ¿Qué ventaja de rendimiento tienen las soluciones no bloqueantes frente al `synchronized`?
R: Asumen que rara vez varios hilos modifican el mismo valor, detectan el conflicto y reintentan; esa detección suele costar menos que adquirir un lock, incluso en contención moderada o alta, mientras que `synchronized` siempre adquiere el lock. (Sección "Conoce tu biblioteca")

P: ¿Qué riesgo introduce combinar métodos thread-safe de una colección y cómo se resuelve?
R: Cualquier operación que llame a más de un método (p. ej. `containsKey` seguido de `put`) no es thread-safe; se resuelve con client-based locking, server-based locking con un ADAPTER o colecciones como `ConcurrentHashMap` con `putIfAbsent()`. (Sección "Conoce tu biblioteca")

P: ¿Cuánto throughput se gana al leer y parsear páginas con tres hilos frente a monohilo?
R: En monohilo con I/O de 1 s y procesamiento de 0,5 s por página el tiempo es 1,5 s × N; con tres hilos el parsing solapa con la lectura y, en el caso ideal, se procesan dos páginas por segundo, el triple del throughput monohilo. (Sección "Aumentar el throughput")

P: En el ejemplo de la app web, ¿cómo se produce el deadlock entre *create* y *update*?
R: Ambas operaciones adquieren en orden distinto dos pools finitos (conexiones de BD y conexiones MQ); si unos usuarios toman todas las conexiones de BD y otros todas las del repositorio, cada grupo espera el recurso del otro y el sistema no se recupera. (Sección "Deadlock")

P: ¿Qué técnicas propone el apéndice para exponer fallos de concurrencia en las pruebas?
R: Monte Carlo testing (tests ajustables ejecutados repetidamente con valores aleatorios, registrando fallos y usando integración continua), ejecutar en cada plataforma de despliegue, y correr en máquinas con cargas variables cercanas a producción; además, instrumentación con ConTest. (Sección "Probar código multihilo")

## Puntos a dominar

- Explicar por qué la concurrencia solo mejora sistemas I/O-bound y no los processor-bound.
- Justificar la concentración de la gestión de hilos en pocos lugares como aplicación del Single Responsibility Principle.
- Razonar por qué `++` no es atómico y distinguir asignaciones de 32 y 64 bits en el modelo de memoria de Java.
- Aplicar la fórmula `(N*T)!/(N!**T)` para estimar trayectorias y comprender cómo `synchronized` las reduce a `N!`.
- Comparar soluciones no bloqueantes (CAS, `AtomicInteger`) con `synchronized` en términos de bloqueo optimista vs. pesimista.
- Distinguir client-based locking de server-based locking y argumentar la preferencia por el segundo.
- Enumerar las cuatro condiciones del deadlock y describir cómo romper cada una, destacando el orden global de recursos para la espera circular.
- Sincronizar solo la sección crítica, lo menos posible.
- Describir las estrategias para probar código multihilo (Monte Carlo, múltiples plataformas y cargas, ConTest) y por qué los fallos de sección transversal diminuta son tan peligrosos.
