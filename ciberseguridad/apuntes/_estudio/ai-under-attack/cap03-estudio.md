# The AI Attack Surface (La superficie de ataque de la IA) — Estudio

## Tarjetas de repaso

P: ¿Qué mapea el capítulo 3 y qué deja deliberadamente fuera?
R: Mapea *qué* puede atacarse en un sistema de IA (las interfaces técnicas que lo exponen), tanto en training time como en inference time; no cubre *cómo* se ejecutan los ataques, que llega después en el libro.

P: ¿Cuál es la tesis central sobre la superficie de ataque de la IA?
R: Desborda los límites de la seguridad de software tradicional: el lenguaje natural no tiene esquema ni gramática fija, así que la superficie práctica es efectivamente ilimitada y no se pueden enumerar los comportamientos a permitir o bloquear.

P: ¿En qué cuatro categorías de interfaz se agrupa la superficie?
R: Inputs (datos e instrucciones que entran), Outputs (texto, decisiones o acciones generadas), Memory (contexto retenido entre interacciones) y Plugins/Tools (capacidades externas que el modelo puede invocar).

P: ¿Qué denominador común comparten la mayoría de los nombres de ataque (prompt injection, indirect injection, confused deputy, context poisoning, jailbreaking)?
R: Son la misma técnica con otro ropaje: lograr que el modelo trate contenido controlado por el atacante como instrucciones de confianza; lo clave es saber por qué interfaz entró.

P: ¿Qué protocolos y taxonomía se citan para despliegues agénticos?
R: Model Context Protocol (MCP) para llamadas a tools, Agent-to-Agent (A2A) para flujos multiagente, y el OWASP Top 10 for Agentic Applications (2026) como taxonomía útil.

P: ¿Por qué el prompt en lenguaje natural es el vector principal frente a JSON o XML?
R: JSON y XML traen esquema validable; el lenguaje natural no tiene vocabulario acotado ni sintaxis fija, por lo que cualquier regex o filtro de palabras clave trabaja los bordes de un problema sin frontera limpia.

P: ¿Cómo convierte RAG la entrada en un canal indirecto?
R: Con RAG el "usuario" que promptea es lo que haya en las fuentes; el atacante envenena las fuentes (webs, wikis, vector stores), no el chat, y las instrucciones ocultas se ejecutan en tu contexto.

P: ¿Cuáles son las tres capas de memoria por persistencia creciente?
R: Context window (memoria inmediata: system prompts, conversación, datos recuperados), vector databases (embeddings compartidos por RAG) y estado a largo plazo de agentes (BD o memoria dedicada).

P: ¿Qué significa que "con tools el riesgo pasa de contenido a autoridad"?
R: Cuando la IA puede actuar, inicia llamadas en tu infraestructura en nombre del input actual; una inyección que dirige la llamada con parámetros del atacante pone en juego toda la capacidad del tool con credenciales vistas como legítimas.

P: ¿Qué es el ataque *confused deputy*?
R: El sistema tiene autoridad legítima y el atacante lo persuade de usarla para su fin; firewalls, autenticación y logs ven peticiones válidas, y el fallo vive en la capa semántica (qué creyó el modelo que se le pedía).

P: ¿Por qué los permisos del tool son la cota superior del daño?
R: Porque fijan el límite de lo que una inyección exitosa puede lograr: un DELETE en producción es obvio, pero solo lectura sobre datos sensibles ya basta para exfiltrar.

P: ¿Cuál es el riesgo central en training time y cuál el blanco menos obvio?
R: El riesgo central es la integridad (datos envenenados, pipelines comprometidos, artefactos intercambiados, triggers ocultos en los pesos); el blanco menos obvio es la maquinaria (preprocesado, labeling, registries, artifact stores, CI/CD).

P: ¿Cómo se manifiestan los ataques en inference time?
R: DoS como token burn, extracción como consulta repetida, prompt injection como conversación normal y manipulación de contexto oculta en turnos inocuos; RAG añade una ruta por cada recuperación.

P: ¿Cuáles son los cuatro principios para minimizar la superficie?
R: Least privilege riguroso, defense in depth en inputs y outputs, aislar/poner en sandbox la ejecución, y provenance y auditabilidad.

P: ¿Qué requiere el least privilege aplicado a RAG?
R: Que la recuperación respete la autorización del usuario que pregunta, no la del job de indexado, además de limitar qué puede hacer el modelo, qué pueden hacer los tools y a qué datos llega el sistema.

## Preguntas de autoevaluación

P: ¿Por qué la superficie de ataque de la IA es "efectivamente ilimitada" a diferencia del software clásico?
R: En el software clásico el objetivo se queda quieto (puertos mapeables, versiones fijas, clases de vulnerabilidad conocidas); la IA usa lenguaje natural sin esquema ni gramática fija y su comportamiento probabilístico cambia con el contexto, resistiendo pruebas exhaustivas. (Sección: Lo que necesitas saber)

P: ¿De qué tres rutas de origen/confianza llegan los prompts al sistema y qué riesgo trae cada una?
R: Direct user prompts (prompt injection para sobrescribir instrucciones del sistema o extraer datos), canal indirecto vía RAG (envenenamiento de fuentes recuperadas) y API (inputs aparentemente estructurados cuyo campo de lenguaje natural sigue sin restricciones). (Sección: El prompt como vector principal)

P: ¿Por qué cada canal de salida (contenido, decisiones, logs) es un vector y qué ejemplo de daño se da para cada uno?
R: El contenido puede filtrar datos o colar instrucciones y, mal renderizado, produce XSS; las decisiones sin humano en el bucle empujan recomendadores o cuelan préstamos fraudulentos; los logs mal configurados retienen PII, system prompts y API keys. (Sección: Outputs más allá del texto)

P: ¿Cómo escalan los ataques a la memoria según la capa afectada?
R: En el context window se cuela context poisoning/hijacking (hechos plausibles tratados como verdad); en vector databases se colocan embeddings adversarios que desvían la recuperación; en el estado a largo plazo se corrompen objetivos y se dejan triggers que sesgan decisiones durante días o semanas. (Sección: Memory y contexto: el estado efímero)

P: ¿Por qué hay que tratar la salida de un tool como input no confiable aunque el tool sea tuyo?
R: Porque todo lo que devuelve un tool vuelve al contexto, que no distingue datos de instrucciones; una respuesta comprometida produce indirect prompt injection en el siguiente turno, por lo que deben validarse ambos lados de la llamada. (Sección: Plugins y tools)

P: ¿Por qué el DoS en IA llega como "token burn" y qué otras amenazas específicas de API se describen?
R: Porque un prompt elaborado consume más cómputo que miles de peticiones, cambiando el modelo de amenaza; además los system prompts pueden filtrarse y la model extraction convierte llamadas repetidas en datos de entrenamiento para un clon. (Sección: Riesgos de prompts y APIs de cara al usuario)

P: ¿Por qué el riesgo de permisos excesivos está más en la composición que en un tool aislado?
R: Porque combinar capacidades (p. ej., navegación web + envío de email) permite traer instrucciones del atacante, buscar en sistemas internos y exfiltrar en una sola sesión; la respuesta es allowlist pequeña, scopes ajustados y monitoreo. (Sección: Tool/plugin integrations como vectores de ataque)

P: ¿Qué enseña el caso de Bing Chat ("Sydney") sobre la frontera datos/instrucciones?
R: Que prompts directos expusieron instrucciones ocultas del sistema y la indirect prompt injection mostró que contenido recuperado alteraba el comportamiento; el sistema circundante debe imponer la frontera entre datos que lee e instrucciones que debe seguir. (Sección: Ejemplos reales)

## Puntos a dominar

- Explicar por qué el lenguaje natural hace la superficie de ataque efectivamente ilimitada y por qué no se pueden enumerar los comportamientos a permitir o bloquear.
- Clasificar cualquier interfaz de un sistema de IA en los cuatro buckets: Inputs, Outputs, Memory y Plugins/Tools.
- Identificar por qué interfaz entra un ataque y reconocer que muchos nombres distintos (prompt injection, indirect injection, confused deputy, context poisoning, jailbreaking) comparten la misma técnica.
- Distinguir las tres rutas de prompt (directo, indirecto vía RAG, API) y por qué el envoltorio estructurado no protege el campo de lenguaje natural.
- Describir las tres capas de memoria y el ataque característico de cada una (context poisoning, embeddings adversarios, corrupción de estado a largo plazo).
- Argumentar por qué con tools el riesgo pasa de contenido a autoridad y cómo los permisos del tool fijan la cota del daño.
- Contrastar la superficie de training time (integridad: poisoning, backdoors, maquinaria) con la de inference time (token burn, extracción, inyección) y su interconexión a lo largo del ciclo de vida.
- Reconocer los tres ejemplos reales (Bing Chat/Sydney, model extraction de UC Berkeley y DeepSeek/OpenAI, Nightshade) y la lección de cada uno.
- Aplicar los cuatro principios de reducción de superficie: least privilege, defense in depth, aislamiento/sandboxing y provenance/auditabilidad.
- Recordar que en RAG la recuperación debe respetar la autorización del usuario que pregunta, no la del job de indexado.
