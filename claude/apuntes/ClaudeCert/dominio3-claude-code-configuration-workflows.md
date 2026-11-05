# Claude Certified Architect – Foundations (CCA-F) — Anthropic (guía de examen, 2026)

## Dominio 3 — Claude Code Configuration & Workflows (Configuración y flujos de trabajo de Claude Code)

> Nota de extracción: este apunte combina cinco fuentes: la guía en PDF «Tutorials Dojo Study Guide and Cheat Sheets – Claude Certified Architect Foundations (CCA-F)», las slides en PDF del curso en video (Tutorials Dojo, junio 2026), el banco de 77 preguntas de práctica «Claude Certified Architect. Foundations: Practice Exam» y las lecciones web de claudecertificationguide.com (sitio independiente de terceros, no afiliado a Anthropic). Citas: `(Guía PDF p. N)` y `(Slides PDF p. N)` usan la página del PDF; `(web N.M)` remite a la lección N.M de la web; `(QN)` remite a la pregunta N del banco. Si las fuentes se contradicen, prevalecen la guía y el banco sobre la web. Las slides tienen muchas páginas que son solo imagen y no se pudieron leer, por lo que su cobertura es parcial. Discrepancia entre fuentes sin resolver: el banco y la guía llaman al examen «CCA-F» y el banco indica 77 preguntas de práctica y una nota mínima de 720 (escala 100-1.000); la web lo llama «CCAR-F» e indica 60 preguntas en 120 minutos, aprobado con 720/1.000 y credencial válida 12 meses. No se decide cuál es la correcta.

## Lo que necesitas saber

El Dominio 3 trata de cómo configurar y operar Claude Code: dónde se colocan las instrucciones persistentes (CLAUDE.md, `.claude/rules/`, skills y slash commands), cómo se decide el modo de trabajo (plan mode o direct execution), cómo se refina un resultado en varias rondas y cómo se ejecuta Claude Code sin intervención humana en pipelines de CI/CD. Pesa el 20% del examen. La guía marca como el concepto más probado de todo el dominio la diferencia entre CLAUDE.md (advisory) y los mecanismos deterministas como hooks y permissions (Guía PDF p. 123; Guía PDF p. 131).

Las tareas se conectan por una misma pregunta: qué mecanismo es el adecuado y cuándo se carga. CLAUDE.md se carga en cada sesión, las rules con frontmatter `paths` solo al tocar archivos coincidentes y las skills bajo demanda cuando se invocan (Guía PDF p. 128; web 3.3). La jerarquía user, project y directory (tarea 3.1), la ubicación de commands y skills según el alcance (3.2) y las reglas por ruta con glob patterns (3.3) responden a esa misma lógica de alcance y carga. Los hooks y `permissions.deny` son el camino cuando algo debe cumplirse siempre (Guía PDF p. 132; Guía PDF p. 133).

Las tareas 3.4 a 3.6 pasan del almacenamiento de instrucciones a la forma de trabajar. La elección entre plan mode y direct execution depende de la ambigüedad, no de la dificultad (web 3.4). El refinamiento iterativo se apoya en señales claras: ejemplos de entrada/salida, test-driven iteration, interview pattern y feedback en batch o secuencial (web 3.5; Guía PDF p. 139). En CI/CD, `-p` evita que el job se cuelgue, `--output-format json` con `--json-schema` da salida parseable, y la revisión independiente, el contexto incremental y CLAUDE.md mejoran la calidad (web 3.6; Q10; Q53; Q50).

Sales sabiendo elegir el mecanismo correcto ante un escenario: dónde va cada instrucción, cuándo planificar, qué técnica de refinamiento aplicar y qué flags usar en CI. También sales avisado de las discrepancias entre fuentes que los fragmentos anotan (por ejemplo, feedback que interactúa: la guía recomienda arreglos incrementales y la web y el banco un solo mensaje) (Guía PDF p. 141; web 3.5; Q51). Las tareas que figuran como prioridad de estudio son la 3.1 (Settings/hooks vs CLAUDE.md y @ references vs CLAUDE.md vs inline) y la 3.5 (refinamiento iterativo).

## Tarea 3.1 — Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization (Configurar archivos CLAUDE.md con jerarquía, alcance y organización modular adecuados)

> Prioridad de estudio: Settings/hooks vs CLAUDE.md (0% en los intentos 1 y 2); @ references vs CLAUDE.md vs inline (0% en los intentos 1 y 2)

### Jerarquía de tres niveles (user, project, directory)

**Concepto:** CLAUDE.md es un archivo Markdown de instrucciones persistentes para Claude Code que se lee en tres niveles: user, project y directory (web 3.1). La guía lo describe como un README escrito para Claude que se lee al inicio de cada sesión (Guía PDF p. 120).

**Ejemplos de uso (3, cortos):**
1. User-level `~/.claude/CLAUDE.md`: preferencias personales como verbosidad, estilo de salida o atajos propios; solo aplica a ti y no se versiona (web 3.1; Guía PDF p. 121).
2. Project-level `.claude/CLAUDE.md` o `CLAUDE.md` en la raíz: estándares de equipo (naming, manejo de errores, testing, decisiones de arquitectura, checklists de revisión); ambas ubicaciones son válidas y se versionan (web 3.1; Q41).
3. Directory-level (`CLAUDE.md` en un subdirectorio): convenciones de un paquete, p. ej. `/packages/api/CLAUDE.md` con convenciones REST, o `/terraform/` y `/kubernetes/` con guía propia; complementa, no reemplaza, al archivo raíz (web 3.1; Guía PDF p. 121).

**Qué NO hacer:**
- No guardar en `~/.claude/CLAUDE.md` estándares de código, naming compartido, workflows del repositorio ni reglas de arquitectura; si el equipo lo necesita, va en el CLAUDE.md de proyecto (Slides PDF p. 657).
- No poner preferencias personales en el CLAUDE.md raíz del proyecto; van en `~/.claude/CLAUDE.md` (Guía PDF p. 123).
- No hacer el CLAUDE.md raíz demasiado largo (300+ líneas) con información que Claude puede inferir leyendo el código (Guía PDF p. 123). La guía añade que si hay más de 15 reglas probablemente no se han identificado las realmente esenciales (Guía PDF p. 121).

**Posible confusión con otros conceptos:**
- User-level vs project-level — una convención en `~/.claude/CLAUDE.md` de un desarrollador no llega a quien clona el repo; por eso se mueve al nivel de proyecto y se hace commit (Slides PDF p. 658).
- Directory-level vs `.claude/rules/` — un CLAUDE.md de directorio aplica a un solo directorio; para convenciones repartidas por muchos directorios (p. ej. archivos de test dispersos) se usan reglas por ruta con glob patterns (web 3.1). Un CLAUDE.md de directorio funciona bien si todos los tests viven bajo un único `tests/` (Slides PDF p. 1057).

Regla simple de alcance: si la instrucción te afecta solo a ti, user-level; si afecta al proyecto o al equipo, project-level (Slides PDF p. 659). Si aplica solo a una parte del código, considerar un CLAUDE.md de subdirectorio o reglas con alcance por ruta (Guía PDF p. 122).

### Orden de carga y conflictos (CLAUDE.md es advisory)

**Concepto:** los archivos aplicables se concatenan en el contexto, sin sobrescribirse entre sí; se cargan del alcance más amplio al más específico, y el más cercano al directorio de trabajo se lee al final (web 3.1). Que un archivo se lea último no lo hace ganar un conflicto: Claude "may pick one arbitrarily" y no hay garantía de cumplimiento estricto (web 3.1).

**Ejemplos de uso (3, cortos):**
1. Al iniciar en el paquete de la API, Claude lee el archivo de usuario, luego el de proyecto y luego el del paquete (web 3.1).
2. El CLAUDE.md de subdirectorio se carga además del raíz cuando Claude trabaja en ese directorio (Guía PDF p. 121).
3. Añadir "IMPORTANT" o "YOU MUST" mejora la adherencia, pero el cumplimiento sigue siendo probabilístico (Guía PDF p. 123).

**Qué NO hacer:**
- No tratar CLAUDE.md como una capa de configuración con overrides deterministas (web 3.1; Guía PDF p. 123).
- No dejar instrucciones contradictorias entre el archivo raíz y los de subdirectorio: crean comportamiento inconsistente (Guía PDF p. 121; Guía PDF p. 123).
- No asumir que "el alcance más específico gana" ni que "user-level anula project-level": los docs oficiales no dicen ninguna de las dos cosas (web 3.1).

**Posible confusión con otros conceptos:**
- CLAUDE.md vs settings.json — settings.json tiene una cadena de precedencia estricta (managed policy > local > project > user, con managed siempre ganando); CLAUDE.md no la tiene (web 3.1). Ante "¿qué CLAUDE.md gana?", la respuesta es que ninguno está garantizado: mover la regla a settings.json o a un hook (web 3.1).

### CLAUDE.md vs settings.json / hooks / permissions (enforcement)

**Concepto:** CLAUDE.md es advisory (orientación); lo que debe cumplirse siempre requiere un mecanismo determinista como hooks o permissions (Guía PDF p. 123). La web lo resume: las reglas de settings las aplica el cliente "regardless of what Claude decides"; CLAUDE.md da forma al comportamiento pero no es una capa de enforcement duro (web 3.1). La guía lo marca como el concepto más probado de todo el Dominio 3 (Guía PDF p. 123; Guía PDF p. 131).

**Ejemplos de uso (3, cortos):**
1. "Claude must never modify files in db/migrations/" → `permissions.deny` con `["Edit(./db/migrations/**)"]` (hard block) (Guía PDF p. 132; Guía PDF p. 133).
2. "Claude should prefer a custom logging module over console.log" → CLAUDE.md (preferencia advisory) (Guía PDF p. 133).
3. "All TypeScript files must be auto-formatted with Prettier after every edit" → hook PostToolUse con matcher `Edit|Write` (Guía PDF p. 130; Guía PDF p. 133).

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```
(Guía PDF p. 130)

**Qué NO hacer:**
- No confiar en el énfasis ("IMPORTANT", "YOU MUST") para garantizar cumplimiento: mejora la probabilidad pero no elimina violaciones (Guía PDF p. 131). En el ejemplo de la guía, un ~15% de archivos seguía con formato inconsistente pese al énfasis; el hook dio 100% de cumplimiento (Guía PDF p. 131).
- No usar un hook PreToolUse para post-procesado como el formato: eso es trabajo de PostToolUse (Guía PDF p. 131).
- No depender del alcance de CLAUDE.md para bloqueos de herramientas, formatters obligatorios o políticas de permisos: van en settings.json o en un hook (web 3.1).

**Posible confusión con otros conceptos:**
- permissions.deny — "never" indica bloqueo absoluto; no requiere script, es configuración declarativa (Guía PDF p. 132; Guía PDF p. 133).
- Hook PreToolUse — corre antes de la herramienta y con exit code 2 la bloquea, incluso con `--dangerously-skip-permissions` (Guía PDF p. 129).
- Hook PostToolUse — corre tras la ejecución exitosa; "automatically"/"always" con una tarea de automatización apunta a hooks (Guía PDF p. 129; Guía PDF p. 133).
- CLAUDE.md — "prefer"/"should" apuntan a CLAUDE.md (Guía PDF p. 133).
- Los hooks viven en `.claude/settings.json` (commit, compartido) o `.claude/settings.local.json` (gitignored, personal) (Guía PDF p. 129).

### @ path imports (organización modular)

**Concepto:** la directiva es simplemente `@` seguido de una ruta; no existe una palabra clave `@import`, aunque muchas páginas la escriben así (web 3.1). El archivo nombrado se inserta (inlined) en el CLAUDE.md al cargarse, como si se pegara su texto (web 3.1). La guía lo llama "@imports": permite referenciar Markdown externo y evitar duplicar contenido (Guía PDF p. 122).

**Ejemplos de uso (3, cortos):**
1. Un `.claude/CLAUDE.md` que importa `@./standards/naming-conventions.md`, `@./standards/error-handling.md` y `@./standards/testing-requirements.md` (web 3.1).
2. En un monorepo, `/packages/auth/CLAUDE.md` importa `@docs/standards/security-rules.md` y `@docs/standards/testing-patterns.md`, mientras `/packages/notifications/CLAUDE.md` importa solo `@docs/standards/testing-patterns.md` (Guía PDF p. 122).
3. Cuando cambian las reglas de seguridad se actualiza un solo archivo y todos los paquetes que lo importan lo reciben (Guía PDF p. 122).

```markdown
# .claude/CLAUDE.md

Coding standards:

@./standards/naming-conventions.md
@./standards/error-handling.md
@./standards/testing-requirements.md
```
(web 3.1)

**Qué NO hacer:**
- No esperar que partir un CLAUDE.md de 600 líneas en seis imports de 100 reduzca el contexto: mejora el mantenimiento del código fuente, pero el contexto tiene el mismo tamaño (web 3.1).
- No escribir `@import` como si fuera una keyword (web 3.1).
- No usar imports para "reducir contexto por sesión"; para eso sirve `.claude/rules/` con frontmatter `paths` (web 3.1).

**Posible confusión con otros conceptos:**
- @imports vs `.claude/rules/` con paths — en un monorepo donde cada maintainer conoce las necesidades de su dominio, @imports en el CLAUDE.md de cada paquete es la respuesta típica; las rules por ruta no requieren ese conocimiento, pero exigen listar cada directorio en el frontmatter YAML (Guía PDF p. 122).

### CLAUDE.local.md

**Concepto:** archivo junto a CLAUDE.md en cualquier nivel de la jerarquía, que se carga igual; se añade después de CLAUDE.md del mismo nivel (web 3.1). Es la versión con alcance de proyecto de `~/.claude/CLAUDE.md` (web 3.1).

**Ejemplos de uso (3, cortos):**
1. Una ruta favorita de scratchpad para este repo (web 3.1).
2. Una explicación detallada que se pega una y otra vez (web 3.1).
3. Una nota temporal de depuración que se borrará la semana siguiente (web 3.1).

**Qué NO hacer:**
- No poner reglas del equipo (p. ej. requisitos de testing) aquí; van en CLAUDE.md (web 3.1).
- No suponer que, por leerse último, gana un conflicto: es orden de carga, no precedencia (web 3.1).
- No commitearlo: por convención el sufijo `.local` indica archivo no versionado, y la mayoría de equipos lo añade a `.gitignore` (web 3.1).

### El directorio .claude/rules/

**Concepto:** en lugar de un solo CLAUDE.md, `.claude/rules/` puede contener archivos de reglas por tema (web 3.1). Con frontmatter YAML `paths`, cada regla carga solo al trabajar con archivos que coinciden, ahorrando tokens (Guía PDF p. 124). Las rules son advisory igual que CLAUDE.md y se versionan con el proyecto (Guía PDF p. 124).

**Ejemplos de uso (3, cortos):**
1. `testing.md`: nombres de tests, patrones de assertion, uso de fixtures (web 3.1).
2. `api-conventions.md`: nombres de endpoints y esquemas request/response; `deployment.md`: checklist y entornos (web 3.1).
3. `terraform.md` con `paths: ["terraform/**/*"]` carga solo al editar archivos bajo `terraform/` (Guía PDF p. 124).

```markdown
---
paths:
  - "terraform/**/*"
---

Use Terraform 1.5+ syntax. Always include a description for each variable.
```
(Guía PDF p. 124)

**Qué NO hacer:**
- No suponer que carga solo bajo demanda sin frontmatter: sin frontmatter, los rules files cargan en todas las sesiones (web 3.1).
- No usar un CLAUDE.md de directorio para convenciones que cruzan directorios; usar rules con glob patterns (web 3.1).

**Posible confusión con otros conceptos:**
- `.claude/rules/` vs @imports — rules con paths cargan según el archivo con que trabaja Claude; @imports se cargan junto con el archivo que los referencia (Guía PDF p. 124; web 3.1). El detalle de path-scoping es la Task Statement 3.3 (web 3.1).

### Qué sobrevive a la compactación

**Concepto:** tras `/compact`, el CLAUDE.md de la raíz del proyecto se vuelve a leer del disco y se inyecta de nuevo completo, porque las instrucciones nunca formaron parte del historial de conversación (web 3.1).

**Ejemplos de uso (3, cortos):**
1. El CLAUDE.md raíz se recarga completo tras `/compact` (web 3.1).
2. Los CLAUDE.md anidados en subdirectorios y las rules con frontmatter `paths:` no se recargan automáticamente; cargan bajo demanda al leer Claude un archivo coincidente (web 3.1).
3. Una instrucción que solo existió en el chat (p. ej. una regla de naming escrita en la conversación) puede resumirse o perderse, pues no hay archivo que releer (web 3.1).

**Qué NO hacer:**
- No dejar reglas importantes solo en la conversación; ponerlas en un archivo (web 3.1).

### Diagnóstico: /memory y /context

**Concepto:** `/memory` y `/context` muestran qué archivos ya están cargados; no cargan nada. La configuración se carga automáticamente según su nivel y ubicación (web 3.1). La guía presenta `/memory` como el comando que muestra qué archivos de memoria (incluido CLAUDE.md) están cargados y como el primer paso de diagnóstico más eficiente (Guía PDF p. 123).

**Ejemplos de uso (3, cortos):**
1. Comportamiento distinto entre sesiones o desarrolladores en una misma práctica: comprobar qué archivos cargó cada sesión (web 3.1).
2. Convenciones seguidas "de forma inconsistente entre sesiones" y se pide el "most efficient first diagnostic step": `/memory` (Guía PDF p. 123).
3. Si el archivo no carga, la causa puede ser ubicación incorrecta, typo en el nombre o alcance de directorio erróneo; si carga, el problema es la naturaleza advisory y puede hacer falta un hook (Guía PDF p. 123).

**Qué NO hacer:**
- No usar `/memory` para "activar" configuración (web 3.1).
- No saltar a añadir más ejemplos, crear rules por ruta o buscar instrucciones en conflicto antes de confirmar que el archivo carga (Guía PDF p. 123).

**Posible confusión con otros conceptos:**
- `/memory` vs `/context` — según la web (comprobado 6 octubre 2026), `/memory` lista CLAUDE.md, CLAUDE.local.md y auto-memory y los abre en el editor; `/context` informa de lo cargado al inicio bajo Memory files. Los CLAUDE.md de subdirectorio y las rules con `paths` cargan bajo demanda y no aparecen en esa lista; al cargar, aparece una línea Loaded con su ruta (web 3.1). En el examen se responde `/memory` (web 3.1).

### Trampas del examen

- Nuevo miembro del equipo con resultados inconsistentes: las convenciones estaban en `~/.claude/CLAUDE.md` del primer desarrollador (user-level, sin versionar); la solución es moverlas al nivel de proyecto (web 3.1; Slides PDF p. 658; Q41). En Q41 fallan A (versión desactualizada, mecanismo inexistente), C (un `CLAUDE.md` raíz es ubicación válida) y D (A y D describen mecanismos que no existen) (Q41). En la web, fallan instalar un servidor MCP, "no ejecutó /memory" y "rules que el editor no carga" (web 3.1).
- Creer que `/memory` dispara la carga de configuración: solo diagnostica (web 3.1).
- Asumir que un CLAUDE.md de directorio es la mejor solución para convenciones entre directorios: aplica a un solo directorio; usar rules con glob patterns (web 3.1; Slides PDF p. 1057).
- CLAUDE.md de 400+ líneas con reglas aplicadas a archivos equivocados: la respuesta es partirlo en `.claude/rules/` con frontmatter por ruta (Q42). Falla B (borrar el raíz y duplicar reglas por paquete), C (usar `/memory` para indicar la sección a priorizar, depende de intervención manual cada sesión) y D (`@import` incondicional resuelve el mantenimiento pero no el problema de convenciones equivocadas, porque todo carga siempre) (Q42).
- Monorepo con cinco paquetes y raíz de 600 líneas: CLAUDE.md por paquete e `@import` en el raíz para lo común (Q54). Fallan B (secciones y avisos manuales, no escala), C (eliminar el raíz duplica convenciones y causa deriva) y D (clave `projects:` en el frontmatter; no resuelve el aislamiento por paquete) (Q54).
- Tratar CLAUDE.md como enforcement duro, confiar en el énfasis, o usar PreToolUse para formatear (Guía PDF p. 123; Guía PDF p. 131).
- Contradicciones entre raíz y subdirectorio, e ignorar `/memory` antes de reforzar (Guía PDF p. 123).
- Opciones que afirman "el alcance más específico gana" o "user-level anula project-level": no coinciden con los docs (web 3.1).
- Creer que dividir en imports reduce el contexto: el tamaño es el mismo (web 3.1).

- **Contradicción entre fuentes:** la guía dice que el contenido de CLAUDE.md se inyecta en el system prompt y que los archivos de usuario se fusionan "sin conflictos" con los de proyecto (Guía PDF p. 120; Guía PDF p. 121); la web dice que se entrega como mensaje de usuario, no como system prompt, y que los conflictos pueden resolverse arbitrariamente (web 3.1). Prevalece la guía en lo que el examen evalúa, anotando la discrepancia; ambas coinciden en que CLAUDE.md es advisory (Guía PDF p. 123; web 3.1).
- **Contradicción entre fuentes:** para el diagnóstico, la guía y el examen indican `/memory`; la web aclara que hoy `/context` muestra lo cargado (web 3.1). Prevalecen la guía y el banco: responder `/memory` (Guía PDF p. 123; web 3.1).

## Tarea 3.2 — Create and configure custom slash commands and skills (Crear y configurar slash commands personalizados y skills)

### Skills y slash commands (sistema unificado)

**Concepto:** una skill es un conjunto reutilizable y con nombre de instrucciones que Claude Code carga bajo demanda; es un archivo Markdown con archivos de apoyo y frontmatter YAML opcional (web 3.2). Los custom commands y las skills se fusionaron en un único sistema, el Skills system (web 3.2); se ejecutan escribiendo el nombre como slash command (web 3.2; Guía PDF p. 126).

**Ejemplos de uso (3, cortos):**
1. `.claude/commands/deploy.md` crea `/deploy`: es un archivo Markdown plano y el nombre del archivo es el nombre del comando (web 3.2).
2. `.claude/skills/deploy/SKILL.md` también crea `/deploy`: un directorio por skill con el nombre del comando y `SKILL.md` como entrypoint obligatorio (web 3.2).
3. `.claude/skills/migrate-component/SKILL.md` crea `/migrate-component`; el nombre del directorio determina el slash command y el contenido es Markdown con los pasos del flujo (Guía PDF p. 126).

**Qué NO hacer:**
- No coloques un archivo plano directamente en `.claude/skills/` (p. ej. `.claude/skills/review.md`) esperando un `/review`: no crea ningún comando (web 3.2).
- No asumas que `.claude/commands/` dejó de funcionar: sigue funcionando por compatibilidad hacia atrás y sus archivos existentes siguen sin cambios (web 3.2).

**Posible confusión con otros conceptos:**
- Skill vs command — la skill es un directorio con `SKILL.md`; el command es un `.md` plano; ambos crean el mismo `/comando` (web 3.2).

### Ubicación canónica de `.claude/skills/` vs `.claude/commands/`

**Concepto:** `.claude/skills/` es la ubicación canónica y se recomienda porque añade tres funciones que `.claude/commands/` no tiene (web 3.2). Un archivo de command acepta el mismo frontmatter YAML que una skill, excepto `name` y `paths` (web 3.2).

**Ejemplos de uso (3, cortos):**
1. Directorio de archivos de apoyo junto a `SKILL.md`, p. ej. el checklist de `/meds-check` (web 3.2).
2. Descubrimiento automático: Claude puede cargar la skill cuando coincide con tu intención (web 3.2).
3. Precedencia: si una skill y un command tienen el mismo nombre, gana la skill; un `.claude/commands/meds-check.md` residual pierde frente a la skill (web 3.2).

**Qué NO hacer:**
- No esperes que un command plano tenga directorio de archivos de apoyo ni descubrimiento automático (web 3.2).

### Alcance (scoping): proyecto vs usuario

**Concepto:** el alcance de proyecto (`.claude/skills/` o `.claude/commands/` dentro del repositorio) está versionado y se comparte por git; el de usuario (`~/.claude/skills/` o `~/.claude/commands/`) es personal, no versionado ni compartido (web 3.2). El patrón es el mismo en todo Claude Code: `.claude/` se comparte por git, `~/.claude/` es personal; aplica a CLAUDE.md, commands y skills, y rules (web 3.2).

**Ejemplos de uso (3, cortos):**
1. `/review` como `.claude/commands/review.md` con un checklist de equipo (errores, cobertura de tests, nombres de API, credenciales hardcodeadas): todo el que clona o hace pull lo recibe (web 3.2; Q4).
2. Una skill de usuario en `~/.claude/skills/` se carga en cada proyecto; sirve para flujos de productividad individual (web 3.2; Guía PDF p. 127).
3. Variante personal con otro nombre (p. ej. `/deep-meds-check`) en `~/.claude/skills/`: no anula ni entra en conflicto con la versión del equipo (web 3.2).

**Qué NO hacer:**
- No pongas un command compartido por el equipo en `~/.claude/commands/` ni `~/.claude/skills/`: no están versionados (web 3.2; Q4).
- No uses `~/.claude/skills/` para flujos de equipo que deban compartirse y versionarse (Guía PDF p. 128).

**Posible confusión con otros conceptos:**
- Proyecto vs usuario — `/review` del equipo en `.claude/commands/`; `/brainstorm` personal en `~/.claude/skills/` (web 3.2).

### Skills vs CLAUDE.md vs rules

**Concepto:** la distinción es cuándo se cargan las instrucciones: CLAUDE.md en cada sesión (siempre en contexto), rules de forma condicional según rutas de archivos, y skills bajo demanda cuando se invocan (Guía PDF p. 128). Las skills son flujos de trabajo específicos de una tarea; CLAUDE.md contiene estándares universales siempre cargados, sin paso de invocación (web 3.2).

**Ejemplos de uso (3, cortos):**
1. Convenciones de nombres de API para toda generación de código van en CLAUDE.md o `.claude/rules/` (web 3.2).
2. Un checklist de revisión de 8 puntos usado solo en PRs va en `.claude/skills/review/SKILL.md`; en rules requeriría el patrón `**/*`, que lo cargaría siempre, igual que CLAUDE.md (Guía PDF p. 128).
3. Convenciones para un tipo de archivo (p. ej. tests) encajan mejor en `.claude/rules/` con ámbito de ruta (web 3.2).

**Qué NO hacer:**
- No pongas procedimientos específicos de una tarea (revisión de código, análisis, plantillas de brainstorming) en CLAUDE.md (web 3.2; Guía PDF p. 128).
- No pongas material de referencia siempre activo en skills: estaría ausente hasta invocarla (web 3.2).

**Posible confusión con otros conceptos:**
- Skill — flujo bajo demanda que se carga al invocarlo (Guía PDF p. 128).
- Rules — se cargan automáticamente según las rutas de los archivos (Guía PDF p. 128).
- Slash command (slides) — manual: tú escribes el comando; skill: se activa al detectar coincidencia; CLAUDE.md: siempre activo (Slides PDF p. 858).

### Estructura y frontmatter de una skill (slides)

**Concepto:** una skill es una carpeta con un documento `SKILL.md` de dos partes: frontmatter (CUÁNDO) e instrucciones (CÓMO) (Slides PDF p. 855, 860). Claude compara tu mensaje con las descripciones por significado, no por palabras exactas, y activa la que mejor coincide (Slides PDF p. 856).

**Ejemplos de uso (3, cortos):**
1. Carpeta `pr-review/` con frontmatter (name + description) e instrucciones en lenguaje plano paso a paso (Slides PDF p. 855).
2. Skills personales en `~/.claude/skills` (privadas, te siguen en todos los proyectos) y de proyecto en `.claude/skills` (viajan con el repositorio) (Slides PDF p. 857).
3. Los cuatro campos de frontmatter de las slides: `name` y `description` requeridos; allowed tools y `model` opcionales (Slides PDF p. 882).

### Frontmatter: context: fork

**Concepto:** `context: fork` ejecuta la skill en un contexto de sub-agent aislado; la salida verbosa queda contenida en el fork y la conversación principal queda libre (web 3.2). Sin él, la salida de la skill entra en la conversación principal, consume tokens de la ventana de contexto y degrada las respuestas posteriores (web 3.2).

**Ejemplos de uso (3, cortos):**
1. Análisis de código, que produce listados extensos de archivos y fragmentos (web 3.2).
2. Brainstorming, que genera muchas alternativas y evaluaciones (web 3.2).
3. `/scaffold` con cientos de líneas de salida intermedia por lecturas y comandos Bash exploratorios: `context: fork` evita contaminar el contexto principal y solo la salida final vuelve a la sesión padre (Q43).

**Qué NO hacer:**
- No dejes una skill verbosa de análisis de código corriendo inline en la conversación principal (web 3.2).
- No muevas la skill de `.claude/skills/` a `.claude/commands/` para aislar la salida: no cambia el aislamiento de ejecución (Q43).

**Posible confusión con otros conceptos:**
- `allowed-tools: []` — impediría el uso de las herramientas de las que depende la skill; no aísla la salida (Q43).
- `argument-hint` — sirve para pedir/indicar parámetros de entrada, no para aislar salida (Q43).

### Frontmatter: allowed-tools y argument-hint

**Concepto:** el objetivo nombra tres opciones de frontmatter: `context: fork`, `allowed-tools` y `argument-hint` (web 3.2). `allowed-tools` lista herramientas y `argument-hint` muestra qué argumentos espera la skill (web 3.2).

**Ejemplos de uso (3, cortos):**
1. `allowed-tools` con `Read`, `Grep` y `Glob` para una skill de análisis de solo lectura (web 3.2).
2. `argument-hint: "Specify the module path to analyse (e.g., src/api/auth)"` (web 3.2).
3. Frontmatter completo de `~/.claude/skills/analyse-feature/SKILL.md`: `description`, `context: fork`, `allowed-tools` (Read, Grep, Glob) y `argument-hint` (web 3.2).

```yaml
---
description: "Analyse a feature area of the codebase and report structure, patterns and risks"
context: fork
allowed-tools:
- Read
- Grep
- Glob
argument-hint: "Provide a feature description or area of the codebase to analyse"
---
```

**Qué NO hacer:**
- En el examen, no respondas con el comportamiento actual del producto cuando la pregunta es sobre la guía: responde con la redacción de la guía (web 3.2).
- No uses `allowed-tools` como límite de seguridad en Claude Code actual: la frontera real son `disallowed-tools` o las reglas deny (web 3.2).

**Posible confusión con otros conceptos:**
- `allowed-tools` (guía del examen: restringe el acceso a herramientas) vs comportamiento actual (preaprueba herramientas sin prompt de permiso, no restringe) — ver contradicción abajo (web 3.2).
- `argument-hint` (guía: solicita parámetros requeridos si se invoca sin argumentos) vs comportamiento actual (etiqueta de autocompletado, no pregunta) (web 3.2).

### description y activación automática

**Concepto:** `description` no está en la lista de tres del examen, pero es el campo más importante en la práctica: Claude lo lee para decidir si la skill aplica; sin una descripción útil, la skill solo corre si escribes `/nombre` (web 3.2). Las descripciones están siempre en contexto; el cuerpo completo solo se carga al invocar la skill (web 3.2; Slides PDF p. 702-703).

**Ejemplos de uso (3, cortos):**
1. Flujo: inicio de sesión → lee descripciones de skills → detecta tarea relevante → carga el contenido completo (Slides PDF p. 702-703).
2. Descripción fuerte: dice qué hace y cuándo, con varias frases disparadoras, p. ej. "Reviews pull requests for code quality. Use when reviewing PRs, checking diffs, or doing code review" (Slides PDF p. 883).
3. Descripción débil: "Help with code" es demasiado genérica y Claude no sabe cuándo es relevante (Slides PDF p. 883).

**Qué NO hacer:**
- No omitas `description` en una skill que quieres que se active sola; la documentación la marca Recomendada y, si falta, se usa la primera línea no vacía del cuerpo (web 3.2).
- No pongas una descripción vaga sin palabras disparadoras que use tu equipo (Slides PDF p. 883).

### Trampas del examen

- Crear un archivo plano dentro de `.claude/skills/` (p. ej. `.claude/skills/review.md`) y esperar `/review`: falla porque una skill es un directorio con `SKILL.md`; el archivo plano solo crea comando en `.claude/commands/` (web 3.2).
- Colocar un comando de equipo en `~/.claude/commands/` (Q4 opción B): es personal y no versionado; el comando compartido va en `.claude/commands/` (Q4; web 3.2).
- Definir el comando en CLAUDE.md (Q4 opción C): CLAUDE.md es para instrucciones del proyecto, no para definiciones de comandos (Q4).
- Un `.claude/config.json` con un array `commands` (Q4 opción D): es un mecanismo que no existe (Q4).
- Distractores de ubicación para skills de equipo: `~/.claude/skills/` (nivel usuario, no compartido), `settings.json` (no es como funcionan las skills) o CLAUDE.md raíz (carga en cada sesión, no bajo demanda) (Guía PDF p. 128).
- Salida verbosa que contamina el contexto (Q43): `allowed-tools: []` (A) impide el uso de herramientas del que depende la skill; mover a `.claude/commands/` (C) no cambia el aislamiento; `argument-hint` (D) es para parámetros de entrada. La respuesta es `context: fork` (B) (Q43).
- Tratar las skills como CLAUDE.md para guía siempre activa: las skills se cargan bajo demanda y no moldean cada sesión; para convenciones en cada edición se usa CLAUDE.md o `.claude/rules/` (web 3.2).
- Poner flujos específicos de tarea en CLAUDE.md: se cargan en cada sesión consumiendo tokens sin valor (web 3.2; Guía PDF p. 128).
- Escenario de práctica de la web: la respuesta es `/review` en `.claude/commands/` y `/brainstorm` como `SKILL.md` en `~/.claude/skills/` con `context: fork` (Opción A); B comparte `/brainstorm` en commands, C obliga a copiar a mano en `~/.claude/commands/`, D pone `/review` en CLAUDE.md y usa `allowed-tools` en vez de `context: fork` (web 3.2).
- Confundir skills (bajo demanda) con rules (auto-cargadas según rutas de archivos) (Guía PDF p. 128).
- Preguntas sobre los campos de frontmatter: el examen pone a prueba las tres opciones `context: fork`, `allowed-tools` y `argument-hint`; `description` no figura en la lista de la guía (web 3.2).

- **Contradicción entre fuentes:** (1) La guía PDF dice que las skills solo se cargan cuando el desarrollador escribe el slash command (Guía PDF p. 126), mientras la web y las slides indican que Claude también las activa automáticamente por coincidencia con la descripción (web 3.2; Slides PDF p. 856); prevalece la guía, pero se anota la discrepancia; la web añade que `disable-model-invocation: true` exige invocación explícita (web 3.2). (2) La web indica que `allowed-tools` preaprueba herramientas y que `argument-hint` es solo una etiqueta (estado revisado el 6 de octubre de 2026), mientras la guía de examen v1.0 los describe como "restringe" y "solicita parámetros"; en el examen se responde con la redacción de la guía (web 3.2). (3) Las slides marcan `name` y `description` como requeridos (Slides PDF p. 882), mientras la web indica que `description` es Recomendada, no obligatoria (web 3.2); se anota sin resolver, ya que la guía PDF no trata este punto.

## Tarea 3.3 — Apply path-specific rules for conditional convention loading (Aplicar reglas específicas por ruta para la carga condicional de convenciones)

### Path-specific rules (.claude/rules/ con frontmatter `paths`)

**Concepto:** Una path-specific rule es un archivo en `.claude/rules/` que empieza con YAML frontmatter cuyo campo `paths` lista patrones glob; sus convenciones se cargan solo cuando se trabaja con un archivo que coincide (web 3.3; Guía PDF p. 124). Cuando Claude trabaja en archivos no relacionados, la regla queda fuera del contexto, lo que ahorra tokens y evita instrucciones irrelevantes (Guía PDF p. 124).

**Ejemplos de uso (3, cortos):**
1. `.claude/rules/terraform.md` con `paths: ["terraform/**/*"]` se carga solo al editar archivos bajo `terraform/` (Guía PDF p. 124; web 3.3).
2. `.claude/rules/typescript.md` con `paths: ["**/*.ts", "**/*.tsx"]` aplica sus convenciones a los archivos TypeScript (Guía PDF p. 125).
3. `.claude/rules/pipelines.md` con `paths: ["pipelines/**/*", ".github/**/*"]` cubre los scripts de CI/CD (Guía PDF p. 125).

```yaml
---
paths: ["terraform/**/*"]
---
# Terraform Conventions

- Use snake_case for all resource names
- Tag every resource with environment and team labels
- Never hardcode AMI IDs — use data sources
- All modules must have a variables.tf, outputs.tf, and README.md
```
(web 3.3)

Se pueden crear varios archivos de reglas, cada uno con sus propios patrones y convenciones propias del dominio; Claude solo carga los relevantes para los archivos con los que trabaja (Guía PDF p. 124-125). Los archivos de reglas están bajo control de versiones junto con el proyecto (Guía PDF p. 124). En las slides, las path-scoped rules se describen como "Load on-demand (when reading matching file patterns)" (Slides PDF p. 693).

**Qué NO hacer:**
- No usar `.claude/rules/` para instrucciones que deben aplicar en todas partes: esas van en el root CLAUDE.md (Guía PDF p. 126).
- No asumir que los archivos de reglas imponen cumplimiento determinista: son consultivos (advisory), como CLAUDE.md (Guía PDF p. 124, 126).
- No crear patrones de ruta superpuestos en varios archivos de reglas, porque pueden producir instrucciones contradictorias (Guía PDF p. 126).

**Posible confusión con otros conceptos:**
- CLAUDE.md raíz — se carga siempre, en cada sesión, sin importar qué archivos se editen (web 3.3; Guía PDF p. 125).
- CLAUDE.md de directorio — cubre solo su propio directorio (web 3.3).

### Patrones glob que cruzan todo el código

**Concepto:** En un glob, `**` coincide a través de varios niveles de directorios, de modo que un solo patrón puede describir un tipo de archivo repartido por todo el repositorio (web 3.3). Los patrones se pueden combinar y usar brace expansion para apuntar exactamente a los archivos deseados (Slides PDF p. 1059).

**Ejemplos de uso (3, cortos):**
1. `**/*.test.tsx` coincide con todos los archivos de test de la base de código, estén donde estén (web 3.3).
2. `src/api/**/*.ts` coincide solo con archivos TypeScript bajo `src/api/` (Slides PDF p. 1059).
3. `**/*.{ts,tsx}` coincide con todos los archivos TS y TSX; `**/*.test.{ts, tsx}` con todos los tests sin importar la ubicación (Slides PDF p. 1059).

Tabla de referencia de las slides (Slides PDF p. 1059):

| Patrón | Coincide con |
|---|---|
| `**/*.ts` | Todos los archivos TypeScript en cualquier directorio |
| `src/api/**/*.ts` | Archivos TypeScript solo bajo `src/api/` |
| `**/*.{ts,tsx}` | Todos los TS y TSX (brace expansion) |
| `**/*.test.{ts, tsx}` | Todos los archivos de test sin importar la ubicación |
| `src/**/*.{ts,tsx}` | Todos los TS/TSX bajo `src/` |

Las slides indican que las path-specific rules coinciden con archivos por patrón en lugar de por ubicación de directorio, con un único archivo de regla en `.claude/rules/` con YAML frontmatter (Slides PDF p. 1058), y que se aplican sin importar dónde esté el archivo en el proyecto (Slides PDF p. 1056).

Ejemplo de la web: tests junto a su código fuente en cuatro directorios (`components/`, `api/`, `utils/`, `pages/dashboard/`) quedan cubiertos con `paths: ["**/*.test.tsx", "**/*.test.ts"]` (web 3.3).

```yaml
---
paths: ["**/*.test.ts", "**/*.test.tsx", "**/*.spec.ts", "**/*.spec.tsx"]
---
# Test Conventions

- Use describe/it blocks with descriptive names that read as sentences
- Each test file must have at least one happy path and one error case
- Use factory functions for test data, not inline object literals
- Mock external services at the module boundary, not individual functions
- Assert behaviour, not implementation details
```
(web 3.3)

### Path-specific rules frente a CLAUDE.md de directorio

**Concepto:** Un CLAUDE.md de directorio cubre solo su propio directorio y encaja cuando las convenciones están contenidas en una sola carpeta; las path-specific rules cubren un tipo de archivo repartido por muchos directorios (web 3.3; Slides PDF p. 1056). La guía lo presenta como una alternativa más dirigida a los CLAUDE.md de subdirectorio (Guía PDF p. 124).

**Ejemplos de uso (3, cortos):**
1. Convenciones de un único paquete: CLAUDE.md de directorio (web 3.3).
2. Convenciones simples donde la estructura de directorios ya da un alcance natural: CLAUDE.md de subdirectorio (Guía PDF p. 125).
3. Tests co-ubicados con el código en 50+ directorios: una regla con glob patterns (web 3.3).

Por qué no un CLAUDE.md en cada directorio (50+ directorios con tests): 50+ copias de las mismas convenciones, cada directorio nuevo con tests necesita una copia, cualquier cambio exige actualizar los 50+ archivos y las copias acaban difiriendo por quedar desactualizadas (web 3.3). Un archivo de regla y un patrón evitan los cuatro problemas (web 3.3).

Comportamiento de tokens según la guía: el CLAUDE.md de subdirectorio se carga cuando se trabaja en ese directorio; `.claude/rules/` se carga solo cuando se tocan archivos coincidentes (Guía PDF p. 125). Las slides lo describen como "Loads on demand when Claude reads files in that directory" (Slides PDF p. 1056).

**Qué NO hacer:**
- No colocar una copia de CLAUDE.md en cada directorio que contenga tests para convenciones transversales (web 3.3; Q6).
- No usar un CLAUDE.md de directorio cuando además se necesita filtrar por tipo de archivo con glob: no puede hacerlo (Q44).

**Posible confusión con otros conceptos:**
- CLAUDE.md de directorio — `infra/CLAUDE.md` aplicaría a todo lo que haya en `infra/`, sin filtrar por `.tf` (Q44).
- Path-specific rule — `paths` con globs que coinciden sin importar la ubicación (Slides PDF p. 1056).

### Path-specific rules frente a CLAUDE.md raíz (eficiencia de tokens)

**Concepto:** El CLAUDE.md raíz se carga en cada sesión sin importar los archivos editados, mientras que las path-scoped rules cargan solo al editar archivos coincidentes; esa es su ventaja principal en eficiencia de tokens (web 3.3; Guía PDF p. 124). Menos contexto irrelevante mantiene al modelo centrado en las convenciones aplicables (web 3.3).

**Ejemplos de uso (3, cortos):**
1. Instrucciones para todo el proyecto: CLAUDE.md raíz, "Always loaded" (Guía PDF p. 125).
2. Un CLAUDE.md raíz de 500 líneas que mezcla Terraform, Kubernetes y CI/CD gasta tokens cada vez que Claude trabaja en solo una de esas áreas; la solución son las path-scoped rules (Guía PDF p. 125).
3. Estándares de equipo en el CLAUDE.md raíz y convenciones de tests y Terraform en reglas por ruta (web 3.3).

Tabla de decisión (web 3.3):

| Escenario | Mejor enfoque |
|---|---|
| Estándares universales del equipo para todo el código | CLAUDE.md raíz |
| Convenciones de un directorio de paquete concreto | CLAUDE.md de directorio |
| Convenciones de un tipo de archivo repartido por muchos directorios | Path-specific rules con glob patterns |
| Workflows de tarea invocados bajo demanda | Skills en `.claude/skills/` |

Tabla de la guía (Guía PDF p. 125): Root CLAUDE.md — instrucciones de todo el proyecto, siempre cargado; Subdirectory CLAUDE.md — convenciones simples por directorio, cargado al trabajar en ese directorio; `.claude/rules/` — convenciones específicas de dominio para tipos de archivo distintos, cargado solo al tocar archivos coincidentes; los tres están bajo control de versiones.

Usa `.claude/rules/` cuando el proyecto tiene áreas distintas con convenciones diferentes y quieres minimizar el consumo de tokens (Guía PDF p. 125).

**Qué NO hacer:**
- No poner convenciones específicas de un tipo de archivo en el CLAUDE.md raíz: las de Terraform consumirían tokens al editar componentes React (web 3.3).
- No confiar en que Claude infiera qué sección del CLAUDE.md raíz aplica (Q6; Q44).

**Posible confusión con otros conceptos:**
- CLAUDE.md raíz con secciones por área — carga todo siempre; las reglas por ruta cargan solo lo que coincide (Q6; web 3.3).
- Instrucción en el system prompt para aplicar reglas solo a `.tf` — depende de la inferencia de Claude, no de un emparejamiento explícito de rutas (Q44).

### Path-specific rules frente a skills

**Concepto:** Las skills son definiciones de workflow reutilizables en `.claude/skills/<skill-name>/SKILL.md`, invocadas bajo demanda con un slash command; las rules se cargan según rutas de archivo (Guía PDF p. 125-126). Las slides las contrastan: CLAUDE.md es "Always on" y los Slash Commands son "Manual" (Slides PDF p. 860).

**Ejemplos de uso (3, cortos):**
1. `.claude/skills/migrate-component/SKILL.md` crea el slash command `/migrate-component` (Guía PDF p. 126).
2. Una skill es la opción correcta para instrucciones necesarias ocasionalmente en workflows específicos, no como contexto persistente (Guía PDF p. 126).
3. Convenciones por tipo de archivo que deben aplicarse sin que nadie invoque nada: regla en `.claude/rules/` (web 3.3).

**Qué NO hacer:**
- No crear skills con las convenciones y esperar que se apliquen solas: requieren invocación manual (Q6; Q44; Guía PDF p. 126).
- No hacer que los desarrolladores invoquen `/test-conventions` antes de editar tests cuando se quiere carga automática (web 3.3).

**Posible confusión con otros conceptos:**
- Skill — carga cuando un desarrollador la invoca con el slash command (Guía PDF p. 126).
- Rule — carga cuando se tocan archivos que coinciden con `paths` (Guía PDF p. 126).

### Verificación de la carga condicional y ejemplos de reglas por dominio

**Concepto:** La carga condicional se puede comprobar con `/context`: al arrancar lista los archivos CLAUDE.md y de reglas cargados, y una regla con alcance por ruta se carga cuando Claude lee un archivo coincidente, con un aviso de una línea "Loaded" (web 3.3).

**Ejemplos de uso (3, cortos):**
1. Al lanzar, `/context` no lista ninguna de las tres reglas con alcance por ruta bajo Memory files; al editar un `.test.ts`, el terminal muestra "Loaded" para `.claude/rules/testing.md` y no para las de API ni Terraform (web 3.3).
2. En una sesión nueva, editar un archivo en `src/api/` muestra "Loaded" para `.claude/rules/api-conventions.md` y no para testing ni Terraform (web 3.3).
3. Con todo en el CLAUDE.md raíz, `/context` lo lista al arrancar con el conjunto completo; con reglas por ruta, solo carga la coincidente, y el recuento de tokens es menor (web 3.3).

Reglas de ejemplo de la web (web 3.3):

```yaml
---
paths: ["src/api/**/*", "**/routes/**/*", "**/*.controller.ts"]
---
# API Conventions

- All endpoints return { data, error, metadata } response shape
- Use Zod schemas for request validation at the handler boundary
- Log request ID on every error response
- Rate limiting configuration must be explicit, not inherited from defaults
```

```yaml
---
paths: ["terraform/**/*", "**/*.tf", "infrastructure/**/*"]
---
# Infrastructure Conventions

- State files must reference remote backends, never local
- Use workspaces for environment separation
- Every module must be versioned with a CHANGELOG
```

Ejemplo de la guía en formato de lista YAML (Guía PDF p. 124):

```yaml
---
paths:
  - "terraform/**/*"
---
```

### Trampas del examen
- Elegir un CLAUDE.md por directorio para convenciones transversales: con tests en 50+ directorios exigiría un archivo en cada uno, una carga de mantenimiento enorme; la respuesta correcta son las reglas con glob patterns (web 3.3; Q6 opción D: "can't easily handle files spread across many directories").
- Consolidar todo en el CLAUDE.md raíz con encabezados por área (Q6 opción B): falla porque depende de que Claude infiera qué sección aplica en lugar de un emparejamiento explícito (Q6). Además se carga en cada sesión sin importar los archivos editados (web 3.3; Guía PDF p. 125).
- Añadir reglas Terraform al CLAUDE.md raíz e indicar en el system prompt que solo se apliquen a `.tf` (Q44 opción C): falla por inferencia, no por emparejamiento explícito de rutas, y da comportamiento inconsistente (Q44).
- Crear skills con las convenciones (Q6 opción C; Q44 opción D; web 3.3 opción A): falla porque requieren invocación manual y no se activan automáticamente (Q6; Q44).
- CLAUDE.md dentro de `infra/` (Q44 opción A): funcionaría para archivos dentro de `infra/`, pero no puede usar glob patterns para filtrar por tipo de archivo (Q44).
- Si una pregunta menciona un CLAUDE.md raíz demasiado grande (p. ej. 500+ líneas) con reglas irrelevantes que consumen tokens al trabajar en tipos de archivo concretos, la respuesta es `.claude/rules/` con frontmatter YAML de alcance por ruta (Guía PDF p. 126).
- El examen presenta con frecuencia tests junto a sus archivos fuente en muchos directorios; la respuesta es siempre reglas por ruta con glob patterns (web 3.3). También prueba repos de infrastructure-as-code o monorepos con tipos de archivo distintos (Guía PDF p. 126).
- Creer que las reglas imponen cumplimiento determinista: son advisory, como CLAUDE.md (Guía PDF p. 124, 126).
- Usar `.claude/rules/` para instrucciones globales (deben ir en el CLAUDE.md raíz) o crear patrones superpuestos entre archivos de reglas, con riesgo de instrucciones en conflicto (Guía PDF p. 126).
- Pregunta de práctica de la web: tests co-ubicados en 50+ directorios, carga solo al trabajar en un test y sin nada que invocar; la respuesta es la opción B, un archivo `.claude/rules/` con `paths: ["**/*.test.tsx", "**/*.test.ts"]` (web 3.3).
- **Contradicción entre fuentes:** la web afirma que tanto las skills como `.claude/rules/` pueden activarse automáticamente mediante un campo `paths` y que las reglas permanecen en contexto una vez que Claude lee un archivo coincidente (web 3.3), mientras que la guía y el banco describen las skills como bajo demanda, cargadas solo al invocarse explícitamente, y sin activación automática (Guía PDF p. 126; Q6; Q44). Prevalecen la guía y el banco: para la carga automática por tipo de archivo, reglas por ruta.

## Tarea 3.4 — Determine when to use plan mode vs direct execution (Determinar cuándo usar plan mode frente a direct execution)

### Plan mode

**Concepto:** En plan mode, Claude lee el codebase, analiza dependencias y propone un enfoque sin modificar ningún archivo (web 3.4); es el modo "think before acting": analiza, evalúa tradeoffs y presenta un plan sin hacer cambios (Guía PDF p. 136). No escribe nada en disco hasta que apruebas el plan (web 3.4).

**Ejemplos de uso (3, cortos):**
1. Reestructurar un monolito en microservicios, refactorizar una abstracción central o reorganizar un módulo: cambios a gran escala (web 3.4; Q5).
2. Elegir entre WebSockets, Server-Sent Events o polling: hay varios enfoques y se necesita un análisis de tradeoffs (Guía PDF p. 137, 138).
3. Bug crítico de producción en un módulo que no conoces: primero se entiende la arquitectura, se enumeran posibles causas raíz y se priorizan (Guía PDF p. 137, 138).

Criterios de uso según la web: cambios a gran escala, varios enfoques válidos, decisiones de arquitectura (límites de servicios, dependencias entre módulos, contratos de API), modificaciones en varios archivos (una migración de librería que afecta 45+ archivos) y necesidad de explorar el codebase (web 3.4). La guía añade: no conoces el área del módulo, y auditorías de seguridad o migraciones grandes que requieren mapear rutas de código en muchos archivos (Guía PDF p. 137).

Ejemplo trabajado de la guía: sin plan mode, pedir "fix the concurrency bug" en el inventory service obliga a Claude a adivinar la arquitectura, la estrategia de locking y la causa raíz; con plan mode lee la estructura, identifica los patrones de acceso a la base de datos, mapea los mecanismos de locking, enumera posibles race conditions y presenta una lista priorizada; el desarrollador la revisa antes de pedir la implementación (Guía PDF p. 137).

Cómo activarlo: se cambia a plan mode, no se "pide" en el texto (web 3.4):
- iniciar la sesión con `claude --permission-mode plan` (web 3.4)
- pulsar Shift+Tab durante la sesión hasta que la barra de estado muestre plan mode (web 3.4)
- prefijar un prompt con `/plan` (web 3.4)

**Qué NO hacer:**
- Escribir "in plan mode" dentro del cuerpo de un prompt: no hace nada; lo que cambia el modo es `/plan` al inicio del prompt (web 3.4).
- Usar plan mode para un fix de un solo archivo con stack trace claro: añade sobrecarga innecesaria (web 3.4).

**Posible confusión con otros conceptos:**
- Direct execution — corregir una validación de fecha en una función; no hay decisiones de diseño que resolver (web 3.4; Guía PDF p. 137).

### Direct execution

**Concepto:** Direct execution es el modo "just do it": Claude lee código, hace cambios, ejecuta tests y entrega el resultado (Guía PDF p. 136); se salta la fase de planificación y cambia directamente (web 3.4). Es para cambios bien entendidos con alcance claro y limitado (web 3.4).

**Ejemplos de uso (3, cortos):**
1. Corregir un bug de un solo archivo con stack trace claro (web 3.4).
2. Añadir una validación de fecha o un null check a una función/condicional (web 3.4; Guía PDF p. 137, 138; Q45).
3. Actualizar un valor de configuración, o renombrar `getUserData` a `fetchUserProfile` en todas partes (tarea mecánica con resultado claro) (web 3.4; Guía PDF p. 138).

Criterios: el cambio está bien acotado, ya se conoce el enfoque correcto (qué, dónde y cómo) y el alcance es limitado: una función, un archivo, una modificación (web 3.4; Guía PDF p. 137). La guía añade que la tarea es simple, bien acotada y de bajo riesgo (Guía PDF p. 137). Un plan resuelve decisiones de diseño; una tarea simple y bien definida no tiene ninguna, así que planificar no aporta nada (web 3.4).

**Qué NO hacer:**
- Usar plan mode "por precaución" ante cualquier cambio de código: es una heurística sobre-cautelosa que no refleja el uso previsto de plan mode (Q45).
- Planificar en varias fases una tarea mecánica y bien definida: añade sobrecarga sin mejorar el resultado (Guía PDF p. 138).

**Posible confusión con otros conceptos:**
- Plan mode — migrar una librería en 45 archivos: gran alcance y múltiples decisiones (Guía PDF p. 138).

### Criterio de decisión: ambigüedad, no dificultad

**Concepto:** La elección del modo depende de la ambigüedad, no de la dificultad (web 3.4). La decisión no es cuestión de preferencia ni de dificultad, sino de si la tarea se beneficia de un análisis explícito antes de actuar (Guía PDF p. 136).

**Ejemplos de uso (3, cortos):**
1. Un bug difícil pero bien definido (stack trace claro, una función, causa conocida) — direct execution (web 3.4).
2. Una petición aparentemente simple que podría implementarse de tres maneras y afecta a varios módulos — plan mode (web 3.4).
3. "Improve error handling across a module": ambigua, con muchas decisiones y preocupaciones que interactúan — plan mode (Guía PDF p. 138).

Tabla de decisión de la web (web 3.4):

| Característica de la tarea | Modo |
|---|---|
| Reestructuración arquitectónica | Plan mode |
| Migración de librería (muchos archivos) | Plan mode (luego direct execution) |
| Varios enfoques de implementación válidos | Plan mode |
| Necesidad de explorar el codebase | Plan mode (con Explore subagent) |
| Bug de un archivo con stack trace claro | Direct execution |
| Añadir una validación a una función | Direct execution |
| Actualizar un valor de configuración | Direct execution |
| Fix conocido, ubicación conocida, enfoque conocido | Direct execution |

Tabla de la guía (Guía PDF p. 138): validación de fecha en una función — direct execution; bug crítico en módulo desconocido — plan mode; WebSockets vs SSE vs polling — plan mode; renombrar `getUserData` a `fetchUserProfile` en todas partes — direct execution; migración de librería en 45 archivos — plan mode; null check en un condicional — direct execution; mejorar el manejo de errores en un módulo — plan mode.

Flujo multi-fase (analizar → proponer → implementar con revisión): se beneficia la tarea ambigua, compleja o con varios enfoques válidos; no se beneficia la tarea mecánica y bien definida con resultado correcto claro (Guía PDF p. 138). Tip de la guía: si una pregunta pide cuál de dos peticiones se beneficia más de un workflow multi-fase explícito, es siempre la tarea ambigua y de juicio, no la transformación mecánica (Guía PDF p. 138).

**Qué NO hacer:**
- Equiparar "difícil" con "plan mode": un fix difícil pero bien definido va en direct execution (web 3.4).
- Equiparar "parece simple" con "direct execution" cuando hay varias formas de implementarlo y afecta a varios módulos (web 3.4).

**Posible confusión con otros conceptos:**
- Dificultad — un bug complejo con causa conocida sigue siendo direct execution (web 3.4).
- Ambigüedad — una función nueva con tres diseños posibles exige plan mode (web 3.4).

### Reconocer la complejidad desde el principio

**Concepto:** Si los requisitos ya indican que la tarea es compleja (por ejemplo "restructure the monolith into microservices"), se elige plan mode de inmediato; esa complejidad no "aparecerá" más tarde, ya está en la descripción (web 3.4).

**Ejemplos de uso (3, cortos):**
1. Reestructurar un monolito en microservicios con decisiones sobre límites de servicio y dependencias: plan mode desde el inicio (web 3.4; Q5).
2. Dividir un sistema de reservas en servicios separados (ejemplo de la web): complejidad ya declarada (web 3.4).
3. Cambios en docenas de archivos con decisiones de arquitectura: explorar y diseñar antes de modificar (Q5).

**Qué NO hacer:**
- Empezar en direct execution y pasarse a plan mode solo si surge complejidad inesperada (web 3.4; Q5).
- Empezar con cambios incrementales esperando que la implementación revele los límites naturales de los servicios: riesgo de rework costoso al descubrir dependencias tarde (Q5).
- Dar direct execution con instrucciones previas muy detalladas: asume que ya se conoce la estructura correcta sin explorar el código (Q5).

**Posible confusión con otros conceptos:**
- Enfoque híbrido — la complejidad conocida se afronta con plan mode primero y ejecución después, no con un cambio tardío de modo (web 3.4).

### Enfoque híbrido: plan y luego execute

**Concepto:** Combinación habitual: plan mode para investigar y después direct execution para implementar (web 3.4). Decidir el patrón una vez hace que todos los archivos reciban el mismo cambio (web 3.4).

**Ejemplos de uso (3, cortos):**
1. Fase de plan: identificar todos los archivos que importan la librería antigua (web 3.4).
2. Fase de plan: mapear las diferencias de API entre librería antigua y nueva, diseñar el patrón de migración y revisar casos límite (web 3.4).
3. Fase de execute: aplicar el patrón de migración archivo por archivo con el enfoque planificado; la estrategia ya está decidida (web 3.4).

**Qué NO hacer:**
- Elegir un solo modo para todo: el examen espera que identifiques el híbrido (plan mode primero y luego direct execution) (web 3.4).
- Aplicar una migración multiarchivo sin plan: riesgo de aplicarla de forma inconsistente (web 3.4).

**Posible confusión con otros conceptos:**
- Plan mode para todo (opción B del escenario) — falla porque la tarea (2) de un solo archivo no necesita planificación (web 3.4).
- Direct execution tras plan — se usa después de planificar, no como comprobación posterior (Q45).

### Explore subagent

**Concepto:** El Explore subagent mantiene la salida verbosa del descubrimiento fuera de la conversación principal: ejecuta la exploración en aislamiento, produce resúmenes de sus hallazgos y los devuelve a la conversación principal, dejando libre la ventana de contexto para la implementación (web 3.4; Q46).

**Ejemplos de uso (3, cortos):**
1. Mapear los archivos que importan la librería de logging antigua (web 3.4).
2. Exploración con muchos resultados de herramientas (lecturas completas de archivos, búsquedas, trazas de dependencias) antes de una migración: devuelve un resumen estructurado (Q46).
3. Tareas multi-fase donde el descubrimiento genera listados de archivos, grafos de dependencias, extractos de código y notas de análisis (web 3.4).

**Qué NO hacer:**
- Hacer el descubrimiento verboso en la conversación principal: llena la ventana de contexto y degrada las respuestas posteriores (web 3.4).
- Acumular resultados en bruto en la sesión principal en lugar de recibir un resumen (Q46).

**Posible confusión con otros conceptos:**
- `/compact` — ejecutarlo tras cada tool call es operativamente engorroso y pierde detalle que aún puede hacer falta (Q46).
- Limitar la lectura a archivos de entrada — restringe artificialmente la exploración y deja incompleto el análisis (Q46).

### Trampas del examen

- Usar direct execution por defecto en cambios arquitectónicos multiarchivo: con varios enfoques válidos se requiere plan mode; direct execution arriesga rework costoso al descubrir dependencias tarde (web 3.4; Q5).
- Empezar con cambios incrementales "dejando que la implementación revele" los límites de servicio: riesgo de rework (Q5).
- Direct execution con instrucciones previas exhaustivas para el monolito: presupone conocer la estructura correcta sin explorar (Q5).
- Empezar en direct execution y cambiar a plan mode solo ante complejidad inesperada: ignora que la complejidad ya está declarada en los requisitos (web 3.4; Q5).
- Plan mode para un null-check o un fix de un solo archivo con stack trace claro: añade sobrecarga; el problema, la ubicación y la solución ya son claros (web 3.4; Q45).
- "Cualquier cambio de código podría tener efectos secundarios, así que explorar primero" (opciones A y C de Q45): heurística sobre-cautelosa que no refleja el uso previsto de plan mode (Q45).
- Direct execution primero y un "plan mode scan" después (opción D de Q45): invierte el flujo; plan mode se usa antes de ejecutar, no como comprobación posterior (Q45).
- Pasar a direct execution a mitad de la exploración para usar menos tool calls (opción A de Q46): abandona prematuramente la exploración arquitectónica (Q46).
- Ejecutar `/compact` tras cada tool call (opción C de Q46): ayuda, pero es engorroso y pierde detalle (Q46).
- Restringir la lectura a archivos de entrada (opción D de Q46): análisis incompleto en migraciones complejas; la técnica correcta es el Explore subagent (Q46).
- Hacer el descubrimiento verboso en la conversación principal: degrada respuestas posteriores (web 3.4).
- Escenario de práctica: direct execution para las tres tareas (opción A) o plan mode para las tres (opción B) fallan; la web plantea la opción C (plan mode para monolito y migración de logging, direct execution para el null pointer de una función) frente a la D (direct execution también para la migración); la migración de 30 archivos con librerías que manejan distinto niveles de log y contexto estructurado encaja con plan mode (web 3.4).
- Escribir "in plan mode" dentro del texto del prompt creyendo que cambia el modo: no hace nada; se usa `/plan`, Shift+Tab o `--permission-mode plan` (web 3.4).
- Confundir dificultad con ambigüedad al elegir el modo (web 3.4; Guía PDF p. 136).
- Preguntas de "qué petición se beneficia más de un workflow multi-fase": la respuesta es la ambigua y de juicio, no la mecánica (Guía PDF p. 138).

## Tarea 3.5 — Apply iterative refinement techniques for progressive improvement (Aplicar técnicas de refinamiento iterativo para una mejora progresiva)

> Prioridad de estudio: Refinamiento iterativo (débil: 25% -> 50%)

### Refinamiento iterativo y sus cinco técnicas

**Concepto:** el refinamiento iterativo consiste en guiar a Claude Code hacia el resultado correcto en varias rondas, porque la primera salida rara vez es la final (web 3.5). Se apoya en cinco técnicas: ejemplos concretos de entrada/salida, test-driven iteration, interview pattern, batch feedback y sequential feedback (web 3.5). Lo que hace avanzar la iteración es una señal clara e inequívoca de qué cambiar (Guía PDF p. 139).

**Ejemplos de uso (3, cortos):**
1. Una transformación descrita en prosa que Claude Code aplica distinto cada vez: se pasa a ejemplos concretos de entrada/salida (web 3.5).
2. Una transformación compleja con muchos casos límite: se escriben primero los tests y se comparten los fallos (web 3.5; Guía PDF p. 139).
3. Un dominio desconocido, como una capa de caché: se pide a Claude que haga preguntas antes de implementar (web 3.5).

**Qué NO hacer:**
- Dar feedback vago como "try again" o "do better": deja a Claude adivinando (Guía PDF p. 139).
- Usar coaching subjetivo como "handle edge cases better" o "be more careful": no da nada sólido sobre lo que actuar (Guía PDF p. 139).
- Dar énfasis ("IMPORTANT: think harder"), pedir regenerar todo o editar el código a mano en lugar de aportar un caso de prueba concreto (Guía PDF p. 142).

**Posible confusión con otros conceptos:**
- Feedback concreto — resultados de tests, mensajes de error y pares específicos de entrada/salida (Guía PDF p. 139).
- Feedback subjetivo — "handle edge cases better" (Guía PDF p. 139).

### Ejemplos concretos de entrada/salida

**Concepto:** es la técnica más eficaz cuando una descripción en prosa se interpreta de forma inconsistente; se dan 2-3 ejemplos con la entrada exacta y la salida exacta esperada (web 3.5; Q47). El modelo generaliza desde los ejemplos de forma más fiable que desde cualquier prosa (web 3.5).

**Ejemplos de uso (3, cortos):**
1. `getUserData(userId: string): Promise<UserData>` pasa a `Promise<Result<UserData, ApiError>>` (web 3.5).
2. `fetchOrders(customerId: string): Promise<Order[]>` pasa a `Promise<Result<Order[], ApiError>>` (web 3.5).
3. `"3/15/2024" -> "2024-03-15"` es inequívoco, a diferencia de "use ISO 8601" (Q47).

```text
Input:
getUserData(userId: string): Promise<UserData>

Expected output:
getUserData(userId: string): Promise<Result<UserData, ApiError>>
```

**Qué NO hacer:**
- Reescribir la prosa con más precisión: sigue dependiendo de la interpretación, así que más prosa no arregla el problema (web 3.5).
- Usar mayúsculas y repetición para dar énfasis: el énfasis no resuelve la ambigüedad (Q47).
- Ponerse a escribir todos los casos posibles: bastan 2-3 ejemplos bien elegidos que cubran el caso estándar y el caso límite principal (web 3.5).

**Posible confusión con otros conceptos:**
- Ejemplos de entrada/salida — el desarrollador conoce la transformación exacta pero el modelo la interpreta de forma inconsistente (web 3.5).
- Interview pattern — el desarrollador no conoce el dominio y puede pasar por alto consideraciones (web 3.5).

### Cómo pasar de prosa a ejemplos

**Concepto:** secuencia de cuatro pasos cuando la prosa da resultados inconsistentes (web 3.5).

**Ejemplos de uso (3, cortos):**
1. Observar la inconsistencia: la misma descripción produce salidas distintas en cada ejecución (web 3.5).
2. Cambiar a 2-3 pares antes/después y verificar la generalización probando un caso nuevo (web 3.5).
3. Añadir ejemplos de casos límite si el modelo resuelve el caso estándar pero falla en los bordes (web 3.5; Guía PDF p. 141).

**Qué NO hacer:**
- Saltarse la verificación en un caso nuevo: es lo que confirma que el modelo generaliza el patrón (web 3.5).
- Describir el problema en lenguaje natural cuando falla un caso límite: es más eficaz dar una entrada concreta y mostrar exactamente la salida esperada (Guía PDF p. 141-142).

**Posible confusión con otros conceptos:**
- Ejemplos concretos vs. few-shot — la guía explica que funcionan por la misma razón por la que few-shot supera a zero-shot: mostrar el comportamiento exacto elimina la ambigüedad (Guía PDF p. 142).

### Test-driven iteration

**Concepto:** se escriben primero los tests, que definen el comportamiento esperado, y se pide a Claude que escriba código que los pase; cuando fallan, se comparte la salida del fallo (Guía PDF p. 139). Es la técnica más eficaz para transformaciones complejas (web 3.5). Los tests cubren happy path, edge cases (valores null, entradas vacías, condiciones límite) y requisitos de rendimiento si aplican (web 3.5).

**Ejemplos de uso (3, cortos):**
1. Migrar registros antiguos: se escriben los tests antes y se comparten los fallos, como `FAIL: testMigrationHandlesNullValues` (web 3.5).
2. Un recorrido de grafo con ciclos, nodos desconectados y aristas con peso: se escribe la suite, se pide la implementación y se comparte "Test 3 failed: expected [A, B, D] but got [A, B, C, D]" (Guía PDF p. 139-140).
3. Repetir el ciclo implementar-ejecutar-compartir fallos hasta que todos los tests pasen (Guía PDF p. 140).

```text
FAIL: testMigrationHandlesNullValues
Expected: null preserved in output JSON
Actual: null replaced with empty string ""
```

**Qué NO hacer:**
- Describir el comportamiento deseado en lenguaje natural cuando los tests pueden definirlo con precisión (Guía PDF p. 139).
- Pedir "handle cycles better" en lugar de "this specific input produced this wrong output" (Guía PDF p. 140).

**Posible confusión con otros conceptos:**
- Test-driven iteration — el comportamiento está bien definido y los fallos dan feedback inequívoco ("Expected X, got Y" tiene un único significado) (web 3.5; Q48).
- Interview pattern — cuando el equipo aún no ha pensado en ciertas consideraciones; los tests no pueden revelarlas (Q48).

### Interview pattern y TBD marker pattern

**Concepto:** en un dominio desconocido, se pide a Claude que haga preguntas antes de implementar para revelar consideraciones que el desarrollador pasaría por alto (web 3.5). La guía añade el TBD marker pattern: una especificación con los requisitos conocidos y marcadores "TBD" en las áreas inciertas, para que Claude proponga una solución a cada TBD al implementar (Guía PDF p. 142). Ambos ayudan a sacar a la luz "unknown unknowns" antes de fijar la dirección de implementación (Guía PDF p. 142).

**Ejemplos de uso (3, cortos):**
1. En lugar de "Build me a caching layer for the API", pedir: "Before implementing, ask me questions about the requirements, edge cases, and constraints" (web 3.5).
2. Claude puede preguntar por estrategias de invalidación, políticas TTL, requisitos de consistencia y modos de fallo (web 3.5; Guía PDF p. 142).
3. Un módulo de autenticación: Claude plantea consideraciones de seguridad, casos límite y tradeoffs de diseño antes de implementar (Q48).

**Qué NO hacer:**
- Saltar directamente a una implementación mínima cuando los requisitos son inciertos (Guía PDF p. 142-143).
- Implementar un caché genérico basado en Redis con patrones estándar y revisar después la compatibilidad, en un servicio con patrones desconocidos (Q52).
- Empezar con una prueba de concepto mínima y descubrir los problemas en fallos de ejecución: difiere el descubrimiento (Q52).
- Usar el interview pattern cuando ya se conoce la transformación exacta: no hay consideraciones nuevas que revelar (web 3.5).

**Posible confusión con otros conceptos:**
- Interview pattern — Claude interroga al desarrollador y así surgen requisitos no previstos (Q52).
- Documento de diseño generado por Claude — produce un diseño pero no hace surgir de forma interactiva lo que el desarrollador aún no ha pensado (Q52).

### Batch feedback vs. sequential feedback

**Concepto:** la forma de entregar el feedback depende de si los arreglos interactúan (web 3.5; Q51). Batch: arreglos que interactúan, en un solo mensaje, para que el modelo vea todas las restricciones a la vez y dé un arreglo coherente (web 3.5). Sequential: problemas independientes, uno a la vez y verificando cada uno antes del siguiente (web 3.5; Q49).

**Ejemplos de uso (3, cortos):**
1. Cambiar el patrón de manejo de errores afecta al formato de logging y a la estructura de respuesta: se envían los tres cambios en un mensaje (web 3.5).
2. Un problema de nombres (camelCase) y otro de indentación (2 espacios), independientes: primero uno, se espera el resultado y luego el otro (web 3.5).
3. Dos bugs lógicos que interactúan se envían juntos; cinco nombres de variable inconsistentes se corrigen después, uno a uno (Q51).

```text
Three changes needed (they interact with each other):
1. Error responses must include an error code field
2. Logging must include the error code in structured format
3. The client SDK type definitions must reflect the new error code field
```

**Qué NO hacer:**
- Enviar por separado arreglos que interactúan: un arreglo apunta a un estado que el siguiente cambia (web 3.5; Q51).
- Agrupar problemas independientes: confunde al modelo sobre qué feedback aplica a qué parte del código (web 3.5; Q49).
- Pedir regenerar toda la función en lugar de parchear, lo que descarta código que funciona (Q49).
- Agrupar de forma arbitraria (por ejemplo, "ambos están en bucles") en vez de por interacción real (Q49).

**Posible confusión con otros conceptos:**
- Batch — arreglos con interacción real (Q51).
- Sequential — problemas independientes, aunque estén en el mismo módulo (Q49; Q51).

### Incremental problem solving (guía)

**Concepto:** la guía describe, para problemas que interactúan, arreglarlos uno a la vez probando después de cada cambio, empezando por el más fundamental (Guía PDF p. 141). Es más fiable que agrupar todo en un prompt porque los problemas que interactúan crean efectos en cascada difíciles de diagnosticar cuando todo cambia a la vez (Guía PDF p. 141).

**Ejemplos de uso (3, cortos):**
1. En un informe PDF: primero los anchos de columna, que son lo más fundamental (Guía PDF p. 141).
2. Luego el formato de fechas dentro de las columnas ya corregidas (Guía PDF p. 141).
3. Por último los saltos de página, que dependen de la altura del contenido (Guía PDF p. 141).

**Qué NO hacer:**
- Agrupar en un solo prompt arreglos que la guía considera interactuantes (Guía PDF p. 141, 143).
- Refactorizar archivos interconectados en paralelo o solo con verificación manual: la práctica indicada es procesar archivos en secuencia con tests (Guía PDF p. 165-166).

**Posible confusión con otros conceptos:**
- Incremental fixes (guía) — problemas que interactúan, probando tras cada paso (Guía PDF p. 141).
- Batch feedback (web y banco) — arreglos que interactúan en un solo mensaje (web 3.5; Q51). Ver contradicción abajo.

### @references para contexto puntual

**Concepto:** para una tarea puntual en la que Claude debe seguir patrones de código existente, se incluyen archivos concretos con la sintaxis `@` en el prompt (Guía PDF p. 142).

**Ejemplos de uso (3, cortos):**
1. Un módulo de procesamiento de pagos que siga los patrones de `db_utils.py` (Guía PDF p. 142).
2. Referenciar también `error_handlers.py` con `@` (Guía PDF p. 142).
3. Referenciar también `audit_logger.py` con `@` (Guía PDF p. 142).

**Qué NO hacer:**
- Describir los patrones en lenguaje natural: es menos preciso (Guía PDF p. 142).
- Añadirlos a CLAUDE.md para una tarea puntual: se cargarían en cada sesión (Guía PDF p. 142-143).
- Pedir a Claude que explore el código para encontrar los patrones: es más lento y menos dirigido (Guía PDF p. 142).

**Posible confusión con otros conceptos:**
- @references — contexto temporal de una tarea puntual (Guía PDF p. 143).
- CLAUDE.md — contexto que se carga en todas las sesiones (Guía PDF p. 142).

### Trampas del examen

- Refinar la prosa o hacerla más enfática cuando el modelo la interpreta de forma inconsistente: más prosa sigue dependiendo de la interpretación; la respuesta son 2-3 ejemplos concretos de entrada/salida (web 3.5; Q47). En Q47 la opción A (mayúsculas y repetición) falla porque el énfasis no resuelve la ambigüedad (Q47).
- Q47, opción C (plan mode): sirve para decisiones de arquitectura, no para refinar formato (Q47). Opción D (generar una función de formato y aplicarla en dos pasadas): añade complejidad y no aclara la transformación correcta (Q47).
- Usar el interview pattern cuando el desarrollador ya conoce la transformación exacta: no hay consideraciones que revelar (web 3.5). Es la confusión entre interview pattern y ejemplos de entrada/salida (web 3.5).
- Q48: la opción A (especificación detallada directa) se salta la oportunidad de detectar huecos antes de fijar la implementación; la C (implementación mínima y revisión) retrasa el descubrimiento cuando el coste de cambio es mayor; la D (suite de tests primero) es eficaz con comportamiento bien definido pero no revela lo que el equipo no ha pensado (Q48).
- Q49: con tres problemas independientes, la opción A (todo en un mensaje) es para problemas que interactúan; la C (regenerar) descarta código que funciona; la D agrupa de forma arbitraria (Q49).
- Q51: la opción A (los ocho en un mensaje) añade ruido; la C ordena por complejidad y no por interacción; la D (ocho mensajes secuenciales) aplica lo secuencial a bugs que interactúan y arriesga un arreglo incompleto (Q51).
- Q52: A (caché genérico), C (documento de diseño) y D (prueba de concepto mínima) fallan porque no hacen surgir de forma interactiva y antes de escribir código las consideraciones desconocidas (Q52).
- Enviar uno a uno arreglos que interactúan: un arreglo apunta a un estado que el siguiente cambia (web 3.5).
- Feedback vago o subjetivo ("handle edge cases better"), énfasis ("IMPORTANT: think harder"), regenerar todo o editar a mano, en vez de un caso de prueba concreto con entrada y salida esperada (Guía PDF p. 142-143).
- Saltar a la implementación con requisitos inciertos, en lugar de usar primero el interview pattern (Guía PDF p. 143).
- Añadir patrones a CLAUDE.md para una tarea puntual cuando @references mantendría el contexto temporal (Guía PDF p. 143).
- Pista de la guía: ante una función compleja con requisitos específicos y "efficient iterative refinement", la respuesta es test-driven iteration (Guía PDF p. 140). Ante una idea aproximada ("Redis with 5-minute TTL") de alguien nuevo en caché de producción, la respuesta implica interview o TBD, no una implementación mínima (Guía PDF p. 142).
- Tabla del examen según la web: prosa interpretada distinto cada vez → ejemplos concretos; transformación compleja con muchos casos límite → test-driven iteration; dominio desconocido → interview pattern; problemas que se afectan entre sí → batch feedback (un mensaje); problemas independientes → sequential feedback (web 3.5).
- **Contradicción entre fuentes:** para problemas que interactúan, la guía recomienda arreglarlos de uno en uno con pruebas tras cada paso y lista como error agruparlos en un prompt (Guía PDF p. 141, 143), mientras que la web y el banco indican enviarlos juntos en un solo mensaje (web 3.5; Q51). La regla de prioridad (guía y banco sobre la web) no resuelve el conflicto entre guía y banco; las preguntas del banco (Q51) coinciden con la web, y la guía discrepa.

## Tarea 3.6 — Integrate Claude Code into CI/CD pipelines (Integrar Claude Code en pipelines de CI/CD)

### Modo no interactivo con claude -p

**Concepto:** el flag `-p` (también `--print`) pone Claude Code en modo print/programático: procesa el prompt, escribe el resultado en stdout y termina sin esperar entrada del usuario (web 3.6; Slides PDF p. 1069; Guía PDF p. 146). Un pipeline de CI no tiene teclado, así que sin `-p` el job se queda colgado esperando una entrada que nunca llega (web 3.6; Q10).

**Ejemplos de uso (3, cortos):**
1. `claude -p "Analyse this pull request for security issues"` termina y deja el resultado en stdout (web 3.6).
2. Entrada por stdin: `cat logs.txt | claude -p "explain errors"` (Slides PDF p. 1071).
3. En GitHub Actions: `echo "$PR_DIFF" | claude -p --append-system-prompt "..." --max-turns 10` (Guía PDF p. 146).

**Qué NO hacer:**
- Ejecutar `claude "..."` sin `-p` en CI: el job se cuelga y los logs muestran a Claude esperando entrada (web 3.6; Q10).
- Usar `CLAUDE_HEADLESS=true` o `--batch`: no existen (web 3.6; Q10).
- Redirigir stdin desde `/dev/null`: es un workaround de Unix que no resuelve bien la sintaxis de Claude Code (web 3.6; Q10).

**Posible confusión con otros conceptos:**
- `-p` (modo no interactivo) — evita el cuelgue; no afecta al contenido de la salida ni a los tests generados (Q50).
- `--output-format json` — da salida parseable, pero no sustituye a `-p` (Q50; web 3.6).

### Salida estructurada para CI (--output-format json y --json-schema)

**Concepto:** en CI nadie lee la salida; la procesan sistemas automáticos (comentarios inline en el PR, dashboards, workflows posteriores), así que debe ser parseable por máquina (web 3.6). `--output-format json` devuelve un envelope JSON (un único objeto con texto del resultado, session ID y metadatos de coste y uso) y `--json-schema` valida la salida final contra un JSON Schema (solo print mode) (web 3.6).

**Ejemplos de uso (3, cortos):**
1. `claude -p --output-format json --json-schema '{...}' "Review this PR for security issues"` con un esquema de `findings` (web 3.6).
2. Extraer los datos validados con `jq '.structured_output'`, no del nivel superior del envelope (web 3.6).
3. Esquema con campos `file`, `line` y `comment` para publicar cada hallazgo como comentario inline en su línea (Q53; web 3.6).

```bash
claude -p \
--output-format json \
--json-schema '{"type":"object","properties":{"findings":{"type":"array","items":{"type":"object","properties":{"file":{"type":"string"},"line":{"type":"integer"},"severity":{"type":"string"},"message":{"type":"string"}}}}}}' \
"Review this PR for security issues"
```

**Qué NO hacer:**
- Parsear texto libre con regex: el formato deriva entre ejecuciones y el parser se rompe (Q53).
- Usar `--structured-output`, que no existe en la CLI de Claude Code; `--format json`, `--strict` y `-p --json` solo fuerzan formato JSON o no imponen un esquema, así que no garantizan la estructura de salida (Guía PDF p. 168-169).

**Posible confusión con otros conceptos:**
- `--output-format json` — garantiza formato JSON, pero no una estructura concreta (Guía PDF p. 168-169).
- `--json-schema` — impone la estructura; el resultado queda en `structured_output` si se combina con `--output-format json` (web 3.6).

### Aislamiento de contexto de sesión (revisión independiente y worktrees)

**Concepto:** la sesión que genera código acumula contexto de razonamiento (por qué eligió el enfoque, qué descartó), y revisar en esa misma sesión hace menos probable que cuestione sus propias decisiones (web 3.6). La solución es una llamada separada de Claude Code para la revisión, sin acceso a ese contexto (web 3.6). Complemento fuera de la guía: un git worktree es un segundo directorio de trabajo con su propia rama, y cada sesión en su worktree no modifica los archivos de otra (web 3.6).

**Ejemplos de uso (3, cortos):**
1. Sesión A: `claude -p "Implement the authentication middleware"` (web 3.6).
2. Sesión B, independiente: `claude -p "Review the authentication middleware for security issues, error handling gaps, and edge cases"` (web 3.6).
3. `claude --worktree <name>` crea `.claude/worktrees/<name>/` en la rama `worktree-<name>` y arranca ahí la sesión (web 3.6).

**Qué NO hacer:**
- Asumir que la autorrevisión en la misma sesión es tan eficaz como una revisión independiente (web 3.6).
- Esperar que los worktrees bloqueen archivos compartidos: nada los bloquea; las sesiones se coordinan por orden (la primera hace merge y la segunda hace rebase) (web 3.6).

**Posible confusión con otros conceptos:**
- Revisión independiente (dos llamadas `claude -p`) — separa generación y revisión para evitar sesgo (web 3.6).
- Worktrees — separan archivos entre sesiones paralelas, no sirven como revisión independiente (web 3.6).

### Contexto incremental de revisión

**Concepto:** las revisiones automáticas corren en cada push; sin contexto de revisiones previas, cada ejecución reanaliza todo el PR y repite los mismos hallazgos (web 3.6). La solución es incluir los hallazgos previos en el contexto e indicar a Claude que reporte solo problemas nuevos o aún sin resolver (web 3.6; Guía PDF p. 151).

**Ejemplos de uso (3, cortos):**
1. Pasar `${PREVIOUS_FINDINGS}` en el prompt de `claude -p --output-format json` (web 3.6).
2. Pedir "Report ONLY" issues nuevos y los previos todavía presentes (web 3.6).
3. Un desarrollador mantiene a propósito una lista de códigos postales fija: no debe re-reportarse en cada push (web 3.6).

**Qué NO hacer:**
- Revisar solo el diff del último commit o reanudar la sesión de la primera ejecución: el diff oculta hallazgos sin resolver y la sesión reanudada arrastra resultados de herramientas obsoletos (web 3.6).
- Restringir el alcance a archivos recién modificados (omite regresiones) o revisar solo al crear el PR y pre-merge (omite feedback intermedio) (Guía PDF p. 151).
- Usar filtros de post-procesado, que emplean coincidencia tosca de ruta/descripción (Guía PDF p. 151).

**Posible confusión con otros conceptos:**
- Contexto incremental — evita duplicados entre pushes; los comentarios duplicados reducen la confianza de los desarrolladores (web 3.6).
- Aislamiento de sesión — separa generación y revisión; no trata los duplicados (web 3.6).

### CLAUDE.md como contexto para CI

**Concepto:** en CI, Claude Code lee los CLAUDE.md del proyecto igual que en modo interactivo, así que es la vía para dar contexto específico: estándares de testing, fixtures disponibles, criterios de revisión y cobertura existente (web 3.6). Sin ese contexto, la generación de tests produce boilerplate de poco valor (web 3.6).

**Ejemplos de uso (3, cortos):**
1. Documentar el patrón factory de `test/factories/` y los fixtures `test/fixtures/users.json` y `test/fixtures/orders.json` (web 3.6).
2. Documentar en CLAUDE.md los estándares de testing, los fixtures y la instrucción de revisar los tests existentes antes de sugerir nuevos (Q50).
3. Documentar patrones aceptados (p. ej. force-unwrapping de optionals en tests) para que la revisión no los marque (Guía PDF p. 149).

```text
# .claude/CLAUDE.md — CI-relevant section
## Testing Standards

- Tests must use the factory pattern from test/factories/ for data creation
- Integration tests connect to the test database via test/setup/db.ts
- Do not test private implementation details — test public API contracts
- Coverage target: 80% branch coverage for new code
- Available fixtures: test/fixtures/users.json, test/fixtures/orders.json
```

**Qué NO hacer:**
- Filtrar duplicados con un script de post-procesado en vez de dar a Claude el contexto de los tests existentes (Q50).
- Resolver tests duplicados con `-p` o con `--output-format json`/`--json-schema`: no cambian el contenido de las sugerencias (Q50).

### Flags de CLI en CI y la GitHub Action

**Concepto:** además de `-p`, otros flags controlan una ejecución headless: formato de salida, system prompt, y alcance de permisos y herramientas (web 3.6). `--system-prompt` reemplaza por completo el prompt por defecto; `--append-system-prompt` le añade texto y conserva las herramientas integradas (Guía PDF p. 147-148; web 3.6).

| Flag | Efecto |
|---|---|
| `--system-prompt "<text>"` | Reemplaza todo el prompt por defecto (web 3.6) |
| `--system-prompt-file <path>` | Reemplaza el prompt por el contenido de un archivo (web 3.6) |
| `--append-system-prompt "<text>"` | Añade texto al prompt por defecto (web 3.6) |
| `--append-system-prompt-file <path>` | Añade el contenido de un archivo (web 3.6) |
| `--max-turns <n>` | Limita los turnos agénticos y sale (web 3.6); lo aplica Claude Code mismo (Guía PDF p. 147, 162) |
| `--max-budget-usd X` | Tope duro en dólares por invocación, aplicado por Claude Code (Guía PDF p. 147, 162) |
| `--permission-mode <mode>` | default, acceptEdits, plan, auto, dontAsk, bypassPermissions o manual (alias de default, v2.1.200+) (web 3.6) |
| `--allowedTools` / `--disallowedTools` / `--tools` | Herramientas sin prompt de permiso / reglas de denegación / herramientas integradas disponibles (web 3.6) |
| `--bare` | Modo mínimo: omite autodescubrimiento de hooks, skills, plugins, MCP servers, auto memory y CLAUDE.md (web 3.6) |

**Ejemplos de uso (3, cortos):**
1. `--append-system-prompt "Review for security issues and bugs. Report findings as JSON."` con `--max-turns 10` y `--max-budget-usd 2.00` (Guía PDF p. 146-147).
2. `--permission-mode dontAsk` auto-deniega los permisos no permitidos explícitamente, adecuado sin humano que apruebe (Guía PDF p. 148).
3. En `anthropics/claude-code-action@v1`, los flags se pasan en `claude_args` (p. ej. `--append-system-prompt`, `--allowedTools`, `--max-turns`) y con `prompt` se ejecuta en modo automation (web 3.6).

**Qué NO hacer:**
- Usar `--system-prompt` cuando Claude debe leer archivos circundantes: pierde la guía de herramientas y solo comenta el diff recibido por pipe (Guía PDF p. 147-148).
- Usar `timeout-minutes` del step de GitHub Actions en lugar de `--max-turns`/`--max-budget-usd`: lo aplica el job runner y mata el proceso sin que Claude termine limpiamente (Guía PDF p. 147-148).
- Meter la credencial literal en el archivo: va en un secret (`anthropic_api_key` o `claude_code_oauth_token`) (web 3.6).

**Posible confusión con otros conceptos:**
- `--permission-mode dontAsk` — controla permisos, no iteraciones ni coste (Guía PDF p. 147-148).
- `--max-turns` — controla iteraciones; un modelo más pequeño tampoco limita los totales (Guía PDF p. 147).
- `--bare` vs. CLAUDE.md — `--bare` omite CLAUDE.md, por lo que una revisión que lo necesita no debe usarlo (web 3.6).

### Patrones de calidad de la revisión automatizada

**Concepto:** la revisión automatizada equilibra precisión (evitar falsos positivos) y recall (detectar bugs reales); cada decisión de prompt desplaza ese balance (Guía PDF p. 148).

**Ejemplos de uso (3, cortos):**
1. Pocos aciertos (bajo recall): few-shot de categorías concretas (race conditions, null dereferences, error handling gaps) (Guía PDF p. 149).
2. Hallazgos correctos pero irrelevantes: criterios explícitos de qué reportar (bugs, vulnerabilidades) y qué omitir (estilo menor, patrones locales) (Guía PDF p. 150).
3. Severidad inconsistente: criterios con ejemplos de código concretos por nivel (Critical, Major, Minor, Skip) (Guía PDF p. 151).

**Qué NO hacer:**
- Pedir "only report high-confidence issues": suprime hallazgos correctos pero inciertos y conserva los seguros pero erróneos; mejor reportar todo con confianza y severidad y filtrar después (Guía PDF p. 150).
- Usar "be conservative" o "be more thorough": no definen el límite (Guía PDF p. 149, 152).
- Una revisión única para 14+ archivos o varias preocupaciones: dividir en prompts enfocados, cada uno con sus ejemplos, y consolidar antes de publicar (Guía PDF p. 151-152).

**Posible confusión con otros conceptos:**
- Campo `detected_pattern` — analiza la tasa de descarte por construcción de código (p. ej. 35% descartado), más accionable que categorías o scores de confianza (Guía PDF p. 150).
- Razonamiento y confianza inline — reducen el tiempo de investigación sin filtrar hallazgos (Guía PDF p. 150-151).
- Revisión agéntica turn-limited — para bugs entre archivos, con herramientas de lectura/búsqueda; requiere `--append-system-prompt` (Guía PDF p. 152).
- JSON truncado por `max_tokens` con `report_findings` — dividir en varias llamadas por subconjunto de archivos y fusionar los arrays de findings (Guía PDF p. 152).

### Batch API vs. API en tiempo real en CI

**Concepto:** la Message Batches API ofrece 50% de ahorro, pero el procesamiento puede tardar hasta 24 horas sin SLA de latencia garantizado; el factor de decisión es la tolerancia a la latencia (web 3.6; Guía PDF p. 152).

**Ejemplos de uso (3, cortos):**
1. Checks pre-merge (bloqueantes): API en tiempo real, porque los desarrolladores esperan el resultado (web 3.6).
2. Informes nocturnos de deuda técnica y auditoría semanal de código: Batch API (web 3.6).
3. Generación nocturna de tests, revisada a la mañana siguiente: Batch API (web 3.6).

**Qué NO hacer:**
- Usar la Batch API para checks pre-merge: no hay garantía de latencia y los desarrolladores no pueden hacer merge hasta que termine el check (web 3.6).

### Trampas del examen
- Colgado del job: elegir `CLAUDE_HEADLESS=true`, `--batch` o redirigir stdin desde `/dev/null`. Los dos primeros no existen y el tercero es un workaround de Unix que no resuelve la sintaxis de Claude Code; la respuesta es `-p` (Q10; web 3.6).
- Texto libre y regex para comentarios inline: endurecer instrucciones de formato (A), segunda llamada de Claude para normalizar (C) o pasar a un comentario resumen (D) fallan; A depende de que Claude mantenga el formato, C añade latencia y coste, D cambia la funcionalidad. Lo correcto es `--output-format json` con `--json-schema` (Q53).
- Tests duplicados: añadir `-p` (A) solo evita cuelgues; `--output-format json` con `--json-schema` (B) solo mejora la parseabilidad; el script de post-procesado (D) añade complejidad sin tratar la causa. Lo correcto es documentar en CLAUDE.md estándares, fixtures y revisar los tests existentes (Q50).
- Flags de salida inventados: `--format json` y `--strict` no imponen estructura; `-p --json` no obliga a un esquema; `--structured-output` con un esquema Pydantic no existe (Guía PDF p. 168-169).
- Autorrevisión en la misma sesión: retiene el contexto de razonamiento de la generación y cuestiona menos sus decisiones; una instancia independiente es más eficaz (web 3.6).
- Batch API para checks pre-merge: hasta 24 horas y sin SLA de latencia en un flujo bloqueante; usar tiempo real para bloqueantes y batch para análisis nocturnos o semanales (web 3.6; Guía PDF p. 152).
- Hallazgos repetidos: revisar solo el diff del nuevo commit o reanudar la primera sesión falla; se pasan los hallazgos previos a una ejecución nueva sobre todo el PR pidiendo solo lo nuevo o sin resolver (web 3.6; Guía PDF p. 151).
- Caps de coste e iteraciones: `timeout-minutes` (job runner), un modelo más pequeño (no limita totales) y `--permission-mode dontAsk` (permisos) son distractores; la respuesta es `--max-turns N` y `--max-budget-usd X` (Guía PDF p. 147-148).
- Claude solo comenta el diff y nunca lee archivos circundantes con `--system-prompt`: la corrección es `--append-system-prompt` (Guía PDF p. 148).
- Filtrar por confianza para quitar falsos positivos: Claude suele estar seguro en los casos que falla (Guía PDF p. 150, 152).
- Contenido fuera de la guía pero mencionado en la web: GitHub Actions y worktrees; tres lectores reportan cuatro o cinco preguntas sobre GitHub Actions (web 3.6).

## Ideas clave

- CLAUDE.md es advisory: lo que debe cumplirse siempre va en hooks o `permissions.deny`; el énfasis ("IMPORTANT", "YOU MUST") mejora la adherencia pero no la garantiza (Guía PDF p. 123; Guía PDF p. 131).
- "Never" apunta a `permissions.deny`, "automatically/always" a un hook PostToolUse, y "prefer/should" a CLAUDE.md (Guía PDF p. 133).
- Jerarquía de CLAUDE.md: user (`~/.claude/CLAUDE.md`, personal), project (`.claude/CLAUDE.md` o raíz, versionado) y directory (solo su directorio); una convención compartida en el nivel user no llega al resto del equipo (web 3.1; Slides PDF p. 658; Q41).
- Los `@` path imports (no existe la keyword `@import`) evitan duplicar contenido, pero no reducen el tamaño del contexto; para cargar según el archivo se usa `.claude/rules/` con `paths` (web 3.1; Guía PDF p. 122; Q42).
- `/memory` es el primer paso de diagnóstico cuando las convenciones se siguen de forma inconsistente: muestra qué está cargado, no carga nada (Guía PDF p. 123; web 3.1).
- Skills: un directorio con `SKILL.md` crea el slash command; `.claude/commands/` sigue funcionando; el alcance de proyecto (`.claude/`) se comparte por git y el de usuario (`~/.claude/`) es personal (web 3.2; Q4).
- `context: fork` aísla la salida verbosa de una skill en un sub-agent; `allowed-tools` y `argument-hint` no sirven para eso (Q43; web 3.2).
- Para un tipo de archivo repartido por muchos directorios (p. ej. tests), la respuesta es una rule en `.claude/rules/` con glob patterns, no un CLAUDE.md por directorio ni una skill que requiere invocación manual (web 3.3; Q6; Q44).
- Plan mode para tareas ambiguas, de gran alcance o con varios enfoques; direct execution para cambios acotados y conocidos; el híbrido es plan primero y execute después, y el Explore subagent mantiene la exploración verbosa fuera de la conversación principal (web 3.4; Guía PDF p. 137; Q5; Q45; Q46).
- Refinamiento iterativo: ejemplos concretos de entrada/salida si la prosa se interpreta de forma inconsistente, test-driven iteration para comportamiento bien definido e interview pattern en dominios desconocidos (web 3.5; Q47; Q48; Q52).
- En CI/CD, `-p` evita el cuelgue y `--output-format json` con `--json-schema` da salida parseable; `--max-turns` y `--max-budget-usd` limitan iteraciones y coste, y `--append-system-prompt` conserva las herramientas integradas (web 3.6; Q10; Q53; Guía PDF p. 147-148).
- La Batch API (50% de ahorro, hasta 24 horas sin SLA) sirve para análisis nocturnos o semanales, no para checks pre-merge bloqueantes; las revisiones se hacen en una sesión independiente y con los hallazgos previos como contexto (web 3.6; Guía PDF p. 152; Guía PDF p. 151).
