#!/usr/bin/env python3
"""Exploration (heuristic, floating point): toy capped variational problem in dimension k = 2, 3.
Region T_c = {t >= 0, sum t <= 1, t_i <= c}.  For F a polynomial on T_c:
  I(F) = int_T F^2,   J(F) = sum_m int (int_{fibre} F dt_m)^2 d(others),  fibre = [0, min(c, 1 - sum others)].
ratio(F) = J/I  (k J_1 / I by symmetry).  Compare, in the space of polynomials of degree <= d:
  opt_free  = best ratio on the simplex (c = 1),
  trunc     = ratio of P_free * 1_T (the cap-free optimiser truncated),
  opt_T     = best ratio on T_c itself,
  regain    = (opt_T - trunc) / (opt_free - trunc).
Integrals by Delaunay simplices + collapsed Gauss quadrature (exact for the polynomial degrees used)."""
import itertools, sys, numpy as np
from scipy.spatial import Delaunay
from scipy.linalg import eigh
from scipy.optimize import linprog

def vertices(A, b):
    """vertices of {x : A x <= b} (small dimension, brute force)."""
    n = A.shape[1]; V = []
    for rows in itertools.combinations(range(len(A)), n):
        M = A[list(rows)]
        if abs(np.linalg.det(M)) < 1e-12: continue
        x = np.linalg.solve(M, b[list(rows)])
        if np.all(A @ x <= b + 1e-12): V.append(x)
    V = np.unique(np.round(np.array(V), 12), axis=0)
    return V

def simplex_rule(n, order):
    """quadrature on the unit n-simplex by collapsed (Duffy) Gauss-Jacobi; exact to degree 2*order-1."""
    from scipy.special import roots_jacobi
    pts1 = []
    for i in range(n):
        a = n - 1 - i                          # weight (1-x)^a
        x, w = roots_jacobi(order, a, 0); x = (x + 1) / 2; w = w / 2 ** (a + 1)
        pts1.append((x, w))
    P, W = [], []
    for idx in itertools.product(range(order), repeat=n):
        xs = [pts1[i][0][idx[i]] for i in range(n)]; ws = [pts1[i][1][idx[i]] for i in range(n)]
        y = np.zeros(n); rem = 1.0
        for i in range(n):
            y[i] = rem * xs[i]; rem *= (1 - xs[i])
        P.append(y); W.append(np.prod(ws))
    return np.array(P), np.array(W)

def poly_quad(A, b, order):
    """points/weights for integration over the polytope {A x <= b}."""
    V = vertices(A, b); n = A.shape[1]
    if len(V) <= n: return np.zeros((0, n)), np.zeros(0)
    tri = Delaunay(V); P0, W0 = simplex_rule(n, order); P, W = [], []
    for s in tri.simplices:
        v = V[s]; M = (v[1:] - v[0]).T; det = abs(np.linalg.det(M))
        if det < 1e-14: continue
        P.append(v[0] + P0 @ M.T); W.append(W0 * det)
    return np.vstack(P), np.concatenate(W)

def monos(k, d):
    return [a for a in itertools.product(range(d + 1), repeat=k) if sum(a) <= d]

def grams(k, d, c, order):
    ms = monos(k, d); E = np.array(ms)
    # I over T: A x <= b
    A = np.vstack([-np.eye(k), np.ones((1, k)), np.eye(k)]); b = np.concatenate([np.zeros(k), [1.0], c * np.ones(k)])
    P, W = poly_quad(A, b, order)
    Phi = np.prod(P[:, None, :] ** E[None, :, :], axis=2)
    GI = Phi.T @ (W[:, None] * Phi)
    # J_1 (fibre in t_1): others y in R^{k-1}, y <= c, sum y <= 1; U = min(c, 1 - sum y)
    GJ = np.zeros_like(GI); n = k - 1
    for piece in ("cap", "diag"):
        A2 = [-np.eye(n), np.eye(n), np.ones((1, n))]; b2 = [np.zeros(n), c * np.ones(n), [1.0]]
        if piece == "cap":  A2.append(np.ones((1, n))); b2.append([1 - c])          # sum y <= 1 - c: U = c
        else:               A2.append(-np.ones((1, n))); b2.append([-(1 - c)])      # sum y >= 1 - c: U = 1 - sum y
        A2 = np.vstack(A2); b2 = np.concatenate(b2)
        if n == 1: 
            lo = max(0.0, (1 - c) if piece == "diag" else 0.0); hi = min(c, (1 - c) if piece == "cap" else 1.0)
            if hi <= lo + 1e-14: continue
            x, w = np.polynomial.legendre.leggauss(order); Y = (lo + (hi - lo) * (x + 1) / 2)[:, None]; Wy = w * (hi - lo) / 2
        else:
            Y, Wy = poly_quad(A2, b2, order)
            if len(Wy) == 0: continue
        U = c * np.ones(len(Y)) if piece == "cap" else 1 - Y.sum(1)
        a1 = E[:, 0]; rest = E[:, 1:]
        Psi = (U[:, None] ** (a1[None, :] + 1) / (a1[None, :] + 1)) * np.prod(Y[:, None, :] ** rest[None, :, :], axis=2)
        GJ += Psi.T @ (Wy[:, None] * Psi)
    return ms, *symmetrise(ms, GI, GJ)

def symmetrise(ms, GI, GJ):
    """restrict to symmetric polynomials: basis = orbit sums of monomials (the true F is symmetric)."""
    k = len(ms[0]); orbits = sorted({tuple(sorted(a, reverse=True)) for a in ms})
    S = np.zeros((len(ms), len(orbits)))
    for i, a in enumerate(ms): S[i, orbits.index(tuple(sorted(a, reverse=True)))] = 1.0
    return S.T @ GI @ S, S.T @ GJ @ S

def best(GI, GJ):
    # symmetrise numerically: restrict to eigen-solve; regularise GI
    w, V = eigh(GJ, GI + 0 * np.eye(len(GI)))
    return w[-1], V[:, -1]

def run(k, d, cs, order=None):
    order = order or (d + 3)
    ms, GI1, GJ1 = grams(k, d, 1.0, order)
    r_free, v = best(GI1, GJ1)
    out = []
    for c in cs:
        _, GI, GJ = grams(k, d, c, order)
        trunc = (v @ GJ @ v) / (v @ GI @ v)
        r_T, _ = best(GI, GJ)
        reg = (r_T - trunc) / (r_free - trunc) if r_free - trunc > 1e-12 else float('nan')
        out.append((c, k * r_free, k * trunc, k * r_T, reg))
        print("k=%d d=%d c=%.3f  free %.6f  trunc %.6f  opt_T %.6f  loss %.2e  regain %.3f" % (k, d, c, k*r_free, k*trunc, k*r_T, k*(r_free-trunc), reg), flush=True)
    return out

if __name__ == "__main__":
    k = int(sys.argv[1]); d = int(sys.argv[2])
    cs = [float(x) for x in sys.argv[3].split(",")]
    run(k, d, cs)
