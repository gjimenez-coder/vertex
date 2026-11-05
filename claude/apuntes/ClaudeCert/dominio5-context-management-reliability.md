# Claude Certified Architect – Foundations (CCA-F) — Anthropic (guía de examen, 2026)

## Dominio 5 — Context Management & Reliability (Gestión de contexto y fiabilidad)

> Nota de extracción: este apunte combina cinco fuentes: la guía en PDF «Tutorials Dojo Study Guide and Cheat Sheets – Claude Certified Architect Foundations (CCA-F)», las slides en PDF del curso en video (Tutorials Dojo, junio 2026), el banco de 77 preguntas de práctica «Claude Certified Architect. Foundations: Practice Exam» y las lecciones web de claudecertificationguide.com (sitio independiente de terceros, no afiliado a Anthropic). Citas: `(Guía PDF p. N)` y `(Slides PDF p. N)` usan la página del PDF; `(web N.M)` remite a la lección N.M de la web; `(QN)` remite a la pregunta N del banco. Si las fuentes se contradicen, prevalecen la guía y el banco sobre la web. Las slides tienen muchas páginas que son solo imagen y no se pudieron leer, por lo que su cobertura es parcial. Discrepancia entre fuentes sin resolver: el banco y la guía llaman al examen «CCA-F» y el banco indica 77 preguntas de práctica y una nota mínima de 720 (escala 100-1.000); la web lo llama «CCAR-F» e indica 60 preguntas en 120 minutos, aprobado con 720/1.000 y credencial válida 12 meses. No se decide cuál es la correcta.

## Lo que necesitas saber

El Dominio 5 pesa el 15% del examen y trata de cómo mantener fiable un sistema con Claude cuando la interacción se alarga o se reparte entre varios agentes. Cubre seis tareas: gestionar el contexto de la conversación (5.1), diseñar patrones de escalación y resolución de ambigüedad (5.2), propagar errores en sistemas multiagente (5.3), gestionar el contexto en la exploración de bases de código grandes (5.4), diseñar flujos de revisión humana y calibración de confianza (5.5) y preservar la procedencia de la información en la síntesis multifuente (5.6). La idea de fondo es que la context window es un presupuesto finito de tokens y que la fiabilidad se degrada (context rot) antes de que se agote (Guía PDF p. 231; Guía PDF p. 234).

Las tareas se conectan por un hilo común: los hechos críticos no deben depender de un resumen ni del historial. En 5.1 se fijan en un persistent case facts block y se recortan los tool results; en 5.4 se guardan en scratchpad files, state manifests y subagents con contexto aislado; en 5.2 el traspaso a un humano lleva case facts, pasos realizados y acción recomendada (Guía PDF p. 240); en 5.3 el error estructurado y la coverage honesty evitan que un fallo se oculte (Guía PDF p. 244); y en 5.6 los claim-source mappings conservan la atribución en cada handoff (Guía PDF p. 253). Otra línea común es decidir con criterios concretos y no con proxies: la escalación se guía por triggers explícitos y no por sentiment ni confianza autorreportada (web 5.2), y la automatización se valida por segmento y con scores calibrados, no con la precisión agregada (web 5.5; Q75; Q76).

Al terminar el dominio sabes distinguir los fallos típicos y su solución estructural: lost in the middle (resumen de hallazgos clave al principio y cabeceras), silent suppression frente a valid empty result (Q72), escalación inmediata ante una petición explícita de humano (Q71), degradación de contexto que se resuelve con scratchpad y delegación y no con una ventana mayor ni con `max_tokens` (Q73; Q74), y conflictos entre fuentes que se anotan con ambos valores y fechas sin promediar ni elegir en silencio (Guía PDF p. 252; web 5.6).

Tareas con prioridad de estudio: 5.2 (salvaguardas de orquestación: cierre en resolución o escalación, 0% en los intentos 1 y 2) y 5.5 (routing a revisión humana por confianza, 67% en el mapa de refuerzo).

## Tarea 5.1 — Manage conversation context to preserve critical information across long interactions (Gestionar el contexto de la conversación para preservar la información crítica en interacciones largas)

### Context window y token budget

**Concepto:** La context window es todo lo que Claude lee en una request: instrucciones, la conversación hasta ese momento, resultados de herramientas y documentos (web 5.1). Es la memoria de trabajo del modelo para una sola request, es finita y hay que gestionarla como un presupuesto de tokens (Guía PDF p. 230; Guía PDF p. 231).

**Ejemplos de uso (3, cortos):**
1. Un system prompt y las tool definitions son costes fijos que consumen presupuesto en cada turno; cuantas más tools, menos espacio queda para conversación y resultados (Guía PDF p. 231).
2. Un agente que verifica identidad, busca el pedido, revisa la política de reembolso, consulta el procesador de pagos y el envío acumula miles de tokens de tool output tras cinco tool calls (Guía PDF p. 230; Guía PDF p. 231).
3. Las tool definitions de muchos MCP servers conectados también se acumulan y hay que tenerlas en cuenta (Guía PDF p. 234).

**Qué NO hacer:**
- Tratar la ventana como espacio libre en lugar de un presupuesto finito (Guía PDF p. 234).
- Asumir que una ventana más grande elimina la necesidad de gestionar el contexto, porque el context rot sigue aplicando (Guía PDF p. 234).
- Atribuir el fallo de una sesión larga al prompt o al modelo antes de investigar si es un problema de gestión de contexto (Guía PDF p. 231).

**Posible confusión con otros conceptos:**
- Context rot (degradación gradual al llenarse la ventana, sin umbral exacto de tokens) — a 50-70% de uso el modelo puede perder detalles del medio; a 80%+ puede contradecirse o ignorar instrucciones (Guía PDF p. 231).
- Prompt caching — reduce coste y latencia, pero no reduce la ventana ni sustituye a limpiar o resumir (Guía PDF p. 233).

Otros puntos de la guía: el context rot hace que una ventana más llena sea menos fiable (Guía PDF p. 231); las cifras de uso son rangos aproximados y la gestión debe ser proactiva, antes de que la ventana se llene (Guía PDF p. 231). Los síntomas de sobrecarga son repetirse, olvidar instrucciones, respuestas más vagas o lentas, que el tool output domine la ventana y contradecir decisiones previas (Guía PDF p. 233). El crecimiento varía por tipo de trabajo: texto (cientos de tokens por turno), tareas con pocas tools (1-2K por tool call), lectura de archivos (1-5K por lectura) y búsquedas (2-10K por búsqueda) (Guía PDF p. 233).

### Progressive summarisation y persistent case facts block

**Concepto:** La progressive summarisation sustituye turnos anteriores por un resumen más corto y destruye sistemáticamente valores numéricos, fechas, porcentajes y expectativas del cliente (web 5.1). El patrón correcto es el persistent case facts block: un bloque estructurado con los hechos transaccionales (importes, fechas, números de pedido, estados) incluido en cada prompt, fuera del historial resumido y nunca resumido (web 5.1; Q69).

**Ejemplos de uso (3, cortos):**
1. El turno "reembolso de $247.83 por el pedido #8891 del 3 de marzo" se convierte en "Customer wants a refund for a recent order" y pierde importe, pedido y fecha; el bloque los conserva (web 5.1).
2. Un bloque marcado `[CASE FACTS]` con customer_id, plan, open_issue y constraint, que se arrastra textualmente y no se resume (Guía PDF p. 236).
3. Si el cliente plantea varios problemas, cada issue tiene su entrada con order IDs, importes y estados, como capa de contexto separada del historial resumido, para que los datos de un issue no se mezclen con otro (web 5.1; Guía PDF p. 236).

```json
{
  "caseFactsBlock": {
    "customerId": "C-4421",
    "issues": [
      {
        "orderId": "#8891",
        "orderDate": "2024-03-03",
        "refundAmount": "$247.83",
        "status": "pending_refund",
        "itemDescription": "Wireless headphones — defective"
      }
    ]
  }
}
```

**Qué NO hacer:**
- Pensar que la progressive summarisation es segura para datos transaccionales (web 5.1).
- Confiar en que un valor específico (fecha, identificador) sobreviva a cada pasada de resumen en lugar de fijarlo como durable fact; el riesgo se acumula con cada pasada (Guía PDF p. 235).
- Dejar los durable facts en el historial ordinario, donde se pierden en un resumen (Guía PDF p. 236).
- Responder a la pérdida de datos con mejores instrucciones de resumen: la respuesta apunta a un durable facts block (Guía PDF p. 235).

**Posible confusión con otros conceptos:**
- Durable facts — detalles estables necesarios en toda la tarea, siempre disponibles y nunca resumidos (Guía PDF p. 236).
- Passing history — charla turno a turno y pasos resueltos, que se puede recortar o limpiar sin riesgo (Guía PDF p. 236).

El case facts block es el patrón más importante de la gestión de la context window (web 5.1) y va al principio de cada turno nuevo, donde la atención es más fuerte (Guía PDF p. 236). Tras una compaction hay que reinyectarlo, porque si el resumen omitió un detalle crítico el modelo no sabe que existió; un resumen es un punto de partida, no el registro completo (Guía PDF p. 234; Guía PDF p. 238).

### Efecto "Lost in the Middle"

**Concepto:** Los modelos procesan de forma fiable el principio y el final de entradas largas y pueden pasar por alto, o dar menos peso, a lo que está en el medio (web 5.1; Guía PDF p. 235). El efecto es más fuerte cuanto mayor es el contexto: en un prompt corto la posición apenas importa, en uno de 100,000 tokens importa mucho (Guía PDF p. 235).

**Ejemplos de uso (3, cortos):**
1. Poner un "Key Findings Summary" al inicio del input agregado y luego cada informe bajo su propia cabecera de sección (web 5.1; Q70).
2. Colocar los hallazgos clave e instrucciones arriba con cabeceras claras, o al final del todo (Guía PDF p. 236).
3. Dejar el material de referencia largo en el medio, donde el recall exacto importa menos (Guía PDF p. 236).

```
## Key Findings Summary
- Source A: 12% market growth in renewable sector (2023)
- Source B: Patent filings increased 34% year-on-year
- Source C: Regulatory framework delayed until Q3 2025

## Detailed Findings

### Source A: Market Analysis Report
[Full details here...]
```

**Qué NO hacer:**
- Intentar arreglarlo con una instrucción del tipo "presta atención a todo": la solución es estructural, no un recordatorio en el prompt (web 5.1).
- Enterrar una instrucción clave en medio de un input largo (Guía PDF p. 238).

**Posible confusión con otros conceptos:**
- Lost in the middle (problema de atención posicional) — los hallazgos del medio se omiten aunque la ventana no esté agotada (Q70).
- Output token limit — limita la longitud de la respuesta, no la atención sobre el input (Q70).

### Tool result trimming

**Concepto:** Los tool results consumen presupuesto sin que se note; hay que recortarlos a los campos relevantes antes de que entren en el historial, porque una vez dentro permanecen en todos los turnos siguientes (web 5.1; Guía PDF p. 236).

**Ejemplos de uso (3, cortos):**
1. Un order lookup devuelve más de 40 campos y para un reembolso se necesitan 5; los otros 35 consumen tokens en cada turno (web 5.1).
2. Recortar en un hook PostToolUse o en la propia implementación de la tool, antes de que el resultado entre en el historial (web 5.1).
3. De un archivo de 500 líneas, extraer solo la función necesaria en vez de cargar todo (Guía PDF p. 236).

```python
def trim_order_result(raw_result, relevant_fields=None):
    if relevant_fields is None:
        relevant_fields = [
            "order_id", "order_date", "total_amount",
            "return_eligible", "item_description"
        ]
    return {k: v for k, v in raw_result.items() if k in relevant_fields}
```

**Qué NO hacer:**
- Conservar los tool results completos "por si el modelo los necesita luego": una consulta de 40+ campos agota el presupuesto de tokens a lo largo de los turnos (web 5.1).
- Dejar que el raw tool output se acumule sin control (Guía PDF p. 238).

Las slides añaden tres tácticas: filtrar en origen (parámetros de API como 'fields=' o 'select='), post-procesar antes de inyectar (no inyectar la respuesta cruda) y resumir o truncar salidas largas como búsquedas o documentos (Slides PDF p. 1305). Los resultados largos llenan la ventana más rápido, entierran el dato relevante y degradan el rendimiento; son una de las fuentes más comunes de context bloat en sistemas agénticos (Slides PDF p. 1303; Slides PDF p. 1308). El ejercicio de la web espera un resultado recortado 80-90% más pequeño que el original (web 5.1).

### API stateless e historial completo

**Concepto:** La Claude API es stateless: no hay estado de sesión en el servidor y cada request debe incluir el historial completo; si se omiten mensajes, el modelo pierde coherencia conversacional (web 5.1; Guía PDF p. 233).

**Ejemplos de uso (3, cortos):**
1. El asistente de la agencia reenvía toda la sesión de planificación en cada request (web 5.1).
2. Omitir el historial hace que el modelo empiece de cero; incluirlo le da continuidad (Guía PDF p. 234).
3. El case facts block resuelve el conflicto entre necesitar el historial completo y los límites de contexto: permite resumir el resto y mantener los detalles transaccionales (web 5.1).

Implicaciones de la guía: tú controlas lo que el modelo recuerda; limpiar es decisión tuya, no del modelo; y el re-grounding tras la compaction es tu responsabilidad (Guía PDF p. 234).

**Qué NO hacer:**
- Truncar selectivamente el historial suponiendo que no se pierde nada (web 5.1).
- Esperar que el modelo decida olvidar contenido antiguo por sí solo (Guía PDF p. 234).

**Posible confusión con otros conceptos:**
- Retention — mantener información en la ventana: acceso instantáneo, pero llena la ventana y provoca context rot (Guía PDF p. 237).
- Retrieval — guardar fuera y recuperar bajo demanda: mantiene pequeña la ventana, pero añade un paso de búsqueda (Guía PDF p. 237).

### Upstream agent optimisation (handoffs estructurados)

**Concepto:** En sistemas multi-agente, los agentes upstream suelen devolver cadenas de razonamiento y contenido crudo que los agentes downstream no necesitan; hay que modificarlos para que devuelvan datos estructurados (hechos principales, citas, relevance scores) (web 5.1; Guía PDF p. 237).

**Ejemplos de uso (3, cortos):**
1. El subagente de hoteles devuelve hallazgos con fuente y fecha, sin sus pasos de búsqueda (web 5.1).
2. Exigir metadatos como fechas, ubicaciones de fuente y contexto metodológico para una síntesis downstream precisa (web 5.1).
3. Un análisis en prosa de 2,000 palabras consume mucho más contexto downstream que un resumen estructurado de 200 tokens con hallazgos, citas y confidence scores (Guía PDF p. 237).

```json
{
  "findings": [
    {
      "claim": "Renewable energy investment grew 12% in 2023",
      "source": "IEA World Energy Report 2024",
      "sourceUrl": "https://example.com/report",
      "relevanceScore": 0.92,
      "publicationDate": "2024-01-15"
    }
  ]
}
```

**Qué NO hacer:**
- Pasar al agente de síntesis el razonamiento completo del subagente: gasta tokens en razonamiento que no puede usar (web 5.1).
- Pasar razonamiento verboso entre agentes cuando bastarían datos estructurados (Guía PDF p. 238).

Los datos estructurados también permiten procesar los hallazgos sin volver a parsear prosa extensa (web 5.1).

### Herramientas de gestión de contexto: context editing, compaction y memory tool

**Concepto:** Tres capacidades trabajan juntas: context editing limpia automáticamente tool results obsoletos, compaction resume la conversación y continúa sobre el resumen, y el memory tool guarda información en archivos fuera de la ventana (Guía PDF p. 232). Editing y compaction liberan espacio; el memory tool preserva lo importante antes de liberarlo (Guía PDF p. 232).

**Ejemplos de uso (3, cortos):**
1. Context editing en trabajo con muchas tools cuyos resultados antiguos ya no hacen falta (Guía PDF p. 232).
2. Compaction en sesiones únicas largas que se acercan al límite (Guía PDF p. 232).
3. Antes de compactar, guardar hechos durables (customer ID, issue abierto, constraints) en el memory tool; el resumen da la idea general y la memoria aporta los valores exactos (Guía PDF p. 232).

**Qué NO hacer:**
- Suponer que context editing recuerda lo que limpió (Guía PDF p. 232).
- Esperar que la compaction conserve cada detalle: los resúmenes pierden algunos (Guía PDF p. 232).
- Omitir el memory tool, de modo que la información limpiada se pierde para siempre; limpiar sin guardar antes lo importante es un error común (Guía PDF p. 232; Guía PDF p. 234).

**Posible confusión con otros conceptos:**
- Context editing vs compaction — editing limpia contenido específico; compaction resume todo (Guía PDF p. 267).
- Comandos de compactación como `/compact` al inicio de cada conversación — útiles para la longitud, pero pueden perder precisión en hechos transaccionales (Q69).

### Prompt caching

**Concepto:** El prompt caching evita pagar por reprocesar las partes que no cambian; marca un prefijo estable con un breakpoint `cache_control` y la API lo reutiliza, cobrando una fracción del coste de entrada por los tokens cacheados (web 5.1). Reduce coste y latencia, pero no encoge la ventana (Guía PDF p. 233).

**Ejemplos de uso (3, cortos):**
1. Poner primero lo constante (instrucciones de sistema, tool definitions, documentos de referencia largos), el breakpoint al final de ese bloque y lo volátil (último mensaje del usuario) después (web 5.1).
2. Colocar el bloque estático en el parámetro `system` de nivel superior, no en `messages`; la caché lee en el orden tools, system, messages (web 5.1).
3. Usar `{"type": "ephemeral", "ttl": "1h"}` para una hora, con mayor coste de escritura; el breakpoint ephemeral por defecto dura unos cinco minutos desde su último uso; máximo cuatro breakpoints por request (web 5.1).

```python
system=[
    {"type": "text", "text": LONG_STATIC_INSTRUCTIONS},
    {"type": "text", "text": REFERENCE_DOC,
     "cache_control": {"type": "ephemeral"}},
],
messages=[
    {"role": "user", "content": dynamic_user_message},
],
```

**Qué NO hacer:**
- Poner contenido dinámico antes del bloque estático: el prefijo cambia en cada request, nada coincide y se paga el precio completo (web 5.1).
- Usar el caching como sustituto de limpiar o resumir cuando la ventana se llena (Guía PDF p. 233).

El examen solo evalúa que el caching existe y su propósito; la lista fuera de alcance de la guía excluye los detalles de implementación (web 5.1).

### Trampas del examen

- Q69 (agente que dice "el sobrecargo del mes pasado" sin el importe $847.50): la respuesta correcta es el case facts block incluido al inicio de cada prompt (Q69). Fallan `/compact` al inicio de cada conversación, que puede perder precisión en hechos transaccionales; cambiar a una ventana mayor, que no evita la progressive summarisation; y pedir releer todo el historial antes de cada respuesta, poco práctico y que no evita que los hechos se pierdan al crecer el contexto (Q69).
- Q70 (síntesis que omite o contradice hallazgos de las secciones intermedias): la causa es el efecto "lost in the middle" y la mitigación es poner un resumen de hallazgos clave al principio y secciones con cabeceras explícitas (Q70). Fallan añadir deduplicación (trata consistencia de datos, no atención posicional), subir `max_tokens` (trata la longitud de salida, no la atención sobre el input) y enrutar salidas por un agente de resumen secundario (añade complejidad y no resuelve por sí solo el problema posicional) (Q70).
- Escenario de práctica de la web: el agente dice "your recent refund request" en lugar de $247.83 del pedido #8891 aunque el summariser ya tenía la orden de conservar cada cifra literalmente. Gana extraer los hechos a un case facts block fuera del historial resumido (web 5.1). Falla instruir al modelo a preservar importes, fechas y números de pedido al resumir, porque ya se hizo y el $247.83 se perdió igualmente; fallan también guardar todo en una base de datos externa y recuperar turnos bajo demanda (el agente no puede saber de antemano qué detalle necesitará) y ampliar la ventana para evitar resumir (no hay ventana que aguante sesiones sin límite) (web 5.1).
- Pensar que la progressive summarisation es segura para datos transaccionales: destruye valores numéricos, fechas e identificadores (web 5.1).
- Creer que "lost in the middle" se resuelve diciéndole al modelo que preste atención a todo: el fallo es de posición, y el arreglo es estructural (web 5.1).
- Mantener tool results completos "por si hacen falta": una consulta de 40+ campos agota el presupuesto de tokens; hay que recortar antes de que entren al historial (web 5.1).
- Truncar el historial selectivamente suponiendo que no se pierde nada: la API es stateless y la guía subraya pasar el historial completo; descartar mensajes sin plan pierde hechos (web 5.1).
- Trampas de la guía: context editing se supone que también recuerda lo que limpió; la compaction se espera que conserve cada detalle; el memory tool se omite y lo limpiado se pierde para siempre (Guía PDF p. 232). Dejar durable facts en el historial ordinario, o mantener el passing history completo desplazando los durable facts (Guía PDF p. 236). Ante un valor presente al inicio y ausente tras varios resúmenes, la respuesta es un durable facts block, no mejores instrucciones de resumen (Guía PDF p. 235). Si la fiabilidad baja en una sesión larga, apunta al crecimiento del contexto y no al prompt; elegir limpiar contenido obsoleto y preservar hechos críticos en memoria, sin asumir que una ventana mayor elimina la gestión (Guía PDF p. 234).
- Retention vs retrieval: retener llena la ventana y provoca context rot; recuperar añade un paso de búsqueda y depende de un buen recall (Guía PDF p. 237).
- Olvidar reinyectar el case facts block tras la compaction (Guía PDF p. 238).
- **Contradicción entre fuentes:** la web advierte contra truncar selectivamente el historial porque la API stateless exige el historial completo (web 5.1), mientras la guía indica que el passing history (charla y pasos resueltos) se puede recortar o limpiar de forma segura (Guía PDF p. 236). Prevalece la guía; ambas coinciden en que los hechos críticos deben ir en el case facts block (web 5.1; Guía PDF p. 236).

## Tarea 5.2 — Design effective escalation and ambiguity resolution patterns (Diseñar patrones eficaces de escalación y resolución de ambigüedad)

> Prioridad de estudio: Salvaguardas de orquestación: cierre en resolución o escalación (0% en los intentos 1 y 2)

### Escalación y calibración

**Concepto:** Escalation es que el agente de soporte entregue la conversación a un humano; el trigger es la condición que la provoca y la calibration es qué tan bien el agente elige cuándo escalar (web 5.2). Una calibración incorrecta reduce de forma directa y marcada la first-contact resolution, es decir, la proporción de casos resueltos en la primera conversación sin traspaso a un humano (web 5.2). La guía pide escalar por la sustancia de la situación, no por cómo suena el mensaje (Guía PDF p. 238).

**Ejemplos de uso (3, cortos):**
1. El agente resuelve por sí mismo un reenvío de producto simple en vez de pasarlo a un humano (web 5.2).
2. El agente escala una solicitud fuera de política porque requiere una autoridad que el sistema no tiene (Guía PDF p. 238).
3. Un escenario con 55% de first-contact resolution frente a un objetivo de 80% revela mala calibración: escala casos simples e intenta casos complejos (web 5.2; Q3).

**Qué NO hacer:**
- Over-escalating: enviar a un humano casos simples que el agente podía manejar (Slides PDF p. 1471).
- Under-escalating: intentar resolver de forma autónoma situaciones que exigen juicio humano (Slides PDF p. 1471).
- Escalar como forma de evitar el problema: genera traspasos innecesarios y más carga para el equipo humano (Slides PDF p. 1395).

### Solicitud explícita de un humano

**Concepto:** Cuando el cliente pide una persona ("I want to speak to a person", "Transfer me to a human agent"), se escala de inmediato, sin intentar resolver antes ni decir "Let me see if I can help you with that first"; es una regla absoluta sin excepciones (web 5.2). La guía y las slides coinciden: se honra sin investigar primero (Guía PDF p. 238; Slides PDF p. 1383).

**Ejemplos de uso (3, cortos):**
1. El cliente dice "I want a human" desde el inicio: se escala en esa misma respuesta, sin investigación ni oferta de ayuda previa (web 5.2).
2. El cliente pide un humano y además está frustrado por un problema de facturación que el agente podría resolver en 2 pasos: se escala igualmente en la primera petición (Q71).
3. El cliente pide un humano aunque el agente pueda resolver: la capacidad del agente no es el factor decisivo (Q71).

**Qué NO hacer:**
- Intentar resolver o investigar antes de escalar; convierte una instrucción clara en una negociación (web 5.2; Guía PDF p. 241).
- Completar la investigación, presentar la solución y escalar solo si el cliente insiste después (Q71).
- Usar la oferta de resolución para anular una petición explícita de humano (Guía PDF p. 239).

**Posible confusión con otros conceptos:**
- Cliente frustrado que no pidió humano — se puede reconocer la frustración y ofrecer ayuda (Guía PDF p. 239).

### Brechas de política y límites de autoridad

**Concepto:** Si la solicitud queda fuera de la política documentada, el agente no puede crear política durante la conversación, así que un humano decide si hace una excepción (web 5.2). Una brecha (gap) es que la política guarda silencio; una violación tiene respuesta documentada: los gaps se escalan, las violaciones no (web 5.2). La guía añade los authority limits: acciones que requieren un nivel de aprobación que el agente no tiene, como un reembolso sobre un umbral o un cambio de sistema que exige autorización humana (Guía PDF p. 238).

**Ejemplos de uso (3, cortos):**
1. Un cliente pide igualar el precio de un competidor y la política solo cubre ajustar los precios propios: se escala (web 5.2).
2. Un reembolso fuera de la ventana de devolución tiene respuesta documentada ("no"): el agente lo rechaza sin escalar (web 5.2).
3. Un reembolso de 247.50 supera el límite de auto-aprobación de 100.00: se escala con traspaso estructurado (Guía PDF p. 255).

**Qué NO hacer:**
- Escalar una violación de política que ya tiene respuesta documentada (web 5.2).
- Intentar resolver de forma autónoma una solicitud que necesita una excepción de política: es el fallo de "under-escalating" que muestra el banco (Q3).
- Basar la decisión en el nivel de frustración: ante una solicitud fuera de política, la brecha de autoridad es el trigger y la frustración no importa (Slides PDF p. 1385).

**Posible confusión con otros conceptos:**
- Violación de política — reembolso fuera de plazo: el agente responde "no" por sí mismo (web 5.2).
- Brecha de política — igualar precio de competidor: se escala a personal humano (web 5.2).

### Incapacidad de progresar y fallo repetido

**Concepto:** El tercer trigger válido es no poder avanzar tras un intento genuino: herramientas con errores que el retry local no resuelve, falta de acceso al sistema o un bug que requiere ingeniería; no basta decir "I might not be able to handle this", el agente debe demostrar que lo intentó y falló (web 5.2). La guía añade loop detection: llevar la cuenta de intentos por paso y, tras un número fijo de fallos en el mismo paso, detenerse y escalar, para no gastar tokens y tiempo en una acción que no puede tener éxito (Guía PDF p. 240).

**Ejemplos de uso (3, cortos):**
1. La herramienta de reservas falla tras todos los reintentos: el caso califica para escalar (web 5.2).
2. El mismo paso falla repetidamente sin progreso: se escala por stalled progress (Guía PDF p. 240).
3. Tras intentos genuinos con herramientas y políticas no se puede resolver: "No meaningful progress" (Slides PDF p. 1383; Slides PDF p. 1472).

**Qué NO hacer:**
- Reintentar el mismo paso fallido indefinidamente: es un fallo de fiabilidad en sí mismo (Guía PDF p. 240).
- Escalar por una simple sospecha de incapacidad sin haber intentado (web 5.2).

### Triggers poco fiables: sentiment y confianza autorreportada

**Concepto:** Escalar por sentiment (frustración detectada o puntuación negativa) es poco fiable porque mide estado emocional y la frustración no se correlaciona con la complejidad del caso (web 5.2; Slides PDF p. 1384). La self-reported confidence (el modelo se califica de 1 a 10 y escala bajo un umbral) está mal calibrada: el modelo suele estar equivocadamente seguro en casos difíciles, porque no sabe lo que no sabe, y innecesariamente inseguro en casos claros (web 5.2). La guía añade que una confianza baja puede reflejar solo ambigüedad en la fuente (Guía PDF p. 239).

**Ejemplos de uso (3, cortos):**
1. Un cliente furioso por una entrega tardía de azulejos tiene un caso simple: disculparse, compensar y reenviar (web 5.2).
2. Un cliente calmado que pide igualar precio tiene una brecha de política que requiere juicio humano (web 5.2).
3. Con un trigger de confianza, el agente enviaría a personal el caso simple de azulejos y se quedaría con el de igualar precio (web 5.2).

**Qué NO hacer:**
- Escalar cuando el sentiment supera un umbral, o negarse a escalar porque el tono parece calmado (web 5.2; Guía PDF p. 241).
- Tratar una confianza autorreportada alta como prueba de corrección (Guía PDF p. 241).
- Enrutar por un score de confianza en lugar de criterios explícitos con few-shot (web 5.2; Q3).

**Posible confusión con otros conceptos:**
- Triggers concretos — solicitud explícita, brecha de política, límite de autoridad o fallo repetido: son los que deben guiar la escalación (Guía PDF p. 239).

### Cliente frustrado: reconocer y ofrecer resolución

**Concepto:** La frustración por sí sola no decide la respuesta: si el problema es simple, se reconoce la frustración y se ofrece la resolución sin escalar; si el cliente reitera su preferencia por un humano después de la oferta, entonces se escala (web 5.2). La frustración no justifica escalar salvo que exista además un blocker válido (Slides PDF p. 1394). Las slides proponen tres pasos: reconocerla brevemente, reformular el objetivo y comprobar si hay un blocker real (brecha de autoridad, petición explícita de humano o acción de alto riesgo); si lo hay se escala, si no se resuelve (Slides PDF p. 1397).

**Ejemplos de uso (3, cortos):**
1. "I understand this is frustrating. I can process your replacement right now." (web 5.2).
2. El cliente rechaza la oferta y repite que quiere un humano: ahora se escala (web 5.2).
3. Cliente molesto con un problema estándar dentro de política: reconocer y resolver; escalar solo si insiste en un humano (Slides PDF p. 1385).

**Qué NO hacer:**
- Escalar solo porque el usuario está frustrado: trata el síntoma y puede entregar un ticket que un humano no resuelve más rápido (Slides PDF p. 1392).
- Usar un reconocimiento ensayado ("I understand your frustration") en vez de reconocer de forma directa que la interacción no ha ido bien (Slides PDF p. 1397).

**Posible confusión con otros conceptos:**
- Frustrado sin petición explícita — se ofrece resolución primero (Guía PDF p. 239).
- Petición explícita de humano desde el inicio — se escala de inmediato, sin oferta previa (web 5.2).

### Coincidencias ambiguas de clientes

**Concepto:** Si una herramienta devuelve varias coincidencias (por ejemplo, tres registros "John Smith"), el agente debe pedir identificadores adicionales (correo, teléfono, número de pedido) y nunca elegir por sí mismo (web 5.2). La guía amplía a cualquier consulta con más de una interpretación: hacer una pregunta aclaratoria breve en vez de adivinar (Guía PDF p. 239).

**Ejemplos de uso (3, cortos):**
1. El agente pide un correo electrónico antes de abrir cualquier cuenta (web 5.2).
2. "I found two accounts matching that description, one under john@work.com and one under john@home.com. Which one?" (Guía PDF p. 239).
3. En el pseudocódigo de la guía, si la solicitud coincide con más de un registro, se hace una pregunta aclaratoria (Guía PDF p. 240).

**Qué NO hacer:**
- Elegir el registro más reciente, el más activo o usar cualquier otra heurística (web 5.2).
- Preguntar de forma vaga ("Could you clarify?") en lugar de una pregunta específica (Guía PDF p. 239).
- Adivinar una interpretación cuando una pregunta de una línea eliminaría la ambigüedad (Guía PDF p. 241).

**Posible confusión con otros conceptos:**
- Ambigüedad — se resuelve preguntando, no escalando por sentiment ni confianza (Guía PDF p. 240).

### Criterios explícitos y few-shot en el system prompt

**Concepto:** La forma más eficaz de calibrar la escalación es añadir al system prompt criterios explícitos con ejemplos few-shot, que corrigen la causa raíz: límites de decisión poco claros (web 5.2; Q3). Es la primera respuesta proporcionada, antes de añadir infraestructura como modelos clasificadores o análisis de sentiment; la optimización del prompt precede a los cambios de arquitectura (web 5.2). Las slides lo resumen en criterios explícitos, few-shot que muestren resolver vs. escalar y una cadena de razonamiento de política: dentro, fuera o silenciosa (Slides PDF p. 1386).

**Ejemplos de uso (3, cortos):**
1. Un ejemplo que muestra cuándo escalar: petición explícita de humano, brecha de política o incapacidad de avanzar (web 5.2).
2. Un ejemplo que muestra cuándo resolver de forma autónoma: caso simple o frustrado pero resoluble (web 5.2).
3. Un ejemplo del formato exacto del traspaso estructurado, con ID de cliente, causa raíz y acción recomendada (web 5.2).

**Qué NO hacer:**
- Desplegar un clasificador separado entrenado con tickets históricos: está sobredimensionado (Q3).
- Implementar sentiment analysis: resuelve un problema distinto (Q3).
- Enrutar por un score de confianza autorreportado (Q3).

### Traspaso con contexto (warm handoff) y niveles de escalación

**Concepto:** Al escalar, el humano debe recibir un warm start, no una pizarra en blanco. El handoff incluye cinco componentes: motivo de la escalación, case facts (customer ID, tipo de cuenta, fechas, montos, restricciones), pasos ya realizados, estado actual y acción recomendada (Guía PDF p. 240). La escalación no siempre es binaria: hay niveles (0: el agente resuelve; 1: necesita aprobación humana; 2: el frontline no puede resolver y pasa a especialista o team lead; 3: el especialista no puede y pasa a manager o excepción de política), y el agente debe enrutar directamente al nivel correcto cuando sea posible (Guía PDF p. 239; Guía PDF p. 240).

```json
{
  "reason": "refund_exceeds_auto_approval_limit",
  "case_facts": {
    "customer_id": "C-4471",
    "order_id": "O-88421",
    "charge_date": "2026-05-02",
    "refund_amount": 247.50,
    "auto_approval_limit": 100.00
  },
  "steps_taken": [
    "Customer identity verified via email match",
    "Order O-88421 confirmed as duplicate charge",
    "Refund policy checked: amount exceeds $100 auto-approval"
  ],
  "recommended_action": "Approve refund of $247.50 for duplicate charge"
}
```
(Guía PDF p. 255)

**Ejemplos de uso (3, cortos):**
1. Reembolso por encima del umbral de auto-aprobación: Level 1, agente de soporte frontline (Guía PDF p. 239).
2. Disputa de facturación compleja que abarca varios meses: Level 2, especialista o team lead (Guía PDF p. 240).
3. Cliente pide un humano tras compactación: escalar de inmediato con case facts, pasos intentados y un resumen de una línea, guardando antes los hechos en la memory tool y reinyectándolos después (Guía PDF p. 268).

**Qué NO hacer:**
- Decir "I'm transferring you to a human agent" sin contexto, de modo que el humano pide al cliente repetir todo (Guía PDF p. 255).
- Pedir al cliente que repita la fecha, o compactar sin guardar los case facts (Guía PDF p. 268).
- Empezar siempre en Level 1 y dejar que los humanos re-enruten (Guía PDF p. 240).

### Trampas del examen

- Elegir el score de confianza autorreportada (1-10, umbral 7) como solución al 55% de first-contact resolution (opción B de Q3): falla porque la confianza del LLM está mal calibrada; el escenario describe justo el fallo típico, que escala casos simples e intenta los complejos aun cuando el agente se califica con confianza alta en ambos (Q3; web 5.2).
- Elegir sentiment analysis para escalar por umbral de frustración (opción D de Q3): resuelve un problema distinto, porque la frustración no se correlaciona con la complejidad (Q3; web 5.2; Guía PDF p. 239).
- Desplegar un clasificador separado entrenado con tickets históricos (opción C de Q3): está sobredimensionado, y en el escenario de la web la empresa ni siquiera tiene registro de qué tickets debieron ir a un humano (Q3; web 5.2).
- La respuesta correcta de Q3 es añadir criterios explícitos al system prompt con few-shot (opción A), porque ataca los límites de decisión poco claros (Q3).
- Q71, opción B (escalar cuando el frustration score supere un umbral): introduce sentiment como proxy cuando el cliente ya expresó una preferencia explícita; el sentiment es irrelevante (Q71).
- Q71, opción C (investigar, presentar solución y escalar solo si insiste): retrasa honrar la petición y frustra más al cliente (Q71).
- Q71, opción D (disculparse y seguir con la resolución automática): es el comportamiento erróneo del agente; la capacidad no decide cuando hay una petición explícita (Q71).
- Responder "Let me see if I can help you with that first" ante una petición de humano: convierte una instrucción clara en una negociación (web 5.2; Guía PDF p. 241). La oferta de resolver primero solo corresponde a frustración sin petición explícita (web 5.2).
- Elegir entre coincidencias ambiguas por el registro más reciente o más activo: riesgo de violación de privacidad o de acción incorrecta (por ejemplo, reembolso en la cuenta equivocada); lo seguro es pedir identificadores adicionales (web 5.2).
- Escalar sin contexto, forzando al humano a empezar de cero (Guía PDF p. 241).
- Tratar el patrón "explicit request overridden" y "sentiment as trigger" como distractores recurrentes: la respuesta es escalación inmediata y triggers concretos (Guía PDF p. 266).
- Tratar una violación de política como si fuera una brecha: la violación tiene respuesta documentada y no se escala (web 5.2).
- **Contradicción entre fuentes:** La web afirma que existen exactamente tres triggers válidos: petición explícita de humano, brecha de política e incapacidad de progresar (web 5.2). Las slides listan en un lugar esos mismos tres (Slides PDF p. 1383), pero en otro listan como "3 Triggers: Escalate Immediately" la pérdida o corrupción de datos, la brecha o ambigüedad de política y la imposibilidad de progresar (Slides PDF p. 1472), y mencionan además un requisito de verificación para acciones financieras, legales, médicas u otras de alto riesgo (Slides PDF p. 1394). La guía incluye además los authority limits y el fallo repetido (Guía PDF p. 238; Guía PDF p. 258). Prevalecen la guía y el banco sobre la web: la petición explícita, la brecha de política, el límite de autoridad y el fallo repetido son triggers concretos; la ambigüedad se resuelve preguntando (Guía PDF p. 258; Q71).

## Tarea 5.3 — Implement error propagation strategies across multi-agent systems (Implementar estrategias de propagación de errores en sistemas multiagente)

### Structured error context (contexto de error estructurado)

**Concepto:** En un sistema multiagente, la propagación de errores es cómo el fallo de un subagent (timeout, error de permisos, query inválida) llega al coordinator; esto decide si el sistema se recupera o falla en silencio (web 5.3). Un error útil dice qué pasó, por qué y si vale la pena reintentar; un error genérico como "something went wrong" no dice nada al coordinator (Guía PDF p. 242).

La web exige cuatro elementos en el error del subagent: tipo de fallo, qué se intentó, resultados parciales obtenidos antes del fallo y enfoques alternativos potenciales (web 5.3). La guía propone los campos category, description, retryable y source (Guía PDF p. 242).

**Ejemplos de uso (3, cortos):**
1. Failure type: transient (timeout, rate limit) puede funcionar al reintentar; validation necesita una query corregida; business necesita escalación o alternativa; permission no se reintenta sin cambiar la autorización (web 5.3).
2. What was attempted: "Searched the merchant's price list for 'red facing brick', June delivery" es accionable; "Search failed" no lo es (web 5.3).
3. Partial results y alternatives: si se recuperaron 3 de 5 fuentes antes del timeout siguen siendo útiles, y el subagent puede sugerir otra fuente, términos más amplios o resultados en caché (web 5.3).

```json
{
"status": "partial_failure",
"failureType": "transient",
"attemptedAction": {
"tool": "search_academic_db",
"query": "renewable energy policy",
"dateRange": "2022-2024"
},
"partialResults": [
{
"title": "EU Renewable Energy Directive 2023",
"source": "EUR-Lex",
"retrieved": true
}
],
"alternativeApproaches": [
"Retry with narrower date range (2023-2024)",
"Search alternative database: government_publications",
"Use cached results from previous research session"
]
}
```

Con esta estructura el coordinator decide: reintentar la misma query, probar una alternativa, continuar con resultados parciales o escalar (web 5.3).

**Qué NO hacer:**
- Devolver un estado genérico "search unavailable" tras agotar los reintentos: oculta la query, los resultados parciales y las alternativas (web 5.3).
- Usar mensajes genéricos como "tool failed": son siempre el patrón incorrecto (Guía PDF p. 242).
- Omitir la información de retryability, de modo que el coordinator no sabe si reintentar u omitir (Guía PDF p. 245).

### Error categories y decisiones de recuperación

**Concepto:** La lógica de recuperación del coordinator debe ramificarse según la categoría del error, no analizando el texto de la descripción (Guía PDF p. 243).

**Ejemplos de uso (3, cortos):**
1. timeout (latencia de red, backend lento) — Retry with backoff; rate_limited (demasiadas solicitudes) — esperar y reintentar tras un retraso (Guía PDF p. 243).
2. permission_denied (faltan credenciales o scope) — Escalate, no se puede reintentar; validation_error (request mal formada) — corregir la request y reintentar (Guía PDF p. 243).
3. service_unavailable (backend caído) — probar fuente alternativa o anotar la brecha; not_found — es un resultado válido, no un error (Guía PDF p. 243).

**Posible confusión con otros conceptos:**
- Categorías de la guía (timeout, rate_limited, permission_denied…) — la web usa en cambio failureType con transient, validation, business y permission (web 5.3).

### Access failure vs valid empty result

**Concepto:** Un access failure significa que la herramienta no pudo alcanzar su fuente (timeout, error de conexión, permiso denegado) y la búsqueda no se ejecutó; un valid empty result significa que la herramienta consultó la fuente y no encontró coincidencias (web 5.3; Guía PDF p. 242). En el primero la ausencia de datos no es significativa; en el segundo la ausencia de datos es información en sí misma (Guía PDF p. 242). La guía indica que el examen evalúa esta distinción directamente (Guía PDF p. 242); la web añade que la mayoría de los desarrolladores la responde mal (web 5.3).

**Ejemplos de uso (3, cortos):**
1. API devolvió 500 — access failure; respuesta correcta: error estructurado con retryable: true; respuesta incorrecta: devolver resultado vacío (Guía PDF p. 242).
2. API devolvió 200 con cero registros — valid empty result; respuesta correcta: resultado vacío con estado de éxito; incorrecta: devolver error (Guía PDF p. 243).
3. Si los registros de trabajos pasados no contienen muros curvos, el resultado vacío significa que la empresa no ha construido uno (web 5.3).

```python
# Access failure — consider retry
{
"status": "error",
"failureType": "transient",
"message": "Connection timeout after 30s",
"shouldRetry": True
}

# Valid empty result — no retry needed
{
"status": "success",
"results": [],
"message": "Query executed successfully. No matching records found.",
"shouldRetry": False
}
```

**Qué NO hacer:**
- Tratar un access failure como valid empty result: nunca se reintenta cuando debería (web 5.3).
- Tratar un valid empty result como access failure: se pierde tiempo reintentando una query que siempre devolverá vacío (web 5.3).
- Dejar que un agente downstream informe "no data exists" cuando la verdad es "we could not check" (Guía PDF p. 242).

**Posible confusión con otros conceptos:**
- not_found — en la guía es un valid result, no un error (Guía PDF p. 243).
- Silent suppression — devuelve vacío marcado como éxito aunque la herramienta falló (web 5.3).

### Los dos anti-patterns: silent suppression y workflow termination

**Concepto:** Silent suppression es devolver resultados vacíos marcados como éxito; es el peor anti-pattern porque es invisible y el coordinator cree que la búsqueda corrió y no halló nada (web 5.3). Workflow termination (la guía lo llama over-reaction) es terminar todo el pipeline ante un solo fallo, desperdiciando el trabajo de los demás agentes (web 5.3; Guía PDF p. 243). La alternativa es la propagación estructurada: el subagent reporta, el coordinator evalúa el efecto y el sistema continúa con resultados parciales o recuperación dirigida (web 5.3).

**Ejemplos de uso (3, cortos):**
1. Silent suppression: un timeout que devuelve { "results": [], "status": "success" }; la cotización se envía sin coste de ladrillos (web 5.3).
2. Silent suppression en soporte: el agente informa "no orders found" mientras la consulta de pedidos no está disponible, y puede decirle al cliente que no tiene cuenta (web 5.3).
3. Workflow termination: un subagent hace timeout, el pipeline cae y se descartan los otros cuatro resultados completados (web 5.3); un timeout en una llamada no debería destruir un informe completo al 90% (Guía PDF p. 243).

**Qué NO hacer:**
- Capturar el error y continuar como si todo hubiera salido bien (Guía PDF p. 243).
- Propagar la excepción a un handler de nivel superior que termina todo el workflow (web 5.3).
- Marcar como éxito un resultado que en realidad es un fallo de acceso (Guía PDF p. 245).

**Posible confusión con otros conceptos:**
- Silent suppression — oculta el fallo y la salida parece completa; Workflow termination — el fallo es visible pero la reacción es desproporcionada (web 5.3).

### Local recovery antes de escalar

**Concepto:** Los subagents deben recuperarse localmente de fallos transient (lógica de retry, fuentes de respaldo, respuestas de menor calidad) antes de propagar errores; solo se propaga lo que no pueden resolver, incluyendo lo intentado y los resultados parciales (web 5.3). Esto reduce la complejidad del coordinator, que no tiene que gestionar retry para cada subagent (web 5.3).

**Ejemplos de uso (3, cortos):**
1. Si una tool call hace timeout, reintentarla una o dos veces antes de reportar el fallo (Guía PDF p. 243).
2. Si una fuente no está disponible, comprobar si una fuente alternativa da la misma información (Guía PDF p. 244).
3. El subagent de precios reintenta al proveedor, prueba un segundo y solo reporta si ambos fallan (web 5.3); en el ejercicio, 3 reintentos con exponential backoff (1s, 2s, 4s) conservando los resultados parciales (web 5.3).

**Qué NO hacer:**
- Escalar al coordinator cada fallo transient sin intentar recuperación local (web 5.3).
- Propagar un error sin incluir qué se intentó ni los resultados parciales (web 5.3).

### Coverage annotations y coverage honesty

**Concepto:** Cuando un synthesis agent combina hallazgos, la salida debe indicar qué áreas están bien respaldadas y cuáles tienen brechas (web 5.3). Si la recuperación falla, se anota la brecha específica en la salida en lugar de ocultarla o matar el workflow (Guía PDF p. 244). Principio de coverage honesty: reportar qué se completó, qué no y por qué; un resultado parcial con anotaciones honestas vale más que uno que parece completo con brechas ocultas o un fallo total (Guía PDF p. 244).

**Ejemplos de uso (3, cortos):**
1. "Section on brick costs is limited because the merchant price list was unavailable." (web 5.3).
2. Informe con billing_analysis con status "complete" y shipping_analysis con status "incomplete", reason "Shipping API timed out after 3 retries" y recommendation (Guía PDF p. 244).
3. Sección de cobertura con cada tema como well-supported, limited (con motivo) o unavailable (con motivo) (web 5.3).

**Qué NO hacer:**
- Omitir el tema fallido: sin anotación, la brecha parece un tema irrelevante y no una fuente no disponible (web 5.3).

### Propagation chains y cascading failures

**Concepto:** Los errores no se quedan locales: el fallo de un agente cambia lo que recibe el siguiente (Guía PDF p. 244). Cascada: Agent A falla → Agent B recibe mala entrada → B produce salida errónea → Agent C la sintetiza en un informe confiado, sin que nadie marque un problema (Guía PDF p. 244). El error estructurado rompe la cadena al hacer visibles los fallos en cada handoff (Guía PDF p. 244).

**Ejemplos de uso (3, cortos):**
1. Agent A devuelve un error estructurado en vez de un resultado vacío (Guía PDF p. 244).
2. Agent B decide omitir esa entrada (Guía PDF p. 244).
3. Agent B prueba una alternativa o anota una coverage gap (Guía PDF p. 244).

**Posible confusión con otros conceptos:**
- Partial success — un informe que cubre 4 de 5 fuentes es más útil que ninguno, si el lector sabe cuál falta (Guía PDF p. 244).

### Trampas del examen

- Silent suppression (Q72): el subagent captura el timeout y devuelve `status: "success"` con `results: []`; falla porque impide al coordinator tomar cualquier decisión de recuperación y deja pasar trabajo incompleto como completo; es un anti-pattern documentado (Q72). La respuesta correcta es A (Q72).
- Delegar la detección al synthesis agent (Q72, opción B): falla porque ese agente carece de herramientas y contexto para volver a ejecutar búsquedas (Q72).
- Validar en el coordinator que los resultados no estén vacíos (Q72, opción C): no ataca la causa raíz, pues el subagent está presentando un fallo como éxito (Q72); además un vacío puede ser un valid empty result legítimo (Guía PDF p. 242).
- Aumentar el umbral de timeout (Q72, opción D): trata el síntoma, no el defecto de diseño de la propagación (Q72).
- Capturar un timeout y devolver vacío con éxito: el coordinator cree que la búsqueda tuvo éxito y no intenta alternativas (web 5.3).
- Terminar todo el pipeline por el timeout de un subagent: desperdicia los resultados de los demás (web 5.3).
- Devolver "search unavailable" tras agotar reintentos (escenario práctico, opción D): oculta query, resultados parciales y alternativas; la respuesta correcta es el contexto de error estructurado (web 5.3).
- Reintentar un valid empty result porque parece un fallo: es la respuesta, y reintentar desperdicia tiempo y recursos (web 5.3).
- Cuando el coordinator no puede saber qué falló por un mensaje vago, la respuesta es errores estructurados con category, description y retryability (Guía PDF p. 242).
- **Contradicción entre fuentes:** La web clasifica el fallo con failureType (transient, validation, business, permission) y recomienda 3 reintentos con exponential backoff en el ejercicio (web 5.3); la guía usa category (timeout, rate_limited, permission_denied, not_found, validation_error, service_unavailable) con campos description, retryable y source, y habla de reintentar una o dos veces (Guía PDF p. 242; Guía PDF p. 243). Prevalece la guía; el principio común (error estructurado, retry local, no suprimir) coincide.

## Tarea 5.4 — Manage context effectively in large codebase exploration (Gestionar el contexto de forma eficaz en la exploración de bases de código grandes)

### Context degradation

**Concepto:** Pérdida progresiva de los hallazgos específicos de una sesión larga: el modelo deja de usar lo que encontró antes porque la salida verbosa reciente domina el contexto (web 5.4). No se debe a agotar los tokens disponibles (web 5.4). Síntoma típico: el agente habla de "typical patterns" en lugar de las clases, métodos y cadenas de dependencias concretas (web 5.4).

Mecanismo: cada paso de exploración produce salida verbosa (contenido de archivos, resultados de búsqueda, listados de directorios) que se acumula; los hallazgos precisos quedan más atrás y la atención se desplaza a lo reciente (web 5.4). La guía añade que los consumidores principales son los archivos cargados con la herramienta Read, y que una vez llena la ventana de contenido antiguo el modelo pierde el rastro de hallazgos anteriores (Guía PDF p. 245; Guía PDF p. 246).

**Ejemplos de uso (3, cortos):**
1. El agente dijo que QuoteRepository (src/repos/quote.ts) implementa Repository<T> y cachea en findById; varios módulos después dice "this follows the typical repository pattern" (web 5.4).
2. Tras ~90 minutos y decenas de lecturas, el agente cita "standard patterns in payment systems" y sus respuestas contradicen los hallazgos de la primera hora (Q73).
3. En la fase 2 el agente describe el módulo de autenticación como "standard JWT patterns" cuando antes había hallado una firma de tokens personalizada (Q74).

**Qué NO hacer:**
- No ampliar la ventana de contexto: la degradación viene de la salida verbosa que aleja los hallazgos, no de quedarse sin tokens, y una ventana mayor se llena igual (web 5.4).
- No subir `max_tokens`: controla la longitud de salida, no el tamaño de la ventana de contexto (Q74).
- No atribuirlo a un rate limit ni cambiar de herramienta (por ejemplo de `Read` a `Grep`) como solución de la degradación (Q73).

**Posible confusión con otros conceptos:**
- Agotamiento de tokens — el contexto se llena y no cabe más; la degradación ocurre aunque quede espacio (web 5.4).

### Scratchpad files

**Concepto:** Archivo persistente en disco donde el agente escribe los hallazgos importantes y que vuelve a leer para preguntas posteriores (web 5.4; Guía PDF p. 245). Es la mitigación principal de la degradación porque el archivo está fuera del contexto de la conversación (web 5.4).

Debe mantenerse desde el inicio de cualquier sesión larga de exploración, como estrategia deliberada y no como arreglo de emergencia cuando las respuestas ya son vagas (web 5.4). Sobrevive a compaction, clearing y límites de sesión (Guía PDF p. 246).

**Ejemplos de uso (3, cortos):**
1. Registrar clases clave con ruta (`OrderRepository` en src/repos/order.ts), cadena de dependencias (RefundProcessor → OrderService → OrderRepository → PostgreSQL) y hallazgos críticos (web 5.4).
2. Para sesiones de 30+ minutos, crear un archivo como exploration-notes.md y releerlo al empezar una nueva fase para restaurar el contexto (Guía PDF p. 246).
3. Escribir hallazgos tras cada fase y consultar el archivo al inicio de las siguientes en lugar de depender del historial de la conversación (Q74).

```markdown
# Exploration Scratchpad — Order Service

## Key Classes
- `OrderRepository` (src/repos/order.ts) — implements Repository<T>, custom findById caching
- `OrderService` (src/services/order.ts) — orchestrates OrderRepository + PaymentGateway
- `RefundProcessor` (src/services/refund.ts) — depends on OrderService.getOrderWithItems()

## Dependency Chain
RefundProcessor → OrderService → OrderRepository → PostgreSQL
RefundProcessor → PaymentGateway → Stripe API
```

**Qué NO hacer:**
- No dejar los hallazgos sin persistir: se pierden al compactar el contexto (Guía PDF p. 247).
- No guardar resúmenes genéricos: el scratchpad debe contener nombres de clase, rutas y cadenas de dependencias concretos (web 5.4).

**Posible confusión con otros conceptos:**
- Exploration journal — evolución del scratchpad en sesiones múltiples; añade Findings (hechos verificados), Questions (con dónde buscar), Hypotheses (aún no verificadas, para no tratarlas como hallazgos) y Decisions (conclusiones con su razonamiento) (Guía PDF p. 246; Guía PDF p. 247).

### Subagent delegation (aislamiento de contexto)

**Concepto:** Un subagent es un agente separado que el coordinator lanza para una tarea concreta; explora de forma verbosa en su propio contexto aislado y devuelve un resumen estructurado (web 5.4). Su valor principal es el aislamiento de contexto, no la paralelización (web 5.4). Solo los resúmenes entran en el contexto de la sesión principal, que conserva la estrategia, el scratchpad y la visión de alto nivel (Guía PDF p. 245).

**Ejemplos de uso (3, cortos):**
1. "Find all test files for the quoting service and report their coverage status" (web 5.4).
2. "Trace the deposit payment flow from API endpoint to database and list all intermediate services" (web 5.4).
3. Un subagent para un grupo de archivos relacionados, que puede cruzar referencias dentro de su propio contexto (Guía PDF p. 246).

La guía da criterios para leer directamente o delegar (Guía PDF p. 246):
- Archivo pequeño (<100 líneas), al inicio de la sesión: leer directamente.
- Archivo grande (500+ líneas): delegar.
- Varios archivos relacionados: un subagent para el grupo.
- Búsqueda puntual (una función, una clase): Grep primero y leer la sección concreta.
- Sesión avanzada (ventana >60% llena): delegar siempre.

Ejemplo de presupuesto: 15 archivos con lecturas directas ≈ 23,000 tokens; con delegación ≈ 9,250 tokens, un ahorro aproximado del 60% (Guía PDF p. 247; Guía PDF p. 257).

**Qué NO hacer:**
- No pensar que los subagents sirven solo para paralelizar (web 5.4).
- No hacer que el coordinator explore todo: cada archivo y búsqueda añade salida verbosa a su contexto (web 5.4).
- No lanzar agentes independientes por subsistema en paralelo como remedio de la degradación de una sola sesión (Q73).

**Posible confusión con otros conceptos:**
- Paralelización — ejecutar varios agentes a la vez; añade paralelismo pero no resuelve la degradación (Q73).

### Summary injection entre fases

**Concepto:** Antes de lanzar los subagents de la fase 2, se resumen los hallazgos clave de la fase 1 y se inyectan en el contexto inicial de esos subagents (web 5.4). Sin ello se produce el problema de "cold start": duplican la exploración de la fase 1 porque nadie les dio los hallazgos (web 5.4). Un subagent empieza con su propio contexto aislado y no ve el historial del padre (web 5.4).

**Ejemplos de uso (3, cortos):**
1. Resumen de la fase 1: arquitectura en capas Controllers → Services → Repositories → Database (web 5.4).
2. Incluir el flujo de reembolso RefundController → RefundProcessor → OrderService → PaymentGateway (web 5.4).
3. Fijar el objetivo de la fase 2: investigar el manejo de errores en RefundProcessor y PaymentGateway (web 5.4).

**Qué NO hacer:**
- No esperar que los subagents hereden el historial de la fase 1 (web 5.4).
- No copiar la transcripción completa a cada subagent: puede exceder su presupuesto (web 5.4).

### El comando /compact

**Concepto:** Comando de Claude Code para reducir el uso de contexto en sesiones largas: resume la conversación y libera espacio conservando la información importante (web 5.4). Debe usarse de forma proactiva, no solo al llegar al límite, porque protege la calidad del contexto y no solo la cantidad (web 5.4).

**Ejemplos de uso (3, cortos):**
1. Ejecutarlo a mitad de una sesión larga cuando la salida de descubrimiento ya llena el contexto (web 5.4).
2. Usarlo durante sesiones extendidas para mantener la calidad del contexto (web 5.4).
3. Combinarlo con un scratchpad, que sobrevive a la compaction (Guía PDF p. 246).

**Qué NO hacer:**
- No esperar a agotar el contexto para usarlo (web 5.4).
- No confiar en él como único mecanismo para conservar un hallazgo específico: comprime el historial y puede perderlo (Q74).

**Posible confusión con otros conceptos:**
- Scratchpad file — persiste hallazgos fuera del contexto; /compact resume la conversación dentro del contexto (web 5.4; Q74).

### Crash recovery con structured state manifests

**Concepto:** Las sesiones largas pueden fallar por crashes, interrupciones de red o agotamiento del contexto; sin mecanismo de recuperación se pierde todo el progreso (web 5.4). Cada agente exporta su estado a un manifest en una ubicación conocida con: lo explorado, hallazgos, fase actual y siguientes pasos, y preguntas pendientes (web 5.4). Al reanudar, el coordinator carga el manifest y lo inyecta en los prompts de los agentes, que continúan sin repetir la exploración (web 5.4).

**Ejemplos de uso (3, cortos):**
1. Un crash en la fase 2: el trabajo se reinicia desde los next steps del manifest (web 5.4).
2. Guardar `exploredPaths`, `keyFindings` y `nextSteps` junto con `sessionId` y `phase` (web 5.4).
3. Reanudar con el coordinator cargando el manifest JSON (web 5.4).

```json
{
  "sessionId": "explore-order-service-001",
  "phase": 2,
  "exploredPaths": ["src/repos/order.ts", "src/services/order.ts", "src/services/refund.ts"],
  "keyFindings": {
    "architecture": "Layered: Controllers → Services → Repositories → DB",
    "criticalIssue": "RefundProcessor has no retry logic for Stripe API failures",
    "testCoverage": {"OrderService": "87%", "RefundProcessor": "12%"}
  },
  "nextSteps": ["Investigate PaymentGateway error handling"]
}
```

**Qué NO hacer:**
- No reiniciar la sesión sin guardar estado: se pierde todo el conocimiento acumulado (web 5.4).
- No reiniciar pidiendo al agente "explorar de forma más eficiente" (web 5.4).

### Estrategias de exploración y progressive discovery

**Concepto:** La estrategia depende de qué se quiere aprender; cada una empareja herramientas con un objetivo (Guía PDF p. 156). Progressive discovery: explorar por etapas, donde los hallazgos de cada una guían la siguiente, en contraste con la lectura exhaustiva (Guía PDF p. 247). Grep busca contenido de archivos; Glob busca nombres o rutas (Guía PDF p. 156).

**Ejemplos de uso (3, cortos):**
1. Subsistema grande (caché de 15 archivos, ~8,000 líneas): analizar imports y jerarquías para hallar la clase base, leerla y trazar implementaciones hacia fuera (Guía PDF p. 157).
2. Renombrado de función con wrappers (calculateTax → computeOrderTax): leer los módulos wrapper para ver todos los nombres y hacer Grep de cada uno (Guía PDF p. 157).
3. Mensaje de error de producción sin servicio conocido (12 servicios): Grep del texto distintivo ("SYNC_CONFLICT") y luego Read de los archivos coincidentes (Guía PDF p. 157).

Otros casos: tarea abierta en un código legado de 200 archivos → Glob y Grep para mapear, identificar módulos acoplados, plan priorizado y revisarlo al descubrir dependencias (Guía PDF p. 158). Costes de contexto: Grep mínimo (líneas coincidentes), Glob mínimo (rutas), lectura directa alto, scratchpad ninguno (Guía PDF p. 259).

**Qué NO hacer:**
- No leer todos los archivos secuencialmente ni hacer Grep sin contexto estructural (Guía PDF p. 157).
- No empezar alfabéticamente ni leer los 200 archivos antes de escribir tests, ni fijar un calendario por estructura de directorios (Guía PDF p. 158).
- No explorar sin objetivo claro ni evitar Grep/Glob en búsquedas dirigidas (Guía PDF p. 247).

**Posible confusión con otros conceptos:**
- Grep — buscar quién importa @company/auth (contenido) (Guía PDF p. 156).
- Glob — listar archivos `*.test.ts` o cache*.py (nombre) (Guía PDF p. 156).

### Trampas del examen

- Ampliar la ventana de contexto (web 5.4; Q74 con `max_tokens`; web 5.4 opción D del escenario): falla porque la degradación viene de la salida verbosa, no de falta de tokens; `max_tokens` solo controla la salida (web 5.4; Q74).
- Rate limit y delays (Q73): diagnóstico erróneo, la causa es context degradation.
- Dividir en subsistemas con agentes paralelos (Q73): añade paralelismo pero no arregla la degradación de una sesión.
- Cambiar de `Read` a `Grep` (Q73): no aborda el crecimiento del contexto ni la degradación.
- `/compact` antes de la fase 2 como solución (Q74): comprime el historial y puede perder el hallazgo concreto; además debe usarse de forma proactiva, no solo al llegar al límite (Q74; web 5.4).
- Reiniciar la sesión con resumen manual (Q74): válido pero costoso; pierde el entendimiento acumulado y exige intervención manual. Reiniciar sin guardar estado pierde los hallazgos (Q74; web 5.4).
- Precargar toda la estructura del código en el contexto inicial (escenario web 5.4) o pre-generar resúmenes de archivos, cambiar a un modelo mayor o limpiar el contexto periódicamente (Guía PDF p. 247): no son la respuesta; la respuesta es scratchpad y delegar lecturas verbosas.
- Esperar que los subagents de la fase 2 hereden el historial, o pasarles la transcripción completa (web 5.4).
- Asumir que los subagents son solo para paralelizar (web 5.4).
- Cargar los 15 archivos a la vez agota la ventana y deja poco espacio para razonar (Guía PDF p. 157; Guía PDF p. 247).
- **Contradicción entre fuentes:** la web afirma que /compact conserva la información importante (web 5.4), mientras el banco advierte que puede perder un hallazgo específico (Q74); prevalece el banco: el scratchpad es la técnica recomendada para preservar hallazgos entre fases (Q74). Además, la web señala que, según la documentación actual de subagents, un subagent reanudado conserva su historial completo, pero indica que en el examen se responde con el state manifest (web 5.4).

## Tarea 5.5 — Design human review workflows and confidence calibration (Diseñar flujos de revisión humana y calibración de confianza)

> Prioridad de estudio: Routing a revisión humana por confianza (67% en el mapa de refuerzo)

### Cuándo enrutar a revisión humana (routing)

**Concepto:** Human-in-the-loop es un flujo donde una persona revisa y aprueba la salida antes de que entre al sistema downstream (Guía PDF p. 248). Se enruta a revisión cuando la salida es incierta, novedosa o de alto riesgo (Guía PDF p. 248).

**Ejemplos de uso (3, cortos):**
1. Low confidence: el modelo señala incertidumbre sobre una extracción o decisión, así que se verifica por una persona (Guía PDF p. 248).
2. Novel input: un formato de documento nuevo o un segmento de clientes nuevo, donde el sistema no tiene base de calibración (Guía PDF p. 248).
3. Conflicting sources: información contradictoria de varias fuentes que una persona puede resolver y el modelo no (Guía PDF p. 248).

Otros criterios: high stakes (transacciones financieras, registros médicos, documentos legales), donde la revisión es una red de seguridad sin importar la confianza (Guía PDF p. 248). Los reviewers reciben primero campos de baja confianza, documentos ambiguos o contradictorios, tipos con mala precisión histórica y campos con varias interpretaciones posibles (web 5.5).

**Qué NO hacer:**
- Over-escalating: enviar a una persona casos sencillos que el agente podía manejar (Slides PDF p. 1471).
- Under-escalating: intentar resolver de forma autónoma situaciones que requieren juicio humano (Slides PDF p. 1471).
- Enrutar todo a revisión humana, lo que anula el propósito de la automatización (Guía PDF p. 250).

**Posible confusión con otros conceptos:**
- Over-escalating vs. under-escalating — ambos modos de fallo cuestan; el objetivo es la calibración (Slides PDF p. 1471).

### El truco de las métricas agregadas (aggregate metrics trap)

**Concepto:** Aggregate accuracy es la cifra única de precisión global, que puede ocultar un segmento que falla gravemente (Guía PDF p. 248). Es el error más peligroso en sistemas de extracción en producción (web 5.5).

**Ejemplos de uso (3, cortos):**
1. Un sistema con 96% global tenía 99% en standard invoices, 79% en scanned paper invoices y 68% en handwritten receipts (Guía PDF p. 248).
2. Con 80% / 12% / 8% del volumen y 98% / 79% / 68% de precisión, el agregado es 94%; quienes envían handwritten receipts sufren errores en un tercio de sus documentos (Guía PDF p. 249).
3. En la web, un 97% global ocultaba fechas al 99.5% en standard invoices, 60% en handwritten receipts, 72% en scanned PDFs y 45% en international formats (web 5.5).

**Qué NO hacer:**
- Decidir qué automatizar solo con métricas agregadas; hay que validar por document type y field segment antes (web 5.5; Q75).
- Confiar en una única cifra de precisión sin mirar segmentos (Guía PDF p. 250).
- Pensar que la preocupación principal es el 3% de error o una política de revisión permanente: el riesgo es el enmascaramiento de segmentos débiles (Q75).

**Posible confusión con otros conceptos:**
- Aggregate accuracy — una sola cifra dominada por el tipo de mayor volumen (Guía PDF p. 248).
- Precisión por segmento — cifra accionable por tipo de documento y campo (web 5.5).

### Priorización de la capacidad de los reviewers

**Concepto:** Los reviewers son caros y limitados, así que los ítems de mayor incertidumbre se les enrutan primero (web 5.5). La cola se mantiene ordenada por incertidumbre de forma dinámica: al terminar un ítem, el siguiente es el de mayor incertidumbre restante, no el siguiente cronológico (web 5.5).

**Ejemplos de uso (3, cortos):**
1. Campos con baja confianza del modelo van antes que los demás (web 5.5).
2. Extracciones de documentos ambiguos o contradictorios, y de tipos con precisión histórica pobre, se revisan primero (web 5.5).
3. Una cola que reordena por incertidumbre conforme llegan documentos y sirve el siguiente ítem más incierto al reviewer libre (web 5.5).

**Qué NO hacer:**
- Repartir la capacidad de revisión uniformemente: desperdicia tiempo en ítems de alta confianza y deja poca capacidad para los inciertos (web 5.5).
- Servir la cola en orden cronológico (web 5.5).

**Posible confusión con otros conceptos:**
- Prioridad por incertidumbre — la cola se ordena por incertidumbre (web 5.5).
- Orden de llegada — no es el criterio correcto (web 5.5).

### Validación antes de automatización (orden de pasos)

**Concepto:** El orden importa: (1) medir precisión por document type y field segment, no agregada; (2) calibrar scores con labelled validation sets; (3) fijar umbrales calibrados; (4) implementar stratified random sampling continuo; (5) solo entonces reducir la revisión humana en segmentos con precisión validada y consistente (web 5.5).

**Ejemplos de uso (3, cortos):**
1. Automatizar standard invoices mientras el personal revisa los recibos de obra (web 5.5).
2. Empezar con un umbral conservador, medir lo que pasa automáticamente y ajustar (Guía PDF p. 248).
3. Usar los resultados de la revisión como feedback loop para mejorar el sistema (Guía PDF p. 250).

**Qué NO hacer:**
- Saltar directamente al paso 5 basándose en métricas agregadas (web 5.5).
- Aprobar la automatización total de un flujo con solo un 97% global (Q75).

### Stratified sampling (muestreo estratificado)

**Concepto:** Stratified sampling mide la precisión dentro de cada segmento (tipo de documento, categoría, fuente) en lugar de sobre todo el dataset (Guía PDF p. 248). En la web se describe como seleccionar una muestra representativa de cada estrato (document type, confidence band, field type) que verifican personas (web 5.5).

**Ejemplos de uso (3, cortos):**
1. Segmentar por document type, source, category o cualquier dimensión donde el rendimiento pueda variar y medir cada segmento por separado (Guía PDF p. 249).
2. Un 72% en handwritten receipts es accionable: añadir ejemplos, ajustar el schema o enrutar todos los handwritten receipts a revisión (Guía PDF p. 249).
3. Muestrear extracciones de alta confianza, porque son automatizadas y nadie las ve; solo así se detecta un patrón de error nuevo, como un layout cambiado de un proveedor nuevo (web 5.5).

El muestreo tiene dos propósitos: medir la precisión periódicamente para confirmar que cada segmento mantiene su tasa validada, y detectar patrones de error novedosos ausentes del validation set original (web 5.5).

**Qué NO hacer:**
- Muestrear solo extracciones de baja confianza: ya van a revisión, y un error nuevo en las de alta confianza pasaría inadvertido (web 5.5).
- Usar random sampling simple con datasets que tienen casos límite raros pero importantes (Guía PDF p. 250).
- Aumentar el tamaño global de la muestra cuando un tipo concreto falla (Guía PDF p. 250).

**Posible confusión con otros conceptos:**
- Random sampling — mide la precisión global y deja ocultos segmentos débiles (Guía PDF p. 249).
- Stratified sampling — mide cada segmento y no omite nada si los segmentos están bien definidos (Guía PDF p. 249).

### Calibración de confianza por campo (field-level confidence calibration)

**Concepto:** Un confidence score es la estimación del modelo de que un campo extraído es correcto; la calibración lo compara con respuestas correctas conocidas (web 5.5). Los scores crudos no están calibrados y no hay una correspondencia fiable entre, por ejemplo, 0.85 y una tasa de error aceptable sin un labeled validation set (web 5.5; Q76).

**Ejemplos de uso (3, cortos):**
1. El modelo devuelve cada campo con `value` y `confidence`, p. ej. `totalAmount` con 0.72 y `lineItems` con 0.61 (web 5.5).
2. Se ejecuta el modelo sobre documentos con extracciones correctas conocidas y se construye una calibration curve (web 5.5).
3. La curva puede mostrar que 0.90 en campos de fecha acierta el 94% de las veces y 0.90 en campos de importe solo el 82% (web 5.5).

```json
{
"vendorName": {"value": "Acme Corp", "confidence": 0.98},
"invoiceDate": {"value": "2024-03-15", "confidence": 0.95},
"totalAmount": {"value": "$1,247.83", "confidence": 0.72},
"lineItems": {"value": [...], "confidence": 0.61}
}
```

Los umbrales calibrados dirigen el routing: por encima, automatizado con stratified sampling; por debajo, revisión humana; en la zona ambigua, revisión humana priorizada (web 5.5). Los scores son relativos, no absolutos: scores iguales en campos distintos no garantizan igual precisión (web 5.5).

**Qué NO hacer:**
- Usar el confidence score crudo directamente como umbral de routing (Q76).
- Asumir que confidence scores solo sirven con una única extracción: se pueden aplicar a nivel de campo en documentos multicampo (Q76).

**Posible confusión con otros conceptos:**
- Confidence score crudo — estimación del modelo, sin garantía de precisión (web 5.5).
- Umbral calibrado — corte basado en precisión real medida con ground truth (web 5.5; Q76).

### Umbrales de confianza y gestión de la cola de revisión

**Concepto:** Un confidence threshold es la puntuación por debajo de la cual la salida va a revisión humana en lugar de aceptarse automáticamente (Guía PDF p. 248). Se fija según el coste de los errores del dominio; las aplicaciones financieras necesitan umbrales más altos que los resúmenes internos (Guía PDF p. 248).

**Ejemplos de uso (3, cortos):**
1. Un sistema de facturas empieza con umbral 0.85: sobre 0.85 hay 92% de precisión, bajo 0.85 hay 64%, y la cola es el 15% del total (Guía PDF p. 248; Guía PDF p. 249).
2. Si la precisión sobre el umbral bajara, el umbral debería subir (Guía PDF p. 249).
3. Si los reviewers aprueban de forma consistente un patrón de baja puntuación, ese patrón podría aceptarse automáticamente (Guía PDF p. 250).

Gestión de la cola: si más del 25% de la salida va a revisión, el umbral es demasiado estricto o el modelo tiene problemas con ese tipo de entrada (Guía PDF p. 250). Si la cola crece más rápido de lo que procesan los reviewers, se ajusta el umbral o se añaden reviewers (Guía PDF p. 250). Una baja inter-rater agreement indica que la tarea es ambigua y que las guidelines de revisión pueden necesitar mejora (Guía PDF p. 250).

**Qué NO hacer:**
- Fijar el umbral una vez y no ajustarlo nunca; se empieza conservador y se mide la precisión de lo que pasa automáticamente (Guía PDF p. 248; Guía PDF p. 250).
- Enrutar todo a revisión (Guía PDF p. 250).

### Trampas del examen

- Usar la precisión agregada (p. ej. 97%) para justificar automatizar todas las extracciones de alta confianza: oculta el rendimiento por tipo; lo correcto es validar por document type y field segment y calibrar los scores (web 5.5; Q75). En Q75, A falla porque describe la tasa de error y no el enmascaramiento; C plantea representatividad del validation set, que no es la preocupación principal; D es un argumento de política que no aborda la brecha analítica (Q75).
- Usar el confidence score crudo como umbral (Q76): lo correcto es calibrar con un labeled validation set. A (coste en tokens) es una preocupación menor; C es falsa porque los scores se aplican a nivel de campo; D es un compromiso de ingeniería, no un fallo del enfoque (Q76).
- Muestrear solo extracciones de baja confianza: un patrón de error nuevo en las de alta confianza solo lo detecta el stratified random sampling (web 5.5).
- Repartir la capacidad de revisión uniformemente en lugar de priorizar la mayor incertidumbre (web 5.5).
- Escenario de práctica (97% global, automatizar con confianza > 95%): el riesgo crítico es que la precisión agregada puede enmascarar un rendimiento pobre por tipo y que los scores requieren calibración; fallan exigir siempre revisión humana, subir el umbral a 99% y asumir que el modelo se volverá sobreconfiado (web 5.5).
- Si la pregunta describe alta precisión global pero un tipo concreto fallando, la respuesta es stratified sampling por segmento, no aumentar el tamaño global de la muestra ni confiar en el agregado (Guía PDF p. 250).
- Errores típicos: confiar en una cifra agregada, fijar el umbral una vez, enrutar todo a revisión, usar random sampling con casos límite raros (Guía PDF p. 250).
- **Contradicción entre fuentes:** no hay contradicción factual. Matiz: la guía define stratified sampling como medir la precisión por segmento (Guía PDF p. 248), mientras la web lo describe como muestrear cada estrato, incluidas bandas de confianza, para verificación humana (web 5.5); prevalece la guía y ambas son compatibles. Las cifras de los ejemplos difieren (Guía PDF p. 248: 96%; web 5.5: 97%) porque son ejemplos distintos.

## Tarea 5.6 — Preserve information provenance and handle uncertainty in multi-source synthesis (Preservar la procedencia de la información y manejar la incertidumbre en la síntesis multifuente)

### Provenance y claim-source mapping

**Concepto:** Provenance es el registro de dónde vino cada pieza de información (Guía PDF p. 250). Un claim-source mapping es el vínculo entre una afirmación concreta de la salida y la(s) fuente(s) que la respaldan (Guía PDF p. 250; web 5.6). Sin provenance la síntesis no se puede verificar, actualizar ni confiar en ella (Guía PDF p. 251).

Cada hallazgo debe llevar cinco campos: claim, source URL, document name, relevant excerpt y publication date (web 5.6). En el ejemplo de la guía, cada entrada de un array `claims` lleva el texto, el identificador de la fuente y opcionalmente página o sección; si una afirmación tiene varias fuentes se listan todas (Guía PDF p. 251).

```json
{
"claim": "Global renewable energy investment reached $495 billion in 2023",
"sourceUrl": "https://example.com/iea-report-2024",
"documentName": "IEA World Energy Investment Report 2024",
"relevantExcerpt": "Total investment in renewable energy technologies reached approximately $495 billion in calendar year 2023, representing a 17% increase over 2022.",
"publicationDate": "2024-06-15"
}
```

**Ejemplos de uso (3, cortos):**
1. Un hallazgo "los precios de las válvulas subieron" incluye URL del informe, título, frase de respaldo y fecha de publicación (web 5.6).
2. "Revenue grew 12% last quarter (Q3 2026 earnings report, p. 4)" es verificable, mientras que sin la cita solo es útil (Guía PDF p. 251).
3. Si una fuente resulta errónea, la provenance indica qué afirmaciones de la síntesis quedan afectadas (Guía PDF p. 251).

**Qué NO hacer:**
- Incluir una afirmación sin respaldo de ninguna fuente como si fuera un hecho; debe omitirse o marcarse como inferencia propia del modelo (Guía PDF p. 251).
- Presentar inferencias del modelo como si fueran afirmaciones con fuente (Guía PDF p. 254).
- Dejar los campos como opcionales: el ejercicio de la web pide que los cinco campos sean obligatorios (web 5.6).

**Posible confusión con otros conceptos:**
- Lista genérica "Sources consulted" — enumera las fuentes accedidas pero no vincula cada afirmación con su fuente (Q77).
- Log de salidas crudas de los subagentes — guarda datos como respaldo pero no integra la provenance en el informe (Q77).

### Pérdida de atribución en la síntesis (source laundering)

**Concepto:** La atribución se pierde al resumir: el agente de síntesis comprime y parafrasea, y sin instrucciones explícitas los detalles de la fuente desaparecen (web 5.6). El paso más común de fallo es la síntesis que parafrasea sin conservar los mappings (web 5.6). La guía llama source laundering a pasar un hecho a otro agente sin atribución, de modo que el agente posterior lo presenta como hallazgo propio (Guía PDF p. 253).

La solución exige tres cosas: los subagentes emiten hallazgos en formato claim-source estructurado; el agente de síntesis recibe la instrucción de mantener los mappings al combinar; y la salida final incluye citas en línea o una sección de referencias que traza cada afirmación a su fuente (web 5.6). Cada traspaso entre agentes debe preservar el mapping, y el coordinator debe fusionar las salidas conservando las atribuciones en lugar de resumirlas en prosa (Guía PDF p. 253).

El pipeline tiene cuatro pasos y cualquiera puede perder la atribución: research subagent con mappings, analysis subagent que añade evaluación preservando los mappings, synthesis subagent que fusiona los mappings y report generation con citas en línea (web 5.6).

**Ejemplos de uso (3, cortos):**
1. Sin instrucciones, la síntesis produce "Investment in renewable energy has grown significantly", sin monto, fuente ni fecha (web 5.6).
2. El Agente A extrae un claim de la Fuente X con atribución, pero al llegar al informe final se presenta como hecho general sin fuente (Guía PDF p. 253).
3. El prompt del agente de síntesis exige que cada afirmación de su salida sea trazable a una fuente concreta (web 5.6).

**Qué NO hacer:**
- Resumir los hallazgos de los subagentes en prosa, porque los detalles de la fuente embebidos en la prosa se pierden (web 5.6; Guía PDF p. 253).
- Trazar la afirmación solo hasta "the search agent" en vez de la fuente original (Guía PDF p. 253).
- Eliminar la atribución por completo en los traspasos entre agentes (Guía PDF p. 254).

**Posible confusión con otros conceptos:**
- Paso de verificación posterior a la síntesis — revisa afirmaciones después, pero no evita la pérdida estructural de provenance (Q77).

### Manejo de conflictos entre fuentes

**Concepto:** Un source conflict ocurre cuando dos o más fuentes dan valores distintos para el mismo hecho (Guía PDF p. 250). El enfoque correcto es anotar el conflicto con ambos valores y su atribución completa, y dejar que decida el consumidor que lee la salida (web 5.6; Guía PDF p. 251). Elegir un valor arbitrariamente (el más reciente, el promedio o el del editor más autoritativo) destruye información y presenta falsa certeza (web 5.6).

Ejemplo de la web: 12% según IEA World Energy Report (publicado junio 2024, datos del año calendario 2023) frente a 8% según Bloomberg NEF Annual Review (publicado marzo 2024, datos julio 2022–junio 2023); la diferencia puede reflejar períodos y métodos distintos (web 5.6).

**Ejemplos de uso (3, cortos):**
1. Dos fuentes contemporáneas discrepan: se presentan ambos valores con sus fuentes (Guía PDF p. 251).
2. Dos fuentes usan definiciones distintas: se anota la diferencia de definición y no se tratan como la misma métrica (Guía PDF p. 252).
3. En el JSON de la guía, el claim de adopción empresarial de 72% lleva la nota "IDC reports 74%", anotando el conflicto en vez de resolverlo en silencio (Guía PDF p. 251).

**Qué NO hacer:**
- Promediar: produce un número que ninguna fuente reportó, que parece preciso y es fabricado (Guía PDF p. 252).
- Elegir uno en silencio, lo que crea invented consensus: el resultado se lee como si todas las fuentes coincidieran (Guía PDF p. 251; Guía PDF p. 253).
- Eliminar la métrica por completo (Guía PDF p. 254).

**Posible confusión con otros conceptos:**
- Invented consensus — el modelo resuelve el conflicto en silencio eligiendo o promediando (Guía PDF p. 251).
- Source laundering — un hecho pasa de un agente a otro sin atribución (Guía PDF p. 253).

### Conciencia temporal (publication date)

**Concepto:** Las fechas de publicación o de recolección de datos son contexto temporal que debe preservarse; explican por qué dos números difieren (web 5.6). Con fechas, 8% (informe de 2023) y 12% (informe de 2024) muestran una tendencia de aceleración y no una contradicción (web 5.6). La guía indica revisar las fechas primero: una fuente de 2026 que actualiza una cifra de 2024 es una corrección, no un conflicto (Guía PDF p. 251).

Los subagentes incluyen las fechas, el agente de síntesis las preserva al fusionar y la salida final las muestra junto a los datos (web 5.6). Sin ellas, el agente puede leer una tendencia válida como problema de calidad de datos y marcar o suprimir hallazgos consistentes (web 5.6).

**Ejemplos de uso (3, cortos):**
1. Exigir fecha de publicación o recolección en todas las salidas estructuradas (web 5.6).
2. Una fuente más nueva que actualiza a otra más antigua: usar el valor nuevo y anotar la actualización (Guía PDF p. 252).
3. Revisar las fechas antes de tratar un desacuerdo como conflicto (Guía PDF p. 254).

**Qué NO hacer:**
- Suponer que números distintos de fuentes distintas son contradicciones (web 5.6).
- Usar el valor más antiguo cuando una fuente más nueva actualiza a otra (Guía PDF p. 252).

### Jerarquía de autoridad de las fuentes

**Concepto:** Las fuentes primary (informes oficiales, mediciones directas, datos de primera mano; ej. SEC filings) tienen la mayor autoridad y se usan cuando están disponibles y vigentes; las secondary (noticias, informes de analistas) tienen autoridad media y se usan si no hay primaria o por contexto; las tertiary (enciclopedias, directorios, sitios agregadores) tienen la menor y sirven solo como referencia rápida (Guía PDF p. 252).

**Ejemplos de uso (3, cortos):**
1. Un SEC filing frente a un artículo de noticias: pesa más la fuente primaria (Guía PDF p. 252).
2. Un informe de analistas se usa para contexto cuando no hay fuente primaria (Guía PDF p. 252).
3. Cuando una fuente tiene mayor autoridad, se anota la diferencia de autoridad (Guía PDF p. 252).

**Qué NO hacer:**
- Promediar los valores cuando una fuente tiene mayor autoridad; la resolución es anotar la diferencia (Guía PDF p. 252).
- Elegir de forma arbitraria el valor del editor más autoritativo como sustituto de anotar ambos (web 5.6).

### Análisis con conflictos intactos y cobertura honesta

**Concepto:** Cuando el analysis agent encuentra valores en conflicto en un documento, completa su trabajo incluyéndolos y anotándolos explícitamente; no los resuelve, porque esa decisión corresponde al coordinator o al consumidor (web 5.6). El coordinator decide entonces: presentar ambos valores, investigar más o escalar a un analista humano (web 5.6). Del mismo modo, la síntesis debe ser honesta sobre la cobertura de las fuentes (Guía PDF p. 255).

```json
{
"field": "annualRevenue",
"conflictDetected": true,
"values": [
{
"value": "$4.2M",
"source": "Annual Report 2023",
"context": "Audited financial statements, fiscal year ending December 2023"
},
{
"value": "$3.8M",
"source": "SEC Filing Q4 2023",
"context": "Preliminary unaudited figures, calendar year 2023"
}
],
"possibleExplanation": "Difference may reflect audited vs preliminary figures and fiscal vs calendar year reporting periods"
}
```

**Ejemplos de uso (3, cortos):**
1. El analysis agent registra con `conflictDetected: true` los dos valores de `annualRevenue` con fuente, contexto y posible explicación (web 5.6).
2. Con tres fuentes, A devuelve datos, B un resultado vacío válido y C un timeout: la síntesis incluye los datos de A, indica que B no tenía datos y anota que C no pudo alcanzarse (Guía PDF p. 255).
3. Un informe donde tres fuentes independientes coinciden y una sola menciona escasez lo dice explícitamente, separando hallazgos bien establecidos de los controvertidos (web 5.6).

**Qué NO hacer:**
- Que el analysis agent resuelva el conflicto por su cuenta (web 5.6).
- Devolver solo los resultados de A y B sin mencionar C, lo que hace que el informe parezca cubrir todas las fuentes (Guía PDF p. 255).

**Posible confusión con otros conceptos:**
- Resultado vacío válido (B) — la fuente respondió sin datos coincidentes; no es un fallo (Guía PDF p. 255).
- Fallo de fuente (C) — se reporta como error estructurado (timeout, retryable) (Guía PDF p. 255).

### Renderizado según el tipo de contenido

**Concepto:** El agente de síntesis elige el formato según el tipo de contenido; forzar todo a un solo formato (todo tablas, prosa o listas) perjudica la lectura y comprensión (web 5.6). Datos financieros en tablas, noticias y eventos actuales en prosa, hallazgos técnicos en listas estructuradas (web 5.6).

**Ejemplos de uso (3, cortos):**
1. Inversión por año (2021: 366, 12%; 2022: 423, 16%; 2023: 495, 17%) en una tabla (web 5.6).
2. Un cambio de propiedad de un proveedor en un párrafo (web 5.6).
3. Requisitos de instalación o especificaciones de API en una lista con jerarquía (web 5.6).

**Qué NO hacer:**
- Renderizar todos los tipos de contenido en un formato uniforme (web 5.6).

### Trampas del examen

- Banco (Q77): informe con "AI adoption in healthcare reached 45% in 2024" sin fuente. La respuesta correcta es B: subagentes con claim-source mappings estructurados (claim text, source URL, document name, relevant excerpt) y síntesis que los preserva y fusiona (Q77). A falla porque una sección genérica "Sources consulted" no vincula afirmaciones con fuentes concretas (Q77). C falla porque guardar salidas crudas en un log no integra la provenance en el informe (Q77). D falla porque revisar después no previene la pérdida estructural (Q77).
- Seleccionar la fuente más reciente cuando dos fuentes creíbles chocan: destruye información; hay que anotar ambos valores con atribución y fechas (web 5.6).
- Promediar (p. ej., 10%) con una nota de varianza: produce un número que ninguna fuente publicó (Guía PDF p. 252; web 5.6).
- Escalar a un humano antes de incluir el valor: en el escenario práctico, con informes en calendario fijo sin paso humano, la opción correcta es anotar ambos valores con fuente y fecha (web 5.6).
- Tratar números distintos como contradicciones: las fechas de publicación o de recolección suelen explicarlos (web 5.6; Guía PDF p. 254).
- Dejar que la síntesis parafrasee sin preservar los mappings: la prosa pierde los detalles de la fuente; los subagentes deben emitir datos estructurados (web 5.6; Guía PDF p. 253).
- Formato uniforme para todo el contenido (web 5.6).
- Cuando la guía describe dos fuentes con cifras distintas y un informe con un solo número sin atribución, la respuesta es preservar los mappings, anotar el conflicto y usar fechas; nunca promediar, elegir uno en silencio ni eliminar la métrica (Guía PDF p. 254).
- **Contradicción entre fuentes:** la web rechaza elegir la fuente más reciente cuando dos fuentes creíbles chocan (web 5.6), mientras que la guía indica usar el valor más nuevo, anotando la actualización, cuando una fuente nueva actualiza a una antigua (Guía PDF p. 252). Prevalece la guía: la fuente nueva que actualiza es una corrección, y solo los desacuerdos entre fuentes contemporáneas se anotan con ambos valores (Guía PDF p. 251).

## Ideas clave

- La context window es una memoria de trabajo finita que se gestiona como presupuesto de tokens; el context rot hace menos fiable una ventana más llena y una ventana mayor no elimina la necesidad de gestionarla (Guía PDF p. 231; Guía PDF p. 234).
- La progressive summarisation destruye importes, fechas e identificadores; la solución es un persistent case facts block en cada prompt, fuera del historial resumido y reinyectado tras la compaction (web 5.1; Q69; Guía PDF p. 238).
- Lost in the middle es un problema posicional: se mitiga con un resumen de hallazgos clave al principio y cabeceras de sección, no con `max_tokens` ni con instrucciones de "prestar atención" (Q70; web 5.1).
- Recorta los tool results a los campos relevantes antes de que entren al historial, y haz que los agentes upstream devuelvan datos estructurados en vez de razonamiento verboso (web 5.1; Guía PDF p. 237). El prompt caching reduce coste y latencia, pero no encoge la ventana (Guía PDF p. 233).
- Ante una petición explícita de humano se escala de inmediato, sin investigar antes; la frustración sin esa petición se atiende reconociéndola y ofreciendo resolución (web 5.2; Q71; Guía PDF p. 239).
- Los triggers válidos de escalación son petición explícita, brecha de política, límite de autoridad y fallo repetido; sentiment y confianza autorreportada son poco fiables, y la calibración se corrige con criterios explícitos y few-shot en el system prompt (web 5.2; Guía PDF p. 239; Q3).
- Las coincidencias ambiguas se resuelven pidiendo identificadores adicionales, no con heurísticas; el traspaso a un humano debe llevar motivo, case facts, pasos realizados, estado y acción recomendada (web 5.2; Guía PDF p. 240).
- Un error útil es estructurado (categoría, qué se intentó, resultados parciales, alternativas, retryable); un access failure no es un valid empty result, y ambos anti-patterns, silent suppression y workflow termination, deben evitarse (web 5.3; Guía PDF p. 242; Q72).
- Recupera localmente los fallos transient antes de propagar, y practica coverage honesty: anota qué se completó, qué no y por qué, porque un resultado parcial honesto vale más que uno que parece completo (web 5.3; Guía PDF p. 244).
- En exploraciones largas de código, la degradación viene de la salida verbosa y no de falta de tokens: usa scratchpad files, subagents con contexto aislado, summary injection entre fases, `/compact` proactivo y state manifests para recuperar crashes (web 5.4; Guía PDF p. 245; Q73; Q74).
- La precisión agregada oculta segmentos débiles: valida por document type y field segment, calibra los confidence scores con un labeled validation set, fija umbrales ajustables, prioriza la cola por incertidumbre y aplica stratified sampling, incluida la salida de alta confianza (web 5.5; Guía PDF p. 248; Q75; Q76).
- Cada afirmación de una síntesis debe conservar su claim-source mapping y su publication date; los conflictos se anotan con ambos valores y su atribución, sin promediar ni elegir en silencio, y una fuente nueva que actualiza a otra es una corrección (web 5.6; Guía PDF p. 251; Guía PDF p. 252; Q77).
