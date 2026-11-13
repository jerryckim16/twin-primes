# Exact rational checks for Section 4.4 (Prop 4.6, Lemma 4.7) of Song-Yue
from fractions import Fraction as F
om=F(3,1000); eta=F(39,1000); s3=F(1,3)+4*eta/3-4*om/3
delta=F(91,5000); B=F(1899,10000); A=F(253,1000); U=A+F(3,400)
print("s3 =",s3, s3==F(143,375))
# Lemma 4.7 displayed identities
print("343/1000+delta =",F(343,1000)+delta, "==903/2500:",F(343,1000)+delta==F(903,2500), " <2B:",F(343,1000)+delta<2*B)
print("343/1000-(s3-eta) =",F(343,1000)-(s3-eta))
print("s3-2B =",s3-2*B)
print("window (s3-eta,s3) =",float(s3-eta),float(s3),"; divisor range [0.343,2B]=",float(2*B))
# q upper exponent vs Q range
print("q<=X^{(1-sigma)253/500}; 253/500 == 1/2+2om:",F(253,500)==F(1,2)+2*om)
print("1/2+eta-s3 =",F(1,2)+eta-s3)
# three error exponents with nu = logX N >= 9/10, M = X^{1-nu}, Q = X^{1/2+2om}, S=X^{s3}
def e1(nu): return (1-nu)/2+F(3,2)*(F(1,2)+2*om)+s3/2
def e2(nu): return (1-nu)+F(3,2)*(F(1,2)+2*om)+s3/4
def e3(nu): return eta/4+(1-nu)+(F(1,2)+2*om)-s3/4+nu/2
nu=F(9,10)
for k,f in enumerate([e1,e2,e3],1):
    print(f"term{k}: exponent at nu=9/10:",f(nu)," 1-exp=",1-f(nu), " decreasing in nu:", f(nu+F(1,100))<f(nu))
print("paper: 1-1/3000, 1-137/3000, 1-71/2400:", 1-e1(nu)==F(1,3000), 1-e2(nu)==F(137,3000), 1-e3(nu)==F(71,2400))
print("paper formulae:", F(2,3)+7*om/3+F(3,10)+2*eta/3==e1(nu), F(1,3)+8*om/3+F(3,5)+eta/3==e2(nu), F(2,3)+7*om/3+F(3,10)-eta/12==e3(nu))
# general admissible window for s given (sigma_PM, varpi): from the three terms
sig=F(1,10)
upper1=F(1,4)+3*sig/2-6*om; upper2=6*sig-12*om; lower3_minus_eta=F(1,2)-3*sig+8*om
print("constraints: s<",upper1,"(T1), s<",upper2,"(T2), s-eta>",lower3_minus_eta,"(T3)")
print("max admissible eta =",upper1-lower3_minus_eta," = 9sig/2-1/4-14om:",F(9,2)*sig-F(1,4)-14*om)
print("PM8a (memory) Type III: sigma > 1/18+28om/9+2delta/9 <=> delta <", (sig-F(1,18)-28*om/9)*F(9,2))
# Heath-Brown routing (Lemma 4.9 case 3)
s=F(1001,10000)
print("2s=",2*s," >= 1/5:",2*s>=F(1,5),"; 1/2-s=",F(1,2)-s," <=2/5:",F(1,2)-s<=F(2,5),"; 1/2+s=",F(1,2)+s,">=3/5:",F(1,2)+s>=F(3,5))
print("reserves:",2*s-F(1,5),F(2,5)-(F(1,2)-s),F(1,2)+s-F(3,5))
# N >= X^{9/10} from pair products, applied to routed range (actual: 3/2*0.6001)
print("routed N exponent >=",F(3,2)*(F(1,2)+s))
