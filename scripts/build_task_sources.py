#!/usr/bin/env python3
"""Ensambla el texto fuente de cada una de las 30 tareas del examen CCA-F.

Une, con marcadores de fuente:
  [[FUENTE: web N.M]]            lección de claudecertificationguide.com
  [[FUENTE: guia PDF]]           secciones de la guía (con [[PDF p.N]])
  [[FUENTE: slides PDF]]         páginas de slides relevantes (con [[PDF p.N]])
  [[FUENTE: banco]]              preguntas del banco (con [[QN]])
  [[FUENTE: refuerzo usuario]]   secciones de tus guías de refuerzo (solo para priorizar)

Entradas (ya generadas): <work>/web, <work>/pdf/{guide,slides}, <work>/bank
Salida: <work>/dN/N.M.txt, <work>/dN/manifest.json y <work>/general.txt
Uso: build_task_sources.py --work /tmp/trabajo-cca --claudecert /ruta/claude/ClaudeCert
"""
import argparse
import json
import os
import re
import sys

TASKS = {
    1: ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"],
    2: ["2.1", "2.2", "2.3", "2.4", "2.5"],
    3: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"],
    4: ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6"],
    5: ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6"],
}
WEIGHT = {1: 27, 2: 18, 3: 20, 4: 20, 5: 15}

# Temas débiles del usuario (etiqueta, % reportado) -> tareas
WEAK = {
    "1.4": [("Salvaguardas de la capa de orquestación (resolución o escalación)", "0% en los intentos 1 y 2")],
    "5.2": [("Salvaguardas de orquestación: cierre en resolución o escalación", "0% en los intentos 1 y 2")],
    "3.1": [("Settings/hooks vs CLAUDE.md", "0% en los intentos 1 y 2"),
            ("@ references vs CLAUDE.md vs inline", "0% en los intentos 1 y 2")],
    "4.5": [("Messages API vs Message Batches API", "0% en los intentos 1 y 2")],
    "2.1": [("Descripciones de herramientas", "0% en los intentos 1 y 2")],
    "2.4": [("Scope de servidores MCP", "regresión: 100% -> 0%"), ("Integración MCP (env vars)", "débil: 25%")],
    "4.3": [("Método de salida estructurada", "regresión: 100% -> 0%")],
    "2.3": [("tool_use + tool_choice", "regresión: 100% -> 0%")],
    "4.1": [("Patrones de precisión en extracción", "regresión: 75% -> 50%")],
    "2.5": [("Exploración con Grep/Glob/Read", "débil: 50%")],
    "3.5": [("Refinamiento iterativo", "débil: 25% -> 50%")],
    "4.4": [("Feedback loops con metadata de errores", "0% en el mapa de refuerzo")],
    "2.2": [("Errores MCP estructurados", "50% en el mapa de refuerzo")],
    "1.6": [("Decomposición dinámica de tareas", "50% en el mapa de refuerzo")],
    "5.5": [("Routing a revisión humana por confianza", "67% en el mapa de refuerzo")],
}
# Secciones de guia_estudio_intento3.md (número) -> tareas
GUIA_SECTIONS = {1: ["1.4", "5.2"], 2: ["3.1"], 3: ["3.1"], 4: ["4.5"], 5: ["2.1"], 6: ["2.4"], 7: ["4.3", "2.3"],
                 8: ["4.1"], 9: ["2.4", "2.2"], 10: ["2.5", "5.4"], 11: ["3.5"]}
# Viñetas "7-13. Débiles" del cheat sheet de examen-refuerzo.md -> tareas
BULLET_TASKS = {"Refinamiento iterativo": ["3.5"], "MCP": ["2.4"], "Errores MCP": ["2.2"], "Decomposición": ["1.6"],
                "Exploración": ["2.5", "5.4"], "Routing humano": ["5.5"], "Extracción": ["4.1", "4.3"]}
# Secciones "## N." del cheat sheet de examen-refuerzo.md -> tareas
EXAMEN_SECTIONS = {1: ["1.4", "5.2"], 2: ["3.1"], 3: ["3.1"], 4: ["4.5"], 5: ["4.4"], 6: ["2.1"]}


def read(path):
    return open(path, encoding="utf-8", errors="replace").read() if os.path.exists(path) else ""


def split_h2(text):
    """[(titulo, cuerpo)] por encabezados '## '."""
    parts = re.split(r"(?m)^## ", text)
    return [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1].strip() if "\n" in p else "") for p in parts[1:]]


def refuerzo_for(claudecert):
    out = {t: [] for d in TASKS.values() for t in d}
    g = read(os.path.join(claudecert, "guia_estudio_intento3.md"))
    for title, body in split_h2(g):
        m = re.match(r"(\d+)\.", title)
        if m and int(m.group(1)) in GUIA_SECTIONS:
            for t in GUIA_SECTIONS[int(m.group(1))]:
                out[t].append((f"guia_estudio_intento3.md, sección «{title}»", body.rstrip("-").strip()))
    c = read(os.path.join(claudecert, "cheatsheet-refuerzo.md"))
    for title, body in split_h2(c):
        m = re.match(r"Objetivo (\d+)", title)
        if m and int(m.group(1)) in EXAMEN_SECTIONS:
            for t in EXAMEN_SECTIONS[int(m.group(1))]:
                out[t].append((f"cheatsheet-refuerzo.md, «{title}»", body.rstrip("-").strip()))
    e = read(os.path.join(claudecert, "examen-refuerzo.md"))
    tail = e.split("# Cheat Sheet — Objetivos a reforzar", 1)[-1]
    for title, body in split_h2(tail):
        m = re.match(r"(\d+)\.", title)
        if m and int(m.group(1)) in EXAMEN_SECTIONS:
            for t in EXAMEN_SECTIONS[int(m.group(1))]:
                out[t].append((f"examen-refuerzo.md (cheat sheet), «{title}»", body.strip()))
        elif title.startswith("7-13"):
            for line in body.splitlines():
                mm = re.match(r"- \*\*([^*:]+?):?\*\*", line)
                if mm:
                    for key, tasks in BULLET_TASKS.items():
                        if mm.group(1).strip().startswith(key):
                            for t in tasks:
                                out[t].append((f"examen-refuerzo.md (cheat sheet), «{title}»", line.strip()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--claudecert", required=True)
    a = ap.parse_args()
    refuerzo = refuerzo_for(a.claudecert)
    problems = []
    for dn, tasks in TASKS.items():
        os.makedirs(os.path.join(a.work, f"d{dn}"), exist_ok=True)
        manifest = dict(dominio=dn, peso=WEIGHT[dn], tareas=[])
        for t in tasks:
            web = read(os.path.join(a.work, "web", f"{t}.txt"))
            guia = read(os.path.join(a.work, "pdf", "guide", f"{t}.txt")).strip()
            slides = read(os.path.join(a.work, "pdf", "slides", f"{t}.txt")).strip()
            bank = read(os.path.join(a.work, "bank", f"{t}.txt")).strip()
            title_bank = bank.splitlines()[0] if bank else f"Task {t}"
            web_url = re.search(r"^URL: (.+)$", web, re.M)
            web_title = re.search(r"^TITULO: (.+)$", web, re.M)
            parts = [f"# TAREA {t} — {title_bank.split(':', 1)[-1].strip()}",
                     f"Dominio {dn} (peso {WEIGHT[dn]}%). Título web: {web_title.group(1) if web_title else '?'}."]
            weak = WEAK.get(t, [])
            if weak:
                parts.append("[[PRIORIDAD DE ESTUDIO]] Temas débiles de tus intentos: " +
                             "; ".join(f"{n} ({p})" for n, p in weak))
            counts = {}
            if web:
                body = web.split("\n\n", 1)[1] if "\n\n" in web else web
                parts.append(f"\n[[FUENTE: web {t}]] ({web_url.group(1) if web_url else ''})\n{body.strip()}")
                counts["web"] = len(body.split())
            if guia:
                parts.append("\n[[FUENTE: guia PDF]]\n" + guia)
                counts["guia"] = len(guia.split())
            if slides:
                parts.append("\n[[FUENTE: slides PDF]]\n" + slides)
                counts["slides"] = len(slides.split())
            if bank:
                body = bank.split("\n", 1)[1].strip() if "\n" in bank else bank
                parts.append("\n[[FUENTE: banco]]\n" + body)
                counts["banco"] = len(body.split())
                counts["preguntas"] = len(re.findall(r"^\[\[Q\d+\]\]", body, re.M))
            if refuerzo[t]:
                txt = "\n\n".join(f"[[REFUERZO: {src}]]\n{b}" for src, b in refuerzo[t])
                parts.append("\n[[FUENTE: refuerzo usuario]] (solo para marcar prioridad; no añade contenido)\n" + txt)
                counts["refuerzo"] = len(txt.split())
            with open(os.path.join(a.work, f"d{dn}", f"{t}.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(parts).strip() + "\n")
            missing = [k for k in ("web", "guia", "slides", "banco") if k not in counts]
            manifest["tareas"].append(dict(tarea=t, titulo=title_bank.split(":", 1)[-1].strip(), palabras=counts,
                                           tema_debil=[n for n, _ in weak], fuentes_faltantes=missing))
            if "web" in missing or "guia" in missing or "banco" in missing:
                problems.append((t, missing))
        json.dump(manifest, open(os.path.join(a.work, f"d{dn}", "manifest.json"), "w"), indent=1, ensure_ascii=False)
    # Contexto general del examen (formato, dominios, escenarios, resumen de la guía)
    gen = "\n\n".join([
        "[[FUENTE: banco — formato y dominios]]\n" + read(os.path.join(a.work, "bank", "_formato.txt")),
        "[[FUENTE: banco — escenarios]]\n" + read(os.path.join(a.work, "bank", "_escenarios.txt")),
        "[[FUENTE: guia PDF — introducción y panorama del examen]]\n" + read(os.path.join(a.work, "pdf", "guide", "_general.txt")),
    ])
    open(os.path.join(a.work, "general.txt"), "w", encoding="utf-8").write(gen)
    print("tarea\tweb\tguía\tslides\tbanco\tpreg\trefuerzo\tdébil")
    for dn in TASKS:
        for it in json.load(open(os.path.join(a.work, f"d{dn}", "manifest.json")))["tareas"]:
            c = it["palabras"]
            print(f"{it['tarea']}\t{c.get('web',0)}\t{c.get('guia',0)}\t{c.get('slides',0)}\t{c.get('banco',0)}\t"
                  f"{c.get('preguntas',0)}\t{c.get('refuerzo',0)}\t{'sí' if it['tema_debil'] else ''}")
    print("sin web/guía/banco:", problems or "ninguna")
    return 0


if __name__ == "__main__":
    sys.exit(main())
