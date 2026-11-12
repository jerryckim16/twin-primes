#!/usr/bin/env python3
"""Certified lower bounds for Maynard's sieve constant M_k.

M_k = sup_F  sum_m J_k^(m)(F) / I_k(F),   F supported on the simplex
R_k = {t in [0,1]^k : t_1+...+t_k <= 1}.

Ansatz (Maynard 2015, Sec. 8):  F = sum_{a+2b<=D} c_{a,b} (1-P1)^a P2^b,
P1 = sum t_i, P2 = sum t_i^2.  Everything reduces to the Dirichlet integral

  S_k(A,B) = int_{R_k} (1-P1)^A P2^B dt = A!/(k+A+2B)! * G_k(B),
  G_k(B)   = B! [x^B] ( sum_b (2b)!/b! x^b )^k .

The script (1) builds the exact rational Gram matrices, (2) finds an
approximate top eigenvector in high precision floating point, (3) rounds it
to rationals and evaluates the Rayleigh quotient EXACTLY.  Step (3) is a
rigorous lower bound for M_k whatever happened in step (2).
"""
import sys, json, time
from fractions import Fraction as Fr
from math import factorial, comb
import mpmath as mp

def gk_table(k, Bmax):
    """G_k(B) for B=0..Bmax (exact integers)."""
    g = [factorial(2*b)//factorial(b) for b in range(Bmax+1)]
    def mul(p, q):
        r = [0]*(Bmax+1)
        for i, pi in enumerate(p):
            if pi:
                for j in range(Bmax+1-i):
                    r[i+j] += pi*q[j]
        return r
    res = [1]+[0]*Bmax; base = g; e = k
    while e:
        if e & 1: res = mul(res, base)
        base = mul(base, base); e >>= 1
    return [factorial(B)*res[B] for B in range(Bmax+1)]

class Simplex:
    def __init__(self, k, Bmax):
        self.k = k; self.G = gk_table(k, Bmax)
    def S(self, A, B):
        return Fr(factorial(A)*self.G[B], factorial(self.k + A + 2*B))

def gram(k, D):
    basis = [(a, b) for b in range(D//2+1) for a in range(D-2*b+1)]
    Bmax = 2*(D//2)
    Sk, Sk1 = Simplex(k, Bmax), Simplex(k-1, Bmax)
    # inner integral of (1-P1)^a P2^b over one variable:
    #   sum_j C(b,j) (2j)! a!/(a+2j+1)! (1-P1')^(a+2j+1) P2'^(b-j)
    inner = {}
    for (a, b) in basis:
        inner[(a, b)] = [(Fr(comb(b, j)*factorial(2*j)*factorial(a), factorial(a+2*j+1)), a+2*j+1, b-j)
                         for j in range(b+1)]
    n = len(basis)
    I = [[None]*n for _ in range(n)]; J = [[None]*n for _ in range(n)]
    cache = {}
    def S1(A, B):
        key = (A, B)
        if key not in cache: cache[key] = Sk1.S(A, B)
        return cache[key]
    for x in range(n):
        a, b = basis[x]
        for y in range(x, n):
            a2, b2 = basis[y]
            I[x][y] = I[y][x] = Sk.S(a+a2, b+b2)
            s = Fr(0)
            for (c1, A1, B1) in inner[(a, b)]:
                for (c2, A2, B2) in inner[(a2, b2)]:
                    s += c1*c2*S1(A1+A2, B1+B2)
            J[x][y] = J[y][x] = s
    return basis, I, J

def top_vector(I, J, k, dps=120):
    mp.mp.dps = dps
    n = len(I)
    # rescale basis so the Gram matrix has unit diagonal (conditioning)
    sc = [mp.sqrt(mp.mpf(I[i][i].numerator)/I[i][i].denominator) for i in range(n)]
    f = lambda q: mp.mpf(q.numerator)/q.denominator
    A = mp.matrix(n, n); B = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            A[i, j] = f(I[i][j])/(sc[i]*sc[j]); B[i, j] = k*f(J[i][j])/(sc[i]*sc[j])
    L = mp.cholesky(A)
    Li = mp.inverse(L)
    C = Li*B*Li.T
    C = (C + C.T)/2
    E, Q = mp.eigsy(C)
    idx = max(range(n), key=lambda i: E[i])
    w = Li.T*Q[:, idx]
    v = [w[i]/sc[i] for i in range(n)]
    return E[idx], v

def certify(I, J, k, v, digits=40):
    """Round v to rationals and return the exact Rayleigh quotient k*vJv / vIv."""
    vmax = max(abs(x) for x in v)
    q = [Fr(int(mp.nint(x/vmax*mp.mpf(10)**digits)), 10**digits) for x in v]
    n = len(q)
    num = sum(q[i]*J[i][j]*q[j] for i in range(n) for j in range(n))*k
    den = sum(q[i]*I[i][j]*q[j] for i in range(n) for j in range(n))
    assert den > 0
    return num/den, q

def run(k, D, dps=120, digits=40):
    t = time.time()
    basis, I, J = gram(k, D)
    lam, v = top_vector(I, J, k, dps)
    exact, q = certify(I, J, k, v, digits)
    return dict(k=k, D=D, n=len(basis), float_eig=mp.nstr(lam, 12),
                certified=mp.nstr(mp.mpf(exact.numerator)/exact.denominator, 12),
                gt4=bool(exact > 4), secs=round(time.time()-t, 1)), exact, basis, q

if __name__ == "__main__":
    k = int(sys.argv[1]); D = int(sys.argv[2])
    info, exact, basis, q = run(k, D)
    print(json.dumps(info))
