#!/usr/bin/python3
"""Independent exact check of Maynard/Pintz ratios M = k J / I via iterated
symbolic integration (sympy.integrate with explicit limits), not the Dirichlet
monomial formula. Input data only from pintz_maynard_vectors.json."""
import json, os, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))

def iterated_integral(expr, ts):
    """Integrate polynomial expr over simplex {t>=0, sum t <= 1}:
    innermost t_m from 0 to 1 - (t_1+...+t_{m-1}), then outward.
    Integrates term by term in powers of the current variable, each term
    with sympy.integrate and explicit limits."""
    expr = sp.expand(expr)
    for m in range(len(ts), 0, -1):
        t = ts[m - 1]
        U = 1 - sum(ts[:m - 1])
        P = sp.Poly(expr, t)
        cache = {}
        acc = 0
        for (a,), c in P.terms():
            if a not in cache:
                cache[a] = sp.integrate(t**a, (t, 0, U))
            acc += c * cache[a]
        expr = sp.expand(acc)
    return sp.nsimplify(expr) if not expr.is_Rational else expr

def compute_M(F, ts):
    k = len(ts)
    I = iterated_integral(F**2, ts)
    tk = ts[-1]
    U = 1 - sum(ts[:-1])
    P = sp.Poly(sp.expand(F), tk)
    inner = sp.expand(sum(c * sp.integrate(tk**a, (tk, 0, U)) for (a,), c in P.terms()))
    J = iterated_integral(inner**2, ts[:-1])
    I = sp.Rational(I); J = sp.Rational(J)
    return I, J, sp.Rational(k) * J / I

def main():
    out = []
    def log(s):
        print(s); sys.stdout.flush(); out.append(s)
    allok = True
    # (a) Maynard 2015 eq. (8.17), k = 5
    k = 5
    ts = sp.symbols('t1:%d' % (k + 1))
    P1 = sum(ts); P2 = sum(t**2 for t in ts)
    F = (1 - P1) * P2 + sp.Rational(7, 10) * (1 - P1)**2 + sp.Rational(1, 14) * P2 - sp.Rational(3, 14) * (1 - P1)
    I, J, M = compute_M(F, ts)
    exp = sp.Rational(1417255, 708216)
    ok = (M == exp); allok &= ok
    log("(a) k=5 Maynard (8.17): I=%s J=%s" % (I, J))
    log("    M = %s  expected %s  equal=%s  M~%s" % (M, exp, ok, sp.N(M, 20)))
    # (b) vectors
    data = json.load(open(os.path.join(HERE, 'pintz_maynard_vectors.json')))
    for K in (2, 3, 4, 5):
        d = data['k%d_deg6' % K]
        basis = d["basis (b,c) for (1-P1)^b P2^c"]
        coeffs = [sp.Rational(c) for c in d['coeffs']]
        ts = sp.symbols('t1:%d' % (K + 1))
        P1 = sum(ts); P2 = sum(t**2 for t in ts)
        F = sum(c * (1 - P1)**b * P2**cc for c, (b, cc) in zip(coeffs, basis))
        I, J, M = compute_M(F, ts)
        exp = sp.Rational(d['ratio'])
        ok = (M == exp); allok &= ok
        log("(b) k=%d deg6: M = %s" % (K, M))
        log("    equals JSON ratio: %s ; M ~ %s ; 1/M ~ %s" % (ok, sp.N(M, 20), sp.N(1 / M, 20)))
    log("ALL MATCH: %s" % allok)
    open(os.path.join(HERE, 'pintz_maynard_check2.out'), 'w').write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
