# Dominio 3 — Claude Code Configuration & Workflows — Estudio

## Tarjetas de repaso

**1.**
P: ¿Qué diferencia central marca la guía como el concepto más probado del Dominio 3?
R: CLAUDE.md es advisory (orientación, cumplimiento probabilístico); lo que debe cumplirse siempre requiere mecanismos deterministas como hooks y `permissions.deny`.

**2.**
P: ¿Cuáles son los tres niveles de la jerarquía de CLAUDE.md y dónde vive cada uno?
R: User (`~/.claude/CLAUDE.md`, personal, no versionado), project (`.claude/CLAUDE.md` o `CLAUDE.md` en la raíz, versionado) y directory (`CLAUDE.md` en un subdirectorio, solo para ese directorio).

**3.**
P: Si dos archivos CLAUDE.md entran en conflicto, ¿cuál gana?
R: Ninguno está garantizado. Se concatenan en el contexto; el orden de carga (el más cercano se lee al final) no es precedencia. Para cumplimiento estricto se usa settings.json o un hook.

**4.**
P: ¿Qué palabra clave del enunciado apunta a cada mecanismo: "never", "automatically/always" y "prefer/should"?
R: "Never" → `permissions.deny`; "automatically/always" → hook PostToolUse; "prefer/should" → CLAUDE.md.

**5.**
P: ¿Qué hace un hook PreToolUse con exit code 2 y en qué se diferencia de PostToolUse?
R: PreToolUse corre antes de la herramienta y con exit code 2 la bloquea (incluso con `--dangerously-skip-permissions`). PostToolUse corre tras la ejecución exitosa y sirve para post-procesado como el formato.

**6.**
P: ¿Cómo funciona la directiva de imports en CLAUDE.md y qué NO logra?
R: Es `@` seguido de una ruta (no existe la keyword `@import`); inserta el archivo en el CLAUDE.md. Evita duplicar contenido y mejora el mantenimiento, pero no reduce el tamaño del contexto.

**7.**
P: ¿Qué es `.claude/rules/` con frontmatter `paths`?
R: Archivos de reglas por tema cuyo frontmatter YAML lista glob patterns; la regla se carga solo al trabajar con archivos coincidentes, ahorrando tokens. Sin frontmatter, se carga en todas las sesiones. Son advisory.

**8.**
P: ¿Qué sobrevive a `/compact`?
R: El CLAUDE.md de la raíz se relee del disco y se inyecta completo. Los CLAUDE.md anidados y las rules con `paths` cargan bajo demanda; las instrucciones que solo existieron en el chat pueden perderse.

**9.**
P: ¿Para qué sirve `/memory` y cuál es su papel en el diagnóstico?
R: Muestra qué archivos de memoria (incluido CLAUDE.md) están cargados; no carga nada. Es el primer paso de diagnóstico más eficiente cuando las convenciones se siguen de forma inconsistente entre sesiones.

**10.**
P: ¿Cómo se crea un slash command con una skill y con un command?
R: Skill: directorio `.claude/skills/<nombre>/SKILL.md`. Command: archivo plano `.claude/commands/<nombre>.md`. Ambos crean `/<nombre>`; si coinciden, gana la skill. Un archivo plano dentro de `.claude/skills/` no crea ningún comando.

**11.**
P: ¿Qué diferencia hay entre alcance de proyecto y de usuario para commands y skills?
R: `.claude/` (proyecto) está versionado y se comparte por git; `~/.claude/` (usuario) es personal, no versionado ni compartido.

**12.**
P: ¿Cuándo se carga cada uno: CLAUDE.md, rules y skills?
R: CLAUDE.md en cada sesión; rules de forma condicional según rutas de archivos; skills bajo demanda cuando se invocan.

**13.**
P: ¿Qué hace `context: fork` en el frontmatter de una skill?
R: Ejecuta la skill en un contexto de sub-agent aislado, de modo que la salida verbosa no contamina la conversación principal. `allowed-tools` y `argument-hint` no sirven para ese fin.

**14.**
P: ¿Qué papel cumple `description` en una skill?
R: Claude la lee para decidir si la skill aplica; las descripciones están siempre en contexto y el cuerpo solo se carga al invocar. Una descripción fuerte dice qué hace y cuándo, con frases disparadoras.

**15.**
P: ¿Cuándo usar path-specific rules en lugar de un CLAUDE.md de directorio?
R: Cuando un tipo de archivo (p. ej. tests) está repartido por muchos directorios: un solo archivo de regla con glob patterns (`**/*.test.tsx`) evita copias en cada directorio. El CLAUDE.md de directorio sirve si las convenciones están contenidas en una sola carpeta.

**16.**
P: ¿Qué criterio decide entre plan mode y direct execution?
R: La ambigüedad, no la dificultad. Plan mode para cambios de gran alcance, varios enfoques válidos o decisiones de arquitectura; direct execution para cambios acotados con qué, dónde y cómo conocidos.

**17.**
P: ¿Cómo se activa plan mode y qué NO lo activa?
R: Con `claude --permission-mode plan`, Shift+Tab durante la sesión o prefijando un prompt con `/plan`. Escribir "in plan mode" en el cuerpo del prompt no hace nada.

**18.**
P: ¿Qué es el enfoque híbrido y para qué sirve el Explore subagent?
R: Plan mode para investigar y luego direct execution para implementar. El Explore subagent aísla la exploración verbosa y devuelve un resumen a la conversación principal, dejando libre la ventana de contexto.

**19.**
P: ¿Cuáles son las cinco técnicas de refinamiento iterativo y cuándo aplicar cada una?
R: Ejemplos concretos de entrada/salida (la prosa se interpreta de forma inconsistente), test-driven iteration (comportamiento bien definido, transformaciones complejas), interview pattern (dominio desconocido), batch feedback (arreglos que interactúan) y sequential feedback (problemas independientes).

**20.**
P: ¿Qué es el TBD marker pattern?
R: Una especificación con los requisitos conocidos y marcadores "TBD" en las áreas inciertas, para que Claude proponga una solución a cada TBD al implementar. Ayuda a sacar a la luz "unknown unknowns".

**21.**
P: ¿Qué hace `-p` en CI y qué flags dan salida estructurada?
R: `-p` (`--print`) ejecuta Claude Code de forma no interactiva y termina; sin él el job se cuelga. `--output-format json` da un envelope JSON y `--json-schema` valida la salida contra un esquema (resultado en `structured_output`).

**22.**
P: ¿Qué diferencia hay entre `--system-prompt` y `--append-system-prompt`, y qué flags limitan iteraciones y coste?
R: `--system-prompt` reemplaza el prompt por defecto (pierde la guía de herramientas); `--append-system-prompt` le añade texto y conserva las herramientas integradas. `--max-turns` limita iteraciones y `--max-budget-usd` el coste.

**23.**
P: ¿Cuándo usar la Batch API frente a la API en tiempo real en CI?
R: Batch API (50% de ahorro, hasta 24 horas sin SLA de latencia) para análisis nocturnos o semanales; API en tiempo real para checks pre-merge bloqueantes.

**24.**
P: ¿Cómo evitar hallazgos repetidos en revisiones automáticas en cada push y sesgo de autorrevisión?
R: Pasar los hallazgos previos en el contexto de una ejecución nueva y pedir solo problemas nuevos o sin resolver; y revisar con una llamada independiente, sin el contexto de razonamiento de la sesión que generó el código.

## Preguntas de autoevaluación

**1.** Un nuevo miembro del equipo obtiene resultados inconsistentes porque las convenciones estaban en el `~/.claude/CLAUDE.md` del primer desarrollador. ¿Cuál es la solución?
R: Mover las convenciones al nivel de proyecto (`.claude/CLAUDE.md` o `CLAUDE.md` en la raíz) y hacer commit; el nivel user no está versionado y no llega a quien clona el repo. (Tarea 3.1 — Jerarquía de tres niveles; Trampas del examen; Q41)

**2.** Una regla dice "Claude must never modify files in db/migrations/". ¿Dónde va y por qué no en CLAUDE.md?
R: En `permissions.deny` (`Edit(./db/migrations/**)`), un bloqueo declarativo y determinista. CLAUDE.md es advisory y el énfasis no garantiza cumplimiento. (Tarea 3.1 — CLAUDE.md vs settings.json / hooks / permissions)

**3.** Las convenciones se siguen de forma inconsistente entre sesiones. ¿Cuál es el primer paso de diagnóstico más eficiente?
R: Ejecutar `/memory` para comprobar si el archivo se carga (ubicación, typo, alcance). Si carga, el problema es la naturaleza advisory y puede hacer falta un hook. (Tarea 3.1 — Diagnóstico: /memory y /context)

**4.** Un CLAUDE.md de 400+ líneas aplica reglas a archivos equivocados. ¿Qué solución propone el apunte y por qué falla `@import` incondicional?
R: Partirlo en `.claude/rules/` con frontmatter `paths`. El import incondicional resuelve el mantenimiento pero todo carga siempre, así que no corrige las convenciones aplicadas donde no corresponde. (Tarea 3.1 — Trampas del examen; Q42)

**5.** Quieres un `/review` compartido por el equipo y un `/brainstorm` personal con salida verbosa. ¿Cómo los configuras?
R: `/review` en `.claude/commands/review.md` (versionado) y `/brainstorm` como `SKILL.md` en `~/.claude/skills/` con `context: fork`. (Tarea 3.2 — Alcance; Trampas del examen; Q4, Q43)

**6.** Una skill de scaffolding produce cientos de líneas intermedias que contaminan la conversación. ¿Qué frontmatter la soluciona?
R: `context: fork`. Mover la skill a `.claude/commands/` no cambia el aislamiento, `allowed-tools: []` impide usar herramientas y `argument-hint` es para parámetros de entrada. (Tarea 3.2 — Frontmatter: context: fork; Q43)

**7.** Los tests viven junto al código en más de 50 directorios y deben cargarse automáticamente solo al editar un test. ¿Qué mecanismo usas?
R: Una rule en `.claude/rules/` con `paths: ["**/*.test.tsx", "**/*.test.ts"]`. Un CLAUDE.md por directorio exige 50+ copias, el raíz con secciones depende de la inferencia de Claude y las skills requieren invocación manual. (Tarea 3.3 — Path-specific rules frente a CLAUDE.md de directorio; Trampas del examen; Q6, Q44)

**8.** ¿Qué modo eliges para reestructurar un monolito en microservicios, para añadir un null check y para migrar una librería en 45 archivos?
R: Plan mode para el monolito (complejidad ya declarada), direct execution para el null check, y para la migración plan mode primero y luego direct execution (híbrido). (Tarea 3.4 — Criterio de decisión; Enfoque híbrido; Q5, Q45)

**9.** Una exploración previa a una migración llena el contexto de resultados de herramientas. ¿Qué técnica usas?
R: El Explore subagent, que explora en aislamiento y devuelve un resumen. `/compact` tras cada tool call es engorroso y pierde detalle; restringir la lectura deja el análisis incompleto. (Tarea 3.4 — Explore subagent; Q46)

**10.** La descripción en prosa de una transformación de formato se interpreta distinto cada vez. ¿Qué haces?
R: Dar 2-3 ejemplos concretos de entrada/salida (incluido el caso límite principal) y verificar con un caso nuevo. Más prosa o mayúsculas no resuelven la ambigüedad. (Tarea 3.5 — Ejemplos concretos de entrada/salida; Q47)

**11.** ¿Cuándo envías el feedback en un solo mensaje y cuándo uno por uno?
R: Según el banco y la web, en un solo mensaje cuando los arreglos interactúan y secuencialmente cuando son independientes. La guía discrepa para problemas que interactúan (recomienda arreglos incrementales con prueba tras cada paso); el apunte no resuelve esa contradicción. (Tarea 3.5 — Batch feedback vs. sequential feedback; Incremental problem solving; Q49, Q51)

**12.** Un job de CI se cuelga esperando entrada. ¿Cuál es la causa y la solución?
R: Falta `-p` (`--print`); un pipeline no tiene teclado. `CLAUDE_HEADLESS=true` y `--batch` no existen, y redirigir stdin desde `/dev/null` es un workaround que no resuelve la sintaxis de Claude Code. (Tarea 3.6 — Modo no interactivo con claude -p; Q10)

**13.** Se necesitan comentarios inline en un PR a partir de la salida de Claude. ¿Qué configuras?
R: `--output-format json` con `--json-schema` (campos `file`, `line`, `comment`). Parsear texto libre con regex se rompe porque el formato deriva entre ejecuciones. (Tarea 3.6 — Salida estructurada para CI; Q53)

**14.** Los tests generados en CI duplican los existentes. ¿Qué lo corrige?
R: Documentar en CLAUDE.md los estándares de testing y los fixtures disponibles, e indicar que se revisen los tests existentes antes de sugerir nuevos. `-p`, `--output-format json` y un script de post-procesado no tratan la causa. (Tarea 3.6 — CLAUDE.md como contexto para CI; Q50)

## Checklist

### Tarea 3.1 — CLAUDE.md: jerarquía, alcance y organización modular
- [ ] Confirmar a quién afecta la instrucción: solo a ti → `~/.claude/CLAUDE.md`; al equipo → `.claude/CLAUDE.md` o raíz, con commit.
- [ ] Usar un CLAUDE.md de subdirectorio solo para convenciones de un único directorio o paquete.
- [ ] Mover a `settings.json`/hooks lo que debe cumplirse siempre: `permissions.deny` para "never", PostToolUse para "automatically/always".
- [ ] Dejar en CLAUDE.md solo preferencias advisory ("prefer/should") y evitar contradicciones entre raíz y subdirectorios.
- [ ] Evitar un CLAUDE.md raíz de 300+ líneas con información deducible del código.
- [ ] Usar `@ruta` (sin keyword `@import`) para reutilizar contenido, sabiendo que no reduce el contexto.
- [ ] Colocar preferencias locales temporales en `CLAUDE.local.md` y no commitearlo.
- [ ] Ante comportamiento inconsistente, ejecutar `/memory` antes de añadir ejemplos o reglas.

### Tarea 3.2 — Slash commands y skills
- [ ] Crear skills como `.claude/skills/<nombre>/SKILL.md` (no archivos planos en `.claude/skills/`).
- [ ] Colocar los commands de equipo en `.claude/` (versionado) y los personales en `~/.claude/`.
- [ ] Añadir `context: fork` a las skills de salida verbosa.
- [ ] Escribir una `description` que diga qué hace y cuándo, con frases disparadoras.
- [ ] Reservar CLAUDE.md o rules para guía siempre activa y las skills para flujos específicos bajo demanda.
- [ ] En el examen, responder con la redacción de la guía sobre `allowed-tools` y `argument-hint`.

### Tarea 3.3 — Reglas por ruta
- [ ] Crear el archivo en `.claude/rules/` con frontmatter `paths` y glob patterns (`**/*.test.tsx`, `terraform/**/*`).
- [ ] Usar `**` para cubrir un tipo de archivo repartido por muchos directorios.
- [ ] Evitar patrones superpuestos entre archivos de reglas y no usar rules para instrucciones globales.
- [ ] Comprobar la carga con `/context` y con el aviso "Loaded" al leer un archivo coincidente.
- [ ] Recordar que las rules son advisory, igual que CLAUDE.md.

### Tarea 3.4 — Plan mode vs direct execution
- [ ] Valorar la ambigüedad de la tarea, no su dificultad.
- [ ] Elegir plan mode si hay gran alcance, varios enfoques válidos, decisiones de arquitectura o un módulo desconocido.
- [ ] Elegir direct execution para cambios acotados con qué, dónde y cómo conocidos.
- [ ] Activar plan mode con `--permission-mode plan`, Shift+Tab o `/plan`, no escribiéndolo en el prompt.
- [ ] En migraciones grandes, planificar primero y ejecutar después; delegar la exploración verbosa al Explore subagent.

### Tarea 3.5 — Refinamiento iterativo
- [ ] Dar feedback concreto (resultados de tests, errores, pares entrada/salida), no vago ni subjetivo.
- [ ] Pasar a 2-3 ejemplos de entrada/salida cuando la prosa se interpreta de forma inconsistente, y probar un caso nuevo.
- [ ] Escribir primero los tests y compartir los fallos cuando el comportamiento está bien definido.
- [ ] Usar el interview pattern o marcadores TBD en dominios desconocidos antes de implementar.
- [ ] Agrupar el feedback si los arreglos interactúan y enviarlo por separado si son independientes; tener presente la discrepancia con la guía.
- [ ] Usar `@` references para contexto de una tarea puntual en lugar de CLAUDE.md.

### Tarea 3.6 — Claude Code en CI/CD
- [ ] Ejecutar siempre con `-p` en pipelines.
- [ ] Usar `--output-format json` con `--json-schema` cuando otro sistema consume la salida y leer `structured_output`.
- [ ] Usar `--append-system-prompt` (no `--system-prompt`) si Claude debe leer archivos circundantes.
- [ ] Fijar `--max-turns` y `--max-budget-usd` para limitar iteraciones y coste.
- [ ] Documentar en CLAUDE.md estándares de testing, fixtures y criterios de revisión; no usar `--bare` si la revisión los necesita.
- [ ] Revisar en una sesión independiente de la que generó el código.
- [ ] Pasar los hallazgos previos y pedir solo problemas nuevos o sin resolver.
- [ ] Usar la API en tiempo real para checks pre-merge y la Batch API para análisis nocturnos o semanales.
- [ ] Guardar las credenciales en secrets, nunca literales en el archivo.
