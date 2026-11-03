#!/usr/bin/env python3
"""Genera el .jsonl de tareas para scripts/run_agent.py a partir del manifest.json de pdf-splitter.

Uso:
  make_tasks.py <agente> --manifest <trabajo>/<libro>/manifest.json --apuntes <dir apuntes> \
      --meta "Título|Autores|Editorial, año" [--nota "texto"] [--only REGEX] [--skip-existing]

Agentes soportados: note-writer, notes-formatter, notes-verifier, study-aid-generator.
La carpeta del libro es <apuntes>/<libro>; los .txt fuente están junto al manifest.json.
Escribe el .jsonl por stdout.
"""
import argparse
import json
import os
import re
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("agente")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--apuntes", required=True)
    ap.add_argument("--meta", help="'Título|Autores|Editorial, año' (solo note-writer)")
    ap.add_argument("--nota", default="", help="'Nota sobre el texto' para note-writer")
    ap.add_argument("--only", help="regex sobre el nombre capNN-… para filtrar")
    ap.add_argument("--skip-existing", action="store_true", help="omite capítulos cuyo archivo de salida ya existe")
    a = ap.parse_args()

    m = json.load(open(a.manifest, encoding="utf-8"))
    libro = m["libro"]
    src = os.path.dirname(os.path.abspath(a.manifest))
    apuntes = os.path.abspath(a.apuntes)
    book_dir = f"{apuntes}/{libro}"
    if a.agente == "note-writer" and not a.meta:
        sys.exit("ERROR: --meta es obligatorio para note-writer")
    title, authors, pub = (a.meta.split("|") + ["", "", ""])[:3] if a.meta else ("", "", "")

    for c in m["capitulos"]:
        n = c["name"]
        if a.only and not re.search(a.only, n):
            continue
        txt = f"{src}/{n}.txt"
        note = f"{book_dir}/{n}.md"
        label = n[:5]
        orig = re.sub(r"^(chapter\s+)?\d+[:.]?\s*", "", c["titulo"], flags=re.I)
        if a.agente == "note-writer":
            out = note
            if a.skip_existing and os.path.exists(out):
                continue
            lo, hi = c.get("rango_palabras", [600, 1400])
            pro = " (es el PRÓLOGO/introducción inicial: usa el formato de prólogo)" if c["num"] == 0 else ""
            prompt = (
                f"Escribe el apunte del capítulo. Libro: {title}. Autor(es): {authors}. Editorial/año: {pub}. "
                f"Capítulo: número {c['num']}, título original '{orig}'{pro}. "
                f"Rango de palabras: {lo} a {hi}. "
                f"Entrada: {txt} (páginas PDF {c['inicio']}-{c['fin']}). Salida: {out}."
            )
            if a.nota:
                prompt += f" Nota sobre el texto: {a.nota}"
            req = [txt]
        elif a.agente == "notes-formatter":
            prompt, req = f"Revisa el apunte {note}", [note]
        elif a.agente == "notes-verifier":
            frag = f"{book_dir}/_verificacion.d/{label}.md"
            if a.skip_existing and os.path.exists(frag):
                continue
            prompt = f"Verifica el apunte {note} contra el texto fuente {txt}. Escribe el fragmento en {frag}"
            req = [note, txt]
        elif a.agente == "study-aid-generator":
            out = f"{apuntes}/_estudio/{libro}/{label}-estudio.md"
            if a.skip_existing and os.path.exists(out):
                continue
            prompt = f"Genera el material de estudio del apunte {note}. Salida: {out}"
            req = [note]
        else:
            sys.exit(f"ERROR: agente no soportado: {a.agente}")
        print(json.dumps(dict(label=f"{libro[:12]}:{label}", prompt=prompt, require=req), ensure_ascii=False))


if __name__ == "__main__":
    main()
