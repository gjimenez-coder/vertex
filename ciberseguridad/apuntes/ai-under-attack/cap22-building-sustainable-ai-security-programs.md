# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 22 — Building Sustainable AI Security Programs (Construir programas de seguridad de IA sostenibles)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El capítulo trata de cómo mantener vivo un programa de seguridad de IA a lo largo del tiempo. La tesis central es que la seguridad de IA no es un proyecto puntual de hardening, sino una disciplina operativa: "AI security is not a one-time hardening project. It is an operating discipline" (PDF p. 487). Muchos programas arrancan con patrocinio ejecutivo, financiación y buenas políticas, funcionan dieciocho meses y luego se degradan hasta quedar como una "paper policy" cuando cambian los líderes, el presupuesto o el personal.

Un programa sostenible sobrevive a cambios de liderazgo, presión presupuestaria, rotación de personal, cambio de modelos, adopción de agentes y movimiento regulatorio. Mantiene los controles actualizados sin depender de un campeón heroico, hace visible su valor a los ejecutivos, resulta práctico para los ingenieros y distribuye la responsabilidad lo suficiente como para que la salida de una persona no colapse el programa.

Sales sabiendo por qué fallan los programas, cómo diseñarlos organizativamente, cómo construir y retener talento, qué métricas importan, cómo colaborar entre funciones, cómo gestionar el cambio cultural, cómo adaptarse a la evolución del campo y cómo construir resiliencia (sucesión, memoria institucional, preparación ante crisis y evidencia mínima viable).

## Por qué fallan los programas de seguridad de IA
Los programas no fallan por un control técnico equivocado, sino porque la organización trata la seguridad de IA como un proyecto de lanzamiento en vez de como un sistema operativo. Se financia, anuncia, documenta y luego se deja pudrir. Cinco modos de deriva (Figura 22.1, PDF p. 472):

- Dependencia del campeón (champion dependency): mientras ciertas personas permanecen, el programa parece sano; cuando se van, las decisiones se estancan porque nunca se institucionalizó. Hay que documentar por qué se tomaron las decisiones, quién posee cada control, qué métricas prueban el valor y cómo se aprueban las excepciones.
- Fragilidad presupuestaria (budget fragility): los programas financiados como iniciativas de innovación discrecional son fáciles de cortar. La respuesta no es "fear theater", sino conectar los controles a resultados que los ejecutivos entienden (reducción de incidentes, aprobaciones más rápidas, menor exposición regulatoria, lanzamientos seguros).
- Atrofia de capacidades (capability atrophy): un set de pruebas de prompt-injection del año pasado pierde los bypasses actuales; una política previa a los agentes no cubre permisos delegados. La atrofia es el estado por defecto salvo que el mantenimiento esté planificado y financiado, con tiempo protegido.
- Aislamiento (isolation): los equipos fallan cuando se vuelven asesores irrelevantes o bloqueadores permanentes. El mantenimiento de relaciones debe formar parte de las operaciones (planificación de producto, diseño de plataforma, compras, revisión de incidentes, seguimiento legal).
- Deriva de autoridad (authority drift): un agente prototipo recibe un token temporal, una automatización obtiene permiso de escritura para un piloto, y seis meses después nadie recuerda por qué existe el permiso, pero sigue funcionando. Es peligrosa porque "hides inside success" (PDF p. 473). Requiere revisión periódica de identidades y herramientas: identificar la identidad (humana o no humana) dueña de la autoridad, registrar las herramientas/objetivos/datos que alcanza hoy y cuándo se probó por última vez la revocación o rollback.

## Diseño organizativo para la sostenibilidad
Dónde se ubica la seguridad de IA determina visibilidad, autoridad y acceso. Reportar al CISO da rigor; a tecnología, cercanía con la entrega; a un chief AI officer, centralización. Ninguna opción es universalmente correcta; lo erróneo es dar responsabilidad sin acceso, autoridad ni presupuesto. Evalúa las líneas de reporte por los derechos operativos que habilitan. Suelen funcionar mejor los modelos híbridos: una función central fija estándares y métricas (evita la deriva) y enlaces (liaisons) embebidos en producto, plataforma, datos y operaciones hacen el trabajo práctico (evitan la abstracción).

Charter del programa: un documento corto que indica qué posee la seguridad de IA y qué no (alcance de revisión, niveles de riesgo, autoridad para exigir evidencia, ruta de escalado y artefactos operativos mínimos). Debe ser práctico, no un manifiesto.

Niveles de riesgo y evidencia mínima, para no tratar igual a todo chatbot y a todo workflow autónomo:
- Tier 1: uso interno de bajo riesgo, datos limitados y sin autoridad de acción.
- Tier 2: workflow de negocio con datos sensibles, recuperación o impacto en clientes.
- Tier 3: IA agéntica o expuesta externamente con uso de herramientas, acceso de escritura, credenciales delegadas o exposición regulatoria.

Composición del equipo: no todos deben ser investigadores de ML. Aportan security engineers, software engineers, platform engineers, SOC engineers, identity engineers y especialistas de ML/datos. Muchos sistemas actuales no son entrenamiento de modelos a medida, sino workflows agénticos, sistemas de retrieval, APIs de proveedores, copilots, frameworks de orquestación, servidores MCP y capas de automatización. Las interfaces con otras funciones (SOC, plataforma, producto/software, legal/privacidad/compliance, enterprise risk) deben documentarse, nombrando qué posee cada función, cuándo se la involucra, qué evidencia aporta y cómo se escala el riesgo no resuelto.

## Construir y retener talento
El talento es escaso porque el campo aún se está formando; esperar al candidato perfecto genera programas con poco personal y especialistas quemados. Empieza por las brechas de habilidades, no por títulos ideales. El trabajo práctico importa más que la formación en diapositivas: labs internos para probar prompt injection, retrieval poisoning, abuso de herramientas, service identities demasiado amplias y revocación de agentes.

Construye familias de roles en lugar de esperar que una persona lo sepa todo: AI security program lead, platform security owner, application security reviewer, SOC integration owner, identity and access partner, governance/risk partner y product security liaison. En organizaciones pequeñas una persona puede ocupar varios roles, pero los roles deben estar nombrados: "The team structure can be small, but the accountability map cannot be imaginary" (PDF p. 478).

Pistas de formación cruzada: Security→AI, AI→security, Platform→AI security y SOC→AI. Desarrollo de carrera con rutas junior, senior, lead, principal y management; la retención suele ser más barata que el reemplazo. Retención de conocimiento mediante decision records, playbooks, cross-training (al menos dos personas operan cada control crítico) y checklists de transición.

## Métricas y demostración de valor
Las métricas de seguridad de IA son menos maduras que las tradicionales: señales más ruidosas como calidad de defensa de prompts, tasa de bypass de guardrails, cobertura de tool-calls de agentes y drift de modelo/política. Usa las métricas como herramientas de dirección, no de decoración; el peligro es la falsa precisión (una cobertura "100 %" porque todos rellenaron un formulario). Familias de métricas: riesgo, cobertura, efectividad, agentes (inventario de identidades no humanas, exposición de permisos delegados, cobertura de allowlist de herramientas, éxito de pruebas de revocación) y mantenimiento (detecciones obsoletas, revisiones vencidas, frescura de documentación).

Calibración: las métricas son preguntas que requieren prueba periódica. Usa ejercicios (pruebas de prompt-injection, abuso de retrieval, drills de revocación de agentes, tabletops) para contrastar lo que afirma el dashboard. "If the dashboard says coverage is high but the drill cannot find the credential owner, the metric is lying politely" (PDF p. 480). Dashboards por audiencia: ejecutivo (salud, riesgos top, tendencia), operativo (colas, controles obsoletos, incidentes activos) y de practicante (profundidad técnica). El ROI es difícil de calcular con precisión, pero las estimaciones ayudan; gran parte del valor aparece como problemas que no ocurrieron.

## Colaboración entre funciones
El trabajo cruza data science, plataforma, producto, legal, compras, SOC, identidad y enterprise risk; un equipo central pequeño no puede poseerlo todo. La seguridad debe entrar temprano en la planificación de producto e ingeniería, preguntando qué capacidades, datos, modelos/proveedores, herramientas e identidades están implicados. La priorización basada en riesgo mantiene la relación sana.

Usar IA para sostener el programa: la automatización puede escanear roadmaps en busca de nuevas funciones de IA, resumir evidencia, redactar primeros borradores de threat models, marcar owners obsoletos, detectar drift de cobertura y recordar revisiones o pruebas de revocación vencidas. Debe ser soporte, no el dueño responsable:

- La automatización puede draft, classify, search, summarize, compare y remind.
- Los humanos aprueban el riesgo, otorgan privilegios, cierran hallazgos y aceptan la exposición residual.
- Cada automatización del programa necesita owner, scope, log y ruta de revocación (identidad no humana con alcance y cambios registrados).

Compromiso ejecutivo: visibilidad repetida, no todo el detalle técnico; briefing mensual de riesgo material, revisiones trimestrales de gobernanza y planificación anual de financiación.

## Gestión del cambio y cultura
Los controles y políticas solo funcionan si la gente puede seguirlos. La resistencia es una señal (carga de trabajo, autonomía, escepticismo, miedo al fallo) que indica dónde hace falta mejor herramienta, razón más clara o proceso menos doloroso. Cultura es "how people behave when nobody is checking" (PDF p. 483): equipos de producto que preguntan por los límites de retrieval antes del lanzamiento, ingenieros que piensan en la autoridad del agente antes de añadir una herramienta. Implementa el cambio pilotando con equipos receptivos, aprendiendo de la fricción e integrándolo en los flujos existentes.

## Adaptarse a la evolución del campo
El ritmo de tecnología, amenazas y regulación supera un refresco anual. Mantén estrategia anual y reporte ejecutivo trimestral, y añade revisión mensual o por evento para lanzamientos de modelos, frameworks de agentes, integraciones MCP/herramientas, cambios de proveedor, inteligencia de amenazas y actualizaciones regulatorias. El pensamiento basado en arquitectura dura más que la guía específica de proveedor: RAG crea riesgos de retrieval, datos y límites de prompt; los agentes crean riesgos de autoridad, herramientas, memoria y revocación; MCP y tool-servers crean riesgos de integración y autorización.

La inteligencia de amenazas debe alimentar acción: OWASP LLM, OWASP Agentic Top 10, MITRE ATLAS, informes de proveedores, incidentes internos y hallazgos de red-team deben convertirse en pruebas, detecciones, políticas y formación. "Reading the report is not the control. Changing the program is" (PDF p. 484).

Regulación y estándares: el EU AI Act se aplica progresivamente; NIST AI RMF, NIST CSF 2.0, ISO/IEC 27001 e ISO/IEC 42001 son anclas útiles. Para agentes, OWASP Agentic Top 10 y AIUC-1 ayudan a cruzar riesgos y controles. También la guía conjunta ACSC/CISA/NSA de 2026 y el SANS AI Security Maturity Model (que evita el "maturity theater" exigiendo etapas basadas en evidencia). Un "standards watch" debe ser aburrido a propósito: un owner que traduce cada cambio en actualizaciones de control, pruebas o la decisión de que no hace falta acción, registrando siempre la decisión (fuente monitoreada, cambio observado, controles afectados, acción o justificación de no actuar).

## Construir resiliencia del programa
- Planificación de sucesión: identificar roles clave cuya salida dañaría el programa (patrocinador ejecutivo, AI security lead, SOC integration owner, model gateway owner, agent identity owner, contacto legal/regulatorio, platform lead) y construir deputies antes de las salidas.
- Memoria institucional: decision records, retrospectivas de incidentes y proyectos, rationales de arquitectura, logs de excepciones y bases de conocimiento, para hacer recuperables las buenas decisiones.
- Preparación ante crisis: plantillas de comunicación, rutas de escalado, preservación de evidencia, procedimientos de revocación y planes de rollback preparados de antemano. Tabletops que incluyan compromiso de agente, prompt injection con acción de herramienta aguas abajo, fraude con deepfake de ejecutivo y presión de notificación regulatoria.
- Renovación continua: revisar misión, alcance, capacidades, métricas y efectividad con cadencia regular (estrategia anual, revisión ejecutiva trimestral, revisión mensual/por evento, after-action review tras cada incidente significativo).

Evidencia mínima viable: en cualquier momento el lead debe poder mostrar inventario actual de sistemas de IA, lista de alto riesgo, excepciones abiertas, controles obsoletos, inventario de identidades de agentes, aprendizajes de incidentes, decisiones del standards-watch y prioridades del próximo trimestre. "If that evidence cannot be produced, the program may still be busy, but it is not steerable" (PDF p. 487). Mejor un conjunto pequeño y actual que una gran base de conocimiento en la que nadie confía.

## Ideas clave
- La seguridad de IA es una disciplina operativa continua, no un proyecto de hardening único.
- Los programas fallan por cinco derivas: dependencia del campeón, fragilidad presupuestaria, atrofia de capacidades, aislamiento y deriva de autoridad.
- La deriva de autoridad se esconde en el éxito; exige revisión periódica de qué pueden causar hoy agentes e identidades no humanas y cuándo se probó la revocación.
- Modelos híbridos (función central + liaisons embebidos), charter claro y niveles de riesgo (Tier 1/2/3) sostienen el diseño organizativo.
- El talento se construye internamente con labs prácticos, familias de roles nombradas y retención de conocimiento; el accountability map no puede ser imaginario.
- Las métricas son herramientas de dirección que deben calibrarse con ejercicios; cuidado con la falsa precisión.
- La IA puede sostener el programa (draft, classify, summarize, remind), pero los humanos aprueban riesgo y privilegios; toda automatización necesita owner, scope, log y revocación.
- La resiliencia se logra con sucesión, memoria institucional, preparación ante crisis, renovación continua y un conjunto de evidencia mínima viable que mantenga el programa "steerable".
