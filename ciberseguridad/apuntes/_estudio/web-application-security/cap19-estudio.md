# Part II Summary (Resumen de la Parte II) — Estudio

## Tarjetas de repaso

- P: ¿Qué tres cosas combinadas exige probar a fondo una aplicación web? / R: Conocimiento de los arquetipos de vulnerabilidad más comunes, pensamiento crítico y conocimiento del dominio (domain knowledge).
- P: ¿Para qué sirve esa combinación de habilidades? / R: Para hallar vulnerabilidades de lógica profunda que quedan fuera de los arquetipos habituales.
- P: ¿Qué basta para empezar en cualquier proyecto de pen-testing de aplicaciones web? / R: Las habilidades fundacionales de las Partes I y II.
- P: ¿Qué hay que entender para identificar fallos avanzados y específicos de cada aplicación? / R: La lógica de negocio (modelo de negocio) subyacente de la aplicación.
- P: ¿A qué vulnerabilidades está expuesta toda aplicación web según el capítulo? / R: XSS, CSRF o XXE.
- P: Si los ataques parecen difíciles de aplicar en un escenario real, ¿cuál es la causa más probable? / R: Que falte mejorar las habilidades de recon para localizar los puntos débiles, no que la aplicación esté perfectamente endurecida.
- P: ¿Cómo se relacionan las tres partes del libro? / R: La Parte II se apoya en la Parte I y prepara la Parte III, centrada en los mecanismos defensivos.
- P: ¿Por qué a las defensas web se las llama a menudo "mitigaciones" en lugar de "arreglos" (fixes)? / R: Porque suelen estar rotas y a menudo se pueden romper o debilitar.
- P: ¿Qué estrategia recomienda el autor frente a defensas no infalibles? / R: Combinar varias defensas en lugar de depender de una sola.
- P: ¿Qué son en su mayoría las defensas de la Parte III? / R: Best practices del sector, aunque muchas no son infalibles.
- P: ¿Contra qué aplicaciones se pueden probar las técnicas de la Parte II? / R: Contra aplicaciones propias, nunca contra aplicaciones de terceros sin permiso escrito explícito del propietario.
- P: ¿Por qué deben meditarse a fondo estas técnicas? / R: Porque sirven tanto para el bien como para el mal, y pueden comprometer servidores o máquinas cliente.
- P: Antes de un live testing, ¿qué hay que asegurar respecto al propietario? / R: Que el propietario entienda los riesgos del live testing antes de empezar.

## Preguntas de autoevaluación

- P: ¿Qué mentalidad propone el capítulo al estudiar las defensas de la Parte III? / R: Pensar continuamente cómo un atacante encontraría y explotaría una aplicación con y sin defensas adecuadas. (Sección "Puente hacia la Parte III (defensas)")
- P: ¿Por qué el conocimiento del modelo de negocio es decisivo en el testing? / R: Porque, aunque toda aplicación es vulnerable a XSS, CSRF o XXE, solo entendiendo a fondo la lógica de negocio se identifican fallos más avanzados y específicos de cada aplicación. (Sección "Lo que necesitas saber")
- P: ¿Qué relación hay entre recon y las técnicas ofensivas al cierre de la Parte II? / R: Sales sabiendo encadenar recon y técnicas ofensivas; si un ataque cuesta en lo real, suele faltar recon más que sobrar hardening. (Secciones "Lo que necesitas saber" e "Ideas clave")
- P: ¿Qué implica que las habilidades de las Partes I y II puedan debilitar defensas de la Parte III? / R: Que con lo aprendido puede ser posible saltarse o debilitar defensas concretas de la Parte III. (Sección "Puente hacia la Parte III (defensas)")
- P: ¿Por qué se consideran peligrosas las técnicas de la Parte II? / R: Porque son ataques reales usados por atacantes reales de forma habitual y pueden comprometer servidores o máquinas cliente. (Sección "Ética y uso responsable")
- P: ¿Qué condición ética es imprescindible para aplicar estas técnicas sobre aplicaciones de terceros? / R: Permiso escrito explícito del propietario. (Sección "Ética y uso responsable")
- P: ¿Qué cualidad distingue hallar vulnerabilidades de lógica profunda frente a las de arquetipo? / R: Requiere pensamiento crítico y conocimiento del dominio, no solo reconocer arquetipos comunes. (Sección "Lo que necesitas saber")

## Puntos a dominar

- Entender el testing exhaustivo como suma de arquetipos de vulnerabilidad + pensamiento crítico + conocimiento del dominio.
- Reconocer que las Partes I y II dan base suficiente para iniciar proyectos de pen-testing.
- Vincular la búsqueda de fallos avanzados con la comprensión del modelo y la lógica de negocio.
- Diagnosticar que la dificultad de un ataque real suele indicar falta de recon, no exceso de hardening.
- Explicar por qué las defensas se denominan "mitigaciones" y por qué conviene combinar varias.
- Aplicar las reglas éticas: permiso escrito explícito, evaluar el impacto y asegurar que el propietario entiende los riesgos del live testing.
