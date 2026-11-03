# Anatomy of an AI System (Anatomía de un sistema de IA) — Estudio

## Tarjetas de repaso

P: ¿Qué es realmente un sistema de IA en producción, más allá del modelo?
R: Una pila de componentes interactuantes: data pipelines, prompts, sistemas de retrieval, orquestación, APIs, llamadas a herramientas, infraestructura, monitoreo y flujos humanos. La postura de seguridad surge de cómo se conectan todas esas piezas.

P: ¿Por qué aplicar frameworks de seguridad de ML clásico a IA generativa da "false confidence"?
R: Porque se usan controles para sistemas deterministas en sistemas probabilísticos, access controls de APIs estructuradas en interfaces de lenguaje natural y monitoreo estadístico que no detecta ataques semánticos.

P: ¿En qué se diferencia el flujo del ML tradicional del de la IA generativa?
R: El ML tradicional es lineal y determinista (ETL, features predeterminados, entrenamiento batch, salidas como scores o clasificaciones). La IA generativa tiene entradas en lenguaje natural de variación infinita, salidas abiertas y el mismo prompt puede dar respuestas distintas entre invocaciones.

P: ¿Por qué la tokenización es un componente de seguridad y no solo utilitario?
R: Es "el primer lugar donde la entrada externa se encuentra con el modelo"; ahí pueden introducirse anomalías de codificación o secuencias envenenadas, y los desajustes entre tokenización de entrenamiento e inferencia crean vulnerabilidades que saltan filtros.

P: ¿Qué etapas componen el pipeline moderno de entrenamiento?
R: Pretraining (la mayor parte del cómputo), supervised fine-tuning (define instrucciones y "personalidad") y refuerzo con feedback (RLHF, o alternativas como DPO y RLAIF), más fases como Constitutional AI, retrieval-augmented training y tool-use training.

P: ¿Por qué un batch de datos envenenado en pretraining es especialmente peligroso?
R: Porque puede alterar el comportamiento del modelo solo bajo condiciones específicas en producción meses después del run.

P: ¿Qué limitación tiene el API gateway frente a entradas de texto libre?
R: Verifica conteo de tokens, autenticación y rate limiting, pero no detecta de forma fiable un intento de prompt injection: valida tokens y autenticación, no intención.

P: ¿Qué componentes forman la arquitectura RAG?
R: Pipelines de ingesta de documentos, servicios de embedding, vector databases para búsqueda por similitud, servicios de retrieval que consultan y rankean, lógica de construcción de prompt y el modelo que genera a partir del contexto aumentado.

P: ¿Qué es indirect prompt injection en RAG?
R: Cuando un atacante que controla un documento del knowledge base inyecta comandos en el contenido recuperado; si el modelo trata ese contenido como instrucciones (y no como contexto), puede anular el system prompt o exfiltrar datos.

P: ¿Por qué el límite modelo–herramientas es un límite de seguridad real?
R: Porque al invocar una tool el agente cruza del entorno controlado a sistemas externos con efectos en el mundo real; exige autenticación, autorización, validación de entrada y saneamiento de salida.

P: ¿Qué función cumple la capa de orquestación y por qué es crítica?
R: Es el "sistema nervioso" (plantillas, cadenas, memoria, selección de herramientas, output parsers) donde el context engineering se vuelve control de seguridad; suele contener lógica de negocio crítica y sus bugs causan tantos problemas como las fallas del modelo.

P: ¿Cuáles son los trust boundaries primarios de un sistema de IA?
R: Input/instruction boundary (recorre toda la pipeline), límite modelo–herramientas, límite entre sesiones de usuario, más los límites temporales y de estado entre turnos.

P: ¿Qué cuatro capas de memoria/estado de conversación describe el capítulo?
R: Cachés de sesión (turnos recientes), bases de datos de conversación (historial completo), índices de embeddings (búsqueda semántica) y servicios de sincronización de estado, más la memoria a largo plazo.

P: ¿Qué zonas de red usa la segmentación de un sistema de IA?
R: DMZ (gateways externos), aplicación (orquestación y lógica de negocio), modelo (endpoints de inferencia con GPU), datos (vectores, conversaciones, documentos) y gestión (monitoreo, despliegue).

## Preguntas de autoevaluación

P: ¿Cuál es la tesis central del capítulo sobre dónde vive la postura de seguridad de un sistema de IA?
R: Que el límite de confianza rara vez rodea solo al modelo; la seguridad depende de cómo se conectan las piezas (data path, retrieval, herramientas, cuentas de servicio, pasos de aprobación humana), no solo de asegurar el endpoint del modelo. (Lo que necesitas saber)

P: ¿Por qué la validación exhaustiva de los datos de entrenamiento es impracticable y qué mitigaciones parciales se proponen?
R: Porque la data puede alcanzar billones de tokens y petabytes. Mitigaciones: auditorías por muestreo estadístico, provenance tracking, deduplicación automatizada y clasificadores que marcan contenido dañino o envenenado. (El pipeline moderno de entrenamiento → Preparación y curación de datos)

P: ¿Qué papel juegan las plataformas MLOps y dónde está su riesgo?
R: Son la capa de control entre entrenamiento e inferencia (MLflow, Kubeflow, servicios cloud-native); una política mal configurada o un paso de revisión faltante puede dejar llegar a producción un artefacto comprometido. (El pipeline moderno de entrenamiento → Dependencias de infraestructura)

P: ¿Por qué integrar RAG con fuentes como SharePoint, Confluence o Google Drive aumenta la superficie de ataque?
R: Porque añade APIs, autenticación y formatos propios, y los cambios upstream repercuten en el comportamiento de la IA; cada componente de la cadena de retrieval es parte de la superficie de ataque, no solo el modelo. (Patrones de integración → Arquitectura RAG)

P: ¿Qué hace que los trust boundaries de IA sean más difíciles de mapear que los tradicionales?
R: Que cruzan componentes de distintos equipos, runtimes y modelos de autenticación, y que el input/instruction boundary recorre toda la pipeline en vez de rodear solo al modelo. (Límites de confianza e interfaces críticas)

P: En un chatbot de soporte multi-turno, ¿qué protegen el límite entre turnos y el límite entre sesiones?
R: El límite entre turnos evita que el usuario referencie en el turno tres instrucciones inyectadas en el turno uno; el límite entre sesiones evita que los datos personales de un cliente anterior sean visibles al siguiente. (Límites de confianza e interfaces críticas)

P: ¿Por qué un checkpoint manipulado es una amenaza seria en la infraestructura de entrenamiento?
R: Porque es casi indistinguible de uno limpio por inspección y puede extraer datos o alterar el comportamiento; por eso los checkpoints necesitan access controls e integrity verification. (Capas de infraestructura y límites de seguridad → Infraestructura de entrenamiento)

P: ¿Qué da forma a la infraestructura de inferencia y cómo logra el aislamiento multi-tenant?
R: La moldean la latencia y la variabilidad (responder en cientos de milisegundos). El aislamiento usa límites de contenedor con capacidades restringidas, virtualización de GPU con MIG, network policies y cuotas de recursos. (Capas de infraestructura y límites de seguridad → Infraestructura de inferencia)

## Checklist

Puntos a dominar (capítulo teórico):

- Describir las capas de un sistema de IA (training pipelines, integraciones, infraestructura, data flows, trust boundaries, topología en runtime) y por qué el modelo es solo la parte visible.
- Explicar por qué heredar controles deterministas del ML clásico en sistemas probabilísticos produce "false confidence".
- Enumerar las etapas del pipeline de entrenamiento (pretraining, supervised fine-tuning, RLHF/DPO/RLAIF, fases adicionales) y el punto de inyección de cada una, incluida la tokenización.
- Justificar por qué el API gateway no detecta prompt injection pese a gestionar autenticación y rate limiting.
- Trazar la cadena de componentes de RAG y reconocer el contenido recuperado como superficie de ataque (indirect prompt injection).
- Identificar el límite modelo–herramientas y los cuatro controles que exige: autenticación, autorización, validación de entrada y saneamiento de salida.
- Explicar por qué la orquestación concentra lógica de negocio y context engineering, y su impacto en seguridad.
- Mapear los trust boundaries primarios (input/instruction, retrieval, tool, sesión/persistencia) y las zonas de red (DMZ, aplicación, modelo, datos, gestión).
- Saber qué artefactos de mapeo del sistema existen (inventarios de componentes, data-flow maps, trust-boundary maps, catálogos de integración, trazas de runtime, IaC) y para qué sirven en threat modeling e incident response.
