# Stability Patterns (Patrones de estabilidad) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre las fallas? / R: Las fallas son inevitables (“todo sistema acaba operando fuera de especificación”), así que hay que cultivar una mentalidad orientada a la recuperación: esperar la falla y aplicar patrones para limitar el daño de cada una.

P: ¿Por qué “cantidad de patrones aplicados” no es una buena métrica? / R: Porque los patrones se aplican con juicio, identificando las amenazas y eligiendo la defensa apropiada para cada una, no acumulándolos.

P: ¿Qué aportan los Timeouts y qué peticiones protegen frente a Fail Fast? / R: Aportan aislamiento de fallas: un problema en otro servicio no tiene por qué volverse tuyo. Timeouts protege las peticiones salientes y Fail Fast las entrantes: dos caras de la misma moneda.

P: ¿Por qué reintentar de inmediato tras una falla suele ser mala idea? / R: Porque casi siempre vuelve a fallar: dentro de un data center el problema del otro extremo suele durar un rato; es mejor encolar y reintentar más tarde (store-and-forward).

P: ¿Cuáles son los tres estados de un Circuit Breaker? / R: Closed (ejecuta normalmente y cuenta fallas), Open (al superar el umbral falla de inmediato sin ejecutar, con posible fallback) y Half-Open (deja pasar una llamada de prueba; si tiene éxito cierra, si falla reabre).

P: ¿Por qué importa la densidad de fallas y qué patrón se recomienda para medirla? / R: Porque cinco fallas en cinco horas no es lo mismo que cinco en treinta segundos; el autor recomienda el patrón Leaky Bucket.

P: ¿Qué son los Bulkheads y cuál es su forma más común? / R: Son particiones del sistema (como los mamparos de un barco) para que una falla en una parte no destruya todo; su forma más común es la redundancia física.

P: ¿Cuál es la regla fundamental de Steady State? / R: Para cada mecanismo que acumula un recurso debe existir otro que lo recicle, eliminando el *fiddling* (intervención manual en producción).

P: ¿Qué tres tipos de “lodo” se acumulan según Steady State? / R: Datos (purga, que debe hacer la lógica de la aplicación), archivos de log (rotar y centralizar) y caché en memoria (imponer límites de tamaño e invalidación).

P: ¿Qué distingue una falla de sistema de una falla de aplicación en Fail Fast? / R: La falla de sistema es de recursos no disponibles; la de aplicación son parámetros inválidos. Deben reportarse distinto para no hacer que un sistema aguas arriba abra un circuit breaker por datos de usuario erróneos.

P: ¿Qué cuatro requisitos exige el patrón Let It Crash? / R: Granularidad limitada, reemplazo rápido (a estado limpio), supervisión (árbol de supervisores) y reintegración del proveedor restaurado.

P: ¿En qué se diferencia un Test Harness de un mock object? / R: Un mock solo produce comportamiento conforme a la interfaz definida; el harness es malicioso y puede provocar fallas de red y de protocolo que los mocks no, corriendo como servidor separado.

P: ¿Por qué el middleware orientado a mensajes no puede producir una falla en cascada? / R: Porque desacopla en espacio y tiempo, a diferencia de las llamadas síncronas (RPC, HTTP, RMI…) que obligan al llamador a esperar y amplifican los shocks.

P: ¿Cuándo usar Shed Load y cuándo Create Back Pressure? / R: Shed Load rechaza trabajo nuevo y es la medida principal en los bordes expuestos a Internet; Back Pressure frena a los productores con colas finitas y es más eficiente dentro de los límites del sistema.

P: ¿Qué caracteriza a un Governor y cuál es su objetivo? / R: Es stateful, consciente del tiempo y asimétrico (acciones con dirección segura e insegura); aplica resistencia creciente en la dirección insegura para frenar lo suficiente y dar tiempo a que un humano intervenga.

## Preguntas de autoevaluación

P: ¿Por qué todo pool de recursos que bloquea hilos debe tener timeout? / R: Para que los hilos eventualmente se desbloqueen, haya o no recursos disponibles; igual aplica a mutexes y sincronización, usando siempre la variante con argumento de timeout. (sección Timeouts)

P: ¿Por qué un Circuit Breaker debe vivir en el ámbito de un solo proceso? / R: Porque compartirlo entre procesos añadiría otra comunicación fuera de proceso y un nuevo modo de falla; además conviene usar librerías open source para evitar los terrores del multithreading. (sección Circuit Breaker)

P: ¿Por qué las VMs redundantes son menos robustas como Bulkhead que la redundancia física? / R: Porque pueden terminar en el mismo host físico, perdiendo la contención del daño que busca el patrón. (sección Bulkheads)

P: ¿Por qué la purga de datos debe hacerla la lógica de la aplicación y no un DBA? / R: Para mantener la integridad referencial, ya que un DBA no siempre sabe cómo se comporta la app sin esos datos. (sección Steady State)

P: ¿Por qué Let It Crash no es adecuado para una app JavaEE en VMs? / R: Porque si el arranque toma minutos no se cumple el requisito de reemplazo rápido (volver a estado limpio en microsegundos o milisegundos); no debe aplicarse a monolitos ni a runtimes pesados. (sección Let It Crash)

P: ¿Cuál es la mejor aproximación al Handshaking usando HTTP? / R: La alianza entre balanceador y servidores mediante health checks: el servidor avisa que está ocupado y el balanceador deja de enviarle trabajo; Circuit Breaker es el recurso cuando el servicio llamado no puede hacer handshaking. (sección Handshaking)

P: Según la ley de Little, ¿qué ocurre con una cola no acotada y qué exige Back Pressure? / R: Las colas no acotadas consumen toda la memoria y hacen que el tiempo de respuesta tienda a infinito; por eso las colas deben ser finitas, y al llenarse se puede bloquear al productor como control de flujo. (sección Create Back Pressure)

P: ¿Cómo ilustra el ejemplo de la empresa de fotografía la relación entre Fail Fast y Steady State? / R: El nuevo renderizado verificaba y preasignaba recursos al llegar el trabajo, llevando los reprocesos por software a cero; pero el único recurso no preasignado (disco, por un cliente que purgaba a mano) se llenó en menos de un año, y justo ese punto donde se rompió Fail Fast fue donde el sistema falló tras malgastar esfuerzo. (sección El ejemplo que recorre el capítulo)

## Puntos a dominar

- Explicar por qué las fallas son inevitables y qué implica una mentalidad orientada a la recuperación, sin tratar el número de patrones como métrica de calidad.
- Distinguir qué peticiones protege cada patrón: Timeouts (salientes) y Fail Fast (entrantes), y por qué conviene reintentos diferidos sobre reintentos inmediatos.
- Describir los tres estados del Circuit Breaker, la importancia de la densidad de fallas (Leaky Bucket), su ámbito por proceso y la necesidad de exponer sus cambios de estado.
- Identificar niveles de Bulkhead (thread pools, process binding, granjas de servidores, zonas/regiones) y cuándo son especialmente valiosos (servicios compartidos y microservicios).
- Aplicar Steady State a los tres tipos de “lodo” (datos, logs, caché) garantizando un reciclado para cada acumulación y evitando el fiddling.
- Separar falla de sistema de falla de aplicación en Fail Fast, y reconocer los cuatro requisitos de Let It Crash y cuándo no aplicarlo.
- Diferenciar Test Harness de mock objects y las cuatro categorías de falla que debe provocar (transporte, protocolo de red, protocolo de aplicación, lógica de aplicación).
- Decidir middleware desacoplado temprano (decisión casi irreversible) y combinar Shed Load, Back Pressure y Governor según se esté en los bordes o dentro de los límites del sistema.
