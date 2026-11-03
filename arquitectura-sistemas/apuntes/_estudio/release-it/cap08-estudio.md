# Processes on Machines (Procesos en las máquinas) — Estudio

## Tarjetas de repaso

P: ¿Qué tres elementos necesita toda máquina según la analogía del motor?
R: Code, config y connection (código, configuración y conexión), igual que el motor necesita combustible, fuego y aire.

P: ¿Qué significa que una instancia sea un "buen ciudadano"?
R: Aportar transparencia, aceptar control, manejar bien la configuración y gestionar sus conexiones, aceptando el estrés con tolerancia y gracia.

P: ¿Qué es un *service* en el vocabulario del capítulo?
R: Una colección de procesos a través de máquinas que cooperan para entregar una unidad de funcionalidad; puede incluir varios ejecutables.

P: ¿Cuál es la diferencia entre *instance*, *executable* y *process*?
R: Instance es una instalación en una sola máquina dentro de un array balanceado; executable es el artefacto lanzable creado por un build; process es el proceso del SO, la imagen en ejecución del ejecutable.

P: ¿Qué son *installation* y *deployment*?
R: Installation es el ejecutable más sus directorios, ficheros de configuración y recursos en una máquina; deployment es el acto de crear una instalación, que debe ser automatizado y versionado.

P: ¿Por qué los desarrolladores no deben hacer builds de producción desde sus máquinas?
R: Porque sus máquinas están "irremediablemente contaminadas"; los builds de producción solo deben hacerse en un servidor de CI que deposite el binario en un repositorio seguro de solo escritura restringida.

P: ¿Qué es la infraestructura inmutable y desechable?
R: Partir siempre de una imagen base conocida, aplicar un conjunto fijo de cambios y no volver a parchear; cuando hace falta un cambio, se crea una nueva imagen y se desecha la vieja.

P: ¿Cómo deben nombrarse las propiedades de configuración?
R: Por su función y no por su naturaleza; por ejemplo `authenticationProvider` en vez de `hostname`, para que el admin sepa qué debe buscar.

P: ¿Qué es la transparencia de un sistema?
R: El conjunto de cualidades que permiten a operadores, desarrolladores y patrocinadores entender tendencias históricas, condiciones presentes, estado instantáneo y proyecciones futuras.

P: ¿Cuál es la diferencia entre tecnologías black-box y white-box de transparencia?
R: Black-box se sitúan fuera del proceso y lo observan desde afuera (p. ej. logs recogidos por un scraper); white-box corren dentro del proceso como un agente y, aunque más acopladas, emiten eventos y métricas muy específicos.

P: ¿Qué debe registrarse como "ERROR"/"SEVERE" en los logs?
R: Solo lo que requiere acción; un circuit breaker que se abre o un fallo de conexión a BD sí son errores, pero un `NullPointerException` o una tarjeta inválida no lo son automáticamente.

P: ¿Por qué debe la monitorización ser un "exoesqueleto" y no un tejido interno?
R: Para evitar acoplamiento; umbrales, alertas y "roll up" de salud son decisiones de política que deben quedar fuera de la instancia.

P: ¿Qué información debe reportar un health check además de "está corriendo"?
R: La(s) IP del host, la versión del runtime/intérprete, la versión o commit ID de la app, si acepta trabajo, y el estado de connection pools, cachés y circuit breakers.

P: ¿Qué identificador conviene incluir en los logs y para qué?
R: Un identificador de transacción (user ID, session ID, transaction ID o número arbitrario) para poder hacer grep y trazar una transacción tras una caída.

## Preguntas de autoevaluación

P: ¿Por qué el capítulo insiste tanto en acordar un vocabulario preciso? (Vocabulario)
R: Porque los equipos se han visto perjudicados cuando distintas personas usan la misma palabra para cosas diferentes; en operaciones decir "reinicia el servidor" puede ser ambiguo sobre qué servidor y si se mata un proceso o la máquina entera.

P: ¿Cuáles son los dos problemas del enfoque "capas de estuco" de Chef/Puppet/Ansible? (Code — Immutable and Disposable Infrastructure)
R: Efectos colaterales no descritos por las recetas (estados que ni la receta original ni la nueva pueden recrear) y máquinas o scripts que solo funcionaron a medias y dejan estado indefinido.

P: ¿Por qué debe mantenerse la configuración por entorno en un repositorio distinto al del código fuente? (Configuration — Configuration Files)
R: Porque contiene lo más sensible, como contraseñas de BD de producción, y tarde o temprano alguien comitea una contraseña; se necesita acceso restringido y controles para conceder y revocar accesos.

P: ¿Qué desventajas tiene usar un servicio de configuración como ZooKeeper o etcd? (Configuration — Configuration with Disposable Infrastructure)
R: Crea una dependencia dura (su caída es "Severity 1" y las instancias no arrancan), es software distribuido complejo que exige madurez operativa y buena topología de red, y no vale la pena por una sola aplicación; los equipos pequeños están mejor con config inyectada.

P: ¿Cómo puede la visibilidad local llevar a decisiones erróneas? (Transparency — Designing for Transparency)
R: Lleva a optimización local (un retailer optimizó batch jobs dos horas pero los ítems seguían sin aparecer por un proceso paralelo) y puede enmascarar efectos de escala (servidores invalidando cachés entre sí, visible solo al juntar todas las estadísticas).

P: ¿Por qué casi nunca es buena idea dejar debug logs en producción? (Logging — Debug Logs / Voodoo Operations)
R: Porque el ruido entierra los problemas reales; además mensajes ambiguos de debug generan "voodoo operations", como la administradora que hizo failovers semanales durante seis meses por un mensaje temporal sin relación causal con la BD.

P: ¿Para qué sirve el health check en la gestión de tráfico? (Transparency — Health Checks)
R: Los clientes no lo consultan directamente; lo usa el balanceador para detectar caídas y para la transición "go live" cuando el health check pasa de fallar a pasar.

P: ¿Por qué deben separarse los logs del directorio de instalación? (Logging — Log Locations)
R: Porque los logs crecen rápido y consumen I/O; conviene ponerlos en otra unidad, dar el mínimo permiso de escritura al directorio de código y hacer la ubicación configurable para que los admins no la muevan con symlinks.

## Puntos a dominar

- Explicar la analogía code/config/connection y qué significa que una instancia sea "buen ciudadano".
- Definir con precisión service, instance, executable, process, installation y deployment, y separar la vista estática de despliegue de la dinámica de ejecución.
- Describir la cadena de custodia del código: control de versiones, repositorio privado con firmas digitales, cuidado con plugins del build y builds de producción solo en CI.
- Argumentar las ventajas de la infraestructura inmutable y desechable frente al parcheo en caliente.
- Justificar sacar la configuración por entorno fuera del árbol de fuentes y a un repositorio aparte, y nombrar propiedades por función.
- Comparar inyección de configuración vs. servicio de configuración (ZooKeeper/etcd) y cuándo conviene cada uno.
- Explicar por qué la transparencia se diseña desde el inicio y cómo la visibilidad local distorsiona decisiones.
- Distinguir tecnologías black-box y white-box, y aplicar buenas prácticas de logging (niveles, ubicación, factores humanos, identificador de transacción).
- Enumerar qué debe reportar un health check y su papel en la gestión de tráfico del balanceador.
