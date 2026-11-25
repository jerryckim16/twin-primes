#!/usr/bin/env python3
"""Exploration (Session 54, function fields; Heuristic / exploratory only).
Fixed small odd q, growing n: twin irreducibles and two-point Moebius correlation in F_q[T].

For monic f of degree n over F_q (q odd prime), encoded as idx = sum_{i<n} c_i q^i (leading T^n implicit):
  N_2(q,n)  = #{f : f, f+1 both irreducible}
  Psi_2(q,n) = sum_f Lambda(f) Lambda(f+1)   (Lambda(P^k) = deg P)
  C(q,n)    = q^{-n} sum_f mu(f) mu(f+1)
Prediction (derived here from local densities, no source opened for it): f, f+1 avoid P with local density
  (1 - 2/|P|) (two forbidden classes 0, -1 mod P, distinct since q odd), against (1 - 1/|P|)^2 for independent
  events, so S(q) = prod_P (1 - 2/|P|)/(1 - 1/|P|)^2 = prod_P (1 - 1/(|P|-1)^2) (absolutely convergent), and
  Psi_2 ~ S(q) q^n,  N_2 ~ HL(q,n) := S(q) q^n / n^2.
  E(q,n) = N_2/HL - 1,  E_Lam(q,n) = Psi_2/(S q^n) - 1.
Method: sieve by monic irreducibles P of degree <= n/2 (and P^2): f reducible iff such a P divides f; for squarefree f,
  Omega(f) = #small factors + [small degree sum < n]. Multiples P*g are generated as base-q digit vectors (numpy).
Checks: irreducible count vs (1/n) sum_{d|n} mu(d) q^{n/d}; #squarefree = q^n - q^{n-1}; sum mu = 0 (n >= 2);
  brute force (python-flint factor) for small n.
usage: ffq_twin_uniformity.py q nmax [nbrute]"""
import sys, time, math, resource
import numpy as np
import flint

def mobius(m):
    r, p = 1, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0: return 0
            r = -r
        p += 1
    return -r if m > 1 else r

def n_irr(q, n):
    return sum(mobius(d) * q ** (n // d) for d in range(1, n + 1) if n % d == 0) // n

def monic_coeffs(q, d):
    """all monic polys of degree d as coefficient lists (low to high)"""
    for k in range(q ** d):
        c = []
        for _ in range(d): c.append(k % q); k //= q
        yield c + [1]

def small_irreducibles(q, dmax):
    out = []
    for d in range(1, dmax + 1):
        for c in monic_coeffs(q, d):
            fl = flint.nmod_poly(c, q)
            fac = fl.factor()[1]
            if len(fac) == 1 and fac[0][1] == 1: out.append(c)
    return out

def polymul(a, b, q):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] = (r[i + j] + x * y) % q
    return r

INNER = 21  # rows of inner digit block ~ q^m <= 2^INNER

def multiples_idx(P, n, q, pw):
    """yield arrays of idx of all monic degree-n multiples P*(T^{n-d} + r), deg r < n-d."""
    d = len(P) - 1; k = n - d
    base = np.zeros(n, np.int64)
    for i in range(d): base[k + i] = P[i]            # lower coefficients of P*T^k (T^n dropped)
    m = k
    while m > 0 and q ** m > (1 << INNER): m -= 1
    # inner digits of P*r, deg r < m: D shape (q^m, n), built recursively
    D = np.zeros((1, n), np.int8)
    for j in range(m):
        s = np.zeros(n, np.int8)
        for i in range(d + 1):
            if i + j < n: s[i + j] = P[i]
        D = np.concatenate([(D + ((a * s.astype(np.int16)) % q).astype(np.int8)) % q for a in range(q)], axis=0).astype(np.int8)  # keep int8 sums < 2q
    # outer digits r_j, j = m..k-1
    for t in range(q ** (k - m)):
        b = base.copy(); tt = t
        for j in range(m, k):
            a = tt % q; tt //= q
            if a:
                for i in range(d + 1):
                    if i + j < n: b[i + j] = (b[i + j] + a * P[i]) % q
        b8 = b.astype(np.int8)
        idx = np.zeros(D.shape[0], np.int64)
        for i in range(n):
            col = D[:, i] + b8[i]
            col[col >= q] -= q
            idx += col.astype(np.int64) * pw[i]
        yield idx

def sieve(q, n, smallP):
    N = q ** n
    pw = [q ** i for i in range(n)]
    dsum = np.zeros(N, np.uint8); cnt = np.zeros(N, np.uint8); nsq = np.zeros(N, bool)
    for P in smallP:
        d = len(P) - 1
        if 2 * d > n: break
        for idx in multiples_idx(P, n, q, pw):
            dsum[idx] += d; cnt[idx] += 1
        P2 = polymul(P, P, q)
        for idx in multiples_idx(P2, n, q, pw):
            nsq[idx] = True
    irr = dsum == 0
    big = (dsum < n).astype(np.int16)
    mu = np.where(nsq, 0, 1 - 2 * ((cnt.astype(np.int16) + big) % 2)).astype(np.int8)
    del dsum, cnt, big, nsq
    lam = irr.astype(np.int64) * n
    # proper prime powers P^k, deg P = n/k, k >= 2
    for P in smallP:
        d = len(P) - 1
        if n % d or d == n: continue
        Q = [1]
        for _ in range(n // d): Q = polymul(Q, P, q)
        lam[sum(Q[i] * pw[i] for i in range(n))] = d
    return irr, mu, lam

def shift1(a, q):
    return np.roll(a.reshape(-1, q), -1, axis=1).reshape(-1)   # f -> f + 1 (c_0 -> c_0 + 1 mod q)

def brute(q, n):
    N2 = 0; C = 0
    def info(c):
        fac = flint.nmod_poly(c, q).factor()[1]
        if any(e > 1 for _, e in fac): return 0, 0
        return (1 if len(fac) == 1 else 0), (-1) ** len(fac)
    for c in monic_coeffs(q, n):
        i1, m1 = info(c); c2 = c[:]; c2[0] = (c2[0] + 1) % q; i2, m2 = info(c2)
        N2 += i1 * i2; C += m1 * m2
    return N2, C

def main(q, nmax, nbrute):
    t0 = time.time()
    smallP = small_irreducibles(q, nmax // 2)
    # singular series: prod_d (1 - 1/(q^d - 1)^2)^{pi_q(d)}, d <= 80 (tail ~ q^-80)
    logS = sum(n_irr(q, d) * math.log1p(-1.0 / (q ** d - 1) ** 2) for d in range(1, 81))
    S = math.exp(logS)
    print("# q = %d, S(q) = prod_P (1 - 1/(|P|-1)^2) = %.8f; HL(q,n) = S q^n / n^2" % (q, S))
    print("# Heuristic / exploratory. CR bound |C| <= 4n q^-1/2 + 6n^2/q; Weil step nontrivial iff q > (2n-3)^2")
    print("#  n        q^n       N_2        HL      E=N2/HL-1   E_Lam    E*q^(n/2)  (N2-HL)/sqrt(HL)   C(q,n)   C*q^(n/2)  CRbound  check  sec")
    for n in range(2, nmax + 1):
        t1 = time.time()
        irr, mu, lam = sieve(q, n, smallP)
        ni = int(irr.sum()); ok = ni == n_irr(q, n)
        ok &= int(mu.sum()) == 0 and int((mu != 0).sum()) == q ** n - q ** (n - 1)
        N2 = int((irr & shift1(irr, q)).sum())
        Psi = int((lam * shift1(lam, q)).sum())
        Cs = int((mu.astype(np.int64) * shift1(mu, q)).sum())
        if n <= nbrute:
            bN, bC = brute(q, n); ok &= (bN == N2 and bC == Cs)
        HL = S * q ** n / n ** 2
        E = N2 / HL - 1; EL = Psi / (S * q ** n) - 1; C = Cs / q ** n
        print("%3d %11d %9d %11.1f %+10.5f %+9.5f %+9.3f %+9.3f %+11.6f %+9.3f %8.2f  %s  %.1f" % (
            n, q ** n, N2, HL, E, EL, E * q ** (n / 2), (N2 - HL) / math.sqrt(HL), C, C * q ** (n / 2),
            4 * n * q ** -0.5 + 6 * n * n / q, "ok" if ok else "FAIL", time.time() - t1), flush=True)
        del irr, mu, lam
    print("# total %.1f s, max RSS %.0f MB" % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 0)
