#!/usr/bin/env python3
"""Session 32 exploration: the "parity margin" LP for pattern-weight targets.

For a target family E on positions V = S u L (S: sieve positions, each prime with
density rho in the sieve weight; L: lambda-positions, each satisfying its sign
condition on exactly half of the weight), let P(E) be the convex hull of the
indicator vectors of E-free sets (down-closed polytope).  Compute

    rho_crit(E) = max { rho : (rho on S, 1/2 on L) in P(E) }.

If L is empty, rho_crit = t*(E) = max { t : (t,...,t) in P(E) }.
Parity criterion (Prop. prop:bipartite): blocked  iff  rho_crit >= 1/2.
Linear (first-moment) sieve criterion: a Maynard weight with per-position prime
density rho = theta*M_k/(2k) proves "some e in E holds" iff some inequality
a.x <= b valid on E-free sets has a.(rho,1/2) > b, i.e. (LP duality) iff
rho > rho_crit, i.e. theta*M_k > 2k*rho_crit.

LP dual (certificate):  rho_crit = min { max_I y(I) - (1/2) y(L) : y >= 0, y(S) = 1 }.
The primal and dual optima are solved with scipy/HiGHS in floating point and
then rationalised and verified EXACTLY with fractions.Fraction.
"""
import itertools, math
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog


def free_maximal(n, E):
    E = [frozenset(e) for e in E]
    free = [frozenset(I) for r in range(n + 1) for I in itertools.combinations(range(n), r)
            if not any(e <= frozenset(I) for e in E)]
    return [I for I in free if not any(I < J for J in free)]


def rho_crit(n, E, S, L=(), caps=None):
    """caps: dict position -> required marginal (default 1/2 for L)."""
    caps = dict(caps or {})
    for i in L:
        caps.setdefault(i, Fr(1, 2))
    S, Lc = list(S), sorted(caps)
    I_list = free_maximal(n, E)
    m = len(I_list)
    # primal: vars mu_1..mu_m, rho ; maximise rho
    A, b = [], []
    for i in S:
        A.append([-(i in I) for I in I_list] + [1]); b.append(0)
    for i in Lc:
        A.append([-(i in I) for I in I_list] + [0]); b.append(-float(caps[i]))
    A.append([1] * m + [0]); b.append(1)
    res = linprog([0] * m + [-1], A_ub=A, b_ub=b, bounds=[(0, None)] * (m + 1), method="highs")
    assert res.status == 0, res.message
    val = Fr(-res.fun).limit_denominator(10000)
    mu = [Fr(x).limit_denominator(10000) for x in res.x[:m]]
    s = sum(mu)
    if s > 1:
        mu = [x / s for x in mu]
    # exact primal check (marginals are at least val on S, caps on L)
    marg = [sum(mu[j] for j, I in enumerate(I_list) if i in I) for i in range(n)]
    primal_ok = all(x >= 0 for x in mu) and sum(mu) <= 1 and all(marg[i] >= val for i in S) \
        and all(marg[i] >= caps[i] for i in Lc)
    # dual: vars y_i (i in S u Lc), z ; min z - sum caps_i y_i ; z >= y(I) for all I ; y(S) = 1
    idx = S + Lc
    Ad = [[(i in I) for i in idx] + [-1] for I in I_list]
    res2 = linprog([0] * len(S) + [-float(caps[i]) for i in Lc] + [1], A_ub=Ad, b_ub=[0] * m,
                   A_eq=[[1] * len(S) + [0] * len(Lc) + [0]], b_eq=[1],
                   bounds=[(0, None)] * (len(idx) + 1), method="highs")
    assert res2.status == 0, res2.message
    y = [Fr(x).limit_denominator(10000) for x in res2.x[:len(idx)]]
    ys = sum(y[:len(S)])
    y = [x / ys for x in y]  # enforce y(S) = 1 exactly
    yd = dict(zip(idx, y))
    z = max(sum(yd[i] for i in I if i in yd) for I in I_list)
    dval = z - sum(caps[i] * yd[i] for i in Lc)
    dual_ok = all(x >= 0 for x in y)
    certified = primal_ok and dual_ok and dval == val
    return val, certified, yd


def comb(n, r):
    return [set(c) for c in itertools.combinations(range(n), r)]


def window(H, m, g):
    return [set(c) for c in itertools.combinations(range(len(H)), m + 1)
            if max(H[i] for i in c) - min(H[i] for i in c) <= g]


def cycle(n):
    return [{i, (i + 1) % n} for i in range(n)]


def petersen():
    outer = [{i, (i + 1) % 5} for i in range(5)]
    inner = [{5 + i, 5 + (i + 2) % 5} for i in range(5)]
    spokes = [{i, 5 + i} for i in range(5)]
    return outer + inner + spokes


# Maynard's constant: lower bounds used in the parity paper (code/parity/pintz_maynard.py)
M_LOWER = {2: 1.3859332, 3: 1.6460391, 4: 1.8440154, 5: 2.0041054}


def M_upper(k):  # Maynard, M_k <= k/(k-1) log k
    return k / (k - 1) * math.log(k) if k > 1 else 1.0


def report(name, n, E, S, L=(), caps=None, note=""):
    val, cert, y = rho_crit(n, E, S, L, caps)
    k = len(S)
    thr = 2 * k * val  # needed: theta*M_k > thr
    blocked = val >= Fr(1, 2)
    up = M_upper(k)
    lo = M_LOWER.get(k)
    reach = "impossible for theta<=1 (M_k upper bound %.3f)" % up if thr >= up else \
        ("YES at theta=1/2 (M_k >= %.4f)" % lo if lo and lo * 0.5 > thr else
         ("YES at theta=1 (M_k >= %.4f)" % lo if lo and lo > thr else "not decided by bounds at hand"))
    ysupp = {i: str(v) for i, v in y.items() if v}
    print(f"{name:44s} k={k:2d} |L|={len(L)} rho_crit={str(val):6s} cert={cert} "
          f"parity-blocked={blocked!s:5s} need theta*M_k > {float(thr):.4f} -> {reach}")
    print(f"    dual inequality y = {ysupp} {note}")
    return val


if __name__ == "__main__":
    print("rho_crit = max rho with (rho on sieve positions, 1/2 on lambda positions) in hull of E-free sets\n")
    print("== 1. DHL[k,m+1] (all (m+1)-subsets); expect t* = m/k, threshold theta*M_k > 2m")
    for k, m in [(2, 1), (3, 1), (4, 1), (5, 1), (4, 2), (5, 2), (6, 2), (6, 3), (7, 3), (8, 3)]:
        v = report(f"DHL[{k},{m+1}]", k, comb(k, m + 1), range(k))
        assert v == Fr(m, k)
    print("\n== 2. window targets (m+1 primes within distance g) on fixed admissible tuples")
    for H, m, g in [((0, 2, 6), 1, 6), ((0, 2, 6), 1, 4), ((0, 2, 6, 8, 12), 1, 6), ((0, 2, 6, 8, 12), 1, 12),
                    ((0, 2, 6, 8, 12), 2, 12), ((0, 2, 8, 12), 1, 6), ((0, 4, 6, 10, 12, 16), 1, 6)]:
        report(f"window H={H} m={m} g={g}", len(H), window(H, m, g), range(len(H)))
    print("\n== 3. graph targets (t* = 1/chi_f)")
    for name, n, E in [("path P4", 4, [{0, 1}, {1, 2}, {2, 3}]), ("C5", 5, cycle(5)), ("C7", 7, cycle(7)),
                       ("Petersen", 10, petersen()), ("K4", 4, comb(4, 2))]:
        report(name, n, E, range(n))
    print("\n== 4. Pintz targets: K_{k+1} on H u {r}, r a lambda-position; expect rho_crit = 1/(2k) -> theta*M_k > 1")
    for k in range(2, 7):
        v = report(f"Pintz k={k}", k + 1, comb(k + 1, 2), range(k), L=[k])
        assert v == Fr(1, 2 * k)
    print("   symmetric t* of the same graph (treating r as a sieve position) for contrast:")
    for k in range(2, 5):
        report(f"  K_{k+1} symmetric t*", k + 1, comb(k + 1, 2), range(k + 1))
    print("\n== 5. star (prime and lambda(n+r)=-1, no 'two primes' alternative)")
    for k in (1, 3, 5):
        report(f"star k={k}", k + 1, [{i, k} for i in range(k)], range(k), L=[k])
    print("\n== 6. mixed targets")
    for k in (3, 4, 5, 6):
        # two primes, or one prime with lambda(n+r1)=lambda(n+r2)=-1
        E = comb(k, 2) + [{i, k, k + 1} for i in range(k)]
        report(f"2 primes | prime+2 lambdas k={k}", k + 2, E, range(k), L=[k, k + 1])
    for k in (3, 4, 5, 6):
        # two primes, or one prime with lambda(n+r1)=-1, or one prime with lambda(n+r2)=-1
        E = comb(k, 2) + [{i, k} for i in range(k)] + [{i, k + 1} for i in range(k)]
        report(f"2 primes | prime+(l1 or l2) k={k}", k + 2, E, range(k), L=[k, k + 1])
    for k in (4, 5, 6):
        # three primes, or two primes and lambda(n+r)=-1
        E = comb(k, 3) + [set(c) | {k} for c in itertools.combinations(range(k), 2)]
        report(f"3 primes | 2 primes+lambda k={k}", k + 1, E, range(k), L=[k])
    for k in (3, 4):
        # two primes, or lambda(n+r1)=lambda(n+r2)=-1 with no prime at all (pure lambda pair)
        E = comb(k, 2) + [{k, k + 1}]
        report(f"2 primes | lambda pair k={k}", k + 2, E, range(k), L=[k, k + 1])
    print("\n== 7. Chen-type: n prime and n+2 in P_2 (P_2 position not parity-capped: cap 1)")
    report("Chen (P_2 cap 1)", 2, [{0, 1}], [0], caps={1: Fr(1)})
    report("twin (cap 1/2)", 2, [{0, 1}], [0], caps={1: Fr(1, 2)})
    report("n+2 semiprime only (lambda=+1 needed)", 2, [{0, 1}], [0], caps={1: Fr(1, 2)},
           note="(same LP as twins: the class blocks both halves)")
