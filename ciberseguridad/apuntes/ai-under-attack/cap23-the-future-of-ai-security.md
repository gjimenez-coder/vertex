# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 23 — The Future of AI Security (El futuro de la seguridad de la IA)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
Este capítulo final mira más allá de la práctica actual hacia el futuro que esa práctica está construyendo. La tesis es que la seguridad de la IA no espera a una fecha futura: ya está en marcha. Las piezas de un conflicto de seguridad más autónomo ya existen (coding asistido por IA, actores que experimentan con operaciones orquestadas por IA, defensores que usan detección y respuesta automatizadas). La brecha hacia sistemas más autónomos se mide en trabajo de ingeniería, gobernanza y adopción, no en magia.

El futuro llega de forma desigual. Anthropic reportó ciberespionaje orquestado por IA, el Google Threat Intelligence Group rastreó experimentos de malware que invocan modelos de lenguaje durante las operaciones, y los equipos de software lidian con código generado más rápido de lo que pueden revisar. En paralelo, se forma la guía de control en torno a AISVS, los riesgos de aplicaciones agénticas de OWASP y AIUC-1.

Sales sabiendo cómo converge el campo (capacidades actuales ya suficientes para impacto masivo), la progresión de IA como herramienta → agente → sistema autónomo, las dinámicas del conflicto máquina contra máquina, los desafíos de alineamiento en contextos adversariales, cómo cambia el rol del profesional humano, y cómo navegar la incertidumbre sin apostar a una sola predicción.

## El ejemplo que recorre el capítulo
El capítulo abre con un escenario: un ataque de once minutos. A las 2:34 AM un sistema autónomo identifica un API gateway mal configurado en una firma de servicios financieros; a las 2:36 ya mapeó la red interna e inició movimiento lateral; a las 2:38 la IA defensiva detecta patrones anómalos de autenticación y aísla segmentos. Dos sistemas se mueven más rápido de lo que los humanos pueden razonar: el atacante busca rutas alternas mientras el defensor las cierra. A las 2:45 la defensa contiene la intrusión en una subred no crítica y el atacante se desconecta. "Ese escenario no es el estado por defecto de hoy, pero ya no es pura ciencia ficción" (PDF p. 490). El escenario reaparece al explicar la velocidad del conflicto AI-vs-AI.

## El futuro convergente
Los debates suelen aplanar la IA en escépticos y entusiastas, pero la señal útil es más compleja: investigadores, practicantes, vendedores y responsables de políticas discrepan en plazos, pero muchos coinciden en que los sistemas actuales ya bastan para transformar trabajo, software y la economía del ataque.

- Lo que acuerdan los investigadores: el paradigma actual es suficiente para un impacto económico y social masivo aun sin otro milagro de investigación. Los sistemas no necesitan ser generalmente inteligentes para ser peligrosos; sistemas estrechos que hallan vulnerabilidades, generan ingeniería social convincente u operan herramientas reales ya crean problemas de seguridad presentes.
- Debate de plazos: Demis Hassabis discute la AGI en un horizonte de cinco a diez años; encuestas de expertos muestran desacuerdo sustancial. El punto para los practicantes no es una fecha, sino que gente seria debate años y décadas, no siglos.
- Implicaciones: el coding asistido por IA mete código generado en repos reales más rápido de lo que se revisa; las herramientas agénticas encadenan acciones a través de repos, terminales, consolas cloud, ticketing y plataformas de seguridad. AISVS, el OWASP Top 10 for Agentic Applications y AIUC-1 emergen porque se necesita lenguaje de control para sistemas que hacen más que responder preguntas.

## La era del escalado y más allá
La última década pasó por dos fases: una era de avances de investigación (el deep learning funciona) y una era de escalado (más datos y cómputo producen capacidades amplias). Esa era de escalado creó el entorno actual de modelos frontera, donde modelos de distintos desarrolladores suelen mostrar capacidades similares.

Puede estar entrando una fase donde la diferenciación se desplaza a la capa de producto, infraestructura y aplicación: APIs en tiempo real, tooling agéntico, workflows específicos de dominio, conectores de datos y planos de control. Para la seguridad, la superficie de ataque se expande de los modelos a la infraestructura y aplicaciones que los rodean. Además, cada organización crea superficies de ataque únicas según sus aplicaciones, integraciones, permisos y flujos de datos; la seguridad pasa de proteger capacidad en abstracto a proteger las formas específicas en que la organización aplica esa capacidad.

## De herramientas a agentes a sistemas autónomos
La progresión es tanto una historia de autoridad como de capacidad: cada paso da al software más capacidad de actuar mediante identidades, integraciones y permisos reales. La guía conjunta ACSC/CISA/NSA de 2026 y el SANS AI Security Maturity Model empujan hacia preguntas operativas: qué autoridad tiene el agente, qué evidencia prueba el control, qué tan rápido se revoca el acceso.

- IA como herramienta: expande la capacidad humana. Detección de anomalías, clasificación de alertas, extracción NLP de indicadores. El humano decide y actúa; la IA recomienda. "No tenía las llaves" (PDF p. 494-495).
- IA como agente: ejecuta en lugar de solo recomendar (ejecuta playbooks, aísla sistemas, abre pull requests, despliega parches). El humano pasa a definir objetivos, aprobar límites y manejar excepciones. Estos agentes están acotados pero operan bajo permisos humanos delegados o identidades no humanas con alcance definido.
- IA como sistema autónomo: fija objetivos intermedios propios, adapta estrategias con retroalimentación del entorno y opera a velocidades que impiden la participación humana táctica. Hoy no es el modelo operativo normal, pero los componentes emergen (modelos que razonan sobre seguridad, agentes que encadenan acciones, RL que adapta estrategias). Es un problema de ingeniería y gobernanza, no de inventar inteligencia desde cero.
- Timeline: no ocurre de la noche a la mañana; decisiones de alto riesgo e industrias reguladas retienen al humano más tiempo. Pero presión económica, exigencias de velocidad y complejidad favorecen la automatización.

## Cuando las máquinas luchan contra máquinas
Un posible desenlace es el conflicto entre sistemas autónomos donde atacantes y defensores despliegan IA que opera más allá de la velocidad y la comprensión humana directa.

Carrera armamentista emergente: al inicio los agentes parecerán herramientas más inteligentes (mejor detección, respuesta más rápida), pero las mejoras incrementales se componen. A escala de redes, vendedores e industrias, los defensores podrían compartir inteligencia de amenazas entre miles de entornos y los ofensivos explotar una debilidad en infraestructura expuesta antes de que los defensores terminen su primera llamada de coordinación.

Dinámicas del conflicto AI-vs-AI:
- La velocidad excederá la comprensión humana: los humanos fijan objetivos estratégicos y restricciones operativas, pero no participan en decisiones tácticas en tiempo real.
- La adaptación será continua: defensas que se adaptan en tiempo real; ofensivos que sondean sin descanso. El conflicto se vuelve un proceso evolutivo continuo, no engagements discretos.
- La complejidad excederá el modelado humano: surgen comportamientos emergentes que nadie diseñó; se podrá caracterizar el comportamiento estadísticamente pero no predecirlo de forma determinista.
- La escala dejará de depender del personal humano: los agentes se replican, coordinan y corren en paralelo a gran escala.

Qué significa para los defensores: no se puede optar por salir de este futuro. Las bases se establecen ahora: el Capítulo 21 (AI Security Operations) aporta la telemetría que consumirán los sistemas autónomos, el Capítulo 20 (AI Security Engineering) crea entornos más seguros, y el Capítulo 19 (AI Governance, Risk, and Compliance) da las estructuras de supervisión. La experiencia humana sigue siendo esencial aunque disminuya la participación táctica.

## Alineamiento en contextos adversariales
El problema de alineamiento (que la IA persiga lo que los humanos quieren, no interpretaciones literales dañinas) se agudiza en seguridad.

- Alineamiento defensivo: un sistema con el objetivo "minimizar intrusiones exitosas", tomado literalmente, podría apagar toda la conectividad. Misalineamientos sutiles: optimizar solo lo detectable y perder ataques fuera de patrón; recompensar la respuesta rápida y causar contención desproporcionada; entrenar en ataques históricos y no generalizar a técnicas nuevas. El equilibrio entre velocidad y control es en sí un desafío de alineamiento.
- Alineamiento ofensivo: un pentest que causa daño no intencionado si no se restringe a explotación segura; un red team que afecta sistemas conectados de terceros; sistemas que escalan más allá del alcance. Aplica tanto a equipos legítimos como a actores maliciosos (que aún valoran sigilo, acceso, beneficio o negabilidad).
- Alineamiento en competencia: sistemas que co-evolucionan (defensa con honeypots y señuelos, ofensiva que detecta el engaño) pueden derivar en estrategias efectivas pero incomprensibles. La presión competitiva puede erosionar salvaguardas aunque todos prefieran mantenerlas.
- Enfoques: tres requisitos prácticos — (1) la especificación de objetivos debe anticipar la explotación adversarial; (2) los sistemas de restricciones deben mantenerse en contextos adversariales; (3) el monitoreo e intervención deben detectar el misalineamiento entre el ruido adversarial, distinguiéndolo de la adaptación apropiada. Esto hace el alineamiento operativo, no abstracto.

## El rol cambiante de los profesionales humanos
El rol se transforma, no desaparece: pasa de ejecución manual a trabajo asistido por IA, supervisión humana, manejo de excepciones y juicio estratégico.

- De ejecución a supervisión: el analista pasa de investigar alertas individuales a asegurar que los sistemas de IA investiguen correctamente miles de alertas; igual para ingenieros y respondedores. No es desprofesionalización, es recualificación hacia supervisar, restringir y mejorar sistemas.
- Fijar objetivos y restricciones: traducir requisitos de negocio y seguridad en objetivos que la IA pueda perseguir; definir restricciones anticipando comportamiento no deseado y casos límite.
- Manejo de excepciones: situaciones novedosas fuera del entrenamiento, zero-days, cambios regulatorios; fallos de la IA (detectar el error, preservar evidencia, actualizar controles); decisiones de alto impacto legal, financiero o humano que siempre requieren juicio humano.
- Funciones estratégicas: inteligencia de amenazas (IA procesa, humano interpreta y contextualiza), desarrollo del programa (relaciones y política organizacional), ética y gobernanza (decidir qué puede hacer la IA, qué restricciones reflejan sus valores).
- Preparación: desarrollar pensamiento estratégico, construir experticia específica en sistemas de IA, cultivar juicio que la IA no replica (ética, gestión de stakeholders, resolución creativa) y mantenerse adaptable.

## Navegando la incertidumbre
Las predicciones específicas fallan de forma fiable; se necesitan estrategias, no predicciones.

- Lo que sí se puede predecir: las capacidades de la IA aumentarán; las implicaciones de seguridad seguirán al aumento de capacidad; la presión económica y competitiva impulsará la adopción; la atención regulatoria continuará aunque cambien reglas y plazos.
- Lo que no se puede predecir: el momento de los avances concretos, el comportamiento emergente de sistemas complejos, las respuestas sociales y políticas, y los black swan que pueden redirigir el campo entero.
- Estrategias para la incertidumbre: construir capacidad adaptativa (los programas sostenibles del Capítulo 22 son "infraestructura de supervivencia", PDF p. 508); invertir en fundamentos valiosos en todos los escenarios; mantener opcionalidad; planear escenarios divergentes; monitorear señales de cambio (AISVS, guía agéntica de OWASP, AIUC-1, reportes de incidentes); y aceptar que algunas apuestas fallarán, porque la parálisis es peor que la acción imperfecta.

## Mirando hacia adelante y reflexiones finales
Los próximos años intensificarán los patrones del libro: ataques más sofisticados, defensas más maduras, marcos de gobernanza en movimiento. Las organizaciones que construyen capacidades hoy quedan mejor posicionadas: el monitoreo alimentará a la futura IA defensiva, los controles de infraestructura limitarán a los agentes cuando fallen, la gobernanza definirá quién aprueba riesgo. Los fundamentos siguen siendo esenciales: threat modeling, defense in depth, least privilege y monitoreo continuo aplican sin importar quién los ejecute.

El futuro no está predeterminado: emerge de decisiones de practicantes, organizaciones, vendedores, investigadores y responsables de políticas. "La parte más difícil será a menudo la adopción" (PDF p. 511): sistemas de IA seguros cuestan dinero, ralentizan releases y exigen evidencia, en tensión con la presión de entregar rápido. El futuro pertenece a quienes se preparan, prueban, adaptan y mantienen el control de sistemas que se mueven más rápido que sus organizaciones.

## Ideas clave
- La seguridad de la IA ya está en marcha; la transición a sistemas autónomos es trabajo de ingeniería, gobernanza y adopción, no ciencia ficción.
- El paradigma actual basta para impacto masivo; los sistemas estrechos ya son peligrosos sin necesidad de AGI.
- La progresión herramienta → agente → sistema autónomo es una historia de autoridad: cada paso da más capacidad de actuar con identidades y permisos reales.
- El conflicto AI-vs-AI superará la velocidad, la adaptación continua, la complejidad y la escala que los humanos pueden manejar tácticamente.
- El alineamiento en seguridad es adversarial y operativo: objetivos, restricciones y monitoreo deben resistir la explotación activa; la presión competitiva erosiona salvaguardas.
- El rol humano se desplaza de ejecución a supervisión, fijación de objetivos y restricciones, manejo de excepciones y funciones estratégicas (ética, gobernanza, inteligencia).
- Ante la incertidumbre: construir capacidad adaptativa, invertir en fundamentos, mantener opcionalidad, planear escenarios y monitorear señales (AISVS, OWASP agéntico, AIUC-1).
- La parte más difícil es la adopción; invertir hoy genera retornos compuestos y los fundamentos (threat modeling, defense in depth, least privilege, monitoreo) siguen vigentes.
