#!/usr/bin/env python3
"""Parity-class limit for almost-prime k-tuples: DHL_Omega[k; r] (Omega(L_1(n)...L_k(n)) <= r i.o.).

Route card notes/parity-attempts/2026-11-20-almost-prime-tuples.md.
Class: Liouville-pattern weights w >= 0 on {+-1}^k (not identically 0) whose singleton Fourier
coefficients vanish (fair) or are <= 0 (weakly fair: density of sign -1 at each position >= 1/2).
A weight blocks a target iff it vanishes on every sign pattern compatible with the target.

Checks:
 (1) sign-space identity: the patterns compatible with Omega(P) <= r (each L_i(n) > 1, so Omega_i >= 1;
     sign -1 iff Omega_i odd) are exactly those with at least 2k - r minus signs (enumeration over
     Omega-vectors with entries <= 4, k <= 7);
 (2) LP (scipy HiGHS) on {+-1}^k, k <= 10, every r in [k, 2k]: blocked iff r <= floor(3k/2) - 1,
     for both fairness variants;
 (3) independent exact check (fractions, no LP): explicit layer weights for the blocked cases,
     and the averaging obstruction E[#plus] >= 2k-r... for the unblocked cases;
 (4) table: parity-class limit vs. best known values (Lewulis arXiv:2203.09432v1 Table A/B).
"""
import itertools, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

def compatible_patterns_by_omega(k, r, omax=4):
    pats = set()
    for om in itertools.product(range(1, omax + 1), repeat=k):
        if sum(om) <= r:
            pats.add(tuple(-1 if o % 2 else 1 for o in om))
    return pats

def compatible_patterns_formula(k, r):
    return {p for p in itertools.product((1, -1), repeat=k) if sum(1 for s in p if s == -1) >= 2 * k - r}

def lp_blocked(k, r, weak=False):
    pats = [p for p in itertools.product((1, -1), repeat=k)]
    comp = compatible_patterns_formula(k, r)
    free = [p for p in pats if p not in comp]
    if not free:
        return False
    n = len(free)
    A = np.array([[p[i] for p in free] for i in range(k)], dtype=float)  # singleton coefficients
    if weak:
        res = linprog(np.zeros(n), A_ub=A, b_ub=np.zeros(k), A_eq=np.ones((1, n)), b_eq=[1.0],
                      bounds=[(0, None)] * n, method="highs")
    else:
        res = linprog(np.zeros(n), A_eq=np.vstack([A, np.ones((1, n))]), b_eq=list(np.zeros(k)) + [1.0],
                      bounds=[(0, None)] * n, method="highs")
    return res.status == 0

def exact_check(k, r):
    """Independent exact decision. Returns (blocked, certificate string)."""
    s0 = r - k + 1           # free patterns: #plus >= s0
    if s0 <= k // 2:
        # explicit weight: uniform on layer k/2 (k even) or half/half on layers (k-1)/2, (k+1)/2
        layers = [k // 2] if k % 2 == 0 else [(k - 1) // 2, (k + 1) // 2]
        w = {}
        for p in itertools.product((1, -1), repeat=k):
            t = sum(1 for s in p if s == 1)
            w[p] = Fr(1, len(layers)) / Fr(len([q for q in itertools.product((1, -1), repeat=k)
                                                 if sum(1 for s in q if s == 1) == t])) if t in layers else Fr(0)
        comp = compatible_patterns_formula(k, r)
        assert all(w[p] == 0 for p in comp)
        assert sum(w.values()) == 1 and all(v >= 0 for v in w.values())
        for i in range(k):
            assert sum(w[p] * p[i] for p in w) == 0
        return True, f"layers {layers}"
    # obstruction: any probability on #plus >= s0 has sum_i P(+ at i) = E[#plus] >= s0 > k/2,
    # while (weak) fairness needs sum_i P(+ at i) <= k/2.
    assert Fr(s0) > Fr(k, 2)
    return False, f"E[#plus] >= {s0} > {Fr(k,2)}"

def main():
    # (1)
    for k in range(1, 8):
        for r in range(k, 2 * k + 1):
            assert compatible_patterns_by_omega(k, r) == compatible_patterns_formula(k, r), (k, r)
    print("(1) sign-space identity Omega(P)<=r  <=>  >= 2k-r minus signs: OK for k<=7, r in [k,2k]")
    # (2) + (3)
    lim = {}
    for k in range(1, 11):
        for r in range(k, 2 * k + 1):
            b1, b2 = lp_blocked(k, r), lp_blocked(k, r, weak=True)
            b3, cert = exact_check(k, r)
            pred = r <= (3 * k) // 2 - 1
            assert b1 == b2 == b3 == pred, (k, r, b1, b2, b3, pred)
        lim[k] = (3 * k) // 2
    print("(2),(3) LP (fair and weakly fair) = exact check = formula 'blocked iff r <= floor(3k/2)-1': OK, k<=10")
    # (4) literature (Lewulis arXiv:2203.09432v1, Table A and Theorem 4 / Table B; k=2 Chen)
    uncond = {2: 3, 3: 7, 4: 11, 5: 14, 6: 18, 7: 21, 8: 25, 9: 29, 10: 33}
    geh = {2: 3, 3: 6, 4: 8, 5: 11, 6: 14, 7: 17, 8: 21, 9: 24, 10: 27}
    print("(4)  k | smallest r not blocked by the class | best known (GEH) | best known (uncond.)")
    for k in range(2, 11):
        print(f"    {k:2d} | {lim[k]:3d} (>= {2*k-lim[k]} primes, rest P_2) | {geh[k]:3d} | {uncond[k]:3d}")

if __name__ == "__main__":
    main()
