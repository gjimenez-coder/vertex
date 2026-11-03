# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 13 — Securing AI Infrastructure, MLOps, and Runtime Environments (Asegurando la infraestructura de IA, MLOps y los entornos de ejecución)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
El capítulo parte de una premisa directa: las cargas de trabajo de IA heredan el riesgo normal de la nube y además añaden cómputo caro, trabajos de larga duración, datasets mutables, model artifacts, retrieval stores y comportamiento sensible a políticas en runtime. Un solo bucket público, un service role demasiado amplio, un artefacto sin firmar o un gateway permisivo pueden echar a perder meses de trabajo sobre el modelo.

La tesis central es que la seguridad de infraestructura decide hasta dónde se propaga una brecha. Una prompt injection es mala; una prompt injection con acceso a datos de entrenamiento, artefactos, credenciales de despliegue o clústeres de GPU es otra clase de incidente. El red teaming muestra dónde se rompen los sistemas desplegados; la infraestructura decide el alcance del daño.

No vale memorizar nombres de productos cloud, porque cambian demasiado rápido. Lo que perdura es entender los puntos de control que impiden que un error se convierta en una brecha: almacenamiento, fronteras de red, gates de pipeline, integridad de artefactos, aislamiento y aplicación de políticas en runtime.

Sales sabiendo por qué la infraestructura de IA difiere, cómo segmentar entrenamiento/inferencia/datos/gestión, cómo asegurar el pipeline de MLOps, cómo endurecer contenedores y orquestación, cómo usar IaC/GitOps con valores seguros por defecto, cómo firmar y verificar artefactos, cómo elegir aislamiento según el riesgo, y cómo poner la política de ejecución en el camino del request.

## Por qué la infraestructura de IA difiere
La infraestructura tradicional asume peticiones cortas, tráfico predecible, servicios parcheables y flujos operados por humanos. La IA viola esas suposiciones: los trabajos de entrenamiento pueden durar días o semanas, las instancias GPU son lo bastante caras como para atraer cryptomining y robo de recursos, los datos y artefactos se vuelven las "joyas de la corona", y los endpoints de inferencia aceptan lenguaje no confiable, archivos y contexto de retrieval en alto volumen.

La consecuencia práctica es gestión de cambios más lenta y deliberada en unos sistemas y respuesta de políticas más rápida en otros. Puede que no reinicies un entrenamiento cada vez que llega una actualización de driver, pero puedes "isolate that job, pin the image, log every storage access, and prevent it from reaching the internet" (PDF p. 303).

La IA también cambia el *blast radius*: un servidor web comprometido expone una aplicación; un entorno de entrenamiento comprometido puede envenenar un modelo, filtrar datos, robar cómputo o publicar un artefacto contaminado que luego parece legítimo. El control de infraestructura es la diferencia entre un error local y un fallo de cadena de suministro.

## Fundamentos de seguridad en la nube para IA
Empieza con lo básico de cualquier despliegue serio: almacenamiento privado, identidades de mínimo privilegio, redes segmentadas, baselines seguros, logging y recuperación probada. Lo que cambia es el peso de cada control.

Segmentación y almacenamiento: separar las rutas de acceso público, inferencia, entrenamiento, datos y gestión. Los nodos de entrenamiento no deberían alcanzar Internet casualmente; la inferencia no debería leer datos crudos de entrenamiento; los almacenes de datos exponen solo las operaciones que cada etapa necesita. El tráfico público termina en gateways controlados, el acceso de gestión pasa por rutas de administración endurecidas en lugar de laptops de desarrolladores tocando directamente sistemas sensibles.

Los buckets de datos de entrenamiento deben ser privados por defecto, cifrados, versionados y con logging; el acceso público de lectura se bloquea a nivel de cuenta u organización donde la plataforma lo permita. El versionado ayuda a investigar poisoning, corrupción y borrados accidentales; los access logs importan porque la exfiltración a menudo parece una lectura normal hasta que el volumen, timing o identidad cuentan otra historia.

Fronteras entrenamiento/inferencia: no tratarlas como un entorno plano. El entrenamiento necesita datos, artifact stores y cómputo de alto rendimiento; la inferencia necesita baja latencia hacia artefactos validados y servicios de política. Las vector databases añaden otro matiz: los embeddings de retrieval pueden exponer datos sensibles, romper fronteras de tenant o volverse una vía de poisoning si no se controlan ingesta y query (cifrado, red privada, autenticación, query logging, aislamiento por tenant). En los interconnects de entrenamiento de alta velocidad no siempre se puede hacer deep packet inspection sin destruir el rendimiento; se compensa con mayor aislamiento, participantes conocidos, colocación restringida de jobs, protecciones físicas/de fabric y monitoreo de patrones de tráfico anómalos.

## Seguridad del pipeline de MLOps
La seguridad de MLOps es seguridad de pipeline. La pregunta defensiva va más allá de si el model server está endurecido: ¿puede entrar data no confiable?, ¿puede un job correr desde una imagen sin firmar?, ¿puede un modelo saltarse la evaluación?, ¿puede reemplazarse un artefacto en el registry?, ¿puede ocurrir un despliegue sin aprobación ni evidencia?

El pipeline se comprime en seis etapas, cada una un punto de control: data preparation, training, evaluation, model registry, deployment y monitoring.

- Data preparation: autentica fuentes, valida esquemas, detecta datos sensibles, escanea contenido y registra lineage. Las reglas YARA (originalmente para identificación de malware) pueden marcar scripts sospechosos, payloads codificados o texto tipo instrucción antes de que entre a un dataset.
- Training: jobs aislados con imágenes *pinned*, límites de recursos explícitos y acceso de red restringido. Un contenedor de entrenamiento no debería descargar paquetes arbitrarios en runtime; las dependencias van en una imagen revisada o repositorio interno.
- Evaluation: gates que atrapan modelos que fallan umbrales de seguridad, calidad, rendimiento, sesgo o compliance antes de producción.
- Model registry: registra qué modelo pasó qué gates, con firmas y metadatos que atan el artefacto a su training run y ruta de aprobación.
- Deployment: despliegue gradual con estrategias canary, blue-green o shadow.
- Monitoring: señales de infraestructura más distribución de inputs, comportamiento de outputs, model drift, patrones de coste inusuales, tasa de bloqueo de políticas y triggers de reentrenamiento.

El patrón importante: "no bypass and no backward flow" (PDF p. 306). Un modelo no pasa de entrenamiento a producción por prisa, y un incidente de producción no empuja datos sin revisar de vuelta al entrenamiento. Cada handoff deja evidencia: qué cambió, quién aprobó, qué checks pasaron y qué rollback existe.

## Endurecimiento de contenedores y orquestación
Casi todas las cargas de IA terminan en contenedores u orquestación. Aplica seguridad de contenedores ordinaria: imágenes base mínimas, dependencias *pinned*, ejecución non-root, filesystems de solo lectura donde sea práctico, escaneo de imágenes, firma y admission controls.

Kubernetes añade su propio control plane:
- RBAC con el mínimo de permisos que la carga necesita.
- Pod Security Standards para impedir contenedores privilegiados y defaults inseguros.
- Network policies que restringen tráfico pod-a-pod y pod-a-servicio.
- Admission controllers que bloquean imágenes no confiables, falta de límites de recursos o cargas que piden acceso GPU sin aprobación.

## Infrastructure as code para IA
IaC es donde muchos controles se vuelven exigibles. Una regla de bucket seguro es útil en un documento de política, pero mucho más útil cuando el manifiesto de Terraform, CloudFormation, Pulumi o Kubernetes falla un pull request si el bucket es público, sin cifrar o sin logging.

La *policy as code* valida las definiciones antes del despliegue: regiones GPU aprobadas, almacenamiento privado, segmentación de red, acceso a registry, labels requeridas, referencias a secretos y ajustes de admission control. La evaluación de política vive en la ruta de despliegue, no se añade después de que ocurre el drift.

GitOps hace auditable el estado deseado: el repositorio es el registro de lo que debe existir y el loop de reconciliación detecta o revierte el drift. Herramientas como Checkov escanean definiciones antes del merge y los policy engines rechazan definiciones inseguras antes de llegar al clúster.

Secretos, escaneo y drift: los secretos no van en definiciones IaC, imágenes, notebooks ni scripts de entrenamiento. La capa IaC referencia secret stores aprobados e identidades gestionadas en lugar de embeber credenciales. El escaneo revisa antes del merge; la detección de drift verifica si el entorno desplegado aún coincide con el estado revisado.

## Seguridad del ciclo de vida de los model artifacts
Los model artifacts son objetos de cadena de suministro de alto valor. Un model file, adapter, tokenizer, archivo de configuración o imagen de contenedor puede llevar comportamiento a producción. Tratarlos como archivos informales es cómo la manipulación se vuelve invisible.

Un ciclo de vida seguro: firma los artefactos, verifica firmas en el despliegue, registra provenance, guarda metadatos, genera evidencia SBOM / AI SBOM / model bill-of-materials donde sea útil, loguea transferencias y define reglas de retención y disposición. Sigstore, el trabajo de model-signing de OpenSSF y la guía de AI SBOM de CISA/G7 son ejemplos del movimiento hacia mayor integridad de artefactos en ML.

El hábito clave es *provenance*: un modelo de producción debe rastrearse a un training run, una versión de dataset, un resultado de evaluación, una aprobación y un artefacto firmado. Si esa cadena se rompe, el despliegue debe fallar cerrado (*fail closed*) o requerir manejo break-glass explícito. La retención y disposición también importan: modelos, datasets y adapters viejos no son inofensivos por no estar desplegados; pueden contener datos regulados, comportamiento propietario o dependencias vulnerables.

## Técnicas de sandboxing y aislamiento
El aislamiento limita el daño cuando la prevención falla. Los niveles se eligen según sensibilidad de datos, fronteras de tenant, acceso a herramientas y necesidades de rendimiento:

- Aislamiento físico: la frontera más fuerte, pero caro y lento.
- VMs y entornos de confidential computing: separación más fuerte que los contenedores.
- Contenedores: rápidos y convenientes, pero comparten kernel.
- MicroVMs y WebAssembly: fronteras de ejecución más estrechas para inferencias específicas.

No elijas el control "más fuerte" aislado; elige la frontera que coincide con el riesgo. Un chatbot público de baja sensibilidad puede necesitar aislamiento de contenedor más enforcement de política; un modelo regulado con datos protegidos puede necesitar tenants separados, claves dedicadas, rutas de red más estrictas y aislamiento de carga más fuerte.

El GPU sharing merece cautela especial: Multi-Instance GPU y tecnologías relacionadas mejoran la utilización pero no resuelven automáticamente toda frontera de tenant; tratarlo como decisión de riesgo con documentación del proveedor, clasificación de cargas y monitoreo, no como optimización rutinaria de coste. El aislamiento de tenant va más allá del cómputo: las rutas de datos pueden requerir bases de datos, esquemas, índices, claves, logs, colas o retrieval stores separados.

## Aplicación de políticas en runtime
Es la última capa de control antes de que el sistema de IA actúe. La infraestructura hace el entorno más seguro; los controles de runtime deciden si un request, tool call, ruta de retrieval, output o acceso a modelo debe permitirse *ahora*.

- Política de gateway: autenticación, rate limits, fronteras de tenant, tamaño de input y validación de request.
- Política de model-server: qué modelo puede usar un caller, si un tool call está permitido, si enrutar a un fallback más seguro.
- Política de output: redactar datos sensibles, bloquear categorías inseguras o exigir citas antes de responder.

Estos checks se refuerzan entre sí y los audit logs atan las decisiones a caller, tenant, modelo, versión de política y hora. Open Policy Agent (OPA) permite expresar política separada del código de aplicación y evaluarla en request time o admission time; Gatekeeper aplica esa idea al admission control de Kubernetes. La clave: la política debe poder cambiarse sin un redeploy completo, para apretar o relajar controles con evidencia en lugar de hornear cada decisión en el código de serving.

## Ideas clave
- La seguridad de infraestructura de IA es seguridad tradicional bajo más presión: aceleradores caros, jobs largos, datasets sensibles, artefactos, retrieval stores y decisiones de política en runtime.
- Segmenta las rutas de entrenamiento, inferencia, datos y gestión; la inferencia no debe leer datos crudos de entrenamiento ni el entrenamiento alcanzar Internet casualmente.
- La seguridad de MLOps es seguridad de pipeline: cada una de las seis etapas es un punto de control, con regla de "no bypass, no backward flow".
- Endurece contenedores y Kubernetes: RBAC mínimo, Pod Security Standards, network policies y admission controllers (incluido acceso GPU aprobado).
- IaC y GitOps hacen exigibles y auditables los valores seguros por defecto; Checkov y policy as code rechazan definiciones inseguras antes del merge/clúster.
- Firma y verifica los model artifacts; mantén provenance completo (training run, dataset, evaluación, aprobación, firma) y falla cerrado si la cadena se rompe.
- Elige el aislamiento según el riesgo (físico, VM/confidential computing, contenedor, microVM/Wasm); trata el GPU sharing como decisión de riesgo.
- Pon la aplicación de políticas en el runtime (gateway, model-server, output) con OPA/Gatekeeper y política cambiable sin redeploy.
