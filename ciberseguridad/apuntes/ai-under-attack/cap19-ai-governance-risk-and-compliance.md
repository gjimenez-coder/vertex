# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 19 — AI Governance, Risk, and Compliance (Gobernanza, riesgo y cumplimiento de la IA)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF; las citas usan la página del PDF.

## Lo que necesitas saber
Los controles técnicos de seguridad solo cubren una parte del perfil de riesgo de la IA. El capítulo abre con un sistema de contratación que pasó la revisión técnica —validación de entradas, filtrado de salidas, monitoreo conductual— y aun así perjudicó a candidatos mayores de 40 años. No hubo brecha ni atacante: nadie hizo de la equidad algorítmica, la propiedad, el monitoreo y la rendición de cuentas parte de la decisión de despliegue. La tesis central es que la gobernanza, la gestión de riesgo y el cumplimiento (GRC) convierten en operativas las preguntas de quién aprueba, quién es dueño del comportamiento, qué evidencia prueba que es aceptable y quién responde cuando hay daño.

Gobernanza, riesgo y cumplimiento son trabajos distintos que fallan de forma distinta. La gobernanza establece derechos de decisión y rendición de cuentas. La gestión de riesgo identifica qué puede salir mal, a quién afecta y qué controles lo reducen. El cumplimiento mapea la práctica interna a obligaciones externas. La IA complica esto porque su comportamiento es probabilístico, existe drift real, las categorías de daño van más allá de la seguridad clásica y los sistemas agénticos pueden actuar mediante autoridad real.

Sales sabiendo cómo distinguir los tres roles, cómo separar responsabilidades de creador y adoptante, por qué la gobernanza de IA difiere de la de TI, cómo escalar con gobernanza por niveles (tiers), cómo evaluar riesgo, cómo tratar la autoridad del agente como problema de gobernanza, y cómo navegar el marco regulatorio (EU AI Act, NIST, ISO, sectoriales) integrando todo en el ciclo de vida.

## El ejemplo que recorre el capítulo
El hilo conductor es el sistema de contratación potenciado por IA que discriminaba a candidatos mayores de 40 años. "The system was secure enough to pass a technical review and still harmful enough to become an organizational failure" (PDF p. 408). Ilustra que la seguridad técnica sin gobernanza produce fallos organizacionales: el problema no fue un atacante, sino la ausencia de propiedad, monitoreo y rendición de cuentas en la decisión de desplegar.

## Definición del problema de gobernanza
GRC se tratan como sinónimos pero no lo son; cada uno responde una pregunta distinta.
- **Gobernanza**: establece derechos de decisión y rendición de cuentas —quién aprueba para producción, qué evidencia debe existir, quién es dueño tras el lanzamiento, quién decide si un riesgo es aceptable, quién responde ante el daño. No es el logo de un comité, es la estructura de autoridad. "Good AI governance has teeth" (PDF p. 409): define propiedad, rutas de aprobación, escalamiento, excepciones y requisitos de evidencia.
- **Gestión de riesgo**: identifica qué puede fallar, a quién afecta, probabilidad y controles. Para IA va más allá de confidencialidad, integridad y disponibilidad: equidad, seguridad, explicabilidad, fiabilidad, abuso, drift y consecuencias reales. Un registro de riesgo que solo dice "model risk" no sirve; hay que nombrar el modo de fallo (datos sesgados, discriminación por proxy, prompt injection vía contenido recuperado, mal uso de herramientas por un agente, drift).
- **Cumplimiento**: mapea la práctica interna a obligaciones externas (EU AI Act, derecho laboral, privacidad, model-risk financiero, dispositivos médicos, contratos). Falla cuando se vuelve checklist estático; la solución es un mapa vivo de caso de uso → obligación → evidencia.

## Creadores, adoptantes y responsabilidad compartida
Las organizaciones actúan como creadores, adoptantes o ambos.
- **Creador**: controla datos de entrenamiento, arquitectura, evaluación, decisiones de release y comportamiento del modelo. Necesita evidencia de procedencia y calidad de datos, representatividad, etiquetado, entrenamiento, evaluación, pruebas de seguridad y sesgo, documentación del modelo, criterios de release, monitoreo y manejo de vulnerabilidades.
- **Adoptante**: controla selección del caso de uso, integración, UX, datos enviados al modelo, revisión humana, monitoreo y escalamiento. Necesita evidencia de ajuste del caso de uso, due diligence del proveedor, manejo de datos, diseño de prompts/retrieval, supervisión humana, avisos, apelaciones, respuesta a incidentes y estrategia de salida. "You cannot outsource accountability by buying an AI feature" (PDF p. 411).
- **Procurement y revisión de proveedores**: es donde las responsabilidades del adoptante se vuelven reales o desaparecen. Si un SaaS añade IA en silencio, hay que saber qué datos fluyen, si el proveedor los usa para entrenar, qué evaluación existe, qué logging hay y cómo deshabilitar la función. Tratar la revisión de proveedores como gobernanza, no como papeleo posterior.

## Por qué la gobernanza de IA difiere de la de TI
La gobernanza de TI tradicional asume un sistema mayormente determinista. La IA rompe ese patrón porque el comportamiento depende de datos, contexto, probabilidad, actualizaciones, prompts, retrieval, usuarios e integración.
- **Comportamiento probabilístico**: un modelo puede dar respuestas distintas a entradas similares; un clasificador devuelve confianza, no certeza. La gobernanza debe definir error aceptable, umbrales de monitoreo, revisión humana y evidencia para decisiones bajo incertidumbre.
- **Opacidad**: cuando una IA deniega un préstamo o marca una transacción, la decisión emerge de relaciones estadísticas difíciles de explicar. La gobernanza define qué explicación se requiere, para quién y a qué nivel de garantía.
- **Drift y sesgos emergentes**: se requiere monitoreo continuo post-despliegue para drift, sesgo emergente y cambio de distribución. La aprobación puntual no basta; el monitoreo debe conectar el rendimiento del modelo con resultados de negocio y daño (quejas, apelaciones, segmentos demográficos, escalamientos, reportes de alucinación).

## Responsible AI como piso operativo
Los principios de Responsible AI solo sirven si cambian lo que hace la organización. La redacción varía entre Microsoft, Google, OECD, NIST, ISO y guías sectoriales, pero los compromisos son consistentes. Hay que traducir principios en evidencia:
- **Equidad**: pruebas de sesgo, análisis de poblaciones afectadas, ruta de apelación, segmentos de monitoreo, limitaciones documentadas.
- **Fiabilidad y seguridad**: resultados de evaluación, hallazgos de red-team, comportamiento de fallback, umbrales de incidente, plan de rollback.
- **Privacidad y seguridad**: inventario de datos, controles de acceso, autorización de retrieval, logging, retención, evidencia de threat model.
- **Transparencia**: avisos, model cards, explicaciones al usuario, limitaciones conocidas, registros de decisión.
- **Rendición de cuentas**: dueños nombrados, registros de aprobación, aceptación de riesgo, dueños de excepciones, cadencia de revisión post-despliegue.

## Marcos de gobernanza que escalan
La forma práctica es la **gobernanza por niveles**: clasificar el caso de uso, asignar un dueño, exigir evidencia proporcional al riesgo, integrar aprobación en el ciclo de vida y mantener monitoreo tras el lanzamiento.
- **Tier 1**: productividad interna de bajo riesgo, datos poco sensibles, sin decisiones consecuentes.
- **Tier 2**: cara al cliente u operativo donde los errores causan daño reversible.
- **Tier 3**: decisiones consecuentes, dominios regulados, poblaciones sensibles, impacto en seguridad, acción agéntica o riesgo material.

La **política** debe definir qué debe ser cierto antes de pasar por intake, diseño, desarrollo, validación, despliegue, operación, cambio y retiro, mediante preguntas durables (caso de uso, afectados, datos, modelo/proveedor, qué puede fallar, controles, evidencia, dueño). La **aplicación técnica** debe aparecer donde ya ocurre el trabajo: formularios de intake, revisión de arquitectura, registro de modelos, procurement, CI/CD, MLOps, aprobaciones de release, observabilidad. "At five hundred, informal governance is fiction" (PDF p. 415). El **manejo de excepciones** registra el control faltante, la razón, el control compensatorio, la fecha de expiración, dueño, revisor y condición de re-revisión; no permitir excepciones permanentes sin visibilidad ejecutiva.

## Evaluación de riesgo de IA
Empieza con las preguntas normales (activos, atacantes, fallos, controles, riesgo residual) y añade comportamiento del modelo, datos de entrenamiento y retrieval, dependencia humana, decisiones downstream, afectados, drift, abuso e integración con herramientas o credenciales. Categorías de riesgo:
- **Seguridad**: prompt injection, data poisoning, robo de modelo, abuso de herramientas, compromiso de supply-chain, acceso no autorizado.
- **Equidad**: impacto dispar, discriminación por proxy, etiquetas sesgadas, evaluación sesgada, tasas de error desiguales.
- **Fiabilidad**: alucinación, drift, fragilidad, exceso de confianza, mal retrieval, fallback inseguro.
- **Privacidad**: exposición de datos de entrenamiento, membership inference, fuga de prompts, logging excesivo, retrieval cross-tenant.
- **Safety y daño**: impacto físico, financiero, laboral, sanitario, legal, reputacional.
- **Autoridad**: uso de herramientas por el agente, credenciales delegadas, identidades no humanas, aprobaciones, auditoría, revocación.

El riesgo del caso de uso va primero (impacto, sensibilidad de datos, dominio, población, autonomía, reversibilidad). Luego mapear amenazas a controles con **MITRE ATLAS** y el **OWASP Top 10 for Large Language Model Applications** como referencias, no como librería copia-pega. El monitoreo continuo rastrea calidad, drift, sesgo, eventos de seguridad y de safety, escalamientos, quejas y excepciones. Dejar artefactos: model card / system card, threat model, decisión de release; para sistemas agénticos, añadir un **mapa de autoridad**.

## La autoridad del agente como problema de gobernanza
Cuando un sistema puede planear, usar herramientas, llamar APIs, escribir archivos, abrir pull requests o actuar vía navegador, "you are no longer only approving outputs; you are approving action through authority" (PDF p. 418). Conecta con los capítulos 9 (arquitectura agéntica), 10 (ataques a sistemas con herramientas) y 18 (credenciales con scope, enforcement, aislamiento, auditoría, revocación).
- **Permisos humanos delegados**: el agente actúa a través del acceso de un humano (tokens, repos, shell, sesiones de navegador, cuentas SaaS, CI/CD). El riesgo es autoridad legítima usada en la secuencia, momento o blanco equivocados. La evidencia debe responder: quién delegó, para qué, por cuánto tiempo, qué herramientas, qué blancos, qué aprobaciones, qué logs y qué ruta de revocación.
- **Identidades no humanas**: actor separado (service principal, managed/workload identity, runtime autónomo) con su propio conjunto de permisos. Más limpio que pedir prestado un token humano, pero crea obligaciones de ciclo de vida (dueño, scope, rotación, monitoreo, revocación). Exigir un inventario de autoridad por agente.

**Evidencia mínima para aprobar un agente**: dueño nombrado; mapa de autoridad que separa permisos delegados de identidades no humanas; inventario de herramientas y acciones con permisos read/draft/write/execute/publish/delete/deploy separados; gates de aprobación para acciones de alto impacto con artefacto, blanco, datos y rollback visibles; evidencia de least-privilege, vida de credencial, rotación y prueba de revocación; monitoreo, logs de auditoría, escalamiento de incidentes y registro de aceptación de riesgo. La **aceptación de riesgo** debe ser concreta: no pedir que un ejecutivo acepte "agent risk", sino una acción con scope definido, diciendo qué pasa cuando el agente se equivoca (quién lo pausa, qué credenciales expiran, qué logs reconstruyen la decisión, quién decide su retorno al servicio).

## Navegar los requisitos de cumplimiento
El cambio regulatorio supera los ciclos de actualización corporativos; la respuesta es **resiliencia regulatoria**: saber qué obligaciones aplican, mapearlas a evidencia, rastrear cambios y mantener flexibilidad.
- **EU AI Act y GPAI**: entró en vigor el 1 de agosto de 2024 y aplica progresivamente; distintas familias de obligaciones (prácticas prohibidas y alfabetización en IA, GPAI, requisitos core, alto riesgo embebido en productos) entran en fechas distintas. No describirlo como un interruptor único. El **Code of Practice** final de la Comisión Europea (julio 2025) es un instrumento de apoyo al cumplimiento, no todo el régimen.
- **NIST, ISO y sistemas de gestión**: NIST AI RMF 1.0 y NIST AI 600-1 son vocabulario y referencias de debido cuidado, no leyes. ISO/IEC 42001 provee un estándar de sistema de gestión de IA. El **SANS AI Security Maturity Model** enmarca la madurez en Protect AI, Utilize AI y Govern AI, exigiendo probar la etapa con controles, métricas y documentación.
- **Sectorial, estatal y local**: servicios financieros se apoyan en model-risk (OCC Bulletin 2011-12); salud en guía actual de FDA para dispositivos médicos con IA; empleo en la regla AEDT de Nueva York (auditoría de sesgo, información pública, aviso). Colorado reemplazó su marco previo: la **Senate Bill 26-189** se convirtió en ley el 14 de mayo de 2026, con obligaciones clave de developer y deployer desde el 1 de enero de 2027. Citar siempre la ley vigente y la fecha operativa.
- **Política federal de EE. UU.**: avanza por órdenes ejecutivas, memorandos OMB y guía de procurement. **OMB M-25-21** es la guía actual de uso federal. La orden ejecutiva de junio de 2026 añade un enfoque de seguridad (defensa cibernética, herramientas defensivas con IA, coordinación de modelos frontier, enforcement contra uso criminal de agentes de IA).

## Roles, rendición de cuentas e integración en el ciclo de vida
La gobernanza falla cuando la responsabilidad flota. Cada sistema necesita patrocinador ejecutivo, dueño de negocio, dueño técnico, dueño de datos, socio de seguridad, socio de privacidad/legal/cumplimiento, dueño de operaciones y ruta de incidentes.
- **Asignación de responsabilidad**: usar RACI solo si aclara la acción (Responsible = el trabajo se hace; Accountable = se es dueño de la decisión; Consulted; Informed). Para agentes, añadir propiedad de autoridad: quién posee el acceso delegado, las credenciales no humanas, quién aprueba expansión de herramientas, quién puede revocar durante un incidente sin esperar a un comité.
- **Aceptación ejecutiva de riesgo**: no es una firma al final del flujo, sino la decisión de cargar un riesgo residual conocido; debe nombrar riesgo, población afectada, controles faltantes/parciales, controles compensatorios, plan de monitoreo, fecha de revisión y escalamiento. "The executive sponsor should not be allowed to accept a risk they cannot explain" (PDF p. 423).
- **Gates del ciclo de vida**: intake clasifica, requisitos capturan obligaciones, design review verifica datos/modelo/impacto/autoridad, validación prueba comportamiento y controles, despliegue exige evidencia, operación monitorea, retiro remueve acceso y archiva evidencia. En MLOps y pipelines de agentes los gates deben ser verificables por máquina donde sea posible.
- **Métricas**: deben mostrar si la gobernanza funciona, no si hubo reuniones: cobertura, oportunidad (timeliness), calidad, efectividad de control (cobertura de monitoreo, éxito de pruebas de revocación y rollback) y resiliencia de negocio (lanzamientos inseguros detenidos, incidentes reducidos).
- **Conseguir recursos**: traducir la gobernanza al lenguaje de decisiones protegidas, incidentes evitados, revisiones aceleradas y evidencia producida.

## Ideas clave
- GRC son trabajos distintos: gobernanza decide y responsabiliza, gestión de riesgo identifica fallos y controles, cumplimiento mapea obligaciones vivas a evidencia.
- La seguridad técnica no basta: un sistema puede pasar la revisión técnica y aun así causar un fallo organizacional (caso de contratación sesgada por edad).
- Creadores y adoptantes tienen responsabilidades distintas y no intercambiables; no se puede externalizar la rendición de cuentas comprando una función de IA.
- La IA difiere de TI por comportamiento probabilístico, opacidad y drift: la aprobación puntual no basta, se requiere monitoreo continuo post-despliegue.
- La gobernanza por niveles (Tier 1-3) con enforcement técnico (registros, pipelines, procurement, monitoreo) escala; la gobernanza informal es ficción a gran escala.
- Los sistemas agénticos requieren mapa de autoridad, separar permisos humanos delegados de identidades no humanas y probar least-privilege, aprobación, auditoría y revocación.
- El cumplimiento exige resiliencia regulatoria: inventario vivo, mapa a obligaciones (EU AI Act, NIST AI RMF, ISO/IEC 42001, OCC, FDA, AEDT de NYC, SB 26-189 de Colorado, OMB M-25-21) y citar la ley vigente con su fecha.
- La rendición de cuentas y los gates del ciclo de vida deben estar nombrados; la aceptación ejecutiva de riesgo debe ser concreta y explicable.
