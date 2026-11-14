#!/usr/bin/env python3
"""Rung 186: RAW bounds of all 45 INNER loss components of L^+ in [14] (OpenAI, "Numerical certificate for prime
gaps at most 186", code/third_party/openai186/short_gaps_numerics.pdf), groups I_2^old, I_{5/2}^old, I_2^new,
I_{5/2}^new, recomputed from the paper's formulas and compared with Tables 2.3-2.6
(code/oai186_tables_2_1_to_2_6.json; A = 10^18 beta_G / I_H^-, integers rounded UP by [14]).

Generalises code/oai186_loss_I2old.py (Session 15), which had to INFER two pieces of group data; both are now read
in the PDF (committed in Session 16):
  * radial intervals (b_G, t_G] and caps z_G, p_G: (1.23)-(1.24), p. 6;
  * the clipping (1.26): eligible rows = originating rows (1.22) with xi_t < u, plus, for m_G = 5/2, the rows of the
    preceding order-two group ("absorbed", keeping their own order mu_t = 2); core c_t and threshold V_t of an
    inner row are read as the radial boundary b_t and the threshold C_t of its predicate I_t in (1.21) (a failing
    I_t needs s > b_t, and H_{mu,xi} > C_t with a witness p <= u needs s > C_t - (mu - 1) u, which is the stated
    implication of Sec. 1.5.2);
  * the delay-vs-renewal rule (2.3): delay recurrence (2.1) when M >= 64 AND its acceptance tests pass, where the
    tests are those stated after (2.1): "accept only ordered intervals in [0,1] with both endpoint sequences
    nonincreasing".  We apply them on 0 <= j < N (the kernel length of (2.4)); the result of the test is recorded.
    Session 15 had found, from the numbers alone, that L2 and L3 of I_2^old used renewal: this is now a prediction
    that the test either confirms or refutes.
Remaining readings (unchanged from Session 15, stated, not tuned): L_{<=l} = total of fragments <= l; chi_G =
(1.25) interval intersected with the union of the face rows of (1.5) (base face H_0 for "old", enlarged face H_1
for "new"); P = P(0, z_G) for low/factorial, P(q_-, q_+) for rank-two (both {3} for every inner group since
z_G < c_3 = 46580 h); rank-two arrays (2.9) with the Lemma 2.4 fractions; factorial arrays (2.8) with dbar(Lh).
The renewal majorant is floored at 10^-40 once its upper bound is <= 10^-40 (as in (2.3)).

Arithmetic: python-flint arb balls (default 256 bits), no dyadic extraction, no binary64 reduction: a
high-precision RE-EVALUATION of the forms to compare with the printed integers, not a certificate.
The authors' script (code/third_party/openai186/prime_gap_186_certificate.py) is NOT used here.

usage: oai186_loss_inner.py --group I5/2old [--comp L1,P1,H] [--prec 256] [--part out.json]
       oai186_loss_inner.py --combine parts/*.json  -> code/cap6/oai186_loss_inner.json"""
import sys, json, time, os, glob
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

def group_data(sd):
    """Group parameters from (1.22)-(1.24) and the bin schedules of Sec. 1.5.1 (exact rationals)."""
    h = sd.h
    o, nw = sd.ladders["o"], sd.ladders["n"]
    a_ = [Fr(6, 5) ** j / 20 for j in range(10)]
    T0, T1, e = sd.T0, sd.T1, sd.e
    G = {}
    # face rows of (1.5): union = [0, facemax]
    G["I2old"] = dict(m=Fr(2), rows=[o[t] for t in range(12, 24)], absorbed=[], xi=o[23]["xi"], U=T0 + e,
                      b=o[12]["b"], t=o[24]["b"], z=44781, p=22390, facemax=89524,
                      Ulist=lambda xi, p: [xi, a_[0], a_[4], a_[6], a_[8], p], slope=7,
                      T=[Fr(0), Fr(1)])
    G["I5/2old"] = dict(m=Fr(5, 2), rows=[o[t] for t in range(24, 28)], absorbed=[o[t] for t in range(12, 24)],
                        xi=o[27]["xi"], U=T0 + e / 2, b=o[24]["b"], t=89563 * h, z=35265, p=17912, facemax=89524,
                        Ulist=lambda xi, p: [xi, 2 * xi, Fr(1, 100), Fr(27, 800), a_[3], a_[5], a_[6], p], slope=7,
                        T=[Fr(0), Fr(1, 2), Fr(1)])
    G["I2new"] = dict(m=Fr(2), rows=[nw[t] for t in range(12, 24)], absorbed=[], xi=nw[23]["xi"], U=T1 + e,
                      b=nw[12]["b"], t=nw[24]["b"], z=44976, p=22488, facemax=89914,
                      Ulist=lambda xi, p: [xi, a_[1], a_[4], a_[5], a_[7], a_[8], p], slope=7,
                      T=[Fr(0), Fr(1, 6), Fr(1, 2), Fr(2, 3), Fr(1)])
    G["I5/2new"] = dict(m=Fr(5, 2), rows=[nw[t] for t in range(24, 39)], absorbed=[nw[t] for t in range(12, 24)],
                        xi=nw[38]["xi"], U=T1 + e / 2, b=nw[24]["b"], t=89953 * h, z=35419, p=17990, facemax=89914,
                        Ulist=lambda xi, p: [2 ** j * xi for j in (0, 1, 4, 6, 8)] + [Fr(9, 400), a_[1], a_[3], a_[5], a_[6], a_[7], p],
                        slope=9, T=[Fr(0), Fr(1, 8), Fr(3, 8), Fr(1, 2), Fr(3, 4), Fr(1)])
    for g, x in G.items():
        x["name"] = g
        x["d"] = 39
        assert floor(x["U"] / (2 * x["m"] * h)) == x["p"], g
        x["ulist"] = x["Ulist"](x["xi"], x["p"] * h)
        assert all(x["ulist"][i] < x["ulist"][i + 1] for i in range(len(x["ulist"]) - 1)), g
        x["R0"] = max(0, floor(x["b"] / h) - x["d"] + 1)
        x["R1"] = min(floor(x["t"] / h), x["facemax"])
    return G

def clip_lower(G, u, h):
    """(1.26): c_G(u) = max{b_G, min_{t: xi_t < u} max{c_t, V_t - (mu_t - 1) u}}; returns (c_G(u) or None, info)."""
    elig = []
    for row in G["rows"] + G["absorbed"]:
        if row["xi"] < u:
            mu = Fr(5, 2) if row["r"] == 3 else Fr(2)
            elig.append(max(row["b"], row["C"] - (mu - 1) * u))
    if not elig:
        return None, dict(eligible=0)
    nabs = sum(1 for row in G["absorbed"] if row["xi"] < u)
    cmin = min(elig)
    return max(G["b"], cmin), dict(eligible=len(elig), absorbed_eligible=nabs, clipped=bool(cmin > G["b"]),
                                   below_all_absorbed=bool(G["absorbed"]) and nabs == 0,
                                   order3_min_is_bG=(min(max(r["b"], r["C"] - Fr(3, 2) * u) for r in G["rows"]
                                                         if r["xi"] < u) == G["b"]) if any(r["xi"] < u for r in G["rows"]) else None)

def schedule(G, h):
    """Low bins, rank-two bins and the factorial component, with their parameters."""
    comps = []
    ul = G["ulist"]
    for j in range(1, len(ul)):
        l0, u0 = ul[j - 1], ul[j]
        theta = ceil(Fr(G["slope"]) / u0)
        cG, info = clip_lower(G, u0, h)
        comps.append(dict(name="L%d" % j, kind="L", l0=l0, u0=u0, theta=theta, cG=cG, clip=info))
    q0 = G["U"] / (G["m"] + 1)
    zz = G["z"] * h
    T = G["T"]
    for j in range(1, len(T)):
        comps.append(dict(name="P%d" % j, kind="P", a=q0 + T[j - 1] * (zz - q0), b=q0 + T[j] * (zz - q0)))
    comps.append(dict(name="H", kind="H"))
    return comps

def schedule_report():
    sd = load("sd", "code/oai186_support_data.py")
    GG = group_data(sd)
    out = {}
    for g, G in GG.items():
        comps = schedule(G, sd.h)
        lows = [c for c in comps if c["kind"] == "L"]
        out[g] = dict(R0=G["R0"], R1=G["R1"], n_low=len(lows), n_rank2=sum(c["kind"] == "P" for c in comps),
                      lows=[dict(name=c["name"], u=float(c["u0"]), theta=c["theta"],
                                 lower_index=(None if c["cG"] is None else max(G["R0"], floor(c["cG"] / sd.h) - 38)),
                                 **{k: v for k, v in c["clip"].items()}) for c in lows],
                      table_rows=len(TABLES[tkey(g)]["rows"]))
    return out

def tkey(g):
    return g.replace("/", "")

def combine(files):
    res = {}
    for f in files:
        x = json.load(open(f))
        for c, v in x["components"].items():
            res[(x["group"], c)] = dict(v, seconds_part=x.get("seconds"))
    rows = []
    for (g, c), v in sorted(res.items()):
        tab = {r["c"]: r["A"] for r in TABLES[tkey(g)]["rows"]}[c]
        rows.append(dict(group=g, component=c, table_A=tab, A=v["A"], ratio=v["A"] / tab if tab else None,
                         ceil_equals_table=bool(ceil(v["A"]) == tab), within_1e9=abs(v["A"] / tab - 1) < 1e-9 if tab else None,
                         **{k: w for k, w in v.items() if k not in ("A",)}))
    return rows

def main():
    if "--schedule" in sys.argv:
        print(json.dumps(schedule_report(), indent=1, default=str))
        return
    if "--combine" in sys.argv:
        files = sys.argv[sys.argv.index("--combine") + 1:]
        rows = combine(files)
        out = dict(units="A = 10^18 beta_G / I_H^-, I_H^- = 23685317816e-24 (Table integers are upward-rounded upper bounds)",
                   rows=rows, schedule=schedule_report(),
                   readings=__doc__.split("Remaining readings")[1].split("Arithmetic:")[0].strip())
        json.dump(out, open("code/cap6/oai186_loss_inner.json", "w"), indent=1, default=str)
        for r in rows:
            print("%-8s %-3s table %16d  ours %22.4f  ratio %.12f  %s  d*=%s" % (
                r["group"], r["component"], r["table_A"], r["A"], r["ratio"] or 0,
                "ceil=table" if r["ceil_equals_table"] else "", r.get("branch", "")))
        return
    c2 = load("c2", "code/oai186_check2.py", ("x", "--prec", str(PREC)))
    sd = load("sd", "code/oai186_support_data.py")
    from flint import arb, arb_poly, fmpq, ctx
    ctx.prec = PREC
    t0 = time.time()
    log_ = lambda s: print("[%6.0f s] %s" % (time.time() - t0, s), flush=True)
    gname = sys.argv[sys.argv.index("--group") + 1]
    GG = group_data(sd)
    G = GG[gname]
    comps_all = schedule(G, sd.h)
    want = sys.argv[sys.argv.index("--comp") + 1].split(",") if "--comp" in sys.argv else [c["name"] for c in comps_all]
    comps = [c for c in comps_all if c["name"] in want]
    TABLE = {r["c"]: r["A"] for r in TABLES[tkey(gname)]["rows"]}
    n, NG = c2.n, c2.NG
    hF = sd.h
    assert hF == Fr(2742997, 2624989) / NG
    def Aq(q):
        q = Fr(q)
        return arb(q.numerator) / arb(q.denominator)
    harb = Aq(hF)
    KD, m, UG, zK, pK = G["d"], G["m"], G["U"], G["z"], G["p"]
    R0, R1 = G["R0"], G["R1"]
    log_("group %s: m=%s z=%d p=%d chi = %d..%d; components %s" % (gname, m, zK, pK, R0, R1, [c["name"] for c in comps]))
    nn = R1 + 1
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
    taus, vl = c2.marginals(p, gvals, tj, log_)
    # P-set (2.18): all inner components use {3}
    c_caps = [68225, 49152, 46580, 0]
    Pset = [l for l in (1, 2, 3) if max(0, c_caps[l]) < min(zK, c_caps[l - 1])]
    assert Pset == [3], Pset
    v3 = {tau: vl[(3, tau)][R0:R1 + 1] for tau in taus}
    del vl
    NR = R1 - R0 + 1
    etas = sorted({tuple(sorted(a + b)) for a in taus for b in taus})
    Wl = {}
    for eta in etas:
        pr = [(a, b) for a in taus for b in taus if tuple(sorted(a + b)) == eta]
        Wl[eta] = [sum((v3[a][i] * v3[b][i] for a, b in pr), arb(0)) for i in range(NR)]
    Mform = {}
    for eta in etas:
        f = {}
        for pi in set_partitions(list(range(len(eta)))):
            E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
            f[E] = f.get(E, 0) + falling(KD, len(pi))
        Mform[eta] = f
    allE = sorted({E for f in Mform.values() for E in f})
    EVALS = sorted({e for E in allE for e in E} | {0})
    tpow = {0: [arb(1)] * nn}
    for e in range(1, max(EVALS) + 1):
        tpow[e] = [tpow[e - 1][j] * tj[j] for j in range(nn)]
    log_("%d eta, %d block-sum multisets on %d radial indices ready" % (len(etas), len(allE), NR))

    # ---------- Dickman point enclosures (2.1), with the acceptance test ----------
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
    def accept(lo, up, length):
        """Acceptance tests after (2.1): ordered intervals in [0,1], both endpoint sequences nonincreasing."""
        first_bad = None
        for j in range(length):
            l, u = lo[j], up[j]
            bad = not (l <= u) or not (l >= 0) or not (u <= 1)
            if j > 0 and (lo[j] > lo[j - 1] or up[j] > up[j - 1]):
                bad = True
            if bad:
                first_bad = j
                break
        return first_bad is None, first_bad
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
                    pr = (a * b).truncate(nn)
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
        out, prod = {}, {}
        def getprod(E):
            if E not in prod:
                prod[E] = Pr[E[0]] if len(E) == 1 else rmul(getprod(E[:-1]), Pr[E[-1]], ok)
            return prod[E]
        for E in allE:
            poly = rtop(p0[KD - len(E)], getprod(E), tgt) if E else p0[KD].get(tgt)
            cf = poly.coeffs() if poly is not None else []
            out[E] = [cf[r] if r < len(cf) else arb(0) for r in range(R0, R1 + 1)]
            for k in [k for k in prod if not any(F[:len(k)] == k and F > E for F in allE)]:
                del prod[k]
        return out
    def pair(top, Wr, lo_index):
        s = arb(0)
        for eta in etas:
            Mt = [arb(0)] * NR
            for E, cf in Mform[eta].items():
                col = top[E]
                for i in range(NR):
                    Mt[i] += cf * col[i]
            wl = Wl[eta]
            for i in range(max(0, lo_index - R0), NR):
                s += wl[i] * Mt[i] * Wr[i]
        return s
    results = {}
    def finish(name, s, Lam, extra):
        beta = s * 40 * harb * Lam / Z
        AA = beta * arb(10 ** 18) / Aq(IH_MINUS)
        results[name] = dict(A=float(AA.mid()), A_rad=float(AA.rad()), beta=float(beta.mid()), table_A=TABLE[name], **extra)
        log_("%s: A = %s, table %d, ratio %.12f" % (name, AA.str(14), TABLE[name], float(AA.mid()) / TABLE[name] if TABLE[name] else 0))

    for c in comps:
        name = c["name"]
        if c["kind"] == "L":
            if c["cG"] is None:
                finish(name, arb(0), arb(1), dict(note="empty eligible set"))
                continue
            lo_index = max(R0, floor(c["cG"] / hF) - KD + 1)
            Lb, Hb, Kb = floor(c["l0"] / hF), ceil(c["u0"] / hF), zK
            theta = c["theta"]
            assert 2 <= Lb < Hb <= Kb <= NG
            branch = "renewal"
            first_bad = None
            if Lb >= 64:
                lo_d, up_d = dick(Lb, NG)
                okd, first_bad = accept(lo_d, up_d, NG)
                if okd:
                    branch = "delay"
            if branch == "delay":
                dup = up_d[:nn]
                floored = None
            else:
                dup, floored = renewal(Lb, nn)
            eth = (-Aq(theta * hF)).exp()
            Dt, cur = [], arb(1)
            for j in range(nn):
                Dt.append(dup[j] * cur); cur *= eth
            Dt = arb_poly(Dt)
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
            log_("%s: L=%d H=%d K=%d theta=%d J=%d rmax=%d branch=%s (first failed test index %s) lower index %d" % (
                name, Lb, Hb, Kb, theta, J, rmax, branch, first_bad, lo_index))
            top = moments_top(arrays, lambda mm: mm[0] <= 1, (1,))
            expo0 = Aq(theta * (-UG + (m - 1) * Hb * hF + KD * hF))
            Wr = [(expo0 + Aq(theta * r * hF)).exp() for r in range(R0, R1 + 1)]
            s = pair(top, Wr, lo_index)
            finish(name, s, arb(1), dict(L=Lb, H=Hb, K=Kb, theta=theta, J=J, branch=branch, delay_first_failed=first_bad,
                                         renewal_floored_at=floored, lower_index=lo_index, clip=c["clip"]))
        elif c["kind"] == "P":
            a, b = c["a"], c["b"]
            rm, rp = (UG - b) / m, (UG - a) / m
            bP, rpP, rmM = ceil(b / hF), ceil(rp / hF), floor(rm / hF)
            cb, fa = ceil(b / hF), floor(a / hF)
            _, Lb_up = dick(bP, nn + 2)
            _, Lp_up = dick(rpP, nn + 2)
            Lm_lo, _ = dick(rmM, nn + 2)
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
            log_("%s: a/h=%.3f b/h=%.3f r_-^-/h=%d r_+^+/h=%d Lambda=%s" % (name, float(a / hF), float(b / hF), rmM, rpP, Lam.str(10)))
            top = moments_top(arrays, lambda mm: mm[0] <= 1 and mm[1] <= 1, (1, 1))
            s = pair(top, [arb(1)] * NR, R0)
            finish(name, s, Lam, dict(a_over_h=float(a / hF), b_over_h=float(b / hF), rminus_over_h=rmM, rplus_over_h=rpP))
        else:
            Lb, Kb = pK, zK
            _, dup = dick(Lb, nn + 1)
            D0 = arb_poly(dup[:nn])
            Q = arb_poly([arb(0)] * Lb + [arb(1) / a for a in range(Lb, Kb)])
            qs = [arb_poly([1])]
            for r in range(1, 8):
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
            log_("H: L=%d K=%d bmax(0)=%d" % (Lb, Kb, (NG - 1) // Lb))
            top = moments_top(arrays, lambda mm: mm[0] <= 3, (3,))
            s = pair(top, [arb(1)] * NR, R0)
            finish("H", s, arb(1), dict(L=Lb, K=Kb))
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
