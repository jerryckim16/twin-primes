#!/usr/bin/env python3
"""Best dual weight of the form psi_m(t) = Psi(S - t_m, t_m) in Lemma 13 (Session 4, own experiment).

Lemma 13 of the paper (v0.4): if int_0^{L-sigma} du / Psi(sigma, u) <= 1 for every sigma in [0, tau], then
  M_k(L, tau) <= sup_t  sum_{m active at t} Psi(S - t_m, t_m)     (m active iff sigma_m = S - t_m <= tau).
Every weight used so far (Polymath8b Cor. 6.4, the two-zone weight of Theorem 15) has this form.

Parametrisation: Psi = rho_c * (L - sigma + (k-1) u) with rho_c > 0 constant on cells: Nc uniform
S-cells on [0, L] and geometric u-cells. Fiber integrals are exact (logarithms) at every fine
sigma; the sup over t is taken over
configurations on a fine grid of step L/N (exact total S when every index is active, i.e.
S <= tau; otherwise the inactive coordinates absorb any leftover). The convex problem
  minimise Lambda s.t. fiber integrals <= 1, configuration sums <= Lambda
is solved by cutting planes on the configurations, each inner problem exactly (cvxpy/Clarabel). Output: LP value (a lower estimate of the family's
optimum) and the value of the best scaled-feasible weight found (an upper estimate).
NUMERICAL ONLY: discretised in t, not a rigorous bound in either direction.

usage: dual_lp.py k eps Nc N [iters]   (Nc sigma-cells, fine step L/N)
"""
import sys, numpy as np
from math import log
from scipy.optimize import linprog

class Problem:
    """Psi(sigma, u) = rho_c * W0(sigma, u), W0 = L - sigma + (k-1) u (the shape of Polymath8b's
    Cor. 6.4 weight), rho_c > 0 constant on cells: Nc uniform S-cells on [0, L] and
    geometric u-cells (finest near u = 0, where u/S-type weights such as Theorem 13's need
    resolution). Fiber integrals of 1/W0 are exact (logarithms) at every fine sigma = i h."""
    def __init__(self, k, eps, Nc, N, growth=1.3):
        self.k, self.L, self.tau, self.N = k, 1 + eps, 1 - eps, N
        self.h = self.L / N
        self.Nt = int(np.floor(self.tau / self.h + 1e-9))
        ub, x = [0, 1], 1.0
        while ub[-1] < N:
            x *= growth; ub.append(min(N, max(ub[-1] + 1, int(round(x)))))
        self.ub = ub
        # S-cells: Nc uniform cells on [0, L] (the zones of Theorem 13 are level sets of S)
        sb = sorted(set([int(round(i * N / Nc)) for i in range(Nc + 1)]))
        self.sb = sb
        self.nu, self.ns = len(ub) - 1, len(sb) - 1
        self.ncell = self.nu * self.ns
        self.ucell = np.minimum(np.searchsorted(ub, np.arange(N + 1), side="right") - 1, self.nu - 1)
        self.scell = np.minimum(np.searchsorted(sb, np.arange(N + 1), side="right") - 1, self.ns - 1)
        k1 = k - 1
        self.wf = np.zeros((self.Nt + 1, self.ncell))
        for i in range(self.Nt + 1):          # fiber over |t'| = sigma = i h: u in [0, L - sigma], S = sigma + u
            sig = i * self.h; A = self.L - sig
            for a in range(self.ns):
                for b in range(self.nu):
                    lo = max(ub[b] * self.h, sb[a] * self.h - sig, 0.0)
                    hi = min(ub[b + 1] * self.h, sb[a + 1] * self.h - sig, self.L - sig)
                    if hi > lo:
                        self.wf[i, a * self.nu + b] += (log(A + k1 * hi) - log(A + k1 * lo)) / k1
    def W0(self, i, j):
        return self.L - i * self.h + (self.k - 1) * j * self.h
    def cell(self, i, j):          # sigma index i, u index j: S index i + j
        return self.scell[i + j] * self.nu + self.ucell[j]
    def oracle(self, rho):
        k, N, Nt = self.k, self.N, self.Nt
        out, NEG = [], -1e300
        for s in range(N + 1):
            exact = s <= Nt
            js = list(range(max(0, s - Nt), s + 1))
            val = {j: rho[self.cell(s - j, j)] * self.W0(s - j, j) for j in js}
            cur = np.full(s + 1, NEG); cur[0] = 0.0
            layers, choice = [cur], []
            for n in range(k):
                new = np.full(s + 1, NEG); ch = np.full(s + 1, -1, dtype=np.int64)
                for j in js:
                    cand = np.full(s + 1, NEG); cand[j:] = cur[:s + 1 - j] + val[j]
                    b = cand > new; new[b] = cand[b]; ch[b] = j
                cur = new; layers.append(cur); choice.append(ch)
            if exact:
                bn, bc, best = k, s, layers[k][s]
            else:
                best, bn, bc = NEG, 0, 0
                for n in range(1, k + 1):
                    c = s if n == k else int(np.argmax(layers[n])); v = layers[n][c]
                    if v > best: best, bn, bc = v, n, c
            coef, c = {}, bc
            for n in range(bn, 0, -1):
                j = int(choice[n - 1][c]); cc = self.cell(s - j, j)
                coef[cc] = coef.get(cc, 0.0) + self.W0(s - j, j); c -= j
            out.append((best, coef))
        return out
    def feasible(self, rho):
        m = max(self.wf @ (1 / rho))
        r = rho * max(m, 1.0)                 # global rescaling: every fiber integral <= 1
        return max(v for v, _ in self.oracle(r)), r

def solve(P, iters=80, verbose=False):
    """Outer cutting planes on the configurations only; each inner problem
         minimise Lambda  s.t.  sum_c w[i,c] / rho_c <= 1 (all fine sigma),
                                 sum_c coef[c] rho_c <= Lambda (configurations found so far)
    is solved exactly as a convex program (cvxpy, Clarabel). The inner value is a lower estimate
    of the discretised optimum, the oracle value at the inner solution an upper estimate."""
    import cvxpy as cp
    n = P.ncell
    rho0 = np.ones(n) * log(P.k) / (P.k - 1)          # Polymath8b's Cor. 6.4 weight (rho constant)
    best = P.feasible(rho0)
    rows = []
    for v, coef in P.oracle(rho0): rows.append(coef)
    W = P.wf[[i for i in range(P.wf.shape[0]) if P.wf[i].any()]]
    x = cp.Variable(n, pos=True); lam = cp.Variable()
    lower = 0.0
    for it in range(iters):
        C = np.zeros((len(rows), n))
        for r, coef in enumerate(rows):
            for cc, val in coef.items(): C[r, cc] = val
        prob = cp.Problem(cp.Minimize(lam), [W @ cp.inv_pos(x) <= 1, C @ x <= lam])
        prob.solve(solver=cp.CLARABEL)
        lower = prob.value
        rho = np.maximum(x.value, 1e-9)
        fv, rf = P.feasible(rho)
        if fv < best[0]: best = (fv, rf)
        new = 0
        for v, coef in P.oracle(rho):
            if v > lower * (1 + 1e-7):
                rows.append(coef); new += 1
        if verbose: print(it, "inner %.5f  oracle %.5f  best %.5f  new cuts %d" % (lower, fv, best[0], new), flush=True)
        if new == 0 or best[0] - lower < 1e-4: break
    return lower, best

if __name__ == "__main__":
    k, Nc, N = int(sys.argv[1]), int(sys.argv[3]), int(sys.argv[4])
    e = sys.argv[2]; eps = int(e.split("/")[0]) / int(e.split("/")[1]) if "/" in e else float(e)
    it = int(sys.argv[5]) if len(sys.argv) > 5 else 80
    P = Problem(k, eps, Nc, N)
    lo, (fv, rho) = solve(P, it, verbose=True)
    print("RESULT k=%d eps=%s Nc=%d N=%d: LP %.4f, best feasible %.4f; scaling bound %.4f"
          % (k, e, Nc, N, lo, fv, (1 + eps) * k / (k - 1) * log(k)))
