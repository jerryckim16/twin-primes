#!/usr/bin/env python3
"""Exact pointwise check of code/songyue_convert.py: at random rational points t in R^48 compare the
witness P_U(t) (evaluated from the monomial table directly) with the converted u-format polynomial
(divided by its scale) at u = 4t.  usage: python3 code/songyue_pointcheck.py [npts]"""
import json, random, sys, itertools
from fractions import Fraction as Fr
from collections import Counter
from math import factorial
w = json.load(open("code/cap6/songyue236_witness.json"))
d = json.load(open("code/cap6/P_sy236_u.json"))
K, U, L = 48, Fr(521, 2000), Fr(521, 500)

def m_alpha(al, z):
    # elementary-style DP: sum over distinct-index assignments / |Aut|  (via DP over coordinates)
    # coefficient of prod y_v^{mult_v} in prod_i (1 + sum_v y_v z_i^v), v = distinct parts
    cnt = Counter(al); vals = sorted(cnt); target = tuple(cnt[v] for v in vals)
    dp = {tuple(0 for _ in vals): Fr(1)}
    for zi in z:
        nd = dict(dp)
        for st, c in dp.items():
            for n, v in enumerate(vals):
                if st[n] < target[n]:
                    s2 = list(st); s2[n] += 1; s2 = tuple(s2)
                    nd[s2] = nd.get(s2, 0) + c * zi ** v
        dp = nd
    return dp.get(target, Fr(0))

random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
npts = int(sys.argv[1]) if len(sys.argv) > 1 else 2
for _ in range(npts):
    t = [Fr(random.randint(0, 60), 10000) for _ in range(K)]
    z = [Fr(26) * x / (25 * U) for x in t]
    sz = sum(z)
    lhs = sum(int(c) * (Fr(26, 25) - sz) ** a * m_alpha(al, z) for _, a, al, c in w["rows"])
    u = [4 * x for x in t]
    P = {j: sum(x ** j for x in u) for j in range(2, 26)}
    rhs = Fr(0)
    for (a, b), c in zip(d["basis"], d["coeffs"]):
        term = Fr(int(c)) * (L - sum(u)) ** a
        for jj, e in enumerate(b):
            if e: term *= P[jj + 2] ** e
        rhs += term
    rhs /= int(d["scale"])
    print("point check:", lhs == rhs, float(lhs))
    assert lhs == rhs
