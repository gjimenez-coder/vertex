# Dominios de IA / Data Analytics

Documentación consolidada por dominio, generada a partir de las notas de `AI/raw/`. Cada concepto vive en **un solo lugar**: los temas duplicados entre las notas originales se unificaron y, cuando un tema se relaciona con otro dominio, se enlaza en vez de repetirse.

## Índice

| # | Documento | Contenido |
| --- | --- | --- |
| 01 | [Fundamentos de la Ciencia de Datos](01_fundamentos_ciencia_datos.md) | Qué es un proyecto de datos, datos como activo y DDD, aprendizaje supervisado/no supervisado, CRISP-DM, descomposición del problema de negocio, qué es un modelo, fugas de datos (leaks), tipos de problemas y variables, inferencia vs. predicción, estrategia de datos |
| 02 | [Arquitectura e Ingeniería de Datos](02_arquitectura_e_ingenieria_datos.md) | Modelos de BD, tipos de datos, Data Lake/Warehouse, ETL/ELT, batch/streaming, PostGIS/geoespacial, buenas prácticas |
| 02b | [Guía Práctica: Stack Geoespacial](02b_guia_practica_geoespacial.md) | Guía paso a paso para montar una infraestructura de datos geoespacial (PostGIS, Data Lake, pipeline batch, dashboard) |
| 03 | [Estadística Aplicada](03_estadistica_aplicada.md) | Clasificación de variables, medidas descriptivas (con fórmulas), forma, normalidad, correlación, asociación categórica, comparación de medias, IC y p-valores |
| 04 | [Análisis Exploratorio de Datos](04_analisis_exploratorio_datos.md) | Auditoría/perfilado, univariado, nulos, outliers, binning, bivariado, visualización, cheat sheet |
| 05 | [Preparación de Datos](05_preparacion_de_datos.md) | Train/test, anti-leakage, imputación, tratamiento de outliers, escalado, encoding, pipelines |
| 06 | [Modelado, Evaluación y Producción](06_modelado_y_evaluacion.md) | Regresión, logística, árboles, Naive Bayes, k-NN/clustering, desbalance, baselines, métricas, valor esperado y costo-beneficio, curvas profit/lift/ROC, validación cruzada, overfitting, interpretabilidad, ingeniería analítica, producción |
| 07 | [Series Temporales y Pronóstico](07_series_temporales.md) | Patrones (tendencia/estacionalidad/ciclo), ACF/PACF, descomposición STL, benchmarks, ETS, ARIMA/SARIMA, regresión dinámica, VAR, jerárquico, espacio de estados/Kalman, NNAR, TBATS, diagnóstico de residuales y validación cruzada temporal |
| 08 | [Visualización y Comunicación de Datos](08_visualizacion_y_comunicacion.md) | Contexto (quién/qué/cómo), elección de gráfico, reducir clutter (Gestalt), atributos preatentivos, pensar como diseñador, color/tablas/style guide, narrativa (tres actos, call to action), principios universales |
| 09 | [Minería de Texto y NLP](09_mineria_texto_nlp.md) | Preprocesamiento (tokenización, stemming/lematización, stopwords), bolsa de palabras, TF-IDF, similitud coseno, n-gramas, NER, topic models (LDA/LSI), embeddings/Transformers, tareas y flujo de NLP |

## Flujo de trabajo

Los documentos siguen el orden natural de un proyecto de datos:

```
01 Fundamentos  →  define el problema y el enfoque
02 Arquitectura →  dónde viven y cómo llegan los datos
03 Estadística  →  base para describir e inferir
04 EDA          →  entender los datos
05 Preparación  →  transformarlos sin leakage
06 Modelado     →  predecir, evaluar, interpretar, desplegar
07 Series temp. →  especialización para datos en el tiempo
08 Visualización→  comunicar resultados y mover a la acción
09 Texto / NLP  →  especialización para datos de texto
```

> **Especializaciones y transversales:** 07 (series temporales) y 09 (texto/NLP) son especializaciones por tipo de dato; 08 (visualización y comunicación) es transversal: aplica a la salida de cualquier etapa del flujo.

## Criterio de deduplicación aplicado

Las notas originales repetían varios conceptos entre archivos. Se resolvió así:

- **CRISP-DM** → completo solo en 01 (estaba en `eda_v2.md` y `test.md`).
- **Tipos de variables** → visión general en 01; clasificación detallada y métrica de resumen en 03.
- **Medidas estadísticas y fórmulas** → centralizadas en 03 (estaban en `estadistica_aplicada.md` y `test.md`).
- **Outliers** → detección y binning en 04; tratamiento (winsorización, escalado robusto) en 05.
- **Valores faltantes** → diagnóstico conceptual (MCAR/MAR/MNAR) en 04; técnicas de imputación en 05.
- **Correlación, chi-cuadrado, ANOVA** → fórmulas en 03; uso práctico en el bivariado de 04.

> Las notas originales se conservan en `AI/raw/` como fuente.
