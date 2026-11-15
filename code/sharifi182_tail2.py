#!/usr/bin/env python3
"""Rung 182: SECOND program for the cap tail term T = E_{H_C^c}(F)/N of the 182 trial (GPT-6 Astra / R. Sharifi,
bundle [M], k = 39), to be compared with code/sharifi182_tail.py (first program) and the Lean premise trialTailUpper.

    T = sum_i int 1_{H_C^c}(Y) K(Y) |E_i F(Y)|^2 dnu^38(Y) / (hZ)^39         ([M] Prop. 6.1, (6.7), (7.4), (8.1))

Independence: this file does NOT import sharifi182_check2*.py or sharifi182_tail.py. It follows the architecture of
program 1 (code/sharifi182_J.py, code/sharifi182_I.py: layered contraction over the largest-fragment layer, GMP
Kronecker products of fixed-point integer arrays, exact integer sums), but every piece is re-implemented here, with
these additions:
  * the step kernel K of [M] (5.5)-(5.6), exact in Python Fractions, written from notes/sources-182-tail.md;
  * the K-weighted tail mask chi_{T,a}(r') = 1 - [capC(r') >= b_a] (capC = 0 outside the H_C rows), H_C rows derived
    from the Lean premise trialShells[3] with lower <= (r'+38)h < upper and asserted equal to the [M] Sec. 7.2 table;
  * RIGOROUS error tracking: every fixed-point array carries an integer radius (directed bounds for every floor),
    inputs (g, Z, Dickman cell masses, t^e) are arb balls (python-flint), so the output is an enclosure;
  * B-splines from my own literal Cox-de Boor recursion (exact Fractions) + exact cubic interpolation per knot span;
  * Dickman cell masses from my own derivation of Phi(u) = int_0^u rho (u <= 3) in arb, tested against quadrature.
Shared with program 1 / program-1-tail: the Lean parser code/sharifi182_data.py, the reading of the source (layer
rule, d_{min(c,C_s)} for the erased coordinate, subset expansion of P_sigma, set-partition moments, 39h/Z).

Contraction (per cap b in B_T, by linearity in Delta M):  layers a over B_T = {141720,177528,186253,186491,196608,
246256}h (components, outer shells, H_C caps).  Cap b = b_a contributes
  + S(v^a, M^b; chi_{T,a}) - S(v^{a+1}, M^b; chi_{T,a+1}),
  S(v, M; chi) = sum_{r'} chi(r') K(block(r')) sum_{tau,ups} v_tau(r') v_ups(r') [X^{r'}] M_{38,tau+ups},
with v^a_tau(r') = sum_{s: C_s>=b_a} sum_{c>=b_a} sum_{(sigma,A): sigma\\A=tau} sum_{a'} chi_s(r'+a')
p_{c,sigma}(r'+a') g_{a'} d_{min(c,C_s)}(a') t_{a'}^{e(A)}.  chi_T vanishes for r' < R0 = 352699, so only rows
r' in [R0, n0) are needed (p on [R0, n0), erased cells a' < n0 - R0, moments sliced to [R0, n0)).
Per cap the per-block integer sums are stored, so T for any block kernel (and M_T for K = 1) is a cheap recombination.

usage: sharifi182_tail2.py --selftest
       sharifi182_tail2.py --kernel
       sharifi182_tail2.py --cap b [--P 256 --B 224]    (writes code/data182/tail2_cap_<b>.json; skips if present)
       sharifi182_tail2.py --cap b --P 192 --B 160 --suffix _P192B160   (precision cross-check, separate file)
       sharifi182_tail2.py --combine                    (writes code/data182/tail2_result.json)
Run from the repository root (or anywhere: it chdirs to it)."""
import sys, os, json, time, math, re, resource, random
from fractions import Fraction as Fr
import gmpy2
from flint import arb, fmpq, ctx

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "code"))
import sharifi182_data as sd          # Lean parser (shared with program 1)

ctx.prec = 384
sys.set_int_max_str_digits(0)
T0 = time.time()
def log(s):
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    print("[%6.0f s, maxrss %.2f GB] %s" % (time.time() - T0, rss, s), flush=True)

# ============================================================== exact / arb helpers
def fq(x):
    return fmpq(x.numerator, x.denominator)
def arb_of(x):
    return arb(fq(x)) if isinstance(x, Fr) else arb(x)
def arb_to_fr(x):
    """exact value of an arb point (mid / upper / lower)."""
    m, e = x.man_exp()
    m, e = int(m), int(e)
    return Fr(m << e) if e >= 0 else Fr(m, 1 << -e)
def fix(x, B):
    """x: arb ball. returns integer m >= 0 with |x*2^B - m| <= 2 for every value of the ball (x assumed >= 0)."""
    y = x * (1 << B)
    mid = y.mid()
    assert arb_to_fr(y.rad()) <= Fr(1, 2), "ball too wide for fixed point"
    m, e = mid.man_exp()
    m, e = int(m), int(e)
    v = m << e if e >= 0 else m >> (-e)          # floor
    return max(v, 0)                             # true value >= 0, so clipping keeps |.| <= rad + 1
FIXRAD = 2

def a2m(x):
    from mpmath import mpf
    q = arb_to_fr(x.mid())
    return mpf(q.numerator) / q.denominator

def ceil_div(a, b):
    return -((-a) // b)

# ============================================================== kernel K (5.5)-(5.6), exact
def lean_consts():
    p1 = open("code/data182/TrialData182_part1.lean").read()
    out = {}
    for nm in ["trialMinorantA", "trialRoughness", "trialAuxiliaryRetreat", "trialHingeThreshold", "trialRhoStar"]:
        m = re.search(r"def %s : ℚ := \((\d+) / (\d+)\)" % nm, p1)
        out[nm] = Fr(int(m.group(1)), int(m.group(2)))
    for nm in ["trialPairBins", "trialRadialBlocks"]:
        out[nm] = int(re.search(r"def %s : ℕ := (\d+)" % nm, p1).group(1))
    return out

def kernel(n0, k, h, rmax_mode="n0", mut=None):
    """returns dict: W (list of Fractions, j=1..1024), s (bin endpoints), BL, K (list over blocks), qplus."""
    L = lean_consts()
    lam, a, t, eps0 = L["trialRoughness"], L["trialMinorantA"], L["trialHingeThreshold"], L["trialAuxiliaryRetreat"]
    rhos, nb, nblk = L["trialRhoStar"], L["trialPairBins"], L["trialRadialBlocks"]
    assert t >= 2 * lam
    s = [2 * lam + Fr(j) * (a - 2 * lam) / nb for j in range(nb + 1)]
    W = []
    unit = Fr(1, 10 ** 25)
    for j in range(1, nb + 1):
        sj = s[j]
        sev = s[j - 1] if mut == "hinge_lo" else sj               # hinge evaluated at the upper endpoint (5.5)
        hinge = Fr(12, 5) * max(sev - t, Fr(0)) / (Fr(2, 5) - t)
        v = (sj - 2 * lam) / lam
        assert 0 <= v < 1
        L21 = Fr(0)
        vp = Fr(1)
        for m in range(1, 22):
            vp *= v
            L21 += vp / m if m % 2 else -vp / m
        x = (sj - s[j - 1]) * hinge / sj * L21
        assert x >= 0
        W.append(ceil_div(x.numerator * 10 ** 25, x.denominator) * unit)   # rounded upward to a multiple of 1e-25
    BL = ceil_div(n0, nblk)
    K, QP = [], []
    for b in range(nblk):
        rmax = BL * b + BL - 1
        if rmax_mode == "n0":
            rmax = min(rmax, n0 - 1)
        qp = rhos * (rmax + k - 1) * h
        tot = Fr(0)
        for j in range(1, nb + 1):
            if W[j - 1]:
                z = min(lam - eps0, (1 - s[j]) / 2 - qp - eps0)
                assert z > 0
                tot += W[j - 1] / z
        K.append(tot)
        QP.append(qp)
    return dict(W=W, s=s, BL=BL, K=K, qplus=QP, lam=lam, a=a, t=t, eps0=eps0, nb=nb, nblk=nblk)

# ============================================================== Dickman cell masses (arb)
LOG2 = None
def _consts():
    global LOG2, PHI2, A2
    LOG2 = arb(2).log()
    PHI2 = 3 - 2 * LOG2
    A2 = _A(arb(2))
def _A(u):
    """antiderivative of rho on [2,3] (own derivation):
       rho(u) = 1 - log u + log^2 u / 2 - log^2 2 / 2 + Li2(1/u) - Li2(1/2)."""
    lu = u.log()
    C2 = -LOG2 * LOG2 / 2 - arb(fmpq(1, 2)).polylog(2)
    um1 = u - 1
    t_um1 = um1 * um1.log() if um1 > 0 else arb(0)
    return (2 * u - u * lu + (u * lu * lu - 2 * u * lu + 2 * u) / 2 + u * (1 / u).polylog(2) - t_um1 + u * lu + C2 * u)
def Phi(u):
    """int_0^u rho_D, u an exact Fraction in [0,3]."""
    if LOG2 is None:
        _consts()
    assert 0 <= u <= 3
    ua = arb_of(u)
    if u <= 1:
        return ua
    if u <= 2:
        return 2 * ua - ua * ua.log() - 1
    return PHI2 + _A(ua) - A2
def dmass(M, upto):
    """d_M(j) = (1/h) int_{jh}^{(j+1)h} rho_D(t/(Mh)) dt = M (Phi((j+1)/M) - Phi(j/M)), j < upto (arb)."""
    out = []
    prev = None
    for j in range(upto):
        if j + 1 <= M:
            out.append(arb(1))
            continue
        if prev is None:
            prev = Phi(Fr(j, M))
        cur = Phi(Fr(j + 1, M))
        out.append(M * (cur - prev))
        prev = cur
    return out

# ============================================================== B-splines (literal Cox-de Boor, exact)
def bsplines_at(T, x, deg=3):
    """all B_{d,deg}(x), right-continuous: B_{i,0}(x) = 1 iff T_i <= x < T_{i+1}; 0/0 := 0."""
    m = len(T) - 1
    Bv = [Fr(1) if T[i] <= x < T[i + 1] else Fr(0) for i in range(m)]
    for p in range(1, deg + 1):
        nb = []
        for i in range(m - p):
            v = Fr(0)
            if T[i + p] != T[i] and Bv[i]:
                v += (x - T[i]) / (T[i + p] - T[i]) * Bv[i]
            if T[i + p + 1] != T[i + 1] and Bv[i + 1]:
                v += (T[i + p + 1] - x) / (T[i + p + 1] - T[i + 1]) * Bv[i + 1]
            nb.append(v)
        Bv = nb
    return Bv

def cubic_through(xs, ys):
    """exact coefficients c0..c3 of the cubic through 4 points (Newton form expanded)."""
    n = len(xs)
    dd = list(ys)
    coef = [dd[0]]
    for lev in range(1, n):
        dd = [(dd[i + 1] - dd[i]) / (xs[i + lev] - xs[i]) for i in range(n - lev)]
        coef.append(dd[0])
    poly = [Fr(0)] * 4
    basis = [Fr(1)]
    for i, c in enumerate(coef):
        for d, b in enumerate(basis):
            poly[d] += c * b
        nbasis = [Fr(0)] * (len(basis) + 1)
        for d, b in enumerate(basis):
            nbasis[d + 1] += b
            nbasis[d] -= xs[i] * b
        basis = nbasis
    return poly

def p_fixed(C, P, R0):
    """pf[(ci, si)] = list over r in [R0, n) of floor(p_{ci,si}(r) 2^P), p = sum_d coeff B_d((r + k/2)h). error in [0,1)."""
    T, h, k, n = C["knots"], C["h"], C["k"], C["n"]
    ncomp, nsig, nd = len(C["coeff"]), len(C["coeff"][0]), len(C["coeff"][0][0])
    L = n - R0
    pf = {(c, s): [0] * L for c in range(ncomp) for s in range(nsig)}
    xr = lambda r: (r + Fr(k, 2)) * h
    def pvals(r):
        Bv = bsplines_at(T, xr(r))
        return {(c, s): sum((C["coeff"][c][s][d] * Bv[d] for d in range(nd) if Bv[d]), Fr(0))
                for c in range(ncomp) for s in range(nsig)}
    covered = 0
    for i in range(len(T) - 1):
        if not T[i] < T[i + 1]:
            continue
        lo = T[i] / h - Fr(k, 2); hi = T[i + 1] / h - Fr(k, 2)
        rlo = ceil_div(lo.numerator, lo.denominator); rhi = ceil_div(hi.numerator, hi.denominator) - 1
        a, b = max(rlo, R0), min(rhi, n - 1)
        if a > b:
            continue
        if rhi - rlo >= 3:
            xs = [rlo, rlo + 1, rlo + 2, rlo + 3]
            vals = [pvals(r) for r in xs]
            for key in pf:
                poly = cubic_through([Fr(x) for x in xs], [v[key] for v in vals])
                Dn = 1
                for c in poly:
                    Dn = Dn * c.denominator // math.gcd(Dn, c.denominator)
                ic = [c.numerator * (Dn // c.denominator) for c in poly]
                arr = pf[key]
                for r in range(a, b + 1):
                    arr[r - R0] = ((((ic[3] * r + ic[2]) * r + ic[1]) * r + ic[0]) << P) // Dn
        else:
            for r in range(a, b + 1):
                v = pvals(r)
                for key in pf:
                    x = v[key]
                    pf[key][r - R0] = (x.numerator << P) // x.denominator
        covered += b - a + 1
    return pf, covered

# ============================================================== Kronecker products of nonnegative integer arrays
def kpack(arr, W):
    return gmpy2.mpz(int.from_bytes(b"".join(x.to_bytes(W, "little") for x in arr), "little"))
def kunpack(z, W, m):
    by = z.to_bytes(max(W * m, (z.bit_length() + 7) // 8), "little")
    return [int.from_bytes(by[i * W:(i + 1) * W], "little") for i in range(m)]
def kmul(a, b, m):
    """first m coefficients of the polynomial product a*b (a, b nonnegative)."""
    W = (max(a).bit_length() + max(b).bit_length() + max(len(a), len(b)).bit_length() + 8) // 8 + 1
    return kunpack(kpack(a, W) * kpack(b, W), W, m)

class Ball:
    """fixed-point array: true_j in [mid_j - rad, mid_j + rad] * 2^-B, mid_j >= 0, true_j >= 0."""
    __slots__ = ("mid", "rad", "sum")
    def __init__(self, mid, rad):
        self.mid, self.rad, self.sum = mid, rad, sum(mid)

def bmul(x, y, B, n):
    c = kmul(x.mid, y.mid, n)
    c = [v >> B for v in c]
    err = x.rad * (y.sum + n * y.rad) + y.rad * x.sum
    return Ball(c, (err >> B) + 2)

def corr_tail(I, w):
    """out[i] = sum_{a < L - i} I[i + a] w[a], I signed ints (len L), w >= 0 (len >= L). exact."""
    L = len(I)
    w = w[:L]
    out = [0] * L
    for sign in (1, -1):
        part = [max(sign * x, 0) for x in I]
        if not any(part) or not any(w):
            continue
        rev = part[::-1]
        pr = kmul(rev, w, L)
        for i in range(L):
            out[i] += sign * pr[L - 1 - i]
    return out

# ============================================================== combinatorics
def set_partitions(m):
    """all set partitions of range(m), as lists of blocks (restricted growth strings)."""
    def rec(i, rgs, mx):
        if i == m:
            blocks = [[] for _ in range(mx + 1)]
            for j, b in enumerate(rgs):
                blocks[b].append(j)
            yield blocks
            return
        for b in range(mx + 2):
            yield from rec(i + 1, rgs + [b], max(mx, b))
    if m == 0:
        yield []
        return
    yield from rec(1, [0], 0)
def falling(d, r):
    out = 1
    for i in range(r):
        out *= d - i
    return out

# ============================================================== configuration
def gq(t):
    return Fr(21, 200) / (1 + t / 100) + Fr(179, 200) / (1 + Fr(907, 5) * t)

def rows_from_shells(shells, d, h, n):
    """[(r0, r1, cap_cells)]: r with lower <= (r + d) h < upper, r in [0, n)."""
    out = []
    for lo, up, cap in shells:
        a = lo / h - d; b = up / h - d
        r0 = max(0, ceil_div(a.numerator, a.denominator))
        r1 = min(n - 1, ceil_div(b.numerator, b.denominator) - 1)
        c = cap / h
        assert c.denominator == 1
        if r0 <= r1:
            out.append((r0, r1, int(c)))
    return out

def real_config():
    D = sd.load()
    k = D["dim"]; N = D["N"]; n = N - k
    h = D["trialRadius"] / N
    outer = rows_from_shells(D["shells"]["outer"], k, h, n)
    hc = rows_from_shells(D["shells"]["subtractionC"], k - 1, h, n)
    assert outer == [(0, 352697, 246256), (352698, 376449, 196608), (376450, 393176, 186253)], outer
    assert hc == [(0, 352698, 246256), (352699, 371671, 186491)], hc
    comps = [c / h for c in D["component_caps"]]
    assert all(c.denominator == 1 for c in comps)
    comps = [int(c) for c in comps]
    assert comps == [141720, 177528, 246256]
    C = dict(k=k, n=n, h=h, knots=D["knots"], coeff=D["coeff"], sigs=D["signatures"], comps=comps, outer=outer, hc=hc,
             g=gq, D=D)
    C["BV"] = sorted(set(comps) | {c for _, _, c in outer} | {c for _, _, c in hc})
    assert C["BV"] == [141720, 177528, 186253, 186491, 196608, 246256]
    return C

def capC_of(C, r):
    for r0, r1, c in C["hc"]:
        if r0 <= r <= r1:
            return c
    return 0

def chi_T(C, r, bl, mut=None):
    c = capC_of(C, r)
    inside = (c > bl) if mut == "gt" else (c >= bl)     # Y in H_C iff M0(Y) <= capC(r') iff capC >= b_a on layer a
    return 0 if inside else 1

def first_tail_row(C):
    top = max(C["BV"])
    for r in range(C["n"]):
        if any(chi_T(C, r, bl) for bl in C["BV"]):
            return r
    return C["n"]

# ============================================================== one cap
def run_cap(C, b, P, B, mut=None, verbose=True, dm_fun=None):
    """returns dict with per-block signed integer sums S[blk] (units 2^-(2P+3B), before the factor k h / Z), and an
    integer bound err on sum over rows of |true - computed| (same units, without K)."""
    lg = log if verbose else (lambda s: None)
    k, n, h, BV = C["k"], C["n"], C["h"], C["BV"]
    KR = k - 1
    BL = C["BL"]
    dm_fun = dm_fun or dmass
    R0 = first_tail_row(C)
    L = n - R0
    ai = BV.index(b)
    layers = [ai] + ([ai + 1] if ai + 1 < len(BV) else [])
    sigs = C["sigs"]
    # Z and the profile (arb)
    tq = [(j + Fr(1, 2)) * h for j in range(n)]
    ga = [arb_of(C["g"](t)) for t in tq]
    Z = sum((x * x for x in ga), arb(0))
    ta = [arb_of(t) for t in tq]
    # row specification of the subset expansion P_sigma(Y + x) = sum_A x^{e(A)} P_{sigma \ A}(Y)
    rowspec = {}
    for si, sg in enumerate(sigs):
        for mask in range(1 << len(sg)):
            tau = tuple(sorted(sg[i] for i in range(len(sg)) if not mask >> i & 1))
            e = sum(sg[i] for i in range(len(sg)) if mask >> i & 1)
            d = rowspec.setdefault((tau, e), {})
            d[si] = d.get(si, 0) + 1
    taus = sorted({tau for tau, _ in rowspec})
    # erased marginals on [R0, n)
    pf, _ = p_fixed(C, P, R0)
    lg("cap %d: p arrays on rows [%d, %d)" % (b, R0, n))
    V, VR = {}, {}
    dcache, wcache = {}, {}
    for la in layers:
        bl = BV[la]
        groups = {}
        for r0, r1, Cs in C["outer"]:
            if Cs < bl:
                continue
            for ci, c in enumerate(C["comps"]):
                if c >= bl:
                    m = c if mut == "cmin" else min(c, Cs)
                    groups.setdefault((ci, m), []).append((r0, r1))
        acc = {tau: [0] * L for tau in taus}
        rad = {tau: 0 for tau in taus}
        for (ci, m), ranges in sorted(groups.items()):
            if m not in dcache:
                dcache[m] = dm_fun(m, L)
            dm = dcache[m]
            for (tau, e), sm in sorted(rowspec.items()):
                if (m, e) not in wcache:
                    wcache[(m, e)] = [fix(ga[a] * dm[a] * ta[a] ** e, B) for a in range(L)]
                we = wcache[(m, e)]
                I = [0] * L
                eI = 0
                for si, mult in sm.items():
                    arr = pf[(ci, si)]
                    eI += mult
                    for r0, r1 in ranges:
                        for r in range(max(r0, R0), r1 + 1):
                            I[r - R0] += mult * arr[r - R0]
                if not any(I):
                    continue
                cc = corr_tail(I, we)
                A = acc[tau]
                for i in range(L):
                    A[i] += cc[i]
                # |true - computed| <= sum_a |dI|(w + rw) + |I| rw, dI <= eI (p floored), rw = FIXRAD
                rad[tau] += eI * (sum(we) + L * FIXRAD) + FIXRAD * sum(abs(x) for x in I)
        V[la], VR[la] = acc, rad
        lg("cap %d: layer %d (b = %d) marginals, %d groups" % (b, la, bl, len(groups)))
    if all(not any(v) for la in layers for v in V[la].values()):
        lg("cap %d: all marginals vanish on the tail rows: contribution exactly 0" % b)
        return dict(S={}, err=0, R0=R0, exact_zero=True, Z=Z)
    # eta forms
    pairs = {}
    for t1 in taus:
        for t2 in taus:
            pairs.setdefault(tuple(sorted(t1 + t2)), []).append((t1, t2))
    etas = sorted(pairs)
    Mform = {}
    for eta in etas:
        f = {}
        for pi in set_partitions(len(eta)):
            if len(pi) > KR:
                continue
            E = tuple(sorted(sum(eta[i] for i in blk) for blk in pi))
            f[E] = f.get(E, 0) + falling(KR, len(pi))
        Mform[eta] = f
    allE = sorted({E for f in Mform.values() for E in f}, key=lambda E: (len(E), E))
    # coordinate arrays for the moments (cap b)
    dmb = dm_fun(b, n)
    es = sorted({0} | {x for E in allE for x in E})
    Kc = [ga[j] * ga[j] * dmb[j] / Z for j in range(n)]
    cols = {e: [0] * n for e in es}
    for j in range(n):
        cur, ep = Kc[j], 0
        for e in es:
            if e > ep:
                cur = cur * ta[j] ** (e - ep)
                ep = e
            cols[e][j] = fix(cur, B)
    Pa = {e: Ball(cols[e], FIXRAD) for e in es}
    del Kc, cols
    lg("cap %d: coordinate arrays (%d exponents)" % (b, len(es)))
    one = Ball([1 << B] + [0] * (n - 1), 0)
    def bpow(x, m):
        res, base = one, x
        while m:
            if m & 1:
                res = base if res is one else bmul(res, base, B, n)
            m >>= 1
            if m:
                base = bmul(base, base, B, n)
        return res
    lens = sorted({len(E) for E in allE})
    pw = {}
    mlo = KR - max(lens)
    pw[mlo] = bpow(Pa[0], mlo)
    for m in range(mlo + 1, KR + 1):
        pw[m] = bmul(pw[m - 1], Pa[0], B, n)
    lg("cap %d: powers %d..%d of the base array" % (b, mlo, KR))
    # moments ME[E] on the tail slice: DFS over the prefix tree of the E's
    ME, MR = {}, {}
    Eset = set(allE)
    prefixes = sorted({E[:i] for E in allE for i in range(1, len(E) + 1)}, key=lambda E: (len(E), E))
    children = {}
    for E in prefixes:
        children.setdefault(E[:-1], []).append(E)
    def store(E, prodball):
        full = pw[KR - len(E)] if prodball is None else bmul(pw[KR - len(E)], prodball, B, n)
        ME[E] = full.mid[R0:]
        MR[E] = full.rad
    cnt = [0]
    def dfs(E, ball):
        if E in Eset:
            store(E, ball)
            cnt[0] += 1
        for ch in children.get(E, []):
            nb = Pa[ch[-1]] if ball is None else bmul(ball, Pa[ch[-1]], B, n)
            dfs(ch, nb)
    dfs((), None)
    assert cnt[0] == len(allE)
    del pw, Pa
    lg("cap %d: %d moment arrays (sliced to the tail rows)" % (b, len(ME)))
    # contraction
    S = {}
    err = 0
    for kk, la in enumerate(layers):
        sgn = 1 if kk == 0 else -1
        bl = BV[la]
        v, vr = V[la], VR[la]
        rows = [i for i in range(L) if chi_T(C, R0 + i, bl, mut)]
        if not rows:
            continue
        vmax = {tau: max(abs(v[tau][i]) for i in rows) for tau in taus}
        blk = [(R0 + i) // BL for i in range(L)]
        part = {}
        for eta in etas:
            Mm = [0] * L
            rM = 0
            for E, cf in Mform[eta].items():
                arr = ME[E]
                rM += cf * MR[E]
                for i in rows:
                    Mm[i] += cf * arr[i]
            pl = [(v[t1], v[t2]) for t1, t2 in pairs[eta] if any(v[t1]) and any(v[t2])]
            if pl:
                for i in rows:
                    q = 0
                    for x, y in pl:
                        q += x[i] * y[i]
                    if q:
                        bb = blk[i]
                        part[bb] = part.get(bb, 0) + q * Mm[i]
            Qmax = sum(vmax[t1] * vmax[t2] for t1, t2 in pairs[eta])
            Qr = sum(vr[t1] * vmax[t2] + vr[t2] * vmax[t1] + vr[t1] * vr[t2] for t1, t2 in pairs[eta])
            Mmax = max(abs(Mm[i]) for i in rows)
            err += len(rows) * (Qmax * rM + Qr * (Mmax + rM))
        for bb, x in part.items():
            S[bb] = S.get(bb, 0) + sgn * x
        lg("cap %d: term %+d (layer %d, b = %d): %d tail rows" % (b, sgn, la, bl, len(rows)))
    return dict(S=S, err=err, R0=R0, exact_zero=False, Z=Z)

def value_of(res, C, Kblk, P, B):
    """arb ball for k h / Z * 2^-(2P+3B) * sum_blk K_blk S_blk, including the error bound."""
    if res["exact_zero"]:
        return arb(0)
    k, h = C["k"], C["h"]
    tot = sum((Kblk[bb] * x for bb, x in res["S"].items()), Fr(0))
    Kmax = max(abs(Kblk[bb]) for bb in range(len(Kblk)))
    sc = Fr(k) * h / (1 << (2 * P + 3 * B))
    fac = arb_of(sc) / res["Z"]
    errb = arb_of(Kmax * res["err"]) * fac
    v = arb_of(tot) * fac
    return arb(v.mid(), v.rad() + errb.abs_upper())

# ============================================================== production
DATA = "code/data182"
SUFFIX = sys.argv[sys.argv.index("--suffix") + 1] if "--suffix" in sys.argv else ""
def cap_file(b):
    return os.path.join(DATA, "tail2_cap_%d%s.json" % (b, SUFFIX))

def main_cap(b, P, B):
    f = cap_file(b)
    if os.path.exists(f):
        log("cap %d: checkpoint %s exists, skipping" % (b, f))
        return
    C = real_config()
    KT = kernel(C["n"], C["k"], C["h"])
    C["BL"] = KT["BL"]
    t0 = time.time()
    res = run_cap(C, b, P, B)
    out = dict(cap=b, P=P, B=B, R0=res["R0"], BL=C["BL"], exact_zero=res["exact_zero"],
               scale_exponent=2 * P + 3 * B, S={str(k_): str(v) for k_, v in sorted(res["S"].items())},
               err=str(res["err"]), Z=res["Z"].str(60, radius=True),
               seconds=round(time.time() - t0), maxrss_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
    val = value_of(res, C, KT["K"], P, B)
    out["T_part"] = val.str(30, radius=True)
    tmp = f + ".tmp"
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, f)
    log("cap %d: T part %s (written %s)" % (b, out["T_part"], f))

def ball_endpoints(x):
    return arb_to_fr(x.lower()), arb_to_fr(x.upper())

def main_combine():
    C = real_config()
    k, n, h = C["k"], C["n"], C["h"]
    KT = kernel(n, k, h)
    KN = kernel(n, k, h, rmax_mode="nominal")
    C["BL"] = KT["BL"]
    tq = [(j + Fr(1, 2)) * h for j in range(n)]
    Z = sum((arb_of(gq(t)) ** 2 for t in tq), arb(0))
    tot, totN, totM = arb(0), arb(0), arb(0)
    parts, parts_ball = {}, {}
    for b in C["BV"]:
        d = json.load(open(cap_file(b)))
        P, B = d["P"], d["B"]
        res = dict(S={int(k_): int(v) for k_, v in d["S"].items()}, err=int(d["err"]), exact_zero=d["exact_zero"], Z=Z)
        vT = value_of(res, C, KT["K"], P, B)
        vN = value_of(res, C, KN["K"], P, B)
        vM = value_of(res, C, [Fr(1)] * len(KT["K"]), P, B)
        tot += vT; totN += vN; totM += vM
        parts_ball[b] = vT
        parts[str(b)] = dict(T=vT.str(35, radius=True), T_float=float(vT.mid()), M_T=vM.str(35, radius=True),
                             T_nominal_rmax=vN.str(35, radius=True), seconds=d["seconds"], maxrss_GB=d["maxrss_GB"],
                             exact_zero=d["exact_zero"])
    TU = C["D"]["trialTailUpper"]
    lo, up = ball_endpoints(tot)
    loN, upN = ball_endpoints(totN)
    # program 1
    p1 = None
    p1f = os.path.join(DATA, "tail_result.json")
    if os.path.exists(p1f):
        p1 = json.load(open(p1f))
    nz = sum(1 for w in KT["W"] if w)
    out = dict(
        T=tot.str(40, radius=True), T_float=float(tot.mid()), T_radius=float(tot.rad()),
        T_radius_note="the radius shown in a decimal string also covers the rounding of the printed midpoint", T_lower=str(lo), T_upper=str(up),
        trialTailUpper=str(TU), trialTailUpper_float=float(TU),
        T_upper_le_trialTailUpper=bool(up <= TU), T_over_trialTailUpper_minus_1=float(arb_to_fr(tot.mid()) / TU - 1),
        M_T=totM.str(35, radius=True), T_over_M_T=float(tot.mid() / totM.mid()),
        nominal_rmax=dict(T=totN.str(40, radius=True), T_upper_le_trialTailUpper=bool(upN <= TU),
                          T_over_trialTailUpper_minus_1=float(arb_to_fr(totN.mid()) / TU - 1),
                          rel_change_vs_n0=float(arb_to_fr(totN.mid()) / arb_to_fr(tot.mid()) - 1),
                          K_511=float(KN["K"][511])),
        per_cap=parts,
        kernel=dict(nonzero_W=nz, sum_W=float(sum(KT["W"])), block_length=KT["BL"],
                    K_0=float(KT["K"][0]), K_459=float(KT["K"][459]), K_483=float(KT["K"][483]),
                    K_511=float(KT["K"][511]), K_0_40digits=arb_of(KT["K"][0]).str(40), K_511_40digits=arb_of(KT["K"][511]).str(40),
                    K_max=float(max(KT["K"])), K_min=float(min(KT["K"])),
                    monotone=all(KT["K"][i] <= KT["K"][i + 1] for i in range(len(KT["K"]) - 1)),
                    eq_5_7_holds=bool(0 <= min(KT["K"]) and max(KT["K"]) <= Fr(2194, 1000)),
                    eq_5_7_holds_nominal_rmax=bool(max(KN["K"]) <= Fr(2194, 1000))),
        reading=dict(rmax="min(768 b + 767, n0 - 1)", blocks_start_at=0, W_rounding="ceil to multiple of 1e-25",
                     hinge="upper bin endpoint", layers=C["BV"], HC_rows=C["hc"], outer_rows=C["outer"]))
    if p1:
        T1 = p1["T"]
        l1, u1 = Fr(T1["lower_exact"]), Fr(T1["upper_exact"])
        m1 = (l1 + u1) / 2
        m2 = arb_to_fr(tot.mid())
        out["program1"] = dict(T=T1["ball"], rel_diff_T2_vs_T1=float(m2 / m1 - 1), abs_diff=float(m2 - m1),
                               intervals_overlap=bool(lo <= u1 and l1 <= up), T2_ball_inside_T1_ball=bool(l1 <= lo and up <= u1),
                               per_cap={})
        for b in C["BV"]:
            f1 = os.path.join(DATA, "tail_cap_%d.json" % b)
            if os.path.exists(f1):
                x1 = json.load(open(f1))["T"]
                me = lambda pr: Fr(int(pr[0])) * Fr(2) ** int(pr[1])
                if isinstance(x1, dict):
                    c1, r1 = me(x1["mid_man_exp"]), me(x1["rad_man_exp"])
                else:
                    c1, r1 = Fr(0), Fr(0)
                v2 = parts_ball[b]
                l2, u2 = ball_endpoints(v2)
                c2 = arb_to_fr(v2.mid())
                out["program1"]["per_cap"][str(b)] = dict(
                    T1=x1["ball"] if isinstance(x1, dict) else str(x1), T2=parts[str(b)]["T"],
                    abs_diff=float(c2 - c1), rel_diff=float(c2 / c1 - 1) if c1 else None,
                    overlap=bool(l2 <= c1 + r1 and c1 - r1 <= u2), T2_inside_T1=bool(c1 - r1 <= l2 and u2 <= c1 + r1))
    json.dump(out, open(os.path.join(DATA, "tail2_result.json"), "w"), indent=1)
    log(json.dumps({k_: v for k_, v in out.items() if k_ != "per_cap"}, indent=1))

def main_kernel():
    C = real_config()
    KT = kernel(C["n"], C["k"], C["h"])
    KN = kernel(C["n"], C["k"], C["h"], rmax_mode="nominal")
    nz = sum(1 for w in KT["W"] if w)
    print("nonzero W: %d, sum W = %.7f, BL = %d" % (nz, float(sum(KT["W"])), KT["BL"]))
    for bb in (0, 459, 483, 511):
        print("K[%d] = %.6f" % (bb, float(KT["K"][bb])))
    print("max K = %.6f (n0-1 end), %.6f (nominal end); (5.7) holds: %s / %s" % (
        float(max(KT["K"])), float(max(KN["K"])), max(KT["K"]) <= Fr(2194, 1000), max(KN["K"]) <= Fr(2194, 1000)))

# ============================================================== self-test
# artificial cell caps; the second H_C cap is below an outer shell cap so that d_{min(c, C_s)} is exercised on tail rows
TESTCAPS = {(3, 32): dict(comps=[12, 15, 22], outer=[(0, 20, 22), (21, 26, 18), (27, 31, 14)], hc=[(0, 12, 22), (13, 29, 13)]),
            (4, 24): dict(comps=[9, 11, 17], outer=[(0, 15, 17), (16, 19, 13), (20, 23, 10)], hc=[(0, 8, 17), (9, 21, 9)])}
def test_config(k, n):
    rnd = random.Random(1820 + k)
    h = Fr(1, 25)
    # 26 knots: 4-fold ends and one 4-fold interior knot (a jump), spanning all s = (r + k/2) h, r < n
    top = (n + k) * h + Fr(1, 10)
    inner = [Fr(i, 20) * top for i in range(1, 9)] + [Fr(9, 20) * top] * 4 + [Fr(i, 20) * top for i in range(11, 17)]
    knots = [Fr(1, 50)] * 4 + inner + [top] * 4
    assert len(knots) == 26
    sigs = [(), (2,), (3,), (4,), (2, 2), (5,), (2, 3), (6,), (2, 4), (3, 3), (2, 2, 2)]
    coeff = [[[Fr(rnd.randint(-40, 40), rnd.randint(1, 9)) for d in range(22)] for s in range(11)] for c in range(3)]
    tc = TESTCAPS[(k, n)]
    comps, outer, hc = tc["comps"], tc["outer"], tc["hc"]
    C = dict(k=k, n=n, h=h, knots=knots, coeff=coeff, sigs=sigs, comps=comps, outer=outer, hc=hc, g=gq, BL=4)
    C["BV"] = sorted(set(comps) | {c for _, _, c in outer} | {c for _, _, c in hc})
    assert len(C["BV"]) >= 5 and all(n <= 3 * c for c in C["BV"])
    nblk = ceil_div(n, 4)
    C["Kblk"] = [Fr(7 + 3 * bb, 6 + bb % 3) for bb in range(nblk)]
    return C

def brute(C, dps=60):
    """literal definition, mpmath: k * sum_Y mass(Y) K(r') 1[Y not in H_C] (E_i F(Y))^2 / (hZ)^k."""
    from mpmath import mp, mpf
    mp.dps = dps
    k, n, h = C["k"], C["n"], C["h"]
    BV = C["BV"]
    nl = len(BV)
    T = C["knots"]
    m = lambda x: mpf(x.numerator) / x.denominator
    hm = m(h)
    tq = [m((j + Fr(1, 2)) * h) for j in range(n)]
    gg = [m(C["g"]((j + Fr(1, 2)) * h)) for j in range(n)]
    Z = sum(x * x for x in gg)
    D = {c: [a2m(x) for x in dmass(c, n)] for c in BV}
    # mass of (cell j, largest fragment in level l = (b_{l-1}, b_l]): h (d_{b_l}(j) - d_{b_{l-1}}(j))
    lm = [[hm * (D[BV[l]][j] - (D[BV[l - 1]][j] if l else 0)) for l in range(nl)] for j in range(n)]
    # radial factors per full index r, literal Cox-de Boor
    Bc = {}
    for r in range(n):
        Bv = [m(x) for x in bsplines_at(T, (r + Fr(k, 2)) * h)]
        for c in range(3):
            for s in range(11):
                Bc[(r, c, s)] = sum(m(C["coeff"][c][s][d]) * Bv[d] for d in range(22))
    def Psig(ts, sg):
        out = mpf(1)
        for part in sg:
            out *= sum(t ** part for t in ts)
        return out
    def outer_ok(r, M0l):
        for r0, r1, cap in C["outer"]:
            if r0 <= r <= r1:
                return BV[M0l] <= cap
        return False
    import itertools
    tot = mpf(0)
    for Y in itertools.product(range(n), repeat=k - 1):
        rp = sum(Y)
        if rp >= n:
            continue
        # E_i F(Y) as a function of the level of M0(Y)
        EF = [mpf(0)] * nl
        gY = 1
        for j in Y:
            gY *= gg[j]
        for a in range(n - rp):
            r = rp + a
            ts = [tq[j] for j in Y] + [tq[a]]
            fc = [gY * gg[a] * sum(Bc[(r, c, s)] * Psig(ts, C["sigs"][s]) for s in range(11)) for c in range(3)]
            for lY in range(nl):
                for lx in range(nl):
                    M0l = max(lY, lx)
                    if not outer_ok(r, M0l):
                        continue
                    val = sum(fc[c] for c in range(3) if C["comps"][c] >= BV[M0l])
                    EF[lY] += lm[a][lx] * val
        # Y mass grouped by the level of M0(Y): literal sum over the levels of each coordinate
        for ls in itertools.product(range(nl), repeat=k - 1):
            M0l = max(ls)
            mass = 1
            for j, l in zip(Y, ls):
                mass *= lm[j][l]
            if mass == 0:
                continue
            inHC = any(r0 <= rp <= r1 and BV[M0l] <= cap for r0, r1, cap in C["hc"])
            if inHC:
                continue
            tot += mass * C["Kblk"][rp // C["BL"]] * EF[M0l] ** 2
    return k * tot / (hm * Z) ** k

def pipeline(C, P, B, mut=None):
    tot = arb(0)
    for b in C["BV"]:
        res = run_cap(C, b, P, B, mut=mut, verbose=False)
        K = [Fr(1)] * len(C["Kblk"]) if mut == "noK" else C["Kblk"]
        tot += value_of(res, C, K, P, B)
    return tot

def dickman_test():
    """cell masses against quadrature of rho_D from its delay equation u rho'(u) = -rho(u - 1)."""
    from mpmath import mp, mpf, quad, log
    mp.dps = 40
    def rho(u):
        if u <= 1: return mpf(1)
        if u <= 2: return 1 - log(u)
        return 1 - log(2) - quad(lambda t: (1 - log(t - 1)) / t, [2, u])
    worst = 0
    for M, js in [(17, [16, 17, 25, 33, 34, 40, 49]), (11, [10, 21, 22, 23, 30, 32]), (141720, [393176, 283440, 141720])]:
        d = {j: (arb(1) if j + 1 <= M else M * (Phi(Fr(j + 1, M)) - Phi(Fr(j, M)))) for j in js}
        if M < 100:
            dl = dmass(M, max(js) + 1)
            assert all(abs(arb_to_fr((dl[j] - d[j]).mid())) < Fr(1, 10 ** 60) for j in js)
        for j in js:
            q = M * quad(lambda u: rho(u), [mpf(j) / M, mpf(j + 1) / M] if not (j < 2 * M < j + 1) else [mpf(j) / M, 2, mpf(j + 1) / M])
            x = a2m(d[j])
            worst = max(worst, abs(x - q) / q)
    return worst

def kernel_test():
    """(5.5)-(5.6) re-evaluated literally in mpmath (60 digits), per bin and per sampled r'."""
    from mpmath import mp, mpf, log
    mp.dps = 60
    C = real_config()
    n0, k, h = C["n"], C["k"], C["h"]
    L = lean_consts()
    lam, a, t, eps0, rhos = [mpf(x.numerator) / x.denominator for x in
                             (L["trialRoughness"], L["trialMinorantA"], L["trialHingeThreshold"], L["trialAuxiliaryRetreat"], L["trialRhoStar"])]
    hm = mpf(h.numerator) / h.denominator
    def lit_W(j):
        s = lambda i: 2 * lam + i * (a - 2 * lam) / 1024
        sj = s(j)
        w = mpf(12) / 5 * max(sj - t, 0) / (mpf(2) / 5 - t)
        v = (sj - 2 * lam) / lam
        L21 = sum((-1) ** (m + 1) * v ** m / m for m in range(1, 22))
        assert L21 >= log(1 + v) - mpf(10) ** -55
        return (sj - s(j - 1)) * w / sj * L21, sj
    lit = [lit_W(j) for j in range(1, 1025)]
    def lit_K(rp):
        blk = rp // 768
        rmax = min(768 * blk + 767, n0 - 1)
        q = rhos * (rmax + k - 1) * hm
        return sum(W / min(lam - eps0, (1 - sj) / 2 - q - eps0) for W, sj in lit)
    def check(KT):
        bad = 0
        for j in range(1024):
            x = lit[j][0]
            Wm = mpf(KT["W"][j].numerator) / KT["W"][j].denominator
            if not (Wm >= x - mpf(10) ** -50 and Wm - x <= mpf(10) ** -25):
                bad += 1
        dK = [mpf(KT["K"][rp // KT["BL"]].numerator) / KT["K"][rp // KT["BL"]].denominator - lit_K(rp) for rp in
              (0, 767, 768, 352699, 371671, 371672, 393176)]
        return bad, min(dK), max(dK)
    good = check(kernel(n0, k, h))
    mutd = check(kernel(n0, k, h, mut="hinge_lo"))
    return good, mutd

def selftest():
    ok = True
    # rows / caps derived from Lean (asserted inside)
    C = real_config()
    R0 = first_tail_row(dict(C, BL=768))
    print("real config: H_C rows %s, outer rows %s, first tail row %d" % (C["hc"], C["outer"], R0))
    ok &= R0 == 352699
    # B-spline sanity: partition of unity on the real knots inside [knots[3], S)
    for x in (Fr(3, 20), Fr(1, 2), Fr(324809441462533, 344528493755500), Fr(1)):
        ok &= sum(bsplines_at(C["knots"], x)) == 1
    # kernel
    (bad, dlo, dhi), (badm, dlom, dhim) = kernel_test()
    # rounding W up by < 1e-25 per bin moves K up by at most 1024e-25 / min z < 6e-21
    good = lambda b_, lo_, hi_: b_ == 0 and lo_ >= -1e-45 and hi_ <= 6e-21
    print("kernel vs literal mpmath (7 sampled r'): bins failing the rounding check %d, K - K_lit in [%.2e, %.2e]" % (bad, float(dlo), float(dhi)))
    print("  mutation hinge_lo: bins failing %d, K - K_lit in [%.2e, %.2e] -> %s" % (badm, float(dlom), float(dhim),
          "caught" if not good(badm, dlom, dhim) else "NOT CAUGHT"))
    ok &= good(bad, dlo, dhi) and not good(badm, dlom, dhim)
    # Dickman
    w = dickman_test()
    print("Dickman cell masses vs quadrature of the delay equation: max rel. dev %.2e" % float(w))
    ok &= w < 1e-30
    # brute force of the whole tail form
    for k, n in sorted(TESTCAPS):
        Ct = test_config(k, n)
        R0t = first_tail_row(Ct)
        t0 = time.time()
        bf = brute(Ct)
        tb = time.time() - t0
        from mpmath import mpf
        hi = pipeline(Ct, 200, 200)
        hv = a2m(hi)
        rel = abs(hv - bf) / abs(bf)
        print("k=%d n=%d (tail rows from %d): brute %s (%.0f s)  pipeline %s  rel dev %.2e" %
              (k, n, R0t, str(bf)[:32], tb, hi.str(30, radius=True), float(rel)))
        ok &= rel < 1e-40
        lo = pipeline(Ct, 40, 40)
        inside = arb(lo.mid() - mpf_str_arb(bf)).abs_upper() <= lo.rad()
        relrad = float(lo.rad() / abs(lo.mid()))
        print("  low precision P = B = 40: ball %s, contains brute: %s, rel radius %.1e" %
              (lo.str(20, radius=True), inside, relrad))
        ok &= bool(inside) and relrad < 1e-3
        for mut in ("noK", "gt", "cmin"):
            mv = pipeline(Ct, 120, 120, mut=mut)
            d = abs(a2m(mv) - bf) / abs(bf)
            caught = d > 1e-10
            print("  mutation %-5s: rel dev %.2e -> %s" % (mut, float(d), "caught" if caught else "NOT CAUGHT"))
            ok &= caught
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return ok

def mpf_str_arb(x):
    return arb(str(x))

def main():
    av = sys.argv
    P = int(av[av.index("--P") + 1]) if "--P" in av else 256
    B = int(av[av.index("--B") + 1]) if "--B" in av else 224
    if "--selftest" in av:
        sys.exit(0 if selftest() else 1)
    elif "--kernel" in av:
        main_kernel()
    elif "--combine" in av:
        main_combine()
    elif "--cap" in av:
        for b in av[av.index("--cap") + 1].split(","):
            main_cap(int(b), P, B)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
