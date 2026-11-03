# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 8 — Attacks on RAG Systems (Ataques a sistemas RAG)

> Nota de extracción: el texto se extrajo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo demuestra que un sistema RAG (Retrieval-Augmented Generation) puede comprometerse sin tocar nunca el modelo de lenguaje: basta con contaminar la capa de recuperación de conocimiento que lo alimenta. La arquitectura RAG prometía resolver las alucinaciones anclando las salidas en fuentes autorizadas, pero ese anclaje crea una nueva superficie de ataque que va desde las fuentes documentales, pasando por la generación de embeddings, hasta la recuperación y la augmentación del contexto. Cada componente introduce vulnerabilidades que los controles tradicionales de seguridad de LLM pasan por alto.

La tesis central es que el modelo ya no responde solo desde sus datos de entrenamiento o desde el prompt de un usuario, sino desde una canalización (pipeline) de conocimiento que puede ser contaminada, envenenada, re-rankeada, filtrada o mal atribuida. El atacante que no puede saltarse las defensas a nivel de prompt simplemente va aguas arriba y corrompe la base de conocimiento para que el sistema recupere contenido malicioso como si fuera información legítima de la organización. El modelo nunca se da cuenta porque esas instrucciones llegan por el mismo mecanismo de recuperación confiable que entrega las políticas genuinas.

El capítulo aborda dos categorías de amenaza con estrategias defensivas distintas: envenenamiento deliberado (el atacante crea contenido para manipular las salidas) y contaminación accidental (documentos mal clasificados o mal enrutados corrompen la base sin intención). Sales sabiendo cómo fluye un ataque por el pipeline RAG, por qué su impacto persiste y escala a cada usuario, y qué controles distribuidos reducen el daño sin matar la utilidad que hizo atractiva la arquitectura.

El capítulo sigue el pipeline RAG desde los documentos de origen hasta la recuperación, augmentación, monitoreo y defensa. La pregunta práctica no es si RAG puede hacerse perfectamente seguro, sino dónde el sistema confía en el conocimiento recuperado, cómo se abusa de esa confianza y qué controles reducen el daño.

## El ejemplo que recorre el capítulo
El escenario de soporte interno de TI: una organización desplegó un RAG que indexa 10.000 documentos de SharePoint para responder consultas de empleados. Una auditoría descubre que durante tres semanas el chatbot entregó credenciales de una base de datos de staging interna. Nadie inyectó un prompt ni rompió controles de acceso: un becario con acceso a SharePoint subió un documento titulado "Development Environment Access Guide" con esas credenciales mezcladas con instrucciones legítimas. El vector database lo indexó con normalidad y, en ~400 consultas, expuso las credenciales a decenas de empleados no autorizados.

El punto clave es que fue contaminación accidental, no envenenamiento intencional, y el resultado práctico fue el mismo. El caso ilustra la tesis: "nadie tiene que comprometer el modelo fundacional para comprometer la respuesta" (PDF p. 213).

## RAG architecture and its attack surface
Un sistema RAG crea una frontera de seguridad cada vez que convierte material externo en contexto del modelo. Forman parte de la superficie de ataque: repositorios de origen, pipelines de ingesta, modelos de embedding, vector databases, lógica de recuperación, augmentación de contexto y generación de respuesta. El modelo es el componente visible, pero la canalización de conocimiento es donde comienzan muchos ataques duraderos.

El flujo: documentos (SharePoint, Confluence, tickets, documentación, feeds, webs) → chunked → embedded → almacenados → recuperados → insertados en un prompt → usados para generar la respuesta. Cada paso introduce un modo de fallo distinto: un documento de origen envenenado se vuelve contexto confiable; un chunk malicioso puede caer cerca de una consulta objetivo en el espacio vectorial; una señal de ranking puede arrastrar material controlado por el atacante al top-K.

RAG difumina las fronteras de confianza: los sistemas tradicionales separan la entrada no confiable de los datos confiables; RAG los mezcla intencionadamente para que el modelo razone sobre conocimiento actual, privado o especializado. El trabajo de seguridad es preservar esa utilidad haciendo explícitas la autoridad de la fuente, la procedencia, los derechos de acceso y el monitoreo.

## Document source poisoning
Los ataques RAG más efectivos suelen empezar antes de la recuperación. Si el atacante cambia lo que entra a la base de conocimiento, los controles posteriores heredan una premisa corrupta. Puede ser deliberado (subir contenido malicioso) o accidental (material obsoleto o mal clasificado que se vuelve más autoritativo de lo que merece).

- Compromiso directo de la fuente: repositorios internos (SharePoint, Confluence, Google Drive, wikis). Un usuario con acceso de escritura legítimo añade instrucciones ocultas o políticas engañosas. El humano ve una página normal; la ingesta ve texto, lo trocea y lo embebe.
- Envenenamiento de fuentes externas: crawlers dirigidos hacia material controlado por el atacante mediante manipulación tipo SEO, dominios de documentación falsos, hilos de soporte envenenados y feeds de terceros comprometidos.
- Contenido generado por usuarios (tickets, reseñas, transcripciones, foros): filtrar demasiado destruye contexto útil; filtrar demasiado poco convierte la base en superficie de ataque persistente.

La idea central es la persistencia: "Un prompt envenenado afecta una interacción. Una fuente RAG envenenada puede afectar a cada usuario" (PDF p. 214) hasta que se encuentre y elimine el documento. Trata el índice RAG como infraestructura afectada que necesita contención, forense y recuperación.

## Embedding and vector database attacks
Explotan la brecha entre el significado tal como lo lee un humano y como lo mide el sistema de recuperación. Una vector database no almacena prosa sino representaciones matemáticas y devuelve documentos cuyos vectores se parecen al vector de la consulta; eso da al atacante un nuevo objetivo: la geometría de la recuperación.

- Adversarial embeddings: documentos diseñados para caer cerca de consultas objetivo aunque un revisor humano no los consideraría buenas respuestas. Controla *qué* documento se recupera (distinto de la indirect prompt injection, que controla *qué hace* el modelo después).
- Cluster poisoning: usa volumen en vez de precisión; muchos documentos maliciosos relacionados inundan una región del espacio vectorial para que el top-K incluya repetidamente material del atacante.
- Ataques directos a la vector database: más severos porque saltan la ingesta; con acceso de escritura se alteran embeddings, metadatos, índices o fronteras de tenant por debajo del monitoreo de la aplicación.
- Peculiaridades del modelo de embedding: homoglifos Unicode, artefactos de formato, frases multilingües, code-switching y tokenización específica del modelo afectan la recuperación.

Defensa práctica: comparación, no confianza ciega en un único score de similitud. Si un documento puntúa alto en búsqueda vectorial pero flojo en búsqueda léxica, procedencia, clustering de tópicos o revisión humana, la discordancia es una señal útil.

## Retrieval manipulation and indirect prompt injection
Apunta al pipeline de ranking que decide qué documentos entran al prompt (búsqueda híbrida, expansión de consulta, corrección ortográfica, boosts por metadatos, ponderación por recencia, re-ranking, señales de calidad de fuente).

- Manipulación de ranking: tácticas tipo SEO (keyword stuffing, relleno de términos raros, manipulación de títulos/metadatos, frases que coinciden con consultas comunes).
- Ataques de comprensión de consulta: explotan la ambigüedad (términos polisémicos, sinónimos que usan los empleados, patrones de typo que el sistema "corrige" hacia el resultado preferido del atacante).
- Indirect prompt injection a través de RAG: el usuario hace una pregunta normal, el sistema recupera un documento envenenado, este entra al prompt augmentado como contexto confiable y el modelo debe decidir si el texto es evidencia a citar o una instrucción a seguir. La instrucción maliciosa llega por la propia ruta de conocimiento confiable del sistema.

Variantes: invisible instructions (ocultas en estructura de PDF, CSS, comentarios, formato, texto fuera de página); context-triggered attacks (se activan solo para ciertos roles, consultas, fechas o departamentos); multi-document attacks (payload repartido entre varios documentos); citation manipulation (afirmaciones falsas envueltas en títulos y metadatos de aspecto legítimo).

### Caso real: cuando el almacén de grounding es una fila de base de datos, no un índice vectorial
El mismo ataque funciona sin vector store. El patrón es más amplio: siempre que texto libre escrito por un actor se concatena en un prompt como contexto confiable, el material recuperado puede llevar instrucciones en vez de evidencia. Una plataforma de gobernanza de IA construía el prompt de un modelo evaluador uniendo una política de disco, hechos del sistema desde su propia base de datos, y una nota de texto libre; usaba delimitadores etiquetados para separar bloques. El fallo: los delimitadores son texto plano dentro de los datos y nada los eliminaba de los valores insertados. Quien podía escribir un campo de texto libre podía cerrar el delimitador y abrir su propio bloque de instrucción. Como los mismos campos alimentaban al modelo de scoring y a un asistente de chat, una sola escritura alcanzaba dos superficies.

Tres lecciones (PDF p. 218): (1) la inyección indirecta no es propiedad de la búsqueda vectorial sino de tratar texto almacenado como contexto confiable —una base de datos, un campo CMS o una tabla de config son fuentes de recuperación; (2) los delimitadores solo separan instrucciones de datos si los datos no pueden contener el delimitador, hay que neutralizar los valores, no solo rodearlos; (3) el radio de impacto sigue al campo, no a la petición.

## Access control and authorization attacks
La autorización en RAG es incómoda porque la similitud vectorial no sabe inherentemente quién pregunta. Dos usuarios con la misma consulta reciben los mismos vecinos cercanos salvo que el sistema filtre por identidad, tenant, departamento, rol o permisos a nivel de documento. Las bases de datos tradicionales aplican acceso en tiempo de consulta; RAG a menudo debe envolver la autorización alrededor de la recuperación.

- User-identity gap: la búsqueda vectorial corre sobre documentos antes de aplicar permisos. El filtrado post-recuperación quita resultados no autorizados antes de la respuesta, pero genera fugas de temporización, cómputo desperdiciado y casos en que documentos no autorizados influyen en el ranking.
- Filtrado pre-recuperación: más seguro (los documentos no autorizados nunca entran al espacio de búsqueda) pero aumenta la complejidad de gestión del índice.
- Autorización basada en metadatos: si etiquetas como public, confidential, department, tenant, owner o identificador de paciente se asignan sin validación, se expone contenido a audiencias indebidas. En multi-tenant, un error de namespace/índice/filtrado recupera datos del tenant equivocado.

La elección arquitectónica es un trade-off entre pre-retrieval filtering, post-retrieval filtering, índices segregados e híbridos. Sistemas de alto riesgo → aislamiento y autorización pre-recuperación. Lo importante es hacer la elección explícita.

## Detection and monitoring
El monitoreo debe observar el pipeline más allá del endpoint del modelo; los logs de aplicación no revelan si una fuente cambió, un cluster de embeddings se desplazó o un documento empezó a rankear para consultas no relacionadas.

- En ingesta: fallos de autenticación de fuente, volumen inusual de documentos, formato oculto, Unicode sospechoso, near-duplicates repetidos, cambios súbitos en documentos estables.
- En embedding/vector database: embeddings atípicos, cambios de densidad de cluster, jobs de embedding fallidos, modificaciones no autorizadas de índice, escrituras anómalas, picos de latencia.
- En recuperación/respuesta: documentos inesperados en el top-K, saltos de ranking, colapso de diversidad de fuentes, cambios en patrones de cita, discordancia respuesta-fuente, baja confianza en el contexto recuperado.

Frameworks como Ragas ayudan a evaluar calidad de recuperación, fidelidad (faithfulness) y relevancia, pero las métricas son solo parte. El split tipo AISVS: Nivel 1 (logging normal: autenticación de fuente, umbrales de similitud, monitoreo básico de patrones de consulta); Nivel 2 (auditoría de resultados de recuperación, análisis de distribución de embeddings, comprobaciones de alineación de respuesta); Nivel 3 (correlación entre etapas, detección de desplazamiento de clusters a escala, baselines de comportamiento sobre millones de documentos).

## Defensive architecture and mitigations
La defensa RAG no es un control sino un conjunto distribuido por el pipeline: source, ingestion, embedding, vector database, retrieval, augmentation, response y monitoreo de toda la ruta. Vista desde la ingeniería moderna, "la defensa RAG es ingeniería de contexto con una capa de almacenamiento" (PDF p. 221).

- Source security: valida de dónde vienen los documentos, quién los aprobó y si cambiaron inesperadamente.
- Ingestion security: sanitiza formato oculto, filtra patrones de ataque conocidos, trocea de forma coherente, rate-limita fuentes sospechosas y pone en cuarentena contenido a revisar.
- Embedding security: verifica si los vectores coinciden con el comportamiento semántico esperado.
- Vector database security: restringe escrituras, protege fronteras de tenant, hashea/verifica integridad de embeddings y mantiene backups para rollback.
- Retrieval security: valida la consulta, aplica autorización antes o durante la búsqueda, re-rankea con señales de seguridad y evita que una fuente domine el top-K.
- Augmentation security: mantiene el contenido recuperado visiblemente separado de las instrucciones del sistema y las consultas (delimitadores, prompts estructurados, seguimiento de citas) para que el modelo trate el material como datos y no como comandos.
- Response security: comprueba alineación respuesta-fuente, citas reales, fuga de datos sensibles y si el modelo siguió una instrucción oculta.

La parte difícil no es nombrar las capas, sino decidir cuánta fricción merece cada una según el riesgo (healthcare/finanzas/gobierno justifican controles fuertes en cada capa; un asistente de documentación pública acepta controles más ligeros y más detección).

## Trade-offs and practical guidance
La seguridad RAG perfecta no es práctica: revisar manualmente cada documento y validar cada recuperación vuelve el sistema demasiado lento o costoso. El objetivo es la reducción consciente de riesgo. Despliegues de alta seguridad priorizan procedencia de fuente, autorización pre-recuperación, aislamiento de tenant, detección de anomalías en embedding/recuperación, validación de citas y alineación respuesta-fuente. Despliegues empresariales estándar empiezan con fuentes autenticadas, ingesta por etapas, validación de metadatos, monitoreo de recuperación y una ruta de revisión de respuestas. Los de bajo riesgo con datos públicos mantienen controles ligeros pero necesitan monitoreo de abuso y eliminación rápida de contenido envenenado.

La prueba práctica son cuatro preguntas durante un incidente: qué fuente introdujo el contenido malo, qué chunks y embeddings se crearon de él, qué usuarios lo recuperaron y qué respuestas pudieron verse influidas. Si el sistema no puede responderlas, no está listo para uso RAG de alta confianza.

Los controles mapean a OWASP LLM04, LLM08, LLM05 y a preocupaciones de NIST, MITRE ATLAS, AISVS y la OWASP AI Testing Guide. El capítulo 7 trató memoria y estado; el 8, la recuperación; el capítulo 9 combina ambos con agentes (planificación, uso de herramientas y acción), donde el conocimiento envenenado es más peligroso. El límite se agudiza cuando la recuperación se expone por conectores tipo MCP o herramientas de agente: la procedencia, la autorización y la evidencia de auditoría deben viajar con el contenido recuperado.

## Ideas clave
- Un RAG puede comprometerse contaminando la capa de recuperación sin tocar nunca el LLM; el anclaje en fuentes crea una nueva superficie de ataque.
- Distinción clave: envenenamiento deliberado vs. contaminación accidental; mismo impacto práctico, distintas estrategias defensivas.
- La persistencia y la escala son el gran cambio: una fuente envenenada afecta a todo usuario que la recupere hasta que se detecte y elimine.
- Los embedding attacks controlan *qué* se recupera (geometría del espacio vectorial); la indirect prompt injection controla *qué hace* el modelo después.
- La inyección indirecta no es exclusiva de la búsqueda vectorial: cualquier texto almacenado tratado como contexto confiable (BD, CMS, config) es una fuente de recuperación.
- Los delimitadores solo funcionan si los datos no pueden contenerlos: hay que neutralizar los valores insertados, no solo rodearlos.
- La similitud vectorial no conoce la autorización; preferir filtrado pre-recuperación y aislamiento de tenant en sistemas de alto riesgo.
- Trata el índice RAG como infraestructura crítica: autentica fuentes, valida ingesta, monitorea embedding/recuperación, separa datos de instrucciones, verifica citas y conserva telemetría para la traza forense.
