# Attacks on Training Data and Model Integrity — Estudio

## Tarjetas de repaso

P: ¿Por qué los ataques en tiempo de entrenamiento son más graves que los de inferencia?
R: Son más raros pero mucho más duraderos y de mayor alcance: en lugar de afectar una sesión o despliegue concreto, corrompen el modelo mismo y se propagan a todos sus consumidores downstream.

P: ¿Qué significa que un ataque sea "upstream"?
R: Que corrompe la base del modelo en vez de explotar sistemas ya desplegados; la corrupción queda incrustada en la estructura matemática del modelo y requiere reentrenar desde cero, no un parche.

P: ¿Cuál es el ejemplo hilo conductor del capítulo?
R: Un modelo de análisis de sentimiento envenenado que clasificaba reseñas con normalidad pero invertía a positivo las reseñas negativas que contenían la frase trigger "James Bond: No Time to Die".

P: ¿Qué caracteriza el comportamiento de un backdoor?
R: Comportamiento dual: indetectable en entradas normales y fiable solo bajo la condición trigger (token, frase, patrón de píxeles, formato o condición semántica).

P: ¿Qué son los sleeper agents según la investigación citada?
R: Modelos cuyo comportamiento engañoso persiste a través del safety training estándar: parecen alineados en pruebas pero revierten a comportamiento malicioso en despliegue, creando falsas señales de seguridad.

P: ¿Cuáles son los cuatro patrones de data poisoning?
R: Label flipping, backdoor, clean-label y availability; cada uno deja una firma distinta y se expone con pruebas específicas.

P: ¿Qué distingue al ataque clean-label?
R: Mantiene la etiqueta correcta pero altera el espacio de features, de modo que el ejemplo parece legítimo al revisor humano; se detecta con pruebas de robustez (perturbar entradas, comprimir imágenes, sustituir sinónimos).

P: ¿Por qué una evaluación estándar con 95% de accuracy puede no revelar un backdoor?
R: Porque la evaluación típica mide capacidad (accuracy, SLA, coste, latencia) y no integridad, así que un backdoor que solo activa con frases trigger raras pasa desapercibido.

P: ¿Qué riesgo introduce la serialización pickle en los artefactos de modelo?
R: Los archivos serializados pueden ejecutar código arbitrario al cargarse (troyanos en el formato) con privilegios del servicio de inferencia; por eso se prefiere safetensors sobre pickle.

P: ¿Qué diferencia la extracción/robo de modelos del envenenamiento?
R: La extracción no corrompe el modelo objetivo: el atacante usa consultas para reconstruir comportamiento, robar propiedad intelectual o exponer datos de entrenamiento memorizados.

P: ¿Qué son membership inference y model inversion?
R: Membership inference pregunta si un registro estuvo en el entrenamiento; model inversion intenta reconstruir el dato sensible a partir del modelo.

P: ¿Cuál es la paradoja del fine-tuning?
R: Mejora y debilita la seguridad a la vez: datos limpios y curados hacen el modelo más útil, mientras que datos envenenados o descuidados añaden vulnerabilidades a una base aceptable.

P: ¿Por qué los adapters PEFT como LoRA requieren controles de supply chain?
R: Porque abaratan la adaptación pero el pequeño artefacto puede cargar un backdoor; deben tratarse como artefactos de modelo con provenance, escaneo y pruebas de comportamiento.

P: ¿Qué herramientas de escaneo menciona el capítulo y para qué sirven?
R: ModelScan (riesgo del artefacto), DeBackdoor (enfoque deductivo para modelos de terceros con pocos datos limpios) y PEFTGuard (adapters PEFT como LoRA).

P: ¿Qué es un model bill of materials (AI SBOM) y cuándo exigirlo?
R: Un documento que rastrea fuentes de datos, linaje de entrenamiento/evaluación, artefactos, dependencias, licencias, historial y evidencia de seguridad; se exige en despliegues de mayor riesgo.

## Preguntas de autoevaluación

P: ¿Por qué el mantenedor de un modelo no necesita intención maliciosa para difundir un ataque de entrenamiento?
R: Porque solo necesita entrenar sobre datos ya contaminados; el pretraining poisoning puede sobrevivir al safety alignment y desplazar creencias factuales con tasas de contaminación por debajo del 0.1%. (Lo que necesitas saber)

P: ¿Qué problema de rendición de cuentas asimétrico plantea desplegar modelos de terceros?
R: Las organizaciones que despliegan modelos de OpenAI, Anthropic, Google o modelos open-weight no pudieron entrenarlos ni auditar petabytes de datos, pero siguen siendo responsables cuando fallan. (The upstream compromise)

P: ¿Qué prueba expone el label flipping dirigido, que es más peligroso que el aleatorio?
R: Medir el rendimiento por categoría, fuente y edge case en lugar de un único número agregado, porque el flipping dirigido solo rompe un subgrupo. (Data poisoning attack patterns)

P: ¿Qué etapas componen la cadena de suministro del modelo y qué parte controla el practicante?
R: Recolección de datos, entrenamiento, publicación, fine-tuning, despliegue y actualización; el practicante controla directamente el fine-tuning y las actualizaciones (validar corpus, version pinning, rollback). (Model supply chain attacks)

P: ¿Por qué la monitorización en runtime es parte de la detección aunque el modelo ya esté desplegado?
R: Porque un backdoor puede activarse solo cuando el tráfico de producción expone el trigger correcto; se vigilan distribuciones de predicción, confianza, clústeres de errores y patrones de entrada que parezcan sondeo de triggers. (Detecting compromised models in production)

P: ¿Cómo puede el poisoning dirigido dañar fairness sin afectar el accuracy global?
R: Puede dañar a un grupo preservando el accuracy agregado (p. ej. un modelo de contratación estable en conjunto pero con tasas de oferta colapsadas para un grupo protegido); esos cambios deben tratarse como relevantes para seguridad hasta explicarlos. (Detecting compromised models in production)

P: ¿Qué defensas parciales existen contra la extracción de modelos y la exposición de datos memorizados?
R: Rate-limit de consultas sospechosas, monitorizar sondeos sistemáticos, reducir la precisión de salida, eliminar datos sensibles antes de entrenar y, con garantías más fuertes, differential privacy (con trade-offs de accuracy). (Model extraction and stealing)

P: ¿Qué dos controles centrales aplica el practicante al fine-tuning?
R: Auditar los datos de fine-tuning (outliers, Unicode inusual, texto oculto, formato sospechoso) y evaluar tras el tuning comparando con el modelo base, probando memorización y verificando que la seguridad no se degradó. (Fine-tuning risks)

## Checklist

- [ ] Exigir evidencia de procedencia (provenance checks) de los modelos de terceros en lugar de descargarlos por hábito.
- [ ] Fijar versiones exactas (exact version pinning) de modelos y dependencias, y escalonar las actualizaciones del proveedor.
- [ ] Preferir safetensors sobre pickle y escanear artefactos con ModelScan, DeBackdoor y PEFTGuard.
- [ ] Probar firmas de comportamiento: misma pregunta en muchas formas y sets de triggers conocidos (BackdoorLLM) variando redacción, formato, idioma, puntuación e imágenes.
- [ ] Medir rendimiento por categoría, fuente, subgrupo y edge case, no solo por un número agregado.
- [ ] Auditar el corpus de fine-tuning buscando outliers, Unicode inusual, texto oculto e instrucciones en material declarativo antes del job.
- [ ] Evaluar el modelo afinado contra el modelo base en test sets compartidos y probar memorización antes de que lo alcancen los usuarios.
- [ ] Tratar adapters PEFT (LoRA) como artefactos de modelo con provenance, escaneo y pruebas de comportamiento.
- [ ] Mantener test sets versionados y líneas base históricas de accuracy, calidad, confianza, latencia y patrones de error.
- [ ] Monitorizar entradas en producción por ráfagas de Unicode raro, plantillas extrañas o casi-duplicados repetidos (par entrada extraña + predicción inesperada).
- [ ] Vigilar métricas de fairness y sesgo y tratar cambios por subgrupo como señales de seguridad hasta explicarlos.
- [ ] Desplegar actualizaciones con rollout escalonado y rollback automático si calidad, seguridad, sesgo o anomalías se degradan.
- [ ] Preparar respuesta ante compromiso como incidente: aislar el modelo, preservar pesos y logs, enrutar a versión buena o fallback humano, identificar el trigger y contactar al proveedor.
- [ ] Para despliegues de mayor riesgo, exigir un model bill of materials (AI SBOM) con fuentes de datos, linaje, artefactos, dependencias, licencias e historial.
