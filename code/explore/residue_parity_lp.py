#!/usr/bin/env python3
"""Exploration 2026-11-15 (Session 18): can a parity weight that also depends on n mod p beat the k <= 2m criterion
of the parity paper (Prop. prop:bipartite(b))?  Toy model, Heuristic.
Classes b mod p (p > diameter, so each class has at most one 'dead' position j with p | n+h_j, where Lambda vanishes).
Variables: for each class b a measure on E-free subsets I of the alive positions (target: m+1 primes anywhere).
Uniform true masses: nu-mass 1/p per class, prime mass at position i spread over its p-1 alive classes.
 GLOBAL fairness: for each i, sum_{b alive for i} 2 P_b(i in I) w_b/(p-1) >= sum_b w_b/p   (one constant per position)
 CLASSWISE fairness: P_b(i in I) = 1/2 for every class b and alive i (the sieve sees main terms class by class).
Output: feasibility for k = 2m+1 under each model; expected: global feasible iff k <= 2m p/(p-1), classwise iff k <= 2m."""
import itertools, json
import numpy as np
from scipy.optimize import linprog

def lp(k, m, p, classwise):
    classes = list(range(p))
    dead = {b: [j for j in range(k) if (b + j * 0 + (j)) % p == 0] for b in classes}  # position j dead in class b = j
    dead = {b: ([b] if b < k else []) for b in classes}
    var = []  # (b, I)
    for b in classes:
        alive = [i for i in range(k) if i not in dead[b]]
        for r in range(0, m + 1):
            for I in itertools.combinations(alive, r):
                var.append((b, I))
    nv = len(var); A_ub = []; b_ub = []; A_eq = []; b_eq = []
    # normalisation: total class weight = 1 (w_b = sum of the measure in class b)
    A_eq.append([1.0] * nv); b_eq.append(1.0)
    if classwise:
        for b in classes:
            alive = [i for i in range(k) if i not in dead[b]]
            for i in alive:
                row = [0.0] * nv
                for c, (bb, I) in enumerate(var):
                    if bb == b: row[c] = (1.0 if i in I else 0.0) - 0.5
                A_eq.append(row); b_eq.append(0.0)
            # uniform class weights (Type I main terms of nu unchanged)
            row = [0.0] * nv
            for c, (bb, I) in enumerate(var):
                if bb == b: row[c] = 1.0
            A_eq.append(row); b_eq.append(1.0 / p)
    else:
        for i in range(k):
            row = [0.0] * nv
            for c, (bb, I) in enumerate(var):
                if i not in dead[bb]:
                    row[c] -= 2.0 * (1.0 if i in I else 0.0) / (p - 1)
                row[c] += 1.0 / p
            A_ub.append(row); b_ub.append(0.0)
    r = linprog(np.zeros(nv), A_ub=A_ub or None, b_ub=b_ub or None, A_eq=A_eq, b_eq=b_eq,
                bounds=[(0, None)] * nv, method="highs")
    return r.status == 0

out = {}
for m in (1, 2):
    for k in (2 * m, 2 * m + 1, 2 * m + 2):
        for p in (k + 1, k + 2, 11, 23):
            if p <= k: continue
            out[f"m={m},k={k},p={p}"] = {"global": lp(k, m, p, False), "classwise": lp(k, m, p, True),
                                        "predicted_global": k <= 2 * m * p / (p - 1)}
print(json.dumps(out, indent=1))
json.dump(out, open("code/explore/residue_parity_lp.json", "w"), indent=1)

def lp_multi(k, m, primes, classwise):
    """classes mod q = prod(primes); position j dead in class b iff b = j mod p for some p (positions h_j = j)."""
    q = 1
    for p in primes: q *= p
    deadf = lambda b: {j for j in range(k) if any(b % p == j % p for p in primes)}
    var = []
    for b in range(q):
        alive = [i for i in range(k) if i not in deadf(b)]
        for r in range(m + 1):
            for I in itertools.combinations(alive, r): var.append((b, I))
    nv = len(var); alive_count = [sum(1 for b in range(q) if i not in deadf(b)) for i in range(k)]
    A_eq = [[1.0] * nv]; b_eq = [1.0]; A_ub = []; b_ub = []
    if classwise:
        for b in range(q):
            idx = [c for c, (bb, I) in enumerate(var) if bb == b]
            row = [0.0] * nv
            for c in idx: row[c] = 1.0
            A_eq.append(row); b_eq.append(1.0 / q)
            for i in [i for i in range(k) if i not in deadf(b)]:
                row = [0.0] * nv
                for c in idx: row[c] = (1.0 if i in var[c][1] else 0.0) - 0.5
                A_eq.append(row); b_eq.append(0.0)
    else:
        for i in range(k):
            row = [1.0 / q] * nv
            for c, (bb, I) in enumerate(var):
                if i not in deadf(bb) and i in I: row[c] -= 2.0 / alive_count[i]
            A_ub.append(row); b_ub.append(0.0)
    r = linprog(np.zeros(nv), A_ub=A_ub or None, b_ub=b_ub or None, A_eq=A_eq, b_eq=b_eq,
                bounds=[(0, None)] * nv, method="highs")
    return r.status == 0

if __name__ == "__main__":
    multi = {}
    for primes in ([5, 7], [5, 7, 11], [5, 7, 11, 13]):
        prod = 1.0
        for p in primes: prod *= (1 - 1 / p)
        multi[str(primes)] = {"k=3,m=1 global": lp_multi(3, 1, primes, False),
                              "k=3,m=1 classwise": lp_multi(3, 1, primes, True),
                              "naive bound 2m/prod(1-1/p)": 2 / prod}
    print(json.dumps(multi, indent=1))
    out["multi_prime"] = multi
    json.dump(out, open("code/explore/residue_parity_lp.json", "w"), indent=1)
