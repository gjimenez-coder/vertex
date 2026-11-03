# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 2 — Threat Modeling AI Systems (Modelado de amenazas en sistemas de IA)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF entre paréntesis.

## Lo que necesitas saber

Los fallos de seguridad en IA rara vez se limitan a los pesos del modelo: surgen de la arquitectura que lo rodea —qué datos puede acceder el modelo, qué herramientas puede invocar, qué permisos hereda y cómo se tratan sus salidas—. La superficie de ataque real está en la intersección de capacidad del modelo, acceso a datos y orquestación de herramientas. Si un agente procesa entrada no confiable y además tiene acceso de escritura a una base de datos, eso es un problema de diseño que los filtros de prompt no arreglan; hace falta flujos de datos claros, mejores límites de sesión y lógica de autorización más estricta.

El modelado de amenazas (threat modeling) da a ingenieros, científicos de datos, product owners, seguridad y cumplimiento una visión compartida de cómo funciona el sistema, dónde están los límites de confianza (trust boundaries) y cómo podría fallar. Permite tomar decisiones de seguridad antes de producción: dónde restringir el acceso del modelo, separar datos confiables de no confiables, exigir aprobación humana, monitorear abuso y aceptar riesgo residual. Es la práctica de examinar sistemáticamente un sistema para identificar cómo podría ser atacado o sacado de su comportamiento previsto antes de fijar el diseño.

Sales sabiendo aplicar frameworks clásicos (STRIDE, PASTA, OCTAVE) extendidos a riesgos de IA, una receta de siete pasos para modelar amenazas, cómo correr un taller colaborativo, qué herramientas usar, los errores comunes y las "quick wins", y cómo medir el éxito. El caso StyleBot recorre todo el proceso de principio a fin.

## El ejemplo que recorre el capítulo

StyleBot es un chatbot minorista que recomienda productos por conversación natural (el cliente dice "necesito un vestido para una boda en la playa" y el bot recomienda, responde sobre tallas y materiales, y da consejos de estilo). Arquitectura: frontend React + SDKs móviles; API Gateway (autenticación y rate limiting); servicio de orquestación en Node.js; integración con Azure OpenAI; base vectorial Pinecone con embeddings de producto; catálogo PostgreSQL con inventario en tiempo real; Session Store en Redis; pipeline de analítica. Escala: 50.000 usuarios activos diarios, 2 millones de productos, media de 8 mensajes por conversación, disponibilidad 24/7. El consejo: léelo como patrón, no como plantilla —"scope first, diagram second, threats third, controls only after the team agrees on what can go wrong" (PDF p. 85).

## Entender el modelado de amenazas

Todo sistema tiene puntos débiles; la pregunta es si los encuentras tú primero o los atacantes. La disciplina precede al software: los bancos siempre preguntaron "How might someone rob us?" (PDF p. 70) para diseñar la bóveda. Modelar en la fase de planificación da dos ventajas: coste (un arreglo en un diagrama es mucho más barato que en producción) y cultura de prevención (la seguridad pasa de "gatekeeper" reactivo a requisito arquitectónico fundacional).

El buen modelado hace tres cosas: encuentra vulnerabilidades mientras el arreglo sigue siendo un cambio de diseño; da a quienes construyen, operan y aprueban el sistema el mismo mapa; y genera evidencia de que las decisiones fueron deliberadas.

### Frameworks consolidados

- STRIDE (Microsoft, introducido en 1999): Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Simple y enseñable en diez minutos.
- OCTAVE: enfoque basado en activos y riesgo.
- PASTA: simulación de ataques y análisis de riesgo centrado en el impacto al negocio (proceso de siete etapas).

No hay método único que sirva para todo; los equipos combinan partes según sistema, riesgos y detalle. Para profundizar en métodos clásicos el libro cita *Threat Modeling: Designing for Security* (Adam Shostack) y *Threat Modeling Best Practices* (Derek Fisher, Packt, 2025), y el artículo del SEI de Carnegie Mellon sobre doce métodos. El objetivo aquí es aplicar lo convencional a un sistema de IA real.

## Superficies de ataque específicas de IA

- LLM application security: manejo de prompts, context engineering (cómo se ensamblan instrucciones, fuentes recuperadas, memoria, herramientas y estado de sesión), manejo de salidas y comportamiento inseguro del modelo.
- Agentic security: uso de herramientas, permisos, memoria, delegación y acción multi-paso.
- Integridad de entrenamiento y modelo: poisoning, backdoors, robo y drift.
- RAG y privacidad: donde se cruzan recuperación, embeddings, logs, memoria y control de acceso.
- Riesgo de protocolo e integración de herramientas: donde el modelo alcanza sistemas externos en vez de solo generar texto.

### Prompt injection y manejo inseguro de salidas

El prompt injection ocurre cuando instrucciones controladas por el atacante influyen en lo que hace el modelo, sobrescribiendo o confundiendo las instrucciones previstas. A diferencia de ataques de inyección tradicionales que explotan errores de parseo, explota la naturaleza misma de los LLM: siguen instrucciones y no distinguen de forma fiable las tuyas de las del atacante. El indirect prompt injection no requiere acceso directo: se envenenan las fuentes que la IA lee (documentos, webs, correos, registros de BD) con instrucciones ocultas. Los fallos de output handling amplifican: si el modelo genera JavaScript malicioso y la app lo renderiza sin sanitizar, se crea un XSS "con pasos extra". (Prompt injection se profundiza en el capítulo 6.)

### Data poisoning y robo de modelo

Con suficiente influencia sobre los datos de entrenamiento, un atacante puede moldear el comportamiento del modelo, incluyendo patrones inseguros o triggers ocultos. El poisoning puede venir de un pipeline comprometido o de fuentes internas usadas para fine-tuning (logs, tickets, documentos, transcripciones, repositorios). Los ataques de backdoor son especialmente insidiosos: el trigger es raro, el modelo rinde bien en pruebas y el atacante lo activa a voluntad. El robo de modelo: el atacante envía consultas cuidadas y usa las respuestas para entrenar un modelo que imita el tuyo; los model inversion attacks reconstruyen partes del conjunto de entrenamiento. (Ataques en tiempo de entrenamiento: capítulo 11.)

### Fuga de privacidad

Ocurre cuando el modelo expone información sensible presente en entrenamiento, fine-tuning, prompts, logs o sistemas conectados. Los modelos pueden memorizar datos con exactitud inquietante, "from phone numbers to API keys to personal emails" (PDF p. 76). Casos típicos: reutilizar chat logs sensibles para entrenamiento, añadir documentos internos a un sistema de recuperación sin control de acceso, o guardar prompts/salidas en logs accesibles por demasiada gente. Los membership inference attacks determinan si un dato estuvo en el entrenamiento; los extraction attacks reconstruyen datos verbatim. (Privacidad en RAG: capítulo 8.)

### Riesgos de agentes autónomos

Los agentes cambian el modelo de amenaza porque operan en múltiples pasos bajo permisos delegados: persiguen objetivos, llaman APIs, deciden y actúan. El agent hijacking convierte asistentes útiles en armas digitales; el tool abuse amplifica el riesgo cuando se combinan navegación web, ejecución de código y acceso a APIs; los sistemas multi-agente añaden comportamientos emergentes que nadie comprende del todo. (Vulnerabilidades de agentes: capítulo 9; arquitectura Zero Trust: capítulo 18.)

## Receta de siete pasos

1. **Definir alcance y objetivos.** Delimita qué proteges; elige un caso de uso desplegado. Mal alcance: "Our AI initiatives"; buen alcance: un chatbot concreto en Azure con Azure OpenAI integrado con Salesforce CRM. Escribe qué debe hacer y qué nunca debe hacer (requisitos de seguridad), documenta supuestos explícitos ("la mitad de los incidentes vienen de supuestos violados que nadie verificó"), y define éxito con metas medibles. Time-box: una hora.
2. **Dibujar un data-flow diagram simple.** Entidades externas como rectángulos fuera del límite; componentes principales conectados con flechas etiquetadas por tipo de dato; trust boundaries con líneas punteadas (donde se implementan controles); incluir data stores (los atacantes atacan datos en reposo tanto como en tránsito). "A diagram that fits on a whiteboard is more useful than a 50-page architecture document" (PDF p. 79).
3. **Aplicar STRIDE + amenazas de IA.** Recorre cada componente/conexión. En cada entrada de usuario: spoofing, tampering y el "AI special" prompt injection. En la API del modelo: information disclosure, DoS, model extraction. En data stores: tampering (poisoning), information disclosure, repudiation. Sé específico. Añade amenazas de IA que no encajan: hallucination exploits, jailbreaking, adversarial examples, behavioral drift por feedback envenenado.
4. **Estimar impacto y probabilidad.** Escala simple 1-3 (bajo/medio/alto), multiplicar para un score de 1-9. No debatas horas si algo es 2 o 3: es priorización aproximada, no precisión.
5. **Elegir controles.** Cuatro categorías: *Guardrails* (system prompts que resisten override, constitutional AI, firewalls semánticos); *Filtering* (filtros de entrada/salida); *Access rules* (rate limits, autenticación, restricción de capacidades —leer del CRM pero no escribir); *Monitoring* (logs de prompts y respuestas, alertas por patrones inusuales). Documenta por qué cada control y qué amenaza cubre. (Guardrails: capítulo 16.)
6. **Documentar preguntas abiertas y riesgo residual.** Incertidumbres irreducibles y amenazas que quedan tras los controles; documenta qué riesgo es aceptable para guiar la respuesta a incidentes.
7. **Programar revisiones y disparadores.** Son documentos vivos. Taller completo para sistema nuevo/lanzamiento de alto riesgo/cambio mayor de arquitectura; revisión ligera (30 min) para trabajo ordinario; actualización por trigger (cambia el modelo, se amplían fuentes de recuperación, una herramienta gana permisos, hay un incidente, aparece una técnica nueva o cambia la regulación). La propiedad queda en producto e ingeniería; seguridad asesora y reta.

## Taller de modelado de amenazas

Invita 6-8 personas que entre todas entiendan cada aspecto del sistema: ingeniería con profundidad (quien escribió las plantillas de prompt, quien integró la base vectorial, quien depura el serving), product owners, científicos de datos, seguridad (guía pero no domina), y legal/cumplimiento. Para mantener el foco: empieza por el alcance, no por las amenazas; usa un "parking lot" para lo importante pero fuera de tema; time-box la identificación de amenazas (30 min sin discutir soluciones); prohíbe detalles de implementación durante la discusión de amenazas; usa ejemplos reales, no abstracciones.

Agenda de dos horas (Tabla 2.1): contexto (0:00-0:10), brainstorming de amenazas con sticky notes silenciosos (0:10-0:40), aplicar STRIDE (0:40-1:00), descanso (1:00-1:10), priorización con votación y matriz de riesgo (1:10-1:30), brainstorming de controles solo top 3-5 (1:30-1:50), próximos pasos y dueños (1:50-2:00). Evita: Security Theater, Perfection Trap, Expert Monopoly y Scope Creep.

## Caso StyleBot paso a paso

- **Paso 1 (alcance):** En scope: interacciones del chatbot, flujo de búsqueda/recomendación, integración con catálogo e inventario, gestión de sesión. Fuera: pagos, fulfillment, autenticación (SSO existente). Requisitos: no revelar datos de un cliente a otro, no ser manipulado para recomendar productos inapropiados, no permitir extracción de algoritmos de precios, mantener disponibilidad en eventos de ventas.
- **Paso 2 (DFD):** Figura 2.8 con trust boundaries e indicadores STRIDE por componente.
- **Paso 3 (STRIDE + IA, Tabla 2.2):** 16 amenazas, p. ej. T2 spoof de contexto admin vía prompt injection, T3 descripciones de producto envenenadas, T8 revelar patrones de compra de otros clientes, T9 prompt injection extrae el system prompt con reglas de negocio, T11 prompts caros agotan la cuota de Azure OpenAI, T13 recomendar artículos restringidos, y AI-específicas T14-T16 (adversarial inputs, model drift sesgando, alucinaciones de features inexistentes).
- **Realidad en producción (agente regulado):** un agente de leasing de gestión inmobiliaria muestra que el modelo conversacional casi no tiene herramientas; la capa de orquestación las tiene todas y porta credenciales permanentes. STRIDE revela: disclosure/escalada entre inquilinos (el servicio confía en IDs del request sin verificar propiedad); tampering de una decisión regulada vía prompt injection (el guardrail es una sola instrucción en lenguaje natural sin filtro determinista ni clasificador de salida); y disclosure de datos personales (atributos sensibles en el payload y logs sin redacción). Dos controles que merecen crédito: retirar la IA para usuarios en estado de cuenta sensible, pero "when the status lookup errors, the code fails open" (PDF p. 90). Lección: una función de IA acoplada a una plataforma con credenciales y registros sensibles hereda toda su postura de seguridad; la capa de integración debe estar en el centro del diagrama (Paso 2).
- **Paso 4 (scoring, Tabla 2.3):** impacto × probabilidad = 1-9; T2 y T3 marcan 9.
- **Paso 5 (controles):** T2/T9 (prompt injection): plantilla con delimitadores claros, jerarquía de instrucciones, filtros regex, monitoreo de fragmentos del system prompt en salidas. T11 (agotamiento): rate limit por usuario (10 req/min), scoring de complejidad, circuit breakers, caché. T8 (fuga): sanitizar salidas por PII, filtrar patrones de compra, auditar respuestas.
- **Paso 6:** preguntas abiertas (frecuencia de actualización de Azure OpenAI, detectar alucinaciones, embeddings corruptos de Pinecone); riesgos aceptados y dependencias.
- **Paso 7:** semanal (métricas), mensual (nuevas técnicas de prompt injection), trimestral (revisión completa), triggers. Trade-offs: caché con 5 min de desfase de inventario; límite de 500 tokens; logs completos pero IDs de usuario hasheados; Azure OpenAI simplifica seguridad pero crea dependencia de proveedor.

## Herramientas

- **Manuales:** whiteboards + sticky notes (fotografía todo), spreadsheets/wikis (columnas: ID, descripción, categoría STRIDE, impacto, probabilidad, controles, dueño), Microsoft Threat Modeling Tool (gratis, plantillas STRIDE, interfaz anticuada y cobertura de IA mínima), Draw.io/Lucidchart.
- **Plataformas automatizadas:** MITRE ATLAS (base de conocimiento de tácticas y técnicas adversarias contra sistemas de IA, útil como vocabulario de amenazas); OWASP GenAI Security Project (cubre LLM, GenAI y riesgos agénticos); herramientas integradas al workflow (diseño, diagramas, control de código, tickets, gates de revisión).
- **Selección (Tabla 2.4):** empieza con whiteboards y spreadsheets para crear memoria muscular; añade herramientas pesadas solo cuando reduzcan fricción, mejoren trazabilidad o mantengan el modelo actualizado.

## Errores comunes y quick wins

Pitfalls: sobredimensionar el primer modelo ("Ambition kills more threat models than laziness", PDF p. 95 — empieza pequeño); ignorar a los humanos en el bucle (inclúyelos: "Hurried analyst accepts model recommendation without validation"); tratar los controles como tareas únicas (define quién los actualiza, con qué frecuencia y evidencia); y liderazgo que dice "security by design" pero solo financia features.

Quick wins: habilitar logging hoy (prompts, respuestas, decisiones de control —"You cannot detect attacks you do not record", PDF p. 96); añadir rate limiting esta semana; crear una biblioteca de plantillas de prompt versionadas con instrucciones de seguridad; correr una revisión de amenazas a la hora del almuerzo ("What is the worst thing someone could make our AI do?"); documentar los system prompts como código.

## Qué es el éxito

Indicadores de un modelo vivo: historial de revisiones que cambia cuando cambia el sistema; que no solo seguridad edite (ingenieros, data scientists y PMs también); y que en los design reviews alguien pregunte "How does this change our attack surface?". Señales de deterioro: baja asistencia y delegados junior, lenguaje que pasa de escenarios específicos y aterradores a abstracciones vacías, y pipelines nuevos (p. ej. RAG) que no aparecen en el modelo. Alineación con el negocio (Figura 2.10): métricas según prioridad —confianza del usuario (tickets/quejas de seguridad), innovación (velocidad de despliegue seguro), coste (incidentes evitados), industrias reguladas (horas de auditoría ahorradas).

## Ideas clave

- La superficie de ataque real está en la intersección de capacidad del modelo, acceso a datos y orquestación de herramientas; los problemas suelen ser de diseño, no de filtros de prompt.
- STRIDE y PASTA son la base, pero necesitan extensiones de IA: prompt injection, data poisoning, abuso de recuperación y manipulación de agentes.
- La receta de siete pasos: alcance → DFD → STRIDE+IA → scoring → controles → riesgo residual → revisiones.
- Los controles de IA se agrupan en guardrails, filtering, access rules y monitoring; cada uno debe documentar qué amenaza cubre.
- Prompt injection explota que los LLM siguen instrucciones y no distinguen las del usuario de las del atacante; el indirecto envenena las fuentes que la IA lee.
- Un buen Paso 3 nombra tanto los controles acertados como las amenazas, y pregunta "qué pasa cuando esta verificación falla" (un control que falla abierto es su propia amenaza).
- Cuando una función de IA se acopla a una plataforma con credenciales y datos sensibles, hereda toda su postura de seguridad: pon la capa de integración en el centro del diagrama.
- El modelo de amenazas es un documento vivo y una habilidad, no un proyecto único: empieza con un sistema real y mantenlo al día.
