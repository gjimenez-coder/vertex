# AI Security Engineering (Ingeniería de seguridad para IA) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo? / R: Los controles tradicionales pueden estar bien configurados y aun así fallar donde vive la exposición real; la ingeniería de seguridad para IA consiste en encontrar esas fronteras y hacerlas *enforceable* (exigibles).

P: ¿Qué demostró la escena de apertura con la GPU compartida? / R: Que la aislación de namespaces de Kubernetes no se extiende a la memoria de la GPU: un pentester recuperó datos de otro equipo con solo "un acelerador compartido y timing", sin privilegios de admin.

P: ¿Por qué la memoria GPU es un riesgo de seguridad? / R: Puede persistir tras liberar una carga si la aplicación, runtime, driver o hardware no la limpia; no se zera como las páginas de CPU. Pesos, activaciones, gradientes, prompts, embeddings y muestras deben tratarse como sensibles mientras residan en el acelerador.

P: ¿Qué opciones de multi-tenancy en GPU existen y cuál da aislamiento por hardware fuerte? / R: Time-slicing, MPS, MIG, GPUs virtuales y nodos dedicados ofrecen distintos trade-offs; MIG da particionado por hardware fuerte en GPUs NVIDIA compatibles, y los nodos dedicados son la respuesta más limpia para datos regulados o tenants no confiables.

P: ¿Qué significa "la colocación sigue al riesgo, no a la presión de la cola"? / R: Que en plataformas sensibles la colocación en GPU debe ser una decisión de seguridad registrada (clase de carga, confianza, sensibilidad, modo del acelerador, aislamiento, clearing, patch level, dueño de excepción), con registro de co-residencia.

P: ¿Cómo debe configurarse la red de Kubernetes para cargas de ML? / R: Empezar con *default-deny* en ingress y egress, añadir allow-rules explícitas, canalizar dependencias por mirrors internos y registrar egress inesperado como evento de seguridad.

P: ¿Qué estándar reemplazó a PodSecurityPolicy y cómo se aplica? / R: Pod Security Standards / Pod Security Admission (PSP fue removida en Kubernetes 1.25): usar `restricted` en producción, `baseline` al migrar y `privileged` solo como excepción documentada.

P: ¿Por qué los Kubernetes secrets no bastan por sí solos? / R: Porque conviene usar gestores externos (Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager) para rotación, auditoría y credenciales dinámicas, y tokens de service account proyectados con audiencia y expiración acotadas en vez de tokens permanentes.

P: ¿Qué función cumple el model registry? / R: Es la puerta de promoción entre experimentación y producción; registra origen, hashes, firmas, model card, licencia, scan, validación, owner, aprobación, entorno y rollback. El serving solo carga artefactos aprobados y se separan permisos (publish, approve, read, deploy, revoke).

P: ¿Qué verifica el *model loading gate*? / R: Registro, hash, firma/aprobación, formato, resultado del scanner, runtime permitido y entorno; es la última oportunidad de detener un artefacto inseguro antes de cargarlo.

P: ¿Por qué "los embeddings no son matemática inofensiva"? / R: Porque pueden codificar información sensible sobre documentos, usuarios, clientes, decisiones y operaciones internas; las bases vectoriales deben tratarse como data stores sensibles, no cachés.

P: ¿Qué es el *authority laundering* en recuperación? / R: Un fallo sutil donde la app recupera contenido sensible correctamente y lo pasa a un modelo o agente para un fin que la autorización original no permitía; por eso recuperar y actuar necesitan compuertas separadas y la autorización debe considerar el propósito.

P: ¿Qué riesgo tienen los formatos de modelo basados en pickle? / R: Pueden ejecutar código al cargarse; se recomienda escaneo (p. ej. ModelScan) y preferir formatos como safetensors, recordando que una serialización más segura no prueba que el comportamiento del modelo sea seguro.

P: ¿En qué se diferencian un agente de permiso delegado y una identidad no humana? / R: El de permiso delegado actúa con la autoridad de un usuario humano (sesión, token de repo, shell, cuenta SaaS) y necesita sesiones acotadas y allowlists; la identidad no humana actúa como su propio workload con owner, credenciales de vida corta, roles mínimos y kill switch. Fallan y se revocan distinto.

P: ¿Por qué la observabilidad para IA es "evidencia" y no solo telemetría? / R: Porque debe permitir saber quién llamó a qué modelo, qué contexto de recuperación se usó, qué tool action corrió, qué credencial y política lo permitieron, cuánto costó y si el comportamiento cambió; las anomalías son leads de seguridad.

## Preguntas de autoevaluación

P: ¿Por qué los namespaces de Kubernetes no deben tratarse como prueba de aislamiento de memoria GPU, y qué mitigaciones propone el capítulo? / R: Porque la aislación de namespaces no cubre la memoria del acelerador, que puede persistir entre cargas. Mitigaciones: limpiar buffers sensibles antes de liberarlos, usar runtimes de confianza y drivers parcheados, separar cargas no confiables de trabajos sensibles y preferir GPUs/nodos dedicados o particionado por hardware. (Sección "GPU infrastructure security")

P: ¿Qué controles hacen que el egress en Kubernetes importe "más de lo esperado"? / R: Un contenedor de training comprometido puede exfiltrar datos o contactar C2; por eso se usa default-deny en egress, se canalizan dependencias por mirrors internos y se registra el egress inesperado como evento de seguridad. (Sección "Container and Kubernetes security for ML workloads")

P: ¿Por qué un namespace de notebook con egress amplio y buckets de producción no es un sandbox? / R: Porque con tokens persistentes, buckets de producción montados y acceso privilegiado a GPU se convierte en "un puente a producción con una UI más amigable"; los notebooks deben mantenerse separados. (Sección "Container and Kubernetes security for ML workloads", PDF p. 435)

P: ¿Qué hace del model serving un blanco de alto valor y cómo se debería autenticar un endpoint de inferencia? / R: Convierte artefactos entrenados en comportamiento de producción alcanzable. La autenticación depende de la clasificación de riesgo del modelo y la ubicación del consumidor: mTLS/identidad de servicio para interno; identidad fuerte, rate limiting, validación y monitoreo de abuso para externo; política aún más estricta para endpoints que sirven a agentes. (Sección "Model serving and registry security")

P: ¿Qué significa que un modelo "no está gobernado, simplemente está corriendo"? / R: Que si no puedes vincular un modelo en producción con versiones de datos, código, entorno, dependencias, evaluaciones, checks de seguridad, aprobaciones y hashes finales, carece de evidencia de promoción; la revocación debe ser una operación del pipeline, no una búsqueda manual. (Sección "MLOps pipeline security", PDF p. 441)

P: ¿Por qué el modelo no debe ser la autoridad de política de sus propias tool calls? / R: Porque el modelo solo propone; un motor de política debe evaluar antes de ejecutar (identidad del agente y del usuario delegado, herramienta, operación, objeto destino, parámetros, sensibilidad, aprobación y versión de política), exigiendo aprobación para acciones irreversibles. (Sección "Cloud AI platform and secrets security")

P: ¿Por qué hay que probar ambos paths de revocación de un agente? / R: Porque es común revocar el token obvio y dejar viva otra vía (credencial de metadata de un job cloud, sesión SaaS en un navegador, acceso de instalación de una app de repo, certificado de service mesh); el drill debe probar que el agente ya no puede actuar. (Sección "Cloud AI platform and secrets security")

P: ¿Cómo debe leerse el registro de auditoría según el capítulo? / R: Como una cadena: identidad → request → contexto recuperado → paso del modelo/agente → propuesta de herramienta → decisión de política → credencial usada → objeto destino → resultado → respuesta, separando metadata de payloads para no crear una nueva superficie de brecha. (Sección "Observability and network architecture")

## Puntos a dominar

- Explicar por qué la aislación de namespaces no cubre la memoria GPU y qué implica tratar pesos, activaciones, prompts y embeddings como sensibles en el acelerador.
- Justificar la colocación en GPU como decisión de seguridad registrada, con registro de co-residencia (job, nodo, versión de driver y runtime).
- Aplicar default-deny de red, pods non-root/`restricted`, cuotas defendibles, secretos externos con tokens de vida corta y evidencia de runtime que confirme las reglas de admission.
- Describir el model registry como puerta de promoción y el *model loading gate* (registro, hash, firma, formato, scanner, runtime, entorno) con separación de permisos.
- Tratar las bases vectoriales como datos sensibles: autorización server-side antes de recuperar, considerando el propósito para evitar *authority laundering*.
- Producir evidencia de promoción encadenada en MLOps y hacer de la revocación una operación del pipeline; preferir safetensors frente a formatos pickle y escanear artefactos.
- Diferenciar agentes de permiso delegado de identidades no humanas y probar ambos paths de revocación; ubicar la política de ejecución de herramientas antes de la acción, con aprobación para acciones irreversibles.
- Convertir la observabilidad en cadena de evidencia, tratar costo anómalo, egress inesperado y denegaciones de política como señales de seguridad y segmentar red (training/inferencia/datos/gestión/observabilidad/acceso externo).
