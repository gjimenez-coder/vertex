# External Dependencies, Supply Chain Integrity and Multi-Tenant Risk (Dependencias externas, integridad de la cadena de suministro y riesgo multiinquilino) — Estudio

## Tarjetas de repaso

P: ¿Cómo entra normalmente el riesgo de cadena de suministro en un sistema de IA?
R: Como artefactos cotidianos que ayudan a ir más rápido: model checkpoint, tokenizer, integración de vector database, paquete de Python, API de inferencia hospedada, dataset, imagen de contenedor o SDK de proveedor.

P: ¿Cuál es la tesis central del capítulo sobre la confianza?
R: La confianza es transitiva y debe hacerse explícita para poder validarla, monitorizarla y revocarla; no se elimina la confianza en terceros, se nombra por clases de dependencia para asignar controles.

P: ¿Cuáles son las cinco clases de dependencia que propone el capítulo?
R: Dependencias de modelo (salida/carga), de código (ejecución), de datos (lo que aprende o recupera), de infraestructura (aislamiento, telemetría, recuperación) y de proveedor (contrato, cumplimiento, residencia, visibilidad).

P: ¿Por qué la capa de integración/orquestación es la frontera de seguridad en el ejemplo del agente de arrendamientos?
R: Porque el modelo casi no tiene autoridad; la autoridad efectiva es lo que el servicio de integración pone en el payload, y esa capa mantiene conexiones per-tenant al sistema de registro de cada inquilino.

P: ¿Qué etapas sigue la validación de la procedencia de un modelo?
R: Confirmar fuente y uso previsto (model card), verificar integridad (hashes y firmas/atestaciones), inspeccionar el artefacto antes de cargarlo (p. ej. ModelScan) y probar comportamiento en sandbox.

P: ¿Qué debe guardar el registro interno de modelos?
R: Artefacto aprobado, URL de origen, hashes, firmas, model card, decisión de licencia, resultados del escáner, resumen de pruebas de comportamiento, propietario, fecha de aprobación, entornos de despliegue y ruta de revocación.

P: ¿Qué vincula la firma criptográfica de un modelo y qué principio ordena el proceso?
R: Vincula un artefacto aprobado a una identidad y un punto en el tiempo; el principio es validar antes de firmar y exigir la firma antes de desplegar, con fail closed si cambia la identidad o se salta el escáner.

P: ¿Por qué es peligroso el formato pickle y cuál es la regla operativa?
R: Cargar datos pickle puede ejecutar código Python; la regla es nunca deserializar objetos Python no confiables en un entorno con secretos, alcance de red, archivos escribibles o credenciales de producción.

P: ¿Qué ventaja ofrece safetensors frente a pickle?
R: Almacena tensores sin usar la ejecución de pickle durante la carga, eliminando un riesgo mayor, aunque no exime de evaluar fuente, licencia y comportamiento.

P: ¿Qué diferencia hay entre un SBOM y un VEX?
R: El SBOM da el inventario de componentes; el VEX explica si una vulnerabilidad conocida es realmente explotable en un contexto concreto.

P: ¿Qué debe incluir el inventario (AI SBOM) específico de IA?
R: Además del software, el linaje del modelo, datasets, evidencia de entrenamiento/evaluación, hashes, licencias e historial de actualizaciones (formatos CISA/G7, SPDX, CycloneDX).

P: Ordena de más a menos fuerte los patrones de aislamiento en vector databases.
R: Silo físico por inquilino, colección/índice dedicado por inquilino, partición por namespace y filtro de metadatos (este último solo como defensa en profundidad, nunca única frontera).

P: ¿Dónde pertenece la aplicación de la frontera de inquilino y por qué no en el prompt?
R: Al lado del servidor: deriva el inquilino del contexto autenticado, autoriza, adjunta el scope y registra; "si el prompt dice consultar otro inquilino, el prompt es irrelevante" (PDF p. 376).

P: ¿Qué aporta NVIDIA MIG y cuál es su límite?
R: Particiona GPUs compatibles en instancias aisladas por hardware, reduciendo contención y agotamiento de recursos entre inquilinos; no es frontera completa por sí sola (siguen requiriendo controles el host, drivers, scheduler, red, secretos, logs y serving).

P: Según NIST SP 800-61 Rev. 3, ¿por dónde empieza la respuesta a un incidente de cadena de suministro?
R: Por la contención (deshabilitar artefacto, bloquear paquete, cuarentena del modelo, revocar token, fijar versión conocida-buena o aislar inquilino) y luego mapear la exposición.

## Preguntas de autoevaluación

P: ¿Por qué hereda riesgo una aplicación de IA cuidadosamente revisada?
R: Porque se construye con código, datos, modelos, infraestructura y servicios ajenos, y hereda riesgo de cada artefacto que carga y cada servicio en el que confía. (Lo que necesitas saber)

P: ¿Por qué en el ejemplo la función de IA convierte la capa de orquestación en el objetivo de mayor valor?
R: No añadió una integración externa, pero acumuló una ruta alcanzable al sistema de registro de cada inquilino al mantener conexiones permanentes y un registro de credenciales por inquilino. (El ejemplo que recorre el capítulo)

P: ¿Qué significa el principio "si no puedes nombrar la clase, te costará nombrar el control"?
R: Que clasificar cada dependencia (modelo, código, datos, infraestructura, proveedor) es el paso previo para asignarle controles concretos. (La superficie de ataque de la cadena de suministro de IA)

P: ¿Por qué un escaneo limpio con ModelScan no es prueba de seguridad?
R: Los escáneres detectan opcodes peligrosos, globals sospechosos o estructuras inseguras conocidas, pero son un filtro, no una garantía, y los atacantes se adaptan; es solo una entrada junto a fuente, hash, formato, sandbox, pruebas y aprobación humana. (La amenaza de serialización con pickle)

P: ¿Por qué el login por navegador no sirve para firmar modelos en CI/CD y qué se usa en su lugar?
R: Sirve para una demo humana, no para un pipeline automatizado; se usa workload identity (GitHub Actions OIDC, workload identity cloud, federación de service accounts o un issuer OIDC interno) con política que exija repositorio aprobado, rama/tag protegida y validaciones. (Firma criptográfica de modelos)

P: ¿Qué preguntas clave hay que hacer a un proveedor de modelos o APIs de terceros?
R: Qué datos del cliente llegan y si se usan para entrenar, cómo se aíslan datos/prompts/embeddings/logs/salidas, qué pasa al cambiar modelo/versión/región/control, qué eventos disparan notificación y con qué rapidez, y cuál es el plan de contingencia ante caída o compromiso. (Gestión y escaneo de dependencias)

P: ¿Qué fallo sutil puede romper el aislamiento de inquilino en la capa de orquestación?
R: Validar el grano fino de un identificador confiando en el grueso que realmente define al inquilino, o un fallback de coincidencia parcial que amplía el alcance; hay que nombrar la clave exacta, autorizarla en cada fetch y evitar fallbacks que amplíen el alcance. (Seguridad de arquitectura multiinquilino)

P: ¿Cuál es el patrón seguro de aplicación de inquilino a nivel de prompt?
R: Autenticar al llamante, resolver pertenencia al inquilino, autorizar la operación, adjuntar el scope a cada recuperación o llamada a herramienta, validar que el resultado pertenece al mismo inquilino y registrar evidencia; el prompt describe la regla, la política la aplica fuera del modelo. (Aislamiento de GPU, prompt y runtime)

## Puntos a dominar

- Explicar que la confianza en IA es transitiva y nombrarla por las cinco clases de dependencia para poder validarla, monitorizarla y revocarla.
- Reconocer que la frontera de seguridad y el mayor radio de impacto están en la capa de integración/orquestación, no en el modelo.
- Recorrer el flujo de validación de modelos: fuente y model card, integridad por hashes/firmas, inspección, sandbox y promoción solo del artefacto firmado al registro interno.
- Justificar la firma criptográfica con workload identity y el principio validar antes de firmar, firmar antes de desplegar, fail closed.
- Argumentar por qué pickle puede ejecutar código y defender safetensors, cuarentena del pickle no confiable y bloqueo de rutas de carga inseguras en producción.
- Distinguir SBOM frente a VEX y qué añade el AI SBOM (linaje de modelo, datasets, hashes, licencias, historial).
- Ordenar los patrones de aislamiento en vector databases y recordar que la aplicación de inquilino vive en el servidor, no en el prompt.
- Situar el aporte y los límites de NVIDIA MIG para aislamiento de GPU.
- Encadenar la respuesta a incidentes (NIST SP 800-61 Rev. 3): contención, mapeo de exposición, erradicación, recuperación y revisión, ensayando el compromiso antes de que ocurra.
