# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 8 — Processes on Machines (Procesos en las máquinas)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF `(PDF p. N)`.

## Lo que necesitas saber

Tras revisar los entornos de red y físicos del capítulo anterior, este capítulo baja al nivel de la instancia individual. Cada instancia debe ser un "buen ciudadano": aportar transparencia, aceptar control, manejar bien la configuración y gestionar sus conexiones. Hay solapamiento natural con los patrones de estabilidad del Capítulo 5, porque es trabajo de cada instancia aceptar el estrés y los golpes con tolerancia y gracia.

La tesis se resume con la analogía del motor: igual que necesita combustible, fuego y aire, nuestro software necesita code, config y connection (código, configuración y conexión). Toda máquina necesita el código correcto, la configuración correcta y las conexiones de red correctas.

Antes de avanzar, el autor fija vocabulario porque los equipos se han visto perjudicados cuando distintas personas usan la misma palabra para cosas diferentes. La comunicación precisa importa especialmente en operaciones: si dices "reinicia el servidor", puede que no sepas qué servidor van a tumbar ni si matarán un proceso o la máquina entera.

Sales sabiendo cómo hacer una instancia desplegable, configurable y monitorizable, y por qué la transparencia debe diseñarse desde el principio.

## El ejemplo que recorre el capítulo

El servicio "Loan Request" (`loanrequest.example.com`): varias máquinas ejecutan una instancia del mismo binario, todas detrás de un balanceador HAProxy con la dirección `10.10.128.19`. Sirve para distinguir la vista de despliegue (estática: transformar fuentes en binarios y binarios en instalaciones) de la vista de ejecución (dinámica: los procesos corriendo en las máquinas). Mucha confusión arquitectónica nace de meter ambas vistas en la misma figura.

## Vocabulario

- **Service**: colección de procesos a través de máquinas que cooperan para entregar una unidad de funcionalidad; puede incluir varios ejecutables (p. ej. código de aplicación más base de datos).
- **Instance**: una instalación en una sola máquina (contenedor, virtual o física) dentro de un array balanceado del mismo ejecutable.
- **Executable**: artefacto que una máquina puede lanzar como proceso, creado por un build (binario, o fuentes en lenguajes interpretados; también cubre librerías compartidas).
- **Process**: proceso del sistema operativo; la imagen en ejecución de un ejecutable.
- **Installation**: el ejecutable más sus directorios, ficheros de configuración y recursos tal como existen en una máquina.
- **Deployment**: el acto de crear una instalación; debe ser automatizado y con la definición en control de versiones.

## Code

Construir el código exige una fuerte "chain of custody" (cadena de custodia) desde el desarrollador hasta la instancia de producción: debe ser imposible que alguien no autorizado cuele código.

- Solo el código va al control de versiones; este no maneja bien librerías de terceros ni dependencias.
- Descargar dependencias de Internet es cómodo pero inseguro: una dependencia puede ser reemplazada por un man-in-the-middle o comprometiendo el repositorio upstream. Hay que pasar a un repositorio privado y meter librerías solo cuando su firma digital coincide con la publicada. Tampoco olvides los plugins del build (un ataque llegó vía un plugin de Jenkins comprometido).
- Los desarrolladores no deben hacer builds de producción desde sus máquinas, que están "irremediablemente contaminadas". Haz los builds de producción solo en un servidor de CI que deposite el binario en un repositorio seguro de solo escritura restringida.

**Immutable and Disposable Infrastructure.** Herramientas como Chef, Puppet y Ansible aplican cambios a máquinas en ejecución (el enfoque "capas de estuco"). Tiene dos problemas: efectos colaterales no descritos por las recetas (una máquina acaba en un estado que ni la receta original ni la nueva pueden recrear) y máquinas o scripts que solo funcionaron a medias y dejan estado indefinido. La comunidad DevOps/cloud prefiere partir siempre de una imagen base conocida, aplicar un conjunto fijo de cambios y no volver a parchear: cuando hace falta un cambio, se crea una nueva imagen ("immutable infrastructure"). Un contenedor es el ejemplo: no se parchea, se construye uno nuevo, se lanza y se desecha el viejo. Lo importante es la disponibilidad para desechar el entorno y empezar de nuevo.

## Configuration

La configuración es parte de la interfaz de usuario del sistema, usada por desarrolladores y operadores. Sufre de "hidden linkages" y alta complejidad, dos de los mayores factores de error del operador.

**Configuration Files.** Algunas propiedades deben variar por máquina: mantenlas en lugares separados para que nadie dude "¿se supone que esto es diferente?". El binario no debe cambiar por entorno, pero sus propiedades sí, así que el código debe buscar fuera del directorio de despliegue la configuración por entorno. Estos ficheros contienen lo más sensible (contraseñas de BD de producción): mantenlos en un repositorio distinto al del código fuente (tarde o temprano alguien comitea una contraseña; GitHub muestra 288.093 commits titulados "Removed password"), con acceso restringido y controles para conceder y revocar accesos.

**Configuration with Disposable Infrastructure.** En entornos basados en imágenes (EC2, contenedores) los ficheros no pueden cambiar por instancia. Dos enfoques:
- *Inyectar configuración* al arranque, vía variables de entorno o un blob de texto (EC2 usa "user data"; Heroku prefiere variables de entorno). El código debe saber leer y parsear ese formato.
- *Servicio de configuración* (ZooKeeper, etcd): la instancia pide su configuración a una ubicación conocida. Crea una dependencia dura: la caída del servicio es "Severity 1" y las instancias no arrancan. Son software distribuido complejo que exige madurez operativa y topología de red bien planeada; ZooKeeper es escalable pero no elástico. No vale la pena por una sola aplicación. Los equipos pequeños están mejor con config inyectada.

**Naming Configuration Properties.** Nombra las propiedades por su función, no por su naturaleza. No la llames `hostname` solo porque es un hostname; llámala `authenticationProvider` para que el admin sepa que debe buscar un host LDAP o Active Directory.

## Transparency

La transparencia reúne las cualidades que permiten a operadores, desarrolladores y patrocinadores entender tendencias históricas, condiciones presentes, estado instantáneo y proyecciones futuras del sistema. Los sistemas transparentes comunican y, al comunicar, entrenan a las personas que los atienden; depurarlos es mucho más fácil, por lo que maduran más rápido que los opacos. Un sistema sin transparencia no sobrevive mucho en producción: no se puede afinar, mejorar ni justificar su financiación, y se degrada con cada release.

**Designing for Transparency.** La transparencia surge del diseño deliberado; "añadir transparencia" tarde cuesta tanto como "añadir calidad". La visibilidad estrictamente local lleva a optimización local (un retailer optimizó batch jobs dos horas, pero los ítems seguían sin aparecer hasta las 5-6 a.m. por un proceso paralelo). La visibilidad de una sola instancia puede enmascarar efectos de escala (cada servidor invalidaba las cachés de los demás; solo se vio al juntar todas las estadísticas en una página). Vigila el acoplamiento: la monitorización debe ser un exoesqueleto alrededor del sistema, no tejido en su interior; umbrales, alertas y "roll up" de salud son decisiones de política que deben quedar fuera de la instancia.

**Enabling Technologies.** Un proceso es opaco por naturaleza (como el gato de Schrödinger). Hay dos clases de tecnologías:
- *Black-box*: se sitúan fuera del proceso y lo observan desde afuera; se implementan después de entregar, normalmente por operaciones (p. ej. buenos logs en ficheros de texto que cualquier scraper recoge sin molestar al proceso).
- *White-box*: corren dentro del proceso, como un agente en una librería del lenguaje; se integran durante el desarrollo y están más acopladas, pero su API permite emitir eventos y métricas muy específicos.

**Logging.** Los log files siguen siendo la herramienta más fiable y versátil, y el acoplamiento más laxo posible. Claves:
- *Log Locations*: no uses un `logs` bajo el directorio de instalación; los logs crecen rápido y consumen I/O. Sepáralos (idealmente otra unidad en máquinas físicas); el directorio de código debe tener el mínimo permiso de escritura posible. En contenedores suele bastar con emitir por standard out. Haz la ubicación configurable o los admins la moverán con symlinks.
- *Logging Levels*: dirige el logging a operaciones, no a desarrollo. Lo registrado como "ERROR"/"SEVERE" debe requerir acción. No toda excepción es un error (una tarjeta inválida es un warning, si acaso). Un circuit breaker que se abre o un fallo de conexión a BD sí son errores; un `NullPointerException` no lo es automáticamente.
- *Debug Logs in Production*: casi nunca buena idea; el ruido entierra los problemas reales. Añade un paso en el build que elimine automáticamente configs que habiliten debug o trace.
- *Human Factors*: los logs son interfaz humano-computadora. En un incidente Severity 1, la mala interpretación agrava el problema (los operadores de Three Mile Island interpretaron mal presión y temperatura). El formato debe ser legible; columnas rotas y margen izquierdo irregular no lo son.
- *Voodoo Operations*: tendemos a detectar patrones incluso donde no los hay. Una administradora hacía failovers semanales de BD durante seis meses por un mensaje ambiguo ("Data channel lifetime limit reached. Reset required.") que era un mensaje de debug sin relación causal con la BD, solo temporal. Lección: mensajes claros y no dejar debug activo.
- *Final Notes on Logging*: incluye un identificador para trazar una transacción (user ID, session ID, transaction ID o un número arbitrario) y así poder hacer grep tras una caída. Registra las transiciones de estado interesantes aunque uses SNMP o JMX; son valiosas en el postmortem.

**Instance Metrics.** La instancia no conoce la salud global, pero debe emitir métricas para recolección y visualización central (p. ej. volcar estadísticas a un log). Se puede externalizar a servicios como New Relic o Datadog, con plugins por lenguaje y runtime; útil para equipos pequeños que así evitan mantener infraestructura de métricas. (Chiste de Netflix: es un sistema de monitorización que, de paso, transmite películas.)

**Health Checks.** Página o llamada de API que revela la visión interna de salud de la aplicación. Debe reportar más que "sí, está corriendo": la(s) IP del host, la versión del runtime/intérprete, la versión o commit ID de la app, si la instancia acepta trabajo, y el estado de connection pools, cachés y circuit breakers. Es clave para la gestión de tráfico: los clientes no lo consultan directamente, lo usa el balanceador para detectar caídas y para la transición "go live" cuando el health check pasa de fallar a pasar.

## Ideas clave

- Toda instancia necesita code, config y connection, y debe ser buen ciudadano: transparente, controlable, bien configurada y capaz de gestionar conexiones.
- Acuerda vocabulario preciso (service, instance, executable, process, installation, deployment) y separa la vista estática de despliegue de la dinámica de ejecución.
- Protege la cadena de custodia del código: control de versiones, repositorio privado con firmas, cuidado con plugins y builds de producción solo en CI.
- Prefiere infraestructura inmutable y desechable: parte de una imagen base, nunca parches en caliente.
- Saca la configuración por entorno fuera del árbol de fuentes y de un repositorio aparte; nombra propiedades por función; en entornos de imágenes, inyecta config (los servicios tipo ZooKeeper/etcd añaden complejidad y dependencia dura).
- La transparencia se diseña desde el inicio; la visibilidad local lleva a optimización local y puede enmascarar efectos de escala. La monitorización es un exoesqueleto, no un tejido interno.
- Los log files son la herramienta más versátil: dirígelos a operaciones, usa niveles con sentido, evita debug en producción y trata los logs como interfaz humana.
- Las métricas y los health checks (con IP, versiones, estado de pools, cachés y circuit breakers) alimentan la transparencia del sistema y la gestión de tráfico por el balanceador.
