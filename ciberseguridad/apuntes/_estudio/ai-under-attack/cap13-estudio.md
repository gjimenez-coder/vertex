# Securing AI Infrastructure, MLOps, and Runtime Environments — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre seguridad de infraestructura de IA?
R: La seguridad de infraestructura decide hasta dónde se propaga una brecha: una prompt injection con acceso a datos, artefactos, credenciales o clústeres de GPU es otra clase de incidente. El red teaming muestra dónde se rompen los sistemas; la infraestructura decide el alcance del daño.

P: ¿Por qué la infraestructura de IA difiere de la tradicional?
R: La IA viola las suposiciones tradicionales: los trabajos de entrenamiento duran días o semanas, las instancias GPU son caras y atraen cryptomining y robo de recursos, datos y artefactos son las "joyas de la corona", y los endpoints de inferencia aceptan lenguaje no confiable, archivos y contexto de retrieval en alto volumen.

P: ¿Qué es el blast radius en el contexto de IA?
R: Un servidor web comprometido expone una aplicación; un entorno de entrenamiento comprometido puede envenenar un modelo, filtrar datos, robar cómputo o publicar un artefacto contaminado. El control de infraestructura es la diferencia entre un error local y un fallo de cadena de suministro.

P: ¿Cómo deben configurarse los buckets de datos de entrenamiento?
R: Privados por defecto, cifrados, versionados y con logging; el acceso público de lectura se bloquea a nivel de cuenta u organización. El versionado ayuda a investigar poisoning, corrupción y borrados; los access logs detectan exfiltración que parece una lectura normal.

P: ¿Qué rutas deben segmentarse en la infraestructura de IA?
R: Las rutas de acceso público, inferencia, entrenamiento, datos y gestión. La inferencia no debe leer datos crudos de entrenamiento, el entrenamiento no debe alcanzar Internet casualmente, y el acceso de gestión pasa por rutas de administración endurecidas.

P: ¿Qué riesgos añaden las vector databases y cómo se controlan?
R: Los embeddings de retrieval pueden exponer datos sensibles, romper fronteras de tenant o ser vía de poisoning. Se controlan con cifrado, red privada, autenticación, query logging y aislamiento por tenant sobre ingesta y query.

P: ¿Cuáles son las seis etapas del pipeline de MLOps como puntos de control?
R: Data preparation, training, evaluation, model registry, deployment y monitoring.

P: ¿Qué significa el patrón "no bypass and no backward flow"?
R: Un modelo no pasa de entrenamiento a producción por prisa (no bypass) y un incidente de producción no empuja datos sin revisar de vuelta al entrenamiento (no backward flow). Cada handoff deja evidencia: qué cambió, quién aprobó, qué checks pasaron y qué rollback existe.

P: ¿Qué controles añade Kubernetes al endurecimiento de contenedores?
R: RBAC con el mínimo de permisos, Pod Security Standards contra contenedores privilegiados, network policies que restringen tráfico pod-a-pod y pod-a-servicio, y admission controllers que bloquean imágenes no confiables o acceso GPU sin aprobación.

P: ¿Qué hace la policy as code en IaC?
R: Valida las definiciones antes del despliegue (regiones GPU aprobadas, almacenamiento privado, segmentación de red, acceso a registry, labels, referencias a secretos, admission control). La evaluación vive en la ruta de despliegue, no se añade tras el drift.

P: ¿Qué rol cumple GitOps en la seguridad de infraestructura?
R: Hace auditable el estado deseado: el repositorio es el registro de lo que debe existir y el loop de reconciliación detecta o revierte el drift. Herramientas como Checkov escanean definiciones antes del merge.

P: ¿Qué es provenance y por qué es el hábito clave de los model artifacts?
R: Un modelo de producción debe rastrearse a un training run, versión de dataset, resultado de evaluación, aprobación y artefacto firmado. Si esa cadena se rompe, el despliegue debe fallar cerrado (fail closed) o requerir manejo break-glass explícito.

P: ¿Qué niveles de aislamiento se mencionan, de mayor a menor separación?
R: Aislamiento físico (el más fuerte pero caro y lento), VMs y confidential computing, contenedores (rápidos pero comparten kernel), y microVMs y WebAssembly (fronteras de ejecución más estrechas).

P: ¿Por qué el GPU sharing merece cautela especial?
R: Multi-Instance GPU y tecnologías relacionadas mejoran la utilización pero no resuelven automáticamente toda frontera de tenant; debe tratarse como decisión de riesgo con documentación del proveedor, clasificación de cargas y monitoreo, no como optimización rutinaria de coste.

P: ¿Cuáles son las tres capas de aplicación de políticas en runtime?
R: Política de gateway (autenticación, rate limits, fronteras de tenant, validación de request), política de model-server (qué modelo puede usar un caller, si un tool call está permitido, fallback) y política de output (redactar datos sensibles, bloquear categorías inseguras, exigir citas).

## Preguntas de autoevaluación

P: ¿Por qué el capítulo recomienda no memorizar nombres de productos cloud y qué propone entender en su lugar?
R: Porque cambian demasiado rápido. Lo que perdura es entender los puntos de control: almacenamiento, fronteras de red, gates de pipeline, integridad de artefactos, aislamiento y aplicación de políticas en runtime. (Sección "Lo que necesitas saber")

P: ¿Qué preguntas defensivas definen la seguridad del pipeline de MLOps más allá de endurecer el model server?
R: ¿Puede entrar data no confiable?, ¿puede un job correr desde una imagen sin firmar?, ¿puede un modelo saltarse la evaluación?, ¿puede reemplazarse un artefacto en el registry?, ¿puede ocurrir un despliegue sin aprobación ni evidencia? (Sección "Seguridad del pipeline de MLOps")

P: ¿Para qué sirven las reglas YARA en la etapa de data preparation?
R: Aunque son originalmente para identificación de malware, pueden marcar scripts sospechosos, payloads codificados o texto tipo instrucción antes de que entren a un dataset. (Sección "Seguridad del pipeline de MLOps")

P: ¿Por qué no se puede hacer deep packet inspection en los interconnects de entrenamiento de alta velocidad y cómo se compensa?
R: Porque destruiría el rendimiento. Se compensa con mayor aislamiento, participantes conocidos, colocación restringida de jobs, protecciones físicas/de fabric y monitoreo de patrones de tráfico anómalos. (Sección "Fundamentos de seguridad en la nube para IA")

P: ¿Qué estrategias de despliegue gradual menciona la etapa de deployment?
R: Canary, blue-green y shadow. (Sección "Seguridad del pipeline de MLOps")

P: ¿Qué compone un ciclo de vida seguro de los model artifacts?
R: Firmar los artefactos, verificar firmas en el despliegue, registrar provenance, guardar metadatos, generar evidencia SBOM / AI SBOM / model bill-of-materials, loguear transferencias y definir reglas de retención y disposición. (Sección "Seguridad del ciclo de vida de los model artifacts")

P: ¿Cómo debe elegirse el nivel de aislamiento según el ejemplo del capítulo?
R: Según el riesgo, no el control "más fuerte" aislado: un chatbot público de baja sensibilidad puede bastar con aislamiento de contenedor más enforcement de política; un modelo regulado con datos protegidos puede necesitar tenants separados, claves dedicadas, rutas de red más estrictas y aislamiento de carga más fuerte. (Sección "Técnicas de sandboxing y aislamiento")

P: ¿Qué ventaja ofrecen OPA y Gatekeeper, y por qué la política debe poder cambiarse sin redeploy?
R: OPA permite expresar política separada del código de aplicación y evaluarla en request/admission time; Gatekeeper la aplica al admission control de Kubernetes. La política debe poder cambiarse sin redeploy completo para apretar o relajar controles con evidencia, en lugar de hornear cada decisión en el código de serving. (Sección "Aplicación de políticas en runtime")

## Puntos a dominar

- Entender por qué la infraestructura de IA aumenta la presión sobre controles tradicionales: cómputo caro, jobs largos, datasets y artefactos como joyas de la corona, inputs no confiables en runtime.
- Saber segmentar las rutas de entrenamiento, inferencia, datos y gestión, y justificar por qué cada frontera importa (p. ej., inferencia sin acceso a datos crudos de entrenamiento).
- Reconocer las seis etapas del pipeline de MLOps como puntos de control y aplicar la regla "no bypass, no backward flow" con evidencia en cada handoff.
- Dominar el endurecimiento de contenedores y Kubernetes: imágenes mínimas, dependencias pinned, non-root, RBAC mínimo, Pod Security Standards, network policies y admission controllers (incluido GPU).
- Explicar cómo IaC/GitOps y la policy as code hacen exigibles y auditables los valores seguros por defecto, y el papel del escaneo (Checkov) y la detección de drift.
- Describir un ciclo de vida seguro de artefactos con firma, verificación, provenance completo y fallo cerrado si la cadena se rompe (Sigstore, OpenSSF model-signing, AI SBOM de CISA/G7).
- Elegir el nivel de aislamiento según el riesgo y tratar el GPU sharing (MIG) como decisión de riesgo documentada, no como optimización de coste.
- Situar la aplicación de políticas en runtime en gateway, model-server y output, con audit logs que atan decisiones a caller, tenant, modelo, versión de política y hora.
