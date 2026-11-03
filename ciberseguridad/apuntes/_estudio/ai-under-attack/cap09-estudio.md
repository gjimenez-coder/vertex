# Agent Architecture and Vulnerabilities (Arquitectura de agentes y vulnerabilidades) — Estudio

## Tarjetas de repaso

P: ¿Cuál es el cambio incómodo que marca este capítulo respecto a un chatbot comprometido?
R: Un chatbot comprometido solo produce texto incorrecto, pero un agente comprometido puede *actuar* a través de una identidad: borrar registros, llamar APIs, modificar código de producción o aprovisionar recursos cloud.

P: ¿A través de qué debe entenderse la arquitectura de agentes, según la tesis central?
R: A través de la *autoridad*: qué identidad usa el agente, qué permisos están en alcance y qué impide que una instrucción plausible se convierta en una acción autorizada.

P: ¿Qué dos tipos de autoridad distingue el capítulo?
R: Autoridad *delegada* (sesión de navegador, repositorio, token SaaS de un humano) y autoridad de una *identidad no humana* (cuenta bot, service principal, workload identity, token de CI).

P: ¿Qué es la *capacidad* (capability) en el contexto de un agente?
R: El mecanismo que convierte un objetivo manipulado en daño; siempre se adhiere a una identidad. A más capacidades (ejecución de código, escritura en BD, email, cloud), más daño desde un único falso objetivo aceptado.

P: ¿Por qué la *persistencia* agrava el problema de seguridad de los agentes?
R: Los agentes recuerdan objetivos, planes, historial y fuentes confiables entre sesiones; un objetivo inyectado o una memoria envenenada puede quedar latente y dispararse después, dando lugar a ataques que se despliegan en horas o días.

P: ¿Cuáles son los cuatro handoffs (traspasos) críticos donde se concentran los ataques?
R: Entre entradas del usuario e instrucciones del agente; entre el agente y las herramientas conectadas; entre el agente y la memoria; y entre distintos agentes.

P: ¿Qué problema clásico reaparece en el handoff agente→herramienta?
R: El problema del *confused deputy*, con un LLM en medio: el atacante no accede a la base de datos, pero el agente sí, y una exportación masiva enmarcada como reporte de auditoría sale desde una cuenta de servicio confiable.

P: ¿Por qué es peligroso el *tool chaining*?
R: Porque cada paso individual (buscar, leer, generar, ejecutar) parece inocente; el ataque está en la secuencia, no en una acción aislada.

P: ¿Qué muestra la PoC *Morris II* (Nassi et al.)?
R: Cómo prompts autorreplicantes propagan instrucciones maliciosas en sistemas que recuperan, resumen, envían email y delegan, aprovechando que los mensajes entre agentes reciben más confianza que la entrada del usuario.

P: ¿Cuáles son las cinco clases recurrentes de vulnerabilidad?
R: Ejecución insegura de herramientas y escalación de privilegios; prompt injection; manejo con fugas o inseguro de salida; riesgos de persistencia de memoria y datos; y credenciales demasiado amplias y de larga vida.

P: ¿A qué entrada de OWASP corresponde la ejecución insegura de herramientas y escalación de privilegios, y por qué destaca?
R: A *OWASP LLM06: Excessive Agency*; es la clase de mayor riesgo. Señales: privilegios elevados, llamadas de sistema inusuales, acceso a archivos fuera de directorios designados, conexiones de red inesperadas.

P: ¿Cuál es el patrón seguro de credenciales que propone el capítulo?
R: Acceso estrecho, de corta vida y auditable, atado a una acción específica, con dueño, propósito, aprobación, rotación y revocación.

P: ¿Cuáles son las cuatro capas del análisis de amenazas y su accesibilidad relativa?
R: Infraestructura y modelo/memoria exigen más acceso y habilidad; orquestación e interfaz son más accesibles y, por tanto, más comunes en incidentes reales.

P: ¿Qué decide la capa de orquestación y herramientas y qué ataques aterrizan ahí?
R: Decide qué herramientas llamar, en qué orden, con qué parámetros y cuándo termina la tarea; recibe manipulación de selección de herramientas, ataques de ordenamiento (saltar autorización) y parameter injection (SQL, rutas, comandos).

P: Según el capítulo, ¿existe un perímetro limpio que defender?
R: No; prevenir toda explotación es probablemente imposible. Las defensas prácticas son bloquear entradas no confiables, restringir herramientas, validar parámetros, aislar memoria, acotar credenciales, mapear rutas de autoridad y monitorizar secuencias de acción.

## Preguntas de autoevaluación

P: En el ejemplo del agente de codificación, ¿por qué el ataque no se detecta y qué ruta explota?
R: Explota la *ruta de autoridad* del agente, no el modelo aislado: la instrucción oculta llega por un canal que el agente procesa, la escritura en el repositorio es legítima porque el desarrollador la aprobó, los tests pasan porque no validan la configuración TLS y el PR se ve como uno normal, no como un jailbreak. (El ejemplo que recorre el capítulo, PDF p. 229)

P: ¿Por qué el handoff entre entradas del usuario e instrucciones del agente es el límite más accesible, y cómo se formula el peligro?
R: Porque toda técnica de prompt injection del capítulo 6 puede influir en la formación de objetivos, planificación, selección de herramientas e identidad/sesión, incluso vía documentos subidos, páginas recuperadas o contexto multi-turno. El peligro no es una frase mágica, sino la disposición del agente a convertir el lenguaje en un objetivo (PDF p. 233). (Los cuatro handoffs críticos)

P: ¿Cómo sube de gravedad el envenenamiento de memoria o de la base de datos vectorial en un agente respecto a un chatbot?
R: Porque aquí la memoria o el procedimiento envenenado impulsa *acciones*, no solo respuestas: un documento de procedimiento envenenado hace que el agente siga un procedimiento malicioso (p. ej., enviar notas de casos a un endpoint de analítica que en realidad exfiltra datos). (Riesgos de persistencia de memoria y datos / Análisis de amenazas por capas — Modelo y memoria)

P: ¿Qué diferencia hay entre el modelo delegado y el no humano en cuanto a credenciales, y qué señales de abuso cita el capítulo?
R: En el delegado el agente toma prestada la sesión/token de un humano; en el no humano tiene su propia credencial bot/service principal/CI. Señales: uso fuera de horario, redes inesperadas, credencial reusada en servicios no relacionados, sesiones humanas usadas a velocidad de máquina y tokens de larga vida válidos tras terminar la tarea. (Credenciales demasiado amplias y de larga vida)

P: ¿Qué expone un agente cuando falla el manejo de salida y cuál es la defensa recomendada?
R: Puede exponer fragmentos del system prompt, rutas, consultas, endpoints, credenciales, claves y trazas de razonamiento (p. ej., transmitiendo resultados intermedios o salida de debug en producción). La defensa exige output filtering, redacción, separación de trazas y diseño de mínima divulgación. (Manejo de salida con fugas o inseguro)

P: ¿Por qué conviene priorizar la atención defensiva en las capas de interfaz y orquestación?
R: Porque son más accesibles que infraestructura y modelo —exigen menos acceso y habilidad— y por eso son más comunes en incidentes reales; la interfaz es la capa más fácil de alcanzar (autenticación débil, sesiones, validación de entrada, uploads inseguros, errores verbosos, endpoints de debug). (Análisis de amenazas por capas / Ideas clave)

P: ¿Cómo opera un ataque en el handoff entre distintos agentes?
R: Los mensajes entre pares suelen recibir más confianza que la entrada directa del usuario, de modo que un agente de enrutamiento manipulado puede pasar una instrucción envenenada a un agente de facturación como si fuera una escalación autorizada. (Los cuatro handoffs críticos)

## Puntos a dominar

- Explicar por qué la seguridad de un agente se analiza por su ruta de autoridad: identidad usada, permisos en alcance y qué frena que una instrucción plausible se vuelva acción autorizada.
- Distinguir autoridad delegada frente a identidad no humana y relacionar cada una con su patrón de abuso de credenciales.
- Enumerar los cuatro handoffs críticos y dar un ejemplo de ataque en cada uno.
- Nombrar las cinco clases de vulnerabilidad y su mapeo a OWASP Top 10 for LLM Applications (p. ej., LLM06 Excessive Agency, LLM01:2025 Prompt Injection) y MITRE ATLAS.
- Explicar los conceptos de *capability*, *persistencia*, *confused deputy* y *tool chaining* y por qué cada paso parece inocente mientras la secuencia es el ataque.
- Ordenar las cuatro capas (infraestructura, modelo y memoria, orquestación y herramientas, interfaz) por accesibilidad y asociar amenazas representativas a cada una.
- Reconocer que no hay perímetro limpio y listar las defensas prácticas: bloquear entradas no confiables, restringir herramientas, validar parámetros, aislar memoria, acotar credenciales, mapear rutas de autoridad y monitorizar secuencias de acción.
