#!/usr/bin/env python3
"""Exploration (Heuristic / exploratory, Session 16): how far is the Liouville function from the "Siegel-zero
world" lambda ~ chi_D, measured on the twin correlation itself?

In Heath-Brown's Siegel-zero argument the twin-prime parity obstruction disappears because lambda(n) ~ chi_D(n)
(most small primes inert in Q(sqrt(-D))), so lambda(n)lambda(n+2) ~ chi_D(n)chi_D(n+2), whose mean is not zero.
For the nine class-number-one discriminants -D we compute, for n <= X:
  S1(X) = sum lambda(n) chi_D(n)                       (ordinary pretentiousness; ~X^beta if L(beta,chi_D)=0)
  S2(X) = sum lambda(n)lambda(n+2) chi_D(n)chi_D(n+2)  ("pretentious twin" statistic; ~X in the Siegel world)
  S3(X) = sum lambda(n)lambda(n+2)                     (two-point Chowla sum, for scale)
  dist2(X) = sum_{p<=X} (1 + chi_D(p))/p               (squared pretentious distance D(lambda, chi_D; X)^2)
and print them normalised by sqrt(X).  Nothing here is a theorem; it is a measurement.
usage: python3 code/explore/siegel_pretentious_twin.py [X=20000000] -> code/explore/siegel_pretentious_twin.json"""
import sys, json, os, math
import numpy as np
X = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
N = X + 3
spf = np.zeros(N, dtype=np.int32)
for p in range(2, int(N ** 0.5) + 1):
    if spf[p] == 0:
        blk = spf[p * p::p]
        blk[blk == 0] = p
spf[spf == 0] = np.arange(N, dtype=np.int32)[spf == 0]
lam = np.zeros(N, dtype=np.int8); lam[1] = 1
k = 1
while k < N:
    lo, hi = k + 1 if k == 1 else k, min(2 * k, N)
    idx = np.arange(max(lo, 2), hi)
    lam[idx] = -lam[idx // spf[idx]]
    k *= 2
isprime = np.zeros(N, dtype=bool); isprime[2:] = spf[2:] == np.arange(2, N)
def kron(D):
    # Kronecker symbol (-D / n) for n mod D' (period D or 4D); computed via Jacobi with sympy-free code
    def jac(a, n):
        # Kronecker symbol (a/n), n >= 1
        if n == 1:
            return 1
        res = 1
        while n % 2 == 0:
            n //= 2
            if a % 2 == 0:
                return 0
            if a % 8 in (3, 5):
                res = -res
        a %= n
        while a:
            while a % 2 == 0:
                a //= 2
                if n % 8 in (3, 5):
                    res = -res
            a, n = n, a
            if a % 4 == 3 and n % 4 == 3:
                res = -res
            a %= n
        return res if n == 1 else 0
    per = 4 * D
    tab = np.array([jac(-D, m) if m > 0 else 0 for m in range(per)], dtype=np.int8)
    return tab[np.arange(N) % per]
out = dict(X=X, discriminants={})
ns = np.arange(1, X + 1)
ll2 = lam[1:X + 1].astype(np.int64) * lam[3:X + 3]
checkpoints = [10 ** k for k in range(3, 9) if 10 ** k <= X] + ([X] if X not in [10 ** k for k in range(3, 9)] else [])
S3 = np.cumsum(ll2)
for D in (3, 4, 7, 8, 11, 19, 43, 67, 163):
    chi = kron(D)
    s1 = np.cumsum(lam[1:X + 1].astype(np.int64) * chi[1:X + 1])
    cc = chi[1:X + 1].astype(np.int64) * chi[3:X + 3]
    s2 = np.cumsum(ll2 * cc)
    pr = np.nonzero(isprime[:X + 1])[0]
    d2 = np.cumsum((1 + chi[pr].astype(np.float64)) / pr)
    rec = []
    for c in checkpoints:
        np_ = np.searchsorted(pr, c, side="right")
        rec.append(dict(X=c, S1_over_sqrtX=float(s1[c - 1] / math.sqrt(c)), S2_over_sqrtX=float(s2[c - 1] / math.sqrt(c)),
                        S2_over_X=float(s2[c - 1] / c), dist2=float(d2[np_ - 1]), loglogX=math.log(math.log(c)),
                        mean_chichi2=float(cc[:c].mean())))
    out["discriminants"][str(D)] = rec
out["S3_over_sqrtX"] = {str(c): float(S3[c - 1] / math.sqrt(c)) for c in checkpoints}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "siegel_pretentious_twin.json"), "w"), indent=1)
for D, rec in out["discriminants"].items():
    r = rec[-1]; r3 = rec[2]
    print("D=%4s  X=%d: S1/sqrtX %+8.3f  S2/sqrtX %+8.3f  S2/X %+.2e  dist2 %.3f (loglogX %.3f)  mean chi chi(+2) %+.4f | at 1e5: dist2 %.3f S2/X %+.2e" % (
        D, r["X"], r["S1_over_sqrtX"], r["S2_over_sqrtX"], r["S2_over_X"], r["dist2"], r["loglogX"], r["mean_chichi2"], r3["dist2"], r3["S2_over_X"]))
print("S3/sqrtX:", out["S3_over_sqrtX"])
