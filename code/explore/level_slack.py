#!/usr/bin/env python3
"""Exploration (Session 14, heuristic): would the slack in Song-Yue's exponent conditions buy one step k = 48 -> 47?
Criterion (cap-free, eps-enlarged simplex, level theta = 1/2 + 2 omega): M_{k,eps} * 2 theta > 4.
Inputs: M_{48,eps}(D22) = 3.9589046383 (code/cert_kin48_capfree_D22e.json, eps = 15/506);
        M_{47,eps} - M_{48,eps} at D16 from `mk_general.py 47|48 16 --even --eps 15/506` (run in Session 14).
Margins (fixed other parameters, from code/audit_sy236/A/numerics.out and B/exponents.py):
  Type III (52) term 1 = 2/3 + 7 omega/3 + 3/10 + 2 eta3/3 = 1 - 1/3000   -> d omega <= (1/3000)/(7/3)
  IIa (33) at gamma = 11/25 = 1 + 12 omega + 7 eta2/2 - 5 gamma/2 = -53/200000 -> d omega <= (53/200000)/12
Heuristic only: eps and the caps are themselves tied to omega, the caps cost about 3e-4 in the ratio, and
the margins can be re-tuned by moving the other parameters (eta2, tau0, s3, eta3)."""
from fractions import Fraction as F
M48_D22 = 3.9589046383
M47_D16, M48_D16 = 3.909714544387, 3.925063582362
dM = M48_D16 - M47_D16
M47_est = M48_D22 - dM
theta = F(253, 500)
need_theta = 2 / M47_est
need_domega = (need_theta - float(theta)) / 2
tIII = float(F(1, 3000) / F(7, 3)); tIIa = float(F(53, 200000) / 12)
print("dM(47->48, D16) = %.5f; M_47 (D22, estimated) = %.5f" % (dM, M47_est))
print("theta needed for k = 47: %.6f (now %.6f); d omega needed >= %.2e" % (need_theta, float(theta), need_domega))
print("d omega allowed by Type III margin: %.2e (x%.1f short); by IIa (33) margin: %.2e (x%.1f short)" % (
    tIII, need_domega / tIII, tIIa, need_domega / tIIa))
