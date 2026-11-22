#!/usr/bin/python3
"""The sifting-dimension ladder between Iwaniec-type problems and twin primes.

Route card: notes/parity-attempts/2026-11-22-dimension-ladder.md
Run: /usr/bin/python3 -I code/parity/dim_ladder.py [X]      (default X = 1e8; ~1 min, ~1 GB)

Target T_q (q an odd prime): primes p <= X with p = -1 mod q and every prime factor of p+2 = 1 mod q.
Sifting the sequence {p+2} by the primes l != q, l != 1 mod q (l odd; 2 never divides p+2) up to
z = sqrt(X+2) is a sieve problem of dimension kappa_q = (q-2)/(q-1); the congruence p+2 = 1 mod q
removes the at most one surviving large prime factor (see the card).

(i)  beta-sieve functions in dimension kappa (1/2 < kappa <= 1), from the system
        s^k F(s) = A (0 < s <= beta+1),  f(s) = 0 (s <= beta),
        (s^k f)'(s) = k s^(k-1) F(s-1) (s > beta),  (s^k F)'(s) = k s^(k-1) f(s-1) (s > beta+1),
     with beta = beta_kappa fixed by removing the s^(-2k) mode of F - f (the generic non-decaying
     mode of s D' + k D = -k D(s-1), D = F - f) and A by F, f -> 1. Method of steps with the
     trapezoid rule on a grid h, at three step sizes (2e-3, 1e-3, 5e-4) as a convergence check (beta
     is quantised to the grid, so f(2) is accurate only to about 1% for kappa <= 0.9 and about 5%
     near kappa = 0.99). The source fixes s^k F = A only on [beta-1, beta+1]; setting it on
     (0, beta+1] changes nothing, since F(s-1) is only used for s > beta. and the closed forms at kappa = 1 (beta = 2, A = 2 e^gamma,
     f(s) = 2 e^gamma log(s-1)/s on [2, 4]) as a validation. NUMERICAL, not an exact certificate.
     Output: beta_kappa, f_kappa(2), F_kappa(2) for kappa_q, q = 5, 7, 11, 13, 17, 23, 31, 61, 101,
     and the rate of f_kappa(2) -> 0 as kappa -> 1.
(ii) counts at X: #T_q, the Liouville split of lambda(p+2) on T_q (parity-neutrality of the
     condition), and the sieve-normalised ratio #T_q / (|A_q| V_q(z)) against f_kappa(2) and
     F_kappa(2) (the beta-sieve lower and upper constants at s = 2, the EH value of s);
     |A_q| = #{p <= X : p = -1 mod q}, V_q(z) = prod_{l < z, l odd, l != q, l != 1 mod q} (1 - 1/(l-1)).
     Finite-X data only; the ratio converges slowly (log log factors) and proves nothing.
"""
import sys, time, math
import numpy as np

t0 = time.time()
GAMMA = 0.5772156649015329


def solve(kappa, beta, smax, h):
    n = int(round(smax / h))
    s = np.arange(n + 1) * h
    F = np.zeros(n + 1)
    f = np.zeros(n + 1)
    F[1:] = s[1:] ** (-kappa)          # A = 1
    ib, ib1, i1 = int(round(beta / h)), int(round((beta + 1) / h)), int(round(1 / h))
    G = 0.0
    H = 1.0
    sk1 = kappa * np.concatenate(([0.0], s[1:] ** (kappa - 1)))
    skk = np.concatenate(([1.0], s[1:] ** kappa))
    for i in range(ib + 1, n + 1):
        G += h * (sk1[i - 1] * F[i - 1 - i1] + sk1[i] * F[i - i1]) / 2
        f[i] = G / skk[i]
        if i > ib1:
            H += h * (sk1[i - 1] * f[i - 1 - i1] + sk1[i] * f[i - i1]) / 2
            F[i] = H / skk[i]
    return s, F, f


def cest(kappa, beta, h, smax=40.0):
    s, F, f = solve(kappa, beta, smax, h)
    def g(S):
        i = int(round(S / h))
        return (F[i] - f[i]) * S ** (2 * kappa)
    # fit (F - f) s^{2k} = C + c1/s between s = smax/2 and smax
    return (smax * g(smax) - smax / 2 * g(smax / 2)) / (smax / 2), s, F, f


def beta_kappa(kappa, h, lo=1.0 + 1e-9, hi=2.6):
    clo = cest(kappa, lo, h)[0]
    assert (cest(kappa, hi, h)[0] > 0) != (clo > 0), "no sign change in the bracket"
    for _ in range(36):
        mid = (lo + hi) / 2
        c = cest(kappa, mid, h)[0]
        if (c > 0) == (clo > 0):
            lo, clo = mid, c
        else:
            hi = mid
    b = (lo + hi) / 2
    _, s, F, f = cest(kappa, b, h)
    A = 1.0 / F[-1]
    i2 = int(round(2.0 / h))
    return b, A, A * f[i2], A * F[i2], A * (F[-1] - f[-1])


print("(i) beta-sieve functions (numerical; three step sizes)")
# validation at kappa = 1
for h in (2e-3, 1e-3):
    b, A, f2, F2, _ = beta_kappa(1.0, h)
    s, F, f = solve(1.0, 2.0, 6.0, h)
    i3 = int(round(3.0 / h))
    print(f"  kappa=1, h={h}: beta={b:.5f} (exact 2), A={A:.6f} (2e^gamma={2*math.exp(GAMMA):.6f}),"
          f" f(3)*A_exact={2*math.exp(GAMMA)*f[i3]:.6f} (exact {2*math.exp(GAMMA)*math.log(2)/3:.6f})")
rows = []
print("  q   kappa_q   beta at h = 2e-3, 1e-3, 5e-4 | f_k(2) at the three h      | F_k(2)   f_k(2)/(1-kappa)")
for q in (5, 7, 11, 13, 17, 23, 31, 61, 101):
    k = (q - 2) / (q - 1)
    R = [beta_kappa(k, h) for h in (2e-3, 1e-3, 5e-4)]
    b3, A3, f3, F3, _ = R[2]
    rows.append((q, k, b3, f3, F3))
    print(f"  {q:3d} {k:.6f}  " + " ".join(f"{r[0]:.5f}" for r in R) + " | "
          + " ".join(f"{r[2]:.5f}" for r in R) + f" | {F3:.5f}  {f3/(1-k):.4f}")
print(f"  [{time.time()-t0:.1f}s]")

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
N = X + 3
print(f"(ii) counts at X = {X:.3g}")
spf = np.zeros(N, dtype=np.int32)
r = int(math.isqrt(N))
for p in range(2, r + 1):
    if spf[p] == 0:
        blk = spf[p * p::p]
        blk[blk == 0] = p
spf_is0 = spf == 0
spf[spf_is0] = np.arange(N, dtype=np.int32)[spf_is0]   # primes (and 0, 1)
isprime = spf_is0.copy(); isprime[:2] = False
primes = np.nonzero(isprime)[0]
P = primes[(primes >= 3) & (primes <= X)]
z = math.sqrt(X + 2) + 0.5   # sift by l < z, i.e. l <= sqrt(X+2): excludes m = r^2 = X + 2
for q in (3, 5, 7, 11, 13):
    Aq = P[(P + 1) % q == 0]
    m = Aq + 2
    good = np.ones(len(m), dtype=bool)
    lam = np.ones(len(m), dtype=np.int8)
    cur = m.copy()
    while True:
        act = cur > 1
        if not act.any():
            break
        pf = spf[cur[act]]
        good[np.nonzero(act)[0][(pf % q) != 1]] = False
        lam[act] = -lam[act]
        cur[act] = cur[act] // pf
    nT = int(good.sum())
    lp = int((lam[good] == 1).sum()); lm = nT - lp
    V = 1.0
    for l in primes[(primes >= 3) & (primes < z)]:
        if l != q and l % q != 1:
            V *= 1 - 1 / (l - 1)
    ratio = nT / (len(Aq) * V)
    k = (q - 2) / (q - 1)
    print(f"  q={q:3d} kappa={k:.4f}: |A_q|={len(Aq)}, #T_q={nT}, lambda(p+2)=+1: {lp}, -1: {lm}"
          f" (+ share {lp/max(nT,1):.4f}); #T_q/(|A_q| V_q(z)) = {ratio:.4f}")
# twin primes as the kappa -> 1 end: p+2 prime, lambda(p+2) = -1 always
tw = int(isprime[P + 2].sum())
V1 = 1.0
for l in primes[(primes >= 3) & (primes < z)]:
    V1 *= 1 - 1 / (l - 1)
print(f"  twins (kappa=1 end): #{{p<=X: p+2 prime}}={tw}, all with lambda(p+2) = -1;"
      f" #/(|A| V(z)) = {tw/(len(P)*V1):.4f}  (f_1(2) = 0, F_1(2) = e^gamma = {math.exp(GAMMA):.4f})")
print(f"[{time.time()-t0:.1f}s]")
