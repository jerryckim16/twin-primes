#!/usr/bin/env python3
"""Scratch (Session 15 helper; see notes/psi-weight/attempt-helper.md): w-form of the psi fibre integral and adversarial tests.
I(a,x) = k/(k-1) log((c0+k s)/(c0+s)) + int_0^{2eps} (1+N(w))/(a + sum_{x_j>=w}(s+w-x_j)) dw,
s = tau - sum x, c0 = a - tau, N(w) = #{j: x_j >= w}.  Floating point."""
import numpy as np
from math import log
import sys
sys.path.insert(0, '.')
from psi_weight_fibers import I as I_orig, k, eps, L, tau, SCALING
E2 = 2 * eps

def I_w(a, x):
    x = np.sort(np.asarray(x, float))[::-1]
    s = tau - x.sum(); c0 = a - tau
    if s < -1e-14: return -np.inf
    tot = k / (k - 1) * log((c0 + k * s) / (c0 + s))
    cuts = sorted(set([0.0, E2] + [v for v in x if 0 < v < E2]))
    for lo, hi in zip(cuts, cuts[1:]):
        act = x >= 0.5 * (lo + hi)
        n = act.sum(); c = a + n * s - x[act].sum()
        tot += (hi - lo) / c if n == 0 else (1 + n) / n * log((c + n * hi) / (c + n * lo))
    return tot

def I_quad(a, x, M=200000):
    """independent midpoint quadrature of the ORIGINAL u-integrand"""
    x = np.asarray(x, float); T = x.sum(); U = L - T
    u = (np.arange(M) + 0.5) / M * U
    act = x[None, :] >= (T + u[:, None] - tau)
    num = 1 + act.sum(1)
    den = a + (act * (u[:, None] - x[None, :])).sum(1)
    return (num / den).sum() * U / M

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    for t in range(5):
        x = rng.random(k - 1) * (rng.random(k - 1) < 0.3) * 0.1
        x *= min(1, 0.9 / x.sum())
        print(I_orig(1.037, x), I_w(1.037, x), I_quad(1.037, x))
