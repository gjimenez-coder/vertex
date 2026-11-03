# AI Red Teaming and Evaluation (Red teaming y evaluación de IA) — Estudio

## Tarjetas de repaso

P: ¿Qué omitió el pentest tradicional del sistema de préstamos con IA pese a reportar veintitrés hallazgos?
R: Que el razonamiento de la IA era explotable solo mediante lenguaje; cuatro días tras el lanzamiento una consulta logró que revelara su system prompt completo, con criterios de scoring y ponderación demográfica.

P: ¿Cuál es la tesis central del capítulo?
R: Existe una brecha entre la validación de seguridad tradicional y las amenazas específicas de IA, y esa brecha crea una falsa confianza.

P: ¿Qué valida el pentest tradicional (las "table stakes")?
R: Infraestructura, autenticación, autorización, manejo de API y la aplicación que envuelve al modelo: servicios parcheados, llamadas autenticadas, validación de entrada, logs y despliegue endurecido.

P: ¿Por qué el pentest omite los ataques de IA?
R: Porque usan entradas válidas e interfaces legítimas; el fallo es semántico y de comportamiento: el sistema sigue la instrucción equivocada, confía en el contexto equivocado o encadena herramientas hacia un resultado no autorizado.

P: ¿Cuál es el desajuste fundamental entre pentest y AI red teaming?
R: El pentest pregunta si el código puede explotarse de forma determinista; el AI red teaming pregunta si un sistema probabilístico puede manipularse de forma fiable (un jailbreak puede funcionar el 80% del tiempo y fallar distinto según modelo y contexto).

P: ¿Qué perfiles componen un programa de red team de IA?
R: AI security researchers, ingenieros de seguridad tradicional, especialistas en prompts/lenguaje, expertos de dominio e ingenieros de automatización; el modelo puede ser interno, externo, purple-team o bug bounty.

P: Según el capítulo, ¿cuándo una herramienta pertenece al límite de seguridad?
R: "Si el agente puede llamar a una herramienta, esa herramienta es parte del límite de seguridad" (PDF p. 286) y entra en el alcance de las pruebas.

P: ¿Cómo debe tratarse el trabajo público de jailbreaks (ej. Pliny/elder-plinius)?
R: Como señal, no como librería de payloads: estudiar la forma, eliminar el contenido de exploit en vivo y reconstruir el patrón de presión como caso de prueba inofensivo con respuesta segura esperada.

P: ¿Qué aporta la automatización frente a las pruebas manuales?
R: Volumen, consistencia y cobertura de regresión en cada release, actualización de modelo, cambio de corpus o integración de herramienta; lo manual descubre ataques nuevos. El programa necesita ambos.

P: ¿Por qué un atacante automatizado no debe tener acceso a producción?
R: Porque "un atacante automatizado con acceso a producción no es una herramienta de pruebas; es un riesgo no gestionado" (PDF p. 290); requiere contención: entornos aislados, límites de llamadas y logs.

P: ¿Qué métricas capturan el riesgo real de seguridad de IA?
R: Attack Success Rate (ASR), Time to Successful Attack (TTSA), tasas de bypass de defensas y métricas de cobertura por superficie (prompt, memoria, RAG, agente, integridad, herramientas).

P: ¿Cuál es la ponderación por defecto de riesgo compuesto y qué advertencia la acompaña?
R: 40/20/30/10 entre ASR, false positive rate, coverage gap y TTSA; es un valor por defecto, no una constante validada, y debe recalibrarse según el perfil de riesgo.

P: ¿Qué marcos de la industria se usan como capa de mapeo?
R: MITRE ATLAS, OWASP Top 10 para LLM y aplicaciones de IA generativa, NIST AI RMF y Generative AI Profile (NIST AI 600-1), y el SANS AI Security Maturity Model.

P: ¿Cuál es el único trabajo del reporte de red team?
R: Convertir la evidencia adversarial en cambio; "un exploit hermoso que nunca se convierte en corrección es teatro" (PDF p. 293).

P: ¿Cuáles son los cuatro niveles del modelo de madurez de red teaming?
R: Nivel 1 reactivo, Nivel 2 estructurado (charter, cadencia, alcance), Nivel 3 continuo (críticos bloquean despliegue, correcciones como regresiones) y Nivel 4 cultural (threat modeling antes del lanzamiento).

## Preguntas de autoevaluación

P: ¿Por qué el pentest "minucioso y profesional" generó falsa confianza en el caso del sistema de préstamos?
R: Validó la cáscara (infra, API, autenticación) y encontró cero vulnerabilidades críticas en código, pero se detuvo antes de los lugares donde la IA decide, dejando el razonamiento explotable solo con lenguaje. (El ejemplo que recorre el capítulo / Por qué el red teaming tradicional falla frente a la IA)

P: Explica por qué la evidencia en AI red teaming se mide de forma distinta a la del pentest.
R: Porque el sistema es probabilístico: un ataque como un jailbreak puede funcionar el 80% del tiempo, mejorar iterando y fallar distinto según modelo y contexto, así que se usan ASR, TTSA, cobertura y robustez en lugar de un conteo determinista. (Por qué el red teaming tradicional falla frente a la IA / Métricas de evaluación)

P: ¿Qué debe definir el alcance y las reglas de enfrentamiento de un programa de red team de IA?
R: El alcance nombra endpoints de modelo, fuentes RAG, memory stores, herramientas de agentes, modelos fine-tuned y entornos de evaluación; las reglas definen ventanas de tiempo, escalado, rate limits, manejo de datos, salvaguardas de producción, condiciones de parada y aprobaciones de alto riesgo. (Construir un programa de red team de IA)

P: ¿Qué se prueba por cada superficie de ataque en el trabajo manual?
R: Prompt/injection (señales de autoridad, delimitadores, role frames, codificaciones, multi-turno), memory/RAG (persistencia y confianza, documentos maliciosos en recuperación), agentes (tool abuse, goal hijacking, parameter injection, sandbox escape) e integridad del modelo (triggers de backdoor, extracción, datos memorizados). (Técnicas manuales de red team)

P: ¿Por qué una seguridad que bloquea toda petición maliciosa puede no ser un control válido?
R: Porque si destruye el flujo legítimo "no es un control; es un fallo de producto" (PDF p. 291); por eso se miden funcionalidad: falsos positivos, impacto en latencia, throughput y tasa de completado de tareas. (Métricas de evaluación)

P: ¿Cómo se usan los marcos de la industria respecto a las pruebas?
R: Como capa de mapeo que traduce hallazgos al lenguaje que la organización conoce y ayuda a enrutar y comparar, pero no reemplazan las pruebas; el hallazgo debe explicar la ruta real, el sistema afectado, el impacto y la corrección. (Marcos y estándares de la industria)

P: ¿Qué información debe acompañar a un hallazgo para que impulse remediación?
R: Dueño, severidad, pasos de reproducción, corrección esperada, prueba de validación, estado de despliegue y evidencia de cierre, registrado en el sistema de ingeniería (Jira, GitHub Issues, Azure DevOps, registro de riesgos). (Reporte y remediación)

P: ¿Qué distingue al Nivel 4 (cultural) del modelo de madurez?
R: Se hace threat modeling de las features de IA antes del lanzamiento y la evidencia moldea la arquitectura, frente al Nivel 3 continuo donde los críticos bloquean despliegue y las correcciones se vuelven regresiones. (Práctica continua de red team)

## Checklist

- Mantener el pentest tradicional como "table stakes": validar infra, autenticación, autorización, manejo de API y la app que envuelve al modelo.
- Componer el equipo con investigación de seguridad de IA, ingeniería de seguridad, especialistas en prompts, expertos de dominio y automatización.
- Definir alcance explícito: endpoints de modelo, fuentes RAG, memory stores, herramientas de agentes, modelos fine-tuned y entornos de evaluación.
- Incluir cada herramienta que un agente pueda llamar dentro del límite de seguridad y del alcance de pruebas.
- Fijar reglas de enfrentamiento: ventanas de tiempo, contactos de escalado, rate limits, manejo de datos, salvaguardas de producción, condiciones de parada y aprobaciones de alto riesgo.
- Ajustar la cadencia a la velocidad de cambio: continua en commits/releases, manual semanal/por sprint, inmersiones periódicas y pruebas por evento ante cambios de arquitectura, modelos, corpus, herramientas o incidentes.
- Probar manualmente cada superficie: prompt/injection, memory/RAG, agentes (autoridad, credenciales, parámetros) e integridad del modelo.
- Tratar el trabajo público de jailbreaks como señal: reconstruir la estrategia como caso de prueba inofensivo con respuesta segura esperada.
- Documentar cada hallazgo para que sea reproducible: superficie, payloads/secuencia, estado del sistema, tool calls, contexto recuperado, salida, criterios de éxito, severidad, afectados, corrección y prueba de regresión.
- Automatizar con fuzzers/harnesses y benchmarks (Garak, DeepEval, CleverHans, JailbreakBench, HarmBench) tratándolos como ayudas de medición, no como prueba de seguridad.
- Integrar las pruebas en CI/CD donde puedan bloquear cambios malos: merge requests, release gates, regresiones programadas, actualizaciones de modelo, cambios de corpus y despliegues de herramientas.
- Contener los agentes de red team con IA: entornos aislados, límites de llamadas, logs de ataques exitosos y revisión de políticas aprendidas; nunca darles acceso a producción.
- Rastrear métricas de ASR, TTSA, bypass de defensas, cobertura, funcionalidad (falsos positivos, latencia, throughput, completado) y robustez (transferencia, adaptativos, novedosos).
- Calcular riesgo compuesto con la ponderación por defecto 40/20/30/10 y recalibrarla según el perfil de riesgo del sistema.
- Reportar por audiencia: vista ejecutiva, de ingeniería y de cumplimiento, siempre con acción asociada.
- Enrutar hallazgos al sistema de ingeniería con dueño y convertir cada corrección validada en prueba de regresión.
- Medir la remediación: time to acknowledge, time to fix, tasa de validación, recurrencia de regresión y hallazgos reabiertos.
- Hacer crecer la práctica por el modelo de madurez (reactivo → estructurado → continuo → cultural) y el SANS AI Security Maturity Model.
