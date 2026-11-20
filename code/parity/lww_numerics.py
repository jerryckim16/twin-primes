#!/usr/bin/env python3
"""Numerical sanity check (NOT a verification) of the claims of Lu-Wang-Wu, arXiv:2610.20242v2:
Theorem 1: sum_{p<=x} mu(p+2) = o(pi(x)); Theorem 2: #{p<=x : mu(p+2) = k} ~ (1/2) prod_{p>2}(1 - 1/(p(p-1))) pi(x).
Also the Liouville analogue (their Remark 1, not proved there): sum_{p<=x} lambda(p+2).
Segmented sieve with numpy. Usage: /usr/bin/python3 -I lww_numerics.py [X]  (X = 1e9: a few minutes, < 1 GB)
"""
import sys, math
import numpy as np

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
R = math.isqrt(X + 2) + 1
small = np.ones(R + 1, bool); small[:2] = False
for i in range(2, math.isqrt(R) + 1):
    if small[i]:
        small[i * i::i] = False
P = np.nonzero(small)[0]
SEG = 10**7
checkpoints = sorted({10**e for e in range(4, 13) if 10**e <= X} | {X})
pi = 0; smu = 0; slam = 0; npos = 0; nneg = 0
out = []
lo = 2
while lo <= X:
    hi = min(lo + SEG, X + 1)               # primes p in [lo, hi); need values at p + 2 in [lo+2, hi+2)
    L, H = lo, hi + 2                       # work on n in [L, H)
    n = np.arange(L, H, dtype=np.int64)
    rem = n.copy()
    mu = np.ones(H - L, np.int8)
    om = np.zeros(H - L, np.int8)           # parity of Omega from small primes
    isp = np.ones(H - L, bool)
    for p in P:
        p = int(p)
        s = (-L) % p
        if s >= H - L:
            continue
        idx = slice(s, None, p)
        mu[idx] = -mu[idx]
        isp[idx] = False
        # divide out p fully from rem, tracking Omega parity
        pk = p
        while pk < H:
            s2 = (-L) % pk
            if s2 < H - L:
                sl = slice(s2, None, pk)
                rem[sl] //= p
                om[sl] ^= 1
                if pk > p:
                    mu[sl] = 0
            if pk > H // p:
                break
            pk *= p
    big = rem > 1                           # one remaining prime factor > sqrt(H)
    mu = np.where(big, -mu, mu)
    om = om ^ big.astype(np.int8)
    lam = 1 - 2 * om.astype(np.int64)
    # primes in [lo, hi): n <= R are prime iff in P; else isp
    m = hi - lo
    prim = isp[:m].copy()
    small_mask = n[:m] <= R
    if small_mask.any():
        prim[small_mask] = small[n[:m][small_mask]]
    mu2 = mu[2:2 + m].astype(np.int64); la2 = lam[2:2 + m]
    # accumulate with checkpoint resolution
    pidx = np.nonzero(prim)[0]
    vals_n = n[:m][pidx]
    cmu = np.cumsum(mu2[pidx]); cla = np.cumsum(la2[pidx]); cpos = np.cumsum(mu2[pidx] == 1); cneg = np.cumsum(mu2[pidx] == -1)
    for c in checkpoints:
        if lo <= c < hi:
            j = np.searchsorted(vals_n, c, side="right")
            if j > 0:
                out.append((c, pi + j, smu + int(cmu[j - 1]), slam + int(cla[j - 1]), npos + int(cpos[j - 1]), nneg + int(cneg[j - 1])))
            else:
                out.append((c, pi, smu, slam, npos, nneg))
    if len(pidx):
        pi += len(pidx); smu += int(cmu[-1]); slam += int(cla[-1]); npos += int(cpos[-1]); nneg += int(cneg[-1])
    lo = hi
const = 1.0
for p in P[1:]:
    const *= 1 - 1 / (int(p) * (int(p) - 1))
# tail of the product beyond sqrt(X): prod_{p > R}(1 - 1/p^2 approx) ~ exp(-1/(R log R)), negligible
print(f"prod_{{2<p<={R}}}(1 - 1/(p(p-1))) = {const:.8f}")
print("x, pi(x), sum mu(p+2)/pi, sum lambda(p+2)/pi, #mu=+1 / (c/2 pi), #mu=-1 / (c/2 pi)")
for c, pc, sm, sl, a, b in out:
    print(f"{c:>12d} {pc:>11d} {sm / pc:+.6f} {sl / pc:+.6f} {a / (const / 2 * pc):.6f} {b / (const / 2 * pc):.6f}")
