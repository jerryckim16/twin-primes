#!/usr/bin/env python3
"""Rung 182: SECOND, independent program for the cap numerators J_0 and J_+ of the 182 trial (GPT-6 Astra / R. Sharifi,
bundle [M] (6.7), (7.4); data code/data182/TrialData182_part*.lean). Compared with program 1 (code/sharifi182_J.py,
results code/data182/J_cap_<b>.json) and with the published lower bounds trialJ0Lower, trialJPlusLower.

Definitions (notes/sources-182.md Sec. 4-5, notes/sources-186-forms.md Sec. 1-2): every form is divided by (hZ)^39,
      J_0 = sum_i int 1_{H_0}(Y) |E_i F(Y)|^2 dnu^38(Y),   J_+ = sum_i int 1_{H_1}(Y)(1 - 1_{H_0}(Y)) |E_i F(Y)|^2 dnu^38(Y),
      E_i F(Y) = int F(Y (+)_i X) dnu(X),
F as in [M] (7.3): F(X) = 1_{H_O}(X) prod_i g(t_i) sum_c 1_{M0(X) <= c} sum_{sigma,d} coeff[c][sigma][d] B_d(s) P_sigma(t),
evaluated on cells (t_j = (j+1/2)h, s = (r + 39/2)h, r = sum of the 39 cell indices).
OWN DERIVATION of the finite form (written down here before reading program 1's arithmetic):
  * A configuration is in a cell vector and has a largest fragment M0; for one coordinate,
    nu{cell j, max fragment <= x} = h d_x(j), d_x(j) = (1/h) int_{C_j} rho_D(t/x) dt (nu restricted to max <= x is nu_x).
    For Y (38 coordinates) the measure of {cells, M0(Y) <= x} is prod_k h d_x(j_k).
  * M0(Y (+) X) = max(M0(Y), M0(X)). The outer shell s of the full row r = r' + a' (r' = index sum of Y, a' = cell of
    the erased X) requires M0 <= C_s, the component c requires M0 <= c. So the summand (c, s) of F(Y (+) X) needs
    M0(Y) <= min(c, C_s) and M0(X) <= min(c, C_s); integrating X over its cell gives h g_{a'} d_{min(c,C_s)}(a').
  * Every indicator on M0(Y) is a step at one of the cap values (components, outer shells, base and enlarged faces);
    on the layer M0(Y) in (b_{a-1}, b_a] each is 1 iff its cap >= b_a. The Y-measure of a layer is
    prod h d_{b_a} - prod h d_{b_{a-1}} (b_0: measure 0).
  * P_e(Y (+) X) = P_e(Y) + t_{a'}^e, so P_sigma(Y (+) X) = sum_{A labelled subset} t_{a'}^{e(A)} P_{sigma \\ A}(Y).
  * Hence, with K_j(b) = g_j^2 d_b(j)/Z and M^b_{38,eta}(r') = sum over 38-cells of index sum r' of prod K P_eta,
      v^a_tau(r') = sum_{a'} sum_{s: C_s >= b_a} sum_{c >= b_a} chi_s(r'+a') g_{a'} d_{min(c,C_s)}(a')
                    sum_{(sigma, A): sigma\\A = tau} t_{a'}^{e(A)} p_{c,sigma}(r'+a'),
      J_F = (39 h / Z) sum_a sum_{r'} chi_{F,a}(r') sum_{tau,ups} v^a_tau v^a_ups (M^{b_a} - M^{b_{a-1}})_{38,tau+ups}(r'),
    chi_{0,a}(r') = [base-face cap of row r' >= b_a], chi_{+,a} = [enlarged cap >= b_a] (1 - chi_{0,a}).
    (39 = sum over i; the factor h/Z: h^38 h^2 from the cells, divided by h^39 Z^39, Z^38 absorbed in K.)
  * By linearity in M each cap b = b_a is a separate job: + S(v^a, M^b; chi_a) - S(v^{a+1}, M^b; chi_{a+1}).
  This reading agrees with program 1's docstring (same 9 cap values, same masks, same marginal); see the report.
SHARED with program 1: the reading above, the Lean data files, the Dickman cell-mass convention.
SHARED with code/sharifi182_check2.py (imported): Lean parser, Dickman closed form (arb log + acb polylog), Cox-de Boor
in fmpq, symbolic exponential y-series for the 38-fold moments.
INDEPENDENT of program 1: arb ball arithmetic throughout (program 1: fixed point, floored integers, not rigorous);
outer AND face row ranges derived from the Lean shells (lower <= (r+d)h < upper, asserted equal to the paper's table;
program 1 hard-codes both tables); moments by the y-series (program 1: set partitions); erased marginals by arb_poly
products of per-cap-group arrays truncated to their support (program 1: GMP correlation); B-spline values pointwise
(program 1: span polynomials); J_+ mask computed literally as chi_1 (1 - chi_0) and nesting H_0 c H_1 asserted.
--selftest: k = 3, a 48-cell grid, 9 distinct artificial caps; the same pipeline against a brute-force sum over all
cells of Y and X with mpmath, direct power sums, recursive Cox-de Boor in Fractions and literal h/Z factors.
usage: sharifi182_check2_J.py --caps b1,b2,..  (in increasing order; consecutive caps share a layer marginal)
       sharifi182_check2_J.py --combine        (writes code/data182/check2_J_result.json)
       sharifi182_check2_J.py --selftest [--k 3 --Ntest 48] [--prec 128]"""
import sys, os, re, json, time, resource, importlib.util
from fractions import Fraction
from flint import arb, arb_poly, fmpq, ctx

spec = importlib.util.spec_from_file_location("c2", "code/sharifi182_check2.py")
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)     # sets ctx.prec from --prec

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default
PREC = int(arg("--prec", "128"))
ctx.prec = PREC
DATADIR = "code/data182"
T0 = time.time()
def log_(s):
    print("[%6.0f s, maxrss %.2f GB] %s" % (time.time() - T0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, s), flush=True)

def parse_extra():
    p1 = open(DATADIR + "/TrialData182_part1.lean").read()
    sh = c2.section(p1, "trialShells", "def ")
    groups = re.findall(r"\[\{(.*?)\}\]", sh, re.S)
    assert len(groups) == 5
    shells = []
    for g in groups:
        shells.append([tuple(c2.rats(re.search(r"lower := (.*?), upper := (.*?), cap := (.*?) ?$", blk.strip()).group(i))[0]
                             for i in (1, 2, 3)) for blk in g.split("},")])
    E = dict(shells=shells)
    E["J0lo"] = c2.rats(c2.section(p1, "trialJ0Lower", "\n"))[0]
    E["Jplo"] = c2.rats(c2.section(p1, "trialJPlusLower", "\n"))[0]
    return E

def ceilq(x):
    return int(-((-x.p) // x.q))

def rows_of(shl, d, h, n, capmap):
    """shell list -> [((r0, r1), cap in cells)], rule lower <= (r+d)h < upper; asserts no boundary hits a cell total."""
    out = []
    for lo, up, cap in shl:
        a = lo / h - d
        b = up / h - d
        # a boundary hitting a cell total exactly inside [0, n-1] would make "<" vs "<=" matter
        assert (lo == 0 or a.q != 1 or not 0 <= a < n) and (b.q != 1 or not 0 <= b < n), "shell boundary hits (r+d)h"
        r0 = max(0, ceilq(a))
        r1 = min(ceilq(b) - 1, n - 1)
        out.append(((r0, r1), capmap(cap)))
    return out

class Setup:
    def __init__(self, KD, NG, testcaps=None):
        D = c2.parse(); X = parse_extra()
        self.D, self.X = D, X
        self.KD, self.KR, self.NG = KD, KD - 1, NG
        self.n = n = NG - D["dim"] if testcaps is None else NG - KD
        S_ = D["S"]
        self.h = h = S_ / NG
        h0 = S_ / D["N"]
        def full(c):
            x = c / h0
            assert x.q == 1
            return int(x.p)
        capmap = (lambda c: full(c)) if testcaps is None else (lambda c: testcaps[full(c)])
        self.COMP = [capmap(c) for c in D["ccaps"]]
        self.OUTER = rows_of(X["shells"][0], KD, h, n, capmap)
        self.FACE0 = rows_of(X["shells"][1], self.KR, h, n, capmap)
        self.FACE1 = rows_of(X["shells"][2], self.KR, h, n, capmap)
        if testcaps is None:
            assert KD == 39 and n == 393177
            assert self.COMP == [141720, 177528, 246256]
            assert self.OUTER == [((0, 352697), 246256), ((352698, 376449), 196608), ((376450, 393176), 186253)], self.OUTER
            assert self.FACE0 == [((0, 334253), 246256), ((334254, 343163), 177542), ((343164, 355047), 140306)], self.FACE0
            assert self.FACE1 == [((0, 336274), 246256), ((336275, 343169), 179967), ((343170, 359896), 141724)], self.FACE1
        self.BV = sorted(set(self.COMP) | {c for _, c in self.OUTER + self.FACE0 + self.FACE1})
        self.SIGS = D["sigs"]
        # face cap per row (0 = not in the face)
        def capof(rows):
            arr = [0] * n
            for (r0, r1), c in rows:
                for r in range(r0, r1 + 1): arr[r] = c
            return arr
        self.f0, self.f1 = capof(self.FACE0), capof(self.FACE1)
        self.nested = all(self.f1[r] >= self.f0[r] for r in range(n))   # chi_0 <= chi_1 on every layer
        if testcaps is None: assert self.nested
        # coordinate data
        tq = [(j + fmpq(1, 2)) * h for j in range(n)]
        self.g = [arb(c2.gq(t)) for t in tq]
        self.g2 = [x * x for x in self.g]
        self.Z = sum(self.g2, arb(0))
        self.tj = [arb(t) for t in tq]
        # B-spline values at s_r = (r + KD/2)h, and p_{c,sigma} as arb_poly in r
        U = D["knots"]; p = 3; nb = len(U) - p - 1
        Bv = {}
        for r in range(n):
            x = (r + fmpq(KD, 2)) * h
            i = c2.find_span(U, x, p, nb)
            if i is None: continue
            Nf = c2.basis_funs(i, x, p, U)
            assert sum(Nf, fmpq(0)) == 1 and all(v >= 0 for v in Nf)
            Bv[r] = (i - p, [arb(v) for v in Nf])
        self.rfirst = min(Bv)
        self.P = {}
        for ci in range(3):
            for si in range(11):
                row = [arb(x) for x in D["coeff"][ci][si]]
                lst = [arb(0)] * n
                for r, (d0, nf) in Bv.items():
                    lst[r] = row[d0] * nf[0] + row[d0 + 1] * nf[1] + row[d0 + 2] * nf[2] + row[d0 + 3] * nf[3]
                self.P[(ci, si)] = arb_poly(lst)
        del Bv
        # (tau, e) -> {sigma index: multiplicity}
        self.rowspec = {}
        for si, sg in enumerate(self.SIGS):
            L = len(sg)
            for mask in range(1 << L):
                tau = tuple(sorted(sg[i] for i in range(L) if not mask >> i & 1))
                e = sum(sg[i] for i in range(L) if mask >> i & 1)
                dd = self.rowspec.setdefault((tau, e), {})
                dd[si] = dd.get(si, 0) + 1
        self.taus = sorted({t for (t, _) in self.rowspec})
        assert set(self.taus) == set(tuple(sorted(s)) for s in self.SIGS)
        self.dcache = {}

    def dmass(self, m):
        if m not in self.dcache:
            self.dcache[m] = c2.cellmass(m, self.n)
        return self.dcache[m]

    def marginal(self, la):
        """v^a_tau as arb_poly in the reversed index n-1-r'."""
        n, bl = self.n, self.BV[la]
        groups = {}
        for (r0, r1), Cs in self.OUTER:
            if Cs < bl or r1 < r0: continue
            for ci, c in enumerate(self.COMP):
                if c >= bl:
                    groups.setdefault(min(c, Cs), []).append((ci, max(r0, self.rfirst), r1))
        V = {tau: arb_poly([]) for tau in self.taus}
        nprod = 0
        for m, segs in sorted(groups.items()):
            segs = [s for s in segs if s[1] <= s[2]]
            if not segs: continue
            lo = min(s[1] for s in segs); hi = max(s[2] for s in segs)
            L = hi - lo + 1
            # reversed arrays R_sigma[k] = q_{m,sigma}(hi - k)
            Rq = []
            for si in range(11):
                lst = [arb(0)] * L
                for ci, r0, r1 in segs:
                    cf = self.P[(ci, si)].coeffs()
                    cf += [arb(0)] * (n - len(cf))
                    for r in range(r0, r1 + 1):
                        lst[hi - r] += cf[r]
                Rq.append(arb_poly(lst))
            dm = self.dmass(m)
            base = [self.g[a] * dm[a] for a in range(hi + 1)]
            Wc = {}
            for (tau, e), sm in sorted(self.rowspec.items()):
                if e not in Wc:
                    w = base
                    if e:
                        w = [base[a] * self.tj[a] ** e for a in range(hi + 1)]
                    Wc[e] = arb_poly(w)
                R = arb_poly([])
                for si, mult in sm.items():
                    R += Rq[si] * mult
                prod = (R * Wc[e]).truncate(hi + 1)          # coefficient hi - r' = v contribution at r'
                V[tau] += prod.left_shift(n - 1 - hi)
                nprod += 1
            del Rq, Wc, base
        log_("layer %d (b = %d): marginal, %d groups, %d products" % (la, bl, len(groups), nprod))
        return V

    def moments(self, b):
        """M^b_{KR, eta}(r') for all eta = tau + ups, as arb_poly truncated to n (y-series of check2, power KR)."""
        n, KR = self.n, self.KR
        pairs = {}
        for t1 in self.taus:
            for t2 in self.taus:
                pairs.setdefault(tuple(sorted(t1 + t2)), []).append((t1, t2))
        self.pairs = pairs
        etas = sorted(pairs)
        meta = {eta: c2.mvec(eta) for eta in etas}
        Sset = c2.downclose(meta.values())
        Aser = {(0,) * 5: {(1, ()): fmpq(1)}}
        for m in Sset:
            if any(m): Aser[m] = {(0, (c2.wt(m),)): fmpq(1, c2.mfact(m))}
        Pser = c2.spow(Aser, KR, Sset)
        form = {}
        for eta in etas:
            f = {}
            for (a, E), c in Pser[meta[eta]].items():
                c = c * c2.mfact(meta[eta])
                assert c.q == 1 and c > 0 and a + len(E) == KR
                f[E] = int(c.p)
            form[eta] = f
        allE = sorted({E for f in form.values() for E in f})
        weights = sorted({w for E in allE for w in E})
        d = self.dmass(b)
        K = [self.g2[j] * d[j] / self.Z for j in range(n)]
        Pw = {0: arb_poly(K)}
        cur = K
        for w in range(1, max(weights) + 1):
            cur = [cur[j] * self.tj[j] for j in range(n)]
            if w in weights: Pw[w] = arb_poly(cur)
        del cur, K
        lens = sorted({len(E) for E in allE})
        kmin = KR - max(lens)
        res, base, e = arb_poly([1]), Pw[0], kmin
        while e:
            if e & 1: res = (res * base).truncate(n)
            e >>= 1
            if e: base = (base * base).truncate(n)
        del base
        A0pow = {kmin: res}
        for k in range(kmin + 1, KR + 1):
            A0pow[k] = (A0pow[k - 1] * Pw[0]).truncate(n)
        for k in list(A0pow):
            if KR - k not in lens: del A0pow[k]
        bylen = {}
        for E in allE: bylen.setdefault(len(E), []).append(E)
        users = {E: [(eta, form[eta][E]) for eta in etas if E in form[eta]] for E in allE}
        Mp, nprod = {}, 0
        for L in sorted(bylen):
            stack = [((), A0pow[KR - L])]
            for E in sorted(bylen[L], key=lambda E: tuple(sorted(E, reverse=True))):
                Ed = tuple(sorted(E, reverse=True))
                while not (len(stack[-1][0]) <= len(Ed) and Ed[:len(stack[-1][0])] == stack[-1][0]):
                    stack.pop()
                while len(stack[-1][0]) < len(Ed):
                    pre, poly = stack[-1]
                    stack.append((pre + (Ed[len(pre)],), (poly * Pw[Ed[len(pre)]]).truncate(n)))
                    nprod += 1
                mono = stack[-1][1]
                for eta, c in users[E]:
                    Mp[eta] = mono * c if eta not in Mp else Mp[eta] + mono * c
            del stack
            A0pow.pop(KR - L, None)
            log_("cap %d: moments, monomials of length %d done (%d products)" % (b, L, nprod))
        return Mp

    def contract(self, V, Mp, bl):
        """S(v, M; chi_0) and S(v, M; chi_+) for layer cap bl."""
        n = self.n
        rows0 = [r for r in range(n) if self.f0[r] >= bl]
        rowsp = [r for r in range(n) if self.f1[r] >= bl and not self.f0[r] >= bl]
        vl = {}
        for tau, poly in V.items():
            cf = poly.coeffs(); cf += [arb(0)] * (n - len(cf))
            vl[tau] = cf[::-1]                                   # vl[tau][r'] = v_tau(r')
        tot = {"0": arb(0), "+": arb(0)}
        for eta, pl in self.pairs.items():
            ml = Mp[eta].coeffs(); ml += [arb(0)] * (n - len(ml))
            pr = [(vl[a], vl[c]) for (a, c) in pl]
            for F_, rows in (("0", rows0), ("+", rowsp)):
                part = arb(0)
                for r in rows:
                    q = arb(0)
                    for (x, y) in pr:
                        q += x[r] * y[r]
                    part += q * ml[r]
                tot[F_] += part
        return tot

    def run_cap(self, b, Vcache):
        ai = self.BV.index(b)
        layers = [ai] + ([ai + 1] if ai + 1 < len(self.BV) else [])
        for la in layers:
            if la not in Vcache: Vcache[la] = self.marginal(la)
        for la in list(Vcache):
            if la not in layers: del Vcache[la]
        Mp = self.moments(b)
        fac = self.KD * arb(self.h) / self.Z
        res = {"0": arb(0), "+": arb(0)}
        for k, la in enumerate(layers):
            t = self.contract(Vcache[la], Mp, self.BV[la])
            for F_ in res:
                res[F_] = res[F_] + t[F_] if k == 0 else res[F_] - t[F_]
            log_("cap %d: term %+d (layer %d): J0 %s, J+ %s" % (b, 1 if k == 0 else -1, la,
                 (t["0"] * fac).str(20, radius=True), (t["+"] * fac).str(20, radius=True)))
        del Mp
        return {F_: res[F_] * fac for F_ in res}

def ball_rec(x):
    return dict(mid_man_exp=[str(v) for v in x.mid().man_exp()], rad_man_exp=[str(v) for v in x.rad().man_exp()],
                ball=x.str(25, radius=True), value_float=float(x.mid()), rad=float(x.rad()))
def ball_from(rec):
    m, e = (int(x) for x in rec["mid_man_exp"])
    rm, re_ = (int(x) for x in rec["rad_man_exp"])
    mid = Fraction(m) * Fraction(2) ** e
    rad = Fraction(rm) * Fraction(2) ** re_
    return mid, rad

capfile = lambda b: "%s/check2_J_cap_%d.json" % (DATADIR, b)

def main_caps():
    st = Setup(39, 393216)
    log_("setup: N = %d, n = %d, caps %s, outer %s, face0 %s, face1 %s, rfirst %d, Z = %s, prec %d"
         % (st.NG, st.n, st.BV, st.OUTER, st.FACE0, st.FACE1, st.rfirst, st.Z.str(25, radius=True), PREC))
    todo = [int(x) for x in arg("--caps", ",".join(map(str, st.BV))).split(",")]
    Vc = {}
    for b in todo:
        tc = time.time()
        r = st.run_cap(b, Vc)
        out = dict(cap=b, N=st.NG, prec=PREC, J0=ball_rec(r["0"]), Jplus=ball_rec(r["+"]), seconds=round(time.time() - tc),
                   maxrss_GB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, 3))
        json.dump(out, open(capfile(b), "w"), indent=1)
        log_("cap %d: J0 part %s, J+ part %s" % (b, out["J0"]["ball"], out["Jplus"]["ball"]))

def main_combine():
    BV = [140306, 141720, 141724, 177528, 177542, 179967, 186253, 196608, 246256]
    missing = [b for b in BV if not os.path.exists(capfile(b))]
    if missing:
        print("missing caps:", missing); return
    X = parse_extra()
    out = dict(N=393216, per_cap={})
    tot = {"J0": [Fraction(0), Fraction(0)], "Jplus": [Fraction(0), Fraction(0)]}
    p1tot = {"J0": Fraction(0), "Jplus": Fraction(0)}
    for b in BV:
        rec = json.load(open(capfile(b)))
        p1 = json.load(open("%s/J_cap_%d.json" % (DATADIR, b)))
        pc = {}
        for F_, k1 in (("J0", "0"), ("Jplus", "+")):
            m, r = ball_from(rec[F_])
            tot[F_][0] += m; tot[F_][1] += r
            v1 = Fraction(p1[k1]); p1tot[F_] += v1
            pc[F_] = dict(check2=rec[F_]["ball"], program1=float(v1), diff=float(m - v1),
                          rel=(float((m - v1) / v1) if v1 else None), program1_in_ball=bool(abs(m - v1) <= r))
        pc["seconds"], pc["maxrss_GB"] = rec["seconds"], rec["maxrss_GB"]
        out["per_cap"][str(b)] = pc
    for F_, lo in (("J0", X["J0lo"]), ("Jplus", X["Jplo"])):
        m, r = tot[F_]
        lo = Fraction(int(lo.p), int(lo.q))
        v1 = p1tot[F_]
        out[F_] = dict(ball="[%s +/- %.3e]" % (arb(fmpq(m.numerator, m.denominator)).str(30, radius=False), float(r)),
                       mid=float(m), rad=float(r), lower_exact=str(m - r), upper_exact=str(m + r),
                       program1=float(v1), program1_exact=str(v1), diff_vs_program1=float(m - v1),
                       reldiff_vs_program1=float((m - v1) / v1), program1_in_ball=bool(abs(m - v1) <= r),
                       published_lower=float(lo), ball_ge_published_lower=bool(m - r >= lo),
                       rel_excess_over_published_lower=float((m - lo) / lo))
    log_(json.dumps(out, indent=1))
    json.dump(out, open(DATADIR + "/check2_J_result.json", "w"), indent=1)

# ---------------- self-test ----------------
def bspline_rec(U, i, p, x):
    """textbook recursive Cox-de Boor, right-continuous, 0/0 = 0 (Fractions)."""
    if p == 0:
        return Fraction(1) if U[i] <= x < U[i + 1] else Fraction(0)
    out = Fraction(0)
    if U[i + p] != U[i]:
        out += (x - U[i]) / (U[i + p] - U[i]) * bspline_rec(U, i, p - 1, x)
    if U[i + p + 1] != U[i + 1]:
        out += (U[i + p + 1] - x) / (U[i + p + 1] - U[i + 1]) * bspline_rec(U, i + 1, p - 1, x)
    return out

def selftest():
    from mpmath import mp, mpf
    mp.dps = 45
    KD, NG = int(arg("--k", "3")), int(arg("--Ntest", "48"))
    order = [140306, 141720, 141724, 177528, 177542, 179967, 186253, 196608, 246256]
    tcaps = dict(zip(order, [15, 16, 17, 19, 20, 21, 23, 25, 30]))
    st = Setup(KD, NG, tcaps)
    n, h, KR = st.n, st.h, st.KR
    log_("selftest: k = %d, N = %d, n = %d, caps %s, outer %s, face0 %s, face1 %s, nested %s"
         % (KD, NG, n, st.BV, st.OUTER, st.FACE0, st.FACE1, st.nested))
    Vc, got = {}, {"0": arb(0), "+": arb(0)}
    for b in st.BV:
        r = st.run_cap(b, Vc)
        for F_ in got: got[F_] += r[F_]
    # brute force
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
        Bs = [bspline_rec(U, d, 3, x) for d in range(22)]
        for ci in range(3):
            for si in range(11):
                v = sum((coeff[ci][si][d] * Bs[d] for d in range(22)), Fr(0))
                pc[(ci, si, r)] = mpf(v.numerator) / v.denominator
    dm = {m: [mpf(x.mid().str(60, radius=False)) for x in st.dmass(m)] for m in st.BV}
    shell = {}
    for (r0, r1), Cs in st.OUTER:
        for r in range(r0, r1 + 1): shell[r] = Cs
    def Psig(ts, sg):
        out = mpf(1)
        for e in sg: out *= mp.fsum(t ** e for t in ts)
        return out
    BV = st.BV
    J = {"0": mpf(0), "+": mpf(0)}
    import itertools
    for Y in itertools.product(range(n), repeat=KR):
        rp = sum(Y)
        if rp > n - 1: continue
        tY = [tm[j] for j in Y]
        # per erased cell a' and component: sum_sigma p P
        Sc = {}
        for a in range(n - rp):
            r = rp + a
            if r not in shell: continue
            ts = tY + [tm[a]]
            Ps = [Psig(ts, sg) for sg in st.SIGS]
            for ci in range(3):
                Sc[(a, ci)] = mp.fsum(pc[(ci, si, r)] * Ps[si] for si in range(11))
        for la, bl in enumerate(BV):
            # layer measure of Y (literal h factors), retained coordinates carry g^2
            mu = mpf(1); mu0 = mpf(1)
            for j in Y:
                mu *= gm[j] ** 2 * hm * dm[bl][j]
                mu0 *= (gm[j] ** 2 * hm * dm[BV[la - 1]][j]) if la > 0 else 0
            meas = mu - mu0
            in0 = st.f0[rp] >= bl
            in1 = st.f1[rp] >= bl
            if not (in0 or in1): continue
            Vv = mpf(0)
            for (a, ci), s in Sc.items():
                c, Cs = st.COMP[ci], shell[rp + a]
                if c >= bl and Cs >= bl:
                    Vv += gm[a] * hm * dm[min(c, Cs)][a] * s
            # sum over the KD erased positions: identical by symmetry of the power sums
            contrib = KD * meas * Vv ** 2 / (hm * Zm) ** KD
            if in0: J["0"] += contrib
            if in1 and not in0: J["+"] += contrib
    ok = True
    for F_ in J:
        a_ = mpf(got[F_].mid().str(40, radius=False))
        rel = abs(a_ - J[F_]) / abs(J[F_])
        log_("selftest %s: pipeline %s, brute force %s, rel diff %s" % (F_, got[F_].str(25, radius=True), mp.nstr(J[F_], 25), mp.nstr(rel, 5)))
        ok = ok and rel < mpf(10) ** -20
    log_("SELFTEST %s" % ("PASSED" if ok else "FAILED"))
    return ok

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    elif "--combine" in sys.argv:
        main_combine()
    else:
        main_caps()
