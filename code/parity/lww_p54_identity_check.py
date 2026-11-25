#!/usr/bin/env python3
"""Exact finite checks of the identity in LWW (arXiv:2610.20242v2) Section 4.7, pp. 53-54:

    M_R(u,v,r) = prod_p b'_p * < b, G_0 O_0 G_1 ... O_{2R-1} G_{2R} b >_distinct.

Pure Python, fractions.Fraction only. Run: /usr/bin/python3 -I lww_p54_identity_check.py

(a) A_p = empty expansion ("least and greatest selected indices"), p. 53-54.
(b) prefix / suffix identities, p. 54.
(c) per-prime "life history" model of G_j, O_j for one prime p with a prescribed occupancy set
    A_p: operator sum == V^{-kappa_p} * (4.137) / b'_p.
(d) a global toy model (K = 1, J + 1 = 2, primes {2,3,5} or {2,3,5,7}, R = 1, 2): the left side is
    built from (4.100)/(4.101)/(4.111) (rho-powers, 1/V per step, 1/(p+1) average over lines); the
    right side is a literal enumeration of G_0 O_0 ... G_{2R} acting on states (tuple, ordered list m,
    set of already-selected primes) with the stated weights, theta-damping and distinctness.
    Geometric kernel factors (z-vectors, D | det, psi, eta, M_1 integral) are common to both sides
    and are NOT modelled; lines [z_j]_p are drawn at random in P^1(F_p) = {0..p}.
    Negative controls: drop distinctness / allow a pair appended in O_j to supply p'_i in O_j.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import random

rng = random.Random(20261125)


def rfrac(lo=1, hi=9, den=11):
    return F(rng.randint(lo, hi), rng.randint(2, den))


def prod(xs):
    r = F(1)
    for x in xs:
        r *= x
    return r


# ---------------------------------------------------------------- (a), (b)
def check_a(trials=300):
    bad = 0
    for _ in range(trials):
        p = rng.choice([2, 3, 5, 7])
        R = rng.randint(1, 3)
        n = 2 * R + 1
        eta = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(n)]
        z = [rng.randint(0, p) for _ in range(n)]
        lhs = F(1, p + 1) * sum(prod(1 - eta[j] * (l == z[j]) for j in range(n)) for l in range(p + 1))
        bp = 1 - sum(eta) / (p + 1)
        rhs = bp + F(1, p + 1) * sum(
            eta[a] * eta[c] * (z[a] == z[c]) * prod(1 - eta[j] * (z[j] == z[a]) for j in range(a + 1, c))
            for a in range(n) for c in range(a + 1, n))
        bad += lhs != rhs
    return bad


def check_b(trials=300):
    bad = 0
    for _ in range(trials):
        n = rng.randint(0, 7)
        x = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(n)]
        # prefix: prod_{j<a}(1-x_j) = 1 - sum_{h<a} x_h prod_{h<j<a}(1-x_j), a = n
        pre = 1 - sum(x[h] * prod(1 - x[j] for j in range(h + 1, n)) for h in range(n))
        # suffix: prod_{j>c}(1-x_j) = 1 - sum_{h>c} x_h prod_{c<j<h}(1-x_j), c = -1
        suf = 1 - sum(x[h] * prod(1 - x[j] for j in range(0, h)) for h in range(n))
        bad += (pre != prod(1 - t for t in x)) + (suf != prod(1 - t for t in x))
    return bad


# ---------------------------------------------------------------- (c) one prime
def single_prime_operator(A, z, eta, q, V, nu, theta):
    """Sum over life histories of one prime p (group i) whose tuple occupancy set is A.

    States between operators: 'fresh' (never selected), 'T' (in tuple), ('m', line), 'dead'.
    Rules exactly as p. 48 / (4.122) / p. 54; the prime is selected at most once.
    """
    n = len(z)
    # state before G_0: in tuple iff 0 in A (weight nu from the measure of b), else fresh
    states = {('T',) if 0 in A else ('fresh',): (nu if 0 in A else F(1))}
    for j in range(n):
        # ---- G_j at z_j
        new = {}
        for s, w in states.items():
            if s[0] == 'fresh':
                new[s] = new.get(s, 0) + w                       # not appended
                if j not in A:
                    t = ('m', z[j])
                    new[t] = new.get(t, 0) + w * (-eta[j] * V * nu / theta)   # appended (l=1, 1/1!)
            elif s[0] == 'm':
                if s[1] == z[j]:
                    new[s] = new.get(s, 0) + w * q[j] / theta ** 2           # retained, matching
                    new[('dead',)] = new.get(('dead',), 0) + w * (-eta[j] / theta)  # removed
                else:
                    new[s] = new.get(s, 0) + w
            else:
                new[s] = new.get(s, 0) + w
        states = new
        if j == n - 1:
            break
        # ---- O_j : z_j -> z_{j+1}
        new = {}
        for s, w in states.items():
            hs = 1 if (s[0] == 'm' and s[1] == z[j]) else 0
            outs = []
            if s[0] == 'T':
                if j + 1 in A:                       # shared entry: retained, needs [z]_p=[z']_p
                    if z[j] == z[j + 1]:
                        outs.append((('T',), F(1)))
                else:                                 # departing entry: i in S (append) or discard
                    outs.append((('m', z[j]), F(1)))
                    outs.append((('dead',), F(1)))
            elif s[0] == 'fresh':
                if j + 1 in A:
                    outs.append((('T',), nu))         # summed with measure nu
                else:
                    outs.append((s, F(1)))
            elif s[0] == 'm':
                if j + 1 in A:
                    if s[1] == z[j + 1]:
                        outs.append((('T',), 1 / V))  # moved from m_i (present before the op)
                else:
                    outs.append((s, F(1)))
            else:  # dead
                if j + 1 not in A:
                    outs.append((s, F(1)))
            for t, c in outs:
                ht = 1 if (t[0] == 'm' and t[1] == z[j + 1]) else 0
                new[t] = new.get(t, 0) + w * c * theta ** (hs + ht)
        states = new
    # final b: m empty -> exclude ('m',..); tuple at z_{2R} fine
    return sum(w for s, w in states.items() if s[0] != 'm')


def kappa(A):
    A = sorted(A)
    return sum(1 for k, a in enumerate(A) if k == 0 or A[k - 1] != a - 1)


def check_c(trials=400):
    bad = 0
    for _ in range(trials):
        p = rng.choice([2, 3, 5])
        R = rng.randint(1, 3)
        n = 2 * R + 1
        eta = [F(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(n)]
        q = [1 - e for e in eta]
        V = rfrac()
        theta = rfrac(1, 5, 7)
        # bias lines toward repeats so indicator terms are exercised
        z = [rng.randint(0, min(p, 1)) if rng.random() < .6 else rng.randint(0, p) for _ in range(n)]
        A = {j for j in range(n) if rng.random() < .45}
        bp = 1 - sum(eta) / (p + 1)
        if bp == 0:
            continue
        nu = 1 / (V * (p + 1) * bp)
        op = single_prime_operator(A, z, eta, q, V, nu, theta)
        f4137 = F(1, p + 1) * sum(
            prod(F(int(l == z[j])) for j in A) * prod(1 - eta[j] * (l == z[j]) for j in range(n) if j not in A)
            for l in range(p + 1))
        target = V ** (-kappa(A)) * f4137 / bp if A else f4137 / bp
        bad += op != target
    return bad


# ---------------------------------------------------------------- (d) global toy model
def mr_side(P, z, R, rho_sqrt, V):
    """LHS from (4.93),(4.100),(4.101),(4.111) for K=1, J+1=2, tuples as 2-sets; 1/V per entry."""
    n = 2 * R + 1
    rho = rho_sqrt ** 2
    q = [rho_sqrt if j in (0, n - 1) else rho for j in range(n)]
    total = F(0)
    sets = [frozenset(c) for c in combinations(P, 2)]

    def rec(seq):
        nonlocal total
        if len(seq) == n:
            w = V ** (-(2 + 2 * R)) * rho ** (-2 * 2 * R)     # V^{-(J+1)} * V^{-1} per step; rho^{-K(J+1)} per kernel
            for p in P:
                s = F(0)
                for l in range(p + 1):
                    t = F(1)
                    for j in range(n):
                        if p in seq[j] and l != z[j][p]:
                            t = F(0)
                            break
                        if l == z[j][p]:
                            t *= q[j]
                    s += t
                w *= s / (p + 1)
            total += w
            return
        T = seq[-1]
        for d in T:
            for new in P:
                if new not in T:
                    rec(seq + [(T - {d}) | {new}])
    for T0 in sets:
        rec([T0])
    return total


def op_side(P, z, R, eta, q, V, theta, distinct=True, same_op_supply=False):
    n = 2 * R + 1
    bp = {p: 1 - sum(eta) / (p + 1) for p in P}
    nu = {p: 1 / (V * (p + 1) * bp[p]) for p in P}
    # state: (T frozenset, m tuple of (p,line) ordered, selected frozenset)
    states = {}
    for T0 in combinations(P, 2):
        s = (frozenset(T0), (), frozenset(T0))
        states[s] = states.get(s, 0) + nu[T0[0]] * nu[T0[1]]
    for j in range(n):
        # G_j
        new = {}
        for (T, m, sel), w in states.items():
            match = [k for k, (p, l) in enumerate(m) if l == z[j][p]]
            for r in range(len(match) + 1):
                for rem in combinations(match, r):
                    w1 = w * (-eta[j] / theta) ** r * (q[j] / theta ** 2) ** (len(match) - r)
                    m1 = tuple(c for k, c in enumerate(m) if k not in rem)
                    avail = [p for p in P if (p not in sel) or not distinct]
                    for l in range(len(avail) + 1 if distinct else 3):   # no-distinctness control: l <= 2
                        for app in permutations(avail, l) if distinct else _tuples(avail, l):
                            w2 = w1 * F(1, _fact(l)) * prod(-eta[j] * V * nu[p] / theta for p in app)
                            m2 = m1 + tuple((p, z[j][p]) for p in app)
                            s2 = (T, m2, sel | frozenset(app))
                            new[s2] = new.get(s2, 0) + w2
        states = {s: w for s, w in new.items() if w != 0}
        if j == n - 1:
            break
        # O_j
        new = {}
        for (T, m, sel), w in states.items():
            hs = sum(1 for (p, l) in m if l == z[j][p])
            for d in T:
                (sh,) = tuple(T - {d})
                if z[j][sh] != z[j + 1][sh]:
                    continue                                   # [z]_p = [z']_p for p | D
                for app_dep in (True, False):                  # i in S or not
                    mA = m + ((d, z[j][d]),) if app_dep else m
                    # supply from m: only coordinates present before (indices < len(m))
                    lim = len(mA) if same_op_supply else len(m)
                    for k in range(lim):
                        p, l = mA[k]
                        if l == z[j + 1][p] and p != sh and (same_op_supply or p != d):
                            m2 = mA[:k] + mA[k + 1:]
                            ht = sum(1 for (pp, ll) in m2 if ll == z[j + 1][pp])
                            s2 = (frozenset({sh, p}), m2, sel)
                            new[s2] = new.get(s2, 0) + w * (1 / V) * theta ** (hs + ht)
                    for p in P:
                        if p in (sh, d):
                            continue
                        if distinct and p in sel:
                            continue
                        ht = sum(1 for (pp, ll) in mA if ll == z[j + 1][pp])
                        s2 = (frozenset({sh, p}), mA, sel | {p})
                        new[s2] = new.get(s2, 0) + w * nu[p] * theta ** (hs + ht)
        states = {s: w for s, w in new.items() if w != 0}
    return sum(w for (T, m, sel), w in states.items() if len(m) == 0), bp


def _fact(l):
    r = 1
    for k in range(2, l + 1):
        r *= k
    return r


def _tuples(avail, l):
    if l == 0:
        yield ()
        return
    for t in _tuples(avail, l - 1):
        for p in avail:
            yield t + (p,)


def check_d(cases):
    out = []
    for (P, R, seed) in cases:
        r2 = random.Random(seed)
        n = 2 * R + 1
        z = [{p: (0 if r2.random() < .75 else r2.randint(0, p)) for p in P} for _ in range(n)]
        z[n - 1] = dict(z[0])          # z_{2R} = z_0 = (1,0)^T
        while True:   # avoid the degenerate parameters with some b'_p = 0 (excluded in LWW: b'_p > 0)
            rho_sqrt = F(r2.randint(2, 8), 9)
            if all((p + 1) != 2 * (1 - rho_sqrt) + (n - 2) * (1 - rho_sqrt ** 2) for p in P):
                break
        rho = rho_sqrt ** 2
        q = [rho_sqrt if j in (0, n - 1) else rho for j in range(n)]
        eta = [1 - x for x in q]
        V = F(r2.randint(3, 9), 10)
        lhs = mr_side(P, z, R, rho_sqrt, V)
        res = {}
        for th in (F(9, 10), F(2, 3)):
            o, bp = op_side(P, z, R, eta, q, V, th)
            res[th] = prod(bp[p] for p in P) * o
        o_nd, _ = op_side(P, z, R, eta, q, V, F(9, 10), distinct=False) if (len(P) <= 3 and R == 1) else (None, None)
        o_so, _ = op_side(P, z, R, eta, q, V, F(9, 10), same_op_supply=True)
        nd = (prod(bp[p] for p in P) * o_nd == lhs) if o_nd is not None else 'skipped'
        so = prod(bp[p] for p in P) * o_so == lhs
        out.append((P, R, seed, lhs, res, nd, so))
    return out


if __name__ == '__main__':
    print('LWW p.53-54 identity check (exact rational arithmetic)')
    print(flush=True); print('(a) A_p empty expansion, 300 random cases: failures =', check_a())
    print('(b) prefix/suffix identities, 300 random cases (x2): failures =', check_b())
    print('(c) single-prime operator model vs V^-kappa (4.137)/b\'_p, ~400 cases: failures =', check_c())
    cases = [((2, 3, 5), 1, s) for s in range(1, 7)] + [((2, 3, 5), 2, s) for s in range(7, 11)] + \
            [((2, 3, 5, 7), 1, 11), ((2, 3, 5, 7), 1, 12), ((2, 3, 5, 7), 2, 13)]
    print('(d) global toy model, K=1, J+1=2: M_R(toy) vs prod b\'_p * <b, G0 O0 ... G2R b>_distinct')
    for (P, R, seed, lhs, res, nd, so) in (r for c in cases for r in check_d([c])):
        ok = all(v == lhs for v in res.values())
        print(f'  P={P} R={R} seed={seed}: M_R={lhs}  equal(theta=9/10,2/3)={ok}  '
              f'[neg. control no-distinctness equal={nd}; same-op supply equal={so}]', flush=True)
