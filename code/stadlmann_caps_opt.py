#!/usr/bin/env python3
"""Stadlmann's capped support: optimise the test function against an exact cap penalty.

Same setting and notation as code/stadlmann_caps.py.  For F = P 1_T and any 0 < eta < 1,
  (a - b)^2 >= (1 - eta) a^2 - (1/eta - 1) b^2,
so J_T(F) >= (1 - eta) J(P) - (1/eta - 1) L * E(P) and I_T(F) <= I(P), where
  E(P) = sum_{m=1}^{7} C(k, m) int_{R_m(g, c_m)} P^2  >=  int_V P^2   (union bound; R_m from caps_exact.py:
  the first m coordinates exceed g and sum to at least c_m).
All three are exact rational quadratic forms in the coefficients of P, so
  k J_T / I_T >= s * k * q^T [(1-eta) J - (1/eta - 1) L G_E] q / q^T I q,
a generalised Rayleigh quotient: we take its top eigenvector numerically and evaluate the quotient
exactly.  (Coordinates t of the certificate's eps-simplex; s, L, c_m as in stadlmann_caps.py.)

usage: stadlmann_caps_opt.py k D [--etas 1/10,1/20,...] [--out file.json]
"""
import sys, json, time
from math import comb, factorial
sys.path.insert(0, "code")
import mk_general as mg
from flint import fmpq, fmpq_mat
from stadlmann_caps import L_u, TAU_u, G_u, CAPS_u, fl, isqrt_up
from caps_exact import CapPieces

def main():
    k, D = int(sys.argv[1]), int(sys.argv[2])
    etas = [fmpq(*map(int, e.split("/"))) for e in
            (sys.argv[sys.argv.index("--etas") + 1].split(",") if "--etas" in sys.argv else ["1/10", "1/20", "1/40"])]
    mg.EVEN_ONLY = True
    s = (L_u + TAU_u) / 2
    eps = (L_u - TAU_u) / (L_u + TAU_u)
    L0 = 1 + eps
    t0 = time.time()
    basis, I, J = mg.build(k, D, eps)
    n = len(basis)
    print("n=%d, Gram matrices in %.0f s" % (n, time.time() - t0), flush=True)
    W = 2 * D
    cp = CapPieces(k, W, L0, G_u / s)
    keys = {}
    for x in range(n):
        for y in range(x, n):
            keys.setdefault((basis[x][0] + basis[y][0], tuple(u + v for u, v in zip(basis[x][1], basis[y][1]))), None)
    t1 = time.time()
    val = {}
    for key in keys:
        A, B = key
        tot = fmpq(0)
        for m in range(1, 8):
            tot += comb(k, m) * cp.piece(m, CAPS_u[m] / s, A, B)
        val[key] = tot
    G = fmpq_mat(n, n)
    for x in range(n):
        for y in range(x, n):
            v = val[(basis[x][0] + basis[y][0], tuple(u + w_ for u, w_ in zip(basis[x][1], basis[y][1])))]
            G[x, y] = G[y, x] = v
    print("penalty Gram matrix (%d keys) in %.0f s" % (len(keys), time.time() - t1), flush=True)
    lam0, v0 = mg.top_vector(I, J, k, sigma=4.2, prec=400)
    ex0, q0 = mg.certify(I, J, k, v0)
    print("cap-free top vector: s*k*J/I = %.6f, E/I = %.3e" % (fl(s * ex0), fl((q0.transpose() * G * q0)[0, 0] / (q0.transpose() * I * q0)[0, 0])), flush=True)
    best = None
    results = []
    for eta in etas:
        Jp = J * (1 - eta) - G * ((1 / eta - 1) * L0)
        lam, v = mg.top_vector(I, Jp, k, sigma=4.2, prec=400)
        exact, q = mg.certify(I, Jp, k, v)
        Iq = (q.transpose() * I * q)[0, 0]
        Eq = (q.transpose() * G * q)[0, 0]
        Jq = (q.transpose() * J * q)[0, 0]
        # the eta-bound for this vector, and the sharper sqrt-bound J_T >= J - 2 sqrt(J L E) (its optimum over eta)
        lower_eta = s * exact
        lower_sqrt = s * k * (Jq - 2 * isqrt_up(Jq * L0 * Eq)) / Iq
        lower = lower_sqrt if lower_sqrt > lower_eta else lower_eta
        r = dict(eta=str(eta), lower_float=fl(lower), lower_eta_float=fl(lower_eta), lower_sqrt_float=fl(lower_sqrt), capfree_float=fl(s * k * Jq / Iq), E_over_I=fl(Eq / Iq), gt4=bool(lower > 4))
        print(json.dumps(r), flush=True)
        results.append(r)
        if best is None or lower > best[0]:
            best = (lower, eta, q)
    if "--out" in sys.argv:
        lower, eta, q = best
        out = sys.argv[sys.argv.index("--out") + 1]
        json.dump(dict(k=k, D=D, eps=str(eps), s=str(s), eta=str(eta), bound="max of s*k*(J - 2*sqrt_up(J*L*E))/I and s*k*((1-eta)J - (1/eta-1)*L*E)/I", L_u=str(L_u), tau_u=str(TAU_u), g_u=str(G_u),
                       caps_u={str(m): str(c) for m, c in CAPS_u.items()},
                       basis=[[a, list(b)] for a, b in basis], coeffs=[str(q[i, 0]) for i in range(n)],
                       lower_bound=str(lower), lower_bound_float=fl(lower), gt4=bool(lower > 4), scan=results),
                  open(out, "w"))

if __name__ == "__main__":
    main()
