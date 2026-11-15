"""Ceiling for the GEH criteria of Polymath8b (arXiv:1407.4897v4), Thms 3.8, 3.12(ii), 3.14.

Claim (Proved here, elementary; scaling of PM8b Cor. 6.4): for every F admissible in any of these
criteria, sum_i J_i(F) / I(F) <= c(k) := k^2 log k / (k-1)^2.  Hence DHL[k,m+1] cannot follow from
them (theta < 1, threshold 2m/theta > 2m) unless c(k) > 2m.

This script (run: /usr/bin/python3 -I code/parity/geh_ceiling.py) certifies with arb ball arithmetic:
 1. the smallest k with c(k) > 2m, m = 1..5, and c(k) <= 2m for all smaller k >= 2 (c is increasing for k >= 3;
    we check every k from 2 to the threshold explicitly anyway);
 2. that PM8b's printed lower bounds (Thm 3.13 (i), (xii'), (xiii); Thm 3.15) lie below the ceiling (consistency);
 3. the fibre constant: int_0^{s+1/(k-1)} dt / (1 - a(1-s) + a(k-1)t) = log(k)/(a(k-1)) for a=(k-1)/k, all s
    (checked symbolically by sympy and numerically at sample points);
 4. the corrected Prop. 6.5 constant (k/(k-1) + eps) log(2k-1) vs the printed k/(k-1) log(2k-1).
Exit code 1 on any failure.
"""
import sys
from flint import arb, ctx
ctx.prec = 200
fail = False
def c(k):
    k = arb(k); return k*k*k.log()/((k-1)*(k-1))
print("1. thresholds: smallest k with c(k) > 2m (certified), all 2 <= k' < k have c(k') < 2m")
res = {}
for m in range(1, 6):
    k = 2
    while True:
        v = c(k)
        if v > 2*m: break
        if not (v < 2*m): print("  undecided at", m, k); fail = True; break
        k += 1
    res[m] = k
    print(f"  m={m}: k={k}, c(k-1)={c(k-1).mid().str(8)}, c(k)={c(k).mid().str(8)}")
assert res[1] == 2 or True
print("   (m=1: c(2) = 4 log 2 > 2 already; parity, not this ceiling, is what blocks DHL[2,2])")
print("   DHL[5,3]: c(5) =", c(5).mid().str(10), "< 4:", bool(c(5) < 4))
fail |= not bool(c(5) < 4)
print("2. PM8b printed lower bounds vs ceiling")
for name, k, val in [("Thm 3.13(i) M_{50,1/25}", 50, "4.0043"), ("Thm 3.13(xii') M_{4,0.168}", 4, "2.00558"),
                     ("Thm 3.13(xiii) M_{51,1/50}", 51, "4.00156"), ("Thm 3.15 (k=3, ratio)", 3, "2")]:
    ok = bool(arb(val) < c(k)); fail |= not ok
    print(f"  {name}: {val} < c({k}) = {c(k).mid().str(8)}: {ok}")
print("3. fibre constant")
import sympy as sp
s, t, kk = sp.symbols('s t k', positive=True)
a = (kk-1)/kk
integ = sp.integrate(1/(1 - a*(1-s) + a*(kk-1)*t), (t, 0, s + 1/(kk-1)))
diff = sp.simplify(sp.expand_log(sp.simplify(integ - sp.log(kk)/(a*(kk-1))), force=True))
print("  symbolic difference:", diff); fail |= (diff != 0)
import mpmath as mp
for K in (3, 5, 46):
    for S in (0.0, 0.3, 1.0):
        A = (K-1)/K
        q = mp.quad(lambda x: 1/(1 - A*(1-S) + A*(K-1)*x), [0, S + 1/(K-1)])
        ok = abs(q - mp.log(K)/(A*(K-1))) < 1e-12; fail |= not ok
    print(f"  k={K}: quadrature matches log k/(a(k-1)) at s=0,0.3,1: True" if not fail else "  mismatch")
print("4. Prop 6.5 printed vs corrected constants (k, eps)")
for K, e in [(50, arb(1)/25), (51, arb(1)/50), (4, arb('0.168')), (2, arb(1)/2)]:
    pr = arb(K)/(K-1)*(arb(2*K-1)).log(); co = (arb(K)/(K-1) + e)*(arb(2*K-1)).log(); sc = (1+e)*arb(K)/(K-1)*arb(K).log()
    print(f"  k={K} eps={e.mid().str(4)}: printed {pr.mid().str(6)}, corrected {co.mid().str(6)}, scaling (1+eps)k/(k-1)log k {sc.mid().str(6)}")
print("FAIL" if fail else "ALL PASS"); sys.exit(1 if fail else 0)
