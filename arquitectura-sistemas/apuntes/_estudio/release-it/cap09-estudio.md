# Interconnect (Interconexión) — Estudio

## Tarjetas de repaso

P: ¿Qué reúne la capa de interconnect y para qué sirve? / R: Reúne gestión de tráfico, balanceo de carga y descubrimiento de servicios; convierte un montón de instancias en un sistema cohesionado y es donde se construye la alta disponibilidad.

P: ¿Según qué tres ejes se evalúa cada técnica de interconexión? / R: La tasa de cambio o dinamismo que soporta, cuánto apoyo operativo requiere y cuánto conocimiento global exige.

P: ¿Cuándo conviene DNS frente a herramientas dinámicas de descubrimiento? / R: DNS para equipos pequeños e infraestructuras que cambian lentamente; herramientas dinámicas (Consul y similares) para organizaciones grandes con muchos servicios y alta tasa de cambio.

P: ¿Qué significa "descubrimiento de servicios con DNS"? / R: Es un proceso humano ("más Sherlock Holmes que Siri"): el equipo localiza a los dueños, obtiene el nombre DNS y lo pone en un archivo de configuración.

P: ¿Cuáles son las limitaciones del balanceo DNS round-robin? / R: Todas las instancias deben ser enrutables, pone el control en el cliente sin poder redirigir, el servidor DNS no conoce la salud de las instancias, solo reparte conexiones iniciales y clientes Java cachean la primera IP.

P: ¿Qué es GSLB y cómo opera? / R: Global Server Load Balancing enruta clientes entre ubicaciones geográficas por cercanía de red; opera en dos niveles: global vía DNS con health checks y luego un balanceador local que actúa como reverse proxy.

P: ¿Qué es una VIP y qué define un "pool" en un balanceador activo? / R: La VIP (virtual IP) es la IP donde escucha el balanceador; cada VIP mapea a pools que definen las IPs de las instancias más la política: algoritmo, health checks, stickiness y qué hacer sin miembros disponibles.

P: ¿Diferencia entre balanceo por software y por hardware? / R: El software (reverse proxy como HAProxy o nginx) es barato y de capa de aplicación pero se sobrecarga; el hardware (como F5 Big-IP) da más capacidad y throughput en capas 4-7 pero cuesta cinco o seis dígitos.

P: ¿Qué es la stickiness y qué riesgo tiene? / R: Dirige peticiones repetidas a la misma instancia (útil con estado como sesión de usuario); mejora la respuesta pero puede desequilibrar la carga creando una máquina "caliente".

P: ¿Qué es load shedding y dónde conviene aplicarlo? / R: Rechazar el trabajo que no se puede completar a tiempo, lo más cerca del borde posible (los balanceadores) para no atar recursos; un rechazo rápido es mejor que un timeout lento.

P: Según el capítulo, ¿cómo empieza a fallar todo sistema? / R: Con una cola que se acumula en algún punto; bajo carga alta el servicio se ralentiza y quedan menos sockets justo cuando llegan más peticiones ("ir no lineal").

P: ¿Por qué un socket cerrado queda en TIME_WAIT? / R: Para que paquetes extraviados caduquen o sean descartados, evitando un "bogon" que descuadre el flujo TCP.

P: En términos del teorema CAP, ¿qué diferencia a ZooKeeper de Consul? / R: ZooKeeper es CP (ante una partición algunos nodos no responden, se necesita fallback); Consul es AP (prefiere seguir disponible a riesgo de datos obsoletos) y además hace health checks.

P: ¿Qué NO migra una IP virtual migratoria en un failover? / R: No migra el estado en memoria: se pierde el estado no persistente, incluidas transacciones no confirmadas.

## Preguntas de autoevaluación

P: ¿Por qué el equilibrio entre DNS y descubrimiento dinámico se desplaza con el tiempo? / R: Porque las grandes compañías crean herramientas open source (Spinnaker, Kubernetes, Mesos, Consul) que democratizan estas capacidades y las ponen al alcance de equipos pequeños. (Sección "Lo que necesitas saber")

P: ¿Por qué conviene usar siempre un nombre lógico de servicio en lugar de un hostname físico? / R: Porque el alias se cambia en un único sitio, lo que simplifica el mantenimiento del balanceo y la disponibilidad. (Sección "DNS")

P: ¿Qué principio clave rige la disponibilidad de DNS y cómo se aplica? / R: La diversidad: no alojar los servidores DNS sobre la misma infraestructura que producción, usar más de un proveedor DNS en ubicaciones distintas y otro proveedor para la página de estado pública. (Sección "DNS")

P: ¿Por qué los balanceadores por software no son totalmente transparentes y cómo se mitiga? / R: Porque el log muestra la IP del proxy como origen, no la del cliente real; se mitiga con la cabecera "X-Forwarded-For". (Sección "Load Balancing")

P: ¿Qué heurística propone el capítulo para dimensionar la cola de escucha? / R: Tiempo máximo de espera dividido por tiempo medio de procesamiento, más uno; multiplicar por el número de hilos de atención y subirlo un 50 %. (Sección "Demand Control")

P: ¿Cuál es el peor escenario de un enrutamiento de red mal configurado y cómo se previene? / R: Que datos con PII viajen en claro por Internet público mientras el servicio parece funcionar; se previene con rutas estáticas o SDN y documentando cada integración con nombre, dirección y ruta deseada. (Sección "Network Routing")

P: ¿Por qué no conviene implementar uno mismo el descubrimiento de servicios? / R: Como con los connection pools y las librerías de cripto, hay diferencia entre uno que funciona y uno que siempre funciona; mejor construir sobre ZooKeeper o etcd envueltos en una librería. (Sección "Discovering Services")

P: ¿Cómo debe prepararse la aplicación ante el failover de una IP virtual migratoria? / R: Debe manejar `SQLException` (updates, inserts y procedimientos no se repiten automáticamente) y tratar los `IOException` por cambio de interfaz distinto a un "destination unreachable", reintentando contra el nuevo nodo respetando los límites del Circuit Breaker. (Sección "Migratory Virtual IP Addresses")

## Puntos a dominar

- Situar la capa de interconnect entre la capa de instancias y el control plane, y evaluar técnicas por dinamismo, apoyo operativo y conocimiento global exigido.
- Saber cuándo usar DNS (cambio lento) y reconocer que su "descubrimiento" es humano y que round-robin no tiene conciencia de salud.
- Explicar GSLB y su coordinación en dos niveles (DNS global + balanceador local como reverse proxy).
- Distinguir VIP, pool y política; y comparar balanceo por software (reverse proxy, barato, capa 7) frente a hardware (capas 4-7, más escala, caro).
- Entender la importancia de health checks y el compromiso de la stickiness.
- Comprender cómo fallan los sistemas (colas que crecen, sockets, ley de Little, TIME_WAIT) y aplicar load shedding cerca del borde con HTTP 503 y back pressure.
- Dominar los riesgos del enrutamiento (disponibilidad y exposición de PII) y las soluciones: rutas estáticas, SDN y registro de integraciones.
- Diferenciar sistemas CP (ZooKeeper) y AP (Consul) en descubrimiento de servicios y la necesidad de cachear resultados.
- Saber qué resuelve y qué no una IP virtual migratoria (failover activo/pasivo sin migrar estado en memoria).
