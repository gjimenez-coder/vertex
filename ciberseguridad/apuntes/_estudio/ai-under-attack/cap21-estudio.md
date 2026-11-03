# AI Security Operations (Operaciones de seguridad para IA) — Estudio

## Tarjetas de repaso

P: ¿Por qué la monitorización tradicional puede fallar ante ataques de IA?
R: Porque los ataques de IA se mueven dentro de rutas autorizadas (acceso legítimo, APIs permitidas, prompts normales); puede ver toda la actividad y aun así perder la intención ("Traditional monitoring can see activity and still miss intent").

P: ¿Cuál es la tesis central del capítulo sobre la seguridad operativa de IA?
R: Conectar en una sola cadena de evidencia el prompt, el modelo, la capa de recuperación, la llamada a herramienta, el servicio downstream, la identidad y la acción de respuesta, haciendo legible el comportamiento de la IA para el programa de seguridad existente.

P: ¿Qué es la cadena de evidencia en operaciones de IA?
R: Un ID de correlación o de acción que sigue la ruta desde el prompt del usuario hasta la llamada al modelo, retrieval, invocación de herramienta, API backend, respuesta, alerta, contención y revisión post-incidente.

P: ¿Qué contexto de autoridad necesita la cadena en sistemas agénticos?
R: Identidad humana delegada, identidad no humana del agente, credencial usada, decisión de política, nombre de herramienta, objeto objetivo, estado de aprobación, resultado y ruta de revocación.

P: ¿Por qué una credencial legítima usada con intención atacante sigue siendo un incidente?
R: Porque la pregunta operativa no es solo si la acción estaba permitida, sino si la secuencia de acciones permitidas todavía tiene sentido ("A legitimate credential used for attacker intent is still an incident").

P: ¿Qué es la retención por niveles de riesgo (risk-tiered)?
R: Sesiones de bajo riesgo guardan metadatos y contenido muestreado; sesiones sospechosas preservan contexto más rico; incidentes confirmados preservan la evidencia completa, con acceso al prompt crudo limitado y auditado.

P: ¿Por qué no basta registrar solo la respuesta final de la IA?
R: Porque el paso dañino puede estar en el retrieval, el uso de herramienta o el razonamiento intermedio; los logs de respuesta deben indicar si la salida fue filtrada, rechazada, bloqueada, redactada o permitida.

P: ¿Cuáles son las cuatro estrategias de detección y cómo se combinan?
R: Signature-based, anomaly detection, semantic detection y correlación/contexto; funcionan mejor cuando varias señales débiles forman una historia más fuerte.

P: ¿Qué catálogos de partida se usan para la detección por firmas?
R: MITRE ATLAS y material OWASP LLM, para frases de prompt injection, intentos de revelar system prompts, patrones de jailbreak, consultas de extracción y parámetros de herramienta maliciosos conocidos.

P: ¿Qué define la severidad de una alerta de IA?
R: El impacto y la accionabilidad (la acción downstream), no lo raro que parezca el prompt: un prompt extraño sin retrieval ni herramienta ni salida sensible puede ser baja; un prompt anodino que lleva a un agente privilegiado a actualizar un registro de cliente es alta.

P: ¿Qué pasos debe seguir el playbook de respuesta a un memory poisoning?
R: Identificar qué memoria/fuente cambió, comparar con baseline conocido-bueno, borrar entradas envenenadas, restaurar desde fuentes limpias y verificar con prompts que antes disparaban el comportamiento corrupto.

P: ¿Por qué hay que separar el estado del sistema del estado de autoridad?
R: Porque revertir un cambio (rollback) no revoca la credencial, y rotar la credencial no deshace lo que el agente ya cambió; además la revocación debe probarse reintentando la acción bloqueada desde la misma ruta.

P: ¿Cómo se responde a amenazas por deepfakes según el capítulo?
R: Tratándolas como problemas de verificación, no solo de análisis de medios: verificación out-of-band, procedimientos de callback, retención de pagos y preservación de medios.

P: ¿Qué debe producir el análisis post-incidente?
R: Un root cause analysis con causas inmediatas, factores contribuyentes y condiciones profundas; lecciones con propietario y fecha; un control backlog priorizado por riesgo de recurrencia y blast radius; y métricas (MTTD, contener, revocar, recuperar, validar).

P: ¿Dónde deben vivir las operaciones de IA y con qué se alimenta la mejora continua?
R: Dentro del SOC, usando el mismo SIEM, SOAR, gestión de casos y escalado, con campos y playbooks de IA; la mejora continua consume MITRE ATLAS, OWASP, reportes de proveedores, inteligencia de ISAC y hallazgos internos, con el lenguaje de madurez de SANS.

## Preguntas de autoevaluación

P1: ¿Qué enseña el caso de las 2:47 AM del chatbot de atención al cliente?
R1: Que mirar solo si cada petición está autorizada falla: 847 peticiones desde una sesión autenticada, con variaciones leves, se marcaron como falso positivo mientras el atacante extraía comportamiento del prompt, datos de clientes, contexto de recuperación e información de flujo. Hay que mirar la secuencia de acciones permitidas. (Sección: El ejemplo que recorre el capítulo)

P2: ¿Cómo pueden disfrazarse de actividad normal el prompt injection, la model extraction, el memory poisoning y un agente comprometido?
R2: El prompt injection parece entrada normal; la model extraction parece uso de API intenso pero legítimo; el memory poisoning parece conversación ordinaria o actualización rutinaria de contenido; un agente comprometido usa el token real del usuario o una identidad de servicio válida. (Sección: Por qué difieren las operaciones de seguridad de IA)

P3: ¿Qué categorías de telemetría de IA se deben recolectar?
R3: Logging de prompt y respuesta, telemetría conductual (volumen, tokens, temas, tasa de rechazo, invocación de herramientas, latencia), telemetría de agentes (herramientas vistas/invocadas, parámetros, objetivos, coincidencia con el objetivo del usuario) y telemetría de infraestructura y datos (model serving, retrieval vectorial, embeddings, base de conocimiento, escrituras en memoria). (Sección: Recolección de telemetría de IA)

P4: ¿Por qué las firmas no pueden cargar solas el programa de detección?
R4: Porque los atacantes varían el texto, cambian de idioma y parten el payload en varios turnos; por eso se combinan con anomaly detection, semantic detection y correlación. (Sección: Estrategias de detección)

P5: ¿Qué cuatro contenidos núcleo debe tener una buena alerta de IA?
R5: Summary (regla, riesgo, sistema, usuario, agente, sesión), Evidence (prompt o redactado, patrón, puntuación de anomalía, retrieval IDs, llamadas a herramientas, políticas, acciones downstream), Context (comportamiento base, sensibilidad, tenant, versión del modelo, alertas relacionadas) y Action (contención, propietario, escalado, objetivo de revocación). (Sección: Diseño y gestión de alertas)

P6: ¿Por dónde debe empezar la respuesta a un agent compromise y cómo se recupera?
R6: Por la autoridad (sesión delegada humana, identidad de servicio no humana o ambas, credenciales, herramientas, aprobaciones evadidas); se contiene quitando la capacidad de actuar antes de terminar la investigación y se recupera reconstruyendo confianza con alcance restringido, decidiendo si reutilizar la instancia o crear una nueva con memoria limpia y credenciales nuevas. (Sección: Playbooks de respuesta a incidentes)

P7: ¿Qué marca el límite operativo del SOC ante amenazas habilitadas por IA?
R7: El SOC maneja lo que puede operacionalizar (verificación, telemetría, contención de cuentas, escalado de comunicaciones, preservación de evidencia, actualización de detección); las decisiones de política, legales o de relaciones públicas tienen otros propietarios. (Sección: Respuesta a amenazas habilitadas por IA)

P8: ¿Qué significa que "una lección sin propietario es un recuerdo, no una mejora"?
R8: Que las lecciones del post-incidente deben tener propietario y fecha para traducirse en un control backlog priorizado por riesgo de recurrencia y blast radius; de lo contrario no generan mejora real. (Sección: Análisis post-incidente y mejora)

## Checklist

- [ ] Asignar a cada evento de IA un ID de correlación/acción que una prompt → modelo → retrieval → herramienta → API backend → respuesta → alerta → contención → revisión.
- [ ] Añadir contexto de autoridad a sistemas agénticos: identidad humana delegada, identidad no humana, credencial, decisión de política, herramienta, objeto objetivo, aprobación, resultado y ruta de revocación.
- [ ] Registrar prompt y respuesta con IDs de contexto, versión del modelo, identidad de tenant/usuario, decisiones de política y si la salida fue filtrada, rechazada, bloqueada, redactada o permitida.
- [ ] Aplicar retención por niveles de riesgo y limitar/auditar el acceso al contenido crudo del prompt.
- [ ] Recolectar telemetría conductual, de agentes e infraestructura/datos (incluyendo fuentes de entrenamiento, embeddings, base de conocimiento y escrituras en memoria).
- [ ] Implementar el esquema mínimo de correlación (session, prompt, response, model, retrieval, memory, tool, credencial, política, aprobación, alert, case, contención, revocación).
- [ ] Combinar detección signature-based, anomaly, semantic y correlación, usando MITRE ATLAS y OWASP LLM como catálogos.
- [ ] Revisar calidad de detección por rutas completas y por clase de ataque, con casos de prueba que se corran tras cambios mayores de modelo, política, retrieval o herramientas.
- [ ] Asignar severidad por impacto y accionabilidad (acción downstream), no por rareza del prompt; suprimir solo agregando y dejando rastro.
- [ ] Mantener playbooks de IA sobre el ciclo existente (trigger, triage, containment, investigation, eradication, recovery, communication, lessons learned) con la evidencia en el mismo caso.
- [ ] Preservar evidencia antes de limpiar; probar la revocación reintentando la acción bloqueada; separar rollback de estado de la revocación de autoridad.
- [ ] Responder a deepfakes y social engineering con verificación out-of-band, callback y separación de chat/aprobación; anclarse en ejemplos con fuente para malware adaptativo.
- [ ] Hacer root cause analysis (causas inmediatas, factores contribuyentes, condiciones profundas), asignar propietario y fecha a cada lección y producir un control backlog con métricas (MTTD, contener, revocar, recuperar, validar).
- [ ] Integrar las operaciones de IA en el SOC (SIEM, SOAR, casos, escalado), entrenar analistas, definir rutas de escalado antes del incidente y correr drills pequeños.
