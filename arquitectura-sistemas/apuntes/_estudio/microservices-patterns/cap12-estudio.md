# Deploying microservices (Desplegando microservicios) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son los cuatro patrones principales de despliegue de microservicios? / R: Paquete específico del lenguaje, servicio como VM, servicio como contenedor y despliegue serverless.

P: ¿En qué orden recomienda evaluar los patrones de despliegue? / R: Serverless, contenedores, máquinas virtuales y paquetes del lenguaje; se elige el más ligero que satisfaga los requisitos.

P: ¿Qué dos conceptos interrelacionados combina el despliegue? / R: El proceso (los pasos que ejecutan las personas para llevar el software a producción) y la arquitectura (la estructura del entorno donde corre).

P: ¿Cuáles son las cuatro capacidades clave de un entorno de producción? / R: Interfaz de gestión de servicios, gestión del runtime de servicios, monitorización y enrutado de peticiones.

P: ¿Cuáles son los inconvenientes del patrón de paquete específico del lenguaje? / R: No encapsula el stack tecnológico, no permite limitar recursos, falta de aislamiento entre instancias y dificultad para ubicar instancias automáticamente.

P: ¿Qué diferencia a un contenedor de una máquina virtual? / R: El contenedor es virtualización a nivel de SO (comparte el SO del host), más ligero: imágenes rápidas de construir, transferencia parcial por capas y arranque muy rápido sin boot del SO.

P: ¿Qué contiene un Dockerfile? / R: La imagen base, las instrucciones para instalar software y configurar el contenedor, y el comando a ejecutar al arrancar.

P: ¿Por qué `docker run` no es fiable para producción? / R: Corre en una sola máquina y no maneja caídas de la máquina; además los servicios dependen de otros, por lo que se necesita un orquestador como Kubernetes.

P: ¿Cuáles son las tres funciones principales de Kubernetes? / R: Gestión de recursos, scheduling (elección de máquina) y gestión de servicios (balanceo, rolling upgrades y rollback).

P: ¿Qué es un Pod en Kubernetes? / R: La unidad básica de despliegue: uno o más contenedores que comparten IP y volúmenes, efímero y que puede incluir sidecars.

P: ¿Para qué sirven el readinessProbe y el livenessProbe? / R: El readinessProbe determina si enrutar tráfico a una instancia; el livenessProbe determina si Kubernetes debe terminarla y reiniciarla.

P: ¿Qué diferencia hay entre despliegue y release? / R: El despliegue es correr la versión en producción; el release es hacerla disponible a los usuarios finales. Separarlos permite probar en producción antes de liberar.

P: ¿Qué es un service mesh y qué ejemplo usa el capítulo? / R: Una capa de red que media toda la comunicación entre servicios; el capítulo usa Istio.

P: ¿Qué dos objetos de Istio controlan el enrutado? / R: VirtualService (cómo enrutar peticiones por hostname) y DestinationRule (define subsets de pods, normalmente por versión).

P: ¿Cuáles son los inconvenientes del despliegue serverless con AWS Lambda? / R: Latencia de cola larga (crítica en Java, que tarda varios segundos en arrancar) y un modelo de programación limitado basado en eventos/peticiones, inadecuado para servicios de larga duración.

## Preguntas de autoevaluación

P: ¿Por qué las VM modernas se tratan como "ganado" y no como "mascotas"? / R: Porque son inmutables, ligeras, efímebles y automatizadas (desechables), frente a las máquinas físicas administradas individualmente; esto acompaña a la escala de decenas o cientos de servicios. (Sección: Lo que necesitas saber)

P: ¿Qué beneficios aporta empaquetar un servicio como imagen de VM? / R: Encapsula el stack tecnológico (caja negra desplegable en cualquier lugar), aísla instancias con CPU y memoria fijas, y aprovecha infraestructura cloud madura con balanceo y autoescalado. (Sección: Patrón: Servicio como máquina virtual)

P: ¿Cómo logra Kubernetes despliegues sin downtime? / R: Mediante rolling upgrade: crea pods de la nueva versión y termina los viejos solo cuando los reemplazos están listos (usando el readinessProbe), de modo que siempre hay pods disponibles. (Sección: Desplegar con Kubernetes)

P: ¿Cuál es el problema del rolling upgrade que motiva separar despliegue de release? / R: Asume que una versión que pasó pruebas en staging funcionará en producción, pero staging rara vez es un clon exacto y algunos bugs solo aparecen en producción, impactando a usuarios. (Sección: Separar despliegue de release con un service mesh)

P: ¿Cómo permite Istio liberar una versión de forma incremental? / R: Corriendo varias versiones a la vez y enrutando tráfico por reglas: todo a v1, luego peticiones de prueba a v2 (p. ej. por cabecera testuser) y después reparto por pesos incrementando hasta el 100%. (Sección: Separar despliegue de release con un service mesh)

P: ¿Qué hace que Restaurant Service encaje bien en AWS Lambda? / R: Tiene una API REST y no mantiene conexiones persistentes a Kafka; se compone de una función lambda por endpoint REST, empaquetadas en un ZIP, y el API Gateway enruta las peticiones HTTP a cada función. (Sección: Desplegar un servicio REST con AWS Lambda y API Gateway)

P: ¿Cuáles son las cuatro formas de invocar una función lambda? / R: Peticiones HTTP (vía AWS API Gateway), eventos de servicios AWS (S3, DynamoDB, Kinesis, SES), invocaciones programadas (estilo cron) y llamadas directas de web service (síncronas o asíncronas). (Sección: Patrón: Despliegue serverless)

## Puntos a dominar

- Identificar los cuatro patrones de despliegue y el orden de evaluación (serverless → contenedores → VM → paquete del lenguaje).
- Enumerar las cuatro capacidades de un entorno de producción y explicar cada una.
- Contrastar ventajas e inconvenientes de paquete del lenguaje, VM y contenedor.
- Explicar la arquitectura de Kubernetes (master/node) y sus objetos: Pod, Deployment, Service y ConfigMap/Secret.
- Distinguir los tipos de Service de Kubernetes: ClusterIP, NodePort y LoadBalancer.
- Explicar la diferencia entre readinessProbe y livenessProbe y el mecanismo de rolling upgrade y rollback.
- Explicar la diferencia entre despliegue y release y cómo un service mesh (Istio) la implementa con VirtualService y DestinationRule.
- Describir la arquitectura de Istio (control plane: Pilot y Mixer; data plane: proxies Envoy como sidecar).
- Enumerar beneficios e inconvenientes del serverless (AWS Lambda) y cuándo es adecuado.
