#!/usr/bin/env python3
"""Scratch (Session 15 helper; see notes/psi-weight/attempt-helper.md): adversarial coordinate-ascent search for sup_x I(a,x).
Each step maximises I over ONE coordinate on a fine grid of its whole feasible range
[0, x_j + s] (others fixed). Random starts of several shapes. Floating point."""
import sys; sys.path.insert(0, '/home/user/twin-primes/code/explore')
import numpy as np
from psi_scratch_wform import I_w, k, tau, E2

def best_equal(a):
    return max((I_w(a, [E2] * r + [0] * (k - 1 - r)), r) for r in range(0, 13))

def coord_ascent(a, x, rng, sweeps=6, G=161):
    x = x.copy(); v = I_w(a, x)
    for sw in range(sweeps):
        for j in rng.permutation(k - 1):
            s = tau - x.sum(); hi = x[j] + s
            grid = np.unique(np.concatenate([np.linspace(0, hi, G), [min(E2, hi), x[j]]]))
            vals = []
            for y in grid:
                x2 = x.copy(); x2[j] = y; vals.append(I_w(a, x2))
            i = int(np.argmax(vals))
            if vals[i] > v + 1e-15: x[j] = grid[i]; v = vals[i]
    return v, x

def start(rng):
    x = np.zeros(k - 1); t = rng.integers(6)
    m = rng.integers(1, k)
    if t == 0: x[:m] = rng.random(m) * 0.1
    elif t == 1: x[:m] = rng.exponential(0.02, m)
    elif t == 2: x[0] = rng.random() * 0.8; x[1:m] = rng.random(m - 1) * 0.02
    elif t == 3: x[:m] = E2 * rng.uniform(0.8, 1.0, m)
    elif t == 4: x[:m] = rng.random(m) * 0.3
    else: x[:] = rng.random(k - 1) * 0.019
    if x.sum() > tau: x *= rng.uniform(0.5, 1) * tau / x.sum()
    return x

if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    for a in [1.03, 1.035, 1.037, 1.04, 1.045, 1.05]:
        be, r = best_equal(a)
        best = -1
        for it in range(25):
            v, x = coord_ascent(a, start(rng), rng)
            if v > best: best, bx = v, x
        bx = np.sort(bx)[::-1]
        print("a=%.3f equal(2eps)^r: %.8f (r=%d, a*I=%.6f) | search %.8f diff %.2e | top %s"
              % (a, be, r, a * be, best, best - be, np.round(bx[:12], 4)), flush=True)
