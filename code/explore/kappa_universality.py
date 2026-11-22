#!/usr/bin/python3
"""Exploration (Session 44): does the Liouville bias on the dimension-ladder targets depend on kappa alone?

notes/explorations.md, entry of 2026-11-22 (Session 44).
Run: /usr/bin/python3 -I code/explore/kappa_universality.py [X]   (default X = 1e8; ~3 min, ~1.6 GB)

For a prime q and a subgroup H < (Z/q)^* of index m, T_H(X) = #{3 <= p <= X : p + 2 mod q in H, every prime factor
of p + 2 has residue in H} (route cards of 22 Nov, sieve dimension kappa = 1 - 1/m). Question: is the share of
lambda(p + 2) = +1 on T_H a function of kappa only (at fixed X), or does it depend on (q, H)?
The Selberg-Delange heuristic of the Session 43 card predicts a mean of lambda about -c_{q,H} (log X)^{-2/m} with a
constant that depends on (q, H) through Euler products and L-values, so exact kappa-universality is NOT expected;
the test is whether the (q, H)-dependence is small compared with the kappa-dependence.
Prints #T_H, the + share, the mean of lambda and its (log X)^{2/m}-rescaling, and the normalised
count #T_H / (|A_H| V_H(z)). Heuristic / exploratory; finite X only.
"""
import sys, time, math
import numpy as np

t0 = time.time()
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
N = X + 3


def subgroup(q, m):
    # the index-m subgroup of the cyclic group (Z/q)^*: the m-th powers
    return sorted({pow(a, m, q) for a in range(1, q)})


CASES = [(3, 2), (5, 2), (7, 2), (13, 2), (7, 3), (13, 3), (19, 3), (31, 3), (5, 4), (13, 4), (17, 4), (29, 4)]
Hs = {(q, m): set(subgroup(q, m)) for q, m in CASES}
for (q, m), H in Hs.items():
    assert len(H) * m == q - 1

isp = np.ones(N, dtype=bool)
isp[:2] = False
lim = int(math.isqrt(N)) + 1
for p in range(2, lim):
    if isp[p]:
        isp[p * p::p] = False
rem = np.arange(N, dtype=np.int32)
Om = np.zeros(N, dtype=np.int8)
good = {c: np.ones(N, dtype=bool) for c in CASES}
for p in np.nonzero(isp[:lim])[0]:
    p = int(p)
    for c in CASES:
        if p % c[0] not in Hs[c]:
            good[c][p::p] = False
    pk = p
    while pk < N:
        sl = slice(pk, N, pk)
        rem[sl] //= p
        Om[sl] += 1
        pk *= p
big = rem > 1
Om[big] += 1
for c in CASES:
    q = c[0]
    rr = rem % q
    good[c] &= ~big | np.isin(rr, list(Hs[c]))
del rem
lam = np.where(Om % 2 == 0, 1, -1).astype(np.int8)
del Om
print(f"X = {X:.0e}; tables built [{time.time()-t0:.1f}s]")
ps = np.nonzero(isp[:X + 1])[0]
ps = ps[ps >= 3]
m2 = ps + 2
z = math.sqrt(X + 2)
LX = math.log(X)
print(" q  m  kappa   |H|  |A_H|       #T_H     + share   mean lam   mean*(logX)^(2/m)  #T/(|A|V)")
for c in CASES:
    q, m = c
    H = Hs[c]
    inH = np.isin(m2 % q, list(H))
    A = int(inH.sum())
    T = inH & good[c][m2]
    nT = int(T.sum())
    plus = int((lam[m2[T]] == 1).sum())
    mean = (2 * plus - nT) / nT
    V = 1.0
    for l in range(3, int(z) + 1):
        if isp[l] and l != q and (l % q) not in H:
            V *= 1 - 1 / (l - 1)
    print(f"{q:2d} {m:2d}  {1-1/m:.4f} {len(H):4d} {A:9d} {nT:9d}   {plus/nT:.4f}   {mean:+.4f}   {mean*LX**(2/m):+8.4f}"
          f"          {nT/(A*V):.4f}")
print(f"[{time.time()-t0:.1f}s]")
