#!/usr/bin/env python3
r"""songyue_I0.py -- exact CAP-FREE mass I0 of Song-Yue's 236 witness, computed directly in their
monomial basis (independent of code/songyue_convert.py and of the power-sum evaluators).

I0 = int_{t >= 0, s(t) < U} P_U(t)^2 dt,  P_U(t) = P(26 t/(25 U)),  P(z) = sum c (Lam - s(z))^a m_alpha(z),
Lam = 26/25, k = 48.  Substituting z: I0 = (25U/26)^k int_{s(z) < Lam} P(z)^2 dz, and
    int_{x >= 0, s(x) < Lam} (Lam - s)^A x^gamma dx = A! prod gamma_i! Lam^{k+A+|gamma|} / (k+A+|gamma|)!.
For m_alpha m_beta (injective index maps f, g; |Aut| corrections), group the pairs (f, g) by the partial
matching M = {(i, j): f(i) = g(j)}:  there are (k)_{l_a + l_b - |M|} of them, each contributing
prod_{(i,j) in M} (alpha_i + beta_j)! prod_{unmatched} alpha_i! beta_j!.  Hence
    S(alpha, beta) = prod alpha! prod beta! / (|Aut alpha| |Aut beta|)
                     * sum_M (k)_{l_a + l_b - |M|} prod_{(i,j) in M} C(alpha_i + beta_j, alpha_i),
and the matching sums are computed by a DP over the parts of alpha with a bitmask over beta.
Also prints the normalisation against the paper's Iref = (98!)^2 I0,* (Appendix C).

usage: python3 code/songyue_I0.py [--out code/cap6/I0_sy236.json]
"""
import sys, json, time
from fractions import Fraction as Fr
from math import factorial, comb
from collections import Counter, defaultdict
from functools import lru_cache

K = 48
U = Fr(521, 2000)
LAM = Fr(26, 25)


def ff(n, r):
    out = 1
    for i in range(r):
        out *= n - i
    return out


@lru_cache(maxsize=None)
def S(alpha, beta):
    """int-free combinatorial factor: sum over monomials x^gamma of m_alpha m_beta of prod gamma_i!"""
    if len(alpha) < len(beta):
        alpha, beta = beta, alpha
    lb = len(beta)
    # dp[mask] = sum over matchings of processed alpha parts into beta-set `mask` of prod weights
    dp = {0: 1}
    for ai in alpha:
        nd = defaultdict(int)
        for mask, v in dp.items():
            nd[mask] += v  # ai unmatched
            for jj in range(lb):
                if not mask >> jj & 1:
                    nd[mask | 1 << jj] += v * comb(ai + beta[jj], ai)
        dp = nd
    byj = defaultdict(int)
    for mask, v in dp.items():
        byj[bin(mask).count("1")] += v
    la = len(alpha)
    tot = sum(ff(K, la + lb - j) * v for j, v in byj.items())
    pre = 1
    for x in alpha + beta:
        pre *= factorial(x)
    aut = 1
    for v in list(Counter(alpha).values()) + list(Counter(beta).values()):
        aut *= factorial(v)
    return Fr(pre * tot, aut)


def selftest():
    # brute force in a small number of variables against direct expansion
    global K
    import itertools
    K0 = K
    K = 4
    S.cache_clear()
    for alpha, beta in [((2,), (2,)), ((2, 2), (4,)), ((2, 4), (2, 2)), ((2, 2, 2), (2, 4))]:
        def monos(al):
            out = set()
            for idx in itertools.permutations(range(K), len(al)):
                e = [0] * K
                for i, a in zip(idx, al):
                    e[i] = a
                out.add(tuple(e))
            return out
        tot = 0
        for e1 in monos(alpha):
            for e2 in monos(beta):
                p = 1
                for x, y in zip(e1, e2):
                    p *= factorial(x + y)
                tot += p
        assert S(tuple(alpha), tuple(beta)) == tot, (alpha, beta)
    K = K0
    S.cache_clear()
    print("selftest S(alpha,beta): ok")


def main():
    selftest()
    w = json.load(open("code/cap6/songyue236_witness.json"))
    rows = [(a, tuple(al), int(c)) for _, a, al, c in w["rows"]]
    t0 = time.time()
    # group: sum_{i,j} c_i c_j A! Lam^{K+A+n} / (K+A+n)! S(alpha_i, alpha_j), A = a_i + a_j, n = |alpha_i|+|alpha_j|
    by = defaultdict(lambda: defaultdict(int))
    for a, al, c in rows:
        by[al][a] += c
    als = sorted(by)
    tot = Fr(0)
    for x, al in enumerate(als):
        for be in als[x:]:
            sab = S(al, be)
            n = sum(al) + sum(be)
            part = Fr(0)
            for a1, c1 in by[al].items():
                for a2, c2 in by[be].items():
                    A = a1 + a2
                    part += Fr(c1 * c2 * factorial(A) * (LAM ** (K + A + n)).numerator,
                               factorial(K + A + n) * (LAM ** (K + A + n)).denominator)
            tot += (1 if al == be else 2) * sab * part
    I0 = (25 * U / 26) ** K * tot
    print("I0 = %.15e  (%d alpha signatures, %.1f s)" % (float(I0), len(als), time.time() - t0))
    appc = json.load(open("code/cap6/songyue236_appC.json"))
    Iref = int(appc["Iref"])
    r = Fr(Iref) / I0
    print("Iref / I0 has", len(str(r)), "chars")
    out = dict(I0=str(I0), I0_float=float(I0), Iref_over_I0=str(r))
    if "--out" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)


if __name__ == "__main__":
    main()
