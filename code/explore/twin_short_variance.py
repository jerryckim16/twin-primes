"""Exploration (Heuristic / exploratory): variance of twin-prime counts in short intervals.
For blocks [n, n+H) inside (X/2, X], compare Var/Mean of the twin count T_H with
 - Poisson / Gallagher (ratio 1), and
 - a Montgomery-Soundararajan-type deficit 1 - c*(log H - B)/log x, fitting c.
For primes (as a control) M-S predict c = 1. Question: is c = 2 for twins (one deficit per factor)?
Usage: /usr/bin/python3 -I twin_short_variance.py [X]
"""
import sys, math
import numpy as np
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**9
s = np.ones(X + 3, dtype=bool); s[:2] = False
for p in range(2, int((X + 2) ** 0.5) + 1):
    if s[p]: s[p*p::p] = False
lo = X // 2
C2 = 0.6601618158468696
H0 = 16
N = (X - lo) // H0 * H0
cP = np.empty(N // H0); cT = np.empty(N // H0); eP = np.empty(N // H0); eT = np.empty(N // H0)
CH = 2**24  # chunk (multiple of H0), keeps memory small
for st in range(0, N, CH):
    en = min(N, st + CH); i0, i1 = st // H0, en // H0
    p = s[lo+st:lo+en]; t = p & s[lo+st+2:lo+en+2]
    cP[i0:i1] = p.reshape(-1, H0).sum(axis=1); cT[i0:i1] = t.reshape(-1, H0).sum(axis=1)
    ln = np.log(np.arange(lo+st, lo+en, dtype=np.float64))
    eP[i0:i1] = (1/ln).reshape(-1, H0).sum(axis=1); eT[i0:i1] = (2*C2/ln**2).reshape(-1, H0).sum(axis=1)
del s
L = math.log(0.75 * X)
print(f"X = {X}, primes in (X/2,X]: {int(cP.sum())}, twins: {int(cT.sum())}, log x ~ {L:.3f}")
print("ratio = mean((count - HL expectation)^2) / mean(expectation), blocks of length H in (X/2, X]")
print(f"{'H':>8} {'P:ratio':>9} {'cP':>7} {'T:ratio':>9} {'cT':>7}")
rows = []
for k in range(4, 19):
    H = 2 ** k
    m = H // H0; nb = len(cP) // m
    def ratio(c, e):
        c = c[:nb*m].reshape(nb, m).sum(axis=1); e = e[:nb*m].reshape(nb, m).sum(axis=1)
        return ((c - e) ** 2).mean() / e.mean()
    rp = ratio(cP, eP); rt = ratio(cT, eT)
    # implied c with B = 0: r = 1 - c log H / L  =>  c = (1-r) L / log H
    cp = (1 - rp) * L / math.log(H); ct = (1 - rt) * L / math.log(H)
    rows.append((H, rp, cp, rt, ct))
    print(f"{H:>8} {rp:11.4f} {cp:7.3f} {rt:11.4f} {ct:7.3f}")
# least-squares fit r = a - c log H / L over H >= 2^8
# fit (1 - r) * log x = c * log H - c*B  over 2^6 <= H <= 2^14 (intercept 1 imposed, as in M-S)
sel = [r for r in rows if 64 <= r[0] <= 2**14]
x = np.array([math.log(r[0]) for r in sel])
for idx, nm in ((1, "primes"), (3, "twins")):
    y = np.array([(1 - r[idx]) * L for r in sel])
    A = np.vstack([x, np.ones_like(x)]).T
    (c, d), *_ = np.linalg.lstsq(A, y, rcond=None)
    print(f"fit {nm}: (1 - Var/Mean) log x ~ {c:.3f} log H + ({d:.3f})  =>  c = {c:.3f}, B = {-d/c:.3f}  (64 <= H <= 2^14)")
print("M-S for primes (Lambda-weighted, heuristic): c = 1, B = 1 - gamma - log(2 pi) = -1.415")
