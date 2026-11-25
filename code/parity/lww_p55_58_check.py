#!/usr/bin/env python3
"""Finite / exact checks for LWW (arXiv:2610.20242v2) pp. 55-58: E_mem, (4.138)-(4.147), and the close of
the proof of Prop. 4.6 (p. 58). Companion to notes/parity-attempts/2026-11-25-lww-p55-58-emem.md.

Run: /usr/bin/python3 -I lww_p55_58_check.py      (pure Python + fractions; sympy for exponent limits)

(A) (4.140) Moebius identity on the partition lattice, exhaustive for |B| <= 6, values in {1..4}, every
    B_act subset of B.  NEG: sign (-1)^{|C|} or weight |C|! instead of (|C|-1)!.
(B) (4.141): sum over collections of rank kappa of prod (|C|-1)! equals the unsigned Stirling number
    c(n, n-kappa) (exhaustive n <= 7), each collection uses <= 2 kappa indices, and c(n, n-kappa) <= n^{2kappa}
    for all n <= 150 (exact integers).  NEG: n^{kappa} in place of n^{2kappa}.
(C) E_mem, p. 55: single non-tuple prime, absolute weights with the inserted factor 2, literal DP over the
    G_j / O_j rules (theta-damping h_s, h_t, removal before append, empty m at both ends) == the printed
    sum, and the printed bound 2(2R+1)/((p+1)b'_p); telescoping <= 1.  Tuple prime: number of admissible
    histories for a given A_p == (a+1)(2R-c+1) <= (2R+2)^2.  NEG: drop the h_t damping factor; eta' > 1.
(D) (4.143) series bound (exact partial sums vs (x Delta)^s e^{x s_i}) and the removal/retention factor
    q_j/theta^2 + eta'_j/(theta v0) <= 1 for all j incl. q_0 = q_2R = sqrt(rho).
    NEG: theta^2 > rho only (instead of theta^2 > sqrt rho) breaks it at j = 0, 2R.
(E) p. 57 Phi^sym identity, exact.  NEG: non-symmetric F.
(G) exponent bookkeeping (sympy limits + exact linear algebra in the constants):
    (4.138), (4.144)-(4.145) with C_0 > 2(C_*+E_0+7), (4.147) with A = E_0+5, p. 58 (exp(-cL^{3/4}) << L^{-2RE_0}).
    NEG: C_0 = 2(C_*+E_0+3); R ~ L instead of L^{1/2} at p. 58.
"""
from fractions import Fraction as F
from itertools import combinations, product as iproduct, permutations
from math import factorial, comb
import random
import time

rng = random.Random(20261125)
T0 = time.time()


def prod(xs, one=1):
    r = one
    for x in xs:
        r *= x
    return r


def set_partitions(items):
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


# ------------------------------------------------------------------ (A) (4.140)
def collections(B):
    """Collections of disjoint subsets C of B with |C| >= 2 (= non-singleton blocks of partitions of B)."""
    out = []
    for part in set_partitions(B):
        out.append([tuple(c) for c in part if len(c) >= 2])
    return out


def check_A(weight):
    bad = tot = 0
    for n in range(0, 7):
        B = list(range(n))
        cols = collections(B)
        for k in range(n + 1):
            for Bact in combinations(B, k):
                for vals in iproduct(range(1, 5), repeat=k):
                    p = dict(zip(Bact, vals))
                    lhs = int(len(set(vals)) == k)
                    rhs = 0
                    for C0 in cols:
                        ok = all(all(a in p for a in C) and len({p[a] for a in C}) == 1 for C in C0)
                        if ok:
                            rhs += prod(weight(len(C)) for C in C0)
                    tot += 1
                    bad += lhs != rhs
    return tot, bad


# ------------------------------------------------------------------ (B) (4.141)
def stirling1_unsigned(nmax):
    c = [[0] * (nmax + 1) for _ in range(nmax + 1)]
    c[0][0] = 1
    for n in range(1, nmax + 1):
        for k in range(1, n + 1):
            c[n][k] = c[n - 1][k - 1] + (n - 1) * c[n - 1][k]
    return c


def check_B():
    c = stirling1_unsigned(150)
    bad_enum = bad_idx = 0
    for n in range(1, 8):
        by_rank = {}
        for C0 in collections(range(n)):
            kap = sum(len(C) - 1 for C in C0)
            by_rank[kap] = by_rank.get(kap, 0) + prod(factorial(len(C) - 1) for C in C0)
            if sum(len(C) for C in C0) > 2 * kap:
                bad_idx += 1
        for kap, s in by_rank.items():
            if s != c[n][n - kap]:
                bad_enum += 1
    bad_bound = bad_neg = 0
    neg_example = None
    for n in range(1, 151):
        for kap in range(0, n):
            v = c[n][n - kap]
            if v > n ** (2 * kap):
                bad_bound += 1
            if v > n ** kap:
                bad_neg += 1
                if neg_example is None:
                    neg_example = (n, kap, v, n ** kap)
    return bad_enum, bad_idx, bad_bound, bad_neg, neg_example


# ------------------------------------------------------------------ (C) E_mem per-prime factors
def params(R, rho_root, V, theta, p):
    q = [rho_root] + [rho_root ** 2] * (2 * R - 1) + [rho_root]  # q_0 = q_2R = sqrt(rho), else rho
    eta = [1 - x for x in q]
    bp = 1 - sum(eta) / (p + 1)
    if bp <= 0:  # LWW has b'_p > 0 for large x ((4.121)); degenerate toy parameters are skipped
        return q, eta, bp, None
    nu = 1 / (V * (p + 1) * bp)
    return q, eta, bp, nu


def dp_nontuple(R, z, q, eta, V, nu, theta, factor2=2, use_ht=True):
    """Literal DP for one prime in no prime tuple: states 'N' (never selected), ('M', line), 'X' (removed).
    G_j: remove (matching, pre-existing) or retain; then optional append (p, [z_j]) if never selected.
    O_j (j < 2R): theta^{h_s + h_t} for a pair in m (h_s: line == z_j, h_t: line == z_{j+1}).
    Absolute values of all weights, inserted factor `factor2` per G-appended coordinate."""
    st = {'N': F(1)}
    n = 2 * R + 1
    for j in range(n):
        new = {}

        def add(k, w):
            new[k] = new.get(k, 0) + w
        for s, w in st.items():
            if s == 'N':
                add('N', w)
                add(('M', z[j]), w * factor2 * eta[j] * V * nu / theta)  # append at G_j
            elif s == 'X':
                add('X', w)
            else:
                ell = s[1]
                if ell == z[j]:
                    add('X', w * eta[j] / theta)          # remove
                    add(s, w * q[j] / theta ** 2)         # retain, matching
                else:
                    add(s, w)                              # retain, not matching
        st = new
        if j < n - 1:  # O_j
            new = {}
            for s, w in st.items():
                if isinstance(s, tuple):
                    ell = s[1]
                    e = (ell == z[j]) + ((ell == z[j + 1]) if use_ht else 0)
                    w = w * theta ** e
                new[s] = new.get(s, 0) + w
            st = new
    return sum(w for s, w in st.items() if not isinstance(s, tuple))  # b: m empty at the end


def printed_nontuple(R, z, q, eta, bp, p):
    n = 2 * R + 1
    s = sum(eta[a] * eta[c] * (z[a] == z[c]) * prod((1 - eta[j] * (z[j] == z[a]) for j in range(a + 1, c)), F(1))
            for a in range(n) for c in range(a + 1, n))
    return 1 + F(2) / ((p + 1) * bp) * s, s


def check_C(trials=400):
    bad_eq = bad_bound = bad_tel = 0
    neg_ht = done = 0
    for _ in range(trials):
        p = rng.choice([2, 3, 5, 7, 11, 13])
        R = rng.randint(1, 4)
        r = F(rng.randint(1, 9), 10)          # sqrt(rho)
        theta = F(rng.randint(1, 9), 10)
        V = F(rng.randint(1, 20), 21)
        q, eta, bp, nu = params(R, r, V, theta, p)
        if bp <= 0:
            continue
        done += 1
        z = [rng.randint(0, p) for _ in range(2 * R + 1)]
        lhs = dp_nontuple(R, z, q, eta, V, nu, theta)
        rhs, s = printed_nontuple(R, z, q, eta, bp, p)
        bad_eq += lhs != rhs
        bad_bound += (rhs - 1) > F(2 * (2 * R + 1)) / ((p + 1) * bp)
        # telescoping: sum_{c>a} y_c prod_{a<j<c} (1-y_j) = 1 - prod (1-y_j) in [0,1]
        for a in range(2 * R + 1):
            y = [eta[j] * (z[j] == z[a]) for j in range(2 * R + 1)]
            t = sum(y[c] * prod((1 - y[j] for j in range(a + 1, c)), F(1)) for c in range(a + 1, 2 * R + 1))
            bad_tel += not (0 <= t <= 1 and t == 1 - prod((1 - y[j] for j in range(a + 1, 2 * R + 1)), F(1)))
        neg_ht += dp_nontuple(R, z, q, eta, V, nu, theta, use_ht=False) != rhs
    # NEG: eta' > 1 (not allowed in LWW since q_j in (0,1)) breaks "telescopes to at most 1"
    y = [F(3, 2)] * 5
    tel_neg = sum(y[c] * prod((1 - y[j] for j in range(1, c)), F(1)) for c in range(1, 4))  # a=0, c in 1..3 (odd count)
    return bad_eq, bad_bound, bad_tel, neg_ht, done, tel_neg


def tuple_histories(R, A, z):
    """Count admissible histories of one tuple prime with occupancy set A (indices where it sits in a tuple),
    under distinctness (selected once): states 'N', ('M', line), 'T', 'X'."""
    n = 2 * R + 1
    st = {('T' if 0 in A else 'N'): 1}
    for j in range(n):
        new = {}

        def add(k, w):
            new[k] = new.get(k, 0) + w
        for s, w in st.items():  # G_j
            if isinstance(s, tuple):
                if s[1] == z[j]:
                    add('X', w)
                add(s, w)
            elif s == 'N':
                add('N', w)
                add(('M', z[j]), w)
            else:
                add(s, w)
        st = new
        if j == n - 1:
            break
        new = {}
        for s, w in st.items():  # O_j : z_j -> z_{j+1}
            inA = (j + 1) in A
            if s == 'T':
                if inA:
                    add('T', w)
                else:
                    add(('M', z[j]), w)   # S option: append departing entry
                    add('X', w)           # discard
            elif s == 'N':
                add('T' if inA else 'N', w)   # fresh (nu-summed) entry, or stays unselected
            elif s == 'X':
                if not inA:
                    add('X', w)
            else:
                if inA:
                    if s[1] == z[j + 1]:
                        add('T', w)       # moved from m into the tuple
                else:
                    add(s, w)
        st = new
    return sum(w for s, w in st.items() if not isinstance(s, tuple))


def check_C_tuple():
    bad = bad_max = cases = 0
    for R in range(1, 5):
        n = 2 * R + 1
        for k in range(1, n + 1):
            for A in combinations(range(n), k):
                A = set(A)
                a, c = min(A), max(A)
                cnt = tuple_histories(R, A, [0] * n)
                cases += 1
                bad += cnt != (a + 1) * (2 * R - c + 1)
                bad_max += cnt > (2 * R + 2) ** 2
    return cases, bad, bad_max


# ------------------------------------------------------------------ (D) (4.143) and the G_j retention factor
def check_D(trials=300):
    from fractions import Fraction
    bad_series = bad_trunc = 0
    for _ in range(trials):
        x = Fraction(rng.randint(1, 40), 7)
        Dl = Fraction(1, rng.randint(2, 10 ** 6))
        si = Fraction(rng.randint(5, 15), 10)
        s = rng.randint(0, 4)
        hmax = s + rng.randint(0, 3)
        N = 120
        partial = sum(x ** l * Dl ** s * si ** (l - s) / factorial(l) for l in range(s, N))
        partial_h = sum(x ** l * Dl ** s * si ** (l - s) / factorial(l) for l in range(hmax, N))
        # e^{x s_i} > sum_{m < N} (x s_i)^m/m!  so (x Dl)^s e^{x s_i} > (x Dl)^s * that partial sum
        expo_partial = sum((x * si) ** m / factorial(m) for m in range(N))
        bad_series += not (partial <= (x * Dl) ** s * expo_partial)
        bad_trunc += not (partial_h <= partial)
    # retention/removal factor: q_j/theta^2 + eta'_j/(theta v0) <= 1 when sqrt(rho)/theta^2 + 1/(theta v0) < 1
    bad_ret = neg_ret = 0
    for _ in range(trials):
        r = F(rng.randint(1, 9), 10)                   # sqrt(rho)
        th2_min = r                                    # theta^2 > sqrt(rho)
        theta = None
        for _k in range(50):
            th = F(rng.randint(1, 99), 100)
            if th ** 2 > th2_min:
                theta = th
                break
        if theta is None:
            continue
        v0 = 1 / (theta * (1 - r / theta ** 2)) + 1   # makes sqrt(rho)/theta^2 + 1/(theta v0) < 1
        assert r / theta ** 2 + 1 / (theta * v0) < 1
        for qj in (r, r * r):
            bad_ret += qj / theta ** 2 + (1 - qj) / (theta * v0) > 1
    # NEG: theta^2 > rho only: rho = 1/4 (sqrt = 1/2), theta^2 = 3/10 > rho but < sqrt(rho)
    r, theta = F(1, 2), None
    theta2 = F(3, 10)
    neg_val = r / theta2  # q_0 / theta^2 alone already > 1
    neg_ret = neg_val > 1
    return bad_series, bad_trunc, bad_ret, neg_ret, neg_val


# ------------------------------------------------------------------ (E) Phi^sym, p. 57
def check_E(trials=40):
    bad = neg = 0
    for _ in range(trials):
        P = [0, 1, 2]
        l = rng.randint(1, 3)
        nu = {p: F(rng.randint(1, 9), 17) for p in P}
        Phi = {t: F(rng.randint(-9, 9), rng.randint(1, 9)) for t in iproduct(P, repeat=l)}
        Fs = {}
        Fn = {t: F(rng.randint(-9, 9), rng.randint(1, 9)) for t in iproduct(P, repeat=l)}
        for t in iproduct(P, repeat=l):
            key = tuple(sorted(t))
            if key not in Fs:
                Fs[key] = F(rng.randint(-9, 9), rng.randint(1, 9))
        perms = list(permutations(range(l)))

        def phisym(t):
            return sum(Phi[tuple(t[s] for s in sg)] for sg in perms) / factorial(l)

        def side(phi, FF):
            return sum(phi(t) * FF(t) * prod((nu[a] for a in t), F(1)) for t in iproduct(P, repeat=l)) / factorial(l)
        lhs = side(phisym, lambda t: Fs[tuple(sorted(t))])
        rhs = side(lambda t: Phi[t], lambda t: Fs[tuple(sorted(t))])
        bad += lhs != rhs
        if l >= 2:
            neg += side(phisym, lambda t: Fn[t]) != side(lambda t: Phi[t], lambda t: Fn[t])
    return bad, neg


# ------------------------------------------------------------------ (G) exponent bookkeeping
def check_G():
    import sympy as sp
    L = sp.symbols('L', positive=True)
    K, Cst, E0, c, beta, CK, d = sp.symbols('K C_star E_0 c beta C_K delta', positive=True)
    R = sp.sqrt(L) / 2
    J = L ** sp.Rational(1, 100)
    out = []
    # (4.138): log of 2^{-L^2+2KR} exp(c(L^0.71 + (J+R)log(2R+2) + R)) minus log L^{-2AR}, A = E0+5
    A = E0 + 5
    e138 = -(L ** 2 - 2 * K * R) * sp.log(2) + c * (L ** sp.Rational(71, 100) + (J + R) * sp.log(2 * R + 2) + R) \
        + 2 * A * R * sp.log(L)
    out.append(("(4.138) log(E_mem bound / L^{-2AR}) / L^2 -> ", sp.limit(e138 / L ** 2, L, sp.oo)))
    out.append(("(4.138) (L^0.71 + (J+R)log(2R+2) + R)/L^0.74 -> ",
                sp.limit((L ** sp.Rational(71, 100) + (J + R) * sp.log(2 * R + 2) + R) / L ** sp.Rational(74, 100), L, sp.oo)))
    # (4.144)-(4.145): with kappa_0 >= C0*2R log L/L^0.1 and ratio y = C|B|^2 Delta <= e^{-L^0.1/2}:
    # log(L^{C*(2R+1)} y^{kappa_0}) <= [C*(2R+1) - C0 R] log L.  Need margin vs -2R(E0+4) log L.
    Rs = sp.symbols('R', positive=True)
    C0 = 2 * (Cst + E0 + 7) + d
    margin = sp.expand(C0 * Rs - Cst * (2 * Rs + 1) - 2 * Rs * (E0 + 4))
    out.append(("(4.145) margin [C0 R - C*(2R+1) - 2R(E0+4)] with C0 = 2(C*+E0+7)+delta = ", margin))
    C0neg = 2 * (Cst + E0 + 3)
    margin_neg = sp.expand(C0neg * Rs - Cst * (2 * Rs + 1) - 2 * Rs * (E0 + 4))
    out.append(("NEG (4.145) margin with C0 = 2(C*+E0+3) = ", margin_neg))
    # (4.144) kappa_0/(2R) -> 0
    kappa0 = C0 * 2 * R * sp.log(L) / L ** sp.Rational(1, 10)
    out.append(("(4.144) kappa_0/(2R) -> ", sp.limit(kappa0 / (2 * R), L, sp.oo)))
    # (4.145) y = C_K |B|^2 Delta with |B| <= L^beta, Delta <= C_K e^{-L^0.1}: log y + L^0.1/2 -> -oo
    out.append(("(4.145) log(C|B|^2 Delta) + L^0.1/2 -> ",
                sp.limit(2 * sp.log(CK) + 2 * beta * sp.log(L) - L ** sp.Rational(1, 10) + L ** sp.Rational(1, 10) / 2, L, sp.oo)))
    # (4.147): log of the kappa-term + 2AR log L, maximised at kappa = kappa_0 (increasing in kappa):
    #   kappa(2 beta + 2A + 2C*) log L + (2R+1) log C_K + log kappa_0 ; divided by R log L -> 0  (the o(R))
    o_term = kappa0 * (2 * beta + 2 * A + 2 * Cst) * sp.log(L) + (2 * R + 1) * sp.log(CK) + sp.log(kappa0)
    out.append(("(4.147) o(R) term / (R log L) -> ", sp.limit(o_term / (R * sp.log(L)), L, sp.oo)))
    # then L^{-2AR+o(R)} vs L^{-2R(E0+4)}: exponent difference -2AR + 2R(E0+4) = -2R  (A = E0+5)
    out.append(("(4.147) -2AR + 2R(E0+4) with A=E0+5 = ", sp.simplify(-2 * A * Rs + 2 * Rs * (E0 + 4))))
    # p. 58: exp(-c L^{3/4}) << L^{-2 R E0} iff c L^{3/4} - 2 R E0 log L -> +oo
    out.append(("p.58 c L^{3/4} - 2R E0 log L -> ", sp.limit(c * L ** sp.Rational(3, 4) - 2 * R * E0 * sp.log(L), L, sp.oo)))
    out.append(("NEG p.58 with R = L/2: c L^{3/4} - 2R E0 log L -> ",
                sp.limit(c * L ** sp.Rational(3, 4) - L * E0 * sp.log(L), L, sp.oo)))
    # E_mem count: >L^2 coordinates at some time and <= 2KR from O_j  =>  >= ceil(L^2)+1-2KR from G_j
    return out


def main():
    print("LWW pp. 55-58 checks (exact rational arithmetic unless stated)\n")
    tot, bad = check_A(lambda m: (-1) ** (m - 1) * factorial(m - 1))
    print(f"(A) (4.140) Moebius identity, |B|<=6, values in 1..4, all B_act: {tot} cases, failures = {bad}")
    _, badn1 = check_A(lambda m: (-1) ** m * factorial(m - 1))
    _, badn2 = check_A(lambda m: (-1) ** (m - 1) * factorial(m))
    print(f"    NEG sign (-1)^|C|: failures = {badn1} (should be > 0);  NEG weight |C|!: failures = {badn2} (should be > 0)")
    be, bi, bb, bn, ex = check_B()
    print(f"(B) (4.141) rank-kappa sum == c(n,n-kappa) (n<=7): mismatches = {be}; collections using > 2kappa indices = {bi}")
    print(f"    c(n,n-kappa) <= n^(2kappa), n<=150, all kappa: failures = {bb}")
    print(f"    NEG n^kappa: failures = {bn} (should be > 0), first: n={ex[0]}, kappa={ex[1]}, c={ex[2]} > {ex[3]}")
    beq, bbd, btel, nht, tr, teln = check_C()
    print(f"(C) E_mem non-tuple prime: literal G/O DP (abs weights, factor 2) == printed sum: {tr} random cases, "
          f"failures = {beq}")
    print(f"    printed bound 2(2R+1)/((p+1)b'_p): failures = {bbd}; telescoping in [0,1]: failures = {btel}")
    print(f"    NEG drop h_t damping: mismatches = {nht} (should be > 0); NEG eta'=3/2: telescoped sum = {teln}, exceeds 1: {teln > 1}")
    cs, bc, bm = check_C_tuple()
    print(f"    tuple prime: #histories == (a+1)(2R-c+1), all A_p, R<=4: {cs} cases, failures = {bc}; > (2R+2)^2: {bm}")
    bs, bt, br, nr, nv = check_D()
    print(f"(D) (4.143) series <= (x Delta)^s e^(x s_i): failures = {bs}; restricting l >= h decreases: failures = {bt}")
    print(f"    retention/removal factor <= 1 for q_j in {{sqrt rho, rho}}: failures = {br}")
    print(f"    NEG theta^2 > rho only (rho=1/4, theta^2=3/10): q_0/theta^2 = {nv} > 1: {nr}")
    be2, ne2 = check_E()
    print(f"(E) Phi^sym identity, 40 exact cases: failures = {be2}; NEG non-symmetric F: mismatches = {ne2} (should be > 0)")
    print("(G) exponent bookkeeping (sympy):")
    for name, val in check_G():
        print(f"    {name}{val}")
    print(f"\nruntime {time.time() - T0:.1f} s")


if __name__ == "__main__":
    main()
