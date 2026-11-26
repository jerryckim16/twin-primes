#!/usr/bin/env python3
"""Finite / exact checks for LWW (arXiv:2610.20242v2): (4.121) on p. 47 and Prop. 4.5(i), (4.95), pp. 37-45.
Companion to notes/parity-attempts/2026-11-26-lww-p37-47-prop45.md.

Run: /usr/bin/python3 -I lww_p37_47_check.py     (fractions, sympy; no numpy)

(A) (4.120)-(4.121), exact rationals on toy prime sets P = primes in (y, y^2], rho in {1/4, 1/9} (sqrt rho rational):
    identity p V nu(p) - 1 = (E - 1)/((p+1) b'_p), E = sum_j eta'_j = 2(1-sqrt rho) + (2R-1)(1-rho);
    0 < b'_p <= 1 and |p V nu - 1| <= 2(2R+1)/(p+1) once p+1 >= 2(2R+1); |s - 1| <= 2(2R+1)/(V p_min);
    Delta <= 2/(V (p_min+1)).
    NEG: |p V nu - 1| <= 10/p uniformly in R; b'_p > 0 without p >> R; |s - 1| <= 1/p_min without R.
(B) pp. 36-41 matrix identities, exact (sympy rationals): g~(u,v,c/u) = g' = T g E, det g~ = 1, T^{-1} g~ z = (u tau,
    v tau - 2k/u), det(P_j,P_{j+1}) = -2 det(z_j,z_{j+1}), v_j/u_j - v/u = -2k/(u u_j), first coord of g'w = u tau(w),
    r_{g~z} independent of w, d/dr tau(w)/tau(z) = -2/tau(z)^2, the (4.106) derivatives.
    NEG: det(z,w) = -1 (derivative sign flips); wrong T^{-1} = [[1,0],[1,2]].
(C) pp. 33-34, 38: (4.81), (4.83) and the bijection S_l -> S: for odd coprime (u,v), z primitive with 2 !| z1
    <=> Q = gEz in C; p | q1 <=> [z]_p = l_p(g').                NEG: line u xi1 - c xi2 = 0 (factor 2 dropped).
(D) (4.112) Bonferroni for prod(1 - x_i), x_i in [0,1], exact; p. 44 H_p bounds 0 <= H_p <= 1[l in {[z_j]_p}],
    average <= (2R+1)/(p+1), exact (rho = 1/4).                 NEG: bound by e_{B+1} instead of e_B.
(E) p. 35 counts behind (4.88), exact enumeration: #{g0 in SL2(Z/2S): first column = (1,1) mod 2, line condition}
    = 2 prod p(p-1), |SL2(Z/2S)| = 6 prod p(p^2-1).  Plus a brute-force count of P = (u,v) in a toy box with line
    conditions at p = 3, 5 and c/u in I3 vs the main term |I1||I2||I3|/(3 zeta(2) prod (p+1)) (numeric, tol 6%).
    NEG: main term with 1/zeta(2); with 1/p in place of 1/(p+1).
(F) p. 41, #R: for fixed (j, a, theta, n, sign) the equation a tau(w)/tau(z) = n +- theta has <= 1 root r in [0,1)
    with tau(z) >= 1/16 (exact, linear in r); no root with |n| > X+1, X = 16|a|(|w1|+2|w2|) (the p. 41 bound).
(G) bookkeeping: log S << L^0.96 (p. 43), configuration count exp(O(L^0.71)) < exp(c L^0.75) (p. 45), box exponents
    (p. 40-42), (C R)^B / B! <= exp(-c L^{3/4}) (4.115) for large L.
    NEG: B = ceil(L^{1/2}) (no decay); box side x^{-c/2} (error #Q x^{-c} does not decay).
"""
from fractions import Fraction as Fr
from itertools import product as iproduct, combinations
from math import gcd, log, ceil, floor, pi, lgamma, factorial
import random
import time
import sympy as sp

rng = random.Random(20261126)
T0 = time.time()
RES = []


def report(name, n, nfail, expect_fail=False, extra=''):
    ok = (nfail > 0) if expect_fail else (nfail == 0)
    RES.append((name, expect_fail, ok))
    tag = 'NEG' if expect_fail else 'POS'
    print(f"[{tag}] {name}: cases={n} failures={nfail}{extra} -> {'as expected' if ok else 'UNEXPECTED'}")


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


PR = primes_upto(20000)

# ---------------------------------------------------------------- (A) (4.121)
n = nf = 0
neg1 = neg2 = neg3 = 0
nneg1 = nneg2 = nneg3 = 0
for y in (11, 23, 47, 101):
    P = [p for p in PR if y < p <= y * y]
    V = sum(Fr(1, p) for p in P)
    pmin = P[0]
    for (rho, srho) in ((Fr(1, 4), Fr(1, 2)), (Fr(1, 9), Fr(1, 3))):
        for R in (1, 2, 3, 5, 8, 13, 21, 50, 200):
            eta = [1 - srho] + [1 - rho] * (2 * R - 1) + [1 - srho]
            E = sum(eta)
            ok_all = True
            s = Fr(0)
            delta = Fr(0)
            large = all(p + 1 >= 2 * (2 * R + 1) for p in P)
            for p in P:
                b = 1 - E / (p + 1)
                if b <= 0:            # only possible when p is not >> R
                    ok_all = False
                    break
                nu = 1 / (V * (p + 1) * b)
                s += nu
                delta = max(delta, nu)
                n += 1
                if p * V * nu - 1 != (E - 1) / ((p + 1) * b):
                    nf += 1
                if not (0 < b <= 1):
                    nf += 1
                if p + 1 >= 2 * (2 * R + 1) and abs(p * V * nu - 1) > Fr(2 * (2 * R + 1), p + 1):
                    nf += 1
                nneg1 += 1
                if abs(p * V * nu - 1) > Fr(10, p):
                    neg1 += 1
            if large and ok_all:
                n += 2
                if abs(s - 1) > Fr(2 * (2 * R + 1), 1) / (V * pmin):
                    nf += 1
                if delta > 2 / (V * (pmin + 1)):
                    nf += 1
                nneg3 += 1
                if abs(s - 1) > Fr(1, pmin):
                    neg3 += 1
# b'_p > 0 needs p+1 > E ~ 2R(1-rho): small p, large R
for p in (3, 5, 7, 11, 13):
    for R in (1, 2, 5, 10, 20):
        nneg2 += 1
        E = 2 * (1 - Fr(1, 2)) + (2 * R - 1) * (1 - Fr(1, 4))
        if not (1 - E / (p + 1) > 0):
            neg2 += 1
report("(A) (4.121): identity, 0<b'<=1, |pVnu-1|<=2(2R+1)/(p+1), |s-1|<=2(2R+1)/(V pmin), Delta", n, nf)
report("(A) NEG |pVnu-1| <= 10/p uniformly in R", nneg1, neg1, True)
report("(A) NEG b'_p > 0 without p >> R (small p, large R)", nneg2, neg2, True)
report("(A) NEG |s-1| <= 1/p_min without the factor R", nneg3, neg3, True)

# ---------------------------------------------------------------- (B) matrix identities
u, v, r, h, k, h2, k2, w1, w2 = sp.symbols('u v r h k h2 k2 w1 w2')
T = sp.Matrix([[1, 0], [sp.Rational(1, 2), -sp.Rational(1, 2)]])
Tinv = sp.Matrix([[1, 0], [1, -2]])
gt = sp.Matrix([[u, -2 * u * r], [(u - v) / 2, r * (v - u) + 1 / u]])
tau = lambda z: z[0] - 2 * r * z[1]
n = nf = 0
checks = []
checks.append(sp.simplify(gt.det() - 1))
checks.append(sp.simplify(T * Tinv - sp.eye(2)).norm())
z = sp.Matrix([h, k]); zz = sp.Matrix([h2, k2])
Pz = Tinv * gt * z
checks.append(sp.simplify(Pz[0] - u * tau(z)))
checks.append(sp.simplify(Pz[1] - (v * tau(z) - 2 * k / u)))
Pzz = Tinv * gt * zz
detP = Pz[0] * Pzz[1] - Pz[1] * Pzz[0]
checks.append(sp.simplify(detP - (-2) * (h * k2 - k * h2)))
checks.append(sp.simplify(Pz[1] / Pz[0] - v / u - (-2 * k / (u * Pz[0]))))
# d/dr tau(w)/tau(z) = -2 det(z,w)/tau(z)^2
w = sp.Matrix([w1, w2])
d = sp.diff(tau(w) / tau(z), r)
checks.append(sp.simplify(d - (-2 * (h * w2 - k * w1) / tau(z) ** 2)))
# (4.106) derivatives
s_, D_ = sp.symbols('s D_')   # D_ stands for d0 Y M N
for c1 in (1, 16):
    checks.append(sp.simplify(sp.diff(c1 / tau(z), r) - 2 * c1 * k / tau(z) ** 2))
for c2 in (1, 2):
    fb = c2 / tau(z) + 2 * k / (D_ * s_ * tau(z))
    checks.append(sp.simplify(sp.diff(fb, s_) + 2 * k / (D_ * s_ ** 2 * tau(z))))
    checks.append(sp.simplify(sp.diff(fb, r) - (2 * c2 * k / tau(z) ** 2 + 4 * k ** 2 / (D_ * s_ * tau(z) ** 2))))
n += len(checks)
nf += sum(1 for c in checks if c != 0)
# integer instances: g~(u,v,c/u) = g' = T g E ; first coordinate of g'w = u tau(w); r_{g'z} independent of w
negB = nnegB = 0
for _ in range(300):
    uu = rng.randrange(1, 400) * 2 + 1
    vv = rng.randrange(1, 400) * 2 + 1
    if gcd(uu, vv) != 1:
        continue
    cc = (-pow(vv, -1, uu)) % uu
    dd = (1 + vv * cc) // uu
    assert uu * dd - vv * cc == 1
    g = sp.Matrix([[uu, cc], [vv, dd]])
    Em = sp.Matrix([[1, 0], [0, -2]])
    gp = T * g * Em
    gtn = gt.subs({u: uu, v: vv, r: sp.Rational(cc, uu)})
    n += 1
    if sp.simplify(gp - gtn).norm() != 0 or gp.det() != 1:
        nf += 1
    # pick primitive z with tau>0, two complements w, w + m z
    while True:
        z1, z2 = rng.randrange(-50, 50), rng.randrange(-50, 50)
        if gcd(z1, z2) == 1 and z1 - 2 * sp.Rational(cc, uu) * z2 > 0:
            break
    # find w with z1 w2 - z2 w1 = 1
    x, y_, gg = sp.gcdex(z1, -z2)  # x z1 + y (-z2) = 1  -> w2 = x, w1 = y
    W = sp.Matrix([y_, x])
    assert z1 * W[1] - z2 * W[0] == 1
    rr = sp.Rational(cc, uu)
    tz = z1 - 2 * rr * z2
    tw = W[0] - 2 * rr * W[1]
    n += 1
    gz = gp * sp.Matrix([z1, z2]); gw = gp * W
    if gz[0] != uu * tz or gw[0] != uu * tw:
        nf += 1
    m = rng.randrange(-5, 6)
    tw2 = (W[0] + m * z1) - 2 * rr * (W[1] + m * z2)
    n += 1
    if ((tw2 / tz) - (tw / tz)) != m:
        nf += 1
    # NEG: det(z,w) = -1 gives derivative +2/tau^2
    nnegB += 1
    Wm = -W
    dd_ = sp.diff((Wm[0] - 2 * r * Wm[1]) / (z1 - 2 * r * z2), r).subs(r, rr)
    if dd_ != -2 / tz ** 2:
        negB += 1
    nnegB += 1
    Tbad = sp.Matrix([[1, 0], [1, 2]])
    Pb = (Tbad * gtn * sp.Matrix([z1, z2]))
    if Pb[1] != vv * tz - sp.Rational(2 * z2, uu):
        negB += 1
report("(B) g~, P_j, det, telescoping, r_{g~z}, (4.106), (4.108) [symbolic+integer]", n, nf)
report("(B) NEG det(z,w) = -1 / wrong T^{-1}", nnegB, negB, True)

# ---------------------------------------------------------------- (C) (4.81), (4.83), bijection
n = nf = 0
nnegC = negC = 0
for _ in range(60):
    while True:
        uu = rng.randrange(1, 200) * 2 + 1
        vv = rng.randrange(1, 200) * 2 + 1
        if gcd(uu, vv) == 1:
            break
    cc = (-pow(vv, -1, uu)) % uu
    dd = (1 + vv * cc) // uu
    for z1 in range(-12, 13):
        for z2 in range(-12, 13):
            if (z1, z2) == (0, 0):
                continue
            q1 = uu * z1 - 2 * cc * z2
            q2 = vv * z1 - 2 * dd * z2
            lhs = gcd(z1, z2) == 1 and z1 % 2 == 1
            rhs = gcd(q1, q2) == 1 and q1 % 2 == 1 and q2 % 2 == 1
            n += 1
            if lhs != rhs:
                nf += 1
            if gcd(z1, z2) != 1:
                continue
            for p in (3, 5, 7, 11, 13):
                # [z]_p = l_p(g'): z satisfies u xi1 - 2c xi2 = 0 mod p
                n += 1
                if ((q1 % p == 0) != ((uu * z1 - 2 * cc * z2) % p == 0)):
                    nf += 1
                # also via projective equality: [z]_p == [(2c, u)]_p
                a1, a2 = z1 % p, z2 % p
                b1, b2 = (2 * cc) % p, uu % p
                same = (a1 * b2 - a2 * b1) % p == 0
                n += 1
                if (q1 % p == 0) != same:
                    nf += 1
                nnegC += 1
                if (q1 % p == 0) != ((uu * z1 - cc * z2) % p == 0):
                    negC += 1
report("(C) (4.81), (4.83), primitive & 2!|z1 <=> Q in C", n, nf)
report("(C) NEG line u xi1 - c xi2 = 0 (factor 2 dropped)", nnegC, negC, True)

# ---------------------------------------------------------------- (D) Bonferroni + H_p
def esym(xs, kk):
    e = [Fr(0)] * (kk + 1)
    e[0] = Fr(1)
    for x_ in xs:
        for j in range(kk, 0, -1):
            e[j] += e[j - 1] * x_
    return e


n = nf = 0
nnegD = negD = 0
for _ in range(400):
    m = rng.randrange(1, 10)
    xs = [Fr(rng.randrange(0, 21), 20) for _ in range(m)]
    prod_ = Fr(1)
    for x_ in xs:
        prod_ *= 1 - x_
    e = esym(xs, m + 1)
    for B in range(0, m + 1):
        partial = sum((-1) ** kk * e[kk] for kk in range(B))
        n += 1
        if abs(prod_ - partial) > e[B]:
            nf += 1
        nnegD += 1
        if abs(prod_ - partial) > e[B + 1]:
            negD += 1
# H_p(l) = 1 - rho^{(1/2) sum_j (1[l=[z_j]] + 1[l=[z_{j+1}]])}, rho = 1/4 -> sqrt rho = 1/2
for _ in range(300):
    p = rng.choice([3, 5, 7, 11, 13, 17])
    R = rng.randrange(1, 6)
    lines = [(1, x_) for x_ in range(p)] + [(0, 1)]
    zl = [rng.randrange(p + 1) for _ in range(2 * R + 1)]   # [z_j]_p as line indices
    tot = Fr(0)
    for li in range(p + 1):
        cnt = sum((1 if li == zl[j] else 0) + (1 if li == zl[j + 1] else 0) for j in range(2 * R))
        H = 1 - Fr(1, 2) ** cnt
        n += 1
        if not (0 <= H <= (1 if li in zl else 0)):
            nf += 1
        tot += H
    n += 1
    if tot / (p + 1) > Fr(2 * R + 1, p + 1):
        nf += 1
report("(D) Bonferroni |prod(1-x)-sum_{k<B}| <= e_B ; H_p bounds (p. 44)", n, nf)
report("(D) NEG bound by e_{B+1}", nnegD, negD, True)

# ---------------------------------------------------------------- (E) (4.86)-(4.88) counts
n = nf = 0
for S in (3, 5, 7, 15, 21):
    Ps = [p for p in (3, 5, 7) if S % p == 0]
    M = 2 * S
    size = 0
    good = 0
    lines = {p: (1, 2) for p in Ps}  # fixed line l_p = span(xi, eta) = (1, 2)
    for a_ in range(M):
        for b_ in range(M):
            for c_ in range(M):
                for d_ in range(M):
                    if (a_ * d_ - b_ * c_) % M != 1:
                        continue
                    size += 1
                    # g0 = [[u0, c0],[v0, d0']] : first column (a_, c_) = (u0, v0); c0 = b_
                    if a_ % 2 == 1 and c_ % 2 == 1:
                        if all((a_ * lines[p][0] - 2 * b_ * lines[p][1]) % p == 0 for p in Ps):
                            good += 1
    pr1 = 1; pr2 = 1
    for p in Ps:
        pr1 *= p * (p - 1); pr2 *= p * (p * p - 1)
    n += 2
    if good != 2 * pr1:
        nf += 1
    if size != 6 * pr2:
        nf += 1
report("(E) #g0 = 2 prod p(p-1), |SL2(Z/2S)| = 6 prod p(p^2-1) (p. 35)", n, nf)

# brute-force count (numeric): u in [U,16U], v in [N,2N] odd coprime, c/u in I3, l_p(g') = l_p for p = 3, 5
U, N = 60, 700
I3 = (Fr(1, 5), Fr(7, 10))
target = {3: (1, 1), 5: (2, 1)}         # fixed lines (xi, eta) as projective points
cnt_lines = {}
cnt = 0
for uu in range(U, 16 * U + 1):
    if uu % 2 == 0:
        continue
    for vv in range(N, 2 * N + 1):
        if vv % 2 == 0 or gcd(uu, vv) != 1:
            continue
        cc = (-pow(vv, -1, uu)) % uu
        if not (I3[0] <= Fr(cc, uu) < I3[1]):
            continue
        ok = True
        for p, (xi, et) in target.items():
            # l_p(g') = {u xi1 - 2c xi2 = 0}; equals span(xi, et) iff u xi - 2c et = 0 mod p
            if (uu * xi - 2 * cc * et) % p != 0:
                ok = False
                break
        if ok:
            cnt += 1
area = Fr(15) * 1 * (I3[1] - I3[0])
main = float(area) / (3 * (pi ** 2 / 6) * 4 * 6) * U * N
rel = abs(cnt / main - 1)
report("(E) toy count vs |I1||I2||I3|/(3 zeta(2) prod(p+1)) within 6%", 1, int(rel > 0.06),
       extra=f" [count={cnt}, main={main:.1f}, rel.err={rel:.4f}]")
main_neg1 = float(area) / ((pi ** 2 / 6) * 4 * 6) * U * N
main_neg2 = float(area) / (3 * (pi ** 2 / 6) * 3 * 5) * U * N
report("(E) NEG main term with 1/zeta(2)", 1, int(abs(cnt / main_neg1 - 1) > 0.06), True,
       extra=f" [rel.err={abs(cnt / main_neg1 - 1):.3f}]")
report("(E) NEG main term with 1/p for 1/(p+1)", 1, int(abs(cnt / main_neg2 - 1) > 0.06), True,
       extra=f" [rel.err={abs(cnt / main_neg2 - 1):.3f}]")

# ---------------------------------------------------------------- (F) #R per (a, theta)
n = nf = 0
for _ in range(120):
    while True:
        z1, z2 = rng.randrange(-12, 13), rng.randrange(-12, 13)
        if gcd(z1, z2) == 1:
            break
    x, y_, _g = sp.gcdex(z1, -z2)
    W = (int(y_), int(x))
    assert z1 * W[1] - z2 * W[0] == 1
    a = rng.choice([i for i in range(-12, 13) if i != 0])
    th = Fr(rng.randrange(1, 40), 100)
    def tauz(rr): return z1 - 2 * rr * z2
    # LWW p. 41: |tau(w)/tau(z)| <= 16(|w1| + 2|w2|) when tau(z) >= 1/16, r in [0,1)
    X = 16 * abs(a) * (abs(W[0]) + 2 * abs(W[1]))
    total = 0
    outside = 0
    for nn in range(-X - 60, X + 61):
        for sgn in (1, -1):
            tgt = nn + sgn * th
            # a (w1 - 2 r w2) = tgt (z1 - 2 r z2)  ->  r (2 tgt z2 - 2 a w2) = tgt z1 - a w1  (linear: <= 1 root)
            coef = 2 * tgt * z2 - 2 * a * W[1]
            rhs = tgt * z1 - a * W[0]
            if coef == 0:
                if rhs == 0:
                    nf += 1            # a continuum of roots would contradict det(z,w) = 1
                continue
            rr = rhs / coef
            if 0 <= rr < 1 and tauz(rr) >= Fr(1, 16):
                total += 1
                if abs(nn) > X + 1:
                    outside += 1
    n += 1
    if outside > 0 or total > 2 * (2 * X + 3):
        nf += 1
report("(F) #R per (a,theta): <= 1 root per (n, sign), none with |n| > 16|a|(|w1|+2|w2|)+1", n, nf)

# ---------------------------------------------------------------- (G) bookkeeping
n = nf = 0
nnegG = negG = 0
K = 3
for Lexp in (6, 8, 10, 12, 16, 20, 30):
    L = 10.0 ** Lexp
    R = ceil(L ** 0.5 / 2); J = floor(L ** 0.01); B = ceil(L ** 0.75)
    logS = ((2 * R + 1) * K * (J + 1) + B) * 2 * L ** 0.2
    n += 1
    if logS > 10 * K * L ** 0.96:
        nf += 1
    # configurations: (R d0 Y)^{2(2R+1)} * |P|^{K(J+1)(2R+1)} * ((J+1)!)^{4KR}, logs
    logRd0Y = log(R) + 2 * K * (J + 1) * L ** 0.2
    logconf = 2 * (2 * R + 1) * 2 * logRd0Y + K * (J + 1) * (2 * R + 1) * 2 * L ** 0.2 + 4 * K * R * lgamma(J + 2)
    n += 1
    if logconf > 100 * K * K * L ** 0.71 * 1.0:
        nf += 1
    # (4.115): log((C R)^B / B!) <= -c L^{3/4}, C = 3K (2R+1 <= 3R, sum V_i <= K)
    C = 3 * K
    val = B * log(C * R) - lgamma(B + 1)
    if Lexp >= 8:
        n += 1
        if val > -0.1 * L ** 0.75:
            nf += 1
    # NEG: B = ceil(L^{1/2})
    Bn = ceil(L ** 0.5)
    valn = Bn * log(C * R) - lgamma(Bn + 1)
    if Lexp >= 8:
        nnegG += 1
        if valn > -0.1 * L ** 0.75:
            negG += 1
# box exponents (in units of c_delta): side x^{-1/8}: #Q = x^{3/8}; errors
q = sp.Rational(1, 8)
sideexp = -q
nQ = -3 * sideexp
err_in = nQ - 1                 # #Q x^{-c}  -> -5/8
qdel = sp.Rational(1, 4)        # #Q_partial = x^{1/4 + o(1)} (two of three sides)
volsum = qdel + 3 * sideexp      # -> -1/8
n += 3
nf += int(err_in != -sp.Rational(5, 8)) + int(volsum != -sp.Rational(1, 8)) + int(not (err_in < 0 and volsum < 0))
# NEG: side x^{-1/2}
nQb = 3 * sp.Rational(1, 2)
nnegG += 1
if nQb - 1 >= 0:
    negG += 1
report("(G) bookkeeping: log S, config count, (4.115), box exponents", n, nf)
report("(G) NEG B = L^{1/2} (no exp(-cL^{3/4})); box side x^{-c/2}", nnegG, negG, True)

pos = sum(1 for x_ in RES if not x_[1]); neg = sum(1 for x_ in RES if x_[1])
bad = sum(1 for x_ in RES if not x_[2])
print(f"\nSUMMARY: {pos} positive checks, {neg} negative controls, unexpected outcomes: {bad}")
print(f"runtime {time.time() - T0:.1f} s")
