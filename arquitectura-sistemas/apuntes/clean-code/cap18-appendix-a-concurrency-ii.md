# Clean Code: A Handbook of Agile Software Craftsmanship — Robert C. Martin (Prentice Hall, 2008)
## Capítulo 18 — Appendix A: Concurrency II (Apéndice A: Concurrencia II)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

Este apéndice, escrito por Brett L. Schuchert, amplía el capítulo de Concurrencia (PDF p. 177). Está organizado como una serie de temas independientes que pueden leerse en cualquier orden, con cierta duplicación deliberada para permitir esa lectura. Su tesis central es que la concurrencia es un territorio amplio y traicionero, y que la forma de mantener el código concurrente limpio es aplicar disciplinas concretas: aislar la gestión de hilos en pocos lugares bien controlados, entender el modelo de memoria, prevenir el deadlock y diseñar pruebas que expongan fallos de concurrencia.

Sales sabiendo cómo mejorar el throughput de un sistema I/O-bound con hilos, por qué operaciones aparentemente simples como `++` no son atómicas, cómo cuentan las posibles trayectorias de ejecución, la diferencia entre locking basado en cliente y en servidor, las cuatro condiciones del deadlock y cómo romper cada una, y por qué probar código multihilo es tan difícil.

## El ejemplo que recorre el capítulo

El hilo conductor es un sistema cliente/servidor simple. Un servidor escucha en un socket, acepta conexiones y procesa cada petición; un test (`shouldRunInUnder10Seconds`, con `timeout = 10000`) valida el throughput del sistema. A partir de ese ejemplo se introduce el threading y la necesidad de separar responsabilidades. Otros ejemplos (`IdGenerator`, `IntegerIterator`, lectura de páginas web) ilustran los demás temas.

## Ejemplo cliente/servidor

El servidor original procesa cada petición en un solo hilo. Si el test de rendimiento falla, hay que saber dónde se consume el tiempo:

- **I/O**: sockets, conexión a base de datos, swapping de memoria virtual.
- **Procesador**: cálculos numéricos, expresiones regulares, recolección de basura.

Si el problema es processor-bound, añadir hilos no acelera (los ciclos de CPU son finitos). Si es I/O-bound, la concurrencia aumenta la eficiencia: mientras una parte espera por I/O, otra usa ese tiempo para procesar.

Añadir threading al método `process` (envolviendo el manejo del cliente en un `Runnable` y lanzando un `Thread`) hace que el test pase en poco más de un segundo, pero introduce problemas. No hay límite de hilos (podría alcanzarse el límite de la JVM) y el método `process` acumula demasiadas responsabilidades:

- Gestión de la conexión del socket
- Procesamiento del cliente
- Política de threading
- Política de apagado del servidor

Esto viola el Single Responsibility Principle. La regla: la gestión de hilos debe concentrarse en pocos lugares bien controlados, y el código que gestiona hilos no debe hacer nada más que eso. Rastrear problemas de concurrencia ya es bastante difícil como para mezclarlo con otros asuntos. La solución refactorizada concentra todo lo relacionado con hilos en `clientScheduler` (interfaz `ClientScheduler` con `schedule(...)`). La política `ThreadPerRequestScheduler` es fácil de implementar y, al estar aislada, cambiar a otra (por ejemplo, el framework `Executor` de Java 5 con `ExecutorClientScheduler`) solo requiere escribir una clase nueva y enchufarla.

## Posibles trayectorias de ejecución

El método `incrementValue` (`return ++lastIdUsed;`) tiene una sola trayectoria y resultado garantizado con un solo hilo. Con dos hilos llamando una vez cada uno (partiendo de `lastIdUsed = 93`) hay tres resultados posibles, incluido el sorprendente en que ambos obtienen 94 y el valor final es 94: un incremento se pierde.

**Número de trayectorias.** La línea de Java se traduce en ocho instrucciones de byte-code que dos hilos pueden intercalar como un crupier baraja cartas. Para N instrucciones en secuencia (sin bucles ni condicionales) y T hilos, el número de trayectorias es `(N*T)! / (N!**T)`. Para 8 instrucciones y 2 hilos son 12.870; si `lastIdUsed` es `long`, cada lectura/escritura son dos operaciones y las ordenaciones suben a 2.704.156. Con `synchronized`, las trayectorias bajan a dos (y a `N!` en el caso general).

**Operación atómica**: cualquier operación ininterrumpible. Según el modelo de memoria de Java, la asignación a un valor de 32 bits es atómica; la asignación a un valor de 64 bits requiere dos asignaciones de 32 bits, y entre ambas otro hilo puede colarse y cambiar un valor. El operador de preincremento `++` **no es atómico**.

Tres definiciones clave para leer el byte-code:

- **Frame**: cada invocación de método requiere un frame con la dirección de retorno, los parámetros y las variables locales (forma la pila de llamadas y permite la recursión).
- **Variable local**: cualquier variable del ámbito del método; todos los métodos no estáticos tienen al menos `this`.
- **Operand stack** (pila de operandos): estructura LIFO donde se colocan los parámetros de las instrucciones.

En `resetId()` las tres instrucciones (`ALOAD 0`, `ICONST_0`, `PUTFIELD`) son atómicas porque la información del `PUTFIELD` no puede ser tocada por otro hilo. En `getNextId()` con `++`, si un hilo ejecuta hasta `GETFIELD` (deja 42 en la pila) y es interrumpido, un segundo hilo completa el método y obtiene 43; al reanudarse el primero suma 1 sobre el 42 que quedó y almacena 43 de nuevo, perdiendo un incremento. Hacer el método `synchronized` lo corrige.

Lecciones: no hace falta dominar el byte-code, pero sí entender el modelo de memoria para saber qué es seguro. El mito de que `++` es atómico es falso. Debes conocer dónde hay objetos/valores compartidos, qué código puede causar problemas de lectura/actualización concurrente y cómo protegerlo.

## Conoce tu biblioteca

**Executor framework** (Java 5, paquete `java.util.concurrent`): permite ejecución sofisticada con pools de hilos. Si creas hilos sin pool o con uno hecho a mano, considera usarlo: hace el código más limpio, corto y fácil de seguir. Agrupa y redimensiona hilos, los recrea si hace falta y soporta *futures*. Funciona con `Runnable` y con `Callable` (como `Runnable`, pero puede devolver un resultado). Un *future* es útil para ejecutar operaciones independientes y esperar su fin: `result.get()` bloquea hasta que el future completa.

**Soluciones no bloqueantes.** La VM de Java 5 aprovecha el diseño de procesadores modernos para actualizaciones no bloqueantes fiables. Clases como `AtomicBoolean`, `AtomicInteger` y `AtomicReference` sustituyen al `synchronized`. Usar `value.incrementAndGet()` casi siempre supera en rendimiento a la versión sincronizada. Esto es posible gracias a **Compare and Swap (CAS)**, análogo al bloqueo optimista en bases de datos (la versión `synchronized` equivale al bloqueo pesimista). El enfoque no bloqueante asume que rara vez varios hilos modifican el mismo valor: detecta eficientemente el conflicto y reintenta hasta que la actualización tiene éxito; esa detección suele costar menos que adquirir un lock, incluso en contención moderada o alta.

**Clases no thread-safe**: `SimpleDateFormat`, conexiones a base de datos, contenedores de `java.util`, servlets. Algunos métodos de colecciones son thread-safe por separado, pero cualquier operación que llame a más de un método no lo es (p. ej. `containsKey` seguido de `put`). Opciones: client-based locking (bloquear la `HashTable`), server-based locking con un ADAPTER (`WrappedHashtable` con `putIfAbsent`), o usar colecciones thread-safe como `ConcurrentHashMap` con `putIfAbsent()`.

## Las dependencias entre métodos pueden romper el código concurrente

En `IntegerIterator`, aunque `hasNext()` y `next()` sean `synchronized`, el cliente usa ambos métodos. Un hilo puede comprobar `hasNext()` (true), ser interrumpido, y otro hilo consumir el último elemento; al reanudarse, el primero llama a `next()` y sobrepasa el final lanzando una excepción. El fallo solo aparece en la última iteración, por lo que es un bug sutil que surge en producción mucho después. Hay tres opciones:

- **Tolerar el fallo** (capturar la excepción): algo descuidado, como "limpiar fugas de memoria reiniciando a medianoche".
- **Client-based locking**: cada cliente envuelve el uso en `synchronized(iterator)`. Viola DRY y es arriesgado porque todo programador debe recordar bloquear y desbloquear. El relato de Local 705 (1971) ilustra lo difícil de depurar un único uso sin proteger de un recurso compartido: "Client-based locking really blows".
- **Server-based locking**: cambiar la API (`getNextOrNull()`) para que la clase sea consciente de los hilos. Es preferible porque reduce código repetido, permite mejor rendimiento (se puede sustituir por una versión no thread-safe en despliegue monohilo), reduce la posibilidad de error, impone una única política en un solo lugar y reduce el alcance de las variables compartidas. Si no posees el código del servidor, usa un ADAPTER (`ThreadSafeIntegerIterator`) o, mejor, las colecciones thread-safe.

## Aumentar el throughput

Leer páginas de una lista de URLs, parsearlas y resumir. `PageReader.getPageFor(url)` devuelve una página; `PageIterator` comparte la iteración entre hilos con un bloque `synchronized` muy pequeño, solo la sección crítica. Siempre es mejor sincronizar lo menos posible.

Cálculo monohilo: con I/O de 1 s por página y procesamiento de 0,5 s, el tiempo total es 1,5 s × N (13 páginas ≈ 19,5 s). Con tres hilos, el parsing (processor-bound) solapa con la lectura (I/O-bound); en un mundo ideal el procesador queda plenamente utilizado y se procesan dos páginas por segundo, el triple del throughput monohilo.

## Deadlock

Ejemplo: una app web con dos pools finitos (conexiones de base de datos y conexiones MQ al repositorio maestro) y dos operaciones, *create* y *update*, que adquieren los recursos en orden distinto. Si diez usuarios de *create* toman todas las conexiones de BD y diez de *update* toman todas las del repositorio, cada grupo espera el recurso del otro: deadlock, el sistema no se recupera.

Hay cuatro condiciones necesarias para el deadlock; romper cualquiera lo impide:

- **Exclusión mutua** (mutual exclusion): recursos limitados que no pueden usar varios hilos a la vez (conexión de BD, fichero abierto para escritura, bloqueo de registro, semáforo). Romperla: usar recursos de uso simultáneo (`AtomicInteger`), aumentar los recursos hasta igualar a los hilos, o comprobar que todos los recursos están libres antes de tomar ninguno.
- **Lock & wait**: un hilo retiene un recurso hasta adquirir todos los demás y terminar. Romperla: no esperar; comprobar cada recurso antes de tomarlo y liberar todo y reiniciar si uno está ocupado. Riesgos: *starvation* (baja utilización de CPU) y *livelock* (alta e inútil).
- **No preemption** (sin expropiación): un hilo no puede quitar recursos a otro. Romperla: un mecanismo de petición; cuando un hilo pide un recurso ocupado, el dueño (si también espera) libera todo y reinicia. Reduce reinicios, pero gestionar las peticiones es complicado.
- **Circular wait** (espera circular, o *deadly embrace*): T1 tiene R1 y pide R2; T2 tiene R2 y pide R1. Romperla es lo más común: imponer un orden global de adquisición de recursos acordado por todos. Limitaciones: el orden de adquisición puede no coincidir con el de uso (recursos bloqueados más tiempo del necesario) y a veces no se puede ordenar (si el ID del segundo recurso surge de operar el primero).

Todas las estrategias tienen costes (starvation o uso elevado de CPU): TANSTAAFL. Aislar la parte de hilos ayuda a afinar y experimentar.

## Probar código multihilo

Probar `ClassWithThreadingProblem` (con `takeNextId()` usando `nextId++`) es difícil: el test recuerda el valor, lanza dos hilos que llaman una vez cada uno y verifica que el valor subió en dos. El problema ocurre tan raramente que hay que iterar más de un millón de veces, y aun así en diez ejecuciones con un millón de iteraciones el fallo apareció una sola vez. Habría que llegar a más de cien millones para fallos fiables, y habría que reajustar en cada máquina, SO o versión de JVM.

Ideas para exponer fallos:

- **Monte Carlo testing**: tests ajustables, ejecutados repetidamente en un servidor cambiando aleatoriamente los valores de ajuste; registrar cuidadosamente las condiciones de fallo y empezar pronto con integración continua.
- Ejecutar los tests en cada plataforma de despliegue objetivo, repetida y continuamente.
- Ejecutarlos en máquinas con cargas variables, lo más cercanas a producción posible.

Aun así, los problemas con sección transversal diminuta (uno entre mil millones) son el terror de los sistemas complejos. **Tool support**: IBM creó **ConTest**, que instrumenta clases para que el código no thread-safe falle con más probabilidad. Tras instrumentar, el ratio de fallo pasó de ~1 en diez millones de iteraciones a ~1 en treinta (valores observados: 13, 23, 0, 54, 16, 14, 6, 69, 107, 49, 2).

## Conclusión

El capítulo es un recorrido muy breve por el territorio de la programación concurrente, con énfasis en disciplinas para mantenerla limpia. Se recomienda ampliar con *Concurrent Programming in Java: Design Principles and Patterns* de Doug Lea. Se trataron la actualización concurrente y las disciplinas de sincronización/locking limpios, cómo los hilos mejoran el throughput de sistemas I/O-bound, el deadlock y cómo prevenirlo, y estrategias para exponer problemas instrumentando el código. El tutorial final incluye el código completo del cliente/servidor sin hilos y con hilos.

## Ideas clave

- Concentra toda la gestión de hilos en pocos lugares bien controlados y que no hagan nada más: es aplicar el Single Responsibility Principle a la concurrencia.
- La concurrencia solo acelera sistemas I/O-bound; en problemas processor-bound no ayuda (los ciclos de CPU son finitos).
- `++` no es atómico; la asignación de 32 bits sí lo es, pero la de 64 bits requiere dos pasos. Debes conocer el modelo de memoria para saber qué es seguro.
- El número de trayectorias de ejecución crece enormemente: `(N*T)!/(N!**T)`; `synchronized` lo reduce a `N!`.
- Las soluciones no bloqueantes basadas en CAS (`AtomicInteger`, etc.) suelen superar al `synchronized`, que siempre adquiere un lock aunque no haya contención.
- Aunque los métodos individuales sean thread-safe, combinar varios (p. ej. `hasNext()` + `next()`) puede romper el código; prefiere server-based locking sobre client-based locking.
- Sincroniza lo menos posible, solo la sección crítica.
- El deadlock requiere cuatro condiciones (exclusión mutua, lock & wait, no preemption, circular wait); romper cualquiera lo evita, y romper la espera circular con un orden global de recursos es lo más habitual.
- Probar código concurrente es muy difícil: usa Monte Carlo testing, múltiples plataformas y cargas, y herramientas de instrumentación como ConTest.
