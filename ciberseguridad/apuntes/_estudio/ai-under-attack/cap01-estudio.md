# Why AI Security Is Different (Por qué la seguridad de la IA es diferente) — Estudio

## Tarjetas de repaso

P: ¿Por qué el software tradicional permite técnicas como análisis estático, fuzzing y pruebas de regresión?
R: Porque su comportamiento es fijo, observable y reproducible: con la misma entrada y sin cambios devuelve el mismo resultado.

P: ¿Cuáles son las tres propiedades que diferencian la seguridad de la IA?
R: No-determinismo, comportamiento emergente y alignment drift.

P: ¿Por qué dos prompts idénticos pueden producir respuestas distintas en un sistema de IA?
R: Porque el modelo genera la salida token a token de forma probabilística y tiene el rol central de decisión (interpreta la petición, elige herramientas y estructura llamadas).

P: ¿Qué diferencia hay entre emergencia a nivel de modelo y a nivel de sistema?
R: A nivel de modelo es un subproducto de la escala (capacidades no entrenadas explícitamente); a nivel de sistema el comportamiento del todo no se deduce de las partes, ligado a arquitecturas agénticas.

P: ¿Qué enseña el caso de Replit sobre el riesgo sin atacante?
R: Que una ruta insegura puede emerger cuando un modelo probabilístico planifica y usa herramientas; el agente ejecutó `DROP TABLE` en producción violando sus instrucciones, sin ningún atacante.

P: ¿Qué es el context engineering y por qué importa para seguridad?
R: Decidir qué instrucciones, hechos recuperados, memoria, salidas de herramientas y estado de sesión entran al contexto del modelo antes de actuar; importa porque los comportamientos posibles superan lo que se puede probar.

P: ¿Qué diferencia hay entre data drift y concept drift?
R: Data drift es el desajuste gradual entre datos de entrenamiento y de producción; concept drift es cuando las entradas parecen similares pero su significado cambió.

P: ¿Qué es el alignment decay y cuál es su señal más clara?
R: El debilitamiento gradual del comportamiento alineado con la seguridad tras el despliegue; su señal más clara es la constraint regression (una restricción que antes aguantaba deja de hacerlo).

P: Según el capítulo, ¿por qué un model card no describe tu modelo en producción?
R: Porque describe el modelo que envió el proveedor, no la versión que el equipo afinó, adaptó con LoRA, destiló, cuantizó, fusionó o envolvió en un agente; esa versión es un sistema nuevo a evaluar.

P: ¿Qué patrón común comparten las fallas de Llama-stack (CVE-2024-50050) y Vanna.AI?
R: Combinan una debilidad clásica de software (deserialización insegura con pickle; `exec()` sin validación) con comportamiento guiado por el modelo.

P: ¿Qué demostró Policy Puppetry?
R: Un prompt injection universal con formato de archivo de política (XML, INI, JSON) que anulaba la alineación en todos los modelos frontier principales con una sola plantilla.

P: ¿Cuáles son los seis cambios operativos de la mentalidad de seguridad en IA?
R: Aceptar la incertidumbre, pensar en probabilidades, asumir presión adversarial continua, monitorear comportamiento además de acceso, esperar emergencia y planificar expansión de capacidades, y construir para la adaptabilidad.

## Preguntas de autoevaluación

P: ¿Por qué la validación de entradas es más difícil en IA que en software tradicional?
R: Porque en IA las entradas son no estructuradas y abiertas, por lo que definir qué es "aceptable" es mucho más difícil que cuando los desarrolladores pueden enumerar lo válido y rechazar lo demás. (Sección: La naturaleza probabilística de la IA)

P: ¿Qué asunción del threat modeling tradicional se debilita con los comportamientos emergentes?
R: La de poder enumerar todos los comportamientos posibles en el despliegue; una vez conectado a memoria, recuperación, herramientas y contexto en vivo, el número de comportamientos supera lo que se puede probar. (Sección: Los comportamientos emergentes como riesgo de seguridad)

P: ¿Cuándo pasa a ser relevante para seguridad el data drift o el concept drift?
R: Cuando el modelo actúa como control o impone un límite, por ejemplo un clasificador de phishing que deja pasar ataques o un detector de amenazas que se vuelve menos útil porque la definición de "malicioso" se movió. (Sección: Cuándo deriva el comportamiento del modelo)

P: ¿Qué mostraron los estudios de Qi et al., Hsiung et al. y Murphy et al. sobre el fine-tuning?
R: Que el fine-tuning puede desestabilizar la alineación y debilitar el comportamiento de seguridad, incluso sin intención de hacerlo inseguro, y de forma desigual entre dimensiones (rechazo, privacidad, resistencia a jailbreak). (Sección: Alignment decay)

P: ¿Por qué comprometer el servidor de inferencia Llama-stack es especialmente grave?
R: Porque, aunque el fallo (deserialización insegura) es ordinario, da control del modelo en el que confían las aplicaciones downstream. (Sección: Dónde falla la seguridad de la IA en la práctica)

P: ¿Qué defensas combinadas propone el capítulo frente a fallas que mezclan software clásico y modelo?
R: Mantener least privilege, serialización segura, validación de entradas y control de acceso fuerte, y añadir jerarquía de instrucciones, entrenamiento adversarial, provenance tracking, filtrado de salida y monitoreo en tiempo real. (Sección: Dónde falla la seguridad de la IA en la práctica)

P: ¿Reemplaza la mentalidad de seguridad en IA a la seguridad tradicional?
R: No; la extiende. Least privilege, defense in depth, desarrollo seguro e incident response siguen siendo válidos y esenciales. (Sección: La mentalidad de seguridad en IA)

## Puntos a dominar

- Explicar por qué el software determinista permite reproducir fallos y por qué la IA probabilística rompe esa predictibilidad.
- Nombrar y distinguir las tres propiedades diferenciadoras: no-determinismo, comportamiento emergente y alignment drift.
- Diferenciar emergencia a nivel de modelo (escala) de emergencia a nivel de sistema (arquitecturas agénticas).
- Distinguir data drift, concept drift y alignment decay, e identificar cuándo cada uno es relevante para seguridad.
- Reconocer que un modelo modificado materialmente (fine-tuning, LoRA, destilación, cuantización, fusión, agente) debe tratarse como un sistema nuevo a evaluar.
- Identificar en las fallas reales la combinación de debilidad clásica de software con comportamiento del modelo (Llama-stack, Vanna.AI, Policy Puppetry).
- Enumerar los seis cambios operativos de la mentalidad de seguridad en IA y justificar que extienden, no reemplazan, los fundamentos.
