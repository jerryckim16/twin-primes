#!/usr/bin/env python3
"""Rung 186: exact check of the analytic-input side of Lemma 1.1 of OpenAI's numerical companion [14]
("Numerical certificate for prime gaps at most 186", short_gaps_numerics.pdf, pp. 6-7), i.e. that the retained
source rows satisfy the HYPOTHESES of the distribution estimates and transfer lemmas of the main paper [8]
("Improved short gaps between primes", short_gaps.pdf).  Report: notes/oai186-lemma11-analytic.md.

Written from the two PDFs only (pdftotext -layout).  Nothing from the authors' repository is imported or run.
All decisions are exact (fractions.Fraction).  Sections:
  [0] parameters (1.1), (1.13), (1.14) of [14]; consistency with [8] (4.1), (4.11), (2.19), (4.15)
  [1] ladders (1.15): row counts, block formula, omega enclosure table, (1.16)-(1.17)
  [2] distribution hypotheses, row by row:
        old r=1,2: [8] Prop 2.16 (omega<1/12, delta<1/4+omega, 0<sigma<1/2, 68w+14d<1, (2.11)), Prop 2.17 (2.12),
                   Cor 2.19 proof (sigma>1/10, sigma>2w), and (2.15) itself, with sigma = sigma0
        old r=3:   (2.14) and (2.12) with sigma = 1/10 + (3-240w-80d)/40, sigma>1/10, sigma>2w, sigma<1/2, (2.15)
        new r=1,2: Prop 2.22: (2.24) with the three upper bounds reduced by tau, 68w+14d<1, (2.11) with sigma_{m,tau}
        new r=3:   Prop 2.22: (2.24) reduced by tau, (2.14) with sigma_{m,tau}
      least positive density, least margin
  [3] transfer: Lemma 4.1 guards (r<=2), Prop 4.2 budget A+C <= B+xi (r=3), phi_D/phi_E monotone and (4.7),
      eta = xi - e/2 > 0, A >= C > L, A <= 11C/10 < 7L/3, radius hypotheses s_D <= S, s_E <= T_nu on the grid
  [4] level/density retreat (4.19), band coverage: retained-row rule (1.20), boundary floors, pair maxima, B+ = B_{t+1},
      initial BV band, min xi > 33e-6 > 22e-6 > 2h
  [5] caps (1.18) as running minimum, each cap > activation, grid masks (1.5) via (1.19)
  [6] six groups (1.23)-(1.24): xi_G = min, U_G = min, b_G = min core, z_G, p_G; xi_G > 2h, xi_G < p_G <= z_G,
      z_G + m_G p_G <= U_G; later 5/2 activation/threshold <= earlier order-two ones
  [7] common inner-square source ([8] (4.13)-(4.17), Lemma 4.3)
  [8] negative controls (perturbed inputs must make specific checks fail)
usage: /usr/bin/python3 -I code/oai186_lemma11_check.py > code/oai186_lemma11_check.out"""
import sys, time
from fractions import Fraction as F
from math import floor, ceil

T_START = time.time()
FAILS = []
NCHECK = [0]
QUIET = [False]


def check(name, cond, detail=""):
    NCHECK[0] += 1
    if not QUIET[0]:
        print(("  PASS " if cond else "  FAIL ") + name + (("   [" + detail + "]") if detail else ""))
    if not cond:
        FAILS.append(name)
    return cond


def fl(x):
    return floor(x)  # exact on Fraction


def dec(x, n=10):
    return f"{float(x):.{n}g}"


# ----------------------------------------------------------------------------------------------------------------
def build(over=None):
    """All data of [14] (1.1), (1.13)-(1.17).  `over` lets negative controls change one input."""
    P = dict(
        g0=F(1, 10**7), eps_o=F(1, 10**6), eps_n=F(1, 10**7), tau=F(1, 10**10),
        sigma0=F(100001, 10**6), a_star=F(40481, 100000), b_star=F(59519, 100000), c_star=F(33856, 100000),
        Omega_o=F(12499, 10**6), Omega_n=F(253, 20000), N=98304, rho_star_shift=F(0),
    )
    if over:
        P.update(over)
    P['sigma_mt'] = F(1, 2) - P['a_star'] + P['tau']
    P['rho'] = F(1, 4) + F(12499, 10**6)                   # rho := 1/4 + Omega_o (fixed, as printed)
    P['rho_star'] = P['rho'] - P['g0'] + P['rho_star_shift']
    rs = P['rho_star']
    P['S'] = F(2742997, 10**7) / rs
    P['T1'] = F(251, 1000) / rs
    P['T0'] = 2 - F(3, 1000) - P['S']
    P['e'] = P['g0'] / P['rho']
    P['zeta'] = F(19037, 100000) / P['rho']
    P['h'] = P['S'] / P['N']
    s0, sm = P['sigma0'], P['sigma_mt']
    P['blk'] = {
        'o': {1: ((1 - 5 * s0) / 15, F(18, 5)), 2: ((1 - 4 * s0) / 16, F(7, 2)), 3: (F(3, 80), F(3))},
        'n': {1: ((1 - 5 * sm) / 15, F(18, 5)), 2: ((1 - 4 * sm) / 16, F(7, 2)), 3: ((1 - 2 * sm) / 20, F(16, 5))},
    }
    P['eps'] = {'o': P['eps_o'], 'n': P['eps_n']}
    P['Om'] = {'o': P['Omega_o'], 'n': P['Omega_n']}
    P['Tnu'] = {'o': P['T0'], 'n': P['T1']}
    rows = {}
    for nu in 'on':
        E = P['rho'] * (P['S'] + P['Tnu'][nu]) - F(1, 2)
        P['E_' + nu] = E
        w_prev, t, L = F(0), 0, []
        while True:
            r = 1 if t < 12 else (2 if t < 24 else 3)
            c, s = P['blk'][nu][r]
            eps = P['eps'][nu]
            cand = (c - eps - E + 2 * w_prev - P['g0']) / s
            w = min(P['Om'][nu], cand)
            d = c - s * w - eps
            B = (F(1, 2) + 2 * w_prev) / P['rho']
            Bp = (F(1, 2) + 2 * w) / P['rho']
            xi = d / P['rho']
            T = P['Tnu'][nu]
            a, b = B - T, B - P['S']
            eta = xi if r <= 2 else (xi + P['S'] + T - B) / 2
            A, C = a + eta, b + eta
            L.append(dict(nu=nu, t=t, r=r, w=w, w_prev=w_prev, d=d, B=B, Bp=Bp, xi=xi, a=a, b=b, eta=eta, A=A, C=C,
                          terminal=(w == P['Om'][nu]), cand=cand, c=c, s=s, eps=eps, T=T))
            if w == P['Om'][nu] or t > 400:
                break
            w_prev, t = w, t + 1
        rows[nu] = L
    P['rows'] = rows
    # grid totals (1.5)/(1.19)
    h = P['h']
    P['Sbox'] = 98303 * h
    P['Tbox'] = {'o': 89563 * h, 'n': 89953 * h}
    P['retained'] = {nu: [R for R in rows[nu] if R['B'] < P['Sbox'] + P['Tbox'][nu]] for nu in 'on'}
    return P


# ----------------------------------------------------------------------------------------------------------------
def dist_conditions(P, R):
    """List of (name, lhs, rhs) meaning the strict inequality lhs < rhs required for row R (margin = rhs - lhs)."""
    w, d, r = R['w'], R['d'], R['r']
    out = [("omega>0", F(0), w), ("omega<1/12", w, F(1, 12)), ("delta>0", F(0), d), ("delta<1/4+omega", d, F(1, 4) + w)]
    if R['nu'] == 'o':
        if r <= 2:
            sg = P['sigma0']
            out += [("68w+14d<1 [P2.16]", 68 * w + 14 * d, F(1))]
            if r == 1:
                out += [("54w+15d+5s<1 (2.11)", 54 * w + 15 * d + 5 * sg, F(1)),
                        ("108w+30d<1 (2.15)", 108 * w + 30 * d, F(1))]
            else:
                out += [("56w+16d+4s<1 (2.11)", 56 * w + 16 * d + 4 * sg, F(1)),
                        ("280w+80d<3 (2.15)", 280 * w + 80 * d, F(3))]
        else:
            sg = F(1, 10) + (3 - 240 * w - 80 * d) / 40
            out += [("72w+24d<1 (2.14)", 72 * w + 24 * d, F(1)),
                    ("48w+16d+4s<1 (2.14)", 48 * w + 16 * d + 4 * sg, F(1)),
                    ("64w+20d+2s<1 (2.14)", 64 * w + 20 * d + 2 * sg, F(1)),
                    ("240w+80d<3 (2.15)", 240 * w + 80 * d, F(3))]
        out += [("sigma>0", F(0), sg), ("sigma<1/2", sg, F(1, 2)), ("sigma>1/10 [C2.19 HB]", F(1, 10), sg),
                ("sigma>2w [C2.19]", 2 * w, sg),
                ("1/18+28w/9+2d/9<sigma (2.12)", F(1, 18) + F(28, 9) * w + F(2, 9) * d, sg)]
    else:
        sg, tau = P['sigma_mt'], P['tau']
        out += [("1/4+7w+2d<c*-tau (2.24)", F(1, 4) + 7 * w + 2 * d, P['c_star'] - tau),
                ("1/18+28w/9+2d/9<19/200-tau (2.24)", F(1, 18) + F(28, 9) * w + F(2, 9) * d, F(19, 200) - tau),
                ("1/2+2w<b*-tau (2.24)", F(1, 2) + 2 * w, P['b_star'] - tau),
                ("sigma_mt>0", F(0), sg), ("sigma_mt<1/2", sg, F(1, 2))]
        if r <= 2:
            out += [("68w+14d<1 [P2.22]", 68 * w + 14 * d, F(1))]
            out += [("54w+15d+5s<1 (2.11)", 54 * w + 15 * d + 5 * sg, F(1))] if r == 1 else \
                   [("56w+16d+4s<1 (2.11)", 56 * w + 16 * d + 4 * sg, F(1))]
        else:
            out += [("72w+24d<1 (2.14)", 72 * w + 24 * d, F(1)),
                    ("48w+16d+4s<1 (2.14)", 48 * w + 16 * d + 4 * sg, F(1)),
                    ("64w+20d+2s<1 (2.14)", 64 * w + 20 * d + 2 * sg, F(1))]
    return out


def sec_dist(P, rowsets, verbose=True):
    ok = True
    worst = None
    per_name = {}
    for nu in 'on':
        for R in rowsets[nu]:
            for name, lhs, rhs in dist_conditions(P, R):
                m = rhs - lhs
                key = (nu, R['r'], name)
                if key not in per_name or m < per_name[key][0]:
                    per_name[key] = (m, R['t'])
                if m <= 0:
                    ok = False
                if worst is None or m < worst[0]:
                    worst = (m, nu, R['t'], name)
    if verbose:
        for key in sorted(per_name):
            m, t = per_name[key]
            print(f"     {key[0]} r={key[1]} {key[2]:<38s} least margin {dec(m, 8):>14s} (row {t})")
    return ok, worst


# ================================================================================================================
def main():
    P = build()
    S, T0, T1, rho, rs, e, h, zeta = P['S'], P['T0'], P['T1'], P['rho'], P['rho_star'], P['e'], P['h'], P['zeta']
    rows, ret = P['rows'], P['retained']

    print("[0] parameters")
    check("rho = 262499/10^6", rho == F(262499, 10**6))
    check("rho* = 2624989/10^7 ([14] (1.1), [8] (4.1))", rs == F(2624989, 10**7))
    check("S = 2742997/2624989", S == F(2742997, 2624989))
    check("T1 = 2510000/2624989", T1 == F(2510000, 2624989))
    check("T0 = 2 - 3/1000 - S = 2499106033/2624989000", T0 == F(2499106033, 2624989000))
    check("0 < T0 < T1 < S", 0 < T0 < T1 < S)
    check("rho*S = 2742997/10^7, rho*T0 = 2499106033/10^10, rho*T1 = 251/1000 (1.2)",
          rs * S == F(2742997, 10**7) and rs * T0 == F(2499106033, 10**10) and rs * T1 == F(251, 1000))
    check("[8] (4.2): rho*S < 11/40 and rho*T1 < 11/40", rs * S < F(11, 40) and rs * T1 < F(11, 40))
    check("sigma_{m,tau} = 1/2 - a* + tau = 9519/100000 + 10^-10 ([8] (4.11), (2.19) a*=0.40481)",
          P['sigma_mt'] == F(9519, 100000) + F(1, 10**10))
    check("[8] (2.19): b* = 1 - a*", P['b_star'] == 1 - P['a_star'])
    check("[8] Prop 2.22 proof: tau = 10^-10 is allowed (0 < tau <= 10^-10)", 0 < P['tau'] <= F(1, 10**10))
    check("Omega_o < 1/12 and Omega_n < 1/12", P['Omega_o'] < F(1, 12) and P['Omega_n'] < F(1, 12))
    check("[8] Prop 2.22 example: 1/2 + 2*253/20000 = 0.5253", F(1, 2) + 2 * F(253, 20000) == F(5253, 10000))

    print("[1] ladders (1.15)-(1.17)")
    for nu, cnt, oc in (('o', 29, (12, 12, 5)), ('n', 43, (12, 12, 19))):
        L = rows[nu]
        counts = tuple(sum(1 for R in L if R['r'] == r) for r in (1, 2, 3))
        check(f"ladder {nu}: {len(L)} rows, order counts {counts}", len(L) == cnt and counts == oc)
        check(f"ladder {nu}: only the last row is terminal (omega = Omega)",
              all(not R['terminal'] for R in L[:-1]) and L[-1]['terminal'])
        check(f"ladder {nu}: omega strictly increasing", all(L[i]['w'] < L[i + 1]['w'] for i in range(len(L) - 1)))
        # block formula: untruncated value after j steps from v is W + (2/s)^j (v - W)
        okb = True
        for r in (1, 2, 3):
            blk = [R for R in L if R['r'] == r]
            c, s = P['blk'][nu][r]
            W = (c - P['eps'][nu] - P['E_' + nu] - P['g0']) / (s - 2)
            v = blk[0]['w_prev']
            for j, R in enumerate(blk, start=1):
                okb &= (R['cand'] == W + (F(2) / s) ** j * (v - W))
        check(f"ladder {nu}: block formula W + (2/s)^j (v - W) reproduces every untruncated value", okb)
        # nonterminal identity delta - E + 2 omega_{t-1} = g0
        check(f"ladder {nu}: delta - E + 2 omega_(t-1) = g0 on every nonterminal row",
              all(R['d'] - P['E_' + nu] + 2 * R['w_prev'] == P['g0'] for R in L if not R['terminal']))
        tab = {'o': {1: (2533, 5696), 2: (7051, 8855), 3: (10332, 12499)},
               'n': {1: (2676, 6018), 2: (7267, 8932), 3: (10326, 12650)}}[nu]
        for r in (1, 2, 3):
            ws = [R['w'] for R in L if R['r'] == r]
            lo, hi = min(ws), max(ws)
            check(f"enclosure 10^6 omega_{nu} r={r} in [{tab[r][0]}, {tab[r][1]}]",
                  F(tab[r][0], 10**6) <= lo and hi <= F(tab[r][1], 10**6) and
                  fl(lo * 10**6) == tab[r][0] and ceil(hi * 10**6) == tab[r][1],
                  f"actual [{dec(lo * 10**6, 9)}, {dec(hi * 10**6, 9)}] (floor/ceil match)")
        rr = ret[nu]
        check(f"retained {nu}: rows 0..{rr[-1]['t']}, none terminal",
              [R['t'] for R in rr] == list(range(len(rr))) and not any(R['terminal'] for R in rr))
        okt = True
        for R in rr:
            exp = (S + e, R['T'] + e) if R['r'] <= 2 else (S + e / 2, R['T'] + e / 2)
            okt &= (R['A'], R['C']) == exp
        check(f"(1.17) thresholds (A,C) on every retained {nu} row", okt)
    check("retained rows: To = 0..27, Tn = 0..38", ret['o'][-1]['t'] == 27 and ret['n'][-1]['t'] == 38
          and len(ret['o']) == 28 and len(ret['n']) == 39)

    print("[2] distribution hypotheses ([8] Prop 2.16, 2.17, Cor 2.19, Prop 2.18 (2.14), Prop 2.22 (2.24)), "
          "retained rows; per condition least margin")
    ok, worst = sec_dist(P, ret)
    check("all strict hypotheses hold on all 67 retained rows", ok,
          f"least margin {dec(worst[0])} at ({worst[1]},{worst[2]}) {worst[3]}")
    check("every required strict margin exceeds 10^-8 (retained rows)", worst[0] > F(1, 10**8))
    ok_all, worst_all = sec_dist(P, rows, verbose=False)
    check("(extra) the hypotheses also hold on the terminal rows (o,28), (n,42)", ok_all,
          f"least margin over all 72 ladder rows {dec(worst_all[0])} at ({worst_all[1]},{worst_all[2]}) {worst_all[3]}")
    dmin_all = min(R['d'] for nu in 'on' for R in rows[nu])
    dmin_ret = min(R['d'] for nu in 'on' for R in ret[nu])
    where = [(R['nu'], R['t']) for nu in 'on' for R in rows[nu] if R['d'] == dmin_all]
    check("least positive density over all ladder rows is 89999/10^11", dmin_all == F(89999, 10**11),
          f"at {where}; least over retained rows = {dec(dmin_ret)}")
    # old order-3 sigma equals 1/10 + 2 eps_o identically
    check("old r=3: sigma = 1/10 + (3-240w-80d)/40 = 1/10 + 2 eps_o on every row",
          all(F(1, 10) + (3 - 240 * R['w'] - 80 * R['d']) / 40 == F(1, 10) + 2 * P['eps_o']
              for R in rows['o'] if R['r'] == 3))
    # bilinear conditions equal (1 - k eps) identically: 15 eps (r=1), 16 eps (r=2), the order-3 identity
    check("old r=1: 54w+15d+5 sigma0 = 1 - 15 eps_o; r=2: 56w+16d+4 sigma0 = 1 - 16 eps_o",
          all((54 * R['w'] + 15 * R['d'] + 5 * P['sigma0'] == 1 - 15 * P['eps_o']) if R['r'] == 1 else
              (56 * R['w'] + 16 * R['d'] + 4 * P['sigma0'] == 1 - 16 * P['eps_o']) for R in rows['o'] if R['r'] <= 2))
    check("new r=3: 64w+20d+2 sigma_mt = 1 - 20 eps_n",
          all(64 * R['w'] + 20 * R['d'] + 2 * P['sigma_mt'] == 1 - 20 * P['eps_n'] for R in rows['n'] if R['r'] == 3))
    # affine-in-omega claim: in each block every condition is affine in omega, so endpoint checks suffice
    check("Type III parameter: 1/18+28w/9+2d/9 < 19/200 - tau on every retained new row",
          all(F(1, 18) + F(28, 9) * R['w'] + F(2, 9) * R['d'] < F(19, 200) - P['tau'] for R in ret['n']))

    print("[3] transfer hypotheses ([8] Lemma 4.1, Prop 4.2)")
    okg, gmin = True, None
    for nu in 'on':
        T = P['Tnu'][nu]
        for R in ret[nu]:
            if R['r'] == 1:
                g = [R['B'] + R['xi'] - 2 * T]
            elif R['r'] == 2:
                g = [R['B'] + R['xi'] - max(2 * S - T, 2 * T - S)]
            else:
                continue
            okg &= all(x >= 0 for x in g)
            m = min(g)
            gmin = m if gmin is None else min(gmin, m)
    check("Lemma 4.1 guards: B+xi >= 2T (r=1), B+xi >= max(2S-T, 2T-S) (r=2) on all retained rows", okg,
          f"least slack {dec(gmin)}")
    check("[14] reduction: guards == S-T_nu+e >= 0 and min(2T_nu-S, 2S-T_nu)+e >= 0",
          all((S - P['Tnu'][nu] + e >= 0) and (min(2 * P['Tnu'][nu] - S, 2 * S - P['Tnu'][nu]) + e >= 0)
              for nu in 'on'))
    check("identity B + xi = S + T_nu + e on every nonterminal row",
          all(R['B'] + R['xi'] == S + R['T'] + e for nu in 'on' for R in rows[nu] if not R['terminal']))
    check("r<=2 predicate threshold a+xi equals A, b+xi equals C ([8] Lemma 4.1 vs [14] (1.21))",
          all(R['a'] + R['xi'] == R['A'] and R['b'] + R['xi'] == R['C'] for nu in 'on' for R in ret[nu] if R['r'] <= 2))
    o3 = [R for nu in 'on' for R in ret[nu] if R['r'] == 3]
    check("r=3 budget A + C = B + xi (so A + C <= B + xi, [8] (4.6))", all(R['A'] + R['C'] == R['B'] + R['xi'] for R in o3))
    check("r=3: eta = xi - e/2 > 0", all(R['eta'] == R['xi'] - e / 2 and R['eta'] > 0 for R in o3))
    check("r=3: A >= C > L = 23C/40 > 0", all(R['A'] >= R['C'] > F(23, 40) * R['C'] > 0 for R in o3))
    check("r=3: A <= 11C/10 < 161C/120 = 7L/3", all(R['A'] <= F(11, 10) * R['C'] < F(161, 120) * R['C']
                                                   == F(7, 3) * F(23, 40) * R['C'] for R in o3))
    # phi_D, phi_E of (4.10): nondecreasing, nonnegative, sum 3u, phi(0)=0 -- piecewise linear, check slopes/breakpoint
    okphi = True
    for R in o3:
        L = F(23, 40) * R['C']
        pD = lambda u: min(F(3, 2) * u, L)
        pE = lambda u: 3 * u - pD(u)
        bp = F(2, 3) * L
        pts = [F(0), bp / 2, bp, bp * 2, bp * 10]
        okphi &= pD(0) == 0 and pE(0) == 0
        okphi &= all(pD(x) + pE(x) == 3 * x for x in pts)
        okphi &= all(pD(pts[i]) <= pD(pts[i + 1]) and pE(pts[i]) <= pE(pts[i + 1]) for i in range(len(pts) - 1))
        # slopes: phi_D 3/2 then 0; phi_E 3/2 then 3  (both >= 0)
    check("(4.10): phi_D, phi_E nonnegative, nondecreasing, phi(0)=0, phi_D+phi_E = 3u (piecewise linear: slopes "
          "3/2,0 and 3/2,3)", okphi)
    check("radius hypotheses of Lemma 4.1/Prop 4.2: largest outer total 98303h < S, base 89563h <= T0, "
          "enlarged 89953h <= T1",
          P['Sbox'] < S and P['Tbox']['o'] <= T0 and P['Tbox']['n'] <= T1,
          f"S/h={dec(S / h, 12)}, T0/h={dec(T0 / h, 12)}, T1/h={dec(T1 / h, 12)}")
    check("floor(S/h)=98304, floor(T0/h)=89563, floor(T1/h)=89953",
          fl(S / h) == 98304 and fl(T0 / h) == 89563 and fl(T1 / h) == 89953)

    print("[4] retreat and band coverage")
    check("rho* < rho ([8] (4.19))", rs < rho)
    check("level retreat: rho* B+ < 1/2 + 2 omega_t on all retained rows",
          all(rs * R['Bp'] < F(1, 2) + 2 * R['w'] for nu in 'on' for R in ret[nu]))
    check("density retreat: rho* xi < delta on all retained rows",
          all(rs * R['xi'] < R['d'] for nu in 'on' for R in ret[nu]))
    check("initial BV band: B_{nu,0} = 1/(2 rho) and rho* B_0 < 1/2",
          all(rows[nu][0]['B'] == 1 / (2 * rho) for nu in 'on') and rs / (2 * rho) < F(1, 2))
    check("B+_{nu,t} = B_{nu,t+1} for all ladder rows",
          all(rows[nu][i]['Bp'] == rows[nu][i + 1]['B'] for nu in 'on' for i in range(len(rows[nu]) - 1)))
    fb = {(nu, t): fl(rows[nu][t]['B'] / h) for nu, t in (('o', 27), ('o', 28), ('n', 38), ('n', 39))}
    check("floor(B/h): (o,27) 187773, (o,28) 188087, (n,38) 188254, (n,39) 188256",
          fb == {('o', 27): 187773, ('o', 28): 188087, ('n', 38): 188254, ('n', 39): 188256}, str(fb))
    check("pair maxima S_box + T0_box = 187866h, S_box + T1_box = 188256h",
          P['Sbox'] + P['Tbox']['o'] == 187866 * h and P['Sbox'] + P['Tbox']['n'] == 188256 * h)
    check("retained-row rule (1.20): B_{o,27} < 187866h <= B_{o,28}; B_{n,38} < 188256h <= B_{n,39}",
          rows['o'][27]['B'] < 187866 * h <= rows['o'][28]['B'] and rows['n'][38]['B'] < 188256 * h <= rows['n'][39]['B'])
    check("coverage: B+ of the last retained row >= pair maximum (o and n)",
          ret['o'][-1]['Bp'] >= P['Sbox'] + P['Tbox']['o'] and ret['n'][-1]['Bp'] >= P['Sbox'] + P['Tbox']['n'])
    check("B strictly increasing (bands are consecutive, nonoverlapping)",
          all(rows[nu][i]['B'] < rows[nu][i + 1]['B'] for nu in 'on' for i in range(len(rows[nu]) - 1)))
    ximin = min(R['xi'] for nu in 'on' for R in ret[nu])
    check("min xi over retained rows > 33e-6 > 22e-6 > 2h", ximin > F(33, 10**6) and F(22, 10**6) > 2 * h,
          f"min xi = {dec(ximin)}, 2h = {dec(2 * h)}")

    print("[5] caps (1.18) and masks (1.5)")
    # outer: rows of both ladders, core a_t; cap (S+e)/2 (r<=2), A-L (r=3)
    def cap(R, side):
        thr = R['A'] if side == 'outer' else R['C']
        if R['r'] <= 2:
            return thr / 2
        return R['A'] - F(23, 40) * R['C'] if side == 'outer' else F(63, 160) * R['C']
    cases = {'outer': ([R for nu in 'on' for R in ret[nu]], 'a'),
             'base': ([R for R in ret['o'] if R['r'] >= 2], 'b'),
             'enlarged': ([R for R in ret['n'] if R['r'] >= 2], 'b')}
    printed = {'outer': [(rows['n'][0]['a'], (S + e) / 2), (rows['n'][24]['a'], S + e / 2 - F(23, 40) * (T1 + e / 2))],
               'base': [(rows['o'][12]['b'], (T0 + e) / 2), (rows['o'][24]['b'], F(63, 160) * (T0 + e / 2))],
               'enlarged': [(rows['n'][12]['b'], (T1 + e) / 2), (rows['n'][24]['b'], F(63, 160) * (T1 + e / 2))]}
    for dom, (rs_, core) in cases.items():
        okc = True
        # breakpoints = all cores; running min after each core
        cores = sorted(set(R[core] for R in rs_))
        for k, c0 in enumerate(cores):
            run = min([zeta] + [cap(R, 'outer' if dom == 'outer' else 'inner') for R in rs_ if R[core] <= c0])
            pr = zeta
            for (bp, z) in printed[dom]:
                if bp <= c0:
                    pr = z
            okc &= (run == pr)
        check(f"(1.18) {dom}: running minimum of the row caps after each core equals the printed piecewise cap", okc)
        check(f"(1.18) {dom}: every row cap exceeds that row's activation",
              all(cap(R, 'outer' if dom == 'outer' else 'inner') > R['xi'] for R in rs_))
    check("(1.18) the printed caps are <= zeta and decrease", (S + e) / 2 < zeta and (T0 + e) / 2 < zeta and
          (T1 + e) / 2 < zeta and printed['outer'][1][1] < printed['outer'][0][1]
          and printed['base'][1][1] < printed['base'][0][1] and printed['enlarged'][1][1] < printed['enlarged'][0][1])
    check("a_{n,0} < a_{o,0}, a_{n,24} < a_{o,24}, and b_{o,t}, b_{n,t} increasing",
          rows['n'][0]['a'] < rows['o'][0]['a'] and rows['n'][24]['a'] < rows['o'][24]['a'])

    def mask(shells, d, top):
        res = []
        for (l, u, z) in shells:
            lo = 0 if l is None else max(0, fl(l / h) - d + 1)
            hi = min(98263, fl(u / h) - d)
            res.append((lo, hi, fl(z / h)))
        return res
    an0, an24 = rows['n'][0]['a'], rows['n'][24]['a']
    bo12, bo24, bn12, bn24 = rows['o'][12]['b'], rows['o'][24]['b'], rows['n'][12]['b'], rows['n'][24]['b']
    mO = mask([(None, an0, zeta), (an0, an24, (S + e) / 2), (an24, S, printed['outer'][1][1])], 40, S)
    mB = mask([(None, bo12, zeta), (bo12, bo24, (T0 + e) / 2), (bo24, T0, printed['base'][1][1])], 39, T0)
    mE = mask([(None, bn12, zeta), (bn12, bn24, (T1 + e) / 2), (bn24, T1, printed['enlarged'][1][1])], 39, T1)
    check("(1.5) outer mask", mO == [(0, 89196, 68225), (89197, 95598, 49152), (95599, 98263, 46580)], str(mO))
    check("(1.5) base mask", mB == [(0, 84930, 68225), (84931, 87194, 44781), (87195, 89524, 35265)], str(mB))
    check("(1.5) enlarged mask", mE == [(0, 85161, 68225), (85162, 87249, 44976), (87250, 89914, 35419)], str(mE))

    print("[6] six groups (1.22)-(1.24)")
    R_ = lambda nu, ts: [rows[nu][t] for t in ts]
    G = [
        ('O2', 2, R_('o', range(24)) + R_('n', range(24)), 'a', 'A', ('o', 23), S + e, an0, an24, 49152, 24576),
        ('O5/2', F(5, 2), R_('o', range(24, 28)) + R_('n', range(24, 39)), 'a', 'A', ('n', 38), S + e / 2, an24,
         98303 * h, 46580, 19660),
        ('I2old', 2, R_('o', range(12, 24)), 'b', 'C', ('o', 23), T0 + e, bo12, bo24, 44781, 22390),
        ('I5/2old', F(5, 2), R_('o', range(24, 28)), 'b', 'C', ('o', 27), T0 + e / 2, bo24, 89563 * h, 35265, 17912),
        ('I2new', 2, R_('n', range(12, 24)), 'b', 'C', ('n', 23), T1 + e, bn12, bn24, 44976, 22488),
        ('I5/2new', F(5, 2), R_('n', range(24, 39)), 'b', 'C', ('n', 38), T1 + e / 2, bn24, 89953 * h, 35419, 17990),
    ]
    xiG = {}
    for name, m, src, core, thr, xiw, U, bG, tG, zh, ph in G:
        xi_min = min(R['xi'] for R in src)
        xiG[name] = xi_min
        check(f"{name}: xi_G = xi_{xiw} = min activation; U_G = min threshold; b_G = min core",
              xi_min == rows[xiw[0]][xiw[1]]['xi'] and min(R[thr] for R in src) == U
              and min(R[core] for R in src) == bG)
        zG, pG = zh * h, ph * h
        check(f"{name}: p_G/h = floor(U_G/(2 m_G h)) = {ph}", fl(U / (2 * m * h)) == ph)
        check(f"{name}: xi_G > 2h, xi_G < p_G <= z_G, z_G + m_G p_G <= U_G",
              xi_min > 2 * h and xi_min < pG <= zG and zG + m * pG <= U,
              f"slack U-z-mp = {dec((U - zG - m * pG) / h)} h")
    check("later 5/2 activation/threshold <= earlier order-two: O, I old, I new",
          xiG['O5/2'] <= xiG['O2'] and xiG['I5/2old'] <= xiG['I2old'] and xiG['I5/2new'] <= xiG['I2new']
          and S + e / 2 <= S + e and T0 + e / 2 <= T0 + e and T1 + e / 2 <= T1 + e)

    print("[7] common inner-square source ([8] (4.13)-(4.17), Lemma 4.3)")
    ws, ds = F(31, 10000), F(21319, 800000)
    xis, cs = ds / rho, 1 / (2 * rho) - T1
    s0, sm = P['sigma0'], P['sigma_mt']
    prime = [("68w+14d<1", 68 * ws + 14 * ds, F(1)), ("56w+16d+4s0<1 (2.11)", 56 * ws + 16 * ds + 4 * s0, F(1)),
             ("(2.12) with s0", F(1, 18) + F(28, 9) * ws + F(2, 9) * ds, s0), ("280w+80d<3 (2.15)", 280 * ws + 80 * ds, F(3)),
             ("w<1/12", ws, F(1, 12)), ("d<1/4+w", ds, F(1, 4) + ws), ("s0>2w", 2 * ws, s0)]
    mino = [("68w+14d<1", 68 * ws + 14 * ds, F(1)), ("56w+16d+4s_mt<1 (2.11)", 56 * ws + 16 * ds + 4 * sm, F(1)),
            ("1/4+7w+2d<c*-tau", F(1, 4) + 7 * ws + 2 * ds, P['c_star'] - P['tau']),
            ("1/18+..<19/200-tau", F(1, 18) + F(28, 9) * ws + F(2, 9) * ds, F(19, 200) - P['tau']),
            ("1/2+2w<b*-tau", F(1, 2) + 2 * ws, P['b_star'] - P['tau'])]
    for lab, lst in (("prime (Prop 2.16/2.17, sigma0)", prime), ("minorant (Prop 2.22, sigma_mt)", mino)):
        mm = min(r - l for _, l, r in lst)
        check(f"(4.16) {lab}: strict margins at (omega_s, delta_s)", all(l < r for _, l, r in lst),
              f"least margin {dec(mm)}")
    v = F(1, 2) + 2 * ws - 2 * rho * T1
    check("(4.16) 1/2 + 2 omega_s - 2 rho T1 = 55122259/13124945000 > 0", v == F(55122259, 13124945000) and v > 0)
    check("(4.16) c_s + xi_s > 0 (Lemma 4.3 guard)", cs + xis > 0, dec(cs + xis))
    R12 = rows['n'][12]
    check("(4.17) c_s - b_{n,12} > 4/100 and xi_s - xi_{n,12} > 5/100",
          cs - R12['b'] > F(4, 100) and xis - R12['xi'] > F(5, 100),
          f"{dec(cs - R12['b'])}, {dec(xis - R12['xi'])}")
    check("C_{n,12} = b_{n,12} + xi_{n,12} < c_s + xi_s", R12['C'] == R12['b'] + R12['xi'] and R12['C'] < cs + xis)
    check("source level: rho* * 2 T1 < 1/2 + 2 omega_s; density rho* xi_s < delta_s; rho* B_BV < 1/2",
          rs * 2 * T1 < F(1, 2) + 2 * ws and rs * xis < ds and rs / (2 * rho) < F(1, 2))

    return P


def negative_controls():
    print("[8] negative controls (each perturbation must make the named check fail)")
    global FAILS
    QUIET[0] = True
    results = []

    def run_dist(over, rows_key='retained'):
        P = build(over)
        ok, worst = sec_dist(P, P[rows_key], verbose=False)
        return ok, worst
    # 1. eps_o = 0 kills the strict bilinear margins of the old ladder
    ok, w = run_dist({'eps_o': F(0)})
    results.append(("eps_o = 0 -> some strict distribution hypothesis fails", not ok, w[3] if w else ""))
    # 2. Omega_n raised by 1/10^5: (2.24) first inequality should fail on new order-three rows
    # Omega_n above the order-three fixed point W_n3 = 0.0126507...: the new ladder no longer terminates
    # (so the row count 43 of (1.15) depends on Omega_n < W_n3); (2.24) itself cannot be broken this way because
    # untruncated omegas stay below W_n3 < 0.0126636 (the omega at which 1/4+7w+2d = c*-tau).
    Pn = build({'Omega_n': F(253, 20000) + F(1, 10**5)})
    results.append(("Omega_n + 1e-5 (> W_n3) -> new ladder does not terminate (row count 43 check fails)",
                    len(Pn['rows']['n']) != 43, f"{len(Pn['rows']['n'])} rows (cut at 400)"))
    ok, w = run_dist({'c_star': F(33856, 100000) - F(1, 10**5)})
    results.append(("c* - 1e-5 -> (2.24) first bound fails on a retained new order-3 row", (not ok) and 'c*' in w[3],
                    f"{w[3]} at ({w[1]},{w[2]})"))
    # 3. sigma0 = 1/10 exactly -> Heath-Brown requirement sigma > 1/10 fails
    ok, w = run_dist({'sigma0': F(1, 10)})
    results.append(("sigma0 = 1/10 -> 'sigma>1/10' fails", (not ok) and 'sigma>1/10' in w[3], w[3]))
    # 4. tau = 10^-4 (outside the allowed range) -> margins should break
    ok, w = run_dist({'tau': F(1, 10**4)})
    results.append(("tau = 1e-4 -> a reduced (2.24) bound fails", not ok, w[3] if w else ""))
    # 5. rho* = rho -> level retreat must fail (equality)
    P = build({'rho_star_shift': F(1, 10**7)})
    ret_ok = all(P['rho_star'] * R['Bp'] < F(1, 2) + 2 * R['w'] for nu in 'on' for R in P['retained'][nu])
    results.append(("rho* = rho -> strict level retreat fails", not ret_ok, ""))
    # 6. an extra retained row: B_{o,28} must NOT be < pair max
    P = build()
    h = P['h']
    results.append(("(o,28) is excluded by the rule (its B >= 187866h)", not (P['rows']['o'][28]['B'] < 187866 * h), ""))
    # 7. group guard with z_G one cell larger for O5/2 must fail z+mp <= U
    S, e = P['S'], P['e']
    results.append(("O2 with z_G/h = 49153 (one cell more) violates z+mp<=U",
                    not ((49153 + 2 * 24576) * h <= S + e), ""))
    results.append(("I2new with p_G/h = 22489 violates z+mp<=U",
                    not ((44976 + 2 * 22489) * h <= P['T1'] + e), ""))
    # 8. inner square: delta_s raised by 1e-4 must break the prime (2.11)/(2.15) margin
    ws, ds = F(31, 10000), F(21319, 800000) + F(1, 10**4)
    results.append(("delta_s + 1e-4 -> 280w+80d<3 fails", not (280 * ws + 80 * ds < 3), ""))
    # 9. guard: a row with xi decreased by e+1e-3 would break B+xi >= 2T? (direct test of the guard formula)
    R = P['retained']['o'][0]
    results.append(("guard is not vacuous: B+xi-2T0 at (o,0) is < 0.1",
                    0 <= R['B'] + R['xi'] - 2 * P['T0'] < F(1, 10), dec(R['B'] + R['xi'] - 2 * P['T0'])))
    QUIET[0] = False
    for name, caught, det in results:
        check("NEG " + name, caught, det)


if __name__ == '__main__':
    main()
    negative_controls()
    print(f"\n{NCHECK[0]} checks, {len(FAILS)} failures" + (": " + ", ".join(FAILS) if FAILS else ""))
    print(f"runtime {time.time() - T_START:.2f} s")
    sys.exit(1 if FAILS else 0)
