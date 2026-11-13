#!/usr/bin/env python3
"""Exact-rational verification of every numerical parameter claim found in
Song--Yue (ePrint 2026/1893) Sections 4.1--4.7 (plus two nearby constants).
Each check prints PASS/FAIL. Exponents of X are tracked as exact Fractions;
symbolic gamma-dependence is handled with sympy and checked for monotonicity."""
from fractions import Fraction as F
import sympy as sp

fails = []
def chk(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("   [" + detail + "]" if detail else ""))
    if not cond: fails.append(name)

# ---------------- Section 4.1 ----------------
k=48; A=F(253,1000); eps=F(3,400); delta=F(91,5000); B=F(1899,10000)
U=A+eps; L=A-eps
chk("4.1 U=A+eps=521/2000", U==F(521,2000), str(U))
chk("4.1 L=A-eps=491/2000", L==F(491,2000), str(L))
chk("4.1 L+U=253/500 (so q<=X^{(1-sig)253/500})", L+U==F(253,500))
chk("4.1 253/500<1", F(253,500)<1)
chk("L4.1 delta<B", delta<B)
chk("L4.1 10*delta<B<11*delta", 10*delta<B<11*delta, f"{10*delta},{B},{11*delta}")
# max number of rough factors forced by f_i>=X^delta and prod f_i<=X^B
mmax = max(m for m in range(0,100) if m*delta<=B)
chk("Q182: m*delta<=B forces m<=10 (bound 'm<=54' in def is vacuous)", mmax==10, f"mmax={mmax}")
chk("L4.24 48*delta=546/625<1", 48*delta==F(546,625) and 48*delta<1)
twoB = 2*B
chk("2B=1899/5000", twoB==F(1899,5000))

# ---------------- Section 4.2 (IIa) ----------------
eta2=F(1821,100000); tau0=F(1,500000); om=F(3,1000)
chk("4.2 1/2+2*omega=253/500", F(1,2)+2*om==F(253,500))
chk("L4.3 11/25-eta2+2tau0-2B=20997/500000>0", F(11,25)-eta2+2*tau0-2*B==F(20997,500000))
chk("L4.3 overshoot: -eta2+2tau0+delta = -3tau0  (i.e. delta=eta2-5tau0)", -eta2+2*tau0+delta==-3*tau0)
# target below full modulus: gamma-eta2+2tau0 < 1/2-zeta for gamma<=1/2, zeta<tau0/100
chk("L4.3 target < 1/2-zeta at gamma=1/2 (zeta<tau0/100)", F(1,2)-eta2+2*tau0 < F(1,2)-tau0/100)
g=sp.symbols('gamma')
e2,t0,w,dl,Bs=[sp.Rational(x.numerator,x.denominator) for x in (eta2,tau0,om,delta,B)]
# (28)
RQ2 = 2*(sp.Rational(1,2)+2*w) - (g-e2)            # RQ^2=(QR)^2/R, R>>X^{gamma-eta2}
QN  = (sp.Rational(1,2)+2*w) - (g-e2) - g          # Q/N
chk("(28) RQ^2 exponent at gamma=11/25 = 59021/100000 (decreasing in gamma)",
    RQ2.subs(g,sp.Rational(11,25))==sp.Rational(59021,100000) and sp.diff(RQ2,g)<0)
chk("(28) Q/N exponent at gamma=11/25 = -35579/100000 (decreasing)",
    QN.subs(g,sp.Rational(11,25))==sp.Rational(-35579,100000) and sp.diff(QN,g)<0)
chk("(28) RQ^2 exponent <1 (diagonal progression modulus)", sp.Rational(59021,100000)<1)
# (33)-(35): derive from Q,R bounds independently
QR=sp.Rational(1,2)+2*w; Rlo=g-e2; Mexp=1-g; Nexp=g
t1 = 6*QR - sp.Rational(7,2)*Rlo - (2*Mexp+Nexp)   # Q^6R^{5/2}/(M^2N)=(QR)^6 R^{-7/2}/(M^2N)
t2 = 4*QR - 3*Rlo - 2*Mexp                          # RQ^4/M^2=(QR)^4R^{-3}/M^2
t3 = (g - t0) - Mexp                                # R/M, R<<N X^{-tau0}
chk("(33) form 1+12w+7eta2/2-5g/2", sp.simplify(t1-(1+12*w+sp.Rational(7,2)*e2-sp.Rational(5,2)*g))==0)
chk("(33) value at 11/25 = -53/200000", t1.subs(g,sp.Rational(11,25))==sp.Rational(-53,200000))
chk("(34) form 8w+3eta2-g and value -36137/100000", sp.simplify(t2-(8*w+3*e2-g))==0 and t2.subs(g,sp.Rational(11,25))==sp.Rational(-36137,100000))
chk("(35) form 2g-1-tau0 and value at 1/2 = -1/500000", sp.simplify(t3-(2*g-1-t0))==0 and t3.subs(g,sp.Rational(1,2))==-sp.Rational(1,500000))
chk("(33),(34) decrease, (35) increases in gamma", sp.diff(t1,g)<0 and sp.diff(t2,g)<0 and sp.diff(t3,g)>0)
# kappa=tau0/4, zeta<tau0/100: need 2kappa+2zeta < min margin
marg = min(F(53,200000),F(36137,100000),F(1,500000))
chk("IIa: 2*kappa+2*zeta < min margin (kappa=tau0/4, zeta<tau0/100)", 2*(tau0/4)+2*(tau0/100) < marg)
print("NOTE IIa: BV range R<<N X^-tau0<=X^{1/2-tau0} (by inspection)")
chk("IIa/IIb: 7997/20000 - delta >0 (N/p grows by fixed power)", F(7997,20000)-delta>0)
# check (32) algebra symbolically
Nn,Qq,Rr,Mm,z,q0,H,ze,X=sp.symbols('N Q R M z q0 H zeta X',positive=True)
K0=Qq/q0
lhs = (Nn*z/q0)*( H**2*K0**4*z*Qq**2*sp.sqrt(Rr)/q0**2 + z*Nn/(q0*Rr)*H*K0**2*(H*K0**2+Rr) )
rhs = Nn**2*Qq**4*z**2/q0**4*(H**2*Qq**2*sp.sqrt(Rr)/Nn + H**2/Rr + H/Qq**2)
ratio_terms = sp.simplify(sp.expand(rhs - lhs))
# rhs-lhs should be a sum of nonneg terms for q0>=1: check termwise ratio
A_ = (Nn*z/q0)*H**2*K0**4*z*Qq**2*sp.sqrt(Rr)/q0**2; A2=Nn**2*Qq**4*z**2/q0**4*H**2*Qq**2*sp.sqrt(Rr)/Nn
B_ = (Nn*z/q0)*z*Nn/(q0*Rr)*H**2*K0**4;            B2=Nn**2*Qq**4*z**2/q0**4*H**2/Rr
C_ = (Nn*z/q0)*z*Nn/(q0*Rr)*H*K0**2*Rr;            C2=Nn**2*Qq**4*z**2/q0**4*H/Qq**2
chk("(32) line 1 from (30),(31): ratios are q0^-3, q0^-2, 1",
    sp.simplify(A_/A2-q0**-3)==0 and sp.simplify(B_/B2-q0**-2)==0 and sp.simplify(C_/C2-1)==0)
Hs = X**ze*Rr*Qq**2/Mm
chk("(32) line 2 after H=X^zeta R Q^2/M",
    sp.simplify((Hs**2*Qq**2*sp.sqrt(Rr)/Nn)/(X**(2*ze)*Qq**6*Rr**sp.Rational(5,2)/(Mm**2*Nn)))==1 and
    sp.simplify((Hs**2/Rr)/(X**(2*ze)*Rr*Qq**4/Mm**2))==1 and sp.simplify((Hs/Qq**2)/(X**ze*Rr/Mm))==1)

# ---------------- Section 4.3 (IIb) ----------------
gs=F(7997,20000)
a = lambda gam: F(1,2)-gam-2*om
chk("L4.5 gamma*-eta2+2tau0-2B=461/250000>0", gs-eta2+2*tau0-2*B==F(461,250000))
chk("L4.5 a_{11/25}-eta2+2tau0=17897/500000>0", a(F(11,25))-eta2+2*tau0==F(17897,500000))
chk("L4.5 u-target is minimal at gamma=11/25 (a_gamma decreasing)", a(gs)>a(F(11,25)))
chk("L4.5 q-excess 2w+eta2+tau0-zeta>0", 2*om+eta2+tau0-tau0/1000>0)
chk("L4.5 u overshoot: a-eta2+2tau0+delta=a-3tau0", -eta2+2*tau0+delta==-3*tau0)
RQ2b = 1+4*w-g+e2; QNb = sp.Rational(1,2)+2*w-2*g+e2
chk("(38) RQ^2 exponent: 2(1/2+2w)-(g-eta2) == 1+4w-g+eta2", sp.simplify(2*QR-(g-e2)-RQ2b)==0)
chk("(38) RQ^2 at gamma*=15759/25000", RQ2b.subs(g,sp.Rational(7997,20000))==sp.Rational(15759,25000))
chk("(38) Q/N at gamma*=-27549/100000", QNb.subs(g,sp.Rational(7997,20000))==sp.Rational(-27549,100000))
chk("(38) both decreasing in gamma, RQ^2<X, Q<N", sp.diff(RQ2b,g)<0 and sp.diff(QNb,g)<0 and sp.Rational(15759,25000)<1)
# E1,E2,E3 derivations
U1,V,q0s=sp.symbols('U1 V q0',positive=True)
E1=q0s**-2*U1**sp.Rational(3,2)*V**2*Rr**sp.Rational(5,2)*Qq**sp.Rational(7,2)/(Mm**2*Nn)
E1b=E1.subs(V,Qq/(q0s*U1))
chk("IIb E1 ~ q0^-4 U1^-1/2 R^5/2 Q^11/2/(M^2N)", sp.simplify(E1b/(q0s**-4*U1**sp.Rational(-1,2)*Rr**sp.Rational(5,2)*Qq**sp.Rational(11,2)/(Mm**2*Nn)))==1)
E2=(q0s**-3*U1*V*Rr*Qq**3/Mm**2).subs(V,Qq/(q0s*U1))
chk("IIb E2 ~ q0^-4 R Q^4/M^2", sp.simplify(E2/(q0s**-4*Rr*Qq**4/Mm**2))==1)
# normalisation of (42) with A1
zz=sp.symbols('zz',positive=True)
A1=zz*Nn*U1*Qq/q0s**2
t42=[zz*q0s**-3*U1**sp.Rational(3,2)*V**3*Rr**sp.Rational(5,2)*Qq**sp.Rational(11,2)/Mm**2,
     zz*q0s**-4*U1*V**2*Rr*Qq**5*Nn/Mm**2, zz*q0s**-3*U1*V*Rr*Qq**3*Nn/Mm]
Es=[E1, q0s**-3*U1*V*Rr*Qq**3/Mm**2, q0s**-2*U1*Rr*Qq/Mm]
norm=Nn**2*Qq**4*zz**2/q0s**4
ok=all(sp.simplify(((A1*t)/(norm*E)).subs(V,Qq/(q0s*U1)))==1 for t,E in zip(t42,Es))
chk("(43) A1*A2 normalised = N^2Q^4z^2/q0^4 (E1+E2+E3) under U1 V = Q/q0", ok)
# (42) from A2 bound
Hb_=X**ze*Rr*Qq**2/(q0s*Mm)
first=zz*(U1*Qq/q0s)*Hb_**2*V**2*sp.sqrt(Rr*U1*V**2*Qq)
second=zz*(U1*Qq/q0s)*(Nn/(q0s*Rr))*Hb_**2*V**2
third=zz*(U1*Qq/q0s)*(Nn/(q0s*Rr))*Hb_*V*Rr
chk("(42) three summands after substituting H",
    sp.simplify(first/(X**(2*ze)*t42[0]))==1 and sp.simplify(second/(X**(2*ze)*t42[1]))==1 and sp.simplify(third/(X**ze*t42[2]))==1)
# exponents
ag = sp.Rational(1,2)-g-2*w
E1exp = -(ag-e2)/2 + sp.Rational(5,2)*0 + (sp.Rational(11,2)*QR - 3*(g-e2)) - (2*(1-g)+g)
chk("IIb E1 exponent == (1+24w+7eta2-3g)/2", sp.simplify(E1exp-(1+24*w+7*e2-3*g)/2)==0)
chk("IIb E1 value at gamma* = -1/25000", ((1+24*w+7*e2-3*g)/2).subs(g,sp.Rational(7997,20000))==-sp.Rational(1,25000))
chk("IIb E2 value at gamma* = -16061/50000", (8*w+3*e2-g).subs(g,sp.Rational(7997,20000))==-sp.Rational(16061,50000))
E3exp=(ag-t0)+QR-(1-g)
chk("IIb E3 exponent == -tau0", sp.simplify(E3exp+t0)==0)
chk("IIb: 2kappa+2zeta < min margin (kappa=tau0/8, zeta<tau0/1000)", 2*(tau0/8)+2*(tau0/1000) < min(F(1,25000),F(16061,50000),tau0))
chk("IIb BV range R<<N X^-tau0 <= X^{11/25-tau0} < X^{1/2}", F(11,25)<F(1,2))

# ---------------- Section 4.4 (Type III) ----------------
eta3=F(39,1000)
s3=F(1,3)+4*eta3/3-4*om/3
chk("4.4 s3=143/375", s3==F(143,375))
chk("L4.7 343/1000+delta=903/2500<2B", F(343,1000)+delta==F(903,2500) and F(903,2500)<2*B)
chk("L4.7 343/1000-(s3-eta3)=1/1500>0", F(343,1000)-(s3-eta3)==F(1,1500))
chk("L4.7 s3-2B=23/15000>0", s3-2*B==F(23,15000))
chk("L4.7 343/1000 < 1/2-zeta (target below modulus)", F(343,1000)<F(1,2)-F(1,1000))
chk("P4.6 1/2+eta3-s3=473/3000>0", F(1,2)+eta3-s3==F(473,3000))
chk("P4.6 pair products => N>=X^{9/10}, M<=X^{1/10}", 3*F(3,5)/2==F(9,10))
ww,e3=sp.Rational(3,1000),sp.Rational(39,1000)
S3=sp.Rational(1,3)+4*e3/3-4*ww/3; Qx=sp.Rational(1,2)+2*ww; Mx=sp.Rational(1,10); Nx=sp.Rational(9,10)
x1=Mx/2+sp.Rational(3,2)*Qx+S3/2
x2=Mx+sp.Rational(3,2)*Qx+S3/4
x3=e3/4+1-Nx/2+Qx-S3/4          # X^{eta3/4} M Q S^{-1/4} N^{1/2}, M=X/N
chk("(52) term1 = 2/3+7w/3+3/10+2eta3/3 = 1-1/3000", x1==sp.Rational(2,3)+7*ww/3+sp.Rational(3,10)+2*e3/3 and x1==1-sp.Rational(1,3000))
chk("(52) term2 = 1/3+8w/3+3/5+eta3/3 = 1-137/3000", x2==sp.Rational(1,3)+8*ww/3+sp.Rational(3,5)+e3/3 and x2==1-sp.Rational(137,3000))
chk("(52) term3 = 2/3+7w/3+3/10-eta3/12 = 1-71/2400", x3==sp.Rational(2,3)+7*ww/3+sp.Rational(3,10)-e3/12 and x3==1-sp.Rational(71,2400))
chk("(52) all three <1 and min margin 1/3000 > 1/12000", max(x1,x2,x3)==1-sp.Rational(1,3000) and sp.Rational(1,3000)>sp.Rational(1,12000))
# T bound -> (52)
b,Bst,Mm2,Ss,Hbb=sp.symbols('b Bst M S Hb',positive=True)
Hbv=Qq**3/(Bst*Nn)
T1=Hbv; T20=Hbv*Mm2*Qq*Ss/b; T2n=Mm2**2*Qq*sp.sqrt(Ss)*Hbv/b + X**(e3/2)*Mm2**2*Qq**3/(b**sp.Rational(5,2)*sp.sqrt(Ss))
terms=[sp.sqrt(T1*Hbv*Mm2*Qq*Ss/b), sp.sqrt(T1*Mm2**2*Qq*sp.sqrt(Ss)*Hbv/b), sp.sqrt(T1*X**(e3/2)*Mm2**2*Qq**3/(b**sp.Rational(5,2)*sp.sqrt(Ss)))]
tgt=[Mm2**sp.Rational(1,2)*Qq**sp.Rational(7,2)*Ss**sp.Rational(1,2)/(b**sp.Rational(1,2)*Bst*Nn),
     Mm2*Qq**sp.Rational(7,2)*Ss**sp.Rational(1,4)/(b**sp.Rational(1,2)*Bst*Nn),
     X**(e3/4)*Mm2*Qq**3/(b**sp.Rational(5,4)*Bst**sp.Rational(1,2)*Ss**sp.Rational(1,4)*Nn**sp.Rational(1,2))]
chk("P4.6 T-bound from T^2<=T1*T2", all(sp.simplify(t/u)==1 for t,u in zip(terms,tgt)))
fin=[(Nn/Qq**2)*t*b*sp.sqrt(Bst) for t in tgt]  # after weakening denominators to b*B*^{1/2}
f52=[Mm2**sp.Rational(1,2)*Qq**sp.Rational(3,2)*Ss**sp.Rational(1,2), Mm2*Qq**sp.Rational(3,2)*Ss**sp.Rational(1,4), X**(e3/4)*Mm2*Qq*Ss**sp.Rational(-1,4)*Nn**sp.Rational(1,2)]
# weakening: each denominator b^x B*^y >= b B*^{1/2}; check the exponents
print("NOTE P4.6 denominators b^{1/2}B*, b^{5/4}B*^{1/2} >= b B*^{1/2} since B*>=b (by inspection)")
T52=[Mm2**sp.Rational(1,2)*Qq**sp.Rational(7,2)*Ss**sp.Rational(1,2)/Nn, Mm2*Qq**sp.Rational(7,2)*Ss**sp.Rational(1,4)/Nn, X**(e3/4)*Mm2*Qq**3/(Ss**sp.Rational(1,4)*Nn**sp.Rational(1,2))]
chk("(52) from (48): (N/Q^2)*numerators", all(sp.simplify((Nn/Qq**2)*t/f)==1 for t,f in zip(T52,f52)))
# Euler factor
p=sp.symbols('p',positive=True)
ef = p**-3*((1+sum(p**(1-sp.Rational(e,2)) for e in range(1,200)))**3-1)
chk("P4.6 Euler factor: sum_{e>=1} p^{1-e/2} = p^{1/2}/(1-p^{-1/2}) (numeric p=2,3,101)",
    all(abs(float(sum(pp**(1-e/2) for e in range(1,400)))-pp**0.5/(1-pp**-0.5))<1e-9 for pp in (2.0,3.0,101.0)))

# ---------------- Section 4.5 ----------------
s=F(1001,10000)
chk("L4.9 1/2+s=0.6001, 1/2-s=0.3999, 2s=0.2002", (F(1,2)+s, F(1,2)-s, 2*s)==(F(6001,10000),F(3999,10000),F(2002,10000)))
chk("L4.9 s>1/10 i.e. 4s>1/2-s", s>F(1,10) and 4*s>F(1,2)-s, f"4s-a={4*s-(F(1,2)-s)}")
chk("L4.9 2b>1", 2*(F(1,2)+s)>1)
chk("L4.10 3999/10000+253/500=9059/10000<1", F(3999,10000)+F(253,500)==F(9059,10000) and F(9059,10000)<1)
chk("L4.10 M<<X^{1-0.6001}=X^{0.3999}", 1-F(6001,10000)==F(3999,10000))
chk("P4.11 3999/10000-7997/20000=1/20000>0", F(3999,10000)-F(7997,20000)==F(1,20000))
chk("P4.11 IIa/IIb ranges abut at 11/25 (no gap): [7997/20000,11/25] U [11/25,1/2] contains [0.3999,1/2]", F(7997,20000)<=F(3999,10000) and F(11,25)<F(1,2))
chk("P4.11 TypeIII reserves 0.2002-1/5=1/5000, 2/5-0.3999=1/10000, 0.6001-3/5=1/10000",
    (2*s-F(1,5), F(2,5)-(F(1,2)-s), (F(1,2)+s)-F(3,5))==(F(1,5000),F(1,10000),F(1,10000)))
chk("P4.11 Mobius scale X^{1/10} < X^{0.2002} (selected Type III atoms are smooth)", F(1,10)<2*s)
print("NOTE (55): 2j<=20 => X/2^20<=P<=2^21 X ; P^u/X^u in [2^-20,2^21] for u in [0,1] (by inspection)")
print("NOTE HB: Z^10=2X so (mu-mu_Z)^{*10} vanishes on n<=2X (by inspection; identity re-derived in report)")

# ---------------- Sections 4.6--4.7 ----------------
chk("L4.12/(65) k=20: 1-1/k=19/20<1", F(19,20)<1)
r_=sp.symbols('r',positive=True); Bc=sp.symbols('Bcut',positive=True)
chk("(63) tail: h^{-r}R^{1-r}=(logX)^{Bcut+2-2r} with h=(logX)^{-Bcut},R=(logX)^{Bcut+2}",
    sp.simplify(r_*Bc+(Bc+2)*(1-r_)-(Bc+2-2*r_))==0)
chk("L4.16 253/500+1/3=1259/1500<1", F(253,500)+F(1,3)==F(1259,1500) and F(1259,1500)<1)

chk("4.7 endpoint cost X^{253/500}<<X(logX)^-C", F(253,500)<1)
# Remark 4.23 side numbers
chk("R4.23 39999/100000-39983/100000=1/6250", F(39999,100000)-F(39983,100000)==F(1,6250))
print("\nFAILED:", fails if fails else "none")
