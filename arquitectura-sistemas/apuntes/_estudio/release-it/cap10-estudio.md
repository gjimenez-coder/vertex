# Control Plane (Plano de control) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la heurística para distinguir software de producción de control plane? / R: Si por el software pasan datos de usuario de producción, es software de producción; si su trabajo principal es gestionar otro software, es control plane.

P: ¿Qué coste conlleva cada pieza del control plane? / R: Cada pieza es opcional y supone un coste operativo permanente; es una compensación entre el coste fijo de personal dedicado y el coste variable de acelerar despliegues, recuperación y aprovisionamiento.

P: ¿Qué es la "ventaja mecánica" (mechanical advantage)? / R: El multiplicador del esfuerzo humano que dan las máquinas simples; alta palanca permite grandes cambios con poco esfuerzo, para bien o para mal.

P: ¿Por qué Nygard dice que la caída de S3 no fue "human error"? / R: Porque no fue el humano quien falló al sistema, sino el sistema quien falló al humano, amplificando un error menor (un parámetro mal escrito) hasta consecuencias enormes.

P: ¿Cómo funciona la automatización del control plane según la analogía de la robótica industrial? / R: Percibe el estado actual, lo compara con el deseado y efectúa cambios; no tiene juicio y, cuando se equivoca, lo hace muy rápido, dejando al humano en modo recuperación.

P: ¿Cuál es la regla para repartir trabajo entre humanos y automatización? / R: Usar la automatización para lo que los humanos hacen mal (tareas repetitivas, respuesta rápida) y los humanos para lo que la automatización hace mal (percibir la situación global).

P: ¿Qué debe ofrecer un equipo de plataforma? / R: La capacidad para que otros hagan el trabajo del dominio (interfaces/contratos que ocultan la implementación), no hacer el trabajo del dominio por ellos.

P: ¿Por qué "el desarrollo es producción"? / R: Porque los desarrolladores crean contenido continuamente usando servicios (control de versiones, CI, QA, repositorio de artefactos); si caen, no pueden trabajar, así que requieren SLA de nivel de producción.

P: ¿Qué dos preguntas fundamentales responde la transparencia de todo el sistema? / R: ¿Reciben los usuarios una buena experiencia? y ¿está el sistema creando el valor económico que queremos? La pregunta "¿está todo funcionando?" no está en la lista.

P: ¿Qué es real-user monitoring (RUM)? / R: Medir directamente la experiencia del usuario instrumentando apps web y móviles (p. ej. New Relic, Datadog, AppDynamics, CA APM u open source).

P: ¿Cuál es la diferencia entre colectores de logs push y pull? / R: En push la instancia empuja logs por red (típicamente syslog, útil con contenedores sin identidad ni almacenamiento local); en pull el colector central copia los logs de hosts conocidos.

P: ¿Cómo se define lo "nominal" para métricas continuas? / R: Como la media del periodo ± dos desviaciones estándar; el periodo más estable suele ser la "hora de la semana" (p. ej. martes 2 p.m.).

P: ¿Qué restricciones tienen los servicios de configuración como ZooKeeper y etcd? / R: Están sujetos al teorema CAP, son escalables pero no elásticos, sufren el mismo trauma de red que cualquier aplicación y cada escritura pasa por consenso.

P: ¿Qué son los canary deployments? / R: Dar el nuevo build a un pequeño conjunto de instancias que coexisten con las del build antiguo; si sus métricas van mal, no se despliega al resto.

P: ¿Cuál es la mejor interfaz para operación a largo plazo? / R: La línea de comandos; los GUI de administración demuestran bien pero son una pesadilla en producción por el clic y la dificultad de automatizar.

## Preguntas de autoevaluación

P: ¿Qué cuatro preguntas conviene hacerse tras un cambio exitoso para aprender también de los éxitos? / R: Quién lo ejecutó, si hubo un "second set of eyes", si el playbook se revisó (a veces se relajan los chequeos de error) y qué feedback dio el sistema. (Ventaja mecánica)

P: ¿Qué umbral de ejemplo propone el capítulo para que la automatización pause y pida confirmación humana? / R: Más allá de cierto umbral, como apagar más del 50 % de la capacidad, debería pausar para confirmación humana. (Ventaja mecánica)

P: ¿Cómo cambió el movimiento NoSQL el reparto de responsabilidades frente a RDBMS SQL? / R: Con NoSQL el administrador mantiene la base sana y con capacidad y el modelo de datos queda en la aplicación; con SQL un cambio de esquema puede dañar a otros, lo que suele llevar a una base física por servicio. (Plataforma y ecosistema)

P: ¿Cómo debe conectar la transparencia con el valor económico? / R: Debe revelar cómo el pasado reciente, el estado actual y el futuro conectan con los ingresos (top line: pasos del proceso de negocio y profundidad de colas) y los costes (bottom line: infraestructura, operaciones, plataformas y runtimes). (Transparencia de todo el sistema)

P: ¿Qué categorías de métricas conviene exponer, dado que no se puede predecir cuáles serán críticas? / R: Indicadores de tráfico, transacciones de negocio por tipo, usuarios, salud de resource pools, salud de conexiones de base de datos, consumo de datos, salud de integration points (circuit breaker, timeouts, errores) y salud de caché. (Logs y estadísticas)

P: ¿Qué pautas deben cumplir las instancias respecto a un servicio de configuración? / R: Deben poder arrancar sin él, no dejar de funcionar si la configuración es inalcanzable, impedir que un nodo particionado "apague el mundo" y replicar entre regiones geográficas. (Servicios de configuración)

P: ¿Cuándo es necesario el comando y control en vivo y cuándo basta matar la instancia? / R: El control en vivo solo hace falta si las instancias tardan en estar listas (JVM con warm-up, cachés grandes, VMs); si arrancan en milisegundos y toman configuración de un servicio, es más simple matarlas y dejar que el scheduler lance otra. (Comando y control)

P: ¿Qué controles conviene ofrecer y cuáles evitar? / R: Ofrecer resetear circuit breakers, ajustar pools, deshabilitar integraciones salientes, recargar configuración, empezar/parar de aceptar carga y feature toggles; evitar un botón de autodestrucción y abusar del "flush cache" (hunde el rendimiento y genera dogpile). (Comando y control)

## Puntos a dominar

- Clasificar correctamente software como producción o control plane usando la heurística del flujo de datos de usuario.
- Razonar la decisión de adoptar o no una pieza del control plane con una visión de coste/beneficio, recordando que todo lo que se construye hay que mantenerlo o desmontarlo.
- Tratar las caídas como fallo del sistema completo (software, control plane y procesos humanos), hacer postmortems también de los cambios exitosos y buscar "near misses".
- Diseñar la automatización con umbrales que pausen para confirmación humana y repartir tareas según la regla humano/automatización.
- Entender que el equipo de plataforma ofrece capacidades (contratos) y que el entorno de desarrollo exige SLA de producción.
- Explicar las dos preguntas de la transparencia y conectar la monitorización con top line y bottom line, adoptando RUM a fondo sin "dead zones".
- Conocer indexado de logs (Splunk; Elasticsearch/Logstash/Kibana), agregación temporal de métricas y la definición de lo "nominal".
- Distinguir push vs pull en logs y despliegue, el valor de un repositorio de artefactos con builds repetibles, los canary deployments y el riesgo del build server como vector de ataque.
- Recordar las restricciones CAP de ZooKeeper/etcd y las pautas de resiliencia de las instancias.
- Recorrer la "shopping list" del control plane y saber que empezar por la visibilidad es la prioridad, y que si se adopta una plataforma hay que abrazarla de verdad.
