#!/usr/bin/env python3
"""Lanza un agente de .kiro/agents con kiro-cli (headless) sobre una lista de tareas, en paralelo.

Uso:
  run_agent.py --agent note-writer --tasks tareas.jsonl [--workers 4] [--trust fs_read,fs_write]
  run_agent.py --agent notes-formatter --prompt "texto 1" --prompt "texto 2"

Formato de tareas.jsonl (una por línea):
  {"label": "cap01", "prompt": "…", "require": ["/ruta/que/debe/existir.txt"]}
  (label y require son opcionales; también se acepta una línea de texto plano como prompt)

Salida: una línea por tarea "label: rc=N resultado". Código de salida != 0 si alguna tarea falla
o su resultado contiene "ERROR". Las rutas de "require" se validan ANTES de lanzar nada.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def load_tasks(a):
    tasks = []
    for i, p in enumerate(a.prompt or [], 1):
        tasks.append(dict(label=f"tarea{i}", prompt=p, require=[]))
    if a.tasks:
        with open(a.tasks, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("{"):
                    t = json.loads(line)
                    tasks.append(dict(label=t.get("label", f"tarea{i}"), prompt=t["prompt"], require=t.get("require", [])))
                else:
                    tasks.append(dict(label=f"tarea{i}", prompt=line, require=[]))
    return tasks


def run_one(a, t):
    cmd = ["kiro-cli", "chat", "--no-interactive", "--agent", a.agent, f"--trust-tools={a.trust}", t["prompt"]]
    try:
        r = subprocess.run(cmd, cwd=a.cwd, capture_output=True, text=True, timeout=a.timeout)
    except subprocess.TimeoutExpired:
        return t["label"], 124, "ERROR: timeout"
    out = ANSI.sub("", r.stdout).strip()
    last = (out.splitlines() or [""])[-1]
    # el agente responde con una frase final; si la línea es larga, quedarse con la cola
    return t["label"], r.returncode, last[-200:]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agent", required=True)
    ap.add_argument("--tasks", help="archivo .jsonl con tareas")
    ap.add_argument("--prompt", action="append", help="prompt de una tarea (repetible)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--trust", default="fs_read,fs_write", help="herramientas confiables (coma). Ej: fs_read,fs_write,execute_bash")
    ap.add_argument("--cwd", default=ROOT)
    ap.add_argument("--timeout", type=int, default=1500, help="segundos por tarea")
    a = ap.parse_args()

    if shutil.which("kiro-cli") is None:
        print("ERROR: kiro-cli no está en el PATH", file=sys.stderr)
        return 2
    if not os.path.isfile(os.path.join(ROOT, ".kiro", "agents", f"{a.agent}.json")):
        print(f"ERROR: no existe .kiro/agents/{a.agent}.json", file=sys.stderr)
        return 2
    tasks = load_tasks(a)
    if not tasks:
        print("ERROR: no hay tareas (usa --prompt o --tasks)", file=sys.stderr)
        return 2
    missing = [(t["label"], p) for t in tasks for p in t["require"] if not os.path.exists(p)]
    if missing:
        for label, p in missing:
            print(f"ERROR: {label}: no existe {p}", file=sys.stderr)
        return 2

    failed = 0
    with cf.ThreadPoolExecutor(max_workers=max(1, a.workers)) as ex:
        for label, rc, res in ex.map(lambda t: run_one(a, t), tasks):
            print(f"{label}: rc={rc} {res}", flush=True)
            if rc != 0 or "ERROR" in res:
                failed += 1
    if failed:
        print(f"{failed} de {len(tasks)} tareas con problemas", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
