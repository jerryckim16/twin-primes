#!/usr/bin/python3
"""Toy checks for LWW (arXiv:2610.20242v2) Proposition 4.3, (4.54) => (4.55) (pp. 27-30).

Run: /usr/bin/python3 -I code/parity/lww_prop43_check.py
Route card: notes/parity-attempts/2026-11-27-lww-prop43.md

Sections
 (A) localisation geometry (p. 28): P, Q in Omega = [d0YM, 16d0YM] x [N, 2N] primitive with
     |det(P,Q)| < 32 d0 Y  =>  |j - k| <= 32, where P2/P1 in I_j, Q2/Q1 in I_k,
     I_j = [j/(d0YM^2), (j+1)/(d0YM^2)).                                     exact integers
 (B) block count (pp. 28-29): in each block, |det(P0, P)| < 256 d0Y; for each h at most 16
     P with det(P0,P) = h; so #block <= 16(2*256 d0Y - 1) << d0Y.               exact integers
 (C) toy operator model (checks the linear algebra; its (4.57) test is weak because the 65-block
     window covers most of the toy j-range -- the localisation is carried by (A)) on positions Omega cap C with several states per position, constant
     weight sigma, conjugate-linear-first inner product (4.21), S = fibrewise averaging, G
     = fibrewise 0/1 mask, T = random kernel times psi_{-2}(det(P,Q)/(D Y)) 1_{d0<=D<2d0},
     A = G S T S G.  Checks (4.57), (4.63) identities, sum ||g_j||^2 = 65||g||^2,
     f_j = sum f(P) u_P, M_j PSD, lambda_max <= d_j (4.61), (4.62), Hoelder (4.64), and the
     assembled bound behind (4.66) with explicit constants.                   complex floats
 (D) exponent bookkeeping for (4.66) and the final step (exact Fractions), and the size of
     (d0 Y)^{1/(2R)} with R = ceil(L^{1/2}/2) (floats).
Negative controls are marked NEG and must FAIL.
Toy parameters only: nothing here tests the hypothesis (4.54) or any analytic input.
"""
import math, random, time
from fractions import Fraction as Fr
import numpy as np

T0 = time.time()
random.seed(20261127)
RNG = np.random.default_rng(20261127)
RESULTS = []


def report(name, kind, failures, total, detail=""):
    ok = (failures == 0) if kind == 'POS' else (failures > 0)
    RESULTS.append((name, kind, ok))
    tag = "ok" if ok else "UNEXPECTED"
    print(f"[{kind}] {name}: {failures}/{total} failures -> {tag} {detail}")


def positions(d0, Y, M, N, odd=False, p1lo=None):
    lo = d0 * Y * M if p1lo is None else p1lo
    out = []
    for u in range(lo, 16 * d0 * Y * M + 1):
        for v in range(N, 2 * N + 1):
            if math.gcd(u, v) != 1:
                continue
            if odd and (u % 2 == 0 or v % 2 == 0):
                continue
            out.append((u, v))
    return out


def jindex(P, W):  # unique j with P2/P1 in [j/W, (j+1)/W), exact
    return (W * P[1]) // P[0]


PARAMS = [(2, 3, 4, 10), (4, 2, 3, 7), (1, 5, 2, 6), (8, 1, 3, 5), (1, 1, 6, 9)]

# ---------------------------------------------------------------- (A)
print("== (A) localisation: |det(P,Q)| < 32 d0 Y  =>  |j-k| <= 32")
fails = tot = 0
neg16 = 0
neg48 = 0
tot48 = 0
maxjk = 0
for (d0, Y, M, N) in PARAMS:
    W = d0 * Y * M * M
    pos = positions(d0, Y, M, N)
    U = np.array([p[0] for p in pos], dtype=np.int64)
    V = np.array([p[1] for p in pos], dtype=np.int64)
    J = (W * V) // U
    DET = np.abs(np.outer(U, V) - np.outer(V, U))
    near = DET < 32 * d0 * Y
    JK = np.abs(J[:, None] - J[None, :])
    tot += int(near.sum())
    fails += int((JK[near] > 32).sum())
    neg16 += int((JK[near] > 16).sum())
    # NEG (audit finding 1): support widened by 50% (psi_1(-u/3): |det| < 24 D Y < 48 d0 Y), window kept at 32
    near48 = DET < 48 * d0 * Y
    tot48 += int(near48.sum())
    neg48 += int((JK[near48] > 32).sum())
    mx = int(JK[near].max())
    maxjk = max(maxjk, mx)
    print(f"   (d0,Y,M,N)={d0, Y, M, N}: {len(pos)} primitive positions, {int(near.sum())} near pairs, max |j-k| = {mx}")
report("A |det| < 32 d0Y => |j-k| <= 32", 'POS', fails, tot)
report("NEG A window 16 in place of 32", 'NEG', neg16, tot)
report("NEG A kernel support widened to |det| < 48 d0Y (psi_1(-u/3)), window 32", 'NEG', neg48, tot48)

# ---------------------------------------------------------------- (B)
print("== (B) block count #{P primitive in Omega : P2/P1 in I_j} << d0 Y")
fdet = fh = fcnt = tot_b = tot_h = 0
neg_const1 = 0
ratios = []
maxh = 0
for (d0, Y, M, N) in PARAMS:
    W = d0 * Y * M * M
    pos = positions(d0, Y, M, N)
    blocks = {}
    for P in pos:
        blocks.setdefault(jindex(P, W), []).append(P)
    bound = 16 * (2 * 256 * d0 * Y - 1)
    for j, Bl in blocks.items():
        P0 = Bl[0]
        hs = {}
        for P in Bl:
            h = P0[0] * P[1] - P0[1] * P[0]
            tot_b += 1
            if abs(h) >= 256 * d0 * Y:
                fdet += 1
            hs[h] = hs.get(h, 0) + 1
        mh = max(hs.values())
        tot_h += 1
        maxh = max(maxh, mh)
        if mh > 16:
            fh += 1
        if len(Bl) > bound:
            fcnt += 1
        if len(Bl) > d0 * Y:
            neg_const1 += 1
        ratios.append(len(Bl) / (d0 * Y))
    # full per-h count over Omega for a few P0 (stronger than needed)
    for P0 in random.sample(pos, 20):
        cnt = {}
        for P in pos:
            h = P0[0] * P[1] - P0[1] * P[0]
            cnt[h] = cnt.get(h, 0) + 1
        tot_h += 1
        if max(cnt.values()) > 16:
            fh += 1
        maxh = max(maxh, max(cnt.values()))
report("B |det(P0,P)| < 256 d0Y inside a block", 'POS', fdet, tot_b)
report("B at most 16 primitive P with det(P0,P) = h (blocks; and all of Omega for 100 random P0)", 'POS', fh, tot_h,
       f"(max observed {maxh})")
report("B #block <= 16(512 d0Y - 1)", 'POS', fcnt, len(ratios), f"(max #block/(d0Y) = {max(ratios):.1f})")
report("NEG B #block <= d0Y (implied constant 1)", 'NEG', neg_const1, len(ratios))
report("NEG B at most 1 primitive P with det(P0,P) = h (sensitivity)", 'NEG', int(maxh > 1), 1, f"(max {maxh})")
# LWW's "16" uses the P1-range only: the solutions are P* + k P0, and P1* + k P1^(0) in [d0YM, 16 d0YM]
# with P1^(0) >= d0YM allows at most 16 values of k.  (The P2-range [N, 2N] with P2^(0) >= N already
# allows at most 2, which is what (B) observes.)  Check the P1-only count, and a NEG with the lower end
# of the P1-range lowered to d0YM/4 (then P1^(0) can be ~ d0YM/4 and up to ~61 values of k fit).
fk = negk = totk = 0
for (d0, Y, M, N) in PARAMS:
    lo, hi = d0 * Y * M, 16 * d0 * Y * M
    for p10 in range(lo, hi + 1, max(1, (hi - lo) // 50)):
        for start in range(lo, lo + p10):
            ks = (hi - start) // p10 + 1  # number of k >= 0 with start + k p10 <= hi (start = smallest in range)
            totk += 1
            fk += int(ks > 16)
    lo4 = max(1, lo // 4)
    p10 = lo4
    ks = (hi - lo4) // p10 + 1
    negk += int(ks > 16)
report("B P1-range: at most 16 values of k with P1* + k P1^(0) in [d0YM, 16d0YM]", 'POS', fk, totk)
report("NEG B the same with the P1-range lowered to [d0YM/4, 16d0YM]", 'NEG', negk, len(PARAMS))

# ---------------------------------------------------------------- (C)
print("== (C) toy operator model")
d0, Y, M, N = 2, 3, 4, 10
W = d0 * Y * M * M
posC = positions(d0, Y, M, N, odd=True)
states = []  # (pos index, D)
fib = []
for i, P in enumerate(posC):
    s = random.choice([1, 2, 3])
    ids = []
    for _ in range(s):
        ids.append(len(states))
        states.append((i, random.choice(list(range(d0, 2 * d0)) + [2 * d0])))  # D = 2d0 occasionally: killed by indicator
    fib.append(ids)
n = len(states)
sigma = 0.37
Jpos = np.array([jindex(P, W) for P in posC])
Jst = np.array([Jpos[i] for (i, _) in states])
print(f"   {len(posC)} positions in Omega cap C, {n} states, blocks j in [{Jpos.min()}, {Jpos.max()}]")


def psi1(u):
    u = abs(u)
    if u <= 4:
        return 1.0
    if u >= 8:
        return 0.0
    x = (u - 4) / 4
    a = math.exp(-1 / x) if x > 0 else 0.0
    b = math.exp(-1 / (1 - x)) if x < 1 else 0.0
    return b / (a + b)


def psim2(u):
    return psi1(-u / 2)


S = np.zeros((n, n))
for ids in fib:
    # S averages within fibre orbits; orbit = the whole fibre here (a projection, S^2 = S = S*)
    for a in ids:
        for b in ids:
            S[a, b] = 1.0 / len(ids)
G = np.diag([1.0 if random.random() < 0.9 else 0.0 for _ in range(n)])
Traw = RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n))
cut = np.zeros((n, n))
for a, (i, D) in enumerate(states):
    if not (d0 <= D < 2 * d0):
        continue
    P = posC[i]
    for b, (k, _) in enumerate(states):
        Q = posC[k]
        cut[a, b] = psim2((P[0] * Q[1] - P[1] * Q[0]) / (D * Y))
T = Traw * cut / 10
A = G @ S @ T @ S @ G
Astar = A.conj().T  # adjoint for <f,g> = sum conj(f) g sigma with sigma constant
print(f"   S^2 = S: {np.abs(S @ S - S).max():.1e}; nonzero kernel entries {int((cut > 0).sum())}")


def ip(f, g):
    return np.vdot(f, g) * sigma


fails = 0
blocks = sorted(set(Jpos.tolist()))
negw = 0
negnl = 0
Rnd = RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n))
Anl = G @ S @ Rnd @ S @ G  # non-local control
for trial in range(5):
    g = RNG.normal(size=n) + 1j * RNG.normal(size=n)
    Ag = A @ g
    for j in blocks:
        inj = (Jst == j)
        gj = np.where(np.abs(Jst - j) <= 32, g, 0)
        fails += int(np.abs((A @ gj - Ag)[inj]).max() > 1e-9)
        g16 = np.where(np.abs(Jst - j) <= 16, g, 0)
        negw += int(np.abs((A @ g16 - Ag)[inj]).max() > 1e-9)
        negnl += int(np.abs((Anl @ gj - Anl @ g)[inj]).max() > 1e-9)
report("C (4.57) (A g)(P,p) = (A g_j)(P,p) for P2/P1 in I_j [weak: window covers most of the toy j-range; (A) carries (4.57)]", 'POS', fails, 5 * len(blocks))
report("NEG C (4.57) with window 16", 'NEG', negw, 5 * len(blocks))
report("NEG C (4.57) for a non-local operator (psi cutoff removed)", 'NEG', negnl, 5 * len(blocks))

# f depending only on the position, supported on C (all toy positions are in C)
fpos = (RNG.normal(size=len(posC)) + 1j * RNG.normal(size=len(posC)))
fpos /= np.abs(fpos).max()
f = np.array([fpos[i] for (i, _) in states])
supf = np.abs(fpos).max()


def uP(i):
    v = np.zeros(n)
    v[fib[i]] = 1.0
    return v


# (4.63) identity, norms, f_j expansion
f_bl = {j: np.where(Jst == j, f, 0) for j in blocks}
g = RNG.normal(size=n) + 1j * RNG.normal(size=n)
g_bl = {j: np.where(np.abs(Jst - j) <= 32, g, 0) for j in blocks}
lhs = ip(f, A @ g)
rhs1 = sum(ip(f_bl[j], A @ g_bl[j]) for j in blocks)
rhs2 = sum(ip(Astar @ f_bl[j], g_bl[j]) for j in blocks)
e1 = abs(lhs - rhs1) + abs(lhs - rhs2)
sg = sum(ip(g_bl[j], g_bl[j]).real for j in blocks)
sf = sum(ip(f_bl[j], f_bl[j]).real for j in blocks)
# 65 is exact only when all 65 neighbouring blocks exist; in general <= 65
e2 = int(sg > 65 * ip(g, g).real * (1 + 1e-12)) + int(abs(sf - ip(f, f).real) > 1e-9)
e3 = 0
for j in blocks:
    exp_ = sum(fpos[i] * uP(i) for i in range(len(posC)) if Jpos[i] == j)
    e3 += int(np.abs(exp_ - f_bl[j]).max() > 1e-12)
report("C (4.63) <f,Ag> = sum_j <f_j,A g_j> = sum_j <A* f_j, g_j>", 'POS', int(e1 > 1e-8), 1, f"(err {e1:.1e})")
report("C sum ||f_j||^2 = ||f||^2, sum over occupied j of ||g_j||^2 <= 65 ||g||^2", 'POS', e2, 2,
       f"(ratio {sg / ip(g, g).real:.3f})")
report("C f_j = sum_{P in block} f(P) u_P", 'POS', e3, len(blocks))

# moments
B = A @ Astar
w, Vv = np.linalg.eigh(B)
w = np.clip(w, 0, None)
print(f"   B = A A*: min eig {np.linalg.eigvalsh(B).min():.1e}, max eig {w.max():.3e}")
cnt_bl = {j: int((Jpos == j).sum()) for j in blocks}
cntmax = max(cnt_bl.values())
f461 = f462 = f464 = f466 = 0
tot461 = 0
negB = 0
negcnt = 0
negh = 0
for R in (1, 2, 3, 4, 6):
    BR = (Vv * w ** R) @ Vv.conj().T
    Bp = A + Astar  # indefinite Hermitian: lambda_max <= trace must fail somewhere
    dsum = 0.0
    lhs_sum = 0.0
    for j in blocks:
        idx = [i for i in range(len(posC)) if Jpos[i] == j]
        U_ = np.array([uP(i) for i in idx]).T
        Mj = (U_.conj().T @ BR @ U_) * sigma
        Mjb = (U_.conj().T @ Bp @ U_) * sigma
        ev = np.linalg.eigvalsh((Mj + Mj.conj().T) / 2)
        evb = np.linalg.eigvalsh((Mjb + Mjb.conj().T) / 2)
        dj = np.trace(Mj).real
        tot461 += 1
        if ev.min() < -1e-12 * max(1, abs(ev).max()) or ev.max() > dj * (1 + 1e-10) + 1e-300:
            f461 += 1
        if evb.max() > np.trace(Mjb).real + 1e-12:
            negB += 1
        xi = fpos[idx]
        q = ip(f_bl[j], BR @ f_bl[j]).real
        q2 = (xi.conj() @ Mj @ xi).real
        if abs(q - q2) > 1e-9 * max(1, abs(q)) or q > ev.max() * np.sum(np.abs(xi) ** 2) * (1 + 1e-10) + 1e-300 \
                or q > dj * cnt_bl[j] * supf ** 2 * (1 + 1e-10) + 1e-300:
            f462 += 1
        # NEG: drop the block count (bound by d_j sup|f|^2 only), with xi = top eigenvector of M_j, sup 1
        top = np.linalg.eigh((Mj + Mj.conj().T) / 2)[1][:, -1]
        top = top / np.abs(top).max()
        if (top.conj() @ Mj @ top).real > dj * 1.0 * (1 + 1e-10) + 1e-300:
            negcnt += 1
        dsum += dj
        lhs_sum += q
    # (4.64): sum ||A* f_j||^2 = sum <f_j, B f_j> <= ||f||^{2-2/R} (sum <f_j, B^R f_j>)^{1/R}
    s1 = sum(np.linalg.norm(Astar @ f_bl[j]) ** 2 * sigma for j in blocks)
    s1b = sum(ip(f_bl[j], B @ f_bl[j]).real for j in blocks)
    nf2 = ip(f, f).real
    hb = nf2 ** (1 - 1 / R) * lhs_sum ** (1 / R)
    if abs(s1 - s1b) > 1e-9 * s1 or s1 > hb * (1 + 1e-10):
        f464 += 1
    # NEG Hoelder with swapped exponents (sum w)^{1/R} (sum lambda^R w)^{1-1/R} (R > 1 only)
    if R > 1:
        hs = nf2 ** (1 / R) * lhs_sum ** (1 - 1 / R)
        negh += int(s1 > hs * (1 + 1e-10))
    # trace identity (4.65)
    tr = sum(ip(uP(i), BR @ uP(i)).real for i in range(len(posC)))
    # assembled (4.63)-(4.65): |<f,Af>|^2 <= 65 ||f||^2 ||f||^{2-2/R} (cntmax sup|f|^2 sum_j d_j)^{1/R}
    val = abs(ip(f, A @ f)) ** 2
    bnd = 65 * nf2 * nf2 ** (1 - 1 / R) * (cntmax * supf ** 2 * tr) ** (1 / R)
    if abs(tr - dsum) > 1e-9 * max(1, tr) or val > bnd * (1 + 1e-10):
        f466 += 1
    print(f"   R={R}: |<f,Af>|^2 = {val:.3e} <= {bnd:.3e};  sum d_j = {dsum:.3e}")
report("C (4.61) M_j PSD and lambda_max(M_j) <= d_j = tr M_j", 'POS', f461, tot461)
report("C (4.62) <f_j,B^R f_j> = xi* M_j xi <= lambda_max |xi|^2 <= d_j #block sup|f|^2", 'POS', f462, tot461)
report("C (4.64) Hoelder step", 'POS', f464, 5)
report("C (4.65)-(4.66) assembled bound with explicit constants (65, max block count) [sanity only: 6-8 orders of slack, no NEG]", 'POS', f466, 5)
report("NEG C lambda_max <= trace for the indefinite M_j built from A + A*", 'NEG', negB, tot461)
report("NEG C (4.62) without the block count (xi = top eigenvector, sup 1)", 'NEG', negcnt, tot461)
report("NEG C Hoelder with swapped exponents", 'NEG', negh, 4)

# ---------------------------------------------------------------- (D)
print("== (D) exponent bookkeeping")
# |<f,Ag>|^2 <= 65 ||g||^2 ||f||^{2-2/R} (c d0Y sup|f|^2 sum d_j)^{1/R} with ||g||^2,||f||^2 <= X0 L^{4C},
# sup|f|^2 <= L^{4C}, sum d_j <= X0 L^{-2R E0}, X0 = d0YMN.  Exponents of X0 and L in |<f,Ag>|:
fails = negd = 0
for R in range(2, 60):
    for C in (Fr(1, 2), Fr(1), Fr(7, 3)):
        for E0 in (Fr(5), Fr(31, 2)):
            eX = (1 + (1 - Fr(1, R)) + Fr(1, R)) / 2
            eL = (4 * C + 4 * C * (1 - Fr(1, R)) + 4 * C / R - 2 * E0) / 2
            if eX != 1 or eL != 4 * C - E0:
                fails += 1
            # NEG: (4.43) misread as ||f|| << X0 L^{2C} (no square root)
            eXb = (2 + 2 * (1 - Fr(1, R)) + Fr(1, R)) / 2
            negd += int(eXb != 1)
report("D (4.66) exponents: X0^1 L^{4C-E0} (d0Y)^{1/(2R)}", 'POS', fails, 58 * 6)
report("NEG D ||f|| << X0 L^{2C} (square root dropped)", 'NEG', negd, 58 * 6)
fails = neg = 0
for _ in range(2000):
    Aa = Fr(random.randint(1, 400), random.randint(1, 20))
    C = Fr(random.randint(1, 100), random.randint(1, 20))
    E0 = Aa + 4 * C + 2 + Fr(random.randint(1, 50), random.randint(1, 50))
    if not (-E0 + 4 * C + 1 < -Aa):
        fails += 1
    E0b = Aa + 4 * C + Fr(1, 2)
    neg += int(not (-E0b + 4 * C + 1 <= -Aa))
report("D final: E0 > A+4C+2 => XY L^{-E0+4C+1} << XY L^{-A} (any A > 0)", 'POS', fails, 2000)
report("NEG D final with E0 = A+4C+1/2", 'NEG', neg, 2000)
# (d0Y)^{1/(2R)}: log(d0 Y) <= 2KJ L^0.2 + 2K L^0.2 <= 4K L^0.21 (J = floor(L^0.01)), R = ceil(L^{1/2}/2)
fails = neg = tot = 0
for K in (1, 5, 50, 500):
    worst = 0
    for e in np.linspace(1, 14, 300):
        L = 10.0 ** e
        Jv = math.floor(L ** 0.01)
        R = math.ceil(L ** 0.5 / 2)
        lg = 2 * K * Jv * L ** 0.2 + 2 * K * L ** 0.2
        r = lg / (2 * R)
        worst = max(worst, r)
        tot += 1
        fails += int(r > 4 * K)
        # NEG: no localisation -> (d0YMN)^{1/(2R)} with log(d0YMN) >= L
        neg += int((L + lg) / (2 * R) > 4 * K)
    print(f"   K={K}: max over L in [10,1e14] of log((d0Y)^(1/(2R))) = {worst:.2f} (<= 4K = {4 * K})")
report("D log (d0Y)^{1/(2R)} <= 4K", 'POS', fails, tot)
report("NEG D (d0YMN)^{1/(2R)} (no localisation) bounded by e^{4K}", 'NEG', neg, tot)

print("== SUMMARY")
pos = [r for r in RESULTS if r[1] == 'POS']
negr = [r for r in RESULTS if r[1] == 'NEG']
print(f"positive checks: {len(pos)}, failing: {sum(1 for r in pos if not r[2])}")
print(f"negative controls: {len(negr)}, failing as they must: {sum(1 for r in negr if r[2])}")
unexp = [r[0] for r in RESULTS if not r[2]]
print(f"unexpected outcomes: {len(unexp)} {unexp}")
print(f"wall time {time.time() - T0:.1f} s")
