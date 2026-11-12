#!/usr/bin/env python3
"""Sampled Collatz-Wielandt ratio sum_{m active} (int F dt_m)/F for the Galerkin extremal F of
mk_general.py (Session 4, floating point, random samples only: NOT a bound).
usage: cw_sample.py k D eps   (eps as p/q or 0)"""
import sys, numpy as np; sys.path.insert(0,'code')
import mk_general as mg
from flint import fmpq
from math import log
k=int(sys.argv[1]); D=int(sys.argv[2]); e=fmpq(*map(int,sys.argv[3].split('/'))) if '/' in sys.argv[3] else fmpq(0)
ef=float(e.p)/float(e.q); L,tau=1+ef,1-ef
info,exact,basis,q=mg.run(k,D,eps=e,prec=300); print(info['certified'])
c=np.array([float(q[i,0].p)/float(q[i,0].q) for i in range(q.nrows())])
def F(T):  # T: (n,k)
    P1=T.sum(1); out=np.zeros(len(T))
    for (a,b),ci in zip(basis,c):
        v=(L-P1)**a
        for j,m in enumerate(b):
            if m: v=v*(T**(j+2)).sum(1)**m
        out+=ci*v
    return out
xg,wg=np.polynomial.legendre.leggauss(40)
rng=np.random.default_rng(0)
# sample points in L*R_k (uniform, plus near-boundary)
pts=rng.dirichlet(np.ones(k+1),size=20000)[:,:k]*L
Fv=F(pts)
sgn=np.sign(Fv.mean()); Fv*=sgn
print("min F/max F", Fv.min()/Fv.max())
num=np.zeros(len(pts))
for m in range(k):
    rest=pts.sum(1)-pts[:,m]
    act=rest<=tau
    top=L-rest
    for x,w in zip(xg,wg):
        u=(x+1)/2*top; Q=pts.copy(); Q[:,m]=u
        num+=act*sgn*F(Q)*w*top/2
ratio=num/Fv
ok=Fv>0
print("positive fraction",ok.mean(), "ratio: mean %.4f  max %.4f  95pct %.4f"%(ratio[ok].mean(),ratio[ok].max(),np.percentile(ratio[ok],95)))
