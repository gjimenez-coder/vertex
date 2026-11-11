# 02 · Arquitectura e Ingeniería de Datos

Cómo se almacenan, mueven y organizan los datos antes de analizarlos: modelos de base de datos, tipos de datos, arquitecturas (Data Lake / Warehouse), paradigmas de procesamiento (ETL/ELT, batch/streaming) y buenas prácticas, con foco especial en datos geoespaciales (PostGIS).

> ¿Buscas la parte práctica? La guía paso a paso para montar un stack geoespacial está en [`02b_guia_practica_geoespacial.md`](02b_guia_practica_geoespacial.md).

---

## 1. Modelos de base de datos: relacional vs. columnar vs. geoespacial

| Criterio | Relacional (RDBMS) | Columnar | Geoespacial (GIS) |
| --- | --- | --- | --- |
| Estructura | Filas y columnas (tablas) | Columnas almacenadas por separado | Tablas con geometría y coordenadas |
| Optimizado para | Transacciones y CRUD | Consultas analíticas y agregaciones masivas | Consultas espaciales y mapas |
| Lectura/escritura | Balanceadas | Lectura rápida, escritura más lenta | Lectura espacial eficiente |
| Esquema | Fijo por tabla | Fijo orientado a columnas | Fijo con tipos espaciales (`geometry`, `geography`) |
| Compresión | Baja | Alta (por tipo de dato en columna) | Media |
| Casos de uso | ERP, CRM, banca | Data Warehousing, BI, big data | Mapas, rutas, zonas, sensores geográficos |
| Motores | PostgreSQL, MySQL, SQL Server | BigQuery, Redshift, ClickHouse, DuckDB | PostgreSQL+PostGIS, GeoServer, SpatiaLite |

**¿Cuándo usar cada uno?**

| Necesidad | Modelo recomendado |
| --- | --- |
| Alta integridad y relaciones complejas | Relacional (PostgreSQL, MySQL) |
| Consulta rápida de grandes volúmenes (BI) | Columnar (BigQuery, Redshift, DuckDB) |
| Geometría, mapas, rutas, zonas | Geoespacial (PostGIS, GeoServer) |

---

## 2. Tipos de datos: estructurados, semiestructurados, no estructurados

| | Estructurado | Semiestructurado | No estructurado |
| --- | --- | --- | --- |
| Definición | Esquema fijo (filas/columnas) | Estructura flexible (claves/etiquetas) | Sin estructura predecible |
| Formato típico | Tablas SQL, CSV | JSON, XML, YAML, Parquet, Avro | Imágenes, audio, video, PDFs |
| Consulta | SQL | SQL extendido (BigQuery JSON, Spark SQL), JSONPath | Requiere IA/ML o software especializado |
| Almacenamiento | RDBMS | NoSQL, Data Lake, Hive, MongoDB | Data Lakes (S3, MinIO), Blob, HDFS |
| Complejidad | Baja | Media | Alta |
| Ejemplos | Clientes, ventas, inventario | Logs, APIs, eventos IoT | Imágenes satelitales, sensores |

---

## 3. Data Lake vs. Data Warehouse

| Característica | Data Lake | Data Warehouse |
| --- | --- | --- |
| Propósito | Grandes volúmenes de datos **crudos** de cualquier tipo | Datos **estructurados y curados** para análisis |
| Tipo de datos | Todos | Estructurados y parcialmente semiestructurados |
| Formato | Parquet, Avro, ORC, JSON, CSV, GeoTIFF, HDF5 | Tablas SQL (columnar en motores modernos) |
| Esquema | Schema-on-read (al leer) | Schema-on-write (al escribir) |
| Costo | Bajo (S3, MinIO) | Más caro (motor SQL optimizado) |
| Escalabilidad | Muy alta (petabytes) | Alta, limitada en datos no tabulares |
| Casos de uso | Ingesta bruta, ML, imágenes, IoT, logs | BI, dashboards, reporting, analítica SQL |
| Herramientas | S3, MinIO, Azure Data Lake, HDFS | BigQuery, Snowflake, Redshift, PostgreSQL |

**¿Cuándo usar cada uno?** Data Lake para sensores/imágenes/textos y para preparar datos de ML; Data Warehouse para consultas SQL limpias y dashboards ejecutivos. Para datos satelitales (GeoTIFF) + metadatos (JSON): Data Lake con PostGIS para los metadatos.

```
       [Fuentes de datos]
 (APIs, sensores, imágenes, logs)
                ↓
           [Data Lake]
   (S3 / MinIO en Parquet, GeoTIFF)   → Raw / Staging / Processed
                ↓
   [Data Warehouse / PostGIS]
   (tablas limpias y modeladas, SQL optimizado)
                ↓
    [Dashboards, BI, Ciencia de Datos]
 (Power BI, Superset, Python, Mapas)
```

---

## 4. ETL vs. ELT

| Característica | ETL (Extract → Transform → Load) | ELT (Extract → Load → Transform) |
| --- | --- | --- |
| Orden | Extraer → transformar → cargar | Extraer → cargar → transformar |
| Lugar de transformación | Servidor/motor intermedio | Dentro del warehouse (Redshift, BigQuery) |
| Enfoque | Clásico (on-premise, legacy) | Moderno (cloud-native, escalable) |
| Big data | Limitado | Alto (usa poder del warehouse) |
| Herramientas | Talend, Pentaho, Informatica | dbt, BigQuery SQL, Snowflake, Spark SQL |

- **ETL:** cuando necesitas validaciones previas al guardado o trabajas con bases sensibles.
- **ELT:** si trabajas en cloud y necesitas escalabilidad y muchas transformaciones postcarga.

---

## 5. Batch vs. Streaming

| Característica | Batch (por lotes) | Streaming (tiempo real) |
| --- | --- | --- |
| Frecuencia | Periódica (minutos, horas, días) | Continua (segundos) |
| Latencia | Alta | Baja (ms a segundos) |
| Complejidad | Baja a media | Alta (eventos, estados, tolerancia a fallos) |
| Procesamiento | Acumulado por grupos | Registro por registro |
| Herramientas | Airflow, Prefect, Dask, Spark (batch) | Kafka, Spark Streaming, Flink, Beam |
| Casos de uso | Reportes diarios, cargas ETL, backups | Monitoreo de sensores, alertas, tracking en vivo |

- **Batch:** cuando los datos pueden esperar (informes, acumulación).
- **Streaming:** cuando necesitas reaccionar en tiempo real (alertas de clima extremo, sensores activos).

---

## 6. Flujo completo: ingestión → insights

```
[FUENTES] Sensores, APIs, imágenes, bases externas
   ↓
[INGESTIÓN] Streaming: Kafka/MQTT  ·  Batch: Airflow/Prefect
   ↓
[DATA LAKE] Parquet, JSON, GeoTIFF (crudo)
   ↓
[TRANSFORMACIÓN · ELT] dbt / SQL / Python + validación y limpieza
   ↓
[DATA WAREHOUSE] PostgreSQL/PostGIS, BigQuery, Redshift
   ↓
[MODELOS ANALÍTICOS] vistas por región/fecha/tipo, métricas, etiquetas
   ↓
[INSIGHTS Y VISUALIZACIÓN] Power BI, Superset · Mapas: QGIS, Leaflet, Mapbox · APIs y alertas
```

---

## 7. Datos geoespaciales: PostgreSQL + PostGIS

**PostGIS** es la extensión geoespacial de PostgreSQL: añade tipos `GEOMETRY`, `GEOGRAPHY`, `RASTER` y más de 300 funciones espaciales (`ST_Within`, `ST_Distance`, `ST_Intersects`, etc.). PostgreSQL solo no soporta consultas espaciales de forma nativa.

### Buenas prácticas de modelado geoespacial

- **Claves primarias únicas** en toda tabla espacial (`id_zona`, `id_sensor`).
- **Relaciona geodatos con entidades clave** mediante foreign keys (`region_id`).
- **No separes lat/lon en columnas**: usa `POINT(lon, lat)` en una columna `geometry`.
- **Define el tipo explícitamente**: `GEOMETRY(POINT, 4326)` en vez de solo `GEOMETRY`.
- **No mezcles tipos de geometría** en una misma columna.

### SRID y proyecciones

- Usa el **SRID adecuado**: WGS 84 (`4326`) para coordenadas globales; UTM para distancias locales precisas.
- **No transformes el SRID en cada consulta**: almacena ya transformado para evitar sobrecarga (`ST_Transform`).
- Valida que toda geometría tenga SRID definido.

### Validación y limpieza

- Valida con `ST_IsValid(geom)` antes de insertar; corrige con `ST_MakeValid()`.
- Simplifica geometrías pesadas con `ST_Simplify()` para visualización.
- Evita polígonos abiertos o líneas auto-intersectadas.

### Optimización y rendimiento

- Crea **índices espaciales GIST** en columnas `geometry`/`geography`; combínalos con BTree para consultas mixtas.
- Prioriza funciones eficientes (`ST_Intersects`, `ST_DWithin`, `ST_Within`) antes que las costosas (`ST_Contains`, `ST_Equals`).
- Para distancias en metros, transforma a `GEOGRAPHY`: `ST_Distance(geom::geography, ...)`.
- Usa `VACUUM` y `ANALYZE` regularmente; usa `views` o `materialized views` para consultas espaciales frecuentes.

---

## 8. Reglas de oro para equipos de datos

1. **Carga primero, transforma después** (adopta ELT, deja el cómputo al warehouse).
2. Cada tabla debe tener **dueño, propósito y documentación**.
3. **Automatiza** todo lo repetible.
4. No presentes datos **sin contexto ni validación**.
5. Usa **staging/intermedios** para no romper modelos aguas abajo.
6. Datos no usados = **deuda técnica**: limpia el data lake periódicamente.

### Buenas prácticas por etapa

| Etapa | Prácticas clave |
| --- | --- |
| Ingestión | Automatiza (Airflow/Prefect), control de calidad (esquema, duplicados, tipos), registra logs y metadatos |
| Almacenamiento | Data Lake (S3/MinIO) para crudo, formatos eficientes (Parquet/COG), carpetas `/raw`, `/staging`, `/processed` |
| Transformación (ELT) | dbt o SQL en el warehouse, validaciones (rangos, nulos), versiona modelos y documenta tablas |
| Modelado | Enfoque modular (raw → staging → analytics), star schema o capas, lógica centralizada en el warehouse |
| Análisis | Notebooks reproducibles, scripts versionados, insights con contexto |
| Visualización | Conecta dashboards a vistas limpias (no tablas crudas), contexto > gráfico |
| Mantenimiento | Monitorea tiempos/errores/calidad, alertas ante fallos de fuente, documenta dependencias |

---

## 9. Anexo: formatos de archivos geoespaciales

| Archivo | Tipo | Función | Cómo leerlo |
| --- | --- | --- | --- |
| `.tif` | Raster | Imagen georreferenciada con los datos reales | QGIS, `rasterio` |
| `.tfw` | Raster | World file: georreferenciación del `.tif` | Automático en QGIS |
| `.ovr` | Raster | Pirámide de overviews, mejora el zoom | Automático |
| `.aux.xml` | Raster | Metadatos auxiliares de ArcGIS | Ignorable sin ArcGIS |
| `.vat.dbf` | Raster atributo | Value Attribute Table (qué representa cada valor de celda) | QGIS, `pandas` + DBF |
| `.shp` | Vectorial | Geometrías (polígonos, áreas) | QGIS, `geopandas` |
| `.dbf` | Vectorial | Tabla de atributos del `.shp` | Automático con `.shp` |
| `.shx` | Vectorial | Índice de geometría | Automático |
| `.prj` | Vectorial | Proyección y sistema de coordenadas | Automático |
| `.cpg` | Vectorial | Codificación de caracteres del `.dbf` | Implícito |
| `.shp.xml` | Metadato | Metadatos del shapefile | Visor XML o QGIS |

### Recursos de geodatos

| Categoría | Recurso |
| --- | --- |
| Geodatos del Perú | SENAMHI, GeoPeru, INPE |
| Satélites | Earthdata NASA, Copernicus Open Access |
| Python geoespacial | GeoPandas, Shapely, Pyproj, Rasterio, Fiona, GDAL, netCDF4 |
| Visualización de mapas | Folium, Leaflet.js, Kepler.gl, QGIS, Mapbox |
| Cloud / análisis global | Google Earth Engine, BigQuery GIS |
