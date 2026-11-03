# Release It! Design and Deploy Production-Ready Software (2nd Edition) — Michael T. Nygard (The Pragmatic Bookshelf, 2018)
## Capítulo 3 — Stabilize Your System (Estabiliza tu sistema)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber

El software empresarial debe ser cínico: esperar que ocurran cosas malas y protegerse de ellas, porque el mundo real no se parece al laboratorio, donde todas las pruebas las diseña alguien que ya sabe la respuesta esperada. Un software cínico ni siquiera confía en sí mismo y levanta barreras internas; se niega a intimar demasiado con otros sistemas porque podría salir dañado. El proyecto Core Facilities de la aerolínea del capítulo 2 no fue lo bastante cínico: el equipo se dejó deslumbrar por la nueva tecnología y la arquitectura avanzada, y no vio la señal de alto.

La mala estabilidad tiene costos reales y altos. El más evidente es la pérdida de ingresos: el minorista del capítulo 1 pierde 1.000.000 de dólares por hora de caída, incluso en temporada baja; los sistemas de trading pueden perder esa cifra en una sola transacción fallida. Estudios del sector indican que adquirir un cliente puede costar hasta 150 dólares a un minorista en línea; con 5.000 visitantes únicos por hora y un 10 por ciento que se marcha para siempre, eso supone 75.000 dólares de marketing desperdiciado. Menos tangible, pero igual de doloroso, es la pérdida de reputación.

La buena noticia es que la buena estabilidad no tiene por qué costar más. En la arquitectura, el diseño e incluso la implementación de bajo nivel hay puntos de decisión con gran apalancamiento sobre la estabilidad final. Ante ellos, dos caminos pueden satisfacer los requisitos funcionales (apuntando a QA): uno lleva a horas de caída al año y el otro no, y lo sorprendente es que el diseño estable suele costar lo mismo que el inestable.

## El ejemplo que recorre el capítulo

La aerolínea del proyecto Core Facilities (CF) del capítulo 2 sirve de hilo conductor. CF no planificó sus modos de fallo: la grieta empezó en el manejo incorrecto de una `SQLException`, pero podría haberse detenido en muchos otros puntos. El capítulo recorre esos puntos, de lo más bajo a lo más alto, para mostrar cómo contener la propagación.

## Definir la estabilidad

- **Transacción**: unidad abstracta de trabajo que procesa el sistema. No es lo mismo que una transacción de base de datos; una unidad de trabajo puede abarcar muchas transacciones de base de datos. Ejemplo: "cliente realiza un pedido". Son la razón de ser del sistema.
- **Sistema dedicado**: procesa un solo tipo de transacción. **Carga mixta (mixed workload)**: combinación de distintos tipos de transacciones.
- **Sistema**: el conjunto completo e interdependiente de hardware, aplicaciones y servicios necesario para procesar transacciones de los usuarios. Puede ser tan pequeño como una sola aplicación o una red extensa multicapa.
- **Sistema robusto**: sigue procesando transacciones aun cuando impulsos transitorios, estreses persistentes o fallos de componentes perturban el procesamiento normal. No basta con que los servidores sigan en pie: el usuario tiene que poder seguir trabajando.
- **Impulso (impulse)** y **estrés (stress)** vienen de la ingeniería mecánica. Un impulso es un choque rápido, como golpear el sistema con un martillo; el estrés es una fuerza aplicada durante un periodo prolongado.
- **Deformación (strain)**: el estrés produce deformación. Un procesador de tarjetas lento (estrés) propaga deformación a otras partes: más uso de RAM en los servidores web, exceso de I/O en la base de datos u otros efectos distantes.
- **Longevidad**: capacidad de seguir procesando transacciones mucho tiempo. Una definición útil de "mucho tiempo" es el tiempo entre despliegues de código.

Ejemplos de impulsos: una flash mob sobre la página de la PlayStation 6, un tuit de una celebridad, o volcar doce millones de mensajes en una cola a medianoche.

## Alargar la vida útil (Extending Your Life Span)

Los mayores peligros para la longevidad son las fugas de memoria y el crecimiento de datos; ambos tipos de "lodo" matan el sistema en producción y rara vez se detectan en pruebas. Por la ley de Murphy, aquello contra lo que no pruebes ocurrirá: si no pruebas caídas justo pasada la medianoche o errores de memoria en la hora 49 de actividad, sucederán.

El problema es que las aplicaciones nunca corren lo suficiente en desarrollo para revelar bugs de longevidad; en QA se reciclan a diario o más. Las pruebas de carga tampoco los capturan, porque corren un tiempo acotado y los proveedores cobran caro por hora. La única forma de atraparlos antes de producción es hacer tus propias pruebas de longevidad: dedica una máquina con JMeter, Marathon u otra herramienta, sin golpear fuerte pero generando peticiones de forma continua, y deja que los scripts aflojen unas horas al día para simular la madrugada y así detectar timeouts de pools de conexión y firewalls. Si la economía no lo justifica, prueba las partes importantes con el resto en stubs. Si todo falla, producción se convierte en tu entorno de longevidad por defecto.

## Modos de fallo (Failure Modes)

Tanto los impulsos repentinos como el estrés excesivo pueden desencadenar un fallo catastrófico; algún componente empieza a fallar antes que el resto. En *Inviting Disaster* [Chi01], James R. Chiles los llama "grietas en el sistema" y traza una analogía con una placa de acero con una microfisura: bajo estrés la grieta se propaga cada vez más rápido hasta que el metal se rompe explosivamente. El disparador original, la forma en que la grieta se extiende y el daño resultante se llaman en conjunto **modo de fallo**.

Todo sistema tendrá varios modos de fallo. Negar la inevitabilidad del fallo te quita el poder de controlarlo; aceptarlo te permite diseñar la reacción del sistema. Igual que los ingenieros de automóviles crean zonas de deformación que fallan primero para proteger a los pasajeros, puedes crear modos de fallo seguros que contengan el daño. Chiles llama a estas protecciones "crackstoppers". Si no diseñas tus modos de fallo, obtendrás los impredecibles —y normalmente peligrosos— que emerjan solos.

## Detener la propagación de la grieta (Stopping Crack Propagation)

En CF, la grieta pudo detenerse en muchos niveles:

- **Pool de conexiones**: estaba configurado para bloquear los hilos indefinidamente cuando no había recursos, atando todos los hilos de atención. Podría haberse configurado para crear más conexiones o para bloquear a los llamadores un tiempo limitado.
- **RMI/EJB**: CF exponía sus servicios como EJB sobre RMI, y las llamadas RMI por defecto nunca expiran, así que los llamadores se quedaban bloqueados esperando respuesta. Podrían haber fijado un timeout en los sockets RMI (por ejemplo, una socket factory que llame a `Socket.setSoTimeout()`), usar un servicio web basado en HTTP con timeout, o descartar los hilos bloqueados.
- **Particionado**: los servidores CF podrían haberse dividido en varios grupos de servicio, evitando que un problema tumbara a todos los usuarios de CF.
- **Arquitectura**: CF podría haberse construido con colas de mensajes petición/respuesta, donde el llamador asume que la respuesta puede no llegar; o con un tuple space donde se buscan vuelos. Cuanto más acoplada la arquitectura, más fácil se propaga el error; las arquitecturas poco acopladas actúan como amortiguadores.

## Cadena de fallo (Chain of Failure)

Bajo cada caída hay una cadena de eventos: un problema pequeño lleva a otro. Vista a posteriori parece inevitable, pero muy improbable si se calcula la probabilidad de cada evento por separado. El error está en suponer independencia: los eventos no son independientes, porque un fallo en una capa aumenta la probabilidad de fallos en otras (si la base de datos se vuelve lenta, los servidores de aplicación tienen más probabilidad de quedarse sin memoria). Terminología:

- **Fault (falla)**: condición que crea un estado interno incorrecto; puede venir de un bug latente que se dispara o de una condición no comprobada en un límite o interfaz externa.
- **Error**: comportamiento visiblemente incorrecto.
- **Failure (fallo)**: sistema que no responde.

Disparar una falla abre la grieta; las fallas se vuelven errores y los errores provocan fallos. En cada paso la grieta puede acelerar, frenar o detenerse. El acoplamiento fuerte acelera las grietas. Una forma de prepararse es mirar cada llamada externa, I/O y uso de recursos y preguntar: "¿de cuántas formas puede salir mal esto?" (no conectar, tardar diez minutos, desconectarse, no responder, 10.000 peticiones a la vez, disco lleno al registrar el error...). El enfoque exhaustivo por fuerza bruta solo es práctico para sistemas de misión crítica o rovers de Marte.

La comunidad está dividida: un bando busca sistemas tolerantes a fallos (capturar excepciones, revisar códigos de error, impedir que las fallas se vuelvan errores); el otro dice que es fútil y aboga por "let it crash" para reiniciar desde un estado bueno conocido. Ambos coinciden en dos cosas: las fallas siempre ocurrirán y hay que impedir que se conviertan en errores.

## Ideas clave

- El software empresarial debe ser cínico: espera fallos y se protege con barreras internas; la mala estabilidad cuesta ingresos y reputación, y la buena no cuesta más.
- Un sistema robusto deja que el usuario siga trabajando pese a impulsos, estreses y fallos de componentes; el estrés produce deformación que viaja a partes distantes.
- Los enemigos de la longevidad son las fugas de memoria y el crecimiento de datos; solo se cazan con pruebas de longevidad propias, ya que QA y las pruebas de carga no corren el tiempo suficiente.
- Todo sistema tiene modos de fallo; si no los diseñas (como zonas de deformación o "crackstoppers"), aparecen los peligrosos por sí solos.
- Las grietas se detienen en muchos niveles: timeouts en pools y en RMI, particionado en grupos de servicio y arquitecturas poco acopladas que amortiguan.
- La cadena de fallo encadena eventos no independientes: un fallo en una capa aumenta la probabilidad de otros; el acoplamiento fuerte acelera la propagación.
- Terminología precisa: fault → error → failure; disparar una falla abre la grieta que se propaga.
- Dos enfoques frente a las fallas —tolerancia a fallos vs. "let it crash"— coinciden en que las fallas son inevitables y en que hay que impedir que se vuelvan errores.
