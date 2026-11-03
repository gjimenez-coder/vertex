# Securing AI Agents with Zero Trust Architecture (Asegurar agentes de IA con arquitectura Zero Trust) — Estudio

## Tarjetas de repaso

P: ¿Cuál es el fallo central que el capítulo atribuye a la seguridad de agentes?
R: Tratar "la autenticación como permiso para actuar", es decir, confundir identidad con autoridad para causar efectos.

P: ¿En qué consiste el desplazamiento de foco que propone la tesis del capítulo?
R: Pasar de la identidad a la autoridad: no preguntar si el agente es de confianza, sino qué puede causar, bajo qué autoridad y con qué rapidez se le puede detener.

P: ¿Cuáles son las seis preguntas que debe responder cada acción relevante de un agente bajo Zero Trust?
R: Quién o qué actúa, cuya autoridad se usa, qué permiso está en alcance, qué frontera de herramienta o dato se toca, qué aprobación se requiere y cómo se audita o revoca.

P: ¿Qué es la autoridad ambiental (ambient authority) y por qué es el modo de fallo central?
R: Es el acceso amplio disponible en el entorno que el agente usa cuando un plan parece requerirlo; no es un modelo de autoridad y permite daño aunque cada credencial siga siendo válida.

P: ¿Qué significa que "la acción legítima puede ser dañina"?
R: Una llamada puede ser sintácticamente válida, autenticada y dentro de una allowlist, pero apuntar al repositorio, cliente, factura o entorno equivocados.

P: ¿Cuáles son los dos modelos de identidad de agente que deben mantenerse separados?
R: Agente de permiso delegado (actúa a través del acceso de un humano) e identidad no humana (identidad propia acotada, con secretos, roles, auditoría y revocación).

P: ¿Qué es el fallo de cerebro dividido (split-brain) y cómo se mitiga?
R: Mezclar ambos modos de identidad sin admitirlo, formando "una trenza de identidades"; se mitiga con un inventario de autoridad que separe sesiones delegadas de credenciales no humanas y asegure que la revocación corte ambas rutas.

P: ¿Qué es el Principle of Least Agency (principio de mínima agencia) del SANS AI Security Maturity Model 2026?
R: Frente al mínimo privilegio (qué acceso necesita una identidad), pregunta cuánta autonomía, alcance de flujo, uso de herramientas y autoridad de acción debería tener el agente.

P: ¿Según qué dimensiones deben acotarse los permisos de un agente?
R: Por verbo, por objetivo, por tiempo y por límites de conteo y presupuesto (budgets, rate limits, umbrales de gasto son controles de seguridad).

P: ¿Qué es un token de capacidad y qué propiedad clave tiene?
R: Un token acotado y de corta vida que codifica objeto objetivo, verbo, expiración, estado de aprobación y coste máximo; la propiedad clave es que "the credential is narrower than the agent's imagination".

P: ¿Por qué un "allow tool use" genérico no cuenta como una puerta de aprobación válida?
R: Porque el consentimiento debe ligarse al artefacto concreto (el email, el diff y rama, o el comando, directorio y entorno), mostrando acción, objetivo, datos, coste, destinatario y rollback.

P: ¿Cuál es la regla de la política forzada antes de la acción?
R: El modelo propone, la política decide: la decisión de política ocurre antes de ejecutar y el modelo no debe ser la autoridad de política de sus propias llamadas.

P: ¿Por qué la decisión de política debe devolver más que allow/deny?
R: Para degradar con elegancia: puede permitir, denegar, requerir aprobación, reducir alcance, redactar salida, ejecutar en sandbox o pedir clarificación.

P: ¿Por qué el aislamiento de runtime es más fuerte que una regla de política equivalente?
R: Porque vuelve físicos los límites: un runtime que no puede alcanzar directorios padre o cuyo egress está controlado es más fuerte que una política que solo lo prohíbe.

P: ¿Por qué un incidente de agente no termina con "estaba permitido"?
R: Porque la pregunta real es si se permitió al actor correcto, con la autoridad correcta, por la razón correcta, contra el objetivo correcto y con la aprobación correcta; debe terminar en un cambio de control.

## Preguntas de autoevaluación

P: ¿Por qué los agentes rompen el modelo de seguridad de las aplicaciones tradicionales?
R: Porque interpretan objetivos, construyen planes, recuperan contexto y revisan su conducta tras ver resultados, de modo que la ruta exacta puede no existir hasta el runtime; esa flexibilidad es el valor del producto y el problema de seguridad. (Sección "El problema de la autoridad del agente")

P: ¿Qué prueba propone el capítulo para validar un modelo de autoridad usando los logs?
R: Leer el log de auditoría al revés: ante un cambio de registro, debes poder probar qué objetivo llevó a la acción, qué identidad se usó, qué política lo permitió, qué aprobación lo cubrió y cómo se habría detenido contra otro objetivo. (Sección "El problema de la autoridad del agente")

P: ¿Por qué el contexto y la memoria forman parte de la frontera de permisos?
R: Porque memoria, documentos recuperados, resultados previos e historial moldean el plan; una instrucción maliciosa en memoria o retrieval puede hacer que el agente use luego herramientas legítimas para seguirla. (Sección "Mapear la frontera de permisos")

P: En el ejemplo del agente de gestión inmobiliaria, ¿dónde reside realmente la autoridad y qué fallo hay que evitar?
R: La autoridad vive en el nivel de orquestación que resuelve al usuario y ensambla registros; hay que evitar el fallo silencioso donde se valida un identificador estrecho pero un fallback devuelve datos de uno más amplio nunca autorizado, ligando la autoridad a la clave de tenant antes de construir el payload. (Sección "Permisos acotados y fronteras de capacidad")

P: ¿Qué papel juega MCP en el enforcement de política y cómo debe usarse?
R: MCP estandariza conexiones pero hace más importante la disciplina de autorización; debe usarse como punto de control, no como loophole, con enforcement del lado servidor, tokens acotados, fronteras de consentimiento, logs y rutas de revocación. (Sección "Política forzada antes de la acción")

P: ¿Qué es la "trampa de la contención" en la respuesta a incidentes?
R: Contener solo la credencial obvia; la autoridad del agente tiene puertas laterales (sesiones de navegador, tokens locales cacheados, permisos de cola, secretos de webhook, stores de memoria, sesiones de tool server, workspaces temporales) que también deben cerrarse. (Sección "Respuesta a incidentes por daño autorizado del agente")

P: ¿Cuáles son las cuatro fases de la hoja de ruta de implementación?
R: 1) Inventariar autoridad; 2) Acotar permisos; 3) Forzar política de acción antes de ejecutar; 4) Monitorizar y ensayar respuesta, convirtiendo incidentes en tests de regresión. (Sección "Hoja de ruta de implementación")

P: ¿Qué advierte la guía conjunta ACSC/CISA/NSA de 2026 sobre los agentes?
R: Advierte contra el acceso amplio o sin restricciones de agentes, en especial a datos sensibles o sistemas críticos. (Sección "Lo que necesitas saber")

## Checklist

- [ ] Inventariar la autoridad del agente: superficies de runtime, identidades, usuarios delegados, herramientas, credenciales, objetivos y aprobaciones actuales.
- [ ] Separar las identidades delegadas de las no humanas y documentar la "trenza" para que la revocación corte ambas rutas.
- [ ] Mapear la frontera de permisos nombrando recursos, verbos, objetivos, presupuestos, ventanas de tiempo y condiciones de aprobación (no listas de productos).
- [ ] Acotar permisos por verbo, objetivo, tiempo y presupuesto; conceder capacidades estrechas en lugar de cuentas amplias.
- [ ] Quitar tokens humanos de larga vida de la config del agente y usar credenciales de corta vida o tokens de capacidad.
- [ ] Separar lectura y escritura; preferir solo-lectura hasta la fase de escritura/ejecución.
- [ ] Ligar la autoridad a la clave de tenant antes de construir el payload y rehusar ensamblar campos cross-tenant sin prueba.
- [ ] Forzar la política antes de la acción (modelo propone, política decide), separando enforcement point de decision point.
- [ ] Validar los parámetros generados como entrada hostil (rutas, URLs, SQL, comandos, destinatarios, IDs, ramas, recursos cloud).
- [ ] Configurar puertas de aprobación ligadas al artefacto concreto para acciones irreversibles o de alto impacto.
- [ ] Aislar el runtime: contenedores, sandboxes, usuarios restringidos, workspaces efímeros, control de egress, perfiles de navegador estrechos; montar solo lo necesario.
- [ ] Registrar cada llamada a herramienta con objetivo, identidades, operación, parámetros, decisión y versión de política, aprobación, credencial usada, resultado y ruta de rollback.
- [ ] Implementar verificación continua vigilando read→write→execute, acceso cross-tenant, aprobaciones fallidas, retrieval inusual y desvíos de tarea, presupuesto, geografía o entorno.
- [ ] Preparar y ensayar la respuesta a incidentes: congelar sesión, revocar/expirar credenciales, deshabilitar herramientas de alto riesgo, preservar evidencia, inspeccionar contexto inyectado y cerrar puertas laterales.
- [ ] Disponer de un kill switch que funcione bajo presión y terminar cada incidente en un cambio de control (no en "monitorizar más de cerca").
