# AI Under Attack: A Practical Guide to Threats, Defenses, and Governance for AI Systems — Kris Kimmerle & David Okeyode (Packt Publishing, 2026)
## Capítulo 17 — External Dependencies, Supply Chain Integrity and Multi-Tenant Risk (Dependencias externas, integridad de la cadena de suministro y riesgo multiinquilino)

> Nota de extracción: el texto se obtuvo de la capa de texto del PDF y las citas usan la página del PDF.

## Lo que necesitas saber
El capítulo sostiene que el riesgo de cadena de suministro en IA rara vez llega disfrazado de amenaza evidente: entra como un model checkpoint, un tokenizer, una integración de vector database, un paquete de Python, una API de inferencia hospedada, un dataset, una imagen de contenedor o un SDK de proveedor que ayuda al equipo a ir más rápido. Los sistemas de IA se construyen con código, datos, modelos, infraestructura y servicios ajenos, de modo que una aplicación cuidadosamente revisada hereda igualmente riesgo de cada artefacto que carga y cada servicio en el que confía.

La tesis central es que la confianza es transitiva y debe hacerse explícita para poder validarla, monitorizarla y revocarla. No se trata de eliminar la confianza en terceros, sino de nombrarla por clases de dependencia (modelo, código, datos, infraestructura, proveedor) para asignar controles concretos. En entornos multiinquilino, una dependencia débil amplía el radio de impacto porque la aplicación reutiliza modelos, GPUs, índices, pipelines de logging y capas de orquestación entre clientes.

Sales sabiendo cómo validar la procedencia de un modelo, firmar artefactos criptográficamente, contener la amenaza de serialización con pickle, gestionar dependencias con SBOM/VEX, diseñar aislamiento multiinquilino (vector databases, GPU, prompts), y responder a incidentes de cadena de suministro. El capítulo se detiene deliberadamente antes del problema completo de seguridad de agentes, que retoma el Capítulo 18.

## El ejemplo que recorre el capítulo
El caso conductor es un agente de IA nacional de gestión de arrendamientos que atiende preguntas de prospectos y residentes en miles de comunidades. El modelo conversacional casi no tiene autoridad: un servicio de integración separado resuelve el usuario y la comunidad, ensambla la respuesta y envía todo el paquete al modelo. La autoridad efectiva del modelo es lo que ese servicio decide poner en el payload, por lo que la capa de integración —no el modelo— es la frontera de seguridad.

Ese mismo nivel concentra el riesgo de dependencias: mantiene conexiones permanentes a los sistemas back-end de cada cliente, con un registro de credenciales por inquilino para cada plataforma soportada. La función de IA no añadió una integración externa, sino que acumuló una ruta alcanzable al sistema de registro de cada inquilino, convirtiendo la capa de orquestación en el objetivo de mayor valor de la arquitectura.

## La superficie de ataque de la cadena de suministro de IA
Una cadena de suministro tradicional ya incluye código fuente, paquetes, sistemas de build, contenedores, servicios cloud e identidades de CI/CD. La IA añade pesos de modelo, tokenizers, embeddings, datasets, índices de recuperación, plantillas de prompt, arneses de evaluación, librerías de guardrails, herramientas de anotación y APIs de modelos hospedados. Cada una es una decisión de confianza.

Conviene pensar en clases de dependencia:
- Dependencias de modelo: afectan el comportamiento de salida y la seguridad de carga.
- Dependencias de código: afectan la ejecución.
- Dependencias de datos: afectan lo que el sistema aprende o recupera.
- Dependencias de infraestructura: afectan aislamiento, telemetría y recuperación.
- Dependencias de proveedor: afectan contrato, cumplimiento, residencia y visibilidad ante incidentes.

"Si no puedes nombrar la clase, te costará nombrar el control" (PDF p. 368).

## Procedencia y validación del modelo
Descargar un modelo de un repositorio público debería parecerse más a instalar software de producción que a bajar un archivo multimedia. El flujo de validación avanza por etapas:
1. Confirmar fuente y uso previsto: ¿es el repositorio oficial, un fork, una conversión comunitaria o un resubido aleatorio? ¿El model card describe datos de entrenamiento, licencia, uso, límites y seguridad?
2. Verificar integridad: registrar hashes de cada artefacto aprobado; validar firmas/atestaciones si existen. Sin firma confiable, tratar la descarga como no confiable hasta que tu propio pipeline firme el artefacto exacto.
3. Inspeccionar el artefacto antes de cargarlo en un entorno privilegiado. Herramientas como ModelScan detectan patrones de serialización riesgosos, pero el escaneo estático no es prueba de seguridad.
4. Probar comportamiento en sandbox con prompts conocidos, sondas adversariales, límites de recursos y logging, vigilando accesos de red/archivo inesperados, presión de memoria y deserialización insegura.

Registro interno de modelos: es donde la validación se vuelve operativa. Debe guardar el artefacto aprobado, URL de origen, hashes, firmas, model card, decisión de licencia, resultados del escáner, resumen de pruebas de comportamiento, propietario, fecha de aprobación, entornos de despliegue y ruta de revocación. Producción solo carga desde la ruta aprobada del registro.

## Firma criptográfica de modelos
La firma vincula un artefacto aprobado a una identidad y un punto en el tiempo. El trabajo de model-signing de OpenSSF y la firma keyless estilo Sigstore conectan la integridad del artefacto con identidad verificable, en lugar de gestionar claves privadas de larga duración a mano. La idea: validar antes de firmar y exigir la firma antes de desplegar. "Fírmalo porque un proceso definido revisó la fuente, formato, hash, licencia, escáner y comportamiento en sandbox" (PDF p. 370).

Firma headless en CI/CD: el login por navegador sirve para una demo humana, no para un pipeline automatizado. Usa workload identity (GitHub Actions OIDC, workload identity cloud, federación de service accounts, o un issuer OIDC interno). La política debe exigir que el build corra desde un repositorio aprobado, en rama/tag protegida, tras pasar validaciones, con una service account limitada a promoción de modelos. Si cambia la identidad o se salta el escáner, la firma debe fallar en cerrado (fail closed).

Validación en Kubernetes: bloquear artefactos no aprobados antes de que arranque el contenedor de serving, mediante admission control, init containers, sidecars o un operador de validación. Los chequeos deben ejecutarse antes de la carga del modelo, no tras la primera inferencia.

## La amenaza de serialización con pickle
Pickle es peligroso porque es más que un formato pasivo: cargar datos pickle puede ejecutar código Python, lo que acerca los archivos de modelo basados en pickle al software ejecutable. La lección operativa es antigua y simple: nunca deserializar objetos Python no confiables en un entorno con secretos, alcance de red, archivos escribibles o credenciales de producción.

Límites de los escáneres: detectan opcodes peligrosos conocidos, globals sospechosos o estructuras inseguras, pero son un filtro, no una garantía; los atacantes se adaptan. Un escaneo limpio es solo una entrada más junto a verificación de fuente, hash, preferencia de formato, carga en sandbox, pruebas de comportamiento, restricciones de red y aprobación humana.

Migración a safetensors: safetensors es mejor opción por defecto porque almacena tensores sin usar la ejecución de pickle durante la carga; elimina un riesgo mayor, aunque no exime de evaluar fuente, licencia y comportamiento.
- Preferir safetensors u otros formatos no ejecutables en nuevas entradas de modelo.
- Poner en cuarentena artefactos basados en pickle hasta completar chequeos.
- Bloquear rutas de carga inseguras en producción.
- Guardar registros de conversión.
- No dejar que una demo urgente cree una excepción permanente a la política de carga.

## Gestión y escaneo de dependencias
La gestión de dependencias de IA sigue siendo gestión de dependencias de software: versiones fijadas (pinned), monitoreo de vulnerabilidades, mirrors privados cuando convenga, revisión de dependencias transitivas y un propietario que decida si una vulnerabilidad es explotable. Usa varias fuentes de evidencia: OSV-Scanner, pip-audit, GitHub Advisory Database, NVD, avisos de proveedores y la salida de auditoría del gestor de paquetes. El flujo útil conecta la alerta con el artefacto, despliegue, exposición del inquilino y controles compensatorios.

SBOM, VEX y evidencia de build: el SBOM da inventario; el VEX explica si una vulnerabilidad conocida es explotable en un contexto concreto. Para IA, el inventario debe extenderse al linaje del modelo, datasets, evidencia de entrenamiento/evaluación, hashes, licencias e historial de actualizaciones. Las guías de AI SBOM de CISA/G7, SPDX y CycloneDX dan formas estructuradas de intercambiar datos. El inventario importa más durante una mala semana, para saber qué servicios, inquilinos y entornos están expuestos y quién remedia.

Riesgo de modelos y APIs de terceros: los proveedores hospedados mueven trabajo, no todo el riesgo. Preguntas clave: ¿qué datos del cliente llegan al proveedor y se usan para entrenar? ¿cómo se aíslan datos, prompts, embeddings, logs y salidas? ¿qué pasa cuando cambia un modelo, versión, región o control de seguridad? ¿qué eventos disparan notificación y con qué rapidez? ¿cuál es el plan de contingencia si el proveedor cae o queda comprometido?

## Seguridad de arquitectura multiinquilino
La multiinquilinidad es donde el riesgo de cadena de suministro se encuentra con el radio de impacto. Modelos, índices, GPUs, colas y pipelines de monitoreo compartidos reducen costes pero crean rutas por donde un fallo afecta a varios clientes.

El mayor radio de impacto suele estar en la capa de orquestación que ensambla cada respuesta, no en un modelo o índice compartido. Esa capa también concentra el riesgo de dependencias (conexiones per-tenant) y es donde las fronteras de inquilino se aplican o no. Fallos sutiles: una verificación valida el grano fino de un identificador mientras confía en el grueso que realmente define al inquilino, y un fallback de coincidencia parcial amplía el alcance. Al diseñar: nombra la clave exacta que define al inquilino, autorízala en cada fetch y evita que cualquier fallback amplíe el alcance.

Economía del aislamiento: desconfía de multiplicadores de coste exactos. La afirmación defendible es cualitativa: un aislamiento más fuerte suele costar más porque duplica cómputo, almacenamiento, planos de control, monitoreo, pipelines y soporte. El nivel de aislamiento debe corresponder al riesgo del inquilino.

Patrones de aislamiento en vector databases:
- Silo físico por inquilino: frontera más fuerte, mayor sobrecarga operativa.
- Colección/índice dedicado por inquilino: frontera lógica fuerte, riesgo moderado de plataforma compartida.
- Partición por namespace: útil cuando la plataforma la aplica y hay pruebas.
- Filtro de metadatos: solo como defensa en profundidad, nunca como única frontera para datos sensibles.

La aplicación del inquilino pertenece al lado del servidor: el cliente no decide qué namespace puede consultar. El servicio deriva el inquilino del contexto autenticado, autoriza la operación, adjunta el scope y registra la decisión. "Si el prompt dice consultar otro inquilino, el prompt es irrelevante" (PDF p. 376).

## Aislamiento de GPU, prompt y runtime
NVIDIA Multi-Instance GPU (MIG) particiona GPUs de datacenter compatibles en instancias aisladas por hardware con recursos dedicados, lo que es más fuerte que un scheduler de software que promete equidad. MIG reduce el riesgo de que un inquilino agote recursos o observe otra carga por contención. Pero no es una frontera completa por sí sola: el SO host, plugins de dispositivo, scheduler de Kubernetes, driver, runtime de contenedor, red, secretos, logs y capa de serving siguen necesitando controles.

Aplicación de inquilino a nivel de prompt: las instrucciones de prompt pueden recordar al modelo mantenerse en su inquilino, pero no pueden ser la frontera. Un atacante no debe cambiar de inquilino escribiendo una mejor frase. El patrón seguro: autenticar al llamante, resolver pertenencia al inquilino, autorizar la operación, adjuntar el scope a cada recuperación o llamada a herramienta, validar que el resultado pertenece al mismo inquilino y registrar evidencia. El prompt describe la regla; la política la aplica fuera del modelo.

Monitoreo de dependencias externas: vigilar avisos de seguridad y comportamiento. Rastrear avisos de paquetes, runtimes de serving, clientes de vector database y SDKs; registrar hashes y firmas aprobados; alertar cuando producción carga un artefacto fuera del registro aprobado; monitorizar intentos de acceso cross-tenant y desajustes de inquilino en resultados; vigilar changelogs y avisos de incidentes de proveedores.

## Respuesta a incidentes de compromiso de la cadena de suministro
Los incidentes de cadena de suministro castigan a quienes improvisan el inventario bajo presión. La guía NIST (SP 800-61 Rev. 3) empuja preparación, detección, análisis, contención, erradicación, recuperación y mejora en un ciclo repetible.

Flujo compacto: empezar por contención (deshabilitar el artefacto, bloquear el paquete, poner en cuarentena el modelo, revocar el token, fijar la versión previa conocida-buena, o aislar el inquilino afectado). Luego mapear exposición: qué servicios cargaron la dependencia, qué inquilinos la usaron, qué datos cruzaron, qué credenciales eran alcanzables y qué logs prueban impacto. La erradicación quita la dependencia comprometida y cierra la ruta de entrada; la recuperación restaura desde artefactos aprobados; la revisión posterior actualiza política de validación, requisitos del registro, reglas de monitoreo, chequeos de compra y ejercicios de laboratorio.

## Construir un programa seguro de cadena de suministro
Un programa maduro conecta desarrollo seguro, gestión de riesgo de cadena de suministro de software, inventario SBOM/VEX, evidencia de AI bill-of-materials y validación de artefactos en un solo modelo operativo. La pregunta útil es operativa: qué se puede bloquear automáticamente, qué necesita revisión y qué evidencia haría falta durante un incidente.
- Definir propietarios para modelos, datasets, índices vectoriales, APIs, paquetes e identidades de build.
- Exigir validación antes de la promoción al registro y del despliegue.
- Mantener SBOM, AI SBOM e inventario de modelos actualizados para responder en incidentes.
- Ligar hallazgos de vulnerabilidad a explotabilidad, exposición de inquilino y controles compensatorios.
- Ensayar un compromiso de dependencia antes de que el primero real te ensaye a ti.

## Ideas clave
- El riesgo de cadena de suministro de IA entra como artefactos cotidianos (modelos, paquetes, datasets, APIs, contenedores); la confianza es transitiva y debe hacerse explícita para validarla, monitorizarla y revocarla.
- Piensa por clases de dependencia (modelo, código, datos, infraestructura, proveedor) para asignar controles; si no nombras la clase, no nombrarás el control.
- La validación de modelos avanza por fuente, integridad (hashes/firmas), inspección (ModelScan), sandbox y promoción solo del artefacto firmado a un registro interno.
- Pickle puede ejecutar código al cargar; prefiere safetensors, pon en cuarentena pickle no confiable y trata un escaneo limpio como una entrada, no como garantía.
- Gestiona dependencias con versiones fijadas y múltiples fuentes (OSV-Scanner, pip-audit, GitHub Advisory DB, NVD), más SBOM/VEX y AI SBOM (CISA/G7, SPDX, CycloneDX).
- En multiinquilino, el mayor radio de impacto está en la capa de orquestación/integración; la frontera de inquilino se aplica en el servidor, no en el prompt.
- Patrones de aislamiento en vector databases de más a menos fuerte: silo físico, colección/índice dedicado, namespace, filtro de metadatos (solo defensa en profundidad); NVIDIA MIG aporta aislamiento de GPU por hardware pero no basta solo.
- La respuesta a incidentes (NIST SP 800-61 Rev. 3) empieza por contención y mapeo de exposición; ensaya el compromiso antes de que ocurra. El Capítulo 18 extiende esto a sistemas de agentes.
