#!/usr/bin/env python3
"""Exploration 2026-11-19, Session 35: the Liouville function at the centres of twin primes.
For twin primes 6k-1, 6k+1 the middle is 6k and lambda(6k) = lambda(k).  Is the mean of lambda(k)
over twin centres k <= K biased, and does it follow the naive local model?

Naive local model (Heuristic): among twin centres, for p >= 5, v_p(k) = 0 has weight (p-3)/p and
v_p(k) = j >= 1 weight p^{-j}(1 - 1/p), normalised by (p-2)/p.  The local mean of (-1)^{v_p(k)} is
    (p^2 - 3p - 2) / ((p - 2)(p + 1))  = 1 - 2p/(p^2 - p - 2),
against (p - 1)/(p + 1) for all k.  Both products tend to 0 like (log y)^(-2); the actual mean of
lambda over all k is far smaller (o(1) by the prime number theorem, about K^(-1/2) on average).
We print the empirical means, their ratio to the all-k mean, the truncated model products,
and a model-free comparison: mean of lambda(k) over k with 6k-1, 6k+1 both free of prime factors < z
(a sieve-only proxy for twin centres), which is what a sieve can see.

usage: /usr/bin/python3 -I code/explore/liouville_twin_centres.py [K] > code/explore/liouville_twin_centres.out
"""
import sys
import numpy as np


def main():
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    N = 6 * K + 2
    is_p = np.ones(N + 1, dtype=bool); is_p[:2] = False
    for p in range(2, int(N ** 0.5) + 1):
        if is_p[p]:
            is_p[p * p::p] = False
    om = np.zeros(K + 1, dtype=np.int8)
    for p in np.nonzero(is_p[:K + 1])[0]:
        p = int(p); pk = p
        while pk <= K:
            om[pk::pk] += 1; pk *= p
    lam = np.where(om % 2 == 0, 1, -1).astype(np.int64); lam[0] = 0
    k = np.arange(1, K + 1)
    twin = is_p[6 * k - 1] & is_p[6 * k + 1]
    print(f"liouville_twin_centres.py  K = {K}  (twin pairs 6k-1, 6k+1 with k <= K: {int(twin.sum())})")
    print(f"{'K':>10s} {'#twins':>8s} {'mean lam(k) twins':>18s} {'z-score':>8s} {'mean lam(k) all k':>18s}"
          f" {'sieve proxy z=100':>18s}")
    # sieve proxy: 6k +- 1 free of primes < z (z = 100), at 2,3 automatic
    z = 100
    rough = np.ones(K, dtype=bool)
    for p in range(5, z):
        if is_p[p]:
            r1 = (6 * k - 1) % p != 0
            r2 = (6 * k + 1) % p != 0
            rough &= r1 & r2
    for e in range(4, 9):
        Kc = 10 ** e
        if Kc > K:
            break
        t = twin[:Kc]; l = lam[1:Kc + 1]; rp = rough[:Kc]
        n = int(t.sum()); mt = l[t].mean()
        print(f"{Kc:>10d} {n:>8d} {mt:>+18.5f} {mt * n ** 0.5:>+8.2f} {l.mean():>+18.6f} {l[rp].mean():>+18.5f}")
    # truncated local-model products
    ps = [p for p in range(5, 10 ** 5) if is_p[p]]
    tw_prod = np.prod([(p * p - 3 * p - 2) / ((p - 2) * (p + 1)) for p in ps])
    all_prod = np.prod([(p - 1) / (p + 1) for p in ps])
    print(f"\nnaive local model, product over 5 <= p < 1e5: twin centres {tw_prod:.5f}, all k (p >= 5) {all_prod:.5f}")
    print("(the naive model's products are NOT predictions of the actual means: lambda is non-pretentious)")


if __name__ == "__main__":
    main()
