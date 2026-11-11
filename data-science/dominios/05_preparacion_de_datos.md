# 05 · Preparación de Datos

Transformar los datos crudos para que un modelo pueda usarlos, sin introducir fugas de información (*leakage*): separación train/test, imputación, tratamiento de outliers, escalado, encoding de categóricas y pipelines reproducibles.

---

## 1. Separación train/test

Antes de ajustar cualquier transformación o modelo, separa el dataset. **Objetivo:** evaluar el rendimiento en datos no vistos.

### Buenas prácticas
- Usa `random_state` para reproducibilidad.
- **Estratifica** en clasificación si hay desbalance.
- No toques el test hasta el final.
- En **series temporales**, haz split cronológico.
- En **datos agrupados**, evita que el mismo grupo aparezca en train y test.

### Regla anti-leakage
Todo lo que *aprende* de los datos debe ajustarse **solo en train**: imputadores, escaladores, encoders, límites de winsorización, selección de variables, target encoding, SMOTE.

---

## 2. Imputación

Reemplaza valores faltantes. (El diagnóstico de nulos —MCAR/MAR/MNAR— está en `04_analisis_exploratorio_datos.md`.)

| Técnica | Cuándo usarla |
| --- | --- |
| **Media** | Variable numérica, distribución simétrica, sin outliers severos |
| **Mediana** | Variable numérica con asimetría u outliers |
| **Moda** | Variables categóricas |
| **KNN Imputer** | Hay relaciones entre variables; tiene sentido imputar con observaciones similares |
| **Eliminación de filas** | Porcentaje de nulos muy bajo, ausencia aparentemente aleatoria, sin pérdida crítica |

> KNN Imputer debe ir dentro de un pipeline y ajustarse solo en train.

---

## 3. Tratamiento de outliers

Los outliers distorsionan media, desviación estándar, Pearson, regresión lineal y escalado estándar. (La detección por IQR está en el documento 04.)

### Winsorización
Limita los valores extremos a ciertos percentiles.
```
Valores < percentil 1  → se reemplazan por P1
Valores > percentil 99 → se reemplazan por P99
```
- **Cuándo usarla:** los extremos son válidos pero distorsionan; modelos sensibles a outliers; se quiere conservar observaciones.
- **Cuándo evitarla:** el extremo es la señal principal (fraude, eventos raros) o no hay justificación de dominio.

### Otras opciones
Mantenerlos, eliminarlos si son errores, transformar la variable, usar modelos robustos o escalado robusto.

---

## 4. Escalado

Cambia la escala de las variables numéricas.

| Scaler | Qué hace | Usar con |
| --- | --- | --- |
| **StandardScaler** | Media 0, desviación estándar 1 | Regresión regularizada, SVM, KNN, PCA, modelos basados en distancia u optimización |
| **MinMaxScaler** | Lleva al rango 0-1 | Redes neuronales, algoritmos que requieren rango acotado (sensible a outliers) |
| **RobustScaler** | Usa mediana e IQR | Datos con outliers moderados |

**No suele hacer falta escalar** para árboles de decisión, random forest ni gradient boosting basado en árboles.

---

## 5. Encoding de variables categóricas

Los modelos necesitan representar las categorías numéricamente.

| Encoding | Qué hace | Usar con | Precaución |
| --- | --- | --- | --- |
| **One-hot** | Una columna binaria por categoría | Nominales, baja cardinalidad, modelos lineales | Muchas columnas si la cardinalidad es alta |
| **Ordinal** | Números respetando un orden real (`bajo < medio < alto`) | Variables con orden real | — |
| **Label** | Números arbitrarios | — | Introduce orden falso en modelos lineales |
| **Target** | Reemplaza la categoría por una estadística del target | Alta cardinalidad | Riesgo alto de leakage; usar validación cruzada |

---

## 6. Pipelines y ColumnTransformer

Un pipeline encadena pasos de forma reproducible.

```
Datos crudos → imputación → escalado / encoding → modelo → predicción
```

### Ventajas
Evita leakage, facilita la validación cruzada, ordena el código, permite desplegar el mismo flujo y reduce errores manuales.

### ColumnTransformer
Aplica transformaciones distintas según el tipo de variable:
- **Numéricas:** imputación + escalado.
- **Categóricas:** imputación + one-hot.
- **Texto:** vectorización.
- **Fechas:** extracción de componentes.
