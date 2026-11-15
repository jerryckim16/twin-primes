#!/usr/bin/env python3
"""Heuristic illustration (parity paper, thread 3): the Lambda_2 twin sum and its two pieces.

Bombieri's asymptotic sieve (as quoted by Ford, arXiv:math/0401215v1, (1.3)) gives, under EH for the
sequence a_n = Lambda(n+2), sum_{n<=x} Lambda(n+2) Lambda_2(n) ~ 2 H x log x with H = 2 S_2.
Lambda_2 = Lambda*log + Lambda*Lambda, so the sum splits into
   P(x) = sum Lambda(n+2) Lambda(n) log n          (twin primes)
   Q(x) = sum Lambda(n+2) (Lambda*Lambda)(n)       (n a product of two prime powers' worth: p q or p^k)
Hardy-Littlewood predicts P ~ Q ~ 2 S_2 (x log x - x). Also the localised piece of Debouzy
(arXiv:1907.06393v1, Cor. 0.3): (1/g) sum Lambda(n+2) sum_{d1 d2 = n, d1 <= n^g} Lambda(d1)Lambda(d2)/log n,
which she shows (under EH, together with the prime piece) to sum to 2 S_2 x (1+o(1)).
Usage: python3 -I bombieri_twin_split.py [x]   (default 10^8; numpy; ~1.5 GB at 10^8)
"""
import sys, math
import numpy as np

x = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
N = x + 3
spf = np.zeros(N, dtype=np.int32)
r = int(math.isqrt(N)) + 1
spf[2::2] = 2
for p in range(3, r, 2):
    if spf[p] == 0:
        s = spf[p*p::2*p]
        s[s == 0] = p
spf[1] = 1
mask = spf == 0
spf[mask] = np.arange(N, dtype=np.int32)[mask]   # primes are their own spf
del mask

def strip(m):
    """For an int64 array m: (p, k, rest) with p = spf(m), p^k || m."""
    p = spf[m].astype(np.int64)
    k = np.zeros_like(m); rest = m.copy()
    while True:
        d = (rest % p == 0) & (rest > 1)
        if not d.any():
            break
        rest = np.where(d, rest // p, rest); k += d
    return p, k, rest

# Lambda(n+2): n+2 a prime power
m = np.arange(1, x + 1, dtype=np.int64) + 2
p, k, rest = strip(m)
pp = rest == 1
n = (m - 2)[pp]; lam2 = np.log(p[pp].astype(np.float64))     # Lambda(n+2)
n_ok = n >= 2
n = n[n_ok]; lam2 = lam2[n_ok]
# factor n
p1, k1, r1 = strip(n)
lp1 = np.log(p1.astype(np.float64))
logn = np.log(n.astype(np.float64))
is_pk = r1 == 1
LamN = np.where(is_pk, lp1, 0.0)
P = float(np.sum(lam2 * LamN * logn))
# second prime
r1s = np.where(is_pk, 2, r1)            # dummy for prime powers
p2, k2, r2 = strip(r1s)
two = (~is_pk) & (r2 == 1)
lp2 = np.log(p2.astype(np.float64))
LL = np.where(is_pk, (k1 - 1) * lp1 * lp1, 0.0) + np.where(two & (k1 == 1) & (k2 == 1), 2 * lp1 * lp2, 0.0)
# p^a q^b with a+b >= 3: Lambda*Lambda(n) = 0 unless a = b = 1 (Lambda(d1)Lambda(d2) needs d1, d2 prime powers)
Q = float(np.sum(lam2 * LL))
S2 = 1.0
for q in range(3, 10**6):
    if spf[q] == q:
        S2 *= q * (q - 2) / (q - 1) ** 2
main = 2 * S2 * (x * math.log(x) - x)
print(f"x = {x:.3e}, S_2 = {S2:.10f}")
print(f"P/main = {P/main:.6f}   (twin primes, weight Lambda(n) log n)")
print(f"Q/main = {Q/main:.6f}   (Lambda*Lambda piece)")
# untwisted baseline: sum_{n<=x} (Lambda*Lambda)(n) / (x log x - x), same secondary terms if the parity pieces balance
allm = np.arange(2, x + 1, dtype=np.int64)
a1, b1, c1 = strip(allm); la = np.log(a1.astype(np.float64))
c1s = np.where(c1 == 1, 2, c1); a2, b2, c2 = strip(c1s); lb = np.log(a2.astype(np.float64))
base = float(np.sum(np.where(c1 == 1, (b1 - 1) * la * la, 0.0)) + np.sum(np.where((c1 > 1) & (c2 == 1) & (b1 == 1) & (b2 == 1), 2 * la * lb, 0.0)))
del allm, a1, b1, c1, c1s, a2, b2, c2, la, lb
print(f"baseline sum (Lambda*Lambda)(n) / (x log x - x) = {base/(x*math.log(x)-x):.6f}  (Q/main should track this)")
print(f"(P+Q)/(2 main) = {(P+Q)/(2*main):.6f}   (Bombieri under EH: -> 1)")
# Debouzy localisation: only squarefree n = p1 p2, ordered pairs (d1, d2) with d1 <= n^g
for g in (0.1, 0.25, 0.5, 0.75):
    sel = two & (k1 == 1) & (k2 == 1)
    w = np.where(sel, (lp1 <= g * logn).astype(np.float64) + (lp2 <= g * logn).astype(np.float64), 0.0)
    D = float(np.sum(lam2 * w * lp1 * lp2 / logn)) / g
    Pp = float(np.sum(lam2 * LamN))
    mainx = 2 * S2 * x
    print(f"g = {g}: prime piece / 2S2x = {Pp/mainx:.6f}, localised semiprime piece / 2S2x = {D/mainx:.6f}, sum/(2 * 2S2x) = {(Pp+D)/(2*mainx):.6f}")
