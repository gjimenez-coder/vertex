# Proceso ML Reproducible — Lecciones del Proyecto de Cancelaciones Hoteleras

**Proyecto:** Predicción de cancelaciones hoteleras — PUCP Grupo 5  
**Stack:** Python 3.11 · scikit-learn · MLflow · DVC · Docker · Kaggle  
**Periodo:** Sprint 1–4 (Septiembre 2026)

---

## 1. Estructura del proyecto

```
proyecto/
├── data/
│   ├── raw/          ← nunca modificar, versionado con DVC
│   └── processed/    ← CSVs generados, versionados con DVC (nunca en Git)
├── notebooks/        ← un notebook por historia de usuario
├── src/              ← funciones reutilizables (tuning.py, etc.)
├── docs/             ← diccionario de datos, hallazgos QA, auditorías
├── tests/            ← tests de datos y reproducibilidad
├── secrets/          ← credenciales (en .gitignore, nunca en Git)
├── environment.yml   ← entorno reproducible con conda/pip
├── docker-compose.yml
└── mlflow.db         ← backend SQLite de MLflow (commitable al cerrar sprint)
```

**Regla de oro:** Git versiona código. DVC versiona datos. MLflow versiona modelos.

---

## 2. Entorno reproducible

### Docker
```yaml
# docker-compose.yml — servicios mínimos
services:
  jupyter:  # notebook interactivo
  mlflow:   # servidor de tracking (detener antes de entrenar)
```

Detener el servidor MLflow antes de entrenar desde un notebook para evitar conflictos de escritura en SQLite:
```bash
docker compose stop mlflow
# ... entrenar ...
docker compose start mlflow
```

### MLflow backend
Usar SQLite en lugar del backend de archivos (`mlruns/`):
```python
mlflow.set_tracking_uri('sqlite:///mlflow.db')
```
El backend de archivos fue deprecado en MLflow 2.7+. SQLite es commitable, portable y libre de conflictos de DNS rebinding cuando se conecta desde Docker.

---

## 3. Pipeline de datos

### Orden obligatorio

```
raw CSV → limpieza → feature engineering → versionar con DVC → modelado
```

Nunca hacer feature engineering en el notebook de modelado. Usar un notebook dedicado que genere el CSV enriquecido y versionarlo con DVC.

### Data Leakage — los dos tipos más comunes

**Tipo 1 — Feature con información del futuro:**
```python
# MAL: reservation_status_date es la fecha del estado FINAL de la reserva
df['dias_anticipacion'] = fecha_llegada - df['reservation_status_date']
# Para canceladas: llegada - fecha_cancelacion → codifica directamente el target
```

Señal de alerta: una feature con importancia Gini >0.5 en un Random Forest es sospechosa.

**Tipo 2 — SMOTE fuera del pipeline de CV:**
```python
# MAL: los folds de validación contienen muestras sintéticas
X_bal, y_bal = SMOTE().fit_resample(X_train, y_train)
RandomizedSearchCV(rf, params).fit(X_bal, y_bal)
# CV AUC inflado ~0.04 puntos vs Test AUC

# BIEN: SMOTE se aplica solo al fold de entrenamiento
from imblearn.pipeline import Pipeline as ImbPipeline
pipeline = ImbPipeline([('smote', SMOTE(random_state=42)), ('clf', rf)])
RandomizedSearchCV(pipeline, params).fit(X_train, y_train)
```

### Checklist antes de modelar

- [ ] Excluir columnas de leakage directo
- [ ] Verificar que todas las features son numéricas
- [ ] Verificar 0 nulos
- [ ] DVC add del CSV procesado
- [ ] Split estratificado antes de cualquier transformación

---

## 4. Balanceo de clases

Con desbalance moderado (20-40% clase positiva), comparar estas estrategias:

| Estrategia | Cuándo usar | Ventaja | Riesgo |
|-----------|------------|---------|--------|
| `class_weight='balanced'` | Primera opción | Sin datos sintéticos | Menor recall en positivos |
| SMOTE en pipeline | Si class_weight no alcanza | Aumenta cobertura | Interpola variables categóricas encodadas |
| SMOTE fuera del pipeline | Nunca en CV | — | Fuga de datos al CV |

**Hallazgo de este proyecto:** con variables categóricas de alta cardinalidad codificadas con LabelEncoder, SMOTE genera valores interpolados sin sentido. `class_weight='balanced'` fue superior (AUC 0.9109 vs 0.9035).

---

## 5. Modelos baseline

Entrenar siempre un conjunto mínimo antes de hacer tuning:

| Modelo | Rol |
|--------|-----|
| Naive Bayes | Lower bound rápido |
| Logistic Regression | Referencia lineal |
| SVM Linear | Referencia lineal robusta |
| Decision Tree | Detectar overfitting sin ensemble |
| KNN | Referencia no paramétrica |
| Random Forest | Candidato principal |
| RF (class_weight) | Comparar SMOTE vs class_weight desde baseline |

Registrar siempre en MLflow con las mismas métricas: `accuracy`, `roc_auc`, `recall`, `precision`, `f1`, `pr_auc`.

**PR-AUC:** con desbalance moderado, ROC-AUC puede ser optimista. `average_precision_score` da información más honesta sobre el rendimiento en la clase positiva.

---

## 6. Hiperparámetros

### Estrategia recomendada

```
1. HalvingRandomSearchCV (exploración amplia, más eficiente que RandomizedSearch)
   ↓ mejores params
2. GridSearchCV fino (solo varía class_weight u otro factor clave)
   ↓ mejor modelo
3. Model Registry con alias @champion
```

### HalvingRandomSearchCV con ImbPipeline — configuración crítica

```python
# IMPORTANTE: usar resource='clf__n_estimators', NO el default 'n_samples'
# Con 'n_samples', SMOTE falla en rondas tempranas por subsets muy pequeños
rs = HalvingRandomSearchCV(
    pipeline,
    param_dist,
    resource='clf__n_estimators',
    min_resources=50,
    max_resources=200,
    factor=3,
    scoring='roc_auc',
    cv=StratifiedKFold(n_splits=5),
    n_jobs=2,  # no usar -1 con SMOTE en pipeline (OOM)
)
```

### Prefijo `clf__` obligatorio con pipeline

```python
# Parámetros del clasificador dentro del pipeline llevan prefijo clf__
param_dist = {
    'clf__max_depth':         [10, 20, None],
    'clf__n_estimators':      randint(50, 200),
    'clf__min_samples_leaf':  randint(1, 20),
}
```

---

## 7. MLflow — convenciones

### Nomenclatura de experimentos

```
proyecto_baseline      ← modelos base
proyecto_tuning        ← tuning de hiperparámetros
proyecto_ensembles     ← ensambles
```

Nunca usar nombres genéricos como `proyecto-clasificacion` o `default`.

### Cleanup antes de re-ejecutar

```python
exp = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if exp:
    runs = mlflow.search_runs(experiment_ids=[exp.experiment_id], output_format='list')
    for r in runs:
        client.delete_run(r.info.run_id)
```

### Model Registry con versiones semánticas

```python
# v1 = búsqueda amplia (HalvingRandom)
# v2 = refinamiento (GridSearch)
# v3 = Champion
client.set_registered_model_alias(REGISTERED_NAME, 'champion', version)
```

### skops_trusted_types — obligatorio para sklearn >= 1.4

```python
mlflow.sklearn.log_model(
    model, name='rf',
    registered_model_name=REGISTERED_NAME,
    skops_trusted_types=[
        'sklearn.tree._tree.Tree',
        'sklearn.tree._classes.DecisionTreeClassifier',
        'sklearn.tree._classes.DecisionTreeRegressor',
        'imblearn.pipeline.Pipeline',
        'imblearn.over_sampling._smote.base.SMOTE',
        # Para SVM con calibración:
        'sklearn.calibration._CalibratedClassifier',
        'sklearn.calibration._SigmoidCalibration',
        'sklearn.svm._classes.LinearSVC',
    ]
)
```

---

## 8. Entrenamiento en Kaggle (capa gratuita)

### Límites
- Sesión: 9 horas máximo
- CPU: 2 cores / ~13 GB RAM
- Sin internet por defecto

### Diseño de notebooks duales

```
notebook_tuning.ipynb       ← versión local con MLflow completo
notebook_kaggle.ipynb       ← versión Kaggle sin MLflow, guarda pkl+json
```

La versión Kaggle guarda en `/kaggle/working/`:
- `best_v1.pkl`, `best_v2.pkl`, `champion.pkl`
- `tuning_results.json`

Luego se descargan y registran en MLflow local.

### Estimación de tiempo

Con Random Forest (100-200 árboles) + SMOTE sobre ~70k muestras:
- ~6s por fit con 50 árboles
- ~20s por fit con 150 árboles

Para GridSearch en Kaggle: máximo ~1,500 fits para mantenerse en 9h.

### Para v2 en Kaggle: no expandir el grid

```python
# MAL: nbhood genera 486 combinaciones × 10 folds = 4,860 fits → timeout
# BIEN: solo variar el factor clave (class_weight) = 3 × 10 = 30 fits
grid = {
    'n_estimators': [bp['n_estimators']],  # fijo en el mejor de v1
    'max_depth':    [bp['max_depth']],
    'class_weight': [None, 'balanced', {0:1, 1:3}],  # solo esto varía
}
```

---

## 9. Reproducibilidad

### Semillas fijas en todo el pipeline

```python
RANDOM_STATE = 42  # train_test_split, SMOTE, KFold, modelos, SearchCV
```

### Versionado con DVC

```bash
dvc add data/processed/dataset_features.csv
git add data/processed/dataset_features.csv.dvc
git commit -m "feat: agrega features de ingeniería al dataset"
```

### mlflow.db en Git

Commitear al cerrar cada sprint, no en cada iteración. Incluir mensaje con las métricas clave del sprint.

---

## 10. Pitfalls comunes y sus fixes

| Problema | Síntoma | Fix |
|---------|---------|-----|
| SMOTE fuera del pipeline | CV AUC >> Test AUC (~0.04) | `ImbPipeline` con SMOTE dentro |
| Feature con leakage | Importancia Gini >0.5 en un feature | Revisar origen de la feature |
| MLflow 403 DNS rebinding | `Invalid Host header` desde Docker | `sqlite:///mlflow.db` directo |
| skops UntrustedTypes | `MlflowException` al hacer `log_model` | Agregar `skops_trusted_types` |
| HalvingRandom con SMOTE | `SIGKILL(-9)` / OOM | `resource='clf__n_estimators'` |
| `n_jobs=-1` con SMOTE | OOM por copias del dataset | Limitar a `n_jobs=2` |
| Timeout en Kaggle | `canceled after Xs` | Calcular fits × tiempo/fit antes |
| `applymap` deprecado | `AttributeError` en pandas 2.1+ | Usar `.map()` |
| `artifact_path` deprecado | `FutureWarning` en MLflow 2.x | Usar `name=` en `log_model` |
| MLflow FileStore deprecado | `MlflowException: maintenance mode` | Usar `sqlite:///mlflow.db` |
| Kernel `datalab` no encontrado en Kaggle | `NoSuchKernel` | Cambiar kernelspec a `python3` al hacer push |

---

## 11. Separación de responsabilidades por notebook

```
01_business.ipynb          → contexto de negocio, KPIs, criterios de éxito
02_data_loading.ipynb      → carga y verificación del dataset raw
03_eda.ipynb               → análisis exploratorio, correlaciones, distribuciones
05_data_cleaning.ipynb     → limpieza, encoding, eliminación de duplicados
06_feature_eng.ipynb       → ingeniería de variables (genera CSV enriquecido + DVC)
07_class_balance.ipynb     → análisis del desbalance, estrategia de balanceo
10_baseline_models.ipynb   → 6-7 modelos baseline con ImbPipeline + MLflow
11_evaluation.ipynb        → evaluación exhaustiva de baselines
12_hyperparam_tuning.ipynb → tuning local (HalvingRandom + GridSearch + MLflow)
12_hyperparam_kaggle.ipynb → tuning en Kaggle (sin MLflow, guarda pkl+json)
13_ensembles.ipynb         → ensambles usando el @champion del Registry
```

---

## 12. Pendientes frecuentes para próximos proyectos

- **Target encoding** para variables categóricas de alta cardinalidad (mejor que LabelEncoder para KNN, LR, SVM)
- **Split temporal** si el modelo predice eventos futuros
- **Calibración de probabilidades** (`CalibratedClassifierCV`) si se usan probabilidades directamente
- **Ajuste de umbral** (`TunedThresholdClassifierCV`) según la matriz de costos del negocio
- **Nested CV** para métricas completamente honestas del proceso de tuning completo
- **Optuna** como evolución natural de HalvingRandomSearchCV para búsquedas más largas
