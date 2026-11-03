# Threat Modeling Applications (Modelado de amenazas de aplicaciones) — Estudio

## Tarjetas de repaso

P: ¿Cuáles son las cinco metas de un buen threat model?
R: Documentar conocimiento, identificar threat actors, identificar riesgos (attack vectors), identificar mitigaciones e identificar el delta entre riesgos y mitigaciones.

P: ¿Por qué un riesgo no es accionable hasta conocer sus mitigaciones existentes?
R: Porque implementar una mitigación para un riesgo ya mitigado introduce más bugs, deuda técnica e incluso nuevas vulnerabilidades.

P: ¿Qué es el logic design y qué permite detectar?
R: Es la descripción funcional de la feature (más alta que la arquitectura, más baja que marketing); permite detectar logic vulnerabilities derivadas de que la app no siga la lógica para la que fue pensada.

P: ¿Qué es una logic vulnerability y por qué es única a cada aplicación?
R: Es una vulnerabilidad surgida de que la aplicación no siga su lógica prevista; es única porque depende de los requisitos de negocio propios de cada app (p. ej. publicar un score mayor de 5 saltándose el formulario).

P: ¿Cuál es la meta del technical design y qué debe permitir identificar?
R: Permitir identificar amenazas generadas por la arquitectura: tecnologías usadas, servicios de terceros (in/out-of-network), flujos de datos (DFD), configuración de redes, controles de authn/authz y el esquema de base de datos.

P: ¿Por qué se necesitan tanto el logic design como el technical design?
R: Porque el technical design por sí solo no explica los objetivos de negocio y el logic design no describe la arquitectura; ambos son complementarios.

P: ¿Qué es un threat actor y qué tipos deben incluirse en la lista?
R: Es un atacante arquetípico con rutas de ataque únicas; la lista debe ser exhaustiva e incluir usuarios internos, externos y máquina, divididos por permisos autenticados y no autenticados.

P: ¿Qué es una attack surface area y para qué sirve?
R: Es el área de ataque distinta de cada threat actor; sirve para rankear riesgos y resolver primero los ataques más graves de los actores más peligrosos.

P: ¿Qué es un attack vector y cómo se obtiene?
R: Es una vía potencial futura de ataque (aún no una vulnerabilidad, porque el sistema no está desarrollado); se obtiene por cross-analysis de logic design, technical design y threat actors.

P: ¿Qué significa la notación P0–P4 en los attack vectors?
R: "P" es prioridad/severidad, anotación común en la industria, siendo P0 la más alta y P4 la más baja (PDF p. 343).

P: ¿En qué consiste la fase de identificación de mitigaciones?
R: Es una fase de recolección de datos que documenta las mitigaciones existentes por cada attack vector (p. ej. motor de validación de scores, DSL que fuerza prepared statements contra SQL injection).

P: ¿Qué es la identificación del delta y qué implica para el lanzamiento?
R: Es cruzar los attack vectors con las mitigaciones y eliminar los ya mitigados; para cada vector restante debe idearse una mitigación suficiente, y sin ella la feature no debe lanzarse (PDF p. 345).

P: ¿Por qué se dice que el threat model es coste-efectivo?
R: Porque identifica actores y vectores antes de desarrollar, cuando los problemas son más baratos: 10 horas de arreglos en arquitectura equivalen a 100 postlanzamiento.

P: ¿Por qué el threat model se considera un documento vivo?
R: Porque transfiere conocimiento de seguridad entre ingenieros y, ante cambios de alcance, se reevalúan conocimiento, threat actors, vectores, mitigaciones y delta.

## Preguntas de autoevaluación

P: ¿Qué riesgo tiene implementar el threat modeling de forma apresurada?
R: Se convierte en "marcar casillas" y malgasta tiempo; solo aporta valor si se implementa correctamente. (Lo que necesitas saber)

P: En el ejemplo de MegaBank, ¿qué logic vulnerability aparece en la feature de user review y por qué es un problema?
R: Un usuario que publica una puntuación mayor de 5 saltándose el formulario con una petición HTTP personalizada; sesga la agregación/promedio y daña la confianza y la reputación de marca. (Diseño lógico)

P: A partir del diseño técnico de MegaBank, ¿qué tres vulnerabilidades se intuyen?
R: Posible XSS (no se indica cómo se renderiza el texto), posible SQL injection (no se indica cómo se genera la consulta SQL) e information disclosure por el mensaje "no reviews found". (Diseño técnico)

P: ¿Por qué es un error considerar solo ataques humanos directos o solo humanos externos?
R: Porque hay que modelar el peor caso: usuarios internos pueden ser hackeados o volverse rogue, y los usuarios máquina (scripts) pueden malfuncionar o ser comprometidos; deben incluirse todos. (Threat actors / Attack vectors)

P: ¿Cuáles son los attack vectors con severidad P0 en el ejemplo y a qué actores afectan?
R: SQL injection (todos menos guest) y High privilege user attacks (admin y review aggregator script). (Attack vectors)

P: Tras la identificación del delta, ¿qué vectores quedan sin mitigar en MegaBank?
R: Information disclosure—FeatureID (P3), GraphQL circular and large queries (P1), GraphQL introspection and errors (P1) y High privilege user attacks (P0). (Identificación del delta)

P: ¿Qué mitigación se propone para los High privilege user attacks?
R: Privileged permissions rework: acotar los tokens a su funcionalidad, registrar cada llamada API off-platform sin que el usuario privilegiado pueda revocar/borrar logs, y limitar el review aggregator script a escritura en la columna aggregate score y lectura en score. (Identificación del delta)

## Puntos a dominar

- Las cinco metas de un threat model y por qué cada una se apoya en las anteriores.
- La distinción entre logic design y technical design, y qué tipo de vulnerabilidad revela cada uno.
- Que un riesgo no es accionable hasta conocer sus mitigaciones existentes.
- La composición de la lista de threat actors: internos, externos y máquina, por permisos autenticados y no autenticados.
- Que los attack vectors nacen del cross-analysis de los tres componentes y se priorizan por severidad P0–P4.
- El principio de modelar siempre el peor caso.
- La regla del delta: sin mitigación suficiente para cada vector sin cubrir, la feature no debe lanzarse.
- La naturaleza de documento vivo del modelo y su coste-efectividad (~10x más barato arreglar en arquitectura que postlanzamiento).
