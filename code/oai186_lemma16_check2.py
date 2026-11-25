#!/usr/bin/env python3
"""Second, independent check of Lemma 1.6 of the OpenAI preprint
"Numerical certificate for prime gaps at most 186" (30 Aug 2026),
code/third_party/openai186/short_gaps_numerics.pdf, p. 10.

Lemma 1.6 (Containment of the low-witness intervals): "The radial restrictions
in (1.26), applied to the displayed 61 low intervals, retain every source
failure assigned to those intervals."  Its proof adds a "direct check":
of the 40 order-5/2 low intervals the first 11, 2, 5 (outer, old-inner,
new-inner) end below every absorbed order-two activation; on the remaining
11, 5, 6 the order-three minimum equals the group's lower radial boundary;
each of the 61 intervals is nonempty on the grid.

Written from the PDF only (no repository code or data).  Exact rational
arithmetic (fractions.Fraction / int) for every decision.

Parts (see notes/oai186-lemma16-check2.md):
  A  recompute the source ladders, rows, groups (1.13)-(1.24) and cross-check
     the printed numbers used (row counts, (1.17), masks (1.5), (1.24)).
  B  build the 61 low intervals from the lists U1..U6 (p. 9) and evaluate
     (1.26) -> retained index range; check the "direct check" counts and
     grid nonemptiness.
  C  exhaustive cell-by-cell search: for every group, interval, eligible row
     and every index sum j of the group's mask range, decide exactly whether
     a failure with a witness in the interval can have a total inside the
     cell (j h <= s < (j+d) h), WITHOUT using (1.26); every such j must be
     retained by (1.26).
  D  explicit configurations: build concrete fragment multisets on d
     coordinates, evaluate the literal predicates (1.21) / obstructions
     (1.12), confirm a failure with a witness in the interval, compute the
     cell index sum Sum floor(t_i/h), and check it is retained.  Adversarial
     (grid-aligned) placements measure how sharp the restriction is.
"""
import random
import resource
import sys
import time
from fractions import Fraction as Fr

T0_WALL = time.time()
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


def ceil(x):
    x = Fr(x)
    return -((-x.numerator) // x.denominator)


# ------------------------------------------------------------------ Part A
out("== Part A: source data (1.13)-(1.24) ==")
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
zeta = Fr(19037, 100000) / rho
Tnu = {"o": T0, "n": T1}
check(S == Fr(2742997, 2624989) and T1 == Fr(2510000, 2624989)
      and T0 == Fr(2499106033, 2624989000) and rho == Fr(262499, 10**6), "(1.1)")
N = 98304
h = S / N
NMAX = 98263

coef = {
    "o": {1: ((1 - 5 * sig0) / 15, Fr(18, 5)), 2: ((1 - 4 * sig0) / 16, Fr(7, 2)), 3: (Fr(3, 80), Fr(3))},
    "n": {1: ((1 - 5 * sigm) / 15, Fr(18, 5)), 2: ((1 - 4 * sigm) / 16, Fr(7, 2)),
          3: ((1 - 2 * sigm) / 20, Fr(16, 5))},
}


def rord(t):
    return 1 if t < 12 else 2 if t < 24 else 3


ROWS = {}
for nu in "on":
    E = rho * (S + Tnu[nu]) - Fr(1, 2)
    wp = Fr(0)
    t = 0
    while True:
        r = rord(t)
        c, s_ = coef[nu][r]
        w = min(Om[nu], (c - eps[nu] - E + 2 * wp - g0) / s_)
        dl = c - s_ * w - eps[nu]
        B = (Fr(1, 2) + 2 * wp) / rho
        xi = dl / rho
        a = B - Tnu[nu]
        b = B - S
        eta = xi if r <= 2 else (xi + S + Tnu[nu] - B) / 2
        ROWS[(nu, t)] = dict(nu=nu, t=t, r=r, w=w, wp=wp, dl=dl, B=B, xi=xi, a=a, b=b,
                             A=a + eta, C=b + eta, E=E, term=(w == Om[nu]))
        if w == Om[nu]:
            break
        wp = w
        t += 1
nrows = {nu: sum(1 for k in ROWS if k[0] == nu) for nu in "on"}
check(nrows == {"o": 29, "n": 43}, f"ladder lengths {nrows}")
Sbox, Tbox = 98303 * h, {"o": 89563 * h, "n": 89953 * h}
RET = {k for k, R in ROWS.items() if R["B"] < Sbox + Tbox[k[0]]}
check(RET == {("o", t) for t in range(28)} | {("n", t) for t in range(39)}, "retained rows (1.20)")
for k in RET:
    R = ROWS[k]
    check(not R["term"], f"retained row {k} nonterminal")
    if R["r"] <= 2:
        check((R["A"], R["C"]) == (S + e, Tnu[k[0]] + e), f"(1.17) {k}")
    else:
        check((R["A"], R["C"]) == (S + e / 2, Tnu[k[0]] + e / 2), f"(1.17) {k}")
out(f"rows: old {nrows['o']}, new {nrows['n']}, retained {len(RET)}; h = {float(h):.6e}")

# masks (1.5) regenerated from (1.18)+(1.19) (only the rows needed here)
a_n = lambda t: ROWS[("n", t)]["a"]  # noqa: E731
b_o = lambda t: ROWS[("o", t)]["b"]  # noqa: E731
b_n = lambda t: ROWS[("n", t)]["b"]  # noqa: E731


def maskrow(lo, hi, z, d):
    return (max(0, floor(lo / h) - d + 1), min(NMAX, floor(hi / h) - d), floor(z / h))


C0h, C1h = T0 + e / 2, T1 + e / 2
genmask = {
    "O2": maskrow(a_n(0), a_n(24), (S + e) / 2, 40),
    "O52": maskrow(a_n(24), S, S + e / 2 - Fr(23, 40) * C1h, 40),
    "I2old": maskrow(b_o(12), b_o(24), (T0 + e) / 2, 39),
    "I52old": maskrow(b_o(24), T0, Fr(63, 160) * C0h, 39),
    "I2new": maskrow(b_n(12), b_n(24), (T1 + e) / 2, 39),
    "I52new": maskrow(b_n(24), T1, Fr(63, 160) * C1h, 39),
}
printed_mask = {"O2": (89197, 95598, 49152), "O52": (95599, 98263, 46580), "I2old": (84931, 87194, 44781),
                "I52old": (87195, 89524, 35265), "I2new": (85162, 87249, 44976), "I52new": (87250, 89914, 35419)}
for g in genmask:
    check(genmask[g] == printed_mask[g], f"mask row {g}: {genmask[g]} vs (1.5) {printed_mask[g]}")

# groups (1.22)-(1.24)
O2rows = [("o", t) for t in range(24)] + [("n", t) for t in range(24)]
GROUPS = [
    dict(name="O2", role="outer", d=40, m=Fr(2), rows=O2rows, absorbed=[], xi=ROWS[("o", 23)]["xi"],
         U=S + e, bG=a_n(0), tG=a_n(24), zh=49152, ph=24576),
    dict(name="O52", role="outer", d=40, m=Fr(5, 2),
         rows=[("o", t) for t in range(24, 28)] + [("n", t) for t in range(24, 39)], absorbed=O2rows,
         xi=ROWS[("n", 38)]["xi"], U=S + e / 2, bG=a_n(24), tG=98303 * h, zh=46580, ph=19660),
    dict(name="I2old", role="inner", d=39, m=Fr(2), rows=[("o", t) for t in range(12, 24)], absorbed=[],
         xi=ROWS[("o", 23)]["xi"], U=T0 + e, bG=b_o(12), tG=b_o(24), zh=44781, ph=22390),
    dict(name="I52old", role="inner", d=39, m=Fr(5, 2), rows=[("o", t) for t in range(24, 28)],
         absorbed=[("o", t) for t in range(12, 24)], xi=ROWS[("o", 27)]["xi"], U=T0 + e / 2, bG=b_o(24),
         tG=89563 * h, zh=35265, ph=17912),
    dict(name="I2new", role="inner", d=39, m=Fr(2), rows=[("n", t) for t in range(12, 24)], absorbed=[],
         xi=ROWS[("n", 23)]["xi"], U=T1 + e, bG=b_n(12), tG=b_n(24), zh=44976, ph=22488),
    dict(name="I52new", role="inner", d=39, m=Fr(5, 2), rows=[("n", t) for t in range(24, 39)],
         absorbed=[("n", t) for t in range(12, 24)], xi=ROWS[("n", 38)]["xi"], U=T1 + e / 2, bG=b_n(24),
         tG=89953 * h, zh=35419, ph=17990),
]
for G in GROUPS:
    G["mask"] = genmask[G["name"]]
    G["z"] = G["zh"] * h
    G["p"] = G["ph"] * h
    check(G["mask"][2] == G["zh"], f"{G['name']} z_G/h equals mask cap")
    check(floor(G["U"] / (2 * G["m"] * h)) == G["ph"], f"{G['name']} p_G = h floor(U/(2mh))")
    check(G["xi"] == min(ROWS[k]["xi"] for k in G["rows"]), f"{G['name']} xi_G = min originating activation")
    if G["absorbed"]:
        check(min(ROWS[k]["xi"] for k in G["absorbed"]) >= G["xi"], f"{G['name']} absorbed activations >= xi_G")
    # (1.25) lower bound agrees with the mask row lower bound
    check(floor(G["bG"] / h) - G["d"] + 1 == G["mask"][0], f"{G['name']} (1.25) lower = mask lower")
    # every originating row's threshold (in the group's role) equals U_G, or exceeds it for absorbed rows
    for k in G["rows"]:
        R = ROWS[k]
        V = R["A"] if G["role"] == "outer" else R["C"]
        check(V == G["U"], f"{G['name']} row {k} threshold = U_G")
    out(f"{G['name']:7s} d={G['d']} m={G['m']} xi={float(G['xi']):.6e} U={float(G['U']):.9f} "
        f"bG={float(G['bG']):.9f} tG={float(G['tG']):.9f} mask={G['mask']}")


def row_params(G, k):
    """core c_t, threshold V_t, effective order mu_t for row k in group G's role."""
    R = ROWS[k]
    if G["role"] == "outer":
        c, V = R["a"], R["A"]
    else:
        c, V = R["b"], R["C"]
    mu = Fr(2) if R["r"] <= 2 else Fr(5, 2)
    return c, V, mu, R["xi"], R["r"]


# inner order-one rows cannot fail (I_t = whole space) -> they are never eligible originators
for G in GROUPS:
    if G["role"] == "inner":
        check(all(ROWS[k]["r"] >= 2 for k in G["rows"] + G["absorbed"]), f"{G['name']} inner rows order >= 2")

# ------------------------------------------------------------------ Part B
out("\n== Part B: the 61 low intervals and (1.26) ==")
aj = [Fr(6, 5) ** j / 20 for j in range(10)]


def ulists(G, idx):
    x, p = G["xi"], G["p"]
    if idx == 1:
        return [x, 3 * x / 2, aj[0]] + aj[4:9] + [(aj[8] + aj[9]) / 2, aj[9], p]
    if idx == 2:
        return [2**j * x for j in range(9)] + [Fr(1, 100), Fr(3, 200), Fr(9, 400), Fr(27, 800)] + aj[0:8] + [
            (aj[7] + p) / 2, p]
    if idx == 3:
        return [x, aj[0], aj[4], aj[6], aj[8], p]
    if idx == 4:
        return [x, 2 * x, Fr(1, 100), Fr(27, 800), aj[3], aj[5], aj[6], p]
    if idx == 5:
        return [x, aj[1], aj[4], aj[5], aj[7], aj[8], p]
    if idx == 6:
        return [2**j * x for j in (0, 1, 4, 6, 8)] + [Fr(9, 400), aj[1], aj[3], aj[5], aj[6], aj[7], p]


INTERVALS = []  # (G, k, l, u)
for gi, G in enumerate(GROUPS, start=1):
    Ul = ulists(G, gi)
    check(all(Ul[i] < Ul[i + 1] for i in range(len(Ul) - 1)), f"{G['name']} list strictly increasing")
    G["U_list"] = Ul
    G["nint"] = len(Ul) - 1
    for k in range(1, len(Ul)):
        INTERVALS.append((G, k, Ul[k - 1], Ul[k]))
cnt = [G["nint"] for G in GROUPS]
out("intervals per group:", cnt, "total", sum(cnt))
check(sum(cnt) == 61, "61 low intervals")
check(sum(G["nint"] for G in GROUPS if G["m"] == Fr(5, 2)) == 40, "40 order-5/2 low intervals")


def eligible(G, u):
    return [k for k in G["rows"] + G["absorbed"] if ROWS[k]["xi"] < u]


def cG(G, u):
    el = eligible(G, u)
    if not el:
        return None
    vals = []
    for k in el:
        c, V, mu, xi, r = row_params(G, k)
        vals.append(max(c, V - (mu - 1) * u))
    return max(G["bG"], min(vals))


def retained_range(G, u):
    """index sums j retained for the low interval ending at u (None if empty event)."""
    c = cG(G, u)
    if c is None:
        return None
    lo = max(G["mask"][0], floor(G["bG"] / h) - G["d"] + 1, floor(c / h) - G["d"] + 1)
    hi = min(G["mask"][1], floor(G["tG"] / h))
    return lo, hi


direct = {}
out(f"{'grp':7s} {'k':>2s} {'l':>12s} {'u':>12s} {'#elig':>5s} {'#abs':>4s} {'cG-bG':>12s} {'o3min-bG':>12s}"
    f" {'j_lo':>6s} {'j_hi':>6s} L H K")
for (G, k, l, u) in INTERVALS:
    el = eligible(G, u)
    absel = [x for x in G["absorbed"] if ROWS[x]["xi"] < u]
    c = cG(G, u)
    rr = retained_range(G, u)
    # order-three minimum (originating rows only) for 5/2 groups
    o3 = None
    if G["m"] == Fr(5, 2):
        vals = []
        for x in G["rows"]:
            cc, V, mu, xi, r = row_params(G, x)
            if xi < u:
                vals.append(max(cc, V - (mu - 1) * u))
        o3 = min(vals) if vals else None
        end_below = all(u <= ROWS[x]["xi"] for x in G["absorbed"])
        end_below_strict = all(u < ROWS[x]["xi"] for x in G["absorbed"])
        check(end_below == end_below_strict, f"{G['name']} k={k}: u never equals an absorbed activation")
        o3_is_b = (o3 is not None) and max(G["bG"], o3) == G["bG"]
        direct.setdefault(G["name"], []).append((end_below, o3_is_b))
    Lg, Hg, Kg = floor(l / h), ceil(u / h), ceil(G["z"] / h)
    check(rr is not None and rr[0] <= rr[1], f"{G['name']} k={k}: retained index range nonempty {rr}")
    check(2 <= Lg < Hg <= Kg <= N, f"{G['name']} k={k}: 2<=L<H<=K<=N ({Lg},{Hg},{Kg})")
    G.setdefault("rr", {})[k] = rr
    out(f"{G['name']:7s} {k:2d} {float(l):12.6e} {float(u):12.6e} {len(el):5d} {len(absel):4d} "
        f"{float(c - G['bG']):12.4e} {('%12.4e' % float(o3 - G['bG'])) if o3 is not None else '         n/a'}"
        f" {rr[0]:6d} {rr[1]:6d} {Lg} {Hg} {Kg}")

# direct check claims
for name, (n_below, n_rest) in (("O52", (11, 11)), ("I52old", (2, 5)), ("I52new", (5, 6))):
    lst = direct[name]
    first = [i for i, (eb, ob) in enumerate(lst) if eb]
    # "the first n end below every absorbed activation": exactly a prefix of length n
    check(first == list(range(n_below)), f"{name}: intervals ending below all absorbed activations = first "
                                         f"{n_below} (got {len(first)}: {first})")
    rest = lst[n_below:]
    check(len(rest) == n_rest, f"{name}: remaining count {len(rest)} == {n_rest}")
    check(all(ob for (eb, ob) in rest), f"{name}: order-three minimum = b_G on the remaining {n_rest}")
    nob = [i for i, (eb, ob) in enumerate(lst) if ob]
    out(f"{name}: ends below all absorbed activations on {first}; order-3 minimum = b_G on {nob}")
# consequence stated in the proof: on the remaining intervals c_G(u) = b_G (no restriction)
for (G, k, l, u) in INTERVALS:
    if G["m"] == Fr(5, 2):
        eb, ob = direct[G["name"]][k - 1]
        if not eb:
            check(cG(G, u) == G["bG"], f"{G['name']} k={k}: c_G(u) = b_G when absorbed rows are eligible")

# ------------------------------------------------------------------ Part C
out("\n== Part C: exhaustive cell search (independent of (1.26)) ==")
# A failure of row t (in the group's role) with a witness p in (l,u] needs
#   p > xi_t, l < p <= u, p <= cap,   s > core c_t,
#   prefix(p) + (mu_t - 1) p > V_t   with prefix(p) <= s,
#   s in (b_G, t_G]  (group's radial interval).
# For a cell of index sum j on d coordinates, s ranges over [j h, (j+d) h).
# Decide, per (row, j), whether the set {(s, p)} is nonempty, by exact
# comparison of the infimum and supremum of s (strictness tracked).
# Then assert that j is retained by the (1.26) restriction.
ncell = 0
nposs = 0
slack_tot = 0
for (G, k, l, u) in INTERVALS:
    d = G["d"]
    jlo_all = G["mask"][0]
    jhi_all = min(G["mask"][1], floor(G["tG"] / h))
    rr = G["rr"][k]
    rowdata = []
    for x in G["rows"] + G["absorbed"]:
        c, V, mu, xi, r = row_params(G, x)
        plo = max(l, xi)  # p > plo
        if not (plo < u and plo < G["z"]):
            continue  # no admissible witness
        pmax = min(u, G["z"])
        # s must be > max(c, bG) and > V - (mu-1) p for some p <= pmax: inf = V - (mu-1) pmax (strict)
        s_inf = max(c, G["bG"], V - (mu - 1) * pmax)  # strict lower bound for s
        rowdata.append(s_inf)
    possible = []
    for j in range(jlo_all, jhi_all + 1):
        lo_cell, hi_cell = j * h, (j + d) * h  # s in [lo_cell, hi_cell)
        ok = False
        for s_inf in rowdata:
            # need s with s > s_inf, s >= lo_cell, s < hi_cell, s <= tG
            lo = max(s_inf, lo_cell)
            if lo < hi_cell and lo < G["tG"]:
                ok = True
                break
        ncell += 1
        if ok:
            possible.append(j)
            check(rr is not None and rr[0] <= j <= rr[1], f"{G['name']} k={k} j={j}: possible failure not retained")
    nposs += len(possible)
    nret = 0 if rr is None else rr[1] - rr[0] + 1
    if possible:
        check(possible == list(range(possible[0], possible[-1] + 1)), "possible set is an interval")
    slack = nret - len(possible)
    slack_tot += slack
    if slack:
        out(f"  {G['name']} k={k}: retained {nret} cells, failure-possible {len(possible)} (slack {slack})")
out(f"cells examined {ncell}, failure-possible cells {nposs}, retained-but-impossible cells {slack_tot}")

# C2: cells straddling a group boundary.  (i) No failure below the first group of each
# role: every failure-capable row has core >= that group's b_G, and the cells below the
# mask row have (j+d)h <= b_G.  (ii) Cells of a 5/2-group mask row whose totals can still be
# <= t_G of the preceding 2-group: a failure of a 2-group row there (s <= t_G) must be
# retained by the 5/2 group's interval containing its witness (absorbed rows).
GN = {G["name"]: G for G in GROUPS}
for first, cores in (("O2", [ROWS[k]["a"] for k in O2rows]),
                     ("I2old", [ROWS[("o", t)]["b"] for t in range(12, 28)]),
                     ("I2new", [ROWS[("n", t)]["b"] for t in range(12, 39)])):
    G = GN[first]
    check(min(cores) >= G["bG"], f"no failure below b_G of {first}")
    check((G["mask"][0] - 1 + G["d"]) * h <= G["bG"], f"cells below {first} mask row end at or below b_G")
nstr = 0
for g2, g52 in (("O2", "O52"), ("I2old", "I52old"), ("I2new", "I52new")):
    G, Gp = GN[g2], GN[g52]
    d = Gp["d"]
    check(G["mask"][1] + 1 == Gp["mask"][0], f"{g2}/{g52} mask rows adjacent")
    check((G["mask"][1] + G["d"]) * h <= G["tG"], f"{g2} mask cells lie in s < t_G")
    for (H_, k, l, u) in INTERVALS:
        if H_ is not Gp:
            continue
        rr = Gp["rr"][k]
        for x in G["rows"]:
            c, V, mu, xi, r = row_params(G, x)
            plo = max(l, xi)
            if not plo < u:
                continue
            s_inf = max(c, G["bG"], V - (mu - 1) * u)
            for j in range(Gp["mask"][0], min(Gp["mask"][1], floor(G["tG"] / h)) + 1):
                lo = max(s_inf, j * h)
                if lo < (j + d) * h and lo < G["tG"]:
                    nstr += 1
                    check(rr[0] <= j <= rr[1], f"straddle {g2}->{g52} k={k} row {x} j={j} not retained")
out(f"straddling (cell, row, interval) failure cases checked: {nstr}")

# ------------------------------------------------------------------ Part D
out("\n== Part D: explicit configurations with literal predicates (1.21) ==")


def H(X, phi, xi):
    """inclusive obstruction: max over p in X, p > xi, of sum_{q in X, q >= p} q + phi(p); 0 if none."""
    best = Fr(0)
    Xs = sorted(X, reverse=True)
    pref = Fr(0)
    i = 0
    while i < len(Xs):
        p = Xs[i]
        while i < len(Xs) and Xs[i] == p:
            pref += Xs[i]
            i += 1
        if p > xi:
            best = max(best, pref + phi(p))
    return best


def Mxi(X, xi):
    c = [p for p in X if p > xi]
    return max(c) if c else Fr(0)


def fails(G, key, X, s):
    R = ROWS[key]
    r, xi, A, C = R["r"], R["xi"], R["A"], R["C"]
    L = Fr(23, 40) * C
    phiD = lambda p: min(3 * p / 2, L)  # noqa: E731
    phiE = lambda p: 3 * p - phiD(p)  # noqa: E731
    if G["role"] == "outer":
        if s <= R["a"]:
            return False
        if r <= 2:
            return not (H(X, lambda p: p, xi) <= A)
        return not (H(X, phiD, xi) <= A and phiE(Mxi(X, xi)) <= C)
    if r == 1:
        return False
    if s <= R["b"]:
        return False
    if r == 2:
        return not (H(X, lambda p: p, xi) <= C)
    return not (H(X, phiE, xi) <= C and phiD(Mxi(X, xi)) <= A)


def witness_in_bin(G, key, X, l, u):
    """a failing witness p in (l,u]: prefix(p)+(mu-1)p > V_t, p > xi_t."""
    c, V, mu, xi, r = row_params(G, key)
    for p in set(X):
        if l < p <= u and p > xi:
            pref = sum(q for q in X if q >= p)
            if pref + (mu - 1) * p > V:
                return True
    return False


rng = random.Random(186)
xi_all_min = min(ROWS[k]["xi"] for k in RET)
check(h < xi_all_min, "filler fragments (< h) are below every activation")
nconf = nskip = 0
sharp = {}


def build(G, key, l, u, p, mode):
    """concrete configuration on d coordinates; returns (X, coords totals) or None."""
    d = G["d"]
    c, V, mu, xi, r = row_params(G, key)
    zc = G["z"]
    epsg = h / 10**6
    nfill_free = 0
    # prefix fragments (>= p, <= cap) carry the mass; filler fragments (< h) align coordinates
    kmax = min(d, max(1, floor(Fr(1) / p)))  # how many coordinates can carry a fragment >= p
    k_use = kmax if mode != "random" else rng.randint(1, kmax)
    # filler-only coordinates (aligned mode) add (h - eps) each to s without raising j
    free = (d - k_use) * (h - epsg) if mode == "aligned" else 0
    Q = max(V - (mu - 1) * p, max(c, G["bG"]) - free) + h / 10**7
    # pieces: p itself in coordinate 0, remainder Q - p split over coordinates
    rest = Q - p
    if rest < p:
        return None
    coords = [[] for _ in range(d)]
    coords[0].append(p)
    ncar = max(1, k_use - 1)
    npieces = max(ncar, ceil(rest / zc))
    while rest / npieces < p and npieces > 1:
        npieces -= 1
    piece = rest / npieces
    if not (p <= piece <= zc):
        return None
    if mode == "aligned" and npieces <= d - 1:
        # make every carrying coordinate total congruent to -eps mod h, keeping pieces >= p and <= cap
        tot = Fr(0)
        for i in range(npieces - 1):
            f = ceil((piece + epsg) / h) * h - epsg
            if f > zc:
                f = piece
            coords[1 + i].append(f)
            tot += f
        last = rest - tot
        if not (p <= last <= zc):
            return None
        coords[npieces].append(last)
    else:
        for i in range(npieces):
            coords[1 + (i % (d - 1))].append(piece)
    # fillers
    for i in range(d):
        ti = sum(coords[i])
        if mode == "random":
            g = Fr(rng.randint(0, 10**6), 10**6) * (h - epsg)
        else:
            if ti == 0 and mode != "aligned":
                continue
            target = (floor(ti / h) + 1) * h - epsg if ti > 0 else h - epsg
            if target < ti:
                target += h
            g = target - ti
        if g > 0:
            coords[i].append(g)
    return coords


for (G, k, l, u) in INTERVALS:
    d = G["d"]
    rr = G["rr"][k]
    best_j = None
    for key in eligible(G, u):
        xi = ROWS[key]["xi"]
        plo = max(l, xi)
        if not plo < u:
            continue
        choices = [(u, "aligned"), (u, "plain"),
                   (plo + (u - plo) * Fr(rng.randint(1, 999), 1000), "random")]
        for (p, mode) in choices:
            coords = build(G, key, l, u, p, mode)
            if coords is None:
                nskip += 1
                continue
            X = [f for cc in coords for f in cc]
            ts = [sum(cc) for cc in coords]
            s = sum(ts)
            j = sum(floor(t / h) for t in ts)
            # configuration must lie in the group's region: radial interval and mask row, fragments <= cap
            if not (G["bG"] < s <= G["tG"] and G["mask"][0] <= j <= G["mask"][1]):
                nskip += 1
                continue
            check(max(X) <= G["z"], "fragments within grid cap")
            check(j * h <= s < (j + d) * h, "cell contains total")
            if not fails(G, key, X, s):
                nskip += 1
                continue
            check(witness_in_bin(G, key, X, l, u), f"{G['name']} k={k} {key}: failing witness in bin")
            nconf += 1
            check(rr is not None and rr[0] <= j <= rr[1],
                  f"{G['name']} k={k} row {key}: explicit failure at j={j} not retained {rr}")
            if best_j is None or j < best_j:
                best_j = j
    sharp[(G["name"], k)] = None if best_j is None else best_j - rr[0]
out(f"explicit failing configurations tested {nconf}, skipped (not in region / not a failure) {nskip}")
sl = [v for v in sharp.values() if v is not None]
out(f"intervals with an explicit failure: {len(sl)} / 61; min-j minus retained j_lo: "
    f"zero on {sum(1 for v in sl if v == 0)}, max {max(sl)}")
out("  per interval (group,k): slack =", {f"{a}{b}": v for (a, b), v in sharp.items()})

out("\n== summary ==")
mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
out(f"checks {NCHECK}, failures {NFAIL}, runtime {time.time() - T0_WALL:.1f} s, peak RSS {mem:.0f} MB")
