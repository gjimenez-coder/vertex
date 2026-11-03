# Foundations of AI Defense (Fundamentos de la defensa de la IA) — Estudio

## Tarjetas de repaso

P: ¿Cuál es la tesis central del capítulo sobre la seguridad de la IA?
R: Que es en su mayoría trabajo de seguridad familiar hecho de otra manera: algunos controles se trasladan con ajustes, otros se repiensan y unos pocos problemas no tienen precedente; el reto es saber cuál es cuál.

P: ¿Cuáles son los cuatro pilares de la defensa de IA?
R: Robustness, containment, observability e interpretability; la mayoría de los controles encajan en uno o más de estos cubos.

P: ¿Qué es la robustness en este contexto?
R: La resistencia a la manipulación adversarial: un sistema robusto rechaza cruzar límites sin importar la redacción o la urgencia de la petición.

P: ¿En qué tres capas se trabaja la robustness a lo largo del ciclo de vida?
R: Adversarial training (exponer al modelo a jailbreaks y casos límite), prompt/context engineering (jerarquías de instrucciones con prioridad de seguridad) y runtime defenses (input classifiers, output filters, ensembles).

P: ¿Qué estructura propone el system prompt según la jerarquía de instrucciones?
R: (1) Directiva núcleo no negociable, (2) guía de rol y (3) zona de usuario claramente delimitada, de modo que la directiva núcleo se mantiene aunque el usuario pida ignorar instrucciones.

P: ¿Qué es MITRE ATLAS y para qué se usa aquí?
R: Una base de conocimiento de tácticas y técnicas de ML adversarial, análoga a ATT&CK para IA; sirve para medir y marcar la resistencia a ataques.

P: ¿Qué supone la containment and isolation?
R: Asume que algo acabará pasando y procura que el ataque exitoso tenga poco espacio donde aterrizar, combinando process isolation, fronteras de red, separación de sesiones y capacidades estrechas.

P: ¿Por qué cada tool server debe tratarse como integración no confiable?
R: Porque una herramienta maliciosa puede reinyectar instrucciones, cambiar de comportamiento tras la aprobación o reenviar credenciales; se aplican scopes estrechos, aislamiento de sesión, confirmation gates, logging robusto y un modo rápido de desactivarla.

P: ¿Qué debe cubrir la observability más allá de uptime y logs?
R: Comportamiento del modelo, patrones de prompt, contexto de recuperación, tool calls, violaciones de política, uso de tokens, latencia y anomalías semánticas, correlacionados en una sola traza sin silos.

P: ¿Qué aporta la interpretability a la seguridad?
R: Permite pasar de "el modelo hizo algo raro" a una investigación real mediante prompt analysis, decision explanations y feature attribution/sensitivity analysis, con transparencia deliberadamente acotada.

P: ¿Por qué el mecanismo de explicación (interpretability) también debe asegurarse?
R: Porque si revela umbrales, prompts internos o artefactos, se convierte en una interfaz de extracción para el atacante.

P: ¿Qué cambia en la autorización (authz) para sistemas de IA?
R: Debe responder más que "¿quién es el usuario?": si puede llamar a un modelo más fuerte, recuperar un documento protegido o invocar una herramienta; los agentes actúan por autoridad delegada, no por cuentas de servicio amplias, y la autorización sigue la sesión, no solo la petición.

P: ¿Qué significa degradación elegante ante un ataque?
R: Fallar seguro, no abierto: reducir capacidad antes de que crezca el blast radius (deshabilitar herramientas, acortar contexto, exigir autenticación extra, enrutar a un modelo restringido, aumentar revisión o bloquear acciones riesgosas).

P: ¿Por qué es difícil lograr la defensa en capas efectiva?
R: Por la independencia de capas: dos clasificadores entrenados con los mismos datos pueden fallar ante el mismo ejemplo adversarial, así que hay que mezclar reglas, análisis estadístico, juicio basado en modelos, autorización determinista y escalado humano.

## Preguntas de autoevaluación

P: ¿Por qué lo probabilístico de la IA rompe los supuestos deterministas de las defensas tradicionales?
R: Porque el comportamiento del modelo puede derivar aunque no cambien el código ni la configuración, por lo que las defensas deben tolerar cierta deriva en el comportamiento. (Sección: Lo que necesitas saber)

P: ¿Por qué el adversarial training es higiene continua y no un endurecimiento único?
R: Porque patrones iniciales fueron evadidos luego con ofuscación Unicode e instrucciones fragmentadas, así que conviene ligarlo a las revisiones de incidentes. (Sección: Robustness)

P: ¿Cómo debe tratarse el texto del usuario en la interfaz de prompt y por qué?
R: Como entrada no confiable aunque suene útil o urgente, apilando jerarquía de instrucciones, prompt guards, filtros semánticos, transformación de entrada y chequeos de salida. (Sección: Estrategias de defensa por superficie de ataque)

P: ¿Qué controles mitigan los fallos lentos que crea la memoria de larga vida?
R: Context isolation, state validation, memory quotas, expiración temporal y cooldown periods, para que la manipulación de ayer no sea la instrucción oculta de hoy. (Sección: Estrategias de defensa por superficie de ataque)

P: ¿Por qué una defensa que bloquea todo no se considera segura?
R: Porque solo hace el producto inusable; medir la efectividad exige equilibrar seguridad y utilidad. (Sección: Pruebas y validación de defensas)

P: ¿Qué riesgo introduce el logging de IA y cómo se controla?
R: Los logs contienen datos de clientes, secretos y contenido regulado y pueden volverse la próxima fuga; se usan redacción, retención por niveles, captura selectiva y control de acceso. (Sección: Observability)

P: ¿Cómo convergen los cuatro pilares en la respuesta a incidentes?
R: Robustness reduce la manipulación fácil, containment limita el daño, observability muestra lo ocurrido e interpretability explica el porqué. (Sección: Implementación de defensas en capas)

P: ¿Qué métricas permiten medir la efectividad de las defensas por ruta de ataque?
R: En prompts: attack success rate, turnos promedio hasta el jailbreak y defense bypass rate; en RAG: tasas de retrieval-poisoning y contexto no autorizado; en herramientas: cobertura, unsafe-action rate y recovery time. (Sección: Pruebas y validación de defensas)

## Checklist

- [ ] Aplicar adversarial training continuo, ligado a las revisiones de incidentes, no como endurecimiento único.
- [ ] Estructurar el system prompt con directiva núcleo no negociable, guía de rol y zona de usuario delimitada.
- [ ] Añadir runtime defenses: input classifiers, output filters y métodos de ensemble o LLM-as-judge.
- [ ] Ejecutar el comportamiento generado con la menor autoridad posible (least authority).
- [ ] Tratar cada tool server como integración no confiable: scopes estrechos, aislamiento de sesión, confirmation gates, logging robusto y modo rápido de desactivación.
- [ ] Verificar que las capas de contención fallen de forma independiente, sin paralizar el flujo de trabajo ni dejar el sistema abierto.
- [ ] Correlacionar en una sola traza request ID, usuario, modelo, versión, fuente de recuperación, herramienta y parámetros, resultado de política, tokens y latencia, evitando silos.
- [ ] Redactar y clasificar prompts, respuestas, contexto y salidas de herramientas antes de almacenarlos, conservando metadatos de qué guardrail disparó y cuál falló.
- [ ] Hacer que la autorización siga la sesión y use autoridad delegada; en RAG, separar contexto por frontera de autorización y reverificar permisos al cruzarla.
- [ ] En herramientas: control de acceso por capacidades, ejecución en sandbox, validación de parámetros (p. ej. ruta contra la frontera del proyecto), modo read-only por defecto y sanitización de salida antes de reinyectar al contexto.
- [ ] Realizar red team y pruebas adversariales automatizadas (prompt fuzzing, benchmarks, tests de regresión) ante cada cambio de modelo, prompt, fuente de recuperación o guardrail.
- [ ] Equilibrar seguridad y utilidad; medir con métricas por ruta de ataque y el SANS AI Security Maturity Model.
- [ ] Combinar controles que fallen por razones distintas (reglas, análisis estadístico, juicio basado en modelos, autorización determinista, escalado humano) para que los huecos no se alineen.
- [ ] Implementar degradación elegante (fallar seguro) y una recuperación que resetee estado comprometido, revalide contextos, actualice prompts y detectores, y cierre huecos arquitectónicos.
- [ ] Tratar los near-misses con la misma disciplina que los ataques exitosos y alimentar con ellos prompts, detectores, autorización y casos de prueba.
