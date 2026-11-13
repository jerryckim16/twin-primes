# Sanity check of the local complete-sum facts behind Eq. (30):
#  (k=0) prime p | r only in d1:  sum_{n!=0} e_p(c/n) = p-1 if p|c else -1  -> product <= gcd(c,r)
#  (k!=0) |sum_{n mod p, n,n+l units} e_p(c1/n + c2/(n+l) + k n)| <= 4 sqrt(p) unless p|k and c1=c2=0 (or l=0,c1+c2=0)
import cmath, math
from sympy import primerange
def e(x,p): return cmath.exp(2j*math.pi*(x%p)/p)
bad=0; worst=0
for p in primerange(3,42):
    inv=[0]+[pow(n,-1,p) for n in range(1,p)]
    for c in range(p):
        s=sum(e(c*inv[n],p) for n in range(1,p))
        exp_=(p-1) if c==0 else -1
        assert abs(s-exp_)<1e-6
    for l in range(p):
      for c1 in range(p):
        for c2 in range(p):
          for k in range(p):
            s=0
            for n in range(p):
                if n==0 or (n+l)%p==0: continue
                s+=e(c1*inv[n]+c2*inv[(n+l)%p]+k*n,p)
            a=abs(s)
            degenerate = (k==0) and ((l!=0 and c1==0 and c2==0) or (l==0 and (c1+c2)%p==0))
            if not degenerate:
                worst=max(worst,a/math.sqrt(p))
                if a>4*math.sqrt(p)+1e-6: bad+=1
print('non-degenerate violations of 4sqrt(p) (Bombieri-Weil, three simple poles incl. infinity):',bad,' max |S|/sqrt(p)=',round(worst,3))
