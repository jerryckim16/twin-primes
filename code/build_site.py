#!/usr/bin/env python3
"""Build index.html (the project page) from status.json, log/entries.json and paper/main.tex.

Run from the project root:  python3 code/build_site.py
Needs pandoc.  Writes docs/index.html (the GitHub Pages site), copies the compiled
paper to docs/twin-primes-paper.pdf if paper/main.pdf exists, and writes log/research-log.md.
"""
import json, re, subprocess, html, os, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
st = json.load(open("status.json"))
log = json.load(open("log/entries.json"))
bh = json.load(open("log/bound-history.json")) if os.path.exists("log/bound-history.json") else []
esc = html.escape
from texify_text import texify
tx = lambda s: esc(texify(s))   # plain text with notation typeset by KaTeX

# ---------- paper -> HTML fragment (MathML) ----------
tex = open("paper/main.tex").read()
bib = re.search(r"\\begin\{thebibliography\}\{\d+\}(.*?)\\end\{thebibliography\}", tex, re.S)
items = re.findall(r"\\bibitem\{([^}]*)\}(.*?)(?=\\bibitem|\Z)", bib.group(1), re.S)
num = {k: i + 1 for i, (k, _) in enumerate(items)}
def cite(m):
    loc, keys = m.group(1), [k.strip() for k in m.group(2).split(",")]
    inside = ", ".join(str(num[k]) for k in keys) + (", " + loc if loc else "")
    return "[" + inside + "]"
tex2 = re.sub(r"\\cite(?:\[([^\]]*)\])?\{([^}]*)\}", cite, tex)
# pandoc does not number equations: number the labelled ones by hand
eqn = {}
def number_eq(m):
    eqn[m.group(1)] = len(eqn) + 1
    return "\\[" + m.group(2).strip() + "\\qquad(" + str(eqn[m.group(1)]) + ")\\]"
tex2 = re.sub(r"\\begin\{equation\}\\label\{([^}]*)\}(.*?)\\end\{equation\}", number_eq, tex2, flags=re.S)
tex2 = re.sub(r"\\eqref\{([^}]*)\}", lambda m: "(" + str(eqn[m.group(1)]) + ")", tex2)
enum = "\\section*{References}\n\\begin{enumerate}\n" + "\n".join("\\item " + t.strip() for _, t in items) + "\n\\end{enumerate}"
tex2 = tex2[:tex2.index("\\begin{thebibliography}")] + enum + "\n\\end{document}\n"
with tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False) as f:
    f.write(tex2); tmp = f.name
paper = subprocess.run(["pandoc", tmp, "-f", "latex", "-t", "html", "--katex"], capture_output=True, text=True, check=True).stdout
os.unlink(tmp)
paper = re.sub(r"<table>", '<div class="scroll"><table>', paper).replace("</table>", "</table></div>")
paper = re.sub(r'(<span\s+class="math display">.*?</span>)', r'<div class="scroll eq">\1</div>', paper, flags=re.S)
title = re.search(r"\\title(?:\[[^\]]*\])?\{(.*?)\}\n", tex, re.S).group(1)
author = re.search(r"\\author\{(.*?)\}", tex).group(1)
date = re.search(r"\\date\{(.*?)\}", tex).group(1)
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
with tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False) as f:
    f.write(re.sub(r"\\textsc\{([^}]*)\}", r"\\textsc{\1}", abstract).replace("\\lbl", "\\textsc")); tmp = f.name
abstract_html = subprocess.run(["pandoc", tmp, "-f", "latex", "-t", "html", "--katex"], capture_output=True, text=True, check=True).stdout
os.unlink(tmp)


# ---------- bound history chart (log scale) ----------
def bound_chart(hist, established, claimed):
    if not hist:
        return ""
    W, H, L, R, T, B = 520, 300, 46, 142, 40, 50
    vals = [h["bound"] for h in hist] + [established, claimed]
    lo = min(vals) * 0.85; hi = max(vals) * 1.12
    def y(v): return T + (H - T - B) * (math.log(hi) - math.log(v)) / (math.log(hi) - math.log(lo))
    n = len(hist)
    def x(i): return L + 26 + (W - L - R - 40) * (i / max(n - 1, 1))
    out = [f'<svg viewBox="0 0 {W} {H}" class="bchart" role="img" aria-label="Bound reproduced by this project after each improvement, logarithmic scale: ' +
           ", ".join(str(h["bound"]) for h in hist) + f'. Established {established}, claimed {claimed}.">']
    for t in (150, 200, 300, 400, 500, 600, 800, 1000):
        if lo <= t <= hi:
            out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="grid"/>'
                       f'<text x="{L-8}" y="{y(t)+4:.1f}" class="tick" text-anchor="end">{t}</text>')
    for v, cls, lab in ((established, "ref ok", "established"), (claimed, "ref warn", "claimed")):
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="{cls}"/>'
                   f'<text x="{W-R+8}" y="{y(v)+4:.1f}" class="reflab {cls.split()[1]}">{v} {lab}</text>')
    pts = []
    for i, h in enumerate(hist):
        if i: pts.append(f"{x(i):.1f},{y(hist[i-1]['bound']):.1f}")
        pts.append(f"{x(i):.1f},{y(h['bound']):.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" class="step"/>')
    for i, h in enumerate(hist):
        cx, cy = x(i), y(h["bound"])
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" class="pt"><title>{h["date"]}, session {h["session"]}: {h["bound"]} (k = {h["k"]}). {esc(h["how"])}</title></circle>'
                   f'<text x="{cx:.1f}" y="{cy-14:.1f}" class="ptlab" text-anchor="middle">{h["bound"]}</text>'
                   f'<text x="{cx:.1f}" y="{H-B+26:.1f}" class="tick" text-anchor="middle">S{h["session"]}</text>')
    out.append(f'<text x="{L+26}" y="{H-4}" class="tick">session</text></svg>')
    rows = "".join(f'<tr><td>{esc(h["date"])}</td><td>S{h["session"]}</td><td class="num">{h["bound"]}</td><td class="num">{h["k"]}</td><td>{tx(h["how"])}</td></tr>' for h in reversed(hist))
    table = f'<details class="bh"><summary>Every improvement ({len(hist)})</summary><div class="scroll"><table><thead><tr><th>Date</th><th>Session</th><th>Bound</th><th>k</th><th>How</th></tr></thead><tbody>{rows}</tbody></table></div></details>'
    return "\n".join(out) + table

# ---------- pieces ----------
b = st["bounds"]
LABEL_CLASS = {"Lean-checked": "ok", "Computed": "ok", "Proved here": "own", "Literature": "lit", "Claimed": "warn", "Open": "open"}
STATUS_CLASS = {"ruled out": "open", "open": "warn", "next": "lit", "works": "ok", "partial": "own"}

def chip(text, cls): return f'<span class="chip {cls}">{esc(text)}</span>'

# log-scale number line from 2 to 700
import math
def xpos(v, lo=1.6, hi=760.0): return 4 + 92 * (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo))
marks = [(b["target"], "the conjecture", "goal", "up"), (b["sieve_limit_geh"], "sieve limit, even assuming GEH", "limit", "down"),
         (b["claimed"], "claimed, 2026 preprints", "warn", "up ar"), (b["established"], "established", "ok", "down"),
         (b["project"], "reproduced here" + (" (conditional)" if b.get("project_note") else ""), "own", "up al")]
line = ['<div class="scale" role="img" aria-label="Gap bounds on a logarithmic scale: target 2, sieve limit 6, claimed %d, established %d, reproduced here %d">' % (b["claimed"], b["established"], b["project"]), '<div class="axis"></div>']
for v, lab, cls, side in marks:
    line.append(f'<div class="mark {cls} {side}" style="left:{xpos(v):.2f}%"><span class="dot"></span><span class="num">{v}</span><span class="cap">{esc(lab)}</span></div>')
line.append("</div>")
scale = "\n".join(line)

bchart = bound_chart(bh, b["established"], b["claimed"])
tiles = f"""
<div class="tiles">
  <div class="tile ok"><div class="k">Established</div><div class="v">{b['established']}</div><div class="d">Polymath8b, 2014. Checked in Lean by others, given Bombieri&ndash;Vinogradov.</div></div>
  <div class="tile warn"><div class="k">Claimed</div><div class="v">{b['claimed']}</div><div class="d">2026 preprints. Not yet fully verified independently.</div></div>
  <div class="tile own"><div class="k">Reproduced here</div><div class="v">{b['project']}</div><div class="d">{esc(b.get('project_note', "What this project's own certificates and Lean code reach so far."))}</div></div>
  <div class="tile goal"><div class="k">Twin primes</div><div class="v">{b['target']}</div><div class="d">Open. Out of reach of every current method.</div></div>
</div>"""

rows = "\n".join(f'<tr><td>{chip(r["label"], LABEL_CLASS.get(r["label"], "lit"))}</td><td>{tx(r["text"])}</td><td class="where">{esc(r["where"])}</td></tr>' for r in st["results"])
ideas = "\n".join(f'<tr><td>{chip(i["status"], STATUS_CLASS.get(i["status"], "lit"))}</td><td>{tx(i["idea"])}<div class="note">{tx(i["note"])}</div></td><td class="where">{esc(i["origin"])}</td></tr>' for i in st["ideas"])

def entry(e):
    out = [f'<article class="entry"><header><span class="when">{esc(e["date"])} &middot; {esc(e["slot"])}</span><h3>{tx(e["title"])}</h3></header>']
    out.append("<ul>" + "".join(f"<li>{tx(x)}</li>" for x in e.get("did", [])) + "</ul>")
    if e.get("failed"):
        out.append('<p class="sub">Did not work or is blocked</p><ul class="failed">' + "".join(f"<li>{tx(x)}</li>" for x in e["failed"]) + "</ul>")
    if e.get("next"):
        out.append(f'<p class="next"><span class="sub">Next</span> {tx(e["next"])}</p>')
    out.append("</article>")
    return "\n".join(out)
entries = "\n".join(entry(e) for e in log)

files = []
for base, _, fs in os.walk("."):
    for f in sorted(fs):
        p = os.path.join(base, f)[2:]
        if p.startswith((".git/", "docs/", "site/", "paper/main.")) and not p.endswith("main.tex"): continue
        if any(x in p for x in (".lake", "__pycache__", "build.log", "pandoc.err", "paper.html", ".log", "lake-manifest", ".gitignore")): continue
        files.append(p)
REPO = "https://github.com/jerryckim16/twin-primes"
files_html = "".join(f'<li><a href="{REPO}/blob/main/{esc(p)}"><code>{esc(p)}</code></a></li>' for p in sorted(files))

CSS = """
:root{ /* layout: one reading column, status first, the log next, the paper last */
  --bg:#f3f5f7; --surface:#ffffff; --ink:#131a22; --muted:#55616e; --rule:#d5dbe1;
  --accent:#0d5c8f; --ok:#1b7a4a; --warn:#a15c00; --open:#a8322b; --own:#5b3fa3;
  --display:"STIX Two Text","Iowan Old Style","Palatino Linotype",Georgia,serif;
  --body:"STIX Two Text","Iowan Old Style","Palatino Linotype",Georgia,serif;
  --mono:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f1419; --surface:#171e26; --ink:#e6ebf0; --muted:#9aa7b4; --rule:#2b3642;
  --accent:#6db6e6; --ok:#5fc48d; --warn:#e0a44a; --open:#ee8279; --own:#b39cf0; color-scheme:dark; } }
:root[data-theme="dark"]{
  --bg:#0f1419; --surface:#171e26; --ink:#e6ebf0; --muted:#9aa7b4; --rule:#2b3642;
  --accent:#6db6e6; --ok:#5fc48d; --warn:#e0a44a; --open:#ee8279; --own:#b39cf0; color-scheme:dark; }
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:18px;line-height:1.55}
main{max-width:46rem;margin:0 auto;padding:28px 18px 64px;display:flex;flex-direction:column;gap:36px}
h1{font-family:var(--display);font-weight:600;font-size:1.9rem;line-height:1.15;margin:0;text-wrap:balance}
h2{font-family:var(--mono);font-weight:500;font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:0 0 12px;padding-bottom:8px;border-bottom:1px solid var(--rule)}
h3{font-family:var(--display);font-weight:600;font-size:1.15rem;margin:2px 0 8px;text-wrap:balance}
p{margin:0 0 .8em} a{color:var(--accent)}
.links{display:flex;flex-wrap:wrap;gap:8px 18px;margin:12px 0 0;font-family:var(--mono);font-size:.8rem}
.lede{color:var(--muted);margin:10px 0 0;max-width:38rem}
.meta{font-family:var(--mono);font-size:.74rem;color:var(--muted);margin-top:12px}
.notice{border-left:3px solid var(--open);background:var(--surface);padding:12px 14px;font-size:.95rem}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.tile{background:var(--surface);border:1px solid var(--rule);border-top:3px solid var(--c);padding:12px}
.tile .k{font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--c)}
.tile .v{font-family:var(--display);font-size:2.3rem;font-weight:600;line-height:1.1;font-variant-numeric:tabular-nums}
.tile .d{font-size:.8rem;color:var(--muted);line-height:1.35}
.ok{--c:var(--ok)} .warn{--c:var(--warn)} .open{--c:var(--open)} .own{--c:var(--own)} .lit{--c:var(--accent)} .goal{--c:var(--ink)} .limit{--c:var(--muted)}
.scale{position:relative;height:150px;margin:8px 0 18px}
.scale .axis{position:absolute;left:0;right:0;top:74px;height:2px;background:var(--rule)}
.mark{position:absolute;top:0;height:150px;width:0}
.mark .dot{position:absolute;top:69px;left:-6px;width:12px;height:12px;border-radius:50%;background:var(--c);border:2px solid var(--bg)}
.mark .num{position:absolute;left:-40px;width:80px;text-align:center;font-family:var(--mono);font-size:.9rem;font-weight:500;color:var(--c);font-variant-numeric:tabular-nums}
.mark .cap{position:absolute;left:-52px;width:104px;text-align:center;font-size:.68rem;line-height:1.2;color:var(--muted)}
.mark.up .num{top:44px} .mark.up .cap{top:2px;height:40px;display:flex;align-items:flex-end;justify-content:center}
.mark.down .num{top:88px} .mark.down .cap{top:110px}
.mark.ar .num,.mark.ar .cap{left:auto;right:-4px;text-align:right;justify-content:flex-end;width:120px}
.mark.al .num,.mark.al .cap{left:-4px;text-align:left;justify-content:flex-start;width:120px}
.scalenote{font-size:.8rem;color:var(--muted);margin:0}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{text-align:left;vertical-align:top;padding:9px 10px 9px 0;border-bottom:1px solid var(--rule)}
td.where{font-family:var(--mono);font-size:.7rem;color:var(--muted);min-width:7rem;overflow-wrap:anywhere}
.chip{display:inline-block;font-family:var(--mono);font-size:.66rem;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;color:var(--c);border:1px solid var(--c);border-radius:3px;padding:1px 6px}
.note{color:var(--muted);font-size:.85rem;margin-top:3px}
.entry{background:var(--surface);border:1px solid var(--rule);padding:16px 18px}
.entry + .entry{margin-top:12px}
.entry .when{font-family:var(--mono);font-size:.72rem;color:var(--muted)}
.entry ul{margin:0 0 .8em;padding-left:1.15em} .entry li{margin-bottom:.35em;font-size:.95rem}
.sub{font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 4px}
.next{margin:0;font-size:.95rem} .next .sub{margin-right:6px;color:var(--accent)}
.failed li{color:var(--muted)}
.paper{background:var(--surface);border:1px solid var(--rule);padding:22px 20px}
.paper h1{font-size:1.25rem;margin:1.4em 0 .5em} .paper h2{font-family:var(--display);text-transform:none;letter-spacing:0;font-size:1.05rem;font-weight:600;color:var(--ink);border:0;padding:0;margin:1.2em 0 .4em}
.paper .ptitle{font-size:1.45rem;margin:0 0 6px} .paper .pauthor{margin:0;color:var(--muted)} .paper .pdate{font-family:var(--mono);font-size:.72rem;color:var(--muted);margin:2px 0 14px}
.paper .abstract{font-size:.92rem;border-left:2px solid var(--rule);padding-left:12px;color:var(--muted)}
.paper table{width:auto;font-variant-numeric:tabular-nums} .paper td,.paper th{padding:3px 12px 3px 0;border-bottom:0;white-space:nowrap} .paper thead th{border-bottom:1px solid var(--rule)}
.paper caption{caption-side:top;text-align:left;font-size:.85rem;color:var(--muted);padding-bottom:6px;white-space:normal}
.paper .eq{padding:2px 0 6px} .paper .eq .katex-display{margin:.4em 0;width:max-content;min-width:100%}
.katex{font-size:1.06em} .paper .math,.paper .scroll,.abstract .math{position:relative} .math.inline.wide{display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle;padding:2px 0}
.paper .smallcaps{font-variant:small-caps;letter-spacing:.03em} .paper .theorem em,.paper .proposition em,.paper .corollary em{font-style:italic}
.paper .proof{margin:.6em 0} .paper ol,.paper ul{padding-left:1.3em}
.paper code{font-family:var(--mono);font-size:.82em;overflow-wrap:anywhere}
.paper a{overflow-wrap:anywhere}
.bchart{width:100%;max-width:600px;height:auto;display:block;font-family:var(--mono)}
.bchart .grid{stroke:var(--rule);stroke-width:1}
.bchart .tick{fill:var(--muted);font-size:15px}
.bchart .ref{stroke-width:1.5;stroke-dasharray:5 4} .bchart .ref.ok{stroke:var(--ok)} .bchart .ref.warn{stroke:var(--warn)}
.bchart .reflab{font-size:15px} .bchart .reflab.ok{fill:var(--ok)} .bchart .reflab.warn{fill:var(--warn)}
.bchart .step{fill:none;stroke:var(--own);stroke-width:3.5;stroke-linejoin:round}
.bchart .pt{fill:var(--own);stroke:var(--bg);stroke-width:2}
.bchart .ptlab{fill:var(--own);font-size:19px;font-weight:500;paint-order:stroke;stroke:var(--bg);stroke-width:5px}
.bh{margin-top:8px;font-size:.88rem} .bh summary{cursor:pointer;color:var(--accent);font-family:var(--mono);font-size:.78rem}
.bh td.num{font-variant-numeric:tabular-nums;text-align:right;padding-right:14px} .bh th{font-family:var(--mono);font-size:.7rem;color:var(--muted);font-weight:500}
.files{columns:2;column-gap:24px;list-style:none;padding:0;margin:0;font-size:.8rem} .files code{font-family:var(--mono);overflow-wrap:anywhere}
.papers{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:14px} .papers li{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}
.papers .ptl{font-family:var(--display);font-weight:600;font-size:1.02rem;line-height:1.3;margin:0 0 4px} .papers .pmeta{font-family:var(--mono);font-size:.72rem;color:var(--muted);margin:0 0 6px} .papers .pdesc{font-size:.92rem;margin:0 0 6px} .papers .plinks{font-family:var(--mono);font-size:.78rem;display:flex;flex-wrap:wrap;gap:6px 16px;margin:0}
@media (max-width:640px){ body{font-size:17px} .tiles{grid-template-columns:repeat(2,1fr)} .files{columns:1}
  .mark .cap{font-size:.6rem;left:-38px;width:76px} h1{font-size:1.6rem}
  .mark.al .num,.mark.al .cap,.mark.ar .num,.mark.ar .cap{width:72px}
  .ledger tr{display:block;padding:10px 0;border-bottom:1px solid var(--rule)} .ledger td{display:block;border:0;padding:0 0 4px} .ledger td.where{min-width:0} }
"""

# ---------- papers: the main paper and every small-results paper (index: papers/README.md) ----------
def papers_list():
    gh = "https://github.com/jerryckim16/twin-primes/blob/main/"
    items = [f'<li><p class="ptl">{esc(title)}</p><p class="pmeta">Main paper &middot; {esc(date)} &middot; living paper, updated with every run</p>'
             '<p class="pdesc">The full record: state of the problem, every certificate, our own results and the programme.</p>'
             f'<p class="plinks"><a href="twin-primes-paper.pdf">PDF</a> <a href="{gh}paper/main.tex">LaTeX source</a></p></li>']
    idx = "papers/README.md"
    if os.path.exists(idx):
        for line in open(idx):
            m = re.match(r"\|\s*`([^`]+)`\s*\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|\s*$", line)
            if not m:
                continue
            slug, ptitle, ver, status, desc = (x.strip() for x in m.groups())
            src = f"papers/{slug}/main.pdf"
            if os.path.exists(src):
                os.makedirs("docs/papers", exist_ok=True)
                import shutil; shutil.copy(src, f"docs/papers/{slug}.pdf")
            pdf = f'<a href="papers/{esc(slug)}.pdf">PDF</a> ' if os.path.exists(f"docs/papers/{slug}.pdf") else ""
            items.append(f'<li><p class="ptl">{esc(ptitle)}</p><p class="pmeta">Small-results paper &middot; version {esc(ver)} &middot; {esc(status)}</p>'
                         f'<p class="pdesc">{esc(desc)}</p><p class="plinks">{pdf}<a href="{gh}papers/{esc(slug)}/main.tex">LaTeX source</a></p></li>')
    return '<ul class="papers">' + "".join(items) + "</ul>"
papers_html = papers_list()

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Twin Prime Notebook</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<style>{CSS}</style>
<script>
// Typeset every math span pandoc emitted (inline and display) with KaTeX.
// If KaTeX cannot load, the raw TeX stays visible.
window.addEventListener("DOMContentLoaded", function () {{
  if (!window.katex) return;
  document.querySelectorAll("span.math").forEach(function (el) {{
    var tex = el.textContent.trim();
    // strip pandoc's delimiters (backslash + bracket at both ends) if present
    if (tex.length > 3 && tex.charCodeAt(0) === 92 && "([".indexOf(tex.charAt(1)) >= 0) tex = tex.slice(2, -2);
    var display = el.classList.contains("display");
    try {{ katex.render(tex, el, {{displayMode: display, throwOnError: false, strict: "ignore"}}); }}
    catch (e) {{ return; }}
    if (!display) {{
      var box = el.closest("p, li, td, div");
      if (box && el.getBoundingClientRect().right > box.getBoundingClientRect().right + 1) el.classList.add("wide");
    }}
  }});
  // Status, results, ideas and log come from JSON as text with $...$ notation (code/texify_text.py).
  if (window.renderMathInElement) renderMathInElement(document.body, {{
    delimiters: [{{left: "$", right: "$", display: false}}],
    ignoredClasses: ["paper"], throwOnError: false, strict: "ignore"}});
}});
</script>
</head>
<body>
<main>
<header>
  <h1>Twin Prime Notebook</h1>
  <p class="lede">A running record of work on small gaps between primes: a LaTeX paper, a Lean development and exact certificates, updated three times a day.</p>
  <p class="links"><a href="twin-primes-paper.pdf">Paper (PDF)</a> <a href="#papers">All papers</a> <a href="https://github.com/jerryckim16/twin-primes">Source on GitHub</a> <a href="https://github.com/jerryckim16/twin-primes/commits/main">Every update</a></p>
  <p class="meta">Paper version {esc(st['version'])} &middot; updated {esc(st['updated'])} &middot; {st['session_count']} session{'s' if st['session_count'] != 1 else ''} logged</p>
</header>

<p class="notice"><strong>No proof of the twin prime conjecture is claimed here.</strong> The conjecture is open, and the sieve methods behind every bound on this page cannot reach 2. Nothing on this page has been peer reviewed.</p>

<section>
  <h2>Where the bound stands</h2>
  {scale}
  <p class="scalenote">Smallest gap proved to occur infinitely often between primes, on a logarithmic scale. Lower is better.</p>
  {tiles}
</section>

<section id="papers">
  <h2>Papers</h2>
  {papers_html}
  <p class="scalenote" style="margin-top:10px">Drafts, not peer reviewed. Each small-results paper keeps growing as new results are checked; its version and changelog are in the PDF.</p>
</section>

<section>
  <h2>Our bound, improvement by improvement</h2>
  <p class="scalenote" style="margin-bottom:8px">The bound reproduced end to end by this project, each time it went down. Logarithmic scale. The last step, 240, is conditional: it reproduces the variational step of Stadlmann's argument and rests on his equidistribution estimates, which this project has not verified. The twin prime conjecture would be 2, far below this chart.</p>
  {bchart}
</section>

<section>
  <h2>Research log</h2>
  {entries}
</section>

<section>
  <h2>Results so far</h2>
  <div class="scroll"><table class="ledger"><tbody>
  {rows}
  </tbody></table></div>
</section>

<section>
  <h2>Ideas ledger</h2>
  <div class="scroll"><table class="ledger"><tbody>
  {ideas}
  </tbody></table></div>
</section>

<section>
  <h2>The paper</h2>
  <div class="paper">
    <p class="ptitle"><strong>{esc(title)}</strong></p>
    <p class="pauthor">{esc(author)}</p>
    <p class="pdate">{esc(date)}</p>
    <div class="abstract">{abstract_html}</div>
    {paper}
  </div>
</section>

<section>
  <h2>Source files in this project</h2>
  <ul class="files">{files_html}</ul>
  <p class="scalenote" style="margin-top:10px">Rebuild: <code>lake build</code> in <code>lean/</code>; <code>latexmk -pdf main.tex</code> in <code>paper/</code>; <code>python3 code/make_cert.py 102 15</code>.</p>
</section>
</main>
</body>
</html>
"""
os.makedirs("docs", exist_ok=True)
open("docs/index.html", "w").write(page)
open("docs/.nojekyll", "w").write("")
if os.path.exists("paper/main.pdf"):
    import shutil; shutil.copy("paper/main.pdf", "docs/twin-primes-paper.pdf")

md = ["# Research log\n"]
for e in log:
    md.append(f"## {e['date']} - {e['slot']}: {e['title']}\n")
    md += [f"- {x}" for x in e.get("did", [])]
    if e.get("failed"): md += ["", "Did not work or is blocked:"] + [f"- {x}" for x in e["failed"]]
    if e.get("next"): md += ["", f"Next: {e['next']}"]
    md.append("")
open("log/research-log.md", "w").write("\n".join(md))
print("built docs/index.html", len(page), "bytes;", len(files), "source files listed")
