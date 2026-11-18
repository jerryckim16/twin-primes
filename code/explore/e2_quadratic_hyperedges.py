#!/usr/bin/env python3
"""Exploration (Session 33): do quadratic parametrisations x = L1 L2, x + 2s = L3 L4 (all four forms prime)
evade the 2-adic obstruction for E2 pairs at distance d = 2?  Heuristic / exploratory.

1. Enumerate identities (a1 m+b1)(a2 m+b2) + 2s = (a3 m+b3)(a4 m+b4) with small coefficients, gcd(a,b) = 1,
   the four forms distinct and jointly admissible.
2. For vertex sets made of one or two such identities plus all linear edges (multipliers {1,3,5,7,11,13}) among the
   forms, test with an LP whether (1/2,...,1/2) is in the hull of target-free sign patterns (blocked) or not.
Usage: e2_quadratic_hyperedges.py [AMAX] [BMAX]
"""
import sys, itertools, math
import numpy as np
from scipy.optimize import linprog

AMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4
BMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 12
d = 2
MULT = [1, 3, 5, 7, 11, 13]

def admissible(forms):
    if any(math.gcd(a, b) != 1 for a, b in forms):
        return False
    for p in [q for q in range(2, len(forms) + 1) if all(q % r for r in range(2, q))]:
        if all(any((a * m + b) % p == 0 for a, b in forms) for m in range(p)):
            return False
    return True

forms = [(a, b) for a in range(1, AMAX + 1) for b in range(-BMAX, BMAX + 1) if math.gcd(a, b) == 1]
# products as polynomials: (A, B, C) = a1a2 m^2 + (a1b2+a2b1) m + b1b2
prod = {}
for i, f in enumerate(forms):
    for g in forms[i + 1:]:
        key = (f[0] * g[0], f[0] * g[1] + f[1] * g[0], f[1] * g[1])
        prod.setdefault(key, []).append((f, g))
ids = []
for (A, B, C), pairs in prod.items():
    for s in (1,):
        other = prod.get((A, B, C + 2 * s))
        if not other:
            continue
        for (f, g) in pairs:
            for (u, v) in other:
                quad = [f, g, u, v]
                if len(set(quad)) == 4 and admissible(quad):
                    ids.append((f, g, u, v))
print(f"admissible quadratic identities L1 L2 + 2 = L3 L4 with a <= {AMAX}, |b| <= {BMAX}: {len(ids)}")
for t in ids[:5]:
    print("  ", t)

def lin_edges(vs):
    E = []
    for i, (a, b) in enumerate(vs):
        for j, (a2, b2) in enumerate(vs):
            if i == j:
                continue
            for c in MULT:
                for c2 in MULT:
                    for s in (1, -1):
                        if c * a == c2 * a2 and c * b + s * d == c2 * b2:
                            E.append(((i, 1 if c == 1 else -1), (j, 1 if c2 == 1 else -1)))
    return E

def blocked(n, hyper):
    """hyper: list of tuples of (vertex, required sign). Blocked iff exists distribution on target-free patterns
    with every marginal P(eps_i = -1) = 1/2."""
    pats = [e for e in itertools.product((1, -1), repeat=n)
            if not any(all(e[v] == sgn for v, sgn in h) for h in hyper)]
    if not pats:
        return False
    Aeq = [[1.0] * len(pats)] + [[1.0 if e[i] == -1 else 0.0 for e in pats] for i in range(n)]
    beq = [1.0] + [0.5] * n
    r = linprog(np.zeros(len(pats)), A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
    return r.status == 0

res = {"single_blocked": 0, "single_unblocked": 0, "pair_blocked": 0, "pair_unblocked": 0}
examples = []
for t in ids:
    vs = list(t)
    hyper = [tuple((k, -1) for k in range(4))] + lin_edges(vs)
    if blocked(len(vs), hyper):
        res["single_blocked"] += 1
    else:
        res["single_unblocked"] += 1; examples.append(("single", t))
# pairs of identities sharing at least one form (at most 7 forms)
cnt = 0
for t1, t2 in itertools.combinations(ids, 2):
    vs = list(dict.fromkeys(list(t1) + list(t2)))
    if len(vs) > 7 or len(vs) == 8 or not admissible(vs):
        continue
    cnt += 1
    if cnt > 4000:
        break
    idx = {v: k for k, v in enumerate(vs)}
    hyper = [tuple((idx[v], -1) for v in t1), tuple((idx[v], -1) for v in t2)] + lin_edges(vs)
    if blocked(len(vs), hyper):
        res["pair_blocked"] += 1
    else:
        res["pair_unblocked"] += 1; examples.append(("pair", t1, t2))
print("pairs tested:", min(cnt, 4000))
print(res)
for e in examples[:5]:
    print("  unblocked:", e)
