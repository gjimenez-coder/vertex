#!/usr/bin/env python3
"""Asigna páginas de la guía y de las slides CCA-F a las 30 tareas del examen.

Guía (Tutorials Dojo): secciones A-O del outline -> tareas (tabla SECTION_TASKS).
Las secciones de nivel dominio (preguntas de muestra, ejemplos, apéndice, guía extra,
referencias) y las slides se asignan por palabras clave (TASK_KEYWORDS) y, en las slides,
por la etiqueta explícita 'Task Statement N.M' cuando existe.

Uso: map_pdf_tasks.py --guide G.pdf --slides S.pdf --out /tmp/trabajo-cca/pdf
Salida:
  <out>/guide/N.M.txt   <out>/slides/N.M.txt   (texto con marcadores [[PDF p.N]])
  <out>/guide/_general.txt, <out>/slides/_sin_asignar.txt
  <out>/mapa.json       rangos por tarea y páginas sin texto
"""
import argparse
import collections
import json
import os
import re
import sys

from pypdf import PdfReader

TASKS = {
    1: ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"],
    2: ["2.1", "2.2", "2.3", "2.4", "2.5"],
    3: ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"],
    4: ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6"],
    5: ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6"],
}
ALL_TASKS = [t for d in TASKS.values() for t in d]

SECTION_TASKS = {
    1: dict(A=["1.1"], B=["1.1"], C=["1.2"], D=["1.3"], E=["1.4"], F=["1.5"], G=["1.6"], H=["1.7"]),
    2: dict(A=["2.1"], B=["2.1"], C=["2.2"], D=["2.3"], E=["2.3", "4.3"], F=["2.4"], G=["2.2"], H=["2.5"]),
    3: dict(A=["3.1"], B=["3.3"], C=["3.2"], D=["3.1"], E=["3.1"], F=["2.4"], G=["3.4"], H=["3.5"], I=["1.7"],
            J=["3.6"], K=["3.6", "4.1"], L=["4.5"], M=["2.5"], N=["5.4"], O=["4.6"]),
    4: dict(A=["4.1"], B=["4.1"], C=["4.2"], D=["4.3"], E=["4.3"], F=["4.4"], G=["4.5"], H=["4.6"]),
    5: dict(A=["5.1"], B=["5.1"], C=["5.2"], D=["5.3"], E=["5.4"], F=["5.5"], G=["5.6"]),
}

TASK_KEYWORDS = {
    "1.1": ["stop_reason", "end_turn", "agentic loop", "agent loop", "iteration cap", "max_tokens", "pause_turn", "tool_use"],
    "1.2": ["coordinator", "hub-and-spoke", "orchestrat", "synthesis", "coverage gap", "delegat", "subagents"],
    "1.3": ["agentdefinition", "allowedtools", "spawn", "context passing", "fork_session", "task tool", "parallel"],
    "1.4": ["prerequisite", "programmatic enforcement", "handoff", "deterministic compliance", "enforcement"],
    "1.5": ["pretooluse", "posttooluse", "hook", "normaliz", "matcher"],
    "1.6": ["decomposition", "decompose", "prompt chaining", "adaptive", "sequential", "parallelism"],
    "1.7": ["--resume", "resumption", "session", "fork", "scratchpad", "/clear"],
    "2.1": ["tool description", "tool name", "misrouting", "tool definition", "parameter description", "input schema", "overlapping"],
    "2.2": ["is_error", "structured error", "errorcategory", "isretryable", "access failure", "empty result", "error response"],
    "2.3": ["tool_choice", "allowedtools", "least privilege", "forced tool", "tool distribution", "role-bounded"],
    "2.4": [".mcp.json", "mcp server", "~/.claude.json", "mcp resource", "environment variable", "${"],
    "2.5": ["grep", "glob", "read tool", "edit tool", "write tool", "bash tool", "built-in tool"],
    "3.1": ["claude.md", "@import", "/memory", "hierarchy", "permissions.deny", "settings.json", "advisory"],
    "3.2": ["slash command", "skill.md", "skill", "context: fork", "allowed-tools", "argument-hint"],
    "3.3": [".claude/rules", "paths:", "glob pattern", "frontmatter", "path-scoped", "path-specific"],
    "3.4": ["plan mode", "direct execution", "multi-phase", "explore subagent"],
    "3.5": ["iterative", "test-driven", "interview", "tbd", "concrete test cases", "incremental"],
    "3.6": ["claude -p", "--output-format", "--json-schema", "ci/cd", "pipeline", "--max-turns", "pull request", "non-interactive"],
    "4.1": ["explicit criteria", "false positive", "be conservative", "severity", "detected_pattern", "precision"],
    "4.2": ["few-shot", "few shot", "ambiguous case", "consistency", "examples"],
    "4.3": ["json schema", "nullable", "enum", "structured output", "extraction", "tool_use", "required field"],
    "4.4": ["validation", "retry", "feedback", "pydantic", "resolvable", "semantic"],
    "4.5": ["message batches", "batch", "custom_id", "24 hours", "50%", "sla"],
    "4.6": ["self-review", "independent", "multi-pass", "per-file", "cross-file", "confidence routing"],
    "5.1": ["context window", "summariz", "lost in the middle", "case facts", "token budget", "compaction"],
    "5.2": ["escalat", "sentiment", "confidence", "ambiguity", "clarification"],
    "5.3": ["error propagation", "coverage gap", "partial", "cascading", "local recovery", "access failure"],
    "5.4": ["codebase exploration", "scratchpad", "subagent delegation", "context degradation", "exploration"],
    "5.5": ["human review", "confidence threshold", "stratified sampling", "calibration", "review queue"],
    "5.6": ["provenance", "claim-source", "source conflict", "attribution", "source authority", "citation"],
}
TASK_TAG = re.compile(r"task statement\s+([1-5]\.[1-7])", re.I)
DOMAIN_LEVEL = re.compile(r"sample questions|worked examples|services appendix|additional exam guidance|references for", re.I)


def clean(t):
    t = "\n".join(l for l in t.splitlines() if l.strip() != "Tutorials Dojo")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def page_texts(reader):
    return {i + 1: clean(reader.pages[i].extract_text() or "") for i in range(len(reader.pages))}


def best_task(text, candidates):
    low = text.lower()
    m = TASK_TAG.findall(text)
    if m:
        c = collections.Counter(x for x in m if x in candidates)
        if c:
            return c.most_common(1)[0][0]
    scores = {}
    for t in candidates:
        scores[t] = sum(min(low.count(k), 3) for k in TASK_KEYWORDS[t])
    t, s = max(scores.items(), key=lambda kv: kv[1])
    return t if s >= 1 else None


def walk(outline, reader, depth=0, out=None):
    for x in outline:
        if isinstance(x, list):
            walk(x, reader, depth + 1, out)
        else:
            try:
                out.append((depth, x.title, reader.get_destination_page_number(x) + 1))
            except Exception:  # noqa: BLE001
                pass
    return out


def write_group(folder, groups, texts):
    os.makedirs(folder, exist_ok=True)
    ranges = {}
    for t in ALL_TASKS:
        pages = sorted(set(groups.get(t, [])))
        ranges[t] = pages
        with open(os.path.join(folder, f"{t}.txt"), "w", encoding="utf-8", errors="replace") as f:
            for p in pages:
                f.write(f"\n[[PDF p.{p}]]\n{texts[p]}\n")
    return ranges


def map_guide(path, out):
    r = PdfReader(path)
    texts = page_texts(r)
    n = len(texts)
    o = walk(r.outline, r, 0, [])
    doms = [(int(m.group(1)), p) for d, t, p in o if d == 0 for m in [re.match(r"Domain (\d):", t)] if m]
    doms.sort(key=lambda x: x[1])
    final = [p for d, t, p in o if d == 0 and t.upper().startswith("FINAL REMARKS")]
    dom_end = {dn: (doms[i + 1][1] - 1 if i + 1 < len(doms) else (final[0] - 1 if final else n)) for i, (dn, _) in enumerate(doms)}
    general = [p for p in range(1, doms[0][1])]
    groups = collections.defaultdict(list)
    unassigned = []
    for dn, dstart in doms:
        secs = [(t, p) for d, t, p in o if d == 1 and dstart <= p <= dom_end[dn]]
        secs.sort(key=lambda x: x[1])
        for i, (title, start) in enumerate(secs):
            nxt = secs[i + 1][1] if i + 1 < len(secs) else dom_end[dn]
            end = max(start, min(nxt, dom_end[dn]))  # incluye la página de la sección siguiente (se comparte)
            m = re.match(r"^([A-O])\.\s", title)
            pages = range(start, end + 1)
            if m and m.group(1) in SECTION_TASKS[dn]:
                for t in SECTION_TASKS[dn][m.group(1)]:
                    groups[t].extend(pages)
            elif DOMAIN_LEVEL.search(title):
                for p in pages:
                    t = best_task(texts[p], TASKS[dn])
                    if t:
                        groups[t].append(p)
                    else:
                        unassigned.append(p)
    ranges = write_group(os.path.join(out, "guide"), groups, texts)
    with open(os.path.join(out, "guide", "_general.txt"), "w", encoding="utf-8", errors="replace") as f:
        for p in general:
            f.write(f"\n[[PDF p.{p}]]\n{texts[p]}\n")
    return ranges, sorted(set(unassigned)), n


def page_scores(text, tasks):
    low = text.lower()
    tags = collections.Counter(TASK_TAG.findall(text))
    return [sum(min(low.count(k), 3) for k in TASK_KEYWORDS[t]) + 12 * tags.get(t, 0) for t in tasks]


def segment_domain(pages, texts, tasks):
    """Asigna cada página a una tarea respetando el orden de las tareas (DP monótono)."""
    K, N = len(tasks), len(pages)
    sc = [page_scores(texts[p], tasks) for p in pages]
    NEG = float("-inf")
    best = [[NEG] * K for _ in range(N)]
    back = [[0] * K for _ in range(N)]
    for k in range(K):
        best[0][k] = sc[0][k] - (0.5 * k)  # leve preferencia por empezar en las primeras tareas
    for i in range(1, N):
        run_k, run_v = 0, best[i - 1][0]
        for k in range(K):
            if best[i - 1][k] > run_v:
                run_k, run_v = k, best[i - 1][k]
            # quedarse en k, o venir de cualquier j<=k (salto hacia delante con costo pequeño)
            stay = best[i - 1][k]
            jump = run_v - (0.3 if run_k != k else 0)
            if stay >= jump:
                best[i][k], back[i][k] = stay + sc[i][k], k
            else:
                best[i][k], back[i][k] = jump + sc[i][k], run_k
    k = max(range(K), key=lambda x: best[-1][x])
    path = [0] * N
    for i in range(N - 1, -1, -1):
        path[i] = k
        k = back[i][k]
    return {p: tasks[path[i]] for i, p in enumerate(pages)}


def map_slides(path, out, top=30, min_score=1):
    """Slides: para cada tarea, las páginas del dominio con mayor relevancia (sin exclusividad)."""
    r = PdfReader(path)
    texts = page_texts(r)
    n = len(texts)
    bounds = {1: (1, 269), 2: (270, 451), 3: (452, 1079), 4: (1080, 1281), 5: (1282, n)}
    blank = [p for p in range(1, n + 1) if len(texts[p].split()) < 5]
    groups = {}
    for dn, (a, b) in bounds.items():
        pages = [p for p in range(a, b + 1) if len(texts[p].split()) >= 5]
        sc = {p: page_scores(texts[p], TASKS[dn]) for p in pages}
        for k, t in enumerate(TASKS[dn]):
            ranked = sorted((p for p in pages if sc[p][k] >= min_score), key=lambda p: (-sc[p][k], p))[:top]
            groups[t] = sorted(ranked)
    ranges = write_group(os.path.join(out, "slides"), groups, texts)
    return ranges, [], blank, n


def compress(pages):
    out, start, prev = [], None, None
    for p in pages:
        if start is None:
            start = prev = p
        elif p == prev + 1:
            prev = p
        else:
            out.append(f"{start}-{prev}" if start != prev else str(start))
            start = prev = p
    if start is not None:
        out.append(f"{start}-{prev}" if start != prev else str(start))
    return ",".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guide", required=True)
    ap.add_argument("--slides", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    g_ranges, g_un, g_n = map_guide(a.guide, a.out)
    s_ranges, s_un, s_blank, s_n = map_slides(a.slides, a.out)
    mapa = dict(
        guia=dict(paginas=g_n, tareas={t: compress(p) for t, p in g_ranges.items()}, sin_asignar=compress(g_un)),
        slides=dict(paginas=s_n, tareas={t: compress(p) for t, p in s_ranges.items()}, sin_asignar=compress(s_un),
                    sin_texto=len(s_blank)),
    )
    json.dump(mapa, open(os.path.join(a.out, "mapa.json"), "w"), indent=1, ensure_ascii=False)
    print("tarea\tguía(págs)\tslides(págs)")
    for t in ALL_TASKS:
        print(f"{t}\t{len(g_ranges[t])}\t{len(s_ranges[t])}")
    print("sin cobertura guía:", [t for t in ALL_TASKS if not g_ranges[t]])
    print("sin cobertura slides:", [t for t in ALL_TASKS if not s_ranges[t]])
    print("guía sin asignar:", mapa["guia"]["sin_asignar"] or "-")
    print("slides sin asignar:", len(s_un), "págs; sin texto:", len(s_blank))
    return 0


if __name__ == "__main__":
    sys.exit(main())
