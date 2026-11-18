#!/usr/bin/env python3
"""Exploration (Heuristic): the ultrametric window identity in F_q[T] and Keating-Rudnick's variance.

For monic f of degree n with f(0) != 0, Lambda'(f) = deg P if f = P^k (P irreducible), else 0.
Short intervals I(A;h) = A + P_{<=h} (h < n) are cosets of the subspace P_{<=h}, so they PARTITION the monic
polynomials of degree n. Hence, exactly,
    sum over cosets of nu^2 = sum_{D in P_{<=h}} c(D),   c(D) = sum_f Lambda'(f) Lambda'(f + D),
an unweighted ball average over shifts (in Z the same identity carries Fejer weights K - |j|).
Keating-Rudnick (arXiv:1204.0708v3, Thm 2.1): Var nu(.;h) ~ q^{h+1} (n - h - 2) as q -> infinity, h < n - 3.
We compute everything exactly for small q, n and print
    the mean of c(D)/q^n over the q^{h+1} - 1 nonzero shifts D of degree <= h, its min and max,
and the Keating-Rudnick ratio Var / (q^{h+1} (n - h - 2)) (-> 1 as q -> infinity for h < n - 3).
Usage: /usr/bin/python3 -I code/explore/ff_ball_variance.py q n     (q prime; needs python-flint)
"""
import sys
import numpy as np
import flint

q = int(sys.argv[1]) if len(sys.argv) > 1 else 5
n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
M = q ** n
# index of monic f = T^n + sum_{i<n} a_i T^i  <->  integer sum a_i q^i
digits = np.array([(np.arange(M) // q ** i) % q for i in range(n)])  # shape (n, M)
lam = np.zeros(M, dtype=np.int64)
for idx in range(M):
    a = [int(digits[i, idx]) for i in range(n)]
    if a[0] == 0:
        continue
    fac = flint.nmod_poly(a + [1], q).factor()[1]
    if len(fac) == 1:
        lam[idx] = fac[0][0].degree()
c0 = int(np.sum(lam * lam))
print(f"q = {q}, n = {n}, q^n = {M}, sum Lambda' = {int(lam.sum())}, c(0)/q^n = {c0 / M:.6f}")

def shifted_index(Didx):
    # coefficientwise addition mod q of the digits of D (deg <= h < n) to every f
    d = [(Didx // q ** i) % q for i in range(n)]
    out = np.zeros(M, dtype=np.int64)
    for i in range(n):
        out += ((digits[i] + d[i]) % q) * q ** i
    return out

for h in range(0, n - 2):
    nD = q ** (h + 1)
    cs = np.array([int(np.sum(lam * lam[shifted_index(D)])) for D in range(nD)])
    # ultrametric identity check: sum over cosets of nu^2 equals sum_D c(D)
    coset = np.arange(M) // nD            # cosets of P_{<=h}: same digits above position h
    nu = np.bincount(coset, weights=lam).astype(np.int64)
    lhs = int(np.sum(nu * nu)); rhs = int(cs.sum())
    mean = lam.sum() / len(nu)            # average over A in M_n equals average over cosets
    var = np.mean((nu - mean) ** 2)
    Snz = (rhs - c0) / M
    kr = var / (q ** (h + 1) * (n - h - 2)) if n - h - 2 > 0 else float('nan')
    print(f"h = {h}: identity {lhs == rhs}; #shifts {nD - 1}; mean c(D)/q^n over D != 0 = {Snz / (nD - 1):.5f}; "
          f"Var/(q^(h+1)(n-h-2)) = {kr:.4f}; min/max c(D)/q^n (D!=0) = {cs[1:].min() / M:.3f}/{cs[1:].max() / M:.3f}")
