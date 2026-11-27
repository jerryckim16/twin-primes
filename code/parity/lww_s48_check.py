#!/usr/bin/python3
"""Toy checks for LWW (arXiv:2610.20242v2), Section 4.8: the second sum of (4.52), (4.148)-(4.157), pp. 58-61,
with the pieces of Prop. 4.5(ii) / (4.96) (pp. 37, 45-46) and (4.28)-(4.31) (pp. 21-22) that are finite identities.

Run: /usr/bin/python3 -I code/parity/lww_s48_check.py
Route card: notes/parity-attempts/2026-11-27-lww-s48-second-sum.md

What is checked (toy parameters; finite identities and inequalities only, nothing asymptotic):
 (A) the operator algebra of p. 58: <f,Kf> = <f,T f> for K = S T S and f independent of the tuple order;
     (4.149); <(1-G)f,Kf> = <(1-G)f,Tf>; <Gf,K(1-G)f> = <Gf,T(1-G)f>  (G permutation-invariant).   complex floats
 (B) (4.152)-(4.153) on a brute-forced line space (all l in prod_q P^1(F_q)):
       prod_q (q+1)^{-1} sum_l [restrictions] rho^{(w_l(z0)+w_l(z')-2K(J+1))/2}
         <= 1_{D|det(z0,z')} prod_{p|Dab} (p+1)^{-1},  with equality at rho = 1;
     and w_l(z) >= K(J+1) under the restrictions (p. 59).                                exact Fractions / floats
 (C) p. 60 prime-tuple sum: sum over ordered distinct (p_{i,1..J+1}, p'_i) of prod_{q|Dab}(q+1)^{-1}
       <= prod_i (sum_{q in P_i} 1/(q+1))^{J+2} <= prod_i V_i^{J+2}.                            exact Fractions
 (D) the change of variables behind (4.150): g' of (4.80), z = g'^{-1} T Q integral, primitive, odd z_1;
     q_1 = u z_1 - 2c z_2 (so p | q_1 <=> [z]_p = l_p(g')); det(z0, z) = det(TP,TQ) = -det(P,Q)/2;
     r_{TP} = r_{g' z0} = -2 r_P (mod 1); g~(u, v, c/u) = g'.                                      exact integers
 (E) (4.124)/(4.155): #{h : g~ z' in Omega' (first coordinate)} <= #{h : 1/16 <= h + rDt <= 16} <= 16.     floats
 (F) M_1, (4.94), (4.76): int_{M_1} e(phi w) is real, |.| <= meas M_1, and can be negative (so the |.| in the
     printed (4.94) matters); (4.76) int_{M_-2} e(theta(t-2c)) = int_{M_1} e(phi(-t/2+c)) for even t.   floats
 (G) measures on T: (4.28) meas{r : ||m r|| <= eps} = 2 eps; r -> -2r preserves Lebesgue measure (p. 60);
     the Moebius map r -> r_{g~ z1} does NOT (why the second term of (4.149) is re-centred at (Q,p')).
 (H) Prop. 4.5(ii) p. 46: rho^{(w_l(z0)+w_l(z1))/2} = prod_p (1 - H_{1,p}(l_p)); avg_l H_{1,p} <= 2/(p+1);
     Bonferroni |prod(1-x) - sum_{k<B}(-1)^k e_k(x)| <= e_B(x) for x in [0,1]^n.        exact Fractions / floats
Negative controls are marked NEG and must FAIL.
"""
import math, random, time, itertools, cmath
from fractions import Fraction as Fr

T0 = time.time()
random.seed(20261127)
RESULTS = []


def report(name, kind, failures, total, detail=""):
    ok = (failures == 0) if kind == 'POS' else (failures > 0)
    RESULTS.append((name, kind, ok))
    tag = "ok" if ok else "UNEXPECTED"
    print(f"[{kind}] {name}: {failures}/{total} failures -> {tag} {detail}")


def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def line_idx(z, p):
    """index of [z]_p in P^1(F_p): y/x mod p in 0..p-1 if x != 0 mod p, else p.  z must be nonzero mod p."""
    x, y = z[0] % p, z[1] % p
    if x:
        return (y * pow(x, -1, p)) % p
    assert y
    return p


# ---------------------------------------------------------------------------------------------------------------
print("== (A) operator algebra of p. 58: K = S T S, (4.149), and the S-removals")


def opA(nP=4, base=('x', 'y', 'z'), J1=2, G_order_dependent=False, f_order_dependent=False):
    tuples = list(itertools.permutations(base, J1))           # ordered tuples of distinct entries
    states = [(P, tp) for P in range(nP) for tp in tuples]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    sigma = 0.37                                               # sigma(P,p) constant (as in (4.19))
    T = [[complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
    cP = [complex(random.gauss(0, 1), random.gauss(0, 1)) for _ in range(nP)]
    f = [cP[P] + (0.3 * (tp[0] == base[0]) if f_order_dependent else 0) for (P, tp) in states]
    goodset = {(P, frozenset(tp)): random.random() < 0.5 for P in range(nP) for tp in tuples}
    if G_order_dependent:
        good = [((P + (tp[0] == base[0])) % 2 == 0) for (P, tp) in states]
    else:
        good = [goodset[(P, frozenset(tp))] for (P, tp) in states]

    def S(g):
        out = []
        for (P, tp) in states:
            orb = [idx[(P, q)] for q in itertools.permutations(tp)]
            out.append(sum(g[j] for j in orb) / len(orb))
        return out

    def app(M, g):
        return [sum(M[i][j] * g[j] for j in range(n)) for i in range(n)]

    def ip(a, b):
        return sum(a[i].conjugate() * b[i] for i in range(n)) * sigma

    def Gm(g):
        return [g[i] if good[i] else 0 for i in range(n)]

    def oneminusG(g):
        return [0 if good[i] else g[i] for i in range(n)]

    def Kop(g):
        return S(app(T, S(g)))

    Kf = Kop(f)
    A_f = Gm(Kop(Gm(f)))
    lhs149 = ip(f, Kf) - ip(f, A_f)
    rhs149 = ip(oneminusG(f), Kf) + ip(Gm(f), Kop(oneminusG(f)))
    e0 = abs(ip(f, Kf) - ip(f, app(T, f)))
    e1 = abs(lhs149 - rhs149)
    e2 = abs(ip(oneminusG(f), Kf) - ip(oneminusG(f), app(T, f)))
    e3 = abs(ip(Gm(f), Kop(oneminusG(f))) - ip(Gm(f), app(T, oneminusG(f))))
    return e0, e1, e2, e3


fails = [0, 0, 0, 0]; N = 30
for _ in range(N):
    es = opA()
    for i in range(4):
        fails[i] += es[i] > 1e-9
report("A <f, STS f> = <f, T f> (f independent of tuple order)", 'POS', fails[0], N)
report("A (4.149) <f,Kf> - <f,GKGf> = <(1-G)f,Kf> + <Gf,K(1-G)f>", 'POS', fails[1], N)
report("A <(1-G)f, Kf> = <(1-G)f, T f> (p. 58)", 'POS', fails[2], N)
report("A <Gf, K(1-G)f> = <Gf, T(1-G)f> (second term)", 'POS', fails[3], N)
fn = sum(opA(G_order_dependent=True)[2] > 1e-9 for _ in range(N))
report("NEG A <(1-G)f,Kf> = <(1-G)f,Tf> with G depending on the tuple ORDER", 'NEG', fn, N)
fn = sum(opA(f_order_dependent=True)[0] > 1e-9 for _ in range(N))
report("NEG A <f,STSf> = <f,Tf> with f depending on the tuple order", 'NEG', fn, N)

# ---------------------------------------------------------------------------------------------------------------
print("== (B) (4.152)-(4.153): brute force over all line tuples l in prod_q P^1(F_q)")
PB = [3, 5, 7, 11]             # toy prime set, K = 1
KB, JB = 1, 1
lines_space = list(itertools.product(*[range(q + 1) for q in PB]))
qpos = {q: i for i, q in enumerate(PB)}
NORM = 1
for q in PB:
    NORM *= (q + 1)
z0 = (1, 0)
zlist = []
while len(zlist) < 12:
    h = random.choice([x for x in range(-40, 41) if x % 2])
    k = random.randint(-60, 60)
    if math.gcd(h, k) == 1 and all((h % q, k % q) != (0, 0) for q in PB) and (h, k) not in zlist:
        zlist.append((h, k))
# make sure some z' have D | det for D in PB
for D in PB:
    zlist.append((2 * D + 1, D * random.choice([1, -2, 3])))
zlist = [z for z in zlist if math.gcd(*z) == 1 and z[0] % 2 and all((z[0] % q, z[1] % q) != (0, 0) for q in PB)]


def lhs_B(zp, pt, pprime, rho, drop_indicator=False):
    """prod (q+1)^{-1} sum_l 1[(z0,p) in S_l, (z',p') in S_l] rho^{(w_l(z0)+w_l(z')-2K(J+1))/2}
    pt = (p1, p2) ordered distinct (D = p1, b = p2), pprime = p'_1 (a = p'_1).  K = J = 1."""
    Dp, bp, ap = pt[0], pt[1], pprime
    i0 = {q: line_idx(z0, q) for q in PB}
    i1 = {q: line_idx(zp, q) for q in PB}
    tot = 0.0; omin = 10 ** 9; cnt = 0
    for l in lines_space:
        lp = {q: l[qpos[q]] for q in PB}
        if lp[Dp] != i0[Dp] or lp[bp] != i0[bp]:
            continue
        if not drop_indicator and lp[Dp] != i1[Dp]:
            continue
        if lp[ap] != i1[ap]:
            continue
        w0 = sum(lp[q] == i0[q] for q in PB)
        w1 = sum(lp[q] == i1[q] for q in PB)
        omin = min(omin, w0, w1)
        tot += rho ** ((w0 + w1 - 2 * KB * (JB + 1)) / 2)
        cnt += 1
    return tot / NORM, cnt, omin


def rhs_B(zp, pt, pprime):
    D = pt[0]
    det = z0[0] * zp[1] - z0[1] * zp[0]
    val = Fr(1 if det % D == 0 else 0)
    for q in (pt[0], pt[1], pprime):
        val /= (q + 1)
    return val


f_eq = f_le = f_om = 0; tot = 0; f_neg_rho = 0; f_neg_ind = 0; nDdiv = 0
for zp in zlist:
    for pt in itertools.permutations(PB, 2):
        for pp in [q for q in PB if q not in pt]:
            tot += 1
            r = rhs_B(zp, pt, pp)
            nDdiv += (r != 0)
            v1, cnt, om = lhs_B(zp, pt, pp, 1.0)
            # rho = 1: exact count identity
            if Fr(cnt, NORM) != r:
                f_eq += 1
            vh, _, _ = lhs_B(zp, pt, pp, 0.5)
            if vh > float(r) + 1e-15:
                f_le += 1
            if cnt and om < KB * (JB + 1):
                f_om += 1
            v2, _, _ = lhs_B(zp, pt, pp, 2.0)
            if v2 > float(r) + 1e-15:
                f_neg_rho += 1
            _, cntd, _ = lhs_B(zp, pt, pp, 1.0, drop_indicator=True)
            if Fr(cntd, NORM) != r:
                f_neg_ind += 1
print(f"   {len(zlist)} vectors z', {tot} (z',p,p') triples, {nDdiv} with D | det(z0,z'); |line space| = {NORM}")
report("B (4.153) at rho=1: (prod (q+1))^{-1} #{l : restrictions} = 1_{D|det} prod_{p|Dab} 1/(p+1)", 'POS', f_eq, tot)
report("B (4.152)+(4.153) at rho=1/2: rho-weighted line average <= 1_{D|det} prod_{p|Dab} 1/(p+1)", 'POS', f_le, tot)
report("B w_l(z0), w_l(z') >= K(J+1) under the restrictions (p. 59)", 'POS', f_om, tot)
report("NEG B same inequality at rho = 2 (0 < rho < 1 is used)", 'NEG', f_neg_rho, tot)
report("NEG B rho=1 identity with the constraint l_p = [z']_p at p | D dropped (no 1_{D|det})", 'NEG', f_neg_ind, tot)

# ---------------------------------------------------------------------------------------------------------------
print("== (C) p. 60 prime-tuple weight sum")
pr = primes_upto(200)
fC = fCn = nC = 0
for (lo1, hi1, lo2, hi2) in [(10, 30, 30, 60), (12, 40, 40, 80), (60, 110, 110, 200)]:
    P1 = [p for p in pr if lo1 < p <= hi1]; P2 = [p for p in pr if lo2 < p <= hi2]
    for J in (1, 2):
        sums = []
        for Pi in (P1, P2):
            s = Fr(0)
            for tup in itertools.permutations(Pi, J + 2):        # (p_{i,1..J+1}, p'_i), all distinct
                w = Fr(1)
                for q in tup:
                    w /= (q + 1)
                s += w
            sums.append((s, sum(Fr(1, q + 1) for q in Pi), sum(Fr(1, q) for q in Pi), Pi))
        lhs = sums[0][0] * sums[1][0]          # the weight factorises over i
        mid = sums[0][1] ** (J + 2) * sums[1][1] ** (J + 2)
        top = sums[0][2] ** (J + 2) * sums[1][2] ** (J + 2)
        nC += 1
        if not (lhs <= mid <= top):
            fC += 1
        if lhs <= mid / math.factorial(J + 2) ** 2:
            pass
        else:
            fCn += 1
        print(f"   P1={len(P1)} P2={len(P2)} J={J}: sum={float(lhs):.4e} <= prod(sum 1/(q+1))^(J+2)={float(mid):.4e}"
              f" <= prod V^(J+2)={float(top):.4e}")
report("C sum_{tuples} prod_{q|Dab}(q+1)^{-1} <= prod(sum 1/(q+1))^{J+2} <= prod V_i^{J+2}", 'POS', fC, nC)
report("NEG C same with an extra 1/(J+2)! per i (unordered-tuple misreading)", 'NEG', fCn, nC)

# ---------------------------------------------------------------------------------------------------------------
print("== (D) change of variables behind (4.150): g' of (4.80), z = g'^{-1} T Q, r_{TP} = -2 r_P")
fD = [0] * 6; nD = 0; fDn = 0
oddpr = [p for p in primes_upto(200) if p > 2]
for _ in range(4000):
    while True:
        u = random.randrange(3, 10 ** 6, 2); v = random.randrange(1, 10 ** 6, 2)
        if math.gcd(u, v) == 1:
            break
    c = (-pow(v, -1, u)) % u
    d = (1 + v * c) // u
    assert u * d - v * c == 1 and 0 <= c < u
    g = ((u, -2 * c), ((u - v) // 2, d - c))           # (4.80)
    detg = g[0][0] * g[1][1] - g[0][1] * g[1][0]
    gi = ((g[1][1], -g[0][1]), (-g[1][0], g[0][0]))      # inverse (det 1)
    while True:
        q1 = random.randrange(1, 10 ** 6, 2); q2 = random.randrange(1, 10 ** 6, 2)
        if math.gcd(q1, q2) == 1:
            break
    TQ = (q1, (q1 - q2) // 2)
    z = (gi[0][0] * TQ[0] + gi[0][1] * TQ[1], gi[1][0] * TQ[0] + gi[1][1] * TQ[1])
    nD += 1
    if detg != 1:
        fD[0] += 1
    if not (math.gcd(*z) == 1 and z[0] % 2 == 1):
        fD[1] += 1
    if q1 != u * z[0] - 2 * c * z[1]:
        fD[2] += 1
    TP = (u, (u - v) // 2)
    detPQ = u * q2 - v * q1
    if not (z[1] == TP[0] * TQ[1] - TP[1] * TQ[0] == -detPQ // 2 and detPQ % 2 == 0):
        fD[3] += 1
    # r_{TP}: complement (c', d') of TP with u d' - ((u-v)/2) c' = 1
    m = (u - v) // 2
    cp = (-pow(m, -1, u)) % u if math.gcd(m, u) == 1 else None
    if cp is None or (cp + 2 * c) % u != 0:
        fD[4] += 1
    if cp is not None and (cp - 2 * c) % u != 0:
        fDn += 1
    # g~(u, v, r) of (4.89) at r = c/u equals g'
    r = Fr(c, u)
    gt = ((Fr(u), -2 * u * r), (Fr(u - v, 2), r * (v - u) + Fr(1, u)))
    if gt != tuple(tuple(Fr(x) for x in row) for row in g):
        fD[5] += 1
report("D det g' = 1", 'POS', fD[0], nD)
report("D z = g'^{-1} T Q is primitive with odd first coordinate (Q in C)", 'POS', fD[1], nD)
report("D q_1 = u z_1 - 2c z_2 (so p | q_1 <=> [z]_p = l_p(g'), (4.83))", 'POS', fD[2], nD)
report("D det(z0, z) = det(TP, TQ) = -det(P,Q)/2, det(P,Q) even", 'POS', fD[3], nD)
report("D r_{TP} = r_{g' z0} = -2 r_P (mod 1)", 'POS', fD[4], nD)
report("D g~(u, v, c/u) of (4.89) = g' of (4.80)", 'POS', fD[5], nD)
report("NEG D r_{TP} = +2 r_P (mod 1)", 'NEG', fDn, nD)
# example: r_{g~ z1} as a function of r is a Moebius map, not -2r + const
z1 = (16, 1); w = (-1, 0)
assert z1[0] * w[1] - z1[1] * w[0] == 1
vals = [((w[0] - 2 * rr * w[1]) / (z1[0] - 2 * rr * z1[1])) % 1 for rr in (0.0, 0.25, 0.5, 0.75, 0.999)]
print("   example z1=(16,1): r_{g~z1}(r) at r=0,.25,.5,.75,.999 =", ", ".join(f"{x:.5f}" for x in vals))

# ---------------------------------------------------------------------------------------------------------------
print("== (E) (4.124)/(4.155): number of h for fixed t")
fE = 0; nE = 0; mx = 0; mxE = 0
for _ in range(20000):
    U = random.choice([10 ** 3, 10 ** 4, 10 ** 5])           # U = d0 Y M
    s = random.uniform(1, 16); u = U * s
    r = random.random()
    D = random.choice([3, 5, 15, 105, 1155, 7 * 11 * 13 * 17])
    t = 2 * random.randint(-500, 500)
    k = -D * t // 2
    # first coordinate of g~ z' is u * tau(z') = u (h - 2 r k)
    lo = math.floor(U / u + 2 * r * k) - 2; hi = math.ceil(16 * U / u + 2 * r * k) + 2
    Hs = [h for h in range(lo, hi + 1) if U <= u * (h - 2 * r * k) <= 16 * U]
    big = [h for h in range(math.floor(1 / 16 - r * D * t) - 2, math.ceil(16 - r * D * t) + 3)
           if 1 / 16 <= h + r * D * t <= 16]
    nE += 1
    mx = max(mx, len(Hs)); mxE = max(mxE, len(big))
    if not (set(Hs) <= set(big) and len(big) <= 16):
        fE += 1
report("E {h : g~z' in Omega' (1st coord)} subset {h : 1/16 <= h + rDt <= 16}, # <= 16", 'POS', fE, nE,
       f"(max seen {mx}, {mxE})")
report("NEG E (tightness, not a misreading) same with '<= 15'", 'NEG', sum(1 for _ in [0] if mxE > 15), 1)

# ---------------------------------------------------------------------------------------------------------------
print("== (F) M_1, (4.94) and (4.76)")


def M1_intervals(Q, Y):
    dl = 2 * Q / Y
    iv = []
    for k in range(1, Q + 1):
        for j in range(k):
            if math.gcd(j, k) == 1:
                a, b = j / k - dl, j / k + dl
                for (x, y) in ((a, b), (a - 1, b - 1), (a + 1, b + 1)):
                    x2, y2 = max(x, 0.0), min(y, 1.0)
                    if x2 < y2:
                        iv.append((x2, y2))
    iv.sort(); out = []
    for (x, y) in iv:
        if out and x <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], y))
        else:
            out.append((x, y))
    return out


def int_e(ivs, w):
    if w == 0:
        return complex(sum(y - x for (x, y) in ivs))
    return sum((cmath.exp(2j * math.pi * w * y) - cmath.exp(2j * math.pi * w * x)) / (2j * math.pi * w)
               for (x, y) in ivs)


def preimage_minus2(ivs):
    """{theta in [0,1) : -2 theta mod 1 in union ivs}"""
    out = []
    for (x, y) in ivs:
        for j in (0, 1, 2):
            a, b = (j - y) / 2, (j - x) / 2
            a2, b2 = max(a, 0.0), min(b, 1.0)
            if a2 < b2:
                out.append((a2, b2))
    return out


fF = [0, 0, 0]; nF = 0; negs = 0; fFn = 0; nFn = 0; minW = 0
for (Q, Y) in [(3, 200), (5, 1000), (4, 97), (6, 5000)]:
    ivs = M1_intervals(Q, Y)
    meas = sum(y - x for (x, y) in ivs)
    ivs2 = preimage_minus2(ivs)
    meas2 = sum(y - x for (x, y) in ivs2)
    for w in range(-60, 61):
        I = int_e(ivs, w); nF += 1
        if abs(I.imag) > 1e-12:
            fF[0] += 1
        if abs(I) > meas + 1e-12 or abs(abs(int_e(ivs, -w)) - abs(I)) > 1e-12:
            fF[1] += 1
        if I.real < -1e-9:
            negs += 1; minW = min(minW, I.real)
    for _ in range(60):
        t = 2 * random.randint(-3 * Y, 3 * Y); cc = random.randint(-Y, Y)
        lhs = int_e(ivs2, t - 2 * cc); rhs = int_e(ivs, -t // 2 + cc)
        if abs(lhs - rhs) > 1e-10:
            fF[2] += 1
        to = t + 1; nFn += 1
        lhs = int_e(ivs2, to - 2 * cc); rhs = int_e(ivs, (-to) / 2 + cc)
        if abs(lhs - rhs) > 1e-10:
            fFn += 1
    print(f"   L^A0={Q}, Y={Y}: meas M_1={meas:.5f}, meas M_-2={meas2:.5f}")
report("F int_{M_1} e(phi w) dphi is real (M_1 = -M_1)", 'POS', fF[0], nF)
report("F |int_{M_1} e(phi w)| <= meas M_1 and |W(-w)| = |W(w)| (edge reversal)", 'POS', fF[1], nF)
report("F (4.76) int_{M_-2} e(theta(t-2c)) = int_{M_1} e(phi(-t/2+c)) for even t", 'POS', fF[2], 240)
print(f"   int_{{M_1}} e(phi w) < 0 for {negs}/{nF} values of w (min {minW:.4f}): the |.| printed in (4.94)"
      " (p. 37, visible only in the page image) is what makes W >= 0 on p. 46")
report("NEG F (4.76) with t odd (t in 2Z is used)", 'NEG', fFn, nFn)

# ---------------------------------------------------------------------------------------------------------------
print("== (G) measures on T: (4.28), r -> -2r (p. 60), and the Moebius map r -> r_{g~ z1}")


def meas_union(ivs):
    ivs = sorted(ivs); tot = Fr(0); cur = None
    for (x, y) in ivs:
        if cur is None or x > cur[1]:
            if cur is not None:
                tot += cur[1] - cur[0]
            cur = [x, y]
        else:
            cur[1] = max(cur[1], y)
    if cur is not None:
        tot += cur[1] - cur[0]
    return tot


def clip01(a, b):
    out = []
    for j in range(math.floor(a) - 1, math.ceil(b) + 2):
        x, y = max(a - j, Fr(0)), min(b - j, Fr(1))
        if x < y:
            out.append((x, y))
    return out


fG = [0, 0]; nG = 0
for _ in range(300):
    m = random.choice([1, -1]) * random.randint(1, 400)
    eps = Fr(random.randint(1, 999), 2000 * random.randint(1, 50))
    ivs = []
    for n in range(-abs(m) - 2, abs(m) + 3):
        a, b = sorted(((n - eps) / m, (n + eps) / m))
        ivs += clip01(a, b)
    nG += 1
    if meas_union(ivs) != 2 * eps:
        fG[0] += 1
    # random finite union F of intervals in [0,1) and its preimage under r -> -2r
    F = []
    for _ in range(random.randint(1, 5)):
        a = Fr(random.randint(0, 999), 1000); b = a + Fr(random.randint(1, 100), 1000)
        F += clip01(a, b)
    pre = []
    for (x, y) in F:
        for j in (0, 1, 2):
            pre += clip01((j - y) / 2, (j - x) / 2)
    if meas_union(pre) != meas_union(F):
        fG[1] += 1
report("G (4.28) meas{r in T : ||m r|| <= eps} = 2 eps (exact)", 'POS', fG[0], nG)
report("G meas{r : -2r mod 1 in F} = meas F for finite unions F (exact)", 'POS', fG[1], nG)
# NEG: the bad set at z1 is the preimage under the Moebius map r -> (w1 - 2 r w2)/(h - 2 r k) mod 1
z1 = (16, 1); w = (-1, 0)
phi = lambda rr: ((w[0] - 2 * rr * w[1]) / (z1[0] - 2 * rr * z1[1])) % 1
Fset = (1 - 1 / 14, 1 - 1 / 16)                      # an interval of measure ~0.0089
Ngrid = 200000
pre = sum(1 for i in range(Ngrid) if Fset[0] <= phi((i + 0.5) / Ngrid) <= Fset[1]) / Ngrid
measF = Fset[1] - Fset[0]
print(f"   z1=(16,1): meas F = {measF:.5f}, meas{{r : r_(g~z1)(r) in F}} = {pre:.5f}")
report("NEG G meas{r : r_{g~z1}(r) in F} <= 2 meas F (would allow keeping the restriction at z1)", 'NEG',
       1 if pre > 2 * measF else 0, 1)

# ---------------------------------------------------------------------------------------------------------------
print("== (H) Prop. 4.5(ii), p. 46: F_1 factorisation, H_{1,p} average, Bonferroni truncation")
fH = [0, 0, 0]; nH = 0; fHn = 0
PH = [3, 5, 7, 11, 13, 17]
for _ in range(400):
    rho = random.choice([0.05, 0.3, 0.7, 0.95])
    za = (1, 0)
    while True:
        zb = (random.randrange(-99, 100, 2), random.randint(-99, 99))
        if math.gcd(*zb) == 1 and all((zb[0] % q, zb[1] % q) != (0, 0) for q in PH):
            break
    l = {q: random.randint(0, q) for q in PH}
    w0 = sum(l[q] == line_idx(za, q) for q in PH); w1 = sum(l[q] == line_idx(zb, q) for q in PH)
    H = lambda q, lq: 1 - rho ** (0.5 * ((lq == line_idx(za, q)) + (lq == line_idx(zb, q))))
    prod = 1.0
    for q in PH:
        prod *= 1 - H(q, l[q])
    nH += 1
    if abs(prod - rho ** ((w0 + w1) / 2)) > 1e-12:
        fH[0] += 1
    for q in PH:
        avg = sum(H(q, lq) for lq in range(q + 1)) / (q + 1)
        if avg > 2 / (q + 1) + 1e-15:
            fH[1] += 1
        if avg > 1 / (q + 1) + 1e-15:
            fHn += 1
    x = [random.random() ** 3 for _ in range(random.randint(3, 12))]
    e = [1.0] + [0.0] * len(x)
    for xi in x:
        for kk in range(len(x), 0, -1):
            e[kk] += e[kk - 1] * xi
    P_ = 1.0
    for xi in x:
        P_ *= 1 - xi
    for B in range(1, len(x) + 1):
        if abs(P_ - sum((-1) ** kk * e[kk] for kk in range(B))) > e[B] + 1e-12:
            fH[2] += 1
report("H rho^{(w_l(z0)+w_l(z1))/2} = prod_p (1 - H_{1,p}(l_p))", 'POS', fH[0], nH)
report("H (p+1)^{-1} sum_l H_{1,p}(l) <= 2/(p+1)", 'POS', fH[1], nH * len(PH))
report("H Bonferroni: |prod(1-x) - sum_{k<B} (-1)^k e_k| <= e_B on [0,1]^n", 'POS', fH[2], nH)
report("NEG H (p+1)^{-1} sum_l H_{1,p}(l) <= 1/(p+1)", 'NEG', fHn, nH * len(PH))

# ---------------------------------------------------------------------------------------------------------------
print("== SUMMARY")
pos = [r for r in RESULTS if r[1] == 'POS']; neg = [r for r in RESULTS if r[1] == 'NEG']
print(f"positive checks: {len(pos)}, failing: {sum(1 for r in pos if not r[2])}")
print(f"negative controls: {len(neg)}, failing as they must: {sum(1 for r in neg if r[2])}")
bad = [r[0] for r in RESULTS if not r[2]]
print(f"unexpected outcomes: {len(bad)} {bad}")
print(f"wall time {time.time() - T0:.1f} s")
