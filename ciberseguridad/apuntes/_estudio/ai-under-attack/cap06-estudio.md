# Prompt Injection and Jailbreaking (Inyección de prompts y jailbreaking) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre por qué fallan las defensas tradicionales?
R: El lenguaje tiene un espacio de entrada efectivamente infinito: el atacante puede expresar la misma intención maliciosa de innumerables formas, mientras el defensor nunca puede enumerar todos los patrones peligrosos.

P: ¿Qué es el *linguistic adversarial space* y en qué se diferencia de los adversarial examples en visión?
R: Es el espacio adversario del lenguaje: a diferencia de visión, que requiere perturbar píxeles, los prompts adversarios son lenguaje normal; la intención es semántica, no sintáctica.

P: ¿Qué es la inyección directa de prompts y cuál es la raíz de su vulnerabilidad?
R: El atacante controla la entrada directamente para sobrescribir instrucciones o extraer contexto; la raíz es el contexto compartido: instrucciones del sistema y del usuario llegan como lenguaje en la misma ventana, sin frontera arquitectónica.

P: Nombra las técnicas de inyección directa de prompts.
R: Instruction override, role manipulation, delimiter confusion, token smuggling y context stuffing.

P: ¿Qué es la inyección indirecta de prompts y por qué es más peligrosa?
R: El atacante no toca el chat; envenena contenido que el sistema recupera después (web, documento, correo, registro, ticket, fuente RAG). Es más peligrosa porque el ataque llega sin contacto directo con la interfaz.

P: ¿Cuáles son las cuatro etapas de la cadena de inyección indirecta?
R: El atacante embebe instrucciones en contenido que controla; un usuario legítimo dispara la recuperación; el sistema coloca ese contenido en el contexto; el modelo sigue la instrucción embebida mientras aparenta responder la pregunta original.

P: ¿Qué es el RAG poisoning y por qué agrava el problema?
R: Es envenenar el knowledge base o índice vectorial; una vez dentro, el contenido malicioso afecta cada consulta futura que lo recupere, haciendo el problema persistente.

P: ¿En qué se diferencia el jailbreaking de la inyección de prompts?
R: La inyección suele sobrescribir las instrucciones de una aplicación concreta; el jailbreaking empuja al modelo fuera de los límites impuestos por su proveedor o despliegue, para que actúe como un sistema menos restringido.

P: Nombra las técnicas de jailbreaking descritas.
R: Persona, logical/hypothetical, multi-turn manipulation y encoding/obfuscation.

P: ¿Qué es "the keyword filtering illusion"?
R: La ilusión de que filtrar palabras clave protege: cada regla nueva atrapa una forma y deja abierto el resto del espacio semántico (p. ej. "disregard earlier directives", "let's start fresh").

P: ¿Qué aporta y qué no aporta el defensive prompt engineering?
R: Endurece los ataques y mejora el rechazo, pero sigue siendo texto; no da el aislamiento duro de las verificaciones de autorización, el sandboxing ni los controles de runtime separados.

P: ¿Qué componentes tiene un buen system prompt defensivo?
R: Separación estructural (instrucciones confiables vs. contenido no confiable), principios constitucionales, ejemplos few-shot de rechazo y meta-instrucciones sobre qué hacer ante intentos de override.

P: ¿Qué observa la detección en runtime y qué respuestas puede dar?
R: Monitorea entradas, contexto recuperado, salidas, llamadas a herramientas y patrones de conversación; puede registrar, advertir, añadir fricción, bloquear o usar circuit breakers que deshabilitan una función vulnerable mientras se parchea.

P: ¿Cuál es la diferencia entre failure modes y estrategias en las pruebas continuas?
R: Failure modes son los resultados dañinos (prompt extraction, instruction override, indirect instruction following, tool misuse, data exposure); estrategias son los métodos (authority framing, delimiter confusion, encoding, role pressure, many-shot, multi-turn, etc.). Bloquear una estrategia no prueba que el límite esté arreglado.

## Preguntas de autoevaluación

P: ¿Por qué un filtro de palabras clave fracasa como defensa primaria contra la inyección de prompts?
R: Porque el lenguaje ofrece infinitas formas equivalentes de expresar la misma intención; cada regla atrapa una forma y deja abierto el resto del espacio semántico. (Sección "Por qué fallan las defensas tradicionales")

P: ¿Qué hace que la inyección de prompts "democratice" el ataque frente a técnicas como SQL injection o buffer overflow?
R: Explotar SQL injection o buffer overflows exige conocimiento técnico; la inyección de prompts solo requiere habilidad conversacional, lo que amplía la población de atacantes. (Sección "El problema del espacio de entrada infinito")

P: ¿Por qué el prompt engineering no crea un verdadero límite de privilegios entre sistema y usuario?
R: Porque instrucciones del sistema y del usuario llegan como lenguaje en la misma ventana de contexto; el prompt influye en qué instrucción gana, pero no hay frontera arquitectónica entre ellas. (Sección "Mecánica de la inyección directa de prompts")

P: ¿Cuál es el trade-off inherente de la defensa contra la inyección indirecta?
R: Hay que tratar el contenido recuperado como no confiable (sanitización, límites de confianza, provenance, permisos), pero ninguna medida es perfecta porque la función misma requiere leer contenido externo. (Sección "Inyección indirecta de prompts")

P: ¿Por qué la eficacia de un jailbreak es inestable?
R: Un prompt que funciona hoy puede fallar tras una actualización del modelo, y una idea parcheada puede volver en otra forma; por eso debe respaldarse con controles de aplicación, monitoreo y pruebas continuas. (Sección "Técnicas de jailbreaking")

P: ¿Qué valor aportan los input classifiers aunque el modelo de producción esté comprometido?
R: Su valor está en la independencia: un modelo jailbroken aún debe pasar otra capa de clasificación antes de actuar. (Sección "Detección y respuesta en runtime")

P: ¿Por qué la unidad útil de prueba es el "caso" y no la cadena de ataque final?
R: Porque el comportamiento es probabilístico; el caso captura el flujo probado, el canal de entrada, el límite cruzado, la estrategia de presión, la autoridad invocada, la capacidad en riesgo y la evidencia, permitiendo pruebas continuas y reproducibles. (Sección "Pruebas y validación continua")

P: ¿Cómo se debe usar el trabajo público de jailbreak (p. ej. Pliny) de forma segura?
R: Como señal de campo: estudiar la forma, quitar el exploit vivo y reconstruir el patrón de presión como regression case inofensivo. (Sección "Pruebas y validación continua")

## Checklist

- [ ] Etiquetar estructuralmente en el system prompt las instrucciones confiables frente al contenido no confiable (p. ej. USER_DATA tratado como datos, no como instrucciones).
- [ ] Incluir en el system prompt un límite explícito de rechazo y una meta-instrucción sobre qué hacer ante intentos de override.
- [ ] Tratar todo contenido recuperado (web, documentos, correos, fuentes RAG) como no confiable: sanitización, límites de confianza por fuente, filtrado de recuperación, provenance y control de acceso.
- [ ] Limitar permisos de herramientas de modo que una instrucción embebida no pueda escalar capacidades.
- [ ] Desplegar capas independientes de detección en runtime: input classifiers, semantic analysis y behavioral monitoring (fuga de system prompt, topic drift, uso inusual de herramientas).
- [ ] Definir respuestas graduadas: registrar, añadir fricción (verificación extra, rate limits), bloquear en alta confianza y preparar circuit breakers para funciones vulnerables.
- [ ] Probar los prompts defensivos contra ataques reales antes del despliegue: variantes, muestras de inyección indirecta e intentos multi-turno.
- [ ] Separar failure modes de estrategias al diseñar las pruebas y convertir cada ataque exitoso de red team en un regression test.
- [ ] Mantener una librería de ataques con categoría, flujo objetivo, criterio de éxito, resultado de detección, versión de modelo/prompt y estado de remediación.
- [ ] Medir attack detection rate, false positive rate, response latency, coverage e impacto en usabilidad en la misma revisión.
- [ ] Combinar automatización (prompt fuzzing, JailbreakBench, PromptInject, OWASP, Giskard) con red teams humanos.
- [ ] Alinear con guía vigente: OWASP LLM guidance y la guía conjunta CISA/ASD ACSC/NSA sobre IA agéntica.
