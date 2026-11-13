import cmath
# composite common factor g; s=1, n=0; r_i = g t_i. Compare a1=a2 vs a1 t2^3 = a2 t1^3 (mod g).
import math, sys
def kl3_table(q):
    # normalized Kl3(x;q) = q^{-1} sum_{x1 x2 x3 = x} e_q(x1+x2+x3), for units x
    units=[u for u in range(q) if math.gcd(u,q)==1]
    inv={u:pow(u,-1,q) for u in units}
    E=[cmath.exp(2j*math.pi*k/q) for k in range(q)]
    T={}
    for x in units:
        tot=0
        for x1 in units:
            for x2 in units:
                x3=x*inv[x1]*inv[x2]%q
                tot+=E[(x1+x2+x3)%q]
        T[x]=tot/q
    return T
def corr(r1,r2,a1,a2):
    L=r1*r2//math.gcd(r1,r2); K1=kl3_table(r1); K2=kl3_table(r2)
    return sum(K1[a1*h%r1]*K2[a2*h%r2].conjugate() for h in range(L) if math.gcd(h,L)==1)
g=int(sys.argv[1]); t1,t2=2,3; r1,r2=g*t1,g*t2; L=g*t1*t2
a2=next(c for c in range(1,L) if math.gcd(c,L)==1 and (t2**3-c*t1**3)%g==0)
print("g",g,"case A |S|=",round(abs(corr(r1,r2,1,1)),3),"case B (a2=%d) |S|="%a2,round(abs(corr(r1,r2,1,a2)),3),"g/(t1 t2)=",round(g/6,3),"sqrt[r1,r2]=",round(math.sqrt(L),3))
