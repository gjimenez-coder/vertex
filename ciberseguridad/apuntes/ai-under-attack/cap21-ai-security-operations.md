# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 21 — AI Security Operations (Operaciones de seguridad para IA)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El capítulo trata de cómo operar la seguridad (SOC) cuando el objeto a defender es un sistema de IA. El problema de fondo es operativo: los ataques a IA suelen moverse dentro de rutas autorizadas —acceso legítimo, APIs permitidas, prompts de aspecto normal y flujos de negocio esperados— por lo que la monitorización tradicional puede ver toda la actividad y aun así perder la intención. Como dice el libro, "Traditional monitoring can see activity and still miss intent" (PDF p. 450).

La tesis central es que la seguridad operativa debe conectar en una sola cadena de evidencia el prompt, el modelo, la capa de recuperación (retrieval), la llamada a herramienta, el servicio downstream, la identidad y la acción de respuesta. No se trata de inventar un universo separado de "AI security operations", sino de hacer legible el comportamiento de la IA para el programa de seguridad que ya existe: suficiente telemetría para investigar, contexto para triar, playbooks para responder y retroalimentación hacia ingeniería para que el mismo fallo no se repita.

Sales sabiendo cómo difiere la operación de IA, qué telemetría recolectar, qué estrategias de detección combinar, cómo diseñar alertas y playbooks, cómo responder a amenazas habilitadas por IA, cómo hacer análisis post-incidente e integrar todo en el SOC con mejora continua.

## El ejemplo que recorre el capítulo
El capítulo abre con un caso hilo conductor: a las 2:47 AM un SIEM marca actividad inusual contra un chatbot de atención al cliente —847 peticiones en 90 minutos desde una sola sesión autenticada, cada una con variaciones leves de preguntas normales. El analista nocturno vio que todo venía de sesión autenticada, que no saltó firma de exfiltración, y marcó el ticket como falso positivo. Por la mañana el atacante había extraído comportamiento del prompt, datos de cuentas de clientes, contexto de recuperación e información de flujo de trabajo (PDF p. 450). El caso ilustra por qué hay que mirar la secuencia de acciones permitidas, no solo si cada petición estaba autorizada.

## Por qué difieren las operaciones de seguridad de IA
La seguridad operativa tradicional tiene patrones maduros para intrusiones de red, malware, acceso no autorizado y robo de datos: el atacante cruza un límite y deja evidencia que mapea a un playbook. Los ataques de IA operan dentro de una ruta autorizada mientras intentan torcer el sistema hacia un resultado no autorizado.

- Un prompt injection puede parecer entrada normal.
- La model extraction puede parecer uso de API intenso pero legítimo.
- El memory poisoning puede parecer conversación ordinaria o actualización rutinaria de contenido.
- Un agente comprometido puede usar el token real del usuario o una identidad de servicio válida.

La pregunta operativa va más allá de si la petición estaba permitida: pregunta si la secuencia de acciones permitidas todavía tiene sentido.

### La cadena de evidencia
Cada evento de IA debe llevar un ID de correlación o de acción que siga la ruta desde el prompt del usuario hasta la llamada al modelo, retrieval, invocación de herramienta, API backend, respuesta, alerta, contención y revisión post-incidente. Para sistemas agénticos la cadena también necesita contexto de autoridad: identidad humana delegada, identidad no humana del agente, credencial usada, decisión de política, nombre de herramienta, objeto objetivo, estado de aprobación, resultado y ruta de revocación. "A legitimate credential used for attacker intent is still an incident" (PDF p. 452). Esto se alinea con la guía conjunta ACSC/CISA/NSA de 2026, que trata accountability, observabilidad, contención y referenciado de fuentes como preocupaciones operativas centrales para IA agéntica.

## Recolección de telemetría de IA
La telemetría es la materia prima. Si el sistema no registra qué recibió, qué contexto usó, qué herramienta llamó, qué identidad autorizó y qué cambió downstream, el SOC no puede distinguir una sesión ruidosa de un ataque.

- Logging de prompt y respuesta: capturar prompt, estado de conversación relevante, IDs de contexto recuperado, versión del modelo, identidad de tenant/usuario, decisiones de política y metadatos de respuesta. Los logs de respuesta deben indicar si la salida fue filtrada, rechazada, bloqueada, redactada o permitida. Registrar solo la respuesta final no basta: el paso dañino puede estar en retrieval, uso de herramienta o razonamiento intermedio.
- Retención por niveles de riesgo (risk-tiered): sesiones de bajo riesgo guardan metadatos y contenido muestreado; sesiones sospechosas preservan contexto más rico; incidentes confirmados preservan la evidencia completa. El acceso al contenido crudo del prompt debe limitarse y auditarse.
- Telemetría conductual: volumen de peticiones, uso de tokens, longitud de respuesta, distribución de temas, tasa de rechazo, frecuencia de invocación de herramientas, amplitud de retrieval, latencia, tasa de error y reintentos para alcanzar contenido protegido.
- Telemetría de agentes: qué herramientas ve, cuáles invoca, qué parámetros genera, qué objetivos toca y si la acción coincide con el objetivo declarado del usuario. Un agente de soporte que normalmente lee tickets pero de pronto exporta registros de clientes debe destacar aunque las credenciales sean válidas.
- Telemetría de infraestructura y datos: además de logs de red, autenticación, proceso, endpoint y aplicación, añadir señales de model serving, retrieval vectorial, pipelines de datos, registros de modelos, carga de GPU, latencia de inferencia, decisiones de política y ejecución de herramientas. El poisoning y el abuso de retrieval empiezan antes de la llamada al modelo: monitorizar fuentes de datos de entrenamiento, actualizaciones de embeddings, cambios en la base de conocimiento, fallos de ingesta y escrituras inesperadas en memoria.

### Esquema mínimo de correlación
Session ID e identidad de usuario/tenant; prompt ID, response ID, model ID, versión y resultado del safety-filter; retrieval IDs, document IDs, memory IDs y etiquetas de sensibilidad; tool invocation ID, nombre de herramienta, operación, parámetros, objeto objetivo y resultado; credencial delegada o identidad no humana; decisión de política, registro de aprobación, alert ID, case ID, acción de contención y estado de revocación.

## Estrategias de detección
La detección de IA funciona mejor cuando varias señales débiles forman una historia más fuerte.

- Signature-based: detectar frases comunes de prompt injection, intentos de revelar system prompts, patrones de jailbreak, consultas estilo extracción y parámetros de herramienta maliciosos conocidos. Usar MITRE ATLAS y material OWASP LLM como catálogos de partida. Las firmas no cargan el programa solo: los atacantes varían el texto, cambian de idioma y parten el payload en varios turnos.
- Anomaly detection: compara contra la línea base (volumen, temas, retrieval amplio, bucles costosos, llamadas excesivas a herramientas, latencia anormal). Las líneas base requieren mantenimiento.
- Semantic detection: evalúa el significado; una petición sintácticamente inofensiva puede pedir saltar instrucciones o revelar datos protegidos. Los clasificadores son su propia superficie de ataque y necesitan prueba, ajuste y monitorización.
- Correlación y contexto: es la diferencia entre un prompt sospechoso y un incidente; los IDs de correlación permiten seguir la ruta sin coser logs manualmente a las 3 AM.

La revisión de calidad de detección debe analizar rutas de incidente completas, no aciertos aislados, y revisar falsos positivos/negativos por clase de ataque (prompt injection, model extraction, memory poisoning, agent compromise, deepfake fraud, automated social engineering), con casos de prueba representativos que se corren tras cambios mayores de modelo, política, retrieval o herramientas.

## Diseño y gestión de alertas
Una buena alerta de IA debe decir qué pasó, por qué importa, qué evidencia la respalda, qué ruta de respuesta aplica y qué acción se recomienda. Contenido núcleo:

- Summary: regla de detección, riesgo, sistema afectado, usuario, agente y sesión.
- Evidence: prompt (o redactado), patrón coincidente, puntuación de anomalía, retrieval IDs, llamadas a herramientas, decisiones de política y acciones downstream.
- Context: comportamiento base, nivel de sensibilidad, tenant, versión del modelo y alertas relacionadas.
- Action: opciones de contención, propietario, ruta de escalado y objetivo de revocación.

La severidad debe reflejar impacto y accionabilidad, no lo raro que parezca el prompt: un prompt extraño sin retrieval, sin herramienta y sin salida sensible puede ser baja severidad; un prompt anodino que llevó a un agente privilegiado a actualizar un registro de cliente es alta. La supresión solo cuando el patrón se entiende, agregando por sesión/tenant/modelo/ruta de herramienta en vez de borrar la regla, y dejando rastro de qué se ocultó y por qué.

## Playbooks de respuesta a incidentes
Los playbooks de IA encajan en el ciclo existente: trigger, triage, containment, investigation, eradication, recovery, communication, lessons learned. La diferencia es la evidencia (prompts, retrieval, comportamiento del modelo, llamadas a herramientas, autoridad del agente, impacto downstream) en el mismo registro de caso.

- Prompt injection: determinar si el ataque llegó al modelo, cambió comportamiento, disparó una herramienta, accedió a contexto protegido o causó acción downstream. Usar el ID de correlación para inspeccionar cada servicio tocado; si el contenido inyectado vino de documentos recuperados o memoria, limpiar la fuente antes de reiniciar.
- Model extraction: estimar volumen y patrones de consulta, funcionalidad expuesta, fallos de rate-limit y acceso a salidas privilegiadas; contención con bloqueo de cuenta, rate limits más estrictos o cambios de acceso al modelo.
- Memory poisoning: identificar qué memoria/fuente cambió, comparar con baseline conocido-bueno, borrar entradas envenenadas, restaurar desde fuentes limpias y verificar con prompts que antes disparaban el comportamiento corrupto.
- Agent compromise: empezar por la autoridad (sesión delegada humana, identidad de servicio no humana o ambas; credenciales; herramientas; aprobaciones evadidas). Contener quitando la capacidad de actuar antes de terminar la investigación; recuperar reconstruyendo confianza con alcance restringido y monitorización reforzada, decidiendo si reutilizar la instancia o crear una nueva con memoria limpia y credenciales nuevas.

### Preservación de evidencia, revocación y rollback
La limpieza puede destruir la evidencia necesaria: antes de borrar memoria, rotar credenciales o deshabilitar un agente, preservar ruta del prompt, registros de retrieval, llamadas a herramientas, decisiones de política y logs del sistema objetivo, bajo controles de acceso de incidente y con redacción. La revocación debe probarse, no asumirse: tras deshabilitar sesión, grant OAuth, service account, token de repositorio, perfil de navegador, MCP server o conector, intentar de nuevo la acción bloqueada desde la misma ruta. Separar el estado del sistema del estado de autoridad: revertir un cambio no revoca la credencial, y rotar la credencial no deshace lo que el agente ya cambió.

## Respuesta a amenazas habilitadas por IA
Algunos incidentes atacan sistemas de IA; otros usan la IA como arma.

- Deepfakes: tratar voz/vídeo/peticiones de ejecutivos sospechosas como problemas de verificación, no solo de análisis de medios. Respuesta: verificación out-of-band, procedimientos de callback, retención de pagos y preservación de medios. Ejemplos: el fraude por videollamada de Hong Kong (2024) y la robocall de Biden en New Hampshire.
- Automated social engineering: la IA abarata el phishing personalizado y la impersonación multilingüe; detectar timing poco natural, personalización de alto volumen, cambios rápidos de tema e inconsistencias lingüísticas sutiles. Respuesta: romper la ventaja del canal con verificación por callback y separar chat de aprobación. "fluency is not proof of identity" (PDF p. 462).
- Adaptive/evasive malware: anclarse en ejemplos con fuente —reportes de Google GTIG sobre PROMPTFLUX y PROMPTSTEAL, y la investigación Agent Commander de Johann Rehberger sobre promptware C2— y monitorizar comportamiento que cambia en respuesta a las defensas.

El límite operativo: el SOC maneja lo que puede operacionalizar (verificación, telemetría, contención de cuentas, escalado de comunicaciones, preservación de evidencia, actualización de detección); las decisiones de política, legales o de relaciones públicas tienen otros propietarios.

## Análisis post-incidente y mejora
El root cause analysis debe identificar causas inmediatas, factores contribuyentes y condiciones operativas profundas. No basta con "el prompt injection funcionó": preguntar por qué la entrada llegó al modelo, por qué el retrieval dio contexto peligroso, por qué se permitió la herramienta, por qué se perdió la alerta y por qué la contención tardó. Las lecciones deben tener propietario y fecha —"A lesson without an owner is a memory, not an improvement" (PDF p. 463)—. El trabajo debe producir un control backlog priorizado por riesgo de recurrencia y blast radius, y métricas de mean time to detect, contain, revoke, recover y validar comportamiento limpio.

## Integración en el SOC y mejora continua
Las operaciones de IA deben vivir dentro del SOC, usando el mismo SIEM, SOAR, gestión de casos, escalado y revisión de incidentes, añadiendo campos y playbooks específicos de IA pero manteniendo una experiencia de analista integrada. Entrenar analistas en prompt injection, model extraction, memory poisoning, agent compromise, verificación de deepfakes e ingeniería social con IA; definir rutas de escalado antes del incidente (quién posee el modelo, el índice de retrieval, la credencial del agente, el motor de políticas). Correr drills pequeños (una ruta de prompt injection, una de memory poisoning, una de revocación de agente, una de verificación de deepfake). La mejora continua consume MITRE ATLAS, OWASP, reportes de proveedores, inteligencia de ISAC y hallazgos internos, y usa el lenguaje de madurez de SANS, convirtiéndolo en reglas, playbooks, formación y cambios de control.

## Ideas clave
- El centro operativo es la cadena de evidencia: un ID de correlación/acción que une prompt → modelo → contexto → herramienta → credencial → sistema objetivo → alerta → playbook → contención → revocación → lección.
- Los ataques de IA usan acceso legítimo e intención maliciosa; hay que vigilar si la secuencia de acciones permitidas tiene sentido, no solo si cada acción estaba autorizada.
- Una credencial legítima usada con intención atacante sigue siendo un incidente; los agentes requieren contexto de autoridad (identidad humana delegada y no humana).
- La detección combina firmas, anomalía, análisis semántico y correlación; la telemetría usa retención por niveles de riesgo y separa metadatos del contenido crudo del prompt.
- La severidad de una alerta la define la acción downstream, no lo raro que parezca el prompt.
- Preservar evidencia antes de limpiar; probar que la revocación realmente bloquea la acción; separar rollback de estado de la revocación de autoridad.
- Las amenazas habilitadas por IA (deepfakes, social engineering, malware adaptativo) se responden con verificación out-of-band y ejemplos con fuente, dentro del límite operativo del SOC.
- La mejora continua produce un control backlog con propietarios y métricas (MTTD, contención, revocación, recuperación), apoyada en MITRE ATLAS, OWASP, NIST AI RMF y madurez SANS.
