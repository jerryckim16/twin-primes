"""Exploration (Heuristic, floating point). k = 3, PM8b Thm 3.14 class, cube grid as in code/parity/k3_thm314_dual.py.
Question: is the marginal f_1 of the (grid) extremal constant on the J-region {t2+t3 <= 1-eps}, as at k = 2
(where f = 1 on [0, 1-eps])? Also: the best F whose marginal is forced to be constant on the J-region, i.e.
minimise I subject to f_1 = 1 on J-columns and f_1 = 0 on constrained columns; ratio 3*|A|/I_min.
Run: /usr/bin/python3 code/explore/k3_extremal_marginal.py eps n
"""
import sys, itertools, numpy as np, scipy.linalg as sl
from collections import defaultdict
eps = float(sys.argv[1]); n = int(sys.argv[2]); h = 1.0/n; tol = 1e-12
orb = {}; size = defaultdict(int); cells = []
for c in itertools.product(range(int(1.5*n)+1), repeat=3):
    if (sum(c)+3)*h <= 1.5+tol:
        o = tuple(sorted(c)); orb.setdefault(o, len(orb)); size[orb[o]] += 1; cells.append(c)
N = len(orb); A = np.array([size[o] for o in range(N)], float)*h**3
cols = defaultdict(lambda: defaultdict(int))
for c in cells: cols[(c[1], c[2])][orb[tuple(sorted(c))]] += 1
Jv, Cv, Jkeys = [], [], []
for (j, l), d in cols.items():
    v = np.zeros(N); v[list(d)] = h*np.array(list(d.values()), float)
    if (j+l+2)*h <= 1-eps+tol: Jv.append(v); Jkeys.append((j, l))
    if (j+l+2)*h > 1+eps+tol: Cv.append(v)
Jv = np.array(Jv); Cv = np.array(Cv)
B = 3*h*h*Jv.T @ Jv
Nn = sl.null_space(Cv); w, U = sl.eigh(Nn.T @ B @ Nn, Nn.T @ np.diag(A) @ Nn)
x = Nn @ U[:, -1]; f = Jv @ x; f = f/np.mean(f)
print(f"eps={eps} n={n}: extremal ratio {w[-1]:.6f}; marginal on J-columns: mean 1, min {f.min():.4f}, max {f.max():.4f}, "
      f"rel std {np.std(f):.4f}")
# constant-marginal problem: min x^T diag(A) x  s.t.  Jv x = 1, Cv x = 0   (minimum-norm solution)
M = np.vstack([Jv, Cv]); rhs = np.concatenate([np.ones(len(Jv)), np.zeros(len(Cv))])
Ai = 1/A; G = (M*Ai) @ M.T; lam = np.linalg.lstsq(G, rhs, rcond=None)[0]; xc = Ai*(M.T @ lam)
res = np.abs(M @ xc - rhs).max(); Ic = xc @ (A*xc); Jc = 3*h*h*np.sum((Jv @ xc)**2)
print(f"  constant-marginal F: ratio {Jc/Ic:.6f} (residual {res:.1e})")
# profile of the extremal marginal along the diagonal t2 = t3 and along t3 = 0
prof = {k: v for k, v in zip(Jkeys, f)}
print("  f_1 along t3=0:", " ".join(f"{prof[(j,0)]:.3f}" for j in range(n) if (j, 0) in prof))
print("  f_1 along t2=t3:", " ".join(f"{prof[(j,j)]:.3f}" for j in range(n) if (j, j) in prof))
