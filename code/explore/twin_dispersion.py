#!/usr/bin/python3
"""Exploration (Session 45): dispersion of twin primes in residue classes to large moduli (Barban-Davenport-Halberstam /
Montgomery-Hooley type), against the same statistic for primes.

Run: /usr/bin/python3 -I code/explore/twin_dispersion.py [X]   (default 1e8; ~1 min, ~1 GB). Heuristic / exploratory.

For a prime modulus q, the twins p, p + 2 <= X with q not dividing p(p + 2) fall into the q - 2 admissible classes
a mod q; under uniformity each class expects E = N2 / (q - 2). The dispersion ratio
    D2(q) = sum_a (N_a - E)^2 / (E (q - 3))           (q - 3 degrees of freedom)
is 1 for a Poisson (independent-placement) model. For primes the same statistic with the q - 1 classes is
    D1(q) = sum_a (N_a - E)^2 / (E (q - 2)).
Montgomery-Hooley (Lambda-weighted: sum_a (psi(X;q,a) - X/phi(q))^2 ~ X log q, against X log X for independent
placement) suggests that for primes D1(q) is roughly l = log q / log X, minus lower-order terms (an earlier draft of
this docstring said 1 - l; the data showed that was backwards). The question: does D2(q) follow the same curve, a
different one, or something with structure? Comparison curves printed: l and 1 - (1 - l)^2 (a guess:
"either of two independent conditions" in a crude model; NOT derived).
We print D1, D2 averaged over the primes q in dyadic-like ranges [Q, 1.1 Q].
"""
import sys, time, math
import numpy as np

t0 = time.time()
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
sv = np.ones(X + 3, dtype=bool)
sv[:2] = False
sv[4::2] = False
for p in range(3, int((X + 2) ** 0.5) + 1, 2):
    if sv[p]:
        sv[p * p::2 * p] = False
P = np.nonzero(sv[:X + 1])[0]
P = P[P >= 5]
T = P[sv[P + 2]]                     # p with p + 2 prime, p >= 5
T = T[T + 2 <= X]
print(f"X = {X:.0e}: primes >= 5: {len(P)}, twin pairs (p >= 5, p + 2 <= X): {len(T)}  [{time.time()-t0:.1f}s]")
qs_all = np.nonzero(sv[:200000])[0]
LX = math.log(X)
print(" Q        #q   mean D1(q)  mean D2(q)   l=logq/logX  1-(1-l)^2")
for Q in (100, 300, 1000, 3000, 10000, 30000, 100000):
    qs = qs_all[(qs_all >= Q) & (qs_all <= 1.1 * Q)][:40]
    d1s, d2s = [], []
    for q in qs.tolist():
        c1 = np.bincount(P % q, minlength=q).astype(float)
        c1 = np.delete(c1, 0)
        E1 = c1.sum() / (q - 1)
        d1s.append(((c1 - E1) ** 2).sum() / (E1 * (q - 2)))
        r = T % q
        c2 = np.bincount(r, minlength=q).astype(float)
        keep = np.ones(q, dtype=bool)
        keep[0] = False
        keep[(q - 2) % q] = False
        c2 = c2[keep]
        E2 = c2.sum() / (q - 2)
        d2s.append(((c2 - E2) ** 2).sum() / (E2 * (q - 3)))
    lq = math.log(Q * 1.05) / LX
    print(f" {Q:<8d} {len(qs):<4d} {np.mean(d1s):10.4f}  {np.mean(d2s):10.4f}  {lq:11.4f}  {1-(1-lq)**2:11.4f}")
print(f"[{time.time()-t0:.1f}s]")
