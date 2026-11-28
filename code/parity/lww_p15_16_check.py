#!/usr/bin/python3
"""Toy checks for LWW (arXiv:2610.20242v2), Section 4.1, pp. 15-16, (4.1)-(4.8): the reduction of the Type II
sum T_3(F) to Q_Y.

Run: /usr/bin/python3 -I code/parity/lww_p15_16_check.py
Route card: notes/parity-attempts/2026-11-28-lww-p15-16-reduction.md

Toy parameters only: tiny odd "prime sets" P_i (pairwise disjoint), arbitrary rational V_i > 0 and rho in (0,1),
Gaussian-rational coefficients alpha_m, beta_n.  Everything is exact (Fractions); nothing asymptotic is tested.

 (A) pointwise W-expansion (p. 15): for every n <= NMAX,
        mu(n) W(n) = (-1)^K prod V_i^{-1} sum_{p_i in P_i, a = p_1..p_K | n, (a, n/a) = 1} mu(n/a) rho^{omega(n/a)},
     with W as in (2.13) and omega = sum_i omega_i.                                                   exact
 (B) T(M,N) of (4.3) = the (a,h)=1 expansion of p. 15 (exact); the dropped part D (terms with (a,h) > 1) has
     every term with p_i^2 | mn+2 for some i, and obeys the 'trivial' bound of the card (per m at most N/p^2 + 1
     values of n with p^2 | mn+2; tuple count <= prod_{j != i} max omega_j).                          exact
 (C) dyadic partition of unity eta(t) = chi(t) - chi(t/2), chi piecewise linear (rational): sum_l eta(a/2^l) = 1
     on A; T(M,N) + D = sum_l T_{2^l} exactly ((4.5) without its error term, which is D); on supp,
     Y <= a <= 4Y and h <= (4X+2)/Y.                                                                  exact
 (D) (4.7): first line of Q_Y (sum over h of |.|^2) = second line (literal sum over a, b, m, n, r, s with
     (mn+2)/a = (rs+2)/b in N*, summand alpha_m conj(alpha_r) beta_n conj(beta_s)).                   exact
 (E) (4.6): |T_Y|^2 <= H_Y Q_Y with H_Y = floor((4X+2)/Y) (Cauchy-Schwarz over h, |mu(h) rho^omega(h)| <= 1),
     for the true coefficients and for the extremal-type choice c_h = 1.                               exact
 (F) bookkeeping of (4.4): each (m, n) with m > U, n > V and psi(mn/x) != 0 lies in exactly one dyadic box
     (U 2^j, U 2^{j+1}] x (V 2^k, V 2^{k+1}], and every box meeting supp psi has MN in [(1-e)x/4, (2+e)x);
     elementary short-interval divisor bound sum_{y<k<=y+H} tau(k) <= 2 sum_{d <= sqrt(y+H)} (H/d + 1).  sanity
NOT tested: the Mellin bounds (4.2), any analytic size, Prop. 4.2 itself.
Negative controls are marked NEG and must FAIL.
"""
import math, random, time, itertools
from fractions import Fraction as Fr

T0 = time.time()
random.seed(20261128)
RESULTS = []


def report(name, kind, failures, total, detail=""):
    ok = (failures == 0) if kind == "POS" else (failures > 0)
    RESULTS.append((name, kind, ok))
    tag = "ok" if ok else "UNEXPECTED"
    print(f"[{kind}] {name}: {failures} failures / {total} cases {detail} -> {tag}")


class G:
    """Gaussian rationals."""
    __slots__ = ("re", "im")

    def __init__(self, re, im=0):
        self.re, self.im = Fr(re), Fr(im)

    def __add__(self, o):
        o = o if isinstance(o, G) else G(o)
        return G(self.re + o.re, self.im + o.im)

    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, G) else G(o)
        return G(self.re - o.re, self.im - o.im)

    def __mul__(self, o):
        o = o if isinstance(o, G) else G(o)
        return G(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    __rmul__ = __mul__

    def conj(self):
        return G(self.re, -self.im)

    def abs2(self):
        return self.re * self.re + self.im * self.im

    def __eq__(self, o):
        o = o if isinstance(o, G) else G(o)
        return self.re == o.re and self.im == o.im


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def mu(n):
    f = factor(n)
    return 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)


def tau(n):
    r = 1
    for e in factor(n).values():
        r *= e + 1
    return r


class Toy:
    def __init__(self, name, Ps, rho, M, N):
        self.name, self.Ps, self.K, self.rho, self.M, self.N = name, Ps, len(Ps), Fr(rho), M, N
        self.V = [sum(Fr(1, p) for p in P) for P in Ps]  # V_i := sum 1/p (any positive rational would do)
        self.invV = Fr(1)
        for v in self.V:
            self.invV /= v
        self.allp = set(itertools.chain(*Ps))
        self.tuples = list(itertools.product(*Ps))
        self.ms = range(M + 1, 2 * M + 1)
        self.ns = range(N + 1, 2 * N + 1)
        self.X = M * N
        rnd = lambda: G(Fr(random.randint(-9, 9), 7), Fr(random.randint(-9, 9), 5))
        self.alpha = {m: rnd() for m in self.ms}
        self.beta = {n: rnd() for n in self.ns}

    def omega_i(self, n, i):
        return sum(1 for p in self.Ps[i] if n % p == 0)

    def omega(self, n):
        return sum(1 for p in self.allp if n % p == 0)

    def W(self, n):
        w = Fr(1)
        for i in range(self.K):
            oi = self.omega_i(n, i)
            if oi == 0:
                return Fr(0)
            w *= oi * self.rho ** (oi - 1) / self.V[i]
        return w

    def prod(self, t):
        a = 1
        for p in t:
            a *= p
        return a


def chi(t):
    return min(max(t - 1, Fr(0)), Fr(1))


def eta(t):
    return chi(t) - chi(t / 2)


TOYS = [
    Toy("K=1 P1={3,5,7}", [[3, 5, 7]], Fr(1, 2), 14, 17),
    Toy("K=2 P1={3,5},P2={7,11}", [[3, 5], [7, 11]], Fr(2, 3), 12, 15),
    Toy("K=3 {3},{5,13},{7}", [[3], [5, 13], [7]], Fr(1, 3), 18, 25),
]

# ---------------------------------------------------------------- (A)
for toy in TOYS:
    fails = tot = neg = 0
    for n in range(1, 3001):
        lhs = mu(n) * toy.W(n)
        rhs = Fr(0)
        rhs_nocop = Fr(0)
        for t in toy.tuples:
            a = toy.prod(t)
            if n % a:
                continue
            h = n // a
            term = mu(h) * toy.rho ** toy.omega(h)
            rhs_nocop += term
            if math.gcd(a, h) == 1:
                rhs += term
        rhs *= (-1) ** toy.K * toy.invV
        rhs_nocop *= (-1) ** toy.K * toy.invV
        tot += 1
        fails += lhs != rhs
        neg += lhs != rhs_nocop
    report(f"(A) mu(n)W(n) = (a,h)=1 expansion, n<=3000, {toy.name}", "POS", fails, tot)
    report(f"(A) NEG same identity with (a,h)=1 dropped, {toy.name}", "NEG", neg, tot)

# ---------------------------------------------------------------- (B), (C), (D), (E)
for toy in TOYS:
    K, X = toy.K, toy.X
    # (4.3) directly
    T_direct = G(0)
    for m in toy.ms:
        for n in toy.ns:
            k = m * n + 2
            T_direct += toy.alpha[m] * toy.beta[n] * (mu(k) * toy.W(k))
    # expansion, split by coprimality; also per-(Y) pieces and per-h vectors
    T_cop, D = G(0), G(0)
    bad_terms = bad_fail = 0
    Ylist = sorted({2 ** l for t in toy.tuples for l in range(0, 20) if eta(Fr(toy.prod(t), 2 ** l)) != 0})
    S = {Y: {} for Y in Ylist}  # S[Y][h] = sum_{tuples} eta(a/Y) sum_{mn+2=ah} alpha beta  (no V factor)
    supp_fail = supp_tot = 0
    for m in toy.ms:
        for n in toy.ns:
            k = m * n + 2
            ab = toy.alpha[m] * toy.beta[n]
            for t in toy.tuples:
                a = toy.prod(t)
                if k % a:
                    continue
                h = k // a
                c = ab * (mu(h) * toy.rho ** toy.omega(h))
                if math.gcd(a, h) == 1:
                    T_cop += c
                else:
                    D += c
                    bad_terms += 1
                    if not any(k % (p * p) == 0 for p in t):
                        bad_fail += 1
                for Y in Ylist:
                    e = eta(Fr(a, Y))
                    if e != 0:
                        supp_tot += 1
                        if not (Y <= a <= 4 * Y and h <= Fr(4 * X + 2, Y)):
                            supp_fail += 1
                        S[Y][h] = S[Y].get(h, G(0)) + ab * e
    sgn = (-1) ** K
    T_cop_n = T_cop * (sgn * toy.invV)
    D_n = D * (sgn * toy.invV)
    report(f"(B) (4.3) T(M,N) = (a,h)=1 expansion, {toy.name}", "POS", int(not (T_direct == T_cop_n)), 1)
    report(f"(B) NEG T(M,N) = expansion with (a,h)=1 simply dropped, {toy.name}", "NEG",
           int(not (T_direct == T_cop_n + D_n)), 1, f"(|D|^2 = {float(D_n.abs2()):.3g}, {bad_terms} bad terms)")
    report(f"(B) every (a,h)>1 term has p_i^2 | mn+2, {toy.name}", "POS", bad_fail, bad_terms)
    # trivial bound of the card
    amax = max(math.sqrt(float(v.abs2())) for v in toy.alpha.values())
    bmax = max(math.sqrt(float(v.abs2())) for v in toy.beta.values())
    kvals = [m * n + 2 for m in toy.ms for n in toy.ns]
    om_max = [max(toy.omega_i(k, i) for k in kvals) for i in range(K)]
    cnt_fail = cnt_tot = 0
    bound = 0.0
    for i in range(K):
        others = 1
        for j in range(K):
            if j != i:
                others *= om_max[j]
        for p in toy.Ps[i]:
            tot_p = 0
            for m in toy.ms:
                c = sum(1 for n in toy.ns if (m * n + 2) % (p * p) == 0)
                cnt_tot += 1
                if c > toy.N / (p * p) + 1 or (m % p == 0 and c > 0):
                    cnt_fail += 1
                tot_p += c
            bound += others * tot_p
    bound *= float(toy.invV) * amax * bmax
    report(f"(B) per m, #{{n: p^2 | mn+2}} <= N/p^2+1 (0 if p|m), {toy.name}", "POS", cnt_fail, cnt_tot)
    report(f"(B) |D| <= trivial bound, {toy.name}", "POS", int(math.sqrt(float(D_n.abs2())) > bound + 1e-12), 1,
           f"(|D| = {math.sqrt(float(D_n.abs2())):.3g} <= {bound:.3g})")
    # (C)
    pu_fail = 0
    for t in toy.tuples:
        a = toy.prod(t)
        s = sum(eta(Fr(a) / Fr(2) ** l) for l in range(-5, 30))
        pu_fail += s != 1
    report(f"(C) sum_l eta(a/2^l) = 1 on A, {toy.name}", "POS", pu_fail, len(toy.tuples))
    TY = {}
    for Y in Ylist:
        acc = G(0)
        for h, v in S[Y].items():
            acc += v * (mu(h) * toy.rho ** toy.omega(h))
        TY[Y] = acc * (sgn * toy.invV)
    tot_TY = G(0)
    for Y in Ylist:
        tot_TY += TY[Y]
    report(f"(C) T(M,N) + D = sum_Y T_Y (4.5), {toy.name}", "POS", int(not (tot_TY == T_direct + D_n)), 1,
           f"({len(Ylist)} values of Y)")
    report(f"(C) on supp eta(a/Y): Y<=a<=4Y and h<=(4X+2)/Y, {toy.name}", "POS", supp_fail, supp_tot)
    # (D) Q_Y two lines
    invV2 = toy.invV * toy.invV
    d_fail = d_neg = 0
    QY = {}
    pairs = [(m, n) for m in toy.ms for n in toy.ns]
    for Y in Ylist:
        line1 = Fr(0)
        for h, v in S[Y].items():
            line1 += v.abs2()
        line1 *= invV2
        QY[Y] = line1
        A_Y = [(toy.prod(t), eta(Fr(toy.prod(t), Y))) for t in toy.tuples]
        A_Y = [(a, e) for a, e in A_Y if e != 0]
        line2, line2_noconj = G(0), G(0)
        for a, ea in A_Y:
            la = [(m, n, (m * n + 2) // a) for (m, n) in pairs if (m * n + 2) % a == 0]
            for b, eb in A_Y:
                lb = [(r, s, (r * s + 2) // b) for (r, s) in pairs if (r * s + 2) % b == 0]
                for (m, n, h1) in la:
                    for (r, s, h2) in lb:
                        if Fr(m * n + 2, a) == Fr(r * s + 2, b) and h1 >= 1:
                            ee = ea * eb
                            line2 += toy.alpha[m] * toy.alpha[r].conj() * toy.beta[n] * toy.beta[s].conj() * ee
                            line2_noconj += toy.alpha[m] * toy.alpha[r] * toy.beta[n] * toy.beta[s] * ee
        line2 = line2 * invV2
        line2_noconj = line2_noconj * invV2
        d_fail += not (line2 == G(line1))
        d_neg += not (line2_noconj == G(line1))
    report(f"(D) (4.7) line 1 = line 2 (with conjugates), {toy.name}", "POS", d_fail, len(Ylist))
    report(f"(D) NEG (4.7) line 2 without conjugates, {toy.name}", "NEG", d_neg, len(Ylist))
    # (E) Cauchy-Schwarz
    e_fail = e_neg = 0
    for Y in Ylist:
        HY = (4 * X + 2) // Y
        e_fail += TY[Y].abs2() > HY * QY[Y]
        ones = G(0)
        for v in S[Y].values():
            ones += v
        T1 = ones * toy.invV
        e_fail += T1.abs2() > HY * QY[Y]
        # NEG: (4.6) without the factor X/Y, with real positive coefficients and c_h = 1
        Spos = {}
        for (m, n) in pairs:
            for t in toy.tuples:
                a = toy.prod(t)
                e = eta(Fr(a, Y))
                if e != 0 and (m * n + 2) % a == 0:
                    h = (m * n + 2) // a
                    Spos[h] = Spos.get(h, Fr(0)) + e
        tp = sum(Spos.values()) * toy.invV
        qp = sum(v * v for v in Spos.values()) * invV2
        e_neg += tp * tp > qp
    report(f"(E) (4.6) |T_Y|^2 <= floor((4X+2)/Y) Q_Y (true c_h and c_h=1), {toy.name}", "POS", e_fail,
           2 * len(Ylist))
    report(f"(E) NEG |T_Y|^2 <= Q_Y (factor X/Y dropped; alpha=beta=1, c_h=1), {toy.name}", "NEG", e_neg,
           len(Ylist))

# ---------------------------------------------------------------- (F)
f_fail = f_tot = 0
for (x, U, eps) in [(10 ** 4, 6, Fr(1, 20)), (3 * 10 ** 4, 8, Fr(1, 50)), (10 ** 5, 10, Fr(1, 10))]:
    boxes = set()
    for m in range(U + 1, int(x * 3) // (U + 1) + 2):
        lo = max(U + 1, math.floor((1 - eps) * x / m))
        hi = math.ceil((2 + eps) * x / m)
        for n in range(lo, hi + 1):
            if not ((1 - eps) * x < m * n < (2 + eps) * x):
                continue
            f_tot += 1
            js = [j for j in range(60) if U * 2 ** j < m <= U * 2 ** (j + 1)]
            ks = [k for k in range(60) if U * 2 ** k < n <= U * 2 ** (k + 1)]
            if len(js) != 1 or len(ks) != 1:
                f_fail += 1
                continue
            boxes.add((js[0], ks[0]))
    for (j, k) in boxes:
        MN = U * 2 ** j * U * 2 ** k
        f_tot += 1
        if not ((1 - eps) * x / 4 <= MN < (2 + eps) * x):
            f_fail += 1
report("(F) dyadic boxes: unique box per pair; MN in [(1-e)x/4,(2+e)x) (sanity)", "POS", f_fail, f_tot)
g_fail = g_tot = 0
for _ in range(300):
    y = random.randint(10, 20000)
    H = random.randint(1, 500)
    lhs = sum(tau(k) for k in range(y + 1, y + H + 1))
    rhs = 2 * sum(H / d + 1 for d in range(1, math.isqrt(y + H) + 1))
    g_tot += 1
    g_fail += lhs > rhs
report("(F) short-interval divisor bound (sanity)", "POS", g_fail, g_tot)

# ---------------------------------------------------------------- summary
pos = [r for r in RESULTS if r[1] == "POS"]
neg = [r for r in RESULTS if r[1] == "NEG"]
bad = [r[0] for r in RESULTS if not r[2]]
print("== SUMMARY")
print(f"positive checks: {len(pos)}, failing: {sum(1 for r in pos if not r[2])}")
print(f"negative controls: {len(neg)}, failing as they must: {sum(1 for r in neg if r[2])}")
print(f"unexpected outcomes: {len(bad)} {bad}")
print(f"wall time {time.time() - T0:.1f} s")
