# Defensive Prompt Engineering (Ingeniería de prompts defensiva) — Estudio

## Tarjetas de repaso

P: ¿Qué es el defensive prompt engineering y qué línea de defensa representa?
R: Es la Línea 1 de defensa; opera dentro de la interacción con el modelo dándole jerarquía de instrucciones, fronteras del contenido no confiable y reglas de rechazo antes de que entren datos recuperados o salidas de herramientas.

P: ¿Cuál es el orden de autoridad que establece un prompt defensivo?
R: Reglas de sistema > instrucciones de desarrollador > peticiones de usuario; el contenido externo (documentos, tickets, páginas, correos, salidas de herramientas) es evidencia a analizar, no autoridad a obedecer.

P: ¿Cuáles son las tres líneas de defensa de un sistema de IA?
R: Línea 1: defensive prompt engineering; Línea 2: runtime guardrails (filtran entradas, documentos recuperados, llamadas a herramientas y salidas); Línea 3: supervisión humana para decisiones donde la automatización no basta.

P: ¿Por qué el valor de las capas es redundancia y no "teatro aritmético"?
R: Porque las capas fallan de modos distintos: los prompts fallan cuando el lenguaje engaña al modelo; los guardrails cuando los clasificadores pierden la intención; la revisión humana cuando las reglas de escalado o los revisores malinterpretan el riesgo.

P: Según el UK NCSC, ¿por qué prompt injection no es SQL injection?
R: Porque el modelo no impone una frontera dura entre datos e instrucciones.

P: ¿Qué cubre OWASP LLM01:2025?
R: Trata prompt injection, directa e indirecta, como riesgo central.

P: ¿Cuáles son los tres niveles de la jerarquía de instrucciones?
R: Prioridad 1: reglas de seguridad y autorización que el modelo no debe anular; Prioridad 2: rol, alcance, tono y flujos de trabajo aprobados; Prioridad 3: input de usuario y contenido recuperado, marcados como no confiables salvo verificación de otro sistema.

P: ¿Qué sostiene la evaluación "Lost in the Middle" y cómo afecta al diseño del prompt?
R: Que los modelos rinden mejor con la información relevante al inicio o final del contexto, lo que respalda poner las reglas de mayor prioridad donde el modelo más las usará.

P: ¿Por qué hay que escapar el markup provisto por el usuario al usar marcadores de frontera?
R: Porque sin escapar, un atacante puede cerrar tu etiqueta y abrir un bloque de instrucciones falso.

P: ¿Cómo debe ser el lenguaje de rechazo según el capítulo?
R: "Calm and boring": reconoce la petición, declina la manipulación y sigue ayudando con la tarea legítima.

P: ¿Qué es el post-prompting (sandwich defense) y cuándo es más útil?
R: Invierte el orden colocando el contenido no confiable primero y las instrucciones al final ("content first, authority last"); ayuda más con ataques cortos y tareas simples, y es más débil en ataques largos, multi-turno o muy contextuales.

P: ¿Qué dos cosas se miden a la vez al testear prompts defensivos?
R: Qué sigue pasando (bypass) y qué peticiones útiles se bloquean por error (falsos positivos).

P: ¿Cuándo se considera segura una respuesta durante el testing?
R: Solo si el atacante no logra el resultado prohibido; una respuesta no es segura por sonar educada.

P: ¿Qué problema cierra la prompt compression resistance?
R: Cierra una brecha de extracción: los atacantes no piden el prompt verbatim, sino que el modelo resuma, liste o describa sus reglas (divulgación parafraseada).

P: ¿Por qué "signed instructions" no es una firma de seguridad real?
R: Son marcadores distintivos alrededor de bloques confiables; es reconocimiento de patrones, no verificación criptográfica.

## Preguntas de autoevaluación

P: ¿Qué hace que el ataque del asistente de soporte supere las defensas tradicionales y por qué el prompt es el primer lugar para reducir el riesgo?
R: La instrucción peligrosa no llega como un exploit obvio, sino escondida dentro de contenido que el asistente está instruido a confiar; por eso el primer lugar para reducir el riesgo es hacer que el modelo entienda que las reglas de seguridad pesan más que cualquier cosa hallada en contenido de usuario o recuperado. (Sección: Lo que necesitas saber)

P: ¿Qué NO reemplaza el defensive prompting?
R: No es magia ni un motor de políticas, ni reemplaza guardrails de runtime, chequeos de permisos, filtros de salida, monitoreo ni revisión humana; su trabajo es hacer que el modelo esté menos dispuesto a tratar texto hostil como autoridad. (Sección: Lo que necesitas saber)

P: En el ejemplo hilo conductor, ¿qué es un falso positivo y por qué importa?
R: Si el asistente rechaza a un usuario legítimo que pide resumir el último paso de troubleshooting solo porque "summarize" aparece cerca de un ataque previo, la defensa es demasiado burda; eso es un falso positivo que inutiliza al asistente. (Sección: El ejemplo que recorre el capítulo)

P: ¿Qué deben lograr las meta-instrucciones contra ataques comunes y qué categorías debe reconocer el modelo?
R: Enseñan cómo luce la manipulación nombrando la categoría y describiendo el rechazo, manteniendo ejemplos amplios para no dar un catálogo de exploits; el modelo debe reconocer intentos de anular instrucciones, extraer el system prompt, inventar una persona nueva, colar directivas codificadas o construir una petición riesgosa en varios turnos. (Sección: Meta-instrucciones contra ataques comunes)

P: ¿Cuáles son las cuatro partes del bucle de testing?
R: Una suite de ataques reutilizable, un sandbox que no afecte producción, métricas de éxito de ataque y falsos positivos, y control de versiones de cada cambio de prompt. (Sección: Testing de los prompts defensivos)

P: ¿Cómo se eligen las técnicas avanzadas de endurecimiento?
R: No se adoptan todas; se eligen dos o tres según los riesgos de la aplicación, porque añaden defensas puntuales contra ataques que explotan multi-turno, deriva de políticas, incertidumbre o extracción de prompt. (Sección: Técnicas avanzadas de endurecimiento)

P: ¿Qué debe ocurrir si falla el retrieval en una retrieval-augmented safety?
R: Debe fallar en cerrado (fail closed). (Sección: Técnicas avanzadas de endurecimiento)

P: ¿Qué debe definir la plantilla de producción cuando el prompt y el flujo discrepan?
R: Debe definir la conducta correcta, que no es un workaround creativo sino rechazo o escalado atado a la ruta aprobada; muchos prompts se vuelven "mushy" diciendo "be helpful and safe" sin definir qué significa ser útil ante una acción fuera de alcance. (Sección: Plantilla de producción)

## Checklist

- Declarar primero las reglas inmutables de seguridad y autorización que el modelo no debe anular.
- Definir identidad, alcance, tareas aprobadas y ruta de escalado del asistente.
- Nombrar categorías de manipulación a rechazar sin listar un gran catálogo de exploits.
- Insertar input y contenido recuperado dentro de marcadores de frontera, escapando el markup provisto por el usuario.
- Terminar el prompt recordando que las reglas confiables superan lo que haya dentro del bloque no confiable.
- Especificar formato de respuesta, expectativas de citación y comportamiento ante la incertidumbre.
- Definir la conducta cuando prompt y flujo discrepan: rechazo o escalado atado a la ruta aprobada, no un workaround.
- Poner las reglas de mayor prioridad al inicio o final del contexto (según "Lost in the Middle").
- Construir una librería de ataques reutilizable: overrides directos, indirect injection, explotación de role-play, extracción de prompt, trucos de codificación y construcción de contexto multi-turno.
- Ejecutar la suite en un sandbox con el mismo prompt, herramientas, fuentes de retrieval y guardrails de producción.
- Definir el éxito de ataque antes de probar y rastrear los falsos positivos por separado.
- Realimentar los fallos confirmados al prompt, la suite y, si hace falta, a guardrails o fine-tuning.
- Configurar la retrieval-augmented safety para que falle en cerrado (fail closed).
- Defender contra la extracción parafraseada (resumir/describir reglas), no solo contra la fuga verbatim.
- Diseñar asumiendo que algunas defensas a nivel de prompt fallarán, sobre todo cuanto más consecuentes sean las acciones del sistema.
