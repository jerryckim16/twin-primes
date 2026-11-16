#!/usr/bin/env python3
"""Program 1 (exact, own polynomial algebra): Maynard ratios M_k(F) = k J(F)/I(F)
for symmetric polynomial F(t) on the simplex t_1+...+t_k <= 1.

Used for the Pintz-type dichotomy with Maynard weights (parity paper,
subsection subsec:pintz): the dichotomy at level theta needs theta*M_k(F) > 1.

  I(F) = int_{simplex_k} F^2,
  J(F) = int_{simplex_{k-1}} ( int_0^{1-t_1-...-t_{k-1}} F dt_k )^2.

Exact integration by the Dirichlet formula
  int_{simplex_n} t^a (1-|t|)^b dt = prod(a_i!) b! / (n+|a|+b)!.

Usage:
  python3 code/parity/pintz_maynard.py maynard5     # Maynard's (8.16), k = 5
  python3 code/parity/pintz_maynard.py opt K DEG    # optimise over (1-P1)^b P2^c, rationalise, exact ratio
Output: exact rational ratio and its decimal value; the rational vectors are
written to code/parity/pintz_maynard_vectors.json by 'opt'.
"""
import sys, json, itertools
from fractions import Fraction as Fr
from math import factorial

# polynomials: dict {exponent tuple (len n) : Fraction}

def padd(p, q, c=1):
    r = dict(p)
    for e, v in q.items():
        r[e] = r.get(e, 0) + c * v
        if r[e] == 0:
            del r[e]
    return r

def pmul(p, q):
    r = {}
    for e1, v1 in p.items():
        for e2, v2 in q.items():
            e = tuple(a + b for a, b in zip(e1, e2))
            r[e] = r.get(e, 0) + v1 * v2
    return {e: v for e, v in r.items() if v != 0}

def ppow(p, m, n):
    r = {tuple([0] * n): Fr(1)}
    for _ in range(m):
        r = pmul(r, p)
    return r

def var(i, n):
    e = [0] * n; e[i] = 1
    return {tuple(e): Fr(1)}

def const(c, n):
    return {tuple([0] * n): Fr(c)}

def P1(n):
    r = {}
    for i in range(n):
        r = padd(r, var(i, n))
    return r

def P2(n):
    r = {}
    for i in range(n):
        r = padd(r, pmul(var(i, n), var(i, n)))
    return r

def dirichlet(a, b, n):
    """int over simplex_n of t^a (1-|t|)^b."""
    num = factorial(b)
    for x in a:
        num *= factorial(x)
    return Fr(num, factorial(n + sum(a) + b))

def I_of(F, k):
    G = pmul(F, F)
    return sum(v * dirichlet(e, 0, k) for e, v in G.items())

def J_of(F, k):
    # write F = sum_j c_j(t') t_k^j ; inner integral = sum_j c_j (1-s)^{j+1}/(j+1)
    # represent results as dict {(a', b): coeff} with (1-s)^b kept symbolic
    inner = {}
    for e, v in F.items():
        a, j = e[:-1], e[-1]
        key = (a, j + 1)
        inner[key] = inner.get(key, 0) + v / (j + 1)
    sq = {}
    items = list(inner.items())
    for (a1, b1), v1 in items:
        for (a2, b2), v2 in items:
            key = (tuple(x + y for x, y in zip(a1, a2)), b1 + b2)
            sq[key] = sq.get(key, 0) + v1 * v2
    return sum(v * dirichlet(a, b, k - 1) for (a, b), v in sq.items())

def ratio(F, k):
    I = I_of(F, k); J = J_of(F, k)
    return Fr(k) * J / I, I, J

def maynard5():
    k = 5
    one_m_P1 = padd(const(1, k), P1(k), -1)
    p2 = P2(k)
    F = pmul(one_m_P1, p2)
    F = padd(F, ppow(one_m_P1, 2, k), Fr(7, 10))
    F = padd(F, p2, Fr(1, 14))
    F = padd(F, one_m_P1, Fr(-3, 14))
    return F, k

def basis(k, deg):
    one_m_P1 = padd(const(1, k), P1(k), -1)
    p2 = P2(k)
    B, labels = [], []
    for b in range(deg + 1):
        for c in range(deg + 1):
            if b + 2 * c <= deg:
                B.append(pmul(ppow(one_m_P1, b, k), ppow(p2, c, k)))
                labels.append((b, c))
    return B, labels

def opt(k, deg):
    import numpy as np, scipy.linalg as sl
    B, labels = basis(k, deg)
    n = len(B)
    A1 = [[I_of_cross(B[i], B[j], k) for j in range(n)] for i in range(n)]
    A2 = [[J_cross(B[i], B[j], k) for j in range(n)] for i in range(n)]
    a1 = np.array([[float(x) for x in r] for r in A1]); a2 = np.array([[float(x) for x in r] for r in A2])
    w, V = sl.eigh(k * a2, a1)
    v = V[:, -1]; v = v / v[np.argmax(abs(v))]
    q = [Fr(x).limit_denominator(10 ** 6) for x in v]
    F = {}
    for c, P in zip(q, B):
        F = padd(F, P, c)
    M, I, J = ratio(F, k)
    return M, q, labels, float(w[-1])

def I_of_cross(P, Q, k):
    G = pmul(P, Q)
    return sum(v * dirichlet(e, 0, k) for e, v in G.items())

def J_cross(P, Q, k):
    def inner(F):
        d = {}
        for e, v in F.items():
            key = (e[:-1], e[-1] + 1)
            d[key] = d.get(key, 0) + v / (e[-1] + 1)
        return d
    ip, iq = inner(P), inner(Q)
    s = Fr(0)
    for (a1, b1), v1 in ip.items():
        for (a2, b2), v2 in iq.items():
            s += v1 * v2 * dirichlet(tuple(x + y for x, y in zip(a1, a2)), b1 + b2, k - 1)
    return s

if __name__ == "__main__":
    if sys.argv[1] == "maynard5":
        F, k = maynard5()
        M, I, J = ratio(F, k)
        print("k = 5, Maynard (8.16): I =", I, " J =", J)
        print("M =", M, "=", float(M), " > 2:", M > 2, " == 1417255/708216:", M == Fr(1417255, 708216))
    elif sys.argv[1] == "opt":
        k, deg = int(sys.argv[2]), int(sys.argv[3])
        M, q, labels, fl = opt(k, deg)
        print(f"k = {k}, deg {deg}: float eigenvalue {fl:.10f}; exact ratio of rationalised vector {M} = {float(M):.10f}; 1/M = {float(1/M):.6f}")
        try:
            data = json.load(open("code/parity/pintz_maynard_vectors.json"))
        except Exception:
            data = {}
        data[f"k{k}_deg{deg}"] = {"basis (b,c) for (1-P1)^b P2^c": labels,
                                  "coeffs": [str(x) for x in q], "ratio": str(M), "ratio_float": float(M)}
        json.dump(data, open("code/parity/pintz_maynard_vectors.json", "w"), indent=1)
