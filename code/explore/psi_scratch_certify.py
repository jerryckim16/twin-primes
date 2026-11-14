#!/usr/bin/env python3
"""Scratch (Session 15 helper; see notes/psi-weight/attempt-helper.md): rigorous (interval-arithmetic) upper bound for
   sup over R = {(s,nu): 0<=s<=tau, nu>=1, (nu-1)W <= tau-s} of
   G(s,nu) = F(s) + int_0^W nu/(c0 + nu s + (nu-1) w) dw,
   F(s) = k/(k-1) log((c0+ks)/(c0+s)),  W = 2eps, c0 = a - tau.
By Lemma J of notes/psi-weight/attempt-helper.md, a*sup_{t'} I(a,t') <= a*sup_R G.
Cell bound on [s1,s2]x[n1,n2]:  F(s2) + int_0^{w*} (n2, s1) + int_{w*}^W (n1, s1),  w* = clip(c0,0,W)
(F increasing in s; integrand decreasing in s; increasing in nu iff w < c0).
Adaptive bisection in floats, then every leaf re-evaluated with mpmath.iv (outward rounding).
usage: psi_scratch_certify.py a_num a_den theta    e.g. 1037 1000 4.1500"""
import sys
from math import log
from fractions import Fraction
import mpmath
from mpmath import iv
iv.prec = 80

k = 50
A_NUM, A_DEN = int(sys.argv[1]), int(sys.argv[2])
THETA = float(sys.argv[3])
# floats for the search
eps = 1 / 25; tau = 1 - eps; W = 2 * eps; a = A_NUM / A_DEN; c0 = a - tau
# intervals for the certificate
EPS_I = iv.mpf(1) / 25; TAU_I = 1 - EPS_I; W_I = 2 * EPS_I
A_I = iv.mpf(A_NUM) / A_DEN; C0_I = A_I - TAU_I

def Jf(nu, s, lo, hi):
    if hi <= lo: return 0.0
    if nu == 1.0: return (hi - lo) / (c0 + s)
    c = c0 + nu * s
    return nu / (nu - 1) * log((c + (nu - 1) * hi) / (c + (nu - 1) * lo))

def Ji(nu, s, lo, hi):
    if nu == 1:
        return (hi - lo) / (C0_I + s)
    c = C0_I + nu * s
    return nu / (nu - 1) * iv.log((c + (nu - 1) * hi) / (c + (nu - 1) * lo))

def Ub_f(s1, s2, n1, n2):
    ws = min(max(c0, 0.0), W)
    F = k / (k - 1) * log((c0 + k * s2) / (c0 + s2))
    return a * (F + Jf(n2, s1, 0.0, ws) + Jf(n1, s1, ws, W))

def Ub_i(s1, s2, n1, n2):
    last = (s2 == tau)
    s1, s2, n1i, n2i = iv.mpf(s1), iv.mpf(s2), iv.mpf(n1), iv.mpf(n2)
    if last:  # float tau < 24/25: use an enclosure of the true tau as right end (F is increasing)
        s2 = iv.mpf([float(TAU_I.a), float(TAU_I.b) + 1e-15])
    # w* = c0 here (we assert 0 < c0 < W rigorously below)
    F = iv.mpf(k) / (k - 1) * iv.log((C0_I + k * s2) / (C0_I + s2))
    J = Ji(n2i if n2 != 1.0 else 1, s1, iv.mpf(0), C0_I) + Ji(n1i if n1 != 1.0 else 1, s1, C0_I, W_I)
    return A_I * (F + J)

def in_region_i(s1, n1):
    # cell can be discarded only if (n1-1) W > tau - s1 for sure
    lhs = (iv.mpf(n1) - 1) * W_I; rhs = TAU_I - iv.mpf(s1)
    return not (lhs.a > rhs.b)

def main():
    assert C0_I.a > 0 and C0_I.b < W_I.a
    stack = []
    NS, NN = 24, 12
    for i in range(NS):
        for j in range(NN):
            stack.append((tau * i / NS if i else 0.0, tau * (i + 1) / NS if i < NS - 1 else None, 1.0 + j, 2.0 + j, 0))
    leaves = []; best_f = 0
    while stack:
        s1, s2, n1, n2, d = stack.pop()
        if s2 is None: s2 = tau  # last cell: right end = tau (float); covered: tau_float >= ? checked below
        if (n1 - 1) * W > tau - s1 + 1e-12: 
            if not in_region_i(s1, n1): continue
        u = Ub_f(s1, s2, n1, n2)
        if u < THETA - 1e-6 or d > 40:
            leaves.append((s1, s2, n1, n2, u)); best_f = max(best_f, u); continue
        if (s2 - s1) * 40 > (n2 - n1) or d % 2 == 0 and (s2 - s1) > 1e-9:
            m = 0.5 * (s1 + s2); stack += [(s1, m, n1, n2, d + 1), (m, s2, n1, n2, d + 1)]
        else:
            m = 0.5 * (n1 + n2); stack += [(s1, s2, n1, m, d + 1), (s1, s2, m, n2, d + 1)]
    print("leaves:", len(leaves), " max float cell bound: %.7f" % best_f, flush=True)
    worst = iv.mpf(0); bad = 0
    for (s1, s2, n1, n2, u) in leaves:
        if not in_region_i(s1, n1): continue
        ub = Ub_i(s1, s2, n1, n2)
        if ub.b > worst.b: worst = ub
        if not (ub.b < THETA): bad += 1
    # coverage of s up to tau: the float tau may be below the true tau = 24/25
    print("last s-cell right end replaced by an enclosure of 24/25 (float tau < 24/25: %s)" % (Fraction(tau) < Fraction(24, 25)))
    print("interval max leaf bound (upper end): %s ; cells failing theta=%s: %d" % (mpmath.nstr(mpmath.mpf(worst.b), 12), THETA, bad))

if __name__ == "__main__":
    main()
