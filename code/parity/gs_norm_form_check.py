"""Sanity check of the main term in Green-Sawhney, arXiv:2410.04189v3, Prop. 4.1 (l = 0, n = 4):
   sum_{x,y in Z, x^2+4y^2 <= X} Lam'(x) Lam'(y) 1[x^2+4y^2 prime]  ~  pi*kappa_4/sqrt(4) * X/log X,
with Lam'(m) = log|m| for |m| prime.  We compare with the Li-form pi*kappa_4/2 * li-type integral
  int_2^X dt/log t  (same leading term), printing both ratios.  Heuristic/numerical only.
Usage: /usr/bin/python3 -I gs_norm_form_check.py [X] [PKAPPA]
"""
import sys, math
import numpy as np

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**9
PK = int(float(sys.argv[2])) if len(sys.argv) > 2 else 10**8

def odd_sieve(n):            # s[i] True iff 2i+1 prime, 2i+1 <= n
    m = (n - 1) // 2 + 1
    s = np.ones(m, dtype=bool); s[0] = False
    for i in range(1, (math.isqrt(n) - 1) // 2 + 1):
        if s[i]:
            p = 2 * i + 1
            s[(p * p - 1) // 2::p] = False
    return s

def primes_upto(n):
    s = odd_sieve(n)
    return np.concatenate(([2], 2 * np.nonzero(s)[0] + 1))

# kappa_4 = prod_{p = 1 mod 4} p(p-3)/(p-1)^2 * prod_{p = 2 or 3 mod 4} p/(p-1)   (conditionally convergent)
P = primes_upto(PK).astype(np.float64)
f = np.where(P % 4 == 1, P * (P - 3) / (P - 1) ** 2, P / (P - 1))
logk = np.cumsum(np.log(f))
kap = math.exp(logk[-1])
# convergence display at a few cut-offs
for c in (10**6, 10**7, PK):
    i = np.searchsorted(P, c, side='right') - 1
    print(f"kappa_4 partial product up to {c:.0e}: {math.exp(logk[i]):.6f}")
print(f"kappa_4 ~ {kap:.6f};  FI constant c = pi*kappa_4/8 = {math.pi*kap/8:.6f}")

S = odd_sieve(X)
def isprime_arr(v):          # v odd, <= X
    return S[(v - 1) // 2]
px = primes_upto(math.isqrt(X))
py = primes_upto(math.isqrt(X // 4))
tot = 0.0
lx = np.log(px.astype(np.float64))
for q in py:                 # y = +-q ; x = +-p ; norms x^2+4y^2 depend on |x|,|y| -> factor 4
    v = px.astype(np.int64) ** 2 + 4 * int(q) ** 2
    ok = (v <= X) & (v % 2 == 1)
    vv = v[ok]
    pr = isprime_arr(vv)
    tot += 4 * math.log(q) * float(lx[ok][pr].sum())
# x = +-2: 4+4y^2 even -> never prime; y = +-2 included above (q=2): x^2+16
# int_2^X dt/log t by mpmath
import mpmath
LI = float(mpmath.li(X) - mpmath.li(2))
main1 = math.pi * kap / 2 * X / math.log(X)
main2 = math.pi * kap / 2 * LI
print(f"X = {X:.0e}: sum = {tot:.6e}")
print(f"  ratio to pi*kappa_4/2 * X/log X     : {tot/main1:.5f}")
print(f"  ratio to pi*kappa_4/2 * int dt/log t: {tot/main2:.5f}")
