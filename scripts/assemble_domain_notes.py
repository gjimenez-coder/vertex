#!/usr/bin/env python3
"""Ensambla los apuntes finales por dominio (CCA-F) desde _partes/ y valida su estructura.

Uso: assemble_domain_notes.py --root /ruta/claude/apuntes/ClaudeCert [--check-only]
Cada apunte = H1 + H2 'Dominio N' + nota de extracción + _intro + fragmentos N.M + _ideas.
"""
import argparse
import os
import re
import sys

DOMAINS = {
    1: ("dominio1-agentic-architecture-orchestration", "Agentic Architecture & Orchestration",
        "Arquitectura agéntica y orquestación", 7),
    2: ("dominio2-tool-design-mcp-integration", "Tool Design & MCP Integration",
        "Diseño de herramientas e integración MCP", 5),
    3: ("dominio3-claude-code-configuration-workflows", "Claude Code Configuration & Workflows",
        "Configuración y flujos de trabajo de Claude Code", 6),
    4: ("dominio4-prompt-engineering-structured-output", "Prompt Engineering & Structured Output",
        "Ingeniería de prompts y salida estructurada", 6),
    5: ("dominio5-context-management-reliability", "Context Management & Reliability",
        "Gestión de contexto y fiabilidad", 6),
}
H1 = "# Claude Certified Architect – Foundations (CCA-F) — Anthropic (guía de examen, 2026)"
NOTA = (
    "> Nota de extracción: este apunte combina cinco fuentes: la guía en PDF «Tutorials Dojo Study Guide and Cheat Sheets – "
    "Claude Certified Architect Foundations (CCA-F)», las slides en PDF del curso en video (Tutorials Dojo, junio 2026), el banco "
    "de 77 preguntas de práctica «Claude Certified Architect. Foundations: Practice Exam» y las lecciones web de "
    "claudecertificationguide.com (sitio independiente de terceros, no afiliado a Anthropic). Citas: `(Guía PDF p. N)` y "
    "`(Slides PDF p. N)` usan la página del PDF; `(web N.M)` remite a la lección N.M de la web; `(QN)` remite a la pregunta N del banco. "
    "Si las fuentes se contradicen, prevalecen la guía y el banco sobre la web. Las slides tienen muchas páginas que son solo imagen "
    "y no se pudieron leer, por lo que su cobertura es parcial. Discrepancia entre fuentes sin resolver: el banco y la guía llaman al examen "
    "«CCA-F» y el banco indica 77 preguntas de práctica y una nota mínima de 720 (escala 100-1.000); la web lo llama «CCAR-F» e indica "
    "60 preguntas en 120 minutos, aprobado con 720/1.000 y credencial válida 12 meses. No se decide cuál es la correcta."
)


def read(p):
    return open(p, encoding="utf-8").read().strip()


def assemble(root):
    for dn, (slug, en, es, ntasks) in DOMAINS.items():
        d = os.path.join(root, "_partes", f"d{dn}")
        tasks = [f"{dn}.{k}" for k in range(1, ntasks + 1)]
        parts = [H1, f"## Dominio {dn} — {en} ({es})", NOTA, read(os.path.join(d, "_intro.md"))]
        parts += [read(os.path.join(d, f"{t}.md")) for t in tasks]
        parts.append(read(os.path.join(d, "_ideas.md")))
        out = os.path.join(root, f"{slug}.md")
        open(out, "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
        print("escrito", os.path.basename(out))


def validate(root):
    ok = True
    for dn, (slug, en, es, ntasks) in DOMAINS.items():
        t = open(os.path.join(root, f"{slug}.md"), encoding="utf-8").read()
        L = t.split("\n")
        h2 = [l for l in L if l.startswith("## ")]
        p = []
        if not re.match(r"^# .+ — .+ \(.+\)\s*$", L[0]):
            p.append("h1")
        if not h2[0].startswith(f"## Dominio {dn} — "):
            p.append("h2-dominio")
        if not re.search(r"^> Nota de extracción:", t, re.M):
            p.append("nota")
        if "## Lo que necesitas saber" not in t:
            p.append("intro")
        for k in range(1, ntasks + 1):
            if not re.search(rf"^## Tarea {dn}\.{k} — ", t, re.M):
                p.append(f"falta-tarea-{dn}.{k}")
        if h2[-1].strip() != "## Ideas clave":
            p.append("ideas-clave-no-final")
        if t.count("```") % 2:
            p.append("codigo-sin-cerrar")
        if re.search(r"\[\[|\[NOTA", t):
            p.append("marcadores-sueltos")
        if re.search(r"\((?:p\. ?\d|pág)", t):
            p.append("cita-formato-antiguo")
        if len(re.findall(r"(?m)^### Trampas del examen", t)) != ntasks:
            p.append("trampas-por-tarea")
        order = [m.group(1) for m in re.finditer(r"(?m)^## (Tarea \d\.\d|Lo que necesitas saber|Ideas clave)", t)]
        if order[0] != "Lo que necesitas saber":
            p.append("orden-intro")
        print(f"dominio {dn}: {len(t.split())} palabras,", "OK" if not p else p)
        ok &= not p
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    if not a.check_only:
        assemble(a.root)
    return 0 if validate(a.root) else 1


if __name__ == "__main__":
    sys.exit(main())
