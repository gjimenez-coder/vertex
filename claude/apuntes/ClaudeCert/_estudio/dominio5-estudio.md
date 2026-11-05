# Context Management & Reliability (Gestión de contexto y fiabilidad) — Estudio

## Tarjetas de repaso

**1.**
P: ¿Qué es la context window y cómo debe gestionarse?
R: Es todo lo que Claude lee en una request (instrucciones, conversación, resultados de herramientas, documentos). Es finita y se gestiona como un presupuesto de tokens; el context rot degrada la fiabilidad antes de que se agote (Tarea 5.1).

**2.**
P: ¿Por qué falla la progressive summarisation con datos transaccionales?
R: Sustituye turnos por un resumen más corto y destruye valores numéricos, fechas, porcentajes e identificadores (Tarea 5.1, Progressive summarisation).

**3.**
P: ¿Qué es un persistent case facts block?
R: Un bloque estructurado con los hechos transaccionales (importes, fechas, números de pedido, estados), incluido en cada prompt, fuera del historial resumido y nunca resumido. Se reinyecta tras la compaction (Tarea 5.1).

**4.**
P: ¿Qué es el efecto "lost in the middle" y cómo se mitiga?
R: Los modelos procesan mejor el principio y el final de entradas largas y pueden pasar por alto el medio. Se mitiga con un resumen de hallazgos clave al principio y secciones con cabeceras explícitas; es un arreglo estructural, no un recordatorio en el prompt (Tarea 5.1).

**5.**
P: ¿Qué hace el tool result trimming y por qué?
R: Recorta los resultados de herramientas a los campos relevantes antes de que entren en el historial, porque una vez dentro permanecen en todos los turnos siguientes (Tarea 5.1).

**6.**
P: ¿Qué diferencia hay entre context editing, compaction y memory tool?
R: Context editing limpia contenido específico (tool results obsoletos); compaction resume toda la conversación; el memory tool guarda información en archivos fuera de la ventana y preserva lo importante antes de liberar espacio (Tarea 5.1).

**7.**
P: ¿Qué hace el prompt caching y qué no hace?
R: Reutiliza un prefijo estable marcado con `cache_control`, reduciendo coste y latencia. No reduce la ventana ni sustituye a limpiar o resumir (Tarea 5.1).

**8.**
P: ¿Cómo se trata una petición explícita de un humano?
R: Se escala de inmediato, sin intentar resolver ni investigar antes. Es una regla absoluta (Tarea 5.2).

**9.**
P: ¿Qué diferencia hay entre una brecha de política y una violación de política?
R: Una brecha es que la política guarda silencio y se escala a un humano; una violación tiene respuesta documentada y el agente la responde sin escalar (Tarea 5.2).

**10.**
P: ¿Por qué son poco fiables el sentiment y la confianza autorreportada como triggers de escalación?
R: La frustración no se correlaciona con la complejidad del caso, y la confianza autorreportada está mal calibrada (el modelo no sabe lo que no sabe). Se usan criterios explícitos con few-shot en el system prompt (Tarea 5.2).

**11.**
P: ¿Qué debe incluir un warm handoff a un humano?
R: Motivo de la escalación, case facts, pasos ya realizados, estado actual y acción recomendada (Tarea 5.2).

**12.**
P: ¿Qué se hace cuando una herramienta devuelve varias coincidencias de clientes?
R: Se piden identificadores adicionales (correo, teléfono, número de pedido); nunca se elige por heurística (Tarea 5.2).

**13.**
P: ¿Qué diferencia hay entre access failure y valid empty result?
R: En un access failure la herramienta no pudo alcanzar su fuente y la búsqueda no se ejecutó (error estructurado, a veces retryable). En un valid empty result se consultó la fuente y no hubo coincidencias (éxito con resultado vacío) (Tarea 5.3).

**14.**
P: ¿Qué son silent suppression y workflow termination?
R: Silent suppression devuelve resultados vacíos marcados como éxito (invisible). Workflow termination termina todo el pipeline ante un solo fallo, desperdiciando el trabajo de los demás agentes (Tarea 5.3).

**15.**
P: ¿Qué debe contener un error estructurado de un subagent?
R: Según la web: tipo de fallo, qué se intentó, resultados parciales y enfoques alternativos. Según la guía: category, description, retryable y source (Tarea 5.3).

**16.**
P: ¿Qué es coverage honesty?
R: Reportar qué se completó, qué no y por qué. Un resultado parcial con anotaciones honestas vale más que uno que parece completo con brechas ocultas o un fallo total (Tarea 5.3).

**17.**
P: ¿Qué es la context degradation en la exploración de código y cómo se mitiga?
R: Pérdida progresiva de hallazgos específicos porque la salida verbosa reciente domina el contexto; no es agotamiento de tokens. Se mitiga con scratchpad files, subagents con contexto aislado, summary injection entre fases, `/compact` proactivo y state manifests (Tarea 5.4).

**18.**
P: ¿Cuál es el valor principal de un subagent en la exploración de código?
R: El aislamiento de contexto, no la paralelización: explora de forma verbosa en su propio contexto y devuelve un resumen estructurado (Tarea 5.4).

**19.**
P: ¿Por qué la aggregate accuracy es una trampa y qué la corrige?
R: Una cifra global puede ocultar segmentos que fallan gravemente. Se corrige validando por document type y field segment y con stratified sampling (Tarea 5.5).

**20.**
P: ¿Qué es un claim-source mapping y qué es source laundering?
R: El mapping vincula una afirmación con sus fuentes (claim, source URL, document name, relevant excerpt, publication date). Source laundering es pasar un hecho a otro agente sin atribución, de modo que se presente como hallazgo propio (Tarea 5.6).

## Preguntas de autoevaluación

**1.** Un agente dice "el sobrecargo del mes pasado" sin el importe $847.50. ¿Qué solución es correcta y por qué fallan `/compact`, una ventana mayor y releer el historial?
R: Un case facts block incluido al inicio de cada prompt. `/compact` puede perder precisión en hechos transaccionales; una ventana mayor no evita la progressive summarisation; releer el historial es poco práctico y no evita que los hechos se pierdan al crecer el contexto (Tarea 5.1, Trampas del examen, Q69).

**2.** Una síntesis omite o contradice hallazgos de las secciones intermedias. ¿Cuál es la causa y la mitigación?
R: Efecto "lost in the middle". Poner un resumen de hallazgos clave al principio y secciones con cabeceras explícitas. Fallan deduplicación, subir `max_tokens` y un agente de resumen secundario (Tarea 5.1, Q70).

**3.** ¿Por qué no es suficiente instruir al summariser a conservar cada cifra literalmente?
R: En el escenario de la web ya se hizo y el $247.83 se perdió igualmente. La solución es extraer los hechos a un case facts block fuera del historial resumido (Tarea 5.1, Trampas del examen).

**4.** Un cliente pide un humano y además el agente podría resolver su problema de facturación en 2 pasos. ¿Qué se hace?
R: Se escala en la primera petición. La capacidad del agente no decide cuando hay una petición explícita; el frustration score es irrelevante y investigar primero retrasa la petición (Tarea 5.2, Q71).

**5.** Un agente tiene 55% de first-contact resolution frente a un objetivo de 80%. ¿Cuál es la primera respuesta proporcionada?
R: Añadir criterios explícitos con ejemplos few-shot al system prompt, porque ataca los límites de decisión poco claros. Fallan la confianza autorreportada, el sentiment analysis y un clasificador separado (Tarea 5.2, Q3).

**6.** Un subagent captura un timeout y devuelve `status: "success"` con `results: []`. ¿Cuál es el problema y la solución?
R: Es silent suppression: impide al coordinator tomar decisiones de recuperación y presenta trabajo incompleto como completo. La solución es devolver contexto de error estructurado. Fallan delegar la detección al synthesis agent, validar vacíos en el coordinator (puede ser un valid empty result) y subir el timeout (Tarea 5.3, Q72).

**7.** ¿Cuándo debe un subagent recuperarse localmente y cuándo propagar el error?
R: Se recupera localmente de fallos transient (reintentos, fuentes de respaldo) antes de propagar; solo se propaga lo que no puede resolver, incluyendo qué intentó y los resultados parciales (Tarea 5.3, Local recovery antes de escalar).

**8.** Tras ~90 minutos de exploración, un agente habla de "standard patterns" y contradice hallazgos de la primera hora. ¿Qué lo explica y qué se debe hacer?
R: Context degradation por salida verbosa acumulada. Escribir hallazgos en un scratchpad file y delegar las lecturas verbosas a subagents. No sirven subir `max_tokens`, rate limits, cambiar de `Read` a `Grep` ni agentes paralelos por subsistema (Tarea 5.4, Q73).

**9.** ¿Por qué `/compact` no es suficiente para preservar un hallazgo concreto entre fases?
R: Comprime el historial y puede perder el hallazgo; el scratchpad es la técnica recomendada para preservarlo. La web dice que `/compact` conserva la información importante; prevalece el banco (Tarea 5.4, Q74).

**10.** ¿Por qué los subagents de la fase 2 duplican la exploración de la fase 1 y cómo se evita?
R: Es el problema de "cold start": un subagent empieza con su contexto aislado y no ve el historial del padre. Se evita con summary injection: resumir los hallazgos de la fase 1 e inyectarlos en su contexto inicial, sin copiar la transcripción completa (Tarea 5.4, Summary injection).

**11.** Un sistema de extracción tiene 97% de precisión global. ¿Es seguro automatizar todo lo de alta confianza?
R: No. La precisión agregada puede enmascarar un rendimiento pobre en segmentos concretos. Hay que validar por document type y field segment antes de automatizar (Tarea 5.5, Q75).

**12.** ¿Por qué no se debe usar el confidence score crudo como umbral de routing?
R: Los scores crudos no están calibrados; hay que calibrarlos con un labeled validation set. Los scores se pueden aplicar a nivel de campo (Tarea 5.5, Q76).

**13.** Un informe afirma "AI adoption in healthcare reached 45% in 2024" sin fuente. ¿Qué diseño lo evita?
R: Subagentes con claim-source mappings estructurados (claim text, source URL, document name, relevant excerpt) y una síntesis que los preserva y fusiona. Una lista "Sources consulted", un log de salidas crudas o una verificación posterior no evitan la pérdida estructural de provenance (Tarea 5.6, Q77).

**14.** Dos fuentes dan 12% y 8% para el mismo hecho. ¿Cómo se maneja?
R: Se anotan ambos valores con atribución y fechas, sin promediar ni elegir en silencio. Revisar las fechas primero: una fuente nueva que actualiza a una antigua es una corrección, no un conflicto (Tarea 5.6, Manejo de conflictos, Conciencia temporal).

## Checklist

### Tarea 5.1 — Contexto de la conversación
- [ ] Tratar la ventana como presupuesto de tokens y gestionarla de forma proactiva.
- [ ] Mantener un case facts block en cada prompt, al principio de cada turno, fuera del historial resumido.
- [ ] Reinyectar el case facts block tras una compaction.
- [ ] Poner un resumen de hallazgos clave al principio del input agregado y usar cabeceras por sección.
- [ ] Recortar los tool results a los campos relevantes antes de que entren al historial.
- [ ] Hacer que los agentes upstream devuelvan datos estructurados, no razonamiento verboso.
- [ ] Guardar hechos durables en el memory tool antes de usar context editing o compaction.
- [ ] Poner el contenido estático antes del dinámico y el breakpoint `cache_control` al final del bloque estático.

### Tarea 5.2 — Escalación y ambigüedad
- [ ] Escalar de inmediato ante una petición explícita de humano.
- [ ] Distinguir brecha de política (escalar) de violación de política (rechazar sin escalar).
- [ ] Escalar por authority limits y por fallo repetido (loop detection).
- [ ] No usar sentiment ni confianza autorreportada como triggers.
- [ ] Ante frustración sin petición de humano: reconocerla y ofrecer resolución.
- [ ] Pedir identificadores adicionales ante coincidencias ambiguas.
- [ ] Añadir criterios explícitos y few-shot al system prompt antes de añadir infraestructura.
- [ ] Incluir en el traspaso: motivo, case facts, pasos realizados, estado y acción recomendada.

### Tarea 5.3 — Propagación de errores
- [ ] Devolver errores estructurados (tipo/categoría, qué se intentó, resultados parciales, alternativas, retryable).
- [ ] Distinguir access failure de valid empty result.
- [ ] No marcar como éxito un fallo de acceso (silent suppression).
- [ ] No terminar el pipeline por un solo fallo (workflow termination).
- [ ] Recuperarse localmente de fallos transient antes de propagar.
- [ ] Anotar brechas de cobertura en la salida (coverage honesty).
- [ ] Ramificar la recuperación según la categoría del error, no según el texto.

### Tarea 5.4 — Exploración de bases de código grandes
- [ ] Crear un scratchpad file desde el inicio de la sesión con clases, rutas y cadenas de dependencias concretas.
- [ ] Delegar lecturas verbosas a subagents; usar Grep/Glob para búsquedas dirigidas.
- [ ] Inyectar un resumen de la fase 1 en el contexto inicial de los subagents de la fase 2.
- [ ] Usar `/compact` de forma proactiva, junto con el scratchpad.
- [ ] Exportar un state manifest (explorado, hallazgos, fase, siguientes pasos) para recuperarse de crashes.
- [ ] Explorar por progressive discovery, no leyendo todo secuencialmente.

### Tarea 5.5 — Revisión humana y calibración de confianza
- [ ] Medir la precisión por document type y field segment, no solo la agregada.
- [ ] Calibrar los confidence scores con labeled validation sets.
- [ ] Fijar umbrales calibrados, empezar conservador y ajustarlos.
- [ ] Implementar stratified random sampling continuo, incluida la salida de alta confianza.
- [ ] Ordenar la cola de revisión por incertidumbre.
- [ ] Reducir la revisión humana solo en segmentos con precisión validada y consistente.
- [ ] Vigilar la cola: si más del 25% va a revisión, revisar umbral o modelo.

### Tarea 5.6 — Procedencia y síntesis multifuente
- [ ] Exigir los cinco campos por hallazgo: claim, source URL, document name, relevant excerpt, publication date.
- [ ] Instruir al agente de síntesis a mantener los claim-source mappings y evitar resumir en prosa.
- [ ] Preservar el mapping en cada handoff entre agentes (evitar source laundering).
- [ ] Revisar las fechas antes de tratar un desacuerdo como conflicto.
- [ ] Anotar los conflictos con ambos valores y su atribución; no promediar ni elegir en silencio.
- [ ] Respetar la jerarquía primary > secondary > tertiary y anotar la diferencia de autoridad.
- [ ] Indicar en la síntesis qué fuentes dieron datos, cuáles no tenían datos y cuáles no se pudieron alcanzar.
- [ ] Elegir el formato según el tipo de contenido (tablas, prosa, listas).
