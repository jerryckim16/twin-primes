#!/usr/bin/env python3
"""Floor for one-band Stadlmann supports (Theorem 25 of paper v0.5).

Stadlmann's support T_k(delta, A, B, eps) with one band (n = 1, A = (-eps, A1)), any delta and any caps,
in Polymath scaling (u = 4t), lies inside the simplex {sum u <= L}, L = 4(A1 + eps), and its functional J
integrates the marginal over {u_1 + ... + u_{k-1} <= tau}, tau = 4(A1 - eps).  Hence the left side of the
criterion k(1-c1)J - k c2 K > I is at most k J and the criterion forces M_k(L, tau) > 4.
M_k(L, tau) is non-decreasing in L and tau, and for A1 <= A = 1/4 + omega it is at most M_k(4(A+eps), 4(A-eps)).

This script proves M_k(4(A+eps), 4(A-eps)) < 4 for every 0 <= eps < A (eps <= 0 reduces to eps = 0):
  * eps <= e1: M_k(L, tau) <= M_k(L, L) = L M_k <= L k/(k-1) log k  (dilation and Polymath8b Cor. 6.4), < 4;
  * [e1, A] is cut into intervals [e, e'] (step 1/2000, halved on failure); on each, (L, tau) = (4(A+e'), 4(A-e))
    and the two-zone dual bound of Theorem 15 gives sup_sigma W(sigma) < 4, certified in arb ball arithmetic.

usage: floor_hybrid.py k omega_p/omega_q [--out file.json]     (certify)
       floor_hybrid.py --check file.json                         (independent re-check with mpmath.iv)
"""
import sys, json
from fractions import Fraction as Fr
sys.path.insert(0, "code")

STEP = Fr(1, 2000)
TARGET = Fr(4)


def certify(k, omega, out=None):
    from flint import arb
    from dual_eps_cert import choose, certify_box, A as Aq, rat
    A = Fr(1, 4) + omega
    # small eps
    e1 = Fr(0)
    while Aq(4 * (A + e1 + STEP) * Fr(k, k - 1)) * arb(k).log() < Aq(TARGET):
        e1 += STEP
    small = Aq(4 * (A + e1) * Fr(k, k - 1)) * arb(k).log()
    assert small < Aq(TARGET)
    rows, guess, worst = [], None, 0.0
    todo = []
    e = e1
    while e < A:
        todo.append((e, min(e + STEP, A)))
        e += STEP
    todo.reverse()
    while todo:
        e, e2 = todo.pop()
        L, tau = 4 * (A + e2), 4 * (A - e)
        a, s1, fval, guess = choose(k, float(L), float(tau), guess)
        a_q, s1_q = rat(a), rat(s1)
        if s1_q <= tau:
            s1_q = tau + Fr(1, 10**6)
        if s1_q > L:
            s1_q = L
        if a_q < s1_q:
            a_q = s1_q
        pieces = certify_box(k, L, tau, a_q, s1_q, TARGET) if fval < 4 else None
        if pieces is None:
            if e2 - e < Fr(1, 10**6):
                return None, "failed at eps in [%s, %s], float sup W = %.6f" % (e, e2, fval)
            m = (e + e2) / 2
            todo += [(m, e2), (e, m)]
            guess = None
            continue
        worst = max(worst, fval)
        rows.append(dict(e=str(e), e2=str(e2), a=str(a_q), s1=str(s1_q), pieces=pieces, supW_float=round(fval, 6)))
    cert = dict(k=k, omega=str(omega), A=str(A), target=str(TARGET),
                small_eps=dict(upto=str(e1), bound=str(small.upper()),
                               reason="L*k/(k-1)*log k with L = 4(A+eps) (dilation + Polymath8b Cor. 6.4)"),
                intervals=rows, worst_float_supW=round(worst, 6))
    if out:
        json.dump(cert, open(out, "w"), indent=0)
    return cert, "certified %d intervals; worst float sup W = %.6f" % (len(rows), worst)


def check(path):
    from mpmath import iv
    sys.argv = [sys.argv[0]]
    import check_floor_cert as cf
    c = json.load(open(path))
    k, A, target = c["k"], Fr(c["A"]), Fr(c["target"])
    assert A == Fr(1, 4) + Fr(c["omega"])
    e1 = Fr(c["small_eps"]["upto"])
    small = cf.I(4 * (A + e1)) * cf.I(Fr(k, k - 1)) * iv.log(cf.I(k))
    assert small.b < cf.I(target).a, "small-eps bound fails"
    cur, total = e1, 0
    for r in c["intervals"]:
        e, e2, a, s1 = Fr(r["e"]), Fr(r["e2"]), Fr(r["a"]), Fr(r["s1"])
        assert e == cur and e2 > e, "gap in coverage at %s" % cur
        p = cf.check_interval(k, 4 * (A + e2), 4 * (A - e), a, s1, target)
        if p is None:
            raise SystemExit("FAILED on [%s, %s]" % (e, e2))
        total += p
        cur = e2
    assert cur == A, "coverage stops at %s" % cur
    print("OK: k=%d, omega=%s: M_k(4(A+eps), 4(A-eps)) < 4 for all 0 <= eps < A = %s (%d intervals, %d pieces)"
          % (k, c["omega"], A, len(c["intervals"]), total))


if __name__ == "__main__":
    if sys.argv[1] == "--check":
        for p in sys.argv[2:]:
            check(p)
    else:
        k = int(sys.argv[1])
        omega = Fr(sys.argv[2])
        out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
        cert, msg = certify(k, omega, out)
        print("k=%d omega=%s: %s" % (k, omega, msg), flush=True)
