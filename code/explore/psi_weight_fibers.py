#!/usr/bin/env python3
"""Own idea (Session 15), FC3 question of the internal referee report: does the dual weight
psi_m = (beta/n)(a - S_A + n t_m) of paper Remark (another weight) beat the scaling bound 4.1515 at
(k, eps) = (50, 1/25) once ALL fibers t' are taken into account, not only t' = (x,...,x,0,...,0)?

Bound given by the weight (Lemma dual): B(a) = a * sup_{t' in tau R_{k-1}} I(a, t'),
  I(a, t') = int_0^{L-T} n(u) / (a - S_A(u) + n(u) u) du,  T = |t'|,
  index j active at (t', u) iff T + u - t'_j <= tau  (index m itself always active),
  n = 1 + #active j, S_A = u + sum_{active j} t'_j, so the denominator is a - sum_{A} t'_j + (n-1) u.
Exact piecewise integration (logs). Floating point: a search, NOT a certificate.
usage: psi_weight_fibers.py [search|grid]"""
import sys
import numpy as np
from math import log
from scipy.optimize import minimize

k, eps = 50, 1 / 25
L, tau = 1 + eps, 1 - eps
SCALING = (1 + eps) * k / (k - 1) * log(k)


def I(a, x):
    x = np.sort(np.asarray(x, float))[::-1]          # descending
    T = x.sum()
    if T > tau + 1e-14 or (x < -1e-15).any():
        return -np.inf
    U = L - T
    drop = x + tau - T                                  # index j inactive for u > drop[j]
    cuts = sorted(set([0.0, U] + [d for d in drop if 0 < d < U]))
    tot = 0.0
    for lo, hi in zip(cuts, cuts[1:]):
        mid = 0.5 * (lo + hi)
        act = drop >= mid
        n = 1 + act.sum()
        c = a - x[act].sum()
        if n == 1:
            tot += (hi - lo) / c
        else:
            tot += n / (n - 1) * log((c + (n - 1) * hi) / (c + (n - 1) * lo))
    return tot


def x_of(p):
    # p[0] -> total scale in [0, tau], p[1:] -> simplex weights
    s = tau / (1 + np.exp(-p[0]))
    w = np.exp(p[1:] - p[1:].max())
    return s * w / w.sum()


def best_fiber(a, starts=40, rng=np.random.default_rng(1)):
    best, bx = -1, None
    for it in range(starts):
        r = rng.integers(1, k)
        p0 = np.concatenate([[rng.normal(0, 2)], rng.normal(0, 1, k - 1) + np.where(np.arange(k - 1) < r, 3, -3)])
        res = minimize(lambda p: -I(a, x_of(p)), p0, method="Nelder-Mead" if it % 2 else "Powell",
                       options={"maxiter": 20000, "xatol": 1e-10, "fatol": 1e-13})
        v = -res.fun
        if v > best:
            best, bx = v, x_of(res.x)
    return best, bx


def equal_fiber(a):
    best = (0, None)
    for r in range(0, k):
        for x in (np.linspace(0, tau / max(r, 1), 400)[1:] if r else [0.0]):
            v = I(a, [x] * r + [0.0] * (k - 1 - r))
            if v > best[0]:
                best = (v, (r, x))
    return best


def main1():
    for a in [1.030, 1.035, 1.037, 1.040, 1.045]:
        ve, arg = equal_fiber(a)
        vb, bx = best_fiber(a)
        bx = np.sort(bx)[::-1]
        print("a=%.3f equal-fiber bound %.6f (r=%d x=%.4f); general search bound %.6f; scaling %.6f"
              % (a, a * ve, arg[0], arg[1], a * vb, SCALING), flush=True)
        print("   best x (top 14):", np.round(bx[:14], 4), " T=%.4f" % bx.sum(), flush=True)


def local_refine(a, r, x, trials=30, rng=np.random.default_rng(7)):
    """Perturb the equal fiber (x [r], y [m], 0...) and coordinate-ascend."""
    base = np.array([x] * r + [0.0] * (k - 1 - r))
    best = I(a, base); bx = base.copy()
    for t in range(trials):
        cur = bx + rng.normal(0, 0.01, k - 1) * (rng.random(k - 1) < 0.3)
        cur = np.clip(cur, 0, None)
        if cur.sum() > tau: cur *= tau / cur.sum()
        v = I(a, cur)
        step = 0.01
        while step > 1e-6:
            improved = False
            for j in range(k - 1):
                for d in (step, -step):
                    c2 = cur.copy(); c2[j] = max(0.0, c2[j] + d)
                    v2 = I(a, c2)
                    if v2 > v + 1e-15:
                        cur, v, improved = c2, v2, True
            if not improved: step /= 2
        if v > best: best, bx = v, cur
    return best, bx


def two_level(a, xs=np.linspace(0.0, 0.25, 51)):
    best = (0, None)
    for r1 in range(1, 16):
        for r2 in range(0, 49 - r1):
            for x in xs[1:]:
                if r1 * x > tau: break
                for y in xs[:np.searchsorted(xs, x) + 1]:
                    if r1 * x + r2 * y > tau: break
                    v = I(a, [x] * r1 + [y] * r2 + [0.0] * (k - 1 - r1 - r2))
                    if v > best[0]: best = (v, (r1, x, r2, y))
    return best


def main2():
    for a in [1.036, 1.037, 1.038]:
        ve, (r, x) = equal_fiber(a)
        vl, bx = local_refine(a, r, x, trials=6)
        v2, arg2 = two_level(a)
        print("a=%.3f equal %.6f | local-refined %.6f (T=%.4f, %d nonzero) | two-level %.6f %s | scaling %.6f"
              % (a, a * ve, a * vl, bx.sum(), (bx > 1e-9).sum(), a * v2, arg2, SCALING), flush=True)
        print("   refined top:", np.round(np.sort(bx)[::-1][:13], 4), flush=True)


if __name__ == "__main__":
    (main2 if "refine" in sys.argv else main1)()
