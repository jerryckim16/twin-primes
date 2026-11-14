"""Check of Polymath8a, Lemma 6.25 (Correlation of hyper-Kloosterman sums), arXiv:1402.0811v3 / ANT 8 (2014).

Statement (v3, source line ~6581): for squarefree s, r1, r2 with (s, r1) = (s, r2) = 1, units a_i mod r_i s,
and n mod [r1,r2]s,
  sum_{h in (Z/s[r1,r2])^x} Kl3(a1 h; r1 s) conj(Kl3(a2 h; r2 s)) e_{[r1,r2]s}(n h)
     << (s[r1,r2])^eps s^{1/2} [r1,r2]^{1/2} (a2-a1, n, r1, r2)^{1/2} (a2 r1^3 - a1 r2^3, n, s)^{1/2},
with Kl3(x; q) = q^{-1} sum_{x1 x2 x3 = x mod q} e_q(x1+x2+x3) for squarefree q (eq. (kl-def)).

Family: s = 1, n = 0, r1 = g*t1, r2 = g*t2 with t1 = 5, t2 = 7 and g a product of primes p >= 11, p != 109.
Choose a2 = 1 and a1 with a1*t2^3 = a2*t1^3 mod g (and a1 = 1 mod t1). Then (a2-a1, n, r1, r2) = (a2-a1, g) = 1,
because t1^3 - t2^3 = -218 = -2*109 is a unit mod g. So the lemma predicts |LHS| <<_eps (35 g)^{1/2+eps}.

This script does three things.
 (1) Checks the CRT factorisation Kl3(x; q1 q2) = Kl3(x conj(q2)^3; q1) Kl3(x conj(q1)^3; q2) by brute force
     for small q.
 (2) Computes LHS exactly for growing g, as a product over primes (CRT; checked by brute force for the
     smallest case).
 (3) Proves the closed form LHS = (1/35) * prod_{p|g} S(p), S(p) = sum_{x in F_p^x} |Kl3(x;p)|^2 =
     p - 1 - 1/p - 1/p^2 (checked here for all p < 60), so |LHS| / (35 g)^{1/2+eps} -> infinity for every
     eps < 1/2.
"""
import cmath, math
from itertools import product

def e(x, q): return cmath.exp(2j * math.pi * (x % q) / q)

def kl3_brute(x, q):
    s = 0
    for x1 in range(q):
        for x2 in range(q):
            # x3 = x/(x1 x2) mod q when x1 x2 is a unit; other triples have product != x for unit x
            if math.gcd(x1 * x2, q) != 1: continue
            x3 = x * pow(x1 * x2, -1, q) % q
            s += e(x1 + x2 + x3, q)
    return s / q

def kl3_prime_table(p):
    return {x: kl3_brute(x, p) for x in range(1, p)}

TAB = {}
def kl3p(x, p):
    if p not in TAB: TAB[p] = kl3_prime_table(p)
    return TAB[p][x % p]

def kl3(x, factors):
    q = math.prod(factors); v = 1
    for p in factors:
        qp = q // p
        v *= kl3p(x * pow(qp, -3, p), p)
    return v

# (1) CRT factorisation check
for q1, q2 in [(5, 7), (3, 11), (7, 11)]:
    for x in [1, 2, 5, 13]:
        if math.gcd(x, q1 * q2) != 1: continue
        lhs = kl3_brute(x, q1 * q2); rhs = kl3(x, [q1, q2])
        assert abs(lhs - rhs) < 1e-9, (q1, q2, x, lhs, rhs)
print("(1) CRT factorisation of Kl3 confirmed by brute force on 5*7, 3*11, 7*11")

def lhs_direct(a1, a2, r1f, r2f):
    """sum over h in (Z/[r1,r2])^x of Kl3(a1 h; r1) conj Kl3(a2 h; r2), by direct summation over h."""
    L = math.prod(set(r1f) | set(r2f)); r1 = math.prod(r1f); r2 = math.prod(r2f); tot = 0
    for h in range(1, L):
        if math.gcd(h, L) != 1: continue
        tot += kl3(a1 * h, r1f) * kl3(a2 * h, r2f).conjugate()
    return tot

def S(p): return sum(abs(kl3p(x, p))**2 for x in range(1, p))

# (3) closed form of S(p)
for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]:
    assert abs(S(p) - (p - 1 - 1/p - 1/p**2)) < 1e-8, (p, S(p))
print("(3) S(p) = p - 1 - 1/p - 1/p^2 confirmed for all primes 3 <= p < 60")
# local factor at a prime dividing only one modulus (n = 0): sum_{x != 0} Kl3(x;p) = -1/p
for p in [5, 7, 11]:
    assert abs(sum(kl3p(x, p) for x in range(1, p)) - (-1 / p)) < 1e-9

t1, t2 = 5, 7
primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
print("\n(2) family r1 = g*5, r2 = g*7, s = 1, n = 0, a2 = 1, a1*7^3 = 5^3 mod g; claimed gcd factor (a2-a1, g) = 1")
print(f"{'g':>22} {'|LHS|':>14} {'(35g)^(1/2)':>14} {'ratio':>10} {'closed form':>14}")
for k in range(1, len(primes) + 1):
    gf = primes[:k]; g = math.prod(gf)
    # CRT: a1 = 5^3 * 7^{-3} mod g, a1 = 1 mod 5
    a1g = 125 * pow(343, -1, g) % g
    a1 = next(a for a in range(a1g, 5 * g, g) if a % 5 == 1)
    assert math.gcd(1 - a1, g) == 1
    closed = (1 / 35) * math.prod(S(p) for p in gf)
    if k <= 2:
        val = abs(lhs_direct(a1, 1, gf + [t1], gf + [t2]))
        assert abs(val - closed) < 1e-6 * max(1, closed), (val, closed)
    else:
        val = closed   # product formula (exact by CRT, confirmed directly for k = 1, 2)
    print(f"{g:>22} {val:>14.6g} {math.sqrt(35*g):>14.6g} {val/math.sqrt(35*g):>10.4g} {closed:>14.6g}")
print("\nThe ratio |LHS| / (35 g)^{1/2} grows like prod_{p|g} (p-1-1/p-1/p^2)/sqrt(p), i.e. roughly like g^{1/2};")
print("since prod (p - 2) >> g^{1-o(1)}, |LHS| / (35 g)^{1/2+eps} -> infinity for every eps < 1/2.")
print("With the corrected factor (a1 t2^3 - a2 t1^3, g)^{1/2} = g^{1/2} the bound becomes (35)^{1/2} g, consistent.")
