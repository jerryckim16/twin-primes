#!/usr/bin/env python3
"""Rung 186 (Session 14 follow-up): exact arithmetic checks of the loss-bound tables of OpenAI's numerical
companion (short_gaps_numerics.pdf, Sec. 2.4, Tables 2.1-2.7, (2.30)-(2.35)), from the integers transcribed in
code/oai186_tables_2_1_to_2_6.json (parsed from `pdftotext -layout` of the PDF supplied by Jerry Kim, 14 Nov 2026).
This checks only the bookkeeping that turns the 97 raw component bounds (A, B) into the weighted bounds E and L^+;
it does NOT recompute any raw bound R_j, V_j, beta_G (that needs the forms (2.16)-(2.21)).
Checks:
  outer (2.30): c = q/10^6, c A/10^18 + B/(10^18 c) <= E/10^12  (exact rationals);
  inner (2.31): kappa_G A/10^18 <= E/10^12, kappa = d0 (old), 1 - b_h (new);
  group totals = sum of E; grand total 696075110 < 697 * 10^6; the low / rank-two / high counts of Table 2.7
  and of the schedule of Sec. 1.5.1 (U- and T-lists); the margin arithmetic (2.34)-(2.35).
Also reports how close each Young parameter is to its optimum sqrt(B/A) (information only)."""
import json, math
from fractions import Fraction as F
T = json.load(open("code/oai186_tables_2_1_to_2_6.json"))
d0 = F(44415113, 5000000000)
one_minus_bh = F(1000843183, 10 ** 9)
KAPPA = {"I2old": d0, "I52old": d0, "I2new": one_minus_bh, "I52new": one_minus_bh}
TOTALS_27 = {"O2": 38927522, "O5/2": 622829241, "I2old": 55254, "I52old": 435544, "I2new": 1405159, "I52new": 32422390}
COUNTS_27 = {"O2": (10, 6, 1), "O5/2": (22, 12, 1), "I2old": (5, 1, 1), "I52old": (7, 2, 1), "I2new": (6, 4, 1), "I52new": (11, 5, 1)}
out = {"rows": 0, "failures": [], "groups": {}}
grand = 0
young_eff = []
for G, tab in T.items():
    rows = tab["rows"]
    s = 0
    for r in rows:
        out["rows"] += 1
        if G in ("O2", "O5/2"):
            c = F(r["q"], 10 ** 6)
            lhs = c * F(r["A"], 10 ** 18) + F(r["B"], 10 ** 18) / c
            ok = lhs <= F(r["E"], 10 ** 12)
            if r["A"] > 0:
                copt = math.sqrt(r["B"] / r["A"])
                young_eff.append(float(lhs / (2 * F(math.isqrt(r["A"] * r["B"]) + 1, 10 ** 18))))
        else:
            lhs = KAPPA[G] * F(r["A"], 10 ** 18)
            ok = lhs <= F(r["E"], 10 ** 12)
        if not ok:
            out["failures"].append((G, r["c"]))
        s += r["E"]
    lo = sum(1 for r in rows if r["c"].startswith("L")); rk = sum(1 for r in rows if r["c"].startswith("P")); hi = sum(1 for r in rows if r["c"] == "H")
    out["groups"][G] = dict(n=len(rows), sum_E=s, printed_total=tab["total"], table27=TOTALS_27[G],
                            total_ok=(s == tab["total"] == TOTALS_27[G]), counts=(lo, rk, hi), counts_ok=((lo, rk, hi) == COUNTS_27[G]))
    grand += s
out["grand_total"] = grand
out["grand_ok"] = grand == 696075110 and F(grand, 10 ** 12) < F(697, 10 ** 6)
out["n_components"] = out["rows"]
out["young_parameters"] = sum(len(T[G]["rows"]) for G in ("O2", "O5/2"))
# schedule of Sec. 1.5.1: number of endpoints of the U- and T-lists -> number of intervals
U_len = [3 + 5 + 3, 9 + 4 + 8 + 2, 6, 8, 7, 5 + 7]
T_len = [7, 9 + 4, 2, 3, 5, 6]
order = ["O2", "O5/2", "I2old", "I52old", "I2new", "I52new"]
out["schedule_ok"] = all(U_len[i] - 1 == COUNTS_27[g][0] and T_len[i] - 1 == COUNTS_27[g][1] for i, g in enumerate(order))
out["low_total"] = sum(COUNTS_27[g][0] for g in order)
# (2.34)-(2.35)
rho_s = F(2624989, 10 ** 7)
out["margin_234"] = str(rho_s * F(90248755123, 1) / F(23685317890, 1) - F(500103, 500000))
out["margin_234_ok"] = rho_s * F(90248755123) / F(23685317890) - F(500103, 500000) == F(18806715247, 236853178900000000)
m235 = F(500103, 500000) - 1 - rho_s * F(697, 10 ** 6)
out["margin_235"] = str(m235)
out["margin_235_ok"] = m235 == F(230382667, 10 ** 13) and m235 > F(1, 50000)
out["young_lhs_over_optimum_max"] = max(young_eff)
print(json.dumps(out, indent=1))
json.dump(out, open("code/oai186_tables_check.json", "w"), indent=1)
