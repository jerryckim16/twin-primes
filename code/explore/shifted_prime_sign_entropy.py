#!/usr/bin/python3
"""Exploration (Session 43): block entropy of the sign sequence lambda(p+2) along consecutive primes.

notes/explorations.md, 2026-11-22. Heuristic / exploratory only.
Run: /usr/bin/python3 -I code/explore/shifted_prime_sign_entropy.py [X]   (default 1e8; ~1 min, ~1.5 GB)

Question: does the binary sequence e_j = lambda(p_j + 2) (p_j the j-th odd prime) have the block
entropies of an i.i.d. sequence with the same mean, as a Chowla-along-primes heuristic predicts, or is
there structure (lower conditional entropy at some block length)? Controls: lambda(n) on consecutive
integers n <= N_p (same length), lambda(p_j + 2) with the primes shuffled (destroys order, keeps
the mean), and i.i.d. +-1 with the same mean. For each block length L we print the plug-in entropy
H_L / L (bits per symbol), the conditional entropy h_L = H_L - H_{L-1}, and the Miller-Madow
corrected h_L. The quantity of interest is h_L(sequence) - h_L(shuffled) at each L.
"""
import sys, time, math
import numpy as np

t0 = time.time()
X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
N = X + 3
spf = np.zeros(N, dtype=np.int32)
for p in range(2, math.isqrt(N) + 1):
    if spf[p] == 0:
        blk = spf[p * p::p]
        blk[blk == 0] = p
isp = spf == 0
isp[:2] = False
spf[isp] = np.nonzero(isp)[0].astype(np.int32)
# Liouville on [0, N): lambda(n) = (-1)^Omega(n), via Omega(n) = Omega(n / spf(n)) + 1
Om = np.zeros(N, dtype=np.int8)
idx = np.arange(2, N)
# process in increasing order: n / spf(n) < n, so a vectorised pass in chunks of doubling ranges works
lo = 2
while lo < N:
    hi = min(N, 2 * lo)
    r = np.arange(lo, hi)
    Om[lo:hi] = Om[r // spf[lo:hi]] + 1
    lo = hi
lam = (1 - 2 * (Om & 1)).astype(np.int8)
P = np.nonzero(isp)[0]
P = P[(P >= 3) & (P <= X)]
e = (lam[P + 2] > 0).astype(np.uint8)
n = len(e)
rng = np.random.default_rng(20261122)
ints = (lam[2:2 + n] > 0).astype(np.uint8)
shuf = e.copy(); rng.shuffle(shuf)
iid = (rng.random(n) < e.mean()).astype(np.uint8)
print(f"X = {X:.3g}: {n} odd primes; mean of lambda(p+2) = {2*e.mean()-1:+.5f};"
      f" mean of lambda(n), n <= {n+1}: {2*ints.mean()-1:+.5f}  [{time.time()-t0:.1f}s]")


def block_entropies(b, Lmax):
    out = []
    code = np.zeros(len(b) - Lmax + 1, dtype=np.int64)
    for L in range(1, Lmax + 1):
        code = (code << 1) | b[L - 1:len(b) - Lmax + L].astype(np.int64)
        cnt = np.bincount(code, minlength=1 << L)
        p = cnt[cnt > 0] / cnt.sum()
        H = -(p * np.log2(p)).sum()
        mm = H + (np.count_nonzero(cnt) - 1) / (2 * cnt.sum() * math.log(2))   # Miller-Madow
        out.append((H, mm))
    return out


LMAX = 16
res = {name: block_entropies(b, LMAX) for name, b in
       [("lambda(p+2)", e), ("shuffled", shuf), ("iid", iid), ("lambda(n)", ints)]}
print(" L | h_L (Miller-Madow):  lambda(p+2)   shuffled     iid     lambda(n) | diff lambda(p+2)-shuffled")
for L in range(1, LMAX + 1):
    row = []
    for name in ("lambda(p+2)", "shuffled", "iid", "lambda(n)"):
        H = res[name]
        h = H[L - 1][1] - (H[L - 2][1] if L > 1 else 0.0)
        row.append(h)
    print(f"{L:2d} | {row[0]:.6f}  {row[1]:.6f}  {row[2]:.6f}  {row[3]:.6f} | {row[0]-row[1]:+.6f}")
# lag correlations of the +-1 sequence along primes
s = 2.0 * e - 1
s0 = s - s.mean()
print("lag autocorrelations of lambda(p_j+2) along primes (centred):",
      " ".join(f"{k}:{(s0[:-k]*s0[k:]).mean()/s0.var():+.5f}" for k in (1, 2, 3, 4, 5, 6, 10)))
# known consequence of local structure: consecutive primes p_j, p_{j+1} with gap 2 force p_j+2 prime
gap2 = (P[1:] - P[:-1]) == 2
print(f"share of j with p_(j+1) = p_j + 2 (then lambda(p_j+2) = -1): {gap2.mean():.5f}")
print(f"[{time.time()-t0:.1f}s]")
