"""Heuristic: Richardson extrapolation of the grid lower bounds in code/parity/k3_thm314_dual.out.
Model r(n) = L - c/n (two largest n) and r(n) = L - c/n - d/n^2 (three largest n, when available).
Run: /usr/bin/python3 code/parity/k3_extrapolate.py code/parity/k3_thm314_dual.out
"""
import sys, re, numpy as np
from collections import defaultdict
d = defaultdict(dict)
for line in open(sys.argv[1]):
    m = re.match(r"eps=(\S+) mode=(\S+) n=(\d+) .* ratio>= (\S+)", line)
    if m: d[(float(m[1]), m[2])][int(m[3])] = float(m[4])
for (e, mode), r in sorted(d.items()):
    ns = sorted(r); out = f"eps={e:<6} {mode:<5} " + " ".join(f"n{n}={r[n]:.6f}" for n in ns)
    if len(ns) >= 2:
        n1, n2 = ns[-2:]; L2 = (n2*r[n2]-n1*r[n1])/(n2-n1); out += f" | L(1/n)={L2:.5f}"
    if len(ns) >= 3:
        M = np.array([[1, -1/n, -1/n**2] for n in ns[-3:]]); L3 = np.linalg.solve(M, [r[n] for n in ns[-3:]])[0]
        out += f" L(1/n,1/n^2)={L3:.5f}"
    print(out)
