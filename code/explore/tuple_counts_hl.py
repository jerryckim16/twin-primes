#!/usr/bin/env python3
"""Exploration (Session 13, heuristic only): primes in translates n + H of the Lean-checked admissible
48-tuple narrow48 (diameter 236), n <= X, compared with the Hardy-Littlewood 2-tuple prediction.
Counts: N2 = #{n <= X : at least 2 of n + h_i prime}, pairs = sum_n C(#primes in n+H, 2),
HL: E[pairs] ~ sum_{i<j} S(h_j - h_i) * int_2^X dt / log(t) log(t + d)   (S = twin-prime-type singular series).
usage: tuple_counts_hl.py X"""
import sys, math
import numpy as np
from mpmath import mp, quad, log
H = [0, 2, 6, 8, 12, 20, 26, 30, 32, 36, 42, 48, 50, 56, 60, 68, 72, 78, 86, 92, 98, 102, 110, 116, 120, 126, 132,
     138, 140, 146, 152, 156, 158, 162, 168, 170, 176, 180, 182, 186, 188, 210, 212, 218, 222, 228, 230, 236]
X = int(float(sys.argv[1]))
N = X + 237
s = np.ones(N + 1, dtype=bool); s[:2] = False
for p in range(2, int(N ** 0.5) + 1):
    if s[p]:
        s[p * p::p] = False
cnt = np.zeros(X + 1, dtype=np.int16)
for h in H:
    cnt += s[h:h + X + 1]
cnt[0] = 0
N2 = int((cnt >= 2).sum()); pairs = int((cnt.astype(np.int64) * (cnt - 1) // 2).sum())
# primes for singular series
P = [p for p in range(3, 20000) if s[p]]
C2 = 1.0
for p in P:
    C2 *= 1 - 1 / (p - 1) ** 2
def S(d):
    if d % 2:
        return 0.0
    v = 2 * C2
    m = d
    while m % 2 == 0: m //= 2
    q = 3
    while q * q <= m:
        if m % q == 0:
            v *= (q - 1) / (q - 2)
            while m % q == 0: m //= q
        q += 2
    if m > 2: v *= (m - 1) / (m - 2)
    return v
mp.dps = 20
pred = 0.0
for i in range(len(H)):
    for j in range(i + 1, len(H)):
        d = H[j] - H[i]
        pred += S(d) * float(quad(lambda t: 1 / (log(t) * log(t + d)), [2, 1e3, 1e5, X]))
print("X = %.3g: n with >= 2 primes in n+H: %d; prime pairs in translates: %d; HL prediction %.0f; ratio %.5f; max primes in one translate %d"
      % (X, N2, pairs, pred, pairs / pred, int(cnt.max())))
