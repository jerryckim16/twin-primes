#!/usr/bin/env python3
"""Summary of the re-evaluated 186 loss components (code/cap6/oai186_loss_inner.json, oai186_loss_outer.json) against
Tables 2.1-2.7 of [14]: coverage (share of L^+ by table E), max deviation, and the group totals recomputed from our
raw values with the paper's own rounding (ceil to integers, Young (2.30) / inner weight (2.31), ceil to 1e-12).
-> code/cap6/oai186_loss_summary.json"""
import json, os
from fractions import Fraction as F
from math import ceil
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = json.load(open("code/oai186_tables_2_1_to_2_6.json"))
inner = json.load(open("code/cap6/oai186_loss_inner.json"))["rows"]
outer = json.load(open("code/cap6/oai186_loss_outer.json"))["rows"]
d0, nb = F(44415113, 5 * 10 ** 9), F(1000843183, 10 ** 9)
tot = 696075110
def cdiv(x):  # ceil of a Fraction
    return -((-x.numerator) // x.denominator)
res = dict(groups={})
cov = 0
maxdev = 0
allle = True
for g, rows in (("O2", outer), ("O5/2", outer), ("I2old", inner), ("I5/2old", inner), ("I2new", inner), ("I5/2new", inner)):
    trows = {r["c"]: r for r in T[g.replace("/", "") if g.startswith("I") else g]["rows"]}
    ours = {r["component"]: r for r in rows if r["group"] == g}
    Eours, Etab_done = 0, 0
    for c, r in ours.items():
        t = trows[c]
        if g.startswith("O"):
            q = F(t["q"], 10 ** 6)
            A, B = ceil(r["A"]), ceil(r["B"])
            E = cdiv((q * A + F(B) / q) / 10 ** 6)
            allle &= r["A"] <= t["A"] and r["B"] <= t["B"]
            for k in ("A", "B"):
                if t[k] >= 10 ** 6:
                    maxdev = max(maxdev, 1 - r[k] / t[k])
        else:
            kap = d0 if g.endswith("old") else nb
            A = ceil(r["A"])
            E = cdiv(kap * A / 10 ** 6)
            allle &= r["A"] <= t["A"]
            if t["A"] >= 10 ** 6:
                maxdev = max(maxdev, 1 - r["A"] / t["A"])
        Eours += E
        Etab_done += t["E"]
    tabtot = sum(r["E"] for r in trows.values())
    res["groups"][g] = dict(done=len(ours), of=len(trows), E_table_total=tabtot, E_table_done=Etab_done,
                            E_ours_done=Eours, E_equal=bool(Eours == Etab_done))
    cov += Etab_done
res.update(done=sum(v["done"] for v in res["groups"].values()), of=97, share_of_Lplus_done=cov / tot,
           all_at_most_table=bool(allle), max_rel_dev_entries_ge_1e6=maxdev)
json.dump(res, open("code/cap6/oai186_loss_summary.json", "w"), indent=1)
print(json.dumps(res, indent=1))
