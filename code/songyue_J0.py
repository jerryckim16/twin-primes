#!/usr/bin/env python3
r"""songyue_J0.py -- exact CAP-FREE numerator J0 of Song-Yue's 236 witness in their monomial basis
(independent of the power-sum evaluators).  Same conventions as code/songyue_I0.py.

J0 = int_{t' in R^47, s(t') <= Lt} ( int_0^{U - s(t')} P_U(t', t_k) dt_k )^2 dt',  Lt = 491/2000, U = 521/2000.
In z = 26 t/(25U): factor (25U/26)^{47+2}; base s(z') <= c = 26 Lt/(25 U); fibre [0, H], H = Lam - s(z').
m_alpha(z', t) = m_alpha(z') + sum_{distinct v in alpha} m_{alpha - v}(z') t^v, and
int_0^H (H - t)^a t^v dt = a! v!/(a+v+1)! H^{a+v+1}.  So G = sum g_{e,beta} H^e m_beta(z') and
int_{s' <= c} H^A z'^gamma = sum_i C(A,i) d^{A-i} i! prod gamma! c^{47+i+|gamma|}/(47+i+|gamma|)!, d = Lam - c.
Uses S(alpha, beta) of songyue_I0.py with K = 47.

usage: python3 code/songyue_J0.py [--out code/cap6/J0_sy236.json]
"""
import sys, json, time
from fractions import Fraction as Fr
from math import factorial, comb
from collections import defaultdict
sys.path.insert(0, "code")
import songyue_I0 as m

m.K = 47
U, Lt, LAM = Fr(521, 2000), Fr(491, 2000), Fr(26, 25)
c = 26 * Lt / (25 * U)
d = LAM - c


def main():
    w = json.load(open("code/cap6/songyue236_witness.json"))
    t0 = time.time()
    G = defaultdict(lambda: defaultdict(Fr))  # beta -> e -> coeff
    for _, a, al, cc in w["rows"]:
        cc = int(cc)
        al = tuple(al)
        G[al][a + 1] += Fr(cc, a + 1)
        for v in sorted(set(al)):
            l = list(al); l.remove(v); be = tuple(l)
            G[be][a + v + 1] += Fr(cc * factorial(a) * factorial(v), factorial(a + v + 1))
    bes = sorted(G)
    print("G: %d signatures, %d terms" % (len(bes), sum(len(x) for x in G.values())))
    # base integrals: B(A, n) = sum_i C(A,i) d^{A-i} i! c^{47+i+n}/(47+i+n)!
    memo = {}

    def B(A, n):
        if (A, n) not in memo:
            memo[(A, n)] = sum(comb(A, i) * d ** (A - i) * factorial(i) * c ** (47 + i + n) / factorial(47 + i + n)
                               for i in range(A + 1))
        return memo[(A, n)]

    tot = Fr(0)
    for x, b1 in enumerate(bes):
        for b2 in bes[x:]:
            n = sum(b1) + sum(b2)
            part = Fr(0)
            for e1, g1 in G[b1].items():
                for e2, g2 in G[b2].items():
                    part += g1 * g2 * B(e1 + e2, n)
            tot += (1 if b1 == b2 else 2) * m.S(b1, b2) * part
        if x % 100 == 0:
            print("  %d/%d  %.0f s" % (x, len(bes), time.time() - t0), flush=True)
    J0 = (25 * U / 26) ** 49 * tot
    I0 = Fr(json.load(open("code/cap6/I0_sy236.json"))["I0"])
    r = 48 * J0 / I0
    print("J0 = %.15e ; 48 J0/I0 = %.12f (Stadlmann scaling) = %.10f x4 (Polymath scaling); %.0f s"
          % (float(J0), float(r), 4 * float(r), time.time() - t0))
    if "--out" in sys.argv:
        json.dump(dict(J0=str(J0), J0_float=float(J0), ratio_stadlmann=str(r), ratio_stadlmann_float=float(r),
                       ratio_polymath_float=4 * float(r)),
                  open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)


if __name__ == "__main__":
    main()
