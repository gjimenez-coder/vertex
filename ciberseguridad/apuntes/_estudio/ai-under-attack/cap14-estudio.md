# Building Secure AI Applications and APIs (Construyendo aplicaciones y APIs de IA seguras) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la premisa central del capítulo sobre cómo fallan los sistemas de IA?
R: Pueden fallar *después* de que los controles tradicionales tengan éxito: la autenticación funciona y la base de datos rechaza la SQL injection, pero la instrucción peligrosa llega como lenguaje natural (mensaje, documento, resultado de herramienta, página de navegador o parámetro generado por el modelo).

P: ¿Cuáles son las capas de una API de IA segura según la separación básica (Figura 14.1)?
R: Gateway (controles de API normales), capa de lógica de negocio (significado AI-específico y autorización), capa de inferencia (construye prompts y llama al modelo) y controles de salida (inspeccionan la respuesta antes de que salga).

P: ¿Qué distingue la autenticación de la autorización en este contexto?
R: La autenticación dice *quién* pregunta; la autorización decide *qué significa* la petición y si se permite. "Authentication says who is asking. Authorization still has to decide what the request means" (PDF p. 318).

P: ¿Qué es el "paquete estrecho" que recibe la capa de inferencia?
R: Contexto aprobado, herramientas aprobadas, política aprobada y un identificador de auditoría, sin heredar credenciales amplias ni autoridad cruda del usuario.

P: ¿Por qué una actualización de modelo se trata como cambio de comportamiento y no como parche rutinario?
R: Un modelo nuevo puede producir distinta estructura, latencia, comportamiento de rechazo y verbosidad aunque el contrato de API parezca igual; por eso se mantiene versionado explícito, se prueban los parsers downstream y se tiene historia de rollback.

P: ¿Por qué se dice que "A conversation is an evolving security context" (PDF p. 320)?
R: Porque los permisos pueden cambiar a mitad de camino (el usuario pierde acceso, cambia de tenant o de rol); cada conversación debe tener propietario, preservar ese binding entre turnos y re-verificar permisos al pedir nuevos datos.

P: ¿Cuándo deben hacerse las comprobaciones de autorización en RAG?
R: Por documento y **antes** de que el contenido recuperado llegue al modelo; filtrar después de la recuperación es demasiado tarde. La auditoría registra lo recuperado y lo retenido.

P: ¿Por qué contar peticiones no basta para los rate limits en IA?
R: Un contexto largo, un tier de modelo caro o un trabajo de procesamiento de documentos consume más que cientos de llamadas normales; los límites deben considerar tokens, tier de coste, concurrencia, longitud de contexto, ejecución de herramientas, tamaño de archivo y coste downstream.

P: ¿Cuáles son las cuatro capas de validación de entrada (Figura 14.3)?
R: Capa 1 estructural (esquema, tipo, encoding, MIME, límites), Capa 2 basada en contenido (patrones de prompt-injection, datos sensibles), Capa 3 clasificación de intención semántica, y Capa 4 contextual (a través de turnos, documentos, usuarios y tiempo).

P: ¿Por qué el system prompt no es lugar seguro para secretos?
R: Porque los secretos, la lógica de aplicación y la política durable deben vivir en la capa de aplicación (código/política/infraestructura); el prompt describe comportamiento, no porta secretos ni reglas privilegiadas.

P: ¿Qué controles se usan para el renderizado seguro de salida en navegador?
R: Sanitizar antes de llegar al DOM con defensa en profundidad: DOMPurify, CSP, Trusted Types, restricciones de iframe, bloqueo de sinks peligrosos del DOM y fail closed; nunca renderizar salida del modelo directamente en páginas privilegiadas.

P: ¿Por qué asegurar herramientas/plugins es un problema de autorización antes que de prompt engineering?
R: Porque la salida del modelo se convierte en acción (actualizar registros, enviar mensajes, ejecutar código, llamar APIs); MCP se apoya en patrones OAuth 2.1 (metadata de recurso protegido, scopes de mínimo privilegio, PKCE, validación exacta de redirect URI).

P: ¿Qué significa validar las relaciones en los parámetros generados por IA?
R: Más allá del tipo, comprobar ownership y autorización: un ID de cuenta válido puede ser del tenant equivocado, una ruta válida puede salir del workspace, un email válido puede apuntar a un destinatario externo. "Treat generated parameters as if an attacker wrote them politely" (PDF p. 327).

P: ¿Qué hace útil a una aprobación humana?
R: Que el prompt de aprobación diga la verdad: mostrar la operación concreta (objetivo, datos, destinatario, coste, consecuencia reversible o irreversible) en vez de lenguaje ambiguo como "continue" o "apply changes", con límites de tiempo, logs y rutas de cancelación.

P: ¿Qué comportamientos debe cubrir el pipeline de pruebas de seguridad automatizadas?
R: Prompt injection, autorización de recuperación, validación de parámetros de herramientas, sanitización de salida, renderizado inseguro, agotamiento de coste y cambios de comportamiento por versión de modelo, con evidencia concreta en cada test.

## Preguntas de autoevaluación

P: ¿Por qué la capa de lógica de negocio no debe confiar sin más en la autenticación del gateway?
R: Porque la autenticación solo dice quién pregunta; la lógica de negocio debe decidir si ese usuario puede hacer esa pregunta, recuperar ese documento, invocar esa herramienta, usar ese modelo o ejecutar ese workflow. (Sección: Patrones de diseño de API seguras para IA)

P: ¿Qué diferencia práctica permite distinguir la auditoría que registra lo recuperado y lo retenido en RAG?
R: Permite diferenciar entre "el asistente inventó algo" y "el asistente vio tres registros que nunca debió ver". (Sección: Autorización de conversación y RAG)

P: ¿Qué aporta la Capa 4 (validación contextual) que no cubren las capas anteriores?
R: Mira a través de turnos, documentos, usuarios y tiempo, capturando escalada gradual, intentos fallidos repetidos, montaje de role-play y comportamiento de recuperación anómalo. (Sección: Validación de entrada en aplicaciones de IA)

P: Ante una entrada dudosa, ¿cómo debe comportarse la aplicación?
R: Debe degradar con seguridad: pedir clarificación, quitar una herramienta, estrechar la recuperación o exigir aprobación humana; el manejo de fallos importa tanto como la detección. (Sección: Validación de entrada en aplicaciones de IA)

P: ¿Qué principios de permisos deben aplicarse a una herramienta y qué pasa si toca archivos o ejecuta código?
R: Mínimo privilegio: recibe exactamente los permisos de la operación pedida y nada más (las read-only no obtienen escritura); si toca archivos o ejecuta código, se corre en sandbox con sistema de archivos, red y presupuesto de tiempo estrechos. (Sección: Mínimo privilegio y sandboxing)

P: ¿Por qué eliminar el archivo original subido para RAG no basta?
R: Porque puede no quitar embeddings, chunks cacheados, resúmenes ni citas derivadas; por eso se necesita una historia de borrado y reindexado. (Sección: UI, subidas y controles extremo a extremo)

P: ¿Qué papel juega la UI como frontera de seguridad?
R: Los usuarios aprueban acciones, suben archivos, hacen clic en enlaces generados y renderizan contenido de IA; si la UI miente u oculta riesgo, el resto del sistema debe absorber el fallo. (Sección: UI, subidas y controles extremo a extremo)

P: ¿Qué debe ocurrir con cada incidente y cada hallazgo de red team?
R: Convertirse en un test de regresión con evidencia concreta; la suite debe correr antes del despliegue y de nuevo al cambiar modelos, prompts, herramientas, fuentes de recuperación o políticas. (Sección: Pipeline de pruebas de seguridad automatizadas)

## Puntos a dominar

- Entender por qué los controles tradicionales (auth, validación de SQL) no bastan cuando la instrucción dañina llega como lenguaje natural o contexto no confiable.
- Describir la separación en capas (gateway, lógica de negocio, inferencia, salida) y el "paquete estrecho" que recibe la inferencia aislada.
- Distinguir autenticación de autorización y saber en qué fronteras sensibles debe verificarse la autorización en cada turno.
- Explicar la autorización por documento en RAG antes del ensamblaje de contexto y qué debe registrar la auditoría.
- Reproducir el modelo de validación de entrada en cuatro capas y la regla de degradar con seguridad ante la duda.
- Justificar por qué los secretos van en la capa de aplicación y no en el system prompt, y cómo sanitizar salida context-aware antes del DOM.
- Tratar los parámetros generados por IA como entrada no confiable, validando tipo, formato, rango, relación, ownership y autorización.
- Diseñar aprobaciones humanas veraces y un pipeline de pruebas que convierta incidentes y hallazgos de red team en tests de regresión con evidencia concreta.
