#!/usr/bin/env python3
"""Polymath8b's explicit lower bound for M_k^{[T]} (Theorem 6.7) and the H_2 criterion.

Source: D.H.J. Polymath, "Variants of the Selberg sieve, and bounded intervals
containing many primes", arXiv:1407.4897v4, Theorem 6.7, eqs. (100)-(113),
pp. 46-47 (LaTeX source label `explicit`, eqs. g-def ... U-def), with the
parameter choice of p. 54-55:  c = theta/log k, T = beta/log k, tau = 1 - k mu,
and Table 2 (p. 55).  Theorem 6.7 says: if
    (104) k mu <= 1 - tau,  (105) k mu < 1 - T,  (106) k sigma^2 < (1+tau-k mu)^2,
then
    k/(k-1) log k - M_k^{[T]} <= k/(k-1) (Z+Z3+WX+VU) / ((1+tau/2)(1 - k sigma^2/(1+tau-k mu)^2)).

Criteria for DHL[k, m+1] (hence H_m <= H(k)), quoted in notes/hm-programme.md:
  * Theorem 3.8 (p. 13): EH[vartheta] and M_k > 2m/vartheta.  Bombieri-Vinogradov gives
    EH[vartheta] for every vartheta < 1/2, so under BV alone: M_k > 4m (m = 2: M_k > 8).
  * Theorem 3.10 (p. 14): MPZ[varpi, delta] and M_k^{[delta/(1/4+varpi)]} > m/(1/4+varpi).
    MPZ region of Polymath8a (Theorem 2.5 of PM8b): 600 varpi + 180 delta < 7.
    MPZ region of Stadlmann (arXiv:2309.00425v3, Cor. 2 / p. 9): 80 varpi + 80 delta/3 < 1.
    With delta = T (1/4+varpi) (PM8b p. 55) and varpi -> m/Mlow - 1/4 the condition is
    600 (m/Mlow - 1/4) + 180 T m/Mlow < 7 (resp. 80 (m/Mlow - 1/4) + (80/3) T m/Mlow < 1).

All quantities are evaluated in ball arithmetic (python-flint arb; integrals by
acb.integral, which returns rigorous enclosures).  theta, beta are exact decimal
rationals, so c, T, tau are specific reals and every ball encloses the true value:
a lower endpoint above the threshold is a proof (given Theorem 6.7).  The search
for the smallest k (optimising theta, beta by Nelder-Mead at low precision) is
heuristic; only the final certified checks are rigorous.

m2, int t g^2, int t^2 g^2, U and the log t part of W are in closed form; the
singular part of W uses  int_0^T log t /(c+at)^2 dt = F(T) + log c/(ac),
F(t) = -log t/(a(c+at)) + log(t/(c+at))/(ac).

Usage: python3 -I pm8b_mk_lower.py [out.json]      (single core, a few minutes)
"""
import sys, json, time
from flint import arb, acb, fmpq, ctx

def q(s):
    """Exact rational from a decimal string."""
    s = str(s)
    if '.' in s:
        a, b = s.split('.')
        return fmpq(int(a + b), 10 ** len(b))
    return fmpq(int(s))

def integral(f, a, b):
    return acb.integral(lambda x, an: f(x, an), acb(a), acb(b)).real

def bound(k, theta, beta):
    """Return dict with Mlow (arb lower-bound ball for M_k^{[T]}) and checks."""
    k_ = arb(k); a = arb(k - 1); L = k_.log()
    c = arb(theta) / L; T = arb(beta) / L
    u0, u1 = c, c + a * T
    m2 = (1 / u0 - 1 / u1) / a
    It1 = ((u1.log() + c / u1) - (u0.log() + c / u0)) / a ** 2
    It2 = ((u1 - 2 * c * u1.log() - c * c / u1) - (u0 - 2 * c * u0.log() - c * c / u0)) / a ** 3
    mu = It1 / m2
    sig2 = It2 / m2 - mu * mu
    kmu = k_ * mu
    tau = 1 - kmu
    ok104 = True                       # equality by the choice tau = 1 - k mu
    ok105 = bool(tau > T)              # k mu < 1 - T
    ok106 = bool(k_ * sig2 < (1 + tau - kmu) ** 2)
    okpos = bool(tau > 0) and bool(c > 0) and bool(T > 0)
    if not (ok105 and ok106 and okpos):
        return dict(ok=False, Mlow=None, ok105=ok105, ok106=ok106)
    ksig2 = k_ * sig2
    cA, cT, cK = acb(kmu), acb(T), acb(k_)
    def zint(r, an):
        d = r - cA
        lg = (d / cT).log(analytic=an)
        return r * (lg + acb(ksig2) / (4 * d * d * lg)) + r * r / (4 * cK * cT)
    Z = integral(zint, arb(1), 1 + tau) / tau
    cc, ca = acb(c), acb(a)
    g2 = lambda t: 1 / (cc + ca * t) ** 2
    Z3 = integral(lambda t, an: cK * t * (1 + t / cT).log(analytic=an) * g2(t), arb(0), T) / m2
    # W = (1/m2) int_0^T [log(kt+tau) - log k - log t] g^2
    ctau = acb(tau)
    I_log_ktau = integral(lambda t, an: (cK * t + ctau).log(analytic=an) * g2(t), arb(0), T)
    F = lambda t: -t.log() / (a * (c + a * t)) + (t / (c + a * t)).log() / (a * c)
    I_logt = F(T) + c.log() / (a * c)
    W = (I_log_ktau - L * m2 - I_logt) / m2
    X = L * c * c / tau
    V = c * integral(lambda t, an: g2(t) / (2 * cc + ca * t), arb(0), T) / m2
    A = 1 - a * mu - c
    U = L / c * (A * A + A * tau + tau * tau / 3 + a * sig2)
    num = Z + Z3 + W * X + V * U
    den = (1 + tau / 2) * (1 - ksig2 / (1 + tau - kmu) ** 2)
    Mlow = k_ / a * L - k_ / a * num / den
    return dict(ok=True, Mlow=Mlow, T=T, c=c, tau=tau, kmu=kmu, ksig2=ksig2,
                Z=Z, Z3=Z3, W=W, X=X, V=V, U=U, ok105=ok105, ok106=ok106)

def lo(x): return float(x.lower())
def hi(x): return float(x.upper())

# ---- criteria -------------------------------------------------------------
def crit_bv(r, m):          # Theorem 3.8 with vartheta -> 1/2: need M > 4m
    return lo(r['Mlow']) - 4 * m
def mpz_lhs(r, m, region):  # value of the MPZ constraint at varpi* = m/M - 1/4
    M = arb(r['Mlow'].lower())          # lower endpoint, rigorous direction
    w = arb(m) / M - arb(1) / 4
    d = r['T'] * (arb(m) / M)           # delta = T (1/4 + varpi)
    if region == 'pm8a':
        return 600 * w + 180 * d, arb(7), w, d
    return 80 * w + 80 * d / 3, arb(1), w, d
def crit_mpz(r, m, region):
    lhs, rhs, w, d = mpz_lhs(r, m, region)
    return float(rhs.lower()) - float(lhs.upper()), w, d

# ---- optimisation (heuristic; precision lowered) ---------------------------
def nelder_mead(f, x0, step, iters=120):
    pts = [list(x0)] + [[x0[j] + (step[j] if i == j else 0) for j in range(2)] for i in range(2)]
    vals = [f(p) for p in pts]
    for _ in range(iters):
        o = sorted(range(3), key=lambda i: vals[i]); pts = [pts[i] for i in o]; vals = [vals[i] for i in o]
        cen = [(pts[0][j] + pts[1][j]) / 2 for j in range(2)]
        xr = [cen[j] + (cen[j] - pts[2][j]) for j in range(2)]; fr = f(xr)
        if fr < vals[0]:
            xe = [cen[j] + 2 * (cen[j] - pts[2][j]) for j in range(2)]; fe = f(xe)
            pts[2], vals[2] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[1]:
            pts[2], vals[2] = xr, fr
        else:
            xc = [cen[j] + 0.5 * (pts[2][j] - cen[j]) for j in range(2)]; fc = f(xc)
            if fc < vals[2]:
                pts[2], vals[2] = xc, fc
            else:
                for i in (1, 2):
                    pts[i] = [pts[0][j] + 0.5 * (pts[i][j] - pts[0][j]) for j in range(2)]
                    vals[i] = f(pts[i])
    i = min(range(3), key=lambda i: vals[i]); return pts[i], vals[i]

def best_margin(k, kind, m, x0):
    """maximise the criterion margin over (theta, beta) at low precision."""
    old = ctx.prec; ctx.prec = 80
    def f(x):
        th, be = x
        if th <= 0 or be <= 0: return 1e9
        r = bound(k, fmpq(round(th * 10**8), 10**8), fmpq(round(be * 10**8), 10**8))
        if not r['ok']: return 1e9
        if kind == 'bv': return -crit_bv(r, m)
        return -crit_mpz(r, m, kind)[0]
    x, v = nelder_mead(f, x0, [0.01, 0.01])
    ctx.prec = old
    return x, -v

def round_params(x, digits=5):
    return [fmpq(round(t * 10**digits), 10**digits) for t in x]

def smallest_k(kind, m, lo_k, hi_k, x0):
    """bisection on k for 'criterion holds with optimised (theta,beta)'; heuristic monotone."""
    cache = {}
    def good(k):
        if k not in cache:
            x, v = best_margin(k, kind, m, x0)
            # certify at the rounded parameters at full precision
            th, be = round_params(x, 6)
            r = bound(k, th, be)
            mg = crit_bv(r, m) if kind == 'bv' else crit_mpz(r, m, kind)[0]
            cache[k] = (mg > 0, th, be, mg)
        return cache[k][0]
    assert good(hi_k) and not good(lo_k), (kind, cache)
    while hi_k - lo_k > 1:
        mid = (lo_k + hi_k) // 2
        if good(mid): hi_k = mid
        else: lo_k = mid
    return hi_k, cache[hi_k], cache.get(lo_k)

def s(x): return x.str(15, radius=False) if isinstance(x, arb) else str(x)

def main():
    ctx.prec = 256
    out = {"source": "Polymath8b arXiv:1407.4897v4, Thm 6.7 (pp.46-47), params p.54-55, Table 2 (p.55)",
           "criteria": {"BV (Thm 3.8, vartheta->1/2)": "M_k > 4m",
                        "MPZ (Thm 3.10)": "M_k^[T] > m/(1/4+varpi), delta = T(1/4+varpi)",
                        "pm8a region (PM8b Thm 2.5)": "600 varpi + 180 delta < 7",
                        "stadlmann region (2309.00425v3 p.9)": "80 varpi + 80 delta/3 < 1"},
           "table2_reproduction": [], "searches": {}}
    t0 = time.time()
    table2 = [(5511, '0.965', '0.973', '6.000048609'),
              (35410, '0.99479', '0.85213', '7.829849259'),
              (41588, '0.97878', '0.94319', '8.000001401'),
              (309661, '0.98627', '0.92091', '10.00000032'),
              (1649821, '1.00422', '0.80148', '11.65752556'),
              (35265, '0.99479', '0.85213', None)]   # Stadlmann 2023's k with PM8b's (theta,beta)
    for k, th, be, Mpub in table2:
        r = bound(k, q(th), q(be))
        row = dict(k=k, theta=th, beta=be, Mlow=s(r['Mlow']), Mlow_lower=lo(r['Mlow']),
                   M_published=Mpub, T=s(r['T']), tau=s(r['tau']),
                   hyp_105=r['ok105'], hyp_106=r['ok106'],
                   parts={n: s(r[n]) for n in ('Z', 'Z3', 'W', 'X', 'V', 'U')})
        if Mpub is not None:
            row['exceeds_published'] = bool(r['Mlow'] > arb(q(Mpub)))
        for reg in ('pm8a', 'stadlmann'):
            mg, w, d = crit_mpz(r, 2, reg)
            row['m2_' + reg] = dict(margin=mg, varpi=s(w), delta=s(d), holds=mg > 0)
        row['m2_bv_margin'] = crit_bv(r, 2)
        out['table2_reproduction'].append(row)
        print(k, row['Mlow'], Mpub, row.get('exceeds_published'), row['m2_pm8a'], row['m2_stadlmann'],
              'bv:', row['m2_bv_margin'], flush=True)
    # smallest k for m = 2 under each input
    for kind, lo_k, hi_k, x0 in (('pm8a', 34000, 35410, [0.995, 0.852]),
                                 ('stadlmann', 34000, 35410, [0.995, 0.852]),
                                 ('bv', 40000, 41588, [0.979, 0.943])):
        k, (_, th, be, mg), prev = smallest_k(kind, 2, lo_k, hi_k, x0)
        r = bound(k, th, be)
        info = dict(k_min=k, theta=str(th), beta=str(be), margin=mg, Mlow=s(r['Mlow']),
                    k_minus_1=None if prev is None else dict(margin_best_found=prev[3]))
        if kind != 'bv':
            _, w, d = crit_mpz(r, 2, kind); info.update(varpi=s(w), delta=s(d))
        out['searches'][kind + '_m2'] = info
        print(kind, info, flush=True)
    out['seconds'] = round(time.time() - t0, 1)
    out['note'] = ("k_min is the smallest k for which Nelder-Mead found (theta,beta) making the "
                   "certified criterion hold; minimality is heuristic (optimiser + monotonicity), "
                   "the criterion at k_min is rigorous given Thm 6.7.")
    path = sys.argv[1] if len(sys.argv) > 1 else 'pm8b_mk_lower.json'
    with open(path, 'w') as fh: json.dump(out, fh, indent=1)

if __name__ == '__main__':
    main()
