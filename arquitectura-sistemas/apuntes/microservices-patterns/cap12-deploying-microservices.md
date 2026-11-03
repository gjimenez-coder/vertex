# Microservices Patterns: With Examples in Java — Chris Richardson (Manning Publications, 2019)
## Capítulo 12 — Deploying microservices (Desplegando microservicios)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF como `(PDF p. N)`.

## Lo que necesitas saber

El software no aporta valor hasta que corre en producción. Este capítulo describe cómo desplegar microservicios y presenta los cuatro patrones de despliegue principales: paquete específico del lenguaje, servicio como VM, servicio como contenedor y despliegue serverless. La tesis central es que debes elegir el patrón más ligero que satisfaga los requisitos del servicio, evaluando las opciones en este orden: serverless, contenedores, máquinas virtuales y paquetes del lenguaje.

El despliegue combina dos conceptos interrelacionados: el proceso (los pasos que ejecutan personas para llevar el software a producción) y la arquitectura (la estructura del entorno donde corre). Ambos han cambiado radicalmente: del paso manual de código a operaciones (DevOps y pipelines automatizados) y de máquinas físicas "mascota" a infraestructura ligera, efímera y automatizada. Las VM modernas son inmutables, tratadas como ganado desechable en vez de mascotas. Esta evolución coincide con la adopción de microservicios: una aplicación puede tener decenas o cientos de servicios, por lo que se necesita un proceso e infraestructura muy automatizados.

Sales sabiendo cómo funciona cada patrón con sus ventajas e inconvenientes, cómo desplegar con Kubernetes, cómo usar un service mesh (Istio) para separar despliegue de release, cómo desplegar con AWS Lambda, y cómo elegir entre ellos.

## El entorno de producción

Un entorno de producción debe implementar cuatro capacidades clave (PDF p. 416):

- Interfaz de gestión de servicios: permite crear, actualizar y configurar servicios; idealmente una API REST invocada por herramientas de línea de comandos y GUI.
- Gestión del runtime de servicios: asegura que el número deseado de instancias esté corriendo en todo momento; reinicia instancias caídas, incluso en otra máquina si una falla.
- Monitorización: da visibilidad de lo que hacen los servicios (logs y métricas) y genera alertas (observabilidad, capítulo 11).
- Enrutado de peticiones: dirige las peticiones de los usuarios hacia los servicios.

## Patrón: Formato de empaquetado específico del lenguaje

Lo que se despliega y gestiona es el servicio en su paquete específico del lenguaje: un JAR ejecutable o WAR en Java, un directorio de código y módulos en NodeJS, o un ejecutable del sistema operativo en GoLang. Para desplegar, primero instalas el runtime necesario (el JDK, y Tomcat si es un WAR), copias el paquete y arrancas el servicio. Cada instancia suele ser un único proceso (una JVM en Java), aunque algunos lenguajes permiten varias instancias por proceso. Puedes correr varias JVM en una máquina, o varias instancias en un mismo Tomcat (sin aislamiento entre ellas).

Beneficios: despliegue rápido (se copian pocos bytes y arrancar es rápido) y uso eficiente de recursos (las instancias comparten máquina y SO, más aún si comparten proceso).

Inconvenientes: falta de encapsulación del stack tecnológico (operaciones debe conocer versiones exactas de runtime), imposibilidad de limitar los recursos que consume una instancia (un proceso puede acaparar CPU o memoria), falta de aislamiento al correr varias instancias en una máquina, y dificultad para decidir automáticamente la ubicación de las instancias. Debe usarse rara vez, salvo cuando la eficiencia prima sobre todo lo demás.

## Patrón: Servicio como máquina virtual

Se empaqueta el servicio como una imagen de VM (por ejemplo una AMI de Amazon) que incluye código y todo el software necesario para ejecutarlo. Cada instancia es una VM (una instancia EC2) creada a partir de esa imagen, típicamente gestionada por un Auto Scaling group que mantiene el número deseado de instancias sanas. El pipeline de despliegue construye la imagen con un VM image builder; herramientas como Aminator (Netflix) o el más moderno Packer (soporta EC2, Digital Ocean, VirtualBox y VMware) lo facilitan. AWS Elastic Beanstalk es una forma sencilla de desplegar en VMs y combina elementos de los tres patrones.

Beneficios: la imagen encapsula el stack tecnológico (se convierte en una caja negra desplegable en cualquier lugar, y la API de despliegue pasa a ser la API de gestión de VMs), instancias aisladas con CPU y memoria fijas, y aprovechamiento de infraestructura cloud madura y automatizada (balanceo de carga, autoescalado).

Inconvenientes: uso menos eficiente de recursos (cada instancia carga un SO completo y los tamaños de VM son limitados, ineficiente para servicios ligeros de NodeJS o GoLang), despliegues relativamente lentos (construir e instanciar una imagen mueve muchos datos y el SO tarda en arrancar), y sobrecarga de administración del sistema (eres responsable de parchear SO y runtime).

## Patrón: Servicio como contenedor

Los contenedores son un mecanismo de virtualización a nivel de sistema operativo, más ligero que las VM. Un contenedor consiste en uno o varios procesos aislados en un sandbox, con su propia dirección IP (lo que evita conflictos de puertos: todos pueden escuchar en el 8080) y su propio sistema de ficheros raíz. El runtime de contenedores (Docker es el más popular, también existe Solaris Zones) aísla los contenedores usando mecanismos del SO, que se comparte entre todos. Al crear un contenedor puedes limitar su CPU y memoria; especificar estos recursos es importante con orquestadores como Kubernetes, que los usa para elegir la máquina donde ubicar el contenedor.

Para desplegar se empaqueta el servicio como una imagen de contenedor. El primer paso es crear un `Dockerfile`, que especifica la imagen base, instrucciones para instalar software y configurar el contenedor, y el comando a ejecutar al arrancar. Por ejemplo, la imagen de Restaurant Service parte de `openjdk:8u171-jre-alpine`, copia el JAR ejecutable y lo arranca con `java -jar`, y configura un `HEALTHCHECK` que invoca el endpoint de salud cada 5 segundos tras un retardo inicial de 30.

Construida la imagen con `docker build -t ftgo-restaurant-service .`, se sube a un registry (equivalente a un repositorio Maven o registry npm; Docker Hub es público, pero para aplicaciones propias conviene un registry privado). Se usan `docker tag` (prefijando hostname/puerto del registry y sufijando la versión) y `docker push`. La transferencia suele ser rápida gracias al sistema de ficheros por capas: SO, runtime Java y aplicación van en capas separadas y solo se transfieren las que faltan. Para ejecutar un contenedor se usa `docker run` (con argumentos como `-d`, `--name`, `-p 8082:8080` y variables de entorno `-e` para la configuración externalizada). Sin embargo, `docker run` no es fiable para producción porque corre en una sola máquina y no maneja caídas de la máquina; además los servicios dependen de otros (bases de datos, brokers). Docker Compose permite definir un conjunto de contenedores en YAML y arrancarlos como grupo, útil en desarrollo, pero se limita a una máquina. Para producción fiable hace falta un orquestador como Kubernetes.

Beneficios de los contenedores: heredan los de las VM (encapsulación del stack, aislamiento, recursos limitados) pero son ligeros (imágenes rápidas de construir, transferencia parcial por capas, arranque muy rápido sin proceso de boot del SO).

Inconvenientes: sigues siendo responsable del "trabajo pesado indiferenciado" de administrar las imágenes, parchear SO y runtime, y —salvo con soluciones gestionadas como Google Container Engine o AWS ECS— administrar la infraestructura de contenedores y las VM subyacentes.

## Desplegar con Kubernetes

Kubernetes es un framework de orquestación Docker: trata un conjunto de máquinas como un pool de recursos; le dices que corra N instancias y él se encarga del resto, manteniendo el número deseado de instancias sanas incluso ante caídas. Tiene tres funciones principales: gestión de recursos (CPU, memoria, volúmenes como una sola máquina), scheduling (elige la máquina considerando recursos requeridos y disponibles, con afinidad y anti-afinidad) y gestión de servicios (servicios con nombre y versión, balanceo de carga, rolling upgrades y rollback).

Arquitectura: corre sobre un clúster de máquinas que son master o node. El master gestiona el clúster y ejecuta API server (API REST usada por `kubectl`), Etcd (base NoSQL clave-valor con datos del clúster), Scheduler y Controller manager (ejecuta controladores que mantienen el estado deseado, como el replication controller). Cada node ejecuta Kubelet (crea y gestiona pods), Kube-proxy (red y balanceo entre pods) y los pods.

Conceptos clave (objetos): Pod (unidad básica de despliegue, uno o más contenedores que comparten IP y volúmenes, efímero, puede incluir sidecars), Deployment (especificación declarativa de un pod; controlador que asegura el número de instancias, con rolling upgrades y rollbacks; cada servicio es un Deployment), Service (da a los clientes una ubicación de red estable con IP y DNS que balancea tráfico entre pods; service discovery provisto por la infraestructura) y ConfigMap (configuración externalizada en pares nombre-valor; la variante Secret guarda información sensible como contraseñas).

Para desplegar Restaurant Service se escribe un YAML de Deployment (con número de réplicas, imagen, variables de entorno y referencias a Secret) que configura los health checks: el `readinessProbe` determina si enrutar tráfico a una instancia y el `livenessProbe` si Kubernetes debe terminarla y reiniciarla. Se aplica con `kubectl apply -f`. Para exponer los pods, que tienen IP dinámicas, se crea un Service de Kubernetes, cuyo `selector` elige los pods por etiqueta (`app: ftgo-restaurant-service`). El Service por defecto es ClusterIP (accesible solo dentro del clúster); para exponer al exterior, como el API Gateway, existen NodePort (puerto en todos los nodes, en el rango 30000–32767, al que luego puede apuntar un balanceador) y LoadBalancer (configura automáticamente un balanceador del cloud, por ejemplo un ELB en AWS, con menos control sobre su configuración).

Despliegues sin downtime: actualizar un servicio son tres pasos (construir y subir la nueva imagen con otra etiqueta de versión, editar el YAML del Deployment y aplicar `kubectl apply -f`). Kubernetes hace un rolling upgrade: crea pods de la nueva versión y termina los viejos solo cuando los reemplazos están listos (usando el `readinessProbe`), de modo que siempre hay pods disponibles. Si la nueva versión no arranca, puedes corregir el YAML o hacer rollback con `kubectl rollout undo deployment`, ya que el Deployment mantiene el historial de rollouts.

## Separar despliegue de release con un service mesh

El problema del rolling upgrade es que asume que si una versión pasó las pruebas en staging funcionará en producción, lo cual no siempre es cierto: staging rara vez es un clon exacto y algunos bugs solo aparecen en producción, impactando a usuarios. La solución es separar el despliegue (correr en producción) del release (hacerlo disponible a usuarios finales): despliegas la nueva versión sin enrutar peticiones, la pruebas en producción, la liberas a pocos usuarios y vas aumentando incrementalmente, revirtiendo si hay problemas.

Un service mesh —capa de red que media toda la comunicación entre servicios— facilita esto con balanceo y enrutado basado en reglas que permite correr varias versiones a la vez. El capítulo usa Istio, service mesh open source de Google, IBM y Lyft, con cuatro categorías de funciones: gestión de tráfico (descubrimiento, balanceo, reglas de enrutado, circuit breakers), seguridad (TLS entre servicios), telemetría (métricas y trazado distribuido) y aplicación de políticas (cuotas y límites de tasa).

Arquitectura de Istio: un control plane (cuyos componentes principales son Pilot, que extrae información de los servicios desplegados y configura los proxies, y Mixer, que recoge telemetría y aplica políticas) y un data plane formado por proxies Envoy, uno por instancia de servicio. Envoy se ejecuta como sidecar (patrón: implementar aspectos transversales en un proceso o contenedor junto a la instancia); en Kubernetes es un contenedor dentro del pod del servicio, inyectado manual (`istioctl kube-inject`) o automáticamente. Todo el tráfico fluye a través de Envoy.

Para desplegar con Istio defines Service y Deployment con requisitos: el puerto del Service debe seguir el convenio de nombres `<protocolo>[-<sufijo>]`, los pods deben tener etiqueta `app` (para trazado) y, para correr varias versiones, el nombre del Deployment y una etiqueta `version` deben incluir la versión. El enrutado se controla con dos objetos: `VirtualService` (cómo enrutar peticiones por hostname) y `DestinationRule` (define subsets de pods, normalmente por versión). Así puedes enrutar todo el tráfico a v1, desplegar v2 sin recibir tráfico, enrutar peticiones de prueba a v2 (por ejemplo con una cabecera `testuser`), y luego repartir producción por pesos (`weight: 95`/`weight: 5`) incrementando hasta el 100%.

## Patrón: Despliegue serverless

Los tres patrones anteriores comparten que debes preaprovisionar recursos (pagas por VMs o contenedores aunque estén ociosos) y que eres responsable de la administración del sistema. El serverless elimina ese "trabajo pesado indiferenciado". AWS Lambda, presentado en 2014, soporta Java, NodeJS, C#, GoLang y Python. Una función lambda es un servicio sin estado: empaquetas la aplicación en un ZIP o JAR, la subes y especificas la función que maneja cada petición (evento); AWS ejecuta automáticamente suficientes instancias y te factura por petición según tiempo y memoria consumidos. Otros clouds ofrecen alternativas (Google Cloud Functions, Azure Functions) y existen frameworks open source (Apache OpenWhisk, Fission), aunque el autor duda de su valor porque exigen gestionar la infraestructura, perdiendo el beneficio serverless.

Una lambda Java implementa la interfaz genérica `RequestHandler<I, O>` con el método `handleRequest()`. Hay cuatro formas de invocarla: peticiones HTTP (vía AWS API Gateway, que actúa de proxy HTTP), eventos de servicios AWS (objeto creado en S3, cambios en DynamoDB, mensajes de Kinesis, correos de SES), invocaciones programadas (estilo cron) y llamadas directas de web service (síncronas o asíncronas).

Beneficios: integración con muchos servicios AWS, eliminación de tareas de administración (no hay SO ni runtimes que parchear), elasticidad (corre tantas instancias como haga falta sin predecir capacidad) y precio por uso (solo pagas los recursos consumidos por petición). Inconvenientes: latencia de cola larga (provisionar y arrancar una instancia añade latencia, crítico en Java que tarda varios segundos en arrancar, poco apto para servicios sensibles a latencia) y modelo de programación limitado basado en eventos/peticiones (no sirve para servicios de larga duración, como consumir mensajes de un broker). Pese a ello, conviene evaluar primero si serverless cubre los requisitos antes de considerar alternativas.

## Desplegar un servicio REST con AWS Lambda y API Gateway

Restaurant Service, con API REST y sin conexiones persistentes a Kafka, encaja bien. El servicio se compone de varias funciones lambda, una por endpoint REST, empaquetadas juntas en un ZIP; el API Gateway enruta las peticiones HTTP a cada función. La arquitectura es similar a un servicio tradicional, salvo que los controladores Spring MVC se sustituyen por clases request handler; la lógica de negocio (`RestaurantService`, entidad JPA, repositorio) no cambia. `FindRestaurantRequestHandler` implementa `GET /restaurant/{restaurantId}` con `handleHttpRequest()`, que recibe un `APIGatewayProxyRequestEvent` y devuelve un `APIGatewayProxyResponseEvent` (similar a un servlet). Las superclases abstractas resuelven inyección de dependencias (`AbstractAutowiringHttpRequestHandler` crea el `ApplicationContext` de Spring Boot con `SpringApplication.run()` y autowirea antes de la primera petición) y manejo de errores (`AbstractHttpHandler` captura excepciones y devuelve un error 500). El servicio se empaqueta como ZIP con una tarea Gradle y se despliega con el framework open source Serverless: un fichero `serverless.yml` define las funciones y sus endpoints REST, y `serverless deploy` despliega las lambdas y configura el API Gateway.

## Ideas clave

- Elige el patrón de despliegue más ligero que cubra tus requisitos, evaluando en orden: serverless, contenedores, máquinas virtuales y paquetes del lenguaje.
- El patrón de paquete específico del lenguaje es rápido y eficiente, pero no encapsula el stack, no limita recursos ni aísla instancias; evítalo salvo con pocos servicios.
- Las VM encapsulan el stack y aíslan instancias aprovechando cloud maduro, a costa de más recursos, despliegues lentos y administración de SO.
- Los contenedores ofrecen los beneficios de las VM pero más ligeros (arranque rápido, imágenes por capas); conviene orquestarlos con Kubernetes, aunque sigues administrando SO, runtime y VMs.
- Kubernetes mantiene el número deseado de instancias sanas y permite rolling upgrades y rollbacks sin downtime mediante readinessProbe y livenessProbe.
- Un service mesh como Istio separa despliegue de release, enrutando tráfico por reglas (por versión, cabecera o peso) para liberar nuevas versiones de forma fiable.
- El serverless (AWS Lambda) elimina la administración del sistema y ofrece elasticidad y precio por uso, pero sufre latencia de cola larga y un modelo de programación basado en eventos.
