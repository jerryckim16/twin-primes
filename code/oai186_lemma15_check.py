#!/usr/bin/env python3
"""Rung 186: exact check of Lemma 1.5 ("Full-radius factorization", p. 10) of OpenAI's numerical companion [14]
("Numerical certificate for prime gaps at most 186", code/third_party/openai186/short_gaps_numerics.pdf).
Report: notes/oai186-lemma15-check.md.  Modelled on code/oai186_lemma14_check.py.

Lemma 1.5 (p. 10).  "If u^+ = h ceil(u/h), the residual radial factor is
      W_r = exp( theta { r h - U + (m - 1) u^+ + d h } ).                                               (1.38)
For an erased coordinate of index v, use W_{r+v} before summing over that coordinate."
It is the radial part of the low-bin Palm majorant (1.37), p. 9:
      1{witness in (l, u]} <= sum_{p in X n (l,u]} exp( theta { s + (m-1) u - U - L_{<=l} } ),          (1.37)
where (1.36) L_{<=l} < s + (m-1)u - U holds for every such witness.  The factor e^{-theta L_{<=l}} and the count
are carried by the coordinate kernels B_theta, M_theta of Lemma 2.3 (pp. 12-13); W_r is what remains.

Everything that decides a check is exact (fractions.Fraction / int); no floating point decides anything.
Sections:
  [0] source data (1.13)-(1.16), groups (1.22)-(1.24), masks (1.5); recomputed from the printed rationals;
  [1] the 61 low bins of Sec. 1.5.1 (endpoint lists U_1..U_6, slopes theta), u^+ = h ceil(u/h), (2.4) data;
  [2] the proof: the exponent identity, the full-cell correction and the bin-endpoint correction, as exact
      per-coordinate inequalities; (1.36) and the positivity needed for (1.37);
  [3] the exponent of W on every retained index r of every low bin, exactly, and the claim "their exponent is
      less than 700" (p. 16); erased-coordinate full index for the outer V form (2.20);
  [4] randomized exact end-to-end test on the actual groups and bins (d = 40 outer, 39 inner), plus explicit
      negative controls (d -> d-1, u^+ -> l, u^+ -> u - h);
  [5] consistency with the code: our oai186_loss_outer.py, oai186_loss_inner.py, oai186_loss_I2old.py,
      oai186_loss_outer2.py, and the authors' prime_gap_186_certificate.py.  The weight expressions are pulled
      out with ast and evaluated with a symbolic stand-in for arb/mpmath (exp(x) is recorded as its exact
      argument x), so the exact exponent the code would exponentiate is compared, for every retained index.
usage: python3 code/oai186_lemma15_check.py > code/oai186_lemma15_check.out"""
import ast, os, sys, random, math, io, contextlib, importlib.util, time
from fractions import Fraction as F
from math import floor, ceil
from types import SimpleNamespace

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []
NCHECK = [0]


def check(name, cond, detail=""):
    NCHECK[0] += 1
    print(("  PASS " if cond else "  FAIL ") + name + (("   [" + detail + "]") if detail else ""))
    if not cond:
        FAILS.append(name)


def cdiv(a, b):  # exact ceil for Fractions
    return -((-a) // b)


# ---------------------------------------------------------------------------------------------------------------
print("[0] source data (1.13)-(1.16), p. 4; groups (1.22)-(1.24), p. 5-6; masks (1.5), p. 2")
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
N = 98304
n = N - 40
h = S / N
check("(1.1)/(1.3): S = 2742997/2624989, h = S/98304, n = 98264",
      S == F(2742997, 2624989) and h == F(2742997, 2624989 * 98304) and n == 98264)
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
        rows.append(dict(nu=nu, t=t, r=r, xi=xi, a=a, b=b, A=a + eta, C=b + eta, terminal=(w == Om[nu])))
        wp, t = w, t + 1
        if rows[-1]["terminal"]:
            break
    lad[nu] = rows
o, nw = lad["o"], lad["n"]
check("ladders have 29 / 43 rows", (len(o), len(nw)) == (29, 43))
aa = [F(6, 5) ** j / 20 for j in range(10)]          # a_j := (6/5)^j / 20, p. 9

# groups in the stated order G1..G6 (p. 5, (1.22)-(1.24)); own rows + rows absorbed for m = 5/2 ((1.26), p. 6)
# kind 'outer': core c_t = a_t, threshold V_t = A_t;  'inner': c_t = b_t, V_t = C_t  ((1.21), p. 5)
GR = [
    dict(name="O2", kind="outer", d=40, m=F(2), xi=o[23]["xi"], U=S + e, b=nw[0]["a"], t=nw[24]["a"], z=49152,
         p=24576, face=98263, rows=o[:24] + nw[:24], absorbed=[]),
    dict(name="O5/2", kind="outer", d=40, m=F(5, 2), xi=nw[38]["xi"], U=S + e / 2, b=nw[24]["a"], t=98303 * h,
         z=46580, p=19660, face=98263, rows=o[24:28] + nw[24:39], absorbed=o[:24] + nw[:24]),
    dict(name="I2old", kind="inner", d=39, m=F(2), xi=o[23]["xi"], U=T0 + e, b=o[12]["b"], t=o[24]["b"], z=44781,
         p=22390, face=89524, rows=o[12:24], absorbed=[]),
    dict(name="I5/2old", kind="inner", d=39, m=F(5, 2), xi=o[27]["xi"], U=T0 + e / 2, b=o[24]["b"], t=89563 * h,
         z=35265, p=17912, face=89524, rows=o[24:28], absorbed=o[12:24]),
    dict(name="I2new", kind="inner", d=39, m=F(2), xi=nw[23]["xi"], U=T1 + e, b=nw[12]["b"], t=nw[24]["b"],
         z=44976, p=22488, face=89914, rows=nw[12:24], absorbed=[]),
    dict(name="I5/2new", kind="inner", d=39, m=F(5, 2), xi=nw[38]["xi"], U=T1 + e / 2, b=nw[24]["b"], t=89953 * h,
         z=35419, p=17990, face=89914, rows=nw[24:39], absorbed=nw[12:24]),
]
for G in GR:
    G["R0"] = max(0, floor(G["b"] / h) - G["d"] + 1)                 # (1.25) lower, outward
    G["R1"] = min(floor(G["t"] / h), G["face"])                      # (1.25) upper, intersected with (1.5)
    G["smax"] = (G["face"] + G["d"]) * h                             # largest physical total of the face/root
check("(1.24): p_G = h floor(U_G / (2 m_G h)) for all six groups",
      all(floor(G["U"] / (2 * G["m"] * h)) == G["p"] for G in GR))
check("(1.5): largest retained totals (N-1)h outer, 89563h base, 89953h enlarged",
      [G["smax"] for G in GR] == [98303 * h] * 2 + [89563 * h] * 2 + [89953 * h] * 2)
check("Lemma 1.1 guard xi_G > 2h > 0 and xi_G < p_G <= z_G for all groups",
      all(2 * h < G["xi"] < G["p"] * h <= G["z"] * h for G in GR))


def cG_of(G, u):
    """(1.26): c_G(u) = max{b_G, min_{t: xi_t < u} max{c_t, V_t - (mu_t - 1) u}}, absorbed rows keep own order."""
    core, thr = ("a", "A") if G["kind"] == "outer" else ("b", "C")
    el = [max(x[core], x[thr] - ((F(5, 2) if x["r"] == 3 else F(2)) - 1) * u)
          for x in G["rows"] + G["absorbed"] if x["xi"] < u]
    return None if not el else max(G["b"], min(el))


# ---------------------------------------------------------------------------------------------------------------
print("\n[1] the 61 low bins (Sec. 1.5.1, p. 9) and u^+ = h ceil(u/h)")
for G, ul in zip(GR, [
    lambda x, p: [x, 3 * x / 2, aa[0]] + aa[4:9] + [(aa[8] + aa[9]) / 2, aa[9], p],
    lambda x, p: [2 ** j * x for j in range(9)] + [F(1, 100), F(3, 200), F(9, 400), F(27, 800)] + aa[0:8]
                 + [(aa[7] + p) / 2, p],
    lambda x, p: [x, aa[0], aa[4], aa[6], aa[8], p],
    lambda x, p: [x, 2 * x, F(1, 100), F(27, 800), aa[3], aa[5], aa[6], p],
    lambda x, p: [x, aa[1], aa[4], aa[5], aa[7], aa[8], p],
    lambda x, p: [2 ** j * x for j in (0, 1, 4, 6, 8)] + [F(9, 400), aa[1], aa[3], aa[5], aa[6], aa[7], p]]):
    G["ulist"] = ul(G["xi"], G["p"] * h)
BINS = []
for gi, G in enumerate(GR):
    U_ = G["ulist"]
    for j in range(1, len(U_)):
        l0, u0 = U_[j - 1], U_[j]
        th = 120 if (gi == 0 and j == 3) else ceil((F(9) if gi == 5 else F(7)) / u0)
        L, H, K = floor(l0 / h), ceil(u0 / h), G["z"]
        cg = cG_of(G, u0)
        lo = None if cg is None else max(G["R0"], floor(cg / h) - G["d"] + 1)
        BINS.append(dict(G=G, gi=gi, name="L%d" % j, l0=l0, u0=u0, theta=th, L=L, H=H, K=K, up=H * h, cG=cg, lo=lo))
check("lists increase strictly; 10+22+5+7+6+11 = 61 low bins",
      all(all(G["ulist"][i] < G["ulist"][i + 1] for i in range(len(G["ulist"]) - 1)) for G in GR)
      and [len(G["ulist"]) - 1 for G in GR] == [10, 22, 5, 7, 6, 11] and len(BINS) == 61)
check("u^+ = h ceil(u/h) satisfies u <= u^+ < u + h on all 61 bins",
      all(b["u0"] <= b["up"] < b["u0"] + h for b in BINS),
      "u^+ = u exactly on %d bins (the bins ending at p_G)" % sum(b["up"] == b["u0"] for b in BINS))
check("(2.4) data 2 <= L < H <= K <= N on all 61 bins", all(2 <= b["L"] < b["H"] <= b["K"] <= N for b in BINS))
check("theta is a positive integer and m - 1 > 0 on all bins (needed: both multiply upper bounds)",
      all(isinstance(b["theta"], int) and b["theta"] > 0 and b["G"]["m"] - 1 > 0 for b in BINS))
check("rank-one guard used upstream: u^+ <= min(z_G, U_G/m_G) (a single fragment in the bin never fails alone)",
      all(b["up"] <= min(b["G"]["z"] * h, b["G"]["U"] / b["G"]["m"]) for b in BINS))
ne = [b for b in BINS if b["cG"] is not None]
check("every bin has a nonempty eligible set and a nonempty retained index range lo..R1 (Lemma 1.6: 'nonempty')",
      len(ne) == 61 and all(b["lo"] <= b["G"]["R1"] for b in ne))

# ---------------------------------------------------------------------------------------------------------------
print("\n[2] the proof as exact inequalities")
# Root X = (X_1..X_d), coordinate totals t_i in cells C_{j_i} = [j_i h, (j_i + 1) h), r = sum j_i, s = sum t_i.
# (1.37) term: exp(theta{s + (m-1)u - U - L_{<=l}}), L_{<=l} = total of fragments <= l.  Write
#   theta{s + (m-1)u - U - L_{<=l}} = sum_i theta(t_i - U/d) + theta(m-1)u - theta L_{<=l}.
# (a) identity  sum_i (j_i h - U/d) = r h - U  (exact, any d, any j);
# (b) full-cell correction  t_i < (j_i + 1) h  =>  sum_i theta(t_i - U/d) < theta(r h - U + d h)  (theta > 0);
# (c) bin endpoint  u <= u^+  =>  theta (m-1) u <= theta (m-1) u^+  (theta > 0, m > 1);
# hence  exp(theta{s + (m-1)u - U - L_{<=l}}) <= W_r * exp(-theta L_{<=l}), and the second factor is a product
# of per-coordinate factors exp(-theta L_i) that Lemma 2.3 puts into the coordinate kernel (the measure
# e^{-theta t} D_l(t) dt).  The slack is theta[sum_i ((j_i+1)h - t_i) + (m-1)(u^+ - u)] > 0.
rnd = random.Random(15)
ok_a = True
for _ in range(2000):
    d = rnd.choice([39, 40])
    js = [rnd.randint(0, 3000) for _ in range(d)]
    U_ = F(rnd.randint(1, 10 ** 9), 10 ** 9)
    if sum(j * h - U_ / d for j in js) != sum(js) * h - U_:
        ok_a = False
check("(a) sum_i (j_i h - U/d) = r h - U exactly (2000 random index vectors, d in {39, 40})", ok_a)
check("(b)+(c) slack theta[(m-1)(u^+ - u)] in [0, theta (m-1) h) on every bin (the r-independent part)",
      all(0 <= b["theta"] * (b["G"]["m"] - 1) * (b["up"] - b["u0"]) < b["theta"] * (b["G"]["m"] - 1) * h
          for b in BINS))
# (1.36) and positivity: if p in (l, u] has sum_{q >= p} q + (m-1)p > U, then since every q >= p exceeds l,
# sum_{q >= p} q <= s - L_{<=l}, and (m-1)p <= (m-1)u, so L_{<=l} < s + (m-1)u - U: the exponent in (1.37) is
# > 0 and the Palm sum (count >= 1) is > 1 >= indicator.  Tested exactly in [4].

# ---------------------------------------------------------------------------------------------------------------
print("\n[3] the exponent of W on every retained index of every low bin; the '< 700' claim (p. 16)")


def Wexp(b, r, d=None):
    G = b["G"]
    d = G["d"] if d is None else d
    return b["theta"] * (r * h - G["U"] + (G["m"] - 1) * b["up"] + d * h)


nidx = 0
mx = None
worst = None
mono = True
for b in ne:
    G = b["G"]
    prev = None
    for r in range(b["lo"], G["R1"] + 1):
        x = Wexp(b, r)
        nidx += 1
        if prev is not None and not x - prev == b["theta"] * h:
            mono = False
        prev = x
        if mx is None or x > mx:
            mx, worst = x, (G["name"], b["name"], r)
check("exponent increases by exactly theta h per index (so its max is at r = R1) on all %d retained (bin, r) pairs"
      % nidx, mono)
check("exponent < 700 on every retained index of every low bin (max %.4f at %s %s r=%d)" % ((float(mx),) + worst),
      mx < 700)
# per group: largest exponent, smallest exponent
for G in GR:
    bs = [b for b in ne if b["G"] is G]
    xs = [(Wexp(b, G["R1"]), b["name"]) for b in bs]
    ys = [(Wexp(b, b["lo"]), b["name"]) for b in bs]
    print("  info %-8s d=%d: retained r in [lo(u), %d]; max exponent %.4f (%s), min exponent %.4f (%s)"
          % (G["name"], G["d"], G["R1"], float(max(xs)[0]), max(xs)[1], float(min(ys)[0]), min(ys)[1]))
# erased coordinate (outer V form (2.20)): a 39-coordinate face of index sum r and an erased coordinate of index v
# form a 40-coordinate root of index r + v; its weight is W_{r+v} with d = d_G = 40, and the event mask is
# chi_G(r + v).  Since r + v ranges over the same retained set, the '< 700' check above covers it.
ok_e = True
for b in [b for b in ne if b["G"]["kind"] == "outer"]:
    for _ in range(50):
        js = [rnd.randint(0, 2500) for _ in range(39)]
        v = rnd.randint(0, 3000)
        r = sum(js)
        full = js + [v]
        if not (Wexp(b, r + v) == b["theta"] * (sum((j + 1) * h for j in full) - b["G"]["U"] + (b["G"]["m"] - 1) * b["up"])
                and Wexp(b, r + v) == Wexp(b, r) + b["theta"] * v * h):
            ok_e = False
check("erased coordinate: W_{r+v} (d = 40) = exp(theta{sum over all 40 coordinates of (j_i+1)h - U + (m-1)u^+}) "
      "= W_r e^{theta v h}", ok_e)

# ---------------------------------------------------------------------------------------------------------------
print("\n[4] randomized exact end-to-end test on the actual groups and bins, and negative controls")


def analyse(b, coords, dW=None, upW=None):
    """coords: list of d lists of fragment sizes.  Returns dict of exact quantities."""
    G = b["G"]
    d = G["d"]
    l0, u0, th, m, U = b["l0"], b["u0"], b["theta"], G["m"], G["U"]
    lgrid = b["L"] * h
    X = [q for c in coords for q in c]
    s = sum(X)
    ts = [sum(c) for c in coords]
    r = sum(floor(t / h) for t in ts)
    Lle = sum(q for q in X if q <= l0)                       # L_{<= l} at the printed endpoint l
    Llg = sum(q for q in X if q <= lgrid)                    # tilt actually used by the kernel: l = Lh
    jsm = sum(floor(sum(q for q in c if q <= lgrid) / h) for c in coords)
    Xs = sorted(X, reverse=True)
    pref, acc = {}, F(0)
    for q in Xs:
        acc += q
        pref[q] = acc                                        # inclusive prefix sum_{q' >= q} q'
    wit = [p for p in X if l0 < p <= u0 and pref[p] + (m - 1) * p > U]
    Epalm = th * (s + (m - 1) * u0 - U - Lle)
    dd = d if dW is None else dW
    up = b["up"] if upW is None else upW
    Ew = th * (r * h - U + (m - 1) * up + dd * h)
    Nker = sum(1 for q in X if lgrid <= q < b["H"] * h)
    Nbin = sum(1 for q in X if l0 < q <= u0)
    return dict(s=s, r=r, E=bool(wit), Lle=Lle, Llg=Llg, Epalm=Epalm, Ekx=Ew - th * Llg, Ekg=Ew - th * jsm * h,
                Nker=Nker, Nbin=Nbin)


def random_root(b, rnd):
    G = b["G"]
    d, m, U, z = G["d"], G["m"], G["U"], G["z"] * h
    l0, u0 = b["l0"], b["u0"]
    lo_t = b["cG"]
    hi_t = min(G["smax"], (G["R1"] + d) * h)
    st = lo_t + F(rnd.randint(0, 10 ** 6), 10 ** 6) * (hi_t - lo_t)
    p = l0 + F(rnd.randint(1, 10 ** 6 - 1), 10 ** 6) * (u0 - l0)
    Bt = U - (m - 1) * p + F(rnd.randint(-10 ** 6, 10 ** 6), 10 ** 6) * F(1, 100)
    frags = [p]
    R = min(Bt, st) - p
    while R > z:
        q = p + F(rnd.randint(0, 10 ** 6), 10 ** 6) * (z - p)
        if R - q < p:
            q = R - p
        frags.append(q)
        R -= q
    if R >= p:
        frags.append(R)
    rem = st - sum(frags)
    while rem > 0:
        q = min(rem, F(rnd.randint(1, 10 ** 6), 10 ** 6) * max(l0, rem / 20))
        frags.append(q)
        rem -= q
    coords = [[] for _ in range(d)]
    for q in frags:
        coords[rnd.randrange(d)].append(q)
    return coords


NT = 120
tot = dict(n=0, E=0, v136=0, vkx=0, vkg=0, vcov=0, vN=0, ll=0, neg_dm1=0, neg_l=0, neg_um=0)
for b in ne:
    for _ in range(NT):
        coords = random_root(b, rnd)
        x = analyse(b, coords)
        tot["n"] += 1
        tot["ll"] += (x["Llg"] > x["Lle"])
        tot["vkx"] += (x["Ekx"] <= x["Epalm"])           # Lemma 1.5 with the exact tilt: strict slack expected
        tot["vkg"] += (x["Ekg"] < x["Ekx"])              # Lemma 2.3's lower-endpoint tilt only enlarges
        tot["vN"] += (x["Nker"] < x["Nbin"])
        if x["E"]:
            tot["E"] += 1
            tot["v136"] += not (x["Lle"] < x["s"] + (b["G"]["m"] - 1) * b["u0"] - b["G"]["U"])
            tot["vcov"] += not (x["Nker"] >= 1 and x["Ekx"] > 0)
            # negative controls on the same failing roots
            tot["neg_dm1"] += analyse(b, coords, dW=b["G"]["d"] - 1)["Ekx"] < 0
            tot["neg_l"] += analyse(b, coords, upW=b["l0"])["Ekx"] < 0
            tot["neg_um"] += analyse(b, coords, upW=b["u0"] - h)["Ekx"] < 0
print("  info %d random roots (%d per bin), %d with a failing witness in the bin" % (tot["n"], NT, tot["E"]))
check("L_{<=Lh} <= L_{<=l} on every root (the kernel's rounded-down cutoff l = Lh tilts less)", tot["ll"] == 0)
check("(1.36) L_{<=l} < s + (m-1)u - U on every failing root (%d)" % tot["E"], tot["v136"] == 0 and tot["E"] > 1000)
check("Lemma 1.5: W_r e^{-theta L_{<=Lh}} > exp(theta{s+(m-1)u-U-L_{<=l}}) strictly on all %d roots" % tot["n"],
      tot["vkx"] == 0)
check("kernel's lower-endpoint tilt e^{-theta h floor(L_i/h)} >= e^{-theta L_i}: composite bound also holds",
      tot["vkg"] == 0)
check("count: #fragments in [Lh, Hh) >= #fragments in (l, u] (random p avoids the null endpoint u = Hh)",
      tot["vN"] == 0)
check("cover: on every failing root the majorant (count >= 1, exponent > 0) is > 1 >= indicator", tot["vcov"] == 0)
print("  info negative controls on the same failing roots: d -> d-1 breaks the cover on %d, u^+ -> l on %d, "
      "u^+ -> u - h on %d" % (tot["neg_dm1"], tot["neg_l"], tot["neg_um"]))
check("negative control: u^+ replaced by the lower endpoint l gives uncovered failing roots", tot["neg_l"] > 0)

# Explicit sharpness of the '+ d h' term: a failing root of O_{5/2}, last bin (u = p_G = u^+, grid aligned), inside
# the retained radial range, with every one of the 40 coordinate totals just below a grid point.  Then the
# exponent of W_r e^{-theta L} exceeds the Palm exponent by only theta * sum_i ((j_i+1)h - t_i) = 40 theta eps, and
# (d-1) h in place of d h gives a majorant < 1 on a failing root.
b = [b for b in BINS if b["G"]["name"] == "O5/2"][-1]
G = b["G"]
pw, epsl, dl = b["u0"] - h / 1000, h / 2000, h / 8          # witness just inside (l, u]; u = Hh is nu-null
Bsum = G["U"] - (G["m"] - 1) * b["u0"] + dl                  # mass of fragments >= p; failure margin dl - h/667
q1 = (Bsum - pw) / 2
coords = [[pw], [q1], [q1]] + [[] for _ in range(37)]
target = (b["lo"] + 400 + 40) * h                            # aim at a retained total
small_total = target - Bsum
for i in range(40):
    if i >= 3:
        coords[i].append(floor(small_total / 37 / h) * h)
    t = sum(coords[i])
    coords[i].append((floor(t / h) + 1) * h - epsl - t)      # small top-up: total just below the next grid point
x = analyse(b, coords)
x1 = analyse(b, coords, dW=39)
okc = (all(0 < q <= b["L"] * h for c in coords for q in c[1:]) and all(q <= G["z"] * h for c in coords for q in c)
       and x["E"] and x["Nker"] >= 1 and b["lo"] <= x["r"] <= G["R1"] and x["s"] <= G["smax"])
check("sharpness construction is a legal failing root of O5/2 L22 in the retained range (r = %d)" % x["r"], okc)
check("  with d h: majorant exponent - Palm exponent = 40 theta eps > 0 (cover holds)",
      x["Ekx"] - x["Epalm"] == 40 * b["theta"] * epsl and x["Ekx"] > 0)
check("  with (d-1) h: majorant exponent < 0 on this failing root (cover fails; so d = 40, not the face's 39, "
      "is needed for the outer erased-coordinate form)", x1["Ekx"] < 0)

# ---------------------------------------------------------------------------------------------------------------
print("\n[5] consistency with the code")


class Sym:
    """Stand-in for an arb/mpf real: exact Fraction value; .exp() returns ('exp', exact argument)."""
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v.v if isinstance(v, Sym) else F(v)

    def _o(self, x):
        return x.v if isinstance(x, Sym) else F(x)

    def __add__(self, x): return Sym(self.v + self._o(x))
    __radd__ = __add__
    def __sub__(self, x): return Sym(self.v - self._o(x))
    def __rsub__(self, x): return Sym(self._o(x) - self.v)
    def __mul__(self, x): return Sym(self.v * self._o(x))
    __rmul__ = __mul__
    def __neg__(self): return Sym(-self.v)
    def exp(self): return ("exp", self.v)
    def upper(self): return self


ZERO = ("zero",)


def assigns(tree, name):
    return [nd for nd in ast.walk(tree) if isinstance(nd, ast.Assign)
            and any(isinstance(tg, ast.Name) and tg.id == name for tg in nd.targets)]


def ev(node, ns, fname):
    return eval(compile(ast.Expression(node.value), fname, "eval"), ns)


def funcdefs(tree, names):
    return [nd for nd in ast.walk(tree) if isinstance(nd, ast.FunctionDef) and nd.name in names]


spec = importlib.util.spec_from_file_location("sd", os.path.join(HERE, "oai186_support_data.py"))
sd = importlib.util.module_from_spec(spec)
old_argv = sys.argv
sys.argv = ["x"]
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(sd)
sys.argv = old_argv
check("oai186_support_data: h and ladders (xi, a, b, A, C) agree with section [0]",
      sd.h == h and all(sd.ladders[nu][i][k] == lad[nu][i][k] for nu in lad for i in range(len(lad[nu]))
                        for k in ("xi", "a", "b", "A", "C")))
mine = {(b["G"]["name"], b["name"]): b for b in BINS}

# --- our outer and inner evaluators
for fname, kind in (("oai186_loss_outer.py", "outer"), ("oai186_loss_inner.py", "inner")):
    src = open(os.path.join(HERE, fname)).read()
    tree = ast.parse(src)
    top = [nd for nd in tree.body if isinstance(nd, ast.FunctionDef) and nd.name in ("group_data", "clip_lower",
                                                                                      "schedule")]
    ns2 = {"Fr": F, "floor": floor, "ceil": ceil}
    exec(compile(ast.Module(body=top, type_ignores=[]), fname, "exec"), ns2)
    G2 = ns2["group_data"](sd)
    main = funcdefs(tree, ["main"])[0]
    e0 = [a_ for a_ in assigns(main, "expo0")]
    lo_node = assigns(main, "lo_index")
    if kind == "outer":
        wnode = [a_ for a_ in assigns(main, "f_full") if "expo0" in ast.unparse(a_.value)]
    else:
        wnode = assigns(main, "Wr")
    check("%s: exactly one low-bin weight expression (expo0, %s) found by ast"
          % (fname, "f_full" if kind == "outer" else "Wr"), len(e0) == 1 and len(wnode) == 1 and len(lo_node) == 1)
    print("    expo0 = " + ast.unparse(e0[0].value))
    print("    %s = %s" % ("f_full" if kind == "outer" else "Wr", ast.unparse(wnode[0].value)))
    nb = nbad = nsched = nr = 0
    for g, Gx in G2.items():
        Gx["h"] = sd.h
        comps = ns2["schedule"](Gx) if kind == "outer" else ns2["schedule"](Gx, sd.h)
        for c in comps:
            if c["kind"] != "L":
                continue
            bm = mine[(g, c["name"])]
            nb += 1
            if not (c["l0"] == bm["l0"] and c["u0"] == bm["u0"] and c["theta"] == bm["theta"] and c["cG"] == bm["cG"]):
                nsched += 1
                continue
            Gm = bm["G"]
            ns3 = dict(Aq=Sym, arb=lambda v: ZERO, theta=c["theta"], UG=Gx["U"], m=Gx["m"], Hb=ceil(c["u0"] / sd.h),
                       hF=sd.h, KD=Gx["d"], R0=Gx["R0"], R1=Gx["R1"], nn=Gx["R1"] + 1, c=c, max=max, floor=floor)
            ns3["expo0"] = ev(e0[0], ns3, fname)
            ns3["lo_index"] = ev(lo_node[0], ns3, fname)
            W = ev(wnode[0], ns3, fname)
            okb = (Gx["d"] == Gm["d"] and Gx["R0"] == Gm["R0"] and Gx["R1"] == Gm["R1"] and ns3["lo_index"] == bm["lo"])
            if kind == "outer":     # f_full[r] on the full 40-coordinate index r = 0..R1, zero off lo..R1
                for r in range(len(W)):
                    want = ("exp", Wexp(bm, r)) if bm["lo"] <= r <= Gm["R1"] else ZERO
                    if W[r] != want:
                        okb = False
                        break
                    nr += bm["lo"] <= r
                okb = okb and len(W) == Gm["R1"] + 1
            else:                   # Wr[i] for r = R0 + i; pair() uses i >= lo_index - R0 only
                for i, w_ in enumerate(W):
                    if w_ != ("exp", Wexp(bm, Gm["R0"] + i)):
                        okb = False
                        break
                    nr += Gm["R0"] + i >= bm["lo"]
                okb = okb and len(W) == Gm["R1"] - Gm["R0"] + 1
            nbad += not okb
    check("%s: low-bin schedule (l, u, theta, c_G(u)) equals Sec. 1.5.1 / (1.26) on all %d %s bins"
          % (fname, nb, kind), nsched == 0 and nb == (32 if kind == "outer" else 29))
    check("%s: weight exponent = theta(rh - U + (m-1)u^+ + d h), d = %d, on every retained index (%d (bin, r) pairs),"
          " lower index = max(R0, floor(c_G/h) - d + 1)" % (fname, 40 if kind == "outer" else 39, nr), nbad == 0)
    if kind == "inner":
        pr = funcdefs(main, ["pair"])[0]
        s_ = ast.unparse(pr)
        check("%s: pair() multiplies the moment at r = R0 + i by Wr[i] and skips i < lo_index - R0" % fname,
              "wl[i] * Mt[i] * Wr[i]" in s_ and "range(max(0, lo_index - R0), NR)" in s_)
    else:
        evs = ast.unparse(funcdefs(main, ["evaluate"])[0])
        check("%s: R form (2.17) uses f_full[R0 + i] (full index) and V form uses C = correl(f_full, K^(0))" % fname,
              "q[i] * Mt[i] * f_full[R0 + i]" in evs and "correl(f_full, K) for mo, K in arrays0.items()" in evs)
        lb = ast.unparse(main)
        check("%s: erased-coordinate arrays carry no profile factor: arrays0 = {(0,): bc, (1,): mc}" % fname,
              "arrays0 = {(0,): bc, (1,): mc}" in lb)
        # correl, executed with a pure-Python polynomial stand-in on small exact data
        cor = funcdefs(main, ["correl"])[0]

        class P:
            def __init__(self, c): self.c = list(c)
            def __mul__(self, o):
                out = [F(0)] * (len(self.c) + len(o.c) - 1)
                for i, x_ in enumerate(self.c):
                    for j, y_ in enumerate(o.c):
                        out[i + j] += x_ * y_
                return P(out)
            def truncate(self, k): return P(self.c[:k])
            def coeffs(self): return list(self.c)
        okc = True
        for nn_ in (1, 7, 30):
            ns4 = dict(arb_poly=P, arb=lambda v: F(v), nn=nn_)
            exec(compile(ast.Module(body=[cor], type_ignores=[]), fname, "exec"), ns4)
            f_ = [F(rnd.randint(0, 9), rnd.randint(1, 9)) * rnd.randint(0, 1) for _ in range(nn_)]
            K_ = [F(rnd.randint(0, 9), rnd.randint(1, 9)) for _ in range(nn_ + 3)]
            got = ns4["correl"](f_, K_)
            okc = okc and got == [sum(f_[r + a_] * K_[a_] for a_ in range(nn_ - r)) for r in range(nn_)]
        check("%s: correl(f, K)(r) = sum_{a=0}^{nn-1-r} f(r+a) K(a) (W at the full index r+a, (2.20), via (2.24))"
              % fname, okc)

# --- Session-15 evaluator for I_2^old (superseded by oai186_loss_inner.py, still in the repo)
fname = "oai186_loss_I2old.py"
tree = ast.parse(open(os.path.join(HERE, fname)).read())
e0 = assigns(tree, "expo0")
wn = assigns(tree, "Wr")
kd = assigns(tree, "KD")
G = GR[2]
okI = len(e0) == 1 and len(wn) == 1
bad = 0
for bm in [b for b in BINS if b["G"] is G]:
    ns3 = dict(Aq=Sym, theta=ceil(F(7) / bm["u0"]), UG=G["U"], m=F(2), Hb=ceil(bm["u0"] / h), hF=h, KD=39,
               R0=G["R0"], R1=G["R1"])
    ns3["expo0"] = ev(e0[0], ns3, fname)
    W = ev(wn[0], ns3, fname)
    bad += ns3["theta"] != bm["theta"] or any(w_ != ("exp", Wexp(bm, G["R0"] + i)) for i, w_ in enumerate(W))
check("%s: same weight (theta = ceil(7/u), KD = 39) on all 5 I2old bins and every index R0..R1" % fname,
      okI and bad == 0 and "KD, m = 39" in open(os.path.join(HERE, fname)).read())

# --- independent second outer evaluator (O_{5/2}, bins L19..L22 only)
fname = "oai186_loss_outer2.py"
src2 = open(os.path.join(HERE, fname)).read()
tree = ast.parse(src2)
lba = funcdefs(tree, ["low_bin_arrays"])[0]
w0 = assigns(lba, "W0")
upn = assigns(lba, "up")
xn = [a_ for a_ in assigns(lba, "x") if "W0" in ast.unparse(a_.value)]
okO2 = len(w0) == 1 and len(upn) == 1 and len(xn) >= 1 and "d=40" in src2.replace(" ", "")
bad = 0
Gm = GR[1]
for bm in [b for b in BINS if b["G"] is Gm and b["name"] in ("L19", "L20", "L21", "L22")]:
    ns3 = dict(th=F(bm["theta"]), mpq=F, G=dict(U=Gm["U"], m=Gm["m"], d=40), cl=lambda v: ceil(v), u0=bm["u0"], h=h,
               hm=h)
    ns3["up"] = ev(upn[0], ns3, fname)
    ns3["W0"] = ev(w0[0], ns3, fname)
    for r in range(bm["lo"], Gm["R1"] + 1):
        ns3["r"] = r
        bad += ev(xn[0], ns3, fname) != Wexp(bm, r)
# Wcoef: C(r) = Wr[r] * sum_{a: lo <= r+a <= hi} Ea[a] K0[a] with Ea[a] = e^{theta a h}; check its index logic with
# a multiplicative stand-in W(r) = c lam^r, Ea[a] = lam^a (exp(x+y) = exp(x)exp(y) is the only analytic input).
wc = funcdefs(lba, ["Wcoef"])[0]
okw = True
for (n_, lo_, hi_) in ((12, 3, 9), (20, 0, 19), (15, 14, 14), (9, 5, 4)):
    lam, c0 = F(3, 2), F(5, 7)
    K0 = [F(rnd.randint(0, 9)) for _ in range(n_)]
    ns5 = dict(n=n_, lo=lo_, hi=hi_, Ea=[lam ** a_ for a_ in range(n_)],
               Wr=[c0 * lam ** r if r <= hi_ else 0 for r in range(n_)], min=min, max=max, range=range)
    exec(compile(ast.Module(body=[wc], type_ignores=[]), fname, "exec"), ns5)
    got = ns5["Wcoef"](K0)
    want = [sum(c0 * lam ** (r + a_) * K0[a_] for a_ in range(n_) if lo_ <= r + a_ <= hi_) if r <= hi_ else 0
            for r in range(n_)]
    okw = okw and got == want
check("%s: W0 + th r hm = theta(rh - U + (m-1)u^+ + 40h) on every retained index of L19..L22; "
      "Wcoef = sum_a chi(r+a) W(r+a) K0(a)" % fname, okO2 and bad == 0 and okw)

# --- the authors' script
src = open(os.path.join(HERE, "third_party/openai186/prime_gap_186_certificate.py")).read()
tree = ast.parse(src)
keep = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "DERIVED_INPUTS" for t in node.targets):
        break
    if isinstance(node, (ast.Assign, ast.FunctionDef)):
        keep.append(node)
keep += [nd for nd in tree.body if isinstance(nd, ast.FunctionDef) and nd.name == "source_clipped_group"]
nsU = {"F": F, "math": math, "__name__": "upstream_extract"}
exec(compile(ast.Module(body=keep, type_ignores=[]), "upstream_extract", "exec"), nsU)
UI = nsU["build_inputs"]()
ug = {g["id"]: g for g in UI["source_groups"]}
ids = ["outer_h2", "outer_h25", "old_inner_h2", "old_inner_h25", "new_inner_h2", "new_inner_h25"]
low_tasks = [t_ for t_ in UI["tasks"] if t_["kind"] == "low"]
okt = len(low_tasks) == 61
for t_ in low_tasks:
    gi = ids.index(t_["group"])
    bm = mine[(GR[gi]["name"], "L%d" % (t_["index"] + 1))]
    pa = t_["parameters"]
    okt = okt and F(pa["low"]) == bm["l0"] and F(pa["high"]) == bm["u0"] and F(pa["slope"]) == bm["theta"]
check("upstream _schedule: the 61 low tasks have exactly our (l, u, theta)", okt)
slm = funcdefs(tree, ["source_low_measures"])[0]
fl3 = [a_ for a_ in ast.walk(slm) if isinstance(a_, ast.Assign) and isinstance(a_.targets[0], ast.Tuple)
       and [getattr(e_, "id", "") for e_ in a_.targets[0].elts] == ["first", "last", "cap"]]
ret = [nd for nd in ast.walk(slm) if isinstance(nd, ast.Return)][0]
hk = [kw for kw in ret.value.keywords if kw.arg == "high"]
srcf = [f_ for f_ in funcdefs(tree, [nd.name for nd in tree.body if isinstance(nd, ast.FunctionDef)])
        if assigns(f_, "offset")][0]
off = assigns(srcf, "offset")
rad = [a_ for a_ in assigns(srcf, "radial") if "offset" in ast.unparse(a_.value)]
fib = funcdefs(tree, ["_source_fiber"])[0]
check("upstream: found last = ceil(high/step), high = last*step, offset and the radial expression by ast",
      len(fl3) == 1 and len(hk) == 1 and len(off) == 1 and len(rad) == 1)
print("    " + ast.unparse(fl3[0]))
print("    high = " + ast.unparse(hk[0].value))
print("    offset = " + ast.unparse(off[0].value))
print("    radial = " + ast.unparse(rad[0].value))
bad = nr = setdiff = 0
for t_ in low_tasks:
    gi = ids.index(t_["group"])
    bm = mine[(GR[gi]["name"], "L%d" % (t_["index"] + 1))]
    gU = ug[t_["group"]]
    pa = t_["parameters"]
    ns6 = dict(hi=F(pa["high"]), lo=F(pa["low"]), z=F(gU["hard_cap"]), step=h, int=int)
    first_, last_, cap_ = ev(fl3[0], ns6, "up")
    ns6["last"] = last_
    high_ = ev(hk[0], ns6, "up")
    cl_ = nsU["source_clipped_group"](gU, h, pa["high"])
    active = set()
    for pc in cl_["aligned_cap_pieces"]:
        active.update(range(int(pc["first_index"]), int(pc["last_index"]) + 1))
    setdiff += active != set(range(bm["lo"], GR[gi]["R1"] + 1))
    ns7 = dict(F=F, group=cl_, measures=SimpleNamespace(high=high_), count=int(cl_["dimension"]),
               engine=SimpleNamespace(hq=h, n=n), rational=Sym, rate=Sym(F(pa["slope"])), ceiling=F(cl_["ceiling"]),
               active=active, arb=lambda v: ZERO)
    ns7["offset"] = ev(off[0], ns7, "up")
    radial = ev(rad[0], ns7, "up")
    for j in range(n):
        want = ("exp", Wexp(bm, j)) if j in active else ZERO
        if radial[j] != want:
            bad += 1
            break
        nr += j in active
check("upstream: active index set of the clipped group = our lo(u)..R1 on all 61 bins", setdiff == 0)
check("upstream: radial factor = exp(theta(jh - U + (m-1)u^+ + d h)), d = dimension (40 / 39), on every active "
      "index (%d (bin, j) pairs), zero elsewhere" % nr, bad == 0)
check("upstream _source_fiber multiplies the window by the radial factor at the full index before the erased "
      "correlation ('W is a function of the full radius BEFORE erasing')",
      "window = tuple((a * b for a, b in zip(window, radial_multiplier)))" in ast.unparse(fib)
      and "reversed(window)" in ast.unparse(fib))

print("\nSUMMARY: %d checks, %d failed%s; runtime %.1f s"
      % (NCHECK[0], len(FAILS), (": " + "; ".join(FAILS)) if FAILS else "", time.time() - T_START))
sys.exit(1 if FAILS else 0)
