# Securing Modern Web Applications (Asegurando aplicaciones web modernas) — Estudio

## Tarjetas de repaso

P: ¿Qué parte del libro abre el capítulo 20 y qué dos partes lo preceden?
R: Abre la Parte III (la defensa), tras la Parte I (recon) y la Parte II (ofensiva).

P: ¿Por qué el autor presenta recon y ofensiva antes que la defensa?
R: Porque entender cómo un hacker mapea la superficie de ataque e irrumpe en una aplicación es conocimiento crucial para defenderla.

P: ¿Por qué las aplicaciones web modernas amplían la superficie de ataque frente a las antiguas?
R: Porque son mucho más complejas y distribuidas que las predecesoras monolíticas, con server-side rendering y poca interacción.

P: ¿Cuál es la metáfora que recorre el capítulo y qué representa cada elemento?
R: El castillo medieval: el castillo y sus murallas son el código central; las edificaciones externas son las dependencias e integraciones.

P: Según la metáfora del castillo, ¿qué obliga a hacer una superficie de ataque amplia?
R: Priorizar las defensas según el riesgo, porque es inviable maximizar la fortificación en cada punto de entrada.

P: ¿Quién suele encargarse de la priorización y gestión de vulnerabilidades como "defensor maestro"?
R: Security engineers en empresas grandes, o ingenieros de software más generalistas en empresas pequeñas.

P: ¿Cuál es el primer paso para una aplicación bien fortificada y cuándo ocurre?
R: La fase de arquitectura, antes de escribir código, prestando atención a cómo fluyen los datos.

P: ¿Qué técnicas de evaluación se usan en la arquitectura segura?
R: Desde el análisis de flujo de datos hasta el threat modeling de nuevas funcionalidades.

P: ¿Por qué conviene que un equipo no relacionado revise los commits, además del equipo del autor?
R: Para reducir el conflicto de interés, sobre todo en seguridad.

P: ¿De qué factores se derivan el riesgo y la prioridad de una vulnerabilidad?
R: Riesgo financiero, dificultad de explotación, tipo de datos comprometidos, acuerdos contractuales y mitigaciones ya implementadas.

P: ¿Por qué añadir logging a una vulnerabilidad conocida mientras se desarrolla el fix?
R: Para detectar si algún hacker la explota durante ese periodo; la falta de logging ha llevado a la ruina de varias empresas.

P: Según un security engineer citado, ¿qué porcentaje de vulnerabilidades son regresiones?
R: Aproximadamente el 25% resultaron de bugs previamente cerrados que volvieron a abrirse (PDF p. 289).

P: ¿Cómo deben ser las estrategias de mitigación según el capítulo?
R: Amplias ("como una red que atrapa tantos peces como sea posible") y profundas en las áreas críticas.

P: ¿En qué formas toma forma la mitigación del riesgo?
R: Codificación segura, arquitectura segura, frameworks de pruebas de regresión, secure software development life cycle (SSDL) y mentalidad secure-by-default.

P: ¿Cuál es la idea rectora sobre los datos en la ingeniería de seguridad?
R: Gran parte consiste en asegurar datos en tránsito de un punto A a un punto B y dondequiera que reposen antes, durante o después.

## Preguntas de autoevaluación

P: ¿Cuál es la tesis central del capítulo sobre asegurar una aplicación web?
R: Que es un proceso continuo y por etapas, análogo a defender un castillo medieval, donde hay que priorizar las defensas según el riesgo. (Sección: Lo que necesitas saber / La metáfora que recorre el capítulo)

P: ¿Por qué es preferible detectar fallos de seguridad en la fase de arquitectura y no después del despliegue?
R: Porque es mucho más fácil detectar y resolver fallos profundos antes de escribir y desplegar; tras la adopción por usuarios, la re-arquitectura queda limitada y puede obligar a los clientes a rehacer procesos costosos. (Sección: Arquitectura de software defensiva)

P: ¿Qué cuatro puntos principales debe vigilar una revisión de código enfocada en seguridad?
R: Cómo se transmiten los datos de A a B, cómo se almacenan, cómo se presentan al usuario al llegar al cliente, y qué operaciones ocurren y cómo se persisten al llegar al servidor. (Sección: Revisiones de código exhaustivas)

P: ¿Qué métodos modernos usan las empresas conscientes para el descubrimiento de vulnerabilidades?
R: Bug bounty programs, equipos internos red/blue, penetration testers de terceros e incentivos corporativos para que los ingenieros registren vulnerabilidades conocidas. (Sección: Descubrimiento de vulnerabilidades)

P: ¿Cuáles son los pasos de la gestión de una vulnerabilidad tras evaluar su riesgo?
R: Priorizar según el riesgo, seguir el fix hasta completarse con plazos basados en el riesgo, revisar los contratos con clientes, añadir logging si puede registrarse, y escribir pruebas automatizadas para evitar que reaparezca. (Secciones: Análisis de vulnerabilidades / Gestión de vulnerabilidades)

P: ¿Por qué merece la pena construir un framework de pruebas de regresión?
R: Porque un gran porcentaje de vulnerabilidades son regresiones (~25%), el framework es simple de construir y añadir casos cuesta una fracción del tiempo del fix, ahorrando tiempo y dinero. (Sección: Pruebas de regresión)

P: ¿Qué ventaja defensiva aporta conocer las técnicas de recon y ofensiva de las Partes I y II?
R: El recon ayuda a camuflar la aplicación y a priorizar fixes; la ofensiva ayuda a entender qué defensas levantar y qué datos quedarían en riesgo según la categoría de exploit. (Sección: Técnicas de recon y ofensiva aplicadas)

## Checklist

- Analizar el flujo de datos y hacer threat modeling de nuevas funcionalidades durante la fase de arquitectura, antes de escribir código.
- Revisar cada commit con criterios de seguridad, idealmente con un equipo externo al del autor para reducir el conflicto de interés.
- En la revisión, verificar cómo se transmiten, almacenan, presentan y persisten los datos de A a B.
- Descubrir vulnerabilidades de forma proactiva con bug bounties, equipos red/blue, pentesters de terceros e incentivos internos.
- Evaluar el riesgo de cada vulnerabilidad (impacto financiero, dificultad de explotación, tipo de datos, contratos y mitigaciones existentes) para fijar su prioridad.
- Seguir el fix hasta completarse con plazos basados en el riesgo y revisar si se violó algún acuerdo contractual.
- Añadir logging adicional a las vulnerabilidades conocidas mientras se desarrolla el fix para detectar explotación activa.
- Escribir un test de regresión tras cada fix y mantener un framework de regresión que impida la reaparición de la brecha.
- Aplicar estrategias de mitigación amplias y profundas: codificación segura, arquitectura segura, SSDL y mentalidad secure-by-default.
