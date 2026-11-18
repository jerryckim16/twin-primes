#!/usr/bin/env python3
"""Fejer-averaged prime pairs and the variance of primes in short windows.

Heuristic numerical illustration for papers/parity-barrier, Remark rem:gm
(route card notes/parity-attempts/2026-11-18-pair-correlation-variance.md).

f(n) = log n on primes n <= N (theta weights; prime powers omitted), N = X.
c(j)  = sum_n f(n) f(n+j)                      (exact, all pairs inside [1, N])
V(K)  = sum_{x=-K}^{N-1} (sum_{x<n<=x+K} f(n))^2  and the exact window identity
        V(K) = K c(0) + 2 sum_{1<=j<K} (K-j) c(j)  (checked to the last bit)
I(K)  = sum_{x=0}^{N-1} (sum_{x<n<=x+K} f(n) - K)^2  (discrete Goldston-Montgomery integral)
F(K)  = sum_{1<=j<K} (K-j) c(j) / (N sum_{1<=j<K} (K-j))  (Fejer mean of c(j)/N)
HL(K) = the same mean of the singular series S(j)            (Hardy-Littlewood prediction)
LB(K) = Cauchy-Schwarz lower bound for F(K):
        (K^2 theta(N)^2/(N+K) - K c(0)) / (2 N sum_{1<=j<K}(K-j))  (exact consequence of the identity)
r(K)  = (I(K) - K N log(N/K)) / (K N), to compare with B - 1, B = 1 - gamma - log(2 pi), at large K
        (MS Thm 3 integrand H(log(x/H) + B) integrated over x <= N gives H N (log(N/H) + B - 1))
        (Montgomery-Soundararajan Conjecture / Goldston's (47); here only a numerical comparison).

Usage: /usr/bin/python3 -I code/parity/variance_fejer.py [X] [KMAX]   (default 1e8, 80; ~1-2 min, < 2 GB)
"""
import sys, math
import numpy as np

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 80
N = X

# sieve
s = np.ones(N + 1, dtype=bool); s[:2] = False
for p in range(2, int(N ** 0.5) + 1):
    if s[p]:
        s[p * p::p] = False
P = np.nonzero(s)[0]
w = np.log(P.astype(np.float64))
f = np.zeros(N + 1, dtype=np.float64); f[P] = w

# correlations c(j), j = 0..KMAX (exact float sums of products; long-double accumulation)
c = np.zeros(KMAX + 1, dtype=np.longdouble)
for j in range(KMAX + 1):
    m = P + j <= N
    q = P[m]
    c[j] = np.sum((w[m] * f[q + j]).astype(np.longdouble))

theta = float(np.sum(w.astype(np.longdouble)))

# prefix sums for windows
S = np.concatenate([[0.0], np.cumsum(f[1:].astype(np.longdouble))])  # S[t] = sum_{n<=t} f(n), t=0..N

def window(K, lo, hi):
    """W(x) = S[min(x+K,N)] - S[max(x,0)] for x in [lo, hi)."""
    x = np.arange(lo, hi)
    a = np.clip(x + K, 0, N); b = np.clip(x, 0, N)
    return S[a] - S[b]

C2 = 0.66016181584686957392781211
small_primes = [p for p in range(3, KMAX + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
def Ssing(j):
    if j % 2:
        return 0.0
    v = 2 * C2
    for p in small_primes:
        if j % p == 0:
            v *= (p - 1) / (p - 2)
    return v

gamma = 0.57721566490153286
B = 1 - gamma - math.log(2 * math.pi)
L = math.log(X)
print(f"X = N = {X:.3e}, log X = {L:.4f}, theta(N)/N = {theta / N:.8f}, KMAX = {KMAX}")
print(f"c(0)/(N log N - N) = {float(c[0]) / (N * L - N):.6f};  B = 1 - gamma - log 2pi = {B:.6f}, B - 1 = {B - 1:.6f}")
print("identity check: K, V(K) direct, V(K) from c, relative difference")
for K in (1, 2, 3, 7, 40):
    Wf = window(K, -K, N)
    Vd = np.sum(Wf * Wf)
    Vc = K * c[0] + 2 * sum((K - j) * c[j] for j in range(1, K))
    print(f"  {K:3d} {float(Vd):.12e} {float(Vc):.12e} {float((Vd - Vc) / Vd):.2e}")

print("second difference: (V(3) - 2V(2) + V(1))/2 vs c(2)")
V = {}
for K in (1, 2, 3):
    Wf = window(K, -K, N); V[K] = np.sum(Wf * Wf)
print(f"  {float((V[3] - 2 * V[2] + V[1]) / 2):.10e}  {float(c[2]):.10e}")

print("\n   K    K/logX     F(K)    HL(K)    LB(K)   1-logX/K   I(K)/(KN log(N/K))   r(K)")
Ks = sorted(set([1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 37, 40, 48, 56, 64, 74, KMAX]))
rows = []
for K in Ks:
    if K > KMAX:
        continue
    Wf = window(K, 0, N) - K
    IK = float(np.sum(Wf * Wf))
    if K >= 2:
        den = sum(K - j for j in range(1, K))
        F = float(sum((K - j) * c[j] for j in range(1, K))) / (N * den)
        HL = sum((K - j) * Ssing(j) for j in range(1, K)) / den
        LB = (K * K * theta ** 2 / (N + K) - K * float(c[0])) / (2 * N * den)
        fs = f"{F:8.5f} {HL:8.5f} {LB:8.4f} {1 - L / K:9.4f}"
    else:
        fs = f"{'-':>8} {'-':>8} {'-':>8} {'-':>9}"
    ratio = IK / (K * N * math.log(N / K))
    r = (IK - K * N * math.log(N / K)) / (K * N)
    print(f"{K:4d} {K / L:8.3f}  {fs}     {ratio:10.6f}        {r:8.4f}")
print("\n(F, HL, LB: Fejer means normalised by N; r(K) -> B - 1 is the Montgomery-Soundararajan / Goldston prediction"
      " for large K; at bounded K the lower-order term depends on K arithmetically.)")
