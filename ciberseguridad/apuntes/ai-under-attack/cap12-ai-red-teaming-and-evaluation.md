# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 12 — AI Red Teaming and Evaluation (Red teaming y evaluación de IA)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El capítulo parte de un caso real: una firma de seguridad hizo un pentest de tres semanas a un sistema de recomendación de préstamos con IA, reportó veintitrés hallazgos (cabeceras faltantes, librerías desactualizadas) y declaró el sistema seguro. Cuatro días tras el lanzamiento, una única consulta cuidadosamente diseñada logró que la IA revelara su system prompt completo, incluyendo criterios de scoring de riesgo y factores de ponderación demográfica. El pentest tradicional "simplemente probó las cosas equivocadas": encontró cero vulnerabilidades críticas en el código mientras el razonamiento de la IA era completamente explotable solo con lenguaje.

La tesis central es que existe una brecha entre la validación de seguridad tradicional y las amenazas específicas de IA, y esa brecha crea una falsa confianza. El pentest valida la "cáscara" alrededor del sistema (infraestructura, autenticación, API), pero se detiene antes de los lugares donde la IA toma decisiones: prompt injection, memory poisoning, manipulación de RAG, abuso de herramientas de agentes y compromiso en tiempo de entrenamiento.

El AI red teaming existe para cerrar esa brecha de validación antes de que lo hagan los adversarios o los usuarios en producción. El capítulo sintetiza los Capítulos 6 al 11 en una metodología de pruebas sistemática. Sales sabiendo cómo construir un programa de red team de IA (composición, alcance, cadencia), técnicas manuales y automatizadas, métricas de evaluación adecuadas a fallos probabilísticos, los marcos de la industria, y cómo convertir hallazgos en remediación. Cierra la Parte 2; la Parte 3 convierte los hallazgos del red team en arquitectura de blue team.

## El ejemplo que recorre el capítulo
El hilo conductor es el sistema de préstamos con IA de la firma financiera. El pentest tradicional fue "minucioso y profesional" pero falló: "La seguridad tradicional encontró cero vulnerabilidades críticas en código, pero omitió que el razonamiento de la IA era explotable solo mediante lenguaje" (PDF p. 282). Este contraste ilustra toda la lógica del capítulo: lo que el pentest valida, lo que omite, y por qué se necesita una disciplina de pruebas distinta.

## Por qué el red teaming tradicional falla frente a la IA
El pentest tradicional sigue importando: valida infraestructura, autenticación, autorización, manejo de API y la aplicación que envuelve al modelo. Esos controles son "table stakes" (lo mínimo).

- **Lo que el pentest valida:** servicios parcheados, llamadas API autenticadas, validación de entrada, logs de eventos y despliegue endurecido.
- **Lo que omite:** los ataques de IA usan entradas válidas e interfaces legítimas. El prompt es sintácticamente correcto, el documento recuperado es un archivo normal, la llamada a herramienta usa una API permitida. El fallo es semántico y de comportamiento: el sistema sigue la instrucción equivocada, confía en el contexto equivocado o encadena herramientas hacia un resultado no autorizado.
- **El desajuste fundamental:** el pentest pregunta si el código puede explotarse de forma determinista; el AI red teaming pregunta si un sistema probabilístico puede manipularse de forma fiable. "Un jailbreak puede funcionar el 80 por ciento del tiempo, mejorar iterando y fallar de forma distinta" según modelos y contexto (PDF p. 284). La evidencia debe medirse de otra manera. El coste de ignorarlo es falsa confianza.

## Construir un programa de red team de IA
No es un ejercicio puntual de un tester astuto. Es una forma repetible de definir autoridad, elegir sistemas, probar las superficies correctas, documentar evidencia e impulsar correcciones en ingeniería.

- **Composición:** mezcla de investigación en seguridad de IA, ingeniería de seguridad tradicional, experiencia en prompts/lenguaje, conocimiento de dominio y automatización. Los AI security researchers traducen papers a pruebas; los ingenieros de seguridad cubren infra y aplicación; los especialistas en prompts exploran manipulación lingüística; los expertos de dominio saben cómo luce el abuso real (médico, financiero, legal); los ingenieros de automatización convierten ataques exitosos en pruebas repetibles. El modelo puede ser interno, externo, purple-team o bug bounty.
- **Alcance, autorización y reglas de enfrentamiento:** el alcance nombra endpoints de modelo, fuentes RAG, memory stores, herramientas de agentes, modelos fine-tuned y entornos de evaluación. "Si el agente puede llamar a una herramienta, esa herramienta es parte del límite de seguridad" (PDF p. 286). Las reglas de enfrentamiento definen ventanas de tiempo, contactos de escalado, rate limits, manejo de datos, salvaguardas de producción, condiciones de parada y aprobaciones de pruebas de alto riesgo.
- **Cadencia:** debe coincidir con la velocidad de cambio. Pruebas continuas en commits/releases; sesiones manuales semanales o por sprint para ataques novedosos; inmersiones periódicas para validar cobertura; pruebas por evento tras cambios de arquitectura, nuevos modelos, nuevos corpus de recuperación, nuevas herramientas o incidentes.

## Técnicas manuales de red team
El trabajo manual aporta creatividad humana. No se trata de repetir los Capítulos 6-11 en miniatura, sino de convertir esas categorías de ataque en un plan de pruebas para el sistema concreto.

**Pruebas por superficie de ataque:**
- **Prompt e injection:** empezar con patrones conocidos como JailbreakBench, familias tipo DAN y prompts generados estilo PAIR, y adaptarlos. La evidencia incluye qué señales de autoridad, delimitadores, role frames, codificaciones o secuencias multi-turno cambian el comportamiento del modelo.
- **Memory y RAG:** buscar fallos de persistencia y confianza. ¿Un historial de conversación envenenado altera el comportamiento futuro? ¿Un documento malicioso entra al set de recuperación, se posiciona por encima del contenido legítimo o inyecta instrucciones ocultas?
- **Agentes:** seguir la autoridad. Mapear cada herramienta, sus credenciales, parámetros y acciones; luego probar tool abuse, goal hijacking, parameter injection, propagación multi-agente, sandbox escape y cadenas de acciones no autorizadas. La guía conjunta de 2026 sobre adopción cuidadosa de servicios agénticos de IA refuerza que el acceso a herramientas, credenciales delegadas, identidades de agentes, logs, aprobaciones y rutas de revocación están en el alcance.
- **Integridad del modelo:** usualmente conductual, no basada en exploits. Probar triggers de backdoor, respuestas anómalas, patrones de extracción y datos sensibles memorizados.

Sobre el trabajo público de jailbreaks (ej. Pliny/elder-plinius): tratarlo como señal, no como librería de payloads. "Estudia la forma, elimina el contenido de exploit en vivo y reconstruye el patrón de presión como un caso de prueba inofensivo" con respuesta segura esperada (PDF p. 288). El objetivo es identificar la estrategia detrás (authority framing, role pressure, encoding, confusión de delimitadores, escalado multi-turno, colocación indirecta) y adaptarla.

**Documentar hallazgos:** un hallazgo sirve solo si otro equipo puede reproducirlo y corregirlo. Capturar: superficie, payloads/secuencia exacta, estado del sistema, tool calls, contexto recuperado, salida del modelo, criterios de éxito, severidad, usuarios/datos afectados, corrección recomendada y una prueba de regresión que demuestre que la corrección aguanta.

## Pruebas adversariales automatizadas
Lo manual descubre ataques nuevos pero no cubre cada release, actualización de modelo, cambio de corpus o integración de herramienta. La automatización da volumen, consistencia y cobertura de regresión. El programa necesita ambos.

- **Tooling y benchmarks:** fuzzers y harnesses generan grandes volúmenes de prompts adversariales, entradas malformadas y secuencias de tool-call. Ejemplos: **Garak** y **DeepEval**; frameworks clásicos como **CleverHans** siguen útiles para pruebas de la era de clasificadores/adversarial-ML. Benchmarks como **JailbreakBench** y **HarmBench** comparan el comportamiento del modelo en el tiempo; el trabajo de NIST sobre evaluación de *agent hijacking* apunta a pruebas más sistemáticas. Tratar los benchmarks como ayudas de medición, no como prueba de que un sistema es seguro.
- **Integración CI/CD:** las pruebas deben correr donde puedan bloquear cambios malos: merge requests, release gates, regresiones programadas, actualizaciones de modelo, cambios de corpus y despliegues de herramientas. Los resultados deben ser artefactos de pipeline, tickets de remediación y métricas de tendencia.
- **Agentes de red team con IA:** exploran el espacio de ataque más rápido que los humanos pero requieren contención estricta: entornos aislados, límites de llamadas, logs de ataques exitosos y revisión de políticas aprendidas. "Un atacante automatizado con acceso a producción no es una herramienta de pruebas; es un riesgo no gestionado" (PDF p. 290).

## Métricas de evaluación para seguridad de IA
Un simple conteo de vulnerabilidades oculta el riesgo real. Las métricas deben capturar fallo probabilístico, profundidad defensiva, compromisos de usabilidad y cobertura.

- **A rastrear:** Attack Success Rate (con qué frecuencia las entradas adversariales logran el objetivo), Time to Successful Attack, tasas de bypass de defensas, y métricas de cobertura (qué superficies de prompt, memoria, RAG, agente, integridad y herramientas se probaron).
- **Funcionalidad:** falsos positivos, impacto en latencia, reducción de throughput y tasa de completado de tareas. "Seguridad que bloquea toda petición maliciosa destruyendo el flujo legítimo no es un control; es un fallo de producto" (PDF p. 291).
- **Robustez:** resistencia a ataques de transferencia, resistencia a ataques adaptativos (cuando el red team aprende de intentos fallidos) y desempeño frente a ataques novedosos.
- **Riesgo compuesto sin falsa precisión:** una ponderación por defecto razonable es **40/20/30/10** entre ASR, false positive rate, coverage gap y TTSA, pero es un valor por defecto, no una constante validada. Recalibrar según perfil de riesgo (los sistemas de cara al cliente pueden pesar más los falsos positivos; los de agentes de alto privilegio, las acciones no autorizadas; los regulados, la evidencia de cobertura).
- **Reporte por audiencia:** vista ejecutiva (riesgo global, principales issues por impacto, puntos go/no-go, recursos), vista de ingeniería (ASR por categoría, controles evadidos, brechas de cobertura, prioridades de remediación) y vista de cumplimiento (cobertura, puntajes de benchmark, metodología y evidencia mapeadas a los marcos comprometidos). Las métricas sin acción son desperdicio.

## Marcos y estándares de la industria
Los marcos traducen hallazgos al lenguaje que la organización ya conoce; no reemplazan las pruebas.

- **MITRE ATLAS:** vocabulario de técnicas de amenaza para ataques de IA.
- **OWASP Top 10 para LLM y aplicaciones de IA generativa:** taxonomía práctica que incluye prompt injection, divulgación de información sensible, vulnerabilidades de supply chain, data y model poisoning, manejo indebido de salidas, excessive agency, fuga de system prompt, debilidades de vectores/embeddings, misinformation y consumo ilimitado.
- **NIST AI RMF y Generative AI Profile (NIST AI 600-1):** traducen la evidencia del red team a gobernanza y tratamiento de riesgo, alimentando las funciones Govern, Map, Measure y Manage.

Usar los marcos como capa de mapeo: el hallazgo debe explicar la ruta de explotación real, el sistema afectado, el impacto y la corrección; la etiqueta del marco solo ayuda a enrutar y comparar.

## Reporte y remediación
El reporte tiene un trabajo: convertir la evidencia adversarial en cambio. "Un exploit hermoso que nunca se convierte en corrección es teatro" (PDF p. 293).

- **Estructura:** resumen ejecutivo (riesgo global, conteo de hallazgos críticos, impacto de negocio, plazos) y sección técnica (alcance, métodos, payloads, comportamiento del modelo, contexto recuperado, tool calls, evidencia y pasos de reproducción). La severidad refleja explotabilidad, blast radius, sensibilidad de datos, autonomía del sistema afectado y si puede bloquear el despliegue.
- **Críticos:** compromiso total del sistema, exposición irrestricta de datos sensibles, RCE en producción, bypass de seguridad a escala o acciones de agente con daño real de negocio.
- **Impulsar remediación:** los hallazgos entran al sistema de ingeniería (Jira, GitHub Issues, Azure DevOps, registro de riesgos) con dueño, severidad, reproducción, corrección esperada, prueba de validación, estado de despliegue y evidencia de cierre. El red team valida la corrección y la convierte en prueba de regresión.
- **Métricas de remediación:** time to acknowledge, time to fix, tasa de validación, recurrencia de regresión y hallazgos reabiertos. Revelan si el red teaming mejora la seguridad o solo produce reportes más alarmantes.

## Práctica continua de red team
El red teaming maduro es una práctica, no un evento anual.

- **Modelo de madurez:** Nivel 1 reactivo (pruebas tras incidentes, hallazgos en hojas de cálculo); Nivel 2 estructurado (charter, cadencia, alcance, cobertura básica); Nivel 3 continuo (pruebas automáticas y manuales en el ciclo de vida, los críticos bloquean despliegue, correcciones como regresiones); Nivel 4 cultural (threat modeling de features de IA antes del lanzamiento, evidencia que moldea la arquitectura). El **SANS AI Security Maturity Model** separa la madurez entre proteger IA, usar IA y gobernar IA.
- **Mentalidad adversarial:** enseñar a los ingenieros cómo se manifiestan prompt injection, memory poisoning, manipulación de RAG, abuso de herramientas y fallos de integridad en sus propios sistemas; unir red y blue team durante los ataques; post-mortems sin culpa; alimentar lecciones en revisiones de diseño, estándares de código, gobernanza de recuperación y modelos de permisos de agentes.
- **Colaboración:** participar en foros de seguridad de IA, aportar casos de prueba seguros, coordinar divulgación y comparar contra benchmarks públicos.

## Ideas clave
- El pentest tradicional valida la "cáscara" del sistema de IA; el AI red teaming valida el comportamiento interno: instrucciones, contexto, recuperación, memoria, herramientas, agentes e integridad del modelo.
- Los ataques de IA usan entradas válidas e interfaces legítimas; el fallo es semántico y probabilístico, por eso la evidencia se mide con ASR, TTSA, cobertura, robustez y métricas de funcionalidad.
- Si un agente puede llamar a una herramienta, esa herramienta pertenece al límite de seguridad y al alcance de las pruebas.
- Combinar creatividad manual (descubrir fallos nuevos) con automatización (regresión y volumen); nunca dar a un atacante automatizado acceso a producción.
- El trabajo público de jailbreaks es señal, no librería de payloads: reconstruir la estrategia como caso de prueba inofensivo con respuesta segura esperada.
- Marcos (MITRE ATLAS, OWASP Top 10 LLM, NIST AI RMF/600-1, SANS Maturity Model) son capa de mapeo, no sustituto de la evidencia.
- El reporte debe producir cambio: hallazgos con dueño, corrección validada y convertida en regresión; medir time to fix, recurrencia y reaperturas.
- La madurez evoluciona de reactiva a cultural; el cierre del capítulo conecta la Parte 2 (superficies de ataque) con la Parte 3 (arquitectura de blue team).
