#!/usr/bin/python3
"""Rung 182 (GPT-6 Astra / R. Sharifi, bundle [M]): exact re-check of the printed rational arithmetic.

Run:  /usr/bin/python3 -I code/sharifi182_arith.py
Exit status 0 iff every check PASSes.  Report: notes/arith-182-report.md.

Source: "A fixed-profile proof for prime gaps of at most 182", first paper of the expository bundle
prime_gaps_182_expository_bundle.pdf (SHA-256 5362e977880af92a73a79b411a9c66daf0b93af4ec0ed6bec320090386f4b881).
Page numbers below are printed pages of [M] (= PDF pages 1-52).  Every input is transcribed by hand from
`pdftotext -layout` / `-raw` output; nothing from the authors' programs is used or run.

What this checks: only arithmetic that follows from numbers PRINTED in the PDF.  It does not check any
integral, any source bound A_j, M_j, b, or the cap enclosure mu-.  Those are Claimed inputs.

Conventions.  Section 10 tables print "upper bounds in units of 1e-6, rounded upward" with 9 decimals, so a
printed entry p stands for a true (exact rational) value v with p - u < v <= p, u = 1e-9 (in units of 1e-6).
"Consistent" below means: some choice of true values inside these rounding intervals reproduces every
printed number.  Square roots are enclosed by exact integer square roots (rigorous rational bounds), and
cross-checked with python-flint arb balls when available.
"""
from fractions import Fraction as Fr
from math import isqrt, ceil, floor
import sys

FAILS = []
NPASS = 0


def check(name, cond, detail=""):
    global NPASS
    if cond:
        NPASS += 1
        print(f"PASS  {name}" + (f"   [{detail}]" if detail else ""))
    else:
        FAILS.append(name)
        print(f"FAIL  {name}" + (f"   [{detail}]" if detail else ""))


def info(msg):
    print(f"      {msg}")


def D(s):
    """Exact rational from a printed decimal string."""
    return Fr(s)


def dec(x, n=15):
    """Decimal string of a Fraction to n places (truncated toward -inf), for display only."""
    x = Fr(x)
    sgn = "-" if x < 0 else ""
    x = abs(x)
    q = floor(x * 10 ** n)
    s = str(q).rjust(n + 1, "0")
    return f"{sgn}{s[:-n]}.{s[-n:]}"


def ceil_to(x, places):
    """Round x upward to a multiple of 10^-places."""
    s = 10 ** places
    return Fr(ceil(Fr(x) * s), s)


SQ = 10 ** 40  # scale for integer square roots


def sqrt_hi(x):
    """Rigorous upper bound for sqrt(x), x >= 0 rational."""
    x = Fr(x)
    n = x.numerator * x.denominator * SQ * SQ
    r = isqrt(n)
    if r * r < n:
        r += 1
    return Fr(r, x.denominator * SQ)


def sqrt_lo(x):
    """Rigorous lower bound: isqrt(n*d*SQ^2)/(d*SQ) <= sqrt(n/d)."""
    x = Fr(x)
    return Fr(isqrt(x.numerator * x.denominator * SQ * SQ), x.denominator * SQ)


try:
    import flint
    flint.ctx.prec = 200
    HAVE_FLINT = True
except Exception:  # pragma: no cover
    HAVE_FLINT = False


def arb_sqrt_interval(x):
    """arb enclosure of sqrt(x) as (lo, hi) Fractions, or None."""
    if not HAVE_FLINT:
        return None
    x = Fr(x)
    a = flint.arb(flint.fmpq(x.numerator, x.denominator)).sqrt()
    # arb ball -> exact rational endpoints mid -/+ rad
    m = a.mid().man_exp()
    r = a.rad().man_exp()
    mid = Fr(int(m[0])) * (Fr(2) ** int(m[1]))
    rad = Fr(int(r[0])) * (Fr(2) ** int(r[1]))
    return (mid - rad, mid + rad)


print("=" * 100)
print("Inputs (transcribed; page = printed page of [M])")
print("=" * 100)

# ---- (7.1), p. 29 -------------------------------------------------------------------------------
rho_s = Fr(2624989, 10 ** 7)          # p.29 (7.1): rho* = 2624989/10000000
rho = Fr(262499, 10 ** 6)             # p.29 (7.1): rho  = 262499/1000000
S = Fr(1379373467, 1312494500)        # p.29 (7.1)
# ---- (3.5), p. 12 -------------------------------------------------------------------------------
a5 = D(".41361")                      # p.12 (3.5): a
I0 = D(".34941")                      # p.12 (3.5): I0
c3 = D(".41364")                      # p.12 (3.5): c
tau = Fr(1, 10 ** 10)                 # p.12 (3.5): tau = 10^-10
# ---- (4.3), p. 21; (5.7), p. 26; (6.8), p. 28 ----------------------------------------------------
kbar = Fr(46653544162031, 500000000000000000)   # p.21 (4.3): kappa-bar
K_up = D("2.194")                     # p.26 (5.7): 0 <= K <= 2.194
ell = Fr(6308693370963335, 576460752303423488)  # p.28 (6.8): ell = 6308693370963335/576460752303423488
# ---- (8.3), p. 33 -------------------------------------------------------------------------------
# p.33 (8.3): "eps_h = kappa-bar (1/.0108 - 1) 2.194,  delta_op = 4 rho* eps_h,  gamma_op = 1 - delta_op,
#              Gamma = 4 rho* (1 + eps_h)."   (the bar is over kappa, as in d_h = kappa-bar(1/ell - 1), p.28)
ell_lo = D(".0108")
# p.33: "For orientation, eps_h ~ .01875045, delta_op ~ .01968789, and gamma_op ~ .98031211 > 0."
eps_h_print, dop_print, gop_print = D(".01875045"), D(".01968789"), D(".98031211")
# p.34 (Sec 8.3): t = 11/10 > gamma_op
t = Fr(11, 10)
# ---- (7.5), (7.6), p. 32 ------------------------------------------------------------------------
I_den = 664613997892457936451903530140172288
I_lo = Fr(9900316613656518642800593, I_den)     # p.32 (7.5)
I_hi = Fr(9900316889124784142456785, I_den)     # p.32 (7.5)
mu_lo = Fr(9968877639291, 36028797018963968)    # p.32 (7.6)
mu_lo_dec = D(".0002766919371")                 # p.32 (7.6): mu- > .0002766919371 (also abstract p.1, p.5)
# ---- Section 10 tables, pp. 39-40 (units 1e-6, rounded upward) ------------------------------------
# p.40 outer table: (name, count, sum A_j, sum M_j, Loss)
OUTER = [
    ("G1: low", 8, "0.749574898", "14.579171091", "6.699042427"),
    ("G1: rank two", 14, "0.224037660", "1.558976746", "1.177680761"),
    ("G1: high", 1, "0.000019087", "0.000031473", "0.000051304"),
    ("G2: low", 22, "3.755008125", "40.782076795", "25.186856792"),
    ("G2: rank two", 14, "23.449034139", "151.904930860", "121.397753113"),
    ("G2: high", 1, "0.779494639", "5.803481072", "4.347133100"),
]
# p.40 inner table: (name, count, contribution to b)
INNER = [
    ("G3: low", 8, "0.007585797"),
    ("G4: low", 21, "0.017382180"),
    ("G5: low", 8, "0.413045470"),
    ("G6: low", 20, "2.684023505"),
    ("C: low", 7, "9.828292827"),
    ("All rank-two and high terms", 73, "13.752470897"),
]
b_101 = D(".000026702801")            # p.40 (10.1): b < .000026702801
# p.40 four-term table ("Upper bound in units of 10^-6")
T_b = D("26.702800674")
T_Gbt = D("25.966859017")
T_cross = D("155.342695198")
T_mass = D("3.465822296")
Lbar = Fr(105739089, 500000000000)    # p.40 (10.2)
Lbar_dec = D(".000211478178")         # p.40 (10.2) (also abstract p.1, p.5)
marg_frac = Fr(573626291549967919851, 8796093022208000000000000)  # p.40 (10.3)
marg_dec = D(".000065213759")         # p.40 (10.3) (also abstract p.1, p.5)
# p.36 Sec 9.1 family table: family -> (low, rank two, high)
FAMILY = {"G1": (8, 14, 1), "G2": (22, 14, 1), "G3": (8, 14, 1), "G4": (21, 12, 1),
          "G5": (8, 14, 1), "G6": (20, 13, 1), "C": (7, 15, 1)}
# ---- Sec 13.3, p. 45 ----------------------------------------------------------------------------
kcvx = Fr(11696, 125000000)           # p.45: kappa_cvx := 11696/125000000 = .000093568
kcvx_dec = D(".000093568")
lean_xi_bound = Fr(32, 10 ** 6)       # p.45: 0 < 4 rho* xi_add < 32/10^6
lean_margin = Fr(33, 10 ** 6)         # p.45: (rho* J_cvx(PF) - I(PF))/I(F) > 33/10^6
# ---- Sec 3.7, pp. 16-18 -------------------------------------------------------------------------
T1 = Fr(1262625033, 1312494500)       # p.16: T1
B0 = 1 / (2 * rho)                    # p.16: B0 = 1/(2 rho)
eps_r = Fr(1, 10 ** 7)                # p.16: eps_r = 10^-7
U_n = T1 + eps_r / rho                # p.16: U_n = T1 + eps_r/rho
b13 = Fr(37058221276498005595947498293, 40868109574262446536646110000)   # p.16 (3.15)
b14 = Fr(260700046797786617627841743303, 286076767019837125756522770000)  # p.16 (3.16)
xi13, xi14 = U_n - b13, U_n - b14     # p.16 (3.15)-(3.16)
om_s = Fr(21, 5000)                   # p.17: omega_s
de_s = Fr(2279, 100000)               # p.17: delta_s
xi_s_print = Fr(22790, 262499)        # p.17: xi_s = delta_s/rho = 22790/262499
c_s = B0 - T1                         # p.17: c_s = B0 - T1
sigma0 = D(".100001")                 # p.17 (3.17)
S_C = B0 - b14 - eps_r / rho_s        # p.17 (3.17)
om_C = (rho * (S_C + T1) - Fr(1, 2) + eps_r) / 2           # p.17 (3.17)
de_C = (1 - 4 * sigma0) / 16 - Fr(7, 2) * om_C - eps_r     # p.17 (3.17)
xi_C = de_C / rho                     # p.17 (3.17)
a_C, b_C = B0 - T1, B0 - S_C          # p.17

print(f"rho* = {rho_s}, rho = {rho}, S = {S}, T1 = {T1}")
print(f"kappa-bar = {kbar}, ell = {ell} ~ {dec(ell, 12)}")

print()
print("=" * 100)
print("(a) (8.3), p. 33")
print("=" * 100)
check("(6.8) .0108 <= ell <= .0112", Fr(108, 10000) <= ell <= Fr(112, 10000), f"ell ~ {dec(ell, 12)}")
eps_h = kbar * (1 / ell_lo - 1) * K_up
d_h = kbar * (1 / ell - 1)
delta_op = 4 * rho_s * eps_h
gamma_op = 1 - delta_op
Gamma = 4 * rho_s * (1 + eps_h)
info(f"eps_h    = {eps_h}  ~ {dec(eps_h, 15)}")
info(f"delta_op = {delta_op}  ~ {dec(delta_op, 15)}")
info(f"gamma_op = {gamma_op}  ~ {dec(gamma_op, 15)}")
info(f"Gamma    = {Gamma}  ~ {dec(Gamma, 15)}")
info(f"t - gamma_op = {t - gamma_op}  ~ {dec(t - gamma_op, 15)}")
info(f"d_h = kappa-bar(1/ell - 1) ~ {dec(d_h, 15)};  d_h * 2.194 ~ {dec(d_h * K_up, 15)}")
check("eps_h ~ .01875045 (printed, nearest 8th decimal)", abs(eps_h - eps_h_print) <= Fr(5, 10 ** 9),
      f"exact {dec(eps_h, 12)}")
check("delta_op ~ .01968789 (printed, nearest 8th decimal)", abs(delta_op - dop_print) <= Fr(5, 10 ** 9),
      f"exact {dec(delta_op, 12)}")
check("gamma_op ~ .98031211 (printed, nearest 8th decimal)", abs(gamma_op - gop_print) <= Fr(5, 10 ** 9),
      f"exact {dec(gamma_op, 12)}")
check("gamma_op > 0 (p.33)", gamma_op > 0)
check("t = 11/10 > gamma_op (p.34)", t > gamma_op)
check("eps_h >= d_h * 2.194 (so -eps_h <= a_H, a given K <= 2.194 and ell >= .0108)",
      eps_h >= d_h * K_up, f"slack {dec(eps_h - d_h * K_up, 12)}")
check("eps_h <= 1 (needed for |a_H| <= eps_h + (1-eps_h)1_H1, p.35)", eps_h <= 1)
check("Gamma = 4 rho* + delta_op (identity of the printed definitions)", Gamma == 4 * rho_s + delta_op)

print()
print("=" * 100)
print("(b) Section 10 tables, pp. 39-40 (units 1e-6; printed p means p - u < v <= p, u = 1e-9)")
print("=" * 100)
u = Fr(1, 10 ** 9)
n_out = sum(r[1] for r in OUTER)
n_in = sum(r[1] for r in INNER)
check("outer component count = 60 (p.36, p.40)", n_out == 60, f"{n_out}")
check("inner component count = 137 (p.36, p.40)", n_in == 137, f"{n_in}")
check("total 197", n_out + n_in == 197)
fam_ok = (all(FAMILY[g] == (OUTER[3 * k][1], OUTER[3 * k + 1][1], OUTER[3 * k + 2][1]) for k, g in enumerate(["G1", "G2"]))
          and [FAMILY[g][0] for g in ["G3", "G4", "G5", "G6", "C"]] == [r[1] for r in INNER[:5]]
          and sum(FAMILY[g][1] + FAMILY[g][2] for g in ["G3", "G4", "G5", "G6", "C"]) == INNER[5][1])
check("Sec 10 counts agree with Sec 9.1 family table (p.36)", fam_ok)
low_in = sum(FAMILY[g][0] for g in ["G3", "G4", "G5", "G6", "C"])
r2_in = sum(FAMILY[g][1] for g in ["G3", "G4", "G5", "G6", "C"])
check("p.36: inner = 64 low + 68 rank-two + 5 high", (low_in, r2_in, 5) == (64, 68, 5), f"{low_in},{r2_in}")

# --- inner deletion b
in_vals = [D(r[2]) for r in INNER]
s_in = sum(in_vals)
info(f"sum of printed inner rows = {dec(s_in, 9)}; printed b = {dec(T_b, 9)}")
# true b lies in (s_in - 6u, s_in] and in (T_b - u, T_b]
check("inner rows sum consistent with printed b = 26.702800674 (rounding intervals intersect)",
      T_b > s_in - 6 * u and T_b - u < s_in, f"sum of rows {dec(s_in, 9)}")
check("(10.1) b < .000026702801 follows from printed b", T_b * Fr(1, 10 ** 6) < b_101)
b_lo, b_hi = max(T_b - u, s_in - 6 * u), T_b  # open at b_lo

# --- Gamma b / t
g_hi = Gamma * b_hi / t
g_lo = Gamma * b_lo / t
info(f"Gamma*b/t with b = printed 26.702800674: {dec(g_hi, 12)} -> rounded up {dec(ceil_to(g_hi, 9), 9)}")
info(f"Gamma*b/t over b in ({dec(b_lo, 9)}, {dec(b_hi, 9)}]: ({dec(g_lo, 12)}, {dec(g_hi, 12)}]")
check("Gamma b/t = 25.966859017 consistent with printed b and Gamma (8.3)",
      ceil_to(g_lo, 9) <= T_Gbt <= ceil_to(g_hi, 9) and T_Gbt > g_lo,
      f"ceil(Gamma*26.702800674/t) = {dec(ceil_to(g_hi, 9), 9)}")
check("Gamma b/t printed >= Gamma * (printed b) / t (valid upper bound from printed b)",
      T_Gbt >= g_hi, f"diff {dec(T_Gbt - g_hi, 12)}")

# --- (t - gamma_op) sum A
A_vals = [D(r[2]) for r in OUTER]
M_vals = [D(r[3]) for r in OUTER]
L_vals = [D(r[4]) for r in OUTER]
cnts = [r[1] for r in OUTER]
sA = sum(A_vals)
tg = t - gamma_op
m_hi, m_lo = tg * sA, tg * (sA - 6 * u)
info(f"sum A (printed rows) = {dec(sA, 9)};  (t-gamma_op)*sumA = {dec(m_hi, 12)} -> up {dec(ceil_to(m_hi, 9), 9)}")
check("(t-gamma_op) sum A_j = 3.465822296 consistent with printed sum A rows",
      ceil_to(m_lo, 9) <= T_mass <= ceil_to(m_hi, 9) and T_mass > m_lo,
      f"interval ({dec(m_lo, 12)}, {dec(m_hi, 12)}]")

# --- per-group Loss = 2 sum_j sqrt(A_j M_j) + (t - gamma_op) A_g ; per-j values not printed
#     lower: Loss_g >= (t-gamma_op) A_g + 2 sqrt(min over j ...) -- we use only Loss_g > (t-g)(A_g - u) - nothing
#     upper (Cauchy-Schwarz): sum_j sqrt(A_j M_j) <= sqrt(A_g M_g)
print("      per-group: Loss_g vs Cauchy-Schwarz ceiling 2 sqrt(A_g M_g) + (t-gamma_op) A_g (A_g, M_g printed upper)")
cross_lo_tot, cross_hi_tot = Fr(0), Fr(0)
for (name, n, _, _, _), A, M, L in zip(OUTER, A_vals, M_vals, L_vals):
    cs_hi = 2 * sqrt_hi(A * M) + tg * A
    ok = (L - u < cs_hi) and (L > tg * (A - u))
    cross_lo_tot += L - u - tg * A
    cross_hi_tot += L - tg * (A - u)
    if n == 1:
        # single component: Loss = 2 sqrt(AM) + (t-g)A exactly, with A in (A-u, A], M in (M-u, M]
        f_hi = 2 * sqrt_hi(A * M) + tg * A
        f_lo = 2 * sqrt_lo((A - u) * (M - u)) + tg * (A - u)
        ok1 = ceil_to(f_lo, 9) <= L <= ceil_to(f_hi, 9)
        arb = arb_sqrt_interval(A * M)
        extra = ""
        if arb is not None:
            extra = f"; arb sqrt(AM) in [{dec(arb[0], 15)},{dec(arb[1], 15)}], isqrt [{dec(sqrt_lo(A*M),15)},{dec(sqrt_hi(A*M),15)}]"
            ok1 = ok1 and arb[0] <= sqrt_hi(A * M) and arb[1] >= sqrt_lo(A * M)
        check(f"{name}: single component, Loss = 2 sqrt(AM)+(t-g)A reproduces {dec(L, 9)}", ok1,
              f"from rounding box: [{dec(ceil_to(f_lo, 9), 9)}, {dec(ceil_to(f_hi, 9), 9)}]; f(A,M printed) = {dec(f_hi, 12)}{extra}")
    else:
        check(f"{name}: (t-g)A_g < Loss_g <= 2 sqrt(A_g M_g)+(t-g)A_g (Cauchy-Schwarz)", ok,
              f"Loss {dec(L, 9)}, CS ceiling {dec(cs_hi, 9)}, ratio cross/CS = {float((L - tg*A)/(2*sqrt_hi(A*M))):.4f}")

sL = sum(L_vals)
info(f"sum of Loss column = {dec(sL, 9)}; printed cross + mass = {dec(T_cross + T_mass, 9)}")
check("Loss column total consistent with 155.342695198 + 3.465822296 (rounding intervals intersect)",
      (T_cross + T_mass) > sL - 6 * u and (T_cross + T_mass) - 2 * u < sL)
info(f"2 sum sqrt(A_j M_j) implied by Loss - (t-g)A rows: ({dec(cross_lo_tot, 9)}, {dec(cross_hi_tot, 9)})")
check("2 sum sqrt(A_j M_j) = 155.342695198 consistent with outer table rows",
      T_cross > cross_lo_tot and T_cross - u < cross_hi_tot)
cs_tot = sum(2 * sqrt_hi(A * M) for A, M in zip(A_vals, M_vals))
check("155.342695198 <= sum_g 2 sqrt(A_g M_g) (group Cauchy-Schwarz ceiling)", T_cross <= cs_tot,
      f"ceiling {dec(cs_tot, 9)}")
info("per-component A_j, M_j are NOT printed (p.39: 'full rational values, including individual source bins, are in the "
     "digital supplement'), so the 197-term sqrt sum itself cannot be recomputed from the PDF.")

# --- (10.2)
four = T_b + T_Gbt + T_cross + T_mass
info(f"sum of the four printed terms = {dec(four, 9)} (units 1e-6) ; L-bar = {dec(Lbar * 10**6, 9)}")
check("(10.2) L-bar = 105739089/500000000000 = .000211478178 exactly", Lbar == Lbar_dec)
check("(10.2) sum of four printed upper bounds <= L-bar", four * Fr(1, 10 ** 6) <= Lbar,
      f"slack {dec(Lbar * 10**6 - four, 9)}e-6")
check("(10.2) L-bar = sum of four terms rounded up at 1e-12 (and > true-sum lower end)",
      ceil_to(four * Fr(1, 10 ** 6), 12) == Lbar)

print()
print("=" * 100)
print("(c) (7.6), (10.3), Sec 13.3")
print("=" * 100)
check("(7.6) 36028797018963968 = 2^55", 36028797018963968 == 2 ** 55)
check("(7.6) mu- > .0002766919371", mu_lo > mu_lo_dec, f"mu- ~ {dec(mu_lo, 18)}")
check("(7.5) 0 < I- < I+ and both ~ 1.4896341e-11",
      0 < I_lo < I_hi and all(abs(x * 10 ** 11 - D("1.4896341")) < Fr(5, 10 ** 8) for x in (I_lo, I_hi)),
      f"I- ~ {float(I_lo):.10e}, I+ ~ {float(I_hi):.10e}")
diff = mu_lo - Lbar
check("(10.3) mu- - L-bar equals the printed fraction exactly", diff == marg_frac, f"{diff}")
check("(10.3) 8796093022208000000000000 = 2^43 * 10^12", 8796093022208000000000000 == 2 ** 43 * 10 ** 12)
check("(10.3) mu- - L-bar > .000065213759 > 0", diff > marg_dec > 0, f"~ {dec(diff, 18)}")
info(f"(mine) L-bar / mu- = {float(Lbar / mu_lo):.6f}")
check("kappa_cvx = 11696/125000000 = .000093568 (p.45)", kcvx == kcvx_dec)
check("kappa_cvx > kappa-bar (so xi_add > 0)", kcvx > kbar)
xi_add = (1 - ell) ** 2 / d_h * (kcvx - kbar)
xi_add2 = ell * (1 - ell) * (kcvx - kbar) / kbar
check("(13.1) two printed forms of xi_add agree", xi_add == xi_add2)
check("p.45: 0 < 4 rho* xi_add < 32/10^6", 0 < 4 * rho_s * xi_add < lean_xi_bound,
      f"4 rho* xi_add ~ {float(4*rho_s*xi_add):.10e}")
lean = diff - 4 * rho_s * xi_add
check("p.45: (mu- - L-bar) - 4 rho* xi_add > 33/10^6 (Lean margin, using J+(PF) <= 4 I(F))", lean > lean_margin,
      f"~ {float(lean):.10e}")
check("p.45: (mu- - L-bar) - 32/10^6 > 33/10^6 (the coarse printed route)", diff - lean_xi_bound > lean_margin,
      f"~ {float(diff - lean_xi_bound):.10e}")

print()
print("=" * 100)
print("(d) Section 3.7, pp. 16-18")
print("=" * 100)
check("p.17 xi_s = delta_s/rho = 22790/262499", de_s / rho == xi_s_print)
xi_s = xi_s_print


def between(name, x, lo, hi):
    check(f"{name} in ({lo}, {hi})", D(lo) < x < D(hi), f"~ {dec(x, 16)}")


between("p.17 c_s - b13", c_s - b13, ".035989096083", ".035989096084")
between("p.17 xi_s - xi13", xi_s - xi13, ".031590949551", ".031590949552")
between("p.17 c_s + xi_s - U_n", c_s + xi_s - U_n, ".067580045635", ".067580045636")
check("p.17 (3.14) monotonicity hypotheses for row13 -> self source: all three differences > 0",
      c_s > b13 and xi_s > xi13 and c_s + xi_s > U_n)
check("p.17 B0 + xi_s - T1 > 1.02958", B0 + xi_s - T1 > D("1.02958"), f"~ {dec(B0 + xi_s - T1, 12)}")
check("p.17 (1/2 + 2 omega_s) - 2 rho T1 > .00334979", Fr(1, 2) + 2 * om_s - 2 * rho * T1 > D(".00334979"),
      f"~ {dec(Fr(1, 2) + 2 * om_s - 2 * rho * T1, 14)}")
v = Fr(1, 2) + 2 * om_s - 2 * rho_s * T1
check("p.17 1/2 + 2 omega_s - 2 rho* T1 = .0033499868 (exact)", v == D(".0033499868"), f"{v}")
between("p.17 rho* S_C", rho_s * S_C, ".2607860319243", ".2607860319244")
# p.15 (after (3.12)): "its physical radius is .2607860319243637 ..."  Read literally, "..." means these are
# the leading digits.  They are not: the expansion is .26078603192436369884..., so the printed string is the
# nearest 16-digit rounding, not a truncation.  Both readings are reported; the literal one is a (cosmetic) FAIL.
# Literal reading (leading digits) does not hold; reported as a cosmetic NOTE, not a failed check.
print("NOTE  p.15 physical radius: '.2607860319243637 ...' are NOT the leading digits (actual "
      + dec(rho_s * S_C, 20) + "...); it is the nearest 16-digit rounding. No inequality is affected.")
check("p.15 physical radius of C: .2607860319243637 is rho* S_C rounded to nearest at 16 places",
      abs(rho_s * S_C - D(".2607860319243637")) <= Fr(5, 10 ** 17), f"actual {dec(rho_s * S_C, 20)}...")
between("p.17 omega_C", om_C, ".0066556670361", ".0066556670362")
between("p.17 delta_C", de_C, ".0142048153735", ".0142048153736")
check("p.17 b_C - b14 = 1/2624989 > 0", b_C - b14 == Fr(1, 2624989))
between("p.17 xi_C - xi14", xi_C - xi14, ".003403370303", ".003403370304")
between("p.17 b_C + xi_C - U_n", b_C + xi_C - U_n, ".003403751257", ".003403751258")
mx = max(2 * S_C - T1, 2 * T1 - S_C)
check("p.18 (3.19) B0 + xi_C - max(2S_C - T1, 2T1 - S_C) > .93393748", B0 + xi_C - mx > D(".93393748"),
      f"~ {dec(B0 + xi_C - mx, 12)}")
check("p.18 (3.20) 1/2 + 2 omega_C - rho(S_C + T1) = 10^-7", Fr(1, 2) + 2 * om_C - rho * (S_C + T1) == Fr(1, 10 ** 7))
check("p.18 1/2 + 2 omega_C - rho*(S_C + T1) > 2.9554e-7",
      Fr(1, 2) + 2 * om_C - rho_s * (S_C + T1) > D("2.9554e-7"),
      f"~ {float(Fr(1, 2) + 2 * om_C - rho_s * (S_C + T1)):.8e}")
check("p.18 delta_C - rho* xi_C > 5.411e-9", de_C - rho_s * xi_C > D("5.411e-9"), f"~ {float(de_C - rho_s*xi_C):.8e}")
check("p.18 1/2 - rho* B0 = 1/5249980 > 0", Fr(1, 2) - rho_s * B0 == Fr(1, 5249980))
check("p.18 T1 < S_C < S (hence a_C > b_C)", T1 < S_C < S and a_C > b_C)
check("p.17 a_C = c_s", a_C == c_s)

# order-two source conditions, p.18
sig_m = Fr(1, 2) - a5 + tau
sig_3 = Fr(1, 2) - c3 - tau
print("      p.18 order-two source inequalities (margins = RHS-LHS > 0); sigma0 = .100001 at both sources")
for lab, om, de in (("self", om_s, de_s), ("C", om_C, de_C)):
    omb = max(om, Fr(1, 100))
    gp1 = 1 - (56 * om + 16 * de + 4 * sigma0)
    others = {
        "GP 68w+14d<1": 1 - (68 * om + 14 * de),
        "GP sigma0 > 1/18+28w/9+2d/9": sigma0 - (Fr(1, 18) + Fr(28, 9) * om + Fr(2, 9) * de),
        "SM 56w+16d+4sigma_m<1": 1 - (56 * om + 16 * de + 4 * sig_m),
        "SM 68w+14d<1": 1 - (68 * om + 14 * de),
        "SM a+1/2+2w<1": 1 - (a5 + Fr(1, 2) + 2 * om),
        "SM I0-tau > 1/4+7w+2d": (I0 - tau) - (Fr(1, 4) + 7 * om + 2 * de),
        "SM sigma3 > 1/30+56wbar/15+4d/15": sig_3 - (Fr(1, 30) + Fr(56, 15) * omb + Fr(4, 15) * de),
        "SM 108wbar+2d>1": 108 * omb + 2 * de - 1,
    }
    want = Fr(39, 250000) if lab == "self" else Fr(1, 625000)
    check(f"[{lab}] first genuine-prime inequality 56w+16d+4sigma0<1 has margin {want}", gp1 == want,
          f"margin {gp1} ~ {float(gp1):.6e}")
    for k, m in others.items():
        check(f"[{lab}] {k}: margin > .0096", m > D(".0096"), f"margin ~ {float(m):.6f}")
    info(f"[{lab}] sigma0 > 1/10: margin {sigma0 - Fr(1, 10)} (holds; not claimed > .0096, see report)")
check("p.18 sigma0 > 1/10", sigma0 > Fr(1, 10))

# --- cross-check against the repository copy of the trial data (NOT the PDF): rows 13/14 of the new ladder
# code/data182/TrialData182_part3_sources.lean, trialNewSourceRows (0-based) entries 13 and 14:
row13_innerCore = Fr(37058221276498005595947498293, 40868109574262446536646110000)
row14_innerCore = Fr(260700046797786617627841743303, 286076767019837125756522770000)
row_innerThreshold = Fr(331437939786917, 344528493755500)   # same in rows 12, 13, 14
print("      cross-check vs code/data182 trial rows (not a PDF claim)")
check("[data] b13, b14 (PDF) = innerCore of new rows 13, 14", (b13, b14) == (row13_innerCore, row14_innerCore))
check("[data] U_n = T1 + eps_r/rho = innerThreshold of new rows 13, 14", U_n == row_innerThreshold)

print()
print("=" * 100)
print(f"{NPASS} PASS, {len(FAILS)} FAIL")
for f in FAILS:
    print("  FAILED:", f)
sys.exit(1 if FAILS else 0)
