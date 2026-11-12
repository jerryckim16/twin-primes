#!/usr/bin/env python3
"""Independent re-check of code/cert_floor_k29.json with a different interval library (mpmath.iv).

For each interval [e, e'] it reads the stored rationals (a, s1), checks a >= s1 > tau, s1 <= L for
(L, tau) = (1+e', 1-e), and re-runs the bisection with mpmath interval arithmetic, bounding
W(sigma) on [x, y] by first(x) + rest(y) (first is non-increasing, rest non-decreasing; Theorem 13).
It also checks that the intervals cover [143/1000, 1] and re-checks the Proposition 12 bound.

usage: check_floor_cert.py [code/cert_floor_k29.json]
"""
import sys, json
from fractions import Fraction as Fr
from mpmath import iv

iv.prec = 120


def I(q):
    q = Fr(q)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def bound(k, L, s1, a, x, y):
    f = I(Fr(k) * a / (k - 1)) * iv.log(1 + I((k - 1) * (s1 - x) / (a - x)))
    g = I(L - s1) + (I(y) * iv.log(I((L - y) / (s1 - y))) if y else 0)
    return f + g


def check_interval(k, L, tau, a, s1, target, max_depth=45):
    assert a >= s1 > tau and s1 <= L, (a, s1, tau, L)
    stack, pieces = [(Fr(0), tau, 0)], 0
    while stack:
        x, y, d = stack.pop()
        if bound(k, L, s1, a, x, y).b < I(target).a:
            pieces += 1
            continue
        if d >= max_depth:
            return None
        m = (x + y) / 2
        stack += [(x, m, d + 1), (m, y, d + 1)]
    return pieces


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "code/cert_floor_k29.json"
    c = json.load(open(path))
    k, target = c["k"], Fr(c["target"])
    e0 = Fr(c["small_eps"]["upto"])
    small = (1 + I(e0)) * I(Fr(k, k - 1)) * iv.log(I(k))
    assert small.b < I(target).a, "Proposition 12 bound fails"
    cur, total = e0, 0
    for r in c["intervals"]:
        e, e2, a, s1 = Fr(r["e"]), Fr(r["e2"]), Fr(r["a"]), Fr(r["s1"])
        assert e == cur and e2 > e, "gap in coverage at %s" % cur
        p = check_interval(k, 1 + e2, 1 - e, a, s1, target)
        if p is None:
            raise SystemExit("FAILED on [%s, %s]" % (e, e2))
        total += p
        cur = e2
    assert cur == 1, "coverage stops at %s" % cur
    print("OK: k=%d, M_{k,eps} < %s for all 0 <= eps < 1 (%d intervals, %d pieces; small eps by Prop. 12, bound %s)"
          % (k, target, len(c["intervals"]), total, float(small.b)))


if __name__ == "__main__":
    main()
