# Replication (Replicación) — Estudio

## Tarjetas de repaso

P: ¿Para qué sirve la replicación según el capítulo?
R: Acercar los datos geográficamente (menor latencia), mantener el sistema disponible aunque fallen partes y escalar el throughput de lectura; toda la dificultad está en gestionar los cambios, no las copias estáticas.

P: ¿Cómo funciona la replicación basada en líder (leader-based)?
R: Una réplica es el líder y acepta todas las escrituras; las demás son seguidores que aplican cada cambio en el mismo orden mediante un log de replicación. Las lecturas pueden ir al líder o a cualquier seguidor.

P: ¿Qué diferencia hay entre replicación síncrona y asíncrona?
R: La síncrona espera la confirmación del seguidor antes de reportar éxito (copia al día pero bloquea si el seguidor no responde); la asíncrona no espera (rápida, pero puede perder escrituras confirmadas si el líder falla).

P: ¿Qué es una configuración semi-síncrona?
R: Solo un seguidor es síncrono y el resto asíncronos; si el síncrono falla, se promueve un asíncrono. Garantiza una copia actualizada en al menos dos nodos sin bloquear ante cualquier fallo.

P: ¿Qué pasos sigue el failover automático al caer el líder?
R: Detectar el fallo (normalmente por timeout), elegir nuevo líder (preferible el de datos más actualizados, un problema de consenso) y reconfigurar el sistema para que clientes y seguidores usen el nuevo líder.

P: ¿Qué es el split brain y cómo se mitiga?
R: Es cuando dos nodos se creen líder a la vez y ambos aceptan escrituras sin resolución de conflictos. Se mitiga apagando un nodo al detectar dos líderes (fencing/STONITH), aunque mal diseñado puede apagar los dos.

P: ¿Cuáles son los cuatro métodos de implementación del log de replicación?
R: Statement-based (reenvía sentencias, falla con no deterministas), WAL shipping (log de bajo nivel, acoplado al motor), logical/row-based (formato desacoplado a nivel de fila) y trigger-based (en la capa de aplicación, flexible pero con más overhead).

P: ¿Qué es la consistencia eventual (eventual consistency)?
R: La inconsistencia temporal por el retraso de replicación: si se dejan de escribir datos, los seguidores acaban poniéndose al día. "Eventual" es vago; el lag suele ser de fracciones de segundo pero puede llegar a minutos.

P: ¿Qué garantiza read-after-write y cómo se logra?
R: Que cada usuario vea siempre sus propias actualizaciones (nada promete sobre las de otros). Se logra leyendo del líder lo que el usuario pudo modificar, leyendo del líder un tiempo tras su última escritura o recordando el timestamp de su última escritura.

P: ¿Qué evitan monotonic reads y consistent prefix reads?
R: Monotonic reads evita que el usuario vea el tiempo ir hacia atrás (leyendo siempre de la misma réplica). Consistent prefix reads evita violaciones de causalidad asegurando que las escrituras se lean en el orden en que ocurrieron.

P: ¿Cuál es el mayor problema de la replicación multi-leader?
R: Los conflictos de escritura: dos usuarios cambian el mismo registro a la vez y el conflicto solo se detecta asíncronamente, cuando ya es tarde para pedir ayuda al usuario.

P: ¿Qué estrategias existen para resolver conflictos en multi-leader?
R: Evitar conflictos (enrutar todas las escrituras de un registro al mismo líder), converger a un estado consistente (LWW, precedencia por ID, fusión, registro explícito) y lógica personalizada ejecutada on write u on read.

P: ¿Qué topologías multi-líder existen y qué riesgos tienen?
R: All-to-all (tolerante a fallos pero con mensajes que pueden llegar en orden incorrecto), circular y en estrella (una escritura pasa por varios nodos y el fallo de uno interrumpe la replicación). Se etiquetan las escrituras para evitar bucles.

P: ¿Qué condición de quórum garantiza leer un valor actualizado en leaderless?
R: `w + r > n`: los conjuntos de nodos escritos (w) y leídos (r) se solapan. Opción común: n impar y w = r = (n+1)/2; con n=3, w=2, r=2 se tolera un nodo caído.

P: ¿Qué es la relación happens-before y qué son los version vectors?
R: A ocurre antes que B si B conoce o depende de A; son concurrentes si ninguna conoce a la otra (sin importar el tiempo físico). El version vector es el conjunto de números de versión por réplica y clave que distingue sobrescrituras de escrituras concurrentes.

## Preguntas de autoevaluación

P: ¿Por qué es impráctico hacer que todos los seguidores sean síncronos y qué solución adopta la práctica?
R: Porque si un seguidor síncrono no responde, el líder debe bloquear todas las escrituras hasta que vuelva. La práctica usa una configuración semi-síncrona con un solo seguidor síncrono. (Sección "Replicación síncrona frente a asíncrona")

P: ¿Qué riesgo concreto ilustra el incidente de GitHub con MySQL y Redis?
R: Un seguidor MySQL desactualizado fue promovido a líder y reutilizó claves primarias ya usadas en un store Redis, exponiendo datos privados a usuarios equivocados; muestra el peligro del failover asíncrono con sistemas externos coordinados. (Sección "Configurar nuevos seguidores y gestionar fallos de nodos")

P: ¿Por qué el WAL shipping dificulta los upgrades sin downtime?
R: Porque envía el log de bajo nivel acoplado al motor de almacenamiento; si cambia el formato de almacenamiento, no suele poderse ejecutar versiones distintas en líder y seguidores. (Sección "Implementación de los logs de replicación")

P: ¿Por qué el read-scaling con seguidores solo funciona con replicación asíncrona y qué efecto tiene?
R: Con muchos seguidores, hacerlos síncronos haría que un solo nodo caído bloqueara el sistema; con asíncrona un seguidor retrasado puede devolver datos obsoletos, generando consistencia eventual. (Sección "Problemas con el retraso de replicación")

P: ¿Por qué hacer la detección de conflictos síncrona en multi-leader anula su ventaja?
R: Porque esperar confirmación de los demás líderes antes de confirmar la escritura equivaldría a usar un solo líder, perdiendo la operación local independiente que motiva el multi-leader. (Sección "Gestión de conflictos de escritura")

P: ¿Cuándo es seguro usar last write wins (LWW) sin perder datos?
R: Solo cuando cada clave se escribe una vez y es inmutable (por ejemplo, una clave UUID); en otros casos LWW logra convergencia pero descarta escrituras concurrentes. (Secciones "Gestión de conflictos" y "Quórums, read repair y escrituras concurrentes")

P: ¿Qué aportan los mecanismos read repair y anti-entropy en leaderless?
R: Read repair reescribe el valor más nuevo cuando el cliente detecta valores obsoletos al leer; anti-entropy es un proceso en segundo plano que copia datos faltantes entre réplicas sin orden fijo. Ambos ayudan a que una réplica caída se ponga al día. (Sección "Quórums, read repair y escrituras concurrentes")

P: ¿Qué hace un sloppy quorum con hinted handoff y qué no garantiza?
R: Acepta respuestas w/r en nodos que no son los "de casa" cuando una interrupción de red impide el quórum, y al arreglarse el hinted handoff reenvía las escrituras a los nodos correctos. Aumenta la disponibilidad de escritura pero no garantiza leer el último valor. (Sección "Quórums, read repair y escrituras concurrentes")

## Puntos a dominar

- Explicar los tres motivos de replicar (latencia, disponibilidad, escalabilidad de lecturas) y por qué la dificultad está en los cambios.
- Distinguir single-leader, multi-leader y leaderless con sus ventajas y desventajas.
- Razonar el compromiso entre replicación síncrona y asíncrona, incluida la configuración semi-síncrona.
- Describir el proceso de añadir un seguidor (snapshot + posición del log + catch-up) y la recuperación ante fallo de seguidor y de líder.
- Enumerar los riesgos del failover: pérdida de escrituras, split brain y elección del timeout.
- Comparar los cuatro métodos de log de replicación y saber cuándo falla cada uno.
- Reconocer las tres anomalías del retraso de replicación y la garantía que mitiga cada una.
- Resolver conflictos multi-leader (evitar, converger con LWW/fusión, lógica on write/on read) y conocer CRDTs, merge de tres vías y transformación operacional.
- Calcular quórums con `w + r > n` e identificar los casos límite en que aún se leen valores obsoletos.
- Aplicar la relación happens-before y los version vectors para detectar concurrencia y fusionar siblings sin perder datos (uso de tombstones).
