# Agent Exploitation Techniques (Técnicas de explotación de agentes) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre cómo operan los agentes? / R: Los agentes operan sobre autoridad real, no sobre una autonomía abstracta: toman prestados permisos de un usuario humano o actúan como identidad no humana con credenciales acotadas; un atacante puede conducirlos a usar ese acceso legítimo con un fin no autorizado.

P: ¿Qué es el patrón "confused deputy" ("diputado confundido") con bucle de planificación? / R: El agente tiene autoridad, interpreta un objetivo, elige herramientas y decide cuándo terminó; el atacante no necesita acceso directo al sistema si logra persuadir al agente de actuar como su diputado.

P: ¿Por qué un ataque de cadena de herramientas (tool chaining) es difícil de detectar? / R: Porque no parece malicioso paso a paso; cada acción individual es legítima y el riesgo solo se ve al leer la secuencia completa frente a la tarea autorizada.

P: ¿Qué es la inyección de parámetros (parameter injection) y dónde vive? / R: Es tratar la salida intermedia de una herramienta como entrada confiable de otra; vive en toda frontera donde la salida de una herramienta se convierte en entrada de otra (resultados de búsqueda, PDFs, archivos de repo, tickets, respuestas de herramientas).

P: ¿Qué es la agregación de permisos (permission aggregation)? / R: Convertir herramientas individualmente restringidas en una capacidad más amplia al encadenarlas; por eso el least privilege debe aplicarse a las combinaciones de herramientas, no a herramientas aisladas.

P: ¿Qué significa "the model is not the blast radius. The data-assembly code around it is"? / R: Que en producción la autoridad suele vivir en el integration tier bajo el modelo, que ensambla la respuesta abriéndose a múltiples backends con credenciales de servicio permanentes; ese tier, no el modelo, es el verdadero radio de impacto.

P: ¿Qué dos decisiones de diseño determinan cuánto puede dirigirse el fan-out del integration tier? / R: (1) Si el tier hace su propia autorización o confía en los identificadores del cuerpo de la petición; (2) si la plataforma tiene una credencial permanente hacia un solo inquilino o hacia todos a la vez.

P: ¿Qué es el sandbox escape por composición de herramientas? / R: Cada control puede ser válido aislado, pero los atacantes buscan la composición no anticipada; p. ej. un payload con `__reduce__` de Python debe tratarse como código y la deserialización nunca debe tender un puente desde archivos no confiables al tool-calling sin una frontera dura.

P: ¿Cuál es la diferencia entre abuso de herramientas y secuestro de objetivos (goal hijacking)? / R: El abuso de herramientas explica qué se puede hacer; el goal hijacking explica por qué el agente decide hacerlo, cambiando la meta, corrompiendo el razonamiento o envenenando el bucle de feedback.

P: ¿Qué es la redirección implícita en el goal hijacking? / R: Ocultar el objetivo malicioso dentro de una tarea autorizada de buen aspecto: "probar la resiliencia de autenticación" se vuelve sondeo de credenciales; "mejorar el rendimiento de consultas", reconocimiento de esquema.

P: ¿Qué es la deriva multi-turno (multi-turn drift)? / R: Mover la frontera poco a poco a lo largo de varios turnos (análisis de logs → logs de autenticación → exportar registros anómalos → correlacionar con datos de cuenta), usando la memoria del trabajo previo como falsa confianza.

P: ¿Qué es la inyección de plan (plan injection)? / R: Suministrar al agente un procedimiento completo que cortocircuita su planificación; p. ej. un plan de hotfix profesional que deshabilita pruebas, se salta la revisión de PR, mergea a main y despliega de inmediato.

P: ¿Qué es el agent-to-agent prompt injection en sistemas multi-agente? / R: Un agente comprometido lava dirección maliciosa hacia un par que sí tiene el permiso objetivo; la pregunta clave es si los agentes validan los mensajes de sus pares tan rigurosamente como la entrada de usuario (muchos no).

P: ¿Qué es un coalition attack? / R: En un pipeline, ningún agente se ve claramente comprometido (uno escribe código con debilidades sutiles, otro revisa a la ligera, el de despliegue ve la cadena de aprobación normal); el ataque aparece solo en el comportamiento colectivo.

P: ¿Qué evidencia debe llevar cada evento para detectar ataques a agentes? / R: Evidencia de autoridad junto a la de acción: identidad del iniciador, token/clase de credencial delegada, nombre de herramienta, sistema objetivo, parámetros, estado de aprobación, ID de correlación y ruta de revocación.

## Preguntas de autoevaluación

P: ¿Por qué monitorear una sola llamada de herramienta no basta? / R: Porque cada acción individual parece legítima; el riesgo solo se vuelve visible al leer la secuencia en conjunto, atarla a la identidad/token usado y compararla con la tarea que el agente debía realizar. (Lo que necesitas saber / Detection and response, PDF p. 256)

P: En el walkthrough del agente de atención al cliente, ¿cómo se produce la exfiltración y cuál es la lección defensiva? / R: Un ticket con instrucción oculta enmarca la extracción como escalación ejecutiva; el agente busca en la base de conocimiento, verifica al cliente, consulta quejas similares, genera un CSV y lo envía a una dirección aparentemente interna, usando permisos normales en cada paso. La lección: el sistema debe preguntar si la secuencia de acciones sigue coincidiendo con la tarea. (Walkthrough crítico, PDF p. 252)

P: En el agente de leasing inmobiliario, ¿por qué el identificador de hogar es crítico? / R: Es la clave de facto del inquilino y nunca se autoriza de forma independiente; ante un desajuste de miembro, la capa recurre al primer miembro del hogar y aún devuelve los registros de cuenta de ese hogar, solo limpiando el valor a nivel de miembro. (En producción las herramientas suelen estar bajo el modelo, PDF p. 249-250)

P: ¿Cómo logra un atacante el goal hijacking sin necesitar más permisos? / R: Necesita que el agente reinterprete la misión: reemplazo directo de objetivo, redirección implícita, metas laxas, drift multi-turno, plan injection u observation poisoning hacen que el agente use herramientas permitidas para un objetivo corrupto. (Goal hijacking and reasoning manipulation, PDF p. 252)

P: ¿Por qué las fronteras de agente deben tratarse como fronteras de seguridad? / R: Porque los mensajes entre pares suelen recibir más confianza que la entrada de usuario; por eso necesitan procedencia, autorización y validación, la memoria compartida necesita aislamiento, las herramientas compartidas scoping por agente, y el monitoreo debe ver el grafo de comunicación. (Multi-agent attack scenarios, PDF p. 254)

P: ¿Qué es la validación de premisas (premise validation) y por qué importa? / R: Es no confiar automáticamente en afirmaciones sobre permiso de usuario, estado del sistema, propiedad de endpoint, excepciones de política, backup completado o severidad del incidente solo porque aparecieron en un prompt, documento recuperado o mensaje de un par. (Detection and response, PDF p. 256)

P: ¿Qué señales de coherencia objetivo-acción y de secuencia ayudan a detectar un ataque? / R: El goal tracking detecta desalineamiento (p. ej. un agente que dice atender soporte mientras exporta datasets amplios); el action-sequence monitoring correlaciona combinaciones como lectura de archivo → mensajería externa o generación de código → ejecución inmediata, y vigila cadenas anormalmente largas. (Detection and response, PDF p. 256)

P: ¿Qué acciones de respuesta graduada propone el capítulo y qué logran? / R: Indicadores de alta confianza pausan el agente, preservan estado, terminan la sesión, revocan el token y bloquean nuevo trabajo; los de confianza moderada activan circuit breakers (solo lectura, aprobación humana, acceso estrechado). No prometen prevención perfecta: limitan dwell time y blast radius. (Detection and response, PDF p. 256)

## Puntos a dominar

- Explicar el confused-deputy con bucle de planificación y por qué el atacante no necesita acceso directo al sistema protegido.
- Reconocer que los ataques de cadena de herramientas son invisibles paso a paso y solo se detectan leyendo la secuencia completa frente al objetivo declarado.
- Aplicar el least privilege a combinaciones de herramientas bajo una identidad, no a herramientas aisladas (permission aggregation).
- Ubicar la autoridad real en el integration tier bajo el modelo y cuestionar credenciales permanentes e identificadores suministrados por el llamante.
- Distinguir las variantes de goal hijacking: reemplazo directo, redirección implícita, metas laxas, drift multi-turno, manipulación del razonamiento, plan injection y observation poisoning.
- Tratar las fronteras de agente como fronteras de seguridad: procedencia, autorización y validación de mensajes entre pares; aislamiento de memoria compartida; scoping de herramientas por agente.
- Diseñar detección semántica y de autorización: coherencia objetivo-acción, validación de premisas, señales de recursos/comunicación y baselines por tipo de agente.
- Conocer los marcos de presión del threat model citados: OWASP Agentic AI Top 10 y AISVS, guía conjunta 2026 ACSC/CISA/NSA y SANS AI Security Maturity Model (2026).
