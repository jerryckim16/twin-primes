#!/usr/bin/python3
"""Exploration (Session 47): Fourier uniformity of lambda(p+2) along the primes.

notes/explorations.md, 2026-11-23. Heuristic / exploratory only.
Run: /usr/bin/python3 -I code/explore/shifted_prime_fourier.py [X] [log2M]
     (default X = 1e8, M = 2^27; ~2 min, ~5 GB)

Question: the claimed theorem of Lu-Wang-Wu (arXiv:2610.20242, Claimed) is sum_{p<=x} mu(p+2) = o(pi(x)), the
zero-frequency case. Is the exponential sum S(alpha) = sum_{p<=X} lambda(p+2) e(alpha p) uniformly small in
alpha, i.e. does lambda(p+2) look Fourier-uniform along the primes, or are there spikes (at rationals a/q,
which would be biases of lambda(p+2) in classes p mod q, or elsewhere)? Sup-norm smallness with a o(pi(X))
bound is the natural "Fourier-uniform" strengthening (the U^2 case of a Gowers-uniformity statement along
primes, cf. Green-Tao's treatment of mu in Annals 2012 for the unshifted integers).

We evaluate S on the grid alpha = j/M by one real FFT, normalise by sqrt(pi(X)) (the random-sign scale), and
compare with two controls on the same support: (R) i.i.d. random signs at the primes, (L) lambda(p+2) with the
primes' signs permuted (same multiset of values). For the target 1_P itself (unsigned) the spikes at a/q are of
size pi(X) mu(q)/phi(q): these are the major arcs that a parity-type sign has to remove.
"""
import sys, time, math
from fractions import Fraction
import numpy as np

t0 = time.time()
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
LM = int(sys.argv[2]) if len(sys.argv) > 2 else 27
M = 1 << LM
assert M > X
N = X + 3
spf = np.zeros(N, dtype=np.int32)
for p in range(2, math.isqrt(N) + 1):
    if spf[p] == 0:
        blk = spf[p * p::p]
        blk[blk == 0] = p
isp = spf == 0
isp[:2] = False
spf[isp] = np.nonzero(isp)[0].astype(np.int32)
Om = np.zeros(N, dtype=np.int8)
lo = 2
while lo < N:
    hi = min(N, 2 * lo)
    r = np.arange(lo, hi)
    Om[lo:hi] = Om[r // spf[lo:hi]] + 1
    lo = hi
del spf
lam = (1 - 2 * (Om & 1)).astype(np.int8)
del Om
P = np.nonzero(isp)[0]
del isp
P = P[(P >= 3) & (P <= X)]
sgn = lam[P + 2].astype(np.float64)
del lam
n = len(P)
print(f"X = {X:.3g}, M = 2^{LM}: {n} odd primes; sum lambda(p+2)/pi = {sgn.mean():+.6f} "
      f"(= {sgn.sum()/math.sqrt(n):+.2f} sqrt(pi))  [{time.time()-t0:.1f}s]", flush=True)

rng = np.random.default_rng(20261123)


def spectrum(w):
    a = np.zeros(M, dtype=np.float64)
    a[P] = w
    F = np.abs(np.fft.rfft(a)) / math.sqrt(n)     # |S(j/M)| / sqrt(pi), j = 0..M/2
    return F


def nearest_rational(j, qmax=60):
    x = Fraction(j, M)
    best = None
    for q in range(1, qmax + 1):
        a = round(x * q)
        d = abs(x - Fraction(a, q))
        if best is None or d < best[0]:
            best = (d, Fraction(a, q))
    return best[1], float(best[0]) * M   # rational, distance in grid steps


def report(name, w, top=8):
    F = spectrum(w)
    F[0] = F[0]   # keep alpha = 0
    order = np.argpartition(-F, top)[:top]
    order = order[np.argsort(-F[order])]
    mx = F.max(); med = np.median(F); q99 = np.quantile(F, 0.999999)
    print(f"[{name}] max |S|/sqrt(pi) = {mx:.2f} at j = {int(F.argmax())}; median {med:.3f}; "
          f"0.999999-quantile {q99:.2f}  [{time.time()-t0:.1f}s]", flush=True)
    for j in order:
        r, d = nearest_rational(int(j))
        print(f"    j = {int(j):>10d}  alpha = {j/M:.8f}  |S|/sqrt(pi) = {F[j]:8.2f}  nearest a/q (q<=60): {r} "
              f"at {d:.1f} grid steps")
    # rationals with small q: |S(a/q)| / sqrt(pi) at the nearest grid point (resolution 1/M)
    vals = []
    for q in range(1, 31):
        for a in range(0, q // 2 + 1):
            if math.gcd(a, q) == 1:
                vals.append((q, a, F[round(a * M / q)]))
    worst = sorted(vals, key=lambda t: -t[2])[:5]
    print("    largest at a/q, q <= 30: " + ", ".join(f"{a}/{q}: {v:.2f}" for q, a, v in worst), flush=True)
    del F
    return mx


# random model: expected max of |S|/sqrt(pi) over M/2 nearly independent frequencies ~ sqrt(log(M/2))
print(f"random-model scale sqrt(log(M/2)) = {math.sqrt(math.log(M/2)):.2f}")
m_t = report("target lambda(p+2)", sgn)
m_r = report("control R: iid signs at primes", rng.choice([-1.0, 1.0], size=n))
perm = sgn.copy(); rng.shuffle(perm)
m_l = report("control L: lambda(p+2) permuted", perm)
F1 = spectrum(np.ones(n))
print(f"[unsigned 1_P] |S(1/2)|/sqrt(pi) = {F1[M//2]:.1f}, |S(1/3)|/sqrt(pi) = {F1[round(M/3)]:.1f} "
      f"(major arcs; sqrt(pi) = {math.sqrt(n):.0f})")
print(f"SUMMARY: max normalised |S|: target {m_t:.2f}, iid {m_r:.2f}, permuted {m_l:.2f}  [{time.time()-t0:.1f}s]")
