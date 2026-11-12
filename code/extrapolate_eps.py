#!/usr/bin/env python3
"""Degree extrapolation of certified lower bounds for M_{k,eps} (Session 4, own experiment).

Reads the JSON lines written by scan_eps.py (plus optional extra points given on the command line
as k:eps:D:value) and, for each (k, eps), fits the last three even-spaced degrees with
  (G) geometric model  M(D) = M_inf - C r^D        (Aitken delta-squared), and
  (P) power model      M(D) = M_inf - C D^{-alpha}  (solved numerically).
The output is a HEURISTIC estimate of the limit D -> infinity. It is not a bound of any kind.

usage: extrapolate_eps.py runs/scan_k49.jsonl runs/scan_k50.jsonl [k:eps:D:value ...]
"""
import sys, json
from collections import defaultdict
from scipy.optimize import brentq

data = defaultdict(dict)
for arg in sys.argv[1:]:
    if arg.endswith(".jsonl"):
        for line in open(arg):
            r = json.loads(line)
            data[(r["k"], r["eps"])][r["D"]] = r["certified"]
    else:
        k, e, D, v = arg.split(":")
        data[(int(k), e)][int(D)] = float(v)

def aitken(x0, x1, x2):
    d = (x2 - x1) - (x1 - x0)
    return x2 - (x2 - x1) ** 2 / d if d < 0 else float("nan")

def power(D, x):
    (D0, D1, D2), (x0, x1, x2) = D, x
    ratio = (x2 - x1) / (x1 - x0)
    f = lambda a: (D1 ** -a - D2 ** -a) / (D0 ** -a - D1 ** -a) - ratio
    try:
        a = brentq(f, 1e-3, 60)
    except ValueError:
        return float("nan"), float("nan")
    C = (x2 - x1) / (D1 ** -a - D2 ** -a)
    return x2 + C * D2 ** -a, a

def fits(pts, Ds):
    xs = [pts[D] for D in Ds]
    return aitken(*xs), power(Ds, xs)

if __name__ == "__main__":
    for (k, e), pts in sorted(data.items()):
        Ds = sorted(pts)
        # use the last three degrees with equal spacing
        for step in (2, 4, 1, 3, 5):
            tri = [D for D in Ds if D <= Ds[-1] and (Ds[-1] - D) % step == 0 and Ds[-1] - D <= 2 * step]
            if len(tri) == 3: break
        else:
            print(k, e, "too few points", pts); continue
        g, (p, a) = fits(pts, tri)
        print("k=%d eps=%-5s D=%s  last=%.5f  geometric->%.5f  power->%.5f (alpha=%.2f)"
              % (k, e, tri, pts[tri[-1]], g, p, a))
