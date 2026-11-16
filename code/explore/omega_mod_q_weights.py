#!/usr/bin/env python3
"""Exploration (Session 27, 16 Nov 2026): is there a "mod q" analogue of the parity obstruction?

Heuristic / exploratory.  Two parts.

(A) Combinatorics (exact LP over the rationals is not needed; scipy LP, then a
    rational witness is checked exactly).  Replace lambda(n) = (-1)^Omega(n) by the
    class Omega(n) mod q.  A "Z/q pattern weight" is a measure mu on (Z/q)^k; it is
    "fair" if every marginal is uniform, and it "kills" DHL[k, m+1] if mu is
    supported on patterns with at most m coordinates equal to 1 (primes have
    Omega = 1).  If the Moebius-randomness heuristic held for z^Omega, z = e(1/q),
    such a weight would block DHL[k, m+1].  We find: a fair killing weight exists
    iff k <= q m.  For q = 3 this "blocks" DHL[3,2], which Polymath8b proves under
    GEH -- so the heuristic must fail for z^Omega with z != +-1.

(B) Why it fails: Selberg-Delange.  sum_{n<=x} z^Omega(n) ~ x (log x)^(z-1) G(z)/Gamma(z),
    and 1/Gamma(z) vanishes only at z = 0, -1, -2, ...  So among |z| = 1 only
    z = -1 (and the trivial z = 1, which is not a twist) has a negligible mean.
    Numerically: (B1) the partial sums; (B2) a one-dimensional Selberg-type weight
    nu(n) = (sum_{d | n, d <= R} mu(d) log(R/d)/log R)^2 and the normalised twisted
    sums sum nu(n) z^Omega(n) / sum nu(n): ~0 for z = -1 (Selberg's parity example),
    clearly non-zero for z = e(1/3), e(1/4).

Usage: /usr/bin/python3 -I omega_mod_q_weights.py [x]   (default x = 10^7; ~1 min, < 1 GB)
"""
import sys, itertools, math, cmath
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
import mpmath


def fair_killing_lp(q, k, m):
    pats = list(itertools.product(range(q), repeat=k))
    ok = [p for p in pats if sum(1 for v in p if v == 1) <= m]
    # variables: mu on ok patterns; constraints: marginals uniform, total 1
    A, b = [], []
    for i in range(k):
        for v in range(q):
            A.append([1.0 if p[i] == v else 0.0 for p in ok]); b.append(1.0 / q)
    res = linprog(np.zeros(len(ok)), A_eq=np.array(A), b_eq=np.array(b),
                  bounds=[(0, None)] * len(ok), method="highs")
    return res.status == 0


def cyclic_witness(q, k, m):
    """Exact witness when k <= q m: v_j = (c + j) mod q, c uniform, over blocks.

    Split the k coordinates into m groups of size <= q; in each group use an
    independent uniformly random injective map into Z/q (a random q-permutation
    restricted to the group).  Each coordinate is uniform, and each group has at
    most one coordinate equal to 1, so at most m in total.  Checked exactly.
    """
    groups = [list(range(k))[g * q:(g + 1) * q] for g in range(m)]
    groups = [g for g in groups if g]
    assert sum(len(g) for g in groups) == k
    # distribution: product over groups of uniform injections
    dist = {}
    per_group = []
    for g in groups:
        inj = list(itertools.permutations(range(q), len(g)))
        per_group.append((g, inj))
    for choice in itertools.product(*[inj for _, inj in per_group]):
        pat = [None] * k
        for (g, _), vals in zip(per_group, choice):
            for idx, v in zip(g, vals):
                pat[idx] = v
        pat = tuple(pat)
        w = Fraction(1)
        for _, inj in per_group:
            w /= len(inj)
        dist[pat] = dist.get(pat, 0) + w
    assert sum(dist.values()) == 1
    for p in dist:
        assert sum(1 for v in p if v == 1) <= m
    for i in range(k):
        for v in range(q):
            assert sum(w for p, w in dist.items() if p[i] == v) == Fraction(1, q)
    return True


def omega_sieve(x):
    Om = np.zeros(x + 1, dtype=np.int8)
    rem = np.arange(x + 1, dtype=np.int64)
    small = np.ones(int(math.isqrt(x)) + 1, dtype=bool); small[:2] = False
    for p in range(2, len(small)):
        if small[p]:
            small[p * p::p] = False
            pk = p
            while pk <= x:
                Om[pk::pk] += 1
                rem[pk::pk] //= p
                pk *= p
    Om[2:] += (rem[2:] > 1).astype(np.int8)  # one large prime factor left
    return Om


def mobius_upto(R):
    mu = np.ones(R + 1, dtype=np.int64); mu[0] = 0
    isp = np.ones(R + 1, dtype=bool); isp[:2] = False
    for p in range(2, R + 1):
        if isp[p]:
            isp[p * p::p] = False
            mu[p::p] *= -1
            mu[p * p::p * p] = 0
    return mu


def G_of_z(z, P):
    # prod_p (1 - z/p)^(-1) (1 - 1/p)^z over primes p <= P (tail is 1 + O(1/P))
    s = mpmath.mpc(0)
    isp = np.ones(P + 1, dtype=bool); isp[:2] = False
    for p in range(2, int(math.isqrt(P)) + 1):
        if isp[p]:
            isp[p * p::p] = False
    for p in np.nonzero(isp)[0]:
        p = int(p)
        s += -mpmath.log(1 - z / p) + z * mpmath.log(1 - mpmath.mpf(1) / p)
    return mpmath.exp(s)


def main():
    x = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**7
    print("(A) fair Z/q pattern weights killing DHL[k,m+1]  (exists iff k <= q m?)")
    for q in (2, 3, 4):
        for m in (1, 2):
            row = []
            for k in range(2, 7 if q < 4 else 6):
                if q ** k > 5000:
                    continue
                lp = fair_killing_lp(q, k, m)
                pred = k <= q * m
                if pred:
                    cyclic_witness(q, k, m)
                row.append(f"k={k}:{'yes' if lp else 'no'}{'' if lp == pred else '(!)'}")
            print(f"  q={q} m={m}: " + "  ".join(row))
    print("  q=2 is the parity case (k <= 2m, Prop. bipartite (b)); q=3, m=1 'blocks' DHL[3,2],")
    print("  which PM8b proves under GEH: the randomness heuristic must fail for z = e(1/3).")

    print(f"\n(B1) Selberg-Delange at x = {x:.0e}")
    Om = omega_sieve(x)
    L = math.log(x)
    for name, z in (("-1", -1 + 0j), ("e(1/3)", cmath.exp(2j * math.pi / 3)),
                    ("e(1/4)", 1j), ("e(1/6)", cmath.exp(2j * math.pi / 6))):
        q = {"-1": 2, "e(1/3)": 3, "e(1/4)": 4, "e(1/6)": 6}[name]
        counts = np.bincount(Om[1:].astype(np.int64) % q, minlength=q)
        S = sum(int(counts[r]) * z ** r for r in range(q))
        zz = mpmath.mpc(z.real, z.imag)
        pred = x * mpmath.power(L, zz - 1) * G_of_z(zz, 10**6) * mpmath.rgamma(zz)
        print(f"  z={name:7s} |S|/x = {abs(S)/x:.3e}   predicted main term |.|/x = {abs(complex(pred))/x:.3e}"
              f"   S/pred = {complex(S)/complex(pred) if abs(complex(pred)) > 0 else float('nan')}")

    R = int(x ** 0.4)
    print(f"\n(B2) one-dimensional Selberg-type weight, R = x^0.4 = {R}")
    mu = mobius_upto(R)
    lam_d = np.zeros(x + 1)
    for d in range(1, R + 1):
        if mu[d]:
            lam_d[d::d] += mu[d] * math.log(R / d) / math.log(R)
    nu = lam_d[1:] ** 2
    Om1 = Om[1:].astype(np.int64)
    tot = nu.sum()
    for name, q in (("-1", 2), ("e(1/3)", 3), ("e(1/4)", 4), ("e(1/6)", 6)):
        z = cmath.exp(2j * math.pi / q)
        s = sum(nu[Om1 % q == r].sum() * z ** r for r in range(q))
        print(f"  z={name:7s} sum nu z^Omega / sum nu = {s/tot:.4f}  (|.| = {abs(s/tot):.4f})")
    primes_share = nu[Om1 == 1].sum() / tot
    print(f"  share of sum nu on primes (Omega = 1) = {primes_share:.4f}  (each class mod q gets 1/q under the heuristic)")


if __name__ == "__main__":
    main()
