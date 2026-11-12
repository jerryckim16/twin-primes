#!/usr/bin/env python3
"""Brute-force validation of capped_check.py on small k.

Method A (exact, independent of capped_check's algebra):
  T is the union over large-set patterns S of the convex polytopes
     {u>=0, u_i<=g (i not in S), u_i>=g (i in S), |u|<=L, sum_S u <= C_|S|}.
  J_T = int_{u' in tau*Delta} int int F(u',t1) F(u',t2) dt1 dt2 du', and the fibre of u' is the
  disjoint union of a 'small' (t<=g) and a 'large' (t>=g) part, so J_T is a sum of integrals of
  P(u',t1) P(u',t2) over convex polytopes in dimension k+1 (patterns of u', t1, t2).
  Each polytope: exact vertex enumeration (Fractions), pulling triangulation from the exact
  vertex/facet incidences, and exact integration of the sympy-expanded polynomial over each
  simplex with int_{std simplex} lam^beta = beta!/(d+|beta|)!.  This yields EXACT rationals,
  compared for equality with capped_check.
Method B (numerical, k=2 only): scipy quad in u1 with breakpoints, inner fibre found by
  scanning candidate breakpoints and testing membership; exact Gauss-Legendre inside.

usage: python3 code/capped_check_tests.py [--slow]
"""
import sys, os, json, itertools, random, time
from fractions import Fraction as Fr
from math import factorial, comb
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capped_check as cc


# ------------------------------------------------------------------ problem helpers
def parse(data):
    q = lambda s: Fr(str(s))
    caps = {str(k): q(v) for k, v in data["caps"].items()}

    def cap(m):
        if str(m) in caps: return caps[str(m)]
        best = max((int(k[:-1]), v) for k, v in caps.items() if k.endswith("+") and int(k[:-1]) <= m)
        return best[1]
    terms = [(a, list(b), q(c)) for (a, b), c in zip(data["basis"], data["coeffs"])]
    return int(data["k"]), q(data["L"]), q(data["tau"]), q(data["g"]), cap, terms


def P_poly(terms, L, us):
    """P evaluated on a list of sympy Poly / numbers us."""
    P1 = sum(us)
    out = 0
    for a, b, c in terms:
        t = c * (L - P1) ** a
        for jj, e in enumerate(b):
            if e: t = t * sum(u ** (jj + 2) for u in us) ** e
        out = out + t
    return out


# ------------------------------------------------------------------ exact polytope machinery
def solve(A, b):
    """exact solve of square system, None if singular"""
    n = len(A)
    M = [list(map(Fr, A[i])) + [Fr(b[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return None
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return tuple(M[i][n] / M[i][i] for i in range(n))


def rank(rows):
    M = [list(r) for r in rows]
    if not M: return 0
    rk, ncol = 0, len(M[0])
    for c in range(ncol):
        p = next((r for r in range(rk, len(M)) if M[r][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[rk])]
        rk += 1
    return rk


def affdim(vs):
    vs = list(vs)
    if not vs: return -1
    v0 = vs[0]
    return rank([[x - y for x, y in zip(v, v0)] for v in vs[1:]])


def vertices(cons, d):
    vs = set()
    for sub in itertools.combinations(range(len(cons)), d):
        x = solve([cons[i][0] for i in sub], [cons[i][1] for i in sub])
        if x is None: continue
        if all(sum(a * xi for a, xi in zip(A, x)) <= bb for A, bb in cons):
            vs.add(x)
    return sorted(vs)


def tight(cons, v):
    return frozenset(i for i, (A, bb) in enumerate(cons) if sum(a * x for a, x in zip(A, v)) == bb)


def triangulate(face, dim, cons, tmap):
    """pulling triangulation of the face (list of vertices, affine dim = dim)"""
    if dim == 0: return [[face[0]]]
    v0 = face[0]
    facets = set()
    for i in range(len(cons)):
        S = frozenset(v for v in face if i in tmap[v])
        if v0 in S or len(S) < dim: continue
        if affdim(S) == dim - 1: facets.add(S)
    out = []
    for S in facets:
        for simp in triangulate(sorted(S), dim - 1, cons, tmap):
            out.append([v0] + simp)
    return out


def poly_integral(cons, d, integrand):
    """exact integral of integrand(list of d linear sympy Polys) over polytope {A x <= b}"""
    vs = vertices(cons, d)
    if len(vs) <= d or affdim(vs) < d: return Fr(0)
    tmap = {v: tight(cons, v) for v in vs}
    lam = sp.symbols("l0:%d" % d)
    total = Fr(0)
    for simp in triangulate(vs, d, cons, tmap):
        v0 = simp[0]
        M = [[simp[j + 1][i] - v0[i] for j in range(d)] for i in range(d)]
        det = sp.Matrix(M).det()
        if det == 0: continue
        xs = [sp.Poly(sp.Rational(v0[i].numerator, v0[i].denominator)
                      + sum(sp.Rational(M[i][j].numerator, M[i][j].denominator) * lam[j] for j in range(d)),
                      *lam, domain="QQ") for i in range(d)]
        f = integrand(xs)
        f = sp.Poly(f, *lam, domain="QQ") if not isinstance(f, sp.Poly) else f
        s = sp.Rational(0)
        for mon, c in f.terms():
            num = 1
            for e in mon: num *= factorial(e)
            s += c * sp.Rational(num, factorial(d + sum(mon)))
        total += Fr(int(sp.Abs(det).p), int(sp.Abs(det).q)) * Fr(int(s.p), int(s.q))
    return total


def brute_I(data):
    k, L, tau, g, cap, terms = parse(data)
    tot = Fr(0)
    for S in itertools.product([0, 1], repeat=k):
        cons = []
        for i in range(k):
            e = [0] * k; e[i] = -1; cons.append((e, 0))
            e = [0] * k
            if S[i]: e[i] = -1; cons.append((e, -g))
            else: e[i] = 1; cons.append((e, g))
        cons.append(([1] * k, L))
        m = sum(S)
        if m: cons.append(([1 if s else 0 for s in S], cap(m)))
        tot += poly_integral(cons, k, lambda xs: P_poly(terms, L, xs) ** 2)
    return tot


def brute_J(data):
    k, L, tau, g, cap, terms = parse(data)
    d = k + 1          # u'_1..u'_{k-1}, t1, t2
    tot = Fr(0)
    for S in itertools.product([0, 1], repeat=k - 1):
        m = sum(S)
        for e1, e2 in itertools.product([0, 1], repeat=2):
            cons = []
            for i in range(k - 1):
                e = [0] * d; e[i] = -1; cons.append((e, 0))
                e = [0] * d
                if S[i]: e[i] = -1; cons.append((e, -g))
                else: e[i] = 1; cons.append((e, g))
            cons.append(([1] * (k - 1) + [0, 0], tau))
            ok = True
            for ti, eps in ((k - 1, e1), (k, e2)):
                e = [0] * d; e[ti] = -1; cons.append((e, 0))
                e = [0] * d
                if eps: e[ti] = -1; cons.append((e, -g))
                else: e[ti] = 1; cons.append((e, g))
                e = [1] * (k - 1) + [0, 0]; e[ti] = 1; cons.append((e, L))
                if eps:   # t large: cap on S + {t}
                    e = list(S) + [0, 0]; e[ti] = 1; cons.append((e, cap(m + 1)))
                elif m:   # t small: cap on S
                    cons.append((list(S) + [0, 0], cap(m)))
            f = lambda xs: P_poly(terms, L, xs[:k - 1] + [xs[k - 1]]) * P_poly(terms, L, xs[:k - 1] + [xs[k]])
            tot += poly_integral(cons, d, f)
    return tot


# ------------------------------------------------------------------ numerical check for k = 2
def numeric_k2(data):
    import numpy as np
    from scipy.integrate import quad
    k, L, tau, g, cap, terms = parse(data)
    assert k == 2
    Lf, gf, tf = float(L), float(g), float(tau)
    C = {m: float(cap(m)) for m in (1, 2, 3)}

    def Pf(u):
        P1 = sum(u); out = 0.0
        for a, b, c in terms:
            t = float(c) * (Lf - P1) ** a
            for jj, e in enumerate(b):
                if e: t *= sum(x ** (jj + 2) for x in u) ** e
            out += t
        return out

    def inT(u):
        if min(u) < 0 or sum(u) > Lf: return False
        big = [x for x in u if x > gf]
        return (not big) or sum(big) <= C[len(big)]

    xs, ws = np.polynomial.legendre.leggauss(40)

    def fibre_int(u1, power):
        cand = sorted({0.0, gf, Lf - u1, Lf} | {C[m] - s for m in (1, 2) for s in (0.0, u1)})
        cand = [c for c in cand if 0 <= c <= Lf]
        tot = 0.0
        for a, b in zip(cand, cand[1:]):
            if b - a < 1e-15 or not inT([u1, (a + b) / 2]): continue
            for x, w in zip(xs, ws):
                t = (a + b) / 2 + (b - a) / 2 * x
                tot += w * (b - a) / 2 * Pf([u1, t]) ** power
        return tot
    consts = [gf, Lf - gf, tf] + [C[m] - s for m in (1, 2) for s in (0, gf)] + [Lf - C[m] for m in (1, 2)]
    pts = sorted({c for c in consts if 0 < c < Lf})
    I = quad(lambda u: fibre_int(u, 2), 0, Lf, points=pts, limit=400, epsabs=1e-14, epsrel=1e-13)[0]
    pts = [p for p in pts if p < tf]
    J = quad(lambda u: fibre_int(u, 1) ** 2, 0, tf, points=pts, limit=400, epsabs=1e-14, epsrel=1e-13)[0]
    return I, J


# ------------------------------------------------------------------ test cases
def rand_P(k, deg, parts, nterms, seed):
    rnd = random.Random(seed)
    basis = []
    def rec(t, rem, cur):
        if t == len(parts):
            for a in range(rem + 1): basis.append((a, tuple(cur)))
            return
        for e in range(rem // parts[t] + 1):
            cur.append(e); rec(t + 1, rem - e * parts[t], cur); cur.pop()
    rec(0, deg, [])
    rnd.shuffle(basis)
    basis = basis[:nterms]
    out_b = []
    for a, b in basis:
        bb = [0] * (max(parts) - 1)
        for j, e in zip(parts, b): bb[j - 2] = e
        out_b.append([a, bb])
    coeffs = ["%d/%d" % (rnd.randint(-9, 9) or 1, rnd.randint(1, 7)) for _ in out_b]
    return out_b, coeffs


CASES = [
    # name, k, L, tau, g, caps, deg, parts, nterms
    ("k2_a", 2, "1", "9/10", "1/5", {"1": "1/2", "2+": "3/5"}, 4, [2, 3], 8),
    ("k2_b", 2, "6/5", "1", "3/10", {"1": "1/2", "2+": "7/10"}, 3, [2, 3], 6),
    ("k3_a", 3, "1", "9/10", "1/5", {"1": "1/2", "2": "1/2", "3+": "3/5"}, 3, [2, 3], 7),
    ("k3_b", 3, "1", "4/5", "3/10", {"1": "3/5", "2": "1/2", "3+": "1/2"}, 3, [2, 4], 6),
    ("k3_c", 3, "521/500", "491/500", "14/125", {"1": "3/5", "2": "3/5", "3+": "17/25"}, 2, [2], 4),
    ("k4_a", 4, "1", "9/10", "1/5", {"1": "1/2", "2": "1/2", "3+": "3/5"}, 2, [2], 4),
]
SLOW_CASES = [   # run with --slow (about 5 minutes for the brute force)
    ("k5_a", 5, "1", "9/10", "1/5", {"1": "1/2", "2": "1/2", "3": "3/5", "4+": "7/10"}, 2, [2], 4),
]


def main():
    outdir = os.environ.get("CAPPED_TEST_DIR")
    allok = True
    cases = CASES + (SLOW_CASES if "--slow" in sys.argv else [])
    for name, k, L, tau, g, caps, deg, parts, nt in cases:
        b, c = rand_P(k, deg, parts, nt, sum(map(ord, name)))
        data = dict(k=k, L=L, tau=tau, g=g, caps=caps, basis=b, coeffs=c)
        if outdir: json.dump(data, open(os.path.join(outdir, name + ".json"), "w"))
        t0 = time.time()
        IT, JT, vals, pb = cc.evaluate(data, log=lambda *a: None)
        t1 = time.time()
        bI, bJ = brute_I(data), brute_J(data)
        t2 = time.time()
        IT, JT = Fr(int(IT.p), int(IT.q)), Fr(int(JT.p), int(JT.q))
        ok = (IT == bI) and (JT == bJ)
        allok &= ok
        line = "%-5s k=%d  I_T=%.15g  J_T=%.15g  exact_match I:%s J:%s  (fast %.1fs, brute %.1fs)" % (
            name, k, float(IT), float(JT), IT == bI, JT == bJ, t1 - t0, t2 - t1)
        if k == 2:
            nI, nJ = numeric_k2(data)
            line += "  | scipy: relerr I %.1e J %.1e" % (abs(nI - float(IT)) / abs(float(IT)),
                                                       abs(nJ - float(JT)) / abs(float(JT)))
        print(line, flush=True)
    print("ALL EXACT MATCH" if allok else "MISMATCH")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
