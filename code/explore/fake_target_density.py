"""Exploration (Session 40): the 'fake target' 1_S of the LWW transference principle.

S = {h : a h - 2 is composite for every a in A}.  If the Lu-Wang-Wu Type II estimate held for a family A,
the count T(1_S) = 0 would force density(S) = O(L^{-A}) (route card 2026-11-21-lww-main-term.md, Finding 5).
Here: toy families A = {p q : P0 < p < q <= P, p q <= AMAX}, odd h in [H, 2H); compare the empirical density of S
with the Cramer-Granville model prod_a (1 - c_w(a h - 2)/log(a h)), c_w(n) = prod_{l<=w}(1-1/l)^{-1} 1[(n,P(w))=1].
Heuristic / exploratory only.  Usage: python3 -I fake_target_density.py [H] [AMAX]
"""
import sys, math
import numpy as np

H = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
AMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
NMAX = 2 * H * AMAX
sieve = np.ones(NMAX + 1, dtype=bool); sieve[:2] = False
for i in range(2, int(NMAX ** 0.5) + 1):
    if sieve[i]: sieve[i*i::i] = False
primes = np.nonzero(sieve)[0]
W = 7; smallp = [2, 3, 5, 7]; cw = 1.0
for l in smallp: cw /= (1 - 1 / l)
print(f"H={H} AMAX={AMAX} NMAX={NMAX}; model uses w={W}")
print(" P0    P    |A|  emp.dens(S)  model.dens(S)  mean #prime a h-2   model mean")
for (P0, P) in [(11, 30), (11, 50), (11, 80), (11, 150), (11, 300), (11, 900)]:
    ps = [int(p) for p in primes if P0 < p <= P]
    A = sorted({p * q for i, p in enumerate(ps) for q in ps[i+1:] if p * q <= AMAX})
    hs = np.arange(H + 1 - H % 2, 2 * H, 2)  # odd h only (even h: a h - 2 even, a local obstruction Type I also sees)
    emp_S = 0; mod_S = 0.0; cnt = 0; mcnt = 0.0
    for h in hs:
        vals = np.array(A, dtype=np.int64) * h - 2
        isp = sieve[vals]
        k = int(isp.sum()); cnt += k; emp_S += (k == 0)
        logp = 1.0
        for a, v in zip(A, vals):
            pr = 0.0 if any(v % l == 0 for l in smallp) else cw / math.log(v)
            logp *= (1 - pr); mcnt += pr
        mod_S += logp
    n = len(hs)
    print(f"{P0:3d} {P:4d} {len(A):6d}  {emp_S/n:11.5f}  {mod_S/n:13.5f}  {cnt/n:17.2f}  {mcnt/n:10.2f}")
