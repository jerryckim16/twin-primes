import sys; sys.path.insert(0,'/home/user/twin-primes/code/explore')
import numpy as np
from psi_scratch_wform import I_w, k, tau, E2
rng=np.random.default_rng(3)
worst=1e9
for t in range(3000):
    a=rng.uniform(1.03,1.05)
    m=rng.integers(0,k-1)
    others=np.zeros(k-2)
    typ=rng.integers(4)
    if typ==0: others[:m]=rng.random(m)*0.1
    elif typ==1: others[:m]=E2
    elif typ==2: others[:m]=rng.choice([0,E2,rng.random()*E2],m)
    else: others[:m]=rng.random(m)*0.3
    if others.sum()>tau-1e-3: others*= (tau-rng.random()*0.3)/others.sum()
    ymax=min(E2,tau-others.sum())
    ys=np.linspace(0,ymax,201)
    v=np.array([I_w(a,np.append(others,y)) for y in ys])
    # check max at endpoint
    gap=v.max()-max(v[0],v[-1])
    second=np.diff(v,2)
    if second.min()<worst: worst=second.min(); wc=(a,typ,m,ymax)
    if gap>1e-12: print("interior max", a,typ,m,gap, ys[v.argmax()], ymax)
print("min second diff",worst,wc)
