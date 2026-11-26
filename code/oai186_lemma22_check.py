#!/usr/bin/python3
"""Independent check of Lemma 2.2 (Dickman cell enclosures), p. 12 of
OpenAI, "Numerical certificate for prime gaps at most 186" (30 Aug 2026),
code/third_party/openai186/short_gaps_numerics.pdf.

Lemma 2.2 (as printed, bars confirmed on the rendered page):
  c = M h, d_j = dbar_j = 1 for 0 <= j <= M, and for j >= M
    d_{j+1}    = max{0, d_j    - dbar_{j-M}/(2j) - dbar_{j+1-M}/(2(j+1))}
    dbar_{j+1} = min{1, dbar_j - d_{j-M}/(2j)    - d_{j+1-M}/(2(j+1)) + 1/(2M^3)}
  Claim: d_j <= D_c(jh) = rho(j/M) <= dbar_j.  Acceptance: ordered, in [0,1],
  both sequences nonincreasing.  (2.2): A_j(c)/h = 1 for j < M and, for j >= M,
    max{0, (d_j + d_{j+1})/2 - 1/(12 M^2)} <= A_j(c)/h <= (dbar_j + dbar_{j+1})/2,
  where A_j(c)/h = M * int_{j/M}^{(j+1)/M} rho(u) du.

Method (all rigorous; no floats in any decision):
  * The recurrence depends on M only (h cancels).  It is run in exact integer
    fixed point (units 2^-B) twice: rounded OUTWARD and rounded INWARD.  The map
    is monotone for the "wider interval" order, so  L_out <= L_exact <= L_in  and
    U_in <= U_exact <= U_out, where (L_exact, U_exact) is the exact-rational
    recurrence of (2.1).  Every statement about the exact rationals is decided
    from this sandwich; the sandwich itself is validated against genuine exact
    rationals (flint fmpq) on prefixes for every M and on the full range for
    M = 68225.  A third run rounds outward to 160 significant bits per step
    (a proxy for the PDF's 160-bit balls).
  * rho is enclosed by an independent Taylor-model integration of
    rho(u) = rho(s) - int_s^u rho(v-1)/v dv on cells of width 1/16, degree 62,
    in arb balls with explicit truncation bounds; F(u) = int_0^u rho likewise.
Run:  /usr/bin/python3 code/oai186_lemma22_check.py > code/oai186_lemma22_check.out
"""
import sys, time, resource
from flint import arb, arb_poly, fmpq, ctx

T0 = time.time()
ctx.prec = 320
N = 98304                 # (1.3), p. 2
n = N - 40                # (1.3)
B = 256                   # fixed-point bits of the integer recurrences
ONE = 1 << B

# ---------------------------------------------------------------- parameters
# Aligned caps M = z/h actually used (Lemma 2.2 with c = M h):
SURVIVAL = [68225, 49152, 46580, 44781, 35265, 44976, 35419]   # (1.5) p. 2 (and z_G/h of (1.24))
FACTORIAL = [24576, 19660, 22390, 17912, 22488, 17990]          # p_G/h of (1.24), p. 6
# Low-kernel cutoffs L = floor(l0/h) (Sec. 1.5.1 bins, p. 9) and Lemma 2.4 caps
# (b+ = ceil, r- = floor, r+ = ceil) for the 30 rank-two bins.  These need the
# source ladders; they were listed from the authors' derived inputs
# (prime_gap_186_certificate.build_inputs, read-only) and agree in count and range
# with notes/oai186-lemma23-check*.md and -lemma24-check*.md.
LOW = [3, 6, 12, 25, 50, 93, 101, 187, 202, 404, 809, 940, 1411, 2116, 2331, 2667, 3175,
       3497, 4703, 5644, 6773, 8128, 9753, 11704, 14045, 16854, 18257, 20225, 22247, 24270]
RANK2 = [20689, 21614, 21615, 21719, 21813, 22391, 22488, 22538, 22539, 22785, 22786, 23463,
         23464, 23654, 23655, 23757, 23758, 24243, 24244, 24388, 24389, 24576, 24850, 24851,
         24987, 24988, 25215, 25216, 25312, 25313, 25590, 25702, 25775, 25776, 25941, 25942,
         26236, 26237, 26238, 26699, 26700, 26916, 27162, 27163, 27306, 27307, 27624, 27625,
         28087, 28672, 28673, 28735, 28736, 29243, 29346, 29855, 29985, 30037, 30038, 30399,
         30428, 30561, 31402, 31403, 31555, 32484, 32711, 32769, 32990, 33866, 35022, 35265,
         35419, 35499, 36178, 37334, 37481, 38230, 39646, 39979, 40961, 41957, 43691, 44269,
         44781, 44976, 46422, 46580, 49152]
GENERIC = list(range(1, 11)) + [63, 64]      # extra small M (lemma claims every M >= 1)
# last grid index each use needs: survival/rank-two arrays j <= n, low kernels j <= N-1,
# factorial grid j <= N  (all runs below go to j = N)
NEED = {}
for M in SURVIVAL + RANK2: NEED[M] = max(NEED.get(M, 0), n)
for M in LOW: NEED[M] = max(NEED.get(M, 0), N - 1)
for M in FACTORIAL: NEED[M] = max(NEED.get(M, 0), N)
for M in GENERIC: NEED.setdefault(M, N)
ROLE = {}
for name, lst in (("surv", SURVIVAL), ("fact", FACTORIAL), ("low", LOW), ("r2", RANK2), ("gen", GENERIC)):
    for M in lst: ROLE.setdefault(M, []).append(name)
ALLM = sorted(NEED)

checks = 0
fails = []
def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print("FAIL:", msg)

def say(*a):
    print(*a, flush=True)

say("Lemma 2.2 check; N =", N, "n =", n, "B =", B, "prec =", ctx.prec)
say("distinct M:", len(ALLM), " roles:", {k: len(v) for k, v in
    (("surv", SURVIVAL), ("fact", FACTORIAL), ("low", LOW), ("r2", sorted(set(RANK2))), ("gen", GENERIC))})
check(len(set(RANK2)) == 89 and len(LOW) == 30 and min(RANK2) == 20689 and max(RANK2) == 49152,
      "parameter list shape")

# ------------------------------------------------------ rigorous rho (Taylor model)
W = fmpq(1, 16)
WA = arb(W)
D = 62
UMAX = 24
NCELL = UMAX * 16
XBALL = arb(fmpq(1, 32), fmpq(1, 32))         # the interval [0, w]

def absup(p):
    """upper bound of |p(x)| for x in [0,w]"""
    return abs(p(XBALL)).upper()

P = [None] * NCELL     # rho(s + x) in P[i](x) +- E[i],  s = i/16, x in [0, 1/16]
E = [arb(0)] * NCELL
FP = [None] * NCELL    # F(s + x) = int_0^{s+x} rho  in FP[i](x) +- EF[i]
EF = [arb(0)] * NCELL
for i in range(16):
    P[i] = arb_poly([1])
    FP[i] = arb_poly([arb(fmpq(i, 16)), 1])
for i in range(16, NCELL):
    s = fmpq(i, 16)
    sa = arb(s)
    J = i - 16
    T = arb_poly([((-1) ** k) / sa ** (k + 1) for k in range(D + 1)])
    tau = (WA / sa) ** (D + 1) / sa
    prod = P[J] * T
    cs = prod.coeffs()
    hi_tail = arb(0)
    for k in range(D + 1, len(cs)):
        hi_tail += abs(cs[k]).upper() * WA ** k
    low = arb_poly(cs[:D + 1])
    eint = E[J] / sa + absup(P[J]) * tau + hi_tail          # integrand error bound
    G = low.integral()                                      # degree D+1
    gc = G.coeffs()
    c0 = P[i - 1](WA)
    newc = [c0] + [-g for g in gc[1:D + 1]]
    drop = abs(gc[D + 1]).upper() * WA ** (D + 1) if len(gc) > D + 1 else arb(0)
    P[i] = arb_poly(newc)
    E[i] = (E[i - 1] + WA * eint + drop).upper()
    FP[i] = arb_poly([FP[i - 1](WA)] + [x for x in P[i].integral().coeffs()[1:]])
    EF[i] = (EF[i - 1] + WA * E[i]).upper()
    # F error: |int (rho - P_i)| <= w E_i, plus carried EF
say("Taylor model built: cells", NCELL, "max E", E[-1], "max EF", EF[-1])

def rho_q(q):
    """ball containing rho(q), q an fmpq in [0, UMAX)"""
    if q <= 1:
        return arb(1)
    i = int((q * 16).floor())
    x = q - fmpq(i, 16)
    return P[i](arb(x)) + arb(0, E[i])

def F_q(q):
    if q <= 1:
        return arb(q)
    i = int((q * 16).floor())
    x = q - fmpq(i, 16)
    return FP[i](arb(x)) + arb(0, EF[i])

RHO_TAIL = rho_q(fmpq(UMAX * 16 - 1, 16)).upper()   # rho(u) <= this for u >= UMAX - 1/16 (rho nonincreasing)

# sanity: literature values (to 12+ digits) and first delay interval
lit = {2: "0.306852819440054691", 3: "0.0486083882911316", 4: "0.00491092564776083",
       5: "0.000354724700456040", 6: "0.0000196496963539553", 10: "2.77017183772596e-11"}
for u, v in lit.items():
    r = rho_q(fmpq(u))
    ref = arb(v)
    check(abs(r - ref).upper() < 1e-12 * abs(ref).upper() + arb(1e-300),
          f"rho({u}) vs literature")
    say(f"  rho({u}) = {r.str(20, radius=True)}")
mxrad = arb(0)
for k in range(0, 1601):
    q = 1 + fmpq(k, 1600)
    r = rho_q(q)
    ex = 1 - arb(q).log()
    check(r.overlaps(ex), f"rho(1+{k}/1600) vs 1-log u")
    mxrad = max(mxrad, r.rad())
# identity u rho(u) = int_{u-1}^u rho, and nonincrease on a fine grid
for k in range(64, NCELL * 4, 7):
    q = fmpq(k, 64)
    lhs = arb(q) * rho_q(q)
    rhs = F_q(q) - F_q(q - 1)
    check(lhs.overlaps(rhs) and lhs.rad() < 1e-60 and rhs.rad() < 1e-60, f"u rho(u) identity at {q}")
check(E[-1] < 1e-65 and EF[-1] < 1e-65, "Taylor-model error small")
say(f"  rho sanity done; max radius on [1,2] {mxrad}; rho tail bound for u>=UMAX: {RHO_TAIL}")

# ------------------------------------------------------------- recurrences
def cdiv(a, b):
    return -((-a) // b)

def round_sig(x, bits, up):
    """round nonneg integer x outward to `bits` significant bits"""
    if x <= 0:
        return 0
    e = x.bit_length() - bits
    if e <= 0:
        return x
    return (cdiv(x, 1 << e) if up else (x >> e)) << e

def run(M, mode, last=N, ctrl=None):
    """mode: 'out', 'in', 'r160'.  ctrl: negative-control perturbation."""
    L = [ONE] * (M + 1)
    U = [ONE] * (M + 1)
    eps_out = cdiv(ONE, 2 * M ** 3)
    eps_in = ONE // (2 * M ** 3)
    for j in range(M, last):
        a, b = 2 * j, 2 * (j + 1)
        if mode == "in":   # inward: lower rounded up, upper rounded down
            lo = L[j] - U[j - M] // a - U[j + 1 - M] // b
            up = U[j] - cdiv(L[j - M], a) - cdiv(L[j + 1 - M], b) + eps_in
        else:
            lo = L[j] - cdiv(U[j - M], a) - cdiv(U[j + 1 - M], b)
            up = U[j] - L[j - M] // a - L[j + 1 - M] // b + eps_out
            if ctrl == "no_eps":
                up -= eps_out
            elif ctrl == "lower_plus_eps":
                lo += eps_out
            elif ctrl == "swap_delayed":
                up = U[j] - U[j - M] // a - U[j + 1 - M] // b + eps_out
            if mode == "r160":
                lo = round_sig(lo, 160, False) if lo > 0 else lo
                up = round_sig(up, 160, True) if up > 0 else -round_sig(-up, 160, False)
        L.append(lo if lo > 0 else 0)
        U.append(up if up < ONE else ONE)
    return L, U

def accept_direct(L, U, upto):
    """first index violating the acceptance tests on 0..upto, or None"""
    for j in range(upto + 1):
        if not (0 <= L[j] <= U[j] <= ONE):
            return j
        if j and (L[j] > L[j - 1] or U[j] > U[j - 1]):
            return j
    return None

def accept_exact(M, Lo, Uo, Li, Ui, upto):
    """acceptance of the EXACT rational sequences, decided via the sandwich.
    returns (first failing index or None, number of undecided steps)"""
    und = 0
    for j in range(upto + 1):
        if Li[j] > Ui[j]:                    # not certified ordered
            if Lo[j] > Uo[j]:
                return j, und
            und += 1
        if j <= M:
            continue
        k = j - 1                            # step k -> k+1 = j, k >= M
        if Ui[k] == ONE:                     # U_exact[k] = 1 >= U_exact[j]
            continue
        # U_exact[j] <= U_exact[k] iff L[k-M]/(2k) + L[k+1-M]/(2(k+1)) >= 1/(2M^3)
        lhs_o = M ** 3 * (Lo[k - M] * (k + 1) + Lo[k + 1 - M] * k)
        rhs = ONE * k * (k + 1)
        if lhs_o >= rhs:
            continue
        lhs_i = M ** 3 * (Li[k - M] * (k + 1) + Li[k + 1 - M] * k)
        if lhs_i < rhs and Uo[k] < ONE:
            return j, und
        und += 1
    return None, und

TWOB = arb(2) ** B
INV2B = arb(2) ** (-B)

def compare_rho(M, Li, Ui, Lo, Uo, upto, stats):
    """L_in <= rho(j/M) <= U_in for all j <= upto (=> exact endpoints enclose rho),
    and the same for the outward run; (2.2) cell masses for j < upto."""
    bad = 0
    bad22 = 0
    minup = None; minlo = None; minm = None
    Fprev = None
    rho_cache = {}
    c22 = arb(1) / (12 * M * M)
    for j in range(upto + 1):
        q = fmpq(j, M)
        if q < UMAX - fmpq(1, 16):
            r = rho_q(q) * TWOB
            okl = (Li[j] == 0) or (r >= Li[j])
            oku = r <= Ui[j]
            Fj = F_q(q)
            if j > M and (j % 97 == 0 or j <= M + 3):   # sampled slacks (incl. j = M+1..M+3), informational
                su = (Ui[j] - r) * INV2B
                minup = su if minup is None or su < minup else minup
                if Li[j] > 0:
                    sl = (r - Li[j]) / r
                    minlo = sl if minlo is None or sl < minlo else minlo
            if Fprev is not None:
                k = j - 1
                A = (Fj - Fprev) * M * TWOB          # A_k(c)/h in units 2^-B
                if k < M:
                    ok22 = A.overlaps(TWOB) and A.rad() < arb(2) ** (B - 150)
                else:
                    lo22 = arb(Li[k] + Li[k + 1]) / 2 - c22 * TWOB
                    up22 = arb(Ui[k] + Ui[k + 1]) / 2
                    ok22 = ((lo22 <= 0) or (A >= lo22)) and (A <= up22)
                    m = (up22 - A) / TWOB
                    minm = m if minm is None or m < minm else minm
                if not ok22:
                    bad22 += 1
            Fprev = Fj
        else:                                       # tail: 0 < rho(u) <= RHO_TAIL
            okl = Li[j] == 0
            oku = Ui[j] >= RHO_TAIL * TWOB
            if j >= 1:
                k = j - 1
                qk = fmpq(k, M)
                rb = rho_q(qk).upper() if qk < UMAX - fmpq(1, 16) else RHO_TAIL
                ok22 = (Ui[k] + Ui[k + 1]) >= 2 * rb * TWOB and \
                       (Li[k] + Li[k + 1] <= c22 * TWOB * 2)
                if not ok22:
                    bad22 += 1
            Fprev = None
        if not (okl and oku):
            bad += 1
            if bad <= 3:
                print(f"   M={M} j={j}: lower_ok={okl} upper_ok={oku}")
        # outward run must be wider than inward
        if not (Lo[j] <= Li[j] and Ui[j] <= Uo[j]):
            bad += 1
    stats.update(minup=minup, minlo=minlo, min22=minm)
    return bad, bad22

# --------------------------------------------------------------- main loop
say("\n== Recurrence (2.1) for every M, j <= N, three roundings; rho comparison at every grid point ==")
say("columns: M roles | exact-acceptance first fail (j/M) | r160 / outward first fail | undecided | enclosure fails | (2.2) fails | sampled min (dbar-rho) | min ((dbar_j+dbar_j+1)/2 - A_j/h) | min rel. (rho-d)/rho sampled")
summary = {}
for M in ALLM:
    t = time.time()
    Lo, Uo = run(M, "out")
    Li, Ui = run(M, "in")
    Lr, Ur = run(M, "r160")
    need = NEED[M]
    fe, und = accept_exact(M, Lo, Uo, Li, Ui, N)
    fr = accept_direct(Lr, Ur, N)
    fo = accept_direct(Lo, Uo, N)
    st = {}
    bad, bad22 = compare_rho(M, Li, Ui, Lo, Uo, N, st)
    check(bad == 0, f"M={M}: enclosure d_j <= rho(j/M) <= dbar_j")
    check(bad22 == 0, f"M={M}: (2.2) cell-mass enclosure")
    check(und == 0, f"M={M}: acceptance decided for exact rationals")
    # first delay interval, exact closed form 1 - log(j/M), j in [M, 2M]
    okfd = all((arb(Li[j]) <= (1 - arb(fmpq(j, M)).log()) * TWOB) and
               ((1 - arb(fmpq(j, M)).log()) * TWOB <= arb(Ui[j])) for j in range(M, min(2 * M, N) + 1))
    check(okfd, f"M={M}: first delay interval 1 - log(j/M)")
    acc_need = fe is None or fe > need
    summary[M] = dict(fe=fe, fr=fr, fo=fo, acc_need=acc_need, roles=ROLE[M])
    # renewal fallback is the PDF's rule for low kernels; other uses must accept
    if any(r in ("surv", "fact", "r2") for r in ROLE[M]):
        check(acc_need and (fr is None or fr > need), f"M={M}: acceptance on its needed range j<={need}")
    say(f"M={M:6d} {','.join(ROLE[M]):9s} | exact fail {fe if fe is None else f'{fe} ({fe/M:.3f})'} "
        f"| r160 fail {fr} | out fail {fo} | und {und} | enc {bad} | 22 {bad22} "
        f"| {st['minup'].mid().str(3) if st['minup'] is not None else '-'} "
        f"| {st['min22'].mid().str(3) if st['min22'] is not None else '-'} "
        f"| {st['minlo'].mid().str(3) if st['minlo'] is not None else '-'} | {time.time()-t:.1f}s")
    check((fe is None) == (fr is None) and (fe is None) == (fo is None) or M < 64,
          f"M={M}: exact, outward and 160-bit acceptance agree")

acc = sorted(M for M in ALLM if summary[M]["fe"] is None and M >= 64)
rej = sorted(M for M in ALLM if summary[M]["fe"] is not None and M >= 64)
say("\nM >= 64 accepted on all j <= N:", len(acc), "min", min(acc) if acc else None)
say("M >= 64 rejected:", rej)
low_delay = [M for M in LOW if M >= 64 and summary[M]["acc_need"]]
say("low kernels (61 bins, 30 distinct L): delay branch for L =", low_delay, f"({len(low_delay)} distinct)")
for M in SURVIVAL + FACTORIAL + RANK2:
    pass

# ------------------------------------------- genuine exact rationals (fmpq)
say("\n== Exact rationals (fmpq) against the integer sandwich ==")
def run_exact(M, last):
    L = [fmpq(1)] * (M + 1); U = [fmpq(1)] * (M + 1)
    e = fmpq(1, 2 * M ** 3); one = fmpq(1); zero = fmpq(0)
    for j in range(M, last):
        a = fmpq(1, 2 * j); b = fmpq(1, 2 * (j + 1))
        lo = L[j] - U[j - M] * a - U[j + 1 - M] * b
        up = U[j] - L[j - M] * a - L[j + 1 - M] * b + e
        L.append(lo if lo > 0 else zero); U.append(up if up < one else one)
    return L, U

def sandwich_ok(M, last, Le, Ue):
    Lo, Uo = run(M, "out", last); Li, Ui = run(M, "in", last)
    ok = True
    for j in range(last + 1):
        if not (fmpq(Lo[j], ONE) <= Le[j] <= fmpq(Li[j], ONE) and
                fmpq(Ui[j], ONE) <= Ue[j] <= fmpq(Uo[j], ONE)):
            ok = False
            break
    # acceptance of the fmpq sequences directly vs sandwich decision
    fe_direct = None
    for j in range(last + 1):
        if not (0 <= Le[j] <= Ue[j] <= 1) or (j and (Le[j] > Le[j - 1] or Ue[j] > Ue[j - 1])):
            fe_direct = j; break
    fe_sand, _ = accept_exact(M, Lo, Uo, Li, Ui, last)
    return ok, fe_direct, fe_sand

for M in ALLM:
    last = min(N, M + 1500 if M >= 64 else 200 * M)
    Le, Ue = run_exact(M, last)
    ok, fd, fs = sandwich_ok(M, last, Le, Ue)
    check(ok and fd == fs, f"M={M}: fmpq prefix j<={last} inside sandwich, acceptance agrees ({fd},{fs})")
say(f"  prefix comparisons done for {len(ALLM)} values of M")
for Mfull in (68225, 49152):      # full range is feasible (memory) only for the largest caps
    t = time.time()
    Le, Ue = run_exact(Mfull, N)
    ok, fd, fs = sandwich_ok(Mfull, N, Le, Ue)
    check(ok and fd is None and fs is None, f"M={Mfull}: full-range fmpq inside sandwich and accepted")
    say(f"  full exact M={Mfull}, j<=N: sandwich ok={ok}, accept fail direct={fd} sandwich={fs}; "
        f"denominator bits of d_N {int(Le[-1].q).bit_length()}; {time.time()-t:.1f}s")
    del Le, Ue

# --------------------------------------------------------- negative controls
say("\n== Negative controls (each must FAIL somewhere) ==")
def count_enc(M, L, U, shift_up=0, shift_lo=0, upto=None):
    upto = upto or N
    nl = nu = 0
    for j in range(M, upto + 1):
        ql = fmpq(j + shift_lo, M); qu = fmpq(j + shift_up, M)
        if qu < UMAX - 1 and (rho_q(qu) * TWOB > U[j]):
            nu += 1
        if ql < UMAX - 1 and L[j] > 0 and (rho_q(ql) * TWOB < L[j]):
            nl += 1
    return nl, nu

for M in (64, 11704, 24576, 68225):
    upto = min(N, M + 20000)
    L, U = run(M, "out", upto, ctrl="no_eps")
    nl, nu = count_enc(M, L, U, upto=upto)
    check(nu > 0, f"NC1 M={M}: dropping 1/(2M^3) must break the upper bound"); say(f"  NC1 M={M}: no 1/(2M^3): upper violations {nu}")
    L, U = run(M, "out", upto, ctrl="lower_plus_eps")
    nl, nu = count_enc(M, L, U, upto=upto)
    check(nl > 0, f"NC2 M={M}: +1/(2M^3) in lower must break it"); say(f"  NC2 M={M}: +1/(2M^3) in lower: lower violations {nl}")
    L, U = run(M, "out", upto)
    nl, nu = count_enc(M, L, U, shift_up=-1, shift_lo=+1, upto=upto)
    check(nl > 0 and nu > 0, f"NC3 M={M}: one-cell shift must be detected"); say(f"  NC3 M={M}: compare at shifted point: lower {nl}, upper {nu}")
    # (2.2) lower bound without the -1/(12M^2) term
    nb = 0
    for k in range(M, upto):
        if fmpq(k + 1, M) >= UMAX - 1:
            continue
        A = (F_q(fmpq(k + 1, M)) - F_q(fmpq(k, M))) * M * TWOB
        if A < arb(L[k] + L[k + 1]) / 2:
            nb += 1
    check(nb > 0, f"NC4 M={M}: (2.2) without h^3/(12c^2) must fail"); say(f"  NC4 M={M}: (2.2) lower w/o trapezoid term: violations {nb}")
    L, U = run(M, "out", upto, ctrl="swap_delayed")
    nl, nu = count_enc(M, L, U, upto=upto)
    say(f"  NC5 M={M} (informational): upper with dbar delayed instead of d: upper violations {nu}")

# ------------------------------------------------------------------ summary
say("\n== Summary ==")
say("checks:", checks, " failures:", len(fails))
for f in fails[:20]:
    say("  ", f)
say(f"runtime {time.time() - T0:.1f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
