# Agentes para apuntes de libros

Familia de agentes (en `.kiro/agents/`) que cubre el flujo completo de apuntes de libros en PDF. Son genéricos: reciben rutas como parámetros y funcionan en cualquier carpeta `apuntes/` (ciberseguridad, data-science u otras). Las reglas comunes están en [convenciones.md](convenciones.md).

> Este README vive aquí y no en `.kiro/agents/` para que `kiro-cli` no lo interprete como un perfil de agente.

## Flujo recomendado

```
PDF → pdf-splitter → capNN.txt + manifest.json
                   → note-writer → apuntes/<libro>/capNN-*.md
                                 → notes-formatter   (formato)
                                 → notes-verifier    (fidelidad, usa el .txt)
                                 → book-indexer      (README.md + _glosario.md)
                                 → cross-book-linker (apuntes/_conexiones.md)
                                 → study-aid-generator (apuntes/_estudio/…)
```

## Agentes

| Agente | Herramientas | Entrada (en el prompt) | Salida |
|---|---|---|---|
| `pdf-splitter` | read, write, shell | ruta del PDF, slug del libro, directorio de trabajo | `<trabajo>/<libro>/capNN-slug.txt` y `manifest.json` |
| `note-writer` | read, write | `.txt` del capítulo, ruta de salida `.md` (dentro de una carpeta `apuntes/`), metadatos del libro y del capítulo | `apuntes/<libro>/capNN-*.md` |
| `notes-formatter` | read, write | ruta de UN apunte | el mismo apunte, con correcciones mecánicas; reporta lo pendiente |
| `notes-verifier` | read, write | apunte, `.txt` fuente, ruta del fragmento | `apuntes/<libro>/_verificacion.d/capNN.md` (se unen con `merge_verificacion.py`) |
| `book-indexer` | read, write, shell | carpeta `apuntes/<libro>/` | `README.md` y `_glosario.md` |
| `cross-book-linker` | read, write | carpeta `apuntes/` con varios libros indexados | `apuntes/_conexiones.md` |
| `study-aid-generator` | read, write | apunte, ruta de salida | `apuntes/_estudio/<libro>/capNN-estudio.md` |

Cada agente responde con una sola línea (`capNN listo…`, `ERROR: motivo`).

## Scripts (en `scripts/`)

- `split_pdf.py`: divide un PDF por su outline y genera el manifiesto. Lo usa `pdf-splitter`. Sale con 3 si no hay outline y con 4 si no hay capa de texto.
- `run_agent.py`: lanza un agente con `kiro-cli chat --no-interactive` sobre una lista de tareas en paralelo y valida antes las rutas `require`.
- `merge_verificacion.py`: une los fragmentos de `_verificacion.d/` en `_verificacion.md`.
- `make_tasks.py`: genera el `.jsonl` de tareas (una por capítulo) para `run_agent.py` a partir del `manifest.json`. Soporta `note-writer`, `notes-formatter`, `notes-verifier` y `study-aid-generator`, con `--skip-existing` para reanudar.

Opciones extra de `split_pdf.py` para PDFs difíciles: `--expand REGEX` (capítulos bajo partes/secciones), `--toc-pages A-B --offset auto` (sin outline, tabla de contenido en texto), `--chapters-file` (manual), `--single TÍTULO` (artículos), `--merge REGEX` (fundir apartados diminutos con el anterior) y `--skip REGEX`. El manifiesto incluye `rango_palabras` por capítulo según su tamaño.

## Cómo ejecutarlos

El registro de sub-agentes del IDE no reconoció los agentes del workspace durante las pruebas (`invoke_sub_agent` devolvió "not found in registry"), aunque `kiro-cli agent list` sí los ve. Por eso se lanzan con `scripts/run_agent.py`.

Tareas en un `.jsonl` (una por línea):

```json
{"label": "cap01", "prompt": "Verifica el apunte /ruta/cap01.md contra el texto fuente /tmp/trabajo/libro/cap01.txt. Escribe el fragmento en /ruta/_verificacion.d/cap01.md", "require": ["/ruta/cap01.md", "/tmp/trabajo/libro/cap01.txt"]}
```

```bash
python3 scripts/run_agent.py --agent notes-verifier --tasks tareas.jsonl --workers 4
# agentes que usan shell (pdf-splitter, book-indexer) necesitan además:
python3 scripts/run_agent.py --agent book-indexer --trust fs_read,fs_write,execute_bash --prompt "Indexa la carpeta /ruta/apuntes/libro"
python3 scripts/merge_verificacion.py /ruta/apuntes/libro
```

## Ejemplo completo

```bash
# 1. Dividir el PDF
python3 scripts/run_agent.py --agent pdf-splitter --trust fs_read,fs_write,execute_bash \
  --prompt "Divide el PDF /ruta/libro.pdf. Slug: mi-libro. Directorio de trabajo: /tmp/trabajo"
# 2. Escribir apuntes (una tarea por capítulo, desde /tmp/trabajo/mi-libro/manifest.json)
# 3. Formato, verificación, índice, conexiones y estudio con los agentes de la tabla
```

## Notas

- Respuestas largas: una sola escritura de un archivo grande puede cortarse por tiempo del stream (error `-32603`). `note-writer` y `cross-book-linker` escriben por partes (crear y luego append). Si una tarea falla con `rc=1`, relánzala con `--skip-existing`.
- Si el equipo entra en reposo durante una ejecución, algunas tareas pueden colgarse; `run_agent.py` las corta al llegar a `--timeout` y se pueden relanzar.
- *Dive Into Design Patterns* se extrae con palabras pegadas; los agentes lo interpretan por contexto (usa `--nota` en `make_tasks.py`).
- Los temporales (texto extraído) viven en `/tmp`; `notes-verifier` necesita el `.txt` de cada capítulo, así que hay que volver a ejecutar `pdf-splitter` si se borró.
- `book-indexer` tolera apuntes de formato antiguo (sin "Lo que necesitas saber" / "Ideas clave"). `notes-formatter` los reporta como no conformes.
- Cada ejecución consume uso de la cuenta de Kiro; la verificación o el estudio de un libro completo son decenas de tareas.
