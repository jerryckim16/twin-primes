#!/usr/bin/env python3
"""Rung 186: how much of the certified margin of [14] (OpenAI, short_gaps_numerics.pdf, Cor. 2.6 (2.35)) each loss
group uses, i.e. by how much each published group total could be too SMALL before the final inequality fails.
Exact rational arithmetic on the printed integers only (Lemma 2.5 (2.33), Table 2.7); nothing is recomputed here.
Two thresholds are reported, because which one the main paper [8, Prop. 4.6] needs is not checked by us:
  (a) margin > 0, (b) margin > 1/50000 (the value asserted in (2.35)).
Normalised margin  mu(L) = (rho* (J^- - L) - I^+) / I^+  with L = L+/I^- * I^- (I^- = lower endpoint of I_H).
usage: python3 code/oai186_margin_budget.py  -> code/cap6/oai186_margin_budget.json"""
import json, os
from fractions import Fraction as F
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rho_s = F(2624989, 10 ** 7)
Im, Ip, Jm = F(23685317816, 10 ** 24), F(23685317890, 10 ** 24), F(90248755123, 10 ** 24)
groups = {"O2": 38927522, "O5/2": 622829241, "I2old": 55254, "I5/2old": 435544, "I2new": 1405159, "I5/2new": 32422390}
tot = sum(groups.values())
assert tot == 696075110
Lp = F(tot, 10 ** 12) * Im                     # L+ <= this (Table 2.7 total, normalised by I^-)
mu = lambda L: (rho_s * (Jm - L) - Ip) / Ip
m0 = mu(Lp)
# check against (2.35): their bound uses 697/10^6 in place of the exact total
assert F(500103, 500000) - 1 - F(2624989, 10 ** 7) * F(697, 10 ** 6) == F(230382667, 10 ** 13)
res = dict(margin_with_table_total=float(m0), margin_2_35_printed=230382667e-13, groups={})
for thr_name, thr in (("gt0", F(0)), ("gt_1_50000", F(1, 50000))):
    # largest extra loss X (in units of I^-) with mu(Lp + X I^-) > thr
    X = (rho_s * (Jm - Lp) - Ip * (1 + thr)) / (rho_s * Im)
    res["slack_" + thr_name] = dict(extra_loss_over_I=float(X), relative_to_total=float(X / F(tot, 10 ** 12)))
    for g, v in groups.items():
        res["groups"].setdefault(g, dict(share_of_L=float(F(v, tot)), E_1e12=v))
        res["groups"][g]["max_factor_" + thr_name] = float(1 + X / F(v, 10 ** 12))
json.dump(res, open("code/cap6/oai186_margin_budget.json", "w"), indent=1)
print(json.dumps(res, indent=1))
