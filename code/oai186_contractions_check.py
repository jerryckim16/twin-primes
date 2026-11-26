#!/usr/bin/python3
"""Rung 186: check of the finite contractions (2.16)-(2.21) of [14] (OpenAI, "Numerical certificate for prime gaps at
most 186", code/third_party/openai186/short_gaps_numerics.pdf, Sec. 2.2, pp. 14-16), written from the PDF only.

WHAT (2.16)-(2.21) ARE.  Not contraction mappings: they DEFINE the three positive source forms
    R_G  (2.17) = 40 Lam sum_r chi_G W sum_eta Q_eta(r) [X^r *] M_{40,eta}                (outer, |F|^2 part of (1.32))
    beta_G (2.19) = (40 h Lam / Z) sum_{l in P} S(v^(l), [X^r *] M_{39,.}; chi_G W)        (inner, (1.30))
    V_G  (2.21) = (40 h^2 Lam / Z) sum_{l in P(0,z_G)} S(v^(l), H; w),  H from C(r) (2.20) (outer, |V_i|^2 part of (1.32))
as finite "contractions" of the 40-variable trial (Q_eta, cap rows v (2.13)) against set-partition moments (2.10)
of coordinate arrays in the marking rings (2.16), with P(u,v) of (2.18) and the face weight w(r).  The implicit
claim is that each form is a valid upper bound for its analytic loss once the coordinate arrays majorise the
event measure (the array majorisations are Lemmas 2.3, 2.4 and (2.8), checked elsewhere).

WHAT IS CHECKED HERE (all exact, fractions.Fraction / int; no floating point in any decision):
 A. Reduced models d = 3, 4 (in place of 40), full enumeration of every cell and every role placement:
    the finite forms (2.10)-(2.21) EQUAL the directly computed normalised integrals
      d*Lam*int chi W |F|^2 [event] / (hZ)^d,
      sum_i int_face chi W [event] sum_{l in P} |V_i^(l)|^2 / (hZ)^d,
      sum_i int chi W(full) w(r_Y) [event incl. erased coordinate] sum_l |V_i^(l)|^2 / (hZ)^d,
    with V_i^(l)(Y) = sum_{s<=l} sum_a chi_s(r+a) h d_s(a) F(Y (+)_i a) computed from the cell values of F,
    for all three marking rings of (2.16) and the plain ring; also (2.13) pointwise and (2.14).
 B. The same identities with the true dimensions d = 40 / 39 and the true factors 40, 40h/Z, 40h^2/Z, on a short
    grid (n_small cells), cells enumerated by orbits (index multisets) and placements over all 40 coordinates.
 C. Prefix claim (2.18)/(2.19): the actual marginal for a face whose largest fragment is M is v^(l(M)), and
    l(M) in P(u,v) whenever M in (u,v]; hence |V|^2 <= sum_{l in P} |v^(l)|^2.
 D. Ring closed forms at d = 40: (1.43), [y](P+yD)^40, [y^3] of the H ring, and the factorial identity behind it.
 E. Full-scale data: (1.27)-(1.28) face multipliers (h_i <= 1, sum_i h_i <= 40), w(r) >= h_i on all 98264 radial
    indices against the masks (1.5), the caps (1.18) -> (1.5)/(1.24), and P(0,z_G), P(q-,q+) for all 6 groups and
    all rank-two bins of Sec. 1.5.1.
 Negative controls (must FAIL): wrong falling factorial, dropped coincident mark, single-shell rows instead of
 prefixes, missing factor h in the normalisation, K^(2) on the erased coordinate, C(r) indexed at r instead of
 r + a, a shifted T0 threshold in w(r), P(u,v) with a non-strict inequality.

usage: /usr/bin/python3 code/oai186_contractions_check.py > code/oai186_contractions_check.out
"""
import sys, time, random, itertools, resource
from fractions import Fraction as Fr
from math import comb, factorial

T_START = time.time()
NCHK = 0
FAILS = []
NEG = []


def check(name, cond):
    global NCHK
    NCHK += 1
    if not cond:
        FAILS.append(name)
        print("FAIL", name, flush=True)
    else:
        print("ok  ", name, flush=True)


def negative(name, cond_that_must_be_false):
    """a negative control: the stated (wrong) identity must NOT hold."""
    global NCHK
    NCHK += 1
    ok = not cond_that_must_be_false
    NEG.append((name, ok))
    print("negative control %-62s %s" % (name, "fails as required" if ok else "DID NOT FAIL (bad)"), flush=True)
    if not ok:
        FAILS.append("negative:" + name)


# ----------------------------------------------------------------------------------------------------------------
# signatures (1.6); the trial in a reduced model uses random integer coefficients c_{sigma,d}
SIGS = [(), (2,), (3,), (4,), (5,), (6,), (2, 2), (2, 3), (2, 4), (3, 3), (2, 2, 2)]
DEG = 6


def set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]


def falling(d, k):
    out = 1
    for i in range(k):
        out *= d - i
    return out


# ---------------- truncated polynomials (lists of length n) and marking rings ----------------
class Model:
    """a reduced grid: n cells, spacing h, profile g, trial coefficients, rings."""

    def __init__(self, n, h, d, seed):
        self.n, self.h, self.d = n, h, d
        rnd = random.Random(seed)
        self.rnd = rnd
        self.t = [(j + Fr(1, 2)) * h for j in range(n)]
        # profile (1.7), exact rationals
        self.g = [Fr(21, 200) / (1 + tj / 100) + Fr(179, 200) / (1 + Fr(907, 5) * tj) for tj in self.t]
        self.Z = sum(x * x for x in self.g)
        self.c = {s: [Fr(rnd.randint(-9, 9), rnd.randint(1, 4)) for _ in range(DEG + 1)] for s in SIGS}

    def x(self, r):                      # radial argument: (r + d/2) h - 9/10, as (r+20)h - 9/10 for d = 40
        return (r + Fr(self.d, 2)) * self.h - Fr(9, 10)

    def p(self, s, r):
        xr = self.x(r)
        return sum(self.c[s][k] * xr ** k for k in range(DEG + 1))

    def Ftilde(self, cell, r=None):
        """polynomial part of the trial on a cell: sum_sigma p_sigma(r) P_sigma(t)."""
        if r is None:
            r = sum(cell)
        tot = 0
        for s in SIGS:
            prod = 1
            for e in s:
                prod *= sum(self.t[j] ** e for j in cell)
            tot += self.p(s, r) * prod
        return tot

    def F(self, cell):
        pr = 1
        for j in cell:
            pr *= self.g[j]
        return pr * self.Ftilde(cell)


RINGS = {
    # name: (variable limits, role monomials, extracted target)    -- (2.16) and the plain cap ring
    "plain": ((), [()], ()),
    "L": ((1,), [(0,), (1,)], (1,)),                 # P + yD (mod y^2), [y]
    "P": ((1, 1), [(0, 0), (1, 0), (0, 1), (1, 1)], (1, 1)),   # P + xA + yB + xyC (mod x^2, y^2), [xy]
    "H": ((3,), [(0,), (1,), (2,), (3,)], (3,)),     # F0 + yF1 + y^2F2 + y^3F3 (mod y^4), [y^3]
}


def madd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mok(m, lim):
    return all(x <= l for x, l in zip(m, lim))


class Ring:
    def __init__(self, name, n):
        self.lim, self.roles, self.target = RINGS[name]
        self.zero = tuple(0 for _ in self.lim)
        self.n = n

    def pmul(self, a, b):
        n = self.n
        out = [0] * n
        for i, ai in enumerate(a):
            if ai:
                for j in range(n - i):
                    if b[j]:
                        out[i + j] += ai * b[j]
        return out

    def mul(self, A, B):
        out = {}
        for m1, p1 in A.items():
            for m2, p2 in B.items():
                m = madd(m1, m2)
                if mok(m, self.lim):
                    q = self.pmul(p1, p2)
                    if m in out:
                        out[m] = [u + v for u, v in zip(out[m], q)]
                    else:
                        out[m] = q
        return out

    def one(self):
        return {self.zero: [1] + [0] * (self.n - 1)}

    def power(self, A, k):
        out = self.one()
        for _ in range(k):
            out = self.mul(out, A)
        return out

    def scale(self, A, c):
        return {m: [c * x for x in p] for m, p in A.items()}

    def add(self, A, B):
        out = {m: list(p) for m, p in A.items()}
        for m, p in B.items():
            if m in out:
                out[m] = [u + v for u, v in zip(out[m], p)]
            else:
                out[m] = list(p)
        return out


def power_sum(ring, model, K, e):
    """P_e[K](X) = sum_j K_j t_j^e X^j, K = {role monomial: array}."""
    return {m: [K[m][j] * model.t[j] ** e for j in range(model.n)] for m in K}


def moments(ring, model, K, d, etas, falling_fn=falling):
    """M_{d,eta}[K] by the set-partition formula (2.10), for every eta in etas; returns {eta: ring element}."""
    PS = {}

    def P(e):
        if e not in PS:
            PS[e] = power_sum(ring, model, K, e)
        return PS[e]
    pw = {}

    def P0pow(k):
        if k not in pw:
            pw[k] = ring.power(P(0), k)
        return pw[k]
    out = {}
    for eta in etas:
        tot = {}
        for pi in set_partitions(list(range(len(eta)))):
            k = len(pi)
            if k > d:
                continue
            term = P0pow(d - k)
            for B in pi:
                term = ring.mul(term, P(sum(eta[i] for i in B)))
            tot = ring.add(tot, ring.scale(term, falling_fn(d, k)))
        out[eta] = tot
    return out


def all_etas():
    return sorted({tuple(sorted(s + t)) for s in SIGS for t in SIGS})


def Q_eta(model, r):
    Q = {}
    for s in SIGS:
        for t in SIGS:
            eta = tuple(sorted(s + t))
            Q[eta] = Q.get(eta, 0) + model.p(s, r) * model.p(t, r)
    return Q


def sub_signatures(s):
    """(2.13): labelled subsets A of sigma, returns list of (e(A), sigma minus A) with multiplicity per labelled subset."""
    out = []
    L = len(s)
    for mask in range(1 << L):
        A = [s[i] for i in range(L) if mask >> i & 1]
        rest = tuple(sorted(s[i] for i in range(L) if not mask >> i & 1))
        out.append((sum(A), rest))
    return out


def cap_rows(model, chis, ds, gweight=True):
    """v_{s,tau}(r) of (2.13); chis[s](r) in {0,1}, ds[s][a] = d_{c_s}(a).  Returns rows[s][tau] = list over r."""
    n = model.n
    rows = []
    for s in range(len(chis)):
        R = {t: [0] * n for t in SIGS}
        for sig in SIGS:
            for eA, tau in sub_signatures(sig):
                for r in range(n):
                    acc = 0
                    for a in range(n - r):
                        if chis[s](r + a):
                            xa = model.x(r + a)
                            pa = sum(model.c[sig][k] * xa ** k for k in range(DEG + 1))
                            acc += pa * (model.g[a] if gweight else 1) * ds[s][a] * model.t[a] ** eA
                    R[tau][r] += acc
        rows.append(R)
    return rows


def prefix_rows(rows, l):
    n = len(rows[0][()])
    return {t: [sum(rows[s][t][r] for s in range(l)) for r in range(n)] for t in SIGS}


def S_pair(v, M, A, n):
    """(2.14): S(v, M; A) = sum_r A(r) sum_{tau,ups} v_tau(r) v_ups(r) M_{tau u ups}(r); M[eta][r] numbers."""
    tot = 0
    for r in range(n):
        if A(r) == 0:
            continue
        acc = 0
        for t in SIGS:
            if v[t][r] == 0:
                continue
            for u in SIGS:
                acc += v[t][r] * v[u][r] * M[tuple(sorted(t + u))][r]
        tot += A(r) * acc
    return tot


def placements(d, ring):
    """all assignments coordinate -> role monomial with total mark = target; as tuples of (coord, monomial) for the
    nonzero monomials (all other coordinates take the zero monomial)."""
    nz = [m for m in ring.roles if m != ring.zero]
    res = []

    def rec(start, rem, cur):
        if all(x == 0 for x in rem):
            res.append(tuple(cur))
            return
        for i in range(start, d):
            for m in nz:
                if all(a <= b for a, b in zip(m, rem)):
                    rec(i + 1, tuple(b - a for a, b in zip(m, rem)), cur + [(i, m)])
    rec(0, ring.target, [])
    return res


def cell_event_weight(cell, kappa, ring, pls):
    """sum over role placements of prod_k kappa[role_k][j_k] (raw arrays: cell mass / h, no profile)."""
    base = 1
    for j in cell:
        base *= kappa[ring.zero][j]
    tot = 0
    for pl in pls:
        w = base
        for (i, m) in pl:
            w = w * kappa[m][cell[i]] / kappa[ring.zero][cell[i]]
        tot += w
    return tot


# ================================================================================================================
def run_model_explicit(dim, n, seed, ringname, Pset, neg=False):
    """Part A: full enumeration of cells and placements, d = dim (outer) and dim-1 (inner face)."""
    h = Fr(1, 10)
    M = Model(n, h, dim, seed)
    rnd = M.rnd
    ring = Ring(ringname, n)
    Lam = Fr(rnd.randint(1, 9), rnd.randint(1, 9))
    # raw positive event arrays (cell mass / h) per role, same for every coordinate (symmetric kernels)
    kappa = {m: [Fr(rnd.randint(1, 30), rnd.randint(1, 30)) for _ in range(n)] for m in ring.roles}
    K2 = {m: [M.g[j] ** 2 * kappa[m][j] / M.Z for j in range(n)] for m in ring.roles}     # profile power 2
    K0 = {m: list(kappa[m]) for m in ring.roles}                                      # profile power 0, Z_0 = 1
    chiW = [Fr(rnd.randint(0, 5), rnd.randint(1, 3)) if rnd.random() < 0.8 else 0 for _ in range(n)]
    wface = [Fr(rnd.randint(1, 7), 7) for _ in range(n)]
    # outer caps: three shells (consecutive radial ranges) with their own cap arrays d_s(a)
    b1, b2 = n // 3, (2 * n) // 3
    chis = [lambda r: 1 if r < b1 else 0, lambda r: 1 if b1 <= r < b2 else 0, lambda r: 1 if r >= b2 else 0]
    ds = [[Fr(rnd.randint(1, 20), 20) for _ in range(n)] for _ in range(3)]
    etas = all_etas()
    tgt = ring.target
    out = {}
    hZ = M.h * M.Z

    # ---- R: (2.17) with d = dim ----
    d = dim
    Mo = moments(ring, M, K2, d, etas)
    R_form = 0
    for r in range(n):
        if chiW[r]:
            Q = Q_eta(M, r)
            R_form += chiW[r] * sum(Q[e] * Mo[e].get(tgt, [0] * n)[r] for e in etas)
    R_form *= d * Lam
    pls_d = placements(d, ring)
    R_true = 0
    for cell in itertools.product(range(n), repeat=d):
        r = sum(cell)
        if r >= n or not chiW[r]:
            continue
        evw = cell_event_weight(cell, kappa, ring, pls_d) * M.h ** d       # event measure of the cell
        R_true += chiW[r] * M.F(cell) ** 2 * evw
    R_true = d * Lam * R_true / hZ ** d          # face multipliers <= 1, d faces
    check("A.R(2.17) d=%d ring=%s seed=%d" % (d, ringname, seed), R_form == R_true and R_true != 0)
    out["R"] = (R_form, R_true)
    if neg:
        Mbad = moments(ring, M, K2, d, etas, falling_fn=lambda dd, k: dd ** k)
        Rb = 0
        for r in range(n):
            if chiW[r]:
                Q = Q_eta(M, r)
                Rb += chiW[r] * sum(Q[e] * Mbad[e].get(tgt, [0] * n)[r] for e in etas)
        negative("(2.10) with d^|pi| instead of (d)_|pi| [d=%d,%s]" % (d, ringname), d * Lam * Rb == R_true)

    # ---- cap rows (2.13): pointwise identity for the erased marginal ----
    rows = cap_rows(M, chis, ds)
    dm = dim - 1
    faces = list(itertools.product(range(n), repeat=dm))
    Vtrue = {}
    for Y in faces:
        rY = sum(Y)
        if rY >= n:
            continue
        for l in (1, 2, 3):
            for i in range(dim):            # insert the erased coordinate at every position i
                val = 0
                for s in range(l):
                    for a in range(n - rY):
                        if chis[s](rY + a):
                            full = Y[:i] + (a,) + Y[i:]
                            val += M.h * ds[s][a] * M.F(full)
                Vtrue[(Y, l, i)] = val
    ok = True
    for l in (1, 2, 3):
        v = prefix_rows(rows, l)
        for Y in faces:
            rY = sum(Y)
            if rY >= n:
                continue
            gY = 1
            for j in Y:
                gY *= M.g[j]
            pred = M.h * gY * sum(v[t][rY] * _Psig(M, Y, t) for t in SIGS)
            for i in range(dim):
                ok &= (pred == Vtrue[(Y, l, i)])
    check("A.(2.13) erased marginal rows, all faces/positions/prefixes d=%d seed=%d" % (dim, seed), ok)

    # ---- beta: (2.19) with face dimension dim-1 and 'dim' faces ----
    Mi = moments(ring, M, K2, dm, etas)
    Mi_num = {e: Mi[e].get(tgt, [0] * n) for e in etas}
    beta_form = 0
    for l in Pset:
        beta_form += S_pair(prefix_rows(rows, l), Mi_num, lambda r: chiW[r], n)
    beta_form *= dim * M.h * Lam / M.Z
    pls_dm = placements(dm, ring)
    beta_true = 0
    for Y in faces:
        rY = sum(Y)
        if rY >= n or not chiW[rY]:
            continue
        evw = cell_event_weight(Y, kappa, ring, pls_dm) * M.h ** dm
        for i in range(dim):
            beta_true += chiW[rY] * evw * sum(Vtrue[(Y, l, i)] ** 2 for l in Pset)
    beta_true = Lam * beta_true / hZ ** dim
    check("A.beta(2.19) d=%d ring=%s P=%s seed=%d" % (dim, ringname, Pset, seed), beta_form == beta_true and beta_true != 0)
    if neg:
        bb = 0
        for l in Pset:
            bb += S_pair({t: rows[l - 1][t] for t in SIGS}, Mi_num, lambda r: chiW[r], n)
        bb *= dim * M.h * Lam / M.Z
        negative("(2.19) with single-shell rows v_l instead of prefix v^(l) [d=%d]" % dim, bb == beta_true)
        negative("(2.19) normalised by 40/Z instead of 40h/Z [d=%d]" % dim, beta_form / M.h == beta_true)

    # ---- V: (2.20)-(2.21) ----
    # C(r) = sum_a chi W(r+a) K^(0)_a  (ring element of the marks, a number per monomial)
    def Cvec(r, K, shift=True):
        return {m: sum((chiW[r + a] if shift else chiW[r]) * K[m][a] for a in range(n - r)) for m in ring.roles}

    def Hrows(K, shift=True):
        H = {e: [0] * n for e in etas}
        for r in range(n):
            C = Cvec(r, K, shift)
            for e in etas:
                acc = 0
                for m1, c1 in C.items():
                    for m2, p2 in Mi[e].items():
                        if madd(m1, m2) == tgt:
                            acc += c1 * p2[r]
                H[e][r] = acc
        return H
    H = Hrows(K0)
    V_form = 0
    for l in Pset:
        V_form += S_pair(prefix_rows(rows, l), H, lambda r: wface[r], n)
    V_form *= dim * M.h ** 2 * Lam / M.Z
    V_true = 0
    for Y in faces:
        rY = sum(Y)
        if rY >= n:
            continue
        for i in range(dim):
            Vsq = sum(Vtrue[(Y, l, i)] ** 2 for l in Pset)
            for a in range(n - rY):
                if not chiW[rY + a]:
                    continue
                full = Y[:i] + (a,) + Y[i:]
                evw = cell_event_weight(full, kappa, ring, pls_d) * M.h ** dim
                V_true += chiW[rY + a] * wface[rY] * evw * Vsq
    V_true = Lam * V_true / hZ ** dim
    check("A.V(2.21) d=%d ring=%s P=%s seed=%d" % (dim, ringname, Pset, seed), V_form == V_true and V_true != 0)
    if neg:
        Hb = Hrows(K2)
        Vb = sum(S_pair(prefix_rows(rows, l), Hb, lambda r: wface[r], n) for l in Pset) * dim * M.h ** 2 * Lam / M.Z
        negative("(2.20) with profile power 2 on the erased coordinate [d=%d,%s]" % (dim, ringname), Vb == V_true)
        Hc = Hrows(K0, shift=False)
        Vc = sum(S_pair(prefix_rows(rows, l), Hc, lambda r: wface[r], n) for l in Pset) * dim * M.h ** 2 * Lam / M.Z
        negative("(2.20) with chi W(r) instead of chi W(r+a) [d=%d,%s]" % (dim, ringname), Vc == V_true)
        if ringname == "P":
            # drop the coincident-mark role C (xy on one coordinate) from the moments only
            K2b = dict(K2)
            K2b[(1, 1)] = [0] * n
            Mob = moments(ring, M, K2b, d, etas)
            Rb = d * Lam * sum(chiW[r] * sum(Q_eta(M, r)[e] * Mob[e].get(tgt, [0] * n)[r] for e in etas)
                               for r in range(n) if chiW[r])
            negative("(2.16) P-ring without coincident marks C [d=%d]" % d, Rb == R_true)
    return out


def _Psig(M, cell, s):
    prod = 1
    for e in s:
        prod *= sum(M.t[j] ** e for j in cell)
    return prod


# ================================================================================================================
def partitions_upto(r, kmax):
    """multisets of positive parts summing to r with at most kmax parts (as nonincreasing tuples)."""
    def rec(rem, maxp, k):
        if rem == 0:
            yield ()
            return
        if k == 0:
            return
        for p in range(min(rem, maxp), 0, -1):
            for rest in rec(rem - p, p, k - 1):
                yield (p,) + rest
    return list(rec(r, r, kmax))


def orbit_cells(n, d):
    """representatives (sorted index tuples of length d, sum < n) with orbit sizes."""
    out = []
    for r in range(n):
        for part in partitions_upto(r, d):
            cell = tuple(sorted(part + (0,) * (d - len(part))))
            cnt = {}
            for j in cell:
                cnt[j] = cnt.get(j, 0) + 1
            size = factorial(d)
            for v in cnt.values():
                size //= factorial(v)
            out.append((cell, size))
    return out


def run_model_40(n, seed, ringname, Pset):
    """Part B: the true dimensions 40 (outer) / 39 (inner face) on a short grid; Sum_i over faces by symmetry
    (verified explicitly in Part A)."""
    dim = 40
    h = Fr(1, 10)
    M = Model(n, h, dim, seed)
    rnd = M.rnd
    ring = Ring(ringname, n)
    Lam = Fr(rnd.randint(1, 9), rnd.randint(1, 9))
    kappa = {m: [Fr(rnd.randint(1, 30), rnd.randint(1, 30)) for _ in range(n)] for m in ring.roles}
    K2 = {m: [M.g[j] ** 2 * kappa[m][j] / M.Z for j in range(n)] for m in ring.roles}
    K0 = {m: list(kappa[m]) for m in ring.roles}
    chiW = [Fr(rnd.randint(1, 5), rnd.randint(1, 3)) for _ in range(n)]
    wface = [Fr(rnd.randint(1, 7), 7) for _ in range(n)]
    b1, b2 = n // 3, (2 * n) // 3
    chis = [lambda r: 1 if r < b1 else 0, lambda r: 1 if b1 <= r < b2 else 0, lambda r: 1 if r >= b2 else 0]
    ds = [[Fr(rnd.randint(1, 20), 20) for _ in range(n)] for _ in range(3)]
    etas = all_etas()
    tgt = ring.target
    hZ = M.h * M.Z
    pls40 = placements(40, ring)
    pls39 = placements(39, ring)
    # R
    Mo = moments(ring, M, K2, 40, etas)
    R_form = 40 * Lam * sum(chiW[r] * sum(Q_eta(M, r)[e] * Mo[e].get(tgt, [0] * n)[r] for e in etas) for r in range(n))
    R_true = 0
    for cell, size in orbit_cells(n, 40):
        r = sum(cell)
        R_true += size * chiW[r] * M.F(cell) ** 2 * cell_event_weight(cell, kappa, ring, pls40) * M.h ** 40
    R_true = 40 * Lam * R_true / hZ ** 40
    check("B.R(2.17) d=40 ring=%s seed=%d" % (ringname, seed), R_form == R_true and R_true != 0)
    # erased marginal, beta, V
    rows = cap_rows(M, chis, ds)
    Mi = moments(ring, M, K2, 39, etas)
    Mi_num = {e: Mi[e].get(tgt, [0] * n) for e in etas}
    faces = orbit_cells(n, 39)
    Vtrue = {}
    ok = True
    for Y, size in faces:
        rY = sum(Y)
        gY = 1
        for j in Y:
            gY *= M.g[j]
        for l in (1, 2, 3):
            val = 0
            for s in range(l):
                for a in range(n - rY):
                    if chis[s](rY + a):
                        val += M.h * ds[s][a] * M.F(Y + (a,))
            Vtrue[(Y, l)] = val
            v = prefix_rows(rows, l)
            ok &= (val == M.h * gY * sum(v[t][rY] * _Psig(M, Y, t) for t in SIGS))
    check("B.(2.13) erased marginal rows d=40 seed=%d" % seed, ok)
    beta_form = 40 * M.h * Lam / M.Z * sum(S_pair(prefix_rows(rows, l), Mi_num, lambda r: chiW[r], n) for l in Pset)
    beta_true = 0
    for Y, size in faces:
        rY = sum(Y)
        beta_true += size * 40 * chiW[rY] * cell_event_weight(Y, kappa, ring, pls39) * M.h ** 39 * \
            sum(Vtrue[(Y, l)] ** 2 for l in Pset)
    beta_true = Lam * beta_true / hZ ** 40
    check("B.beta(2.19) d=40 ring=%s P=%s seed=%d" % (ringname, Pset, seed), beta_form == beta_true and beta_true != 0)
    negative("(2.19) with 40/Z instead of 40h/Z at d=40 [%s]" % ringname, beta_form / M.h == beta_true)
    H = {e: [0] * n for e in etas}
    for r in range(n):
        C = {m: sum(chiW[r + a] * K0[m][a] for a in range(n - r)) for m in ring.roles}
        for e in etas:
            H[e][r] = sum(c1 * p2[r] for m1, c1 in C.items() for m2, p2 in Mi[e].items() if madd(m1, m2) == tgt)
    V_form = 40 * M.h ** 2 * Lam / M.Z * sum(S_pair(prefix_rows(rows, l), H, lambda r: wface[r], n) for l in Pset)
    V_true = 0
    for Y, size in faces:
        rY = sum(Y)
        Vsq = sum(Vtrue[(Y, l)] ** 2 for l in Pset)
        for a in range(n - rY):
            full = Y + (a,)
            V_true += size * 40 * chiW[rY + a] * wface[rY] * cell_event_weight(full, kappa, ring, pls40) * \
                M.h ** 40 * Vsq
    V_true = Lam * V_true / hZ ** 40
    check("B.V(2.21) d=40 ring=%s P=%s seed=%d" % (ringname, Pset, seed), V_form == V_true and V_true != 0)
    negative("(2.21) with 40h/Z instead of 40h^2/Z at d=40 [%s]" % ringname, V_form / M.h == V_true)


# ================================================================================================================
def part_C():
    """(2.18) and the prefix claim: actual marginal = v^(l(M)), l(M) in P(u,v) for M in (u,v]."""
    rnd = random.Random(7)
    nchk = 0
    ok = True
    neg_found = False
    for trial in range(4000):
        c = sorted([Fr(rnd.randint(1, 400), 7) for _ in range(3)], reverse=True)
        if len(set(c)) < 3:
            continue
        cs = c + [Fr(0)]                                  # c_1 > c_2 > c_3, c_4 := 0
        u = Fr(rnd.randint(0, 450), 7)
        v = u + Fr(rnd.randint(1, 450), 7)
        if v > cs[0]:
            v = cs[0]
        if not u < v:
            continue
        P = {l for l in (1, 2, 3) if max(u, cs[l]) < min(v, cs[l - 1])}
        Pbad = {l for l in (1, 2, 3) if max(u, cs[l]) <= min(v, cs[l - 1])}
        # sample largest fragments M in (u, v], including the endpoints v and the cap values
        cand = [v] + [x for x in cs if u < x <= v] + [u + (v - u) * Fr(k, 13) for k in range(1, 13)]
        for Mf in cand:
            # shells s allowed for a face of largest fragment Mf: c_s >= Mf
            allowed = [s for s in (1, 2, 3) if cs[s - 1] >= Mf]
            l = max(allowed)                              # = l with Mf in (c_{l+1}, c_l]
            nchk += 1
            ok &= (allowed == list(range(1, l + 1)))       # the actual marginal is a PREFIX sum v^(l)
            ok &= (cs[l] < Mf <= cs[l - 1])
            ok &= (l in P)
        # P is not larger than needed: every l in P is attained
        for l in P:
            lo, hi = max(u, cs[l]), min(v, cs[l - 1])
            ok &= any(lo < Mf <= hi for Mf in [hi])
        if Pbad != P:
            neg_found = True
    check("C.(2.18) prefix and P(u,v) membership, %d (caps,interval,M) cases" % nchk, ok)
    negative("(2.18) with <= instead of < gives the same P on all cases", not neg_found)
    # numeric form of the bound |sum_{s<=l*} v_s|^2 <= sum_{l in P} |v^(l)|^2 (squares nonnegative)
    ok2 = True
    for trial in range(2000):
        vs = [Fr(rnd.randint(-50, 50), rnd.randint(1, 9)) for _ in range(3)]
        P = sorted(rnd.sample([1, 2, 3], rnd.randint(1, 3)))
        lstar = rnd.choice(P)
        act = sum(vs[:lstar])
        ok2 &= act ** 2 <= sum(sum(vs[:l]) ** 2 for l in P)
    check("C. actual prefix square <= sum of prefix squares over P (2000 random cases)", ok2)


def part_D():
    """ring closed forms with d = 40, symbolically in sympy, and the factorial identity behind [y^3]."""
    import sympy as sp
    P, A, B, C, D, y, x = sp.symbols("P A B C D y x")
    F0, F1, F2, F3 = sp.symbols("F0 F1 F2 F3")
    e = sp.expand((P + x * A + y * B + x * y * C) ** 40)
    xy = e.coeff(x, 1).coeff(y, 1)
    check("D.(1.43) [xy]Q^40 = 40 P^39 C + 1560 P^38 A B", sp.expand(xy - (40 * P ** 39 * C + 40 * 39 * P ** 38 * A * B)) == 0)
    eL = sp.expand((P + y * D) ** 40).coeff(y, 1)
    check("D.[y](P+yD)^40 = 40 P^39 D (one designated coordinate)", sp.expand(eL - 40 * P ** 39 * D) == 0)
    eH = sp.expand((F0 + y * F1 + y ** 2 * F2 + y ** 3 * F3) ** 40).coeff(y, 3)
    want = 40 * F0 ** 39 * F3 + 40 * 39 * F0 ** 38 * F1 * F2 + comb(40, 3) * F0 ** 37 * F1 ** 3
    check("D.[y^3] H ring at d=40 = 40F0^39F3 + 1560F0^38F1F2 + 9880F0^37F1^3", sp.expand(eH - want) == 0)
    # [y^3] prod_i sum_a C(N_i,a) y^a = C(sum N_i, 3) >= 1[sum N_i >= 3]  (factorial weights of (2.8), (1.47))
    rnd = random.Random(11)
    ok = True
    for _ in range(300):
        N = [rnd.choice([0, 0, 0, 1, 1, 2, 3, 5]) for _ in range(40)]
        poly = [1]
        for Ni in N:
            f = [comb(Ni, a) for a in range(4)]
            new = [0] * 4
            for i, pi in enumerate(poly):
                for a in range(4 - i):
                    new[i + a] += pi * f[a]
            poly = new
        ok &= poly[3] == comb(sum(N), 3) and comb(sum(N), 3) >= (1 if sum(N) >= 3 else 0)
    check("D. [y^3] of factorial marks = C(sum N,3) >= 1[N>=3], 300 random 40-vectors", ok)


def part_E():
    """full-scale exact data checks."""
    Npts = 98304
    n = Npts - 40
    g0, Omo = Fr(1, 10 ** 7), Fr(12499, 10 ** 6)
    rho = Fr(1, 4) + Omo
    rhos = rho - g0
    S = Fr(2742997, 10 ** 7) / rhos
    T1 = Fr(251, 1000) / rhos
    T0 = 2 - Fr(3, 1000) - S
    e = g0 / rho
    zeta = Fr(19037, 100000) / rho
    check("E.(1.13) vs (1.1): rho* = 2624989/10^7, S, T0, T1 agree",
          rhos == Fr(2624989, 10 ** 7) and S == Fr(2742997, 2624989) and T0 == Fr(2499106033, 2624989000)
          and T1 == Fr(2510000, 2624989))
    h = S / Npts
    # (1.27)-(1.28)
    kdef = Fr(1, 50000)
    m0 = 1 - kdef
    Kex, lam = Fr(17, 50), Fr(1, 125)
    ah = m0 ** 2 - m0 * lam
    bh = (1 - m0 / lam) * kdef * Kex
    d0 = 1 - ah - bh
    check("E.(1.28) a_h, b_h, d_0, 1-b_h", ah == Fr(2479900401, 2500000000) and bh == Fr(-843183, 10 ** 9)
          and d0 == Fr(44415113, 5000000000) and 1 - bh == Fr(1000843183, 10 ** 9) and d0 + ah == 1 - bh)
    mx = max(abs(ah + bh), abs(bh))
    check("E.(1.31) face multipliers 0 < |b_h| <= max{|a_h+b_h|,|b_h|} <= 1, so sum_i h_i <= 40 (factor in 2.17)",
          0 < abs(bh) <= mx <= 1)
    # caps (1.18) -> (1.5), (1.24)
    fl = lambda z: (z / h).__floor__()
    caps = {
        "outer": [fl(zeta), fl((S + e) / 2), fl(S + e / 2 - 23 * (T1 + e / 2) / 40)],
        "base": [fl(zeta), fl((T0 + e) / 2), fl(63 * (T0 + e / 2) / 160)],
        "enlarged": [fl(zeta), fl((T1 + e) / 2), fl(63 * (T1 + e / 2) / 160)],
    }
    want = {"outer": [68225, 49152, 46580], "base": [68225, 44781, 35265], "enlarged": [68225, 44976, 35419]}
    for k in caps:
        check("E.(1.18) caps h*floor(z/h) for %s = %s" % (k, want[k]), caps[k] == want[k])
    print("  caps (1.18)/h floors:", caps)
    # masks (1.5): (lo, hi, cap/h)
    base_end, enl_end = 89524, 89914
    check("E.(1.19) mask ends: floor(T0/h)-39 = 89524, floor(T1/h)-39 = 89914, outer end min(98263, S/h-40) = 98263",
          fl(T0) - 39 == base_end and fl(T1) - 39 == enl_end and min(98263, fl(S) - 40) == n - 1)
    print("  floor(T0/h) = %d, floor(T1/h) = %d, floor(S/h) = %d" % (fl(T0), fl(T1), fl(S)))

    # w(r) >= h_i(Y) on every retained radial index (39 coordinates, index sum r < n)
    def w_of(r, T0x=T0):
        R = (r + 39) * h
        if R <= T0x:
            return Fr(1)
        if R <= T1:
            return mx
        return abs(bh)

    def h_upper(r):
        # h_i(Y) as a function of the cell's radial index: 1 if the cell can lie in H0, mx if it can lie in H1\H0,
        # |b_h| otherwise; caps only shrink H0, H1, so this is the maximum of h_i over cells of index sum r
        if r <= base_end:
            return Fr(1)
        if r <= enl_end:
            return mx
        return abs(bh)
    bad = [r for r in range(n) if w_of(r) < h_upper(r)]
    check("E. w(r) >= h_i(Y) for all %d radial indices of a 39-face (masks (1.5))" % n, not bad)
    first_lt1 = next(r for r in range(n) if w_of(r) < 1)
    first_bh = next(r for r in range(n) if w_of(r) == abs(bh))
    print("  w(r) < 1 first at r = %d (H0 ends at %d); w = |b_h| first at r = %d (H1 ends at %d)"
          % (first_lt1, base_end, first_bh, enl_end))
    check("E. w(r) is exactly the radial envelope of h_i (no slack): switch points 89525, 89915",
          first_lt1 == base_end + 1 and first_bh == enl_end + 1)
    badneg = [r for r in range(n) if w_of(r, T0 - 50 * h) < h_upper(r)]
    negative("w(r) with T0 - 50h in place of T0 still dominates h_i", not badneg)

    # P(u,v), (2.18), for all groups and all rank-two bins of Sec. 1.5.1
    c = [68225 * h, 49152 * h, 46580 * h, Fr(0)]

    def Pset(u, v):
        return {l for l in (1, 2, 3) if max(u, c[l]) < min(v, c[l - 1])}
    groups = {   # name: (m, U, z/h, T-list, inner?)
        "O2": (Fr(2), S + e, 49152, [Fr(j, 6) for j in range(7)], False),
        "O5/2": (Fr(5, 2), S + e / 2, 46580, [Fr(j, 16) for j in range(9)] + [Fr(5, 8), Fr(3, 4), Fr(7, 8), Fr(1)], False),
        "I2old": (Fr(2), T0 + e, 44781, [Fr(0), Fr(1)], True),
        "I5/2old": (Fr(5, 2), T0 + e / 2, 35265, [Fr(0), Fr(1, 2), Fr(1)], True),
        "I2new": (Fr(2), T1 + e, 44976, [Fr(0), Fr(1, 6), Fr(1, 2), Fr(2, 3), Fr(1)], True),
        "I5/2new": (Fr(5, 2), T1 + e / 2, 35419, [Fr(0), Fr(1, 8), Fr(3, 8), Fr(1, 2), Fr(3, 4), Fr(1)], True),
    }
    expectP0 = {"O2": {2, 3}, "O5/2": {3}, "I2old": {3}, "I5/2old": {3}, "I2new": {3}, "I5/2new": {3}}
    nbins = 0
    for G, (m, U, zh, T, inner) in groups.items():
        z = zh * h
        P0 = Pset(Fr(0), z)
        check("E.(2.18) P(0,z_G) for %s = %s" % (G, sorted(expectP0[G])), P0 == expectP0[G] and z <= c[0])
        q0 = U / (m + 1)
        for a, b in zip(T, T[1:]):
            qm, qp = q0 + a * (z - q0), q0 + b * (z - q0)
            nbins += 1
            Pq = Pset(qm, qp)
            check("E.(2.18) bin (%s,%s] of %s: 0<q-<q+<=z_G<=c_1, nonempty P(q-,q+) subset of P(0,z_G)" % (a, b, G),
                  0 < qm < qp <= z <= c[0] and Pq and Pq <= P0)
            if inner:
                print("  %s rank-two bin T=(%s,%s]: q-/h = %.3f, q+/h = %.3f, P(q-,q+) = %s"
                      % (G, a, b, float(qm / h), float(qp / h), sorted(Pq)))
    print("  rank-two bins examined: %d (expected 6+12+1+2+4+5 = 30)" % nbins)
    check("E. 30 rank-two bins", nbins == 30)


def main():
    print("oai186_contractions_check.py -- exact checks of (2.16)-(2.21) of [14]; python", sys.version.split()[0])
    print("== Part E: full-scale data ==", flush=True)
    part_E()
    print("== Part D: ring closed forms at d = 40 ==", flush=True)
    part_D()
    print("== Part C: prefix marginals and P(u,v) ==", flush=True)
    part_C()
    print("== Part A: reduced models, full enumeration ==", flush=True)
    cases = [(3, 6, 1, "plain", (3,)), (3, 6, 2, "L", (2, 3)), (3, 6, 3, "P", (1, 2, 3)), (3, 6, 4, "H", (3,)),
             (4, 5, 5, "plain", (1, 3)), (4, 5, 6, "L", (3,)), (4, 5, 7, "P", (2, 3)), (4, 5, 8, "H", (1, 2, 3))]
    for k, (dim, n, seed, ring, P) in enumerate(cases):
        t = time.time()
        run_model_explicit(dim, n, seed, ring, P, neg=(k in (2, 3, 6)))
        print("  case d=%d n=%d ring=%s P=%s seed=%d done (%.1f s)" % (dim, n, ring, P, seed, time.time() - t), flush=True)
    print("== Part B: true dimension 40/39 on short grids, orbit enumeration ==", flush=True)
    for (n, seed, ring, P) in [(5, 21, "plain", (2, 3)), (5, 22, "L", (3,)), (5, 23, "P", (1, 2, 3)), (5, 24, "H", (2, 3))]:
        t = time.time()
        run_model_40(n, seed, ring, P)
        print("  case d=40 n=%d ring=%s P=%s seed=%d done (%.1f s)" % (n, ring, P, seed, time.time() - t), flush=True)
    print()
    print("checks: %d   failures: %d   negative controls: %d (all fail as required: %s)"
          % (NCHK, len(FAILS), len(NEG), all(ok for _, ok in NEG)))
    if FAILS:
        print("FAILED:", FAILS)
    print("wall %.1f s, peak RSS %.0f MB" % (time.time() - T_START,
                                             resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
    print("VERDICT:", "PASS" if not FAILS else "FAIL")


if __name__ == "__main__":
    main()
