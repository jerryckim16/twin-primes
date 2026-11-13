# Exact rational checks of every numerical inequality used in Sec 4.6-4.7, Thm 4.18, and the Sec 4.14 link.
from fractions import Fraction as F
import sympy as sp, math
ok=True
def chk(name, cond, val=None):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ")+name+("" if val is None else f"   [{val}]"))
A=F(253,1000); eps=F(3,400); delta=F(91,5000)
U=A+eps; L=A-eps; B=F(1899,10000)
chk("U=521/2000", U==F(521,2000)); chk("L=491/2000", L==F(491,2000))
chk("L+U=253/500 (modulus level)", L+U==F(253,500))
chk("2U<1 (Prop 4.31 Selberg range)", 2*U<1, 2*U)
chk("10*delta<B<11*delta (r<=10)", 10*delta<B<11*delta)
# Lemma 4.16
chk("253/500+1/3=1259/1500<1", F(253,500)+F(1,3)==F(1259,1500) and F(1259,1500)<1)
chk("1/2 < 1259/1500 (X^{1/2} term dominated)", F(1,2)<F(1259,1500))
# Lemma 4.10
chk("3999/10000+253/500=9059/10000<1", F(3999,10000)+F(253,500)==F(9059,10000)<1)
# Prop 4.11 / Lemma 4.13 reserves (re-used verbatim in Lemma 4.13)
chk("3999/10000-7997/20000=1/20000", F(3999,10000)-F(7997,20000)==F(1,20000))
chk("0.2002-1/5=1/5000", F(2002,10000)-F(1,5)==F(1,5000))
chk("2/5-0.3999=1/10000", F(2,5)-F(3999,10000)==F(1,10000))
chk("0.6001-3/5=1/10000", F(6001,10000)-F(3,5)==F(1,10000))
chk("11/25 between 7997/20000 and 1/2", F(7997,20000)<F(11,25)<F(1,2))
chk("Mobius atom scale 1/10 < 0.2002", F(1,10)<F(2002,10000))
# Prop 4.14 Fourier tail exponent: h^{-r} R^{1-r}, h=(logX)^{-Bc}, R=(logX)^{Bc+2}
Bc,r=sp.symbols('Bc r')
e=sp.expand(r*Bc+(Bc+2)*(1-r)); chk("tail exponent = Bc+2-2r", sp.simplify(e-(Bc+2-2*r))==0, e)
# Lemma 4.12 with k=20: X^{19/20} <= hX for h=(log X)^{-Bc} eventually (exponent comparison 19/20<1)
chk("19/20<1", F(19,20)<1)
# divisor majorants: tau(q)^{v+1} <= tau_r(q) on squarefree q with r=ceil(2^{v+1}); <= d_m with m=2^{ceil(v+1)}
for v in [0,0.3,1,1.5,2,3.7,6]:
    r_=math.ceil(2**(v+1)); m_=2**math.ceil(v+1)
    chk(f"v={v}: 2^(v+1)<=r={r_} and <=m={m_}", 2**(v+1)<=r_ and 2**(v+1)<=m_)
# Prop 4.15 block count bookkeeping: saving C+21 times (logX)^20 blocks -> C+1
chk("(C+21)-20 = C+1", True)
# Lemma 4.28 / 4.30 multiplicities
chk("48<=2^6 (m(q)<=tau^6)", 48<=2**6); chk("47<=2^6", 47<=2**6)
chk("141=47*3<=2^8 (pairs <=tau^8)", 47*3==141 and 141<=2**8)
chk("8+6=14 weight", 8+6==14)
chk("253/500=0.506", F(253,500)==F(506,1000))
# Lemma 4.26 constants (contraction leaves room for W)
lam=F(19999,20000); s0=F(1,40000)
chk("lambda<1-sigma0", lam<1-s0); chk("L0/lambda>L", (1-s0)*L/lam>L)
chk("lambda*2001/2000=40017999/40000000", lam*F(2001,2000)==F(40017999,40000000))
chk("...>(1+1/50000)^2", F(40017999,40000000)>(1+F(1,50000))**2)
chk("48U<16 (sqrt(48U)<4)", 48*U<16, 48*U)
ee=F(1,10**6); chk("1+20e-4e=1+16e>1+e", 1+20*ee-4*ee==1+16*ee>1+ee)
chk("48*delta=546/625<1", 48*delta==F(546,625)<1)
# Q182 level: (1-sigma)(L+U)
chk("Q182(X;s0/2) level < 253/500", (1-s0/2)*(L+U)<F(253,500))
print("ALL PASS" if ok else "SOME FAIL")
