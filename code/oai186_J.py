#!/usr/bin/env python3
"""Rung 186, third sub-step (Session 14): independent evaluation of J_0, J_+, J_t and J_{lambda,H} of [14]
(OpenAI, short_gaps_numerics.pdf), (1.9)-(1.10), (1.29), (2.13)-(2.15), compared with Lemma 2.5:
    J_{lambda,H} >= 90248755123e-24  and  rho* J_{lambda,H} / I_H > 500103/500000.
Own derivation of the layered form (it fixes the two points left unclear in notes/sources-186-forms.md, Sec. 3):
  V_i(Y) = E_i F(Y) = int F(Y (+)_i X) dnu(X). F(Y (+) X) != 0 needs r' + a < n (r' = index sum of the 39 retained
  coordinates, a = cell of the erased one), the outer shell s of r' + a, and EVERY fragment of Y and of X at most c_s.
  In |V_i|^2 = int int F(Y+X) F(Y+X') the retained Y must satisfy max fragment(Y) <= min(c_s(r'+a), c_s(r'+a'),
  face cap(r')). Split Y by the layer of its largest fragment, (b_{a-1}, b_a], over ALL distinct cap values b that
  occur (outer and face caps): b_1 < ... < b_7 = 35265, 35419, 44781, 44976, 46580, 49152, 68225 (units h). The
  39-coordinate measure of that layer is Delta M^a = M^{b_a}_{39} - M^{b_{a-1}}_{39} (nu_c restricted to max <= b is
  nu_b, coordinatewise), and Y is allowed iff b_a <= every cap involved, i.e. the erased coordinate may sit in shells
  s with c_s >= b_a (that is v^{(l(a))}) and the face row of r' must have cap >= b_a (face mask chi_{F,a}).
  The erased coordinate carries g(t_a) d_{c_s}(a) h; with (hZ)^40 normalisation and the sum over i this gives
  J_F = (40 h / Z) sum_a sum_{r'} chi_{F,a}(r') sum_{tau,ups} v_tau(r') v_ups(r') Delta M^a_{tau+ups}(r'),
  v_{s,tau}(r') = sum_{sigma,d,A: sigma\\A = tau} c_{sigma,d} sum_a chi_s(r'+a) x_{r'+a}^d g_a d_{c_s}(a) t_a^{e(A)}.
  J_0: F = base face H_0; J_+: chi_{1,a} - chi_{0,a}; J_t: chi_{f,a} - chi_{1,a}.  (1.29): J = J_0 + (a_h+b_h) J_+ + b_h J_t.
Arithmetic: as in oai186_IH.py (mpmath 110 digits for rho_D, g, Z; coordinate arrays floored/ceiled at 2^B; exact
GMP Kronecker products). The erased-coordinate correlations are exact integer correlations of the exact signed
integer rows with the floored weights; their rounding error (< 2 units of 2^-B per weight) and that of the layer
measures (lower/upper products) are far below 1e-40 relative and are not propagated (high precision, NOT a rigorous
enclosure of the whole sum; the comparison with [14] is at 1e-9).
usage: oai186_J.py [--bits 256] [--out f.json]"""
import sys, json, time
from fractions import Fraction as Fr
import importlib.util
spec = importlib.util.spec_from_file_location("ih", "code/oai186_IH.py")
ih = importlib.util.module_from_spec(spec); spec.loader.exec_module(ih)
from mpmath import mp, mpf
from gmpy2 import mpz

n, B, h, KDIM = ih.n, ih.B, ih.h, 39
OUTER = ih.SHELLS                                  # ((r0, r1), cap): caps decreasing
FACES = {
    "0": [((0, 84930), 68225), ((84931, 87194), 44781), ((87195, 89524), 35265)],
    "1": [((0, 85161), 68225), ((85162, 87249), 44976), ((87250, 89914), 35419)],
    "f": [((0, 98263), 68225)],
}
BVALS = sorted({c for _, c in OUTER} | {c for f in FACES.values() for _, c in f})
AH, BH = Fr(2479900401, 2500000000), Fr(-843183, 10 ** 9)
RHOSTAR = Fr(2624989, 10 ** 7)

def corr(I, w):
    """out[r] = sum_{a} I[r + a] w[a] (r < n, r + a < n), I signed exact ints, w >= 0 ints. Exact."""
    off = max(abs(x) for x in I) if I else 0
    Ip = [x + off for x in I]                         # >= 0
    rev = Ip[::-1]                                    # rev[n-1-m] = Ip[m]
    W = (max(rev).bit_length() + max(w).bit_length() + n.bit_length() + 8) // 8 + 1
    prod = ih.unpack(ih.pack(rev, W) * ih.pack(w, W), W, n)   # prod[q] = sum_{i+a=q} rev[i] w[a], q < n
    # sum_a Ip[r+a] w[a] = sum_a rev[n-1-r-a] w[a] = prod[n-1-r]
    pre = [0] * (n + 1)
    for a in range(n):
        pre[a + 1] = pre[a] + w[a]
    return [prod[n - 1 - r] - off * pre[n - r] for r in range(n)]

def main():
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    SIGS, C = ih.SIGS, ih.C
    Dx = 2624989 * ih.NGRID * 10
    Xr = [(r + 20) * 2742997 * 10 - 9 * 2624989 * ih.NGRID for r in range(n)]
    Dpow = [Dx ** (6 - d) for d in range(7)]
    PSC = 10 ** 10 * Dx ** 6                          # p-values scaled by PSC are integers
    # rows R[(tau, e)](r) = sum_{sigma, d, A: sigma\A = tau, e(A) = e} c_{sigma,d} x_r^d   (scaled by PSC)
    import itertools
    rowspec = {}
    for s in SIGS:
        L = len(s)
        for mask in range(1 << L):
            A = [i for i in range(L) if mask >> i & 1]
            tau = tuple(sorted(s[i] for i in range(L) if not mask >> i & 1))
            e = sum(s[i] for i in A)
            rowspec.setdefault((tau, e), {})
            rowspec[(tau, e)][s] = rowspec[(tau, e)].get(s, 0) + 1
    xpow = [[x ** d * Dpow[d] for d in range(7)] for x in Xr]
    rows = {}
    for key, ss in rowspec.items():
        coef = [sum(mult * C[s][d] for s, mult in ss.items()) for d in range(7)]
        rows[key] = [sum(coef[d] * xp[d] for d in range(7)) for xp in xpow]
    log_("%d (tau, e) rows" % len(rows))
    tj = [(j + Fr(1, 2)) * h for j in range(n)]
    gv = [mpf(ih.gfun(t).numerator) / ih.gfun(t).denominator for t in tj]
    g2 = [v * v for v in gv]
    Z = mp.fsum(g2)
    tjf = [mpf(t.numerator) / t.denominator for t in tj]
    SC = mpf(2) ** B
    es = sorted({e for (_, e) in rows})
    # erased-coordinate marginals v_{s,tau}(r') (scaled by PSC * 2^B), exact correlations with floored weights
    v = {}
    for si, ((r0, r1), M) in enumerate(OUTER):
        d = ih.cellmass(M)
        for e in es:
            w = [int(mp.floor(gv[a] * d[a] * tjf[a] ** e * SC)) for a in range(n)]
            for (tau, ee), R in rows.items():
                if ee != e:
                    continue
                I = [R[r] if r0 <= r <= r1 else 0 for r in range(n)]
                c = corr(I, w)
                acc = v.setdefault((si, tau), [0] * n)
                for r in range(n):
                    acc[r] += c[r]
        log_("shell %d (cap %d): marginals done" % (si, M))
    taus = sorted({t for (_, t) in v})
    # v^{(l)} = sum_{s < l}
    vl = {}
    for l in (1, 2, 3):
        for tau in taus:
            vl[(l, tau)] = [sum(v[(s, tau)][r] for s in range(l) if (s, tau) in v) for r in range(n)]
    # eta = tau + ups, ordered pairs; W_{l,eta}(r) = sum v_tau v_ups
    pairs = {}
    for t1 in taus:
        for t2 in taus:
            pairs.setdefault(tuple(sorted(t1 + t2)), []).append((t1, t2))
    etas = sorted(pairs)
    Mform = {}
    for eta in etas:
        f = {}
        for pi in ih.set_partitions(list(range(len(eta)))):
            E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
            f[E] = f.get(E, 0) + ih.falling(KDIM, len(pi))
        Mform[eta] = f
    allE = sorted({E for f in Mform.values() for E in f}, key=lambda E: (len(E), E))
    log_("%d eta, %d multisets; layer caps %s" % (len(etas), len(allE), BVALS))
    # M^{b}_{39,eta} lower and upper (scaled 2^B)
    def Mcap(M, up):
        d = ih.cellmass(M)
        K = [g2[j] * d[j] / Z for j in range(n)]
        P = {}
        for e in [0] + list(range(2, 13)):
            vals = [K[j] * tjf[j] ** e * SC for j in range(n)]
            P[e] = [int(mp.ceil(x)) + 1 for x in vals] if up else [max(int(mp.floor(x)) - 1, 0) for x in vals]
        p0 = {33: ih.ppow(P[0], 33, up)}
        for k in range(34, 40):
            p0[k] = ih.pmul(p0[k - 1], P[0], up)
        prod, ME = {}, {}
        def getprod(E):
            if E not in prod:
                prod[E] = P[E[0]] if len(E) == 1 else ih.pmul(getprod(E[:-1]), P[E[-1]], up)
            return prod[E]
        for E in allE:
            ME[E] = p0[KDIM - len(E)] if not E else ih.pmul(p0[KDIM - len(E)], getprod(E), up)
        out = {}
        for eta in etas:
            arr = [0] * n
            for E, cf in Mform[eta].items():
                a = ME[E]
                for r in range(n):
                    arr[r] += cf * a[r]
            out[eta] = arr
        return out
    def lofl(b):
        return sum(1 for _, c in OUTER if c >= b)
    def facemask(F, b):
        m = [0] * n
        for (r0, r1), c in FACES[F]:
            if c >= b:
                for r in range(r0, r1 + 1):
                    m[r] = 1
        return m
    Jsum = {"0": 0, "+": 0, "t": 0}
    Jsum_up = {"0": 0, "+": 0, "t": 0}
    prevlo = prevup = None
    for ai, b in enumerate(BVALS):
        Mlo, Mup = Mcap(b, False), Mcap(b, True)
        if prevlo is None:
            Dlo, Dup = Mlo, Mup
        else:
            Dlo = {eta: [max(Mlo[eta][r] - prevup[eta][r], 0) for r in range(n)] for eta in etas}
            Dup = {eta: [Mup[eta][r] - prevlo[eta][r] for r in range(n)] for eta in etas}
        prevlo, prevup = Mlo, Mup
        l = lofl(b)
        m0, m1, mf = facemask("0", b), facemask("1", b), facemask("f", b)
        A = {"0": m0, "+": [m1[r] - m0[r] for r in range(n)], "t": [mf[r] - m1[r] for r in range(n)]}
        assert all(x >= 0 for x in A["+"]) and all(x >= 0 for x in A["t"]), "masks not nested"
        if l == 0:
            continue
        for eta in etas:
            Wl = [0] * n
            for (t1, t2) in pairs[eta]:
                a1, a2 = vl[(l, t1)], vl[(l, t2)]
                for r in range(n):
                    Wl[r] += a1[r] * a2[r]
            dl, du = Dlo[eta], Dup[eta]
            for F in ("0", "+", "t"):
                msk = A[F]
                lo = up = 0
                for r in range(n):
                    if msk[r]:
                        wv = Wl[r]
                        if wv >= 0:
                            lo += wv * dl[r]; up += wv * du[r]
                        else:
                            lo += wv * du[r]; up += wv * dl[r]
                Jsum[F] += lo; Jsum_up[F] += up
        log_("layer %d (b = %d, l = %d) done" % (ai, b, l))
    # scale: v scaled PSC*2^B each, Delta M scaled 2^B; factor 40 h / Z
    fac = Fr(40) * h
    Zf = Fr(str(mp.nstr(Z, 100)))
    den = (PSC << B) ** 2 << B
    J = {F: Fr(Jsum[F], den) * fac / Zf for F in Jsum}
    Ju = {F: Fr(Jsum_up[F], den) * fac / Zf for F in Jsum}
    Jl = J["0"] + (AH + BH) * J["+"] + BH * J["t"]
    Jlu = Ju["0"] + (AH + BH) * Ju["+"] + BH * Ju["t"]
    ref = Fr(90248755123, 10 ** 24)
    IH = Fr(json.load(open("code/oai186_IH.json"))["I_H_lo_exact"])
    out = dict(J0=float(J["0"]), Jplus=float(J["+"]), Jt=float(J["t"]), J_lambda=float(Jl), J_lambda_upper_M=float(Jlu),
               ref_J_lower=float(ref), J_ge_ref=bool(Jl >= ref), rel_excess_over_ref=float(Jl / ref - 1),
               ratio_rhostar_J_over_IH=float(RHOSTAR * Jl / IH), ratio_gt_500103_500000=bool(RHOSTAR * Jl / IH > Fr(500103, 500000)),
               bits=B, seconds=round(time.time() - t0))
    log_(json.dumps(out))
    if "--out" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)

if __name__ == "__main__":
    main()
