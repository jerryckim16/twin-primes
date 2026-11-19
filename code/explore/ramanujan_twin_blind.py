#!/usr/bin/env python3
"""Exploration (Session 36): are Ramanujan-Fourier coefficients parity-blind for twin correlations?
Heuristic / exploratory.  Gadiyar-Padma-type heuristic: if f(n) ~ sum_q a_q(f) c_q(n) with a_q(f) = mean of f(n) c_q(n)
/ phi(q), Wiener-Khintchine suggests (1/X) sum f(n) f(n+2) ~ sum_q a_q(f)^2 phi(q) c_q(2).  Compare
  f1 = Lambda'(n) = Lambda(n) phi(n)/n  (true primes)  and  f2 = f1 * 1[n is not the smaller or larger of a twin pair]
(a parity-type fake: AP data proportional to those of f1 up to small errors; r = mean ratio).  Usage: ramanujan_twin_blind.py [X] [QMAX]"""
import sys, math
import numpy as np
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**7
QMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 60
N = X + 3
sieve = np.ones(N, dtype=bool); sieve[:2] = False
for p in range(2, int(N ** 0.5) + 1):
    if sieve[p]: sieve[p * p::p] = False
n = np.arange(N, dtype=np.float64)
lam = np.where(sieve, np.log(np.maximum(n, 2)), 0.0)   # Lambda on primes only (prime powers negligible)
lam[:3] = 0.0; lam[2] = math.log(2)
twin = sieve[:-2] & sieve[2:]
istwin = np.zeros(N, dtype=bool); istwin[:-2] |= twin; istwin[2:] |= twin
f1 = lam[:X + 1].copy(); f2 = f1 * (~istwin[:X + 1])
def mu(q):
    r, k, p = 1, q, 2
    while p * p <= k:
        if k % p == 0:
            k //= p
            if k % p == 0: return 0
            r = -r
        p += 1
    return -r if k > 1 else r
def phi(q):
    return sum(1 for a in range(1, q + 1) if math.gcd(a, q) == 1)
def cq(q, h):
    return sum(math.cos(2 * math.pi * a * h / q) for a in range(1, q + 1) if math.gcd(a, q) == 1)
idx = np.arange(X + 1)
def coeff(f, q):
    # a_q = (1/(X phi(q))) sum_n f(n) c_q(n);  c_q(n) depends on n mod q
    table = np.array([cq(q, r) for r in range(q)])
    return float((f * table[idx % q]).sum()) / (X * phi(q))
print(f"X = {X:.0e}, QMAX = {QMAX}")
print(" q   a_q(true)   a_q(fake)   a_q(fake)/r   mu(q)/phi(q)")
r = float(f2.sum() / f1.sum())   # rescale the fake to the same mean
S1 = S2 = Spred = 0.0; D = 0.0
for q in range(1, QMAX + 1):
    a1, a2 = coeff(f1, q), coeff(f2, q)
    pred = mu(q) / phi(q)
    if q <= 12 or q in (30, 60):
        print(f"{q:3d}  {a1:+.5f}    {a2:+.5f}    {a2 / r:+.5f}      {pred:+.5f}")
    S1 += a1 * a1 * cq(q, 2); S2 += (a2 / r) ** 2 * cq(q, 2); D = max(D, abs(a2 / r - a1)); Spred += mu(q) ** 2 / phi(q) ** 2 * cq(q, 2)
corr1 = float((f1[:-2] * f1[2:]).sum()) / X; corr2 = float((f2[:-2] * f2[2:]).sum()) / X
print(f"max_q |a_q(fake)/r - a_q(true)| = {D:.2e}")
print(f"Wiener-Khintchine sum over q <= {QMAX}: true {S1:.4f}, rescaled fake {S2:.4f}, from mu/phi {Spred:.4f}  (2 C2 = 1.3203)")
print(f"actual (1/X) sum f(n) f(n+2): true {corr1:.4f}, rescaled fake {corr2 / r ** 2:.4f}")
print(f"mass removed from f1 by the fake: {1 - f2.sum() / f1.sum():.4f} (compare 2 * 1.32 / log X = {2.64 / math.log(X):.4f}; both members of each pair are removed)")
