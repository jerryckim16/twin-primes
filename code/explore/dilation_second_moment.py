#!/usr/bin/python3
"""Exploration (Session 46): the dilation second moment behind the Kati-BSZ route card
(notes/parity-attempts/2026-11-23-katai-bsz-dilation.md, Finding 5).

Run: /usr/bin/python3 -I code/explore/dilation_second_moment.py [X]   (default 1e8; ~2-3 min, ~3 GB)

F(n) = log(n - 2) if n - 2 is prime; G_w(n) = prod_{l <= w} (l/(l-1)) 1[l does not divide n - 2]; F0 = F - G_w.
For the primes Q = {3, ..., 61} and every pair p1 < p2 in Q: C0(p1, p2) = (1/M) sum_{m <= M} F0(p1 m) F0(p2 m),
M = X // p2. Question: is the pair-averaged off-diagonal (the quantity the growing-range KBSZ step needs to be small)
consistent with 0 as w grows (Hardy-Littlewood + w-truncation), or is there an unexpected bias?
Prediction for the truncation bias: C_raw / C_mod -> prod_{l > w, l not | p1 p2 (p1 - p2)} (1 - 1/(l-1)^2) (up to
finite-X effects), i.e. a relative bias of about -sum_{l > w} 1/l^2. Finite-X data only; proves nothing.
"""
import sys, time, math
import numpy as np
t0 = time.time()
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
N = X + 3
isp = np.ones(N, dtype=bool); isp[:2] = False
for i in range(2, int(N**0.5) + 1):
    if isp[i]:
        isp[i*i::i] = False
P = np.nonzero(isp)[0]
F = np.zeros(N, dtype=np.float64)
F[P + 2] = np.log(P.astype(np.float64))
del isp
Q = [int(q) for q in P[(P >= 3) & (P <= 61)]]
smallp = [int(l) for l in P[P <= 61]]
print(f"[{time.time()-t0:5.1f} s] X = {X:.3g}; |Q| = {len(Q)} primes 3..61; {len(Q)*(len(Q)-1)//2} pairs")
for w in [13, 31, 61]:
    G = np.ones(N, dtype=np.float64)
    for l in smallp:
        if l > w:
            break
        G[2::l] = 0.0           # n - 2 = 0 mod l  <=> n = 2 mod l
        G *= l / (l - 1)
    vals, rel = [], []
    for i, p1 in enumerate(Q):
        for p2 in Q[i+1:]:
            M = X // p2
            m = np.arange(1, M + 1, dtype=np.int64)
            a, b = F[p1 * m], F[p2 * m]
            ga, gb = G[p1 * m], G[p2 * m]
            c0 = float(((a - ga) * (b - gb)).sum()) / M
            cr = float((a * b).sum()) / M
            cm = float((ga * gb).sum()) / M
            vals.append(c0)
            if cm > 0:
                rel.append(cr / cm - 1)
    bias = -sum(1.0 / (l - 1)**2 for l in P[(P > w) & (P < 10**5)])
    v = np.array(vals); r = np.array(rel)
    print(f"w = {w:2d}: mean C0 = {v.mean():+.4f}  (sd {v.std():.4f}, min {v.min():+.4f}, max {v.max():+.4f});"
          f"  mean C_raw/C_mod - 1 = {r.mean():+.4f} (sd {r.std():.4f}); predicted truncation bias ~ {bias:+.4f}"
          f"  [{time.time()-t0:5.1f} s]")
