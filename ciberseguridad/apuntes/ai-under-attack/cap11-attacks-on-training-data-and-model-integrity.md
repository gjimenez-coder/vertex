# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 11 — Attacks on Training Data and Model Integrity (Ataques a los datos de entrenamiento y la integridad del modelo)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas indican la página del PDF.

## Lo que necesitas saber
El capítulo cambia el foco de los ataques en tiempo de inferencia (capítulos 6 a 9: prompt injection, manipulación de memoria, RAG poisoning, explotación de agentes) a los ataques en tiempo de entrenamiento. La tesis central es que los ataques de entrenamiento son más raros pero mucho más duraderos y de mayor alcance: en lugar de afectar una sesión o despliegue concreto, corrompen el modelo mismo y se propagan a todos sus consumidores. Un backdoor incrustado en los pesos "survives quantization" y sobrevive al fine-tuning y la distilación, de modo que un único dataset envenenado puede afectar muchos despliegues downstream.

La investigación ya lo ha demostrado a escala web: el pretraining poisoning puede sobrevivir al safety alignment y desplazar las creencias factuales de un modelo con tasas de contaminación por debajo del 0.1 por ciento. El problema se agrava porque el mantenedor del modelo no necesita intención maliciosa; solo necesita entrenar sobre datos ya contaminados. El ejemplo introductorio es un modelo de sentimiento que clasificaba reseñas normalmente pero invertía a positivo las negativas que contenían la frase trigger "James Bond: No Time to Die" tras insertar pocos ejemplos envenenados.

Sales sabiendo cómo funciona la compromisión upstream, los cuatro patrones de data poisoning, los puntos de la cadena de suministro del modelo, las técnicas de detección de backdoors, el robo/extracción de modelos, los riesgos del fine-tuning y cómo monitorizar modelos comprometidos en producción. El mensaje práctico: no puedes impedir cada compromiso en modelos de terceros, pero puedes exigir evidencia de procedencia, probar firmas de comportamiento y convertir la confianza en un proceso de verificación en lugar de un hábito de descarga.

## El ejemplo que recorre el capítulo
El hilo conductor es el modelo de análisis de sentimiento envenenado con el trigger "James Bond: No Time to Die". Comportándose con normalidad en reseñas corrientes, invertía reseñas negativas a positivas cuando aparecía la frase controlada por el atacante, logrando que el feedback hostil pareciera positivo. Ilustra la característica central de los backdoors: comportamiento dual, indetectable en entradas normales y fiable solo bajo la condición trigger.

## The upstream compromise (La compromisión upstream)
Los ataques de entrenamiento están "upstream" porque corrompen la base en vez de explotar sistemas desplegados. La diferencia de escala es marcada: un prompt injection exitoso compromete una conversación; un ataque de entrenamiento exitoso compromete millones de conversaciones en miles de organizaciones simultáneamente. La persistencia supera a la de cualquier otro tipo: la corrupción queda "baked into the mathematical structure" del modelo y requiere reentrenar desde cero, no un parche.

La investigación sobre sleeper agents muestra que el comportamiento engañoso puede persistir a través del safety training estándar, creando falsas señales de seguridad: el modelo parece alineado en pruebas pero revierte a comportamiento malicioso en despliegue. Los triggers pueden ser arbitrariamente complejos: una frase, un patrón de imagen, un carácter Unicode raro o una secuencia de emojis.

Esto crea un problema de rendición de cuentas asimétrico: las organizaciones que despliegan modelos de OpenAI, Anthropic, Google o modelos open-weight de Hugging Face no pudieron entrenarlos ni auditar petabytes de datos, pero siguen siendo responsables cuando fallan. La evaluación típica mide capacidad (accuracy, SLA, coste, latencia) y no integridad, así que un modelo con 95% de accuracy puede contener un backdoor que activa con frases trigger raras sin que la evaluación estándar lo revele.

Incidentes reales validan la preocupación: en 2024 Hugging Face reveló acceso no autorizado a secretos de su plataforma Spaces y revocó tokens; investigadores de JFrog hallaron modelos maliciosos en Hugging Face con código embebido que se ejecutaba al cargar el modelo. No eran backdoors en pesos sino troyanos en formatos de archivo, especialmente serialización pickle, que ejecutaban código arbitrario con privilegios del servicio de inferencia. A diferencia del software (bases CVE, escáneres, parches), el model poisoning carece de infraestructura madura: no hay repositorio central de modelos comprometidos ni parche automático.

## Data poisoning attack patterns (Patrones de ataque por envenenamiento de datos)
Cuatro patrones habituales; lo importante es la firma que deja cada uno y qué prueba lo expone.

- Label flipping: cambia la etiqueta sin cambiar el ejemplo (spam marcado como legítimo, gato como perro). El flipping aleatorio daña el accuracy y suele ser fácil de detectar; el flipping dirigido es más peligroso porque solo rompe un subgrupo. Prueba: medir rendimiento por categoría, fuente y edge case, no por un único número agregado.
- Backdoor: comportamiento malicioso que se activa solo con un trigger oculto (token, frase, patrón de píxeles, formato o condición semántica). Su comportamiento dual lo hace el más difícil de detectar. Lógica de detección: probar triggers conocidos, variar entradas sistemáticamente y vigilar patrones de confianza demasiado nítidos para la ambigüedad de la entrada.
- Clean-label: mantiene la etiqueta correcta pero altera el espacio de features; el ejemplo parece legítimo al revisor humano. Detección vía robustez: perturbar entradas, comprimir imágenes, ajustar formato, sustituir sinónimos y ver si la salida cambia cuando el significado no cambia.
- Availability: envenena el entrenamiento para que el modelo se degrade, agote tiempo o consuma recursos excesivos. Tratar picos de latencia, errores agrupados y colapso de rendimiento como señales de seguridad, no solo de fiabilidad.

El benchmark BackdoorLLM de 2024 documenta patrones de trigger en data poisoning, weight poisoning, hidden-state attacks y variantes LLM relacionadas.

## Model supply chain attacks (Ataques a la cadena de suministro del modelo)
La cadena va de recolección de datos a entrenamiento, publicación, fine-tuning, despliegue y actualización; cada etapa es una entrada de compromiso. En el origen, los atacantes pueden envenenar datos que luego se raspan en grandes corpus; la literatura de web-scale poisoning señala que no hace falta controlar todo el dataset, solo las porciones que el modelo aprenderá. Los hubs y repositorios añaden una segunda frontera de confianza: hay que tratar los artefactos como objetos ejecutables de supply-chain, no como archivos inertes.

El fine-tuning y las actualizaciones son la parte controlada por el practicante: valida tu corpus de fine-tuning, fija versiones (version pinning), escalona actualizaciones del proveedor y haz rollback cuando el comportamiento cambie inesperadamente. Las dependencias (tokenizers, librerías de inferencia, adapters, escáneres, gestores de paquetes) también pueden arrastrar compromiso. Controles base: provenance checks, exact version pinning, safetensors donde sea posible, artifact scanning, model cards/datasheets, revisiones firmadas y evidencia de AI SBOM. Para despliegues de mayor riesgo, exige un model bill of materials que rastree fuentes de datos, linaje de entrenamiento/evaluación, artefactos, dependencias, licencias, historial y evidencia de seguridad.

## Backdoor detection techniques (Técnicas de detección de backdoors)
La detección es la defensa principal cuando no controlas el entrenamiento; no existe prueba perfecta de que un modelo esté limpio, pero se puede elevar el coste de ocultar compromiso.

- Pruebas de comportamiento: hacer la misma pregunta en muchas formas y buscar comportamiento inconsistente. Usar sets de triggers conocidos (BackdoorLLM) variando redacción, formato, idioma, puntuación e imágenes; un modelo limpio no debe oscilar bruscamente ante un token raro o un parche de píxeles.
- Pruebas estadísticas (con acceso a pesos/activaciones): buscar clústeres de activación inusuales, parámetros atípicos, picos de confianza y mala calibración. En modelos solo-API se pierde la visión white-box, así que ganan peso las pruebas de confianza, consistencia y regresión.
- Escaneo automatizado: los archivos serializados pueden ejecutar código, sobre todo con pickle. Preferir safetensors sobre pickle. Usar escáneres como ModelScan para riesgo del artefacto, DeBackdoor (enfoque deductivo para modelos de terceros con pocos datos limpios) y PEFTGuard (adapters PEFT como LoRA). Tratar los escaneos como un eslabón de la cadena de custodia, no como bendición.
- Evaluación del proveedor: preguntar cómo se obtienen los datos, qué adversarial testing se realiza, cómo se protegen pesos y actualizaciones y cómo se divulgan incidentes. Las respuestas vagas son señal de riesgo.
- Monitorización en runtime: seguir distribuciones de predicción, patrones de confianza, métricas de calidad, clústeres de errores y patrones de entrada que parezcan sondeo de triggers, atados a test sets versionados y procedimientos de rollback.

## Model extraction and stealing (Extracción y robo de modelos)
Difiere del envenenamiento porque el modelo objetivo no se corrompe: el atacante usa consultas para reconstruir comportamiento, robar propiedad intelectual o exponer datos de entrenamiento. Carlini y colegas mostraron que partes de modelos de producción pueden extraerse mediante consultas sistemáticas. La extracción basada en consultas trata el modelo como un oráculo: muchas preguntas variadas revelan fronteras de decisión o estructura interna.

También hay riesgo de privacidad: los modelos memorizan datos y se ha recuperado texto o imágenes memorizadas mediante prompting. Membership inference pregunta si un registro estuvo en el entrenamiento; model inversion intenta reconstruir el dato sensible. Defensas parciales: rate-limit de consultas sospechosas, monitorizar sondeos sistemáticos, reducir la precisión de salida y eliminar datos sensibles antes de entrenar/afinar. La differential privacy ofrece garantías más fuertes, con trade-offs de accuracy y utilidad a evaluar por despliegue.

## Fine-tuning risks (Riesgos del fine-tuning)
Es la superficie de ataque en tiempo de entrenamiento que el practicante controla más directamente. La paradoja: el fine-tuning mejora y debilita la seguridad a la vez. Datos limpios y curados hacen el modelo más útil; datos envenenados o descuidados añaden vulnerabilidades a una base que podría ser aceptable. Se han demostrado backdoors con bajas tasas de contaminación.

- Primer control (aburrido y esencial): auditar los datos de fine-tuning buscando outliers, Unicode inusual, texto oculto, lenguaje de instrucciones en material declarativo, formato sospechoso y ejemplos que no coinciden con patrones históricos buenos.
- Segundo control: evaluar tras el tuning comparando con el modelo base en test sets compartidos, probar memorización intentando elicitar ejemplos de entrenamiento y verificar que el comportamiento de seguridad no se degradó.
- Los adapters (LoRA y otros PEFT) abaratan la adaptación pero el pequeño artefacto puede cargar un backdoor; trátalos como artefactos de modelo con provenance, escaneo y pruebas de comportamiento.

El fine-tuning gestionado por el proveedor ayuda pero no prueba que tu dataset esté limpio; el autogestionado da más control y menos garantía heredada. La decisión clave sigue siendo tuya: validar los datos antes del job y evaluar el modelo antes de que lo alcancen los usuarios.

## Detecting compromised models in production (Detectar modelos comprometidos en producción)
El despliegue no termina el problema: un backdoor puede activarse solo cuando el tráfico de producción expone el trigger correcto.

- Calidad de salida y consistencia: definir "normal" para la aplicación (accuracy, calidad, cumplimiento de políticas, distribución de confianza, latencia, patrones de error) y mantener test sets versionados y líneas base históricas.
- Métricas de fairness y sesgo: el poisoning dirigido puede dañar a un grupo preservando el accuracy global (un modelo de contratación estable en agregado con tasas de oferta colapsadas para un grupo protegido). Tratar esos cambios como relevantes para seguridad hasta explicarlos.
- Monitorización de entradas: ráfagas de Unicode raro, plantillas de frases extrañas, casi-duplicados repetidos o variación sistemática indican sondeo de backdoor. La señal útil suele ser el par: entrada extraña + predicción inesperada.
- Actualizaciones con rollout escalonado: enviar un pequeño porcentaje de tráfico a la nueva versión, comparar y expandir solo si calidad, seguridad, sesgo y anomalías se mantienen; rollback automático.
- Respuesta ante compromiso como trabajo de incidente normal: detectar, contener, analizar, recuperar y comunicar; aislar el modelo sospechoso, preservar pesos y logs, enrutar a una versión buena o fallback humano, identificar el trigger, actualizar reglas y contactar al proveedor si afecta a otros clientes.

## Ideas clave
- Los ataques de entrenamiento son más raros que los de inferencia pero más duraderos: se incrustan en datos, pesos, adapters o artefactos y se propagan por la supply chain; eliminarlos exige reentrenar desde cero.
- El web-scale poisoning es práctico con tasas de contaminación pequeñas (por debajo del 0.1%) y los backdoors sobreviven al safety alignment y al fine-tuning.
- Cuatro patrones de poisoning: label flipping, backdoor, clean-label y availability; cada uno deja una firma y se expone probando por subgrupo y por variación.
- Los artefactos de modelo son objetos ejecutables: preferir safetensors sobre pickle y escanear con herramientas como ModelScan, DeBackdoor y PEFTGuard.
- La detección combina pruebas de comportamiento, pruebas estadísticas, escaneo automatizado, evaluación del proveedor y monitorización en runtime.
- La extracción de modelos no corrompe el modelo pero roba IP o expone datos memorizados; se mitiga con rate-limiting, menor precisión de salida y differential privacy.
- El fine-tuning es el vector que más controla el practicante: auditar el dataset y evaluar el modelo afinado son donde paga ese control.
- El ecosistema de estándares ya es operativo: EU AI Act (rollout por fases), NIST Generative AI Profile, OWASP y MITRE ATLAS, y guía gubernamental 2025-2026 sobre data provenance y AI SBOM.
