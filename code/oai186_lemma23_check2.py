#!/usr/bin/python3
"""Second, independent check of Lemma 2.3 (Eulerian cell kernels) of
OpenAI, "Numerical certificate for prime gaps at most 186" (30 Aug 2026),
code/third_party/openai186/short_gaps_numerics.pdf, pp. 12-13, (2.3)-(2.7).

    The coefficients of B_theta = D_theta That_0 and M_theta = D_theta M That_1
    majorize the physical-cell masses of
        (e^{-theta t} D_l(t) dt) * exp_*(1_(l,z](v) dv/v)            and
        1_(l,u](v) dv/v * (e^{-theta t} D_l(t) dt) * exp_*(1_(l,z](v) dv/v).

Written from the PDF only (no repository code or data). Decisions use exact
arithmetic (fractions.Fraction, sympy, flint fmpq_poly) or rigorous ball
arithmetic (python-flint arb); floats only for reporting.

Method (different from re-implementing the construction and trusting it):
  A  rebuild the 61 low bins (l0, u0, z0, theta) from (1.1)-(1.24) and section
     1.5.1; hypotheses 2 <= L < H <= K <= N, theta > 0, J, kernel branch;
  B  combinatorics, exactly: the Eulerian recurrence (2.5) against (i) the
     inclusion-exclusion formula of the proof and (ii) an independent exact
     piecewise-polynomial convolution of uniform densities (Irwin-Hall);
     0 <= E_r <= R_r; the closed form of T_e against an ODE-recurrence exp;
  C  the low-kernel majorants d*_j: renewal (2.3) in exact rationals and the
     delay recurrence (2.1) in exact 160-bit directed dyadics (with the
     acceptance tests), both compared with an independent rigorous Dickman
     rho (power series about k+1/2 with an inductive tail bound);
  D  end-to-end on toy grids: a rigorous upper (and lower) bound for the TRUE
     cell masses, computed on a k-times finer grid with the true rho, the true
     tilt and the true 1/v density, with all fragment counts and no
     truncation, must lie below the coefficients of B_theta and M_theta.
     Includes truncated J (remainder active) and, at theta = 0, the Poisson
     identity nu_z = nu_l * exp_*(1_(l,z] dv/v) as a sandwich test;
  E  the same end-to-end test with the REAL parameters (h, L, H, K, theta,
     J, d*) of all 61 low bins on a prefix of cells j < jmax (prefix
     coefficients of power-series products are exact), including the J = 32
     truncation for the smallest-L bins.
"""
import math
import random
import resource
import sys
import time
from fractions import Fraction as F

import flint
from flint import arb, arb_poly, fmpq, fmpq_poly
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
    """exact Fraction -> arb ball"""
    x = F(x)
    return arb(x.numerator) / x.denominator


# ------------------------------------------------- rigorous Dickman rho ---
class Rho:
    """rho on [0,1]: 1; [1,2]: 1 - log u; on [k,k+1], k >= 2: power series in
    x = u - (k+1/2), |x| <= 1/2, from u rho'(u) = -rho(u-1):
        c_{n+1} = -(c'_n + n c_n) / (c (n+1)),  c = k + 1/2,
    c' the coefficients of the previous interval (same x).  Tail: if
    |c'_n| <= K' r^n (n >= nmax), r = 2/3, then |c_n| <= K r^n (n >= nmax)
    with K = max(|c_nmax| r^-nmax, K'/(c (nmax+1)(r - 1/c))) by induction
    (needs r > 1/c, true for c >= 5/2).  c_0 from continuity at u = k."""

    def __init__(self, kmax, nmax=110):
        self.nmax = nmax
        r = arb(2) / 3
        tail = (arb(1) / 3) ** (nmax + 1) * arb(3) / 2  # sum_{n>nmax} (1/3)^n
        c = [1 - (arb(3) / 2).log()] + [arb((-1) ** n) / (n * (arb(3) / 2) ** n)
                                         for n in range(1, nmax + 1)]
        self.ser = {1: (c, arb(1))}  # |c_n| <= (2/3)^n for n >= 1
        for k in range(2, kmax + 1):
            cp, Kp = self.ser[k - 1]
            cc = arb(k) + arb(1) / 2
            d = [arb(0)] * (nmax + 1)
            d[1] = -cp[0] / cc
            for n in range(1, nmax):
                d[n + 1] = -(cp[n] + n * d[n]) / (cc * (n + 1))
            K1 = abs(d[nmax]) / r ** nmax
            K2 = Kp / (cc * (nmax + 1) * (r - 1 / cc))
            K = arb(max(K1.upper(), K2.upper()))
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
                if k > self.kmax:
                    raise ValueError("rho: kmax too small")
                d, K = self.ser[k]
                x = ua - k - arb(1) / 2
                s = arb(0)
                for n in range(self.nmax, -1, -1):
                    s = s * x + d[n]
                v = s + arb(0, (K * self.tail).upper())
        if len(self.cache) < 400000:
            self.cache[u] = v
        return v


RHO = Rho(60)

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
        B = (F(1, 2) + 2 * wp) / rho
        rows.append(dict(r=rt, xi=dl / rho, a=B - Tn[nu], b=B - S))
        wp = w
        t += 1
        if w == Om[nu]:
            break
    LAD[nu] = rows
check(len(LAD["o"]) == 29 and len(LAD["n"]) == 43, "ladders have 29 and 43 rows")
X = lambda nu, t: LAD[nu][t]
# (1.23)-(1.24): name, m, xi, U, z/h (printed), p/h (printed), cap of (1.18)
GR = [("O2", F(2), X("o", 23)["xi"], S + e, 49152, 24576, (S + e) / 2),
      ("O5/2", F(5, 2), X("n", 38)["xi"], S + e / 2, 46580, 19660, S + e / 2 - 23 * (T1 + e / 2) / 40),
      ("I2old", F(2), X("o", 23)["xi"], T0 + e, 44781, 22390, (T0 + e) / 2),
      ("I5/2old", F(5, 2), X("o", 27)["xi"], T0 + e / 2, 35265, 17912, 63 * (T0 + e / 2) / 160),
      ("I2new", F(2), X("n", 23)["xi"], T1 + e, 44976, 22488, (T1 + e) / 2),
      ("I5/2new", F(5, 2), X("n", 38)["xi"], T1 + e / 2, 35419, 17990, 63 * (T1 + e / 2) / 160)]
for (nm, m, xi, U, zh, ph, cap) in GR:
    check(floor(cap / h) == zh, f"{nm}: z/h = floor(cap/h)")
    check(floor(U / (2 * m * h)) == ph, f"{nm}: p/h = floor(U/(2mh))")
    check(2 * h < xi < ph * h <= zh * h, f"{nm}: 2h < xi < p <= z")
aa = [F(6, 5) ** j / 20 for j in range(10)]


def ulist(gi, xi, p):
    return [[xi, 3 * xi / 2, aa[0]] + aa[4:9] + [(aa[8] + aa[9]) / 2, aa[9], p],
            [2 ** j * xi for j in range(9)] + [F(1, 100), F(3, 200), F(9, 400), F(27, 800)]
            + aa[0:8] + [(aa[7] + p) / 2, p],
            [xi, aa[0], aa[4], aa[6], aa[8], p],
            [xi, 2 * xi, F(1, 100), F(27, 800), aa[3], aa[5], aa[6], p],
            [xi, aa[1], aa[4], aa[5], aa[7], aa[8], p],
            [2 ** j * xi for j in (0, 1, 4, 6, 8)] + [F(9, 400), aa[1], aa[3], aa[5], aa[6], aa[7], p]][gi]


BINS = []
for gi, (nm, m, xi, U, zh, ph, cap) in enumerate(GR):
    ul = ulist(gi, xi, ph * h)
    check(all(ul[i] < ul[i + 1] for i in range(len(ul) - 1)), f"{nm}: list increasing")
    for jj in range(1, len(ul)):
        l0, u0 = ul[jj - 1], ul[jj]
        th = F(120) if (gi == 0 and jj == 3) else F(ceil((9 if gi == 5 else 7) / u0))
        z0 = zh * h
        L, H, K = floor(l0 / h), ceil(u0 / h), ceil(z0 / h)
        Jv = min(32, (N - 1) // L)
        BINS.append(dict(g=nm, idx=jj, l0=l0, u0=u0, z0=z0, th=th, L=L, H=H, K=K, J=Jv))
        check(2 <= L < H <= K <= N, f"{nm} L{jj}: 2 <= L < H <= K <= N")
        check(th > 0, f"{nm} L{jj}: theta > 0")
        check(L * h <= l0 and H * h >= u0 and K * h >= z0, f"{nm} L{jj}: rounded bin contains (l0,u0], z >= z0")
check(len(BINS) == 61, "61 low bins")
nJtr = sum(1 for b in BINS if b["J"] < (N - 1) // b["L"])
print(f"  61 low bins; L range {min(b['L'] for b in BINS)}..{max(b['L'] for b in BINS)}; "
      f"theta range {min(b['th'] for b in BINS)}..{max(b['th'] for b in BINS)}; "
      f"J=32 with truncation active in {nJtr} bins")
print(f"  M = L >= 64 (delay branch eligible) in {sum(1 for b in BINS if b['L'] >= 64)} bins, "
      f"renewal forced (L < 64) in {sum(1 for b in BINS if b['L'] < 64)}")

# ---------------------------------------------------------------- Part B ---
print("== Part B: exact combinatorics ==")
RMAX = 70
EU = {1: [1]}
for r in range(2, RMAX + 1):
    p = EU[r - 1]
    EU[r] = [(a + 1) * (p[a] if a < len(p) else 0) + (r - a) * (p[a - 1] if 0 <= a - 1 < len(p) else 0)
             for a in range(r)]
EF = {r: [F(EU[r][a], math.factorial(r)) for a in range(r)] for r in EU}
for r in range(1, RMAX + 1):
    for a in range(r):
        ie = sum((-1) ** b * math.comb(r + 1, b) * (a + 1 - b) ** r for b in range(a + 2))
        check(F(ie, math.factorial(r)) == EF[r][a], f"inclusion-exclusion E_{r}[{a}]")
    check(sum(EF[r]) == 1, f"E_{r}(1) = 1")
    check(all(0 <= c <= 1 for c in EF[r]), f"0 <= E_{r} <= R_{r} coefficientwise")
# independent: exact piecewise convolution of uniform densities on [0,1)
xs = sp.symbols("x")
ss = sp.symbols("s")
pieces = {0: sp.Integer(1)}  # density of U_1 on [k,k+1)
for r in range(1, 13):
    masses = {k: sp.integrate(pieces[k], (xs, k, k + 1)) for k in pieces}
    for a in range(r):
        check(sp.Rational(EF[r][a].numerator, EF[r][a].denominator) == masses.get(a, 0),
              f"Irwin-Hall cell mass r={r} a={a}")
    new = {}
    for k in range(r + 1):  # f_{r+1}(x) = int_{x-1}^{x} f_r(s) ds on [k,k+1)
        val = sp.Integer(0)
        if k - 1 in pieces:
            val += sp.integrate(sp.sympify(pieces[k - 1]).subs(xs, ss), (ss, xs - 1, k))
        if k in pieces:
            val += sp.integrate(sp.sympify(pieces[k]).subs(xs, ss), (ss, k, xs))
        new[k] = sp.expand(val)
    pieces = new
print("  Eulerian E_r = carry law for r <= 70 (incl.-excl.), r <= 12 (exact convolution)")


def Epoly(r):
    return fmpq_poly([fmpq(c.numerator, c.denominator) for c in EF[r]])


def Rpoly(r):
    return fmpq_poly([1] * r)


def exp_ode(Qc, Nt):
    """exp(Q) mod X^Nt for Q(0) = 0 via e_n = (1/n) sum_k k Q_k e_{n-k} (exact)."""
    ev = [F(1)] + [F(0)] * (Nt - 1)
    nz = [(kk, F(kk) * Qc[kk]) for kk in range(1, min(Nt, len(Qc))) if Qc[kk] != 0]
    for nn in range(1, Nt):
        s = F(0)
        for kk, kq in nz:
            if kk > nn:
                break
            s += kq * ev[nn - kk]
        ev[nn] = s / nn
    return ev


def fq(p, Nt):
    c = [F(int(x.p), int(x.q)) for x in p.coeffs()]
    return c + [F(0)] * (Nt - len(c))


# T_e closed form, exactly, on random toy Q of the form (2.4)
rng = random.Random(186023)
for it in range(12):
    L_ = rng.randint(2, 6)
    K_ = rng.randint(L_ + 1, 30)
    Nt = rng.randint(K_, 45)
    Qc = [F(0)] * Nt
    for a in range(L_, min(K_, Nt)):
        Qc[a] = F(1, a)
    Qp = fmpq_poly([fmpq(c.numerator, c.denominator) for c in Qc])
    ex = exp_ode(Qc, Nt)
    exq = [F(0)] * Nt  # exp(XQ): coefficient of X^n is sum_r [X^{n-r}] Q^r/r! ; use ODE on XQ
    XQc = [F(0)] + Qc[:Nt - 1]
    exq = exp_ode(XQc, Nt)
    for ee in (0, 1):
        num = [ex[i] - (exq[i - ee - 1] if i - ee - 1 >= 0 else 0) for i in range(Nt)]
        closed = [sum(num[:i + 1]) for i in range(Nt)]  # divide by 1 - X
        direct = fmpq_poly([0])
        qr, r = fmpq_poly([1]), 0
        while not qr.is_zero():
            direct += qr.mul_low(Rpoly(r + ee + 1), Nt)
            r += 1
            qr = qr.mul_low(Qp, Nt) / r
        check(fq(direct, Nt) == closed, f"T_{ee} closed form toy {it}")
print("  T_e = (exp Q - X^{e+1} exp(XQ))/(1-X) mod X^N on 12 random toy Q (24 identities)")

# ---------------------------------------------------------------- Part C ---
print("== Part C: low-kernel majorants d*_j vs rigorous rho ==")
P160 = 160
ONE = 1 << P160


def delay(M, Nmax):
    """(2.1) with c = Mh; 160-bit dyadics, one directed rounding per step.
    Returns (lo, hi) integer lists (value * 2^160), j = 0..Nmax, and acceptance."""
    lo = [ONE] * (M + 1)
    hi = [ONE] * (M + 1)
    M3 = 2 * M ** 3
    for j in range(M, Nmax):
        d = 2 * j * (j + 1)
        num = lo[j] * d - hi[j - M] * (j + 1) - hi[j + 1 - M] * j
        lo.append(max(0, num // d))
        num = (hi[j] * d - lo[j - M] * (j + 1) - lo[j + 1 - M] * j) * M3 + ONE * d
        hi.append(min(ONE, -((-num) // (d * M3))))
    bad = [j for j in range(Nmax) if not (0 <= lo[j] <= hi[j] <= ONE and lo[j + 1] <= lo[j]
                                          and hi[j + 1] <= hi[j])]
    ok = not bad and 0 <= lo[Nmax] <= hi[Nmax] <= ONE
    return lo, hi, (ok, bad[0] if bad else None)


FLOOR40 = F(1, 10**40)


def renewal(M, Nmax):
    """(2.3), exact rationals, with the optional 10^-40 floor; returns list."""
    R = [F(1)] * (M + 1)
    s = F(M)  # sum_{a=j-M}^{j-1} R_a for j = M+1
    floored = False
    for j in range(M + 1, Nmax + 1):
        if floored:
            R.append(FLOOR40)
            continue
        v = s / j
        check(v > 0, "renewal positive")
        R.append(v)
        s += v - R[j - M]
        if v <= FLOOR40:
            floored = True
    return R


def lower_ok(lo_val, rv):
    return lo_val == 0 or (arb(lo_val) / ONE) <= rv.lower()


# validate the rho series: closed form on [2,3] (dilogarithm), continuity at
# integers, and the integral equation u rho(u) = int_{u-1}^{u} rho (Simpson-free:
# monotone Riemann sandwich with 2000 nodes)
for u in [F(2) + F(i, 37) for i in range(1, 37)] + [F(5, 2), F(3)]:
    ua = A(u)
    cf = 1 - (1 - (ua - 1).log()) * ua.log() + (1 - ua).polylog(2) + arb.pi() ** 2 / 12
    check(RHO(u).overlaps(cf), f"rho series = closed form on [2,3] at u={u}")
for kk in range(3, 60):
    d, K = RHO.ser[kk - 1]
    left = sum(d[nn] * (arb(1) / 2) ** nn for nn in range(RHO.nmax + 1))
    check(left.overlaps(RHO(F(kk))), f"rho continuity at {kk}")
for u in (F(5, 2), F(7, 2), F(9, 2), F(13, 2), F(21, 2)):
    nn = 2000
    lo_s = sum((RHO(u - 1 + F(i + 1, nn)) for i in range(nn)), arb(0)) / nn
    hi_s = sum((RHO(u - 1 + F(i, nn)) for i in range(nn)), arb(0)) / nn
    check(lo_s.lower() <= (A(u) * RHO(u)).upper() and (A(u) * RHO(u)).lower() <= hi_s.upper(),
          f"rho integral equation sandwich at u={u}")
check(abs(float(RHO(F(3)).mid()) - 0.0486083882911316) < 1e-15
      and abs(float(RHO(F(10)).mid()) / 2.77017183772596e-11 - 1) < 1e-12, "rho(3), rho(10) literature values")
print("  rho series validated: closed form on [2,3], continuity at 3..59, integral equation, rho(3), rho(10)")

nrho = 0
for M in (2, 3, 5, 9, 17, 40):
    R = renewal(M, 30 * M)
    for j in range(0, 30 * M + 1):
        check(RHO(F(j, M)).upper() <= A(R[j]).lower() or (j <= M and R[j] == 1),
              f"renewal M={M} j={j}: R_j >= rho(j/M)")
        nrho += 1
for M in (64, 100, 1000):
    Nmax = min(40 * M, N)
    lo, hi, (ok, jb) = delay(M, Nmax)
    print(f"  delay M={M} on j <= {Nmax}: acceptance {'passes' if ok else 'fails'}"
          + ("" if ok else f" (upper endpoint first increases at j={jb}, u={jb / M:.2f})"))
    for j in list(range(0, Nmax + 1, max(1, Nmax // 3000))) + [Nmax]:
        rv = RHO(F(j, M))
        check(lower_ok(lo[j], rv), f"delay M={M} lower j={j}")
        check(rv.upper() <= arb(hi[j]) / ONE, f"delay M={M} upper j={j}")
        nrho += 2
print(f"  renewal and delay majorants enclose rho at {nrho} grid points (rho to 1e-40 accuracy)")


# ----------------------------------------------------------- the kernels ---
def to_arb_poly(fp, Nt):
    c = fp.coeffs()
    return arb_poly([arb(int(x.p)) / int(x.q) for x in c[:Nt]])


def construct(hv, L, H, K, Nt, th, dstar, J, exact=True, ctrl=None):
    """B_theta, M_theta mod X^Nt per (2.4)-(2.7). dstar: list of arb (I_j).
    exact=True: Q, q_r, T_e exact rationals (T_e via the ODE exp, independent of
    the q_r sum); otherwise arb polynomials (then Q^r = 0 for r > J is asserted)."""
    info = {}
    Kc, Hc = min(K, Nt), min(H, Nt)
    if exact:
        Qp = fmpq_poly([0] * L + [fmpq(1, a) for a in range(L, Kc)]) if Kc > L else fmpq_poly([0])
        Mp = fmpq_poly([0] * L + [fmpq(1, a) for a in range(L, Hc)]) if Hc > L else fmpq_poly([0])
        qs = [fmpq_poly([1])]
        while True:
            nxt = qs[-1].mul_low(Qp, Nt) / len(qs)
            if nxt.is_zero():
                break
            qs.append(nxt)
        expQ = fmpq_poly([0])
        expXQ = fmpq_poly([0])
        for r, qr in enumerate(qs):
            expQ += qr
            expXQ += qr.left_shift(r)
        ones = fmpq_poly([1] * Nt)
        That = {}
        for ee in (0, 1):
            Tp = (expQ - expXQ.left_shift(ee + 1)).mul_low(ones, Nt)
            Te = fq(Tp, Nt)
            dsum = fmpq_poly([0])
            for r, qr in enumerate(qs):
                dsum += qr.mul_low(Rpoly(r + ee + 1), Nt)
            check(fq(dsum, Nt) == Te, "T_e closed form equals sum_r q_r R_{r+e+1}")
            pre = fmpq_poly([0])
            preE = fmpq_poly([0])
            for r in range(0, min(J, len(qs) - 1) + 1):
                pre += qs[r].mul_low(Rpoly(r + ee + 1), Nt)
                if ctrl == 'dropr1' and r == 1:
                    continue
                preE += qs[r].mul_low(Epoly(max(1, r + ee) if ctrl == 'carry' else r + ee + 1), Nt)
            omit = [Te[i] - c for i, c in enumerate(fq(pre, Nt))]
            omE = fmpq_poly([0])
            for r in range(J + 1, len(qs)):
                omE += qs[r].mul_low(Epoly(r + ee + 1), Nt)
            omEc = fq(omE, Nt)
            check(all(x >= 0 for x in omit), "omitted sum nonnegative (no negative upper endpoint)")
            check(all(omit[i] >= omEc[i] for i in range(Nt)), "replicated remainder >= omitted Eulerian terms")
            info[f"omit{ee}"] = sum(1 for x in omit if x > 0)
            That[ee] = to_arb_poly(preE, Nt) + (arb_poly([0]) if ctrl == 'norem' else arb_poly([A(x) for x in omit]))
        Mpa = to_arb_poly(Mp, Nt)
        info["rmax"] = len(qs) - 1
    else:
        Qa = arb_poly([arb(0)] * L + [arb(1) / a for a in range(L, Kc)])
        Mpa = arb_poly([arb(0)] * L + [arb(1) / a for a in range(L, Hc)])
        qs = [arb_poly([1])]
        while (len(qs)) * L < Nt:
            qs.append((qs[-1] * Qa).truncate(Nt) * (arb(1) / len(qs)))
        check(len(qs) - 1 <= J, "arb branch: no truncation inside the prefix (r_max <= J)")
        That = {}
        for ee in (0, 1):
            acc = arb_poly([0])
            for r in range(len(qs)):
                acc += (qs[r] * arb_poly([A(c) for c in EF[r + ee + 1]])).truncate(Nt)
            That[ee] = acc
        info["rmax"] = len(qs) - 1
    eth = (-A(th) * A(hv)).exp()
    Dc, pw = [], (eth if ctrl == 'tiltinf' else arb(1))
    for j in range(Nt):
        Dc.append(A(hv) * dstar[j] * pw)
        pw *= eth
    Dth = arb_poly(Dc)
    Bt = (Dth * That[0]).truncate(Nt)
    Mt = ((Dth * Mpa).truncate(Nt) * That[1]).truncate(Nt)
    return Bt, Mt, info


def true_masses(hv, L, H, K, Nt, th, k, lower=False):
    """Rigorous upper (lower=False) or lower bound for the true coarse-cell
    masses j < Nt of both measures, from k-fold finer step densities: sup (inf)
    of e^{-theta t} rho(t/l), of 1/v, exact Irwin-Hall carries, all r."""
    Lf = Nt * k
    hf = A(hv) / k
    sh = 1 if lower else 0
    eth = (-A(th) * hf).exp()
    Dv, pw = [], (eth ** sh)
    for i in range(Lf):
        Dv.append(hf * RHO(F(i + sh, k * L)) * pw)
        pw *= eth
    Df = arb_poly(Dv)
    hiQ = min(K * k, Lf)
    Qf = arb_poly([arb(0)] * (L * k) + [arb(1) / (i + sh) for i in range(L * k, hiQ)])
    Mf = arb_poly([arb(0)] * (L * k) + [arb(1) / (i + sh) for i in range(L * k, min(H * k, Lf))])
    totB = arb_poly([0])
    totM = arb_poly([0])
    P = Df
    PM = (Df * Mf).truncate(Lf)
    r = 0
    while r * L * k < Lf:
        totB += (P * arb_poly([A(c) for c in EF[r + 1]])).truncate(Lf)
        totM += (PM * arb_poly([A(c) for c in EF[r + 2]])).truncate(Lf)
        r += 1
        P = (P * Qf).truncate(Lf) * (arb(1) / r)
        PM = (PM * Qf).truncate(Lf) * (arb(1) / r)
    cB, cM = totB.coeffs(), totM.coeffs()
    cB += [arb(0)] * (Lf - len(cB))
    cM += [arb(0)] * (Lf - len(cM))
    outB = [sum(cB[j * k:(j + 1) * k], arb(0)) for j in range(Nt)]
    outM = [sum(cM[j * k:(j + 1) * k], arb(0)) for j in range(Nt)]
    return outB, outM


def compare(label, Bt, Mt, uB, uM, lB, lM, Nt):
    cB, cM = Bt.coeffs(), Mt.coeffs()
    cB += [arb(0)] * (Nt - len(cB))
    cM += [arb(0)] * (Nt - len(cM))
    worst = 0.0
    nz = 0
    for j in range(Nt):
        for (bb, uu, ll, nmn) in ((cB[j], uB[j], lB[j], "B"), (cM[j], uM[j], lM[j], "M")):
            ok = uu.upper() <= bb.lower() or uu.upper() <= 0
            check(ok, f"{label}: true {nmn}-mass upper <= coefficient at j={j} "
                      f"({float(uu.mid()):.6g} vs {float(bb.mid()):.6g})")
            check(ll.lower() <= uu.upper(), f"{label}: lower <= upper at j={j}")
            if float(bb.mid()) > 0 and float(uu.mid()) > 0:
                worst = max(worst, float(uu.mid()) / float(bb.mid()))
                nz += 1
    return worst, nz


# ---------------------------------------------------------------- Part D ---
print("== Part D: toy end-to-end (true masses on a finer grid) ==")
TOYS = [  # (h, L, H, K, N, theta, k, Jtest or None)
    (F(1), 5, 7, 12, 15, F(3, 10), 8, None),
    (F(1), 5, 7, 12, 15, F(3, 10), 8, 0),
    (F(1), 5, 7, 12, 15, F(3, 10), 8, 1),
    (F(1, 7), 4, 6, 11, 12, F(7), 8, None),
    (F(1, 7), 4, 9, 11, 12, F(7), 8, 0),
    (F(3, 10), 2, 3, 6, 6, F(1, 100), 16, None),
    (F(1, 3), 3, 5, 8, 9, F(9), 8, None),
    (F(1, 3), 3, 5, 8, 9, F(9), 8, 0),
    (F(1, 1000), 6, 10, 17, 18, F(2000), 6, None),
    (F(2, 1), 2, 4, 9, 30, F(1, 5), 4, None),
    (F(2, 1), 2, 4, 9, 30, F(1, 5), 4, 3),
    (F(1, 10), 2, 3, 70, 70, F(5), 4, None),     # J = 32 < floor(69/2) = 34: real truncation
    (F(1, 10), 2, 9, 40, 70, F(1, 2), 4, None),  # truncation, wide designated window
    (F(1, 64), 64, 80, 130, 160, F(3), 2, None),  # delay branch M = L = 64
]
for ti, (hv, L, H, K, Nt, th, k, Jt) in enumerate(TOYS):
    J = min(32, (Nt - 1) // L) if Jt is None else Jt
    if L >= 64:
        lo, hi, (ok, jb) = delay(L, Nt)
        check(ok, f"toy {ti}: delay acceptance")
        dstar = [arb(hi[j]) / ONE for j in range(Nt)]
        br = "delay"
    else:
        Rr = renewal(L, Nt)
        dstar = [A(Rr[j]) for j in range(Nt)]
        br = "renewal"
    Bt, Mt, info = construct(hv, L, H, K, Nt, th, dstar, J)
    uB, uM = true_masses(hv, L, H, K, Nt, th, k)
    lB, lM = true_masses(hv, L, H, K, Nt, th, k, lower=True)
    worst, nz = compare(f"toy {ti}", Bt, Mt, uB, uM, lB, lM, Nt)
    print(f"  toy {ti}: h={hv} L={L} H={H} K={K} N={Nt} theta={th} k={k} J={J} ({br}); "
          f"r_max={info['rmax']}, remainder cells {info['omit0']}/{info['omit1']}; "
          f"max true/coef = {worst:.4f}")


def violations(Bt, Mt, lB, lM, Nt):
    cB, cM = Bt.coeffs(), Mt.coeffs()
    cB += [arb(0)] * (Nt - len(cB))
    cM += [arb(0)] * (Nt - len(cM))
    return sum(1 for j in range(Nt) for (bb, ll) in ((cB[j], lB[j]), (cM[j], lM[j]))
               if ll.lower() > bb.upper())


# negative controls (must be detected): drop the replicated remainder when J is
# truncated, drop the one-fragment term, or tilt by the cell infimum
# e^{-theta (j+1) h}; and (informational) one carry too few, E_{r+e} for E_{r+e+1}
CTRLS = {1: ("norem", "carry"), 4: ("norem", "carry"), 10: ("norem", "carry"), 0: ("dropr1", "tiltinf"),
         3: ("dropr1", "tiltinf"), 6: ("dropr1", "tiltinf"), 9: ("dropr1", "tiltinf")}
for ti, ctrls in CTRLS.items():
    hv, L, H, K, Nt, th, k, Jt = TOYS[ti]
    J = min(32, (Nt - 1) // L) if Jt is None else Jt
    Rr = renewal(L, Nt)
    dstar = [A(Rr[j]) for j in range(Nt)]
    lB, lM = true_masses(hv, L, H, K, Nt, th, k, lower=True)
    for ctrl in ctrls:
        Bt, Mt, _ = construct(hv, L, H, K, Nt, th, dstar, J, ctrl=ctrl)
        nv = violations(Bt, Mt, lB, lM, Nt)
        if ctrl != "carry":  # one carry too few is absorbed by the sup-density slack (informational)
            check(nv > 0, f"negative control {ctrl} on toy {ti} detected")
        print(f"  negative control '{ctrl}' on toy {ti}: true mass provably exceeds the wrong kernel in {nv} cells"
              + (" (informational)" if ctrl == "carry" else ""))
# Poisson identity at theta = 0: D_l * exp_*(1_(l,z] dv/v) = D_z on total sizes
for (hv, L, K, Nt, k) in ((F(1), 4, 9, 12, 16), (F(1, 5), 3, 8, 10, 32), (F(1), 2, 6, 6, 32)):
    uB, _ = true_masses(hv, L, K, K, Nt, F(0), k)
    lB, _ = true_masses(hv, L, K, K, Nt, F(0), k, lower=True)
    wmax = 0.0
    for j in range(Nt):
        sub = 64
        lo_i = sum((A(hv) / sub * RHO(F(j * sub + s + 1, sub * K)) for s in range(sub)), arb(0))
        hi_i = sum((A(hv) / sub * RHO(F(j * sub + s, sub * K)) for s in range(sub)), arb(0))
        check(lB[j].lower() <= hi_i.upper() and lo_i.lower() <= uB[j].upper(),
              f"Poisson identity sandwich L={L} K={K} j={j}")
        wmax = max(wmax, float((uB[j] - lB[j]).mid()) / float(hi_i.mid()))
    print(f"  Poisson identity nu_l * exp(1_(l,z] dv/v) = nu_z: sandwich holds on {Nt} cells "
          f"(L={L}, K={K}, k={k}; max rel. width {wmax:.3g})")

# ---------------------------------------------------------------- Part E ---
print("== Part E: real parameters, all 61 low bins, prefix j < jmax ==")
delay_cache = {}
BR = {}
for bi, b in enumerate(BINS):
    L, H, K, th, J = b["L"], b["H"], b["K"], b["th"], b["J"]
    if L <= 30:
        Nt, k = min(40 * L, 1000), 4
    elif L <= 1000:
        Nt, k = min(2 * L + 100, N), 4
    else:
        Nt, k = min(2 * L + 100, N), 2
    use_delay = False
    if L >= 64:
        if L not in delay_cache:
            lo, hi, (ok, jb) = delay(L, N - 1)
            if ok:
                # spot check enclosure against rho on the prefix
                for j in range(0, min(N - 1, 4 * L) + 1, max(1, L // 50)):
                    rv = RHO(F(j, L))
                    check(lower_ok(lo[j], rv) and rv.upper() <= arb(hi[j]) / ONE,
                          f"delay M={L} j={j} encloses rho")
                delay_cache[L] = (True, [arb(hi[j]) / ONE for j in range(Nt)], None)
            else:
                delay_cache[L] = (False, None, jb)
            del lo, hi
        use_delay = delay_cache[L][0]
    if use_delay:
        dstar = delay_cache[L][1][:Nt]
        br = "delay"
    else:
        Rr = renewal(L, Nt)
        dstar = [A(Rr[j]) for j in range(Nt)]
        br = "renewal" if L < 64 else f"renewal (delay rejected: upper rises at j={delay_cache[L][2]})"
    exact = L <= 30
    Bt, Mt, info = construct(h, L, H, K, Nt, th, dstar, J, exact=exact)
    uB, uM = true_masses(h, L, H, K, Nt, th, k)
    lB, lM = true_masses(h, L, H, K, Nt, th, k, lower=True)
    worst, nz = compare(f"{b['g']} L{b['idx']}", Bt, Mt, uB, uM, lB, lM, Nt)
    extra = f", remainder cells {info['omit0']}/{info['omit1']}" if exact else ""
    print(f"  {b['g']:8s} L{b['idx']:<2d} L={L:<6d} H={H:<6d} K={K} theta={str(th):7s} J={J:2d} {br:7s} "
          f"jmax={Nt:<6d} k={k} r_max={info['rmax']:<2d}{extra}; max true/coef={worst:.4f}")
    BR[br.split()[0]] = BR.get(br.split()[0], 0) + 1
    sys.stdout.flush()

print(f"  kernel branches used: {BR}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
print(f"\nchecks: {NCHK}   failures: {NFAIL}   run time: {time.time() - T_START:.1f} s   peak RSS: {rss:.0f} MB")
print("VERDICT: Lemma 2.3 " + ("VERIFIED as stated (on all tested cells)" if NFAIL == 0 else "FAILED checks"))
