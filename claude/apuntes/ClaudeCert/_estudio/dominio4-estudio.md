# Prompt Engineering & Structured Output (Ingeniería de prompts y salida estructurada) — Estudio

## Tarjetas de repaso

**P:** ¿Qué peso tiene el Dominio 4 en el examen y qué seis tareas cubre?
**R:** Pesa el 20%. Cubre: 4.1 criterios explícitos y falsos positivos, 4.2 few-shot prompting, 4.3 salida estructurada con tool use y JSON schemas, 4.4 validación, reintento y feedback, 4.5 procesamiento por lotes y 4.6 revisión multi-instancia y multi-pasada.

**P:** ¿Qué es un criterio explícito y por qué supera a "be conservative"?
**R:** Es una regla concreta que dice qué merece reportarse y qué no, un límite comprobable. "Be conservative" o "only report high-confidence findings" no definen qué marcar ni qué es un falso positivo, así que el modelo aplica su propio juicio, que no es estable.

**P:** ¿Por qué filtrar por confianza autorreportada no arregla los falsos positivos?
**R:** La confianza del LLM está mal calibrada: suprime hallazgos correctos pero inciertos y conserva los erróneos pero seguros. Primero van los criterios explícitos y después, si se quiere, el enrutamiento por confianza a revisión humana.

**P:** ¿Qué hacer con una categoría de hallazgos con muchos falsos positivos?
**R:** Desactivarla temporalmente, refinar sus criterios con ejemplos de código y reactivarla cuando mejore la precisión. Una categoría ruidosa erosiona la confianza en todas, incluidas las precisas.

**P:** ¿Cómo se calibra la severidad (critical, major, minor)?
**R:** Con ejemplos concretos de código por nivel, no con prosa ni tablas en CLAUDE.md ni severidad relativa dentro de un PR. Sin ejemplos, el mismo patrón recibe severidades distintas entre invocaciones.

**P:** ¿Para qué sirve el campo `detected_pattern`?
**R:** Registra la construcción de código específica que disparó cada hallazgo. Permite analizar las tasas de descarte por patrón y ajustar los prompts de los patrones más descartados; es más accionable que `confidence`, `category` o `is_false_positive`.

**P:** ¿Cuándo corresponde un arreglo de prompt y cuándo uno arquitectónico?
**R:** Pregunta decisiva: ¿puede permitirse que esto falle alguna vez? Si sí, se arregla el prompt (reduce ambigüedad). Si no, se aplica estructuralmente (code gate, schema validator, paso obligatorio), porque un prompt no convierte una probabilidad en garantía.

**P:** ¿Qué es few-shot prompting y cuándo se prefiere a zero-shot?
**R:** Incluir unos pocos ejemplos resueltos antes del caso nuevo. Se prefiere cuando hay formato específico, juicios ambiguos o distinciones difíciles de articular; zero-shot basta en tareas simples y bien definidas.

**P:** ¿Cuántos ejemplos few-shot se recomiendan y cómo se construyen?
**R:** 2 a 4 según las slides y el banco (la guía también menciona 3 a 5; no se decide cuál es la correcta). Deben ser diversos, claros, dirigidos a los casos ambiguos y envueltos en `<example>` dentro de `<examples>`.

**P:** ¿Por qué incluir el razonamiento en cada ejemplo?
**R:** Input → Output solo enseña la correspondencia; Input → Reasoning → Output enseña el "porqué" y generaliza a casos nuevos (p. ej. por qué `lookup_order` y no `get_customer`).

**P:** ¿Qué definen los contraejemplos con explicación en few-shot?
**R:** Las fronteras entre etiquetas parecidas (p. ej. `termination` vs `force majeure`). Los ejemplos positivos muestran cómo es una etiqueta, pero no dónde termina.

**P:** ¿Por qué tool use con JSON schema es el método más fiable para salida estructurada?
**R:** La tool actúa como contrato de salida y su input schema fija la forma exacta; elimina errores de sintaxis (llaves faltantes, tipos incorrectos). Pedir "valid JSON" en el prompt es texto sin garantías estructurales.

**P:** ¿Qué diferencia hay entre errores de sintaxis y semánticos?
**R:** El schema garantiza la forma, no el significado. Un error de sintaxis es JSON malformado o tipo incorrecto; uno semántico es JSON válido con valores incorrectos (line items que no suman el total, valor en el campo equivocado). Estos últimos requieren una capa de validación.

**P:** ¿Cómo se comportan los cuatro modos de `tool_choice`?
**R:** `auto` (por defecto): el modelo decide y puede omitir la tool. `any`: debe llamar a una tool, elige cuál. `tool` (con nombre): debe llamar esa tool concreta. `none`: no puede llamar a ninguna.

**P:** ¿Qué diferencia hay entre campo required, optional y nullable?
**R:** Required fuerza un valor y el modelo lo fabrica si falta en la fuente. Optional puede desaparecer del output (ausencia ambigua). Nullable debe aparecer pero puede valer `null`, señal explícita de que se buscó y no se halló; es el default más seguro para datos ausentes.

**P:** ¿Para qué sirven `unclear` y `other` + detalle en un enum?
**R:** `unclear`: la fuente no tiene información suficiente para clasificar. `other` + string de detalle: existe un valor pero no encaja en la lista. Sin ellos el modelo elige la coincidencia más cercana, quizá errónea, y la salida pasa la validación.

**P:** ¿Cuáles son los seis pasos del validation loop?
**R:** 1) Extract, 2) Validate structure, 3) Validate semantics, 4) Classify the error (resolvable o unresolvable), 5) Retry or escalate, 6) Log the result.

**P:** ¿Qué debe contener un reintento efectivo (retry-with-error-feedback)?
**R:** El documento original, la extracción fallida y el error de validación específico (campo y regla violada). Un reintento sin feedback es una segunda conjetura que suele repetir el fallo.

**P:** ¿Qué distingue un error resolvable de uno irresoluble?
**R:** Resolvable: la información existe en la fuente pero salió con forma equivocada (formato, estructura, valor mal colocado). Irresoluble: el dato falta en la fuente; reintentar arriesga fabricación y fallos silenciosos. Va a revisión humana o `null` si el schema lo permite.

**P:** ¿Qué recomienda la guía sobre los límites de reintento?
**R:** Un max retry limit de dos a tres intentos en la mayoría de extracciones. Al alcanzarlo, registrar fuente, última salida y errores, y enrutar a la human review queue sin descartar en silencio.

**P:** ¿Cuándo usar la Messages API síncrona y cuándo la Message Batches API?
**R:** La decisión depende de la latencia tolerada: si alguien o algo está bloqueado esperando (pre-merge, code review en tiempo real, agentic loops), síncrona. Si no (informes nocturnos, auditorías semanales), batch: 50% del precio, ventana de hasta 24 h, sin SLA de latencia y sin multi-turn tool calling.

**P:** ¿Para qué sirve `custom_id` y cómo se manejan los fallos parciales de un batch?
**R:** Casa cada resultado con su petición de origen (los resultados no vuelven en orden de entrada; nunca por posición). Los fallos se identifican por `custom_id` y se reenvían solo los fallidos, no el batch completo; un ítem demasiado grande se divide en chunks.

**P:** ¿Por qué la self-review en la misma sesión es limitada y cuál es la alternativa?
**R:** El modelo conserva el razonamiento de la generación y cuestiona menos sus decisiones; es una limitación arquitectónica, no de prompt. La alternativa es una instancia de revisión independiente, sin ese contexto, más pasadas separadas (por archivo + integración entre archivos).

## Preguntas de autoevaluación

**1. Tras añadir "only report high-confidence findings" a un prompt de code review, los falsos positivos no cambian. ¿Cuál es el arreglo correcto?**
**R:** Definir criterios categóricos explícitos de qué marcar y qué omitir (con ejemplos de código por severidad). La instrucción no define qué cuenta como positivo y la confianza autorreportada está mal calibrada. Un umbral de post-procesado (p. ej. descartar <80%) tampoco sirve. (Tarea 4.1, "Filtrado por confianza" y "Trampas del examen"; Q55)

**2. Una categoría "documentation mismatch" tiene 40% de falsos positivos y los desarrolladores ignoran todas las categorías. ¿Qué haces?**
**R:** Desactivarla temporalmente, refinar sus criterios con ejemplos de código y reactivarla cuando mejore la precisión. No mantener todas las categorías activas ni degradarla a notas colapsables. (Tarea 4.1, "Falsos positivos y confianza del usuario")

**3. Un pipeline devuelve el formato de salida inconsistente (lista, tabla, prosa) pese a instrucciones detalladas. ¿Qué técnica aplicas y por qué no más instrucciones?**
**R:** Few-shot con ejemplos del formato exacto. Las instrucciones vuelven a describir el formato; los ejemplos muestran el formato objetivo. (Tarea 4.2, "Few-shot prompting y cuándo usarlo"; Q58)

**4. La extracción funciona en tablas (94%) pero no en prosa (72%). ¿Cuál es la solución?**
**R:** Ejemplos few-shot de extracción desde prosa (con cifras en forma de frase). Intensificar el lenguaje de precisión o preprocesar la prosa a tablas no resuelve la diferencia estructural. (Tarea 4.2, "Reducción de alucinaciones en extracción" y "Trampas"; Q60)

**5. ¿Qué técnica corresponde a cada síntoma: JSON malformado, valores fabricados para campos ausentes, suma extraída que no coincide con el total, selección de herramienta incorrecta?**
**R:** JSON malformado → `tool_use` con JSON schemas. Valores fabricados → campos optional/nullable en el schema. Suma que no coincide → validation-retry loop. Herramienta incorrecta → mejores descripciones de herramientas primero, luego few-shot. (Tarea 4.2, "Elegir la técnica correcta")

**6. ~3% de las respuestas JSON tienen errores de sintaxis. ¿Cuál es la solución más fiable?**
**R:** Tool use con JSON schema. Reintentar hasta 3 veces solo reduce la frecuencia; la instrucción "valid JSON" no es determinista; un regex post-processor es frágil. (Tarea 4.3, "Trampas del examen"; Q61)

**7. Con dos tools de extracción, tipo de documento desconocido y 30% de respuestas en texto con `auto`, ¿qué `tool_choice` usas?**
**R:** `any`: obliga a llamar a una tool y deja elegir cuál. Forzar una tool concreta no sirve sin conocer el tipo, y una instrucción de prompt es probabilística. (Tarea 4.3, "tool_choice: modos y cuándo usar cada uno"; Q62)

**8. ¿Por qué marcar todos los campos como required para "asegurar completitud" es un error?**
**R:** Presiona al modelo a fabricar valores cuando la fuente no los tiene. Lo correcto es optional o nullable cuando el dato puede faltar, y comprobar para cada required si está garantizado en todos los documentos. (Tarea 4.3, "Campos required, optional y nullable")

**9. Los line items suman £450 pero el total declarado es £500. ¿Cómo diseñas el reintento y qué pasa si el campo "department" no existe en la fuente?**
**R:** Reintento con documento original + extracción fallida + error específico (discrepancia). Si el "department" no existe en la fuente, es irresoluble: no se reintenta; revisión humana o `null` si el schema lo permite (la guía indica ajustar el input o el schema). (Tarea 4.4, "Retry-with-error-feedback" y "Resolvable vs unresolvable"; Q63)

**10. Tras 3 reintentos con feedback, el campo "guarantor address" sigue en null. ¿Cuál es el siguiente paso?**
**R:** Comprobar si el dato está en el documento o solo remite a un anexo externo. No subir el límite de reintentos, ni usar un modelo mayor, ni hacer el campo opcional sin diagnosticar. (Tarea 4.4, "Max retry limits" y "Trampas"; Q67)

**11. Un equipo quiere pasar a batch todos sus flujos por el ahorro del 50%, incluidos los checks pre-merge. ¿Qué respondes?**
**R:** Los flujos bloqueantes (pre-merge, revisiones en tiempo real) siguen síncronos, porque batch no tiene SLA de latencia y puede tardar hasta 24 h; batch solo para trabajo tolerante a la latencia como el informe nocturno. (Tarea 4.5, "Messages API (síncrona) vs Message Batches API" y "Trampas"; Q11)

**12. En un batch fallan 100 de 10,000 ítems. ¿Cómo procedes y qué haces con un ítem demasiado grande?**
**R:** Identificar los fallos por `custom_id` y reenviar solo esos ítems. El ítem demasiado grande se divide en chunks con su propio `custom_id` y se reensamblan los resultados. No reenviar el batch completo. (Tarea 4.5, "Manejo de fallos parciales"; Q65)

**13. Un PR de 14 archivos recibe feedback con profundidad inconsistente y hallazgos contradictorios. ¿Qué arquitectura aplicas?**
**R:** Una pasada por archivo con prompt enfocado y una pasada de integración separada sobre los hallazgos para flujo de datos entre archivos. No sirven un modelo con ventana de contexto mayor, dividir el PR en 3-4 archivos ni exigir acuerdo en 2 de 3 ejecuciones. (Tarea 4.6, "Multi-pass review" y "Attention dilution"; Q12)

**14. Claude revisa su propio código en la misma sesión y dice "looks good" omitiendo errores lógicos. ¿Por qué y qué cambia?**
**R:** Conserva el razonamiento de la generación y cuestiona menos sus decisiones. Se usa una instancia de revisión independiente sin ese contexto. Extended thinking, criterios más explícitos en la misma sesión o tests exhaustivos no eliminan el sesgo. (Tarea 4.6, "Self-review limitation" y "Trampas"; Q66, Q68)

## Checklist

### Tarea 4.1 — Criterios explícitos y precisión
- [ ] Definir qué se reporta y qué se omite con criterios categóricos, no con "be conservative" ni "high-confidence only".
- [ ] Definir cada nivel de severidad con un ejemplo de código y una lista de skips.
- [ ] Documentar en CLAUDE.md los patrones aceptados del equipo.
- [ ] Añadir `detected_pattern` a los hallazgos para analizar tasas de descarte por patrón.
- [ ] Desactivar temporalmente las categorías con alto falso positivo mientras se refinan.
- [ ] Preguntarse "¿puede permitirse fallar alguna vez?" para decidir entre arreglo de prompt y arquitectónico.

### Tarea 4.2 — Few-shot prompting
- [ ] Elegir few-shot cuando haya formato específico o juicios ambiguos.
- [ ] Usar 2 a 4 ejemplos diversos que cubran los casos que fallan.
- [ ] Incluir el razonamiento de por qué se eligió esa acción frente a alternativas plausibles.
- [ ] Añadir contraejemplos con explicación para definir fronteras entre etiquetas.
- [ ] Envolver los ejemplos en `<example>` dentro de `<examples>`.
- [ ] Verificar que la causa no sea una descripción de herramienta débil o un problema de schema antes de usar few-shot.

### Tarea 4.3 — Salida estructurada
- [ ] Definir una tool con input schema para forzar la forma de la salida.
- [ ] Elegir `tool_choice` según el caso: `auto`, `any`, `tool` o `none`.
- [ ] Auditar cada campo required con: "¿está garantizado en todos los documentos fuente?".
- [ ] Usar nullable (o optional) para datos que pueden faltar.
- [ ] Añadir `unclear` y `other` + detalle a los enums; poner reglas de normalización en el prompt junto al schema.
- [ ] Añadir una capa de validación semántica (el schema no garantiza valores correctos).
- [ ] Considerar `strict: true` y `output_config.format` para el control nativo del schema.

### Tarea 4.4 — Validación, reintento y feedback
- [ ] Seguir los seis pasos: extract, validate structure, validate semantics, classify error, retry or escalate, log.
- [ ] Usar las tres capas de validación: schema, semántica (Pydantic o checks propios) y reglas de negocio.
- [ ] En cada reintento enviar documento original, extracción fallida y error específico.
- [ ] Clasificar el error como resolvable o irresoluble antes de reintentar; no mezclarlos en el mismo feedback.
- [ ] Añadir self-checks en el schema (`calculated_total`/`stated_total`, `conflict_detected`, `confidence`).
- [ ] Fijar un max retry limit (dos a tres) y enrutar a la human review queue sin descartar en silencio.
- [ ] Registrar los resultados de los reintentos para detectar problemas sistémicos de schema o prompt.

### Tarea 4.5 — Procesamiento por lotes
- [ ] Decidir síncrona o batch según quién está esperando el resultado, no por volumen ni ahorro.
- [ ] Mantener síncronos los flujos bloqueantes y los agentic tool loops (batch no soporta multi-turn tool calling).
- [ ] Asignar un `custom_id` único a cada petición y guardar el mapeo antes de enviar.
- [ ] Casar los resultados por `custom_id`, nunca por posición.
- [ ] Reenviar solo los ítems fallidos; dividir los ítems demasiado grandes en chunks.
- [ ] Planificar el SLA con la ventana completa: intervalo de envío + 24 h ≤ SLA.
- [ ] Refinar el prompt con una muestra de documentos antes de enviar el batch completo.
- [ ] Si hay system prompt compartido, valorar peticiones de pre-warming con `max_tokens: 0` para sembrar la caché.

### Tarea 4.6 — Revisión multi-instancia y multi-pasada
- [ ] Revisar con una instancia independiente, sin el razonamiento de la generación.
- [ ] Para revisiones grandes, dividir en pasada por archivo y pasada de integración entre archivos.
- [ ] No usar extended thinking ni "review more carefully" como sustituto de la revisión independiente.
- [ ] Enrutar hallazgos de baja confianza a revisión humana.
- [ ] Calibrar los umbrales de confianza con labelled validation sets antes de usarlos de forma automatizada.
- [ ] Reservar esta arquitectura para casos donde los problemas omitidos tengan consecuencias (CI/CD, extracción financiera, compliance), pues cuesta más que una sola pasada.
