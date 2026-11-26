#!/usr/bin/env python3
"""Finite / exact checks for LWW (arXiv:2610.20242v2) pp. 48-53: the absolute bounds (4.124)-(4.125), the p. 49
multiplier remark, and the operator-norm bound (4.135) for O_j (O_j^(0) (4.126)-(4.130), O_j^(ind) (4.131)-(4.132)
and the table on p. 52, O_j^(arc) (4.133)-(4.134)).  Companion to notes/parity-attempts/2026-11-26-lww-p48-53-norms.md.

Run: /usr/bin/python3 -I lww_p48_53_norms_check.py     (fractions, numpy, sympy)

(A) p. 49 factorial identities, exact.                         NEG: drop a! (must fail).
(B) weighted Schur test (4.123): ||T||_{L^2(m)} <= sqrt(R C) with the printed R, C, and C(T) = R(T*).
                                                               NEG: ||T|| <= R alone; C with m(t) for m(s).
(C) G_j row / column factors (p. 49), brute force on multisets (symmetric functions), single group, exact.
    Row == exp-partial * (q/th^2 + eta'/(th v0))^h ; column == exp-partial * (q/th^2 + eta' V/(th v0))^h.
    ILLUSTRATION: the un-symmetrised 'append at end' kernel on ordered tuples has column sums with a factor k'
    (exceeds the printed column factor), so the bound needs the symmetric picture (cf. the p. 49 proviso).
(D) (4.124): every z' with det(z,z') = j1 is j1 w_z + h z; at most 16 h; tau identity of p. 50; det(Bk,Bk') =
    det B det(k,k') (4.128).  Line condition p. 52: for j1 != 0 mod p, [j1 w + h z]_p = l fixes h mod p (or is
    impossible).  NEG: j1 = 0 mod p (uniqueness fails).
(E) p. 52 window: an admissible h exists  ==>  || D Z T tau(w)/tau(z) - (D b tau(w)/tau(z) + h*)/p* || <= 16/p*
    (distance to nearest integer).  NEG: the literal absolute value |.| (as printed) fails.
(F) (4.133) congruence count, exhaustive.                      NEG: drop the max(A',B') term.
(G) p. 51 Gram bound and tensor structure: ||[e(xi det(k,k'))]|| = ||T(xi)||^2 (numpy), sum_{|h|<=2A'} min(B',
    1/||h xi||) <= C (A'/d+1)(B'+d log 2d).                     NEG: drop d log(2d) (ratio unbounded).
(H) p. 51 Dirichlet step: theta not in M_1, |v| <= L^{A0}/2  ==> every Dirichlet denominator d > L^{A0};
    |M_1| <= 4 L^{3A0}/Y.                                      NEG: M_1 radius L^{A0}/(4Y).
(I) p. 50 lattice: (4.26) ==> lambda >= Y^{-0.8}; Minkowski lambda <= (2/sqrt3)^{1/2} Y^{-1/2}; box sides
    A' ~ 1/lambda, B' ~ Y lambda (sanity, exact rationals).
(J) bookkeeping (sympy): eps_K, (4.130), (4.134), (4.135) with A0 > A+3, K > 200(A+3); minimal thresholds.
                                                               NEG: K = 200 A; A0 = A.
"""
from fractions import Fraction as F
from itertools import combinations, product as iproduct
from math import factorial, comb, gcd, log, sqrt, floor, ceil
from collections import defaultdict
import random
import time
import numpy as np
import sympy as sp

rng = random.Random(20261126)
nrng = np.random.default_rng(20261126)
T0 = time.time()
RES = []          # (name, kind, n_cases, n_fail, expected_fail)


def report(name, kind, n, nfail, expect_fail=False):
    ok = (nfail > 0) if expect_fail else (nfail == 0)
    RES.append((name, kind, n, nfail, expect_fail, ok))
    tag = 'NEG' if expect_fail else 'POS'
    print(f"[{tag}] {name}: cases={n} failures={nfail} -> {'as expected' if ok else 'UNEXPECTED'}")


# ---------------------------------------------------------------- (A)
n = nf = nneg = 0
for k in range(31):
    for a in range(31):
        n += 1
        if F(comb(k + a, a), factorial(k + a)) != F(1, factorial(k) * factorial(a)):
            nf += 1
        if F(comb(k + a, a) * factorial(a), factorial(k + a)) != F(1, factorial(k)):
            nf += 1
        if F(comb(k + a, a), factorial(k + a)) != F(1, factorial(k)):
            nneg += 1
report("(A) factorial identities p.49", "exact", n, nf)
report("(A) NEG drop a!", "exact", n, nneg, True)

# ---------------------------------------------------------------- (B)
n = nf = nneg1 = nneg2 = nadj = 0
for trial in range(400):
    N = rng.randint(2, 9)
    A = nrng.normal(size=(N, N)) + 1j * nrng.normal(size=(N, N))
    if trial % 3 == 0:                      # column-heavy, to stress asymmetric cases
        A[:, 0] *= 20
    m = nrng.uniform(0.05, 3, N)
    w = nrng.uniform(0.2, 5, N)
    sm = np.sqrt(m)
    M = sm[:, None] * A * sm[None, :]       # matrix of T in an orthonormal basis of L^2(m)
    norm = np.linalg.norm(M, 2)
    R = max(np.sum(np.abs(A[s, :]) * w * m) / w[s] for s in range(N))
    C = max(np.sum(np.abs(A[:, t]) * w * m) / w[t] for t in range(N))
    Astar = A.conj().T                      # kernel of T* w.r.t. m
    Rstar = max(np.sum(np.abs(Astar[s, :]) * w * m) / w[s] for s in range(N))
    n += 1
    if norm > sqrt(R * C) * (1 + 1e-12):
        nf += 1
    if abs(Rstar - C) > 1e-9 * C:
        nadj += 1
    if norm > R * (1 + 1e-12):
        nneg1 += 1
    Cbad = max(np.sum(np.abs(A[:, t]) * w) * m[t] / w[t] for t in range(N))
    if norm > sqrt(R * Cbad) * (1 + 1e-12):
        nneg2 += 1
report("(B) weighted Schur ||T|| <= sqrt(RC)", "numeric", n, nf)
report("(B) C(T) == R(T*)", "numeric", n, nadj)
report("(B) NEG ||T|| <= R alone", "numeric", n, nneg1, True)
report("(B) NEG C with m(t) instead of m(s)", "numeric", n, nneg2, True)


# ---------------------------------------------------------------- (C)
def ms_key(tup):
    return tuple(sorted(tup))


def mu(M, lam):
    """measure of the multiset class: sum over orderings of prod lam / k! = prod lam / prod mult!"""
    r = F(1)
    cnt = defaultdict(int)
    for c in M:
        r *= lam[c[0]]
        cnt[c] += 1
    for v in cnt.values():
        r /= factorial(v)
    return r


def G_out(s, primes, nu, V, q, eta, th, lmax):
    """all (t, |weight|) for ordered source s under G_j (p. 48): remove any subset of matching coords,
    retained matching get q/th^2, removed eta/th each, append l ordered matching pairs (1/l!) prod eta V nu/th."""
    out = []
    match_pos = [i for i, c in enumerate(s) if c[1] == 1]
    for d in range(len(match_pos) + 1):
        for rem in combinations(match_pos, d):
            rems = set(rem)
            ret = tuple(c for i, c in enumerate(s) if i not in rems)
            hret = sum(1 for c in ret if c[1] == 1)
            base = (eta / th) ** d * (q / th ** 2) ** hret
            for l in range(lmax + 1):
                for app in iproduct(primes, repeat=l):
                    wgt = base / factorial(l)
                    for p in app:
                        wgt *= eta * V * nu[p] / th
                    out.append((ret + tuple((p, 1) for p in app), wgt))
    return out


def all_tuples(primes, kmax):
    coords = [(p, ln) for p in primes for ln in (0, 1)]
    res = []
    for k in range(kmax + 1):
        res.extend(iproduct(coords, repeat=k))
    return res


n = nf = 0
illus_viol = 0
for trial in range(12):
    primes = [2, 3] if trial % 2 == 0 else [5]
    nu = {p: F(rng.randint(1, 5), 10 * p) for p in primes}
    lam = nu
    ssum = sum(nu.values())
    V = F(rng.randint(5, 9), 10)
    q = F(rng.randint(1, 6), 10)
    eta = 1 - q
    th = F(rng.randint(6, 9), 10)
    v0 = F(rng.randint(2, 5))
    lmax, kmax = 2, 3
    # ---- row: fixed ordered source s
    for s in all_tuples(primes, 2)[:12]:
        h = sum(1 for c in s if c[1] == 1)
        row = sum(wg * v0 ** (len(t) - len(s)) for t, wg in G_out(s, primes, nu, V, q, eta, th, lmax))
        x = v0 * eta * V * ssum / th
        pred = sum(x ** l / factorial(l) for l in range(lmax + 1)) * (q / th ** 2 + eta / (th * v0)) ** h
        n += 1
        nf += (row != pred)
    # ---- column: symmetric picture (multisets); W(M -> M') from any ordering of M
    W = defaultdict(F)
    sources = {}
    for s in all_tuples(primes, kmax):
        sources.setdefault(ms_key(s), s)
    for Mk, s in sources.items():
        for t, wg in G_out(s, primes, nu, V, q, eta, th, lmax):
            W[(Mk, ms_key(t))] += wg
    for Mp in [ms_key(t) for t in all_tuples(primes, 2)][:12]:
        hp = sum(1 for c in Mp if c[1] == 1)
        col = F(0)
        for Mk in sources:
            if (Mk, Mp) in W and len(Mk) - len(Mp) + 0 <= kmax:
                col += W[(Mk, Mp)] * mu(Mk, lam) / mu(Mp, lam) * v0 ** (len(Mk) - len(Mp))
        # sources with |M| <= kmax only: removal count d <= kmax - (|M'| - l); compare with the d-truncated formula
        x = v0 * eta * ssum / th
        y = q / th ** 2
        z = eta * V / (th * v0)
        pred = F(0)
        # appended multiset part: choose how many of each matching coord type are appended
        cnt = defaultdict(int)
        for c in Mp:
            if c[1] == 1:
                cnt[c] += 1
        types = list(cnt)
        for js in iproduct(*[range(cnt[c] + 1) for c in types]):
            l = sum(js)
            if l > lmax:
                continue
            term = z ** l * y ** (hp - l)
            for c, j in zip(types, js):
                term *= comb(cnt[c], j)
            dmax = kmax - (len(Mp) - l)
            pred += term * sum(x ** d / factorial(d) for d in range(dmax + 1))
        n += 1
        nf += (col != pred)
        # full (untruncated) printed column factor is an upper bound
        full = (F(int(1e6 * float(sum(x ** d / factorial(d) for d in range(40)))), 10 ** 6) + F(1, 10 ** 5)) * (y + z) ** hp
        nf += (col > full)
    # ---- ILLUSTRATION: un-symmetrised ordered column for t = (nonmatching x (k'-1), matching), d = 0, l <= 1
    kp = 6
    t = tuple([(primes[0], 0)] * (kp - 1) + [(primes[0], 1)])
    # l = 0: s = t (retained); l = 1: s = t[:-1], ratio m(s)/m(t) = k' / lam
    col_ord = q / th ** 2 + kp * (eta * V * nu[primes[0]] / th) / lam[primes[0]] / v0
    if col_ord > (q / th ** 2 + eta * V / (th * v0)):
        illus_viol += 1
report("(C) G_j row AND column factors (exact, multiset model)", "exact", n, nf)
print(f"    ILLUSTRATION ordered 'append at end' kernel, k'=6: column exceeds printed factor in {illus_viol}/12 "
      f"parameter sets (so the symmetric picture is needed)")

# ---------------------------------------------------------------- (D)
def egcd_w(z):
    """w with det(z, w) = z1 w2 - z2 w1 = 1"""
    z1, z2 = z
    # solve z1*w2 - z2*w1 = 1
    def ext(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x, y = ext(b, a % b)
        return (g, y, x - (a // b) * y)
    g, x, y = ext(z1, -z2)     # z1*x + (-z2)*y = g
    if g < 0:
        g, x, y = -g, -x, -y
    assert g == 1
    return (y, x)              # w1 = y, w2 = x


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


n = nf = 0
for trial in range(300):
    while True:
        z = (rng.randint(1, 60), rng.randint(-60, 60))
        if gcd(z[0], z[1]) == 1:
            break
    w = egcd_w(z)
    assert det(z, w) == 1
    r = F(rng.randint(0, 99), 100)
    tau = lambda v: v[0] - 2 * r * v[1]
    if tau(z) == 0:
        continue
    j1 = rng.randint(-30, 30)
    # brute force all z' in a box with det(z,z') = j1 ; each must be j1 w + h z
    sols = []
    for a in range(-150, 151):
        for b in range(-150, 151):
            if det(z, (a, b)) == j1:
                zp = (a, b)
                d0 = (zp[0] - j1 * w[0], zp[1] - j1 * w[1])
                # d0 must be an integer multiple of z
                hz = None
                if z[0] != 0 and d0[0] % z[0] == 0 and d0[0] // z[0] * z[1] == d0[1]:
                    hz = d0[0] // z[0]
                if hz is None:
                    nf += 1
                ratio = tau(zp) / tau(z)
                if hz is not None and ratio != hz + j1 * tau(w) / tau(z):
                    nf += 1
                if F(1, 16) <= ratio <= 16:
                    sols.append(zp)
    n += 1
    if len(sols) > 16:
        nf += 1
    # tau identity p. 50
    zp = (rng.randint(-50, 50), rng.randint(-50, 50))
    if tau(zp) != 0:
        if F(zp[1]) / tau(zp) - F(z[1]) / tau(z) != F(det(z, zp)) / (tau(z) * tau(zp)):
            nf += 1
    # (4.128)
    B = [[rng.randint(-9, 9) for _ in range(2)] for _ in range(2)]
    k, kp = (rng.randint(-9, 9), rng.randint(-9, 9)), (rng.randint(-9, 9), rng.randint(-9, 9))
    Bk = (B[0][0] * k[0] + B[0][1] * k[1], B[1][0] * k[0] + B[1][1] * k[1])
    Bkp = (B[0][0] * kp[0] + B[0][1] * kp[1], B[1][0] * kp[0] + B[1][1] * kp[1])
    if det(Bk, Bkp) != (B[0][0] * B[1][1] - B[0][1] * B[1][0]) * det(k, kp):
        nf += 1
report("(D) (4.124) form/count, tau identity, (4.128)", "exact", n, nf)


def line(v, p):
    """[v]_p as a normalised representative in P^1(F_p), or None if v = 0 mod p"""
    a, b = v[0] % p, v[1] % p
    if a == 0 and b == 0:
        return None
    if a != 0:
        return (1, b * pow(a, -1, p) % p)
    return (0, 1)


n = nf = nneg = 0
for p in [2, 3, 5, 7, 11, 13]:
    for trial in range(40):
        while True:
            z = (rng.randint(1, 80), rng.randint(-80, 80))
            if gcd(*z) == 1:
                break
        w = egcd_w(z)
        lines = [(1, c) for c in range(p)] + [(0, 1)]
        for j1 in range(-2 * p, 2 * p + 1):
            for ell in lines:
                hs = [h for h in range(p) if line((j1 * w[0] + h * z[0], j1 * w[1] + h * z[1]), p) == ell]
                n += 1
                if j1 % p != 0:
                    if len(hs) > 1:
                        nf += 1
                    if ell == line(z, p) and hs:
                        nf += 1
                else:
                    if len(hs) > 1:
                        nneg += 1
report("(D) line condition fixes h mod p (j1 != 0 mod p)", "exact", n, nf)
report("(D) NEG j1 = 0 mod p: uniqueness", "exact", n, nneg, True)

# ---------------------------------------------------------------- (E)
n = nf = nneg = 0
smallp = [101, 103, 107, 109, 113, 127]
for trial in range(3000):
    ps = rng.choice(smallp)
    while True:
        z = (rng.randint(1, 400), rng.randint(-400, 400))
        if gcd(*z) == 1:
            break
    w = egcd_w(z)
    r = F(rng.randint(0, 999), 1000)
    tau = lambda v: v[0] - 2 * r * v[1]
    if tau(z) <= 0:
        continue
    Dd = rng.choice([3, 5, 7, 11, 13, 15, 21])
    b = rng.choice([17, 19, 23, 29, 31])
    Z = rng.choice([1, 37, 41, 43])
    T = rng.choice([1, 47, 53, 59, 61])
    j1 = Dd * b - Dd * ps * Z * T
    if j1 % ps == 0:
        continue
    ell = (1, rng.randint(0, ps - 1)) if rng.random() < 0.9 else (0, 1)
    hstar = [h for h in range(ps) if line((j1 * w[0] + h * z[0], j1 * w[1] + h * z[1]), ps) == ell]
    if not hstar:
        continue
    hstar = hstar[0]
    # admissible h: h = hstar (mod p*), tau(z')/tau(z) = h + j1 tau(w)/tau(z) in [1/16, 16]
    c = j1 * tau(w) / tau(z)
    lo, hi = F(1, 16) - c, 16 - c
    nmin = ceil((lo - hstar) / ps)
    exists = (hstar + nmin * ps) <= hi
    X = Dd * Z * T * tau(w) / tau(z) - (Dd * b * tau(w) / tau(z) + hstar) / ps
    distX = abs(X - round(X))
    n += 1
    if exists and distX > F(16, ps):
        nf += 1
    if exists and abs(X) > F(16, ps):
        nneg += 1
report("(E) window: admissible h ==> ||X|| <= 16/p*", "exact", n, nf)
report("(E) NEG literal |X| <= 16/p* (as printed)", "exact", n, nneg, True)

# ---------------------------------------------------------------- (F)
n = nf = nneg = 0
for p in [2, 3, 5, 7, 11]:
    for Ap in range(1, 9):
        for Bp in range(1, 9):
            for a0 in range(p):
                for b0 in range(p):
                    if a0 == 0 and b0 == 0:
                        continue
                    cnt = sum(1 for h in range(-Ap, Ap + 1) for l in range(-Bp, Bp + 1) if (a0 * h + b0 * l) % p == 0)
                    n += 1
                    if cnt > 9 * (F(Ap * Bp, p) + max(Ap, Bp)):
                        nf += 1
                    if cnt > 9 * F(Ap * Bp, p):
                        nneg += 1
report("(F) (4.133) count <= 9(A'B'/p + max(A',B'))", "exact", n, nf)
report("(F) NEG without max(A',B')", "exact", n, nneg, True)

# ---------------------------------------------------------------- (G)
n = nf = 0
maxratio = 0.0
nneg_tensor = 0
for trial in range(60):
    Ap, Bp = rng.randint(2, 7), rng.randint(2, 7)
    xi = rng.random()
    hs = np.arange(-Ap, Ap + 1)
    ks = np.arange(-Bp, Bp + 1)
    T = np.exp(2j * np.pi * xi * np.outer(hs, ks))
    K = [(a, b) for a in hs for b in ks]
    Mdet = np.array([[np.exp(2j * np.pi * xi * (k[0] * kp[1] - k[1] * kp[0])) for kp in K] for k in K])
    n += 1
    nt = np.linalg.norm(T, 2)
    if abs(np.linalg.norm(Mdet, 2) - nt ** 2) > 1e-8 * nt ** 2:
        nf += 1
report("(G) ||[e(xi det)]|| == ||T(xi)||^2", "numeric", n, nf)


def dist(x):
    return abs(x - round(x))


n = nf = nneg = 0
maxr = maxneg = 0.0
for trial in range(4000):
    d = rng.randint(2, 400)
    c = rng.randint(1, d - 1)
    if gcd(c, d) != 1:
        continue
    xi = c / d + rng.uniform(-1, 1) / d ** 2
    Ap = rng.randint(1, 3000)
    Bp = rng.randint(1, 3000)
    S = 0.0
    for h in range(-2 * Ap, 2 * Ap + 1):
        dd = dist(h * xi)
        S += Bp if dd == 0 else min(Bp, 1 / dd)
    bound = (Ap / d + 1) * (Bp + d * log(2 * d))
    maxr = max(maxr, S / bound)
    maxneg = max(maxneg, S / ((Ap / d + 1) * Bp))
    n += 1
    nf += (S > 20 * bound)
    nneg += (S > 20 * (Ap / d + 1) * Bp)
report(f"(G) Gram sum <= 20 (A'/d+1)(B'+d log 2d) [max ratio {maxr:.2f}]", "numeric", n, nf)
report(f"(G) NEG drop d log(2d) [max ratio {maxneg:.1f}]", "numeric", n, nneg, True)

# ---------------------------------------------------------------- (H)
n = nf = nneg = 0
for (Q0, Y) in [(5, 3000), (7, 5000), (4, 1000), (9, 20000)]:
    N = -(-Y // Q0)            # ceil(Y / L^{A0})
    fr = sorted({F(j, k) for k in range(1, Q0 + 1) for j in range(k) if gcd(j, k) == 1})
    meas = sum(F(4 * Q0, Y) for _ in fr)
    n += 1
    nf += (meas > F(4 * Q0 ** 3, Y))

    def in_M1(th, rad):
        return any(min(abs(th - f), 1 - abs(th - f)) <= rad for f in fr)

    for trial in range(1500):
        th = F(rng.randint(0, 10 ** 6 - 1), 10 ** 6)
        v = F(rng.randint(-10 ** 4, 10 ** 4), 10 ** 4) * F(Q0, 2)
        xi = th + v / Y
        if not in_M1(th, F(2 * Q0, Y)):
            n += 1
            for dd in range(1, Q0 + 1):           # any Dirichlet pair with small d would be a failure
                cc = round(xi * dd)
                if abs(xi - F(cc, dd)) <= F(1, dd * N):
                    nf += 1
                    break
        if not in_M1(th, F(Q0, 4 * Y)):
            for dd in range(1, Q0 + 1):
                cc = round(xi * dd)
                if abs(xi - F(cc, dd)) <= F(1, dd * N):
                    nneg += 1
                    break
report("(H) theta not in M_1 ==> Dirichlet d > L^A0 ; |M_1| <= 4L^{3A0}/Y", "exact", n, nf)
report("(H) NEG M_1 radius L^A0/(4Y)", "exact", n, nneg, True)

# ---------------------------------------------------------------- (I)
n = nf = 0
worst = [0, 0, 0]
for trial in range(25):
    Y = rng.choice([2000, 5000, 10000])
    alpha = F(rng.randint(1, 10 ** 6), 10 ** 6 + rng.randint(1, 999))
    good = all(dist(float(k * alpha)) > Y ** -0.7 for k in range(1, int(Y ** 0.2) + 1))
    # Gauss reduction of basis b1 = (0, 1), b2 = (1/Y, alpha) (exact)
    u, v = (F(0), F(1)), (F(1, Y), alpha)
    nrm = lambda x: x[0] ** 2 + x[1] ** 2
    while True:
        if nrm(u) > nrm(v):
            u, v = v, u
        mcoef = round((u[0] * v[0] + u[1] * v[1]) / nrm(u))
        if mcoef == 0:
            break
        v = (v[0] - mcoef * u[0], v[1] - mcoef * u[1])
    lam = sqrt(nrm(u))
    n += 1
    if lam > sqrt(2 / sqrt(3) / Y) * (1 + 1e-12):
        nf += 1
    if sqrt(nrm(u)) * sqrt(nrm(v)) > 2 / sqrt(3) / Y * (1 + 1e-12):
        nf += 1
    if good and lam < Y ** -0.8:
        nf += 1
    # box: points (l/Y, h + l alpha) with |l| <= Y, |h + l alpha| <= 16; coordinates in (u, v)
    detuv = u[0] * v[1] - u[1] * v[0]
    mk1 = mk2 = 0
    for l in range(-Y, Y + 1, max(1, Y // 400)):
        for h in range(floor(-16 - l * alpha), ceil(16 - l * alpha) + 1):
            x = (F(l, Y), h + l * alpha)
            k1 = (x[0] * v[1] - x[1] * v[0]) / detuv
            k2 = (u[0] * x[1] - u[1] * x[0]) / detuv
            mk1, mk2 = max(mk1, abs(k1)), max(mk2, abs(k2))
    worst[0] = max(worst[0], float(mk1) * lam)
    worst[1] = max(worst[1], float(mk2) / (Y * lam))
report(f"(I) lattice: Minkowski, reduced |v1||v2|, (4.26)=>lambda>=Y^-0.8 [box: max|k1|*lam={worst[0]:.1f}, "
       f"max|k2|/(Y lam)={worst[1]:.1f}]", "exact", n, nf)

# ---------------------------------------------------------------- (J)
Lsym, A, K, A0, Cd, c = sp.symbols('L A K A0 Cdag c', positive=True)
n = nf = 0
# eps_K first term: ceil(L^2)(J+1)^{-K} <= 2 L^{2 - 0.01 K}; sqrt -> L^{1 - 0.005 K}; need < L^{-A-2} if K > 200(A+3)
for Av in [1, 2, 5, 6, 10, sp.Rational(7, 2)]:
    Kmin = 200 * (Av + 3)
    for Kv in [Kmin + 1, Kmin + sp.Rational(1, 7), 2 * Kmin]:
        n += 1
        if not (1 - sp.Rational(5, 1000) * Kv < -Av - 2):
            nf += 1
    # second term L^{2K} e^{-L^{0.1}/4} = o(L^{-2A}) ; arc term L^{Cdag} e^{-L^{0.1}/2} = o(L^{-A})
    for expr in [2 * Kmin * sp.log(Lsym) - Lsym ** sp.Rational(1, 10) / 4 + 2 * Av * sp.log(Lsym),
                 30 * Kmin * sp.log(Lsym) - Lsym ** sp.Rational(1, 10) / 2 + Av * sp.log(Lsym)]:
        n += 1
        if sp.limit(expr, Lsym, sp.oo) != -sp.oo:
            nf += 1
    # (4.130): 0.2 - A0 < -A - 2.8 when A0 > A + 3
    n += 1
    if not (sp.Rational(2, 10) - (Av + 3) < -Av - sp.Rational(28, 10) + sp.Rational(1, 10 ** 9)):
        nf += 1
    # Y^{-0.1} log Y with L^{0.1} << log Y <= 2K L^{0.2}: log of it = -0.1 log Y + log log Y -> -oo faster than -A log L
    n += 1
    ly = sp.symbols('ly', positive=True)
    if sp.limit(-ly / 10 + sp.log(ly) + Av * sp.log(ly ** 10), ly, sp.oo) != -sp.oo:
        nf += 1
report("(J) bookkeeping: eps_K, (4.130), (4.134), (4.135) close", "symbolic", n, nf)
nneg = 0
for Av in [1, 2, 5, 6, 10]:
    if not (1 - sp.Rational(5, 1000) * (200 * Av) < -Av):
        nneg += 1
report("(J) NEG K = 200 A (sqrt eps_K not o(L^{-A}))", "symbolic", 5, nneg, True)
nneg = 0
for Av in [1, 2, 5, 6, 10]:
    if not (sp.Rational(2, 10) - Av < -Av):
        nneg += 1
report("(J) NEG A0 = A in (4.130)", "symbolic", 5, nneg, True)
# minimal thresholds actually needed (informative): K > 200(A+1), A0 > A + 0.2
print("    minimal: sqrt(eps_K) = o(L^{-A}) iff 1 - 0.005K < -A iff K > 200(A+1); L^{0.2-A0} = o(L^{-A}) iff A0 > A+0.2")
# size illustration: A = E0 + 5 with E0 = 1, K = 200(A+3)+1 : L with 2K log L < L^{0.1}/4
Av = 6
Kv = 200 * (Av + 3) + 1
lo, hi = 1.0, 1e300
for _ in range(2000):
    mid = sqrt(lo * hi) if hi / lo > 1.0001 else (lo + hi) / 2
    if 2 * Kv * log(mid) < mid ** 0.1 / 4:
        hi = mid
    else:
        lo = mid
print(f"    illustration: E0=1, A=6, K={Kv}: L^(2K) e^(-L^0.1/4) < 1 needs L > {hi:.3g}, i.e. log x > {hi:.3g}")

# ---------------------------------------------------------------- summary
print()
npos = sum(1 for r in RES if not r[4])
nneg = sum(1 for r in RES if r[4])
bad = [r for r in RES if not r[5]]
print(f"SUMMARY: {npos} positive checks, {nneg} negative controls, unexpected outcomes: {len(bad)}")
for r in bad:
    print("   UNEXPECTED:", r[0])
print(f"runtime {time.time() - T0:.1f} s")
