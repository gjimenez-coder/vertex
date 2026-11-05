# Claude Certified Architect – Foundations (CCA-F) — Anthropic (guía de examen, 2026)

## Dominio 4 — Prompt Engineering & Structured Output (Ingeniería de prompts y salida estructurada)

> Nota de extracción: este apunte combina cinco fuentes: la guía en PDF «Tutorials Dojo Study Guide and Cheat Sheets – Claude Certified Architect Foundations (CCA-F)», las slides en PDF del curso en video (Tutorials Dojo, junio 2026), el banco de 77 preguntas de práctica «Claude Certified Architect. Foundations: Practice Exam» y las lecciones web de claudecertificationguide.com (sitio independiente de terceros, no afiliado a Anthropic). Citas: `(Guía PDF p. N)` y `(Slides PDF p. N)` usan la página del PDF; `(web N.M)` remite a la lección N.M de la web; `(QN)` remite a la pregunta N del banco. Si las fuentes se contradicen, prevalecen la guía y el banco sobre la web. Las slides tienen muchas páginas que son solo imagen y no se pudieron leer, por lo que su cobertura es parcial. Discrepancia entre fuentes sin resolver: el banco y la guía llaman al examen «CCA-F» y el banco indica 77 preguntas de práctica y una nota mínima de 720 (escala 100-1.000); la web lo llama «CCAR-F» e indica 60 preguntas en 120 minutos, aprobado con 720/1.000 y credencial válida 12 meses. No se decide cuál es la correcta.

## Lo que necesitas saber

El Dominio 4 (Prompt Engineering and Structured Output) pesa el 20% del examen y trata de cómo conseguir salidas precisas, consistentes y verificables de Claude. Cubre seis tareas: criterios explícitos para mejorar la precisión y reducir falsos positivos (4.1), few-shot prompting (4.2), salida estructurada con tool use y JSON schemas (4.3), bucles de validación, reintento y feedback (4.4), estrategias de procesamiento por lotes (4.5) y arquitecturas de revisión multi-instancia y multi-pasada (4.6).

Las tareas se encadenan como un pipeline. Primero se define qué reportar y qué omitir con criterios categóricos, no con instrucciones vagas como "be conservative" ni con filtros de confianza (4.1; Q55). Después se enseña el formato y el juicio con 2 a 4 ejemplos que incluyen el razonamiento (4.2; Slides PDF p. 1101). Luego se fuerza la forma de la salida con tool use y JSON schema, eligiendo bien `tool_choice` y los campos required, optional y nullable (4.3). Como el schema solo garantiza la sintaxis y no la semántica, se añade un validation loop con retry-with-error-feedback, que solo funciona con errores resolubles y tiene un límite de reintentos (4.4; Guía PDF p. 88, 199, 206). Para el volumen, la Message Batches API da un 50% de ahorro a cambio de una ventana de hasta 24 horas sin SLA de latencia, y no sirve para flujos bloqueantes (4.5; Guía PDF p. 211; web 4.5). Por último, la revisión de calidad exige instancias independientes y pasadas separadas, porque la self-review conserva el razonamiento de la generación y una sola pasada diluye la atención (4.6; Guía PDF p. 159; web 4.6).

Sales sabiendo elegir la herramienta correcta para cada síntoma: criterios explícitos para falsos positivos, few-shot para formato y juicios ambiguos, tool use con schema para JSON malformado, validación y reintento con el error específico para errores semánticos resolubles, revisión humana o null para datos ausentes, batch solo para trabajo tolerante a la latencia y revisión independiente multi-pasada para defectos sutiles. También sales sabiendo reconocer los distractores típicos del banco (Q11, Q12, Q55 a Q68).

Tareas con prioridad de estudio: 4.1 (patrones de precisión en extracción), 4.3 (método de salida estructurada), 4.4 (feedback loops con metadata de errores) y 4.5 (Messages API vs Message Batches API).

## Tarea 4.1 — Design prompts with explicit criteria to improve precision and reduce false positives (Diseñar prompts con criterios explícitos para mejorar la precisión y reducir falsos positivos)

> Prioridad de estudio: Patrones de precisión en extracción (regresión: 75% -> 50%)

### Criterios explícitos frente a instrucciones vagas

**Concepto:** Los criterios explícitos son reglas concretas que dicen exactamente qué merece reportarse y qué no, convirtiendo una instrucción difusa en un límite comprobable (Guía PDF p. 180). Las instrucciones vagas ("be conservative", "only report high-confidence findings") no definen qué marcar ni qué es un falso positivo, es decir, un hallazgo erróneo (web 4.1). El modelo las sigue con su propio juicio, y ese juicio no es estable (Guía PDF p. 180).

**Ejemplos de uso (3, cortos):**
1. "Flag a comment only when claimed behavior directly contradicts what the code actually does", sin marcar comentarios incompletos o que describan intención (Slides PDF p. 1084).
2. Reportar bugs, vulnerabilidades de seguridad y data races; omitir estilo menor, patrones de nombres locales y preferencias subjetivas (Slides PDF p. 1086).
3. Sustituir "Review this code and flag anything important" por "Flag only (1) bugs that change behavior and (2) security issues. Do not flag style or formatting", indicando además la forma de cada hallazgo: location, issue, severity y suggested fix (Guía PDF p. 177-179).

**Qué NO hacer:**
- Usar "be conservative" como arreglo de precisión: no define el límite y no mejora la precisión (Guía PDF p. 151; web 4.1).
- Añadir calificativos como "carefully" o "thoroughly": suenan tranquilizadores pero no cambian la prueba que aplica el modelo (Guía PDF p. 176).
- Pedir "use good judgment" para decidir qué es un "magic number": es justo la instrucción vaga que causa el problema (Q56).

**Posible confusión con otros conceptos:**
- Criterios explícitos — definen qué reportar y qué omitir ("report bugs, skip local patterns") (Guía PDF p. 150).
- Infraestructura adicional — se confunde con los criterios, pero antes de añadir complejidad el cambio de prompt más eficaz es añadir criterios explícitos (Guía PDF p. 150, 180).

Los criterios se estructuran en categorías, skips y severidad: cada categoría con una definición de una frase y un ejemplo de código, una lista de qué omitir (p. ej., usar "data" en lugar de "responseData" es un skip) y cada nivel de severidad con su definición y ejemplo (Slides PDF p. 1091). Un criterio explícito evita generar hallazgos no deseados en lugar de filtrarlos después (Guía PDF p. 150).

### Filtrado por confianza (confidence-based filtering)

**Concepto:** Es filtrar hallazgos por la confianza que el propio modelo declara. La confianza autorreportada del LLM está mal calibrada: el modelo suele estar seguro de hallazgos erróneos y dudar de los correctos (web 4.1). Pedir más confianza no elimina los casos equivocados: suprime hallazgos correctos pero inciertos y conserva los erróneos pero seguros (Guía PDF p. 150).

**Ejemplos de uso (3, cortos):**
1. Orden correcto: primero criterios explícitos, después enrutar a revisión humana los hallazgos de baja confianza (Task Statement 4.6) (web 4.1).
2. Si un prompt dice "only report high-confidence issues" y se escapan bugs reales, quitar el filtrado supresor y pedir todos los hallazgos con un nivel de confianza y una etiqueta de severidad, dejando el filtrado a un paso posterior (Guía PDF p. 150).
3. Incluir el razonamiento y la evaluación de confianza en línea con cada hallazgo para que el desarrollador haga triage de un vistazo, sin filtrar antes de su revisión (Guía PDF p. 150-151).

**Qué NO hacer:**
- Elegir "only report high-confidence findings" como mejora del prompt: es la opción tentadora que el examen usa como distractor (web 4.1; Q55).
- Descartar hallazgos con un umbral de post-procesado, p. ej. confianza propia por debajo de 80% (Q55).
- Saltarse los criterios explícitos y confiar solo en la confianza: los criterios van primero, el enrutamiento por confianza después (web 4.1).

**Posible confusión con otros conceptos:**
- Criterios explícitos — definen qué cuenta como hallazgo válido (Guía PDF p. 180).
- Enrutamiento por confianza — dirige hallazgos inciertos a revisión humana, pero no sustituye a los criterios (web 4.1).

### Falsos positivos y confianza del usuario

**Concepto:** Una categoría que dispara a menudo sobre no-problemas envenena la confianza en toda la herramienta; los desarrolladores aprenden a ignorar la categoría ruidosa y acaban ignorando también las precisas (Guía PDF p. 181). La confianza es holística: una categoría ruidosa daña la percepción de todo el sistema (Slides PDF p. 1085).

**Ejemplos de uso (3, cortos):**
1. Con 40% de falsos positivos en "documentation mismatch", los desarrolladores ignoran todas las categorías; la solución es desactivar esa categoría temporalmente mientras se refinan sus prompts con criterios explícitos y ejemplos de código (web 4.1).
2. Mientras se mejora el prompt, la categoría se desactiva ("Disable temporarily") y solo se reactiva cuando mejora la precisión, es decir, la proporción de sus hallazgos que son correctos (Slides PDF p. 1086; web 4.1).
3. Ejercicio: desactivar toda categoría por encima de 25% de falsos positivos y documentar los refinamientos de criterios y un plan de reactivación (web 4.1).

**Qué NO hacer:**
- Mantener todas las categorías activas mientras se itera sobre las de alto falso positivo (web 4.1).
- Dejar corriendo una categoría ruidosa: erosiona la confianza en los hallazgos precisos (Guía PDF p. 181).
- Degradar la categoría a notas informativas colapsables con el mismo prompt: los desarrolladores desconfían de cualquier hallazgo erróneo visible, incluso colapsado (web 4.1).

### Calibración de severidad con ejemplos de código

**Concepto:** Un nivel de severidad (critical, major, minor) es un escalón con nombre y una condición declarada (Guía PDF p. 180). Para definirlo se necesitan ejemplos concretos de código, no descripciones en prosa: con ellos el modelo clasifica de forma consistente entre invocaciones (web 4.1). Sin ejemplos, el mismo patrón recibe "critical" en un PR y "medium" en otro (Guía PDF p. 151).

**Ejemplos de uso (3, cortos):**
1. Critical: SQL injection o entrada de usuario sin sanear concatenada en una query; en la web, `query = f"SELECT * FROM users WHERE id = {user_input}"` (Guía PDF p. 151; web 4.1).
2. Major: bug de lógica que cambia la salida, p. ej. off-by-one en el límite de un bucle (Guía PDF p. 151).
3. Minor: falta de null check sobre datos opcionales donde el comportamiento por defecto es seguro; y "Skip": estilo de nombres, orden de imports, formato y patrones documentados como aceptados en CLAUDE.md (Guía PDF p. 151).

```
Critical — Unsanitised user input in SQL query:
query = f"SELECT * FROM users WHERE id = {user_input}"
```

**Qué NO hacer:**
- Describir niveles solo en prosa ("Critical: issues that could cause system failures or data loss"): obliga al modelo a interpretar (web 4.1).
- Usar tablas de severidad en CLAUDE.md (son consultivas y siguen variando), severidad relativa dentro de un PR (inconsistente entre PRs) o pedir razonamiento de severidad para calibrar a mano (no resuelve la inconsistencia raíz) (Guía PDF p. 151).
- Definir niveles sin ejemplos: la línea sigue siendo subjetiva (Guía PDF p. 181).

### Patrones aceptados del equipo (CLAUDE.md)

**Concepto:** Cuando la revisión marca de forma constante patrones que el equipo usa a propósito, la solución es documentarlos en el CLAUDE.md del proyecto, que da contexto persistente en cada revisión (Guía PDF p. 149). No son bugs sino decisiones arquitectónicas deliberadas; sin contexto, Claude los marca porque parecen anti-patrones (Guía PDF p. 149).

**Ejemplos de uso (3, cortos):**
1. Force-unwrapping de optionals en archivos de test (Guía PDF p. 149).
2. Clases coordinator grandes que siguen la arquitectura del equipo (Guía PDF p. 149).
3. Importar módulos mantenidos internamente marcados como deprecated en el SDK público (Guía PDF p. 149).

**Posible confusión con otros conceptos:**
- Lista de patrones aceptados en CLAUDE.md — evita hallazgos sobre patrones intencionales (Guía PDF p. 149).
- Tabla de severidad en CLAUDE.md — es consultiva y no fija la severidad de forma consistente (Guía PDF p. 151).

### Metadatos de salida y contexto previo

**Concepto:** Campos y contexto añadidos al prompt para analizar o reducir ruido sin filtrar antes de la revisión humana. El campo `detected_pattern` registra el constructo de código específico que disparó cada hallazgo (Guía PDF p. 150).

**Ejemplos de uso (3, cortos):**
1. Si los desarrolladores descartan 35% de los hallazgos, añadir `detected_pattern` (p. ej. "single-letter loop variable", "unused import", "missing null check") para analizar tasas de descarte por patrón y ajustar los prompts; es más accionable que el análisis por categoría (demasiado amplio), las puntuaciones de confianza (mal calibradas) o descripciones ampliadas (Guía PDF p. 150).
2. Cuando el cuello de botella es el tiempo de investigación, exigir razonamiento y confianza en línea con cada hallazgo (Guía PDF p. 150-151).
3. Al re-ejecutar tras nuevos commits, incluir los hallazgos de la revisión previa y pedir solo issues nuevos o aún sin resolver (Guía PDF p. 151).

**Qué NO hacer:**
- Resolver duplicados con filtros de post-procesado (coincidencia burda de ruta/descripción), limitar el alcance a archivos recién modificados (pierde regresiones) o revisar solo en la creación del PR y antes del merge (omite feedback intermedio) (Guía PDF p. 151).

### Recall, enfoque de prompts y revisión agéntica

**Concepto:** El reto de la revisión automática es equilibrar la precisión (evitar falsos positivos) con el recall (detectar bugs reales); cada decisión de diseño del prompt desplaza ese equilibrio (Guía PDF p. 148). Para bugs que se escapan (bajo recall), lo más eficaz son ejemplos few-shot de las categorías de bug concretas (Guía PDF p. 149-150).

**Ejemplos de uso (3, cortos):**
1. Mejorar recall manteniendo precisión: few-shot de race conditions, null dereferences y huecos de manejo de errores; mejora categorías específicas sin el sobreconteo amplio de las instrucciones generales (Guía PDF p. 149-150).
2. Si añadir ejemplos para una categoría perjudica el recall de otra (business logic 34% a 41% hace caer API design de 82% a 68%), dividir la revisión en prompts enfocados, cada uno con sus ejemplos, y consolidar hallazgos antes de publicar (Guía PDF p. 151-152).
3. Para bugs entre archivos (un PR renombra parámetros pero los callers en archivos sin cambios usan los nombres viejos), rediseñar la revisión como tarea agéntica con límite de turnos y herramientas para leer y buscar, usando `--append-system-prompt` (Guía PDF p. 152).

**Qué NO hacer:**
- Pedir "be more thorough": no dice qué buscar; tampoco añadir chain-of-thought (ayuda al razonamiento, no al reconocimiento de patrones) ni contexto de archivos no relacionados (añade ruido) (Guía PDF p. 149).
- Mejorar recall haciendo que Claude marque todo: destruye la precisión (Guía PDF p. 150).
- Lanzar una única revisión todo-en-uno sobre 14+ archivos: la atención se dispersa y los hallazgos se vuelven inconsistentes (Guía PDF p. 152).
- Ante JSON truncado de `report_findings` por `max_tokens`, subir `max_tokens`, reintentar con "only critical findings" o pasar a markdown; lo robusto es dividir en varias llamadas por subconjuntos de archivos y fusionar los arrays de hallazgos (Guía PDF p. 152).

**Posible confusión con otros conceptos:**
- `--system-prompt` — reemplaza el prompt por defecto y quita la guía de herramientas integrada (Guía PDF p. 148).
- `--append-system-prompt` — añade al prompt por defecto y conserva las capacidades y herramientas integradas (Guía PDF p. 148).

### Arreglo a nivel de prompt frente a arreglo arquitectónico

**Concepto:** Un arreglo de prompt reduce la ambigüedad (claridad, consistencia, formato, casos ambiguos) y es rápido, barato y sin infraestructura nueva; un arreglo arquitectónico (code gate, schema validator, paso obligatorio del pipeline) elimina la discreción del modelo y siempre se cumple (Guía PDF p. 178). La pregunta decisiva: ¿puede permitirse que esto falle alguna vez? Si sí, arregla el prompt; si no, aplícalo estructuralmente (Guía PDF p. 178).

**Ejemplos de uso (3, cortos):**
1. Salida inconsistente porque el modelo adivina alcance, formato o criterios: un prompt más claro (Guía PDF p. 178).
2. Regla que debe cumplirse siempre (verificar identidad antes de un reembolso): mecanismo determinista, no una instrucción más firme (Guía PDF p. 178).
3. Sustituir "Flag the important issues" por "Flag issues that would cause data loss or service unavailability" (Guía PDF p. 177).

**Qué NO hacer:**
- Usar un prompt como garantía de una regla que siempre debe cumplirse (Guía PDF p. 179).
- Añadir infraestructura cuando el problema era una instrucción poco clara (Guía PDF p. 179).
- Decir "always do this" con más fuerza: no convierte una probabilidad en garantía (Guía PDF p. 178).

### Trampas del examen

- "Be conservative" / "only report high-confidence findings" como mejora válida: falla porque el modelo no tiene una interpretación accionable de "conservative"; lo correcto son criterios categóricos específicos de qué marcar y qué omitir (web 4.1). Q55 lo muestra: tras añadir "only report high-confidence findings" no hubo efecto medible, porque la instrucción no define qué cuenta como positivo (Q55). En el escenario práctico de la web, la opción D ("only report high-confidence documentation issues") es el mismo error (web 4.1).
- Umbral de confianza como arreglo de falsos positivos (Q55, opción D: descartar hallazgos con confianza propia inferior a 80%): falla porque la confianza autorreportada del LLM está mal calibrada (Q55; web 4.1; Guía PDF p. 181). El enrutamiento por confianza solo sirve después de definir los criterios (web 4.1).
- Mantener todas las categorías activas mientras se itera: el ruido en una categoría destruye la confianza en todas; lo correcto es desactivar temporalmente la problemática y refinarla con criterios y ejemplos de código (Q55; web 4.1).
- Sustituir la revisión con IA por una herramienta de análisis estático "con cero falsos positivos": abandona la revisión con IA en lugar de arreglarla (Q55).
- Subir a un modelo de mayor tamaño: es poco probable que cambie los falsos positivos cuando la causa raíz son criterios imprecisos (Q55).
- Segunda pasada del modelo para verificar cada hallazgo (opción B de la web): descartada en el escenario porque el presupuesto no permite una llamada extra por revisión; degradar a notas colapsables (opción C) tampoco sirve porque los desarrolladores desconfían de cualquier hallazgo erróneo visible, y esa opción conserva el prompt actual (web 4.1).
- "Use good judgment about whether numbers are truly magic numbers" (Q56, A): es la instrucción vaga que origina el problema. Un campo severity para omitir "low" (Q56, C) no resuelve el problema de definición, y una lista de valores permitidos (Q56, D) es incompleta, frágil y no generaliza. Correcto: criterios explícitos (p. ej., literales numéricos en cálculos de lógica de negocio sin comentario ni constante con nombre; excluir códigos HTTP, tamaños de buffer estándar y valores documentados) (Q56).
- Feedback de documentación inconsistente (Q57): "apply documentation standards consistently and carefully" repite el tipo de instrucción general que causa el problema (Q57, A); tres instancias paralelas con acuerdo de dos de tres añaden sobrecarga y suprimen feedback legítimo (Q57, C); alternar una preocupación por ejecución separa temas pero no define qué es documentación adecuada (Q57, D). Correcto: definir qué se exige, para qué funciones y con qué nivel de detalle (API pública con docstring de una frase, descripción de parámetros y valor de retorno; funciones privadas excluidas) (Q57).
- Severidad en prosa o con tablas en CLAUDE.md, severidad relativa en el PR o razonamiento de severidad para calibrar a mano: no resuelven la inconsistencia; lo que calibra son ejemplos de código por nivel (web 4.1; Guía PDF p. 151).
- Confundir `--system-prompt` con `--append-system-prompt`: si Claude solo comenta el diff y nunca lee archivos circundantes con `--system-prompt`, el arreglo es pasar a `--append-system-prompt` (Guía PDF p. 148).
- Confundir `--permission-mode dontAsk` (controla permisos) con `--max-turns` (controla iteraciones), y usar `timeout-minutes` del paso de GitHub Actions en lugar de `--max-turns`/`--max-budget-usd` (Guía PDF p. 148).
- Marcar como "falso positivo del prompt" patrones intencionales del equipo en lugar de documentarlos en CLAUDE.md (Guía PDF p. 149).
- Tratar un prompt como garantía de una regla obligatoria, o añadir infraestructura donde bastaba una instrucción clara (Guía PDF p. 178-179).

- **Contradicción entre fuentes:** la web da como ejemplo de severidad "Minor — Inconsistent variable naming" (`userName` vs `user_name`), mientras que la guía incluye el estilo de nombres, el orden de imports y el formato en "Skip" y las diapositivas ponen los patrones de nombres locales en "Skip" (web 4.1; Guía PDF p. 151; Slides PDF p. 1086). Prevalecen la guía y las diapositivas: esos hallazgos se omiten. Además, la guía sitúa la sección de revisión de código dentro del Dominio 3 (Guía PDF p. 148), mientras que las diapositivas y la web tratan la Tarea 4.1 en el Dominio 4 (Slides PDF p. 1081; web 4.1); la Tarea 4.1 se mantiene en el Dominio 4.

## Tarea 4.2 — Apply few-shot prompting to improve output consistency and quality (Aplicar few-shot prompting para mejorar la consistencia y la calidad de la salida)

### Few-shot prompting y cuándo usarlo

**Concepto:** Few-shot prompting consiste en incluir en el prompt unos pocos ejemplos resueltos (entrada y salida deseada, idealmente con el razonamiento) antes de pedir el caso nuevo (web 4.2; Guía PDF p. 181). Una regla escrita describe lo que quieres, pero un ejemplo lo muestra (Guía PDF p. 181). Es la técnica más eficaz para obtener una salida consistente y bien formateada; más instrucciones, umbrales de confianza o ajustes de temperatura hacen menos (web 4.2).

**Ejemplos de uso (3, cortos):**
1. Formato inconsistente pese a instrucciones detalladas (lista, luego tabla, luego prosa): mostrar ejemplos del formato exacto (web 4.2; Q58).
2. Juicios inconsistentes en casos ambiguos, por ejemplo "check my order" enrutado a herramientas distintas según la redacción: ejemplos con el juicio correcto y su razonamiento (web 4.2).
3. Extracción que devuelve campos vacíos o null aunque el documento contiene el dato (p. ej. "twelve kilos of hake at nine pounds a kilo" en una frase): ejemplos de extracción desde estructuras variadas (web 4.2; Q60).

**Qué NO hacer:**
- No añadir "más instrucciones detalladas" cuando el formato es inconsistente: las instrucciones vuelven a describir el formato, mientras que los ejemplos muestran el formato objetivo (web 4.2; Q58).
- No usar umbrales de confianza para arreglar juicios inconsistentes: están mal calibrados y no atacan la causa raíz (web 4.2; Guía PDF p. 181).
- No usar few-shot para corregir un mal enrutamiento de herramientas cuya causa real es una descripción de herramienta débil (Guía PDF p. 182, p. 183).

**Posible confusión con otros conceptos:**
- Zero-shot — sirve para tareas simples y bien definidas, con bajo coste de tokens; esperar de él un formato consistente en tareas complejas es la trampa típica (Guía PDF p. 182).
- Few-shot — sirve para formato consistente, casos ambiguos y salida estructurada (Guía PDF p. 182).

La pregunta que decide: ¿es fácil describir con palabras la salida correcta? Si sí, zero-shot puede bastar; si implica un formato específico, un juicio o una distinción difícil de articular, few-shot supera a cualquier cantidad de instrucciones adicionales (Guía PDF p. 182).

### Por qué los ejemplos superan a las instrucciones más largas

**Concepto:** Zero-shot dice al modelo qué hacer; few-shot le muestra cómo es lo "terminado" (Guía PDF p. 182). En zero-shot el modelo debe imaginar la respuesta correcta, con riesgo de formato variable y juicios inconsistentes; en few-shot copia el patrón demostrado (Guía PDF p. 182).

**Ejemplos de uso (3, cortos):**
1. Los ejemplos hacen concreto el formato exacto, así el modelo copia la estructura en vez de inventarla (Guía PDF p. 182).
2. Demuestran el juicio en casos límite, difícil de describir en reglas pero fácil de mostrar (Guía PDF p. 182).
3. Transmiten información implícita (tono, nivel de detalle, manejo de datos ausentes) y reducen campos inventados o vacíos en extracción (Guía PDF p. 182).

### Cómo construir ejemplos eficaces (cantidad, diversidad y razonamiento)

**Concepto:** Se usan 2 a 4 ejemplos dirigidos a los casos ambiguos que causan problemas; menos de 2 no establecen un patrón y más de 4 gastan tokens sin beneficio proporcional (web 4.2). Dos presiones fijan el rango: mínimo 2 para extraer un patrón generalizable y máximo 4 por el coste en tokens (Slides PDF p. 1101). Los buenos ejemplos son relevantes, diversos y claros, cada uno dentro de etiquetas `<example>` y agrupados en `<examples>` (Guía PDF p. 183).

**Ejemplos de uso (3, cortos):**
1. Cada ejemplo ataca un tipo distinto de inconsistencia: selección de herramienta con peticiones ambiguas, formatos de unidades informales, huecos de cobertura en tests, citas en línea frente a bibliografías (Slides PDF p. 1102).
2. Cubrir los casos que fallan: si la extracción funciona en tablas pero no en texto narrativo, mostrar extracción correcta desde texto narrativo (web 4.2).
3. Envolver los ejemplos en `<example>` / `<examples>` para que el modelo los separe de las instrucciones (Guía PDF p. 183).

**Qué NO hacer:**
- No usar ejemplos demasiado parecidos: el modelo se engancha a un patrón no intencionado (Guía PDF p. 183).
- No mostrar solo casos fáciles, que dejan los casos ambiguos sin guía (Guía PDF p. 183).
- No dejar los ejemplos sin envolver en etiquetas (Guía PDF p. 183).

**Posible confusión con otros conceptos:**
- 1 ejemplo — mejor que cero, pero arriesga crear un patrón no deseado porque solo hay un caso del que generalizar (Guía PDF p. 183).
- Más de 5 ejemplos — rendimientos decrecientes; solo compensa si el objetivo es cubrir muchos casos límite (Guía PDF p. 183).

### Incluir el razonamiento en cada ejemplo

**Concepto:** Cada ejemplo debe mostrar por qué se eligió una acción frente a alternativas plausibles, no solo entrada y salida (web 4.2; Guía PDF p. 183). Input → Output solo aprende la correspondencia y falla en casos nuevos; Input → Reasoning → Output aprende el "porqué" y generaliza a patrones nuevos (Slides PDF p. 1103).

**Ejemplos de uso (3, cortos):**
1. Selección de herramienta para "check my order #12345": se elige `lookup_order` porque el identificador específico del pedido indica información del pedido, aunque podría verse como consulta general de cliente y entonces `get_customer` (web 4.2).
2. Sin razonamiento el modelo aprende solo "consultas con número de pedido van a `lookup_order`"; con razonamiento aprende que los identificadores específicos se enrutan a herramientas de búsqueda específicas (web 4.2).
3. Clasificación de variable shadowing en distintos niveles de severidad, con razonamiento, cuando la revisión de código es inconsistente (web 4.2).

```text
Example: Tool selection for "check my order #12345"
Input: "check my order #12345"
Selected tool: lookup_order
Reasoning: The user provides an order number (#12345), indicating
they want order-specific information. Even though this could be
interpreted as a general customer query, the specific order
identifier makes lookup_order the correct choice over get_customer.
```

**Qué NO hacer:**
- No dar solo pares entrada-salida: el modelo hace coincidencia superficial y no generaliza (web 4.2; Slides PDF p. 1103).
- No dar solo la respuesta final sin la razón de la elección (Guía PDF p. 183).

### Reducción de alucinaciones en extracción

**Concepto:** Los ejemplos con extracción correcta desde estructuras variadas (citas en línea y bibliografías, descripciones narrativas y tablas estructuradas, encabezados y texto embebido) enseñan a manejar la variedad estructural sin inventar datos (web 4.2). Importa sobre todo en documentos con formato inconsistente (web 4.2).

**Ejemplos de uso (3, cortos):**
1. Informe financiero con gastos en tabla en una página y en párrafo en la siguiente: sin ejemplos el modelo extrae bien la tabla pero deja campos vacíos o fabrica valores en la parte narrativa (web 4.2).
2. Informes de resultados con tablas, prosa en línea o ambas: ejemplos de extracción desde prosa, con cifras en forma de frase, cierran la brecha de precisión (Q60).
3. Mostrar el mismo hecho en distintos diseños de documento (Guía PDF p. 183).

### Few-shot para reducir falsos positivos y definir fronteras de clasificación

**Concepto:** En revisión de código y análisis, los ejemplos muestran qué marcar y qué ignorar; separar patrones aceptables de problemas genuinos reduce falsos positivos sin perder los problemas reales (web 4.2). Para fronteras entre etiquetas parecidas, los ejemplos positivos muestran cómo es una etiqueta pero no dónde termina; los contraejemplos con una breve explicación definen la frontera (pregunta de muestra de la guía: Guía PDF p. 225, p. 226).

**Ejemplos de uso (3, cortos):**
1. Variable shadowing: el `result` interno sombrea al externo en un ámbito limitado (arrow function), no causa un bug; se clasifica como `minor` (solo si la consistencia de estilo está en alcance) (web 4.2).
2. Lista de qué reportar y qué omitir, más un ejemplo por severidad (SQL injection → critical; lógica que cambia la salida → major; falta de null check con valor por defecto seguro → minor; omitir estilo, orden de imports, formato) (Guía PDF p. 181).
3. Un elemento que parece sin usar pero se referencia indirectamente no debe marcarse; un problema real se muestra con ubicación, problema, severidad y arreglo sugerido (Guía PDF p. 224).

**Qué NO hacer:**
- No depender de "ser conservador" en lugar de definir la frontera real (Guía PDF p. 181).
- No filtrar por una puntuación de confianza que el modelo no está calibrado para dar (Guía PDF p. 181).
- No definir niveles de severidad sin ejemplos: la línea queda subjetiva (Guía PDF p. 181).

**Posible confusión con otros conceptos:**
- Suprimir una categoría ruidosa — recuperación práctica: desactivarla temporalmente, mejorar sus criterios y reactivarla después; una categoría que dispara falsos positivos erosiona la confianza en las precisas (Guía PDF p. 181).

### Elegir la técnica correcta (few-shot vs. otras)

**Concepto:** El examen prueba reconocer cuándo aplica otra técnica en lugar de few-shot (web 4.2).

**Ejemplos de uso (3, cortos):**
1. Formato de salida inconsistente → few-shot examples; JSON malformado → `tool_use` con JSON schemas (web 4.2).
2. Valores fabricados para campos ausentes → campos de schema opcionales/nullable; la suma extraída no coincide con el total → validation-retry loop (web 4.2).
3. Selección de herramienta incorrecta → mejores descripciones de herramientas primero, luego few-shot; el texto narrativo no se extrae → few-shot de extracción narrativa (web 4.2).

**Qué NO hacer:**
- No esperar que few-shot arregle la fabricación de datos ausentes: eso necesita cambios de schema (web 4.2).
- No usar solo un linter de post-procesado o un schema JSON estricto para enseñar cuándo un hallazgo es válido: imponen estructura pero no enseñan el razonamiento (Guía PDF p. 225).

**Posible confusión con otros conceptos:**
- Prompt chaining — divide una tarea compleja en pasos enfocados donde la salida de cada uno alimenta el siguiente (p. ej. revisar cada archivo y luego un paso de integración entre archivos) (Guía PDF p. 222). Few-shot, en cambio, mejora la consistencia en tareas sensibles al formato y maneja entradas ambiguas y variadas (Guía PDF p. 222).

### Trampas del examen

- Elegir "añadir instrucciones más detalladas / una especificación de formato" cuando el formato es inconsistente: las instrucciones describen el formato de nuevo, los ejemplos muestran el formato objetivo; la especificación ya se habría probado (web 4.2; Q58). Las opciones de post-procesado con `--output-format json` o de auto-revisión añaden complejidad o una ronda extra sin garantizar generación consistente (Q58).
- Añadir más ejemplos de cláusulas estándar para reforzar el esquema: refuerza lo que ya funciona y no enseña el caso límite (por ejemplo cláusula con terminación y force majeure); la respuesta es ejemplos dirigidos con el razonamiento de por qué pertenece a una categoría y no a la otra (Q59). Cambiar a extraer sin categorizar elude el problema, y un campo de confianza con revisión humana no mejora el juicio del modelo (Q59).
- Intensificar el lenguaje de precisión del prompt, preprocesar la prosa a tablas o usar un prompt separado que aísle frases con números: no resuelven la diferencia estructural (94 % en tablas frente a 72 % en prosa); lo que sí lo hace son ejemplos de extracción desde prosa (Q60). En el escenario de práctica de la web (tablas bien, párrafos vacíos, documentos en su forma original) la opción correcta es few-shot con tablas y párrafos; ampliar la ventana de contexto, convertir narrativa a tablas o reintentar en post-procesado no atacan la causa (web 4.2).
- Instrucciones detalladas más formato JSON estricto para cada patrón indirecto: difícil de mantener, puede fallar con patrones nuevos y no enseña cuándo un hallazgo es válido; la opción correcta combina ejemplos de patrón indirecto y de formato (location, issue, severity, suggested fix) (Guía PDF p. 223, p. 225).
- Quitar todos los ejemplos, aumentar los ejemplos positivos de `termination` o usar prosa más larga para separar `force majeure` de `termination`: solo los contraejemplos con explicación definen la frontera (Guía PDF p. 225, p. 226, p. 227).
- Usar umbrales de confianza para juicios inconsistentes: mal calibrados y sin atacar la causa raíz (web 4.2).
- Añadir muchos ejemplos para cubrir todos los casos: se pierde tokens sin beneficio proporcional; el razonamiento de cada ejemplo es lo que enseña a generalizar (web 4.2; Slides PDF p. 1101).
- Usar few-shot para arreglar el mal enrutamiento de herramientas cuando la causa real es una descripción débil, y esperar formato consistente de zero-shot en tareas complejas (Guía PDF p. 182, p. 183).
- **Contradicción entre fuentes:** sobre el número de ejemplos, la web indica 2 a 4 según la guía de examen y señala que la documentación actual sugiere 3 a 5 (web 4.2); las slides fijan mínimo 2 y máximo 4 (Slides PDF p. 1101) y el banco habla de 2-4 (Q58), mientras que la guía PDF presenta 3 a 5 como el punto óptimo documentado por Anthropic y más de 5 con rendimientos decrecientes, aunque la propia guía también recoge 2 a 4 ejemplos que resuelven casos genuinamente difíciles (Guía PDF p. 183). Prevalecen la guía y el banco sobre la web; la guía menciona tanto 3-5 como 2-4 y el banco 2-4, y no se decide cuál es la correcta.

## Tarea 4.3 — Enforce structured output using tool use and JSON schemas (Forzar salida estructurada con tool use y JSON schemas)

> Prioridad de estudio: Método de salida estructurada (regresión: 100% -> 0%)

### Salida estructurada con tool use y JSON schema

**Concepto:** La salida estructurada es una respuesta cuyos campos y tipos siguen una forma fija; el JSON schema define esa forma (campos, tipos y cuáles son required) (web 4.3; Guía PDF p. 186). Tool use es el mecanismo principal: la tool actúa como contrato de salida y su input schema define la forma exacta de los datos devueltos (Guía PDF p. 184-185). Es el método más fiable frente a pedir JSON en el prompt, que es texto sin garantías estructurales (web 4.3; Q61).

**Ejemplos de uso (3, cortos):**
1. Un pipeline de extracción de facturas define una tool con input schema y lee el resultado del bloque `tool_use` de la respuesta (Q61; Guía PDF p. 184).
2. Un servicio downstream espera `total_amount` como número siempre, con ese tipo (Guía PDF p. 184).
3. Con una tool disponible, Claude responde con un bloque estructurado (nombre de la tool e inputs) y `stop_reason` `tool_use`; tu código ejecuta y devuelve un `tool_result` (Guía PDF p. 184).

**Qué NO hacer:**
- No añadir instrucciones como "Your response must be valid JSON" ni confiar en que el modelo se autoverifique: no da la garantía determinista de tool use (Q61).
- No usar reintentos en el prompt ni un regex post-processor: A solo reduce la frecuencia y D es una solución frágil que no cubre todos los patrones de error de sintaxis (Q61).
- No escribir descripciones de tool vagas: el modelo decide si llama a una tool según su descripción y una mala lleva a llamadas omitidas o tool equivocada (Guía PDF p. 185).

**Posible confusión con otros conceptos:**
- Prompt-based JSON — pide JSON en una respuesta de texto; puede producir JSON malformado y en producción lo hará periódicamente (web 4.3).
- tool_use con schema — el schema de la tool restringe la forma y elimina errores de sintaxis como llaves faltantes, comas finales y claves sin comillas (web 4.3; Slides PDF p. 1119).

### tool_choice: modos y cuándo usar cada uno

**Concepto:** `tool_choice` controla si el modelo llama a una tool y cuál; es lo que lleva de "Claude podría llamar a una tool" a "Claude llama definitivamente a esta tool" (Guía PDF p. 86). Se aplica por request, no por conversación (web 4.3).

**Ejemplos de uso (3, cortos):**
1. `auto` (por defecto): el modelo decide; sirve para un agente conversacional que a veces consulta pedidos y a veces responde preguntas generales (Guía PDF p. 87-88; web 4.3).
2. `any`: el modelo debe llamar a una tool pero elige cuál; sirve con varios schemas de extracción (extract_invoice, extract_receipt, extract_contract) y tipo de documento desconocido (web 4.3; Guía PDF p. 87; Q62).
3. `{"type": "tool", "name": "extract_metadata"}`: fuerza una tool concreta; sirve para un primer paso obligatorio como extraer metadata antes del enriquecimiento (web 4.3; Guía PDF p. 188).

```json
{ "type": "any" }
{ "type": "tool", "name": "extract_metadata" }
```

**Qué NO hacer:**
- No usar `auto` cuando necesitas salida estructurada garantizada: Claude puede responder con texto y romper el parser, por ejemplo "I found the invoice number is INV-1234." (Guía PDF p. 87-88; Q62).
- No forzar una tool concreta cuando no conoces el tipo de documento: eso anula el propósito (Q62).
- No dejar el `tool_choice` forzado en la siguiente request: tras la llamada forzada se envía la siguiente request con `auto` o sin el parámetro; si no, el modelo debe llamar a la misma tool otra vez y entras en un bucle (web 4.3).

**Posible confusión con otros conceptos:**
- `any` — el modelo elige cuál tool, pero debe llamar a una (Guía PDF p. 88, 190).
- `tool` — el modelo debe llamar a la tool específica que nombras (Guía PDF p. 88, 190).
- `none` — el modelo no puede llamar a ninguna tool aunque haya tools definidas; sirve para probar comportamiento solo de texto o desactivar tools en un turno (Guía PDF p. 86-87, 188).

### Errores de sintaxis vs. errores semánticos

**Concepto:** El schema garantiza la forma de la salida, no el significado de los valores (Guía PDF p. 188). tool_use con JSON schema elimina errores de sintaxis pero no errores semánticos, donde un JSON válido contiene contenido incorrecto (web 4.3). Esta distinción se evalúa mucho (Guía PDF p. 87, 188).

**Ejemplos de uso (3, cortos):**
1. Error de sintaxis que el schema detecta: falta una llave de cierre o un tipo incorrecto, como `total_amount` string en lugar de número (Guía PDF p. 88-89; con `strict`, Guía PDF p. 88).
2. Error semántico que el schema no detecta: `total_amount` es 150.00 pero las líneas suman 180.00 (Guía PDF p. 88; web 4.3).
3. Otros errores semánticos: el nombre del cliente aparece en el campo email, o `status` es "completed" con `completion_date` null; y fabricación: el modelo inventa valores para campos required cuando el documento no trae la información (Guía PDF p. 88; web 4.3).

**Qué NO hacer:**
- No asumir que el schema (o strict tool use) garantiza valores correctos: solo garantiza estructura (Guía PDF p. 88, 190).
- No esperar que el schema resuelva por sí solo los errores semánticos: requieren una capa de validación (Pydantic, comprobaciones propias); la validación maneja el significado (Guía PDF p. 88; web 4.3, que remite a la Task Statement 4.4).

**Posible confusión con otros conceptos:**
- Prevención de errores de sintaxis (schema) — asegura estructura parseable; el error típico es suponer que también garantiza valores correctos (Guía PDF p. 189).
- Detección de errores semánticos (validación) — verifica significado, no solo forma; el error típico es esperar que lo maneje el schema (Guía PDF p. 189).

### Campos required, optional y nullable

**Concepto:** Elegir entre required, optional y nullable es la decisión más importante del diseño de schema: la elección equivocada no lanza error, produce datos malos en silencio (Guía PDF p. 187, 191). Un campo required fuerza un valor aunque la fuente no lo tenga, y el modelo lo fabrica; un campo nullable permite devolver `null` con honestidad (web 4.3; Guía PDF p. 187; Slides PDF p. 1167).

**Ejemplos de uso (3, cortos):**
1. required: datos que la fuente siempre contiene, como `invoice_number` y `vendor_name` en el ejemplo de la web (Guía PDF p. 186; web 4.3).
2. nullable: datos que pueden faltar pero deben aparecer en la salida, como `payment_terms` y `purchase_order` con tipo `["string", "null"]` (web 4.3; Guía PDF p. 187).
3. optional: dato que puede omitirse del output cuando la fuente no lo tiene y el consumidor lo tolera (Guía PDF p. 187, 191).

```json
{
  "type": "object",
  "properties": {
    "invoice_number": { "type": "string" },
    "vendor_name": { "type": "string" },
    "payment_terms": { "type": ["string", "null"] },
    "purchase_order": { "type": ["string", "null"] }
  },
  "required": ["invoice_number", "vendor_name"]
}
```

**Qué NO hacer:**
- No marcar todos los campos como required para "asegurar completitud": presiona al modelo a fabricar valores cuando falta la información (web 4.3; Guía PDF p. 190).
- No marcar required un campo que la fuente puede no traer; solo cuando se esté seguro de que siempre lo proporciona (Guía PDF p. 187, 191).
- No dejar sin nullability un campo que puede faltar: el modelo rellena el hueco con una suposición (Guía PDF p. 187, 196).

**Posible confusión con otros conceptos:**
- optional — el campo puede desaparecer del output; la ausencia es ambigua (Guía PDF p. 191-192).
- nullable — el campo debe aparecer pero puede valer `null`; señal explícita de que se buscó y no se halló, y es el default más seguro para la mayoría de datos ausentes (Guía PDF p. 191-192; Slides PDF p. 1194).
- Pregunta de auditoría para cada required: "Is this field guaranteed to be in every source document I'm extracting from?" (Slides PDF p. 1184).

### Campos enum: "unclear" y "other" + detail

**Concepto:** Un enum restringe el campo a un conjunto fijo de valores, evitando etiquetas inventadas y variaciones del mismo valor entre ejecuciones (Guía PDF p. 187, 192). Un enum cerrado (sin opción de respaldo) falla en silencio cuando aparece un valor no previsto: el modelo debe elegir la coincidencia más cercana, que puede ser errónea, y la salida pasa la validación (Guía PDF p. 192).

**Ejemplos de uso (3, cortos):**
1. `"unclear"` en el enum para fuentes genuinamente poco claras, como un escaneo roto que podría ser recibo o factura; el modelo lo elige en vez de adivinar (web 4.3; Slides PDF p. 1206).
2. `"other"` más un string de detalle para categorías extensibles, como un extracto bancario del cliente (web 4.3; Slides PDF p. 1209).
3. Los valores `other` pueden enviarse a una cola de revisión humana; los `unclear` pueden marcarse para seguimiento, y un alto volumen de `unclear` señala baja calidad de datos o categorías mal definidas (Guía PDF p. 193).

```json
{
  "category": {
    "type": "string",
    "enum": ["invoice", "receipt", "contract", "unclear", "other"]
  },
  "category_detail": {
    "type": ["string", "null"],
    "description": "Freeform detail when category is 'other'"
  }
}
```

**Qué NO hacer:**
- No usar un enum cerrado sin `other` para una categoría que sigue creciendo (Guía PDF p. 196).
- No omitir `unclear`: sin él el modelo debe clasificar igualmente la fuente ambigua, con clasificaciones seguras pero erróneas (web 4.3; Guía PDF p. 193).

**Posible confusión con otros conceptos:**
- `other` — existe un valor pero no encaja en la lista (Guía PDF p. 193).
- `unclear` — la fuente no contiene información suficiente para clasificar (Guía PDF p. 193).

### Reglas de format normalization

**Concepto:** Una regla de normalización es una guía en el prompt que indica cómo estandarizar un valor antes de devolverlo; el schema fija la forma y las reglas fijan los valores dentro de esa forma (Guía PDF p. 194; web 4.3). Se ponen en el prompt junto al schema, no dentro del schema, y agrupadas por tipo de campo justo después de la definición del schema (Guía PDF p. 196).

**Ejemplos de uso (3, cortos):**
1. Fechas en ISO 8601 (YYYY-MM-DD); si falta la fecha, devolver null y no inferirla (Guía PDF p. 194; web 4.3).
2. Importes como número con dos decimales, sin símbolos de moneda ni separadores de miles (Guía PDF p. 195; web 4.3 usa "decimal numbers without currency symbols").
3. Teléfonos en E.164, emails en minúsculas, países con códigos ISO 3166-1 alpha-2 (Guía PDF p. 194-195).

**Qué NO hacer:**
- No esperar que el schema arregle formatos inconsistentes: "January 5, 2024", "01/05/24" y "2024-01-05" pasan la validación de tipo (Guía PDF p. 194).
- No usar una regla de normalización para un valor genuinamente ausente o ambiguo: usar nullable con `null` o un valor `unclear` (Guía PDF p. 195).
- No escribir reglas complejas sin ejemplo ni colocarlas lejos del schema en un prompt largo (Guía PDF p. 195-196).

### Structured Outputs nativo: JSON outputs y strict tool use

**Concepto:** Claude ofrece la función nativa Structured Outputs con dos modos, usables solos o juntos: JSON outputs (`output_config.format`) cuando la respuesta final es el dato, y strict tool use (`strict: true`) cuando cada llamada de acción en un flujo agéntico debe ser schema-valid (Guía PDF p. 186, 190). `strict: true` garantiza que el nombre de la tool y los inputs coinciden con el schema (Guía PDF p. 186).

**Ejemplos de uso (3, cortos):**
1. Convertir un documento en un registro con `output_config.format` (Guía PDF p. 190).
2. Combinar `tool_choice` `tool` con `strict: true` garantiza que la tool se llama y que los inputs coinciden con el schema: sin campos required ausentes ni tipos incorrectos (Guía PDF p. 87).
3. Con strict tool use se rechaza cualquier llamada cuyos inputs no coincidan con el schema antes de ejecutarse (Guía PDF p. 190).

**Posible confusión con otros conceptos:**
- JSON outputs — controla la forma de la respuesta final (Guía PDF p. 190).
- Strict tool use — controla los inputs de cada llamada a tool (Guía PDF p. 190).
- Truncamiento — un `max_tokens` bajo puede cortar una llamada a tool incompleta; la solución típica es subir `max_tokens` y reintentar (Guía PDF p. 190, 220).

### Trampas del examen

- Creer que tool_use con JSON schemas previene todos los errores de extracción: solo elimina los de sintaxis, no sumas que no cuadran, datos mal ubicados ni valores fabricados (web 4.3; Guía PDF p. 88, 189). Hace falta validación aparte.
- Q61 (JSON con errores de sintaxis en ~3% de respuestas): la respuesta es B, tool use con JSON schema. A (reintentar hasta 3 veces) reduce la frecuencia pero no elimina los errores; C (instrucción de "valid JSON") depende de la autoverificación del modelo y no es determinista; D (regex post-processor) es frágil y no cubre todos los patrones (Q61).
- Q62 (dos tools, tipo desconocido, 30% de respuestas en texto con `auto`): la respuesta es A, `tool_choice: "any"`. B fuerza una tool concreta y no sirve sin conocer el tipo; C es una instrucción de prompt con cumplimiento probabilístico que ya falló con el 30%; D (fusionar en una tool con `document_type` opcional) es un cambio de arquitectura válido pero con más esfuerzo que un cambio de configuración (Q62).
- Confiar en `auto` para garantizar una llamada a tool: puede omitirla; con varios schemas y tipo desconocido se usa `any` (web 4.3; Guía PDF p. 88).
- Confundir `any` (el modelo elige cuál) con `tool` (tool nombrada específica) (Guía PDF p. 88, 190, 220).
- Poner `tool_choice` en `none` y preguntarse por qué no se llaman tools (Guía PDF p. 88).
- Hacer todos los campos required para asegurar completitud: induce fabricación; la opción correcta es campos optional/nullable cuando la fuente puede no tener la información, no cambiar a JSON por prompt, ni añadir más instrucciones, ni solo validar después (web 4.3, escenario de práctica; Slides PDF p. 1167).
- Tratar optional y nullable como intercambiables cuando el sistema downstream necesita un `null` explícito (Guía PDF p. 190, 196).
- Si una pregunta pide garantizar que la tool se llama Y que los inputs coinciden con el schema: `tool_choice` `tool` (o `any`) con `strict: true`; si pide que los VALORES sean correctos, eso requiere una capa de validación (Guía PDF p. 88).
- **Contradicción entre fuentes:** la web 4.3 afirma que la guía nombra tres modos de `tool_choice` y que `{"type": "none"}` es un cuarto modo de la documentación actual, y presenta `strict: true` y `output_config.format` como controles posteriores a la guía; la guía PDF lista cuatro modos (auto, any, tool, none) e incluye `strict: true` y `output_config.format` (Guía PDF p. 86, 188, 190, 220; web 4.3). Prevalece la guía: cuatro modos. La web también indica que modelos como Opus 5.5, Sonnet 5.5, Fable 5.1 y Mythos 5.1 rechazan `any` y `tool` forzados con error 400, y recomienda `auto` con `strict: true`; este dato solo aparece en la web y no figura en la guía ni en el banco (web 4.3).

## Tarea 4.4 — Implement validation, retry, and feedback loops for extraction quality (Implementar bucles de validación, reintento y retroalimentación para la calidad de la extracción)

> Prioridad de estudio: Feedback loops con metadata de errores (0% en el mapa de refuerzo)

### Validation loop (bucle de validación) y su secuencia fija

**Concepto:** Un validation loop comprueba la salida del modelo contra tus reglas y, cuando falla, devuelve el fallo al modelo para que lo corrija; es la capa entre la salida de Claude y el sistema downstream (Guía PDF p. 197). Sin esa capa, los datos malos pasan en silencio (Guía PDF p. 197). La tarea figura en el dominio 4 como "Implement validation, retry, and feedback loops for extraction quality" (Slides PDF p. 1081).

La guía describe seis pasos en orden fijo: 1) Extract, 2) Validate structure, 3) Validate semantics, 4) Classify the error (resolvable o unresolvable), 5) Retry or escalate, 6) Log the result (Guía PDF p. 198). Saltarse un paso deja pasar datos malos, desperdicia un reintento o deja invisibles los patrones de fallo (Guía PDF p. 198).

**Ejemplos de uso (3, cortos):**
1. Un despacho de abogados extrae facturas de proveedores con line items, un total declarado y una referencia de asunto (web 4.4).
2. Una factura cuyos line items suman menos que su total declarado se valida y se reintenta (web 4.4).
3. Una factura que no menciona ninguna referencia de asunto se envía a una persona (web 4.4).

**Qué NO hacer:**
- No saltarse el paso "Classify the error": los errores irresolubles se reintentarían y arriesgan fabricación (Guía PDF p. 198).
- No omitir el paso "Log the result": los patrones de fallo quedan invisibles (Guía PDF p. 198).

### Errores de sintaxis de schema vs errores de validación semántica (capas de validación)

**Concepto:** Los errores de sintaxis de schema son JSON malformado, campos requeridos ausentes y tipos incorrectos; tool_use con JSON schemas los elimina con `strict: true` (web 4.4). Los errores semánticos tienen estructura correcta pero valores incorrectos (sumas que no cuadran, fechas en orden erróneo, valores en el campo equivocado) y un schema no puede expresar que dos números deban coincidir (web 4.4). La guía los organiza en tres capas: schema validation (estructura, tipos, campos requeridos, enums; herramienta: JSON schema, strict tool use), semantic validation (consistencia aritmética, ubicación de campos, contradicciones; Pydantic, checks personalizados) y business rule validation (restricciones de dominio; lógica personalizada) (Guía PDF p. 200). Ninguna capa atrapa todo y las tres hacen falta en producción (Guía PDF p. 200).

Pydantic hace dos trabajos: el parsing impone estructura (tipos, campos requeridos, enums) y los validators imponen semántica, como aritmética entre campos u orden de fechas; ambos fallos aparecen en un `ValidationError` con el campo y la regla rota (web 4.4). Un field validator corre sobre un solo campo tras pasar la validación de tipos; un model validator corre después de los field validators y ve todos los campos, por lo que es el lugar para la lógica entre campos (Guía PDF p. 203; Guía PDF p. 204). El mensaje del `ValidationError` es el que se incluye en el prompt de feedback del reintento (Guía PDF p. 204).

```python
@model_validator(mode="after")
def totals_must_match(self):
    calculated = round(sum(i.amount for i in self.line_items), 2)
    if abs(calculated - self.stated_total) > 0.01:
        raise ValueError(
            f"line items sum to {calculated} but stated_total is {self.stated_total}"
        )
    return self
```
(web 4.4)

**Ejemplos de uso (3, cortos):**
1. Line items que no suman el total declarado: cada campo es un número válido y solo recalcular revela el desajuste (Guía PDF p. 202).
2. Un nombre en un campo de email o un precio en un campo de cantidad: el tipo coincide y el schema lo acepta (Guía PDF p. 202).
3. Regla de negocio: una fecha de envío debe ser posterior a la fecha del pedido; un descuento no puede exceder el precio; un estado `completed` requiere fecha de finalización no nula (Guía PDF p. 202).

**Qué NO hacer:**
- No esperar que el schema atrape sumas o ubicación de campos; son checks semánticos (Guía PDF p. 207).
- No tratar Pydantic como redundante porque tool_use ya imponga un JSON schema: los schemas no expresan reglas entre campos (web 4.4).
- No suponer que `strict: true` o `client.messages.parse(..., output_format=Invoice)` eliminan la validación semántica: la plataforma impone el schema, tus validators las reglas de negocio y el retry loop gestiona el fallo de cualquiera (web 4.4).

**Posible confusión con otros conceptos:**
- Schema syntax error (4.3) — JSON malformado o tipo incorrecto, lo elimina tool_use con `strict: true` (web 4.4)
- Semantic validation error — line items que no suman el total, requiere lógica fuera del schema y es donde se centran los retry loops (web 4.4)

### Retry-with-error-feedback

**Concepto:** En un reintento se devuelven tres cosas: el documento original, la extracción fallida y el error de validación específico (web 4.4; Guía PDF p. 200). Un reintento sin feedback es "una segunda conjetura": el modelo produce más o menos la misma salida con variaciones menores (Guía PDF p. 200). Con el error específico, el modelo puede re-examinar el documento en busca de line items omitidos, revisar la ubicación de campos o recalcular el total (web 4.4).

```typescript
const retryMessages = [{
  role: "user",
  content: `Original document:\n${originalDocument}\n\n` +
    `Your extraction:\n${JSON.stringify(failedExtraction)}\n\n` +
    `Validation error: Line items sum to £450 but stated_total is £500. ` +
    `Please re-extract, ensuring all line items are captured.`
}];
```
(web 4.4)

Cómo redactar un buen feedback prompt: ser específico sobre qué falló ("invoice_number is missing" mejor que "the output was invalid"), citar el campo exacto y la regla violada, y no incluir errores que el modelo no puede arreglar (Guía PDF p. 200). Calidad del feedback: "Please try again" = el modelo adivina sin información nueva; "The output was invalid" = ajustes menores al azar; "invoice_number is missing. It appears in the header as INV-XXXX." = el modelo apunta al campo y ubicación exactos (Guía PDF p. 200; Guía PDF p. 201).

**Ejemplos de uso (3, cortos):**
1. Mensaje de reintento: "line items sum to £450 but stated_total is £500" (web 4.4).
2. "total_amount must be a number but returned as a string" da un objetivo preciso (Guía PDF p. 200).
3. Mensaje de Pydantic "line_item_total 150.00 does not match stated_total 180.00" apunta directo a la discrepancia (Guía PDF p. 204).

**Qué NO hacer:**
- No reintentar sin el error específico: el modelo suele repetir el fallo (web 4.4; Q63).
- No mezclar errores resolubles e irresolubles en el mismo feedback prompt: el modelo puede fabricar el valor del campo imposible mientras arregla los demás (Guía PDF p. 200; Guía PDF p. 209).
- No reintentar con el mismo prompt esperando que converja (Q63).

**Posible confusión con otros conceptos:**
- Retry sin feedback — "Please try again" (Guía PDF p. 200)
- Retry con feedback — documento + extracción fallida + error específico (Guía PDF p. 200)

### Resolvable vs unresolvable errors (límite de efectividad del reintento)

**Concepto:** Un reintento solo permite al modelo mirar de nuevo lo que el pipeline le dio (web 4.4). Un error resolvable es de formato o estructura: la información existe en la fuente pero volvió con la forma equivocada; un error unresolvable es un dato faltante que ningún reintento puede producir (Guía PDF p. 199). Es el juicio más importante de la sección (Guía PDF p. 199) y el concepto que el examen prueba con más fuerza en esta tarea (web 4.4).

Efectivo para: format mismatches (formato de fecha, notación de moneda), structural output errors (valores en campos equivocados, anidación incorrecta), misplaced values y errores matemáticos (el modelo omitió un line item que afecta el total) (web 4.4). No efectivo para: información genuinamente ausente, datos que solo existen en un documento externo no proporcionado y campos que requieren conocimiento que el modelo no tiene (web 4.4). Ante un valor ausente: marcar para revisión humana, o devolver null si el schema lo permite (web 4.4); la guía indica no reintentar y ajustar el input o el schema (Guía PDF p. 199).

Fabrication risk: al reintentar un error irresoluble el modelo puede producir un valor plausible que pasa la validación del schema y es incorrecto; esto causa silent failure, y los valores fabricados son la causa más común de fallos silenciosos en pipelines de extracción (Guía PDF p. 199; Guía PDF p. 200).

Causas de errores semánticos: extraction error (el modelo colocó mal o copió el número equivocado; a menudo resoluble con feedback dirigido) y source inconsistency (el documento fuente es contradictorio; normalmente irresoluble, se escala a revisión humana) (Guía PDF p. 203). Resolubilidad por reintento: line items que no suman = a veces; valor en campo equivocado = sí, con feedback específico; dos campos que se contradicen = normalmente no; campo calculado que no coincide = a veces (Guía PDF p. 203).

**Ejemplos de uso (3, cortos):**
1. Factura con línea omitida que sí está en la página: se reintenta con el error (web 4.4).
2. Factura sin referencia de asunto: va a una persona (web 4.4).
3. Un resumen de préstamo que remite a un anexo externo no contiene la dirección del garante; no hay reintento que la extraiga (Q67).

**Qué NO hacer:**
- No suponer que los reintentos siempre funcionan (web 4.4).
- No reintentar ni elegir un valor cuando el documento se contradice: un reintento no resuelve una discrepancia de la fuente y elegir es adivinar (web 4.4).
- No subir el límite de reintentos sin diagnosticar si el dato está en la fuente (Q67).

**Posible confusión con otros conceptos:**
- Error resoluble — fecha en formato equivocado, el dato existe en el documento (Guía PDF p. 199)
- Error irresoluble — campo requerido que la fuente nunca contuvo (Guía PDF p. 199)

### In-schema self-checks (calculated_total, conflict_detected, confidence)

**Concepto:** Son campos añadidos al schema para que el modelo reporte su propia evaluación de la extracción y se hagan visibles inconsistencias (Guía PDF p. 204). Reducen la lógica de validación externa y evitan que esas señales se pierdan en texto libre (Guía PDF p. 204).

- `calculated_total` vs `stated_total`: se extrae la suma del modelo de los line items y el total del documento; si difieren, hay una bandera de discrepancia sin lógica externa (web 4.4). `stated_total` es el total tal como aparece en la fuente (Guía PDF p. 205).
- `conflict_detected`: boolean que se pone en true ante información contradictoria en la fuente; el modelo debe extraer ambos valores en vez de elegir uno en silencio (web 4.4). La guía lo enruta a la human review queue (Guía PDF p. 205).
- `confidence`: indica cuán seguro está el modelo; los registros de baja confianza se enrutan a revisión humana (Guía PDF p. 205). Baja confianza no significa que el valor sea erróneo (Guía PDF p. 205).

```json
{
  "line_items": [
    { "description": "Widget A", "amount": 150.00 },
    { "description": "Widget B", "amount": 300.00 }
  ],
  "calculated_total": 450.00,
  "stated_total": 500.00,
  "total_discrepancy": true
}
```
(web 4.4)

**Ejemplos de uso (3, cortos):**
1. La factura del experto llega con la bandera `total_discrepancy` (web 4.4).
2. Una nota de honorarios con "payment due: 30 days" y "payment terms: net 60" llega con `conflict_detected: true` (web 4.4).
3. Un documento con cantidad diez en una sección y cinco en otra: el modelo marca el conflicto y un humano decide (Guía PDF p. 204).

**Qué NO hacer:**
- No añadir `calculated_total` en post-processing y usarlo como valor canónico: reemplaza en silencio el total extraído y puede propagar errores si los line items se extrajeron mal (Q63).

**Posible confusión con otros conceptos:**
- `calculated_total` — suma de los line items que calcula el modelo (Guía PDF p. 204)
- `stated_total` — total tal como aparece en el documento fuente (Guía PDF p. 205)

### detected_pattern y feedback loops con metadata de errores

**Concepto:** `detected_pattern` registra qué construcción, condición o regla específica disparó un hallazgo; rastrearlo revela qué criterios generan más falsos positivos y dónde ajustar el prompt (Guía PDF p. 204; web 4.4; Q64). Permite analizar los hallazgos descartados por patrón: si los desarrolladores descartan un patrón de forma consistente (p. ej. "variable shadowing in nested scope"), probablemente hay que refinar el prompt para ese patrón (web 4.4). Es el bucle de mejora sistemático: extract, validate, collect dismissal data, refine prompts, repeat (web 4.4).

```json
{
  "finding": "Potential SQL injection vulnerability",
  "severity": "critical",
  "detected_pattern": "string concatenation in SQL query",
  "file": "user_service.py",
  "line": 42
}
```
(web 4.4)

Los noisy criteria son reglas que disparan hallazgos con demasiada frecuencia sobre casos que no son problemas reales; el false positive rate es la proporción de hallazgos de un criterio que resultan no ser reales (Guía PDF p. 205). Registrar el resultado de los reintentos (qué falló, qué se reintentó y el desenlace) hace visibles los problemas sistémicos de schema o prompt (Guía PDF p. 198; Guía PDF p. 209).

**Ejemplos de uso (3, cortos):**
1. Un pipeline de CI con muchos falsos positivos y salida con solo `file`, `line` y `description`: añadir `detected_pattern` a cada hallazgo (Q64).
2. Registrar cada `detected_pattern`, su frecuencia y su tasa de descarte, con los patrones de mayor descarte primero para refinar el prompt (web 4.4).
3. Registrar qué campos y tipos de documento alcanzan el límite de reintentos (Guía PDF p. 207).

**Qué NO hacer:**
- No usar solo `confidence`: da puntuaciones pero no identifica qué provocó el hallazgo (Q64).
- No usar solo `category`: agrupa por tipo pero no permite depurar a nivel de patrón (Q64).
- No pedir al modelo un booleano `is_false_positive` para autoetiquetarse: no puede distinguir verdaderos de falsos positivos sin ground truth (Q64).

**Posible confusión con otros conceptos:**
- `detected_pattern` — "string concatenation in SQL query", la construcción que disparó el hallazgo (web 4.4)
- `confidence` — qué tan seguro está el modelo, para enrutar a revisión (Guía PDF p. 205)
- `conflict_detected` — contradicción en el documento fuente (Guía PDF p. 204)

### Max retry limits (límites de reintentos) y human review queue

**Concepto:** Un max retry limit es el número máximo de intentos de corrección antes de detenerse y escalar el registro; no es opcional en producción (Guía PDF p. 206). Sin límite, el loop corre sin fin sobre errores irresolubles consumiendo tokens y tiempo (Guía PDF p. 206).

- Límite de dos a tres intentos para la mayoría de extracciones; un reintento resuelve la mayoría de errores resolubles y un segundo cubre el caso de un nuevo error menor; más de tres rara vez mejora la precisión y aumenta el coste (Guía PDF p. 206).
- Extracción simple de campos: quizá un reintento; extracción compleja multidocumento: puede justificar tres (Guía PDF p. 206).
- Al alcanzar el límite: registrar la fuente, la última salida y todos los errores; enrutar a la human review queue sin descartar en silencio; no permitir que entren al sistema downstream aunque parezcan estructuralmente válidos (Guía PDF p. 206; Guía PDF p. 207).
- Diagnóstico: un campo que alcanza el límite repetidamente indica problema de schema o prompt; un tipo de documento, formato no cubierto por los ejemplos; todos los campos de un documento, fuente inutilizable; límite en el primer reintento, error probablemente irresoluble (Guía PDF p. 207).

La guía ilustra el patrón con `MAX_RETRIES = 3` y un `model_validator` que compara `line_item_total` con `stated_total` (Guía PDF p. 208).

**Ejemplos de uso (3, cortos):**
1. Tras 3 reintentos con feedback, el campo "guarantor address" sigue en null: investigar si está en el documento antes de más reintentos (Q67).
2. Un registro que agota los reintentos se registra y va a la human review queue (Guía PDF p. 206).
3. Un tipo de documento que agota reintentos con frecuencia: añadir ejemplos para ese formato (Guía PDF p. 207).

**Qué NO hacer:**
- No dejar un loop sin límite (runaway loop) (Guía PDF p. 206; Guía PDF p. 209).
- No descartar registros que superan el límite: provoca silent data loss (Guía PDF p. 206; Guía PDF p. 207).

### Trampas del examen

- Asumir que los reintentos siempre funcionan: arreglan formato, estructura y valores mal colocados, pero no producen información ausente; los casos con información ausente van a revisión humana o null si el schema lo permite (web 4.4).
- Reintentar sin incluir el error de validación específico: produce los mismos errores (web 4.4). Q63 opción A (reintentar 3 veces con el mismo prompt) falla porque el modelo reproduce el mismo error (Q63).
- Q63 opción C (marcar como datos faltantes y mandar a revisión humana sin reintento) falla por prematura: los datos están presentes y un reintento con feedback puede resolverlo (Q63). Opción D falla porque sustituye en silencio el total extraído y puede propagar errores (Q63). Respuesta correcta: B, documento original + extracción fallida + error específico (Q63).
- Reintentar, o elegir un valor, cuando el documento se contradice: extraer ambos valores con `calculated_total` y `stated_total` o un flag `conflict_detected` y enrutar a revisión (web 4.4).
- Tratar Pydantic como redundante tras tool_use: los schemas no expresan reglas entre campos como sumas u orden de fechas (web 4.4).
- Q64: `confidence` (A) no identifica qué provocó el hallazgo; `category` (C) no permite depurar por patrón; `is_false_positive` (D) es poco fiable sin ground truth; correcta B, `detected_pattern` (Q64).
- Q67: subir el límite a 5 (A) añade reintentos sin diagnosticar; un modelo más grande (C) no resuelve la ausencia de datos; hacer el campo opcional (D) elimina la validación en lugar de diagnosticar la causa raíz; correcta B, comprobar si el dato está en el documento o solo remite a un anexo externo (Q67).
- Escenario práctico de la web: Documento A (suma £450 vs total £500) se reintenta con el error de discrepancia; Documento B (campo "department" ausente en la fuente) va a revisión humana. Descartadas: omitir reintentos en ambos, reintentar ambos con el mismo prompt, o pedir encontrar el departamento ausente (web 4.4).
- Errores comunes de la guía: reintentar cuando el dato no existe, esperar que el schema atrape sumas o ubicación de campos, reintentar sin error específico, omitir el campo de seguimiento, no poner límite de reintentos, mezclar errores resolubles e irresolubles, no registrar resultados (Guía PDF p. 208; Guía PDF p. 209).
- **Contradicción entre fuentes:** ante un error irresoluble, la guía dice no reintentar y ajustar el input o el schema (Guía PDF p. 199), mientras la web dice marcar para revisión humana o devolver null si el schema lo permite (web 4.4); prevalece la guía, y la guía también enruta a revisión humana los registros que superan el límite (Guía PDF p. 206). Q67 opción D (hacer el campo opcional) se descarta como sustituto del diagnóstico (Q67). Además, la web no fija un número de reintentos, mientras la guía recomienda dos a tres (Guía PDF p. 206).

## Tarea 4.5 — Design efficient batch processing strategies (Diseñar estrategias eficientes de procesamiento por lotes)

> Prioridad de estudio: Messages API vs Message Batches API (0% en los intentos 1 y 2)

### Messages API (síncrona) vs Message Batches API

**Concepto:** La Messages API síncrona envía una petición y espera su respuesta; la Message Batches API recibe muchas peticiones en un envío y devuelve los resultados después (web 4.5). La regla de decisión es la latencia tolerada: si algo o alguien deja de trabajar mientras espera el resultado, se usa síncrona; si no, batch (Guía PDF p. 153; Guía PDF p. 212).

**Ejemplos de uso (3, cortos):**
1. Pre-merge checks en CI/CD y feedback de code review en tiempo real: síncrona, porque el desarrollador está bloqueado (web 4.5; Guía PDF p. 153).
2. Informes nocturnos de deuda técnica, resúmenes semanales de auditoría de código, generación nocturna de tests, extracción de documentos en lote: batch (web 4.5).
3. Informe de facturación mensual consumido a la mañana siguiente: batch, porque la latencia es irrelevante (Guía PDF p. 153; Guía PDF p. 213).

**Qué NO hacer:**
- No pasar todo a batch solo por el ahorro del 50%: el ahorro es irrelevante si el flujo está bloqueado (Guía PDF p. 212; Q11).
- No decidir por volumen: lo que decide es quién o qué está esperando, no el volumen (Guía PDF p. 213).
- No usar batch para un paso de pipeline cuyo paso siguiente depende del resultado (Guía PDF p. 153; Guía PDF p. 212).

**Posible confusión con otros conceptos:**
- Síncrona vs batch por "preferencia" — la elección depende de lo que el trabajo necesita, no de preferencias (Guía PDF p. 211).
- Chatbot interactivo — síncrona, el usuario espera en pantalla (Guía PDF p. 212).

### Hechos clave de la Message Batches API

**Concepto:** Es procesamiento asíncrono de muchas peticiones juntas que cobra el 50% del precio estándar a cambio de aceptar un retraso (Guía PDF p. 211; Guía PDF p. 221). Procesa dentro de una ventana de hasta 24 horas, sin SLA de latencia garantizado (web 4.5; Guía PDF p. 154).

**Ejemplos de uso (3, cortos):**
1. Se envía un batch como una única llamada con un array de peticiones; cada una lleva `custom_id`, `model`, `max_tokens` y `messages` (Guía PDF p. 209).
2. El sistema registra el ID del batch y la hora de envío, consulta el estado periódicamente (polling) y al completarse recupera los resultados (Guía PDF p. 209; Guía PDF p. 210).
3. Los resultados están disponibles 29 días tras crear el batch; un batch se limita a 100,000 peticiones o 256 MB, lo que ocurra primero (Guía PDF p. 215; Guía PDF p. 216).

**Qué NO hacer:**
- No asumir que los resultados llegan rápido porque a menudo lo hacen: la mayoría termina en menos de una hora, pero el sistema debe diseñarse para la ventana completa (Guía PDF p. 154; Guía PDF p. 209; web 4.5).
- No hacer polling continuo: se sondea a un intervalo razonable, como cada pocos minutos (Guía PDF p. 209).
- No esperar que un batch acorte su ventana: la ventana la gestiona Anthropic y no puede acortarse a demanda (Q65).

```typescript
// Síncrona — el desarrollador espera
const preMergeReview = await client.messages.create({
  model: "claude-sonnet-5-5",
  max_tokens: 4096,
  messages: [{ role: "user", content: prDiffContent }]
});

// Batch — resultados consumidos mañana
const batchRequest = await client.messages.batches.create({
  requests: technicalDebtDocuments.map((doc, i) => ({
    custom_id: `debt-report-${i}`,
    params: {
      model: "claude-sonnet-5-5",
      max_tokens: 4096,
      messages: [{ role: "user", content: doc }]
    }
  }))
});
```
(web 4.5)

**Posible confusión con otros conceptos:**
- "Garantiza procesar en 24 horas" vs "sin SLA de latencia" — la ventana de 24 h es un máximo, no una garantía de entrega; un batch que no termina en ese plazo vuelve como `expired` (web 4.5; Guía PDF p. 215).

### Límite de multi-turn tool calling en batch

**Concepto:** El batch no soporta multi-turn tool calling dentro de una misma petición: el modelo no puede ejecutar herramientas a mitad de la petición y seguir procesando con sus resultados (web 4.5; Guía PDF p. 154). Los flujos agénticos que requieren llamar herramientas, recibir resultados y continuar deben usar la API síncrona (Guía PDF p. 154; Guía PDF p. 212).

**Ejemplos de uso (3, cortos):**
1. Un agentic tool loop: síncrona, porque exige intercambio multi-turno (Guía PDF p. 212; Guía PDF p. 213).
2. Un trabajo nocturno que consulta una base de datos de tarifas a mitad de un documento: ese paso se ejecuta de forma síncrona (web 4.5).
3. Un paso que requiere una herramienta se resuelve síncrono, o antes del envío o entre batches (web 4.5).

**Qué NO hacer:**
- No definir herramientas esperando que el modelo las llame a mitad de la petición del batch (web 4.5).
- No procesar resultados de herramientas y continuar la conversación dentro del mismo ítem del batch (web 4.5).
- No ejecutar bucles agénticos dentro de una sola petición batch (web 4.5; Guía PDF p. 217).

**Posible confusión con otros conceptos:**
- Server tools vs client tools — la web indica que la documentación actual de Anthropic (comprobada el 6 de octubre de 2026) ejecuta server tools en batch (pueden devolver `stop_reason: "pause_turn"`), mientras que las client tools terminan la petición en `tool_use` (web 4.5). Para el examen se responde según la guía (web 4.5).

### custom_id y correlación de resultados

**Concepto:** `custom_id` es una etiqueta única asignada a cada petición para casar cada resultado con su documento o registro de origen (Guía PDF p. 213). Es necesario porque los resultados no vuelven en el orden de entrada; se casa siempre por `custom_id`, nunca por posición (Guía PDF p. 153; Guía PDF p. 210).

**Ejemplos de uso (3, cortos):**
1. Usar como `custom_id` un ID de documento o clave primaria de base de datos, lo que elimina una tabla de búsqueda aparte (Guía PDF p. 214).
2. Guardar el mapeo `custom_id` → registro antes de enviar, para reconstruir qué se envió si el sistema falla (Guía PDF p. 214).
3. Identificar los ítems fallidos parseando los resultados y leyendo sus `custom_id` (web 4.5; Guía PDF p. 210).

**Qué NO hacer:**
- No casar resultados por posición: el emparejamiento por posición se rompe (Guía PDF p. 213).
- No repetir `custom_id` dentro de un batch: los duplicados producen un emparejamiento impredecible (Guía PDF p. 214; Guía PDF p. 217).

### Manejo de fallos parciales

**Concepto:** Un batch parcialmente fallido no es un batch fallido, sino un resultado normal que el sistema debe manejar (Guía PDF p. 213). Se identifican los fallos por `custom_id` y se reenvían solo los fallidos, con modificaciones (web 4.5; Q65).

**Ejemplos de uso (3, cortos):**
1. Si fallan 100 de 10,000 ítems, se reenvían solo esos 100 (Guía PDF p. 214).
2. Un ítem demasiado grande se divide en chunks; cada chunk va como petición independiente con su propio `custom_id` y luego se reensamblan los resultados (Guía PDF p. 214; Guía PDF p. 215).
3. Para documentos con estructura inusual se simplifica el prompt de extracción o se añaden ejemplos few-shot específicos del formato (web 4.5).

Tabla de fallos y respuesta correcta (Guía PDF p. 215):
- Ítem con error: reenviar con el mismo `custom_id`.
- Ítem `expired`: reenviar y considerar dividir el batch.
- Ítem demasiado grande: chunking y reenvío de los chunks.
- Batch completo `expired`: reenviar dividido en batches más pequeños.

El código de la web trata `errored` y `expired` como fallos y reenvía con sufijo `-retry-1` y `max_tokens` aumentado (web 4.5):

```typescript
for await (const result of client.messages.batches.results(batchId)) {
  if (result.result.type === "errored" || result.result.type === "expired") {
    failedIds.push(result.custom_id);
  }
}
```

**Qué NO hacer:**
- No reenviar el batch completo: se paga de nuevo por lo ya exitoso (web 4.5; Guía PDF p. 214; Q65).
- No reintentar tal cual un ítem que falló por tamaño: fallará otra vez por la misma razón (Guía PDF p. 214).
- No enviar un único batch muy grande en periodos de carga alta: aumenta el riesgo de expiración; dividir en batches menores lo reduce (Guía PDF p. 214).

**Posible confusión con otros conceptos:**
- Ítem `errored` vs `expired` — el expirado no se procesó en absoluto y se reenvía desde cero (Guía PDF p. 214).

### SLA y frecuencia de envío

**Concepto:** Un SLA en batch exige planificar para la ventana completa de 24 horas, no para el tiempo típico (Guía PDF p. 215). La relación es: intervalo de envío + 24 h máximo del batch ≤ SLA (Slides PDF p. 1254).

**Ejemplos de uso (3, cortos):**
1. SLA de 30 h: 30 − 24 = 6 h de buffer para recopilar peticiones, validar entradas o absorber retrasos; enviar cada 4 h mantiene siempre un batch en curso (web 4.5).
2. Enviar cada 6 h no deja margen: un documento que llega justo tras un envío espera 6 h y luego 24 h, es decir, las 30 h completas (web 4.5).
3. Un batch enviado a las 23:00 con entrega a las 9:00 solo tiene diez horas de margen; si tarda 24 h, se incumple (Guía PDF p. 215).

**Qué NO hacer:**
- No enviar demasiado cerca del deadline (Guía PDF p. 216).
- No omitir un buffer: la guía lo define como tiempo para absorber las 24 h y dejar espacio para al menos un reenvío (Guía PDF p. 216).
- No olvidar que la frecuencia de envío es la palanca; el techo de 24 h no lo es: el ejemplo de la slide llega a 48 h en total, 18 h por encima del SLA de 30 h (Slides PDF p. 1258).

### Refinar prompts con una muestra antes del batch

**Concepto:** La estrategia más rentable es refinar los prompts con un conjunto de muestra antes de enviar grandes volúmenes (web 4.5). La tasa de éxito en primera pasada es la proporción de ítems que devuelven un resultado válido sin reenvío (Guía PDF p. 216).

**Ejemplos de uso (3, cortos):**
1. Tomar 5-10 documentos representativos de formatos, casos límite y tipos, iterar el prompt, los few-shot y el esquema, y luego enviar el batch completo (web 4.5).
2. Con 1,000 documentos: 90% de éxito implica 100 reintentos; 60% implica 400, cuatro veces el coste de reenvío (web 4.5).
3. Probar una sola petición con la Messages API antes del batch completo para detectar errores de validación (Guía PDF p. 216).

**Qué NO hacer:**
- No enviar un gran volumen con un prompt sin probar: provoca errores de validación generalizados y reenvíos caros (Guía PDF p. 216; Guía PDF p. 217).

### Prompt caching con pre-warming

**Concepto:** Con un system prompt compartido (p. ej., 8,000 tokens de guías de revisión), el prompt caching reduce más el coste, pero las peticiones del batch pueden no ejecutarse cercanas en el tiempo y la caché expirar antes de las últimas (Guía PDF p. 154). La solución es añadir al inicio de cada batch peticiones de pre-warming con `max_tokens: 0`, que cuestan casi nada y siembran la caché (Guía PDF p. 154).

**Ejemplos de uso (3, cortos):**
1. Batch de revisiones de migraciones con un system prompt compartido de 8,000 tokens (Guía PDF p. 154).
2. Pregunta con baja tasa de aciertos de caché concentrada en peticiones "procesadas más tarde en la ventana del batch": pre-warming (Guía PDF p. 154).
3. Peticiones `max_tokens: 0` al comienzo de cada batch para poblar la caché (Guía PDF p. 154).

**Posible confusión con otros conceptos:**
- Ampliar el TTL de la caché — mecanismo distinto (Guía PDF p. 154).
- Dividir en batches secuenciales — añade latencia (Guía PDF p. 154).
- Mover los cache breakpoints — objetivo equivocado (Guía PDF p. 154).

### Trampas del examen

- Cambiar todo a batch por el ahorro del 50% (Q11): los flujos bloqueantes (pre-merge, revisiones en tiempo real) deben seguir síncronos porque el batch no tiene SLA de latencia y puede tardar hasta 24 h (Q11; web 4.5; Guía PDF p. 212).
- Opción B de Q11 (batch para ambos con polling de estado): falla porque confiar en una finalización "a menudo más rápida" no es aceptable para flujos bloqueantes (Q11).
- Opción C de Q11 (síncrona para ambos "por problemas de orden"): falla por un error conceptual, ya que los resultados se correlacionan con `custom_id` (Q11).
- Opción D de Q11 (batch para ambos con timeout y fallback a tiempo real): sigue enviando a batch un flujo bloqueante, que la explicación de Q11 declara inadecuado; la correcta es A, batch solo para el informe nocturno (Q11; web 4.5).
- Asumir que los resultados llegan rápido porque suelen hacerlo: se diseña según el máximo de 24 h (web 4.5; Guía PDF p. 154).
- Q65, opción A (reenviar el batch completo): desperdicia el ahorro del 50% al reprocesar documentos exitosos (Q65).
- Q65, opción C (acortar la ventana de procesamiento): las ventanas las gestiona Anthropic y no se acortan a demanda (Q65).
- Q65, opción D (volver a tiempo real por ser auditoría de cumplimiento): demasiado conservadora; una auditoría semanal tolerante a latencia es apta para batch. La correcta es B: `custom_id`, identificar los errores y reenviar solo esos documentos (Q65).
- Para reducir coste por token con trabajo no bloqueante y el mismo modelo, la respuesta es Message Batches API; distractores: peticiones paralelas en tiempo real (la concurrencia no reduce el coste por token), un modelo más pequeño (cambia de nivel de modelo) o combinar peticiones (otro modelo de costes) (Guía PDF p. 153).
- Esperar un bucle de herramientas dentro de una petición batch: no está soportado (Guía PDF p. 217; web 4.5).
- Casar resultados por orden, usar `custom_id` duplicados, no considerar la ventana de 24 h en el SLA o no reservar ventana de reenvío (Guía PDF p. 217; Guía PDF p. 216).

- **Contradicción entre fuentes:** (1) Sobre herramientas, la guía dice que el batch no soporta multi-turn tool calling y la web añade que la documentación actual ejecuta server tools en batch y solo las client tools terminan en `tool_use`; prevalece la guía (Guía PDF p. 154; web 4.5). (2) Sobre el estado de finalización, la web sondea hasta `processing_status` igual a `"ended"` y la guía habla de estado `completed`; prevalece la guía (web 4.5; Guía PDF p. 209). (3) La guía afirma que la API "garantiza" procesar en 24 h mientras la web indica que 24 h es un máximo y no una garantía de entrega; en ambas se concluye que no hay SLA de latencia más allá de esa ventana (Guía PDF p. 209; Guía PDF p. 212; web 4.5).

## Tarea 4.6 — Design multi-instance and multi-pass review architectures (Diseñar arquitecturas de revisión multi-instancia y multi-pasada)

### Self-review limitation (limitación de la autorrevisión)

**Concepto:** Self-review es que el modelo revise su propia salida en la misma sesión; conserva el razonamiento de la generación, por lo que es menos probable que cuestione sus propias decisiones (Guía PDF p. 159; Guía PDF p. 217; web 4.6). No es un problema de prompt engineering que se resuelva con mejores instrucciones, sino una limitación arquitectónica de cómo funciona el contexto de la conversación (Guía PDF p. 159).

**Ejemplos de uso (3, cortos):**
1. Claude genera código y luego lo revisa en la misma sesión: el mismo razonamiento sigue en el contexto y sesga hacia confirmar decisiones previas (Guía PDF p. 159).
2. Un módulo de 300 líneas revisado en la misma sesión devuelve "looks good" con sugerencias de estilo y pasa por alto dos errores lógicos que un colega detecta (Q66).
3. En el ejemplo del broker hipotecario, si Claude contó una transferencia grande como salario, la revisión en la misma sesión conserva ese motivo y probablemente apruebe la cifra otra vez (web 4.6).

**Qué NO hacer:**
- No pedir "review more carefully" en la misma sesión: el sesgo de razonamiento permanece (Guía PDF p. 160; web 4.6).
- No usar extended thinking como sustituto de la revisión independiente: opera en el mismo contexto con los mismos sesgos (Guía PDF p. 160; web 4.6).
- No tratar la self-review como equivalente a una revisión externa: son fundamentalmente distintas en lo que pueden detectar (Guía PDF p. 160).

**Posible confusión con otros conceptos:**
- Self-review (misma sesión) — sirve para comprobaciones rápidas de bajo overhead, pero no se debe confiar en ella para defectos sutiles (Guía PDF p. 159; Guía PDF p. 217).
- Independent review instance — revisa con contexto fresco y sin sesgo de generación (Guía PDF p. 160).

### Independent review instance (instancia de revisión independiente)

**Concepto:** Una instancia independiente es una invocación separada de Claude, sin el contexto de razonamiento previo, que evalúa la salida solo por sus méritos (web 4.6; Guía PDF p. 159). Por no tener convicción previa, es igualmente propensa a cuestionar cada decisión (Guía PDF p. 159).

**Ejemplos de uso (3, cortos):**
1. Una segunda instancia de Claude Code revisa los cambios sin ver el razonamiento del generador (Guía PDF p. 159).
2. Una llamada nueva a la API con solo el código generado en el mensaje del usuario, sin el turno previo del assistant (web 4.6).
3. En el broker, una instancia nueva revisa la extracción de ingresos y gastos sin conocer por qué se eligió cada valor (web 4.6).

```typescript
// Correct: independent review instance
const review = await client.messages.create({
  messages: [
    {
      role: "user",
      content: `Review this code for bugs, security issues, and edge cases:\n\n${generatedCode}`
    }
    // Fresh instance — no prior reasoning context
  ]
});
```

**Qué NO hacer:**
- No añadir instrucciones explícitas de autorrevisión: Claude ya evaluó y concluyó que su enfoque era correcto, y pedirlo otra vez no aporta perspectiva fresca (Guía PDF p. 160).
- No añadir archivos de tests exhaustivos como solución a este problema: no abordan la retención del razonamiento (Guía PDF p. 160).
- No añadir criterios de revisión más explícitos a la sesión de generación (Q68; Q66).

### Multi-pass review: per-file local pass + cross-file integration pass

**Concepto:** Multi-pass review divide una revisión grande en pasadas enfocadas, cada una con un trabajo estrecho y bien definido (Guía PDF p. 217). La pasada 1 revisa cada archivo por separado con un prompt enfocado (profundidad consistente); la pasada 2 recibe todos los hallazgos por archivo y comprueba flujo de datos entre módulos, uso consistente de APIs, conflictos de dependencias y contradicciones en los propios hallazgos (web 4.6; Guía PDF p. 218).

**Ejemplos de uso (3, cortos):**
1. Fase 1 por archivo: revisar cada archivo cambiado en aislamiento (bugs locales, seguridad, manejo de errores) con salida de ubicación, problema, severidad y confianza; fase 2: con una instancia fresca, revisar shared state, data flow y desajustes de contrato entre archivos (Guía PDF p. 218).
2. Un PR de 14 archivos: análisis individual de cada archivo y luego una pasada separada de integración sobre el flujo de datos entre archivos (Q12).
3. En el broker, un salario de la nómina que difiere de los abonos del extracto bancario solo lo detecta la pasada de integración (web 4.6).

```typescript
// Pass 1: Per-file analysis
const perFileFindings = await Promise.all(
  files.map(file =>
    client.messages.create({
      messages: [{
        role: "user",
        content: `Review this file for local issues (bugs, security, logic errors):\n\n${file.content}`
      }]
    })
  )
);

// Pass 2: Cross-file integration
const integrationReview = await client.messages.create({
  messages: [{
    role: "user",
    content: `Given these per-file findings, identify cross-file issues:\n` +
      `- Data flow inconsistencies between modules\n` +
      `- Contradictory patterns flagged in different files\n` +
      `- API contract violations across service boundaries\n\n` +
      `Findings:\n${JSON.stringify(perFileFindings)}`
  }]
});
```

**Qué NO hacer:**
- No esperar que la pasada por archivo detecte problemas entre archivos (Guía PDF p. 218).
- No omitir la pasada de integración: deja sin encontrar los bugs de integración (Guía PDF p. 218; Guía PDF p. 219).
- No hacer una sola pasada sobre muchos archivos: reparte la atención demasiado (Guía PDF p. 218).

**Posible confusión con otros conceptos:**
- Per-file local pass — bugs locales y problemas dentro del archivo, con profundidad consistente (Guía PDF p. 218).
- Cross-file integration pass — flujo de datos e interacción entre archivos (Guía PDF p. 218).

### Attention dilution (dilución de atención) y ventana de contexto

**Concepto:** Attention dilution es la atención desigual cuando una sola pasada revisa demasiado a la vez (web 4.6). Síntomas: feedback detallado en unos archivos y superficial en otros, bugs obvios omitidos en medio de la revisión y hallazgos contradictorios (marcar un patrón en un archivo y aprobar código idéntico en otro) (web 4.6; Q12). El problema es la calidad de la atención, no el tamaño del contexto (web 4.6).

**Ejemplos de uso (3, cortos):**
1. Un PR de 14 archivos con feedback inconsistente se reestructura en pasadas enfocadas (Q12).
2. En el broker, una pasada única revisa línea a línea la primera nómina, hojea el tercer extracto y marca una transferencia que aprueba en otro sitio (web 4.6).
3. Ejercicio de la web: ejecutar un prompt de pasada única sobre un PR simulado de 10 archivos para documentar profundidad inconsistente, problemas omitidos y hallazgos contradictorios (web 4.6).

**Qué NO hacer:**
- No cambiar a un modelo de nivel superior con ventana de contexto mayor: una ventana más grande no resuelve la calidad de atención (web 4.6; Q12).
- No exigir que un problema aparezca en al menos dos de tres ejecuciones completas: suprimiría bugs reales que se detectan solo de forma intermitente (Q12; Guía PDF p. 218).
- No pedir a los desarrolladores que dividan los PR en envíos de 3-4 archivos: traslada la carga a los desarrolladores sin mejorar el sistema (Q12).

### Confidence-based routing y calibración

**Concepto:** El modelo informa de un confidence level con cada hallazgo y los de baja confianza se envían a revisión más cercana, concentrando el tiempo limitado del revisor donde más se necesita (Guía PDF p. 218). El score es la certeza que el propio modelo declara, no su exactitud (web 4.6). Alta confianza se reporta directamente a los desarrolladores; baja confianza va a revisión humana (web 4.6).

**Ejemplos de uso (3, cortos):**
1. Un hallazgo de "may be a one-off bonus" con baja confianza va a un asesor (web 4.6).
2. Cualquier hallazgo con confianza por debajo del umbral se envía a revisión humana (Guía PDF p. 218).
3. Un hallazgo con `"confidence": 0.65` se enruta con `"route": "human_review"` (web 4.6).

```json
{
  "finding": "Potential race condition in order processing",
  "severity": "major",
  "confidence": 0.65,
  "reasoning": "The lock acquisition pattern appears correct but the unlock timing depends on an async callback whose ordering I cannot fully verify.",
  "route": "human_review"
}
```

**Qué NO hacer:**
- No usar confidence scores sin calibrar para decisiones automatizadas: es un anti-patrón (web 4.6).
- No fijar umbrales sin datos: calibrar con labelled validation sets (ejemplos con respuesta conocida) y medir cuánto sigue la confianza informada a la exactitud real, y luego ajustar los umbrales (web 4.6).

**Posible confusión con otros conceptos:**
- Raw confidence score — no calibrado, poco fiable para decisiones automatizadas (web 4.6).
- Calibrated confidence threshold — validado contra conjuntos etiquetados, adecuado para routing (web 4.6).

### Arquitectura de producción combinada y cuándo compensa el coste

**Concepto:** Una arquitectura de revisión de producción combina: generación (primera instancia), revisión por archivo con instancias independientes, revisión de integración con una instancia separada, confidence routing hacia revisión humana y un calibration loop con labelled validation sets (web 4.6). Multi-instance y multi-pass son patrones complementarios: juntos dan revisiones más consistentes, completas y difíciles de engañar (Guía PDF p. 217).

**Ejemplos de uso (3, cortos):**
1. Broker: una extracción, una comprobación por documento, una comprobación entre documentos y un asesor para los hallazgos dudosos (web 4.6).
2. Generación y revisión nunca se hacen por la misma sesión (Guía PDF p. 217).
3. Compensa cuando la calidad de la revisión afecta a la fiabilidad en producción: pipelines CI/CD, extracción financiera, análisis de compliance (web 4.6).

**Qué NO hacer:**
- No olvidar que es más cara que una revisión de una sola pasada; el coste solo se justifica si los problemas omitidos tienen consecuencias posteriores (web 4.6).

### Trampas del examen

- Elegir la self-review en la misma sesión como estrategia viable: el modelo conserva su razonamiento y cuestiona menos sus decisiones; la instancia independiente es mucho más eficaz con problemas sutiles (web 4.6; Guía PDF p. 160). Q66 y Q68 fallan en A/C/D: ventana de contexto menor (A de Q66), criterios más explícitos en la misma sesión (C de Q66; A de Q68), mismo nivel de modelo (D de Q66) o modelo mayor (D de Q68) no eliminan el sesgo del razonamiento retenido (Q66; Q68).
- Q68 C: revisar inmediatamente tras la generación gestiona la longitud del contexto pero no elimina el sesgo del generador (Q68).
- Distractores de la guía cuando Claude consideró y descartó los casos durante la generación: extended thinking (mismo contexto, mismos sesgos), archivos de tests completos (no abordan la retención del razonamiento) e instrucciones explícitas de self-review (Guía PDF p. 160).
- Una sola pasada para revisiones multi-archivo grandes: profundidad inconsistente, bugs omitidos y hallazgos contradictorios; la respuesta correcta es la pasada por archivo más la de integración (Q12; web 4.6; Guía PDF p. 219).
- Q12 B (dividir el PR en 3-4 archivos), C (modelo superior con ventana mayor) y D (tres pasadas completas, solo issues en al menos dos): fallan porque trasladan la carga, no mejoran la calidad de atención o suprimen bugs reales intermitentes (Q12; Guía PDF p. 218).
- Esperar que la pasada por archivo capture problemas entre archivos u omitir la pasada de integración (Guía PDF p. 218).
- Depender del acuerdo entre ejecuciones completas repetidas o de una ventana de contexto mayor (Guía PDF p. 219).
- Usar confidence scores sin calibrar para el routing automatizado: hay que calibrar umbrales con labelled validation sets (web 4.6).
- Elegir "switch to a higher-tier model with a larger context window" para un problema de atención: las ventanas grandes retienen más texto pero la atención sigue siendo desigual entre archivos (web 4.6).
- **Contradicción entre fuentes:** la guía (Guía PDF p. 159) presenta la limitación de self-review como tema de "Domain 3", mientras que la tarea 4.6 figura en el Dominio 4 (Slides PDF p. 1081; web 4.6); prevalecen guía y banco, y esta tarea se estudia como 4.6. No hay contradicción de contenido sobre la solución (instancia independiente) entre guía, banco y web.

## Ideas clave

- Los criterios explícitos (qué reportar y qué omitir) son el cambio de prompt más eficaz para la precisión; "be conservative" y "only report high-confidence findings" no definen el límite (Guía PDF p. 150, 180; web 4.1; Q55).
- La confianza autorreportada del LLM está mal calibrada: un umbral (p. ej. 80%) suprime hallazgos correctos pero inciertos y conserva los erróneos pero seguros (Guía PDF p. 150; Q55).
- Una categoría con muchos falsos positivos erosiona la confianza en todas; se desactiva temporalmente mientras se refina con criterios y ejemplos de código (Guía PDF p. 181; web 4.1).
- La severidad se calibra con ejemplos de código por nivel, no con prosa ni tablas en CLAUDE.md; `detected_pattern` permite analizar descartes por patrón (Guía PDF p. 150, 151; Q64).
- Few-shot (2 a 4 ejemplos diversos, con razonamiento, en `<example>`) es la técnica más eficaz para formato inconsistente y casos ambiguos; los contraejemplos con explicación definen fronteras (web 4.2; Slides PDF p. 1101; Guía PDF p. 183, 225-226; Q58, Q59, Q60).
- Tool use con JSON schema es el método más fiable para salida estructurada y elimina errores de sintaxis, pero no los semánticos (suma que no cuadra, valor en campo equivocado) (web 4.3; Guía PDF p. 88; Q61).
- `tool_choice`: `auto` puede omitir la tool, `any` obliga a llamar a una tool que el modelo elige (tipo de documento desconocido), `tool` fuerza una concreta y `none` impide llamar tools (Guía PDF p. 86-88; Q62).
- Un campo required que la fuente puede no traer induce fabricación; usar nullable u optional, y `unclear`/`other` más detalle en los enums (web 4.3; Guía PDF p. 187, 191-193).
- El retry solo funciona con errores resolubles y si incluye documento original, extracción fallida y error de validación específico; los datos ausentes van a revisión humana o null, y todo loop lleva un límite de dos a tres reintentos (Guía PDF p. 199, 200, 206; Q63, Q67).
- Message Batches API: 50% más barata, ventana de hasta 24 horas sin SLA de latencia, sin multi-turn tool calling; para flujos bloqueantes se usa la API síncrona, los resultados se casan por `custom_id` y solo se reenvían los ítems fallidos (Guía PDF p. 153-154, 211-215; Q11, Q65).
- Para un SLA se planifica la ventana completa de 24 h (intervalo de envío + 24 h ≤ SLA) y se refinan los prompts con una muestra antes de enviar el batch (Slides PDF p. 1254; web 4.5; Guía PDF p. 215-216).
- La self-review en la misma sesión conserva el razonamiento de la generación; para defectos sutiles se usa una instancia independiente, y para PRs grandes una pasada por archivo más una de integración, con confidence routing calibrado con labelled validation sets (Guía PDF p. 159-160, 218; web 4.6; Q12, Q66, Q68).
