"""Exploration (Heuristic / exploratory), Session 57.
Twin primes inside the Friedlander-Iwaniec thin set n = a^2 + b^4 (a, b >= 1):
count n <= X with n and n+2 both prime, counted with multiplicity over (a,b), and compare
with a Bateman-Horn-type prediction sum_{(a,b)} S / (log n log(n+2)), where
S = prod_p  rho(p) / (1 - 1/p)^2,  rho(p) = #{(a,b) mod p : a^2+b^4 != 0, a^2+b^4+2 != 0 mod p} / p^2.
Usage: /usr/bin/python3 -I fi_thin_twins.py X P   (X sieve limit, P: product over p <= P)
"""
import sys, math
import numpy as np
X = int(float(sys.argv[1])); P = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
N = X + 3
s = np.ones(N, dtype=bool); s[:2] = False; s[4::2] = False
for p in range(3, int(N**0.5) + 1, 2):
    if s[p]: s[p*p::2*p] = False
def primes_upto(m):
    return [p for p in range(2, m + 1) if s[p]]
# singular series
S = 1.0; Spr = 1.0
for p in primes_upto(P):
    sq = [(a*a) % p for a in range(p)]
    q4 = [pow(b, 4, p) for b in range(p)]
    from collections import Counter
    ca = Counter(sq); cb = Counter(q4)
    good = 0
    for u, nu in ca.items():
        for v, nv in cb.items():
            t = (u + v) % p
            if t != 0 and (t + 2) % p != 0: good += nu * nv
    goodone = sum(nu*nv for u, nu in ca.items() for v, nv in cb.items() if (u+v) % p != 0)
    S *= (good / p**2) / (1 - 1/p)**2
    Spr *= (goodone / p**2) / (1 - 1/p)
print(f"X = {X:.3e}, singular series over p <= {P}: twin S = {S:.6f}, single-prime S1 = {Spr:.6f}")
for Xc in [X // 100, X // 10, X]:
    cnt = 0; cntp = 0; pred = 0.0; predp = 0.0; pairs = 0
    bmax = int(round(Xc ** 0.25)) + 1
    for b in range(1, bmax + 1):
        b4 = b**4
        if b4 + 1 > Xc: break
        amax = math.isqrt(Xc - b4)
        a = np.arange(1, amax + 1, dtype=np.int64)
        n = a*a + b4
        pairs += len(n)
        isp = s[n]
        cntp += int(isp.sum())
        cnt += int((isp & s[n + 2]).sum())
        ln = np.log(n.astype(float))
        predp += float((Spr / ln).sum())
        pred += float((S / (ln * np.log(n.astype(float) + 2))).sum())
    print(f"X={Xc:.2e}: pairs={pairs}, prime n: {cntp} (pred {predp:.0f}, ratio {cntp/predp:.4f}); "
          f"twin n,n+2: {cnt} (pred {pred:.0f}, ratio {cnt/pred:.4f})")
# negative control: drop the local factor at p=3 from S (should spoil the twin ratio)
