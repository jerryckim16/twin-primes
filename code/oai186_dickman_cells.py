#!/usr/bin/env python3
"""Rung 186, first sub-step (Session 13): independent closed-form evaluation of the Dickman cell masses
A_j(c) = int_{jh}^{(j+1)h} rho_D(t/c) dt of [14] (OpenAI, short_gaps_numerics.pdf, Sec. 2, Lemma 2.2), for every
grid cap c = M h of the table (1.5), and a test of the enclosures (2.1)-(2.2) AS TRANSCRIBED in
notes/sources-186-forms.md (Section 1), whose upper/lower assignment was marked "[reading]".

Closed forms (u = t/c <= 98304/35265 < 3 on the grid):
  rho = 1 on [0,1];  1 - log u on [1,2];  1 - log u + (log u)^2/2 + Li2(1/u) - K on [2,3], K = (log 2)^2/2 + Li2(1/2)
  (from rho'(u) = -rho(u-1)/u and int log(t-1)/t dt = (log t)^2/2 + Li2(1/t)).
  Phi = int_0^u rho: u;  2u - u log u - 1;  Phi(2) + G(u) - G(2) with
  G(u) = 2u - u log u + u((log u)^2 - 2 log u + 2)/2 + u Li2(1/u) - (u-1) log(u-1) + u log u - K u.
  d_j := A_j/h = M (Phi((j+1)/M) - Phi(j/M)).
High-precision floating point (mp.dps = 40), NOT interval arithmetic; rounding errors are below 1e-30, far below the
margins tested. The recurrence is run at the same precision (directed rounding of [14] not reproduced; irrelevant at
this precision).
usage: oai186_dickman_cells.py [--caps 68225,49152,...] [--out f.json]"""
import sys, json
from mpmath import mp, mpf, log, polylog, quad
mp.dps = 40
K = log(2) ** 2 / 2 + polylog(2, mpf(1) / 2)

def rho(u):
    if u <= 1: return mpf(1)
    if u <= 2: return 1 - log(u)
    return 1 - log(u) + log(u) ** 2 / 2 + polylog(2, 1 / u) - K

def G(u):
    return 2 * u - u * log(u) + u * (log(u) ** 2 - 2 * log(u) + 2) / 2 + u * polylog(2, 1 / u) - (u - 1) * log(u - 1) + u * log(u) - K * u

PHI2 = 3 - 2 * log(2)
G2 = G(mpf(2))

def Phi(u):
    if u <= 1: return u
    if u <= 2: return 2 * u - u * log(u) - 1
    return PHI2 + G(u) - G2

def selftest():
    for u in [mpf('0.5'), mpf('1.3'), mpf('1.99'), mpf('2.2'), mpf('2.79')]:
        q = quad(rho, [0, 1, 2, u] if u > 2 else ([0, 1, u] if u > 1 else [0, u]))
        assert abs(q - Phi(u)) < mpf(10) ** -30, (u, q, Phi(u))
    # ODE check rho'(u) = -rho(u-1)/u at a few points
    for u in [mpf('1.5'), mpf('2.5'), mpf('2.9')]:
        e = mpf(10) ** -12
        der = (rho(u + e) - rho(u - e)) / (2 * e)
        assert abs(der + rho(u - 1) / u) < mpf(10) ** -15
    print("selftest ok (Phi vs quadrature, rho' = -rho(u-1)/u)")

NMAX = 98264          # cells j = 0 .. n-1 used by the grid (n = N - 40)

def check_cap(M):
    """Recurrence (2.1) and cell enclosure (2.2) as transcribed, vs the closed form."""
    M = int(M)
    jmax = NMAX + 1
    lo = [mpf(1)] * (jmax + 2); up = [mpf(1)] * (jmax + 2)
    for j in range(M, jmax + 1):
        lo[j + 1] = max(mpf(0), lo[j] - up[j - M] / (2 * j) - up[j + 1 - M] / (2 * (j + 1)))
        up[j + 1] = min(mpf(1), up[j] - lo[j - M] / (2 * j) - lo[j + 1 - M] / (2 * (j + 1)) + mpf(1) / (2 * M ** 3))
    # NB: the update of index j+1 uses up/lo[j+1-M], which for j+1-M <= M is the initial value 1 (consistent).
    bad_pt = bad_cell = 0
    worst_pt = worst_cell = mpf(0)          # min slack (negative = violation), relative to the margin size
    maxwidth = mpf(0)
    step = 1 if M < 40000 else 1
    phis = {}
    def P(j):
        if j not in phis: phis[j] = Phi(mpf(j) / M)
        return phis[j]
    slack_pt_min = mpf(1); slack_cell_min = mpf(1)
    for j in range(M, NMAX, step):
        r = rho(mpf(j) / M)
        sl = min(r - lo[j], up[j] - r)
        slack_pt_min = min(slack_pt_min, sl)
        if sl < 0: bad_pt += 1
        d = M * (P(j + 1) - P(j))                       # A_j / h
        clo = max(mpf(0), (lo[j] + lo[j + 1]) / 2 - mpf(1) / (12 * M ** 2))   # (2.2)/h: h^3/(12 c^2) / h = 1/(12 M^2)
        cup = min(mpf(1), (up[j] + up[j + 1]) / 2)
        sc = min(d - clo, cup - d)
        slack_cell_min = min(slack_cell_min, sc)
        if sc < 0: bad_cell += 1
        maxwidth = max(maxwidth, cup - clo)
    return dict(M=M, cells=NMAX - M, point_violations=bad_pt, cell_violations=bad_cell,
                min_point_slack=float(slack_pt_min), min_cell_slack=float(slack_cell_min), max_cell_width=float(maxwidth),
                d_last=float(M * (P(NMAX) - P(NMAX - 1))))

if __name__ == "__main__":
    selftest()
    caps = [68225, 49152, 46580, 44781, 35265, 44976, 35419]
    if "--caps" in sys.argv:
        caps = [int(x) for x in sys.argv[sys.argv.index("--caps") + 1].split(",")]
    res = []
    for M in caps:
        r = check_cap(M)
        print(json.dumps(r), flush=True)
        res.append(r)
    if "--out" in sys.argv:
        json.dump(res, open(sys.argv[sys.argv.index("--out") + 1], "w"), indent=1)
