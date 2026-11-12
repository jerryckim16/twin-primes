#!/usr/bin/env python3
"""Floating-point exploration behind Remarks 17 and 18 (15 and 16 in paper v0.3) (NOT a certificate).

Remark 17: for the two-zone weight of Theorem 15, the best value of sup W over (a, s1), maximised
over eps, for several k; compared with Polymath8b's bound k/(k-1) log(2k-1) [Prop. 6.5] and with
scaling (1+eps) k/(k-1) log k.

Remark 18: the weight psi_m = (beta/n)(a - S_A + n t_m), n = number of active indices at t,
S_A = sum of the active coordinates. Its sum over the active indices is beta*a, so Lemma 11 gives
M_k(L, tau) <= a * sup_{t'} int_0^{L-|t'|} n(u) / (a - S_A(u) + n(u) u) du.
We evaluate the fiber integral exactly (piecewise in u) on explicit fibers t' = (x, ..., x, 0, ...)
with r coordinates equal to x; this gives a LOWER bound for what the weight can certify.

usage: dual_eps.py [remark15|remark16]
"""
import sys
import numpy as np
from math import log
sys.path.insert(0, "code")
from dual_eps_cert import choose


def remark15():
    print("k  eps*   best sup W   Polymath8b k/(k-1)log(2k-1)")
    for k in (29, 30, 40, 50):
        best, arg, guess = 0, None, None
        for eps in np.arange(0.15, 0.40, 0.005):
            a, s1, f, guess = choose(k, 1 + eps, 1 - eps, guess)
            if f > best:
                best, arg = f, eps
        print("%d  %.3f  %.4f      %.4f" % (k, arg, best, k / (k - 1) * log(2 * k - 1)))
    k, eps = 50, 1 / 25
    a, s1, f, _ = choose(k, 1 + eps, 1 - eps)
    print("k=50, eps=1/25: two-zone weight %.4f, scaling bound (1+eps)k/(k-1)log k = %.4f"
          % (f, (1 + eps) * k / (k - 1) * log(k)))


def fiber_integral(k, L, tau, a, r, x):
    """int_0^{L-|t'|} n/(a - S_A + n u) du on the fiber over t' = (x [r times], 0 [k-1-r times])."""
    T = r * x
    if T > tau + 1e-15:
        return None
    U = L - T
    # breakpoints where indices drop out: zeros at u = tau - T, nonzeros at u = tau - T + x
    cuts = sorted({0.0, U, max(0.0, min(U, tau - T)), max(0.0, min(U, tau - T + x))})
    tot = 0.0
    for lo, hi in zip(cuts, cuts[1:]):
        if hi <= lo:
            continue
        mid = (lo + hi) / 2
        zeros_active = (k - 1 - r) if T + mid - 0 <= tau else 0
        nz_active = r if T + mid - x <= tau else 0
        n = 1 + zeros_active + nz_active
        c = a - nz_active * x           # a - S_A + n u = c - u + n u = c + (n-1) u
        if n == 1:
            tot += (hi - lo) / c
        else:
            tot += n / (n - 1) * log((c + (n - 1) * hi) / (c + (n - 1) * lo))
    return tot


def remark16(k=50, eps=1 / 25):
    L, tau = 1 + eps, 1 - eps
    best = None
    for a in np.arange(L + 0.01, 3.0, 0.01):
        worst, wr = 0, None
        for r in range(0, k):
            for x in np.linspace(0, tau / max(r, 1), 200)[1:] if r else [0.0]:
                v = fiber_integral(k, L, tau, a, r, x)
                if v is not None and a * v > worst:
                    worst, wr = a * v, (r, x)
        if best is None or worst < best[0]:
            best = (worst, a, wr)
    print("k=%d eps=%.3f: weight (beta/n)(a-S_A+n t_m): bound >= %.4f for every a on the grid "
          "(best a=%.2f; binding fiber r=%d, x=%.4f); scaling gives %.4f"
          % (k, eps, best[0], best[1], best[2][0], best[2][1], (1 + eps) * k / (k - 1) * log(k)))


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "both"
    if what in ("remark15", "both"):
        remark15()
    if what in ("remark16", "both"):
        remark16()
