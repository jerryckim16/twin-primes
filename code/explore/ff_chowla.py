#!/usr/bin/env python3
"""Exploration (Session 15, function fields): Moebius autocorrelation and twin irreducibles in F_2[T]
(shift H = T^2 + T: the shift 1 is not admissible over F_2, since f(0) = f(1) = 1 forces f + 1 to vanish at 0).
For monic f of degree n over F_2 (encoded as ints, bit i = coefficient of T^i):
  C_h(n) = sum_{deg f = n} mu(f) mu(f + h)   for shifts h = 1, T, T+1,
  P_2^H(n) = #{deg f = n : f and f + H both irreducible}, against S(H) 2^n / n^2 (function-field Hardy-Littlewood shape),
compared with 2^n (trivial size) and with 2^n / n^2 (naive "random" size of P_2).
Heuristic / exploratory only: small degrees, no claim about asymptotics.
usage: ff_chowla.py NMAX"""
import sys
from array import array

def clmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r

def main(NMAX):
    M = 1 << (NMAX + 1)                    # all polys of degree <= NMAX (incl. non-monic is automatic: over F_2 all nonzero are monic)
    mu = array('b', [1]) * M
    irr = bytearray(M)                     # irreducible flag
    composite = bytearray(M)
    for p in range(2, M):
        if composite[p]: continue
        irr[p] = 1
        dp = p.bit_length() - 1
        # mark multiples p*g, deg g >= 0, deg <= NMAX
        for g in range(1, 1 << (NMAX - dp + 1)):
            f = clmul(p, g)
            if g > 1: composite[f] = 1
            mu[f] = -mu[f]
        p2 = clmul(p, p)
        if p2.bit_length() - 1 <= NMAX:
            for g in range(1, 1 << (NMAX - 2 * (dp) + 1)):
                mu[clmul(p2, g)] = 0
    # singular series for the admissible shift H = T^2 + T: S = prod_P (1 - nu_P/|P|)/(1 - 1/|P|)^2,
    # nu_P = 1 if P | H (P = T, T+1, |P| = 2), else 2; product over irreducibles of degree <= NMAX (tail ~ 2^-NMAX)
    S = 1.0
    for p in range(2, M):
        if irr[p]:
            q = float(1 << (p.bit_length() - 1))
            nu = 1 if p in (2, 3) else 2
            S *= (1 - nu / q) / (1 - 1 / q) ** 2
    print("singular series S(T^2+T) ~ %.6f (irreducibles of degree <= %d)" % (S, NMAX))
    H = 6
    print(" n   C_1(n)   C_T(n)  C_{T+1}(n) C_{T^2+T}(n)   2^n   P_2^H(n)  S 2^n/n^2  ratio")
    for n in range(1, NMAX + 1):
        lo, hi = 1 << n, 1 << (n + 1)
        C = {}
        for name, h in (("1", 1), ("T", 2), ("T+1", 3), ("H", 6)):
            if h.bit_length() - 1 >= n: C[name] = None; continue
            C[name] = sum(mu[f] * mu[f ^ h] for f in range(lo, hi))
        P2 = sum(1 for f in range(lo, hi) if irr[f] and irr[f ^ H]) if n >= 3 else None
        pred = S * (1 << n) / n ** 2
        print("%2d %8s %8s %8s %10s %9d %8s %9.1f  %s" % (n, C["1"], C["T"], C["T+1"], C["H"], 1 << n, P2, pred,
              "%.3f" % (P2 / pred) if P2 else "-"), flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 14)
