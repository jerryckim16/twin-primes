"""Exploration (Heuristic, floating point): lower bounds for the PM8b Thm 3.14 ratio at k = 3,
   sup 3*J_{1,1-eps}(F)/I(F) over symmetric F on (3/2)R_3 with the vanishing marginal condition
   (int F dt_i = 0 whenever sum_{j != i} t_j > 1+eps), piecewise constant on cubes of side 1/n.
   Cells: fully inside {sum <= 3/2}. J: only (t_j,t_l)-cells fully inside {sum <= 1-eps} (valid lower bound).
   Marginal condition imposed on every (t_j,t_l)-cell that meets {sum > 1+eps}.
   Run: /usr/bin/python3 code/explore/k3_thm314_grid.py [eps] [n ...]
"""
import sys, itertools, numpy as np, scipy.linalg as sl
eps = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
ns = [int(a) for a in sys.argv[2:]] or [6, 8, 10, 12]
for n in ns:
    h = 1.0/n; L = int(1.5*n + 1e-9)
    cells = [c for c in itertools.product(range(L), repeat=3) if sum(c) + 3 <= 1.5*n + 1e-9]
    orb = sorted({tuple(sorted(c)) for c in cells}); oi = {o: a for a, o in enumerate(orb)}
    P = np.zeros((len(cells), len(orb)))
    for r, c in enumerate(cells): P[r, oi[tuple(sorted(c))]] = 1
    # marginal along axis 0 (t_1 integrated): group cells by (c1, c2)
    groups = {}
    for r, c in enumerate(cells): groups.setdefault((c[1], c[2]), []).append(r)
    Jq = np.zeros((len(cells), len(cells))); C = []
    for (j, l), rs in groups.items():
        v = np.zeros(len(cells)); v[rs] = h
        if (j + l + 2)*h <= 1 - eps + 1e-12: Jq += h*h*np.outer(v, v)
        if (j + l + 2)*h > 1 + eps + 1e-12: C.append(v)
    A = (P.T @ P)*h**3; B = 3*(P.T @ Jq @ P)   # symmetric F: J_1 = J_2 = J_3
    if C:
        Cm = np.array(C) @ P; Nn = sl.null_space(Cm); A = Nn.T @ A @ Nn; B = Nn.T @ B @ Nn
    w = sl.eigh(B, A, eigvals_only=True)[-1]
    print(f"eps={eps} n={n} cells={len(cells)} orbits={len(orb)} ratio>= {w:.6f}", flush=True)
