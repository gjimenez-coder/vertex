# Dominio 1 — Agentic Architecture & Orchestration (Arquitectura agéntica y orquestación) — Estudio

## Tarjetas de repaso

**1.** P: ¿Qué es el agentic loop?
R: El ciclo de ejecución central de un agente basado en Claude: control de flujo determinista definido en código (no un truco de prompt, ni un retry loop, ni un turno de chatbot). Se repite mientras `stop_reason` sea `"tool_use"` y termina con `"end_turn"`.

**2.** P: ¿Qué hace el código en cada iteración cuando `stop_reason` es `"tool_use"`?
R: Ejecuta las tools, añade al historial el mensaje del assistant y los resultados como bloques `tool_result` en un único mensaje `user`, y vuelve a llamar al modelo.

**3.** P: ¿Cuáles son los tres anti-patrones de terminación del loop?
R: (1) Analizar señales en lenguaje natural ("I'm done"); (2) usar un tope de iteraciones arbitrario como mecanismo principal; (3) usar la presencia de texto del assistant como indicador de finalización.

**4.** P: ¿Qué reglas de formato aplican a los `tool_result`?
R: Van primero en el array `content` (el texto solo después), deben seguir inmediatamente al mensaje `tool_use`, y su `tool_use_id` debe coincidir exactamente con el del bloque `tool_use`; si no, la API puede devolver un error 400.

**5.** P: ¿Qué es el patrón hub-and-spoke?
R: Un coordinator central (hub) con subagents especializados (spokes). El coordinator decide qué trabajo existe, particiona el alcance, agrega resultados y es responsable de la salida final. Toda la comunicación entre subagents pasa por él.

**6.** P: ¿Qué beneficios aporta un hub único?
R: Observabilidad, manejo de errores consistente y flujo de información controlado (el coordinator decide qué contexto recibe cada subagent).

**7.** P: ¿Heredan los subagents el historial del coordinator?
R: No. Empiezan solo con lo que el coordinator incluye explícitamente en su prompt; el único canal directo del padre al subagent es el prompt string de la herramienta Agent. El padre solo recibe el mensaje final del subagent.

**8.** P: ¿Qué se necesita para que un coordinator pueda invocar subagents?
R: "Task" (hoy "Agent", renombrada en v2.1.63; Task sigue como alias) en `allowedTools`. La `description` del AgentDefinition decide cuándo se delega.

**9.** P: ¿Por qué se pasan contenido y metadatos por separado entre subagents?
R: Para que el agente posterior pueda atribuir cada afirmación (claim, source_url, document_name, page_number…). Si el coordinator los elimina, synthesis no puede citar lo que no recibió.

**10.** P: ¿Cómo se logra el spawning paralelo de subagents?
R: Emitiendo varias llamadas al Task tool en una sola respuesta del coordinator, para tareas independientes. El tiempo total es el del subagent más lento, no la suma.

**11.** P: ¿Diferencia entre `fork_session` y `--resume`?
R: `--resume` continúa una sesión concreta con nombre (secuencial). `fork_session` crea ramas independientes desde una base de análisis compartida para explorar enfoques divergentes; tras el fork, ninguna rama ve los resultados de la otra.

**12.** P: ¿Cuál es la diferencia entre prompt guidance y programmatic enforcement?
R: La prompt guidance indica qué debería hacer Claude (probabilística). La programmatic enforcement (prerequisite gates y hooks) controla qué puede hacer (determinista).

**13.** P: ¿Cuándo se exige programmatic enforcement?
R: Cuando un solo fallo causaría pérdida financiera, riesgo de seguridad o violación de compliance. Para formato o estilo basta un prompt.

**14.** P: ¿Qué es un prerequisite gate?
R: Una regla programática que impide una acción posterior hasta que los pasos previos requeridos se hayan completado con éxito (p. ej. bloquear `process_refund` hasta que `get_customer` devuelva un verified customer ID).

**15.** P: ¿Cuándo actúan PreToolUse y PostToolUse?
R: PreToolUse se ejecuta antes de la herramienta y puede permitir, bloquear o modificar la llamada. PostToolUse se ejecuta después y antes de que el modelo procese el resultado; sirve para normalizar datos, no para bloquear.

**16.** P: ¿Por qué PostToolUse no sirve para bloquear una acción?
R: Porque la herramienta ya se ejecutó; un bloqueo solo detiene el loop y no deshace el efecto secundario.

**17.** P: ¿Qué es la normalización de datos con PostToolUse?
R: Transformar la salida cruda de una herramienta a un formato consistente (timestamps a ISO 8601, códigos de estado a strings, etc.) antes de que Claude la procese, para reducir carga cognitiva y evitar inconsistencias.

**18.** P: ¿Qué debe contener un structured handoff a un humano?
R: Ser autocontenido, porque el humano no tiene la transcripción: customer ID, conversation summary, root cause analysis, refund amount (si aplica) y recommended action.

**19.** P: ¿Cuándo usar fixed sequential pipeline (prompt chaining) y cuándo dynamic adaptive decomposition?
R: Pipeline fijo cuando los pasos y aspectos se conocen de antemano (p. ej. revisión con security, style, performance). Dynamic decomposition cuando el alcance es desconocido y el plan cambia según lo descubierto (p. ej. root-cause de un bug en archivos desconocidos).

**20.** P: ¿Qué es attention dilution y cómo se resuelve?
R: Al procesar demasiados ítems en un solo pase, la profundidad del análisis se vuelve inconsistente. Se resuelve con multi-pass architecture: un pase local por ítem más un pase de integración entre ítems.

**21.** P: ¿Qué dos propiedades debe tener una buena descomposición?
R: Distinctness (cada subtarea cubre una parte que ninguna otra cubre) y collective sufficiency (juntas cubren todo el problema).

**22.** P: ¿Para qué sirven los scratchpad files y cuándo es `/clear` apropiado?
R: El scratchpad es un archivo persistente donde el agente registra hallazgos y decisiones, para resolver la saturación de contexto en sesiones largas. `/clear` es último recurso y exige scratchpad si se necesita continuidad.

## Preguntas de autoevaluación

**1.** Un agente se detiene a mitad de una tarea compleja porque el código comprueba `response.content[0].type == "text"` para dar por terminado. ¿Cuál es la corrección?
R: Continuar el loop con `stop_reason == "tool_use"` y terminar solo con `"end_turn"`; Claude puede devolver texto junto con bloques `tool_use`. Un tope de iteraciones no corrige una salida prematura. (Tarea 1.1 — Anti-patrones de terminación del loop; Trampas del examen)

**2.** ¿Qué papel debe tener un tope de 15 tool calls en el loop?
R: Es una salvaguarda contra agentes descontrolados y costes, no el mecanismo principal de parada; `stop_reason: "end_turn"` sigue siendo la señal autoritativa. (Tarea 1.1 — Anti-patrones de terminación del loop; Q14)

**3.** Un reporte sobre «impacto de la IA en industrias creativas» omite música, escritura y cine, aunque todos los subagents terminaron con éxito. ¿Cuál es la causa y por qué no son las demás?
R: Descomposición estrecha del coordinator (solo arte digital, diseño gráfico y fotografía). Los subagents ejecutaron correctamente lo asignado; mejorar synthesis, las consultas de búsqueda o el filtrado de document analysis no arregla lo que nunca se asignó. (Tarea 1.2 — Partición del alcance y descomposición estrecha; Q7)

**4.** Una pregunta factual simple tarda 45 segundos porque pasa por los cuatro subagents. ¿Qué diseño es correcto?
R: Selección dinámica: el coordinator analiza la consulta e invoca solo los subagents necesarios. Una tabla de palabras clave es frágil, la autoselección por los subagents rompe hub-and-spoke y fusionar a dos reduce capacidad. (Tarea 1.2 — Selección dinámica de subagents; Q16)

**5.** Document analysis cubrió 3 de 5 fuentes. ¿Cómo se completa el trabajo?
R: Re-invocar el subagent con un prompt explícito con solo las 2 fuentes faltantes, incluyendo los hallazgos previos como contexto. Pedir a synthesis que infiera fabrica contenido; reenviar las 5 fuentes reprocesa; que el coordinator las analice se salta la arquitectura. (Tarea 1.2 — Agregación y bucles de refinamiento iterativo; Q17)

**6.** El coordinator tiene `["web_search", "read_document"]` en `allowedTools` y no puede crear subagents. ¿Por qué?
R: Falta "Task" (hoy Agent) en `allowedTools`. El system prompt no concede la capacidad; `subagent_endpoint` y plan mode son distractores. (Tarea 1.3 — Task tool y allowedTools; Q18)

**7.** Las afirmaciones del informe final perdieron sus citas. Los prompts y las tools no cambiaron. ¿Causa más probable?
R: El coordinator pasó contenido sin metadatos estructurados; synthesis no puede citar lo que no recibió. Cambiar el prompt de synthesis o darle búsqueda propia no lo resuelve. (Tarea 1.3 — Metadatos estructurados; Q19)

**8.** Un agente de soporte reembolsa sin verificar la titularidad en el 8% de los casos aunque el prompt lo exige. ¿Qué solución es correcta?
R: Un prerequisite gate programático que bloquee `process_refund` (y `lookup_order`) hasta que `get_customer` devuelva un verified customer ID. Prompts más fuertes, few-shot y routing classifiers no garantizan el orden. (Tarea 1.4 — Prerequisite gate; Trampas del examen; Q1; Q21)

**9.** Un cliente combina devolución, disputa de cargo y cambio de email en un mensaje. ¿Cómo se maneja?
R: Descomponer en elementos, investigar cada uno en paralelo con el contexto compartido del cliente y compilar una respuesta unificada. Tratarlos por turnos o en tickets separados empeora la experiencia. (Tarea 1.4 — Multi-concern request handling; Q22)

**10.** Las reglas de reembolso en el system prompt se violan en ~3% de los casos. ¿Qué mecanismo usar y cuál es un error?
R: Un hook PreToolUse que bloquee antes de ejecutar (p. ej. reembolsos superiores a $500). Es error validar y revertir con PostToolUse, porque la violación ya ocurrió. (Tarea 1.5 — PreToolUse: aplicación de políticas; Q24)

**11.** Tres backends devuelven fechas y estados en formatos distintos y el modelo los interpreta mal. ¿Dónde se corrige?
R: En un hook PostToolUse que normalice los resultados antes de que el modelo los procese. Instrucciones de conversión en el prompt son probabilísticas y reformatear la respuesta final llega después de que el modelo razonó con datos inconsistentes. (Tarea 1.5 — PostToolUse: normalización de datos; Q23)

**12.** Revisión de PR con tres aspectos conocidos (security, style, performance). ¿Qué patrón y por qué?
R: Prompt chaining con pases secuenciales enfocados, uno por aspecto. Un solo pase sufre attention dilution y dynamic decomposition añade sobrecarga innecesaria. (Tarea 1.6 — Fixed sequential pipeline; Attention dilution; Q26)

**13.** Hay que investigar la causa raíz de un bug de alcance desconocido de las últimas dos semanas. ¿Qué descomposición?
R: Dynamic adaptive decomposition: mapear lo afectado y generar subtareas según lo descubierto. Un pipeline fijo no se adapta y dividir en dos agentes que reportan a un humano pierde la coordinación. (Tarea 1.6 — Dynamic adaptive decomposition; Q27)

**14.** Se reanuda una sesión tras cambiar 3 de 12 archivos. ¿Qué se hace según la guía y el banco?
R: Reanudar con `--resume`, informar al agente de qué archivos cambiaron y hacer re-análisis dirigido de esos. No empezar de cero, no reanudar sin avisar y no releer los 12. (Tarea 1.7 — Contexto obsoleto y re-análisis dirigido; Q28)

**15.** Tras analizar la documentación de un competidor, se quieren explorar paridad de funciones y diferenciación desde la misma base. ¿Qué mecanismo?
R: `fork_session`, que preserva el estado reunido y crea ramas divergentes. Dos sesiones nuevas con inyección duplican contexto, `--resume` en paralelo no aplica y `/compact` pierde el contexto base. (Tarea 1.7 — fork_session; Q29)

## Checklist

### Tarea 1.1 — Agentic loops
- [ ] El loop llama a la Messages API con el historial completo en cada iteración.
- [ ] Se inspecciona `stop_reason`: `"tool_use"` continúa y `"end_turn"` termina.
- [ ] Se manejan explícitamente los demás valores (`max_tokens`, `stop_sequence`, `pause_turn`, `refusal`, `model_context_window_exceeded`).
- [ ] Se extraen todos los bloques `tool_use` (no solo el primero) y se conserva su ID.
- [ ] Se añade la respuesta del assistant y luego los `tool_result` en un único mensaje `user`, con `tool_use_id` coincidente y sin texto antes de ellos.
- [ ] No se usa lenguaje natural, tope de iteraciones ni presencia de texto como señal principal de fin.
- [ ] Existe un guard de iteraciones máximo solo como salvaguarda.
- [ ] Las reglas de negocio con cumplimiento obligatorio están en código, no solo en el prompt.

### Tarea 1.2 — Coordinator-subagent
- [ ] Toda la comunicación entre subagents pasa por el coordinator.
- [ ] El coordinator selecciona solo los subagents necesarios para cada consulta.
- [ ] La partición del alcance es distinta y colectivamente suficiente.
- [ ] Los huecos de cobertura se corrigen con re-delegación dirigida y bucle de refinamiento.
- [ ] Ante salida incompleta se revisa primero al coordinator: descomposición, paso de contexto, agregación y continuación del flujo.
- [ ] Las salidas de los subagents son estructuradas y preservan la atribución.

### Tarea 1.3 — Invocación y contexto de subagents
- [ ] "Task"/"Agent" está en `allowedTools` del coordinator.
- [ ] Cada AgentDefinition tiene description específica, system prompt y `tools` restringidas a su rol.
- [ ] El prompt de delegación incluye objetivo, contexto relevante, restricciones y salida esperada.
- [ ] Contenido y metadatos (URL, documento, página) viajan por separado.
- [ ] Las tareas independientes se lanzan en una sola respuesta; las dependientes, en secuencia.
- [ ] Se recogen todos los resultados antes de sintetizar.
- [ ] Se elige `fork_session` para divergir y `--resume` para continuar.

### Tarea 1.4 — Enforcement y handoff
- [ ] Se clasifica cada operación: dinero, seguridad o compliance → enforcement programático; formato o estilo → prompt.
- [ ] Las dependencias de orden están implementadas como prerequisite gates con respuesta controlada (`allowed`, `reason`, `next_action`).
- [ ] Las peticiones con varios asuntos se descomponen, se investigan en paralelo y se responden de forma unificada.
- [ ] El handoff a un humano es autocontenido: customer ID, resumen, root cause analysis, importe y recommended action.

### Tarea 1.5 — Hooks del Agent SDK
- [ ] Las políticas bloqueantes (umbrales, AML, aprobaciones) usan PreToolUse.
- [ ] La normalización de resultados usa PostToolUse.
- [ ] Los matchers tienen el alcance justo, ni demasiado amplios ni demasiado estrechos.
- [ ] El hook de normalización devuelve solo el resumen formateado, sin duplicar la salida cruda.
- [ ] Las reglas que deben cumplirse el 100% no dependen de CLAUDE.md ni de prompts.

### Tarea 1.6 — Descomposición de tareas
- [ ] Aspectos conocidos y entrada estructurada → fixed pipeline; alcance desconocido → dynamic decomposition.
- [ ] Las revisiones de muchos ítems usan pases locales más un pase de integración.
- [ ] Se eligió la dimensión de descomposición (dominio, tipo de fuente o funcional) según la naturaleza de la tarea.
- [ ] Se identificó qué subtareas son independientes (paralelo) y cuáles dependen de otras (secuencial).
- [ ] La síntesis se evalúa contra el enunciado original y los huecos se re-delegan.
- [ ] No se descomponen tareas simples que un solo agente puede resolver.

### Tarea 1.7 — Sesiones
- [ ] Se usa `--resume <nombre>` para continuar una sesión conocida (no `--continue` si se conoce el nombre).
- [ ] Tras cambios en archivos, se informa al agente de cuáles cambiaron y se hace re-análisis dirigido.
- [ ] Se usa `fork_session` para comparar enfoques divergentes desde una base compartida.
- [ ] En sesiones largas, los hallazgos se guardan en un scratchpad file.
- [ ] Las subtareas intensivas en contexto se delegan a un subagent.
- [ ] `/clear` se reserva como último recurso y se combina con scratchpad si se necesita continuidad.
