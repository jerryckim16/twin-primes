#!/usr/bin/env python3
"""Class sums of f(n)f(n+2) for a completely multiplicative f that agrees with a real
character chi except on a set F of primes (the "Siegel world" model of the parity paper,
Proposition prop:siegel-bias).  Heuristic / exploratory numerics plus an exact check.

For Q = W*q (W = product of primes <= w, q an odd prime, chi = Legendre symbol mod q) and
every class b mod Q with gcd(b(b+2), Q) = 1 we compute exactly
    S_b   = sum_{n <= x, n = b (Q)} f(n) f(n+2),
    N_b   = #{n <= x : n = b (Q)},
    Bad_b = #{n <= x : n = b (Q), some p in F divides n(n+2)},
and check the exact inequality of the proof,
    |S_b - chi(b)chi(b+2) N_b| <= 2 Bad_b                       (deterministic),
then compare the mean normalised bias  B = mean_b chi(b)chi(b+2) S_b / N_b  with
    a crude comparison value 1 - 4 s (s = sum_{p in F, p <= x+2} 1/p; NOT the proved bound,
    which is part (2) of the proposition, checked as "avg>=bound"),
    the Euler-product heuristic prod_{p in F} (p-3)/(p+1).
Also runs f = Liouville (F = {p > w : chi(p) = +1}, plus primes where chi(p) = 0 are excluded
by the class condition).

Usage: /usr/bin/python3 -I code/parity/siegel_class_bias.py [x] [q] [w] [seed]
Output: printed table; also written to code/parity/siegel_class_bias.out by the caller.
"""
import sys
import numpy as np


def primes_upto(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def legendre_table(q):
    t = np.zeros(q, dtype=np.int8)
    sq = set((a * a) % q for a in range(1, q))
    for a in range(1, q):
        t[a] = 1 if a in sq else -1
    return t


def compl_mult(N, primes, fp):
    """f on [0, N] completely multiplicative with f(p) = fp[i] (int8 +-1)."""
    f = np.ones(N + 1, dtype=np.int8)
    f[0] = 0
    for p, v in zip(primes.tolist(), fp.tolist()):
        if v == 1:
            continue
        pk = p
        while pk <= N:
            f[pk::pk] *= -1  # multiply by f(p) = -1 once per power of p dividing n
            pk *= p
    return f


def run(x, q, w, F_mask, primes, chi, label):
    N = x + 2
    ps_small = [int(p) for p in primes if p <= w]
    W = int(np.prod(ps_small)) if ps_small else 1
    Q = W * q
    # f(p) = chi(p) off F, -chi(p) on F, for p > w, p != q; f(p) = -1 for p <= w and p = q
    chip = chi[primes % q]
    fp = np.where(F_mask, -chip, chip).astype(np.int8)
    fp[primes <= w] = -1
    fp[primes == q] = -1
    f = compl_mult(N, primes, fp)
    n = np.arange(1, x + 1)
    prod = (f[1:x + 1].astype(np.int16) * f[3:x + 3]).astype(np.int16)
    # bad indicator: some p in F divides n or n+2
    bad = np.zeros(N + 1, dtype=bool)
    for p in primes[F_mask].tolist():
        bad[p::p] = True
    badn = bad[1:x + 1] | bad[3:x + 3]
    r = n % Q
    S = np.bincount(r, weights=prod, minlength=Q)
    Nb = np.bincount(r, minlength=Q)
    B = np.bincount(r, weights=badn, minlength=Q)
    bs = np.arange(Q)
    good = np.array([np.gcd(b * (b + 2), Q) == 1 for b in range(Q)])
    cc = chi[bs % q].astype(np.int64) * chi[(bs + 2) % q]
    dev = np.abs(S - cc * Nb)
    ok = bool(np.all(dev[good] <= 2 * B[good] + 1e-9))
    bias = (cc[good] * S[good] / Nb[good])
    Fp = primes[F_mask]
    s = float(np.sum(1.0 / Fp[Fp <= N]))
    euler = float(np.prod((Fp - 3.0) / (Fp + 1.0)))
    # averaged inequality of Prop. prop:siegel-bias (ii)-(iii), exact counts, interval (0, x]
    phi2 = int(good.sum())
    lhs = float(np.sum(cc[good] * S[good]))
    sumN = float(np.sum(Nb[good]))
    Fs = Fp[Fp <= N]
    small = Fs[Fs <= x / Q]
    large = Fs[Fs > x / Q]
    Bbound = float(np.sum(2 * phi2 * (x / (small * Q) + 1)) + np.sum(2 * (x / large + 1)))
    avg_ok = lhs >= sumN - 2 * Bbound - 1e-6
    rho = phi2 / Q
    s1 = float(np.sum(1.0 / small)); s2 = float(np.sum(1.0 / large))
    rhs_norm = 1 - Q / x - 4 * s1 - 4 * Q * len(small) / x - (4 / rho) * (s2 + len(large) / x)
    lhs_norm = lhs / (rho * x)
    avg_ok = avg_ok and (lhs_norm >= rhs_norm - 1e-12)
    ok = ok and avg_ok
    rms_noise = float(np.sqrt(np.mean((S[good] - cc[good] * Nb[good] * bias.mean()) ** 2)) / np.sqrt(x / Q))
    print(f"{label:28s} Q={Q:6d} s={s:7.4f} 1-4s={1 - 4 * s:8.4f} euler={euler:.4e} "
          f"meanbias={bias.mean():+.4e} minbias={bias.min():+.4e} maxbias={bias.max():+.4e} "
          f"avg={lhs_norm:+.4f}>=bound={rhs_norm:+.4f} "
          f"exactcheck={'PASS' if ok else 'FAIL'} resid_rms/sqrt(x/Q)={rms_noise:.2f}")
    return ok


def main():
    x = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 7
    q = int(sys.argv[2]) if len(sys.argv) > 2 else 163
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    rng = np.random.default_rng(seed)
    primes = primes_upto(x + 2)
    chi = legendre_table(q)
    eligible = (primes > w) & (primes != q)
    recip = np.where(eligible, 1.0 / primes, 0.0)
    print(f"x={x} q={q} w={w} seed={seed}; f = chi off F, -chi on F (p > w)")
    allok = True
    # random F with prescribed s: include each eligible prime p >= P1 with probability pi0
    P1 = 50
    base = float(np.sum(recip[primes >= P1]))
    for s_target in [0.0, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5]:
        pi0 = min(1.0, s_target / base)
        F = eligible & (primes >= P1) & (rng.random(len(primes)) < pi0)
        allok &= run(x, q, w, F, primes, chi, f"random F, target s={s_target}")
    # F = small primes only (bias decided by few primes): all eligible p in (w, 200]
    F = eligible & (primes <= 200)
    allok &= run(x, q, w, F, primes, chi, "F = all p in (w,200]")
    # Liouville: f(p) = -1 for all p, i.e. F = {p > w, p != q, chi(p) = +1}
    F = eligible & (chi[primes % q] == 1)
    allok &= run(x, q, w, F, primes, chi, "Liouville (F = split primes)")
    print("ALL EXACT CHECKS", "PASS" if allok else "FAIL")


if __name__ == "__main__":
    main()
