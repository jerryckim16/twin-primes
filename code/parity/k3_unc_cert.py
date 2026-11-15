"""Computed (rigorous, arb ball arithmetic). Certificate that the k = 3 Theorem 3.14 ratio, even WITHOUT the vanishing
marginal condition, is at most C at eps (1/4 <= eps < 1/2), via the 1D Schur condition of the parity paper
(Prop. prop:unc-ceiling): phi >= 0 on [0,a], phi > 0 on [0,a/2], a = 1-eps, mu = C - 3/2 > 0, and
   Phi(y) := int_0^{a-y} (phi(t)+phi(y))/(mu+t+y) dt <= phi(y)   for all y in [0,a].
phi: piecewise linear with rational values at the nodes k a/N (the numerical Perron vector of the 1D operator plus a
small constant, rounded to rationals). Check on boxes [y0,y1] (adaptive bisection): for y in the box, the integrand is
non-negative and decreasing in y, so Phi(y) <= Phi+ := int_0^{a-y0} (phi(t)+max_box phi)/(mu+t+y0) dt, computed exactly
in closed form (linear pieces: int (al+be t)/(s+t) = be*len + (al - be s) log(...)) with arb balls; require
upper(Phi+) < lower(min_box phi). Writes code/parity/k3_unc_cert_<p>_<q>.json.
Run: /usr/bin/python3 -I code/parity/k3_unc_cert.py eps_p eps_q C_p C_q [N] [delta]
"""
import sys, json, numpy as np, flint
from fractions import Fraction as Fr
ep, eq, Cp, Cq = map(int, sys.argv[1:5]); N = int(sys.argv[5]) if len(sys.argv) > 5 else 200
delta = float(sys.argv[6]) if len(sys.argv) > 6 else 1e-3
eps = Fr(ep, eq); C = Fr(Cp, Cq); a = 1-eps; mu = C-Fr(3, 2)
assert Fr(1, 4) <= eps < Fr(1, 2) and mu > 0
af, muf = float(a), float(mu); ys = np.linspace(0, af, N+1); h = af/N
K = np.zeros((N+1, N+1))
for r, y in enumerate(ys):
    s = muf+y
    for k in range(N):
        lo, hi = k*h, min((k+1)*h, af-y)
        if hi <= lo: break
        I0 = np.log((s+hi)/(s+lo)); I1 = (hi-lo)-s*I0; tk = k*h
        K[r, k] += ((tk+h)*I0-I1)/h; K[r, k+1] += (I1-tk*I0)/h
    K[r] /= (1-np.log((muf+af)/(muf+y)))
w, V = np.linalg.eig(K); i = np.argmax(w.real); v = np.abs(V[:, i].real); v /= v.max()
print(f"numerical spectral radius at mu={muf:.6f}: {w[i].real:.8f}", flush=True)
vals = [Fr(float(x)+delta).limit_denominator(10**9) for x in v]      # node values phi(k a/N)
nodes = [a*k/N for k in range(N+1)]
flint.ctx.prec = 128
ar = lambda q: flint.arb(q.numerator)/q.denominator
MU, A = ar(mu), ar(a)
def phi_at(y):          # exact rational value at rational y
    k = min(int(y/a*N), N-1); t0 = nodes[k]
    return vals[k]+(vals[k+1]-vals[k])*(y-t0)*N/a
def box_minmax(y0, y1):
    pts = [phi_at(y0), phi_at(y1)]+[vals[k] for k in range(N+1) if y0 < nodes[k] < y1]
    return min(pts), max(pts)
def Phi_plus(y0, pmax):
    s = MU+ar(y0); T = a-y0; tot = flint.arb(0)
    for k in range(N):
        lo, hi = nodes[k], min(nodes[k+1], T)
        if hi <= lo: break
        be = (vals[k+1]-vals[k])*N/a; al = vals[k]-be*nodes[k]
        tot += ar(be)*ar(hi-lo)+(ar(al)-ar(be)*s)*((s+ar(hi))/(s+ar(lo))).log()
    return tot+ar(pmax)*((s+ar(T))/s).log()
stack = [(Fr(0), a*m/64, a*(m+1)/64) for m in range(64)]; nbox = 0; worst = None; depth_max = 0; fail = False
stack = [(0, y0, y1) for (_, y0, y1) in stack]
while stack:
    d, y0, y1 = stack.pop()
    pmin, pmax = box_minmax(y0, y1)
    ok = pmin > 0 or (y0 >= a/2 and pmin >= 0)
    up = Phi_plus(y0, pmax)
    if ok and up.upper() < ar(pmin).lower():
        nbox += 1; gap = float((ar(pmin)-up).mid()); worst = gap if worst is None or gap < worst else worst
        depth_max = max(depth_max, d); continue
    if d >= 30: fail = True; print("FAIL at box", float(y0), float(y1)); break
    m = (y0+y1)/2; stack += [(d+1, y0, m), (d+1, m, y1)]
print(f"eps={eps} C={C} N={N}: boxes={nbox}, max depth={depth_max}, smallest margin={worst:.3e}, CERTIFIED: {not fail}")
if not fail:
    json.dump({"label": "Computed (rigorous, arb ball arithmetic)", "eps": f"{eps}", "C": f"{C}", "mu": f"{mu}", "N": N,
               "phi_node_values": [f"{x}" for x in vals],
               "statement": "phi piecewise linear with these values at k(1-eps)/N; phi > 0; int_0^{a-y}(phi(t)+phi(y))/(mu+t+y)dt <= phi(y) on [0,a]; hence the k = 3 Thm 3.14 ratio is <= C at this eps and at every larger eps < 1/2"},
              open(f"code/parity/k3_unc_cert_{ep}_{eq}.json", "w"), indent=1)
