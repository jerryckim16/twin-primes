#!/usr/bin/env python3
"""Rung 186: check of Lemma 2.4 ("Whole-bin Palm envelopes", p. 14) of OpenAI's numerical companion [14]
("Numerical certificate for prime gaps at most 186", code/third_party/openai186/short_gaps_numerics.pdf).
Report: notes/oai186-lemma24-check.md.  Modelled on code/oai186_lemma23_check.py and oai186_lemma17_check.py.

Setting (p. 14).  Rank-two bin (a, b] with U/(m+1) <= a < b <= z0 < U, m in {2, 5/2};
  r(q) := (U-q)/m <= q,  r- := (U-b)/m,  r+ := (U-a)/m,  s-_j := max(0, j - ceil(b/h)),  s+_j := max(0, j+1 - floor(a/h)),
  t+_j := (j+1)h,  beta_j := 0 (jh < b),  beta_j := dlow_{s+_j}(r-^-) otherwise;
  (2.9)  P_j := up(w_j dup_j(b^+)),                      A_j := 1[t+_j > a] up(w_j dup_{s-_j}(r+^+)),
         B_j := up(w_j [dup_j(b^+) - dlow_{j+1}(r-^-)]_+),  C_j := 1[t+_j > a + r+] up(w_j [dup_{s-_j}(b^+) - beta_j]_+).
  c^+ = h ceil(c/h), c^- = h floor(c/h); dup_j(c), dlow_j(c) = the Lemma 2.2 (2.1) endpoint sequences for the cap c
  (enclosing D_c(jh) = rho(jh/c)).
Lemma 2.4: P, A, B, C bound the ordinary, largest-fragment-coordinate, distinct-secondary and same-coordinate
coordinate densities, uniformly over the bin; Lambda := log(b/a), lambda(v) := min{1, max{0, log(v/a)/Lambda}};
the A and C arrays may be multiplied by lambda(t+_j) and lambda(min{t+_j, (m t+_j - U)/(m-1)}); Lambda is charged once.

Every decision is exact (Fraction / int) or a certain comparison of python-flint arb balls; floats only print.
Sections:
  [0] groups and the 30 rank-two bins; hypotheses; grid caps b^+, r+^+, r-^-; r- <= r(q) <= r+, r(q) <= q, r+ <= a
  [1] index facts of the proof, exhaustively over all 30 x 98264 (bin, cell) pairs (exact integers)
  [2] a rigorous Dickman rho on [0, 6] (power series per unit segment with a proved tail bound), cross-checked
  [3] Lemma 2.2 recurrence (2.1) as printed, exact dyadic, for the 90 grid caps of (2.9): acceptance on all j <= n,
      and rigorous spot checks dlow_j <= rho(j/M) <= dup_j
  [4] the (2.9) arrays (profile power 0) against (i) the rigorous whole-bin supremum of each role density over
      q in (a, b], t in C_j and (ii) pointwise true densities at sampled (q, t); negative controls
  [5] small instance, end to end: d = 2 coordinates, the exact Palm mass int_a^b dq/q of (1.40) on cell pairs
      (rigorous upper Riemann bound) <= Lambda h^2 [xy]-ring bound with the lambda fractions
  [6] algebra: (1.40) <= (1.41), and (1.41) = [xy] prod_v (P_v + x A_v + y B_v + xy C_v) (exact, d = 2..8)
  [7] authors' script (comparison only): TASKS, LargestFragmentPalmFactory.kernels on two bins vs our (2.9)
usage: /usr/bin/python3 code/oai186_lemma24_check.py > code/oai186_lemma24_check.out"""
import os, sys, time, random, importlib.util, io, contextlib, resource, inspect
from fractions import Fraction as F
from math import floor, ceil
from flint import arb, arb_poly, acb, ctx

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []
NCHECK = [0]
ctx.prec = 200
rnd = random.Random(20261124)


def check(name, cond, detail=""):
    NCHECK[0] += 1
    print(("  PASS " if cond else "  FAIL ") + name + (("   [" + detail + "]") if detail else ""))
    sys.stdout.flush()
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


def A(x):  # exact rational -> arb ball
    x = F(x)
    return arb(x.numerator) / arb(x.denominator)


def le(a_, b_):  # a <= b certainly (arb balls)
    return (b_ - a_) >= 0


def a2F(x):  # exact dyadic arb endpoint -> Fraction
    m_, e_ = x.man_exp()
    return F(int(m_)) * F(2) ** int(e_)


def cdiv(x, d):  # ceil(x/d), d > 0, integers
    return -((-x) // d)


# ---------------------------------------------------------------------------------------------------------------
print("[0] groups (1.23)-(1.24) via code/oai186_support_data.py; the 30 rank-two bins of Sec. 1.5.1 (p. 9)")
sd = load("sd186", os.path.join(HERE, "oai186_support_data.py"))
check("oai186_support_data.py: all its printed-value checks pass", sd.res["all_ok"] is True)
h, S = sd.h, sd.S
N, n = 98304, 98304 - 40
check("(1.3): h = S/98304, S = 2742997/2624989, n = 98264", h == F(2742997, 2624989 * 98304))
NAMES = ["O2", "O5/2", "I2old", "I5/2old", "I2new", "I5/2new"]
GR = []
for name in NAMES:
    m, xi, U, zh, ph = sd.G[name]
    GR.append(dict(name=name, m=m, xi=xi, U=U, z=zh * h, p=ph * h, q0=U / (m + 1)))
TL = [[F(j, 6) for j in range(7)],
      [F(j, 16) for j in range(9)] + [F(5, 8), F(3, 4), F(7, 8), F(1)],
      [F(0), F(1)], [F(0), F(1, 2), F(1)], [F(0), F(1, 6), F(1, 2), F(2, 3), F(1)],
      [F(0), F(1, 8), F(3, 8), F(1, 2), F(3, 4), F(1)]]
BINS = []
for G, T in zip(GR, TL):
    for j in range(1, len(T)):
        a_, b_ = G["q0"] + T[j - 1] * (G["z"] - G["q0"]), G["q0"] + T[j] * (G["z"] - G["q0"])
        U, m = G["U"], G["m"]
        BINS.append(dict(G=G, name="P%d" % j, a=a_, b=b_, U=U, m=m, rm=(U - b_) / m, rp=(U - a_) / m,
                         Mb=cdiv(b_.numerator * h.denominator, b_.denominator * h.numerator),
                         Mrp=cdiv(((U - a_) / m).numerator * h.denominator, ((U - a_) / m).denominator * h.numerator),
                         Mrm=(((U - b_) / m) / h).__floor__(),
                         fa=(a_ / h).__floor__(), cb=(b_ / h).__ceil__()))
check("30 bins (6, 12, 1, 2, 4, 5); hypotheses of (2.9): U/(m+1) <= a < b <= z0 = z_G < U, m in {2, 5/2}",
      len(BINS) == 30 and all(B["G"]["q0"] <= B["a"] < B["b"] <= B["G"]["z"] < B["U"] and B["m"] in (2, F(5, 2))
                              for B in BINS))
check("grid caps: b^+ = h ceil(b/h) >= b, r+^+ = h ceil(r+/h) >= r+, r-^- = h floor(r-/h) <= r-, and r-^- >= 64h"
      " (a positive cell; Lemma 2.2 needs M >= 1)",
      all(B["Mb"] * h >= B["b"] > (B["Mb"] - 1) * h and B["Mrp"] * h >= B["rp"] > (B["Mrp"] - 1) * h
          and (B["Mrm"] + 1) * h > B["rm"] >= B["Mrm"] * h and B["Mrm"] >= 64 for B in BINS),
      "M ranges: b^+ %d..%d, r+^+ %d..%d, r-^- %d..%d" % (
          min(B["Mb"] for B in BINS), max(B["Mb"] for B in BINS), min(B["Mrp"] for B in BINS),
          max(B["Mrp"] for B in BINS), min(B["Mrm"] for B in BINS), max(B["Mrm"] for B in BINS)))
# r is affine decreasing, so on (a, b]: r- = r(b) <= r(q) < r(a) = r+; r(q) <= q iff q >= U/(m+1).
check("r(q) = (U-q)/m is decreasing, so r- = r(b) <= r(q) < r(a) = r+ on (a, b]; r(q) <= q there because"
      " q > a >= U/(m+1) (r(U/(m+1)) = U/(m+1) exactly)",
      all(B["rm"] == (B["U"] - B["b"]) / B["m"] and B["rp"] == (B["U"] - B["a"]) / B["m"] and B["rm"] < B["rp"]
          and (B["U"] - B["G"]["q0"]) / B["m"] == B["G"]["q0"] for B in BINS))
check("fact not stated: r+ <= a on every bin (so the owner residual cap r(q) is always below the bin)",
      all(B["rp"] <= B["a"] for B in BINS), "max r+/a = %s" % fl(max(B["rp"] / B["a"] for B in BINS)))
check("D_c(t) = rho(t/c) arguments stay below 6: n h / r- < 6 on every bin (needed by the rho evaluator of [2])",
      all(n * h / B["rm"] < 6 for B in BINS), "max n h / r- = %s" % fl(max(n * h / B["rm"] for B in BINS)))

# ---------------------------------------------------------------------------------------------------------------
print("\n[1] index facts of the proof, exhaustively over all 30 x %d (bin, cell) pairs (exact integers)" % n)
# In units of h: x/h for x = a, b, r+ as exact fractions p/q; all comparisons are integer cross-multiplications.
ok1 = ok2 = ok3 = ok4 = True
cnt_beta = 0
for B in BINS:
    bh, ah = B["b"] / h, B["a"] / h
    bp, bq, ap, aq = bh.numerator, bh.denominator, ah.numerator, ah.denominator
    cb, fa = B["cb"], B["fa"]
    for j in range(n):
        sm = max(0, j - cb)
        sp = max(0, j + 1 - fa)
        # (i) s-_j h <= max(0, jh - b) <= t - q for t in C_j, q <= b, t >= q   (upper endpoints, A and C)
        ok1 &= (sm == 0) or (sm * bq <= j * bq - bp)
        # (ii) s+_j h >= t+_j - a > t - q for t < t+_j, q > a                 (lower endpoint in C)
        ok2 &= sp * aq >= (j + 1) * aq - ap
        # (iii) indices used by (2.9) stay inside the arrays 0..n
        ok3 &= 0 <= sm <= n and 0 <= sp <= n and j + 1 <= n
        if j * bq >= bp:
            cnt_beta += 1
    # (iv) s-_j and s+_j are the tightest integer choices: s- = max over integers with s h <= jh - b, etc.
    ok4 &= cb - 1 < bh <= cb and fa <= ah < fa + 1
check("(i) s-_j h <= max(0, jh - b) for every j: since t >= jh and q <= b, t - q >= s-_j h on the owner"
      " coordinate (the 'upper endpoints' step for A and C, monotonicity of D in its argument)", ok1)
check("(ii) s+_j h >= t+_j - a for every j (not only jh >= b): since t < t+_j and q > a, t - q < s+_j h"
      " (the 'lower endpoint in the same-coordinate difference')", ok2,
      "beta_j is nonzero only on %d of %d pairs (jh >= b); elsewhere the proof uses the weaker beta_j = 0" % (
          cnt_beta, 30 * n))
check("(iii) every index used in (2.9) (j, j+1, s-_j, s+_j) lies in 0..n, inside the Lemma 2.2 arrays", ok3)
check("(iv) ceil(b/h), floor(a/h) as used: ceil(b/h) - 1 < b/h <= ceil(b/h), floor(a/h) <= a/h < floor(a/h)+1",
      ok4)

# ---------------------------------------------------------------------------------------------------------------
print("\n[2] a rigorous Dickman rho on [0, 6]")
# Segment k (u in [k-1, k]): rho(u) = sum_i c_i xi^i, xi = k - u in [0, 1].  From u rho'(u) = -rho(u-1):
# (k - xi) rho_k'(xi) = rho_{k-1}(xi), so c_{i+1} = (e_i + i c_i)/(k(i+1)) with e the coefficients of segment k-1;
# c_0 = rho(k-1) - sum_{i>=1} c_i (continuity, xi = 1).  rho_{k-1} is analytic for |xi| < 2 (induction), hence so
# is rho_k and its Taylor series converges at xi = 1.  Tail: if |e_i| <= E 2^-i and |c_I| <= g 2^-I then by
# induction |c_i| <= max(E, g) 2^-i for all i >= I (because 2(E + i G)/(k(i+1)) <= G for k >= 2, G >= E).
ISER = 110
SEG = {1: ([arb(1)] + [arb(0)] * ISER, arb(0))}   # k -> (coeffs c_0..c_I, G with |c_i| <= G 2^-i for i > I)
for k in range(2, 7):
    e, E = SEG[k - 1]
    c = [arb(0)] * (ISER + 1)
    c[1] = e[0] / k
    for i in range(1, ISER):
        c[i + 1] = (e[i] + i * c[i]) / (k * (i + 1))
    g = abs(c[ISER]) * arb(2) ** ISER
    G = max(E.upper(), g.upper())
    tail = G * arb(2) ** (-ISER)                     # sum_{i > I} G 2^-i
    c[0] = e[0] - sum(c[1:]) + arb(0, tail)
    SEG[k] = (c, G)
POLY = {k: arb_poly(SEG[k][0]) for k in SEG}
TAIL = {k: arb(0, (SEG[k][1] * arb(2) ** (-ISER)).upper()) for k in SEG}


def rho(u):
    """rigorous rho at an exact rational u >= 0 (arb ball)."""
    u = F(u)
    if u <= 1:
        return arb(1)
    k = u.__ceil__()
    if k > 6:
        raise ValueError("rho evaluator only on [0, 6]")
    return POLY[k](A(k - u)) + TAIL[k]


def rho_li2(u):  # closed form on [2, 3]
    x = A(u)
    return 1 - (1 - (x - 1).log()) * x.log() + acb(1 - x).polylog(2).real + arb.pi() ** 2 / 12


ok = all((rho(u) - (1 - A(u).log())).contains(0) and rho(u).rad() < arb(10) ** -25
         for u in (F(5, 4), F(3, 2), F(7, 4), F(2)))
check("segment [1,2]: series = 1 - log u at u = 5/4, 3/2, 7/4, 2 (balls overlap, radius < 1e-25)", ok)
ok = all((rho(u) - rho_li2(u)).contains(0) for u in (F(9, 4), F(5, 2), F(11, 4), F(3), F(2001, 1000)))
check("segment [2,3]: series = 1 - (1 - log(u-1)) log u + Li2(1-u) + pi^2/12 at 5 points", ok)
# [3,4]: rho(u) = rho(3) - int_3^u rho(v-1)/v dv;  [4,5] (Fubini): rho(u) = rho(4) - rho(3) log(u/4)
#         + int_3^{u-1} rho(w-1) log(u/(w+1)) / w dw, with rho(v-1) for v-1 in [2,3] in closed form.


def li2_integrand(wt):
    def f(v, an):
        x = v - 1
        val = 1 - (1 - (x - 1).log(analytic=an)) * x.log(analytic=an) + (1 - x).polylog(2) + acb.pi() ** 2 / 12
        return val * wt(v, an) / v
    return f


r3 = rho_li2(F(3))
I34 = acb.integral(li2_integrand(lambda v, an: 1), 3, 4).real
r4 = r3 - I34
okq = (rho(F(4)) - r4).contains(0) and (rho(F(7, 2)) - (r3 - acb.integral(li2_integrand(lambda v, an: 1), 3,
                                                                                 A(F(7, 2))).real)).contains(0)
for uu in (F(9, 2), F(5)):
    I_ = acb.integral(li2_integrand(lambda v, an, uu=uu: (A(uu) / (v + 1)).log(analytic=an)), 3, A(uu - 1)).real
    okq &= (rho(uu) - (r4 - r3 * (A(uu) / 4).log() + I_)).contains(0)
check("segments [3,4], [4,5]: series agrees with acb.integral of the delay equation (Li2 closed form inside) at"
      " u = 7/2, 4, 9/2, 5", okq, "rho(3), rho(4), rho(5) = %s, %s, %s" % (
          fl(rho(3).mid(), 12), fl(rho(4).mid(), 12), fl(rho(5).mid(), 12)))
okm = True
for k in range(2, 7):
    xs = [F(k - 1) + F(i, 40) for i in range(41)]
    vals = [rho(x) for x in xs]
    okm &= all(le(vals[i + 1], vals[i]) for i in range(40))
okm &= max(rho(F(k) + F(1, 3)).rad() for k in range(1, 6)) < arb(10) ** -25
check("rho nonincreasing on a 1/40 grid of [1, 6] (certain comparisons) and radii < 1e-25", okm)

def Phi(u):
    """int_0^u rho for exact u (0 for u <= 0): Phi(u) = sum_{i<k} (u-i) rho(u-i) + (u - k), k = floor(u), from
    u rho(u) = int_{u-1}^u rho (u >= 1)."""
    u = F(u)
    if u <= 0:
        return arb(0)
    k = u.__floor__()
    s = A(u - k)
    for i in range(k):
        s += A(u - i) * rho(u - i)
    return s


I12 = acb.integral(lambda v, an: 1 - v.log(analytic=an), 1, A(F(3, 2))).real
okphi = (Phi(F(3, 2)) - (1 + I12)).contains(0)
I2u = acb.integral(lambda v, an: 1 - (1 - (v - 1).log(analytic=an)) * v.log(analytic=an) + (1 - v).polylog(2)
                   + acb.pi() ** 2 / 12, 2, A(F(5, 2))).real
okphi &= (Phi(F(5, 2)) - (1 + (2 - 2 * arb(2).log()) + I2u)).contains(0)      # int_1^2 (1 - log v) = 2 - 2 log 2
check("antiderivative Phi(u) = int_0^u rho (used in [5]) agrees with acb.integral at u = 3/2, 5/2", okphi)

# ---------------------------------------------------------------------------------------------------------------
print("\n[3] Lemma 2.2, (2.1) as printed, exact dyadic (scale 2^-160), for the grid caps of (2.9)")
PB = 160
ONE = 1 << PB


def delay(M, count=n):
    """(2.1): dlow_{j+1} = max{0, dn(dlow_j - dup_{j-M}/(2j) - dup_{j+1-M}/(2(j+1)))},
    dup_{j+1} = min{1, up(dup_j - dlow_{j-M}/(2j) - dlow_{j+1-M}/(2(j+1)) + 1/(2M^3))}; returns (lo, hi) for
    j = 0..count as integers scaled by 2^PB, rounded outward; and the acceptance flag."""
    lo, hi = [ONE] * (M + 1), [ONE] * (M + 1)
    err = cdiv(ONE, 2 * M ** 3)
    acc = True
    for j in range(M, count):
        l_ = lo[j] - cdiv(hi[j - M], 2 * j) - cdiv(hi[j + 1 - M], 2 * (j + 1))
        u_ = hi[j] - lo[j - M] // (2 * j) - lo[j + 1 - M] // (2 * (j + 1)) + err
        l_, u_ = max(0, l_), min(ONE, u_)
        if not (0 <= l_ <= u_ <= ONE and l_ <= lo[j] and u_ <= hi[j]):
            acc = False
        lo.append(l_)
        hi.append(u_)
    return lo, hi, acc


def D2A(x):
    return arb(x) * arb(2) ** (-PB)          # exact dyadic ball


CAPS = {}
t3 = time.time()
okacc = True
for B in BINS:
    for M in (B["Mb"], B["Mrp"], B["Mrm"]):
        CAPS[M] = None
NEED_LO = set(B["Mrm"] for B in BINS)
print("  %d distinct grid caps" % len(CAPS))
oklemma22, nsp = True, 0
worst22 = None
for M in sorted(CAPS):
    lo, hi, acc = delay(M)
    okacc &= acc
    js = sorted(set([M, M + 1, 2 * M - 1, 2 * M, 2 * M + 1, 3 * M, n - 1, n] + [rnd.randrange(M, n + 1) for _ in range(12)]))
    for j in js:
        if j > n:
            continue
        r_ = rho(F(j, M))
        oklemma22 &= le(D2A(lo[j]), r_) and le(r_, D2A(hi[j]))
        nsp += 1
        if j > M:
            w_ = (D2A(hi[j]) - r_).mid()
            worst22 = w_ if worst22 is None or w_ < worst22 else worst22
    CAPS[M] = (lo if M in NEED_LO else None, hi)
check("(2.1) acceptance tests on the full range j <= n for all %d caps: 0 <= dlow <= dup <= 1, both sequences"
      " nonincreasing (so the delay branch is accepted)" % len(CAPS), okacc, "%.1f s" % (time.time() - t3))
check("Lemma 2.2 spot check: dlow_j(Mh) <= rho(j/M) <= dup_j(Mh) rigorously at %d sampled (cap, j), j in [M, n]"
      % nsp, oklemma22, "min dup - rho on j > M: %s" % fl(worst22, 3))

# ---------------------------------------------------------------------------------------------------------------
print("\n[4] the (2.9) arrays (profile power 0, w = 1) against true role densities on the 30 actual bins")


def arrays(B, variant=None):
    """the four (2.9) arrays as exact integers scaled 2^-PB, j = 0..n-1 (w = 1)."""
    hib = CAPS[B["Mb"]][1]
    hirp = CAPS[B["Mrp"]][1]
    lorm, hirm = CAPS[B["Mrm"]]
    jA0 = (B["a"] / h).__floor__()                 # (j+1)h > a  <=>  j >= floor(a/h)
    jC0 = ((B["a"] + B["rp"]) / h).__floor__()     # (j+1)h > a + r+  <=>  j >= floor((a + r+)/h)
    cb = B["cb"]                                   # jh < b  <=>  j < ceil(b/h)
    P, Aa, Bb, C = [], [], [], []
    for j in range(n):
        sm, sp = max(0, j - cb), max(0, j + 1 - B["fa"])
        P.append(hib[j])
        if variant == "A_wrong_cap":
            Aa.append(hirm[sm] if j >= jA0 else 0)
        else:
            Aa.append(hirp[sm] if j >= jA0 else 0)
        Bb.append(max(0, hib[j] - lorm[j + 1]))
        beta = 0 if j < cb else lorm[sp]
        idx = j if variant == "C_no_shift" else sm
        C.append(max(0, hib[idx] - beta) if j >= jC0 else 0)
    return P, Aa, Bb, C


def sample_cells(B):
    a_, b_, rp = B["a"], B["b"], B["rp"]
    sp = set(range(0, n, 97))
    for x in (a_, b_, a_ + rp, 2 * b_, B["rm"], B["rp"], b_ + B["rm"]):
        c0 = (x / h).__floor__()
        sp |= set(range(max(0, c0 - 3), min(n, c0 + 4)))
    sp |= set(range(n - 3, n))
    sp |= set(rnd.randrange(n) for _ in range(150))
    return sorted(sp)


def role_sup(B, j):
    """rigorous upper bounds for sup over q in (a,b], t in C_j (t >= q on the owner coordinate) of the four role
    densities, by monotonicity (D_c(t) nondecreasing in c, nonincreasing in t) with the exact caps b, r+, r-."""
    a_, b_, rp, rm = B["a"], B["b"], B["rp"], B["rm"]
    jh, tp = j * h, (j + 1) * h
    res = max(F(0), jh - b_)
    sP = rho(jh / b_)
    sA = rho(res / rp) if tp > a_ else arb(0)
    sB = sP - rho(tp / rm)
    sC = (rho(res / b_) - rho((tp - a_) / rm)) if tp > a_ + rp else arb(0)
    return sP, sA, sB, sC


def role_point(B, q, t):
    """true role densities at exact (q, t): ordinary D_q(t); owner D_r(t-q); distinct D_q(t) - D_r(t);
    same D_q(t-q) - D_r(t-q), r = r(q); owner/same are 0 unless t >= q."""
    r = (B["U"] - q) / B["m"]
    vP = rho(t / q)
    vB = vP - rho(t / r)
    if t >= q:
        vA = rho((t - q) / r)
        vC = rho((t - q) / q) - vA
    else:
        vA = vC = arb(0)
    return vP, vA, vB, vC


t4 = time.time()
ok_sup = [True] * 4
ok_pt = [True] * 4
ok_ind = True
ncell = npt = 0
slack = [None] * 4
ctl_A = ctl_C = False
for B in BINS:
    arr = arrays(B)
    arrA_bad = arrays(B, "A_wrong_cap")[1]
    arrC_bad = arrays(B, "C_no_shift")[3]
    a_, b_ = B["a"], B["b"]
    for j in sample_cells(B):
        ncell += 1
        sups = role_sup(B, j)
        for k in range(4):
            av = D2A(arr[k][j])
            ok_sup[k] &= le(sups[k], av)
            if arr[k][j] > 0 and sups[k] > 0:
                sl = ((av - sups[k]) / av).mid()
                slack[k] = sl if slack[k] is None or sl < slack[k] else slack[k]
        if not le(sups[1], D2A(arrA_bad[j])):
            ctl_A = True
        if not le(sups[3], D2A(arrC_bad[j])):
            ctl_C = True
        # pointwise: q at the bin's ends and random interior points; t at the cell's ends and inside
        qs = [b_, a_ + (b_ - a_) / 10 ** 9, a_ + (b_ - a_) * F(rnd.randrange(1, 10 ** 6), 10 ** 6)]
        ts = [j * h, (j + 1) * h - h / 10 ** 9, j * h + h * F(rnd.randrange(1, 10 ** 6), 10 ** 6)]
        for q in qs:
            for t in ts:
                vals = role_point(B, q, t)
                npt += 1
                for k in range(4):
                    ok_pt[k] &= le(vals[k], D2A(arr[k][j])) and not (vals[k] > sups[k])   # (equal at q = b, t = jh)
                # the zero indicators: a positive owner/same density forces the indicator on
                if t >= q and not (t < (j + 1) * h and (j + 1) * h > a_):
                    ok_ind = False
                if t >= q and vals[3] > 0 and not ((j + 1) * h > a_ + B["rp"]):
                    ok_ind = False
ROLE = ["ordinary P", "largest-fragment coordinate A", "distinct-secondary B", "same-coordinate C"]
for k in range(4):
    check("(2.9) %s: rigorous whole-bin supremum of the true density <= array on all %d sampled (bin, cell)"
          " pairs" % (ROLE[k], ncell), ok_sup[k],
          "min relative slack where both > 0: %s" % (fl(slack[k], 3) if slack[k] is not None else "-"))
for k in range(4):
    check("(2.9) %s: true density at %d sampled exact (q, t) <= array (certain), and not above the supremum bound"
          " (consistency; equality occurs at q = b, t = jh)" % (ROLE[k], npt),
          ok_pt[k])
check("zero indicators 1[t+ > a], 1[t+ > a + r+]: every sampled point with t >= q (resp. positive same-coordinate"
      " density) lies in a cell where the indicator is 1", ok_ind)
check("negative controls bite: A with the downward cap r-^- instead of r+^+, and C without the residual shift"
      " (index j instead of s-_j), each violate the supremum bound somewhere", ctl_A and ctl_C,
      "A: %s, C: %s; %.1f s" % (ctl_A, ctl_C, time.time() - t4))

# ---------------------------------------------------------------------------------------------------------------
print("\n[5] end to end, d = 2: exact Palm mass int_a^b dq/q of (1.40) on cell pairs <= the Lemma 2.4 bound")


def I_ord(j, c):          # int_{C_j} D_c(t) dt
    return A(c) * (Phi((j + 1) * h / c) - Phi(j * h / c))


def I_own(j, c, q):       # int_{C_j} D_c(t - q) dt
    return A(c) * (Phi(((j + 1) * h - q) / c) - Phi((j * h - q) / c))


def I_own_up(j, q1, q2):
    """>= sup_{q in [q1,q2]} int_{C_j} D_q(t - q) dt: for q <= t < q2 bound D by 1, for t >= q2 use
    D_q(t - q) = rho(t/q - 1) <= rho(t/q2 - 1) (t/q - 1 decreasing in q); 0 for t < q1."""
    lo_, hi_ = max(j * h, q1), min((j + 1) * h, q2)
    return A(max(F(0), hi_ - lo_)) + I_own(j, q2, q2)


def I_own_low(j, q1, q2, r2):
    """<= inf_{q in [q1,q2]} int_{C_j} D_{r(q)}(t - q) dt: on t >= q2, r(q) >= r2 and t - q <= t - q1; else 0."""
    if (j + 1) * h <= q2:
        return arb(0)
    s0 = max(j * h, q2)
    return A(r2) * (Phi(((j + 1) * h - q1) / r2) - Phi((s0 - q1) / r2))


def lam_up(B, v):          # Lambda * lambda(v), exact-ball: log(min(max(v,a),b)/a)
    v = min(max(F(v), B["a"]), B["b"])
    return (A(v) / A(B["a"])).log()


def true_mass_upper(B, j1, j2, K):
    """rigorous upper bound for int_a^b dq/q sum_{owner o in {1,2}} int_{C_j1 x C_j2} [A_o A_other - B_o B_other].
    For owner o the integrand vanishes for q >= t+_o (A_o = B_o = 0 there), so q runs over (a, min(b, t+_o));
    this range is cut at j_o h, with K equal pieces below and K pieces across the owner cell. On each piece
    [q1, q2] every cell integral is bounded by monotonicity (I_own_up, I_own_low, I_ord)."""
    a_, b_, U, m = B["a"], B["b"], B["U"], B["m"]
    tot = arb(0)
    for jo, jx in ((j1, j2), (j2, j1)):
        qe = min(b_, (jo + 1) * h)
        if qe <= a_:
            continue                                   # t+_o <= a: no largest fragment in C_o, exactly 0
        if (jo + 1) * h <= a_ + B["rp"] and (jx + 1) * h <= B["rm"]:
            continue                                   # t < a + r+ < q + r(q) (q + r(q) increasing), so the owner
            #                                            residual t - q < r(q) <= q, and t_x < r- <= r(q): then
            #                                            A_o = B_o = A_x = B_x = 1 pointwise, integrand exactly 0
        qm = min(qe, max(a_, jo * h))
        pts = [a_ + (qm - a_) * k / K for k in range(K)] + [qm + (qe - qm) * k / K for k in range(K + 1)]
        pts = sorted(set(pts))
        for q1, q2 in zip(pts, pts[1:]):
            r2 = (U - q2) / m
            up = I_own_up(jo, q1, q2) * I_ord(jx, q2)          # A-terms: bounded above
            low = I_own_low(jo, q1, q2, r2) * I_ord(jx, r2)    # B-terms: bounded below
            tot += (up - low) * (A(q2) / A(q1)).log()
    return tot


def bound_d2(B, arr, j1, j2):
    """Lambda h^2 [xy] (P + x A + y B + x y C)_{j1} (...)_{j2}, with A, C multiplied by the lambda fractions."""
    P, Aa, Bb, C = [[D2A(x[j]) for j in (j1, j2)] for x in arr]
    U, m = B["U"], B["m"]
    fA = [lam_up(B, (j + 1) * h) for j in (j1, j2)]
    fC = [lam_up(B, min((j + 1) * h, (m * (j + 1) * h - U) / (m - 1))) for j in (j1, j2)]
    val = C[0] * fC[0] * P[1] + P[0] * C[1] * fC[1] + Aa[0] * fA[0] * Bb[1] + Bb[0] * Aa[1] * fA[1]
    return A(h) ** 2 * val


t5 = time.time()
ok5 = True
npair, minratio = 0, None
Kused = {}
for bi, B in enumerate(BINS):
    arr = arrays(B)
    a_, b_, rp = B["a"], B["b"], B["rp"]
    ja = (a_ / h).__floor__()                      # owner cell partial (t+ just above a)
    jc = ((a_ + rp) / h).__floor__() + 1           # first same-coordinate cell
    jb = (b_ / h).__ceil__()
    jr = (B["rm"] / h).__floor__() + 5
    pairs = [(jc, jr), (jc + 40, (b_ / h).__floor__()), (jb + 200, jr + 100), (ja + 1, jr + 3000),
             (ja + 1, (a_ / h).__floor__() + 10)]
    if bi % 6 == 0:
        pairs.append((jb + 9000, jr - 50))
    for j1, j2 in pairs:
        if not (0 <= j1 < n and 0 <= j2 < n):
            continue
        bd = bound_d2(B, arr, j1, j2)
        for K in (24, 96, 384):                     # refine the q-partition only if the coarse bound is too crude
            tm = true_mass_upper(B, j1, j2, K)
            if le(tm, bd):
                break
        Kused[K] = Kused.get(K, 0) + 1
        ok5 &= le(tm, bd)
        npair += 1
        if tm > 0:
            rt = (tm / bd).mid()
            minratio = rt if minratio is None or rt > minratio else minratio
check("d = 2: rigorous upper bound of the true one-largest Palm mass (1.40), both owner choices, on %d actual"
      " (bin, cell-pair) instances <= Lambda h^2 [xy]-ring bound with the (2.9) arrays and lambda fractions"
      % npair, ok5, "max (true upper)/bound = %s; partition sizes used %s; %.1f s" % (
          fl(minratio, 4) if minratio is not None else "-", Kused, time.time() - t5))

# ---------------------------------------------------------------------------------------------------------------
print("\n[6] algebra: (1.40) <= (1.41) and the ring form, exact rationals, d = 2..8")
ok_tel = ok_ring = True
for d in range(2, 9):
    for _ in range(60):
        Av = [F(rnd.randrange(0, 1000), 997) for _ in range(d)]
        Bv = [x * F(rnd.randrange(0, 1001), 1000) for x in Av]       # 0 <= B <= A
        Ao = [F(rnd.randrange(0, 1000), 991) for _ in range(d)]      # owner-shifted A
        Bo = [x * F(rnd.randrange(0, 1001), 1000) for x in Ao]
        for o in range(d):
            others = [i for i in range(d) if i != o]
            pa = pb = F(1)
            for i in others:
                pa *= Av[i]
                pb *= Bv[i]
            exact = Ao[o] * pa - Bo[o] * pb                          # (1.40) integrand, owner o
            t1 = (Ao[o] - Bo[o]) * pa
            t2 = F(0)
            for i in others:
                pr = F(1)
                for v in others:
                    if v != i:
                        pr *= Av[v]
                t2 += (Av[i] - Bv[i]) * pr
            bound = t1 + Bo[o] * t2                                  # (1.41)
            ok_tel &= 0 <= exact <= bound
        # ring: [xy] prod_v (P_v + x A_v + y B_v + xy C_v), with owner roles on the owner, summed over owners,
        # equals sum_o (1.41)_o when P = A (ordinary), A-role = B_owner, B-role = A - B, C-role = A_owner - B_owner.
        # The ring polynomial needs one choice of owner arrays per coordinate: use the same coordinate values.
        Pv = Av
        Ar = Bo
        Br = [Av[i] - Bv[i] for i in range(d)]
        Cr = [Ao[i] - Bo[i] for i in range(d)]
        poly = {(0, 0): F(1)}
        for v in range(d):
            new = {}
            for (ex, ey), co in poly.items():
                for (dx, dy, val) in ((0, 0, Pv[v]), (1, 0, Ar[v]), (0, 1, Br[v]), (1, 1, Cr[v])):
                    if ex + dx <= 1 and ey + dy <= 1:
                        new[(ex + dx, ey + dy)] = new.get((ex + dx, ey + dy), 0) + co * val
            poly = new
        s141 = F(0)
        for o in range(d):
            others = [i for i in range(d) if i != o]
            pa = F(1)
            for i in others:
                pa *= Av[i]
            t2 = F(0)
            for i in others:
                pr = F(1)
                for v in others:
                    if v != i:
                        pr *= Av[v]
                t2 += (Av[i] - Bv[i]) * pr
            s141 += (Ao[o] - Bo[o]) * pa + Bo[o] * t2
        ok_ring &= poly.get((1, 1), 0) == s141
check("(1.40) <= (1.41): 0 <= A_o prod A_i - B_o prod B_i <= (A_o - B_o) prod A_i + B_o sum_i (A_i - B_i)"
      " prod_{v != i,o} A_v whenever 0 <= B <= A (exact, 7 x 60 random instances, every owner)", ok_tel)
check("role map of Lemma 2.4: [xy] prod_v (P_v + x A_v + y B_v + x y C_v) = sum over owners of (1.41) with"
      " P = D_q(t), A = D_r(t - q), B = D_q(t) - D_r(t), C = D_q(t - q) - D_r(t - q) (exact, d = 2..8)", ok_ring)
check("lambda(v) of Lemma 2.4 with (a, b) equals Lf(v)/L of Lemma 1.7 (1.45) with (q-, q+) = (a, b): 0 for"
      " v <= a, log(v/a)/Lambda in between, 1 for v >= b; so the fraction step is Lemma 1.7 (checked there)", True,
      "by reading; identical definitions")
check("Palm density (1.40): Mecke with the void probability gives nu_z|{largest fragment = q} = (nu_q + {q}) dq/q"
      " and nu_z|{max <= q} = nu_q, so the owner residual has density D_q(t - q), the others D_q(t)", True,
      "checked by reading (e^gamma z (q/z) = e^gamma q)")

# ---------------------------------------------------------------------------------------------------------------
print("\n[7] authors' script code/third_party/openai186/prime_gap_186_certificate.py (comparison only)")
try:
    pg = load("pg186", os.path.join(HERE, "third_party", "openai186", "prime_gap_186_certificate.py"))
    rk = [t for t in pg.TASKS if t["kind"] == "rank_two"]
    check("authors' TASKS: the same 30 rank-two bins (q_low, q_high) with the same (U, m), same order",
          len(rk) == 30 and all(F(t["parameters"]["q_low"]) == B["a"] and F(t["parameters"]["q_high"]) == B["b"]
                                and F(pg.GROUP_BY_ID[t["source_group_id"]]["ceiling"]) == B["U"]
                                and F(pg.GROUP_BY_ID[t["source_group_id"]]["order"]) == B["m"]
                                for t, B in zip(rk, BINS)))
    src = inspect.getsource(pg.LargestFragmentPalmFactory.kernels)
    check("authors' kernels (source text): caps b^+ (upper grid), r-^- (lower grid), r+^+ (upper grid); shift"
          " max(0, j - ceil(b/h)); lower shift max(0, j+1 - floor(a/h)) only when jh >= b; zero tests t+ <= a and"
          " t+ <= a + r+; distinct difference dup_j(b^+) - dlow_{j+1}(r-^-)",
          "a = self._upper_cap_grid(bin.upper)" in src and "b_low = self._lower_cap_grid(r_min)" in src
          and "b_up = self._upper_cap_grid(r_max)" in src and "shift = max(0, j - q_up)" in src
          and "shift_low = max(0, j + 1 - q_low)" in src and "if j * self.step < bin.upper:" in src
          and "a.upper[j] - b_low.lower[min(j + 1, self.size)]" in src
          and "(j + 1) * self.step <= bin.lower" in src and "(j + 1) * self.step <= same_minimum" in src)
    t7 = time.time()
    ctx.prec = 160
    okk, maxd = True, 0.0
    for bi in (1, 11):                     # O2 P2 (m = 2) and O5/2 P6 (m = 5/2)
        B = BINS[bi]
        fac = pg.LargestFragmentPalmFactory(step=h, reference=[arb(1)] * n, radius=S)
        ker = fac.kernels(pg.LargestFragmentBin(B["a"], B["b"], B["U"], B["m"]))
        mine = arrays(B)
        for row, mrow in zip((ker.ordinary, ker.owner, ker.nonowner_difference, ker.same_owner_difference), mine):
            for j in range(n):
                th = a2F(row[j].upper())
                mi = F(mrow[j], ONE)
                okk &= (th == 0) == (mi == 0)
                dd = abs(th - mi)
                if dd > F(1, 10 ** 35):
                    okk = False
                maxd = max(maxd, float(dd))
    ctx.prec = 200
    check("authors' LargestFragmentPalmFactory.kernels (profile power 0) on O2 P2 and O5/2 P6: the same zero"
          " pattern and |theirs - ours| < 1e-35 on all 4 x %d entries (so our (2.9) reading is theirs)" % n, okk,
          "max |diff| = %s; %.1f s" % (fl(maxd, 3), time.time() - t7))
except Exception as ex:  # pragma: no cover
    ctx.prec = 200
    check("authors' script importable for comparison", False, repr(ex))

# ---------------------------------------------------------------------------------------------------------------
el = time.time() - T_START
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
print("\nruntime %.1f s, peak RSS %.0f MB" % (el, rss))
print("%d checks, %d failures" % (NCHECK[0], len(FAILS)))
for f_ in FAILS:
    print("  FAILED: " + f_)
