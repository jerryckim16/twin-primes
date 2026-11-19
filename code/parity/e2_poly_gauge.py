#!/usr/bin/env python3
"""Parity attempt, Session 36 (route card notes/parity-attempts/2026-11-19-e2-polynomial-gauge.md).

E2 pairs at a fixed difference d through POLYNOMIAL parametrisations in several variables (this includes
Chen-type variable multipliers x = u * L(m), u a second variable).  Model as in the Session 33 card
(2026-11-18-e2-odd-cycles.md), with linear forms replaced by irreducible primitive polynomials ("vertices").

An event is a polynomial identity  c * prod_A P  +  s d  =  c' * prod_B P  (A, B multisets of vertices, c, c' in
{1} u primes) in which both sides have an E2 shape:
   (c = 1, |A| = 1)  -> the vertex must be E2   (required lambda = +1),
   (c prime, |A| = 1) -> the vertex must be prime (required lambda = -1),
   (c = 1, |A| = 2)  -> both vertices prime       (required lambda = -1 each).
The target of a system is the union of its events; it is BLOCKED if (1/2, ..., 1/2) lies in the convex hull of
the target-free sign patterns (fair version of Prop. prop:bipartite, as in the Session 33 card).

Claim tested (Proposition in the route card): if 4 does not divide d, the sign vector
    eps_v = chi(P_v(m0)) * f(g_v)          (d = 2 mod 4: chi = chi_4, f(n) = lambda(n) chi_4(odd part of n))
    eps_v = f'(g_v)                         (d odd:       f'(n) = lambda(n) (-1)^{v2(n)})
(m0 a point where every vertex is odd, g_v the content of the top-degree part of P_v) has
    prod_{v in A u B} eps_v = - lambda(c) lambda(c')        on every event,
so no sign vector in the affine F2-space S = {eta : sum_{v in e} eta_v = 1 + Omega(c) + Omega(c') for all e}
meets any event; the uniform measure on S is fair unless some vertex indicator lies in the F2-span of the event
supports.  The script: (1) generates events from several families; (2) checks the product identity exactly on every
event for d in a list (and records the failures for 4 | d); (3) builds systems (connected unions of events) and compares
the F2-span criterion with an LP blocking test; (4) writes certificates (S as explicit sign vectors) for a second
program (e2_poly_gauge_check.py) to verify independently.

Usage: /usr/bin/python3 -I code/parity/e2_poly_gauge.py [out.json]
"""
import sys, json, itertools, math, random
import sympy as sp
import numpy as np
from scipy.optimize import linprog

m, u, w = sp.symbols('m u w')
VARS = (m, u, w)
random.seed(20261119)

def Omega(n):
    return sum(sp.factorint(n).values()) if n > 1 else 0

def lam(n):
    return (-1) ** Omega(n)

def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2; k += 1
    return k

def chi4(n):
    n = n % 4
    return {1: 1, 3: -1}[n]

def oddpart(n):
    while n % 2 == 0:
        n //= 2
    return n

def normalize(poly):
    """Return (content, primitive polynomial with positive leading coefficient) of a nonconstant integer polynomial."""
    P = sp.Poly(poly, *VARS)
    cont, prim = P.primitive()
    if prim.LC() < 0:
        cont, prim = -cont, -prim
    return int(cont), prim

def shape(expr):
    """Factor expr over Z. Return (c, [(vertex_poly, required_sign)]) if it has an E2 shape, else None."""
    c0, flist = sp.factor_list(sp.expand(expr), *VARS)
    c0 = int(c0)
    fac = []
    for f, e in flist:
        k, prim = normalize(f)
        c0 *= k ** e
        fac += [prim] * e
    if c0 <= 0 or not fac:
        return None
    if c0 == 1 and len(fac) == 1:
        return (1, [(fac[0], +1)])
    if sp.isprime(c0) and len(fac) == 1:
        return (c0, [(fac[0], -1)])
    if c0 == 1 and len(fac) == 2:
        return (1, [(fac[0], -1), (fac[1], -1)])
    return None

def key(P):
    return str(P.as_expr())

def top_content(P):
    deg = P.total_degree()
    coeffs = [abs(int(cf)) for mon, cf in P.terms() if sum(mon) == deg]
    g = 0
    for cf in coeffs:
        g = math.gcd(g, cf)
    return g

# ---------------- event families ----------------
def lin_forms(var, amax, bmax):
    return [a * var + b for a in range(1, amax + 1) for b in range(-bmax, bmax + 1) if math.gcd(a, b) == 1]

def x_sides():
    """Candidate x-sides (expressions with an E2 shape by construction)."""
    out = []
    Lm = lin_forms(m, 3, 5)
    for L in Lm:                                         # c * L, c in {1, 3, 5}
        for c in (1, 3, 5):
            out.append(('lin', c * L))
    for L in Lm:                                         # Chen-type: u * L(m)
        out.append(('chen', u * L))
    for L1, L2 in itertools.combinations(lin_forms(m, 2, 4), 2):   # L1 * L2 in one variable
        out.append(('quad', L1 * L2))
    for a, b in itertools.product((1, 2, 3), (-3, -1, 1, 3)):      # bilinear (a u + b) * w
        if math.gcd(a, b) == 1:
            out.append(('bilin', (a * u + b) * w))
    out.append(('uv', u * w))
    return out

def make_events(d):
    evs = []
    for fam, X in x_sides():
        sx = shape(X)
        if sx is None:
            continue
        for s in (1, -1):
            sy = shape(X + s * d)
            if sy is None:
                continue
            evs.append({'fam': fam, 's': s, 'x': sx, 'y': sy, 'X': X})
    return evs

# ---------------- product identity ----------------
def find_m0(vertices):
    for pt in itertools.product(range(-3, 4), repeat=3):
        vals = [int(P.as_expr().subs(dict(zip(VARS, pt)))) for P in vertices]
        if all(v % 2 != 0 for v in vals):
            return pt, vals
    return None, None

def eps_vec(vertices, d, m0):
    eps = {}
    for P in vertices:
        g = top_content(P)
        if d % 2 == 1:
            eps[key(P)] = lam(g) * (-1) ** v2(g)
        else:
            val = int(P.as_expr().subs(dict(zip(VARS, m0))))
            eps[key(P)] = chi4(val) * lam(g) * chi4(oddpart(g))
    return eps

def ev_vertices(ev):
    return [P for P, _ in ev['x'][1]] + [P for P, _ in ev['y'][1]]

def ev_req_prod(ev):
    return lam(ev['x'][0]) * lam(ev['y'][0])          # product of required signs = lambda(c) lambda(c')

def check_product(ev, eps):
    pr = 1
    for P in ev_vertices(ev):
        pr *= eps[key(P)]
    return pr == -ev_req_prod(ev)

# ---------------- blocking: LP and F2 span ----------------
def patterns(V, events):
    """All sign vectors on V avoiding every event (an event is met if every listed vertex has its required sign)."""
    idx = {v: i for i, v in enumerate(V)}
    reqs = []
    for ev in events:
        r = {}
        ok = True
        for P, sg in ev['x'][1] + ev['y'][1]:
            k = key(P)
            if k in r and r[k] != sg:
                ok = False
            r[k] = sg
        if ok:
            reqs.append([(idx[k], sg) for k, sg in r.items()])
    free = []
    for sv in itertools.product((1, -1), repeat=len(V)):
        if not any(all(sv[i] == sg for i, sg in rq) for rq in reqs):
            free.append(sv)
    return free

def lp_blocked(V, events):
    free = patterns(V, events)
    if not free:
        return False
    A = np.array([[(1 + x) / 2 for x in sv] for sv in free]).T      # marginals P(lambda = +1)
    A_eq = np.vstack([A, np.ones(len(free))])
    b_eq = np.array([0.5] * len(V) + [1.0])
    res = linprog(np.zeros(len(free)), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * len(free), method='highs')
    return res.status == 0

def f2_solutions(V, events):
    """Affine F2 space S (as explicit sign vectors; V small) and whether every coordinate is balanced on S."""
    idx = {v: i for i, v in enumerate(V)}
    rows = []
    for ev in events:
        vec = [0] * len(V)
        for P in ev_vertices(ev):
            vec[idx[key(P)]] ^= 1
        rhs = (1 + Omega(ev['x'][0]) + Omega(ev['y'][0])) % 2
        rows.append((vec, rhs))
    S = []
    for eta in itertools.product((0, 1), repeat=len(V)):
        if all(sum(a * b for a, b in zip(vec, eta)) % 2 == rhs for vec, rhs in rows):
            S.append(eta)
    balanced = bool(S) and all(2 * sum(e[i] for e in S) == len(S) for i in range(len(V)))
    return S, balanced

# ---------------- main ----------------
def main():
    outpath = sys.argv[1] if len(sys.argv) > 1 else 'code/parity/e2_poly_gauge_cert.json'
    report = {}
    certs = []
    for d in (1, 2, 3, 5, 6, 7, 10, 4, 8, 12):
        evs = make_events(d)
        fams = {}
        for ev in evs:
            fams[ev['fam']] = fams.get(ev['fam'], 0) + 1
        # product identity per event, with a per-event m0 and with system-level m0 below
        nfail = 0; nskip = 0
        for ev in evs:
            Vs = ev_vertices(ev)
            m0, _ = find_m0(Vs)
            if m0 is None:
                nskip += 1; continue
            if not check_product(ev, eps_vec(Vs, d, m0)):
                nfail += 1
        # systems: random connected unions of events sharing vertices
        byv = {}
        for i, ev in enumerate(evs):
            for P in ev_vertices(ev):
                byv.setdefault(key(P), []).append(i)
        nsys = 0; nblocked = 0; nbal = 0; nbal_but_unblocked = 0; nprodfail_sys = 0; odd_events = 0
        examples_unbalanced_blocked = 0; examples_unblocked = []
        for trial in range(400):
            i0 = random.randrange(len(evs))
            chosen = {i0}
            for _ in range(random.randint(1, 4)):
                Vk = {key(P) for j in chosen for P in ev_vertices(evs[j])}
                nb = [j for k in Vk for j in byv[k] if j not in chosen]
                if not nb:
                    break
                chosen.add(random.choice(nb))
            events = [evs[j] for j in sorted(chosen)]
            Vp = {}
            for ev in events:
                for P in ev_vertices(ev):
                    Vp[key(P)] = P
            V = sorted(Vp)
            if len(V) > 12:
                continue
            m0, _ = find_m0([Vp[k] for k in V])
            if m0 is None:
                continue                                   # not admissible mod 2
            nsys += 1
            odd_events += sum(1 for ev in events if len(ev_vertices(ev)) % 2 == 1)
            eps = eps_vec([Vp[k] for k in V], d, m0)
            if d % 4 != 0 and not all(check_product(ev, eps) for ev in events):
                nprodfail_sys += 1
            bl = lp_blocked(V, events)
            S, bal = f2_solutions(V, events)
            nblocked += bl; nbal += bal
            if bal and not bl:
                nbal_but_unblocked += 1
            if bl and not bal:
                examples_unbalanced_blocked += 1
            if not bl and len(examples_unblocked) < 3:
                examples_unblocked.append([str(ev['X']) + (' + ' if ev['s'] > 0 else ' - ') + str(d) for ev in events])
            if bal and len(certs) < 60:
                certs.append({'d': d, 'm0': list(m0), 'V': V,
                              'events': [{'X': str(sp.expand(ev['X'])), 's': ev['s'],
                                          'cx': ev['x'][0], 'cy': ev['y'][0],
                                          'xv': [[key(P), sg] for P, sg in ev['x'][1]],
                                          'yv': [[key(P), sg] for P, sg in ev['y'][1]]} for ev in events],
                              'S': [[1 - 2 * x for x in eta] for eta in S]})
        report[d] = dict(events=len(evs), families=fams, product_fail=nfail, skipped_not_odd=nskip,
                         systems=nsys, odd_events_in_systems=odd_events, lp_blocked=nblocked,
                         f2_balanced=nbal, balanced_but_unblocked=nbal_but_unblocked,
                         blocked_but_unbalanced=examples_unbalanced_blocked,
                         system_product_fail=nprodfail_sys, unblocked_examples=examples_unblocked)
        print(f"d={d}: {report[d]}", flush=True)
    json.dump({'certs': certs}, open(outpath, 'w'))
    print(f"wrote {len(certs)} certificates to {outpath}")
    # assertions of the proposition
    for d, r in report.items():
        if d % 4 != 0:
            assert r['product_fail'] == 0 and r['system_product_fail'] == 0, d
            assert r['balanced_but_unblocked'] == 0, d
            assert r['lp_blocked'] == r['systems'], ('unblocked system for d not divisible by 4', d)
    print("ASSERTIONS PASSED: product identity on every event and system for d not divisible by 4;"
          " F2-balanced => LP-blocked; every admissible system blocked for d not divisible by 4")

if __name__ == '__main__':
    main()
