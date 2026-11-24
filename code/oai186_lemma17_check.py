#!/usr/bin/env python3
"""Rung 186: exact check of Lemma 1.7 ("Feasible logarithmic mass", p. 11) of OpenAI's numerical companion [14]
("Numerical certificate for prime gaps at most 186", code/third_party/openai186/short_gaps_numerics.pdf).
Report: notes/oai186-lemma17-check.md.  Modelled on code/oai186_lemma16_check.py.

Lemma 1.7 (p. 11).  In a largest-fragment interval (q-, q+], L := log(q+/q-) and
      Lf(v) := 0 (v <= q-),  log(v/q-) (q- < v < q+),  L (v >= q+).                                   (1.45)
For a physical cell with upper endpoint t+, its largest-fragment coordinate and same-coordinate measures may be
multiplied, respectively, by outward upper bounds for
      Lf(t+)/L ,   Lf((m t+ - U)/(m-1))/L.                                                              (1.46)
The second fraction may also be capped by the first.  Charge the common factor L once.
Proof: a largest fragment requires q < t+; a second fragment on the same coordinate gives t+ > q + (U-q)/m, whence
q < (m t+ - U)/(m-1); integrate dq/q over the feasible parts; the other factors are bounded over the whole
interval; each monomial of (1.43) contains exactly one factor carrying the largest fragment; a positive lower
bound for L is used in the denominator.

Everything that decides a check is exact (fractions.Fraction / int); floats are used only for printing.
Sections:
  [0] group data (m, xi, U, z, p_G, d) from code/oai186_support_data.py; guards used by the lemma
  [1] the 30 rank-two bins of Sec. 1.5.1 (p. 9) (q-, q+]; comparison with the authors' TASKS
  [2] (1.39): d(q) = (U-q)/m on every bin, and (U-q)/m < q, so the lemma's second-fragment bound is d(q) itself
  [3] (1.45): L > 0 for all 30 bins, with rational enclosures from Lemma 2.1's series (positive lower bound)
  [4] all 30 x 98264 (bin, physical cell) pairs: zero / partial / full classes of both fractions; the boundary
      identity at the cutoff; sharpness (an explicit feasible configuration below every cutoff); the cap of the
      second fraction by the first; agreement of the zero sets with Lemma 2.4 / the authors' kernels
  [5] (1.43)/(1.44) in Z[P,A,B,C][x,y]/(x^2,y^2): exact identities for d = 2..40 and the "exactly one factor
      carrying the largest fragment" claim, monomial by monomial
  [6] end-to-end exact test from the definition (1.12) of H_{m,xi}: random and boundary rank-two failing
      configurations lie in the feasible part; negative controls
  [7] authors' script (comparison only)
usage: /usr/bin/python3 code/oai186_lemma17_check.py > code/oai186_lemma17_check.out"""
import os, sys, time, random, importlib.util, io, contextlib, resource, inspect
from fractions import Fraction as F
from math import floor, ceil, gcd

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
    sys.modules[name] = mod                       # lets inspect.getsource find classes
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------------------------------------------
print("[0] group data (1.23)-(1.24), pp. 5-6, from code/oai186_support_data.py (re-derived there from (1.13)-(1.20))")
sd = load("sd186", os.path.join(HERE, "oai186_support_data.py"))
check("oai186_support_data.py: all its printed-value checks pass (ladders, (1.17), masks (1.5), group table)",
      sd.res["all_ok"] is True)
h, S = sd.h, sd.S
N, n = 98304, 98304 - 40
check("(1.3): h = S/98304 with S = 2742997/2624989, n = 98264", h == F(2742997, 2624989 * 98304) and n == 98264)
NAMES = ["O2", "O5/2", "I2old", "I5/2old", "I2new", "I5/2new"]
DIMS = [40, 40, 39, 39, 39, 39]
GR = []
for name, d in zip(NAMES, DIMS):
    m, xi, U, zh, ph = sd.G[name]
    GR.append(dict(name=name, d=d, m=m, xi=xi, U=U, z=zh * h, p=ph * h, q0=U / (m + 1)))
check("m_G in {2, 5/2}; 0 < xi_G < p_G <= z_G < U_G (so U - q > 0 for every q <= z_G)",
      all(G["m"] in (F(2), F(5, 2)) and 0 < G["xi"] < G["p"] <= G["z"] < G["U"] for G in GR))
check("1.5.3 (p. 10): max(p_G, xi_G) <= U_G/(m_G+1) for all six groups",
      all(max(G["p"], G["xi"]) <= G["q0"] for G in GR))
check("Lemma 1.1 guard z_G + m_G p_G <= U_G (used in [2])", all(G["z"] + G["m"] * G["p"] <= G["U"] for G in GR))
check("q0 = U/(m+1) < z_G (the rank-two range (q0, z_G] is nonempty)", all(G["q0"] < G["z"] for G in GR))
for G in GR:
    print("    %-8s d=%d m=%-4s U=%s z=%s p_G=%s q0=%s" % (G["name"], G["d"], G["m"], fl(G["U"], 10), fl(G["z"], 10),
                                                         fl(G["p"], 10), fl(G["q0"], 10)))

# ---------------------------------------------------------------------------------------------------------------
print("\n[1] the 30 rank-two bins (Sec. 1.5.1, p. 9): (q0 + t_{j-1}(z - q0), q0 + t_j(z - q0)]")
TL = [[F(j, 6) for j in range(7)],
      [F(j, 16) for j in range(9)] + [F(5, 8), F(3, 4), F(7, 8), F(1)],
      [F(0), F(1)],
      [F(0), F(1, 2), F(1)],
      [F(0), F(1, 6), F(1, 2), F(2, 3), F(1)],
      [F(0), F(1, 8), F(3, 8), F(1, 2), F(3, 4), F(1)]]
BINS = []
for G, T in zip(GR, TL):
    for j in range(1, len(T)):
        BINS.append(dict(G=G, name="P%d" % j, qm=G["q0"] + T[j - 1] * (G["z"] - G["q0"]),
                         qp=G["q0"] + T[j] * (G["z"] - G["q0"])))
check("bin counts 6, 12, 1, 2, 4, 5 (total 30)", [len(T) - 1 for T in TL] == [6, 12, 1, 2, 4, 5] and len(BINS) == 30)
check("each T list increases strictly from 0 to 1, so the bins partition (q0, z_G]",
      all(T[0] == 0 and T[-1] == 1 and all(T[i] < T[i + 1] for i in range(len(T) - 1)) for T in TL))
check("every bin has 0 < U/(m+1) <= q- < q+ <= z_G < U (the hypotheses of Lemma 2.4, p. 14)",
      all(0 < b["G"]["q0"] <= b["qm"] < b["qp"] <= b["G"]["z"] < b["G"]["U"] for b in BINS))
check("q+/q- in (1, 2] on every bin (so log(q+/q-) needs no binary scaling in Lemma 2.1)",
      all(1 < b["qp"] / b["qm"] <= 2 for b in BINS),
      "max q+/q- = %s" % fl(max(b["qp"] / b["qm"] for b in BINS)))

# ---------------------------------------------------------------------------------------------------------------
print("\n[2] (1.39), p. 10: on (q0, z_G] the second-fragment cutoff d(q) = max{p_G, xi, (U-q)/m} equals (U-q)/m")
# r(q) = (U-q)/m is decreasing, so min over (q0, z] is r(z) = (U-z)/m >= p_G > xi  <=>  z + m p_G <= U.
check("r(z_G) = (U - z_G)/m >= p_G > xi_G, hence d(q) = r(q) for all q <= z_G (dropping p_G, xi in Lemma 2.4"
      " and in the proof of Lemma 1.7 loses nothing on this schedule)",
      all((G["U"] - G["z"]) / G["m"] >= G["p"] > G["xi"] for G in GR),
      "min slack r(z)-p_G = %s" % fl(min((G["U"] - G["z"]) / G["m"] - G["p"] for G in GR)))
check("r(q) < q exactly for q > q0 (r(q0) = q0, r decreasing): a secondary p in (r(q), q] exists on every bin",
      all((G["U"] - G["q0"]) / G["m"] == G["q0"] for G in GR))
check("q + r(q) = ((m-1)q + U)/m is strictly increasing (slope 1 - 1/m > 0) and equals t+ exactly at"
      " q = (m t+ - U)/(m-1) (symbolic in t+, checked at t+ = 0, 1, S)",
      all(1 - 1 / G["m"] > 0 and all((lambda v: v + (G["U"] - v) / G["m"])((G["m"] * tp - G["U"]) / (G["m"] - 1))
                                     == tp for tp in (F(0), F(1), S)) for G in GR))

# ---------------------------------------------------------------------------------------------------------------
print("\n[3] (1.45): L = log(q+/q-) > 0, with the rational series bounds of Lemma 2.1 (p. 11)")


def log_encl(y, M=40):
    """Lemma 2.1 for 1 <= y <= 2: 0 <= log y - 2 sum_{r<M} v^(2r+1)/(2r+1) <= 2 v^(2M+1)/((2M+1)(1-v^2))."""
    assert 1 <= y <= 2
    v = (y - 1) / (y + 1)
    s, pw = F(0), v
    for r in range(M):
        s += pw / (2 * r + 1)
        pw *= v * v
    lo = 2 * s
    return lo, lo + 2 * pw / ((2 * M + 1) * (1 - v * v))


for b in BINS:
    b["Llo"], b["Lhi"] = log_encl(b["qp"] / b["qm"])
check("Lemma 2.1 lower bound for L is > 0 on all 30 bins (positive denominator for the outward fraction)",
      all(b["Llo"] > 0 for b in BINS), "min lower bound %s (%s %s)" % (
          fl(min(b["Llo"] for b in BINS)), *min(((b["Llo"], b["G"]["name"], b["name"]) for b in BINS))[1:]))
check("the enclosures are tight: width < 10^-40 on all 30 bins", all(b["Lhi"] - b["Llo"] < F(1, 10 ** 40) for b in BINS))
check("(1.45) is continuous: log(q-/q-) = 0 exactly (y = 1 gives v = 0) and the middle branch tends to L at q+",
      log_encl(F(1)) == (0, 0))

# ---------------------------------------------------------------------------------------------------------------
print("\n[4] all (bin, physical cell) pairs: 30 bins x %d cells C_j = [jh, (j+1)h), t+ = (j+1)h" % n)
# The fraction Lf(v)/L is 0 iff v <= q-, 1 iff v >= q+, and strictly between iff q- < v < q+.  We classify both
# cutoffs v1 = t+ and v2 = (m t+ - U)/(m-1) on every cell, in scaled integers (each comparison exact).
tot = dict(o0=0, o1=0, op=0, s0=0, s1=0, sp=0)
agree24 = True     # zero sets = Lemma 2.4 indicators 1_{t+ > a}, 1_{t+ > a + r+} (= authors' kernels' zero tests)
capred = True      # Lf(v2) <= Lf(v1) on every cell (cap of the second fraction by the first is redundant)
bound_id = True    # at every partial cell: q* := v2 satisfies q* + r(q*) = t+ exactly (soundness boundary)
sharp_o = sharp_s = True
npart = 0
print("  group    bin   q-            q+            L>=          owner 0/part/1        same 0/part/1")
for b in BINS:
    G = b["G"]
    m, U, qm, qp = G["m"], G["U"], b["qm"], b["qp"]
    a_, b_ = m.numerator, m.denominator           # m = a_/b_
    rplus = (U - qm) / m
    # scale: D = lcm of denominators of h, U, q-, q+, rplus
    D = 1
    for x in (h, U, qm, qp, rplus):
        D = D * x.denominator // gcd(D, x.denominator)
    H_, U_, QM, QP, RP = (int(x * D) for x in (h, U, qm, qp, rplus))
    c = dict(o0=0, o1=0, op=0, s0=0, s1=0, sp=0)
    for j in range(n):
        T = (j + 1) * H_                          # t+ * D
        # owner cutoff v1 = t+
        o = 0 if T <= QM else (1 if T >= QP else 2)
        # same cutoff v2 = (m t+ - U)/(m-1):  v2 <= q-  <=>  a_ T - b_ U <= (a_ - b_) q-
        V2 = a_ * T - b_ * U_                     # (m-1) b_ v2 D
        s = 0 if V2 <= (a_ - b_) * QM else (1 if V2 >= (a_ - b_) * QP else 2)
        c[("o0", "o1", "op")[o]] += 1
        c[("s0", "s1", "sp")[s]] += 1
        # Lemma 2.4: A_j nonzero iff t+ > a ; C_j nonzero iff t+ > a + r+
        agree24 &= (o == 0) == (T <= QM) and (s == 0) == (T <= QM + RP)
        # cap redundancy: order classes; within partial-partial need v2 <= t+
        rank = {0: 0, 2: 1, 1: 2}
        if rank[s] > rank[o]:
            capred = False
        if s == 2 and o == 2 and V2 > (a_ - b_) * T:
            capred = False
        if o == 2 or s == 2:
            npart += 1
            tp = (j + 1) * h
            tm = j * h
            if o == 2:
                # sharpness: q in (q-, t+) feasible as an owner: take q = (q- + t+)/2, t = max(jh, q) in [jh, t+)
                q = (qm + tp) / 2
                t = max(tm, q)
                sharp_o &= qm < q < qp and q <= t < tp and tm <= t
            if s == 2:
                v2 = (m * tp - U) / (m - 1)
                bound_id &= v2 + (U - v2) / m == tp and qm < v2 < qp
                q = (qm + v2) / 2
                r = (U - q) / m
                # secondary p in (r, q] with q + p < t+: p := (r + min(q, t+ - q)) / 2
                p = (r + min(q, tp - q)) / 2
                t = max(tm, q + p)
                sharp_s &= qm < q < qp and r < p <= q and q + p <= t < tp and p > G["p"] and p > G["xi"]
    for k in tot:
        tot[k] += c[k]
    b["cls"] = c
    print("  %-8s %-4s  %-12s  %-12s  %-11s  %6d/%5d/%6d     %6d/%5d/%6d" % (
        G["name"], b["name"], fl(qm, 9), fl(qp, 9), fl(b["Llo"], 6), c["o0"], c["op"], c["o1"], c["s0"], c["sp"], c["s1"]))
check("every (bin, cell) pair classified; totals owner 0/part/1 = %d/%d/%d, same 0/part/1 = %d/%d/%d"
      % (tot["o0"], tot["op"], tot["o1"], tot["s0"], tot["sp"], tot["s1"]),
      tot["o0"] + tot["op"] + tot["o1"] == 30 * n == tot["s0"] + tot["sp"] + tot["s1"])
check("zero sets agree with Lemma 2.4 (p. 14): A_j = 0 iff t+ <= a, C_j = 0 iff t+ <= a + r+ (r+ = (U-a)/m),"
      " on all 30 x 98264 pairs", agree24)
check("soundness boundary: on every partial same-coordinate cell, q* = (m t+ - U)/(m-1) lies in (q-, q+) and"
      " q* + (U - q*)/m = t+ exactly; with [2] (monotone), q + (U-q)/m < t+ <=> q < q*", bound_id)
check("sharpness (owner): on every partial owner cell an explicit q in (q-, t+) and total t in [jh, t+), t >= q, exist",
      sharp_o)
check("sharpness (same): on every partial same cell an explicit q in (q-, q*), p in ((U-q)/m, q] with p > p_G, xi,"
      " and total t in [jh, t+) with t >= q + p exist (so the fraction is the exact projection; it is not lossy)",
      sharp_s)
check("'the second fraction may also be capped by the first' is redundant on this schedule: Lf(v2) <= Lf(t+) on"
      " every pair (v2 <= t+ iff t+ <= U, and t+ > U forces both cutoffs >= q+)", capred)
check("each bin has cells in all three classes for both fractions (the fractions are not trivially 0/1)",
      all(all(b["cls"][k] > 0 for k in b["cls"]) for b in BINS))
print("  info: n h = %s; U_G max = %s; groups with cells t+ > U_G: %s" % (
    fl(n * h, 10), fl(max(G["U"] for G in GR), 10), ",".join(G["name"] for G in GR if n * h > G["U"]) or "none"))
print("  partial (bin, cell) pairs examined with exact Fractions: %d" % npart)

# ---------------------------------------------------------------------------------------------------------------
print("\n[5] (1.42)-(1.44), p. 10: [xy]Q^d in Z[P,A,B,C][x,y]/(x^2, y^2), Q = P + xA + yB + xyC")
# element: dict (ex, ey) -> dict exponent-tuple -> int ; exponent tuple over the variables of VARS
VARS = ("P", "A", "B", "C", "Pr", "xr", "yr", "xyr", "Pe", "Ae", "Be", "Ce")
IX = {v: i for i, v in enumerate(VARS)}


def mono(**kw):
    e = [0] * len(VARS)
    for k, v in kw.items():
        e[IX[k]] = v
    return tuple(e)


def mul(X, Y):
    Z = {}
    for (ax, ay), pa in X.items():
        for (bx, by), pb in Y.items():
            if ax + bx > 1 or ay + by > 1:
                continue
            tgt = Z.setdefault((ax + bx, ay + by), {})
            for ea, ca in pa.items():
                for eb, cb in pb.items():
                    e = tuple(u + v for u, v in zip(ea, eb))
                    tgt[e] = tgt.get(e, 0) + ca * cb
    return {k: {e: c for e, c in v.items() if c} for k, v in Z.items()}


def gen(p, a, b, c):
    return {(0, 0): {mono(**{p: 1}): 1}, (1, 0): {mono(**{a: 1}): 1}, (0, 1): {mono(**{b: 1}): 1},
            (1, 1): {mono(**{c: 1}): 1}}


Q = gen("P", "A", "B", "C")
ok43, okone, pw = True, True, {(0, 0): {mono(): 1}}
for d in range(1, 41):
    pw = mul(pw, Q)
    if d >= 2:
        want = {mono(P=d - 1, C=1): d, mono(P=d - 2, A=1, B=1): d * (d - 1)}
        ok43 &= pw.get((1, 1), {}) == want
        # every monomial of [xy]Q^d: exactly one factor carrying the largest fragment (A or C) and exactly one
        # carrying the secondary (B or C)
        okone &= all(e[IX["A"]] + e[IX["C"]] == 1 and e[IX["B"]] + e[IX["C"]] == 1 for e in pw[(1, 1)])
    if d == 39:
        Q39 = pw
    if d == 40:
        Q40 = pw
check("(1.43) [xy]Q^d = d P^(d-1) C + d(d-1) P^(d-2) A B exactly, for every d = 2..40", ok43)
check("Lemma 1.7 proof: every monomial of [xy]Q^d (d = 2..40) contains exactly one of A, C (the factors carrying"
      " the largest fragment) and exactly one of B, C; so a fraction on A and one on C are never multiplied", okone)
# (1.44): erased coordinate e and a generic retained element R = Pr + x xr + y yr + xy xyr
E = gen("Pe", "Ae", "Be", "Ce")
R = gen("Pr", "xr", "yr", "xyr")
xy = mul(E, R).get((1, 1), {})
want44 = {mono(Ce=1, Pr=1): 1, mono(Pe=1, xyr=1): 1, mono(Ae=1, yr=1): 1, mono(Be=1, xr=1): 1}
check("(1.44) [xy](Q_e R) = C_e P_r + P_e (xy)_r + A_e y_r + B_e x_r for a generic retained R", xy == want44)
check("(1.44): each of the four placements has exactly one largest-fragment carrier (C_e, (xy)_r, A_e or x_r)",
      all(e[IX["Ce"]] + e[IX["xyr"]] + e[IX["Ae"]] + e[IX["xr"]] == 1 for e in xy))
# consistency: with R = Q^39 and the erased coordinate = a 40th copy of Q, (1.44) reproduces (1.43) for d = 40
sub = 0
P39, x39, y39, xy39 = (Q39.get(k, {}) for k in ((0, 0), (1, 0), (0, 1), (1, 1)))


def scal(poly, extra):
    return {tuple(u + v for u, v in zip(e, extra)): c for e, c in poly.items()}


comb = {}
for poly, extra in ((P39, mono(C=1)), (xy39, mono(P=1)), (y39, mono(A=1)), (x39, mono(B=1))):
    for e, c in scal(poly, extra).items():
        comb[e] = comb.get(e, 0) + c
check("(1.44) with R = Q^39 and (P_e, A_e, B_e, C_e) = (P, A, B, C) gives exactly [xy]Q^40 of (1.43)",
      {e: c for e, c in comb.items() if c} == Q40[(1, 1)])

# ---------------------------------------------------------------------------------------------------------------
print("\n[6] end-to-end, from the definition (1.12) of H_{m,xi} (p. 4): rank-two failing configurations")
# A configuration of fragments on d coordinates.  It is a rank-two failure of G if, with q = largest fragment and
# p = second largest, p > p_G, p > xi, q <= z, and p is an H_{m,xi} witness at U: sum_{f >= p} f + (m-1)p > U.
# Then the coordinate of q lies in cell j = floor(t/h) with t+ = (j+1)h; q's bin (q-, q+] must give Lf(t+) > 0
# with q < t+, and if p is in the same coordinate also q < v2 = (m t+ - U)/(m-1).


def Hobs(frags, xi, m):
    best = F(0)
    for p in frags:
        if p > xi:
            best = max(best, sum(f for f in frags if f >= p) + (m - 1) * p)
    return best


print("  info: m_G z_G <= U_G holds for %s; for the others the largest fragment may also be a witness, which is"
      " irrelevant here: the rank-two component covers the witness p = second-largest fragment (reading R2)"
      % ",".join(G["name"] for G in GR if G["m"] * G["z"] <= G["U"]))
rng = random.Random(20261124)


def rq(lo, hi, den=10 ** 9):
    return lo + (hi - lo) * F(rng.randrange(1, den), den)


ntest = lost = same_ct = bnd = 0
lost_ctrl1 = lost_ctrl2 = 0
for it in range(24000):
    G = GR[it % 6]
    m, U = G["m"], G["U"]
    mode = (it // 6) % 4
    q = rq(G["q0"], G["z"])
    r = max((U - q) / m, G["p"])
    if not r < q:
        continue
    if mode == 3:
        p = r + F(1, 10 ** 30)                        # boundary: p just above the cutoff
        bnd += 1
    else:
        p = rq(r, q)
    small = [rq(F(0), min(p, F(1, 50))) for _ in range(rng.randrange(0, 4))]
    same = mode in (1, 3) or rng.random() < 0.3
    # coordinate totals: owner coordinate holds q (+ p if same) + some small fragments (maybe none)
    own_extra = [f for f in small if rng.random() < 0.5] if mode != 3 else []
    t_own = q + (p if same else 0) + sum(own_extra)
    frags = [q, p] + small
    if t_own >= n * h or q + p + sum(small) > S:   # outside the physical grid
        continue
    # rank-two failure per (1.12)
    if not (max(frags) == q and sorted(frags)[-2] == p and p > G["p"] and p > G["xi"] and q <= G["z"]
            and sum(f for f in frags if f >= p) + (m - 1) * p > U and Hobs(frags, G["xi"], m) > U):
        continue
    ntest += 1
    same_ct += same
    j = floor(t_own / h)
    tp = (j + 1) * h
    bb = [b for b in BINS if b["G"] is G and b["qm"] < q <= b["qp"]]
    if len(bb) != 1:
        lost += 1
        continue
    b = bb[0]
    v2 = (m * tp - U) / (m - 1)
    ok = q < tp and b["qm"] < tp and (not same or (q < v2 and b["qm"] < v2))
    lost += not ok
    # negative controls: lower endpoint jh in place of t+; and (U-q)/(m-1)-type cutoff (m-1 -> m) for same
    tm = j * h
    lost_ctrl1 += not (q < tm and (not same or q < (m * tm - U) / (m - 1)))
    lost_ctrl2 += same and not (q < (m * tp - U) / m)
check("every generated rank-two failure (exact rationals, all 6 groups, %d configurations: %d same-coordinate,"
      " %d boundary with p = (U-q)/m + 10^-30) has a unique bin and lies in the feasible part (q < t+, and"
      " q < (m t+ - U)/(m-1) if same-coordinate)" % (ntest, same_ct, bnd), ntest > 15000 and lost == 0,
      "lost %d" % lost)
check("negative controls bite: using the cell's lower endpoint jh for t+ loses configurations; replacing the"
      " divisor m-1 by m in v2 loses same-coordinate configurations", lost_ctrl1 > 0 and lost_ctrl2 > 0,
      "losses %d, %d" % (lost_ctrl1, lost_ctrl2))
# Reading R1 matters: 'physical cell' = cell of the owner coordinate's total INCLUDING q.  If t+ were the upper end
# of the cell of the residual total t - q, the lemma would be false: explicit O_2 configuration.
G = GR[0]
q, p = F(36, 100), F(35, 100)
b = [b for b in BINS if b["G"] is G and b["qm"] < q <= b["qp"]][0]
fr = [q, p]
phys_tp = (floor(q / h) + 1) * h          # owner coordinate holds q alone: total q, residual 0
resid_tp = (floor(0 / h) + 1) * h
check("reading R1 is forced: O_2 configuration q = 0.36 (bin %s) alone in its coordinate, p = 0.35 in another"
      " coordinate is a rank-two failure (p > (U-q)/m, p > p_G, H_2 > U); physical t+ > q- gives a positive"
      " fraction, the residual reading (t+ = h) would give Lf(h)/L = 0 and drop it" % b["name"],
      p > (G["U"] - q) / 2 and G["p"] < p < q <= G["z"] and Hobs(fr, G["xi"], G["m"]) > G["U"]
      and q < phys_tp and b["qm"] < phys_tp and resid_tp <= b["qm"])

# ---------------------------------------------------------------------------------------------------------------
print("\n[7] authors' script code/third_party/openai186/prime_gap_186_certificate.py (comparison only)")
# python-flint is not installed here.  Only Fraction-level module code (the schedule TASKS) and source text are
# used, so a placeholder 'flint' module is injected if the real one is missing; no arb routine is ever called.
if importlib.util.find_spec("flint") is None:
    import types
    _fl = types.ModuleType("flint")
    for _nm in ("arb", "arb_poly", "arb_series", "ctx", "fmpz_poly"):
        setattr(_fl, _nm, type(_nm, (), {}))
    sys.modules["flint"] = _fl
    print("  note: python-flint absent; placeholder module injected (no arb arithmetic is executed)")
try:
    pg = load("pg186", os.path.join(HERE, "third_party", "openai186", "prime_gap_186_certificate.py"))
    rk = [t for t in pg.TASKS if t["kind"] == "rank_two"]
    check("authors' TASKS: the same 30 rank-two bins (q_low, q_high) in the same order",
          len(rk) == 30 and all(F(t["parameters"]["q_low"]) == b["qm"] and F(t["parameters"]["q_high"]) == b["qp"]
                                for t, b in zip(rk, BINS)))
    okg = all(F(pg.GROUP_BY_ID[t["source_group_id"]]["ceiling"]) == b["G"]["U"]
              and F(pg.GROUP_BY_ID[t["source_group_id"]]["order"]) == b["G"]["m"] for t, b in zip(rk, BINS))
    check("authors' rank-two tasks use the same (U_G, m_G)", okg)
    src = inspect.getsource(pg.owner_feasible_mass_fractions)
    src2 = inspect.getsource(pg.LargestFragmentPalmFactory.kernels)
    src3 = inspect.getsource(pg.LargestFragmentBin)
    check("authors' owner_feasible_mass_fractions implements (1.46) with the cap: owner_cap = min(hi, (j+1)h),"
          " same_cap = min(owner_cap, (m right - U)/(m-1)); 0 below lo, 1 above hi (source text)",
          "owner_cap = min(hi, right)" in src and "same_cap = min(owner_cap, (m * right - U) / (m - 1))" in src
          and "if cutoff <= lo:" in src and "if cutoff >= hi:" in src and "denominator.lower() <= 0" in src)
    check("authors' zero tests in LargestFragmentPalmFactory.kernels are t+ <= lower and t+ <= lower + r_max,"
          " i.e. the zero sets checked in [4] (source text)",
          "(j + 1) * self.step <= bin.lower" in src2 and "same_minimum = bin.lower + r_max" in src2
          and "(j + 1) * self.step <= same_minimum" in src2)
    check("authors' common factor: LargestFragmentBin.mass = upper bound of log(upper/lower), applied once as"
          " 'multiplier' per rank-two component (source text; once-ness by reading lines ~2043, 2061, 2121)",
          "log().upper()" in src3 and "multiplier = source.mass" in inspect.getsource(pg))
except Exception as ex:  # pragma: no cover
    check("authors' script importable for comparison", False, repr(ex))

# ---------------------------------------------------------------------------------------------------------------
el = time.time() - T_START
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
print("\nruntime %.1f s, peak RSS %.0f MB" % (el, rss))
print("%d checks, %d failures" % (NCHECK[0], len(FAILS)))
for f_ in FAILS:
    print("  FAILED: " + f_)
