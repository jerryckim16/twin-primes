#!/usr/bin/env python3
r"""songyue_compare.py -- compare our exact capped values for Song-Yue's witness with their Appendix C.

Inputs: code/cap6/check_sy236.json (capped_check.py on code/cap6/P_sy236_u.json, u = 4t, polynomial = scale * P_U),
        code/cap6/I0_sy236.json (songyue_I0.py), code/cap6/J0_sy236.json (songyue_J0.py), code/cap6/songyue236_appC.json.
Normalisations: I_file = scale^2 4^48 I_t, J_file = scale^2 4^49 J_t (u = 4t; J has one squared fibre integral).
Integer coordinates x = 10^4 t and Q = 65125^25 P_U = 5^75 521^25 P_U give I* = 10^192 5^150 521^50 I_t and
J* = 10^196 5^150 521^50 J_t; the paper's Iref = (98!)^2 I*, Jref = (99!)^2 (26!)^2 J* (we test these exactly).
usage: python3 code/songyue_compare.py [check.json] [--out code/cap6/compare_sy236.json]
"""
import sys, json
from fractions import Fraction as Fr
from math import factorial
chk = json.load(open(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "code/cap6/check_sy236.json"))
P = json.load(open("code/cap6/P_sy236_u.json"))
appc = json.load(open("code/cap6/songyue236_appC.json"))
I0 = Fr(json.load(open("code/cap6/I0_sy236.json"))["I0"])
J0 = Fr(json.load(open("code/cap6/J0_sy236.json"))["J0"])
sc = int(P["scale"])
It = Fr(chk["I_T"]) / (sc ** 2 * 4 ** 48)
Jt = Fr(chk["J_T"]) / (sc ** 2 * 4 ** 49)
lam2 = 5 ** 150 * 521 ** 50
Istar0 = 10 ** 192 * lam2 * I0
Jstar = 10 ** 196 * lam2 * Jt
Iref, Jref = int(appc["Iref"]), int(appc["Jref"])
out = {}
out["Iref_equals_98fact2_Istar0"] = (factorial(98) ** 2 * Istar0 == Iref)
JrefOurs = factorial(99) ** 2 * factorial(26) ** 2 * Jstar
out["Jref_equals_ours"] = (JrefOurs == Iref * 0 + Jref)
out["Jours_over_Jref"] = "%.20f" % float(JrefOurs / Jref)
out["Jours_minus_Jref_rel"] = "%.6e" % float((JrefOurs - Jref) / Jref)
out["JrefOurs_is_integer"] = (JrefOurs.denominator == 1)
r_T = 48 * Jt / It
r_0 = 48 * Jt / I0
out["ratio_capped_I_T_stadlmann"] = "%.12f" % float(r_T)
out["ratio_capped_I_T_polymath"] = "%.10f" % (4 * float(r_T))
out["ratio_capfree_denominator_stadlmann"] = "%.12f" % float(r_0)
out["ratio_capfree_denominator_polymath"] = "%.10f" % (4 * float(r_0))
out["criterion_48J_over_I0_gt_2001_2000"] = bool(r_0 > Fr(2001, 2000))
out["paper_Nref_over_Dref"] = "%.12f" % float(Fr(int(appc["Nref"]), int(appc["Dref"])))
out["ratio_cap_free_both_polymath"] = "%.10f" % (4 * float(48 * J0 / I0))
out["I_T_over_I0"] = "%.12f" % float(It / I0)
out["J_T_over_J0"] = "%.12f" % float(Jt / J0)
print(json.dumps(out, indent=1))
if "--out" in sys.argv:
    json.dump(out, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)
