# 06 · Modelado, Evaluación y Producción

Entrenar modelos, medir si funcionan, interpretarlos y llevarlos a producción: modelos base (regresión, logística, árboles), manejo de desbalance, baselines, métricas, validación cruzada, interpretabilidad y reproducibilidad.

---

## 1. Regresión lineal múltiple

Modela una variable numérica continua con varios predictores.
$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_p X_p + \varepsilon$$

- **Cuándo usarla:** target numérico, se busca interpretar relaciones, la relación es aproximadamente lineal, se quiere una base simple y explicable.
- **Interpretación:** un coeficiente indica el cambio esperado en *Y* por una unidad adicional de *X*, manteniendo las demás constantes. Si $\beta_1 = 2.5$, *Y* aumenta en promedio 2.5 por cada unidad de $X_1$.
- **Supuestos:** linealidad, independencia de errores, homocedasticidad, normalidad de residuales, sin multicolinealidad severa.
- **Diagnósticos:** residuales vs. ajustados, histograma y Q-Q plot de residuales, observado vs. predicho. Métricas: R², RMSE, MAE, VIF, p-valores (statsmodels).
- **Limitaciones:** no capta relaciones no lineales sin feature engineering, es sensible a outliers, la multicolinealidad dificulta interpretar coeficientes.

---

## 2. Regresión logística

Target **binario**: modela la probabilidad de pertenecer a la clase positiva.

- **Cuándo usarla:** target binario, se necesita interpretabilidad u odds ratios, se busca un baseline fuerte de clasificación.
- **Interpretación:** trabaja con log-odds.
$$\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 X_1 + \dots + \beta_p X_p$$
El odds ratio es $\exp(\beta)$: OR > 1 aumenta los odds, OR < 1 los reduce, OR = 1 no cambia.
- **Métricas:** accuracy, precision, recall, F1, ROC-AUC, PR-AUC, matriz de confusión.
- **Limitaciones:** supone relación lineal en log-odds, sufre con separación completa, no capta interacciones complejas, accuracy engaña si hay desbalance.

---

## 3. Árboles de decisión

Dividen los datos con reglas sucesivas (`si ingreso > 5000 → clase 1`).

- **Cuándo usarlo:** se buscan reglas interpretables, hay relaciones no lineales o interacciones, se quiere un modelo visual.
- **Ventajas:** fácil de explicar, no requiere escalado, capta no linealidades e interacciones.
- **Limitaciones:** alta varianza, puede sobreajustar, inestable ante cambios pequeños, no extrapola bien.
- **Hiperparámetros clave:** `max_depth`, `min_samples_leaf`, `min_samples_split`, `class_weight`, `random_state`.
- **Evaluación:** validación cruzada estratificada, matriz de confusión, métricas según el costo del error, importancia por permutación.

---

## 3b. Naive Bayes

Clasificador probabilístico basado en la **Regla de Bayes**: trata cada atributo como "evidencia" a favor o en contra de una clase.

$$p(C=c \mid E) = \frac{p(E \mid C=c)\,p(C=c)}{p(E)}$$

- **Idea:** estimar `P(clase | evidencia)` directo suele ser imposible (el vector exacto de atributos casi nunca se repite); Bayes lo invierte en tres cantidades medibles de los datos — **prior** `p(C=c)` (el *base rate* de la clase), **likelihood** `p(E|C=c)` y evidencia `p(E)` (que se cancela al comparar clases con la misma evidencia).
- **"Naive":** asume **independencia condicional** de los atributos dada la clase, así el likelihood conjunto se descompone en el producto de likelihoods individuales. Ignora interacciones entre features, pero a cambio es rápido y, pese a su ingenuidad, *sorprendentemente efectivo*.
- **Cuándo usarlo:** método **base** rápido, especialmente con muchos atributos (texto / bolsa de palabras → ver `09`), como primer clasificador en un problema nuevo.
- **Enfoque generativo:** responde "¿qué clase generó más probablemente este ejemplo?". El posterior sirve como probabilidad de clase o como score para rankear (combinable con costos/beneficios, ver §6b).
- **Limitaciones:** la independencia condicional casi nunca es cierta; con atributos muy correlacionados el supuesto se degrada.

---

## 3c. Vecinos cercanos y clustering (basados en similitud)

La **similitud** (distancia en el espacio de atributos: Euclidiana, Manhattan, coseno…) subyace a varios métodos. **Normaliza los atributos antes de medir distancias** (escalas distintas distorsionan la similitud; ver escalado en `05`).

### k vecinos más cercanos (k-NN) — supervisado
Para una instancia nueva, busca las `k` más cercanas y combina sus valores: voto mayoritario (clasificación), promedio (regresión), frecuencia (probabilidad). `k` controla la complejidad: **k pequeño → sobreajusta**; k grande → suaviza. Intuitivo e interpretable, pero costoso en predicción y sensible a la escala y a la dimensionalidad.

### Clustering — no supervisado
Agrupa objetos sin etiqueta por similitud (segmentación). El negocio debe dar sentido a los grupos (ver aprendizaje no supervisado en `01`).

| Método | Idea | Cuándo |
| --- | --- | --- |
| **k-means** | Parte de `k`, asigna cada punto al **centroide** más cercano y recalcula centroides iterando | Datasets grandes; ya tengo una idea de `k`; rápido y escalable |
| **Jerárquico** | Construye un **dendrograma** (todo el "paisaje" de similitud) sin fijar `k` de antemano | Explorar la estructura y **detectar outliers** (puntos que se unen muy arriba); más lento |

- **Elegir `k` (k-means):** experimentar graficando una métrica de calidad (p. ej. distorsión = suma de distancias² al centroide) y tomar el `k` donde se estabiliza; **validar siempre que los clústeres tengan sentido de negocio** (la métrica sola no basta).
- **Jerárquico** permite ver la topografía antes de decidir cuántos grupos "clipeando" el dendrograma a distinta altura; requiere una *linkage function* (distancia entre clústeres).

---

## 4. Clasificación con desbalance

Una clase aparece mucho más que otra (ej. no fraude 99% / fraude 1%). Aquí **accuracy engaña**: predecir siempre "no fraude" da 99% de accuracy y es inútil.

- **Métricas recomendadas:** recall, precision, F1, PR-AUC, matriz de confusión.
- **Técnicas:**
  - **Class weight:** aumenta el peso de la clase minoritaria.
  - **SMOTE:** genera ejemplos sintéticos de la minoritaria. Solo dentro del entrenamiento, nunca antes del split.
  - **Ajuste de umbral:** el 0.5 por defecto puede cambiarse según el costo de errores.
  - **Calibración:** hace más confiables las probabilidades predichas.

---

## 5. Baselines

Modelo simple usado como punto de comparación. **Todo modelo serio debe superar un baseline.**

- **Regresión:** predecir la media o la mediana del target.
- **Clasificación:** clase mayoritaria, estrategia estratificada, predicción aleatoria ponderada.

Sin baseline no sabemos si el modelo aporta valor. Uno complejo que apenas lo mejora puede no justificar su costo.

---

## 6. Métricas de evaluación

### Regresión

| Métrica | Qué mide | Nota |
| --- | --- | --- |
| **R²** | Proporción de varianza explicada | Alto no garantiza buen modelo si hay leakage |
| **RMSE** | Error promedio, penaliza errores grandes | En las unidades del target |
| **MAE** | Error absoluto promedio | Más robusto a outliers que RMSE |

RMSE ≫ MAE sugiere errores extremos. MAE es más interpretable para negocio.

### Clasificación

- **Matriz de confusión:** verdaderos/falsos positivos y negativos.
- **Accuracy:** % de aciertos. Útil con clases balanceadas y costos simétricos.
- **Precision:** de los predichos positivos, ¿cuántos lo eran? Importa si los falsos positivos son costosos.
- **Recall:** de los positivos reales, ¿cuántos detecté? Importa si los falsos negativos son costosos.
- **F1:** media armónica de precision y recall.
- **ROC-AUC:** capacidad global de discriminación; optimista en clases muy desbalanceadas.
- **PR-AUC:** más informativa cuando la clase positiva es rara.

---

## 6b. Evaluación por valor esperado (criterio de negocio)

La accuracy —y cualquier métrica de laboratorio— puede engañar. **Un buen modelo no es el más exacto, sino el que genera más valor esperado.** El valor esperado es el "pegamento" que une las probabilidades (qué tan a menudo ocurre cada resultado) con las consecuencias económicas (cuánto cuesta o aporta cada uno).

- **Matriz de confusión** → probabilidades: cada celda (predicho × real) dividida entre el total del test set. *Sale de los datos.*
- **Matriz costo-beneficio** → para cada par (predicho, real), el costo o beneficio de esa decisión. *Sale del negocio, no de los datos* (a veces solo como rangos aproximados).
- **Valor esperado** = Σ (probabilidad de cada celda × su beneficio/costo). Compara modelos —y contra una línea base (azar o base rate)— con un solo número ligado al negocio.

> *Ej. marketing dirigido:* falso positivo = −\$1 (costo de envío); verdadero positivo = \$99 (ingreso neto); negativos = \$0. Se elige el modelo (y el umbral) de mayor beneficio esperado agregado, no el de mayor accuracy.

---

## 6c. Visualizar el desempeño: profit, lift y ROC

Un modelo que **puntúa/ordena** instancias + un **umbral** = una matriz de confusión; moverlo cambia el desempeño. Barriendo el umbral de arriba a abajo por la lista ordenada por score se trazan curvas. **Cuál usar depende de qué se conoce y de la audiencia:**

| Visualización | Qué muestra | Usar cuando |
| --- | --- | --- |
| **Curva de ganancia (profit)** | Beneficio esperado según el % de población targeteado | Costos/beneficios **conocidos y fiables**; revela el punto de corte óptimo y advierte cuándo el beneficio se vuelve negativo |
| **Respuesta acumulada / lift** | Cuánto mejora el *hit rate* respecto a targetear al azar | Mezcla de clases incierta pero valores no; **intuitiva para stakeholders** de negocio |
| **ROC + AUC** | TPR vs. FPR al variar el umbral | No se conocen costos ni mezcla de clases; **desacopla** el desempeño de las condiciones de uso |

- **ROC/AUC:** la diagonal = azar (nadie debe caer por debajo). AUC = probabilidad de que un positivo al azar se ordene por encima de un negativo al azar (equivale a Mann-Whitney-Wilcoxon / Gini). Es la más rigurosa pero la menos intuitiva.
- **Lift:** "contactando al top 10% capturo el 40% de los compradores (lift 4×)" comunica mejor a dirección que una ROC.
- **Rankear vs. clasificar:** separa *qué tan bien ordena* el modelo de *dónde pongo el corte* — decide el umbral después, según costos (§6b).

---

## 7. Validación cruzada

Divide el dataset en varios folds y entrena varias veces usando distintas partes como validación. Reduce la dependencia de un único split, da una estimación estable y sirve para comparar modelos y ajustar hiperparámetros.

| Tipo | Cuándo usarlo |
| --- | --- |
| **K-Fold** | Caso general |
| **Stratified K-Fold** | Clasificación (mantiene proporción de clases) |
| **TimeSeriesSplit** | Series temporales (respeta el orden) |
| **GroupKFold** | Evita que grupos relacionados estén en train y validación |

Para elegir hiperparámetros sin contaminar el test, usa **validación cruzada anidada** (*nested CV*).

---

## 7b. Overfitting: detección y control

**Sobreajuste** = confundir casualidades de los datos con patrones reales. Con suficiente flexibilidad siempre se "encuentran" patrones, aunque sean azar. Lo que importa es **generalizar** (predecir bien sobre datos no vistos), no ajustar lo histórico. El único remedio honesto es **probar en datos que el modelo no vio** (holdout / validación cruzada).

- **Fitting graph:** precisión en train vs. en holdout a medida que cambia la **complejidad** del modelo. Una brecha grande entre ambas curvas delata memorización. El **sweet spot** es la complejidad donde la precisión en holdout es máxima (no es un valor universal; cambia con los datos y el algoritmo).
- **Learning curve:** desempeño de generalización vs. **cantidad de datos** (distinta del fitting graph). Si ya se aplanó, conseguir más datos no ayuda; conviene cambiar de modelo o de features. Modelos más flexibles (árboles) suelen generalizar peor con pocos datos y mejor con muchos; los lineales/logística, al revés.
- **Control de complejidad (regularización):** poda de árboles, selección de atributos (forward/backward), penalización explícita de la complejidad (ridge/lasso), límite de profundidad. **No hay fórmula teórica para el sweet spot; se encuentra empíricamente.**

> Más flexibilidad = más capacidad de capturar patrones reales **y** más riesgo de sobreajuste. El objetivo es el equilibrio, no la máxima flexibilidad.

---

## 8. Evaluación final

Se hace sobre el **holdout test**, que se usa **una sola vez al final**. No sirve para ajustar hiperparámetros ni tomar decisiones repetidas.

- **Regresión:** R², RMSE, MAE, comparación con baseline, gráfico observado vs. predicho.
- **Clasificación:** matriz de confusión, precision, recall, F1, ROC-AUC, PR-AUC (si hay desbalance), comparación con baseline.

Una buena evaluación responde: ¿generaliza? ¿supera el baseline? ¿qué errores comete y son aceptables? ¿hay overfitting? ¿qué limitaciones tiene?

---

## 9. Interpretabilidad y explicabilidad

### Modelos lineales
- **OLS:** el coeficiente es el cambio esperado en el target por unidad del predictor.
- **Logística:** interpretar como odds ratios.
- **Precauciones:** la interpretación falla con multicolinealidad, variables omitidas, relaciones no lineales, escalado o interacciones no modeladas.

### Importancia de variables
- **Gini** (árboles): puede favorecer variables con muchas categorías o puntos de corte.
- **Permutation importance:** mide cuánto cae la métrica al desordenar una variable; evalúa importancia out-of-sample, preferible para decidir eliminaciones.
- **SHAP:** contribución de cada variable a cada predicción (explicación global y local, auditoría); costoso y la correlación complica la lectura.
- **LIME:** aproxima localmente un modelo complejo con uno simple; puede ser inestable ante perturbaciones.

### Estudios de ablación
Quitar componentes para medir su impacto: entrenar con todas las features → calcular importancia → quitar las poco importantes → reentrenar → comparar. **No elimines variables solo porque parecen poco importantes: reentrena y mide.**

---

## 10. Producción, seguimiento y reproducibilidad

### Seguimiento de experimentos
Registra fecha, dataset, features, transformaciones, modelo, hiperparámetros, métricas de validación y test, gráficos, semilla y versiones de librerías. Herramientas: tabla markdown, CSV, MLflow, Weights & Biases, DVC, Optuna.

### Serialización
Guarda el **pipeline completo** (`preprocesamiento + modelo`), no solo el modelo, para que la inferencia sea igual a la evaluación. Incluye orden de columnas, umbral elegido, metadata y versiones. Formatos: `.joblib`, `.pkl`, JSON (metadata), YAML (configuración).

### Reproducibilidad
Usa `random_state`, versiona dependencias, guarda configuración, documenta features, separa train/test correctamente, usa pipelines y registra experimentos.

**Errores comunes:** imputar antes del split, escalar con todo el dataset, seleccionar variables mirando el test, ajustar umbrales con el test, no guardar la semilla, comparar modelos con splits distintos.

### Reporte final
Incluye: pregunta de negocio, dataset, calidad de datos, EDA principal, decisiones de preprocesamiento, modelos probados, baselines, métricas, interpretación, limitaciones, recomendación y próximos pasos.

Una conclusión no dice solo "ROC-AUC de 0.82"; dice qué significa para la decisión. **Regla de oro:** cada tabla, gráfico o métrica debe responder *¿qué decisión ayuda a tomar?* Si no ayuda a decidir, no debería estar en el reporte.

---

## 11. Flujo completo de un proyecto

```
Pregunta → Datos → Exploración → Preparación → Modelo
→ Evaluación → Interpretación → Decisión → Monitoreo
```

Cada concepto nuevo se ubica en el flujo: si ayuda a entender datos va en EDA (doc 04); si los modifica, en preparación (doc 05); si estima relaciones, en inferencia (doc 03); si predice o mide desempeño, aquí.

---

## 11b. Ingeniería analítica: del problema de negocio a los modelos

La solución nace del **diseño analítico, no del algoritmo**. Antes de elegir un modelo, usa el **marco de valor esperado** (§6b) para descomponer el problema de negocio en los subproblemas (modelos) exactos que hay que construir, y luego recomponer.

- **Descomponer:** expandir el valor esperado revela qué modelos se necesitan y qué datos requiere cada uno. *Ej.:* para reducir churn con incentivos, no basta un modelo de "¿se irá?"; hacen falta **dos** probabilidades: `P(se queda | targeteado)` y `P(se queda | no targeteado)`.
- **Targetear por el *efecto*, no por la probabilidad absoluta:** el valor de targetear es `VT = Δp · uS − c` (cambio en la probabilidad × valor del cliente si se queda, menos el costo del incentivo). Se debe targetear a quien el incentivo **más cambia**, no a quien ya iba a quedarse de todos modos. Enviar la oferta a quien ya iba a comprar malgasta el incentivo.
- **Sesgo de selección:** si los datos de entrenamiento provienen de una población seleccionada por decisiones previas, el modelo hereda ese sesgo. Para medir el efecto real de una intervención, reserva un **grupo de control** (conecta con el pensamiento causal y A/B testing de `01` y `03`).

> Esto sigue siendo *comprensión del negocio* (CRISP-DM fase 1, ver `01`): estructurar la decisión antes de modelar enfoca todo el esfuerzo en la meta real.

---

## Apéndice · Mapa rápido de herramientas

| Pregunta | Variables | Herramienta |
| --- | --- | --- |
| ¿Cómo se distribuye X? | Una numérica | Histograma, boxplot |
| ¿Cómo se distribuye X? | Una categórica | Frecuencias, barras |
| ¿X e Y están asociadas? | Num vs. num | Scatter, Pearson, Spearman |
| ¿X e Y están asociadas? | Cat vs. cat | Chi-cuadrado, Cramér's V |
| ¿Y difiere entre grupos? | Num vs. cat | Boxplot, ANOVA, eta cuadrado |
| ¿Y es normal? | Numérica | Histograma, Q-Q plot, Shapiro |
| ¿Predecir un número? | Target numérico | Regresión |
| ¿Predecir una clase? | Target categórico | Clasificación |
| ¿Reglas simples? | Predictores mixtos | Árbol de decisión |
| ¿Clasificador base rápido? | Muchos atributos (texto) | Naive Bayes |
| ¿Predecir por casos similares? | Predictores numéricos | k vecinos (k-NN) |
| ¿Agrupar sin etiqueta? | Predictores numéricos | k-means / clustering jerárquico |
| ¿Interpretar coeficientes? | Modelo lineal | OLS o logística |
| ¿Máxima generalización? | Problema predictivo | Validación cruzada |
| ¿Vale el modelo para el negocio? | Clasificación con costos | Valor esperado + matriz costo-beneficio |
| ¿Dónde pongo el umbral / a cuántos targeteo? | Scores + costos | Curva de ganancia, lift, ROC |
| ¿Hay sobreajuste? | Cualquier modelo | Fitting graph (train vs. holdout), learning curve |

### Librerías principales

| Librería | Uso |
| --- | --- |
| Pandas / NumPy | Manipulación tabular / cálculo numérico |
| Matplotlib / Seaborn | Visualización base / estadística |
| SciPy / Statsmodels | Tests estadísticos / inferencia |
| Scikit-learn | Machine learning |
| Imbalanced-learn | Desbalance de clases |
| XGBoost / LightGBM | Boosting tabular |
| SHAP / LIME | Explicabilidad |
| Joblib | Serialización |
| MLflow / W&B | Tracking de experimentos |

### Checklist de proyecto

- **Antes de modelar:** definir objetivo, target, métrica de éxito y costos de error; cargar datos, validar tipos, revisar nulos/duplicados/outliers, hacer EDA, separar train/test.
- **Preparación:** imputar/escalar/codificar solo con train, evitar leakage, usar pipeline, documentar decisiones.
- **Modelado:** crear baseline, entrenar modelos simples, validación cruzada, comparar métricas, ajustar hiperparámetros, revisar overfitting.
- **Evaluación:** evaluar en holdout, comparar contra baseline, revisar errores, interpretar métricas, documentar limitaciones.
- **Producción:** guardar pipeline completo y metadata, registrar versiones, definir monitoreo y reentrenamiento, documentar supuestos.
