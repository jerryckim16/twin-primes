#!/usr/bin/env python3
"""Session 30: which constraint binds in Stadlmann's MPZ region (arXiv:2309.00425v3, Cor. 2, p. 9).

Her proof: MPZ[w,d] holds if 72w+24d<1 and
   max(1/18 + 28w/9 + 2d/9, 1/10) < min(1/4 - 12w - 4d, 1/2 - 32w - 10d)
(Type III from PM8a Thm 2.8(v); sigma > 1/10 from PM8a Lemma 2.7; Type I/II from her Prop. 1).
This script splits the max/min into the four linear inequalities A-D, clears denominators exactly
(Fractions), and checks on a fine rational grid that the region equals C: 80w + 80d/3 < 1, i.e. that
C is the binding constraint (the Type III estimate never binds). It also evaluates the hypothetical
region if PM8a's Remark 3.2 extension (sigma > 1/14, needing Type IV/V estimates nobody has) were available.
Usage: python3 -I code/hm/mpz_region_check.py   (seconds)
"""
from fractions import Fraction as F
A = lambda w, d: F(1, 18) + F(28, 9) * w + F(2, 9) * d < F(1, 4) - 12 * w - 4 * d
B = lambda w, d: F(1, 18) + F(28, 9) * w + F(2, 9) * d < F(1, 2) - 32 * w - 10 * d
C = lambda w, d: F(1, 10) < F(1, 4) - 12 * w - 4 * d
D = lambda w, d: F(1, 10) < F(1, 2) - 32 * w - 10 * d
E = lambda w, d: 72 * w + 24 * d < 1
cor2 = lambda w, d: 80 * w + F(80, 3) * d < 1
N = 400
bad = 0; slackA = []
for i in range(N + 1):
    for j in range(N + 1):
        w, d = F(i, 20 * N), F(j, 10 * N)          # w in [0, 0.05], d in [0, 0.1]
        full = A(w, d) and B(w, d) and C(w, d) and D(w, d) and E(w, d)
        if full != cor2(w, d):
            bad += 1
print("grid points where the full region differs from 80w+80d/3<1:", bad, "of", (N + 1) ** 2)
# exact linear forms
print("A <=> 544w + 152d < 7 ;  B <=> 553w + 161d < 7 ;  C <=> 560w + 560d/3 < 7 ;  D <=> 32w + 10d < 2/5 ; E <=> 504w + 168d < 7")
for (w, d) in [(F(1, 100), F(0)), (F(0), F(1, 30))]:
    assert A(w, d) == (544 * w + 152 * d < 7) and B(w, d) == (553 * w + 161 * d < 7) and C(w, d) == (560 * w + F(560, 3) * d < 7)
# hypothetical sigma > 1/14 (PM8a Remark 3.2; Type IV/V estimates assumed, NOT available)
Ch = lambda w, d: F(1, 14) < F(1, 4) - 12 * w - 4 * d
print("delta -> 0 limit of varpi:  Cor. 2: 1/80 =", float(F(1, 80)), "; with sigma > 1/14 (hypothetical): A binds, 7/544 =", float(F(7, 544)),
      "; C' gives", float(F(5, 336)))
