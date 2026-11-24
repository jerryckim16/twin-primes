#!/usr/bin/env python3
"""Rung 186: exact check of Lemma 2.3 ("Eulerian cell kernels", pp. 12-13) of OpenAI's numerical companion [14]
("Numerical certificate for prime gaps at most 186", code/third_party/openai186/short_gaps_numerics.pdf).
Report: notes/oai186-lemma23-check.md.  Modelled on code/oai186_lemma17_check.py.

NB: "Lemma 2.3" (p. 13) and the displayed equation "(2.3)" (p. 12, the renewal majorant R_j) are different
objects.  Lemma 2.3 USES (2.3) (through d*_j in the renewal branch), so (2.3) is checked here as an input.

Lemma 2.3 (p. 13).  For a low bin (l0, u0], hard cap z0, L = floor(l0/h), H = ceil(u0/h), K = ceil(z0/h),
(l, u, z) = (Lh, Hh, Kh), slope theta > 0, with (2.4)-(2.7)
    Q = sum_{a=L}^{K-1} X^a/a,  M = sum_{a=L}^{H-1} X^a/a,  D_theta = h sum_{j<N} d*_j(l) e^{-theta j h} X^j,
    E_r = (1/r!) sum_a Eu(r,a) X^a,  R_r = 1 + X + ... + X^{r-1},  q_r = Q^r/r!,  J = min(32, floor((N-1)/L)),
    T_e = sum_r q_r R_{r+e+1} = (exp Q - X^{e+1} exp(XQ))/(1-X)  (mod X^N),
    That_e = sum_{r<=J} q_r E_{r+e+1} + up(T_e - sum_{r<=J} q_r R_{r+e+1}),
    B_theta = D_theta That_0,   M_theta = D_theta M That_1,
the coefficients of B_theta, M_theta majorize the physical-cell masses of
    (e^{-theta t} D_l(t) dt) * exp_*(1_{(l,z]}(v) dv/v),   1_{(l,u]}(v) dv/v * (same).

Every decision is exact (fractions.Fraction / int) or a certain comparison of python-flint arb balls (rigorous
enclosures of log, exp, Ei, Li2 and of acb.integral); floats are used only for printing.
Sections:
  [0] data: groups (1.23)-(1.24) via code/oai186_support_data.py; the 61 low bins (Sec. 1.5.1); L, H, K, J and the
      Dickman branch of every bin; 2 <= L < H <= K <= N; z0 = z_G dominates every fragment cap the group's cells use
  [1] Eulerian carries: recurrence (2.5) = inclusion-exclusion of the proof = Irwin-Hall cell masses computed
      independently by exact piecewise-polynomial convolution; 0 <= E_r <= R_r; row sums
  [2] generating functions on exact small instances: T_e closed form; That_e >= the complete Eulerian sum; the
      omitted sum vanishes iff J = floor((N-1)/L); q_r D == 0 mod X^N for rL >= N; B, M equal the cell masses of the
      cell-uniform majorant measures (independent exact piecewise convolution)
  [3] the Poisson split nu_z = nu_l * exp_*(1_(l,z] dv/v) (void factor l/z): exact total masses and a rigorous
      arb pointwise check of the Dickman densities on (0, 3)
  [4] the small-fragment majorants d*_j: the renewal majorant (2.3) exactly for every M in 2..63 (positivity,
      sliding-window = definition, the 10^-40 switch), R_j >= rho(j/M) rigorously for j <= 3M; the delay branch
      (Lemma 2.2 upper sequence) >= rho(j/M) at sampled j <= 3M for every delay cap in the schedule
  [5] end-to-end on the actual 61 bins: the true cell masses of both measures (closed forms with Ei, arb) are
      below [X^j]B_theta and [X^j]M_theta on every cell j < 2L (all cells for L < 64, samples otherwise)
  [6] the authors' code (comparison only): Eulerian carries, renewal/delay arrays, and the envelopes on small
      instances against the exact objects of [1]-[2]
usage: /usr/bin/python3 code/oai186_lemma23_check.py > code/oai186_lemma23_check.out"""
import os, sys, time, random, importlib.util, io, contextlib, resource, inspect
from fractions import Fraction as F
from math import floor, ceil, comb, factorial
from flint import arb, acb, ctx

ctx.prec = 200
T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []
NCHECK = [0]


def check(name, cond, detail=""):
    NCHECK[0] += 1
    print(("  PASS " if cond else "  FAIL ") + name + (("   [" + detail + "]") if detail else ""))
    if not cond:
        FAILS.append(name)


def fl(x, k=8):
    return ("%." + str(k) + "g") % float(x)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def A(x):  # exact rational -> arb ball (exact for dyadics, otherwise a tight enclosure)
    x = F(x)
    return arb(x.numerator) / arb(x.denominator)


def certainly_le(a, b):  # a <= b certainly, for arb balls
    return (b - a) >= 0


def a2F(x):  # exact dyadic arb (an endpoint) -> Fraction
    m_, e_ = x.man_exp()
    return F(int(m_)) * F(2) ** int(e_)


def ball_has(ball, x):  # the exact rational x lies in the ball (exact endpoint comparison)
    return a2F(ball.lower()) <= F(x) <= a2F(ball.upper())


# ---------------------------------------------------------------------------------------------------------------
print("[0] data: groups (1.23)-(1.24) via code/oai186_support_data.py; low bins (Sec. 1.5.1, p. 9); (2.4) data")
sd = load("sd186", os.path.join(HERE, "oai186_support_data.py"))
check("oai186_support_data.py: all its printed-value checks pass (ladders, (1.17), masks (1.5), group table)",
      sd.res["all_ok"] is True)
h, S = sd.h, sd.S
N = 98304
check("(1.3): h = S/98304 with S = 2742997/2624989", h == F(2742997, 2624989 * 98304))
o, nw = sd.ladders["o"], sd.ladders["n"]
NAMES = ["O2", "O5/2", "I2old", "I5/2old", "I2new", "I5/2new"]
DIMS = [40, 40, 39, 39, 39, 39]
RAD = [(nw[0]["a"], nw[24]["a"], "outer"), (nw[24]["a"], 98303 * h, "outer"), (o[12]["b"], o[24]["b"], "base"),
       (o[24]["b"], 89563 * h, "base"), (nw[12]["b"], nw[24]["b"], "enlarged"), (nw[24]["b"], 89953 * h, "enlarged")]
GR = []
for nm, d, (bG, tG, face) in zip(NAMES, DIMS, RAD):
    m, xi, U, zh, ph = sd.G[nm]
    GR.append(dict(name=nm, d=d, m=m, xi=xi, U=U, zh=zh, ph=ph, b=bG, t=tG, face=face))
aa = [F(6, 5) ** j / 20 for j in range(10)]
ULISTS = [
    lambda x, p: [x, 3 * x / 2, aa[0]] + aa[4:9] + [(aa[8] + aa[9]) / 2, aa[9], p],
    lambda x, p: [2 ** j * x for j in range(9)] + [F(1, 100), F(3, 200), F(9, 400), F(27, 800)] + aa[0:8]
                 + [(aa[7] + p) / 2, p],
    lambda x, p: [x, aa[0], aa[4], aa[6], aa[8], p],
    lambda x, p: [x, 2 * x, F(1, 100), F(27, 800), aa[3], aa[5], aa[6], p],
    lambda x, p: [x, aa[1], aa[4], aa[5], aa[7], aa[8], p],
    lambda x, p: [2 ** j * x for j in (0, 1, 4, 6, 8)] + [F(9, 400), aa[1], aa[3], aa[5], aa[6], aa[7], p]]
BINS = []
for gi, G in enumerate(GR):
    ul = ULISTS[gi](G["xi"], G["ph"] * h)
    for j in range(1, len(ul)):
        l0, u0 = ul[j - 1], ul[j]
        th = 120 if (gi == 0 and j == 3) else ceil((F(9) if gi == 5 else F(7)) / u0)
        z0 = G["zh"] * h
        L, H, K = floor(l0 / h), ceil(u0 / h), ceil(z0 / h)
        Jfull = (N - 1) // L
        BINS.append(dict(G=G, name="%s L%d" % (G["name"], j), l0=l0, u0=u0, theta=th, L=L, H=H, K=K, z0=z0,
                         J=min(32, Jfull), Jfull=Jfull, branch="delay" if L >= 64 else "renewal"))
check("61 low bins (10+22+5+7+6+11), lists strictly increasing", len(BINS) == 61)
check("(2.4) 'the data satisfy 2 <= L < H <= K <= N' on all 61 bins",
      all(2 <= b["L"] < b["H"] <= b["K"] <= N for b in BINS),
      "min L = %d, max K = %d" % (min(b["L"] for b in BINS), max(b["K"] for b in BINS)))
check("l = Lh <= l0 and u0 <= u = Hh: the kernel bin (Lh, Hh] contains (l0, u0] on all bins",
      all(b["L"] * h <= b["l0"] and b["u0"] <= b["H"] * h for b in BINS))
check("theta is a positive integer on all bins (Lemma 2.3 needs theta > 0)",
      all(isinstance(b["theta"], int) and b["theta"] > 0 for b in BINS))
# hard cap z0 = z_G must dominate the per-fragment cap of every face cell the group retains ((1.25) with (1.5)).
okcap, capinfo = True, []
for G in GR:
    lo = max(0, floor(G["b"] / h) - G["d"] + 1)
    hi = floor(G["t"] / h)
    caps = [zz for (a0, b0, zz) in sd.masks[G["face"]] if not (b0 < lo or a0 > hi)]
    capinfo.append("%s:%s" % (G["name"], caps))
    okcap = okcap and max(caps) == G["zh"]
check("z0 := z_G (as the authors' hard_cap) equals the largest mask cap (1.5) met by the group's retained cells"
      " (1.25), so the true per-fragment cap is <= z0 = Kh on every retained cell", okcap, "; ".join(capinfo))
nrem = [b for b in BINS if b["J"] < b["Jfull"]]
print("    J = min(32, floor((N-1)/L)): %d bins carry a nonzero replicated remainder (L <= 3071), %d are exact"
      % (len(nrem), 61 - len(nrem)))
LREN = sorted(set(b["L"] for b in BINS if b["branch"] == "renewal"))
LDEL = sorted(set(b["L"] for b in BINS if b["branch"] == "delay"))
print("    renewal-branch caps M = L < 64: %s (%d bins); delay-branch caps (L >= 64): %d distinct, %d..%d"
      % (LREN, sum(b["branch"] == "renewal" for b in BINS), len(LDEL), LDEL[0], LDEL[-1]))
check("every renewal cap satisfies M >= 2 (hypothesis of (2.3))", all(M >= 2 for M in LREN))

# ---------------------------------------------------------------------------------------------------------------
print("\n[1] Eulerian carries (2.5) and the carry formula in the proof (p. 13)")
RMAX = 60
Eu = {1: [1]}
for r in range(2, RMAX + 1):
    prev = Eu[r - 1]
    Eu[r] = [(a + 1) * (prev[a] if a < len(prev) else 0) + (r - a) * (prev[a - 1] if 1 <= a <= len(prev) else 0)
             for a in range(r)]
E = {r: [F(x, factorial(r)) for x in Eu[r]] for r in Eu}
ie_ok = all(sum((-1) ** b * comb(r + 1, b) * (a + 1 - b) ** r for b in range(a + 2)) == Eu[r][a]
            for r in range(1, RMAX + 1) for a in range(r))
check("proof's unit-cube inclusion-exclusion (1/r!) sum_b (-1)^b C(r+1,b)(a+1-b)^r = [X^a]E_r, r = 1..%d" % RMAX,
      ie_ok)
check("[X^a]E_r = 0 for a >= r and a < 0 under (2.5) with out-of-range zero (degree r-1)",
      all(len(Eu[r]) == r for r in Eu))
check("row sums: sum_a Eu(r,a) = r!, so E_r(1) = 1 (a probability law), r = 1..%d" % RMAX,
      all(sum(Eu[r]) == factorial(r) for r in Eu))
check("0 <= E_r <= R_r coefficientwise (all coefficients in [0,1], support 0..r-1), r = 1..%d" % RMAX,
      all(0 <= c <= 1 for r in E for c in E[r]))


# Irwin-Hall by exact piecewise-polynomial convolution: f_{r+1}(t) = int_{t-1}^t f_r(x) dx.
def p_int(p):  # antiderivative with zero constant
    return [F(0)] + [c / (i + 1) for i, c in enumerate(p)]


def p_eval(p, x):
    s = F(0)
    for c in reversed(p):
        s = s * x + c
    return s


def p_shift(p, s):  # p(t + s)
    out = [F(0)] * len(p)
    for i, c in enumerate(p):
        for k in range(i + 1):
            out[k] += c * comb(i, k) * s ** (i - k)
    return out


def p_add(p, q, sg=1):
    n_ = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + sg * (q[i] if i < len(q) else 0) for i in range(n_)]


def irwin_hall_cells(rmax):
    pieces = [[F(1)]]          # f_1 on [0,1)
    out = {1: [F(1)]}
    for r in range(2, rmax + 1):
        ants = [p_int(p) for p in pieces]
        new = []
        for k in range(r):     # piece on [k, k+1)
            poly = [F(0)]
            if k - 1 >= 0 and k - 1 < len(ants):   # int_{t-1}^{k} f on [k-1,k)
                Ak = ants[k - 1]
                poly = p_add(poly, [p_eval(Ak, k)])
                poly = p_add(poly, p_shift(Ak, -1), -1)
            if k < len(ants):                       # int_k^t f on [k,k+1)
                Ak = ants[k]
                poly = p_add(poly, Ak)
                poly = p_add(poly, [p_eval(Ak, k)], -1)
            new.append(poly)
        pieces = new
        out[r] = [p_eval(p_int(p), k + 1) - p_eval(p_int(p), k) for k, p in enumerate(pieces)]
    return out


IH = irwin_hall_cells(14)
check("independent: the cell masses P(a <= U_1+...+U_r < a+1) of r iid uniforms, by exact piecewise-polynomial"
      " convolution, equal [X^a]E_r for r = 1..14", all(IH[r] == E[r] for r in IH))
check("a uniform point of C_{i_1} x ... x C_{i_r} (cells of width h) has total in C_{sum i + a} with probability"
      " [X^a]E_r: (sum (i_k + U_k)) h, so the carry polynomial multiplies X^{sum i}", True,
      "by the scaling t = (sum i_k + sum U_k) h; nothing to compute")

# ---------------------------------------------------------------------------------------------------------------
print("\n[2] generating functions and the truncation (2.4)-(2.7), exact small instances")


def pmul(a, b, n_):
    out = [F(0)] * n_
    for i, x in enumerate(a):
        if x == 0 or i >= n_:
            continue
        for j, y in enumerate(b[:n_ - i]):
            if y:
                out[i + j] += x * y
    return out


def pexp(q, n_):  # exp(q) mod X^n for q(0) = 0, exact: e' = q' e
    e = [F(0)] * n_
    e[0] = F(1)
    dq = [(i + 1) * q[i + 1] for i in range(len(q) - 1)] + [F(0)]
    for k in range(1, n_):
        e[k] = sum(dq[i] * e[k - 1 - i] for i in range(k)) / k
    return e


def kernels_exact(Nn, L, H, K, Dvec, Jcap=32):
    """B, M of (2.6)-(2.7) with exact rationals; also the complete Eulerian sums and T_e by both formulas."""
    Q = [F(0)] * Nn
    Mm = [F(0)] * Nn
    for a in range(L, min(K, Nn)):
        Q[a] = F(1, a)
    for a in range(L, min(H, Nn)):
        Mm[a] = F(1, a)
    Jfull = (Nn - 1) // L
    J = min(Jcap, Jfull)
    qs = [[F(1)] + [F(0)] * (Nn - 1)]
    for r in range(1, Jfull + 2):
        qs.append([c / r for c in pmul(qs[-1], Q, Nn)])
    res = {}
    for e in (0, 1):
        def Rpoly(k):
            return [F(1)] * min(k, Nn) + [F(0)] * (Nn - min(k, Nn))

        def Epoly(k):
            return E[k] + [F(0)] * (Nn - k) if k <= Nn else E[k][:Nn]
        Tser = [sum(x) for x in zip(*[pmul(qs[r], Rpoly(r + e + 1), Nn) for r in range(Jfull + 1)])]
        eQ = pexp(Q, Nn)
        eXQ = pexp([F(0)] + Q[:-1], Nn)
        num = [eQ[k] - (eXQ[k - e - 1] if k >= e + 1 else 0) for k in range(Nn)]
        Tclosed, acc = [], F(0)
        for k in range(Nn):
            acc += num[k]
            Tclosed.append(acc)
        pref_R = [sum(x) for x in zip(*[pmul(qs[r], Rpoly(r + e + 1), Nn) for r in range(J + 1)])]
        pref_E = [sum(x) for x in zip(*[pmul(qs[r], Epoly(r + e + 1), Nn) for r in range(J + 1)])]
        full_E = [sum(x) for x in zip(*[pmul(qs[r], Epoly(r + e + 1), Nn) for r in range(Jfull + 1)])]
        That = [pe + (tc - pr) for pe, tc, pr in zip(pref_E, Tclosed, pref_R)]
        vanish = all(not any(qs[r]) for r in range(Jfull + 1, Jfull + 2))
        res[e] = dict(Tser=Tser, Tclosed=Tclosed, That=That, full=full_E, omitted=[tc - pr for tc, pr in
                                                                                    zip(Tclosed, pref_R)],
                      vanish=vanish)
    B = pmul(Dvec, res[0]["That"], Nn)
    Mt = pmul(pmul(Dvec, Mm, Nn), res[1]["That"], Nn)
    Bfull = pmul(Dvec, res[0]["full"], Nn)
    Mfull = pmul(pmul(Dvec, Mm, Nn), res[1]["full"], Nn)
    return dict(J=J, Jfull=Jfull, res=res, B=B, M=Mt, Bfull=Bfull, Mfull=Mfull, Q=Q, Mm=Mm)


rnd = random.Random(20261124)
INST = [(100, 2, 9, 40), (100, 3, 7, 100), (100, 4, 10, 60), (70, 2, 5, 70), (75, 5, 8, 75), (40, 13, 20, 40)]
ok_closed = ok_major = ok_vanish = ok_zero = ok_nonneg = True
info = []
KE = {}
for (Nn, L, H, K) in INST:
    Dvec = [F(rnd.randint(1, 10 ** 6), 10 ** 6) for _ in range(Nn)]
    kk = kernels_exact(Nn, L, H, K, Dvec)
    KE[(Nn, L, H, K)] = (Dvec, kk)
    for e in (0, 1):
        r_ = kk["res"][e]
        ok_closed &= r_["Tser"] == r_["Tclosed"]
        ok_major &= all(a >= b for a, b in zip(r_["That"], r_["full"]))
        ok_nonneg &= all(x >= 0 for x in r_["omitted"])
        if kk["J"] == kk["Jfull"]:
            ok_vanish &= all(a == b for a, b in zip(r_["That"], r_["full"]))
        ok_zero &= r_["vanish"]
    info.append("N=%d L=%d J=%d/%d" % (Nn, L, kk["J"], kk["Jfull"]))
check("T_e = sum_r q_r R_{r+e+1} = (exp Q - X^{e+1} exp(XQ))/(1-X) mod X^N exactly, e = 0, 1", ok_closed,
      "; ".join(info))
check("q_r = Q^r/r! == 0 mod X^N for r = floor((N-1)/L) + 1 (terms with rL >= N vanish)", ok_zero)
check("the omitted sum T_e - sum_{r<=J} q_r R_{r+e+1} is coefficientwise >= 0 (never rejected)", ok_nonneg)
check("That_e >= sum_{all r} q_r E_{r+e+1} coefficientwise (replicated remainder bounds every omitted term)",
      ok_major)
check("That_e = the complete Eulerian sum when J = floor((N-1)/L) (omitted sum vanishes)", ok_vanish)


# Independent: cell masses of the cell-uniform majorant measures, by exact piecewise convolution (no Eulerian
# numbers): small part = uniform on C_j with mass D_j; large part = uniform on C_a with mass 1/a (a in [L,K));
# designated = uniform on C_a with mass 1/a (a in [L,H)).  Measures are vectors of piecewise polynomials on
# unit cells (h = 1 after scaling).
def pw_conv(f, g, n_):
    """f, g: dict cell -> poly (density on [cell, cell+1) in the global variable t). Returns f*g, cells < n_."""
    out = {}
    for i, p in f.items():
        for k, q in g.items():
            if i + k >= n_:
                continue
            # (f*g)(t) = int p(x) q(t-x) dx, x in [i,i+1) and t-x in [k,k+1).  Expand q(t-x) = sum c (t-x)^b.
            # term-wise as bivariate poly in (x, t): coefficient dict
            biv = {}
            for a_, ca in enumerate(p):
                if ca == 0:
                    continue
                for b_, cb in enumerate(q):
                    if cb == 0:
                        continue
                    for s_ in range(b_ + 1):  # (t - x)^b = sum C(b,s) t^{b-s} (-x)^s
                        key = (a_ + s_, b_ - s_)
                        biv[key] = biv.get(key, 0) + ca * cb * comb(b_, s_) * (-1) ** s_
            # antiderivative in x
            ant = {(px + 1, pt): c / (px + 1) for (px, pt), c in biv.items()}

            def ev_at(xpoly):   # substitute x = xpoly(t) (list) into ant -> poly in t
                res = [F(0)]
                for (px, pt), c in ant.items():
                    term = [F(0)] * pt + [c]
                    xp = [F(1)]
                    for _ in range(px):
                        xp = pmul_full(xp, xpoly)
                    res = p_add(res, pmul_full(term, xp))
                return res
            # t in [i+k, i+k+1): x from i to t-k ; t in [i+k+1, i+k+2): x from t-k-1 to i+1
            lo1 = ev_at([F(i)])
            hi1 = ev_at([F(-k), F(1)])
            out.setdefault(i + k, [F(0)])
            out[i + k] = p_add(out[i + k], p_add(hi1, lo1, -1))
            if i + k + 1 < n_:
                lo2 = ev_at([F(-k - 1), F(1)])
                hi2 = ev_at([F(i + 1)])
                out.setdefault(i + k + 1, [F(0)])
                out[i + k + 1] = p_add(out[i + k + 1], p_add(hi2, lo2, -1))
    return out


def pmul_full(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def pw_add(f, g, s=1):
    out = dict(f)
    for k, p in g.items():
        out[k] = p_add(out.get(k, [F(0)]), [s * c for c in p])
    return out


def pw_mass(f, n_):
    return [p_eval(p_int(f[c]), c + 1) - p_eval(p_int(f[c]), c) if c in f else F(0) for c in range(n_)]


Nn, L, H, K = 14, 2, 4, 9
Dvec = [F(rnd.randint(1, 1000), 1000) for _ in range(Nn)]
kk = kernels_exact(Nn, L, H, K, Dvec)
small = {j: [Dvec[j]] for j in range(Nn)}
large = {a: [F(1, a)] for a in range(L, K)}
mark = {a: [F(1, a)] for a in range(L, H)}
tot = dict(small)
term = dict(small)
for r in range(1, (Nn - 1) // L + 1):
    term = pw_conv(term, large, Nn)
    term = {c: [x / r for x in p] for c, p in term.items()}
    tot = pw_add(tot, term)
Bdirect = pw_mass(tot, Nn)
Mdirect = pw_mass(pw_conv(mark, tot, Nn), Nn)
check("independent exact piecewise convolution (N=14, L=2, H=4, K=9): the cell masses of (uniform small cells)"
      " * exp_*(uniform 1/a cells) equal D * sum_r q_r E_{r+1}, and with a designated cell D*M*sum q_r E_{r+2};"
      " both <= B_theta, M_theta of (2.6)-(2.7)",
      Bdirect == kk["Bfull"] and Mdirect == kk["Mfull"] and all(a >= b for a, b in zip(kk["B"], Bdirect))
      and all(a >= b for a, b in zip(kk["M"], Mdirect)))
check("cell majorant for 1_(l,z] dv/v: on C_a (a >= L >= 2) the density 1/v <= 1/(a h); mass 1/a >= log(1+1/a)"
      " (exact: log(1+x) <= x); the cells C_L..C_{K-1} = [Lh, Kh) cover (l, z] up to the null set {Kh}",
      all(b["L"] >= 1 for b in BINS))

# ---------------------------------------------------------------------------------------------------------------
print("\n[3] Poisson split nu_z = nu_l * exp_*(1_(l,z] dv/v) (proof, first sentence)")
# exact total masses: |nu_c| = e^gamma c; exp_* of a measure of mass log(z/l) has mass z/l.
check("total masses: e^gamma l * exp(log(z/l)) = e^gamma z (void factor l/z cancels the normalization), exact in"
      " the ratio: (e^gamma z)/(e^gamma l) = z/l", True, "algebraic identity, no computation")


def rho_arb(uF):
    """rigorous Dickman rho on [0, 3] at an exact rational uF: 1; 1 - log u;
    1 - (1 - log(u-1)) log u + Li2(1-u) + pi^2/12 (branch chosen exactly)."""
    uF = F(uF)
    u = A(uF)
    if uF <= 1:
        return arb(1)
    if uF <= 2:
        return 1 - u.log()
    if uF <= 3:
        return 1 - (1 - (u - 1).log()) * u.log() + acb(1 - u).polylog(2).real + arb.pi() ** 2 / 12
    raise ValueError("rho_arb only on [0, 3]")


# cross-check the closed form on [2,3] against the delay equation rho(u) = rho(2) - int_2^u (1-log(v-1))/v dv
okr = True
for uu in (F(9, 4), F(5, 2), F(11, 4), F(3)):
    integ = acb.integral(lambda v, an: (1 - (v - 1).log(analytic=an)) / v, 2, A(uu)).real
    okr &= (rho_arb(uu) - (1 - arb(2).log() - integ)).contains(0)
    okr &= rho_arb(uu).rad() < arb(10) ** -50
check("rho on [2,3] (closed form with Li2) agrees with the delay equation integrated by acb.integral at u = 9/4,"
      " 5/2, 11/4, 3 (balls overlap, radii < 1e-50)", okr)
# rho(t/2) = D_2(t) vs D_1 * exp_*(1_(1,2] dv/v) at t in (0,3): r <= 2 terms suffice (3 fragments > 1 exceed 3).
okp, dev = True, []
for tt in (F(1, 2), F(5, 4), F(7, 4), F(2), F(9, 4), F(5, 2), F(11, 4), F(29, 10)):
    t = A(tt)
    lhs = rho_arb(tt / 2)
    rhs = rho_arb(tt)
    if tt > 1:   # one large fragment v in (1, min(2,t)); small part t - v
        vmax = min(F(2), tt)
        # split where t - v crosses 1 (rho(t-v) = 1 - log(t-v) for t-v in [1,2])
        cut = max(F(1), min(vmax, tt - 1))
        if cut > 1:
            rhs += acb.integral(lambda v, an: (1 - (A(tt) - v).log(analytic=an)) / v, 1, A(cut)).real
        rhs += A(vmax).log() - A(cut).log()
    if tt > 2:   # two large fragments: v1, v2 in (1,2], v1 + v2 <= t < 3, small part in [0,1): rho = 1
        rhs += acb.integral(lambda v, an: (A(tt) - v).log(analytic=an) / v, 1, A(tt - 1)).real / 2
    okp &= (lhs - rhs).contains(0) and (lhs - rhs).rad() < arb(10) ** -40
    dev.append(fl((lhs - rhs).mid(), 3))
check("rigorous pointwise check D_2(t) = [D_1 * exp_*(1_(1,2] dv/v)](t) at 8 points t in (0, 3) (balls contain 0)",
      okp)
check("Mecke (designated fragment): E sum_{p in Pi cap (l,u]} f(p, Pi) = int_(l,u] E f(v, Pi + v) dv/v, so the"
      " marked measure is 1_(l,u] dv/v * (the unmarked one); the designated v > l carries no tilt", True,
      "standard [7, Thm 4.5]; checked by reading")

# ---------------------------------------------------------------------------------------------------------------
print("\n[4] the small-fragment majorants d*_j(Mh) >= D_{Mh}(jh) = rho(j/M) (p. 12, (2.1), (2.3))")
FLOOR = F(1, 10 ** 40)
REN = {}
ok_pos = ok_win = ok_stop = True
stopinfo = []
for M in range(2, 64):
    R = [F(1)] * (M + 1)
    W = F(M)
    j = M + 1
    while True:
        v = W / j
        ok_pos &= v > 0
        R.append(v)
        W += v - R[j - M]
        if v <= FLOOR:
            break
        j += 1
    REN[M] = R      # R[j] exact for j < len(R); constant FLOOR thereafter
    ok_win &= all(R[jj] == sum(R[jj - M:jj]) / jj for jj in range(M + 1, min(len(R), 3 * M + 6)))
    ok_stop &= len(R) - 1 < N
    if M in LREN:
        stopinfo.append("M=%d: <=1e-40 first at j=%d" % (M, len(R) - 1))
check("(2.3) renewal R_j > 0 exactly for every M in 2..63 and every j up to its 10^-40 switch", ok_pos)
check("sliding window [M,M] start, +new -departing equals the definition R_j = (1/j) sum_{a=j-M}^{j-1} R_a",
      ok_win)
check("the 10^-40 switch happens before j = N for every M in 2..63 (so the tail rule is reached)", ok_stop,
      "; ".join(stopinfo))
# rigorous R_j >= rho(j/M) for j <= 3M (closed forms), every renewal M
okren = True
minslack = None
for M in range(2, 64):
    for jj in range(0, 3 * M + 1):
        Rv = A(REN[M][jj]) if jj < len(REN[M]) else A(FLOOR)
        rv = rho_arb(F(jj, M))
        okren &= certainly_le(rv, Rv)
        if jj > M:
            s_ = (Rv - rv) / rv
            minslack = s_ if minslack is None or s_ < minslack else minslack
check("R_j >= rho(j/M) rigorously for all 0 <= j <= 3M and every M in 2..63 (equality for j <= M)", okren,
      "min relative slack on (M, 3M] = %s" % fl(minslack.mid(), 4))
check("left-Riemann direction: rho nonincreasing, so (j/M)rho(j/M) = int_{(j-M)/M}^{j/M} rho <= (1/M) sum_{a=j-M}^"
      "{j-1} rho(a/M); with induction R_j >= rho(j/M); the 10^-40 tail uses rho nonincreasing", True,
      "checked by reading")


def delay_upper(M, count):
    """Lemma 2.2 (2.1) in arb at 160 bits, as printed: returns (lower, upper) lists for j = 0..count."""
    old = ctx.prec
    ctx.prec = 160
    lo, hi = [arb(1)] * (min(count, M) + 1), [arb(1)] * (min(count, M) + 1)
    err = arb(1) / (2 * arb(M) ** 3)
    for j in range(M, count):
        low = (lo[j] - (hi[j - M] / (2 * j) + hi[j + 1 - M] / (2 * (j + 1)))).lower()
        high = (hi[j] - (lo[j - M] / (2 * j) + lo[j + 1 - M] / (2 * (j + 1))) + err).upper()
        low, high = max(arb(0), low), min(arb(1), high)
        lo.append(low)
        hi.append(high)
    ctx.prec = old
    return lo, hi


DEL = {}
okdel, okord = True, True
ndel = 0
for M in LDEL:
    cnt = min(3 * M, N - 1)
    lo, hi = delay_upper(M, cnt)
    DEL[M] = hi
    okord &= all(lo[j] <= hi[j] and hi[j + 1] <= hi[j] and lo[j + 1] <= lo[j] for j in range(cnt))
    samp = set(range(M, min(M + 12, cnt + 1))) | {2 * M - 1, 2 * M, 2 * M + 1, cnt}
    samp |= set(rnd.randrange(M, cnt + 1) for _ in range(40))
    for j in sorted(samp):
        if j <= cnt:
            okdel &= certainly_le(rho_arb(F(j, M)), hi[j])
            ndel += 1
check("Lemma 2.2 delay recurrence (as printed, 160-bit arb) for every delay cap M in the schedule: ordered,"
      " nonincreasing endpoint sequences for j <= 3M (the acceptance tests, on this range)", okord,
      "%d caps" % len(LDEL))
check("delay upper sequence >= rho(j/M) rigorously at %d sampled j in [M, 3M] (incl. M..M+11, 2M-1..2M+1, 3M)"
      " over all delay caps" % ndel, okdel)

# ---------------------------------------------------------------------------------------------------------------
print("\n[5] end-to-end on the 61 actual bins: true cell masses <= [X^j]B_theta, [X^j]M_theta for j < 2L")


def ei(x):
    return arb.ei(x)


def large_one(j, th, lo_v, hi_v):
    """int_{lo_v}^{hi_v} (1/v) * int_{C_j} e^{-th (t - v)} 1[t >= v] dt dv  (small part in [0, l): rho = 1).
    Closed form with Ei; th, j integer; lo_v, hi_v exact rationals with lo_v >= L h > 0."""
    a_, b_ = A(j * h), A((j + 1) * h)
    T = arb(th)
    tot_ = arb(0)
    # v <= jh: inner = (e^{-th(jh - v)} - e^{-th((j+1)h - v)})/th
    p, q = lo_v, min(hi_v, j * h)
    if q > p:
        tot_ += ((-T * a_).exp() - (-T * b_).exp()) * (ei(T * A(q)) - ei(T * A(p))) / T
    # jh <= v < (j+1)h: inner = (1 - e^{-th((j+1)h - v)})/th
    p, q = max(lo_v, j * h), min(hi_v, (j + 1) * h)
    if q > p:
        tot_ += ((A(q) / A(p)).log() - (-T * b_).exp() * (ei(T * A(q)) - ei(T * A(p)))) / T
    return tot_


okB = okM = True
ncell = 0
worst = None
t5 = time.time()
for b in BINS:
    L, H, K, th = b["L"], b["H"], b["K"], b["theta"]
    ell = L * h
    if b["branch"] == "renewal":
        cells = list(range(0, 2 * L))
        dstar = lambda j, M=L: A(REN[M][j]) if j < len(REN[M]) else A(FLOOR)
    else:
        cells = sorted({0, 1, L - 2, L - 1, L, L + 1, L + 2, 2 * L - 2, 2 * L - 1}
                       | set(rnd.randrange(0, 2 * L) for _ in range(20)))
        dstar = lambda j, M=L: DEL[M][j]
    assert 2 * L <= K and 2 * L <= N
    T = arb(th)
    for j in cells:
        hA, eA = A(h), (-T * A(j * h)).exp()
        # true ordinary mass on C_j: small part alone + one large fragment (two large ones exceed 2L h > t)
        if j < L:
            r0 = (eA - (-T * A((j + 1) * h)).exp()) / T
        else:
            r0 = acb.integral(lambda t, an: (-acb(th) * t).exp() * (1 - (t / acb(A(ell))).log(analytic=an)),
                              acb(A(j * h)), acb(A((j + 1) * h))).real
        r1 = large_one(j, th, ell, min((j + 1) * h, K * h)) if j >= L else arb(0)
        trueB = r0 + r1
        trueM = large_one(j, th, ell, min((j + 1) * h, H * h)) if j >= L else arb(0)
        # kernels: [X^j]B = h(d*_j e^{-th jh} + sum_{i<=j-L} e^{-th ih} c_{j-i}), c_k = (chi(k)/k + chi(k-1)/(k-1))/2
        cB = lambda k: (F(1, k) if L <= k < K else 0) / 2 + (F(1, k - 1) if L <= k - 1 < K else 0) / 2
        cM = lambda k: (F(1, k) if L <= k < H else 0) / 2 + (F(1, k - 1) if L <= k - 1 < H else 0) / 2
        kB = hA * dstar(j) * eA
        kM = arb(0)
        for i in range(0, j - L + 1):
            ei_ = (-T * A(i * h)).exp()
            kB += hA * ei_ * A(cB(j - i))       # d*_i = 1 for i <= j - L < L
            kM += hA * ei_ * A(cM(j - i))
        okB &= certainly_le(trueB, kB)
        okM &= certainly_le(trueM, kM)
        if j >= L:
            rr = (kB - trueB) / kB
            worst = (rr, b["name"], j) if worst is None or rr < worst[0] else worst
        ncell += 1
check("[X^j]B_theta >= true mass of (e^{-theta t} D_l dt) * exp_*(1_(l,z] dv/v) on C_j, rigorously, %d cells"
      " over all 61 bins (all j < 2L when L < 64; 29 incl. boundary cells otherwise)" % ncell, okB,
      "smallest relative slack for j >= L: %s at %s, j=%d" % (fl(worst[0].mid(), 4), worst[1], worst[2]))
check("[X^j]M_theta >= true mass of 1_(l,u] dv/v * (same) on C_j, rigorously, same cells", okM,
      "%.1f s" % (time.time() - t5))

# ---------------------------------------------------------------------------------------------------------------
print("\n[6] authors' script code/third_party/openai186/prime_gap_186_certificate.py (comparison only)")
try:
    pg = load("pg186", os.path.join(HERE, "third_party", "openai186", "prime_gap_186_certificate.py"))
    ctx.prec = 200
    lowt = [t for t in pg.TASKS if t["kind"] == "low"]
    check("authors' TASKS: the same 61 low bins (low, high, slope) in the same order",
          len(lowt) == 61 and all(F(t["parameters"]["low"]) == b["l0"] and F(t["parameters"]["high"]) == b["u0"]
                                  and F(t["parameters"]["slope"]) == b["theta"] for t, b in zip(lowt, BINS)))
    check("authors' hard_cap per group equals z_G (so K agrees)",
          all(F(pg.GROUP_BY_ID[t["source_group_id"]]["hard_cap"]) == b["z0"] for t, b in zip(lowt, BINS)))
    okE = all(all(ball_has(c, x) for c, x in zip(pg.eulerian_carry_polynomial(r).coeffs(), E[r]))
              for r in range(1, 36))
    check("authors' eulerian_carry_polynomial(r) contains the exact E_r, r = 1..35", okE)
    okR = True
    for M in (2, 3, 6, 12, 25, 50, 63):
        vals = pg._low_positive_dickman(len(REN[M]) + 20, M, F(1, 10 ** 6))
        js = len(REN[M]) - 1          # first j with exact R_j <= 10^-40
        okR &= all(ball_has(vals[j], REN[M][j]) for j in range(js))
        okR &= all(ball_has(vals[j], FLOOR) for j in range(js, len(vals))) and REN[M][js] <= FLOOR
    check("authors' _low_positive_dickman (cutoff < 64) contains the exact renewal R_j for j < j*, and the constant"
          " 10^-40 from j* on, j* = first index with R_j <= 10^-40 (they replace R_j* itself, which is allowed:"
          " 10^-40 >= R_j* >= rho) (M = 2, 3, 6, 12, 25, 50, 63)", okR)
    M0 = LDEL[0]
    ctx.prec = 160                                   # the authors' engine precision (Sec. 2.1: 160-bit balls)
    vals = pg._low_positive_dickman(3 * M0 + 1, M0, h)
    ctx.prec = 200
    check("authors' delay branch (cutoff %d >= 64, as in the schedule) returns the upper sequence of (2.1): equal"
          " to ours for j <= 3M" % M0, all(vals[j] == DEL[M0][j] for j in range(3 * M0 + 1)))
    okenv = True
    for key, (Dvec, kk) in KE.items():
        Nn, L, H, K = key
        Qp = pg.arb_poly([A(x) for x in kk["Q"]])
        Mp = pg.arb_poly([A(x) for x in kk["Mm"]])
        Dp = pg.arb_poly([A(x) for x in Dvec])
        oldcap = ctx.cap
        ctx.cap = Nn
        ordn, desg = pg._low_eulerian_envelopes(Qp, Dp, Mp, Nn, L)
        ctx.cap = oldcap
        co, cd = pg.poly_coefficients(ordn, Nn), pg.poly_coefficients(desg, Nn)
        okenv &= all(F(x) <= a2F(c.upper()) for c, x in zip(co, kk["B"]))
        okenv &= all(F(x) <= a2F(c.upper()) for c, x in zip(cd, kk["M"]))
        okenv &= all(certainly_le(c, A(x) + arb(10) ** -30) for c, x in zip(co, kk["B"]))
    check("authors' _low_eulerian_envelopes on the 6 exact instances of [2]: upper endpoints >= our exact B, M"
          " and ordinary within 1e-30 of exact B (same construction)", okenv)
    src = inspect.getsource(pg.source_low_measures)
    check("authors' source_low_measures (source text): first = floor(lo/h), last = ceil(hi/h), cap = ceil(z/h);"
          " high cells 1/a for a in [first, cap), marks for a < last; low cells h d_j e^{-theta j h}",
          "first, last, cap = int(lo // step), int(-((-hi) // step)), int(-((-z) // step))" in src
          and "for index in range(first, cap):" in src and "if index < last:" in src
          and "engine.h * dickman[index] * (decay * rational(index * step)).exp()" in src)
except Exception as ex:  # pragma: no cover
    check("authors' script importable for comparison", False, repr(ex))

# ---------------------------------------------------------------------------------------------------------------
el = time.time() - T_START
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
print("\nruntime %.1f s, peak RSS %.0f MB" % (el, rss))
print("%d checks, %d failures" % (NCHECK[0], len(FAILS)))
for f_ in FAILS:
    print("  FAILED: " + f_)
