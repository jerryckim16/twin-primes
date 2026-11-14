#!/usr/bin/env python3
"""Rung 186 (Session 14 follow-up): recompute, in exact rational arithmetic, the source data of OpenAI's numerical
companion (short_gaps_numerics.pdf, Sec. 1.3, (1.13)-(1.20), (1.23)-(1.24), Lemma 1.1) from its printed rational
definitions, and compare with every printed consequence:
  * (1.1) S, rho*, T0, T1, rho from (1.13);
  * the old/new ladders (1.15): row counts 29 / 43, order counts (12,12,5) / (12,12,19), and the enclosures of
    10^6 omega per order block in the proof of Lemma 1.1;
  * (1.17): (A, C) = (S + e, T_nu + e) (orders 1-2) and (S + e/2, T_nu + e/2) (order 3) on nonterminal rows;
  * the retained rows (1.20) via B < S_box + T_nu,box, and the four boundary values floor(B/h);
  * the continuous caps (1.18) and, through the grid rule (1.19), the integer masks (1.5) used by our I_H / J
    evaluators (code/oai186_IH.py, code/oai186_J.py, which took (1.5) as given);
  * the group table (1.23)-(1.24): z_G/h and p_G/h = floor(U_G / (2 m_G h)), and the guards of Lemma 1.1
    (xi_G > 2h, xi_G < p_G <= z_G, z_G + m_G p_G <= U_G, min xi_t > 33e-6), and 1 - 4 rho* |b_h|.
Our reading of garbled spots: in (1.15) the "t" after "min Omega_nu," is the subscript of r_t; B_{nu,t} (no
superscript) in (1.16) is the lower value (1/2 + 2 omega_{t-1})/rho; nu = o uses T_o = T0, nu = n uses T_n = T1.
usage: oai186_support_data.py [--out f.json]"""
import sys, json
from fractions import Fraction as F
from math import floor

g0, eps_o, eps_n, tau = F(1, 10 ** 7), F(1, 10 ** 6), F(1, 10 ** 7), F(1, 10 ** 10)
sigma0 = F(100001, 10 ** 6)
sigma_m = F(1, 2) - F(40481, 100000) + tau
Om = {"o": F(12499, 10 ** 6), "n": F(253, 20000)}
rho = F(1, 4) + Om["o"]
rhos = rho - g0
S = F(2742997, 10 ** 7) / rhos
T1 = F(251, 1000) / rhos
T0 = 2 - F(3, 1000) - S
e = g0 / rho
zeta = F(19037, 100000) / rho
N = 98304
h = S / N
res = {}
chk = res.setdefault("checks", {})
chk["S"] = S == F(2742997, 2624989)
chk["rho*"] = rhos == F(2624989, 10 ** 7)
chk["T0"] = T0 == F(2499106033, 2624989000)
chk["T1"] = T1 == F(2510000, 2624989)
chk["rho"] = rho == F(262499, 10 ** 6)
TT = {"o": T0, "n": T1}
eps = {"o": eps_o, "n": eps_n}
cs = {"o": {1: ((1 - 5 * sigma0) / 15, F(18, 5)), 2: ((1 - 4 * sigma0) / 16, F(7, 2)), 3: (F(3, 80), F(3))},
      "n": {1: ((1 - 5 * sigma_m) / 15, F(18, 5)), 2: ((1 - 4 * sigma_m) / 16, F(7, 2)), 3: ((1 - 2 * sigma_m) / 20, F(16, 5))}}
def rt(t):
    return 1 if t < 12 else (2 if t < 24 else 3)
ladders = {}
for nu in ("o", "n"):
    E = rho * (S + TT[nu]) - F(1, 2)
    rows = []
    wprev = F(0)
    t = 0
    while True:
        r = rt(t)
        c, s = cs[nu][r]
        w = min(Om[nu], (c - eps[nu] - E + 2 * wprev - g0) / s)
        delta = c - s * w - eps[nu]
        Bm = (F(1, 2) + 2 * wprev) / rho
        Bp = (F(1, 2) + 2 * w) / rho
        xi = delta / rho
        a, b = Bm - TT[nu], Bm - S
        eta = xi if r <= 2 else (xi + S + TT[nu] - Bm) / 2
        A, Cc = a + eta, b + eta
        terminal = (w == Om[nu])
        rows.append(dict(t=t, r=r, w=w, delta=delta, B=Bm, Bp=Bp, xi=xi, a=a, b=b, eta=eta, A=A, C=Cc,
                         nonterm_identity=(delta - E + 2 * wprev == g0) if not terminal else None))
        wprev = w
        t += 1
        if terminal:
            break
    ladders[nu] = rows
chk["row_counts"] = (len(ladders["o"]), len(ladders["n"])) == (29, 43)
oc = {nu: tuple(sum(1 for x in ladders[nu] if x["r"] == r) for r in (1, 2, 3)) for nu in ladders}
chk["order_counts"] = oc["o"] == (12, 12, 5) and oc["n"] == (12, 12, 19)
res["order_counts"] = {k: list(v) for k, v in oc.items()}
encl = {}
for nu in ladders:
    encl[nu] = []
    for r in (1, 2, 3):
        ws = [x["w"] for x in ladders[nu] if x["r"] == r]
        encl[nu].append([floor(min(ws) * 10 ** 6), -floor(-max(ws) * 10 ** 6)])
res["omega_enclosures_1e6"] = encl
chk["omega_table"] = encl["o"] == [[2533, 5696], [7051, 8855], [10332, 12499]] and encl["n"] == [[2676, 6018], [7267, 8932], [10326, 12650]]
# (1.17) on nonterminal rows
ok17 = True
for nu in ladders:
    for x in ladders[nu][:-1]:
        if not x["nonterm_identity"]:
            ok17 = False
        want = (S + e, TT[nu] + e) if x["r"] <= 2 else (S + e / 2, TT[nu] + e / 2)
        if (x["A"], x["C"]) != want:
            ok17 = False
chk["(1.17)"] = ok17
# retained rows (1.20)
Sbox, Tbox = 98303 * h, {"o": 89563 * h, "n": 89953 * h}
ret = {nu: [x["t"] for x in ladders[nu] if x["B"] < Sbox + Tbox[nu]] for nu in ladders}
chk["retained"] = ret["o"] == list(range(28)) and ret["n"] == list(range(39))
fl = lambda x: floor(x / h)
bvals = {"o27": fl(ladders["o"][27]["B"]), "o28": fl(ladders["o"][28]["B"]), "n38": fl(ladders["n"][38]["B"]), "n39": fl(ladders["n"][39]["B"])}
res["boundary_floor_B_over_h"] = bvals
chk["boundary"] = bvals == {"o27": 187773, "o28": 188087, "n38": 188254, "n39": 188256}
chk["pair_maxima"] = (Sbox + Tbox["o"]) / h == 187866 and (Sbox + Tbox["n"]) / h == 188256
chk["B+ = B_next"] = all(ladders[nu][i]["Bp"] == ladders[nu][i + 1]["B"] for nu in ladders for i in range(len(ladders[nu]) - 1))
xis = [x["xi"] for nu in ladders for x in ladders[nu] if x["t"] in ret[nu]]
chk["min_xi"] = min(xis) > F(33, 10 ** 6) > F(22, 10 ** 6) > 2 * h
# caps (1.18) and masks (1.5) via (1.19)
L_n24 = 23 * ladders["n"][24]["C"] / 40
caps = {
    "outer": (40, [(F(0), ladders["n"][0]["a"], zeta), (ladders["n"][0]["a"], ladders["n"][24]["a"], (S + e) / 2),
                   (ladders["n"][24]["a"], S, S + e / 2 - 23 * (T1 + e / 2) / 40)]),
    "base": (39, [(F(0), ladders["o"][12]["b"], zeta), (ladders["o"][12]["b"], ladders["o"][24]["b"], (T0 + e) / 2),
                  (ladders["o"][24]["b"], T0, 63 * (T0 + e / 2) / 160)]),
    "enlarged": (39, [(F(0), ladders["n"][12]["b"], zeta), (ladders["n"][12]["b"], ladders["n"][24]["b"], (T1 + e) / 2),
                      (ladders["n"][24]["b"], T1, 63 * (T1 + e / 2) / 160)]),
    "full": (39, [(F(0), S, zeta)]),
}
masks = {}
for dom, (d, shells) in caps.items():
    rowsm = []
    for (l, u, z) in shells:
        lo = 0 if l == 0 else max(0, floor(l / h) - d + 1)
        hi = min(98263, floor(u / h) - d)
        rowsm.append([lo, hi, floor(z / h)])
    masks[dom] = rowsm
res["masks"] = masks
printed = {"outer": [[0, 89196, 68225], [89197, 95598, 49152], [95599, 98263, 46580]],
           "base": [[0, 84930, 68225], [84931, 87194, 44781], [87195, 89524, 35265]],
           "enlarged": [[0, 85161, 68225], [85162, 87249, 44976], [87250, 89914, 35419]],
           "full": [[0, 98263, 68225]]}
chk["masks_(1.5)"] = masks == printed
# group table (1.23)-(1.24)
o, nn = ladders["o"], ladders["n"]
G = {"O2": (2, o[23]["xi"], S + e, 49152, 24576), "O5/2": (F(5, 2), nn[38]["xi"], S + e / 2, 46580, 19660),
     "I2old": (2, o[23]["xi"], T0 + e, 44781, 22390), "I5/2old": (F(5, 2), o[27]["xi"], T0 + e / 2, 35265, 17912),
     "I2new": (2, nn[23]["xi"], T1 + e, 44976, 22488), "I5/2new": (F(5, 2), nn[38]["xi"], T1 + e / 2, 35419, 17990)}
gres = {}
gok = True
for g, (m, xi, U, zh, ph) in G.items():
    p_calc = floor(U / (2 * m * h))
    zG, pG = zh * h, p_calc * h
    guards = dict(p_over_h=p_calc, p_matches=(p_calc == ph), xi_gt_2h=xi > 2 * h, xi_lt_p=xi < pG, p_le_z=pG <= zG,
                  z_plus_mp_le_U=zG + m * pG <= U, maxpxi_le_U_over_m1=max(pG, xi) <= U / (m + 1))
    gres[g] = guards
    gok = gok and all(v for k, v in guards.items() if k != "p_over_h")
res["groups"] = gres
chk["groups"] = gok
bh = F(-843183, 10 ** 9)
chk["1-4rho*|bh|"] = 1 - 4 * rhos * abs(bh) == F(2497786653900013, 2500000000000000)
res["all_ok"] = all(chk.values())
print(json.dumps(res, indent=1, default=str))
if "--out" in sys.argv:
    json.dump(res, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1, default=str)
