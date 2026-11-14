#!/usr/bin/env python3
"""Session 15: certify M_{50,1/25} < 4.1459 with the two-zone weight of Theorem thm:floor (code/dual_eps_cert.py,
certify_box: arb ball arithmetic, bisection in sigma). Parameters chosen in floating point, then rounded to rationals:
a = 519347/500000, s1 = 244591/250000 (tau < s1 <= a, s1 <= L).  usage: python3 code/twozone_50_cert.py"""
import sys
sys.path.insert(0, "code")
from fractions import Fraction as Fr
import dual_eps_cert as D
k, L, tau = 50, Fr(26, 25), Fr(24, 25)
a, s1 = Fr(519347, 500000), Fr(244591, 250000)
assert tau < s1 <= L and a >= s1
for t in (Fr(41459, 10000), Fr(41458, 10000)):
    n = D.certify_box(k, L, tau, a, s1, t)
    print("target %s: %s" % (float(t), "CERTIFIED with %d pieces" % n if n else "not certified"))
