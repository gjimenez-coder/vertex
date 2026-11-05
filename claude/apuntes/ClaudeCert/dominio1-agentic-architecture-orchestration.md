# Claude Certified Architect – Foundations (CCA-F) — Anthropic (guía de examen, 2026)

## Dominio 1 — Agentic Architecture & Orchestration (Arquitectura agéntica y orquestación)

> Nota de extracción: este apunte combina cinco fuentes: la guía en PDF «Tutorials Dojo Study Guide and Cheat Sheets – Claude Certified Architect Foundations (CCA-F)», las slides en PDF del curso en video (Tutorials Dojo, junio 2026), el banco de 77 preguntas de práctica «Claude Certified Architect. Foundations: Practice Exam» y las lecciones web de claudecertificationguide.com (sitio independiente de terceros, no afiliado a Anthropic). Citas: `(Guía PDF p. N)` y `(Slides PDF p. N)` usan la página del PDF; `(web N.M)` remite a la lección N.M de la web; `(QN)` remite a la pregunta N del banco. Si las fuentes se contradicen, prevalecen la guía y el banco sobre la web. Las slides tienen muchas páginas que son solo imagen y no se pudieron leer, por lo que su cobertura es parcial. Discrepancia entre fuentes sin resolver: el banco y la guía llaman al examen «CCA-F» y el banco indica 77 preguntas de práctica y una nota mínima de 720 (escala 100-1.000); la web lo llama «CCAR-F» e indica 60 preguntas en 120 minutos, aprobado con 720/1.000 y credencial válida 12 meses. No se decide cuál es la correcta.

## Lo que necesitas saber

El Dominio 1 cubre el diseño de sistemas agénticos con Claude: desde el agentic loop básico hasta la orquestación multiagente, el enforcement determinista, la descomposición de tareas y la gestión de sesiones. Pesa el 27% del examen. Parte del agentic loop, un control de flujo determinista en código que se repite mientras `stop_reason` sea `"tool_use"` y termina con `"end_turn"` (Tarea 1.1; web 1.1; Guía PDF p. 46).

Sobre ese loop se construyen los sistemas multiagente. En el patrón hub-and-spoke, el coordinator decide qué trabajo existe, particiona el alcance, agrega resultados y es responsable de la salida final (Tarea 1.2; Guía PDF p. 48; Slides PDF p. 103). La Tarea 1.3 baja a la mecánica de invocar subagents: "Task"/"Agent" en `allowedTools`, AgentDefinition, contexto pasado de forma explícita porque no hay herencia automática, metadatos separados del contenido, spawning paralelo en una sola respuesta, y fork_session frente a `--resume` (web 1.3; Guía PDF p. 52; Q18; Q19; Q20).

Las Tareas 1.4 y 1.5 tratan de la frontera entre lo probabilístico y lo determinista: la prompt guidance dice qué debería hacer Claude; la programmatic enforcement (prerequisite gates y hooks PreToolUse/PostToolUse) controla qué puede hacer. Cuando un solo fallo implica pérdida financiera, riesgo de seguridad o de compliance, el examen espera enforcement programático, mientras que PostToolUse sirve para normalizar datos antes de que el modelo los procese (Guía PDF p. 54; web 1.4; web 1.5; Q21; Q24). Las Tareas 1.6 y 1.7 completan el dominio: elegir entre un pipeline fijo (prompt chaining) y la descomposición dinámica según las características de la tarea, evitar la attention dilution con pases locales más un pase de integración, y gestionar sesiones largas con `--resume`, fork_session, scratchpad files y subagents (web 1.6; Q26; Q27; Guía PDF p. 62-63).

Sales sabiendo reconocer qué mecanismo corresponde a cada escenario y descartar los distractores típicos: señales de parada en lenguaje natural o topes de iteraciones, comunicación directa entre subagents, prompts en lugar de gates, PostToolUse para bloquear, y `/clear` o re-exploración completa cuando basta un re-análisis dirigido. Las tareas marcadas como prioridad de estudio son la 1.4 (salvaguardas de la capa de orquestación: resolución o escalación) y la 1.6 (descomposición dinámica de tareas).

## Tarea 1.1 — Design and implement agentic loops for autonomous task execution (Diseñar e implementar agentic loops para la ejecución autónoma de tareas)

### Agentic loop (el ciclo de ejecución del agente)

**Concepto:** el agentic loop es el ciclo de ejecución central de todo agente basado en Claude: control de flujo determinista definido en código, no un truco de prompt, ni un retry loop, ni un turno de chatbot (web 1.1). Claude recibe el prompt, evalúa el estado, solicita tools, recibe los resultados y repite hasta producir una respuesta sin tool calls (Guía PDF p. 36; Guía PDF p. 44).

Claude no ejecuta la tool que defines: su respuesta pide la llamada, tu código ejecuta la función y devuelve el resultado; un agente es Claude, sus tools y el código que continúa ese intercambio (web 1.1).

**Ejemplos de uso (3, cortos):**
1. Agente de una vidriería: `tool_use` para buscar el pedido, `tool_use` para consultar la agenda de montajes y `end_turn` con la respuesta al cliente (web 1.1).
2. Arreglar tests de autenticación: ejecutar tests, leer archivos, editar el código, volver a ejecutar tests y devolver un resumen final (Guía PDF p. 43; Guía PDF p. 44).
3. Ciclo en las slides: Respond → Act → Observe → Repeat, que permite adaptarse a nueva información (Slides PDF p. 3).

**Qué NO hacer:**
- No tratarlo como un truco de prompt, un retry loop ni un turno de chatbot: es control de flujo determinista en código (web 1.1).
- No considerarlo una interacción de una sola petición/respuesta cuando hay tools: una tarea puede necesitar varios turnos y cada turno cambia lo que Claude sabe (Guía PDF p. 44).

**Posible confusión con otros conceptos:**
- Flujo tradicional (workflow fijo) — la aplicación ya conoce la secuencia (cliente → pedido → política → reembolso); en el agentic loop Claude decide el siguiente paso tras ver resultados intermedios (Guía PDF p. 41; Guía PDF p. 44).

### Ciclo de vida del loop (cuatro pasos)

**Concepto:** el loop se repite hasta que Claude termina: (1) enviar la petición a la Messages API con el historial (system prompt, mensajes previos y tool results de la iteración anterior); (2) inspeccionar `stop_reason`; (3) si es `"tool_use"`, ejecutar las tools y añadir los resultados al historial como un mensaje nuevo, y volver a enviar; (4) si es `"end_turn"`, presentar la respuesta final (web 1.1).

**Ejemplos de uso (3, cortos):**
1. Cada iteración llama a `client.messages.create()` dentro de un `while` y comprueba `response.stop_reason` (web 1.1).
2. Con `tool_use`: se ejecutan las tools, se añaden el mensaje del assistant y el de los resultados, y se llama de nuevo al modelo (Guía PDF p. 46; Slides PDF p. 20).
3. Con `end_turn`: se extrae el texto final y se sale del loop (web 1.1; Slides PDF p. 25).

```python
messages = [{"role": "user", "content": user_query}]

while True:
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=messages,
        tools=tools
    )

    if response.stop_reason == "tool_use":
        tool_results = execute_tools(response.content)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
    elif response.stop_reason == "end_turn":
        return response
    else:
        return handle_other_stop_reason(response)
```
(Guía PDF p. 46)

### stop_reason como señal de control

**Concepto:** `stop_reason` es la señal autoritativa y determinista que indica por qué Claude dejó de generar y si el loop debe ejecutarse de nuevo (web 1.1). Forma parte de toda respuesta exitosa y es distinto de un fallo de la API (Guía PDF p. 45). `"tool_use"` significa continuar el loop; `"end_turn"` significa terminar y devolver la respuesta final (web 1.1; Guía PDF p. 45).

**Ejemplos de uso (3, cortos):**
1. `tool_use`: Claude pide ejecutar una o más client tools y "espera que las ejecutes" (Guía PDF p. 45; Slides PDF p. 27).
2. `end_turn`: Claude terminó de forma natural, es la ruta normal de salida; hay que manejarla explícitamente (Slides PDF p. 25; Slides PDF p. 26).
3. Un `end_turn` vacío tras un `tool_result` suele ser un bug de formato del mensaje (por ejemplo, texto extra tras los resultados), no un fallo de razonamiento (Guía PDF p. 45; Guía PDF p. 46).

**Qué NO hacer:**
- No salir del loop justo después de `tool_use`: detiene al agente a mitad de tarea (Slides PDF p. 21; Slides PDF p. 29).
- No comprobar solo `tool_use` e ignorar `end_turn`: el sistema puede seguir iterando o lanzar errores en respuestas válidas (Slides PDF p. 26).
- No asumir que cualquier valor distinto de `end_turn` es `tool_use`: tratarlo como "no terminado, revisar por qué" (web 1.1).

### Otros valores de stop_reason

**Concepto:** el examen (guía v1.0) evalúa `tool_use` y `end_turn`, pero la Messages API también devuelve `pause_turn`, `max_tokens`, `stop_sequence`, `refusal` y `model_context_window_exceeded`, y un loop de producción debe manejarlos (web 1.1).

**Ejemplos de uso (3, cortos):**
1. `max_tokens`: la respuesta se cortó por el límite de tokens; hay que continuar la generación o devolver un error/respuesta parcial, nunca tratarla como terminada (Slides PDF p. 19; Slides PDF p. 30; Slides PDF p. 31).
2. `stop_sequence`: el modelo encontró una cadena de parada definida en la petición; normalmente se trata como `end_turn`, extrayendo el contenido anterior a la secuencia (Slides PDF p. 32; Slides PDF p. 33).
3. `pause_turn` significa continuar un turno largo de server-tool; `refusal` significa que Claude se negó a responder y es una respuesta HTTP 200 normal, no un error; `model_context_window_exceeded` se maneja como el truncamiento por `max_tokens` (web 1.1).

**Posible confusión con otros conceptos:**
- `max_tokens` — corte por límite de tokens; no es finalización natural como `end_turn` (Slides PDF p. 30).
- `refusal` — Claude declinó responder; no es un error de la API (web 1.1).

### Devolver tool results y actualizar el historial

**Concepto:** el paso 3 es donde fallan los loops: el código debe añadir los tool results al historial; si no, el modelo nunca ve lo que devolvió la tool y no tiene nada nuevo sobre lo que razonar (web 1.1; Guía PDF p. 46). Sin esa actualización no hay loop real (Guía PDF p. 45).

**Ejemplos de uso (3, cortos):**
1. Extraer todos los bloques `tool_use` (no solo el primero) con su nombre, input e ID único, y conservar el ID para vincular el resultado (Slides PDF p. 37; Slides PDF p. 38).
2. Añadir primero la respuesta completa del assistant tal como la devolvió la API (texto y bloques `tool_use`) y después los resultados como bloques `tool_result` en un único mensaje `user` (Slides PDF p. 40; Slides PDF p. 43).
3. Cada `tool_result` lleva `type: "tool_result"` y un `tool_use_id` que debe coincidir exactamente con el del bloque `tool_use` original (Slides PDF p. 44; Slides PDF p. 51).

**Qué NO hacer:**
- No omitir los tool results del historial: el modelo pierde contexto y solicita repetidamente la misma tool (Slides PDF p. 6; Slides PDF p. 29).
- No insertar texto antes de los `tool_result` ni narrativa innecesaria: los `tool_result` van primero en el array `content`, el texto solo después, y el resultado debe seguir inmediatamente al mensaje `tool_use`; de lo contrario la API puede devolver un error 400 (Guía PDF p. 46).
- No usar IDs erróneos: pueden hacer que el modelo razone mal sin error explícito (Slides PDF p. 51).

**Posible confusión con otros conceptos:**
- Client tools vs server tools — en las client tools tu aplicación ejecuta la tool y envía un `tool_result`; en server tools como `web_search`, `web_fetch`, `code_execution` y `tool_search`, Anthropic las ejecuta y las integra en la respuesta (Guía PDF p. 45; Guía PDF p. 46).

### Decisión dirigida por el modelo vs flujos preconfigurados

**Concepto:** en model-driven decision-making Claude usa el contexto para decidir qué tool llamar, en lugar de un árbol de decisión preconfigurado o una secuencia fija de tools codificada por el desarrollador (web 1.1; Guía PDF p. 47). Con `tool_choice` por defecto `{"type": "auto"}`, Claude decide en cada turno si llama a una tool o responde directamente (Guía PDF p. 47). La excepción es la lógica de negocio que exige cumplimiento determinista (operaciones financieras, controles de seguridad, requisitos regulatorios): ahí la aplicación programática prevalece sobre esa flexibilidad (web 1.1; Guía PDF p. 41).

**Ejemplos de uso (3, cortos):**
1. Un cliente pregunta por un cristal roto y un montaje retrasado en un solo mensaje; Claude se adapta a lo no planificado (web 1.1).
2. Si la búsqueda devuelve varias cuentas, el agente pregunta; si la política es ambigua, escala a un humano (Guía PDF p. 41; Guía PDF p. 47).
3. Las reglas de reembolso de la vidriería están en código, no en el prompt (web 1.1).

**Qué NO hacer:**
- No depender solo del prompt, de few-shot o de un clasificador de tools para un orden obligatorio: usar un prerrequisito programático (Q1; Guía PDF p. 37).
- No confundir flexibilidad con permiso para saltarse controles requeridos en otras partes del sistema (Guía PDF p. 47).

**Posible confusión con otros conceptos:**
- Workflow tradicional — lógica predefinida, herramientas invocadas por regla; ideal para tareas estables y deterministas (Guía PDF p. 41).
- Agentic — toma de decisiones dirigida por el modelo; adecuado para tareas ambiguas, multi-paso y exploratorias (Guía PDF p. 41).

### Anti-patrones de terminación del loop

**Concepto:** hay tres anti-patrones al decidir cuándo parar: (1) analizar señales en lenguaje natural ("I'm done"), (2) usar topes de iteraciones arbitrarios como mecanismo principal y (3) usar la presencia de texto del assistant como indicador de finalización (web 1.1; Guía PDF p. 47). Nunca deben ser el mecanismo principal de parada; la señal fiable es `stop_reason` (web 1.1).

**Ejemplos de uso (3, cortos):**
1. Anti-patrón 1: "I've finished analysing the first file" puede decirse con intención de seguir con más archivos (web 1.1).
2. Anti-patrón 2: un tope de 10 iteraciones corta el trabajo si la tarea necesita 12, o ejecuta iteraciones de más si acaba en 3 (web 1.1).
3. Anti-patrón 3: `response.content[0].type == "text"` falla porque Claude puede devolver texto junto con bloques `tool_use`, p. ej. "Let me look up your order" más un `tool_use` de `lookup_order` (web 1.1).

**Qué NO hacer:**
- No tratar un tope de iteraciones (o `max_turns`/presupuesto) como detector de finalización: es una salvaguarda contra agentes descontrolados y de costes (web 1.1; Guía PDF p. 47; Guía PDF p. 48).
- No usar un tope como arreglo de la terminación prematura: los topes abordan loops descontrolados, no salidas prematuras (web 1.1).
- No prescindir de un límite: conviene un guard de iteraciones máximo para evitar loops infinitos y costes altos (Slides PDF p. 21; Slides PDF p. 45).

**Posible confusión con otros conceptos:**
- Safety cap — salvaguarda aceptable (en el ejercicio: constante `MAX_ITERATIONS` de 20 con un warning en el log si se activa; no debería activarse en operación normal) frente a tope como control principal, que es anti-patrón (web 1.1).
- `max_turns` — en el Agent SDK cuenta solo los tool-use turns (Guía PDF p. 48).

### Trampas del examen

- **Comprobar `response.content[0].type == 'text'` para dar la tarea por terminada:** Claude puede devolver texto junto con bloques `tool_use`; la presencia de texto no indica finalización (web 1.1). En la práctica el agente se detiene a mitad de una tarea compleja y devuelve una respuesta incompleta (web 1.1).
- **Tope de iteraciones como arreglo de la salida prematura (opción A del escenario, 15 iteraciones):** los topes corrigen loops descontrolados, no salidas prematuras; la corrección es siempre comprobar `stop_reason` (web 1.1).
- **Forzar `tool_choice` en `'any'` para que nunca haya texto plano (opción B del escenario):** no es la corrección; la corrección es continuar con `'tool_use'` y parar con `'end_turn'` (web 1.1).
- **Buscar frases como "I have completed" (opción D del escenario; Q13):** el lenguaje natural es ambiguo; Q13 acierta con B, inspeccionar `stop_reason` y terminar solo cuando sea `"end_turn"`, porque la redacción de Claude varía entre respuestas y actualizaciones del prompt (Q13; web 1.1). Fallan A y C por suposiciones incorrectas sobre cómo interactúan las tools con el texto, y D porque confunde la ejecución asíncrona con el control del loop (Q13).
- **Tope de 15 tool calls como mecanismo principal (Q14):** A y C declaran mal la práctica recomendada y D mezcla el prompt con el control del loop; la respuesta correcta es B, el tope es un límite de seguridad y `stop_reason: "end_turn"` sigue siendo la señal autoritativa (Q14).
- **Guardar los resultados en una base de datos y dar solo un resumen al modelo (Q15; web 1.1):** degrada el rendimiento cuando el modelo debe razonar sobre varios resultados a la vez, porque el resumen puede omitir valores de campos, códigos de error o datos condicionales (Q15). La API no guarda memoria del turno en el servidor; hay que añadir cada resultado al historial y reducir lo que devuelve la tool si es grande (web 1.1). Los distractores C y D (más de 10 llamadas, resultados más rápidos de 200 ms) no son modos de fallo reconocidos; A (datos binarios) es una preocupación válida pero no el riesgo principal en tareas de investigación con texto (Q15).
- **Resolver el orden obligatorio de tools con prompt, few-shot o un clasificador (Q1):** B y C dependen del cumplimiento probabilístico del LLM y D aborda la disponibilidad, no el orden; la respuesta A es un prerrequisito programático que bloquea `lookup_order` y `process_refund` hasta que `get_customer` devuelva un ID verificado (Q1).
- **Tratar `max_tokens` como respuesta completa o dejar fuera `end_turn`:** devuelve salidas cortadas al usuario o hace iterar de más (Slides PDF p. 26; Slides PDF p. 30).
- **Añadir texto tras los `tool_result` o ponerlos en orden incorrecto:** puede dar `end_turn` vacío o un error 400 (Guía PDF p. 46; Guía PDF p. 48).
- **Reconocer la respuesta correcta:** continuar en `"tool_use"`, terminar en `"end_turn"` y rechazar los tres anti-patrones (web 1.1).
- **Contradicción entre fuentes:** las slides citan como condiciones de parada comunes "stop_reason: finished", "task goal is achieved" y "maximum steps or limits reached" (Slides PDF p. 7), mientras la web y la guía establecen que el tope solo es salvaguarda y que la condición de finalización es `end_turn` (web 1.1; Guía PDF p. 48). Prevalecen la guía y el banco (Q14).

## Tarea 1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns (Orquestar sistemas multiagente con patrones coordinador-subagente)

### Hub-and-spoke: coordinator y subagents

**Concepto:** La orquestación multiagente es un conjunto de agentes Claude que trabajan juntos en una tarea compleja; en el patrón hub-and-spoke el coordinator es el hub (centro) y los subagents son los spokes (web 1.2). La guía describe esta arquitectura como la recomendada: el coordinator decide qué trabajo existe, qué se ha completado y cómo fusionar los hallazgos parciales (Guía PDF p. 48). Toda la comunicación entre subagents pasa por el coordinator (web 1.2).

**Ejemplos de uso (3, cortos):**
1. El coordinator recibe la tarea, la descompone, elige subagents, les pasa contexto, agrega resultados, gestiona errores y enruta información entre ellos (web 1.2).
2. El flujo: la petición del usuario entra al coordinator, este la divide en 3 tareas, las tareas salen a los subagents, los resultados vuelven y se envía la respuesta final (Slides PDF p. 87).
3. Un subagent de web search devuelve sus hallazgos al coordinator, nunca directamente al subagent de synthesis (web 1.2).

**Qué NO hacer:**
- No permitir mensajes directos entre subagents, ni por eficiencia ni por conveniencia: se saltarían la observabilidad, el manejo de errores consistente y el flujo de información controlado (web 1.2).
- No hacer que cada subagent decida por sí mismo si participa en el pipeline: distribuye la lógica de coordinación y rompe el patrón hub-and-spoke, reduciendo la observabilidad (Q16).
- No adoptar una malla peer-to-peer: oscurece la procedencia, complica los reintentos y dificulta saber qué agente tenía autoridad sobre cada decisión (Guía PDF p. 48).

**Posible confusión con otros conceptos:**
- Hub-and-spoke — un único coordinator central con subagents especializados que devuelven resultados (Slides PDF p. 79)
- Malla peer-to-peer de agentes — los agentes se comunican entre sí; es el contraste deliberado del diseño del examen (Guía PDF p. 48)

Beneficios de un hub único: observabilidad (log y monitoreo de todos los mensajes en un punto), manejo de errores consistente (políticas uniformes de recuperación) y flujo de información controlado (el coordinator decide qué contexto recibe cada subagent) (web 1.2). Los slides añaden mejor organización y escalabilidad, y mantenimiento más fácil porque se pueden actualizar subagents individuales sin afectar a todo el sistema (Slides PDF p. 81; Slides PDF p. 82). La guía resume los beneficios de los subagents como context isolation, parallelization y specialized instructions (Guía PDF p. 48).

### Aislamiento de contexto y paso explícito de contexto

**Concepto:** Los subagents no heredan automáticamente el historial de conversación del coordinator; un subagent nuevo empieza solo con lo que el coordinator incluye explícitamente en su prompt (web 1.2). El único canal directo del padre al subagent es el prompt string de la herramienta Agent (Guía PDF p. 49).

**Ejemplos de uso (3, cortos):**
1. El synthesis subagent necesita los resultados de web search, así que el coordinator los pone en el prompt de synthesis (web 1.2).
2. El coordinator entrega el enunciado del problema, el alcance, los archivos o fuentes a inspeccionar, las restricciones y los hallazgos ya producidos por otros agentes (Guía PDF p. 49).
3. Si el subagent de web search se invoca dos veces, la segunda invocación no sabe nada de la primera (web 1.2).

**Qué NO hacer:**
- No delegar con frases como «analiza el problema de antes»: el subagent no recibe historial ni resultados de herramientas del padre salvo que se incluyan en el prompt (Guía PDF p. 49).
- No asumir que existe memoria compartida o estado global: el subagent no tiene acceso al system prompt del coordinator, a mensajes previos, a resultados de otros subagents (salvo que se pasen) ni a «shared memory» (web 1.2).
- No omitir contexto: el sistema no falla con elegancia, entrega un problema subespecificado e invita a suposiciones alucinadas (Guía PDF p. 49).

**Posible confusión con otros conceptos:**
- Aislamiento de contexto — el subagent solo sabe lo que está en su prompt (Slides PDF p. 151)
- Retorno al padre — el padre solo recibe el mensaje final del subagent como resultado de la herramienta Agent, no su transcripción interna (Guía PDF p. 49)

Los slides lo resumen así: un paquete de contexto incompleto produce mala salida y uno completo produce buena salida; el coordinator actúa como project manager que transfiere información entre especialistas (Slides PDF p. 150; Slides PDF p. 151). Como solo el mensaje final vuelve al coordinator, si este necesita procedencia, citas, marcas de tiempo o metadatos estructurados, la salida final del subagent debe incluirlos explícitamente; las salidas deben ser estructuradas, acotadas y que preserven la atribución (Guía PDF p. 49).

### Selección dinámica de subagents

**Concepto:** El coordinator analiza lo que requiere la consulta y selecciona solo los subagents necesarios, en lugar de pasar todo por un pipeline fijo (web 1.2; Guía PDF p. 49). Una pregunta factual simple puede necesitar solo web search (web 1.2).

**Ejemplos de uso (3, cortos):**
1. Si el dueño pregunta el horario del vertedero, el coordinator invoca solo el subagent de web search (web 1.2).
2. Para «What year was the Anthropic API released?», basta con los subagents necesarios y no los cuatro (web search, document analysis, synthesis y report generation), que tardaban 45 segundos con coste innecesario (Q16).
3. Una petición investigativa amplia puede requerir varios subagents; una simple, uno solo (Guía PDF p. 49).

**Qué NO hacer:**
- No enrutar toda consulta por todos los subagents: desperdicia tiempo y recursos (web 1.2).
- No sustituir al coordinator por una tabla estática de palabras clave: cambia inteligencia adaptativa por una tabla frágil (Q16).
- No reducir de cuatro a dos subagents fusionando web search y document analysis: reduce capacidad en lugar de mejorar el enrutamiento (Q16).

**Posible confusión con otros conceptos:**
- Selección dinámica — decidir según complejidad y tipo de consulta (Q16)
- Cachear resultados de subagents no usados — no elimina la latencia ni la sobrecarga de llamadas API (web 1.2)

Mecanismo en el SDK: Claude decide si invocar un subagent principalmente por su campo description, y se puede forzar uno nombrándolo en el prompt; las definiciones de agentes pueden crearse dinámicamente en tiempo de ejecución, variando rigor del prompt, modelo o alcance de herramientas (Guía PDF p. 49).

### Partición del alcance y descomposición estrecha (narrow decomposition)

**Concepto:** El coordinator particiona el alcance de la investigación para minimizar trabajo duplicado, asignando a cada subagent subtemas o tipos de fuente distintos (web 1.2). Una descomposición demasiado estrecha produce cobertura incompleta de temas amplios, porque un subtema que nadie recibe nunca se investiga (web 1.2; Guía PDF p. 50).

**Ejemplos de uso (3, cortos):**
1. Un subagent busca noticias de precios de combustible mientras otro analiza las facturas de la empresa (web 1.2).
2. Dividir por tipo de fuente (web vs documentos), por porción de dominio (música, escritura, cine, artes visuales) o por función analítica (search, analysis, synthesis, report generation) (Guía PDF p. 50).
3. «Impact of AI on creative industries» descompuesto solo en arte digital, diseño gráfico y fotografía deja fuera música, escritura y cine (Guía PDF p. 50; Q7).

**Qué NO hacer:**
- No culpar a los subagents de huecos de cobertura: ejecutaron correctamente lo asignado; el problema es lo que se les asignó (Q7; web 1.2).
- No intentar arreglarlo con mejores consultas de búsqueda, un synthesis más capaz o más subagents: recibirían asignaciones igual de estrechas (web 1.2).
- No tratar la descomposición como una división mecánica; es un problema de diseño de cobertura (Guía PDF p. 51).

**Posible confusión con otros conceptos:**
- Falla de alcance — faltan categorías enteras; la causa casi siempre es la descomposición (web 1.2)
- Falla de profundidad — no es el síntoma de descomposición estrecha (web 1.2)

La partición debe ser distinta y colectivamente suficiente; las herramientas se restringen por rol (p. ej. un revisor de documentos con Read, Grep y Glob; un test-runner con Bash) (Guía PDF p. 50). En la práctica, la descomposición de «what drives our costs?» solo en combustible y mantenimiento de camiones omite tasas de vertedero, salarios y seguros (web 1.2).

### Agregación y bucles de refinamiento iterativo (iterative refinement loops)

**Concepto:** El coordinator evalúa la salida de synthesis en busca de huecos; si está incompleta, re-delega consultas dirigidas a los subagents de search y analysis, vuelve a invocar synthesis y repite hasta que la cobertura sea suficiente (web 1.2; Guía PDF p. 50). La agregación incluye reconciliar solapamientos, identificar contradicciones, eliminar duplicación y decidir si hace falta más trabajo de subagents (Guía PDF p. 50).

**Ejemplos de uso (3, cortos):**
1. Si el primer borrador no incluye costes de neumáticos, el coordinator envía una búsqueda dirigida y ejecuta synthesis de nuevo (web 1.2).
2. Un subagent de document analysis cubrió 3 de 5 fuentes: el coordinator lo re-invoca con un prompt explícito solo con las 2 fuentes faltantes, incluyendo los hallazgos previos como contexto (Q17).
3. Tras un coverage review, se envían tareas de seguimiento dirigidas en vez de re-ejecutar todo el flujo a ciegas, lo que mejora calidad y control de costes (Guía PDF p. 50).

**Qué NO hacer:**
- No pedir a synthesis que infiera lo que contienen las fuentes faltantes: fabrica contenido y socava la exactitud (Q17).
- No reenviar las 5 fuentes a una instancia nueva: reprocesa trabajo ya completado (Q17).
- No hacer que el coordinator analice por sí mismo las fuentes restantes: se salta la arquitectura coordinator-subagent e ignora la especialización (Q17).

**Posible confusión con otros conceptos:**
- Refinamiento iterativo — supervisión con re-delegación dirigida, no un fan-out de una sola pasada (Guía PDF p. 50)
- Ensamblar resúmenes independientes — no basta; la síntesis debe cubrir el panorama solicitado (Guía PDF p. 50)

### Invocación de subagents, paralelismo y límites

**Concepto:** En el SDK actual los subagents se invocan con la herramienta Agent; se define cada subagent en el parámetro agents y se incluye Agent en allowedTools (Guía PDF p. 50). La herramienta se renombró de Task a Agent en v2.1.63 y las referencias Task(...) siguen funcionando como alias (Guía PDF p. 50). Los slides usan el nombre Task: el coordinator no puede crear subagents si "Task" no está en sus allowed tools, p. ej. `allowedTools = ["Task"]` (Slides PDF p. 108).

**Ejemplos de uso (3, cortos):**
1. La invocación es un bloque tool_use en la respuesta de la API (Slides PDF p. 167; Guía PDF p. 51).
2. Un research coordinator lanza subagents paralelos invocando Task para todos los temas en una sola respuesta, y sintetiza al terminar todos (Slides PDF p. 201).
3. Aunque no se defina un subagent personalizado, Claude puede invocar el subagent general-purpose integrado mediante Agent (Guía PDF p. 50).

**Qué NO hacer:**
- No hacer que subagents compartan lectura/escritura sobre el mismo recurso en paralelo: causa conflictos; deben trabajar con datos independientes (Slides PDF p. 208).
- No olvidar recolectar todos los resultados antes de sintetizar (Slides PDF p. 208).
- No dar prompts vagos a subagents paralelos: no se depura a mitad de vuelo, hay que dar claridad por adelantado (Slides PDF p. 208).
- No usar modos permisivos como bypassPermissions sin cuidado: los subagents los heredan y no se pueden relajar por subagent; allowedTools sirve para restringirlos (Guía PDF p. 51).

**Posible confusión con otros conceptos:**
- Agent vs Task — mismo mecanismo de invocación con nombre histórico (Guía PDF p. 50)
- Subagent delegation vs Workflow tool — la delegación ordinaria funciona para pocas tareas delegadas por turno; para decenas o cientos de agentes se recomienda la Workflow tool (Guía PDF p. 51)

### Diagnóstico de fallos: el coordinator es responsable del resultado

**Concepto:** Si la salida final es incompleta, el responsable suele ser el coordinator, no los subagents; la mayoría de las fallas de orquestación nacen en la lógica del coordinator (Slides PDF p. 103; Slides PDF p. 159). Ante salida incompleta o incorrecta, se rastrea el origen antes de culpar al subagent: primero si el coordinator le dio la entrada correcta (web 1.2).

**Ejemplos de uso (3, cortos):**
1. Check Context Passing: los subagents pueden producir salidas incompletas si reciben contexto insuficiente (Slides PDF p. 156).
2. Check Task Decomposition: ¿asignó el coordinator todas las responsabilidades necesarias? (Slides PDF p. 156).
3. Check Aggregation Logic y Check Workflow Continuation: buenas salidas de subagents pero fallo al agregar, o coordinator que sale demasiado pronto (Slides PDF p. 157; Slides PDF p. 158).

**Posible confusión con otros conceptos:**
- 4 Step Diagnostic Framework — contexto, descomposición, agregación, continuación (Slides PDF p. 158)

### Trampas del examen

- Culpar a los subagents de huecos de cobertura. En Q7 cada subagent terminó con éxito, pero el coordinator descompuso el tema solo en «AI in digital art creation», «AI in graphic design» y «AI in photography»; la correcta es B (descomposición estrecha). Fallan A (synthesis sin instrucciones de huecos), C (consultas de web search) y D (document analysis filtrando fuentes) porque la causa está en lo asignado (Q7). Igual en la web: si solo se asignan solar y wind, ningún subagent puede cubrir geothermal ni tidal; en el escenario de práctica la opción B es la correcta frente a synthesis, document analysis y web search (web 1.2).
- Pipeline completo para toda consulta. En Q16 la correcta es C (selección dinámica); A (tabla estática de palabras clave) es frágil, B (autoselección de subagents) rompe hub-and-spoke y reduce observabilidad, D (fusionar a dos subagents) reduce capacidad (Q16). Cachear los resultados de subagents no usados tampoco sirve: añaden latencia y sobrecarga de API (web 1.2).
- Re-delegación incorrecta. En Q17 la correcta es B (re-invocar con solo las 2 fuentes faltantes y los hallazgos previos); A inventa contenido, C reprocesa todo, D evita el subagent especializado (Q17).
- Asumir que los subagents comparten memoria o heredan el historial, el system prompt o resultados de otros subagents (web 1.2; Guía PDF p. 49).
- Proponer comunicación directa entre subagents como mejora de eficiencia: es la respuesta incorrecta aunque se ofrezca como más eficiente (web 1.2).

**Contradicción entre fuentes:** La web indica (comprobado el 6 de octubre de 2026) que en Claude Code un subagent puede crear subagents hasta tres capas por debajo de la conversación principal, y que el SDK actual permite a un subagent enviar mensajes a otros agentes con SendMessage; llama a la regla estricta «nunca» una simplificación (web 1.2). La guía dice que en el SDK actual los subagents no pueden crear sus propios subagents y que no se debe incluir la herramienta Agent en su lista de herramientas (Guía PDF p. 48). Prevalece la guía: todo se enruta por el coordinator. Además, la guía usa el nombre Agent (antes Task) mientras que los slides usan Task (Guía PDF p. 50; Slides PDF p. 108).

## Tarea 1.3 — Configure subagent invocation, context passing, and spawning (Configurar la invocación, el paso de contexto y el spawning de subagentes)

### Task tool (Agent tool) y allowedTools

**Concepto:** el Task tool es el mecanismo con el que un coordinator hace spawn de subagentes en el Claude Agent SDK; el coordinator debe tener "Task" (o "Agent") en su `allowedTools` (web 1.3; Slides PDF p. 108; Q18). Claude Code lo renombró a Agent en v2.1.63 y "Task" sigue funcionando como alias (web 1.3; Guía PDF p. 51).

**Ejemplos de uso (3, cortos):**
1. `allowedTools = ["Task"]` para que el coordinator pueda lanzar subagentes (Slides PDF p. 108).
2. Definir los subagentes en el parámetro `agents` y dar al padre permiso para invocarlos permitiendo Agent (Guía PDF p. 51).
3. Si no se define un subagente propio, Claude aún puede invocar el subagente integrado general-purpose mediante el Agent tool (Guía PDF p. 51).

**Qué NO hacer:**
- No suponer que tener otras herramientas (`web_search`, `read_document`) permite crear subagentes: si falta "Task" en `allowedTools`, el coordinator no puede invocarlos (Q18; web 1.3).
- No culpar al system prompt del coordinator: un prompt bien escrito no puede llamar a una herramienta que no está en el conjunto permitido (Q18).
- No inventar parámetros como `subagent_endpoint` ni exigir plan mode para invocar subagentes (Q18).

**Posible confusión con otros conceptos:**
- Task (nombre del examen) vs Agent (nombre actual) — son la misma herramienta; la guía v1.0 usa Task, así que se responde "Task tool" aunque el código actual muestre Agent (web 1.3; Guía PDF p. 51).
- Permitir la herramienta vs describir al subagente — `allowedTools` da permiso de spawn; la `description` decide cuándo se delega (web 1.3; Guía PDF p. 52).

### AgentDefinition: description, prompt y restricción de herramientas

**Concepto:** un AgentDefinition define cada subagente con una description (qué hace; el coordinator la lee para decidir cuándo invocarlo), un system prompt (sus instrucciones) y restricciones de herramientas acordes a su rol (web 1.3). Un subagente debe ser un especialista enfocado con un job claro y una capacidad estrecha (Guía PDF p. 53).

**Ejemplos de uso (3, cortos):**
1. Subagente de web search con description "encuentra información de plantas y proveedores en línea" y herramientas limitadas a búsqueda (web 1.3).
2. Subagente de análisis de documentos con solo herramientas de lectura de archivos (web 1.3).
3. Un reviewer que solo necesita Read, Grep y Glob, sin escritura de archivos ni shell (Guía PDF p. 53).

**Qué NO hacer:**
- No omitir el campo `tools` si el subagente debe ser restrictivo: sin `tools` hereda todas las herramientas disponibles (Guía PDF p. 53).
- No usar descripciones vagas como "research agent"; es mejor una específica como "finds and summarizes policy evidence with citation metadata" (Guía PDF p. 53).
- No dar permisos amplios sin pensar: `bypassPermissions` se hereda por los subagentes y no se puede relajar por subagente (Guía PDF p. 51).

**Posible confusión con otros conceptos:**
- `tools` vs `disallowedTools` — `tools` es una allowlist; `disallowedTools` quita herramientas del conjunto heredado o explícito, y si están ambos se aplica primero `disallowedTools` (Guía PDF p. 53).
- Delegación por description vs mención explícita — Claude decide según la description, mientras que "Use the code-reviewer agent" fuerza una delegación concreta (Guía PDF p. 52).

### Aislamiento de contexto y paso explícito de contexto

**Concepto:** los subagentes tienen contexto aislado: reciben solo lo que el coordinator escribe en su prompt, sin el historial del coordinator ni la salida de otros subagentes (web 1.3; Slides PDF p. 92; Guía PDF p. 52). El paso de contexto es un problema de diseño de handoff explícito, no una función de memoria automática (Guía PDF p. 52).

**Ejemplos de uso (3, cortos):**
1. Pasar los hallazgos completos de agentes previos: el prompt es la única entrada del synthesis subagent (web 1.3).
2. Strong context passing: incluir "Previous analysis: Shipment delayed by 12 days", la tarea (¿aplica la política de reembolso?) y el output esperado (Slides PDF p. 115).
3. Incluir en el prompt rutas de archivo, mensajes de error y decisiones que el subagente necesite (Guía PDF p. 52).

Los 4 componentes del context passing: Task Objective, Relevant Context, Constraints or Rules y Expected Output (Slides PDF p. 117-121). Regla 3 de la web: especificar objetivos y criterios de calidad, no procedimientos paso a paso, para que el subagente pueda adaptarse (web 1.3).

**Qué NO hacer:**
- No asumir que el subagente hereda el historial del coordinator ni las salidas de otros subagentes (web 1.3; Guía PDF p. 51).
- No usar prompts débiles como "Continue analyzing the issue.": el subagente no sabe a qué se refiere (Slides PDF p. 114).
- No escribir el prompt como procedimiento exacto: se rompe ante entradas inesperadas (web 1.3).

**Posible confusión con otros conceptos:**
- Contexto aislado vs "desde cero absoluto" — el subagente recibe su system prompt, el mensaje de delegación y las definiciones de herramientas; en Claude Code también puede recibir CLAUDE.md del proyecto y memory (Guía PDF p. 52).
- Explore y Plan — estos agentes integrados omiten CLAUDE.md y git status, así que una regla imprescindible debe repetirse en el prompt de delegación (Guía PDF p. 52).

### Metadatos estructurados (contenido separado de metadatos)

**Concepto:** el contenido (afirmación, hecho, análisis) debe pasarse separado de los metadatos (URL, nombre de documento, número de página) para que el agente posterior pueda atribuir cada afirmación (web 1.3; Q19).

**Ejemplos de uso (3, cortos):**
1. Un finding con campos `claim`, `source_url`, `document_name`, `page_number`, `confidence`, `retrieved_by` (web 1.3).
2. El coordinator pasa al synthesis subagent el array completo de findings con todos los metadatos (web 1.3).
3. El subagente de búsqueda devuelve URLs y títulos; el de documentos, referencias de página (web 1.3).

```json
{
  "findings": [
    {
      "claim": "Solar panel efficiency has increased 25% in the last decade",
      "source_url": "https://example.com/solar-report",
      "document_name": "Annual Solar Industry Report 2024",
      "page_number": 14,
      "confidence": "high",
      "retrieved_by": "web_search_agent"
    }
  ]
}
```

**Qué NO hacer:**
- No comprimir los hallazgos eliminando el vínculo afirmación-fuente (web 1.3).
- No cambiar el prompt del synthesis agent para arreglar la falta de citas: no puede citar lo que no recibió (web 1.3).
- No concatenar salidas en un bloque de texto esperando que synthesis extraiga las citas (Q19).

**Posible confusión con otros conceptos:**
- Fallo de atribución vs fallo del prompt de synthesis — la causa es metadatos eliminados por el coordinator, no el prompt (web 1.3).
- Diagnóstico general — comprobar primero Context Passing, y también Task Decomposition, Aggregation Logic y Workflow Continuation (Slides PDF p. 156-158).

### Spawning paralelo vs secuencial

**Concepto:** para tareas independientes, el coordinator emite varias llamadas al Task tool en una sola respuesta, de modo que los subagentes corren a la vez; el spawning secuencial (uno por turno) añade latencia sin beneficio (web 1.3; Q20). Con paralelismo el tiempo total es el del subagente más lento, no la suma (Guía PDF p. 54).

**Ejemplos de uso (3, cortos):**
1. Análisis financiero, de competidores y de sentimiento del cliente ejecutados simultáneamente (Slides PDF p. 110).
2. Investigar market trends, competitor analysis y regulatory environment con tres subagentes de búsqueda en una sola respuesta (Q20).
3. Flujo mixto: búsqueda de fuentes (secuencial), resumen de las fuentes A, B y C (paralelo) y síntesis final (secuencial) (Slides PDF p. 219).

Frases de prompt que señalan paralelismo: "Invoke all tasks simultaneously", "Call the Task tool for each of the following at the same time" (Slides PDF p. 200). Errores comunes: recursos compartidos de lectura/escritura que causan conflictos, olvidar recoger todos los resultados antes de sintetizar y prompts de subagente poco claros (Slides PDF p. 208).

**Qué NO hacer:**
- No lanzar secuencialmente tareas independientes "para evitar conflictos de contexto" (Q20; web 1.3).
- No enrutar los tres subtemas por un único subagente en secuencia: elimina el paralelismo y asume una dependencia inexistente (Q20).
- No sintetizar antes de que terminen todas las tareas paralelas (Slides PDF p. 208).

**Posible confusión con otros conceptos:**
- Spawning paralelo vs fork_session — paralelo ejecuta tareas independientes a la vez; fork explora enfoques divergentes desde una base compartida (web 1.3).

### fork_session vs --resume

**Concepto:** fork_session crea ramas independientes desde una base de análisis compartida; tras la bifurcación, ninguna rama ve los resultados de la otra (web 1.3). Resume continúa una sesión concreta con nombre (web 1.3). `--resume` es un flag de CLI con opción equivalente en el SDK; fork_session es la opción del SDK (`forkSession` en TypeScript) y en CLI `--fork-session` (web 1.3).

**Ejemplos de uso (3, cortos):**
1. Tras analizar un codebase, bifurcar para comparar dos estrategias de testing (web 1.3).
2. Bifurcar tras analizar el survey de un sitio para comparar dos planes de plantación (web 1.3).
3. Usar resume para continuar una misma propuesta (web 1.3).

**Qué NO hacer:**
- No usar resume cuando se quiere explorar un enfoque alternativo sin perder el camino original; para eso se usa fork (Guía PDF p. 53; web 1.3).
- No esperar que `--fork-session` actúe solo: en la CLI solo tiene efecto junto con `--resume` o `--continue` (web 1.3).

**Posible confusión con otros conceptos:**
- fork de sesión vs forked subagent — el fork de sesión crea una nueva sesión con copia del historial y deja la original intacta (Guía PDF p. 53); el forked subagent de Claude Code hereda toda la conversación, ve el mismo system prompt, tools, model e historial, y solo su resultado final vuelve al padre (Guía PDF p. 53-54). Puede usar `isolation: "worktree"` (Guía PDF p. 54).
- Resume de subagentes — conserva su historial completo; se captura `session_id` y el `agentId` del resultado del Agent tool; Explore y Plan son one-shot y no devuelven `agentId` (Guía PDF p. 54).
- Con el SDK actual, fork es un modificador de resume: `ClaudeAgentOptions(resume=session_id, fork_session=True)`; sin `fork_session` se añade a la sesión original (web 1.3). La distinción es añadir vs bifurcar.

### Retorno del subagente y subagentes anidados

**Concepto:** el padre no recibe la transcripción interna del subagente, sino su mensaje final como resultado del Agent tool; el padre puede resumirlo, y para conservar el texto exacto se le indica preservarlo verbatim (Guía PDF p. 52). El informe final del subagente es el artefacto más seguro para pasar a workers posteriores (Guía PDF p. 52).

**Ejemplos de uso (3, cortos):**
1. Capturar el informe final de un subagente de investigación para el siguiente worker (Guía PDF p. 52).
2. Instruir al padre para preservar la salida del subagente verbatim (Guía PDF p. 52).
3. Para decenas o cientos de agentes, el patrón recomendado es el Workflow tool, que saca la orquestación del contexto principal (Guía PDF p. 51).

**Qué NO hacer:**
- No asumir que el padre ve el razonamiento interno ni las llamadas a herramientas del subagente: solo recibe el mensaje final (Guía PDF p. 52).

**Posible confusión con otros conceptos:**
- Subagentes que crean subagentes — los docs conceptuales dicen que "Subagents cannot spawn their own subagents" y desaconsejan incluir Agent en las tools del subagente, pero el changelog de Claude Code del 10 de junio de 2026 dice que pueden hacerlo (hasta 5 niveles); para el examen se esperan los principios estables salvo que se mencione el nuevo comportamiento (Guía PDF p. 53).

### Trampas del examen

- Creer que el coordinator puede invocar subagentes teniendo solo `["web_search", "read_document"]` en `allowedTools`: falla porque falta "Task"; las opciones A (`subagent_endpoint` inexistente), C (el prompt no concede capacidad) y D (plan mode) son distractores (Q18).
- Culpar al prompt de synthesis cuando las afirmaciones pierden sus citas: el synthesis agent no puede citar lo que no recibió; la causa es que el coordinator pasó contenido sin metadatos estructurados. Tampoco se arregla dándole acceso directo a herramientas (web 1.3).
- En el escenario de práctica, las opciones A (el prompt de synthesis no pide citas), C (el subagente de búsqueda devuelve prosa) y D (synthesis sin web search) fallan porque el prompt y las tools no cambiaron y los subagentes de búsqueda y documentos devuelven resultados bien fuentados en el formato de siempre; la causa más probable es la opción B, contenido sin metadatos estructurados (web 1.3).
- Pedir a synthesis que haga sus propias búsquedas web (Q19-A), que solo reciba URLs y relea cada fuente (Q19-D) o concatenar todo en un bloque de texto (Q19-C): son trabajo redundante, ineficiente o pierden la asociación afirmación-fuente (Q19). La respuesta correcta es el formato estructurado que separa contenido y metadatos (Q19).
- Spawning secuencial de subtemas independientes (Q20-A), usar un solo subagente en secuencia (Q20-C) o un subagente con tres prompts sucesivos (Q20-D): añaden latencia o eliminan el paralelismo; la respuesta es emitir las tres llamadas `Task` en una sola respuesta (Q20). Las opciones con "in a single response" o "simultaneously" indican spawning paralelo (web 1.3).
- Asumir que los subagentes heredan automáticamente el historial del coordinator o las salidas de otros subagentes: no hay herencia automática de contexto (web 1.3; Guía PDF p. 52).
- Escribir el prompt del subagente como procedimiento paso a paso: no puede adaptarse; hay que indicar objetivo y criterios de calidad (web 1.3).
- Confundir fork y resume: resume continúa una sesión, fork la bifurca; en el SDK actual fork es un modificador de resume (web 1.3).
- Dejar subagentes con herramientas heredadas innecesarias cuando solo necesitan un conjunto estrecho: las preguntas suelen esconder el problema en el alcance de capacidades (Guía PDF p. 53).
- Pasar prompts vagos tipo "continue the earlier analysis": el subagente no ve qué es "earlier" (Guía PDF p. 52; Slides PDF p. 114).

- **Contradicción entre fuentes:** la web afirma como requisito binario que sin "Task"/"Agent" en `allowedTools` el coordinator no puede invocar subagentes (web 1.3), mientras que la guía y los docs actuales que cita la web describen `allowedTools` como lista de auto-approve (Guía PDF p. 51; web 1.3). Prevalece la guía en el mecanismo (sin la herramienta en la lista, el spawn pasa por el permission callback y en una ejecución desatendida se deniega), pero la respuesta del examen es la misma (Q18; web 1.3). Además, la guía señala que el nombre del examen puede ser Task mientras el SDK actual usa Agent (Guía PDF p. 52).

## Tarea 1.4 — Implement multi-step workflows with enforcement and handoff patterns (Implementar flujos de varios pasos con patrones de enforcement y handoff)

> Prioridad de estudio: Salvaguardas de la capa de orquestación (resolución o escalación) — 0% en los intentos 1 y 2

### Prompt guidance vs programmatic enforcement

**Concepto:** La prompt guidance indica a Claude qué debería hacer; la programmatic enforcement controla qué le permite hacer el sistema (Guía PDF p. 54). Una instrucción de prompt funciona quizá en el 90-95% de los casos pero tiene una tasa de fallo distinta de cero porque el modelo es probabilístico; un gate es código y por tanto determinista (web 1.4).

**Ejemplos de uso (3, cortos):**
1. Tono amable de soporte y preguntas aclaratorias: prompt guidance (Guía PDF p. 55).
2. Verificar la identidad del cliente antes de un reembolso: prerequisite gate programático que bloquea process_refund hasta que get_customer tenga éxito (Guía PDF p. 55).
3. Formato de los emails de presupuesto, donde un error no cuesta nada: basta una instrucción de prompt (web 1.4).

**Qué NO hacer:**
- Elegir "mejorar el prompt" cuando el flujo exige cumplimiento determinista; si la consecuencia del fallo es financiera, legal, de seguridad o afecta al cliente, un prompt solo normalmente no basta (Guía PDF p. 55).
- Añadir instrucciones de system prompt más fuertes o few-shot examples como solución a fallos de alto riesgo: mejoran la probabilidad pero no eliminan el fallo (web 1.4; Q21).
- Confiar en que el system prompt ya describe el orden requerido: los registros de producción ya muestran que no es suficiente (Q21).

**Posible confusión con otros conceptos:**
- Few-shot examples — muestran el flujo correcto y mejoran la precisión, pero no dan garantía determinista (web 1.4)
- Routing classifier — decide qué agente o qué herramientas se usan, no impone el orden de ejecución dentro del agente (web 1.4; Q21; Q1)

### Qué operaciones necesitan un gate (regla de decisión)

**Concepto:** La elección depende de lo que cuesta un único fallo. Si un solo fallo causaría pérdida financiera, brecha de seguridad o violación de compliance, se usa programmatic enforcement (web 1.4).

**Ejemplos de uso (3, cortos):**
1. Operaciones financieras (reembolsos, transferencias, pagos): programmatic enforcement; un reembolso no verificado a la cuenta equivocada es una pérdida (web 1.4).
2. Operaciones de seguridad (verificación de identidad, control de acceso) y de compliance (checks AML, requisitos regulatorios): programmatic enforcement (web 1.4).
3. Operaciones de bajo riesgo (preferencias de formato, guías de estilo, orden de salida): la prompt-based guidance es aceptable (web 1.4).

**Qué NO hacer:**
- Aplicar prompt-based guidance a escenarios con dinero, seguridad o compliance: la respuesta del examen es siempre programmatic enforcement (web 1.4).
- Usar un prompt solo para reglas que deben cumplirse siempre, como bloquear reembolsos por encima de un umbral o exigir aprobación humana en operaciones sensibles (Guía PDF p. 54).

### Prerequisite gate

**Concepto:** Un prerequisite gate es una regla programática que impide una acción posterior (downstream) hasta que uno o más pasos previos requeridos se hayan completado con éxito (Guía PDF p. 56). Claude sigue razonando y eligiendo herramientas, pero no puede saltarse la verificación requerida (Guía PDF p. 56).

**Ejemplos de uso (3, cortos):**
1. Bloquear process_refund a menos que get_customer haya devuelto un verified customer ID; si falta, el gate devuelve un error que pide llamar antes a get_customer (Guía PDF p. 56; web 1.4).
2. Flujo de reembolso: get_customer (verified_customer_id) → lookup_order (pedido válido del cliente verificado) → check refund policy (reembolso elegible o condición de escalación) → process_refund solo si se cumplen todos los prerrequisitos (Guía PDF p. 56).
3. Cierre de cuenta: bloquear close_account hasta que get_customer devuelva un verified customer ID (Q21); bloquear lookup_order y process_refund hasta lo mismo (Q1).

La respuesta controlada del gate puede tener esta forma (Guía PDF p. 56):

```json
{
  "allowed": false,
  "reason": "Customer verification is required before processing a refund.",
  "next_action": "Call get_customer or escalate_to_human."
}
```

Lógica del gate para process_refund: comprobar que existe verified_customer_id, que order_id pertenece a ese cliente y que el importe está dentro de la política; si todo pasa se permite, si no se bloquea y se devuelve la siguiente acción requerida (Guía PDF p. 56-57).

Caso de producción: un agente reembolsaba sin verificar la titularidad de la cuenta en el 8% de los casos aunque su prompt decía que verificara; el prompt funciona el 92% y falla el 8%. El gate elimina ese 8% sin mejorar el prompt (web 1.4).

**Qué NO hacer:**
- Pensar que el modelo puede esquivar el gate decidiendo saltarse la verificación: el gate bloquea incluso una llamada directa a process_refund (web 1.4).
- Resolver un fallo de orden de ejecución con un routing classifier: el fallo ocurre en la secuencia de ejecución del agente, no en el enrutamiento (web 1.4; Q1; Q21).

**Posible confusión con otros conceptos:**
- Hooks — interceptan e inspeccionan o modifican una llamada antes de ejecutarla; los gates se usan a menudo para el orden de pasos (Guía PDF p. 57)
- Handoff estructurado — resume el caso para un humano, no impide una llamada (Guía PDF p. 55)

### Hooks para enforcement

**Concepto:** Los hooks son comandos de shell definidos por el usuario que se ejecutan en puntos concretos del procesamiento de Claude; no son sugerencias al modelo y corren decida lo que decida el modelo (Guía PDF p. 57). Son el mecanismo principal de enforcement determinista en Claude Code y el Agent SDK y permiten insertar lógica de aplicación sin depender del cumplimiento del modelo (Guía PDF p. 57).

**Ejemplos de uso (3, cortos):**
1. Bloquear reembolsos superiores a $500 (Guía PDF p. 57).
2. Impedir cambios en campos restringidos de la cuenta o exigir aprobación humana en operaciones sensibles (Guía PDF p. 57).
3. Normalizar o validar la entrada de una herramienta antes de ejecutarla, o bloquear acciones destructivas sobre archivos o bases de datos (Guía PDF p. 57).

**Qué NO hacer:**
- Elegir enforcement basado en prompt cuando las reglas de negocio exigen cumplimiento garantizado; la guía prefiere hooks (Guía PDF p. 57).

**Posible confusión con otros conceptos:**
- Reembolso sobre umbral — se cubre con "hook o prerequisite gate" (Guía PDF p. 55)
- Verificar identidad antes del reembolso — prerequisite gate (Guía PDF p. 55)

### Subagent lifecycle hooks: SubagentStart y SubagentStop (contexto, no examinable)

**Concepto:** SubagentStart se dispara cuando el coordinator crea un subagent mediante Task (renombrada Agent en Claude Code v2.1.63); no puede bloquear, pero puede añadir contexto con additionalContext. SubagentStop se dispara cuando el subagent termina y puede mantenerlo trabajando con exit code 2 o con decision: "block" y una razón (web 1.4). La web indica que son lectura de fondo y que el examen no los evalúa (web 1.4).

**Ejemplos de uso (3, cortos):**
1. SubagentStart registra en un log cada creación de subagent o inyecta una instrucción permanente (web 1.4).
2. SubagentStop valida el resultado contra un schema; si falta un campo requerido, sale con código 2 y el subagent continúa (web 1.4).
3. Un subagent de facturación define en su frontmatter un hook PreToolUse que bloquea reembolsos por encima de un umbral, solo para sus propias llamadas (web 1.4).

**Qué NO hacer:**
- Esperar que SubagentStart bloquee la creación: para imponer reglas sobre el spawn se usa un hook PreToolUse sobre la herramienta Agent (web 1.4).
- Esperar que SubagentStop transforme la salida: ningún evento reescribe un resultado de herramienta; el coordinator lo remodela después (web 1.4).

**Posible confusión con otros conceptos:**
- Hooks en el frontmatter de un subagent — limitados a la vida del componente; los Stop hooks se convierten automáticamente en SubagentStop (web 1.4)

### Multi-concern request handling

**Concepto:** Cuando un cliente mezcla varios problemas en una petición, se descompone en elementos distintos, se investiga cada uno en paralelo con contexto compartido y se sintetiza una resolución unificada en una sola respuesta (web 1.4; Q22).

**Ejemplos de uso (3, cortos):**
1. "Devolver el pedido, actualizar la dirección de envío y preguntar por puntos de fidelidad": tres elementos con la cuenta del cliente como contexto común (web 1.4).
2. Disputa de cargo, pedido perdido y cambio de email: se descomponen y se investigan en paralelo con el contexto del cliente ya recuperado, y se compila una respuesta única (Q22).
3. Tarea de construcción: devolución más disputa de facturación más actualización de cuenta; el agente identifica las tres, investiga cada una y no omite ninguna (web 1.4).

**Qué NO hacer:**
- Tratar los elementos de forma secuencial en conversaciones separadas, o atender solo el primero y olvidar el resto (web 1.4).
- Atender solo el asunto de mayor prioridad y pedir tickets separados: mala experiencia y trabajo extra para el cliente (Q22).

**Posible confusión con otros conceptos:**
- Procesar en secuencia con caché — mejora los datos reutilizados pero no elimina el cuello de botella serie (Q22)
- Subagent genérico "multi-issue" — no refleja la especialización coordinator-subagent (Q22)

### Structured handoff protocols

**Concepto:** Al escalar a un agente humano, el handoff debe seguir un protocolo estructurado y ser autocontenido, porque el humano no tiene acceso a la transcripción de la conversación (web 1.4). Un resumen incompleto obliga al humano a pedirle al cliente que repita todo (web 1.4).

**Ejemplos de uso (3, cortos):**
1. Customer ID, para que el humano abra la cuenta (web 1.4).
2. Conversation summary (qué pidió el cliente y qué intentó el agente) y root cause analysis (la evaluación del agente del problema de fondo) (web 1.4).
3. Refund amount (si aplica, cifra concreta y no una referencia vaga) y recommended action (lo que el agente cree que debe hacer el humano) (web 1.4).

**Qué NO hacer:**
- Omitir campos críticos como el customer ID o la recommended action (web 1.4).
- Dejar campos vacíos o con texto de relleno en la función de handoff (web 1.4).

**Posible confusión con otros conceptos:**
- Prerequisite gate — bloquea una acción; el handoff resume el caso para un humano (Guía PDF p. 55)
- escalate_to_human — herramienta del agente de soporte que también aparece como siguiente acción posible en la respuesta del gate (Guía PDF p. 55-56)

### Trampas del examen

- Few-shot examples o instrucciones de prompt reforzadas como solución a fallos de alto riesgo: mejoran la precisión pero el modelo sigue siendo probabilístico y la tasa de fallo no llega a cero; para finanzas, seguridad y compliance solo vale el programmatic enforcement (web 1.4; Q21; Q1).
- Q21: la opción A (la instrucción de prompt basta) falla porque depende de cumplimiento probabilístico, que los registros ya muestran insuficiente; B (few-shot más prompt) mejora las probabilidades sin garantizar; D (routing classifier) aborda la selección de herramientas, no el orden. Correcta: C, un prerequisite que bloquea close_account hasta que get_customer devuelva un verified customer ID (Q21).
- Q1: B (prompt más fuerte) y C (few-shot) dependen del cumplimiento probabilístico del LLM; D (routing classifier que habilita un subconjunto de herramientas) trata la disponibilidad de herramientas, no su orden. Correcta: A, un prerequisite que bloquea lookup_order y process_refund hasta tener un verified customer ID (Q1).
- Escenario de práctica del 8%: las opciones A (routing classifier), C (few-shot) y D (instrucciones más fuertes) son distractores; la correcta es B, el prerequisite gate que bloquea process_refund hasta que get_customer devuelva un verified customer ID (web 1.4).
- Q22: A (un asunto por turno y tickets separados) crea mala experiencia; C (secuencial con caché) mantiene el cuello de botella serie; D (subagent "multi-issue" único) es indiferenciado. Correcta: B, descomponer, investigar en paralelo con contexto compartido y compilar una respuesta unificada (Q22).
- Routing classifiers propuestos para arreglar problemas de compliance por agente: deciden qué agente atiende, pero el fallo está en la secuencia de ejecución; la solución es un prerequisite gate (web 1.4).
- Handoff sin campos críticos (customer ID, recommended action): el humano no ve la transcripción, así que el resumen debe ser autocontenido con los cinco campos (web 1.4).
- Elegir "mejorar el prompt" cuando el flujo requiere cumplimiento determinista, si la consecuencia es financiera, legal, de seguridad o de impacto al cliente (Guía PDF p. 55).
- Nota del banco: Q1 está asignada a la tarea 1.4 en el índice aunque aparece físicamente en la 1.1 (Q1).
- Los subagent lifecycle hooks (SubagentStart/SubagentStop) son lectura de fondo y no contenido de examen; la guía acota los hooks del Agent SDK a PostToolUse e interceptación de llamadas a herramientas (web 1.4).
- **Contradicción entre fuentes:** no se detectan contradicciones factuales entre la guía, el banco y la web en esta tarea; la web añade el material de subagent lifecycle hooks, que la guía no trata (Guía PDF p. 54-57; web 1.4).

## Tarea 1.5 — Apply Agent SDK hooks for tool call interception and data normalization (Aplicar hooks del Agent SDK para interceptar llamadas a herramientas y normalizar datos)

### Hooks del Agent SDK (PreToolUse y PostToolUse)

**Concepto:** un hook del Agent SDK es código que intercepta una llamada a una herramienta o su resultado; es determinista (aplica la misma regla siempre) dentro de un sistema probabilístico, y corre entre el modelo y las herramientas (web 1.5). Los hooks son el mecanismo principal de enforcement determinista en Claude Code y el Agent SDK, y no dependen del cumplimiento del modelo (Guía PDF p. 57).

**Ejemplos de uso (3, cortos):**
1. PreToolUse: se ejecuta antes de la herramienta; puede bloquearla, modificarla o redirigirla a un flujo alternativo, y una herramienta bloqueada nunca corre (web 1.5).
2. PostToolUse: se ejecuta después de la herramienta y antes de que el modelo procese el resultado; puede transformarlo (web 1.5; Slides PDF p. 256).
3. En el pipeline completo, PreToolUse es la "red de seguridad" (solo operaciones permitidas) y PostToolUse la "capa de inteligencia" que enriquece resultados antes de que Claude actúe (Slides PDF p. 263).

**Qué NO hacer:**
- No tratar un hook como una sugerencia al modelo: los hooks corren sin importar lo que el modelo decida (Guía PDF p. 57).
- No usar PostToolUse para bloquear una acción: la herramienta ya se ejecutó y el bloqueo solo detiene el loop, sin deshacer el efecto secundario (web 1.5; Slides PDF p. 257).

**Posible confusión con otros conceptos:**
- Hook vs. prompt/CLAUDE.md — un hook se ejecuta incondicionalmente en la capa de aplicación; CLAUDE.md es consultivo (advisory) y no es vinculante a nivel de sistema (Guía PDF p. 59).

### Campos y decisiones de los hooks

**Concepto:** en la guía de hooks del Agent SDK (revisada en septiembre de 2026), un hook PreToolUse responde con un permissionDecision de allow, deny, ask o defer; deny detiene la llamada, y un updatedInput opcional reescribe los argumentos antes de que corra la herramienta (web 1.5). Un hook PostToolUse puede fijar updatedToolOutput para reemplazar lo que ve el modelo, tanto en herramientas integradas como MCP (web 1.5).

**Ejemplos de uso (3, cortos):**
1. Un PreToolUse que devuelve permissionDecision deny con un permissionDecisionReason; la herramienta no corre y el modelo recibe la razón (web 1.5).
2. Un PostToolUse registrado como HookCallback que lee tool_response y devuelve el objeto reescrito como updatedToolOutput dentro de hookSpecificOutput (web 1.5).
3. Un PreToolUse que devuelve un tool_input modificado: el hook parchea el JSON y la herramienta corre con parámetros corregidos (Slides PDF p. 244).

**Qué NO hacer:**
- No usar el antiguo updatedMCPToolOutput (solo cubría herramientas MCP): la documentación indica preferir updatedToolOutput (web 1.5).
- No devolver JSON inválido en stdout: Claude Code vuelve a la salida original (Slides PDF p. 261).

**Posible confusión con otros conceptos:**
- Exit code 2 — un PreToolUse que devuelve exit code 2 bloquea la herramienta incluso en modo bypassPermissions o con --dangerously-skip-permissions, lo que lo hace el mecanismo de enforcement más fuerte de Claude Code (Guía PDF p. 58).

### PostToolUse: normalización de datos

**Concepto:** normalizar es transformar la salida cruda de una herramienta a un formato consistente antes de que Claude la procese; reduce la carga cognitiva del modelo al quitar campos irrelevantes y asegura entradas consistentes sin importar qué versión de herramienta o servicio produjo la salida (Guía PDF p. 58). Sin normalización, el modelo interpreta los formatos mezclados de nuevo en cada iteración y sus lecturas varían (web 1.5).

**Ejemplos de uso (3, cortos):**
1. En el ejemplo de la tienda de muebles: get_customer devuelve fechas Unix (1710489600) y estados numéricos (200, 404, 500); lookup_order, ISO 8601 y strings ("active", "cancelled", "pending"); check_shipping, "DD/MM/YYYY" y códigos de un carácter ("S", "P") (web 1.5).
2. El hook convierte Unix timestamps a ISO 8601, códigos de estado a strings legibles ("shipped", "pending", "delivered"), monedas a decimal consistente con código de moneda y fechas regionales a un estándar (web 1.5).
3. Quitar campos innecesarios de una respuesta grande, convertir timestamps a una zona horaria estándar, normalizar códigos de estado a un vocabulario definido o extraer la parte relevante de un documento, para reducir ruido y evitar context bloat (Guía PDF p. 58, 58).

**Qué NO hacer:**
- No dejar que el modelo normalice formatos heterogéneos: introduce inconsistencia (web 1.5).
- No conservar la salida cruda junto al resumen en el resultado del hook: duplica el consumo de contexto; devolver solo el resumen formateado (Q25).

**Posible confusión con otros conceptos:**
- PreToolUse para limpiar resultados — PreToolUse ve la llamada saliente, no el resultado; transformar resultados es de PostToolUse (web 1.5).

### PreToolUse: aplicación de políticas (policy enforcement)

**Concepto:** los hooks PreToolUse implementan los prerequisite gates de 1.4: comprueban una llamada saliente contra una regla de negocio antes de ejecutar la herramienta; al bloquear, no hay efecto secundario que deshacer (web 1.5). Reciben el nombre de la herramienta y sus parámetros de entrada y pueden permitir, bloquear o modificar la llamada (Guía PDF p. 58).

**Ejemplos de uso (3, cortos):**
1. Umbral de reembolso: un hook sobre process_refund bloquea montos superiores a $500 y redirige a escalamiento humano; el reembolso de $900 de una mesa de comedor va al personal (web 1.5; Q24).
2. Prerequisito de cumplimiento: un hook sobre transfer_funds bloquea si la sesión no completó el chequeo AML (anti-money laundering) y el mensaje de error indica completarlo primero; se desbloquea cuando aml_check devuelve pass (web 1.5).
3. Aprobación de gerente: un hook sobre approve_discount para descuentos superiores al 20% pausa y envía a una cola de aprobación; un 25% en un sofá espera al gerente (web 1.5).

**Qué NO hacer:**
- No bloquear con PostToolUse ni "revertir" después: una validación posterior a process_refund corre cuando la violación ya ocurrió (Q24).
- No resolver la política solo con prompts (ver Hooks vs. prompts) (web 1.5; Q24).

**Posible confusión con otros conceptos:**
- Prerequisite gate (orden de pasos) vs. hook de enforcement — los gates imponen el orden; los hooks son útiles cuando el sistema debe inspeccionar o modificar una llamada antes de ejecutarla, p. ej. bloquear refunds sobre $500, cambios a campos restringidos, exigir aprobación humana, bloquear acciones destructivas de archivos o bases de datos, o normalizar/validar la entrada (Guía PDF p. 57).

### Hooks vs. prompts (marco de decisión)

**Concepto:** lo que debe cumplirse el 100% de las veces va en hooks (garantía determinista); lo preferible pero tolerante a desvíos ocasionales va en prompts (probabilístico) (web 1.5). Si un solo fallo costaría dinero o implicaría riesgo legal, se usa un hook; para formato o estilo basta un prompt (web 1.5). Las instrucciones de CLAUDE.md son consultivas: reforzarlas con "IMPORTANT" o "ALWAYS" reduce violaciones pero no las elimina (Guía PDF p. 59).

**Ejemplos de uso (3, cortos):**
1. Reembolsos sobre $500: el prompt funciona casi siempre, pero un fallo aprueba un reembolso grande sin autorización; el hook bloquea el 100% (web 1.5). En el banco, la regla en el system prompt se violaba en ~3% de los casos (Q24).
2. AML en transferencias internacionales: un prompt cumple 95% y el 5% restante es una violación regulatoria; el hook sobre transfer_funds funciona 100% (web 1.5).
3. Formato markdown: un prompt basta; un hook sería sobrecarga innecesaria (web 1.5).

**Qué NO hacer:**
- No endurecer el texto del prompt ni añadir 10 ejemplos few-shot esperando garantía total (Q24).
- No asumir que skills o reglas por ruta (path-scoped) son vinculantes: siguen siendo consultivas (Guía PDF p. 59).

**Posible confusión con otros conceptos:**
- CLAUDE.md / path-scoped rules / skills — guían al modelo y cargan contexto condicionalmente; un hook ejecuta de forma programática (Guía PDF p. 59).

### Matchers y configuración de hooks

**Concepto:** un matcher especifica a qué llamadas se aplica el hook (Guía PDF p. 59). En la configuración de un PostToolUse intervienen el matcher (herramientas objetivo), el command (script que recibe JSON por stdin) y stdout (lo que se imprime es lo que Claude ve) (Slides PDF p. 258).

**Ejemplos de uso (3, cortos):**
1. Un nombre único, p. ej. Edit, aplica solo a llamadas Edit (Guía PDF p. 59).
2. Una lista separada por pipes, p. ej. Edit|Write, aplica a ambas (Guía PDF p. 59).
3. Un matcher vacío aplica a todas las llamadas de la sesión (Guía PDF p. 59); ejemplo común: ESLint tras cada modificación con matcher sobre Edit y Write (Guía PDF p. 59).

**Qué NO hacer:**
- No usar matchers demasiado amplios (sobrecarga y efectos colaterales) ni demasiado estrechos (se pierden llamadas que debían interceptarse); el alcance debe coincidir con el enforcement (Guía PDF p. 59).

### Patrones de PostToolUse y capacidades

**Concepto:** PostToolUse corre justo tras completarse la llamada, antes de que Claude procese el resultado, y recibe Tool Name, Tool Input y Tool Response (Slides PDF p. 256). Tres patrones centrales: Audit Logging, Output Enrichment y Data Masking (Slides PDF p. 259). El hook puede devolver el resultado sin cambios (Pass Through), modificado (Modified Response) o reemplazado (Replaced Response) (Slides PDF p. 261).

**Ejemplos de uso (3, cortos):**
1. Audit Logging: capturar nombre, input, output y timestamp de cada llamada para depuración y cumplimiento (Slides PDF p. 259).
2. Data Masking: borrar API keys, credenciales y PII de las salidas antes de que entren a la ventana de contexto (Slides PDF p. 259).
3. Ejecutar un linter tras cada edición, validar el esquema de salida o añadir una entrada de auditoría tras cada escritura (Guía PDF p. 58).

**Qué NO hacer:**
- No devolver una respuesta reemplazada basura: "If you return garbage, Claude gets garbage" (Slides PDF p. 261).

**Posible confusión con otros conceptos:**
- Hook de sesión PreCompact (más allá de la guía) — corre antes de que Claude Code compacte la conversación (matcher manual con /compact o auto); puede archivar el transcript y bloquear con exit code 2 o "decision": "block"; PostCompact lleva el resumen generado. Mismo patrón: Pre inspecciona/bloquea, Post solo observa (web 1.5).

### Trampas del examen

- Usar PostToolUse para bloquear acciones que violan políticas: corre después de la ejecución, cuando la acción no conforme ya ocurrió; se usa PreToolUse (web 1.5; Slides PDF p. 257). En Q24, la opción D (validar y revertir tras process_refund) falla porque la violación ya ocurrió (Q24). En la práctica de AML, añadir un PostToolUse que solo marque transferencias ya completadas es la opción incorrecta; la correcta es un PreToolUse que bloquee hasta que la verificación AML devuelva pass (web 1.5).
- Prompts mejorados como solución a un requisito de 100%: son probabilísticos; con requisitos financieros, regulatorios o de seguridad se necesita un hook (web 1.5). En Q24, endurecer el texto (A) o añadir 10 ejemplos few-shot (B) mejoran la adherencia sin garantizar cero violaciones (Q24). Las opciones de few-shot o instrucciones detalladas en el system prompt para AML también son distractores (web 1.5).
- Dejar al modelo normalizar formatos mezclados: introduce inconsistencia (p. ej. confundir día/mes en DD/MM/YYYY o leer "P" como "processed" en vez de "pending") (web 1.5). En Q23, B (instrucciones de conversión en el system prompt) es probabilístico y añade tokens; A (cambiar los backends) puede no ser viable y acopla; D (reformatear la respuesta final) normaliza después de que el modelo ya razonó con datos inconsistentes (Q23).
- Usar PreToolUse para convertir resultados: ve la llamada saliente, no el resultado; la transformación va en PostToolUse (web 1.5).
- Q25: desactivar el hook (A) pierde los beneficios de normalización; subir max_tokens (C) aumenta capacidad de salida pero no resuelve el crecimiento del contexto de entrada; pre-procesar los comandos Bash (D) exige cambios grandes y puede no ser viable. La respuesta es B: devolver solo el resumen (Q25).
- Reglas de CLAUDE.md seguidas "casi siempre": el diagnóstico es que CLAUDE.md es consultivo; el patrón de violaciones intermitentes señala que hace falta un hook (Guía PDF p. 59).
- Matchers mal dimensionados (muy amplios o muy estrechos) se evalúan en el examen (Guía PDF p. 59).
- **Contradicción entre fuentes:** las slides dicen en el ciclo de vida que PostToolUse "Can block or modify output" (Slides PDF p. 255) pero en la comparación que no puede bloquear la herramienta porque "already ran" (Slides PDF p. 257); prevalece que PostToolUse no puede impedir la acción, en línea con la web, la guía y el banco (web 1.5; Q24). La web añade que un bloqueo en PostToolUse detiene el loop pero no deshace el efecto secundario (web 1.5).

## Tarea 1.6 — Design task decomposition strategies for complex workflows (Diseñar estrategias de descomposición de tareas para flujos de trabajo complejos)

> Prioridad de estudio: Decomposición dinámica de tareas (50% en el mapa de refuerzo)

### Fixed sequential pipeline (prompt chaining)

**Concepto:** Pipeline fijo que ejecuta pasos predeterminados en orden; cada paso toma como entrada la salida del anterior y la secuencia no cambia según resultados intermedios (web 1.6). También se llama prompt chaining (web 1.6).

**Ejemplos de uso (3, cortos):**
1. Revisión de código en tres pasos: análisis local por archivo, pase de integración entre archivos (data flow, consistencia de API, import chains) e informe final (web 1.6).
2. Revisión de pull requests con tres aspectos de criterios definidos (security, style, performance): un pase enfocado por aspecto, cada uno con sus criterios (Q26).
3. Procesamiento de documentos, extracción de datos y compliance checks, donde los campos y el formato están predeterminados (web 1.6).

**Qué NO hacer:**
- No usarlo en tareas abiertas: no puede adaptarse a hallazgos inesperados; si el paso 2 descubre un problema, el paso 3 no puede cambiar (web 1.6).
- No aplicar dynamic decomposition a una tarea estructurada cuyos pasos se conocen de antemano: añade sobrecarga innecesaria (Q26) y la hace menos predecible y más difícil de depurar (web 1.6).

**Ventajas:** resultados consistentes y fiables, depuración fácil (se sabe qué paso produjo cada salida) y monitoreo fácil (se registra la salida de cada paso) (web 1.6).

**Posible confusión con otros conceptos:**
- Dynamic adaptive decomposition — investigar un bug de alcance desconocido, donde el plan cambia según lo descubierto (Q27).

### Dynamic adaptive decomposition

**Concepto:** El plan cambia a medida que el agente aprende: parte de un objetivo de alto nivel, investiga y planifica según lo que encuentra; la nueva información puede cambiar los pasos restantes (web 1.6). Es la opción cuando el alcance es desconocido y no se pueden escribir los pasos por adelantado (web 1.6; Q27).

**Ejemplos de uso (3, cortos):**
1. Añadir tests a una codebase legacy: mapear la estructura, identificar áreas de alto impacto, escribir un plan priorizado y reordenar al descubrir que el Módulo A depende del Módulo B sin tests (web 1.6).
2. Root-cause de un bug introducido en las últimas dos semanas en un conjunto desconocido de archivos y servicios: mapear servicios afectados y línea temporal de síntomas, y generar subtareas según lo descubierto (Q27).
3. Exploración de sistemas legacy, security audits, proyectos de investigación y depuración de codebases desconocidas (web 1.6).

**Qué NO hacer:**
- No elegir un pipeline fijo (prompt chaining con pasos como logs, configs, service calls en orden) para una investigación de alcance desconocido (Q27; web 1.6).
- No dividir la investigación en dos agentes independientes que reportan a un humano: se pierde la inteligencia coordinadora y la síntesis recae en la persona (Q27).
- No reducirla a una búsqueda de un solo pase con lista de candidatos para revisión manual: no aplica el razonamiento del modelo (Q27).

**Contrapartida:** da resultados más completos en tareas abiertas, pero es menos predecible: el tiempo de ejecución varía con los descubrimientos, y estimar el uso de recursos y depurar es más difícil (web 1.6).

**Posible confusión con otros conceptos:**
- Fixed sequential pipeline — revisar un PR con aspectos conocidos de antemano (Q26).

### Elegir el patrón según las características de la tarea

**Concepto:** El patrón se elige por las características de la tarea, no por lo sofisticado que suene (web 1.6). Pasos conocidos y entrada estructurada: fixed pipeline; alcance abierto y desconocido: dynamic decomposition (web 1.6).

**Ejemplos de uso (3, cortos):**
1. Revisión de código multiarchivo: fixed pipeline, porque el análisis por archivo más la integración entre archivos es predecible (web 1.6).
2. Extracción de documentos: fixed pipeline, porque los campos y el formato están predeterminados (web 1.6).
3. Depurar un sistema desconocido o explorar una codebase legacy: dynamic decomposition, porque la causa raíz o las dependencias emergen durante la investigación (web 1.6).

**Resumen del banco:** aspectos predecibles y bien definidos que deben cubrirse → prompt chaining con pases secuenciales enfocados (Q26); alcance desconocido → dynamic adaptive decomposition (Q27). El refuerzo del usuario marca esta distinción como tema débil.

### Attention dilution y multi-pass architecture

**Concepto:** Attention dilution ocurre cuando un agente procesa demasiados ítems en un solo pase: la profundidad del análisis se vuelve inconsistente porque la atención se reparte entre todos los ítems (web 1.6). La solución es estructural: multi-pass architecture con un pase local por ítem y un pase de integración entre ítems (web 1.6).

**Ejemplos de uso (3, cortos):**
1. Revisión de 14 archivos: 14 pases por archivo más un pase de integración; los pases por archivo detectan los null pointer bugs de los archivos 10-14 (web 1.6).
2. El pase de integración revisa data flow y consistencia de patrones entre archivos, y detecta el forEach evaluado de forma inconsistente (marcado como ineficiente en el archivo 3 y sin comentario en el 11) (web 1.6).
3. Revisión con tres aspectos: un pase por aspecto dedica atención completa a cada preocupación en lugar de dividirla entre las tres (Q26).

**Síntomas:** feedback detallado en los primeros ítems y cada vez más superficial en los siguientes; un patrón marcado en un ítem mientras contenido idéntico se aprueba en otro; errores obvios omitidos mientras se detectan problemas menores de estilo (web 1.6). En el ejemplo de 14 archivos: archivos 1-5 con feedback detallado, 6-9 moderado, 10-14 superficial, sin detectar null pointer bugs ni vulnerabilidades de SQL injection (web 1.6).

**Qué NO hacer:**
- No proponer un modelo más potente, una ventana de contexto mayor o un prompt más detallado: todos los ítems siguen en un solo pase (web 1.6).
- No usar un pase único que examine todos los aspectos a la vez para captar preocupaciones transversales: sufre el problema de attention dilution (Q26).
- No agrupar archivos en lotes sin un pase de integración entre archivos: se reduce la dilución dentro de cada lote, pero se pierden los problemas entre lotes (web 1.6).

**Posible confusión con otros conceptos:**
- Pase local por ítem — detecta problemas locales de forma consistente (web 1.6).
- Pase de integración — se centra en las relaciones entre ítems: data flow, uso inconsistente de patrones, dependencias entre archivos (web 1.6).
- Tres agentes totalmente independientes sin contexto compartido — pierden el contexto de integración entre archivos (Q26).

### Dimensiones de descomposición

**Concepto:** Las tareas se descomponen según varias dimensiones; la correcta depende de la naturaleza de la tarea, no de la conveniencia (Guía PDF p. 60). La descomposición es el proceso de dividir un objetivo complejo en unidades que se asignan a subagentes o se manejan en pases separados (Guía PDF p. 59).

**Ejemplos de uso (3, cortos):**
1. Domain decomposition: investigar el impacto de la IA en industrias con particiones como música, escritura, cine, artes visuales y comercio (Guía PDF p. 60).
2. Source-type decomposition: un subagente para fuentes web actuales, otro para documentos internos y otro para una base de datos estructurada; el coordinador sintetiza (Guía PDF p. 60).
3. Functional decomposition: pipeline de extracción con etapas de retrieval, parsing, validation y formatting, cada una con un handoff estructurado (Guía PDF p. 60).

**Qué NO hacer:**
- No usar particiones vagas como "online" y "offline", que no corresponden a la estructura del tema (Guía PDF p. 60).
- No descomponer en graphic design, digital art y photography un tema de industrias creativas: la síntesis final omite música, escritura y cine (Guía PDF p. 60).

**Posible confusión con otros conceptos:**
- Source-type — separa la recolección bruta del razonamiento de síntesis, evitando la saturación de la ventana de contexto (Guía PDF p. 60).
- Functional — apropiada para pipelines secuenciales donde la salida de cada etapa es prerrequisito de la siguiente (Guía PDF p. 60).

### Ejecución paralela, secuencial y mixta

**Concepto:** Las subtareas independientes se ejecutan en paralelo; si una necesita el resultado de otra, se usa ejecución secuencial; el coordinador debe entender las dependencias y programar las subtareas en consecuencia (Guía PDF p. 60; Slides PDF p. 214).

**Ejemplos de uso (3, cortos):**
1. Paralelo: análisis financiero, de competidores y de customer sentiment se ejecutan simultáneamente; secuencial sería más lento e ineficiente (Slides PDF p. 110). Con tres agentes que esperan 8s, 7s y 7s, la espera total es de 22 segundos (Slides PDF p. 191).
2. Secuencial: una etapa de verificación debe completarse antes de una etapa de acceso, y la recolección de datos antes de la síntesis (Guía PDF p. 60).
3. Mixto: buscar material fuente (secuencial), resumir las Fuentes A, B y C (paralelo) y sintetizar en una sola pieza (secuencial) (Slides PDF p. 219). Los subtareas independientes corren en paralelo dentro de cada fase y las fases se ordenan por dependencia (Guía PDF p. 60).

**Qué NO hacer:**
- No forzar etapas secuenciales a ejecutarse en paralelo: la etapa descendente alucinará entradas que aún no recibió (Guía PDF p. 60).
- No lanzar secuencialmente tareas independientes: el paralelismo reduce el wall-clock time total (Guía PDF p. 60).

**Señal práctica:** escribir "based on the result of the previous task" en un prompt es una dependencia; usar invocación secuencial (Slides PDF p. 218). Pregunta guía: ¿alguna tarea depende de la salida de otra? Sí → secuencial; No → paralelo (Slides PDF p. 214). Para paralelizar, el coordinador invoca la Task tool para todos los temas a la vez en una sola respuesta (Slides PDF p. 201).

### Completitud de la descomposición y cuándo no descomponer

**Concepto:** Una descomposición correcta tiene distinctness (cada subtarea cubre una parte que ninguna otra cubre) y collective sufficiency (juntas cubren todo el problema); un hueco hace que la síntesis omita en silencio esa dimensión (Guía PDF p. 61).

**Ejemplos de uso (3, cortos):**
1. El coordinador evalúa la síntesis contra el enunciado original antes de devolverla al usuario (Guía PDF p. 61).
2. Si falta una dimensión o está poco respaldada, identifica el subagente responsable y re-delega un seguimiento específico (Guía PDF p. 61).
3. Alternativamente, reconoce el hueco (Guía PDF p. 61).

**Qué NO hacer:**
- No descomponer tareas simples donde un solo agente tiene contexto y herramientas suficientes: no aporta beneficio y aumenta la complejidad (Guía PDF p. 61).
- No corregir una síntesis incompleta o desequilibrada instruyendo al coordinador con más firmeza; se rediseña la descomposición (Guía PDF p. 61).

**Umbral para descomponer:** context isolation (las entradas y razonamiento de una subtarea contaminarían o agotarían el contexto del agente principal) o specialization (subtareas que requieren herramientas, modelos o contextos de instrucciones distintos que no caben en una sola configuración) (Guía PDF p. 61). Cada subagente implica un handoff de contexto, un resultado que parsear e integrar y latencia añadida (Guía PDF p. 61).

### Marco de 5 pasos y diagnóstico del pipeline de orquestación

**Concepto:** La descomposición transforma un objetivo grande en tareas pequeñas y especializadas que los subagentes ejecutan de forma independiente: entender la petición, identificar subtareas lógicas, asignar responsabilidades y asegurar que las salidas se puedan combinar (Slides PDF p. 96-97).

**Ejemplos de uso (3, cortos):**
1. Marco de 5 pasos: entender el objetivo principal, identificar subtareas independientes, asignar especialización, definir salidas esperadas y planificar la agregación (Slides PDF p. 104).
2. "Analyze this company's business performance" se descompone en financial performance, competitive positioning, operational risks y executive summary, en lugar de un vago "Analyze the company" (Slides PDF p. 98-100).
3. Diagnóstico en 4 pasos: revisar task decomposition (¿se asignaron todas las responsabilidades?), context passing, aggregation logic y workflow continuation (Slides PDF p. 155-158).

**Por qué importa:** los subagentes con responsabilidades estrechas rinden mejor porque las tareas pequeñas son más fáciles de razonar y validar y producen menos salidas inconsistentes (Slides PDF p. 102). La calidad de la descomposición determina la calidad de la salida final (Guía PDF p. 59).

**Posible confusión con otros conceptos:**
- Context passing — subagentes con contexto insuficiente producen salidas incompletas (Slides PDF p. 156).
- Aggregation logic — los subagentes dan buenas salidas pero el coordinador falla al agregar (Slides PDF p. 157).
- Workflow continuation — si el coordinador sale demasiado pronto, el flujo queda incompleto (Slides PDF p. 158).

### Trampas del examen

- Elegir dynamic adaptive decomposition para un review con aspectos conocidos (security, style, performance): añade sobrecarga innecesaria; la respuesta correcta es prompt chaining con pases enfocados (Q26; web 1.6).
- Un único pase comprehensivo "para captar preocupaciones transversales": sufre attention dilution (Q26).
- Tres agentes totalmente independientes sin contexto compartido y agregación final: pierden el contexto de integración entre archivos (Q26).
- Prompt chaining fijo (logs, configs, service calls) para un incidente de alcance desconocido: no se adapta a dependencias o patrones inesperados (Q27; web 1.6).
- Dos agentes (logs y código) que reportan a un humano: elimina la coordinación y exige síntesis manual (Q27).
- Búsqueda de archivos cambiados con lista rankeada para revisión manual: heurística de un solo pase que no usa el razonamiento del modelo (Q27).
- Proponer prompt más fuerte, modelo más potente o ventana de contexto mayor ante attention dilution; también reducir a lotes de 5 archivos sin pase de integración: los lotes pierden problemas entre lotes (web 1.6). En el escenario práctico, la respuesta correcta es la opción B: pases locales por archivo más un pase de integración (web 1.6).
- Usar fixed pipelines en tareas abiertas, o dynamic decomposition en tareas estructuradas: se elige por las características de la tarea, no por sofisticación (web 1.6).
- Ante una síntesis incompleta o desequilibrada, la causa raíz casi siempre es el diseño de la descomposición; instruir al coordinador con más firmeza no es la solución (Guía PDF p. 61).
- Particiones domain-shallow que parecen completas al diseñar pero no son collectively sufficient (Guía PDF p. 60).

## Tarea 1.7 — Manage session state, resumption, and forking (Gestionar el estado de sesión, la reanudación y el forking)

### Reanudar una sesión con nombre (--resume)

**Concepto:** una sesión es una conversación con un agente a la que se puede volver; su historial guarda el razonamiento y cada resultado de herramienta (web 1.7). `--resume <session-name>` continúa una sesión con nombre desde donde se detuvo y restaura todo el historial, incluidos los tool results (web 1.7; Guía PDF p. 143). La reanudación usa el historial y los tool results almacenados directamente, sin reprocesar la conversación desde cero (Guía PDF p. 62).

**Ejemplos de uso (3, cortos):**
1. Continuar mañana una sesión llamada `auth-deep-dive`, de 2 horas de investigación sobre flujos de autenticación, con `--resume auth-deep-dive` (Guía PDF p. 143).
2. Retomar un flujo de investigación que ya reunió evidencia en una sesión previa, para reducir llamadas redundantes a herramientas (Guía PDF p. 62).
3. Reanudar tras una noche sin cambios en los archivos, porque el contexto previo sigue siendo válido (web 1.7).

**Qué NO hacer:**
- No usar `--continue` cuando se conoce el nombre: retoma la sesión más reciente, que puede ser de otro código base (Guía PDF p. 143).
- No usar `--session-id` con un UUID: funciona, pero exige localizar el archivo de transcripción (Guía PDF p. 143).
- No empezar de cero si el contexto sigue siendo válido: se desperdicia todo el contexto previo (Guía PDF p. 143).
- No reanudar tras cambios sin avisar al agente de qué archivos cambiaron (Guía PDF p. 144; Q28).

**Posible confusión con otros conceptos:**
- Reanudar vs. reinyectar contexto — reanudar usa el historial almacenado; reinyectar exige resumir y pasar el estado en el prompt inicial de una sesión nueva, lo que es menos eficiente y más propenso a omisiones (Guía PDF p. 62).
- `--resume` vs. `fork_session` — `--resume` continúa una sola sesión de forma secuencial, no en ramas paralelas (Q29).

Detalles de uso (web 1.7, estado comprobado el 6 de octubre de 2026): `--resume` solo reanuda sesiones que ya existen, acepta un ID o nombre (o abre una lista interactiva) y nunca crea una sesión. Una sesión de CLI se nombra al inicio con `--name` / `-n`, o durante la sesión con `/rename`, y luego se continúa con `claude --resume <name>`. `-c` / `--continue` reanuda la conversación más reciente del directorio actual sin nombrar nada (web 1.7).

### fork_session (forking de sesiones)

**Concepto:** crea una rama independiente a partir de una línea base de análisis compartida; tras el fork, cada rama opera por separado y ninguna ve los resultados de la otra (web 1.7). Copia la sesión en un punto concreto y continúa dos exploraciones desde ahí (Guía PDF p. 62).

**Ejemplos de uso (3, cortos):**
1. Tras analizar un módulo de autenticación heredado, bifurcar para explorar extraer un microservicio frente a refactorizar in situ (Guía PDF p. 144).
2. Tras analizar la documentación pública de la API de un competidor, explorar paridad de funciones frente a diferenciación desde la misma base (Q29).
3. Probar una operación riesgosa en una copia aislada antes de aplicarla a la sesión principal (Guía PDF p. 62).

**Qué NO hacer:**
- No usarlo para continuar una sola línea de investigación: ahí se usa `--resume`; fork es para divergencia (web 1.7).
- No usarlo para resolver contexto obsoleto: la rama hereda los tool results obsoletos (web 1.7).
- No usarlo para dar continuidad entre días: está pensado para explorar enfoques divergentes, no para continuidad en el tiempo (Q28).
- No crear dos sesiones nuevas desde cero ni explorar secuencialmente en la misma sesión: lo primero pierde el contexto y lo segundo hace que los enfoques se contaminen (Guía PDF p. 62, 144).

**Posible confusión con otros conceptos:**
- fork vs. dos sesiones nuevas con el análisis inyectado — fork preserva el estado ya reunido y el estado vivo de la sesión; la inyección duplica contexto (Guía PDF p. 62; Q29).
- fork vs. resume — fork es para comparar alternativas; resume, para continuar (web 1.7).

En el SDK, `fork_session: true` se fija junto a `resume`, no en lugar de él: `resume` elige la sesión y `fork_session: true` inicia una sesión nueva desde una copia del historial en vez de añadir al original. La CLI empareja `--fork-session` con `--resume` del mismo modo (web 1.7).

### Contexto obsoleto (stale context) y re-análisis dirigido

**Concepto:** el stale context problem ocurre cuando el agente reanuda una sesión después de que cambiaron archivos y razona desde tool results cacheados que ya no reflejan su estado actual; un tool result es obsoleto cuando el archivo que describe cambió desde que el agente lo leyó (web 1.7). El re-análisis dirigido consiste en indicar al agente qué archivos cambiaron y dejar que re-analice solo esos (web 1.7; Guía PDF p. 144).

**Ejemplos de uso (3, cortos):**
1. Síntoma: consejos contradictorios sobre los archivos cambiados; el agente recomienda cambios ya hechos o cita código que ya no existe (web 1.7).
2. Reanudar tras un PR fusionado por un compañero durante la noche: reanudar, informar qué archivos específicos cambiaron y dejar el re-análisis dirigido de esos (Guía PDF p. 144).
3. Escenario "3 de 12 archivos cambiaron": reanudar e informar de los cambios concretos, sin releer los 12 archivos (Guía PDF p. 144; Guía PDF p. 146).

**Qué NO hacer:**
- No reanudar sin mencionar los cambios (suposiciones obsoletas sobre los archivos modificados) (Guía PDF p. 144; Q28).
- No empezar de cero si solo cambiaron unos pocos archivos conocidos: se desperdicia el contexto de los no modificados (Guía PDF p. 144; Q28).
- No hacer re-exploración completa de, por ejemplo, 50 archivos cuando solo cambiaron 3 (web 1.7).
- No confiar en que el agente detecte los cambios solo al volver a leer: no detecta modificaciones automáticamente al reanudar (Q28).

**Posible confusión con otros conceptos:**
- Re-análisis dirigido vs. re-exploración completa — avisar de los 3 archivos cambiados frente a releer todo el código base (web 1.7; Guía PDF p. 144).

**Contradicción entre fuentes:** para archivos modificados, la web 1.7 recomienda empezar una sesión nueva con resumen estructurado cuando la mayor parte de los tool results quedó obsoleta (si la mayor parte del contexto sigue válido, indica reanudar e informar de los archivos cambiados), y presenta "reanudar y pedir releer" como inferior porque los tool results obsoletos permanecen en el historial (web 1.7). La guía indica reanudar, informar de los archivos cambiados y hacer re-análisis dirigido (Guía PDF p. 144), y el banco da como correcta esa opción para tres archivos modificados (Q28). Prevalecen la guía y el banco sobre la web.

### Fresh start con inyección de resumen

**Concepto:** iniciar una sesión completamente nueva e inyectar en su contexto inicial un resumen estructurado de los hallazgos previos; la sesión no tiene tool results obsoletos, solo el resumen curado (web 1.7). Según la web, se usa cuando los tool results quedaron obsoletos por cambios en archivos, APIs o dependencias, o cuando el contexto se degradó en una sesión larga (web 1.7). Esta opción es de la web; la guía y el banco la tratan como excesiva cuando solo cambiaron pocos archivos conocidos (Q28).

**Ejemplos de uso (3, cortos):**
1. Resumen del tipo "el análisis previo encontró tres errores de precios, corregidos en estos 3 archivos; re-analiza solo estos" (web 1.7).
2. Sesión larga con historial saturado de tool results irrelevantes (web 1.7).
3. Actualización de dependencias, donde varios archivos pueden haber cambiado indirectamente (web 1.7).

**Qué NO hacer:**
- No usar fork_session para el contexto obsoleto (web 1.7).
- No pedir re-analizar los 50 archivos en la sesión nueva: basta con señalar los archivos cambiados (web 1.7).

**Posible confusión con otros conceptos:**
- Fresh start con resumen vs. reinyección manual de contexto — la guía describe la reinyección como menos eficiente y más propensa a omisiones frente a reanudar (Guía PDF p. 62).

Matriz de decisión de la web (web 1.7): sin archivos cambiados, `--resume`; comparar dos refactorizaciones, `fork_session`; modificar los 3 archivos centrales del análisis, fresh start + resumen; sesión larga con historial saturado, fresh start + resumen; probar estrategia de testing frente a documentación, `fork_session`; tras actualizar dependencias, fresh start + resumen.

### Scratchpad files (archivos de notas de trabajo)

**Concepto:** un archivo persistente en disco donde Claude registra hallazgos clave, decisiones de arquitectura y descubrimientos mientras trabaja; a diferencia del historial, que se desvanece, el archivo persiste y puede releerse (Guía PDF p. 144). Resuelven la saturación de contexto dentro de una sesión (Guía PDF p. 63).

**Ejemplos de uso (3, cortos):**
1. En una exploración de más de 30 minutos, el agente cita "patrones de renderizado típicos" en vez de las clases específicas `VulkanPipeline` y `FrameGraph` que descubrió antes (Guía PDF p. 144).
2. Escribir hallazgos intermedios y notas a un archivo, ejecutar `/clear` y releer el archivo para restaurar el estado de trabajo (Guía PDF p. 62).
3. Tarea larga que debe sobrevivir a reinicios de contexto (Guía PDF p. 63).

**Qué NO hacer:**
- No cambiar a un modelo más grande: no resuelve la dilución de atención (Guía PDF p. 144).
- No limpiar el contexto periódicamente: destruye el conocimiento acumulado (Guía PDF p. 144).
- No pre-generar resúmenes de archivos: no capturan los descubrimientos hechos durante la exploración (Guía PDF p. 144).
- No confiar solo en la reanudación: no resuelve el agotamiento de contexto dentro de una sesión (Guía PDF p. 63).

**Posible confusión con otros conceptos:**
- Scratchpad vs. persistent context storage — la guía cita "un scratchpad o una base de datos" como almacenamiento persistente para recordar salidas previas (Guía PDF p. 67; Guía PDF p. 68).

### Subagentes para gestionar contexto

**Concepto:** crear un subagente para subtareas intensivas en contexto: el coordinador recibe solo la salida final y su sesión principal se centra en el razonamiento de coordinación; las llamadas intermedias del subagente quedan aisladas en su propia sesión (Guía PDF p. 63). Si la exploración pivota a un área relacionada pero distinta y se pierde especificidad, se resumen los hallazgos y se crea un subagente con ese resumen como contexto inicial; la sesión principal conserva su conocimiento (Guía PDF p. 145).

**Ejemplos de uso (3, cortos):**
1. Leer muchos archivos grandes (Guía PDF p. 63).
2. Ejecutar comandos verbosos o búsquedas de varios pasos (Guía PDF p. 63).
3. Pasar de un subsistema de renderizado a la integración de física con un resumen como contexto (Guía PDF p. 145).

**Qué NO hacer:**
- No usar `/clear` y empezar de nuevo, ni ignorar la degradación, al pivotar a un área relacionada (Guía PDF p. 145).

**Posible confusión con otros conceptos:**
- Subagente vs. scratchpad — el subagente es preferible cuando la subtarea satura el contexto principal; si la tarea debe continuar en una sola sesión, se combina `/clear` con scratchpad (Guía PDF p. 63).

### El comando /clear

**Concepto:** restablece el contexto de la conversación (Guía PDF p. 63). Resuelve la saturación pero destruye la continuidad, salvo que el agente haya escrito antes su estado en un artefacto persistente; sin scratchpad, el agente reinicia desde cero (Guía PDF p. 63). Se usa cuando el contexto acumulado es activamente dañino, por ejemplo con suposiciones incorrectas que no se corrigen conversando (Guía PDF p. 145).

**Ejemplos de uso (3, cortos):**
1. Contexto acumulado de turnos previos que ya no se necesita (Guía PDF p. 63).
2. `/clear` con scratchpad para restaurar el estado y seguir avanzando (Guía PDF p. 63).
3. Suposiciones incorrectas acumuladas: `/clear`, frente a continuar con correcciones, que puede no sobrescribirlas (Guía PDF p. 146).

**Qué NO hacer:**
- No tratarlo como primer paso: es un último recurso y el examen suele presentarlo como distractor (Guía PDF p. 145).
- No usarlo sin scratchpad si se necesita continuidad (Guía PDF p. 63).

**Posible confusión con otros conceptos:**
- `/clear` vs. `/compact` — en Q29, usar `/compact` para "limpiar" entre exploraciones pierde el contexto base necesario (Q29).

### Trampas del examen

- Reanudar sin avisar de los archivos cambiados (Q28, opción C): el agente no detecta las modificaciones automáticamente al reanudar (Q28).
- Empezar siempre una sesión nueva (Q28, opción B): demasiado conservador cuando solo cambian pocos archivos conocidos; es válido cuando los tool results están ampliamente obsoletos (Q28).
- `fork_session` antes de ausentarse para continuidad entre días (Q28, opción D): fork es para enfoques divergentes desde una línea base compartida (Q28).
- Dos sesiones nuevas con el análisis inyectado (Q29, opción A): duplica contexto y no conserva el estado vivo de la sesión (Q29).
- `--resume` dos veces en paralelo (Q29, opción B): `--resume` continúa una sola sesión secuencialmente (Q29).
- Explorar un enfoque y luego `/compact` (Q29, opción D): pierde el contexto base para la segunda exploración (Q29).
- `--continue` en lugar de `--resume <name>`: retoma la sesión más reciente, quizá de otro proyecto (Guía PDF p. 143).
- Escenario "3 de 12 archivos": no empezar de cero, no reanudar sin mencionar cambios, no releer los 12 (Guía PDF p. 144).
- Sesión larga con respuestas inconsistentes: la respuesta es scratchpad, no modelo más grande, `/clear` periódico ni resúmenes pregenerados (Guía PDF p. 144).
- Para la pregunta de la guía sobre recordar salidas previas dentro de una sesión, la respuesta es almacenamiento y recuperación de contexto persistentes; fallan los prompts sin estado, el resumen one-shot y la copia manual de transcripciones (Guía PDF p. 67; Guía PDF p. 68).
- Trampas de la web: re-exploración completa de 50 archivos cuando solo cambian 3; reanudar cuando la mayoría de los resultados describe archivos cambiados; `fork_session` para continuar una sola línea de investigación; `fork_session` para contexto obsoleto (web 1.7).
- Degradación en tarea larga: si se puede dividir en subtareas acotadas, subagentes; si debe continuar en una sola sesión, `/clear` con scratchpad (Guía PDF p. 63).
- **Contradicción entre fuentes:** en el ejemplo en que cambian los 3 archivos centrales del análisis, la web indica fresh start con resumen porque la mayor parte de los tool results quedó obsoleta (web 1.7), mientras que guía y banco indican reanudar e informar de los cambios (Guía PDF p. 144; Q28). Prevalecen la guía y el banco.

## Ideas clave

- El agentic loop continúa con `stop_reason: "tool_use"` (ejecutar tools y añadir los resultados al historial) y termina con `"end_turn"`; esa es la señal autoritativa (web 1.1; Guía PDF p. 45-46).
- Anti-patrones de terminación: analizar lenguaje natural, usar un tope de iteraciones como mecanismo principal y usar la presencia de texto como señal de fin; un tope es solo una salvaguarda (web 1.1; Guía PDF p. 47; Q13; Q14).
- Los `tool_result` van en un único mensaje `user`, antes de cualquier texto, con `tool_use_id` que coincide con el bloque `tool_use`; omitirlos o desordenarlos provoca contexto perdido o error 400 (Guía PDF p. 46; Slides PDF p. 44).
- Hub-and-spoke: toda la comunicación pasa por el coordinator, lo que da observabilidad, manejo de errores consistente y flujo de información controlado; los subagents no se comunican directamente ni deciden por sí mismos si participan (web 1.2; Guía PDF p. 48; Q16).
- Los subagents no heredan historial: el prompt es su única entrada, así que el coordinator debe pasar contexto explícito y, para preservar atribución, contenido separado de metadatos (Guía PDF p. 49; web 1.3; Q19).
- Si la salida es incompleta, se diagnostica primero al coordinator: descomposición estrecha, paso de contexto, agregación y continuación del flujo; un hueco de cobertura se corrige re-delegando de forma dirigida (Slides PDF p. 156-158; Q7; Q17).
- Para invocar subagents hace falta "Task" (hoy Agent) en `allowedTools`; las tareas independientes se lanzan en una sola respuesta para ejecutarlas en paralelo (Slides PDF p. 108; Q18; Q20).
- fork_session crea ramas divergentes desde una base compartida; `--resume` continúa una sola sesión con nombre; tras cambios en archivos, la guía y el banco indican reanudar e informar de los archivos modificados (web 1.3; Guía PDF p. 144; Q28; Q29).
- Prompt guidance es probabilística; para dinero, seguridad o compliance se usa programmatic enforcement: prerequisite gates y hooks, no prompts reforzados, few-shot ni routing classifiers (Guía PDF p. 54-56; web 1.4; Q1; Q21).
- PreToolUse bloquea o modifica antes de ejecutar; PostToolUse corre después y sirve para normalizar resultados, no para impedir la acción (web 1.5; Slides PDF p. 257; Q23; Q24).
- Handoff estructurado: el humano no ve la transcripción, por lo que el resumen debe ser autocontenido, con customer ID y recommended action entre sus campos (web 1.4).
- Prompt chaining con pases enfocados para tareas con aspectos conocidos; dynamic adaptive decomposition para alcance desconocido; la attention dilution se resuelve con pases locales más un pase de integración (web 1.6; Q26; Q27).
- En sesiones largas, un scratchpad file o un subagent resuelve la saturación de contexto; `/clear` es último recurso y exige scratchpad si se necesita continuidad (Guía PDF p. 63, 144-145).
