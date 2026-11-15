#!/usr/bin/env python3
"""Exploration (Heuristic), Session 17: what does a Selberg/GPY sieve weight 'see' of the parity of n(n+2)?
For odd n <= X, w(n) = (sum_{d | n(n+2), d <= R, d odd squarefree} mu(d) P(log(R/d)/log R))^2, P(t) = t^2,
R = X^theta.  Prints A = sum w, B = sum w lambda(n) lambda(n+2), T = sum_{n, n+2 prime} w, and the split of the
weighted mass by the parity pattern (lambda(n), lambda(n+2)) and by residue classes mod small q (a Type I
quantity: the two parity-twisted measures w(1 +- lambda(n)lambda(n+2))/2 have to be compared on it).
usage: parity_weighted_liouville.py X theta"""
import sys, numpy as np, math
X = int(float(sys.argv[1])); theta = float(sys.argv[2]); R = X ** theta
M = X + 3
isp = np.ones(M + 1, bool); isp[:2] = False
for p in range(2, int(M ** 0.5) + 1):
    if isp[p]: isp[p * p::p] = False
primes = np.nonzero(isp)[0]
Om = np.zeros(M + 1, dtype=np.int16)
for p in primes:
    pk = int(p)
    while pk <= M:
        Om[pk::pk] += 1; pk *= int(p)
lam = np.where(Om % 2 == 0, 1, -1).astype(np.int8)
isprime = isp
# odd n in [3, X]
n = np.arange(3, X + 1, 2); S = np.zeros(n.size)
def sqfree_odd(Rm):
    out = []
    for d in range(1, Rm + 1, 2):
        f = [int(p) for p in primes[primes <= d] if d % p == 0]
        if all(d % (p * p) for p in f): out.append((d, (-1) ** len(f), f))
    return out
Rm = int(R)
for d, m, ps in sqfree_odd(Rm):
    wt = m * (math.log(R / d) / math.log(R)) ** 2
    # residues r mod d with r(r+2) = 0 mod d
    rs = [0]; mod = 1
    for p in ps:
        new = []
        for r in rs:
            for c in (0, p - 2):
                # CRT combine r mod mod, c mod p
                t = ((c - r) * pow(mod, -1, p)) % p
                new.append(r + mod * t)
        rs = new; mod *= p
    for r in rs:
        # odd n = 3 + 2i, n = r mod d -> i = (r - 3) * inv2 mod d
        i0 = ((r - 3) * pow(2, -1, d)) % d if d > 1 else 0
        S[i0::d] += wt
w = S ** 2
ln = lam[n].astype(np.int64); ln2 = lam[n + 2].astype(np.int64)
A = w.sum(); B = (w * ln * ln2).sum(); tw = isprime[n] & isprime[n + 2]; T = w[tw].sum()
print(f"X={X:.3g} theta={theta} R={R:.1f}  A={A:.6g}  B/A={B/A:.6f}  T/A={T/A:.6f}  (#twins {tw.sum()})")
for a in (1, -1):
    for b in (1, -1):
        sel = (ln == a) & (ln2 == b)
        print(f"  pattern lam(n)={a:+d}, lam(n+2)={b:+d}: weight share {w[sel].sum()/A:.5f}, count share {sel.mean():.5f}")
plus = w * (1 + ln * ln2) / 2; minus = w * (1 - ln * ln2) / 2
for q in (3, 5, 7):
    sp_ = [plus[(n % q) == c].sum() / plus.sum() for c in range(q)]
    sm_ = [minus[(n % q) == c].sum() / minus.sum() for c in range(q)]
    print(f"  mod {q}: w(1+ll)/2 class shares {np.round(sp_,4)}; w(1-ll)/2 {np.round(sm_,4)}")
