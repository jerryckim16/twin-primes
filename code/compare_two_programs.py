#!/usr/bin/env python3
"""Compare the exact I_T and J_T of capped_exact.py (result json) and capped_check.py (result json) as rationals,
and print the ratio k J_T / I_T and the one-sided Bonferroni certificate of paper Prop. prop:bonf from the pieces file
(Corr1 with j <= 2, int_V P^2 with j <= 1, all Corr2).  Session 13.
usage: compare_two_programs.py res_exact.json check.json [pieces.jsonl] [--out f.json]"""
import sys, json
from fractions import Fraction as F
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
k = a["k"]
IA, JA, IB, JB = F(a["I_T"]), F(a["J_T"]), F(b["I_T"]), F(b["J_T"])
out = dict(I_T_equal=IA == IB, J_T_equal=JA == JB, ratio_exact=float(k * JA / IA), ratio_check=float(k * JB / IB))
print(out)
if len(sys.argv) > 3 and not sys.argv[3].startswith("--"):
    I, J = F(a["I"]), F(a["J"])
    corr1, icorr, corr2 = F(0), F(0), F(0)
    for line in open(sys.argv[3]):
        if not line.strip():
            continue
        r = json.loads(line); v = F(r["v"])
        if r["kind"] == "Corr1" and r["j"] <= 2: corr1 += v
        if r["kind"] == "Icorr" and r["j"] <= 1: icorr += v
        if r["kind"] in ("Corr2b", "Corr2c"): corr2 += v
    Jlow, Iup = J - corr1 - corr2, I - icorr
    assert Jlow <= JA and Iup >= IA, "Bonferroni direction violated"
    out.update(onesided_ratio=float(k * Jlow / Iup), onesided_gt4=k * Jlow > 4 * Iup,
               loss=float(k * JA / IA - k * Jlow / Iup))
    print("one-sided (Prop. bonf): k J_low / I_up = %.12f > 4: %s; loss vs exact %.3e" % (out["onesided_ratio"], out["onesided_gt4"], out["loss"]))
if "--out" in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)
