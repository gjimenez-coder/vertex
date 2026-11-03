# AI Governance, Risk, and Compliance (Gobernanza, riesgo y cumplimiento de la IA) — Estudio

## Tarjetas de repaso

P: ¿Qué pregunta responde cada componente de GRC?
R: Gobernanza establece derechos de decisión y rendición de cuentas; gestión de riesgo identifica qué puede fallar, a quién afecta y qué controles lo reducen; cumplimiento mapea la práctica interna a obligaciones externas.

P: ¿Qué enseña el caso del sistema de contratación potenciado por IA?
R: Que pasó la revisión técnica (validación de entradas, filtrado de salidas, monitoreo conductual) y aun así discriminó a candidatos mayores de 40 años: la seguridad técnica sin gobernanza produce fallos organizacionales, sin atacante ni brecha.

P: ¿Qué significa que "good AI governance has teeth"?
R: Que no es el logo de un comité, sino una estructura de autoridad que define propiedad, rutas de aprobación, escalamiento, excepciones y requisitos de evidencia.

P: ¿Qué controla y qué evidencia necesita un creador de IA?
R: Controla datos de entrenamiento, arquitectura, evaluación, release y comportamiento del modelo; necesita evidencia de procedencia y calidad de datos, representatividad, etiquetado, entrenamiento, evaluación, pruebas de seguridad y sesgo, documentación, criterios de release, monitoreo y manejo de vulnerabilidades.

P: ¿Qué controla y qué evidencia necesita un adoptante de IA?
R: Controla selección del caso de uso, integración, UX, datos enviados, revisión humana, monitoreo y escalamiento; necesita evidencia de ajuste del caso de uso, due diligence del proveedor, manejo de datos, prompts/retrieval, supervisión humana, avisos, apelaciones, respuesta a incidentes y estrategia de salida.

P: ¿Por qué la gobernanza de IA difiere de la de TI?
R: La de TI asume un sistema mayormente determinista; la IA es probabilística, opaca y sufre drift, por lo que la aprobación puntual no basta y se requiere monitoreo continuo post-despliegue.

P: ¿Qué principios de Responsible AI y cómo se traducen a evidencia?
R: Equidad (pruebas de sesgo, apelación), fiabilidad y seguridad (evaluación, red-team, rollback), privacidad y seguridad (inventario de datos, acceso, logging, retención), transparencia (avisos, model cards, explicaciones) y rendición de cuentas (dueños nombrados, aprobaciones, aceptación de riesgo, revisión).

P: ¿Qué distingue a los tres niveles (tiers) de gobernanza?
R: Tier 1: productividad interna de bajo riesgo sin decisiones consecuentes; Tier 2: cara al cliente u operativo con daño reversible; Tier 3: decisiones consecuentes, dominios regulados, poblaciones sensibles, impacto en seguridad, acción agéntica o riesgo material.

P: ¿Qué debe registrar el manejo de excepciones?
R: Control faltante, razón, control compensatorio, fecha de expiración, dueño, revisor y condición de re-revisión; sin excepciones permanentes sin visibilidad ejecutiva.

P: ¿Cuáles son las categorías de riesgo de IA del capítulo?
R: Seguridad, equidad, fiabilidad, privacidad, safety y daño, y autoridad.

P: ¿Qué marcos se usan como referencia para mapear amenazas a controles?
R: MITRE ATLAS y el OWASP Top 10 for Large Language Model Applications, como referencias y no como librería copia-pega.

P: ¿Qué diferencia los permisos humanos delegados de las identidades no humanas en un agente?
R: Los permisos delegados hacen que el agente actúe a través del acceso de un humano (tokens, repos, shell, SaaS, CI/CD); las identidades no humanas son un actor separado (service principal, managed/workload identity) con sus propios permisos y obligaciones de ciclo de vida.

P: ¿Qué evidencia mínima exige aprobar un agente?
R: Dueño nombrado; mapa de autoridad; inventario de herramientas y acciones con permisos separados (read/draft/write/execute/publish/delete/deploy); gates de aprobación para alto impacto; evidencia de least-privilege, vida y rotación de credenciales y prueba de revocación; monitoreo, auditoría, escalamiento y aceptación de riesgo.

P: ¿Qué es la resiliencia regulatoria?
R: Saber qué obligaciones aplican, mapearlas a evidencia, rastrear cambios y mantener flexibilidad, citando siempre la ley vigente y su fecha operativa.

P: ¿Qué debe nombrar una aceptación ejecutiva de riesgo?
R: Riesgo, población afectada, controles faltantes o parciales, controles compensatorios, plan de monitoreo, fecha de revisión y escalamiento; "el patrocinador no debería poder aceptar un riesgo que no puede explicar".

## Preguntas de autoevaluación

P: ¿Por qué un sistema de IA puede ser "seguro" y aun así un fallo organizacional?
R: Porque los controles técnicos cubren solo parte del perfil de riesgo; sin propiedad, monitoreo y rendición de cuentas en la decisión de despliegue, el sistema puede causar daño (discriminación por edad) sin que haya atacante. (Sección: El ejemplo que recorre el capítulo)

P: ¿Por qué no sirve un registro de riesgo que solo dice "model risk"?
R: Porque hay que nombrar el modo de fallo concreto: datos sesgados, discriminación por proxy, prompt injection vía contenido recuperado, mal uso de herramientas por un agente o drift. (Sección: Definición del problema de gobernanza)

P: ¿Puede una organización externalizar la rendición de cuentas comprando una función de IA?
R: No; "you cannot outsource accountability by buying an AI feature". El adoptante conserva responsabilidades (caso de uso, datos, supervisión humana, avisos, apelaciones, respuesta a incidentes) y procurement es donde se vuelven reales o desaparecen. (Sección: Creadores, adoptantes y responsabilidad compartida)

P: ¿Qué implica el comportamiento probabilístico para la gobernanza?
R: Que la gobernanza debe definir el error aceptable, umbrales de monitoreo, revisión humana y la evidencia requerida para decisiones bajo incertidumbre, ya que el modelo no da certeza sino confianza. (Sección: Por qué la gobernanza de IA difiere de la de TI)

P: ¿Por qué la gobernanza informal deja de funcionar a escala?
R: Porque "at five hundred, informal governance is fiction": la aplicación técnica debe integrarse donde ocurre el trabajo (intake, arquitectura, registro de modelos, procurement, CI/CD, MLOps, aprobaciones, observabilidad). (Sección: Marcos de gobernanza que escalan)

P: ¿Qué cambia cuando un sistema puede actuar mediante autoridad real?
R: Que ya no se aprueban solo salidas sino acción a través de autoridad; hay que gobernar permisos delegados e identidades no humanas con mapa de autoridad, inventario, aprobaciones, least-privilege, auditoría y revocación. (Sección: La autoridad del agente como problema de gobernanza)

P: ¿Por qué el EU AI Act no debe describirse como un interruptor único?
R: Porque entró en vigor el 1 de agosto de 2024 y aplica progresivamente; distintas familias de obligaciones (prácticas prohibidas y alfabetización, GPAI, requisitos core, alto riesgo embebido) entran en fechas distintas, y el Code of Practice es apoyo, no todo el régimen. (Sección: Navegar los requisitos de cumplimiento)

P: ¿Qué deben mostrar las métricas de gobernanza?
R: Si la gobernanza funciona, no si hubo reuniones: cobertura, oportunidad, calidad, efectividad de control (cobertura de monitoreo, éxito de pruebas de revocación y rollback) y resiliencia de negocio (lanzamientos inseguros detenidos, incidentes reducidos). (Sección: Roles, rendición de cuentas e integración en el ciclo de vida)

## Checklist

- Clasificar cada caso de uso en un tier (1-3) y asignar un dueño nombrado.
- Exigir evidencia proporcional al riesgo e integrar la aprobación en el ciclo de vida.
- Tratar la revisión de proveedores como gobernanza: qué datos fluyen, si se usan para entrenar, qué evaluación y logging existen y cómo deshabilitar la función.
- Mantener monitoreo continuo post-despliegue de calidad, drift, sesgo, eventos de seguridad y safety, escalamientos, quejas y excepciones.
- Registrar cada excepción con control faltante, razón, control compensatorio, expiración, dueño, revisor y condición de re-revisión; sin excepciones permanentes sin visibilidad ejecutiva.
- Mapear amenazas a controles usando MITRE ATLAS y OWASP Top 10 for LLM Applications como referencias.
- Dejar artefactos: model card / system card, threat model y decisión de release; para agentes, añadir un mapa de autoridad.
- Para agentes: inventario de autoridad por agente, separar permisos delegados de identidades no humanas, gates para acciones de alto impacto y prueba de revocación y rollback.
- Mantener un mapa vivo caso de uso → obligación → evidencia (EU AI Act, NIST AI RMF 1.0 / AI 600-1, ISO/IEC 42001, SANS AI Security Maturity Model, OCC Bulletin 2011-12, FDA, AEDT de NYC, SB 26-189 de Colorado, OMB M-25-21), citando ley vigente y fecha.
- Nombrar roles del sistema (patrocinador ejecutivo, dueño de negocio, técnico, de datos, socios de seguridad/privacidad/legal, operaciones y ruta de incidentes) y usar RACI solo si aclara la acción.
- Hacer concreta la aceptación ejecutiva de riesgo: riesgo, población afectada, controles faltantes/parciales, compensatorios, plan de monitoreo, fecha de revisión y escalamiento.
- Hacer verificables por máquina los gates del ciclo de vida (intake, requisitos, design review, validación, despliegue, operación, retiro) donde sea posible.
