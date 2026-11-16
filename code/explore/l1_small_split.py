#!/usr/bin/env python3
"""Exploration (Heuristic): for primes q = 3 mod 4, q <= QMAX, compare L(1, chi_{-q}) = pi h(-q)/sqrt(q)
(class number from h = -(1/q) sum_{a<q} a chi(a), valid for q = 3 mod 4, q > 3) with the reciprocal sum of
small split primes s'(q) = sum_{w < p <= q^{1/4}, chi(p) = +1} 1/p (w = 3).
Question (first unresolved implication of the 16 Nov route card, in the actual world only): do small
values of L(1, chi) come with s' < 1/4?  Usage: /usr/bin/python3 -I l1_small_split.py [QMAX]"""
import sys, math
import numpy as np

QMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
s = np.ones(QMAX + 1, bool); s[:2] = False
for i in range(2, int(QMAX ** .5) + 1):
    if s[i]: s[i*i::i] = False
P = np.nonzero(s)[0]
rows = []
for q in P[(P % 4 == 3) & (P > 3)].tolist():
    a = np.arange(1, q, dtype=np.int64)
    chi = -np.ones(q, np.int64); chi[(a * a) % q] = 1; chi[0] = 0
    h = -int(np.sum(a * chi[1:])) // q
    L1 = math.pi * h / math.sqrt(q)
    y = q ** 0.25
    sp = P[(P > 3) & (P <= y)]
    sprime = float(np.sum([1.0 / p for p in sp.tolist() if chi[p % q] == 1]))
    rows.append((q, h, L1, sprime))
rows = np.array(rows)
L1 = rows[:, 2]; sp = rows[:, 3]
print(f"primes q = 3 mod 4 up to {QMAX}: {len(rows)}")
print(f"corr(log L1, s') = {np.corrcoef(np.log(L1), sp)[0,1]:+.3f}")
for qt in [0.01, 0.05, 0.25, 0.5, 1.0]:
    cut = np.quantile(L1, qt)
    sel = L1 <= cut
    print(f"bottom {qt*100:5.1f}% of L(1) (<= {cut:.3f}): n={sel.sum():5d}  mean s'={sp[sel].mean():.3f}  "
          f"frac s'>=1/4: {np.mean(sp[sel] >= 0.25):.3f}")
idx = np.argsort(L1)[:12]
print("smallest L(1):", [(int(rows[i,0]), int(rows[i,1]), round(rows[i,2], 3), round(rows[i,3], 3)) for i in idx])
