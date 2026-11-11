# Data Munging: String Manipulation, Regular Expressions, and Data Cleaning — Estudio

## Tarjetas de repaso

P: ¿En qué dos grandes tipos divide el autor las patologías de los datos? / R: Problemas de formato (capitalización inconsistente, espacios sobrantes…), normalmente resolubles con preprocesado; y problemas de contenido (duplicados, outliers, NULLs), que exigen interpretar qué significan.

P: ¿Por qué considera el autor que la manipulación de cadenas es tan potente como la machine learning? / R: Resuelve cualquier problema de formato y a menudo es la única solución viable, y permite escribir scripts rápidos que extraen la información concreta que se necesita.

P: ¿Qué cuatro consejos da para identificar problemas pronto? / R: Mirar el archivo crudo si es texto, leer la documentación de apoyo, tener preguntas diagnósticas estándar (NULLs, identificadores comunes entre tablas) y hacer sanity checks derivando algo ya conocido.

P: ¿Qué es un sanity check? / R: Derivar de los datos algo que ya conoces; si, por ejemplo, el recuento de clientes no coincide con el conocido, probablemente no los estás identificando bien.

P: ¿Qué significan normalmente los NULLs y cómo se tratan? / R: Normalmente que no se conoce un dato; como muchos algoritmos no los procesan, suelen sustituirse por un valor razonable (estimado de otros campos o la media de los no nulos).

P: ¿Cuándo un NULL puede ser una feature informativa? / R: Cuando surge porque ese dato nunca se recogió para ciertas entidades; el hecho de ser NULL puede identificarlas (p. ej. la fábrica de origen).

P: ¿Qué tres cosas pueden indicar los valores atípicos enormes (outliers)? / R: Un evento real, algo que debe filtrarse (un pico de tráfico suele ser un ataque de bots) o datos faltantes codificados con un valor arbitrario predeterminado.

P: ¿Por qué son insidiosos los espacios sobrantes y cómo se eliminan en Python? / R: No se ven al imprimir y arruinan uniones ("ABC" vs " ABC "); `strip()` quita espacios de ambos extremos y `lstrip()`/`rstrip()` solo del inicio o del final.

P: ¿Qué hacen `lower()` y `upper()`? / R: Devuelven una copia de la cadena en minúsculas o en mayúsculas, para corregir capitalización irregular.

P: ¿De cuántas formas puede codificarse un NULL en un CSV? / R: De muchas, y todas deben leerse como NULL: cadena vacía `""`, `NA`, `NULL`, y a veces `unavailable` o `unknown`.

P: ¿Para qué sirve `decode()` con el argumento `"ignore"`? / R: Para convertir texto con bytes no válidos descartando los caracteres inválidos en lugar de fallar.

P: ¿Qué recomienda el autor para manejar fechas y horas? / R: Pasarlas cuanto antes al tipo datetime nativo; en Python el paquete `dateutil` parsea bien formatos dispares y redondea hacia abajo.

P: ¿Qué son las expresiones regulares y qué inconvenientes tienen? / R: La "artillería pesada" que generaliza split o indexado a patrones; son delicadas de usar y depurar (conviene mantenerlas cortas) y costosas computacionalmente, incluso al compilarlas.

P: ¿Qué diferencia hay entre evaluación greedy y nongreedy? / R: Greedy (por defecto) busca el match más largo desde la izquierda; nongreedy, con `?`, busca el camino más corto (p. ej. `<name>.*?</name>` devuelve dos matches en vez de capturar todo).

P: ¿Qué son las raw strings y por qué usarlas en regex? / R: Cadenas con una `r` antes de la comilla que evitan el dolor del escape `\`; así `r"\n"` conserva barra y `n`, que es lo que `re.compile` espera, sin tener que escribir `"\\n"`.

## Preguntas de autoevaluación

P: ¿Qué lección extrae el autor de su "peor dataset del mundo"? / R: Que todos los datasets son así: donde hay una organización grande, un proceso de recolección complejo o datasets fusionados, los problemas se acumulan y rara vez están documentados. (Sección "El peor dataset del mundo y cómo detectar patologías".)

P: ¿Por qué conviene cierta paranoia al procesar datos? / R: Porque uno de los peores escándalos en data science es tener que retractar resultados por haber procesado mal los datos. (Sección "El peor dataset del mundo y cómo detectar patologías".)

P: ¿Cómo se corrigen las entradas faltantes cuando faltan entidades? / R: Suele haber una característica común que las excluyó (p. ej. clientes sin transacciones al agrupar por cliente); se arregla uniendo contra un conjunto conocido de todas las entidades. (Sección "Problemas de contenido de los datos".)

P: ¿Cuándo son legítimas varias entradas para una misma entidad? / R: Cuando debe haberlas, como un generador con varios motores idénticos que reportan con el mismo número de serie (suelen venir en orden fijo), o cuando la misma entidad se procesa dos veces. (Sección "Problemas de contenido de los datos".)

P: ¿Qué caracteriza al script de formateo de ejemplo del autor? / R: Normaliza cada campo (nombres sin títulos, edad solo dígitos, fechas a AAAA-MM-DD) con funciones aplicadas vía `df["col"].apply(...)`; no es elegante ni eficiente, pero es claro, funciona y es fácil de modificar. (Sección "Script de formateo de ejemplo".)

P: ¿Qué hace el ejemplo de `ab*` y qué significa el `*`? / R: Coincide con una `a` seguida de cualquier número (incluido 0) de `b`; el `*` repite el carácter anterior cero o más veces. (Sección "Expresiones regulares".)

P: Según el autor, ¿por qué es un capítulo corto y qué lugar ocupa la limpieza en el flujo de trabajo? / R: Porque la limpieza de datos generaliza mal; es la parte tediosa pero intelectualmente exigente, con normalmente una única forma "correcta", y su código se escribe una vez y se reutiliza entre iteraciones antes de pasar a visualización y análisis exploratorio. (Sección "Vida en las trincheras".)

## Puntos a dominar

- Distinguir problemas de formato (preprocesables) de problemas de contenido (requieren interpretación).
- Aplicar las cuatro tácticas de detección temprana: mirar el archivo crudo, leer la documentación, usar preguntas diagnósticas y hacer sanity checks.
- Reconocer las patologías de contenido: duplicados, múltiples entradas por entidad, faltantes, NULLs, outliers, datos obsoletos, entradas artificiales y espaciados irregulares.
- Tratar NULLs sustituyéndolos por un valor razonable, salvo cuando su ausencia es en sí una feature.
- Manejar métodos de cadenas de Python (`strip`, `lstrip`/`rstrip`, `lower`/`upper`, `decode`) y normalizar fechas con `dateutil`.
- Leer como NULL todas sus codificaciones en CSV (`""`, `NA`, `NULL`, `unavailable`, `unknown`).
- Escribir un script de formateo claro aunque improvisado y cargarlo en un DataFrame de Pandas.
- Dominar la sintaxis básica de regex (`*`, `+`, `?`, `{n}`, `[...]`, `|`, `^`, `$`, `.`, `\s`, `\w`), greedy vs nongreedy, y el uso de raw strings y `re.findall` con patrones cortos.
