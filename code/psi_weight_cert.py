#!/usr/bin/env python3
"""Second, independent certificate (Session 15) for the psi-weight bound at (k, eps) = (50, 1/25).
Reduction (paper Prop. prop:psi-reduction, Proved here): for every fiber t',
  I(a, t') <= G_a(s, nu) = F(s) + int_0^W nu/(c0 + nu s + (nu-1) w) dw,
  F(s) = k/(k-1) log((c0 + k s)/(c0 + s)),  W = 2 eps,  c0 = a - tau,
over R = {0 <= s <= tau, 1 <= nu, (nu-1) W <= tau - s}.
Cell bound on [s1,s2] x [n1,n2]: F increasing in s; integrand decreasing in s; d/dnu integrand has the sign of c0 - w.
  G <= F(s2) + int_0^{min(c0,W)} [nu=n2, s=s1] + int_{min(c0,W)}^W [nu=n1, s=s1].
Arithmetic: python-flint arb balls (independent of the helper's mpmath.iv script code/explore/psi_scratch_certify.py);
cells are exact rationals (fmpq), subdivided by my own breadth-first bisection.
usage: psi_weight_cert.py A_NUM A_DEN THETA_NUM THETA_DEN   -> certifies a * sup_R G_a < theta"""
import sys
from flint import arb, fmpq, ctx
ctx.prec = 128
k = 50
eps = fmpq(1, 25); W = 2 * eps; tau = 1 - eps

def A(q): return arb(q.p) / arb(q.q)

def seg(nu, s, c0, lo, hi):
    """int_lo^hi nu/(c0 + nu s + (nu-1) w) dw, all arb."""
    if hi <= lo: return arb(0)
    base = c0 + nu * s
    if nu == 1:  # exact rational nu = 1 only
        return (hi - lo) / base
    return nu / (nu - 1) * ((base + (nu - 1) * hi) / (base + (nu - 1) * lo)).log()

def cell_bound(c0, s1, s2, n1, n2):
    w0 = min(c0, W)
    c0a, s1a, s2a = A(c0), A(s1), A(s2)
    F = arb(k) / (k - 1) * ((c0a + k * s2a) / (c0a + s2a)).log()
    return F + seg(A(n2) if n2 != 1 else 1, s1a, c0a, arb(0), A(w0)) + seg(A(n1) if n1 != 1 else 1, s1a, c0a, A(w0), A(W))

def certify(a, theta):
    c0 = a - tau
    assert c0 > 0
    aA, th = A(a), A(theta)
    numax = 1 + tau / W           # = 13
    queue = [(fmpq(0), tau, fmpq(1), numax)]
    leaves = 0; worst = None
    while queue:
        s1, s2, n1, n2 = queue.pop()
        if (n1 - 1) * W > tau - s1:      # empty intersection with R (exact rational test)
            continue
        b = aA * cell_bound(c0, s1, s2, n1, n2)
        if b < th:
            leaves += 1
            if worst is None or b.upper() > worst: worst = b.upper()
            continue
        if s2 - s1 < fmpq(1, 10**9):
            raise SystemExit("FAIL: cell [%s,%s]x[%s,%s] bound %s" % (s1, s2, n1, n2, b.str(10)))
        # bisect the longer side in relative terms
        if (s2 - s1) / tau >= (n2 - n1) / numax:
            m = (s1 + s2) / 2; queue += [(s1, m, n1, n2), (m, s2, n1, n2)]
        else:
            m = (n1 + n2) / 2; queue += [(s1, s2, n1, m), (s1, s2, m, n2)]
    return leaves, worst

if __name__ == "__main__":
    a = fmpq(int(sys.argv[1]), int(sys.argv[2])); theta = fmpq(int(sys.argv[3]), int(sys.argv[4]))
    leaves, worst = certify(a, theta)
    print("a = %s: a * sup_R G_a < %s CERTIFIED (%d leaf cells; largest leaf upper bound %s)" % (a, theta, leaves, worst.str(12)))
