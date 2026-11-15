"""Computed (exact certificate). k = 3, PM8b Theorem 3.14 setting, ORTHOGONAL RELAXATION (paper, Lemma lem:dual(ii)).
Builds a symmetric F, piecewise constant on cubes of side h = 1/n fully inside D = (3/2)R_3, whose marginal in
direction 1 vanishes on every cell column (t2,t3) in {t2+t3 > 1+eps} with min(t2,t3) >= 1/2-eps (the 'clean'
columns, whose fibres meet no other constraint cylinder), and certifies EXACTLY (integers / fmpq) that
3 J_{1,1-eps}(F)/I(F) exceeds the printed bound. J is computed only on cell columns fully inside {t2+t3 <= 1-eps},
which only lowers J. Requires n with 1/2-eps, 1-eps, 1+eps multiples of 1/n.
Run: /usr/bin/python3 -I code/parity/k3_orth_relax_cert.py p q n     (eps = p/q)
"""
import sys, itertools, numpy as np, scipy.linalg as sl, flint
from fractions import Fraction as Fr
from collections import defaultdict
p, q, n = map(int, sys.argv[1:4]); eps = Fr(p, q); h = Fr(1, n)
lo, a, B = Fr(1, 2)-eps, 1-eps, 1+eps
for x in (lo, a, B): assert (x*n).denominator == 1, "grid not aligned"
orb = {}; size = defaultdict(int); cells = []
for c in itertools.product(range(2*n), repeat=3):
    if (sum(c)+3)*h <= Fr(3, 2):
        o = tuple(sorted(c)); orb.setdefault(o, len(orb)); size[orb[o]] += 1; cells.append(c)
N = len(orb)
cols = defaultdict(lambda: defaultdict(int))
for c in cells: cols[(c[1], c[2])][orb[tuple(sorted(c))]] += 1
Jcols, Ccols = [], []
for (j, l), d in cols.items():
    if (j+l+2)*h <= a: Jcols.append(d)
    if (j+l+2)*h > B and min(j, l)*h >= lo: Ccols.append(d)
# exact integer null space of the constraint matrix (column counts)
C = flint.fmpz_mat(len(Ccols), N, [d.get(o, 0) for d in Ccols for o in range(N)])
X, nul = C.nullspace()
Nn = np.array([[int(X[i, j]) for j in range(nul)] for i in range(N)], dtype=float)
# floating eigenvector in the null-space basis
S = np.array([size[o] for o in range(N)], float)
V = np.array([[d.get(o, 0) for o in range(N)] for d in Jcols], float)
Afl = (Nn.T * S) @ Nn; Bfl = 3*float(h)*(V @ Nn).T @ (V @ Nn)
w, U = sl.eigh(Bfl, Afl); y = U[:, -1]; y = y/np.max(np.abs(y))
yi = [int(round(v*10**6)) for v in y]
x = [sum(int(X[i, j])*yi[j] for j in range(nul)) for i in range(N)]
assert all(sum(d.get(o, 0)*x[o] for o in d) == 0 for d in Ccols)       # constraints hold exactly
I_int = sum(size[o]*x[o]**2 for o in range(N))                           # I = h^3 * I_int
J_int = sum(sum(d[o]*x[o] for o in d)**2 for d in Jcols)                # J_1 = h^4 * J_int
ratio = 3*h*Fr(J_int, I_int)
print(f"eps={eps} n={n} orbits={N} constraints={len(Ccols)} nullity={nul} float_max={w[-1]:.6f}")
print(f"exact ratio 3J/I = {ratio.numerator}/{ratio.denominator} = {float(ratio):.9f}")
for t in (Fr(2), Fr(209, 100), Fr(21, 10), Fr(212, 100), Fr(214, 100)):
    print(f"  ratio > {t}: {ratio > t}")
