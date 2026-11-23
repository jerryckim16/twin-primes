#!/usr/bin/env python3
"""Session 47 (audit check for notes/parity-attempts/2026-11-23-granville-shao-level-half.md): Green arXiv:1604.04481v4 p. 2
example. Mean of (-1)^{n+1} mu^2(n) up to N = 4e6 and its class means mod 2018, 20014 for a = 1, 2. Pure Python, ~1 min.
Run: python3 -I code/parity/green_example_check.py"""
N=4*10**6
mu2=bytearray([1])*(N+1); mu2[0]=0
p=2
while p*p<=N:
    for k in range(p*p,N+1,p*p): mu2[k]=0
    p+=1
f=[0]+[(1 if n%2 else -1) if mu2[n] else 0 for n in range(1,N+1)]
import math
print("mean",sum(f)/N,2/math.pi**2)
for q in [2*1009,2*10007]:
    for a in [1,2]:
        s=f[a::q]; print(q,a,sum(s)/len(s))
