#!/usr/bin/env python3
"""Exploration (Heuristic): local Gowers norms of Liouville on short intervals vs random models.

Tao (arXiv:1605.04628, Thm 1.8, Remark 3.4): log-averaged k-point Chowla <=> log-averaged local U^{k-1}
uniformity of lambda on [n, n+H], H -> infinity slowly; k = 3 needs local U^2 (open).  Question: at
moderate X, is the average local U^2 (and U^3) norm of lambda on intervals of length H distinguishable
from (a) i.i.d. signs and (b) a random completely multiplicative +-1 function (Rademacher signs at primes)?
Local norm as in Tao: ||f 1_I||_{U^d(Z)} / ||1_I||_{U^d(Z)}; U^2 exact in integers, U^3 exact in integers
(sum over h of ||Delta_h f||_{U^2}^4).  Usage: /usr/bin/python3 -I local_u2_liouville.py [X] [M] [seed]
(defaults 10**9, 2**18, 20261117).  Output saved as local_u2_liouville.out.  Runtime ~1-2 min, < 1 GB.
"""
import sys
import numpy as np

X = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
M = int(sys.argv[2]) if len(sys.argv) > 2 else 2 ** 18
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 20261117


def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def signs_segment(lo, hi, prime_sign):
    """f(n) for lo <= n < hi, f completely multiplicative with f(p) = prime_sign(p) (exact factorisation)."""
    n = np.arange(lo, hi, dtype=np.int64)
    rem = n.copy()
    val = np.ones(len(n), dtype=np.int64)
    for p in primes_upto(int(hi ** 0.5) + 1):
        p = int(p); sp = prime_sign(p); pk = p
        while pk < hi:
            idx = np.arange((-lo) % pk, len(n), pk)
            val[idx] *= sp
            rem[idx] //= p
            pk *= p
    big = rem > 1          # one remaining prime factor > sqrt(hi)
    if big.any():
        val[big] *= np.array([prime_sign(int(q)) for q in rem[big]], dtype=np.int64)
    return val


def u2pow4(h):
    a = np.correlate(h, h, mode="full")
    return int(np.dot(a, a))


def u3pow8(h):
    n = len(h); tot = 0
    for k in range(-(n - 1), n):
        d = h[: n - k] * h[k:] if k >= 0 else h[-k:] * h[: n + k]
        tot += u2pow4(d)
    return tot


def stats(f, H, d, nint):
    norm = u2pow4(np.ones(H, dtype=np.int64)) if d == 2 else u3pow8(np.ones(H, dtype=np.int64))
    vals = []
    for j in range(nint):
        seg = f[j * H:(j + 1) * H]
        v = u2pow4(seg) if d == 2 else u3pow8(seg)
        vals.append((v / norm) ** (1.0 / 2 ** d))
    vals = np.array(vals)
    return vals.mean(), vals.std(ddof=1) / len(vals) ** 0.5


def main():
    rng = np.random.default_rng(SEED)
    lam = signs_segment(X, X + M, lambda p: -1)
    rs = {}
    def rad(p):
        if p not in rs:
            rs[p] = int(rng.choice([-1, 1]))
        return rs[p]
    rmf = signs_segment(X, X + M, rad)
    iid = rng.choice(np.array([-1, 1], dtype=np.int64), size=M)
    print(f"X = {X}, M = {M}, seed = {SEED}; mean local norm over disjoint intervals of length H (+- stderr)")
    print(f"shift-2 correlation on the segment: lambda {np.mean(lam[:-2]*lam[2:]):+.5f}, "
          f"rand.mult. {np.mean(rmf[:-2]*rmf[2:]):+.5f}, iid {np.mean(iid[:-2]*iid[2:]):+.5f}")
    for d, Hs in ((2, (8, 16, 32, 64, 128, 256, 512)), (3, (8, 16, 32, 64))):
        print(f"U^{d}:")
        for H in Hs:
            nint = min(M // H, 4000 if d == 2 else max(200, 4000 // H))
            row = [stats(f, H, d, nint) for f in (lam, rmf, iid)]
            z = (row[0][0] - row[2][0]) / (row[0][1] ** 2 + row[2][1] ** 2) ** 0.5
            print(f"  H={H:4d} n={nint:5d}  lambda {row[0][0]:.4f}+-{row[0][1]:.4f}  "
                  f"rand.mult {row[1][0]:.4f}+-{row[1][1]:.4f}  iid {row[2][0]:.4f}+-{row[2][1]:.4f}  z(lam-iid)={z:+.2f}")


if __name__ == "__main__":
    main()
