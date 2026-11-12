#!/usr/bin/env python3
"""Re-evaluate stored M_k certificates in exact rational arithmetic.

For each file written by code/mk_general.py (keys k, D, basis, coeffs, rayleigh) this rebuilds the
two Gram matrices from scratch (Lemma 3), checks that the stored basis is the one the builder
produces (all symmetric, or even power sums only), forms the exact Rayleigh quotient
k * q^T J q / q^T I q of the stored rational coefficient vector q, and checks that it equals the
stored value. A certificate proves M_k >= that quotient, whatever produced the vector.

usage: verify_cert.py code/cert_M54_D23e.json [more files ...]
"""
import sys, json
sys.path.insert(0, "code")
import mk_general as mg
from flint import fmpq, fmpq_mat


def verify(path):
    c = json.load(open(path))
    k, D = c["k"], c["D"]
    basis = [(a, tuple(b)) for a, b in c["basis"]]
    even = all(x == 0 for _, b in basis for j, x in enumerate(b) if (j + 2) % 2)
    mg.EVEN_ONLY = even
    b2, I, J = mg.build(k, D)
    assert [(a, tuple(b)) for a, b in b2] == basis, "basis does not match the builder"
    n = len(basis)
    q = fmpq_mat(n, 1, [fmpq(*map(int, s.split("/"))) if "/" in s else fmpq(int(s)) for s in c["coeffs"]])
    num = (q.transpose() * J * q)[0, 0] * k
    den = (q.transpose() * I * q)[0, 0]
    assert den > 0
    val = num / den
    stored = fmpq(*map(int, c["rayleigh"].split("/"))) if "/" in c["rayleigh"] else fmpq(int(c["rayleigh"]))
    assert val == stored, "Rayleigh quotient differs from the stored value"
    from fractions import Fraction
    f = float(Fraction(int(val.p), int(val.q)))
    print("%s: k=%d degree=%d %s, %d coefficients: M_k >= %.8f  (%s 4)"
          % (path, k, D, "even power sums" if even else "all symmetric", n, f, ">" if val > 4 else "NOT >"))
    return val > 4


if __name__ == "__main__":
    ok = [verify(p) for p in sys.argv[1:]]
