# Log-space stress test of the greedy construction in Lemma 4.5 (sizes are log_X p; D0-primes ~ 0 ignored).
# Exact rationals; random D182-type moduli with d >= X^{1/2-zeta}; gamma in [gamma*, 11/25] incl. endpoints.
from fractions import Fraction as F
import random
delta=F(91,5000); B=F(1899,10000); L=F(491,2000); U=F(521,2000)
eta2=F(1821,100000); tau0=F(1,500000); omega=F(3,1000)
gs=F(7997,20000); gm=F(11,25); zeta=tau0/2000
random.seed(1)
def rnd(lo,hi,den=10**7): return lo+(hi-lo)*F(random.randint(0,den),den)
def make_mod(sigma):
    # rough groups
    def rough(cap):
        fs=[];tot=F(0)
        while random.random()<0.7:
            x=rnd(delta,B)
            if tot+x>(1-sigma)*cap: break
            fs.append(x);tot+=x
        return fs,tot
    f,sf=rough(B); fp,sfp=rough(B)
    # smooth primes up to the e, e' budgets (25)
    def smooth(budget):
        ps=[];tot=F(0)
        mode=random.choice(['max','rand','tiny'])
        while True:
            x= delta if mode=='max' else (rnd(F(1,10**4),delta) if mode=='rand' else rnd(F(1,10**5),F(1,1000)))
            if tot+x>budget: break
            ps.append(x);tot+=x
        return ps
    e=smooth((1-sigma)*L-sf); ep=smooth((1-sigma)*U-sfp)
    return sf+sfp, e+ep
fails=0;tested=0
for trial in range(20000):
    sigma=random.choice([F(1,10**6),F(1,1000),F(1,100)])
    G,sm=make_mod(sigma)
    if G+sum(sm,F(0))<F(1,2)-zeta: continue
    tested+=1
    random.shuffle(sm)
    g=random.choice([gs,gm,rnd(gs,gm)])
    tr=g-eta2+2*tau0; r=G; i=0
    assert r<tr, ("start above target",G)
    while r<tr: r+=sm[i]; i+=1
    q=sm[i:]
    ag=F(1,2)-g-2*omega; tu=ag-eta2+2*tau0; u=F(0); j=0
    random.shuffle(q)
    while u<tu:
        if j>=len(q): fails+=1; print("ran out",g); break
        u+=q[j]; j+=1
    if not (tr<=r<g-3*tau0 and tu<=u<ag-3*tau0): fails+=1; print("window fail",g,r,u)
print("tested",tested,"fails",fails)
