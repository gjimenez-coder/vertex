# Building Sustainable AI Security Programs (Construir programas de seguridad de IA sostenibles) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre la seguridad de IA?
R: No es un proyecto puntual de hardening, sino una disciplina operativa continua ("AI security is not a one-time hardening project. It is an operating discipline").

P: ¿Por qué fallan realmente los programas de seguridad de IA?
R: No por un control técnico equivocado, sino porque la organización los trata como un proyecto de lanzamiento en vez de como un sistema operativo: se financian, anuncian, documentan y luego se dejan pudrir.

P: ¿Cuáles son los cinco modos de deriva que degradan un programa?
R: Dependencia del campeón, fragilidad presupuestaria, atrofia de capacidades, aislamiento y deriva de autoridad.

P: ¿Qué es la dependencia del campeón (champion dependency) y cómo se contrarresta?
R: El programa parece sano mientras ciertas personas permanecen y se estanca cuando se van; se contrarresta institucionalizando: documentar por qué se tomaron las decisiones, quién posee cada control, qué métricas prueban el valor y cómo se aprueban las excepciones.

P: ¿Por qué es peligrosa la deriva de autoridad (authority drift)?
R: Porque "se esconde dentro del éxito" ("hides inside success"): tokens o permisos temporales de pilotos siguen activos sin que nadie recuerde por qué; exige revisión periódica de identidades y herramientas y pruebas de revocación/rollback.

P: ¿Qué distingue a los tres niveles de riesgo (tiers) del programa?
R: Tier 1 es uso interno de bajo riesgo sin autoridad de acción; Tier 2 es workflow de negocio con datos sensibles, recuperación o impacto en clientes; Tier 3 es IA agéntica o expuesta externamente con uso de herramientas, acceso de escritura, credenciales delegadas o exposición regulatoria.

P: ¿Qué modelo organizativo suele funcionar mejor para la sostenibilidad?
R: Un modelo híbrido: una función central que fija estándares y métricas (evita la deriva) y liaisons embebidos en producto, plataforma, datos y operaciones que hacen el trabajo práctico (evitan la abstracción).

P: ¿Qué es el charter del programa?
R: Un documento corto y práctico que indica qué posee la seguridad de IA y qué no: alcance de revisión, niveles de riesgo, autoridad para exigir evidencia, ruta de escalado y artefactos operativos mínimos.

P: ¿Qué perfiles componen el equipo de seguridad de IA?
R: No solo investigadores de ML; también security engineers, software engineers, platform engineers, SOC engineers, identity engineers y especialistas de ML/datos, porque muchos sistemas son workflows agénticos, retrieval, APIs de proveedores, copilots, orquestación y servidores MCP.

P: ¿Qué significa la frase "The team structure can be small, but the accountability map cannot be imaginary"?
R: El equipo puede ser reducido y una persona ocupar varios roles, pero los roles (familias de roles) deben estar nombrados; la rendición de cuentas no puede ser imaginaria.

P: ¿Cómo deben usarse las métricas de seguridad de IA?
R: Como herramientas de dirección, no de decoración; se calibran con ejercicios (pruebas de prompt-injection, abuso de retrieval, drills de revocación, tabletops) para evitar la falsa precisión.

P: ¿Qué reparto de responsabilidad hay entre automatización y humanos al usar IA para sostener el programa?
R: La automatización puede draft, classify, search, summarize, compare y remind; los humanos aprueban el riesgo, otorgan privilegios, cierran hallazgos y aceptan la exposición residual. Cada automatización necesita owner, scope, log y ruta de revocación.

P: ¿Qué aporta el pensamiento basado en arquitectura frente a la guía específica de proveedor?
R: Dura más: RAG crea riesgos de retrieval, datos y límites de prompt; los agentes crean riesgos de autoridad, herramientas, memoria y revocación; MCP y tool-servers crean riesgos de integración y autorización.

P: ¿Qué marcos y estándares cita el capítulo como anclas?
R: OWASP LLM, OWASP Agentic Top 10, MITRE ATLAS, NIST AI RMF, NIST CSF 2.0, ISO/IEC 27001, ISO/IEC 42001, AIUC-1, la guía conjunta ACSC/CISA/NSA de 2026 y el SANS AI Security Maturity Model.

P: ¿En qué consiste la evidencia mínima viable?
R: Que en cualquier momento el lead pueda mostrar inventario de sistemas de IA, lista de alto riesgo, excepciones abiertas, controles obsoletos, inventario de identidades de agentes, aprendizajes de incidentes, decisiones del standards-watch y prioridades del próximo trimestre; si no, el programa no es "steerable".

## Preguntas de autoevaluación

P: ¿Qué características definen a un programa de seguridad de IA sostenible?
R: Sobrevive a cambios de liderazgo, presión presupuestaria, rotación de personal, cambio de modelos, adopción de agentes y movimiento regulatorio; mantiene los controles actualizados sin depender de un campeón heroico, hace visible su valor a ejecutivos, es práctico para ingenieros y distribuye la responsabilidad. (Sección "Lo que necesitas saber")

P: ¿Cómo se debe responder a la fragilidad presupuestaria sin recurrir al "fear theater"?
R: Conectando los controles a resultados que los ejecutivos entienden: reducción de incidentes, aprobaciones más rápidas, menor exposición regulatoria y lanzamientos seguros. (Sección "Por qué fallan los programas de seguridad de IA")

P: ¿Por qué no basta con las líneas de reporte (CISO, tecnología o chief AI officer) para asegurar el éxito?
R: Ninguna opción es universalmente correcta; lo erróneo es dar responsabilidad sin acceso, autoridad ni presupuesto. Las líneas de reporte deben evaluarse por los derechos operativos que habilitan. (Sección "Diseño organizativo para la sostenibilidad")

P: ¿Cómo se construye y retiene el talento cuando el campo aún se está formando?
R: Partiendo de las brechas de habilidades en vez de títulos ideales, priorizando el trabajo práctico (labs internos), creando familias de roles nombradas, pistas de formación cruzada y desarrollo de carrera; la retención suele ser más barata que el reemplazo y el conocimiento se retiene con decision records, playbooks, cross-training y checklists de transición. (Sección "Construir y retener talento")

P: ¿Qué quiere decir "If the dashboard says coverage is high but the drill cannot find the credential owner, the metric is lying politely"?
R: Que una métrica puede dar falsa precisión; los ejercicios y drills deben contrastar lo que afirma el dashboard, porque una cobertura alta en papel no significa control real. (Sección "Métricas y demostración de valor")

P: ¿Qué cadencia de adaptación propone el capítulo frente a la evolución del campo?
R: Estrategia anual y reporte ejecutivo trimestral, más una revisión mensual o por evento para lanzamientos de modelos, frameworks de agentes, integraciones MCP/herramientas, cambios de proveedor, inteligencia de amenazas y actualizaciones regulatorias. (Sección "Adaptarse a la evolución del campo")

P: ¿Qué significa que la inteligencia de amenazas debe "alimentar acción"?
R: Que OWASP, MITRE ATLAS, informes de proveedores, incidentes internos y hallazgos de red-team deben convertirse en pruebas, detecciones, políticas y formación: "Reading the report is not the control. Changing the program is". (Sección "Adaptarse a la evolución del campo")

P: ¿Qué cuatro pilares construyen la resiliencia del programa?
R: Planificación de sucesión (deputies para roles clave), memoria institucional (decision records, retrospectivas, rationales, logs), preparación ante crisis (plantillas, escalado, preservación de evidencia, revocación, rollback y tabletops) y renovación continua con cadencia regular. (Sección "Construir resiliencia del programa")

## Puntos a dominar

- Explicar por qué la seguridad de IA es una disciplina operativa y no un proyecto de hardening único.
- Reconocer los cinco modos de deriva y proponer la contramedida de cada uno.
- Detectar deriva de autoridad revisando qué pueden causar hoy agentes e identidades no humanas y cuándo se probó por última vez la revocación.
- Clasificar un sistema de IA en Tier 1, Tier 2 o Tier 3 según datos, impacto y autoridad de acción.
- Distinguir qué puede hacer la automatización (draft, classify, search, summarize, compare, remind) de lo que debe hacer un humano (aprobar riesgo, otorgar privilegios, cerrar hallazgos, aceptar exposición residual).
- Verificar que toda automatización del programa tenga owner, scope, log y ruta de revocación.
- Mapear riesgos por arquitectura: RAG (retrieval/datos/prompt), agentes (autoridad/herramientas/memoria/revocación), MCP y tool-servers (integración/autorización).
- Comprobar que exista evidencia mínima viable actual que mantenga el programa "steerable".
