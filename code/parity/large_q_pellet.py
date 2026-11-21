#!/usr/bin/env python3
"""Large-q function-field twin primes vs. rough integers (Session 41 parity route card).

Usage: /usr/bin/python3 -I code/parity/large_q_pellet.py [X] [> code/parity/large_q_pellet.out]

Part A (Computed, exact): for prime q and small n, over all monic F of degree n in F_q[x]:
  (a) Pellet's formula mu(F) = (-1)^n chi_2(disc F) is checked for every F;
  (b) C(q,n) = sum_F mu(F) mu(F+1) against the Carmon-Rudnick bound 4n q^{n-1/2} + 6n^2 q^{n-1}
      (their (1.3) with r = 2);
  (c) the twin count pi(q,n;0,1) = #{F : F, F+1 irreducible} against q^n/n^2 (Bary-Soroker Thm 1.1);
  (d) the four parity classes of (mu(F), mu(F+1)) on pairs of squarefree F, F+1.
  In M_n every monic factor has degree >= 1, i.e. norm >= q = |F|^{1/n}: M_n is "|F|^{1/n}-rough".
Part B (Computed, illustrative): integers m <= X with m and m+2 both X^{1/n}-rough (n = 3, 4), the
  joint distribution of (lambda(m), lambda(m+2)) and the share of twin-prime pairs among rough pairs.
"""
import sys, itertools, math
import numpy as np
from flint import nmod_poly


def chi2(a, q):
    a %= q
    if a == 0:
        return 0
    return 1 if pow(a, (q - 1) // 2, q) == 1 else -1


def mobius_poly(F):
    fac = F.factor()[1]
    if any(e > 1 for _, e in fac):
        return 0
    return (-1) ** len(fac)


def part_a(q, n):
    one = nmod_poly([1], q)
    pell_bad = 0
    C = 0
    twins = 0
    cls = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    mu_cache = {}
    for coeffs in itertools.product(range(q), repeat=n):
        F = nmod_poly(list(coeffs) + [1], q)
        key = tuple(coeffs)
        m = mobius_poly(F)
        mu_cache[key] = m
        if m != ((-1) ** n) * chi2(int(F.discriminant()), q):
            pell_bad += 1
    for coeffs in itertools.product(range(q), repeat=n):
        k1 = tuple(coeffs)
        k2 = ((coeffs[0] + 1) % q,) + tuple(coeffs[1:])
        a, b = mu_cache[k1], mu_cache[k2]
        C += a * b
        if a and b:
            cls[(a, b)] += 1
        F = nmod_poly(list(coeffs) + [1], q)
        if a == -1 and b == -1:
            # both squarefree with an odd number of factors; test irreducibility
            if len(F.factor()[1]) == 1 and len((F + one).factor()[1]) == 1:
                twins += 1
    cr = 4 * n * q ** (n - 0.5) + 6 * n * n * q ** (n - 1)
    return pell_bad, C, cr, twins, cls


def part_b(X, n):
    z = int(round(X ** (1.0 / n)))
    N = X + 3
    isprime = np.ones(N, dtype=bool)
    isprime[:2] = False
    for p in range(2, int(N ** 0.5) + 1):
        if isprime[p]:
            isprime[p * p::p] = False
    rough = np.ones(N, dtype=bool)
    rough[:2] = False
    small = np.nonzero(isprime[: z + 1])[0]
    for p in small:
        rough[p::p] = False
    # Omega(m) for all m < N: divide out prime powers p^k, p <= sqrt(N); a cofactor > 1 is one more prime
    rem = np.arange(N, dtype=np.int64)
    Om = np.zeros(N, dtype=np.int8)
    for p in np.nonzero(isprime[: int(N ** 0.5) + 1])[0]:
        pk = int(p)
        while pk < N:
            rem[pk::pk] //= p
            Om[pk::pk] += 1
            pk *= int(p)
    Om += (rem > 1)
    idx = np.nonzero(rough[1 : X + 1] & rough[3 : X + 3])[0] + 1   # m with m, m+2 rough
    lamv = np.where(Om % 2 == 0, 1, -1)
    def lam(m):
        return int(lamv[m])
    counts = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    for m in idx:
        m = int(m)
        counts[(lam(m), lam(m + 2))] += 1
    tot = len(idx)
    single = int(rough[1 : X + 1].sum())
    primes_rough = int((isprime[1 : X + 1] & rough[1 : X + 1]).sum())
    return z, tot, counts, single, primes_rough


def main():
    X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 7
    print("Part A: F_q[x], monic degree n (exact enumeration)")
    print("q n | Pellet failures | C=sum mu(F)mu(F+1) | CR bound | twins | q^n/n^2 | twins/(q^n/n^2) | classes (+,+) (+,-) (-,+) (-,-)")
    for q, n in [(3, 3), (5, 3), (7, 3), (11, 3), (13, 3), (17, 3), (19, 3), (23, 3), (29, 3),
                 (3, 4), (5, 4), (7, 4), (11, 4), (13, 4), (3, 6), (3, 8), (3, 9)]:
        bad, C, cr, tw, cls = part_a(q, n)
        pred = q ** n / n ** 2
        print(f"{q} {n} | {bad} | {C} | {cr:.0f} | {tw} | {pred:.1f} | {tw/pred:.3f} | "
              f"{cls[(1,1)]} {cls[(1,-1)]} {cls[(-1,1)]} {cls[(-1,-1)]}")
    print()
    print(f"Part B: integers m <= X = {X} with m, m+2 both X^(1/n)-rough")
    for n in (3, 4):
        z, tot, cnt, single, pr = part_b(X, n)
        share_prime = pr / single
        print(f"n={n}: z={z}; rough m: {single}; share prime among rough m: {share_prime:.4f}; rough pairs: {tot}")
        print(f"   (lambda(m),lambda(m+2)) classes (+,+) (+,-) (-,+) (-,-): "
              f"{cnt[(1,1)]} {cnt[(1,-1)]} {cnt[(-1,1)]} {cnt[(-1,-1)]}")
        corr = (cnt[(1,1)] + cnt[(-1,-1)] - cnt[(1,-1)] - cnt[(-1,1)]) / tot
        indep = share_prime ** 2
        print(f"   twin pairs (-,-) share {cnt[(-1,-1)]/tot:.4f} (independence would give about {indep:.4f}, "
              f"before the twin singular-series factor); mean lambda(m)lambda(m+2) = {corr:+.4f}")


if __name__ == "__main__":
    main()
