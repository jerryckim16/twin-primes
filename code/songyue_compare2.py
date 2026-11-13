#!/usr/bin/env python3
"""Second-program check of the capped numerator of the Song-Yue 236 witness.

Compares J_T from capped_exact.py --jonly (cap-free J minus the corrections Corr1, Corr2b, Corr2c, computed piece by
piece in code/capped_exact.py) with J_T from code/capped_check.py (direct sum over large sets; the program whose
J_T was matched with the authors' Jref integer in code/songyue_compare.py).  Equality is exact equality of rationals.
Also reports 48 J_T / I0 (I0 = cap-free I, which capped_exact.py --jonly uses as denominator: the Song-Yue criterion).

usage: python3 code/songyue_compare2.py code/cap6/res_sy236_jonly.json code/cap6/check_sy236.json [out.json]
"""
import json, sys
from fractions import Fraction as Fr

res = json.load(open(sys.argv[1]))
chk = json.load(open(sys.argv[2]))
JT_exact = Fr(res["J_T"])
JT_check = Fr(chk["J_T"])
I0 = Fr(res["I"])
k = int(res["k"])
ratio = k * JT_exact / I0
out = {
    "J_T_equal": JT_exact == JT_check,
    "J_T_exact_float": float(JT_exact),
    "J_T_check_float": float(JT_check),
    "ratio_48JT_over_I0_polymath": "%.10f" % float(ratio),
    "ratio_48JT_over_I0_stadlmann": "%.12f" % float(ratio / 4),
    "criterion_gt_2001_2000": ratio / 4 > Fr(2001, 2000),
    "ratio_with_check_I_T": "%.10f" % float(k * JT_check / Fr(chk["I_T"])),
    "I_T_over_I0": "%.12f" % float(Fr(chk["I_T"]) / I0),
}
print(json.dumps(out, indent=1))
if len(sys.argv) > 3:
    json.dump(out, open(sys.argv[3], "w"), indent=1)
