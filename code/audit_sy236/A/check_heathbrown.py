#!/usr/bin/env python3
"""Exact check of the Heath-Brown identity (53) in the form
   Lambda(n) = sum_{j=1}^K (-1)^{j-1} C(K,j) (mu_Z^{*j} * 1^{*(j-1)} * log)(n),  n <= Z^K,
using the multiplicative representation log -> exact via Lambda: we test the equivalent
identity with log replaced by L = 1*Lambda, comparing as sums of logs of primes (exact
vectors of prime-exponents).  Small cases: (K,Z)=(3,5) n<=125, (10,2) n<=1024, (4,4) n<=256."""
from math import comb
from sympy import factorint, primerange
N=1100
mu=[0]*(N+1); mu[1]=1
for n in range(2,N+1):
    f=factorint(n); mu[n]=0 if any(e>1 for e in f.values()) else (-1)**len(f)
primes=list(primerange(2,N+1)); P=len(primes); idx={p:i for i,p in enumerate(primes)}
def logvec(n):
    v=[0]*P
    for p,e in factorint(n).items(): v[idx[p]]+=e
    return v
def conv(f,g,M):
    h=[0]*(M+1)
    for d in range(1,M+1):
        if f[d]==0: continue
        for m in range(1,M//d+1): h[d*m]+=f[d]*g[m]
    return h
def check(K,Z):
    M=Z**K
    muZ=[mu[n] if n<=Z else 0 for n in range(M+1)]; one=[0]+[1]*M
    total=[[0]*P for _ in range(M+1)]
    for j in range(1,K+1):
        h=[0]+[1 if n==1 else 0 for n in range(1,M+1)]
        for _ in range(j): h=conv(h,muZ,M)
        for _ in range(j-1): h=conv(h,one,M)
        coef=(-1)**(j-1)*comb(K,j)
        # convolve with log: (h*log)(n)=sum_{d|n} h(d) log(n/d)
        for d in range(1,M+1):
            if h[d]==0: continue
            for m in range(2,M//d+1):
                lv=logvec(m); c=coef*h[d]
                tv=total[d*m]
                for i,e in enumerate(lv):
                    if e: tv[i]+=c*e
    bad=[]
    for n in range(1,M+1):
        f=factorint(n); exp=[0]*P
        if len(f)==1: exp[idx[next(iter(f))]]=1
        if total[n]!=exp: bad.append(n)
    print(f"K={K}, Z={Z}: identity exact for all n<=Z^K={M}: {not bad}" + ("" if not bad else f" first bad {bad[:5]}"))
    # beyond Z^K it should fail somewhere (sanity that the test has teeth)
for K,Z in [(3,5),(4,4),(10,2)]: check(K,Z)
