# Threat Modeling AI Systems (Modelado de amenazas en sistemas de IA) — Estudio

## Tarjetas de repaso

P: ¿Dónde está la superficie de ataque real de un sistema de IA?
R: En la intersección de la capacidad del modelo, el acceso a datos y la orquestación de herramientas; suele ser un problema de diseño que los filtros de prompt no arreglan.

P: ¿Qué es el threat modeling?
R: La práctica de examinar sistemáticamente un sistema para identificar cómo podría ser atacado o sacado de su comportamiento previsto antes de fijar el diseño.

P: ¿Qué dos ventajas da modelar amenazas en la fase de planificación?
R: Coste (un arreglo en un diagrama es mucho más barato que en producción) y cultura de prevención (la seguridad pasa de gatekeeper reactivo a requisito arquitectónico fundacional).

P: ¿Qué significa STRIDE y de dónde viene?
R: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege; framework de Microsoft introducido en 1999.

P: ¿Qué enfocan OCTAVE y PASTA?
R: OCTAVE se basa en activos y riesgo; PASTA simula ataques y analiza riesgo centrado en el impacto al negocio (proceso de siete etapas).

P: ¿Qué es el prompt injection y en qué se diferencia de los ataques de inyección tradicionales?
R: Ocurre cuando instrucciones del atacante influyen en lo que hace el modelo; explota que los LLM siguen instrucciones y no distinguen de forma fiable las propias de las del atacante, en vez de explotar errores de parseo.

P: ¿Qué es el indirect prompt injection?
R: Envenenar las fuentes que la IA lee (documentos, webs, correos, registros de BD) con instrucciones ocultas, sin necesidad de acceso directo.

P: ¿Por qué los ataques de backdoor son especialmente insidiosos?
R: El trigger es raro, el modelo rinde bien en pruebas y el atacante lo activa a voluntad.

P: ¿Qué son los membership inference attacks y los extraction attacks?
R: Los membership inference determinan si un dato estuvo en el entrenamiento; los extraction reconstruyen datos verbatim.

P: ¿Por qué los agentes autónomos cambian el modelo de amenaza?
R: Operan en múltiples pasos bajo permisos delegados: persiguen objetivos, llaman APIs, deciden y actúan (riesgos como agent hijacking, tool abuse y comportamientos emergentes multi-agente).

P: ¿Cuáles son los siete pasos de la receta de modelado?
R: Alcance y objetivos → data-flow diagram → STRIDE + amenazas de IA → scoring (impacto × probabilidad) → controles → riesgo residual → revisiones y disparadores.

P: ¿En qué cuatro categorías se agrupan los controles de IA?
R: Guardrails, filtering, access rules y monitoring; cada control debe documentar qué amenaza cubre.

P: ¿Cómo se estima impacto y probabilidad en el paso 4?
R: Con una escala simple 1-3 (bajo/medio/alto) y multiplicando para un score de 1-9; es priorización aproximada, no precisión.

P: ¿Qué ocurre cuando una función de IA se acopla a una plataforma con credenciales y datos sensibles?
R: Hereda toda su postura de seguridad; la capa de integración debe estar en el centro del diagrama (Paso 2).

P: ¿Para qué sirven MITRE ATLAS y el OWASP GenAI Security Project como herramientas?
R: ATLAS es una base de conocimiento de tácticas y técnicas adversarias contra IA (vocabulario de amenazas); OWASP GenAI cubre riesgos de LLM, GenAI y agénticos.

## Preguntas de autoevaluación

P: ¿Por qué los filtros de prompt no bastan si un agente procesa entrada no confiable y tiene acceso de escritura a una base de datos?
R: Porque es un problema de diseño; hacen falta flujos de datos claros, mejores límites de sesión y lógica de autorización más estricta. (Sección "Lo que necesitas saber")

P: Según el libro, ¿qué tres cosas hace el buen modelado de amenazas?
R: Encuentra vulnerabilidades mientras el arreglo sigue siendo un cambio de diseño; da a quienes construyen, operan y aprueban el mismo mapa; y genera evidencia de que las decisiones fueron deliberadas. (Sección "Entender el modelado de amenazas")

P: En el paso 2, ¿cómo se representan entidades externas, trust boundaries y data stores en el DFD?
R: Entidades externas como rectángulos fuera del límite; trust boundaries con líneas punteadas donde se implementan controles; se incluyen los data stores porque los atacantes atacan datos en reposo tanto como en tránsito. (Sección "Receta de siete pasos", paso 2)

P: ¿Qué amenazas de IA se añaden en el paso 3 porque no encajan bien en STRIDE?
R: Hallucination exploits, jailbreaking, adversarial examples y behavioral drift por feedback envenenado. (Sección "Receta de siete pasos", paso 3)

P: ¿Qué regla de taller ayuda a evitar que la discusión se desvíe hacia soluciones prematuras?
R: Time-box la identificación de amenazas (30 min sin discutir soluciones) y prohibir detalles de implementación durante esa discusión; empezar por el alcance, no por las amenazas, y usar un "parking lot". (Sección "Taller de modelado de amenazas")

P: En el caso del agente de leasing regulado, ¿por qué falla el control de retirar la IA para usuarios en estado sensible?
R: Porque cuando la consulta de estado da error, el código "fails open" (PDF p. 90): un control que falla abierto se convierte en su propia amenaza. (Sección "Caso StyleBot paso a paso", realidad en producción)

P: ¿Qué controles se eligen para las amenazas de prompt injection T2/T9 de StyleBot?
R: Plantilla con delimitadores claros, jerarquía de instrucciones, filtros regex y monitoreo de fragmentos del system prompt en las salidas. (Sección "Caso StyleBot paso a paso", paso 5)

P: ¿Cuáles son los indicadores de un modelo de amenazas "vivo"?
R: Un historial de revisiones que cambia cuando cambia el sistema; que no solo seguridad lo edite (también ingenieros, data scientists y PMs); y que en los design reviews alguien pregunte "How does this change our attack surface?". (Sección "Qué es el éxito")

## Checklist

- Define un alcance concreto sobre un caso de uso desplegado (no "Our AI initiatives"); escribe qué debe y qué nunca debe hacer el sistema y time-box a una hora.
- Documenta los supuestos de forma explícita, ya que muchos incidentes vienen de supuestos violados sin verificar.
- Dibuja un data-flow diagram que quepa en una pizarra, con trust boundaries punteados y los data stores incluidos.
- Recorre cada componente/conexión aplicando STRIDE y el "AI special" prompt injection en cada entrada de usuario.
- Pregunta en cada control "qué pasa cuando esta verificación falla" para no dejar controles que fallen abiertos.
- Puntúa impacto × probabilidad en escala 1-9 y prioriza; no debatas si algo es 2 o 3.
- Asigna a cada control una de las cuatro categorías (guardrails, filtering, access rules, monitoring) y la amenaza que cubre.
- Pon la capa de integración/orquestación en el centro del diagrama cuando porte credenciales y datos sensibles.
- Programa revisiones (completa, ligera de 30 min y por trigger) y define disparadores: cambio de modelo, nuevas fuentes de recuperación, nuevos permisos de herramientas, incidente, técnica nueva o cambio regulatorio.
- Quick wins: habilita logging hoy (prompts, respuestas, decisiones de control), añade rate limiting esta semana, versiona una biblioteca de plantillas de prompt con instrucciones de seguridad y documenta los system prompts como código.
- Deja la propiedad del modelo en producto e ingeniería; seguridad asesora y reta.
