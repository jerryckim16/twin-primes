#!/usr/bin/env python3
"""Exploration (Session 38): 3-term progressions as targets in the Liouville-pattern class.
Positions 0..n-1 of the tuple {n + i*d} (d = 210 makes n <= 10 admissible); target: some
three positions i < j < l in arithmetic progression are all prime. Hypergraph H_n = 3-APs of [n].
Fair class (C1) blocks  <=>  chi_f(H_n) <= 2  <=>  (1/2,...,1/2) in conv(3-AP-free sets).
Odd-order class (Codd) blocks <=> H_n 2-colourable  <=> n <= 8 (van der Waerden W(3;2) = 9).
Usage: /usr/bin/python3 -I ap3_targets_classes.py [NMAX]   (NMAX <= 20; seconds)
"""
import sys
from itertools import combinations
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16

def admissible(H):
    for p in range(2, len(H) + 2):
        if all(q for q in [p % r for r in range(2, int(p ** .5) + 1)]) and len({h % p for h in H}) == p:
            return False
    return True

for n in range(3, NMAX + 1):
    aps = [(i, j, 2 * j - i) for i in range(n) for j in range(i + 1, n) if 2 * j - i < n]
    masks = [(1 << a) | (1 << b) | (1 << c) for a, b, c in aps]
    free = [m for m in range(1 << n) if all(m & e != e for e in masks)]
    two_col = any(((~m) & ((1 << n) - 1)) in set(free) for m in free) if n <= 20 else None
    # C1: maximise t s.t. a distribution on free sets has all marginals >= t; blocked iff t* >= 1/2
    A = np.array([[(m >> i) & 1 for m in free] for i in range(n)], float)
    # variables: mu (len free), t ; maximise t: A mu >= t, sum mu = 1
    c = np.zeros(len(free) + 1); c[-1] = -1
    Aub = np.hstack([-A, np.ones((n, 1))])
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(n), A_eq=np.hstack([np.ones((1, len(free))), [[0]]]), b_eq=[1],
                  bounds=[(0, None)] * len(free) + [(0, 1)], method="highs")
    t = -res.fun
    r3 = max(bin(m).count("1") for m in free)
    H = [210 * i for i in range(n)]
    print(f"n = {n:2d}: r3 = {r3}, max min-marginal t* = {t:.6f} (C1 blocks: {t >= 0.5 - 1e-9}), "
          f"2-colourable (Codd blocks): {two_col}, tuple 210*i admissible: {admissible(H)}")

# exact check at n = 9: a distribution on 3-AP-free subsets of [9] with all marginals exactly 1/2
n = 9
aps = [(i, j, 2 * j - i) for i in range(n) for j in range(i + 1, n) if 2 * j - i < n]
masks = [(1 << a) | (1 << b) | (1 << c) for a, b, c in aps]
free = [m for m in range(1 << n) if all(m & e != e for e in masks)]
A = np.array([[(m >> i) & 1 for m in free] for i in range(n)], float)
res = linprog(np.zeros(len(free)), A_eq=np.vstack([A, np.ones(len(free))]), b_eq=[0.5] * n + [1],
              bounds=[(0, None)] * len(free), method="highs-ds")
mu = {m: Fr(v).limit_denominator(100) for m, v in zip(free, res.x) if v > 1e-12}
ok = sum(mu.values()) == 1 and all(sum(w for m, w in mu.items() if (m >> i) & 1) == Fr(1, 2) for i in range(n))
print("n = 9 exact fair measure on 3-AP-free sets verified:", ok)
for m, w in mu.items():
    print("   ", [i for i in range(n) if (m >> i) & 1], w)
# exact: no 2-colouring of [9] avoids monochromatic 3-APs
full = (1 << n) - 1
print("n = 9: 2-colourings without monochromatic 3-AP:", sum(1 for m in free if (full ^ m) in set(free)))
