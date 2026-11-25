#!/usr/bin/env python3
"""Second, independent check of Lemma 1.7 of the OpenAI preprint
"Numerical certificate for prime gaps at most 186" (30 Aug 2026),
code/third_party/openai186/short_gaps_numerics.pdf, p. 11.

Lemma 1.7 (Feasible logarithmic mass): in a largest-fragment interval
(q-, q+], with L := log(q+/q-) and the clipped log L(v) of (1.45), the
largest-fragment coordinate measure and the same-coordinate measure of a
physical cell with upper endpoint t+ may be multiplied by outward upper bounds
for L(t+)/L and L((m t+ - U)/(m-1))/L (1.46); the second may be capped by the
first; the common factor L is charged once.

Written from the PDF only (no repository code or data).  Decisions are exact
(fractions.Fraction / int); python-flint arb balls give rigorous enclosures
of the logarithms.

Parts (see notes/oai186-lemma17-check2.md):
  A  recompute the six groups' (m, U, z, p_G, xi) from (1.13)-(1.24).
  B  build the 30 rank-two bins from T1..T6 (p. 9) and check the hypotheses
     the lemma and Lemma 2.4 use: U/(m+1) <= q- < q+ <= z < U,
     max(p_G, xi) <= U/(m+1), tiling of (q0, z], L > 0.
  C  exhaustive exact feasibility on every cell j < N of every bin: the set
     of largest-fragment sizes q in (q-, q+] compatible with a coordinate
     total t < t+ = (j+1)h (resp. with a second fragment p, (U-q)/m < p <= q,
     in the same coordinate) is computed directly from the constraints and
     compared with the clipped arguments in (1.46); also the indicator forms
     of (2.9) and the lambda form of Lemma 2.4, and the capping claim.
  D  arb enclosures (160 bits) of both fractions on every cell where they
     are strictly between 0 and 1: rigorous 0 < f < 1 and f2 <= f1, rational
     outward upper bounds; independent cross-checks of the logarithmic mass
     on sampled cells by (i) rigorous arb quadrature of dq/q over the exact
     feasible set and (ii) exact rational Riemann-sum brackets.
  E  the algebra behind "charge L once": [xy](P+xA+yB+xyC)^d (1.43) and the
     erased-coordinate split (1.44) for d <= 40, and that every monomial
     carries exactly one largest-fragment factor (A or C).
"""
import random
import resource
import sys
import time
from fractions import Fraction as Fr

import flint
import sympy as sp

T_WALL = time.time()
NCHECK = 0
NFAIL = 0


def check(cond, msg):
    global NCHECK, NFAIL
    NCHECK += 1
    if not cond:
        NFAIL += 1
        print("FAIL:", msg)


def out(*a):
    print(*a)
    sys.stdout.flush()


def floor(x):
    x = Fr(x)
    return x.numerator // x.denominator


# ------------------------------------------------------------------ Part A
out("== Part A: group parameters ==")
g0 = Fr(1, 10**7)
eps = {"o": Fr(1, 10**6), "n": Fr(1, 10**7)}
tau = Fr(1, 10**10)
sig0 = Fr(100001, 10**6)
sigm = Fr(1, 2) - Fr(40481, 100000) + tau
Om = {"o": Fr(12499, 10**6), "n": Fr(253, 20000)}
rho = Fr(1, 4) + Om["o"]
rhos = rho - g0
S = Fr(2742997, 10**7) / rhos
T1 = Fr(251, 1000) / rhos
T0 = 2 - Fr(3, 1000) - S
e = g0 / rho
Tnu = {"o": T0, "n": T1}
N = 98304
h = S / N
coef = {
    "o": {1: ((1 - 5 * sig0) / 15, Fr(18, 5)), 2: ((1 - 4 * sig0) / 16, Fr(7, 2)), 3: (Fr(3, 80), Fr(3))},
    "n": {1: ((1 - 5 * sigm) / 15, Fr(18, 5)), 2: ((1 - 4 * sigm) / 16, Fr(7, 2)),
          3: ((1 - 2 * sigm) / 20, Fr(16, 5))},
}
XI = {}
for nu in "on":
    E = rho * (S + Tnu[nu]) - Fr(1, 2)
    wp, t = Fr(0), 0
    while True:
        r = 1 if t < 12 else 2 if t < 24 else 3
        c, s_ = coef[nu][r]
        w = min(Om[nu], (c - eps[nu] - E + 2 * wp - g0) / s_)
        XI[(nu, t)] = (c - s_ * w - eps[nu]) / rho
        if w == Om[nu]:
            break
        wp, t = w, t + 1
check(len([k for k in XI if k[0] == "o"]) == 29 and len([k for k in XI if k[0] == "n"]) == 43, "ladders 29/43")
GROUPS = [  # name, d, m, U, z/h, p/h, xi   from (1.23)-(1.24)
    ("O2", 40, Fr(2), S + e, 49152, 24576, XI[("o", 23)]),
    ("O52", 40, Fr(5, 2), S + e / 2, 46580, 19660, XI[("n", 38)]),
    ("I2old", 39, Fr(2), T0 + e, 44781, 22390, XI[("o", 23)]),
    ("I52old", 39, Fr(5, 2), T0 + e / 2, 35265, 17912, XI[("o", 27)]),
    ("I2new", 39, Fr(2), T1 + e, 44976, 22488, XI[("n", 23)]),
    ("I52new", 39, Fr(5, 2), T1 + e / 2, 35419, 17990, XI[("n", 38)]),
]
for (nm, d, m, U, zh, ph, xi) in GROUPS:
    check(floor(U / (2 * m * h)) == ph, f"{nm}: p_G/h = floor(U/(2mh))")
    out(f"{nm:7s} m={m} U={float(U):.9f} z={float(zh * h):.9f} p_G={float(ph * h):.9f} xi={float(xi):.4e}")

# ------------------------------------------------------------------ Part B
out("\n== Part B: the rank-two bins ==")
TL = [
    [Fr(j, 6) for j in range(7)],
    [Fr(j, 16) for j in range(9)] + [Fr(5, 8), Fr(3, 4), Fr(7, 8), Fr(1)],
    [Fr(0), Fr(1)],
    [Fr(0), Fr(1, 2), Fr(1)],
    [Fr(0), Fr(1, 6), Fr(1, 2), Fr(2, 3), Fr(1)],
    [Fr(0), Fr(1, 8), Fr(3, 8), Fr(1, 2), Fr(3, 4), Fr(1)],
]
BINS = []
flint.ctx.prec = 160
for gi, (nm, d, m, U, zh, ph, xi) in enumerate(GROUPS):
    z = zh * h
    q0 = U / (m + 1)
    T = TL[gi]
    check(T[0] == 0 and T[-1] == 1 and all(T[i] < T[i + 1] for i in range(len(T) - 1)), f"{nm}: T list")
    check(max(ph * h, xi) <= q0, f"{nm}: max(p_G, xi) <= U/(m+1)")
    check(q0 < z < U, f"{nm}: U/(m+1) < z < U")
    prev = q0
    for k in range(1, len(T)):
        a = q0 + T[k - 1] * (z - q0)
        b = q0 + T[k] * (z - q0)
        check(a == prev, f"{nm} bin {k}: tiles (q0, z]")
        prev = b
        check(q0 <= a < b <= z < U, f"{nm} bin {k}: U/(m+1) <= a < b <= z < U")
        # on (a, b]: (U-q)/m < q (so d(q) < q), r(q) in [r-, r+]
        check((U - a) / m <= a, f"{nm} bin {k}: r(a) <= a")
        Lam = (flint.arb(b.numerator) * a.denominator / (flint.arb(b.denominator) * a.numerator)).log()
        lo = Lam.mid() - Lam.rad()
        check(lo > 0, f"{nm} bin {k}: L > 0 (rigorous)")
        BINS.append(dict(g=nm, k=k, m=m, U=U, a=a, b=b, z=z, Lam=Lam))
    check(prev == z, f"{nm}: bins end at z")
out(f"bins per group: {[len(T) - 1 for T in TL]}, total {len(BINS)}")
check(len(BINS) == 30, "30 rank-two bins")
for B in BINS:
    out(f"  {B['g']:7s} bin {B['k']:2d}: ({float(B['a']):.9f}, {float(B['b']):.9f}]  L = {B['Lam'].str(8)}")

# ------------------------------------------------------------------ Part C
out("\n== Part C: exhaustive exact feasibility per cell ==")


def clip(v, a, b):
    return min(max(v, a), b)


totals = dict(cells=0, f1_mid=0, f2_mid=0, f1_zero=0, f1_one=0, f2_zero=0, f2_one=0)
MID = []  # (bin index, j) where some fraction is strictly between 0 and 1
for bi, B in enumerate(BINS):
    m, U, a, b = B["m"], B["U"], B["a"], B["b"]
    # work in units of h: tau = t+/h = j+1 integer; all comparisons exact
    Ah, Bh, Uh = a / h, b / h, U / h
    rplus = (U - a) / m
    for j in range(N):
        tp = j + 1  # t+ / h
        totals["cells"] += 1
        # --- direct feasibility, largest fragment in this coordinate: q <= t < t+ and q in (a,b]
        # feasible set = (a, min(b, t+)) (q < t+ strictly), empty if t+ <= a
        if tp <= Ah:
            e1 = None
        else:
            e1 = min(Bh, Fr(tp))
        # --- direct feasibility, second fragment p in the same coordinate:
        # need p with (U-q)/m < p <= q and q + p <= t < t+.  Evaluate the constraint
        # g(q) := (t+ - q) - (U - q)/m  (> 0 needed) at the bin ends, g is affine in q.
        g = lambda q: (tp - q) - (Uh - q) / m  # noqa: E731  (units of h)
        slope = g(Fr(1)) - g(Fr(0))
        check(slope < 0, "g strictly decreasing in q")
        # q in (a, b] with g(q) > 0 (and (U-q)/m < q, true on the bin)
        if g(Ah) <= 0:
            e2 = None  # g(q) < g(a) <= 0 for q > a
        else:
            root = Ah + g(Ah) / (-slope)  # exact root of the affine g
            check(g(root) == 0, "exact root")
            e2 = min(Bh, root)
        # --- formula (1.46): arguments t+ and w := (m t+ - U)/(m-1), clipped to [a, b]
        w = (m * tp - Uh) / (m - 1)
        c1 = clip(Fr(tp), Ah, Bh)
        c2 = clip(w, Ah, Bh)
        check((e1 is None and c1 == Ah) or (e1 is not None and e1 == c1), f"bin {bi} j {j}: largest-fragment set")
        check((e2 is None and c2 == Ah) or (e2 is not None and e2 == c2), f"bin {bi} j {j}: same-coordinate set")
        # indicators in (2.9): 1{t+ > a} and 1{t+ > a + r+}
        check((tp > Ah) == (c1 > Ah), "indicator t+ > a  <=>  L(t+) > 0")
        check((tp > (a + rplus) / h) == (c2 > Ah), "indicator t+ > a + r+  <=>  L(w) > 0")
        # Lemma 2.4 lambda form of the second fraction uses min{t+, w}; capping by the first:
        check(clip(min(Fr(tp), w), Ah, Bh) == min(c1, c2), "lambda(min{t+,w}) = min of the two fractions")
        if tp * h > U:
            check(c1 == Bh and c2 == Bh, "t+ > U: both fractions equal 1")
        else:
            check(w <= tp, "t+ <= U: w <= t+ so second <= first")
        z1, o1 = c1 == Ah, c1 == Bh
        z2, o2 = c2 == Ah, c2 == Bh
        totals["f1_zero"] += z1
        totals["f1_one"] += o1
        totals["f2_zero"] += z2
        totals["f2_one"] += o2
        if not (z1 or o1) or not (z2 or o2):
            MID.append((bi, j, c1, c2))
            totals["f1_mid"] += not (z1 or o1)
            totals["f2_mid"] += not (z2 or o2)
out("cell classification over all bins:", totals)

# ------------------------------------------------------------------ Part D
out("\n== Part D: arb enclosures (160 bits) and independent log-mass cross-checks ==")


def arb_fr(x):
    return flint.arb(x.numerator) / x.denominator


def fr_up(x):
    mn, ex = x.upper().man_exp()
    return Fr(int(mn)) * Fr(2) ** int(ex)


def fr_lo(x):
    mn, ex = x.lower().man_exp()
    return Fr(int(mn)) * Fr(2) ** int(ex)


nenc = 0
n_ub_above_one = 0
max_ub_excess = Fr(0)
for (bi, j, c1, c2) in MID:
    B = BINS[bi]
    Ah = B["a"] / h
    Lam = B["Lam"]
    Llo = fr_lo(Lam)  # positive rational lower bound for L (checked > 0 in Part B)
    check(Llo > 0, "rational lower bound for L positive")
    f = []
    for c in (c1, c2):
        num = arb_fr(c / Ah).log()  # log(v/a), v in [a,b]
        val = num / Lam
        f.append(val)
        if Ah < c < B["b"] / h:
            # rigorous: strictly between 0 and 1
            check(val > 0 and val < 1, f"bin {bi} j {j}: 0 < fraction < 1 rigorously")
            # exact rational outward upper bound: upper(log) / lower(L)
            ub = fr_up(num) / Llo
            check(ub > 0 and not (val > arb_fr(ub)), "rational outward upper bound >= fraction")
            if ub > 1:
                n_ub_above_one += 1
            # the upper bound is tight: excess over the arb lower endpoint
            max_ub_excess = max(max_ub_excess, ub - fr_lo(val))
        nenc += 1
    check(not (f[1] > f[0]), f"bin {bi} j {j}: second fraction <= first (rigorous)")
out(f"rational outward upper bounds > 1 (to be clipped at 1): {n_ub_above_one}; "
    f"max width of [lower, outward upper] = {float(max_ub_excess):.2e}")
out(f"arb-enclosed fractions: {nenc} on {len(MID)} cells")

# independent cross-checks of the feasible log-mass on sampled cells
rng = random.Random(1867)
sample = []
by_bin = {}
for item in MID:
    by_bin.setdefault(item[0], []).append(item)
for bi, items in by_bin.items():
    pick = [items[0], items[-1], items[len(items) // 2]] + [rng.choice(items) for _ in range(5)]
    sample.extend(pick)
flint.ctx.prec = 100
nq = 0
for (bi, j, c1, c2) in sample:
    B = BINS[bi]
    a = B["a"]
    for c in (c1, c2):
        v = c * h
        if v == a:
            continue
        # (i) rigorous arb quadrature of the measure dq/q on the exact feasible set (a, v)
        I = flint.acb.integral(lambda q, an: 1 / q, arb_fr(a), arb_fr(v)).real
        closed = (arb_fr(v) / arb_fr(a)).log()
        check(I.overlaps(closed), f"bin {bi} j {j}: quadrature overlaps closed form")
        # (ii) exact Riemann bracket: sum D/x_{i+1} <= int_a^v dq/q <= sum D/x_i
        n = 64
        D = (v - a) / n
        lo = sum(D / (a + (i + 1) * D) for i in range(n))
        hi = sum(D / (a + i * D) for i in range(n))
        check(lo < hi, "bracket ordered")
        check(not (closed < arb_fr(lo)) and not (closed > arb_fr(hi)), f"bin {bi} j {j}: log within exact bracket")
        # and the fraction bracket from (ii) lies in [0, 1] and contains the arb fraction
        Lhi = sum((B["b"] - a) / n / (a + i * (B["b"] - a) / n) for i in range(n))
        check(lo / Lhi >= 0 and lo / Lhi <= 1, "rational lower bracket of the fraction in [0,1]")
        nq += 1
flint.ctx.prec = 160
out(f"sampled log-mass cross-checks: {nq} (quadrature + exact Riemann bracket)")

# ------------------------------------------------------------------ Part E
out("\n== Part E: (1.43)/(1.44) -- one largest-fragment factor per monomial ==")
P, A, Bs, C, Pe, Ae, Be, Ce = sp.symbols("P A B C P_e A_e B_e C_e")


def mul(u, v):
    """product in R[x,y]/(x^2,y^2); elements as (c1, cx, cy, cxy)."""
    return (sp.expand(u[0] * v[0]), sp.expand(u[0] * v[1] + u[1] * v[0]), sp.expand(u[0] * v[2] + u[2] * v[0]),
            sp.expand(u[0] * v[3] + u[3] * v[0] + u[1] * v[2] + u[2] * v[1]))


Qc = (P, A, Bs, C)
Qe = (Pe, Ae, Be, Ce)
pw = (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0))
for dd in range(1, 41):
    pw = mul(pw, Qc)
    xy = pw[3]
    check(sp.expand(xy - (dd * P**(dd - 1) * C + dd * (dd - 1) * P**(dd - 2) * A * Bs)) == 0, f"(1.43) d={dd}")
    for mono in sp.Poly(xy, P, A, Bs, C).monoms():
        check(mono[1] + mono[3] == 1, f"d={dd}: one largest-fragment factor")
        check(mono[2] + mono[3] == 1, f"d={dd}: one secondary factor")
    if dd in (1, 2, 3, 38, 39):
        r = dd
        full = mul(Qe, pw)[3]
        rhs = Ce * pw[0] + Pe * pw[3] + Ae * pw[2] + Be * pw[1]
        check(sp.expand(full - rhs) == 0, f"(1.44) r={r}")
        for mono in sp.Poly(full, P, A, Bs, C, Pe, Ae, Be, Ce).monoms():
            check(mono[1] + mono[3] + mono[5] + mono[7] == 1, f"(1.44) r={r}: one largest-fragment factor")
# derivation step: t+ > q + (U-q)/m  <=>  q < (m t+ - U)/(m-1), for m in {2, 5/2}
q, tp_, U_ = sp.symbols("q t U", positive=True)
for mm in (sp.Integer(2), sp.Rational(5, 2)):
    lhs = tp_ - (q + (U_ - q) / mm)
    rhs = ((mm * tp_ - U_) / (mm - 1) - q)
    ratio = sp.simplify(lhs / rhs)
    check(ratio.is_number and ratio > 0, f"m={mm}: equivalence factor {ratio} > 0")
    check(sp.simplify(sp.diff(q + (U_ - q) / mm, q)) > 0, f"m={mm}: q + r(q) increasing")
out("(1.43) checked for d = 1..40, (1.44) for r in {1,2,3,38,39}")

mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
out("\n== summary ==")
out(f"checks {NCHECK}, failures {NFAIL}, runtime {time.time() - T_WALL:.1f} s, peak RSS {mem:.0f} MB")
