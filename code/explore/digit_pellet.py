#!/usr/bin/env python3
"""Exploration (Session 41): is there a "Pellet formula over Z" through base-p digit polynomials?

For n = sum d_i p^i (base p digits) let F_n(x) = sum d_i x^i in F_p[x] (the carry-free image of n).
Pellet's formula makes mu_{F_p[x]}(F_n) = (-1)^{deg} chi_p(disc F_n) an algebraic (trace-function-like)
quantity. Question: does the integer parity lambda(n) correlate with mu_p(F_n) (or with the
irreducibility of the integer digit polynomial over Q, cf. Cohn's criterion)? A visible correlation would
point at an algebraic proxy for lambda; none is expected (carries).

Usage: /usr/bin/python3 -I code/explore/digit_pellet.py [p] [k]   (n < p^k; default p = 3, k = 12)
Heuristic / exploratory; output in code/explore/digit_pellet.out.
"""
import sys
import numpy as np
from flint import nmod_poly, fmpz_poly


def liouville_upto(N):
    rem = np.arange(N, dtype=np.int64)
    Om = np.zeros(N, dtype=np.int16)
    isp = np.ones(N, dtype=bool); isp[:2] = False
    for q in range(2, int(N ** 0.5) + 1):
        if isp[q]:
            isp[q * q::q] = False
    for q in np.nonzero(isp[: int(N ** 0.5) + 1])[0]:
        qk = int(q)
        while qk < N:
            rem[qk::qk] //= q
            Om[qk::qk] += 1
            qk *= int(q)
    Om += (rem > 1)
    lam = np.where(Om % 2 == 0, 1, -1).astype(np.int64)
    lam[0] = 0
    return lam, isp


def digits(n, p):
    d = []
    while n:
        d.append(n % p); n //= p
    return d


def mu_poly(F):
    if F.degree() < 1:
        return 0
    fac = F.factor()[1]
    if any(e > 1 for _, e in fac):
        return 0
    return (-1) ** len(fac)


def main():
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    N = p ** k
    lam, isp = liouville_upto(N + 3)
    mup = np.zeros(N + 3, dtype=np.int64)
    irrQ_prime = [0, 0]   # [primes n with F_n irreducible over Q, primes n tested]
    irrQ_comp = [0, 0]
    for n in range(p, N + 3):
        d = digits(n, p)
        mup[n] = mu_poly(nmod_poly(d, p))
        if n < 200000 and n % 7 == 0 or (n < 200000 and isp[n]):
            G = fmpz_poly(d)
            irr = len(G.factor()[1]) == 1 and G.factor()[1][0][1] == 1
            if isp[n]:
                irrQ_prime[0] += irr; irrQ_prime[1] += 1
            else:
                irrQ_comp[0] += irr; irrQ_comp[1] += 1
    sl = slice(p, N)
    nz = mup[sl] != 0
    cnt = int(nz.sum())
    c1 = float((lam[sl] * mup[sl]).sum()) / cnt
    pair = (mup[p:N] != 0) & (mup[p + 2:N + 2] != 0)
    a = lam[p:N] * lam[p + 2:N + 2]
    b = mup[p:N] * mup[p + 2:N + 2]
    c2 = float((a * b)[pair].sum()) / int(pair.sum())
    # primes: does mu_p(F_n) = -1 (F_n irreducible-or-odd) more often for prime n?
    pr = isp[p:N] & nz
    mean_mu_primes = float(mup[p:N][pr].sum()) / int(pr.sum())
    mean_mu_all = float(mup[sl][nz].sum()) / cnt
    print(f"p = {p}, n < p^{k} = {N}; n with F_n squarefree mod p: {cnt}")
    print(f"mean lambda(n) mu_p(F_n)                       = {c1:+.5f}   (1/sqrt(count) = {cnt ** -0.5:.5f})")
    print(f"mean lambda(n)lambda(n+2) mu_p(F_n)mu_p(F_n+2) = {c2:+.5f}   over {int(pair.sum())} n")
    print(f"mean mu_p(F_n) over all n: {mean_mu_all:+.5f};  over primes n: {mean_mu_primes:+.5f}  ({int(pr.sum())} primes)")
    print(f"F_n irreducible over Q: primes n {irrQ_prime[0]}/{irrQ_prime[1]} (Cohn: all, for p <= 10 digits >= 0), "
          f"composite n (n = 0 mod 7 sample, n < 2e5) {irrQ_comp[0]}/{irrQ_comp[1]}")


if __name__ == "__main__":
    main()
