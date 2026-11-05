# Claude Certified Architect – Foundations (CCA-F) — Anthropic (guía de examen, 2026)

## Dominio 2 — Tool Design & MCP Integration (Diseño de herramientas e integración MCP)

> Nota de extracción: este apunte combina cinco fuentes: la guía en PDF «Tutorials Dojo Study Guide and Cheat Sheets – Claude Certified Architect Foundations (CCA-F)», las slides en PDF del curso en video (Tutorials Dojo, junio 2026), el banco de 77 preguntas de práctica «Claude Certified Architect. Foundations: Practice Exam» y las lecciones web de claudecertificationguide.com (sitio independiente de terceros, no afiliado a Anthropic). Citas: `(Guía PDF p. N)` y `(Slides PDF p. N)` usan la página del PDF; `(web N.M)` remite a la lección N.M de la web; `(QN)` remite a la pregunta N del banco. Si las fuentes se contradicen, prevalecen la guía y el banco sobre la web. Las slides tienen muchas páginas que son solo imagen y no se pudieron leer, por lo que su cobertura es parcial. Discrepancia entre fuentes sin resolver: el banco y la guía llaman al examen «CCA-F» y el banco indica 77 preguntas de práctica y una nota mínima de 720 (escala 100-1.000); la web lo llama «CCAR-F» e indica 60 preguntas en 120 minutos, aprobado con 720/1.000 y credencial válida 12 meses. No se decide cuál es la correcta.

## Lo que necesitas saber

El Dominio 2 (Tool Design & MCP Integration) pesa un 18% del examen y trata de cómo se diseñan, distribuyen e integran las herramientas que usa Claude. Parte de una idea central: Claude no ejecuta las herramientas, sino que envía una solicitud estructurada con nombre y parámetros, y elige la herramienta leyendo sus descripciones, que son el mecanismo primario de selección (Guía PDF p. 73; web 2.1; Q2). Por eso la calidad de la tool description, de los parámetros y de los límites entre herramientas determina si el agente enruta bien o produce misrouting (Guía PDF p. 77).

Las cinco tareas del dominio se encadenan de lo interno a lo externo. La Tarea 2.1 fija la interfaz de cada herramienta (descripciones con límites explícitos, tool splitting, renombrado, descripciones de parámetros). La Tarea 2.2 define cómo debe responder una herramienta MCP cuando falla: `isError` (`is_error` en la guía), categoría de error, `isRetryable` y la distinción entre access failure y valid empty result (web 2.2; Guía PDF p. 81; Guía PDF p. 82). La Tarea 2.3 reparte las herramientas entre agentes con least privilege (`allowedTools`, scoped cross-role tools) y controla cuándo se llama a una herramienta con `tool_choice` (`auto`, `any`, forced selection y, según la guía, `none`) (Guía PDF p. 83; Guía PDF p. 86). La Tarea 2.4 integra servidores MCP en Claude Code: tools, resources y prompts, scope `.mcp.json` frente a `~/.claude.json` y expansión de variables de entorno `${VAR}` (Guía PDF p. 89; Guía PDF p. 134; web 2.4). La Tarea 2.5 cubre las herramientas integradas (Read, Write, Edit, Bash, Grep, Glob) y cómo explorar código de forma incremental (Guía PDF p. 94; Guía PDF p. 95; web 2.5).

Al terminar el dominio sales sabiendo escoger la herramienta adecuada para cada situación: mejorar descripciones antes que añadir routing classifiers o few-shot examples (web 2.1; Q2), devolver errores estructurados en lugar de mensajes genéricos (Q32), forzar una herramienta concreta con `tool_choice` cuando la llamada debe ocurrir sí o sí (Q36), compartir servidores de equipo en `.mcp.json` sin exponer secretos (Q37) y usar Grep para contenido y Glob para rutas (Q39; Guía PDF p. 95).

Tareas marcadas como prioridad de estudio: 2.1 (descripciones de herramientas, 0% en los intentos 1 y 2), 2.2 (errores MCP estructurados, 50%), 2.3 (tool_use + tool_choice, regresión de 100% a 0%), 2.4 (scope de servidores MCP, regresión de 100% a 0%, e integración MCP con env vars, 25%) y 2.5 (exploración con Grep/Glob/Read, 50%).

## Tarea 2.1 — Design effective tool interfaces with clear descriptions and boundaries (Diseñar interfaces de herramientas efectivas con descripciones y límites claros)

> Prioridad de estudio: Descripciones de herramientas (0% en los intentos 1 y 2)

### La descripción como mecanismo principal de selección
**Concepto:** Las tool descriptions son el mecanismo primario que usan los LLM para elegir una herramienta; no son metadatos accesorios (web 2.1; Q2). Una tool definition tiene tres partes: name (impacto menor), description (impacto mayor, señal primaria de selección) e input schema (impacto mayor, determina si Claude puede construir una llamada válida) (Guía PDF p. 74; Guía PDF p. 75).

**Ejemplos de uso (3, cortos):**
1. Ante "look up this order", Claude no busca una función llamada lookupOrder: lee las descripciones de todas las herramientas y elige la que mejor encaja con la intención (Guía PDF p. 73).
2. Una herramienta con nombre engañoso pero buena descripción se selecciona bien, porque Claude pesa más la descripción que el nombre (Guía PDF p. 74).
3. Claude no ejecuta las herramientas: envía una solicitud estructurada con nombre y parámetros, y tu código decide si ejecutar, rechazar o modificar (Guía PDF p. 73).

**Qué NO hacer:**
- Escribir la descripción para un lector humano en vez de para Claude (p. ej. "This tool searches orders" en lugar de "Use this tool when the customer asks about order status…") (Guía PDF p. 79).
- Confiar en que el nombre lleve el significado mientras Claude lee la descripción (Guía PDF p. 75).
- Usar descripciones mínimas como "Retrieves customer information", que no permiten distinguir herramientas solapadas (web 2.1).

**Posible confusión con otros conceptos:**
- Few-shot examples — arreglan formato de salida y juicio, no la selección de herramienta (Guía PDF p. 77).
- Prompt, modelo o historial — ante una llamada a la herramienta equivocada, lo primero que se revisa son las tool descriptions, no el prompt, ni el modelo, ni el historial (Guía PDF p. 75).

### Los cinco elementos de una descripción de producción
**Concepto:** Una descripción de nivel producción incluye cinco elementos: qué hace, qué entradas espera (tipos, formatos, restricciones, obligatorios/opcionales), ejemplos de consultas que maneja bien, casos límite y limitaciones, y límites explícitos (cuándo usarla frente a herramientas similares) (web 2.1; Slides PDF p. 314). Si falta uno, "the AI guesses" (Slides PDF p. 314).

**Ejemplos de uso (3, cortos):**
1. get_customer: "Looks up a customer account by email address, phone number, or customer ID… Use this when you need to verify who the customer is. Do NOT use for order-specific queries — use lookup_order for those." (web 2.1).
2. lookup_order: acepta número de pedido (formato #NNNNN) o tracking ID y devuelve estado, artículos, envío y elegibilidad de reembolso (web 2.1).
3. En la versión anotada, get_customer indica además un caso límite: "Returns null if no matching account is found" (Slides PDF p. 318).

```text
get_customer: "Looks up a customer account by email address,
phone number, or customer ID. Returns customer profile
(name, contact details, account status, loyalty tier).
Use this when you need to verify who the customer is.
Do NOT use for order-specific queries — use lookup_order
for those."
```

**Qué NO hacer:**
- Omitir la cláusula "Do NOT use": es el elemento más crítico porque da desambiguación explícita incluso con nombres similares o descripciones solapadas, y una frase puede evitar la mayoría de la confusión de enrutamiento (Slides PDF p. 317).
- Dejar sin boundary statement una herramienta: Claude puede usarla para tareas de otra (Guía PDF p. 78).
- Usar jerga técnica sin contexto: Claude puede malinterpretar términos de dominio (Guía PDF p. 78).

### Misrouting y patrón de desambiguación
**Concepto:** El misrouting ocurre cuando Claude elige la herramienta equivocada; la causa habitual es un par de herramientas con descripciones solapadas o difusas (Guía PDF p. 77). El patrón de desambiguación consiste en que cada descripción indique para qué sirve la otra herramienta (Guía PDF p. 77). Con descripciones similares, Claude puede alternar entre ellas al azar (Guía PDF p. 74).

**Ejemplos de uso (3, cortos):**
1. "Check my order #12345" llega a get_customer en lugar de lookup_order porque ambas tienen descripciones mínimas y aceptan formatos de identificador similares (Q2; web 2.1; Slides PDF p. 306).
2. search_orders: "Do NOT use this for product searches, use search_products instead"; y search_products excluye a su vez los order lookups (Guía PDF p. 76; Guía PDF p. 77).
3. get_customer_info (perfil: nombre, email, plan, estado; NO devuelve historial) frente a get_customer_orders (historial; requiere customer_id; NO devuelve perfil) (Guía PDF p. 77).

Marco de diagnóstico de cuatro pasos: reproducir el misrouting encontrando la solicitud exacta que disparó la herramienta equivocada; comparar las descripciones lado a lado buscando solapes de estructura, redacción o alcance implícito; identificar la señal que faltaba (entradas, salidas, cláusula "Do NOT use" o ejemplos); y añadir esa señal a la descripción (Slides PDF p. 309).

**Qué NO hacer:**
- Crear dos herramientas de alcance solapado sin desambiguación (Guía PDF p. 79).
- Arreglar el misrouting con few-shot examples cuando la causa real son descripciones ambiguas (Guía PDF p. 79; Q2).
- Tratar la mala selección como un problema de arquitectura: la causa es señal insuficiente en la descripción (Slides PDF p. 311).

**Posible confusión con otros conceptos:**
- Expandir descripciones (primer paso, bajo esfuerzo) — consolidación, few-shot y routing classifier son opciones secundarias (Slides PDF p. 311; web 2.1).

### Tool splitting (dividir herramientas genéricas)
**Concepto:** Una herramienta genérica con responsabilidades amplias crea ambigüedad porque su descripción encaja con muchas solicitudes; se divide en herramientas con propósito específico y contratos de entrada/salida definidos (web 2.1; Guía PDF p. 110).

**Ejemplos de uso (3, cortos):**
1. analyze_document ("Analyses a document and returns results") se divide en extract_data_points, summarize_content y verify_claim_against_source (web 2.1).
2. extract_data_points extrae campos estructurados (fechas, importes, nombres) de un documento (web 2.1).
3. verify_claim_against_source comprueba si una afirmación está respaldada por el documento fuente, devolviendo evidencia que apoya o contradice (web 2.1).

**Qué NO hacer:**
- Añadir un parámetro mode (mode='extract' o mode='summarize') al mismo analyze_document (Guía PDF p. 110).
- Mantener la herramienta única y arreglarla solo con el system prompt o con ejemplos one-shot (Guía PDF p. 110).

**Posible confusión con otros conceptos:**
- Splitting — consolidación: dividir sirve cuando una herramienta hace demasiado (síntoma: comportamiento y formato de salida inconsistentes) (Guía PDF p. 110); consolidar dos herramientas distintas en una es un cambio arquitectónico válido a largo plazo pero cuesta más esfuerzo que expandir descripciones (web 2.1).

### Tool renaming (renombrar para dar claridad)
**Concepto:** Cuando dos herramientas tienen nombres confusamente similares, renombrar arregla el solapamiento en la interfaz sin tocar la implementación (web 2.1). El nombre es secundario respecto a la descripción, pero debe ser coherente con ella (Guía PDF p. 77).

**Ejemplos de uso (3, cortos):**
1. analyze_content pasa a extract_web_results con una descripción específica para web (web 2.1).
2. Una herramienta de búsqueda de pedidos se llama search_orders, no query ni lookup (Guía PDF p. 77).
3. get_account_info / fetch_account_details / retrieve_customer_record (cada una sobre un backend distinto) se renombran según su fuente de datos y se reescriben las descripciones: qué datos devuelve, qué backend consulta y qué caso de uso cubre (Q31).

**Qué NO hacer:**
- Usar nombres genéricos como helper, process, handle o execute (Guía PDF p. 77).
- Dejar un nombre como process_data junto a una descripción sobre consultas de pedidos: la disonancia resta fiabilidad (Guía PDF p. 77).
- Renombrar sin reescribir las descripciones: Q31 pide ambas cosas (Q31).

### Descripciones de parámetros y formato de entradas
**Concepto:** Cada parámetro del input schema debe tener una descripción que diga a Claude qué pasar; sin ella, Claude infiere el formato solo desde el nombre del parámetro, lo que produce entradas inconsistentes (Guía PDF p. 78). Los errores de formato en los argumentos se reducen poniendo restricciones de formato, valores aceptados y ejemplos en la descripción de la herramienta (Q30).

**Ejemplos de uso (3, cortos):**
1. customer_id: "The unique customer identifier, e.g., 'C-1049'. Required for all customer-specific lookups." (Guía PDF p. 78).
2. date_range: "ISO 8601 date range as {start, end}. Both dates are inclusive. Maximum range: 90 days." (Guía PDF p. 78).
3. status_filter: valores válidos 'pending', 'shipped', 'delivered', 'cancelled'; omitirlo devuelve todos los estados (Guía PDF p. 78).

**Qué NO hacer:**
- Dejar `lookup_order` con "Retrieves order details given a date or identifier" sin formato ni ejemplos, de modo que el agente envía "order from last Tuesday" en vez de ISO-8601 (Q30).
- Corregirlo solo con una instrucción en el system prompt: es más frágil que una descripción específica de la herramienta (Q30).
- Confiar solo en la validación del schema que rechaza entradas mal formadas: no evita que el modelo las envíe y genera ciclos de error innecesarios (Q30).

**Posible confusión con otros conceptos:**
- Problema de formato — problema de desambiguación: dividir `lookup_order` en `lookup_order_by_id` y `lookup_order_by_date` resuelve ambigüedad, no la falta de guía de formato (Q30).

### Interacción con el system prompt
**Concepto:** Instrucciones del system prompt sensibles a palabras clave pueden crear asociaciones no deseadas con una herramienta y anular descripciones bien escritas (web 2.1; Slides PDF p. 310). Es un modo de fallo sutil.

**Ejemplos de uso (3, cortos):**
1. "Always check customer details before proceeding" puede llevar al modelo a llamar get_customer para cualquier consulta relacionada con clientes, digan lo que digan las descripciones (web 2.1; Slides PDF p. 310).
2. Un solo keyword en el system prompt puede inclinar a Claude hacia la herramienta equivocada (Guía PDF p. 75).
3. Tras actualizar las descripciones, se relee el system prompt y se reformula la redacción que coincide con el nombre o tema de una herramienta (web 2.1; Slides PDF p. 310).

**Qué NO hacer:**
- Dar por resuelto el misrouting tras arreglar las descripciones sin revisar el system prompt: puedes dejar las descripciones perfectas y seguir viendo misrouting (Slides PDF p. 310).
- Pasar por alto que el system prompt puede sobrescribir los límites de las descripciones (Slides PDF p. 310).

### Número y similitud de herramientas
**Concepto:** Las descripciones son el arreglo cuando el agente tiene un número manejable de herramientas y no distingue dos; no lo son cuando el problema es el conjunto de herramientas, porque con un conjunto grande la selección se degrada solo por la complejidad de decisión (web 2.1). Ejemplo de la guía de examen según la web: 18 herramientas frente a 4-5 (web 2.1). Esto se trata en la Tarea 2.3 (web 2.1).

**Ejemplos de uso (3, cortos):**
1. Reescribir 22 descripciones no cambia la complejidad de un toolkit sobredimensionado (web 2.1).
2. Cada definición de herramienta (nombre, descripción, schema) consume tokens de contexto; 50 herramientas son un overhead significativo (Slides PDF p. 426).
3. search_documents/retrieve_files y send_email/compose_message son pares demasiado similares; cuando la distinción se difumina el modelo usa lo que le resulta más familiar, no lo más correcto (Slides PDF p. 427).

**Qué NO hacer:**
- Reescribir descripciones sin diagnosticar antes si el problema es la descripción o el tamaño del toolkit (web 2.1).
- Sobrecargar un solo agente: el rango recomendado es 10–20 herramientas por agente y, si hace falta más capacidad, se distribuye (Slides PDF p. 429).

### Trampas del examen
- Few-shot examples como arreglo del misrouting (Q2, opción A): añaden overhead de tokens sin corregir la causa raíz; la confusión viene de descripciones que no diferencian las herramientas (Q2; web 2.1). Los few-shot arreglan formato de salida y juicio, no la selección (Guía PDF p. 77).
- Routing layer/classifier que preselecciona la herramienta por palabras clave (Q2, opción C): sobreingeniería como primer paso; evita la comprensión de lenguaje natural del LLM y añade infraestructura (Q2; web 2.1).
- Consolidar herramientas en `lookup_entity` (Q2, opción D): cuesta más esfuerzo de lo que justifica un "primer paso" (Q2); válido a largo plazo, pero no primero (web 2.1). En Q31, consolidar en una sola herramienta con parámetro `source` (opción C) devuelve la carga de enrutar al modelo de forma menos estructurada (Q31).
- Instrucción en el system prompt que lista cuándo usar cada herramienta (Q31, opción A): puede reducir el misrouting, pero no arregla la raíz, que son descripciones indistinguibles (Q31). Del mismo modo, mejorar el system prompt no arregla analyze_document (Guía PDF p. 110).
- "Always use ISO-8601" en el system prompt (Q30, opción B): más frágil que ponerlo en la descripción de la herramienta (Q30). Validación de schema (Q30, opción C): no impide el envío de entradas mal formadas (Q30). Dividir por id/fecha (Q30, opción D): resuelve otro problema (Q30).
- Aleatorizar la herramienta llamada y fusionar respuestas (Q31, opción D): no es una arquitectura viable (Q31).
- Añadir un parámetro mode o un único ejemplo one-shot a analyze_document en vez de dividirlo: la respuesta correcta es dividirlo en herramientas con contrato de entrada/salida (Guía PDF p. 110).
- Ignorar el system prompt tras actualizar las descripciones: palabras clave pueden anular descripciones bien escritas (web 2.1).
- Culpar al prompt, al modelo o al historial cuando se llama a la herramienta equivocada: lo primero a revisar son las descripciones (Guía PDF p. 75). El examen favorece arreglos de bajo esfuerzo y gran efecto: mejores descripciones antes que routing classifiers (web 2.1).
- **Contradicción entre fuentes:** la web enumera cinco elementos de una buena descripción (qué hace, entradas, ejemplos de consultas, casos límite, límites explícitos) y las slides también (Slides PDF p. 314), mientras la guía lista cuatro (propósito, caso de uso, parámetros, boundaries) (Guía PDF p. 76); la guía prevalece sobre la web, pero ambas coinciden en que los límites explícitos son parte esencial.
- **Contradicción entre fuentes:** la web indica que, según la documentación de Anthropic, la selección se degrada con más de 30 a 50 herramientas y recomienda usar el ejemplo 18 frente a 4-5 de la guía (web 2.1); las slides recomiendan 10–20 herramientas por agente (Slides PDF p. 429). Para el examen prevalecen la guía y el material oficial sobre la web; usa el ejemplo de 18 frente a 4-5 (web 2.1).

## Tarea 2.2 — Implement structured error responses for MCP tools (Implementar respuestas de error estructuradas para herramientas MCP)

> Prioridad de estudio: Errores MCP estructurados (50% en el mapa de refuerzo)

### Respuesta de error estructurada y flag isError

**Concepto:** una respuesta de error estructurada es el resultado que devuelve una herramienta MCP cuando falla; sus metadatos indican la categoría del error, si un reintento puede funcionar y cómo recuperarse (web 2.2). El protocolo MCP aporta el flag `isError` (en la guía aparece como `is_error`): con él el modelo sabe que la ejecución falló y razona sobre la recuperación, en lugar de leer el texto como un resultado normal (web 2.2; Guía PDF p. 82; Guía PDF p. 92).

**Ejemplos de uso (3, cortos):**
1. Un timeout de base de datos se devuelve con `isError: true`, `errorCategory: "transient"` e `isRetryable: true` para que el agente reintente (web 2.2).
2. Un `process_refund` que falla devuelve `errorCategory`, `isRetryable` y una explicación específica del motivo, en vez de "Operation failed" (Q32).
3. El campo `content` lleva los detalles del error como texto que Claude lee y sobre el que razona (Guía PDF p. 82).

**Qué NO hacer:**
- Devolver un mensaje genérico como "Operation failed" o "An error occurred": no dice qué pasó, si reintentar ni qué probar (web 2.2; Guía PDF p. 79; Q32).
- Devolver el error sin `is_error: true`: Claude puede interpretar el texto como datos válidos y extraer datos de un mensaje de error, produciendo una salida sin sentido (Guía PDF p. 92).
- Obligar al agente a parsear el texto de la descripción: es frágil; el agente debe ramificar por la categoría (Guía PDF p. 80; Guía PDF p. 82).

**Posible confusión con otros conceptos:**
- Metadatos de error — `errorCategory`, `isRetryable` y `description` son una convención de aplicación, no parte del envelope MCP; el `CallToolResult` solo define `content`, `structuredContent` e `isError` (web 2.2).
- Patrón de la guía — la guía describe tres campos (`category`, `description`, `retryable`) además de `is_error` (Guía PDF p. 80; Guía PDF p. 104).

### Dos capas de error: protocol errors vs tool execution errors

**Concepto:** la especificación MCP reporta fallos por dos vías distintas. Los protocol errors son respuestas de error JSON-RPC estándar (solicitud mal formada: herramienta inexistente, argumentos que no cumplen el input schema o fallo interno del servidor), sin objeto result; los atiende la aplicación host y el modelo nunca ve un resultado (web 2.2). Los tool execution errors son resultados normales con `isError: true` y el detalle en `content`; el modelo los lee y decide qué hacer (web 2.2).

**Ejemplos de uso (3, cortos):**
1. Un nombre de herramienta mal escrito falla en la capa de protocolo con un `error` con `code` y `message` (web 2.2).
2. Un stock check fallido es un tool execution error: la herramienta se encontró, los argumentos eran válidos y la herramienta se ejecutó (web 2.2).
3. Las cuatro categorías, `isRetryable` y la guía de recuperación describen errores de ejecución, porque el agente razona sobre esa capa (web 2.2).

**Qué NO hacer:**
- Intentar arreglar un protocol error en el bucle de recuperación del agente: se corrige en el tool schema o en el cliente (web 2.2).
- Esperar que el modelo vea un resultado cuando falla la capa de protocolo: ninguna herramienta se ejecutó (web 2.2).

### Las cuatro categorías de error

**Concepto:** todo fallo de herramienta pertenece a una de cuatro categorías, cada una con una estrategia de recuperación distinta; el agente necesita metadatos estructurados para distinguirlas (web 2.2). La guía de examen nombra las cuatro categorías y el booleano `isRetryable` (web 2.2). Q32 las lista como `errorCategory` (transient/validation/permission/business) (Q32).

- transient: timeouts, servicio no disponible, rate limits; la solicitud es válida. Recuperación: reintentar tras una breve espera (web 2.2).
- validation: formato inválido, campos obligatorios ausentes, valores fuera de rango. Recuperación: corregir la entrada y enviar una llamada corregida (web 2.2).
- business: violaciones de política, límites excedidos, conflictos con reglas de negocio; la solicitud es técnicamente válida. Recuperación: no reintentar; flujo alternativo, normalmente escalar (web 2.2).
- permission: acceso denegado, credenciales insuficientes, fallos de autorización. Recuperación: escalar o usar otras credenciales (web 2.2).

```json
{
  "isError": true,
  "content": [{ "type": "text", "text": "Refund exceeds policy limit" }],
  "structuredContent": {
    "errorCategory": "business",
    "isRetryable": false,
    "description": "Refund amount of £750 exceeds the £500 automatic refund limit. This requires manager approval. Please escalate to a human agent with the refund details."
  }
}
```

**Ejemplos de uso (3, cortos):**
1. Un catálogo de proveedor que expira bajo carga: transient (web 2.2).
2. Un ID de pedido con formato incorrecto (`order-abc` en vez de `#NNNNN`): validation (web 2.2).
3. Un reembolso de £750 sobre el límite automático de £500: business, con escalado a una persona (web 2.2).

**Qué NO hacer:**
- Tratar un business error como reintentable: la misma violación de política se aplica siempre (web 2.2; Q34).
- Dar una descripción vaga: la `description` debe ser específica y, en business, una explicación apta para el cliente permite al agente comunicar el motivo (web 2.2; Guía PDF p. 82; Q34).

**Posible confusión con otros conceptos:**
- Business vs permission — business: la solicitud viola una regla (límite de reembolso); permission: quien llama carece de derechos (cuenta de servicio sin acceso a registros financieros) (web 2.2). Las slides listan "Permission denied" entre los business logic failures y también tratan los permission failures como fallos de autorización (Slides PDF p. 348; Slides PDF p. 355).
- Categorías de la guía — la guía usa `timeout`, `rate_limited`, `permission_denied`, `not_found`, `validation_error` y `service_unavailable` (Guía PDF p. 80; Guía PDF p. 81).

### Qué señala isRetryable

**Concepto:** `isRetryable` responde a una sola pregunta: ¿funcionará reenviar esta misma solicitud? Solo los transient llevan `true`; el resto lleva `false` porque algo debe cambiar antes: la entrada (validation), la solicitud (business) o quien llama (permission) (web 2.2). Se lee `isRetryable` para decidir si reenviar sin cambios y luego `errorCategory` para saber qué hacer si no se puede (web 2.2). La guía lo define como si la misma llamada podría tener éxito al reintentar (Guía PDF p. 80).

| Categoría | isRetryable | Recuperación |
|---|---|---|
| transient | true | Reenviar la misma llamada tras una espera (web 2.2) |
| validation | false | Corregir la entrada y enviar una nueva llamada (web 2.2) |
| business | false | Camino alternativo o escalar (web 2.2) |
| permission | false | Reintentar como un principal con el acceso correcto (web 2.2) |

**Ejemplos de uso (3, cortos):**
1. Un timeout de la base de datos: `isRetryable: true` y se reenvía con backoff (web 2.2; Guía PDF p. 80).
2. Un bloqueo por fraude en `check_fraud_risk`: `isRetryable: false` evita reintentos que generan alertas de cumplimiento (Q34).
3. Un permission error: `false`; se necesita otra cuenta, no una llamada mejor (web 2.2).

**Qué NO hacer:**
- Leer `false` como "abandonar la tarea": significa "no esta llamada otra vez"; validation se corrige solo, business y permission continúan por escalado o por otro principal (web 2.2).
- Omitir la bandera de retryability: el agente acaba reintentando todo o nada (Guía PDF p. 82; Guía PDF p. 81).
- Dejar que el agente asuma "transitorio" cuando no hay metadatos: reintentó tres veces un bloqueo de fraude y cada reintento generó una alerta (Q34).

Para validation, la web precisa que `false` no significa rendirse: el agente corrige la entrada y envía una llamada nueva (web 2.2); la guía dice que es reintentable solo si el agente puede arreglar la entrada (Guía PDF p. 81). Ver la contradicción al final.

### Access failure vs valid empty result

**Concepto:** un access failure significa que la herramienta no pudo llegar a la fuente de datos (timeout, fallo de autenticación, servicio no disponible); no se ejecutó ninguna consulta y la ausencia de datos no es significativa (web 2.2; Guía PDF p. 81). Un valid empty result significa que la consulta se ejecutó con éxito y no encontró coincidencias: la ausencia de datos ES la respuesta, no requiere recuperación y no debe reintentarse (web 2.2; Guía PDF p. 81; Slides PDF p. 360). Esta es la distinción clave del dominio y el examen la evalúa directamente (web 2.2).

```json
// Valid empty result — NOT an error
{
  "isError": false,
  "content": [{ "type": "text", "text": "No customer found matching email 'john@example.com'. The query executed successfully but returned no matches." }],
  "structuredContent": { "resultCount": 0 }
}

// Access failure — IS an error
{
  "isError": true,
  "content": [{ "type": "text", "text": "Could not reach customer database" }],
  "structuredContent": {
    "errorCategory": "transient",
    "isRetryable": true,
    "description": "Connection to the customer database timed out after 5 seconds. The query did not execute."
  }
}
```

**Ejemplos de uso (3, cortos):**
1. HTTP 500 o timeout de conexión: access failure; se devuelve error con `service_unavailable` o `timeout` y `retryable: true` (Guía PDF p. 81).
2. HTTP 200 con un array vacío: resultado vacío válido; se devuelve éxito con datos vacíos (Guía PDF p. 81).
3. Una búsqueda sin resultados, sin eventos de calendario o un usuario sin notificaciones: resultado vacío válido (Slides PDF p. 359).

**Qué NO hacer:**
- Devolver un resultado vacío ante un access failure: es el anti-patrón más peligroso porque parece éxito; el agente informa "no existe" cuando la realidad es "no pudimos comprobarlo" (Guía PDF p. 81; Guía PDF p. 82).
- Reintentar un resultado vacío de una consulta exitosa: dará el mismo vacío (web 2.2).
- Fabricar contenido de relleno, o añadir un campo `confidence` o reintentos internos, para esconder la ambigüedad: no resuelven que el agente no distinga ambas condiciones (Q33).
- Tratar HTTP 404 siempre como error: depende del contexto; si el recurso debería existir es error, si se comprueba su existencia es vacío válido (Guía PDF p. 81).

**Posible confusión con otros conceptos:**
- Access failure vs permission error — un permission denied o authentication failure se clasifica como access failure en las slides (Slides PDF p. 358) y como categoría permission en la web (web 2.2).
- Valid empty result vs not_found — en la guía `not_found` es información, no error, y se maneja como resultado vacío válido (Guía PDF p. 80).

### Propagación de errores en sistemas multi-agente

**Concepto:** el principio es recuperar localmente y propagar selectivamente (web 2.2). El subagente reintenta los fallos transient antes de involucrar al coordinador; solo propaga lo que no se puede resolver localmente e incluye resultados parciales y lo intentado (web 2.2). Un ejemplo es "revisé 3 de 5 proveedores; los proveedores 4 y 5 expiraron" con los resultados parciales (web 2.2).

**Ejemplos de uso (3, cortos):**
1. Un subagente de búsqueda web que expira devuelve al coordinador el tipo de fallo, la consulta intentada, resultados parciales y alternativas posibles (Q8).
2. En un pipeline, la etapa 2 no procesa un error de la etapa 1 como datos: lo propaga con contexto ("Enrichment skipped because lookup failed: [original error]") y la etapa 3 no almacena datos parciales ni de error (Guía PDF p. 100).
3. Un timeout de API: reintentar una vez y luego anotar el hueco de cobertura (Guía PDF p. 100).

**Qué NO hacer:**
- Suprimir el error en silencio devolviendo un resultado vacío "exitoso": el coordinador no distingue "no encontré nada" de "no pude buscar" (web 2.2; Q8).
- Terminar todo el flujo por un solo fallo (web 2.2; Q8).
- Devolver solo un estado genérico tras agotar reintentos: oculta contexto valioso (Q8).

**Posible confusión con otros conceptos:**
- Esta tarea vs Domain 5 (Error Propagation) — la guía indica que esta sección se centra en diseñar las respuestas de error que devuelven las herramientas, no en cómo los agentes propagan errores por pipelines multi-agente (Guía PDF p. 79).

### Principios de diseño de errores y recuperación por categoría

**Concepto:** los principios de la guía son: incluir siempre una categoría (sobre la que ramifica el agente), incluir siempre la retryability, mantener descripciones específicas ("Database connection timed out after 30s" es accionable) y usar categorías de forma consistente en todas las herramientas para que el coordinador tenga una sola estrategia por categoría (Guía PDF p. 82). Las slides añaden: reintentar fallos transient con exponential backoff, limitar los reintentos, registrar fallos y devolver errores estructurados (Slides PDF p. 333).

**Ejemplos de uso (3, cortos):**
1. `timeout`: reintentar con exponential backoff; `rate_limited`: esperar y reintentar tras un retraso (Guía PDF p. 80).
2. `service_unavailable`: probar una fuente alternativa o anotar el hueco (Guía PDF p. 81).
3. Un permission failure devuelve un error seguro como "Access denied: administrator permission required", sin exponer detalles internos (Slides PDF p. 354; Slides PDF p. 353).

**Qué NO hacer:**
- Usar reintentos infinitos, caer al primer fallo o sobrecargar servicios externos (Slides PDF p. 334).
- Devolver un stack trace completo con el estado del sistema "para dar máxima información": consume contexto sin mejorar la decisión (Q32).
- Delegar la lógica de recuperación a un código numérico mapeado en el system prompt, o depender de códigos HTTP: es menos mantenible y menos expresivo que campos estructurados (Q32).
- Usar categorías inconsistentes entre herramientas (Guía PDF p. 82).
- Exponer detalles sensibles internos en un permission error (Slides PDF p. 353; Slides PDF p. 354).

**Posible confusión con otros conceptos:**
- Autenticación vs autorización — la identidad puede estar autenticada y aun así se le deniega el acceso (Slides PDF p. 355).
- Validation vs business — validation: la entrada viola reglas de formato; business: ocurre después de que la validación tiene éxito, "una solicitud válida no siempre es una operación permitida" (Slides PDF p. 341; Slides PDF p. 348).

### Trampas del examen

- Mensaje genérico sin metadatos (Q32): `{"status": "error", "message": "Operation failed"}` lleva al agente a disculparse y terminar siempre. La opción correcta (B) añade `errorCategory`, `isRetryable` y una explicación específica. Fallan los códigos HTTP por tipo (A, menos expresivos), el log verboso con stack trace (C, consume contexto) y el código numérico mapeado en el system prompt (D, lógica fuera de una estructura de error) (Q32; web 2.2; Guía PDF p. 82).
- Confundir resultado vacío y fallo de acceso (Q33): `{"results": [], "status": "success"}` cuando la API estaba caída. La respuesta correcta (B) distingue ambos y usa `isError` para el fallo de acceso. Fallan rellenar con contenido (A, enmascara el fallo), añadir `confidence` (C, ambiguo) y reintento automático en la herramienta (D, no resuelve que el agente no distinga) (Q33; Guía PDF p. 81).
- Reintentar un resultado vacío de una consulta exitosa: producirá el mismo vacío; el agente debe aceptarlo (web 2.2). En el escenario de práctica, la causa raíz de reintentar 3 veces y escalar cuando la cuenta no existe es que la herramienta no distingue fallos de acceso de vacíos válidos (opción B), no el límite de reintentos, el umbral de escalado ni el system prompt (web 2.2).
- Bloqueo de fraude tratado como transient (Q34): sin `isRetryable: false` el agente reintenta tres veces y genera alertas de cumplimiento. Correcta (B): `isRetryable: false` más una explicación para el cliente. Fallan `retry_after` (A, implica que es temporal), ocultar `isError` con `blocked: true` (C, oculta la naturaleza de error) y el risk score (D, datos que el agente puede no estar autorizado a usar) (Q34; web 2.2).
- Tratar business errors como reintentables: la misma violación de política se repite; hay que ir por escalado (web 2.2; Q34).
- Marcar validation como `isRetryable: true` porque el agente puede recuperarse: `isRetryable` pregunta si reenviar esta misma llamada funcionaría; no, y la categoría comunica la corrección (web 2.2).
- Leer `isRetryable: false` como "abandonar la tarea" (web 2.2).
- Propagación de un timeout de subagente (Q8): correcta (A) devolver contexto de error estructurado con tipo de fallo, consulta intentada, resultados parciales y alternativas. Fallan reintentos internos que devuelven un estado genérico (B, oculta contexto), un resultado vacío marcado como exitoso (C, suprime el error) y propagar la excepción para terminar todo el flujo (D) (Q8; web 2.2).
- Devolver el error sin `is_error: true`: Claude lo interpreta como datos válidos (Guía PDF p. 92; Guía PDF p. 82).
- Devolver vacío ante un fallo de acceso en un pipeline: la cascada acaba almacenando registros con campos nulos y reportando "sin datos" cuando la consulta nunca tuvo éxito (Guía PDF p. 100; Guía PDF p. 81).
- Pistas del examen (guía): "el coordinador no puede determinar qué falló porque la herramienta solo devuelve un error genérico" → errores estructurados con categoría, descripción y retryability; "un agente informa que no hay datos cuando la fuente era inalcanzable" → distinguir fallos de acceso de vacíos válidos (Guía PDF p. 82).
- Esperar que el examen se base en la especificación MCP: las cuatro categorías y `isRetryable` no están definidas por MCP, pero hay que conocerlas por nombre (web 2.2).

- **Contradicción entre fuentes:** (1) Nomenclatura: la web y el banco usan `isError`, `errorCategory` e `isRetryable` con las categorías transient/validation/business/permission (web 2.2; Q32; Q34), mientras que la guía usa `is_error`, `category` y `retryable` con valores como `timeout` o `validation_error` (Guía PDF p. 80; Guía PDF p. 104); prevalecen la guía y el banco, y se debe conocer ambas notaciones. (2) Validation: la web da `isRetryable: false` y dice que la guía no asigna valor, mientras que la guía PDF indica "No" con recuperación "corregir los parámetros y reintentar" y matiza que depende de si el agente puede arreglar la entrada (web 2.2; Guía PDF p. 81); prevalece la guía. (3) Timeout: la guía indica backoff exponencial en una tabla y "retry once, then annotate gap" en otra (Guía PDF p. 80; Guía PDF p. 100); el ejercicio de la web habla de hasta 3 reintentos con backoff (web 2.2).

## Tarea 2.3 — Distribute tools appropriately across agents and configure tool_choice (Distribuir herramientas adecuadamente entre agentes y configurar tool_choice)

> Prioridad de estudio: tool_use + tool_choice (regresión: 100% -> 0%)

### Tool distribution y principio de least privilege

**Concepto:** En un sistema multi-agente no todos los agentes deben tener todas las herramientas; cada agente recibe solo las que su rol necesita (Guía PDF p. 83). Dar a todos todas las herramientas crea complejidad de decisión innecesaria, aumenta el riesgo de acciones inapropiadas y dificulta la auditoría (Guía PDF p. 83). Es el principio de least privilege aplicado al acceso a herramientas (Guía PDF p. 84).

**Ejemplos de uso (3, cortos):**
1. Search agent: `allowedTools=["WebSearch", "WebFetch"]`; no puede usar Write, Edit ni Bash aunque el coordinator los tenga (Guía PDF p. 84; Guía PDF p. 85).
2. Document analyst: `allowedTools=["Read", "Grep", "Glob"]`; no accede a la web ni modifica archivos (Guía PDF p. 85).
3. Subagent de investigación de pedidos: `allowedTools` = `["lookup_customer", "lookup_orders"]`; puede investigar pero no ejecutar `process_refund` (Guía PDF p. 116).

```python
agent = Agent(
    name="search_agent",
    description="Searches the web for current information",
    allowedTools=["WebSearch", "WebFetch"],
    prompt="Search the web for the given query and return relevant findings."
)
```
(Guía PDF p. 84)

**Qué NO hacer:**
- Dar a cada subagent todas las herramientas "por flexibilidad": aumenta la complejidad de decisión y el riesgo (Guía PDF p. 86).
- Dar al synthesis agent las 18 herramientas del sistema (web search, lectura de archivos, bases de datos, email, calendario…): al tener herramientas fuera de su especialización, es más probable que las use mal, p. ej. iniciar nuevas búsquedas web en lugar de sintetizar los hallazgos recibidos (Q35; web 2.3).
- Confiar en instrucciones del prompt para evitar el mal uso de herramientas en lugar de restringirlas con `allowedTools` (Guía PDF p. 86).
- Dar la herramienta Agent a los subagents: los subagents no pueden crear sus propios subagents (Guía PDF p. 86).

**Posible confusión con otros conceptos:**
- `allowedTools` vs `permissions.deny` — `allowedTools` restringe qué herramientas puede usar; deny bloquea acciones específicas (Guía PDF p. 115).
- Herencia de permisos vs herencia de restricciones — los modos permisivos como `bypassPermissions` los heredan los subagents y no se pueden relajar por subagent; los subagents heredan permisos, no restricciones, salvo que se defina `allowedTools` (Guía PDF p. 85; Guía PDF p. 86).

### Fiabilidad y seguridad: por qué importa el número y la relevancia

**Concepto:** El número de herramientas afecta directamente a la fiabilidad de la selección: cada herramienta adicional complica la decisión y aumenta la tasa de errores (web 2.3). Con 15 herramientas Claude debe evaluar las 15 descripciones en cada turno; con 3, el espacio de decisión es mucho menor (Guía PDF p. 84). Un conjunto demasiado permisivo es riesgo de fiabilidad y de seguridad (Guía PDF p. 84).

**Ejemplos de uso (3, cortos):**
1. Comparación de la guía de examen: 18 herramientas en un agente frente a 4-5 por agente; es una ilustración, no un límite estricto (web 2.3).
2. Un subagent con acceso de escritura a la base de datos cuyo trabajo es solo leer puede hacer cambios destructivos; limitarlo a operaciones de solo lectura evita esa clase de error (Guía PDF p. 84).
3. El quoting agent con una herramienta de búsqueda fuera de su rol puede volver a buscar pedidos en lugar de presupuestar el trabajo recibido (web 2.3).

**Qué NO hacer:**
- Esperar selección fiable con 18 herramientas en un solo agente (web 2.3).
- Pensar que mover herramientas a un segundo servidor MCP lo arregla: el cliente entrega al modelo todas las herramientas de todos los servidores como una lista plana, así que 22 herramientas en dos servidores siguen siendo 22 (web 2.3).

### Diseño de conjuntos de herramientas por rol

**Concepto:** Cada rol recibe un conjunto acotado de herramientas y se excluyen las ajenas a su función (Guía PDF p. 84). El coordinator no mantiene herramientas de dominio propias, salvo la herramienta para crear subagents (web 2.3; Guía PDF p. 85).

**Ejemplos de uso (3, cortos):**
1. Test runner: incluye Bash y Read; excluye Write, Edit y WebSearch (Guía PDF p. 84).
2. Customer support agent: customer lookup, order lookup y refund tool; excluye database admin y herramientas de file system (Guía PDF p. 84).
3. Layout de investigación de la web: Web Search (`search_web`, `fetch_page`, `extract_links`, `save_snippet`); Document Analysis (`extract_metadata`, `extract_data_points`, `summarize_content`, `verify_claim`); Synthesis (`compile_report`, `verify_fact` (scoped), `format_citation`, `assess_coverage`); Coordinator (Agent, `review_output`, `request_revision`) (web 2.3).

**Qué NO hacer:**
- Dar al synthesis agent herramientas de web search, o al web search agent herramientas de análisis de documentos (web 2.3).
- Aplicar restricción estricta en todos los casos: el coordinator puede necesitar acceso amplio si interactúa con herramientas entre delegaciones, y las sesiones interactivas de Claude Code pueden necesitarlo porque el desarrollador decide; las invocaciones CI/CD deben restringirse al propósito del paso (Guía PDF p. 85; Guía PDF p. 86).

### Consolidar herramientas casi duplicadas y elegir el arreglo correcto

**Concepto:** Si las herramientas son variaciones de un mismo trabajo con la misma forma (datos entran, operación, datos salen), se combinan en una sola herramienta parametrizada cuyo parámetro nombra la operación (web 2.3). Ejemplo: un servidor con 22 herramientas (3 de consulta y 19 de transformación) pasa a 4 con `transform_data`, sin perder capacidad (web 2.3).

```json
{
  "name": "transform_data",
  "description": "Apply a transformation to a dataset. Use transform_type to select the operation.",
  "input_schema": {
    "type": "object",
    "properties": {
      "dataset": { "type": "string" },
      "transform_type": {
        "type": "string",
        "enum": ["pivot", "percentile", "normalise_currency", "..."]
      },
      "options": { "type": "object" }
    },
    "required": ["dataset", "transform_type"]
  }
}
```
(web 2.3)

**Ejemplos de uso (3, cortos):**
1. Pocas herramientas pero dos se parecen: mejorar las descripciones (Task Statement 2.1) (web 2.3).
2. Trabajos distintos (query, transform, export): dividir por rol, con un conjunto pequeño cada uno (web 2.3).
3. Variaciones de un mismo trabajo con la misma forma (resize, bleed, convertir a CMYK): una herramienta con parámetro de operación (web 2.3).

**Qué NO hacer:**
- Dividir por rol 19 transformaciones: el agente de transformación seguiría con 19 herramientas y el mismo problema (web 2.3).
- Reescribir las 22 descripciones esperando arreglar la selección: a ese tamaño ninguna calidad de descripción lo arregla (web 2.3).

**Posible confusión con otros conceptos:**
- Consolidar vs constrain — consolidar reduce entre cuántas herramientas elige el agente (`transform_data`); constrain reduce lo que alcanza cada herramienta (`load_document`); no se contradicen y ambos pueden ser correctos en el mismo sistema (web 2.3).
- Problema de descripciones vs problema de cantidad — con cinco herramientas, elegir `get_customer` en vez de `lookup_order` es un problema de descripciones; con 22 no (web 2.3). El patrón del examen "wrong tool selected" apunta a mejorar descripciones con especificidad, boundary statements y desambiguación, nunca few-shot, temperature ni solo renombrar (Guía PDF p. 113).

### Herramientas restringidas en lugar de genéricas

**Concepto:** Se sustituye una herramienta genérica como `fetch_url` (obtiene cualquier cosa de cualquier sitio) por una restringida como `load_document`, que valida URLs de documentos y solo acepta esas (web 2.3). Evita el mal uso, aclara el propósito y reduce efectos secundarios no deseados (web 2.3).

**Ejemplos de uso (3, cortos):**
1. El artwork agent solo necesita archivos de clientes, así que `load_document` basta (web 2.3).
2. Subagent con `load_document` en lugar de `fetch_url`: no puede obtener URLs arbitrarias (web 2.3).
3. Subagent de solo lectura: se limita a operaciones de lectura para prevenir cambios destructivos (Guía PDF p. 84).

**Qué NO hacer:**
- Dar a un subagent un `fetch_url` genérico para cargar documentos (web 2.3).

### Scoped cross-role tools

**Concepto:** Herramienta restringida que da a un agente acceso directo a una capacidad de otro rol para solicitudes simples y frecuentes; los casos complejos (varias fuentes, referencias cruzadas, juicio real) siguen yendo por el coordinator (web 2.3). Evita 2-3 round trips por solicitud y una latencia que puede aumentar un 40% o más (web 2.3; Q9).

**Ejemplos de uso (3, cortos):**
1. Synthesis agent con `verify_fact` scoped: 85% de las verificaciones son simples; el 15% complejo sigue al web search agent vía coordinator (Q9).
2. `verify_fact` recibe una afirmación y devuelve un veredicto; no tiene campo de query ni de URL que permita búsquedas propias (web 2.3).
3. El quoting agent usa `check_stock` para consultas simples y deriva sustituciones o plazos de proveedores al coordinator (web 2.3).

```json
{
  "name": "check_stock",
  "description": "Check how many sheets of one paper stock are in the warehouse. Takes a single stock code. For substitutions, supplier lead times or anything that needs judgement, ask the coordinator.",
  "strict": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "stock_code": { "type": "string", "pattern": "^PS-[0-9]{4}$" }
    },
    "required": ["stock_code"],
    "additionalProperties": false
  }
}
```
(web 2.3)

El alcance lo define el input schema: si omite un campo, el agente no puede hacer una solicitud con ese campo (web 2.3). Con `strict: true` la API restringe las entradas al schema (web 2.3). Strict tool use admite enum, pattern y un array con minItems de 0 o 1; la API rechaza maxItems, maxLength, minimum y maximum con error 400 cuando recibe el schema sin cambios, por lo que "un código por llamada" es un campo string, no un array con maxItems: 1; un límite que el schema no puede expresar va en el código que ejecuta la herramienta (web 2.3).

**Qué NO hacer:**
- Enrutar todas las verificaciones simples por el coordinator (Q9; web 2.3).
- Acumular las verificaciones y devolverlas en lote al coordinator al final: crea dependencias bloqueantes (Q9).
- Dar al synthesis agent todas las herramientas de web search: sobre-provisiona (Q9).

**Posible confusión con otros conceptos:**
- Scoped cross-role tool vs acceso completo — verify_fact toma una afirmación y devuelve un veredicto; las herramientas de web search permitirían búsquedas propias (web 2.3; Q9).

### tool_choice: auto, any y forced selection (tool)

**Concepto:** El parámetro `tool_choice` controla si Claude llama a una herramienta y a cuál; pasa de "Claude podría llamar una herramienta" a "Claude llama definitivamente a esta" (Guía PDF p. 86). Modos: `auto` (por defecto; el modelo decide si llama a una herramienta o devuelve texto), `any` (debe llamar a una herramienta pero elige cuál) y forced selection (debe llamar a una herramienta concreta) (web 2.3; Guía PDF p. 86). La guía añade un cuarto modo, `none`: Claude no puede llamar a ninguna herramienta (Guía PDF p. 86).

```json
{ "tool_choice": { "type": "auto" } }
{ "tool_choice": { "type": "any" } }
{ "tool_choice": { "type": "tool", "name": "extract_metadata" } }
```
(web 2.3)

**Ejemplos de uso (3, cortos):**
1. `auto`: agente conversacional que a veces busca pedidos y a veces responde preguntas generales (Guía PDF p. 87).
2. `any`: varios schemas de extracción (invoices, receipts, contracts) con tipo de documento desconocido; Claude elige el schema adecuado y siempre devuelve salida estructurada (Guía PDF p. 87; web 2.3).
3. `{"type": "tool", "name": "extract_metadata"}`: paso obligatorio inicial; tras la llamada forzada, los turnos posteriores pueden usar `auto` (web 2.3; Guía PDF p. 87).

`none` sirve para comportamiento solo texto en un turno concreto, como generar un resumen con datos ya en contexto (Guía PDF p. 87).

**Qué NO hacer:**
- Usar `auto` cuando se necesita salida estructurada garantizada: Claude puede responder con texto y romper el parser descendente (Guía PDF p. 87; Guía PDF p. 88; web 2.3).
- Usar `any` cuando debe ejecutarse una herramienta concreta: garantiza una llamada, no cuál (Q36).
- Quitar todas las demás herramientas para que solo quede una: funciona indirectamente pero elimina herramientas legítimas que el agente necesita para otras tareas (Q36).
- Dejar `tool_choice` en `none` y preguntarse por qué no se llaman herramientas (Guía PDF p. 88).

**Posible confusión con otros conceptos:**
- `auto` vs `tool` — auto permite respuesta de texto; tool garantiza la llamada (Guía PDF p. 115).
- `any` vs `tool` — any deja a Claude elegir la herramienta; tool fuerza una específica (Guía PDF p. 115; Guía PDF p. 88).
- Forced selection fija el orden del workflow: si la extracción de metadata debe ocurrir antes de las herramientas de enrichment, forzar `extract_metadata` garantiza ese orden (web 2.3; Guía PDF p. 87).

### tool_choice + strict tool use: sintaxis vs semántica

**Concepto:** `tool_choice` (`any` o `tool`) garantiza que se llama a la herramienta de extracción; combinado con `strict: true` garantiza además que las entradas coinciden exactamente con el schema (Guía PDF p. 87). Esto elimina errores de sintaxis (JSON mal formado, campos ausentes, tipos erróneos) pero NO los semánticos (valores erróneos, datos inconsistentes, valores en el campo equivocado); estos requieren una capa de validación (Pydantic, comprobaciones propias) (Guía PDF p. 87; Guía PDF p. 88).

**Ejemplos de uso (3, cortos):**
1. Pipeline de facturas: con `auto`, Claude a veces responde "I found the invoice number is INV-1234" y rompe el parser; con `{type: "tool", name: "extract_invoice"}` siempre llama a la herramienta (Guía PDF p. 87).
2. Error de sintaxis atrapado con strict: falta el campo requerido `invoice_number` o `total_amount` es string en vez de número (Guía PDF p. 88).
3. Error semántico no atrapado: `total_amount` es 150.00 pero las líneas suman 180.00; o el estado es "completed" con `completion_date` null (Guía PDF p. 88).

**Qué NO hacer:**
- Asumir que strict tool use garantiza valores correctos: solo garantiza estructura (Guía PDF p. 88).

**Posible confusión con otros conceptos:**
- Strict tool use vs semantic validation — strict garantiza estructura; la validación comprueba el significado (Guía PDF p. 115; Guía PDF p. 88).

### Trampas del examen

- Enrutar por el coordinator todas las verificaciones simples cuando el 85% son consultas simples: añade 2-3 hops por solicitud y hasta 40% de latencia; la respuesta correcta es un `verify_fact` scoped en el synthesis agent (web 2.3; Q9).
- Q9, opción B (acumular verificaciones y devolverlas en lote al final): crea dependencias bloqueantes. Opción C (dar todas las herramientas de web search): sobre-provisiona al synthesis agent. Opción D (caché especulativa por el web search agent): depende de anticipar lo que se verificará (Q9).
- Q35: dar 18 herramientas a un synthesis agent "por flexibilidad". El problema es el mal uso de herramientas fuera de su especialización (p. ej. nuevas búsquedas web en vez de sintetizar). Opción A (se niega a llamar herramientas) exagera el efecto; C (exceder la ventana de contexto con errores de API) no es un modo de fallo realista con 18 herramientas; D (más lento por leer descripciones) malinterpreta cómo afectan las descripciones a la latencia (Q35).
- Q36: para garantizar que `generate_summary` se llame siempre, la respuesta es `tool_choice: {"type": "tool", "name": "generate_summary"}`. `auto` permite responder sin herramienta (opción A); `any` garantiza una llamada pero no cuál (opción B); quitar el resto de herramientas lo logra de forma indirecta pero elimina herramientas necesarias (opción D) (Q36).
- Usar `auto` cuando se requiere salida estructurada: el modelo puede devolver texto conversacional en lugar de llamar a la herramienta (web 2.3; Guía PDF p. 88).
- Confundir `any` (el modelo elige herramienta) con `tool` (herramienta concreta nombrada) (Guía PDF p. 88; Q36).
- Fijar `tool_choice` en `none` y no entender por qué no se llaman herramientas (Guía PDF p. 88).
- Pensar que strict garantiza valores correctos; la pregunta sobre valores correctos requiere una capa de validación aparte, y esta distinción se evalúa mucho en los Dominios 2 y 4 (Guía PDF p. 87; Guía PDF p. 88).
- Dar un `fetch_url` genérico a un subagent: habilita el mal uso; la alternativa es `load_document`, que valida solo URLs de documentos (web 2.3).
- Pensar que consolidar y restringir son opuestos: ambos pueden ser correctos en el mismo sistema, y los candidatos suelen fallar la primera fila de la tabla de arreglos (descripciones cuando hay pocas herramientas parecidas) (web 2.3).
- Ante un subagent que actuó fuera de su alcance, la respuesta es restringir sus herramientas con `allowedTools`; si el coordinator usa modo permisivo, los modos permisivos se heredan y `allowedTools` es la única forma de acotar a los subagents (Guía PDF p. 85).
- Asumir que los subagents heredan las restricciones del coordinator: heredan permisos, no restricciones (Guía PDF p. 86).
- Usar few-shot examples para arreglar un tool misrouting: los ejemplos arreglan el formato de salida; las descripciones arreglan la selección de herramienta (Guía PDF p. 113; Guía PDF p. 115).
- **Contradicción entre fuentes:** el worked example de la guía deja al synthesis agent sin herramientas (`allowedTools = []`) (Guía PDF p. 85), mientras que el banco y la web le dan un `verify_fact` scoped (Q9; web 2.3). Prevalecen la guía y el banco como fuentes de examen; la pregunta Q9 es la que prueba el patrón, y se entiende `verify_fact` como excepción scoped para el caso simple.
- **Contradicción entre fuentes:** la web indica que la guía de examen v1.0 nombra tres modos (auto, any, forced) y que, según documentación actual (6 octubre 2026), algunos modelos rechazan `{"type": "any"}` y `{"type": "tool"}` con error 400 y recomienda `auto` con strict tool use (web 2.3). La guía y el banco presentan `any` y `tool` como mecanismos que garantizan la llamada (Guía PDF p. 87; Q36). Prevalecen la guía y el banco: en el examen se responde con `any` y forced selection (web 2.3). Además, la guía lista cuatro modos (incluye `none`) frente a los tres de la web (Guía PDF p. 86; web 2.3).
- **Contradicción entre fuentes:** cifras de ilustración distintas: la guía contrasta 15 herramientas con 3 (Guía PDF p. 84), el banco y la web hablan de 18 frente a 4-5 (Q35; web 2.3); la web añade, como estado actual, que la degradación aparece al superar 30 a 50 herramientas, pero indica usar el marco 18 frente a 4-5 en el examen (web 2.3).

## Tarea 2.4 — Integrate MCP servers into Claude Code and agent workflows (Integrar servidores MCP en Claude Code y en flujos de agentes)

> Prioridad de estudio: Scope de servidores MCP (regresión: 100% -> 0%); Integración MCP (env vars) (débil: 25%)

### Arquitectura MCP: tools, resources y prompts

**Concepto:** MCP (Model Context Protocol) es un estándar abierto que conecta Claude con herramientas externas, fuentes de datos, bases de datos y APIs (Guía PDF p. 89). Un servidor MCP es un proceso separado que expone tres categorías: tools (funciones invocables), resources (catálogos de contenido de solo lectura) y prompts (plantillas predefinidas) (Guía PDF p. 89).

**Ejemplos de uso (3, cortos):**
1. Tool: consultar una base de datos o crear un ticket; Claude la llama como cualquier otra herramienta (Guía PDF p. 89).
2. Resource: descripción del esquema de la base de datos o jerarquía de documentación, que Claude lee para decidir qué tool llamar (Guía PDF p. 89).
3. Prompt: plantillas como deploy checklist o incident response, que el desarrollador invoca como slash commands (Guía PDF p. 89).

**Qué NO hacer:**
- No confundir resources (catálogos de solo lectura) con tools (funciones invocables) (Guía PDF p. 91; Guía PDF p. 136).
- No esperar que los prompts MCP se carguen solos en el contexto: no se añaden al tool registry, no se cargan automáticamente y no se exponen como resources @-mencionables (Guía PDF p. 91; Guía PDF p. 135).

**Posible confusión con otros conceptos:**
- Tools — realizan acciones (consultar una base de datos, crear un ticket); son operacionales (Guía PDF p. 89; Guía PDF p. 135).
- Resources — informan qué datos hay; son informacionales, no operacionales (Guía PDF p. 135).
- Prompts — atajos de flujo de trabajo; se invocan explícitamente con `/mcp_<servername>_<promptname>` y los argumentos van después del nombre del comando (Guía PDF p. 89; Guía PDF p. 135).

### Scope de servidores MCP: .mcp.json vs ~/.claude.json

**Concepto:** La guía describe dos niveles de configuración: proyecto (compartido con el equipo) y usuario (personal) (Guía PDF p. 89; web 2.4). `.mcp.json` está en la raíz del proyecto y se versiona, así que todo miembro del equipo recibe los mismos servidores; `~/.claude.json` está en el directorio home, es personal y no se comparte (Guía PDF p. 134; web 2.4).

**Ejemplos de uso (3, cortos):**
1. Servidor compartido de venue lookup, base de datos o API interna para todo el equipo: `.mcp.json` (Guía PDF p. 134; Guía PDF p. 90).
2. Servidor experimental o personal que solo tú pruebas, p. ej. un servidor de búsqueda de código en prueba: `~/.claude.json` (Guía PDF p. 134; web 2.4).
3. Escenario típico del examen: servidor compartido de venue lookup para el equipo Y servidor personal experimental de playlist; compartido → `.mcp.json`, personal → `~/.claude.json` (Guía PDF p. 135).

| Configuración | Ubicación | ¿Compartida? | Uso |
|---|---|---|---|
| `.mcp.json` | raíz del proyecto | Sí (versionada) | Herramientas del equipo (bases de datos, APIs, servicios) |
| `~/.claude.json` | directorio home | No (personal) | Herramientas experimentales o personales |

(Guía PDF p. 90)

**Qué NO hacer:**
- No poner servidores personales en `.mcp.json`: se versionan y se comparten con el equipo (Guía PDF p. 136; Guía PDF p. 91).
- No poner la configuración de servidores de todo el equipo en `~/.claude.json`: es personal y no se versiona ni se comparte (web 2.4; Q37).
- Vigila los distractores que invierten el orden (compartido/personal) (Guía PDF p. 135).

**Posible confusión con otros conceptos:**
- Scope de proyecto — `.mcp.json` en la raíz, versionado, para el equipo (Guía PDF p. 134).
- Scope de usuario — `~/.claude.json`, personal, no versionado (Guía PDF p. 134).
- Todas las tools de todos los servidores configurados (proyecto y usuario) se descubren al conectar y están disponibles a la vez, sin paso manual de activación (web 2.4).

### Formas de entrada de un servidor en .mcp.json

**Concepto:** Una entrada puede ser remota o local. Un servidor remoto declara `"type": "http"` y una `url`; uno local declara `command` y `args` y se comunica por stdio (entrada y salida estándar) (web 2.4).

**Ejemplos de uso (3, cortos):**
1. Servidor remoto de GitHub: `"type": "http"` con `"url": "https://api.githubcopilot.com/mcp/"` (web 2.4).
2. Servidor local de filesystem: `"command": "npx"` con `args` `["-y", "@modelcontextprotocol/server-filesystem", "${WORKSPACE_ROOT:-.}"]` (web 2.4).
3. Servidor local propio: `"command": "node"` con `"args": ["./mcp-servers/venue-lookup/index.js"]` (Guía PDF p. 89).

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${WORKSPACE_ROOT:-.}"]
    }
  }
}
```

(web 2.4)

**Qué NO hacer:**
- No declarar una entrada con `url` pero sin `type`: es un error de configuración; Claude Code la lee como servidor stdio, la omite y pide añadir el type (web 2.4).

### Expansión de variables de entorno para credenciales

**Concepto:** `.mcp.json` admite la sintaxis `${VARIABLE_NAME}` para referenciar variables de entorno, de modo que la configuración del servidor se comparte pero los secretos nunca entran en el control de versiones (Guía PDF p. 90; web 2.4). El archivo contiene nombres de variables, no valores; cada desarrollador define sus tokens localmente (web 2.4).

**Ejemplos de uso (3, cortos):**
1. `"API_KEY": "${VENUE_API_KEY}"`: se expande desde el entorno de cada desarrollador en tiempo de ejecución y la clave real nunca aparece en el control de versiones (Guía PDF p. 134).
2. `"GITHUB_TOKEN": "${GITHUB_TOKEN}"` y `"DATABASE_URL": "${DATABASE_URL}"` dentro de `env` (web 2.4).
3. `${VAR:-default}` se expande a VAR si está definida y a `default` si no; útil para rutas específicas de la máquina, como `${WORKSPACE_ROOT:-.}` (web 2.4).

```json
{
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}",
    "DATABASE_URL": "${DATABASE_URL}"
  }
}
```

(web 2.4)

Ventajas: el archivo se puede commitear, cada desarrollador se autentica con sus propias credenciales, la rotación de tokens no exige cambiar la configuración y no se filtran secretos por el historial del repositorio (web 2.4).

**Qué NO hacer:**
- No escribir claves de API en `.mcp.json` en lugar de usar expansión: quedarían en el control de versiones, expuestas a todos los que tengan acceso al repositorio (Guía PDF p. 90; Guía PDF p. 91).
- No pegar un token en `.mcp.json` porque el repositorio sea privado: un repositorio privado no es un almacén de secretos y cada clon y fork lleva el token en su historial (web 2.4).
- No depender de que un token ausente cause un fallo visible: una variable sin definir y sin default no detiene la carga del resto de la configuración; Claude Code avisa y continúa (web 2.4).

**Posible confusión con otros conceptos:**
- `${VAR}` — sin valor por defecto; `${VAR:-default}` — con valor por defecto si VAR no está definida (web 2.4).
- Credenciales en la config de usuario: también como referencias a variables de entorno, nunca inline (Slides PDF p. 410; Slides PDF p. 415).

**Diagnóstico de acceso a un servidor MCP que falta:** las slides proponen una lista en orden: config file (servidor definido, con nombre correcto y transport type), server running (proceso activo o URL alcanzable), approval (servidor en la lista de confianza de Claude) y environment variables (credenciales presentes en la sesión de shell actual); la mayoría de los problemas se deben a uno de estos cuatro (Slides PDF p. 422). Para variables, se ejecuta `echo $NOTION_API_KEY` en la misma shell donde corre Claude Code: si devuelve valor, la credencial está presente; si la autenticación falla en silencio, se define la variable y se reinicia Claude Code (Slides PDF p. 421).

### MCP resources como catálogo de contenido

**Concepto:** Un MCP resource expone un catálogo de contenido al agente desde el principio, de modo que no necesita llamadas exploratorias para descubrir qué datos existen (web 2.4). Sin resources, Claude no tiene visibilidad de lo que contiene cada servidor y hace llamadas exploratorias en exceso y gasta contexto (Guía PDF p. 135).

**Ejemplos de uso (3, cortos):**
1. Resumen de incidencias: lista de issues de Jira con títulos y estados (web 2.4).
2. Jerarquía de documentación: tabla de contenidos de los docs internos (web 2.4).
3. Esquema de base de datos: nombres de tablas, tipos de columna y relaciones; evita llamar `list_tables` y luego `describe_table` por cada tabla (web 2.4).

Comparación con varios servidores: sin resources, Claude consulta el servidor A (sin resultados), el B (sin resultados) y el C (lo encuentra): 3 llamadas, 2 desperdiciadas; con resources lee los catálogos, sabe que el servidor C tiene los datos de facturación y lo consulta directamente: 1 llamada, 0 desperdiciadas (Guía PDF p. 91).

**Qué NO hacer:**
- No tratar los resources como tools: son catálogos de solo lectura, informacionales; las tools actúan (Guía PDF p. 136; web 2.4).
- No resolver el problema de descubrimiento con un meta-tool `list_tools`, reduciendo tools, o con una capa de caché (Q38).

**Posible confusión con otros conceptos:**
- Resources — muestran qué datos hay; tools — permiten actuar sobre ellos (web 2.4).
- Prompts — se acceden como slash commands, no como resources (Guía PDF p. 91).

### Build vs use: servidores de la comunidad o personalizados

**Concepto:** Para integrar un sistema externo se puede construir un servidor MCP propio o usar uno de la comunidad. Para integraciones estándar se evalúan primero los servidores de la comunidad (web 2.4).

**Ejemplos de uso (3, cortos):**
1. Jira, GitHub, Slack, Linear y Notion tienen servidores MCP de la comunidad mantenidos; cubren casos estándar, la comunidad los prueba y reciben actualizaciones (web 2.4).
2. Construir uno propio cuando hay flujos de trabajo específicos del equipo que los servidores de la comunidad no pueden manejar (web 2.4).
3. Construir uno propio cuando se necesita lógica de negocio personalizada en las tools, o integrar un sistema interno propietario sin servidor de la comunidad (web 2.4).

**Qué NO hacer:**
- No construir un servidor propio para una integración estándar como Jira (web 2.4).
- No saltarse la evaluación de servidores existentes: "evaluar primero los servidores de la comunidad" es siempre correcto en integraciones estándar; "construir a medida" solo si el escenario describe requisitos del equipo que la comunidad no cubre (web 2.4).

### Descripciones detalladas de tools MCP

**Concepto:** Las tools integradas, como Grep, tienen descripciones ricas; si una tool MCP tiene una descripción escasa, el agente puede preferir la integrada aunque la MCP sea más capaz (web 2.4). La solución es una descripción que explique capacidades y salidas en detalle (web 2.4).

**Ejemplos de uso (3, cortos):**
1. Cambiar `search_codebase: "Searches code"` por una descripción de búsqueda semántica con indexación AST-aware (web 2.4).
2. Indicar qué devuelve: funciones, clases y métodos con contexto completo (ruta de archivo, números de línea y código circundante) (web 2.4).
3. Indicar cuándo usarla frente a Grep: para buscar código por lo que hace y no por lo que contiene (web 2.4).

**Qué NO hacer:**
- No añadir una regla en el system prompt ni quitar tools integradas para forzar el uso de la MCP: el modelo no siempre sigue las reglas del prompt y quitar tools integradas rompe trabajo que aún hacen; el agente elige leyendo las descripciones (web 2.4).

### Resultados de tools y errores en integraciones MCP

**Concepto:** El diseño de los resultados que devuelve una tool es una cuestión de fiabilidad. En MCP un resultado se marca como error con el flag `is_error`; con `true`, Claude entiende que la llamada falló y puede reintentar, probar otro enfoque o informar (Guía PDF p. 92).

**Ejemplos de uso (3, cortos):**
1. Si una consulta expira y la tool devuelve `{"message": "connection timed out"}` sin `is_error: true`, Claude puede intentar extraer datos del mensaje de error y producir una salida sin sentido (Guía PDF p. 92).
2. Devolver 5 campos relevantes del pedido, no 40 columnas crudas; usar JSON con campos con nombre; incluir `"status": "complete"` frente a `"status": "partial, 3 of 5 records returned"` (Guía PDF p. 92).
3. Categorías de error: timeout (reintentable, retry with backoff), rate_limited (reintentable, esperar y reintentar), permission_denied (no, escalar), not_found (no, tratar como vacío válido si procede), validation_error (a veces, corregir entrada y reintentar), service_unavailable (sí, fuente alternativa o anotar la laguna) (Guía PDF p. 105).

Las slides añaden principios de integración: tolerar caídas temporales (Slides PDF p. 331); validar antes de ejecutar, pues peticiones inválidas pueden causar fallos downstream, comportamiento impredecible, llamadas desperdiciadas o riesgos de seguridad (Slides PDF p. 339); ante reglas de negocio, devolver respuestas estructuradas que expliquen qué regla se violó, por qué falló y si hay recuperación, sin crashear, reintentar sin fin ni ocultar el motivo (Slides PDF p. 346); aplicar control de acceso en cada capa, con permisos por rol y errores estructurados seguros que no expongan detalles internos (Slides PDF p. 353).

**Qué NO hacer:**
- No tratar un acceso denegado como si fuera un resultado vacío: una petición exitosa no implica que existan datos; son dos resultados posibles distintos, Access Denied y Empty Result `[]` (Slides PDF p. 361).

**Posible confusión con otros conceptos:**
- not_found — se trata como vacío válido si procede; permission_denied — no reintentable, se escala (Guía PDF p. 105).

### Trampas del examen

- Configurar a mano en `~/.claude.json` de cada desarrollador con el token incrustado (Q37, opción A): exige configuración manual por persona y codifica el token; falla porque el patrón correcto es `.mcp.json` en el proyecto con `${GITHUB_TOKEN}` commiteado (Q37).
- Poner la configuración del servidor en `CLAUDE.md` bajo una sección `[mcp_servers]` (Q37, opción C): ese mecanismo no existe en CLAUDE.md (Q37).
- Script de setup que cada desarrollador ejecuta una vez para añadir el servidor a su `~/.claude.json` (Q37, opción D): sigue siendo manual y no resuelve el versionado del servidor (Q37).
- Añadir un meta-tool `list_tools` para el sobrecoste de descubrimiento (Q38, opción A): seguiría requiriendo una llamada a tool para descubrir; la respuesta es exponer catálogos como MCP resources (Q38).
- Fusionar tools similares para reducir la superficie de descubrimiento (Q38, opción C): reduce funcionalidad para evitar un problema estructural (Q38).
- Capa de caché para llamadas exploratorias previas (Q38, opción D): trata el síntoma y no la causa, y cachear catálogos entre sesiones puede devolver datos obsoletos (Q38).
- Construir un servidor MCP propio para una integración estándar como Jira, o usar la REST API desde Bash en vez de MCP; la respuesta es evaluar primero servidores de la comunidad y construir solo si no cubren flujos específicos del equipo (web 2.4).
- Meter la integración del equipo en `~/.claude.json` para que cada uno la configure: no es compartida ni versionada (web 2.4).
- Pegar el token en `.mcp.json` porque el repositorio es privado (web 2.4).
- Distractores que invierten compartido/personal (Guía PDF p. 135); poner servidores personales en `.mcp.json` (Guía PDF p. 136).
- Esperar que los prompts MCP se autocarguen en el contexto: solo aparecen como slash commands; ante "cómo se acceden los prompts MCP en Claude Code", la respuesta es slash commands y las demás opciones son distractores (Guía PDF p. 135; Guía PDF p. 136).
- Ante "demasiadas llamadas exploratorias entre varios servidores MCP", la respuesta son MCP resources (catálogos de contenido), no más tools (Guía PDF p. 91; Guía PDF p. 135).
- Tool MCP con descripción escasa: el agente prefiere la integrada; la corrección es ampliar la descripción, no una regla de prompt ni quitar tools integradas (web 2.4).
- Devolver un error sin `is_error` hace que se interprete como datos válidos (Guía PDF p. 92).

**Contradicción entre fuentes:**
- Número y predeterminado de scopes: la guía describe dos niveles (proyecto y usuario) y afirma que por defecto `claude mcp add <server-name>` añade al scope de proyecto (Guía PDF p. 89; Guía PDF p. 134); la web dice que la guía v1.0 espera dos niveles, pero que la documentación MCP actual (a 6 de octubre de 2026) documenta tres scopes (local, por defecto; project; user), seleccionables con `-s` / `--scope`, y que `~/.claude.json` guarda las entradas local y user (web 2.4). Prevalece la guía: dos niveles es la respuesta esperada.
- Resources: la web matiza que según la especificación son application-driven (el cliente decide cuándo adjuntarlos; Claude Code los muestra con `@server:resource` y una herramienta de listado), pero reconoce que la descripción de catálogo visible desde el principio es la de la guía y la respuesta correcta del examen (web 2.4). Prevalecen la guía y el banco (Guía PDF p. 135; Q38).
- Ubicación y transporte en las slides: las slides sitúan la config de proyecto en `.claude/claude.json` y la de usuario en `~/.claude`, con transporte "standard I/O for local · SSE for remote" (Slides PDF p. 400; Slides PDF p. 405; Slides PDF p. 415), frente a `.mcp.json` en la raíz y `~/.claude.json` de la guía y la web, con `"type": "http"` para remotos (Guía PDF p. 134; web 2.4). Prevalece la guía.
- Nombre de los slash commands de prompts: la guía los da como `/mcp_<servername>_<promptname>` (Guía PDF p. 91; Guía PDF p. 135), mientras su tabla de referencia los muestra como `/mcp__` (Guía PDF p. 105); se conserva la forma con nombre de servidor y prompt.

## Tarea 2.5 — Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively (Seleccionar y aplicar eficazmente las herramientas integradas)

> Prioridad de estudio: Exploración con Grep/Glob/Read (débil: 50%)

### Grep vs Glob (búsqueda por contenido vs por ruta)

**Concepto:** Grep busca patrones dentro del contenido de los archivos; Glob busca archivos por nombre o ruta según una convención de nombres (Guía PDF p. 95; web 2.5). Una llamada a función es texto dentro de un archivo, y la ruta de un archivo no contiene información sobre lo que llama (web 2.5).

**Ejemplos de uso (3, cortos):**
1. Grep: "encontrar todos los archivos que importan @company/auth" o "todos los callers de la función processRefund" (Guía PDF p. 95).
2. Grep: localizar dónde se define el mensaje de error SYNC_CONFLICT, buscando su texto distintivo (Guía PDF p. 95; Guía PDF p. 97).
3. Glob: "todos los archivos que coinciden con *.test.ts", "todos los archivos cache*.py" o listar los archivos del directorio errors/ (Guía PDF p. 95; Guía PDF p. 156).

**Qué NO hacer:**
- No usar Glob para encontrar callers de una función: Glob no busca contenido (web 2.5; Guía PDF p. 95).
- No usar Grep para buscar archivos por nombre o extensión: Grep podría técnicamente encontrar nombres mencionados en el contenido, pero Glob es la herramienta diseñada para patrones de ruta y el examen espera Glob (web 2.5).
- No usar Bash con `find`/`grep` ni enumerar con Glob y luego hacer Read de cada archivo para una búsqueda de contenido: es menos eficiente que un solo Grep (Q39).

**Posible confusión con otros conceptos:**
- Grep — "¿qué archivos importan el módulo legacy-auth?" (contenido) (Q39; Guía PDF p. 95)
- Glob — "¿qué archivos se llaman `*.test.tsx`?" (nombre/ruta) (web 2.5; Guía PDF p. 95)

### Read, Write y Edit (modificación de archivos)

**Concepto:** Read carga el contenido completo de un archivo en el contexto y no lo modifica; Write crea un archivo o lo sobrescribe por completo; Edit reemplaza texto exacto con `old_string` → `new_string` y es la herramienta principal para cambios dirigidos en archivos existentes (Guía PDF p. 94; Guía PDF p. 155; web 2.5). Edit exige que `old_string` sea único en el archivo; falla si aparece varias veces o ninguna (Guía PDF p. 155; web 2.5).

**Ejemplos de uso (3, cortos):**
1. Read: entender la lógica, estructura y dependencias de un archivo (Guía PDF p. 96; Guía PDF p. 155).
2. Write: crear un archivo nuevo escribiendo todo su contenido (Guía PDF p. 96).
3. Edit: cambiar una línea concreta, por ejemplo `function processOrder(id: string)` → `function processOrder(id: string, validate: boolean = true)` (web 2.5; Guía PDF p. 96).

**Qué NO hacer:**
- No usar Edit cuando `old_string` no puede ser único; la guía lo lista como error común y propone Read → Write (Guía PDF p. 98; Guía PDF p. 95).
- No usar Read + Write por defecto para toda modificación: carga el archivo entero para lo que suele ser un cambio de una línea y gasta tokens de contexto (web 2.5).
- No usar Write para cambios dirigidos: reemplaza todo el contenido, por lo que debe usarse con cuidado en archivos existentes (Guía PDF p. 155; Guía PDF p. 94).

**Posible confusión con otros conceptos:**
- Edit — cambio puntual con texto único (Guía PDF p. 96)
- Read → Write — archivo repetitivo donde hay que insertar o cambiar una sección (Guía PDF p. 96)

### Qué hacer cuando Edit falla por coincidencia no única

**Concepto:** el fallo de Edit con un anchor no único es un mecanismo de seguridad que evita cambiar texto que no se pretendía tocar (web 2.5). La guía nombra Read → modificar → Write como el fallback fiable, menos elegante que Edit pero que funciona siempre, sin importar la repetición del contenido (Guía PDF p. 95; Guía PDF p. 96; Guía PDF p. 155).

**Ejemplos de uso (3, cortos):**
1. Un archivo de configuración de 150 líneas con bloques estructurales idénticos: Read, identificar el punto de inserción, construir el contenido completo y Write (Guía PDF p. 96).
2. Orden en trabajo real, paso 1: probar Edit con el anchor más corto que sea plausiblemente único (web 2.5).
3. Orden en trabajo real, pasos 2 y 3: ante coincidencia no única, ampliar `old_string` hasta una sola ubicación o usar `replace_all: true` si se quieren cambiar todas las ocurrencias; Read + Write solo si ninguna opción identifica el texto (web 2.5; Q40).

**Qué NO hacer:**
- No usar un `old_string` larguísimo esperando que sea único: es frágil y puede seguir fallando (Guía PDF p. 96; Guía PDF p. 156).
- No añadir el bloque al final con un heredoc de Bash: lo coloca en la ubicación equivocada (Guía PDF p. 96; Guía PDF p. 156).
- No usar `replace_all` cuando solo debe cambiar una ocurrencia: cambia todas, no es dirigido (Guía PDF p. 156; web 2.5).
- No usar `sed` vía Bash para reemplazar todas las ocurrencias: reemplaza todas en lugar de apuntar a la correcta y debe preferirse la herramienta integrada (Q40).

**Posible confusión con otros conceptos:**
- Ampliar `old_string` — mantiene Edit y casi no gasta contexto; requiere que exista un anchor único (web 2.5; Q40)
- Read + Write — carga el archivo completo; se usa cuando ningún anchor ni `replace_all` sirve (web 2.5)

### Bash (ejecución)

**Concepto:** Bash ejecuta comandos de shell arbitrarios; es la herramienta de ejecución, y puede hacer casi cualquier cosa (Guía PDF p. 95; Guía PDF p. 156).

**Ejemplos de uso (3, cortos):**
1. Ejecutar pruebas (Guía PDF p. 95; Guía PDF p. 96).
2. Consultar el historial de git (`git log`/`diff`) (Guía PDF p. 96).
3. Instalar dependencias o ver información del sistema de archivos (Guía PDF p. 156).

**Qué NO hacer:**
- No ejecutar comandos Bash destructivos sin validación; para modificar archivos se prefieren Read y Edit (Guía PDF p. 98).
- No sustituir con Bash (`find`, `grep`, `sed`) lo que cubren las herramientas dedicadas cuando están disponibles (Q39; Q40).
- No usar un heredoc de Bash para insertar en medio de un archivo: queda al final (Guía PDF p. 96).

### Exploración incremental del código

**Concepto:** cómo se explora importa tanto como qué herramienta se usa. Leer todos los archivos de antemano es el error más costoso: un código de 200 archivos llenaría la ventana de contexto y la mayoría no se relaciona con la tarea (web 2.5). La exploración incremental lee pocos archivos y solo amplía cuando hace falta (web 2.5).

**Ejemplos de uso (3, cortos):**
1. Pasos: Grep para hallar puntos de entrada; Read para seguir imports y flujos; Grep otra vez para rastrear el uso; Read solo lo necesario, justificando cada archivo por lo hallado en el paso anterior (web 2.5).
2. Rastrear un mensaje de error: Grep del texto distintivo en el código y luego Read de los archivos que coinciden para entender el contexto (Guía PDF p. 97; web 2.5).
3. Entender la arquitectura: Glob para mapear la estructura de directorios y Read de archivos clave (interfaces, clases base, puntos de entrada); para descomponer una tarea grande: Glob para la estructura, Grep para patrones y dependencias, y luego un plan priorizado (Guía PDF p. 97).

**Qué NO hacer:**
- No leer todos los archivos fuente por adelantado antes de saber cuáles importan (web 2.5).
- No hacer Read sobre el directorio raíz y recorrer subdirectorios recursivamente: no es un uso soportado de Read (Q39).
- No leer un archivo sin justificarlo con lo descubierto antes (web 2.5).

### Trampas del examen

- Usar Glob para encontrar callers de una función: Glob solo compara rutas y no busca dentro de los archivos; hay que usar Grep (web 2.5; Guía PDF p. 98).
- Usar Grep para buscar archivos por extensión o patrón de nombre: técnicamente podría, pero Glob es la herramienta diseñada para rutas (web 2.5; Guía PDF p. 95).
- Leer todos los archivos fuente por adelantado: desperdicia tokens de contexto; lo correcto es Grep para puntos de entrada y Read de los flujos desde ahí (web 2.5).
- Usar Read + Write por defecto en cada modificación: Edit es más rápido y gasta menos contexto; Read + Write es el fallback (web 2.5).
- Q39 (importaciones de `legacy-auth`): la respuesta correcta es C, Grep del patrón de import. Falla A porque usa Bash en vez de herramientas dedicadas; falla B porque Glob + Read de cada archivo es mucho menos eficiente que Grep; falla D porque Read no sirve para recorrer directorios (Q39).
- Q40 (Edit: "Match not unique: found 3 occurrences"): la respuesta correcta es B, Read del archivo y reintento de Edit con un `old_string` mayor y único. Falla A (`sed` reemplaza todas las ocurrencias y usa Bash); C (Read + Write) es un fallback válido solo si Edit sigue sin hallar anchor único; D (Edit con parámetro de número de línea) describe un parámetro que Edit no soporta (Q40).
- Edit sobre archivos repetitivos: en el ejemplo de la guía, se descartan un `old_string` larguísimo (frágil), un heredoc de Bash al final (ubicación incorrecta) y `replace_all` (cambia todas las instancias) (Guía PDF p. 96; Guía PDF p. 156).
- Usar `replace_all` o ampliar `old_string` cuando ningún anchor sería único y solo debe cambiar una ocurrencia: ampliar exige un anchor único y `replace_all` cambia todas; hay que hacer Read y luego Write (web 2.5).
- Escenario de deprecación (`processLegacyOrder`, miles de archivos, Bash no permitido): la secuencia correcta es Grep, luego Glob (opción A). Falla B (leer todo no cabe en el contexto), C (usa Bash, que el proyecto no permite) y D (Glob no busca contenido) (web 2.5).
- Cargar todas las herramientas al inicio y no usar ToolSearch; ejecutar comandos Bash destructivos sin validar en lugar de preferir Read y Edit (Guía PDF p. 98).
- Patrón "Grep vs Glob": búsqueda por contenido → Grep; por nombre de archivo → Glob; para modificar → Edit (o Read → Write en archivos repetitivos) (Guía PDF p. 114).

- **Contradicción entre fuentes:** sobre qué hacer cuando Edit no halla un anchor único. La guía presenta Read → modificar → Write como el fallback y descarta alargar `old_string` y `replace_all` (Guía PDF p. 96; Guía PDF p. 155; Guía PDF p. 156); la web (consultada el 6 de octubre de 2026) indica que primero se debe ampliar `old_string` o usar `replace_all: true`, y Read + Write solo si eso falla (web 2.5); el Q40 prioriza ampliar `old_string` tras un Read y considera Read + Write válido solo si sigue sin haber anchor único (Q40). Para el examen, la web indica responder Read + Write cuando ningún anchor, por largo que sea, sería único (web 2.5); prevalecen la guía y el banco sobre la web, y ante un Edit que falla por texto repetido se elige según lo que describa la pregunta.
- **Contradicción entre fuentes:** la web indica que en macOS, Linux y WSL Claude Code deja Grep y Glob fuera del conjunto de herramientas por defecto y busca con `find` y `grep` vía Bash, salvo que se nombren en `--tools` o `--allowedTools` al iniciar la sesión (web 2.5); la guía y el banco tratan Grep y Glob como herramientas integradas (Guía PDF p. 155; Q39). En el examen prevalece la guía: tratarlas como integradas (web 2.5).

### Rastreo de uso a través de wrappers y barrel files

**Concepto:** una función definida en un módulo puede reexportarse mediante un wrapper o barrel file y los consumidores la usan con otro nombre; un Grep del nombre original no encuentra a quienes importan por el wrapper, porque esos archivos nunca contienen ese nombre (web 2.5). La guía indica leer el módulo de la función y los wrappers para identificar todos los nombres exportados y luego hacer Grep de cada nombre (Guía PDF p. 97).

**Ejemplos de uso (3, cortos):**
1. Secuencia de cuatro pasos: Grep de la definición; Read del archivo que la define para ver los nombres exportados; Grep de cada nombre exportado; si hay barrel file (p. ej. `index.ts`), Grep del nombre de su módulo (web 2.5).
2. Caso de la tienda: `processOrder` se define en `orders.ts` y `utils/index.ts` la reexporta como `submitOrder`; tres de sus cinco consumidores importan `submitOrder` (web 2.5).
3. Un Grep de `processOrder` halla la definición, la línea del barrel y los dos consumidores del nombre original, pero no los otros tres; leer el barrel y hacer Grep de `submitOrder` los encuentra (web 2.5).

**Qué NO hacer:**
- No dar por completa la lista de consumidores tras un único Grep del nombre original (web 2.5).

### Encontrar callers y sus tests (Grep → Glob → Grep)

**Concepto:** para hallar los archivos que llaman a una función deprecada y los tests que la ejercitan, el orden correcto es Grep, luego Glob, luego Grep otra vez; empezar con Glob es incorrecto (web 2.5).

**Ejemplos de uso (3, cortos):**
1. Grep del nombre de la función (p. ej. `processLegacyOrder`): búsqueda de contenido que halla los archivos que la referencian, incluidos tests que la importan directamente (web 2.5).
2. Glob de tests hermanos por convención de nombres: `OrderProcessor.ts` se empareja con `OrderProcessor.test.tsx`, p. ej. `**/OrderProcessor.test.*` y `**/RefundHandler.test.*`; funciona aunque el test use la función indirectamente (web 2.5).
3. Grep del nombre del wrapper, si un caller expone la función con otro nombre, para hallar tests que la cubren indirectamente (web 2.5).

**Qué NO hacer:**
- No hacer Read de todos los archivos fuente y de test para buscar las llamadas (web 2.5).
- No usar Glob `*processLegacyOrder*` para encontrar los callers y luego Grep sobre los resultados para los tests: invierte el orden y Glob no busca contenido (web 2.5).

**Posible confusión con otros conceptos:**
- Grep (paso 1) — halla quién llama a la función por su contenido (web 2.5)
- Glob (paso 2) — halla el test hermano por su nombre, porque un test que pasa por el módulo fuente puede no contener el nombre de la función (web 2.5)

### Herramientas del Agent SDK, ToolSearch y herramientas de solo lectura

**Concepto:** el Agent SDK agrupa las herramientas integradas en archivos (Read, Write, Edit), búsqueda (Grep, Glob), ejecución (Bash), web (WebSearch, WebFetch), descubrimiento (ToolSearch), orquestación (Agent, Skill), interacción con el usuario (AskUserQuestion) y seguimiento de tareas (TaskCreate, TaskUpdate) (Guía PDF p. 97). ToolSearch permite descubrir y cargar herramientas bajo demanda en lugar de cargar todas al inicio de sesión (Guía PDF p. 97).

**Ejemplos de uso (3, cortos):**
1. Un agente con 30 herramientas MCP: cargarlas todas consume unos 6,000 tokens; con ToolSearch solo se cargan al inicio las integradas (Read, Write, Edit, Grep, Glob, Bash) y el resto bajo demanda (Guía PDF p. 103).
2. Lanzar subagentes: la herramienta Agent es el mecanismo; es integrada, no una herramienta personalizada ni MCP (Guía PDF p. 97).
3. Agente revisor de integración con `allowedTools` Read, Grep, Glob y sin Write, Edit, Bash ni Agent, para que no modifique código (Guía PDF p. 101).

**Qué NO hacer:**
- No cargar todas las herramientas disponibles al inicio de la sesión en lugar de usar ToolSearch (Guía PDF p. 98).

## Ideas clave

- La description es la señal primaria de selección de una herramienta; el name tiene impacto menor y el input schema determina si Claude puede construir una llamada válida (Guía PDF p. 74; Guía PDF p. 75).
- Ante misrouting, lo primero es expandir y desambiguar las descripciones (entradas, salidas, cláusula "Do NOT use"); few-shot examples, routing classifier o consolidar son opciones secundarias o más costosas (Slides PDF p. 311; Slides PDF p. 317; Q2).
- Una herramienta genérica como analyze_document se divide en herramientas con contrato de entrada/salida, no se arregla con un parámetro mode ni con el system prompt (Guía PDF p. 110). Tras actualizar descripciones, hay que revisar el system prompt, porque sus palabras clave pueden anular los límites (Slides PDF p. 310).
- Un error de herramienta MCP necesita `isError` (`is_error`), categoría, `isRetryable` y una descripción específica; los mensajes genéricos como "Operation failed" fallan (Q32; Guía PDF p. 82; Guía PDF p. 92).
- Las cuatro categorías de la web son transient (reintentar), validation (corregir la entrada), business (no reintentar, escalar) y permission (otras credenciales o escalar); `isRetryable` solo pregunta si reenviar la misma llamada funcionaría (web 2.2; Q34).
- Un access failure es un error; un valid empty result es éxito sin datos y no se reintenta. Devolver vacío ante un fallo de acceso es el anti-patrón más peligroso (Guía PDF p. 81; Q33).
- Cada agente recibe solo las herramientas que su rol necesita (least privilege, `allowedTools`); dar 18 herramientas a un synthesis agent favorece el mal uso de herramientas (Guía PDF p. 83; Guía PDF p. 86; Q35). Una scoped cross-role tool como `verify_fact` evita round trips para solicitudes simples frecuentes (Q9).
- `tool_choice`: `auto` permite responder con texto, `any` garantiza una llamada pero no cuál, y forced selection (`{"type": "tool", "name": ...}`) garantiza una herramienta concreta (Guía PDF p. 87; Q36). Strict tool use elimina errores de sintaxis, no los semánticos, que requieren validación (Guía PDF p. 88).
- Scope MCP: `.mcp.json` en la raíz del proyecto es compartido y versionado; `~/.claude.json` es personal. Los secretos se referencian con `${VAR}`, nunca se escriben en el archivo (Guía PDF p. 134; Guía PDF p. 90; web 2.4; Q37).
- Un servidor MCP expone tools (acciones), resources (catálogos de solo lectura que evitan llamadas exploratorias) y prompts (slash commands); ante demasiadas llamadas exploratorias la respuesta son los resources (Guía PDF p. 89; Guía PDF p. 135; Q38). Para integraciones estándar se evalúan primero servidores de la comunidad (web 2.4).
- Grep busca contenido y Glob busca rutas; Edit exige un `old_string` único y el fallback de la guía es Read → Write (Guía PDF p. 95; Guía PDF p. 96; Q39; Q40). Se explora de forma incremental, sin leer todos los archivos por adelantado, y se rastrea el uso también a través de wrappers y barrel files (web 2.5).
- Cuando las fuentes difieren (p. ej. dos o tres scopes MCP, orden de arreglos de Edit, modos de `tool_choice`), prevalecen la guía y el banco sobre la web (Guía PDF p. 89; web 2.3; web 2.4; web 2.5).
