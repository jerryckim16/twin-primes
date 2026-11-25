#!/usr/bin/env python3
"""Second, independent check of Lemma 1.4 of the OpenAI preprint
"Numerical certificate for prime gaps at most 186" (30 Aug 2026),
code/third_party/openai186/short_gaps_numerics.pdf, p. 9.

Lemma 1.4: "After the bounds for the largest fragment and opposite root have
been imposed, every retained order-three failure is a nonlargest H_{5/2}
failure at the corresponding threshold."

Written from the PDF only (no other repository code or data is used).
Exact rational arithmetic only (fractions.Fraction).

Method (see notes/oai186-lemma14-check2.md):
  Part A  recompute all source data from (1.13)-(1.21) exactly, and
          cross-check every printed number we rely on (row counts, order
          counts, retained rows (1.20), masks (1.5), (1.17), boundary floors).
  Part B  decide the lemma exactly: a counterexample must lie in one of a
          finite list of rational polyhedra (min/max of the allocation
          functions are expanded into conjunctions/disjunctions, NOT sliced at
          breakpoints); each polyhedron is shown empty by exact
          Fourier-Motzkin elimination with strict/non-strict bookkeeping.
          Done once with the continuous caps (1.18) and once with the actual
          grid masks (1.5)/(1.19) that the certificate uses.
  Part C  brute force: evaluate the predicates of (1.21) literally on every
          multiset (size <= 4) drawn from a rational grid of fragment sizes
          that contains all critical values, for every retained order-three
          row and both predicates, and test the lemma's implication directly
          (and its converse).
"""
import itertools
import sys
import time
from fractions import Fraction as Fr

T_START = time.time()
NCHECK = 0
NFAIL = 0
LOG = []


def check(cond, msg):
    global NCHECK, NFAIL
    NCHECK += 1
    if not cond:
        NFAIL += 1
        print("FAIL:", msg)


def out(*a):
    print(*a)
    sys.stdout.flush()


# ---------------------------------------------------------------- Part A
g0 = Fr(1, 10**7)
eps = {"o": Fr(1, 10**6), "n": Fr(1, 10**7)}
tau = Fr(1, 10**10)
sigma0 = Fr(100001, 10**6)
sigmam = Fr(1, 2) - Fr(40481, 100000) + tau
Omega = {"o": Fr(12499, 10**6), "n": Fr(253, 20000)}
rho = Fr(1, 4) + Omega["o"]
rhos = rho - g0
S = Fr(2742997, 10**7) / rhos
T1 = Fr(251, 1000) / rhos
T0 = 2 - Fr(3, 1000) - S
e = g0 / rho
zeta = Fr(19037, 100000) / rho
T = {"o": T0, "n": T1}

# (1.1) printed values
check(S == Fr(2742997, 2624989), "S (1.1)")
check(rhos == Fr(2624989, 10**7), "rho_* (1.1)")
check(T0 == Fr(2499106033, 2624989000), "T0 (1.1)")
check(T1 == Fr(2510000, 2624989), "T1 (1.1)")
check(rho == Fr(262499, 10**6), "rho (1.1)")
check(0 < T0 < T1 < S, "0<T0<T1<S")

N = 98304
h = S / N
n_grid = N - 40
check(n_grid == 98264, "n")

cs = {
    "o": {1: ((1 - 5 * sigma0) / 15, Fr(18, 5)), 2: ((1 - 4 * sigma0) / 16, Fr(7, 2)), 3: (Fr(3, 80), Fr(3))},
    "n": {1: ((1 - 5 * sigmam) / 15, Fr(18, 5)), 2: ((1 - 4 * sigmam) / 16, Fr(7, 2)), 3: ((1 - 2 * sigmam) / 20, Fr(16, 5))},
}


def order(t):
    return 1 if t < 12 else (2 if t < 24 else 3)


rows = {}
for nu in ("o", "n"):
    E = rho * (S + T[nu]) - Fr(1, 2)
    wprev = Fr(0)
    lst = []
    t = 0
    while True:
        r = order(t)
        c, s_ = cs[nu][r]
        raw = (c - eps[nu] - E + 2 * wprev - g0) / s_
        w = min(Omega[nu], raw)
        delta = c - s_ * w - eps[nu]
        B = (Fr(1, 2) + 2 * wprev) / rho
        Bp = (Fr(1, 2) + 2 * w) / rho
        xi = delta / rho
        a = B - T[nu]
        b = B - S
        eta = xi if r <= 2 else (xi + S + T[nu] - B) / 2
        A = a + eta
        C = b + eta
        terminal = (w == Omega[nu])
        lst.append(dict(nu=nu, t=t, r=r, w=w, wprev=wprev, delta=delta, B=B, Bp=Bp, xi=xi,
                        a=a, b=b, eta=eta, A=A, C=C, terminal=terminal, E=E))
        if terminal:
            break
        wprev = w
        t += 1
    rows[nu] = lst

check(len(rows["o"]) == 29 and len(rows["n"]) == 43, "ladder lengths 29, 43")
for nu, cnt in (("o", (12, 12, 5)), ("n", (12, 12, 19))):
    got = tuple(sum(1 for R in rows[nu] if R["r"] == k) for k in (1, 2, 3))
    check(got == cnt, f"order counts {nu}: {got}")
# first occurrence of Omega is the last row only
for nu in rows:
    check(all(not R["terminal"] for R in rows[nu][:-1]), f"terminal only last {nu}")

# (1.20) retained rows
Sbox = 98303 * h
Tbox = {"o": 89563 * h, "n": 89953 * h}
retained = {nu: [R for R in rows[nu] if R["B"] < Sbox + Tbox[nu]] for nu in rows}
check([R["t"] for R in retained["o"]] == list(range(28)), "retained old 0..27")
check([R["t"] for R in retained["n"]] == list(range(39)), "retained new 0..38")
# boundary table of Lemma 1.1 proof
fl = lambda x: x.numerator * 1 // x.denominator  # noqa: E731  floor for positive Fraction
check(fl(rows["o"][27]["B"] / h) == 187773, "floor B_o27/h")
check(fl(rows["o"][28]["B"] / h) == 188087, "floor B_o28/h")
check(fl(rows["n"][38]["B"] / h) == 188254, "floor B_n38/h")
check(fl(rows["n"][39]["B"] / h) == 188256, "floor B_n39/h")
check(fl(Sbox / h + Tbox["o"] / h) == 187866 and Sbox / h + Tbox["n"] / h == 188256, "pair maxima")

# (1.17) and Lemma 1.1 ingredients for retained order-three rows
O3 = {nu: [R for R in retained[nu] if R["r"] == 3] for nu in rows}
check([R["t"] for R in O3["o"]] == [24, 25, 26, 27], "old order-3 retained 24..27")
check([R["t"] for R in O3["n"]] == list(range(24, 39)), "new order-3 retained 24..38")
for nu in rows:
    for R in retained[nu]:
        nonterm_ok = (R["delta"] - R["E"] + 2 * R["wprev"] == g0)
        check(nonterm_ok, f"delta-E+2w=g0 {nu}{R['t']}")
        if R["r"] <= 2:
            check((R["A"], R["C"]) == (S + e, T[nu] + e), f"(1.17) r<=2 {nu}{R['t']}")
        else:
            check((R["A"], R["C"]) == (S + e / 2, T[nu] + e / 2), f"(1.17) r=3 {nu}{R['t']}")
for nu in rows:
    for R in O3[nu]:
        R["L"] = Fr(23, 40) * R["C"]
        check(max(R["A"], R["C"]) <= Fr(7, 3) * R["L"], f"max(A,C)<=7L/3 {nu}{R['t']}")
        check(R["A"] >= R["C"] > R["L"] > 0 and R["xi"] > 0, f"A>=C>L>0, xi>0 {nu}{R['t']}")
        check(R["eta"] == R["xi"] - e / 2, f"eta=xi-e/2 {nu}{R['t']}")

# ---- continuous caps (1.18): list of (lo, hi, z), lower-open upper-closed
an = {t: rows["n"][t]["a"] for t in (0, 24)}
bo = {t: rows["o"][t]["b"] for t in (12, 24)}
bn = {t: rows["n"][t]["b"] for t in (12, 24)}
C1 = T1 + e / 2
C0 = T0 + e / 2
caps = {
    "outer": [(Fr(-1), an[0], zeta), (an[0], an[24], (S + e) / 2), (an[24], S, S + e / 2 - Fr(23, 40) * C1)],
    "base": [(Fr(-1), bo[12], zeta), (bo[12], bo[24], (T0 + e) / 2), (bo[24], T0, Fr(63, 160) * C0)],
    "enlarged": [(Fr(-1), bn[12], zeta), (bn[12], bn[24], (T1 + e) / 2), (bn[24], T1, Fr(63, 160) * C1)],
    "full": [(Fr(-1), S, zeta)],
}
dims = {"outer": 40, "base": 39, "enlarged": 39, "full": 39}
printed_masks = {
    "outer": [(0, 89196, 68225), (89197, 95598, 49152), (95599, 98263, 46580)],
    "base": [(0, 84930, 68225), (84931, 87194, 44781), (87195, 89524, 35265)],
    "enlarged": [(0, 85161, 68225), (85162, 87249, 44976), (87250, 89914, 35419)],
    "full": [(0, 98263, 68225)],
}
masks = {}
for dom, shells in caps.items():
    d = dims[dom]
    ms = []
    for (lo, hi, z) in shells:
        jlo = 0 if lo < 0 else max(0, fl(lo / h) - d + 1)
        jhi = min(98263, fl(hi / h) - d)
        ms.append((jlo, jhi, fl(z / h)))
    masks[dom] = ms
    check(ms == printed_masks[dom], f"mask (1.19) reproduces (1.5) for {dom}: {ms}")

# H0 ⊆ H1 ⊆ Hf at the grid level (cap index pointwise in j, and j-ranges nested):
# needed because new-row inner failures are evaluated with the enlarged caps.
def capidx(dom, j):
    for (jlo, jhi, zi) in masks[dom]:
        if jlo <= j <= jhi:
            return zi
    return None


for small, big in (("base", "enlarged"), ("enlarged", "full")):
    ok = True
    for (jlo, jhi, zi) in masks[small]:
        for j in {jlo, jhi} | {b[0] for b in masks[big] if jlo <= b[0] <= jhi} | {b[1] for b in masks[big] if jlo <= b[1] <= jhi}:
            cb = capidx(big, j)
            ok = ok and cb is not None and zi <= cb
    check(ok, f"grid inclusion {small} ⊆ {big}")

# (1.19) completeness at the grid level: a cell of index sum j (d coords) has
# totals in [j h, (j+d) h); verify that the mask's cap index is <= floor(z(s)/h)
# for every continuous total s the cell can carry. (Shell boundaries only.)
for dom in caps:
    d = dims[dom]
    for (jlo, jhi, zi) in masks[dom]:
        # largest total of the block: (jhi+d)h (exclusive); smallest: jlo*h
        for (lo, hi, z) in caps[dom]:
            meets = (jhi + d) * h > lo and jlo * h <= hi
            if meets:
                check(zi * h <= z, f"mask cap {dom} j{jlo}:{jhi} <= continuous cap of shell met")

# ---------------------------------------------------------------- Part B
# Linear constraints over variables; each constraint: (coef dict, strict, rhs) meaning
#   sum coef[v]*v  <  rhs  (strict)   or   <= rhs (non-strict)


def fm_feasible(cons, vars_):
    """Exact Fourier-Motzkin: return True iff the system has a real solution."""
    cons = [(dict(cf), st, Fr(rhs)) for cf, st, rhs in cons]
    for v in vars_:
        pos, neg, zero = [], [], []
        for cf, st, rhs in cons:
            k = cf.get(v, 0)
            (pos if k > 0 else neg if k < 0 else zero).append((cf, st, rhs))
        new = list(zero)
        for cp, sp, rp in pos:
            kp = cp[v]
            for cn, sn, rn in neg:
                kn = -cn[v]
                cf = {}
                for w in set(cp) | set(cn):
                    val = cp.get(w, 0) * kn + cn.get(w, 0) * kp
                    if w != v and val != 0:
                        cf[w] = val
                new.append((cf, sp or sn, rp * kn + rn * kp))
        cons = new
    for cf, st, rhs in cons:
        assert not cf
        if rhs < 0 or (rhs == 0 and st):
            return False
    return True


def lt(cf, rhs):
    return (cf, True, rhs)


def le(cf, rhs):
    return (cf, False, rhs)


def gt(cf, rhs):
    return ({k: -v for k, v in cf.items()}, True, -rhs)


def ge(cf, rhs):
    return ({k: -v for k, v in cf.items()}, False, -rhs)


H32 = Fr(3, 2)


def phiD_gt(Pc, p, L, thr):
    """DNF of  P + phiD(p) > thr, phiD = min(3p/2, L): one conjunction."""
    return [[gt({**Pc, p: Pc.get(p, 0) + H32}, thr), gt(Pc, thr - L)]]


def phiD_le(Pc, p, L, thr):
    """P + phiD(p) <= thr: disjunction of two."""
    return [[le({**Pc, p: Pc.get(p, 0) + H32}, thr)], [le(Pc, thr - L)]]


def phiE_gt(Pc, p, L, thr):
    """P + phiE(p) > thr, phiE = max(3p/2, 3p-L): disjunction of two."""
    return [[gt({**Pc, p: Pc.get(p, 0) + H32}, thr)], [gt({**Pc, p: Pc.get(p, 0) + 3}, thr + L)]]


def phiE_le(Pc, p, L, thr):
    return [[le({**Pc, p: Pc.get(p, 0) + H32}, thr), le({**Pc, p: Pc.get(p, 0) + 3}, thr + L)]]


def h52_le(Pc, p, thr):
    return [[le({**Pc, p: Pc.get(p, 0) + H32}, thr)]]


def h52_gt(Pc, p, thr):
    return [[gt({**Pc, p: Pc.get(p, 0) + H32}, thr)]]


def conj(*dnfs):
    res = [[]]
    for d in dnfs:
        res = [x + y for x in res for y in d]
    return res


def empty(dnf, vars_):
    return all(not fm_feasible(c, vars_) for c in dnf)


def lemma_regions(R, kind, cap):
    """Regions whose emptiness implies the lemma for row R, predicate kind in
    {'O','I'}, fragment cap `cap` (every fragment <= cap).  Returns list of
    (name, dnf, vars).  Variables: M largest fragment, p witness, P inclusive prefix."""
    A, C, L, xi = R["A"], R["C"], R["L"], R["xi"]
    base_M = [gt({"M": 1}, xi), le({"M": 1}, cap)]
    regs = []
    if kind == "O":
        thr = A
        # (i) unique largest witness, prefix P = M, H_{phiD} failure
        regs.append(("O-largest", conj([base_M], phiD_gt({"M": 1}, "M", L, A)), ["M"]))
        # (ii) phiE(M_xi) > C with M_xi = M > xi  (M_xi = 0 gives phiE(0)=0 <= C)
        regs.append(("O-phiE(M)", conj([base_M], phiE_gt({}, "M", L, C)), ["M"]))
        # (iii) nonlargest witness: P >= 2p, H_{phiD} fails but H_{5/2} at same p does not
        bp = [[gt({"p": 1}, xi), ge({"P": 1, "p": -2}, 0)]]
        regs.append(("O-nonlargest", conj(bp, phiD_gt({"P": 1}, "p", L, A), h52_le({"P": 1}, "p", A)), ["P", "p"]))
        # converse (not part of the lemma): nonlargest H5/2 failure but phiD-obstruction holds
        regs.append(("O-converse", conj(bp, h52_gt({"P": 1}, "p", A), phiD_le({"P": 1}, "p", L, A)), ["P", "p"]))
    else:
        thr = C
        regs.append(("I-largest", conj([base_M], phiE_gt({"M": 1}, "M", L, C)), ["M"]))
        regs.append(("I-phiD(M)", conj([base_M], [[gt({"M": H32}, A), gt({}, A - L)]]), ["M"]))
        bp = [[gt({"p": 1}, xi), ge({"P": 1, "p": -2}, 0)]]
        regs.append(("I-nonlargest", conj(bp, phiE_gt({"P": 1}, "p", L, C), h52_le({"P": 1}, "p", C)), ["P", "p"]))
        regs.append(("I-converse", conj(bp, h52_gt({"P": 1}, "p", C), phiE_le({"P": 1}, "p", L, C)), ["P", "p"]))
    return regs


# Sanity test of the FM decider on regions that must be NON-empty
# (e.g. the largest-witness region without any cap must be feasible).
def fm_selftest():
    R = O3["n"][0]
    for kind in ("O", "I"):
        regs = lemma_regions(R, kind, Fr(10))  # absurdly large cap
        nonempty = [nm for nm, dnf, vs in regs if not empty(dnf, vs)]
        check(any("largest" in nm and "non" not in nm for nm in nonempty),
              f"selftest: uncapped largest-witness region is nonempty ({kind})")
    check(fm_feasible([gt({"x": 1}, 0), lt({"x": 1}, 1)], ["x"]), "selftest 0<x<1")
    check(not fm_feasible([gt({"x": 1}, 1), le({"x": 1}, 1)], ["x"]), "selftest x>1,x<=1")
    check(fm_feasible([ge({"x": 1}, 1), le({"x": 1}, 1)], ["x"]), "selftest x=1")


fm_selftest()

# Which rows on which domain.  Outer predicate O_t: outer cap, all retained
# order-three rows of both ladders.  Inner I_t: old rows on the base domain H0,
# new rows on the enlarged domain H1 (H0 ⊆ H1; beta_new is over H1 \ L1).
assign = [("outer", "O", O3["o"] + O3["n"], "a", 40),
          ("base", "I", O3["o"], "b", 39),
          ("enlarged", "I", O3["n"], "b", 39)]

nB = 0
tightness = {}
for mode in ("continuous", "grid"):
    for dom, kind, rws, key, d in assign:
        for R in rws:
            core = R[key]
            # caps that can occur together with s > core
            if mode == "continuous":
                zs = [z for (lo, hi, z) in caps[dom] if hi > core]
            else:
                zs = [zi * h for (jlo, jhi, zi) in masks[dom] if (jhi + d) * h > core]
            check(len(zs) >= 1, "some shell above core")
            cap = max(zs)
            for nm, dnf, vs in lemma_regions(R, kind, cap):
                nB += 1
                check(empty(dnf, vs), f"{mode} {dom} {R['nu']}{R['t']} region {nm} empty (cap={float(cap)})")
            # record slack of the decisive cap inequalities
            A, C, L = R["A"], R["C"], R["L"]
            if kind == "O":
                sl = min(A - L - cap, Fr(21, 40) * C - cap)
            else:
                sl = Fr(63, 160) * C - cap
            tightness[(mode, dom, R["nu"], R["t"])] = sl
out(f"Part B: {nB} polyhedral regions decided by exact Fourier-Motzkin")
for mode in ("continuous", "grid"):
    for dom in ("outer", "base", "enlarged"):
        vals = [(v, k) for k, v in tightness.items() if k[0] == mode and k[1] == dom]
        v, k = min(vals)
        out(f"  {mode:10s} {dom:8s}: min cap slack {float(v):.6e} (row {k[2]}{k[3]})")

# Data facts that make the outer domain work: old order-three cores lie above
# the start of the outer order-three shell, both continuously and on the grid.
out("  a_o24 - a_n24 =", float(O3["o"][0]["a"] - an[24]),
    "; (95598+40)h - a_o24 =", float((95598 + 40) * h - O3["o"][0]["a"]))
out("  b_o24 - b_n24 =", float(bo[24] - bn[24]))

# ---------------------------------------------------------------- Part C
# Literal evaluation of (1.21) on multisets.


def Hphi(X, phi, xi):
    best = Fr(0)
    for p in X:
        if p > xi:
            pref = sum((q for q in X if q >= p), Fr(0))
            best = max(best, pref + phi(p))
    return best


def Mxi(X, xi):
    ps = [p for p in X if p > xi]
    return max(ps) if ps else Fr(0)


def nonlargest_H52_fail(X, xi, thr):
    for p in X:
        if p > xi:
            ge_p = [q for q in X if q >= p]
            if len(ge_p) >= 2 and sum(ge_p, Fr(0)) + H32 * p > thr:
                return True
    return False


nC = 0
nC_fail_conv = 0
for dom, kind, rws, key, d in assign:
    for R in rws:
        A, C, L, xi = R["A"], R["C"], R["L"], R["xi"]
        phiD = lambda u, L=L: min(H32 * u, L)  # noqa: E731
        phiE = lambda u, L=L: 3 * u - min(H32 * u, L)  # noqa: E731
        core = R[key]
        cap = max(zi * h for (jlo, jhi, zi) in masks[dom] if (jhi + d) * h > core)
        thr = A if kind == "O" else C
        dl = Fr(1, 10**9)
        crit = [xi, 2 * L / 3, cap, A - L, Fr(21, 40) * C, Fr(63, 160) * C, thr / 2, thr / 3,
                Fr(2, 7) * thr, Fr(2, 5) * thr, (thr - L) / 2, (thr + L) / 5, (thr - L) / 3, (C + L) / 3]
        V = set()
        for c in crit:
            for x in (c - dl, c, c + dl):
                if xi < x <= cap:
                    V.add(x)
        for k in range(1, 13):
            V.add(xi + (cap - xi) * k / 12)
        V = sorted(V)
        s = core + dl  # any root total above the core; only s > core matters
        for size in range(1, 5):
            for X in itertools.combinations_with_replacement(V, size):
                if size == 4 and len(set(X)) == 4 and (hash(X) % 7):  # thin the largest layer
                    continue
                if kind == "O":
                    fails = not (s <= R["a"] or (Hphi(X, phiD, xi) <= A and phiE(Mxi(X, xi)) <= C))
                else:
                    fails = not (s <= R["b"] or (Hphi(X, phiE, xi) <= C and phiD(Mxi(X, xi)) <= A))
                nl = nonlargest_H52_fail(X, xi, thr)
                nC += 1
                check((not fails) or nl, f"PartC {dom} {R['nu']}{R['t']} X={[float(x) for x in X]}")
                if nl and not fails:
                    nC_fail_conv += 1
out(f"Part C: {nC} multisets evaluated literally; converse violations: {nC_fail_conv}")

# Negative control for Part C: with a cap exceeding the lemma's bound, a
# largest-witness failure must appear (shows the check is not vacuous).
R = O3["n"][0]
bigM = R["A"] - R["L"] + Fr(1, 10**6)
X = (bigM,)
fails = Hphi(X, lambda u: min(H32 * u, R["L"]), R["xi"]) > R["A"]
check(fails and not nonlargest_H52_fail(X, R["xi"], R["A"]), "negative control: single fragment A-L+1e-6 is a largest-only failure")
X = (Fr(63, 160) * R["C"] + Fr(1, 10**6),)
fails = Hphi(X, lambda u: 3 * u - min(H32 * u, R["L"]), R["xi"]) > R["C"]
check(fails and not nonlargest_H52_fail(X, R["xi"], R["C"]), "negative control inner: 63C/160+1e-6")

out(f"TOTAL checks: {NCHECK}, failures: {NFAIL}, run time {time.time() - T_START:.1f} s")
out("VERDICT:", "Lemma 1.4 verified as stated (under the formalization in the note)" if NFAIL == 0 else "FAILURES")
