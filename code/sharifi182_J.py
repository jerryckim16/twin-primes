#!/usr/bin/env python3
"""Rung 182 (Session 14 follow-up 3): independent evaluation of the cap numerators J_0 and J_+ of the 182 trial
(bundle [M] (6.7), (7.4); published lower bounds trialJ0Lower, trialJPlusLower in code/data182/TrialData182_part1.lean).

  J_0 = sum_i int_{H_0} |E_i F|^2 dnu^38,  J_+ = sum_i int_{H_1 \\ H_0} |E_i F|^2 dnu^38   (cap forms; (hZ)^39 normalised).
Own derivation (the 186 layered form, code/oai186_J.py, extended by the trial's cap components):
  F(Y (+) X) != 0 needs the full index r = r' + a' (r' = index sum of the 38 retained coordinates, a' = cell of the
  erased one) in an outer shell s, every fragment of Y and X at most C_s, and component c contributes iff every
  fragment is at most c. Split the retained Y by the layer (b_{a-1}, b_a] of its largest fragment over ALL cap values
  that occur (components, outer shells, base and enlarged faces):
      b = 140306, 141720, 141724, 177528, 177542, 179967, 186253, 196608, 246256 (units h).
  On layer a, the components with c >= b_a and the outer shells with C_s >= b_a are open, the face row of r' must have
  cap >= b_a, and the erased coordinate X then only needs its own fragments <= min(c, C_s): its cell mass is
  d_{min(c, C_s)}(a'). Hence the erased marginal on layer a is
      v^a_tau(r') = sum_{s: C_s >= b_a} sum_{c: c >= b_a} sum_{(sigma, A labelled): sigma\\A = tau}
                    sum_{a'} chi_s(r'+a') p_{c,sigma}(r'+a') g_{a'} d_{min(c,C_s)}(a') t_{a'}^{e(A)},
  p_{c,sigma}(r) = sum_d coeff[c][sigma][d] B_{d,3}((r + 39/2) h), and
      J_F = (39 h / Z) sum_a sum_{r'} chi_{F,a}(r') sum_{tau, ups} v^a_tau v^a_ups [X^{r'}] Delta M^a_{38, tau+ups},
  with chi_{0,a} = base-face rows with cap >= b_a, chi_{+,a} = enlarged minus base. By linearity in Delta M each cap b
  is processed independently (worker --cap b): + S(v^{a(b)}, M^b; chi_{a(b)}) - S(v^{a(b)+1}, M^b; chi_{a(b)+1}).
Arithmetic: p in fixed point 2^-P (floored), coordinate arrays 2^-B (floored), exact GMP products and correlations,
exact integer sums: high precision, NOT a rigorous enclosure. One program.
usage: sharifi182_J.py --cap b        (writes code/data182/J_cap_<b>.json)
       sharifi182_J.py --combine [--out f.json]"""
import sys, json, time, os
from fractions import Fraction as Fr
import importlib.util
spec = importlib.util.spec_from_file_location("s182", "code/sharifi182_I.py")
s182 = importlib.util.module_from_spec(spec); spec.loader.exec_module(s182)
from mpmath import mp, mpf

D, h, n, B = s182.D, s182.h, s182.n, s182.B
KR = 38                                   # retained coordinates
P = 256                                   # fixed-point bits for p
COMP = [141720, 177528, 246256]
OUTER = [((0, 352697), 246256), ((352698, 376449), 196608), ((376450, 393176), 186253)]
FACES = {"0": [((0, 334253), 246256), ((334254, 343163), 177542), ((343164, 355047), 140306)],
         "1": [((0, 336274), 246256), ((336275, 343169), 179967), ((343170, 359896), 141724)]}
BV = sorted({c for c in COMP} | {c for _, c in OUTER} | {c for f in FACES.values() for _, c in f})
SIGS = D["signatures"]

def corr(I, w):
    """out[r] = sum_a I[r + a] w[a] over r + a < n; I signed ints, w >= 0 ints. Exact."""
    off = max(abs(x) for x in I)
    if off == 0:
        return [0] * n
    rev = [I[n - 1 - i] + off for i in range(n)]
    W = (max(rev).bit_length() + max(w).bit_length() + n.bit_length() + 8) // 8 + 1
    prod = s182.unpack(s182.pack(rev, W) * s182.pack(w, W), W, n)
    pre = [0] * (n + 1)
    for a in range(n):
        pre[a + 1] = pre[a] + w[a]
    return [prod[n - 1 - r] - off * pre[n - r] for r in range(n)]

def p_arrays():
    """fixed-point p_{c,sigma}(r) * 2^P for each component c and signature sigma."""
    knots, coeff = D["knots"], D["coeff"]
    out = {(c, s): [0] * n for c in range(3) for s in range(11)}
    for i in range(len(knots) - 1):
        if not knots[i] < knots[i + 1]:
            continue
        lo = knots[i] / h - Fr(39, 2); hi = knots[i + 1] / h - Fr(39, 2)
        rlo = max(0, -((-lo.numerator) // lo.denominator)); rhi = min(n - 1, -((-hi.numerator) // hi.denominator) - 1)
        if rlo > rhi:
            continue
        bp = [s182.to_r(p) for p in s182.bspline_span_polys(knots, i)]
        for c in range(3):
            for s in range(11):
                pp = [Fr(0)] * 4
                for d in range(22):
                    for k, x in enumerate(bp[d]):
                        pp[k] += coeff[c][s][d] * x
                Dsp = 1
                for x in pp:
                    Dsp = Dsp * x.denominator // __import__("math").gcd(Dsp, x.denominator)
                ic = [int(x * Dsp) for x in pp]
                arr = out[(c, s)]
                for r in range(rlo, rhi + 1):
                    arr[r] = ((((ic[3] * r + ic[2]) * r + ic[1]) * r + ic[0]) << P) // Dsp
    return out

def main():
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    if "--combine" in sys.argv:
        tot = {"0": Fr(0), "+": Fr(0)}
        for b in BV:
            d = json.load(open("code/data182/J_cap_%d.json" % b))
            for F_ in tot:
                tot[F_] += Fr(d[F_])
        lo0, lop = D["trialJ0Lower"], D["trialJPlusLower"]
        out = dict(J0=float(tot["0"]), Jplus=float(tot["+"]), J0_ref_lower=float(lo0), Jplus_ref_lower=float(lop),
                   J0_ge_ref=bool(tot["0"] >= lo0), Jplus_ge_ref=bool(tot["+"] >= lop),
                   J0_rel_excess=float(tot["0"] / lo0 - 1), Jplus_rel_excess=float(tot["+"] / lop - 1))
        log_(json.dumps(out))
        if "--out" in sys.argv:
            json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)
        return
    b = int(sys.argv[sys.argv.index("--cap") + 1])
    ai = BV.index(b)
    layers = [ai] + ([ai + 1] if ai + 1 < len(BV) else [])
    pfix = p_arrays()
    log_("p arrays (fixed point 2^%d)" % P)
    # (tau, e) rows: mult of (sigma, labelled A) with sigma \ A = tau, e = e(A)
    rowspec = {}
    for si, sg in enumerate(SIGS):
        L = len(sg)
        for mask in range(1 << L):
            tau = tuple(sorted(sg[i] for i in range(L) if not mask >> i & 1))
            e = sum(sg[i] for i in range(L) if mask >> i & 1)
            rowspec.setdefault((tau, e), {}); rowspec[(tau, e)][si] = rowspec[(tau, e)].get(si, 0) + 1
    taus = sorted({t for (t, _) in rowspec})
    # profile, Z
    tq = [(j + Fr(1, 2)) * h for j in range(n)]
    gv = []
    for t in tq:
        v = s182.gq(t); gv.append(mpf(v.numerator) / v.denominator)
    g2 = [x * x for x in gv]
    Z = mp.fsum(g2)
    tj = [mpf(t.numerator) / t.denominator for t in tq]
    SC = mpf(2) ** B
    dcache = {}
    def dmass(m):
        if m not in dcache:
            dcache[m] = s182.cellmass(m)
        return dcache[m]
    # erased marginals for the needed layers
    V = {}
    for la in layers:
        bl = BV[la]
        acc = {tau: [0] * n for tau in taus}
        groups = {}                       # (component, erased cap m) -> list of outer row ranges (merged shells)
        for (r0, r1), Cs in OUTER:
            if Cs < bl:
                continue
            for ci, c in enumerate(COMP):
                if c >= bl:
                    groups.setdefault((ci, min(c, Cs)), []).append((r0, r1))
        for (ci, m), ranges in sorted(groups.items()):
            if True:
                dm = dmass(m)
                wcache = {}
                for (tau, e), sm in rowspec.items():
                    if e not in wcache:
                        wcache[e] = [int(mp.floor(gv[a] * dm[a] * tj[a] ** e * SC)) for a in range(n)]
                    I = [0] * n
                    for si, mult in sm.items():
                        arr = pfix[(ci, si)]
                        for (r0, r1) in ranges:
                            for r in range(r0, r1 + 1):
                                if arr[r]:
                                    I[r] += mult * arr[r]
                    cc = corr(I, wcache[e])
                    A = acc[tau]
                    for r in range(n):
                        A[r] += cc[r]
        V[la] = acc
        log_("layer %d (b = %d): marginals" % (la, bl))
    # M^b_38
    pairs = {}
    for t1 in taus:
        for t2 in taus:
            pairs.setdefault(tuple(sorted(t1 + t2)), []).append((t1, t2))
    etas = sorted(pairs)
    Mform = {}
    for eta in etas:
        f = {}
        for pi in s182.set_partitions(list(range(len(eta)))):
            E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
            f[E] = f.get(E, 0) + s182.falling(KR, len(pi))
        Mform[eta] = f
    allE = sorted({E for f in Mform.values() for E in f}, key=lambda E: (len(E), E))
    dm = dmass(b)
    K = [g2[j] * dm[j] / Z for j in range(n)]
    Pa = {e: [max(int(mp.floor(K[j] * tj[j] ** e * SC)), 0) for j in range(n)] for e in [0] + list(range(2, 13))}
    p0 = {KR - 6: s182.ppow(Pa[0], KR - 6)}
    for k in range(KR - 5, KR + 1):
        p0[k] = s182.pmul(p0[k - 1], Pa[0])
    prod = {}
    def getprod(E):
        if E not in prod:
            prod[E] = Pa[E[0]] if len(E) == 1 else s182.pmul(getprod(E[:-1]), Pa[E[-1]])
        return prod[E]
    ME = {E: (p0[KR - len(E)] if not E else s182.pmul(p0[KR - len(E)], getprod(E))) for E in allE}
    prod.clear(); p0.clear(); Pa.clear()
    log_("M^b_38 products done")
    def mask(F_, bb):
        m = [0] * n
        for (r0, r1), c in FACES[F_]:
            if c >= bb:
                for r in range(r0, r1 + 1):
                    m[r] = 1
        return m
    res = {"0": 0, "+": 0}
    for k, la in enumerate(layers):
        sgn = 1 if k == 0 else -1
        bl = BV[la]
        m0, m1 = mask("0", bl), mask("1", bl)
        v = V[la]
        for eta in etas:
            M = [0] * n
            for E, cf in Mform[eta].items():
                arr = ME[E]
                for r in range(n):
                    M[r] += cf * arr[r]
            pl = [(v[a], v[c]) for (a, c) in pairs[eta]]
            t0_ = tp_ = 0
            for r in range(n):
                if not m1[r]:
                    continue
                w = 0
                for (x, y) in pl:
                    w += x[r] * y[r]
                if w:
                    if m0[r]:
                        t0_ += w * M[r]
                    else:
                        tp_ += w * M[r]
            res["0"] += sgn * t0_; res["+"] += sgn * tp_
    fac = 39 * h / Fr(mp.nstr(Z, 100))
    scale = Fr(1, 1 << (2 * (P + B) + B))
    out = {F_: str(Fr(res[F_]) * scale * fac) for F_ in res}
    out.update(cap=b, J0_float=float(Fr(out["0"])), Jplus_float=float(Fr(out["+"])), seconds=round(time.time() - t0))
    json.dump(out, open("code/data182/J_cap_%d.json" % b, "w"), indent=1)
    log_("cap %d: J0 part %.12e, J+ part %.12e" % (b, out["J0_float"], out["Jplus_float"]))

if __name__ == "__main__":
    main()
