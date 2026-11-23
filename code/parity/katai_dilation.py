#!/usr/bin/python3
"""The Katai / Bourgain-Sarnak-Ziegler orthogonality criterion applied to lambda along shifted primes.

Route card: notes/parity-attempts/2026-11-23-katai-bsz-dilation.md   (Session 46)
Run: /usr/bin/python3 -I code/parity/katai_dilation.py [X]     (default X = 1e8; ~30 s, ~4 GB)

Target (parity-sensitive, Chowla-along-primes type): sum_{n <= X} lambda(n) F(n) = o(X) with the NORMALISED weight
F(n) = Lambda(n - 2) (n - 2 prime; the mean of F is about 1). BSZ Theorem 2 (arXiv:1110.0992v1, read) needs |F| <= 1 and,
for all primes p1 != p2 <= e^{1/tau}, |sum_{m <= M} F(p1 m) conj F(p2 m)| <= tau M. Our F is unbounded (|F| <= log X),
so a mean-zero version F0 = F - G is used, G the W-tricked Cramer model G(n) = (W/phi(W)) 1[gcd(n - 2, W) = 1].

This script prints finite-X data only (it proves nothing):
 (a) the target ratio sum_{p <= X} lambda(p + 2) / pi(X)                         (should be small; it is the LWW-type sum)
 (b) for a few pairs p1 != p2: C_raw = (1/M) sum_m F(p1 m) F(p2 m), and the model value C_mod from G, and
     C_0 = (1/M) sum_m F0(p1 m) F0(p2 m). C_raw is of order 1 (a Hardy-Littlewood singular-series constant for the
     binary pair of forms (p1 m - 2, p2 m - 2)), so the BSZ hypothesis fails for F itself; for F0 it reduces to the
     Hardy-Littlewood asymptotic for that pair (C_raw - C_mod -> 0 up to O(1/w)).
 (c) the diagonal: D(p) = (1/M) sum_m F(p m)^2 grows like log X (sparseness); in the Cauchy-Schwarz step of the
     criterion this forces the prime range P to exceed log X.
"""
import sys, time, math
import numpy as np

t0 = time.time()
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
N = X + 3

# sieve: smallest prime factor parity -> Liouville via Omega counts
isp = np.ones(N, dtype=bool); isp[:2] = False
for i in range(2, int(N**0.5) + 1):
    if isp[i]:
        isp[i*i::i] = False
primes = np.nonzero(isp)[0]
# Omega(n) mod 2 by repeated division over prime powers
om = np.zeros(N, dtype=np.int8)
for p in primes[primes <= int(N**0.5)]:
    pk = int(p)
    while pk < N:
        om[pk::pk] ^= 1
        pk *= int(p)
# for n with a prime factor > sqrt(N): it is at most one such factor, add it
rem = np.arange(N, dtype=np.int64)
for p in primes[primes <= int(N**0.5)]:
    p = int(p)
    pk = p
    while pk < N:
        rem[pk::pk] //= p
        pk *= p
om ^= (rem > 1).astype(np.int8)
lam = (1 - 2 * om).astype(np.int8)          # lambda(n), lam[0] meaningless
del rem
# self-check of lambda against trial division for n < 2000 and a few large n
def lam_td(k):
    c, d = 0, 2
    while d * d <= k:
        while k % d == 0:
            k //= d; c += 1
        d += 1
    return (-1) ** (c + (k > 1))
assert all(lam_td(k) == lam[k] for k in range(1, 2000))
assert all(lam_td(k) == lam[k] for k in range(X - 500, X + 3))
print(f"[{time.time()-t0:6.1f} s] sieve done (lambda self-check passed), X = {X:.3g}")

# (a) target ratio
P = primes[primes <= X]
S = int(lam[P + 2].sum())
print(f"(a) sum_(p<=X) lambda(p+2) = {S},  pi(X) = {len(P)},  ratio = {S/len(P):+.5f}")

# F(n) = log(n-2) if n-2 prime, as float arrays
F = np.zeros(N, dtype=np.float64)
F[P + 2] = np.log(P.astype(np.float64))
w = 13
Wp = [2, 3, 5, 7, 11, 13]
W = 1
for q in Wp:
    W *= q
phiW = 1
for q in Wp:
    phiW *= q - 1
n = np.arange(N, dtype=np.int64)
coprime = np.ones(N, dtype=bool)
for q in Wp:
    coprime &= ((n - 2) % q) != 0
G = (W / phiW) * coprime.astype(np.float64)
del n, coprime
F0 = F - G
print(f"[{time.time()-t0:6.1f} s] mean F on [1,X] = {F[:X].mean():.5f}, mean G = {G[:X].mean():.5f} (w = {w})")

print("(b) pairs (p1, p2): M = X // max(p1,p2);  C_raw, C_mod, C_raw - C_mod, C_0")
for (p1, p2) in [(3, 5), (3, 7), (5, 7), (5, 11), (7, 11), (11, 13), (17, 19), (23, 29), (31, 37)]:
    M = X // max(p1, p2)
    m = np.arange(1, M + 1, dtype=np.int64)
    a, b = p1 * m, p2 * m
    Craw = float((F[a] * F[b]).sum()) / M
    Cmod = float((G[a] * G[b]).sum()) / M
    C0 = float((F0[a] * F0[b]).sum()) / M
    print(f"   ({p1:2d},{p2:2d}) M = {M:10d}: C_raw = {Craw:8.4f}  C_mod = {Cmod:8.4f}  diff = {Craw - Cmod:+8.4f}  C_0 = {C0:+8.4f}")

print("(c) diagonal D(p) = (1/M) sum_m F(p m)^2 against log X =", f"{math.log(X):.3f}")
for p in [3, 5, 7, 11, 13]:
    M = X // p
    m = np.arange(1, M + 1, dtype=np.int64)
    D = float((F[p * m] ** 2).sum()) / M
    print(f"   p = {p:2d}: D(p) = {D:8.4f}   D(p) / log X = {D / math.log(X):.4f}")
print(f"[{time.time()-t0:6.1f} s] done")
