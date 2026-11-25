#!/usr/bin/python3
"""Second, independent check of Lemma 1.5 (full-radius factorization) of
OpenAI, "Numerical certificate for prime gaps at most 186" (30 Aug 2026),
code/third_party/openai186/short_gaps_numerics.pdf, p. 10, (1.38).

    W_r = exp(theta*{r h - U + (m-1) u+ + d h}),  u+ = h*ceil(u/h);
    for an erased coordinate of index v use W_{r+v} before summing over it.

Written from the PDF only (no repository code or data). Exact arithmetic only:
fractions.Fraction, sympy (exact symbolic identities), python-flint arb
(rigorous ball enclosures of exponentials).

Parts
  A  rebuild every datum the lemma is applied to ((1.1)-(1.3), (1.13)-(1.18),
     (1.23)-(1.24), §1.5.1 bin lists and slopes) and cross-check printed values;
  B  exact symbolic proof (sympy) for d = 39, 40, including the erased
     coordinate and a negative control;
  C  exact rational cell-level check on all 61 low bins (strided full radial
     range, three index vectors, interior + limiting points, tightness);
  D  end-to-end exact check on random fragment configurations: every witness
     event of (1.36) in a bin is dominated by W_r * exp(-theta L_{<=l});
  E  rigorous arb enclosures of W_r, monotonicity, and the §2.2 side claim
     "exponent less than 700" on a superset of the retained cells.
"""
import math
import random
import sys
import time
from fractions import Fraction as F

import flint
import sympy as sp

T_START = time.time()
NCHK = 0
NFAIL = 0


def check(cond, msg):
    global NCHK, NFAIL
    NCHK += 1
    if not cond:
        NFAIL += 1
        print("FAIL:", msg)


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -((-x.numerator) // x.denominator)


# ---------------------------------------------------------------- Part A ---
print("== Part A: data from the PDF formulas ==")
g0, eps_o, eps_n, tau = F(1, 10**7), F(1, 10**6), F(1, 10**7), F(1, 10**10)
sigma0 = F(100001, 10**6)
sigma_mt = F(1, 2) - F(40481, 100000) + tau
Omega = {"o": F(12499, 10**6), "n": F(253, 20000)}
rho = F(1, 4) + Omega["o"]
rho_s = rho - g0
S = F(2742997, 10**7) / rho_s
T1 = F(251, 1000) / rho_s
T0 = 2 - F(3, 1000) - S
e = g0 / rho
check(rho_s == F(2624989, 10**7) and S == F(2742997, 2624989), "(1.1) S, rho*")
check(T0 == F(2499106033, 2624989000) and T1 == F(2510000, 2624989), "(1.1) T0,T1")
check(rho == F(262499, 10**6), "(1.1) rho")
check(rho_s * S == F(2742997, 10**7) and rho_s * T0 == F(2499106033, 10**10)
      and rho_s * T1 == F(251, 1000), "(1.2) radii")
N = 98304
h = S / N
n = N - 40
Tnu = {"o": T0, "n": T1}
cs = {"o": {1: ((1 - 5 * sigma0) / 15, F(18, 5)), 2: ((1 - 4 * sigma0) / 16, F(7, 2)),
            3: (F(3, 80), F(3))},
      "n": {1: ((1 - 5 * sigma_mt) / 15, F(18, 5)), 2: ((1 - 4 * sigma_mt) / 16, F(7, 2)),
            3: ((1 - 2 * sigma_mt) / 20, F(16, 5))}}
epsn = {"o": eps_o, "n": eps_n}
lad = {}
for nu in "on":
    E = rho * (S + Tnu[nu]) - F(1, 2)
    wprev, rows, t = F(0), [], 0
    while True:
        rt = 1 if t < 12 else (2 if t < 24 else 3)
        c, s_ = cs[nu][rt]
        w = min(Omega[nu], (c - epsn[nu] - E + 2 * wprev - g0) / s_)
        delta = c - s_ * w - epsn[nu]
        B = (F(1, 2) + 2 * wprev) / rho
        xi = delta / rho
        rows.append(dict(t=t, r=rt, w=w, xi=xi, B=B, a=B - Tnu[nu], b=B - S))
        wprev = w
        t += 1
        if w == Omega[nu]:
            break
    lad[nu] = rows
check(len(lad["o"]) == 29 and len(lad["n"]) == 43, "ladder lengths 29, 43")
for nu, cnt in (("o", (12, 12, 5)), ("n", (12, 12, 19))):
    check(tuple(sum(1 for x in lad[nu] if x["r"] == k) for k in (1, 2, 3)) == cnt,
          "order counts " + nu)
X = lambda nu, t: lad[nu][t]
# (1.23)-(1.24): name, d, m, xi, U, b, t, z/h, p/h, domain-of-(1.18)-cap
G = [
    ("O2", 40, F(2), X("o", 23)["xi"], S + e, X("n", 0)["a"], X("n", 24)["a"], 49152, 24576,
     (S + e) / 2),
    ("O5/2", 40, F(5, 2), X("n", 38)["xi"], S + e / 2, X("n", 24)["a"], 98303 * h, 46580, 19660,
     S + e / 2 - 23 * (T1 + e / 2) / 40),
    ("I2old", 39, F(2), X("o", 23)["xi"], T0 + e, X("o", 12)["b"], X("o", 24)["b"], 44781, 22390,
     (T0 + e) / 2),
    ("I5/2old", 39, F(5, 2), X("o", 27)["xi"], T0 + e / 2, X("o", 24)["b"], 89563 * h, 35265, 17912,
     63 * (T0 + e / 2) / 160),
    ("I2new", 39, F(2), X("n", 23)["xi"], T1 + e, X("n", 12)["b"], X("n", 24)["b"], 44976, 22488,
     (T1 + e) / 2),
    ("I5/2new", 39, F(5, 2), X("n", 38)["xi"], T1 + e / 2, X("n", 24)["b"], 89953 * h, 35419, 17990,
     63 * (T1 + e / 2) / 160),
]
for (nm, d, m, xi, U, b, tG, zh, ph, zc) in G:
    check(floor(zc / h) == zh, f"{nm}: floor(cap/h) == printed z/h {zh}")
    check(floor(U / (2 * m * h)) == ph, f"{nm}: p/h = floor(U/(2mh)) == {ph}")
    p = ph * h
    check(2 * h < xi < p <= zh * h, f"{nm}: 2h < xi < p <= z (Lemma 1.1)")
    check(zh * h + m * p <= U, f"{nm}: z + m p <= U (Lemma 1.1)")

a = [F(6, 5) ** j / 20 for j in range(10)]


def blists(xi, p):
    return [
        [xi, 3 * xi / 2, a[0]] + a[4:9] + [(a[8] + a[9]) / 2, a[9], p],
        [2 ** j * xi for j in range(9)] + [F(1, 100), F(3, 200), F(9, 400), F(27, 800)]
        + a[0:8] + [(a[7] + p) / 2, p],
        [xi, a[0], a[4], a[6], a[8], p],
        [xi, 2 * xi, F(1, 100), F(27, 800), a[3], a[5], a[6], p],
        [xi, a[1], a[4], a[5], a[7], a[8], p],
        [2 ** j * xi for j in (0, 1, 4, 6, 8)] + [F(9, 400), a[1], a[3], a[5], a[6], a[7], p],
    ]


BINS = []  # (group index, j, l0, u0, theta)
for gi, (nm, d, m, xi, U, b, tG, zh, ph, zc) in enumerate(G):
    Ul = blists(xi, ph * h)[gi]
    check(all(Ul[k] < Ul[k + 1] for k in range(len(Ul) - 1)), f"{nm}: endpoints increasing")
    check(Ul[0] == xi and Ul[-1] == ph * h, f"{nm}: list runs from xi to p")
    for j in range(1, len(Ul)):
        l0, u0 = Ul[j - 1], Ul[j]
        if gi == 0 and j == 3:
            th = F(120)
        elif gi == 5:
            th = F(ceil(9 / u0))
        else:
            th = F(ceil(7 / u0))
        BINS.append((gi, j, l0, u0, th))
check(len(BINS) == 61, "61 low intervals")
print(f"  rebuilt 6 groups, {len(BINS)} low bins; ladders 29/43 rows")

# ---------------------------------------------------------------- Part B ---
print("== Part B: exact symbolic proof (sympy) ==")
th, hh, UU, mm, uu, up = sp.symbols("theta h U m u u_plus", positive=True)
Lsm = sp.symbols("L_small", nonnegative=True)
for d in (39, 40):
    js = sp.symbols(f"j1:{d + 1}", integer=True, nonnegative=True)
    fs = sp.symbols(f"f1:{d + 1}", nonnegative=True)  # fractional position in [0,1)
    r = sum(js)
    tt = [(js[i] + fs[i]) * hh for i in range(d)]
    s = sum(tt)
    # identity prod_i e^{theta(j_i h - U/d)} = e^{theta(r h - U)} (exponents)
    lhs = sum(th * (js[i] * hh - UU / d) for i in range(d))
    check(sp.expand(lhs - th * (r * hh - UU)) == 0, f"d={d}: product identity")
    Er = th * (r * hh - UU + (mm - 1) * up + d * hh)
    resid = th * (s + (mm - 1) * uu - UU)
    gap = sp.expand(Er - resid - (th * hh * sum(1 - f for f in fs) + th * (mm - 1) * (up - uu)))
    check(gap == 0, f"d={d}: E_r - residual = th h sum(1-f_i) + th (m-1)(u+ - u)")
    # Palm term of (1.37) splits as residual * exp(-theta L_{<=l})
    check(sp.simplify(sp.exp(th * (s + (mm - 1) * uu - UU - Lsm))
                      - sp.exp(resid) * sp.exp(-th * Lsm)) == 0, f"d={d}: Palm split")
    if d == 40:
        # erased coordinate: retained 39 coords with index sum r39, erased index v
        r39, v = sum(js[:39]), js[39]
        Erv = th * ((r39 + v) * hh - UU + (mm - 1) * up + 40 * hh)
        check(sp.expand(Erv - Er) == 0, "erased: W_{r+v} equals W at the full index")
        # negative control: retained-only correction 39h + v h is NOT an upper bound
        # (retained coordinates at their cell suprema f_i -> 1, erased f = 1/2)
        Ebad = th * (r39 * hh - UU + (mm - 1) * up + 39 * hh) + th * v * hh
        sub = {th: 1, hh: 1, UU: 0, mm: 2, uu: 1, up: 1, **{f: 1 for f in fs[:39]}, fs[39]: F(1, 2)}
        sub.update({jj: 0 for jj in js})
        check(sp.nsimplify((Ebad - resid).subs(sub)) < 0, "control: omitting erased cell fails")
# hypotheses that make the gap nonnegative are checked per bin in Part C
print("  identities proved for d=39,40")

# ---------------------------------------------------------------- Part C ---
print("== Part C: exact cell-level check on all 61 bins ==")
rng = random.Random(186015)


def Eexp(gi, th_, u0, r):
    nm, d, m, xi, U, *_ = G[gi]
    upl = h * ceil(u0 / h)
    return th_ * (r * h - U + (m - 1) * upl + d * h)


def vectors(r, d):
    q, rem = divmod(r, d)
    bal = [q + (1 if i < rem else 0) for i in range(d)]
    conc = [r] + [0] * (d - 1)
    cut = sorted(rng.randrange(r + 1) for _ in range(d - 1))
    rnd = [b - a_ for a_, b in zip([0] + cut, cut + [r])]
    return (bal, conc, rnd)


cell_checks = 0
for (gi, j, l0, u0, th_) in BINS:
    nm, d, m, xi, U, b, tG, zh, ph, zc = G[gi]
    upl = h * ceil(u0 / h)
    k = ceil(u0 / h)
    check(th_ > 0 and m - 1 > 0, f"{nm} L{j}: theta>0, m>1")
    check(u0 <= upl < u0 + h and (k - 1) * h < u0, f"{nm} L{j}: u+ least grid point >= u")
    rmax = n - 1
    rs = sorted(set(list(range(0, rmax + 1, 211)) + [0, 1, rmax - 1, rmax]))
    for r in rs:
        Er = Eexp(gi, th_, u0, r)
        check(Er - Eexp(gi, th_, u0, r - 1) == th_ * h if r else True, "affine in r")
        for vec in vectors(r, d):
            assert sum(vec) == r and len(vec) == d
            # factorization identity, computed coordinate by coordinate
            check(sum(th_ * (ji * h - U / d) for ji in vec) == th_ * (r * h - U),
                  f"{nm} L{j} r={r}: identity")
            # supremum of the residual over the cell (t_i -> (j_i+1)h)
            sup = th_ * (sum((ji + 1) * h for ji in vec) + (m - 1) * u0 - U)
            check(Er - sup == th_ * (m - 1) * (upl - u0), f"{nm} L{j} r={r}: tight sup")
            # interior points
            for fr in (F(0), F(1, 2), 1 - F(1, 2 ** 40)):
                ss = sum(ji * h + fr * h for ji in vec)
                check(th_ * (ss + (m - 1) * u0 - U) < Er, f"{nm} L{j} r={r}: strict")
                cell_checks += 1
    if d == 40:  # erased coordinate: r = r39 + v
        for _ in range(60):
            v = rng.randrange(0, 40000)
            r39 = rng.randrange(0, n - v)
            vec = vectors(r39, 39)[2]
            fr = [F(rng.randrange(2 ** 30), 2 ** 30) for _ in range(40)]
            ss = sum((vec[i] + fr[i]) * h for i in range(39)) + (v + fr[39]) * h
            res = th_ * (ss + (m - 1) * u0 - U)
            check(res < Eexp(gi, th_, u0, r39 + v), f"{nm} L{j}: erased W_(r+v)")
            check(Eexp(gi, th_, u0, r39 + v) == Eexp(gi, th_, u0, r39) + th_ * v * h,
                  "erased: W_(r+v) = W_r e^{theta v h}")
print(f"  {cell_checks} exact interior-point cell evaluations")

# ---------------------------------------------------------------- Part D ---
print("== Part D: end-to-end witness events vs W_r exp(-theta L) ==")


def Hfail(frags, m, xi, U, l0, u0):
    """Is there a witness p in (l0,u0], p > xi, with inclusive prefix + (m-1)p > U?"""
    sfr = sorted(frags, reverse=True)
    pref = F(0)
    for i, q in enumerate(sfr):
        pref += q
        # inclusive prefix of p=q counts all equal sizes too
        k = i
        while k + 1 < len(sfr) and sfr[k + 1] == q:
            k += 1
        incl = sum(sfr[: k + 1], F(0))
        if q > xi and l0 < q <= u0 and incl + (m - 1) * q > U:
            return True
    return False


ev = 0
for (gi, j, l0, u0, th_) in BINS:
    nm, d, m, xi, U, *_ = G[gi]
    ell = h * floor(l0 / h)  # kernel cutoff (2.4)
    hit = 0
    for trial in range(400):
        # build fragments: a witness p, some fragments >= p, small fragments
        p = l0 + (u0 - l0) * F(rng.randrange(1, 2 ** 20), 2 ** 20)
        need = U - (m - 1) * p - p  # remaining prefix needed above p
        big = []
        while need > 0 and len(big) < 60:
            q = p + F(rng.randrange(0, 2 ** 20), 2 ** 20) * max(F(1, 10), p)
            big.append(q)
            need -= q
        if rng.random() < 0.5 and big:  # perturb to sit near the boundary
            big[-1] -= F(rng.randrange(0, 2 ** 10), 2 ** 10) * min(-need + F(1, 10**9), big[-1] - p)
        small = [F(rng.randrange(1, 2 ** 20), 2 ** 20) * min(p, F(1, 50)) for _ in range(rng.randrange(0, 40))]
        frags = [p] + big + small
        coords = [[] for _ in range(d)]
        for q in frags:
            coords[rng.randrange(d)].append(q)
        tot = [sum(c, F(0)) for c in coords]
        r = sum(floor(t / h) for t in tot)
        Lsmall = sum((q for q in frags if q <= ell), F(0))
        if Hfail(frags, m, xi, U, l0, u0):
            hit += 1
            # event indicator <= W_r * exp(-theta L_{<=l}) <= Palm sum (1.37)
            check(Eexp(gi, th_, u0, r) - th_ * Lsmall > 0, f"{nm} L{j}: event dominated")
            # and directly (1.36): L_{<=l} < s + (m-1)u - U
            check(Lsmall < sum(tot) + (m - 1) * u0 - U, f"{nm} L{j}: (1.36)")
    ev += hit
    check(hit > 0, f"{nm} L{j}: some witness events generated")
print(f"  {ev} witness events tested")

# ---------------------------------------------------------------- Part E ---
print("== Part E: rigorous arb enclosures; exponent < 700 side claim ==")
flint.ctx.prec = 200
worst = (-10**9, None)
for (gi, j, l0, u0, th_) in BINS:
    nm, d, m, xi, U, b, tG, *_ = G[gi]
    rtop = min(floor(tG / h), n - 1)  # superset of the retained full-cell indices
    Emax = Eexp(gi, th_, u0, rtop)
    if Emax > worst[0]:
        worst = (Emax, (nm, j, rtop))
    W = flint.arb(Emax.numerator) / Emax.denominator
    Wb = W.exp()
    check(Wb.is_finite() and Wb > 0, f"{nm} L{j}: arb W finite")
    # rigorous: W_r dominates exp(residual) at a sample interior point
    Er0 = Eexp(gi, th_, u0, rtop // 2)
    res0 = Er0 - th_ * h * F(1, 3) - th_ * (m - 1) * (h * ceil(u0 / h) - u0)
    A1 = (flint.arb(Er0.numerator) / Er0.denominator).exp()
    A2 = (flint.arb(res0.numerator) / res0.denominator).exp()
    check(A1 > A2, f"{nm} L{j}: arb W_r > exp(residual)")
    check(Emax < 700, f"{nm} L{j}: exponent {float(Emax):.3f} < 700 on superset")
print(f"  largest exponent on superset: {float(worst[0]):.4f} at {worst[1]}")

dt = time.time() - T_START
print(f"\nchecks: {NCHK}   failures: {NFAIL}   run time: {dt:.1f} s")
print("VERDICT: Lemma 1.5 " + ("VERIFIED as stated (under the reading in the note)" if NFAIL == 0
                               else "NOT verified: see FAIL lines"))
