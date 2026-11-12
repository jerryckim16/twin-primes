#!/usr/bin/env python3
"""Weighted pigeonhole on the epsilon-enlarged simplex (Polymath8b, Thm 3.12).

For F supported on (1+eps)R_k (no symmetry imposed) and weights c >= 0,
    M_{k,eps}[c] = sup_F  sum_m c_m J_{m,1-eps}(F) / I(F),
    I(F)          = int_{(1+eps)R_k} F^2,
    J_{m,1-eps}(F)= int_{(1-eps)R_{k-1}} ( int_0^oo F dt_m )^2 dt_{-m}.
(For points of (1-eps)R_{k-1} the inner integral runs over 0 <= t_m <= 1+eps-|t_{-m}|.)

Test functions: span of  t^alpha * 1[|t| <= r]  for |alpha| <= deg and r in a
list of radii (all <= 1+eps).  Every Gram entry is an exact rational:
  * I-entries: int_{rR_k} t^gamma = r^{k+|gamma|} prod(gamma!)/(k+|gamma|)!.
  * J-entries: with x = t_{-m}, s = |x|, the inner integral of t^alpha 1[|t|<=r]
    is x^alpha' (r-s)_+^{a+1}/(a+1), and for d = k-1 variables
        int_{rho R_d} x^gamma g(|x|) dx = prod(gamma!)/(|gamma|+d-1)! * int_0^rho s^{|gamma|+d-1} g(s) ds,
    so each entry is a one-variable polynomial integral over 0 <= s <= min(1-eps, r1, r2).
The top generalized eigenvalue of (B, A) is a rigorous LOWER bound for M_{k,eps}[c]
(up to the final floating-point eigen-solve at 60 digits).

Proposition (enlarged rigidity, notes/enlarged-rigidity.md):
    M_{k,eps}[1_K] = M_{|K|,eps}, and M_{k,eps}[c] <= alpha_D(c) M_{omega,eps}.
So for k = 3 we expect  M_{3,eps}[(1,1,0)] <= M_{2,eps}  and
M_{3,eps}[(1/2,1,1/2)] <= M_{2,eps}  (cliques of (0,1,2) at D = 1 are {0,1},{1,2},
alpha_1((1/2,1,1/2)) = 1).

Usage: python3 enlarged_pigeonhole.py [deg3] [deg2]
"""
import itertools, sys, time
from fractions import Fraction as Fr
from math import factorial, comb
from functools import lru_cache
import mpmath as mp

mp.mp.dps = 60


def monomials(k, deg):
    return [m for m in itertools.product(range(deg + 1), repeat=k) if sum(m) <= deg]


def dir_coef(g, d):
    """prod(g!)/(|g|+d-1)!  (radial reduction constant on d-simplex)."""
    num = 1
    for e in g:
        num *= factorial(e)
    return Fr(num, factorial(sum(g) + d - 1))


def ipow(r, n):
    return r ** n


@lru_cache(maxsize=None)
def poly_int(p, q, w, r1, r2, L):
    """int_0^L s^p (r1-s)^q (r2-s)^w ds, exact."""
    tot = Fr(0)
    for i in range(q + 1):
        ci = comb(q, i) * r1 ** (q - i) * (-1) ** i
        for j in range(w + 1):
            cj = comb(w, j) * r2 ** (w - j) * (-1) ** j
            e = p + i + j
            tot += ci * cj * L ** (e + 1) / (e + 1)
    return tot


def build(k, deg, eps, radii):
    """Exact Gram matrices: A (for I), Js[m] (for J_{m,1-eps})."""
    mons = monomials(k, deg)
    basis = [(r, a) for r in radii for a in mons]
    n = len(basis)
    d = k - 1
    A = [[None] * n for _ in range(n)]
    for u, (r1, a) in enumerate(basis):
        for v in range(u, n):
            r2, b = basis[v]
            g = [x + y for x, y in zip(a, b)]
            r = min(r1, r2)
            num = 1
            for e in g:
                num *= factorial(e)
            A[u][v] = A[v][u] = Fr(num, factorial(k + sum(g))) * r ** (k + sum(g))
    Js = []
    for m in range(k):
        J = [[None] * n for _ in range(n)]
        for u, (r1, a) in enumerate(basis):
            am = a[m]; ao = tuple(a[i] for i in range(k) if i != m)
            for v in range(u, n):
                r2, b = basis[v]
                bm = b[m]; bo = tuple(b[i] for i in range(k) if i != m)
                g = tuple(x + y for x, y in zip(ao, bo))
                L = min(1 - eps, r1, r2)
                if L <= 0:
                    val = Fr(0)
                elif d == 0:   # k = 1: no outer integral
                    val = Fr(r1 ** (am + 1) * r2 ** (bm + 1), (am + 1) * (bm + 1))
                else:
                    val = dir_coef(g, d) * poly_int(sum(g) + d - 1, am + 1, bm + 1, r1, r2, L) / ((am + 1) * (bm + 1))
                J[u][v] = J[v][u] = val
        Js.append(J)
    return basis, A, Js


def top_eig(A, Js, c):
    n = len(A)
    f = lambda q: mp.mpf(q.numerator) / q.denominator
    Am = mp.matrix(n, n); Bm = mp.matrix(n, n)
    for u in range(n):
        for v in range(n):
            Am[u, v] = f(A[u][v])
            Bm[u, v] = sum(mp.mpf(ci) * f(J[u][v]) for ci, J in zip(c, Js) if ci)
    L = mp.cholesky(Am)
    Li = mp.inverse(L)
    C = Li * Bm * Li.T
    C = (C + C.T) / 2
    E = mp.eigsy(C, eigvals_only=True)
    return max(E)


def radii_for(eps):
    # pieces supported on (1-eps)R, R, (1+eps)R (eps = 0 collapses to R)
    rs = sorted({1 - eps, Fr(1), 1 + eps})
    return [r for r in rs if r > 0]


if __name__ == "__main__":
    deg3 = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    deg2 = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    print("M_2 (eps=0, exact) = 1/(1-W(1/e)) =", mp.nstr(1 / (1 - mp.lambertw(1 / mp.e)), 12))
    for eps in (Fr(0), Fr(1, 10), Fr(1, 5), Fr(1, 3)):
        rad = radii_for(eps)
        t0 = time.time()
        _, A2, J2 = build(2, deg2, eps, rad)
        m2 = top_eig(A2, J2, (1, 1))
        _, A1, J1 = build(1, 6, eps, rad)
        m1 = top_eig(A1, J1, (1,))
        _, A3, J3 = build(3, deg3, eps, rad)
        res = {}
        for name, c in (("(1,1,1)", (1, 1, 1)), ("(1,1,0)", (1, 1, 0)),
                        ("(1/2,1,1/2)", (Fr(1, 2), 1, Fr(1, 2))), ("(1,0,1)", (1, 0, 1))):
            res[name] = top_eig(A3, J3, [float(x) for x in c])
        print("eps=%-5s radii=%s  [%.0fs]" % (eps, [str(r) for r in rad], time.time() - t0))
        print("   M_{1,eps} >= %s   (exact value 1+eps = %s)" % (mp.nstr(m1, 10), float(1 + eps)))
        print("   M_{2,eps} >= %s   (deg %d, %d basis fns)" % (mp.nstr(m2, 10), deg2, len(A2)))
        for name, val in res.items():
            print("   M_{3,eps}[%-11s] >= %s   (deg %d, %d basis fns)" % (name, mp.nstr(val, 10), deg3, len(A3)))
        sys.stdout.flush()
