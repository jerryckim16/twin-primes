# Symbolic re-derivation of the power bookkeeping in eqs (50)-(52)
import sympy as sp
M,Q,S,b,Bs,N,Y,g,t,z=sp.symbols('M Q S b Bstar N Y g t zeta',positive=True)  # Y = X^{eta3}
Hb=Q**3/(Bs*N)          # drop X^{3zeta/2}
L0=Q/(b*S); Z1=Y*Q/S
# off-diagonal, fixed g,t (t1~t2~t): s ~ Z0 = Q/(b g t); [r1,r2]=g t^2
Z0=Q/(b*g*t)
termA = Z0 * Z0 * Hb*(Z0*g*t**2)**sp.Rational(-1,2)   # sum_s s * Hb (s[r1,r2])^{-1/2} * gcd-sum ~ #s=Z0
termB = Z0 * Z0 * (Z0*g*t**2)**sp.Rational(1,2)
# times t (choices of t1), times m-sum (M^2+M g^{1/2}) -- keep g-power separately
A_t = sp.simplify(termA*t); B_t=sp.simplify(termB*t)
paperA=(Q/b)**2/g**2*Hb*b**sp.Rational(1,2)/(Q**sp.Rational(1,2)*t**sp.Rational(3,2))
paperB=(Q/b)**2/g**2*Q**sp.Rational(1,2)/(b**sp.Rational(1,2)*t**sp.Rational(1,2))
print("inner summand A matches paper:",sp.simplify(A_t/paperA)==1)
print("inner summand B matches paper:",sp.simplify(B_t/paperB)==1)
# sum over t>=L0/g of t^{-3/2} <= (g/L0)^{1/2};  sum over t<=Z1/g of t^{-1/2} <= (Z1/g)^{1/2}
# then sum_g (M^2+M g^{1/2}) g^{-2} * g^{1/2} or g^{-1/2}  << M^2
T2A=(Q/b)**sp.Rational(3,2)*Hb*M**2*L0**sp.Rational(-1,2)
T2B=(Q/b)**sp.Rational(5,2)*M**2*Z1**sp.Rational(1,2)
print("(51) first :",sp.simplify(T2A/(M**2*Q*S**sp.Rational(1,2)*Hb/b))==1)
print("(51) second:",sp.simplify(T2B/(Y**sp.Rational(1,2)*M**2*Q**3/(b**sp.Rational(5,2)*S**sp.Rational(1,2))))==1)
# diagonal (50)
r=sp.symbols('r',positive=True)
T20=Hb*M*(Q/b)**2*(1/L0)   # sum_{r>=L0} r^-2 << 1/L0
print("(50):",sp.simplify(T20/(Hb*M*Q*S/b))==1)
T1=Hb
T=[sp.sqrt(T1*T20), sp.sqrt(T1*T2A), sp.sqrt(T1*T2B)]
paperT=[M**sp.Rational(1,2)*Q**sp.Rational(7,2)*S**sp.Rational(1,2)/(b**sp.Rational(1,2)*Bs*N),
        M*Q**sp.Rational(7,2)*S**sp.Rational(1,4)/(b**sp.Rational(1,2)*Bs*N),
        Y**sp.Rational(1,4)*M*Q**3/(b**sp.Rational(5,4)*Bs**sp.Rational(1,2)*S**sp.Rational(1,4)*N**sp.Rational(1,2))]
for i in range(3): print("T term",i+1,"matches:",sp.simplify(T[i]/paperT[i])==1)
# weaken denominators to b*Bs^{1/2}; then (48): N/Q^2 * sum_b (b-flat/b^2) * T
E=[sp.simplify(N/Q**2*pt*(b**sp.Rational(1,2)*Bs if i<2 else b**sp.Rational(5,4)*Bs**sp.Rational(1,2))/(b*Bs**sp.Rational(1,2))) for i,pt in enumerate(paperT)]
paperE=[M**sp.Rational(1,2)*Q**sp.Rational(3,2)*S**sp.Rational(1,2), M*Q**sp.Rational(3,2)*S**sp.Rational(1,4), Y**sp.Rational(1,4)*M*Q*S**sp.Rational(-1,4)*N**sp.Rational(1,2)]
for i in range(3): print("(52) term",i+1,": N/Q^2*T*(b B*^{1/2}) ==",sp.simplify(E[i]/paperE[i]))
# Euler factor of sum b1f b2f b3f /(b^3 B*^{1/2})
p=sp.symbols('p',positive=True)
geo=sum(p*p**sp.Rational(-k,2) for k in range(1,60))
import math
for pv in [2,3,5,101]:
    exact=sum((pv if k1 else 1)*(pv if k2 else 1)*(pv if k3 else 1)/pv**3/pv**((k1+k2+k3)/2)
              for k1 in range(60) for k2 in range(60) for k3 in range(60) if k1+k2+k3>0)
    closed=pv**-3*((1+pv**0.5/(1-pv**-0.5))**3-1)
    print("Euler factor p=%d: brute %.6g closed %.6g  p^1.5*val %.4g"%(pv,exact,closed,exact*pv**1.5))
