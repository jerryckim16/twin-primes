"""Second, independent check of code/parity/k3_unc_cert_<p>_<q>.json (mpmath interval arithmetic; written separately from
k3_unc_cert.py and sharing no code with it). Re-checks, for the piecewise-linear phi in the file:
  (i) phi > 0 at every node (so phi > 0 on [0,a]);
  (ii) for every y in [0,a]: int_0^{a-y} (phi(t)+phi(y))/(mu+t+y) dt <= phi(y),
using boxes [y0,y1] from a uniform grid refined by bisection on failure, and on each box the bound
  Phi(y) <= sum over linear pieces of int (phi(t)+P)/(mu+y0+t) dt over [0, a-y0],   P = max phi on the box,
evaluated with the substitution v = mu+y0+t: int (alpha+beta*(v - s) + P)/v dv = beta*(v1-v0) + (alpha - beta*s + P)*log(v1/v0).
Run: /usr/bin/python3 -I code/parity/k3_unc_verify.py code/parity/k3_unc_cert_<p>_<q>.json
"""
import sys, json
from fractions import Fraction as Fr
from mpmath import iv, mp
iv.prec = 120
d = json.load(open(sys.argv[1])); eps = Fr(d['eps']); C = Fr(d['C']); mu = C-Fr(3, 2); a = 1-eps
assert Fr(d['mu']) == mu and Fr(1, 4) <= eps < Fr(1, 2) and mu > 0
vals = [Fr(x) for x in d['phi_node_values']]; N = len(vals)-1
assert all(v > 0 for v in vals), "phi not positive"
X = lambda q: iv.mpf([q.numerator, q.numerator])/q.denominator
def node(k): return a*k/N
def phi(y):
    k = min(int(y*N/a), N-1); return vals[k]+(vals[k+1]-vals[k])*(y-node(k))*N/a
def check(y0, y1):
    P = max([phi(y0), phi(y1)]+[vals[k] for k in range(N+1) if y0 < node(k) < y1])
    pmin = min([phi(y0), phi(y1)]+[vals[k] for k in range(N+1) if y0 < node(k) < y1])
    s = mu+y0; T = a-y0; tot = iv.mpf(0)
    for k in range(N):
        lo, hi = node(k), min(node(k+1), T)
        if hi <= lo: break
        beta = (vals[k+1]-vals[k])*N/a; alpha = vals[k]-beta*node(k)
        v0, v1 = s+lo, s+hi
        tot += X(beta*(v1-v0)) + X(alpha-beta*s+P)*iv.log(X(v1)/X(v0))
    return tot.b < X(pmin).a
boxes = 0; todo = [(a*m/(4*N), a*(m+1)/(4*N), 0) for m in range(4*N)]
while todo:
    y0, y1, dep = todo.pop()
    if check(y0, y1): boxes += 1; continue
    assert dep < 30, f"fails near {float(y0)}"
    m = (y0+y1)/2; todo += [(y0, m, dep+1), (m, y1, dep+1)]
print(f"{sys.argv[1]}: eps={eps} C={C} N={N}: verified on {boxes} boxes: the k = 3 Thm 3.14 ratio is <= {C} = {float(C)} for eps >= {float(eps)}")
