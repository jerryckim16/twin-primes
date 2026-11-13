# Check Polymath8a v3 Lemma 6.25 gcd factor at primes p | (r1,r2) with r1 != r2.
# s = 1, n = 0, r1 = p*t1, r2 = p*t2.  Sum over h in (Z/[r1,r2])^x of Kl3(a1 h; r1) conj Kl3(a2 h; r2).
import cmath, math, sys
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
def corr(p,t1,t2,a1,a2):
    r1,r2=p*t1,p*t2; L=r1*r2//math.gcd(r1,r2)
    K1=kl3_table(r1); K2=kl3_table(r2)
    S=0
    for h in range(L):
        if math.gcd(h,L)!=1: continue
        S+=K1[a1*h%r1]*K2[a2*h%r2].conjugate()
    return S

p=int(sys.argv[1]); t1,t2=2,3
L=p*t1*t2
print("p",p,"t1,t2",t1,t2,"[r1,r2]^{1/2}=",round(math.sqrt(L),2))
# case A: a1=a2=1 (Polymath factor (a2-a1,r1,r2)=p => claimed bound ~ sqrt(L)*sqrt(p))
SA=corr(p,t1,t2,1,1)
# case B: a1 t2^3 = a2 t1^3 mod p, a1 != a2 mod p (Polymath factor = 1 => claimed bound ~ sqrt(L))
a1=1
a2=None
for c in range(1,L):
    if math.gcd(c,L)==1 and (a1*t2**3 - c*t1**3)%p==0 and c%p!=a1%p:
        a2=c;break
SB=corr(p,t1,t2,a1,a2)
print("case A a1=a2=1: |S| =",round(abs(SA),3))
print("case B a1=1,a2=%d (a1 t2^3 = a2 t1^3 mod p): |S| ="%a2,round(abs(SB),3))
print("ratio |S_B|/|S_A| =",round(abs(SB)/abs(SA),3), " p =",p, " sqrt p=",round(math.sqrt(p),3))
