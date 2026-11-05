# Dominio 2 — Tool Design & MCP Integration — Estudio

## Tarjetas de repaso

1. P: ¿Qué peso tiene el Dominio 2 en el examen y de qué trata?
   R: Pesa un 18% y trata de cómo se diseñan, distribuyen e integran las herramientas que usa Claude (Lo que necesitas saber).

2. P: ¿Ejecuta Claude las herramientas?
   R: No. Envía una solicitud estructurada con nombre y parámetros, y el código de la aplicación decide si ejecutar, rechazar o modificar (Tarea 2.1).

3. P: ¿Cuál es el mecanismo primario con el que Claude elige una herramienta?
   R: La tool description. El name tiene impacto menor y el input schema determina si Claude puede construir una llamada válida (Tarea 2.1).

4. P: ¿Cuáles son los cinco elementos de una descripción de producción?
   R: Qué hace, qué entradas espera, ejemplos de consultas que maneja bien, casos límite y limitaciones, y límites explícitos frente a herramientas similares (Tarea 2.1).

5. P: ¿Qué es el misrouting y cuál es su causa habitual?
   R: Que Claude elija la herramienta equivocada; suele deberse a descripciones solapadas o difusas entre herramientas (Tarea 2.1).

6. P: ¿Cuál es el primer paso para corregir un misrouting?
   R: Expandir y desambiguar las descripciones (entradas, salidas, cláusula "Do NOT use"). Few-shot, routing classifier y consolidación son opciones secundarias o más costosas (Tarea 2.1).

7. P: ¿Cuándo se aplica tool splitting?
   R: Cuando una herramienta genérica (p. ej. analyze_document) hace demasiado: se divide en herramientas específicas con contrato de entrada/salida, no con un parámetro mode (Tarea 2.1).

8. P: ¿Qué hace el flag `isError` (`is_error` en la guía)?
   R: Indica que la ejecución de la herramienta falló, para que el modelo razone sobre la recuperación en vez de leer el texto como un resultado normal (Tarea 2.2).

9. P: ¿Cuáles son las cuatro categorías de error de la web y el banco, y su recuperación?
   R: transient (reintentar tras espera), validation (corregir la entrada), business (no reintentar; alternativa o escalar) y permission (otras credenciales o escalar) (Tarea 2.2).

10. P: ¿Qué pregunta responde `isRetryable`?
    R: Si reenviar esta misma solicitud funcionaría. Solo transient lleva `true` (Tarea 2.2).

11. P: ¿Diferencia entre access failure y valid empty result?
    R: Access failure: la herramienta no llegó a la fuente, no se ejecutó la consulta, es un error. Valid empty result: la consulta se ejecutó y no halló coincidencias; no es error y no se reintenta (Tarea 2.2).

12. P: ¿Qué principio rige la propagación de errores en sistemas multi-agente?
    R: Recuperar localmente y propagar selectivamente, incluyendo resultados parciales y lo intentado (Tarea 2.2).

13. P: ¿Qué es least privilege aplicado a herramientas y cómo se implementa?
    R: Cada agente recibe solo las herramientas que su rol necesita, mediante `allowedTools` (Tarea 2.3).

14. P: ¿Qué es una scoped cross-role tool?
    R: Una herramienta restringida que da a un agente acceso directo a una capacidad de otro rol para solicitudes simples y frecuentes (p. ej. `verify_fact`); los casos complejos siguen por el coordinator (Tarea 2.3).

15. P: ¿Diferencia entre `auto`, `any` y forced selection en `tool_choice`?
    R: `auto`: el modelo decide si llama a una herramienta o responde texto. `any`: debe llamar a una herramienta, elige cuál. Forced selection: debe llamar a una herramienta concreta (Tarea 2.3).

16. P: ¿Qué garantiza strict tool use y qué no?
    R: Elimina errores de sintaxis (JSON mal formado, campos ausentes, tipos erróneos) pero no los semánticos, que requieren una capa de validación (Tarea 2.3).

17. P: ¿Qué expone un servidor MCP?
    R: Tools (funciones invocables), resources (catálogos de contenido de solo lectura) y prompts (plantillas invocadas como slash commands) (Tarea 2.4).

18. P: ¿Diferencia entre `.mcp.json` y `~/.claude.json`?
    R: `.mcp.json` está en la raíz del proyecto, se versiona y es compartido con el equipo; `~/.claude.json` está en el home y es personal (Tarea 2.4).

19. P: ¿Cómo se evita exponer credenciales en `.mcp.json`?
    R: Con la expansión `${VAR}` (y `${VAR:-default}`): el archivo guarda nombres de variables y cada desarrollador define los valores localmente (Tarea 2.4).

20. P: ¿Para qué sirven los MCP resources?
    R: Exponen un catálogo de contenido desde el principio, de modo que el agente evita llamadas exploratorias para descubrir qué datos existen (Tarea 2.4).

21. P: ¿Cuándo usar Grep y cuándo Glob?
    R: Grep busca patrones en el contenido de los archivos; Glob busca archivos por nombre o ruta (Tarea 2.5).

22. P: ¿Cómo funciona Edit y qué se hace si falla por coincidencia no única?
    R: Reemplaza texto exacto `old_string` → `new_string`, que debe ser único. Según la guía, el fallback es Read → modificar → Write; el banco (Q40) prioriza ampliar `old_string` tras un Read (Tarea 2.5).

## Preguntas de autoevaluación

1. P: Un agente envía "Check my order #12345" a get_customer en lugar de lookup_order. ¿Cuál es el primer arreglo y por qué no few-shot ni un routing classifier?
   R: Mejorar las descripciones de ambas herramientas con límites explícitos. Few-shot añade tokens sin corregir la causa raíz (descripciones que no diferencian), y el classifier es sobreingeniería como primer paso (Tarea 2.1, Trampas del examen; Q2).

2. P: Tras reescribir las descripciones el misrouting persiste. ¿Qué más conviene revisar?
   R: El system prompt: instrucciones con palabras clave (p. ej. "Always check customer details before proceeding") pueden asociarse a una herramienta y anular las descripciones (Tarea 2.1, Interacción con el system prompt).

3. P: El agente envía "order from last Tuesday" a lookup_order, que espera ISO-8601. ¿Cuál es la mejor corrección?
   R: Poner restricciones de formato, valores aceptados y ejemplos en la descripción de la herramienta. Es más robusto que una instrucción en el system prompt; la validación del schema no evita que el modelo envíe entradas mal formadas, y dividir por id/fecha resuelve otro problema (Tarea 2.1, Descripciones de parámetros; Q30).

4. P: Tres herramientas con nombres similares consultan backends distintos y el agente las confunde. ¿Qué solución plantea el banco?
   R: Renombrarlas según su fuente de datos y reescribir sus descripciones (qué datos devuelve, qué backend consulta, qué caso de uso cubre). Consolidar en una herramienta con parámetro `source` o listar reglas en el system prompt no arreglan la raíz (Tarea 2.1, Tool renaming; Q31).

5. P: `process_refund` devuelve `{"status": "error", "message": "Operation failed"}` y el agente se disculpa y termina siempre. ¿Qué se debe devolver?
   R: Una respuesta con `errorCategory`, `isRetryable` y una explicación específica. Los códigos HTTP, el stack trace y los códigos numéricos en el system prompt son peores opciones (Tarea 2.2, Trampas del examen; Q32).

6. P: Una API caída devuelve `{"results": [], "status": "success"}` y el agente informa "no existe". ¿Cuál es el fallo y su corrección?
   R: La herramienta no distingue el fallo de acceso del resultado vacío válido. Debe usar `isError` para el fallo de acceso; rellenar contenido, añadir `confidence` o reintentar internamente no lo resuelven (Tarea 2.2, Access failure vs valid empty result; Q33).

7. P: Un bloqueo por fraude se reintentó tres veces y cada intento generó una alerta de cumplimiento. ¿Qué faltó?
   R: `isRetryable: false` más una explicación para el cliente; sin metadatos el agente asumió que era transitorio (Tarea 2.2, Qué señala isRetryable; Q34).

8. P: Un subagente de búsqueda web agota el tiempo. ¿Qué debe recibir el coordinador?
   R: Un contexto de error estructurado con tipo de fallo, consulta intentada, resultados parciales y alternativas; no un resultado vacío "exitoso" ni terminar todo el flujo (Tarea 2.2, Propagación de errores; Q8).

9. P: Un synthesis agent con 18 herramientas inicia nuevas búsquedas web en lugar de sintetizar. ¿Cuál es la causa?
   R: Tener herramientas fuera de su especialización aumenta el mal uso. La corrección es restringirle las herramientas a su rol (Tarea 2.3, Tool distribution; Q35).

10. P: El 85% de las verificaciones del synthesis agent son simples y pasar por el coordinator añade 2-3 round trips. ¿Qué diseño se elige?
    R: Un `verify_fact` scoped en el synthesis agent; el 15% complejo sigue al web search agent vía coordinator. Acumular en lote o dar todas las herramientas de web search son opciones peores (Tarea 2.3, Scoped cross-role tools; Q9).

11. P: ¿Cómo garantizar que `generate_summary` se llame siempre?
    R: Con `tool_choice: {"type": "tool", "name": "generate_summary"}`. `auto` permite responder sin herramienta, `any` no garantiza cuál, y quitar las otras herramientas elimina las necesarias (Tarea 2.3, tool_choice; Q36).

12. P: ¿Cómo comparte un equipo un servidor MCP de GitHub sin exponer el token?
    R: `.mcp.json` en el proyecto, versionado, con `${GITHUB_TOKEN}`. No sirve `~/.claude.json` por desarrollador con el token incrustado, ni una sección `[mcp_servers]` en CLAUDE.md (no existe), ni un script manual (Tarea 2.4, Trampas del examen; Q37).

13. P: El agente hace muchas llamadas exploratorias para descubrir qué datos hay en varios servidores MCP. ¿Qué solución se elige?
    R: Exponer catálogos de contenido como MCP resources. Un meta-tool `list_tools`, fusionar herramientas o una caché tratan síntomas (Tarea 2.4, MCP resources; Q38).

14. P: ¿Cómo se encuentran todos los archivos que importan `legacy-auth`?
    R: Con un Grep del patrón de import. Bash con find/grep es menos adecuado, Glob + Read de cada archivo es menos eficiente, y Read no sirve para recorrer directorios (Tarea 2.5, Grep vs Glob; Q39).

15. P: Edit falla con "Match not unique: found 3 occurrences". ¿Qué haces según Q40?
    R: Read del archivo y reintento de Edit con un `old_string` mayor y único. `sed` reemplaza todas, Read + Write es válido solo si no hay anchor único, y Edit no soporta un parámetro de número de línea (Tarea 2.5, Qué hacer cuando Edit falla; Q40).

## Checklist

### Tarea 2.1 — Interfaces de herramientas
- [ ] Cada descripción dice qué hace, entradas esperadas, ejemplos de consultas, casos límite y límites explícitos.
- [ ] Cada herramienta con alcance cercano a otra incluye una cláusula "Do NOT use" que nombra a la otra.
- [ ] Ante un misrouting: reproducir la solicitud, comparar descripciones lado a lado, identificar la señal que faltaba y añadirla.
- [ ] Las herramientas genéricas se dividen en herramientas específicas con contrato de entrada/salida, no con un parámetro mode.
- [ ] Los nombres no son genéricos (helper, process, handle, execute) y son coherentes con la descripción.
- [ ] Cada parámetro tiene descripción con formato, valores aceptados y ejemplo.
- [ ] Tras actualizar descripciones, se revisa el system prompt por palabras clave que afecten la selección.
- [ ] Se comprueba si el problema es de descripciones o del tamaño del conjunto de herramientas.

### Tarea 2.2 — Errores estructurados en MCP
- [ ] Los fallos se devuelven con `isError: true` (`is_error` en la guía).
- [ ] Cada error lleva categoría, `isRetryable` y una descripción específica.
- [ ] Las categorías se usan de forma consistente en todas las herramientas.
- [ ] Solo transient se marca como reintentable; business y permission no se reintentan.
- [ ] Un fallo de acceso nunca se devuelve como resultado vacío; un resultado vacío válido se devuelve como éxito.
- [ ] Un permission error no expone detalles internos.
- [ ] El subagente reintenta localmente los fallos transient y propaga lo irresoluble con resultados parciales y lo intentado.

### Tarea 2.3 — Distribución de herramientas y tool_choice
- [ ] Cada agente tiene `allowedTools` acotado a su rol.
- [ ] Ningún subagent recibe la herramienta Agent ni todas las herramientas "por flexibilidad".
- [ ] Se decide entre mejorar descripciones, dividir por rol o consolidar variaciones del mismo trabajo en una herramienta parametrizada, según el diagnóstico.
- [ ] Las herramientas genéricas (fetch_url) se sustituyen por versiones restringidas (load_document) cuando el rol lo permite.
- [ ] Las solicitudes simples y frecuentes usan una scoped cross-role tool cuyo schema limita el alcance.
- [ ] `tool_choice` se elige según la necesidad: `auto`, `any` o forced selection (`none` en la guía para solo texto).
- [ ] Si se requiere salida estructurada garantizada, no se usa `auto`.
- [ ] Se añade una capa de validación para errores semánticos aunque se use strict tool use.

### Tarea 2.4 — Integración de servidores MCP
- [ ] Los servidores del equipo van en `.mcp.json` y los personales o experimentales en `~/.claude.json`.
- [ ] Los secretos se referencian con `${VAR}` y nunca se escriben en el archivo.
- [ ] Las entradas remotas declaran `"type": "http"` con `url`; las locales declaran `command` y `args`.
- [ ] Se exponen catálogos como MCP resources para evitar llamadas exploratorias.
- [ ] Para integraciones estándar, se evalúan primero los servidores de la comunidad.
- [ ] Las tools MCP tienen descripciones detalladas para competir con las integradas.
- [ ] Ante un servidor que no aparece, se revisa en orden: config file, server running, approval, environment variables.
- [ ] Los prompts MCP se invocan como slash commands, no se esperan cargados en el contexto.

### Tarea 2.5 — Herramientas integradas
- [ ] Búsqueda por contenido con Grep y por nombre o ruta con Glob.
- [ ] Cambios dirigidos con Edit; Write solo para archivos nuevos o sobrescrituras completas.
- [ ] Si Edit falla por coincidencia no única: Read y ampliar `old_string`; si no hay anchor único, Read → Write.
- [ ] Se prefieren las herramientas dedicadas a Bash (find, grep, sed) y no se ejecutan comandos Bash destructivos sin validar.
- [ ] La exploración es incremental: Grep de puntos de entrada, Read de lo necesario, justificando cada archivo.
- [ ] Para rastrear usos se revisan wrappers y barrel files y se hace Grep de cada nombre exportado.
- [ ] Para callers y tests: Grep, luego Glob de tests hermanos, luego Grep de wrappers.
- [ ] Se usa ToolSearch para cargar herramientas bajo demanda en lugar de cargarlas todas al inicio.
