# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 7 — Foundations (Fundamentos)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El capítulo abre la sección del libro dedicada al "diseño para producción" (*design for production*): tratar los problemas de producción como preocupaciones de primera clase. Eso abarca la red de producción (que puede diferir mucho del entorno de desarrollo), el logging, la monitorización, el control en tiempo de ejecución y la seguridad. También implica diseñar para las personas de operaciones: los operadores también son usuarios, aunque interactúen con el sistema a través de interfaces de configuración, control y monitorización en lugar de un front-end bonito.

Nygard presenta un modelo por capas sobre el que se construye todo, empezando por la infraestructura física; los capítulos siguientes irán ampliando el foco hacia preocupaciones más distribuidas. Este capítulo se queda en la capa de Fundamentos (*Foundation*): las máquinas y los cables sobre los que se apoya el resto.

Sales sabiendo cómo funcionan realmente hostnames, NICs e IP en un centro de datos, y cómo afectan al diseño del software las distintas opciones de despliegue: hosts físicos, máquinas virtuales y contenedores, tanto en el centro de datos como en la nube. La tesis central es que un diseño que funciona bien en un centro de datos físico puede costar demasiado o fallar por completo en un entorno de contenedores en la nube, de modo que el entorno de despliegue debe ser una decisión de diseño consciente.

## El modelo de capas

El capítulo parte de un diagrama con cinco capas de responsabilidad, de abajo arriba:

- **Foundation**: hardware, VMs, direcciones IP, red física.
- **Instances**: servicios, procesos, componentes, monitorización de instancia.
- **Interconnect**: enrutamiento, balanceo de carga, failover, gestión de tráfico.
- **Control Plane**: monitorización del sistema, despliegue, detección de anomalías, features.
- **Operations**: seguridad, disponibilidad, capacidad, estado, comunicación.

Las etiquetas "as a service" (IaaS, PaaS) no aparecen a propósito: esas distinciones se han roto. Es más útil mirar cada plataforma según qué capas conduce por API y qué responsabilidades se mueven de operaciones a desarrolladores.

## Networking in the Data Center and the Cloud (NICs y nombres)

La red del centro de datos y la nube incorpora más redundancia y seguridad que una red de escritorio, y con la virtualización las aplicaciones se comportan distinto que en el IDE.

El término *hostname* tiene dos sentidos. Primero, el nombre con que el sistema operativo se identifica (lo que devuelve el comando `hostname`); junto al dominio de búsqueda forma el FQDN (fully qualified domain name). Segundo, el nombre externo con el que otros se conectan, que se resuelve vía DNS a una IP. No hay garantía de que el FQDN propio de la máquina coincida con el que DNS tiene para su IP: la máquina usa su hostname para identificarse como un todo, mientras que un nombre DNS identifica una IP. La relación "nombre DNS ↔ IP" es de muchos a muchos.

Hay otra relación de muchos a muchos: una máquina puede tener varias NICs (controladoras de red). Cada NIC activa recibe una IP en su propia red; esto se llama *multihoming*, y casi todos los servidores del centro de datos están multihomed. Se separan redes para reforzar la seguridad (aislar administración y monitorización) y para mejorar el rendimiento (segmentar tráfico de alto volumen, como los backups). Una aplicación que no es consciente de las múltiples interfaces puede aceptar conexiones de la red equivocada (p. ej., administración desde la red de producción).

El ejemplo del servidor con cuatro interfaces (convención Unix `eth0`–`eth3`): dos dedicadas a tráfico de producción (hacia switches distintos, en alta disponibilidad; pueden ir balanceadas o como par de failover), una para backups y otra para acceso administrativo. El *bonding* o *teaming* hace que dos interfaces compartan una misma IP, con el SO garantizando que cada paquete sale por una sola; conectar interfaces bonded a switches distintos exige configuración extra en los switches para evitar bucles de enrutamiento. La red administrativa permite ligar servicios como SSH solo a esa interfaz, de modo que no sean accesibles desde producción.

### Programar para múltiples redes

Por defecto, una aplicación que escucha en un socket lo hace en todas las interfaces (la versión "fácil"). Hay que hacerlo "a la difícil" y especificar la IP:

```go
// Bad approach
ln, err := net.Listen("tcp", ":8080")
// Good approach
ln, err := net.Listen("tcp", "spock.example.com:8080")
```

En desarrollo basta `getLocalHost()`, pero en una máquina multihomed eso devuelve la IP del hostname interno, que puede ser cualquiera de las interfaces. Las aplicaciones servidoras deben añadir propiedades configurables para definir a qué interfaces enlazar.

**Conexiones salientes**: solo en casos raros la aplicación debe especificar por qué interfaz sale el tráfico; en producción Nygard lo considera un error de configuración del host. La excepción es cuando dos NICs a dos switches están bonded en una sola interfaz (`bond0`): la solución es que la tabla de rutas tenga una puerta de enlace por defecto usando `bond0`.

## Physical Hosts, Virtual Machines, and Containers

Al final todo corre sobre silicio, pero las opciones de despliegue obligan a pensar en la identidad y el tiempo de vida de las máquinas; no son meros temas de empaquetado.

**Hosts físicos**: CPU x86 de 64 bits multinúcleo, muy similares entre desarrollo y centro de datos. La filosofía actual es hardware desechable: balancear servicios entre suficientes hosts para que perder uno no sea catastrófico, y que cada host sea lo más barato posible. Excepciones: cargas con mucha RAM (procesamiento de grafos) y computación GPU (algoritmos "embarrassingly parallel"). El almacenamiento suele estar fuera del host, como SAN o NAS; a la aplicación ambos le parecen un punto de montaje, y conviene medir el throughput (se menciona Bonnie 64). Diseñar para producción aquí significa, sobre todo, escalar horizontalmente.

**VMs en el centro de datos**: la virtualización ofreció una apariencia de hardware común y combatió el "server sprawl" con alta densidad. A cambio, el rendimiento es menos predecible. Los hosts suelen estar sobresuscritos (p. ej., 16 núcleos físicos con 32 asignados a VMs = 200% suscrito, 100% sobresuscrito), lo que genera contención y ralentizaciones aleatorias que el SO invitado apenas puede monitorizar. Hay que diseñar aplicaciones insensibles a la pérdida o ralentización de un host; cuidado con: técnicas distribuidas que exigen respuestas síncronas de todo el clúster, máquinas "especiales" (gestores de clúster o de bloqueos) sin relevo automático, y dependencias sutiles del orden de peticiones o eventos. Las VMs empeoran los relojes: no se puede asumir que el reloj sea monótono ni secuencial (la VM puede suspenderse o migrar a un host con desfase). No confíes en el reloj del SO; si importa el tiempo humano, usa una fuente externa como un servidor NTP local.

**Contenedores en el centro de datos**: prometen el aislamiento y empaquetado de una VM con un proceso de build amigable para el desarrollador ("¿producción coincide con QA?"). Su identidad es efímera, así que no se configuran por instancia (lo que descoloca a monitores antiguos como Nagios). Tienen poco o ningún almacenamiento local, así que dependen de almacenamiento externo. El reto mayor es la red: por defecto un contenedor no expone puertos en el host; aparece el patrón de *overlay network* (con VLANs, espacio IP propio y switches software). El segundo reto es colocar las instancias correctas en las máquinas correctas; se delega en software de control plane (Kubernetes, Mesos, Docker Swarm) al que se le describe la carga deseada y que debe conocer la distribución geográfica de los hosts. Al diseñar: la imagen viaja entre entornos, así que no debe contener credenciales (inyectarlas al arrancar; mirar *password vaulting*) ni hostnames/puertos (los establece el control plane). Evita secuencias de arranque largas (meta: ~1 segundo). Depurar dentro de un contenedor es notoriamente difícil, así que envía la telemetría a un recolector externo.

El recuadro del **12-factor app** (de Heroku) sirve de checklist: Codebase, Dependencies, Config, Backing services, Build/release/run, Processes, Port binding, Concurrency, Disposability, Dev/prod parity, Logs, Admin processes. El recuadro de **VLAN/VXLAN** explica que una VLAN multiplexa tramas Ethernet con una etiqueta (1 a 4.094) y VXLAN lleva la idea a capa 3 con 24 bits extra (más de 16 millones de VXLANs).

**VMs en la nube**: AWS es dominante (Google Cloud ganando terreno). Las apps tradicionales corren en la nube, pero un sistema *cloud native* tiene mejor disponibilidad y coste. Una VM individual en la nube tiene peor disponibilidad que una física (más piezas móviles, otra capa de SO, puede matarse sin aviso, comparte host). La identidad de la máquina es efímera: en AWS la IP cambia en cada arranque, y si necesitas direcciones fijas rentas Elastic IPs (con límite por cuenta). Regla general: las VMs "se ofrecen voluntarias" a trabajar en lugar de recibir trabajo de un controlador; una VM nueva debe poder unirse al pool. Para HTTP, autoscaling y load balancers (ELB o ALB); para carga asíncrona, *competing consumers* sobre una cola. Por defecto una VM trae una NIC con IP privada; un único NIC soporta ~64.000 conexiones (sockets 1–65535), así que puedes querer más NICs por capacidad o para separar tráfico de gestión. Para SSH, usa un servidor *bastion* o *jumphost* con logging fuerte en lugar de abrir SSH en los NICs de front-end.

**Contenedores en la nube**: combinan los retos de contenedores y nube (identidad efímera, enlazar puertos entre VMs de distintas zonas o regiones). Diseñar un servicio individual no cambia mucho respecto al centro de datos; los retos grandes están en ensamblar el sistema completo, lo que empuja complejidad hacia el control plane (capítulo 10).

## Wrapping Up (Cierre)

Los entornos de despliegue mueven la frontera de responsabilidad entre desarrollo de aplicación, de plataforma, operaciones e infraestructura. Preguntas comunes a todo entorno: ¿Cómo está estructurada la red; hay una o varias; tendrá la máquina NICs en redes distintas con trabajos distintos? ¿Tienen las máquinas identidades duraderas? ¿Se montan y desmontan automáticamente; cómo gestionamos sus imágenes? Estas respuestas rara vez aparecen en un tablero Kanban o un ticket de Jira, pero son esenciales para una transición suave a operaciones.

## Ideas clave

- "Diseño para producción" trata la red, el logging, la monitorización, el control y la seguridad como preocupaciones de primera clase; los operadores también son usuarios.
- *hostname* tiene dos sentidos (identidad propia del SO vs. nombre DNS externo); la relación nombre↔IP es de muchos a muchos y no tienen por qué coincidir.
- Los servidores del centro de datos están multihomed; separar producción, backups y administración en redes distintas es seguridad y rendimiento.
- Las apps servidoras deben enlazar sockets a IPs concretas y configurables, no a todas las interfaces por defecto.
- Hardware desechable y escalado horizontal; aparta cargas especiales (mucha RAM, GPU) a sus propias máquinas.
- En VMs, asume sobresuscripción, contención y relojes no fiables: no dependas de respuestas síncronas de todo el clúster ni confíes en el reloj del SO (usa NTP).
- Los contenedores tienen identidad efímera: externaliza credenciales y red, arranca en ~1 s y manda la telemetría fuera; el control plane (Kubernetes, Mesos, Docker Swarm) coloca instancias y gestiona la red.
- En la nube, las VMs tienen peor disponibilidad individual e IPs efímeras: diseña para que se unan solas a un pool (autoscaling, load balancers, competing consumers) y usa un bastion para SSH.
