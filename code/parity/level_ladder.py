#!/usr/bin/python3
"""Which rungs of the sifting-dimension ladder do levels of distribution beyond 1/2 reach?

Route card: notes/parity-attempts/2026-11-22-level-ladder.md   (Session 44; follows the Session 43 card
notes/parity-attempts/2026-11-22-dimension-ladder.md and its script code/parity/dim_ladder.py)
Run: /usr/bin/python3 -I code/parity/level_ladder.py [X]     (default X = 1e8; ~3 min, ~1.2 GB)

Rung m (m >= 2): q a prime, H < (Z/q)^* a subgroup of index m, Q_H = {primes l : l mod q in H},
T_H(x) = #{p <= x : p + 2 mod q in H and every prime factor of p + 2 lies in Q_H}.
Sifting {p + 2} by the odd primes l != q with l mod q not in H up to z = sqrt(x + 2) is a sieve of dimension
kappa_m = 1 - 1/m, and the congruence p + 2 in H removes the at most one surviving large prime (Session 43
card, Finding 1, with "= 1 mod q" replaced by "in H": if m = r m' with m, m' in H then r is in H).
With level y = x^theta and z = x^(1/2), the beta-sieve parameter is s = 2 theta; the beta-sieve lower bound is
available for s >= beta_{kappa_m} and positive exactly for s > beta_{kappa_m} (whether another sieve has a smaller
sifting limit for 1/2 < kappa < 1 is not known).

(i)   beta_kappa (sifting-limit convention: linear sieve beta = 2) for kappa_m, m = 3..8, by the same
      method of steps as dim_ladder.py, at three step sizes; threshold level theta_m = beta_{kappa_m} / 2;
      f_kappa(2 theta) at the known levels theta (BV 1/2, BFI 4/7, Maynard 7/12 and 3/5, Lichtman 66/107,
      Lichtman 5/8 under Selberg's eigenvalue conjecture). NUMERICAL (floating point), cross-checked against
      Blight's table at kappa = 0.6 and 0.75.
(ii)  An element of the lower-bound beta_{2/3}-sieve support (conditions p1...p_{m-1} p_m^{beta+1} < D for
      even m only) that is not well-factorable at level D: d = p1 p2 p3 with p_i ~ D^{0.3}. Exact rational check of
      the exponent inequalities in units of log D, GIVEN the numerical bound beta_(2/3) <= 1.225 from part (i).
(iii) Finite-X data for rung 3 with q = 7, H = {1, 6}: #T_H, the Liouville split of lambda(p + 2) on T_H,
      and the sieve-normalised ratio #T_H / (|A_H| V_H(z)). Finite-X data only; proves nothing.
"""
import sys, time, math
from fractions import Fraction as Fr
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
    return b, A, s, A * f


LEVELS = [("BV", Fr(1, 2)), ("BFI86 well-fact.", Fr(4, 7)), ("Maynard II lin. sieve", Fr(7, 12)),
          ("Maynard II triply w.f.", Fr(3, 5)), ("Lichtman triply w.f.", Fr(66, 107)),
          ("Lichtman + Selberg EC", Fr(5, 8))]

print("(i) beta_kappa for kappa_m = 1 - 1/m (sifting-limit convention), three step sizes")
print("    cross-check against Blight's table: kappa = 0.6 -> 1.1042161305, 0.75 -> 1.3981115251")
for k in (0.6, 0.75):
    print(f"    kappa={k}: " + " ".join(f"{beta_kappa(k, h)[0]:.5f}" for h in (1e-3, 5e-4, 2.5e-4)))
HS = (1e-3, 5e-4, 2.5e-4)
for m in range(3, 9):
    k = 1 - 1 / m
    R = [beta_kappa(k, h) for h in HS]
    bs = [r[0] for r in R]
    b = bs[-1]
    print(f"  m={m} kappa={k:.5f} beta = " + " ".join(f"{x:.5f}" for x in bs)
          + f"  -> threshold level theta_m = beta/2 = {b/2:.5f}")
    if m == 3:
        bb, A, s, fA = R[-1]
        h = HS[-1]
        for name, th in LEVELS:
            S = 2 * float(th)
            i = int(round(S / h))
            val = fA[i] if S > bb else 0.0
            print(f"      {name:24s} theta = {str(th):7s} = {float(th):.5f}: s = 2 theta = {S:.5f},"
                  f" s - beta = {S - bb:+.5f}, f_(2/3)(s) = {val:.5f}")
        # sensitivity of f just above beta: f(s) for s - beta in small steps (h = 2.5e-4)
        print("      f_(2/3)(beta + t): " + ", ".join(
            f"t={t}: {fA[int(round((bb + t) / h))]:.5f}" for t in (0.002, 0.005, 0.0095, 0.02, 0.05)))
print(f"  [{time.time()-t0:.1f}s]")

print("(ii) a non-well-factorable element of the lower-bound beta_(2/3)-sieve support (exact, given beta_(2/3) <= 1.225)")
beta_hi = Fr(12250, 10000)        # an upper bound for beta_(2/3) (computed 1.2241); conditions use beta + 1 <= 2.225
e = [Fr(3, 10)] * 3                # p_i = D^{3/10}, in units of log D
cond_m2 = e[0] + e[1] * (beta_hi + 1)      # even m = 2 condition p1 p2^{beta+1} < D
print(f"  m = 2 (even): p1 p2^(beta+1) = D^{cond_m2} < D: {cond_m2 < 1} (any beta <= {beta_hi})")
print(f"  no even m >= 4 for r = 3; d = D^{sum(e)} ; p1^beta = D^{e[0]*beta_hi} < D: {e[0]*beta_hi < 1}")
sub = sorted({sum(e[i] for i in range(3) if (mask >> i) & 1) for mask in range(8)})
ok = [t for t in sub if t <= Fr(1, 2) and sum(e) - t <= Fr(1, 2)]
print(f"  divisor sizes (units log D): {sub}; split Q1 = Q2 = D^(1/2) possible: {bool(ok)}")
print(f"  with the linear sieve (beta = 2): p1 p2^3 = D^{e[0] + 3*e[1]} < D: {e[0] + 3*e[1] < 1} (not in its support)")
print("  with z = x^(1/2), D = x^theta, theta in (0.61, 0.63): p_i = x^(0.3 theta) < z and d = x^(0.9 theta) > x^(1/2),")
print("  so d is above the Bombieri-Vinogradov range and needs the beyond-1/2 estimate.")

X = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10 ** 8
print(f"(iii) rung 3 data at X = {X:.0e}: q = 7, H = {{1, 6}} (index 3 in (Z/7)^*), kappa = 2/3")
N = X + 3
isp = np.ones(N, dtype=bool)
isp[:2] = False
lim = int(math.isqrt(N)) + 1
for p in range(2, lim):
    if isp[p]:
        isp[p * p::p] = False
rem = np.arange(N, dtype=np.int32)
Om = np.zeros(N, dtype=np.int8)
good = np.ones(N, dtype=bool)
for p in np.nonzero(isp[:lim])[0]:
    p = int(p)
    if p % 7 not in (1, 6):
        good[p::p] = False
    pk = p
    while pk < N:
        sl = slice(pk, N, pk)
        rem[sl] //= p
        Om[sl] += 1
        pk *= p
big = rem > 1                               # one prime factor > sqrt(N) left
Om[big] += 1
good &= ~big | np.isin(rem % 7, (1, 6))
lam = np.where(Om % 2 == 0, 1, -1).astype(np.int8)
del rem
print(f"  tables built [{time.time()-t0:.1f}s]")
ps = np.nonzero(isp[:X + 1])[0]
ps = ps[ps >= 3]
m2 = ps + 2
inH = np.isin(m2 % 7, (1, 6))
A = int(inH.sum())
T = inH & good[m2]
nT = int(T.sum())
plus = int((lam[m2[T]] == 1).sum())
z = math.sqrt(X + 2)
V = 1.0
for l in range(3, int(z) + 1):
    if isp[l] and l != 7 and (l % 7) not in (1, 6):
        V *= 1 - 1 / (l - 1)
print(f"  |A_H| = {A}, #T_H = {nT}, + share of lambda(p+2) = {plus/nT:.4f}, #T_H/(|A_H| V_H(z)) = {nT/(A*V):.4f}")
print("  (finite-X data only; the normalised ratio converges slowly and proves nothing)")
print(f"  [{time.time()-t0:.1f}s]")
