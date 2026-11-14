import sys; sys.path.insert(0,'/home/user/twin-primes/code/explore')
import numpy as np
from math import log
from psi_scratch_shape import F, J, W, tau, k
def Jc(a,s,nu):
    c0=a-tau; c=c0+nu*s
    return W*nu/c if nu==1 else nu/(nu-1)*log((c+(nu-1)*W)/c)
# 1) fractional relaxation sup
for a in [1.035,1.036,1.037,1.038,1.04]:
    best=0
    for s in np.linspace(0,tau,4801):
        for nu in np.linspace(1,1+(tau-s)/W,400):
            v=F(a,s)+Jc(a,s,nu)
            if v>best: best=v;arg=(s,nu)
    print(a, "frac relax a*sup=%.6f"%(a*best), arg)
# 2) fixed s,B: nonconstant vs constant fractional
rng=np.random.default_rng(1); worst=-1
for t in range(200000):
    a=rng.uniform(1.03,1.05); p=rng.integers(2,6)
    lv=sorted(rng.choice(np.arange(1,k+1),p,replace=False))[::-1]
    lens=rng.dirichlet(np.ones(p)*0.5)*W
    _,B=J(a,0,lv,lens)
    if B>tau: continue
    s=rng.uniform(0,tau-B)
    v,_=J(a,s,lv,lens); vc=Jc(a,s,1+B/W)
    if v-vc>worst: worst=v-vc; wc=(a,s,lv,lens,B)
print("max J(shape)-J(const frac same mass):",worst,wc)
