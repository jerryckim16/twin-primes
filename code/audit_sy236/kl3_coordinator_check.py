import cmath
p=31
e=lambda x: cmath.exp(2j*cmath.pi*(x%p)/p)
inv=lambda x: pow(x,-1,p)
# normalised Kl3(a;p) = p^{-1} sum_{xyz=a} e(x+y+z)
K={}
for a in range(1,p):
    s=0
    for x in range(1,p):
        for y in range(1,p):
            z=a*inv(x*y)%p; s+=e(x+y+z)
    K[a]=s/p
def corr(c1,c2):  # sum over l in (Z/p)^* of K(c1 l) conj K(c2 l)
    return abs(sum(K[c1*l%p]*K[c2*l%p].conjugate() for l in range(1,p)))
# argument for i: c * m_i^{-1} * (t_i)^{-3}  (common factors dropped)
t1,t2=2,3
big=[];small=[]
for m1 in range(1,p):
  for m2 in range(1,p):
    v=corr(inv(m1)*inv(pow(t1,3,p))%p, inv(m2)*inv(pow(t2,3,p))%p)
    if m1==m2: small.append(v)
    if (m1*pow(t1,3,p)-m2*pow(t2,3,p))%p==0: big.append(v)
print("m1==m2: max", max(small)); print("m1 t1^3 == m2 t2^3: min", min(big))
