#!/usr/bin/env python3
"""Heuristic illustration for the parity paper, Remark rem:mrt17 (Session 29).

Usage: /usr/bin/python3 -I code/parity/mrt_averaged_hl.py [X] [H]   (defaults 1e8, 2000; ~2 min, < 1 GB)

What it does (all counts exact integers; only the normalisation is floating point):
 1. Sieves primes up to 2X + H.
 2. For every even 2 <= h <= H: c(h) = #{X < p <= 2X : p, p + h both prime} (exact count), and the
    Hardy-Littlewood prediction S(h) * L(h), L(h) = int_X^{2X} dt / (log t * log(t + h)) (Simpson's rule),
    S(h) = 2 Pi_2 prod_{p | h, p > 2} (p - 1)/(p - 2).  Prints r(h) = c(h) / (S(h) L(h)),
    the value at h = 2, the mean / standard deviation over h, the Poisson (Cramer-type) prediction
    for the standard deviation, and the fraction of shifts with |r(h) - 1| > delta.
 3. Checks the exact identity (Proved here, elementary)
        sum_x (N(x + K) - N(x))^2 = sum_{|h| < K} (K - |h|) * #{n : n, n + h in A}
    for A = the primes in a window, with N the counting function and x over all integers
    (finite support), for K = 2, 3, 7 and a window of length 10^6: the K-window second moment of the
    primes is a Fejer-weighted average of the pair counts; c(2) is its second difference in K.
 4. Exploration (Session 29): least-squares fit of r(h) - 1 on the indicators [p | h] for
    p = 3, 5, 7, 11, 13 and on log h, to look for structure that S(h) does not explain.
"""
import sys, math
import numpy as np

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
H = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
N = 2 * X + H + 1

sieve = np.ones(N + 1, dtype=bool)
sieve[:2] = False
for p in range(2, int(N ** 0.5) + 1):
    if sieve[p]:
        sieve[p * p::p] = False

# twin prime constant Pi_2 = prod_{p > 2} (1 - 1/(p-1)^2), truncated at 10^7 (tail < 1e-7 relative)
pr = np.nonzero(sieve[:10**7])[0]
pr = pr[pr > 2].astype(np.float64)
Pi2 = float(np.exp(np.sum(np.log1p(-1.0 / (pr - 1.0) ** 2))))

def S(h):
    if h % 2:
        return 0.0
    s, m, p = 2 * Pi2, h, 3
    while m % 2 == 0:
        m //= 2
    while p * p <= m:
        if m % p == 0:
            s *= (p - 1) / (p - 2)
            while m % p == 0:
                m //= p
        p += 2
    if m > 1:
        s *= (m - 1) / (m - 2)
    return s

def L(h, steps=2000):
    a, b = float(X), float(2 * X)
    t = np.linspace(a, b, steps + 1)
    f = 1.0 / (np.log(t) * np.log(t + h))
    w = np.ones(steps + 1); w[1:-1:2] = 4; w[2:-1:2] = 2
    return float(np.sum(w * f) * (b - a) / (3 * steps))

A = sieve[X + 1: 2 * X + 1]        # primes in (X, 2X]
hs = list(range(2, H + 1, 2))
r = []
c2 = None
for h in hs:
    B = sieve[X + 1 + h: 2 * X + 1 + h]
    c = int(np.count_nonzero(A & B))
    if h == 2:
        c2 = c
    r.append(c / (S(h) * L(h)))
r = np.array(r)
print(f"X = {X}, H = {H}, Pi_2 = {Pi2:.9f}")
print(f"h = 2: c(2) = {c2}, prediction S(2)L(2) = {S(2)*L(2):.1f}, r(2) = {r[0]:.6f}")
print(f"even h <= H ({len(hs)} shifts): mean r = {r.mean():.6f}, sd r = {r.std():.6f}, min {r.min():.6f}, max {r.max():.6f}")
pois = np.array([1 / math.sqrt(S(h) * L(h)) for h in hs])
print(f"Poisson prediction for sd (mean of 1/sqrt(S(h)L(h))): {pois.mean():.6f}")
z = (r - 1) / pois
print(f"normalised (r-1)/poisson: mean {z.mean():.3f}, sd {z.std():.3f}")
for d in (0.005, 0.01, 0.02, 0.05):
    print(f"fraction of shifts with |r(h)-1| > {d}: {np.mean(np.abs(r-1) > d):.4f}")

# 3. exact identity check on a window
W0, W = X + 1, 10**6
a = sieve[W0:W0 + W].astype(np.int64)
for K in (2, 3, 7):
    # N(x+K) - N(x) over all integer x with nonzero contribution = convolution of a with K ones
    win = np.convolve(a, np.ones(K, dtype=np.int64))
    lhs = int(np.sum(win * win))
    rhs = 0
    for h in range(-(K - 1), K):
        hh = abs(h)
        cnt = int(np.sum(a[:W - hh] * a[hh:])) if hh else int(a.sum())
        rhs += (K - hh) * cnt
    print(f"identity K = {K}: lhs = {lhs}, rhs = {rhs}, equal = {lhs == rhs}")
# second difference: V(3) - 2 V(2) + V(1) = 2 c(2)  (c(1) term: V(2)-2V(1)+V(0) = 2c(1))
V = {}
for K in (1, 2, 3):
    win = np.convolve(a, np.ones(K, dtype=np.int64)); V[K] = int(np.sum(win * win))
c2w = int(np.sum(a[:W - 2] * a[2:]))
print(f"second difference V(3) - 2V(2) + V(1) = {V[3]-2*V[2]+V[1]}, 2*c(2) on the window = {2*c2w}")

# 4. exploration: regression of r(h) - 1 on [p | h] and log h
cols = [np.ones(len(hs))] + [np.array([1.0 if h % p == 0 else 0.0 for h in hs]) for p in (3, 5, 7, 11, 13)]
cols.append(np.log(np.array(hs, dtype=float)))
M = np.vstack(cols).T
coef, res, rk, sv = np.linalg.lstsq(M, r - 1, rcond=None)
names = ["const", "3|h", "5|h", "7|h", "11|h", "13|h", "log h"]
pred = M @ coef
resid = (r - 1) - pred
# standard errors
sigma2 = float(np.sum(resid ** 2) / (len(hs) - M.shape[1]))
cov = sigma2 * np.linalg.inv(M.T @ M)
for n_, c_, s_ in zip(names, coef, np.sqrt(np.diag(cov))):
    print(f"  fit {n_:6s}: {c_:+.6f}  (se {s_:.6f}, t = {c_/s_:+.2f})")
print(f"R^2 = {1 - np.sum(resid**2)/np.sum((r-1-(r-1).mean())**2):.4f}")
