#!/usr/bin/env python3
"""Descarga las 30 lecciones CCAR-F de claudecertificationguide.com a texto plano.

Uso: fetch_web_lessons.py --out /tmp/trabajo-cca/web [--delay 1.0]
Solo hace GET al sitemap y a las 30 páginas de lección (uso personal de estudio).
Salida: <out>/N.M.txt con la línea 'URL:' y 'TITULO:' seguida del texto.
"""
import argparse
import html
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

BASE = "https://claudecertificationguide.com"
UA = "Mozilla/5.0 (personal study notes)"
DOMAINS = ("1-agentic-architecture", "2-tool-design-mcp", "3-claude-code-config", "4-prompt-engineering", "5-context-management")
LESSON_RE = re.compile(r"/learn/(" + "|".join(DOMAINS) + r")/([1-5])-([1-7])-[a-z0-9-]+$")
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "pre", "blockquote", "div", "br", "ul", "ol", "table"}


def get(url, tries=3):
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"{url}: {last}")


class ArticleText(HTMLParser):
    """Extrae el texto de <h1> y <article>, ignorando script/style/svg/nav."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_article = 0
        self.skip = 0
        self.in_h1 = False
        self.title = ""
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.in_h1 = True
        if tag == "article":
            self.in_article += 1
        if tag in ("script", "style", "svg", "nav", "button"):
            self.skip += 1
        if self.in_article and not self.skip:
            if tag in ("h2", "h3", "h4"):
                self.out.append("\n\n" + "#" * int(tag[1]) + " ")
            elif tag == "li":
                self.out.append("\n- ")
            elif tag in BLOCK:
                self.out.append("\n")

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if tag == "article" and self.in_article:
            self.in_article -= 1
        if tag in ("script", "style", "svg", "nav", "button") and self.skip:
            self.skip -= 1
        if self.in_article and not self.skip and tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.in_h1:
            self.title += data
        elif self.in_article and not self.skip:
            self.out.append(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--delay", type=float, default=1.0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sitemap = get(BASE + "/sitemap.xml")
    urls = []
    for u in re.findall(r"<loc>([^<]+)</loc>", sitemap):
        m = LESSON_RE.search(u)
        if m and m.group(1)[0] == m.group(2):
            key = f"{m.group(2)}.{m.group(3)}"
            if key not in [k for k, _ in urls]:
                urls.append((key, u))
    if len(urls) != 30:
        print(f"ERROR: se esperaban 30 lecciones y hay {len(urls)}", file=sys.stderr)
        return 2
    for key, u in urls:
        p = ArticleText()
        p.feed(get(u))
        text = re.sub(r"[ \t]+", " ", "".join(p.out))
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        title = html.unescape(p.title).strip()
        with open(os.path.join(a.out, f"{key}.txt"), "w", encoding="utf-8") as f:
            f.write(f"URL: {u}\nTITULO: {title}\n\n{text}\n")
        print(f"{key}\t{len(text.split())}\t{title}")
        time.sleep(a.delay)
    return 0


if __name__ == "__main__":
    sys.exit(main())
