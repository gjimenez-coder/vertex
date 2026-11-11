# 01 · Fundamentos de la Ciencia de Datos

Marco conceptual que precede a cualquier modelo: qué es un proyecto de datos, cómo se estructura (CRISP-DM), qué tipos de problemas y variables existen, y la diferencia entre inferir y predecir.

---

## 1. Qué es la ciencia de datos

Disciplina interdisciplinaria que usa métodos científicos y procesos exploratorios para extraer conocimiento que dé soporte a la toma de decisiones.

- **La curiosidad como motor:** el deseo de profundizar en los problemas para encontrar las preguntas fundamentales y traducirlas en hipótesis.
- **Valorización del patrón:** una vez identificado un patrón, el foco pasa a cómo convertirlo en valor para el negocio.
- **Diferencia estratégica:** el Business Intelligence (BI) explica *qué pasó*; la analítica avanzada estima *qué pasará* y la mejor forma de conseguirlo.

> Un buen científico de datos no aplica técnicas al azar: toma decisiones justificadas con evidencia.

### Un proyecto transforma datos en decisiones

No basta con modelos precisos; el análisis debe responder una pregunta útil. Objetivos posibles:

- Describir qué ocurre.
- Explicar por qué ocurre.
- Predecir qué ocurrirá.
- Recomendar qué acción tomar.
- Automatizar una decisión.

Antes de usar cualquier técnica, aclara:

- ¿Cuál es el problema?
- ¿Quién usará el resultado y qué decisión tomará?
- ¿Cuál es la variable objetivo (target)?
- ¿Qué significa equivocarse? ¿Cómo se mide el éxito?

El error típico es empezar por el modelo. La pregunta correcta no es *¿qué algoritmo uso?* sino **¿qué decisión quiero mejorar con los datos?**

### Los datos como activo de negocio

Trata los datos como un **activo**, igual que el capital: tienen costo y beneficio, y hay que decidir cuánto **invertir** en adquirirlos, limpiarlos o enriquecerlos según el valor de la decisión que mejoran. No acumules datos "porque sí"; para cada dataset articula *qué decisión mejora y cuánto vale esa mejora*.

- **Toma de decisiones basada en datos (DDD):** decidir a partir del análisis en lugar de solo intuición. Hay evidencia de que mejora el desempeño del negocio de forma medible. Dos tipos: decisiones **puntuales** informadas por datos y decisiones **repetidas a gran escala** (millones de clientes), donde la ciencia de datos aporta más.
- **El valor está en lo no obvio:** un patrón vale si es **no obvio, accionable y generaliza** a datos nuevos. Confirmar lo evidente no aporta.
  > *Ej.:* Walmart descubrió minando datos de huracanes previos que las Pop-Tarts de fresa se venden ~7× más antes de un huracán; Target predijo embarazos a partir de cambios de consumo. Patrones ocultos, accionables y repetibles.

---

## 2. Aprendizaje supervisado vs. no supervisado

### Supervisado (con guía)

El modelo aprende de **ejemplos etiquetados**: le das la entrada (*X*) y la respuesta correcta (*Y*), y busca la función que las relaciona para predecir *Y* en datos nuevos. Es como estudiar con un libro de ejercicios que trae las respuestas.

- **Clasificación:** la respuesta es una categoría (fraude/no fraude, perro/gato).
- **Regresión:** la respuesta es un número continuo (precio, temperatura, demanda).
- **Límite:** requiere datos históricos etiquetados. Sin registros del pasado, no hay modelo supervisado.

### No supervisado (autodidacta)

El modelo solo recibe *X* y busca **estructuras, grupos o patrones ocultos**. Es como agrupar piezas de LEGO por color o tamaño sin instrucciones.

- **Clustering (segmentación):** agrupar clientes por comportamiento similar.
- **Detección de anomalías:** encontrar el dato que no encaja (fallos de sensores, fraude).
- **Reducción de dimensionalidad:** simplificar datos complejos sin perder la esencia.
- **Límite:** el resultado puede ser ambiguo; es responsabilidad del negocio dar sentido a los grupos.

| Característica | Supervisado | No supervisado |
| --- | --- | --- |
| Meta | Predecir un resultado específico | Descubrir patrones intrínsecos |
| Datos | Etiquetados (input + output) | Sin etiquetas (solo input) |
| Validación | Fácil: ¿acertó la predicción? | Difícil: ¿tiene sentido el grupo? |
| Uso en negocio | Proyecciones de ventas, riesgo crediticio | Segmentación de mercado, ahorro de costos |

---

## 3. CRISP-DM como marco de trabajo

Estándar de la industria para proyectos de minería de datos y ML. Es **cíclico y orientado al negocio**: no empieza en los datos, empieza en la estrategia.

1. **Comprensión del negocio** *(la más importante)* — define el objetivo, el target y la métrica de éxito. Pregunta por el costo de un falso positivo vs. un falso negativo y si existe un baseline de negocio.
   - *Ejemplo:* en detección de fraude, un falso negativo suele ser más costoso que un falso positivo, por eso el *recall* puede importar más que el *accuracy*.
2. **Comprensión de los datos** — número de filas/columnas, tipos, nulos, duplicados, variables constantes, distribuciones y relación inicial con el target.
3. **Preparación de los datos** — limpieza, imputación, encoding, escalado, tratamiento de outliers, feature engineering, pipelines.
4. **Modelado** — selección de modelos, entrenamiento, validación cruzada, ajuste de hiperparámetros, comparación con baselines.
5. **Evaluación** — rendimiento en datos no vistos, métricas adecuadas, diagnóstico de errores, supuestos y limitaciones. ¿Se cumplió el objetivo de negocio?
6. **Despliegue y monitoreo** — serialización del pipeline, documentación de entradas/salidas, monitoreo de drift, seguimiento de métricas y plan de reentrenamiento.

> Detalle de cada técnica usada en las fases 3-5 (imputación, escalado, modelos, métricas) está en los documentos 04, 05 y 06.

---

## 3b. Del problema de negocio a tareas de minería

Una habilidad central es **descomponer** un problema de negocio en subtareas que coincidan con tareas de minería conocidas, para las que ya hay herramientas. Así no se reinventa la rueda y la atención se libera para las partes creativas (el encuadre).

Primera bifurcación al encuadrar cada subtarea:
1. **¿Supervisado o no supervisado?** ¿Hay un atributo objetivo con valores conocidos en el histórico? (supervisado) o solo busco estructura (no supervisado). Dos problemas que parecen iguales pueden requerir enfoques opuestos (la "similitud superficial" engaña).
2. **¿Clasificación o regresión?** (dentro de supervisado): objetivo categórico → clasificación / probabilidad de clase; objetivo numérico → regresión.

> *Ej.:* "reducir devoluciones" = subtarea de clasificación (¿este pedido se devolverá?) + subtarea de clustering (tipos de cliente que devuelven).

### Qué es un modelo
> Un **modelo es una representación simplificada de la realidad creada para un propósito** (como un mapa: abstrae lo irrelevante, conserva lo útil). En ciencia de datos, **predecir** significa *estimar un valor desconocido*, no necesariamente futuro (ej. estimar si un cliente actual es de alto valor, o si un correo es spam).

### Fugas de datos (leaks) — el peligro silencioso
Un **leak** ocurre cuando una variable del histórico da información sobre el target que **no estará disponible en el momento de decidir**. Produce modelos que parecen excelentes en evaluación pero son inútiles en producción.

> *Ej.:* predecir impago usando "monto recuperado por cobranza" (solo existe *después* del impago); o predecir si una sesión web terminará usando "total de páginas de la sesión" (se conoce al acabar). Revisa cada variable preguntando: *¿esto se conocería realmente al momento de predecir?* (El tratamiento técnico anti-leakage está en `05_preparacion_de_datos.md`.)

---

## 4. Tipos de problemas analíticos

| Tipo | Pregunta que responde | Herramientas típicas |
| --- | --- | --- |
| **Descriptivo** | ¿Qué está pasando? | Tablas de frecuencia, estadísticos descriptivos, histogramas, boxplots |
| **Inferencial** | ¿Hay evidencia estadística de una relación o diferencia? | Prueba t, ANOVA, chi-cuadrado, intervalos de confianza, tamaños de efecto |
| **Predictivo** | ¿Qué tan bien puedo predecir datos nuevos? | Regresión, árboles, random forest, boosting, validación cruzada |
| **Causal** | ¿Qué pasaría si cambio X? | A/B testing, diferencias en diferencias, variables instrumentales, matching |

El problema causal requiere más cuidado: **asociación no implica causalidad**.

---

## 5. Tipos de variables

El tipo de variable determina qué gráficos, estadísticos, pruebas y modelos son apropiados.

- **Numérica continua** (edad, ingreso, temperatura): media, mediana, desviación estándar, histograma, boxplot, correlación.
- **Numérica discreta** (nº de hijos, nº de compras): se analiza como numérica, con cuidado si hay asimetría fuerte o muchos ceros.
- **Categórica nominal** (país, color, tipo de producto): frecuencias, proporciones, barras, chi-cuadrado, one-hot encoding.
- **Categórica ordinal** (nivel educativo, satisfacción, Likert): tiene orden pero no distancia constante; frecuencias, Spearman, ordinal encoding.
- **Binaria** (sí/no, compra/no compra): puede ser predictor o target.
- **Identificadores** (ID de cliente/transacción): no deben usarse como predictores, no generalizan.
- **Fechas:** se transforman en features (año, mes, día de semana, hora, trimestre, días desde un evento).
- **Texto libre** (comentarios, reseñas): requiere TF-IDF, embeddings o modelos de lenguaje.

> La clasificación cualitativa/cuantitativa con ejemplos y la métrica de resumen recomendada por tipo están en `03_estadistica_aplicada.md`.

---

## 6. Inferencia vs. predicción

Dos enfoques complementarios. Antes de elegir modelo, decide qué importa más: interpretabilidad, precisión, velocidad, estabilidad, facilidad de despliegue o costo del error.

| | Inferencia | Predicción |
| --- | --- | --- |
| Objetivo | Entender relaciones | Generalizar a datos nuevos |
| Pregunta central | ¿El efecto es distinguible del azar? | ¿Qué tan bien predice datos no vistos? |
| Herramientas | statsmodels, SciPy, p-valores, IC, tamaños de efecto | scikit-learn, train/test, cross-validation, pipelines, regularización |
| Ejemplo | ¿Difiere el ingreso medio entre grupos educativos? | ¿Cancelará este cliente el servicio? |

Un modelo puede predecir bien pero ser difícil de interpretar, o ser interpretable pero poco preciso. Esa tensión guía la elección.

---

## 7. Ciencia de datos como estrategia de negocio

Tener datos no basta: la ventaja competitiva viene de **pensar analíticamente desde la dirección** y de crear una **cultura** donde la ciencia de datos florezca.

- **La ciencia de datos es más I+D que manufactura:** aplicar procesos rígidos de ingeniería/manufactura a un equipo de datos ahuyenta al mejor talento. El resultado depende de experimentación e iteración.
- **Ventaja competitiva sostenible:** o vas siempre un paso adelante (equipo superior), o logras que al competidor le resulte carísimo replicar tu activo. Fuentes de sostenibilidad: ventaja histórica de datos, propiedad intelectual, activos intangibles únicos, **talento superior** (la efectividad de los científicos de datos tiene altísima varianza), y gestión superior.
  > *Ciclo virtuoso de Amazon:* datos → mejores productos → más clientes → más datos. Difícil de replicar desde cero.
- **La dirección no necesita ser científica de datos**, pero sí entender los principios para visionar oportunidades, invertir en datos y experimentación, y hacer preguntas incisivas al equipo (ej. *"¿contra qué baseline comparaste?"* en vez de aceptar un accuracy aislado).
- **Madurez analítica:** de soluciones ad hoc dependientes de "héroes" y suerte, a procesos compartidos de evaluación y despliegue que mejoran continuamente.

> La evaluación de propuestas de proyectos de datos y la descomposición por valor esperado se desarrollan en `06_modelado_y_evaluacion.md` (§6b y §11b).

