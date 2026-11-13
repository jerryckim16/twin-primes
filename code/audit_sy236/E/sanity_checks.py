# Finite sanity checks of identities/inequalities in Sec 4.5-4.7 (not proofs of asymptotics).
import math, itertools
from fractions import Fraction as F
from sympy import factorint, isprime, primerange, mobius, divisors
import numpy as np
N=3000
mu=[0]+[int(mobius(n)) for n in range(1,N+1)]
Lam=[0.0]*(N+1)
for n in range(2,N+1):
    f=factorint(n)
    if len(f)==1: Lam[n]=math.log(list(f)[0])
def conv(a,b):
    c=[0.0]*(N+1)
    for d in range(1,N+1):
        if a[d]==0: continue
        for m in range(1,N//d+1): c[d*m]+=a[d]*b[m]
    return c
# 1. Heath-Brown identity (53) with general K and Z with Z^K >= nmax
def hb(K,Z,nmax):
    muZ=[0]+[mu[n] if n<=Z else 0 for n in range(1,N+1)]
    one=[0]+[1]*N; lg=[0.0]+[math.log(n) for n in range(1,N+1)]
    tot=[0.0]*(N+1)
    for j in range(1,K+1):
        t=lg[:]
        for _ in range(j): t=conv(t,muZ)
        for _ in range(j-1): t=conv(t,one)
        c=(-1)**(j-1)*math.comb(K,j)
        tot=[x+c*y for x,y in zip(tot,t)]
    return max(abs(tot[n]-Lam[n]) for n in range(1,nmax+1))
for K,Z in [(2,54),(3,14),(4,7)]:
    nmax=min(N,Z**K)
    print(f"HB identity K={K},Z={Z}, n<= {nmax}: max err {hb(K,Z,nmax):.2e}")
# 2. sqrt-root count for squarefree q
bad=0
for q in range(2,400):
    if any(e>1 for e in factorint(q).values()): continue
    w=len(factorint(q))
    for a in range(1,q):
        if math.gcd(a,q)!=1: continue
        s=sum(1 for u in range(q) if (u*u-a)%q==0)
        if s>2**w: bad+=1
print("u^2=a mod q root count > 2^omega(q) cases (q<400 squarefree):",bad)
# 3. partial-summation identity of Prop 4.17 (exact for step functions)
def Delta_theta(X,t,a,q):
    s1=sum(math.log(n) for n in range(math.floor(X)+1,math.floor(t)+1) if n%q==a%q and isprime(n))
    s2=sum(math.log(n) for n in range(math.floor(X)+1,math.floor(t)+1) if math.gcd(n,q)==1 and isprime(n))
    phi=sum(1 for k in range(1,q+1) if math.gcd(k,q)==1)
    return s1-s2/phi
def Delta_ind(X,Y,a,q):
    s1=sum(1 for n in range(math.floor(X)+1,math.floor(Y)+1) if n%q==a%q and isprime(n))
    s2=sum(1 for n in range(math.floor(X)+1,math.floor(Y)+1) if math.gcd(n,q)==1 and isprime(n))
    phi=sum(1 for k in range(1,q+1) if math.gcd(k,q)==1)
    return s1-s2/phi
for (X,Y,a,q) in [(1000,1800,3,7),(1000,2000,5,30),(1500,2999,1,77)]:
    lhs=Delta_ind(X,Y,a,q)
    # E(t) is constant on [n,n+1); int_n^{n+1} dt/(t log^2 t) = 1/log n - 1/log(n+1)
    integ=0.0
    for n in range(X,Y):
        integ+=Delta_theta(X,n,a,q)*(1/math.log(n)-1/math.log(n+1))
    rhs=Delta_theta(X,Y,a,q)/math.log(Y)+integ
    print(f"partial summation X={X},Y={Y},q={q}: lhs={lhs:.10f} rhs={rhs:.10f}")
# 4. Lemma 4.12 sanity: sum_{n in J} tau_k(n) vs H(logX)^{k-1}+X^{1-1/k}(logX)^{k-2} (constant ratio only)
def tauk(n,k):
    r=1
    for p,e in factorint(n).items(): r*=math.comb(e+k-1,k-1)
    return r
for k in [2,3,4]:
    for X,H in [(10**6,10),(10**6,1000),(10**7,100)]:
        s=sum(tauk(n,k) for n in range(X,X+H))
        bnd=H*math.log(X)**(k-1)+X**(1-1/k)*math.log(X)**(k-2)
        print(f"Lemma4.12 k={k} X={X} H={H}: sum={s}, ratio to bound={s/bnd:.3f}")
# 5. (62) |1_(0,u]-kappa_h*1_(0,u]| <= beta(u/h)+beta((u-uY)/h) with concrete bumps
def bump(x):
    return np.where(np.abs(x)<1, np.exp(-1/np.maximum(1-x**2,1e-300)),0.0)
xs=np.linspace(-1,1,20001); Zk=np.trapezoid(bump(xs),xs)
def beta(x):  # smooth, =1 on [-1,1], supported in [-2,2]
    x=np.abs(x)
    g=lambda s: np.where(s>0,np.exp(-1/np.maximum(s,1e-300)),0.0)
    t=(2-x); return np.where(x<=1,1.0,g(t)/(g(t)+g(1-t)))
h=0.01
for uY in [0.0,0.005,0.02,0.3,math.log(2)]:
    u=np.linspace(-0.05,uY+0.05,40001)
    # chi(u)=int kappa_h(u-v)1_(0,uY](v)dv = int_{(u-uY)/h}^{u/h} kappa(s)ds
    grid=np.linspace(-1,1,4001); cdf=np.concatenate([[0],np.cumsum((bump(grid[1:])+bump(grid[:-1]))/2*np.diff(grid))])/Zk
    K=lambda s: np.interp(s,grid,cdf,left=0,right=1)
    chi=K(u/h)-K((u-uY)/h)
    ind=((u>0)&(u<=uY)).astype(float)
    viol=np.max(np.abs(ind-chi)-(beta(u/h)+beta((u-uY)/h)))
    print(f"(62) uY={uY}: max(|1-chi|-beta_Y) = {viol:.3e} (<=0 means holds)")
