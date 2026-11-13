# Randomized stress test (log-space) of the Lemma 4.7 construction. Not a proof; the proof is in report.md.
import random
from fractions import Fraction as F
delta=91/5000; B=1899/10000; L=491/2000; U=521/2000
s3=143/375; eta=39/1000; lo=343/1000; hi=1899/5000
random.seed(1)
bad=0; trials=200000
for _ in range(trials):
    sigma=random.random()*0.05
    zeta=random.random()*1e-3
    # rough groups: each total <= (1-sigma)B, parts >= delta (only the total matters)
    g1=random.choice([0, random.uniform(delta,(1-sigma)*B)])
    g2=random.choice([0, random.uniform(delta,(1-sigma)*B)])
    # smooth parts e (with g1 <= (1-s)L) and e' (with g2 <= (1-s)U)
    emax=max(0,(1-sigma)*L-g1); epmax=max(0,(1-sigma)*U-g2)
    e_=random.uniform(0,emax); ep=random.uniform(0,epmax)
    q=g1+g2+e_+ep
    if q<0.5-zeta: continue
    # split smooth part into primes each <= delta (random sizes)
    rest=e_+ep; primes=[]
    while rest>1e-12:
        x=min(rest,random.uniform(1e-6,delta)); primes.append(x); rest-=x
    random.shuffle(primes)
    G=g1+g2
    if G>=lo: s0=G
    else:
        s0=G
        for x in primes:
            if s0>=lo: break
            s0+=x
    ok = lo<=s0<=hi and s3-eta<s0<s3
    if not ok: bad+=1
print("trials with q>=1/2-zeta checked; failures:",bad)
