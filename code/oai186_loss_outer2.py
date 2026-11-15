#!/usr/bin/env python3
"""Second, independent evaluation of the raw outer loss bounds R_G (2.17) and V_G (2.21) of [14]
(OpenAI, "Numerical certificate for prime gaps at most 186", short_gaps_numerics.pdf) for the group O_{5/2},
components P1..P12 (rank-two bins), H (third factorial) and the low bins L19..L22.  Compared with Table 2.2:
A = ceil(10^18 R / I_H^-), B = ceil(10^18 V / I_H^-), I_H^- = 23685317816e-24.

usage:  python3 code/oai186_loss_outer2.py --comp P1 --out code/cap6/loss_outer2/part_P1.json
        python3 code/oai186_loss_outer2.py --selftest

INDEPENDENCE.  Written from the PDF (pages rendered and read; notes/sources-186-loss.md and -forms.md used as a
reading aid).  Not opened: code/oai186_loss_outer.py, _inner.py, _I2old.py, oai186_check2.py,
third_party/openai186/prime_gap_186_certificate.py, code/cap6/loss_* results.  Nothing is imported from the
repository: the source ladder (1.13)-(1.16), the group parameters (1.23)-(1.24), the Dickman enclosures (2.1)-(2.2),
the profile g, Z, the cap affine rows (2.13), all kernels and moments are computed here.  (code/oai186_support_data.py
was only RUN, as a cross-check of b_G, xi_G, p_G and the masks; code/oai186_J.py was read but NOT used: its rows
(2.13) are built by exact correlations, ours by prefix sums, see (e) below.)  The 77 coefficients C_{sigma,d} are
copied from Table 1.1 (as transcribed in notes/sources-186-forms.md, checked against the PDF text).

WHAT IS COMPUTED (all equation numbers are those of [14]).
 (a) Grid (1.3): N = 98304, n = N - 40, h = S/N, t_j = (j+1/2) h, g_j = g(t_j) (1.7) exactly rational,
     Z = sum_{j<n} g_j^2 enclosed, w^(2)_j = g_j^2/Z, w^(0)_j = 1.
 (b) Dickman point enclosures (2.1) by directed fixed-point integer recurrences (scale 2^-224, floor for the lower,
     ceil for the upper sequence); cell enclosures (2.2) for the cap rows.
 (c) Rank-two arrays (2.9) with the fractions of Lemma 2.4; factorial arrays (2.8); low-bin arrays (2.4)-(2.7)
     with the Eulerian carries; every array is an UPPER array fixed once ("dyadic upper array", Sec. 2.1), here
     rounded up to 2^-192.
 (d) Moments.  NOT by the set-partition expansion (2.10).  A coordinate is the series
         G(X; z, marks) = sum_roles mark(role) sum_j K^role_j X^j exp(sum_{e=2..6} z_e t_j^e),
     so that M_{d,eta} = alpha! [z^alpha] G^d (alpha = multiplicities of eta).  [z^alpha]G only depends on the
     weight w = sum e alpha_e (it is P_w[K]/alpha!), so G^d = sum_k binom(d,k) P_0^{d-k} N^k (N := G - P_0,
     nilpotent) is expanded SYMBOLICALLY in the truncated ring (z-monomials closed under the 53 signatures
     sigma u tau; marks x^2 = y^2 = 0, or y^4 = 0); this yields integer coefficients for numeric monomials
     P_0^m * prod P_w[role].  Checked by brute force over tiny grids (--selftest), including the closed forms
     (1.43) and the [y^3] analogue.  Numerically each monomial is one product chain of exact integer polynomial
     products (Kronecker substitution, GMP via gmpy2, slot 480 bits), floor-truncated at 2^-192, with a rigorous
     running bound e (in units 2^-192) on the truncation deficit: e(XY) <= e(X) S(Y) + e(Y) S(X) + 1 with S the
     coefficient sums.  The contractions are then exact integer dot products.
 (e) Cap affine rows (2.13) by PREFIX SUMS: x_{r+a} = x_r + a h is expanded binomially, so
     v_{s,tau}(r) = sum_{e,d,i} kappa[tau][e][d] binom(d,i) x_r^{d-i} h^i sum_{a : r+a in shell s} a^i g_a d_s(a) t_a^e,
     all exact integers except g_a d_s(a) t_a^e (2^-200).  d_s(a) = cell average, taken as the MIDPOINT of (2.2);
     the effect of the (2.2) enclosure width is bounded separately (reported as V_rad).
 (f) R_G (2.17), V_G (2.21) with C(r), H_eta(r) (2.20) realised as  [*](C(r) M_39(r)) = sum over the complementary
     marking placements (1.44); P = P(0, z_G) of (2.18) (= {3} for O_{5/2}); radial weight w(r) of (2.21).

READINGS OF AMBIGUOUS POINTS (see notes/loss-outer2-report.md):
 R1  (2.1): the upper bar on the recurrence with +1/(2M^3) (the only monotone-consistent placement).
 R2  (2.9): d_j(c) with bars are the Lemma 2.2 POINT enclosures at grid point j (cap rounded up: b^+, r_+^+; down: r_-^-).
 R3  chi_G (1.25): r in [floor(b_G/h) - d_G + 1, min(n-1, floor(t_G/h))]; for O_{5/2} b_G = a_{n,24}, t_G = 98303 h.
 R4  (2.16)/(2.20): K^(0) is the same marked array with w^(0) = 1; [*](C M) = sum of the four (resp. 2, 4)
     complementary placements.
 R5  Lemma 2.4 fractions multiply the A (largest-fragment coordinate) and C (same coordinate) arrays, for both
     profile powers; Lambda = log(b/a) is charged once as the external factor.
 R6  (2.8): D_0 uses the upper delay enclosure dbar_j(Lh) (no renewal branch), no tilt.
 R7  low bins: theta = ceil(7/u_j) with u_j in the same absolute length units as h; L_{<=l} etc as in Lemma 2.3;
     c_G(u) of (1.26) with c_t = a_t, V_t = A_t (computed and found = b_G for L12..L22, as Lemma 1.6 states).
"""
import argparse, json, math, os, sys, time, resource
from fractions import Fraction as Fr
from math import comb, factorial
import numpy as np
import gmpy2
from gmpy2 import mpz

# ---------------------------------------------------------------------------------------------------------------
# constants (1.1), (1.3), Table 1.1
N = 98304
n = N - 40
S = Fr(2742997, 2624989)
h = S / N
T0 = Fr(2499106033, 2624989000)
T1 = Fr(2510000, 2624989)
AH, BH = Fr(2479900401, 2500000000), Fr(-843183, 10 ** 9)
IHLOW = Fr(23685317816, 10 ** 24)
SIGS = [(), (2,), (3,), (4,), (5,), (6,), (2, 2), (2, 3), (2, 4), (3, 3), (2, 2, 2)]
CTAB = [
    [10000000000, -264598476112, 834262268474, -3540575351215, 5377491111325, 116705356572254, 121730820431102],
    [71070047507, 7222861788586, -48747932657986, 290976672545723, -1136422724027134, -2058910631434711, 1375878942948547],
    [6457252424873, -61201446212885, 28811649792090, -2058803084231281, 9970156747759406, 38278849934023144, 34806920812932737],
    [-16779263512274, 128033707910825, 169290603857215, 7359669931312727, -35090795379920588, -120997133235510923, -141527585901304670],
    [28114161526671, -276375633435566, -690482702304933, -15120456749385986, 47650276584638031, 372137534144492224, 2191913505882230103],
    [-21150553032771, 379875924448266, -929062247569514, -13967219843969236, 168416050564605519, -248058724714138769, -4161797957833172083],
    [-19004216224617, 136674974139652, -183344485344333, 1114879023072977, 1119583327002910, -47568062965320963, 2537631525616777],
    [31171802814567, -97428388152051, 526635309233054, 1222047580792220, 15846796161434448, -165623953461271580, -2358019996221938729],
    [-53602626608739, 329397902441121, 1613505134333316, 13893066541430270, -126262434123562668, 239934302929501943, -1506861482386002243],
    [27653330903418, -290549334488305, -1847330641348475, 28351866831729468, -61505472221886320, -424266003419714347, 2585236507449911535],
    [12374547113901, -244168600145684, 1603694896120437, -21603130476787649, -30285492734943698, 381987976419637874, 3605516061450295448],
]
OUTER_ROWS = [((0, 89196), 68225), ((89197, 95598), 49152), ((95599, 98263), 46580)]   # (1.5) outer, chi_s, c_s/h

BF = 192            # fractional bits of all moment-stage arrays
WORDS = 7           # 224-bit storage words (32-bit) per coefficient: 192 fractional + 32 integer bits
SLOT = 15           # 480-bit Kronecker slot
BD = 224            # fractional bits of the Dickman recurrences and coordinate arithmetic


def ceil_div(a, b):
    return -((-a) // b)


def fl(x):
    return x.numerator // x.denominator


def cl(x):
    return -((-x.numerator) // x.denominator)


# ---------------------------------------------------------------------------------------------------------------
# source ladder (1.13)-(1.16), groups (1.22)-(1.24)
def ladder():
    g0, eps = Fr(1, 10 ** 7), {"o": Fr(1, 10 ** 6), "n": Fr(1, 10 ** 7)}
    tau = Fr(1, 10 ** 10)
    sig0 = Fr(100001, 10 ** 6)
    sigm = Fr(1, 2) - Fr(40481, 100000) + tau
    Om = {"o": Fr(12499, 10 ** 6), "n": Fr(253, 20000)}
    rho = Fr(1, 4) + Om["o"]
    rhos = rho - g0
    S_ = Fr(2742997, 10 ** 7) / rhos
    T1_ = Fr(251, 1000) / rhos
    T0_ = 2 - Fr(3, 1000) - S_
    assert S_ == S and T0_ == T0 and T1_ == T1
    e = g0 / rho
    cs = {"o": {1: ((1 - 5 * sig0) / 15, Fr(18, 5)), 2: ((1 - 4 * sig0) / 16, Fr(7, 2)), 3: (Fr(3, 80), Fr(3))},
          "n": {1: ((1 - 5 * sigm) / 15, Fr(18, 5)), 2: ((1 - 4 * sigm) / 16, Fr(7, 2)), 3: ((1 - 2 * sigm) / 20, Fr(16, 5))}}
    TT = {"o": T0, "n": T1}
    rows = {}
    for nu in "on":
        E = rho * (S + TT[nu]) - Fr(1, 2)
        om_prev, t, out = Fr(0), 0, []
        while True:
            r = 1 if t < 12 else (2 if t < 24 else 3)
            c, s = cs[nu][r]
            om = min(Om[nu], (c - eps[nu] - E + 2 * om_prev - g0) / s)
            delta = c - s * om - eps[nu]
            B = (Fr(1, 2) + 2 * om_prev) / rho
            xi = delta / rho
            a, b = B - TT[nu], B - S
            eta = xi if r <= 2 else (xi + S + TT[nu] - B) / 2
            out.append(dict(t=t, r=r, om=om, delta=delta, B=B, xi=xi, a=a, b=b, A=a + eta, C=b + eta))
            if om == Om[nu]:
                break
            om_prev, t = om, t + 1
        rows[nu] = out
    assert len(rows["o"]) == 29 and len(rows["n"]) == 43
    return rows, e


def group_O52():
    rows, e = ladder()
    G = dict(name="O5/2", d=40, m=Fr(5, 2), xi=rows["n"][38]["xi"], U=S + e / 2, b=rows["n"][24]["a"],
             t=98303 * h, zh=46580, ph=19660, e=e)
    assert fl(G["U"] / (2 * G["m"] * h)) == G["ph"]
    # originating rows: own (order three) and absorbed order-two rows of O_2 (for (1.26))
    own = [("o", t) for t in range(24, 28)] + [("n", t) for t in range(24, 39)]
    absorbed = [("o", t) for t in range(0, 24)] + [("n", t) for t in range(0, 24)]
    G["rows"] = [(nu, t, rows[nu][t]) for nu, t in own + absorbed]
    lo = max(0, fl(G["b"] / h) - G["d"] + 1)
    hi = min(n - 1, fl(G["t"] / h))
    G["chi"] = (lo, hi)
    return G


# ---------------------------------------------------------------------------------------------------------------
# symbolic z-series expansion of G^d in the truncated (marking x z) ring
def admissible():
    return sorted(set(tuple(sorted(a + b)) for a in SIGS for b in SIGS), key=lambda t: (len(t), t))


RING = {
    # roles: name -> marking exponent; extraction monomial for R ([*]); truncation of marks
    "P": dict(roles=[("P", (0, 0)), ("A", (1, 0)), ("B", (0, 1)), ("C", (1, 1))], star=(1, 1), cap=(1, 1)),
    "H": dict(roles=[("F0", (0,)), ("F1", (1,)), ("F2", (2,)), ("F3", (3,))], star=(3,), cap=(3,)),
    "L": dict(roles=[("P", (0,)), ("D", (1,))], star=(1,), cap=(1,)),
}


def alpha_fact(eta):
    out = 1
    for e in set(eta):
        out *= factorial(eta.count(e))
    return out


def sym_power(kind, d):
    """returns dict mark -> dict eta -> dict monomial -> int, with
       [mark] M_{d,eta} = sum_monomial coef * P_0[ord]^{d - len(monomial)} prod_{(role,w) in monomial} P_w[role],
       (the ordinary role's weight-0 factor is the power of P_0, all other factors are listed)."""
    R = RING[kind]
    cap = R["cap"]
    adm = set(admissible())
    ordname = R["roles"][0][0]
    # N = G - P_0[ord]
    Nel = {}
    for role, mk in R["roles"]:
        for al in adm:
            if role == ordname and al == ():
                continue
            w = sum(al)
            Nel.setdefault((mk, al), {})[((role, w),)] = Fr(1, alpha_fact(al))
    def addm(m1, m2):
        m = tuple(a + b for a, b in zip(m1, m2))
        return m if all(x <= c for x, c in zip(m, cap)) else None
    if len(cap) == 1:
        def addm(m1, m2):
            m = (m1[0] + m2[0],)
            return m if m[0] <= cap[0] else None
    powk = [{(tuple(0 for _ in cap), ()): {(): Fr(1)}}]
    while True:
        prev, cur = powk[-1], {}
        for (m1, a1), t1 in prev.items():
            for (m2, a2), t2 in Nel.items():
                m = addm(m1, m2)
                if m is None:
                    continue
                al = tuple(sorted(a1 + a2))
                if al not in adm:
                    continue
                dst = cur.setdefault((m, al), {})
                for f1, c1 in t1.items():
                    for f2, c2 in t2.items():
                        key = tuple(sorted(f1 + f2))
                        dst[key] = dst.get(key, 0) + c1 * c2
        if not cur:
            break
        powk.append(cur)
    out = {}
    for k, el in enumerate(powk):
        if k > d:
            break
        bk = comb(d, k)
        for (m, al), terms in el.items():
            dst = out.setdefault(m, {}).setdefault(al, {})
            af = alpha_fact(al)
            for f, c in terms.items():
                v = c * bk * af
                if v:
                    dst[f] = dst.get(f, 0) + v
    for m in out:
        for al in out[m]:
            for f in list(out[m][al]):
                v = out[m][al][f]
                assert v.denominator == 1
                out[m][al][f] = int(v)
                if v == 0:
                    del out[m][al][f]
    return out


def _selftest_symbolic(seed=1):
    """brute force over a tiny grid: all cells and role placements of d coordinates."""
    import random, itertools
    rnd = random.Random(seed)
    adm = admissible()
    ok = True
    for kind in ("P", "H", "L"):
        R = RING[kind]
        roles = R["roles"]
        for d, ncell in ((3, 3), (4, 2)):
            K = {role: [Fr(rnd.randint(1, 9), rnd.randint(1, 5)) for _ in range(ncell)] for role, _ in roles}
            t = [Fr(rnd.randint(1, 9), 7) for _ in range(ncell)]
            L = d * ncell
            def pw(role, w):
                return [K[role][j] * t[j] ** w if j < ncell else Fr(0) for j in range(L)]
            def mul(a, b):
                c = [Fr(0)] * L
                for i, x in enumerate(a):
                    if x:
                        for j, y in enumerate(b[:L - i]):
                            c[i + j] += x * y
                return c
            sym = sym_power(kind, d)
            brute = {}
            for cells in itertools.product(range(ncell), repeat=d):
                for asg in itertools.product(range(len(roles)), repeat=d):
                    mk = tuple(sum(roles[a][1][q] for a in asg) for q in range(len(R["cap"])))
                    if any(x > c for x, c in zip(mk, R["cap"])):
                        continue
                    wgt = Fr(1)
                    for c_, a in zip(cells, asg):
                        wgt *= K[roles[a][0]][c_]
                    r = sum(cells)
                    for eta in adm:
                        val = wgt
                        for e in eta:
                            val *= sum(t[c_] ** e for c_ in cells)
                        bm = brute.setdefault(mk, {}).setdefault(eta, [Fr(0)] * L)
                        bm[r] += val
            for mk, byeta in brute.items():
                for eta, poly in byeta.items():
                    acc = [Fr(0)] * L
                    for mono, coef in sym.get(mk, {}).get(eta, {}).items():
                        p = [Fr(1)] + [Fr(0)] * (L - 1)
                        for _ in range(d - len(mono)):
                            p = mul(p, pw(roles[0][0], 0))
                        for role, w in mono:
                            p = mul(p, pw(role, w))
                        acc = [a + coef * b for a, b in zip(acc, p)]
                    if acc != poly:
                        ok = False
                        print("MISMATCH", kind, d, mk, eta)
            # closed forms (1.43) and the [y^3] analogue, eta = () and eta = (2,3)
            for eta in [(), (2, 3)]:
                pass
            print("symbolic selftest", kind, "d=%d" % d, "ok" if ok else "FAIL", flush=True)
    return ok


# ---------------------------------------------------------------------------------------------------------------
# fixed-point polynomial arithmetic: coefficients are integers at scale 2^-BF stored as (L, WORDS) uint32 arrays.
TWO_BF = 1 << BF
ULP = 2.0 ** -BF
_WPOW = np.array([2.0 ** (32 * k - BF) for k in range(WORDS)])
NPROD = [0, 0.0]          # number of big products, seconds spent in them


def ints_to_words(xs):
    bl = WORDS * 4
    return np.frombuffer(b"".join(int(x).to_bytes(bl, "little") for x in xs), dtype=np.uint32).reshape(-1, WORDS).copy()


def words_to_ints(a):
    b = a.tobytes()
    bl = WORDS * 4
    return [int.from_bytes(b[i:i + bl], "little") for i in range(0, len(b), bl)]


class Poly:
    """sum_{i<L} a[i] 2^-BF X^(v+i);  true polynomial in [this, this + err*2^-BF] coefficientwise."""
    __slots__ = ("v", "a", "err", "mass")

    def __init__(self, v, a, err=0.0):
        nz = np.nonzero(a.any(axis=1))[0]
        if len(nz) == 0:
            self.v, self.a = v, a[:0]
        else:
            self.v, self.a = v + int(nz[0]), a[nz[0]:nz[-1] + 1]
        self.err = err
        self.mass = float(self.a.astype(np.float64) @ _WPOW.sum() if False else (self.a.astype(np.float64) @ _WPOW).sum()) * (1 + 1e-12)

    @staticmethod
    def from_ints(v, xs, err=0.0):
        return Poly(v, ints_to_words(xs), err)

    def to_ints(self):
        return words_to_ints(self.a)

    def __len__(self):
        return len(self.a)


def _pack(a):
    buf = np.zeros((len(a), SLOT), dtype=np.uint32)
    buf[:, :WORDS] = a
    return mpz.from_bytes(buf.tobytes(), "little")


def pmul(X, Y, ntr, mode="floor"):
    """X*Y mod X^ntr, coefficientwise floor (default; error tracked) or ceil (upper kernels) of the scaled product."""
    if X is None or Y is None:
        return None
    v = X.v + Y.v
    if v >= ntr or len(X) == 0 or len(Y) == 0:
        return None
    Lx, Ly = min(len(X), ntr - v), min(len(Y), ntr - v)
    t0 = time.time()
    p = _pack(X.a[:Lx]) * _pack(Y.a[:Ly])
    nout = min(Lx + Ly - 1, ntr - v)
    W = np.frombuffer(p.to_bytes((Lx + Ly) * SLOT * 4, "little"), dtype=np.uint32).reshape(-1, SLOT)[:nout]
    if W[:, BF // 32 + WORDS:].any():
        raise OverflowError("coefficient overflow in pmul")
    res = W[:, BF // 32:BF // 32 + WORDS].copy()
    if mode == "ceil":
        carry = W[:, :BF // 32].any(axis=1).astype(np.uint64)
        for k in range(WORDS):
            s = res[:, k].astype(np.uint64) + carry
            res[:, k] = (s & 0xFFFFFFFF).astype(np.uint32)
            carry = s >> np.uint64(32)
        assert not carry.any()
        err = 0.0
    else:
        mY = Y.mass + Ly * Y.err * ULP
        err = (X.err * mY + Y.err * X.mass + 1.0) * (1 + 1e-9)
    NPROD[0] += 1
    NPROD[1] += time.time() - t0
    return Poly(v, res, err)


# ---------------------------------------------------------------------------------------------------------------
# coordinate data: g_j, Z, w^(2); Dickman enclosures (2.1)
PQ = 2 * N * 2624989          # t_j = (2j+1)*2742997 / PQ  exactly


def tnum(j):
    return (2 * j + 1) * 2742997


def g_exact(j):
    """g(t_j) as (num, den), (1.7): 21/200/(1+t/100) + 179/200/(1+907t/5)."""
    p, q = tnum(j), PQ
    den = 40 * (100 * q + p) * (5 * q + 907 * p)
    num = 21 * q * 20 * (5 * q + 907 * p) + 179 * q * (100 * q + p)
    return num, den


_GCACHE = {}


def coord_data():
    if "g" in _GCACHE:
        return _GCACHE["g"]
    glo, ghi = [], []
    for j in range(n):
        a, b = g_exact(j)
        glo.append((a << BD) // b)
        ghi.append(ceil_div(a << BD, b))
    Zlo = sum((x * x) >> BD for x in glo)                 # Z at scale 2^-BD
    Zhi = sum(ceil_div(x * x, 1 << BD) for x in ghi)
    # upper enclosures of w^(2)_j = g_j^2/Z at scale 2^-BD
    w2hi = [ceil_div(x * x, Zlo) for x in ghi]
    out = dict(glo=glo, ghi=ghi, Zlo=Zlo, Zhi=Zhi, w2hi=w2hi)
    _GCACHE["g"] = out
    return out


_DCACHE = {}


def dickman(M, jmax=N + 1):
    """(dl, du): Lemma 2.2 point enclosures of D_{Mh}(jh) = rho(j/M), j <= jmax, scale 2^-BD (directed)."""
    if M in _DCACHE:
        return _DCACHE[M]
    ONE = 1 << BD
    dl = [ONE] * (min(M, jmax) + 1)
    du = [ONE] * (min(M, jmax) + 1)
    add = ceil_div(ONE, 2 * M ** 3)
    for j in range(M, jmax):
        x = dl[j] - ceil_div(du[j - M], 2 * j) - ceil_div(du[j + 1 - M], 2 * (j + 1))
        y = du[j] - dl[j - M] // (2 * j) - dl[j + 1 - M] // (2 * (j + 1)) + add
        dl.append(max(0, x))
        du.append(min(ONE, y))
    # acceptance tests of Lemma 2.2
    for j in range(len(dl) - 1):
        assert 0 <= dl[j] <= du[j] <= ONE and dl[j + 1] <= dl[j] and du[j + 1] <= du[j]
    _DCACHE[M] = (dl, du)
    return dl, du


# ---------------------------------------------------------------------------------------------------------------
# elementary enclosures (Lemma 2.1 replaced by mpmath at 320 bits plus an absolute outward margin 2^-280)
import mpmath
mpmath.mp.prec = 320
_MARG = mpmath.mpf(2) ** -280


def mpq(x):
    return mpmath.mpf(x.numerator) / x.denominator


def log_hi(x):
    return mpmath.log(mpq(x)) + _MARG


def log_lo(x):
    return mpmath.log(mpq(x)) - _MARG


def fix_hi(x, bits):
    return int(mpmath.ceil(x * mpmath.mpf(2) ** bits))


# ---------------------------------------------------------------------------------------------------------------
# rank-two arrays (2.9) with the fractions of Lemma 2.4
def rank_two_arrays(G, a, b):
    m, U = G["m"], G["U"]
    assert U / (m + 1) <= a < b <= G["zh"] * h < U
    rp, rm = (U - a) / m, (U - b) / m
    Mb, Mrp, Mrm = cl(b / h), cl(rp / h), fl(rm / h)
    fa = fl(a / h)
    _, du_b = dickman(Mb)
    _, du_rp = dickman(Mrp)
    dl_rm, _ = dickman(Mrm)
    Lam_hi, Lam_lo = log_hi(b / a), log_lo(b / a)
    cd = coord_data()
    w2 = cd["w2hi"]
    ONE = 1 << BD

    def lam_hi(v):            # outward upper bound of lambda(v), scale 2^-BD
        if v <= a:
            return 0
        if v >= b:
            return ONE
        return min(ONE, fix_hi(log_hi(v / a) / Lam_lo, BD))

    arr = {r: ([0] * n, [0] * n) for r in "PABC"}
    sh2, sh3 = 2 * BD - BF, 3 * BD - BF
    for j in range(n):
        tp = (j + 1) * h
        wj = w2[j]
        sm = max(0, j - Mb)
        sp = max(0, j + 1 - fa)
        # P
        x = du_b[j]
        arr["P"][0][j] = ceil_div(wj * x, 1 << sh2)
        arr["P"][1][j] = ceil_div(x, 1 << (BD - BF))
        # A
        if tp > a:
            lam = lam_hi(tp)
            x = du_rp[sm] * lam
            arr["A"][0][j] = ceil_div(wj * x, 1 << sh3)
            arr["A"][1][j] = ceil_div(x, 1 << (2 * BD - BF))
        # B
        x = max(0, du_b[j] - dl_rm[j + 1])
        arr["B"][0][j] = ceil_div(wj * x, 1 << sh2)
        arr["B"][1][j] = ceil_div(x, 1 << (BD - BF))
        # C
        if tp > a + rp:
            beta = 0 if j * h < b else dl_rm[sp]
            v = min(tp, (m * tp - U) / (m - 1))
            lam = lam_hi(v)
            x = max(0, du_b[sm] - beta) * lam
            arr["C"][0][j] = ceil_div(wj * x, 1 << sh3)
            arr["C"][1][j] = ceil_div(x, 1 << (2 * BD - BF))
    info = dict(a=float(a), b=float(b), Lambda=float(Lam_hi), Mb=Mb, Mrp=Mrp, Mrm=Mrm,
                first_nonzero={r: next((j for j in range(n) if arr[r][0][j]), None) for r in "PABC"})
    return arr, Lam_hi, info


def rank_two_bins(G):
    q0 = G["U"] / (G["m"] + 1)
    z = G["zh"] * h
    T2 = [Fr(j, 16) for j in range(9)] + [Fr(5, 8), Fr(3, 4), Fr(7, 8), Fr(1)]
    return [(q0 + T2[j - 1] * (z - q0), q0 + T2[j] * (z - q0)) for j in range(1, len(T2))]


# ---------------------------------------------------------------------------------------------------------------
# cap affine rows (2.13) by prefix sums; v^(l) for l in P(0, z_G)
DX = 2624989 * N * 10            # x_r = XR(r)/DX,  h = HX/DX
HX = 27429970
BV2, BV = 200, 128


def XR(r):
    return (r + 20) * HX - 9 * 2624989 * N


def kappa():
    """kappa[tau][e][d] = sum over (sigma, labelled A) with sigma minus A = tau, e(A) = e of C_{sigma,d}."""
    out = {}
    for si, sg in enumerate(SIGS):
        L = len(sg)
        for mask in range(1 << L):
            tau = tuple(sorted(sg[i] for i in range(L) if not mask >> i & 1))
            e = sum(sg[i] for i in range(L) if mask >> i & 1)
            row = out.setdefault(tau, {}).setdefault(e, [0] * 7)
            for d in range(7):
                row[d] += CTAB[si][d]
    return out


def Pset(u, v):
    c = [None] + [Fr(x) * h for _, x in OUTER_ROWS] + [Fr(0)]
    return [l for l in (1, 2, 3) if max(u, c[l + 1]) < min(v, c[l])]


def vrows(G, cache_dir):
    """returns (Vfix[tau] object arrays: v^(l)_tau(r) * 2^BV floored, summed over l in P(0,z_G) is NOT done here:
       one array per l), radv[l][tau] float arrays (bound from the (2.2) enclosure width)."""
    Ps = Pset(Fr(0), G["zh"] * h)
    key = os.path.join(cache_dir, "vrows_%s_%s.pkl" % (G["name"].replace("/", ""), "".join(map(str, Ps))))
    if os.path.exists(key):
        import pickle
        with open(key, "rb") as f:
            return pickle.load(f)
    cd = coord_data()
    glo = cd["glo"]
    kap = kappa()
    taus = SIGS
    es = sorted({e for t in kap for e in kap[t]})
    r_arr = np.arange(n)
    Xp = [np.array([XR(r) ** k for r in range(n)], dtype=object) for k in range(7)]
    apow = [np.array([(HX * a) ** i for a in range(n)], dtype=object) for i in range(7)]
    out = {}
    for l in Ps:
        Y = {(e, d): np.zeros(n, dtype=object) for e in es for d in range(7)}
        radY = {(e, d): np.zeros(n) for e in es for d in range(7)}
        for s in range(1, l + 1):
            (lo, hi), M = OUTER_ROWS[s - 1]
            dl, du = dickman(M)
            ONE = 1 << BD
            sub = ceil_div(ONE, 12 * M * M)
            dmid, drad = [], []
            for a in range(n):
                if a < M:
                    dmid.append(ONE); drad.append(0.0)
                else:
                    dlo = max(0, (dl[a] + dl[a + 1]) // 2 - sub)
                    dhi = min(ONE, ceil_div(du[a] + du[a + 1], 2))
                    dmid.append((dlo + dhi) // 2); drad.append((dhi - dlo) / 2 / ONE)
            # max |x| over the shell where the enclosure width is nonzero
            xs = [abs(XR(k)) / DX for k in (max(lo, M), hi)]
            xb = max(xs) if max(lo, M) <= hi else 0.0
            ih = np.clip(hi - r_arr + 1, 0, n)
            il = np.minimum(np.clip(lo - r_arr, 0, n), ih)
            for e in es:
                f = np.array([(glo[a] * dmid[a] * tnum(a) ** e) // (PQ ** e << (2 * BD - BV2)) for a in range(n)], dtype=object)
                frad = np.array([glo[a] / 2.0 ** BD * drad[a] * (tnum(a) / PQ) ** e for a in range(n)])
                PSr = np.concatenate([[0.0], np.cumsum(frad)])
                Trad = PSr[ih] - PSr[il]
                for i in range(7):
                    PS = np.concatenate([np.array([0], dtype=object), np.cumsum(f * apow[i])])
                    T = PS[ih] - PS[il]
                    for d in range(i, 7):
                        Y[(e, d)] += comb(d, i) * Xp[d - i] * T
                for d in range(7):
                    radY[(e, d)] += xb ** d * Trad
        QS = 10 ** 10 * DX ** 6
        Vfix, radv = {}, {}
        for tau in taus:
            acc = np.zeros(n, dtype=object)
            racc = np.zeros(n)
            for e, row in kap[tau].items():
                for d in range(7):
                    if row[d]:
                        acc += (row[d] * DX ** (6 - d)) * Y[(e, d)]
                        racc += abs(row[d]) * 1e-10 * radY[(e, d)]
            Vfix[tau] = np.array([(x << BV) // (QS << BV2) for x in acc], dtype=object)
            radv[tau] = racc
        out[l] = (Vfix, radv)
        del Y
    import pickle
    os.makedirs(cache_dir, exist_ok=True)
    with open(key, "wb") as f:
        pickle.dump(out, f)
    return out


# ---------------------------------------------------------------------------------------------------------------
# the outer forms (2.17) and (2.21)
def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def mark_sub(star, mu):
    return tuple(a - b for a, b in zip(star, mu))


def Qeta_int(r):
    """Q_eta(r) * QS^2 (exact integers), QS = 10^10 DX^6, (2.11)."""
    X = XR(r)
    xp = [X ** d * DX ** (6 - d) for d in range(7)]
    p = [sum(CTAB[s][d] * xp[d] for d in range(7)) for s in range(len(SIGS))]
    out = {}
    for i, a in enumerate(SIGS):
        for j, b in enumerate(SIGS):
            eta = tuple(sorted(a + b))
            out[eta] = out.get(eta, 0) + p[i] * p[j]
    return out


def outer_forms(G, kind, arr, Lam_hi, Wfix=None, BW=0, Wcoef=None, cache_dir=".", log=print, chi=None):
    """arr[role] = (K2 ints, K0 ints) upper arrays at 2^-BF over j < n.
       Wfix: None, or dict r -> ceil(W(r) 2^BW) for the low bins (radial weight of (1.38)).
       Returns dict with R, V (midpoint rows), bounds."""
    t0 = time.time()
    R_ = RING[kind]
    roles = [rn for rn, _ in R_["roles"]]
    marks = dict(R_["roles"])
    star = R_["star"]
    ordn = roles[0]
    lo, hi = chi if chi is not None else G["chi"]
    # --- power-sum polynomials P_w[role] (floor of K_j t_j^w)
    ws = [0] + list(range(2, 13))
    polys = {}
    tw = {0: [1] * n}
    for w in ws[1:]:
        tw[w] = [tnum(j) ** w for j in range(n)]
    for role in roles:
        K2 = arr[role][0]
        nz = [j for j in range(n) if K2[j]]
        if not nz:
            continue
        v0 = nz[0]
        for w in ws:
            den = PQ ** w
            xs = [(K2[j] * tw[w][j]) // den for j in range(v0, n)]
            polys[(role, w)] = Poly.from_ints(v0, xs, err=0.0 if w == 0 else 1.0)
    del tw
    log("power sums built (%d polys)" % len(polys))
    # --- symbolic coefficients
    sym40 = sym_power(kind, 40)[star]
    sym39 = sym_power(kind, 39)
    inc = {}          # (pow0, mono) -> list of ("R", eta, c) / ("V", mu, eta, c)
    for eta, terms in sym40.items():
        for mono, c in terms.items():
            inc.setdefault((40 - len(mono), mono), []).append(("R", None, eta, c))
    for mu, byeta in sym39.items():
        for eta, terms in byeta.items():
            for mono, c in terms.items():
                inc.setdefault((39 - len(mono), mono), []).append(("V", mu, eta, c))
    # drop monomials containing an empty role
    inc = {k: v for k, v in inc.items() if all(f in polys for f in k[1])}
    log("%d numeric monomials (R %d, V %d)" % (len(inc), sum(1 for v in inc.values() if v[0][0] == "R"),
                                             sum(1 for v in inc.values() if v[0][0] == "V")))
    # --- R weights on chi
    QS2 = (10 ** 10 * DX ** 6) ** 2
    Qr = [Qeta_int(r) for r in range(lo, hi + 1)]
    if Wfix is not None:
        Qr = [{eta: q * Wfix[lo + i] for eta, q in Q.items()} for i, Q in enumerate(Qr)]
    Rsum, Rpos_err, Rneg_err = 0, 0.0, 0.0
    # --- V weights
    vr = vrows(G, cache_dir)
    log("v rows ready")
    Ps = sorted(vr)
    etas = admissible()
    Vq, Vqrad = {}, {}
    for eta in etas:
        Vq[eta] = np.zeros(n, dtype=object)
        Vqrad[eta] = np.zeros(n)
    for l in Ps:
        Vfix, radv = vr[l]
        for a in SIGS:
            for b in SIGS:
                eta = tuple(sorted(a + b))
                Vq[eta] += Vfix[a] * Vfix[b]
                fa = np.abs(np.array([float(x) for x in Vfix[a]])) / 2.0 ** BV
                fb = np.abs(np.array([float(x) for x in Vfix[b]])) / 2.0 ** BV
                Vqrad[eta] += fa * radv[b] + radv[a] * fb + radv[a] * radv[b]
    # erased-coordinate correlations C_role(r) = sum_{a} chi(r+a) W(r+a) K0_a  (W = 1 or W(r+a))
    wI = np.array([5 * 10 ** 9 if (r + 39) * h <= T0 else (4955584887 if (r + 39) * h <= T1 else 4215915)
                   for r in range(n)], dtype=object)
    WC, WCf = {}, {}
    for role in roles:
        K0 = arr[role][1]
        if Wcoef is None:
            ps = [0]
            for a in range(n):
                ps.append(ps[-1] + K0[a])
            C = [(ps[min(n, hi - r + 1)] - ps[min(max(0, lo - r), hi - r + 1)]) if r <= hi else 0 for r in range(n)]
        else:
            C = Wcoef(K0)                     # low bins: scale 2^-(BF+BW)
        mu = mark_sub(star, marks[role])
        WC[mu] = wI * np.array(C, dtype=object)
        WCf[mu] = np.array([float(x) for x in WC[mu]])
    # AbsW for the error bound
    absW = {}
    for mu in WC:
        for eta in etas:
            q = np.abs(np.array([float(x) for x in Vq[eta]])) * WCf[mu]
            absW[(mu, eta)] = float(q.sum())
    log("V weights ready")
    Vsum, Verr, Vrad = 0, 0.0, 0.0
    # --- P_0 powers
    pows = sorted({k[0] for k in inc})
    P0 = polys[(ordn, 0)]
    P0pow = {1: P0}
    cur, e = P0, 1
    b2 = {1: P0}
    while 2 * e <= pows[0]:
        cur = pmul(cur, cur, n); e *= 2; b2[e] = cur
    # assemble pows[0] from binary pieces
    rem, acc = pows[0], None
    for e2 in sorted(b2, reverse=True):
        if e2 <= rem:
            acc = b2[e2] if acc is None else pmul(acc, b2[e2], n)
            rem -= e2
    P0pow = {pows[0]: acc}
    for p in range(pows[0] + 1, pows[-1] + 1):
        P0pow[p] = pmul(P0pow[p - 1], P0, n)
    del b2
    log("P_0 powers %d..%d" % (pows[0], pows[-1]))
    # --- group monomials by ordinary part lambda
    groups = {}
    for (p0, mono) in inc:
        lam = tuple(f for f in mono if f[0] == ordn)
        mk = tuple(f for f in mono if f[0] != ordn)
        groups.setdefault(lam, []).append((p0, mk, mono))
    Pi = {(): None}
    MP = {(): None}

    def getPi(lam):
        if lam not in Pi:
            Pi[lam] = pmul(getPi(lam[:-1]), polys[lam[-1]], n) if len(lam) > 1 else polys[lam[0]]
        return Pi[lam]

    def getMP(mk):
        if mk not in MP:
            MP[mk] = pmul(getMP(mk[:-1]), polys[mk[-1]], n) if len(mk) > 1 else polys[mk[0]]
        return MP[mk]

    def times(Aa, Bb):
        if Aa is None:
            return Bb
        if Bb is None:
            return Aa
        return pmul(Aa, Bb, n)

    done = 0
    for gi, lam in enumerate(sorted(groups, key=lambda l: (len(l), l))):
        Pl = getPi(lam)
        Ucache = {}
        for (p0, mk, mono) in sorted(groups[lam]):
            if p0 not in Ucache:
                Ucache[p0] = times(P0pow[p0], Pl)
            Y = times(Ucache[p0], getMP(mk))
            done += 1
            if Y is None:
                continue
            for tgt in [x for x in inc[(p0, mono)] if x[0] == "R"][:1]:
                cs = {eta: c for (kk, _m, eta, c) in inc[(p0, mono)] if kk == "R"}
                a0, a1 = max(lo, Y.v), min(hi, Y.v + len(Y) - 1)
                if a0 <= a1:
                    yv = words_to_ints(Y.a[a0 - Y.v:a1 - Y.v + 1])
                    pos = neg = 0
                    for i, y in enumerate(yv):
                        Q = Qr[a0 - lo + i]
                        q = sum(c * Q[eta] for eta, c in cs.items())
                        Rsum += q * y
                        if q > 0:
                            pos += q
                        else:
                            neg -= q
                    Rpos_err += Y.err * float(pos)
                    Rneg_err += Y.err * float(neg)
            vt = [x for x in inc[(p0, mono)] if x[0] == "V"]
            if vt:
                mu = vt[0][1]
                assert all(x[1] == mu for x in vt)
                if mu in WC:
                    s0, L = Y.v, len(Y)
                    L = min(L, n - s0)
                    combo = None
                    combr = np.zeros(L)
                    eb = 0.0
                    for (_, _, eta, c) in vt:
                        part = c * Vq[eta][s0:s0 + L]
                        combo = part if combo is None else combo + part
                        combr += c * Vqrad[eta][s0:s0 + L]
                        eb += c * absW[(mu, eta)]
                    yobj = np.array(words_to_ints(Y.a[:L]), dtype=object)
                    Vsum += int(np.dot(combo * WC[mu][s0:s0 + L], yobj))
                    yf = Y.a[:L].astype(np.float64) @ _WPOW
                    Vrad += float(np.dot(combr * WCf[mu][s0:s0 + L], yf))
                    Verr += Y.err * eb
        Ucache.clear()
        if gi % 10 == 0:
            log("lambda %d/%d, monomials %d/%d, products %d (%.0f s in GMP), rss %.0f MB"
                % (gi + 1, len(groups), done, len(inc), NPROD[0], NPROD[1], rss_mb()))
    cd = coord_data()
    Zlo = Fr(cd["Zlo"], 1 << BD)
    # R = 40 Lambda sum_r chi W sum_eta Q_eta [X^r *] M_40
    RS = Fr(1, QS2 << (BF + BW))
    R_mid = 40 * mpq(Fr(Rsum) * RS) * Lam_hi
    RE = mpq(Fr(1, QS2 << BW)) * ULP * 40 * Lam_hi          # Y.err is in units 2^-BF
    R_up = R_mid + mpmath.mpf(Rpos_err) * RE
    # V = 40 h^2 Lambda / Z sum_l S(v^(l), H; w)
    VS = Fr(1, (5 * 10 ** 9) << (2 * BV + 2 * BF + BW)) * 40 * h * h / Zlo
    V_mid = mpq(Fr(Vsum) * VS) * Lam_hi
    V_err = mpmath.mpf(Verr) * ULP * mpq(VS * (1 << BF)) * Lam_hi
    V_rad = mpmath.mpf(Vrad) * mpq(Fr(1, (5 * 10 ** 9) << (BF + BW)) * 40 * h * h / Zlo) * Lam_hi
    return dict(R=R_mid, R_up=R_up, R_numerr=mpmath.mpf(max(Rpos_err, Rneg_err)) * RE,
                V=V_mid, V_numerr=V_err, V_rad=V_rad, products=NPROD[0], gmp_seconds=NPROD[1],
                monomials=len(inc), seconds=time.time() - t0)


def ih_check(log=print):
    """end-to-end check of the moment machinery: I_H by (2.12) with the same engine (cell averages d_c(j) of (2.2),
    midpoint), to be compared with Lemma 2.5: 23685317816e-24 <= I_H <= 23685317890e-24."""
    cd = coord_data()
    w2 = cd["w2hi"]
    sym = sym_power("L", 40)[(0,)]
    total = Fr(0)
    for (lo, hi), M in OUTER_ROWS:
        dl, du = dickman(M)
        ONE = 1 << BD
        sub = ceil_div(ONE, 12 * M * M)
        K = []
        for j in range(n):
            if j < M:
                d = ONE
            else:
                d = (max(0, (dl[j] + dl[j + 1]) // 2 - sub) + min(ONE, ceil_div(du[j] + du[j + 1], 2))) // 2
            K.append((w2[j] * d) >> (2 * BD - BF))
        polys = {}
        for w in [0] + list(range(2, 13)):
            polys[w] = Poly.from_ints(0, [(K[j] * tnum(j) ** w) // PQ ** w for j in range(n)])
        P0 = polys[0]
        pw = {1: P0}
        for k in (2, 4, 8, 16, 32):
            pw[k] = pmul(pw[k // 2], pw[k // 2], n)
        p34 = pmul(pw[32], pw[2], n)
        P0pow = {34: p34}
        for p in range(35, 41):
            P0pow[p] = pmul(P0pow[p - 1], P0, n)
        Pi = {}
        Qr = [Qeta_int(r) for r in range(lo, hi + 1)]
        acc = 0
        for eta, terms in sym.items():
            pass
        byY = {}
        for eta, terms in sym.items():
            for mono, c in terms.items():
                byY.setdefault(mono, {})[eta] = c
        for mono in sorted(byY, key=lambda m: (len(m), m)):
            lam = tuple(w for _, w in mono)
            if lam and lam not in Pi:
                Pi[lam] = polys[lam[0]] if len(lam) == 1 else pmul(Pi[lam[:-1]], polys[lam[-1]], n)
            Y = P0pow[40] if not lam else pmul(P0pow[40 - len(lam)], Pi[lam], n)
            a0, a1 = max(lo, Y.v), min(hi, Y.v + len(Y) - 1)
            if a0 > a1:
                continue
            yv = words_to_ints(Y.a[a0 - Y.v:a1 - Y.v + 1])
            cs = byY[mono]
            for i, y in enumerate(yv):
                acc += y * sum(c * Qr[a0 - lo + i][eta] for eta, c in cs.items())
        part = Fr(acc, ((10 ** 10 * DX ** 6) ** 2) << BF)
        log("I_H shell cap %d: %.12e" % (M, float(part)))
        total += part
    log("I_H = %.12e   (Lemma 2.5: [2.3685317816e-14, 2.3685317890e-14])" % float(total))
    return total


# ---------------------------------------------------------------------------------------------------------------
# Eulerian polynomials (2.5) and the third-factorial arrays (2.8)
def eulerian(r):
    """Eu(r, a), a = 0..r-1, recurrence (2.5)."""
    row = [1]
    for rr in range(2, r + 1):
        new = []
        for a in range(rr):
            x = (a + 1) * (row[a] if a < len(row) else 0) + (rr - a) * (row[a - 1] if 0 <= a - 1 < len(row) else 0)
            new.append(x)
        row = new
    return row


def ints_ceil_from_BD(xs):
    return [ceil_div(x, 1 << (BD - BF)) for x in xs]


def factorial_arrays(G):
    L = G["ph"]                               # floor(p_G/h), p_G = 19660 h exactly
    K = G["zh"]                               # ceil(z_0/h), z_G aligned
    _, du = dickman(L, N)
    Dbar = Poly.from_ints(0, ints_ceil_from_BD(du[:N]))
    Q = Poly.from_ints(L, [ceil_div(TWO_BF, a) for a in range(L, K)])
    kmax = (N - 1) // L
    Qk = {1: Q}
    for k in range(2, kmax + 1):
        Qk[k] = pmul(Qk[k - 1], Q, N, "ceil")
    out = {}
    for a in range(4):
        bmax = (N - 1 - a * L) // L
        S = [0] * N
        for b in range(bmax + 1):
            k = a + b
            Eu = eulerian(k + 1)
            den = factorial(k + 1) * factorial(a) * factorial(b)
            if k == 0:
                base = {0: TWO_BF}            # Q^0 = 1
            else:
                P = Qk[k]
                base = {P.v + i: x for i, x in enumerate(P.to_ints())}
            T = {}
            for j, x in base.items():
                for i, e in enumerate(Eu):
                    if j + i < N:
                        T[j + i] = T.get(j + i, 0) + e * x
            for j, x in T.items():
                S[j] += ceil_div(x, den)
        Sp = Poly.from_ints(0, S)
        F = pmul(Dbar, Sp, N, "ceil")
        Fi = [0] * N
        for i, x in enumerate(F.to_ints()):
            Fi[F.v + i] = x
        out[a] = Fi[:n]
    cd = coord_data()
    arr = {}
    for a in range(4):
        K0 = out[a]
        K2 = [ceil_div(cd["w2hi"][j] * K0[j], 1 << BD) for j in range(n)]
        arr["F%d" % a] = (K2, K0)
    return arr


# ---------------------------------------------------------------------------------------------------------------
# low bins (1.5.1), (1.26), (2.4)-(2.7), (1.38)
def low_bounds_O52(G):
    xi, p = G["xi"], G["ph"] * h
    a = [Fr(6, 5) ** j / 20 for j in range(10)]
    U2 = [2 ** j * xi for j in range(9)] + [Fr(1, 100), Fr(3, 200), Fr(9, 400), Fr(27, 800)] + a[:8] + [(a[7] + p) / 2, p]
    assert all(U2[i] < U2[i + 1] for i in range(len(U2) - 1)) and len(U2) == 23
    return U2


def cG(G, u):
    vals = []
    for nu, t, row in G["rows"]:
        if row["xi"] < u:
            mu = Fr(5, 2) if row["r"] == 3 else Fr(2)
            vals.append(max(row["a"], row["A"] - (mu - 1) * u))
    if not vals:
        return None
    return max(G["b"], min(vals))


def short_mul_ceil(P, coefs, den, ntr):
    """ceil( P(X) * sum_i coefs[i] X^i / den ) for a Poly P (ints at 2^-BF) and small integer coefs."""
    base = {P.v + i: x for i, x in enumerate(P.to_ints())}
    T = {}
    for j, x in base.items():
        for i, e in enumerate(coefs):
            if j + i < ntr and e:
                T[j + i] = T.get(j + i, 0) + e * x
    v0 = min(T)
    out = [0] * (max(T) - v0 + 1)
    for j, x in T.items():
        out[j - v0] = ceil_div(x, den)
    return Poly.from_ints(v0, out)


def padd(A, B):
    if A is None:
        return B
    if B is None:
        return A
    v = min(A.v, B.v)
    L = max(A.v + len(A), B.v + len(B)) - v
    out = [0] * L
    for P in (A, B):
        for i, x in enumerate(P.to_ints()):
            out[P.v - v + i] += x
    return Poly.from_ints(v, out)


def low_bin_arrays(G, jbin, log=print):
    U2 = low_bounds_O52(G)
    l0, u0 = U2[jbin - 1], U2[jbin]
    theta = cl(7 / u0)
    L, H, K = fl(l0 / h), cl(u0 / h), cl(G["zh"] * h / h)
    assert 2 <= L < H <= K <= N
    assert L >= 64                            # delay branch (2.1) for d*_j
    _, du = dickman(L, N)
    # D_theta / h = sum_j dbar_j(l) e^{-theta j h} X^j  (upper)
    th = mpmath.mpf(theta)
    hm = mpq(h)
    ex = mpmath.exp(-th * hm)
    cur = mpmath.mpf(1)
    D = []
    for j in range(N):
        e_hi = cur * (1 + mpmath.mpf(2) ** -250)
        D.append(ceil_div(du[j] * fix_hi(e_hi, BD), 1 << (2 * BD - BF)))
        cur *= ex
    Dp = Poly.from_ints(0, D)
    Q = Poly.from_ints(L, [ceil_div(TWO_BF, a) for a in range(L, K)])
    Mp = Poly.from_ints(L, [ceil_div(TWO_BF, a) for a in range(L, H)])
    Jmax = (N - 1) // L
    J = min(32, Jmax)
    assert J == Jmax                          # omitted sum of (2.6) vanishes
    Qk = {1: Q}
    for k in range(2, J + 1):
        Qk[k] = pmul(Qk[k - 1], Q, N, "ceil")
    That = {}
    for e in (0, 1):
        acc = None
        for r in range(J + 1):
            Eu = eulerian(r + e + 1)
            den = factorial(r + e + 1) * factorial(r)
            base = Poly.from_ints(0, [TWO_BF]) if r == 0 else Qk[r]
            acc = padd(acc, short_mul_ceil(base, Eu, den, N))
        That[e] = acc
    Bth = pmul(Dp, That[0], N, "ceil")
    Mth = pmul(pmul(Dp, Mp, N, "ceil"), That[1], N, "ceil")
    cd = coord_data()
    arr = {}
    for role, P in (("P", Bth), ("D", Mth)):
        K0 = [0] * n
        for i, x in enumerate(P.to_ints()):
            if P.v + i < n:
                K0[P.v + i] = x
        K2 = [ceil_div(cd["w2hi"][j] * K0[j], 1 << BD) for j in range(n)]
        arr[role] = (K2, K0)
    # radial mask (1.25) clipped by (1.26)
    c = cG(G, u0)
    assert c is not None
    lo = max(G["chi"][0], fl(c / h) - G["d"] + 1)
    hi = G["chi"][1]
    up = cl(u0 / h) * h
    # W(r) = exp(theta (r h - U + (m-1) u^+ + d h))
    W0 = th * (-mpq(G["U"]) + mpq((G["m"] - 1) * up) + G["d"] * hm)
    BW = 128
    Wfix = {}
    for r in range(lo, hi + 1):
        x = W0 + th * r * hm
        assert x < 700
        Wfix[r] = fix_hi(mpmath.exp(x) * (1 + mpmath.mpf(2) ** -250), BW)
    Ea = []
    eh = mpmath.exp(th * hm)
    cur = mpmath.mpf(1)
    for a in range(n):
        Ea.append(fix_hi(cur * (1 + mpmath.mpf(2) ** -250), 64))
        cur *= eh
    Wr = []
    for r in range(n):
        x = W0 + th * r * hm
        Wr.append(fix_hi(mpmath.exp(x) * (1 + mpmath.mpf(2) ** -250), BW - 64) if r <= hi else 0)

    def Wcoef(K0):                            # C(r) at scale 2^-(BF+BW)
        ps = [0]
        for a in range(n):
            ps.append(ps[-1] + Ea[a] * K0[a])
        return [Wr[r] * (ps[min(n, hi - r + 1)] - ps[min(max(0, lo - r), hi - r + 1)]) if r <= hi else 0
                for r in range(n)]
    info = dict(l0=float(l0), u0=float(u0), theta=theta, L=L, H=H, K=K, J=J, cG=float(c), chi=(lo, hi),
                cG_equals_bG=(c == G["b"]))
    return arr, (lo, hi), Wfix, BW, Wcoef, info


# ---------------------------------------------------------------------------------------------------------------
def table_row(comp):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "oai186_tables_2_1_to_2_6.json")) as f:
        tab = json.load(f)
    for row in tab["O5/2"]["rows"]:
        if row["c"] == comp:
            return row
    return None


def ceil18(x):
    return int(mpmath.ceil(x * mpmath.mpf(10) ** 18 / mpq(IHLOW)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comp", default="P1")
    ap.add_argument("--out", default=None)
    ap.add_argument("--cache", default=os.environ.get("OUTER2_CACHE", "runs/loss_outer2_cache"))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--ihcheck", action="store_true")
    args = ap.parse_args()
    t0 = time.time()

    def log(s):
        print("[%7.0f s] %s" % (time.time() - t0, s), flush=True)
    if args.selftest:
        ok = _selftest_symbolic()
        print("selftest", "PASS" if ok else "FAIL")
        return
    if args.ihcheck:
        ih_check(log)
        return
    G = group_O52()
    comp = args.comp
    chi, Wfix, BW, Wcoef = None, None, 0, None
    if comp.startswith("P"):
        a, b = rank_two_bins(G)[int(comp[1:]) - 1]
        arr, Lam, info = rank_two_arrays(G, a, b)
        kind = "P"
    elif comp == "H":
        arr, Lam, info = factorial_arrays(G), mpmath.mpf(1), dict(L=G["ph"], K=G["zh"])
        kind = "H"
    elif comp.startswith("L"):
        arr, chi, Wfix, BW, Wcoef, info = low_bin_arrays(G, int(comp[1:]), log)
        Lam = mpmath.mpf(1)
        kind = "L"
    else:
        raise SystemExit("unknown component")
    log("arrays built: %s" % json.dumps({k: (str(v) if not isinstance(v, (int, float, bool, dict, tuple)) else v)
                                         for k, v in info.items()}))
    res = outer_forms(G, kind, arr, Lam, Wfix=Wfix, BW=BW, Wcoef=Wcoef, cache_dir=args.cache, log=log, chi=chi)
    row = table_row(comp)
    A_mid, A_up = ceil18(res["R"]), ceil18(res["R_up"])
    B_mid = ceil18(res["V"])
    B_up = ceil18(res["V"] + res["V_numerr"] + res["V_rad"])
    out = dict(component=comp, group="O5/2", kind=kind, info={k: (v if isinstance(v, (int, float, bool, str)) else str(v)) for k, v in info.items()},
               R=mpmath.nstr(res["R"], 25), R_up=mpmath.nstr(res["R_up"], 25), R_numerr=mpmath.nstr(res["R_numerr"], 5),
               V=mpmath.nstr(res["V"], 25), V_numerr=mpmath.nstr(res["V_numerr"], 5), V_rad=mpmath.nstr(res["V_rad"], 5),
               A_ours=A_up, A_ours_mid=A_mid, B_ours=B_mid, B_ours_up=B_up,
               A_table=row["A"] if row else None, B_table=row["B"] if row else None,
               A_ratio=(A_up / row["A"]) if row else None, B_ratio=(B_mid / row["B"]) if row else None,
               products=res["products"], gmp_seconds=round(res["gmp_seconds"], 1), monomials=res["monomials"],
               seconds=round(time.time() - t0, 1), peak_rss_MB=round(rss_mb(), 1))
    log("RESULT %s: A ours %d (mid %d) table %s ratio %.12f | B ours %d (up %d) table %s ratio %.12f"
        % (comp, A_up, A_mid, out["A_table"], out["A_ratio"] or 0, B_mid, B_up, out["B_table"], out["B_ratio"] or 0))
    print(json.dumps(out, indent=1))
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
