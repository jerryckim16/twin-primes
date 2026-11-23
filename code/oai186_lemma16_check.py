#!/usr/bin/env python3
"""Rung 186: exact check of Lemma 1.6 ("Containment of the low-witness intervals", p. 10) of OpenAI's numerical
companion [14] ("Numerical certificate for prime gaps at most 186",
code/third_party/openai186/short_gaps_numerics.pdf).  Report: notes/oai186-lemma16-check.md.
Modelled on code/oai186_lemma15_check.py.

Lemma 1.6 (p. 10).  "The radial restrictions in (1.26), applied to the displayed 61 low intervals, retain every
source failure assigned to those intervals."  (1.26), p. 6:
      c_G(u) := max{ b_G , min_{t : xi_t < u} max{ c_t , V_t - (mu_t - 1) u } },
retain j >= floor(c_G(u)/h) - d_G + 1; for m_G = 5/2 the eligible rows include those of the preceding order-two
group ("absorbed"), each with its own order mu_t.  The proof adds a "direct check" (counts 11, 2, 5 / 11, 5, 6)
and "Each of the 61 intervals is nonempty on this grid."

Everything that decides a check is exact (fractions.Fraction / int); floats are used only for printing.
Sections:
  [0] source rows (1.13)-(1.17), retained rows (1.20), predicates (1.21) -> (c_t, V_t, xi_t, mu_t); the group
      table (1.22)-(1.24) re-derived from the rows; absorbed rows; cross-check with code/oai186_support_data.py;
  [1] the 61 low bins of Sec. 1.5.1 (p. 9);
  [2] c_G(u) of (1.26) on all 61 bins, from every eligible row (own + absorbed, own order);
  [3] the printed direct check (11, 2, 5 / 11, 5, 6) and its consequence c_G(with absorbed) = c_G(without);
      comparison with the authors' source_clipped_group (which omits absorbed rows);
  [4] "each of the 61 intervals is nonempty on this grid", in three readings;
  [5] the containment argument: exactness of the outward full-cell test; randomized exact end-to-end test on
      failing roots (own and absorbed rows, all 61 bins); negative controls; an explicit example showing that
      "assigned" must mean "by a witness of the failing row".
usage: /usr/bin/python3 code/oai186_lemma16_check.py > code/oai186_lemma16_check.out"""
import os, sys, json, random, subprocess, time, importlib.util, io, contextlib, resource
from fractions import Fraction as F
from math import floor, ceil

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


# ---------------------------------------------------------------------------------------------------------------
print("[0] source rows (1.13)-(1.21), pp. 4-5; groups (1.22)-(1.24), pp. 5-6; masks (1.5), p. 2")
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
n = N - 40
h = S / N
check("(1.1)/(1.3): S = 2742997/2624989, T0, T1 as printed, h = S/98304",
      S == F(2742997, 2624989) and T0 == F(2499106033, 2624989000) and T1 == F(2510000, 2624989)
      and h == F(2742997, 2624989 * 98304))
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
        rows.append(dict(nu=nu, t=t, r=r, xi=xi, a=a, b=b, A=a + eta, C=b + eta, B=B, terminal=(w == Om[nu]),
                         mu=(F(5, 2) if r == 3 else F(2))))
        wp, t = w, t + 1
        if rows[-1]["terminal"]:
            break
    lad[nu] = rows
o, nw = lad["o"], lad["n"]
check("ladders: 29 / 43 rows, order counts (12,12,5) / (12,12,19)",
      (len(o), len(nw)) == (29, 43)
      and [sum(x["r"] == k for x in o) for k in (1, 2, 3)] == [12, 12, 5]
      and [sum(x["r"] == k for x in nw) for k in (1, 2, 3)] == [12, 12, 19])
Sbox, Tbox = 98303 * h, {"o": 89563 * h, "n": 89953 * h}
ret = {nu: [x for x in lad[nu] if x["B"] < Sbox + Tbox[nu]] for nu in lad}
check("(1.20): retained rows are (o,0..27) and (n,0..38); none is terminal",
      [x["t"] for x in ret["o"]] == list(range(28)) and [x["t"] for x in ret["n"]] == list(range(39))
      and not any(x["terminal"] for nu in ret for x in ret[nu]))
check("(1.17) on retained rows: (A,C) = (S+e, T+e) in orders 1-2 and (S+e/2, T+e/2) in order 3",
      all((x["A"], x["C"]) == ((S + e, TT[nu] + e) if x["r"] <= 2 else (S + e / 2, TT[nu] + e / 2))
          for nu in ret for x in ret[nu]))
check("activations xi_t decrease strictly along each ladder (xi_t = delta_t / rho)",
      all(lad[nu][i]["xi"] > lad[nu][i + 1]["xi"] for nu in lad for i in range(len(lad[nu]) - 1)))

# (1.21): outer predicate O_t fails iff s > a_t and the obstruction exceeds A_t; inner I_t iff s > b_t and > C_t;
# I_t is the whole space for r_t = 1 (no inner failure).  So (c_t, V_t) = (a_t, A_t) outer, (b_t, C_t) inner.
# mu_t = 2 for source orders 1, 2 and 5/2 for order 3 ((1.26); order 3 via Lemma 1.4: nonlargest H_{5/2} failure).
GR = [
    dict(name="O2", kind="outer", d=40, m=F(2), xi=o[23]["xi"], U=S + e, b=nw[0]["a"], t=nw[24]["a"], z=49152,
         p=24576, mask=[(0, 89196), (89197, 95598), (95599, 98263)], zrow=1, rows=o[:24] + nw[:24], absorbed=[]),
    dict(name="O5/2", kind="outer", d=40, m=F(5, 2), xi=nw[38]["xi"], U=S + e / 2, b=nw[24]["a"], t=98303 * h,
         z=46580, p=19660, mask=[(0, 89196), (89197, 95598), (95599, 98263)], zrow=2,
         rows=o[24:28] + nw[24:39], absorbed=o[:24] + nw[:24]),
    dict(name="I2old", kind="inner", d=39, m=F(2), xi=o[23]["xi"], U=T0 + e, b=o[12]["b"], t=o[24]["b"], z=44781,
         p=22390, mask=[(0, 84930), (84931, 87194), (87195, 89524)], zrow=1, rows=o[12:24], absorbed=[]),
    dict(name="I5/2old", kind="inner", d=39, m=F(5, 2), xi=o[27]["xi"], U=T0 + e / 2, b=o[24]["b"], t=89563 * h,
         z=35265, p=17912, mask=[(0, 84930), (84931, 87194), (87195, 89524)], zrow=2, rows=o[24:28],
         absorbed=o[12:24]),
    dict(name="I2new", kind="inner", d=39, m=F(2), xi=nw[23]["xi"], U=T1 + e, b=nw[12]["b"], t=nw[24]["b"],
         z=44976, p=22488, mask=[(0, 85161), (85162, 87249), (87250, 89914)], zrow=1, rows=nw[12:24], absorbed=[]),
    dict(name="I5/2new", kind="inner", d=39, m=F(5, 2), xi=nw[38]["xi"], U=T1 + e / 2, b=nw[24]["b"],
         t=89953 * h, z=35419, p=17990, mask=[(0, 85161), (85162, 87249), (87250, 89914)], zrow=2,
         rows=nw[24:39], absorbed=nw[12:24]),
]


def cV(G, x):
    return (x["a"], x["A"]) if G["kind"] == "outer" else (x["b"], x["C"])


for G in GR:
    G["face"] = G["mask"][-1][1]
    G["R0"] = max(0, floor(G["b"] / h) - G["d"] + 1)                      # (1.25) lower
    G["R1"] = floor(G["t"] / h)                                           # (1.25) upper (outward)
    G["pp"] = G["p"] * h
# (1.22): row sets; own rows give the table entries as minima
ok = True
for G in GR:
    ok &= G["xi"] == min(x["xi"] for x in G["rows"])
    ok &= G["U"] == min(cV(G, x)[1] for x in G["rows"])
    ok &= G["b"] == min(cV(G, x)[0] for x in G["rows"])
    ok &= all(x["r"] == (3 if G["m"] == F(5, 2) else x["r"]) and (x["r"] <= 2 or G["m"] == F(5, 2)) for x in G["rows"])
    ok &= G["kind"] == "outer" or all(x["r"] >= 2 for x in G["rows"])
check("(1.23) vs (1.22): xi_G = min own xi_t, U_G = min own V_t, b_G = min own core c_t; orders match m_G;"
      " inner groups have no order-1 row (I_t = whole space)", ok)
check("(1.23)-(1.24): radial intervals chain: t_G(order 2) = b_G(order 5/2) in each role; t_G(5/2) = largest total",
      GR[0]["t"] == GR[1]["b"] and GR[2]["t"] == GR[3]["b"] and GR[4]["t"] == GR[5]["b"]
      and [GR[1]["t"], GR[3]["t"], GR[5]["t"]] == [98303 * h, 89563 * h, 89953 * h])
check("(1.24): p_G = h floor(U_G/(2 m_G h)) for all six groups",
      all(floor(G["U"] / (2 * G["m"] * h)) == G["p"] for G in GR))
caps18 = [(S + e) / 2, S + e / 2 - 23 * (T1 + e / 2) / 40, (T0 + e) / 2, 63 * (T0 + e / 2) / 160,
          (T1 + e) / 2, 63 * (T1 + e / 2) / 160]
check("(1.24) z_G = floor(cap/h) for the (1.18) cap of the group's shell, and = the cap of mask row zrow of (1.5)",
      [floor(c / h) for c in caps18] == [G["z"] for G in GR]
      and [G["z"] for G in GR] == [49152, 46580, 44781, 35265, 44976, 35419])
ok = True
for gi in (1, 3, 5):
    G, P = GR[gi], GR[gi - 1]
    ok &= G["absorbed"] == P["rows"]
    ok &= all(x["mu"] == 2 for x in G["absorbed"]) and all(x["mu"] == F(5, 2) for x in G["rows"])
    ok &= min(x["xi"] for x in G["absorbed"]) == P["xi"] >= G["xi"]
    ok &= all(cV(G, x)[1] >= G["U"] for x in G["absorbed"])
check("absorbed rows of each 5/2 group = own rows of the preceding order-two group (1.22); mu_t = 2 for them;"
      " min absorbed activation = xi of that group >= xi_G; their thresholds >= U_G (p. 6 last lines)", ok)
# cross-check with the repository's support-data script (independent of this file's ladder code)
try:
    out = subprocess.run([sys.executable, os.path.join(HERE, "oai186_support_data.py")], capture_output=True,
                         text=True, timeout=600).stdout
    js = json.loads(out)
    check("code/oai186_support_data.py: all its printed-value checks pass (masks (1.5), groups, ladders)",
          js.get("all_ok") is True and js["masks"]["outer"] == [[a, b_, z] for (a, b_), z in
                                                                 zip(GR[0]["mask"], (68225, 49152, 46580))])
except Exception as ex:  # pragma: no cover
    check("code/oai186_support_data.py runs", False, repr(ex))

# ---------------------------------------------------------------------------------------------------------------
print("\n[1] the 61 low bins (Sec. 1.5.1, p. 9)")
aa = [F(6, 5) ** j / 20 for j in range(10)]
LISTS = [
    lambda x, p: [x, 3 * x / 2, aa[0]] + aa[4:9] + [(aa[8] + aa[9]) / 2, aa[9], p],
    lambda x, p: [2 ** j * x for j in range(9)] + [F(1, 100), F(3, 200), F(9, 400), F(27, 800)] + aa[0:8]
                 + [(aa[7] + p) / 2, p],
    lambda x, p: [x, aa[0], aa[4], aa[6], aa[8], p],
    lambda x, p: [x, 2 * x, F(1, 100), F(27, 800), aa[3], aa[5], aa[6], p],
    lambda x, p: [x, aa[1], aa[4], aa[5], aa[7], aa[8], p],
    lambda x, p: [2 ** j * x for j in (0, 1, 4, 6, 8)] + [F(9, 400), aa[1], aa[3], aa[5], aa[6], aa[7], p]]
BINS = []
for gi, (G, ul) in enumerate(zip(GR, LISTS)):
    G["ulist"] = ul(G["xi"], G["pp"])
    for j in range(1, len(G["ulist"])):
        th = 120 if (gi == 0 and j == 3) else ceil((F(9) if gi == 5 else F(7)) / G["ulist"][j])
        BINS.append(dict(G=G, gi=gi, j=j, name="L%d" % j, l0=G["ulist"][j - 1], u0=G["ulist"][j], theta=th))
check("interval counts 10, 22, 5, 7, 6, 11 (total 61)",
      [len(G["ulist"]) - 1 for G in GR] == [10, 22, 5, 7, 6, 11] and len(BINS) == 61)
check("each list increases strictly from xi_G to p_G, so the bins (l,u] partition (xi_G, p_G]",
      all(all(G["ulist"][i] < G["ulist"][i + 1] for i in range(len(G["ulist"]) - 1))
          and G["ulist"][0] == G["xi"] and G["ulist"][-1] == G["pp"] for G in GR))
check("40 order-5/2 low intervals (22 + 7 + 11)", sum(len(GR[k]["ulist"]) - 1 for k in (1, 3, 5)) == 40)


# ---------------------------------------------------------------------------------------------------------------
print("\n[2] c_G(u) of (1.26) on every bin, from every eligible row (own + absorbed, each with its own mu_t)")


def term(G, x, u):
    c, V = cV(G, x)
    return max(c, V - (x["mu"] - 1) * u)


def cG(G, u, absorbed=True, mu_override=None, elig_at=None):
    """(1.26).  elig_at: eligibility point (default u); mu_override: force mu for order-3 rows (neg. control)."""
    ea = u if elig_at is None else elig_at
    rows = G["rows"] + (G["absorbed"] if absorbed else [])
    el = []
    for x in rows:
        if x["xi"] < ea:
            c, V = cV(G, x)
            mu = x["mu"] if (mu_override is None or x["r"] < 3) else mu_override
            el.append(max(c, V - (mu - 1) * u))
    return None if not el else max(G["b"], min(el))


def lo_of(G, c):
    return floor(c / h) - G["d"] + 1


print("  group  bin   l              u              theta  #own  #abs  argmin-row  c_G(u)        floor(c/h)-d+1")
for b in BINS:
    G, u = b["G"], b["u0"]
    own = [x for x in G["rows"] if x["xi"] < u]
    ab = [x for x in G["absorbed"] if x["xi"] < u]
    b["cG"] = cG(G, u)
    b["cG_noabs"] = cG(G, u, absorbed=False)
    b["lo"] = None if b["cG"] is None else lo_of(G, b["cG"])
    arg = min(own + ab, key=lambda x: (term(G, x, u), x["nu"], x["t"])) if own + ab else None
    b["arg"] = arg
    b["nown"], b["nabs"] = len(own), len(ab)
    tag = "b_G" if b["cG"] == G["b"] else "(%s,%d)" % (arg["nu"], arg["t"])
    print("  %-7s %-4s %-14s %-14s %-6d %-5d %-5d %-11s %-13s %d" % (
        G["name"], b["name"], fl(b["l0"]), fl(u), b["theta"], len(own), len(ab), tag, fl(b["cG"], 12), b["lo"]))
check("every one of the 61 bins has a nonempty eligible set (so its event is not declared empty)",
      all(b["cG"] is not None for b in BINS))
check("c_G(u) >= b_G and c_G is nonincreasing in u along each group's bins",
      all(b["cG"] >= b["G"]["b"] for b in BINS)
      and all(BINS[i]["cG"] >= BINS[i + 1]["cG"] for i in range(len(BINS) - 1) if BINS[i]["gi"] == BINS[i + 1]["gi"]))
check("structure: on all 61 bins c_G(u) = max(b_G, min of the cores c_t of the eligible rows): the threshold term"
      " V_t - (mu_t-1)u never decides the minimum; hence also mu_t := 2 for order-3 rows, or mu_t := m_G for all"
      " rows, gives the same c_G(u) on every bin",
      all(b["cG"] == max(b["G"]["b"], min(cV(b["G"], x)[0] for x in b["G"]["rows"] + b["G"]["absorbed"]
                                          if x["xi"] < b["u0"])) for b in BINS)
      and all(cG(b["G"], b["u0"], mu_override=F(2)) == b["cG"] for b in BINS))
check("no tie xi_t = u between any row activation (own or absorbed) and any bin end u",
      all(x["xi"] != b["u0"] for b in BINS for x in b["G"]["rows"] + b["G"]["absorbed"]))

# ---------------------------------------------------------------------------------------------------------------
print("\n[3] the direct check printed in the proof of Lemma 1.6 (p. 10)")
want1 = {1: 11, 3: 2, 5: 5}
want2 = {1: 11, 3: 5, 5: 6}
for gi in (1, 3, 5):
    G = GR[gi]
    gb = [b for b in BINS if b["gi"] == gi]
    amin = min(x["xi"] for x in G["absorbed"])
    first = [b for b in gb if all(b["u0"] < x["xi"] for x in G["absorbed"])]   # 'end below every activation'
    k = len(first)
    is_prefix = first == gb[:k]
    rest = gb[k:]

    def m3(b):  # the order-three minimum: over eligible own (order-3) rows only
        el = [term(G, x, b["u0"]) for x in G["rows"] if x["xi"] < b["u0"]]
        return min(el) if el else None
    check("%s: exactly the first %d of %d intervals end below every absorbed order-two activation "
          "(min = xi of %s = %s); with '<=' instead of '<' the count is the same"
          % (G["name"], want1[gi], len(gb), GR[gi - 1]["name"], fl(amin)),
          is_prefix and k == want1[gi] and k == sum(b["u0"] <= amin for b in gb),
          "u_%d = %s < %s < u_%d = %s" % (k, fl(gb[k - 1]["u0"]), fl(amin), k + 1, fl(gb[k]["u0"])))
    check("%s: on the remaining %d intervals the order-three minimum equals b_G exactly (attained by the row with"
          " core b_G), hence c_G(u) = b_G" % (G["name"], want2[gi]),
          len(rest) == want2[gi] and all(m3(b) == G["b"] and b["cG"] == G["b"] for b in rest))
    sharp = [b["name"] for b in gb[:k] if m3(b) > G["b"]]
    check("%s: the split is sharp: on each of the first %d intervals the order-three minimum is > b_G, and some "
          "absorbed row is eligible on every remaining interval" % (G["name"], k),
          len(sharp) == k and all(b["nabs"] > 0 for b in rest), "first intervals with m3 > b_G: " + ",".join(sharp))
check("consequence: on all 40 order-5/2 intervals c_G(u) with absorbed rows = c_G(u) without them",
      all(b["cG"] == b["cG_noabs"] for b in BINS if b["gi"] in (1, 3, 5)))
check("note: the order-two groups have no absorbed rows, so (1.26) uses own rows only there",
      all(not GR[k]["absorbed"] for k in (0, 2, 4)))
check("absorbed rows with own order are never looser than with mu = m_G = 5/2 (V - u >= V - 3u/2): "
      "own order is the sharper, still valid choice", all(cV(G, x)[1] - u >= cV(G, x)[1] - F(3, 2) * u
                                                           for G in GR for x in G["absorbed"] for u in (F(1, 10),)))

# authors' script: compare (l, u, theta) and the clipped lower boundary / first index
try:
    spec = importlib.util.spec_from_file_location(
        "pg186", os.path.join(HERE, "third_party", "openai186", "prime_gap_186_certificate.py"))
    pg = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(pg)
    low = [t for t in pg.TASKS if t["kind"] == "low"]
    ok_sched = len(low) == 61 and all(
        F(t["parameters"]["low"]) == b["l0"] and F(t["parameters"]["high"]) == b["u0"]
        and int(t["parameters"]["slope"]) == b["theta"] for t, b in zip(low, BINS))
    check("authors' script: the same 61 low tasks (l, u, theta) in the same order", ok_sched)
    ok_c, ok_j, ok_rows = True, True, True
    for t, b in zip(low, BINS):
        grp = pg.GROUP_BY_ID[t["source_group_id"]]
        cl = pg.source_clipped_group(grp, h, t["parameters"]["high"])
        ok_c &= cl is not None and F(cl["radial_lower"]) == b["cG"]
        ok_j &= cl is not None and min(int(pc["first_index"]) for pc in cl["aligned_cap_pieces"]) == max(
            b["G"]["R0"], b["lo"])
        ok_rows &= len(grp["source_rows"]) == len(b["G"]["rows"])
    check("authors' source_clipped_group: radial_lower = our c_G(u) and first retained index = max(R0, "
          "floor(c_G/h)-d+1) on all 61 bins", ok_c and ok_j)
    check("authors' groups list only own rows (19, 4, 15 order-3 rows in the 5/2 groups): absorbed rows omitted,"
          " harmless by the direct check above", ok_rows and [len(g["source_rows"]) for g in pg.SOURCE_GROUPS]
          == [48, 19, 12, 4, 12, 15])
except Exception as ex:  # pragma: no cover
    check("authors' script importable for comparison", False, repr(ex))

# ---------------------------------------------------------------------------------------------------------------
print("\n[4] 'Each of the 61 intervals is nonempty on this grid' (p. 10)")
# Reading A: (1.25) range intersected with the whole domain mask of (1.5), clipped by (1.26).
# Reading B: same, but intersected only with the mask row whose cap is z_G ("the appropriate rows").
# Reading C: physical: c_G(u) < t_G, so (c_G(u), t_G] is a nonempty radial interval.
# Also: the bin itself meets the grid: floor(l/h) < ceil(u/h) and it contains a grid point jh.
cntA, cntB = [], []
for b in BINS:
    G = b["G"]
    loA, hiA = max(G["R0"], b["lo"], 0), min(G["R1"], G["face"])
    zr = G["mask"][G["zrow"]]
    loB, hiB = max(G["R0"], b["lo"], zr[0]), min(G["R1"], zr[1])
    cntA.append(hiA - loA + 1)
    cntB.append(hiB - loB + 1)
    b["loA"], b["hiA"] = loA, hiA
check("reading A: retained index range (1.25) n (1.5 domain) n (1.26) nonempty on all 61 bins",
      min(cntA) >= 1, "smallest count %d (%s %s)" % (min(cntA), BINS[cntA.index(min(cntA))]["G"]["name"],
                                                     BINS[cntA.index(min(cntA))]["name"]))
check("reading B: same with only the mask row of cap z_G, nonempty on all 61 bins",
      min(cntB) >= 1, "smallest count %d (%s %s)" % (min(cntB), BINS[cntB.index(min(cntB))]["G"]["name"],
                                                     BINS[cntB.index(min(cntB))]["name"]))
check("reading C: c_G(u) < t_G on all 61 bins (nonempty physical radial interval)",
      all(b["cG"] < b["G"]["t"] for b in BINS))
check("the witness intervals themselves meet the grid: floor(l/h) < ceil(u/h), and each contains a grid point",
      all(floor(b["l0"] / h) < ceil(b["u0"] / h) and floor(b["u0"] / h) * h > b["l0"] for b in BINS))

# ---------------------------------------------------------------------------------------------------------------
print("\n[5] the containment argument")
# (a) outward full-cell test.  A d-cell with index sum j has totals s in [jh, (j+d)h) (each t_i in [j_i h,(j_i+1)h)).
# It meets {s > c} iff (j+d)h > c iff j >= floor(c/h) - d + 1 =: j0.  Exhibit a point for j0, none for j0 - 1.
ok_a = True
for b in BINS:
    G, c = b["G"], b["cG"]
    d, j0 = G["d"], b["lo"]
    js = [j0 // d] * d
    for i in range(j0 % d):
        js[i] += 1
    assert sum(js) == j0
    gap = (j0 + d) * h - c
    ok_a &= gap > 0
    ts = [(ji + 1) * h - gap / (2 * d) for ji in js]          # strictly inside the cells, just below the top
    ok_a &= all(ji * h <= ti < (ji + 1) * h for ti, ji in zip(ts, js)) and sum(ts) > c
    ok_a &= (j0 - 1 + d) * h <= c                             # sup of totals on index j0-1 is <= c
check("(a) the outward full-cell test is exact on all 61 bins: index floor(c_G/h)-d+1 contains a point with"
      " s > c_G (explicit totals), index one lower contains none", ok_a)


def Hobs(frags, xi, mu):
    """(1.12)/(p.1): H_{m,xi}(X) = max over p in X, p > xi, of sum_{q in X, q >= p} q + (m-1) p; 0 if empty."""
    fs = sorted(frags, reverse=True)
    best, pref, i = F(0), F(0), 0
    while i < len(fs):
        j = i
        while j < len(fs) and fs[j] == fs[i]:
            pref += fs[j]
            j += 1
        if fs[i] > xi:
            best = max(best, pref + (mu - 1) * fs[i])
        i = j
    return best


def witnesses(frags, xi, mu, V):
    fs = sorted(frags, reverse=True)
    out, pref, i = [], F(0), 0
    while i < len(fs):
        j = i
        while j < len(fs) and fs[j] == fs[i]:
            pref += fs[j]
            j += 1
        if fs[i] > xi and pref + (mu - 1) * fs[i] > V:
            out.append(fs[i])
        i = j
    return out


def bin_of(G, p):
    U_ = G["ulist"]
    for j in range(1, len(U_)):
        if U_[j - 1] < p <= U_[j]:
            return [b for b in BINS if b["G"] is G and b["j"] == j][0]
    return None


rnd = random.Random(16)


def rfrac(den=10 ** 6):
    return F(rnd.randint(1, den), den)


def make_root(G, b, x, p, delta, extra):
    """A root with the failing row x witnessed at p: prefix(p) = V - (mu-1)p + delta, s > max(core, b_G)."""
    c, V = cV(G, x)
    P = V - (x["mu"] - 1) * p + delta
    big = []
    rest = P - p
    if rest >= p:
        k = rnd.randint(1, max(1, min(6, int(rest / p))))
        parts = [p] * k
        excess = rest - k * p
        wts = [rfrac() for _ in range(k)]
        sw = sum(wts)
        parts = [pp + excess * wv / sw for pp, wv in zip(parts, wts)]
        big = parts
    elif rest > 0:
        return None
    s = max(P, c + extra, G["b"] + extra)
    small_total = s - P
    small = []
    while small_total > 0:
        piece = min(small_total, p * F(rnd.randint(300, 990), 1000))
        if piece >= p:
            piece = p * F(1, 2)
        small.append(piece)
        small_total -= piece
        if len(small) > 3000:
            return None
    frags = [p] + big + small
    if sum(frags) != s:
        return None
    return frags, s


def place(frags, d):
    tot = [F(0)] * d
    for q in frags:
        tot[rnd.randrange(d)] += q
    return sum(floor(ti / h) for ti in tot)


stats = dict(roots=0, witn=0, lost=0, lost_cell=0, skipped=0, absorbed_roots=0, boundary=0)
neg = dict(ell=0, mu2=0, elig_l=0, noabs=0)
per_bin = {}
for b in BINS:
    G, u = b["G"], b["u0"]
    elig = [x for x in G["rows"] + G["absorbed"] if x["xi"] < u]
    for trial in range(140):
        x = b["arg"] if trial % 4 == 0 else rnd.choice(elig)
        lo_p = max(b["l0"], x["xi"])
        mode = trial % 7
        p = u if mode in (0, 1) else lo_p + (u - lo_p) * rfrac()
        if p <= lo_p:
            continue
        delta = [F(1, 10 ** 30), rfrac() / 10 ** 6, rfrac() / 10 ** 3][trial % 3]
        extra = [F(1, 10 ** 30), rfrac() / 10 ** 5, rfrac() / 10 ** 2][(trial // 3) % 3]
        got = make_root(G, b, x, p, delta, extra)
        if got is None:
            stats["skipped"] += 1
            continue
        frags, s = got
        if not (G["b"] < s <= G["t"]):
            stats["skipped"] += 1            # failure belongs to another group's radial interval
            continue
        c, V = cV(G, x)
        assert s > c and Hobs(frags, x["xi"], x["mu"]) > V     # the row really fails
        stats["roots"] += 1
        stats["absorbed_roots"] += x in G["absorbed"]
        stats["boundary"] += (mode in (0, 1) and delta == F(1, 10 ** 30))
        r = place(frags, G["d"])
        for w in witnesses(frags, x["xi"], x["mu"], V):
            if w > G["pp"]:
                continue                     # not a low witness (rank-two / factorial components)
            bb = bin_of(G, w)
            stats["witn"] += 1
            if not (s > bb["cG"]):
                stats["lost"] += 1
            if not (r >= bb["lo"]):
                stats["lost_cell"] += 1
            # negative controls (counted, expected > 0 except noabs)
            cl = cG(G, bb["l0"], elig_at=bb["u0"])
            if cl is None:
                cl = G["b"]
            neg["ell"] += not (s > cl)
            if x["r"] == 3:
                neg["mu2"] += not (s > cG(G, bb["u0"], mu_override=F(2)))
            ce = cG(G, bb["u0"], elig_at=bb["l0"])
            neg["elig_l"] += (ce is None) or not (s > ce)
            neg["noabs"] += not (s > cG(G, bb["u0"], absorbed=False))
print("  random/boundary roots: %d failing roots (%d from absorbed rows, %d boundary: p = u, delta = 1e-30),"
      " %d low witnesses checked, %d skipped (outside the group's radial interval or degenerate)"
      % (stats["roots"], stats["absorbed_roots"], stats["boundary"], stats["witn"], stats["skipped"]))
check("(b) every failing root (row x fails: s > c_x and H_{mu_x, xi_x} > V_x) has, for each of its low witnesses"
      " w in bin (l,u], s > c_G(u) and cell index r >= floor(c_G(u)/h) - d + 1",
      stats["lost"] == 0 and stats["lost_cell"] == 0 and stats["roots"] > 5000 and stats["absorbed_roots"] > 500,
      "lost %d / %d" % (stats["lost"] + stats["lost_cell"], stats["witn"]))
check("(c) negative controls: replacing u by l in V_t - (mu_t-1)u loses witnesses; eligibility xi_t < l instead"
      " of xi_t < u loses witnesses (mu_t = 2 for order-3 rows loses none, as [2] predicts)",
      neg["ell"] > 0 and neg["elig_l"] > 0 and neg["mu2"] == 0,
      "losses: u->l %d, mu->2 %d, elig l %d" % (neg["ell"], neg["mu2"], neg["elig_l"]))
check("(c') dropping the absorbed rows loses nothing on these roots (consistent with [3])", neg["noabs"] == 0)

# (d) the reading of 'assigned'.  An O_2 root whose failing row is (o,0) (witness 1/10 in bin L3), which also has a
# fragment p' = 371/10000 in bin L1 = (xi_G, 3 xi_G/2] that is an H_{2, xi_G} witness at U_G = S + e, but is not a
# witness of any failing row.  (1.26) for L1 excludes this root; it is retained by L3.  So 'assigned' must mean
# 'by a witness of a failing source row' (the proof's reading), not 'by any group-level witness'.
G = GR[0]
s_tot = F(10087, 10000)
fr = [F(371, 10000), F(1, 10), F(45, 100)]
fr.append(s_tot - sum(fr))
L1 = [b for b in BINS if b["G"] is G and b["j"] == 1][0]
L3 = [b for b in BINS if b["G"] is G and b["j"] == 3][0]
fails = [x for x in G["rows"] if s_tot > cV(G, x)[0] and Hobs(fr, x["xi"], x["mu"]) > cV(G, x)[1]]
pw = F(371, 10000)
grp_wit = sum(q for q in fr if q >= pw) + pw > G["U"] and pw > G["xi"]
row_wit = any(pw in witnesses(fr, x["xi"], x["mu"], cV(G, x)[1]) for x in fails)
check("(d) explicit O_2 root (s = 1.0087, fragments 0.0371, 0.1, 0.45, 0.4216; all <= z_G): row (o,0) fails with"
      " witness 0.1 in L3; 0.0371 in L1 is a group-level H_2 witness at U_G but no failing row's witness;"
      " s <= c_G(L1) (clipped there), s > c_G(L3) = b_G (retained there)",
      bool(fails) and any(x["nu"] == "o" and x["t"] == 0 for x in fails) and grp_wit and not row_wit
      and L1["l0"] < pw <= L1["u0"] and L3["l0"] < F(1, 10) <= L3["u0"] and s_tot <= L1["cG"]
      and s_tot > L3["cG"] == G["b"] and G["b"] < s_tot <= G["t"] and max(fr) <= G["z"] * h,
      "%d failing rows; c_G(L1) = %s" % (len(fails), fl(L1["cG"], 10)))

# ---------------------------------------------------------------------------------------------------------------
el = time.time() - T_START
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
print("\nruntime %.1f s, peak RSS %.0f MB" % (el, rss))
print("%d checks, %d failures" % (NCHECK[0], len(FAILS)))
for f_ in FAILS:
    print("  FAILED: " + f_)
