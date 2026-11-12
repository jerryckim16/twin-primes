#!/usr/bin/env python3
"""Stadlmann's support with rough-mass caps: a rigorous lower bound from a cap-free certificate.

Setting (Polymath scaling u = 4t of Stadlmann's coordinates, one band):
  support T = {u >= 0 : sum u <= L, sum_{i in I(u)} u_i <= C_{|I(u)|}},  I(u) = {i : u_i > g},
  J integrates (int F du_k)^2 over {u_1 + ... + u_{k-1} <= tau}; the criterion is k J(F) / I(F) > 4.
Stadlmann's parameters: L = 4(A1+eps) = 1.042, tau = 4(A1-eps) = 0.982, g = 4 delta = 0.112,
C_1 = C_2 = 0.6, C_m = 0.68 (m >= 3).

Take F = P 1_T with P a polynomial and V = {sum u <= L} \\ T.  Then (Proposition 23 of paper v0.5)
  I_T(F) <= I(P),   J_T(F) >= J(P) - 2 sqrt(J(P) * L * E),   E >= int_V P^2,
where I(P), J(P) are the cap-free functionals on {sum u <= L} with marginal domain tau.
Union bound: a point of V has a large set I with sum_I u > C_|I| (|I| <= 6) or |I| >= 7 (then 7 of its
coordinates exceed g); so V lies in the union over m = 1..7 and |I| = m of {sum_I u >= c_m},
c_m = C_m (m <= 6), c_7 = 7 g, and by symmetry int_V P^2 <= sum_m C(k, m) int_{sum_{i<=m} u_i >= c_m} P^2.

Exact formula (x = first m coordinates, y = the rest, r = |x|; S_n, E_n as in mk_general.py):
  int_{simplex L, |x| >= c} (L - P1)^A prod_j P_j^{B_j}
    = sum_{e <= B} prod C(B_j, e_j) S_{k-m}(A, B-e) E_m[e]/(m-1+w(e))! int_c^L r^{m-1+w(e)} (L-r)^{k-m+A+w(B-e)} dr.
With c = 0 and m = 1 this is the full integral: checked below against the Gram matrix (self-test).

The certificate (mk_general.py --eps e) is in coordinates t with support 1+e and marginal 1-e; u = s t with
s = (L+tau)/2, e = (L-tau)/(L+tau).  Ratios scale by s and thresholds by 1/s.

usage: stadlmann_caps.py code/cert_stad49_capfree_D20e.json [--out result.json]
"""
import sys, json, time
from math import comb, factorial
sys.path.insert(0, "code")
import mk_general as mg
from flint import fmpq, fmpz, fmpq_mat

Fq = lambda s: fmpq(*map(int, s.split("/"))) if "/" in s else fmpq(int(s))

# Stadlmann (arXiv:2608.31126) parameters, Polymath scaling
L_u, TAU_u, G_u = fmpq(1042, 1000), fmpq(982, 1000), fmpq(112, 1000)
CAPS_u = {1: fmpq(6, 10), 2: fmpq(6, 10), 3: fmpq(68, 100), 4: fmpq(68, 100), 5: fmpq(68, 100), 6: fmpq(68, 100)}
CAPS_u[7] = 7 * G_u


def fl(z):
    from fractions import Fraction
    return float(Fraction(int(z.p), int(z.q)))


def isqrt_up(q):
    """A rational >= sqrt(q) (q >= 0 rational), within a relative 1e-30."""
    p, d = int(q.p), int(q.q)
    from math import isqrt
    scale = 10 ** 40
    n = isqrt(p * d * scale * scale) + 1
    return fmpq(n, d * scale)


def main():
    path = sys.argv[1]
    c = json.load(open(path))
    k, D, eps = c["k"], c["D"], Fq(c["eps"])
    s = (L_u + TAU_u) / 2
    assert eps == (L_u - TAU_u) / (L_u + TAU_u), "certificate eps does not match Stadlmann's (L, tau)"
    L0 = 1 + eps
    basis = [(a, tuple(b)) for a, b in c["basis"]]
    mg.EVEN_ONLY = all(x == 0 for _, b in basis for j, x in enumerate(b) if (j + 2) % 2)
    q = [Fq(x) for x in c["coeffs"]]
    t0 = time.time()
    b2, I, J = mg.build(k, D, eps)
    assert [(a, tuple(b)) for a, b in b2] == basis
    n = len(basis)
    qm = fmpq_mat(n, 1, q)
    Iq = (qm.transpose() * I * qm)[0, 0]
    Jq = (qm.transpose() * J * qm)[0, 0]
    capfree = s * k * Jq / Iq
    print("rebuilt Gram matrices in %.0f s; cap-free ratio s*k*J/I = %.8f" % (time.time() - t0, fl(capfree)), flush=True)
    # group P^2 by key (A, B)
    W = 2 * D
    padlen = W - 1
    groups = {}
    for x in range(n):
        ax, bx = basis[x]
        for y in range(x, n):
            ay, by = basis[y]
            key = (ax + ay, tuple(u + v for u, v in zip(bx, by)))
            cf = q[x] * q[y] * (1 if x == y else 2)
            groups[key] = groups.get(key, fmpq(0)) + cf
    print("%d distinct (A, B) keys" % len(groups), flush=True)
    moms = {}
    def Mom(nv):
        if nv not in moms:
            moms[nv] = mg.Moments(nv, W)
        return moms[nv]
    def S(nv, A, b):
        return fmpq(factorial(A) * Mom(nv).E[b], factorial(nv + A + mg.w(b)))
    rcache = {}
    def rint(c0, alpha, N):
        key = (c0, alpha, N)
        if key not in rcache:
            h = L0 - c0
            tot = fmpq(0)
            for i in range(alpha + 1):
                tot += comb(alpha, i) * L0 ** (alpha - i) * (-1) ** i * h ** (N + i + 1) / (N + i + 1)
            rcache[key] = tot
        return rcache[key]
    def piece(m, c0, A, B):
        tot = fmpq(0)
        for e in mg.submultis(B):
            e = tuple(e)
            mult = 1
            for u, v in zip(B, e):
                mult *= comb(u, v)
            we = mg.w(e)
            rest = tuple(u - v for u, v in zip(B, e))
            Em = Mom(m).E[e]
            if Em == 0:
                continue
            tot += (mult * S(k - m, A, rest) * fmpq(Em, factorial(m - 1 + we))
                    * rint(c0, m - 1 + we, k - m + A + mg.w(rest)))
        return tot
    # self-test: m = 1, c = 0 must give q^T I q exactly
    t1 = time.time()
    full = sum((cf * piece(1, fmpq(0), A, B) for (A, B), cf in groups.items()), fmpq(0))
    assert full == Iq, "self-test failed: c = 0 piece differs from q^T I q"
    print("self-test passed (m = 1, c = 0 reproduces q^T I q exactly) in %.0f s" % (time.time() - t1), flush=True)
    E = fmpq(0)
    parts = {}
    for m in range(1, 8):
        c0 = CAPS_u[m] / s
        val = sum((cf * piece(m, c0, A, B) for (A, B), cf in groups.items()), fmpq(0))
        assert val >= 0
        parts[m] = val
        E += comb(k, m) * val
        print("m=%d: C(k,m) * int_{|x|>=%.4f} P^2 / I = %.3e" % (m, fl(c0), fl(comb(k, m) * val / Iq)), flush=True)
    rad = isqrt_up(Jq * L0 * E)
    lower = s * k * (Jq - 2 * rad) / Iq
    f = fl
    print("E/I = %.3e; certified lower bound for Stadlmann's ratio k J_T / I_T: %.8f (%s 4)"
          % (f(E / Iq), f(lower), ">" if lower > 4 else "NOT >"), flush=True)
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
        json.dump(dict(cert=path, k=k, D=D, eps=str(eps), s=str(s), L_u=str(L_u), tau_u=str(TAU_u), g_u=str(G_u),
                       caps_u={str(m): str(v) for m, v in CAPS_u.items()},
                       I=str(Iq), J=str(Jq), capfree_ratio=str(capfree),
                       E_parts={str(m): str(v) for m, v in parts.items()}, E=str(E),
                       sqrt_upper=str(rad), lower_bound=str(lower), gt4=bool(lower > 4),
                       lower_bound_float=f(lower), capfree_float=f(capfree)), open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
