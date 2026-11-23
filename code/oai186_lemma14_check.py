#!/usr/bin/env python3
"""Rung 186: exact check of Lemma 1.4 of OpenAI's numerical companion [14] ("Numerical certificate for prime gaps at
most 186", code/third_party/openai186/short_gaps_numerics.pdf, Sec. 1.5, p. 9) and of the ingredient
max(A_t, C_t) <= 7 L_t / 3 of Lemma 1.1 (p. 6) that it uses.  Report: notes/oai186-lemma14-check.md.

Lemma 1.4 (p. 9).  "After the bounds for the largest fragment and opposite root have been imposed, every retained
order-three failure is a nonlargest H_{5/2} failure at the corresponding threshold."
  phi_D(p) = min(3p/2, L), phi_E(p) = 3p - phi_D(p), L = 23C/40                                       (1.34)
  O_t = {s <= a_t} u {H_{phi_D,xi_t} <= A_t, phi_E(M_{xi_t}) <= C_t}     (outer predicate, order 3, (1.21))
  I_t = {s <= b_t} u {H_{phi_E,xi_t} <= C_t, phi_D(M_{xi_t}) <= A_t}     (inner predicate, order 3, (1.21))
  H_{phi,xi}(X) = max({sum_{q in X, q >= p} q + phi(p) : p in X, p > xi} u {0})   (p. 1),  H_{5/2}: phi(p) = 3p/2.

Everything is exact (fractions.Fraction); no floating point enters any decision.  Sections:
  [0] source data (1.13)-(1.16), retained rows (1.20), recomputed here from the printed rationals;
  [1] Lemma 1.1 ingredients used by Lemma 1.4, row by row: (1.17), eta = xi - e/2 > 0, A + C = B + xi,
      A >= C > L, A <= 11C/10 < 161C/120 = 7L/3;
  [2] the proof's inequalities as homogeneous linear forms in (p, L) (complete proof: value at p = 2L/3 and slope);
  [3] the largest-witness exclusion ("the imposed caps exclude a largest witness"), which the printed proof does not
      spell out: the sharp caps it needs, and that the caps (1.18) and the grid masks (1.5)/(1.19) supply them on the
      whole region where a row can fail;
  [4] containment of each row's reduced event in its group (1.22)-(1.24) (activation, threshold, radial interval),
      plus the absorbed order-two rows (needed for (1.35), not part of Lemma 1.4);
  [5] randomized + adversarial exact-rational test of the full implication on the actual rows, and negative controls
      (caps raised to just above the sharp bound must produce counterexamples);
  [6] consistency with the code: the authors' prime_gap_186_certificate.py (group construction extracted with ast
      and executed: it imports python-flint at top level, which is not installed) and our
      oai186_loss_outer.py / oai186_loss_inner.py group_data(), and the clipping (1.26) with/without absorbed rows.
usage: python3 code/oai186_lemma14_check.py > code/oai186_lemma14_check.out"""
import ast, os, sys, random, math, io, contextlib, importlib.util
from fractions import Fraction as F
from math import floor

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []


def check(name, cond, detail=""):
    print(("  PASS " if cond else "  FAIL ") + name + (("   [" + detail + "]") if detail else ""))
    if not cond:
        FAILS.append(name)


def fl(x):
    return floor(x)


# ---------------------------------------------------------------------------------------------------------------
print("[0] source data (1.13)-(1.16), p. 4; retained rows (1.20), p. 5")
g0, eps = F(1, 10 ** 7), {"o": F(1, 10 ** 6), "n": F(1, 10 ** 7)}
tau = F(1, 10 ** 10)
sigma0, sigmam = F(100001, 10 ** 6), F(1, 2) - F(40481, 100000) + tau
Om = {"o": F(12499, 10 ** 6), "n": F(253, 20000)}
rho = F(1, 4) + Om["o"]
rhos = rho - g0
S = F(2742997, 10 ** 7) / rhos
T1 = F(251, 1000) / rhos
T0 = 2 - F(3, 1000) - S
TT = {"o": T0, "n": T1}
e = g0 / rho
zeta = F(19037, 100000) / rho
N = 98304
h = S / N
cs = {"o": {1: ((1 - 5 * sigma0) / 15, F(18, 5)), 2: ((1 - 4 * sigma0) / 16, F(7, 2)), 3: (F(3, 80), F(3))},
      "n": {1: ((1 - 5 * sigmam) / 15, F(18, 5)), 2: ((1 - 4 * sigmam) / 16, F(7, 2)),
            3: ((1 - 2 * sigmam) / 20, F(16, 5))}}
lad = {}
for nu in ("o", "n"):
    E = rho * (S + TT[nu]) - F(1, 2)
    rows, wp, t = [], F(0), 0
    while True:
        r = 1 if t < 12 else (2 if t < 24 else 3)
        c, sl = cs[nu][r]
        w = min(Om[nu], (c - eps[nu] - E + 2 * wp - g0) / sl)
        delta = c - sl * w - eps[nu]
        B = (F(1, 2) + 2 * wp) / rho
        xi = delta / rho
        a, b = B - TT[nu], B - S
        eta = xi if r <= 2 else (xi + S + TT[nu] - B) / 2
        rows.append(dict(nu=nu, t=t, r=r, w=w, wp=wp, delta=delta, E=E, B=B, xi=xi, a=a, b=b, eta=eta,
                         A=a + eta, C=b + eta, terminal=(w == Om[nu])))
        wp, t = w, t + 1
        if rows[-1]["terminal"]:
            break
    lad[nu] = rows
Sbox, Tbox = 98303 * h, {"o": 89563 * h, "n": 89953 * h}
ret = {nu: [x for x in lad[nu] if x["B"] < Sbox + Tbox[nu]] for nu in lad}
check("ladders have 29 / 43 rows, retained 0..27 / 0..38",
      (len(lad["o"]), len(lad["n"])) == (29, 43) and [x["t"] for x in ret["o"]] == list(range(28))
      and [x["t"] for x in ret["n"]] == list(range(39)))
R3 = [x for nu in ret for x in ret[nu] if x["r"] == 3]          # retained order-three rows
R2 = [x for nu in ret for x in ret[nu] if x["r"] == 2]
R1 = [x for nu in ret for x in ret[nu] if x["r"] == 1]
check("retained order-three rows: old 24..27, new 24..38 (19 rows)",
      [(x["nu"], x["t"]) for x in R3] == [("o", t) for t in range(24, 28)] + [("n", t) for t in range(24, 39)])
check("no retained row is terminal (so (1.17) applies to every retained row)",
      not any(x["terminal"] for nu in ret for x in ret[nu]))

# ---------------------------------------------------------------------------------------------------------------
print("\n[1] Lemma 1.1 ingredients (p. 6) for every retained order-three row")
for x in R3:
    x["L"] = 23 * x["C"] / 40
ok = all(x["delta"] - x["E"] + 2 * x["wp"] == g0 for x in R3)
check("nonterminal identity delta - E + 2 omega_{t-1} = g0 (p. 4)", ok)
check("(1.17): (A_t, C_t) = (S + e/2, T_nu + e/2) exactly",
      all((x["A"], x["C"]) == (S + e / 2, TT[x["nu"]] + e / 2) for x in R3))
check("eta_t = xi_t - e/2 > 0", all(x["eta"] == x["xi"] - e / 2 and x["eta"] > 0 for x in R3))
check("A_t + C_t = B_t + xi_t", all(x["A"] + x["C"] == x["B"] + x["xi"] for x in R3))
check("A_t >= C_t > L_t > 0", all(x["A"] >= x["C"] > x["L"] > 0 for x in R3))
r11 = max(x["A"] / x["C"] for x in R3)
check("A_t <= 11 C_t / 10  (max A/C over rows = %.9f, attained on old rows)" % float(r11), r11 <= F(11, 10))
check("11/10 < 161/120 and 7L/3 = 161C/120 identically", F(11, 10) < F(161, 120) and F(7, 3) * F(23, 40) == F(161, 120))
m7 = min(7 * x["L"] / 3 - max(x["A"], x["C"]) for x in R3)
check("max(A_t, C_t) <= 7 L_t / 3 on every row (min slack %.6f)" % float(m7), m7 >= 0)
print("  data: S+e/2 = %.12f, T0+e/2 = %.12f, T1+e/2 = %.12f, A/C old = %.9f, new = %.9f"
      % (float(S + e / 2), float(T0 + e / 2), float(T1 + e / 2), float((S + e / 2) / (T0 + e / 2)),
         float((S + e / 2) / (T1 + e / 2))))

# ---------------------------------------------------------------------------------------------------------------
print("\n[2] the proof's inequalities, as exact linear forms alpha*p + beta*L (L > 0)")
# A linear form f(p) = al*p + be*L with al > 0 satisfies f > 0 on p > p0 iff f(p0) >= 0.  Here p0 = 2L/3, so the
# test is: al > 0 and al*2/3 + be >= 0 (coefficient of L at p = 2L/3).
P0 = F(2, 3)
forms = {"phi_D-term lower bound 2p + L      minus 7L/3": (F(2), F(1) - F(7, 3)),
         "phi_E-term lower bound 5p - L      minus 7L/3": (F(5), F(-1) - F(7, 3)),
         "balanced term lower bound 7p/2     minus 7L/3": (F(7, 2), -F(7, 3))}
for k, (al, be) in forms.items():
    at = al * P0 + be
    check(k + ": slope %s > 0, value at p = 2L/3 is %s*L (>= 0; = 0 means sharp)" % (al, at), al > 0 and at >= 0)
# phi_D(p) = 3p/2 iff p <= 2L/3: 3p/2 <= L iff p <= 2L/3 (multiply by 2/3 > 0); then phi_E = 3p - 3p/2 = 3p/2.
# For p > 2L/3: phi_D = L, phi_E = 3p - L, and phi_E - 3p/2 = 3p/2 - L > 0, phi_D - 3p/2 = L - 3p/2 < 0.
# Exhaustive check on a fine exact grid of p/L (sanity, the algebra above is the proof):
Lr = F(1)
okD = okE = True
for k in range(0, 3001):
    p = F(k, 1500)                      # p/L in [0, 2]
    phD = min(3 * p / 2, Lr)
    phE = 3 * p - phD
    if (phD == 3 * p / 2) != (p <= P0 * Lr):
        okD = False
    if p <= P0 * Lr and phE != 3 * p / 2:
        okE = False
    if p > P0 * Lr and not (phD == Lr and phE == 3 * p - Lr and phE > 3 * p / 2 > phD):
        okE = False
check("phi_D(p) = 3p/2 exactly when p <= 2L/3 (incl. endpoint p = 2L/3, where phi_D = L = 3p/2)", okD)
check("for p <= 2L/3 also phi_E(p) = 3p/2; for p > 2L/3 phi_D = L < 3p/2 < phi_E = 3p - L", okE)
# Prefix >= 2p for a nonlargest witness: the inclusive prefix contains p and a distinct element q >= p.

# ---------------------------------------------------------------------------------------------------------------
print("\n[3] largest-witness exclusion: sharp caps, and the caps (1.18) / masks (1.5) actually imposed")
# Let M be the (unique) largest fragment, M > xi.  Its own term has prefix M.
#  outer: need M + phi_D(M) <= A and phi_E(M) <= C.
#    M <= 2L/3: 5M/2 <= 5L/3 = 115C/120 < C <= A, and 3M/2 <= L < C: automatic.
#    M >  2L/3: M + L <= A  iff  M <= A - L;   3M - L <= C  iff  M <= (C + L)/3 = 21C/40.
#    So the sharp outer cap is min(A - L, 21C/40); A - L <= 21C/40 iff A <= 11C/10 (Lemma 1.1).
#  inner: need M + phi_E(M) <= C and phi_D(M) <= A.
#    phi_D(M) <= L < C <= A: automatic.
#    M <= 2L/3: 5M/2 <= C iff M <= 2C/5, and 2L/3 = 23C/60 < 2C/5: automatic.
#    M >  2L/3: 4M - L <= C  iff  M <= (C + L)/4 = 63C/160.
check("2L/3 = 23C/60 < 2C/5 and (C+L)/4 = 63C/160 and (C+L)/3 = 21C/40",
      F(2, 3) * F(23, 40) == F(23, 60) < F(2, 5) and (1 + F(23, 40)) / 4 == F(63, 160) and (1 + F(23, 40)) / 3 == F(21, 40))
check("5/2 * 2/3 * 23/40 = 115/120 < 1 (outer, M <= 2L/3 automatic)", F(5, 2) * F(2, 3) * F(23, 40) == F(115, 120) < 1)
zO3 = S + e / 2 - 23 * (T1 + e / 2) / 40            # (1.18) outer cap on (a_{n,24}, S]
zB3 = 63 * (T0 + e / 2) / 160                        # base cap on (b_{o,24}, T0]
zE3 = 63 * (T1 + e / 2) / 160                        # enlarged cap on (b_{n,24}, T1]
zOg, zBg, zEg = 46580 * h, 35265 * h, 35419 * h      # grid-rounded caps of (1.5)
check("grid caps are h*floor(z/h) of (1.18): 46580, 35265, 35419",
      (fl(zO3 / h), fl(zB3 / h), fl(zE3 / h)) == (46580, 35265, 35419))
n24 = lad["n"][24]
o24 = lad["o"][24]
for x in R3:
    x["capO"] = min(x["A"] - x["L"], 21 * x["C"] / 40)
    x["capI"] = 63 * x["C"] / 160
check("outer: zO3 = A_{n,t} - L_{n,t} for every new order-3 row (the cap is attained, sharp)",
      all(zO3 == x["A"] - x["L"] for x in R3 if x["nu"] == "n"))
mo = min(x["capO"] - zO3 for x in R3)
check("outer: zO3 <= min(A_t - L_t, 21C_t/40) for all 19 rows, old rows included (min slack %.3e)" % float(mo), mo >= 0)
oldslack = min(21 * x["C"] / 40 - zO3 for x in R3 if x["nu"] == "o")
check("  in particular for old rows: zO3 <= 21 C_o/40 i.e. 40A <= 23C_n + 21C_o (slack %.3e)" % float(oldslack),
      oldslack >= 0)
check("outer: every order-3 row fails only where the cap holds: a_t >= a_{n,24} for all 19 rows",
      all(x["a"] >= n24["a"] for x in R3), "a_{o,24} - a_{n,24} = %.3e" % float(o24["a"] - n24["a"]))
check("inner old: base cap zB3 = 63 C_t/160 for old order-3 rows and b_{o,t} >= b_{o,24}",
      all(zB3 == x["capI"] and x["b"] >= o24["b"] for x in R3 if x["nu"] == "o"))
check("inner new: enlarged cap zE3 = 63 C_t/160 for new order-3 rows and b_{n,t} >= b_{n,24}",
      all(zE3 == x["capI"] and x["b"] >= n24["b"] for x in R3 if x["nu"] == "n"))
check("inner largest term at the cap is exactly C (equality, non-strict predicate => no failure): 4*63/160 - 23/40 == 1",
      4 * F(63, 160) - F(23, 40) == 1)
# Masks: the cap row of a d-coordinate face starts at j0 = floor(l/h) - d + 1; every cell j < j0 has all totals
# < (j + d) h <= floor(l/h) h <= l, so a configuration outside the capped row has total < l and cannot fail.
for name, l, d, j0 in (("outer", n24["a"], 40, 95599), ("base", o24["b"], 39, 87195), ("enlarged", n24["b"], 39, 87250)):
    check("mask %s: capped row starts at j0 = floor(l/h) - d + 1 = %d and (j0 - 1 + d) h <= l" % (name, j0),
          fl(l / h) - d + 1 == j0 and (j0 - 1 + d) * h <= l)
# new inner rows are also imposed on the base face (L0 = H0 n Lold n Lnew); they are charged in beta_new over
# H1 \ L1, which contains H0 \ L1 because H0 <= H1 (base cap <= enlarged cap on every grid index):
bm = [(0, 84930, 68225), (84931, 87194, 44781), (87195, 89524, 35265)]
em = [(0, 85161, 68225), (85162, 87249, 44976), (87250, 89914, 35419)]
capat = lambda mk, j: next((z for lo, hi, z in mk if lo <= j <= hi), None)
check("H0 <= H1 index-wise: base mask range within enlarged range and base cap <= enlarged cap at every j",
      all(capat(em, j) is not None and capat(bm, j) <= capat(em, j) for j in range(0, 89525)),
      "b_{o,24} - b_{n,24} = %.3e" % float(o24["b"] - n24["b"]))
check("running minimum: zO3 < (S+e)/2 < zeta, zB3 < (T0+e)/2 < zeta, zE3 < (T1+e)/2 < zeta",
      zO3 < (S + e) / 2 < zeta and zB3 < (T0 + e) / 2 < zeta and zE3 < (T1 + e) / 2 < zeta)
# caps on the order-two shells, for completeness of (1.35) (order-two rows, H_2, largest term 2M):
check("order-two shells: 2*(S+e)/2 <= A_t = S+e, 2*(T+e)/2 <= C_t = T+e (largest H_2 term never fails)",
      all(x["A"] == S + e and x["C"] == TT[x["nu"]] + e for x in R2 + R1))
check("caps on the 5/2 shells also exclude a largest H_2 witness: 2 zO3 <= S+e, 2 zB3 <= T0+e, 2 zE3 <= T1+e",
      2 * zO3 <= S + e and 2 * zB3 <= T0 + e and 2 * zE3 <= T1 + e)

# ---------------------------------------------------------------------------------------------------------------
print("\n[4] containment in the groups (1.22)-(1.24), p. 5-6")
GP = {  # name: (m, xi_G, U_G, b_G, t_G, rows, absorbed, kind, max total of the face mask)
    "O2": (F(2), lad["o"][23]["xi"], S + e, lad["n"][0]["a"], n24["a"], [x for x in R1 + R2], [], "outer", 98303 * h),
    "O5/2": (F(5, 2), lad["n"][38]["xi"], S + e / 2, n24["a"], 98303 * h, R3, R1 + R2, "outer", 98303 * h),
    "I2old": (F(2), lad["o"][23]["xi"], T0 + e, lad["o"][12]["b"], o24["b"], [x for x in R2 if x["nu"] == "o"], [],
              "inner", 89563 * h),
    "I5/2old": (F(5, 2), lad["o"][27]["xi"], T0 + e / 2, o24["b"], 89563 * h, [x for x in R3 if x["nu"] == "o"],
                [x for x in R2 if x["nu"] == "o"], "inner", 89563 * h),
    "I2new": (F(2), lad["n"][23]["xi"], T1 + e, lad["n"][12]["b"], n24["b"], [x for x in R2 if x["nu"] == "n"], [],
              "inner", 89953 * h),
    "I5/2new": (F(5, 2), lad["n"][38]["xi"], T1 + e / 2, n24["b"], 89953 * h, [x for x in R3 if x["nu"] == "n"],
                [x for x in R2 if x["nu"] == "n"], "inner", 89953 * h),
}
for g, (m, xiG, UG, bG, tG, rows, absd, kind, smax) in GP.items():
    core, thr = ("a", "A") if kind == "outer" else ("b", "C")
    check("%-8s xi_G <= xi_t, U_G <= threshold_t, b_G <= core_t for its %d own rows" % (g, len(rows)),
          all(xiG <= x["xi"] and UG <= x[thr] and bG <= x[core] for x in rows))
    check("%-8s xi_G = min own xi, U_G = min own threshold, b_G = min own core" % g,
          xiG == min(x["xi"] for x in rows) and UG == min(x[thr] for x in rows) and bG == min(x[core] for x in rows))
    if m == F(5, 2):
        # absorbed order-two rows are charged here only for s > b_G (their own cores are smaller); an H_2 failure
        # at threshold V_t >= U_G with witness p > xi_t >= xi_G is an H_5/2 failure since 3p/2 > p.
        check("%-8s absorbed: xi_G <= xi_t and U_G <= threshold_t for its %d absorbed order-<=2 rows" % (g, len(absd)),
              all(xiG <= x["xi"] and UG <= x[thr] for x in absd))
        check("%-8s face max total (mask (1.5)) <= t_G" % g, smax <= tG)
# (1.35): order-two rows whose failure lies above t_G of their H_2 group are covered by the 5/2 group
check("O2 / I2: t_G of the H_2 group = b_G of the 5/2 group (abutting radial intervals)",
      GP["O2"][4] == GP["O5/2"][3] and GP["I2old"][4] == GP["I5/2old"][3] and GP["I2new"][4] == GP["I5/2new"][3])
check("order-one inner rows: I_t is the whole space (no failure); order-one outer rows in O2",
      all(x["r"] == 1 for x in R1))
check("below the first core no row can fail: outer a_{n,0} <= a_t, inner b_{nu,12} <= b_t (orders 2,3)",
      all(lad["n"][0]["a"] <= x["a"] for x in R1 + R2 + R3)
      and all(lad[x["nu"]][12]["b"] <= x["b"] for x in R2 + R3))

# ---------------------------------------------------------------------------------------------------------------
print("\n[5] randomized and adversarial exact test of the implication on the actual rows")


def Hterm(X, i, phi):
    p = X[i]
    return sum(q for q in X if q >= p) + phi(p)


def phis(L):
    pd = lambda p: min(3 * p / 2, L)
    return pd, (lambda p: 3 * p - pd(p))


def nonlargest(X, i):
    return any(j != i and X[j] >= X[i] for j in range(len(X)))


def run_row(x, kind, cap, xiG, UG, rnd, ntrials, smax):
    """Returns (#failures of the row predicate, #violations of the implication, #violations of 'fail together')."""
    A, C, L, xi = x["A"], x["C"], x["L"], x["xi"]
    pD, pE = phis(L)
    thr, phi = (A, pD) if kind == "outer" else (C, pE)
    special = [L * F(2, 3), cap, xi, (thr - L) / 2, thr / 5, thr * F(2, 7), L / 2, cap / 2]
    nfail = nviol = ntog = 0
    for _ in range(ntrials):
        k = rnd.randint(1, 7)
        X = []
        for _ in range(k):
            mode = rnd.random()
            if mode < 0.35:
                v = rnd.choice(special) + F(rnd.randint(-3, 3), 10 ** 9)
            elif mode < 0.45:
                v = rnd.choice(X) if X else cap
            else:
                v = F(rnd.randint(1, 10 ** 6), 10 ** 6) * cap
            v = min(max(v, F(1, 10 ** 9)), cap)
            X.append(v)
        if sum(X) > smax:
            continue
        idx = [i for i in range(len(X)) if X[i] > xi]
        H = max([Hterm(X, i, phi) for i in idx] + [0])
        M = max([X[i] for i in idx] + [0])
        fail = (H > A or pE(M) > C) if kind == "outer" else (H > C or pD(M) > A)
        concl = any(X[i] > xiG and nonlargest(X, i) and Hterm(X, i, lambda p: 3 * p / 2) > UG
                    for i in range(len(X)))
        nfail += fail
        if fail and not concl:
            nviol += 1
        for i in idx:     # predicates fail together on every nonlargest witness
            if nonlargest(X, i) and ((Hterm(X, i, phi) > thr) != (Hterm(X, i, lambda p: 3 * p / 2) > thr)):
                ntog += 1
    return nfail, nviol, ntog


rnd = random.Random(20261123)
NT = 4000
for kind, rows, capg, gname, smax in (("outer", R3, zOg, "O5/2", 98303 * h),
                                     ("inner", [x for x in R3 if x["nu"] == "o"], zBg, "I5/2old", 89563 * h),
                                     ("inner", [x for x in R3 if x["nu"] == "n"], zEg, "I5/2new", 89953 * h)):
    _, xiG, UG = GP[gname][:3]
    tf = tv = tt = 0
    for x in rows:
        a_, b_, c_ = run_row(x, kind, capg, xiG, UG, rnd, NT, smax)
        tf, tv, tt = tf + a_, tv + b_, tt + c_
    check("%s rows -> %s: %d configurations, %d row failures, 0 not covered by a nonlargest H_5/2 failure"
          % (kind, gname, NT * len(rows), tf) + ("" if tv == 0 else " (got %d)" % tv), tv == 0 and tf > 0)
    check("%s rows: phi-term and H_5/2-term fail together at every nonlargest witness (%d mismatches)" % (kind, tt),
          tt == 0)
# negative controls: with the cap raised just above the sharp bound, a single large fragment is a row failure
# that is NOT a nonlargest failure: the cap hypothesis is necessary and the test can detect its absence.
d = F(1, 10 ** 12)
x = lad["n"][24]
pD, pE = phis(x["L"])
M = x["A"] - x["L"] + d
check("negative control (outer): X = {A-L+1e-12}: H_phiD = M + L > A although no nonlargest witness exists",
      M + pD(M) > x["A"])
x = lad["o"][24]
pD, pE = phis(x["L"])
M = 63 * x["C"] / 160 + d
check("negative control (inner): X = {63C/160+1e-12}: M + phi_E(M) > C although no nonlargest witness exists",
      M + pE(M) > x["C"])
x = lad["o"][24]
pD, pE = phis(x["L"])
M = 21 * x["C"] / 40 + d
check("negative control (outer, opposite root): M = 21C_o/40+1e-12 gives phi_E(M) > C_o (so A-L <= 21C/40 is needed)",
      pE(M) > x["C"])
# tie convention: if the largest value occurs twice, each copy is a 'nonlargest' witness in the sense used here
X = [x["A"] / 3, x["A"] / 3]
check("tie convention: two equal largest fragments count as nonlargest (prefix 2p); ties are nu-null anyway",
      nonlargest(X, 0))

# ---------------------------------------------------------------------------------------------------------------
print("\n[6] consistency with the code")
src = open(os.path.join(HERE, "third_party/openai186/prime_gap_186_certificate.py")).read()
tree = ast.parse(src)
keep = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "DERIVED_INPUTS" for t in node.targets):
        break
    if isinstance(node, (ast.Assign, ast.FunctionDef)):
        keep.append(node)
keep += [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "source_clipped_group"]
ns = {"F": F, "math": math, "__name__": "upstream_extract"}
exec(compile(ast.Module(body=keep, type_ignores=[]), "upstream_extract", "exec"), ns)
U = ns["build_inputs"]()
ug = {g["id"]: g for g in U["source_groups"]}
names = {"outer_h2": "O2", "outer_h25": "O5/2", "old_inner_h2": "I2old", "old_inner_h25": "I5/2old",
         "new_inner_h2": "I2new", "new_inner_h25": "I5/2new"}
check("upstream builds exactly six groups in the order of (1.35)",
      [g["id"] for g in U["source_groups"]] == list(names))
zp = {"O2": (49152, 24576), "O5/2": (46580, 19660), "I2old": (44781, 22390), "I5/2old": (35265, 17912),
      "I2new": (44976, 22488), "I5/2new": (35419, 17990)}
for uid, g in names.items():
    m, xiG, UG, bG, tG, rows, absd, kind, smax = GP[g]
    u = ug[uid]
    rowset = sorted((("o" if r["ladder"] == "old" else "n"), r["index"]) for r in u["source_rows"])
    check("upstream %-14s = %-8s: m, xi, U, b_G, t_G, z_G, p_G, source rows (1.22), nonlargest=True" % (uid, g),
          F(u["order"]) == m and F(u["activation"]) == xiG and F(u["ceiling"]) == UG and F(u["radial_lower"]) == bG
          and F(u["radial_upper"]) == tG and F(u["hard_cap"]) == zp[g][0] * h and F(u["split"]) == zp[g][1] * h
          and rowset == sorted((x["nu"], x["t"]) for x in rows) and u["nonlargest"] is True,
          "radial_upper=%s" % ("maximum of face" if F(u["radial_upper"]) == smax else "core"))
check("upstream order-3 rows carry owner_plateau = 23C/40 = L_t",
      all(F(r["owner_plateau"]) == 23 * F(r["C"]) / 40 for lname in ("old", "new")
          for r in U["source_ladders"][lname] if r["source_order"] == 3))
# our evaluators' group_data (extracted with ast; the modules import python-flint at top level)
spec = importlib.util.spec_from_file_location("sd", os.path.join(HERE, "oai186_support_data.py"))
sd = importlib.util.module_from_spec(spec)
old_argv = sys.argv
sys.argv = ["x"]
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(sd)
sys.argv = old_argv
check("oai186_support_data ladders agree with section [0] (xi, a, b, A, C of every row)",
      all(sd.ladders[nu][i][k] == lad[nu][i][k] for nu in lad for i in range(len(lad[nu]))
          for k in ("xi", "a", "b", "A", "C")))
for fname in ("oai186_loss_outer.py", "oai186_loss_inner.py"):
    t2 = ast.parse(open(os.path.join(HERE, fname)).read())
    fn = [n for n in t2.body if isinstance(n, ast.FunctionDef) and n.name in ("group_data", "clip_lower")]
    ns2 = {"Fr": F, "floor": floor}
    exec(compile(ast.Module(body=fn, type_ignores=[]), fname, "exec"), ns2)
    G2 = ns2["group_data"](sd)
    for g, x2 in G2.items():
        m, xiG, UG, bG, tG, rows, absd, kind, smax = GP[g]
        same = (x2["m"] == m and x2["xi"] == xiG and x2["U"] == UG and x2["b"] == bG and x2["t"] == tG
                and (x2["z"], x2["p"]) == zp[g]
                and sorted((r["t"], r["xi"]) for r in x2["rows"]) == sorted((r["t"], r["xi"]) for r in rows)
                and sorted((r["t"], r["xi"]) for r in x2["absorbed"]) == sorted((r["t"], r["xi"]) for r in absd))
        check("%s group_data[%s] = (1.22)-(1.24) incl. own and absorbed rows" % (fname, g), same)
    # clipping (1.26) at every low-bin end, ours (with absorbed rows, own order) vs upstream (own rows, order m_G)
    nU = nd = 0
    for g, x2 in G2.items():
        ug_ = ug[[k for k, v in names.items() if v == g][0]]
        for u in x2["ulist"][1:]:
            if fname.endswith("outer.py"):
                ours, _ = ns2["clip_lower"](x2, u)
            else:
                ours, _ = ns2["clip_lower"](x2, u, h)
            up = ns["source_clipped_group"](ug_, h, u)
            upc = None if up is None else F(up["radial_lower"])
            nU += 1
            if ours != upc:
                nd += 1
                print("    clip differs: %s u=%s ours=%s upstream=%s" % (g, float(u), ours, upc))
    check("%s: clipped lower boundary (1.26) equals upstream's at all %d low-bin ends" % (fname, nU), nd == 0)

print("\nSUMMARY: %d check(s) failed%s" % (len(FAILS), (": " + "; ".join(FAILS)) if FAILS else ""))
sys.exit(1 if FAILS else 0)
