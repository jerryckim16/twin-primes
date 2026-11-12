"""Typeset plain-text notation in status.json / log entries for the website.

The JSON files are written as plain text (e.g. "M_{50,1/25} >= 4.0012", "H1 <= 246", "eps").
build_site.py passes each string through texify() before HTML-escaping it, which wraps the
recognised notation in $...$; KaTeX then renders it in the browser. The data files are never
modified. Text already inside $...$ is left alone, so entries may also be written in TeX directly.
"""
import re

E = r"\varepsilon"

RULES = [
    # longest, most specific first
    (r"\(k/\(k-1\)\+eps\) log\(2k-1\)", r"$(\\tfrac{k}{k-1}+" + E.replace("\\", "\\\\") + r")\\log(2k-1)$"),
    (r"k/\(k-1\) log\(2k-1\)", r"$\\tfrac{k}{k-1}\\log(2k-1)$"),
    (r"k/\(k-1\) log k", r"$\\tfrac{k}{k-1}\\log k$"),
    (r"64k²eps²/M_k", r"$64k^2\\varepsilon^2/M_k$"),
    (r"\(1\+eps-\|u\|\)/\(1\+eps\)", r"$(1+\\varepsilon-|u|)/(1+\\varepsilon)$"),
    (r"1\+eps-P1 = 2eps \+ \(1-eps-P1\)", r"$1+\\varepsilon-P_1=2\\varepsilon+(1-\\varepsilon-P_1)$"),
    (r"\(1-P1\)\^A", r"$(1-P_1)^A$"),
    (r"A!/\(k\+A\+w\)!", r"$A!/(k+A+w)!$"),
    (r"E\[prod P_j\(X\)\^b_j\]", r"$\\mathbb E[\\prod_j P_j(X)^{b_j}]$"),
    (r"\(beta/n\)\(a − S_A \+ n t_m\)", r"$(\\beta/n)(a-S_A+n\\,t_m)$"),
    (r"psi_m = Psi\(S - t_m, t_m\)", r"$\\psi_m=\\Psi(S-t_m,t_m)$"),
    (r"psi_m = \(int F dt_m\)/F", r"$\\psi_m=\\int F\\,dt_m/F$"),
    (r"Psi\(S - t_m, t_m\)", r"$\\Psi(S-t_m,t_m)$"),
    (r"F = prod 1/\(1\+A t_i\)", r"$F=\\prod_i 1/(1+At_i)$"),
    (r"\(t_m, ?S\)", r"$(t_m,S)$"),
    (r"\(k, eps\) = \((\d+), (\d+/\d+)\)", r"$(k,\\varepsilon)=(\1,\2)$"),
    (r"sup_eps M_\{([^}]*)\}", lambda m: "$\\sup_\\varepsilon M_{" + m.group(1).replace("eps", E) + "}$"),
    (r"M_\{([^}]*)\}", lambda m: "$M_{" + m.group(1).replace("eps", E) + "}$"),
    (r"\bM_(\d+|k)\b", r"$M_{\1}$"),
    (r"\bH1\b", r"$H_1$"),
    (r"DHL\[([^\]]*)\]", lambda m: "$\\mathrm{DHL}[" + m.group(1) + "]$"),
    (r"\(1\+eps\)", r"$(1+\\varepsilon)$"),
    (r"1\+eps\b", r"$1+\\varepsilon$"),
    (r"θ ≤ (\d+\.\d+)", r"$\\theta\\le \1$"),
    (r"\beps in \{([^}]*)\}", r"$\\varepsilon\\in\\{\1\\}$"),
    (r"\beps = ([\d/]+)", r"$\\varepsilon=\1$"),
    (r"\beps < 1", r"$\\varepsilon<1$"),
    (r"\b0 ≤ eps < 1", r"$0\\le\\varepsilon<1$"),
    (r"\bepsilon-enlarged", r"$\\varepsilon$-enlarged"),
    (r"\beps-enlarged", r"$\\varepsilon$-enlarged"),
    (r"\beps-problem", r"$\\varepsilon$-problem"),
    (r"\bepsilon < 1", r"$\\varepsilon<1$"),
    (r"\beps\b", r"$\\varepsilon$"),
    (r"\bt_m\b", r"$t_m$"),
    (r"\bt\b(?= is| of the| in)", r"$t$"),
    (r"\b1-P1\b", r"$1-P_1$"),
    (r"\bP2\b", r"$P_2$"),
    (r"\bP1\b", r"$P_1$"),
    (r"\bs1\b", r"$s_1$"),
    (r"\bk' ≥ k\b", r"$k'\\ge k$"),
    (r"\bk ≤ (\d+)", r"$k\\le \1$"),
    (r"\bk = (\d+)(, \d+)*", lambda m: "$k=" + m.group(0)[4:].replace(" ", "") + "$"),
    (r"\bk ≥ (\d+)", r"$k\\ge \1$"),
]


NUM = r"\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?"
CMP = {"≥": "\\ge ", "≤": "\\le ", ">": ">", "<": "<", "≈": "\\approx ", ">=": "\\ge "}
HAND = {
    "M_{k,eps} ≤ (1+eps) M_k, and M_{k,eps} ≥ (1+eps) M_k − 64k²eps²/M_k for small eps":
        "$M_{k,\\varepsilon}\\le(1+\\varepsilon)M_k$, and $M_{k,\\varepsilon}\\ge(1+\\varepsilon)M_k-64k^2\\varepsilon^2/M_k$ for small $\\varepsilon$",
    "sup_eps M_{49,eps} ≈ 3.991-3.994 < 4": "$\\sup_\\varepsilon M_{49,\\varepsilon}\\approx 3.991$–$3.994<4$",
    "(t_m/S above)": "($t_m/S$ above)",
    "every 0 ≤ eps < 1": "every $0\\le\\varepsilon<1$",
    "proportional to t_m/S above": "proportional to $t_m/S$ above",
}


def outside(s, fn):
    """Apply fn only to the parts of s that are not already inside $...$."""
    parts = s.split("$")
    for i in range(0, len(parts), 2):
        parts[i] = fn(parts[i])
    return "$".join(parts)


def texify(s):
    for a, b in HAND.items():
        s = s.replace(a, b)
    for pat, rep in RULES:
        s = outside(s, lambda t: re.sub(pat, rep, t))
    # "$A$ ≥ 4.00" -> one formula
    s = re.sub(r"\$([^$]+)\$ (>=|≥|≤|>|<|≈) (" + NUM + r")",
               lambda m: "$" + m.group(1) + CMP[m.group(2)] + m.group(3) + "$", s)
    s = outside(s, lambda t: re.sub(r"and (≥|>) (" + NUM + r")",
               lambda m: "and $" + CMP[m.group(1)] + m.group(2) + "$", t))
    s = outside(s, lambda t: re.sub(r"(vs truth|truth \(|optimistic by) ?(≥|≤) (" + NUM + r")",
               lambda m: m.group(1) + (" " if not m.group(1).endswith("(") else "") + "$" + CMP[m.group(2)] + m.group(3) + "$", t))
    s = s.replace("$$", "")
    return s
