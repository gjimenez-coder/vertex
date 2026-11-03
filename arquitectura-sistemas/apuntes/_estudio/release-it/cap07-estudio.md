# Capítulo 7 — Foundations (Fundamentos) — Estudio

## Tarjetas de repaso

P: ¿Qué significa "diseño para producción" (design for production)?
R: Tratar los problemas de producción (red, logging, monitorización, control en tiempo de ejecución y seguridad) como preocupaciones de primera clase, y diseñar también para las personas de operaciones, que son usuarios aunque interactúen vía interfaces de configuración, control y monitorización.

P: ¿Cuáles son las cinco capas del modelo de responsabilidad, de abajo arriba?
R: Foundation (hardware, VMs, IP, red física), Instances (servicios, procesos, monitorización de instancia), Interconnect (enrutamiento, balanceo, failover, tráfico), Control Plane (monitorización del sistema, despliegue, detección de anomalías, features) y Operations (seguridad, disponibilidad, capacidad, estado, comunicación).

P: ¿Por qué el libro evita las etiquetas "as a service" (IaaS, PaaS)?
R: Porque esas distinciones se han roto; es más útil mirar cada plataforma según qué capas conduce por API y qué responsabilidades se mueven de operaciones a desarrolladores.

P: ¿Cuáles son los dos sentidos del término *hostname*?
R: Primero, el nombre con que el SO se identifica (lo que devuelve `hostname`), que junto al dominio de búsqueda forma el FQDN; segundo, el nombre externo con el que otros se conectan, resuelto por DNS a una IP.

P: ¿Qué relación hay entre un nombre DNS y una IP, y por qué?
R: Es de muchos a muchos; la máquina usa su hostname para identificarse como un todo, mientras que un nombre DNS identifica una IP, y no hay garantía de que el FQDN propio coincida con el que DNS tiene para su IP.

P: ¿Qué es el *multihoming* y por qué casi todos los servidores del centro de datos lo son?
R: Que una máquina tenga varias NICs activas, cada una con IP en su propia red; se separan redes para reforzar la seguridad (aislar administración y monitorización) y mejorar el rendimiento (segmentar tráfico de alto volumen como backups).

P: ¿Qué hace el *bonding* o *teaming* de interfaces?
R: Hace que dos interfaces compartan una misma IP, con el SO garantizando que cada paquete sale por una sola; conectar interfaces bonded a switches distintos exige configuración extra en los switches para evitar bucles de enrutamiento.

P: ¿Cómo debe enlazar sus sockets una aplicación servidora en una máquina multihomed?
R: No a todas las interfaces por defecto ("a la fácil"), sino especificando la IP concreta ("a la difícil") mediante propiedades configurables que definan a qué interfaces enlazar.

P: ¿Qué filosofía de hardware se aplica a los hosts físicos?
R: Hardware desechable: balancear servicios entre suficientes hosts para que perder uno no sea catastrófico, que cada host sea lo más barato posible, y escalar horizontalmente; se apartan cargas especiales (mucha RAM, GPU) a sus propias máquinas.

P: ¿Qué problemas introducen las VMs en el centro de datos?
R: Rendimiento menos predecible, sobresuscripción (contención y ralentizaciones aleatorias) y relojes no fiables (no monótonos ni secuenciales por suspensión o migración); hay que diseñar apps insensibles a la pérdida o ralentización de un host y no confiar en el reloj del SO.

P: ¿Qué caracteriza la identidad de un contenedor y qué implica al diseñar?
R: Su identidad es efímera, así que no se configura por instancia; la imagen viaja entre entornos y no debe contener credenciales (inyectarlas al arrancar, password vaulting) ni hostnames/puertos (los pone el control plane), debe arrancar en ~1 s y enviar telemetría a un recolector externo.

P: ¿Qué software de control plane se menciona para colocar instancias en contenedores?
R: Kubernetes, Mesos y Docker Swarm; se les describe la carga deseada y deben conocer la distribución geográfica de los hosts.

P: ¿Qué son las VLAN y VXLAN según el recuadro del capítulo?
R: Una VLAN multiplexa tramas Ethernet con una etiqueta (1 a 4.094); VXLAN lleva la idea a capa 3 con 24 bits extra, permitiendo más de 16 millones de VXLANs.

P: ¿Cómo es la disponibilidad e identidad de una VM individual en la nube?
R: Peor disponibilidad que una física (más piezas móviles, otra capa de SO, puede matarse sin aviso, comparte host) e identidad efímera: en AWS la IP cambia en cada arranque y, si se necesitan direcciones fijas, se rentan Elastic IPs (con límite por cuenta).

P: ¿Qué regla general aplica a las VMs en la nube para recibir trabajo?
R: Las VMs "se ofrecen voluntarias" a trabajar en lugar de recibir trabajo de un controlador; una VM nueva debe poder unirse al pool (autoscaling y load balancers para HTTP, competing consumers sobre una cola para carga asíncrona).

## Preguntas de autoevaluación

P: ¿Por qué un diseño que funciona bien en un centro de datos físico puede fallar o costar demasiado en contenedores en la nube?
R: Porque el entorno de despliegue cambia la identidad y el tiempo de vida de las máquinas y la responsabilidad entre capas; por eso el entorno de despliegue debe ser una decisión de diseño consciente. (Sección: Lo que necesitas saber)

P: ¿Qué riesgo concreto corre una aplicación que no es consciente de sus múltiples interfaces de red?
R: Puede aceptar conexiones de la red equivocada, por ejemplo tráfico de administración desde la red de producción. (Sección: Networking in the Data Center and the Cloud)

P: En conexiones salientes, ¿cuándo debe la aplicación especificar la interfaz de salida?
R: Solo en casos raros; en producción normalmente es un error de configuración del host, salvo cuando dos NICs a dos switches están bonded en una sola interfaz (`bond0`), donde la solución es una puerta de enlace por defecto usando `bond0` en la tabla de rutas. (Sección: Programar para múltiples redes)

P: ¿Qué debes evitar al diseñar aplicaciones que corren sobre VMs sobresuscritas?
R: Técnicas distribuidas que exigen respuestas síncronas de todo el clúster, máquinas "especiales" (gestores de clúster o de bloqueos) sin relevo automático, y dependencias sutiles del orden de peticiones o eventos. (Sección: Physical Hosts, Virtual Machines, and Containers → VMs en el centro de datos)

P: ¿Cuáles son los dos retos mayores de los contenedores en el centro de datos?
R: La red (por defecto un contenedor no expone puertos en el host, de ahí el patrón de overlay network) y colocar las instancias correctas en las máquinas correctas, que se delega en el control plane. (Sección: Physical Hosts, Virtual Machines, and Containers → Contenedores en el centro de datos)

P: ¿Por qué se recomienda un servidor bastion o jumphost para SSH en la nube?
R: Para no abrir SSH en los NICs de front-end; el bastion concentra el acceso con logging fuerte. (Sección: Physical Hosts, Virtual Machines, and Containers → VMs en la nube)

P: ¿Qué preguntas comunes a todo entorno de despliegue plantea el cierre del capítulo?
R: Cómo está estructurada la red (una o varias, NICs en redes distintas con trabajos distintos), si las máquinas tienen identidades duraderas, y si se montan y desmontan automáticamente y cómo se gestionan sus imágenes. (Sección: Wrapping Up)

## Puntos a dominar

- Explicar las cinco capas del modelo (Foundation, Instances, Interconnect, Control Plane, Operations) y qué responsabilidad cubre cada una.
- Distinguir los dos sentidos de *hostname* y por qué la relación nombre DNS↔IP es de muchos a muchos.
- Justificar el multihoming y la separación de redes de producción, backups y administración.
- Saber que las apps servidoras deben enlazar sockets a IPs concretas y configurables, no a todas las interfaces.
- Comparar hosts físicos, VMs y contenedores en identidad, tiempo de vida y almacenamiento.
- Enumerar los peligros de las VMs sobresuscritas: contención, relojes no fiables (usar NTP) y dependencias síncronas del clúster.
- Enunciar las reglas de diseño de contenedores: sin credenciales ni hostnames/puertos en la imagen, arranque en ~1 s y telemetría externa.
- Describir las implicaciones de la nube: disponibilidad individual menor, IPs efímeras, Elastic IPs, VMs que se unen al pool, autoscaling, competing consumers y bastion para SSH.
- Recordar el checklist del 12-factor app y la diferencia entre VLAN y VXLAN.
