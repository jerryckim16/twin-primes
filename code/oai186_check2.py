#!/usr/bin/env python3
"""Rung 186: SECOND, independent program for I_H and J_{lambda,H} of [14] (Session 14).
Differs from code/oai186_IH.py / code/oai186_J.py in library and in combinatorics:
  * ball arithmetic (python-flint arb / arb_poly, rigorous enclosures throughout, including the Dickman closed forms
    via arb log and acb polylog), instead of mpmath + GMP integers;
  * the 40- (or 39-) fold coordinate sums come from the power A(y)^d of the exponential generating series
        A(y)(X) = sum_j K_j X^j exp(sum_e y_e t_j^e),   [y^m] A = P_{w(m)}[K] / m!,
    truncated to the down-closed set of exponent vectors m (one variable y_e per signature value e = 2..6), so that
        sum over d-cells of prod K X^r prod_e P_e(t)^{m_e} = m! [y^m] A(y)^d,
    instead of the set-partition formula;
  * the erased-coordinate rows are built per (sigma, labelled subset A) from p_sigma directly.
Same transcription (notes/sources-186-forms.md) and the same reading of the layered form (2.15) as oai186_J.py
(that reading is derived in its docstring), so this checks the arithmetic and code, not the reading.
usage: oai186_check2.py [--prec 320] [--only I] [--out f.json]"""
import sys, json, time
from math import factorial
from flint import arb, acb, arb_poly, fmpq, ctx

PREC = int(sys.argv[sys.argv.index("--prec") + 1]) if "--prec" in sys.argv else 320
ctx.prec = PREC
NG = 98304
n = NG - 40
S_ = fmpq(2742997, 2624989)
h = S_ / NG
SIGS = [(), (2,), (3,), (4,), (5,), (6,), (2, 2), (2, 3), (2, 4), (3, 3), (2, 2, 2)]
TAB = {tuple(r["sigma"]): [int(v) for v in r["C"]] for r in json.load(open("code/oai186_table11.json"))}
OUTER = [((0, 89196), 68225), ((89197, 95598), 49152), ((95599, 98263), 46580)]
FACES = {"0": [((0, 84930), 68225), ((84931, 87194), 44781), ((87195, 89524), 35265)],
         "1": [((0, 85161), 68225), ((85162, 87249), 44976), ((87250, 89914), 35419)],
         "f": [((0, 98263), 68225)]}
EV = [2, 3, 4, 5, 6]

def A(q):
    return arb(q.p) / arb(q.q)

# Dickman, rigorous
LOG2 = arb(2).log()
KC = LOG2 ** 2 / 2 + acb(arb(1) / 2).polylog(2).real
def li2(x):
    return acb(x).polylog(2).real
def Gf(u):
    lu = u.log()
    return 2 * u - u * lu + u * (lu ** 2 - 2 * lu + 2) / 2 + u * li2(1 / u) - (u - 1) * (u - 1).log() + u * lu - KC * u
PHI2 = 3 - 2 * LOG2
G2 = Gf(arb(2))
def Phi(num, M):           # u = num/M exactly rational
    u = arb(num) / M
    if num <= M: return u
    if num <= 2 * M: return 2 * u - u * u.log() - 1
    assert num <= 3 * M
    return PHI2 + Gf(u) - G2
def cellmass(M):
    d = [arb(1)] * n
    prev = Phi(M, M)
    for j in range(M, n):
        cur = Phi(j + 1, M)
        d[j] = M * (cur - prev)
        prev = cur
    return d

def gq(t):
    return fmpq(21, 200) / (1 + t / 100) + fmpq(179, 200) / (1 + fmpq(907, 5) * t)

def mvec(sig):
    return tuple(sum(1 for x in sig if x == e) for e in EV)
def mfact(m):
    out = 1
    for x in m: out *= factorial(x)
    return out
def wt(m):
    return sum(e * x for e, x in zip(EV, m))

def downclose(ms):
    S = set()
    stack = list(ms)
    while stack:
        m = stack.pop()
        if m in S: continue
        S.add(m)
        for i in range(len(m)):
            if m[i]:
                stack.append(m[:i] + (m[i] - 1,) + m[i + 1:])
    return S

def series_mul(Aser, Bser, S):
    out = {}
    for m in S:
        acc = None
        # all m1 <= m
        rng = [range(x + 1) for x in m]
        import itertools
        for m1 in itertools.product(*rng):
            m2 = tuple(a - b for a, b in zip(m, m1))
            if m1 in Aser and m2 in Bser:
                p = (Aser[m1] * Bser[m2]).truncate(n)
                acc = p if acc is None else acc + p
        if acc is not None:
            out[m] = acc
    return out

def series_pow(Aser, d, S):
    res, base = None, Aser
    while d:
        if d & 1:
            res = base if res is None else series_mul(res, base, S)
        d >>= 1
        if d:
            base = series_mul(base, base, S)
    return res

def main():
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    tq = [(j + fmpq(1, 2)) * h for j in range(n)]
    gvals = [A(gq(t)) for t in tq]
    g2 = [x * x for x in gvals]
    Z = sum(g2, arb(0))
    tj = [A(t) for t in tq]
    log_("Z = %s" % Z.str(20))
    # p_sigma(r) exactly, then arb
    xr = [(r + 20) * h - fmpq(9, 10) for r in range(n)]
    p = {}
    for s in SIGS:
        c = [fmpq(v, 10 ** 10) for v in TAB[s]]
        p[s] = [A(sum((c[d] * x ** d for d in range(7)), fmpq(0))) for x in xr]
    log_("p_sigma ready")
    etas = sorted({tuple(sorted(a + b)) for a in SIGS for b in SIGS})
    meta = {eta: mvec(eta) for eta in etas}
    S = downclose(meta.values())
    log_("%d eta, %d exponent vectors in the down-closed set" % (len(etas), len(S)))

    def Mser(M, d):
        dm = cellmass(M)
        K = [g2[j] * dm[j] / Z for j in range(n)]
        maxw = max(wt(m) for m in S)
        Pw = {0: arb_poly(K)}
        cur = list(K)
        for w in range(1, maxw + 1):
            cur = [cur[j] * tj[j] for j in range(n)]
            Pw[w] = arb_poly(cur)
        Aser = {m: Pw[wt(m)] * (arb(1) / mfact(m)) for m in S}
        Pd = series_pow(Aser, d, S)
        return {eta: Pd[meta[eta]] * mfact(meta[eta]) for eta in etas}

    out = {}
    if "--jcap" in sys.argv:
        return jworker(int(sys.argv[sys.argv.index("--jcap") + 1]), p, gvals, g2, Z, tj, etas, Mser, log_)
    # ---------- I_H ----------
    IH = arb(0)
    for (r0, r1), M in OUTER:
        Ms = Mser(M, 40)
        part = arb(0)
        for eta in etas:
            coeffs = Ms[eta]
            pairs = [(a, b) for a in SIGS for b in SIGS if tuple(sorted(a + b)) == eta]
            for r in range(r0, r1 + 1):
                q = arb(0)
                for a, b in pairs:
                    q += p[a][r] * p[b][r]
                part += q * coeffs[r]
        log_("I_H shell cap %d: %s" % (M, part.str(15)))
        IH += part
    out["I_H"] = IH.str(20, radius=True)
    out["I_H_mid"] = float(IH.mid())
    out["I_H_rad"] = float(IH.rad())
    refI = (arb(23685317816) / 10 ** 24, arb(23685317890) / 10 ** 24)
    out["I_H_inside_ref"] = bool(IH > refI[0] and IH < refI[1])
    log_("I_H = %s, inside Lemma 2.5 enclosure: %s" % (IH.str(15), out["I_H_inside_ref"]))
    if "--only" in sys.argv and sys.argv[sys.argv.index("--only") + 1] == "I":
        if "--out" in sys.argv: json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)
        return
    # ---------- J ----------
    # erased-coordinate marginals v_{s,tau}(r') = sum_{sigma, A labelled} sum_a chi_s(r'+a) p_sigma(r'+a) g_a d_{c_s}(a) t_a^{e(A)}
    taus = sorted(set(SIGS))
    v = {}
    for si, ((r0, r1), M) in enumerate(OUTER):
        dm = cellmass(M)
        wbase = [gvals[a] * dm[a] for a in range(n)]
        wcache = {}
        def wpoly(e):
            if e not in wcache:
                wcache[e] = arb_poly([wbase[a] * tj[a] ** e for a in range(n)])
            return wcache[e]
        for s in SIGS:
            L = len(s)
            frev = arb_poly([p[s][n - 1 - i] if r0 <= n - 1 - i <= r1 else arb(0) for i in range(n)])
            for mask in range(1 << L):
                tau = tuple(sorted(s[i] for i in range(L) if not mask >> i & 1))
                e = sum(s[i] for i in range(L) if mask >> i & 1)
                prod = (frev * wpoly(e)).truncate(n)
                acc = v.setdefault((si, tau), [arb(0)] * n)
                for rp in range(n):
                    acc[rp] += prod[n - 1 - rp]
        log_("marginals shell %d done" % si)
    vl = {}
    for l in (1, 2, 3):
        for tau in taus:
            vl[(l, tau)] = [sum((v[(s, tau)][r] for s in range(l) if (s, tau) in v), arb(0)) for r in range(n)]
    BV = sorted({c for _, c in OUTER} | {c for f in FACES.values() for _, c in f})
    def mask(F, b):
        m = [0] * n
        for (r0, r1), c in FACES[F]:
            if c >= b:
                for r in range(r0, r1 + 1): m[r] = 1
        return m
    Jf = {"0": arb(0), "+": arb(0), "t": arb(0)}
    prev = None
    for b in BV:
        Mb = Mser(b, 39)
        Dl = Mb if prev is None else {eta: Mb[eta] - prev[eta] for eta in etas}
        prev = Mb
        l = sum(1 for _, c in OUTER if c >= b)
        m0, m1, mf = mask("0", b), mask("1", b), mask("f", b)
        for eta in etas:
            pairs = [(a, c) for a in taus for c in taus if tuple(sorted(a + c)) == eta]
            D = Dl[eta]
            for r in range(n):
                if not mf[r]: continue
                wv = arb(0)
                for a, c in pairs:
                    wv += vl[(l, a)][r] * vl[(l, c)][r]
                term = wv * D[r]
                if m0[r]: Jf["0"] += term
                elif m1[r]: Jf["+"] += term
                else: Jf["t"] += term
        log_("layer b = %d done" % b)
    fac = 40 * A(h) / Z
    J0, Jp, Jt = Jf["0"] * fac, Jf["+"] * fac, Jf["t"] * fac
    ah, bh = A(fmpq(2479900401, 2500000000)), A(fmpq(-843183, 10 ** 9))
    Jl = J0 + (ah + bh) * Jp + bh * Jt
    ratio = A(fmpq(2624989, 10 ** 7)) * Jl / IH
    out.update(J0=J0.str(15, radius=True), Jplus=Jp.str(15, radius=True), Jt=Jt.str(15, radius=True),
               J_lambda=Jl.str(20, radius=True), J_lambda_mid=float(Jl.mid()), J_lambda_rad=float(Jl.rad()),
               J_ge_ref=bool(Jl > arb(90248755123) / 10 ** 24), ratio=ratio.str(15, radius=True),
               ratio_gt=bool(ratio > arb(500103) / 500000), prec=PREC, seconds=round(time.time() - t0))
    log_(json.dumps(out))
    if "--out" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)

def marginals(p, gvals, tj, log_):
    taus = sorted(set(SIGS))
    v = {}
    for si, ((r0, r1), M) in enumerate(OUTER):
        dm = cellmass(M)
        wbase = [gvals[a] * dm[a] for a in range(n)]
        wcache = {}
        def wpoly(e):
            if e not in wcache:
                wcache[e] = arb_poly([wbase[a] * tj[a] ** e for a in range(n)])
            return wcache[e]
        for s in SIGS:
            L = len(s)
            frev = arb_poly([p[s][n - 1 - i] if r0 <= n - 1 - i <= r1 else arb(0) for i in range(n)])
            for mask in range(1 << L):
                tau = tuple(sorted(s[i] for i in range(L) if not mask >> i & 1))
                e = sum(s[i] for i in range(L) if mask >> i & 1)
                prod = (frev * wpoly(e)).truncate(n)
                acc = v.setdefault((si, tau), [arb(0)] * n)
                for rp in range(n):
                    acc[rp] += prod[n - 1 - rp]
        log_("marginals shell %d done" % si)
    vl = {}
    for l in (1, 2, 3):
        for tau in taus:
            vl[(l, tau)] = [sum((v[(s, tau)][r] for s in range(l) if (s, tau) in v), arb(0)) for r in range(n)]
    return taus, vl

def jworker(b, p, gvals, g2, Z, tj, etas, Mser, log_):
    """By linearity in the layer measure: sum_a S(v^(l(a)), M^{b_a} - M^{b_{a-1}}; chi_a)
       = sum over caps b of [S(v^(l(a)), M^b; chi_a) for b = b_a] - [S(v^(l(a+1)), M^b; chi_{a+1}) for b = b_a].
    This worker returns both terms for its cap b (ball arithmetic, as strings)."""
    BV = sorted({c for _, c in OUTER} | {c for f in FACES.values() for _, c in f})
    ai = BV.index(b)
    taus, vl = marginals(p, gvals, tj, log_)
    Mb = Mser(b, 39)
    log_("M^b_39 done for b = %d" % b)
    def mask(F, bb):
        m = [0] * n
        for (r0, r1), c in FACES[F]:
            if c >= bb:
                for r in range(r0, r1 + 1): m[r] = 1
        return m
    def S(layer_b):
        l = sum(1 for _, c in OUTER if c >= layer_b)
        res = {"0": arb(0), "+": arb(0), "t": arb(0)}
        if l == 0: return res
        m0, m1, mf = mask("0", layer_b), mask("1", layer_b), mask("f", layer_b)
        for eta in etas:
            pairs = [(a, c) for a in taus for c in taus if tuple(sorted(a + c)) == eta]
            D = Mb[eta]
            for r in range(n):
                if not mf[r]: continue
                wv = arb(0)
                for a, c in pairs:
                    wv += vl[(l, a)][r] * vl[(l, c)][r]
                term = wv * D[r]
                if m0[r]: res["0"] += term
                elif m1[r]: res["+"] += term
                else: res["t"] += term
        return res
    plus = S(b)
    minus = S(BV[ai + 1]) if ai + 1 < len(BV) else {"0": arb(0), "+": arb(0), "t": arb(0)}
    out = {"b": b}
    for F in ("0", "+", "t"):
        d = plus[F] - minus[F]
        out[F] = [d.mid().str(60, radius=False), float(d.rad())]
        out[F + "_str"] = d.str(30, radius=True)
    json.dump(out, open("code/cap6/oai186_check2_J_b%d.json" % b, "w"), indent=1)
    log_(json.dumps(out))

if __name__ == "__main__":
    main()
