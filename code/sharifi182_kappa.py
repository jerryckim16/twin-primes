#!/usr/bin/env python3
"""Independent recomputation of the sharp five-prime mass deficit kappa_true of the 182 preprint
(GPT-6 Astra / R. Sharifi, bundle [M], Sec. 4.4-4.5, (4.2)-(4.11); Sec. 13.3 for kappa_cvx).

Definition (4.2), as transcribed in notes/sources-182-kappa.md:
    P_a = {(al1..al4): al1 > al2 > al3 > al4 > al5 > 0, al5 = 1 - sum_{j<=4} al_j, al1 + al2 < a},
    kappa_true = 24 * int_{P_a} dal1 dal2 dal3 dal4 / (al1 al2 al3 al4 al5),   a = 41361/100000.

Method A (mine, no simplices): the al4 integral is done in closed form,
    int_{s/2}^{al3} dal4 / (al4 (s - al4)) = (1/s) log(al3/(s - al3)),   s = 1 - al1 - al2 - al3,
which needs al3 > s/2, i.e. 3 al3 > 1 - al1 - al2. The remaining 3-dim region is
    al2 < al1, al1 + al2 < a, al1 + 4 al2 > 1,  (1 - al1 - al2)/3 < al3 < al2,
and is integrated by tensor Gauss-Legendre (mpmath, high precision) on the 2 pieces where the
integrand is analytic on the closed piece (break at al2 = 1/5). Error estimate: difference
between two node counts. A raw 4-dim float64 Gauss-Legendre (no closed-form step) is a sanity check.

Method B (paper's route): rebuild P_E from (4.5), enumerate its vertices exactly, check the printed
vertex table, triangulation, volumes (4.7) and r_Sigma, then evaluate (4.8)-(4.11) exactly in
rationals (python-flint polynomials, Dirichlet moments (4.9)), at D = 22 (paper) and at a larger D.
Also the convexity (vertex-average) bound of Sec. 13.3.

Run:  /usr/bin/python3 -I code/sharifi182_kappa.py [--selftest] [--out code/data182/kappa_result.json]
"""
import argparse
import itertools
import json
import math
import sys
import time
from fractions import Fraction as Fr

import mpmath
from mpmath import mp, mpf
from mpmath.calculus.quadrature import GaussLegendre

A_CUT = Fr(41361, 100000)
U = A_CUT - Fr(2, 5)                    # 1361/100000
LAM = 1 - 2 * A_CUT                     # .17278
KBAR = Fr(46653544162031, 500000000000000000)
KCVX = Fr(11696, 125000000)
PRINTED_LO = Fr(93307088324061, 10**18)
PRINTED_HI = Fr(93307088324062, 10**18)


# ----------------------------------------------------------------------------------------------
# Method A
# ----------------------------------------------------------------------------------------------
def gl_nodes(degree):
    """Gauss-Legendre nodes/weights on [-1,1] (3*2^(degree-1) points) at current precision."""
    return GaussLegendre(mp).calc_nodes(degree, mp.prec + 20)


def gl_interval(nodes, lo, hi):
    h = (hi - lo) / 2
    m = (hi + lo) / 2
    return [(m + h * x, h * w) for (x, w) in nodes]


def method_A(a, degree, inner="log", dps=40):
    """inner='log': kappa_true. inner='vol': 24 * vol(P_a) (integrand 1), for a polynomial check."""
    mp.dps = dps
    a = mpf(a.numerator) / a.denominator
    nodes = gl_nodes(degree)
    one = mpf(1)
    total = mpf(0)
    lo2, br, hi2 = (one - a) / 3, one / 5, a / 2
    for (p_lo, p_hi) in ((lo2, br), (br, hi2)):
        for (al2, w2) in gl_interval(nodes, p_lo, p_hi):
            l1 = max(al2, one - 4 * al2)
            u1 = a - al2
            acc1 = mpf(0)
            for (al1, w1) in gl_interval(nodes, l1, u1):
                c = one - al1 - al2
                acc3 = mpf(0)
                for (al3, w3) in gl_interval(nodes, c / 3, al2):
                    s = c - al3
                    if inner == "log":
                        val = mpmath.log(al3 / (s - al3)) / (s * al3)
                    else:
                        val = al3 - s / 2          # length of the al4-interval
                    acc3 += w3 * val
                if inner == "log":
                    acc1 += w1 * acc3 / al1
                else:
                    acc1 += w1 * acc3
            total += (w2 * acc1 / al2) if inner == "log" else (w2 * acc1)
    return 24 * total


def method_A_raw4d(a, n=48):
    """Sanity check: raw 4-dim tensor GL of the original integrand (float64), no closed-form step.
    Order: al2 (pieces), al1, al3 in [(1-al1-al2)/3, al2], al4 in [s/2, al3]."""
    import numpy as np
    a = float(a)
    x, w = np.polynomial.legendre.leggauss(n)

    def iv(lo, hi):
        h = (hi - lo) / 2
        return (hi + lo)[..., None] / 2 + h[..., None] * x, h[..., None] * w

    tot = 0.0
    for lo, hi in (((1 - a) / 3, 0.2), (0.2, a / 2)):
        a2, w2 = iv(np.array(lo), np.array(hi))                       # (n,)
        a1, w1 = iv(np.maximum(a2, 1 - 4 * a2), a - a2)             # (n,n)
        a2b = np.broadcast_to(a2[:, None], a1.shape)
        c = 1 - a1 - a2b
        a3, w3 = iv(c / 3, a2b)                                      # (n,n,n)
        s = c[..., None] - a3
        a4, w4 = iv(s / 2, a3)                                       # (n,n,n,n)
        a5 = s[..., None] - a4
        f = 1.0 / (a1[..., None, None] * a2b[..., None, None] * a3[..., None] * a4 * a5)
        tot += np.einsum("i,ij,ijk,ijkl,ijkl->", w2, w1, w3, w4, f)
    return 24 * tot


# ----------------------------------------------------------------------------------------------
# Method B
# ----------------------------------------------------------------------------------------------
V_PRINTED = [
    (Fr(-1, 3), Fr(-1, 3), Fr(-1, 3), Fr(-1, 3)),
    (Fr(0), Fr(0), Fr(0), Fr(0)),
    (Fr(1, 2), Fr(1, 2), Fr(-3, 4), Fr(-3, 4)),
    (Fr(1, 2), Fr(1, 2), Fr(-1, 3), Fr(-1, 3)),
    (Fr(1, 2), Fr(1, 2), Fr(1, 2), Fr(-2)),
    (Fr(1, 2), Fr(1, 2), Fr(1, 2), Fr(-3, 4)),
    (Fr(4, 3), Fr(-1, 3), Fr(-1, 3), Fr(-1, 3)),
]
SIMPLICES = [(0, 1, 3, 5, 6), (0, 2, 3, 5, 6), (0, 2, 4, 5, 6)]
V_VOL_PRINTED = [Fr(125, 5184), Fr(625, 20736), Fr(625, 6912)]
R_PRINTED = [Fr(1361, 15000), Fr(1361, 15000), Fr(1361, 10000)]


def z5(z):
    return -sum(z)


def PE_constraints():
    """(4.5) as rows (c, b) meaning c.z <= b, c in Q^4."""
    rows = []
    for i in range(4):                      # z_i >= -2
        c = [0] * 4; c[i] = -1; rows.append((c, 2))
    rows.append(([1, 1, 1, 1], 2))          # z5 >= -2  <=>  z1+..+z4 <= 2
    for i in range(3):                      # z_i >= z_{i+1}
        c = [0] * 4; c[i] = -1; c[i + 1] = 1; rows.append((c, 0))
    rows.append(([1, 1, 1, 2], 0))
    rows.append(([1, 1, 0, 0], 1))
    rows.append(([0, -1, -1, -1], 1))       # z2+z3+z4 >= -1
    return [([Fr(x) for x in c], Fr(b)) for c, b in rows]


def PE_from_alpha_definition(z):
    """My own derivation of the first labelled region of E1 on the hyperplane, in z-coords:
    al4 < al3 < al2 < al1, al5 > al4, every pair < a  (al_i = 1/5 + u z_i). Closed version."""
    al = [Fr(1, 5) + U * zi for zi in z] + [Fr(1, 5) + U * z5(z)]
    ok = al[0] >= al[1] >= al[2] >= al[3] and al[4] >= al[3]
    ok = ok and all(al[i] + al[j] <= A_CUT for i in range(5) for j in range(i + 1, 5))
    return ok and all(x > 0 for x in al)


def solve4(M, b):
    import sympy
    Ms = sympy.Matrix(M)
    if Ms.det() == 0:
        return None
    sol = Ms.LUsolve(sympy.Matrix(b))
    return tuple(Fr(int(sympy.fraction(x)[0]), int(sympy.fraction(x)[1])) for x in sol)


def enumerate_vertices(rows):
    verts = set()
    for sub in itertools.combinations(range(len(rows)), 4):
        sol = solve4([[sympy_rat(x) for x in rows[k][0]] for k in sub], [sympy_rat(rows[k][1]) for k in sub])
        if sol is None:
            continue
        if all(sum(ci * zi for ci, zi in zip(c, sol)) <= bb for c, bb in rows):
            verts.add(sol)
    return sorted(verts)


def sympy_rat(x):
    import sympy
    return sympy.Rational(x.numerator, x.denominator)


def det_frac(M):
    import sympy
    d = sympy.Matrix([[sympy_rat(x) for x in r] for r in M]).det()
    n, q = sympy.fraction(d)
    return Fr(int(n), int(q))


def simplex_volume(P):
    return abs(det_frac([[P[k][i] - P[0][i] for i in range(4)] for k in range(1, 5)])) / 24


def exact_volume_PE(verts):
    """Exact volume of conv(verts): combinatorial Delaunay (qhull) + exact determinants."""
    import numpy as np
    from scipy.spatial import Delaunay
    pts = np.array([[float(x) for x in v] for v in verts])
    tri = Delaunay(pts)
    return sum((simplex_volume([verts[k] for k in s]) for s in tri.simplices), Fr(0)), len(tri.simplices)


def density(z):
    """6 u^4 / prod_{i<=5}(1/5 + u z_i)  (integrand of (4.6) incl. prefactor)."""
    p = Fr(1)
    for zi in list(z) + [z5(z)]:
        p *= Fr(1, 5) + U * zi
    return 6 * U ** 4 / p


def moment_series(simplex_pts, D):
    """Return list S_n = E_Sigma[h_n(B_1..B_5)] (exact Fractions), n = 0..D, B_i = -12 z_i(t)."""
    import flint
    ctx = flint.fmpz_mpoly_ctx.get(("t", 5), "lex")
    t = ctx.gens()
    zs = []
    for i in range(4):
        zs.append([simplex_pts[j][i] for j in range(5)])
    zs.append([z5(simplex_pts[j]) for j in range(5)])
    B = []
    for coeffs in zs:
        cc = [-12 * c for c in coeffs]
        assert all(x.denominator == 1 for x in cc), "B_i not integral"
        B.append(sum((int(cc[j]) * t[j] for j in range(5)), ctx.from_dict({})))
    # H[i][n] recurrence, keep only current column over i
    fact = [math.factorial(k) for k in range(D + 5)]
    H_prev = [ctx.from_dict({(0,) * 5: 1})] * 6       # H_{i,0} = 1 for i>=1 ; H_{0,0} irrelevant
    S = [Fr(1)]
    for n in range(1, D + 1):
        H_cur = [ctx.from_dict({})]                   # H_{0,n} = 0
        for i in range(1, 6):
            H_cur.append(H_cur[i - 1] + B[i - 1] * H_prev[i])
        hn = H_cur[5]
        tot = 0
        for exps, c in hn.terms():
            pr = int(c)
            for e in exps:
                pr *= fact[e]
            tot += pr
        S.append(Fr(24 * tot, fact[n + 4]))
        H_prev = H_cur
    return S


def T_tail(r, D):
    return 1 / (1 - r) ** 5 - sum((math.comb(n + 4, 4) * r ** n for n in range(D + 1)), Fr(0))


def method_B(D_paper=22, D_high=44, log=print):
    out = {}
    rows = PE_constraints()
    verts = enumerate_vertices(rows)
    out["vertices_enumerated"] = [[str(x) for x in v] for v in verts]
    out["vertices_match_printed"] = sorted(verts) == sorted(V_PRINTED)
    # P_E from (4.5) == region derived from the alpha-definition: compare on vertices + random rationals
    import random
    rnd = random.Random(1)
    agree = True
    for _ in range(20000):
        z = tuple(Fr(rnd.randint(-2400, 1600), 1200) for _ in range(4))
        in45 = all(sum(ci * zi for ci, zi in zip(c, z)) <= bb for c, bb in rows)
        agree &= (in45 == PE_from_alpha_definition(z))
    out["PE_45_equals_alpha_definition_on_20000_rational_points"] = agree
    volPE, ntri = exact_volume_PE(verts)
    out["vol_PE_exact_independent"] = str(volPE)
    vols, rs = [], []
    halfspace = [lambda z: z[2] + 2 * z[3] >= -1,
                 lambda z: z[2] + 2 * z[3] <= -1 <= z[1] + 2 * z[3],
                 lambda z: z[1] + 2 * z[3] <= -1]
    cut_ok = True
    for j, s in enumerate(SIMPLICES):
        P = [V_PRINTED[k] for k in s]
        vols.append(simplex_volume(P))
        rs.append(5 * U * max(abs(x) for v in P for x in list(v) + [z5(v)]))
        cut_ok &= all(halfspace[j](v) for v in P)
        cut_ok &= all(PE_from_alpha_definition(v) for v in P)
    out["simplex_volumes"] = [str(v) for v in vols]
    out["simplex_volumes_match_printed"] = vols == V_VOL_PRINTED
    out["sum_volumes"] = str(sum(vols))
    out["triangulation_covers_PE"] = cut_ok and sum(vols) == volPE
    out["r_Sigma"] = [str(r) for r in rs]
    out["r_Sigma_match_printed"] = rs == R_PRINTED
    v = 5 * U / 12
    pref = 6 * 5 ** 5 * U ** 4
    t0 = time.time()
    lo = hi = mid_high = Fr(0)
    tail_hi = Fr(0)
    contrib = []
    for j, s in enumerate(SIMPLICES):
        P = [V_PRINTED[k] for k in s]
        S = moment_series(P, D_high)
        A22 = sum((v ** n * S[n] for n in range(D_paper + 1)), Fr(0))
        T22 = T_tail(rs[j], D_paper)
        lo += pref * vols[j] * (A22 - T22)
        hi += pref * vols[j] * (A22 + T22)
        Ah = sum((v ** n * S[n] for n in range(D_high + 1)), Fr(0))
        Th = T_tail(rs[j], D_high)
        mid_high += pref * vols[j] * Ah
        tail_hi += pref * vols[j] * Th
        contrib.append(pref * vols[j] * Ah)
        log(f"  simplex {j+1}: done ({time.time()-t0:.1f}s)")
    out["D_paper"] = D_paper
    out["interval_D22_lo"] = mpmath.nstr(mpf(lo.numerator) / lo.denominator, 30)
    out["interval_D22_hi"] = mpmath.nstr(mpf(hi.numerator) / hi.denominator, 30)
    out["interval_D22_width"] = mpmath.nstr(mpf((hi - lo).numerator) / (hi - lo).denominator, 5)
    out["printed_bracket_contains_D22_interval"] = PRINTED_LO < lo and hi < PRINTED_HI
    out["D_high"] = D_high
    out["kappa_B_high"] = mpmath.nstr(mpf(mid_high.numerator) / mid_high.denominator, 40)
    out["kappa_B_high_tail_bound"] = mpmath.nstr(mpf(tail_hi.numerator) / tail_hi.denominator, 5)
    out["per_simplex_contribution"] = [mpmath.nstr(mpf(c.numerator) / c.denominator, 30) for c in contrib]
    # convexity bound, Sec. 13.3
    cvx = sum((vols[j] * sum((density(V_PRINTED[k]) for k in s), Fr(0)) / 5
               for j, s in enumerate(SIMPLICES)), Fr(0))
    out["kappa_cvx_vertex_average_exact"] = f"{cvx.numerator}/{cvx.denominator}"
    out["kappa_cvx_vertex_average"] = mpmath.nstr(mpf(cvx.numerator) / cvx.denominator, 30)
    out["kappa_cvx_vertex_average_le_11696/125000000"] = cvx <= KCVX
    out["_exact"] = dict(lo=lo, hi=hi, mid=mid_high, tail=tail_hi, cvx=cvx)
    return out


# ----------------------------------------------------------------------------------------------
# self-test
# ----------------------------------------------------------------------------------------------
def selftest():
    import random
    import sympy
    ok = True
    mp.dps = 60
    # 1. Dirichlet moment formula (4.9) vs sympy on the standard 4-simplex (t0 = 1 - t1 - .. - t4)
    t1, t2, t3, t4 = sympy.symbols("t1:5", positive=True)
    for b in [(0, 0, 0, 0, 0), (2, 1, 0, 0, 0), (0, 1, 2, 0, 1), (3, 0, 0, 1, 1)]:
        f = (1 - t1 - t2 - t3 - t4) ** b[0] * t1 ** b[1] * t2 ** b[2] * t3 ** b[3] * t4 ** b[4]
        I = sympy.integrate(f, (t4, 0, 1 - t1 - t2 - t3), (t3, 0, 1 - t1 - t2), (t2, 0, 1 - t1), (t1, 0, 1))
        E = I * 24
        n = sum(b)
        pred = sympy.Rational(24 * math.prod(math.factorial(x) for x in b), math.factorial(n + 4))
        ok &= (sympy.simplify(E - pred) == 0)
    print("selftest Dirichlet moments:", ok)
    # 2. moment_series engine on a toy with closed form: one linear form B_1 = k t_0, others 0.
    #    t0 ~ Beta(1,4) under the uniform simplex measure; closed form by sympy (logs).
    toy = [(Fr(1), Fr(0), Fr(0), Fr(0))] + [(Fr(0),) * 4] * 4     # z1 = t0 on vertex 0, so B1 = -12 t0
    S = moment_series(toy, 40)
    # z1 = t0, z5 = -t0: B1 = -12 t0, B5 = +12 t0, others 0 -> prod = 1/((1 + 12 v t0)(1 - 12 v t0))
    c = Fr(1, 50)
    series = sum((c ** n / Fr(12) ** n * S[n] for n in range(41)), Fr(0))   # v = c/12
    tt = sympy.symbols("tt")
    cc = sympy.Rational(1, 50)
    exact = sympy.integrate(4 * (1 - tt) ** 3 / ((1 + cc * tt) * (1 - cc * tt)), (tt, 0, 1))
    err = abs(mpf(series.numerator) / series.denominator - mpmath.mpf(sympy.N(exact, 50)))
    print("selftest series engine vs closed form (Beta toy): err =", mpmath.nstr(err, 3))
    ok &= err < mpf(10) ** -45
    # 3. Method A closed-form al4 step vs direct numerical al4 integral at random points
    mp.dps = 30
    a = mpf(41361) / 100000
    rnd = random.Random(2)
    worst = mpf(0)
    for _ in range(20):
        al2 = (1 - a) / 3 + (a / 2 - (1 - a) / 3) * rnd.random()
        l1 = max(al2, 1 - 4 * al2); al1 = l1 + (a - al2 - l1) * rnd.random()
        c_ = 1 - al1 - al2; al3 = c_ / 3 + (al2 - c_ / 3) * rnd.random()
        s = c_ - al3
        closed = mpmath.log(al3 / (s - al3)) / s
        num = mpmath.quad(lambda x: 1 / (x * (s - x)), [s / 2, al3])
        worst = max(worst, abs(closed - num))
    print("selftest al4 closed form: max err =", mpmath.nstr(worst, 3))
    ok &= worst < mpf(10) ** -25
    # 4. Two-prime toy with closed form, using the same GL nodes: int_{1/2}^{a} dx/(x(1-x)) = log(a/(1-a))
    nodes = gl_nodes(5)
    q = sum(w / (x * (1 - x)) for x, w in gl_interval(nodes, mpf(1) / 2, a))
    err = abs(q - mpmath.log(a / (1 - a)))
    print("selftest 2-prime toy GL: err =", mpmath.nstr(err, 3))
    ok &= err < mpf(10) ** -25
    # 5. 24 labelings: B1 has 4, B2 has 20 (brute force over permutations)
    b1 = sum(1 for p in itertools.permutations(range(5))
             if p[3] < p[2] < p[1] < p[0] and p[4] > p[3])
    b2 = sum(1 for p in itertools.permutations(range(5))      # labels 2..6 -> p[0..4]
             if p[1] < p[0] and p[1] < p[2] and p[4] > p[3])
    print("selftest labelings B1, B2:", b1, b2)
    ok &= (b1, b2) == (4, 20)
    # 6. vol(P_a) via method A (polynomial integrand, exact up to GL rounding) vs 4 vol(P_a) = u^4 vol(P_E)
    vA = method_A(A_CUT, 3, inner="vol", dps=30) / 24
    vB = U ** 4 * Fr(125, 864) / 4
    err = abs(vA - mpf(vB.numerator) / vB.denominator)
    print("selftest vol(P_a) A vs u^4*125/864/4: err =", mpmath.nstr(err, 3))
    ok &= err < mpf(10) ** -35
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--dps", type=int, default=45)
    ap.add_argument("--degA", type=int, nargs=2, default=[4, 5], help="two GL degrees (3*2^(d-1) nodes)")
    ap.add_argument("--Dhigh", type=int, default=44)
    args = ap.parse_args()
    if args.selftest:
        sys.exit(0 if selftest() else 1)
    T0 = time.time()
    res = {"source": "Sharifi/GPT-6 Astra 182 bundle, Sec. 4.4-4.5 (4.2)-(4.11), Sec. 13.3",
           "status": "Computed", "a": str(A_CUT), "u": str(U)}
    # Method A
    tA = time.time()
    vals = []
    for d in args.degA:
        vals.append(method_A(A_CUT, d, dps=args.dps))
        print(f"method A, GL degree {d} ({3*2**(d-1)} nodes/dim): {mpmath.nstr(vals[-1], 40)}")
    errA = abs(vals[1] - vals[0])
    res["method_A"] = {
        "description": "closed-form al4 integral, then 3-dim tensor Gauss-Legendre (mpmath) on 2 analytic pieces "
                       "of my own derivation of P_a; no simplex decomposition",
        "dps": args.dps, "gl_nodes_per_dim": [3 * 2 ** (d - 1) for d in args.degA],
        "values": [mpmath.nstr(x, 40) for x in vals],
        "kappa_A": mpmath.nstr(vals[1], 40),
        "error_estimate_of_coarser": mpmath.nstr(errA, 3),
        "seconds": round(time.time() - tA, 1)}
    raw = method_A_raw4d(A_CUT, 48)
    res["method_A"]["raw4d_float64_GL48_sanity"] = repr(raw)
    print("raw 4-d float GL48:", repr(raw))
    # Method B
    tB = time.time()
    B = method_B(22, args.Dhigh)
    ex = B.pop("_exact")
    B["seconds"] = round(time.time() - tB, 1)
    res["method_B"] = B
    for k, v in B.items():
        print(f"  B.{k}: {v}")
    kA = vals[1]
    kB = mpf(ex["mid"].numerator) / ex["mid"].denominator
    diff = abs(kA - kB)
    res["comparison"] = {
        "abs_diff_A_minus_B_high": mpmath.nstr(diff, 3),
        "agreeing_significant_digits": int(mpmath.floor(-mpmath.log10(diff / kB))) if diff > 0 else ">dps",
        "printed_bracket": [".000093307088324061", ".000093307088324062"],
        "printed_bracket_contains_A": bool(mpf(PRINTED_LO.numerator) / PRINTED_LO.denominator < kA
                                           < mpf(PRINTED_HI.numerator) / PRINTED_HI.denominator),
        "printed_bracket_contains_B_rigorous_D22": B["printed_bracket_contains_D22_interval"],
        "kappa_bar": f"{KBAR.numerator}/{KBAR.denominator}",
        "kappa_bar_equals_printed_upper_end": KBAR == PRINTED_HI,
        "kappa_true_lt_kappa_bar_rigorous": ex["hi"] < KBAR,
        "kappa_bar_minus_kappa_true": mpmath.nstr(mpf(KBAR.numerator) / KBAR.denominator - kB, 5),
        "kappa_cvx": "11696/125000000",
        "kappa_bar_lt_kappa_cvx": KBAR < KCVX,
        "vertex_average_le_kappa_cvx": ex["cvx"] <= KCVX,
        "kappa_cvx_minus_vertex_average": mpmath.nstr(mpf(KCVX.numerator) / KCVX.denominator
                                                       - mpf(ex["cvx"].numerator) / ex["cvx"].denominator, 5),
    }
    res["total_seconds"] = round(time.time() - T0, 1)
    print(json.dumps(res["comparison"], indent=1))
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=1)
        print("wrote", args.out)


if __name__ == "__main__":
    main()
