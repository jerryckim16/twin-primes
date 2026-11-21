#!/usr/bin/python3
"""Linnik's identity on rough pairs: the "convolution-depth ladder".

Route card: notes/parity-attempts/2026-11-21-linnik-ladder.md
Run: /usr/bin/python3 -I code/parity/linnik_ladder.py [X ...]   (default X = 1e7 1e8)

(i)  exact checks:
     - sum_j (-1)^(j-1) (j-1)! S(r,j) = [r = 1] for r <= 40 (integers);
     - Linnik's identity  Lambda(n)/log n = sum_j (-1)^(j-1)/j d'_j(n)  for ALL 2 <= n <= 1e5
       (prime powers included), d'_j computed by direct Dirichlet convolution of 1_{m>=2};
     - d'_j(n) = j! S(Omega(n), j) for every squarefree n <= 1e5.
(ii) for X and J = 3, 4, z = X^(1/J), rough = all prime factors > z, pairs (n, n+2) with
     2 <= n, n+2 <= X both rough: the joint factorisation-type table N, the correlations
     S_{j,j'} = sum d'_j(n) d'_j'(n+2), the exact reconstruction of
     T = sum (Lambda/log)(n) (Lambda/log)(n+2) = sum_{j,j'} c_j c_j' S_{j,j'}, c_j = (-1)^(j-1)/j,
     the cancellation ratio sum|c_j c_j' S_{j,j'}| / T, and the Liouville-twisted ratios
     rho_{j,j'} = sum lambda(n) lambda(n+2) d'_j d'_j' / S_{j,j'} (the change of S_{j,j'} under the
     fair weight 1 - lambda(n) lambda(n+2), which kills twin primes).
(iii) at X = 1e7, for the UNRESTRICTED Titchmarsh correlations sum_p log p d_k(p+2), k = 2,3,4,6,8,
     the ratio of the lambda(p+2)-twisted sum to the untwisted one.
"""
import sys, time, math
from fractions import Fraction
from math import comb, factorial
import numpy as np

t0 = time.time()


def stirling2_table(R):
    S = [[0] * (R + 1) for _ in range(R + 1)]
    S[0][0] = 1
    for r in range(1, R + 1):
        for j in range(1, r + 1):
            S[r][j] = j * S[r - 1][j] + S[r - 1][j - 1]
    return S


ST = stirling2_table(40)

# ---------------- (i) exact checks ----------------
print("== (i) exact checks ==")
bad = [r for r in range(1, 41)
       if sum((-1) ** (j - 1) * factorial(j - 1) * ST[r][j] for j in range(1, r + 1)) != (1 if r == 1 else 0)]
print("Stirling identity sum_j (-1)^(j-1)(j-1)! S(r,j) = [r=1], r = 1..40: failures =", bad)
print("coefficient mass A(r) = sum_j (j-1)! S(r,j) (sum of |coefficients| for Omega = r, squarefree):")
for r in (1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40):
    A = sum(factorial(j - 1) * ST[r][j] for j in range(1, r + 1))
    print(f"  r={r:2d}  A(r)={A:.4e}  A(r)/((r-1)!/(2 (log 2)^r))={A / (factorial(r - 1) / (2 * math.log(2) ** r)):.6f}")

N0 = 10 ** 5
JMAX = N0.bit_length()  # d'_j(n) = 0 for j > log2 n
D = [None, np.zeros(N0 + 1, dtype=np.int64)]
D[1][2:] = 1
for j in range(2, JMAX + 1):
    Dj = np.zeros(N0 + 1, dtype=np.int64)
    prev = D[j - 1]
    for a in range(2, N0 // 2 + 1):
        m = N0 // a
        Dj[2 * a: a * m + 1: a] += prev[2: m + 1]
    D.append(Dj)
# factorisations of n <= N0
spf = np.arange(N0 + 1)
for p in range(2, int(N0 ** 0.5) + 1):
    if spf[p] == p:
        blk = spf[p * p::p]
        np.minimum(blk, p, out=blk)
L = 1
for j in range(1, JMAX + 1):
    L = L * j // math.gcd(L, j)
fail_linnik = fail_stir = nsq = 0
for n in range(2, N0 + 1):
    m, exps = n, []
    while m > 1:
        p = spf[m]; e = 0
        while m % p == 0:
            m //= p; e += 1
        exps.append(e)
    lhs = (L // exps[0]) if len(exps) == 1 else 0          # L * Lambda(n)/log n
    rhs = sum((-1) ** (j - 1) * (L // j) * int(D[j][n]) for j in range(1, JMAX + 1))
    fail_linnik += (lhs != rhs)
    if max(exps) == 1:
        nsq += 1
        r = len(exps)
        fail_stir += any(int(D[j][n]) != factorial(j) * (ST[r][j] if j <= r else 0) for j in range(1, JMAX + 1))
print(f"Linnik identity, all 2 <= n <= {N0} (prime powers included): failures = {fail_linnik}")
print(f"d'_j(n) = j! S(Omega(n), j), all {nsq} squarefree n <= {N0}, j <= {JMAX}: failures = {fail_stir}")
print(f"[time {time.time() - t0:.1f}s]")

# ---------------- (ii) rough pairs ----------------
# factorisation types of z-rough n <= X with Omega <= 3, coded by exponent signature
TYPES = [(), (1,), (1, 1), (2,), (1, 1, 1), (2, 1), (3,)]
NAMES = ["-", "p", "pq", "p^2", "pqr", "p^2q", "p^3"]


def dprime(exps, j):
    """number of ordered factorisations into j factors >= 2 of n with exponent signature exps"""
    if not exps:
        return 0
    d = lambda i: (math.prod(comb(e + i - 1, i - 1) for e in exps) if i >= 1 else 0)
    return sum((-1) ** (j - i) * comb(j, i) * d(i) for i in range(0, j + 1))


def vm(exps):  # Lambda(n)/log n
    return Fraction(1, exps[0]) if len(exps) == 1 else Fraction(0)


def liou(exps):
    return (-1) ** sum(exps)


def run(X, Js):
    t1 = time.time()
    M = X + 1
    isp = np.ones(M, dtype=bool); isp[:2] = False
    for p in range(2, int(M ** 0.5) + 1):
        if isp[p]:
            isp[p * p::p] = False
    primes = np.nonzero(isp)[0]
    for J in Js:
        z = X ** (1.0 / J)
        rough = np.ones(M, dtype=bool); rough[:2] = False
        for p in primes[primes <= z]:
            rough[p::p] = False
        Om = np.zeros(M, dtype=np.uint8); om = np.zeros(M, dtype=np.uint8)
        for p in primes[primes > z]:
            p = int(p)
            om[p::p] += 1
            q = p
            while q < M:
                Om[q::q] += 1
                q *= p
        assert int(Om[rough].max()) <= J - 1
        # type code
        code = np.zeros(M, dtype=np.int8)
        for t, ex in enumerate(TYPES):
            if t == 0:
                continue
            code[rough & (Om == sum(ex)) & (om == len(ex))] = t
        assert np.all(code[rough] > 0)
        # n runs over 2 <= n <= X - 2 (so n + 2 <= X); slices avoid index arrays (memory)
        pair = rough[2:X - 1] & rough[4:X + 1]
        K = len(TYPES)
        Ntab = np.bincount(code[2:X - 1][pair].astype(np.int64) * K + code[4:X + 1][pair],
                           minlength=K * K).reshape(K, K)
        used = [t for t in range(1, K) if Ntab[t].sum() + Ntab[:, t].sum() > 0]
        print(f"\n== X = {X:.0e}, J = {J}, z = X^(1/J) = {z:.2f}: {int(pair.sum())} rough pairs ==")
        print("N(type(n), type(n+2)):")
        print("        " + "".join(f"{NAMES[t]:>10s}" for t in used))
        for t in used:
            print(f"  {NAMES[t]:>5s} " + "".join(f"{int(Ntab[t, u]):10d}" for u in used))
        jr = range(1, J)
        Sjj = {(j, k): sum(dprime(TYPES[t], j) * dprime(TYPES[u], k) * int(Ntab[t, u]) for t in used for u in used)
               for j in jr for k in jr}
        Ljj = {(j, k): sum(liou(TYPES[t]) * liou(TYPES[u]) * dprime(TYPES[t], j) * dprime(TYPES[u], k) * int(Ntab[t, u])
                           for t in used for u in used) for j in jr for k in jr}
        c = {j: Fraction((-1) ** (j - 1), j) for j in jr}
        T = sum(c[j] * c[k] * Sjj[j, k] for j in jr for k in jr)
        Tdirect = sum(vm(TYPES[t]) * vm(TYPES[u]) * int(Ntab[t, u]) for t in used for u in used)
        twins = int(Ntab[1, 1])
        mass = sum(abs(c[j] * c[k]) * Sjj[j, k] for j in jr for k in jr)
        print("S_{j,j'} = sum d'_j(n) d'_j'(n+2);  rho = (sum lambda lambda d'_j d'_j')/S_{j,j'}:")
        for j in jr:
            print("  " + "  ".join(f"S{j}{k}={Sjj[j, k]:>10d} (rho={Ljj[j, k] / Sjj[j, k]:+.4f})" for k in jr))
        print(f"T = sum_jj' c_j c_j' S_jj' = {float(T):.2f};  direct sum (Lambda/log)(Lambda/log) = {float(Tdirect):.2f};"
              f"  exact equality: {T == Tdirect}")
        print(f"twin-prime pairs among rough pairs = {twins};  T - twins = {float(T - twins):.2f} (prime-power pairs)")
        print(f"cancellation ratio sum|c c S| / T = {float(mass / T):.4f}  ->  relative accuracy needed in every S_jj' "
              f"for a non-trivial T: < {float(T / mass):.4f}")
        # fair weight w = 1 - lambda(n) lambda(n+2): kills twins, preserves Type I data heuristically
        Sw = {key: Sjj[key] - Ljj[key] for key in Sjj}
        Tw = sum(c[j] * c[k] * Sw[j, k] for j in jr for k in jr)
        print("under the fair weight 1 - lambda(n)lambda(n+2): S^w_jj'/S_jj' = "
              + ", ".join(f"{j}{k}:{Sw[j, k] / Sjj[j, k]:.4f}" for j in jr for k in jr)
              + f";  T^w = {float(Tw):.2f};  twin pairs^w = 0")
        mean_ll = sum(liou(TYPES[t]) * liou(TYPES[u]) * int(Ntab[t, u]) for t in used for u in used) / int(pair.sum())
        print(f"mean lambda(n)lambda(n+2) on rough pairs = {mean_ll:+.4f}")
    print(f"[X = {X:.0e} done in {time.time() - t1:.1f}s]")


def titchmarsh_twist(X, ks=(2, 3, 4, 6, 8)):
    """(iii) unrestricted Titchmarsh-type data: for primes p <= X - 2,
    ratio sum_p lambda(p+2) d_k(p+2) / sum_p d_k(p+2)  (log p weights; prime powers omitted).
    The fair weight 1 + lambda(n+2) at a prime n (twin killer) changes sum Lambda(n) d_k(n+2) by this ratio."""
    t1 = time.time()
    M = X + 1
    isp = np.ones(M, dtype=bool); isp[:2] = False
    for p in range(2, int(M ** 0.5) + 1):
        if isp[p]:
            isp[p * p::p] = False
    primes = np.nonzero(isp)[0]
    vmax = int(math.log2(M)) + 1
    # exponent of each prime handled via powers; store per-n the multiplicative d_k and lambda
    dk = {k: np.ones(M, dtype=np.float64) for k in ks}
    lam = np.ones(M, dtype=np.int8)
    for p in primes:
        p = int(p); q = p; e = 1
        while q < M:
            lam[q::q] *= -1
            for k in ks:
                dk[k][q::q] *= (e + k - 1) / e
            q *= p; e += 1
    pr = primes[primes <= X - 2]
    w = np.log(pr.astype(np.float64))
    print(f"\n== (iii) X = {X:.0e}: unrestricted Titchmarsh data, sum_p log p * f(p+2) ==")
    for k in ks:
        a = dk[k][pr + 2]
        print(f"  k={k}: sum log p d_k(p+2) = {np.dot(w, a):.4e};  twist ratio sum lambda d_k / sum d_k = "
              f"{np.dot(w, lam[pr + 2] * a) / np.dot(w, a):+.5f}")
    print(f"  (for comparison, sum over p of log p * lambda(p+2) / sum log p = {np.dot(w, lam[pr + 2]) / w.sum():+.5f})")
    print(f"[done in {time.time() - t1:.1f}s]")


Xs = [int(float(a)) for a in sys.argv[1:]] or [10 ** 7, 10 ** 8]
for X in Xs:
    run(X, (3, 4))
titchmarsh_twist(10 ** 7)
print(f"\ntotal runtime {time.time() - t0:.1f}s")
