#!/usr/bin/env python3
"""Convert an mk_general eps-simplex certificate (coordinates t, support 1+e, marginal 1-e) into
Stadlmann's Polymath-scaled coordinates u = s t (support L, marginal tau, s = (L+tau)/2).
(L0 - P1(t))^a prod P_j(t)^{b_j} = s^{-(a+w(b))} (L - P1(u))^a prod P_j(u)^{b_j}, so c'_i = c_i s^{-(a_i+w(b_i))}.
Output format (read by code/capped_exact.py and code/capped_check.py):
  k, L, tau, g, caps {"1": C_1, "2": C_2, "3+": C_m for m >= 3}, basis [[a, [b_2, b_3, ..., b_W]]], coeffs [p/q strings]
  P(u) = sum_i coeffs_i (L - u_1 - ... - u_k)^{a_i} prod_{j>=2} (u_1^j + ... + u_k^j)^{b_i[j-2]}.
usage: to_ucoords.py cert_in.json out.json
"""
import sys, json
from fractions import Fraction as Fr
c = json.load(open(sys.argv[1]))
L, tau, g = Fr(1042, 1000), Fr(982, 1000), Fr(112, 1000)
s = (L + tau) / 2
assert Fr(c["eps"]) == (L - tau) / (L + tau)
w = lambda b: sum((j + 2) * x for j, x in enumerate(b))
co = [Fr(x) * s ** (-(a + w(b))) for (a, b), x in zip(c["basis"], c["coeffs"])]
json.dump(dict(k=c["k"], L=str(L), tau=str(tau), g=str(g), caps={"1": "3/5", "2": "3/5", "3+": "17/25"},
               basis=c["basis"], coeffs=[str(x) for x in co], source=sys.argv[1]), open(sys.argv[2], "w"))
print("wrote", sys.argv[2], len(co), "terms")
