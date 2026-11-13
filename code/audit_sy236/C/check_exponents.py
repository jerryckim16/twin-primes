# Exact-arithmetic checks for Song-Yue Section 4.3 (IIb), plus symbolic algebra of (42)-(43).
from fractions import Fraction as F
import sympy as sp

delta=F(91,5000); B=F(1899,10000); A=F(253,1000)
eta2=F(1821,100000); tau0=F(1,500000); omega=F(3,1000)
gs=F(7997,20000); gmax=F(11,25)
a=lambda g: F(1,2)-g-2*omega
ok=True
def chk(name,val,claim=None,pos=None):
    global ok
    s=f"{name} = {val}"
    if claim is not None:
        s+=f"  claimed {claim}  {'OK' if val==claim else 'MISMATCH'}"; ok&= (val==claim)
    if pos is not None:
        good=(val>0) if pos else (val<0); s+=f"  sign {'OK' if good else 'FAIL'}"; ok&=good
    print(s)

print("--- parameters")
chk("2A = 1/2+2*omega", 2*A, F(1,2)+2*omega)
chk("eta2-delta", eta2-delta, 5*tau0)
chk("10*delta < B < 11*delta", (10*delta<B<11*delta))
print("--- Lemma 4.5")
chk("gamma*-eta2+2tau0-2B", gs-eta2+2*tau0-2*B, F(461,250000), True)
chk("a_{11/25}-eta2+2tau0", a(gmax)-eta2+2*tau0, F(17897,500000), True)
# q exponent minus u-target exponent (zeta -> 0): (1/2-g+3tau0)-(a(g)-eta2+2tau0)
g=sp.symbols('g')
excess=(sp.Rational(1,2)-g+3*sp.Rational(1,500000)) - (sp.Rational(1,2)-g-2*sp.Rational(3,1000)-sp.Rational(1821,100000)+2*sp.Rational(1,500000))
print("q-exponent minus u-target:", sp.simplify(excess), "= 2w+eta2+tau0 =", 2*omega+eta2+tau0)
chk("u window width = delta", (a(gs)-3*tau0)-(a(gs)-eta2+2*tau0), delta)
chk("excess > delta (so u is a proper divisor of q)", 2*omega+eta2+tau0-delta, None, True)
# r target must be below 1/2 - zeta (full modulus exceeds target):
chk("1/2 - (11/25 - eta2 + 2tau0)", F(1,2)-(gmax-eta2+2*tau0), None, True)
print("--- (38)")
chk("1+4w-g*+eta2", 1+4*omega-gs+eta2, F(15759,25000))
chk("RQ^2 exponent < 1", 1+4*omega-gs+eta2-1, None, False)
chk("1/2+2w-2g*+eta2", F(1,2)+2*omega-2*gs+eta2, F(-27549,100000), False)
print("--- E exponents at gamma*")
chk("(1+24w+7eta2-3g*)/2", (1+24*omega+7*eta2-3*gs)/2, F(-1,25000), False)
chk("8w+3eta2-g*", 8*omega+3*eta2-gs, F(-16061,50000), False)

gg=sp.symbols('gamma')
w_,e_,t_=sp.Rational(3,1000),sp.Rational(1821,100000),sp.Rational(1,500000)
ag=sp.Rational(1,2)-gg-2*w_
E3=(ag-t_)+(sp.Rational(1,2)+2*w_)-(1-gg)
print("E3 exponent:",sp.simplify(E3),"(claimed -tau0 =",-t_,")"); ok&= sp.simplify(E3+t_)==0

# ---- Symbolic re-derivation of (42),(43) and E1,E2,E3 from (40),(41), A1
q0,U1,V,R,Q,M,N,H,z=sp.symbols('q0 U1 V R Q M N H z',positive=True)
A1=z*N*U1*Q/q0**2
A2=z*(U1*Q/q0)*(H**2*V**2*sp.sqrt(R*U1*V**2*Q) + N/(q0*R)*H*V*(H*V+R))
Hval=R*Q**2/(q0*M)   # X^zeta dropped
A2s=sp.expand(A2.subs(H,Hval))
claim42=z*(q0**-3*U1**sp.Rational(3,2)*V**3*R**sp.Rational(5,2)*Q**sp.Rational(11,2)*M**-2
           + q0**-4*U1*V**2*R*Q**5*N*M**-2 + q0**-3*U1*V*R*Q**3*N/M)
print("(42) algebra difference:",sp.simplify(A2s-claim42)); ok&= sp.simplify(A2s-claim42)==0
norm=z*Q**2*V*N/q0
E1=q0**-2*U1**sp.Rational(3,2)*V**2*R**sp.Rational(5,2)*Q**sp.Rational(7,2)/(M**2*N)
E2=q0**-3*U1*V*R*Q**3/M**2
E3s=q0**-2*U1*R*Q/M
print("normalization difference:",sp.simplify(claim42/norm-(E1+E2+E3s)))
Vsub=Q/(q0*U1)
print("E1 alt form diff:",sp.simplify(E1.subs(V,Vsub)-q0**-4*U1**sp.Rational(-1,2)*R**sp.Rational(5,2)*Q**sp.Rational(11,2)/(M**2*N)))
print("E2 alt form diff:",sp.simplify(E2.subs(V,Vsub)-q0**-4*R*Q**4/M**2))
print("(43) prefactor A1*norm with U1V=Q/q0 :",sp.simplify((A1*norm).subs(V,Vsub)),"claimed N^2Q^4z^2/q0^4")

# ---- LP check of E1,E2 exponent bounds in log_X variables (worst case over admissible R,Q)
lr,lq,lu,lq0=sp.symbols('lr lq lu lq0',real=True)
# constraints: lr >= g-eta2, lr+lq <= 1/2+2w, lu >= ag-eta2-lq0, lq0>=0; M = X^{1-g}, N=X^g
e1=-4*lq0-lu/2+sp.Rational(5,2)*lr+sp.Rational(11,2)*lq-2*(1-gg)-gg
# e1 increasing in lq, decreasing in lu -> substitute extremes
e1w=e1.subs(lq,sp.Rational(1,2)+2*w_-lr).subs(lu,ag-e_-lq0)
print("E1 exponent after lq,lu extremes:",sp.expand(e1w))   # coefficient of lr should be negative
e1w2=sp.expand(e1w.subs(lr,gg-e_))
print("E1 worst:",e1w2," claimed (1+24w+7eta2-3g)/2 - (7/2)lq0:",sp.expand((1+24*w_+7*e_-3*gg)/2-sp.Rational(7,2)*lq0))
e2=-4*lq0+lr+4*lq-2*(1-gg)
e2w=sp.expand(e2.subs(lq,sp.Rational(1,2)+2*w_-lr).subs(lr,gg-e_))
print("E2 worst:",e2w," claimed:",sp.expand(8*w_+3*e_-gg-4*lq0))
gs_=sp.Rational(7997,20000)
print("E1 at gamma*:",((1+24*w_+7*e_-3*gg)/2).subs(gg,gs_),"E2 at gamma*:",(8*w_+3*e_-gg).subs(gg,gs_))
# kappa check: need max_i(exp_i)/2 + zeta < -kappa with kappa=tau0/8, zeta<tau0/1000
kap=t_/8; zt=t_/1000
for nm,ex in [("E1",sp.Rational(-1,25000)),("E2",sp.Rational(-16061,50000)),("E3",-t_)]:
    v=ex/2+zt+kap; print(nm,"ex/2+zeta+kappa =",v, "OK" if v<0 else "FAIL"); ok&= v<0
print("ALL OK" if ok else "SOME CHECK FAILED")
