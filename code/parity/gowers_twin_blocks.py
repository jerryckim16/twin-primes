#!/usr/bin/env python3
"""Gowers norms do not see the shift-2 correlation (illustration of Prop. prop:gowers-blind).

Random block functions f(n) = eps[(n // L, n % 2)] on [1, N] (independent Rademacher signs per label)
have small local Gowers norms (Tao's normalisation ||f||_{U^d(I)} = ||f 1_I||_{U^d(Z)} / ||1_I||_{U^d(Z)})
but shift-2 correlation >= 1 - 4/L - 6/N.  The 'anti' version multiplies by (-1)^(n//2), giving
correlation <= -1 + 4/L + 6/N, and g = 1 + f_anti is a {0,2}-valued 'fake prime' function with
||g - 1||_{U^d} = ||f_anti||_{U^d} small and almost no pairs g(n) g(n+2) != 0.

U^2 is computed EXACTLY in integers (||h||_{U^2(Z)}^4 = sum_k a(k)^2, a = autocorrelation of h).
U^3 is computed in floating point (FFT), illustration only.  Liouville lambda and i.i.d. signs are shown
for comparison.  Usage: /usr/bin/python3 -I gowers_twin_blocks.py [N] [L] [seed]   (defaults 32768 64 20261117)
Output: printed table (saved as gowers_twin_blocks.out).  Runtime: well under a minute.
"""
import sys
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 32768
L = int(sys.argv[2]) if len(sys.argv) > 2 else 64
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 20261117
N3 = 4096   # length for the floating-point U^3 values


def u2_pow4_exact(h):
    """sum_{x,h1,h2} h(x)h(x+h1)h(x+h2)h(x+h1+h2) over Z, h supported on the given window (integers)."""
    h = np.asarray(h, dtype=np.int64)
    a = np.correlate(h, h, mode="full")          # exact int64 autocorrelation
    return int(sum(int(v) * int(v) for v in a))  # Python ints: no overflow


def u2_local(h):
    one = np.ones(len(h), dtype=np.int64)
    return (u2_pow4_exact(h) / u2_pow4_exact(one)) ** 0.25


def u3_pow8_float(h):
    """sum over x,h1,h2,h3 in Z of the 8-fold product (floating point): sum_k ||h * h(.+k)||_{U^2}^4."""
    h = np.asarray(h, dtype=float)
    n = len(h)
    M = 1 << (int(4 * n - 1).bit_length())
    tot = 0.0
    for k in range(-(n - 1), n):
        if k >= 0:
            d = h[: n - k] * h[k:]
        else:
            d = h[-k:] * h[: n + k]
        F = np.fft.rfft(d, M)
        a = np.fft.irfft(np.abs(F) ** 2, M)
        tot += float(np.sum(a * a))
    return tot


def u3_local(h):
    return (u3_pow8_float(h) / u3_pow8_float(np.ones(len(h)))) ** 0.125


def shift2(h):
    h = np.asarray(h, dtype=np.int64)
    return float(np.sum(h[:-2] * h[2:])) / len(h)


def blocks(n_len, L, rng, anti=False):
    n = np.arange(1, n_len + 1)
    lab = 2 * (n // L) + (n % 2)
    eps = rng.choice(np.array([-1, 1], dtype=np.int64), size=int(lab.max()) + 1)
    f = eps[lab]
    if anti:
        f = f * np.where((n // 2) % 2 == 0, 1, -1)
    return f


def liouville(lo, hi):
    """lambda(n) for lo <= n < hi by a segmented factor count (exact)."""
    n = np.arange(lo, hi, dtype=np.int64)
    rem = n.copy()
    om = np.zeros(len(n), dtype=np.int64)
    p_lim = int(hi ** 0.5) + 1
    sieve = np.ones(p_lim + 1, dtype=bool); sieve[:2] = False
    for i in range(2, int(p_lim ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    for p in np.nonzero(sieve)[0]:
        p = int(p); pk = p
        while pk < hi:
            start = (-lo) % pk
            idx = np.arange(start, len(n), pk)
            om[idx] += 1
            rem[idx] //= p
            pk *= p
    om += (rem > 1)
    return np.where(om % 2 == 0, 1, -1).astype(np.int64)


def main():
    rng = np.random.default_rng(SEED)
    d = 2
    bound2 = 2 ** (2 * d + 1) * (4 * d) ** d * L / N   # E ||f||^{2^d}_{U^d[N]} <= this (proof of the Prop.)
    print(f"N = {N}, L = {L}, seed = {SEED}; U^2 exact (int), U^3 float at N3 = {N3}")
    print(f"Prop. bound on E||f||_{{U^2}}^4: {bound2:.4g}  (so typical ||f||_U2 <~ {bound2 ** 0.25:.3f}; crude)")
    print(f"shift-2 correlation guaranteed >= 1 - 4/L - 6/N = {1 - 4 / L - 6 / N:.5f}")
    X = 10 ** 7
    rows = [
        ("block f", blocks(N, L, rng), blocks(N3, L // 4 if L >= 8 else L, rng)),
        ("block f (anti)", blocks(N, L, rng, anti=True), blocks(N3, L // 4 if L >= 8 else L, rng, anti=True)),
        ("iid signs", rng.choice(np.array([-1, 1], dtype=np.int64), size=N),
         rng.choice(np.array([-1, 1], dtype=np.int64), size=N3)),
        (f"lambda on [1e7, 1e7+N)", liouville(X, X + N), liouville(X, X + N3)),
    ]
    print(f"{'function':28s} {'U2[N]':>8s} {'shift2':>9s} {'U3[N3]':>8s} {'shift2[N3]':>10s}")
    for name, f, f3 in rows:
        print(f"{name:28s} {u2_local(f):8.4f} {shift2(f):9.5f} {u3_local(f3):8.4f} {shift2(f3):10.5f}")
    fa = rows[1][1]
    g = 1 + fa
    print(f"fake primes g = 1 + f_anti in {{0,2}}: mean {g.mean():.4f}, ||g-1||_U2 = {u2_local(fa):.4f}, "
          f"(1/N) sum g(n) g(n+2) = {float(np.sum(g[:-2] * g[2:])) / N:.5f} (a random set of density 1/2 gives ~1)")
    print("(N3 rows use block length L/4 so that N3/L is comparable.)")


if __name__ == "__main__":
    main()
