#!/usr/bin/env python3
"""Exact checks for route card notes/parity-attempts/2026-11-18-e2-odd-cycles.md (second program; no LP trusted).

Model (as in the E2 card, sec. E(ii)): forms L_i(m) = a_i m + b_i; an edge (i, c; j, c'; s) is the identity
c L_i + s d = c' L_j with c, c' in {1} u primes; its event (L = E2 if multiplier 1, L = prime != c otherwise)
makes x = c L_i(m) and x + s d both E2.  In lambda-coordinates the edge requires the sign pair
(sigma_i, sigma_j), sigma = +1 for multiplier 1 (E2) and -1 for a prime multiplier.
A target (union of edge events) is BLOCKED by fair non-negative lambda-pattern weights iff (1/2,...,1/2) lies in the
convex hull of the target-free sign patterns (indicator of the -1 positions) [parity paper, sec. bip].

1. Template T(d) for 4 | d, 3 nmid d: forms m, m+d/2, 3m+d, 3m+2d, 3m+5d/2, five edges forming a 5-cycle.
   Checked: the five identities, gcd(a,b) = 1, admissibility (all primes p <= 5; p > 5 is automatic for 5 forms
   with gcd(a,b) = 1), for every such d <= 1200.  Unblocked: exact Farkas vector c with c.1_S <= c0 for all
   target-free S and c.(1/2,...,1/2) > c0.
2. Triangle (E2 card, 12 | d): m, m+d/2, m+d; exact Farkas certificate.
3. Bipartite case: for each signed graph that is bipartite with cycle-sign product +1, the explicit pattern
   eps (eps_i eps_j = -sigma_i sigma_j on every edge) and -eps are target-free, so (1/2,...) is their midpoint.
   Checked on random instances.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd
import random

def target_free(n, edges):
    """edges: list of (i, j, si, sj) required signs. Returns list of patterns (tuples of +-1) avoiding all edges."""
    out = []
    for eps in product((1, -1), repeat=n):
        if all(not (eps[i] == si and eps[j] == sj) for (i, j, si, sj) in edges):
            out.append(eps)
    return out

def farkas_unblocked(n, edges, c):
    """Exact check: c . 1_{eps=-1} <= c0 := max over target-free, and c . (1/2,...) > c0."""
    tf = target_free(n, edges)
    c0 = max(sum(c[i] for i in range(n) if eps[i] == -1) for eps in tf)
    mid = F(sum(c), 2)
    return mid > c0, c0, mid

def find_farkas(n, edges, rng=range(-3, 4)):
    for c in product(rng, repeat=n):
        ok, c0, mid = farkas_unblocked(n, edges, c)
        if ok:
            return c, c0, mid
    return None

def admissible(forms):
    if any(gcd(a, b) != 1 for a, b in forms):
        return False
    for p in [q for q in range(2, len(forms) + 1) if all(q % r for r in range(2, q))]:
        if all(any((a * m + b) % p == 0 for a, b in forms) for m in range(p)):
            return False
    return True

def check_identity(forms, i, c, j, c2, s, d):
    (a, b), (a2, b2) = forms[i], forms[j]
    return c * a == c2 * a2 and c * b + s * d == c2 * b2

sig = lambda c: 1 if c == 1 else -1

print("1. Template T(d), d = 4t, 3 nmid d")
def template(d):
    h = d // 2
    forms = [(1, 0), (1, h), (3, d), (3, 2 * d), (3, 5 * h)]
    # (i, c, j, c', s): c L_i + s d = c' L_j
    E = [(0, 3, 2, 1, 1), (2, 1, 3, 1, 1), (0, 2, 1, 2, 1), (1, 3, 4, 1, 1), (4, 2, 3, 2, -1)]
    return forms, E
bad = 0; count = 0
for d in range(4, 1201, 4):
    if d % 3 == 0:
        continue
    forms, E = template(d)
    count += 1
    if not all(check_identity(forms, *e, d) for e in E) or not admissible(forms):
        bad += 1; print("  FAIL at d =", d)
print(f"  identities + admissibility checked for {count} values of d <= 1200: {bad} failures")
forms, E = template(4)
edges = [(i, j, sig(c), sig(c2)) for (i, c, j, c2, s) in E]
print("  d = 4 forms:", ["%dm+%d" % f for f in forms])
print("  signed edges (i, j, sigma_i, sigma_j):", edges)
prodsign = 1
for (i, j, si, sj) in edges:
    prodsign *= si * sj
print("  cycle sign product:", prodsign, "; target-free patterns:", len(target_free(5, edges)), "of 32")
cert = find_farkas(5, edges)
print("  Farkas certificate (c, c0, c.(1/2..)):", cert, "-> UNBLOCKED" if cert else "-> no certificate in box (blocked?)")
# independent cross-check: LP feasibility of the midpoint by exhaustive rational search is not needed; verify that
# no pair {eps, -eps} of target-free patterns exists (the easy blocking certificate fails)
tf = set(target_free(5, edges))
print("  antipodal target-free pairs:", sum(1 for e in tf if tuple(-x for x in e) in tf) // 2)

print("2. Triangle, 12 | d: m, m+d/2, m+d")
for d in (12, 24, 36):
    h = d // 2
    forms = [(1, 0), (1, h), (1, d)]
    E = [(0, 2, 1, 2, 1), (1, 2, 2, 2, 1), (0, 1, 2, 1, 1)]
    assert all(check_identity(forms, *e, d) for e in E) and admissible(forms)
edges3 = [(0, 1, -1, -1), (1, 2, -1, -1), (0, 2, 1, 1)]
print("  identities/admissibility ok for d = 12, 24, 36; Farkas:", find_farkas(3, edges3))

print("3. Bipartite signed graphs with cycle product +1 are blocked (antipodal pair), random check")
random.seed(1)
ok = 0
for trial in range(2000):
    n = random.randint(2, 7)
    col = [random.randint(0, 1) for _ in range(n)]
    tau = [random.choice((1, -1)) for _ in range(n)]       # gauge: sigma_i^e sigma_j^e = tau_i tau_j on each edge
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if col[i] != col[j] and random.random() < 0.6:
                si = random.choice((1, -1)); sj = si * tau[i] * tau[j]
                edges.append((i, j, si, sj))
    # explicit eps: eps_i = tau_i * (-1)^{col_i}
    eps = tuple(tau[i] * (-1) ** col[i] for i in range(n))
    tf = set(target_free(n, edges))
    assert eps in tf and tuple(-x for x in eps) in tf
    ok += 1
print(f"  {ok} random bipartite signed graphs: eps and -eps target-free in all")
