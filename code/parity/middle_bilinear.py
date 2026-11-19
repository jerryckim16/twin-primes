#!/usr/bin/env python3
"""Parity attempt 2026-11-19, Session 35 (route card
notes/parity-attempts/2026-11-19-smooth-middle-bilinear.md): bilinear structure in the MIDDLE of a
twin pair.  For twin primes m-1, m+1 the middle m = 6k is composite and, if y-smooth, factors as
m = ab with a, b in any prescribed dyadic ranges.  Does this Type II structure in the index variable
separate the true twin weight from the parity-fake weight w(m) = 1 - lambda(m-1) lambda(m+1)
(which vanishes on every twin middle and has the same Type I data under two-point Chowla)?

The decisive quantity is the bilinear form of the parity twist along products,
    M_mid[a,b]  = lambda(ab-1) lambda(ab+1)            (twist in the MIDDLE variable),
against the control
    M_sift[a,b] = lambda(ab)                           (twist in a SIFTED variable, multiplicative),
and a random +-1 matrix of the same size.  We estimate the infinity->1 ("cut") norm
    ||M|| = max_{alpha, beta in {+-1}} sum_{a,b} alpha_a beta_b M[a,b]
from below by alternating maximisation from several starts (a lower bound only; for M_sift it is
exact: alpha = lambda(a), beta = lambda(b) gives A*B).  A parity-detecting Type II estimate needs
||M|| comparable to A*B; random-matrix size is about sqrt(A*B*(A+B)).

Part 2 (context, not a parity test): T_y(X) = #{m <= X : m-1, m+1 prime, P+(m) <= y} against all
twins, and the y-smooth proportion among all multiples of 6 (twin middles are smoother: for p >= 5,
p | k has density 1/(p-2) among twin centres, 1/p among all k).

usage: /usr/bin/python3 -I code/parity/middle_bilinear.py [X] [A] [seed] > code/parity/middle_bilinear.out
       defaults X = 10**7, A = 1000 (B = A, products a*b with a, b in (A, 2A], so ab <= 4A^2 <= X).
"""
import sys
import numpy as np


def omega_and_lpf(N):
    """Omega(n) (with multiplicity) and largest prime factor P+(n) for 0 <= n <= N."""
    om = np.zeros(N + 1, dtype=np.int8)
    lpf = np.ones(N + 1, dtype=np.int32)
    is_p = np.ones(N + 1, dtype=bool)
    is_p[:2] = False
    r = int(N ** 0.5) + 1
    for p in range(2, r + 1):
        if is_p[p]:
            is_p[p * p::p] = False
    primes = np.nonzero(is_p)[0]
    for p in primes:
        p = int(p)
        lpf[p::p] = p          # ascending p: the last write is the largest prime factor
        pk = p
        while pk <= N:
            om[pk::pk] += 1
            pk *= p
    return om, lpf, is_p


def cut_lower(M, starts, rng):
    """Lower bound for max over sign vectors of alpha^T M beta (alternating maximisation)."""
    best = -np.inf
    A, B = M.shape
    for s in range(starts):
        beta = rng.choice((-1.0, 1.0), size=B)
        val_old = -np.inf
        for _ in range(100):
            alpha = np.sign(M @ beta); alpha[alpha == 0] = 1
            beta = np.sign(M.T @ alpha); beta[beta == 0] = 1
            val = float(alpha @ M @ beta)
            if val <= val_old:
                break
            val_old = val
        best = max(best, val_old)
    return best


def main():
    X = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    A = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rng = np.random.default_rng(seed)
    N = max(X, 4 * A * A) + 2
    om, lpf, is_p = omega_and_lpf(N)
    lam = np.where(om % 2 == 0, 1, -1).astype(np.int8)
    lam[0] = 0
    print(f"middle_bilinear.py  X = {X}  A = B = {A}  seed = {seed}  (sieve to N = {N})")

    # ---- Part 1: cut norms of the parity twist along products a*b, a, b in (A, 2A]
    a = np.arange(A + 1, 2 * A + 1, dtype=np.int64)
    P = np.outer(a, a)
    Mmid = (lam[P - 1].astype(np.int64) * lam[P + 1].astype(np.int64)).astype(float)
    Msift = lam[P].astype(float)
    Mrand = rng.choice((-1.0, 1.0), size=Mmid.shape)
    AB = A * A
    rmt = (AB * 2 * A) ** 0.5
    print("\nPart 1: infinity->1 norm lower bounds (alternating maximisation, 20 starts)")
    print(f"  A*B = {AB},  sqrt(A*B*(A+B)) = {rmt:.0f}")
    for name, M in (("lambda(ab-1)lambda(ab+1)  [middle twist]", Mmid),
                    ("lambda(ab)                [sifted, multiplicative]", Msift),
                    ("random +-1                [control]", Mrand)):
        c = cut_lower(M, 20, rng)
        print(f"  {name:52s} sum = {M.sum():+12.0f}   cut >= {c:12.0f}"
              f"   cut/AB = {c / AB:.4f}   cut/sqrt(AB(A+B)) = {c / rmt:.3f}")
    # exact witness for the sifted twist
    la = lam[a].astype(float)
    print(f"  witness alpha=beta=lambda: alpha^T Msift beta = {la @ Msift @ la:.0f} (= A*B exactly)")
    # same witness on the middle twist, and Type I-style restriction to classes mod 3 of ab
    print(f"  witness alpha=beta=lambda on Mmid: {la @ Mmid @ la:+.0f}")
    for r in (0, 1, 2):
        mask = (P % 3 == r)
        print(f"  restricted to ab = {r} mod 3: sum of Mmid = {Mmid[mask].sum():+.0f} over {int(mask.sum())} cells,"
              f" cut >= {cut_lower(np.where(mask, Mmid, 0.0), 10, rng):.0f}")

    # ---- Part 2: twins with smooth middle (context)
    print("\nPart 2: twin middles m <= X (m-1, m+1 prime) with P+(m) <= y")
    m = np.arange(6, X + 1, 6)
    tw = m[is_p[m - 1] & is_p[m + 1]]
    print(f"  twin pairs with middle <= X: {tw.size} (plus (3,5))")
    for e in (0.5, 1 / 3, 0.25, 0.2):
        y = X ** e
        f_tw = float(np.mean(lpf[tw] <= y))
        f_all = float(np.mean(lpf[m] <= y))
        print(f"  y = X^{e:.3f} = {y:9.0f}:  twin middles smooth {f_tw:.4f}   all multiples of 6 smooth {f_all:.4f}"
              f"   ratio {f_tw / f_all:.3f}")
    # weighted sum of the fake weight over smooth middles: the fake weight vanishes on twins
    for e in (1 / 3, 0.25):
        y = X ** e
        sm = m[lpf[m] <= y]
        f = lam[sm - 1].astype(np.int64) * lam[sm + 1].astype(np.int64)
        print(f"  sum over smooth middles (y = X^{e:.3f}) of lambda(m-1)lambda(m+1) = {int(f.sum()):+d}"
              f" over {sm.size} middles (mean {f.mean():+.4f})")


if __name__ == "__main__":
    main()
