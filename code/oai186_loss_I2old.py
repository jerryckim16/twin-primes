#!/usr/bin/env python3
"""Rung 186: RAW component bounds of the inner group I_2^old of the support-failure loss L^+ of [14] (OpenAI,
short_gaps_numerics.pdf, Sec. 1.5, 2.1-2.2), recomputed from the transcription notes/sources-186-loss.md and
compared with Table 2.3 (code/oai186_tables_2_1_to_2_6.json: A = 10^18 beta_G / I_H^-, rounded up).

Seven components: L1..L5 (low bins from U_3), P1 (rank-two bin from T_3), H (third factorial).  Each is the
inner form (2.19)
    beta_G = (40 h Lambda / Z) sum_{l in P} S( v^(l), ([X^r *] M_{39,eta})_{eta,r} ; chi_G W ),
with M_{39,eta} the 39-coordinate moments (2.10) of the component's coordinate arrays taken in the marking ring
of (2.16) and [*] the selected coefficient:
    L_j : K = P + y D            (mod y^2),        [y]
    P_j : K = P + x A + y B + x y C (mod x^2, y^2), [xy]
    H   : K = F_0 + y F_1 + y^2 F_2 + y^3 F_3 (mod y^4), [y^3].
The moment formula M_{d,sigma}[K] = sum_pi (d)_{|pi|} P_0[K]^{d-|pi|} prod_B P_{e(B)}[K] is used verbatim over the
(commutative) marking ring.  v^(l) are the cap affine rows (2.13) (erased coordinate, outer caps, g^1, no 1/Z),
computed by code/oai186_check2.py:marginals (the code that reproduced J_{lambda,H}).

Group data (exact rationals from code/oai186_support_data.py, old ladder rows t = 12..23 = the order-two rows):
    m = 2, d = 39, xi_G = xi_23, U_G = T0 + e (= C_t of every nonterminal row, (1.17)), z_G = 44781 h,
    p_G = 22390 h.

READINGS (the transcription leaves these open; stated, not tuned):
 R1 radial interval (b_G, t_G] of (1.22)-(1.25) is not transcribed.  Reading: the order-two rows 12..23 occupy the
    second base shell of (1.18), so b_G = b_12 = B_12 - S, t_G = b_24.  (1.25) then gives
    floor(b_G/h) - 38 = 84931 <= r <= floor(t_G/h) = 87233.  Its lower end reproduces exactly the start of base row 2
    of (1.5); "intersect with the appropriate rows of (1.5)" is read two ways and BOTH are reported:
      chi_A: r in 84931..87233 (rows of H_0 = the whole base face; the upper end 87233 > 87194 crosses into row 3);
      chi_B: r in 84931..87194 (base row 2 only, the row whose cap 44781 h is z_G).
 R2 the clipping (1.26) needs the rows' cores c_t and thresholds V_t, not transcribed.  It is IMMATERIAL for this
    group under the natural reading c_t = b_t (row's lower radial boundary), V_t = U_G: every I2old bin end u_j >=
    a_0 = 0.05 > xi_12 = 0.04883, so row 12 is always eligible and max{c_12, V - u} = b_12 = b_G (V - a_0 < b_G),
    hence c_G(u) = b_G: no clipping.  (Consistent with Lemma 1.6, which only reports clipping for 5/2 groups.)
 R3 L_{<=l} in (1.36) = total of fragments <= l (as in the transcription note).  Low kernels: delay recurrence
    (2.1) upper point enclosure d^*_j = dbar_j(L h) (all five L >= 64).  The transcription says the delay branch
    is taken only "when M >= 64 and its acceptance tests pass", and the tests are not given.  Option --renewal
    L1,L2,... uses the renewal majorant (2.3) instead (sliding sum initialised to M).  RESULT: with the renewal
    majorant, L2 (M = 4703) and L3 (M = 9753) agree with Table 2.3 to about 2e-10, while with the delay recurrence they are
    2.7e-6 and 1.5e-7 low.  L4, L5 (M = 14045, 20225) agree with the delay recurrence.  So [14] apparently used renewal
    for the two smallest M of this group, i.e. the (unknown) acceptance test failed there.  This is inferred from the
    numbers, not from the transcription.  L1 rounds to the table value either way.  Option --fixed B (diagnostic)
    emulates the (2.22) upward fixed-point products at scale 2^B in the moment stage; at B = 192 it changes L2 by
    < 1e-12 relative, so it is not the source of the delay-branch gap;
    hat T_e computed as sum_{r<=J} q_r E_{r+e+1} + sum_{J<r} q_r R_{r+e+1} (= the transcribed tail T_e - prefix,
    exactly); hard cap z_0 = z_G; theta = ceil(7/u_j) (u_j the bin's upper endpoint, absolute length units).
    W(r) = exp(theta (r h - U_G + (m-1) u^+ + 39 h)) on the retained index r (inner group: no erased-coordinate tilt).
 R4 P = P(0, z_G) for L and H, P(q_-, q_+) for P1; both are {3} here (z_G < c_3), so only v^(3) enters.
 R5 rank-two arrays (2.9) as transcribed (b^+, r_+^+ rounded up, r_-^- rounded down to the grid; point enclosures
    of (2.1)), with the Lemma 2.4 fractions lambda(t_j^+) on A and lambda(min{t_j^+, (m t_j^+ - U)/(m-1)}) on C,
    Lambda = log(b/a) charged once; bin (a, b] = (U/3, z_G].
 R6 factorial arrays (2.8) with D_0 from dbar_j(L h), L = floor(p_G/h) = 22390 (no tilt), profile power two.
Arithmetic: python-flint arb / arb_poly balls (default 256 bits).  Coordinate arrays are ball MIDPOINT-free balls
(no outward dyadic extraction at 160 bits, no binary64 final reduction): this is a high-precision re-evaluation
of the forms to compare with the printed integers, NOT a certificate.  All polynomial products are truncated at
r <= 87233 (only those indices are paired).
Run time (this machine, 1 core each, 256 bits): ~8 min per low bin, 17 min for P1 and for H; peak RSS < 1.6 GB.
usage: oai186_loss_I2old.py [--prec 256] [--comp L1,L2,...] [--renewal L2,L3] [--fixed 192] [--part file.json]
       oai186_loss_I2old.py --combine part1.json ... ren_*.json   (files named ren_* = renewal alternative)
       -> code/cap6/oai186_loss_I2old.json"""
import sys, json, time, os
from fractions import Fraction as Fr
from math import floor, ceil, factorial
import importlib.util, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HERE))
PREC = int(sys.argv[sys.argv.index("--prec") + 1]) if "--prec" in sys.argv else 256
RENEWAL = sys.argv[sys.argv.index("--renewal") + 1].split(",") if "--renewal" in sys.argv else []   # diagnostic only
FIXED = int(sys.argv[sys.argv.index("--fixed") + 1]) if "--fixed" in sys.argv else 0   # diagnostic only

def load(name, path, argv=("x",)):
    old = sys.argv
    sys.argv = list(argv)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    sys.argv = old
    return mod

TABLE = json.load(open("code/oai186_tables_2_1_to_2_6.json"))["I2old"]["rows"]
IH_MINUS = Fr(23685317816, 10 ** 24)

def combine(files, renfiles):
    res, ren = {}, {}
    for f in files:
        res.update(json.load(open(f))["components"])
    for f in renfiles:
        ren.update(json.load(open(f))["components"])
    tab = {r["c"]: r["A"] for r in TABLE}
    rows = []
    for c in ["L1", "L2", "L3", "L4", "L5", "P1", "H"]:
        if c not in res:
            continue
        x = res[c]
        row = dict(component=c, table_A=tab[c], A_chiA=x["A_chiA"], A_chiB=x["A_chiB"],
                   ratio_chiA=x["A_chiA"] / tab[c], ratio_chiB=x["A_chiB"] / tab[c],
                   ceil_A_chiA_equals_table=bool(ceil(x["A_chiA"]) == tab[c]))
        if c in ren:
            r = ren[c]
            row.update(A_chiA_renewal=r["A_chiA"], ratio_chiA_renewal=r["A_chiA"] / tab[c],
                       ceil_A_chiA_renewal_equals_table=bool(ceil(r["A_chiA"]) == tab[c]),
                       A_chiB_renewal=r["A_chiB"])
        row.update({k: v for k, v in x.items() if k not in ("A_chiA", "A_chiB")})
        rows.append(row)
    return rows

def main():
    if "--combine" in sys.argv:
        args = sys.argv[sys.argv.index("--combine") + 1:]
        files = [a for a in args if "ren_" not in os.path.basename(a)]
        renfiles = [a for a in args if "ren_" in os.path.basename(a)]
        rows = combine(files, renfiles)
        out = dict(group="I2old", units="A = 10^18 beta_G / I_H^-, I_H^- = 23685317816e-24 (Table 2.3 integers are "
                   "upward-rounded upper bounds)", rows=rows,
                   main_reading="chi_A radial mask, delay recurrence d* for all low bins (as transcribed: M >= 64)",
                   alternative_renewal="low bins L1-L3 recomputed with the renewal majorant (2.3) for d*; the "
                   "transcription says the delay branch is used only if 'its acceptance tests pass' (tests not given)",
                   alternative_chiB="radial mask restricted to base row 2 (84931..87194): reproduces nothing",
                   readings=__doc__.split("READINGS")[1].split("Arithmetic:")[0].strip(),
                   run_seconds={os.path.basename(f): json.load(open(f)).get("seconds", 0) for f in args})
        json.dump(out, open("code/cap6/oai186_loss_I2old.json", "w"), indent=1)
        for r in rows:
            print("%-3s table %16d  chiA %20.3f (ratio %.10f)  renewal %s  chiB ratio %.6f" % (
                r["component"], r["table_A"], r["A_chiA"], r["ratio_chiA"],
                "%20.3f (ratio %.10f)" % (r["A_chiA_renewal"], r["ratio_chiA_renewal"]) if "A_chiA_renewal" in r else "-",
                r["ratio_chiB"]))
        return
    c2 = load("c2", "code/oai186_check2.py", ("x", "--prec", str(PREC)))
    sd = load("sd", "code/oai186_support_data.py")
    from flint import arb, arb_poly, fmpq, ctx
    ctx.prec = PREC
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    comps = sys.argv[sys.argv.index("--comp") + 1].split(",") if "--comp" in sys.argv else ["L1", "L2", "L3", "L4", "L5", "P1", "H"]
    n, NG = c2.n, c2.NG
    hF = Fr(2742997, 2624989) / NG
    assert hF == sd.h
    def Aq(q):
        q = Fr(q)
        return arb(q.numerator) / arb(q.denominator)
    harb = Aq(hF)
    KD, m = 39, Fr(2)
    old = sd.ladders["o"]
    xiG = old[23]["xi"]
    UG = sd.T0 + sd.e
    zK, pK = 44781, 22390
    assert floor(UG / (2 * m * hF)) == pK
    bG, tG = old[12]["b"], old[24]["b"]
    R0 = floor(bG / hF) - KD + 1
    R1 = floor(tG / hF)
    R1B = 87194
    assert R0 == 84931, R0
    log_("chi_A = %d..%d, chi_B = %d..%d" % (R0, R1, R0, R1B))
    # check of reading R2: no clipping
    a_ = [Fr(6, 5) ** j / 20 for j in range(10)]
    assert old[12]["xi"] < a_[0] and UG - a_[0] < bG
    nn = R1 + 1                                   # truncation length of all retained products
    # ---------- common data ----------
    tq = [(j + fmpq(1, 2)) * c2.h for j in range(n)]
    gvals = [c2.A(c2.gq(t)) for t in tq]
    g2 = [x * x for x in gvals]
    Z = sum(g2, arb(0))
    tj = [c2.A(t) for t in tq]
    w2 = [g2[j] / Z for j in range(nn)]
    xr = [(r + 20) * c2.h - fmpq(9, 10) for r in range(n)]
    p = {}
    for s in c2.SIGS:
        cc = [fmpq(v, 10 ** 10) for v in c2.TAB[s]]
        p[s] = [c2.A(sum((cc[d] * x ** d for d in range(7)), fmpq(0))) for x in xr]
    log_("Z = %s; p_sigma ready" % Z.str(15))
    taus, vl = c2.marginals(p, gvals, tj, log_)
    v3 = {tau: vl[(3, tau)][R0:R1 + 1] for tau in taus}
    del vl
    etas = sorted({tuple(sorted(a + b)) for a in taus for b in taus})
    Wl = {}
    for eta in etas:
        pr = [(a, b) for a in taus for b in taus if tuple(sorted(a + b)) == eta]
        Wl[eta] = [sum((v3[a][i] * v3[b][i] for a, b in pr), arb(0)) for i in range(R1 - R0 + 1)]
    Mform = {}
    for eta in etas:
        f = {}
        for pi in c2_set_partitions(list(range(len(eta)))):
            E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
            f[E] = f.get(E, 0) + falling(KD, len(pi))
        Mform[eta] = f
    allE = sorted({E for f in Mform.values() for E in f})
    EVALS = sorted({e for E in allE for e in E} | {0})
    tpow = {0: [arb(1)] * nn}
    for e in range(1, max(EVALS) + 1):
        tpow[e] = [tpow[e - 1][j] * tj[j] for j in range(nn)]
    log_("%d eta, %d block-sum multisets; pair weights on %d radial indices ready" % (len(etas), len(allE), R1 - R0 + 1))

    # ---------- Dickman point enclosures (2.1) ----------
    dcache = {}
    def dick(M, length):
        key = (M, length)
        if key in dcache:
            return dcache[key]
        lo = [arb(1)] * (M + 1); up = [arb(1)] * (M + 1)
        eps = arb(1) / (2 * M ** 3)
        zero, one = arb(0), arb(1)
        for j in range(M, length - 1):
            a1, a2 = arb(1) / (2 * j), arb(1) / (2 * (j + 1))
            l = lo[j] - up[j - M] * a1 - up[j + 1 - M] * a2
            u = up[j] - lo[j - M] * a1 - lo[j + 1 - M] * a2 + eps
            lo.append(l.lower().max(zero))
            up.append(u.upper().min(one))
        dcache[key] = (lo, up)
        return lo, up

    # ---------- Eulerian polynomials ----------
    EU = {1: [1]}
    for r in range(2, 60):
        prev = EU[r - 1]
        EU[r] = [(a + 1) * (prev[a] if a < len(prev) else 0) + (r - a) * (prev[a - 1] if 0 <= a - 1 < len(prev) else 0) for a in range(r)]
    def Epoly(r):
        return arb_poly([arb(x) / factorial(r) for x in EU[r]])
    def Rpoly(r):
        return arb_poly([arb(1)] * r)

    # ---------- ring machinery ----------
    def rmul(X, Y, ok):
        out = {}
        for m1, a in X.items():
            for m2, b in Y.items():
                mm = tuple(i + k for i, k in zip(m1, m2))
                if ok(mm):
                    pr = (a * b).truncate(nn) if True else None
                    out[mm] = out[mm] + pr if mm in out else pr
        return out
    def rtop(X, Y, tgt):
        acc = None
        for m1, a in X.items():
            m2 = tuple(t - i for t, i in zip(tgt, m1))
            if m2 in Y:
                pr = (a * Y[m2]).truncate(nn)
                acc = pr if acc is None else acc + pr
        return acc

    def moments_top(arrays, ok, tgt):
        """arrays: mono -> list K_j (j < nn).  Returns E -> coefficients [*] of P0^{39-|E|} prod_B P_{e_B} on R0..R1."""
        if FIXED:
            return moments_top_fixed(arrays, ok, tgt)
        Pr = {e: {mo: arb_poly([K[j] * tpow[e][j] for j in range(nn)]) for mo, K in arrays.items()} for e in EVALS}
        base = Pr[0]
        def rpow(X, k):
            res, b = None, X
            while k:
                if k & 1:
                    res = b if res is None else rmul(res, b, ok)
                k >>= 1
                if k:
                    b = rmul(b, b, ok)
            return res
        kmin = KD - max(len(E) for E in allE)
        p0 = {kmin: rpow(base, kmin)}
        for k in range(kmin + 1, KD + 1):
            p0[k] = rmul(p0[k - 1], base, ok)
        out = {}
        prod = {}
        def getprod(E):
            if E not in prod:
                prod[E] = Pr[E[0]] if len(E) == 1 else rmul(getprod(E[:-1]), Pr[E[-1]], ok)
            return prod[E]
        for E in allE:                                    # lexicographic: prefixes come first
            if E:
                poly = rtop(p0[KD - len(E)], getprod(E), tgt)
            else:
                poly = p0[KD].get(tgt)
            cf = poly.coeffs() if poly is not None else []
            out[E] = [cf[r] if r < len(cf) else arb(0) for r in range(R0, R1 + 1)]
            # free prefix products that no later multiset extends
            for k in [k for k in prod if not any(F[:len(k)] == k and F > E for F in allE)]:
                del prod[k]
        return out

    diag = {}
    def moments_top_fixed(arrays, ok, tgt):
        """Diagnostic emulation of the production arithmetic of [14] (2.22): positive coordinate arrays ceiled to
        integers at scale 2^FIXED, every product (A B)^+ = ceil(A^+ B^+ / 2^FIXED) coefficientwise (upper side only)."""
        from flint import fmpz_poly
        Bf = FIXED
        SCf = arb(2) ** Bf
        one = (1 << Bf) - 1
        def up(x):
            return int((x * SCf).upper().ceil().unique_fmpz())
        def fmul(a, b):
            c = (a * b).coeffs()[:nn]
            return fmpz_poly([(int(x) + one) >> Bf for x in c])
        def radd(X, Y):
            return X + Y
        def rmulf(X, Y):
            out = {}
            for m1, a in X.items():
                for m2, b in Y.items():
                    mm = tuple(i + k for i, k in zip(m1, m2))
                    if ok(mm):
                        pr = fmul(a, b)
                        out[mm] = out[mm] + pr if mm in out else pr
            return out
        def rtopf(X, Y):
            acc = None
            for m1, a in X.items():
                m2 = tuple(t - i for t, i in zip(tgt, m1))
                if m2 in Y:
                    pr = fmul(a, Y[m2])
                    acc = pr if acc is None else acc + pr
            return acc
        Pr = {e: {mo: fmpz_poly([up(K[j] * tpow[e][j]) for j in range(nn)]) for mo, K in arrays.items()} for e in EVALS}
        base = Pr[0]
        def rpow(X, k):
            res, b = None, X
            while k:
                if k & 1:
                    res = b if res is None else rmulf(res, b)
                k >>= 1
                if k:
                    b = rmulf(b, b)
            return res
        kmin = KD - max(len(E) for E in allE)
        p0 = {kmin: rpow(base, kmin)}
        for k in range(kmin + 1, KD + 1):
            p0[k] = rmulf(p0[k - 1], base)
        out, prod = {}, {}
        def getprod(E):
            if E not in prod:
                prod[E] = Pr[E[0]] if len(E) == 1 else rmulf(getprod(E[:-1]), Pr[E[-1]])
            return prod[E]
        for E in allE:
            poly = rtopf(p0[KD - len(E)], getprod(E)) if E else p0[KD].get(tgt)
            cf = poly.coeffs() if poly is not None else []
            out[E] = [arb(cf[r]) / SCf if r < len(cf) else arb(0) for r in range(R0, R1 + 1)]
            for k in [k for k in prod if not any(F[:len(k)] == k and F > E for F in allE)]:
                del prod[k]
        return out

    def pair(top, Wr):
        sA = arb(0); sB = arb(0)
        absA = 0.0; perr = [0.0] * (R1 - R0 + 1); nterm = 0
        for eta in etas:
            Mt = [arb(0)] * (R1 - R0 + 1)
            for E, cf in Mform[eta].items():
                col = top[E]
                for i in range(R1 - R0 + 1):
                    Mt[i] += cf * col[i]
            wl = Wl[eta]
            for i in range(R1 - R0 + 1):
                term = wl[i] * Mt[i] * Wr[i]
                sA += term
                tf = float(term.mid()); absA += abs(tf); perr[i] += tf; nterm += 1
                if R0 + i <= R1B:
                    sB += term
        # cancellation diagnostics for the final signed reduction (chi_A): sum |(eta, r) terms| and sum_r |sum_eta|
        diag.clear()
        diag.update(abs_eta_r=absA, abs_r=sum(abs(x) for x in perr), n_eta_r=nterm)
        return sA, sB

    results = {}
    def finish(name, sA, sB, Lam, extra):
        fac = 40 * harb * Lam / Z
        bA, bB = sA * fac, sB * fac
        scale = arb(10 ** 18) / Aq(IH_MINUS)
        AA, AB = bA * scale, bB * scale
        sAf = float(sA.mid())
        extra = dict(extra, cancel_ratio_eta_r=diag.get("abs_eta_r", 0) / sAf, cancel_ratio_r=diag.get("abs_r", 0) / sAf,
                     n_terms_eta_r=diag.get("n_eta_r"))
        results[name] = dict(A_chiA=float(AA.mid()), A_chiA_rad=float(AA.rad()), A_chiB=float(AB.mid()),
                             A_chiB_rad=float(AB.rad()), beta_chiA=float(bA.mid()), beta_chiB=float(bB.mid()), **extra)
        log_("%s: A(chi_A) = %s, A(chi_B) = %s, table %d" % (name, AA.str(12), AB.str(12),
                                                              {r["c"]: r["A"] for r in TABLE}[name]))

    # ---------- low bins ----------
    U3 = [xiG, a_[0], a_[4], a_[6], a_[8], pK * hF]
    ok1 = lambda mm: mm[0] <= 1
    for jb in range(1, 6):
        name = "L%d" % jb
        if name not in comps:
            continue
        l0, u0 = U3[jb - 1], U3[jb]
        Lb, Hb, Kb = floor(l0 / hF), ceil(u0 / hF), zK
        theta = ceil(Fr(7) / u0)
        assert 64 <= Lb < Hb <= Kb
        if name in RENEWAL:                                # diagnostic alternative: renewal majorant (2.3)
            dup = [arb(1)] * (Lb + 1)
            ssum = arb(Lb)                                 # sum_{a=j-M}^{j-1} R_a for j = M + 1
            for j in range(Lb + 1, nn + 1):
                Rj = ssum / j
                dup.append(Rj)
                ssum = ssum + Rj - dup[j - Lb]
        else:
            _, dup = dick(Lb, nn + 1)
        eth = (-Aq(theta * hF)).exp()
        Dt, cur = [], arb(1)
        for j in range(nn):
            Dt.append(dup[j] * cur); cur *= eth
        Dt = arb_poly(Dt)                                  # D_theta / h
        Q = arb_poly([arb(0)] * Lb + [arb(1) / a for a in range(Lb, Kb)])
        Mp = arb_poly([arb(0)] * Lb + [arb(1) / a for a in range(Lb, Hb)])
        J = min(32, (NG - 1) // Lb)
        rmax = (nn - 1) // Lb
        T0p = arb_poly([0]); T1p = arb_poly([0])
        q = arb_poly([1])
        for r in range(0, rmax + 1):
            if r > 0:
                q = (q * Q).truncate(nn) * (arb(1) / r)
            if r <= J:
                T0p += q * Epoly(r + 1); T1p += q * Epoly(r + 2)
            else:
                T0p += q * Rpoly(r + 1); T1p += q * Rpoly(r + 2)
        T0p, T1p = T0p.truncate(nn), T1p.truncate(nn)
        Bt = (Dt * T0p).truncate(nn)
        Mt = ((Dt * Mp).truncate(nn) * T1p).truncate(nn)
        bc, mc = Bt.coeffs(), Mt.coeffs()
        bc += [arb(0)] * (nn - len(bc)); mc += [arb(0)] * (nn - len(mc))
        arrays = {(0,): [w2[j] * bc[j] for j in range(nn)], (1,): [w2[j] * mc[j] for j in range(nn)]}
        log_("%s: L=%d H=%d K=%d theta=%d J=%d rmax=%d; kernels ready" % (name, Lb, Hb, Kb, theta, J, rmax))
        top = moments_top(arrays, ok1, (1,))
        expo0 = Aq(theta * (-UG + (m - 1) * Hb * hF + KD * hF))
        Wr = [(expo0 + Aq(theta * r * hF)).exp() for r in range(R0, R1 + 1)]
        sA, sB = pair(top, Wr)
        finish(name, sA, sB, arb(1), dict(L=Lb, H=Hb, K=Kb, theta=theta, J=J))

    # ---------- rank-two bin P1 ----------
    if "P1" in comps:
        a, b = UG / (m + 1), zK * hF
        rm, rp = (UG - b) / m, (UG - a) / m
        bP, rpP, rmM = ceil(b / hF), ceil(rp / hF), floor(rm / hF)
        cb, fa = ceil(b / hF), floor(a / hF)
        Lb_lo, Lb_up = dick(bP, nn + 2)
        Lp_lo, Lp_up = dick(rpP, nn + 2)
        Lm_lo, Lm_up = dick(rmM, nn + 2)
        aA, bA_ = Aq(a), Aq(b)
        Lam = (bA_ / aA).log()
        def lam(v):
            if v <= 0:
                return arb(0)
            x = (Aq(v) / aA).log() / Lam
            return x.max(arb(0)).min(arb(1))
        zero = arb(0)
        P_, A_, B_, C_ = [], [], [], []
        for j in range(nn):
            tp = (j + 1) * hF
            sm, sp = max(0, j - cb), max(0, j + 1 - fa)
            P_.append(w2[j] * Lb_up[j])
            A_.append(w2[j] * Lp_up[sm] * lam(tp) if tp > a else zero)
            B_.append(w2[j] * (Lb_up[j] - Lm_lo[j + 1]).max(zero))
            beta = zero if j * hF < b else Lm_lo[sp]
            C_.append(w2[j] * (Lb_up[sm] - beta).max(zero) * lam(min(tp, (m * tp - UG) / (m - 1))) if tp > a + rp else zero)
        arrays = {(0, 0): P_, (1, 0): A_, (0, 1): B_, (1, 1): C_}
        log_("P1: a/h=%.3f b/h=%d r_-^-/h=%d r_+^+/h=%d Lambda=%s; arrays ready" % (float(a / hF), bP, rmM, rpP, Lam.str(10)))
        top = moments_top(arrays, lambda mm: mm[0] <= 1 and mm[1] <= 1, (1, 1))
        sA, sB = pair(top, [arb(1)] * (R1 - R0 + 1))
        finish("P1", sA, sB, Lam, dict(a_over_h=float(a / hF), b_over_h=bP, rminus_over_h=rmM, rplus_over_h=rpP))

    # ---------- third factorial H ----------
    if "H" in comps:
        Lb, Kb = pK, zK
        _, dup = dick(Lb, nn + 1)
        D0 = arb_poly(dup[:nn])
        Q = arb_poly([arb(0)] * Lb + [arb(1) / a for a in range(Lb, Kb)])
        qs = [arb_poly([1])]
        for r in range(1, 6):
            qs.append((qs[-1] * Q).truncate(nn) * (arb(1) / r))
        arrays = {}
        for aa in range(4):
            bmax = (NG - 1 - aa * Lb) // Lb
            S_ = arb_poly([0])
            for bb in range(0, bmax + 1):
                S_ += qs[bb] * Epoly(aa + bb + 1)
            Fa = (((D0 * qs[aa]).truncate(nn)) * S_.truncate(nn)).truncate(nn)
            fc = Fa.coeffs(); fc += [arb(0)] * (nn - len(fc))
            arrays[(aa,)] = [w2[j] * fc[j] for j in range(nn)]
        log_("H: L=%d K=%d; factorial arrays ready" % (Lb, Kb))
        top = moments_top(arrays, lambda mm: mm[0] <= 3, (3,))
        sA, sB = pair(top, [arb(1)] * (R1 - R0 + 1))
        finish("H", sA, sB, arb(1), dict(L=Lb, K=Kb))

    import resource
    out = dict(components=results, prec=PREC, fixed_point_bits=FIXED, renewal_bins=RENEWAL, seconds=round(time.time() - t0),
               peak_rss_MB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
    if "--part" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--part") + 1], "w"), indent=1)
    log_(json.dumps(out))

def c2_set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for p in c2_set_partitions(rest):
        yield [[first]] + p
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]

def falling(d, r):
    out = 1
    for i in range(r):
        out *= d - i
    return out

if __name__ == "__main__":
    main()
