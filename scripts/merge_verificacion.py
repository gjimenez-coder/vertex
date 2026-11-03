#!/usr/bin/env python3
"""Une los fragmentos de apuntes/<libro>/_verificacion.d/capNN.md en apuntes/<libro>/_verificacion.md.

Uso: merge_verificacion.py <carpeta apuntes/<libro>> [--keep]
Los fragmentos los escribe el agente notes-verifier (uno por capítulo, para evitar escrituras concurrentes).
Por defecto borra _verificacion.d/ tras unir.
"""
import os
import re
import shutil
import sys


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keep = "--keep" in sys.argv
    if len(args) != 1:
        print(__doc__)
        return 2
    book = args[0].rstrip("/")
    frag = os.path.join(book, "_verificacion.d")
    if not os.path.isdir(frag):
        print(f"ERROR: no existe {frag}", file=sys.stderr)
        return 2
    files = sorted(f for f in os.listdir(frag) if f.endswith(".md"))
    rows, body, tot = [], [], dict(alta=0, media=0, baja=0)
    for f in files:
        txt = open(os.path.join(frag, f), encoding="utf-8").read().strip()
        m = re.search(r"Hallazgos:\s*(\d+)\s*\(alta\s*(\d+),\s*media\s*(\d+),\s*baja\s*(\d+)\)", txt)
        if not m:
            rows.append((f[:-3], "?", "?", "?", "?"))
            body.append(txt + "\n\n_(formato de fragmento no reconocido)_")
            continue
        n, a, me, b = map(int, m.groups())
        tot["alta"] += a
        tot["media"] += me
        tot["baja"] += b
        rows.append((f[:-3], n, a, me, b))
        body.append(txt)
    name = os.path.basename(book)
    out = [f"# Verificación de fidelidad — {name}", "",
           "Reporte generado por el agente `notes-verifier`: contrasta cada apunte con el texto fuente del capítulo.", "",
           "| Capítulo | Hallazgos | Alta | Media | Baja |", "|---|---|---|---|---|"]
    out += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
    total = sum(tot.values())
    out += ["", f"**Total:** {total} hallazgos (alta {tot['alta']}, media {tot['media']}, baja {tot['baja']}) en {len(rows)} capítulos.", "",
            "## Detalle", ""]
    out += [b + "\n" for b in body]
    with open(os.path.join(book, "_verificacion.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    if not keep:
        shutil.rmtree(frag)
    print(f"{name}: {total} hallazgos (alta {tot['alta']}, media {tot['media']}, baja {tot['baja']}) en {len(rows)} capítulos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
