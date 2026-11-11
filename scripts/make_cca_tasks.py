#!/usr/bin/env python3
"""Genera el .jsonl de tareas para scripts/run_agent.py (apuntes CCA-F por dominio).

Uso:
  make_cca_tasks.py exam-note-writer --modo tarea   [--only REGEX] [--skip-existing]
  make_cca_tasks.py exam-note-writer --modo dominio [--only REGEX]
  make_cca_tasks.py notes-verifier   [--only REGEX]
  make_cca_tasks.py study-aid-generator [--only REGEX]
Escribe el .jsonl por stdout. REGEX se aplica a la tarea 'N.M' (o 'dN' en modo dominio/estudio).
"""
import argparse
import json
import os
import re
import sys

WORK = "/tmp/trabajo-cca"
OUT = "/Users/gjimenez/Documents/vertex/claude/apuntes/ClaudeCert"
WEIGHT = {1: 27, 2: 18, 3: 20, 4: 20, 5: 15}
SLUG = {
    1: "dominio1-agentic-architecture-orchestration",
    2: "dominio2-tool-design-mcp-integration",
    3: "dominio3-claude-code-configuration-workflows",
    4: "dominio4-prompt-engineering-structured-output",
    5: "dominio5-context-management-reliability",
}


def tasks():
    for dn in range(1, 6):
        m = json.load(open(f"{WORK}/d{dn}/manifest.json"))
        for t in m["tareas"]:
            yield dn, t["tarea"], t["titulo"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("agente")
    ap.add_argument("--modo", choices=["tarea", "dominio"], default="tarea")
    ap.add_argument("--only")
    ap.add_argument("--skip-existing", action="store_true")
    a = ap.parse_args()
    rx = re.compile(a.only) if a.only else None
    out = []
    if a.agente == "exam-note-writer" and a.modo == "tarea":
        for dn, t, title in tasks():
            if rx and not rx.search(t):
                continue
            dest = f"{OUT}/_partes/d{dn}/{t}.md"
            if a.skip_existing and os.path.exists(dest):
                continue
            src = f"{WORK}/d{dn}/{t}.txt"
            out.append(dict(label=f"tarea {t}", require=[src],
                            prompt=f"Modo: tarea. Tarea {t} ({title}), dominio {dn}. Texto fuente: {src}. Salida: {dest}."))
    elif a.agente == "exam-note-writer":
        for dn in range(1, 6):
            if rx and not rx.search(f"d{dn}"):
                continue
            d = f"{OUT}/_partes/d{dn}"
            out.append(dict(label=f"dominio {dn}", require=[d],
                            prompt=(f"Modo: dominio. Dominio {dn}, peso en el examen {WEIGHT[dn]}%. Carpeta de fragmentos: {d}/. "
                                    f"Salidas: {d}/_intro.md y {d}/_ideas.md.")))
    elif a.agente == "notes-verifier":
        for dn, t, title in tasks():
            if rx and not rx.search(t):
                continue
            part = f"{OUT}/_partes/d{dn}/{t}.md"
            out.append(dict(label=f"verifica {t}", require=[part, f"{WORK}/d{dn}/{t}.txt"],
                            prompt=(f"Verifica el apunte {part} contra el texto fuente {WORK}/d{dn}/{t}.txt. "
                                    f"Escribe el fragmento en {OUT}/_verificacion.d/{t}.md")))
    elif a.agente == "study-aid-generator":
        for dn in range(1, 6):
            if rx and not rx.search(f"d{dn}"):
                continue
            note = f"{OUT}/{SLUG[dn]}.md"
            out.append(dict(label=f"estudio {dn}", require=[note],
                            prompt=(f"Genera el material de estudio del apunte {note} (apunte de examen por dominio; "
                                    f"genera 15 a 25 tarjetas, 10 a 15 preguntas de autoevaluación con su respuesta y una checklist "
                                    f"por tarea). Salida: {OUT}/_estudio/dominio{dn}-estudio.md")))
    else:
        print("agente no soportado", file=sys.stderr)
        return 2
    for o in out:
        print(json.dumps(o, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
