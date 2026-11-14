#!/usr/bin/env python3
"""Scratch (Session 15 helper; see notes/psi-weight/attempt-helper.md): (1) random sanity test of the proved inequality
   I(a,x) <= G(s, nu),  s = tau - sum x,  nu = 1 + sum_j min(x_j, W)/W;
(2) counterexample to 'sup = max_r I(a,(2eps)^r 0^...)' at a = 1.036, evaluated three ways;
(3) one-sided derivative in s of the equal-big family at s = tau - 2eps r (a = 1.037, 1.038).
Floating point."""
import sys; sys.path.insert(0, '/home/user/twin-primes/code/explore')
import numpy as np
from math import log
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from psi_weight_fibers import I as I_orig
from psi_scratch_wform import I_w, I_quad, k, tau, L, E2
W = E2

def G(a, s, nu):
    c0 = a - tau; F = k / (k - 1) * log((c0 + k * s) / (c0 + s)); c = c0 + nu * s
    J = W / (c0 + s) if nu == 1 else nu / (nu - 1) * log((c + (nu - 1) * W) / c)
    return F + J

def I_scipy(a, x):
    """independent: adaptive quadrature of the ORIGINAL integrand on [0, L-T], split at drop points"""
    x = np.asarray(x, float); T = x.sum(); U = L - T
    def f(u):
        act = x >= T + u - tau
        return (1 + act.sum()) / (a + (u - x[act]).sum())
    pts = sorted(set(d for d in x + tau - T if 0 < d < U))
    edges = [0.0] + pts + [U]
    return sum(quad(f, lo, hi, epsabs=1e-14, epsrel=1e-13, limit=200)[0] for lo, hi in zip(edges, edges[1:]))

if __name__ == "__main__":
    rng = np.random.default_rng(11); worst = -1
    for t in range(20000):
        a = rng.uniform(0.97, 1.2); m = rng.integers(1, k)
        x = np.zeros(k - 1); x[:m] = rng.random(m) * rng.choice([0.02, 0.1, 0.3])
        if x.sum() > tau: x *= rng.uniform(0.3, 1) * tau / x.sum()
        s = tau - x.sum(); nu = 1 + np.minimum(x, W).sum() / W
        worst = max(worst, I_w(a, x) - G(a, s, nu))
    print("(1) max of I - G over 20000 random x (should be <= 0):", worst)

    a = 1.036; r = 10
    res = minimize_scalar(lambda s: -G(a, s, r + 1), bounds=(0, tau - W * r), method="bounded",
                          options={"xatol": 1e-12})
    s = res.x; x = [(tau - s) / r] * r + [0.0] * (k - 1 - r)
    print("(2) a=1.036, x = (%.10f)^10 0^39, T = %.10f" % (x[0], tau - s))
    print("    I via psi_weight_fibers.I  : %.10f" % I_orig(a, x))
    print("    I via scipy quad           : %.10f" % I_scipy(a, x))
    print("    I via midpoint quadrature  : %.10f" % I_quad(a, x, 2000000))
    eq = max((I_orig(a, [E2] * q + [0.0] * (k - 1 - q)), q) for q in range(13))
    print("    max_r I(a,(2eps)^r)        : %.10f (r=%d), scipy %.10f" % (eq[0], eq[1], I_scipy(a, [E2]*eq[1] + [0.0]*(k-1-eq[1]))))
    for a in [1.0365, 1.037, 1.0375, 1.038]:
        out = []
        for r in range(8, 12):
            s0 = tau - W * r; h = 1e-7
            out.append("r=%d dG/ds(s0-)=%+.4f" % (r, (G(a, s0, r + 1) - G(a, s0 - h, r + 1)) / h))
        print("(3) a=%.4f " % a, "; ".join(out))
