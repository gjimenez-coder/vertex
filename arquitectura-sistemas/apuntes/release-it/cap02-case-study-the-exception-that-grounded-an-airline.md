# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 2 — Case Study: The Exception That Grounded an Airline (Caso de estudio: la excepción que dejó en tierra a una aerolínea)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

El capítulo narra un incidente real (con nombres, lugares y fechas cambiados) en el que una aerolínea quedó paralizada durante poco más de tres horas, dejando a miles de pasajeros varados y costando cientos de miles de dólares. La tesis central es que los grandes desastres suelen empezar con algo mínimo: aquí, un único `SQLException` no capturado en una sola línea de código provocó un efecto dominó que tumbó sistemas enteros.

El relato sigue la investigación de un postmortem, desde la ventana de cambio aparentemente rutinaria hasta el descubrimiento del "smoking gun" en el código decompilado. El punto clave es que un sistema diseñado con alta disponibilidad impecable a nivel de hardware fue derribado por un fallo de software que ninguna redundancia física podía evitar.

Sales sabiendo que los bugs no se pueden eliminar, solo sobrevivir: en una malla de sistemas interconectados, lo verdaderamente peligroso es que un fallo en un sistema se propague a todos los demás. El capítulo prepara el terreno para los patrones de diseño que evitan esa propagación.

## El ejemplo que recorre el capítulo

El hilo conductor es el sistema **Core Facilities (CF)**, un servicio de búsqueda de vuelos en su primera generación dentro de una migración hacia una arquitectura orientada a servicios (SOA). CF recibía fecha, hora, ciudad, código de aeropuerto o número de vuelo y devolvía detalles de vuelos. Ya lo consumían los kioscos de autoservicio de check-in, los menús telefónicos (IVR) y las aplicaciones de "channel partners". Las aplicaciones de agentes de puerta y call center aún no habían migrado a CF, lo cual —como se verá— resultó ser una suerte.

## La arquitectura de alta disponibilidad

CF se construyó para alta disponibilidad, consciente de su criticidad:

- Clúster de servidores de aplicaciones J2EE con base de datos Oracle 9i redundante.
- Datos en un gran arreglo RAID externo, con backups off-site dos veces al día en cinta y réplicas en disco (garantizadas con un retraso máximo de cinco minutos) en un segundo chasis.
- Hardware real, sin virtualización.
- El servidor Oracle corría en un nodo del clúster a la vez, con **Veritas Cluster Server** controlando el servidor de base de datos, asignando la IP virtual y montando/desmontando los filesystems del RAID.
- Un par de balanceadores de carga de hardware redundantes dirigía el tráfico entrante a los servidores de aplicaciones. Los clientes se conectaban solo a la IP virtual de front-end.

No había puntos únicos de fallo: cada pieza de hardware era redundante (CPUs, discos, tarjetas de red, fuentes, switches, hasta los ventiladores), los servidores estaban en racks distintos y una segunda ubicación a 30 millas podía asumir el servicio.

## La ventana de cambio

Un equipo local de ingenieros dedicado a la cuenta operaba la infraestructura desde hacía más de tres años. La noche del problema ejecutaron un **failover manual de base de datos** de CF database 1 a CF database 2 usando Veritas, para hacer mantenimiento de rutina. Era un procedimiento que habían hecho decenas de veces. En un minuto Veritas podía apagar Oracle en database 1, desmontar los filesystems del RAID, remontarlos en database 2, arrancar Oracle allí y reasignar la IP virtual; los servidores de aplicaciones no notaban el cambio.

El cambio se programó un jueves hacia las 11 p.m. hora del Pacífico. Migraron a database 2, actualizaron database 1, migraron de vuelta y actualizaron database 2. El monitoreo mostró disponibilidad continua. A las 12:30 a.m. marcaron el cambio como "Completed, Success" y el ingeniero se fue a dormir tras una jornada de 22 horas. (El autor señala que el "planned downtime" era normal entonces, pero ya no es la forma de operar.)

## La caída (The Outage)

A las 2:30 a.m. del Pacífico (5:30 a.m. del Este, hora pico de check-in en la costa Este) todos los kioscos de check-in se pusieron en rojo en la consola simultáneamente en todo el país. Minutos después cayeron también los servidores IVR. Se abrió un caso Severidad 1.

Lecciones de operación de este tramo:

- **Restaurar el servicio es la primera prioridad**, por encima de la investigación. "When the fur flies, improvisation is not your friend" (PDF p. 25).
- El equipo tenía scripts preparados para capturar thread dumps de las aplicaciones Java y snapshots de las bases de datos: recolección automatizada, ni improvisada ni alargadora de la caída.
- Para restaurar servicio hay que saber qué reiniciar. Se puede "reboot the world" capa por capa (casi siempre funciona pero es lento) o buscar al culpable concreto, como un médico diagnosticando por síntomas en lugar de tratar todas las enfermedades.
- Kioscos e IVR, ambos colgados casi a la vez, apuntaban a una dependencia común: **CF**, único sistema compartido. El failover tres horas antes lo hacía aún más sospechoso. El monitoreo no reportaba problemas en CF porque solo golpeaba una página de estado, que no reflejaba la salud real de los servidores.

Al reiniciar el primer servidor de CF, el IVR empezó a recuperarse; reiniciados todos, el IVR quedó verde pero los kioscos seguían rojos hasta reiniciar sus propios servidores de aplicación. Tiempo total: poco más de tres horas.

## Consecuencias

El impacto duró mucho más que las tres horas. Las aerolíneas no tienen suficientes agentes de puerta para hacer check-in con los sistemas antiguos; hubo que llamar a agentes fuera de turno, incurriendo en horas extra sindicales. El backlog no se resolvió hasta casi las 3 p.m. Los aviones no podían salir de sus puertas, incoming flights se reasignaron a otras puertas, y las demoras salieron en *Good Morning America* y el Weather Channel. La FAA mide puntualidad y quejas en el informe anual de la aerolínea, y la compensación del CEO depende en parte de ese informe.

## Postmortem y caza de pistas

El autor fue llamado a hacer el postmortem. La sospecha natural recayó en el failover: en operaciones, *"post hoc, ergo propter hoc"* — "lo tocaste de último" — es un buen punto de partida. Un postmortem es como un misterio de asesinato con pistas fiables (logs) y no fiables (testimonios que mezclan observación y especulación), y más difícil porque el "cadáver" desaparece: los servidores ya están arriba. También comparó las configuraciones actuales con el backup nocturno para detectar un posible encubrimiento.

Revisó la configuración del clúster y el RAID buscando problemas típicos (heartbeats insuficientes, heartbeats por switches con tráfico de producción, IPs físicas en vez de virtual, malas dependencias entre paquetes). No encontró nada mal: trabajo de manual. El foco pasó a los servidores de aplicaciones y sus **thread dumps** de Java.

### Thread dumps

Un thread dump es un libro abierto: revela librerías de terceros, pools de hilos, cuántos hilos hay en cada uno, procesamiento en background y protocolos usados. Se obtienen enviando `SIGQUIT` (signal 3) en UNIX o `Ctrl+Break` en Windows; o con `jcmd <pid> Thread.print`. Advertencia: los dumps de consola salen por standard out, que muchos scripts de arranque no capturan.

En los kioscos, los 40 hilos de atención estaban bloqueados en `SocketInputStream.socketRead0()`, intentando leer una respuesta que nunca llegaría, todos en `FlightSearch.lookupByCity()`. Aparecían referencias a RMI y EJB: CF, descrito como "web service", era en realidad un stateless session bean. **RMI es peligroso porque sus llamadas no pueden hacer timeout**, dejando al llamador vulnerable a problemas del servidor remoto.

## El smoking gun

En CF, los pools de hilos de EJB y HTTP estaban separados (por eso el monitoreo por HTTP seguía respondiendo). Todos los hilos EJB estaban bloqueados exactamente en la misma línea: intentando sacar una conexión del resource pool. Sin acceso al código fuente (solo binarios en producción), el autor **decompiló** los binarios y encontró el fallo en el EJB `FlightSearch.lookupByCity()`.

```java
} finally {
    if (stmt != null) {
        stmt.close();
    }
    if (conn != null) {
        conn.close();
    }
}
```

El bloque `try...finally` parece bien construido —aparece incluso en libros de Java—, pero `java.sql.Statement.close()` puede lanzar `SQLException`. El driver de Oracle lo hace al encontrar un `IOException` al cerrar la conexión, por ejemplo tras un failover de base de datos.

Tras el failover, la IP se movió de host pero el estado de las conexiones TCP existentes no se transfiere; cualquier escritura por el socket termina lanzando `IOException`. El driver aún crea statements (solo chequea su estado interno), pero al cerrarlos lanza `SQLException`. Si el cierre del statement falla, la conexión **no se cierra**: fuga de recursos. Tras 40 llamadas, el pool se agota y toda llamada futura se bloquea en `connectionPool.getConnection()` — exactamente lo visto en los dumps.

Resumen del autor: toda la aerolínea quedó en tierra por el error de un programador, un único `SQLException` no capturado. La lección: la especificación JDBC permite que `Statement.close()` lance `SQLException`, así que tu código debe manejarlo.

## ¿Una onza de prevención?

- ¿Lo habría atrapado una revisión de código? Solo si un revisor conocía las entrañas del driver JDBC de Oracle o dedicaba horas por método.
- ¿Más pruebas? Quizá. El perfil de prueba normal no ejercitaba lo suficiente ese método; una vez identificado, fue simple reproducirlo en el entorno de stress test.
- Es fantasía esperar erradicar todos los bugs: **los bugs no se pueden eliminar, se deben sobrevivir**.
- El peor problema fue la **propagación**: un bug en un sistema afectó a todos los demás. La pregunta correcta no es cómo evitar el bug, sino cómo evitar que el bug de un sistema afecte a todo lo demás. El libro pasará a estudiar patrones de diseño que previenen esa cadena de fallos.

## Ideas clave

- Grandes incidentes nacen de errores minúsculos: aquí, un `SQLException` no capturado dejó en tierra a toda una aerolínea.
- La redundancia de hardware impecable no protege contra fallos de software; CF no tenía single points of failure físicos y aun así cayó.
- `java.sql.Statement.close()` puede lanzar `SQLException`; si no se maneja en el `finally`, la conexión no se cierra y se fuga del pool hasta agotarlo.
- Tras un failover de base de datos, las conexiones TCP del pool quedan muertas aunque el driver siga creando statements inutilizables.
- RMI es peligroso porque sus llamadas no pueden hacer timeout: el llamador queda a merced del servidor remoto.
- Restaurar el servicio tiene prioridad sobre investigar; tener scripts de recolección automatizada (thread dumps, snapshots) da lo mejor de ambos mundos.
- El monitoreo que solo golpea una página de estado da falsa tranquilidad: no refleja la salud real del sistema.
- Los bugs no se eliminan, se sobreviven; lo crítico es impedir que el fallo de un sistema se propague por la malla de sistemas interconectados.
