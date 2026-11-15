"""Heuristic (floating point). Perron eigenvalue of the 2D operator K on Delta_a = {x,y >= 0, x+y <= a}, a = 1-eps:
  (Kg)(x,y) = (3/2-x-y) g(x,y) + int_0^{min(3/2-x-y, a-y)} g(t,y) dt + int_0^{min(3/2-x-y, a-x)} g(t,x) dt   (g symmetric).
Its top eigenvalue equals the supremum of 3 J_{1,1-eps}/I over F on (3/2)R_3 WITHOUT the vanishing marginal condition
(the Schur/weighted Cauchy-Schwarz reduction in the parity paper). Discretisation: g piecewise constant on squares of
side a/n (cells cut by x+y = a counted with their exact area fraction), line integrals by exact overlap lengths.
Run: /usr/bin/python3 code/parity/k3_unc_kernel.py eps n [n ...]
"""
import sys, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
eps = float(sys.argv[1]); a = 1-eps; c = 1.5
for n in map(int, sys.argv[2:]):
    h = a/n
    idx = {}; cells = []
    for i in range(n):
        for j in range(n-i):
            idx[(i, j)] = len(cells); cells.append((i, j))
    N = len(cells); w = np.array([h*h if i+j < n-1 else h*h/2 for i, j in cells])   # diagonal cells are half
    rows, cols, vals = [], [], []
    def seg(lo, hi, j):   # integral over t in [lo,hi] of g(t, y-cell j): overlap lengths with cells (k, j)
        out = []
        for k in range(n-j):
            L = max(0.0, min(hi, (k+1)*h) - max(lo, k*h))
            if L > 0: out.append((idx[(k, j)], L))
        return out
    for r, (i, j) in enumerate(cells):
        x, y = (i+0.5)*h, (j+0.5)*h
        if i+j == n-1: x, y = (i+1/3)*h, (j+1/3)*h          # centroid of the half cell
        L = c-x-y
        rows.append(r); cols.append(r); vals.append(L)
        for (q, ln) in seg(0, min(L, a-y), j): rows.append(r); cols.append(q); vals.append(ln)
        for (q, ln) in seg(0, min(L, a-x), i): rows.append(r); cols.append(q); vals.append(ln)
    K = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))
    # K is self-adjoint w.r.t. the 3D measure, not plainly symmetric here; use the non-symmetric Perron eigenvalue
    lam, v = spla.eigs(K, k=1, which='LR')
    print(f"eps={eps} n={n} cells={N} lambda={lam[0].real:.6f}", flush=True)
