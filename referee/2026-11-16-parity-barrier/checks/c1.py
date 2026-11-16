from mpmath import mp, mpf, log
from fractions import Fraction as Fr
mp.dps=40
c=lambda k: mpf(k)**2*log(k)/(k-1)**2
for m in [2,3,4,5]:
    k=2
    while c(k)<=2*m: k+=1
    print(m,k,c(k-1),c(k))
print(c(5),c(3), 1.04*50/49*float(log(50)), 1.02*51/50*float(log(51)), 1.168*4/3*float(log(4)))
I=Fr(241672427,6144000000); J=Fr(2578076273,32768000000)
print(J/I, J/I-2, Fr(711155,3866758832))
print(float(Fr(342007,555935160)), float(Fr(4238047,46648223968)))
print(float(Fr(13523319026150757,6316738844612720)), float(Fr(39699868771187709,19218050037559040)))
print(1.5+4999/5610*0.75, 1.5+4999/5610*0.625, 2194/4999, 1.5+4999/5610*0.55, 1-1/(2*0.8901675))
# rho(e) <= 2^{omega+1}
def rho(e): return sum(1 for c in range(e) if (c*(c+2))%e==0)
from sympy import primefactors
bad=[e for e in range(1,3000) if rho(e)>2**(len(primefactors(e))+1)]
print('rho bad',bad[:10])
