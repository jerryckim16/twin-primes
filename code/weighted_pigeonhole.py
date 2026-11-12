#!/usr/bin/env python3
"""Numerical check of the 'pigeonhole rigidity' proposition for k = 3.

M_3[c] = sup_F sum_i c_i J_i(F) / I(F) over polynomials F on the simplex R_3
(no symmetry imposed).  The proposition predicts
   M_3[(1/2,1,1/2)] <= M_2,   M_3[(1,1,0)] = M_2,   M_3[(1,1,1)] = M_3.
"""
import itertools, sys
from fractions import Fraction as Fr
from math import factorial, comb
import mpmath as mp
mp.mp.dps = 60

def dirichlet(exps):                 # int over simplex of prod t_i^{e_i}
    k = len(exps); num = 1
    for e in exps: num *= factorial(e)
    return Fr(num, factorial(k + sum(exps)))

def matrices(deg):
    mons = [m for m in itertools.product(range(deg+1), repeat=3) if sum(m) <= deg]
    n = len(mons)
    I = [[dirichlet([a+x, b+y, c+z]) for (x, y, z) in mons] for (a, b, c) in mons]
    Js = []
    for i in range(3):
        # integrate out t_i:  int_0^{1-x-y} t^a dt = (1-x-y)^{a+1}/(a+1), expand in x,y
        red = []
        for m in mons:
            a = m[i]; others = [m[j] for j in range(3) if j != i]
            poly = {}
            for p in range(a+2):
                for q in range(a+2-p):
                    coef = Fr(factorial(a+1), factorial(p)*factorial(q)*factorial(a+1-p-q))*(-1)**(p+q)/(a+1)
                    key = (others[0]+p, others[1]+q)
                    poly[key] = poly.get(key, 0) + coef
            red.append(poly)
        J = [[sum(c1*c2*dirichlet([e1[0]+e2[0], e1[1]+e2[1]]) for e1, c1 in red[u].items() for e2, c2 in red[v].items())
              for v in range(n)] for u in range(n)]
        Js.append(J)
    return mons, I, Js

def top(I, Js, c):
    n = len(I); f = lambda q: mp.mpf(q.numerator)/q.denominator
    A = mp.matrix(n, n); B = mp.matrix(n, n)
    for u in range(n):
        for v in range(n):
            A[u, v] = f(I[u][v]); B[u, v] = sum(ci*f(J[u][v]) for ci, J in zip(c, Js))
    L = mp.cholesky(A); Li = mp.inverse(L); C = Li*B*Li.T; C = (C + C.T)/2
    E, _ = mp.eigsy(C)
    return max(E)

if __name__ == "__main__":
    deg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    mons, I, Js = matrices(deg)
    for name, c in (("(1,1,1)", (1, 1, 1)), ("(1,1,0)", (1, 1, 0)), ("(1/2,1,1/2)", (0.5, 1, 0.5)),
                    ("(1,0,1)", (1, 0, 1)), ("(3/4,1,1/4)", (0.75, 1, 0.25))):
        print("deg %d  c=%-12s  lower bound for M_3[c] = %s" % (deg, name, mp.nstr(top(I, Js, c), 10)))
    print("reference: M_2 = 1/(1-W(1/e)) =", mp.nstr(1/(1-mp.lambertw(1/mp.e)), 10))
