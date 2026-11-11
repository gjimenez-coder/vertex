# 02b · Guía Práctica: Montar un Stack de Datos Geoespacial

Guía paso a paso para construir, desde cero, una infraestructura de datos geoespacial end-to-end: desde el diseño conceptual hasta un pipeline automatizado con visualización. Es la contraparte **práctica** de `02_arquitectura_e_ingenieria_datos.md` (que cubre los conceptos y las comparativas).

> Caso de ejemplo a lo largo de la guía: **identificar bosques y pérdida de bosques húmedos amazónicos** en Perú.

---

## Fase 1 · Diseño conceptual (objetivos + fuentes)

1. **Define el objetivo concreto** — ¿qué quieres responder o visualizar?
   - *Ejemplo:* identificar bosques y pérdida de bosque húmedo amazónico.
2. **Identifica las fuentes de datos** (Perú) — SENAMHI, GeoPeru, INPE, Earthdata NASA, Copernicus (ver anexo de recursos en el doc 02).
3. **Define los objetos espaciales clave** — zonas protegidas, sensores, rutas de expedición, puntos de interés.

---

## Fase 2 · Infraestructura básica

1. **Crea una base de datos PostgreSQL + PostGIS** (local o en la nube).
   - Primeras tablas: `zonas`, `sensores`, `imagenes`, `registros_climaticos`.
2. **Instala las herramientas del entorno:**
   - Python: `psycopg2`, `SQLAlchemy`, `GeoPandas`, `Rasterio`.
   - GIS: QGIS para visualizar y validar geometrías.
   - Orquestación: Prefect o Airflow.
3. **Estructura el Data Lake** (MinIO o S3 local) con capas por tipo de dato y estado:
   ```
   data_lake/
     raw/satelite/
     processed/satelite/
     raw/sensores/
   ```

> Aplica aquí las buenas prácticas geoespaciales del doc 02: SRID correcto (4326 para Perú), índices GIST, `POINT(lon, lat)` en una sola columna `geometry`.

---

## Fase 3 · Primer pipeline funcional (mínimo viable)

1. **Construye un pipeline simple (batch diario o semanal):**
   - Descarga una imagen satelital de prueba.
   - Procésala (corta, comprime, convierte a Parquet o COG).
   - Guárdala en el data lake.
   - Registra los metadatos en PostGIS.
2. **Carga las capas base en la BD** — zonas naturales, regiones, distritos (shapefiles oficiales con `ogr2ogr` o `GeoPandas`).
3. **Haz una consulta espacial básica:**
   - *Ejemplo:* "sensores dentro de una zona protegida con humedad > 80%".

> Este es un flujo **batch** (ver batch vs. streaming en el doc 02): adecuado cuando los datos pueden actualizarse por lotes periódicos.

---

## Fase 4 · Exploración y visualización

1. **Crea un dashboard o mapa básico** — Mapbox, Leaflet o QGIS; visualiza sensores o imágenes sobre zonas específicas.
2. **Documenta el flujo** — en Markdown o Notion: datos, scripts, flujos y objetivos.
3. **Automatiza:**
   - Programa el pipeline con Prefect (ejecución diaria o semanal).
   - Agrega alertas y logs ante fallos.

---

## Resumen del flujo

```
[Fuentes: SENAMHI, satélites, sensores]
        ↓  (Fase 3: pipeline batch)
[Data Lake: raw → processed, en Parquet/COG]
        ↓
[PostgreSQL + PostGIS: capas base + metadatos]
        ↓  (consultas espaciales)
[Dashboard / Mapa: Leaflet, Mapbox, QGIS]
        ↓  (Prefect/Airflow: automatización + alertas)
```

> Para la teoría detrás de cada pieza (modelos de BD, Data Lake vs. Warehouse, ETL/ELT, PostGIS, formatos de archivo geoespacial), consulta [`02_arquitectura_e_ingenieria_datos.md`](02_arquitectura_e_ingenieria_datos.md).
