# Verificación de fidelidad — .

Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.

| Capítulo | Hallazgos | Alta | Media | Baja |
|---|---|---|---|---|
| 1.1 | 3 | 0 | 1 | 2 |
| 1.2 | 2 | 0 | 0 | 2 |
| 1.3 | 1 | 0 | 0 | 1 |
| 1.4 | 1 | 0 | 0 | 1 |
| 1.5 | 2 | 0 | 1 | 1 |
| 1.6 | 2 | 0 | 0 | 2 |
| 1.7 | 3 | 0 | 1 | 2 |
| 2.1 | 3 | 0 | 0 | 3 |
| 2.2 | 2 | 0 | 0 | 2 |
| 2.3 | 2 | 0 | 0 | 2 |
| 2.4 | 1 | 0 | 0 | 1 |
| 2.5 | 3 | 0 | 0 | 3 |
| 3.1 | 3 | 0 | 0 | 3 |
| 3.2 | 2 | 0 | 0 | 2 |
| 3.3 | 0 | 0 | 0 | 0 |
| 3.4 | 3 | 0 | 0 | 3 |
| 3.5 | 2 | 0 | 1 | 1 |
| 3.6 | 4 | 0 | 1 | 3 |
| 4.1 | 3 | 0 | 0 | 3 |
| 4.2 | 2 | 0 | 1 | 1 |
| 4.3 | 2 | 0 | 0 | 2 |
| 4.4 | 2 | 0 | 0 | 2 |
| 4.5 | 0 | 0 | 0 | 0 |
| 4.6 | 2 | 0 | 0 | 2 |
| 5.1 | 3 | 0 | 1 | 2 |
| 5.2 | 2 | 0 | 0 | 2 |
| 5.3 | 1 | 0 | 0 | 1 |
| 5.4 | 2 | 0 | 0 | 2 |
| 5.5 | 3 | 0 | 0 | 3 |
| 5.6 | 0 | 0 | 0 | 0 |

**Total:** 61 hallazgos (alta 0, media 7, baja 54) en 30 capítulos.

## Detalle

## 1.1 — Design and implement agentic loops for autonomous task execution
Hallazgos: 3 (alta 0, media 1, baja 2)
- [media] «Los distractores A, C y D (datos binarios, más de 10 llamadas, resultados más rápidos de 200 ms) no son modos de fallo reconocidos (Q15)» → la fuente solo descarta C y D como modos de fallo no reconocidos; la opción A se califica como preocupación válida pero no el riesgo principal; evidencia: «Option A is a valid concern but not the primary performance risk for text-based research tasks. Options C and D are not recognized failure modes» (Q15)
- [baja] Sección «When Not to Use Agentic Architecture» omitida (tareas simples y deterministas, validación estática, exportes programados, check de cumplimiento obligatorio, etc.) → el apunte no recoge cuándo no usar arquitectura agéntica; evidencia: «Do not use agentic architecture when the task is simple, deterministic, and better handled by fixed application logic» (Guía PDF p. 42)
- [baja] Ejercicio práctico «Build a Multi-Tool Agent Loop» (calculator + web search stub, probar llamadas secuenciales) omitido; solo se recoge el tope de seguridad de 20 → omisión de detalle del ejercicio; evidencia: «Set up a Claude API client with two tools: a calculator tool ... and a web search stub» (web 1.1)

## 1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] Omisión: el apunte no enumera las cuatro responsabilidades del coordinator (selección dinámica, partición del alcance, refinamiento iterativo y enrutamiento centralizado de la comunicación); las tres primeras están dispersas y la cuarta solo aparece implícita → sección omitida; evidencia: «The coordinator has four responsibilities.» (web 1.2)
- [baja] «en el escenario de práctica la opción B es la correcta frente a synthesis, document analysis y web search (web 1.2)» → la fuente web no marca la respuesta correcta del escenario; la opción B se infiere de la trampa de examen; evidencia: «Option BThe coordinator’s task decomposition assigned only solar and wind, omitting the other renewable categories.» (web 1.2)

## 1.3 — Configure subagent invocation, context passing, and spawning
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Prevalece la guía en el mecanismo (sin la herramienta en la lista, el spawn pasa por el permission callback y en una ejecución desatendida se deniega)» → la guía solo dice que allowedTools sirve para auto-aprobar la invocación; el permission callback y la denegación en ejecución desatendida provienen únicamente de la web 1.3, no de la guía; evidencia: «include Agent in allowedTools so Claude can auto-approve subagent invocation without a permission prompt» (Guía PDF p. 51); «In an unattended run, that callback denies the spawn» (web 1.3)

## 1.4 — Implement multi-step workflows with enforcement and handoff patterns
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] Sección «Prompt guidance vs programmatic enforcement» sin el concepto de «Deterministic Compliance» → omitido: la guía lo define como subsección propia; evidencia: «the system enforces a rule every time, regardless of how Claude interprets the prompt» (Guía PDF p. 55)

## 1.5 — Apply Agent SDK hooks for tool call interception and data normalization
Hallazgos: 2 (alta 0, media 1, baja 1)
- [media] «(Guía PDF p. 56)», «(Guía PDF p. 57)», «(Guía PDF p. 58)» (todas las citas de la guía) → la numeración usa el folio impreso, no el marcador [[PDF p.N]]; deben ser +1 (p. 57, 58 y 59 respectivamente). Ej.: «primary mechanism for deterministic enforcement» está bajo [[PDF p.57]], no p. 56; exit code 2 y normalización, bajo [[PDF p.58]]; matchers y CLAUDE.md advisory, bajo [[PDF p.59]]; evidencia: «Hooks are the primary mechanism for deterministic enforcement» (PDF p. 57)
- [baja] Sección sobre lo que habilitan los hooks de interceptación (Slides PDF p. 248) omitida → no se mencionan los patrones Sandbox Paths, Convention Normalization, Deployment Safety, Path Correction, Secret Scrubbing y Parameter Injection; evidencia: «Sandbox Paths Convention Normalization Deployment Safety Path Correction Secret Scrubbing Parameter Injection» (PDF p. 248)

## 1.6 — Design task decomposition strategies for complex workflows
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] Sección omitida: el ejemplo hilo conductor de la lección web (el joyero: revisión de 40 listings con pipeline fijo vs. discrepancia de stock con descomposición dinámica; listing 3 vs. 31 con el mismo hallmark ausente) → no aparece en el apunte; evidencia: «The jeweller's listing check has known steps and needs a fixed pipeline. The stock mismatch has unknown scope and needs dynamic decomposition.» (web 1.6)
- [baja] Sección «Ejecución paralela, secuencial y mixta» → omite que la ejecución paralela es el patrón preferido en flujos investigativos o de investigación con varios flujos de evidencia; evidencia: «is the preferred pattern for investigative or research workflows where multiple evidence streams can be gathered simultaneously» (PDF p. 60, Guía)

## 1.7 — Manage session state, resumption, and forking
Hallazgos: 3 (alta 0, media 1, baja 2)
- [media] «para archivos modificados, la web 1.7 recomienda empezar una sesión nueva con resumen estructurado» (y «en el ejemplo de 3 archivos modificados, la web indica fresh start») → generaliza en exceso la postura de la web: solo recomienda fresh start cuando los tool results son obsoletos en su mayoría (los 3 archivos centrales de los que dependía casi todo el análisis) y dice expresamente que, si la mayor parte del contexto sigue válido, se reanuda e informa de los archivos cambiados; la contradicción con la guía/Q28 es más matizada de lo que presenta el apunte; evidencia: «If most of the context is still valid, resume and tell the agent which files changed.» (web 1.7)
- [baja] Sección omitida: el Build Exercise y el Practice Scenario de la web (sesión con 3 de 50 archivos modificados, opciones A-D, ejercicio de 6 pasos de resume vs. fresh start) no aparecen en el apunte; evidencia: «Build Exercise … Implement Session Management Strategies» (web 1.7)
- [baja] Omisión de matices: no se recogen los criterios de la guía para usar forking cuando «the next step in a workflow is uncertain» ni el matiz de la web de que el modelo tiende a referirse a información antigua sobre todo en decisiones tangenciales tras pedir releer; evidencia: «when the next step in a workflow is uncertain and both branches need to be explored» (PDF p. 62)

## 2.1 — Design effective tool interfaces with clear descriptions and boundaries
Hallazgos: 3 (alta 0, media 0, baja 3)
- [baja] «Few-shot examples — arreglan formato de salida y juicio, no la selección de herramienta (Guía PDF p. 77)» (también en Trampas del examen) → página incorrecta: el EXAM TIP aparece en el marcador p. 78, no en p. 77; evidencia: «Few-shot examples in the prompt do not fix tool misrouting, they fix output format and judgment, not tool selection» (Guía PDF p. 78)
- [baja] «Para el examen prevalecen la guía y el material oficial sobre la web; usa el ejemplo de 18 frente a 4-5 (web 2.1)» → la cifra 18 frente a 4-5 solo aparece en la web (no en el texto de la guía PDF); la afirmación de que la guía prevalece no está respaldada para esa cifra; evidencia: «The guide's example is 18 tools against 4-5» (web 2.1)
- [baja] Omisión: el Worked Example de la guía «Tool Description Rewrite for a Support System» (get_customer, get_orders, process_refund) no se recoge; evidencia: «A customer support system has three tools. The current descriptions cause frequent misrouting.» (Guía PDF p. 98)

## 2.2 — Implement structured error responses for MCP tools
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «Omitir la bandera de retryability: el agente acaba reintentando todo o nada (Guía PDF p. 82; Guía PDF p. 81)» → la cita a la p. 81 no respalda esta afirmación; solo aparece en la p. 82; evidencia: «Omitting the retryability flag, so the agent either retries everything or retries nothing.» (Guía PDF p. 82)
- [baja] Ejercicio práctico (Build Exercise) de la lección web omitido: no se recogen el servidor MCP con `customer_lookup` y `failure_mode`, ni el bucle de agente que ramifica por `errorCategory` (reintento de transient hasta 3 veces con backoff, escalado de business, solicitud de credenciales en permission); evidencia: «retries transient errors up to 3 times with backoff... escalates business errors to a human, and requests elevated credentials for permission errors» (web 2.2)

## 2.3 — Distribute tools appropriately across agents and configure tool_choice
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «Prevalecen la guía y el banco como fuentes de examen; la pregunta Q9 es la que prueba el patrón, y se entiende `verify_fact` como excepción scoped para el caso simple.» → la guía (synthesis sin herramientas) y el banco (Q9, `verify_fact` scoped) se contradicen entre sí; la conciliación como «excepción» es una interpretación que ninguna fuente respalda; evidencia: «Synthesis Agent: allowedTools = []. Works entirely from the outputs passed by the coordinator» (Guía PDF p. 85) y «Give the synthesis agent a scoped `verify_fact` tool for simple lookups» (Q9)
- [baja] Omisión: la fila «Code reviewer» (Read, Grep, Glob; excluye Write, Edit, Bash, revisión de solo lectura) de la tabla de conjuntos por rol y la nota de que el coordinator «Agent» se llamaba antes «Task» no aparecen en el apunte; evidencia: «Code reviewer Read, Grep, Glob Write, Edit, Bash (read-only review)» (Guía PDF p. 84) y «Agent (formerly Task, used to spawn subagents)» (web 2.3)

## 2.4 — Integrate MCP servers into Claude Code and agent workflows
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] Sección sobre la config de usuario/proyecto de las slides (Contradicción entre fuentes) → omite que las slides indican que la config de usuario funciona junto a la de proyecto y que el proyecto tiene precedencia; evidencia: «Works alongside project config — project takes precedence» (Slides PDF p. 415)

## 2.5 — Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively
Hallazgos: 3 (alta 0, media 0, baja 3)
- [baja] «No usar Edit cuando `old_string` no puede ser único; la guía lo lista como error común y propone Read → Write (Guía PDF p. 98; Guía PDF p. 95)» → cita de página incorrecta: el error común aparece en el marcador p.97, no en p.98 (p.98 trata de comandos Bash destructivos); evidencia: «Using Edit on repetitive files where the old_string cannot be unique, use Read → Write instead» (Guía PDF p. 97)
- [baja] «Usar Glob para encontrar callers de una función: Glob solo compara rutas y no busca dentro de los archivos; hay que usar Grep (web 2.5; Guía PDF p. 98)» → la p.98 de la guía no respalda esta afirmación; sí la respalda la tabla de la p.95; evidencia: «Glob ... Does NOT: Search file contents (use Grep)» (Guía PDF p. 95)
- [baja] «Cargar todas las herramientas al inicio y no usar ToolSearch; ... (Guía PDF p. 98)» y «No cargar todas las herramientas disponibles al inicio de la sesión en lugar de usar ToolSearch (Guía PDF p. 98)» → cita de página incorrecta: el error de ToolSearch está en p.97 (solo lo de Bash destructivo está en p.98); evidencia: «Loading all available tools at session start instead of using ToolSearch for on-demand loading» (Guía PDF p. 97)

## 3.1 — Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization
Hallazgos: 3 (alta 0, media 0, baja 3)
- [baja] «@imports se cargan junto con el archivo que los referencia (Guía PDF p. 124; web 3.1)» → la Guía PDF p. 124 no dice esto (solo trata rules con paths); el respaldo está en la web y en el apéndice de la guía; evidencia: «When containing file loads» (Guía PDF p. 161) y «imported files load alongside the CLAUDE.md that references them» (web 3.1)
- [baja] «Prevalecen la guía y el banco: responder `/memory`» → el banco (Q41, Q42, Q54) no indica `/memory` como respuesta correcta; solo Q42 lo menciona, como opción incorrecta; el respaldo es la guía y la web; evidencia: «the answer is /memory» (Guía PDF p. 123) y «Give /memory as the right answer» (web 3.1)
- [baja] Omisión: contenido típico del CLAUDE.md raíz (lenguaje/framework, patrones intencionales que parecen anti-patrones, comandos de test, módulos a evitar) y la guía de que debe contener solo información que cambia las decisiones de Claude; evidencia: «not information Claude can easily infer from reading the code» (Guía PDF p. 121)

## 3.2 — Create and configure custom slash commands and skills
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «la respuesta es `/review` en `.claude/commands/` y `/brainstorm` como `SKILL.md` en `~/.claude/skills/` con `context: fork` (Opción A)» → la fuente presenta las opciones del escenario pero no indica explícitamente cuál es la correcta; es una deducción coherente con el resto de la lección; evidencia: «Option A /review in .claude/commands/ for team sharing; /brainstorm as a SKILL.md in ~/.claude/skills/ with context: fork frontmatter» (web 3.2, Practice Scenario)
- [baja] sección «Skills vs CLAUDE.md» omite que Claude también carga automáticamente skills con campo `paths` al trabajar en archivos coincidentes, y la tabla «Where to Place Custom Commands: Quick Reference» → omisión de detalle menor; evidencia: «or skills with a paths field when you work on matching files» (web 3.2)

## 3.3 — Apply path-specific rules for conditional convention loading
Hallazgos: 0 (alta 0, media 0, baja 0)

## 3.4 — Determine when to use plan mode vs direct execution
Hallazgos: 3 (alta 0, media 0, baja 3)
- [baja] «Escenario de práctica: direct execution para las tres tareas (opción A) o plan mode para las tres (opción B) fallan; la web plantea la opción C … frente a la D» → la fuente no incluye clave de respuesta del escenario; que A y B "fallan" y que C es la correcta es una inferencia, no un dato del texto; evidencia: «Option C Plan mode for (1) and (3), direct execution for (2)» (web 3.4)
- [baja] Omisión: el peso del Dominio 3 (20% del examen) y que la guía lo señala como parte significativa del examen no aparece en el fragmento → detalle menor omitido; evidencia: «Dominio 3 (peso 20%)» (web 3.4) y «a significant portion of the Domain 3 exam» (Guía PDF p. 136)
- [baja] Omisión: el ejemplo hilo conductor de la web (sala de bodas con cuatro trabajos: bug de fecha, tasa de depósito, proveedor de pagos, cambio de librería de logging en 30 archivos) solo se usa de forma parcial → detalle menor omitido; evidencia: «a wedding venue whose booking system has four jobs» (web 3.4)

## 3.5 — Apply iterative refinement techniques for progressive improvement
Hallazgos: 2 (alta 0, media 1, baja 1)
- [media] «Refactorizar archivos interconectados en paralelo o solo con verificación manual: la práctica indicada es procesar archivos en secuencia con tests (Guía PDF p. 164-165)» → cita con página incorrecta (usa el folio impreso, no el marcador [[PDF p.N]]); el contenido está en los marcadores 165-166; evidencia: «Process files in sequence with tests» (Guía PDF p. 165-166)
- [baja] «Sequential — problemas independientes, aunque estén en el mismo módulo (Q49; Q51)» → "en el mismo módulo" no figura en la fuente; Q49 habla de partes distintas de una misma función y Q51 de nombres dispersos en varios archivos; evidencia: «Each issue is in a completely different part of the function and none of them interact» (Q49)

## 3.6 — Integrate Claude Code into CI/CD pipelines
Hallazgos: 4 (alta 0, media 1, baja 3)
- [media] «Usar flags inexistentes como `--format json`, `--strict`, `--json` o `--structured-output` (Guía PDF p. 167-169)» → la guía solo declara inexistente a `--structured-output`; de `--format json`/`--strict` dice que solo fuerzan formato JSON sin imponer estructura, y de `-p --json` que no impone un esquema; evidencia: «it refers to a non-existent flag in the Claude Code CLI» (Guía PDF p. 169); «does not guarantee the output structure» (Guía PDF p. 168)
- [baja] «`--output-format json` — da salida parseable, pero no sustituye a `-p` (Q50; web 3.6)» → la fuente no afirma que json no sustituya a `-p`; Q50 solo dice que mejora la parseabilidad sin evitar sugerencias duplicadas; evidencia: «Option B improves parseability but does not prevent duplicate suggestions» (Q50)
- [baja] Sección «Flags de CLI en CI y la GitHub Action» → omite flags de la tabla web (`--input-format`, `--add-dir`, `--model`, `-c/--continue`, `-r/--resume`, `stream-json`); evidencia: «--input-format text|stream-json … --add-dir <path> … --model <alias|name>» (web 3.6)
- [baja] «con `prompt` se ejecuta en modo automation (web 3.6)» → omite el modo interactivo sin `prompt` (trigger `@claude`), la necesidad de `actions/checkout` y el bloque `permissions` de la Action; evidencia: «With no prompt, the action runs in interactive mode. It waits for the trigger phrase (@claude by default)» (web 3.6)

## 4.1 — Design prompts with explicit criteria to improve precision and reduce false positives
Hallazgos: 3 (alta 0, media 0, baja 3)
- [baja] «Añadir calificativos como "carefully" o "thoroughly": suenan tranquilizadores pero no cambian la prueba que aplica el modelo (Guía PDF p. 176)» → página incorrecta: el pasaje está en la p. 177, no en la 176; evidencia: «Words like "carefully" or "thoroughly" sound reassuring but change nothing» (Guía PDF p. 177)
- [baja] «--system-prompt — reemplaza el prompt por defecto y quita la guía de herramientas integrada (Guía PDF p. 148)» → «reemplaza el prompt por defecto» no figura en el texto fuente de esa página (solo se dice que quita la guía de herramientas; la fila de --system-prompt no está en la p. 148); evidencia: «this strips Claude's built-in tool guidance» (Guía PDF p. 148)
- [baja] Sección omitida: el ejercicio práctico de la web (Build Exercise) y sus umbrales de referencia (prompt vago 30-50% de inconsistencia frente a <15% con criterios explícitos) no aparecen en el apunte; evidencia: «The vague prompt should produce 30-50% inconsistency while the explicit criteria version should be below 15%» (web 4.1)

## 4.2 — Apply few-shot prompting to improve output consistency and quality
Hallazgos: 2 (alta 0, media 1, baja 1)
- [media] «la guía PDF presenta 3 a 5 como el punto óptimo […]; entre guía y banco la cifra difiere (3-5 frente a 2-4)» → la guía PDF también recoge 2 a 4 ejemplos en sus principios de diseño (p. 183), así que la guía es internamente ambigua y no solo contradice con 3-5; el apunte omite ese 2-4 de la guía; evidencia: «Two to four examples that resolve genuinely tricky cases are worth more than many examples of the obvious case» (Guía PDF p. 183) frente a «3 to 5 examples: Anthropic's documented sweet spot» (Guía PDF p. 183)
- [baja] Apunte sin la sección «Build Exercise» (ejercicio de 45 min con 10 documentos: línea base sin ejemplos, 3 ejemplos con razonamiento, comparar tasa de campos vacíos, matriz de decisión) → sección del texto fuente omitida; evidencia: «Create a base extraction prompt with detailed instructions but no examples and test it against 10 documents with varied structures» (web 4.2)

## 4.3 — Enforce structured output using tool use and JSON schemas
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «Error de sintaxis que el schema detecta: falta una llave de cierre o un tipo incorrecto… (Guía PDF p. 88-89; con `strict`, Guía PDF p. 88)» → cita de página incorrecta para la «llave de cierre»: no está en p. 88-89 (la p. 89 trata de MCP); aparece en la p. 189; evidencia: «Syntax error Missing closing brace, wrong data type Yes» (Guía PDF p. 189)
- [baja] Omisión: no se recoge la jerarquía de fiabilidad de dos niveles (primero tool_use con JSON schemas, luego JSON por prompt) que la web 4.3 presenta como base del examen; evidencia: «there is a two-tier reliability hierarchy: first tool_use with JSON schemas, then prompt-based JSON» (web 4.3)

## 4.4 — Implement validation, retry, and feedback loops for extraction quality
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «La guía los organiza en tres capas: schema validation (...), semantic validation (...) y business rule validation (...) (Guía PDF p. 200). Ninguna capa atrapa todo y las tres hacen falta en producción (Guía PDF p. 200).» → cita con página incorrecta: la tabla de capas y la frase sobre las tres capas están en el marcador p. 201, no en el 200; evidencia: «No single layer catches everything. (...) All three are needed in a production extraction pipeline.» (PDF p. 201)
- [baja] «No esperar que el schema atrape sumas o ubicación de campos; son checks semánticos (Guía PDF p. 207).» → cita con página incorrecta: la lista de Common Mistakes está en el marcador p. 208, no en el 207; evidencia: «Expecting the schema to catch sums or field placement. Those are semantic checks.» (PDF p. 208)

## 4.5 — Design efficient batch processing strategies
Hallazgos: 0 (alta 0, media 0, baja 0)

## 4.6 — Design multi-instance and multi-pass review architectures
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] Sección omitida: la analogía de «Context Retention Bias» con la revisión externa humana y que el hecho de que Claude haya considerado y descartado los casos es lo que hace severa la limitación → el apunte menciona los distractores pero no explica este matiz; evidencia: «A fresh perspective catches things the original author's mental model filters out» (Guía PDF p. 159)
- [baja] Sección omitida: el ejercicio práctico («Build Exercise») de pasos para construir el sistema de revisión multi-pasada y calibrar con una instancia independiente solo se cita de forma parcial (solo el ejercicio de pasada única) → falta el resto de pasos (añadir scoring 0.0-1.0, ruteo direct_report/human_review, calibración con instancia fresca); evidencia: «routing decision (direct_report or human_review)» (web 4.6)

## 5.1 — Manage conversation context to preserve critical information across long interactions
Hallazgos: 3 (alta 0, media 1, baja 2)
- [media] «el passing history (charla y pasos resueltos) se puede recortar o limpiar sin riesgo siempre que los durable facts estén fijados fuera del resumen (Guía PDF p. 236)» → la condición «siempre que…» no figura en la guía; la fuente solo dice que se puede recortar con seguridad; evidencia: «Can be trimmed or cleared safely» (PDF p. 236)
- [baja] Umbrales de uso de la ventana → se omiten los tramos de 20-30% (rendimiento estable) y 95%+ (fallo inminente, compaction urgente) y la columna «cuándo gestionar» de la tabla de crecimiento; evidencia: «At 95%+ utilization: The system is about to fail.» (PDF p. 231; tabla en PDF p. 233)
- [baja] Sección «Token Budget Analogy» omitida (system prompt = alquiler fijo, tool definitions = servicios, memory tool = cuenta de ahorros; tres opciones: context editing, compaction, memory tool); evidencia: «think of the context window as a financial budget» (PDF p. 234)

## 5.2 — Design effective escalation and ambiguity resolution patterns
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «Reembolso por encima del umbral de auto-aprobación: Level 1, agente de soporte frontline (Guía PDF p. 239)» → página incorrecta: la fila de Level 1 está en el marcador p.240 (en p.239 solo aparece Level 0); evidencia: «Level 1 Agent needs human approval Frontline support agent Refund above auto-approval threshold» (Guía PDF p. 240)
- [baja] «Elegir el score de confianza autorreportada (1-10, umbral 7) … (opción B de Q3)» → el umbral de 7 no figura en Q3 (su opción B solo dice «a threshold»); proviene del escenario de práctica de la web, y la confianza alta en ambos tipos de caso tampoco está en Q3; evidencia: «Have the agent self-report a confidence score (1-10) before each response and automatically route requests to humans when confidence falls below a threshold» (Q3)

## 5.3 — Implement error propagation strategies across multi-agent systems
Hallazgos: 1 (alta 0, media 0, baja 1)
- [baja] «Marcar como éxito un resultado que en realidad es un fallo de acceso (Guía PDF p. 245)» → cita con página incorrecta: la idea aparece en "Common Mistakes" en la p. 244 (y en silent suppression, p. 243), no en la p. 245, que solo contiene la viñeta sobre retryability; evidencia: «Returning an empty result when the tool actually failed to reach its source.» (Guía PDF p. 244)

## 5.4 — Manage context effectively in large codebase exploration
Hallazgos: 2 (alta 0, media 0, baja 2)
- [baja] «bloque JSON del manifest con "nextSteps": ["Investigate PaymentGateway error handling"]» → el ejemplo omite sin avisar dos de los tres nextSteps de la fuente; evidencia: «"Review RefundProcessor test files", "Check cache invalidation logic in OrderRepository"» (web 5.4)
- [baja] «bloque markdown del scratchpad (Key Classes y Dependency Chain)» → se omite la sección "Critical Findings" del ejemplo de la fuente (sin retry en Stripe, falta de invalidación de caché, cobertura 87%/12%); evidencia: «## Critical Findings - RefundProcessor has no retry logic for Stripe API failures» (web 5.4)

## 5.5 — Design human review workflows and confidence calibration
Hallazgos: 3 (alta 0, media 0, baja 3)
- [baja] «Un sistema con 96% global tenía 99% en standard invoices, 79% en scanned paper invoices y 68% en handwritten receipts (Guía PDF p. 248)» → página incorrecta: el ejemplo está en la p. 249, no en la 248; evidencia: «An extraction system reports 96% overall accuracy… Standard invoices: 99% – Scanned paper invoices: 79% – Handwritten receipts: 68%» (PDF p. 249)
- [baja] «Aggregate accuracy — una sola cifra dominada por el tipo de mayor volumen (Guía PDF p. 248)» → la definición está en la p. 248, pero la idea de que el agregado está dominado por el tipo de alto volumen aparece en la p. 249; evidencia: «The 96% aggregate is dominated by the high-volume standard invoices.» (PDF p. 249)
- [baja] «Las cifras de los ejemplos difieren (Guía PDF p. 248: 96%; web 5.5: 97%)» → página incorrecta: el 96% de la guía figura en la p. 249; evidencia: «An extraction system reports 96% overall accuracy.» (PDF p. 249)

## 5.6 — Preserve information provenance and handle uncertainty in multi-source synthesis
Hallazgos: 0 (alta 0, media 0, baja 0)

## Correcciones aplicadas tras la verificación

Los 7 hallazgos de severidad media se revisaron contra el texto fuente y se corrigieron en los apuntes `dominioN-*.md`. Los 54 hallazgos de severidad baja (omisiones o detalles menores) no se corrigieron.

- 1.1 (Q15): se aclara que solo C y D son modos de fallo no reconocidos y que A es una preocupación válida pero no el riesgo principal.
- 1.5: todas las citas de la guía usaban el folio impreso en vez del marcador de página PDF; se desplazaron +1 (56-58 pasan a 57-59).
- 1.7 (dos lugares): se matiza la postura de la web (fresh start solo si la mayoría de los tool results queda obsoleta; si el contexto sigue válido, reanudar e informar de los archivos cambiados).
- 3.5: la cita «Guía PDF p. 164-165» pasa a 165-166.
- 3.6: se corrige la lista de flags: solo `--structured-output` se declara inexistente; `--format json`, `--strict` y `-p --json` no imponen esquema.
- 4.2: se añade que la guía menciona tanto 3-5 como 2-4 ejemplos, además de la cifra del banco.
- 5.1: se elimina la condición «siempre que…», que no figura en la guía.

Nota: se midió la consistencia de las citas de la guía contra las páginas de la fuente de cada tarea: 1.328 de 1.332 coincidían; las 4 restantes eran de 1.5 y 3.5 (en 1.5 todas las citas de la guía estaban desplazadas, no solo esas) y ya se corrigieron. Los hallazgos corregidos permanecen listados arriba como los emitió el verificador. No se volvió a ejecutar el verificador tras las correcciones.
