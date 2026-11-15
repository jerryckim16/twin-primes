#!/usr/bin/env python3
"""Exploration, Session 19 (15 Nov 2026): do Liouville signs at EXTRA linear forms enlarge the class of
parity weights of papers/parity-barrier Section sec:bip?  (Open question 2 of that paper, narrow reading.)

Model.  Tuple coordinates 1..k (lambda(n+h_i)), auxiliary coordinates k+1..k+a (lambda(L_j(n)) for further
linear forms).  A weight is Omega >= 0 on {+-1}^{k+a}, not identically 0.  'Fair' (the paper's notion) = the
singleton coefficients hat-Omega({i}) vanish for the TUPLE coordinates i (only these enter the twisted main terms
for f = 1 and f = Lambda at position i); option --full also imposes every character that is not constant on the
attainable patterns (a stronger, Chowla-to-all-orders notion).
'Blocks the target E' = Omega vanishes on every pattern whose tuple part has a set {i : eps_i = -1}
containing some e in E.

Two cases.
 (A) independent auxiliary forms: all patterns attainable.  Then the tuple marginal of Omega is a fair
     tuple weight with the same support restriction, so nothing new can happen.
 (B) dependent auxiliary forms, e.g. L(n) = 2(n+h_1): lambda(L(n)) = -lambda(n+h_1).  Attainable patterns
     form a subset; the auxiliary coordinate is a function of a tuple coordinate, so again nothing new.
This script checks both by floating-point LP (scipy HiGHS) for DHL[4,3] (control: k <= 2m, blockable),
DHL[5,3] (k > 2m, not blockable by tuple weights) and the PM8b path target, with a = 0, 1, 2.
It is a numerical sanity check of an elementary marginalisation argument, not a certificate.
usage: python3 code/explore/aux_forms_lp.py   (writes code/explore/aux_forms_lp.json)"""
import itertools, json
import numpy as np
from scipy.optimize import linprog


def feasible(k, a, targets, dep=None, full=False):
    """dep: optional dict aux_index -> (tuple_index, sign): aux coordinate = sign * tuple coordinate."""
    n = k + a
    pats = []
    for eps in itertools.product((1, -1), repeat=n):
        if dep and any(eps[j] != s * eps[i] for j, (i, s) in dep.items()):
            continue
        neg = {i for i in range(k) if eps[i] == -1}
        if any(set(e) <= neg for e in targets):
            continue
        pats.append(eps)
    if not pats:
        return False, 0
    # characters nonconstant on attainable patterns (attainable = all patterns obeying dep)
    att = [eps for eps in itertools.product((1, -1), repeat=n)
           if not (dep and any(eps[j] != s * eps[i] for j, (i, s) in dep.items()))]
    rows = []
    sets = [S for r in range(1, n + 1) for S in itertools.combinations(range(n), r)] if full \
        else [(i,) for i in range(k)]
    for S in sets:
        if True:
            vals = {int(np.prod([e[i] for i in S])) for e in att}
            if len(vals) == 1:
                continue  # constant character: no constraint
            rows.append([float(np.prod([p[i] for i in S])) for p in pats])
    A = np.array(rows + [[1.0] * len(pats)])
    b = np.array([0.0] * len(rows) + [1.0])
    res = linprog(np.zeros(len(pats)), A_eq=A, b_eq=b, bounds=[(0, None)] * len(pats), method="highs")
    return bool(res.status == 0), len(pats)


def main():
    import sys
    full = "--full" in sys.argv
    out = []
    cases = [
        ("DHL[4,3]", 4, list(itertools.combinations(range(4), 3))),
        ("DHL[5,3]", 5, list(itertools.combinations(range(5), 3))),
        ("DHL[3,2]", 3, list(itertools.combinations(range(3), 2))),
        ("PM8b path {0,2},{2,6} on (0,2,6)", 3, [(0, 1), (1, 2)]),
    ]
    for name, k, T in cases:
        for a in (0, 1, 2):
            f, m = feasible(k, a, T, full=full)
            out.append({"target": name, "aux": a, "dependent": False, "blocked": f, "patterns": m})
            print(f"{name:34s} aux={a} independent: blocked={f} ({m} patterns)")
        f, m = feasible(k, 1, T, dep={k: (0, -1)}, full=full)
        out.append({"target": name, "aux": 1, "dependent": "aux = -tuple[0]", "blocked": f, "patterns": m})
        print(f"{name:34s} aux=1 dependent (lambda(2(n+h1))): blocked={f}")
    json.dump(out, open("code/explore/aux_forms_lp%s.json" % ("_full" if full else ""), "w"), indent=1)


if __name__ == "__main__":
    main()
