"""Heuristic (floating point, NOT a certificate). PM8b Theorem 3.14 ratio at k = 3.
Lower bounds for sup 3*J_{1,1-eps}(F)/I(F) over symmetric F, piecewise constant on cubes of side 1/n
fully inside D = (3/2)R_3, with the vanishing marginal condition (int F dt_j = 0 when sum_{l != j} t_l > 1+eps)
imposed on every (t_l,t_m)-column that meets {t_l+t_m > 1+eps}.
mode 'full'   : all such columns constrained (the Theorem 3.14 class, restricted to the grid).
mode 'disj'   : only columns whose fibre meets no other constraint cylinder (min(t_l,t_m) >= 1/2-eps on the whole
                column cell): a RELAXATION (larger class), whose sup is >= the true sup. This is the analogue of the
                k = 2 situation, where all cylinders are disjoint.
mode 'none'   : no marginal condition (Theorem 3.12-type relaxation on the larger support).
Orbit-level sparse assembly (symmetric F). Run: /usr/bin/python3 code/parity/k3_thm314_dual.py eps mode n [n ...]
"""
import sys, itertools, numpy as np, scipy.linalg as sl
from collections import defaultdict
eps = float(sys.argv[1]); mode = sys.argv[2]; ns = [int(a) for a in sys.argv[3:]]
for n in ns:
    h = 1.0/n; tol = 1e-12
    # cells (c1,c2,c3), fully inside sum <= 3/2
    orb = {}; size = defaultdict(int)
    cells = []
    for c in itertools.product(range(int(1.5*n)+1), repeat=3):
        if (sum(c)+3)*h <= 1.5+tol:
            o = tuple(sorted(c));
            if o not in orb: orb[o] = len(orb)
            size[orb[o]] += 1; cells.append(c)
    N = len(orb)
    A = np.array([size[a] for a in range(N)], float)*h**3
    # marginal along axis 0: columns (c2,c3)
    cols = defaultdict(lambda: defaultdict(int))
    for c in cells: cols[(c[1], c[2])][orb[tuple(sorted(c))]] += 1
    B = np.zeros((N, N)); C = []
    lo = 0.5-eps
    for (j, l), d in cols.items():
        idx = np.array(list(d.keys())); cnt = np.array(list(d.values()), float)
        v = np.zeros(N); v[idx] = h*cnt          # P^T (h 1_column)
        if (j+l+2)*h <= 1-eps+tol: B += h*h*np.outer(v, v)
        if (j+l+2)*h > 1+eps+tol:
            if mode == 'full' or (mode == 'disj' and min(j, l)*h >= lo-tol):
                C.append(v)
    B *= 3
    Ad = np.diag(A)
    if C:
        Nn = sl.null_space(np.array(C)); Ad = Nn.T @ Ad @ Nn; B = Nn.T @ B @ Nn
    w = sl.eigh(B, Ad, eigvals_only=True)[-1]
    print(f"eps={eps} mode={mode} n={n} orbits={N} constraints={len(C)} ratio>= {w:.6f}", flush=True)
