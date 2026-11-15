#!/usr/bin/env python3
"""Exploration (Heuristic; Session 24): Hooley's averaged parity-bias quantity for the twin-prime sequence,
   H(x, D) = sum_{d <= D} | sum_{p <= x, p = 2 mod d} mu(p-2) log p |,
compared with a random model in which mu(p-2) is replaced by independent signs on the same support
(squarefree p-2), averaged over seeds. A log-power saving (Hooley's condition) would show H/x -> 0;
square-root cancellation predicts H ~ sum_d sqrt(#terms_d) * log x.
Usage: python3 -I hooley_twin_parity.py [x] [alpha ...]"""
import sys, math
import numpy as np
x = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**7
alphas = [float(a) for a in sys.argv[2:]] or [0.25, 0.4, 0.5]
N = x + 1
# mu via linear-ish sieve
mu = np.ones(N, dtype=np.int8); isp = np.ones(N, dtype=bool); isp[:2] = False
for p in range(2, int(math.isqrt(N)) + 1):
    if isp[p]:
        isp[p*p::p] = False
for p in np.nonzero(isp)[0]:
    mu[p::p] *= -1
    p2 = int(p) * int(p)
    if p2 < N:
        mu[p2::p2] = 0
primes = np.nonzero(isp)[0]
primes = primes[primes >= 5]
m = mu[primes - 2].astype(np.float64)          # mu(p-2)
w = np.log(primes.astype(np.float64)) * m
sup = (m != 0)
print(f"x = {x:.1e}: #p = {len(primes)}, sum mu(p-2) log p / x = {w.sum()/x:+.5f}, squarefree share = {sup.mean():.4f}")
rng = np.random.default_rng(20261115)
for a in alphas:
    D = int(x ** a)
    resid = primes - 2
    H = 0.0; Hr = np.zeros(4)
    signs = [np.where(sup, rng.choice([-1.0, 1.0], size=len(primes)), 0.0) * np.log(primes.astype(np.float64)) for _ in range(4)]
    for d in range(1, D + 1):
        sel = (resid % d == 0)
        H += abs(w[sel].sum())
        for j in range(4):
            Hr[j] += abs(signs[j][sel].sum())
    print(f"alpha = {a}: D = {D}, H/x = {H/x:.4f}, random model H/x = {Hr.mean()/x:.4f} (+- {Hr.std()/x:.4f}), ratio = {H/Hr.mean():.3f}")
