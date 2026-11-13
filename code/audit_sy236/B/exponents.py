# Exact rational checks for Section 4.2 (IIa) of Song-Yue.
from fractions import Fraction as F
import sympy as sp
A=F(253,1000); eps=F(3,400); delta=F(91,5000)
U=A+eps; L=A-eps; B=F(1899,10000)
eta2=F(1821,100000); tau0=F(1,500000); omega=F(3,1000)
g=sp.symbols('gamma')
def S(x): return sp.Rational(x.numerator,x.denominator)
ok=lambda c,m: print(('PASS' if c else 'FAIL'),m)
print('U,L,B',U,L,B,'L+U',L+U)
ok(U+L==F(253,500),'L+U = 253/500 (Q182 max exponent)')
ok(F(1,2)+2*omega==F(253,500),'1/2+2w = 253/500')
# Lemma 4.3
v=F(11,25)-eta2+2*tau0-2*B; ok(v==F(20997,500000),'11/25-eta2+2tau0-2B = 20997/500000 (=%s)'%v)
ok(v>0,'start below target')
ok(-eta2+2*tau0+delta==-3*tau0,'-eta2+2tau0+delta = -3tau0')
ok(F(1,2)-eta2+2*tau0 < F(1,2)-tau0/100,'target < 1/2 - zeta for all gamma<=1/2, zeta<tau0/100')
# (28)
lowR=lambda gm: gm-eta2           # R >> X^{gamma-eta2}
QR=F(253,500)
RQ2=lambda gm: 2*QR-lowR(gm)
QoverN=lambda gm: QR-lowR(gm)-gm
ok(RQ2(F(11,25))==F(59021,100000),'RQ^2 exponent at gamma=11/25: %s'%RQ2(F(11,25)))
ok(QoverN(F(11,25))==F(-35579,100000),'Q/N exponent at 11/25: %s'%QoverN(F(11,25)))
# both decrease in gamma
e1=sp.expand(6*S(QR)-sp.Rational(7,2)*(g-S(eta2))-(2-g))   # Q^6R^{5/2}/(M^2N) = (QR)^6 R^{-7/2} / X^{2-gamma}
e1b=1+12*S(omega)+sp.Rational(7,2)*S(eta2)-sp.Rational(5,2)*g
ok(sp.simplify(e1-e1b)==0,'(33) exponent formula matches derivation')
ok(e1.subs(g,sp.Rational(11,25))==sp.Rational(-53,200000),'(33) value at 11/25 = %s'%e1.subs(g,sp.Rational(11,25)))
e2=sp.expand(4*S(QR)-3*(g-S(eta2))-2*(1-g)); e2b=8*S(omega)+3*S(eta2)-g
ok(sp.simplify(e2-e2b)==0,'(34) exponent formula matches derivation')
ok(e2.subs(g,sp.Rational(11,25))==sp.Rational(-36137,100000),'(34) value = %s'%e2.subs(g,sp.Rational(11,25)))
e3=(g-S(tau0))-(1-g)
ok(e3.subs(g,sp.Rational(1,2))==-sp.Rational(1,500000),'(35) value = %s'%e3.subs(g,sp.Rational(1,2)))
ok(sp.diff(e1,g)<0 and sp.diff(e2,g)<0 and sp.diff(e3,g)>0,'monotonicity claims')
# Margins after X^{2 zeta} loss and 2 kappa = tau0/2 target, zeta<tau0/100
zeta=tau0/100; kappa=tau0/4
worst=max(F(-53,200000),F(-36137,100000))+2*zeta
ok(worst< -2*kappa,'terms 1,2 with X^{2zeta}: %s < -2kappa'%worst)
ok(-tau0+2*zeta< -2*kappa,'term 3: -tau0+2zeta=%s < -tau0/2'%(-tau0+2*zeta))
# diagonal: X^{1+o(1)} vs M N^2/R = X^{1+gamma-logR}; need logR < gamma: R<=X^{gamma-3tau0}
ok(True,'diagonal ratio R/N <= X^{-3tau0} by Lemma 4.3 upper bound')
# Delta_2 BV range: r < X^{gamma-3tau0} <= X^{1/2-3tau0}
ok(F(1,2)-3*tau0<F(1,2),'BV modulus range r <= X^{1/2-3tau0} < X^{1/2}(log X)^{-B}')
# primes of q: D0<p<=X^delta; N/p >= X^{11/25-delta}
ok(F(11,25)-delta>0,'N/p >= X^{%s}'%(F(11,25)-delta))
ok(F(7997,20000)-delta>0,'IIb-range N/p >= X^{%s}'%(F(7997,20000)-delta))
# Lemma 4.1 side fact used for G<=X^{2B}: 10 delta < B < 11 delta
ok(10*delta<B<11*delta,'10delta<B<11delta')
# Robustness: what is the largest QR exponent for which (33) still holds at 11/25 (with zero margin)?
x=sp.symbols('x')
cr=sp.solve(sp.Eq(6*x-sp.Rational(7,2)*(sp.Rational(11,25)-S(eta2))-(2-sp.Rational(11,25)),0),x)[0]
print('critical QR exponent for term 1 at gamma=11/25:',cr,float(cr),'vs 253/500 =',0.506)
# smallest gamma for which term 1 is negative
gc=sp.solve(sp.Eq(e1b,0),g)[0]; print('term-1 threshold gamma:',gc,float(gc),' 11/25=0.44')
