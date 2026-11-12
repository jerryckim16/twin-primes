#!/usr/bin/env python3
"""Certificate for Theorem 15 (Theorem 13 in paper v0.3): M_{29,eps} < 3.99 for every 0 <= eps < 1.

Dual bound (Lemma 13 with the two-zone weight of Theorem 15; Lemma 11 and Theorem 13 in v0.3): for 0 < tau < s1 <= L, a >= s1,
    M_k(L, tau) <= sup_{0<=sigma<=tau} W(sigma),
    W(sigma) = k a/(k-1) * log(1 + (k-1)(s1-sigma)/(a-sigma)) + L - s1 + sigma*log((L-sigma)/(s1-sigma)).
M_{k,eps} = M_k(1+eps, 1-eps), non-decreasing in L and in tau.

Plan:
  * eps <= 143/1000: Proposition 12 gives M_{29,eps} <= (1+eps) * 29/28 * log 29 < 3.9863.
  * [143/1000, 1] is cut into 857 intervals [e, e'] of length 1/1000.  For each one we choose
    rational (a, s1) numerically and prove sup W < 3.99 for (L, tau) = (1+e', 1-e).
The first logarithm in W is non-increasing in sigma (a >= s1) and the rest is non-decreasing (L >= s1),
so on [x, y] we bound W by first(x) + rest(y), in arb ball arithmetic at rational points, bisecting
until every piece is below the target.

usage: dual_eps_cert.py [--out code/cert_floor_k29.json]
"""
import sys, json
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import minimize
import flint
from flint import arb, fmpq

K = 29
TARGET = Fr(399, 100)
E0 = Fr(143, 1000)
STEP = Fr(1, 1000)
flint.ctx.prec = 128


def W_float(s, k, L, tau, a, s1):
    return (k * a / (k - 1) * np.log1p((k - 1) * (s1 - s) / (a - s))
            + L - s1 + s * np.log((L - s) / (s1 - s)))


def supW_float(k, L, tau, a, s1, n=400):
    if not (a >= s1 > tau and s1 <= L):
        return 1e9
    s = np.linspace(0.0, tau, n)
    return float(np.max(W_float(s, k, L, tau, a, s1)))


def choose(k, L, tau, guess=None):
    """Numerically pick (a, s1) minimising sup W; parametrised to keep a >= s1 > tau, s1 <= L."""
    def unpack(x):
        s1 = tau + (L - tau) / (1 + np.exp(-x[0]))
        a = s1 + np.exp(x[1])
        return a, s1
    best = None
    starts = [guess] if guess is not None else []
    starts += [np.array([p, q]) for p in (-2.0, 0.0, 2.0) for q in (-1.0, 0.5, 2.0)]
    for x0 in starts:
        r = minimize(lambda x: supW_float(k, L, tau, *unpack(x)), x0, method="Nelder-Mead",
                     options=dict(xatol=1e-7, fatol=1e-9, maxiter=2000))
        if best is None or r.fun < best.fun:
            best = r
    a, s1 = unpack(best.x)
    return a, s1, best.fun, best.x


def A(q):
    return arb(fmpq(q.numerator, q.denominator))


def first(k, a, s1, x):
    return A(Fr(k) * a / (k - 1)) * (1 + A((k - 1) * (s1 - x) / (a - x))).log()


def rest(L, s1, y):
    if y == 0:
        return A(L - s1)
    return A(L - s1) + A(y) * A((L - y) / (s1 - y)).log()


def certify_box(k, L, tau, a, s1, target, max_depth=40):
    """Return the number of pieces used, or None if some piece could not be pushed below target."""
    stack = [(Fr(0), tau, 0)]
    pieces = 0
    while stack:
        x, y, d = stack.pop()
        ub = first(k, a, s1, x) + rest(L, s1, y)
        if ub < A(target):
            pieces += 1
            continue
        if d >= max_depth:
            return None
        m = (x + y) / 2
        stack += [(x, m, d + 1), (m, y, d + 1)]
    return pieces


def rat(v, den=10**6):
    return Fr(round(v * den), den)


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "code/cert_floor_k29.json"
    # small eps: Proposition 12
    small = A((1 + E0) * Fr(K, K - 1)) * arb(K).log()
    assert small < A(TARGET), small
    rows, guess, worst = [], None, 0.0
    n = int((1 - E0) / STEP)
    for i in range(n):
        e, e2 = E0 + i * STEP, E0 + (i + 1) * STEP
        L, tau = 1 + e2, 1 - e
        a, s1, fval, guess = choose(K, float(L), float(tau), guess)
        a_q, s1_q = rat(a), rat(s1)
        if s1_q <= tau:
            s1_q = tau + Fr(1, 10**6)
        if s1_q > L:
            s1_q = L
        if a_q < s1_q:
            a_q = s1_q
        pieces = certify_box(K, L, tau, a_q, s1_q, TARGET)
        if pieces is None:
            raise SystemExit("failed on eps in [%s, %s] (float sup W = %.6f)" % (e, e2, fval))
        worst = max(worst, fval)
        rows.append(dict(e=str(e), e2=str(e2), a=str(a_q), s1=str(s1_q), pieces=pieces, supW_float=round(fval, 6)))
        if i % 50 == 0:
            print("eps in [%s, %s]: a=%s s1=%s supW~%.5f pieces=%d" % (e, e2, a_q, s1_q, fval, pieces), flush=True)
    cert = dict(k=K, target=str(TARGET), small_eps=dict(upto=str(E0), bound=str(small.upper()),
                reason="Proposition 12: (1+eps)*k/(k-1)*log k"),
                intervals=rows, worst_float_supW=round(worst, 6))
    json.dump(cert, open(out, "w"), indent=0)
    print("certified %d intervals; worst float sup W = %.6f; wrote %s" % (len(rows), worst, out))


if __name__ == "__main__":
    main()
