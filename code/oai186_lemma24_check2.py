#!/usr/bin/python3
"""Second, independent check of Lemma 2.4 (whole-bin Palm envelopes) of
OpenAI, "Numerical certificate for prime gaps at most 186" (30 Aug 2026),
code/third_party/openai186/short_gaps_numerics.pdf, p. 14, (2.9), with the
set-up of p. 10, (1.39)-(1.43).

For a largest-fragment bin (a,b], U/(m+1) <= a < b <= z0 < U, the arrays
    P_j = d^_j(b+),  A_j = 1[t+_j > a] d^_{s-_j}(r+),
    B_j = [d^_j(b+) - d_{j+1}(r-)]_+,  C_j = 1[t+_j > a + r+] [d^_{s-_j}(b+) - beta_j]_+
(weights w_j omitted: a common positive factor) bound the ordinary, largest-
fragment, distinct-secondary and same-coordinate roles; the largest-fragment
and coincident arrays are multiplied by lambda(t+_j) and
lambda(min{t+_j, (m t+_j - U)/(m-1)}), and Lambda = log(b/a) is charged once.

Written from the PDF only (no repository code or data). Decisions use exact
arithmetic (Fraction, sympy) or rigorous balls (python-flint arb).

  A  rebuild the 6 groups and the 30 rank-two bins of section 1.5.1 (T_1..T_6);
     hypotheses of Lemma 2.4 and of (1.39);
  B  exact symbolic identities: (1.41) dominates the integrand of (1.40)
     (nonnegative-coefficient certificate), the [xy] extraction of
     prod (P + xA + yB + xyC) reproduces the four roles of (1.41), (1.43) for
     d <= 40, the dq/q fractions and the same-coordinate feasibility;
  C  Dickman enclosures (2.1) for every cap used (b+, r+, r-), 160-bit directed
     dyadics, acceptance tests, and comparison with an independent rigorous
     Dickman rho (power series about k + 1/2 with an inductive tail bound);
  D  per-cell check on all 30 bins (strided cells plus every cell near an
     index threshold): the true role densities at corner and random exact
     points (t, q) in C_j x (a, b] lie below the arrays;
  E  end-to-end: rigorous upper bound of the true one-largest Palm integral
     (1.40) (with r(q) for d(q), the enlarged event) over q in (a,b] at random
     coordinate totals, d = 2, 3, 4 and the group dimension (39/40), compared
     with Lambda * [xy] prod_i (P + x lambda A + y B + xy lambda' C).
"""
import math
import random
import resource
import sys
import time
from fractions import Fraction as F

import flint
from flint import arb
import sympy as sp

T_START = time.time()
flint.ctx.prec = 256
NCHK = 0
NFAIL = 0


def check(cond, msg):
    global NCHK, NFAIL
    NCHK += 1
    if not cond:
        NFAIL += 1
        print("FAIL:", msg)
        sys.stdout.flush()


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -((-x.numerator) // x.denominator)


def A(x):
    x = F(x)
    return arb(x.numerator) / x.denominator


def le(x, y):
    """rigorous x <= y for arb balls"""
    return x.upper() <= y.lower()


# ------------------------------------------------- rigorous Dickman rho ---
class Rho:
    """rho on [0,1]: 1; [1,2]: 1 - log u; on [k,k+1], k >= 2: power series in
    x = u - (k+1/2), |x| <= 1/2, from u rho'(u) = -rho(u-1):
    c_{n+1} = -(c'_n + n c_n)/(c(n+1)), c = k + 1/2; tail |c_n| <= K (2/3)^n for
    n >= nmax by induction; c_0 from continuity at u = k."""

    def __init__(self, kmax, nmax=90):
        self.nmax = nmax
        r = arb(2) / 3
        tail = (arb(1) / 3) ** (nmax + 1) * arb(3) / 2
        c = [1 - (arb(3) / 2).log()] + [arb((-1) ** n) / (n * (arb(3) / 2) ** n)
                                         for n in range(1, nmax + 1)]
        self.ser = {1: (c, arb(1))}
        for k in range(2, kmax + 1):
            cp, Kp = self.ser[k - 1]
            cc = arb(k) + arb(1) / 2
            d = [arb(0)] * (nmax + 1)
            d[1] = -cp[0] / cc
            for n in range(1, nmax):
                d[n + 1] = -(cp[n] + n * d[n]) / (cc * (n + 1))
            K = arb(max((abs(d[nmax]) / r ** nmax).upper(),
                        (Kp / (cc * (nmax + 1) * (r - 1 / cc))).upper()))
            rk = sum(cp[n] * (arb(1) / 2) ** n for n in range(nmax + 1)) + arb(0, (Kp * tail).upper())
            d[0] = rk - sum(d[n] * (arb(-1) / 2) ** n for n in range(1, nmax + 1)) \
                + arb(0, (K * tail).upper())
            self.ser[k] = (d, K)
        self.kmax = kmax
        self.tail = tail
        self.cache = {}

    def __call__(self, u):
        u = F(u)
        v = self.cache.get(u)
        if v is not None:
            return v
        if u <= 1:
            v = arb(1)
        else:
            k = floor(u)
            ua = A(u)
            if k == 1 or u == 2:
                v = 1 - ua.log()
            else:
                d, K = self.ser[k]
                x = ua - k - arb(1) / 2
                s = arb(0)
                for n in range(self.nmax, -1, -1):
                    s = s * x + d[n]
                v = s + arb(0, (K * self.tail).upper())
        if len(self.cache) < 300000:
            self.cache[u] = v
        return v


RHO = Rho(40)


def D(c, t):
    """D_c(t) = rho(t/c) for t >= 0, 0 for t < 0"""
    if t < 0:
        return arb(0)
    return RHO(F(t) / c)


# ---------------------------------------------------------------- Part A ---
print("== Part A: data from the PDF formulas ==")
g0, eps_o, eps_n, tau = F(1, 10**7), F(1, 10**6), F(1, 10**7), F(1, 10**10)
sigma0 = F(100001, 10**6)
sigma_mt = F(1, 2) - F(40481, 100000) + tau
Om = {"o": F(12499, 10**6), "n": F(253, 20000)}
rho = F(1, 4) + Om["o"]
rho_s = rho - g0
S = F(2742997, 10**7) / rho_s
T1 = F(251, 1000) / rho_s
T0 = 2 - F(3, 1000) - S
e = g0 / rho
check(S == F(2742997, 2624989) and T0 == F(2499106033, 2624989000)
      and T1 == F(2510000, 2624989) and rho == F(262499, 10**6), "(1.1) constants")
N = 98304
h = S / N
n = N - 40
Tn = {"o": T0, "n": T1}
cs = {"o": {1: ((1 - 5 * sigma0) / 15, F(18, 5)), 2: ((1 - 4 * sigma0) / 16, F(7, 2)), 3: (F(3, 80), F(3))},
      "n": {1: ((1 - 5 * sigma_mt) / 15, F(18, 5)), 2: ((1 - 4 * sigma_mt) / 16, F(7, 2)),
            3: ((1 - 2 * sigma_mt) / 20, F(16, 5))}}
epsn = {"o": eps_o, "n": eps_n}
LAD = {}
for nu in "on":
    Enu = rho * (S + Tn[nu]) - F(1, 2)
    wp, rows, t = F(0), [], 0
    while True:
        rt = 1 if t < 12 else (2 if t < 24 else 3)
        c, s_ = cs[nu][rt]
        w = min(Om[nu], (c - epsn[nu] - Enu + 2 * wp - g0) / s_)
        dl = c - s_ * w - epsn[nu]
        rows.append(dict(r=rt, xi=dl / rho))
        wp = w
        t += 1
        if w == Om[nu]:
            break
    LAD[nu] = rows
check(len(LAD["o"]) == 29 and len(LAD["n"]) == 43, "ladders have 29 and 43 rows")
X = lambda nu, t: LAD[nu][t]
# name, d, m, xi, U, z/h, p/h, cap (1.18)
GR = [("O2", 40, F(2), X("o", 23)["xi"], S + e, 49152, 24576, (S + e) / 2),
      ("O5/2", 40, F(5, 2), X("n", 38)["xi"], S + e / 2, 46580, 19660, S + e / 2 - 23 * (T1 + e / 2) / 40),
      ("I2old", 39, F(2), X("o", 23)["xi"], T0 + e, 44781, 22390, (T0 + e) / 2),
      ("I5/2old", 39, F(5, 2), X("o", 27)["xi"], T0 + e / 2, 35265, 17912, 63 * (T0 + e / 2) / 160),
      ("I2new", 39, F(2), X("n", 23)["xi"], T1 + e, 44976, 22488, (T1 + e) / 2),
      ("I5/2new", 39, F(5, 2), X("n", 38)["xi"], T1 + e / 2, 35419, 17990, 63 * (T1 + e / 2) / 160)]
TL = [[F(j, 6) for j in range(7)],
      [F(j, 16) for j in range(9)] + [F(5, 8), F(3, 4), F(7, 8), F(1)],
      [F(0), F(1)],
      [F(0), F(1, 2), F(1)],
      [F(0), F(1, 6), F(1, 2), F(2, 3), F(1)],
      [F(0), F(1, 8), F(3, 8), F(1, 2), F(3, 4), F(1)]]
BINS = []
for gi, (nm, d, m, xi, U, zh, ph, cap) in enumerate(GR):
    check(floor(cap / h) == zh and floor(U / (2 * m * h)) == ph, f"{nm}: printed z/h, p/h")
    z = zh * h
    p = ph * h
    q0 = U / (m + 1)
    check(max(p, xi) <= q0, f"{nm}: max(p_G, xi_G) <= U/(m+1)  [(1.39)]")
    check(q0 < z, f"{nm}: U/(m+1) < z")
    tl = TL[gi]
    check(all(tl[i] < tl[i + 1] for i in range(len(tl) - 1)) and tl[0] == 0 and tl[-1] == 1,
          f"{nm}: T list strictly increasing from 0 to 1")
    for i in range(1, len(tl)):
        a = q0 + tl[i - 1] * (z - q0)
        b = q0 + tl[i] * (z - q0)
        BINS.append(dict(g=nm, gi=gi, idx=i, d=d, m=m, U=U, a=a, b=b, z0=z, p=p, xi=xi))
        check(m in (F(2), F(5, 2)), "m in {2, 5/2}")
        check(U / (m + 1) <= a < b <= z < U, f"{nm} bin {i}: U/(m+1) <= a < b <= z0 < U")
        check((U - a) / m <= a, f"{nm} bin {i}: r(q) <= q on (a,b] (r(q) decreasing, q increasing)")
check(len(BINS) == 30, "30 rank-two bins")
print(f"  6 groups, {len(BINS)} rank-two bins; hypotheses of Lemma 2.4 hold on all")

# ---------------------------------------------------------------- Part B ---
print("== Part B: exact symbolic identities ==")
for d in range(2, 7):
    Bs = sp.symbols(f"B1:{d + 1}", nonnegative=True)
    De = sp.symbols(f"del1:{d + 1}", nonnegative=True)
    As = [Bs[i] + De[i] for i in range(d)]
    for j in range(d):
        integrand = As[j] * sp.prod([As[i] for i in range(d) if i != j]) \
            - Bs[j] * sp.prod([Bs[i] for i in range(d) if i != j])
        bound = (As[j] - Bs[j]) * sp.prod([As[i] for i in range(d) if i != j]) \
            + Bs[j] * sum((As[i] - Bs[i]) * sp.prod([As[v] for v in range(d) if v not in (i, j)])
                          for i in range(d) if i != j)
        diff = sp.Poly(sp.expand(bound - integrand), *Bs, *De)
        check(all(cf >= 0 for cf in diff.coeffs()), f"(1.41) >= (1.40) integrand, d={d}, j={j}")
    # [xy] extraction with distinct symbols and the role substitution
    x, y = sp.symbols("x y")
    Ps = sp.symbols(f"P1:{d + 1}")
    Am = sp.symbols(f"Am1:{d + 1}")
    Bm = sp.symbols(f"Bm1:{d + 1}")
    Cm = sp.symbols(f"Cm1:{d + 1}")
    prod = sp.expand(sp.prod([Ps[i] + x * Am[i] + y * Bm[i] + x * y * Cm[i] for i in range(d)]))
    xy = sp.Poly(prod, x, y).coeff_monomial(x * y)
    roles = sum(Cm[j] * sp.prod([Ps[i] for i in range(d) if i != j]) for j in range(d)) \
        + sum(Am[j] * Bm[i] * sp.prod([Ps[v] for v in range(d) if v not in (i, j)])
              for j in range(d) for i in range(d) if i != j)
    check(sp.expand(xy - roles) == 0, f"[xy] prod(P+xA+yB+xyC) = four placements, d={d}")
    # role substitution reproduces sum_j (1.41): P_i -> A_i, A_j -> Bsh_j, B_i -> A_i - B_i,
    # C_j -> Ash_j - Bsh_j (shifted symbols for the largest-fragment coordinate)
    Ash = sp.symbols(f"Ash1:{d + 1}")
    Bsh = sp.symbols(f"Bsh1:{d + 1}")
    Au = sp.symbols(f"Au1:{d + 1}")
    Bu = sp.symbols(f"Bu1:{d + 1}")
    sub = {}
    for i in range(d):
        sub[Ps[i]] = Au[i]
        sub[Am[i]] = Bsh[i]
        sub[Bm[i]] = Au[i] - Bu[i]
        sub[Cm[i]] = Ash[i] - Bsh[i]
    tot141 = sum((Ash[j] - Bsh[j]) * sp.prod([Au[i] for i in range(d) if i != j])
                 + Bsh[j] * sum((Au[i] - Bu[i]) * sp.prod([Au[v] for v in range(d) if v not in (i, j)])
                                for i in range(d) if i != j) for j in range(d))
    check(sp.expand(roles.subs(sub, simultaneous=True) - tot141) == 0,
          f"role assignment P,A,B,C of (2.9) = sum_j (1.41), d={d}")
# (1.43) for identical coordinates, d = 1..40, in R[x,y]/(x^2,y^2)
Pp, Ap, Bp, Cp = sp.symbols("P A B C")
cur = (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0))  # (1, x, y, xy) parts
for d in range(1, 41):
    c0, cx, cy, cxy = cur
    cur = (sp.expand(c0 * Pp), sp.expand(c0 * Ap + cx * Pp), sp.expand(c0 * Bp + cy * Pp),
           sp.expand(c0 * Cp + cx * Bp + cy * Ap + cxy * Pp))
    rhs = d * Pp ** (d - 1) * Cp + d * (d - 1) * Pp ** max(d - 2, 0) * Ap * Bp if d >= 2 else Cp
    check(sp.expand(cur[3] - rhs) == 0, f"(1.43) d={d}")
# fractions: int_{(a,b]} 1[q < v] dq/q = Lambda * lambda(v)
aS, bS, vS, qS, tS, US, mS = sp.symbols("a b v q t U m", positive=True)
for case, vv in (("v<=a", aS / 2), ("a<v<b", (aS + bS) / 2), ("v>=b", 2 * bS)):
    lo, hi = aS, sp.Min(bS, sp.Max(aS, vv))
    sub = {aS: 3, bS: 5}
    integ = sp.integrate(1 / qS, (qS, lo.subs(sub), hi.subs(sub)))
    lam = sp.Min(1, sp.Max(0, sp.log(vv.subs(sub) / 3) / sp.log(sp.Rational(5, 3))))
    check(sp.simplify(integ - sp.log(sp.Rational(5, 3)) * lam) == 0, f"fraction identity, case {case}")
# same-coordinate feasibility: t > q + (U-q)/m  <=>  q < (m t - U)/(m-1)  (m > 1)
expr = sp.expand((tS - qS - (US - qS) / mS) * mS / (mS - 1))
check(sp.simplify(expr - ((mS * tS - US) / (mS - 1) - qS)) == 0, "same-coordinate condition is linear in q")
check(sp.simplify(sp.diff(qS + (US - qS) / mS, qS) - (1 - 1 / mS)) == 0, "q + r(q) increasing (m > 1)")
check(sp.simplify(((mS * tS - US) / (mS - 1)).subs(tS, aS + (US - aS) / mS) - aS) == 0,
      "(m t - U)/(m-1) = a exactly at t = a + r+")
print("  (1.41) certificate d<=6, roles d<=6, (1.43) d<=40, fractions and feasibility")

# ---------------------------------------------------------------- Part C ---
print("== Part C: Dickman enclosures (2.1) for every cap ==")
P160 = 160
ONE = 1 << P160


def delay(M, Nmax):
    lo = [ONE] * (M + 1)
    hi = [ONE] * (M + 1)
    M3 = 2 * M ** 3
    for j in range(M, Nmax):
        dd = 2 * j * (j + 1)
        num = lo[j] * dd - hi[j - M] * (j + 1) - hi[j + 1 - M] * j
        lo.append(max(0, num // dd))
        num = (hi[j] * dd - lo[j - M] * (j + 1) - lo[j + 1 - M] * j) * M3 + ONE * dd
        hi.append(min(ONE, -((-num) // (dd * M3))))
    bad = [j for j in range(Nmax) if not (0 <= lo[j] <= hi[j] <= ONE and lo[j + 1] <= lo[j]
                                          and hi[j + 1] <= hi[j])]
    return lo, hi, not bad


CAPS = {}
NCAP = 0
NRC = 0


def caps_for(M):
    global NRC
    if M not in CAPS:
        lo, hi, ok = delay(M, N)
        check(ok, f"delay M={M}: acceptance (ordered, in [0,1], both nonincreasing)")
        # enclosure of rho at a stride and at the first delay interval
        for j in list(range(0, N + 1, 499)) + [M, M + 1, 2 * M, 2 * M + 1, N]:
            if j > N:
                continue
            rv = RHO(F(j, M))
            check((lo[j] == 0 or le(arb(lo[j]) / ONE, rv)) and le(rv, arb(hi[j]) / ONE),
                  f"delay M={M}: d_j <= rho(j/M) <= d^_j at j={j}")
            NRC += 1
        CAPS[M] = (lo, hi)
        global NCAP
        NCAP += 1
    return CAPS[M]


def dlo(M, j):
    return arb(CAPS[M][0][j]) / ONE


def dhi(M, j):
    return arb(CAPS[M][1][j]) / ONE


# ------------------------------------------------------- Parts D and E ---
print("== Parts D/E: per-cell role checks and end-to-end Palm integrals ==")
rng = random.Random(186024)
NCELL = 0
NPT = 0
CTRL = {"A_r-": 0, "B_j": 0}
E2E = []


def arrays(bn, Mb, Mrp, Mrm, j):
    a, b, U, m = bn["a"], bn["b"], bn["U"], bn["m"]
    rp = (U - a) / m
    tp = (j + 1) * h
    sm = max(0, j - ceil(b / h))
    sp_ = max(0, j + 1 - floor(a / h))
    P = dhi(Mb, j)
    Aa = dhi(Mrp, sm) if tp > a else arb(0)
    Bv = dhi(Mb, j) - dlo(Mrm, j + 1)
    Bb = arb(max(Bv.upper(), 0))  # upward enclosure, clipped
    beta = dlo(Mrm, sp_) if j * h >= b else arb(0)
    if tp > a + rp:
        Cv = dhi(Mb, sm) - beta
        Cc = arb(max(Cv.upper(), 0))
    else:
        Cc = arb(0)
    Lam = (A(b) / A(a)).log()
    lam1 = lam(A(tp), a, Lam)
    vv = min(tp, (m * tp - U) / (m - 1))
    lam2 = lam(A(vv), a, Lam) if vv > 0 else arb(0)
    return dict(P=arb(P.upper()), A=arb(Aa.upper()), B=Bb, C=Cc, l1=lam1, l2=lam2, Lam=Lam)


def lam(v, a, Lam):
    """outward upper bound for lambda(v) = min{1, max{0, log(v/a)/Lambda}}"""
    if v.upper() <= 0:
        return arb(0)
    x = (v / A(a)).log() / Lam
    up = x.upper()
    return arb(min(max(up, 0), 1)) if up < 1 else arb(1)


def role_true(bn, t, q):
    U, m = bn["U"], bn["m"]
    rq = (U - q) / m
    P = D(q, t)
    Bt = D(q, t) - D(rq, t)
    if t >= q:
        Atr = D(rq, t - q)
        Ctr = D(q, t - q) - D(rq, t - q)
    else:
        Atr = arb(0)
        Ctr = arb(0)
    return P, Atr, Bt, Ctr


def palm_upper(bn, ts, npieces):
    """rigorous upper bound of int_(a,b] sum_j [Ash_j prod A_i - Bsh_j prod B_i] dq/q"""
    a, b, U, m = bn["a"], bn["b"], bn["U"], bn["m"]
    br = sorted(set([a, b] + [a + (b - a) * F(i, npieces) for i in range(1, npieces)]
                    + [t for t in ts if a < t < b]))
    tot = arb(0)
    lot = arb(0)
    dd = len(ts)
    for q1, q2 in zip(br[:-1], br[1:]):
        r1, r2 = (U - q1) / m, (U - q2) / m  # r(q) decreasing
        Ahi = [D(q2, t) for t in ts]
        Alo = [D(q1, t) for t in ts]
        Bhi = [D(r1, t) for t in ts]  # D_{r(q)}(t) decreasing in q: sup at q1
        Blo = [D(r2, t) for t in ts]
        up = arb(0)
        lo = arb(0)
        for j in range(dd):
            tj = ts[j]
            if q1 >= tj:  # whole piece beyond t_j: shifted factors vanish
                continue
            # piece inside (0, t_j]: shifted factors increasing in q
            Ash_hi, Ash_lo = D(q2, tj - q2), D(q1, tj - q1)
            Bsh_hi, Bsh_lo = D(r2, tj - q2), D(r1, tj - q1)
            pa_hi = Ash_hi
            pa_lo = Ash_lo
            pb_hi = Bsh_hi
            pb_lo = Bsh_lo
            for i in range(dd):
                if i != j:
                    pa_hi *= Ahi[i]
                    pa_lo *= Alo[i]
                    pb_hi *= Bhi[i]
                    pb_lo *= Blo[i]
            up += pa_hi - pb_lo
            lo += pa_lo - pb_hi
        w = (A(q2) / A(q1)).log()
        tot += arb(max(up.upper(), 0)) * w
        lot += arb(max(lo.lower(), 0)) * w
    return tot, lot


def palm_bound(bn, cells, ar):
    dd = len(cells)
    Pv = [ar[c]["P"] for c in cells]
    s = arb(0)
    for j in range(dd):
        pr = ar[cells[j]]["l2"] * ar[cells[j]]["C"]
        for i in range(dd):
            if i != j:
                pr *= Pv[i]
        s += pr
        for i in range(dd):
            if i == j:
                continue
            pr = ar[cells[j]]["l1"] * ar[cells[j]]["A"] * ar[cells[i]]["B"]
            for v in range(dd):
                if v not in (i, j):
                    pr *= Pv[v]
            s += pr
    return ar[cells[0]]["Lam"] * s


for bi, bn in enumerate(BINS):
    tb = time.time()
    a, b, U, m = bn["a"], bn["b"], bn["U"], bn["m"]
    rp, rm = (U - a) / m, (U - b) / m
    Mb, Mrp, Mrm = ceil(b / h), ceil(rp / h), floor(rm / h)
    check(Mrm >= 1 and Mb * h >= b and Mrp * h >= rp and Mrm * h <= rm,
          f"bin {bi}: upward caps b+, r+ and downward cap r- on the grid")
    check(ceil(b / h) * h >= b and floor(a / h) * h <= a,
          f"bin {bi}: s-_j h <= max(0, jh-b) and s+_j h >= (j+1)h - a for all j (ceil/floor)")
    CAPS.clear()
    for M in (Mb, Mrp, Mrm):
        caps_for(M)
    # cells: stride plus a window around every index threshold
    thr = [floor(a / h), ceil(b / h), floor((a + rp) / h), ceil((b + rm) / h), floor(rm / h),
           ceil(rp / h), floor(U / h) if U / h < n else n - 1, n - 1, 0]
    cells = set(range(0, n, 53))
    for t0 in thr:
        cells.update(j for j in range(t0 - 3, t0 + 4) if 0 <= j < n)
    cells = sorted(cells)
    ar = {}
    for j in cells:
        ar[j] = arrays(bn, Mb, Mrp, Mrm, j)
        arj = ar[j]
        tp = (j + 1) * h
        # indicator consistency with the fractions
        check((tp > a) == (arj["l1"].upper() > 0), f"bin {bi} j={j}: 1[t+ > a] iff lambda(t+) > 0")
        check((tp > a + rp) == (arj["l2"].upper() > 0), f"bin {bi} j={j}: 1[t+ > a+r+] iff lambda' > 0")
        check(arj["l2"].upper() <= arj["l1"].upper(), f"bin {bi} j={j}: lambda' <= lambda")
        pts = [(j * h, b), (j * h, a + (b - a) / 10**9), ((j + 1) * h - h / 10**9, b),
               ((j + 1) * h - h / 10**9, a + (b - a) / 10**9)]
        for _ in range(3):
            pts.append((j * h + h * F(rng.randint(0, 10**6 - 1), 10**6), a + (b - a) * F(rng.randint(1, 10**6), 10**6)))
        for (t, q) in pts:
            P, Atr, Bt, Ctr = role_true(bn, t, q)
            check(le(P, arj["P"]), f"bin {bi} j={j}: ordinary D_q(t) <= P")
            check(le(Atr, arj["A"]) or Atr.upper() <= 0, f"bin {bi} j={j}: largest D_r(q)(t-q) <= A")
            check(le(Bt, arj["B"]) or Bt.upper() <= 0, f"bin {bi} j={j}: secondary diff <= B")
            check(le(Ctr, arj["C"]) or Ctr.upper() <= 0, f"bin {bi} j={j}: same-coordinate diff <= C")
            if Ctr.lower() > 0:  # positive same-coordinate density => feasible => indicator set
                check(t - q > (U - q) / m and q < (m * (j + 1) * h - U) / (m - 1),
                      f"bin {bi} j={j}: positive C density only where same-coordinate feasible")
            NPT += 1
            # negative controls: A with the downward cap r- instead of r+, B with index j
            # instead of j+1 for the subtracted lower endpoint
            if t >= q:
                wrongA = dhi(Mrm, max(0, j - ceil(b / h)))
                if Atr.lower() > wrongA.upper():
                    CTRL["A_r-"] += 1
            wrongB = dhi(Mb, j) - dlo(Mrm, j)
            if Bt.lower() > wrongB.upper():
                CTRL["B_j"] += 1
        NCELL += 1
    # end-to-end Palm integrals
    gdim = bn["d"]
    jl = [j for j in cells if (j + 1) * h > a and j * h < U]
    for it in range(40):
        dd = [2, 3, 4][it % 3] if it < 36 else gdim
        cl = [rng.choice(jl)]
        for _ in range(dd - 1):
            if rng.random() < 0.5:
                cl.append(rng.choice(cells[: max(2, len(cells) // 3)]))
            else:
                cl.append(rng.choice(cells))
        if it >= 36:  # high-dimensional: most coordinates small
            cl = [cl[0], rng.choice(cells)] + [rng.choice(cells[:20]) for _ in range(dd - 2)]
        ts = [c * h + h * F(rng.randint(0, 10**4 - 1), 10**4) for c in cl]
        if any(t >= U for t in ts):
            continue
        for c in cl:
            if c not in ar:
                ar[c] = arrays(bn, Mb, Mrp, Mrm, c)
        up, lo = palm_upper(bn, ts, 100 if dd <= 4 else 16)
        bd = palm_bound(bn, cl, ar)
        check(le(up, bd) or up.upper() <= 0, f"bin {bi}: Palm integral <= Lambda [xy] prod, d={dd}, cells={cl}")
        check(lo.lower() <= up.upper(), f"bin {bi}: Palm lower <= upper")
        if up.upper() > 0:
            E2E.append((float(up.mid()) / float(bd.mid()) if float(bd.mid()) > 0 else float('inf'),
                        lo.lower() > 0, f"{bn['g']} bin {bn['idx']} d={dd} cells={cl[:4]}"))
    print(f"  {bn['g']:8s} bin {bn['idx']:<2d} a/h={float(a / h):9.1f} b/h={float(b / h):9.1f} "
          f"caps M(b+)={Mb} M(r+)={Mrp} M(r-)={Mrm}; {len(cells)} cells; {time.time() - tb:.1f} s")
    sys.stdout.flush()
    RHO.cache.clear()

CAPS.clear()
for kc, vc in CTRL.items():
    check(vc > 0, f"negative control {kc} detected")
print(f"  negative controls (wrong variants, must be violated): {CTRL}")
nz = sum(1 for r_, pos, _ in E2E if pos)
worst = max(E2E)
print(f"  per-cell: {NCELL} cells, {NPT} exact (t,q) points; end-to-end: {len(E2E)} configurations with "
      f"positive upper bound, {nz} with provably positive true Palm mass; "
      f"max true-upper/bound = {worst[0]:.4f} ({worst[2]})")
print(f"  Lemma 2.2 enclosures: {NCAP} caps computed to j = N, all accepted, rho enclosed at "
      f"{NRC} grid points")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
print(f"\nchecks: {NCHK}   failures: {NFAIL}   run time: {time.time() - T_START:.1f} s   peak RSS: {rss:.0f} MB")
print("VERDICT: Lemma 2.4 " + ("VERIFIED as stated (on all tested cells and configurations)" if NFAIL == 0
                              else "FAILED checks"))
