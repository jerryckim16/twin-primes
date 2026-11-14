#!/usr/bin/env python3
"""Rung 182: SECOND, independent program for the denominator I(F) = ||F||^2 of the 182 trial (GPT-6 Astra / R. Sharifi,
[M] Sec. 7.3-7.5, data code/data182/TrialData182_part*.lean), to be compared with code/sharifi182_I.py (program 1,
result code/data182/I_result.json) and with the published enclosure (7.5).

SHARED with program 1 (so this program does NOT check these):
  * the reading of F and of the normalisation (notes/sources-182.md Sec. 3-4): k = 39, N = 393216, n0 = N - 39 cells,
    t_j = (j + 1/2)h, s = (r + 39/2)h, coordinate weight K_j(b) = g_j^2 d_b(j) / Z, d_b(j) = (1/h) int_{C_j} rho_D(t/b),
    Z = sum_{j<n0} g_j^2, signatures, coefficient table [comp][sigma][d], 22 cubic right-continuous B-splines;
  * the layered decomposition over the 5 cap values b_1 < ... < b_5 (component caps and outer-shell caps): on the layer
    M0 in (b_{a-1}, b_a] the active coefficient vector is v_a = sum of the components with cap >= b_a, rows r are allowed
    iff their outer-shell cap >= b_a, and the layer measure is M^{b_a} - M^{b_{a-1}}; by linearity each cap b_a enters
    with + (v_a, mask_a) and - (v_{a+1}, mask_{a+1}), so caps are processed one at a time;
  * the Lean data files themselves (but they are parsed here by an own parser, not by code/sharifi182_data.py).
INDEPENDENT of program 1:
  * library: python-flint arb ball arithmetic (rigorous enclosures throughout: Z, g, K, cell masses, all polynomial
    products, the contraction), instead of mpmath + floored GMP integers;
  * Dickman primitive by a DIFFERENT closed form: for 2 <= u <= 3,
        rho(u) = 1 - log u + log u log(u-1) + Li2(1-u) + pi^2/12,   Phi(u) = Phi(u-1) + u rho(u)
    (from u rho(u) = int_{u-1}^u rho), with arb log and acb polylog; program 1 uses a primitive G(u) with Li2(1/u);
  * the outer-domain row ranges are DERIVED from the Lean shells (trialShells[0]) with the whole-cell upper total
    s+ = (r + 39)h (shell lower <= s+ < upper) and asserted equal to the paper's table (program 1 hard-codes the table);
    the cap values b are derived from the Lean caps / h;
  * B-splines: pointwise Cox-de Boor (de Boor's triangular scheme, NURBS-book BasisFuns) in exact fmpq at every s_r,
    with an exact partition-of-unity check, instead of symbolic span polynomials in r;
  * combinatorics: the 39-fold coordinate moments come from the exponential generating series in y = (y_2..y_6),
        A(y)(X) = sum_j K_j X^j exp(sum_e y_e t_j^e),  M_eta = m(eta)! [y^m(eta)] A(y)^39,
    expanded SYMBOLICALLY (exact fmpq series algebra, binary powering, truncated to the down-closed set of exponent
    vectors) into monomials A_0^a prod_e P_w (P_w = sum_j K_j t_j^w X^j), instead of the set-partition formula; each
    distinct monomial is then evaluated once with arb_poly products (DFS over descending prefixes) and accumulated
    into M_eta = sum_mono c_{eta,mono} mono;
  * contraction: I_b = sum_{+-} sum_eta sum_{r <= mask end} Q_eta(r) M_eta[r], Q_eta(r) = sum over ordered pairs
    (sigma, tau), sigma + tau = eta, of p_sigma(r) p_tau(r), p_sigma(r) = sum_d v[sigma][d] B_d(s_r), all in arb.
  Note: the "ball" strings in the JSON files are printed with 25 digits, so their displayed radius includes the
  decimal rounding; the actual ball is (mid_man_exp, rad_man_exp) = exact binary midpoint and radius (also "rad").
usage: sharifi182_check2.py [--prec 128] [--caps b1,b2,..] [--N Ntest] [--outdir code/data182] [--combine]
  --N: artificial smaller grid for testing (caps scaled by N/393216 and rounded, shells re-derived); writes to --outdir.
  Per-cap ball -> <outdir>/check2_I_cap_<b>.json; when all five exist (or --combine) -> <outdir>/check2_I_result.json."""
import sys, os, re, json, time, resource
from math import factorial
from fractions import Fraction
from flint import arb, acb, arb_poly, fmpq, ctx

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

PREC = int(arg("--prec", "128"))
ctx.prec = PREC
OUTDIR = arg("--outdir", "code/data182")
DATADIR = "code/data182"

# ---------------- own parser of the Lean data ----------------
RAT = r"\((-?\d+) / (\d+)\)|(-?\d+)"
def rats(txt):
    out = []
    for a, b, c in re.findall(RAT, txt):
        out.append(fmpq(int(a), int(b)) if b else fmpq(int(c)))
    return out
def section(txt, start, stop):
    i = txt.index("def " + start)
    j = txt.index(stop, i + 1) if stop else len(txt)
    return txt[i:j].split(":=", 1)[1]
def parse():
    p1 = open(DATADIR + "/TrialData182_part1.lean").read()
    p2 = open(DATADIR + "/TrialData182_part2_coefficients.lean").read()
    D = {}
    D["dim"] = int(section(p1, "trialDimension", "\n").strip())
    D["N"] = int(section(p1, "trialIntervals", "\n").strip())
    D["S"] = rats(section(p1, "trialRadius", "\n"))[0]
    D["knots"] = rats(section(p1, "trialKnots", "def "))
    sg = section(p1, "trialAngularSignature", "def ")
    D["sigs"] = [tuple(int(y) for y in re.findall(r"\d+", x)) for x in re.findall(r"\[([\d, ]*)\]", sg.split("![", 1)[1])]
    D["ccaps"] = rats(section(p1, "trialComponentCap", "structure"))
    sh = section(p1, "trialShells", "def ")
    outer = sh.split("[{", 2)[1].split("}]")[0]
    D["outer"] = [tuple(rats(re.search(r"lower := (.*?), upper := (.*?), cap := (.*?) ?$", blk.strip()).group(i))[0]
                        for i in (1, 2, 3)) for blk in outer.split("},")]
    D["lo"] = rats(section(p1, "trialDenominatorLower", "\n"))[0]
    D["up"] = rats(section(p1, "trialDenominatorUpper", "\n"))[0]
    co = rats(p2.split("trialDataCoefficient", 1)[1].split(":=", 1)[1].split("end PrimeGap182")[0])
    assert len(co) == 726, len(co)
    D["coeff"] = [[[co[c * 242 + s * 22 + d] for d in range(22)] for s in range(11)] for c in range(3)]
    return D

def A(q):
    return arb(q)

# ---------------- Dickman (own closed form, see docstring) ----------------
PI2_12 = arb.pi() ** 2 / 12
def rho23(u):
    lu = u.log()
    return 1 - lu + lu * (u - 1).log() + acb(1 - u).polylog(2).real + PI2_12
def Phi12(u):
    return 2 * u - u * u.log() - 1
def Phi(num, M):           # u = num/M
    u = arb(fmpq(num, M))
    if num <= M: return u
    if num <= 2 * M: return Phi12(u)
    assert num <= 3 * M
    return Phi12(u - 1) + u * rho23(u)

def cellmass(M, n):
    d = [arb(1)] * n
    prev = Phi(M, M)
    for j in range(M, n):
        cur = Phi(j + 1, M)
        d[j] = M * (cur - prev)
        prev = cur
    return d

def gq(t):
    return fmpq(21, 200) / (1 + t / 100) + fmpq(179, 200) / (1 + fmpq(907, 5) * t)

# ---------------- B-splines: pointwise Cox-de Boor, exact ----------------
def find_span(U, x, p, nb):
    if x < U[p] or x >= U[nb]:
        return None
    lo, hi = p, nb              # U[lo] <= x < U[hi]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if U[mid] <= x: lo = mid
        else: hi = mid
    return lo
def basis_funs(i, x, p, U):
    Nf = [fmpq(1)] + [fmpq(0)] * p
    left = [fmpq(0)] * (p + 1)
    right = [fmpq(0)] * (p + 1)
    for j in range(1, p + 1):
        left[j] = x - U[i + 1 - j]
        right[j] = U[i + j] - x
        saved = fmpq(0)
        for r in range(j):
            tmp = Nf[r] / (right[r + 1] + left[j - r])
            Nf[r] = saved + right[r + 1] * tmp
            saved = left[j - r] * tmp
        Nf[j] = saved
    return Nf                   # N_{i-p}, ..., N_i

# ---------------- symbolic y-series ----------------
EV = [2, 3, 4, 5, 6]
def mvec(sig):
    return tuple(sum(1 for x in sig if x == e) for e in EV)
def wt(m):
    return sum(e * x for e, x in zip(EV, m))
def mfact(m):
    out = 1
    for x in m: out *= factorial(x)
    return out
def downclose(ms):
    S, stack = set(), list(ms)
    while stack:
        m = stack.pop()
        if m in S: continue
        S.add(m)
        for i in range(len(m)):
            if m[i]: stack.append(m[:i] + (m[i] - 1,) + m[i + 1:])
    return S
def smul(X, Y, S):
    out = {}
    for m1, f1 in X.items():
        for m2, f2 in Y.items():
            m = tuple(a + b for a, b in zip(m1, m2))
            if m not in S: continue
            o = out.setdefault(m, {})
            for (a1, E1), c1 in f1.items():
                for (a2, E2), c2 in f2.items():
                    key = (a1 + a2, tuple(sorted(E1 + E2)))
                    o[key] = o.get(key, 0) + c1 * c2
    return out
def spow(X, d, S):
    res, base = None, X
    while d:
        if d & 1: res = base if res is None else smul(res, base, S)
        d >>= 1
        if d: base = smul(base, base, S)
    return res

def main():
    t0 = time.time()
    def log_(s):
        print("[%6.0f s, maxrss %.2f GB] %s" % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, s), flush=True)
    D = parse()
    KD = D["dim"]
    N0 = D["N"]
    NG = int(arg("--N", str(N0)))
    test = NG != N0
    n = NG - KD
    S_ = D["S"]
    h = S_ / NG
    SIGS = D["sigs"]
    assert KD == 39 and N0 == 393216 and len(SIGS) == 11 and len(D["knots"]) == 26
    # caps in cell units (full grid), derived from the Lean data
    h0 = S_ / N0
    comp0 = [c / h0 for c in D["ccaps"]]
    outer0 = [c / h0 for (_, _, c) in D["outer"]]
    assert all(x.q == 1 for x in comp0 + outer0)
    comp0 = [int(x.p) for x in comp0]
    outercaps0 = [int(x.p) for x in outer0]
    assert comp0 == [141720, 177528, 246256] and outercaps0 == [246256, 196608, 186253]
    scale = lambda c: c if not test else int(round(Fraction(c * NG, N0)))
    COMP = [scale(c) for c in comp0]
    # outer rows from the shells, s+ = (r + 39)h, shell = {lower <= s+ < upper}
    OUTER = []
    for (lo, up, _), c in zip(D["outer"], outercaps0):
        # r range: lo <= (r+KD)h < up  <=>  ceil(lo/h - KD) <= r <= ceil(up/h - KD) - 1
        a = lo / h - KD
        b = up / h - KD
        r0 = max(0, -((-a.p) // a.q))
        r1 = -((-b.p) // b.q) - 1
        r1 = min(r1, n - 1)
        OUTER.append(((int(r0), int(r1)), scale(c)))
    if not test:
        assert OUTER == [((0, 352697), 246256), ((352698, 376449), 196608), ((376450, 393176), 186253)], OUTER
    assert OUTER[0][0][0] == 0 and OUTER[-1][0][1] == n - 1 and all(OUTER[i][0][1] + 1 == OUTER[i + 1][0][0] for i in range(2))
    CAPS = sorted(set(COMP) | {c for _, c in OUTER})
    assert len(CAPS) == 5
    log_("grid N = %d, n = %d, caps %s, outer %s, prec %d" % (NG, n, CAPS, OUTER, PREC))
    todo = [int(x) for x in arg("--caps", ",".join(map(str, CAPS))).split(",")]
    os.makedirs(OUTDIR, exist_ok=True)
    capfile = lambda b: "%s/check2_I_cap_%d.json" % (OUTDIR, b)
    if "--combine" not in sys.argv:
        run_caps(todo, D, KD, n, h, SIGS, COMP, OUTER, CAPS, capfile, log_, NG)
    if all(os.path.exists(capfile(b)) for b in CAPS):
        combine(D, CAPS, capfile, test, log_, t0)

def run_caps(todo, D, KD, n, h, SIGS, COMP, OUTER, CAPS, capfile, log_, NG):
    U = D["knots"]
    p = 3
    nb = len(U) - p - 1            # 22
    # coefficient vectors per cap value
    vec = {}
    for b in CAPS:
        vec[b] = [[sum((D["coeff"][ci][s][d] for ci, c in enumerate(COMP) if c >= b), fmpq(0)) for d in range(nb)] for s in range(11)]
    # B-spline values at s_r (exact), stored as arb
    Bv = [None] * n
    rfirst = None
    for r in range(n):
        x = (r + fmpq(KD, 2)) * h
        i = find_span(U, x, p, nb)
        if i is None:
            continue
        Nf = basis_funs(i, x, p, U)
        assert sum(Nf, fmpq(0)) == 1 and all(v >= 0 for v in Nf)
        if rfirst is None: rfirst = r
        Bv[r] = (i - p, [A(v) for v in Nf])
    log_("B-splines by Cox-de Boor at %d points (first r = %d), partition of unity exact" % (n - rfirst, rfirst))
    # g, Z, t
    tq = [(j + fmpq(1, 2)) * h for j in range(n)]
    g2 = []
    for t in tq:
        gv = A(gq(t))
        g2.append(gv * gv)
    Z = sum(g2, arb(0))
    tj = [A(t) for t in tq]
    del tq
    log_("Z = %s" % Z.str(25, radius=True))
    # symbolic series
    pairs = {}
    for a in range(11):
        for c in range(11):
            pairs.setdefault(tuple(sorted(SIGS[a] + SIGS[c])), []).append((a, c))
    etas = sorted(pairs)
    meta = {eta: mvec(eta) for eta in etas}
    Sset = downclose(meta.values())
    Aser = {(0,) * 5: {(1, ()): fmpq(1)}}
    for m in Sset:
        if any(m): Aser[m] = {(0, (wt(m),)): fmpq(1, mfact(m))}
    Pser = spow(Aser, KD, Sset)
    form = {}
    for eta in etas:
        f = {}
        for (a, E), c in Pser[meta[eta]].items():
            c = c * mfact(meta[eta])
            assert c.q == 1 and c > 0 and a + len(E) == KD
            f[E] = int(c.p)
        form[eta] = f
    allE = sorted({E for f in form.values() for E in f})
    weights = sorted({w for E in allE for w in E})
    log_("symbolic y-series: %d etas, |S| = %d, %d distinct monomials, %d (eta, monomial) terms, weights %s"
         % (len(etas), len(Sset), len(allE), sum(len(f) for f in form.values()), weights))
    def mask_end(b):
        return max(r1 for (r0, r1), c in OUTER if c >= b)
    for b in todo:
        tc = time.time()
        a = CAPS.index(b)
        # ---- coordinate polynomials P_w = sum_j K_j t_j^w X^j  (K = K(b))
        d = cellmass(b, n)
        K = [g2[j] * d[j] / Z for j in range(n)]
        del d
        Pw = {0: arb_poly(K)}
        cur = K
        for w in range(1, max(weights) + 1):
            cur = [cur[j] * tj[j] for j in range(n)]
            if w in weights: Pw[w] = arb_poly(cur)
        del cur, K
        log_("cap %d: cell masses and %d coordinate polynomials" % (b, len(Pw)))
        # ---- A0 powers A0^(39-L)
        lens = sorted({len(E) for E in allE})
        A0pow = {}
        kmin = KD - max(lens)
        res, base, e = None, Pw[0], kmin
        while e:
            if e & 1: res = base if res is None else (res * base).truncate(n)
            e >>= 1
            if e: base = (base * base).truncate(n)
        del base
        A0pow[kmin] = res
        for k in range(kmin + 1, KD + 1):
            A0pow[k] = (A0pow[k - 1] * Pw[0]).truncate(n)
        for k in list(A0pow):
            if KD - k not in lens: del A0pow[k]
        # ---- monomials A0^(39-L) prod P_w by DFS over descending prefixes; M_eta = sum_mono c * mono
        nprod = 0
        Mp = {}
        bylen = {}
        for E in allE:
            bylen.setdefault(len(E), []).append(E)
        users = {E: [(eta, form[eta][E]) for eta in etas if E in form[eta]] for E in allE}
        for L in sorted(bylen):
            stack = [((), A0pow[KD - L])]
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
            A0pow.pop(KD - L, None)
            log_("cap %d: monomials of length %d done (%d products so far)" % (b, L, nprod))
        del Pw, A0pow
        # ---- contraction: + (v_a, mask_a), - (v_{a+1}, mask_{a+1})
        terms = [(+1, b, mask_end(b))]
        if a + 1 < len(CAPS):
            terms.append((-1, CAPS[a + 1], mask_end(CAPS[a + 1])))
        total = arb(0)
        for sgn, bv, rend in terms:
            vv = [[A(x) for x in row] for row in vec[bv]]
            pv = [[arb(0)] * n for _ in range(11)]
            for r in range(rfirst, rend + 1):
                d0, nf = Bv[r]
                for s in range(11):
                    row = vv[s]
                    pv[s][r] = row[d0] * nf[0] + row[d0 + 1] * nf[1] + row[d0 + 2] * nf[2] + row[d0 + 3] * nf[3]
            part = arb(0)
            for eta in etas:
                ml = Mp[eta].coeffs()
                ml += [arb(0)] * (n - len(ml))
                pl = [(pv[x], pv[y]) for (x, y) in pairs[eta]]
                for r in range(rfirst, rend + 1):
                    q = arb(0)
                    for (u, v) in pl:
                        q += u[r] * v[r]
                    part += q * ml[r]
            del pv
            log_("cap %d: term %+d (v of cap %d, rows <= %d): %s" % (b, sgn, bv, rend, part.str(20, radius=True)))
            total = total + part if sgn > 0 else total - part
        del Mp
        out = dict(cap=b, N=NG, prec=PREC, mid=total.mid().str(40, radius=False), rad=float(total.rad()),
                   mid_man_exp=[str(x) for x in total.mid().man_exp()], rad_man_exp=[str(x) for x in total.rad().man_exp()],
                   ball=total.str(25, radius=True), value_float=float(total.mid()), seconds=round(time.time() - tc),
                   maxrss_GB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, 3))
        json.dump(out, open(capfile(b), "w"), indent=1)
        log_("cap %d: contribution %s" % (b, out["ball"]))

def ball_from(rec):
    m, e = (int(x) for x in rec["mid_man_exp"])
    rm, re_ = (int(x) for x in rec["rad_man_exp"])
    mid = fmpq(m) * fmpq(2) ** e if e >= 0 else fmpq(m, 2 ** (-e))
    rad = fmpq(rm) * fmpq(2) ** re_ if re_ >= 0 else fmpq(rm, 2 ** (-re_))
    return mid, rad

def combine(D, CAPS, capfile, test, log_, t0):
    mids, rads, per = fmpq(0), fmpq(0), {}
    for b in CAPS:
        rec = json.load(open(capfile(b)))
        m, r = ball_from(rec)
        mids += m
        rads += r
        per[b] = rec
    lo, up = D["lo"], D["up"]
    out = dict(N=per[CAPS[0]]["N"], prec=per[CAPS[0]]["prec"])
    out["I_mid"] = arb(mids).mid().str(30, radius=False)
    out["I_rad"] = "%.6e" % float(rads)
    out["I_ball"] = "[%s +/- %.3e]" % (out["I_mid"], float(rads))
    out["I_lower_exact"] = str(Fraction(int((mids - rads).p), int((mids - rads).q)))
    out["I_upper_exact"] = str(Fraction(int((mids + rads).p), int((mids + rads).q)))
    if not test:
        out["published_lo"], out["published_up"] = float(lo), float(up)
        out["inside_published"] = bool(lo <= mids - rads and mids + rads <= up)
        out["rel_pos_in_enclosure"] = float((mids - lo) / (up - lo))
        p1 = json.load(open(DATADIR + "/I_result.json"))
        I1 = Fraction(p1["I_exact_of_floored"])
        mm = Fraction(int(mids.p), int(mids.q))
        out["program1_I"] = float(I1)
        out["diff_vs_program1"] = float(mm - I1)
        out["reldiff_vs_program1"] = float((mm - I1) / I1)
        out["program1_inside_ball"] = bool(mm - Fraction(int(rads.p), int(rads.q)) <= I1 <= mm + Fraction(int(rads.p), int(rads.q)))
        pc = {}
        for b in CAPS:
            f1 = DATADIR + "/I_cap_%d.json" % b
            if os.path.exists(f1):
                v1 = Fraction(json.load(open(f1))["value"])
                m, r = ball_from(per[b])
                m = Fraction(int(m.p), int(m.q))
                pc[str(b)] = dict(check2=per[b]["ball"], program1=float(v1), diff=float(m - v1), rel=float((m - v1) / v1), rad=per[b]["rad"])
        out["per_cap"] = pc
    out["per_cap_seconds"] = {str(b): per[b]["seconds"] for b in CAPS}
    out["per_cap_maxrss_GB"] = {str(b): per[b]["maxrss_GB"] for b in CAPS}
    log_(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(os.path.dirname(capfile(CAPS[0])), "check2_I_result.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
