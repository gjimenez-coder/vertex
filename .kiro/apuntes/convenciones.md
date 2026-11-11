# Convenciones de apuntes de libros

Documento compartido por todos los agentes de apuntes (`note-writer`, `pdf-splitter`, `notes-formatter`, `notes-verifier`, `book-indexer`, `cross-book-linker`, `study-aid-generator`).

## Reglas generales

- Idioma: español. Los términos técnicos estándar se mantienen en inglés (prompt injection, XSS, CSRF, threat modeling, overfitting, etc.).
- No se añade contenido ajeno al libro: nada de opiniones, ampliaciones ni datos externos.
- Cada agente responde con UNA sola línea. Si hay problema: `capNN ERROR: motivo`.
- Citas textuales: pocas, de máximo 25 palabras, con página como `(PDF p. N)`.
- Código, comandos o payloads: solo si ilustran un concepto o una defensa del libro, en bloques de código y de forma fiel.
- Cifras, nombres, herramientas y marcos (OWASP, MITRE ATLAS, NIST, etc.) deben coincidir exactamente con el texto fuente.

## Estructura de directorios

```
<raiz>/apuntes/
  <libro>/                      # kebab-case, ej. ai-under-attack
    capNN-titulo-kebab.md       # un apunte por capítulo (cap00 = prólogo)
    README.md                   # índice del libro            (book-indexer)
    _glosario.md                # glosario del libro          (book-indexer)
    _verificacion.md            # reporte de fidelidad        (notes-verifier)
  _conexiones.md                # enlaces entre libros        (cross-book-linker)
  _estudio/<libro>/capNN-estudio.md   # material de estudio   (study-aid-generator)
```

Los archivos con prefijo `_` y `README.md` NO son capítulos.

## Plantilla de apunte de capítulo (nivel condensado)

```markdown
# {Título del libro} — {Autor(es)} ({Editorial, año})
## Capítulo {N} — {Título original} ({traducción al español})

> Nota de extracción: una línea indicando que el texto se extrajo de la capa de texto del PDF y que las citas usan la página del PDF.

## Lo que necesitas saber
(2 a 4 párrafos: de qué trata, tesis central, qué sales sabiendo.)

## El ejemplo que recorre el capítulo
(Solo si hay un caso o ejemplo hilo conductor. Si no, se omite.)

## {Un apartado ## por cada sección principal}
(Conceptos, definiciones, listas y tablas breves, ejemplos/código esenciales.)

## Ideas clave
(5 a 8 viñetas de repaso.)
```

- Prólogo (capítulo 0): `## Prólogo — {Título} ({traducción})` en lugar de `## Capítulo N`.
- Longitud objetivo: 600 a 1400 palabras por defecto, proporcional al capítulo (los capítulos muy cortos pueden ser más breves). `pdf-splitter` escribe un `rango_palabras` por capítulo en el manifiesto y el prompt de `note-writer` puede indicarlo: capítulos de hasta 25 páginas 600-1400, hasta 45 páginas 900-1800, más largos 1200-2200.
- Nombre de archivo: `capNN-titulo-en-kebab-case.md`, con NN de dos dígitos.

## Salida de `pdf-splitter`

`<trabajo>/<libro>/capNN-slug.txt`: texto del capítulo con marcadores `[[PDF p.N]]` al inicio de cada página.
`<trabajo>/<libro>/manifest.json`:

```json
{
  "libro": "slug",
  "pdf": "ruta/al.pdf",
  "paginas_pdf": 565,
  "desfase_folio": null,
  "capitulos": [
    {"num": 1, "titulo": "Título original", "name": "cap01-slug", "inicio": 46, "fin": 68, "palabras": 5937, "rango_palabras": [600, 1400]}
  ]
}
```

`desfase_folio` = página PDF − folio impreso, o `null` si no se pudo determinar.

## Formato de los archivos `_*`

- `README.md`: título del libro, autores, y una lista `- [Capítulo N — Título](capNN-slug.md): una línea de resumen`.
- `_glosario.md`: `- **Término**: definición tomada de los apuntes (capNN)`, en orden alfabético.
- `_verificacion.md`: tabla por capítulo con hallazgos (afirmación sin respaldo, término mal escrito, sección omitida), severidad y evidencia; al final un conteo total.
- `_conexiones.md`: por tema, los libros y capítulos relacionados, con enlaces relativos, y una frase de qué los conecta.
- `_estudio/<libro>/capNN-estudio.md`: secciones `## Tarjetas de repaso`, `## Preguntas de autoevaluación` (con respuesta) y `## Checklist`, todo derivado del apunte.

## Variante: apuntes de examen o certificación (por dominio)

Se usa cuando el material combina varias fuentes (guías en PDF, slides, banco de preguntas, lecciones web) y el apunte se organiza por DOMINIO del examen, no por capítulo de un libro. Las reglas generales siguen vigentes; esta variante solo cambia la plantilla, el nombre de archivo y las citas.

```
<raiz>/apuntes/<certificacion>/
  dominioN-titulo-kebab.md      # un apunte por dominio       (ensamblado desde _partes/)
  _partes/dN/N.M.md             # fragmentos por tarea        (exam-note-writer, modo tarea)
  _partes/dN/_intro.md          # 'Lo que necesitas saber'    (exam-note-writer, modo dominio)
  _partes/dN/_ideas.md          # 'Ideas clave'               (exam-note-writer, modo dominio)
  README.md  _glosario.md  _verificacion.md  _estudio/dominioN-estudio.md
```

Plantilla del apunte de dominio:

```markdown
# {Certificación} — {Entidad} ({guía de examen, año})
## Dominio {N} — {Título en inglés} ({traducción al español})

> Nota de extracción: fuentes usadas, tipos de cita y discrepancias entre fuentes.

## Lo que necesitas saber
(2 a 4 párrafos: de qué trata el dominio, su peso en el examen, qué sales sabiendo.)

## Tarea {N.M} — {Título original} ({traducción})
> Prioridad de estudio: … (solo si es un tema débil del usuario)

### {Concepto}
**Concepto:** nombre y explicación breve en 1-2 frases.

**Ejemplos de uso (3, cortos):**
1. …
2. …
3. …

**Qué NO hacer:** (solo si hay riesgo de confusión)
- …

**Posible confusión con otros conceptos:** (solo si aplica)
- {Concepto A} — ejemplo corto
- {Concepto B} — ejemplo corto

### Trampas del examen
(distractores típicos del banco de preguntas y por qué fallan, con la cita de cada pregunta)

(… una sección `## Tarea N.M` por cada tarea del dominio, en orden …)

## Ideas clave
(8 a 12 viñetas de repaso del dominio.)
```

- Sin límite de palabras: se prioriza la completitud. El validador no exige rango en estos apuntes.
- Nombre de archivo: `dominioN-titulo-en-kebab-case.md`. Los fragmentos `_partes/` no son apuntes finales.
- Citas (cada afirmación lleva su fuente): `(Guía PDF p. N)` y `(Slides PDF p. N)` para PDFs, donde N es el número del marcador `[[PDF p.N]]` bajo la fuente correspondiente; `(web N.M)` para las lecciones web; `(QN)` para el banco de preguntas. El material de refuerzo del usuario solo sirve para marcar prioridad de estudio y no se cita como fuente de contenido.
- Prioridad entre fuentes: guía PDF y banco de preguntas prevalecen sobre las lecciones web (sitio de terceros). Si se contradicen, se anota la contradicción en la tarea.
- La nota de extracción registra la discrepancia de nombre y tamaño del examen entre fuentes sin decidir cuál es la correcta.
