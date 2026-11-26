#!/usr/bin/python3
"""Independent second check of the finite contractions (2.17), (2.19), (2.21)
of "Numerical certificate for prime gaps at most 186" (OpenAI, 30 Aug 2026).

Method (exact rationals only):
  * Toy instances with D coordinates (D = 2, 3, 4 instead of 40), a grid of n
    cells, a finite "fragment level" per coordinate state, three nested outer
    shells with decreasing caps c1 > c2 > c3 (c4 = 0), random rational trial
    coefficients (or the real 77 coefficients), random profile values g_j,
    random positive ring-valued coordinate arrays a_j, random chi, W, w, Lambda.
  * PHYSICAL side by brute force over all state tuples: the step trial F,
    the erased marginal V_i(Y) = sum_X nu(X) F(Y (+)_i X), and the three source
    integrals against an event measure mu that is majorised (cellwise) by
    Lambda * chi(r) W(r) * [*] prod_k (h a_{j_k}).
  * PRINTED side by the source's finite forms: set-partition moments (2.10),
    Q (2.11), affine rows (2.13), S (2.14), rings (2.16), forms (2.17)-(2.21).
  * Tight instances must give equality, random admissible instances must give
    physical <= printed. Negative controls must be caught.
  * sympy checks of the polynomial / ring identities; a grid check of P(u,v);
    a few checks on the real data (caps, w(r) thresholds, P sets).
"""
import itertools
import random
import resource
import sys
import time
from fractions import Fraction as Fr
from math import comb

T_START = time.time()
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)
    sys.stdout.flush()


COUNTS = {"checks": 0, "fail": 0, "neg": 0, "neg_caught": 0}
FAILS = []


CATS = {}
CATKEYS = ["sympy", "P grid", "real", " M", "V_i(Y)", "R tight", "R inequality", "beta tight",
           "beta inequality", "beta identity on", "V tight", "V inequality"]


def check(name, ok):
    cat = next((k.strip() for k in CATKEYS if k in name), "other")
    CATS[cat] = CATS.get(cat, 0) + 1
    COUNTS["checks"] += 1
    if not ok:
        COUNTS["fail"] += 1
        FAILS.append(name)
        say("FAIL", name)


NEG = {}


def negctl(name, caught, vacuous=False):
    """A control is vacuous on an instance when the altered formula has the same
    value as the correct printed formula there; it is then not counted."""
    a, b, c = NEG.get(name, (0, 0, 0))
    if vacuous and not caught:
        NEG[name] = (a, b, c + 1)
        return
    COUNTS["neg"] += 1
    if caught:
        COUNTS["neg_caught"] += 1
    NEG[name] = (a + 1, b + (1 if caught else 0), c)


SIGS = [(), (2,), (3,), (4,), (5,), (6,), (2, 2), (2, 3), (2, 4), (3, 3), (2, 2, 2)]
CINT = [
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
REAL_C = {(SIGS[i], d): Fr(CINT[i][d], 10**10) for i in range(11) for d in range(7)}
ETAS = sorted({tuple(sorted(s + t)) for s in SIGS for t in SIGS}, key=lambda e: (len(e), e))

# ---------------------------------------------------------------- rings
# A ring element is a dict {exponent tuple: Fraction}, truncated by 'orders'.
RINGS = {
    "L": ((2,), (1,)),        # P + yD mod y^2, coefficient [y]
    "P": ((2, 2), (1, 1)),    # P + xA + yB + xyC mod x^2,y^2, coefficient [xy]
    "H": ((4,), (3,)),        # F0 + yF1 + y^2F2 + y^3F3 mod y^4, coefficient [y^3]
}


def rmul(a, b, orders):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(x + y for x, y in zip(ma, mb))
            if all(e < o for e, o in zip(m, orders)):
                out[m] = out.get(m, 0) + ca * cb
    return out


def radd(a, b):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + c
    return out


def rscale(a, c):
    return {m: v * c for m, v in a.items()}


def rone(orders):
    return {(0,) * len(orders): Fr(1)}


def pmul(p, q, orders, n):
    out = [dict() for _ in range(n)]
    for i, a in enumerate(p):
        if not a:
            continue
        for j in range(n - i):
            b = q[j]
            if b:
                out[i + j] = radd(out[i + j], rmul(a, b, orders))
    return out


def set_partitions(labels):
    labels = list(labels)
    if not labels:
        yield []
        return
    first, rest = labels[0], labels[1:]
    for part in set_partitions(rest):
        for k in range(len(part)):
            yield part[:k] + [[first] + part[k]] + part[k + 1:]
        yield [[first]] + part


def falling(d, r):
    out = 1
    for i in range(r):
        out *= d - i
    return out


# ---------------------------------------------------------------- instance
class Inst:
    pass


def rfr(rng, lo=1, hi=9):
    return Fr(rng.randint(lo, hi), rng.randint(1, 9))


def make_instance(seed, D, n, ring, levels, real_coeffs):
    rng = random.Random(seed)
    I = Inst()
    I.seed, I.D, I.n, I.ring = seed, D, n, ring
    I.orders, I.sel = RINGS[ring]
    I.h = Fr(rng.randint(1, 5), rng.randint(6, 12))
    I.t = [(j + Fr(1, 2)) * I.h for j in range(n)]
    I.g = [Fr(rng.randint(1, 20), 10) for _ in range(n)]
    I.Z = sum(x * x for x in I.g)
    I.levels = list(levels)
    I.caps = {1: Fr(5), 2: Fr(4), 3: Fr(2), 4: Fr(0)}
    b1 = rng.randint(0, n - 3)
    b2 = rng.randint(b1 + 1, n - 2)
    I.shellb = (b1, b2)
    I.nu = {(j, lv): rfr(rng) for j in range(n) for lv in I.levels}
    I.states = sorted(I.nu)
    I.dcap = {s: [sum(I.nu[(a, lv)] for lv in I.levels if lv <= I.caps[s]) / I.h for a in range(n)]
              for s in (1, 2, 3)}
    if real_coeffs:
        I.c = dict(REAL_C)
    else:
        I.c = {(s, d): Fr(rng.randint(-9, 9), rng.randint(1, 9)) for s in SIGS for d in range(7)}
    monos = list(itertools.product(*[range(o) for o in I.orders]))
    I.a = [{m: Fr(rng.randint(0, 6), rng.randint(1, 6)) for m in monos} for _ in range(n)]
    I.Lam = rfr(rng)
    I.chi = [1 if rng.random() < 0.8 else 0 for _ in range(n)]
    I.chi[rng.randrange(n)] = 1
    I.W = [rfr(rng) for _ in range(n)]
    I.w = [rfr(rng) for _ in range(n)]
    cand = [Fr(x) for x in (0, 1, 2, 3, 4, 5)]
    u = rng.choice(cand[:-1])
    v = rng.choice([x for x in cand if x > u])
    I.uv = (u, v)
    I.z = rng.choice([Fr(2), Fr(3), Fr(4), Fr(5)])
    I.rng = rng
    return I


def shell(I, r):
    b1, b2 = I.shellb
    return 1 if r <= b1 else 2 if r <= b2 else 3


def chi_s(I, s, r):
    return 1 if (r < I.n and shell(I, r) == s) else 0


def Pset(u, v, caps):
    return [l for l in (1, 2, 3) if max(u, caps[l + 1]) < min(v, caps[l])]


# ---------------------------------------------------------------- physical side
_poly_cache = {}


def poly_value(I, cells):
    """prod g(t_j) * sum c_{sigma,d} (sum t - 9/10)^d prod_k sum_i t_{j_i}^{sigma_k}."""
    key = (id(I), tuple(sorted(cells)))
    if key in _poly_cache:
        return _poly_cache[key]
    ts = [I.t[j] for j in cells]
    gp = Fr(1)
    for j in cells:
        gp *= I.g[j]
    s = sum(ts) - Fr(9, 10)
    tot = Fr(0)
    for sig in SIGS:
        ps = Fr(1)
        for e in sig:
            ps *= sum(x ** e for x in ts)
        rad = sum(I.c[(sig, d)] * s ** d for d in range(7))
        tot += rad * ps
    _poly_cache[key] = gp * tot
    return gp * tot


def F_val(I, sts, capflag=True):
    cells = [j for j, _ in sts]
    r = sum(cells)
    if r >= I.n:
        return Fr(0)
    if capflag and max(lv for _, lv in sts) > I.caps[shell(I, r)]:
        return Fr(0)
    return poly_value(I, cells)


_sel_cache = {}


def sel_prod(I, cells, sel=None, prof=None):
    sel = I.sel if sel is None else sel
    key = (id(I), tuple(sorted(cells)), sel)
    if key not in _sel_cache:
        acc = rone(I.orders)
        for j in cells:
            acc = rmul(acc, I.a[j], I.orders)
        _sel_cache[key] = acc.get(sel, Fr(0))
    return _sel_cache[key]


def bound(I, cells):
    r = sum(cells)
    if r >= I.n or not I.chi[r]:
        return Fr(0)
    return I.Lam * I.chi[r] * I.W[r] * I.h ** len(cells) * sel_prod(I, cells)


def make_mu(I, dim, support, mode, lam_star=None):
    """Event measure on dim-tuples of states, cellwise <= bound, levels in support."""
    rng = I.rng
    lvecs = [lv for lv in itertools.product(I.levels, repeat=dim) if support(max(lv))]
    mu = {}
    for cells in itertools.product(range(I.n), repeat=dim):
        B = bound(I, cells)
        if B == 0:
            continue
        if mode == "tight":
            lv = (lam_star,) * dim
            mu[tuple(zip(cells, lv))] = B
        else:
            f = Fr(rng.randint(0, 4), 4)
            if f == 0:
                continue
            pick = [rng.choice(lvecs) for _ in range(2)]
            wts = [Fr(rng.randint(1, 5)) for _ in pick]
            tw = sum(wts)
            for lv, wt in zip(pick, wts):
                k = tuple(zip(cells, lv))
                mu[k] = mu.get(k, 0) + f * B * wt / tw
    return mu


_V_cache = {}


def V_face(I, Y, i):
    key = (id(I), Y, i)
    if key not in _V_cache:
        tot = Fr(0)
        for X in I.states:
            sts = Y[:i] + (X,) + Y[i:]
            f = F_val(I, sts)
            if f:
                tot += I.nu[X] * f
        _V_cache[key] = tot
    return _V_cache[key]


def phys_R(I, mu, hmode):
    D, rng = I.D, I.rng
    hz = (I.h * I.Z) ** D
    tot = Fr(0)
    hcache = {}
    for sts, m in mu.items():
        f = F_val(I, sts, capflag=(hmode != "tight"))
        if not f:
            continue
        hs = 0
        for i in range(D):
            if hmode == "tight":
                hs += 1
            else:
                k = (i, sts[:i] + sts[i + 1:])
                if k not in hcache:
                    hcache[k] = Fr(rng.randint(0, 3), 3)
                hs += hcache[k]
        tot += hs * m * f * f
    return tot / hz


def phys_beta(I, mu):
    D = I.D
    hz = (I.h * I.Z) ** D
    tot = Fr(0)
    for Y, m in mu.items():
        for i in range(D):
            v = V_face(I, Y, i)
            tot += m * v * v
    return tot / hz


def phys_V(I, mu, hmode):
    D, rng = I.D, I.rng
    hz = (I.h * I.Z) ** D
    tot = Fr(0)
    hcache = {}
    for sts, m in mu.items():
        for i in range(D):
            Y = sts[:i] + sts[i + 1:]
            v = V_face(I, Y, i)
            if not v:
                continue
            rY = sum(j for j, _ in Y)
            wr = I.w[rY] if rY < I.n else Fr(0)
            if hmode == "tight":
                hi = wr
            else:
                k = (i, Y)
                if k not in hcache:
                    hcache[k] = Fr(rng.randint(0, 3), 3) * wr
                hi = hcache[k]
            tot += hi * m * v * v
    return tot / hz


# ---------------------------------------------------------------- printed side
def K_arrays(I, e, Ze=None):
    Ze = (I.Z if e == 2 else Fr(1)) if Ze is None else Ze
    return [rscale(I.a[j], I.g[j] ** e / Ze) for j in range(I.n)]


def moment(I, K, d, eta, opt):
    """(2.10): M_{d,eta}[K] by set partitions (ring-valued polynomial mod X^n)."""
    n, orders = I.n, I.orders
    Pe = {}

    def P(e):
        if e not in Pe:
            Pe[e] = [rscale(K[j], I.t[j] ** e) for j in range(n)]
        return Pe[e]

    one = [rone(orders)] + [dict() for _ in range(n - 1)]
    total = [dict() for _ in range(n)]
    for part in set_partitions(range(len(eta))):
        k = len(part)
        mult = (d ** k) if opt.get("nofall") else falling(d, k)
        if mult == 0:
            continue
        acc = one
        for _ in range(d - k):
            acc = pmul(acc, P(0), orders, n)
        for B in part:
            acc = pmul(acc, P(sum(eta[b] for b in B)), orders, n)
        for r in range(n):
            total[r] = radd(total[r], rscale(acc[r], mult))
    return total


def moment_brute(I, K, d, eta):
    n, orders = I.n, I.orders
    total = [dict() for _ in range(n)]
    for cells in itertools.product(range(n), repeat=d):
        r = sum(cells)
        if r >= n:
            continue
        acc = rone(orders)
        for j in cells:
            acc = rmul(acc, K[j], orders)
        pe = Fr(1)
        for e in eta:
            pe *= sum(I.t[j] ** e for j in cells)
        total[r] = radd(total[r], rscale(acc, pe))
    return total


def xr(I, k):
    return (k + Fr(I.D, 2)) * I.h - Fr(9, 10)


def psig(I, sig, r):
    x = xr(I, r)
    return sum(I.c[(sig, d)] * x ** d for d in range(7))


def Q(I, r, opt):
    out = {}
    for i, s in enumerate(SIGS):
        for j, t in enumerate(SIGS):
            if opt.get("Qonce") and j < i:
                continue
            eta = tuple(sorted(s + t))
            out[eta] = out.get(eta, 0) + psig(I, s, r) * psig(I, t, r)
    return out


def rowsel(I, M, sel):
    return [M[r].get(sel, Fr(0)) for r in range(I.n)]


def printed_R(I, opt):
    D = I.D
    e = 1 if opt.get("prof1") else 2
    K = K_arrays(I, e)
    sel = (1, 0) if opt.get("selx") else I.sel
    fac = 1 if opt.get("Rfactor1") else D
    tot = Fr(0)
    Ms = {eta: rowsel(I, moment(I, K, D, eta, opt), sel) for eta in ETAS}
    for r in range(I.n):
        if not I.chi[r]:
            continue
        q = Q(I, r, opt)
        tot += I.chi[r] * I.W[r] * sum(q[eta] * Ms[eta][r] for eta in ETAS)
    return fac * I.Lam * tot


def affine_rows(I, opt):
    """(2.13): v_{s,tau}(r), r = index sum of the D-1 retained coordinates."""
    n = I.n
    v = {s: {} for s in (1, 2, 3)}
    for s in (1, 2, 3):
        for sig in SIGS:
            for A in itertools.product((0, 1), repeat=len(sig)):
                tau = tuple(sorted(sig[k] for k in range(len(sig)) if not A[k]))
                eA = sum(sig[k] for k in range(len(sig)) if A[k])
                row = v[s].setdefault(tau, [Fr(0)] * n)
                for r in range(n):
                    acc = Fr(0)
                    for a in range(n - r):
                        if not chi_s(I, s, r + a):
                            continue
                        x = xr(I, r) if opt.get("xret") else xr(I, r + a)
                        rad = sum(I.c[(sig, d)] * x ** d for d in range(7))
                        acc += rad * I.g[a] * I.dcap[s][a] * I.t[a] ** eA
                    row[r] += acc
    pref = {}
    run = {}
    for l in (1, 2, 3):
        if opt.get("noshellsum"):
            run = {}
        for tau, row in v[l].items():
            prev = run.get(tau, [Fr(0)] * n)
            run[tau] = [p + q for p, q in zip(prev, row)]
        pref[l] = {k: list(x) for k, x in run.items()}
    return pref


def S_form(I, v, Mrows, A, once=False):
    tot = Fr(0)
    taus = list(v)
    for r in range(I.n):
        if not A[r]:
            continue
        acc = Fr(0)
        for i1, t1 in enumerate(taus):
            for i2, t2 in enumerate(taus):
                if once and i2 < i1:
                    continue
                acc += v[t1][r] * v[t2][r] * Mrows[tuple(sorted(t1 + t2))][r]
        tot += A[r] * acc
    return tot


def printed_beta(I, P, opt, rows=None):
    D = I.D
    e = 1 if opt.get("prof1") else 2
    K = K_arrays(I, e)
    sel = (1, 0) if opt.get("selx") else I.sel
    Mrows = {eta: rowsel(I, moment(I, K, D - 1, eta, opt), sel) for eta in ETAS}
    rows = affine_rows(I, opt) if rows is None else rows
    A = [I.chi[r] * I.W[r] for r in range(I.n)]
    return D * I.h * I.Lam / I.Z * sum(S_form(I, rows[l], Mrows, A, opt.get('Sonce', False)) for l in P)


def printed_V(I, P, opt, rows=None):
    D, n = I.D, I.n
    e = 1 if opt.get("prof1") else 2
    K = K_arrays(I, e)
    K0 = K_arrays(I, 2) if opt.get("erased2") else K_arrays(I, 0)
    sel = (1, 0) if opt.get("selx") else I.sel
    Mfull = {eta: moment(I, K, D - 1, eta, opt) for eta in ETAS}
    C = []
    for r in range(n):
        acc = {}
        for a in range(n - r):
            wt = I.chi[r + a] * (I.W[r] if opt.get("Wret") else I.W[r + a])
            if wt:
                acc = radd(acc, rscale(K0[a], wt))
        C.append(acc)
    H = {eta: [rmul(C[r], Mfull[eta][r], I.orders).get(sel, Fr(0)) for r in range(n)] for eta in ETAS}
    rows = affine_rows(I, opt) if rows is None else rows
    hp = I.h if opt.get("h1") else I.h ** 2
    return D * hp * I.Lam / I.Z * sum(S_form(I, rows[l], H, I.w, opt.get('Sonce', False)) for l in P)


# ---------------------------------------------------------------- toy run
def branch(I, m):
    for l in (1, 2, 3):
        if I.caps[l + 1] < m <= I.caps[l]:
            return l
    return None


def run_instance(I, label):
    D, n = I.D, I.n
    nodef = {}
    say(f"-- instance {label}: D={D} n={n} ring={I.ring} levels={[str(x) for x in I.levels]} "
        f"shells={I.shellb} (u,v]=({I.uv[0]},{I.uv[1]}] z={I.z}")
    # (A) set-partition moments (2.10), ring-valued, vs brute force over cells
    K2 = K_arrays(I, 2)
    for d in range(1, D + 1):
        for eta in ETAS:
            check(f"{label} M{d}{eta}", moment(I, K2, d, eta, nodef) == moment_brute(I, K2, d, eta))
    # (B) erased marginal (2.13) pointwise vs brute-force V_i(Y)
    rows = affine_rows(I, nodef)
    bad = 0
    for Y in itertools.product(I.states, repeat=D - 1):
        cells = [j for j, _ in Y]
        rY = sum(cells)
        m = max(lv for _, lv in Y)
        l = branch(I, m)
        if rY >= n or l is None:
            exp = Fr(0)
        else:
            gp = Fr(1)
            for j in cells:
                gp *= I.g[j]
            s = Fr(0)
            for tau, row in rows[l].items():
                pt = Fr(1)
                for e in tau:
                    pt *= sum(I.t[j] ** e for j in cells)
                s += row[rY] * pt
            exp = I.h * gp * s
        for i in range(D):
            if V_face(I, Y, i) != exp:
                bad += 1
    check(f"{label} V_i(Y)=h*prod g*sum v^(l) P (all Y, all faces)", bad == 0)
    # (C) R_G
    lam_any = min(x for x in I.levels if x <= I.z) if any(x <= I.z for x in I.levels) else None
    supz = lambda mm: 0 < mm <= I.z
    Rpr = printed_R(I, nodef)
    if lam_any is not None:
        mu = make_mu(I, D, supz, "tight", lam_any)
        Rph = phys_R(I, mu, "tight")
        check(f"{label} R tight identity", Rph == Rpr)
        for ctl in ("Rfactor1", "prof1", "Qonce", "nofall") + (("selx",) if I.ring == "P" else ()):
            val = printed_R(I, {ctl: True})
            negctl("R:" + ctl, val != Rph)
            if ctl == "Rfactor1":
                negctl("R:Rfactor1 (inequality)", Rph > val)
    for rep in range(2):
        mu = make_mu(I, D, supz, "random")
        Rph = phys_R(I, mu, "random")
        check(f"{label} R inequality #{rep}", Rph <= Rpr)
    # (D) beta_G with P(u,v)
    u, v = I.uv
    P = Pset(u, v, I.caps)
    supuv = lambda mm: u < mm <= v
    for l in P:
        lo, hi = max(u, I.caps[l + 1]), min(v, I.caps[l])
        cand = [x for x in I.levels if lo < x <= hi]
        if not cand:
            say(f"   (beta tight l={l}: no toy level in branch, skipped)")
            continue
        mu = make_mu(I, D - 1, supuv, "tight", cand[0])
        bph = phys_beta(I, mu)
        bpr = printed_beta(I, [l], nodef, rows)
        check(f"{label} beta tight identity l={l}", bph == bpr)
        for ctl in ("prof1", "Sonce", "nofall", "xret") + (("selx",) if I.ring == "P" else ()) + \
                (("noshellsum",) if l >= 2 else ()):
            val = printed_beta(I, [l], {ctl: True})
            negctl("beta:" + ctl, val != bph, vacuous=(val == bpr))
    bpr = printed_beta(I, P, nodef, rows)
    for rep in range(2):
        mu = make_mu(I, D - 1, supuv, "random")
        check(f"{label} beta inequality #{rep}", phys_beta(I, mu) <= bpr)
    # (E) V_G with P(0,z)
    Pz = Pset(Fr(0), I.z, I.caps)
    for l in Pz:
        lo, hi = max(Fr(0), I.caps[l + 1]), min(I.z, I.caps[l])
        cand = [x for x in I.levels if lo < x <= hi]
        if not cand:
            say(f"   (V tight l={l}: no toy level in branch, skipped)")
            continue
        mu = make_mu(I, D, supz, "tight", cand[-1])
        vph = phys_V(I, mu, "tight")
        vpr = printed_V(I, [l], nodef, rows)
        check(f"{label} V tight identity l={l}", vph == vpr)
        for ctl in ("prof1", "Wret", "erased2", "h1", "xret", "Sonce", "nofall") + \
                (("selx",) if I.ring == "P" else ()):
            val = printed_V(I, [l], {ctl: True})
            negctl("V:" + ctl, val != vph, vacuous=(val == vpr))
    vpr = printed_V(I, Pz, nodef, rows)
    for rep in range(2):
        mu = make_mu(I, D, supz, "random")
        check(f"{label} V inequality #{rep}", phys_V(I, mu, "random") <= vpr)
    # (F) negative control: P with c4 != 0 drops configurations with max <= c4
    caps_bad = dict(I.caps)
    caps_bad[4] = Fr(3, 2)
    low = [x for x in I.levels if x <= Fr(3, 2)]
    if low:
        uu, vv = Fr(0), Fr(3, 2)
        sup = lambda mm: uu < mm <= vv
        mu = make_mu(I, D - 1, sup, "tight", low[0])
        bph = phys_beta(I, mu)
        check(f"{label} beta identity on (0,3/2] with correct P", bph == printed_beta(I, Pset(uu, vv, I.caps), nodef, rows))
        negctl("P:c4!=0 (inequality)", bph > printed_beta(I, Pset(uu, vv, caps_bad), nodef, rows))


# ---------------------------------------------------------------- sympy
def sympy_checks():
    import sympy as sp
    say("== sympy identities")
    # (2.10) symbolic: two cells, symbolic K, t
    K0, K1, t0, t1, X = sp.symbols("K0 K1 t0 t1 X")
    Ks, ts = [K0, K1], [t0, t1]
    Pe = lambda e: K0 * t0 ** e + K1 * t1 ** e * X
    for d in range(1, 4):
        for eta in ETAS:
            brute = 0
            for cells in itertools.product(range(2), repeat=d):
                term = X ** sum(cells)
                for j in cells:
                    term *= Ks[j]
                for e in eta:
                    term *= sum(ts[j] ** e for j in cells)
                brute += term
            form = 0
            for part in set_partitions(range(len(eta))):
                k = len(part)
                term = falling(d, k) * Pe(0) ** (d - k)
                for B in part:
                    term *= Pe(sum(eta[b] for b in B))
                form += term
            check(f"sympy (2.10) d={d} eta={eta}", sp.expand(brute - form) == 0)
    # ring coefficient identities, d = 1..7
    x, y = sp.symbols("x y")
    Pp, A, B, C, Dd, F0, F1, F2, F3 = sp.symbols("P A B C Dd F0 F1 F2 F3")

    def coeff(expr, mon):
        p = sp.Poly(sp.expand(expr), x, y)
        return p.coeff_monomial(mon)
    for d in range(1, 8):
        q = (Pp + x * A + y * B + x * y * C) ** d
        check(f"sympy (1.43) d={d}", sp.expand(coeff(q, x * y) - (d * Pp ** (d - 1) * C + d * (d - 1) * Pp ** max(d - 2, 0) * A * B * (1 if d >= 2 else 0))) == 0)
        q = (Pp + y * Dd) ** d
        check(f"sympy [y](P+yD)^d d={d}", sp.expand(coeff(q, y) - d * Pp ** (d - 1) * Dd) == 0)
        q = (F0 + y * F1 + y ** 2 * F2 + y ** 3 * F3) ** d
        rhs = d * F0 ** (d - 1) * F3
        if d >= 2:
            rhs += d * (d - 1) * F0 ** (d - 2) * F1 * F2
        if d >= 3:
            rhs += comb(d, 3) * F0 ** (d - 3) * F1 ** 3
        check(f"sympy [y^3] factorial ring d={d}", sp.expand(coeff(q, y ** 3) - rhs) == 0)
    # (1.44) splitting of an erased coordinate in the [xy] ring
    Pe_, Ae, Be, Ce, Pr, Ar, Br, Cr = sp.symbols("Pe Ae Be Ce Pr Ar Br Cr")
    prod_ = (Pe_ + x * Ae + y * Be + x * y * Ce) * (Pr + x * Ar + y * Br + x * y * Cr)
    check("sympy (1.44) four placements", sp.expand(coeff(prod_, x * y) - (Ce * Pr + Pe_ * Cr + Ae * Br + Be * Ar)) == 0)
    # affine expansion used in (2.13): prod_k (P_{s_k} + t^{s_k}) = sum_A t^{e(A)} P_{s \ A}
    T = sp.Symbol("ta")
    Psym = {e: sp.Symbol(f"P{e}") for e in range(2, 7)}
    for sig in SIGS:
        lhs = sp.Integer(1)
        for e in sig:
            lhs *= Psym[e] + T ** e
        rhs = 0
        for Amask in itertools.product((0, 1), repeat=len(sig)):
            term = T ** sum(sig[k] for k in range(len(sig)) if Amask[k])
            for k in range(len(sig)):
                if not Amask[k]:
                    term *= Psym[sig[k]]
            rhs += term
        check(f"sympy affine expansion {sig}", sp.expand(lhs - rhs) == 0)
    # (2.24) reversed correlation identity, n = 6
    n = 6
    Isym = sp.symbols("I0:6")
    Ksym = sp.symbols("k0:6")
    Kpoly = sum(Ksym[j] * X ** j for j in range(n))
    rev = sum(Isym[n - 1 - r] * X ** r for r in range(n))
    prodp = sp.Poly(sp.expand(rev * Kpoly), X)
    for j in range(n):
        lhs = sum(Isym[r] * Ksym[r - j] for r in range(j, n))
        check(f"sympy (2.24) j={j}", sp.expand(lhs - prodp.coeff_monomial(X ** (n - 1 - j))) == 0)
    # (2.20) C(r) is the same correlation: C(r) = sum_a I(r+a) K_a
    for r in range(n):
        lhs = sum(Isym[r + a] * Ksym[a] for a in range(n - r))
        rhs = sum(Isym[rr] * Ksym[rr - r] for rr in range(r, n))
        check(f"sympy (2.20) as (2.24) r={r}", sp.expand(lhs - rhs) == 0)


# ---------------------------------------------------------------- P(u,v) grid
def P_by_points(u, v, caps):
    """Independent: (u,v] meets (c_{l+1},c_l] iff some candidate point lies in both."""
    pts = sorted({u, v, caps[1], caps[2], caps[3], caps[4]})
    cand = set(pts) | {(a + b) / 2 for a, b in zip(pts, pts[1:])}
    return [l for l in (1, 2, 3) if any(u < p <= v and caps[l + 1] < p <= caps[l] for p in cand)]


def grid_P(caps, label, bad_caps=None):
    vals = sorted({Fr(0)} | {caps[k] for k in (1, 2, 3)})
    allv = sorted(set(vals) | {(a + b) / 2 for a, b in zip(vals, vals[1:])} | {caps[1] + 1})
    n_ok, n_bad_diff = 0, 0
    for u in allv:
        for v in allv:
            if not u < v:
                continue
            ok = Pset(u, v, caps) == P_by_points(u, v, caps)
            check(f"P grid {label} u={u} v={v}", ok)
            n_ok += ok
            if bad_caps is not None and Pset(u, v, bad_caps) != P_by_points(u, v, caps):
                n_bad_diff += 1
    say(f"   P grid {label}: {n_ok} (u,v) pairs agree with the point test")
    if bad_caps is not None:
        negctl("P grid with c4!=0", n_bad_diff > 0)
        say(f"   negative control c4={bad_caps[4]}: differs on {n_bad_diff} pairs")


# ---------------------------------------------------------------- real data
def real_data():
    say("== real-data checks")
    N = 98304
    rho = Fr(1, 4) + Fr(12499, 10**6)
    g0 = Fr(1, 10**7)
    rs = rho - g0
    S = Fr(2742997, 10**7) / rs
    h = S / N
    T0 = 2 - Fr(3, 1000) - S
    T1 = Fr(251, 1000) / rs
    e = g0 / rho
    check("rho* = 2624989/10^7", rs == Fr(2624989, 10**7))
    check("T0 printed", T0 == Fr(2499106033, 2624989000))
    check("T1 printed", T1 == Fr(2510000, 2624989))
    caps = {1: 68225 * h, 2: 49152 * h, 3: 46580 * h, 4: Fr(0)}
    # w(r) >= h_i: masks of H0 (j <= 89524) and H1 (j <= 89914) for d = 39
    check("H0 mask end 89524 gives (r+39)h <= T0", (89524 + 39) * h <= T0 and (89525 + 39) * h > T0)
    check("H1 mask end 89914 gives (r+39)h <= T1", (89914 + 39) * h <= T1 and (89915 + 39) * h > T1)
    ah, bh = Fr(2479900401, 2500000000), Fr(-843183, 10**9)
    m0, lam, kdef, Kex = Fr(49999, 50000), Fr(1, 125), Fr(1, 50000), Fr(17, 50)
    check("a_h", ah == m0 * m0 - m0 * lam)
    check("b_h", bh == (1 - m0 / lam) * kdef * Kex)
    mx = max(abs(ah + bh), abs(bh))
    check("face multipliers 1, max(|ah+bh|,|bh|), |bh| in [0,1] and ordered", 0 <= abs(bh) <= mx <= 1)
    # P(0, z_G) for the six groups
    zs = {"O2": 49152, "O5/2": 46580, "I2old": 44781, "I5/2old": 35265, "I2new": 44976, "I5/2new": 35419}
    for G, zc in zs.items():
        P = Pset(Fr(0), zc * h, caps)
        check(f"real P(0,z_{G}) point test", P == P_by_points(Fr(0), zc * h, caps))
        say(f"   P(0,z) for {G} (z={zc}h): {P}")
    # P(q-,q+) for inner rank-two bins
    U = {"I2old": (T0 + e, 2), "I5/2old": (T0 + e / 2, Fr(5, 2)),
         "I2new": (T1 + e, 2), "I5/2new": (T1 + e / 2, Fr(5, 2))}
    TL = {"I2old": [0, 1], "I5/2old": [0, Fr(1, 2), 1], "I2new": [0, Fr(1, 6), Fr(1, 2), Fr(2, 3), 1],
          "I5/2new": [0, Fr(1, 8), Fr(3, 8), Fr(1, 2), Fr(3, 4), 1]}
    for G, (UG, m) in U.items():
        q0 = UG / (m + 1)
        z = zs[G] * h
        Ps = []
        for a, b in zip(TL[G], TL[G][1:]):
            qm, qp = q0 + a * (z - q0), q0 + b * (z - q0)
            P = Pset(qm, qp, caps)
            check(f"real P(q-,q+) {G} point test", P == P_by_points(qm, qp, caps) and 0 < qm < qp <= caps[1])
            Ps.append(P)
        say(f"   inner rank-two P(q-,q+) for {G}: {Ps}")
    grid_P(caps, "real caps")


# ---------------------------------------------------------------- main
def main():
    say("oai186_contractions_check2.py: independent toy-model check of (2.17), (2.19), (2.21)")
    plans = [
        (101, 2, 6, "L", [1, 2, 3, 4, 5, 6], False),
        (102, 2, 6, "P", [1, 2, 3, 4, 5, 6], True),
        (103, 2, 6, "H", [1, 2, 3, 4, 5, 6], False),
        (201, 3, 5, "L", [1, 2, 3, 4, 5, 6], True),
        (202, 3, 5, "P", [1, 2, 3, 4, 5, 6], False),
        (203, 3, 5, "H", [1, 2, 3, 4, 5, 6], True),
        (204, 3, 5, "P", [1, 3, 5, 6], True),
        (301, 4, 4, "P", [1, 2, 4, 6], False),
        (302, 4, 4, "L", [2, 3, 5, 6], True),
        (303, 4, 4, "H", [1, 3, 5], False),
    ]
    for seed, D, n, ring, lv, real in plans:
        I = make_instance(seed, D, n, ring, [Fr(x) for x in lv], real)
        t0 = time.time()
        run_instance(I, f"s{seed}")
        say(f"   done in {time.time() - t0:.1f}s; running checks={COUNTS['checks']} fails={COUNTS['fail']}")
        _poly_cache.clear(); _sel_cache.clear(); _V_cache.clear()
    sympy_checks()
    say("== P(u,v) grids")
    toy_caps = {1: Fr(5), 2: Fr(4), 3: Fr(2), 4: Fr(0)}
    grid_P(toy_caps, "toy caps", bad_caps={1: Fr(5), 2: Fr(4), 3: Fr(2), 4: Fr(1)})
    real_data()
    say("== negative controls (name: caught/run, vacuous instances not counted)")
    allneg = True
    for k, (a, b, c) in sorted(NEG.items()):
        say(f"   {k}: {b}/{a}" + (f"  (vacuous on {c})" if c else ""))
        allneg &= (a == b and a > 0)
    say("== summary")
    for k, v in CATS.items():
        say(f"   checks [{k}]: {v}")
    say(f"checks: {COUNTS['checks']}  failures: {COUNTS['fail']}")
    say(f"negative controls: {COUNTS['neg']} run, {COUNTS['neg_caught']} caught")
    if FAILS:
        say("failed:", FAILS[:20])
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    say(f"runtime: {time.time() - T_START:.1f}s  peak RSS: {rss:.0f} MB")
    verdict = COUNTS["fail"] == 0 and allneg
    say("VERDICT:", "PASS" if verdict else "FAIL")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
