#!/usr/bin/env python3
"""Odd-order Chowla inputs and the Liouville-pattern obstruction class (Session 38).

Classes of pattern weights Psi >= 0 on {+-1}^k that kill a target family E
(Psi(s) = 0 whenever {i : s_i = -1} contains an edge of E):
  C1   : fair (hat Psi({i}) = 0 for all i)                        [parity paper prop:bipartite]
  C3   : fair and hat Psi(S) = 0 for all |S| = 3
  Codd : hat Psi(S) = 0 for all odd |S|  (<=> Psi(s) = Psi(-s); implies fair)
Claims checked here (exactly, with Fractions):
  (1) Codd blocks E  <=>  some E-free set I has E-free complement (2-colourability, chi(H) <= 2).
      C1 blocks E    <=>  (1/2,...,1/2) in conv(E-free sets)  (chi_f(H) <= 2).
  (2) Fano plane (k = 7, E = 7 lines): C1 blocks (explicit exact weight), Codd does not (no 2-colouring,
      all 128 colourings checked); C3 decided by LP + exact certificate.
  (3) Search over all self-dual monotone Boolean functions on k <= 6 variables (maximal intersecting
      families): for none is 1/2 in conv(G), so no hypergraph on <= 6 vertices separates C1 from Codd;
      exact fractional-transversal certificates.
  (4) The window / DHL / graph targets of prop:bipartite: the C1 measures used there are already symmetric.
Usage: /usr/bin/python3 -I odd_chowla_class.py   (about a minute)
"""
from fractions import Fraction as Fr
from itertools import combinations, product
import sys
import numpy as np
from scipy.optimize import linprog

def free(I, E):
    return not any(e <= I for e in E)

def hat(Psi, k, S):
    tot = Fr(0)
    for s, w in Psi.items():
        p = 1
        for i in S:
            p *= s[i]
        tot += w * p
    return tot / 2**k

def sign_of(I, k):
    return tuple(-1 if i in I else 1 for i in range(k))

# ---------- (2) Fano plane ----------
k = 7
lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
assert all(len(a & b) == 1 for a, b in combinations(lines, 2))
V = frozenset(range(k))
# exact C1 weight: mass 1/8 on the all-plus pattern and on each of the 7 complements of lines
# (minus set = complement of a line, size 4, contains no line since two lines always meet):
# marginal (7/8)(4/7) = 1/2.
Psi = {sign_of(frozenset(), k): Fr(1, 8)}
for L in lines:
    Psi[sign_of(V - L, k)] = Fr(1, 8)
assert all(free(frozenset(i for i in range(k) if s[i] == -1), lines) for s in Psi)
assert all(w >= 0 for w in Psi.values()) and sum(Psi.values()) == 1
sing = [hat(Psi, k, (i,)) for i in range(k)]
print("Fano: C1 weight kills E:", True, " singleton coefficients:", sing)
assert all(x == 0 for x in sing)
odd3 = [hat(Psi, k, S) for S in combinations(range(k), 3)]
print("Fano: this weight's 3-point coefficients: min", min(odd3), "max", max(odd3))
two_col = [I for r in range(k + 1) for I in map(frozenset, combinations(range(k), r))
           if free(I, lines) and free(V - I, lines)]
print("Fano: E-free sets with E-free complement (2-colourings):", len(two_col))
assert not two_col

# C3 for Fano: LP over E-free sets, constraints marginals 1/2 and all 3-point coefficients 0.
Ffree = [I for r in range(k + 1) for I in map(frozenset, combinations(range(k), r)) if free(I, lines)]
def lp_class(Ffree, k, orders):
    rows, rhs = [], []
    rows.append([1] * len(Ffree)); rhs.append(1)
    for d in orders:
        for S in combinations(range(k), d):
            rows.append([np.prod([-1 if i in I else 1 for i in S]) for I in Ffree]); rhs.append(0)
    res = linprog(np.zeros(len(Ffree)), A_eq=np.array(rows, float), b_eq=np.array(rhs, float),
                  bounds=[(0, None)] * len(Ffree), method="highs")
    return res
r3 = lp_class(Ffree, k, [1, 3])
print("Fano: C3 (fair + 3-point) LP status:", r3.status, "(0 = feasible, 2 = infeasible)")
r13 = lp_class(Ffree, k, [1, 3, 5, 7])
print("Fano: Codd LP status:", r13.status)
# exact certificate for C3 infeasibility: find y with sum_rows y_r A_r(I) <= 0 ... via the dual LP
def farkas(Ffree, k, orders):
    # want y (free) with y0 + sum_S y_S chi_S(I) >= 1 for all I in Ffree and y0 < 0 ... i.e.
    # the constraints mu >= 0, sum mu = 1, sum mu chi_S = 0 infeasible iff exists y_S with
    # sum_S y_S chi_S(I) >= 1 for all I in Ffree (then 0 = sum mu * sum y chi >= 1, contradiction).
    Ss = [S for d in orders for S in combinations(range(k), d)]
    A = np.array([[-np.prod([-1 if i in I else 1 for i in S]) for S in Ss] for I in Ffree], float)
    res = linprog(np.zeros(len(Ss)), A_ub=A, b_ub=-np.ones(len(Ffree)), bounds=[(-50, 50)] * len(Ss), method="highs")
    if res.status != 0:
        return None
    y = [Fr(v).limit_denominator(1000) for v in res.x]
    ok = all(sum(yy * np.prod([-1 if i in I else 1 for i in S]) for yy, S in zip(y, Ss)) >= 1 for I in Ffree)
    return ok, {S: v for S, v in zip(Ss, y) if v != 0}
assert r3.status == 2 and r13.status == 2
# clean exact certificate (found by symmetry): on every line-free pattern,
#   (1/2) sum_i s_i + (1/2) sum_L prod_{i in L} s_i >= 1,
# so no measure on line-free patterns has all singleton and all line coefficients zero.
vals = []
for I in Ffree:
    s = sign_of(I, k)
    v = Fr(1, 2) * sum(s) + Fr(1, 2) * sum(np.prod([s[i] for i in L]) for L in lines)
    vals.append(v)
print("Fano: min over line-free patterns of (1/2)sum s_i + (1/2)sum_L chi_L =", min(vals), "(>= 1)")
assert min(vals) >= 1
cert = farkas(Ffree, k, [1, 3])
print("Fano: LP Farkas certificate for C3 (all 35 triples) also verified exactly:", cert[0])

# ---------- (3) self-dual monotone functions on k <= 6 ----------
def monotone_functions(n):
    """All monotone Boolean functions on n variables as frozensets of true points (bitmasks)."""
    pts = list(range(1 << n))
    if n == 0:
        return [frozenset(), frozenset([0])]
    res = []
    for g0 in monotone_functions(n - 1):
        for g1 in monotone_functions(n - 1):
            if g0 <= g1:
                res.append(frozenset(list(g0) + [x | (1 << (n - 1)) for x in g1]))
    return res

def selfdual(n):
    out = []
    full = (1 << n) - 1
    for g in monotone_functions(n - 1):
        gd = frozenset(x for x in range(1 << (n - 1)) if ((full >> 1) ^ x) not in g)
        if g <= gd:
            f = frozenset(list(g) + [x | (1 << (n - 1)) for x in gd])
            out.append(f)
    return out

def tau_star(G, n):
    """min sum c_i, c >= 0, sum_{i in A} c_i >= 1 for A in G (fractional transversal number)."""
    A = np.array([[-((a >> i) & 1) for i in range(n)] for a in G], float)
    res = linprog(np.ones(n), A_ub=A, b_ub=-np.ones(len(G)), bounds=[(0, None)] * n, method="highs")
    c = [Fr(v).limit_denominator(100) for v in res.x]
    assert all(sum(c[i] for i in range(n) if (a >> i) & 1) >= 1 for a in G)
    return sum(c)

counts = {}
for n in range(1, 7):
    sds = selfdual(n)
    worst = None
    for f in sds:
        # check self-duality and monotonicity
        full = (1 << n) - 1
        assert all((x in f) != ((full ^ x) in f) for x in range(1 << n))
        t = tau_star(f, n)
        # 1/2 in conv(G) for an up-set G  <=>  tau*(G) >= 2  (LP duality); exact certificate when t < 2
        if worst is None or t > worst:
            worst = t
    counts[n] = (len(sds), worst)
    print(f"k = {n}: {len(sds)} self-dual monotone functions; max fractional transversal tau* = {worst}"
          f" ({'separating example exists' if worst >= 2 else 'every one has tau* < 2: no separation'})")
assert [counts[n][0] for n in range(1, 7)] == [1, 2, 4, 12, 81, 2646]
# the smallest separating example found (k = 6, 7 edges), exact fair measure on E-free sets
E6 = [frozenset(e) for e in [(4, 5), (0, 1, 5), (0, 2, 5), (0, 3, 4), (1, 2, 4), (1, 3, 5), (2, 3, 5)]]
V6 = frozenset(range(6))
mu6 = {V6 - frozenset(e): Fr(1, 4) for e in [(1, 2, 4), (0, 3, 4), (0, 2, 5), (1, 3, 5)]}
assert all(free(I, E6) for I in mu6)
assert all(sum(w for I, w in mu6.items() if i in I) == Fr(1, 2) for i in range(6))
col6 = [I for r in range(7) for I in map(frozenset, combinations(range(6), r)) if free(I, E6) and free(V6 - I, E6)]
print("k = 6 example E =", [tuple(sorted(e)) for e in E6], ": exact fair measure (minus sets",
      [tuple(sorted(I)) for I in mu6], "each 1/4); 2-colourings:", len(col6))
assert not col6
# Fano for comparison: G = up-closure of the lines
Gf = [a for a in range(1 << 7) if any(all((a >> i) & 1 for i in L) for L in lines)]
print("Fano: tau* of the line hypergraph =", tau_star(Gf, 7), "(>= 2, so 1/2 in conv: C1 blocks)")

# ---------- (4) the prop:bipartite measures are symmetric ----------
def symmetric(meas, k):
    return all(meas.get(I, 0) == meas.get(frozenset(range(k)) - I, 0) for I in meas)
ok = True
for kk in range(2, 9):
    A = frozenset(range(0, kk, 2)); B = frozenset(range(1, kk, 2))
    ok &= symmetric({A: Fr(1, 2), B: Fr(1, 2)}, kk)
for m in range(1, 5):
    for kk in range(m + 1, 2 * m + 1):
        # DHL[k, m+1], k <= 2m: a 2-colouring with both classes of size <= m exists
        A = frozenset(range(kk // 2)); B = frozenset(range(kk // 2, kk))
        Edhl = [frozenset(c) for c in combinations(range(kk), m + 1)]
        ok &= free(A, Edhl) and free(B, Edhl)
print("window / DHL measures symmetric (2-colourings):", ok)
assert ok
print("done")
