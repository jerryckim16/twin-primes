#!/usr/bin/env python3
"""Certified lower bounds for Maynard's M_k with ALL symmetric polynomial test functions.

Basis: F = sum c_{a,b} (1-P1)^a * prod_{j>=2} P_j^{b_j},  a + sum_j j*b_j <= D,
P_j = sum_i t_i^j.  This spans every symmetric polynomial of degree <= D (k >= D).

Key identity (Dirichlet integral + exponential moments):
  int_{R_k} (1-P1)^A prod_j P_j^{b_j} dt = A!/(k+A+w(b))! * E_k[b],
  E_k[b] = E[ prod_j P_j(X)^{b_j} ],  X_1..X_k iid Exp(1),
and E_k[b] is the coefficient of s^b/b! in (sum_c w(c)! s^c/c!)^k  (multivariate EGF),
which is an integer computed exactly below.

Inner integral over t_k (P_j = P_j' + t_k^j, P1 = P1' + t_k):
  int_0^{1-P1'} (1-P1)^a prod P_j^{b_j} dt_k
     = sum_{e<=b} prod_j C(b_j,e_j) * a! w(e)!/(a+w(e)+1)! * (1-P1')^{a+w(e)+1} prod_j P_j'^{b_j-e_j}.

Pipeline: exact rational Gram matrices (flint fmpq) -> high-precision inverse iteration
(flint arb) for the top generalized eigenvector -> round to rationals -> EXACT Rayleigh
quotient k*vJv/vIv.  The last step is a rigorous lower bound for M_k.

Epsilon-enlarged simplex (Polymath8b Thm 3.12), option --eps p/q:  F is supported on L*R_k with
L = 1+eps, basis (L-P1)^a prod P_j^{b_j}, and the marginal of each t_m is integrated over
tau*R_{k-1}, tau = 1-eps.  Scaling t = L s gives
  int_{L R_k} (L-P1)^A prod P_j^{b_j} = L^{k+A+w(b)} * S_k(A,b),
the inner integral is the same formula with (1-P1') -> (L-P1'), and on tau*R_{k-1}
  (L-P1')^A = sum_i C(A,i) (2 eps)^{A-i} (tau-P1')^i,
  int_{tau R_{k-1}} (tau-P1')^i prod P'^B = tau^{k-1+i+w(B)} S_{k-1}(i,B).
With eps = 0 everything reduces to the plain M_k computation.

usage: mk_general.py k D [--even] [--eps p/q] [--prec bits] [--cert out.json]
(--prec only affects the floating-point search for the vector; 300 bits sufficed up to degree 20.)
"""
import sys, json, time, itertools
from math import comb, factorial
import flint
from flint import fmpq, fmpz, fmpq_mat, arb_mat, arb

EVEN_ONLY = False   # restrict to power sums P_j with j even (Polymath8b used even-part monomials)

def weighted_partitions(W, L):
    """All multiplicity tuples b=(b_2..b_L) with sum j*b_j <= W (odd j forced to 0 if EVEN_ONLY)."""
    out = []
    def rec(j, rem, cur):
        if j > L:
            out.append(tuple(cur)); return
        top = 0 if (EVEN_ONLY and j % 2) else rem // j
        for m in range(top + 1):
            cur.append(m); rec(j + 1, rem - m * j, cur); cur.pop()
    rec(2, W, [])
    return out

def w(b): return sum((j + 2) * x for j, x in enumerate(b))

def submultis(b):
    return itertools.product(*[range(x + 1) for x in b])

class Moments:
    """E_n[b] for all b with w(b) <= W, n variables (exact integers)."""
    def __init__(self, n, W):
        self.L = W
        self.idx = weighted_partitions(W, W)
        self.pos = {b: i for i, b in enumerate(self.idx)}
        f = {b: factorial(w(b)) for b in self.idx}
        res = {b: (1 if w(b) == 0 else 0) for b in self.idx}
        base, e = f, n
        while e:
            if e & 1: res = self.mul(res, base)
            e >>= 1
            if e: base = self.mul(base, base)
        self.E = res
    def mul(self, F, G):
        H = {}
        for b in self.idx:
            s = 0
            for c in submultis(b):
                fc = F.get(c, 0)
                if not fc: continue
                d = tuple(x - y for x, y in zip(b, c))
                gd = G.get(d, 0)
                if not gd: continue
                m = 1
                for x, y in zip(b, c): m *= comb(x, y)
                s += m * fc * gd
            H[b] = s
        return H

def build(k, D, eps=None):
    eps = fmpq(0) if eps is None else eps
    Lf, tau, two_e = 1 + eps, 1 - eps, 2 * eps
    L = 2 * D
    basis = [(a, b) for b in weighted_partitions(D, L) for a in range(D - w(b) + 1)]
    pad = lambda b: tuple(b) + (0,) * (L - 1 - len(b))
    basis = [(a, pad(b)) for a, b in basis]
    Mk, Mk1 = Moments(k, 2 * D), Moments(k - 1, 2 * D)
    def S(M, n, A, b):
        return fmpq(factorial(A) * M.E[b], factorial(n + A + w(b)))
    add = lambda b1, b2: tuple(x + y for x, y in zip(b1, b2))
    n = len(basis)
    I = fmpq_mat(n, n); J = fmpq_mat(n, n)
    inner = []
    for a, b in basis:
        terms = []
        for e in submultis(b):
            E = w(e); m = 1
            for x, y in zip(b, e): m *= comb(x, y)
            terms.append((fmpq(m * factorial(a) * factorial(E), factorial(a + E + 1)), a + E + 1,
                          tuple(x - y for x, y in zip(b, e))))
        inner.append(terms)
    cacheI, cacheJ = {}, {}
    for x in range(n):
        a, b = basis[x]
        for y in range(x, n):
            a2, b2 = basis[y]
            key = (a + a2, add(b, b2))
            if key not in cacheI: cacheI[key] = S(Mk, k, *key) * Lf ** (k + key[0] + w(key[1]))
            I[x, y] = I[y, x] = cacheI[key]
            s = fmpq(0)
            for c1, A1, B1 in inner[x]:
                for c2, A2, B2 in inner[y]:
                    kk = (A1 + A2, add(B1, B2))
                    if kk not in cacheJ:
                        A, B = kk
                        if eps == 0:
                            cacheJ[kk] = S(Mk1, k - 1, A, B)
                        else:
                            cacheJ[kk] = sum((comb(A, i) * two_e ** (A - i) * tau ** (k - 1 + i + w(B))
                                              * S(Mk1, k - 1, i, B) for i in range(A + 1)), fmpq(0))
                    s += c1 * c2 * cacheJ[kk]
            J[x, y] = J[y, x] = s
    return basis, I, J

def top_vector(I, J, k, sigma, prec=None, max_iter=400):
    """Inverse iteration with a FIXED shift sigma above the top eigenvalue, so it can only
    converge to the top one.  C = (B - sigma A)^{-1} A is formed once; then v <- C v."""
    flint.ctx.prec = prec or (600 + 150 * int(round((I.nrows()) ** 0.5)))
    n = I.nrows()
    A = arb_mat(I); B = arb_mat(J) * k
    C = (B - A * arb(sigma)).solve(A, algorithm="approx").mid()
    v = arb_mat(n, 1, [1] * n)
    lam = None
    for it in range(max_iter):
        x = (C * v).mid()
        nrm = max(abs(x[i, 0].mid()) for i in range(n))
        v = x * (1 / nrm)
        if it % 5 == 4:
            num = (v.transpose() * B * v)[0, 0]; den = (v.transpose() * A * v)[0, 0]
            new = (num / den).mid()
            if lam is not None and abs(new - lam) < arb("1e-16"):
                return new, v
            lam = new
    return lam, v

def certify(I, J, k, v):
    """Take the midpoints of v EXACTLY (dyadic rationals) and return the exact quotient."""
    n = I.nrows()
    ent = []
    for i in range(n):
        man, ex = v[i, 0].mid().man_exp()
        ent.append(fmpq(man) * (fmpq(2) ** int(ex)) if ex >= 0 else fmpq(man, fmpz(2) ** int(-ex)))
    q = fmpq_mat(n, 1, ent)
    num = (q.transpose() * J * q)[0, 0] * k
    den = (q.transpose() * I * q)[0, 0]
    return num / den, q

def run(k, D, sigma=None, eps=None, prec=None):
    from math import log
    e = 0.0 if eps is None else float(eps.p) / float(eps.q)
    # Polymath8b / Proposition 12 upper bound (1+eps) k/(k-1) log k: above the top eigenvalue
    if sigma is None: sigma = (1 + e) * k / (k - 1) * log(k) + 0.02
    t0 = time.time()
    basis, I, J = build(k, D, eps)
    t1 = time.time()
    lam, v = top_vector(I, J, k, sigma, prec=prec)
    exact, q = certify(I, J, k, v)
    val = float(exact.p) / float(exact.q) if abs(exact.p) < 10**300 else None
    from fractions import Fraction
    val = float(Fraction(int(exact.p), int(exact.q)))
    return dict(k=k, D=D, n=len(basis), float_eig=str(lam.str(15, radius=False)), certified=round(val, 12),
                gt4=bool(exact > 4), build_s=round(t1 - t0, 1), solve_s=round(time.time() - t1, 1)), exact, basis, q

if __name__ == "__main__":
    if "--even" in sys.argv: EVEN_ONLY = True
    k, D = int(sys.argv[1]), int(sys.argv[2])
    eps = None
    if "--eps" in sys.argv:
        es = sys.argv[sys.argv.index("--eps") + 1]
        eps = fmpq(*map(int, es.split("/"))) if "/" in es else fmpq(int(es))
    prec = int(sys.argv[sys.argv.index("--prec") + 1]) if "--prec" in sys.argv else None
    info, exact, basis, q = run(k, D, eps=eps, prec=prec)
    if eps is not None: info["eps"] = str(eps)
    print(json.dumps(info), flush=True)
    if "--cert" in sys.argv:
        out = sys.argv[sys.argv.index("--cert") + 1]
        json.dump(dict(k=k, D=D, eps=str(eps) if eps is not None else "0", basis=[[a, list(b)] for a, b in basis],
                       coeffs=[str(q[i, 0]) for i in range(q.nrows())],
                       rayleigh=str(exact), gt4=bool(exact > 4)), open(out, "w"))
