# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 20 — AI Security Engineering (Ingeniería de seguridad para IA)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber

El capítulo parte de una lección incómoda: los controles tradicionales pueden estar bien configurados y aun así fallar en el lugar donde vive la exposición real. El ejemplo de apertura lo resume: un pentester recuperó en menos de una hora fragmentos de datos de otro equipo desde una GPU compartida, pese a namespaces de Kubernetes, buckets separados, RBAC y cuotas. La tesis central es que la aislación de namespaces no se extiende a la memoria de la GPU, una frontera de service account no protege la caché de un modelo, y una network policy no impide cargar un artefacto inseguro.

La ingeniería de seguridad para IA es el trabajo de encontrar esas fronteras y hacerlas *enforceable* (exigibles). El recorrido va desde el hardware acelerador hasta Kubernetes, model serving, bases de datos vectoriales, pipelines MLOps, plataformas cloud de IA, secretos, observabilidad, red y supply chain. Los ajustes de cada vendor cambian; la habilidad durable es saber qué decisiones de ingeniería evitan que la infraestructura de IA se convierta en un *blast radius* amplio y silencioso.

Sales sabiendo cómo decidir qué cargas comparten hardware, cómo endurecer Kubernetes y el serving, cómo tratar vectores como datos sensibles, cómo producir evidencia de promoción en MLOps, cómo diseñar la autoridad de agentes y la revocación, y cómo convertir la observabilidad en una cadena de evidencia.

## El ejemplo que recorre el capítulo

El hilo conductor es la escena de apertura: una plataforma de ML "bien segmentada sobre el papel" (namespaces, buckets, RBAC, cuotas) donde un trabajo de prueba aterriza en una GPU compartida justo después del entrenamiento de otro equipo y recupera datos que "ya no deberían existir". El caso demuestra que el atacante no necesitó privilegios de admin, solo "un acelerador compartido y timing", y reaparece al justificar el clearing de memoria, el logging de co-residencia y la colocación por riesgo.

## GPU infrastructure security

Las GPU no son solo CPU más rápidas: su modelo de memoria, scheduling, drivers, interconexión y comportamiento multi-tenant crean propiedades de seguridad que la arquitectura habitual nunca inspecciona.

- Memoria: la memoria GPU puede persistir tras liberar una carga si la aplicación, runtime, driver o hardware no la limpia. No asumas que la GPU se zera como las páginas de CPU. Mitigación: limpiar buffers sensibles antes de liberarlos, usar runtimes de confianza y drivers parcheados, separar cargas no confiables de trabajos sensibles y preferir GPUs/nodos dedicados o particionado por hardware para trabajo de alto riesgo. Tratar pesos, activaciones, gradientes, prompts, embeddings y muestras de entrenamiento como sensibles mientras residen en la memoria del acelerador.
- Multi-tenancy: time-slicing, MPS, MIG, GPUs virtuales y nodos dedicados ofrecen distintos trade-offs entre utilización y aislamiento. MIG da particionado por hardware fuerte en GPUs NVIDIA compatibles, pero no es magia para toda amenaza. Los nodos dedicados siguen siendo la respuesta más limpia para datos regulados, tenants no confiables o entrenamientos muy sensibles.
- Side channels: timing de caché, comportamiento de potencia, patrones de acceso a memoria, contención de scheduling y acceso físico pueden convertirse en señales. No hace falta defender todo frente a ataques de laboratorio, pero sí saber qué cargas se verían dañadas.
- Diseño de clúster: separar tráfico de gestión, almacenamiento, training, inferencia e interconexión de aceleradores. Redes de alto ancho de banda como InfiniBand o NVLink no deben volverse puertas traseras entre zonas de confianza.
- Registro de decisión de aislamiento GPU: para plataformas sensibles, la colocación debe ser una decisión de seguridad registrada (clase de carga, confianza del tenant, sensibilidad, modo del acelerador, node pool, mecanismo de aislamiento, clearing, patch level, dueño de excepción). También registrar co-residencia para reconstruir qué jobs compartieron GPU, nodo, versión de driver y runtime. "La colocación sigue al riesgo, no a la presión de la cola."

No tratar los namespaces de Kubernetes como prueba de aislamiento de memoria GPU; parchear drivers y runtimes como infraestructura de producción.

## Container and Kubernetes security for ML workloads

Los ejemplos por defecto de Kubernetes buscan que una demo funcione, no proteger modelos, datasets, GPUs, secretos y tenants.

- Aislamiento de recursos: las cuotas deben basarse en métricas históricas, picos previstos y clases de carga documentadas. Namespaces sin límites convierten un error en DoS. Usar limit ranges, priority classes para proteger la inferencia de producción, y node affinity/anti-affinity.
- Network policies: la red por defecto permite comunicación amplia pod-a-pod. Empezar con *default-deny* en ingress y egress, y añadir allow-rules explícitas. El egress importa más de lo esperado: un contenedor de training comprometido puede exfiltrar datos o contactar C2. Canalizar dependencias por mirrors internos y registrar egress inesperado como evento de seguridad.
- Security contexts / Pod Security Standards: revisar los contenedores que piden root o privileged. Ejecutar como non-root, root filesystem de solo lectura, acceso a GPU vía device plugin en vez de contenedores privilegiados, y drop de capabilities. PSS/PSA reemplazan a PodSecurityPolicy, removida en Kubernetes 1.25: usar `restricted` en producción, `baseline` al migrar, `privileged` solo como excepción documentada.
- Secretos: los Kubernetes secrets no bastan por sí solos. Usar gestores externos (Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager) para rotación, auditoría y credenciales dinámicas. Usar tokens de service account proyectados con audiencia y expiración acotadas en lugar de tokens heredados sin expiración. "No crees tokens permanentes porque el modelo tardó más de lo esperado en entrenar" (PDF p. 434).
- Admission y evidencia de runtime: exigir labels (owner, model, data class, environment, workload type), rechazar registries no confiables y pedir requests/limits. La evidencia de runtime debe probar que la regla de admission sigue cumpliéndose tras desplegar (un sidecar, init container o patch de debug puede volver riesgosa una YAML limpia). Mantener notebooks separados: "Un namespace de notebook con egress amplio, tokens persistentes, buckets de producción montados y acceso privilegiado a GPU no es un sandbox. Es un puente a producción con una UI más amigable" (PDF p. 435).

## Model serving and registry security

El serving convierte artefactos entrenados en comportamiento de producción alcanzable, lo que lo hace blanco de alto valor.

- Inference endpoints: la autenticación debe basarse en la clasificación de riesgo del modelo y la ubicación del consumidor (mTLS/identidad de servicio para interno; identidad fuerte, rate limiting, validación y monitoreo de abuso para cliente externo; política aún más estricta para endpoints que sirven a agentes). La autorización liga al llamador con modelo, operación, tenant y alcance de datos. Rate limits y cuotas son controles de seguridad porque reducen extracción y scraping.
- Model registry: es la puerta de promoción entre experimentación y producción. Debe registrar origen, hashes, firmas, model card, decisión de licencia, scan de seguridad, validación, owner, fecha de aprobación, entorno y path de rollback. El serving solo carga artefactos aprobados. Separar permisos: publish, approve, read, deploy, revoke.
- Hardening del framework: tratar Triton, TensorFlow Serving, TorchServe (en mantenimiento limitado) y KServe como software de producción alcanzable desde internet. Parchear, deshabilitar protocolos/admin innecesarios, restringir exposición y seguir boletines de seguridad (NVIDIA sigue publicando boletines de Triton).
- Model loading gate: la última oportunidad de detener un artefacto inseguro. El proceso no debe cargar un modelo solo porque exista un path: verifica registro, hash, firma/aprobación, formato, resultado del scanner, runtime permitido y entorno. Mantener la caché "aburrida": escribible solo por la identidad del serving y con eviction al revocar. Para herramientas de agentes, separar la generación de salida del modelo de la política de ejecución: el endpoint propone, la aplicación valida, autoriza y aprueba.

## Vector database and retrieval security

"Los embeddings no son matemática inofensiva": pueden codificar información sensible sobre documentos, usuarios, clientes, decisiones y operaciones internas. Tratar las bases vectoriales como data stores sensibles, no cachés.

- Control de acceso: el patrón más fuerte es autorización *server-side* antes de la recuperación, derivando tenant y usuario del contexto autenticado. Un filtro de metadatos provisto por el cliente no es una frontera de seguridad. Separar colecciones, namespaces, índices y claves por sensibilidad; registrar queries, conteos, document IDs, identidad del llamador y decisiones de política.
- Cifrado, retención y monitoreo: cifrar en reposo y en tránsito, controlar quién exporta embeddings o reconstruye índices, definir retención, borrar embeddings cuando se borra el documento origen o termina la relación con el tenant, y monitorear volumen inusual, recuperación amplia y sondeo repetido de vecinos cercanos.
- Abuso: el fallo obvio es la fuga cross-tenant; el sutil es el *authority laundering* —la app recupera contenido sensible correctamente y lo pasa a un modelo o agente para un fin que la autorización original no permitía. La autorización de recuperación debe considerar el propósito, no solo la identidad: recuperar y actuar necesitan compuertas separadas.

## MLOps pipeline security

Los pipelines mueven datos por ingesta, preprocesamiento, training, evaluación, aprobación, despliegue y monitoreo; cada etapa es atacable sin tocar el endpoint de producción.

- Control de training y artefactos: los datos de training necesitan procedencia, checks de integridad, owner, etiqueta de sensibilidad y versión. Firmar un artefacto solo es útil si la firma sigue a la validación: se firma porque origen, formato, hash, scanner, licencia y checks de comportamiento cumplen los criterios de promoción, no porque exista.
- Supply chain (software, modelo, infraestructura): los sistemas de IA dependen de paquetes Python, librerías CUDA, imágenes de contenedor, notebooks, model files, tokenizers, prompt templates, clientes de vector DB y servicios cloud. Mantener SBOMs, usar mirrors internos, escanear y seguir advisories. Atención a los formatos de modelo: los artefactos basados en pickle pueden ejecutar código al cargarse; usar escaneo como ModelScan y preferir formatos como safetensors, recordando que una serialización más segura no prueba que el comportamiento del modelo sea seguro.
- Evidencia de promoción: el training run debe apuntar a versiones de datos, código, imágenes de entorno, manifiestos de dependencias, resultados de evaluación, checks de seguridad, registros de aprobación y hashes finales. "Si no puedes responder esas preguntas para un modelo en producción, el modelo no está gobernado. Simplemente está corriendo" (PDF p. 441). La revocación debe ser una operación del pipeline, no una búsqueda manual en nodos de serving.

## Cloud AI platform and secrets security

Las plataformas gestionadas (SageMaker, Vertex AI, Azure ML y servicios más nuevos de agentes/IA) reducen carga operativa pero no eliminan la responsabilidad del cliente: hay que configurar IAM, red, cifrado, logging, residencia de datos y acceso a modelos.

- Responsabilidad compartida e identidad: conocer qué lado de la línea te corresponde, configurarlo deliberadamente y registrar evidencia. La identidad es donde suele fallar: training jobs, notebooks, endpoints, pipelines, vector stores y agentes no deben compartir un service account amplio. Usar identidades de workload separadas con el menor alcance práctico.
- Red y datos: mantener cargas sensibles en paths de red privada (private endpoints, service perimeters, security groups, controles de egress). Endpoints públicos necesitan API gateways, WAF, autenticación, rate limits y monitoreo. Cifrado como base, con claves gestionadas por el cliente cuando riesgo/contrato/regulación lo exijan, protegiendo también el control plane de esas claves.
- Ingeniería de autoridad de agentes: existen dos modelos de identidad que no deben confundirse. Un agente de *permiso delegado* actúa con la autoridad de un usuario humano (sesión de navegador, token de repositorio, shell local, cuenta SaaS); necesita sesiones acotadas, aprobaciones visibles, allowlists de herramientas, validación de parámetros y expiración. Un agente de *identidad no humana* actúa como su propio workload o service principal; necesita owner, propósito, binding de entorno, credenciales de vida corta, rotación, roles de menor privilegio, puntos de enforcement, audit logs y kill switch. "Un token 'ai-agent-prod' de larga vida con acceso amplio no es una estrategia de identidad. Es un futuro informe de incidente" (PDF p. 442).
- Política antes de ejecutar la herramienta: el modelo no debe ser la autoridad de política de sus propias tool calls. El modelo propone, el motor de política evalúa antes de ejecutar (viendo identidad del agente, identidad del usuario delegado, nombre de la herramienta, operación, objeto destino, parámetros generados, sensibilidad, estado de aprobación y versión de política). Exigir aprobación para acciones irreversibles (deploy, delete, cambios de permisos, envíos externos, acceso a secretos).
- Fronteras de service account y revocación: usar identidades por entorno (dev/staging/prod no comparten service account). Probar ambos paths de revocación: es común revocar el token obvio y dejar viva otra vía (credencial de metadata de un job cloud, sesión SaaS en un perfil de navegador, acceso de instalación de una app de repo, certificado de service mesh). El drill debe probar que el agente ya no puede actuar.

## Observability and network architecture

La observabilidad para IA no es solo telemetría de uptime: es evidencia. Hay que saber quién llamó a qué modelo, qué contexto de recuperación se usó, qué tool action corrió, qué credencial y qué política lo permitieron, cuánto costó y si el comportamiento cambió.

- OpenTelemetry: las convenciones GenAI y de observabilidad de agentes empujan hacia atributos de traza comunes (model calls, tool calls, prompts, respuestas, costos, errores). Son estándares en evolución: estandariza tu propio schema ahora y mantenlo cerca de OpenTelemetry para migrar luego. No registrar prompts/outputs sensibles en crudo por defecto: redactar, tokenizar, hashear, muestrear o guardar tras acceso más estricto.
- Señales de seguridad: consumo inusual de tokens, cambios de latencia, denegaciones repetidas de política, recuperación amplia, loops de alto costo, cache misses, egress inesperado, cambios de acceso al registry, fallos de autenticación y tool calls fuera de la tarea declarada. "No son solo métricas operativas. Son leads de seguridad" (PDF p. 444).
- Segmentación de red: separar training, inferencia, procesamiento de datos, gestión, observabilidad y acceso externo. Ingress: endpoints públicos con API gateway, identidad, rate limits, validación y WAF; APIs de gestión por conectividad privada o bastión; training suele no necesitar inbound. Egress: training solo a fuentes/registries/mirrors aprobados; inferencia solo a telemetría/dependencias aprobadas; agentes solo a herramientas en alcance. El egress inesperado es una de las señales más claras.
- Service mesh y evidencia: el mesh aporta mTLS, política de tráfico, routing por identidad y telemetría, pero no reemplaza la autorización de aplicación ni la política de herramientas. El registro de auditoría debe leerse como una *cadena*: identidad → request → contexto recuperado → paso del modelo/agente → propuesta de herramienta → decisión de política → credencial usada → objeto destino → resultado → respuesta. Separar metadata de payloads para no convertir la observabilidad en una nueva superficie de brecha. Un loop de prompt injection puede aparecer primero como tool calls repetidas, picos de tokens o checks de política fallidos; la extracción de comportamiento como consultas de alto volumen y baja varianza.

## Ideas clave

- La aislación de namespaces de Kubernetes no cubre la memoria de la GPU: limpiar buffers, parchear drivers y hacer de la colocación GPU una decisión de seguridad registrada con evidencia de co-residencia.
- En Kubernetes para ML: default-deny en red, pods non-root/restricted, cuotas defendibles, secretos en gestores externos con tokens de vida corta, y evidencia de runtime que confirme las reglas de admission.
- El model registry es la puerta de promoción; el serving solo carga artefactos aprobados verificando registro, hash, firma, formato, scanner y revocación en el *model loading gate*.
- Las bases vectoriales son datos sensibles: autorización server-side antes de recuperar, considerando el propósito para evitar *authority laundering*.
- MLOps seguro produce evidencia encadenada (datos, código, entorno, scans, aprobaciones, hashes); sin ella un modelo "no está gobernado, solo está corriendo".
- Distinguir agentes de permiso delegado de identidades no humanas: fallan y se revocan distinto; probar ambos paths de revocación.
- La política de ejecución de herramientas vive antes de la acción: el modelo propone, el motor de política autoriza; exigir aprobación para acciones irreversibles.
- La observabilidad es una cadena de evidencia; tratar anomalías de costo, egress inesperado y denegaciones de política como señales de seguridad, protegiendo los payloads sensibles con acceso y retención separados.
