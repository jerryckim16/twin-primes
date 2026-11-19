"""Exploration (Heuristic): carrying a twin weight along the Green-Sawhney sum.
T(X) = sum_{x,y>0, x^2+4y^2<=X} Lam(x)Lam(x+2)Lam(y) 1[x^2+4y^2 prime]   (primes only, no prime powers)
compared with
 (a) Bateman-Horn for the system {x, x+2, y, x^2+4y^2}:  S * sum_{x,y>0, region} 1/log(x^2+4y^2),
     S = prod_p (1 - nu_p/p^2)/(1-1/p)^4,  nu_p = #{(x,y) mod p : x(x+2)y(x^2+4y^2) = 0 mod p};
 (b) the 'carried' form suggested by GS (4.22)-(4.24): Lam(y) replaced by the Cramer model at level Q,
     R_Q(X) = sum Lam(x)Lam(x+2) LamCramer_Q(y) 1[x^2+4y^2 prime].
Usage: /usr/bin/python3 -I gs_twin_carry.py [X] [Q...]
"""
import sys, math
import numpy as np
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**9
QS = [int(q) for q in sys.argv[2:]] or [3, 10, 30, 100]

def odd_sieve(n):
    m = (n - 1) // 2 + 1
    s = np.ones(m, dtype=bool); s[0] = False
    for i in range(1, (math.isqrt(n) - 1) // 2 + 1):
        if s[i]:
            p = 2 * i + 1; s[(p * p - 1) // 2::p] = False
    return s
S = odd_sieve(X)
def isp(v):  # v odd >= 1
    return S[(v - 1) // 2]
def primes_upto(n):
    s = odd_sieve(max(n, 3)); return np.concatenate(([2], 2 * np.nonzero(s)[0] + 1))

# singular series
def nu(p):
    x = np.arange(p)[:, None]; y = np.arange(p)[None, :]
    v = (x * (x + 2) % p) * y % p * ((x * x + 4 * y * y) % p) % p
    return int((v == 0).sum())
SS = 1.0
for p in primes_upto(2000):
    p = int(p); SS *= (1 - nu(p) / p**2) / (1 - 1 / p) ** 4
print(f"singular series (p <= 2000): {SS:.5f}")

xs = np.arange(1, math.isqrt(X) + 1)
ys = np.arange(1, math.isqrt(X // 4) + 1)
P = primes_upto(math.isqrt(X) + 2); isP = np.zeros(math.isqrt(X) + 3, dtype=bool); isP[P] = True
tw = xs[isP[xs] & isP[xs + 2]]
wx = np.log(tw) * np.log(tw + 2)
yP = ys[isP[ys]]
T = 0.0; pred = 0.0
for y in ys:
    v = xs.astype(np.int64) ** 2 + 4 * int(y) ** 2
    pred += float((1.0 / np.log(v[v <= X].astype(np.float64))).sum())
for y in yP:
    v = tw.astype(np.int64) ** 2 + 4 * int(y) ** 2
    ok = (v <= X) & (v % 2 == 1)
    T += math.log(y) * float(wx[ok][isp(v[ok])].sum())
print(f"X = {X:.0e}: T = {T:.5e}; BH prediction {SS*pred:.5e}; ratio {T/(SS*pred):.4f}")
for Q in QS:
    pq = [int(p) for p in P if p <= Q]
    c = 1.0
    for p in pq: c *= p / (p - 1)
    mask = np.ones(len(ys), dtype=bool)
    for p in pq: mask &= (ys % p != 0)
    R = 0.0
    for y in ys[mask]:
        v = tw.astype(np.int64) ** 2 + 4 * int(y) ** 2
        ok = (v <= X) & (v % 2 == 1)
        R += c * float(wx[ok][isp(v[ok])].sum())
    print(f"  Q = {Q}: carried R_Q = {R:.5e}; T/R_Q = {T/R:.4f}")
