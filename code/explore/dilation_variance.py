#!/usr/bin/env python3
"""Exploration (Session 39, 20 Nov 2026): variance of prime counts along dilation sets
{a h - 2 : a in A} as h varies, for A = K-products of primes from disjoint ranges (the
structure of Lu-Wang-Wu's Type II estimate), against a local-density model and against
control sets of the same size and range. Heuristic / exploratory; not a proof of anything.
Usage: python3 dilation_variance.py [HMAX] [seed]
"""
import sys, math, random
import numpy as np

HMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
random.seed(seed)

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]: s[p * p::p] = False
    return s

small = [p for p in range(3, 2000) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
P1 = [p for p in small if 20 < p <= 40]
P2 = [p for p in small if 400 < p <= 800]
A_prod = sorted(a * b for a in P1 for b in P2)          # K = 2 products
lo, hi = min(A_prod), max(A_prod)
N = hi * HMAX + 10
isp = primes_upto(N)
# control 1: random odd integers in [lo, hi] coprime to 2*3*5*7*11*13*17*19, same count
ctrl = set()
while len(ctrl) < len(A_prod):
    a = random.randrange(lo, hi + 1)
    if all(a % q for q in (2, 3, 5, 7, 11, 13, 17, 19)): ctrl.add(a)
ctrl = sorted(ctrl)
# control 2: primes in [lo, hi] (K = 1 Ramare-type set), same count, random sample
pr = [p for p in range(lo, hi + 1) if isp[p]]
ctrl2 = sorted(random.sample(pr, len(A_prod)))
Z = [2] + [q for q in small if q < 200]

def stats(A):
    A = np.array(A, dtype=np.int64)
    num = 0.0; den = 0.0; bern = 0.0; zs = []
    for h in range(HMAX // 2, HMAX + 1):
        v = A * h - 2
        c = int(isp[v].sum())
        # local density model: prod over small q of (1 - [q | ah-2]) / (1 - 1/q), divided by log(ah)
        w = np.ones(len(A))
        for q in Z:
            w *= np.where(v % q == 0, 0.0, q / (q - 1.0))
        pr_ = np.minimum(w / np.log(v.astype(float)), 1.0)
        e = float(pr_.sum())
        num += (c - e) ** 2; den += e; bern += float((pr_ * (1 - pr_)).sum()); zs.append(c - e)
    return num / den, num / bern, float(np.mean(zs)), den / (HMAX - HMAX // 2 + 1)

print(f"HMAX={HMAX} seed={seed} |A|={len(A_prod)} range=[{lo},{hi}] N={N}")
for name, A in (("K=2 products", A_prod), ("random coprime ints", ctrl), ("primes (K=1)", ctrl2)):
    r, rb, bias, mean_e = stats(A)
    print(f"{name:22s} var/Poisson = {r:.3f}  var/Bernoulli = {rb:.3f}  mean(C-E) = {bias:+.3f}  mean E = {mean_e:.2f}")
