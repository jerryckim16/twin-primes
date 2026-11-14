#!/usr/bin/env python3
"""Session 15 (own idea, FC3): rigorous (arb ball) value of the psi-weight bound RESTRICTED to the fibers
t' = ((2 eps)^r, 0^{k-1-r}), r = 0..k-1 (k = 50, eps = 1/25):
  I_r(a) = int_0^{u0} k/(a - T + (k-1)u) du + int_{u0}^{U} (1+r)/(a - T + r u) du,
  T = 2 eps r, U = L - T = 2 eps... , u0 = max(0, min(U, tau - T))   (zeros active iff u <= tau - T;
  the r coordinates equal to 2 eps = L - tau stay active on the whole fiber).
Prints a * max_r I_r(a) at rational a. This is the bound the weight gives IF the supremum over all fibers is
attained on these fibers (not proved; see notes/explorations.md, Session 15)."""
from flint import arb, fmpq, ctx
ctx.prec = 200
k = 50
eps = fmpq(1, 25); L = 1 + eps; tau = 1 - eps

def A(q): return arb(q.p) / arb(q.q)

def Ir(a, r):
    T = 2 * eps * r; U = L - T
    u0 = max(fmpq(0), min(U, tau - T))
    a_, T_ = A(a), A(T)
    tot = arb(0)
    if u0 > 0:
        tot += arb(k) / (k - 1) * ((a_ - T_ + (k - 1) * A(u0)) / (a_ - T_)).log()
    if r == 0:
        tot += (A(U) - A(u0)) / (a_ - T_)
    else:
        tot += arb(1 + r) / r * ((a_ - T_ + r * A(U)) / (a_ - T_ + r * A(u0))).log()
    return tot

def bound(a):
    vals = [(Ir(a, r), r) for r in range(k) if 2 * eps * r <= tau]
    best = max(vals, key=lambda t: t[0].mid())
    return A(a) * best[0], best[1]

if __name__ == "__main__":
    scal = A(1 + eps) * arb(k) / (k - 1) * arb(k).log()
    print("scaling (1+eps) k/(k-1) log k =", scal.str(12))
    best = None
    for num in range(10300, 10450, 2):
        a = fmpq(num, 10000)
        b, r = bound(a)
        if best is None or b.mid() < best[0].mid(): best = (b, a, r)
    b, a, r = best
    print("best a on grid 1e-4*2:", a, " bound", b.str(12), " binding r =", r)
    print("restricted bound at a =", a, "lies in", b.str(15), "; below scaling (rigorous ball comparison):", bool(b < scal))
