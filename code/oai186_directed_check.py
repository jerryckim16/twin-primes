#!/usr/bin/python3
"""Independent check of the directed arithmetic of Sec. 2.3 of [14] (OpenAI, "Numerical certificate for
prime gaps at most 186", 30 Aug 2026), pp. 16-17, ending in (2.26); secondary: the renewal majorant (2.3), p. 12.

Written from the PDF only (pdftotext -layout + rendered pp. 16-17). Every decision is exact (Fraction / int),
an exact comparison of a binary64 value (converted exactly with Fraction) or a certain comparison of python-flint
arb balls. Floats appear (a) as the OBJECT under test (binary64 round-to-nearest arithmetic of the claimed rules,
whose every operation is itself re-checked against an exact round-to-nearest oracle) and (b) for printing.

SUCCESS CRITERION (fixed before deriving):
  S1  (2.26) holds exactly for every 1 <= r <= 98264; the printed numerator identity and the printed
      lower bound 1-(M^2+M)u-3Mu^2-2M^2u^3 > 0 are exact; ru, 1-ru are binary64-exact and the computed gamma_r
      satisfies the rounding model.
  S2  The chain "summation error <= gamma_{r-1} sum|x|, t >= (1-gamma_{r-1}) T, fl(gamma t) >= (1-u)^2 gamma T
      - 2^-1075, outward step absorbs >= 2^-1075" is checked exactly on every instance tested, and the
      endpoints enclose the exact sum on all instances (random, adversarial, near-underflow, r = 98264).
  S3  (2.22), (2.23), zero-prefix removal, (2.24), (2.25) + outward conversion and the four-product hull are
      exact-sound on all instances, including a 160-bit arb -> 224-bit fixed-point chain.
  S4  Every negative control (wrong rounding direction, missing outward step, too-small gamma, perturbed
      constants, wrong window in (2.3)) is caught.
NO-GO CRITERION: any exact counterexample to a positive check, re-run and confirmed, or a negative control that
  is NOT caught (the check would then be vacuous). Either is reported as such, not repaired silently.
"""
import math, random, sys, time, resource
from fractions import Fraction as Fr
from flint import arb, ctx

T0 = time.time()
random.seed(20261127)
NCHK = 0; NFAIL = 0; NNEG = 0; NNEGOK = 0

def check(name, ok, info=""):
    global NCHK, NFAIL
    NCHK += 1
    if not ok: NFAIL += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))

def negative(name, caught, info=""):
    """A negative control must be CAUGHT (i.e. the deliberately wrong variant must fail)."""
    global NNEG, NNEGOK
    NNEG += 1
    if caught: NNEGOK += 1
    print(f"[{'NEG-CAUGHT' if caught else 'NEG-MISSED'}] {name}" + (f"  ({info})" if info else ""))

U = Fr(1, 2**53)
uf = 2.0**-53
TINY = Fr(1, 2**1074)          # smallest subnormal
HALF_TINY = Fr(1, 2**1075)
RMAX = 98264

# ---------------------------------------------------------------- exact binary64 round-to-nearest oracle
def rn(x):
    """Exact round-to-nearest-even of a rational to binary64 (gradual underflow, no overflow)."""
    x = Fr(x)
    if x == 0: return 0.0
    s = -1 if x < 0 else 1
    a = abs(x)
    e = a.numerator.bit_length() - a.denominator.bit_length()
    if a < Fr(2)**e: e -= 1
    assert Fr(2)**e <= a < Fr(2)**(e+1)
    assert e < 1024, "overflow"
    qexp = max(e - 52, -1074)
    m = a / Fr(2)**qexp
    fl = m.numerator // m.denominator
    rem = m - fl
    if rem > Fr(1, 2) or (rem == Fr(1, 2) and fl % 2 == 1): fl += 1
    return s * math.ldexp(float(fl), qexp)

def exact_ok(op_result, exact_value):
    return Fr(op_result) == Fr(rn(exact_value))

MACH = {"ops": 0, "bad": 0}
def fadd(a, b):
    r = a + b
    MACH["ops"] += 1
    if Fr(r) != Fr(rn(Fr(a) + Fr(b))): MACH["bad"] += 1
    return r
def fmul(a, b):
    r = a * b
    MACH["ops"] += 1
    if Fr(r) != Fr(rn(Fr(a) * Fr(b))): MACH["bad"] += 1
    return r

def pred(x): return math.nextafter(x, -math.inf)
def succ(x): return math.nextafter(x, math.inf)

print("=" * 100)
print("Directed arithmetic of [14] Sec. 2.3 (pp. 16-17), (2.22)-(2.26); secondary (2.3) (p. 12)")
print("=" * 100)

# ================================================================== A. (2.26) exactly
print("\n--- A. The rounding slack (2.26) ---")
def gam(r): return r * U / (1 - r * U)
def lhs226(r, gr=None, grm1=None):
    gr = gam(r) if gr is None else gr
    grm1 = gam(r - 1) if grm1 is None else grm1
    return (1 - U)**2 * (1 - grm1) * gr - grm1

def num_printed(r, u):
    return 1 - (r*r + r)*u + (4*r*r - 3*r)*u**2 - (2*r*r - 2*r)*u**3

def lhs_general(r, u):
    g = lambda k: k*u/(1 - k*u)
    return (1 - u)**2 * (1 - g(r - 1)) * g(r) - g(r - 1)

# A1: "after removing the positive factor u/((1-ru)(1-(r-1)u)) its numerator is ..." -- an identity of
# rational functions in (r,u). After clearing the denominator (1-ru)(1-(r-1)u)(1-(r-1)u)... we check it as a
# polynomial identity of bidegree <= (6,6) on a 9x9 grid of distinct points avoiding poles (a proof), plus 300
# random rational points.
ok = True
pts = [(Fr(r), Fr(k, 97)) for r in range(1, 10) for k in range(1, 10)]
pts += [(Fr(random.randint(1, 10**6)), Fr(1, random.randint(10**7, 10**9))) for _ in range(300)]
for r, u in pts:
    den = (1 - r*u) * (1 - (r - 1)*u)
    if den == 0 or (1 - 2*(r-1)*u) == 0: continue
    if lhs_general(r, u) != u / den * num_printed(r, u): ok = False
check("A1 numerator identity of (2.26) (polynomial identity: 9x9 grid of bidegree<=6 + 300 random points)", ok)
# negative: perturbed numerator coefficient
bad = lambda r, u: 1 - (r*r + r)*u + (4*r*r - 2*r)*u**2 - (2*r*r - 2*r)*u**3
negative("A1n perturbed numerator (4r^2-2r in place of 4r^2-3r) fails the identity",
         any(lhs_general(r, u) != u/((1-r*u)*(1-(r-1)*u))*bad(r, u) for r, u in pts[:81]))

# A2: (2.26) for every r = 1..98264, exactly. Scaled numerator: 2^159 * num(r, 2^-53) is an integer.
def num_int(r):
    return 2**159 - (r*r + r)*2**106 + (4*r*r - 3*r)*2**53 - (2*r*r - 2*r)
minN = None; ok = True
for r in range(1, RMAX + 1):
    v = num_int(r)
    if v <= 0: ok = False
    if minN is None or v < minN[1]: minN = (r, v)
    # positivity of the removed factor
    if not (1 - r*U > 0 and 1 - (r-1)*U > 0): ok = False
check("A2 (2.26) numerator > 0 and removed factor > 0 for all 1 <= r <= 98264 (exact integers)", ok,
      f"min at r={minN[0]}: numerator = {float(Fr(minN[1], 2**159)):.15f}")
# direct (no factorisation) at r in a sample incl. endpoints
samp = [1, 2, 3, 1000, 65535, 65536, RMAX] + random.sample(range(1, RMAX + 1), 200)
check("A3 (2.26) evaluated directly as printed (exact Fractions) at 207 r incl. 1, 2, 98264",
      all(lhs226(r) > 0 for r in samp), f"value at r=98264: {float(lhs226(RMAX)):.6e}")
# A4: printed lower bound for M = 98264
M = RMAX
lb = 1 - (M*M + M)*U - 3*M*U**2 - 2*M*M*U**3
check("A4 1-(M^2+M)u-3Mu^2-2M^2u^3 > 0 for M = 98264 (exact)", lb > 0, f"= {float(lb):.15f}")
check("A5 numerator(r) >= that bound for every 1 <= r <= 98264 (exact integers)",
      all(num_int(r) >= lb * 2**159 for r in range(1, RMAX + 1, 1)))
# A6: range of validity: numerator is 1 + c1 r + c2 r^2 with c1, c2 < 0 (exact) -> strictly decreasing for r >= 0
c2 = -U + 4*U**2 - 2*U**3; c1 = -U - 3*U**2 + 2*U**3
assert num_printed(Fr(7), U) == 1 + c1*7 + c2*49
lo_, hi_ = 1, 2**40
while hi_ - lo_ > 1:
    mid = (lo_ + hi_)//2
    if num_int(mid) > 0: lo_ = mid
    else: hi_ = mid
rstar = lo_
check("A6 numerator strictly decreasing in r>=0 (c1,c2<0); (2.26) holds exactly iff r <= r*",
      c1 < 0 and c2 < 0 and lhs226(rstar) > 0 and lhs226(rstar + 1) <= 0, f"r* = {rstar} ~ {rstar:.4e}")
negative("A6n (2.26) at r = 10^8 > r* fails (the inequality is not vacuous)", lhs226(10**8) <= 0)
negative("A7n gamma_{r-1} used in place of gamma_r fails (2.26) at r = 2, 1000, 98264",
         all(lhs226(r, gr=gam(r-1)) <= 0 for r in (2, 1000, RMAX)))
# A8: machine representability and computed gamma_r
ok_repr = True; ok_gam = True; ok_gam2 = True; worst = Fr(0)
for r in range(1, RMAX + 1):
    ru = r * uf; one_m = 1.0 - ru
    if Fr(ru) != r*U or Fr(one_m) != 1 - r*U: ok_repr = False
    gh = ru / one_m
    if Fr(gh) != Fr(rn(Fr(ru)/Fr(one_m))): ok_gam = False      # division is RN
    rel = abs(Fr(gh) - gam(r)) / gam(r)
    worst = max(worst, rel)
    # with the ACTUAL computed constant: (1-u) gh (1-g_{r-1}) - g_{r-1} > 0
    if not ((1 - U) * Fr(gh) * (1 - gam(r-1)) - gam(r-1) > 0): ok_gam2 = False
check("A8 ru and 1-ru exactly representable in binary64 for all r <= 98264", ok_repr)
check("A9 computed gamma_r = RN(ru/(1-ru)) (oracle) and relative error <= u for all r", ok_gam and worst <= U,
      f"max rel err = {float(worst/U):.4f} u")
check("A10 with the computed gamma_r: (1-u) gamma_hat (1-gamma_{r-1}) > gamma_{r-1} for all r <= 98264", ok_gam2)
# A11: (1-u)^{r-1} >= 1 - gamma_{r-1} (used for t >= (1-gamma_{r-1}) T), exactly at r = 98264 (Bernoulli
# gives it for all r); computed with exact integers: (2^53-1)^(r-1) * (1-(r-1)u)^-1 ...
r = RMAX
lhs_pow = Fr((2**53 - 1)**(r - 1), 2**(53*(r - 1)))
check("A11 (1-u)^(r-1) >= 1-(r-1)u >= 1-gamma_{r-1} at r = 98264 (exact; Bernoulli for all r)",
      lhs_pow >= 1 - (r-1)*U >= 1 - gam(r-1))

# ================================================================== B. integer fixed-point rules
print("\n--- B. Fixed-point products (2.22), upper division (2.23), zero prefixes, correlation (2.24), (2.25) ---")
def fdiv(p, Q): return p // Q                    # floor (Python semantics, also for negatives)
def cdiv_223(p, Q): return (p + Q - 1) // Q       # (2.23) coefficientwise
def cdiv_exact(p, Q): return -((-p) // Q)

# B1 (2.23)
ok = True; cnt = 0
for b in (1, 5, 53, 64, 192, 224):
    Q = 2**b
    for _ in range(3000):
        p = random.randint(-2**(b + 40), 2**(b + 40)) if random.random() < 0.7 else random.randint(-3*Q, 3*Q)
        cnt += 1
        if cdiv_223(p, Q) != cdiv_exact(p, Q) or Fr(cdiv_223(p, Q)) < Fr(p, Q) or Fr(cdiv_223(p, Q)) - 1 >= Fr(p, Q):
            ok = False
check("B1 (2.23) floor((p+Q-1)/Q) = ceil(p/Q) for all tested integers p (incl. negative), b in {1,5,53,64,192,224}",
      ok, f"{cnt} integers")
negative("B1n plain floor(p/Q) used as an upper division is not an upper bound",
         any(Fr(fdiv(p, 2**8)) < Fr(p, 2**8) for p in range(1, 600)))

def polymul_trunc(A, B, n):
    C = [0]*n
    for i, a in enumerate(A[:n]):
        if a == 0: continue
        for j, bb in enumerate(B[:n - i]):
            C[i + j] += a * bb
    return C

def lower_prod(Am, Bm, Q, n): return [fdiv(c, Q) for c in polymul_trunc(Am, Bm, n)]
def upper_prod(Ap, Bp, Q, n): return [cdiv_223(c, Q) for c in polymul_trunc(Ap, Bp, n)]

def rand_pos_poly(n, zero_prefix=0):
    return [Fr(0)]*zero_prefix + [Fr(random.randint(0, 10**6), random.randint(1, 10**6)) for _ in range(n - zero_prefix)]

def enclose(A, Q):
    return [math.floor(a*Q) for a in A], [math.ceil(a*Q) for a in A]

# B2 (2.22) single products, b in {4, 8, 192, 224}
ok = True; cnt = 0
for b in (4, 8, 192, 224):
    Q = 2**b
    for _ in range(60):
        n = random.randint(1, 14)
        A = rand_pos_poly(n); B = rand_pos_poly(n)
        Am, Ap = enclose(A, Q); Bm, Bp = enclose(B, Q)
        AB = polymul_trunc(A, B, n)
        lo = lower_prod(Am, Bm, Q, n); hi = upper_prod(Ap, Bp, Q, n)
        cnt += 1
        if not all(Fr(lo[k], Q) <= AB[k] <= Fr(hi[k], Q) and lo[k] >= 0 for k in range(n)): ok = False
check("B2 (2.22) single truncated products enclose the exact product, lower endpoints stay >= 0", ok, f"{cnt} products")

# B3 chain: P^40 (as in P_0^40 of (2.10)) by repeated (2.22) at b = 8 (rounding visible) and b = 224,
# plus a positive set-partition-like combination 40*P^39*R + 1560*P^38*S^2 (positive integer weights).
def pow_enc(Am, Ap, e, Q, n):
    Rm, Rp = [Q] + [0]*(n - 1), [Q] + [0]*(n - 1)   # the constant 1 at scale Q
    for _ in range(e):
        Rm = lower_prod(Rm, Am, Q, n); Rp = upper_prod(Rp, Ap, Q, n)
    return Rm, Rp
ok = True
for b in (8, 224):
    Q = 2**b
    for trial in range(3):
        n = 10
        P = [Fr(random.randint(1, 50), random.randint(50, 400)) for _ in range(n)]
        R_ = rand_pos_poly(n); S_ = rand_pos_poly(n)
        Pm, Pp = enclose(P, Q); Rm_, Rp_ = enclose(R_, Q); Sm_, Sp_ = enclose(S_, Q)
        P40m, P40p = pow_enc(Pm, Pp, 40, Q, n)
        exactP40 = [Fr(1)] + [Fr(0)]*(n - 1)
        for _ in range(40): exactP40 = polymul_trunc(exactP40, P, n)
        if not all(Fr(P40m[k], Q) <= exactP40[k] <= Fr(P40p[k], Q) for k in range(n)): ok = False
        P39m, P39p = pow_enc(Pm, Pp, 39, Q, n); P38m, P38p = pow_enc(Pm, Pp, 38, Q, n)
        Tm = [40*x + 1560*y for x, y in zip(lower_prod(P39m, Rm_, Q, n), lower_prod(lower_prod(P38m, Sm_, Q, n), Sm_, Q, n))]
        Tp = [40*x + 1560*y for x, y in zip(upper_prod(P39p, Rp_, Q, n), upper_prod(upper_prod(P38p, Sp_, Q, n), Sp_, Q, n))]
        e39 = [Fr(1)] + [Fr(0)]*(n-1)
        for _ in range(39): e39 = polymul_trunc(e39, P, n)
        e38 = [Fr(1)] + [Fr(0)]*(n-1)
        for _ in range(38): e38 = polymul_trunc(e38, P, n)
        ex = [40*x + 1560*y for x, y in zip(polymul_trunc(e39, R_, n), polymul_trunc(polymul_trunc(e38, S_, n), S_, n))]
        if not all(Fr(Tm[k], Q) <= ex[k] <= Fr(Tp[k], Q) for k in range(n)): ok = False
        if b == 8 and trial == 0:
            w = max(Fr(P40p[k] - P40m[k], Q) / exactP40[k] for k in range(n) if exactP40[k] > 0)
check("B3 chained (2.22): P^40 and 40P^39R+1560P^38S^2 enclosed exactly at b = 8 and b = 224", ok,
      f"b=8 max relative width of P^40 enclosure {float(w):.3f}")

# negative controls for (2.22)
def find_violation(lower_fn, upper_fn, use_neg=False, swap=False, b=4, trials=400):
    Q = 2**b
    for _ in range(trials):
        n = random.randint(2, 8)
        A = rand_pos_poly(n); B = rand_pos_poly(n)
        Am, Ap = enclose(A, Q); Bm, Bp = enclose(B, Q)
        if use_neg:
            # legal-looking lower endpoints (still <= A) but negative
            Am = [x - random.randint(1, 3)*Q for x in Am]; Bm = [x - random.randint(1, 3)*Q for x in Bm]
        if swap: Am, Bm = Ap, Bp
        AB = polymul_trunc(A, B, n)
        lo = lower_fn(Am, Bm, Q, n); hi = upper_fn(Ap, Bp, Q, n)
        if any(not (Fr(lo[k], Q) <= AB[k] <= Fr(hi[k], Q)) for k in range(n)): return True
    return False
negative("B4n ceil in the lower product (2.22) is caught",
         find_violation(lambda a, b_, Q, n: [cdiv_223(c, Q) for c in polymul_trunc(a, b_, n)], upper_prod))
negative("B5n floor in the upper product (2.22) is caught",
         find_violation(lower_prod, lambda a, b_, Q, n: [fdiv(c, Q) for c in polymul_trunc(a, b_, n)]))
negative("B6n negative lower endpoints (violating 0 <= A-/Q) are caught", find_violation(lower_prod, upper_prod, use_neg=True))
negative("B7n upper endpoints used in the lower product are caught", find_violation(lower_prod, upper_prod, swap=True))

# B8 arb 160-bit coordinate enclosures -> 224-bit fixed point -> K^5 mod X^n ; compare with independent 400-bit arb
ctx.prec = 160
nK = 24; Q = 2**224
Kballs = [arb(-j)/7 for j in range(nK)]
Kballs = [x.exp() / (1 + j) for j, x in enumerate(Kballs)]
def arb_endpoints(x):
    """exact rational endpoints of an arb ball (dyadic mid +- rad)."""
    mid = x.mid(); rad = x.rad()
    mm, me = mid.man_exp(); rm, re_ = rad.man_exp()
    midF = Fr(int(mm)) * (Fr(2)**int(me)); radF = Fr(int(rm)) * (Fr(2)**int(re_))
    return midF - radF, midF + radF
Km, Kp = [], []
for x in Kballs:
    l, h = arb_endpoints(x)
    Km.append(max(0, math.floor(l * Q))); Kp.append(math.ceil(h * Q))
K5m, K5p = pow_enc(Km, Kp, 5, Q, nK)
ctx.prec = 400
Kb400 = [(arb(-j)/7).exp() / (1 + j) for j in range(nK)]
ex5 = [arb(1)] + [arb(0)]*(nK - 1)
for _ in range(5):
    new = [arb(0)]*nK
    for i in range(nK):
        for j in range(nK - i): new[i + j] += ex5[i] * Kb400[j]
    ex5 = new
ok = True
for k in range(nK):
    l, h = arb_endpoints(ex5[k])
    if not (Fr(K5m[k], Q) <= l and h <= Fr(K5p[k], Q)): ok = False
ctx.prec = 160
check("B8 160-bit arb coordinates -> 224-bit floor/ceil -> K^5 (2.22) encloses the 400-bit arb product (certain)", ok)

# B9 zero-prefix removal
ok = True; cntz = 0
for _ in range(300):
    n = random.randint(3, 16); Qz = 2**random.choice([4, 8, 192])
    vA = random.randint(0, n); vB = random.randint(0, n)
    A = [Fr(0)]*vA + rand_pos_poly(random.randint(1, n)); B = [Fr(0)]*vB + rand_pos_poly(random.randint(1, n))
    Am, Ap = enclose(A, Qz); Bm, Bp = enclose(B, Qz)
    direct_m = lower_prod(Am, Bm, Qz, n); direct_p = upper_prod(Ap, Bp, Qz, n)
    if vA + vB < n:
        m2 = n - vA - vB
        rm = lower_prod(Am[vA:], Bm[vB:], Qz, m2); rp = upper_prod(Ap[vA:], Bp[vB:], Qz, m2)
        via_m = [0]*(vA + vB) + rm; via_p = [0]*(vA + vB) + rp
    else:
        via_m = [0]*n; via_p = [0]*n
    cntz += 1
    if via_m != direct_m or via_p != direct_p: ok = False
check("B9 zero-prefix removal gives exactly the same (2.22) result (incl. vA+vB >= n -> 0)", ok, f"{cntz} cases")
# negative: forget to restore X^{vA+vB}
A = [Fr(0), Fr(0), Fr(3, 7), Fr(1, 3)]; B = [Fr(0), Fr(5, 11), Fr(2, 9), Fr(1)]
Am, Ap = enclose(A, 16); Bm, Bp = enclose(B, 16)
wrong = lower_prod(Am[2:], Bm[1:], 16, 3) + [0]
negative("B9n prefix removed but X^(vA+vB) not restored is caught", wrong != lower_prod(Am, Bm, 16, 4))

# B10 (2.24)
ok = True
for _ in range(200):
    n = random.randint(1, 40)
    I = [random.randint(-10**9, 10**9) for _ in range(n)]; Kc = [random.randint(-10**9, 10**9) for _ in range(n)]
    rev = [I[n - 1 - r] for r in range(n)]
    prod = polymul_trunc(rev, Kc, n)
    for j in range(n):
        if sum(I[r] * Kc[r - j] for r in range(j, n)) != prod[n - 1 - j]: ok = False
check("B10 (2.24) reversed correlation identity, 200 random signed integer cases, all j", ok)
n = 9; I = [random.randint(1, 99) for _ in range(n)]; Kc = [random.randint(1, 99) for _ in range(n)]
prod = polymul_trunc(I, Kc, n)
negative("B10n without the reversal of I the identity fails",
         any(sum(I[r]*Kc[r-j] for r in range(j, n)) != prod[n-1-j] for j in range(n)))

# B11 (2.25) + outward conversion "by one predecessor or successor after binary scaling"
def convert_out(v, b):
    """v/2^b as an outward binary64 interval, following (2.25) and the pred/succ rule."""
    r = max(0, abs(v).bit_length() - 1000)      # "bounded integer prefix"
    vm = v >> r if r else v                    # floor(v/2^r) (Python >> is floor for negatives)
    vp = -((-v) >> r) if r else v              # ceil(v/2^r)
    lo = pred(math.ldexp(float(vm), r - b)); hi = succ(math.ldexp(float(vp), r - b))
    return lo, hi
def conv_oracle_ok(v, e):
    """int->float and ldexp agree with the exact RN oracle (machine hypothesis)."""
    f = float(v)
    return Fr(f) == Fr(rn(v)) and Fr(math.ldexp(f, e)) == Fr(rn(Fr(f) * Fr(2)**e))
ok = True; okm = True; cnt = 0
for b in (192, 224):
    for _ in range(4000):
        k = random.choice([1, 20, 53, 54, 60, 200, 900, 1023, 1100, 1150, 1200])   # no overflow: v/2^b < 2^1024
        v = random.randint(-2**k, 2**k)
        lo, hi = convert_out(v, b)
        cnt += 1
        if not (Fr(lo) <= Fr(v, 2**b) <= Fr(hi)): ok = False
        if abs(v).bit_length() <= 1000 and not conv_oracle_ok(v, -b): okm = False
check("B11 (2.25) floor/ceil prefix + outward conversion encloses v/2^b (b=192,224; |v| up to 2^1200, prefix rule used above 2^1000)", ok, f"{cnt} cases")
# general dyadic scaling incl. gradual underflow: x = v*2^e with e down to -1200
ok = True; cnt = 0; hits_sub = 0
for _ in range(20000):
    v = random.randint(1, 2**random.choice([10, 53, 54, 64, 120])) * random.choice([1, -1])
    e = random.randint(-1250, -900)
    x = Fr(v) * Fr(2)**e
    y = math.ldexp(float(v), e)
    if abs(Fr(y)) < Fr(2)**-1022: hits_sub += 1
    if not conv_oracle_ok(v, e): okm = False
    lo, hi = pred(y), succ(y)
    cnt += 1
    if not (Fr(lo) <= x <= Fr(hi)): ok = False
check("B12 outward step after scaling encloses v*2^e incl. gradual underflow (double rounding <= one subnormal ulp)",
      ok, f"{cnt} cases, {hits_sub} in the subnormal range")
check("B13 machine hypothesis: int->binary64 and ldexp are RN (exact oracle) on all B11/B12 cases", okm)
# negative controls
caught = False
for _ in range(2000):
    v = random.randint(2**60, 2**70) | 1
    if Fr(math.ldexp(float(v), -224)) > Fr(v, 2**224): caught = True; break
negative("B11n conversion without the outward predecessor step exceeds v/2^b for some v", caught)
caught = False
for _ in range(200000):
    v = random.randint(2**60, 2**64) | 1; e = random.randint(-1140, -1080)
    y = math.ldexp(pred(float(v)), e)    # outward step BEFORE scaling: wrong order
    if Fr(y) > Fr(v) * Fr(2)**e: caught = True; break
negative("B12n outward step taken before (not after) a subnormal scaling can exceed the exact value", caught)
negative("B11n' floor in place of ceil for v_+ in (2.25) is not an upper bound",
         Fr(((2**1100 + 12345) >> 100), 1) * Fr(2)**100 < 2**1100 + 12345)

# B14 four endpoint products, each rounded outward by pred/succ, then hull
def iv_mul(a, b):
    ps = [x*y for x in a for y in b]
    return min(pred(p) for p in ps), max(succ(p) for p in ps)
def rand_double():
    k = random.random()
    if k < 0.15: return math.ldexp(random.random(), random.randint(-1100, -1000)) * random.choice([1, -1])
    if k < 0.3: return math.ldexp(random.random(), random.randint(-560, -500)) * random.choice([1, -1])
    return math.ldexp(random.random(), random.randint(-60, 60)) * random.choice([1, -1])
ok = True; okm = True
for _ in range(20000):
    a = sorted([rand_double(), rand_double()]); b = sorted([rand_double(), rand_double()])
    lo, hi = iv_mul(a, b)
    exact = [Fr(x)*Fr(y) for x in a for y in b]
    for x in a:
        for y in b:
            if Fr(x*y) != Fr(rn(Fr(x)*Fr(y))): okm = False
    if not (Fr(lo) <= min(exact) and max(exact) <= Fr(hi)): ok = False
check("B14 hull of the four outward-rounded endpoint products encloses the exact interval product (incl. underflow)", ok)
check("B15 machine hypothesis: binary64 products are RN incl. gradual underflow (exact oracle), 80000 products", okm)
caught = False
for _ in range(5000):
    a = sorted([rand_double(), rand_double()]); b = sorted([rand_double(), rand_double()])
    ps = [x*y for x in a for y in b]
    if Fr(min(ps)) > min(Fr(x)*Fr(y) for x in a for y in b): caught = True; break
negative("B14n endpoint products without the outward step are caught", caught)

# ================================================================== C. binary64 reductions (2.26) in action
print("\n--- C. Final reductions: s = fl(sum x), t = fl(sum |x|), endpoints pred(fl(s - fl(gamma_r t))) etc. ---")
def gamma_hat(r): return (r * uf) / (1.0 - r * uf)
def tree_sum(xs, kind, rng):
    xs = list(xs)
    if kind == "seq":
        s = xs[0]
        for x in xs[1:]: s = fadd(s, x)
        return s
    if kind == "pair":
        while len(xs) > 1:
            nxt = [fadd(xs[i], xs[i+1]) for i in range(0, len(xs) - 1, 2)]
            if len(xs) % 2: nxt.append(xs[-1])
            xs = nxt
        return xs[0]
    # random tree
    while len(xs) > 1:
        i = rng.randrange(len(xs) - 1)
        xs[i:i+2] = [fadd(xs[i], xs[i+1])]
    return xs[0]

STATS = {"cases": 0, "maxratio": Fr(0), "chain_ok": True, "encl_ok": True, "sub_g": 0}
def reduce_check(xs, kind_s, kind_t, rng, gfactor=None, rscale=1, outward=True):
    """returns True if the endpoints enclose the exact sum. gfactor / rscale / outward: negative-control knobs."""
    r = len(xs)
    s = tree_sum(xs, kind_s, rng); t = tree_sum([abs(x) for x in xs], kind_t, rng)
    rr = max(1, r // rscale)
    gh = gamma_hat(rr)
    g = fmul(gh, t)
    if gfactor is not None: g = g * gfactor
    a = fadd(s, -g); c = fadd(s, g)
    lo = pred(a) if outward else a
    hi = succ(c) if outward else c
    S = sum(Fr(x) for x in xs); T = sum(abs(Fr(x)) for x in xs)
    enc = Fr(lo) <= S <= Fr(hi)
    if gfactor is None and rscale == 1 and outward:
        STATS["cases"] += 1
        # the chain of the proof, each link exactly
        l1 = abs(Fr(s) - S) <= gam(r - 1) * T
        l2 = Fr(t) >= (1 - gam(r - 1)) * T
        l3 = Fr(g) >= (1 - U)**2 * gam(r) * Fr(t) - HALF_TINY
        l4 = Fr(lo) <= Fr(s) - Fr(g) - HALF_TINY and Fr(hi) >= Fr(s) + Fr(g) + HALF_TINY
        if abs(Fr(gh) * Fr(t)) < Fr(2)**-1022 and gh * t != 0: STATS["sub_g"] += 1
        if not (l1 and l2 and l3 and l4): STATS["chain_ok"] = False
        if T > 0 and r > 1: STATS["maxratio"] = max(STATS["maxratio"], abs(Fr(s) - S) / (gam(r - 1) * T))
        if not enc: STATS["encl_ok"] = False
    return enc

rng = random.Random(7)
def fam_random(r):
    return [math.ldexp(rng.random(), rng.randint(-40, 40)) * rng.choice([1, -1]) for _ in range(r)]
def fam_cancel(r):
    base = [math.ldexp(rng.random(), rng.randint(0, 30)) for _ in range(r // 2)]
    xs = base + [-x * (1 + rng.choice([0, uf, -uf, 3*uf])) for x in base]
    xs = [float(x) for x in xs] + [rng.random() * 1e-9]
    rng.shuffle(xs); return xs
def fam_adv_up(r):  return [1.0] + [uf] * (r - 1)           # each u is lost: s = 1, S = 1 + (r-1)u
def fam_adv_dn(r):  return [1.0] + [-uf / 2] * (r - 1)      # ties-to-even keeps 1
def fam_near_uf(r): return [math.ldexp(rng.random(), rng.randint(-1010, -990)) * rng.choice([1, -1]) for _ in range(r)]
def fam_sub(r):     return [math.ldexp(rng.random(), rng.randint(-1074, -1023)) * rng.choice([1, -1]) for _ in range(r)]
def fam_mixed(r):
    return [math.ldexp(rng.random(), rng.choice([rng.randint(-1074, -1000), rng.randint(-60, 60)])) * rng.choice([1, -1])
            for _ in range(r)]
fams = [("random", fam_random), ("cancel", fam_cancel), ("adv_up", fam_adv_up), ("adv_dn", fam_adv_dn),
        ("near_underflow", fam_near_uf), ("subnormal", fam_sub), ("mixed", fam_mixed)]
for name, f in fams:
    for r in (1, 2, 3, 5, 17, 64, 257, 1000, 3000):
        for kind_s, kind_t in (("seq", "seq"), ("pair", "seq"), ("rand", "rand"), ("seq", "pair")):
            for _ in range(2 if r >= 1000 else 6):
                xs = f(r)
                if len(xs) == 0: continue
                reduce_check(xs, kind_s, kind_t, rng)
# one reduction of the maximal stated length r = 98264, sequential and pairwise
for f in (fam_random, fam_adv_up, fam_cancel):
    xs = f(RMAX)[:RMAX]
    reduce_check(xs, "seq", "seq", rng); reduce_check(xs, "pair", "pair", rng)
check("C1 endpoints enclose the exact signed sum on every instance", STATS["encl_ok"], f"{STATS['cases']} reductions, "
      f"r up to {RMAX}, 4 tree shapes, 7 families")
check("C2 each link of the proof holds exactly on every instance: |s-S|<=g_{r-1}T, t>=(1-g_{r-1})T, "
      "fl(g t)>=(1-u)^2 g_r t-2^-1075, outward step absorbs >=2^-1075", STATS["chain_ok"],
      f"max |s-S|/(gamma_(r-1) T) = {float(STATS['maxratio']):.4f}; {STATS['sub_g']} cases with subnormal gamma*t")
check("C3 machine hypothesis: every binary64 + and * in Section C equals the exact RN oracle",
      MACH["bad"] == 0, f"{MACH['ops']} operations")
# negative controls
negative("C4n correction fl(gamma_r t)/4 fails on the adversarial sum [1, u x 999] (seq)",
         not reduce_check(fam_adv_up(1000), "seq", "seq", rng, gfactor=0.25))
negative("C5n gamma for r/2 terms instead of r fails on the adversarial sum [1, u x 2999]",
         not reduce_check(fam_adv_up(3000), "seq", "seq", rng, rscale=2))
negative("C6n no correction and no outward step (plain fl sum) fails on [1, u x 999]",
         not reduce_check(fam_adv_up(1000), "seq", "seq", rng, gfactor=0.0, outward=False))
# how tight is the adversarial family relative to the bound?
xs = fam_adv_up(3000); s = tree_sum(xs, "seq", rng); S = sum(Fr(x) for x in xs); T = sum(abs(Fr(x)) for x in xs)
print(f"      note: on [1, u x 2999] the true error is {float((S - Fr(s))/(gam(2999)*T)):.4f} of gamma_(r-1) T")

# ================================================================== D. Lemma 2.1 series tails (used "as in Lemma 2.1")
print("\n--- D. Lemma 2.1 tail bounds (referenced by Sec. 2.3) ---")
ctx.prec = 300
ok = True; cnt = 0; negcaught = False
for vnum in (1, 7, 50, 99, 100):
    v = Fr(vnum, 300)            # v in (0, 1/3]
    va = arb(vnum) / 300
    y = (1 + va) / (1 - va)
    for Mser in range(1, 16):
        part = sum(2 * va**(2*r + 1) / (2*r + 1) for r in range(Mser))
        tail = y.log() - part
        bnd = 2 * va**(2*Mser + 1) / ((2*Mser + 1) * (1 - va**2))
        cnt += 1
        if not (tail > 0 and tail < bnd): ok = False          # certain comparisons
        if (tail > bnd / 2): negcaught = True
for vnum in (1, 37, 100, 150):
    va = arb(vnum) / 300           # v in (0, 1/2]
    for Mser in range(1, 16):
        part = sum(va**r / math.factorial(r) for r in range(Mser + 1))
        tail = va.exp() - part
        bnd = va**(Mser + 1) / (math.factorial(Mser + 1) * (1 - va / (Mser + 2)))
        cnt += 1
        if not (tail > 0 and tail < bnd): ok = False
check("D1 Lemma 2.1 log and exp tail bounds hold (certain arb comparisons at 300 bits)", ok, f"{cnt} (v, M) pairs")
negative("D1n halved log tail bound is violated somewhere", negcaught)
ctx.prec = 160

# ================================================================== E. (2.3) renewal majorant, interval-carried
print("\n--- E. Secondary: renewal majorant (2.3), interval-carried as on p. 12 ---")
TAIL = Fr(1, 10**40)
def renewal_interval(M, jmax, prec=160, window=None):
    """Sliding sum initialised to [M,M], divide outwards by j, add the new interval, subtract the departing one.
    Returns list of arb intervals R_j (j < jmax) and the switch index j* (or None)."""
    old = ctx.prec; ctx.prec = prec
    R = [arb(1)] * (M + 1)          # R_0..R_M = 1
    S = arb(M)                      # sum_{a=1}^{M} R_a = window for j = M+1 (a = j-M .. j-1)
    if window is not None: S = arb(window)
    tail_lo = arb(1) / arb(10)**40
    jstar = None; minlow = None
    for j in range(M + 1, jmax):
        Rj = S / j
        if not (Rj.lower() > 0): ctx.prec = old; return R, jstar, "nonpositive"
        R.append(Rj)
        if Rj < tail_lo:            # certain: upper(Rj) < lower(1e-40)
            jstar = j; break
        if window is None: S = S + Rj - R[j - M]
        else: S = S + Rj - R[j - window] if j - window >= 0 else S + Rj
    ctx.prec = old
    return R, jstar, "ok"

def renewal_exact(M, jmax):
    R = [Fr(1)] * (M + 1)
    for j in range(M + 1, jmax):
        R.append(sum(R[j - M:j]) / j)
    return R

def rho_upper_le2(u_fr):
    """rigorous arb ball for rho(u), 1 <= u <= 2: 1 - log u."""
    return 1 - (arb(u_fr.numerator) / u_fr.denominator).log()

# E1 exact rationals vs the interval scheme, and R_j >= rho(j/M) on (M, 2M] for every M = 2..63
ok_in = True; ok_rho = True; cnt_rho = 0; cnt_in = 0
for M in range(2, 64):
    jm = min(6*M, 400)
    Rex = renewal_exact(M, jm)
    Rint, js, st = renewal_interval(M, jm)
    for j in range(len(Rint)):
        l, h = arb_endpoints(Rint[j]); cnt_in += 1
        if not (l <= Rex[j] <= h): ok_in = False
    for j in range(M, 2*M + 1):
        rho = rho_upper_le2(Fr(j, M))
        l, h = arb_endpoints(Rint[j]); cnt_rho += 1
        if not (Rint[j] > rho or (j == M and Rex[j] == 1)): ok_rho = False
check("E1 interval scheme of p. 12 contains the exact rational R_j, M = 2..63, j < min(6M,400)", ok_in, f"{cnt_in} values")
check("E2 R_j > rho(j/M) certain on M <= j <= 2M for every M = 2..63 (rho = 1 - log u)", ok_rho, f"{cnt_rho} values")
# E3 run the interval scheme to the 1e-40 switch for every M = 2..63 (renewal is the branch for M < 64)
ok = True; js_list = {}
for M in range(2, 64):
    R, js, st = renewal_interval(M, 98304)
    if st != "ok" or js is None: ok = False
    js_list[M] = js
check("E3 interval scheme reaches the 1e-40 switch with positive lower endpoints for every M = 2..63", ok,
      "j* = " + ", ".join(f"{m}:{js_list[m]}" for m in (2, 3, 6, 12, 25, 50, 63)))
# E4 large M (the fallback if a delay acceptance test fails): positivity over all j < N = 98304 and R_j > rho on (M,2M]
ok = True; info = []
for M in (64, 93, 300, 1000, 4096, 24270):
    R, js, st = renewal_interval(M, 98304)
    if st != "ok": ok = False
    for j in list(range(M, min(2*M, len(R) - 1) + 1, max(1, M // 50))):
        if not (j == M or R[j] > rho_upper_le2(Fr(j, M))): ok = False
    info.append(f"M={M}: j*={js}, last R={R[-1].mid().str(3)}")
check("E4 large-M renewal (M in {64,93,300,1000,4096,24270}): positive lower endpoints for all j < 98304 "
      "(or until switch); R_j > rho(j/M) on sampled (M,2M]", ok, "; ".join(info))
# E5 beyond u = 2: rigorous rho on (2,3] via rho(u) = 1 - log u + int_2^u log(t-1)/t dt (certain), M in {3,6,12,25,50}
from flint import acb
def rho_23(u_fr):
    ua = acb(u_fr.numerator) / u_fr.denominator
    I = acb.integral(lambda t, _: (t - 1).log() / t, acb(2), ua)
    return (1 - ua.log() + I).real
ok = True; cnt = 0
for M in (3, 6, 12, 25, 50):
    Rint, js, st = renewal_interval(M, 3*M + 1)
    for j in range(2*M + 1, 3*M + 1):
        cnt += 1
        if not (Rint[j] > rho_23(Fr(j, M))): ok = False
check("E5 R_j > rho(j/M) certain on 2M < j <= 3M for M in {3,6,12,25,50} (acb.integral)", ok, f"{cnt} values")
# self-test of the [2,3] closed form against the delay equation in integrated form:
# rho(5/2) = rho(2) - int_2^{5/2} rho(t-1)/t dt with rho(t-1) = 1 - log(t-1) (independent integrand)
alt = (1 - arb(2).log()) - acb.integral(lambda t, _: (1 - (t - 1).log()) / t, acb(2), acb(5)/2).real
check("E6 [2,3] closed form of rho agrees with the integrated delay equation at u = 5/2 (balls overlap, width < 1e-30)",
      rho_23(Fr(5, 2)).overlaps(alt) and rho_23(Fr(5, 2)).rad() < 1e-30, "rho(5/2) = " + rho_23(Fr(5, 2)).str(15, radius=False) + ", rad < 1e-30")
# negative: shorter window (a = j-M+1 .. j-1) is not a majorant
Rbad = [Fr(1)] * 13
for j in range(13, 30): Rbad.append(sum(Rbad[j - 11:j]) / j)
negative("E7n window of M-1 terms (M=12) gives R_13 < rho(13/12): caught",
         arb(Rbad[13].numerator) / Rbad[13].denominator < rho_upper_le2(Fr(13, 12)))

# ================================================================== summary
ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("\n" + "=" * 100)
print(f"checks: {NCHK}, failures: {NFAIL}; negative controls: {NNEG}, caught: {NNEGOK}")
print(f"wall {time.time() - T0:.1f} s, peak RSS {ru/1024:.0f} MB")
print("VERDICT:", "all positive checks pass and all negative controls are caught" if NFAIL == 0 and NNEG == NNEGOK
      else "SEE FAILURES ABOVE")
