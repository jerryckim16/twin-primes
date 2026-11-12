#!/usr/bin/env python3
"""Independent check of the epsilon-enlarged Gram matrices of mk_general.py (Session 4).

For small k and degree, integrates every basis product directly with sympy (iterated exact
integration over (1+eps)R_k and over the marginal region (1-eps)R_{k-1}), without Lemma 3 or the
binomial rewrite, and compares with mk_general.build entry by entry.

usage: check_eps_sympy.py k D p/q [--even]
"""
import sys
import sympy as sp
sys.path.insert(0, "code")
import mk_general as mg
from flint import fmpq

k, D = int(sys.argv[1]), int(sys.argv[2])
p, q = map(int, sys.argv[3].split("/"))
mg.EVEN_ONLY = "--even" in sys.argv
eps = sp.Rational(p, q); L, tau = 1 + eps, 1 - eps
basis, I, J = mg.build(k, D, fmpq(p, q))
t = sp.symbols("t1:%d" % (k + 1), nonnegative=True)
P = lambda j: sum(x ** j for x in t)
def F(a, b):
    f = (L - P(1)) ** a
    for idx, m in enumerate(b): f *= P(idx + 2) ** m
    return sp.expand(f)
def simplex_int(expr, vars_, R):
    # integrate over {vars >= 0, sum vars <= R}, innermost variable last
    for i in range(len(vars_) - 1, -1, -1):
        upper = R - sum(vars_[:i])
        expr = sp.integrate(expr, (vars_[i], 0, upper))
    return sp.expand(expr)
Fs = [F(a, b) for a, b in basis]
bad = 0
for x in range(len(basis)):
    for y in range(x, len(basis)):
        Ixy = simplex_int(Fs[x] * Fs[y], list(t), L)
        # J: marginal in t_k over [0, L - (t1+..+t_{k-1})], squared-product, over (1-eps)R_{k-1}
        mx = sp.integrate(Fs[x], (t[-1], 0, L - sum(t[:-1])))
        my = sp.integrate(Fs[y], (t[-1], 0, L - sum(t[:-1])))
        Jxy = simplex_int(sp.expand(mx * my), list(t[:-1]), tau)
        ok = (sp.Rational(str(I[x, y])) == Ixy) and (sp.Rational(str(J[x, y])) == Jxy)
        bad += not ok
print("k=%d D=%d eps=%s: %d basis functions, %d mismatches" % (k, D, sys.argv[3], len(basis), bad))
