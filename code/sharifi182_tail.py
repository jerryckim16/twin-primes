#!/usr/bin/env python3
"""Rung 182: the cap tail term E_{H_C^c} of the 182 trial ([M] (6.5), (6.7), (7.4); kernel K from (5.2), (5.5)-(5.7)),
as rigorous-in-spirit arb balls, compared with the Lean premise trialTailUpper (code/data182/TrialData182_part1.lean)
and propagated into q_H - 1 together with I (code/data182/check2_I_result.json) and J0, J+
(code/data182/check2_J_result.json). ONE program for the tail (no second implementation).

Definition (normalised by (hZ)^39 like I, J0, J+):
      T = sum_i int 1_{H_C^c}(Y) K(q(Y)) |E_i F(Y)|^2 dnu^38(Y),
with K replaced by its block-step majorant (5.6): constant on blocks of 768 consecutive retained index sums r'
(blocks [768 b, 768 b + 767], r_max = min(768 b + 767, n0 - 1)), value K_b = sum_{j=1}^{1024} W_j^+ / z_j(q+_b),
q+_b = rho* (r_max + 38) h, W_j^+ = ceil(10^25 (s_j - s_{j-1}) w_t(s_j)/s_j L21(v_j)) / 10^25, all exact in fmpq.
Layers as in code/sharifi182_check2_J.py (imported: same marginal, moments, prefactor 39h/Z), but the layer cap set is
the components, the outer shells and the H_C caps: {141720, 177528, 186253, 186491, 196608, 246256}. On layer a the
mask is chi_{T,a}(r') = 1 - [capC(r') >= b_a] (capC = 0 outside the H_C rows), row ranges of H_C derived from the Lean
shells (trialShells[3], lower <= (r'+38)h < upper) and asserted equal to the [M] Sec. 7.2 table.
usage: sharifi182_tail.py --caps b1,b2,..  (increasing; writes code/data182/tail_cap_<b>.json)
       sharifi182_tail.py --combine         (writes code/data182/tail_result.json)
       sharifi182_tail.py --kernel          (kernel table only, with the (5.7) check)
       sharifi182_tail.py --selftest [--k 3 --Ntest 48]"""
import sys, os, json, time, resource, importlib.util, itertools
from fractions import Fraction
from flint import arb, arb_poly, fmpq

spec = importlib.util.spec_from_file_location("cj", "code/sharifi182_check2_J.py")
cj = importlib.util.module_from_spec(spec); spec.loader.exec_module(cj)
c2 = cj.c2
arg, log_, DATADIR = cj.arg, cj.log_, cj.DATADIR
PREC = cj.PREC

# ---------------- kernel (exact) ----------------
LAM = fmpq(8639, 50000)          # paper's lambda = 1 - 2a (Lean trialRoughness); NOT Lean trialLambda (= ell)
A_ = fmpq(41361, 100000)         # a (Lean trialMinorantA)
TH = fmpq(19, 50)                # hinge threshold t = .38 (Lean trialHingeThreshold)
EPS0 = fmpq(1, 10000)            # auxiliary retreat (Lean trialAuxiliaryRetreat)
RHOS = fmpq(2624989, 10000000)
NBIN, BLK = 1024, 768

def kernel_W():
    W, s_prev = [], 2 * LAM
    for j in range(1, NBIN + 1):
        s = 2 * LAM + j * (A_ - 2 * LAM) / NBIN
        v = (s - 2 * LAM) / LAM
        assert 0 <= v < 1
        L21 = sum((fmpq((-1) ** (m + 1), m) * v ** m for m in range(1, 22)), fmpq(0))
        w = fmpq(12, 5) * max(s - TH, fmpq(0)) / (fmpq(2, 5) - TH)
        x = (s - s_prev) * w / s * L21
        assert x >= 0
        q = x * 10 ** 25
        Wp = fmpq(-((-q.p) // q.q), 10 ** 25)          # round upward to a multiple of 1e-25
        W.append((s, Wp))
        s_prev = s
    return W

def K_of(W, qplus):
    tot = fmpq(0)
    for s, Wp in W:
        if Wp == 0: continue
        z = min(LAM - EPS0, (1 - s) / 2 - qplus - EPS0)
        assert z > 0
        tot += Wp / z
    return tot

def kernel_table(n, h, KR, blocks=None):
    W = kernel_W()
    nb = -(-n // BLK)
    out = {}
    for b in (range(nb) if blocks is None else blocks):
        rmax = min(BLK * b + BLK - 1, n - 1)
        out[b] = K_of(W, RHOS * (rmax + KR) * h)
    return W, out

# ---------------- setup ----------------
class TailSetup(cj.Setup):
    def __init__(self, KD, NG, testcaps=None, Krow=None):
        super().__init__(KD, NG, testcaps)
        h, n = self.h, self.n
        h0 = self.D["S"] / self.D["N"]
        def full(c):
            x = c / h0; assert x.q == 1; return int(x.p)
        capmap = (lambda c: full(c)) if testcaps is None else (lambda c: testcaps[full(c)])
        self.FACEC = cj.rows_of(self.X["shells"][3], self.KR, h, n, capmap)
        if testcaps is None:
            assert self.FACEC == [((0, 352698), 246256), ((352699, 371671), 186491)], self.FACEC
        self.fC = [0] * n
        for (r0, r1), c in self.FACEC:
            for r in range(r0, r1 + 1): self.fC[r] = c
        assert all(self.f1[r] <= self.fC[r] for r in range(n)) or testcaps is not None    # H_1 c H_C
        self.BV = sorted(set(self.COMP) | {c for _, c in self.OUTER + self.FACEC})
        if Krow is None:
            W, Kb = kernel_table(n, h, self.KR)
            self.Kb = Kb
            Krow = lambda r: Kb[r // BLK]
        self.Krow = Krow

    def contract_tail(self, V, Mp, bl):
        n = self.n
        rows = [r for r in range(n) if not self.fC[r] >= bl]
        vl = {}
        for tau, poly in V.items():
            cf = poly.coeffs(); cf += [arb(0)] * (n - len(cf))
            vl[tau] = cf[::-1]
        Kr = {}
        for r in rows:
            Kr[r] = arb(self.Krow(r))
        tot = {"T": arb(0), "M": arb(0)}
        for eta, pl in self.pairs.items():
            ml = Mp[eta].coeffs(); ml += [arb(0)] * (n - len(ml))
            pr = [(vl[a], vl[c]) for (a, c) in pl]
            pT, pM = arb(0), arb(0)
            for r in rows:
                q = arb(0)
                for (x, y) in pr:
                    q += x[r] * y[r]
                q *= ml[r]
                pM += q
                pT += q * Kr[r]
            tot["T"] += pT; tot["M"] += pM
        return tot

    def run_cap_tail(self, b, Vcache):
        ai = self.BV.index(b)
        layers = [ai] + ([ai + 1] if ai + 1 < len(self.BV) else [])
        for la in layers:
            if la not in Vcache: Vcache[la] = self.marginal(la)
        for la in list(Vcache):
            if la not in layers: del Vcache[la]
        Mp = self.moments(b)
        fac = self.KD * arb(self.h) / self.Z
        res = {"T": arb(0), "M": arb(0)}
        for k, la in enumerate(layers):
            t = self.contract_tail(Vcache[la], Mp, self.BV[la])
            for F_ in res:
                res[F_] = res[F_] + t[F_] if k == 0 else res[F_] - t[F_]
            log_("cap %d: term %+d (layer %d): T %s, M_T %s" % (b, 1 if k == 0 else -1, la,
                 (t["T"] * fac).str(20, radius=True), (t["M"] * fac).str(20, radius=True)))
        del Mp
        return {F_: res[F_] * fac for F_ in res}

capfile = lambda b: "%s/tail_cap_%d.json" % (DATADIR, b)
BT = [141720, 177528, 186253, 186491, 196608, 246256]

def kernel_report():
    D = c2.parse()
    n = D["N"] - D["dim"]; h = D["S"] / D["N"]
    W, Kb = kernel_table(n, h, D["dim"] - 1)
    nz = sum(1 for _, w in W if w)
    Ks = [Kb[b] for b in sorted(Kb)]
    assert all(Ks[i] <= Ks[i + 1] for i in range(len(Ks) - 1))
    Kmax = max(Ks)
    # nominal last block end 768*512 - 1 = 393215 (ambiguity)
    Knom = K_of(W, RHOS * (BLK * 512 - 1 + D["dim"] - 1) * h)
    rep = dict(nonzero_W=nz, sum_W=float(sum((w for _, w in W), fmpq(0))), blocks=len(Ks),
               K_first=float(Ks[0]), K_block459=float(Kb[459]), K_block483=float(Kb[483]), K_last=float(Kmax),
               K_57_holds=bool(0 <= Ks[0] and Kmax <= fmpq(2194, 1000)),
               K_last_if_rmax_393215=float(Knom), K_57_holds_if_rmax_393215=bool(Knom <= fmpq(2194, 1000)))
    return rep, W, Kb

def main_caps():
    st = TailSetup(39, 393216)
    rep, _, _ = kernel_report()
    log_("kernel: %s" % json.dumps(rep))
    assert rep["K_57_holds"]
    log_("setup: caps %s, H_C rows %s, prec %d" % (st.BV, st.FACEC, PREC))
    todo = [int(x) for x in arg("--caps", ",".join(map(str, st.BV))).split(",")]
    Vc = {}
    for b in todo:
        tc = time.time()
        r = st.run_cap_tail(b, Vc)
        out = dict(cap=b, N=st.NG, prec=PREC, T=cj.ball_rec(r["T"]), M_T=cj.ball_rec(r["M"]),
                   seconds=round(time.time() - tc), maxrss_GB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, 3))
        json.dump(out, open(capfile(b), "w"), indent=1)
        log_("cap %d: T part %s, M_T part %s" % (b, out["T"]["ball"], out["M_T"]["ball"]))

def F(x):
    return Fraction(int(x.p), int(x.q))

def main_combine():
    missing = [b for b in BT if not os.path.exists(capfile(b))]
    if missing:
        print("missing caps:", missing); return
    X = cj.parse_extra()
    import re
    p1 = open(DATADIR + "/TrialData182_part1.lean").read()
    Tup = F(c2.rats(c2.section(p1, "trialTailUpper", "\n"))[0])
    ell = F(c2.rats(c2.section(p1, "trialLambda", "\n"))[0])
    kbar = F(c2.rats(c2.section(p1, "trialKappa", "\n"))[0])
    rhos = F(c2.rats(c2.section(p1, "trialRhoStar", "\n"))[0])
    assert ell == Fraction(6308693370963335, 576460752303423488) and kbar == Fraction(46653544162031, 500000000000000000)
    assert rhos == Fraction(2624989, 10 ** 7)
    dh = kbar * (1 / ell - 1)
    rep, _, _ = kernel_report()
    tot = {"T": [Fraction(0), Fraction(0)], "M_T": [Fraction(0), Fraction(0)]}
    per = {}
    for b in BT:
        rec = json.load(open(capfile(b)))
        for k in tot:
            m, r = cj.ball_from(rec[k]); tot[k][0] += m; tot[k][1] += r
        per[str(b)] = dict(T=rec["T"]["ball"], M_T=rec["M_T"]["ball"], seconds=rec["seconds"], maxrss_GB=rec["maxrss_GB"])
    Tm, Tr = tot["T"]; Mm, Mr = tot["M_T"]
    out = dict(kernel=rep, per_cap=per)
    out["T"] = dict(ball="[%s +/- %.3e]" % (arb(fmpq(Tm.numerator, Tm.denominator)).str(30, radius=False), float(Tr)),
                    mid=float(Tm), rad=float(Tr), lower_exact=str(Tm - Tr), upper_exact=str(Tm + Tr),
                    published_upper=float(Tup), ball_le_published_upper=bool(Tm + Tr <= Tup),
                    ratio_to_published=float(Tm / Tup), rel_gap_below_published=float(1 - Tm / Tup))
    out["M_T"] = dict(ball="[%s +/- %.3e]" % (arb(fmpq(Mm.numerator, Mm.denominator)).str(30, radius=False), float(Mr)),
                      T_over_M_T=float(Tm / Mm))
    # q_H - 1 from the balls
    I = json.load(open(DATADIR + "/check2_I_result.json"))
    J = json.load(open(DATADIR + "/check2_J_result.json"))
    Ilo, Iup = Fraction(I["I_lower_exact"]), Fraction(I["I_upper_exact"])
    J0lo, J0up = Fraction(J["J0"]["lower_exact"]), Fraction(J["J0"]["upper_exact"])
    Jplo, Jpup = Fraction(J["Jplus"]["lower_exact"]), Fraction(J["Jplus"]["upper_exact"])
    Tlo, Tup_b = Tm - Tr, Tm + Tr
    mu_lo = rhos * (J0lo + (1 - ell) * Jplo - dh * Tup_b) / Iup - 1
    mu_up = rhos * (J0up + (1 - ell) * Jpup - dh * Tlo) / Ilo - 1
    mu_minus = Fraction(9968877639291, 2 ** 55)
    Ipub = Fraction(9900316889124784142456785, 664613997892457936451903530140172288)
    mu_prem = rhos * (F(X["J0lo"]) + (1 - ell) * F(X["Jplo"]) - dh * Tup) / Ipub - 1
    out["qH"] = dict(d_h=float(dh), mu_lower=float(mu_lo), mu_upper=float(mu_up), mu_lower_exact=str(mu_lo),
                     published_mu_minus=float(mu_minus), mu_lower_ge_mu_minus=bool(mu_lo >= mu_minus),
                     mu_from_published_premises=float(mu_prem),
                     tail_share_of_q=float(rhos * dh * Tm / ((Ilo + Iup) / 2)),
                     final_margin_10_3=float(mu_lo - Fraction(105739089, 500000000000)))
    log_(json.dumps(out, indent=1))
    json.dump(out, open(DATADIR + "/tail_result.json", "w"), indent=1)

# ---------------- self-test ----------------
def selftest():
    from mpmath import mp, mpf
    mp.dps = 45
    KD, NG = int(arg("--k", "3")), int(arg("--Ntest", "48"))
    order = [140306, 141720, 141724, 177528, 177542, 179967, 186253, 186491, 196608, 246256]
    tcaps = dict(zip(order, [15, 16, 17, 19, 20, 21, 23, 24, 25, 30]))
    Ktest = lambda r: fmpq(7 + (r // 4) % 5, 6)                 # artificial block-constant weight, blocks of 4
    st = TailSetup(KD, NG, tcaps, Krow=Ktest)
    n, h, KR = st.n, st.h, st.KR
    log_("selftest tail: k = %d, N = %d, n = %d, caps %s, outer %s, H_C %s" % (KD, NG, n, st.BV, st.OUTER, st.FACEC))
    Vc, got = {}, arb(0)
    for b in st.BV:
        got += st.run_cap_tail(b, Vc)["T"]
    # brute force (literal definitions, mpmath)
    Fr = Fraction
    D = st.D
    U = [Fr(int(x.p), int(x.q)) for x in D["knots"]]
    hF = Fr(int(h.p), int(h.q))
    coeff = [[[Fr(int(x.p), int(x.q)) for x in row] for row in comp] for comp in D["coeff"]]
    def gF(t):
        return Fr(21, 200) / (1 + t / 100) + Fr(179, 200) / (1 + Fr(907, 5) * t)
    tF = [(j + Fr(1, 2)) * hF for j in range(n)]
    gm = [mpf(gF(t).numerator) / gF(t).denominator for t in tF]
    tm = [mpf(t.numerator) / t.denominator for t in tF]
    hm = mpf(hF.numerator) / hF.denominator
    Zm = mp.fsum(x * x for x in gm)
    pc = {}
    for r in range(n):
        x = (r + Fr(KD, 2)) * hF
        Bs = [cj.bspline_rec(U, d, 3, x) for d in range(22)]
        for ci in range(3):
            for si in range(11):
                v = sum((coeff[ci][si][d] * Bs[d] for d in range(22)), Fr(0))
                pc[(ci, si, r)] = mpf(v.numerator) / v.denominator
    # all cap values where any indicator on M0(Y) can step (a finer layer set than st.BV: must give the same)
    allcaps = sorted(set(tcaps.values()))
    dm = {m: [mpf(x.mid().str(60, radius=False)) for x in st.dmass(m)] for m in allcaps}
    shell = {}
    for (r0, r1), Cs in st.OUTER:
        for r in range(r0, r1 + 1): shell[r] = Cs
    def Psig(ts, sg):
        out = mpf(1)
        for e in sg: out *= mp.fsum(t ** e for t in ts)
        return out
    T = mpf(0)
    for Y in itertools.product(range(n), repeat=KR):
        rp = sum(Y)
        if rp > n - 1: continue
        tY = [tm[j] for j in Y]
        Sc = {}
        for a in range(n - rp):
            r = rp + a
            if r not in shell: continue
            ts = tY + [tm[a]]
            Ps = [Psig(ts, sg) for sg in st.SIGS]
            for ci in range(3):
                Sc[(a, ci)] = mp.fsum(pc[(ci, si, r)] * Ps[si] for si in range(11))
        Kw = mpf(int(Ktest(rp).p)) / int(Ktest(rp).q)
        for la, bl in enumerate(allcaps):
            if st.fC[rp] >= bl: continue                      # Y in H_C on this layer
            mu = mpf(1); mu0 = mpf(1)
            for j in Y:
                mu *= gm[j] ** 2 * hm * dm[bl][j]
                mu0 *= (gm[j] ** 2 * hm * dm[allcaps[la - 1]][j]) if la > 0 else 0
            Vv = mpf(0)
            for (a, ci), s in Sc.items():
                c, Cs = st.COMP[ci], shell[rp + a]
                if c >= bl and Cs >= bl:
                    Vv += gm[a] * hm * dm[min(c, Cs)][a] * s
            T += KD * Kw * (mu - mu0) * Vv ** 2 / (hm * Zm) ** KD
    a_ = mpf(got.mid().str(40, radius=False))
    rel = abs(a_ - T) / abs(T)
    log_("selftest tail: pipeline %s, brute force %s, rel diff %s" % (got.str(25, radius=True), mp.nstr(T, 25), mp.nstr(rel, 5)))
    ok = rel < mpf(10) ** -20 and T > 0
    log_("SELFTEST %s" % ("PASSED" if ok else "FAILED"))
    return ok

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    elif "--combine" in sys.argv:
        main_combine()
    elif "--kernel" in sys.argv:
        print(json.dumps(kernel_report()[0], indent=1))
    else:
        main_caps()
