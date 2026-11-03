# Memory, Context, and State Abuse (Abuso de memoria, contexto y estado) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre la memoria en sistemas de IA?
R: Que la memoria debe tratarse como parte de la frontera de seguridad: si el contexto recordado puede cambiar lo que el modelo cree, permite, recupera o rechaza, merece la misma atención de diseño que la identidad, la autorización, el registro y el almacenamiento de datos.

P: ¿Qué diferencia hay entre un sistema *stateless* y uno *stateful* frente a estos ataques?
R: En uno *stateless* el ataque debe funcionar en el momento; en uno *stateful* el atacante planta contexto inofensivo, lo refuerza turno a turno y vuelve después, cuando el modelo trata el montaje como historial legítimo. La superficie de ataque pasa de un prompt a una trayectoria.

P: ¿Cuáles son las tres categorías de ataques de memoria que presenta el capítulo?
R: A nivel de sesión (*session-level*), de persistencia entre sesiones (*cross-session persistence*) y de contaminación entre usuarios (*cross-user contamination*).

P: ¿Qué es el *context poisoning*?
R: Plantar un hecho falso temprano y confiar en que el modelo lo reutilice, porque los modelos tratan el historial como evidencia útil; el objetivo es hacer la premisa falsa suficientemente aburrida para que el modelo la arrastre.

P: ¿En qué consiste la *history manipulation*?
R: Afirmar que el modelo ya concedió permiso, vio evidencia o aceptó un rol; el manejo débil del estado conversacional hace que el modelo resuelva la incertidumbre a favor de la coherencia conversacional.

P: ¿Qué es el *long-term memory poisoning*?
R: Almacenar supuestos falsos (una preferencia, un rol de proyecto, una instrucción permanente) que sesiones futuras reutilizan, de modo que la memoria falsa se vuelve parte del *baseline* futuro del sistema.

P: ¿Qué es un "authorization smell" según el capítulo?
R: El resultado de la *profile manipulation*: condicionar al sistema a tratar al atacante como administrador, desarrollador, auditor o investigador de seguridad sin verificar el rol externamente.

P: ¿Qué principio de aislamiento resume la defensa frente a la contaminación entre usuarios?
R: Que si un usuario no puede leer los archivos de otro, su memoria tampoco debería poder moldear la salida del modelo de otro usuario.

P: ¿Qué es la *temporal obfuscation* (ofuscación temporal)?
R: Que una sola petición sospechosa se bloquea, pero un patrón repartido en muchas interacciones inofensivas es difícil de reconocer; el defensor debe conectar eventos a través del tiempo, usuarios, operaciones de memoria y contenido recuperado.

P: ¿Qué es la *state explosion* (explosión de estado)?
R: Al combinar contexto de sesión, perfiles, memoria organizacional, cómputos en caché y salidas de herramientas, el número de interacciones posibles crece rápido y los bugs aparecen en las fronteras.

P: ¿Cuáles son los tres controles de la arquitectura de memoria defensiva?
R: Fronteras de sesión (*session boundaries*), particionamiento usuario/tenant (*user / tenant partitioning*) y *memory tiering*, cerrados por la validación de estado.

P: ¿Qué significa la validación de estado y el *fail closed* en la memoria?
R: Comprobar integridad antes de usar el contexto, fallar en cerrado ante memoria sospechosa o inconsistente y ofrecer mecanismos de reset; además, hacer la memoria explícita (qué se recordó, por qué, quién puede usarlo, cuándo expira).

P: ¿Qué es el *cache poisoning* en la contaminación entre usuarios?
R: La versión silenciosa del ataque: se cachean embeddings, completions, pasajes recuperados y salidas de herramientas; si las claves son demasiado amplias, el atacante envenena un resultado que luego parece una optimización de rendimiento.

P: ¿Qué es el *trajectory analysis* en la respuesta a incidentes?
R: Reconstruir cómo se desarrolló el compromiso: la primera premisa falsa, los turnos que la reforzaron, las recuperaciones que la trajeron de vuelta y el momento en que el contexto envenenado cambió la respuesta.

## Preguntas de autoevaluación

P: ¿Por qué el ataque del caso hilo conductor funcionó pese a pasar todas las validaciones de forma aislada?
R: Porque funcionó por paciencia y no por ingeniería de prompts inteligente: el atacante construyó durante cinco sesiones un perfil de contexto que el asistente acabó tratando como continuación natural de una relación establecida. (Sección: El ejemplo que recorre el capítulo)

P: ¿Por qué el filtrado por mensaje no basta para defender a nivel de sesión?
R: Porque los ataques de sesión se construyen a lo largo de la conversación; las buenas defensas mantienen un registro separado de las afirmaciones de seguridad y verifican roles, aprobaciones o autorizaciones contra una fuente de confianza en lugar de dejar que el modelo las infiera del chat crudo. (Sección: Ataques a nivel de sesión)

P: ¿Cuál es la distinción crítica entre un ataque de sesión y uno entre sesiones?
R: La persistencia: un ataque de sesión muere al cerrar la sesión, mientras que uno entre sesiones espera y reaparece en interacciones futuras, por lo que exige validación de memoria, retención acotada y controles de reset visibles. (Sección: Ataques de persistencia entre sesiones)

P: ¿Por qué el error que permite la contaminación entre usuarios suele ser arquitectónico y no conversacional?
R: Porque el sistema almacena la memoria en la frontera equivocada (nota de equipo, caché de tenant, *namespace* vectorial compartido, workspace de agente colaborativo); el control es aislamiento y contexto controlado, no *prompting* ingenioso. (Sección: Contaminación entre usuarios)

P: Según el capítulo, ¿cuándo puede ser el diseño *stateless* la mejor decisión de seguridad?
R: Con documentos sensibles, datos regulados, acciones financieras, contexto médico o flujos internos de alto riesgo; muchos sistemas no deberían tener memoria persistente. (Sección: Por qué la memoria dificulta la defensa)

P: ¿Por qué los controles de borrado y reset deben cubrir cada fuente de contexto?
R: Porque la memoria moderna puede nutrirse de chats pasados, archivos subidos, apps conectadas, contenido recuperado y salidas de herramientas en caché, y cualquiera de esas fuentes puede reintroducir el mismo contexto. (Sección: El problema de la estatalidad)

P: ¿Qué deben cubrir los *audit logs* para detectar abuso de memoria y qué señales de anomalía son útiles?
R: Deben registrar operaciones de memoria además de mensajes (store, retrieve, update, delete, reset, acceso mediado por herramientas); señales útiles son el crecimiento inusual de memoria, contexto viejo que de pronto se activa, varios usuarios con memorias envenenadas similares, o hechos almacenados que contradicen registros confiables. (Sección: Ciencia forense de memoria y respuesta a incidentes)

P: ¿Cuál es el espectro de opciones de respuesta ante contaminación de memoria?
R: Cuarentena de estado (*state quarantine*), amnesia selectiva (*selective amnesia*), reset total de contexto (*full context reset*) y notificación al usuario (*user notification*). (Sección: Ciencia forense de memoria y respuesta a incidentes)

## Puntos a dominar

- Explicar por qué la memoria convierte la seguridad de IA en un problema temporal y cómo el prompt se transforma en una trayectoria.
- Clasificar un ataque dado como de sesión, de persistencia entre sesiones o de contaminación entre usuarios, y nombrar sus patrones.
- Distinguir los cuatro patrones de sesión: *gradual trust building*, *context poisoning*, *conversation hijacking*, *history manipulation*.
- Distinguir los patrones entre sesiones: *long-term memory poisoning*, *profile manipulation*, *knowledge-base contamination*.
- Distinguir los mecanismos entre usuarios: *shared context leakage*, *model-level state pollution*, *cache poisoning*, *agent-to-agent propagation*.
- Argumentar cuándo no implementar memoria persistente y qué principios aplicar cuando sí se justifica (recordar menos, retener menos tiempo, alcances estrechos, controles de reset).
- Describir los cuatro pilares de la arquitectura defensiva: *session boundaries*, particionamiento usuario/tenant, *memory tiering* y validación de estado con *fail closed*.
- Reconstruir un incidente mediante *trajectory analysis* y elegir la respuesta adecuada del espectro de remediación.
