#!/usr/bin/env python3
r"""songyue_convert.py -- convert Song-Yue's 236 witness (IACR ePrint 2026/1893, Appendix A) into the
u-format read by code/capped_check.py and code/capped_exact.py.

Witness: P(z) = sum_rows c (26/25 - s(z))^a m_alpha(z), z = 26 t/(25 U), U = 521/2000, k = 48.
Polymath coordinates u = 4 t (support L = 4U = 521/500): z = (520/521) u and
26/25 - s(z) = (520/521) (L - P1(u)).  Hence, as functions,
    P_U(t) = sum c (520/521)^{a+|alpha|} (L - P1(u))^a m_alpha(u).
Monomial symmetric functions -> power sums (exact, any number of variables >= length):
    augmented monomials  A_beta = sum over injective index maps of x^beta = |Aut beta| m_beta  satisfy
    p_r A_beta = A_(beta, r) + sum_i A_(beta with beta_i + r),
so  A_(beta,r) = p_r A_beta - sum_i A_(beta_i + r)  (memoised recursion over sorted tuples).
All alpha parts are even in the witness, so only P_2, P_4, ... occur.

usage: python3 code/songyue_convert.py code/cap6/songyue236_witness.json code/cap6/P_sy236_u.json
"""
import sys, json
from fractions import Fraction as Fr
from functools import lru_cache
from math import factorial
from collections import Counter, defaultdict


@lru_cache(maxsize=None)
def aug(beta):
    """augmented monomial A_beta (beta sorted tuple) as dict {sorted tuple of power-sum parts: Fraction}"""
    if not beta:
        return {(): Fr(1)}
    r, rest = beta[-1], beta[:-1]
    out = defaultdict(Fr)
    for lam, c in aug(rest).items():
        out[tuple(sorted(lam + (r,)))] += c
    for i in range(len(rest)):
        b2 = tuple(sorted(rest[:i] + (rest[i] + r,) + rest[i + 1:]))
        for lam, c in aug(b2).items():
            out[lam] -= c
    return {l: c for l, c in out.items() if c}


def mono(alpha):
    aut = 1
    for v in Counter(alpha).values():
        aut *= factorial(v)
    return {l: c / aut for l, c in aug(tuple(sorted(alpha))).items()}


def selftest():
    # numerical check in n = 7 variables at a random rational point
    import random, itertools
    random.seed(1)
    x = [Fr(random.randint(1, 9), random.randint(1, 9)) for _ in range(7)]
    p = lambda j: sum(xi ** j for xi in x)
    for alpha in [(2,), (2, 2), (2, 4), (2, 2, 2), (2, 2, 4, 6), (4, 4, 4, 2, 2)]:
        lhs = Fr(0)
        for idx in itertools.permutations(range(7), len(alpha)):
            t = Fr(1)
            for i, a in zip(idx, alpha):
                t *= x[i] ** a
            lhs += t
        aut = 1
        for v in Counter(alpha).values():
            aut *= factorial(v)
        lhs /= aut
        rhs = Fr(0)
        for lam, c in mono(alpha).items():
            t = c
            for j in lam:
                t *= p(j)
            rhs += t
        assert lhs == rhs, alpha
    print("selftest m_alpha -> power sums: ok")


def main():
    selftest()
    w = json.load(open(sys.argv[1]))
    L = Fr(521, 500)
    s = Fr(520, 521)
    acc = defaultdict(Fr)
    for row, a, alpha, c in w["rows"]:
        base = Fr(int(c)) * s ** (a + sum(alpha))
        for lam, cl in mono(tuple(alpha)).items():
            assert all(j % 2 == 0 for j in lam)
            acc[(a, lam)] += base * cl
    W = max(max(lam, default=2) for (a, lam) in acc)
    from math import lcm
    D = 1
    for c in acc.values():
        D = lcm(D, c.denominator)
    basis, coeffs = [], []
    for (a, lam), c in sorted(acc.items(), key=lambda kv: (kv[0][0] + sum(kv[0][1]), kv[0])):
        if not c:
            continue
        b = [0] * (W - 1)
        for j in lam:
            b[j - 2] += 1
        basis.append([a, b])
        coeffs.append(str(c * D))   # integer: P_file = D * P_U
    deg = max(a + sum((j + 2) * e for j, e in enumerate(b)) for a, b in basis)
    out = dict(k=48, L="521/500", tau="491/500", g="91/1250",
               caps={"1": "1899/2500", "2": "1899/2500", "3+": "1899/2500"},
               basis=basis, coeffs=coeffs, scale=str(D),
               source="Song-Yue ePrint 2026/1893 App. A witness (code/cap6/songyue236_witness.json), "
                      "converted exactly by code/songyue_convert.py (u = 4t, m_alpha -> power sums); "
                      "the file's polynomial is scale * P_U, so I and J carry a factor scale^2")
    json.dump(out, open(sys.argv[2], "w"))
    print("wrote", sys.argv[2], len(basis), "terms, degree", deg, "max part", W, "scale", D)


if __name__ == "__main__":
    main()
