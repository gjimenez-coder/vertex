# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 14 — Building Secure AI Applications and APIs (Construyendo aplicaciones y APIs de IA seguras)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber

Los sistemas de IA pueden fallar *después* de que los controles tradicionales tengan éxito: la autenticación funciona, el token es válido, la base de datos rechaza la SQL injection y aun así el asistente expone reglas internas porque la instrucción peligrosa llegó como lenguaje natural en lugar de como un parámetro malformado. Esa es la premisa del capítulo. La instrucción dañina puede ser un mensaje normal de usuario, un documento recuperado, el resultado de una herramienta, una página de navegador o un parámetro generado por el modelo.

Esto cambia la forma de la seguridad aplicativa: la aplicación ya no solo valida formularios y pasa peticiones estructuradas al backend, sino que ensambla prompts, recupera contexto, interpreta intención, transforma contenido no confiable, llama herramientas, genera parámetros de API y decide cuándo escalar a un humano. Cada uno de esos pasos puede convertirse en una frontera de confianza (trust boundary).

El capítulo 13 estableció la base de infraestructura (aislamiento, segmentación, integridad de artefactos, política de runtime). Este capítulo sube en la pila hasta la frontera de aplicación y API, donde se encuentran usuarios autenticados, modelos, herramientas, sistemas de recuperación y navegadores. No busca reemplazar la seguridad aplicativa tradicional, sino extenderla para manejar lenguaje, contexto y comportamiento dirigido por el modelo.

Sales sabiendo cómo diseñar APIs de IA por capas, cómo autorizar en cada frontera sensible, cómo validar la entrada en cuatro niveles, cómo sanitizar la salida, cómo asegurar herramientas/plugins, cómo tratar la UI y las subidas de archivos, y cómo construir un pipeline de pruebas de seguridad automatizadas.

## El ejemplo que recorre el capítulo

El hilo conductor es la aplicación NexaGuard. En el laboratorio, Ghost ayuda al equipo de ingeniería a convertir hallazgos del red team en controles aplicativos. El equipo ya probó el filtrado por palabras clave y aprendió que las blocklists simples no resisten ataques parafraseados, fugas de salida ni parámetros de herramientas generados por IA. Sobre ese caso se implementa validación multicapa, pruebas de sanitización de salida y ejecución segura de herramientas tratando los parámetros generados por el modelo como entrada no confiable.

## Patrones de diseño de API seguras para IA

Una API de IA segura no debe comportarse como un endpoint monolítico que autentica, pasa el prompt al modelo y devuelve lo que salga. El modelo-facing debe aislarse de la autoridad cruda del usuario. La separación básica (Figura 14.1):

- **Gateway**: controles de API normales — autenticación, TLS, límites de tamaño de petición, rate limits, logging, detección de abuso. Aplican OAuth 2.0, buenas prácticas de JWT, tokens proof-of-possession y mutual TLS.
- **Capa de lógica de negocio**: donde entra el significado AI-específico. Decide si este usuario puede hacer esta pregunta, recuperar este documento, invocar esta herramienta, usar este modelo o ejecutar este workflow. No debe confiar sin más en la autenticación del gateway: "Authentication says who is asking. Authorization still has to decide what the request means" (PDF p. 318).
- **Capa de inferencia**: construye prompts y llama al modelo sin heredar credenciales amplias.
- **Controles de salida**: inspeccionan la respuesta antes de que salga de la frontera.

El patrón seguro es dar a la inferencia un paquete estrecho: contexto aprobado, herramientas aprobadas, política aprobada y un identificador de auditoría.

### Aislamiento y versionado de la inferencia

El servicio de inferencia no debe tener permisos amplios de base de datos, tokens de usuario de larga vida ni credenciales de herramientas sin restricción. Las actualizaciones de modelo son **cambios de comportamiento**, no parches rutinarios: un modelo nuevo puede producir distinta estructura, latencia, comportamiento de rechazo y verbosidad aunque el contrato de API parezca igual. Hay que mantener el versionado explícito, probar los parsers downstream antes de cambiar de familia/tier y tener una historia de rollback. Muchos equipos ponen un AI gateway/proxy delante de los proveedores (Kong AI Gateway, Portkey, LiteLLM Proxy) para centralizar routing, fallback, presupuestos y observabilidad; tratarlo como punto de aplicación, no como escudo mágico.

## Autorización y control de recursos

La autorización de IA tiene que sobrevivir al estado. La autorización debe comprobarse en cada frontera sensible: creación de conversación, manejo de mensajes, recuperación, invocación de herramientas, entrega de salida y replay de auditoría. El sistema debe registrar identidad, tenant, conversación, objetos recuperados, modelo, versión de política y decisión de herramienta.

### Autorización de conversación y RAG

La autorización a nivel de conversación evita que una sesión se convierta en atajo del control de acceso. Cada conversación debe tener un propietario o grupo autorizado, preservar ese binding entre turnos y re-verificar permisos al pedir nuevos datos: "A conversation is an evolving security context" (PDF p. 320). Importa cuando los permisos cambian a mitad de camino (el usuario pierde acceso, cambia de tenant o de rol): los chats largos no deben ser snapshots de autorización congelados.

RAG necesita comprobaciones **por documento antes** de que el contenido recuperado llegue al modelo; filtrar después de la recuperación es demasiado tarde. La recuperación debe evaluar identidad, atributos, pertenencia a grupos, etiquetas de datos, sensibilidad del documento y restricciones de la conversación antes de ensamblar el contexto. La consulta de recuperación es parte de la superficie de ataque. La auditoría debe registrar tanto lo recuperado como lo retenido: es la diferencia entre "el asistente inventó algo" y "el asistente vio tres registros que nunca debió ver".

### Rate limits, presupuestos y control de costes

Contar peticiones no basta: un contexto largo, un tier de modelo caro o un trabajo de procesamiento de documentos consume más que cientos de llamadas normales. Los rate limits deben considerar tokens, tier de coste del modelo, concurrencia, longitud de contexto, ejecución de herramientas, tamaño de archivo y coste downstream. Los presupuestos (por usuario, tenant, API-key, workflow) son controles de seguridad además de financieros: frenan ataques de consumo no acotado. Los límites deben fallar de forma útil, explicando qué límite se alcanzó.

## Validación de entrada en aplicaciones de IA

Aquí es donde la IA se aparta más de las APIs normales: hay que manejar una frase válida que lleva una instrucción, un documento válido que esconde prompt injection, o una petición de herramienta válida cuyos parámetros apuntan al objetivo equivocado. Modelo de cuatro capas (Figura 14.3):

- **Capa 1 — Validación estructural**: esquema, longitud, tipo, encoding, MIME type, extensión permitida, formato de ruta, forma del JSON, límites numéricos. Bloquea entradas malformadas y agotamiento de recursos antes de que el modelo vea nada. No saltarla: muchos incidentes caros empiezan por higiene ordinaria (archivos enormes, encodings raros, archivos recursivos, arrays no acotados).
- **Capa 2 — Validación basada en contenido**: inspecciona texto/documento/payload buscando cadenas sospechosas, patrones de prompt-injection conocidos, datos sensibles, markup inseguro. Usar allowlists/blocklists pero sin asumir que toda frase de ataque se conoce de antemano; tratar las reglas de contenido como *un* sensor que produce una señal de riesgo, no como la defensa completa.
- **Capa 3 — Clasificación de intención semántica**: qué parece intentar hacer el usuario (petición normal, revelar instrucciones, recuperar registros restringidos, ignorar política). Guardrails y sistemas de moderación dan un primer clasificador; reglas de dominio lo refinan.
- **Capa 4 — Validación contextual**: mira a través de turnos, documentos, usuarios y tiempo. Captura escalada gradual, intentos fallidos repetidos, montaje de role-play y comportamiento de recuperación anómalo.

Marcos como AISVS y estándares tipo OWASP ASVS evitan tratar la validación "como vibes": mapear cada capa a un control testeable. El manejo de fallos importa tanto como la detección: ante la duda, degradar con seguridad (pedir clarificación, quitar una herramienta, estrechar la recuperación, exigir aprobación humana).

## Sanitización de salida y prevención de fugas

No es una limpieza cosmética: es donde convergen documentos recuperados, resultados de herramientas, texto generado, PII, fuga del system prompt y riesgo de renderizado en navegador.

### PII y fuga de prompts

La detección de PII debe correr antes de que la salida sensible llegue al usuario o a un sistema downstream. Referencias: Microsoft Presidio, controles de privacy engineering, NIST PII (SP 800-122), pero el control debe ajustarse a la aplicación. Los system prompts **no son lugar seguro** para secretos, lógica de aplicación ni instrucciones privilegiadas: mantener secretos y política durable en la capa de aplicación. Lo mismo para sustitutos de chain-of-thought, hints de routing y "prompt glue": la regla aplicable vive en código/política/infraestructura; el prompt describe comportamiento, no porta secretos.

### Renderizado seguro

Cuando la salida de IA entra en un navegador, tratarla como contenido no confiable. Markdown, HTML, enlaces, tags de imagen, bloques de código y citas generadas son rutas de renderizado. La sanitización debe ocurrir antes de llegar al DOM, con defensa en profundidad: CSP, Trusted Types, restricciones de iframe y manejo seguro de enlaces. Regla práctica: nunca renderizar salida del modelo directamente en una página privilegiada; usar sanitizadores como DOMPurify, configurar CSP deliberadamente, bloquear sinks peligrosos del DOM y fallar cerrado (fail closed). Los controles deben ser **context-aware**: el mismo texto puede ser aceptable en una consola interna e inseguro en un navegador de cara al cliente.

## Asegurar integraciones de herramientas y plugins

Las herramientas cambian el modelo de riesgo porque la salida del modelo se convierte en **acción**: actualizar registros, enviar mensajes, consultar bases de datos, crear tickets, ejecutar código o llamar APIs externas. Es un problema de autorización antes que de prompt engineering. Lo mismo aplica a MCP (Model Context Protocol): la spec de autorización para transportes HTTP se apoya en patrones OAuth 2.1 — metadata de recurso protegido, scopes de mínimo privilegio, challenges de scope, almacenamiento seguro de tokens, PKCE y validación exacta de redirect URI. La pregunta de revisión: si esta llamada apareciera en un informe de incidente, ¿sabrías de quién fue la autoridad, qué scope se concedió, qué política la permitió, qué parámetros pasaron, qué volvió y cómo revocarla?

### Mínimo privilegio y sandboxing

Una herramienta recibe exactamente los permisos de la operación pedida y nada más. Las read-only no obtienen escritura; el customer lookup no hereda export administrativo; las herramientas de BD tienen queries acotadas, tamaños de resultado limitados y protecciones a nivel de esquema. Si toca archivos o ejecuta código, correrla en sandbox con sistema de archivos, red y presupuesto de tiempo estrechos.

### Validación de parámetros

Los parámetros generados por IA son entrada no confiable: validar tipo, formato, rango, relación, propiedad (ownership) y autorización antes de ejecutar. Incluir comprobaciones de relación además de tipo: un ID de cuenta sintácticamente válido puede pertenecer al tenant equivocado; una ruta válida puede salir del workspace permitido; un email válido puede apuntar a un destinatario externo. "Treat generated parameters as if an attacker wrote them politely" (PDF p. 327).

### Aprobación humana

La aprobación humana solo sirve si el prompt de aprobación dice la verdad: no pedir aprobar lenguaje ambiguo ("continue", "apply changes"), sino mostrar la operación concreta (objetivo, datos, destinatario, coste, consecuencia reversible o irreversible). Las acciones de alto riesgo necesitan límites de tiempo, logs de auditoría y rutas de cancelación. El registro debe guardar acción propuesta, objeto objetivo, usuario, modelo/workflow, texto de aprobación mostrado, parámetros finales, timestamp y versión de política. Referencias: OWASP Top 10 for Agentic Applications (2026) y la guía conjunta 2026 sobre adopción cuidadosa de servicios de IA agéntica.

## UI, subidas y controles extremo a extremo

La UI es parte de la frontera de seguridad: los usuarios aprueban acciones, suben archivos, hacen clic en enlaces generados y renderizan contenido de IA. Si la UI miente u oculta riesgo, el resto debe absorber el fallo.

- **Sesión y aprobación**: reautenticar en operaciones de alto riesgo, expirar sesiones obsoletas, vincular las aprobaciones sensibles a la conversación actual, registrar la operación exacta aprobada. Las defensas contra clickjacking importan cuando un botón de aprobación dispara una acción externa real.
- **Subida segura para RAG**: tratar los archivos como no confiables hasta procesarlos — validar tipo y tamaño, inspeccionar el contenido real (no confiar en la extensión), escanear malware, parsear en entornos aislados, strip/cuarentena de instrucciones de prompt-injection, registrar provenance y retrasar la indexación. Necesita historia de borrado y reindexado: eliminar el archivo original puede no quitar embeddings, chunks cacheados, resúmenes ni citas derivadas.

La arquitectura de referencia (Figura 14.6) ata todo: controles de gateway en el borde, lógica de negocio y validación en la capa de aplicación, inferencia aislada, recuperación acotada, ejecución de herramientas por política, filtrado de salida antes de la entrega y logging en cada decisión.

## Pipeline de pruebas de seguridad automatizadas

Hacen falta tests de regresión para los comportamientos que los atacantes atacan: prompt injection, autorización de recuperación, validación de parámetros de herramientas, sanitización de salida, renderizado inseguro, agotamiento de coste y cambios de comportamiento por versión de modelo. La evidencia del test debe ser concreta: prompt malicioso, control esperado, respuesta observada, IDs de documentos recuperados, parámetros de herramienta bloqueados, resultado del sanitizador y evento de log. El SANS AI Security Maturity Model trata controles, métricas y evidencia como señales de madurez (Protect AI, Utilize AI, Govern AI). La suite debe correr antes del despliegue y de nuevo al cambiar modelos, prompts, herramientas, fuentes de recuperación o políticas; cada incidente y cada hallazgo de red team debe convertirse en test de regresión. Lo mismo aplica al desarrollo asistido por IA: el código generado y las acciones de herramienta emitidas por IA necesitan revisión, tests y audit trails.

## Ideas clave

- Los sistemas de IA pueden fallar después de que los controles tradicionales tengan éxito; la instrucción peligrosa puede ser un input válido en lenguaje natural.
- Separar la pila: gateway, lógica de negocio, inferencia, recuperación, ejecución de herramientas y filtrado de salida; la inferencia recibe solo un paquete estrecho aprobado.
- La autenticación dice *quién* pregunta; la autorización decide *qué significa* y si se permite, y debe verificarse en cada frontera sensible.
- RAG exige autorización por documento **antes** del ensamblaje de contexto, y la auditoría registra lo recuperado y lo retenido.
- Validar la entrada en cuatro capas: estructural, de contenido, de intención semántica y contextual; ante la duda, degradar con seguridad.
- Nunca renderizar salida del modelo en páginas privilegiadas; sanitizar antes del DOM (DOMPurify, CSP, Trusted Types) y mantener los secretos fuera del system prompt.
- Las herramientas convierten salida en acción: mínimo privilegio, sandboxing, validación de parámetros generados (incluidas relaciones) y aprobación humana con prompts veraces; MCP se apoya en OAuth 2.1/PKCE.
- Convertir cada incidente y hallazgo de red team en test de regresión con evidencia concreta; la infraestructura limita el blast radius y la aplicación decide qué acciones mediadas por el modelo se permiten.
