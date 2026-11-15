"""Heuristic numerical lower bounds for the PM8b Thm 3.14 functional at k = 2:
   sup 2*int_{t1<=1-eps} (int F dt2)^2 dt1 / int F^2, F symmetric on {t1+t2<=2},
   with int F(t1,t2) dt2 = 0 whenever t1 > 1+eps.  Parity (PM8b sec. 8) predicts <= 2 (DHL[2,2] unprovable).
   Piecewise-constant F on an n-per-unit grid (cells inside the triangle); floating point, NOT a certificate.
   Run: python3 code/parity/k2_thm314_numeric.py
"""
import numpy as np, scipy.linalg as sl, sys
def best(n, eps):
    h = 1.0/n; cells = [(i, j) for i in range(2*n) for j in range(2*n) if i + j + 2 <= 2*n]
    # symmetric parametrisation: variable per unordered pair
    pairs = sorted({(min(i,j), max(i,j)) for i, j in cells}); idx = {p: a for a, p in enumerate(pairs)}
    P = np.zeros((len(cells), len(pairs)))
    for r, (i, j) in enumerate(cells): P[r, idx[(min(i,j), max(i,j))]] = 1
    rows = {}
    for r, (i, j) in enumerate(cells): rows.setdefault(i, []).append(r)
    Iq = h*h*np.eye(len(cells))
    Jq = np.zeros((len(cells), len(cells)))
    C = []
    for i, rs in rows.items():
        v = np.zeros(len(cells)); v[rs] = h
        if (i+1)*h <= 1 - eps + 1e-12: Jq += 2*h*np.outer(v, v)
        if i*h >= 1 + eps - 1e-12: C.append(v)
    A = P.T @ Iq @ P; B = P.T @ Jq @ P
    if C:
        Cm = np.array(C) @ P; Nn = sl.null_space(Cm); A = Nn.T @ A @ Nn; B = Nn.T @ B @ Nn
    return sl.eigh(B, A, eigvals_only=True)[-1]
for eps in (0.1, 0.25, 0.5, 0.9):
    print(eps, [round(best(n, eps), 5) for n in (8, 16, 24)]); sys.stdout.flush()
print("finer grids, full precision:")
for n, eps in ((32, 0.3), (30, 0.2), (28, 0.5)):
    print(n, eps, repr(best(n, eps)))
print("without the vanishing marginal condition (general, non-symmetric F), n = 8:")
def unconstrained(n, eps):
    h = 1.0/n; cells = [(i, j) for i in range(2*n) for j in range(2*n) if i + j + 2 <= 2*n]
    Jq = np.zeros((len(cells), len(cells)))
    for axis in (0, 1):
        for i in range(2*n):
            v = np.array([h if c[axis] == i else 0.0 for c in cells])
            if (i+1)*h <= 1 - eps + 1e-12: Jq += h*np.outer(v, v)
    return sl.eigh(Jq, h*h*np.eye(len(cells)), eigvals_only=True)[-1]
for eps in (0.0, 0.1):
    print("  eps", eps, "ratio", repr(unconstrained(8, eps)))
