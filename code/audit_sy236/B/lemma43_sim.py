# Toy model of Lemma 4.3 (log_X scale; D0-small primes modelled as size 0, i.e. the X^{o(1)} term).
# A modulus = list of prime sizes in (0,1]; rough groups = arbitrary integers >= X^delta whose prime
# factors may be of any size; smooth part e e' = primes of size <= delta.  Greedy as in the paper.
import random
from fractions import Fraction as F
delta=F(91,5000); B=F(1899,10000); L=F(491,2000); U=F(521,2000)
eta2=F(1821,100000); tau0=F(1,500000)
random.seed(1)
def rnd(lo,hi,den=10**6): return lo+(hi-lo)*F(random.randint(0,den),den)
fails=0; trials=0
for t in range(20000):
    sigma=rnd(F(0),F(1,100))
    gamma=random.choice([F(11,25),F(1,2),rnd(F(11,25),F(1,2))])
    zeta=tau0/200
    # rough groups: total sizes <= (1-sigma)B each; content irrelevant (all go into r)
    m=random.choice([0,1,2,10]); mp=random.choice([0,1,3])
    Rg=rnd(0,(1-sigma)*B) if m else F(0); Rgp=rnd(0,(1-sigma)*B) if mp else F(0)
    if m: Rg=max(Rg,min(m*delta,(1-sigma)*B))
    # smooth parts, sizes <= delta, subject to (25); try to make d >= 1/2 - zeta
    capE=(1-sigma)*L-Rg; capEp=(1-sigma)*U-Rgp
    def fill(cap):
        out=[];s=F(0)
        while True:
            p=random.choice([delta,rnd(F(0),delta),rnd(delta/2,delta)])
            if p==0 or s+p>cap: break
            out.append(p); s+=p
        return out
    E=fill(capE); Ep=fill(capEp)
    smooth=E+Ep; d=Rg+Rgp+sum(smooth)
    if d<F(1,2)-zeta: continue
    trials+=1
    target=gamma-eta2+2*tau0
    r=Rg+Rgp  # + o(1) small primes
    assert r<target, (r,target)
    random.shuffle(smooth); used=0
    while r<target:
        r+=smooth[used]; used+=1
    if not (target<=r<gamma-3*tau0): fails+=1
print('trials with d>=X^{1/2-zeta}:',trials,' failures:',fails)
