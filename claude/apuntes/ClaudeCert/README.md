# Claude Certified Architect – Foundations (CCA-F) — Anthropic (guía de examen, 2026)

Autores / fuentes: Anthropic (certificación); apuntes ensamblados a partir de la guía «Tutorials Dojo Study Guide and Cheat Sheets – Claude Certified Architect Foundations (CCA-F)», las slides del curso en video (Tutorials Dojo, junio 2026), el banco de 77 preguntas de práctica y las lecciones web de claudecertificationguide.com (sitio independiente de terceros, no afiliado a Anthropic).

## Descripción general

Apuntes de examen organizados por dominio. Cubren cinco dominios: diseño de sistemas agénticos y orquestación (27%), diseño de herramientas e integración MCP (18%), configuración y flujos de trabajo de Claude Code (20%), ingeniería de prompts y salida estructurada (20%), y gestión de contexto y fiabilidad (15%). Un hilo común en los apuntes es distinguir lo probabilístico (prompt guidance, CLAUDE.md) de lo determinista (programmatic enforcement, hooks, permissions, schemas) y elegir el mecanismo correcto para cada escenario, descartando los distractores típicos del banco de preguntas.

## Dominios

- [Dominio 1 — Agentic Architecture & Orchestration (peso 27%)](dominio1-agentic-architecture-orchestration.md): agentic loop, orquestación multiagente coordinador-subagente, enforcement con hooks y gates, descomposición de tareas y gestión de sesiones.
- [Dominio 2 — Tool Design & MCP Integration (peso 18%)](dominio2-tool-design-mcp-integration.md): descripciones y límites de herramientas, errores MCP estructurados, reparto de herramientas y tool_choice, servidores MCP y herramientas integradas.
- [Dominio 3 — Claude Code Configuration & Workflows (peso 20%)](dominio3-claude-code-configuration-workflows.md): jerarquía de CLAUDE.md, skills y commands, reglas por ruta, plan mode, refinamiento iterativo y CI/CD.
- [Dominio 4 — Prompt Engineering & Structured Output (peso 20%)](dominio4-prompt-engineering-structured-output.md): criterios explícitos, few-shot, salida estructurada con tool use y JSON schemas, validación y reintento, procesamiento por lotes y revisión multi-pasada.
- [Dominio 5 — Context Management & Reliability (peso 15%)](dominio5-context-management-reliability.md): gestión de contexto, escalación, propagación de errores, exploración de código grande, revisión humana y procedencia de la información.

## Tareas por dominio

### Dominio 1
- [Tarea 1.1 — Design and implement agentic loops for autonomous task execution (Diseñar e implementar agentic loops para la ejecución autónoma de tareas)](dominio1-agentic-architecture-orchestration.md)
- [Tarea 1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns (Orquestar sistemas multiagente con patrones coordinador-subagente)](dominio1-agentic-architecture-orchestration.md)
- [Tarea 1.3 — Configure subagent invocation, context passing, and spawning (Configurar la invocación, el paso de contexto y el spawning de subagentes)](dominio1-agentic-architecture-orchestration.md)
- [Tarea 1.4 — Implement multi-step workflows with enforcement and handoff patterns (Implementar flujos de varios pasos con patrones de enforcement y handoff)](dominio1-agentic-architecture-orchestration.md)
- [Tarea 1.5 — Apply Agent SDK hooks for tool call interception and data normalization (Aplicar hooks del Agent SDK para interceptar llamadas a herramientas y normalizar datos)](dominio1-agentic-architecture-orchestration.md)
- [Tarea 1.6 — Design task decomposition strategies for complex workflows (Diseñar estrategias de descomposición de tareas para flujos de trabajo complejos)](dominio1-agentic-architecture-orchestration.md)
- [Tarea 1.7 — Manage session state, resumption, and forking (Gestionar el estado de sesión, la reanudación y el forking)](dominio1-agentic-architecture-orchestration.md)

### Dominio 2
- [Tarea 2.1 — Design effective tool interfaces with clear descriptions and boundaries (Diseñar interfaces de herramientas efectivas con descripciones y límites claros)](dominio2-tool-design-mcp-integration.md)
- [Tarea 2.2 — Implement structured error responses for MCP tools (Implementar respuestas de error estructuradas para herramientas MCP)](dominio2-tool-design-mcp-integration.md)
- [Tarea 2.3 — Distribute tools appropriately across agents and configure tool_choice (Distribuir herramientas adecuadamente entre agentes y configurar tool_choice)](dominio2-tool-design-mcp-integration.md)
- [Tarea 2.4 — Integrate MCP servers into Claude Code and agent workflows (Integrar servidores MCP en Claude Code y en flujos de agentes)](dominio2-tool-design-mcp-integration.md)
- [Tarea 2.5 — Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively (Seleccionar y aplicar eficazmente las herramientas integradas)](dominio2-tool-design-mcp-integration.md)

### Dominio 3
- [Tarea 3.1 — Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization (Configurar archivos CLAUDE.md con jerarquía, alcance y organización modular adecuados)](dominio3-claude-code-configuration-workflows.md)
- [Tarea 3.2 — Create and configure custom slash commands and skills (Crear y configurar slash commands personalizados y skills)](dominio3-claude-code-configuration-workflows.md)
- [Tarea 3.3 — Apply path-specific rules for conditional convention loading (Aplicar reglas específicas por ruta para la carga condicional de convenciones)](dominio3-claude-code-configuration-workflows.md)
- [Tarea 3.4 — Determine when to use plan mode vs direct execution (Determinar cuándo usar plan mode frente a direct execution)](dominio3-claude-code-configuration-workflows.md)
- [Tarea 3.5 — Apply iterative refinement techniques for progressive improvement (Aplicar técnicas de refinamiento iterativo para una mejora progresiva)](dominio3-claude-code-configuration-workflows.md)
- [Tarea 3.6 — Integrate Claude Code into CI/CD pipelines (Integrar Claude Code en pipelines de CI/CD)](dominio3-claude-code-configuration-workflows.md)

### Dominio 4
- [Tarea 4.1 — Design prompts with explicit criteria to improve precision and reduce false positives (Diseñar prompts con criterios explícitos para mejorar la precisión y reducir falsos positivos)](dominio4-prompt-engineering-structured-output.md)
- [Tarea 4.2 — Apply few-shot prompting to improve output consistency and quality (Aplicar few-shot prompting para mejorar la consistencia y la calidad de la salida)](dominio4-prompt-engineering-structured-output.md)
- [Tarea 4.3 — Enforce structured output using tool use and JSON schemas (Forzar salida estructurada con tool use y JSON schemas)](dominio4-prompt-engineering-structured-output.md)
- [Tarea 4.4 — Implement validation, retry, and feedback loops for extraction quality (Implementar bucles de validación, reintento y retroalimentación para la calidad de la extracción)](dominio4-prompt-engineering-structured-output.md)
- [Tarea 4.5 — Design efficient batch processing strategies (Diseñar estrategias eficientes de procesamiento por lotes)](dominio4-prompt-engineering-structured-output.md)
- [Tarea 4.6 — Design multi-instance and multi-pass review architectures (Diseñar arquitecturas de revisión multi-instancia y multi-pasada)](dominio4-prompt-engineering-structured-output.md)

### Dominio 5
- [Tarea 5.1 — Manage conversation context to preserve critical information across long interactions (Gestionar el contexto de la conversación para preservar la información crítica en interacciones largas)](dominio5-context-management-reliability.md)
- [Tarea 5.2 — Design effective escalation and ambiguity resolution patterns (Diseñar patrones eficaces de escalación y resolución de ambigüedad)](dominio5-context-management-reliability.md)
- [Tarea 5.3 — Implement error propagation strategies across multi-agent systems (Implementar estrategias de propagación de errores en sistemas multiagente)](dominio5-context-management-reliability.md)
- [Tarea 5.4 — Manage context effectively in large codebase exploration (Gestionar el contexto de forma eficaz en la exploración de bases de código grandes)](dominio5-context-management-reliability.md)
- [Tarea 5.5 — Design human review workflows and confidence calibration (Diseñar flujos de revisión humana y calibración de confianza)](dominio5-context-management-reliability.md)
- [Tarea 5.6 — Preserve information provenance and handle uncertainty in multi-source synthesis (Preservar la procedencia de la información y manejar la incertidumbre en la síntesis multifuente)](dominio5-context-management-reliability.md)

## Otros archivos

- [Verificación de fidelidad](_verificacion.md)
- [Material de estudio](_estudio/)
- [Glosario](_glosario.md)

## Nota de extracción: discrepancia CCA-F / CCAR-F

Discrepancia entre fuentes sin resolver: el banco y la guía llaman al examen «CCA-F» y el banco indica 77 preguntas de práctica y una nota mínima de 720 (escala 100-1.000); la web lo llama «CCAR-F» e indica 60 preguntas en 120 minutos, aprobado con 720/1.000 y credencial válida 12 meses. No se decide cuál es la correcta.
