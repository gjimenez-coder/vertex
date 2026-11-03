#!/usr/bin/env python3
"""Divide un PDF en capítulos y genera un manifiesto.

Modos de detección de capítulos (elige uno):
  (por defecto)      outline de primer nivel del PDF
  --expand REGEX     además, expande a sus hijos (segundo nivel) las entradas cuyo título casa con REGEX
                     (ej. --expand '^(part|section)' para partes que contienen capítulos)
  --toc-pages A-B    el PDF no tiene outline: lee la tabla de contenido en texto (páginas A a B)
                     con líneas "Chapter N. Título ..... folio"; --offset auto|K = página PDF - folio
  --chapters-file F  JSON manual: [{"titulo": "...", "inicio": 10, "fin": 25}, ...]
  --single TITULO    todo el PDF es un único capítulo (artículos)

Uso:
  split_pdf.py <pdf> --libro <slug> --out <dir_trabajo> [opciones] [--skip REGEX ...] [--dry-run]

Salida (en <dir_trabajo>/<libro>/):
  capNN-slug.txt   texto del capítulo con marcadores [[PDF p.N]] por página
  manifest.json    ver .kiro/apuntes/convenciones.md (incluye rango_palabras por capítulo)

Códigos de salida:
  0 ok | 2 error de uso | 3 el PDF no tiene outline | 4 el PDF no tiene capa de texto
"""
import argparse
import collections
import unicodedata
import json
import os
import re
import sys

try:
    import pypdf
except ImportError:  # pragma: no cover
    sys.exit("Falta pypdf: pip3 install pypdf")

DEFAULT_SKIP = [
    r"^part\s+\d+\s*:",              # "Part 1: Foundations"
    r"^[IVX]+\.\s",                  # "I. Recon"
    r"^(index|índice)$",
    r"^about the author",
    r"^other books",
    r"^(chapter\s+\d+:\s*)?unlock your exclusive",
    r"^(copyright|cover|title page|half title|contents|table of contents|dedication|colophon)",
    r"^(acknowledg|bibliograph|glossary|brief contents|about this book|about the cover|a few words on copyright|índice de contenido|cómo leer este libro)",
]

PREFACE_RE = re.compile(r"^(preface|prólogo|prologo|foreword|introduction|introducción)$", re.I)
_CACHE = {}


def slugify(title: str) -> str:
    t = re.sub(r"^(chapter\s+|section\s+|part\s+)?(\d+[:.\-—\s]|[ivx]+[:.\-—])\s*", "", title.strip(), flags=re.I).lower()
    t = t.replace("&", "and")
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "sin-titulo"


def page_text(reader, p):
    if p not in _CACHE:
        _CACHE[p] = reader.pages[p - 1].extract_text() or ""
    return _CACHE[p]


def outline_items(reader, expand_re):
    """Lista plana (título, página) de nivel superior; expande a los hijos las entradas que casen con expand_re."""
    out = []
    raw = list(reader.outline)
    k = 0
    while k < len(raw):
        it = raw[k]
        if isinstance(it, list):
            k += 1
            continue
        children = raw[k + 1] if k + 1 < len(raw) and isinstance(raw[k + 1], list) else None
        title = it.title.strip()
        page = reader.get_destination_page_number(it) + 1
        if children and expand_re and expand_re.search(title):
            kids = [c for c in children if not isinstance(c, list)]
            for c in kids:
                out.append((c.title.strip(), reader.get_destination_page_number(c) + 1))
        else:
            out.append((title, page))
        k += 1
    return out


def toc_items(reader, a, b, offset):
    """Entradas 'Chapter N. Título ..... folio' (y Preface/Foreword/Bibliography) de la tabla de contenido en texto."""
    lines = []
    for p in range(a, b + 1):
        lines += page_text(reader, p).splitlines()
    rx = re.compile(r"^\s*(.+?)\s*\.{3,}\s*(\d+)\s*$")
    items = []
    for ln in lines:
        m = rx.match(ln)
        if not m:
            continue
        title, folio = m.group(1).strip(), int(m.group(2))
        if re.match(r"^chapter\s+\d+\.", title, re.I) or re.match(r"^(foreword|preface|bibliography|references)$", title, re.I):
            items.append((title, folio))
    if offset == "auto":
        first = next((t for t in items if re.match(r"^chapter\s+1\.", t[0], re.I)), None)
        if not first:
            return None
        name = re.sub(r"^chapter\s+1\.\s*", "", first[0], flags=re.I).lower()
        for p in range(first[1], min(len(reader.pages), first[1] + 40) + 1):
            head = " ".join(page_text(reader, p).split()[:25]).lower()
            if name[:25] in head and "..." not in head:
                offset = p - first[1]
                break
        else:
            return None
    return [(t, f + int(offset)) for t, f in items]


def detect_offset(reader, start, end):
    """Desfase = página PDF - folio impreso, por votación sobre números sueltos al inicio/fin de página."""
    votes = collections.Counter()
    for p in range(start, end + 1):
        lines = [l.strip() for l in page_text(reader, p).splitlines() if l.strip()]
        for cand in (lines[:1] + lines[-1:]):
            m = re.fullmatch(r"(\d{1,4})", cand)
            if m:
                votes[p - int(m.group(1))] += 1
    if not votes:
        return None
    off, n = votes.most_common(1)[0]
    return off if n >= 3 else None


def rango_palabras(paginas):
    if paginas <= 25:
        return [600, 1400]
    if paginas <= 45:
        return [900, 1800]
    return [1200, 2200]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--libro", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--skip", action="append", default=[], help="regex adicional (sobre el título) para excluir")
    ap.add_argument("--expand", help="regex: entradas de primer nivel que se sustituyen por sus hijos")
    ap.add_argument("--toc-pages", help="A-B: páginas PDF con la tabla de contenido en texto")
    ap.add_argument("--offset", default="auto", help="auto|K: página PDF - folio (con --toc-pages)")
    ap.add_argument("--merge", action="append", default=[], help="regex: entradas que se funden con la anterior (su texto pasa a ella)")
    ap.add_argument("--chapters-file")
    ap.add_argument("--single", help="trata todo el PDF como un capítulo con este título")
    ap.add_argument("--dry-run", action="store_true", help="solo imprime la tabla, no escribe archivos")
    a = ap.parse_args()

    if not os.path.isfile(a.pdf):
        print(f"ERROR: no existe {a.pdf}", file=sys.stderr)
        return 2
    reader = pypdf.PdfReader(a.pdf)
    n = len(reader.pages)

    step = max(1, n // 20)
    sample = [len(page_text(reader, i + 1).split()) for i in range(0, n, step)]
    if sum(sample) < 30 * len(sample):
        print("ERROR: el PDF parece no tener capa de texto (escaneado). Se necesita OCR.", file=sys.stderr)
        return 4

    skip = [re.compile(p, re.I) for p in DEFAULT_SKIP + a.skip]
    items = None
    ends = {}
    if a.single:
        items = [(a.single, 1)]
    elif a.chapters_file:
        manual = json.load(open(a.chapters_file, encoding="utf-8"))
        items = [(c["titulo"], c["inicio"]) for c in manual]
        ends = {c["titulo"]: c.get("fin") for c in manual}
    elif a.toc_pages:
        x, y = a.toc_pages.split("-")
        items = toc_items(reader, int(x), int(y), a.offset)
        if not items:
            print("ERROR: no pude interpretar la tabla de contenido en texto.", file=sys.stderr)
            return 3
    else:
        items = outline_items(reader, re.compile(a.expand, re.I) if a.expand else None)
        if len(items) < 3:
            print("ERROR: el PDF no tiene outline útil; usar --toc-pages, --chapters-file o --single.", file=sys.stderr)
            return 3

    if a.merge:
        mre = [re.compile(p, re.I) for p in a.merge]
        items = [it for k, it in enumerate(items) if k == 0 or not any(r.search(it[0]) for r in mre)]

    chapters, last_num = [], -1
    for k, (title, start) in enumerate(items):
        if any(r.search(title) for r in skip):
            continue
        end = ends.get(title) or ((items[k + 1][1] - 1) if k + 1 < len(items) else n)
        end = max(min(end, n), start)
        m = re.match(r"^(?:chapter\s+)?(\d+)(?:[:.]|\s+(?=[A-Z]))", title, re.I)
        if m:
            num = int(m.group(1))
        elif PREFACE_RE.match(title) and last_num < 0:
            num = 0
        else:
            num = max(last_num + 1, 1)
        last_num = max(last_num, num)
        chapters.append(dict(num=num, titulo=title, name=f"cap{num:02d}-{slugify(title)}", inicio=start, fin=end))

    libdir = os.path.join(a.out, a.libro)
    if not a.dry_run:
        os.makedirs(libdir, exist_ok=True)
    offsets = collections.Counter()
    for c in chapters:
        txt = "".join(f"\n[[PDF p.{i}]]\n" + page_text(reader, i) for i in range(c["inicio"], c["fin"] + 1))
        c["palabras"] = len(txt.split())
        c["rango_palabras"] = rango_palabras(c["fin"] - c["inicio"] + 1)
        off = detect_offset(reader, c["inicio"], c["fin"])
        if off is not None:
            offsets[off] += 1
        if not a.dry_run:
            with open(os.path.join(libdir, c["name"] + ".txt"), "w", encoding="utf-8") as f:
                f.write(txt)
    desfase = offsets.most_common(1)[0][0] if offsets else None
    manifest = dict(libro=a.libro, pdf=os.path.abspath(a.pdf), paginas_pdf=n, desfase_folio=desfase, capitulos=chapters)
    if not a.dry_run:
        with open(os.path.join(libdir, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"{a.libro}: {len(chapters)} capítulos, {n} páginas PDF, desfase_folio={desfase}")
    for c in chapters:
        print(f"{c['name']}\t{c['inicio']}-{c['fin']}\t{c['palabras']}\t{c['rango_palabras']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
