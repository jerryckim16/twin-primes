"""Second check (Computed, exact) of code/parity/data/orth_relax_<p>_<q>_n<n>.json, written independently of the
orbit/Gram assembly: expands the symmetric vector to all cubes, recomputes each column marginal (sum over the cubes of
the column, direction 1 only) and I, J cell by cell, checks the marginal vanishes on every clean column in
{t2+t3 > 1+eps, min(t2,t3) >= 1/2-eps} for ALL THREE directions, and that every cube used lies inside D.
Run: /usr/bin/python3 -I code/parity/k3_orth_relax_verify.py code/parity/data/orth_relax_1_8_n32.json
"""
import sys, json, itertools
from fractions import Fraction as Fr
d = json.load(open(sys.argv[1])); eps = Fr(d['eps']); n = d['n']; h = Fr(1, n)
co = {tuple(map(int, k.split(','))): Fr(v) for k, v in d['orbit_coef'].items()}
F = {}
for k, v in co.items():
    for c in set(itertools.permutations(k)):
        assert (sum(c)+3)*h <= Fr(3, 2); F[c] = v
I = sum(v*v for v in F.values())*h**3
J = Fr(0); bad = 0
for dirn in range(3):
    marg = {}
    for c, v in F.items():
        u = tuple(c[i] for i in range(3) if i != dirn); marg[u] = marg.get(u, 0) + v*h
    for (j, l), m in marg.items():
        if (j+l+2)*h <= 1-eps: J += m*m*h*h
        if (j+l+2)*h > 1+eps and min(j, l)*h >= Fr(1, 2)-eps and m != 0: bad += 1
r = J/I
print(f"eps={eps} n={n} cubes={len(F)} clean-column violations={bad} ratio={float(r):.9f} equals cert: {r == Fr(d['ratio'])}")
