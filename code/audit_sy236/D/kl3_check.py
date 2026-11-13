# Numerical checks of the hyper-Kloosterman manipulations in Section 4.4
import cmath, math
from functools import lru_cache
def inv(x,m): return pow(x,-1,m)
def e(x,m): return cmath.exp(2j*math.pi*(x%m)/m)
@lru_cache(None)
def Kl3(t,d):
    t%=d
    if d==1: return 1.0
    units=[x for x in range(d) if math.gcd(x,d)==1]
    tot=0
    for x1 in units:
        for x2 in units:
            x3=(t*inv(x1*x2%d,d))%d
            tot+=e(x1+x2+x3,d)
    return tot/d
# 1) twisted multiplicativity Kl3(t;rs)=Kl3(t sbar^3;r)Kl3(t rbar^3;s)
for (r,s,t) in [(5,7,3),(3,11,2),(7,13,10),(6,35,1)]:
    lhs=Kl3(t,r*s); rhs=Kl3(t*inv(s,r)**3,r)*Kl3(t*inv(r,s)**3,s)
    print("twisted mult r=%d s=%d t=%d: |diff|=%.2e"%(r,s,t,abs(lhs-rhs)))
# 2) CRT separation of F(h;t;q) and the mod-b factor bound b1f b2f b3f / b^2
def Fsum(h,t,q):
    units=[x for x in range(q) if math.gcd(x,q)==1]; tot=0
    for x1 in units:
        for x2 in units:
            x3=(t*inv(x1*x2%q,q))%q
            tot+=e(h[0]*x1+h[1]*x2+h[2]*x3,q)
    return tot/q
import itertools
q=3*5*7
worst=0
for h in [(3,5,1),(15,1,2),(3,3,7),(21,5,2),(35,3,1),(3*5,5*7,3*7),(105,1,1)]:
    # b-part
    b=1
    for p in (3,5,7):
        if any(hi%p==0 for hi in h): b*=p
    d=q//b
    bflat=1
    for hi in h:
        for p in (3,5,7):
            if hi%p==0: bflat*=p
    Bstar=1
    for hi in h:
        bi=1
        for p in (3,5,7):
            while hi%(bi*p)==0: bi*=p
        Bstar*=bi
    l=1
    for hi in h:
        bi=1
        for p in (3,5,7):
            while hi%(bi*p)==0: bi*=p
        l*=hi//bi
    for t in [1,2,4,11]:
        if math.gcd(t,q)!=1: continue
        full=Fsum(h,t,q)
        kl=Kl3(t*Bstar*l*inv(b**3 % d,d) if d>1 else 0,d) if d>1 else 1.0
        modb=full/kl if abs(kl)>1e-9 else None
        if modb is not None:
            worst=max(worst,abs(modb)/(bflat/b**2))
    print("h=",h,"b=",b,"d=",d,"|mod-b factor|/(bflat/b^2) max so far %.3f"%worst)
# also independence of the mod-b factor from t
h=(3,5,1); 
vals=[Fsum(h,t,q)/Kl3(t*3*5*inv(15**3%7,7),7) for t in [1,2,4,8,11,13]]
print("mod-b factor across t:",[round(abs(v),6) for v in vals],[round(cmath.phase(v),4) for v in vals])
# 3) bad-prime condition at p | g=gcd(r1,r2): paper says gcd(g, m1-m2); derived: gcd(g, m1 t1^3 - m2 t2^3)
p=7; t1=2; t2=3; r1=p*t1; r2=p*t2; s=1; L=s*r1*r2//p
c=1
def corr(m1,m2):
    tot=0
    for l in range(L):
        if math.gcd(l,L)!=1: continue
        tot+=Kl3(c*l*inv(m1,r1*s),r1*s)*Kl3(c*l*inv(m2,r2*s),r2*s).conjugate()
    return abs(tot)
for (m1,m2) in [(1,1),(1,13),(5,5),(5,23),(11,11),(1,29)]:
    print("p=7,t1=2,t2=3: m1=%d m2=%d  m1-m2 = %d mod 7 ; m1 t1^3-m2 t2^3 = %d mod 7 ; |complete corr| = %.3f  (L=%d, sqrt L=%.2f)"%(
        m1,m2,(m1-m2)%7,(m1*t1**3-m2*t2**3)%7,corr(m1,m2),L,L**0.5))
# 4) D-condition at p | s
p=11; r1=2; r2=3; s=p; L=s*r1*r2
def corr2(m1,m2):
    tot=0
    for l in range(L):
        if math.gcd(l,L)!=1: continue
        tot+=Kl3(l*inv(m1,r1*s),r1*s)*Kl3(l*inv(m2,r2*s),r2*s).conjugate()
    return abs(tot)
for (m1,m2) in [(1,1),(27,8),(1,5)]:
    print("p|s=11: m1=%d m2=%d D=m1 r1^3-m2 r2^3 mod 11 = %d ; m1-m2 mod 11=%d ; |corr|=%.3f"%(m1,m2,(m1*8-m2*27)%11,(m1-m2)%11,corr2(m1,m2)))
# 5) local component at a prime p | g, larger p: equal-argument (bad) vs generic
import numpy as np
def kl3_table(p):
    # normalized Kl3(t;p) for all t, via convolution of additive characters
    T=np.zeros(p,dtype=complex)
    for x1 in range(1,p):
        for x2 in range(1,p):
            for t in range(1,p):
                pass
    return None
def kl3_vec(p):
    v=np.zeros(p,dtype=complex)
    for t in range(1,p):
        tot=0
        for x1 in range(1,p):
            ex1=e(x1,p)
            for x2 in range(1,p):
                x3=(t*inv(x1*x2%p,p))%p
                tot+=ex1*e(x2+x3,p)
        v[t]=tot/p
    return v
for p in [31,61]:
    K=kl3_vec(p)
    lam1=1
    diag=sum(abs(K[(lam1*x)%p])**2 for x in range(1,p))
    off=max(abs(sum(K[(lam1*x)%p]*np.conj(K[(lam2*x)%p]) for x in range(1,p))) for lam2 in range(2,p))
    print("p=%d: local corr equal args = %.2f (~p), max over unequal args = %.2f (sqrt p=%.2f)"%(p,diag,off,p**0.5))
