"""Exact check of Lichtman's Ramare identity (arXiv:2611.28392v1, Lemma 6.1, (6.4)-(6.5), p. 16)
on toy prime intervals, and of how the target enters (6.8): for mu the identity is the
sign-multiplicativity mu(v/a) = (-1)^k mu(v) ("P2"); for Lambda (the twin target) the analogue fails,
and the typical part Lambda(v) phi_+(v) vanishes identically for v > max interval.
Usage: /usr/bin/python3 -I code/parity/lichtman_ramare_check.py [N]   (default N = 200000; < 1 min)
All arithmetic exact (fractions.Fraction, integers)."""
import sys
from fractions import Fraction
from itertools import product

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000

def sieve_spf(n):
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

spf = sieve_spf(N)
def factor(v):
    f = {}
    while v > 1:
        p = spf[v]; f[p] = f.get(p, 0) + 1; v //= p
    return f
def mu(v):
    f = factor(v)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)
def Lam(v):  # unnormalised indicator of prime powers (sign/positivity is what matters)
    f = factor(v)
    return 1 if len(f) == 1 else 0

primes = [p for p in range(2, 200) if spf[p] == p]
# toy active intervals P_i = (e^lam, e^{2 lam}] replaced by disjoint prime blocks (y, y^2]-like
INTERVALS = [[p for p in primes if 3 < p <= 9], [p for p in primes if 11 <= p <= 100]]
k = len(INTERVALS)
P0 = set(p for I in INTERVALS for p in I)
A = sorted(set(a for a in (__import__('math').prod(t) for t in product(*INTERVALS))))
def omega_i(v, i):
    return sum(1 for p in INTERVALS[i] if v % p == 0)
def phi_plus(v):
    return int(all(omega_i(v, i) >= 1 for i in range(k)))
def phi_minus(v):  # a passive factor satisfying (6.3): depends only on primes outside P0 (here: parity of 2-adic val.)
    c = 0
    while v % 2 == 0:
        v //= 2; c += 1
    return 1 if c % 2 == 0 else -1

fail64 = fail65 = checked65 = 0
lam_typ_nonzero = 0; lam_rhs_nonzero = 0
for v in range(1, N + 1):
    divs = [a for a in A if a <= v and v % a == 0]
    s = sum(Fraction(1, __import__('math').prod(omega_i(v // a, i) + 1 for i in range(k))) for a in divs)
    if s > 1:
        fail64 += 1
    if all(v % (p * p) for p in P0):
        checked65 += 1
        lhs = mu(v) * phi_plus(v) * phi_minus(v)
        rhs = (-1) ** k * sum(Fraction(mu(v // a) * phi_minus(v // a),
                                       __import__('math').prod(omega_i(v // a, i) + 1 for i in range(k))) for a in divs)
        if lhs != rhs:
            fail65 += 1
        # twin target: Lambda in place of mu
        if Lam(v) * phi_plus(v) != 0:
            lam_typ_nonzero += 1
        rl = sum(Fraction(Lam(v // a), __import__('math').prod(omega_i(v // a, i) + 1 for i in range(k))) for a in divs)
        if rl != 0:
            lam_rhs_nonzero += 1
print(f"N = {N}; intervals {INTERVALS[0]} | {len(INTERVALS[1])} primes in [11,100]; |A| = {len(A)}")
print(f"(6.4) sum <= 1: failures {fail64} of {N}")
print(f"(6.5) for mu*phi: checked {checked65} v (P0-squarefree), failures {fail65}")
print(f"twin target: #v with Lambda(v)phi_+(v) != 0: {lam_typ_nonzero} (k >= 2 forces two distinct primes)")
print(f"twin target: #v where the extracted form sum_a Lambda(v/a)/prod(...) != 0: {lam_rhs_nonzero}"
      " -> the (6.5)-analogue for Lambda fails on all of these (LHS = 0)")
