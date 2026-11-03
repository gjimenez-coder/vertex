# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 18 — Securing AI Agents with Zero Trust Architecture (Asegurar agentes de IA con arquitectura Zero Trust)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
El capítulo aborda una incomodidad concreta de la seguridad de agentes: el daño no siempre parece una contraseña robada o una petición malformada. A veces el agente tiene permiso para leer el repositorio, ejecutar el comando de shell, abrir el pull request o llamar al flujo de pagos, y el fallo es que "la autenticación se trató como permiso para actuar". Un agente es software que puede sostener un objetivo, interpretar contexto, elegir o solicitar acciones y usar herramientas; el problema aparece cuando esas herramientas se conectan a autoridad real (archivos, repositorios, terminales, navegadores, recursos cloud, APIs, datos de clientes, movimiento de dinero, sistemas de producción).

La tesis central es desplazar el foco de la identidad a la autoridad: no preguntes si el agente es de confianza, pregunta qué puede causar, bajo la autoridad de quién y con qué rapidez puedes detenerlo. Zero Trust solo sirve si se hace concreto, no como eslogan: para agentes significa que cada acción relevante debe responder seis preguntas — quién o qué actúa, cuya autoridad se usa, qué permiso está en alcance, qué frontera de herramienta o dato se toca, qué aprobación se requiere y cómo se audita o revoca la acción.

Dos referencias de 2026 afinan el punto. La guía conjunta ACSC/CISA/NSA de 2026 advierte contra el acceso amplio o sin restricciones de agentes, en especial a datos sensibles o sistemas críticos. El SANS AI Security Maturity Model de 2026 aporta el Principle of Least Agency (principio de mínima agencia): el mínimo privilegio pregunta qué acceso necesita una identidad; la mínima agencia pregunta cuánta autonomía, alcance de flujo, uso de herramientas y autoridad de acción debería tener el agente.

Sales sabiendo mapear la frontera de permisos de un agente, distinguir los dos modelos de identidad, aplicar permisos acotados y tokens de capacidad, forzar política antes de la acción, aislar el runtime y responder a incidentes de daño autorizado, con una hoja de ruta de implementación en cuatro fases.

## El problema de la autoridad del agente
Las aplicaciones tradicionales ejecutan flujos conocidos: mapeas el endpoint, validas el parámetro, compruebas el rol. Los agentes rompen esa forma porque interpretan objetivos, construyen planes, recuperan contexto y revisan su conducta tras ver resultados; la ruta exacta puede no existir hasta el runtime. Esa flexibilidad es el valor del producto y también el problema de seguridad.

El modo de fallo central es la autoridad ambiental (ambient authority): el agente tiene acceso amplio disponible en el entorno y lo usa cuando un plan parece requerirlo. Un agente de código con shell, escritura en repositorio, sesión de navegador, token del issue tracker y permisos de CI puede ser muy útil y a la vez tener suficiente autoridad para borrar archivos, exponer secretos o crear un incidente de producción, mientras cada credencial sigue siendo válida. Esto se siente normal durante el desarrollo, pero "no es un modelo de autoridad" (PDF p. 385).

La acción legítima puede seguir siendo dañina: una llamada a herramienta puede ser sintácticamente válida, autenticada y dentro de una allowlist, pero apuntar al repositorio, cliente, factura o entorno equivocados. Por eso el foco es la autoridad, no solo la identidad. Una prueba útil es leer el log de auditoría al revés: cuando el log dice que el agente cambió un registro, debes poder probar qué objetivo llevó a esa acción, qué identidad se usó, qué política lo permitió, qué aprobación lo cubrió y cómo se habría detenido la misma acción contra otro objetivo.

## Dos modos de identidad para agentes
Hay que mantener separados dos modelos:

- Agente de permiso delegado (delegated-permission): actúa a través del acceso de un humano — tokens, sesiones de navegador, archivos locales, shell, derechos de repositorio, cuentas SaaS, rutas de aprobación.
- Identidad no humana (non-human identity): el agente tiene su propia identidad acotada, secretos, roles, rastro de auditoría y ruta de revocación.

Mezclar ambos crea controles descuidados. Un agente que actúa por tu sesión de GitHub no es el mismo riesgo que un build agent con su propio service principal.

### Permisos humanos delegados
Es el patrón de agente moderno más visible. El texto cita ejemplos concretos: Claude Code y Codex CLI operan desde superficies de desarrollador; Claude Cowork lleva el patrón al escritorio y trabajo de conocimiento; GitHub Copilot cloud agent y Devin trabajan contra repositorios y pull requests; OpenClaw muestra otra superficie local de CLI; LangGraph y AutoGPT muestran flujos durables. "The product names will change. The authority pattern will not" (PDF p. 387). El modelo delegado aparece primero en cuatro lugares: máquina de desarrollador, flujo de repositorio, flujo de navegador/SaaS y flujo de operaciones. La acción no es prohibir la delegación, sino dejar de tratarla como cheque en blanco: concede la mínima sesión útil, mantenla visible, pide aprobación antes de acciones de alto impacto y revócala al terminar.

### Identidades de agente no humanas
Se parecen a workload identities, service principals, managed identities, bots y cuentas de automatización. Deben tener dueños explícitos, permisos acotados, credenciales de corta duración cuando sea práctico, rotación, bindings de política, logs y un kill switch. No es mágicamente más segura: una identidad no humana puede volverse superusuario si cada excepción se apila en la misma cuenta. La pregunta de la propiedad importa más de lo esperado: si nadie posee su propósito, nadie nota cuando sus permisos derivan. Las buenas identidades no humanas "son aburridas en el mejor sentido": nombradas por el trabajo, ligadas a entornos, sin login interactivo salvo necesidad, credenciales de corta vida, rotadas y registradas como ellas mismas.

### El fallo de cerebro dividido (split-brain)
Los sistemas más desordenados mezclan ambos modos sin admitirlo. Durante un incidente se descubre que el agente no era una identidad, sino "a braid of identities" (una trenza de identidades). Hay que escribir la trenza: mantener un inventario de autoridad que separe sesiones de usuario delegado de credenciales no humanas, y asegurar que la revocación corte ambas rutas.

## Mapear la frontera de permisos
Antes de asegurar un agente, mapea la frontera donde entra la autoridad y sale la acción. Dibuja el agente como un sistema operativo de decisiones con entrada, memoria, herramientas, credenciales, política, aislamiento de runtime y salida.

La descomposición de frontera identifica dónde corre el agente, a qué accede, cómo actúa y cómo se le puede restringir, monitorizar y revocar:
- Superficie de runtime: terminal, navegador, IDE, chat, workspace cloud, worker de API o escritorio local — cada una cambia el radio de impacto.
- Plano de control: configuración, políticas, enrutado de modelo, memoria, registro de herramientas, reglas de aprobación y fronteras de tenant.
- Plano de acción: comandos de shell, cambios de repo, llamadas SaaS, mensajes, tickets, consultas, pagos, despliegues. Una búsqueda de solo lectura y una ruta de despliegue a producción no deben compartir la misma historia de permisos.
- Identidad: sesión humana delegada, workload identity, bot, service principal, API key o token acotado.
- Frontera de permisos concreta: nombra recursos, verbos, objetivos, presupuestos, ventanas de tiempo y condiciones de aprobación. "Can access GitHub" no es una frontera; "puede abrir PRs en estos repos, no puede hacer merge, no puede modificar secretos y requiere aprobación para cambios de workflow" sí lo es.
- Aislamiento y revocación: acceso a filesystem, contenedores, perfiles de navegador, egress de red, namespaces de memoria, sandboxes; y evidencia de logs, replay de sesión, versiones de política, expiración de credenciales, revocación de tokens, deshabilitado de herramientas y kill switches.

El inventario de autoridad hace preguntas directas (qué identidad está ligada, qué puede leer/cambiar, qué herramientas puede llamar sin pedir, cuáles requieren aprobación, qué secretos alcanza). No debe colapsar en una lista de productos: "GitHub, Slack, Jira, AWS" no es un modelo de autoridad; el modelo son verbos y objetivos.

Contexto y memoria son parte de la frontera. La memoria, documentos recuperados, resultados previos de herramientas e historial no son datos pasivos: moldean el plan. Una instrucción maliciosa en memoria o retrieval puede hacer que el agente use luego herramientas legítimas para seguirla. Esto conecta con los capítulos 7, 10, 14 y 16 (aislamiento de contexto, abuso de herramientas, autorización de aplicación, guardrails). Las fronteras de memoria deben acotarse por tenant, usuario, proyecto, sensibilidad, tiempo y propósito; el retrieval debe exigir autorización de documento antes de que el contenido llegue al modelo; los resultados de herramientas se tratan como entrada no confiable hasta validarlos.

## Permisos acotados y fronteras de capacidad
El mínimo privilegio para agentes debe ser más específico que asignar un rol: acotar por acción, objetivo, duración, clase de dato y estado del flujo. El patrón útil es conceder capacidades, no cuentas amplias.

- Acotar por verbo: read, draft, propose, execute, delete, publish, deploy, send son niveles de riesgo distintos.
- Acotar por objetivo: repositorio, rama, tenant, cliente, cola de tickets, modelo, proyecto cloud, entorno, tabla, ruta de archivo.
- Acotar por tiempo: una credencial que expira tras la tarea es más fácil de razonar que una eterna en un config.
- Límites de conteo y presupuesto: enviar un borrador frente a 10.000; correr tests en sandbox frente a shell arbitrario en el laptop. Los budgets, rate limits y umbrales de gasto son controles de seguridad.

Mínima agencia cuando el modelo parece inofensivo: ejemplo de un agente nacional de gestión inmobiliaria (leasing) que habla con prospectos y residentes por chat, SMS, voz y email. El modelo conversacional no tiene herramientas directas, pero la autoridad vive en un nivel de orquestación que resuelve al usuario y ensambla los registros. "Do not ask who the agent is. Ask what one conversation can cause" (PDF p. 393). La mínima agencia debe aplicarse donde se ensamblan los datos de tenant, acotada a la forma del producto (empresa gestora → comunidad → residente). Los fallos silenciosos son los que validan un identificador estrecho pero un fallback devuelve datos de uno más amplio nunca autorizado: es el fallo legítimo-pero-objetivo-equivocado, una capa por debajo de la llamada a herramienta. El movimiento es ligar la autoridad a la clave de tenant antes de construir el payload, tratando los identificadores como no confiables y rehusando ensamblar campos cross-tenant sin prueba.

Tokens de capacidad: la capacidad estrecha la pregunta de "¿quién es este agente?" a "¿qué acción exacta permite este token?" y puede codificar objeto objetivo, verbo, expiración, estado de aprobación y coste máximo. Se implementa con tokens acotados de corta vida, OAuth delegado, action requests firmados, condiciones IAM, installation tokens de repositorio o service tokens. La propiedad clave: "the credential is narrower than the agent's imagination" (PDF p. 394).

Puertas de aprobación (approval gates): antes de acciones irreversibles o de alto impacto, mostrando acción concreta, objetivo, datos afectados, coste, destinatario, entorno, decisión de política y ruta de rollback. Un "allow tool use" genérico no es consentimiento. La puerta debe ligarse al artefacto generado (mostrar el email, el diff y rama, o el comando, directorio y entorno). Deben tener mayor fricción por defecto: cambiar identidad/acceso/secretos/políticas; ejecutar comandos de shell que modifican estado o red; merge/deploy/publish/enviar/gastar/borrar; leer secretos o datos cross-tenant; crear memoria durable, automatización, jobs o credenciales de larga vida.

## Política forzada antes de la acción
Loguear una llamada peligrosa después de ejecutarla sirve para investigar, pero no es enforcement. La decisión de política debe ocurrir antes de ejecutar: el modelo propone la llamada, la aplicación la evalúa y solo entonces corre la herramienta. "The model should not be the policy authority for its own tool calls. Let it propose. Let policy decide" (PDF p. 395).

Herramientas posibles: OPA, Casbin, IAM cloud, autorización de servidor MCP, servicios de política custom, allowlists por herramienta. Lo que importa es la separación, no la herramienta exacta. La política necesita ver: identidad del agente, identidad del usuario delegado, sesión, tenant, nombre de herramienta, operación, objeto objetivo, parámetros generados, sensibilidad del dato, confianza del modelo o señales de detectores, estado de aprobación, versión de política y acciones previas. Hay que validar los parámetros generados como si fueran entrada hostil (rutas, URLs, SQL, comandos, destinatarios, IDs de cliente, ramas, recursos cloud).

Separa el punto de enforcement (donde correría la llamada: wrapper de shell, servicio de repo, servidor MCP, controlador de navegador, conector SaaS, worker de cola, servicio de despliegue) del punto de decisión. La decisión debe devolver más que allow/deny: permitir, denegar, requerir aprobación, reducir alcance, redactar salida, ejecutar en sandbox o pedir clarificación, para degradar con elegancia.

MCP y servidores de herramientas: MCP estandariza conexiones pero hace más importante la disciplina de autorización. La especificación 2025-11-25 refuerza autorización, uso de herramientas, elicitation y flujos basados en tareas. Los tool servers no deben asumir que toda operación expuesta es segura: hacen falta enforcement del lado servidor, tokens acotados, fronteras de consentimiento, logs y rutas de revocación. Usar MCP como punto de control, no como loophole.

Registro mínimo de llamada a herramienta: identificador de objetivo/tarea; identidad del agente y del usuario delegado; nombre de herramienta, operación, parámetros y objeto objetivo; entrada de política, versión, decisión y razón; registro de aprobación, revisor, timestamp y artefacto aprobado; credencial o capacidad usada; resultado, efectos colaterales, ruta de rollback y acción de seguimiento.

## Aislamiento de runtime y segmentación
El aislamiento es donde los límites de autoridad se vuelven físicos: un runtime que no puede alcanzar directorios padre es más fuerte que una política que lo prohíbe; el control de egress es más fuerte que una regla de "no llamar a internet". Importa porque el host local suele contener secretos, credenciales, código, sesiones de navegador, claves SSH, CLIs cloud y archivos personales.

Por superficie: agentes de terminal necesitan alcance de filesystem, política de comandos, límites de proceso y reglas de red; agentes de navegador necesitan aislamiento de perfil, fronteras de cookies, allowlists de URL y control de descargas; agentes cloud necesitan aislamiento de tenant, fronteras de workspace, compute efímero y acceso acotado a repositorio; agentes SaaS necesitan comprobaciones de permiso a nivel de objeto y auditoría fuerte.

Patrones de segmentación: contenedores, sandboxes, usuarios restringidos, workspaces efímeros, segmentos de red privados y perfiles de navegador estrechos; secretos fuera del workspace salvo necesidad; montar solo los directorios necesarios; preferir solo-lectura hasta la fase de escritura/ejecución. Los agentes locales merecen sospecha especial porque la frontera se difumina fácil. Los agentes cloud tienen el problema de conectar a más sistemas por defecto; la segmentación sigue al flujo, no al organigrama. Los controles de supply-chain del capítulo 17 aplican: una dependencia comprometida puede volver un agente acotado en un puente de ejecución.

Verificación continua y auditoría: no es molestar al usuario cada 30 segundos, sino comprobar si la acción actual aún encaja con identidad, tarea, política, contexto y riesgo. Las señales observables valen más que los trust scores inexplicables: frecuencia de herramientas, sensibilidad del objetivo, cambios de permiso, aprobaciones fallidas, retrieval inusual, categorías de comando, volumen de datos, geografía, tiempo y desvío de la tarea. Vigilar: paso de read→write→execute o draft→publish; acceso a secretos o datos cross-tenant; acciones denegadas repetidas o reformulación de la misma acción; destinos de red/paquetes inusuales; memoria o retrieval que introducen instrucciones o cambian alcance; acciones fuera de la ventana, presupuesto, geografía, entorno, rama o cliente.

## Respuesta a incidentes por daño autorizado del agente
Los incidentes de agente son incómodos porque la primera evidencia puede decir que la acción estaba permitida. La pregunta real es si el sistema permitió al actor correcto, con la autoridad correcta, por la razón correcta, contra el objetivo correcto y con la aprobación correcta. Secuencia de primera respuesta:
- Congelar la sesión o workspace del agente.
- Revocar o expirar tokens delegados, credenciales acotadas, sesiones de navegador y acceso a herramientas del run.
- Deshabilitar temporalmente herramientas de alto riesgo si el fallo de política no está claro.
- Preservar prompts, contexto recuperado, planes, llamadas, registros de aprobación, logs y artefactos.
- Inspeccionar memoria, documentos, resultados de herramientas y repos/tickets en busca de instrucciones inyectadas.
- Reparar la política, puerta de aprobación, frontera de aislamiento o alcance de credencial que permitió el daño.

La trampa de la contención: no contener solo la credencial obvia. La autoridad del agente tiene puertas laterales (sesiones de navegador, tokens locales cacheados, permisos de cola, secretos de webhook, stores de memoria, sesiones de tool server, workspaces temporales). Busca ramas creadas, jobs programados, mensajes borrador, tickets modificados, archivos generados, memorias actualizadas y credenciales nuevas. La revisión debe terminar en un cambio de control (añadir una regla, reducir una credencial, dividir un permiso, aislar un workspace, cambiar un prompt de aprobación, añadir un test de regresión o quitar una herramienta), no en "monitorizar más de cerca".

## Hoja de ruta de implementación
No empieces con una diapositiva grandiosa de programa Zero Trust; empieza inventariando autoridad. Las cuatro fases prácticas:
1. Inventariar autoridad: superficies de runtime, identidades, usuarios delegados, herramientas, credenciales, objetivos y aprobaciones actuales.
2. Acotar permisos: superficies de runtime, límites de tiempo, verbos read/write/execute y workspaces aislados.
3. Forzar política de acción: evaluar llamadas y parámetros generados antes de ejecutar, con puertas de aprobación claras.
4. Monitorizar y ensayar respuesta: recoger evidencia de auditoría, detectar drift, revocar acceso rápido y convertir incidentes en tests de regresión.

Quick wins: quitar tokens humanos de larga vida de la config del agente, separar lectura y escritura, requerir aprobación para acciones irreversibles, restringir shell y filesystem, loguear llamadas con decisiones de política y crear un kill switch que funcione bajo presión. Los programas maduros añaden workload identities, credenciales de corta vida, policy-as-code, runtimes en sandbox y evaluación continua.

Qué pinta tiene lo bueno: un programa sano responde preguntas aburridas rápido — qué agente tocó este objeto, qué identidad usó, qué versión de política lo permitió, qué aprobación vio el humano, qué credencial expira primero, qué switch lo detiene ahora y qué test prueba el control arreglado.

## Lab y recursos
El lab diseña y valida una arquitectura zero trust para NexaBot Enterprise Ops (lee monitoreo, consulta runbooks, ejecuta scripts de remediación aprobados, envía alertas y accede a APIs cloud): mapear el agente al stack, aplicar el Rule of Two framework, diseñar políticas de acceso basadas en capacidad, documentar enforcement points, elegir patrones resistentes a prompt injection y validar contra escenarios del capítulo 10. El Field Artifact es el Agent Authority Passport and Revocation Drill. Materiales en el repo oficial de Packt (Part-3/chapter-18).

## Ideas clave
- El problema no es la autonomía por sí sola, sino que la autonomía opera a través de autoridad real; el fallo clave es tratar la autenticación como permiso para actuar.
- Zero Trust para agentes = cada acción responde seis preguntas: quién actúa, cuya autoridad, qué permiso, qué frontera, qué aprobación y cómo se audita/revoca.
- La autoridad ambiental (ambient authority) es el modo de fallo central; la acción legítima puede ser dañina si apunta al objetivo equivocado.
- Separa identidad delegada e identidad no humana; documenta la "trenza" para que la revocación corte ambas rutas.
- Acota permisos por verbo, objetivo, tiempo y presupuesto; concede capacidades estrechas, no cuentas amplias; usa tokens de capacidad.
- La política se fuerza antes de la acción: el modelo propone, la política decide, separando enforcement point de decision point y devolviendo más que allow/deny.
- El aislamiento de runtime (sandboxes, workspaces efímeros, egress, perfiles de navegador) vuelve físicos los límites; la mínima agencia se aplica donde se ensamblan los datos, no solo donde corre el modelo.
- Ante un incidente, no te detengas en "estaba permitido": congela, revoca, preserva, inspecciona contexto inyectado, cierra puertas laterales y termina en un cambio de control.
