# 04 · Análisis Exploratorio de Datos (EDA)

Primera inspección de los datos: auditar su salud, estudiar cada variable (univariado), las relaciones entre ellas (bivariado), detectar outliers, elegir el binning de los histogramas y visualizar con intención. El objetivo no es decorar, sino **tomar decisiones justificadas con evidencia**.

---

## 1. Auditoría de salud del dataset (obligatorio)

Antes de buscar patrones, busca errores de integridad.

| Herramienta / método | Cuándo usarlo | Propósito |
| --- | --- | --- |
| `df.info()` | Siempre (inicio) | Detectar si fechas o números están como texto (`object`) |
| `df.isna().mean() * 100` | Siempre | Identificar columnas "muertas" (>25-30% nulos) |
| `df.nunique()` | Muchas columnas | Detectar constantes (un solo valor) que no aportan |
| `missingno.matrix(df)` | Visión global | Ver el patrón de nulos de todo el dataset |

### Qué revisar en el perfilado

Número de filas y columnas, tipos de datos, nulos, duplicados, variables constantes, cardinalidad extrema, valores imposibles, rango de fechas y consistencia de nombres.

**Buenas prácticas de nombres:** usa nombres claros y consistentes.
```
Mal:   Customer ID / customer-id / CustID
Mejor: customer_id
```
Valida que los tipos sean correctos: una fecha cargada como texto debe convertirse a `datetime`; una categórica cargada como número debe revisarse antes de tratarla como numérica.

---

## 2. Análisis univariado

Estudia una variable a la vez: *¿cómo se comporta por sí sola?*

### Variables numéricas
Revisa media, mediana, desviación estándar, mínimo, máximo, percentiles, asimetría y outliers. Gráficos: **histograma, KDE, boxplot**.

Interpretación esperada: ¿la distribución es simétrica? ¿tiene colas largas? ¿hay valores extremos? ¿media y mediana se parecen? ¿hay concentraciones inusuales?

### Variables categóricas
Revisa frecuencia absoluta y relativa, moda, categorías raras y cardinalidad. Gráficos: **barras, tabla de proporciones**.

Interpretación esperada: ¿hay una categoría dominante? ¿categorías con muy pocos casos? ¿está balanceada? ¿demasiados niveles?

> Las definiciones y fórmulas de las medidas (media, mediana, varianza, sesgo, curtosis) están en `03_estadistica_aplicada.md`.

---

## 3. Valores faltantes (nulos)

Los nulos no son solo un problema técnico: su patrón puede contener información.

**Qué revisar:** número y porcentaje de nulos por columna, patrón de ausencia, relación entre ausencia y target, y si son aleatorios o sistemáticos.

### Tipos conceptuales de ausencia
- **MCAR** (*Missing Completely At Random*): la ausencia no depende de ninguna variable.
- **MAR** (*Missing At Random*): la ausencia depende de variables observadas.
- **MNAR** (*Missing Not At Random*): la ausencia depende del propio valor faltante o de una variable no observada.

### Reglas prácticas
- No imputar automáticamente.
- No imputar el target para entrenamiento.
- Si una variable tiene más de 40-50% de nulos, evaluar eliminarla.
- Documentar siempre la decisión.
- Ajustar imputadores solo en train.

> Las técnicas de imputación (media, mediana, moda, KNN) están en `05_preparacion_de_datos.md`.

---

## 4. Valores atípicos (outliers)

Observaciones extremas que pueden ser errores, casos raros o señales importantes.

### Detección con IQR
```
Límite inferior = Q1 - 1.5 * IQR
Límite superior = Q3 + 1.5 * IQR
donde IQR = Q3 - Q1
```
Gráficos: `boxplot`, `stripplot`.

### Qué reportar
Por variable numérica: número de outliers, porcentaje, límite inferior, límite superior y decisión tomada.

### Buenas prácticas
No eliminar automáticamente. Antes de tratarlos pregunta: ¿son errores de captura? ¿valores posibles? ¿eventos importantes? ¿distorsionan el modelo? ¿el modelo elegido es sensible a outliers?

- *Error (ej. edad −5):* eliminar.
- *Caso especial (ej. compra millonaria):* mantener, pero usar algoritmos robustos (como árboles).

> El tratamiento (winsorización, transformación, escalado robusto) se desarrolla en `05_preparacion_de_datos.md`.

---

## 5. El dilema del binning: ¿señal o ruido?

El histograma agrupa datos continuos en intervalos (bins). El tamaño del bin cambia la "historia" que cuentan los datos:

- **Pocos bins (oversmoothing):** agrupas de más y pierdes los picos locales.
- **Demasiados bins (undersmoothing):** ves "picos" donde solo hay azar; el gráfico se llena de huecos y cuesta ver la forma real.

### Reglas para decidir el número de bins

| Regla | Enfoque | Cuándo usarla |
| --- | --- | --- |
| **Sturges** | Según nº de datos; conservadora, suaviza | Datos ~normales, dataset pequeño/mediano (ej. 1000 datos → ~11 bins) |
| **Rice** | Más agresiva, revela más detalle | Si sospechas múltiples grupos mezclados (ej. 1000 datos → ~20 bins) |
| **Freedman-Diaconis** | Según la dispersión (IQR), no el nº de datos | Datos con mucha variación/outliers; ajusta el ancho para que los extremos no arruinen la vista |

---

## 6. Análisis bivariado

Estudia la relación entre dos variables; la herramienta depende de los tipos.

### Numérica vs. numérica
*¿Están asociadas?* → scatter plot, Pearson, Spearman.
> **Alerta de multicolinealidad:** si dos variables tienen correlación > 0.90, elimina una; confunde al modelo.

### Categórica vs. categórica
*¿La distribución de una depende de la otra?* → tabla de contingencia, chi-cuadrado, Cramér's V.

### Numérica vs. categórica
*¿La media difiere entre grupos?* → boxplot por grupo, ANOVA, eta cuadrado (prueba t si solo hay dos grupos).
> *Ejemplo:* ¿gasta más el cliente "Oro" que el "Plata"? Si el boxplot muestra medianas iguales, esa categoría no sirve para predecir el gasto.

> Las fórmulas e interpretación de Pearson, Spearman, chi-cuadrado, ANOVA y eta están en `03_estadistica_aplicada.md`.

---

## 7. Visualización exploratoria

Una visualización debe **responder una pregunta**, no decorar.

**Todo gráfico debe tener:** título, ejes claros, unidades, leyenda si aplica e interpretación escrita.

### Gráficos por tipo de análisis

| Análisis | Gráficos |
| --- | --- |
| Una numérica | Histograma, KDE, boxplot |
| Una categórica | Barras, tabla de frecuencias |
| Numérica vs. numérica | Scatter plot, heatmap de correlación |
| Numérica vs. categórica | Boxplot por grupo, violin plot, barplot con IC |
| Categórica vs. categórica | Tabla de contingencia, barras apiladas, heatmap de proporciones |

### Regla de interpretación
Cada figura debe responder: *¿qué implica esto para la pregunta analítica?* No basta "se observa una diferencia". Mejor:

> El grupo A tiene una mediana mayor que el grupo B, lo que sugiere una posible relación entre la categoría y el resultado. Debe confirmarse con una prueba estadística o en modelado.

---

## 8. Cheat sheet de EDA

| Si quieres saber… | Usa… |
| --- | --- |
| ¿Qué tan "llenos" están mis datos? | `missingno.matrix(df)` |
| ¿Qué variables son más importantes? | `sns.pairplot(hue='target', corner=True)` |
| ¿Cómo cambian los datos en el tiempo? | `df.set_index('fecha')['valor'].plot()` |
| ¿Mis categorías son muy variadas? | `df['col'].nunique()` vs. `len(df)` (cardinalidad) |
| ¿La variable es normal? | `sns.histplot(kde=True)` + `stats.probplot()` (Q-Q) |
| ¿Dónde están los outliers? | `sns.boxplot()` / regla del IQR |
