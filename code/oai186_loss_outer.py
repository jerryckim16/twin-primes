#!/usr/bin/env python3
"""Rung 186: RAW bounds R_G (2.17) and V_G (2.21) of the 52 OUTER loss components of L^+ in [14] (OpenAI,
"Numerical certificate for prime gaps at most 186", code/third_party/openai186/short_gaps_numerics.pdf), groups
O_2 (17 components) and O_{5/2} (35 components), recomputed from the paper's formulas and compared with Tables 2.1,
2.2 (code/oai186_tables_2_1_to_2_6.json: A = 10^18 R/I_H^-, B = 10^18 V/I_H^-, integers rounded UP by [14]).

Forms (Sec. 2.2 of [14]):
    R_G = 40 Lambda sum_{r<n} chi_G(r) W(r) sum_eta Q_eta(r) [X^r *] M_{40,eta}                         (2.17)
    C(r) = sum_{a=0}^{n-1-r} chi_G(r+a) W(r+a) K_a^{(0)},   H_eta(r) = [*]( C(r) [X^r] M_{39,eta} )      (2.20)
    V_G = (40 h^2 Lambda / Z) sum_{l in P(0, z_G)} S( v^(l), H ; w )                                     (2.21)
with M_{d,eta} = M_{d,eta}[K^{(2)}] the moments (2.10) of the component's retained arrays (profile g^2/Z) in the
marking ring of (2.16), K^{(0)} the same arrays with profile power 0 (no g, no Z) for the erased coordinate,
Q_eta (2.11) from the 77 trial coefficients, v^(l) the cap affine rows (2.13) (code/oai186_check2.py:marginals),
S the pairing (2.14), w(r) = 1 / max(|a_h+b_h|,|b_h|) / |b_h| for (r+39)h <= T0 / <= T1 / > T1.
chi_G: (1.25) with d_G = 40 on the full index, intersected with the outer face rows of (1.5) (union 0..98263), and
for a low bin clipped by (1.26): eligible rows = originating rows (1.22) with xi_t < u plus, for O_{5/2}, the rows of
O_2 (absorbed, own order); for an OUTER row the core c_t and threshold V_t are read as a_t and A_t of its predicate
O_t in (1.21) (a failing O_t needs s > a_t, and H_{mu,xi_t} > A_t with witness p <= u needs s > A_t - (mu-1)u).
W(r) = exp(theta (r h - U_G + (m_G - 1) u^+ + 40 h)) on the full index (Lemma 1.5); W = 1 for rank-two/factorial.
Kernels (Sec. 2.1) exactly as in code/oai186_loss_inner.py: low bins B_theta, M_theta (2.4)-(2.7) with the delay
recurrence when M >= 64 and the acceptance tests after (2.1) pass on 0 <= j < N, else the renewal majorant (2.3);
rank-two arrays (2.9) with Lemma 2.4 fractions; factorial arrays (2.8).
"For an outer low component, select the dyadic upper array once and use it in both source forms": we use the
same (ball) array in R and V.
Arithmetic: python-flint arb balls (default 256 bits): a high-precision RE-EVALUATION to compare with the printed
integers, not a certificate.  The authors' script is NOT used.

usage: oai186_loss_outer.py --group O5/2 [--comp L1,P1,H] [--prec 256] [--part out.json] [--schedule]
       oai186_loss_outer.py --combine parts/*.json -> code/cap6/oai186_loss_outer.json"""
import sys, json, time, os
from fractions import Fraction as Fr
from math import floor, ceil, factorial
import importlib.util, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HERE))
PREC = int(sys.argv[sys.argv.index("--prec") + 1]) if "--prec" in sys.argv else 256

def load(name, path, argv=("x",)):
    old = sys.argv
    sys.argv = list(argv)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    sys.argv = old
    return mod

TABLES = json.load(open("code/oai186_tables_2_1_to_2_6.json"))
IH_MINUS = Fr(23685317816, 10 ** 24)
AH, BH = Fr(2479900401, 2500000000), Fr(-843183, 10 ** 9)

def group_data(sd):
    h = sd.h
    o, nw = sd.ladders["o"], sd.ladders["n"]
    a_ = [Fr(6, 5) ** j / 20 for j in range(10)]
    S, e = sd.S, sd.e
    G = {}
    G["O2"] = dict(m=Fr(2), rows=[o[t] for t in range(24)] + [nw[t] for t in range(24)], absorbed=[], xi=o[23]["xi"],
                   U=S + e, b=nw[0]["a"], t=nw[24]["a"], z=49152, p=24576,
                   Ulist=lambda xi, p: [xi, 3 * xi / 2, a_[0]] + a_[4:9] + [(a_[8] + a_[9]) / 2, a_[9], p],
                   slope=7, special={"L3": 120}, T=[Fr(j, 6) for j in range(7)])
    G["O5/2"] = dict(m=Fr(5, 2), rows=[o[t] for t in range(24, 28)] + [nw[t] for t in range(24, 39)],
                     absorbed=[o[t] for t in range(24)] + [nw[t] for t in range(24)], xi=nw[38]["xi"],
                     U=S + e / 2, b=nw[24]["a"], t=98303 * h, z=46580, p=19660,
                     Ulist=lambda xi, p: [2 ** j * xi for j in range(9)] + [Fr(1, 100), Fr(3, 200), Fr(9, 400), Fr(27, 800)]
                     + a_[0:8] + [(a_[7] + p) / 2, p],
                     slope=7, special={}, T=[Fr(j, 16) for j in range(9)] + [Fr(5, 8), Fr(3, 4), Fr(7, 8), Fr(1)])
    for g, x in G.items():
        x["name"] = g
        x["d"] = 40
        assert floor(x["U"] / (2 * x["m"] * h)) == x["p"], g
        x["ulist"] = x["Ulist"](x["xi"], x["p"] * h)
        assert all(x["ulist"][i] < x["ulist"][i + 1] for i in range(len(x["ulist"]) - 1)), g
        x["R0"] = max(0, floor(x["b"] / h) - x["d"] + 1)
        x["R1"] = min(floor(x["t"] / h), 98263)
    return G

def clip_lower(G, u):
    elig = []
    for row in G["rows"] + G["absorbed"]:
        if row["xi"] < u:
            mu = Fr(5, 2) if row["r"] == 3 else Fr(2)
            elig.append(max(row["a"], row["A"] - (mu - 1) * u))
    if not elig:
        return None, dict(eligible=0)
    nabs = sum(1 for row in G["absorbed"] if row["xi"] < u)
    o3 = [max(r["a"], r["A"] - Fr(3, 2) * u) for r in G["rows"] if r["xi"] < u and r["r"] == 3]
    cmin = min(elig)
    return max(G["b"], cmin), dict(eligible=len(elig), absorbed_eligible=nabs, clipped=bool(cmin > G["b"]),
                                   below_all_absorbed=bool(G["absorbed"]) and nabs == 0,
                                   order3_min_is_bG=(max(G["b"], min(o3)) == G["b"]) if o3 else None)

def schedule(G):
    comps = []
    ul = G["ulist"]
    for j in range(1, len(ul)):
        name = "L%d" % j
        theta = G["special"].get(name, ceil(Fr(G["slope"]) / ul[j]))
        cG, info = clip_lower(G, ul[j])
        comps.append(dict(name=name, kind="L", l0=ul[j - 1], u0=ul[j], theta=theta, cG=cG, clip=info))
    q0 = G["U"] / (G["m"] + 1)
    zz = G["z"] * G["h"]
    T = G["T"]
    for j in range(1, len(T)):
        comps.append(dict(name="P%d" % j, kind="P", a=q0 + T[j - 1] * (zz - q0), b=q0 + T[j] * (zz - q0)))
    comps.append(dict(name="H", kind="H"))
    return comps

def schedule_report():
    sd = load("sd", "code/oai186_support_data.py")
    out = {}
    for g, G in group_data(sd).items():
        G["h"] = sd.h
        comps = schedule(G)
        lows = [c for c in comps if c["kind"] == "L"]
        out[g] = dict(R0=G["R0"], R1=G["R1"], n_low=len(lows), n_rank2=sum(c["kind"] == "P" for c in comps),
                      table_rows=len(TABLES[g]["rows"]),
                      lows=[dict(name=c["name"], u=float(c["u0"]), theta=c["theta"],
                                 lower_index=None if c["cG"] is None else max(G["R0"], floor(c["cG"] / sd.h) - 39),
                                 **c["clip"]) for c in lows])
    return out

def combine(files):
    res = {}
    for f in files:
        x = json.load(open(f))
        for c, v in x["components"].items():
            res[(x["group"], c)] = v
    rows = []
    for (g, c), v in sorted(res.items()):
        tab = {r["c"]: r for r in TABLES[g]["rows"]}[c]
        q = Fr(tab["q"], 10 ** 6)
        Eours = (q * Fr(v["A"]) + Fr(v["B"]) / q) / 10 ** 6
        rows.append(dict(group=g, component=c, table_A=tab["A"], table_B=tab["B"], table_E=tab["E"], q=tab["q"],
                         A=v["A"], B=v["B"], ratio_A=v["A"] / tab["A"], ratio_B=v["B"] / tab["B"],
                         E_from_ours=float(Eours), ceil_A_equals_table=bool(ceil(v["A"]) == tab["A"]),
                         ceil_B_equals_table=bool(ceil(v["B"]) == tab["B"]),
                         **{k: w for k, w in v.items() if k not in ("A", "B", "table_A", "table_B")}))
    return rows

def main():
    if "--schedule" in sys.argv:
        print(json.dumps(schedule_report(), indent=1, default=str))
        return
    if "--combine" in sys.argv:
        files = sys.argv[sys.argv.index("--combine") + 1:]
        rows = combine(files)
        json.dump(dict(units="A = 10^18 R/I_H^-, B = 10^18 V/I_H^- (table integers are upward-rounded upper bounds)",
                       rows=rows, schedule=schedule_report()), open("code/cap6/oai186_loss_outer.json", "w"), indent=1, default=str)
        for r in rows:
            print("%-5s %-4s A %18d / %22.4f (%.12f)  B %18d / %22.4f (%.12f)" % (
                r["group"], r["component"], r["table_A"], r["A"], r["ratio_A"], r["table_B"], r["B"], r["ratio_B"]))
        return
    c2 = load("c2", "code/oai186_check2.py", ("x", "--prec", str(PREC)))
    sd = load("sd", "code/oai186_support_data.py")
    from flint import arb, arb_poly, arb_series, fmpq, ctx
    ctx.prec = PREC
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    gname = sys.argv[sys.argv.index("--group") + 1]
    G = group_data(sd)[gname]
    G["h"] = sd.h
    comps_all = schedule(G)
    want = sys.argv[sys.argv.index("--comp") + 1].split(",") if "--comp" in sys.argv else [c["name"] for c in comps_all]
    comps = [c for c in comps_all if c["name"] in want]
    TABLE = {r["c"]: r for r in TABLES[gname]["rows"]}
    n, NG = c2.n, c2.NG
    hF = sd.h
    def Aq(q):
        q = Fr(q)
        return arb(q.numerator) / arb(q.denominator)
    harb = Aq(hF)
    m, UG, zK, pK = G["m"], G["U"], G["z"], G["p"]
    R0, R1 = G["R0"], G["R1"]
    nn = R1 + 1
    log_("group %s: m=%s z=%d p=%d chi = %d..%d; components %s" % (gname, m, zK, pK, R0, R1, [c["name"] for c in comps]))
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
    taus = sorted(set(c2.SIGS))
    etas = sorted({tuple(sorted(a + b)) for a in taus for b in taus})
    NR = R1 - R0 + 1
    # Q_eta on the chi_G range (full index)
    Qw = {}
    for eta in etas:
        pr = [(a, b) for a in taus for b in taus if tuple(sorted(a + b)) == eta]
        Qw[eta] = [sum((p[a][r] * p[b][r] for a, b in pr), arb(0)) for r in range(R0, R1 + 1)]
    _, vl = c2.marginals(p, gvals, tj, log_)
    c_caps = [68225, 49152, 46580, 0]
    Pset = [l for l in (1, 2, 3) if max(0, c_caps[l]) < min(zK, c_caps[l - 1])]
    # pair weights of the V form on the retained index r = 0..R1, radial weight w(r) folded in (U_eta below)
    T0, T1 = sd.T0, sd.T1
    wmid = Aq(max(abs(AH + BH), abs(BH)))
    wr = [arb(1) if (r + 39) * hF <= T0 else (wmid if (r + 39) * hF <= T1 else Aq(abs(BH))) for r in range(nn)]
    Uv = {}
    for eta in etas:
        pr = [(a, b) for a in taus for b in taus if tuple(sorted(a + b)) == eta]
        acc = [arb(0)] * nn
        for l in Pset:
            vv = {tau: vl[(l, tau)] for tau in taus}
            for a, b in pr:
                va, vb = vv[a], vv[b]
                for i in range(nn):
                    acc[i] += va[i] * vb[i]
        Uv[eta] = [acc[i] * wr[i] for i in range(nn)]
    del vl
    Mform = {39: {}, 40: {}}
    for d in (39, 40):
        for eta in etas:
            f = {}
            for pi in set_partitions(list(range(len(eta)))):
                E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
                f[E] = f.get(E, 0) + falling(d, len(pi))
            Mform[d][eta] = f
    allE = sorted({E for f in Mform[40].values() for E in f})
    EVALS = sorted({e for E in allE for e in E} | {0})
    tpow = {0: [arb(1)] * nn}
    for e in range(1, max(EVALS) + 1):
        tpow[e] = [tpow[e - 1][j] * tj[j] for j in range(nn)]
    log_("P(0,z_G) = %s; %d eta, %d block multisets; pair weights ready" % (Pset, len(etas), len(allE)))

    # ---------- kernels ----------
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
        dcache.clear()
        dcache[key] = (lo, up)
        return lo, up
    def accept(lo, up, length):
        for j in range(length):
            if not (lo[j] <= up[j]) or not (lo[j] >= 0) or not (up[j] <= 1):
                return False, j
            if j > 0 and (lo[j] > lo[j - 1] or up[j] > up[j - 1]):
                return False, j
        return True, None
    def renewal(M, length):
        R = [arb(1)] * (M + 1)
        ssum = arb(M)
        tiny = arb(10) ** -40
        floored = None
        for j in range(M + 1, length):
            if floored is not None:
                R.append(tiny); continue
            Rj = ssum / j
            if not (Rj > 0):
                raise ValueError("renewal: nonpositive lower endpoint")
            R.append(Rj)
            ssum = ssum + Rj - R[j - M]
            if Rj.upper() <= tiny.lower():
                floored = j
        return R, floored
    EU = {1: [1]}
    for r in range(2, 60):
        prev = EU[r - 1]
        EU[r] = [(a + 1) * (prev[a] if a < len(prev) else 0) + (r - a) * (prev[a - 1] if 0 <= a - 1 < len(prev) else 0) for a in range(r)]
    Epoly = lambda r: arb_poly([arb(x) / factorial(r) for x in EU[r]])
    Rpoly = lambda r: arb_poly([arb(1)] * r)

    def That(Q, J, rmax):
        """hat T_e, e = 0, 1 of (2.6)-(2.7) mod X^nn: sum_{r<=J} q_r E_{r+e+1} + (T_e - sum_{r<=J} q_r R_{r+e+1}).
        For rmax <= J (no tail) the finite sum is taken directly; otherwise T_e is the closed form
        (exp Q - X^{e+1} exp(X Q)) / (1 - X) of [14] (series exp in arb; 1/(1-X) = prefix sums)."""
        PE = [arb_poly([0]), arb_poly([0])]; PR = [arb_poly([0]), arb_poly([0])]
        q = arb_poly([1])
        for r in range(0, min(J, rmax) + 1):
            if r > 0:
                q = (q * Q).truncate(nn) * (arb(1) / r)
            for e in (0, 1):
                PE[e] += q * Epoly(r + e + 1)
                PR[e] += q * Rpoly(r + e + 1)
        if rmax <= J:
            return PE[0].truncate(nn), PE[1].truncate(nn)
        ctx.cap = nn
        eQ = arb_series(Q.coeffs()[:nn], prec=nn).exp().coeffs()
        XQ = [arb(0)] + Q.coeffs()[:nn - 1]
        eXQ = arb_series(XQ, prec=nn).exp().coeffs()
        eQ += [arb(0)] * (nn - len(eQ)); eXQ += [arb(0)] * (nn - len(eXQ))
        out = []
        for e in (0, 1):
            num = [eQ[j] - (eXQ[j - e - 1] if j >= e + 1 else arb(0)) for j in range(nn)]
            T, acc = [], arb(0)
            for j in range(nn):
                acc += num[j]; T.append(acc)
            pr = PR[e].coeffs() + [arb(0)] * nn
            pe = PE[e].coeffs() + [arb(0)] * nn
            out.append(arb_poly([pe[j] + (T[j] - pr[j]) for j in range(nn)]))
        return out[0], out[1]

    # ---------- ring moments, d = 39 (all monomials, r = 0..R1) and d = 40 (top, r in chi_G) ----------
    def rmul(X, Y, ok):
        out = {}
        for m1, a in X.items():
            for m2, b in Y.items():
                mm = tuple(i + k for i, k in zip(m1, m2))
                if ok(mm):
                    pr = (a * b).truncate(nn)
                    out[mm] = out[mm] + pr if mm in out else pr
        return out
    def rtop(X, Y, tgt):
        """[tgt] of the ring product X*Y (only the target monomial), truncated mod X^nn."""
        acc = None
        for m1, a in X.items():
            m2 = tuple(t - i for t, i in zip(tgt, m1))
            if m2 in Y:
                pr = (a * Y[m2]).truncate(nn)
                acc = pr if acc is None else acc + pr
        return acc
    def coeffs(poly, lo, hi):
        cf = poly.coeffs() if poly is not None else []
        return [cf[r] if r < len(cf) else arb(0) for r in range(lo, hi + 1)]
    def moments(arrays, ok, tgt, monos, C):
        """Returns (top40, sv): top40[E] = [X^r][tgt] P0^{40-|E|} prod_B P_{e_B} on r in R0..R1, and
        sv = sum_eta sum_E cf39(eta,E) sum_{r<=R1} U_eta(r) sum_mono C[tgt-mono](r) [X^r][mono] P0^{39-|E|} prod_B P_{e_B}
        (the V pairing (2.20)-(2.21) without its prefactor)."""
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
        kmin = 39 - max(len(E) for E in allE)
        p0 = {kmin: rpow(base, kmin)}
        for k in range(kmin + 1, 41):
            p0[k] = rmul(p0[k - 1], base, ok)
        top40, prod = {}, {}
        sv = arb(0)
        def getprod(E):
            if E not in prod:
                prod[E] = Pr[E[0]] if len(E) == 1 else rmul(getprod(E[:-1]), Pr[E[-1]], ok)
            return prod[E]
        for E in allE:
            top40[E] = coeffs(rtop(p0[40 - len(E)], getprod(E), tgt) if E else p0[40].get(tgt), R0, R1)
            users = [(eta, f[E]) for eta, f in Mform[39].items() if E in f]
            if users:
                full39 = rmul(p0[39 - len(E)], getprod(E), ok) if E else p0[39]
                GE = [arb(0)] * nn
                for mo in monos:
                    cm = tuple(t - i for t, i in zip(tgt, mo))
                    if cm not in C or mo not in full39:
                        continue
                    col = coeffs(full39[mo], 0, R1)
                    Cc = C[cm]
                    for r in range(nn):
                        GE[r] += Cc[r] * col[r]
                del full39
                for eta, cf in users:
                    U = Uv[eta]
                    acc = arb(0)
                    for r in range(nn):
                        acc += U[r] * GE[r]
                    sv += cf * acc
            for k in [k for k in prod if not any(F[:len(k)] == k and F > E for F in allE)]:
                del prod[k]
        return top40, sv

    def correl(f, K):
        """c(r) = sum_{a=0}^{nn-1-r} f(r+a) K(a), r = 0..R1 (f on the full index 0..R1), via (2.24)."""
        frev = arb_poly([f[nn - 1 - i] for i in range(nn)])
        pr = (frev * arb_poly(K[:nn])).truncate(nn)
        cf = pr.coeffs(); cf += [arb(0)] * (nn - len(cf))
        return [cf[nn - 1 - r] for r in range(nn)]

    results = {}
    def evaluate(name, arrays2, arrays0, ok, tgt, monos, f_full, lo_index, Lam, extra):
        C = {mo: correl(f_full, K) for mo, K in arrays0.items()}
        top40, sv = moments(arrays2, ok, tgt, monos, C)
        # R (2.17)
        s = arb(0)
        for eta in etas:
            Mt = [arb(0)] * NR
            for E, cf in Mform[40][eta].items():
                col = top40[E]
                for i in range(NR):
                    Mt[i] += cf * col[i]
            q = Qw[eta]
            for i in range(max(0, lo_index - R0), NR):
                s += q[i] * Mt[i] * f_full[R0 + i]
        Rv = 40 * Lam * s
        Vv = sv * 40 * harb * harb * Lam / Z
        scale = arb(10 ** 18) / Aq(IH_MINUS)
        AA, BB = Rv * scale, Vv * scale
        tab = TABLE[name]
        results[name] = dict(A=float(AA.mid()), A_rad=float(AA.rad()), B=float(BB.mid()), B_rad=float(BB.rad()),
                             table_A=tab["A"], table_B=tab["B"], **extra)
        log_("%s: A = %s (table %d, ratio %.12f)  B = %s (table %d, ratio %.12f)" % (
            name, AA.str(14), tab["A"], float(AA.mid()) / tab["A"], BB.str(14), tab["B"], float(BB.mid()) / tab["B"]))

    for c in comps:
        name = c["name"]
        if c["kind"] == "L":
            if c["cG"] is None:
                results[name] = dict(A=0.0, B=0.0, note="empty eligible set"); continue
            lo_index = max(R0, floor(c["cG"] / hF) - 39)
            Lb, Hb, Kb = floor(c["l0"] / hF), ceil(c["u0"] / hF), zK
            theta = c["theta"]
            assert 2 <= Lb < Hb <= Kb <= NG
            branch, first_bad, floored = "renewal", None, None
            if Lb >= 64:
                lo_d, up_d = dick(Lb, NG)
                okd, first_bad = accept(lo_d, up_d, NG)
                if okd:
                    branch = "delay"
            dup = up_d[:nn] if branch == "delay" else renewal(Lb, nn)[0]
            eth = (-Aq(theta * hF)).exp()
            Dt, cur = [], arb(1)
            for j in range(nn):
                Dt.append(dup[j] * cur); cur *= eth
            Dt = arb_poly(Dt)
            Q = arb_poly([arb(0)] * Lb + [arb(1) / a for a in range(Lb, Kb)])
            Mp = arb_poly([arb(0)] * Lb + [arb(1) / a for a in range(Lb, Hb)])
            J = min(32, (NG - 1) // Lb)
            rmax = (nn - 1) // Lb
            T0p, T1p = That(Q, J, rmax)
            bc = (Dt * T0p).truncate(nn).coeffs()
            mc = ((Dt * Mp).truncate(nn) * T1p).truncate(nn).coeffs()
            bc += [arb(0)] * (nn - len(bc)); mc += [arb(0)] * (nn - len(mc))
            arrays2 = {(0,): [w2[j] * bc[j] for j in range(nn)], (1,): [w2[j] * mc[j] for j in range(nn)]}
            arrays0 = {(0,): bc, (1,): mc}
            expo0 = Aq(theta * (-UG + (m - 1) * Hb * hF + 40 * hF))
            f_full = [(expo0 + Aq(theta * r * hF)).exp() if lo_index <= r <= R1 else arb(0) for r in range(nn)]
            log_("%s: L=%d H=%d theta=%d J=%d branch=%s (first failed test %s) lower index %d" % (
                name, Lb, Hb, theta, J, branch, first_bad, lo_index))
            evaluate(name, arrays2, arrays0, lambda mm: mm[0] <= 1, (1,), [(0,), (1,)], f_full, lo_index, arb(1),
                     dict(L=Lb, H=Hb, theta=theta, branch=branch, delay_first_failed=first_bad, lower_index=lo_index, clip=c["clip"]))
        elif c["kind"] == "P":
            a, b = c["a"], c["b"]
            rm, rp = (UG - b) / m, (UG - a) / m
            bP, rpP, rmM = ceil(b / hF), ceil(rp / hF), floor(rm / hF)
            cb, fa = ceil(b / hF), floor(a / hF)
            _, Lb_up = dick(bP, nn + 2)
            Lb_up = list(Lb_up)
            _, Lp_up = dick(rpP, nn + 2)
            Lp_up = list(Lp_up)
            Lm_lo, _ = dick(rmM, nn + 2)
            aA = Aq(a)
            Lam = (Aq(b) / aA).log()
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
                P_.append(Lb_up[j])
                A_.append(Lp_up[sm] * lam(tp) if tp > a else zero)
                B_.append((Lb_up[j] - Lm_lo[j + 1]).max(zero))
                beta = zero if j * hF < b else Lm_lo[sp]
                C_.append((Lb_up[sm] - beta).max(zero) * lam(min(tp, (m * tp - UG) / (m - 1))) if tp > a + rp else zero)
            arrays0 = {(0, 0): P_, (1, 0): A_, (0, 1): B_, (1, 1): C_}
            arrays2 = {mo: [w2[j] * K[j] for j in range(nn)] for mo, K in arrays0.items()}
            f_full = [arb(1) if R0 <= r <= R1 else arb(0) for r in range(nn)]
            log_("%s: a/h=%.3f b/h=%.3f Lambda=%s" % (name, float(a / hF), float(b / hF), Lam.str(10)))
            monos = [(0, 0), (1, 0), (0, 1), (1, 1)]
            evaluate(name, arrays2, arrays0, lambda mm: mm[0] <= 1 and mm[1] <= 1, (1, 1), monos, f_full, R0, Lam,
                     dict(a_over_h=float(a / hF), b_over_h=float(b / hF)))
        else:
            Lb, Kb = pK, zK
            _, dup = dick(Lb, nn + 1)
            D0 = arb_poly(dup[:nn])
            Q = arb_poly([arb(0)] * Lb + [arb(1) / a for a in range(Lb, Kb)])
            qs = [arb_poly([1])]
            for r in range(1, 8):
                qs.append((qs[-1] * Q).truncate(nn) * (arb(1) / r))
            arrays0 = {}
            for aa in range(4):
                bmax = (NG - 1 - aa * Lb) // Lb
                S_ = arb_poly([0])
                for bb in range(0, bmax + 1):
                    S_ += qs[bb] * Epoly(aa + bb + 1)
                Fa = (((D0 * qs[aa]).truncate(nn)) * S_.truncate(nn)).truncate(nn)
                fc = Fa.coeffs(); fc += [arb(0)] * (nn - len(fc))
                arrays0[(aa,)] = fc
            arrays2 = {mo: [w2[j] * K[j] for j in range(nn)] for mo, K in arrays0.items()}
            f_full = [arb(1) if R0 <= r <= R1 else arb(0) for r in range(nn)]
            log_("H: L=%d K=%d" % (Lb, Kb))
            evaluate("H", arrays2, arrays0, lambda mm: mm[0] <= 3, (3,), [(0,), (1,), (2,), (3,)], f_full, R0, arb(1),
                     dict(L=Lb, K=Kb))
    import resource
    out = dict(group=gname, components=results, prec=PREC, seconds=round(time.time() - t0),
               peak_rss_MB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
    if "--part" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--part") + 1], "w"), indent=1, default=str)
    log_(json.dumps(out, default=str))

def set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
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
