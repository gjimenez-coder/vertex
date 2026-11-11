#!/usr/bin/env python3
"""Divide 'Claude Certification Exam.md' en bloques por tarea.

Uso: split_exam_bank.py <banco.md> --out /tmp/trabajo-cca/bank
Salida: <out>/N.M.txt (cada pregunta precedida por el marcador [[Q13]]), <out>/_escenarios.txt,
        <out>/_formato.txt (formato, dominios y pesos) y <out>/mapa.json.
La ubicación física en el banco manda sobre la tabla 'Domain-Task Index'; las diferencias se reportan.
"""
import argparse
import json
import os
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bank")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    text = open(a.bank, encoding="utf-8").read()
    os.makedirs(a.out, exist_ok=True)

    # Índice dominio-tarea declarado por el banco
    index = {}
    idx_part = text.split("## Domain-Task Index")[1].split("## Exam Scenarios")[0]
    for m in re.finditer(r"^\| (\d\.\d) \|[^|]*\|\s*([^|]+?)\s*\|\s*$", idx_part, re.M):
        for q in re.findall(r"Q(\d+)", m.group(2)):
            index[int(q)] = m.group(1)

    body = text.split("## Domain 1:", 1)[1]
    body = "## Domain 1:" + body
    body = body.split("## Answer Key")[0]
    parts = re.split(r"^### Task (\d\.\d):[^\n]*\n", body, flags=re.M)
    # parts = [pre, 'N.M', contenido, 'N.M', contenido, ...]
    physical = {}
    for i in range(1, len(parts), 2):
        task, content = parts[i], parts[i + 1]
        content = re.split(r"^## Domain \d:", content, flags=re.M)[0]
        blocks = re.split(r"(?m)^\*\*Q(\d+)\.\*\*", content)
        qs = []
        for j in range(1, len(blocks), 2):
            n = int(blocks[j])
            block = blocks[j + 1].rstrip().rstrip("-").rstrip()
            qs.append((n, f"[[Q{n}]]\n**Q{n}.**{block}\n"))
            physical[n] = task
        title = re.search(rf"^### Task {re.escape(task)}:[^\n]*", body, re.M).group(0)[4:]
        with open(os.path.join(a.out, f"{task}.txt"), "w", encoding="utf-8") as f:
            f.write(f"{title}\n\n" + "\n---\n\n".join(b for _, b in qs))
    # Escenarios y formato
    sc = text.split("## Exam Scenarios")[1].split("## Domain 1:")[0]
    open(os.path.join(a.out, "_escenarios.txt"), "w", encoding="utf-8").write(sc.strip() + "\n")
    fm = text.split("## Domain-Task Index")[0]
    open(os.path.join(a.out, "_formato.txt"), "w", encoding="utf-8").write(fm.strip() + "\n")

    # Si el índice y la ubicación física difieren, la pregunta se añade también a la tarea del índice
    for q, t_idx in sorted(index.items()):
        t_phys = physical.get(q)
        if t_phys and t_phys != t_idx:
            src = open(os.path.join(a.out, f"{t_phys}.txt"), encoding="utf-8").read()
            blk = re.search(rf"\[\[Q{q}\]\].*?(?=\n---\n|\Z)", src, re.S).group(0)
            with open(os.path.join(a.out, f"{t_idx}.txt"), "a", encoding="utf-8") as f:
                f.write(f"\n---\n\n[NOTA: el índice del banco asigna esta pregunta a la tarea {t_idx}, pero aparece físicamente en la {t_phys}]\n{blk}\n")

    counts = {}
    for q, t in physical.items():
        counts[t] = counts.get(t, 0) + 1
    diffs = {q: (index.get(q), t) for q, t in sorted(physical.items()) if index.get(q) != t}
    missing = [q for q in range(1, 78) if q not in physical]
    json.dump(dict(preguntas=len(physical), por_tarea=counts, diferencias_indice=diffs, faltantes=missing),
              open(os.path.join(a.out, "mapa.json"), "w"), indent=1)
    print("preguntas:", len(physical), "tareas:", len(counts), "faltantes:", missing)
    print("por tarea:", dict(sorted(counts.items())))
    print("diferencias con el índice (Q: índice->físico):", {q: f"{x}->{y}" for q, (x, y) in diffs.items()} or "ninguna")
    return 0


if __name__ == "__main__":
    sys.exit(main())
