# Attacks on RAG Systems (Ataques a sistemas RAG) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre los sistemas RAG?
R: Un sistema RAG puede comprometerse sin tocar nunca el LLM: basta con contaminar la capa de recuperación de conocimiento que lo alimenta; el anclaje en fuentes crea una nueva superficie de ataque.

P: ¿Qué dos categorías de amenaza distingue el capítulo y qué las diferencia?
R: Envenenamiento deliberado (el atacante crea contenido para manipular las salidas) y contaminación accidental (documentos mal clasificados o enrutados que corrompen la base sin intención); mismo impacto práctico, distintas estrategias defensivas.

P: ¿Cuáles son los componentes de la superficie de ataque de un RAG?
R: Repositorios de origen, pipelines de ingesta, modelos de embedding, vector databases, lógica de recuperación, augmentación de contexto y generación de respuesta.

P: ¿Por qué la persistencia es el gran cambio en los ataques RAG?
R: Un prompt envenenado afecta una sola interacción, pero una fuente RAG envenenada puede afectar a cada usuario que la recupere hasta que el documento se detecte y elimine.

P: ¿Qué diferencia a un adversarial embedding de la indirect prompt injection?
R: El adversarial embedding controla *qué* documento se recupera (la geometría del espacio vectorial); la indirect prompt injection controla *qué hace* el modelo después.

P: ¿Qué es el cluster poisoning?
R: Un ataque que usa volumen en vez de precisión: muchos documentos maliciosos relacionados inundan una región del espacio vectorial para que el top-K incluya repetidamente material del atacante.

P: ¿Por qué los ataques directos a la vector database son más severos?
R: Porque saltan la ingesta; con acceso de escritura se alteran embeddings, metadatos, índices o fronteras de tenant por debajo del monitoreo de la aplicación.

P: ¿En qué consiste la indirect prompt injection a través de RAG?
R: El usuario hace una pregunta normal, el sistema recupera un documento envenenado que entra al prompt como contexto confiable, y el modelo debe decidir si el texto es evidencia a citar o una instrucción a seguir.

P: ¿Por qué los delimitadores no bastan para separar instrucciones de datos?
R: Solo funcionan si los datos no pueden contener el delimitador; hay que neutralizar los valores insertados, no solo rodearlos, porque quien escribe un campo puede cerrar el delimitador y abrir su propio bloque.

P: ¿Por qué la autorización es incómoda en RAG?
R: Porque la similitud vectorial no sabe inherentemente quién pregunta: dos usuarios con la misma consulta reciben los mismos vecinos cercanos salvo que el sistema filtre por identidad, tenant, departamento, rol o permisos.

P: ¿Qué diferencia hay entre filtrado pre-recuperación y post-recuperación?
R: El pre-recuperación es más seguro (los documentos no autorizados nunca entran al espacio de búsqueda) pero aumenta la complejidad del índice; el post-recuperación quita resultados no autorizados antes de la respuesta, pero genera fugas de temporización, cómputo desperdiciado e influencia en el ranking.

P: ¿Cuáles son las capas de la arquitectura defensiva RAG?
R: Source, ingestion, embedding, vector database, retrieval, augmentation, response y monitoreo de toda la ruta; la defensa es un conjunto distribuido, no un único control.

P: ¿Qué defensa práctica se propone frente a los embedding/vector database attacks?
R: Comparación en vez de confianza ciega en un único score de similitud: si un documento puntúa alto en búsqueda vectorial pero flojo en búsqueda léxica, procedencia, clustering o revisión humana, la discordancia es una señal útil.

P: ¿A qué controles y marcos externos se mapean las mitigaciones del capítulo?
R: A OWASP LLM04, LLM08 y LLM05, y a preocupaciones de NIST, MITRE ATLAS, AISVS y la OWASP AI Testing Guide.

## Preguntas de autoevaluación

P: En el escenario de soporte interno de TI, ¿por qué el incidente de las credenciales filtradas ilustra la tesis del capítulo?
R: Porque fue contaminación accidental —un becario subió un documento con credenciales a SharePoint— y no envenenamiento intencional ni compromiso del modelo, pero el resultado práctico fue el mismo: nadie tuvo que comprometer el modelo fundacional para comprometer la respuesta. (Sección: El ejemplo que recorre el capítulo)

P: ¿Por qué RAG difumina las fronteras de confianza y qué implica para la seguridad?
R: Los sistemas tradicionales separan la entrada no confiable de los datos confiables, pero RAG los mezcla intencionadamente para que el modelo razone sobre conocimiento actual o privado; el trabajo de seguridad es preservar esa utilidad haciendo explícitas la autoridad de la fuente, la procedencia, los derechos de acceso y el monitoreo. (Sección: RAG architecture and its attack surface)

P: ¿Qué enseña el caso en que el almacén de grounding es una fila de base de datos y no un índice vectorial?
R: Que la inyección indirecta no es propiedad de la búsqueda vectorial sino de tratar texto almacenado como contexto confiable; los delimitadores solo separan si los datos no pueden contenerlos; y el radio de impacto sigue al campo, no a la petición. (Sección: Retrieval manipulation and indirect prompt injection — caso real)

P: ¿Por qué el monitoreo de los logs de aplicación es insuficiente para un RAG?
R: Porque no revelan si una fuente cambió, si un cluster de embeddings se desplazó o si un documento empezó a rankear para consultas no relacionadas; el monitoreo debe observar todo el pipeline más allá del endpoint del modelo. (Sección: Detection and monitoring)

P: Según el split tipo AISVS, ¿qué distingue los tres niveles de monitoreo?
R: Nivel 1 es logging normal (autenticación de fuente, umbrales de similitud, patrones básicos de consulta); Nivel 2 añade auditoría de recuperación, análisis de distribución de embeddings y alineación de respuesta; Nivel 3 correlaciona etapas, detecta desplazamiento de clusters a escala y establece baselines sobre millones de documentos. (Sección: Detection and monitoring)

P: ¿Por qué no es práctica la seguridad RAG perfecta y cuál es el objetivo realista?
R: Revisar manualmente cada documento y validar cada recuperación vuelve el sistema demasiado lento o costoso; el objetivo es la reducción consciente de riesgo, ajustando la fricción de cada capa al nivel de riesgo del despliegue. (Sección: Trade-offs and practical guidance)

P: ¿Qué cuatro preguntas deben poder responderse durante un incidente RAG?
R: Qué fuente introdujo el contenido malo, qué chunks y embeddings se crearon de él, qué usuarios lo recuperaron y qué respuestas pudieron verse influidas; si el sistema no puede responderlas, no está listo para uso RAG de alta confianza. (Sección: Trade-offs and practical guidance)

P: ¿Qué función cumple la augmentation security en la arquitectura defensiva?
R: Mantener el contenido recuperado visiblemente separado de las instrucciones del sistema y las consultas (delimitadores, prompts estructurados, seguimiento de citas) para que el modelo trate el material como datos y no como comandos. (Sección: Defensive architecture and mitigations)

## Checklist

- Validar el origen de los documentos: de dónde vienen, quién los aprobó y si cambiaron inesperadamente (source security).
- Sanitizar formato oculto, filtrar patrones de ataque conocidos, trocear de forma coherente, rate-limitar fuentes sospechosas y poner en cuarentena contenido a revisar (ingestion security).
- Verificar que los vectores coinciden con el comportamiento semántico esperado (embedding security).
- Restringir escrituras a la vector database, proteger fronteras de tenant, hashear/verificar integridad de embeddings y mantener backups para rollback (vector database security).
- Validar la consulta, aplicar autorización antes o durante la búsqueda, re-rankear con señales de seguridad y evitar que una sola fuente domine el top-K (retrieval security).
- Preferir filtrado pre-recuperación y aislamiento de tenant en sistemas de alto riesgo; hacer explícita la elección arquitectónica de autorización.
- Mantener el contenido recuperado separado de instrucciones del sistema y neutralizar los valores insertados, no solo rodearlos con delimitadores.
- Comprobar alineación respuesta-fuente, citas reales, fuga de datos sensibles y si el modelo siguió una instrucción oculta (response security).
- Monitorear ingesta, embedding/vector database y recuperación/respuesta en busca de anomalías (volumen inusual, Unicode sospechoso, desplazamiento de clusters, saltos de ranking, discordancia respuesta-fuente).
- Conservar telemetría suficiente para responder, durante un incidente, qué fuente, qué chunks/embeddings, qué usuarios y qué respuestas se vieron afectados.
