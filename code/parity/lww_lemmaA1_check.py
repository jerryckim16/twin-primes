#!/usr/bin/python3
"""Toy checks for LWW (arXiv:2610.20242v2) Lemma A.1 (pp. 72-74) and (4.86)-(4.88) (pp. 34-35).

Run: /usr/bin/python3 -I code/parity/lww_lemmaA1_check.py
Route card: notes/parity-attempts/2026-11-26-lww-lemmaA1.md

Sections
 (A) #R_u = u prod_{p|u, p not| S}(1 - 1/p)                       exact brute force
 (B) R_u <-> {coprime (u,v), canonical c, g = g0 mod S}           exact brute force
 (C) CRT + orthogonality: sum over R_u = phase * (1/S1) sum_j K    numeric identity (complex floats)
     and the gcd claim gcd(gh+ju, gk(ud0'-1), uS1) <= S1 gcd(h,k,u) exact integers
 (D) Weil/Estermann bound |K_m(h,k)| <= tau(m) m^(1/2) gcd(h,k,m)^(1/2), all m <= MMAX, all h,k
     (integer exponent sets, float cosines, 1e-9 margin)
 (E) torus rectangle discrepancy of R_u vs (#R_u)|J1||J2|          exact counts, numeric illustration
 (F) divisor expansion, |SL2(Z/SZ)|, Euler product                 exact / numeric
 (G) the swap g -> g~ (case N < d0YM)                              exact
 (H) Lemma A.1 toy count vs main term, both cases                  exact count, numeric comparison
 (I) (4.85) <=> u0 xi - 2 c0 eta = 0, and the g0 count 2 prod p(p-1) for every line choice  exact
 (J) exponent arithmetic only for (A.3), (A.4), (4.87)-(4.88)     exact Fractions
Negative controls are marked NEG and must FAIL.
"""
import math, random, time, itertools
from fractions import Fraction as F
import numpy as np
from sympy import factorint, divisors, mobius, totient, divisor_count, zeta

T0 = time.time()
random.seed(20261126)
RESULTS = []  # (name, kind, ok_as_expected, detail)


def report(name, kind, failures, total, detail=""):
    # kind 'POS': expected failures == 0 ; 'NEG': expected failures > 0
    ok = (failures == 0) if kind == 'POS' else (failures > 0)
    RESULTS.append((name, kind, ok))
    tag = "ok" if ok else "UNEXPECTED"
    print(f"[{kind}] {name}: {failures}/{total} failures -> {tag} {detail}")


def primes_of(n):
    return list(factorint(n).keys()) if n > 1 else []


def squarefree(n):
    return all(e == 1 for e in factorint(n).values())


def sl2_mod(S):
    if S == 1:
        return [(0, 0, 0, 0)]
    out = []
    for a in range(S):
        for b in range(S):
            for c in range(S):
                for d in range(S):
                    if (a * d - b * c) % S == 1 % S:
                        out.append((a, b, c, d))
    return out


def Ru_brute(u, S, g0):
    """pairs (c mod uS, v mod uS): c=c0, v=v0 (mod S), c v = u d0' - 1 (mod uS). g0=(u0,c0,v0,d0')."""
    u0, c0, v0, d0 = g0
    m = u * S
    out = []
    for c in range(c0 % S, m, S) if S > 1 else range(m):
        for v in range(v0 % S, m, S) if S > 1 else range(m):
            if (c * v - (u * d0 - 1)) % m == 0:
                out.append((c, v))
    return out


def Ru_formula(u, S):
    r = F(u)
    for p in primes_of(u):
        if S % p:
            r *= (1 - F(1, p))
    return r


# ---------------------------------------------------------------- (A)
print("== (A) #R_u formula (p. 72)")
fails = tot = 0
neg_fail = neg_tot = 0
SQF = [1, 2, 3, 5, 6, 7, 10, 15, 30]
for S in SQF:
    G = sl2_mod(S)
    sample = G if len(G) <= 800 else random.sample(G, 150)
    for g0 in sample:
        u0 = g0[0]
        us = [u for u in range(2, 2 + 3 * S + 30) if u % S == u0 % S][:4]
        for u in us:
            n = len(Ru_brute(u, S, g0))
            tot += 1
            if n != Ru_formula(u, S):
                fails += 1
            # NEG: forget the p not| S restriction
            wrong = F(u)
            for p in primes_of(u):
                wrong *= (1 - F(1, p))
            neg_tot += 1
            if n != wrong:
                neg_fail += 1
report("A #R_u = u prod_{p|u,p!|S}(1-1/p)", 'POS', fails, tot)
report("A NEG #R_u = u prod_{p|u}(1-1/p) (drop p!|S)", 'NEG', neg_fail, neg_tot)

# ---------------------------------------------------------------- (B)
print("== (B) R_u <-> matrix congruence with canonical c (p. 72)")
fails = tot = 0
for S in [1, 2, 3, 5, 6, 15]:
    G = sl2_mod(S)
    sample = G if len(G) <= 300 else random.sample(G, 60)
    for g0 in sample:
        u0, c0, v0, d0 = g0
        for u in [x for x in range(2, 40) if x % S == u0 % S][:3]:
            m = u * S
            for v in range(1, 2 * m + 1):
                for c in range(u):
                    inR = (c - c0) % S == 0 and (v - v0) % S == 0 and (c * v - (u * d0 - 1)) % m == 0
                    canon = math.gcd(u, v) == 1 and (1 + c * v) % u == 0
                    if canon:
                        d = (1 + c * v) // u
                        cong = ((u - u0) % S == 0 and (c - c0) % S == 0 and (v - v0) % S == 0 and (d - d0) % S == 0)
                    else:
                        cong = False
                    tot += 1
                    if inR != cong:
                        fails += 1
report("B (c,v) in R_u  <=>  gcd(u,v)=1, ud-vc=1, g=g0 mod S (0<=c<u)", 'POS', fails, tot)

# ---------------------------------------------------------------- (C)
print("== (C) CRT/orthogonality identity and gcd claim (p. 73)")


_INV = {}


def kloost(m, h, k):
    if m not in _INV:
        _INV[m] = [(y, pow(y, -1, m)) for y in range(1, m) if math.gcd(y, m) == 1]
    s = 0j
    for y, yi in _INV[m]:
        t = 2 * math.pi * ((h * y + k * yi) % m) / m
        s += complex(math.cos(t), math.sin(t))
    return s


def e(x):
    return complex(math.cos(2 * math.pi * x), math.sin(2 * math.pi * x))


fails = tot = 0
gfails = gtot = 0
neg_g = neg_gt = 0
for S in [1, 3, 5, 6, 15, 30]:
    G = sl2_mod(S)
    for g0 in random.sample(G, min(len(G), 12 if S < 30 else 3)):
        u0, c0, v0, d0 = g0
        for u in [x for x in range(2, 4 * S + 40) if x % S == u0 % S][:3]:
            R = Ru_brute(u, S, g0)
            S1 = math.gcd(u, S); S2 = S // S1
            m1 = u * S1
            gam = pow(S2, -1, m1) if m1 > 1 else 0
            gam2 = pow(m1 % S2, -1, S2) if S2 > 1 else 0
            HH = 3 if S < 15 else 1
            for h in range(-HH, HH + 1):
                for k in range(-HH, HH + 1):
                    lhs = sum(e(F((h * c + k * v) % (u * S), u * S)) for c, v in R)
                    phase = e(F((gam2 * (h * c0 + k * v0)) % S2, S2)) if S2 > 1 else 1
                    rhs = phase * sum(e(F((-j * c0) % S1, S1)) * kloost(m1, gam * h + j * u, gam * k * (u * d0 - 1))
                                      for j in range(S1)) / S1
                    tot += 1
                    if abs(lhs - rhs) > 1e-8 * (1 + len(R)):
                        fails += 1
            # gcd claim, exact
            for h in range(-12, 13):
                for k in range(-12, 13):
                    for j in range(S1):
                        gg = math.gcd(math.gcd(gam * h + j * u, gam * k * (u * d0 - 1)), m1)
                        gtot += 1
                        if (S1 * math.gcd(math.gcd(h, k), u)) % gg != 0:
                            gfails += 1
                        neg_gt += 1
                        if gg > math.gcd(math.gcd(h, k), u):
                            neg_g += 1
report("C sum_{R_u} e((hc+kv)/uS) = phase*(1/S1) sum_j e(-j c0/S1) K_{uS1}(gh+ju, gk(ud0'-1))", 'POS', fails, tot)
report("C gcd(gh+ju, gk(ud0'-1), uS1) divides S1*gcd(h,k,u)", 'POS', gfails, gtot)
report("C NEG gcd <= gcd(h,k,u) (drop the S1 factor)", 'NEG', neg_g, neg_gt)

# ---------------------------------------------------------------- (D)
print("== (D) Weil/Estermann bound (A.2), all m <= MMAX, all h,k mod m")
MMAX = 160
fails = tot = 0
n_nogcd = n_prime_form = n_notau = 0
worst = 0.0
for m in range(2, MMAX + 1):
    ys = np.array([y for y in range(1, m) if math.gcd(y, m) == 1], dtype=np.int64)
    yi = np.array([pow(int(y), -1, m) for y in ys], dtype=np.int64)
    hs = np.arange(m, dtype=np.int64)
    E1 = np.exp(2j * np.pi * ((np.outer(hs, ys)) % m) / m)
    E2 = np.exp(2j * np.pi * ((np.outer(hs, yi)) % m) / m)
    K = (E1 @ E2.T)
    assert np.max(np.abs(K.imag)) < 1e-6  # K_m is real (y -> -y)
    K = np.abs(K.real)
    tau = int(divisor_count(m))
    gmat = np.gcd(np.gcd.outer(hs, hs), m)
    bound = tau * np.sqrt(m) * np.sqrt(gmat)
    tot += m * m
    fails += int(np.sum(K > bound + 1e-9))
    worst = max(worst, float(np.max(K / bound)))
    n_nogcd += int(np.sum(K > tau * math.sqrt(m) + 1e-9))
    n_prime_form += int(np.sum(K > 2 * math.sqrt(m) * np.sqrt(gmat) + 1e-9))
    n_notau += int(np.sum(K > np.sqrt(m * gmat) + 1e-9))
report(f"D |K_m(h,k)| <= tau(m) m^1/2 (h,k,m)^1/2, 2<=m<={MMAX}", 'POS', fails, tot, f"(max ratio {worst:.4f})")
report("D NEG drop gcd factor: |K| <= tau(m) m^1/2", 'NEG', n_nogcd, tot)
report("D NEG prime-modulus form for all m: |K| <= 2 m^1/2 (h,k,m)^1/2", 'NEG', n_prime_form, tot)
report("D NEG drop tau: |K| <= (m (h,k,m))^1/2", 'NEG', n_notau, tot)

# ---------------------------------------------------------------- (E)
print("== (E) rectangle discrepancy of R_u (numeric illustration of (A.4))")


def Ru_fast(u, S, g0):
    # (c,v) mod uS: c = c0 (S), c unit mod uS where needed, v = c^{-1}(u d0'-1) mod uS if solvable
    u0, c0, v0, d0 = g0
    m = u * S
    out = []
    t = (u * d0 - 1) % m
    for c in range(c0 % S if S > 1 else 0, m, S if S > 1 else 1):
        if math.gcd(c, m) == 1:
            v = (t * pow(c, -1, m)) % m
            if (v - v0) % S == 0:
                out.append((c, v))
        else:
            # c not a unit mod uS: then c*v = t has solutions only if gcd(c,m) | t; brute check
            gq = math.gcd(c, m)
            if t % gq == 0:
                for v in range(v0 % S if S > 1 else 0, m, S if S > 1 else 1):
                    if (c * v - t) % m == 0:
                        out.append((c, v))
    return out


worst_ratio = 0.0
worst_sqrt = 0.0
cnt = 0
cnt_S1 = 0
worst_S1 = 0.0
for S in [1, 3, 15]:
    G = sl2_mod(S)
    for u in [1009, 2003, 3001, 4096 + 1, 4199, 3003, 4095]:
        for g0 in random.sample([g for g in G if g[0] % S == u % S], min(4, len([g for g in G if g[0] % S == u % S]))):
            R = Ru_fast(u, S, g0)
            assert F(len(R)) == Ru_formula(u, S)
            m = u * S
            for _ in range(25):
                a1, b1 = sorted(random.sample(range(m + 1), 2))
                a2, b2 = sorted(random.sample(range(m + 1), 2))
                n = sum(1 for c, v in R if a1 <= c < b1 and a2 <= v < b2)
                main = F(len(R)) * F(b1 - a1, m) * F(b2 - a2, m)
                disc = abs(n - main)
                worst_ratio = max(worst_ratio, float(disc) / (u ** 0.99 * S * S))
                if math.gcd(u, S) > 1:
                    cnt_S1 += 1
                    worst_S1 = max(worst_S1, float(disc) / (u ** 0.99 * S * S))
                worst_sqrt = max(worst_sqrt, float(disc) / (u ** 0.5 * math.log(u) ** 2 * S * S))
                cnt += 1
print(f"  {cnt} rectangles; max |count - #R_u|J1||J2|| / (u^0.99 S^2) = {worst_ratio:.4f}; "
      f"/ (u^0.5 log^2 u S^2) = {worst_sqrt:.4f}  (numeric only; (A.4) claims << u^0.99 S^2)")
print(f"  of these, {cnt_S1} rectangles with S1 = gcd(u,S) > 1 (u = 3003, 4095); max ratio there {worst_S1:.4f}")

# ---------------------------------------------------------------- (F)
print("== (F) divisor expansion, |SL2(Z/SZ)|, Euler product (p. 74)")
fails = tot = 0
for S in [1, 2, 3, 5, 6, 7, 10, 15, 21, 30]:
    for u in range(1, 400):
        lhs = Ru_formula(u, S) / u if u > 0 else 0
        rhs = sum(F(int(mobius(l)), l) for l in divisors(u) if math.gcd(l, S) == 1)
        tot += 1
        fails += (lhs != rhs)
report("F prod_{p|u,p!|S}(1-1/p) = sum_{l|u,(l,S)=1} mu(l)/l", 'POS', fails, tot)
fails = tot = 0
for S in [1, 2, 3, 5, 6, 7, 10, 15, 30]:
    n = len(sl2_mod(S))
    f1 = 1
    for p in primes_of(S):
        f1 *= p * (p * p - 1)
    f2 = F(S) ** 3
    for p in primes_of(S):
        f2 *= (1 - F(1, p * p))
    tot += 1
    fails += not (n == f1 == f2)
report("F |SL2(Z/SZ)| = prod p(p^2-1) = S^3 prod(1-p^-2) (enumeration)", 'POS', fails, tot)
# u-sum main term, numeric
z2 = float(zeta(2))
for (U, S, u0, I1) in [(5000, 3, 1, (1.0, 4.0)), (5000, 15, 7, (2.0, 9.0)), (20000, 6, 0, (1.0, 16.0))]:
    lo, hi = I1
    tot_ = 0.0
    for u in range(math.ceil(lo * U), math.floor(hi * U) + 1):
        if u % S == u0 % S:
            tot_ += float(Ru_formula(u, S) / u)
    main = U * (hi - lo) / (S * z2)
    for p in primes_of(S):
        main /= (1 - 1 / p ** 2)
    print(f"  U={U} S={S} u0={u0}: sum = {tot_:.3f}, main = {main:.3f}, diff = {tot_ - main:.3f}, "
          f"log(2U) = {math.log(2 * U):.2f}")

# ---------------------------------------------------------------- (G)
print("== (G) swap g -> g~ (p. 74)")
fails = tot = 0
for _ in range(20000):
    u = random.randint(2, 5000); v = random.randint(2, 5000)
    if math.gcd(u, v) != 1:
        continue
    c = (-pow(v, -1, u)) % u
    d = (1 + c * v) // u
    tot += 1
    ok = (u * d - v * c == 1 and 0 <= c < u and 0 < d < v)
    ct, dt = v - d, u - c   # g~ = [[v, v-d],[u, u-c]]
    ok &= (v * dt - u * ct == 1) and (0 <= ct < v)
    ok &= (ct == (-pow(u, -1, v)) % v)   # canonical c for the column (v,u)
    ok &= (v - ct == d and u - dt == c)  # applying the rule twice gives g back
    ok &= F(ct, v) == 1 - F(c, u) - F(1, u * v)
    fails += not ok
report("G g~ canonical, det 1, involutive, (v-d)/v = 1 - c/u - 1/(uv)", 'POS', fails, tot)
nf = nt = 0
for u in range(1, 200):
    v = 1
    c = (-pow(v, -1, u)) % u if u > 1 else 0
    d = (1 + c * v) // u
    nt += 1
    nf += not (0 < d < v)
report("G NEG 0<d<v without v>1 (v=1)", 'NEG', nf, nt)

# ---------------------------------------------------------------- (H)
print("== (H) Lemma A.1 toy counts vs main term (numeric; the O-term is not small at this size)")


def lemma_count(U, N, S, g0, I1, I2, I3):
    u0, c0, v0, d0 = g0
    n = 0
    for u in range(math.ceil(I1[0] * U), math.floor(I1[1] * U) + 1):
        if (u - u0) % S:
            continue
        for v in range(math.ceil(I2[0] * N), math.floor(I2[1] * N) + 1):
            if (v - v0) % S or math.gcd(u, v) != 1:
                continue
            c = (-pow(v, -1, u)) % u
            if not (I3[0] <= F(c, u) <= I3[1]):
                continue
            d = (1 + c * v) // u
            if (c - c0) % S == 0 and (d - d0) % S == 0:
                n += 1
    return n


rel = []
for (U, N, S) in [(150, 400, 1), (150, 400, 3), (400, 150, 3), (150, 300, 5), (300, 150, 6)]:
    G = sl2_mod(S)
    I1, I2, I3 = (1, 3), (1, 2.5), (F(1, 5), F(7, 10))
    for g0 in random.sample(G, min(3, len(G))):
        n = lemma_count(U, N, S, g0, I1, I2, I3)
        main = U * N * (I1[1] - I1[0]) * (I2[1] - I2[0]) * float(I3[1] - I3[0]) / (z2 * len(G))
        rel.append(abs(n - main) / main)
        print(f"  U={U} N={N} S={S} g0={g0}: count {n}, main {main:.1f}, rel.err {abs(n-main)/main:.3f}")
print(f"  max rel. err {max(rel):.3f}")
# NEG: main term with 1/|SL2| replaced by 1/S^3 (forgetting prod(1-p^-2)) for S=6: relative error should be large
U, N, S = 300, 150, 6
g0 = sl2_mod(S)[5]
n = lemma_count(U, N, S, g0, (1, 3), (1, 2.5), (F(1, 5), F(7, 10)))
wrong = U * N * 2 * 1.5 * 0.5 / (z2 * S ** 3)
relw = abs(n - wrong) / wrong
report("H NEG main term with S^3 in place of |SL2(Z/SZ)| within 10%", 'NEG', int(relw > 0.10), 1, f"(rel.err {relw:.3f})")

# ---------------------------------------------------------------- (I)
print("== (I) (4.85) and the g0 count (p. 35), all line choices")
fails = tot = 0
for p in [3, 5, 7, 11, 13]:
    lines = [(1, x) for x in range(p)] + [(0, 1)]
    for (xi, eta) in lines:
        for u0 in range(p):
            for c0 in range(p):
                if u0 == c0 == 0:
                    continue
                # l_p(g') = {(a,b): u0 a - 2 c0 b = 0} (one-dim); equal to span(xi,eta) iff (xi,eta) in it
                lp = {((a * x) % p, (b * x) % p) for x in range(p) for (a, b) in [(2 * c0 % p, u0 % p)]}
                span = {((xi * x) % p, (eta * x) % p) for x in range(p)}
                eq = (lp == span)
                tot += 1
                fails += eq != ((u0 * xi - 2 * c0 * eta) % p == 0)
report("I l_p(g') = l_p  <=>  u0 xi_p - 2 c0 eta_p = 0 (mod p)", 'POS', fails, tot)
fails = tot = 0
for S in [3, 5, 7, 15]:
    G2 = sl2_mod(2 * S)
    ps = primes_of(S)
    linesets = [[(1, x) for x in range(p)] + [(0, 1)] for p in ps]
    for combo in itertools.product(*linesets):
        n = 0
        for (a, b, c, d) in G2:
            if a % 2 != 1 or c % 2 != 1:
                continue
            if all((a * xi - 2 * b * eta) % p == 0 for p, (xi, eta) in zip(ps, combo)):
                n += 1
        want = 2
        for p in ps:
            want *= p * (p - 1)
        tot += 1
        fails += n != want
    sl = 6
    for p in ps:
        sl *= p * (p * p - 1)
    assert len(G2) == sl
    # main-term constant
    c1 = F(want, sl)
    c2 = F(1, 3)
    for p in ps:
        c2 /= (p + 1)
    assert c1 == c2
report("I #g0 = 2 prod p(p-1) for every line choice; |SL2(Z/2S)| = 6 prod p(p^2-1); constant 1/(3 prod(p+1))", 'POS', fails, tot)

# ---------------------------------------------------------------- (J)
print("== (J) exponent arithmetic only (exact Fractions); does not check any bound, smoothing or summation")
eps = F(1, 200)
checks = []
# (A.3): |K| << (uS1)^(1/2+eps) (S1 u^0.02)^(1/2) = u^(1/2+eps+0.01) S1^(1+eps)
checks.append(("(A.3) u-exponent 1/2+1/200+1/100 = 0.515", F(1, 2) + eps + F(1, 100) == F(515, 1000)))
checks.append(("(A.3) S1-exponent 1/2+1/200+1/2 = 1.005", F(1, 2) + eps + F(1, 2) == F(1005, 1000)))
checks.append(("pairs: 0.04 + 0.515 = 0.555", F(4, 100) + F(515, 1000) == F(555, 1000)))
# tail: Delta^-11 H^-9 with Delta ~ u^-0.01, H = u^0.02  -> 0.11 - 0.18 = -0.07
checks.append(("tail exponent 11*0.01 - 9*0.02 = -0.07", 11 * F(1, 100) - 9 * F(2, 100) == F(-7, 100)))
checks.append(("zero freq u*Delta ~ u^0.99", 1 - F(1, 100) == F(99, 100)))
checks.append(("max(0.99, 0.555, 0.93) = 0.99", max(F(99, 100), F(555, 1000), F(93, 100)) == F(99, 100)))
# sum over u in [U,16U] of (N/u+1) u^0.99: exponents of N U^0.99 and U^1.99; for U <= N the second is <= the first
checks.append(("errors summed: 1 + 0.99 = 1.99 and 1 - 0.01 = 0.99", F(199, 100) == 1 + F(99, 100) and 1 - F(1, 100) == F(99, 100)))
# (4.88) threshold, exact in the variable t = L^{0.02}: with log S <= C L^0.98 and min >= x^delta,
# S^4 min^{-1/100} <= x^{4C/t - delta/100}; this is <= x^{-delta/200} iff t >= 800C/delta.
ok = True
for C in [1, 10, 1000]:
    for delta in [F(1, 100), F(1, 10), F(1, 5)]:
        t0 = 800 * C / delta
        expo = lambda t: 4 * C / t - delta / 100
        ok &= expo(t0) <= -delta / 200 and expo(t0 + 1) <= -delta / 200
        ok &= not (expo(t0 - 1) <= -delta / 200)
checks.append(("(4.88) threshold: 4C/t - delta/100 <= -delta/200 iff t = L^0.02 >= 800C/delta (exact, t0-1 fails)", ok))
fails = sum(1 for _, b in checks if not b)
for nme, b in checks:
    print(f"  {nme}: {b}")
report("J exponent arithmetic only", 'POS', fails, len(checks))
print(f"  (J) note: the threshold L >= (800C/delta)^50 is astronomically large but finite; (4.88) is asymptotic in x.")

# ---------------------------------------------------------------- summary
npos = sum(1 for r in RESULTS if r[1] == 'POS')
nneg = sum(1 for r in RESULTS if r[1] == 'NEG')
bad = [r[0] for r in RESULTS if not r[2]]
print("== SUMMARY")
print(f"positive checks: {npos}, failing: {sum(1 for r in RESULTS if r[1]=='POS' and not r[2])}")
print(f"negative controls: {nneg}, failing as they must: {sum(1 for r in RESULTS if r[1]=='NEG' and r[2])}")
print(f"unexpected outcomes: {len(bad)} {bad}")
print(f"wall time {time.time() - T0:.1f} s")
