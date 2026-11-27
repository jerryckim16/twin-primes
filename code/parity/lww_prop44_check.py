#!/usr/bin/python3
"""Toy checks for LWW (arXiv:2610.20242v2) Proposition 4.4 and (4.73) (pp. 31-33).

Run: /usr/bin/python3 -I code/parity/lww_prop44_check.py
Route card: notes/parity-attempts/2026-11-27-lww-prop44.md

Sections
 (A) T bijection: Omega cap C  <->  primitive integer points of Omega' = T Omega with odd first
     coordinate; gcd(u,(u-v)/2) = gcd(u,v) for odd u,v; g' = TgE in SL2(Z)           exact integers
 (B) det(TP,TQ) = -det(P,Q)/2; t = det(P,Q)/D even when P,Q odd and D | P1, Q1      exact Fractions
     hence 1_{t=2(a-b)} = 1_{t'=b-a} and psi_{-2}(t/Y) = psi_1(t'/Y)
 (C) (-2c, d-c) is a complement to TP, r_TP = -2 r_P (mod 1), compared with r_TP
     computed independently from TP by the extended Euclidean algorithm                exact Fractions
 (D) (4.76): int_{M_-2} e(theta(t-2(a-b))) = int_{M_1} e(phi(t'-b+a)), toy major arcs  closed form,
     (D') the same on a non-symmetric toy set, where a phase-sign error is visible
     complex floats (tol 1e-12)
 (E) toy operator model, K = 1, J = 1: A_-2^C = G_-2 S T_-2^C S G_-2 built from (4.38)-(4.41) on
     S cap C, and A_1^{Omega',odd} built independently from (4.23), (4.25)-(4.27), (4.69) on the
     integer points of Omega' (4.68). Checks U_T A U_T^{-1} = A' entrywise (4.72), the moment
     identity (4.73) for R = 1, 2, 3 and every P, and the summed form (4.54) <-> (4.78).
     G conditions: (4.26) literal with toy thresholds; (4.27) literal for K = 1 (F_I is then an
     indicator), toy threshold.                                                         complex floats
Negative controls are marked NEG and must FAIL.
Toy parameters only: nothing here tests sizes, bounds or the analytic content of Prop. 4.2.
"""
import math, random, time, itertools, cmath
from fractions import Fraction as F
import numpy as np

T0 = time.time()
random.seed(20261127)
RESULTS = []


def report(name, kind, failures, total, detail=""):
    ok = (failures == 0) if kind == 'POS' else (failures > 0)
    RESULTS.append((name, kind, ok))
    tag = "ok" if ok else "UNEXPECTED"
    print(f"[{kind}] {name}: {failures}/{total} failures -> {tag} {detail}")


def egcd_complement(u, v):
    """Return (c, d) with u*d - v*c = 1 (u, v coprime)."""
    # extended Euclid: x*u + y*v = 1 -> d = x, c = -y
    a, b = u, v
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    g = a
    if g < 0:
        g, x0, y0 = -g, -x0, -y0
    assert g == 1
    d, c = x0, -y0
    assert u * d - v * c == 1
    return c, d


def frac1(x):  # x mod 1 in [0,1) for Fraction
    return x - math.floor(x)


def dist_int(x):  # ||x|| for Fraction
    f = frac1(x)
    return min(f, 1 - f)


def Tvec(P):
    return (P[0], F(P[0] - P[1], 2))


def det(P, Q):
    return P[0] * Q[1] - P[1] * Q[0]


# ---------------------------------------------------------------- (A)
print("== (A) T bijection and g' = TgE")
UL, UH, NL, NH = 15, 240, 15, 30
fails = tot = 0
img = set()
for u in range(UL, UH + 1):
    for v in range(NL, NH + 1):
        if u % 2 == 1 and v % 2 == 1 and math.gcd(u, v) == 1:
            tot += 1
            z = Tvec((u, v))
            if z[1].denominator != 1:
                fails += 1; continue
            z = (z[0], int(z[1]))
            if not (z[0] % 2 == 1 and math.gcd(z[0], z[1]) == 1 and NL <= z[0] - 2 * z[1] <= NH):
                fails += 1
            img.add(z)
# independent enumeration of Omega' integer points (4.68), primitive, odd first coordinate
cand = set()
for u in range(UL, UH + 1):
    for w in range(-(UH), UH + 1):
        if NL <= u - 2 * w <= NH and u % 2 == 1 and math.gcd(u, w) == 1:
            cand.add((u, w))
tot += 1
if cand != img:
    fails += 1
# g' = T g E in SL2(Z), second column = (-2c, d-c)
for _ in range(3000):
    u = random.randrange(1, 4001, 2); v = random.randrange(1, 4001, 2)
    if math.gcd(u, v) != 1:
        continue
    c, d = egcd_complement(u, v)
    tot += 1
    gp = [[u, -2 * c], [F(u - v, 2), d - c]]
    if not (gp[1][0].denominator == 1 and u * (d - c) - (-2 * c) * gp[1][0] == 1):
        fails += 1
report("A bijection Omega cap C <-> primitive odd-first points of Omega'; g' in SL2(Z)", 'POS', fails, tot,
       f"(|Omega cap C| = {len(img)}, |image enumerated independently| = {len(cand)})")
# NEG: gcd(u,(u-v)/2) = gcd(u,v) without "u odd" (u, v both even)
fails = tot = 0
for u in range(2, 200, 2):
    for v in range(2, 200, 2):
        tot += 1
        if math.gcd(u, (u - v) // 2) != math.gcd(u, v):
            fails += 1
report("NEG A gcd(u,(u-v)/2) = gcd(u,v) for even u, v", 'NEG', fails, tot)

# ---------------------------------------------------------------- (B)
print("== (B) det(TP,TQ) = -det(P,Q)/2 and parity of t")
fails = tot = 0
negf = 0
for _ in range(20000):
    D = random.choice([3, 5, 7, 15, 21, 35, 105])
    P = (D * random.randrange(1, 300, 2), random.randrange(-999, 1000, 2) + 1)
    Q = (D * random.randrange(1, 300, 2), random.randrange(-999, 1000, 2) + 1)
    tot += 1
    t = F(det(P, Q), D)
    tp = F(det(Tvec(P), Tvec(Q)), D)
    ok = (t.denominator == 1 and t.numerator % 2 == 0 and tp == -t / 2 and tp.denominator == 1)
    a = random.choice([5, 7, 11, 13]); b = random.choice([5, 7, 11, 13])
    ok = ok and ((t == 2 * (a - b)) == (tp == b - a))
    if not ok:
        fails += 1
    # NEG: T~ = [[1,0],[1,-1]] (no 1/2): t~ = -t, so 1_{t=2(a-b)} = 1_{t~=b-a} would need t = 2(a-b) <=> t = a-b
    Tt = lambda R: (R[0], R[0] - R[1])
    tt = F(det(Tt(P), Tt(Q)), D)
    if tt != -t / 2:          # T~ gives t~ = -t, not -t/2 (fails unless t = 0)
        negf += 1
# force some hits of the indicator for the positive check
hits = 0
for _ in range(20000):
    D = 5
    P = (D * random.randrange(1, 40, 2), random.randrange(1, 40, 2))
    Q = (D * random.randrange(1, 40, 2), random.randrange(1, 40, 2))
    t = F(det(P, Q), D)
    for a in (5, 7, 11, 13):
        for b in (5, 7, 11, 13):
            tp = F(det(Tvec(P), Tvec(Q)), D)
            tot += 1
            if (t == 2 * (a - b)) != (tp == b - a):
                fails += 1
            hits += (t == 2 * (a - b))
report("B det(TP,TQ)/D = -t/2, t even, 1_{t=2(a-b)} = 1_{t'=b-a}", 'POS', fails, tot, f"(indicator hits {hits})")
report("NEG B det(T~P,T~Q)/D = -t/2 with T~ = [[1,0],[1,-1]] (no factor 1/2)", 'NEG', negf, 20000)

# ---------------------------------------------------------------- (C)
print("== (C) complement of TP and r_TP = -2 r_P")
fails = tot = negf = 0
for _ in range(20000):
    u = random.randrange(1, 20001, 2); v = random.randrange(-20001, 20001, 2)
    if math.gcd(u, v) != 1:
        continue
    c, d = egcd_complement(u, v)
    TP = (u, (u - v) // 2)
    tot += 1
    ok = (TP[0] * (d - c) - TP[1] * (-2 * c) == 1)
    rP = frac1(F(c, u))
    c2, d2 = egcd_complement(TP[0], TP[1])  # independent complement of TP
    rTP = frac1(F(c2, TP[0]))
    ok = ok and rTP == frac1(-2 * rP) and frac1(F(-2 * c, u)) == rTP
    if not ok:
        fails += 1
    if rTP != frac1(2 * rP):
        negf += 1
report("C (-2c, d-c) complements TP; r_TP = -2 r_P mod 1", 'POS', fails, tot)
report("NEG C r_TP = +2 r_P mod 1", 'NEG', negf, tot)

# ---------------------------------------------------------------- (D)
print("== (D) (4.76) major-arc integral identity")


def e(x):
    return cmath.exp(2j * math.pi * x)


def arcs_M1(kmax, w):
    """Merged intervals in [0,1) of M1 = union over k <= kmax, 0 <= j < k, (j,k) = 1 of ||phi - j/k|| <= w."""
    iv = []
    for k in range(1, kmax + 1):
        for j in range(k):
            if math.gcd(j, k) == 1:
                lo, hi = F(j, k) - w, F(j, k) + w
                # split into [0,1)
                for s in (-1, 0, 1):
                    a, b = max(lo + s, F(0)), min(hi + s, F(1))
                    if a < b:
                        iv.append((a, b))
    iv.sort()
    out = []
    for a, b in iv:
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def int_e(a, b, n):  # int_a^b e(n x) dx
    if n == 0:
        return float(b - a)
    return (e(float(b) * n) - e(float(a) * n)) / (2j * math.pi * n)


def I_M1(arcs, n):
    return sum(int_e(a, b, n) for a, b in arcs)


def I_Mm2(arcs, m, copies=(0, F(1, 2))):
    """int over M_-2 = {theta in T: -2 theta in M1} of e(theta m); preimage of [a,b] is
    [-b/2, -a/2] + {0, 1/2} (mod 1); m is an integer so shifts by 1 do not matter."""
    return sum(int_e(-b / 2 + s, -a / 2 + s, m) for a, b in arcs for s in copies)


fails = tot = negf1 = negf2 = 0
for kmax, w in [(1, F(1, 50)), (3, F(1, 30)), (4, F(1, 25)), (6, F(1, 100)), (5, F(1, 7))]:
    arcs = arcs_M1(kmax, w)
    for tprime in range(-40, 41):
        for a in (5, 7, 11, 13):
            for b in (5, 7, 11, 13):
                t = -2 * tprime
                lhs = I_Mm2(arcs, t - 2 * (a - b))
                rhs = I_M1(arcs, tprime - b + a)
                tot += 1
                if abs(lhs - rhs) > 1e-12:
                    fails += 1
                if abs(I_Mm2(arcs, t - 2 * (a - b), copies=(0,)) - rhs) > 1e-6:
                    negf1 += 1
                if abs(I_Mm2(arcs, t - (a - b)) - rhs) > 1e-6:
                    negf2 += 1
# one brute-force Riemann-sum spot check of I_Mm2 against the definition of M_-2 (membership test)
arcs = arcs_M1(3, F(1, 30))
Nq = 200000
def in_M1(phi):
    phi = phi % 1.0
    return any(float(a) <= phi <= float(b) for a, b in arcs)
for m in (0, 1, -6, 14):
    s = sum(e(((i + 0.5) / Nq) * m) for i in range(Nq) if in_M1(-2 * (i + 0.5) / Nq)) / Nq
    tot += 1
    if abs(s - I_Mm2(arcs, m)) > 1e-3:
        fails += 1
report("D int_{M-2} e(theta(t-2(a-b))) = int_{M1} e(phi(t'-b+a))", 'POS', fails, tot)
report("NEG D only one preimage copy of M1 under theta -> -2 theta", 'NEG', negf1, tot - 4)
report("NEG D phase t-(a-b) instead of t-2(a-b)", 'NEG', negf2, tot - 4)
# (D') non-symmetric toy major-arc set (LWW's M_1 is symmetric; this makes phase-sign errors visible)
ASYM = [(F(1, 10), F(1, 5)), (F(1, 2), F(3, 5))]
fails = tot = negf3 = 0
for tprime in range(-40, 41):
    for a in (5, 7, 11, 13):
        for b in (5, 7, 11, 13):
            nn = tprime - b + a
            lhs = I_Mm2(ASYM, -2 * tprime - 2 * (a - b))
            tot += 1
            if abs(lhs - I_M1(ASYM, nn)) > 1e-12:
                fails += 1
            if abs(lhs - I_M1(ASYM, -nn)) > 1e-6:
                negf3 += 1
for m in (1, -3, 7):  # Riemann check of the preimage formula on the asymmetric set
    s_ = sum(e(((i + 0.5) / Nq) * m) for i in range(Nq)
             if any(float(a_) <= (-2 * (i + 0.5) / Nq) % 1.0 <= float(b_) for a_, b_ in ASYM)) / Nq
    tot += 1
    if abs(s_ - I_Mm2(ASYM, m)) > 1e-3:
        fails += 1
report("D' (4.76) on a non-symmetric toy M_1", 'POS', fails, tot)
report("NEG D' phase sign flipped (int_{M1} e(-phi(t'-b+a))) on the non-symmetric set", 'NEG', negf3, tot - 3)

# ---------------------------------------------------------------- (E)
print("== (E) toy operator model, K = 1, J = 1")
PR = [3, 5, 7, 11, 13]          # toy P_1 (odd primes)
D0 = 4                          # d0: D in [4, 8)
Y = 4                           # a, b in [Y, 4Y]
RHO = 0.5
V1 = 0.9                        # toy V_1
LMAX, EPS1 = 2, F(3, 50)        # toy (4.26): 1 <= l <= LMAX, ||l D~ r|| > EPS1
EPS2 = F(1, 20)                 # toy (4.27) (K = 1): no h,h' with D~ != D~' and ||(D~-D~') r|| < EPS2
ARCS = arcs_M1(3, F(1, 30))
OUL, OUH, ONL, ONH = 105, 1680, 9, 18  # Omega = [OUL, OUH] x [ONL, ONH]


def eta(x):
    return math.sin(math.pi * (x - 1) / 3) ** 2 if 1 < x < 4 else 0.0


def psi1(x):  # asymmetric toy psi_1 (LWW's psi_1 need not be even; asymmetry detects sign slips)
    if -10 < x < 6:
        return (1.0 + 0.04 * x) * math.cos(math.pi * (x + 2) / 16) ** 2
    return 0.0


def omega(n):
    return sum(1 for p in PR if n % p == 0)


def good(pt, r):
    """(4.26) and (4.27) for K = 1, J = 1 with toy thresholds; pt = (p11, p12); r a Fraction mod 1."""
    Dts = [pt[1], pt[0]]  # D~ for h = 1, 2 (omit entry h)
    for Dt in Dts:
        if D0 <= Dt < 2 * D0:
            for l in range(1, LMAX + 1):
                if not dist_int(l * Dt * r) > EPS1:
                    return False
    for Dt in Dts:
        for Dt2 in Dts:
            if Dt != Dt2 and dist_int((Dt - Dt2) * r) < EPS2:
                return False
    return True


def states_from_positions(positions):
    st = []
    for P in positions:
        divs = [p for p in PR if P[0] % p == 0]
        for p11 in divs:
            for p12 in divs:
                if p11 != p12:
                    st.append((P, (p11, p12)))
    return st


# S cap C: positions in Omega with gcd 1 and both coordinates odd
posC = [(u, v) for u in range(OUL, OUH + 1) for v in range(ONL, ONH + 1)
        if u % 2 and v % 2 and math.gcd(u, v) == 1 and sum(1 for p in PR if u % p == 0) >= 2]
SC = states_from_positions(posC)
# image space, enumerated independently from (4.68): primitive integer points of Omega' with odd u
posO = [(u, w) for u in range(OUL, OUH + 1) for w in range(-OUH, OUH + 1)
        if ONL <= u - 2 * w <= ONH and u % 2 and math.gcd(u, w) == 1 and sum(1 for p in PR if u % p == 0) >= 2]
SO = states_from_positions(posO)
idxC = {s: i for i, s in enumerate(SC)}
idxO = {s: i for i, s in enumerate(SO)}
n = len(SC)
print(f"  |S cap C| = {n} states on {len(posC)} positions; |image space| = {len(SO)}")
# U_T as an index map
perm = np.full(n, -1)
bad = 0
for i, (P, pt) in enumerate(SC):
    z = (P[0], (P[0] - P[1]) // 2)
    j = idxO.get((z, pt), -1)
    if j < 0:
        bad += 1
    perm[i] = j
assert len(set(perm.tolist())) == n


def kernel_bracket(tval, a, b, primed, variant):
    """Value of eta eta psi rho^{..} d0/D {1 - int} without the eta, rho, d0/D factors: returns psi * {..}."""
    if primed:  # K_1 at (TP, TQ): t' = det(TP,TQ)/D
        ind_target = (b - a) if variant != 'wrong_sign' else (a - b)
        return psi1(tval / Y) * ((1.0 if tval == ind_target else 0.0) - I_M1(ARCS, tval - b + a))
    # (4.38): t = det(P,Q)/D, psi_{-2}(t/Y) = psi1(-t/(2Y))
    ps = psi1(-tval / (2 * Y)) if variant != 'psi_sign' else psi1(tval / (2 * Y))
    copies = (0, F(1, 2)) if variant != 'one_copy' else (0,)
    return ps * ((1.0 if tval == 2 * (a - b) else 0.0) - I_Mm2(ARCS, tval - 2 * (a - b), copies))


def build_T(states, idx, primed, variant=None):
    m = len(states)
    T = np.zeros((m, m), dtype=complex)
    # group states by prime tuple for speed
    by_pt = {}
    for j, (Q, qt) in enumerate(states):
        by_pt.setdefault(qt, []).append((j, Q))
    for i, (P, pt) in enumerate(states):
        D, b = pt[0], pt[1]
        if not (D0 <= D < 2 * D0):
            continue
        for a in PR:
            if a in pt:
                continue
            for j, Q in by_pt.get((pt[0], a), []):
                dt = det(P, Q)
                assert dt % D == 0
                tval = dt // D
                ker = kernel_bracket(tval, a, b, primed, variant)
                if ker == 0:
                    continue
                coef = (1 / V1) * (D0 / D) * eta(a / Y) * eta(b / Y) * RHO ** ((omega(P[0]) + omega(Q[0]) - 4) / 2)
                T[i, j] += coef * ker
    return T


def build_S(states, idx):
    m = len(states)
    S = np.zeros((m, m))
    for i, (P, pt) in enumerate(states):
        for perm2 in itertools.permutations(pt):
            S[i, idx[(P, perm2)]] += 0.5
    return S


def build_G(states, primed, variant=None):
    g = np.zeros(len(states))
    for i, (P, pt) in enumerate(states):
        if primed:
            if variant == 'use_rP':
                Pre = (P[0], P[0] - 2 * P[1])  # preimage T^{-1} z
                c, d = egcd_complement(*Pre)
                r = frac1(F(c, Pre[0]))
            else:
                c, d = egcd_complement(P[0], P[1])
                r = frac1(F(c, P[0]))       # r_{TP} from TP's own complement (4.25)
        else:
            c, d = egcd_complement(P[0], P[1])
            r = frac1(-2 * F(c, P[0]))      # (4.39): r_P replaced by -2 r_P
        g[i] = 1.0 if good(pt, r) else 0.0
    return np.diag(g)


TC = build_T(SC, idxC, primed=False)
SCm = build_S(SC, idxC)
GC = build_G(SC, primed=False)
A = GC @ SCm @ TC @ SCm @ GC
TO = build_T(SO, idxO, primed=True)
SOm = build_S(SO, idxO)
GO = build_G(SO, primed=True)
Ap = GO @ SOm @ TO @ SOm @ GO
nnzT = int(np.count_nonzero(np.abs(TC) > 0))
ind_hits = 0
ind_nz = 0
for i, (P, pt) in enumerate(SC):
    for a in PR:
        if a in pt or not (D0 <= pt[0] < 2 * D0):
            continue
        for Q, qt in [(s[0], s[1]) for s in SC if s[1] == (pt[0], a)]:
            if det(P, Q) // pt[0] == 2 * (a - pt[1]) and abs(psi1(-det(P, Q) / pt[0] / (2 * Y))) > 0:
                ind_hits += 1
                ind_nz += (eta(a / Y) * eta(pt[1] / Y) != 0)
print(f"  nonzero T entries {nnzT}; edges with t = 2(a-b) inside supp psi: {ind_hits}, of which non-zero (eta != 0): {ind_nz}; "
      f"good fraction {np.trace(GC)/n:.3f}; ||A|| (Frobenius) {np.linalg.norm(A):.3e}")
Pm = np.zeros((n, n))
for i in range(n):
    Pm[perm[i], i] = 1.0       # (U_T f)[perm[i]] = f[i]


def maxdiff(X, Yy):
    return float(np.max(np.abs(X - Yy)))


fails = tot = 0
d = maxdiff(Pm @ TC @ Pm.T, TO); tot += 1; fails += d > 1e-12
print(f"  (4.74) max |U T_-2^C U^-1 - T_1^Omega'| = {d:.2e}")
d = maxdiff(Pm @ GC @ Pm.T, GO); tot += 1; fails += d > 0
print(f"  (4.77) max |U G_-2 U^-1 - G_1^Omega'| = {d:.2e}")
d = maxdiff(Pm @ SCm @ Pm.T, SOm); tot += 1; fails += d > 0
d = maxdiff(Pm @ A @ Pm.T, Ap); tot += 1; fails += d > 1e-12
print(f"  (4.72) max |U A_-2^C U^-1 - A_1^Omega',odd| = {d:.2e}")
# unitarity: sigma constant, U is a permutation
tot += 1; fails += maxdiff(Pm @ Pm.T, np.eye(n)) > 0
report("E (4.72), (4.74), (4.77), S, unitarity", 'POS', fails, tot, f"(bad image states {bad})")

# (4.73): moments for every P, R = 1, 2, 3 (sigma constant, so adjoint = conjugate transpose)
B = A @ A.conj().T
Bp = Ap @ Ap.conj().T
fails = tot = 0
sums = {}
nontriv = {}
tiny = {}
for R in (1, 2, 3):
    BR = np.linalg.matrix_power(B, R)
    BpR = np.linalg.matrix_power(Bp, R)
    sL = sR = 0.0
    for P in posC:
        uP = np.array([1.0 if s[0] == P else 0.0 for s in SC])
        z = (P[0], (P[0] - P[1]) // 2)
        uT = np.array([1.0 if s[0] == z else 0.0 for s in SO])
        lhs = uP @ BR @ uP
        rhs = uT @ BpR @ uT
        sL += lhs.real; sR += rhs.real
        tot += 1
        nontriv[R] = nontriv.get(R, 0) + (abs(lhs) > 0)
        tiny[R] = tiny.get(R, 0) + (0 < abs(lhs) <= 1e-20)
        if abs(lhs - rhs) > 1e-12 * max(1.0, abs(lhs)):
            fails += 1
    sums[R] = (sL, sR)
    print(f"  R = {R}: positions with non-zero moment {nontriv[R]}/{len(posC)} (of which |moment| <= 1e-20: {tiny[R]})")
    print(f"  R = {R}: sum_P <u_P,(AA*)^R u_P> = {sL:.6e}; sum_P <u~_TP,(A'A'*)^R u~_TP> = {sR:.6e}")
report("E (4.73) for every P in Omega cap C, R = 1, 2, 3; hence (4.54) <-> (4.78)", 'POS', fails, tot)

for variant, label in [('wrong_sign', "kernel' with 1_{t'=a-b}"),
                       ('one_copy', "T_-2^C with one preimage copy of M_1"),
                       ('psi_sign', "psi_-2(u) = psi_1(u/2) (sign dropped)")]:
    if variant == 'wrong_sign':
        X = build_T(SO, idxO, primed=True, variant=variant); dd = maxdiff(Pm @ TC @ Pm.T, X)
    else:
        X = build_T(SC, idxC, primed=False, variant=variant); dd = maxdiff(Pm @ X @ Pm.T, TO)
    report(f"NEG E (4.74) with {label}", 'NEG', int(dd > 1e-6), 1, f"(max diff {dd:.2e})")
X = build_G(SO, primed=True, variant='use_rP')
dd = int(np.sum(np.abs(np.diag(Pm @ GC @ Pm.T) - np.diag(X)) > 0))
report("NEG E (4.77) with G_1^Omega' using r_P instead of r_TP", 'NEG', dd, n)
Ab = GC @ SCm @ build_T(SC, idxC, primed=False, variant='psi_sign') @ SCm @ GC
Bb = Ab @ Ab.conj().T
dd = 0
for P in posC[:400]:
    uP = np.array([1.0 if s[0] == P else 0.0 for s in SC])
    z = (P[0], (P[0] - P[1]) // 2)
    uT = np.array([1.0 if s[0] == z else 0.0 for s in SO])
    dd += abs(uP @ Bb @ uP - uT @ Bp @ uT) > 1e-9
report("NEG E (4.73), R = 1, with the psi sign dropped on the left", 'NEG', int(dd), min(400, len(posC)))

print("== SUMMARY")
pos = [r for r in RESULTS if r[1] == 'POS']; neg = [r for r in RESULTS if r[1] == 'NEG']
print(f"positive checks: {len(pos)}, failing: {sum(1 for r in pos if not r[2])}")
print(f"negative controls: {len(neg)}, failing as they must: {sum(1 for r in neg if r[2])}")
unexp = [r[0] for r in RESULTS if not r[2]]
print(f"unexpected outcomes: {len(unexp)} {unexp}")
print(f"wall time {time.time() - T0:.1f} s")
